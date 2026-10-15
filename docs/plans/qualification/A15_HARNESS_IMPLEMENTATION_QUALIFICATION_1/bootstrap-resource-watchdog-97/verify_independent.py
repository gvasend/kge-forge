"""Read-only AST/JSON reconstruction; no target import or active control tests."""
import ast,copy,hashlib,json,os,pathlib
R=pathlib.Path(__file__).resolve().parents[5];B=R/'docs/plans/qualification/A15_HARNESS_IMPLEMENTATION_QUALIFICATION_1';O=pathlib.Path(__file__).parent

def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def enc(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def must(x,msg):
 if not x:raise ValueError(msg)
def cycle_free(edges):
 a={}
 for e in edges:a.setdefault(e['from'],[]).append(e['to'])
 active=set();done=set()
 def v(n):
  if n in active:return False
  if n in done:return True
  active.add(n)
  for m in a.get(n,[]):
   if not v(m):return False
  active.remove(n);done.add(n);return True
 return all(v(n) for n in a)
auth=read(O/'entry-authentication.json')
for p,h in auth['SOURCE_IDENTITIES'].items():must(sha(R/p)==h,'source pin')
for folder in ['bootstrap-entry-oracle-repair-95','bootstrap-inert-environment-96']:
 for p,h in read(B/folder/'evidence-index.json')['FILES'].items():must(sha(B/folder/p)==h,'prior evidence pin')
for r in auth['EFFECTIVE_GRANT_PINS']:
 must(sha(R/r['path'])==r['raw_sha256'],'effective reference');ref=read(R/r['path']);p=ref['GRANT_RECORD_PIN'];must(sha(R/p['path'])==p['raw_sha256'],'grant raw');g=read(R/p['path']);body=g.get('RECORD',g.get('CONTENT'));must(hashlib.sha256(enc(body)).hexdigest()==r['identity']['sha256'],'grant identity')
 for p in ref['VERIFICATION_PINS']:must(sha(R/p['path'])==p['raw_sha256'],'issuance pin')
limits=read(O/'resource-watchdog-compatibility.json')['APPROVED_LIMITS'];must(limits==body.get('RESOURCE_LIMITS',limits),'unchanged grant resource scope')
model=read(B/'bootstrap-entry-oracle-closure-93/inline-size-model-max.json')['ENTRY'];records={}
for f in model['fixtures'].values():
 for n,h in f['expected_records'].items():
  k=(f['entry']['store'],n);raw=bytes.fromhex(h)
  must(k not in records or records[k]==raw,'shared snapshot consistency');records[k]=raw
fixture=read(B/'bootstrap-inert-readiness-92/sealed-synthetic-fixture-manifest.json');epochs={}
must(hashlib.sha256(enc(fixture['CONTENT'])).hexdigest()==fixture['IDENTITY']['sha256'],'fixture identity')
for c in fixture['CONTENT']['FIXTURES']:
 for v in c['CONTENT']['VARIANTS']:
  i=v['CONTENT']['INPUT'];k=i['RELATIVE_STORE_PATH'];raw=enc(i['EPOCH']);must(k not in epochs or epochs[k]==raw,'shared epoch');epochs[k]=raw
budget=read(O/'numeric-budget-and-reserve.json');must(sum(map(len,records.values()))==budget['EXACT_SEALED_NORMATIVE_RECORD_SUBTOTAL']==23285,'record subtotal');must(sum(map(len,epochs.values()))==budget['EXACT_CANONICAL_EPOCH_SUBTOTAL']==5109,'epoch subtotal');must(1048576-(10*65536+65536+207444)==budget['REMAINING_WRITE_BUDGET']==120236,'fixed reservation')
must(budget['CONSERVATIVE_ACCEPTED_RECORD_ENVELOPE']['TOTAL']==3*2*65536==393216 and budget['CONSERVATIVE_ACCEPTED_RECORD_ENVELOPE']['DEFICIT_VS_120236']==272980,'candidate deficit')
core=(R/'adapter/qualification_bootstrap/systemd_pids_once.py').read_text();test=(R/'adapter/tests/test_systemd_pids_bootstrap.py').read_text();ct=ast.parse(core);tt=ast.parse(test)
functions={n.name:n for n in ast.walk(ct) if isinstance(n,ast.FunctionDef)}
charge=ast.get_source_segment(core,functions['charge']);must("not budget['stopped'] and time.monotonic_ns() < budget['deadline_ns']" in charge and "if critical else reserve" in charge,'critical deadline observation')
pub=ast.get_source_segment(core,functions['_publish']);must('len(raw) <= ORDINARY_RECORD_MAX_BYTES' in pub,'failure-record cap')
must('start_new_session=True' in test and 'os.killpg(child.pid, 9)' in test,'separate helper sessions')
writeall=ast.get_source_segment(core,functions['_write_all']);must('raw[offset:]' in writeall and 'offset += n' in writeall,'short-write discriminator')
reg=read(R/'docs/plans/PLANNER_REASONING_LESSONS_REGISTER_1.json');prev='0'*64
for e in reg['EVENTS']:
 must(e['PREVIOUS_EVENT_HASH']==prev,'lesson chain');must(hashlib.sha256(json.dumps({k:v for k,v in e.items() if k!='EVENT_HASH'},sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()).hexdigest()==e['EVENT_HASH'],'lesson hash');prev=e['EVENT_HASH']
must(prev==auth['LL11_HEAD'],'LL11 preserved');must(sha(B/'campaign-budget.jsonl')==auth['STOPPED_JOURNAL_SHA256'],'journal')
graph=read(O/'dependency-graph.json');must(cycle_free(graph['EDGES']),'acyclic design')
s={'budget_method':'maximum encoded sizes and feasible branches; incomplete where bounds absent','producer_coverage':'includes ledger,preparation,inherited stderr,watchdog','overwrites_count':True,'deleted_writes_refund':False,'max_children':2,'critical_reserve_required':True,'normal_can_use_reserve':False,'failure_dropped_ok':False,'whole_tree_claim':False,'escaped_descendants_ok':False,'watchdog_failure_success':False,'unknown_exit_completion':False,'host_verified':False,'graph':graph['EDGES'],'ceiling':1048576,'source_modification':False,'active_execution':False}
def valid(x):
 must(x['budget_method']==s['budget_method'],'average size');must(x['producer_coverage']==s['producer_coverage'],'missing producer');must(x['overwrites_count'],'overwrite bypass');must(not x['deleted_writes_refund'],'deletion bypass');must(x['max_children']==2,'concurrency ceiling');must(x['critical_reserve_required'],'reserve missing');must(not x['normal_can_use_reserve'],'reserve stolen');must(not x['failure_dropped_ok'],'failure dropped');must(not x['whole_tree_claim'],'parent timeout promoted');must(not x['escaped_descendants_ok'],'escaped descendant ignored');must(not x['watchdog_failure_success'],'watchdog failure success');must(not x['unknown_exit_completion'],'unknown completion');must(not x['host_verified'],'unqualified host promoted');must(cycle_free(x['graph']),'cycle');must(x['ceiling']==1048576,'ceiling increased');must(not x['source_modification'],'source modification');must(not x['active_execution'],'active execution')
valid(s)
changes=[('average-size budgeting','budget_method','average'),('missing producer','producer_coverage','helper streams only'),('overwrite bypass','overwrites_count',False),('deleted-file bypass','deleted_writes_refund',True),('unbounded concurrency','max_children',3),('critical reserve omitted','critical_reserve_required',False),('ordinary steals reserve','normal_can_use_reserve',True),('failure evidence dropped','failure_dropped_ok',True),('parent timeout whole-tree claim','whole_tree_claim',True),('escaped descendant ignored','escaped_descendants_ok',True),('watchdog failure success','watchdog_failure_success',True),('unknown exit completion','unknown_exit_completion',True),('unqualified host promoted','host_verified',True),('circular dependency','graph',graph['EDGES']+[{'from':'INDEPENDENT_ACCOUNTING_TRUST_ROOT','to':'BOOTSTRAP_INERT_TESTS'}]),('ceiling increased','ceiling',1048577),('unauthorized source','source_modification',True),('active test/probe','active_execution',True)]
neg=[]
for name,k,v in changes:
 x=copy.deepcopy(s);x[k]=v
 try:valid(x)
 except ValueError as e:neg.append({'CONTROL':name,'RESULT':'REJECTED','CAUSE':str(e)})
 else:raise ValueError('accepted negative:'+name)
reconstruction={'SOURCES':auth['SOURCE_IDENTITIES'],'LIMITS':limits,'RECORDS':len(records),'NORMATIVE_RECORD_BYTES':sum(map(len,records.values())),'EPOCHS':len(epochs),'EPOCH_BYTES':sum(map(len,epochs.values())),'FIXED_BYTES':928340,'REMAINING_BYTES':120236,'CANDIDATE_ENVELOPE_BYTES':393216,'CANDIDATE_DEFICIT_BYTES':272980,'CRITICAL_RESERVE_BYTES':None,'COMPLETE_BUDGET':False,'WATCHDOG_QUALIFIED':False,'DECISION_READY':False,'GRAPH_ACYCLIC':True,'LL11_HEAD':prev,'SOURCE_OBSERVATIONS':['critical writes blocked after stopped/deadline','failure serialization cap does not bound raw exception evidence','helpers start distinct sessions','short-write suffix submitted again'],'CONTRACT_PINS':{p.name:sha(p) for p in O.glob('*.json') if p.name not in ['preservation-before.json','independent-static-verification.json','four-seed-reconstruction.json','negative-control-results.json','preservation-audit.json','report.json','evidence-index.json','governance-authentication.json']},'NEGATIVES':neg,'ASSURANCE':'static contract mutations and AST/JSON reconstruction only; no behavioral or OS qualification'}
print(json.dumps({'HASH_SEED':os.environ.get('PYTHONHASHSEED'),'RECONSTRUCTION':reconstruction,'SEMANTIC_SHA256':hashlib.sha256(enc(reconstruction)).hexdigest()},sort_keys=True))
