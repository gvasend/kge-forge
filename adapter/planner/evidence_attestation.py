"""Transient, evidence-bound attestation for atomic source admission."""
import hashlib
from . import codec, model as m

EvidenceBoundAttestation = m.EvidenceBoundAttestation

def identity(*, attestor_authority, attestor, source_predicate, source_pin,
                native_entity, semantic_evidence, content, proposition, gate,
                scope, lineage, provenance):
    body={'authority':codec._wire(attestor_authority),'attestor':codec._wire(attestor),
          'source_predicate':codec._wire(source_predicate),'source_pin':codec._wire(source_pin),
          'native_entity':codec._wire(native_entity),'semantic_evidence':codec._wire(semantic_evidence),
          'content':codec._wire(content),'proposition':proposition,'gate':codec._wire(gate),
          'scope':scope,'lineage':lineage,'provenance':codec._wire(provenance)}
    aid=m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY,'planner-evidence-attestation-v1',hashlib.sha256(codec.canonical_bytes(body)).hexdigest())
    return aid


def materialize(**fields):
    return EvidenceBoundAttestation(identity(**fields), **fields)

def validate(attestation, *, entity, contract, gate, context, source_pin,
             semantic_evidence, content, proposition, attestor):
    if attestation.native_entity != entity.id or attestation.attestor != attestor: raise m.PlannerError('EVIDENCE_ATTESTATION_ENTITY')
    if attestation.source_pin != source_pin or attestation.gate != gate: raise m.PlannerError('EVIDENCE_ATTESTATION_SOURCE')
    if attestation.semantic_evidence != semantic_evidence or attestation.content != content: raise m.PlannerError('EVIDENCE_ATTESTATION_SEMANTICS')
    if attestation.proposition != proposition or (attestation.scope,attestation.lineage)!=(context.scope,context.lineage): raise m.PlannerError('EVIDENCE_ATTESTATION_CONTEXT')
    if attestation.provenance != entity.provenance.identity: raise m.PlannerError('EVIDENCE_ATTESTATION_PROVENANCE')
    if contract.gate != gate or contract.scope != context.scope or contract.lineage != context.lineage: raise m.PlannerError('EVIDENCE_ATTESTATION_CONTRACT')
    return True
