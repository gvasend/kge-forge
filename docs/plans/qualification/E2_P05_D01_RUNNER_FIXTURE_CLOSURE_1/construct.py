"""Static orchestration/fixture construction; no semantic operation invoked."""
import ast
from copy import deepcopy
from common import *
from adapter.planner import codec as c
# Only structural codec decoding/wiring is used. Never call native validators,
# recompute, apply, save, restore, prepare, commit or qualification drivers here.
sealed=read(PRIOR/'sealed-128-obligations.json');plans=read(PRIOR/'planned-realization-matrix.json')['rows']
variants=read(PRIOR/'state-variant-declarations.json');original={o['ORIGINAL_INPUT_ID']:o for o in sealed['obligations']}
demand(len(original)==128,'FROZEN_128')
supported={name:dict(module=v[0],entrypoint=v[1],input_type=v[2],output_type=v[3],persistence_effect=v[4],replay_effect=v[5]) for name,v in OPERATIONS.items()}
# Closed argument schemas; bindings are specified at construction, not inferred by run-time input values.
ARGUMENTS={'MODEL_VALIDATE':['snapshot'],'RECOMPUTE':['snapshot'],'APPLY_RESULT':['snapshot','supplied'],'DOSSIER_RESULT':['snapshot','supplied','validation_instances'],'RECORD_RESULT':['bundle','supplied'],'RECORDED_DECISION':['snapshot','recorded_decision'],'APPLY_EVENT':['snapshot','event'],'RECEIPT_PHASE':['snapshot','event'],'SAVE_BUNDLE':['bundle','output_dir','repo_root'],'RESTORE':['bundle_path','expected_bundle_identity','repo_root'],'EVIDENCE_ADMISSION':['bundle','request','source_bytes','output_dir','repo_root'],'EVIDENCE_APPLY':['snapshot','request'],'VALIDATION_APPLY':['snapshot','validation_admission'],'VALIDATION_COMMIT':['bundle','validation_admission','output_dir','repo_root'],'RESUME':['bundle','source_root'],'SATISFACTION':['snapshot'],'INVALIDATE_EVENT':['snapshot','event'],'PREDICATE':['snapshot','predicate_id'],'LOAD_PIN':['source_root','pin'],'VALIDATE_PIN':['pin'],'VALIDATE_POLICY':['policy','policy_version'],'BUNDLE_VALIDATE':['bundle'],'SNAPSHOT_ID':['snapshot'],'BUNDLE_ID':['bundle'],'COMMIT_EVENT':['bundle','event','output_dir','repo_root'],'QUALIFICATION_METADATA':[]}
CONTROL_PATHS={0:['EVIDENCE_APPLY'],1:['LOAD_PIN'],2:['INVALIDATE_EVENT'],3:['PREDICATE','RECOMPUTE'],4:['SATISFACTION'],5:['INVALIDATE_EVENT','RECOMPUTE'],6:['RESTORE'],7:['RESTORE'],8:['EVIDENCE_APPLY'],9:['EVIDENCE_APPLY'],10:['QUALIFICATION_METADATA']}
MUTATION_PATHS={'SOURCE':['LOAD_PIN'],'LINEAGE':['EVIDENCE_APPLY'],'AUTHORITY':['PREDICATE','RECOMPUTE'],'PROOF':['SATISFACTION'],'ROUTE':['RECOMPUTE'],'PERSISTENCE':['RESTORE']}
dispatch={};native_map=[]
for name,ob in original.items():
 ops=CONTROL_PATHS[int(name.split('_')[1])] if name.startswith('CONTROL_') else MUTATION_PATHS[name[9:]] if name.startswith('MUTATION_') else operation_path(name)
 did='D01-DISPATCH:'+name;steps=[]
 for i,symbol in enumerate(ops):
  v=OPERATIONS[symbol]
  steps.append(dict(operation_id=symbol,args=[{'fixture_field':f} for f in ARGUMENTS[symbol]],kwargs={},bind_result_as='step_'+str(i)+'_native_result'))
 dispatch[did]=dict(dispatch_id=did,obligation_id=ob['OBLIGATION_ID'],operation_ids=ops,steps=steps,runtime_operation_selection=False,semantic_transition_owner='EXISTING_NATIVE_FUNCTIONS_ONLY; qualification metadata has no Planner transition')
 native_map.append(dict(OBLIGATION_ID=ob['OBLIGATION_ID'],RUNNER_DISPATCH_ID=did,NATIVE_ENTRYPOINT=[v[0]+'.'+v[1] if v[0] else 'NOT_A_PLANNER_TRANSITION' for v in [OPERATIONS[s] for s in ops]],INPUT_TYPE=[OPERATIONS[s][2] for s in ops],OUTPUT_TYPE=[OPERATIONS[s][3] for s in ops],MUTATION_AUTHORITY='No authority from dispatch; normal per-native-operation applicability and explicit later qualification scope required',PERSISTENCE_EFFECT=[OPERATIONS[s][4] for s in ops],REPLAY_EFFECT=[OPERATIONS[s][5] for s in ops],all_targets_present=True,concrete_operands_complete=False))
