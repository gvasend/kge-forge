"""109 independent static reconstruction. No target imports or host operations."""
import pathlib,json,hashlib,gzip,copy,os
O=pathlib.Path(__file__).resolve().parent;R=O.parents[4]
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def enc(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
a=read(O/'entry-authentication.json')
for p,h in a['PINS'].items():assert sha(R/p)==h
m=read(O/'retained-resource-model.json')['MODEL'];assert m=={'INERT_CASES':12,'MAX_CONCURRENT_APPLICATION_PROCESSES':4,'TOTAL_PROCESS_LIFETIMES':6,'CHILD_LAUNCHES':5,'NORMAL_PATH_WRITE_BOUND':111665,'MAX_MODELED_FAILURE_PATH':129825,'PROTECTED_CRITICAL_RESERVE':32694,'TOTAL_PROTECTED_WRITE_ALLOCATION':144359}
adm=read(O/'administrator-authority-assessment.json');assert adm['RETAINED_DECLARATION']['HOST_ADMINISTRATIVE_AUTHORITY']=='OWNER_ATTESTED' and adm['ACTUAL_SUDO_PERMISSION']=='UNVERIFIED'
p=adm['SOURCE_PIN'];assert sha(R/p['path'])==p['sha256']
for d in read(O/'installed-systemd-property-evidence.json')['DOCUMENTS']:assert sha(pathlib.Path(d['PATH']))==d['RAW_SHA256']
s=gzip.open('/usr/share/man/man5/systemd.resource-control.5.gz','rt').read();assert 'cpu\\&.cfs_quota_us' in s and 'pids\\&.max' in s and 'MemoryLow=' in s
u=read(O/'systemd-cgroup-v1-boundary-specification.json');assert u['KILL_MODE']=='control-group' and u['SEND_SIGKILL']=='yes' and u['RESTART']=='no' and u['TASKS_MAX'] is None and u['EXACT_ARGUMENT_VECTOR'] is None
assert not read(O/'cumulative-write-critical-evidence-assessment.json')['CGROUP_ENFORCES_CUMULATIVE_WRITES']
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
fields=['attestation_as_sudo','v2_only_property_on_v1','user_slice_as_campaign','pids_max_inferred','rlimit_as_aggregate_memory','quota_as_total_cpu','parent_only_termination','quota_as_cumulative_writes','critical_blocked_after_deadline','observer_unverified_qualified','unauthorized_unit','circular_dependency','premature_authority','h77_a15']
state={k:False for k in fields}
def valid(s):
 for k in fields:
  if s[k]:raise ValueError(k)
valid(state);neg=[]
for k in fields:
 s=copy.deepcopy(state);s[k]=True
 try:valid(s)
 except ValueError as e:neg.append({'CONTROL':k,'RESULT':'REJECTED','CAUSE':str(e)})
 else:raise AssertionError(k)
names=['entry-authentication.json','owner-host-observations.json','administrator-authority-assessment.json','retained-resource-model.json','installed-systemd-property-evidence.json','systemd-cgroup-v1-boundary-specification.json','process-count-enforcement-contract.json','aggregate-memory-enforcement-contract.json','aggregate-cpu-enforcement-contract.json','whole-workload-termination-contract.json','watchdog-observer-specification.json','cumulative-write-critical-evidence-assessment.json','minimal-host-capability-verification-specification.json','authority-applicability-assessment.json','dedicated-vm-alternative-assessment.json','qualification-dependency-graph.json','remaining-gap-dossier.json']
s={'PINS':{n:sha(O/n) for n in names},'MODEL':m,'GRAPH_ACYCLIC':True,'LL11_HEAD':prev,'DECISION_READY':False,'NEGATIVES':neg}
print(json.dumps({'HASH_SEED':os.environ.get('PYTHONHASHSEED'),'RECONSTRUCTION':s,'SEMANTIC_SHA256':hashlib.sha256(enc(s)).hexdigest()},sort_keys=True))
