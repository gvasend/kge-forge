"""Pure finite planner gates and bounded inventory acceptance; no effects."""
from .model import (ActionResult, ActionState, ConditionState, EffectClass,
                    GateKind, PlannerError, SuppliedResult, unique, validate_types, ValidationState)


def unavailable_support(snapshot):
    """Derive unavailable qualifications without deleting historical obligations.

    This is a finite projection of the existing state, not persisted parallel state.
    An accepted replacement of an assertion must be explicit; a second edge does
    not silently supersede a stale mandatory assertion.
    """
    stale = {a.id for a in snapshot.assertions if a.validation is m.ValidationState.STALE}
    unavailable = {a.subject for a in snapshot.assertions if a.id in stale and
                   a.relation is m.Relation.REQUIRES}
    unavailable.update(e.id for e in snapshot.entities if e.validation is m.ValidationState.STALE)
    unavailable.update(r.id for r in snapshot.roots if r.state is m.ConditionState.STALE or stale.intersection(r.evidence))
    unavailable.update(v.id for v in snapshot.slots if v.state is m.SlotState.STALE or stale.intersection(v.evidence))
    unavailable.update(k.id for k in snapshot.knowledge if k.validation is m.ValidationState.STALE or stale.intersection(k.evidence))
    unavailable.update(a.id for a in snapshot.actions if a.qualification is m.ValidationState.STALE or stale.intersection(a.evidence) or any(
        k.validation is m.ValidationState.STALE or stale.intersection(k.evidence) for k in a.accepted_inventory))
    edges = {(a.object, a.subject) for a in snapshot.assertions if a.relation is m.Relation.REQUIRES}
    edges.update((g.target, a.id) for a in snapshot.actions for g in a.prerequisites)
    while True:
        added = {after for before, after in edges if before in unavailable}
        for p in snapshot.predicates:
            direct = (p.entity, p.other, p.condition, p.action, p.knowledge)
            operands = (all(ref in unavailable for ref in p.operands) if p.kind is m.PredicateKind.ANY
                        else any(ref in unavailable for ref in p.operands))
            if any(ref in unavailable for ref in direct) or (p.operands and operands):
                added.add(p.id)
        added.update(r.id for r in snapshot.roots if r.predicate in unavailable)
        added.update(v.id for v in snapshot.slots if v.value in unavailable or
                     unavailable.intersection(v.requirements + v.root_requirements))
        for a in snapshot.actions:
            if a.authority in unavailable or unavailable.intersection(a.requirements):
                added.add(a.id)
            if a.id in unavailable:
                added.update(k.id for k in a.accepted_inventory)
        for d in snapshot.decisions:
            if d.dossier is not None and (unavailable.intersection(d.dossier.required_facts) or any(
                    c.predicate in unavailable for c in d.dossier.checks)):
                added.update((d.action,) + d.downstream)
        if added.issubset(unavailable):
            return frozenset(unavailable)
        unavailable.update(added)


def current_completion(snapshot, action_id):
    return (any(s.id == action_id and s.state is m.ActionState.COMPLETED for s in snapshot.statuses)
            and action_id not in unavailable_support(snapshot))


