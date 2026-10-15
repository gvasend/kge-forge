"""Static documentary verification. No target-source imports or capability checks."""
import json,pathlib,hashlib,os,sys,subprocess,copy
O=pathlib.Path(__file__).resolve().parent
B=pathlib.Path('docs/plans/qualification/A15_HARNESS_IMPLEMENTATION_QUALIFICATION_1')
P=B/'p86-risk-adaptive-construction-120'
def read(p):return json.loads(p.read_text())
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def sha(x):return hashlib.sha256(x).hexdigest()
def need(x,s):
 if not x:raise ValueError(s)
def acyclic(edges):
 active=set();done=set();adj={}
 for a,b in edges:adj.setdefault(a,[]).append(b)
 def walk(n):
  need(n not in active,'graph cycle')
  if n in done:return
  active.add(n)
  for v in adj.get(n,[]):walk(v)
  active.remove(n);done.add(n)
 for n in adj:walk(n)
 return True
manifest=read(O/'authenticated-input-index.json')
for p,h in manifest['PINS'].items():need(sha(pathlib.Path(p).read_bytes())==h,'input pin '+p)
for p,h in read(O/'preservation-before.json')['FILES'].items():need(sha(pathlib.Path(p).read_bytes())==h,'prior-file preservation '+p)
policy=read(P/'proposed-policy-allocation.json');paths=read(P/'two-file-scope.json')['EXACT_PATHS']
need(sha(canon(policy))==manifest['PACKAGE120_POLICY_IDENTITY']['sha256'],'policy canonical pin')
need(sha(canon(policy))=='0405a4b19e4b2634f28a9463ef5f3238b3c904d251096427ac4b8ed776613cec','exact120 allocation')
need(all(not pathlib.Path(p).exists() for p in paths),'no construction')
source102=read(B/'fixed-command-bridge-102/source-authority-boundary.json')
need(all(p in json.dumps(source102) for p in paths),'102 paths recovered')
rawphase=read(P/'36-row-phase-matrix.json')['REQUIREMENTS'];audit=read(O/'36-requirement-phase-audit.json')['ROWS']
need(len(audit)==len(rawphase)==36,'36 phases')
for r,a in zip(rawphase,audit):
 need(a['REQUIREMENT_ID']==r['REQUIREMENT_ID'] and a['BINDING_AUTHORITY']==r['AUTHORITY_SOURCE'] and a['EXACT_CLAUSE']==r['EXACT_CLAUSE'] and a['PHASE']==r['RETAINED_EARLIEST_PHASE'] and a['CLASS']==r['CLASS'],'phase provenance')
units=read(O/'six-work-unit-allocation.json');need(units['P120_EXACT_POLICY']==read(P/'work-unit-checkpoint-policy.json'),'six units exact')
need([u['UNIT'] for u in units['P120_EXACT_POLICY']['UNITS']]==['RECOVERY','INTERFACE_DESIGN','LAUNCHER_SOURCE','OBSERVER_TEST_SOURCE','STATIC_VERIFICATION','REPORT_SEAL'],'six stage names')
need(units['MAX_OCCURRENCES']==12 and units['CURRENT_STAGE_EXECUTION']=='NOT_STARTED','revision counting')
limits=read(O/'limit-enforcement-matrix.json')['LIMITS'];expected={k:v for k,v in policy.items() if isinstance(v,int) and not isinstance(v,bool) and k!='REAL_PROBE_PUBLICATION_CEILING'}
for f in policy['FILES']:
 for k in ['MAX_RETAINED_SOURCE_BYTES','MAX_FULL_SOURCE_PUBLICATIONS','MAX_MANUAL_RECOVERABLE_REVISIONS','MAX_CUMULATIVE_LOGICAL_SOURCE_BYTES']:expected[f['PATH']+'::'+k]=f[k]
