"""Persisted, explicitly separated evidence lifecycle transitions.

Receipt admission only creates RECEIVED evidence.  This module owns the
subsequent validation, proof-observation, and reentry-evaluation boundaries;
each operation is deterministic and returns a new immutable snapshot.
"""
from dataclasses import dataclass, replace
import hashlib
from . import model as m
from . import codec


@dataclass(frozen=True)
class ValidationResult:
    identity: m.ArtifactIdentity
    evidence: m.EntityId
    predicate: m.PredicateId
    outcome: m.ValidationOutcome
    scope: str
    lineage: str


@dataclass(frozen=True)
class ProofResult:
    identity: m.ArtifactIdentity
    evidence: m.EntityId
    requirement: m.EvidenceId
    scope: str
    lineage: str


@dataclass(frozen=True)
class ReentryResult:
    identity: m.ArtifactIdentity
    gate: m.GateId
    eligible: bool
    scope: str
    lineage: str


def _id(namespace, body):
    return m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY, namespace,
                              hashlib.sha256(codec.canonical_bytes(body)).hexdigest())


def validate_evidence(snapshot, evidence_id, predicate, proposition, inputs,
                      contract, oracle, provenance):
    """Apply an independent validation oracle to received evidence."""
    m.validate_model(snapshot)
    entity = next((e for e in snapshot.entities if e.id == evidence_id), None)
    if entity is None or not any(a.artifact == evidence_id for a in snapshot.receipt_admissions):
        raise m.PlannerError('VALIDATION_REQUIRES_RECEIPT')
    if entity.validation is not m.ValidationState.NOT_EVALUATED or not entity.produced:
        raise m.PlannerError('VALIDATION_STAGE')
    if snapshot.context is None or (entity.scope, entity.lineage) != (snapshot.context.scope, snapshot.context.lineage):
        raise m.PlannerError('VALIDATION_SCOPE_LINEAGE')
    if type(oracle) is not bool:
        raise m.PlannerError('VALIDATION_ORACLE_REQUIRED')
    result = m.ValidationOutcome.PASS if oracle else m.ValidationOutcome.FAIL
    identity = _id('planner-validation-v1', {'evidence': evidence_id.value,
        'predicate': predicate.value, 'proposition': proposition,
        'inputs': sorted((codec._wire(x) for x in inputs), key=codec.canonical_bytes),
        'contract': codec._wire(contract), 'scope': entity.scope,
        'lineage': entity.lineage, 'provenance': codec._wire(provenance),
        'result': result.value})
    prior = next((v for v in snapshot.validation_instances if v.predicate == predicate), None)
    if prior is not None:
        if prior.result is result and prior.provenance == provenance:
            return snapshot, ValidationResult(identity, evidence_id, predicate, result, entity.scope, entity.lineage)
        raise m.PlannerError('VALIDATION_CONFLICT')
    instance = m.ValidationInstance(predicate, proposition, contract, tuple(inputs), result,
                                     entity.scope, entity.lineage,
                                     m.ValidationState.ACCEPTED if oracle else m.ValidationState.REJECTED,
                                     provenance)
    updated_entity = replace(entity, validated=oracle,
                             validation=m.ValidationState.ACCEPTED if oracle else m.ValidationState.REJECTED)
    updated = replace(snapshot,
        entities=tuple(updated_entity if e.id == evidence_id else e for e in snapshot.entities),
        validation_instances=snapshot.validation_instances + (instance,))
    m.validate_model(updated)
    return updated, ValidationResult(identity, evidence_id, predicate, result, entity.scope, entity.lineage)


def admit_proof(snapshot, gate, evidence_id, requirement, validation, proposition,
                source_pin, scope, lineage, provenance):
    """Admit the typed proof boundary using the native receipt observation path."""
    from . import core
    entity = next((e for e in snapshot.entities if e.id == evidence_id), None)
    if entity is None or validation.outcome is not m.ValidationOutcome.PASS or \
            entity.validation is not m.ValidationState.ACCEPTED or (entity.scope, entity.lineage) != (scope, lineage):
        raise m.PlannerError('PROOF_REQUIRES_ACCEPTED_VALIDATION')
    if not proposition or source_pin is None or provenance is None:
        raise m.PlannerError('PROOF_CONTRACT_INCOMPLETE')
    # T01 admission creates the receipt object; the external lifecycle still
    # needs its explicit RECEIVED boundary before validation can be recorded.
    received = core.apply_receipt(snapshot, m.ExternalEvent(
        gate, m.ExternalStage.EVIDENCE_RECEIVED, codec.snapshot_id(snapshot), evidence_id))
    transition = core.apply_receipt(received.snapshot, m.ExternalEvent(
        gate, m.ExternalStage.EVIDENCE_VALIDATED, codec.snapshot_id(received.snapshot)))
    observation = next((o for o in transition.snapshot.receipt_observations
                        if o.gate == gate and o.artifact == evidence_id), None)
    if observation is None or not observation.accepted:
        raise m.PlannerError('PROOF_NOT_ACCEPTED')
    identity = _id('planner-proof-v1', {'evidence': evidence_id.value,
        'requirement': requirement.value, 'validation': validation.identity.sha256,
        'proposition': proposition, 'source': codec._wire(source_pin),
        'scope': scope, 'lineage': lineage, 'provenance': codec._wire(provenance)})
    return transition.snapshot, ProofResult(identity, evidence_id, requirement, scope, lineage)


def evaluate_reentry(snapshot, gate, scope, lineage, provenance):
    """Evaluate reentry without completing or selecting an Action."""
    from . import core, gates
    g = next((x for x in snapshot.external_gates if x.id == gate), None)
    if g is None or (g.scope if hasattr(g, 'scope') else scope) != scope:
        # ExternalGate carries scope through its resolution contracts.
        raise m.PlannerError('REENTRY_GATE_SCOPE')
    eligible = gates.external_complete(snapshot, g)
    if not eligible:
        identity = _id('planner-reentry-v1', {'gate': gate.value, 'eligible': False,
            'scope': scope, 'lineage': lineage, 'provenance': codec._wire(provenance)})
        return snapshot, ReentryResult(identity, gate, False, scope, lineage)
    event = m.ExternalEvent(gate, m.ExternalStage.DEPENDENT_ACTION_REENTRY,
                            codec.snapshot_id(snapshot))
    transition = core.apply_receipt(snapshot, event)
    # Decision-backed reentry is a separate native prerequisite.  Reevaluate
    # it after the external proof is complete; this only reopens the declared
    # downstream Action and never completes that Action.
    state = transition.snapshot
    current_gate = next(g for g in state.external_gates if g.id == gate)
    for decision in state.decisions:
        if decision.stage is m.DecisionStage.DECISION_RECORDED and \
                any(a in decision.downstream for a in current_gate.reentry):
            state = core.apply_decision_reentry(state, m.DecisionReentry(
                decision.action, codec.snapshot_id(state))).snapshot
            break
    identity = _id('planner-reentry-v1', {'gate': gate.value, 'eligible': True,
        'scope': scope, 'lineage': lineage, 'provenance': codec._wire(provenance)})
    return state, ReentryResult(identity, gate, True, scope, lineage)