def blockers(action, snapshot):
    states = {s.id: s.state for s in snapshot.statuses}
    roots = {r.id: r.state for r in snapshot.roots}
    reasons = []
    if action.id in unavailable_support(snapshot):
        reasons.append("STALE_PREREQUISITE_SUPPORT:" + action.id.value)
    for boundary in snapshot.boundaries:
        if action.id in boundary.actions and boundary.kind is not m.BoundaryKind.EXTERNAL_EVIDENCE:
            reasons.append('CONTROL_BOUNDARY:'+boundary.id.value)
    for gate in snapshot.external_gates:
        if action.id in gate.held_actions+gate.reentry and (gate.stage is not m.ExternalStage.DEPENDENT_ACTION_REENTRY or
                not external_complete(snapshot,gate)):
            reasons.append('EXTERNAL_GATE:'+gate.id.value)
    if action.operation is m.OperationClass.DECISION_INPUT_ACQUISITION and not any(
            d.input_action == action.id for d in snapshot.decisions):
        reasons.append('DECISION_INPUT_ROUTE_MISSING')
    if action.operation is m.OperationClass.OTHER:
        reasons.append('UNSUPPORTED_OPERATION')
    if action.operation in (m.OperationClass.ARCHITECT_AUTHORITY, m.OperationClass.ARCHITECT_CONTRACT_DECISION):
        decision = next((d for d in snapshot.decisions if d.action == action.id), None)
        if decision is None or decision.stage is not m.DecisionStage.DECISION_READY or \
                decision_readiness(snapshot, decision).state is not m.DecisionReadiness.DECISION_READY:
            reasons.append('DECISION_NOT_READY')
        elif any(not recorded_decision_valid(snapshot, next(d for d in snapshot.decisions if d.action == ref))
                for ref in decision.depends_on):
            reasons.append('DECISION_DEPENDENCY_UNRECORDED')
    for decision in snapshot.decisions:
        if action.id == decision.input_action and decision.stage is not m.DecisionStage.DECISION_INPUTS_REQUIRED:
            reasons.append('DECISION_INPUT_ROUTE_NOT_READY')
        if action.id in decision.downstream and (decision.stage is not m.DecisionStage.DOWNSTREAM_REEVALUATION or
                not recorded_decision_valid(snapshot, decision)):
            reasons.append('DECISION_REENTRY_REQUIRED')
    if action.operation in (m.OperationClass.GOVERNED_OPERATION, m.OperationClass.IMPLEMENTATION_REPAIR,
                            m.OperationClass.VALIDATOR_IMPLEMENTATION) and action.authority is None:
        reasons.append('AUTHORITY_REQUIRED')
    if action.prepared_dossier is not None and action.prepared_dossier.validation is m.ValidationState.STALE:
        reasons.append('STALE_PREPARED_DOSSIER')
    stale = {a.id for a in snapshot.assertions if a.validation is ValidationState.STALE}
    for ref in action.evidence:
        if ref in stale:
            reasons.append('STALE_ASSERTION:' + ref.value)
    if any(k.validation is ValidationState.STALE or stale.intersection(k.evidence)
           for k in action.accepted_inventory):
        reasons.append('STALE_INVENTORY_CONTRACT')
    for gate in action.prerequisites:
        met = (current_completion(snapshot, gate.target)
               if gate.kind is GateKind.ACTION_COMPLETED
               else roots[gate.target] is ConditionState.SATISFIED)
        if not met:
            reasons.append(gate.kind.value + ':' + gate.target.value)
    for requirement in action.requirements:
        proof = evaluate_predicate(snapshot, requirement)
        if proof.state is not m.ProofState.PROVED:
            reasons.append('PREDICATE:' + requirement.value + ':' + proof.state.value)
    if action.authority is not None:
        predicate = next(p for p in snapshot.predicates if p.id == action.authority)
        if predicate.kind is not m.PredicateKind.AUTHORITY or evaluate_predicate(
                snapshot, action.authority).state is not m.ProofState.PROVED:
            reasons.append('AUTHORITY_REQUIRED')
    # Human actionability permits review only. Effect classification describes the
    # external decision, never permission for this scheduler to execute it.
    if action.effect is not EffectClass.NON_EFFECTING and action.operation not in (
            m.OperationClass.ARCHITECT_AUTHORITY, m.OperationClass.ARCHITECT_CONTRACT_DECISION):
        if snapshot.context is None or action.effect not in snapshot.context.allowed_effects or action.authority is None:
            reasons.append('EFFECT_NOT_AUTHORIZED')
    return tuple(sorted(set(reasons)))


