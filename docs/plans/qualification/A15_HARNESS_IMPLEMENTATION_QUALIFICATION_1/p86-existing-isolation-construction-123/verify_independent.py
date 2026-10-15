"""Static record/file/AST reconstruction only; no native confinement or target launch."""
import pathlib,json,hashlib,os,sys,subprocess,copy,ast,gzip
O=pathlib.Path(__file__).resolve().parent
B=pathlib.Path('docs/plans/qualification/A15_HARNESS_IMPLEMENTATION_QUALIFICATION_1');A=B/'p86-risk-adaptive-construction-120'
def load(p):return json.loads(p.read_text())
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def sha(x):return hashlib.sha256(x).hexdigest()
def need(x,r):
 if not x:raise ValueError(r)
def acyclic(edges):
 adj={};active=set();seen=set()
 for a,b in edges:adj.setdefault(a,[]).append(b)
 def walk(n):
  need(n not in active,'cycle')
  if n in seen:return
  active.add(n)
  for m in adj.get(n,[]):walk(m)
  active.remove(n);seen.add(n)
 for n in adj:walk(n)
 return True
m=load(O/'authenticated-input-index.json')
for p,h in m['PINS'].items():need(sha(pathlib.Path(p).read_bytes())==h,'input pin '+p)
for p,h in load(O/'preservation-before.json')['FILES'].items():need(sha(pathlib.Path(p).read_bytes())==h,'history '+p)
paths=load(A/'two-file-scope.json')['EXACT_PATHS'];need(len(paths)==2 and all(not pathlib.Path(p).exists() for p in paths),'exact absent sources')
policy=load(A/'proposed-policy-allocation.json');need(sha(canon(policy))==m['PACKAGE120_POLICY_SHA256']=='0405a4b19e4b2634f28a9463ef5f3238b3c904d251096427ac4b8ed776613cec','policy identity')
command=sha(canon(load(B/'system-process-enforcement-86/transient-service-specification.json')['EXACT_COMMAND_ARGV']));need(command=='e628c8664ea72357963dc58dddee934c28cad3ab5c84450656a6595e6910fb50','command pin')
profile_search=load(O/'existing-receipt-search.json');inspected=[];matches=[]
for p in B.rglob('*.json'):
 if O in p.resolve().parents:continue
 if p.name.startswith(('preservation','four-seed','negative','evidence-index')):continue
 if not any(w in p.name.lower() for w in ['profile','receipt','isolation','namespace','environment']):continue
 try:d=load(p)
 except (OSError,ValueError):continue
 inspected.append(str(p))
 if any(s in json.dumps(d).upper() for s in ['ISOLATION_PROFILE_RECEIPT','SIGNED_ISOLATION','PROFILE_RECEIPT_IDENTITY','ISOLATION_PROFILE_INDEPENDENTLY_QUALIFIED']):matches.append(str(p))
need(sorted(inspected)==sorted(profile_search['NAMED_PROFILE_RECORDS_INSPECTED']) and matches==profile_search['RECEIPT_OR_QUALIFICATION_FIELD_MATCHES']==[],'bounded receipt search')
obs=load(O/'read-only-executable-configuration-observations.json');binarypins={}
for x in obs['BINARIES']:
 if x['PATH']:
  need(sha(pathlib.Path(x['PATH']).read_bytes())==x['SHA256'],'observed executable pin '+x['NAME']);binarypins[x['NAME']]=x['SHA256']
for doc in obs['LOCAL_DOCUMENTATION_PINS']:
 p=pathlib.Path(doc['PATH']);need(sha(p.read_bytes())==doc['RAW_SHA256'] and sha(gzip.decompress(p.read_bytes()))==doc['DECOMPRESSED_SHA256'],'manual pin')
# Package-version assertions are independently reconstructed from file metadata, not binary execution.
packages={}
for stanza in pathlib.Path('/var/lib/dpkg/status').read_text().split('\n\n'):
 f=dict(l.split(': ',1) for l in stanza.splitlines() if ': ' in l and not l.startswith(' '))
 if f.get('Package') in obs['PACKAGE_METADATA']:packages[f['Package']]={'VERSION':f.get('Version'),'STATUS':f.get('Status')}
