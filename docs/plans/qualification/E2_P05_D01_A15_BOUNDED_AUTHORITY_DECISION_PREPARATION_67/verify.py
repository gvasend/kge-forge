"""Independent static reconstruction of charter, scoped mandates and readiness.
No native A15 application/capture/save/restore; no grant issued.
"""
import pathlib,json,hashlib,subprocess,sys,os,copy
E=pathlib.Path(__file__).parent;Q=E.parent;G=Q/'KGE_FORGE_QUALIFICATION_GOVERNANCE_CHARTER_65';L=Q/'KGE_FORGE_QUALIFICATION_GOVERNANCE_CHARTER_ADOPTION_66';A=Q/'E2_P05_D01_A15_CAPTURE_PERSISTENCE_RESUME_CLOSURE_61';B=Q/'E2_P05_D01_A15_BOUNDED_AUTHORITY_QUALIFICATION_62';S=Q/'E2_P05_D01_A15_PROSPECTIVE_SCENARIO_DESIGN_59'
def read(p):return json.loads(pathlib.Path(p).read_text())
def cb(x):return ''.join(json.JSONEncoder(sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).iterencode(x)).encode()
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def need(x,r):
 if not x:raise ValueError(r)
def identity(x,ns):return {'$type':'ArtifactIdentity','kind':{'$enum':'IdentityKind','value':'CONTENT_IDENTITY'},'namespace':ns,'sha256':hashlib.sha256(cb(x)).hexdigest()}
for p,h in read(E/'input-authentication.json')['FILES'].items():need(sha(p)==h,'INPUT_CHANGED')
chain=json.loads(subprocess.check_output([sys.executable,str(L/'reader.py')],env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')))
def charter_gate(value):
 need(value['CHARTER_EFFECTIVE'] and value['CURRENT_STATE']=='EFFECTIVE' and [r['STATE'] for r in value['ORDERED_LIFECYCLE']]==['DRAFT','REVIEWED','APPROVED','EFFECTIVE'],'CHARTER_NOT_EFFECTIVE')
charter_gate(chain)
charter=read(G/'charter-content.json');need(identity(charter,'kge-forge-qualification-governance-charter-v1')==chain['CHARTER_CONTENT_IDENTITY'],'CHARTER_HASH')
issuer=read(E/'effective-charter-issuer-evidence.json');need(issuer['ISSUER_ROLE']=='KGE-FORGE-PROJECT-OWNER-QUALIFICATION-GOVERNING-AUTHORITY' and issuer['CHARTER_VERSION']=='1.0' and issuer['CHARTER_IDENTITY']==chain['CHARTER_CONTENT_IDENTITY'] and issuer['LIFECYCLE']==chain['ORDERED_LIFECYCLE'] and not issuer['DELEGATION_USED'] and issuer['ACTUAL_A15_APPROVAL_EVIDENCE'] is None,'ISSUER_BINDING')
subject=read(B/'authority-subject-manifest.json');technical=subject['TECHNICAL_PREPARATION_IDENTITY'];need(identity(subject['TECHNICAL_BODY'],'qualification-A15-technical-preparation-subject-v1')==technical and technical['sha256']=='befe07aacc6b4c4e203488bce731f265a0520cf145174dca33dbfb4e68b43e9b','WRONG_SUBJECT')
oracles=json.loads(subprocess.check_output([sys.executable,str(A/'verify.py')],env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')));need(oracles['RESULT']=='PASS' and len(oracles['VARIANTS'])==2,'ORACLE_INCOMPLETE')
cp=read(B/'checkpoint-ledger-verification.json');need(len(cp['LEDGER'])==19 and all(sha(ev['FILE']['PATH'])==ev['FILE']['RAW_SHA256'] for ev in cp['LEDGER']),'CHECKPOINT_LEDGER')
variants=read(B/'two-variant-authorization-inventory.json');need(len(variants)==2 and len({cb(v['INVALIDATED_CONTENT_IDENTITY']) for v in variants})==2,'VARIANT_SCOPE')
harness=read(A/'static-harness-contract.json');need(harness['STATIC_HARNESS_READY'] and harness['STATUS']=='STATIC_SPECIFICATION_COMPLETE_NOT_INSTALLED_OR_AUTHORIZED' and harness['EXISTING_V3_A15_DISPATCH_IS_NOT_THIS_SEQUENCE'],'SPEC_AS_EXECUTABLE')
env=read(E/'qualification-environment-permission-inventory.json');need(env['EXECUTABLE_IDENTITY'] is None and env['QUALIFIED_WRITER_READER_SUPERVISOR_EXECUTABLE'] is None and env['EXACT_ARGV_ENV_CWD_LAUNCH_PROFILE'] is None and env['ENVIRONMENT_ID'] is None,'EXECUTOR_INVENTED')
need(sha(env['HOST_OR_RUNTIME']['PYTHON_PATH'])==env['HOST_OR_RUNTIME']['PYTHON_BINARY_SHA256'],'INTERPRETER_CHANGED')
bodyenv={k:v for k,v in env.items() if k!='OBSERVED_ENVIRONMENT_CONTENT_IDENTITY'};need(identity(bodyenv,'qualification-A15-local-environment-observation-v1')==env['OBSERVED_ENVIRONMENT_CONTENT_IDENTITY'],'ENV_OBSERVATION_IDENTITY')
need(not env['NETWORK_POLICY']['FUTURE_EXECUTOR_ENFORCEMENT_VERIFIED'] and not env['PROVENANCE']['FUTURE_EXECUTION_ENVIRONMENT_VERIFIED'] and env['AUDIT_BOUNDARY']['ACTUAL_TRUSTED_LAUNCHER_OR_AUDIT_BINDING'] is None,'CHARTER_AS_OS_PERMISSION')
need(env['OUTPUT_ALLOWLIST']==read(A/'save-target-contracts.json') and env['INPUT_ALLOWLIST']['INITIAL_CHECKPOINT']==cp['NATIVE_CHECKPOINT_ARTIFACT'],'ENVIRONMENT_ALLOWLIST')
# Reconstruct normative content directly from sealed source records rather than
# trusting a proposed subject to be its own semantic or authority oracle.
norm=read(E/'normative-adoption-subject.json');n=norm['CONTENT']
need(n['CHARTER_CONTENT_IDENTITY']==chain['CHARTER_CONTENT_IDENTITY'] and n['CHARTER_VERSION']=='1.0' and n['ISSUER_ROLE']==issuer['ISSUER_ROLE'] and n['A15_TECHNICAL_SUBJECT']==technical,'NORMATIVE_AUTHORITY_SUBJECT')
for k,file in [('EXACT_OWNERS','concrete-scenario-specification.json'),('EXACT_OWNER_SUPPORT_RELATIONSHIPS','exact-owner-proof-support-inventory.json'),('REQUIREDNESS','proposed-requiredness-rule.json'),('INVALIDATION_COVERAGE','candidate-invalidation-universe.json'),('DISJOINT_PARTITION','disjoint-variant-policy.json'),('PROTECTION_POLICY','protected-effect-policy.json')]:
 retained=read(S/file);expected=retained['OWNERS'] if k=='EXACT_OWNERS' else retained;need(n[k]==expected,'NORMATIVE_SOURCE_VALUE:'+k)
need(n['TWO_VARIANT_BINDINGS']==variants and n['FROZEN_ACCEPTANCE_COVERAGE']==read(B/'frozen-acceptance-traceability.json') and n['HISTORICAL_EXCLUSIONS']==read(B/'historical-exclusions.json') and not n['EXECUTION_OR_CAPTURE_AUTHORITY_INCLUDED'] and n['NO_NATIVE_OR_HISTORY_OR_FROZEN_AMENDMENT'],'NORMATIVE_EXPANSION')
normid=identity(n,'qualification-A15-normative-adoption-subject-v1');need(norm['IDENTITY']==normid and norm['APPROVAL_EVIDENCE'] is None and not norm['NORMATIVE_ADOPTED'] and norm['DECISION_READY'],'NORMATIVE_HASH_OR_ADOPTION')
execscope=read(E/'execution-mandate-bindings.json');capture=read(E/'capture-persistence-mandate-bindings.json')
need(execscope['CONTENT']==read(B/'native-execution-authority-requirement.json') and execscope['VARIANTS']==variants and execscope['EXECUTABLE_IDENTITY'] is None and execscope['QUALIFIED_INVOCATION'] is None and not execscope['MANDATE_COMPLETE'] and not execscope['PERMISSION_ISSUED'],'EXECUTION_BOUNDARY')
need(capture['VARIANT_EVENT_AFTER_STATE_BUNDLE_ORACLE_PINS']==variants and capture['PUBLICATION_TARGET_MANIFESTS']==read(A/'save-target-contracts.json') and capture['NATIVE_SEQUENCE']=='record_result -> save_bundle -> restore' and not capture['MANDATE_COMPLETE'] and not capture['PERMISSION_ISSUED'],'CAPTURE_SCOPE')
fail=read(E/'failure-retry-contract.json');need(fail['EXACT_PACKAGE61_CONTRACT']==read(A/'failure-retry-matrix.json') and fail['INITIAL_RETRY_LIMIT']==0,'RETRY_EXPANDED')
composition=read(E/'mandate-composition-assessment.json');need(composition['GOVERNING_RULE']==charter['MANDATE_COMPOSITION'] and composition['ONE_INSTRUMENT_THREE_MANDATE_SECTIONS_STRUCTURALLY_PERMITTED'] and not composition['COMBINED_COMPLETE_AUTHORIZATION_OPTION_ELIGIBLE'] and not composition['APPLICABLE_RESOURCE_PERMISSIONS_CREATED_BY_CHARTER'],'COMPOSITION_WITH_MISSING_POWER')
instrument=read(E/'three-mandate-authority-instrument.json');content=instrument['CONTENT'];iid=identity(content,'qualification-A15-partial-three-mandate-instrument-v1');need(instrument['PROPOSED_INSTRUMENT_CONTENT_IDENTITY']==iid and not instrument['COMPLETE'] and instrument['ISSUED_IDENTITY'] is None,'INSTRUMENT_IDENTITY')
need(content['NORMATIVE_SCOPE_MANDATE']['IDENTITY']==normid and content['EXECUTION_MANDATE']==execscope and content['CAPTURE_PERSISTENCE_MANDATE']==capture,'MANDATE_SECTION_MISMATCH')
need(all(content[k] is None for k in ['PROJECT_OWNER_APPROVAL_EVIDENCE','NORMATIVE_ADOPTION_EVIDENCE','EXECUTION_GRANT_IDENTITY','CAPTURE_GRANT_IDENTITY','EFFECTIVE_AUTHORIZATION_BOUNDARY']),'FUTURE_EVIDENCE_IN_CONTENT')
dossier=read(E/'unselected-normative-scope-decision-dossier.json');need(dossier['MANDATE']=='NORMATIVE_SCOPE_ONLY' and dossier['NORMATIVE_SUBJECT_IDENTITY']==normid and dossier['SELECTION'] is None and not dossier['COMBINED_A15_EXECUTION_CAPTURE_OPTION_PRESENT'],'COMBINED_OPTION_BEFORE_READY')
need([o['OPTION_ID'] for o in dossier['OPTIONS']]==['AUTHORIZE_BOUNDED_PROSPECTIVE_A15_NORMATIVE_SCOPE','DECLINE_BOUNDED_PROSPECTIVE_A15_NORMATIVE_SCOPE'],'WRONG_ELIGIBLE_OPTIONS')
gates=read(E/'decision-readiness.json')
def ready(r):
 need(r['CHARTER_EFFECTIVE'] and r['ISSUER_AUTHORITY_VERIFIED'] and r['A15_NORMATIVE_DECISION_READY'] and r['NORMATIVE_MANDATE_COMPLETE'],'NORMATIVE_GATE')
 need(not r['EXECUTION_ENVIRONMENT_VERIFIED'] and not r['EXECUTION_MANDATE_COMPLETE'] and not r['CAPTURE_MANDATE_COMPLETE'] and not r['A15_EXECUTION_DECISION_READY'] and not r['A15_CAPTURE_DECISION_READY'] and not r['COMBINED_A15_DECISION_READY'] and r['COMBINED_OPTIONS']==[],'PARTIAL_EXECUTION_READY')
 need(not any(r[k] for k in ['A15_NORMATIVE_AUTHORITY_ISSUED','A15_EXECUTION_AUTHORITY_ISSUED','A15_CAPTURE_AUTHORITY_ISSUED']),'AUTHORITY_ISSUED')
ready(gates);need(gates['PROPOSED_INSTRUMENT_IDENTITY']==iid and gates['NORMATIVE_SUBJECT_IDENTITY']==normid,'READINESS_IDENTITY')
# Corruption controls verify missing executable/resource information is not
# filled using the charter, an interpreter fingerprint, or future output.
controls=[]
def reject(label,fn):
 try:fn()
 except (ValueError,AssertionError,KeyError):controls.append({'CONTROL':label,'RESULT':'REJECTED'});return
 raise AssertionError('Negative escaped:'+label)
def exact(a,b):need(a==b,'EXACT_BINDING')
reject('WRONG_CHARTER_VERSION',lambda:exact('LATEST',issuer['CHARTER_VERSION']))
revoked=copy.deepcopy(chain);revoked['CURRENT_STATE']='REVOKED';reject('REVOKED_AUTHORITY',lambda:charter_gate(revoked))
reject('WRONG_SUBJECT',lambda:exact(cp['SNAPSHOT_IDENTITY'],technical))
reject('ALTERED_ORACLE',lambda:exact(dict(variants[0]['INDEPENDENT_ORACLE_IDENTITY'],sha256='0'*64),variants[0]['INDEPENDENT_ORACLE_IDENTITY']))
reject('CHANGED_CHECKPOINT',lambda:exact(variants[0]['EXPECTED_AFTER_SNAPSHOT_IDENTITY'],cp['SNAPSHOT_IDENTITY']))
bad=copy.deepcopy(gates);bad['EXECUTION_ENVIRONMENT_VERIFIED']=True;reject('MISSING_ENVIRONMENT_PERMISSION_AS_VERIFIED',lambda:ready(bad))
bad=copy.deepcopy(execscope);bad['CONTENT']['RECORD_RESULT_CALLS']=3;reject('UNAUTHORIZED_EXECUTION_EXPANSION',lambda:exact(bad['CONTENT'],execscope['CONTENT']))
bad=copy.deepcopy(capture);bad['PUBLICATION_TARGET_MANIFESTS'][1]['OUTPUT_DIRECTORY']=bad['PUBLICATION_TARGET_MANIFESTS'][0]['OUTPUT_DIRECTORY'];reject('CAPTURE_SCOPE_MISMATCH',lambda:exact(bad,capture))
reject('CIRCULAR_APPROVAL_IDENTITY',lambda:exact(identity(dict(content,PROJECT_OWNER_APPROVAL_EVIDENCE=iid),'qualification-A15-partial-three-mandate-instrument-v1'),iid))
bad=copy.deepcopy(gates);bad['COMBINED_A15_DECISION_READY']=True;reject('INCOMPLETE_COMBINED_DOSSIER',lambda:ready(bad))
reject('INTERPRETER_AS_QUALIFIED_A15_EXECUTABLE',lambda:exact(env['HOST_OR_RUNTIME']['PYTHON_BINARY_SHA256'],env['EXECUTABLE_IDENTITY']))
bad=copy.deepcopy(fail);bad['INITIAL_RETRY_LIMIT']=1;reject('UNSEALED_RETRY',lambda:exact(bad['INITIAL_RETRY_LIMIT'],fail['INITIAL_RETRY_LIMIT']))
bad=copy.deepcopy(gates);bad['A15_NORMATIVE_AUTHORITY_ISSUED']=True;reject('PREPARATION_AS_APPROVAL',lambda:ready(bad))
reg=read(E/'lessons-register-snapshot.json');before_reg=read(G/'lessons-register-preservation-snapshot.json');need(reg['EVENTS'][:len(before_reg['EVENTS'])]==before_reg['EVENTS'],'LESSON_PREFIX_CHANGED')
head='0'*64
for ev in reg['EVENTS']:
 need(ev['PREVIOUS_EVENT_HASH']==head and hashlib.sha256(json.dumps({k:v for k,v in ev.items() if k!='EVENT_HASH'},sort_keys=True,separators=(',',':')).encode()).hexdigest()==ev['EVENT_HASH'],'LESSON_CHAIN');head=ev['EVENT_HASH']
need(len([ev for ev in reg['EVENTS'] if ev['EVENT_TYPE']=='LESSON_RECORDED'])==10 and len([ev for ev in reg['EVENTS'] if ev.get('WORK_PACKAGE')=='67'])==10,'LESSON_COUNT')
print(json.dumps({'RESULT':'PASS_PARTIAL_READINESS_RECONSTRUCTION','CHARTER_EFFECTIVE':True,'ISSUER_VERIFIED':True,'EXACT_SUBJECT':technical,'NORMATIVE_SUBJECT_IDENTITY':normid,'PROPOSED_INSTRUMENT_IDENTITY':iid,'OBSERVED_ENVIRONMENT_IDENTITY':env['OBSERVED_ENVIRONMENT_CONTENT_IDENTITY'],'A15_NORMATIVE_DECISION_READY':True,'A15_EXECUTION_DECISION_READY':False,'A15_CAPTURE_DECISION_READY':False,'COMBINED_A15_DECISION_READY':False,'DECISION_OPTIONS':[o['OPTION_ID'] for o in dossier['OPTIONS']],'MISSING_GAPS':['E67-QUALIFIED-EXECUTABLE-INVOCATION','E67-SEALED-ENVIRONMENT-RESOURCE-PERMISSIONS'],'NEGATIVE_CONTROLS':controls,'GRANTS_ISSUED':0,'NATIVE_A15_OPERATIONS':0},sort_keys=True))
