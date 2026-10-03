"""Bounded evidence admission checks shared by live commands and canonical replay.

No authority import and no persistence path lives here. Receipt validation remains
in gates.py; this module admits only independently authenticated source objects.
"""
from dataclasses import replace, fields
import hashlib
from . import model as m


def command_key(event):
    from . import codec as c
    body = c._wire(event)
    del body['command_key']
    return c._identity(c.canonical_bytes(body), 'planner-evidence-command-v1')


def evidence_id(gate, identity, context):
    from . import codec as c
    body = dict(gate=c._wire(gate), content_identity=c._wire(identity),
                scope=context.scope, lineage=context.lineage, generation=context.generation)
    return m.EntityId('EVIDENCE:' + hashlib.sha256(c.canonical_bytes(body)).hexdigest())


def ingress(event):
    from . import codec as c
    sources = {x.provenance for x in event.field_provenance
               if x.provenance.identity == event.contract_pin}
    if len(sources) != 1:
        raise m.PlannerError('INGRESS_PROVENANCE')
    source = next(iter(sources))
    raw = source.excerpt.encode('utf-8')
    if source.section != '/' or source.identity != c._identity(raw, 'raw-file-sha256'):
        raise m.PlannerError('INGRESS_CONTENT_PIN')
    body = c.parse_json(raw)
    if type(body) is not dict or set(body) != {'schema', 'contract'} or body['schema'] != 'PLANNER-EVIDENCE-INGRESS-1':
        raise m.PlannerError('INGRESS_SCHEMA')
    record = dict(body['contract'])
    record['provenance'] = c._wire(source)
    contract = c._unwire(record)
    m.validate_types(contract, m.EvidenceIngressContract)
    expected = c._wire(contract); del expected['provenance']
    if raw != c.canonical_bytes({'schema': 'PLANNER-EVIDENCE-INGRESS-1', 'contract': expected}):
        raise m.PlannerError('INGRESS_CANONICAL')
    return contract


def field_bindings(entity, admission, contract):
    """Closed field-level source selectors, not caller-chosen semantic mappings."""
    result = []
    for field in fields(entity):
        key = field.name
        selector = '/contract/' + key if key in ('scope','lineage','generation','valid_until') else '/contract/source_class'
        source = contract.provenance
        if key in ('id','identity','provenance'):
            source, selector = entity.provenance, '/'
        result.append(m.EvidenceFieldProvenance('entity.' + key, selector, source))
    for field in fields(admission):
        key = field.name
        if key == 'dependencies':
            for dependency in admission.dependencies:
                result.append(m.EvidenceFieldProvenance('admission.dependencies.' + dependency.identity.sha256,
                    dependency.section, dependency))
            continue
        source, selector = entity.provenance, '/' + key
        if key in ('artifact','provenance'):
            selector = '/'
        if key in ('authentication','dependencies'):
            source, selector = contract.provenance, '/contract/authentication'
        result.append(m.EvidenceFieldProvenance('admission.' + key, selector, source))
    return tuple(sorted(result,key=lambda x:x.target))