need(packages==obs['PACKAGE_METADATA'],'package versions')
inventory=load(O/'candidate-profile-inventory.json');need(len(inventory['CANDIDATES'])==5 and not inventory['APPLICABLE_EXISTING_PROFILE_FOUND'] and not inventory['INDEPENDENTLY_QUALIFIED_PROFILE'] and inventory['SELECTED']=='NONE','no qualified profile')
legacy=load(B/'direct-host-calibration-guard-108/namespace-mount-contract.json');need(binarypins['bwrap']==legacy['BINARY_IDENTITY_CANDIDATE']['SHA256'],'retained/current bwrap pin')
slot=load(O/'publication-slot-reconciliation.json');options=slot['OPTIONS'];need([x['ID'] for x in options]==['RESERVE_EXISTING_THREE','REDEFINE_MEASURE','EXPLICIT_REVISED_FOUR'],'three alternatives')
need(options[0]['PER_FILE_SLOTS']==3 and options[0]['PAIR_PUBLICATIONS']==6 and options[0]['MAX_CUMULATIVE_SOURCE_BYTES']==3*125034==375102,'three-slot arithmetic')
need(options[0]['REMAINING_DEVELOPMENT_BYTES']==250068 and options[0]['RESERVED_PROMOTION_BYTES']==125034,'promotion reservation')
need(options[1]['PER_FILE_SLOTS'] is None and options[1]['STATUS']=='UNSUPPORTED_UNDER_UNCHANGED_P120_FULL_PUBLICATION_RULE','no favorable redefinition')
need(options[2]['PER_FILE_SLOTS']==4 and options[2]['PAIR_PUBLICATIONS']==8 and options[2]['MAX_CUMULATIVE_SOURCE_BYTES']==500136 and options[2]['DELTA_SOURCE_BYTES']==125034,'revised four-slot arithmetic')
need(options[2]['PER_FILE_CUMULATIVE_BYTES']=={f['PATH']:4*f['MAX_RETAINED_SOURCE_BYTES'] for f in policy['FILES']} and slot['SELECTED'] is None and not slot['ANY_OPTION_EFFECTIVE'],'per-file/no adopted allocation')
original=load(B/'p86-construction-isolation-promotion-122/36-requirement-trace-matrix.json')['ROWS'];audit=load(O/'36-requirement-phase-audit.json');need(audit['COUNT']==len(audit['REQUIREMENTS'])==36 and audit['REQUIREMENTS']==original and audit['PHASE_REASSIGNMENTS']==[],'36 phases preserved')
res=load(O/'resource-observer-enforcement-matrix.json');oldres=load(B/'p86-construction-supervisor-binding-121/limit-enforcement-matrix.json')['LIMITS'];need(len(res['LIMITS'])==len(oldres)==41,'all resource classes')
for old,new in zip(oldres,res['LIMITS']):need(all(new[k]==v for k,v in old.items()) and new['ACTUAL_ENFORCEMENT']=='UNVERIFIED','limits unchanged/not promoted')
need(not res['CONTRACT_COMPLETE'] and not res['OBSERVER_COMPLETE'] and res['OBSERVER_EXECUTABLE_IDENTITY'] is None,'resource/observer gaps')
record=len(canon(load(A/'allocation-rationale.json')['CRITICAL_SCHEMA_MAXIMAL_INSTANCE']));need(record==584 and record*4==policy['PROTECTED_CRITICAL_EVIDENCE_BYTES']==2336,'schema584reserve')
check=load(O/'prospective-minimum-capability-check.json');need(check['PAYLOAD_EXECUTABLE_PIN']['SHA256']==binarypins['findmnt'],'findmnt payload pin');need(check['PAYLOAD_ARGUMENT_VECTOR']==[check['PAYLOAD_EXECUTABLE_PIN']['PATH'],'--json','--output','TARGET,SOURCE,FSTYPE,OPTIONS'] and check['ARGUMENT_VECTOR_SHA256']==sha(canon(check['PAYLOAD_ARGUMENT_VECTOR'])),'prospective argv')
limits=check['PROPOSED_SAFETY_LIMITS_FROM_P120_NOT_AUTHORITY'];mapping={'MAX_AGGREGATE_LIVE_TASKS':'MAX_LIVE_PROCESSES_AND_THREADS','MAX_TOTAL_PROCESS_CREATIONS':'MAX_TOTAL_PROCESS_CREATIONS','MAX_WALL_SECONDS':'MAX_STATIC_ROUND_WALL_SECONDS','MAX_CPU_SECONDS_PER_PROCESS':'MAX_PER_PROCESS_CPU_SECONDS','MAX_CPU_SECONDS_AGGREGATE':'MAX_AGGREGATE_CPU_SECONDS','MAX_ADDRESS_SPACE_BYTES_PER_PROCESS':'MAX_PER_PROCESS_ADDRESS_SPACE_BYTES','MAX_MEMORY_BYTES_AGGREGATE':'MAX_AGGREGATE_MEMORY_BYTES','MAX_FDS_PER_PROCESS':'MAX_OPEN_FDS_PER_PROCESS','MAX_FDS_AGGREGATE':'MAX_AGGREGATE_OPEN_FDS','MAX_OUTPUT_AND_TOTAL_EVIDENCE_BYTES':'MAX_TOTAL_LOGICAL_EVIDENCE_BYTES','PROTECTED_CRITICAL_BYTES':'PROTECTED_CRITICAL_EVIDENCE_BYTES','MAX_ORDINARY_WITNESS_PUBLICATION_BYTES':'MAX_NORMAL_EVIDENCE_BYTES'}
need(all(limits[k]==policy[v] for k,v in mapping.items()) and limits['MAX_ATTEMPTS']==1 and limits['AUTOMATIC_RETRIES']==0,'finite comparison policy not authority')
need(not check['CHECK_SUBJECT_COMPLETE'] and not check['EXECUTION_READY'] and check['AUTHORIZATION_OPTIONS']==[],'unbound capcheck not activated')
for path in ['adapter/qualification_bootstrap/systemd_pids_once.py','adapter/tests/test_systemd_pids_bootstrap.py']:ast.parse(pathlib.Path(path).read_text())
cp=subprocess.run([sys.executable,str(B/'p86-publication-amendment-issuance-115/verify_independent.py'),'EFFECTIVE'],capture_output=True,text=True);need(cp.returncode==0,'fresh governance lifecycle');json.loads(cp.stdout)
edges=load(O/'dependency-graph.json')['EDGES'];acyclic(edges)
contracts=['candidate-profile-inventory.json','protected-path-isolation-analysis.json','disposable-workspace-handoff-contract.json','promotion-contract.json','resource-observer-enforcement-matrix.json','publication-slot-reconciliation.json','prospective-minimum-capability-check.json','risk-adaptive-governance-assessment.json','continuous-versus-isolated-comparison.json','retained-schema-arithmetic-note.json','lessons-register-review.json','remaining-gap-dossier.json']
model={'paths':paths,'pins':binarypins,'qualified_profile':False,'protected_write_allowed':False,'symlinks_allowed':False,'hardlinks_allowed':False,'inherited_writable_fd_allowed':False,'mutation_api_allowed':False,'broad_workspace_is_isolation':False,'postwrite_is_admission':False,'enforcement_verified':False,'observer_qualified':False,'slots':3,'publications':[ 'initial','revision','promotion'],'hidden_fourth':False,'revisions':1,'slot_redefinition_adopted':False,'physical_pair_atomic':False,'pair_report':'INCOMPLETE','pair_files':[False,False],'pair_commit':False,'future_probe_required':False,'entry_safety_required':True,'construction_authority':False,'probe_authority':False,'capcheck_authority':False,'capcheck_outer_guard_qualified':False,'check_ready':False,'byte_measure_conflated':False,'buffer_return_proves_durability':False,'retry_reset':False,'history_preserved':True,'command':command,'edges':edges}
def validate(x):
 need(x['paths']==paths and x['pins']==binarypins,'exact paths/binary pins')
 need(not x['qualified_profile'] and not x['enforcement_verified'] and not x['observer_qualified'],'unverified qualification')
 need(not any(x[k] for k in ['protected_write_allowed','symlinks_allowed','hardlinks_allowed','inherited_writable_fd_allowed','mutation_api_allowed']),'protected path/alias/descriptor exclusion')
 need(not x['broad_workspace_is_isolation'] and not x['postwrite_is_admission'],'confinement vs monitoring')
 need(x['slots']==3 and len(x['publications'])<=3 and not x['hidden_fourth'] and isinstance(x['revisions'],int) and not isinstance(x['revisions'],bool) and 0<=x['revisions']<=1 and not x['slot_redefinition_adopted'],'reserve promotion slot; no fourth/free revision')
 need(not x['physical_pair_atomic'],'no atomicity proof')
 if x['pair_report']=='PASS':need(all(x['pair_files']) and x['pair_commit'],'partial pair not PASS')
 need(not x['future_probe_required'] and x['entry_safety_required'],'entry/execution phase')
 need(not x['construction_authority'] and not x['probe_authority'] and not x['capcheck_authority'] and not x['check_ready'] and not x['capcheck_outer_guard_qualified'],'no inferred unqualified activity')
 need(not x['byte_measure_conflated'] and not x['buffer_return_proves_durability'],'accounting/durability distinct')
 need(not x['retry_reset'] and x['history_preserved'] and x['command']==command,'no retry/history/command change')
 acyclic(x['edges'])
