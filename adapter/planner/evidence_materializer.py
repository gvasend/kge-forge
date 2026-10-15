"""Generic semantic-to-native Evidence materialization.

The semantic fixture identity and the native provenance-bound entity identity
are deliberately separate domains.  This module performs the binding without
changing the native admission rule.
"""
from dataclasses import dataclass
import hashlib
from . import codec, evidence, model as m


SemanticNativeBinding = m.SemanticNativeBinding

@dataclass(frozen=True)
class MaterializedEvidence:
    entity: m.GraphEntity
    binding: SemanticNativeBinding
    canonical_provenance: bytes


def _admission_bytes(admission):
    return codec.canonical_bytes({
        'producer': codec._wire(admission.producer),
        'target': codec._wire(admission.target),
        'claims': sorted((codec._wire(x) for x in admission.claims),
                         key=codec.canonical_bytes),
    })


def materialize(*, semantic_evidence_id, content_id, gate, context,
                proposition, source_pin, attestor, attestor_predicate,
                admission, field_provenance_method='PLANNER-EVIDENCE-ADMISSION-1'):
    """Construct a native candidate; no Planner state is mutated."""
    raw = _admission_bytes(admission)
    raw_id = m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY,
                                'raw-file-sha256', hashlib.sha256(raw).hexdigest())
    entity_id = evidence.evidence_id(gate, raw_id, context)
    provenance = m.Provenance('qualification://planner/evidence-admission',
                              raw_id, '/', raw.decode('utf-8'),
                              field_provenance_method, context.scope)
    entity = m.GraphEntity(entity_id, m.EntityKind.EVIDENCE, raw_id, provenance,
                           context.scope, context.lineage, context.generation,
                           admission.target and 100 or 100)
    binding = SemanticNativeBinding(semantic_evidence_id, entity_id, content_id,
                                    proposition, source_pin, attestor,
                                    attestor_predicate, gate, context.scope,
                                    context.lineage, raw_id)
    validate_binding(binding, entity, content_id, proposition, source_pin,
                     attestor, attestor_predicate, gate, context)
    return MaterializedEvidence(entity, binding, raw)


def binding_identity(binding):
    body = {
        'semantic': codec._wire(binding.semantic_evidence_id),
        'native': codec._wire(binding.native_entity_id),
        'content': codec._wire(binding.content_id),
        'proposition': binding.proposition,
        'source': codec._wire(binding.source_pin),
        'attestor': codec._wire(binding.attestor),
        'predicate': codec._wire(binding.attestor_predicate),
        'gate': codec._wire(binding.gate), 'scope': binding.scope,
        'lineage': binding.lineage, 'provenance': codec._wire(binding.provenance),
    }
    return m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY,
                              'planner-semantic-native-binding-v1',
                              hashlib.sha256(codec.canonical_bytes(body)).hexdigest())


def validate_binding(binding, entity, content_id, proposition, source_pin,
                    attestor, attestor_predicate, gate, context):
    if binding.native_entity_id != entity.id:
        raise m.PlannerError('SEMANTIC_NATIVE_ENTITY_MISMATCH')
    if binding.content_id != content_id or binding.proposition != proposition:
        raise m.PlannerError('SEMANTIC_NATIVE_CONTENT_MISMATCH')
    if binding.source_pin != source_pin or binding.attestor != attestor or \
       binding.attestor_predicate != attestor_predicate or binding.gate != gate:
        raise m.PlannerError('SEMANTIC_NATIVE_SOURCE_MISMATCH')
    if (binding.scope, binding.lineage) != (context.scope, context.lineage):
        raise m.PlannerError('SEMANTIC_NATIVE_CONTEXT_MISMATCH')
    if entity.provenance.identity != binding.provenance:
        raise m.PlannerError('SEMANTIC_NATIVE_PROVENANCE_MISMATCH')
    return True
