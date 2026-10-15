"""Seal an A05-only acceptance overlay. No native authority or event is created."""
import copy
import hashlib
import json
from pathlib import Path

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
RECOVERY=ROOT/'docs/plans/qualification/E2_P05_A05_DECISION_ANCESTRY_RECOVERY_1'
PREFIX='docs/plans/DETERMINISTIC_PLANNER_V0_1_'
OPTION='AUTHORIZE_P05_A05_ALTERNATE_NATIVE_EVIDENCE'
SUBJECT='qualification-scope-subject-v1:a210e434c3424bb8919fea0ca1156785f2c42625a38cd4a887b753ca97f913a2'
DOSSIER_SHA='2638615c3bdfdad98403c5ad63e57569d678c79e4baf7f7b125b978a1ee012f5'


def canonical(value):return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def pin(path,pointer=''):
    raw=(ROOT/path).read_bytes()
    return {'path':path,'pointer':pointer,'raw_sha256':hashlib.sha256(raw).hexdigest()}
def save(name,value):
    (OUT/name).write_text(json.dumps(value,sort_keys=True,indent=2)+'\n')
def ident(value):return value['namespace']+':'+value['sha256']


def main():
    path=str((RECOVERY/'scope-decision-dossier.json').relative_to(ROOT))
    raw=(ROOT/path).read_bytes();d=json.loads(raw)
    assert hashlib.sha256(raw).hexdigest()==DOSSIER_SHA
    assert SUBJECT==d['subject_identity']=='qualification-scope-subject-v1:'+hashlib.sha256(canonical(d['subject'])).hexdigest()
    rpath=PREFIX+'E2_P05_A05_DECISION_ANCESTRY_RECOVERY_1.json'
    recovery=json.loads((ROOT/rpath).read_bytes())
    assert recovery['SCOPE_DECISION_SUBJECT_ID']==SUBJECT and recovery['SCOPE_OPTIONS']==d['options']
    for source in d['subject']['governing_source_pins']:
        assert hashlib.sha256((ROOT/source['path']).read_bytes()).hexdigest()==source['raw_sha256'],source['path']
    selected=next(x for x in d['options'] if x['option']==OPTION)
    w=d['subject']['alternate_native_witness']
    scope={'schema':'E2-P05-A05-ALTERNATE-SCOPE-AUTHENTICATION-1',
        'selected_option':OPTION,'qualification_scope_subject':SUBJECT,
        'dossier':pin(path),'recovery_JSON':pin(rpath),
        'recovery_MD':pin(PREFIX+'E2_P05_A05_DECISION_ANCESTRY_RECOVERY_1.md'),
        'issuer':'authenticated human user of this session',
        'authentication':'Explicit user-role selection supplied through trusted conversation transport in the current authoritative request.',
        'provenance':'E2-P05 A05 ALTERNATE NATIVE-EVIDENCE MAPPING QUALIFICATION 1 / AUTHORITATIVE HUMAN DECISION',
        'date':'2026-10-05','date_precision':'DAY','sequence':1,
        'scope_type':'QUALIFICATION_ACCEPTANCE_ONLY',
        'permissions':['Qualify only the dossier-named retained P03 event for E2-A05.recorded_decision_event_ancestry',
                       'Create the explicit A05-only END/N12/N13 acceptance overlay if its required assurance passes'],
        'authorized_option_terms':selected,'exclusions':d['subject']['exclusions'],
        'exact_event_id':w['event_id'],'native_Action_authority':False,'DECIDE_authority':False,
        'USE_authority':False,'event_authority':False,'new_grant_issuance':False,'P05_execution_authority':False,
        'cryptographic_signature_claimed':False,'new_native_choice_evidence':False,
        'native_scope_issuer_or_grant_materialization':False}
    save('authorization-authentication.json',scope)
    scope_pin=pin(str((OUT/'authorization-authentication.json').relative_to(ROOT)))

    n12=[
        'Actual enclosing native ExecutionEvent with RecordedDecision, not selection/history alone',
        'Exact enrolled ledger event with parent/pre/post-Snapshot identity continuity',
        'Retained native post-state records the exact choice and native decision completion',
        'No new result/event/knowledge or occurrence is fabricated by this mapping']
    n13=[
        'Exact typed RecordedDecision result binds an existing accepted choice record, not an Action/output declaration',
        'Exact native choice knowledge, dossier, issuer/scope-root and provenance bindings are retained',
        'Independent DECIDE and USE proof queries pass at the retained qualified context',
        'Knowledge/root/slot/authority entities unchanged through this historical decision; grant already existed',
        'Original identities and cross-prefix claims are not synthesized or aliased']
    proposal={'witness_kind':'RETAINED_NATIVE_EXECUTION_EVENT','source_role':'P03',
        'event_source':{'path':PREFIX+'P03_PROSPECTIVE_CHECKPOINT_BUNDLE_1.json','pointer':'/bundle/events/1'},
        'event_id':w['event_id'],'event_type':'ExecutionEvent<RecordedDecision>',
        'record_entity_id':w['record']['value'],'recorded_decision_reference':w['event_id']+'#/result',
        'choice_identity':ident(w['choice_source']['identity']),
        'decision_subject':'E2-DECIDE','selected_decision_option':'ALLOW_QUALIFICATION_MAPPING',
        'parent_event_id':w['parent'],'pre_state_id':w['pre_state'],'post_state_id':w['post_state'],
        'ledger_bundle_id':w['checkpoint_bundle'],'ledger_position':w['position'],
        'ledger_zero_based_index':1,'ledger_root':w['root'],'ledger_head':w['event_id'],
        'ledger_id_representation':'NOT_EXPOSED_BY_NATIVE_PERSISTENCEBUNDLE',
        'context':copy.deepcopy(w['context']),'choice_source_pin':copy.deepcopy(w['choice_source']),
        'classification':'AUTHORIZED_ALTERNATE_NATIVE_EVIDENCE',
        'required_input':'E2-A05.recorded_decision_event_ancestry',
        'scope_subject':SUBJECT,'selected_scope_option':OPTION,
        'scope_type':'QUALIFICATION_ACCEPTANCE_ONLY','dossier_raw_sha256':DOSSIER_SHA,
        'N12_mode':'INDEPENDENT_EXPLICIT_MAPPING','N13_mode':'INDEPENDENT_EXPLICIT_MAPPING',
        'N12_required_terms':n12,'N13_required_terms':n13,
        'P03_EVENT_IS_ORIGINAL_A05_EVENT':'NO','ORIGINAL_A05_HISTORICAL_ANCESTRY':'UNPROVEN',
        'HISTORICAL_RECONSTRUCTION':'NO','NEW_A05_OCCURRENCE_CREATED':'NO',
        'NEW_HUMAN_CHOICE_CREATED':'NO','NEW_NATIVE_GRANT_ISSUED':'NO',
        'original_A05_event_id':None,'original_A05_parent_id':None,
        'new_A05_choice_id':None,'new_A05_event_id':None,
        'grant_preexisting':True,'grant_issuance_proven':False,
        'original_prefix_gap_closed':False,'A06_gap_closed':False,
        'full_END_original_ancestry_waived':False,'P05_executed':False,'P06_executed':False}
    contract={'schema':'E2-P05-A05-AUTHORIZED-ALTERNATE-MAPPING-CONTRACT-1',
        'subject_identity':SUBJECT,'selected_option':OPTION,'dossier_raw_sha256':DOSSIER_SHA,
        'dossier_pin':pin(path),'scope_authentication_pin':scope_pin,
        'governing_source_pins':d['subject']['governing_source_pins'],
        'selected_option_terms':selected,'dossier_subject':d['subject'],
        'expected_proposal':proposal,'expected_event':w['event'],'expected_context':w['context'],
        'authoritative_sources':{
            'checkpoint':pin(PREFIX+'P03_PROSPECTIVE_CHECKPOINT_BUNDLE_1.json','/bundle'),
            'canonical_descendant':pin(PREFIX+'E2_P04_CANONICAL_TARGET_BUNDLE_1.json','/bundle'),
            'immutable_event':pin('docs/plans/event-'+w['event_id'].split(':')[1]+'.json'),
            'P05_current_graph':pin('docs/plans/qualification/E2_P05_A04_PROSPECTIVE_ANCESTRY_EXECUTION_1/P05-binding-rerun.json'),
            'P05_readiness':pin(PREFIX+'E2_P05_READINESS.json'),
            'native_model':pin('adapter/planner/model.py'),'native_codec':pin('adapter/planner/codec.py'),
            'native_core':pin('adapter/planner/core.py'),'native_pure_gates':pin('adapter/planner/gates.py')},
        'independent_state_oracle':{
            'before_decision_stage':'DECISION_READY','after_decision_stage':'DECISION_RECORDED',
            'decision_field_changes':['history','record','recorded_choice','stage'],
            'before_action_status':'ACTIONABLE','after_action_status':'COMPLETED',
            'only_status_changed':'E2-DECIDE','all_other_snapshot_fields_unchanged':True,
            'DECIDE_proof':'PROVED','USE_proof':'PROVED','readiness':'DECISION_READY',
            'root_state':'UNRESOLVED','slot_state':'UNRESOLVED','grant_entity_unchanged':True},
        'N12_terms':n12,'N13_terms':n13,
        'semantic_correspondence_policy':{
            'exact_native':['event_type','payload_types_subject_option','native_enrollment_and_position','native_dossier_and_choice_relationships','native_post_decision_effects','no_root_slot_auto_satisfaction'],
            'authorized_equivalence':['original_missing_event_to_exact_named_P03_occurrence','different_exact_choice_record/dossier/issuer-envelope/context',
                'different_native_parent_pre_post_snapshots_and_qualification_ledger',
                'qualification_source_provenance_in_place_of_missing_original_ancestry'],
            'local_ordering':'Exact native parent -> RecordedDecision -> checkpoint; pre-P03 preparation is authored input, not claimed occurrence.',
            'global_original_prefix':'Still UNPROVEN/unresolved; not part of the local replacement acceptance and not waived.',
            'preexisting_grant':'Only existence/current native USE relationship is shown; no issuance occurrence asserted.'},
        'comparison_identity_domain':'qualification-a05-alternate-mapping-v1; not a native event/result/choice/authority identity',
        'fresh_readers':{'seeds':[0,1,7,101],'readers_per_seed':3,'modes':['native','reverse_unordered','rotate_unordered'],
            'ordered_events_history_and_policy_rules_permuted':False,'native_operation_or_replay_permitted':False},
        'sealed_before_qualification':True}
    save('mapping-contract.json',contract)
    negatives=[
        ('wrong_P03_event','event_id','planner-event-v1:'+'0'*64,'EVENT_ID_EXACT'),
        ('wrong_choice_identity','choice_identity','raw-file-sha256:'+'0'*64,'CHOICE_IDENTITY_EXACT'),
        ('wrong_decision_context','context/generation','FOREIGN-GENERATION','DECISION_CONTEXT_EXACT'),
        ('wrong_parent','parent_event_id',w['event_id'],'PARENT_EVENT_EXACT'),
        ('wrong_ledger','ledger_bundle_id',d['subject']['prospective_candidate_start_for_later_assessment']['bundle_id'],'LEDGER_MEMBERSHIP_EXACT'),
        ('wrong_ledger_position','ledger_position',1,'LEDGER_POSITION_EXACT'),
        ('wrong_scope','context/scope','PRODUCTION','DECISION_CONTEXT_EXACT'),
        ('wrong_lineage','context/lineage','E2-CANONICAL-BASELINE-1','DECISION_CONTEXT_EXACT'),
        ('wrong_provenance','choice_source_pin/identity/sha256','0'*64,'CHOICE_PROVENANCE_EXACT'),
        ('report_substituted_for_event','witness_kind','REPORT_METADATA','NATIVE_EVENT_REQUIRED'),
        ('Snapshot_substituted_for_ancestry','witness_kind','SNAPSHOT_ONLY','NATIVE_EVENT_REQUIRED'),
        ('different_P03_decision_event','event_source/pointer','/bundle/events/0','EVENT_SOURCE_EXACT'),
        ('alternate_labeled_original_A05','P03_EVENT_IS_ORIGINAL_A05_EVENT','YES','NO_HISTORICAL_ALIAS'),
        ('new_A05_identity_fabricated','new_A05_event_id','planner-event-v1:'+'f'*64,'NO_NEW_A05_IDENTITY'),
        ('preexisting_grant_limitation_removed','grant_preexisting',False,'PREEXISTING_GRANT_LIMITATION'),
        ('original_prefix_gap_closed','original_prefix_gap_closed',True,'ORIGINAL_PREFIX_STILL_OPEN'),
        ('A06_gap_closed','A06_gap_closed',True,'A06_STILL_OPEN'),
        ('N12_assumed','N12_mode','ASSUMED','N12_INDEPENDENT_MAPPING_REQUIRED'),
        ('N13_assumed_from_N12','N13_mode','FROM_N12','N13_INDEPENDENT_MAPPING_REQUIRED'),
        ('wrong_scope_subject','scope_subject','qualification-scope-subject-v1:'+'0'*64,'SCOPE_SUBJECT_EXACT'),
        ('wrong_dossier_hash','dossier_raw_sha256','0'*64,'DOSSIER_HASH_EXACT'),
        ('scope_used_as_DECIDE_authority','scope_type','DECIDE','QUALIFICATION_SCOPE_ONLY'),
        ('original_event_identity_aliased','original_A05_event_id',w['event_id'],'NO_HISTORICAL_ALIAS'),
        ('grant_issuance_claimed','grant_issuance_proven',True,'PREEXISTING_GRANT_LIMITATION'),
        ('N13_terms_omitted','N13_required_terms',[],'N13_INDEPENDENT_MAPPING_REQUIRED'),
        ('full_END_gap_waived','full_END_original_ancestry_waived',True,'ORIGINAL_PREFIX_STILL_OPEN')]
    save('negative-plan.json',{'schema':'E2-P05-A05-ALTERNATE-NEGATIVE-PLAN-1','sealed_before_qualification':True,
        'domain':'Read-only qualification mapping gates, not new native admission/execution',
        'controls':[{'id':i+1,'case':name,'mutation_path':path,'value':value,'expected_rejection':code}
                    for i,(name,path,value,code) in enumerate(negatives)]})
    save('seal.json',{'schema':'E2-P05-A05-ALTERNATE-MAPPING-SEAL-1','subject_identity':SUBJECT,
        'pins':[pin(str((OUT/f).relative_to(ROOT))) for f in ('authorization-authentication.json','mapping-contract.json','negative-plan.json')],
        'native_events_created':0,'native_choices_created':0,'native_grants_issued':0})
    print(json.dumps({'scope_authentication':'PASS','selected_option':OPTION,'subject':SUBJECT,
                      'negative_controls_sealed':len(negatives),'native_events_created':0}))


if __name__=='__main__':main()
