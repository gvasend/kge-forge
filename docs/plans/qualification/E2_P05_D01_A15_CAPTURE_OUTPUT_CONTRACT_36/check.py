"""Contract-only controls and fresh-process reconstruction; no native effects."""
import copy,json,os,subprocess,sys
from pathlib import Path
E=Path(__file__).resolve().parent;sys.path.insert(0,str(E));from recover import R,Q,load,emit,canon,sha
r=load(E/'recovered-contract.json');graph=r['GRAPH'];target=r['TARGET_CONTRACT'];sources={canon(n['NATIVE_IDENTITY']) for n in graph['NODES'] if n['TYPE']=='SOURCE_CONTENT'}
assert len(sources)==54 and len(graph['NODES'])==131 and len(graph['EDGES'])==474
assert len({canon(x['CONTENT_IDENTITIES']) for x in target['CANDIDATE_PROJECTIONS']})>1 and not target['TARGETS_UNIQUE']
value=dict(graph);gid=value.pop('GRAPH_IDENTITY');assert gid=='qualification-A15-support-graph-v1:'+sha(canon(value))
spec={'expected_snapshot':r['PRESTATE'],'exact_targets':None,'source_identity_kind':'CONTENT_IDENTITY','target_rule':'UNSEALED_REQUIRED_SUPPORT_ROOT_ROLE_PARTITION','target_selection_by_order':False,'native_extra_fields':{'route':None,'receipt':None,'reason':None},'scope':r['CONTEXT']['scope'],'lineage':r['CONTEXT']['lineage'],'provenance':'exact sealed graph/state/source-role pins','apply_event_is_persisted':False,'occurrence_type':'ExecutionEvent','full_oracle_fields':['state','proof','control','resume','ordered_trace','full_frozen_capture_fields'],'trace_order':'EXACT','oracle_source':'INDEPENDENT_CONTRACT_OR_MODEL; never future output','full_oracle_complete':False}
def schema(x):
 if x!=spec:raise ValueError('STATIC_A15_CONTRACT_OR_DOMAIN_VIOLATION')
 return True
assert schema(spec);neg=[]
def rejected(name,fn):
 try:fn()
 except ValueError as ex:neg.append({'NAME':name,'RESULT':'PASS','REJECTION':str(ex),'NATIVE_CASE_OPERATION_EXECUTED':False});return
 raise AssertionError('FAIL_OPEN '+name)
def partition_check(proposed,required):
 keys=[canon(x) for x in proposed]
 if any(k not in sources for k in keys):raise ValueError('TARGET_OUTSIDE_SUPPORT_SOURCE_GRAPH_OR_WRONG_CONTENT_IDENTITY')
 if len(keys)!=len(set(keys)):raise ValueError('OVERLAPPING_SOURCE_TARGET')
 if set(keys)!=set(canon(x) for x in required):raise ValueError('MISSING_OR_EXTRA_DECLARED_PARTITION_MEMBER')
 return True
# Diagnostic membership validator: this is not selection of the actual A15 targets.
diagnostic=target['CANDIDATE_PROJECTIONS'][0]['CONTENT_IDENTITIES'];assert partition_check(diagnostic,diagnostic)
rejected('target outside accepted-support graph',lambda:partition_check([{'foreign':'source'}],diagnostic))
bad=copy.deepcopy(diagnostic);bad[0]['sha256']='0'*64;rejected('wrong content identity',lambda:partition_check(bad,diagnostic))
rejected('missing target',lambda:partition_check(diagnostic[:-1],diagnostic))
extra=next(json.loads(k) for k in sources if k not in {canon(x) for x in diagnostic});rejected('extra target',lambda:partition_check(diagnostic+[extra],diagnostic))
rejected('overlapping source targets',lambda:partition_check(diagnostic+[diagnostic[0]],diagnostic))
for name,field,value in [('source chosen by order','target_selection_by_order',True),('wrong expected_snapshot','expected_snapshot','other'),('wrong scope','scope','other'),('wrong lineage','lineage','other'),('wrong provenance','provenance','report'),('apply_event treated as persisted occurrence','apply_event_is_persisted',True),('report treated as native occurrence','occurrence_type','QualificationReport'),('partial P03 oracle treated as complete','full_oracle_complete',True),('unordered trace accepted','trace_order','UNORDERED'),('future output used as oracle','oracle_source','FUTURE_OUTPUT')]:
 bad=copy.deepcopy(spec);bad[field]=value;rejected(name,lambda bad=bad:schema(bad))
for field in ['route','receipt','reason']:
 bad=copy.deepcopy(spec);bad['native_extra_fields'][field]='invented';rejected('wrong '+field,lambda bad=bad:schema(bad))
for field in ['proof','control','resume']:
 bad=copy.deepcopy(spec);bad['full_oracle_fields'].remove(field);rejected('missing '+field+' expectation',lambda bad=bad:schema(bad))
for variant in [list(reversed(diagnostic)),diagnostic[1:]+diagnostic[:1]]:assert partition_check(variant,diagnostic)
static_files=['descriptor-schema.json','apply-event-contract.json','capture-contract.json','ordered-trace-contract.json','expected-output-frontier.json','acceptance-contract.json','a16-handoff-contract.json','execution-frontier.json']
contracts_hash=sha(canon({n:load(E/n) for n in static_files}));seeds=[]
for seed in [0,1,7,101]:
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED=str(seed));process=subprocess.run([sys.executable,str(E/'recover.py'),'--identity'],cwd=str(R),env=env,capture_output=True,text=True,check=True)
 proc2=subprocess.run([sys.executable,'-c','import json,hashlib,pathlib; p=pathlib.Path('+repr(str(E))+'); names='+repr(static_files)+'; v={n:json.loads((p/n).read_text()) for n in names}; print(hashlib.sha256(json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode()).hexdigest())'],env=env,capture_output=True,text=True,check=True)
 assert proc2.stdout.strip()==contracts_hash;seeds.append({'seed':seed,'graph_and_target_inventory_hash':process.stdout.strip(),'static_contracts_hash':contracts_hash,'selected_target_set':None,'descriptor_identity':None,'post_state_oracle':None,'proof_control_resume_values':None,'ordered_trace_complete':False})
assert len({x['graph_and_target_inventory_hash'] for x in seeds})==1
emit('negative-suite.json',{'RESULT':'PASS','PASS':len(neg),'TOTAL':len(neg),'CASES':neg,'DIAGNOSTIC_PARTITION_TEST_NOT_ACTUAL_TARGET_SELECTION':True,'NATIVE_OPERATIONS_INVOKED':0})
emit('determinism.json',{'RESULT':'PASS','SEEDS':seeds,'QUALIFIED_TARGETS_UNIQUE':False,'GRAPH_IDENTITY':graph['GRAPH_IDENTITY'],'NO_CONCRETE_EXPECTED_ORACLE_OR_DESCRIPTOR_CREATED':True})
print('36 STATIC CHECKS PASS;',len(neg),'negatives; graph/contracts stable across four seeds')