save('dispatch-table.json',dispatch);save('supported-operation-set.json',supported);save('native-operation-coverage.json',native_map)
# Strict native source roles: no writer-fidelity data is promoted to an independent oracle.
selection=read(Q/'E2_P05_PC03_END_BINDING_1/selected-source-collection.json');models={x['model_id']:x for x in selection['native_models']}
def load_model(mid):
 source=models[mid]['source'];demand(filehash(ROOT/source['path'])==source['raw_sha256'],'MODEL_PIN')
 data=at(read(ROOT/source['path']),source['pointer'])
 b=data['bundle'] if models[mid]['type']=='PersistenceBundle' else None
 return deepcopy(b['current'] if b else data),deepcopy(b),source
sources={k:load_model(k) for k in models}
a03_path=Q/'E2_P05_A03_PROSPECTIVE_OCCURRENCE_CONTRACT_1/inputs/starting-bundle.json'
a03=read(a03_path)['bundle'];sources['A03_START']=(a03['current'],a03,ref(a03_path))
a06sealed=read(Q/'E2_P05_A06_PROSPECTIVE_REQUEST_WAIT_CONTRACT_1/sealed-fixtures.json')['primary'];a06_path=ROOT/a06sealed['START_PATH']['path'];a06=read(a06_path)['bundle'];sources['A06_START']=(a06['current'],a06,ref(a06_path))
# A04 prestate is the exact independently qualified A03 post-state; no result applied to manufacture it.
BASE={'E2-A01':'ORIGINAL_INITIAL_MODEL','E2-A02':'ORIGINAL_INITIAL_MODEL','E2-A03':'A03_START','E2-A04':'A03_QUALIFIED_POST_STATE','E2-A06':'A06_START','E2-A07':'A06_QUALIFIED_POST_STATE','E2-A08':'A06_QUALIFIED_POST_STATE','E2-A09':'P04_FINAL_PREEXECUTION','E2-A10':'P04_POST_A09','E2-A11':'P04_POST_A10','E2-A12':'P04_POST_A11','E2-A13':'P04_ROOT_CONTRACT','E2-N02':'P04_FINAL_PREEXECUTION','E2-N03':'P04_FINAL_PREEXECUTION','E2-N04':'P04_POST_A10','E2-N05':'P04_FINAL_PREEXECUTION','E2-N06':'P04_POST_A11','E2-N07':'P04_POST_A12','E2-N08':'ORIGINAL_INITIAL_MODEL','E2-N09':'A03_QUALIFIED_POST_STATE','E2-N10':'P04_FINAL_PREEXECUTION','E2-N11':'P04_FINAL_PREEXECUTION','E2-N12':'ORIGINAL_INITIAL_MODEL','E2-N13':'ORIGINAL_INITIAL_MODEL','E2-N14':'P04_POST_A09','E2-N15':'P04_POST_A11'}
# No convenient wrong-state source for governed unknown/N16 or historical original phase scaffolds.
PHASE_BASE={'INITIAL':'ORIGINAL_INITIAL_MODEL','EXTERNAL_CHECKPOINT':'A06_QUALIFIED_POST_STATE','COLD_RESTORED':'A06_QUALIFIED_POST_STATE','EVIDENCE_RECEIVED':'P04_POST_A09','EVIDENCE_VALIDATED':'P04_POST_A10','REENTRY_ELIGIBLE':'P04_POST_A11'}
request=read(Q/'E2_P04_CANONICAL_EXECUTION_RETRY_1/a09-command.json')
catalog={};status=[];independence=[]
for var in variants:
 vid=var['VARIANT_ID'];cid=var['CASE_ID'];tag=vid.rsplit(':',1)[-1];name=var['source_obligation'][len('D01-OBL:'):]
 base=BASE.get(cid)
 if name.startswith('PHASE_'):base=PHASE_BASE.get(name[6:])
 if cid=='E2-D01' and not name.startswith('PHASE_'):
  base='P04_FINAL_PREEXECUTION' if name.startswith(('INVALIDATE_','MUTATION_','CONTROL_')) or name in ['TRUSTED_NATIVE_BUNDLES','ORDERED_EVENT_ANCESTRY','SOURCE_BYTES','POLICY','CONTEXT_AND_DEFINITIONS','POST_SNAPSHOT_ARCHIVES','COLD_READER_PROCESS','WRITER_PROCESS'] else 'ORIGINAL_INITIAL_MODEL'
 if base is None:
  status.append(dict(variant=vid,status='NOT_MATERIALIZED_NO_EXACT_BASE_ROLE',reason='No source selected that satisfies this concrete precondition; abstract historical phase/scoped source cannot substitute'))
  continue
 state,bundle,source=deepcopy(sources[base]);candidate=deepcopy(state);args={};delta=[];complete=False
 # Pure construction of a negative argument, never a semantic result/state transition.
 if cid=='E2-N08':
  act=next(a for a in candidate['actions'] if a['id']['value']=='E2-PREPARE')
  act['prerequisites'].append({'$type':'Gate','kind':{'$enum':'GateKind','value':'ACTION_COMPLETED'},'target':{'$type':'ActionId' if tag=='UNDECLARED_ACTION_ID' else 'ConditionId','value':'PROSPECTIVE-D01-UNDECLARED'}})
  delta=['actions[E2-PREPARE].prerequisites'];args['snapshot']=candidate;complete=True
 elif cid=='E2-N10':
  args['policy']=deepcopy(bundle['policy']);args['policy_version']=bundle['policy_version']
  if tag=='UNRELATED_POLICY_PIN':args['policy']['identity']['sha256']='0'*64;delta=['policy.identity.sha256']
  else:args['policy_version']='PROSPECTIVE-D01-UNSUPPORTED-POLICY-VERSION';delta=['policy_version']
  complete=True
 elif cid=='E2-N05':
  pin=deepcopy(bundle['sources'][0]);args['pin']=pin
  if tag=='SAME_DIGEST_WRONG_IDENTITY_DOMAIN':pin['identity']['kind']['value']='AUTHORITY_IDENTITY';delta=['pin.identity.kind'];complete=True
  else:delta=['designated source bytes'];complete=False
 elif cid=='E2-N12':
  args['event']={'qualification_type':'SelectionTrace','selected':{'$type':'ActionId','value':'E2-CHECK'},'criterion':1,'steps':[]};args['snapshot']=state;delta=[];complete=True
 elif cid=='E2-N13':
  args['event']=next(a for a in state['actions'] if a['id']['value']=='E2-CHECK')['accepted_inventory'];args['snapshot']=state;complete=True
 elif cid=='E2-N14':
  if tag=='WAITING_TO_VALIDATE':state,bundle,source=deepcopy(sources['P04_FINAL_PREEXECUTION'])
  event={'$type':'ExternalEvent','gate':{'$type':'GateId','value':'E2-GATE'},'stage':{'$enum':'ExternalStage','value':'EVIDENCE_VALIDATED' if tag=='WAITING_TO_VALIDATE' else 'DEPENDENT_ACTION_REENTRY' if tag=='RECEIVED_TO_REENTRY' else 'EVIDENCE_RECEIVED'},'expected_snapshot':{'$type':'ArtifactIdentity','kind':{'$enum':'IdentityKind','value':'CONTENT_IDENTITY'},'namespace':'planner-snapshot-v1','sha256':__import__('hashlib').sha256(canonical({'schema':'PLANNER-SNAPSHOT-1','snapshot':c._wire(c._unwire(state))})).hexdigest()},'artifact':None}
  if tag=='UNRELATED_RECEIPT_ARTIFACT':
   state,bundle,source=deepcopy(sources['P04_FINAL_PREEXECUTION']);event['artifact']={'$type':'EntityId','value':'PROSPECTIVE-D01-UNRELATED-RECEIPT'}
   event['expected_snapshot']['sha256']=__import__('hashlib').sha256(canonical({'schema':'PLANNER-SNAPSHOT-1','snapshot':c._wire(c._unwire(state))})).hexdigest()
  args={'snapshot':state,'event':event};delta=['ExternalEvent.stage/artifact'];complete=True
 # Default typed parameters are exact source objects, not expected post-state/oracle data.
 args.setdefault('snapshot',state)
 if bundle:
  args.setdefault('bundle',bundle)
  args.setdefault('policy',bundle['policy']);args.setdefault('policy_version',bundle['policy_version'])
 if cid in ['E2-A01','E2-A02']:complete=True
 native=c._unwire(state) # structural types only
 normalized=c._wire(native)
 fid='D01-FIXTURE:'+vid.split('D01-VARIANT:',1)[1]
 members=[r for r in plans if vid in r['STATE_VARIANT']]
 content=dict(subject=normalized,bundle=deepcopy(bundle),arguments=args,mutation_fields=delta,source=source,scope=normalized.get('context',{}).get('scope'),lineage=normalized.get('context',{}).get('lineage'),generation=normalized.get('context',{}).get('generation'))
 packet=dict(schema='PROSPECTIVE-D01-CONSTRUCTION-FIXTURE-1',fixture_id=fid,role_ids=sorted({r['FIXTURE'] for r in members}),state_variant_id=vid,native_type='Snapshot',canonical_content=content,content_identity=qid('fixture-content',content),source_construction_rule='Exact retained native input state plus explicitly listed pure argument mutation; no apply/restore/commit/recompute called',execution_inputs_complete=complete,precondition_assurance='STRUCTURAL_INPUT_SUBJECT_ONLY; full row invocation/process context may remain incomplete',oracle_independence='No expectation files opened by native producer/operation; payload does not include future expected outputs',provenance=[source],historical_reconstruction=False)
 fname='fixtures/'+vid.replace(':','__')+'.json';save(fname,packet)
 catalog[fid]=dict(fixture_id=fid,state_variant_id=vid,role_ids=packet['role_ids'],artifact=ref(OUT/fname),content_identity=packet['content_identity'],native_type='Snapshot',operative_arguments_complete=complete,role_preconditions_complete=cid in ['E2-A01','E2-A02','E2-N08','E2-N10','E2-N12','E2-N13','E2-N14'])
 status.append(dict(variant=vid,status='CONCRETE_STRUCTURAL_INPUT_MATERIALIZED',fixture_id=fid,arguments_complete=complete,full_row_complete=False))
 independence.append(dict(fixture_id=fid,expected_output_encoded_as_operand=False,input_source=source,independent_expected_output_reference=None,full_output_oracle_status='NOT_SEALED'))
