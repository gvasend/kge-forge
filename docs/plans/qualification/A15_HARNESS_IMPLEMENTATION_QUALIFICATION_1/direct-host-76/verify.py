"""Independent metadata reconstruction; never imports or executes adapter code."""
import ast,copy,hashlib,json,pathlib,sys
D=pathlib.Path(__file__).resolve().parent;E=D.parent;R=D.parents[4];Q=R/'docs/plans/qualification'
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def encode(x):return ''.join(json.JSONEncoder(sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).iterencode(x)).encode()
def ident(x,ns):return {'kind':'CONTENT_IDENTITY','namespace':ns,'sha256':hashlib.sha256(encode(x)).hexdigest()}
def verify(overrides=None):
 overrides=overrides or {}
 def read(n):return copy.deepcopy(overrides[n]) if n in overrides else load(D/n)
 for item in read('input-authentication.json')['INDICES']:
  p=R/item['PIN']['PATH'];assert sha(p)==item['PIN']['RAW_SHA256'];idx=load(p);assert len(idx['FILES'])==item['VERIFIED_FILES'];assert all(sha(R/f)==h for f,h in idx['FILES'].items())
 probe=read('direct-host-probe-evidence.json')
 assert probe['HOST_NAME']=='ubuntu01' and probe['OPERATING_SYSTEM']=='Ubuntu 20.04.6 LTS' and probe['KERNEL_VERSION']=='5.4.0-216-generic' and probe['BUBBLEWRAP_VERSION']=='0.4.0'
 assert probe['SOURCE_PROVENANCE']['KIND']=='CURRENT_USER_SUPPLIED_HOST_CAPABILITY_OBSERVATION' and probe['INDEPENDENT_REPRODUCTION_PERFORMED'] is False and probe['HOST_QUALIFIED'] is False
 assert probe['OBSERVATION_TIME_IF_AVAILABLE'] is None and probe['USER_SUPPLIED_COMMAND_HASH'] is None and probe['HOST_ATTESTATION_IDENTITY'] is None
 assert probe['DECLARED_PARENT_SECURITY']=={'NoNewPrivs':0,'Seccomp':0,'CapEff':0}
 assert probe['OBSERVED_OUTPUT']=='BWRAP_OK\nuid=1000 gid=1000 groups=1000,65534\nNoNewPrivs:     1\nSeccomp:        0'
 assert all(flag in probe['COMMAND'] for flag in ['--unshare-user','--unshare-pid','--unshare-net','--tmpfs /tmp'])
 compare=read('execution-context-comparison.json');assert compare['CONTEXTS_EQUIVALENT'] is False and compare['DIRECT_SUCCESS_IDENTIFIES_CODEX_DENY_RULE'] is False
 assert compare['CODEX_MANAGED']['COMPATIBILITY']=='UNDETERMINED' and compare['DIRECT_HOST']['PARENT_SECCOMP']==0 and compare['DIRECT_HOST']['RESOURCE_CONTRACT_QUALIFIED'] is False
 p70=Q/'E2_P05_D01_A15_IMPLEMENTATION_TEST_AUTHORITY_70';subject=load(p70/'implementation-test-authority-subject.json');limits=subject['CONTENT']['CONTRACTS']['environment-resource-permission-contract.json']['RESOURCE_LIMITS']
 resources=read('resource-enforcement-matrix.json');assert resources['APPROVED_LIMITS']==limits and len(resources['ROWS'])==10 and not resources['RESOURCE_ENFORCEMENT_READY'] and not resources['CGROUP_V2_DELEGATION_ASSUMED'] and not resources['PROBE_SUCCESS_SUBSTITUTED_FOR_LIMIT_EVIDENCE']
 for row in resources['ROWS']:assert row['APPROVED_CEILING']==limits[row['CONTROL_ID']] and row['CURRENT_STATUS']=='UNDETERMINED'
 controls=read('direct-host-confinement-controls.json');assert len(controls['ROWS'])==11 and controls['QUALIFICATION_TESTS_PERFORMED']==0 and not controls['COMPLETE_CONFINEMENT_QUALIFIED']
 assert all(row['CURRENT_STATUS'] in ['PARTIAL','UNDETERMINED'] for row in controls['ROWS'])
 grant=read('effective-grant-reconciliation.json');p71=Q/'E2_P05_D01_A15_IMPLEMENTATION_TEST_GRANT_ISSUANCE_71';ef=load(p71/'effective-implementation-test-grant-reference.json');record=load(R/ef['GRANT_RECORD_PIN']['PATH'])
 assert record['GRANT_IDENTITY']['sha256']==hashlib.sha256(encode(record['RECORD'])).hexdigest()=='25395fb3c06be58a8c538c618b9e50b9d118aa415d0843968254d3f8e83dd8fa'
 assert grant['GRANT_IDENTITY']==record['GRANT_IDENTITY'] and grant['APPROVED_SUBJECT_IDENTITY']==subject['IDENTITY'] and grant['GRANT_IDENTITY']!=subject['IDENTITY']
 assert grant['RESOURCE_LIMITS']==limits and grant['NEW_CAMPAIGN_ALLOWED_BY_OLD_REFERENCE_ALONE'] is False
 stopped=read('stopped-campaign-reconciliation.json');ledger=E/'campaign-budget.jsonl'
 assert stopped['STOPPED'] is True and stopped['JOURNAL_REOPENED_OR_APPENDED'] is False and stopped['CURRENT_CAMPAIGN_ACTIVE'] is False
 assert stopped['CAMPAIGN_IDENTITY']['sha256']==sha(ledger) and stopped['STOPPED_JOURNAL_PIN']['RAW_SHA256']==sha(ledger)
 assert json.loads(ledger.read_text().splitlines()[-1])['kind']=='stop' and stopped['AUTOMATIC_RETRIES']==stopped['FAKE_PROTOCOL_TESTS']==stopped['NATIVE_SYNTHETIC_TESTS']==stopped['ACTUAL_A15']==0
 # Independently rebuild every exact fake record from supplied synthetic premises,
 # not from primary encoder output or executing the worker.
 manifest=read('synthetic-fixture-manifest.json');assert len(manifest['VARIANTS'])==2 and not manifest['REAL_A15_EXECUTION_INPUTS_USED'] and not manifest['REAL_A15_ORACLES_USED'] and not manifest['EXECUTION_BINDINGS_SEALED']
 source_tree=ast.parse((R/'adapter/qualification_a15/contracts.py').read_text());literal=next(n.value for n in source_tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='PAYLOADS' for t in n.targets));fields=ast.literal_eval(literal)
 roles={'WORKER_REQUEST':'WORKER','PUBLISHED_OUTPUT':'WORKER','HANDOFF_RECORD':'WORKER','WORKER_RESULT':'WORKER','READER_REQUEST':'READER','READER_RESULT':'READER','SUPERVISOR_REQUEST':'SUPERVISOR','SUPERVISOR_RESULT':'SUPERVISOR'}
 base_grant={'kind':'CONTENT_IDENTITY','namespace':record['GRANT_IDENTITY']['namespace'],'sha256':record['GRANT_IDENTITY']['sha256']}
 def build(kind,payload):
  assert set(payload)==fields[kind]
  b=dict(schema='KGE-A15-'+kind+'-1',version=1,role=roles[kind],phase='FAKE_PROTOCOL',grant_identity=base_grant,payload=payload)
  return dict(b,identity=ident(b,'qualification-a15-protocol-'+kind.lower()+'-v1'))
 req_ids=[];variant_results=[];synthetic_ids=[]
 denied=subject['CONTENT']['CONTRACTS']['synthetic-fixture-contract.json']['REAL_INPUT_DENYLIST']
 real_hashes={denied['INITIAL_SNAPSHOT_IDENTITY']['sha256'],denied['INITIAL_BUNDLE_IDENTITY']['sha256']}
 for key in ['RETAINED_SOURCE_IDENTITIES','RETAINED_EVENT_IDENTITIES','INVALIDATION_CONTENT_IDENTITIES','INVALIDATION_EVENT_IDENTITIES','AFTER_SNAPSHOT_IDENTITIES','AFTER_BUNDLE_IDENTITIES']:real_hashes.update(x['sha256'] for x in denied[key])
 for descriptor in manifest['VARIANTS']:
  name=descriptor['VARIANT_ID'];packet=read('fixtures/'+name+'.json');fixture=packet['FIXTURE'];oracle=read('expected/'+name+'.json')
  assert name in ['SYNTHETIC-ONE','SYNTHETIC-TWO'] and fixture['variant_id']==name and fixture['scope']=='KGE-FORGE-A15-SYNTHETIC-IMPLEMENTATION-QUALIFICATION'
  initial={'scope':fixture['scope'],'support_current':True,'protected':{'fixture_history':'FAKE_IMMUTABLE'}};assert fixture['initial_state']==initial
  text='SYNTHETIC-A15-TEST:INDEPENDENT-FAKE-SOURCE:'+name;assert fixture['source_content']==text
  source=dict(kind='CONTENT_IDENTITY',namespace='raw-file-sha256',sha256=hashlib.sha256(text.encode()).hexdigest());initial_id=ident(initial,'qualification-a15-fake-snapshot-v1')
  assert fixture['source_identity']==source and fixture['initial_snapshot_identity']==initial_id
  request=build('WORKER_REQUEST',dict(case_id='T70-CAPTURE',variant_id=name,initial_snapshot_identity=initial_id,source_identity=source,operation='FAKE_RECORD_SAVE'));assert packet['REQUEST']==request
  assert packet['FIXTURE_ID']==ident(fixture,'qualification-a15-fake-fixture-content-v1')==descriptor['FIXTURE_ID']
  req_ids.append(request['identity'])
  after={'scope':fixture['scope'],'support_current':False,'protected':initial['protected']}
  event=ident(dict(initial=initial_id,source=source,variant=name),'qualification-a15-fake-event-v1')
  out=build('PUBLISHED_OUTPUT',dict(request_identity=request['identity'],initial_snapshot_identity=initial_id,source_identity=source,event_identity=event,after_snapshot_identity=ident(after,'qualification-a15-fake-snapshot-v1'),typed_state=after,proof_validation='FAKE_STALE',proof_usability=False,target_satisfaction=False,admission_stale='FAKE_CURRENT_VALIDATION_WITHDRAWN',control='FAKE_BLOCKED',resume=dict(allowed=False,actions=[],reasons=['FAKE_SUPPORT_WITHDRAWN'],supporting_identities=[]),ordered_trace=['FAKE_RESTORE','FAKE_RECORD_RESULT','FAKE_SAVE'],protected_state=initial['protected']))
  handoff=build('HANDOFF_RECORD',dict(request_identity=request['identity'],published_output_identity=out['identity'],publication_bytes_sha256=hashlib.sha256(encode(out)).hexdigest()))
  worker=build('WORKER_RESULT',dict(request_identity=request['identity'],published_output_identity=out['identity'],handoff_identity=handoff['identity']))
  readers=[]
  for seed in [0,1,7,101]:
   rq=build('READER_REQUEST',dict(case_id='T70-CAPTURE',variant_id=name,published_output_identity=out['identity'],expected_output_identity=out['identity'],seed=seed));rr=build('READER_RESULT',dict(request_identity=rq['identity'],published_output_identity=out['identity'],expected_output_identity=out['identity'],matched=True));readers.append({'SEED':seed,'REQUEST':rq,'RESULT':rr})
  assert oracle['EXPECTED_OUTPUT']=={'PUBLISHED_OUTPUT':out,'HANDOFF_RECORD':handoff,'WORKER_RESULT':worker,'READERS':readers}
  assert oracle['EXPECTED_CANONICAL_PUBLICATION_SHA256']==hashlib.sha256(encode(out)).hexdigest() and oracle['ACTUAL_RESULT_OBSERVED'] is False
  variant_results.append({'worker':worker,'readers':[x['RESULT'] for x in readers]})
  for idval in [source,initial_id,event,out['identity'],worker['identity'],packet['FIXTURE_ID']]:assert idval['sha256'] not in real_hashes;synthetic_ids.append(idval)
  for key in ['FIXTURE_PIN','EXPECTED_PIN']:assert sha(R/descriptor[key]['PATH'])==descriptor[key]['RAW_SHA256']
 super_req=build('SUPERVISOR_REQUEST',dict(case_id='T70-CAPTURE',variant_requests=req_ids));super_result=build('SUPERVISOR_RESULT',dict(request_identity=super_req['identity'],variant_results=variant_results))
 assert manifest['SUPERVISOR_REQUEST']==super_req and manifest['EXPECTED_SUPERVISOR_RESULT']==super_result
 assert manifest['VARIANTS'][0]['INITIAL_SNAPSHOT_ID']==manifest['VARIANTS'][1]['INITIAL_SNAPSHOT_ID'] and manifest['VARIANTS'][0]['SOURCE_ID']!=manifest['VARIANTS'][1]['SOURCE_ID']
 profile=read('direct-host-profile-assessment.json');assert not profile['DIRECT_HOST_PROFILE_SEALED'] and not profile['RESOURCE_ENFORCEMENT_READY'] and profile['ACTUAL_RESOURCE_PERMISSION_EVIDENCE'] is None and profile['UNIQUE_ATTESTED_HOST_RUNTIME_IDENTITY'] is None and not profile['CODEX_PROBE_REUSED_AS_DIRECT_HOST_ENFORCEMENT']
 exe=read('executable-identity-manifest.json');assert exe['SOURCE_HASHES']==load(E/'pretest-source-seal.json')['SOURCE_FILE_HASHES'] and all(sha(R/f)==h for f,h in exe['SOURCE_HASHES'].items())
 assert exe['CODE_BYTES_SEALED'] and not exe['EXECUTABLE_IDENTITY_QUALIFIED'] and not exe['EXACT_EXECUTION_PROFILE_SEALED'] and not exe['ADAPTER_EXECUTED']
 authority=read('fresh-campaign-authority-prerequisites.json');assert authority['EFFECTIVE_IMPLEMENTATION_TEST_GRANT']==record['GRANT_IDENTITY'] and authority['PREDECESSOR_STOPPED_CAMPAIGN']==stopped['CAMPAIGN_IDENTITY']
 assert authority['OUTPUT_BOUNDARY'] is None and authority['RESOURCE_LIMITS']==limits and authority['RETRY_POLICY']['AUTOMATIC_RETRIES']==0 and authority['NO_NEW_CAMPAIGN_AUTHORITY_ISSUED'] and not authority['FRESH_CAMPAIGN_DECISION_READY'] and not authority['ACTUAL_A15_INCLUDED'] and authority['DECISION_OPTIONS']==[]
 gates=read('readiness-gates.json');assert gates['DIRECT_HOST_PROBE']=='PASS_USER_SUPPLIED' and gates['CODEX_CONTEXT_COMPATIBILITY']=='UNDETERMINED'
 for key in ['FRESH_CAMPAIGN_DECISION_READY','DIRECT_HOST_PROFILE_SEALED','RESOURCE_ENFORCEMENT_READY','FAKE_PROTOCOL_TEST_READY','NATIVE_SYNTHETIC_TEST_READY']:assert gates[key]=='NO'
 assert gates['INDEPENDENT_FAKE_ORACLES_COMPLETE'].startswith('NO for executable campaign;')
 return {'RESULT':'PASS_STATIC_PARTIAL_DIRECT_HOST_ASSESSMENT','USER_PROBE_AUTHENTICATION':'PASS_CAPTURED_PROVENANCE_NOT_REPRODUCED','ISSUED_GRANT_IDENTITY':record['GRANT_IDENTITY'],'STOPPED_CAMPAIGN_IDENTITY':stopped['CAMPAIGN_IDENTITY'],'SYNTHETIC_IDENTITIES':synthetic_ids,'EXPECTED_SUPERVISOR_RESULT_IDENTITY':super_result['identity'],'SOURCE_HASHES':exe['SOURCE_HASHES'],'CONTROL_MATRIX_HASH':hashlib.sha256(encode(resources)).hexdigest(),'DIRECT_HOST_PROFILE_HASH':hashlib.sha256(encode(profile)).hexdigest(),'READINESS':gates,'ADAPTER_OR_HOST_TESTS_EXECUTED':0}
if __name__=='__main__':print(json.dumps(verify(json.load(sys.stdin) if '--candidate' in sys.argv else None),sort_keys=True))