def validate_result(action, supplied):
    validate_types(supplied, SuppliedResult)
    if supplied.action != action.id or supplied.result is not action.accepted_result:
        raise PlannerError('result differs from bounded outcome contract')
    if supplied.dossier is not None or action.prepared_dossier is not None:
        from .codec import canonical_bytes, _wire
        if canonical_bytes(_wire(supplied.dossier)) != canonical_bytes(_wire(action.prepared_dossier)):
            raise PlannerError('dossier differs from bounded input contract')
    unique(supplied.knowledge, lambda k: k.id)
    if not action.accepted_inventory:
        raise PlannerError('no accepted bounded result contract')
    key = lambda k: k.id.value
    if sorted(supplied.knowledge, key=key) != sorted(action.accepted_inventory, key=key):
        raise PlannerError('inventory result does not meet its exact evidence contract')


# Pure P03 predicates. They inspect admitted typed evidence, never acquire it.
from dataclasses import dataclass
from . import model as m


@dataclass(frozen=True)
class Proof:
    state: m.ProofState
    reasons: tuple


def _proof(state, reason=''):
    return Proof(state, (reason,) if reason else ())


def usable(entity, snapshot):
    if entity is None or not entity.produced or not entity.validated:
        return _proof(m.ProofState.UNKNOWN, 'EVIDENCE_MISSING_OR_UNVALIDATED')
    if entity.id in unavailable_support(snapshot):
        return _proof(m.ProofState.UNKNOWN, "STALE_PREREQUISITE_SUPPORT")
    if entity.validation is not m.ValidationState.ACCEPTED:
        return _proof(m.ProofState.UNKNOWN, 'STALE_EVIDENCE')
    context = snapshot.context
    if context is None:
        return _proof(m.ProofState.UNKNOWN, 'EVALUATION_CONTEXT_MISSING')
    if (entity.scope, entity.lineage, entity.generation) != (context.scope, context.lineage, context.generation):
        return _proof(m.ProofState.DISPROVED, 'SCOPE_LINEAGE_GENERATION_MISMATCH')
    if entity.valid_until < context.tick:
        return _proof(m.ProofState.DISPROVED, 'EXPIRED_EVIDENCE')
    return _proof(m.ProofState.PROVED)


def evaluate_predicate(snapshot, predicate_id):
    """Public admission boundary; recursive evaluation uses admitted state only."""
    m.validate_model(snapshot)
    m.validate_types(predicate_id, m.PredicateId)
    if predicate_id not in {p.id for p in snapshot.predicates}:
        raise m.PlannerError('REFERENCE_CONTRACT: unknown predicate ID')
    return _evaluate_predicate(snapshot, predicate_id)


