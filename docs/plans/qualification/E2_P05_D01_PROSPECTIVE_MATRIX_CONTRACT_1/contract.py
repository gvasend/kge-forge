"""Prospective construction specifications only: no native code imports."""
import ast
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];OUT=Path(__file__).resolve().parent;D=ROOT/'docs/plans';Q=D/'qualification';P='DETERMINISTIC_PLANNER_V0_1_'
REC=Q/'E2_P05_D01_RUNNER_INPUT_MATRIX_RECOVERY_1'
TYPE='PROSPECTIVE_D01_RUNNER_MATRIX'
def read(p):return json.loads(Path(p).read_bytes())
def rawhash(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def ref(p,pointer=''):
 p=Path(p);return dict(path=str(p.relative_to(ROOT)),pointer=pointer,raw_sha256=rawhash(p))
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def qid(kind,x):return 'qualification-prospective-D01-'+kind+'-v1:'+hashlib.sha256(canonical(x)).hexdigest()
def save(n,x):(OUT/n).write_text(json.dumps(x,sort_keys=True,indent=2)+'\n')
def demand(v,m):
 if not v:raise ValueError(m)
def oid(name):return 'D01-OBL:'+name
original=read(REC/'runner-input-matrix.json')
plan=read(D/(P+'CANONICAL_QUALIFICATION_EXPERIMENT_1.json'))
CASES={x['CASE_ID']:x for x in plan['cases'] if x['CASE_ID'].startswith(('E2-A','E2-N'))}
PHASES={'E2-A01':'INITIAL','E2-A02':'INITIAL','E2-A03':'ACQUISITION','E2-A04':'DOSSIER_PREPARATION','E2-A05':'RECORDED_DECISION','E2-A06':'REQUEST_READY_THEN_WAITING','E2-A07':'PERSISTED_EXTERNAL_CHECKPOINT','E2-A08':'COLD_RESTORED','E2-A09':'EVIDENCE_RECEIVED','E2-A10':'EVIDENCE_VALIDATED','E2-A11':'REENTRY_ELIGIBLE','E2-A12':'POST_REENTRY','E2-A13':'PROOF_FINISH','E2-A14':'GOVERNED_UNKNOWN','E2-A15':'INVALIDATED_ACCEPTED','E2-A16':'INVALIDATED_ROUTE'}
def caseid(row):return row['INPUT_ID'].split('_')[0] if row['INPUT_ID'].startswith('E2-') else 'E2-D01'
def polarity(row):
 name=row['INPUT_ID']
 return 'NEGATIVE' if name.startswith(('E2-N','MUTATION_','INVALIDATE_','CONTROL_')) else 'POSITIVE' if name.startswith(('E2-A','PHASE_')) else 'INFRASTRUCTURE_OR_COMPARISON'
def phase(row):
 name=row['INPUT_ID'];cid=caseid(row)
 return name[6:] if name.startswith('PHASE_') else PHASES.get(cid,CASES[cid]['INITIAL_STATE'] if cid in CASES else 'AGGREGATE_QUALIFICATION')
def roleid(row):
 name=row['INPUT_ID']
 if name.startswith('E2-'):return 'D01-ROLE:CASE:'+caseid(row)+(':'+name.split('_')[1])
 return 'D01-ROLE:'+name

def sealed_obligation(row):
 name=row['INPUT_ID'];cid=caseid(row)
 expectation=CASES[cid]['EXPECTED_STATE'] if cid in CASES else row['EXPECTED_SEMANTICS']
 return dict(OBLIGATION_ID=oid(name),ORIGINAL_INPUT_ID=name,ORIGINAL_ROW=row,ROW_CONTENT_ID=qid('obligation-content',row),CASE_CLASS=polarity(row),CASE_ID=cid,PHASE=phase(row),INPUT_REQUIREMENTS=dict(expected_type=row['EXPECTED_TYPE'],expected_source_class=row['EXPECTED_SOURCE_CLASS'],cardinality=row['CARDINALITY'],semantics=row['EXPECTED_SEMANTICS']),EXPECTED_BEHAVIOR=row['EXPECTED_SEMANTICS'],EXPECTED_OUTPUT=expectation,MUTATION_EXPECTATION=row['EXPECTED_SEMANTICS'] if name.startswith('MUTATION_') or cid.startswith('E2-N') else 'NO_UNDECLARED_MUTATION; unchanged fields remain invariant',INVALIDATION_EXPECTATION=row['EXPECTED_SEMANTICS'] if name.startswith('INVALIDATE_') or cid in ['E2-A15','E2-A16','E2-N04','E2-N09'] else 'NOT_APPLICABLE_UNLESS_EXPLICIT_DEPENDENCY',READER_EXPECTATION='Persisted immutable native bundle + trusted identity + original archive/source/policy/contracts; writer exited before independent readers; >=3 cold readers per checkpoint per seed',PERMUTATION_EXPECTATION='Seeds 0,1,7,101; original/reversed/rotated only for native declared unordered fields; recursive object keys; ordered causal/policy/input sequences never canonicalized as sets',COMPARISON_EXPECTATION=dict(ordering=row['ORDERING_SEMANTICS'],full_output_required=True,expected_specification=expectation,oracle_provenance=row['PROVENANCE']))

def output_contract():
 # Field sets read from native class declarations without importing or evaluating them.
 classes={}
 for source in ['adapter/planner/core.py','adapter/planner/model.py','adapter/planner/selector.py']:
  tree=ast.parse((ROOT/source).read_text())
  for n in tree.body:
   if isinstance(n,ast.ClassDef) and n.name in ['Computation','SelectionTrace','ResumeEligibility','Snapshot','PersistenceBundle','ExecutionEvent']:
    classes[n.name]=[a.target.id for a in n.body if isinstance(a,ast.AnnAssign) and isinstance(a.target,ast.Name)]
 return dict(schema='PROSPECTIVE-D01-FULL-OUTPUT-CONTRACT-1',fields=dict(qualification_label='Prospective label/context/runtime/fixture/variant provenance',typed_snapshot='Every serialized Snapshot field, including exact definition/validation/evidence/proof/result state',typed_bundle='Complete initial/current state, sources/policy, dossier bindings and ordered event ledger',Computation=classes['Computation'],selection=classes['SelectionTrace'],resume=classes['ResumeEligibility'],branches='Entire native branch/frontier member values',witnesses='All proof/reason/witness/member identities, not only control or resume scalar',rejections='Exact operation boundary, exception type/message or explicit proof/control rejection state',policy='Exact pin/version plus supported ordered policy rules',source_pins='Exact complete canonical native source membership and prefix availability',snapshot_identity='Native codec snapshot comparison identity',bundle_identity='Native canonical bundle comparison identity with resolver',event_identities='Ordered complete event/native identities, parents, pre/post and sequence',output_field_set='Closed schema; missing/extra field rejected'),native_fields=classes,canonicalization='JSON object keys canonical; native codec.SET_FIELDS only define unordered membership; ordered event/lifecycle/policy/input sequences retain order',excluded_from_semantic_identity=['pid','pid namespace','store absolute path','wall clock','test scheduling order'],process_fields_compared_separately=['writer termination','fresh reader identity/allowlist','seed','presentation','committed artifact/identity references'],expected_values_status='CONCRETE_PER_VARIANT_VALUES_NOT_SEALED',implementation_output_cannot_be_oracle=True)

# Declarative subvariants expressly present in canonical case operations.
SUBVARIANTS={'E2-N01':['NO_ROUTE'],'E2-N02':['WRONG_REQUEST','WRONG_PROPOSITION','WRONG_PRODUCER','WRONG_RECEIPT_TARGET'],'E2-N03':['SOURCE_WRONG_LINEAGE','CONTRACT_WRONG_LINEAGE','UNKNOWN_ROUTE_WRONG_LINEAGE'],'E2-N04':['EVIDENCE_INVALIDATED','ATTESTOR_INVALIDATED'],'E2-N05':['WRONG_RAW_BYTES','SAME_DIGEST_WRONG_IDENTITY_DOMAIN'],'E2-N06':['UNRELATED_GRANT','WRONG_AUTHORITY_CLASS','OUT_OF_SCOPE_GRANT'],'E2-N07':['MISSING_PROOF','WRONG_ROOT_PROOF','WRONG_SLOT_PROOF','PLACEHOLDER_PROOF'],'E2-N08':['UNDECLARED_ACTION_ID','WRONG_REFERENCE_DOMAIN'],'E2-N09':['KNOWLEDGE_SOURCE_INVALIDATED'],'E2-N10':['UNRELATED_POLICY_PIN','UNSUPPORTED_POLICY_VERSION'],'E2-N11':['EVENT_PARENT_TAMPER','CURRENT_SNAPSHOT_TAMPER','SOURCE_INDEX_TAMPER','ATTACKER_REHASH_IS_NOT_TRUST'],'E2-N12':['SELECTION_AS_COMPLETION'],'E2-N13':['DECLARATION_AS_ACTUAL_RESULT'],'E2-N14':['WAITING_TO_VALIDATE','RECEIVED_TO_REENTRY','UNRELATED_RECEIPT_ARTIFACT'],'E2-N15':['INDEPENDENT_CONDITION_UNSATISFIED'],'E2-N16':['MACHINE_FRONTIER','HUMAN_FRONTIER','FACTUAL_BLOCKED_FRONTIER']}
# Exact native errors used only where a concrete contract boundary is specified.
ERRORS={
 'E2-N01':dict(kind='CONTROL_ORACLE',expected=dict(control='PLAN_DEFECT',actionable=[],resume=False),surface='adapter/planner/core.py:_global_control and gates.governed_external_unknown'),
 'E2-N02':dict(kind='BOUNDARY_UNRESOLVED',expected='Canonical contract allows admission rejection or PLAN_DEFECT at different boundaries; concrete variant must pin exactly one before readiness',surface='adapter/planner/evidence.py:RECEIPT_CORRESPONDENCE/ENVELOPE_MISMATCH; core control oracle'),
 'E2-N03':dict(kind='BOUNDARY_UNRESOLVED',expected='Unknown-route probe: PLAN_DEFECT/no resume; source/admission context: ADMISSION_SCOPE_OR_CURRENTNESS only when that ingress boundary is explicitly selected',surface='adapter/planner/evidence.py and core._global_control'),
 'E2-N04':dict(kind='STATE_ORACLE',expected='Receipt support not current/accepted, named reentry ineligible, resume=false; original receipt history retained',surface='adapter/planner/codec.py:invalidate_sources; gates.check_receipt; core.resume_eligibility'),
 'E2-N05':dict(kind='EXACT_ERROR_BRANCHES',expected=dict(WRONG_RAW_BYTES=dict(exception='PlannerError',message_prefix='pinned source changed: ',boundary='codec.load_pinned'),SAME_DIGEST_WRONG_IDENTITY_DOMAIN=dict(exception='PlannerError',message='pin identity type/hash domain mismatch',boundary='codec.validate_pin')),surface='adapter/planner/codec.py'),
 'E2-N06':dict(kind='PROOF_ORACLE',expected='Authority predicate != PROVED; dependent ActionId absent from actionable; unrelated grant changes no root/slot',surface='adapter/planner/gates.py:evaluate_predicate'),
 'E2-N07':dict(kind='STATE_ORACLE',expected='Affected root/slot unresolved or stale; no satisfaction from PASS; exact field values require fixed predicate/claim fixture',surface='adapter/planner/core.py:evaluate_satisfaction; typed_proofs'),
 'E2-N08':dict(kind='EXACT_ERROR',expected=dict(exception='PlannerError',message='invalid prerequisite reference',boundary='model.validate_model'),surface='adapter/planner/model.py'),
 'E2-N09':dict(kind='STATE_ORACLE',expected='Producer historical completion retained; knowledge support stale, dependent prerequisite fails, descendant held/ineligible',surface='adapter/planner/codec.py:invalidate_sources; gates.current_completion'),
 'E2-N10':dict(kind='EXACT_ERROR',expected=dict(exception='PlannerError',message='unsupported selection policy identity/version binding',boundary='selector.validate_policy'),surface='adapter/planner/selector.py'),
 'E2-N11':dict(kind='EXACT_ERROR',expected=dict(exception='PlannerError',message='bundle identity mismatch',boundary='codec.restore trusted expected original identity unchanged'),surface='adapter/planner/codec.py'),
 'E2-N12':dict(kind='EXACT_ERROR_BOUNDARY_PROPOSAL',expected=dict(exception='PlannerError',message='unsupported event',boundary='core.apply_event with SelectionTrace'),surface='adapter/planner/core.py'),
 'E2-N13':dict(kind='EXACT_ERROR_BOUNDARY_PROPOSAL',expected=dict(exception='PlannerError',message='unsupported event',boundary='core.apply_event with Action.accepted_inventory declaration tuple'),surface='adapter/planner/core.py'),
 'E2-N14':dict(kind='SUBVARIANT_BOUNDARIES_NOT_SEALED',expected=dict(WAITING_TO_VALIDATE=['VALIDATION_TRANSACTION_REQUIRED when registered validation route','illegal external lifecycle transition when ordinary route'],RECEIVED_TO_REENTRY='illegal external lifecycle transition',UNRELATED_RECEIPT_ARTIFACT='receipt requires admitted concrete bytes or RECEIPT_CORRESPONDENCE according to chosen boundary'),surface='adapter/planner/core.py:apply_event/apply_receipt and evidence.apply'),
 'E2-N15':dict(kind='ELIGIBILITY_ORACLE',expected='Named-action eligibility=false and resume=false despite accepted evidence/reentry history',surface='adapter/planner/core.py:resume_eligibility'),
 'E2-N16':dict(kind='EXACT_CONTROL_BRANCHES',expected=dict(MACHINE_FRONTIER='RUNNABLE',HUMAN_FRONTIER='HUMAN_HANDOFF',FACTUAL_BLOCKED_FRONTIER='MIXED_WAIT',rule_known=False),surface='adapter/planner/core.py:_global_control')}

def variant_ids(row):
 name=row['INPUT_ID'];cid=caseid(row)
 if cid in SUBVARIANTS:return ['D01-VARIANT:'+cid+':'+s for s in SUBVARIANTS[cid]]
 if cid in CASES:return ['D01-VARIANT:'+cid+':CANONICAL_REQUIRED_BEHAVIOR']
 return ['D01-VARIANT:'+name+':REQUIRED_ROLE']

def descriptor(row):
 cid=caseid(row);name=row['INPUT_ID']
 return dict(kind='INDEPENDENT_SPECIFICATION_NOT_CONCRETE_EXPECTED_VALUE',original_requirement=CASES[cid]['EXPECTED_STATE'] if cid in CASES else row['EXPECTED_SEMANTICS'],negative_contract=ERRORS[cid] if cid in ERRORS else 'NOT_APPLICABLE_TO_THIS_OBLIGATION',full_output_contract='PROSPECTIVE-D01-FULL-OUTPUT-CONTRACT-1',concrete_expected_values='NOT_SEALED_FIXTURE_AND_RUNNER_INCOMPLETE',oracle_source=row['PROVENANCE'])

def planned_row(row):
 name=row['INPUT_ID'];cid=caseid(row)
 return dict(OBLIGATION_ID=oid(name),CASE_ID=cid,RUNNER='REQUIRED_PROSPECTIVE_AGGREGATE_RUNNER_CONTRACT; NO_SUPPORTED_UNIQUE_IMPLEMENTATION_SELECTED',FIXTURE=roleid(row),STATE_VARIANT=variant_ids(row),PHASE=phase(row),INPUTS=dict(original_type=row['EXPECTED_TYPE'],required_semantics=row['EXPECTED_SEMANTICS'],cardinality=row['CARDINALITY'],source_class=row['EXPECTED_SOURCE_CLASS'],source_identity_status='NO_CONCRETE_PROSPECTIVE_ARTIFACT_SELECTED_OR_CONSTRUCTED',scope=row['SCOPE'],lineage=row['LINEAGE']),EXPECTED_OUTPUT=descriptor(row),MUTATION_EXPECTATION=dict(dimension=row['EXPECTED_SEMANTICS'] if name.startswith('MUTATION_') or cid.startswith('E2-N') else 'NO_UNDECLARED_MUTATION',only_sealed_dimension_changes=True,unaffected_native_fields_equal=True,mutation_target_identity_status='CONCRETE_TARGET_NOT_SEALED' if name.startswith(('MUTATION_','E2-N')) else 'NOT_APPLICABLE'),INVALIDATION_EXPECTATION=dict(required_behavior=row['EXPECTED_SEMANTICS'] if name.startswith('INVALIDATE_') or cid in ['E2-A15','E2-A16','E2-N04','E2-N09'] else 'NOT_APPLICABLE_UNLESS_EXPLICIT_DEPENDENCY',only_declared_source_identity_changes=True,historical_events_retained=True),READER_MODE=dict(mode='COLD_INDEPENDENT_PROCESS',writer_termination='After complete immutable source/archive/event/bundle durability and commit acknowledgement; writer exits before reader',persisted_source='Per-variant trusted event-bearing bundle and complete archive/source/policy closure; concrete bytes not yet materialized',reader_input=['persisted bundle','trusted expected bundle identity','original Snapshot archives','pinned source bytes','exact policy pin/version','reviewed contracts','explicit source/store root'],readers_per_checkpoint_seed=3,hash_seeds=[0,1,7,101],expected_output='Full independent expected output for exact persisted variant; concrete values not yet sealed'),PERMUTATION_MODE=dict(native_unordered=['original','reversed','rotated'],recursive_object_keys=True,native_set_authority='Pinned adapter/planner/codec.py SET_FIELDS',ordered_ancestry='REORDER_MUST_REJECT',ordered_policy_rules='PRESERVE_OR_REJECT_SUBSTITUTION',ordered_other_inputs=row['ORDERING_SEMANTICS'],runner_job_list='Documentary planned-obligation IDs compared as unordered coverage; within invocation arguments and causal operations remain explicitly ordered'),COMPARISON_ORACLE=descriptor(row),REALIZATION_STATUS='PLANNED_NOT_CONSTRUCTION_READY',POSITIVE_NEGATIVE=polarity(row),provenance=row['PROVENANCE'])
