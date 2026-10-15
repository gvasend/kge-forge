"""Independent documentary authority verifier; no native or synthetic test execution."""
import ast,copy,hashlib,itertools,json,os,pathlib,platform,stat,subprocess,sys
D=pathlib.Path(__file__).resolve().parent;R=D.parents[3];Q=R/'docs/plans/qualification';C=Q/'E2_P05_D01_A15_CAPTURE_PERSISTENCE_RESUME_CLOSURE_61';P69=Q/'E2_P05_D01_A15_EXECUTOR_ENVIRONMENT_QUALIFICATION_69'
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canon(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def entry():
 out=json.loads(subprocess.check_output([sys.executable,'docs/plans/qualification/E2_P05_D01_A15_NORMATIVE_ADOPTION_ISSUANCE_68/verify_effective.py'],cwd=str(R)))
 assert out['RESULT']=='PASS' and out['NORMATIVE_MANDATE_EFFECTIVE'] is True and not out['EXECUTION_AUTHORITY'] and not out['CAPTURE_AUTHORITY']
 return {'CHARTER_EFFECTIVE':'YES','A15_NORMATIVE_MANDATE_EFFECTIVE':'YES','ADOPTION_RECORD_IDENTITY':out['ADOPTION_RECORD_IDENTITY'],'EFFECTIVE_REFERENCE_RAW_SHA256':out['EFFECTIVE_REFERENCE_RAW_SHA256'],'A15_EXECUTION_AUTHORITY_ISSUED':'NO','A15_CAPTURE_AUTHORITY_ISSUED':'NO'}
def phase_enable(profile,phase,facts):
 guards=profile['PHASE_GUARDS'].get(phase)
 return bool(guards) and all(facts.get(x) is True for x in guards)
def verify(candidate=None,check_entry=True,check_contract_files=True):
 ep=entry() if check_entry else None
 for x in load(D/'input-authentication.json')['INDICES']:
  p=R/x['PIN']['PATH'];assert sha(p)==x['PIN']['RAW_SHA256'];idx=load(p)
  assert len(idx['FILES'])==x['VERIFIED_FILES']
  for path,h in idx['FILES'].items():assert sha(R/path)==h,path
 s=copy.deepcopy(candidate) if candidate is not None else load(D/'implementation-test-authority-subject.json');b=s['CONTENT']
 assert set(b)==set(load(D/'implementation-test-authority-subject.json')['CONTENT'])
 assert s['IDENTITY']['sha256']==canon(b) and s['IDENTITY']['namespace']=='qualification-A15-implementation-synthetic-test-authority-subject-v1'
 assert s['IDENTITY']['kind']['value']=='CONTENT_IDENTITY'
 assert s['PROJECT_OWNER_APPROVAL_EVIDENCE'] is None and s['ISSUED_GRANT_IDENTITY'] is None and s['ANY_OPTION_SELECTED'] is False
 assert b['STATUS']=='PROPOSED_UNISSUED' and b['CHARTER_VERSION']=='1.0'
 assert b['GOVERNING_CHARTER']['sha256']=='d26962c58f17281173e965433dae63a941e078115f3dcc30e2a3512fa21812b8'
 assert b['EFFECTIVE_CHARTER_LIFECYCLE']['sha256']=='a27516baa0ab7f34a36a1130490b6cfa38c508975ca337e0824c8eac33715cbb'
 assert b['NORMATIVE_SUBJECT']['sha256']=='b83a133c612f690f433e64b4e4f2788369851466d850cfdb7a6fb135d6f8e30d'
 assert b['TECHNICAL_PREPARATION_SUBJECT']['sha256']=='befe07aacc6b4c4e203488bce731f265a0520cf145174dca33dbfb4e68b43e9b'
 charter=load(Q/'KGE_FORGE_QUALIFICATION_GOVERNANCE_CHARTER_65/charter-content.json')
 assert b['ISSUER_ROLE']==charter['GOVERNING_AUTHORITY']['ROLE_ID']=='KGE-FORGE-PROJECT-OWNER-QUALIFICATION-GOVERNING-AUTHORITY'
 assert charter['QUALIFICATION_SCOPE']=='KGE-Forge qualification governance only' and 'General engineering governance authority' in charter['EXCLUSIONS']
 actual=load(Q/'E2_P05_D01_A15_NORMATIVE_ADOPTION_ISSUANCE_68/effective-normative-mandate-reference.json')
 assert b['NORMATIVE_ADOPTION_RECORD_PIN']==actual['ADOPTION_RECORD_PIN']
 assert sha(R/b['EFFECTIVE_NORMATIVE_REFERENCE_PIN']['PATH'])==b['EFFECTIVE_NORMATIVE_REFERENCE_PIN']['RAW_SHA256']
 old=load(P69/'proposed-implementation-test-authority-subject.json');assert b['PRIOR_IMPLEMENTATION_SUBJECT_IDENTITY']==old['CONTENT_IDENTITY']
 names=['source-file-scope.json','synthetic-fixture-contract.json','permitted-test-inventory.json','environment-resource-permission-contract.json','process-isolation-persistence-controls.json','failure-retry-controls.json','implementation-qualification-acceptance.json','authority-interpretation.json']
 assert sorted(b['CONTRACTS'])==sorted(names) and len(b['EVIDENCE_PINS'])==len(names)
 # Contract integrity is separate from independently qualified meanings below.
 for n in names:
  assert set(b['CONTRACTS'][n])==set(load(D/n))
  if check_contract_files:assert b['CONTRACTS'][n]==load(D/n)
 for pin in b['EVIDENCE_PINS']:assert sha(R/pin['PATH'])==pin['RAW_SHA256']
 c=b['CONTRACTS'];scope=c['source-file-scope.json']
 required_files=['adapter/qualification_a15/'+n for n in ['__init__.py','contracts.py','supervisor.py','worker.py','reader.py']]+['adapter/tests/test_qualification_a15_harness.py']
 assert scope['PERMITTED_SOURCE_FILES']==old['CONTENT']['PERMITTED_SOURCE_FILES']==required_files
 assert all(not (R/f).exists() for f in required_files)
 assert scope['NO_EXISTING_RUNTIME_MODIFICATION'] and scope['NO_SELECTED_V3_MODIFICATION']
 required_components={'SUPERVISOR_COMPONENT','WORKER_COMPONENT','PROCESS_LAUNCH_INTERFACE','CHECKPOINT_INPUT_VALIDATOR','RESULT_CAPTURE_INTERFACE','SAVE_PUBLICATION_INTERFACE','WRITER_EXIT_OBSERVER','HANDOFF_INTERFACE','COLD_READER_INTERFACE','ORACLE_COMPARISON_INTERFACE','FAILURE_RETRY_CONTROLLER'}
 assert {x['COMPONENT_ID'] for x in scope['COMPONENTS']}==required_components
 assert all(x['SOURCE_PATH'] in required_files and x['STATUS']=='NEW_PROSPECTIVE_SYMBOL_NOT_IMPLEMENTED' for x in scope['COMPONENTS'])
 fixture=c['synthetic-fixture-contract.json'];cp=load(C/'initial-checkpoint-restore-contract.json');real=load(R/cp['SOURCE_PATH'])['bundle'];deny=fixture['REAL_INPUT_DENYLIST']
 assert deny['CHECKPOINT_PATH']==cp['SOURCE_PATH'] and deny['INITIAL_SNAPSHOT_IDENTITY']==cp['INITIAL_SNAPSHOT_IDENTITY'] and deny['INITIAL_BUNDLE_IDENTITY']==cp['NATIVE_BUNDLE_IDENTITY']
 assert deny['LEDGER_FILES']==list(cp['RETAINED_LEDGER_FILES'])
 assert deny['RETAINED_SOURCE_IDENTITIES']==[x['identity'] for x in real['sources']] and len(deny['RETAINED_SOURCE_IDENTITIES'])==54
 assert deny['RETAINED_EVENT_IDENTITIES']==[x['identity'] for x in real['events']] and len(deny['RETAINED_EVENT_IDENTITIES'])==19
 refs=load(C/'static-harness-contract.json')['EXACT_OPERATION_BINDINGS']
 assert deny['VARIANT_IDS']==[x['VARIANT_ID'] for x in refs]
 assert deny['INVALIDATION_CONTENT_IDENTITIES']==[load(C/x['ORACLE_FILE'])['SOURCE_CONTENT_IDENTITY'] for x in refs]
 assert fixture['REAL_A15_EXECUTION_ALLOWED'] is False and fixture['FIXTURE_ORACLES_SEALED_NOW'] is False
 assert fixture['SCOPE']=='KGE-FORGE-A15-SYNTHETIC-IMPLEMENTATION-QUALIFICATION' and fixture['SUBJECT_NAME_PREFIX']=='SYNTHETIC-A15-TEST-'
 assert fixture['NATIVE_IDENTITY_DOMAINS']=={'Snapshot':'CONTENT_IDENTITY/planner-snapshot-v1','Source':'CONTENT_IDENTITY/raw-file-sha256','Bundle':'CONTENT_IDENTITY/planner-bundle-v1','Event':'CONTENT_IDENTITY/planner-event-v1'}
 policy=fixture['POLICY_EXCEPTION'];assert sha(R/policy['PATH'])==policy['RAW_SHA256']=='475bef0b28d7b484ba2641c654b37e9ce3d6f6ae1b0e13dfdcadaa3f79a2a3b5'
 assert 'POLICY_PIN' in (R/'adapter/planner/selector.py').read_text() and 'SUPPORTED_POLICIES' in (R/'adapter/planner/selector.py').read_text()
 assert policy['NATIVE_POLICY_VERSION']=='E1-SELECTION-1-P06' and 'never a changed synthetic source or invalidation target' in policy['PERMITTED_USE']
 tests=c['permitted-test-inventory.json'];assert len(tests['TESTS'])==13 and len({x['TEST_ID'] for x in tests['TESTS']})==13
 assert all(x['ACTUAL_TEST_EXECUTED'] is False for x in tests['TESTS'])
 assert tests['NATIVE_SEQUENCE']==['record_result','save_bundle','restore'] and tests['SEPARATE_APPLY_EVENT_CALL'] is False
 assert tests['NO_REAL_A15_VARIANT_EXECUTION'] is True and tests['HEAD_MUTATION'] is False and tests['OTHER_EXISTING_TEST_SUITES_ALLOWED'] is False
 assert tests['NATIVE_EVENT_ALLOWLIST']==['SourceInvalidation with sealed synthetic expected_snapshot/changed identities only']
 for name in ['record_result','save_bundle','restore']:
  tree=ast.parse((R/'adapter/planner/codec.py').read_text());assert any(isinstance(x,ast.FunctionDef) and x.name==name for x in tree.body)
 profile=c['environment-resource-permission-contract.json'];obs=load(D/'observed-environment.json')
 assert sha(R/profile['OBSERVATION_PIN']['PATH'])==profile['OBSERVATION_PIN']['RAW_SHA256']
 assert profile['HOST_IDENTITY']==obs['OBSERVED_HOST_CONTENT_IDENTITY'] and profile['HOST_IDENTITY']['sha256']==canon(obs['HOST_FACTS'])
 host=obs['HOST_FACTS'];assert host['OS']==platform.system() and host['MACHINE']==platform.machine() and host['KERNEL']==platform.release() and host['NODE_NAME']==platform.node()
 assert host['BOOT_ID_SHA256']==hashlib.sha256(pathlib.Path('/proc/sys/kernel/random/boot_id').read_bytes()).hexdigest()
 assert profile['INTERPRETER']['INTERPRETER_BINARY_SHA256']==sha(pathlib.Path(sys.executable).resolve()) and profile['INTERPRETER']['INTERPRETER_VERSION']==platform.python_version()
 assert profile['SOURCE_ALLOWLIST']==required_files and profile['WORKING_DIRECTORY']==str(R)
 for p in obs['CURRENT_PERMISSIONS']:
  x=pathlib.Path(p['PATH']);st=x.stat();assert p['RESOLVED']==str(x.resolve()) and p['MODE']==oct(stat.S_IMODE(st.st_mode))
  for key,flag in [('READ',os.R_OK),('WRITE',os.W_OK),('EXECUTE',os.X_OK)]:assert p[key]==os.access(str(x),flag)
 assert obs['NAMESPACE_OR_NATIVE_TEST_LAUNCHES']==0 and obs['NETWORK_ACCESS_TESTED'] is False
 assert profile['SEALED_FOR_TEST_ENTRY'] is False and profile['PROFILE_STATE']=='UNSEALED_FUTURE_TEST_ENTRY; COMPLETE_CONDITIONAL_AUTHORIZATION_BOUNDARY'
 expected_ids=['EP70-GRANT','EP70-ACTOR','EP70-PATHS','EP70-CODE-SEAL','EP70-CONFINEMENT','EP70-LIMITS','EP70-PHASE','EP70-FIXTURE','EP70-PROCESS','EP70-NATIVE-SCOPE','EP70-AUDIT']
 assert profile['ACTIVATION_CONJUNCTION']==expected_ids and [x['PREDICATE_ID'] for x in profile['PREDICATES']]==expected_ids
 assert all(x['UNKNOWN_OR_FALSE_RESULT']=='DENY_ACTIVATION' for x in profile['PREDICATES'])
 assert profile['PHASE_GUARDS']['NATIVE_SYNTHETIC_TEST']==expected_ids and profile['PHASE_GUARDS']['FINAL_SEAL']==expected_ids
 assert 'EP70-PHASE' not in profile['PHASE_GUARDS']['FAKE_PROTOCOL_TEST'] and 'EP70-FIXTURE' not in profile['PHASE_GUARDS']['TRUSTED_METADATA_PREFLIGHT']
 assert profile['PHASE_GUARDS']['CONSTRUCTION']==['EP70-GRANT','EP70-ACTOR','EP70-PATHS','EP70-AUDIT']
 assert profile['TEMPORAL_GATES']['READER_LAUNCH_REQUIRED_RUNTIME_FACTS']==['SUPERVISOR_OBSERVED_OWN_CHILD_EXIT_ZERO','EXACT_IMMUTABLE_PUBLICATION_VERIFIED','EXACT_PERSISTED_HANDOFF_VERIFIED']
 assert profile['ACTIVATION_EVALUATION_RULE']['UNKNOWN_POLICY']=='DENY' and profile['ACTIVATION_EVALUATION_RULE']['PHASE_NOT_LISTED']=='DENY' and profile['ACTIVATION_EVALUATION_RULE']['NATIVE_CALLED_IN_PREFLIGHT_OR_FAKE_PHASE'] is False
 limits=profile['RESOURCE_LIMITS'];assert limits['AUTOMATIC_RETRIES']==0 and limits['MAX_LIVE_CHILDREN']==4 and limits['MAX_CHILD_LAUNCHES_PER_APPROVED_CAMPAIGN']==128
 assert limits['MAX_CHILD_WALL_SECONDS']==60 and limits['MAX_CAMPAIGN_WALL_SECONDS']==600 and limits['CHILD_CPU_SECONDS']==30
 assert limits['CHILD_ADDRESS_SPACE_BYTES']==1073741824 and limits['CHILD_FILE_BYTES']==16777216 and limits['MAX_CAMPAIGN_WRITTEN_BYTES']==67108864 and limits['CHILD_OPEN_FILE_DESCRIPTORS']==64
 assert limits['STATUS']=='PROPOSED_AUTHORIZATION_LIMITS_NOT_OBSERVED_RESOURCE_PERMISSIONS'
 paths=profile['INPUT_OUTPUT_PATH_SELECTION'];assert paths['SRC_PATHS']==required_files and paths['RESOURCE_PRIVILEGES_CREATED'] is False
 assert paths['EVIDENCE_ROOT']=='docs/plans/qualification/A15_HARNESS_IMPLEMENTATION_QUALIFICATION_1'
 assert paths['VARIANT_KEYS']==['SYNTHETIC-ONE','SYNTHETIC-TWO'] and paths['ORIGINAL_RUNTIME_DENIED']=='docs/plans/qualification/A15_PROSPECTIVE_SCENARIO_1_RUNTIME'
 assert not (Q/'A15_HARNESS_IMPLEMENTATION_QUALIFICATION_1').exists() and not (Q/'A15_PROSPECTIVE_SCENARIO_1_RUNTIME').exists()
 for p in profile['DEPENDENCY_VERSIONS']['NATIVE_IMPLEMENTATION_SOURCE_PINS']:assert sha(R/p['PATH'])==p['RAW_SHA256']
 bp=profile['DEPENDENCY_VERSIONS']['BWRAP_BINARY_PIN'];assert sha(pathlib.Path(bp['PATH']))==bp['RAW_SHA256']
 proc=c['process-isolation-persistence-controls.json'];assert proc['WORKER_SELF_CERTIFIES_EXIT'] is False and proc['HANDOFF_IS_EXIT_PROOF'] is False and proc['CROSS_VARIANT_STATE_REUSE'] is False
 assert proc['INPUTS_READ_ONLY'] and proc['OUTPUT_ROWS_DISTINCT'] and not proc['HEAD_MUTATION'] and not proc['GENERAL_CRASH_DURABILITY_CLAIM']
 assert proc['PER_SUCCESS_CASE']=={'SUPERVISORS':1,'WRITERS':2,'FRESH_READERS_PER_VARIANT':4,'READER_HASH_SEEDS':[0,1,7,101],'WRITER_HASH_SEED':0}
 fail=c['failure-retry-controls.json'];basefail=load(C/'failure-retry-matrix.json')
 assert fail['AUTOMATIC_RETRY'] is False and fail['AUTHORIZED_RETRY_COUNT']==0
 for p,x in zip(fail['MAPPING'],basefail):assert p['RETAINED_NATIVE_RULE']==x and p['PROPOSED_AUTHORIZED_RETRIES']==0 and p['AUTO_RETRY'] is False
 assert len(fail['MAPPING'])==len(basefail)+5
 accept=c['implementation-qualification-acceptance.json'];assert accept['NO_A15_ACCEPTANCE_PASS_FROM_SYNTHETIC_TESTS'] and accept['NO_REAL_A15_EXECUTION_AUTHORITY_FROM_TEST_PASS']
 assert set(accept['CRITERIA'])=={'SUPERVISOR_CORRECTNESS','WORKER_CORRECTNESS','PROCESS_ISOLATION','CAPTURE_CORRECTNESS','PERSISTENCE_CORRECTNESS','COLD_READER_CORRECTNESS','FAILURE_HANDLING','DETERMINISM','EXECUTABLE_IDENTITY','ENVIRONMENT_PROFILE'}
 assert b['MANDATE']=='BOUNDED_QUALIFICATION_ADAPTER_IMPLEMENTATION_AND_CONDITIONAL_SYNTHETIC_NATIVE_TEST_EVIDENCE_ONLY'
 assert 'real A15 execution/capture grants' in b['HISTORICAL_EXCLUSIONS'] and 'general engineering/production/external/government authority or security bypass' in b['HISTORICAL_EXCLUSIONS']
 interpretation=c['authority-interpretation.json'];assert interpretation['NO_AUTHORITY_SELF_ISSUANCE'] and interpretation['NO_GRANT_ISSUED'] and interpretation['PRIVILEGES_CREATED'] is False
 assert len(interpretation['PHASE_ORDER'])==5
 # Exhaustive abstract safety proof of the guard conjunction; hypothetical facts are not OS evidence or authority.
 accepted=0
 for bits in itertools.product([False,True],repeat=len(expected_ids)):
  facts=dict(zip(expected_ids,bits));enabled=phase_enable(profile,'NATIVE_SYNTHETIC_TEST',facts)
  assert enabled==all(bits);accepted+=int(enabled)
 assert accepted==1
 for bad in [None,'true','YES',1,False]:
  f=dict.fromkeys(expected_ids,True);f['EP70-GRANT']=bad;assert not phase_enable(profile,'NATIVE_SYNTHETIC_TEST',f)
 assert not phase_enable(profile,'REAL_A15_EXECUTION',dict.fromkeys(expected_ids,True))
 assert not phase_enable(profile,'NATIVE_SYNTHETIC_TEST',{})
 for p in [D/'prepare.py',D/'verify.py']:
  for n in ast.walk(ast.parse(p.read_text())):
   if isinstance(n,ast.Import):assert all(not x.name.startswith('adapter') for x in n.names)
   if isinstance(n,ast.ImportFrom):assert not (n.module or '').startswith('adapter')
 return {'RESULT':'PASS_CONDITIONAL_AUTHORITY_SUBJECT','SUBJECT_IDENTITY':s['IDENTITY'],'IMPLEMENTATION_SCOPE_COMPLETE':'YES','SYNTHETIC_TEST_SCOPE_COMPLETE':'YES','ENVIRONMENT_RESOURCE_BOUNDARY_COMPLETE':'YES (exact fail-closed phase predicates; not a sealed future test environment)','IMPLEMENTATION_TEST_DECISION_READY':'YES','ACTUAL_TEST_ENTRY_PROFILE_SEALED':'NO','TESTS_EXECUTED':0,'NATIVE_OPERATIONS':0,'SOURCE_SCOPE_HASH':canon(scope),'SYNTHETIC_SCOPE_HASH':canon(fixture),'RESOURCE_PROFILE_HASH':canon(profile),'PROCESS_HASH':canon(proc),'FAILURE_HASH':canon(fail),'ABSTRACT_NATIVE_GUARD_ASSIGNMENTS':2048,'ASSIGNMENTS_ENABLING_NATIVE_TEST':1,'REAL_A15_EXECUTION_AUTHORIZED':False,'GRANT_ISSUED':False,'ENTRY_GATE':ep}
if __name__=='__main__':print(json.dumps(verify(json.load(sys.stdin) if '--candidate' in sys.argv else None),sort_keys=True,ensure_ascii=False))