save('fixture-catalog.json',catalog);save('state-variant-closure.json',status);save('fixture-oracle-independence.json',independence)
# Exact negative *boundary contracts* separately from complete fixture and full-output qualification.
boundaries={
 'E2-N01':('core.recompute','NO_ROUTE','control=PLAN_DEFECT; actionable empty; resume false','OBSERVATION_ONLY'),
 'E2-N02':('evidence.apply','Well-formed parent/key; wrong request/proposition/producer/target','Variant-specific RECEIPT_CORRESPONDENCE / ROUTE_NOT_CURRENT / SOURCE_PROVENANCE; guards require individually sealed argument closure','UNRESOLVED_VARIANT_ARGUMENT_CLOSURE'),
 'E2-N03':('evidence.apply','Well-formed parent/key; wrong native source/contract context','ADMISSION_SCOPE_OR_CURRENTNESS or ENVELOPE_MISMATCH by exact variant; unknown-route probe requires recompute PLAN_DEFECT','UNRESOLVED_VARIANT_ARGUMENT_CLOSURE'),
 'E2-N04':('core.apply_event','Exact SourceInvalidation on Evidence or attestor support','Current receipt support withdrawn; resume false; original history retained','NATIVE_INVALIDATION'),
 'E2-N05':('codec.load_pinned / codec.validate_pin','Exact pin bytes changed / identity kind changed','pinned source changed: <sealed relative path> / pin identity type/hash domain mismatch','NO_WRITE'),
 'E2-N06':('gates.evaluate_predicate','Authority candidate unrelated/wrong class/out of scope','state != PROVED; named action ineligible','NO_WRITE'),
 'E2-N07':('core.evaluate_satisfaction','Exact missing/wrong/placeholder proof dimension','Affected root/slot unresolved or stale; no satisfaction from PASS','PURE_NATIVE_PROJECTION'),
 'E2-N08':('model.validate_model','Snapshot has dangling or wrong-domain ACTION_COMPLETED reference','PlannerError: invalid prerequisite reference','NO_WRITE'),
 'E2-N09':('core.apply_event','Exact knowledge SourceInvalidation with trusted pre-Snapshot','Knowledge current support stale; descendant prerequisite fails; history retained','NATIVE_INVALIDATION'),
 'E2-N10':('selector.validate_policy','Wrong supported pin or unsupported policy version','PlannerError: unsupported selection policy identity/version binding','NO_WRITE'),
 'E2-N11':('codec.restore','Tampered bytes; original trusted expected bundle identity retained','PlannerError: bundle identity mismatch','NO_WRITE'),
 'E2-N12':('core.apply_event','SelectionTrace qualification record supplied as event','PlannerError: unsupported event','NO_WRITE'),
 'E2-N13':('core.apply_event','Action output declaration tuple supplied as event','PlannerError: unsupported event','NO_WRITE'),
 'E2-N14':('core.apply_event','Registered waiting validation / received premature reentry / unrelated receipt artifact','VALIDATION_TRANSACTION_REQUIRED / illegal external lifecycle transition / receipt requires admitted concrete bytes','NO_WRITE'),
 'E2-N15':('core.resume_eligibility','Valid receipt/reentry but named action independent condition unsatisfied','allowed=false; named action absent from resume.actions','NO_WRITE'),
 'E2-N16':('core.recompute','Machine / human / factual-frontier variants of governed unknown','RUNNABLE / HUMAN_HANDOFF / MIXED_WAIT respectively; rule remains unknown','OBSERVATION_ONLY')}
