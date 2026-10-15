"""107 static reconstruction only. No host capability probes or target imports."""
import pathlib,json,hashlib,copy,os
O=pathlib.Path(__file__).resolve().parent;R=O.parents[4]
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def enc(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
a=read(O/'entry-authentication.json')
for p,h in a['PINS'].items():assert sha(R/p)==h
m=a['RETAINED_MODEL'];assert m=={'MAX_CONCURRENT_APPLICATION_PROCESSES':4,'TOTAL_PROCESS_LIFETIMES':6,'CHILD_LAUNCHES':5,'TOTAL_PROTECTED_WRITE_ALLOCATION':144359,'CRITICAL_RESERVE_BYTES':32694}
d=read(O/'direct-host-evidence-assessment.json');assert not d['DIRECT_HOST_PROFILE_COMPLETE']
for key in ['DIRECT_EVIDENCE_PIN','PROFILE_PIN']:
 p=d[key];assert sha(R/p['path'])==p['sha256']
assert not d['RETAINED_USER_SUPPLIED_OBSERVATION']['INDEPENDENT_REPRODUCTION_PERFORMED']
g=read(O/'qualification-dependency-graph.json');adj={}
for x,y in g['EDGES']:adj.setdefault(x,[]).append(y)
def visit(n,active):
 assert n not in active
 for w in adj.get(n,[]):visit(w,active|{n})
for n in adj:visit(n,set())
fields=['sandbox_as_direct','unbounded_as_finite','prlimit_as_verified','parent_group_as_containment','unknown_descendants_ignored','bwrap_as_full_qualification','delegation_assumed','observer_omitted','circular_dependency','calibration_active','h77_a15_active']
state={k:False for k in fields}
def validate(s):
 for k in fields:
  if s[k]:raise ValueError(k)
validate(state);neg=[]
for k in fields:
 s=copy.deepcopy(state);s[k]=True
 try:validate(s)
 except ValueError as e:neg.append({'CONTROL':k,'RESULT':'REJECTED','REASON':str(e)})
 else:raise AssertionError(k)
reg=read(R/'docs/plans/PLANNER_REASONING_LESSONS_REGISTER_1.json');prev='0'*64
for e in reg['EVENTS']:
 assert e['PREVIOUS_EVENT_HASH']==prev
 assert hashlib.sha256(json.dumps({k:v for k,v in e.items() if k!='EVENT_HASH'},sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()).hexdigest()==e['EVENT_HASH'];prev=e['EVENT_HASH']
assert prev=='885fd0eaceb15847201dfd058217682741fb43c255298713ccbc1e7251eec791'
assert sha(O.parent/'campaign-budget.jsonl')=='3491e9003e1a016dbc4208e3963f8abea0f98c439dc892aa89a3811e73d528eb'
names=['entry-authentication.json','direct-host-evidence-assessment.json','readonly-capability-inventory.json','resource-control-assessment.json','watchdog-observer-candidate.json','process-filesystem-network-assessment.json','minimal-guard-and-gap-dossier.json','qualification-dependency-graph.json']
s={'PINS':{n:sha(O/n) for n in names},'MODEL':m,'GRAPH_ACYCLIC':True,'DIRECT_HOST_PROFILE_COMPLETE':False,'CALIBRATION_DECISION_READY':False,'LL11_HEAD':prev,'NEGATIVES':neg}
print(json.dumps({'HASH_SEED':os.environ.get('PYTHONHASHSEED'),'RECONSTRUCTION':s,'SEMANTIC_SHA256':hashlib.sha256(enc(s)).hexdigest()},sort_keys=True))
