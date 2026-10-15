"""Static101 reconstruction;no service,probe,target import or source modification."""
import ast,copy,hashlib,json,os,pathlib
R=pathlib.Path(__file__).resolve().parents[5];B=R/'docs/plans/qualification/A15_HARNESS_IMPLEMENTATION_QUALIFICATION_1';O=pathlib.Path(__file__).parent

def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def enc(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def require(x,m):
 if not x:raise ValueError(m)
def acyclic(es):
 adj={}
 for e in es:adj.setdefault(e['from'],[]).append(e['to'])
 done=set();active=set()
 def v(n):
  if n in active:return False
  if n in done:return True
  active.add(n)
  for m in adj.get(n,[]):
   if not v(m):return False
  active.remove(n);done.add(n);return True
 return all(v(n) for n in adj)
a=read(O/'entry-authentication.json')
for p,h in a['SOURCE_IDENTITIES'].items():require(sha(R/p)==h,'source preservation')
for folder in a['PACKAGE_INDICES_AUTHENTICATED']:
 x=read(B/folder/'evidence-index.json');files=x.get('FILES',x.get('files'))
 if isinstance(files,dict):
  for n,h in files.items():require(sha(R/n if (R/n).is_file() else B/folder/n)==h,'evidence index pin')
for p in a['P78_P88_ADDITIONAL_INDEX_PINS']:
 require(sha(R/p['path'])==p['raw_sha256'],'78/88 index')
 for n,h in read(R/p['path']).get('FILES',{}).items():
  if isinstance(h,str):require(sha(R/n if (R/n).is_file() else (R/p['path']).parent/n)==h,'78/88 evidence')
for r in a['GRANT_REFERENCES']:
 require(sha(R/r['path'])==r['raw_sha256'],'effective grant reference');ref=read(R/r['path']);p=ref['GRANT_RECORD_PIN'];require(sha(R/p['path'])==p['raw_sha256'],'grant raw');g=read(R/p['path']);body=g.get('CONTENT',g.get('RECORD'));require(hashlib.sha256(enc(body)).hexdigest()==r['identity']['sha256'],'issued identity')
 for p in ref['VERIFICATION_PINS']:require(sha(R/p['path'])==p['raw_sha256'],'issuance pin')
contract=read(O/'exact-package86-probe-contract.json');spec=read(B/'system-process-enforcement-86/transient-service-specification.json');auth87=read(B/'system-probe-authority-87/package86-command-authentication.json')
require(contract['ARGUMENT_VECTOR']==spec['EXACT_COMMAND_ARGV']==auth87['COMMAND_ARGUMENT_VECTOR'],'exact command')
require(hashlib.sha256(enc(contract['ARGUMENT_VECTOR'])).hexdigest()==contract['COMMAND_IDENTITY']['sha256']=='e628c8664ea72357963dc58dddee934c28cad3ab5c84450656a6595e6910fb50','argv identity')
require(hashlib.sha256(contract['ARGUMENT_VECTOR'][-1].encode()).hexdigest()==contract['PAYLOAD_SHA256'],'source program pin')
for f in ['system-process-enforcement-86/proposed-authorization-subject.json','system-probe-authority-87/proposed-system-level-probe-subject.json']:
 s=read(B/f);body=dict(s);id=body.pop('PROPOSED_CONTENT_IDENTITY');require(hashlib.sha256(enc(body)).hexdigest()==id['sha256'],'prospective retained identity')
payload=ast.parse(contract['ARGUMENT_VECTOR'][-1]);emit=next(n for n in payload.body if isinstance(n,ast.FunctionDef) and n.name=='emit');require(any(isinstance(n,ast.Constant) and n.value=='\n' for n in ast.walk(emit)),'LFframing');require(not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr in ['Popen','fork','posix_spawn','system'] for n in ast.walk(payload)),'fixed source no explicit shell/spawn')
require('--uid=1000' in contract['ARGUMENT_VECTOR'] and '--property=RuntimeMaxSec=20s' in contract['ARGUMENT_VECTOR'] and '--property=TasksMax=8' in contract['ARGUMENT_VECTOR'],'sealed profile')
require(contract['RESOURCE_LIMITS']['OBSERVER_TOTAL_WALL_SECONDS']==25 and contract['MAX_OBSERVER_PUBLISHED_BYTES']==65536,'probe observer bounds')
one=read(O/'one-attempt-mechanism-assessment.json');require(not one['ONE_ATTEMPT_MECHANISM_COMPLETE'] and one['EXACT_KEY'] is None,'no fabricated qualified mechanism or grantkey')
p78=read(B/'probe-grant-issuance-78/issuance-gap-dossier.json');require(p78['ISSUED_GRANT_IDENTITY'] is None and not p78['EFFECTIVENESS_REFERENCE_PUBLISHED'],'78 remains unissued')
reg=read(R/'docs/plans/PLANNER_REASONING_LESSONS_REGISTER_1.json');prev='0'*64
for e in reg['EVENTS']:
 require(e['PREVIOUS_EVENT_HASH']==prev,'lesson predecessor');require(hashlib.sha256(json.dumps({k:v for k,v in e.items() if k!='EVENT_HASH'},sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()).hexdigest()==e['EVENT_HASH'],'lesson hash');prev=e['EVENT_HASH']
require(prev==a['LL11_HEAD'],'LL11 head');require(sha(B/'campaign-budget.jsonl')==a['STOPPED_JOURNAL_SHA256'],'stopped journal')
graph=read(O/'qualification-dependency-graph.json');require(acyclic(graph['EDGES']),'graph')
s={'binding_present':True,'host_root_qualified':False,'unit_is_consumption':False,'duplicate_launch':False,'unknown_reopens':False,'output_before_authority':False,'full90stillbinding':True,'construction_allows_service':False,'command_sha':contract['COMMAND_IDENTITY']['sha256'],'service_wall':20,'independent_exit_required':True,'graph':graph['EDGES'],'amendment_applied':False,'H77A15':False,'activated':False}
def valid(x):
 require(x['binding_present'],'binding omitted');require(not x['host_root_qualified'],'unqualified root');require(not x['unit_is_consumption'],'unit as consumption');require(not x['duplicate_launch'],'duplicate launch');require(not x['unknown_reopens'],'unknown reopened');require(not x['output_before_authority'],'probe output prerequisite');require(x['full90stillbinding'],'90case acceptance waived');require(not x['construction_allows_service'],'construction service inference');require(x['command_sha']==s['command_sha'],'wrong command');require(x['service_wall']==20,'unbounded lifetime');require(x['independent_exit_required'],'missing exit');require(acyclic(x['graph']),'cycle');require(not x['amendment_applied'],'amendment applied');require(not x['H77A15'],'H77 A15 included');require(not x['activated'],'premature activation')
valid(s)
changes=[('binding omitted','binding_present',False),('unqualified root accepted','host_root_qualified',True),('unit name as consumption','unit_is_consumption',True),('duplicate launch','duplicate_launch',True),('unknown outcome reopens','unknown_reopens',True),('probe output before authorization','output_before_authority',True),('full campaign requirement waived','full90stillbinding',False),('service from construction grant','construction_allows_service',True),('wrong command','command_sha','0'*64),('unbounded lifetime','service_wall',None),('missing independent exit','independent_exit_required',False),('circular authority','graph',graph['EDGES']+[{'from':'EFFECTIVE_EXACT_PROBE_GRANT','to':'PIDS_METADATA_RESULT'}]),('unauthorized amendment','amendment_applied',True),('H77 A15 included','H77A15',True),('premature activation','activated',True)]
neg=[]
for name,k,v in changes:
 x=copy.deepcopy(s);x[k]=v
 try:valid(x)
 except ValueError as e:neg.append({'CONTROL':name,'RESULT':'REJECTED','CAUSE':str(e)})
 else:raise ValueError('accepted negative:'+name)
r={'COMMAND_IDENTITY':contract['COMMAND_IDENTITY'],'SUBJECT_IDENTITY':contract['SUBJECT_IDENTITY'],'LIMITS':contract['RESOURCE_LIMITS'],'MAX_OBSERVER_PUBLICATION':65536,'EXACT_ARGV_UNCHANGED':True,'FRAMING':'LF0a','SPECIFIC_PIDS_VALUE_REQUIRED_BEFORE_LAUNCH':False,'QUALIFIED_ONE_ATTEMPT_MECHANISM':False,'FULL90REQUIREMENTS_UNCHANGED':True,'PREFERRED_PATH':'B_PROSPECTIVE_SCOPE_ONLY','DECISION_READY':False,'GRAPH_ACYCLIC':True,'LL11_HEAD':prev,'NEGATIVES':neg,'CONTRACT_PINS':{p.name:sha(p) for p in O.glob('*.json') if p.name not in ['preservation-before.json','independent-static-verification.json','four-seed-reconstruction.json','negative-control-results.json','governance-authentication.json','preservation-audit.json','report.json','evidence-index.json']},'ASSURANCE':'retained bytes/content identities,payloadAST,scope/reporting checks;not actual OS/claim/launch qualification'}
print(json.dumps({'HASH_SEED':os.environ.get('PYTHONHASHSEED'),'RECONSTRUCTION':r,'SEMANTIC_SHA256':hashlib.sha256(enc(r)).hexdigest()},sort_keys=True))
