"""Read-only PC01->END qualification projection; never changes Planner state."""
import argparse
from copy import deepcopy
from dataclasses import replace
import hashlib
import json
import os
import sys
from pathlib import Path

from adapter.planner import codec as c, core, model as m, action_installation as ai

ROOT=Path(__file__).resolve().parents[4]
OUT=Path(__file__).resolve().parent
DOCS=ROOT/'docs/plans'
P='DETERMINISTIC_PLANNER_V0_1_'
CLOSURE=ROOT/'docs/plans/qualification/E2_P05_END_INTERFACE_CLOSURE_1'
BASE_ID='qualification-END-evidence-graph-v1:d3979240252a12139aac34db1bb1cb2396c6860af371084b94118740ec23af15'
ACCEPTANCE_ID='qualification-composite-END-acceptance-v1:6c37715a38233e9f556279e182bb3a13d5f03579257e20d787a858c5d246941c'
INPUT_ID='E2-END#/dependencies/0'
CALLS=[]


def deny(name):
    def no(*a,**kw):
        CALLS.append(name)
        raise AssertionError('Binding cannot perform '+name)
    return no


for mod,names in ((core,('apply_event','apply_result','apply_receipt','recompute','resume_eligibility','_inventory')),
    (c,('apply_event','_replay','record_result','append_event','commit_event','commit_result','save_bundle','restore',
        'admit_external_evidence','_publish_head','_prefix_bundle','bundle_id','bundle_bytes'))):
    for name in names:setattr(mod,name,deny(mod.__name__+'.'+name))


class Reject(Exception):
    def __init__(self,term,expected,actual):
        self.record={'term':term,'expected':expected,'actual':actual}
        super().__init__(json.dumps(self.record,sort_keys=True,default=str))


def equal(term,actual,expected):
    if actual!=expected:raise Reject(term,expected,actual)


def read(path):return json.loads(Path(path).read_bytes())
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def aid(value):return value.namespace+':'+value.sha256
def qid(namespace,value):return namespace+':'+hashlib.sha256(c.canonical_bytes(value)).hexdigest()


def ref(path,pointer=''):
    return {'path':str(Path(path).relative_to(ROOT)),'pointer':pointer,'raw_sha256':sha(path)}


def save(name,value):
    path=OUT/name
    raw=(json.dumps(value,sort_keys=True,indent=2,ensure_ascii=False)+'\n').encode()
    if path.exists():equal('immutable new evidence '+name,path.read_bytes().hex(),raw.hex())
    else:
        path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw)


def pointer(value,path):
    for token in path.split('/')[1:]:
        token=token.replace('~1','/').replace('~0','~')
        value=value[int(token)] if isinstance(value,list) else value[token]
    return value


def pins(value):
    if isinstance(value,dict):
        if isinstance(value.get('path'),str) and isinstance(value.get('raw_sha256'),str):yield value
        for child in value.values():yield from pins(child)
    elif isinstance(value,list):
        for child in value:yield from pins(child)


def check_pins(value):
    for item in pins(value):
        path=ROOT/item['path'];equal('source pin '+item['path'],sha(path),item['raw_sha256'])
        if item.get('pointer') and path.suffix=='.json':pointer(read(path),item['pointer'])


def source_specs():
    old=read(CLOSURE/'minimum-PC01-closure-contract.json')
    return [
        {'role':'PC01_ORIGINAL_QUALIFIED_MODEL','source':old['source']['included_native_original_model'],
         'snapshot_id':'planner-snapshot-v1:545ad19184d8dd7dfb5b2737e081b043d13982f05d05326939ac2cbb89bf54e2',
         'context':{'$type':'EvaluationContext','scope':'E2-QUALIFICATION-ONLY','lineage':'E2-CANONICAL-BASELINE-1','generation':'E2-GENERATION-1','tick':0,'allowed_effects':[]},
         'use':'Historical qualified baseline definition/model view; not a current P04 state or replayable source archive'},
        {'role':'P04_CURRENT_DEFINITION_MODEL','source':old['source']['included_canonical_current_model'],
         'snapshot_id':'planner-snapshot-v1:046fdc270a0060503729151368a68672f76af122830b86e65d372e6bc5d7dea4',
         'context':{'$type':'EvaluationContext','scope':'E2-QUALIFICATION-ONLY','lineage':'E2-P03-PROSPECTIVE-QUALIFICATION-1','generation':'E2-P03-PROSPECTIVE-GENERATION-1','tick':0,'allowed_effects':[]},
         'use':'Exact current canonical definition/version view; lifecycle facts are observed, not reproduced'}]


