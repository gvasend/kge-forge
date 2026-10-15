"""Read-only documentary reconstruction; never imports or runs candidate code."""
import pathlib,json,hashlib,sys,subprocess,os,copy
O=pathlib.Path(__file__).resolve().parent
B=pathlib.Path('docs/plans/qualification/A15_HARNESS_IMPLEMENTATION_QUALIFICATION_1')
A=B/'p86-risk-adaptive-construction-120'
def load(p):return json.loads(p.read_text())
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def need(b,s):
 if not b:raise ValueError(s)
def graph_ok(edges):
 active=set();seen=set();adj={}
 for a,b in edges:adj.setdefault(a,[]).append(b)
 def walk(n):
  need(n not in active,'dependency cycle')
  if n in seen:return
  active.add(n)
  for t in adj.get(n,[]):walk(t)
  active.remove(n);seen.add(n)
 for n in adj:walk(n)
 return True
manifest=load(O/'authenticated-input-index.json')
for p,h in manifest['PINS'].items():need(sha(pathlib.Path(p).read_bytes())==h,'input pin '+p)
for p,h in load(O/'preservation-before.json')['FILES'].items():need(sha(pathlib.Path(p).read_bytes())==h,'historical preservation '+p)
policy=load(A/'proposed-policy-allocation.json');paths=load(A/'two-file-scope.json')['EXACT_PATHS']
need(len(paths)==2 and all(not pathlib.Path(p).exists() for p in paths),'sources absent/exact2')
need(sha(canon(policy))==manifest['PACKAGE120_POLICY_CANONICAL_SHA256']=='0405a4b19e4b2634f28a9463ef5f3238b3c904d251096427ac4b8ed776613cec','policy identity')
cmd=load(B/'system-process-enforcement-86/transient-service-specification.json')['EXACT_COMMAND_ARGV'];command=sha(canon(cmd));need(command=='e628c8664ea72357963dc58dddee934c28cad3ab5c84450656a6595e6910fb50','retained command')
original=load(A/'36-row-phase-matrix.json')['REQUIREMENTS'];trace=load(O/'36-requirement-trace-matrix.json')['ROWS'];need(len(original)==len(trace)==36,'36rows')
for r,t in zip(original,trace):need(r['REQUIREMENT_ID']==t['REQUIREMENT_ID'] and r['RETAINED_EARLIEST_PHASE']==t['PHASE'] and r['CLASS']==t['ORIGINAL_CLASS'] and r['EXACT_CLAUSE']==t['EXACT_AUTHORITY_CLAUSE'] and r['AUTHORITY_SOURCE']==t['AUTHORITY_PIN'],'phase/source trace')
# Reconstruct exact clause provenance, not just the proposed classification.
for r in load(O/'construction-control-authority-trace.json')['ROWS']:
 path=pathlib.Path(r['SOURCE_PATH']);need(sha(path.read_bytes())==r['SOURCE_RAW_SHA256'],'trace raw hash')
 value=load(path)
 for part in r['JSON_POINTER'].split('/')[1:]:value=value[int(part)] if isinstance(value,list) else value[part]
 if isinstance(value,list):need(r['EXACT_CLAUSE'] in value,'exact clause array')
 else:need(value==r['EXACT_CLAUSE'],'exact clause text')
