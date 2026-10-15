"""Exclusive documentary grant publication only. No construction/native/test effects."""
import copy,datetime,hashlib,importlib.util,json,os,pathlib,subprocess,sys,tempfile
D=pathlib.Path(__file__).resolve().parent;R=D.parents[3];Q=R/'docs/plans/qualification';P=Q/'E2_P05_D01_A15_IMPLEMENTATION_TEST_AUTHORITY_70'
spec=importlib.util.spec_from_file_location('independent_grant_verifier',D/'verify.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
WP='E2-P05-D01-A15-IMPLEMENTATION-TEST-GRANT-ISSUANCE-71'
def publish(name,x):
 path=D/name;assert not path.exists() and not path.is_symlink(),path
 raw=x.encode() if isinstance(x,str) else (json.dumps(x,sort_keys=True,indent=2,ensure_ascii=False)+'\n').encode()
 fd,tmp=tempfile.mkstemp(prefix='.grant-publication-',dir=str(D))
 try:
  with os.fdopen(fd,'wb') as stream:stream.write(raw);stream.flush();os.fsync(stream.fileno())
  os.link(tmp,path);os.unlink(tmp)
  fd=os.open(str(D),os.O_RDONLY|os.O_DIRECTORY)
  try:os.fsync(fd)
  finally:os.close(fd)
  assert path.read_bytes()==raw
 finally:
  if os.path.exists(tmp):os.unlink(tmp)
 return path
subject,dossier,qualified=v.inputs();c=subject['CONTENT']['CONTRACTS'];env=c['environment-resource-permission-contract.json']
before={}
for base in ['adapter','docs','rust']:
 if not (R/base).exists():continue
 for path in (R/base).rglob('*'):
  if path.is_file() and D not in path.parents and '__pycache__' not in path.parts:before[str(path.relative_to(R))]=v.sha(path)
publish('preservation-before.json',before)
publish('exact-subject-verification.json',{'RESULT':'PASS','SUBJECT_IDENTITY':subject['IDENTITY'],'SUBJECT_PIN':v.pin(P/'implementation-test-authority-subject.json'),'DECISION_DOSSIER_PIN':v.pin(P/'unselected-implementation-test-decision-dossier.json'),'QUALIFICATION_RECONSTRUCTION':qualified,'OLD_SUBJECT_AND_DOSSIER_UNCHANGED':True})
publish('effective-charter-normative-verification.json',{'RESULT':'PASS','GOVERNING_CHARTER':subject['CONTENT']['GOVERNING_CHARTER'],'EFFECTIVE_CHARTER_LIFECYCLE':subject['CONTENT']['EFFECTIVE_CHARTER_LIFECYCLE'],'CHARTER_EFFECTIVE':'YES','NORMATIVE_MANDATE_EFFECTIVE':'YES','NORMATIVE_REFERENCE_PIN':subject['CONTENT']['EFFECTIVE_NORMATIVE_REFERENCE_PIN'],'ADOPTION_RECORD_PIN':subject['CONTENT']['NORMATIVE_ADOPTION_RECORD_PIN'],'ISSUER_ROLE':subject['CONTENT']['ISSUER_ROLE'],'METHOD':'Package70 read-only independent reader -> Package68 effective-reference reader -> ordered Package66 documentary lifecycle reader; no native restore'})
source='''# KGE-Forge — A15 Implementation/Test Grant Issuance 71

Provenance: current conversation user-role instruction, authority and exclusions excerpt. No personal credential, signature, transport message ID or approval timestamp is invented.

## 1. Authority
The project owner explicitly selected:
AUTHORIZE_BOUNDED_A15_ADAPTER_IMPLEMENTATION_SYNTHETIC_TEST

Exact approved subject:
CONTENT_IDENTITY/qualification-A15-implementation-synthetic-test-authority-subject-v1:a2505f248e929f0226d20d813673faa87b8b09fa0e08b071e413d4d7779a9869
Governing charter:
CONTENT_IDENTITY/kge-forge-qualification-governance-charter-v1:d26962c58f17281173e965433dae63a941e078115f3dcc30e2a3512fa21812b8
Effective charter lifecycle:
CONTENT_IDENTITY/kge-forge-charter-lifecycle-record-v1:a27516baa0ab7f34a36a1130490b6cfa38c508975ca337e0824c8eac33715cbb

The authorization permits only bounded adapter construction and phase-gated synthetic testing, subject to effective grant issuance and all applicable entry predicates.

## 2. Objective
Record, persist, and independently verify the exact project-owner implementation/test grant.
Do not construct the adapter or run synthetic tests during issuance.

## Resource ceilings (user-authorized values)
Maximum live children: 4
Maximum launches per campaign: 128
Child wall time: 60 seconds
Child CPU time: 30 seconds
Child address space: 1 GiB
Child file size: 16 MiB
Child open descriptors: 64
Campaign wall time: 600 seconds
Campaign written bytes: 64 MiB
Automatic retries: 0
These limits are authorization ceilings, not proof of enforceability.

## 8. Explicit exclusions
The grant does not authorize:
- Actual A15 checkpoint or variant execution.
- Actual A15 apply_event or record_result.
- A15 capture, save, restore, or replay.
- Modification of native Planner runtime, V3, or frozen acceptance.
- Modification of historical proof/admission evidence.
- E1 changes.
- Production or external-system access.
- New campaigns or automatic retries.
- Self-issuance or scope expansion.
Synthetic qualification results must not be treated as A15 acceptance evidence.

## Issuance constraint
Mark the grant effective only after all required checks pass. If any check fails, stop and preserve the last valid state.
Do not begin construction until the issued grant is independently verified and the construction-phase guard passes.
Do not begin native synthetic testing until fake-protocol qualification and all eleven test-entry predicates pass.
Do not execute actual A15 qualification variants.
'''
sourcepath=publish('project-owner-approval-source.txt',source)
dc={'SCHEMA_ID':'A15-OWNER-IMPLEMENTATION-TEST-DECISION-71-1','SOURCE_KIND':'CURRENT_CONVERSATION_USER_MESSAGE','SOURCE_PIN':v.pin(sourcepath),'SELECTION':v.OPTION,'APPROVED_SUBJECT_IDENTITY':subject['IDENTITY'],'GOVERNING_CHARTER':subject['CONTENT']['GOVERNING_CHARTER'],'EFFECTIVE_CHARTER_LIFECYCLE':subject['CONTENT']['EFFECTIVE_CHARTER_LIFECYCLE'],'ISSUER_ROLE':subject['CONTENT']['ISSUER_ROLE'],'DECISION_DOSSIER_PIN':v.pin(P/'unselected-implementation-test-decision-dossier.json'),'AUTHORIZATION_SCOPE':'Exact approved conditional implementation/test subject only; issuance now, no construction/tests in Package71','PERSONAL_SIGNATURE_OR_EXTERNAL_CREDENTIAL_ASSERTED':False}
decision={'IDENTITY':v.aid('qualification-A15-owner-implementation-test-decision-v1',dc),'CONTENT':dc}
publish('project-owner-decision.json',decision)
publish('preissuance-conflict-audit.json',v.conflicts())
owner_decl=v.read(Q/'KGE_FORGE_QUALIFICATION_GOVERNANCE_CHARTER_65/charter-content.json')['GOVERNING_AUTHORITY']['DECLARATION_PIN']
body={'SCHEMA_ID':'A15-IMPLEMENTATION-TEST-ISSUED-GRANT-71-1','WORK_PACKAGE':WP,'INSTRUMENT_STATUS':'ISSUANCE_RECORDED_PENDING_INDEPENDENT_EFFECTIVENESS_VERIFICATION','APPROVED_SUBJECT_IDENTITY':subject['IDENTITY'],'APPROVED_SUBJECT_PIN':v.pin(P/'implementation-test-authority-subject.json'),'ISSUER_ROLE':subject['CONTENT']['ISSUER_ROLE'],'ISSUER_AUTHORITY_EVIDENCE':{'OWNER_DECLARATION_PIN':owner_decl,'EFFECTIVE_CHARTER_REFERENCE_PIN':v.pin(Q/'KGE_FORGE_QUALIFICATION_GOVERNANCE_CHARTER_ADOPTION_66/effective-charter-reference.json'),'DIRECT_ROLE':'No delegation or personal signature invented'},'GOVERNING_CHARTER_IDENTITY':subject['CONTENT']['GOVERNING_CHARTER'],'EFFECTIVE_CHARTER_LIFECYCLE_IDENTITY':subject['CONTENT']['EFFECTIVE_CHARTER_LIFECYCLE'],'NORMATIVE_MANDATE_REFERENCE':{'SUBJECT_IDENTITY':subject['CONTENT']['NORMATIVE_SUBJECT'],'EFFECTIVE_REFERENCE_PIN':subject['CONTENT']['EFFECTIVE_NORMATIVE_REFERENCE_PIN'],'ADOPTION_RECORD_PIN':subject['CONTENT']['NORMATIVE_ADOPTION_RECORD_PIN'],'VERIFICATION_STATUS':'YES; normative-only, not implementation permission'},'PROJECT_OWNER_DECISION_EVIDENCE':{'IDENTITY':decision['IDENTITY'],'PIN':v.pin(D/'project-owner-decision.json')},'PERMITTED_SOURCE_FILES':c['source-file-scope.json']['PERMITTED_SOURCE_FILES'],'PERMITTED_TESTS':c['permitted-test-inventory.json'],'RESOURCE_LIMITS':env['RESOURCE_LIMITS'],'PHASE_GATES':env['PHASE_GUARDS'],'TEST_ENTRY_PREDICATES':env['PREDICATES'],'TEST_ENTRY_ACTIVATION_RULE':env['ACTIVATION_EVALUATION_RULE'],'TEMPORAL_GATES':env['TEMPORAL_GATES'],'ENVIRONMENT_CONTRACT':env,'SYNTHETIC_FIXTURE_CONTRACT':c['synthetic-fixture-contract.json'],'FAILURE_RETRY_CONTROLS':c['failure-retry-controls.json'],'PROCESS_ISOLATION_PERSISTENCE_CONTROLS':c['process-isolation-persistence-controls.json'],'IMPLEMENTATION_QUALIFICATION_ACCEPTANCE':c['implementation-qualification-acceptance.json'],'EVIDENCE_BOUNDARY':env['INPUT_OUTPUT_PATH_SELECTION']['EVIDENCE_ROOT'],'HISTORICAL_EXCLUSIONS':subject['CONTENT']['HISTORICAL_EXCLUSIONS'],'EFFECTIVE_BOUNDARY':'Only after exclusive publication, independent persisted reread, four-seed agreement, all negative controls and prior-artifact preservation verification, followed by separately persisted effective reference. No backdating; future operations additionally require corresponding entry/temporal gates.','REVOCATION_RULE':subject['CONTENT']['GRANT_TERMINATION_RULE'],'MANDATE':subject['CONTENT']['MANDATE'],'A15_EXECUTION_GRANT':None,'A15_CAPTURE_GRANT':None,'PREDECESSOR_IMPLEMENTATION_TEST_GRANT':None,'SCOPE_EXPANSION_ALLOWED':False,'EXPLICIT_PACKAGE71_EXCLUSIONS':['Actual A15 checkpoint or variant execution','Actual A15 apply_event or record_result','Actual A15 capture/save/restore/replay','Native Planner runtime/V3/frozen acceptance modification','Historical proof/admission evidence modification','E1 changes','Production or external-system access','New campaigns or automatic retries','Self-issuance or scope expansion'],'APPROVED_LIMITS_INTERPRETATION':'Exact approved caps become authorization ceilings only; copied proposed-status metadata does not prove enforcement or resource permissions','IDENTITY_RULE':'Canonical sorted compact UTF-8 JSON RECORD digest; own wrapper, future effectiveness/verification records and generated code/fixture/profile results excluded','CAMPAIGN_STARTED_BY_ISSUANCE':False}
grant={'GRANT_IDENTITY':v.aid(v.NS,body),'RECORD':body}
pre=json.loads(subprocess.check_output([sys.executable,str((D/'verify.py').relative_to(R)),'--candidate'],input=json.dumps(grant).encode(),cwd=str(R)))
publish('prepublication-record-verification.json',pre)
grantpath=publish('issued-implementation-test-grant-'+grant['GRANT_IDENTITY']['sha256']+'.json',grant)
post=json.loads(subprocess.check_output([sys.executable,str((D/'verify.py').relative_to(R))],cwd=str(R)))
publish('independent-persisted-record-verification.json',post)
seeds=[]
for seed in [0,1,7,101]:
 out=json.loads(subprocess.check_output([sys.executable,str((D/'verify.py').relative_to(R))],cwd=str(R),env=dict(os.environ,PYTHONHASHSEED=str(seed),PYTHONDONTWRITEBYTECODE='1')))
 assert out==post
 seeds.append({'PYTHONHASHSEED':seed,'RESULT':'PASS','SEMANTIC_SHA256':v.canonical(out)})
publish('four-seed-determinism.json',{'RESULT':'PASS','FRESH_DOCUMENTARY_RECONSTRUCTIONS':4,'SEEDS':seeds,'NO_ADAPTER_OR_SYNTHETIC_TEST_OPERATIONS':True})
controls=[]
def reject(name,mutator=None,dec_mutator=None,duplicates=1,identity_mutator=None):
 g=copy.deepcopy(grant);d=copy.deepcopy(decision)
 if mutator:mutator(g['RECORD']);g['GRANT_IDENTITY']=v.aid(v.NS,g['RECORD'])
 if dec_mutator:dec_mutator(d['CONTENT']);d['IDENTITY']=v.aid('qualification-A15-owner-implementation-test-decision-v1',d['CONTENT'])
 if identity_mutator:identity_mutator(g)
 try:v.verify(g,d,subject,dossier,duplicate_count=duplicates)
 except (AssertionError,KeyError,ValueError):controls.append({'CONTROL':name,'RESULT':'REJECTED','NATIVE_OR_SYNTHETIC_TEST_EXECUTED':False});return
 raise RuntimeError('Accepted corrupted grant: '+name)
reject('wrong approved subject',lambda b:b['APPROVED_SUBJECT_IDENTITY'].update(sha256='0'*64))
reject('wrong charter identity',lambda b:b['GOVERNING_CHARTER_IDENTITY'].update(sha256='0'*64))
reject('wrong effective lifecycle',lambda b:b['EFFECTIVE_CHARTER_LIFECYCLE_IDENTITY'].update(sha256='0'*64))
reject('wrong owner selected option',dec_mutator=lambda d:d.update(SELECTION='AUTHORIZE_REAL_A15'))
reject('wrong issuer role',lambda b:b.update(ISSUER_ROLE='UNDELEGATED'))
reject('wrong approval provenance pin',dec_mutator=lambda d:d['SOURCE_PIN'].update(RAW_SHA256='0'*64))
reject('wrong subject pin',lambda b:b['APPROVED_SUBJECT_PIN'].update(RAW_SHA256='0'*64))
reject('source allowlist expanded',lambda b:b['PERMITTED_SOURCE_FILES'].append('adapter/planner/core.py'))
reject('test categories omitted',lambda b:b['PERMITTED_TESTS']['TESTS'].pop())
reject('real A15 execution grant inferred',lambda b:b.update(A15_EXECUTION_GRANT={'ISSUED':True}))
reject('real A15 capture grant inferred',lambda b:b.update(A15_CAPTURE_GRANT={'ISSUED':True}))
reject('resource launch cap enlarged',lambda b:b['RESOURCE_LIMITS'].update(MAX_CHILD_LAUNCHES_PER_APPROVED_CAMPAIGN=129))
reject('automatic retries allowed',lambda b:b['RESOURCE_LIMITS'].update(AUTOMATIC_RETRIES=1))
reject('native phase drops permission guard',lambda b:b['PHASE_GATES']['NATIVE_SYNTHETIC_TEST'].remove('EP70-CONFINEMENT'))
reject('predicate unknown treated as allow',lambda b:b['TEST_ENTRY_ACTIVATION_RULE'].update(UNKNOWN_POLICY='ALLOW'))
reject('historical exclusions weakened',lambda b:b.update(HISTORICAL_EXCLUSIONS=[]))
reject('worker self-certified exit',lambda b:b['PROCESS_ISOLATION_PERSISTENCE_CONTROLS'].update(WORKER_SELF_CERTIFIES_EXIT=True))
reject('evidence publication expanded',lambda b:b.update(EVIDENCE_BOUNDARY='docs/experiments/E1'))
reject('duplicate issuance',duplicates=2)
reject('circular predecessor self-issuance',lambda b:b.update(PREDECESSOR_IMPLEMENTATION_TEST_GRANT=grant['GRANT_IDENTITY']))
reject('premature effective state',lambda b:b.update(INSTRUMENT_STATUS='EFFECTIVE'))
reject('wrong canonical grant identity',identity_mutator=lambda g:g['GRANT_IDENTITY'].update(sha256='0'*64))
publish('negative-controls.json',{'RESULT':'PASS','PASSED':len(controls),'TOTAL':len(controls),'CONTROLS':controls,'METHOD':'In-memory grant/decision corruption, independently reidentified except deliberate bad digest; actual persisted records untouched'})
changed=[p for p,h in before.items() if not (R/p).exists() or v.sha(R/p)!=h];assert not changed,changed
original=v.read(Q/'E2_P05_D01_A14_RUNTIME_PERSISTENCE_QUALIFICATION_31/preservation-before.json')
wrong=[p for p,h in original.items() if not (R/p).exists() or v.sha(R/p)!=h];assert not wrong,wrong
assert all(not (R/f).exists() for f in body['PERMITTED_SOURCE_FILES'])
publish('preservation-audit.json',{'RESULT':'PASS','CURRENT_PREEXISTING_FILES_VERIFIED':len(before),'ORIGINAL_A14_FILES_VERIFIED':len(original),'CHANGED_PREEXISTING_FILES':changed,'ADAPTER_FILES_CREATED':0,'SYNTHETIC_TESTS_EXECUTED':0,'NATIVE_OPERATIONS_INVOKED':0,'A14_RERUN':False,'E1_ARTIFACTS_MODIFIED':0,'BASELINE_AMENDED':False,'LESSONS_REGISTER_CHANGED':False,'PRODUCTION_EFFECT':False})
# Effectiveness is a subsequent immutable reference, never a mutation of issuance or Package70.
ef={'SCHEMA_ID':'A15-IMPLEMENTATION-TEST-EFFECTIVE-GRANT-REFERENCE-71-1','GRANT_IDENTITY':grant['GRANT_IDENTITY'],'GRANT_RECORD_PIN':v.pin(grantpath),'APPROVED_SUBJECT_IDENTITY':subject['IDENTITY'],'PROJECT_OWNER_DECISION_IDENTITY':decision['IDENTITY'],'GOVERNING_CHARTER_IDENTITY':body['GOVERNING_CHARTER_IDENTITY'],'EFFECTIVE_CHARTER_LIFECYCLE_IDENTITY':body['EFFECTIVE_CHARTER_LIFECYCLE_IDENTITY'],'IMPLEMENTATION_TEST_GRANT_EFFECTIVE':True,'EFFECTIVE_PUBLICATION_TIME_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'EFFECTIVE_BOUNDARY':'Actual Package71 exclusive publication after authenticated explicit owner approval, persisted-record reread, four-seed agreement, 22 rejected corruptions and complete preservation check; no backdating. Construction/test activation remains separately phase-gated.','PREREQUISITE_PINS':[v.pin(D/n) for n in ['project-owner-decision.json','prepublication-record-verification.json','independent-persisted-record-verification.json','four-seed-determinism.json','negative-controls.json','preservation-audit.json']],'A15_EXECUTION_AUTHORITY_ISSUED':False,'A15_CAPTURE_AUTHORITY_ISSUED':False,'A15_EXECUTED':False,'ADAPTER_CONSTRUCTION_PERFORMED':False,'SYNTHETIC_TESTS_EXECUTED':False,'TEST_CAMPAIGN_STARTED':False}
publish('effective-implementation-test-grant-reference.json',ef)
print(json.dumps({'RESULT':'GRANT_PERSISTED_VERIFIED_EFFECTIVE','GRANT_IDENTITY':grant['GRANT_IDENTITY'],'FOUR_SEED_DETERMINISM':'PASS','NEGATIVE_SUITE':str(len(controls))+'/'+str(len(controls))+' PASS','ADAPTER_CONSTRUCTION_PERFORMED':False,'SYNTHETIC_TESTS_EXECUTED':False},sort_keys=True))