def process_definition():
    body={'schema':'PC01-END-READ-ONLY-PROCESS-1','kind':'READ_ONLY_QUALIFICATION_PROJECTION_AND_AGGREGATION',
        'consumer':INPUT_ID,'contract':ref(CLOSURE/'PC01-process-contract.json'),
        'code':ref(OUT/'binding.py'),'oracle_code':ref(OUT/'oracle.py'),
        'native_primitives':{name:ref(ROOT/('adapter/planner/'+name+'.py')) for name in ('model','codec','action_installation','installation','selector')},
        'authority':ref(CLOSURE/'PC01-authority-requirement.json'),
        'invocations':{'seal':[sys.executable,str(OUT.relative_to(ROOT)/'oracle.py')],
            'materialize':[sys.executable,str(OUT.relative_to(ROOT)/'binding.py'),'materialize'],
            'preflight':[sys.executable,str(OUT.relative_to(ROOT)/'binding.py'),'preflight'],
            'readers':[[sys.executable,str(OUT.relative_to(ROOT)/'binding.py'),'reader','--seed',str(seed),'--index',str(index),'--presentation',form]
                       for seed in (0,1,7,101) for index in (1,2,3) for form in ('original','reversed','rotated')]},
        'interpreter':{'path':sys.executable,'version':sys.version},
        'declared_seed_values':[0,1,7,101],'declared_reader_indices':[1,2,3],
        'declared_presentations':['original','reversed','rotated'],
        'no_new_native_process_id':True,'no_P05_native_execution_or_INSTALL_or_authority':True}
    return {'identity':qid('qualification-PC01-END-process-v1',body),'process':body}


def consumer():
    return {'contract':ref(CLOSURE/'END-PC01-consumer-contract.json'),'input_id':INPUT_ID,
        'declaration':read(CLOSURE/'END-PC01-consumer-contract.json')['consumer_authority_sources'][0],
        'edge_id':read(CLOSURE/'minimum-PC01-closure-contract.json')['identity']['consumer_edge_id'],
        'composite_graph_identity':BASE_ID,'acceptance_mapping_identity':ACCEPTANCE_ID,
        'scope_capture':ref(ROOT/'docs/plans/qualification/E2_P05_COMPOSITE_END_QUALIFICATION_1/scope-authentication.json'),
        'native_END_action_or_slot':False}


def inputs():
    old=read(CLOSURE/'minimum-PC01-closure-contract.json')
    specs=source_specs()
    return [
        ('PC01_DEFINITION_SOURCE','E2-PC01-DEFINITION-SOURCE-1',old['source']['definition']),
        ('PC01_QUALIFICATION','E2-PC01-EXIT-RECONCILIATION-1',ref(DOCS/(P+'E2_PC01_EXIT_RECONCILIATION_1.json'))),
        ('ORIGINAL_NATIVE_MODEL','Snapshot/six-Action definition view',specs[0]['source']),
        ('CURRENT_NATIVE_MODEL','Snapshot/current six-Action definition view',specs[1]['source']),
        ('END_CONSUMER','EXPERIMENT_ACCEPTANCE_CASE input declaration',consumer()['declaration']),
        ('PROCESS_CONTRACT','Read-only qualification projection/aggregation',ref(CLOSURE/'PC01-process-contract.json')),
        ('SCOPE_CAPTURE','Authenticated bounded qualification-scope selection',consumer()['scope_capture']),
        ('COMPOSITE_GRAPH','Qualification evidence graph definition',ref(ROOT/'docs/plans/qualification/E2_P05_END_ANCESTRY_RECONCILIATION_1/qualified-evidence-graph.json')),
        ('QUALIFIED_ACCEPTANCE_MAPPING','Qualification acceptance overlay',ref(ROOT/'docs/plans/qualification/E2_P05_COMPOSITE_END_QUALIFICATION_1/qualified-composite-mapping.json')),
        ('GOVERNED_DEFINITION_HISTORY','Actual retained InstallDefinition/reference/authority records',ref(ROOT/'docs/plans/qualification/E2_P05_END_INPUT_BINDING_1/configuration-history.json')),
        ('SUPPORTED_POLICY','Exact supported selector/codec policy',ref(ROOT/'docs/experiments/E1/E1_GRAPH_RESOLUTION_SELECTION_POLICY_1.md')),
        ('INDEPENDENT_BINDING_ORACLE','Comparator only; never a Planner operand',ref(OUT/'expected-oracle.json'))]