resource=load(O/'resource-allocation-applicability.json');need(resource['P120_EXACT_POLICY']==policy,'retained policy')
conditional=resource['FULL_MAXIMUM_COPY_SCHEDULE_CONDITIONAL'];need(conditional['FULL_SIZE_FOUR_COPY_BYTES']==4*policy['MAX_RETAINED_SOURCE_BYTES']==500136,'four-copy model')
need(conditional['CONDITIONAL_EXCESS']==500136-375102==125034,'conditional source delta')
reservation=resource['UNCHANGED_POLICY_RESERVATION_OPTION'];need(reservation['RESERVE_PROMOTION_SOURCE_BYTES']==125034 and reservation['REMAINING_DEVELOPMENT_SOURCE_BYTES']==250068 and reservation['REMAINING_DEVELOPMENT_SOURCE_PUBLICATIONS']==4,'no-reset reservation arithmetic')
cp=subprocess.run([sys.executable,str(B/'p86-publication-amendment-issuance-115/verify_independent.py'),'EFFECTIVE'],capture_output=True,text=True)
need(cp.returncode==0,'fresh effective charter/104/115/A15 reader');json.loads(cp.stdout)
isolation=load(O/'disposable-isolation-contract.json');promotion=load(O/'two-file-promotion-contract.json');ready=load(O/'decision-readiness-matrix.json');edges=load(O/'dependency-graph.json')['EDGES'];graph_ok(edges)
need(isolation['ROOT_CREATED'] is False and isolation['ACTIVE_BOUNDARY_VERIFIED'] is False,'no active isolation')
need(promotion['DESTINATION_PATHS']==paths and promotion['NO_ACTIVE_PROMOTION'] is True and promotion['CONTRACT_COMPLETE'] is False,'unbound promoter')
need(ready['GOVERNANCE_CHANGE_REQUIRED']=='NO' and ready['DECISION_OPTIONS']==[] and ready['SELECTED_ROUTE']=='C_NEITHER_CURRENTLY_QUALIFIED','readiness scope')
for k,v in ready.items():
 if k.endswith('_READY') or k.endswith('_COMPLETE'):need(v is False,'no qualified phase')
# Documentary admission/phase invariants. No actual file publication or target tests.
model={'paths':paths,'command':command,'candidate_raw_pins':None,'authority_required':True,'authority_issued':False,'isolation_receipt':None,'workspace_access_is_isolation':False,'symlinks_allowed':False,'hardlinks_allowed':False,'postwrite_is_admission':False,'protected_paths':isolation['PROTECTED_HOST_PATHS'],'cpu':policy['MAX_AGGREGATE_CPU_SECONDS'],'memory':policy['MAX_AGGREGATE_MEMORY_BYTES'],'principal_receipt':None,'promoter_qualified':False,'file_fsync_required':True,'directory_fsync_required':True,'published_pair':[False,False],'verified_pair_commit':False,'promotion_report':'NOT_PERFORMED','automatic_retries':0,'reuse_consumption':False,'unknown_result':'INCOMPLETE','own_future_result_required':False,'entry_safety_required':True,'promotion_copy_exempt':False,'phase_budget_reset':False,'resource_applicability_complete':False,'decision_options':[],'edges':edges}
def validate(m):
 need(m['paths']==paths,'source allowlist')
 need(m['command']==command and m['candidate_raw_pins'] is None,'no forged command/source pins')
 need(m['authority_required'] and not m['authority_issued'],'no absent/inferred authority')
 need(m['isolation_receipt'] is None and not m['workspace_access_is_isolation'],'workspace permission not qualified isolation')
 need(not m['symlinks_allowed'] and not m['hardlinks_allowed'],'link escape policy')
 need(not m['postwrite_is_admission'],'detection not admission')
 need(m['protected_paths']==isolation['PROTECTED_HOST_PATHS'],'protected paths omitted')
 need(m['cpu']==policy['MAX_AGGREGATE_CPU_SECONDS'] and m['memory']==policy['MAX_AGGREGATE_MEMORY_BYTES'],'finite retained proposed resource values')
 need(m['principal_receipt'] is None and not m['promoter_qualified'],'unqualified principal')
 need(m['file_fsync_required'] and m['directory_fsync_required'],'durability barriers')
 if m['promotion_report']=='PASS':need(all(m['published_pair']) and m['verified_pair_commit'] and m['promoter_qualified'],'partial or unverified pair not success')
 need(m['automatic_retries']==0 and not m['reuse_consumption'],'consumed no retry/reuse')
 need(m['unknown_result']=='INCOMPLETE','unknown not pass')
 need(not m['own_future_result_required'] and m['entry_safety_required'],'earliest entry safety/own-result distinction')
 need(not m['promotion_copy_exempt'] and not m['phase_budget_reset'],'no copy exemption/reset')
 need(not m['resource_applicability_complete'] and m['decision_options']==[],'incomplete subject not selectable')
 graph_ok(m['edges'])
