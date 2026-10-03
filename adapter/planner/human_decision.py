"""Bounded E2 qualification human-decision materialization.

This module accepts an explicit option identifier and turns it into the
existing native ``RecordedDecision`` inputs.  It never chooses an option and
never mutates the live E2 snapshot.  Choice evidence is represented by the
native GraphEntity/KnowledgeRecord pair already required by
``apply_recorded_decision``; ALLOW additionally produces the narrowly scoped
E2-GRANT projection.
"""
from dataclasses import dataclass
import hashlib
import json
from typing import Optional

from . import model as m
from . import core
from . import codec


OPTIONS = ("ALLOW_QUALIFICATION_MAPPING", "DECLINE")
ISSUER_NAMESPACE = "qualification-authority"
CHOICE_NAMESPACE = "e2-choice-record"
GRANT_NAMESPACE = "e2-grant"
E2_SCOPE = "E2-QUALIFICATION-ONLY"
E2_LINEAGE = "E2-CANONICAL-BASELINE-1"
PROTOCOL_TRUST_ROOT = m.ArtifactIdentity(
    m.IdentityKind.CONTENT_IDENTITY, "raw-file-sha256",
    "d7478df57c6c7619eff262daa6e258103cd31e226db6e523e5d2de6a5a603da0")
QUALIFICATION_ISSUER = m.ArtifactIdentity(
    m.IdentityKind.AUTHORITY_IDENTITY, ISSUER_NAMESPACE,
    "ed59567bbe5e7c719975a4e64db157696bf349d42cb0e73695115a50606c330a")


class HumanDecisionError(m.PlannerError):
    """Rejected synthetic choice input or materialization binding."""


@dataclass(frozen=True)
class HumanChoiceInput:
    option: str
    issuer: m.ArtifactIdentity
    trust_root: m.ArtifactIdentity
    dossier: m.ArtifactIdentity
    subject: m.ActionId
    snapshot: m.ArtifactIdentity
    sequence: int


@dataclass(frozen=True)
class ChoiceEvidence:
    identity: m.ArtifactIdentity
    option: str
    issuer: m.ArtifactIdentity
    dossier: m.ArtifactIdentity
    subject: m.ActionId
    scope: str
    lineage: str
    sequence: int
    provenance: m.Provenance


@dataclass(frozen=True)
class DecisionMaterialization:
    snapshot: m.Snapshot
    evidence: ChoiceEvidence
    record: m.GraphEntity
    predicate: m.Predicate
    event: m.RecordedDecision
    grant: Optional[m.GraphEntity]
    grant_predicate: Optional[m.Predicate]


def _digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                    ensure_ascii=False).encode()).hexdigest()


def _raw_provenance(identity, section, excerpt, method):
    return m.Provenance("qualification://E2-P02-human-decision", identity,
                        section, excerpt, method, E2_SCOPE)


def _decision(snapshot):
    ds = tuple(d for d in snapshot.decisions if d.action.value == "E2-DECIDE")
    if len(ds) != 1:
        raise HumanDecisionError("E2-DECIDE decision subject is not uniquely bound")
    d = ds[0]
    if d.dossier is None or d.stage is not m.DecisionStage.DECISION_READY:
        raise HumanDecisionError("E2-DECIDE is not decision-ready")
    return d


