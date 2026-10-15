"""Read-only AST/JSON reconstruction. Never imports bridge or test modules."""
import ast,copy,hashlib,json,pathlib,os
O=pathlib.Path(__file__).resolve().parent;R=O.parents[4];B=O.parent
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def enc(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
a=read(O/'authenticated-resource-baseline.json')
for p,h in a['PINS'].items():assert sha(R/p)==h
for p,h in a['SOURCE_PINS'].items():assert sha(R/p)==h;ast.parse((R/p).read_text())
assert a['NORMAL_PATH_WRITE_BOUND']==111665 and a['CRITICAL_RESERVE_BYTES']==32694 and a['TOTAL_PROTECTED_WRITE_ALLOCATION']==111665+32694
f=read(B/'fixed-command-bridge-102/logical-synthetic-identity-manifest.json')
assert len(f['CONTENT']['FIXTURES'])==12 and sum(len(enc(x)) for x in f['CONTENT']['FIXTURES'])==36710 and len(enc(f))==37056
p=read(O/'host-interpreter-inventory.json');assert sha(pathlib.Path(p['RESOLVED_EXECUTABLE']))==p['PYTHON_EXECUTABLE_SHA256']
t=read(O/'fixed-inert-topology.json');assert t['MAX_LIVE_APPLICATION_PROCESSES']==4 and t['MAX_CHILD_LAUNCHES']==5 and t['MAX_PROCESS_LIFETIMES']==6
edges=read(O/'qualification-dependency-graph.json')['EDGES'];d={}
for x,y in edges:d.setdefault(x,[]).append(y)
def visit(n,active):
 assert n not in active
 for w in d.get(n,[]):visit(w,active|{n})
for n in d:visit(n,set())
state={'interpreter':p['PYTHON_EXECUTABLE_SHA256'],'direct_host_permission':False,'cpu_from_bytes':False,'rss_enforced_by_rlimit_rss':False,'parent_timeout_whole_tree':False,'untracked_descendant_ignored':False,'fd_from_file_count':False,'observer_accounted':True,'proposed_is_verified':False,'calibration_safety_qualified':False,'authority_needs_own_output':False,'unissued_effective':False,'real_systemd_sudo_bwrap':False,'h77_a15':False,'calibration_active':False}
checks=[('wrong interpreter','interpreter',lambda v:v==p['PYTHON_EXECUTABLE_SHA256'],'wrong'),('Codex permissions promoted','direct_host_permission',lambda v:not v,True),('CPU inferred from fixture bytes','cpu_from_bytes',lambda v:not v,True),('RSS rlimit enforcement','rss_enforced_by_rlimit_rss',lambda v:not v,True),('parent-only watchdog','parent_timeout_whole_tree',lambda v:not v,True),('unknown descendant ignored','untracked_descendant_ignored',lambda v:not v,True),('FD from source count','fd_from_file_count',lambda v:not v,True),('observer budget omitted','observer_accounted',bool,False),('proposed ceiling verified','proposed_is_verified',lambda v:not v,True),('unqualified calibration safety','calibration_safety_qualified',lambda v:not v,True),('self-dependent authority','authority_needs_own_output',lambda v:not v,True),('unissued effective','unissued_effective',lambda v:not v,True),('real forbidden operation','real_systemd_sudo_bwrap',lambda v:not v,True),('H77/A15 included','h77_a15',lambda v:not v,True),('premature activation','calibration_active',lambda v:not v,True)]
def valid(s):
 for name,k,pred,bad in checks:
  if not pred(s[k]):raise ValueError(name)
valid(state);negative=[]
for name,k,pred,bad in checks:
 s=copy.deepcopy(state);s[k]=bad
 try:valid(s)
 except ValueError as e:negative.append({'CONTROL':name,'RESULT':'REJECTED','REASON':str(e)})
 else:raise AssertionError(name)
contracts={q.name:sha(q) for q in sorted(O.glob('*.json')) if q.name in ['authenticated-resource-baseline.json','host-interpreter-inventory.json','fixed-inert-topology.json','resource-ownership-matrix.json','resource-requirement-assessments.json','independent-observer-profile.json','minimal-calibration-specification.json','qualification-dependency-graph.json','remaining-gap-dossier.json']}
semantic={'CONTRACT_PINS':contracts,'WRITE_ALLOCATION':144359,'CRITICAL_RESERVE':32694,'MAX_LIVE_PROCESSES_PROPOSED':4,'CALIBRATION_DECISION_READY':False,'CALIBRATION_EXECUTION_READY':False,'GRAPH_ACYCLIC':True,'NEGATIVES':negative}
print(json.dumps({'HASH_SEED':os.environ.get('PYTHONHASHSEED'),'RECONSTRUCTION':semantic,'SEMANTIC_SHA256':hashlib.sha256(enc(semantic)).hexdigest()},sort_keys=True))
