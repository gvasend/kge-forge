"""Independent static qualification, no native SOURCE_BYTES invocation."""
import ast,copy,importlib.util,json,hashlib,os,subprocess,sys
from pathlib import Path
R=Path('/home/gvasend/app/kge-forge');E=Path(__file__).resolve().parent;Q=R/'docs/plans/qualification';B=Q/'E2_P05_D01_FIXTURE_ORACLE_CLOSURE_2';P=Q/'E2_P05_D01_SOURCE_BYTES_PIN_RECONCILIATION_32'
sys.path.insert(0,str(R));sys.path.insert(0,str(E));import source_dispatch_v3 as v
from adapter.planner import codec

def load(p):return json.loads(Path(p).read_bytes())
def sha(x):return hashlib.sha256(x).hexdigest()
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def emit(n,x):(E/n).write_text(json.dumps(x,sort_keys=True,indent=2)+'\n')
def reconstruct():
 domain=load(P/'source-collection.json');expected=[]
 for m in domain['MEMBERS']:
  instance={'obligation_id':'D01-OBL:SOURCE_BYTES','case_id':'E2-D01','dispatch_id':'D01-DISPATCH:SOURCE_BYTES','operation_id':'LOAD_PIN','native_entrypoint':'adapter.planner.codec.load_pinned','source_id':m['SOURCE_ID'],'source_pin':m['PIN'],'source_role':m['SEMANTIC_ROLE'],'provenance_role':m['PROVENANCE_ROLE'],'capsule_id':'D01-FIXTURE:SOURCE_BYTES:REQUIRED_ROLE','state_variant_id':'D01-VARIANT:SOURCE_BYTES:REQUIRED_ROLE','capsule_source':domain['OWNING_CAPSULE'],'scope':m['SCOPE'],'lineage':m['LINEAGE'],'generation':m['GENERATION'],'first_available_event_prefix':m['FIRST_AVAILABLE_EVENT_PREFIX'],'operands':{'source_root':str(R),'pin':m['PIN']},'mutation_descriptor':None,'comparison_reference':'FUTURE_INDEPENDENT_ORACLE_KEYED_BY_THIS_INSTANCE; no expected values constructed'}
  instance['instance_identity']='qualification-D01-source-instance-v1:'+sha(canon(instance));expected.append(instance)
 expected.sort(key=lambda x:x['instance_identity']);assert expected==load(E/'source-instances.json')
 agg={'obligation_id':'D01-OBL:SOURCE_BYTES','case_id':'E2-D01','acceptance':'ALL','required_instance_identities':sorted(x['instance_identity'] for x in expected),'source_count':51,'source_collection_semantics':'UNORDERED; prefix chronology retained','frozen_obligations':128};agg['aggregate_identity']='qualification-D01-source-aggregate-v1:'+sha(canon(agg));assert agg==load(E/'aggregate-contract.json')
 return expected,agg
instances,aggregate=reconstruct()
if '--identity' in sys.argv:print(sha(canon({'instances':instances,'aggregate':aggregate})));raise SystemExit
old=load(B/'dispatch-table-v2.json');new=load(E/'dispatch-table-v3.json');assert len(old)==len(new)==128
changes=[k for k in old if old[k]!=new[k]];assert changes==['D01-DISPATCH:SOURCE_BYTES'];path=new[changes[0]];without=dict(path);without.pop('per_source_expansion');assert without==old[changes[0]]
trees=[ast.parse(p.read_text()) for p in [B/'runner_v2.py',E/'runner_v3.py']];functions=[{x.name:x for x in t.body if isinstance(x,ast.FunctionDef)} for t in trees];assert set(functions[0])==set(functions[1])
function_changes=[]
for name,fn in functions[0].items():
 newfn=functions[1][name]
 if ast.dump(fn)!=ast.dump(newfn):function_changes.append(name)
 if name=='execute_job':assert [ast.dump(x) for x in fn.body]==[ast.dump(x) for x in newfn.body[1:]]
 elif name=='static_preflight':assert [ast.dump(x) for x in fn.body[1:]]==[ast.dump(x) for x in newfn.body[1:]]
 else:assert ast.dump(fn)==ast.dump(newfn)
assert set(function_changes)=={'execute_job','static_preflight'}
spec=importlib.util.spec_from_file_location('runner_v3',E/'runner_v3.py');runner=importlib.util.module_from_spec(spec);spec.loader.exec_module(runner)
runner.native_function=lambda *args:(_ for _ in ()).throw(AssertionError('NATIVE_CASE_OPERATION_FORBIDDEN_DURING_STATIC_QUALIFICATION'))
packet=load(R/path['per_source_expansion']['original_fixture']['path']);row={'OBLIGATION_ID':'D01-OBL:SOURCE_BYTES','RUNNER_DISPATCH_ID':'D01-DISPATCH:SOURCE_BYTES'};context={'source_root':R,'store_root':R/'unused'}
jobs=v.expand_instances(row,path,packet,context);assert len(jobs)==51
for instance,projected,single in jobs:
 args=[runner.resolve(binding,projected['canonical_content'],context) for binding in single['steps'][0]['args']];codec.validate_pin(args[1]);assert codec._wire(args[1])==instance['source_pin'] and args[0]==R
 a=copy.deepcopy(projected);a['canonical_content']['arguments'].pop('pin');assert a==packet
 assert single==old['D01-DISPATCH:SOURCE_BYTES']
 native=ast.parse((R/'adapter/planner/codec.py').read_text());assert any(isinstance(x,ast.FunctionDef) and x.name=='load_pinned' for x in native.body)