def capture_choice(snapshot, supplied: HumanChoiceInput, trusted_root: m.ArtifactIdentity) -> ChoiceEvidence:
    """Authenticate an explicit option; no option is inferred or normalized."""
    m.validate_types(supplied, HumanChoiceInput)
    m.validate_model(snapshot)
    d = next((x for x in snapshot.decisions if x.action.value == "E2-DECIDE"), None)
    if d is None or d.dossier is None:
        raise HumanDecisionError("E2-DECIDE decision subject is not uniquely bound")
    from .codec import snapshot_id
    if supplied.option not in OPTIONS or supplied.option not in d.dossier.alternatives:
        raise HumanDecisionError("invalid E2 qualification option")
    if supplied.subject != d.action or supplied.dossier != _dossier_identity(d.dossier):
        raise HumanDecisionError("choice subject/dossier binding mismatch")
    if supplied.snapshot != snapshot_id(snapshot):
        raise HumanDecisionError("choice pre-state mismatch")
    if supplied.issuer != QUALIFICATION_ISSUER:
        raise HumanDecisionError("untrusted choice issuer")
    if trusted_root != PROTOCOL_TRUST_ROOT or supplied.trust_root != PROTOCOL_TRUST_ROOT:
        raise HumanDecisionError("choice trust root mismatch")
    if supplied.sequence < 0:
        raise HumanDecisionError("invalid choice sequence")
    if d.stage is m.DecisionStage.DECISION_RECORDED:
        if d.record is None or d.recorded_choice is None:
            raise HumanDecisionError("recorded decision has incomplete evidence")
        if supplied.option != d.recorded_choice:
            raise HumanDecisionError("conflicting second choice")
        record = next((e for e in snapshot.entities if e.id == d.record), None)
        if record is None or record.provenance.identity.kind is not m.IdentityKind.CONTENT_IDENTITY:
            raise HumanDecisionError("recorded choice evidence unavailable")
        try:
            payload = json.loads(record.provenance.excerpt)
        except (TypeError, ValueError):
            raise HumanDecisionError("recorded choice evidence is not canonical")
        if payload.get("issuer") != supplied.issuer.sha256 or payload.get("trust_root") != trusted_root.sha256:
            raise HumanDecisionError("repeated choice does not match authenticated evidence")
        return ChoiceEvidence(record.provenance.identity, supplied.option, supplied.issuer,
                              supplied.dossier, d.action, d.dossier.scope, E2_LINEAGE,
                              int(payload.get("sequence", supplied.sequence)), record.provenance)
    payload = {"subject": d.action.value, "option": supplied.option,
               "issuer": supplied.issuer.sha256, "dossier": supplied.dossier.sha256,
               "scope": d.dossier.scope, "lineage": E2_LINEAGE,
               "sequence": supplied.sequence, "trust_root": trusted_root.sha256}
    digest = _digest(payload)
    identity = m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY, "raw-file-sha256", digest)
    provenance = _raw_provenance(identity, "/choice", json.dumps(payload, sort_keys=True),
                                 "E2-T03-AUTHENTICATED-CHOICE-1")
    return ChoiceEvidence(identity, supplied.option, supplied.issuer, supplied.dossier,
                          d.action, d.dossier.scope, E2_LINEAGE, supplied.sequence, provenance)


def _dossier_identity(dossier):
    data = codec.canonical_bytes(codec._wire(dossier))
    return m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY, "planner-dossier-sha256",
                              hashlib.sha256(data).hexdigest())