def _evaluate_predicate(snapshot, predicate_id, visiting=()):
    if predicate_id in visiting:
        return _proof(m.ProofState.UNKNOWN, 'PREDICATE_CYCLE')
    instance = next((v for v in snapshot.validation_instances if v.predicate == predicate_id), None)
    if instance is not None:
        if instance.result is m.ValidationOutcome.PASS and instance.currentness is m.ValidationState.ACCEPTED:
            return _proof(m.ProofState.PROVED)
        if instance.result is m.ValidationOutcome.FAIL:
            return _proof(m.ProofState.DISPROVED, 'VALIDATION_FAILED')
        return _proof(m.ProofState.UNKNOWN, 'VALIDATION_UNAVAILABLE')
    predicate = next((p for p in snapshot.predicates if p.id == predicate_id), None)
    if predicate is None:
        return _proof(m.ProofState.UNKNOWN, 'PREDICATE_MISSING')
    p = predicate
    if p.unavailable is not None:
        return _proof(m.ProofState.UNKNOWN, 'EXPLICITLY_UNAVAILABLE')
    if p.kind is m.PredicateKind.EVIDENCE_OBLIGATION:
        return _obligation_proof(snapshot,p.obligation)
    if p.kind in (m.PredicateKind.ALL, m.PredicateKind.ANY,
                  m.PredicateKind.DOSSIER_COMPLETE, m.PredicateKind.RECEIPT_COMPLETE):
        if not p.operands:
            return _proof(m.ProofState.UNKNOWN, 'EMPTY_REQUIREMENTS')
        proofs = [_evaluate_predicate(snapshot, ref, visiting + (p.id,)) for ref in p.operands]
        states = {proof.state for proof in proofs}
        if p.kind is m.PredicateKind.ANY:
            result = (m.ProofState.PROVED if m.ProofState.PROVED in states else
                      m.ProofState.DISPROVED if states == {m.ProofState.DISPROVED} else m.ProofState.UNKNOWN)
        else:
            result = (m.ProofState.DISPROVED if m.ProofState.DISPROVED in states else
                      m.ProofState.PROVED if states == {m.ProofState.PROVED} else m.ProofState.UNKNOWN)
        return Proof(result, tuple(sorted({r for proof in proofs for r in proof.reasons})))
    if p.id in unavailable_support(snapshot):
        return _proof(m.ProofState.UNKNOWN, "STALE_PREREQUISITE_SUPPORT")
    if p.kind is m.PredicateKind.ACTION_COMPLETED:
        state = m.ActionState.COMPLETED if current_completion(snapshot, p.action) else None
        return _proof(m.ProofState.PROVED if state is m.ActionState.COMPLETED else m.ProofState.UNKNOWN,
                      '' if state is m.ActionState.COMPLETED else 'ACTION_INCOMPLETE')
    if p.kind is m.PredicateKind.CONDITION_SATISFIED:
        state = next((r.state for r in snapshot.roots if r.id == p.condition), None)
        return _proof(m.ProofState.PROVED if state is m.ConditionState.SATISFIED else
                      m.ProofState.DISPROVED if state is m.ConditionState.DISPROVED else m.ProofState.UNKNOWN,
                      '' if state is m.ConditionState.SATISFIED else 'CONDITION_UNPROVED')
    if p.kind is m.PredicateKind.KNOWLEDGE_ACCEPTED:
        known = next((k for k in snapshot.knowledge if k.id == p.knowledge), None)
        proved = known is not None and known.validation is m.ValidationState.ACCEPTED and \
            known.state is m.KnowledgeState.KNOWN_COMPLETE
        if proved and p.expected is not None:
            proved = (known.provenance.identity == p.expected and known.producer == p.action and
                      known.outcome is p.required_outcome)
        return _proof(m.ProofState.PROVED if proved else m.ProofState.UNKNOWN,
                      '' if proved else 'KNOWLEDGE_INCOMPLETE')
    entities = {e.id: e for e in snapshot.entities}
    entity = entities.get(p.entity)
    if p.kind is m.PredicateKind.UNSUPPORTED:
        return _proof(m.ProofState.UNKNOWN, 'UNSUPPORTED_RULE')
    source = usable(entity, snapshot)
    if source.state is not m.ProofState.PROVED:
        return source
    if p.kind in (m.PredicateKind.SOURCE_IDENTITY, m.PredicateKind.TYPED_EQUAL):
        if p.expected is None:
            return _proof(m.ProofState.UNKNOWN, 'EXPECTED_IDENTITY_MISSING')
        equal = entity.identity == p.expected
        return _proof(m.ProofState.PROVED if equal else m.ProofState.DISPROVED,
                      '' if equal else 'IDENTITY_TYPE_OR_VALUE_MISMATCH')
    if p.kind is m.PredicateKind.AUTHORITY:
        if p.permission is None or p.expected is None:
            return _proof(m.ProofState.UNKNOWN, 'AUTHORITY_REQUIREMENT_INCOMPLETE')
        permitted = (entity.kind is m.EntityKind.AUTHORITY and
            entity.identity.kind is m.IdentityKind.AUTHORITY_IDENTITY and
            p.permission in entity.permissions and entity.target == p.expected and not entity.consumed)
        return _proof(m.ProofState.PROVED if permitted else m.ProofState.DISPROVED,
                      '' if permitted else 'AUTHORITY_CLASS_TARGET_OR_REPLAY_MISMATCH')
    if p.kind is m.PredicateKind.EVIDENCE:
        return (_proof(m.ProofState.PROVED) if entity.kind is m.EntityKind.EVIDENCE
                else _proof(m.ProofState.DISPROVED, 'NOT_EVIDENCE'))
    if p.kind is m.PredicateKind.MAPPING_AVAILABLE:
        return (_proof(m.ProofState.PROVED) if entity.kind is m.EntityKind.MAPPING
                else _proof(m.ProofState.UNKNOWN, 'MAPPING_MISSING'))
    if p.kind is m.PredicateKind.PRODUCER_AVAILABLE:
        for relation in snapshot.assertions:
            if relation.validation is m.ValidationState.ACCEPTED and relation.relation is m.Relation.PRODUCED_BY \
                    and relation.subject == p.entity and (p.other is None or relation.object == p.other):
                producer = entities.get(relation.object)
                if producer is not None and producer.kind is m.EntityKind.PRODUCER and \
                        usable(producer, snapshot).state is m.ProofState.PROVED:
                    return _proof(m.ProofState.PROVED)
        return _proof(m.ProofState.UNKNOWN, 'PRODUCER_MISSING')
    if p.kind is m.PredicateKind.CONSUMER_CHECK:
        # A closed pure registry. EFFECTING_ONLY is rejected before invocation;
        # no user-supplied callback can run through this boundary.
        if entity.kind is not m.EntityKind.VALIDATOR or entity.validator is not m.ValidatorRule.PURE_IDENTITY_MATCH:
            return _proof(m.ProofState.UNKNOWN, 'PURE_VALIDATOR_REQUIRED')
        value = entities.get(p.other)
        available = usable(value, snapshot)
        if available.state is not m.ProofState.PROVED:
            return available
        if p.expected is None:
            return _proof(m.ProofState.UNKNOWN, 'CONSUMER_CONTRACT_INCOMPLETE')
        equal = value.identity == p.expected
        return _proof(m.ProofState.PROVED if equal else m.ProofState.DISPROVED,
                      '' if equal else 'CONSUMER_IDENTITY_MISMATCH')
    return _proof(m.ProofState.UNKNOWN, 'UNSUPPORTED_RULE')


