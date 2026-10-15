"""105independent documentary reconstruction;not execution of proposed topology."""
import copy,hashlib,json,os,pathlib
R=pathlib.Path(__file__).resolve().parents[5];B=R/'docs/plans/qualification/A15_HARNESS_IMPLEMENTATION_QUALIFICATION_1';O=pathlib.Path(__file__).parent

def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def enc(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def must(x,m):
 if not x:raise ValueError(m)
def acyclic(es):
 d={}
 for e in es:d.setdefault(e['from'],[]).append(e['to'])
 active=set();done=set()
 def v(n):
  if n in active:return False
  if n in done:return True
  active.add(n)
  for w in d.get(n,[]):
   if not v(w):return False
  active.remove(n);done.add(n);return True
 return all(v(n) for n in d)
a=read(O/'entry-authentication.json');p=a['GOVERNANCE_REFERENCE_PIN'];must(sha(R/p['path'])==p['raw_sha256'],'governancepin');gov=read(R/p['path']);must(gov['GOVERNANCE_INTERPRETATION_EFFECTIVE'] and gov['INTERPRETATION_IDENTITY']==a['GOVERNANCE_INTERPRETATION_IDENTITY'] and not gov['PROBE_EXECUTION_AUTHORIZED'],'governancescope')
for p in gov['VERIFICATION_PINS']:must(sha(R/p['path'])==p['raw_sha256'],'governanceproofpin')
for folder in ['launch-actor-resource-closure-104','launch-exclusivity-closure-103','fixed-command-bridge-102','host-capability-bootstrap-reassessment-101','system-probe-authority-87','system-process-enforcement-86']:
 for n,h in read(B/folder/'evidence-index.json').get('FILES',{}).items():
  if isinstance(h,str):must(sha(R/n if (R/n).is_file() else B/folder/n)==h,'priorindex')
for r in a['GRANT_REFERENCES']:
 must(sha(R/r['path'])==r['raw_sha256'],'grantref');ref=read(R/r['path']);p=ref['GRANT_RECORD_PIN'];must(sha(R/p['path'])==p['raw_sha256'],'grantpin');g=read(R/p['path']);body=g.get('CONTENT',g.get('RECORD'));must(hashlib.sha256(enc(body)).hexdigest()==r['identity']['sha256'],'grantid')
f=read(B/'fixed-command-bridge-102/logical-synthetic-identity-manifest.json');must(len(f['CONTENT']['FIXTURES'])==12 and sum(len(enc(x)) for x in f['CONTENT']['FIXTURES'])==36710 and len(enc(f))==37056,'fixturefigures')
inv=read(O/'twelve-case-fixture-operation-inventory.json');cs=inv['CASES'];must(len(cs)==12,'cases')
for c in cs:
 orig=next(x for x in f['CONTENT']['FIXTURES'] if x['CONTENT']['TEST_ID']==c['CASE_ID']);must(c['FIXTURE_IDENTITY']==orig['IDENTITY'] and c['SYNTHETIC_GRANT_IDENTITY']==orig['CONTENT']['SYNTHETIC_GRANT']['IDENTITY'],'caseidentities')
must(sum(c['CLAIM_REQUESTS'] for c in cs)==23 and sum(c['EXCLUSIVE_RESERVATIONS_ATTEMPTED'] for c in cs)==14 and sum(c['FULL_CLAIM_PUBLICATIONS'] for c in cs)==8 and sum(c['EXPECTED_CALLBACKS'] for c in cs)==6 and sum(c['EXPECTED_RECOVERY_RECORDS'] for c in cs)==3,'operationcounts')
s=read(O/'bounded-record-schemas.json');nb={x['SCHEMA_ID'][10:-3]:x['MAX_RECORD_BYTES'] for x in s['NORMAL_SCHEMAS']};cb={x['MAXIMAL_INSTANCE']['type']:x['MAX_RECORD_BYTES'] for x in s['CRITICAL_SCHEMAS']}
for r in s['NORMAL_SCHEMAS']+s['CRITICAL_SCHEMAS']:must(len(enc(r['MAXIMAL_INSTANCE']))==r['MAX_RECORD_BYTES'],'encodedbound')
for r in s['CRITICAL_SCHEMAS']:must(len(r['MAXIMAL_INSTANCE']['cause']['code'])>=max(map(len,s['CLOSED_CAUSE_CODES'])) and len(r['MAXIMAL_INSTANCE']['cause']['phase'])>=max(map(len,s['CLOSED_CAUSE_PHASES'])),'enummaxima')
reserve=read(O/'protected-critical-reserve.json');counts=reserve['RECORD_COUNTS'];must(counts=={'FIRST_CAUSAL_FAILURE':4,'SECONDARY_FAILURE':19,'UNKNOWN_OUTCOME':4,'RESOURCE_EXHAUSTION':4,'CONSUMPTION_STATE':4,'FINAL_AUDIT':1},'criticalbranchcounts');critical=sum(counts[t]*cb[t] for t in counts);must(critical==reserve['CRITICAL_RESERVE_BYTES']==32694,'criticalreserve')
w=read(O/'cumulative-write-model.json');nb['FINAL_INDEX']=len(enc(w['FINAL_INDEX_MAXIMAL_INSTANCE']));must(nb==w['NORMAL_RECORD_BOUNDS'],'normalbounds');must(w['INDEX_REFERENCE_COUNT']==82 and w['PARTIAL_SEED_RECORD_REFERENCED'],'indexclosure')
variant=read(O/'postclaim-revocation-variant.json')['SYNTHETIC_GRANT'];must(hashlib.sha256(enc(variant['CONTENT'])).hexdigest()==variant['IDENTITY']['sha256'],'variantid');must(w['FIXTURE_WRITES']==37056+len(enc(variant)),'variantpreparation')
base=w['FIXTURE_WRITES']+14*nb['EPOCH']+nb['CAMPAIGN_ACTIVATION'];prefix=0
for c,row in zip(cs,w['PER_CASE']):
 cnt={'CLAIM':c['FULL_CLAIM_PUBLICATIONS'],'REQUEST_AUDIT':c['CLAIM_REQUESTS'],'CALLBACK_WITNESS':2*c['EXPECTED_CALLBACKS'],'RECOVERY':c['EXPECTED_RECOVERY_RECORDS'],'PROCESS_OBSERVATION':c['HELPER_LAUNCHES'],'CASE_VERDICT':1};amount=sum(cnt[t]*nb[t] for t in cnt)+c['PARTIAL_SEED_BYTES'];must(cnt==row['COUNTS'] and amount==row['MAX_NORMAL_SUBMITTED_BYTES'],'casewrites');prefix+=amount
normal=base+prefix+2*nb['PROCESS_OBSERVATION']+nb['FINAL_INDEX'];must(normal==w['NORMAL_PATH_MAX_SUBMITTED_BYTES']==111665,'normalbytes')
for row in w['FAILURE_BRANCHES']:
 cbytes=sum(row['CRITICAL_COUNTS'][t]*cb[t] for t in counts);must(cbytes==row['CRITICAL_BYTES'],'branchcritical')
 if row['FAILURE_DURING_CASE']=='FINAL_INDEX_OR_AUDIT':must(row['TOTAL_MAX_SUBMITTED_BYTES']==normal+cbytes,'finalfailure')
 else:must(row['TOTAL_MAX_SUBMITTED_BYTES']==base+row['COMPLETED_PREFIX_BYTES']+row['ACTIVE_CASE_BYTES_EXCLUDING_VERDICT_AND_COMPLETED_HELPER_OBSERVATIONS']+2*nb['PROCESS_OBSERVATION']+cbytes,'branchsum')
must(max(normal,max(b['TOTAL_MAX_SUBMITTED_BYTES'] for b in w['FAILURE_BRANCHES']))==w['MAX_FEASIBLE_PATH_SUBMITTED_BYTES']==129825,'pathmaximum');must(normal+critical==w['PROTECTED_TOTAL_ALLOCATION_BYTES']==144359,'protectedallocation')
top=read(O/'process-topology-resource-model.json');must(sum(x['count'] for x in top['HELPER_LAUNCHES'])==4 and top['MAX_CHILD_LAUNCHES']==5 and top['MAX_PROCESS_LIFETIMES']==6 and top['MAX_PROCESSES']==4,'topologycounts');must(top['MAX_CPU_SECONDS'] is None and top['MAX_MEMORY_BYTES'] is None and top['MAX_WALL_SECONDS'] is None and not top['NUMERIC_CONTROLLER_LIMITS_COMPLETE'],'uncalibratedlimitsnotpromoted')
must(not any((R/p).exists() for p in a['SOURCE_PATHS']),'nosources')
reg=read(R/'docs/plans/PLANNER_REASONING_LESSONS_REGISTER_1.json');prev='0'*64
for e in reg['EVENTS']:
 must(e['PREVIOUS_EVENT_HASH']==prev,'lessonprevious');must(hashlib.sha256(json.dumps({k:v for k,v in e.items() if k!='EVENT_HASH'},sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()).hexdigest()==e['EVENT_HASH'],'lessonhash');prev=e['EVENT_HASH']
must(prev==a['LL11_HEAD'],'head');must(sha(B/'campaign-budget.jsonl')==a['STOPPED_JOURNAL_SHA256'],'journal')
graph=read(O/'qualification-dependency-graph.json');must(acyclic(graph['EDGES']),'graph')
state={'gov':a['GOVERNANCE_INTERPRETATION_IDENTITY'],'requests':23,'claimwrites':8,'failurebounded':True,'reserve':32694,'overwrites_counted':True,'concurrency':2,'arbitrary_runtime_limits':False,'host_enforcement_qualified':False,'actualcrashrequired':True,'independentobserverrequired':True,'duplicateconsumption':False,'realsystemd':False,'H77A15':False,'authorityissued':False}
def valid(x):
 must(x['gov']==a['GOVERNANCE_INTERPRETATION_IDENTITY'],'wronggovernance');must(x['requests']==23,'casecountasoperationcount');must(x['claimwrites']==8,'claimwriteomitted');must(x['failurebounded'],'unboundedfailure');must(x['reserve']==32694,'reservemissing');must(x['overwrites_counted'],'overwritebypass');must(x['concurrency']==2,'unboundedconcurrency');must(not x['arbitrary_runtime_limits'],'arbitraryCPU/memory');must(not x['host_enforcement_qualified'],'unknownenforcementqualified');must(x['actualcrashrequired'],'exceptionascrash');must(x['independentobserverrequired'],'observermissing');must(not x['duplicateconsumption'],'duplicategrant');must(not x['realsystemd'],'realsystemd');must(not x['H77A15'],'H77A15');must(not x['authorityissued'],'prematureauthority')
valid(state)
mut=[('wronggovernance','gov',{}),('fixturecountasoperations','requests',12),('missingclaimwrite','claimwrites',0),('unboundedfailure','failurebounded',False),('missingreserve','reserve',0),('overwritebypass','overwrites_counted',False),('unboundedconcurrency','concurrency',3),('arbitraryCPU/memory','arbitrary_runtime_limits',True),('unknownenforcementqualified','host_enforcement_qualified',True),('exceptioncrashsubstitution','actualcrashrequired',False),('observermissing','independentobserverrequired',False),('duplicategrant','duplicateconsumption',True),('realsystemd','realsystemd',True),('H77A15','H77A15',True),('prematureauthority','authorityissued',True)]
neg=[]
for name,k,v in mut:
 x=copy.deepcopy(state);x[k]=v
 try:valid(x)
 except ValueError as e:neg.append({'CONTROL':name,'RESULT':'REJECTED','CAUSE':str(e)})
 else:raise ValueError('accepted:'+name)
r={'GOVERNANCE_IDENTITY':a['GOVERNANCE_INTERPRETATION_IDENTITY'],'CASES':12,'REQUESTS':23,'CLAIM_WRITES':8,'NORMAL_BYTES':111665,'CRITICAL_RESERVE':32694,'MAX_MODELED_FEASIBLE_PATH':129825,'PROTECTED_ALLOCATION':144359,'CPU_MEMORY_WALL_FD_COMPLETE':False,'CONSTRUCTION_DECISION_READY':False,'GRAPH_ACYCLIC':True,'LL11_HEAD':prev,'NEGATIVES':neg,'CONTRACT_PINS':{p.name:sha(p) for p in O.glob('*.json') if p.name not in ['preservation-before.json','independent-static-verification.json','four-seed-reconstruction.json','negative-control-results.json','governance-authentication.json','preservation-audit.json','report.json','evidence-index.json']},'ASSURANCE':'independentcodec/arithmetic/closedprotocolmodel only;notimplemented/enforcedorobservedruntime;unregisteredexternalfacilityoutput wouldrequire budget recomputation'}
print(json.dumps({'HASH_SEED':os.environ.get('PYTHONHASHSEED'),'RECONSTRUCTION':r,'SEMANTIC_SHA256':hashlib.sha256(enc(r)).hexdigest()},sort_keys=True))