save('negative-boundary-contracts.json',{cid:dict(NEGATIVE_CASE_ID=cid,OPERATION=v[0],PRECONDITION=v[1],EXPECTED_REJECTION=v[2],EXPECTED_STATE_EFFECT=v[3],EXPECTED_PERSISTENCE_EFFECT='No admission/publication for error-only probes; invalidation applies only to isolated future native candidate',status='BOUNDARY_DEFINED_NOT_FULLY_SEALED' if cid in ['E2-N02','E2-N03'] else 'EXACT_NATIVE_BOUNDARY_CONTRACT; fixture/complete output closure still required') for cid,v in boundaries.items()})
# Report missing complete outputs rather than promoting old writer-fidelity comparisons.
oracle_inventory=[]
for row in plans:
 oid=row['OBLIGATION_ID'];name=oid[len('D01-OBL:'):];cid=row['CASE_ID']
 model_candidate=BASE.get(cid)
 src=models.get(model_candidate,{}).get('semantic_oracle')
 oracle_inventory.append(dict(obligation_id=oid,expected_full_output_oracle_id=None,status='NOT_SEALED_COMPLETE_FULL_OUTPUT',independent_required_specification=row['COMPARISON_ORACLE'],retained_comparison_candidate=src,retained_candidate_assurance=models.get(model_candidate,{}).get('oracle_role'),not_promoted_to_independent_full_output=True,missing_fields=['Complete Computation','complete witnesses/resume values','full post-state/bundle/event values and identities','case-specific exact before/after persistence effect']))
