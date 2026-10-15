"""Metadata-only99 reconstruction. Never import or execute target modules."""
import json,pathlib,hashlib,ast,copy,os
R=pathlib.Path(__file__).resolve().parents[5];B=R/'docs/plans/qualification/A15_HARNESS_IMPLEMENTATION_QUALIFICATION_1';O=pathlib.Path(__file__).parent

def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def enc(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def require(v,m):
 if not v:raise ValueError(m)
def acyclic(es):
 a={}
 for e in es:a.setdefault(e['from'],[]).append(e['to'])
 done=set();active=set()
 def v(n):
  if n in active:return False
  if n in done:return True
  active.add(n)
  for w in a.get(n,[]):
   if not v(w):return False
  active.remove(n);done.add(n);return True
 return all(v(n) for n in a)
auth=read(O/'entry-authentication.json')
for p,h in auth['SOURCE_IDENTITIES'].items():require(sha(R/p)==h,'source pin')
for folder in ['bootstrap-critical-evidence-termination-98','bootstrap-resource-watchdog-97','bootstrap-inert-environment-96','bootstrap-entry-oracle-repair-95']:
 for n,h in read(B/folder/'evidence-index.json')['FILES'].items():require(sha(B/folder/n)==h,'prior record pin')
grants=[]
for r in auth['GRANT_REFERENCES']:
 require(sha(R/r['path'])==r['raw_sha256'],'effective ref');ref=read(R/r['path']);p=ref['GRANT_RECORD_PIN'];require(sha(R/p['path'])==p['raw_sha256'],'grant pin');g=read(R/p['path']);body=g.get('CONTENT',g.get('RECORD'));require(hashlib.sha256(enc(body)).hexdigest()==r['identity']['sha256'],'grant identity');grants.append(body)
 for p in ref['VERIFICATION_PINS']:require(sha(R/p['path'])==p['raw_sha256'],'issuance pin')
require(grants[0]['PERMITTED_INERT_TESTS']==auth['EXACT14_TEST_SET'],'exact grant tests')
for pin in grants[0]['BOOTSTRAP_CONTRACT_PINS'].values():require(sha(R/pin['path'])==pin['raw_sha256'],'adopted contract')
core=ast.parse((R/'adapter/qualification_bootstrap/systemd_pids_once.py').read_text());tt=ast.parse((R/'adapter/tests/test_systemd_pids_bootstrap.py').read_text());names=[n.name for n in ast.walk(tt) if isinstance(n,ast.FunctionDef) and n.name.startswith('test_')];require(len(names)==14,'test count')
mat=read(O/'requirement-to-authority-matrix.json')
for r in mat['REQUIREMENTS']:
 pin=r['SOURCE_IDENTITY'];require(sha(R/pin['path'])==pin['raw_sha256'],'requirement source')
 forid=r['REQUIREMENT_ID']
 if forid in auth['EXACT14_TEST_SET']:require(r['AUTHORITY_LEVEL']=='ISSUED_GRANT_CONDITION','binding test classification')
 if forid in ['Q99-KERNEL','Q99-71EVENTS']:require(r['AUTHORITY_LEVEL']=='PROSPECTIVE_DESIGN_CHOICE','prospective classification')
A=read(O/'alternative-a-reduced-evidence.json');BALT=read(O/'alternative-b-partitioned-campaigns.json');C=read(O/'alternative-c-bootstrap-subset.json');cost=read(O/'resource-feasibility-comparison.json');model=read(B/'bootstrap-entry-oracle-closure-93/inline-size-model-max.json')['ENTRY']
partsets=[set(p['TESTS']) for p in BALT['PARTITIONS']];require(not(partsets[0]&partsets[1]) and set.union(*partsets)==set(auth['EXACT14_TEST_SET']),'partition coverage')
require(BALT['PROJECTED_TOTAL_HELPERS']==11 and cost['BASELINE']['PLANNED_HELPERS']==10 and C['RESOURCE_MODEL']['PLANNED_HELPERS']==10,'helper cost')
for p in BALT['PARTITIONS']+[C['RESOURCE_MODEL'],cost['BASELINE']]:
 projection=copy.deepcopy(model);projection['fixtures']={k:v for k,v in projection['fixtures'].items() if v['entry']['test_id'] in p['TESTS']};require(len(enc(projection))==p['PROJECTED_ROOT_BYTES'],'projected canonical size');require(len(projection['fixtures'])==p['RUNTIME_VARIANTS'],'variant coverage');require(p['TOTAL_MAX_WRITES'] is None and not p['RESOURCE_FEASIBLE'],'unbounded cost not promoted')
require(sum(p['RUNTIME_VARIANTS'] for p in BALT['PARTITIONS'])==21,'all variants');require(len(C['MINIMAL_TEST_SET'])==11 and len(C['OMISSIONS'])==3,'subset')
require(A['PROJECTED_CRITICAL_RESERVE']==sum(r['MAX_TOTAL_BYTES'] for r in A['DERIVED_COMPACT_RECORD_SHAPES'])+read(B/'bootstrap-critical-evidence-termination-98/critical-record-schemas.json')['INDEX_MAX_BYTES']==70422,'reference size')
require(1048576-(928340+28394+70422)==A['PROVISIONAL_UNALLOCATED']==21420,'reference arithmetic')
graph=read(O/'qualification-dependency-graph.json');require(acyclic(graph['EDGES']),'acyclic proposed graph')
reg=read(R/'docs/plans/PLANNER_REASONING_LESSONS_REGISTER_1.json');prev='0'*64
for e in reg['EVENTS']:
 require(e['PREVIOUS_EVENT_HASH']==prev,'lesson predecessor');require(hashlib.sha256(json.dumps({k:v for k,v in e.items() if k!='EVENT_HASH'},sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()).hexdigest()==e['EVENT_HASH'],'lesson hash');prev=e['EVENT_HASH']
require(prev==auth['LL11_HEAD'],'register head');require(sha(B/'campaign-budget.jsonl')==auth['STOPPED_JOURNAL_SHA256'],'stopped journal')
s={'binding_optional':False,'subset_full_qualified':False,'partition_retry':False,'reuse_grant':False,'missing_cause_ok':False,'max_ref_count':213,'failure_bounded_required':True,'unknown_surplus':False,'parent_only_watchdog':False,'unknown_survivor_ok':False,'graph':graph['EDGES'],'unissued_effective':False,'source_changed':False,'activated':False,'H77_A15':False}
def valid(x):
 require(not x['binding_optional'],'binding optional');require(not x['subset_full_qualified'],'subset full');require(not x['partition_retry'],'partition retry');require(not x['reuse_grant'],'grant reused');require(not x['missing_cause_ok'],'causal evidence missing');require(x['max_ref_count']==213,'unbounded reference');require(x['failure_bounded_required'],'unbounded failure');require(not x['unknown_surplus'],'unknown deficit/surplus');require(not x['parent_only_watchdog'],'parent-only');require(not x['unknown_survivor_ok'],'unknown survivor');require(acyclic(x['graph']),'cycle');require(not x['unissued_effective'],'unissued effective');require(not x['source_changed'],'source changed');require(not x['activated'],'activated');require(not x['H77_A15'],'real execution')
valid(s)
mut=[('binding optional','binding_optional',True),('subset full qualification','subset_full_qualified',True),('partition retry','partition_retry',True),('reused grant','reuse_grant',True),('missing causal evidence','missing_cause_ok',True),('unbounded references','max_ref_count',None),('unbounded failure accepted','failure_bounded_required',False),('unknown deficit treated surplus','unknown_surplus',True),('parent-only watchdog','parent_only_watchdog',True),('unknown survivor ignored','unknown_survivor_ok',True),('qualification cycle','graph',graph['EDGES']+[{'from':'INDEPENDENT_CONTROLLER_TRUST_ROOT','to':'INERT_QUALIFICATION'}]),('unissued authority effective','unissued_effective',True),('unauthorized source changed','source_changed',True),('premature activation','activated',True),('H77 A15 execution','H77_A15',True)]
neg=[]
for name,k,v in mut:
 x=copy.deepcopy(s);x[k]=v
 try:valid(x)
 except ValueError as e:neg.append({'CONTROL':name,'RESULT':'REJECTED','CAUSE':str(e)})
 else:raise ValueError('negative accepted:'+name)
recon={'SOURCES':auth['SOURCE_IDENTITIES'],'BINDING_TESTS':auth['EXACT14_TEST_SET'],'REQUIREMENT_COUNT':len(mat['REQUIREMENTS']),'A_PROPOSED_RESERVE':70422,'A_UNKNOWN_REMAINDER':21420,'B_PARTITION_MODEL_BYTES':[p['PROJECTED_ROOT_BYTES'] for p in BALT['PARTITIONS']],'B_HELPERS':11,'C_HELPERS':10,'C_SUBSET_MODEL_BYTES':C['RESOURCE_MODEL']['PROJECTED_ROOT_BYTES'],'FEASIBILITY_ESTABLISHED':False,'PREFERRED_STRATEGY':'NO_ALTERNATIVE_SELECTED','DECISION_READY':False,'GRAPH_ACYCLIC':True,'LL11_HEAD':prev,'NEGATIVES':neg,'CONTRACT_PINS':{p.name:sha(p) for p in O.glob('*.json') if p.name not in ['preservation-before.json','independent-static-verification.json','four-seed-reconstruction.json','negative-control-results.json','governance-authentication.json','preservation-audit.json','report.json','evidence-index.json']},'ASSURANCE':'AST/JSON comparisons and mutated reporting contracts only; no target imports/behavior or OS tests'}
print(json.dumps({'HASH_SEED':os.environ.get('PYTHONHASHSEED'),'RECONSTRUCTION':recon,'SEMANTIC_SHA256':hashlib.sha256(enc(recon)).hexdigest()},sort_keys=True))
