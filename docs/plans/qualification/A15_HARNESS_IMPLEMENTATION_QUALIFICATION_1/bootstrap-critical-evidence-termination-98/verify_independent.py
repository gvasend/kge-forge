"""Independent AST/JSON analysis; target modules never imported or executed."""
import ast,copy,hashlib,json,os,pathlib
R=pathlib.Path(__file__).resolve().parents[5];B=R/'docs/plans/qualification/A15_HARNESS_IMPLEMENTATION_QUALIFICATION_1';O=pathlib.Path(__file__).parent

def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def enc(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def require(x,s):
 if not x:raise ValueError(s)
def acyclic(es):
 adj={}
 for e in es:adj.setdefault(e['from'],[]).append(e['to'])
 done=set();active=set()
 def visit(v):
  if v in active:return False
  if v in done:return True
  active.add(v)
  for w in adj.get(v,[]):
   if not visit(w):return False
  active.remove(v);done.add(v);return True
 return all(visit(v) for v in adj)
a=read(O/'entry-authentication.json')
for p,h in a['SOURCE_IDENTITIES'].items():require(sha(R/p)==h,'retained source hash')
for folder in ['bootstrap-resource-watchdog-97','bootstrap-inert-environment-96','bootstrap-entry-oracle-repair-95']:
 for p,h in read(B/folder/'evidence-index.json')['FILES'].items():require(sha(B/folder/p)==h,'prior evidence pin')
for r in a['GRANT_REFERENCES']:
 require(sha(R/r['path'])==r['raw_sha256'],'effective reference pin');ref=read(R/r['path']);p=ref['GRANT_RECORD_PIN'];require(sha(R/p['path'])==p['raw_sha256'],'issued pin');g=read(R/p['path']);body=g.get('CONTENT',g.get('RECORD'));require(hashlib.sha256(enc(body)).hexdigest()==r['identity']['sha256'],'issued identity')
 for p in ref['VERIFICATION_PINS']:require(sha(R/p['path'])==p['raw_sha256'],'qualification pin')
core=(R/'adapter/qualification_bootstrap/systemd_pids_once.py').read_text();test=(R/'adapter/tests/test_systemd_pids_bootstrap.py').read_text();tree=ast.parse(core);tt=ast.parse(test)
f={n.name:n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef)}
charge=ast.get_source_segment(core,f['charge']);require("not budget['stopped'] and time.monotonic_ns() < budget['deadline_ns']" in charge,'retained critical guards')
pub=ast.get_source_segment(core,f['_publish']);require('raw = canonical(value)' in pub and 'len(raw) <= ORDINARY_RECORD_MAX_BYTES' in pub,'accepted cap not unbounded')
require('str(original)' in ast.get_source_segment(core,f['consume_inert']) and 'start_new_session=True' in test,'failure input/session findings')
require('os.killpg(child.pid, 9)' in test,'per-helper group behavior')
schemas=read(O/'critical-record-schemas.json');reserve=read(O/'numeric-critical-reserve.json')
require(len(schemas['SCHEMAS'])==8,'record types');count=0;payload=0
for s,m in zip(schemas['SCHEMAS'],schemas['MAXIMAL_INSTANCES']):
 require(s['TYPE']==m['TYPE'] and s['MAX_OCCURRENCES']==m['COUNT'],'typed count binding')
 require(s['MAX_RECORD_BYTES']==len(enc(m['MAXIMAL_INSTANCE']))==m['MAX_ENCODED_BYTES'],'independent encoded byte bound')
 require(m['MAX_TOTAL_BYTES']==m['COUNT']*m['MAX_ENCODED_BYTES'],'multiplication')
 require(m['MAX_ENCODED_BYTES']<=65536,'ordinary cap intact')
 count+=m['COUNT'];payload+=m['MAX_TOTAL_BYTES']
indexbytes=len(enc(schemas['INDEX_MAXIMAL_INSTANCE']));require(len(schemas['INDEX_MAXIMAL_INSTANCE']['events'])==count==71,'fixed finite slots')
require(indexbytes==schemas['INDEX_MAX_BYTES'] and payload+indexbytes==reserve['CRITICAL_RESERVE_BYTES']==81366,'reserve derivation')
fixtures=read(B/'bootstrap-inert-readiness-92/sealed-synthetic-fixture-manifest.json')['CONTENT'];stores=set()
for c in fixtures['FIXTURES']:
 for v in c['CONTENT']['VARIANTS']:stores.add(v['CONTENT']['INPUT']['RELATIVE_STORE_PATH'])
require(len(stores)==19,'consumption store count')
records={};model=read(B/'bootstrap-entry-oracle-closure-93/inline-size-model-max.json')['ENTRY']
for v in model['fixtures'].values():
 for n,h in v['expected_records'].items():
  k=(v['entry']['store'],n);raw=bytes.fromhex(h);require(k not in records or records[k]==raw,'shared record');records[k]=raw