validate(model);negative=[]
def reject(name,mut):
 m=copy.deepcopy(model);mut(m)
 try:validate(m)
 except ValueError as e:negative.append({'DESIGN':name,'RESULT':'REJECTED','CAUSE':str(e)});return
 raise AssertionError('negative accepted: '+name)
def change(k,v):return lambda m:m.__setitem__(k,v)
reject('forged source pins before candidate exists',change('candidate_raw_pins',['0'*64,'0'*64]))
reject('missing scoped authority requirement',change('authority_required',False))
reject('dossier treated as issued grant',change('authority_issued',True))
reject('workspace write access presented as isolation',change('workspace_access_is_isolation',True))
reject('unverified isolation receipt invented',change('isolation_receipt','0'*64))
reject('symlink escape admitted',change('symlinks_allowed',True))
reject('hardlink alias admitted',change('hardlinks_allowed',True))
reject('post-write checks presented as admission',change('postwrite_is_admission',True))
reject('protected path omitted',lambda m:m['protected_paths'].pop())
reject('unbounded CPU',change('cpu',None))
reject('unbounded memory',change('memory',None))
reject('arbitrary CPU',change('cpu',99999))
reject('arbitrary memory',change('memory',99999))
reject('insufficient promotion principal qualified',change('promoter_qualified',True))
reject('forged promoter receipt',change('principal_receipt','0'*64))
reject('changed86command',change('command','0'*64))
reject('widened source allowlist',lambda m:m['paths'].append('adapter/planner/core.py'))
reject('missing file fsync',change('file_fsync_required',False))
reject('missing directory fsync',change('directory_fsync_required',False))
def partial(m):m['published_pair']=[True,False];m['promotion_report']='PASS'
reject('partial two-file promotion treated as success',partial)
def both_nocommit(m):m['published_pair']=[True,True];m['promotion_report']='PASS'
reject('both files without pair verification called success',both_nocommit)
reject('implicit retry',change('automatic_retries',1))
reject('reused consumption',change('reuse_consumption',True))
reject('unknown outcome pass',change('unknown_result','PASS'))
reject('own future outcome required before authority',change('own_future_result_required',True))
reject('entry safety deferred',change('entry_safety_required',False))
reject('promotion copy silently exempted',change('promotion_copy_exempt',True))
reject('budget reset between phases',change('phase_budget_reset',True))
reject('incomplete resource split complete',change('resource_applicability_complete',True))
reject('incomplete decision options supplied',change('decision_options',['AUTHORIZE']))
reject('development authority cycle',lambda m:m['edges'].append(['DEVELOPMENT_OUTCOME','DEVELOPMENT_DECISION']))
reject('promotion own-outcome cycle',lambda m:m['edges'].append(['PROMOTION_OUTCOME','PROMOTION_DECISION']))
semantic={'INPUT_PIN_SET_SHA256':sha(canon(manifest['PINS'])),'COMMAND_SHA256':command,'P120_POLICY_SHA256':sha(canon(policy)),'EXACT_SOURCE_PATHS':paths,'PHASE_COUNT':36,'TRACE_SHA256':sha(canon(trace)),'CONTROL_TRACE_SHA256':sha(canon(load(O/'construction-control-authority-trace.json'))),'FULL_SIZE_CONDITIONAL_CHARGE':500136,'CONDITIONAL_DELTA':125034,'RESERVED_DEVELOPMENT_BYTES':250068,'OUTCOME':'C_NEITHER_CURRENTLY_QUALIFIED','GOVERNANCE_CHANGE_REQUIRED_FOR_NONWEAKENING_SPLIT':'NO','RESOURCE_APPLICABILITY_COMPLETE':False,'PROMOTION_QUALIFIED':False,'ISOLATION_QUALIFIED':False,'DECISION_OPTIONS':[],'READINESS':ready,'GRAPH_ACYCLIC':True,'PRIOR_PRESERVATION':'PASS','NEGATIVES':negative}
print(json.dumps({'HASH_SEED':os.environ.get('PYTHONHASHSEED'),'RECONSTRUCTION':semantic,'SEMANTIC_SHA256':sha(canon(semantic))},sort_keys=True))
