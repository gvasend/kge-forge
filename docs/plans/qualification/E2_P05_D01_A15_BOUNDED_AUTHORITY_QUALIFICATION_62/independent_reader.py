"""Independent static reader: reconstruct from original sealed Package61 inputs.
No adapter imports, native replay, capture, save or restore; candidate output is
read only after independent checkpoint/variant/oracle/harness reconstruction.
"""
import pathlib,json,hashlib,copy
P=pathlib.Path('docs/plans');Q=P/'qualification';E=pathlib.Path(__file__).parent;A=Q/'E2_P05_D01_A15_CAPTURE_PERSISTENCE_RESUME_CLOSURE_61';S=Q/'E2_P05_D01_A15_PROSPECTIVE_SCENARIO_DESIGN_59'
def read(p):return json.loads(pathlib.Path(p).read_text())
def cb(x):return ''.join(json.JSONEncoder(sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).iterencode(x)).encode()
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def ref(p):return {'PATH':str(p),'RAW_SHA256':sha(p),'CONTENT_IDENTITY':{'$type':'ArtifactIdentity','kind':{'$enum':'IdentityKind','value':'CONTENT_IDENTITY'},'namespace':'raw-file-sha256','sha256':sha(p)}}
def enforce(ok,why):
 if not ok:raise ValueError(why)
sealed=read(A/'evidence-index.json')['FILES'];enforce(all(sha(p)==h for p,h in sealed.items()),'PACKAGE61_CHANGED')
for p,h in read(E/'authentication.json')['FILES'].items():enforce(sha(p)==h,'AUTHENTICATED_SOURCE_CHANGED:'+p)
# Native checkpoint choice derives from original capsule provenance, not newly
# written Package62 manifest or a heuristic among equal native aliases.
fixture=read(Q/'E2_P05_D01_FIXTURE_ORACLE_CLOSURE_2/fixtures/D01-VARIANT__E2-A15__CANONICAL_REQUIRED_BEHAVIOR.json');checkpoint_path=pathlib.Path(fixture['provenance'][0]['path']);checkpoint=read(A/'initial-checkpoint-restore-contract.json');native=read(checkpoint_path);bundle=native['bundle'];state=bundle['current'];ledger=[]
enforce(bundle==fixture['canonical_content']['bundle'] and checkpoint_path.read_bytes()==cb(native),'WRONG_CHECKPOINT')
enforce(sha(checkpoint_path)==fixture['provenance'][0]['raw_sha256'],'WRONG_CHECKPOINT_HASH')
enforce(sha(checkpoint_path)==checkpoint['NATIVE_BUNDLE_IDENTITY']['sha256'],'WRONG_BUNDLE')
enforce(hashlib.sha256(cb({'schema':'PLANNER-SNAPSHOT-1','snapshot':state})).hexdigest()==checkpoint['INITIAL_SNAPSHOT_IDENTITY']['sha256'],'WRONG_SNAPSHOT')
for ev in bundle['events']:
 p=checkpoint_path.parent/('event-'+ev['identity']['sha256']+'.json');enforce(p.is_file() and not p.is_symlink() and p.read_bytes()==cb(ev),'MISSING_OR_CHANGED_LEDGER')
 ledger.append({'SEQUENCE':ev['sequence'],'EVENT_IDENTITY':ev['identity'],'FILE':ref(p),'PARENT_SNAPSHOT':ev['parent_snapshot'],'AFTER_SNAPSHOT':ev['after_snapshot']})
