"""Fresh-process static verification; no native imports, replay or filesystem publication.
Original retained input plus Package60's independently checked overlays supply
state semantics. Resume predicates and serialization are reconstructed here.
"""
import json,pathlib,hashlib,copy,subprocess,sys,os
from resume_reference import derive,canonical
E=pathlib.Path(__file__).parent; OLD=E.parent/'E2_P05_D01_A15_INDEPENDENT_AFTER_STATE_ORACLE_60'
def read(p):return json.loads(pathlib.Path(p).read_text())
def demand(x,r):
 if not x:raise ValueError(r)
def compare(actual,expected):demand(actual==expected,'EXACT_FULL_OUTPUT_MISMATCH')
def bytesof(x):return ''.join(json.JSONEncoder(sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).iterencode(x)).encode('utf-8')
def digest(x,ns):return {'$type':'ArtifactIdentity','kind':{'$enum':'IdentityKind','value':'CONTENT_IDENTITY'},'namespace':ns,'sha256':hashlib.sha256(bytesof(x)).hexdigest()}
def publication_contract(target):
 p=pathlib.Path(target['OUTPUT_DIRECTORY']); demand(not p.exists() and p.resolve()==p.absolute(),'TARGET_EXISTS_OR_SYMLINK')
 demand('..' not in p.parts and not p.is_absolute(),'UNSAFE_RELATIVE_TARGET')
 demand(target['NO_SYMLINK_PATH_COMPONENTS'] and target['NO_PREEXISTING_TARGET'] and target['RECHECK_BEFORE_LAUNCH'],'INCOMPLETE_PREFLIGHT')
 demand(not target['HEAD_MUTATION'] and not target['DIRECTORY_CREATION_AUTHORIZED_NOW'],'UNAUTHORIZED_PUBLICATION')
 demand(pathlib.Path(target['BUNDLE_PATH']).parent==p,'CROSS_VARIANT_SAVE')
 demand(target['CONTENT_IDENTITY']['namespace']=='planner-bundle-v1','WRONG_BUNDLE_DOMAIN')
 demand(pathlib.Path(target['BUNDLE_PATH']).name=='bundle-'+target['CONTENT_IDENTITY']['sha256']+'.json','WRONG_TARGET_ID')
def lifecycle(steps):
 required=['record_result','save_bundle','publication_verified','handoff_published','writer_exit_observed','reader_launched','restore_compared']
 demand(steps==required,'LIFECYCLE_ORDER_OR_EXIT_EVIDENCE')
def authorization(a):
 demand(not a['A14_REUSED_AS_AUTHORITY'],'A14_AUTHORITY_REUSE')
 demand(not a['EXECUTION_AUTHORIZED'],'STATIC_IS_NOT_AUTHORITY')
def complete_output(d):
 expected=['qualification_label','typed_snapshot','typed_bundle','Computation','selection','resume','branches','witnesses','rejections','policy','source_pins','snapshot_identity','bundle_identity','event_identities','native_result','output_field_set']
 demand(set(d)==set(expected) and d['output_field_set']==sorted(expected),'INCOMPLETE_OUTPUT_FIELD_SET')
 demand(d['native_result']['$type']=='PersistenceBundle','WRONG_RESULT_TYPE')
 demand(d['native_result']==d['typed_bundle'],'WRONG_CAPTURE_BUNDLE')
 demand(d['typed_snapshot']==d['typed_bundle']['current'],'WRONG_CAPTURE_STATE')
 demand(d['resume'].keys()=={'$type','allowed','actions','reasons','supporting_identities'},'INCOMPLETE_RESUME_SCHEMA')
 demand(d['resume']['$type']=='ResumeEligibility','WRONG_RESUME_TYPE')