def action_row(action,state,spec):
    definition=c._wire(action)
    return {'ACTION_ID':action.id.value,'TYPE':action.operation.value,'EFFECT':action.effect.value,
        'STATE':state.state.value,'PREREQUISITES':c._wire(action.prerequisites),'ACCEPTED_INVENTORY':c._wire(action.accepted_inventory),
        'RESULT_OUTPUT_DECLARATIONS':{'accepted_result':action.accepted_result.value,'prepared_dossier':c._wire(action.prepared_dossier),
            'accepted_inventory_is_prospective':True,'pass_model_complete':action.pass_model_complete},
        'scope':spec['context']['scope'],'lineage':spec['context']['lineage'],'generation':spec['context']['generation'],
        'provenance':c._wire(action.source),'native_definition':definition,
        'definition_comparison_identity':qid('qualification-native-action-view-v1',definition),
        'source_snapshot':spec['snapshot_id'],'no_actual_result_created_from_declaration':True}


def materialized(presentation='original'):
    specs=source_specs();models=[]
    declared=read(DOCS/(P+'E2_PC01_SOURCES.json'))['declarations']
    exact=sorted(d['id'] for d in declared)
    for spec in specs:
        raw=pointer(read(ROOT/spec['source']['path']),spec['source']['pointer'])
        state=c._unwire(raw)
        if presentation=='reversed':state=replace(state,actions=tuple(reversed(state.actions)))
        if presentation=='rotated':state=replace(state,actions=state.actions[1:]+state.actions[:1])
        equal('exact retained Snapshot identity',aid(c.snapshot_id(state)),spec['snapshot_id'])
        equal('exact native context',c._wire(state.context),spec['context'])
        equal('six exact typed source Actions',sorted(a.id.value for a in state.actions),exact)
        rows=[]
        for action in sorted(state.actions,key=lambda a:a.id.value):
            declaration=next(d for d in declared if d['id']==action.id.value)
            equal('PC01 Action operation semantics',action.operation.value,declaration['operation'])
            equal('PC01 non-effecting semantics',action.effect.value,declaration['effect'])
            status=next(s for s in state.statuses if s.id==action.id)
            rows.append(action_row(action,status,spec))
        models.append(dict(spec,actions=rows,source_identity={'file_content':'raw-file-sha256:'+spec['source']['raw_sha256'],
            'native_Snapshot':spec['snapshot_id']},accepted_inventory_not_actual_Knowledge=True))
    proc=process_definition()
    body={'schema':'PC01-END-QUALIFICATION-PROJECTION-1','kind':'QUALIFICATION_EVIDENCE_NOT_NATIVE_STATE',
        'PC01_definition':ref(DOCS/(P+'E2_PC01_SOURCES.json')),
        'PC01_qualification':ref(DOCS/(P+'E2_PC01_EXIT_RECONCILIATION_1.json')),
        'PC01_RESULT':'PASS','action_ids':exact,'models':models,'consumer':consumer(),
        'process_identity':proc['identity'],'process_definition':proc['process'],
        'scope':'E2-QUALIFICATION-ONLY','lineage_policy':'Each native context retained separately; no native lineage synthesized',
        'currentness_boundary':'Current documentary END consumption of exact qualified historical/current model roles; not Action execution permission',
        'new_native_Snapshot_Action_event_INSTALL_authority':False}
    projection={'identity':qid('qualification-PC01-END-projection-v1',body),'projection':body}
    rows=[]
    for input_id,expected_type,source in inputs():
        rows.append({'INPUT_ID':input_id,'EXPECTED_TYPE':expected_type,'SOURCE_ARTIFACT':source,
            'SOURCE_IDENTITY':'raw-file-sha256:'+source['raw_sha256'],
            'SOURCE_VALUE_SEMANTICS':expected_type,'PROJECTION_IDENTITY':projection['identity'],
            'CONSUMER':consumer(),'PROCESS':proc['identity'],'SCOPE':'E2-QUALIFICATION-ONLY',
            'LINEAGE':'Exact source native context if present; otherwise declared source/contract scope, not an invented native lineage',
            'PROVENANCE':source,'CURRENTNESS':'Exact source pin and required declared consumer-boundary role; comparator distinguished from operative input',
            'input_role':'COMPARISON_ONLY' if input_id=='INDEPENDENT_BINDING_ORACLE' else 'PINNED_QUALIFICATION_INPUT'})
    manifest_body={'schema':'PC01-END-INVOCATION-INPUT-MANIFEST-1','projection_identity':projection['identity'],
        'interface':INPUT_ID,'consumer':consumer(),'process':proc,'inputs':rows,
        'environment':{'PYTHONDONTWRITEBYTECODE':'1','PYTHONPATH':'.'},
        'invocation':proc['process']['invocations'],'permitted_parameters':{'seeds':[0,1,7,101],'reader_indices':[1,2,3],'presentations':['original','reversed','rotated']},
        'writer':'Metadata materialization only, from pinned retained native sources; no producer PC01 rerun',
        'reader_allowlist':[row['SOURCE_ARTIFACT'] for row in rows],
        'process_edges':['PC01 sources -> exact historical/current definition model projection','projection -> invocation/input manifest',
            'manifest -> E2-END#/dependencies/0 qualified consumer'],
        'P05_EXECUTED':False,'native_mutating_operations':[]}
    manifest={'identity':qid('qualification-PC01-END-manifest-v1',manifest_body),'manifest':manifest_body}
    return projection,manifest