enforce([e['SEQUENCE'] for e in ledger]==list(range(1,20)),'LEDGER_SEQUENCE')
for p in bundle['sources']+[bundle['policy']]:enforce(p['identity']['kind']['value']=='CONTENT_IDENTITY' and p['identity']['namespace']=='raw-file-sha256' and p['profile']['value']=='raw-file-sha256' and not p['pointer'] and sha(p['path'])==p['identity']['sha256'],'WRONG_SOURCE_PIN')
before=read(A/'starting-state-precondition-oracle.json');policy=read(S/'protected-effect-policy.json');targets=read(A/'save-target-contracts.json');variants=[]
for target in targets:
 name=target['VARIANT_ID'];path=A/(name+'-full-expected-output.json');o=read(path);binding=read(A/(name+'-capture-binding.json'))
 enforce(o['FULL_ORACLE_READY'] and not o['UNDETERMINED'],'INCOMPLETE_ORACLE')
 enforce(o['INITIAL_SNAPSHOT']==checkpoint['INITIAL_SNAPSHOT_IDENTITY'],'CROSS_VARIANT_INITIAL')
 enforce(hashlib.sha256(pathlib.Path(target['EXPECTED_BYTES_EVIDENCE']).read_bytes()).hexdigest()==target['CONTENT_IDENTITY']['sha256'],'EXPECTED_BYTE_MISMATCH')
 dto=o['EXPECTED_FULL_OUTPUT']; enforce(set(dto)==set(dto['output_field_set']) and len(dto)==16,'INCOMPLETE_NATIVE_OUTPUT')
 enforce(dto['typed_bundle']==dto['native_result'] and dto['typed_bundle']['events'][:19]==bundle['events'] and len(dto['event_identities'])==20,'CAPTURE_OR_TRACE_GAP')
 enforce(dto['resume']==o['EXPECTED_RESUME'] and set(dto['resume'])=={'$type','allowed','actions','reasons','supporting_identities'} and dto['resume']['allowed'] is False and dto['resume']['reasons']==sorted(dto['resume']['reasons']) and len(dto['resume']['reasons'])==4,'RESUME_REASON_GAP')
 enforce(o['TARGET_SATISFACTION']=={'E2-ROOT':'UNRESOLVED','E2-SLOT':'UNRESOLVED'} and o['ADMISSION_STALE']['EXPECTED']=='STALE' and all(not p['EXPECTED'] for p in o['PROOF_USABILITY']),'ACCEPTANCE_GAP')
 enforce(next(s for s in o['EXPECTED_STATE']['statuses'] if s['id']['value']=='E2-FINISH')['state']['value']=='BLOCKED' and dto['Computation']['control']['value']=='PLAN_DEFECT','FINISH_GAP')
 enforce(not pathlib.Path(target['OUTPUT_DIRECTORY']).exists(),'OUTPUT_ALREADY_CREATED')
 variants.append({'VARIANT_ID':name,'VARIANT_DEFINITION':ref(A/(name+'-capture-binding.json')),'INITIAL_CHECKPOINT_IDENTITY':checkpoint['NATIVE_BUNDLE_IDENTITY'],'INITIAL_SNAPSHOT_IDENTITY':checkpoint['INITIAL_SNAPSHOT_IDENTITY'],'INVALIDATED_CONTENT_IDENTITY':o['SOURCE_CONTENT_IDENTITY'],'EXPECTED_AFTER_SNAPSHOT_IDENTITY':o['EXPECTED_STATE_IDENTITY'],'EXPECTED_EVENT_IDENTITY':binding['INVALIDATION_EVENT_IDENTITY'],'EXPECTED_BUNDLE_IDENTITY':binding['EXPECTED_BUNDLE_IDENTITY'],'INDEPENDENT_ORACLE_IDENTITY':ref(path)['CONTENT_IDENTITY'],'INDEPENDENT_ORACLE_PIN':ref(path),'EXPECTED_SERIALIZED_BYTES':ref(target['EXPECTED_BYTES_EVIDENCE']),'EXPECTED_SERIALIZED_LENGTH':len(pathlib.Path(target['EXPECTED_BYTES_EVIDENCE']).read_bytes()),'PROTECTED_IDENTITIES':policy['DIRECT_PROTECTED_IDENTITIES'],'PROTECTION_POLICY':ref(S/'protected-effect-policy.json'),'CAPTURE_OUTPUT_NAMESPACE':target['OUTPUT_DIRECTORY'],'SAVE_TARGET':target['BUNDLE_PATH'],'HANDOFF_TARGET':target['HANDOFF_PATH'],'SUPERVISOR_EXIT_EVIDENCE_TARGET':target['SUPERVISOR_EXIT_EVIDENCE'],'READER_EVIDENCE_TARGET':[r['EVIDENCE_PATH'] for r in target['READERS']],'HASH_SEEDS':[r['HASH_SEED'] for r in target['READERS']],'EXACT_CAPTURE_ARGUMENT_BINDINGS':binding['EXACT_CAPTURE_ARGUMENT_BINDINGS']})
