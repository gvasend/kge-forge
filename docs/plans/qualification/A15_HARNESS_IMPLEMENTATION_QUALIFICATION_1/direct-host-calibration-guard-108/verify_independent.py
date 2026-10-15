"""Static JSON/hash verification only; no namespace or workload execution."""
import pathlib,json,hashlib,copy,os
O=pathlib.Path(__file__).resolve().parent;R=O.parents[4]
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def enc(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
a=read(O/'entry-authentication.json')
for p,h in a['PINS'].items():assert sha(R/p)==h
m=read(O/'retained-workload-model.json')['MODEL'];assert m['INERT_CASES']==12 and m['MAX_CONCURRENT_APPLICATION_PROCESSES']==4 and m['TOTAL_PROCESS_LIFETIMES']==6 and m['CHILD_LAUNCHES']==5
assert m['NORMAL_PATH_WRITE_BOUND']==111665 and m['MAX_MODELED_FAILURE_PATH']==129825 and m['PROTECTED_CRITICAL_RESERVE']==32694 and m['TOTAL_PROTECTED_WRITE_ALLOCATION']==144359
h=read(O/'direct-host-evidence-manifest.json');assert h['AUTHENTICATED_AS_OWNER_PROVIDED_CONTENT'] and not h['INDEPENDENT_HOST_REPRODUCTION'] and not h['DIRECT_HOST_PROFILE_AUTHENTICATED']
assert h['OBSERVATIONS']['NOFILE_SOFT']==1024 and h['OBSERVATIONS']['USER_SLICE_DELEGATE']=='no'
n=read(O/'namespace-mount-contract.json');assert n['FULL_ARGUMENT_VECTOR'] is None and '--unshare-pid' in n['EXACT_OPTION_PREFIX'] and '--as-pid-1' not in n['EXACT_OPTION_PREFIX']
assert all(x['PROPOSED_VALUE'] is None for x in read(O/'posix-resource-limit-contract.json')['LIMITS'])
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
assert prev=='885fd0eaceb15847201dfd058217682741fb43c255298713ccbc1e7251eec791'
assert sha(O.parent/'campaign-budget.jsonl')=='3491e9003e1a016dbc4208e3963f8abea0f98c439dc892aa89a3811e73d528eb'
fields=['codex_as_direct','unlimited_as_finite','pid_namespace_as_count','cpu_per_process_as_aggregate','as_as_aggregate_rss','fsize_as_cumulative','parent_only_as_whole_tree','observer_unverified_as_qualified','unbounded_safety_accepted','real_systemd','circular_dependency','premature_activation','h77_a15']
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
names=['entry-authentication.json','direct-host-evidence-manifest.json','retained-workload-model.json','namespace-mount-contract.json','posix-resource-limit-contract.json','whole-workload-containment-specification.json','independent-watchdog-specification.json','process-count-write-enforcement-assessment.json','observer-contract.json','minimal-capability-check-specification.json','authority-applicability-assessment.json','remaining-gap-dossier.json','qualification-dependency-graph.json']
s={'PINS':{n:sha(O/n) for n in names},'MODEL':m,'GRAPH_ACYCLIC':True,'LL11_HEAD':prev,'CAPABILITY_VERIFICATION_DECISION_READY':False,'NEGATIVES':neg}
print(json.dumps({'HASH_SEED':os.environ.get('PYTHONHASHSEED'),'RECONSTRUCTION':s,'SEMANTIC_SHA256':hashlib.sha256(enc(s)).hexdigest()},sort_keys=True))