@dataclass(frozen=True)
class Readiness:
    state: m.DecisionReadiness
    missing: tuple


def decision_readiness(snapshot, decision):
    """Independent nine-check evaluation; deferred downstream facts are not decision facts."""
    m.validate_model(snapshot)
    if decision.action in unavailable_support(snapshot):
        return Readiness(m.DecisionReadiness.STALE, ("STALE_PREREQUISITE_SUPPORT",))
    dossier = decision.dossier
    if dossier is None:
        return Readiness(m.DecisionReadiness.FACT_BLOCKED, ('DOSSIER_MISSING', decision.external_input))
    if dossier.validation is m.ValidationState.STALE:
        return Readiness(m.DecisionReadiness.STALE, ('STALE_DOSSIER',))
    missing_facts = tuple(ref.value for ref in dossier.required_facts
        if _evaluate_predicate(snapshot, ref).state is not m.ProofState.PROVED)
    if missing_facts:
        return Readiness(m.DecisionReadiness.FACT_BLOCKED, tuple(sorted(missing_facts)))
    checks = {check.kind: check for check in dossier.checks}
    # Only checks with an authoritative dossier-level proposition participate
    # in native admission.  Historical labels rehomed by the E2 boundary
    # reconciliation remain descriptive dossier metadata.
    missing = [kind.value for kind in m.SUPPORTED_DOSSIER_CHECKS if kind not in checks or
        _evaluate_predicate(snapshot, checks[kind].predicate).state is not m.ProofState.PROVED]
    if not all((dossier.question, dossier.scope, dossier.alternatives,
                dossier.authority_granted_if_approved, dossier.authority_excluded)) or any(
                    not option for option in dossier.alternatives):
        missing.append('DOSSIER_STRUCTURE_INCOMPLETE')
    return Readiness(m.DecisionReadiness.SEMANTICALLY_INCOMPLETE if missing else
        m.DecisionReadiness.DECISION_READY, tuple(sorted(missing)))