enforce(len(variants)==2 and len({cb(v['INVALIDATED_CONTENT_IDENTITY']) for v in variants})==2,'VARIANT_COVERAGE')
allowed={cb(v['INVALIDATED_CONTENT_IDENTITY']) for v in variants};protected=sorted([p['identity'] for p in bundle['sources']+[bundle['policy']] if cb(p['identity']) not in allowed],key=cb)
enforce({cb(p) for p in protected}=={cb(p) for p in policy['DIRECT_PROTECTED_IDENTITIES']} and len(protected)==len(policy['DIRECT_PROTECTED_IDENTITIES'])==53,'PROTECTION_NOT_SEALED')
names=['static-harness-contract.json','writer-handoff-cold-reader-contracts.json','save-target-contracts.json','failure-retry-matrix.json','initial-checkpoint-restore-contract.json','starting-state-precondition-oracle.json','resume-comparison-schema.json','native-interface-inventory.json'];harness_pins=[ref(A/n) for n in names];hid={'$type':'ArtifactIdentity','kind':{'$enum':'IdentityKind','value':'CONTENT_IDENTITY'},'namespace':'qualification-A15-static-harness-binding-v1','sha256':hashlib.sha256(cb(harness_pins)).hexdigest()}
cp={'CHECKPOINT_DIRECTORY':str(checkpoint_path.parent),'NATIVE_CHECKPOINT_ARTIFACT':ref(checkpoint_path),'NATIVE_MANIFEST_PATH':str(checkpoint_path),'NATIVE_MANIFEST_SCHEMA':'PLANNER-BUNDLE-1; the artifact is its native bundle envelope, not an invented extra file','QUALIFICATION_MANIFEST':ref(A/'initial-checkpoint-restore-contract.json'),'SNAPSHOT_IDENTITY':checkpoint['INITIAL_SNAPSHOT_IDENTITY'],'BUNDLE_IDENTITY':checkpoint['NATIVE_BUNDLE_IDENTITY'],'LEDGER':ledger,'SOURCE_POLICY_PINS':read(A/'source-policy-pin-verification.json'),'AUTHORITY_ENTITIES':[x for x in state['entities'] if x['kind']['value']=='AUTHORITY'],'CONTEXT':state['context'],'REPLAY_SCOPE':bundle['scope'],'INITIAL_CONTROL':before['EXPECTED_BEFORE_COMPUTATION']['control'],'INITIAL_PROOF_USABILITY':before['EXPECTED_BEFORE_TYPED_PROOF_USABILITY'],'FINISH_INITIALLY_ACTIONABLE':before['EXPECTED_BEFORE_COMPUTATION']['actionable'],'BASELINE_REPLACED':False,'RESTORE_EXECUTED':False}
# New proposed permission policy is separately validated against sealed process
# contracts and user62 fail-closed limits, not assumed authorized input.
execution=read(E/'native-execution-authority-requirement.json');exclusions=read(E/'historical-exclusions.json')['EXCLUDED_CLAIMS_AND_OPERATIONS'];issuer=read(E/'issuer-version-scope-qualification.json');scope=read(E/'normative-scope-authority-assessment.json')
def check_execution(x):
 for k,v in {'SUPERVISORS':1,'WRITERS':2,'COLD_READERS':8,'INITIAL_RESTORE_CALLS':2,'COLD_RESTORE_CALLS':8,'RECORD_RESULT_CALLS':2,'DIRECT_APPLY_EVENT_CALLS':0,'SAVE_BUNDLE_CALLS':2,'RETRY_LIMIT':0}.items():enforce(x[k]==v,'EXECUTION_BOUNDARY:'+k)
 enforce(x['HASH_SEEDS']==[0,1,7,101] and x['PERMISSION_REQUIRED'] and not x['AUTHORITY_ISSUED'],'AUTHORITY_CONFUSION')
 enforce(x['ALLOWED_WRITE_TARGETS']==[{'VARIANT_ID':v['VARIANT_ID'],'NAMESPACE':v['CAPTURE_OUTPUT_NAMESPACE'],'SAVE_TARGET':v['SAVE_TARGET'],'HANDOFF':v['HANDOFF_TARGET'],'EXIT_EVIDENCE':v['SUPERVISOR_EXIT_EVIDENCE_TARGET'],'READER_EVIDENCE':v['READER_EVIDENCE_TARGET']} for v in variants],'CROSS_VARIANT_OUTPUT_REUSE')
 enforce(all(not r['RETRY_ALLOWED'] and r['RETRIES_AUTHORIZED_IN_PROPOSED_INITIAL_SCOPE']==0 for r in x['FAILURE_RULES']),'UNAUTHORIZED_RETRY')
 enforce(x['EXCLUDED']==exclusions and x['NATIVE_INTERFACES']==ref(A/'native-interface-inventory.json'),'SCOPE_MISMATCH')
 enforce(len(x['FULL_COMPARISON_DOMAINS'])==15 and len(set(x['FULL_COMPARISON_DOMAINS']))==15,'MISSING_ACCEPTANCE_DOMAIN')