# Reconstruct states and identities using the SEPARATE original-input overlay
# path. This script neither consumes construction output as its source nor runs
# a native cold reader. The subprocess is a static JSON overlay verifier.
second=json.loads(subprocess.check_output([sys.executable,str(OLD/'independent_verify.py')],env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')))
auth=read(E/'authentication.json'); demand(all(hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()==h for p,h in auth['FILES'].items()),'SOURCE_CHANGED')
fixture=read('docs/plans/qualification/E2_P05_D01_FIXTURE_ORACLE_CLOSURE_2/fixtures/D01-VARIANT__E2-A15__CANONICAL_REQUIRED_BEHAVIOR.json')['canonical_content']['bundle']
initial_contract=read(E/'initial-checkpoint-restore-contract.json')
original_capsule=read('docs/plans/qualification/E2_P05_D01_FIXTURE_ORACLE_CLOSURE_2/fixtures/D01-VARIANT__E2-A15__CANONICAL_REQUIRED_BEHAVIOR.json')
assert initial_contract['SOURCE_PATH']==original_capsule['provenance'][0]['path']
assert read(initial_contract['SOURCE_PATH'])=={'schema':'PLANNER-BUNDLE-1','bundle':fixture}
assert initial_contract['EXPECTED_BUNDLE']==fixture
before_expected=read(E/'starting-state-precondition-oracle.json')
assert before_expected['BEFORE_SNAPSHOT']==initial_contract['INITIAL_SNAPSHOT_IDENTITY']
assert before_expected['EXPECTED_BEFORE_COMPUTATION']['control']=={'$enum':'ControlState','value':'RUNNABLE'}
assert before_expected['EXPECTED_BEFORE_COMPUTATION']['actionable']==[{'$type':'ActionId','value':'E2-FINISH'}]
assert before_expected['EXPECTED_BEFORE_TYPED_PROOF_USABILITY']==[{'proof':p['id'],'usable':True} for p in fixture['current']['typed_proofs']]
assert all(p.get('validation',{'value':'ACCEPTED'})['value']=='ACCEPTED' for p in fixture['current']['typed_proofs']+fixture['current']['proof_contracts']+fixture['current']['installed_definitions'])
assert fixture['current']['roots'][0]['state']['value']=='SATISFIED' and fixture['current']['slots'][0]['state']['value']=='RESOLVED'
assert initial_contract['NATIVE_BUNDLE_IDENTITY']==digest({'schema':'PLANNER-BUNDLE-1','bundle':fixture},'planner-bundle-v1')
assert len(initial_contract['RETAINED_LEDGER_FILES'])==20 and initial_contract['ACTUAL_RESTORES_EXECUTED']==0
for path,sha in initial_contract['RETAINED_LEDGER_FILES'].items():assert hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()==sha
results=[]; negatives=[]
for target in read(E/'save-target-contracts.json'):
 name=target['VARIANT_ID']; source=read(OLD/(name+'-expected-output.json')); oracle=read(E/(name+'-full-expected-output.json')); binding=read(E/(name+'-capture-binding.json'))
 independent=next(r for r in second if r['VARIANT']==name)
 b=source['CAPTURE_EXPECTATION']['EXPECTED_UPDATED_BUNDLE'];c=source['EXPECTED_COMPUTATION'];resume,witnesses,proof=derive(b,c['actionable'],c['blocked'])
 expected={'qualification_label':{'type':'PROSPECTIVE_D01_RUNNER_MATRIX','historical_reconstruction':False,'native_context':b['current']['context']},'typed_snapshot':b['current'],'typed_bundle':b,'Computation':dict(c,qualification_type='Computation'),'selection':c['selection'],'resume':resume,'branches':c['branches'],'witnesses':witnesses,'rejections':None,'policy':b['policy'],'source_pins':sorted(b['sources'],key=bytesof),'snapshot_identity':independent['AFTER_STATE'],'bundle_identity':independent['BUNDLE'],'event_identities':b['events'],'native_result':b}
 expected['output_field_set']=sorted(list(expected)+['output_field_set']);complete_output(expected)
 compare(oracle['EXPECTED_FULL_OUTPUT'],expected);compare(binding['EXPECTED_FULL_OUTPUT'],expected)
 # Native contract_current requires the sole ROOT/SLOT configuration to be
 # current. The independent native input overlay stales that exact installed
 # role for BOTH sources, so every retained proof fails this conjunct.
 configurations=[(r,json.loads(r['request']['definition']['descriptor_json'])) for r in b['current']['installed_definitions'] if json.loads(r['request']['definition']['descriptor_json'])['definition_type']=='ROOT_SLOT_CONFIGURATION_SET']
 assert len(configurations)==1 and configurations[0][0]['validation']['value']=='STALE'
 subject=configurations[0][1]['subject'];targets={subject['root'],subject['slot']}
 assert {p['target']['value'] for p in b['current']['typed_proofs']}==targets
 usability=[{'proof':p['id'],'usable':False} for p in b['current']['typed_proofs']]
 assert oracle['EXPECTED_NATIVE_QUERY_OUTPUTS']=={'typed_proof_usability':usability}
 assert binding['RECORD_RESULT_INPUT']==b['events'][-1]['result'] and binding['RECORD_RESULT_PARENT_IDENTITY']==b['events'][-1]['parent_snapshot']
 # Independently read the existing capture signature, without invoking it.
 import ast
 capture_plan=binding['EXACT_CAPTURE_ARGUMENT_BINDINGS'];tree=ast.parse(pathlib.Path(capture_plan['ENTRYPOINT_FILE']).read_text())
 capture_fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==capture_plan['ENTRYPOINT_SYMBOL'])
 assert [a.arg for a in capture_fn.args.args]==['subject','bundle','result','error','context']
 assert capture_plan['ARGUMENTS']=={'subject':'stage_bundle.current','bundle':'stage_bundle','result':'stage_bundle','error':None,'context':{'source_root':str(pathlib.Path('.').resolve()),'snapshot_resolver':None}}
 assert set(capture_plan['STAGES'])=={'POST_RECORD_RESULT','POST_COLD_RESTORE'}
 assert binding['INITIAL_BUNDLE_IDENTITY']==digest({'schema':'PLANNER-BUNDLE-1','bundle':fixture},'planner-bundle-v1')
 assert binding['INITIAL_NATIVE_RESTORE_BINDING']['PATH']==initial_contract['SOURCE_PATH'] and binding['INITIAL_NATIVE_RESTORE_BINDING']['EXPECTED_IDENTITY']==initial_contract['NATIVE_BUNDLE_IDENTITY'] and not binding['INITIAL_NATIVE_RESTORE_BINDING']['RESTORE_EXECUTED']
 assert binding['EXPECTED_RECORDED_EVENT']==b['events'][-1] and binding['INVALIDATION_EVENT_IDENTITY']==independent['EVENT']
 assert len(b['events'])==20 and b['events'][:19]==fixture['events'] and b['events'][-1]['sequence']==20
 assert not binding['PROPOSED_SCOPE_ADOPTED'] and binding['SNAPSHOT_RESOLVER'] is None
 raw=bytesof({'schema':'PLANNER-BUNDLE-1','bundle':b});compare(pathlib.Path(target['EXPECTED_BYTES_EVIDENCE']).read_bytes(),raw)
 assert len(raw)==target['EXPECTED_BYTES'] and hashlib.sha256(raw).hexdigest()==target['EXPECTED_RAW_SHA256']==independent['BUNDLE']['sha256']
 for ev,entry in zip(b['events'],target['LEDGER_FILES']):
  assert entry['RAW_SHA256']==hashlib.sha256(bytesof(ev)).hexdigest() and entry['BYTES']==len(bytesof(ev)) and entry['EVENT_IDENTITY']==ev['identity']
 publication_contract(target)
 assert all(row['START_AFTER_WRITER_EXIT'] and row['FRESH_PROCESS'] for row in target['READERS']) and [r['HASH_SEED'] for r in target['READERS']]==[0,1,7,101]
 assert not b.get('dossier_materializations') and target['SNAPSHOT_ARCHIVE_FILES']==[]
 assert oracle['FULL_ORACLE_READY'] and oracle['UNDETERMINED']==[]
 assert oracle['PERSISTENCE_EXPECTATION']['OUTPUT_DIRECTORY']==target['OUTPUT_DIRECTORY'] and oracle['PERSISTENCE_EXPECTATION']['EXPECTED_SAVE_RETURN']==[{'qualification_process_path':str(pathlib.Path(target['BUNDLE_PATH']).absolute())},independent['BUNDLE']]
 results.append({'VARIANT':name,'AFTER':independent['AFTER_STATE'],'BUNDLE':independent['BUNDLE'],'EVENT':independent['EVENT'],'BYTES':len(raw),'BYTE_HASH':hashlib.sha256(raw).hexdigest(),'RESUME':resume,'WITNESSES':witnesses,'REASON_PROOF':proof,'FULL_OUTPUT_HASH':hashlib.sha256(bytesof(expected)).hexdigest(),'INDEPENDENT_COMPARISON':'PASS'})
 if len(results)==1:
  def reject(label,fn):
   try:fn()
   except (AssertionError,ValueError,KeyError,StopIteration):negatives.append({'CONTROL':label,'RESULT':'REJECTED'});return
   raise AssertionError('Negative escaped: '+label)
  def mutate(field,value):
   d=copy.deepcopy(expected);d[field]=value;complete_output(d);compare(d,expected)
  reject('WRONG_INITIAL_SNAPSHOT',lambda:compare(dict(binding['RECORD_RESULT_INPUT'],expected_snapshot=independent['AFTER_STATE']),binding['RECORD_RESULT_INPUT']))
  reject('WRONG_PARENT_IDENTITY',lambda:compare(independent['AFTER_STATE'],binding['RECORD_RESULT_PARENT_IDENTITY']))
  reject('WRONG_INVALIDATION_EVENT',lambda:compare(dict(binding['EXPECTED_RECORDED_EVENT'],identity=independent['BUNDLE']),binding['EXPECTED_RECORDED_EVENT']))
  reject('WRONG_CAPTURE_RESULT_TYPE',lambda:mutate('native_result',{'qualification_type':'TransitionReport'}))
  reject('MISSING_NATIVE_RESULT_FIELD',lambda:mutate('native_result',{'$type':'PersistenceBundle','current':b['current']}))
  reject('WRONG_BUNDLE_IDENTITY',lambda:mutate('bundle_identity',independent['AFTER_STATE']))
  reject('WRONG_SERIALIZED_BYTES',lambda:compare(raw+b'\n',raw))
  reject('CONFLICTING_SAVE_TARGET',lambda:publication_contract(dict(target,OUTPUT_DIRECTORY=str(OLD))))
  reject('SYMLINK_TARGET_CONTRACT',lambda:publication_contract(dict(target,NO_SYMLINK_PATH_COMPONENTS=False)))
  sequence=['record_result','save_bundle','publication_verified','handoff_published','writer_exit_observed','reader_launched','restore_compared'];lifecycle(sequence)
  reject('HANDOFF_SUBSTITUTED_FOR_EXIT',lambda:lifecycle([s for s in sequence if s!='writer_exit_observed']))
  reject('READER_BEFORE_WRITER_EXIT',lambda:lifecycle(sequence[:4]+['reader_launched','writer_exit_observed','restore_compared']))
  reject('CROSS_VARIANT_CONTAMINATION',lambda:mutate('typed_snapshot',fixture['current']))
  reject('FALSE_WITH_WRONG_REASON',lambda:mutate('resume',dict(resume,reasons=['HELD'])))
  reject('REASON_ORDER_MISMATCH',lambda:mutate('resume',dict(resume,reasons=list(reversed(resume['reasons'])))))
  protected=copy.deepcopy(b['current']);protected['context']['scope']='FOREIGN'
  reject('PROTECTED_STATE_MISMATCH',lambda:mutate('typed_snapshot',protected))
  reject('INCOMPLETE_FROZEN_ACCEPTANCE',lambda:compare(expected['event_identities'][1:],expected['event_identities']))
  reject('A14_AUTHORITY_REUSED',lambda:authorization({'A14_REUSED_AS_AUTHORITY':True,'EXECUTION_AUTHORIZED':False}))
  reject('STATIC_READINESS_AS_EXECUTION',lambda:authorization({'A14_REUSED_AS_AUTHORITY':False,'EXECUTION_AUTHORIZED':True}))
  missing=copy.deepcopy(expected);missing.pop('witnesses')
  reject('PARTIAL_OUTPUT_AS_FULL',lambda:complete_output(missing))
  corrupt=copy.deepcopy(b);corrupt['current']['decisions'][0]['recorded_choice']='WRONG'
  reject('WRONG_DECISION_AUTHORITY',lambda:derive(corrupt,c['actionable'],c['blocked']))
  corrupt=copy.deepcopy(b);corrupt['events'][13]['resume_binding']['sha256']='0'*64
  reject('WRONG_RESUME_BINDING',lambda:derive(corrupt,c['actionable'],c['blocked']))
  corrupt=copy.deepcopy(b);corrupt['current']['entities'][0]['generation']='FOREIGN'
  # Target the actual decision record rather than an unrelated source entity.
  rec=next(e for e in corrupt['current']['entities'] if e['id']==corrupt['current']['decisions'][0]['record']);rec['generation']='FOREIGN'
  reject('WRONG_AUTHORITY_GENERATION',lambda:derive(corrupt,c['actionable'],c['blocked']))
 assert name==binding['VARIANT_ID'] and target['CONTENT_IDENTITY']==independent['BUNDLE']
assert len(results)==2 and results[0]['BUNDLE']!=results[1]['BUNDLE']
assert all(r['INDEPENDENT_COMPARISON']=='PASS' for r in results)
process=read(E/'writer-handoff-cold-reader-contracts.json'); retry=read(E/'failure-retry-matrix.json'); readiness=read(E/'readiness-gates.json'); harness=read(E/'static-harness-contract.json'); scope=read(E/'authority-preparation-eligibility.json')
assert process['SUPERVISORS']==1 and process['WRITERS']==len(results)==2 and process['COLD_READERS']==8 and process['READERS_PER_VARIANT']==4
assert process['PLANNED_INITIAL_RESTORES']==2 and process['TOTAL_PLANNED_RESTORE_CALLS']==10 and 'INITIAL_RESTORE_SCOPE' in scope
assert process['HASH_SEEDS']==[0,1,7,101] and process['HANDOFF_NOT_EXIT_PROOF'] and process['READER_CANNOT_LAUNCH_FROM_WRITER_HANDOFF_ALONE']
assert not process['SAVE_TARGETS_CREATED'] and process['READER_OPERATIONS_EXECUTED']==0
assert process['VARIANT_ORDER']==[r['VARIANT'] for r in results]
assert len(retry)==14 and len({r['FAILURE'] for r in retry})==14 and all(r['RESULT']=='FAIL_CLOSED_NO_PASS_NO_READ_ELIGIBILITY' and not r['AUTOMATIC_RETRY_AUTHORIZED'] for r in retry)
assert all(r['RETRY_PERMITTED']==(r['FAILURE'] in ['CAPTURE_FAILURE','SAVE_FAILURE','WRITER_TERMINATION_FAILURE','MISSING_HANDOFF','COLD_READER_FAILURE']) for r in retry)
assert harness['EXISTING_V3_A15_DISPATCH_IS_NOT_THIS_SEQUENCE'] and harness['V3_SELECTED_PRESERVED']
assert readiness['FULL_A15_ORACLE_READY']==all(read(E/(r['VARIANT']+'-full-expected-output.json'))['FULL_ORACLE_READY'] for r in results)
assert readiness['STATIC_HARNESS_READY'] and readiness['AUTHORITY_PREPARATION_ELIGIBLE'] and scope['FULL_A15_ORACLE_READY'] and scope['STATIC_HARNESS_READY'] and not scope['ALL_GRANTS_ISSUED']
assert not readiness['NORMATIVE_AUTHORITY_ISSUED'] and not readiness['EXECUTION_AUTHORITY_ISSUED']
frozen=read('docs/plans/DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_EXPERIMENT_1.json')['cases'][14]
assert read(E/'frozen-acceptance-exact.json')['EXACT_CASE']==frozen
coverage=read(E/'frozen-acceptance-comparison-matrix.json');assert len(coverage['CLAUSES'])==12
for variant in [r['VARIANT'] for r in results]:
 assert {r['SOURCE_POINTER'] for r in coverage['CLAUSES'] if r['VARIANT']==variant}=={'/cases/14/'+k for k in ['INITIAL_STATE','OPERATION','EXPECTED_STATE','PERSISTENCE_REQUIREMENT','DETERMINISM_REQUIREMENT','NEGATIVE_INVARIANTS']}
register=read(E/'lessons-register-snapshot.json');prior=read(OLD/'lessons-register-snapshot.json');assert register['EVENTS'][:len(prior['EVENTS'])]==prior['EVENTS']
previous='0'*64
for ev in register['EVENTS']:
 assert ev['PREVIOUS_EVENT_HASH']==previous
 assert hashlib.sha256(json.dumps({k:v for k,v in ev.items() if k!='EVENT_HASH'},sort_keys=True,separators=(',',':')).encode()).hexdigest()==ev['EVENT_HASH'];previous=ev['EVENT_HASH']
assert len([e for e in register['EVENTS'] if e.get('WORK_PACKAGE')=='61'])==10
assert len([e for e in register['EVENTS'] if e['EVENT_TYPE']=='LESSON_RECORDED'])==10
print(json.dumps({'RESULT':'PASS','VARIANTS':results,'NEGATIVE_CONTROLS':negatives,'PROCESS_CONTRACT':{'SUPERVISORS':1,'WRITERS':2,'COLD_READERS':8,'FAILURE_CASES':14,'CONDITIONAL_STATIC_GATES':'PASS','AUTHORITY_ISSUED':False},'LESSONS_REGISTER_HEAD':previous,'NATIVE_EFFECTS':0,'RUNTIME_READERS_LAUNCHED':0},sort_keys=True))
