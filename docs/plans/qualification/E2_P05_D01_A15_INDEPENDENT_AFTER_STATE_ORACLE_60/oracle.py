"""Wire-level independent reference derivation. No planner transition/replay API imports."""
import pathlib,json,hashlib,copy,sys
P=pathlib.Path('docs/plans');Q=P/'qualification';E=Q/'E2_P05_D01_A15_INDEPENDENT_AFTER_STATE_ORACLE_60'
def read(p):return json.loads(p.read_text())
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def ident(x,ns):return {'$type':'ArtifactIdentity','kind':{'$enum':'IdentityKind','value':'CONTENT_IDENTITY'},'namespace':ns,'sha256':hashlib.sha256(x).hexdigest()}
def enum(name,value):return {'$enum':name,'value':value}
def sid(snapshot):return ident(canonical({'schema':'PLANNER-SNAPSHOT-1','snapshot':snapshot}),'planner-snapshot-v1')
def pin(p):return {'path':str(p),'raw_sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def write(n,x):(E/n).write_text(json.dumps(x,sort_keys=True,indent=2)+'\n')
# Wire list ordering is already canonical except modified set-valued records; preserve ordered history/reevaluations.
SNAP_SET=('actions','statuses','roots','slots','knowledge','assertions','entities','predicates','information','decisions','evidence_requirements','external_gates','receipt_admissions','boundaries','goals','validation_instances','proof_contracts','typed_proofs','installed_definitions','ingress_contracts','validation_contracts','validation_support_contracts','validation_transaction_contracts','validation_results','validation_support_records','budget_matrices')
def normalize_snapshot(s):
 for field in SNAP_SET:
  if field in s:s[field]=sorted(s[field],key=canonical)
 return s

auth={}
for pack in ['E2_P05_D01_A15_PROSPECTIVE_SCENARIO_DESIGN_59','E2_P05_D01_A15_SOURCE_RELEVANCE_STALE_WITNESS_56','E2_P05_D01_A15_PRODUCER_CURRENTNESS_SOURCE_CLOSURE_55','E2_P05_D01_SOURCE_BYTES_DISPATCH_CORRECTION_33']:
 for f,h in read(Q/pack/'evidence-index.json')['FILES'].items():
  p=pathlib.Path(f)
  if not p.exists():p=Q/pack/f
  assert hashlib.sha256(p.read_bytes()).hexdigest()==h,f
  auth[str(p)]=h
scenario=read(Q/'E2_P05_D01_A15_PROSPECTIVE_SCENARIO_DESIGN_59/concrete-scenario-specification.json');G=Q/'E2_P05_D01_A15_CAPTURE_OUTPUT_CONTRACT_36/accepted-support-graph.json';g=read(G);cap=pathlib.Path(g['CAPSULE_SOURCE']['path']);assert hashlib.sha256(cap.read_bytes()).hexdigest()==g['CAPSULE_SOURCE']['raw_sha256'];bundle=read(cap)['canonical_content']['bundle'];before=copy.deepcopy(bundle['current']);assert sid(normalize_snapshot(copy.deepcopy(before)))==g['PRESTATE_ID']==scenario['START']['SNAPSHOT']
assert len(before['assertions'])==0 and not before.get('information') and len(before['roots'])==len(before['slots'])==1
assert before['roots'][0].get('predicate') is None and before['slots'][0].get('value') is None and not before['slots'][0].get('requirements',[]) and not before['slots'][0].get('root_requirements',[])
assert all(r['id']['value']=='E2-FINISH' or r['state']['value']=='COMPLETED' for r in before['statuses'])
contract_provenance=min(before['proof_contracts'],key=lambda c:c['id']['sha256'])['provenance']
rows=[]
for variant in scenario['VARIANTS']:
 source=variant['INITIAL_TARGET_CONTENT_IDENTITY'];assert variant['START_SNAPSHOT']==sid(before)
 proof=next(p for p in before['typed_proofs'] if p['id']==variant['WITNESS_PROOF_ID']);assert proof['provenance']['identity']==source and proof.get('validation',enum('ValidationState','ACCEPTED'))['value']=='ACCEPTED'
 for collection in ['actions','knowledge','decisions','external_gates','evidence_requirements','validation_instances','validation_results','receipt_admissions']:
  for record in before[collection]:
   if 'provenance' in record:assert record['provenance']['identity']!=source
 assert all(source not in record.get('inputs',record.get('input_identities',[])) for record in before['validation_instances']+before['validation_results'])
 assert all(source!=p['identity'] for a in before['receipt_admissions'] for p in a.get('dependencies',[]))
 assert all(a['source']['identity']!=source and all(k['provenance']['identity']!=source for k in a['accepted_inventory']) for a in before['actions'])
 after=copy.deepcopy(before)
 changes=[]
 # Exact conditional codec branches supported by independently pinned variant role witnesses.
 for collection in ('proof_contracts','typed_proofs'):
  for record in after[collection]:
   if record['provenance']['identity']==source:
    record['validation']=enum('ValidationState','STALE');changes.append({'COLLECTION':collection,'ID':record['id'],'FIELD':'validation','EXPECTED':'STALE','RULE':'Own provenance equality'})
 for record in after['entities']:
  if record['provenance']['identity']==source:
   record['validation']=enum('ValidationState','STALE');changes.append({'COLLECTION':'entities','ID':record['id'],'FIELD':'validation','EXPECTED':'STALE','RULE':'Source entity provenance equality'})
 touched=variant['EXPECTED_STALE_INSTALLED_ROLES']
 for record in after['installed_definitions']:
  if record['id'] in touched:
   record['validation']=enum('ValidationState','STALE');changes.append({'COLLECTION':'installed_definitions','ID':record['id'],'FIELD':'validation','EXPECTED':'STALE','RULE':'Exact source membership in installed support IDs'})
 assert variant['COMMON_CONFIGURATION'] in touched and len(touched)==2
 # Shared installed configuration is stale: both contract_current checks fail, so no usable proof remains.
 for slot in after['slots']:slot['state']=enum('SlotState','UNRESOLVED')
 for root in after['roots']:root['state']=enum('ConditionState','UNRESOLVED')
 normalize_snapshot(after)
 support_state=sid(after) # Native reevaluation support snapshot precedes updated status/record append.
 finish_id={'$type':'ActionId','value':'E2-FINISH'}
 for status in after['statuses']:
  if status['id']==finish_id:status['state']=enum('ActionState','BLOCKED')
 reevaluation={'$type':'ReevaluationRecord','dependencies':[source],'action':finish_id,'old_state':enum('ActionState','ACTIONABLE'),'support_state':support_state,'new_state':enum('ActionState','BLOCKED'),'provenance':copy.deepcopy(contract_provenance)}
 after['reevaluations'].append(reevaluation);normalize_snapshot(after)
 after_id=sid(after)
 # Native shape of expected trace only: no operative descriptor/transaction object constructed.
 result_projection={'$type':'SourceInvalidation','changed':[source],'expected_snapshot':g['PRESTATE_ID']}
 event_body={'sequence':20,'parent':g['PRESTATE_ID'],'parent_event':bundle['events'][-1]['identity'],'result':result_projection,'after':after_id}
 event_identity=ident(canonical(event_body),'planner-event-v1')
 event={'$type':'ExecutionEvent','sequence':20,'parent_snapshot':g['PRESTATE_ID'],'parent_event':bundle['events'][-1]['identity'],'result':result_projection,'after_snapshot':after_id,'identity':event_identity}
 expected_bundle=copy.deepcopy(bundle);expected_bundle['current']=after;expected_bundle['events'].append(event)
 raw=canonical({'schema':'PLANNER-BUNDLE-1','bundle':expected_bundle});bundle_id=ident(raw,'planner-bundle-v1')
 computation={'actionable':[],'statuses':copy.deepcopy(after['statuses']),'blocked':[[finish_id,['PRIOR_ATTEMPT_HOLD:BLOCKED']]],'selection':None,'defects':['UNRESOLVED_GOAL_WITHOUT_CONTROL_PATH'],'human_batches':[],'human_routing':enum('HumanRouting','NO_INTERNAL_ACTION'),'control':enum('ControlState','PLAN_DEFECT'),'frontier':[],'branches':[[{'$type':'ConditionId','value':'E2-ROOT'},enum('BranchState','DEPENDENCY_BLOCKED')]],'unresolved_roots':1,'unresolved_slots':1}
 # Native route set remains E2-REENTER (completed), no actionable named action after independent blocking.
 reasons=sorted(['EXTERNAL:E2-GATE:NAMED_REENTRY_NOT_ACTIONABLE','EXTERNAL:E2-GATE:E2-REENTER:COMPLETED_OR_UNAVAILABLE','DECISION:E2-DECIDE:NAMED_REENTRY_NOT_ACTIONABLE','DECISION:E2-DECIDE:E2-REENTER:COMPLETED_OR_UNAVAILABLE'])
 resume={'$type':'ResumeEligibility','allowed':False,'actions':[],'reasons':reasons,'supporting_identities':[]}
 preserved=[k for k in before if k not in ('entities','installed_definitions','proof_contracts','typed_proofs','slots','roots','statuses','reevaluations')]
 assert all(after[k]==before[k] for k in preserved)
 assert expected_bundle['events'][:19]==bundle['events']
 oracle={'VARIANT_ID':variant['VARIANT_ID'],'STATUS':'INDEPENDENT_RULE_DERIVED_EXPECTATION_NOT_RUNTIME_RESULT','INITIAL_SNAPSHOT':g['PRESTATE_ID'],'SOURCE_CONTENT_IDENTITY':source,'EXPECTED_STATE':after,'EXPECTED_STATE_IDENTITY':after_id,'PROOF_VALIDATION':[{'PROOF_IDENTITY':p['id'],'BEFORE':'ACCEPTED','GUARD':p['provenance']['identity']==source,'EXPECTED_AFTER':'STALE' if p['provenance']['identity']==source else 'ACCEPTED'} for p in before['typed_proofs']],'PROOF_USABILITY':[{'PROOF_IDENTITY':p['id'],'EXPECTED':False,'REASON':'Common configuration/contract currentness withdrawn; matching proof additionally stale'} for p in before['typed_proofs']],'TARGET_SATISFACTION':{'E2-SLOT':'UNRESOLVED','E2-ROOT':'UNRESOLVED'},'ADMISSION_STALE':{'PROOF_ID':proof['id'],'CURRENT_FIELD':'validation','EXPECTED':'STALE','ORIGINAL_OCCURRENCE':variant['WITNESS_ADMISSION_EVENT_ID'],'IMMUTABLE_EVENT_PRESERVED':True},'EXPECTED_COMPUTATION':computation,'EXPECTED_RESUME':resume,'EXPECTED_TRANSITION_REPORT':{'snapshot':after,'action_transitions':[],'computation':computation},'ORDERED_TRACE':{'EXPECTED_PREFIX':bundle['events'],'EXPECTED_NEXT_EVENT':event,'LOGICAL_EFFECTS_NOT_ADDITIONAL_EVENTS':True,'EXPECTED_REEVALUATION':reevaluation},'CAPTURE_EXPECTATION':{'EXPECTED_UPDATED_BUNDLE':expected_bundle,'EXPECTED_BUNDLE_ID':bundle_id,'EVENT_ID':event_identity,'ACTUAL_CAPTURE_INVOKED':False},'PERSISTENCE_EXPECTATION':{'BUNDLE_FORMAT':'PLANNER-BUNDLE-1','EXPECTED_BUNDLE_BYTE_LENGTH':len(raw),'EXPECTED_BUNDLE_BYTE_HASH':hashlib.sha256(raw).hexdigest(),'EXPECTED_NATIVE_BUNDLE_ID':bundle_id,'EXPECTED_BUNDLE_FILENAME':'bundle-'+bundle_id['sha256']+'.json','EXPECTED_EVENT_FILENAME':'event-'+event_identity['sha256']+'.json','EXPECTED_EVENT_BYTE_HASH':hashlib.sha256(canonical(event)).hexdigest(),'REQUIRED_SOURCE_POLICY_PINS':bundle['sources']+[bundle['policy']],'OUTPUT_DIRECTORY':'UNBOUND_HARNESS','DOSSIER_ARCHIVE_REFERENCES':[],'ARCHIVE_DERIVATION':'Existing input has no dossier_materializations; expected update changes only current/events, so save archive guard remains empty' },'RESTORE_EXPECTATION':{'EXPECTED_BUNDLE':expected_bundle,'EXPECTED_CURRENT_SNAPSHOT':after_id,'EXPECTED_RECOMPUTATION':computation,'EXPECTED_RESUME':resume,'NATIVE_RESTORE_INVOKED':False},'PROTECTED_STATE_COMPARISONS':{'IMMUTABLE_EVENT_PREFIX':True,'UNCHANGED_COLLECTIONS':preserved,'UNCHANGED_POLICY_SOURCES_CONTEXT_KNOWLEDGE':True,'EXACT_EXPECTED_CHANGED_FIELDS':changes,'EXPECTED_NEW_REEVALUATION':reevaluation,'FRAME_ORACLE_COMPLETE_FOR_EXPECTED_STATE':True},'UNDETERMINED':['Exact full-output capture observation point/native_result type and updated-bundle binding: V3 current apply_event capture retains old bundle/history','Independent complete resume-route/reason comparison derivation and comparison DTO must be sealed without calling replay; expected four reasons are a rule-derived candidate'],'FULL_ORACLE_READY':False}
 rows.append(oracle)
 if '--stdout' not in sys.argv:write(variant['VARIANT_ID']+'-expected-output.json',oracle)
semantic_id='qualification-A15-reference-oracle-v1:'+hashlib.sha256(canonical(rows)).hexdigest()
if '--stdout' in sys.argv:print(json.dumps({'IDENTITY':semantic_id,'VARIANTS':[{'ID':r['VARIANT_ID'],'EXPECTED_AFTER':r['EXPECTED_STATE_IDENTITY']['sha256'],'EVENT_ID':r['ORDERED_TRACE']['EXPECTED_NEXT_EVENT']['identity']['sha256'],'BUNDLE_ID':r['CAPTURE_EXPECTATION']['EXPECTED_BUNDLE_ID']['sha256']} for r in rows],'NATIVE_TRANSITIONS':0},sort_keys=True));sys.exit()
write('reference-rule-derivation.json',{'METHOD':'Independent wire-level conditional rules; no imports of adapter modules or native transition/query-after-state functions','INPUT':pin(cap),'ASSUMPTIONS':'Exact two proposed singleton sources; fixed scope; verified common configuration and unchanged producer/receipt/other source guards; new prospective coverage is unadopted','RULES':[{'SOURCE':pin(pathlib.Path('adapter/planner/codec.py')),'LOCATION':'invalidate_sources proof/entity/installed guards; snapshot/event/bundle canonical identity rules'},{'SOURCE':pin(pathlib.Path('adapter/planner/typed_proofs.py')),'LOCATION':'contract_current/usable/derive/affected_actions/reevaluate'},{'SOURCE':pin(pathlib.Path('adapter/planner/core.py')),'LOCATION':'actionability/global control/resume_eligibility'}],'EXPECTED_STATE_DERIVED_FROM_ACTUAL_AFTER_STATE':False,'NATIVE_APPLY_INVALIDATE_RECORD_SAVE_REPLAY_RESTORE_CALLED':False,'ORACLE_IDENTITY':semantic_id})
write('authentication.json',{'PACKAGE59_AUTHENTICATED':True,'AUTHORITATIVE_FILES':auth,'STARTING_SNAPSHOT':g['PRESTATE_ID'],'ORACLE_IDENTITY':semantic_id,'VARIANT_OUTPUT_FILES':[r['VARIANT_ID']+'-expected-output.json' for r in rows]})