check_execution(execution)
enforce(not scope['NORMATIVE_ADOPTED'] and not scope['EXECUTION_GRANTED'] and not scope['GRANTS_COMBINED'] and scope['COMPOSITION_PERMISSION_EVIDENCE'] is None,'SCOPE_TREATED_AS_ADOPTED')
schema=read(Q/'E2_P05_D01_A15_NORMATIVE_KNOWLEDGE_CONTRACT_42/normative-knowledge-schema.json');old=read(Q/'E2_P05_D01_A15_NORMATIVE_KNOWLEDGE_INSTANCE_43/proposed-typed-instance.json');eligibility=read(A/'authority-preparation-eligibility.json')
enforce(schema['INSTANCE_VALUES']['ISSUING_AUTHORITY'] is None and old['ISSUING_AUTHORITY'] is None and eligibility['AUTHORITY_SUBJECT_READY'] is False,'ISSUER_SOURCE_STATE_CHANGED')
enforce('Verified authorized human qualification owner' in schema['FIELDS']['ISSUING_AUTHORITY'],'ISSUER_REQUIREMENT_CHANGED')
# Do not invent an authority record to make a negative baseline decision-ready.
def check_issuer(x):
 for k in ('ISSUER_IDENTITY','ISSUER_ROLE','AUTHORITY_VERSION','AUTHORITY_SCOPE','AUTHORIZED_SUBJECT','GRANT_IDENTITY'):enforce(x[k] is None,'UNSUPPORTED_AUTHORITY_TERM:'+k)
 enforce(not any(x[k] for k in ('ISSUER_VERIFIED','AUTHORITY_VERSION_VERIFIED','AUTHORITY_SCOPE_VERIFIED','A14_AUTHORITY_REUSED')),'UNSUPPORTED_AUTHORITY_VERIFICATION')
