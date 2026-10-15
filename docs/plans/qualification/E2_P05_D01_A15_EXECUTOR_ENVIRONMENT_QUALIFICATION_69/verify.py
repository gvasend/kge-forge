"""Independent read-only source/contract reconstruction. No Planner imports or calls.
Optional --candidate overrides only current Package69 metadata in memory.
"""
import ast, copy, hashlib, json, os, pathlib, platform, stat, subprocess, sys
D=pathlib.Path(__file__).resolve().parent;R=D.parents[3];Q=R/'docs/plans/qualification';C=Q/'E2_P05_D01_A15_CAPTURE_PERSISTENCE_RESUME_CLOSURE_61'
def rawhash(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canon(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def original(p):return json.loads(p.read_text())
def run(overrides=None,entry=True):
 overrides=overrides or {}
 def read(name):return copy.deepcopy(overrides[name]) if name in overrides else original(D/name)
 if entry:
  out=json.loads(subprocess.check_output([sys.executable,'docs/plans/qualification/E2_P05_D01_A15_NORMATIVE_ADOPTION_ISSUANCE_68/verify_effective.py'],cwd=str(R)))
  assert out['NORMATIVE_MANDATE_EFFECTIVE'] is True and not out['EXECUTION_AUTHORITY'] and not out['CAPTURE_AUTHORITY']
 assert read('input-authentication.json')['NATIVE_FUNCTIONS_CALLED'] is False
 for row in read('input-authentication.json')['INDICES']:
  index=R/row['EVIDENCE_INDEX']['PATH'];assert rawhash(index)==row['EVIDENCE_INDEX']['RAW_SHA256']
  obj=original(index);assert len(obj['FILES'])==row['FILES_VERIFIED']
  for path,h in obj['FILES'].items():assert rawhash(R/path)==h,path
 inv=read('existing-implementation-inventory.json');assert len(inv)==17 and len({x['COMPONENT_ID'] for x in inv})==17
 rebuilt=[]
 for row in inv:
  p=R/row['SOURCE_PATH'];assert rawhash(p)==row['SOURCE_IDENTITY']['RAW_SHA256']
  assert row['SOURCE_IDENTITY']['PATH']==row['SOURCE_PATH'] and row['INVOKED'] is False
  parsed=ast.parse(p.read_text());parts=row['ENTRYPOINT'].split('.');body=parsed.body
  for name in parts:
   node=next(n for n in body if isinstance(n,(ast.FunctionDef,ast.ClassDef,ast.AsyncFunctionDef)) and n.name==name);body=node.body
  assert node.lineno==row['LINE']
  # Independent signature render from AST source segments, no inspect/import of implementation.
  args=node.args;pos=args.posonlyargs+args.args;defaults=[None]*(len(pos)-len(args.defaults))+args.defaults
  words=[a.arg+('='+ast.get_source_segment(p.read_text(),z) if z is not None else '') for a,z in zip(pos,defaults)]
  if args.vararg:words.append('*'+args.vararg.arg)
  elif args.kwonlyargs:words.append('*')
  words += [a.arg+('='+ast.get_source_segment(p.read_text(),z) if z is not None else '') for a,z in zip(args.kwonlyargs,args.kw_defaults)]
  if args.kwarg:words.append('**'+args.kwarg.arg)
  assert row['FUNCTION_SIGNATURE']=='('+', '.join(words)+')'
  expected='IMPLEMENTED_AND_QUALIFIED' if row['COMPONENT_ID'] in ['N69-RESTORE','N69-SERIALIZE','N69-PUBLISH','N69-IMMUTABLE','N69-REPLAY'] else ('PARTIALLY_IMPLEMENTED' if row['COMPONENT_ID'].startswith('R69-A14-') or row['COMPONENT_ID'].startswith('R69-V3-') else 'IMPLEMENTED_NOT_QUALIFIED')
  assert row['QUALIFICATION_STATUS']==expected
  if expected=='IMPLEMENTED_AND_QUALIFIED':assert row['QUALIFICATION_DOMAIN']=='Retained A14 primitive domain only'
  rebuilt.append({'ID':row['COMPONENT_ID'],'SOURCE_SHA256':rawhash(p),'FUNCTION_AST':hashlib.sha256(ast.dump(node).encode()).hexdigest(),'SIGNATURE':row['FUNCTION_SIGNATURE'],'QUALIFICATION':expected})
 # Independently inspect why these reusable writers/readers are incompatible.
 writer=(Q/'E2_P05_D01_A14_WRITER_HANDOFF_CLOSURE_28/writer_entrypoint.py').read_text()
 reader=(Q/'E2_P05_D01_A14_COLD_READER_BINDING_CLOSURE_29/reader_entrypoint.py').read_text()
 assert 'ZERO_EVENT_FRAME_REQUIRED' in writer and 'bundle.events' in reader and 'event_count\':0' in reader
 codec=(R/'adapter/planner/codec.py').read_text();assert 'os.fsync(stream.fileno())' in codec and 'os.link(temporary, str(target))' in codec
 # Check exact variants/checkpoint/oracles directly from authoritative sources.
 cp=original(C/'initial-checkpoint-restore-contract.json');b=read('checkpoint-and-variant-bindings.json')
 assert b['CHECKPOINT_PATH']==cp['SOURCE_PATH'] and b['INITIAL_SNAPSHOT_IDENTITY']==cp['INITIAL_SNAPSHOT_IDENTITY'] and b['BUNDLE_IDENTITY']==cp['NATIVE_BUNDLE_IDENTITY']
 assert b['LEDGER_FILES_VERIFIED']==19 and b['LIVE_PINS_VERIFIED']==55 and b['NO_NATIVE_RESTORE'] is True
 for p,h in cp['RETAINED_LEDGER_FILES'].items():assert rawhash(R/p)==h
 native=original(R/cp['SOURCE_PATH'])['bundle']
 assert len(native['events'])==19
 for pin in native['sources']+[native['policy']]:assert rawhash(R/pin['path'])==pin['identity']['sha256']
 h=original(C/'static-harness-contract.json');assert h['STATIC_HARNESS_READY'] and len(b['VARIANTS'])==2
 for row,ref in zip(b['VARIANTS'],h['EXACT_OPERATION_BINDINGS']):
  assert row['BINDING']==original(C/ref['CAPTURE_BINDING'])
  assert row['ORACLE_PIN']['RAW_SHA256']==rawhash(C/ref['ORACLE_FILE']) and row['ORACLE_CANONICAL_SHA256']==canon(original(C/ref['ORACLE_FILE']))
  assert original(C/ref['ORACLE_FILE'])['FULL_ORACLE_READY'] is True
 invocations=read('candidate-executable-invocation-inventory.json')
 for x in invocations:
  assert x['SOURCE_IDENTITY']['RAW_SHA256']==rawhash(R/x['EXECUTABLE_PATH']) and x['INVOCATION_ARGUMENTS'] is None
  assert x['INTERPRETER']['RAW_SHA256']==rawhash(pathlib.Path(sys.executable).resolve())
  assert x['INTERPRETER']['RESOLVED_PATH']==str(pathlib.Path(sys.executable).resolve()) and x['INTERPRETER']['VERSION']==platform.python_version()
 obs=read('execution-environment-observations.json')
 assert obs['PYTHON_RUNTIME']['RAW_SHA256']==rawhash(pathlib.Path(sys.executable).resolve()) and obs['EUID']==os.geteuid()
 assert obs['HOST_IDENTITY'] is None and obs['PYTHON_RUNTIME']['VERSION']==platform.python_version()
 for p in obs['PERMISSIONS']:
  path=pathlib.Path(p['PATH']);s=path.stat()
  assert p['MODE']==oct(stat.S_IMODE(s.st_mode)) and p['RESOLVED']==str(path.resolve())
  assert p['OWNER_UID']==s.st_uid and p['OWNER_GID']==s.st_gid
  for key,mode in [('EUID_R_ACCESS',os.R_OK),('EUID_W_ACCESS',os.W_OK),('EUID_X_ACCESS',os.X_OK)]:assert p[key]==os.access(str(path),mode)
 assert obs['OBSERVED_CGROUP_BASE_EXISTS']==pathlib.Path('/sys/fs/cgroup/unified/kge-forge/executor').exists()
 assert obs['BWRAP_PRESENT']==pathlib.Path('/usr/bin/bwrap').exists()
 profile=read('future-execution-profile-specification.json');assert profile['PROFILE_STATUS']=='UNSEALED_SPECIFICATION'
 for k in ['ENVIRONMENT_ID','EXECUTABLE_IDENTITY','HOST_IDENTITY','DEPENDENCY_LOCK_IDENTITY','ACTUAL_SECURITY_LAUNCHER','RESOURCE_PERMISSION_EVIDENCE']:assert profile[k] is None
 assert profile['INVOCATIONS_SEALED'] is False and profile['OUTPUTS_CREATED'] is False
 assert profile['OUTPUT_ALLOWLIST']==original(C/'save-target-contracts.json')
 assert 'one supervisor' in profile['PROCESS_ISOLATION'].lower() and 'two fresh writers' in profile['PROCESS_ISOLATION'].lower() and 'eight fresh readers' in profile['PROCESS_ISOLATION'].lower()
 assert profile['RESOURCE_LIMITS']['NO_AUTOMATIC_RETRY'] and profile['RESOURCE_LIMITS']['total_native_workers']==2 and profile['RESOURCE_LIMITS']['total_cold_readers']==8
 assert not (Q/'A15_PROSPECTIVE_SCENARIO_1_RUNTIME').exists(),'actual runtime output unexpectedly present'
 arch=read('supervisor-worker-architecture-analysis.json')
 process=original(C/'writer-handoff-cold-reader-contracts.json')
 assert [arch['REQUIRED_SUPERVISORS'],arch['REQUIRED_WRITERS'],arch['REQUIRED_READERS']]==[process['SUPERVISORS'],process['WRITERS'],process['COLD_READERS']]==[1,2,8]
 assert arch['WORKER_SELF_CERTIFIES_EXIT'] is False and arch['HANDOFF_IS_EXIT_EVIDENCE'] is False and arch['READERS_REQUIRE_EXIT_AND_PUBLICATION'] is True
 assert arch['DISTINCT_MUTABLE_STATE_AND_OUTPUTS'] is True and arch['IDENTICAL_STARTING_CHECKPOINT'] is True and arch['A15_PROCESS_MODEL_IMPLEMENTED_AND_QUALIFIED'] is False
 cap=read('supervisor-worker-capability-matrix.json');assert len(cap)==9
 assert all(x['STATUS']=='PARTIALLY_IMPLEMENTED' for x in cap[:7]) and all(x['STATUS']=='NOT_IMPLEMENTED' for x in cap[7:])
 mapping=read('failure-retry-capability-mapping.json');old=original(C/'failure-retry-matrix.json')
 assert len(old)==len(mapping)
 for before,after in zip(old,mapping):assert all(after[k]==z for k,z in before.items()) and after['NO_RETRY_EXPANSION'] is True
 plan=read('implementation-qualification-test-plan.json');assert plan['TESTS_RUN_THIS_PACKAGE']==0 and plan['NATIVE_BACKEND_DURING_IMPLEMENTATION_TESTS'].startswith('Injected fake only')
 assert 'reader runs only after successful own-child exit and publication verification' in plan['QUALIFICATION_ACCEPTANCE']
 auth=read('implementation-authority-assessment.json');assert auth['APPLICABLE_IMPLEMENTATION_TEST_GRANTS_FOUND']==0 and auth['NORMATIVE_AUTHORITY_INCLUDES_IMPLEMENTATION'] is False and auth['IMPLEMENTATION_TEST_AUTHORITY_READY'] is False
 subject=read('proposed-implementation-test-authority-subject.json');content=subject['CONTENT']
 assert canon(content)==subject['CONTENT_IDENTITY']['sha256'] and subject['APPROVAL_EVIDENCE'] is None and subject['ISSUANCE_READY'] is False
 assert content['PURPOSE']=='New isolated qualification-only supervisor/worker/reader adapter; preserve native/V3 code and frozen artifacts'
 assert content['STATUS']=='PROPOSED_UNISSUED' and content['ISSUED_GRANT'] is None
 assert len(content['PERMITTED_SOURCE_FILES'])==6 and all(not (R/f).exists() for f in content['PERMITTED_SOURCE_FILES'])
 assert all(x.startswith('adapter/qualification_a15/') or x=='adapter/tests/test_qualification_a15_harness.py' for x in content['PERMITTED_SOURCE_FILES'])
 assert 'production/external/government permissions' in content['EXCLUDED'] and 'native runtime or selected V3 modification' in content['EXCLUDED']
 gates=read('readiness-gates.json')
 expected={'CHARTER_EFFECTIVE':'YES','A15_NORMATIVE_MANDATE_EFFECTIVE':'YES','IMPLEMENTATION_INVENTORY_COMPLETE':'YES','SUPERVISOR_WORKER_QUALIFIED':'NO','EXECUTABLE_IDENTITY_SEALED':'NO','ENVIRONMENT_PROFILE_SEALED':'NO','RESOURCE_PERMISSIONS_VERIFIED':'NO (current read/DAC observations only; future profile unsealed)','IMPLEMENTATION_TEST_AUTHORITY_READY':'NO','A15_EXECUTION_DECISION_READY':'NO','A15_CAPTURE_DECISION_READY':'NO'}
 assert gates==expected
 resource=read('resource-permission-assessment.json');assert resource['RESOURCE_PERMISSIONS_VERIFIED'] is False and resource['CHARTER_CREATES_OS_PERMISSIONS'] is False and resource['ELEVATION_REQUESTED'] is False
 lessons=read('reasoning-lessons-evidence-update.json');assert lessons['LESSONS_REVIEWED']==10 and lessons['NEW_LESSONS']==0 and lessons['REGISTER_MODIFIED'] is False
 for pin in [lessons['REGISTER_PIN'],lessons['MD_PIN']]:assert rawhash(R/pin['PATH'])==pin['RAW_SHA256']
 # Static inventory scripts may inspect strings/AST only, never import or call native modules.
 for p in [D/'construct.py',D/'verify.py']:
  tree=ast.parse(p.read_text())
  for n in ast.walk(tree):
   if isinstance(n,ast.Import):assert all(not z.name.startswith('adapter') for z in n.names)
   if isinstance(n,ast.ImportFrom):assert not (n.module or '').startswith('adapter')
 return {'RESULT':'PASS_STATIC','INVENTORY_RECONSTRUCTION':rebuilt,'CAPABILITIES':cap,'VARIANT_BINDING_HASH':canon(b),'ENVIRONMENT_OBSERVATION_HASH':canon(obs),'PERMISSION_HASH':canon(resource),'IMPLEMENTATION_PLAN_HASH':canon(plan),'PROPOSED_SUBJECT_IDENTITY':subject['CONTENT_IDENTITY'],'READINESS':expected,'NATIVE_FUNCTIONS_CALLED':False}
if __name__=='__main__':
 result=run(json.load(sys.stdin) if '--candidate' in sys.argv else None)
 print(json.dumps(result,sort_keys=True))