validate(model);negatives=[]
def reject(name,mut):
 x=copy.deepcopy(model);mut(x)
 try:validate(x)
 except ValueError as e:negatives.append({'DESIGN':name,'RESULT':'REJECTED','CAUSE':str(e),'MUTATION_CONTENT_SHA256':sha(canon(x))});return
 raise AssertionError('negative admitted: '+name)
def change(k,v):return lambda x:x.__setitem__(k,v)
for name,key in [('writable protected mount','protected_write_allowed'),('symlink escape','symlinks_allowed'),('hardlink escape','hardlinks_allowed'),('inherited writable descriptor','inherited_writable_fd_allowed'),('external mutation interface','mutation_api_allowed'),('broad workspace treated as confinement','broad_workspace_is_isolation'),('postwrite hash treated as admission','postwrite_is_admission'),('unenforced resource qualified','enforcement_verified'),('unqualified observer accepted','observer_qualified'),('installed binary treated as qualified profile','qualified_profile'),('hidden fourth publication','hidden_fourth'),('promotion physically atomic without proof','physical_pair_atomic'),('future probe required before construction','future_probe_required'),('construction authority inferred','construction_authority'),('probe authority inferred','probe_authority'),('capcheck authority inferred','capcheck_authority'),('unqualified capcheck outer guard','capcheck_outer_guard_qualified'),('capcheck activated prematurely','check_ready'),('submitted and logical bytes conflated','byte_measure_conflated'),('write return proves durability','buffer_return_proves_durability'),('retry allocation reset','retry_reset')]:reject(name,change(key,True))
reject('unpinned native binary',lambda x:x['pins'].__setitem__('bwrap','0'*64))
reject('unbounded revisions',change('revisions',None))
reject('second persisted revision in reserved three slots',change('revisions',2))
reject('four persisted publications under three-slot profile',lambda x:x['publications'].append('extra_revision'))
reject('favorable counting adopted without authority',change('slot_redefinition_adopted',True))
reject('entry safety deferred',change('entry_safety_required',False))
reject('changed source allowlist',lambda x:x['paths'].append('adapter/planner/core.py'))
reject('changed retained command',change('command','0'*64))
reject('history modified',change('history_preserved',False))
def partial(x):x['pair_report']='PASS';x['pair_files']=[True,False]
reject('partial pair complete',partial)
reject('own outcome before authority cycle',lambda x:x['edges'].append(['DEVELOPMENT_OUTCOME','DEVELOPMENT_DECISION']))
semantic={'VERIFIER_RAW_SHA256':sha(pathlib.Path(__file__).read_bytes()),'INPUT_PIN_SET_SHA256':sha(canon(m['PINS'])),'COMMAND_IDENTITY':command,'P120_POLICY_IDENTITY':sha(canon(policy)),'SOURCE_PATHS':paths,'LOCAL_BINARY_PINS':binarypins,'LOCAL_PACKAGE_METADATA':packages,'PROFILE_SEARCH_COUNT':len(inspected),'APPLICABLE_PROFILE_FOUND':False,'INDEPENDENT_PROFILE_QUALIFIED':False,'PROTECTED_WRITES_EXCLUDED':'UNVERIFIED','SLOT_OPTIONS':{'three':375102,'reserve_promotion':125034,'development':250068,'four':500136,'delta':125034,'selected':None},'PHASE_ROWS':36,'LIMIT_ROWS':41,'CANONICAL_RECORD_BYTES':584,'CAPCHECK_COMMAND_SHA256':check['ARGUMENT_VECTOR_SHA256'],'CAPCHECK_READY':False,'CONSTRUCTION_DECISION_READY':False,'CONSTRUCTION_ENTRY_READY':False,'CONTRACT_CONTENT_IDENTITIES':{n:sha(canon(load(O/n))) for n in contracts},'GRAPH_ACYCLIC':True,'PRIOR_PRESERVATION':'PASS','NEGATIVES':negatives}
print(json.dumps({'HASH_SEED':os.environ.get('PYTHONHASHSEED'),'RECONSTRUCTION':semantic,'SEMANTIC_SHA256':sha(canon(semantic))},sort_keys=True))