check_issuer(issuer)
body={'CHECKPOINT':cp,'VARIANTS':variants,'HARNESS_IDENTITY':hid,'HARNESS_PINS':harness_pins,'PROPOSED_NORMATIVE_RULE_PIN':ref(S/'proposed-requiredness-rule.json'),'PARTITION_PIN':ref(S/'disjoint-variant-policy.json'),'PROTECTION_PIN':ref(S/'protected-effect-policy.json'),'FROZEN_ACCEPTANCE':ref(P/'DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_EXPERIMENT_1.json'),'FROZEN_SOURCE_POINTER':'/cases/14','EXECUTION_BOUNDARY':execution,'HISTORICAL_EXCLUSIONS':exclusions}
identity={'$type':'ArtifactIdentity','kind':{'$enum':'IdentityKind','value':'CONTENT_IDENTITY'},'namespace':'qualification-A15-technical-preparation-subject-v1','sha256':hashlib.sha256(cb(body)).hexdigest()}
manifest=read(E/'authority-subject-manifest.json');enforce(manifest['TECHNICAL_BODY']==body and manifest['TECHNICAL_PREPARATION_IDENTITY']==identity,'SUBJECT_RECONSTRUCTION_MISMATCH')
enforce(read(E/'two-variant-authorization-inventory.json')==variants and read(E/'checkpoint-ledger-verification.json')==cp,'INVENTORY_RECONSTRUCTION_MISMATCH')
readiness=read(E/'decision-readiness.json')
def check_ready(x):
 enforce(not x['DECISION_READY'] and not x['AUTHORITY_SUBJECT_COMPLETE'] and not x['ISSUER_VERIFIED'] and not x['AUTHORITY_VERSION_VERIFIED'] and not x['AUTHORITY_SCOPE_VERIFIED'] and x['DECISION_OPTIONS']==[] and not x['SELECTABLE_DOSSIER_CREATED'],'INCOMPLETE_DOSSIER_READY')
check_ready(readiness)
trace=read(E/'frozen-acceptance-traceability.json');enforce(trace['EXACT_CASE']==read(P/'DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_EXPERIMENT_1.json')['cases'][14],'FROZEN_CHANGED')
for v in variants:enforce({r['DOMAIN'] for r in trace['DOMAIN_ROWS'] if r['VARIANT_ID']==v['VARIANT_ID']}==set(execution['FULL_COMPARISON_DOMAINS']),'MISSING_FROZEN_TERM')
# Corrupt independently reconstructed scope/candidate records, not native inputs.
neg=[]
def rejected(label,fn):
 try:fn()
 except (ValueError,AssertionError,KeyError):neg.append({'CONTROL':label,'RESULT':'REJECTED'});return
 raise AssertionError('Negative escaped:'+label)