preflight=runner.static_preflight();assert preflight['qualification_case_calls']==0
# Presentation permutations exercise projection only, never execute/capture native jobs.
semantic=lambda jobs:sorted((x['instance_identity'] for x,_,_ in jobs))
for sources in [packet['canonical_content']['arguments']['bundle']['sources'][::-1]]+[packet['canonical_content']['arguments']['bundle']['sources'][i:]+packet['canonical_content']['arguments']['bundle']['sources'][:i] for i in range(51)]:
 perm=copy.deepcopy(packet);perm['canonical_content']['arguments']['bundle']['sources']=sources
 assert semantic(v.expand_instances(row,path,perm,context))==semantic(jobs)
negative=[]
def reject(name,fn):
 try:fn()
 except ValueError as ex:negative.append({'NAME':name,'RESULT':'PASS','REJECTION':str(ex)});return
 raise AssertionError('FAIL_OPEN '+name)
for name,selection in [('single-source selection',[packet['canonical_content']['arguments']['bundle']['sources'][0]]),('first-source selection',packet['canonical_content']['arguments']['bundle']['sources'][:1]),('last-source selection',packet['canonical_content']['arguments']['bundle']['sources'][-1:]),('missing one of 51',packet['canonical_content']['arguments']['bundle']['sources'][:-1]),('duplicate one of 51',packet['canonical_content']['arguments']['bundle']['sources']+[packet['canonical_content']['arguments']['bundle']['sources'][0]])]:
 p=copy.deepcopy(packet);p['canonical_content']['arguments']['bundle']['sources']=selection;reject(name,lambda p=p:v.expand_instances(row,path,p,context))
for name in ['52nd foreign source','source pin from another instance','source/provenance mismatch']:
 p=copy.deepcopy(packet)
 if name=='52nd foreign source':p['canonical_content']['arguments']['bundle']['sources'].append({'foreign':'source'})
 elif name=='source pin from another instance':p['canonical_content']['arguments']['bundle']['sources'][0]=copy.deepcopy(p['canonical_content']['arguments']['bundle']['sources'][1])
 else:p['canonical_content']['lineage']='wrong'
 reject(name,lambda p=p:v.expand_instances(row,path,p,context))
statuses=[{'instance_identity':x['instance_identity'],'status':'PASS'} for x in instances];assert v.acceptance(aggregate,statuses)
for strategy in ['ANY','FIRST_PASS','MAJORITY','ORDER_DEPENDENT_PASS']:
 a=dict(aggregate,acceptance=strategy);reject('aggregate '+strategy,lambda a=a:v.acceptance(a,statuses))
for name,values in [('one failed',statuses[:-1]+[dict(statuses[-1],status='FAIL')]),('one missing',statuses[:-1]),('one twice',statuses[:-1]+[statuses[0]]),('two collapsed',statuses[:-2]+[statuses[0]])]:reject(name,lambda values=values:v.acceptance(aggregate,values))
for name in ['reversal changes aggregate identity','rotation changes aggregate identity','hash seed changes aggregate identity']:
 a=copy.deepcopy(aggregate);a['aggregate_identity']='order-dependent-altered-identity';reject(name,lambda a=a:v.acceptance(a,statuses))
badpath=copy.deepcopy(path);badpath['per_source_expansion']['runtime_source_selection']=True;reject('presentation-order selection',lambda:v.expand_instances(row,badpath,packet,context))
reject('native Planner behavior modified',lambda:v.check_pin({'path':'adapter/planner/codec.py','raw_sha256':'0'*64}))
seeds=[]
for seed in [0,1,7,101]:
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED=str(seed));proc=subprocess.run([sys.executable,str(Path(__file__).resolve()),'--identity'],cwd=str(R),env=env,capture_output=True,text=True,check=True);seeds.append({'seed':seed,'semantic_hash':proc.stdout.strip(),'coverage':'51/51'})
 orderproc=subprocess.run([sys.executable,'-c','import json;print(json.dumps(list(set('+repr([canon(x).decode() for x in packet['canonical_content']['arguments']['bundle']['sources']])+'))))'],env=env,capture_output=True,text=True,check=True);permuted=copy.deepcopy(packet);permuted['canonical_content']['arguments']['bundle']['sources']=[json.loads(s) for s in json.loads(orderproc.stdout)];assert semantic(v.expand_instances(row,path,permuted,context))==semantic(jobs)
assert len({x['semantic_hash'] for x in seeds})==1
emit('qualification.json',{'RESULT':'PASS','SOURCE_DOMAIN_COUNT':51,'COVERAGE':'51/51','STATIC_PREFLIGHT':'PASS','NATIVE_ENTRYPOINT_EXISTS':True,'ALL_51_COMPLETE_OPERANDS_TYPED':True,'NON_SOURCE_DISPATCHES_UNCHANGED':127,'FUNCTION_CHANGES':function_changes,'DISPATCH_FIELDS_ADDED':['per_source_expansion'],'NATIVE_PLANNER_CHANGE':False,'NEGATIVES':{'PASS':len(negative),'TOTAL':len(negative),'CASES':negative},'DETERMINISM':seeds,'AGGREGATE_IDENTITY':aggregate['aggregate_identity'],'PERMUTATIONS':'reverse + all 51 rotations + seed presentations PASS','QUALIFICATION_CASES_EXECUTED':0,'STATIC_BASE_PREFLIGHT':preflight})
print('V3 STATIC QUALIFICATION PASS; 51 instances; 127 unchanged dispatches;',len(negative),'negatives; four seeds PASS')