def preflight(projection,manifest):
    expected=read(OUT/'expected-oracle.json')
    equal('preflight exact independent projection',projection['projection'],expected['expected_projection'])
    equal('qualification projection identity',projection['identity'],qid('qualification-PC01-END-projection-v1',expected['expected_projection']))
    equal('exact manifest interface',manifest['manifest']['interface'],INPUT_ID)
    equal('manifest references actual projection',manifest['manifest']['projection_identity'],projection['identity'])
    equal('manifest comparison identity',manifest['identity'],qid('qualification-PC01-END-manifest-v1',manifest['manifest']))
    equal('exact manifest input IDs',[r['INPUT_ID'] for r in manifest['manifest']['inputs']],expected['expected_input_ids'])
    equal('exact process identity',manifest['manifest']['process']['identity'],process_definition()['identity'])
    equal('exact manifest structure and input facts',manifest['manifest'],read(OUT/'expected-manifest-oracle.json')['expected_manifest'])
    check_pins(projection);check_pins(manifest)
    qualification=read(ROOT/projection['projection']['PC01_qualification']['path'])
    equal('original PC01 qualification PASS',qualification['e2_pc01_result'],'PASS')
    body=projection['projection'];native_checks=[]
    for spec in source_specs():
        state=c._unwire(pointer(read(ROOT/spec['source']['path']),spec['source']['pointer']))
        before=c.snapshot_bytes(state)
        m.validate_model(state)
        for action in state.actions:
            m.validate_types(action,m.Action)
            if spec['role']=='P04_CURRENT_DEFINITION_MODEL':equal('current Action governed definition',ai.action_current(state,action),True)
        equal('read-only native model preflight leaves bytes exact',c.snapshot_bytes(state),before)
        native_checks.append({'role':spec['role'],'snapshot':spec['snapshot_id'],'native_types':'PASS','native_model':'PASS',
            'current_governed_Action_versions':'PASS' if spec['role']=='P04_CURRENT_DEFINITION_MODEL' else 'HISTORICAL_SCOPE_ONLY'})
    equal('no native state/result/event mutations',CALLS,[])
    return {'PC01_END_INTERFACE':'PASS','terms':{key:'PASS' for key in ('SOURCE','CONSUMER','PROJECTION','PROCESS',
        'INPUT_MANIFEST','CURRENTNESS','SCOPE','LINEAGE','PROVENANCE')},'native_checks':native_checks,
        'projection_identity':projection['identity'],'manifest_identity':manifest['identity'],'native_mutating_calls':CALLS}