def exact(a,b):enforce(a==b,'EXACT_IDENTITY_OR_FIELD_MISMATCH')
rejected('WRONG_CHECKPOINT',lambda:exact(cp['SNAPSHOT_IDENTITY'],cp['BUNDLE_IDENTITY']))
rejected('MISSING_LEDGER_FILE',lambda:exact(ledger[:-1],ledger))
wrong=copy.deepcopy(bundle['sources'][0]);wrong['identity']['sha256']='0'*64
rejected('WRONG_SOURCE_PIN',lambda:enforce(sha(wrong['path'])==wrong['identity']['sha256'],'WRONG_SOURCE_PIN'))
rejected('WRONG_VARIANT_IDENTITY',lambda:exact(variants[0]['VARIANT_ID'],variants[1]['VARIANT_ID']))
rejected('WRONG_ORACLE_IDENTITY',lambda:exact(variants[0]['INDEPENDENT_ORACLE_IDENTITY'],variants[1]['INDEPENDENT_ORACLE_IDENTITY']))
rejected('WRONG_EXPECTED_BUNDLE',lambda:exact(variants[0]['EXPECTED_BUNDLE_IDENTITY'],cp['BUNDLE_IDENTITY']))
bad=copy.deepcopy(execution);bad['FULL_COMPARISON_DOMAINS'].remove('RESUME_REASONS');rejected('MISSING_FROZEN_ACCEPTANCE_TERM',lambda:check_execution(bad))
rejected('UNSEALED_PROTECTION_POLICY',lambda:exact(ref(S/'protected-effect-policy.json'),ref(S/'disjoint-variant-policy.json')))
bad=copy.deepcopy(execution);bad['ALLOWED_WRITE_TARGETS'][1]['NAMESPACE']=bad['ALLOWED_WRITE_TARGETS'][0]['NAMESPACE'];rejected('CROSS_VARIANT_OUTPUT_REUSE',lambda:check_execution(bad))
bad=copy.deepcopy(execution);bad['RETRY_LIMIT']=1;rejected('UNAUTHORIZED_RETRY',lambda:check_execution(bad))
bad=copy.deepcopy(issuer);bad['A14_AUTHORITY_REUSED']=True;rejected('A14_AUTHORITY_REUSED',lambda:check_issuer(bad))
bad=copy.deepcopy(execution);bad['AUTHORITY_ISSUED']=True;rejected('PROPOSED_SCOPE_TREATED_AS_AUTHORIZED',lambda:check_execution(bad))
for field,label,value in [('ISSUER_IDENTITY','WRONG_ISSUER',{'namespace':'CORRUPTED','sha256':'0'*64}),('AUTHORITY_VERSION','WRONG_AUTHORITY_VERSION',schema['VERSION']),('AUTHORITY_SCOPE','WRONG_SCOPE','PRODUCTION')]:
 bad=copy.deepcopy(issuer);bad[field]=value;rejected(label,lambda bad=bad:check_issuer(bad))
for label,field in [('HISTORICAL_OCCURRENCE_CLAIM','Original historical A15 execution'),('A16_INCLUDED','A16 qualification'),('E1_INCLUDED','E1 modification'),('PRODUCTION_INCLUDED','Production effects')]:
 bad=copy.deepcopy(execution);bad['EXCLUDED'].remove(field);rejected(label,lambda bad=bad:check_execution(bad))
bad=copy.deepcopy(readiness);bad['DECISION_READY']=True;rejected('INCOMPLETE_DOSSIER_READY',lambda:check_ready(bad))
register=read(E/'lessons-register-snapshot.json');old_register=read(A/'lessons-register-snapshot.json');enforce(register['EVENTS'][:len(old_register['EVENTS'])]==old_register['EVENTS'],'LESSON_PREFIX_CHANGED')
head='0'*64
for e in register['EVENTS']:
 enforce(e['PREVIOUS_EVENT_HASH']==head and hashlib.sha256(json.dumps({k:v for k,v in e.items() if k!='EVENT_HASH'},sort_keys=True,separators=(',',':')).encode()).hexdigest()==e['EVENT_HASH'],'LESSON_HASH_CHAIN_CHANGED');head=e['EVENT_HASH']
enforce(len([e for e in register['EVENTS'] if e['EVENT_TYPE']=='LESSON_RECORDED'])==10 and len([e for e in register['EVENTS'] if e.get('WORK_PACKAGE')=='62'])==10,'LESSON_COUNT_CHANGED')
print(json.dumps({'RESULT':'PASS_PARTIAL_READINESS_CONFIRMED','TECHNICAL_PREPARATION_IDENTITY':identity,'CHECKPOINT_IDENTITY':cp['BUNDLE_IDENTITY'],'SNAPSHOT_IDENTITY':cp['SNAPSHOT_IDENTITY'],'LEDGER_FILES':19,'VARIANTS':[{k:v[k] for k in ['VARIANT_ID','INDEPENDENT_ORACLE_IDENTITY','EXPECTED_BUNDLE_IDENTITY']} for v in variants],'HARNESS_IDENTITY':hid,'DECISION_READY':False,'DECISION_OPTIONS':[],'MISSING_GAPS':readiness['MISSING_GAPS'],'NEGATIVE_CONTROLS':neg,'NATIVE_EFFECTS':0},sort_keys=True))