need({r['LIMIT_ID']:r['NUMERIC_VALUE'] for r in limits}==expected,'all limit classes and exact values')
obs=read(O/'codex-context-read-only-observations.json');codexpin=obs['namespace_init']
if 'RAW_SHA256' in codexpin:need(sha(pathlib.Path(codexpin['EXECUTABLE']).read_bytes())==codexpin['RAW_SHA256'],'observed Codex binary pin')
# Existing bootstrap AST checks are read-only; no module import or execution.
import ast
for p in ['adapter/qualification_bootstrap/systemd_pids_once.py','adapter/tests/test_systemd_pids_bootstrap.py']:ast.parse(pathlib.Path(p).read_text())
# Fresh current normative readers, not payload/system-manager commands.
cp=subprocess.run([sys.executable,str(B/'p86-publication-amendment-issuance-115/verify_independent.py'),'EFFECTIVE'],capture_output=True,text=True)
need(cp.returncode==0,'current charter/104/115/A15 effective readers');json.loads(cp.stdout)
commandpin=manifest['PINS'][str(B/'system-process-enforcement-86/prospective-payload.txt')]
model={'paths':paths,'policy':policy,'limits':limits,'supervisor_pin':codexpin,'qualified_supervisor':False,'claims_verified':False,'control_statuses':[r['STATUS'] for r in limits],'authority':read(O/'authority-separation.json'),'edges':read(O/'dependency-graph.json')['EDGES'],'writable_history':False,'actual_session_workspace_writable':True,'history_preserved':True,'unauthorized_subprocess':False,'construction_sufficiency_proved':False,'retry_reset':False,'future_probe_required':False,'real_launch_enabled':False,'command_pin':commandpin,'recipe_complete':False,'observer_bound':False}
def validate(m):
 need(m['paths']==paths,'wrong source path')
 need(m['policy']==policy,'changed/arbitrary policy ceiling')
 need({r['LIMIT_ID']:r['NUMERIC_VALUE'] for r in m['limits']}==expected,'resource class/value')
 need(m['supervisor_pin']==codexpin,'forged supervisor pin')
 need(not m['qualified_supervisor'] and not m['claims_verified'] and not m['recipe_complete'] and not m['observer_bound'],'unverified control not qualified')
 need(all(s=='UNDETERMINED_ENFORCEMENT' for s in m['control_statuses']),'unverified limit')
 need(m['authority']['DECISION_OPTIONS']==[] and not m['authority']['CONSTRUCTION_DECISION_READY'] and not m['authority']['SOURCE_CONSTRUCTION_AUTHORITY'] and not m['authority']['INERT_TEST_AUTHORITY'] and not m['authority']['REAL_PROBE_AUTHORITY'],'no inferred authority/selectable incomplete subject')
 need(not m['writable_history'] and m['actual_session_workspace_writable'],'required protected boundary vs actual workspace boundary')
 need(m['history_preserved'],'historical hash')
 need(not m['unauthorized_subprocess'],'subprocess scope')
 need(not m['construction_sufficiency_proved'],'allocation not sufficiency proof')
 need(not m['retry_reset'],'no silent restart')
 need(not m['future_probe_required'],'no future output prerequisite')
 need(not m['real_launch_enabled'],'real launch disabled')
 need(m['command_pin']==commandpin,'command unchanged')
 acyclic(m['edges'])
validate(model)
neg=[]
def reject(name,mut):
 m=copy.deepcopy(model);mut(m)
 try:validate(m)
 except ValueError as e:neg.append({'DESIGN':name,'OUTCOME':'REJECTED','CAUSE':str(e)});return
 raise AssertionError('negative accepted: '+name)
def mm(k,v):return lambda m:m.__setitem__(k,v)
def aa(k,v):return lambda m:m['authority'].__setitem__(k,v)
reject('wrong source path',lambda m:m['paths'].append('adapter/planner/core.py'))
reject('changed Package86 command',mm('command_pin','0'*64))
reject('forged Codex supervisor pin',lambda m:m['supervisor_pin'].__setitem__('RAW_SHA256','0'*64))
reject('observed binary treated as qualified supervisor',mm('qualified_supervisor',True))
reject('claimed unverified resource control',mm('claims_verified',True))
reject('arbitrary CPU ceiling',lambda m:m['policy'].__setitem__('MAX_AGGREGATE_CPU_SECONDS',99999))
reject('arbitrary memory ceiling',lambda m:m['policy'].__setitem__('MAX_AGGREGATE_MEMORY_BYTES',99999))
reject('omitted resource class',lambda m:m['limits'].pop())
reject('limit falsely independently verified',lambda m:m['control_statuses'].__setitem__(0,'INDEPENDENTLY_VERIFIED'))
reject('unauthorized subprocess',mm('unauthorized_subprocess',True))
reject('writable prior evidence accepted in approved recipe',mm('writable_history',True))
reject('workspace-wide access called exact confinement',mm('actual_session_workspace_writable',False))
reject('source sufficiency proof asserted',mm('construction_sufficiency_proved',True))
reject('silent retry reset',mm('retry_reset',True))
reject('grant inferred from dossier',aa('SOURCE_CONSTRUCTION_AUTHORITY',True))
reject('construction treated as inert authority',aa('INERT_TEST_AUTHORITY',True))
reject('construction treated as real authority',aa('REAL_PROBE_AUTHORITY',True))
reject('future probe output demanded',mm('future_probe_required',True))
reject('real launch enabled',mm('real_launch_enabled',True))
reject('history modified',mm('history_preserved',False))
reject('incomplete recipe accepted',mm('recipe_complete',True))
reject('unbound observer qualified',mm('observer_bound',True))
reject('incomplete decision made ready',aa('CONSTRUCTION_DECISION_READY',True))
reject('construction depends on own result',lambda m:m['edges'].append(['CONSTRUCTION_OUTPUT','CONSTRUCTION_DECISION']))
semantic={'INPUT_PIN_SET_SHA256':sha(canon(manifest['PINS'])),'P120_POLICY_IDENTITY':manifest['PACKAGE120_POLICY_IDENTITY'],'SOURCE_PATHS':paths,'PHASE_ROWS':36,'PHASE_AUDIT_SHA256':sha(canon(audit)),'LIMITS':expected,'SUPERVISOR_SELECTED':'NONE','OBSERVED_CODEX_BINARY_PIN':codexpin,'QUALIFIED_CONTROL':False,'DECISION_READY':False,'ENTRY_READY':False,'GRAPH_ACYCLIC':True,'PRIOR_PRESERVATION':'PASS','NEGATIVES':neg}
print(json.dumps({'HASH_SEED':os.environ.get('PYTHONHASHSEED'),'RECONSTRUCTION':semantic,'SEMANTIC_SHA256':sha(canon(semantic))},sort_keys=True))
