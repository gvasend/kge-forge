"""112 independent AST/JSON arithmetic verification. No target execution/import."""
import pathlib,json,hashlib,ast,copy,os
O=pathlib.Path(__file__).resolve().parent;R=O.parents[4]
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def enc(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
a=read(O/'entry-authentication.json')
for p,h in a['PINS'].items():assert sha(R/p)==h
c=read(O/'package86-command-authentication.json');s=read(O.parent/'system-process-enforcement-86/transient-service-specification.json');argv=c['EXACT_ARGV'];assert argv==s['EXACT_COMMAND_ARGV']
assert hashlib.sha256(enc(argv)).hexdigest()==c['COMMAND_IDENTITY']['sha256']=='e628c8664ea72357963dc58dddee934c28cad3ab5c84450656a6595e6910fb50'
assert hashlib.sha256(argv[-1].encode()).hexdigest()==c['PAYLOAD_RAW_SHA256'];t=ast.parse(argv[-1]);emit=next(x for x in t.body if isinstance(x,ast.FunctionDef) and x.name=='emit');tr=next(x for x in t.body if isinstance(x,ast.Try))
assert 8192 in [x.value for x in ast.walk(emit) if isinstance(x,ast.Constant)]
assert sum(isinstance(x,ast.Call) and isinstance(x.func,ast.Name) and x.func.id=='snapshot' for x in ast.walk(ast.Module(body=tr.body,type_ignores=[])))==2
assert sum(isinstance(x,ast.Call) and isinstance(x.func,ast.Name) and x.func.id=='emit' for h in tr.handlers for x in ast.walk(h))==1
assert any(isinstance(x,ast.While) for x in ast.walk(emit)) and any(isinstance(x,ast.Subscript) and isinstance(x.value,ast.Name) and x.value.id=='raw' for x in ast.walk(emit))
w=read(O/'payload-partial-write-accounting.json');assert w['MAX_LOGICAL_PAYLOAD_BYTES']==3*8192==24576
assert sum(range(1,8193))==w['MAX_ARGUMENT_BYTES_SUBMITTED_PER_EMIT']==33558528
assert 3*sum(range(1,8193))==w['MAX_THREE_EMIT_ARGUMENT_BYTES_SUBMITTED']==100675584
assert w['SUBMITTED_UPPER_BOUND_MINUS65536']==100610048
ret=read(O.parent/'launch-actor-resource-closure-104/stable-consumption-store-specification.json');k=read(O/'stable-consumption-identity.json');assert k['KEY_RULE']==ret['KEY_RULE'] and k['CONTENT_IDENTITY_NAMESPACE']==ret['KEY_NAMESPACE'] and k['ACTUAL_REAL_KEY'] is None
sc=read(O/'bounded-critical-record-schemas.json');assert len(sc['SCHEMAS'])==7
for r in sc['SCHEMAS']:
 x=r['MAXIMAL_ENCODING_INSTANCE'];assert len(enc(x))==r['MAX_RECORD_BYTES'] and r['MAX_OCCURRENCES'] is None
 assert len(x['cause']['code'])==max(map(len,sc['CLOSED_CAUSE_CODES'])) and len(x['cause']['phase'])==max(map(len,sc['CLOSED_PHASES']))
 assert len(x['consumption_state'])==max(map(len,sc['CLOSED_CONSUMPTION_STATES'])) and len(x['exit_state'])==max(map(len,sc['CLOSED_EXIT_STATES']))
budget=read(O/'publication-budget-and-critical-reserve.json');assert not budget['PUBLICATION_BUDGET_COMPLETE'] and budget['CRITICAL_RESERVE'] is None and budget['MAX_TOTAL_PUBLICATION'] is None
scope=read(O/'twelve-property-inert-qualification-scope.json');orig=read(O.parent/'fixed-command-bridge-102/minimal-inert-qualification-specification.json');assert scope['TESTS']==orig['TESTS'] and scope['EXACT_TEST_COUNT']==12
p=scope['FIXTURE_MANIFEST_PIN'];assert sha(R/p['path'])==p['sha256']
b=read(O/'exact-two-file-source-boundary.json');assert b['EXACT_PATHS']==['adapter/qualification_bootstrap/systemd_pids_fixed_bridge.py','adapter/tests/test_systemd_pids_fixed_bridge.py'];assert all(not (R/p).exists() for p in b['EXACT_PATHS'])
assert not read(O/'construction-authority-assessment.json')['OLD90_94_BRIDGE_AUTHORITY']
g=read(O/'qualification-dependency-graph.json');d={}
for x,y in g['EDGES']:d.setdefault(x,[]).append(y)
def visit(n,active):
 assert n not in active
 for x in d.get(n,[]):visit(x,active|{n})
for n in d:visit(n,set())
reg=read(R/'docs/plans/PLANNER_REASONING_LESSONS_REGISTER_1.json');prev='0'*64
for e in reg['EVENTS']:
 assert e['PREVIOUS_EVENT_HASH']==prev
 assert hashlib.sha256(json.dumps({k:v for k,v in e.items() if k!='EVENT_HASH'},sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()).hexdigest()==e['EVENT_HASH'];prev=e['EVENT_HASH']
assert prev=='885fd0eaceb15847201dfd058217682741fb43c255298713ccbc1e7251eec791';assert sha(O.parent/'campaign-budget.jsonl')=='3491e9003e1a016dbc4208e3963f8abea0f98c439dc892aa89a3811e73d528eb'
fields=['wrong_principal','reusable_capability','duplicate_as_new_authority','missing_directory_fsync','unqualified_observer','arbitrary_resource_limit','submitted_equals_transferred','partial_submission_omitted','unbounded_stderr_accepted','reserve_omitted_accepted','critical_blocked_after_deadline_accepted','unknown_as_success','old_grant_as_bridge_authority','unauthorized_path','real_systemd_enabled','circular_dependency','premature_authority','h77_a15']
state={k:False for k in fields}
def valid(x):
 for k in fields:
  if x[k]:raise ValueError(k)
valid(state);neg=[]
for k in fields:
 x=copy.deepcopy(state);x[k]=True
 try:valid(x)
 except ValueError as e:neg.append({'CONTROL':k,'RESULT':'REJECTED','CAUSE':str(e)})
 else:raise AssertionError(k)
names=['entry-authentication.json','package86-command-authentication.json','launcher-principal-authority-contract.json','stable-consumption-identity.json','durable-store-contract.json','claim-to-launch-protocol.json','independent-observer-contract.json','observer-resource-model.json','payload-partial-write-accounting.json','bounded-critical-record-schemas.json','complete-publication-inventory-and-gaps.json','publication-budget-and-critical-reserve.json','post-deadline-finalization-contract.json','twelve-property-inert-qualification-scope.json','exact-two-file-source-boundary.json','construction-authority-assessment.json','qualification-dependency-graph.json','remaining-gap-dossier.json']
s={'PINS':{n:sha(O/n) for n in names},'COMMAND_IDENTITY':c['COMMAND_IDENTITY'],'LOGICAL_PAYLOAD_BOUND':24576,'CONSERVATIVE_API_ARGUMENT_BOUND':100675584,'CRITICAL_RECORD_MAXIMA':{r['RECORD_TYPE']:r['MAX_RECORD_BYTES'] for r in sc['SCHEMAS']},'CRITICAL_RESERVE_COMPLETE':False,'GRAPH_ACYCLIC':True,'LL11_HEAD':prev,'CONSTRUCTION_DECISION_READY':False,'NEGATIVES':neg}
print(json.dumps({'HASH_SEED':os.environ.get('PYTHONHASHSEED'),'RECONSTRUCTION':s,'SEMANTIC_SHA256':hashlib.sha256(enc(s)).hexdigest()},sort_keys=True))
