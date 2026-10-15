"""Read-only100 AST/JSON reconstruction;no target import/execution."""
import ast,copy,hashlib,json,os,pathlib
R=pathlib.Path(__file__).resolve().parents[5];B=R/'docs/plans/qualification/A15_HARNESS_IMPLEMENTATION_QUALIFICATION_1';O=pathlib.Path(__file__).parent

def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def enc(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def must(v,m):
 if not v:raise ValueError(m)
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
a=read(O/'entry-authentication.json');must(a['APPROVED_CAMPAIGN_COUNT']==1 and a['APPROVED_INERT_CASES']==14,'exact authority scope')
for p,h in a['SOURCE_IDENTITIES'].items():must(sha(R/p)==h,'source pin')
for folder in ['bootstrap-strategy-simplification-99','bootstrap-critical-evidence-termination-98','bootstrap-resource-watchdog-97','bootstrap-inert-environment-96','bootstrap-entry-oracle-repair-95']:
 for p,h in read(B/folder/'evidence-index.json')['FILES'].items():must(sha(B/folder/p)==h,'prior evidence')
for r in a['EFFECTIVE_GRANT_REFERENCES']:
 must(sha(R/r['path'])==r['raw_sha256'],'effective ref');ref=read(R/r['path']);p=ref['GRANT_RECORD_PIN'];must(sha(R/p['path'])==p['raw_sha256'],'grant raw');g=read(R/p['path']);body=g.get('CONTENT',g.get('RECORD'));must(hashlib.sha256(enc(body)).hexdigest()==r['identity']['sha256'],'grant identity')
 for p in ref['VERIFICATION_PINS']:must(sha(R/p['path'])==p['raw_sha256'],'issuance pin')
txt=(R/'adapter/tests/test_systemd_pids_bootstrap.py').read_text();tree=ast.parse(txt)
def name(n):
 if isinstance(n,ast.Name):return n.id
 if isinstance(n,ast.Attribute):return name(n.value)+'.'+n.attr
 return '<dynamic>'
spawns=[(name(n.func),n.lineno) for n in ast.walk(tree) if isinstance(n,ast.Call) and name(n.func) in ['subprocess.Popen','os.fork','os.posix_spawn','os.spawnv','os.system','os.execve','os.setsid']];must(spawns==[('subprocess.Popen',356)],'parent spawn site')
helper=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='helper');must(not any(isinstance(n,ast.Call) and name(n.func) in ['subprocess.Popen','os.fork','os.posix_spawn','os.system'] for n in ast.walk(helper)),'explicit helper spawn')
must('start_new_session=True' in txt and 'child.wait(timeout=remaining)' in txt and 'os.killpg(child.pid, 9)' in txt,'known lifecycle')
d=read(O/'descendant-creation-assessment.json')
for p in d['DEPENDENCY_PINS']+d['STARTUP_OBSERVATIONS']:must(sha(pathlib.Path(p['path']))==p['raw_sha256'],'runtime observed pin')
site=pathlib.Path('/usr/lib/python3.8/site.py').read_text();sub=pathlib.Path('/usr/lib/python3.8/subprocess.py').read_text();must('exec(line)' in site and 'execsitecustomize()' in site and 'addsitepackages' in site,'global startup scope');must('_posixsubprocess.fork_exec' in sub and 'os.posix_spawn' in sub,'native spawn capability')
causal=read(O/'compact-causal-evidence-schema.json');must(len(enc(causal['PROPOSED_SCHEMA_FIELDS']))==causal['BASE_SHAPE_BYTES'],'candidate byte count');must(not causal['COMPACT_CAUSAL_EVIDENCE_COMPLETE'] and causal['MAX_SERIALIZED_BYTES'] is None,'unverified causal closure')
budget=read(O/'cumulative-write-model.json');must(1048576-928340==budget['REMAINING_WRITE_BUDGET']==120236,'starting budget');must(120236-28394-81366==10476,'old candidate arithmetic');must(1048576-(928340+28394+70422)==21420,'compact99 arithmetic');must(budget['TOTAL_MAX_WRITES'] is None and not budget['NUMERIC_WRITE_BUDGET_COMPLETE'],'unknown complete budget')
integrated=read(O/'integrated-feasibility.json');must(integrated['INTEGRATED_FEASIBILITY']=='UNDETERMINED','feasibility classification');pin=integrated['BINDING_ASSURANCE_MATRIX'];must(sha(R/pin['path'])==pin['raw_sha256'],'requirements matrix')
graph=read(O/'qualification-dependency-graph.json');must(acyclic(graph['EDGES']),'graph')
reg=read(R/'docs/plans/PLANNER_REASONING_LESSONS_REGISTER_1.json');prev='0'*64
for e in reg['EVENTS']:
 must(e['PREVIOUS_EVENT_HASH']==prev,'lesson linkage');must(hashlib.sha256(json.dumps({k:v for k,v in e.items() if k!='EVENT_HASH'},sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()).hexdigest()==e['EVENT_HASH'],'lesson hash');prev=e['EVENT_HASH']
must(prev==a['LL11_HEAD'],'head');must(sha(B/'campaign-budget.jsonl')==a['STOPPED_JOURNAL_SHA256'],'stopped journal')
s={'untracked_terminated':False,'sessions_covered_by_parent':False,'parent_timeout_sufficient':False,'watchdog_depends_on_parent':False,'unknown_exit_success':False,'unverified_ref_accepted':False,'first_failure_required':True,'unbounded_failure_accepted':False,'overwrites_counted':True,'deletion_refunds':False,'ordinary_uses_reserve':False,'late_restart':False,'control_authority_assumed':False,'ceiling':1048576,'graph':graph['EDGES'],'execution_authorized':False}
def valid(x):
 must(not x['untracked_terminated'],'untracked descendant');must(not x['sessions_covered_by_parent'],'separate session ignored');must(not x['parent_timeout_sufficient'],'parent timeout accepted');must(not x['watchdog_depends_on_parent'],'dependent watchdog');must(not x['unknown_exit_success'],'unknown exit success');must(not x['unverified_ref_accepted'],'unverifiable ref');must(x['first_failure_required'],'first failure missing');must(not x['unbounded_failure_accepted'],'unbounded failure');must(x['overwrites_counted'],'overwrite bypass');must(not x['deletion_refunds'],'deleted bypass');must(not x['ordinary_uses_reserve'],'reserve bypass');must(not x['late_restart'],'late restart');must(not x['control_authority_assumed'],'authority assumed');must(x['ceiling']==1048576,'ceiling increase');must(acyclic(x['graph']),'cycle');must(not x['execution_authorized'],'premature execution')
valid(s)
mut=[('untracked descendant terminated','untracked_terminated',True),('separate session ignored','sessions_covered_by_parent',True),('parent timeout sufficient','parent_timeout_sufficient',True),('watchdog depends on parent','watchdog_depends_on_parent',True),('unknown termination success','unknown_exit_success',True),('unverifiable reference','unverified_ref_accepted',True),('missing first failure','first_failure_required',False),('unbounded failure accepted','unbounded_failure_accepted',True),('overwrite bypass','overwrites_counted',False),('delete refund','deletion_refunds',True),('ordinary steals reserve','ordinary_uses_reserve',True),('postdeadline restart','late_restart',True),('unqualified controlplane authority','control_authority_assumed',True),('ceiling increase','ceiling',1048577),('qualification cycle','graph',graph['EDGES']+[{'from':'INDEPENDENT_RUNTIME_CLOSURE_OR_KERNEL_BOUNDARY','to':'INERT_QUALIFICATION'}]),('premature execution approval','execution_authorized',True)]
neg=[]
for id,k,v in mut:
 x=copy.deepcopy(s);x[k]=v
 try:valid(x)
 except ValueError as e:neg.append({'CONTROL':id,'RESULT':'REJECTED','CAUSE':str(e)})
 else:raise ValueError('accepted:'+id)
r={'SOURCES':a['SOURCE_IDENTITIES'],'EXPLICIT_PARENT_POPEN_SITES':spawns,'PLANNED_HELPERS':10,'NO_DIRECT_HELPER_SPAWN_CALL':True,'GLOBAL_STARTUP_CLOSURE_QUALIFIED':False,'DESCENDANT_COVERAGE_COMPLETE':False,'MINIMAL_SUPERVISOR_FEASIBLE':'UNDETERMINED','CAUSAL_COMPLETE':False,'NUMERIC_BUDGET_COMPLETE':False,'FEASIBILITY':'UNDETERMINED','DECISION_READY':False,'GRAPH_ACYCLIC':True,'LL11_HEAD':prev,'NEGATIVES':neg,'CONTRACT_PINS':{p.name:sha(p) for p in O.glob('*.json') if p.name not in ['preservation-before.json','independent-static-verification.json','four-seed-reconstruction.json','negative-control-results.json','governance-authentication.json','report.json','preservation-audit.json','evidence-index.json']},'ASSURANCE':'AST/library-source/JSON static reconstruction and reporting mutations only;no target imports,active descendants or enforcement tests'}
print(json.dumps({'HASH_SEED':os.environ.get('PYTHONHASHSEED'),'RECONSTRUCTION':r,'SEMANTIC_SHA256':hashlib.sha256(enc(r)).hexdigest()},sort_keys=True))
