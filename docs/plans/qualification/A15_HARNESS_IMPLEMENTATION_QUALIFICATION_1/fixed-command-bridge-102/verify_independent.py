"""Metadata-only102 verifier;no bridge imports,claims,probes or services."""
import ast,copy,hashlib,json,os,pathlib
R=pathlib.Path(__file__).resolve().parents[5];B=R/'docs/plans/qualification/A15_HARNESS_IMPLEMENTATION_QUALIFICATION_1';O=pathlib.Path(__file__).parent

def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def enc(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def require(x,m):
 if not x:raise ValueError(m)
def acyclic(es):
 d={}
 for e in es:d.setdefault(e['from'],[]).append(e['to'])
 done=set();active=set()
 def v(n):
  if n in active:return False
  if n in done:return True
  active.add(n)
  for w in d.get(n,[]):
   if not v(w):return False
  active.remove(n);done.add(n);return True
 return all(v(n) for n in d)
a=read(O/'entry-authentication.json')
for folder in a['PRIOR_INDICES_VERIFIED']:
 for n,h in read(B/folder/'evidence-index.json').get('FILES',{}).items():
  if isinstance(h,str):require(sha(R/n if (R/n).is_file() else B/folder/n)==h,'prior index')
for p,h in a['SOURCE_IDENTITIES'].items():require(sha(R/p)==h,'source unchanged')
for r in a['GRANT_REFERENCES']:
 require(sha(R/r['path'])==r['raw_sha256'],'effective reference');ref=read(R/r['path']);p=ref['GRANT_RECORD_PIN'];require(sha(R/p['path'])==p['raw_sha256'],'grant raw');g=read(R/p['path']);body=g.get('CONTENT',g.get('RECORD'));require(hashlib.sha256(enc(body)).hexdigest()==r['identity']['sha256'],'grant content')
 for p in ref['VERIFICATION_PINS']:require(sha(R/p['path'])==p['raw_sha256'],'grant evidence')
fixed=read(O/'fixed-command-trust-contract.json');spec=read(B/'system-process-enforcement-86/transient-service-specification.json');require(fixed['ARGUMENT_VECTOR']==spec['EXACT_COMMAND_ARGV'],'byte-equivalent argv')
require(hashlib.sha256(enc(fixed['ARGUMENT_VECTOR'])).hexdigest()==fixed['COMMAND_CONTENT_IDENTITY']['sha256']=='e628c8664ea72357963dc58dddee934c28cad3ab5c84450656a6595e6910fb50','command id')
require(hashlib.sha256(fixed['ARGUMENT_VECTOR'][-1].encode()).hexdigest()==spec['SOURCE_PROGRAM_SHA256'],'payload raw pin');p=fixed['COMMAND_RAW_IDENTITIES']['retained_contract'];require(sha(R/p['path'])==p['raw_sha256'],'raw container')
ast.parse(fixed['ARGUMENT_VECTOR'][-1]);require(fixed['EXECUTABLE_PATHS_AND_HASHES']==spec['EXECUTABLE_PINS'],'binary pins')
proto=read(O/'durable-one-attempt-protocol.json');require(len(proto['ORDERED_STEPS'])==12 and [x['NUMBER'] for x in proto['ORDERED_STEPS']]==list(range(1,13)),'ordered protocol');require(not proto['EXISTING_IDENTICAL_IS_FRESH'] and not proto['UNKNOWN_REOPENS'] and proto['CLAIM_IRREVERSIBLE'],'irreversible')
source=read(O/'source-authority-boundary.json');paths=[p['PATH'] for p in source['PROPOSED_SOURCE_FILES']];require(len(paths)==2 and not any((R/p).exists() for p in paths),'no unauthorized source creation')
fixtures=read(O/'logical-synthetic-identity-manifest.json');require(hashlib.sha256(enc(fixtures['CONTENT'])).hexdigest()==fixtures['IDENTITY']['sha256'],'manifest id');require(fixtures['CONTENT']['COUNT']==len(fixtures['CONTENT']['FIXTURES'])==12,'logical fixtures')
for f in fixtures['CONTENT']['FIXTURES']:
 c=f['CONTENT'];require(hashlib.sha256(enc(c)).hexdigest()==f['IDENTITY']['sha256'],'fixture');g=c['SYNTHETIC_GRANT'];require(hashlib.sha256(enc(g['CONTENT'])).hexdigest()==g['IDENTITY']['sha256'],'synthetic grant');require(g['CONTENT']['issuer']=='SYNTHETIC_NOT_PROJECT_AUTHORITY' and g['CONTENT']['mode']=='INERT_ONLY','not real grant')
 require(hashlib.sha256(enc(c['KEY_BODY'])).hexdigest()==c['CONSUMPTION_KEY']['sha256'],'key reconstruction');require(hashlib.sha256(enc(g['IDENTITY'])).hexdigest()==c['GRANT_ANCHOR']['sha256'],'grant anchor')
 require(c['KEY_BODY']['attempt_number']==1 and c['KEY_BODY']['issued_probe_grant_identity']==g['IDENTITY'],'single synthetic attempt')
require(read(O/'stable-consumption-identity.json')['ACTUAL_REAL_KEY'] is None,'no future key invented')
reg=read(R/'docs/plans/PLANNER_REASONING_LESSONS_REGISTER_1.json');prev='0'*64
for e in reg['EVENTS']:
 require(e['PREVIOUS_EVENT_HASH']==prev,'lesson previous');require(hashlib.sha256(json.dumps({k:v for k,v in e.items() if k!='EVENT_HASH'},sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()).hexdigest()==e['EVENT_HASH'],'lesson hash');prev=e['EVENT_HASH']
require(prev==a['LL11_HEAD'],'LL11 head');require(sha(B/'campaign-budget.jsonl')==a['STOPPED_JOURNAL_SHA256'],'stopped journal')
graph=read(O/'qualification-dependency-graph.json');require(acyclic(graph['EDGES']),'graph')
s={'command':fixed['COMMAND_CONTENT_IDENTITY']['sha256'],'unissued_effective':False,'duplicate_consumption':False,'existing_fresh':False,'crash_reopens':False,'reusable_capability':False,'arbitrary_systemd':False,'independent_observer_required':True,'unknown_exit_success':False,'limits':spec['LIMITS'],'construction_as_probe':False,'graph':graph['EDGES'],'source_created':False,'systemd_executed':False,'H77A15':False}
def valid(x):
 require(x['command']==s['command'],'wrong command');require(not x['unissued_effective'],'unissued grant');require(not x['duplicate_consumption'],'duplicate consumption');require(not x['existing_fresh'],'identical fresh');require(not x['crash_reopens'],'crash reopen');require(not x['reusable_capability'],'reusable capability');require(not x['arbitrary_systemd'],'arbitrary systemd');require(x['independent_observer_required'],'observer missing');require(not x['unknown_exit_success'],'unknown success');require(x['limits']==spec['LIMITS'],'resource increased');require(not x['construction_as_probe'],'construction as probe');require(acyclic(x['graph']),'cycle');require(not x['source_created'],'source created');require(not x['systemd_executed'],'premature systemd');require(not x['H77A15'],'real H77 A15')
valid(s)
lim=copy.deepcopy(spec['LIMITS']);lim['MAX_SERVICE_WALL_TIME_SECONDS']=21
mut=[('wrong command','command','0'*64),('unissued effective','unissued_effective',True),('duplicate accepted','duplicate_consumption',True),('identical record fresh','existing_fresh',True),('crash reopen','crash_reopens',True),('reusable launch','reusable_capability',True),('arbitrary systemd','arbitrary_systemd',True),('observer missing','independent_observer_required',False),('unknown exit success','unknown_exit_success',True),('limit increase','limits',lim),('construction used for probe','construction_as_probe',True),('qualification cycle','graph',graph['EDGES']+[{'from':'INDEPENDENT_STABLE_STORE_AND_RESOURCE_OBSERVER_TRUST','to':'QUALIFIED_FIXED_BRIDGE'}]),('source creation','source_created',True),('systemd execution','systemd_executed',True),('H77 A15 included','H77A15',True)]
neg=[]
for name,k,v in mut:
 x=copy.deepcopy(s);x[k]=v
 try:valid(x)
 except ValueError as e:neg.append({'CONTROL':name,'RESULT':'REJECTED','CAUSE':str(e)})
 else:raise ValueError('accepted:'+name)
r={'COMMAND_IDENTITY':fixed['COMMAND_CONTENT_IDENTITY'],'RETAINED_RAW_SHA256':fixed['COMMAND_RAW_IDENTITIES'],'SERVICE_LIMITS':spec['LIMITS'],'SOURCE_BOUNDARY':paths,'LOGICAL_SYNTHETIC_FIXTURE_IDENTITY':fixtures['IDENTITY'],'INERT_PROPERTIES':12,'REAL_KEY':None,'CLAIM_PROTOCOL_ORDER_COMPLETE':True,'CLAIM_TO_MANAGER_EXCLUSIVITY_QUALIFIED':False,'STORE_RESOURCE_OBSERVER_COMPLETE':False,'DECISION_READY':False,'GRAPH_ACYCLIC':True,'LL11_HEAD':prev,'NEGATIVES':neg,'CONTRACT_PINS':{p.name:sha(p) for p in O.glob('*.json') if p.name not in ['preservation-before.json','independent-static-verification.json','four-seed-reconstruction.json','negative-control-results.json','governance-authentication.json','preservation-audit.json','report.json','evidence-index.json']},'ASSURANCE':'metadata/AST/identity reconstruction and static reporting negatives;not active claim,crash,filesystem or manager qualification'}
print(json.dumps({'HASH_SEED':os.environ.get('PYTHONHASHSEED'),'RECONSTRUCTION':r,'SEMANTIC_SHA256':hashlib.sha256(enc(r)).hexdigest()},sort_keys=True))