def materialize_choice(snapshot: m.Snapshot, evidence: ChoiceEvidence) -> DecisionMaterialization:
    """Build native choice evidence and apply it through the unchanged path."""
    m.validate_types(evidence, ChoiceEvidence)
    d = next((x for x in snapshot.decisions if x.action.value == "E2-DECIDE"), None)
    if d is None or d.dossier is None:
        raise HumanDecisionError("E2-DECIDE decision subject is not uniquely bound")
    if d.stage is m.DecisionStage.DECISION_RECORDED:
        if d.record is None or d.recorded_choice != evidence.option:
            raise HumanDecisionError("conflicting recorded choice")
        record = next((e for e in snapshot.entities if e.id == d.record), None)
        predicate = next((p for p in snapshot.predicates if record is not None and p.entity == record.id), None)
        if record is None or predicate is None:
            raise HumanDecisionError("recorded choice binding unavailable")
        grant = next((e for e in snapshot.entities if e.id.value == "E2-GRANT"), None)
        grant_predicate = next((p for p in snapshot.predicates if p.id.value == "E2-USE-AUTHORITY"), None)
        event = m.RecordedDecision(d.action, evidence.option, record.id, predicate.id, codec.snapshot_id(snapshot))
        return DecisionMaterialization(snapshot, evidence, record, predicate, event, grant, grant_predicate)
    dossier_id = _dossier_identity(d.dossier)
    if evidence.dossier != dossier_id or evidence.subject != d.action or evidence.scope != d.dossier.scope:
        raise HumanDecisionError("choice evidence is not bound to current dossier")
    if evidence.lineage != E2_LINEAGE or evidence.option not in d.dossier.alternatives:
        raise HumanDecisionError("choice evidence scope/lineage/option mismatch")
    record_id = m.EntityId("E2-CHOICE-RECORD:" + evidence.identity.sha256)
    record_identity = m.ArtifactIdentity(m.IdentityKind.AUTHORITY_IDENTITY, CHOICE_NAMESPACE,
                                         evidence.identity.sha256)
    record = m.GraphEntity(record_id, m.EntityKind.AUTHORITY, record_identity,
        evidence.provenance, evidence.scope, evidence.lineage, "E2-GENERATION-1", 100,
        permissions=(m.AuthorityClass.DECIDE,), target=d.dossier.provenance.identity,
        decision=d.action, choice=evidence.option)
    predicate_id = m.PredicateId("E2-CHOICE-AUTHORITY:" + evidence.identity.sha256)
    predicate = m.Predicate(predicate_id, m.PredicateKind.AUTHORITY, entity=record.id,
                             expected=d.dossier.provenance.identity, permission=m.AuthorityClass.DECIDE)
    knowledge = m.KnowledgeRecord(m.KnowledgeId("decision-choice:" + d.action.value),
        m.KnowledgeState.KNOWN_COMPLETE, evidence.option, evidence.provenance)
    if record.id in {x.id for x in snapshot.entities} or predicate_id in {x.id for x in snapshot.predicates}:
        raise HumanDecisionError("duplicate choice evidence")
    # dataclasses.replace is imported locally to keep the public module small.
    from dataclasses import replace
    prepared = replace(snapshot, entities=snapshot.entities + (record,),
                       predicates=snapshot.predicates + (predicate,),
                       knowledge=snapshot.knowledge + (knowledge,))
    event = m.RecordedDecision(d.action, evidence.option, record.id, predicate.id,
                               codec.snapshot_id(prepared))
    applied = core.apply_recorded_decision(prepared, event).snapshot
    grant = grant_predicate = None
    if evidence.option == "ALLOW_QUALIFICATION_MAPPING":
        grant_payload = {"authority": "E2-GRANT", "subject": "E2-REENTER",
                          "permission": "USE", "scope": E2_SCOPE, "lineage": E2_LINEAGE,
                          "dossier": dossier_id.sha256, "choice": evidence.identity.sha256}
        grant_hash = _digest(grant_payload)
        grant_prov_id = m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY, "raw-file-sha256", grant_hash)
        grant_prov = _raw_provenance(grant_prov_id, "/grant", json.dumps(grant_payload, sort_keys=True),
                                     "E2-T03-QUALIFICATION-GRANT-1")
        grant = m.GraphEntity(m.EntityId("E2-GRANT"), m.EntityKind.AUTHORITY,
            m.ArtifactIdentity(m.IdentityKind.AUTHORITY_IDENTITY, GRANT_NAMESPACE, grant_hash),
            grant_prov, E2_SCOPE, E2_LINEAGE, "E2-GENERATION-1", 100,
            permissions=(m.AuthorityClass.USE,), target=dossier_id,
            decision=d.action, choice=evidence.option)
        grant_predicate = m.Predicate(m.PredicateId("E2-USE-AUTHORITY"), m.PredicateKind.AUTHORITY,
                                      entity=grant.id, expected=dossier_id, permission=m.AuthorityClass.USE)
        if grant.id in {x.id for x in applied.entities} or grant_predicate.id in {x.id for x in applied.predicates}:
            raise HumanDecisionError("E2-GRANT already exists")
        applied = replace(applied, entities=applied.entities + (grant,), predicates=applied.predicates + (grant_predicate,))
        m.validate_model(applied)
    return DecisionMaterialization(applied, evidence, record, predicate, event, grant, grant_predicate)


def apply_explicit_choice(snapshot, supplied, trusted_root):
    """Capture and materialize one explicit choice; safe for synthetic tests."""
    return materialize_choice(snapshot, capture_choice(snapshot, supplied, trusted_root))