require(sum(map(len,records.values()))==23285,'known record subtotal')
budget=read(O/'complete-write-budget-analysis.json');require(1048576-928340==120236 and 1048576-(928340+5109+23285+81366)==budget['A_PROVISIONAL_REMAINDER_BEFORE_UNKNOWN_NORMAL_WRITES']==10476,'known arithmetic')
require(not budget['WRITE_BUDGET_COMPLETE'] and budget['COMPLETE_MAXIMUM'] is None,'unknown terms not promoted')
graph=read(O/'dependency-graph.json');require(acyclic(graph['EDGES']),'prospective graph')
reg=read(R/'docs/plans/PLANNER_REASONING_LESSONS_REGISTER_1.json');prev='0'*64
for e in reg['EVENTS']:
 require(e['PREVIOUS_EVENT_HASH']==prev,'lesson predecessor');require(hashlib.sha256(json.dumps({k:v for k,v in e.items() if k!='EVENT_HASH'},sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()).hexdigest()==e['EVENT_HASH'],'lesson hash');prev=e['EVENT_HASH']
require(prev==a['LL11_HEAD'],'LL11 head');require(sha(B/'campaign-budget.jsonl')==a['STOPPED_JOURNAL_SHA256'],'stopped journal')
s={'late_evidence_requires_new_scope':True,'bounded_record_shapes':True,'ordinary_reserve_access':False,'late_workload_restart':False,'parent_group_complete':False,'escape_ignored':False,'watchdog_failure_success':False,'exit_witness_required':True,'unknown_termination_complete':False,'workload_limit':1048576,'control_plane_currently_exempt':False,'graph':graph['EDGES'],'real_system_operations':False,'real_H77_A15':False,'issued_authority':False}
def valid(x):
 require(x['late_evidence_requires_new_scope'],'critical post-stop authority');require(x['bounded_record_shapes'],'unbounded failure');require(not x['ordinary_reserve_access'],'reserve ordinary bypass');require(not x['late_workload_restart'],'renewed workload');require(not x['parent_group_complete'],'parent-only boundary');require(not x['escape_ignored'],'escape ignored');require(not x['watchdog_failure_success'],'watchdog failure success');require(x['exit_witness_required'],'missing exit witness');require(not x['unknown_termination_complete'],'unknown complete');require(x['workload_limit']==1048576,'budget increased');require(not x['control_plane_currently_exempt'],'unauthorized exemption');require(acyclic(x['graph']),'circular dependency');require(not x['real_system_operations'],'real systemd sudo bwrap');require(not x['real_H77_A15'],'real H77 A15');require(not x['issued_authority'],'premature issuance')
valid(s)
mut=[('critical remains blocked/no new scope','late_evidence_requires_new_scope',False),('unbounded failure record','bounded_record_shapes',False),('ordinary consumes reserve','ordinary_reserve_access',True),('postdeadline restart','late_workload_restart',True),('parent group watchdog sufficient','parent_group_complete',True),('escaped helper ignored','escape_ignored',True),('watchdog failure success','watchdog_failure_success',True),('descendant witness omitted','exit_witness_required',False),('unknown termination complete','unknown_termination_complete',True),('resource ceiling increased','workload_limit',1048577),('control plane exempted','control_plane_currently_exempt',True),('qualification cycle','graph',graph['EDGES']+[{'from':'PROCESS_BOUNDARY','to':'BOOTSTRAP_INERT_QUALIFICATION'}]),('real system operations','real_system_operations',True),('H77 A15 operations','real_H77_A15',True),('premature grant','issued_authority',True)]
neg=[]
for name,k,v in mut:
 x=copy.deepcopy(s);x[k]=v
 try:valid(x)
 except ValueError as e:neg.append({'CONTROL':name,'RESULT':'REJECTED','CAUSE':str(e)})
 else:raise ValueError('negative accepted:'+name)
recon={'SOURCES':a['SOURCE_IDENTITIES'],'SOURCE_DEFECTS':'SUPPORTED_STATIC_NOT_RUNTIME','MAX_EVENTS':count,'CRITICAL_PROPOSED_RESERVE':payload+indexbytes,'A_UNQUALIFIED_NORMAL_REMAINDER':10476,'WRITE_BUDGET_COMPLETE':False,'CAUSAL_COMPLETENESS':False,'WATCHDOG_QUALIFIED':False,'DECISION_READY':False,'GRAPH_ACYCLIC':True,'LL11_HEAD':prev,'NEGATIVES':neg,'CONTRACT_PINS':{p.name:sha(p) for p in O.glob('*.json') if p.name not in ['preservation-before.json','independent-static-verification.json','four-seed-reconstruction.json','negative-control-results.json','governance-authentication.json','report.json','preservation-audit.json','evidence-index.json']},'ASSURANCE':'Independent metadata sizing,AST and static fail-closed reporting mutations only; no target imports or operational qualification'}
print(json.dumps({'HASH_SEED':os.environ.get('PYTHONHASHSEED'),'RECONSTRUCTION':recon,'SEMANTIC_SHA256':hashlib.sha256(enc(recon)).hexdigest()},sort_keys=True))
