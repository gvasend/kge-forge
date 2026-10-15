"""Generic qualification-scoped ATTEST authority materialization.

This module only constructs/admit typed authority chains; it never ingests
external evidence or changes a live Planner decision.
"""
from dataclasses import dataclass
import hashlib, json
from dataclasses import replace
from . import model as m
from . import codec

class AttestorError(m.PlannerError): pass

@dataclass(frozen=True)
class AttestContract:
    source: m.ArtifactIdentity
    proposition: m.EvidenceId
    gate: m.GateId
    scope: str
    lineage: str
    valid_until: int
    provenance: m.Provenance

@dataclass(frozen=True)
class AttestorChain:
    snapshot: m.Snapshot
    authority: m.GraphEntity
    authority_predicate: m.Predicate
    attestor: m.GraphEntity
    attestor_predicate: m.Predicate

def _digest(v): return hashlib.sha256(codec.canonical_bytes(v)).hexdigest()
def _ident(ns, payload): return m.ArtifactIdentity(m.IdentityKind.AUTHORITY_IDENTITY, ns, _digest(payload))

def materialize(snapshot, issuer: m.ArtifactIdentity, contract: AttestContract, authorization_identity: m.ArtifactIdentity):
    if snapshot.context is None or snapshot.context.scope != contract.scope or snapshot.context.lineage != contract.lineage:
        raise AttestorError('CONTEXT_MISMATCH')
    if contract.scope != 'E2-QUALIFICATION-ONLY': raise AttestorError('SCOPE_BROADENED')
    payload={'issuer':issuer.sha256,'source':contract.source.sha256,'proposition':contract.proposition.value,'gate':contract.gate.value,'scope':contract.scope,'lineage':contract.lineage,'authorization':authorization_identity.sha256,'valid_until':contract.valid_until}
    aid=_ident('qualification-attest-authority',payload); a_id=m.EntityId('E2-ATTEST-AUTHORITY:'+aid.sha256)
    apid=m.PredicateId('ATTEST-AUTHORITY:'+aid.sha256)
    auth=m.GraphEntity(a_id,m.EntityKind.AUTHORITY,aid,contract.provenance,contract.scope,contract.lineage,snapshot.context.generation,contract.valid_until,permissions=(m.AuthorityClass.ATTEST,),target=contract.source)
    ap=m.Predicate(apid,m.PredicateKind.AUTHORITY,entity=a_id,expected=contract.source,permission=m.AuthorityClass.ATTEST)
    tid=_ident('qualification-attestor',{'authority':aid.sha256,'source':contract.source.sha256,'proposition':contract.proposition.value,'gate':contract.gate.value,'scope':contract.scope,'lineage':contract.lineage}); t_id=m.EntityId('E2-SYNTHETIC-ATTESTOR:'+tid.sha256)
    tp_id=m.PredicateId('E2-ATTESTOR-MAY-ATTEST:'+tid.sha256)
    att=m.GraphEntity(t_id,m.EntityKind.AUTHORITY,tid,contract.provenance,contract.scope,contract.lineage,snapshot.context.generation,contract.valid_until,permissions=(m.AuthorityClass.ATTEST,),target=contract.source)
    tp=m.Predicate(tp_id,m.PredicateKind.AUTHORITY,entity=t_id,expected=contract.source,permission=m.AuthorityClass.ATTEST)
    if any(x.id in {a_id,t_id} for x in snapshot.entities) or any(x.id in {apid,tp_id} for x in snapshot.predicates): raise AttestorError('DUPLICATE')
    out=replace(snapshot,entities=snapshot.entities+(auth,att),predicates=snapshot.predicates+(ap,tp))
    m.validate_model(out)
    return AttestorChain(out,auth,ap,att,tp)