def recorded_decision_valid(snapshot, decision):
    if decision.stage not in (m.DecisionStage.DECISION_RECORDED, m.DecisionStage.DOWNSTREAM_REEVALUATION) or \
            decision_readiness(snapshot, decision).state is not m.DecisionReadiness.DECISION_READY:
        return False
    entity = next((e for e in snapshot.entities if e.id == decision.record), None)
    return entity is not None and entity.kind is m.EntityKind.AUTHORITY and not entity.consumed and \
        entity.decision == decision.action and entity.choice == decision.recorded_choice and \
        m.AuthorityClass.DECIDE in entity.permissions and entity.target == decision.dossier.provenance.identity and \
        usable(entity, snapshot).state is m.ProofState.PROVED


def _check_receipt(snapshot, gate, artifact):
    """Pure admission check. A raw hash is not a producer-authentication rule."""
    admission=next((a for a in snapshot.receipt_admissions if a.artifact==artifact),None)
    entity=next((e for e in snapshot.entities if e.id==artifact),None)
    if gate.validation is not m.ValidationState.ACCEPTED or not gate.contract_complete:
        return Proof(m.ProofState.UNKNOWN,('UNQUALIFIED_RECEIPT_CONTRACT',))
    if admission is None or entity is None or entity.kind is not m.EntityKind.EVIDENCE:
        return Proof(m.ProofState.UNKNOWN,('INDEPENDENT_AUTHENTICATION_MISSING',))
    available=usable(entity,snapshot)
    if available.state is not m.ProofState.PROVED:
        return available
    # Explicit source pin + exact producer competence attestation, independently admitted.
    from .codec import canonical_bytes, _wire
    import hashlib
    body=canonical_bytes({'producer':_wire(admission.producer),'target':_wire(admission.target),
                          'claims':sorted((_wire(c) for c in admission.claims),key=canonical_bytes)})
    if entity.identity != m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY,'raw-file-sha256',hashlib.sha256(body).hexdigest()) or entity.provenance.identity!=entity.identity:
        return Proof(m.ProofState.DISPROVED,('RECEIPT_CONTENT_IDENTITY_MISMATCH',))
    predicate=next(p for p in snapshot.predicates if p.id==admission.authentication)
    owner=next((e for e in snapshot.entities if e.id==predicate.entity),None)
    if predicate.kind is not m.PredicateKind.AUTHORITY or predicate.permission is not m.AuthorityClass.ATTEST or \
            predicate.expected!=entity.identity or owner is None or owner.identity!=admission.producer or \
            owner.provenance.identity==entity.provenance.identity or owner.provenance.path==entity.provenance.path:
        return Proof(m.ProofState.UNKNOWN,('UNBOUND_PRODUCER_ATTESTATION',))
    authentication=_evaluate_predicate(snapshot,admission.authentication)
    if authentication.state is not m.ProofState.PROVED:
        return Proof(m.ProofState.UNKNOWN,('PRODUCER_AUTHENTICATION_UNPROVED',)+authentication.reasons)
    requirements={r.id:r for r in snapshot.evidence_requirements}
    if not admission.claims or any(c.requirement not in gate.requirements for c in admission.claims):
        return Proof(m.ProofState.DISPROVED,('EMPTY_OR_UNRELATED_RECEIPT',))
    for claim in admission.claims:
        requirement=requirements[claim.requirement]
        if not requirement.rule_known or not requirement.producers:
            return Proof(m.ProofState.UNKNOWN,('PROOF_RULE_OR_PRODUCER_UNKNOWN',))
        if admission.target!=requirement.target or admission.producer not in requirement.producers:
            return Proof(m.ProofState.DISPROVED,('PRODUCER_OR_TARGET_MISMATCH',))
    return Proof(m.ProofState.PROVED,())


def _obligation_proof(snapshot, ref):
    requirement=next((r for r in snapshot.evidence_requirements if r.id==ref),None)
    if requirement is None or not requirement.rule_known:
        return Proof(m.ProofState.UNKNOWN,('PROOF_RULE_UNKNOWN',))
    outcomes=set()
    for observation in snapshot.receipt_observations:
        if not observation.accepted:
            continue
        gate=next(g for g in snapshot.external_gates if g.id==observation.gate)
        if _check_receipt(snapshot,gate,observation.artifact).state is m.ProofState.PROVED:
            outcomes.update(c.outcome for c in observation.claims if c.requirement==ref)
    if len(outcomes)!=1:
        return Proof(m.ProofState.UNKNOWN,('CONFLICTING_PROOFS' if outcomes else 'PROOF_RULE_KNOWN_EVIDENCE_MISSING',))
    return Proof(next(iter(outcomes)),())


