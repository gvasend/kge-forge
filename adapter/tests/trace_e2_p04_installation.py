"""Read-only route/currentness and closed installation-interface diagnosis."""
from dataclasses import replace, fields
import ast
import hashlib
import json
from pathlib import Path
from typing import get_args
from adapter.planner import codec as c, model as m, core, gates, evidence as ev
from adapter.planner import evidence_attestation as ea, selector

R=Path(__file__).resolve().parents[2]
D=R/'docs/plans';P='DETERMINISTIC_PLANNER_V0_1_'
INPUT=D/'qualification/E2_P04_CONTINUATION_INPUT_CLOSURE_1'
OUT=D/'qualification/E2_P04_CONTRACT_INSTALLATION_CLOSURE_1'


def run():
    previous=json.loads((D/(P+'E2_P04_CONTINUATION_INPUT_CLOSURE_1.json')).read_text())
    b=c.restore(D/(P+'P03_PROSPECTIVE_CHECKPOINT_BUNDLE_1.json'),
        c._unwire(previous['P04_INITIAL_BUNDLE_ID']),R)
    original=c.bundle_bytes(b);s=b.current;g=s.external_gates[0]
    requirement=next(r for r in s.evidence_requirements if r.id in g.requirements)
    request=c._unwire(json.loads((INPUT/'a09-candidate.json').read_text()))
    attestation_fields=json.loads((INPUT/'evidence-binding.json').read_text())['attestation']['fields']
    attestation=ea.EvidenceBoundAttestation(**{k:c._unwire(v) for k,v in attestation_fields.items()})
    parents={'bundle':request.expected_bundle==c.bundle_id(b),
        'snapshot':request.expected_snapshot==c.snapshot_id(s),
        'event':request.expected_parent_event==b.events[-1].identity,
        'context':(request.entity.scope,request.entity.lineage,request.entity.generation)==
                  (s.context.scope,s.context.lineage,s.context.generation)}
    assert all(parents.values())
    try:ev.apply(s,request,attestation)
    except m.PlannerError as ex:failure=str(ex)
    else:raise AssertionError('unexpected accepted admission')
    assert failure=='ROUTE_NOT_CURRENT'
    route=g.resolution_contracts[0];wire=c._wire(route)
    wire.pop('$type');wire.pop('provenance')
    expected={'schema':'EXTERNAL-RESOLUTION-CONTRACT-1','contract':wire}
    raw=c.canonical_bytes(expected);actual=c.parse_json(route.provenance.excerpt.encode())
    template=c.parse_json(actual['template_provenance']['excerpt'].encode())
    prepared=c.parse_json((INPUT/'resolution-contract.json').read_bytes())
    field_comparison=[{'field':'/schema','expected':expected['schema'],
        'actual_present':False,'actual':None,'equal':False}]
    for key,value in wire.items():
        field_comparison.append({'field':'/contract/'+key,'expected':value,
            'actual_present':False,'actual':None,'equal':False,
            'nested_historical_template_value':template['contract'].get(key),
            'nested_template_is_native_source':False})
    semantic_bindings={
        'scope_lineage_generation':(route.scope,route.lineage,route.generation)==
            (s.context.scope,s.context.lineage,s.context.generation),
        'gate':route.gate==g.id,'requirement':route.requirement==requirement.id,
        'proposition':route.proposition==requirement.proposition,
        'target':route.target==requirement.target,
        'producers':set(route.producers)==set(requirement.producers),
        'gate_source':route.gate_source==g.provenance.identity,
        'requirement_source':route.requirement_source==requirement.provenance.identity,
        'receipt_action':route.receipt_action==g.receipt_action,
        'reentry':set(route.reentry)==set(g.reentry),
        'held_actions':set(route.held_actions)==set(g.held_actions)}
    assert all(semantic_bindings.values())
    assert prepared==expected, 'prepared route semantics differ from required route'
    # Isolated definition oracle only: no replacement bundle is adopted/saved.
    source_path=INPUT/'resolution-contract.json'
    prov=replace(route.provenance,path=str(source_path.relative_to(R)),
        identity=c._identity(raw,'raw-file-sha256'),excerpt=raw.decode())
    definition=replace(route,provenance=prov)
    def predicate(contract,gate=None,context=None):
        isolated_gate=replace(g,resolution_contracts=(contract,)) if gate is None else gate
        isolated=replace(s,external_gates=(isolated_gate,),context=context or s.context)
        return gates.governed_external_unknown(isolated,isolated_gate,requirement,g.reentry[0])
    assert not gates.governed_external_unknown(s,g,requirement,g.reentry[0])
    assert predicate(definition)
    negatives={}
    values={
        'wrong_route_source':replace(definition,provenance=replace(prov,excerpt='{}')),
        'wrong_route_pin':replace(definition,provenance=replace(prov,
            identity=replace(prov.identity,sha256=route.provenance.identity.sha256))),
        'wrong_identity_domain':replace(definition,provenance=replace(prov,
            identity=replace(prov.identity,kind=m.IdentityKind.AUTHORITY_IDENTITY))),
        'wrong_scope':replace(definition,scope='WRONG'),
        'wrong_lineage':replace(definition,lineage='WRONG')}
    for label,value in values.items():
        assert not predicate(value)
        negatives[label]={'result':'PASS_REJECTED','domain':'Native route predicate in isolated counterfactual definition fixture; not installation'}
    assert not predicate(definition,gate=replace(g,validation=m.ValidationState.STALE))
    negatives['stale_route']={'result':'PASS_REJECTED','domain':'Native gate stale validation; no source invalidation event applied'}
    try:selector.validate_policy(replace(b.policy,identity=prov.identity),b.policy_version)
    except m.PlannerError as ex:negatives['wrong_policy_pin']={'result':'PASS_REJECTED','reason':str(ex)}
    else:raise AssertionError('wrong policy accepted')
    foreign=c._unwire(json.loads((D/(P+'E2_P03_SEMANTIC_NATIVE_EVIDENCE_BINDING_1_CANDIDATE.json')).read_text()))
    assert request.expected_parent_event!=foreign.expected_parent_event
    negatives['another_parent_lineage']={'result':'PASS_REJECTED_BY_PARENT_ORACLE',
        'foreign_parent':c._wire(foreign.expected_parent_event),
        'actual_parent':c._wire(request.expected_parent_event),
        'domain':'Exact A09 parent oracle rejects historical G04/T01 parent event; route predicate itself does not authenticate parent events'}
    unqualified=['wrong_installation_authority','definition_installed_without_authority',
        'proof_INSTANCE_for_CONTRACT','ActionResult_for_accepted_result_CONTRACT']
    for label in unqualified:
        negatives[label]={'result':'NOT_QUALIFIED_NO_INSTALLATION_INTERFACE',
            'required_behavior':'Future installer must reject atomically before any durable state/source/event change'}
    event_types=get_args(m.ExecutionEvent.__annotations__['result'])
    source=ast.parse((R/'adapter/planner/core.py').read_text())
    apply=next(n for n in source.body if isinstance(n,ast.FunctionDef) and n.name=='apply_event')
    dispatch=sorted({n.attr for n in ast.walk(apply) if isinstance(n,ast.Attribute)
                     and isinstance(n.value,ast.Name) and n.value.id=='m'})
    assert c.bundle_bytes(b)==original
    assert c.restore(D/(P+'P03_PROSPECTIVE_CHECKPOINT_BUNDLE_1.json'),c.bundle_id(b),R)==b
    OUT.mkdir(parents=True,exist_ok=True)
    result={'initial_parent':parents,'initial_failure':failure,'pre_state':c._wire(c.snapshot_id(s)),
        'initial_bundle':c._wire(c.bundle_id(b)),'append_head':c._wire(b.events[-1].identity),
        'route_type':'ExternalResolutionContract','route_lookup_key':{'gate':g.id.value,'requirement':requirement.id.value},
        'no_native_RouteId':True,'canonical_route':c._wire(route),
        'expected_source':expected,'actual_source':actual,'field_comparison':field_comparison,
        'semantic_bindings':semantic_bindings,
        'expected_source_identity':c._wire(c._identity(raw,'raw-file-sha256')),
        'actual_source_identity':c._wire(route.provenance.identity),
        'prepared_source_identity':c._wire(prov.identity),'prepared_source_equals_expected':True,
        'original_route_predicate_current':False,
        'isolated_prepared_definition_predicate_current':True,
        'isolated_definition_installed_in_canonical_state':False,
        'prepared_pin_already_in_bundle':any(p.identity==prov.identity for p in b.sources),
        'event_union':[getattr(x,'__name__',str(x)) for x in event_types],
        'apply_event_dispatch_attributes':dispatch,
        'existing_route_definition_installation_event':False,
        'negative_controls':negatives,
        'installed_route':None,'post_install_state':None,'install_event':None,
        'canonical_state_unchanged':True,'accepted_P04_events':0}
    (OUT/'native-trace.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'parent':'PASS','first_failure':failure,
        'prepared_source_semantics':'PASS','installation':'NO_SUPPORTED_EVENT',
        'negative_route_policy_checks':8,'no_canonical_state_change':True}))


if __name__=='__main__':run()