def apply(snapshot, event):
    from . import codec as c, core, gates
    m.validate_model(snapshot); m.validate_types(event, m.EvidenceSourceAdmission)
    if event.schema != 'PLANNER-EVIDENCE-ADMISSION-1' or event.command_key != command_key(event):
        raise m.PlannerError('ADMISSION_SCHEMA_OR_KEY')
    if c.snapshot_id(snapshot) != event.expected_snapshot:
        raise m.PlannerError('PARENT_MISMATCH')
    gate = next((g for g in snapshot.external_gates if g.id == event.gate), None)
    if gate is None or gate.stage is not m.ExternalStage.WAITING_FOR_EXTERNAL_EVIDENCE or not gate.contract_complete or gate.validation is not m.ValidationState.ACCEPTED:
        raise m.PlannerError('NO_ACTIVE_GATE')
    contract = ingress(event); ctx = snapshot.context
    if ctx is None or contract.schema != 'PLANNER-EVIDENCE-INGRESS-1' or not contract.source_class:
        raise m.PlannerError('INGRESS_CONTRACT')
    if (contract.scope,contract.lineage,contract.generation) != (ctx.scope,ctx.lineage,ctx.generation) or contract.provenance.scope != ctx.scope:
        raise m.PlannerError('ENVELOPE_MISMATCH')
    required = set(event.requirements)
    if not required or len(required) != len(event.requirements) or required != set(contract.requirements) or not required <= set(gate.requirements) or contract.gate != gate.id or contract.receipt_action != gate.receipt_action or event.receipt_action != gate.receipt_action:
        raise m.PlannerError('RECEIPT_CORRESPONDENCE')
    # The same exact acquired-rule route is required for known and unknown rules.
    requirements = {r.id:r for r in snapshot.evidence_requirements}
    for ref in required:
        route = next((r for r in gate.resolution_contracts if r.requirement == ref),None)
        if route is None or route.source_class != contract.source_class:
            raise m.PlannerError('EXPECTED_SOURCE_CLASS')
        if not any(gates.governed_external_unknown(snapshot,gate,requirements[ref],a)
                   for a in gate.held_actions + gate.reentry):
            raise m.PlannerError('ROUTE_NOT_CURRENT')
    entity, admission = event.entity, event.admission
    if entity.id in {e.id for e in snapshot.entities} or any(a.artifact == entity.id for a in snapshot.receipt_admissions):
        raise m.PlannerError('IDENTITY_CONFLICT')
    if (entity.id != evidence_id(gate.id,entity.identity,ctx) or entity.kind is not m.EntityKind.EVIDENCE or
        (entity.scope,entity.lineage,entity.generation) != (ctx.scope,ctx.lineage,ctx.generation) or
        entity.valid_until != contract.valid_until or entity.valid_until < ctx.tick or
        not entity.produced or not entity.validated or entity.validation is not m.ValidationState.ACCEPTED or
        entity.permissions or entity.target is not None or entity.consumed or entity.validator is not None or
        entity.decision is not None or entity.choice is not None):
        raise m.PlannerError('ADMISSION_SCOPE_OR_CURRENTNESS')
    if admission.artifact != entity.id or admission.provenance != entity.provenance or admission.authentication != contract.authentication:
        raise m.PlannerError('RECEIPT_CORRESPONDENCE')
    if set(event.field_provenance) != set(field_bindings(entity,admission,contract)) or len(event.field_provenance) != len(field_bindings(entity,admission,contract)):
        raise m.PlannerError('FIELD_PROVENANCE')
    auth_record = next((p for p in snapshot.predicates if p.id == admission.authentication),None)
    trust = next((e for e in snapshot.entities if auth_record is not None and e.id == auth_record.entity),None)
    dependencies = {contract.provenance, gate.provenance}
    dependencies.update(requirements[r].provenance for r in required)
    dependencies.update(x.provenance for x in gate.resolution_contracts if x.requirement in required)
    if trust is not None:
        dependencies.add(trust.provenance)
    if set(admission.dependencies) != dependencies or len(admission.dependencies) != len(dependencies):
        raise m.PlannerError('DEPENDENCY_PROVENANCE')
    raw = c.canonical_bytes({'producer' :c._wire(admission.producer),'target':c._wire(admission.target),
        'claims': sorted((c._wire(x) for x in admission.claims),key=c.canonical_bytes)})
    source = entity.provenance
    if source.identity != entity.identity or entity.identity != c._identity(raw,'raw-file-sha256') or source.section != '/' or source.excerpt.encode() != raw or source.scope != ctx.scope or source.method != 'PLANNER-EVIDENCE-ADMISSION-1':
        raise m.PlannerError('SOURCE_PROVENANCE')
    if event.source_additions != (m.ArtifactPin(source.path,source.identity),):
        raise m.PlannerError('SOURCE_ADDITIONS')
    if len(admission.claims) != len(required) or {x.requirement for x in admission.claims} != required or any(x.outcome is m.ProofState.UNKNOWN for x in admission.claims):
        raise m.PlannerError('CLAIM_SCHEMA')
    for claim in admission.claims:
        r = requirements[claim.requirement]
        if admission.target != r.target or admission.producer not in r.producers:
            raise m.PlannerError('SOURCE_DOMAIN_OR_PRODUCER')
        for o in snapshot.receipt_observations:
            if o.gate == gate.id and o.accepted and any(x.requirement == claim.requirement and x.outcome != claim.outcome for x in o.claims):
                raise m.PlannerError('CLAIM_CONFLICT')
    auth = next((p for p in snapshot.predicates if p.id == admission.authentication),None)
    owner = next((e for e in snapshot.entities if auth is not None and e.id == auth.entity),None)
    if (auth is None or auth.kind is not m.PredicateKind.AUTHORITY or auth.permission is not m.AuthorityClass.ATTEST or
        auth.expected != entity.identity or owner is None or owner.identity != admission.producer or
        owner.provenance.identity == source.identity or owner.provenance.path == source.path or
        gates.evaluate_predicate(snapshot,auth.id).state is not m.ProofState.PROVED):
        raise m.PlannerError('PRODUCER_AUTHENTICATION_UNPROVED')
    updated = replace(snapshot,entities=snapshot.entities+(entity,),receipt_admissions=snapshot.receipt_admissions+(admission,))
    m.validate_model(updated)
    # Before any observation is accepted, insertion cannot advance planning.
    before, after = core.recompute(snapshot), core.recompute(updated)
    if before != after:
        raise m.PlannerError('ADMISSION_CHANGED_CONTROL')
    return core.TransitionReport(updated,(),after)