save('full-output-oracle-closure.json',oracle_inventory)
rows=[]
for r in plans:
 fid=[k for k,f in catalog.items() if f['state_variant_id'] in r['STATE_VARIANT']]
 rows.append(dict(OBLIGATION_ID=r['OBLIGATION_ID'],CASE_ID=r['CASE_ID'],RUNNER_DISPATCH_ID='D01-DISPATCH:'+r['OBLIGATION_ID'][len('D01-OBL:'):],NATIVE_OPERATION=dispatch['D01-DISPATCH:'+r['OBLIGATION_ID'][len('D01-OBL:'):]]['operation_ids'],FIXTURE_IDS=fid,STATE_VARIANT_IDS=r['STATE_VARIANT'],INPUT_IDENTITIES=[catalog[k]['content_identity'] for k in fid],EXPECTED_FULL_OUTPUT_ORACLE_ID=None,EXPECTED_MUTATION=r['MUTATION_EXPECTATION'],EXPECTED_INVALIDATION=r['INVALIDATION_EXPECTATION'],READER_MODE=r['READER_MODE'],PERMUTATION_MODE=r['PERMUTATION_MODE'],EXPECTED_COMPARISON=r['COMPARISON_ORACLE'],EXPECTED_FAILURE_BOUNDARY=boundaries.get(r['CASE_ID']),COMPLETE=False))
