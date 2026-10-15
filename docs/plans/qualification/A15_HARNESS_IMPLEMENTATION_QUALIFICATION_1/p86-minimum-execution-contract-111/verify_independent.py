"""111 independent JSON/AST verification; never imports or executes payload."""
import pathlib,json,hashlib,ast,copy,os
O=pathlib.Path(__file__).resolve().parent;R=O.parents[4]
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def enc(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
a=read(O/'entry-authentication.json')
for p,h in a['PINS'].items():assert sha(R/p)==h
c=read(O/'exact-package86-command-authentication.json');s=read(O.parent/'system-process-enforcement-86/transient-service-specification.json');argv=c['COMMAND_ARGUMENT_VECTOR'];assert argv==s['EXACT_COMMAND_ARGV'];assert hashlib.sha256(enc(argv)).hexdigest()==c['COMMAND_CONTENT_IDENTITY']['sha256']=='e628c8664ea72357963dc58dddee934c28cad3ab5c84450656a6595e6910fb50'
assert hashlib.sha256(argv[-1].encode()).hexdigest()==c['PAYLOAD_RAW_SHA256'];assert argv[-1]==(O.parent/'system-process-enforcement-86/prospective-payload.txt').read_text();tree=ast.parse(argv[-1])
assert not any(x.startswith('--property=CPUQuota') for x in argv) and c['RESOURCE_LIMITS']==s['LIMITS'] and c['UNCHANGED']
# Reconstruct source emit bound: two snapshot calls, one error-handler emit, fixed record guard.
emit=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='emit')
assert 8192 in [x.value for x in ast.walk(emit) if isinstance(x,ast.Constant)]
tr=next(x for x in tree.body if isinstance(x,ast.Try));snap=sum(isinstance(x,ast.Call) and isinstance(x.func,ast.Name) and x.func.id=='snapshot' for x in ast.walk(ast.Module(body=tr.body,type_ignores=[])))
err=sum(isinstance(x,ast.Call) and isinstance(x.func,ast.Name) and x.func.id=='emit' for h in tr.handlers for x in ast.walk(h));assert snap==2 and err==1
w=read(O/'publication-budget-analysis.json');assert w['SOURCE_PAYLOAD_MAX_EMIT_CALLS']==snap+err and w['SOURCE_PAYLOAD_ENCODED_RECORD_BOUND_BYTES']==(snap+err)*8192 and not w['PUBLICATION_BUDGET_COMPLETE'] and w['CRITICAL_FAILURE_RESERVE_BYTES'] is None
k=read(O/'consumption-identity-specification.json');assert 'execution_context_identity' in k['SCHEMA_FIELDS'] and 'retained_package86_subject_identity' in k['SCHEMA_FIELDS'] and k['FIXED_BINDINGS']['attempt_number']==1 and k['ACTUAL_REAL_KEY'] is None
assert 'grant-' in k['STORE_KEY'] and 'sha256' in k['FIXED_BINDINGS']['exact_command_identity']
store=read(O/'durable-consumption-store-specification.json');assert not store['STORE_CREATED'] and store['STORE_OWNER'] is None and not store['COMPLETE']
assert not read(O/'launcher-qualification-assessment.json')['QUALIFIED_LAUNCHER_AVAILABLE']
assert read(O/'observer-resource-model.json')['MAX_OBSERVER_WALL_SECONDS']==25 and not read(O/'observer-resource-model.json')['COMPLETE']
g=read(O/'qualification-dependency-graph.json');d={}
for x,y in g['EDGES']:d.setdefault(x,[]).append(y)
def visit(n,active):
 assert n not in active
 for w in d.get(n,[]):visit(w,active|{n})
for n in d:visit(n,set())
reg=read(R/'docs/plans/PLANNER_REASONING_LESSONS_REGISTER_1.json');prev='0'*64
for e in reg['EVENTS']:
 assert e['PREVIOUS_EVENT_HASH']==prev
 assert hashlib.sha256(json.dumps({k:v for k,v in e.items() if k!='EVENT_HASH'},sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()).hexdigest()==e['EVENT_HASH'];prev=e['EVENT_HASH']
assert prev=='885fd0eaceb15847201dfd058217682741fb43c255298713ccbc1e7251eec791';assert sha(O.parent/'campaign-budget.jsonl')=='3491e9003e1a016dbc4208e3963f8abea0f98c439dc892aa89a3811e73d528eb'
state={'command':c['COMMAND_CONTENT_IDENTITY']['sha256'],'duplicate_launch':False,'reusable_claim':False,'unqualified_launcher':False,'self_report_only_observer':False,'missing_observer_limit_accepted':False,'unbounded_stderr':False,'missing_reserve_accepted':False,'unknown_success':False,'cpu_quota_added':False,'memory_exhaustion':False,'attestation_as_sudo':False,'circular_dependency':False,'premature_real_authority':False,'h77_a15':False}
def valid(x):
 if x['command']!=c['COMMAND_CONTENT_IDENTITY']['sha256']:raise ValueError('wrong_command')
 for k,v in x.items():
  if k!='command' and v:raise ValueError(k)
valid(state);neg=[]
for k in state:
 x=copy.deepcopy(state);x[k]='wrong' if k=='command' else True
 try:valid(x)
 except ValueError as e:neg.append({'CONTROL':k,'RESULT':'REJECTED','CAUSE':str(e)})
 else:raise AssertionError(k)
names=['entry-authentication.json','exact-package86-command-authentication.json','consumption-identity-specification.json','durable-consumption-store-specification.json','grant-one-attempt-and-claim-to-launch-contract.json','launcher-qualification-assessment.json','independent-observer-specification.json','observer-resource-model.json','evidence-publication-inventory.json','publication-budget-analysis.json','critical-failure-evidence-contract.json','service-termination-and-administrative-entry.json','minimal-missing-implementation-assessment.json','qualification-dependency-graph.json','remaining-gap-dossier.json']
s={'PINS':{n:sha(O/n) for n in names},'ORIGINAL_COMMAND_IDENTITY':c['COMMAND_CONTENT_IDENTITY'],'GRAPH_ACYCLIC':True,'LL11_HEAD':prev,'PROBE_VERIFICATION_DECISION_READY':False,'QUALIFIED_LAUNCHER_AVAILABLE':False,'NEGATIVES':neg}
print(json.dumps({'HASH_SEED':os.environ.get('PYTHONHASHSEED'),'RECONSTRUCTION':s,'SEMANTIC_SHA256':hashlib.sha256(enc(s)).hexdigest()},sort_keys=True))