def negatives():
    p=read(OUT/'END-projection.json');mft=read(OUT/'invocation-input-manifest.json')
    plan=read(OUT/'negative-plan.json');answers=[]
    for item in plan['cases']:
        badp,badm=deepcopy(p),deepcopy(mft);name=item['name']
        model=badp['projection']['models'][1]
        if name=='wrong_PC01_Snapshot':model['snapshot_id']=badp['projection']['models'][0]['snapshot_id']
        elif name=='wrong_PC01_qualification':badp['projection']['PC01_qualification']=badp['projection']['PC01_definition']
        elif name=='five_Actions':model['actions'].pop()
        elif name=='seven_Actions':model['actions'].append(deepcopy(model['actions'][0]))
        elif name=='wrong_Action_identity':model['actions'][0]['ACTION_ID']='E2-FOREIGN'
        elif name=='foreign_Action':model['actions'][0]=deepcopy(badp['projection']['models'][0]['actions'][0])
        elif name=='wrong_consumer':badp['projection']['consumer']['input_id']='E2-END#/dependencies/1'
        elif name=='wrong_process':badm['manifest']['process']['identity']='qualification-other-process-v1:'+'a'*64
        elif name=='missing_manifest_input':badm['manifest']['inputs'].pop()
        elif name=='extra_manifest_input':badm['manifest']['inputs'].append(deepcopy(badm['manifest']['inputs'][0]))
        elif name=='wrong_source_identity':model['source_identity']['file_content']='raw-file-sha256:'+'a'*64
        elif name=='wrong_projection_identity':badp['identity']='planner-snapshot-v1:'+'a'*64
        elif name=='wrong_scope':model['context']['scope']='PRODUCTION'
        elif name=='wrong_lineage':model['context']['lineage']='E2-CANONICAL-BASELINE-1'
        elif name=='wrong_provenance':model['actions'][0]['provenance']['method']='UNRELATED'
        elif name=='stale_source':model['source']['raw_sha256']='0'*64
        elif name=='unordered_presentation_semantic_difference':
            unnormalized=deepcopy(badp['projection']);unnormalized['models'][0]['actions'].reverse()
            badp['identity']=qid('qualification-PC01-END-projection-v1',unnormalized)
        elif name=='report_only_source':model['source']=badp['projection']['PC01_qualification']
        else:raise AssertionError('Unsealed negative '+name)
        # Attackers may rehash mutated bytes; the independent trusted oracle is
        # still fixed. Wrong identity-only cases remain intentionally unchanged.
        if name not in ('wrong_projection_identity','unordered_presentation_semantic_difference'):
            badp['identity']=qid('qualification-PC01-END-projection-v1',badp['projection'])
        badm['identity']=qid('qualification-PC01-END-manifest-v1',badm['manifest'])
        try:preflight(badp,badm)
        except (Reject,m.PlannerError) as error:
            answers.append(dict(item,RESULT='PASS',actual=str(error),native_state_changed=False))
        else:raise Reject('negative admitted',name,'PASS')
    save('negative-results.json',{'RESULT':'PASS','cases':answers,'count':len(answers),'isolated_documentary_candidates_only':True})
    print(json.dumps({'NEGATIVES':'PASS','count':len(answers)}))


def main(args):
    if args.mode=='materialize':
        p,mft=materialized();save('END-projection.json',p);save('invocation-input-manifest.json',mft)
        save('six-Action-inventory.json',{'roles':p['projection']['models'],'action_ids':p['projection']['action_ids'],'no_native_Snapshot_created':True})
        save('process-binding.json',{'projection_identity':p['identity'],'manifest_identity':mft['identity'],'process':mft['manifest']['process'],
            'source_projection_manifest_consumer_edges':mft['manifest']['process_edges'],'binding_kind':'QUALIFICATION_EVIDENCE','no_native_state_or_permission':True})
        print(json.dumps({'MATERIALIZED':'PASS','projection':p['identity'],'manifest':mft['identity']}))
    elif args.mode=='negatives':negatives()
    else:
        p,mft=materialized(args.presentation)
        result=preflight(p,mft)
        equal('fresh source projection equal retained binding',p,read(OUT/'END-projection.json'))
        equal('fresh source manifest equal retained binding',mft,read(OUT/'invocation-input-manifest.json'))
        if args.mode=='preflight':save('preflight.json',result)
        else:
            save('readers/seed-%s-reader-%s-%s.json'%(os.environ['PYTHONHASHSEED'],args.index,args.presentation),
                dict(result,pid=os.getpid(),seed=os.environ['PYTHONHASHSEED'],reader_index=args.index,presentation=args.presentation,writer_memory_available=False))
        print(json.dumps({'PC01_END_INTERFACE':'PASS','mode':args.mode,'projection':p['identity'],'manifest':mft['identity'],'native_calls':CALLS}))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('mode',choices=['materialize','preflight','negatives','reader'])
    parser.add_argument('--seed',type=int);parser.add_argument('--index',type=int,default=0)
    parser.add_argument('--presentation',choices=['original','reversed','rotated'],default='original');args=parser.parse_args()
    try:main(args)
    except Exception as error:
        save('STOP-'+args.mode+'.json',{'FIRST_COUNTEREXAMPLE':error.record if isinstance(error,Reject) else str(error),
            'native_mutating_calls':CALLS,'P05_EXECUTED':False})
        raise