save('partial-construction-index.json',dict(kind='NOT_COMPLETE_PROSPECTIVE_MATRIX',rows=rows,row_count=128,complete_rows=0,construction_ready=False))
normalization=read(PRIOR/'full-output-comparison-contract.json');normalization['fields']['native_result']='Complete native return value; process-only location recorded separately, never normalized in native provenance'
normalization['normalization_limit']='Native SET_FIELDS only; no identity, error, scope, lineage, provenance, parent, sequence, or ledger-position erasure'
save('normalization-and-output-schema.json',normalization)
runner_identity_body=dict(label='PROSPECTIVE_RUNNER',source=ref(OUT/'runner.py'),helpers=ref(OUT/'common.py'),dispatch=ref(OUT/'dispatch-table.json'),supported_operation_set=ref(OUT/'supported-operation-set.json'),output_schema=ref(OUT/'normalization-and-output-schema.json'),runtime_pins=[ref(p) for p in sorted((ROOT/'adapter/planner').glob('*.py'))],execution_gate='Complete matrix plus trusted externally verified qualification scope; no wire callable or implicit hash authority')
save('runner-source-seal.json',dict(identity=qid('aggregate-orchestration-source',runner_identity_body),body=runner_identity_body,complete_executable_matrix=False))
print('CONSTRUCTION_SOURCE_DISPATCH_SEALED; STATIC_FIXTURE_CAPSULES='+str(len(catalog))+'; FULL_ORACLES=0/128')