def _external_complete(snapshot, gate):
    return gate.validation is m.ValidationState.ACCEPTED and gate.contract_complete and all(
        _obligation_proof(snapshot,ref).state is m.ProofState.PROVED for ref in gate.requirements)


# Public receipt/proof queries admit once. Internal traversal only receives
# immutable snapshots admitted by these wrappers or by the core entry point.
def check_receipt(snapshot, gate, artifact):
    m.validate_model(snapshot)
    return _check_receipt(snapshot, gate, artifact)


def obligation_proof(snapshot, ref):
    m.validate_model(snapshot)
    return _obligation_proof(snapshot, ref)


def external_complete(snapshot, gate):
    m.validate_model(snapshot)
    return _external_complete(snapshot, gate)


def governed_external_unknown(snapshot, gate, requirement, action_id):
    """Control-only admission. UNKNOWN proof and receipt/resume gates are unchanged.

    The source is an independently pinned canonical acquisition contract. Its
    typed projection must match exact source bytes and current native bindings;
    caller-provided completeness/wait labels are not authentication.
    """
    import hashlib
    from . import codec
    contract = next((c for c in gate.resolution_contracts if c.requirement == requirement.id), None)
    context = snapshot.context
    if contract is None or context is None or not gate.contract_complete or gate.validation is not m.ValidationState.ACCEPTED:
        return False
    if gate.stage not in (m.ExternalStage.EXTERNAL_EVIDENCE_REQUIRED,
                          m.ExternalStage.EVIDENCE_REQUEST_READY,
                          m.ExternalStage.WAITING_FOR_EXTERNAL_EVIDENCE,
                          m.ExternalStage.EVIDENCE_RECEIVED,
                          m.ExternalStage.EVIDENCE_VALIDATED):
        return False
    if not contract.request or not contract.source_class or not all((contract.scope, contract.lineage, contract.generation)):
        return False
    if (contract.scope, contract.lineage, contract.generation) != (context.scope, context.lineage, context.generation):
        return False
    if (contract.provenance.scope != context.scope or gate.provenance.scope != context.scope or
        requirement.provenance.scope != context.scope or contract.provenance.section != '/'):
        return False
    if (contract.gate != gate.id or contract.requirement not in gate.requirements or
        contract.proposition != requirement.proposition or contract.target != requirement.target or
        set(contract.producers) != set(requirement.producers) or
        contract.requirement_source != requirement.provenance.identity or
        contract.gate_source != gate.provenance.identity or
        contract.receipt_action != gate.receipt_action or
        set(contract.reentry) != set(gate.reentry) or set(contract.held_actions) != set(gate.held_actions)):
        return False
    if action_id not in gate.held_actions + gate.reentry:
        return False
    action = next(a for a in snapshot.actions if a.id == action_id)
    predicates = {p.id:p for p in snapshot.predicates}
    pending = list(action.requirements)
    seen = set()
    bound = False
    while pending:
        ref = pending.pop()
        if ref in seen:
            continue
        seen.add(ref)
        p = predicates[ref]
        if p.kind is m.PredicateKind.EVIDENCE_OBLIGATION and p.obligation == requirement.id:
            bound = True
        pending.extend(p.operands)
    if not bound:
        return False
    # Independent source pin binds every field, including identity domains and
    # route/envelope correspondence. Provenance itself is outside its own hash.
    body = codec._wire(contract)
    del body['$type']
    del body['provenance']
    expected = codec.canonical_bytes({'schema':'EXTERNAL-RESOLUTION-CONTRACT-1', 'contract':body})
    source = contract.provenance
    return (source.excerpt.encode('utf-8') == expected and
            source.identity == m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY,
                'raw-file-sha256', hashlib.sha256(expected).hexdigest()))
