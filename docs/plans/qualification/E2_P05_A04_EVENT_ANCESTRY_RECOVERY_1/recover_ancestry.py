"""Recover contracts and inspect native fields only; all transition APIs barred."""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PLANS = ROOT/'docs/plans'
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from adapter.planner import codec as c, core, model as m

STEM = 'DETERMINISTIC_PLANNER_V0_1_'
REPORT = PLANS/(STEM+'E2_P05_A04_EVENT_ANCESTRY_RECOVERY_1.json')
FORBIDDEN_CALLS = []


def guard(module, name):
    if hasattr(module, name):
        def prohibited(*args, **kwargs):
            FORBIDDEN_CALLS.append(module.__name__+'.'+name)
            raise AssertionError('Recovery must not evaluate/admit/replay a lifecycle: '+name)
        setattr(module, name, prohibited)


for module, names in ((core, ('recompute', '_inventory', 'apply_result', 'apply_event',
    'admit_dossier_materialization', 'apply_recorded_decision', 'apply_receipt')),
    (c, ('_replay', 'apply_event', 'apply_result', 'recompute', 'append_event', 'record_result',
         'commit_event', 'save_bundle', 'restore', 'bundle_bytes', 'bundle_id', 'snapshot_bytes', 'snapshot_id')),
    (m, ('validate_model',))):
    for name in names:
        guard(module, name)


def read(path):
    return json.loads(Path(path).read_bytes())


def resolve(document, pointer):
    for part in pointer.split('/')[1:] if pointer else ():
        part = part.replace('~1', '/').replace('~0', '~')
        document = document[int(part)] if isinstance(document, list) else document[part]
    return document


def pin(path, pointer=''):
    path = Path(path).resolve()
    raw = path.read_bytes()
    if pointer:
        resolve(json.loads(raw), pointer)
    return {'path':str(path.relative_to(ROOT)), 'pointer':pointer,
            'raw_sha256':hashlib.sha256(raw).hexdigest()}


def source(name, pointer=''):
    return pin(PLANS/(STEM+name+'.json'), pointer)


def write(name, obj):
    (OUT/name).write_text(json.dumps(obj, sort_keys=True, indent=2)+'\n')


def uid(identity):
    return identity.namespace+':'+identity.sha256


def snapshot_inspection(path):
    raw = path.read_bytes()
    native = c._unwire(c.parse_json(raw)['snapshot'])
    assert type(native) is m.Snapshot
    encoded = c.canonical_bytes({'schema':'PLANNER-SNAPSHOT-1','snapshot':c._wire(native)})
    identity = c._identity(encoded, 'planner-snapshot-v1')
    assert raw == encoded
    action = next(a for a in native.actions if a.id.value == 'E2-PREPARE')
    statuses = {s.id.value:s.state.value for s in native.statuses}
    output = next((k for k in native.knowledge if k.id.value=='E2-K-PREPARE'), None)
    decision = next(d for d in native.decisions if d.action.value=='E2-DECIDE')
    return {'source':pin(path,'/snapshot'), 'SnapshotId':uid(identity),
            'scope_lineage_generation':c._wire(native.context), 'prepare_Action':c._wire(action),
            'statuses':statuses, 'prepare_KnowledgeRecord':c._wire(output),
            'decision_stage':decision.stage.value, 'decision_history':[s.value for s in decision.history],
            'dossier':c._wire(decision.dossier), 'validation_instances':c._wire(native.validation_instances),
            'snapshot_bytes_preserved':True, 'canonical_identity_check':'PASS',
            'occurrence_or_ancestry_from_snapshot':'NOT_PROVEN; snapshots contain no event parent/ledger'}, native


def bundle_inspection(path):
    raw = path.read_bytes()
    native = c._unwire(c.parse_json(raw)['bundle'])
    assert type(native) is m.PersistenceBundle
    assert raw == c._bundle_bytes_admitted(native)
    identity = c._identity(raw, 'planner-bundle-v1')
    initial_bytes = c.canonical_bytes({'schema':'PLANNER-SNAPSHOT-1','snapshot':c._wire(native.initial)})
    parent_state = c._identity(initial_bytes, 'planner-snapshot-v1')
    parent = None
    events = []
    for number, event in enumerate(native.events, 1):
        assert event.sequence == number
        assert event.parent_snapshot == parent_state
        assert event.parent_event == parent
        assert event.identity == c._event_identity(number, event.parent_snapshot, event.parent_event,
                                                   event.result, event.after_snapshot, event.resume_binding)
        events.append({'pointer':'/bundle/events/'+str(number-1),'position':number,
            'event_id':uid(event.identity),'event_type':type(event.result).__name__,
            'ActionId':event.result.action.value if type(event.result) is m.SuppliedResult else None,
            'parent_event_id':uid(event.parent_event) if event.parent_event else None,
            'pre_state_id':uid(event.parent_snapshot),'post_state_id':uid(event.after_snapshot),
            'native_identity_and_parent_fields':'PASS'})
        parent_state, parent = event.after_snapshot, event.identity
    current_bytes = c.canonical_bytes({'schema':'PLANNER-SNAPSHOT-1','snapshot':c._wire(native.current)})
    current_id = c._identity(current_bytes, 'planner-snapshot-v1')
    assert parent_state == current_id
    return {'source':pin(path,'/bundle/events'), 'BundleId':uid(identity),
        'current_StateId':uid(current_id), 'ledger_identity_domain':'PersistenceBundle content identity plus /bundle/events; no separate LedgerId field',
        'ledger_root':events[0]['event_id'] if events else None,'append_head':events[-1]['event_id'] if events else None,
        'event_count':len(events),'events':events,'scope_lineage_generation':c._wire(native.current.context),
        'PREPARE_events':[e for e in events if e['ActionId']=='E2-PREPARE'],
        'PREPARE_completed_in_initial':any(s.id.value=='E2-PREPARE' and s.state is m.ActionState.COMPLETED for s in native.initial.statuses),
        'native_decode_and_pure_identity_checks':'PASS', 'replay_or_execution_performed':False,
        'trust_and_cold_restore_claim':'Existing qualified owner evidence retained; this recovery only verifies bytes/types/identity/parent fields'}, native


def main():
    plan_path = PLANS/(STEM+'CANONICAL_QUALIFICATION_EXPERIMENT_1.json')
    plan = read(plan_path)
    case_ids = ('E2-A04','E2-N12','E2-N13','E2-END')
    cases = {x['CASE_ID']: {'declaration':x,'source':pin(plan_path,'/cases/'+str(i))}
             for i,x in enumerate(plan['cases']) if x['CASE_ID'] in case_ids}
    declaration = read(PLANS/(STEM+'E2_PC01_SOURCES.json'))['declarations'][2]
    assert declaration['id'] == 'E2-PREPARE'
    initial, _ = snapshot_inspection(PLANS/(STEM+'E2_P02_INITIAL_SNAPSHOT.json'))
    handoff, _ = snapshot_inspection(PLANS/(STEM+'E2_AUTHORITATIVE_HANDOFF_SNAPSHOT_1.json'))
    decision_post, _ = snapshot_inspection(PLANS/(STEM+'E2_HUMAN_DECISION_ALLOW_POST_SNAPSHOT_1.json'))
    p04, _ = bundle_inspection(PLANS/(STEM+'E2_P04_CANONICAL_TARGET_BUNDLE_1.json'))
    a03, _ = bundle_inspection(PLANS/(STEM+'E2_P05_A03_PROSPECTIVE_OCCURRENCE_BUNDLE_1.json'))
    a03_report = read(PLANS/(STEM+'E2_P05_A03_PROSPECTIVE_OCCURRENCE_RESULT_1.json'))
    assert a03_report['RESULT']=='PASS'
    assert a03_report['POST_A03_BUNDLE_ID']==a03['BundleId']
    assert a03_report['ORIGINAL_A03_HISTORICAL_OCCURRENCE']=='UNPROVEN'
    assert not p04['PREPARE_events'] and not a03['PREPARE_events']

    inventory = {'canonical_A04_case':cases['E2-A04'],
        'earliest_Action_declaration':{'source':source('E2_PC01_SOURCES','/declarations/2'),'value':declaration},
        'prospective_dossier':source('E2_PC01_SOURCES','/prospective_dossier'),
        'native_Action':initial['prepare_Action'], 'initial_native_identity':initial['SnapshotId'],
        'owning_package':'E2-P02; canonical cases A01-A06',
        'purpose':'Decision readiness and authority separation through bounded preparation of the E2-DECIDE dossier.',
        'native_operation':'DECISION_INPUT_ACQUISITION; admit_dossier_materialization(snapshot, SuppliedResult, validation_instances) for qualified actual dossier/validation admission; ordinary apply_result/record_result consume SuppliedResult.',
        'inputs':['Current completed E2-CHECK and E2-COLLECT; accepted E2-K-CHECK/E2-K-COLLECT',
                  'Exact E2-DECIDE DecisionDossier, two required fact predicates, six typed ValidationInstances',
                  'Current definition/source/provenance and E2-QUALIFICATION-ONLY/E2-CANONICAL-BASELINE-1/E2-GENERATION-1 context',
                  'Exact native pre-state and selected E2-PREPARE'],
        'authority':{'Action_authority_requirement':declaration['authority'],
            'separate_event_operating_authority_operand':'NONE on native SuppliedResult/ExecutionEvent; do not invent one.',
            'prospective_qualification_scope_authorization':'A03 grant covers A03 only; no A04 replacement scope authorized.'},
        'expected_result':{'native_result_type':'SuppliedResult','outcome':'PASS','ActionId':'E2-PREPARE',
            'KnowledgeId':'E2-K-PREPARE','dossier_identity':'planner-dossier-sha256:6a507317bc9cc323fbaa626e97b5954cf3ad934b0bd92d9dc96bd4f63e07bddb',
            'complete_dossier_checks':'Two fact predicates plus six admitted deterministic ValidationInstances; see retained dossier/typed instances.',
            'separate_dossier_output':'DecisionDossier, not authority/grant or domain proof'},
        'expected_postcondition':{'E2_PREPARE':'COMPLETED','E2_K_PREPARE':'ACCEPTED/CURRENT',
            'decision':'DECISION_READY with complete dossier/checks','control':'HUMAN_HANDOFF',
            'recorded_decision':'ABSENT','E2_GRANT':'ABSENT','positive_external_evidence':'ABSENT',
            'root_slot_proof_promotion':'NONE'},
        'event_type':'Native ExecutionEvent with exact actual PREPARE admission payload if retained. SuppliedResult is the ordinary result operand; no separate historical dossier-admission event type was recovered.',
        'operation_event_boundary':{'native_apply_result_path':'core.apply_event -> core.apply_result -> _inventory -> _decision_result',
            'native_ordinary_event_path':'codec.record_result -> apply_event -> ExecutionEvent -> append_event',
            'native_dossier_path':'core.admit_dossier_materialization -> typed dossier/validation state -> TransitionReport; this function creates no ExecutionEvent.',
            'historical_event_payload_available':False,
            'do_not_assume_SuppliedResult_alone_serializes_external_validation_instances':True,
            'new_durable_A04_event_contract_or_runtime_gap_assessment':'Outside this recovery; must be explicitly resolved before any prospective execution.'},
        'native_contract_sources':[pin(ROOT/'adapter/planner/model.py'),pin(ROOT/'adapter/planner/core.py'),pin(ROOT/'adapter/planner/codec.py'),pin(ROOT/'adapter/planner/gates.py')]}
    write('A04-contract.json',inventory)
    write('native-state-and-ledger-inspection.json',{'initial':initial,'handoff':handoff,'post_decision':decision_post,
        'canonical_P04':p04,'authorized_prospective_A03':a03,
        'eligibility_permission_or_Action_state_recomputed':False,'native_execution_replay_calls':FORBIDDEN_CALLS})

    # These are native contract fields, not a newly fabricated historical event.
    fields = [
        ('A04_EVENT_ID','REQUIRED','ExecutionEvent.identity: planner-event-v1 content identity; verify full retained event bytes.'),
        ('EVENT_TYPE','REQUIRED','ExecutionEvent carrying actual PREPARE result/admission; PASS enum or report label is not an event type.'),
        ('EVENT_PAYLOAD','REQUIRED','Retained actual typed admission operand, including actual result, exact knowledge and dossier bindings; no guessed materialization inputs.'),
        ('PARENT_EVENT_ID','REQUIRED','ExecutionEvent.parent_event; predecessor identity in the retained ledger, not report chronology or a new A03 identity.'),
        ('PARENT_STATE','REQUIRED_RELATION','Predecessor.after_snapshot equals ExecutionEvent.parent_snapshot; not a separate field.'),
        ('PRE_STATE_ID','REQUIRED','ExecutionEvent.parent_snapshot; exact state with applicable current PREPARE inputs.'),
        ('POST_STATE_ID','REQUIRED','ExecutionEvent.after_snapshot; coherently linked accepted dossier/decision-readiness state.'),
        ('LEDGER_ID','REQUIRED_DOMAIN_CORRECT','Exact event-bearing PersistenceBundle identity plus /bundle/events, or existing native GenesisLedger ID if actually applicable; ordinary bundles have no separate LedgerId.'),
        ('LEDGER_ROOT','REQUIRED_DERIVED_FROM_RETAINED_LEDGER','First native event identity; do not invent GENESIS or a root from report sequence.'),
        ('LEDGER_POSITION','REQUIRED','ExecutionEvent.sequence and exact /bundle/events index agree. Report sequence=3 is not native membership.'),
        ('APPEND_PREDECESSOR','REQUIRED','Previous retained event equals parent_event; canonical Action history connects the actual acquisition prefix.'),
        ('APPEND_SUCCESSOR','CONDITIONAL','If descendant history is supplied, next.parent_event=event.identity and next.parent_snapshot=event.after_snapshot. No successor required at a retained head.'),
        ('ROOT_HEAD_RELATIONSHIP','REQUIRED','Actual native ledger root-to-A04-to-retained-head continuity; preserve event order.'),
        ('RESULT_BINDING','REQUIRED','Event binds actual SuppliedResult/action/outcome/expected_snapshot or exact native admission operand; there is no standalone ActionResult record ID on SuppliedResult.'),
        ('OUTPUT_BINDING','REQUIRED','Exact E2-K-PREPARE KnowledgeRecord bytes and dossier binding; KnowledgeId/content/dossier/event identities remain separate domains.'),
        ('SCOPE','REQUIRED_CONTEXT_BINDING','E2-QUALIFICATION-ONLY from native Snapshot.context and payload/provenance, not a fabricated event field.'),
        ('LINEAGE','REQUIRED_CONTEXT_BINDING','Original E2-CANONICAL-BASELINE-1 or an independently acceptable authoritative boundary; no prospective-lineage splice.'),
        ('GENERATION','REQUIRED_CONTEXT_BINDING','E2-GENERATION-1 for original retained context; generation from canonical context/provenance.'),
        ('PROVENANCE','REQUIRED','Exact source/content/provenance of Action, actual output, dossier and admitted validations, coherently pinned by retained state/bundle.'),
        ('COMMAND_ID','NOT_A_NATIVE_MANDATORY_FIELD','SuppliedResult and ExecutionEvent have no command ID; inspect HEAD.command if retained, do not invent one.'),
        ('POST_HANDOFF_LINK','REQUIRED','Native occurrence/state trace connects actual PREPARE result to accepted dossier/handoff; equal control or name alone is insufficient.')]
    assurance = {'END':{'requirement':cases['E2-END'],
        'assurance':'Actual native preparation occurred on a coherent canonical path from acquisition into dossier readiness, before recorded decision; sources/oracles remain independent.'},
        'N12':{'requirement':cases['E2-N12'],
        'assurance':'PREPARE selection/readiness is not proof of actual execution/result/event admission; no ledger or knowledge fabrication.'},
        'N13':{'requirement':cases['E2-N13'],
        'assurance':'Prospective accepted_inventory/prepared_dossier declarations cannot substitute for an actual supplied result and admitted occurrence.'},
        'ancestry_beyond_occurrence':'An event identity/payload alone does not prove enrollment in the canonical ledger, its predecessor state, ordering or linkage to the accepted handoff.',
        'lost_assurance':['Exact original PREPARE admission payload and event identity','Native parent and append position/membership',
                          'Coherent event-to-accepted-handoff before/after link and original prefix-to-descendant ordering'],
        'preserved_assurance':['Authoritative P02 PASS and semantic dossier/readiness qualification',
                               'Typed accepted KnowledgeRecord/dossier/validation state in retained authoritative snapshots',
                               'Authorized prospective A03 assurance only; original A03 historical occurrence remains unproven'],
        'N12_N13_new_execution_or_suite_PASS_claim':False}
    ancestry_contract = {'input':'E2-A04.prepare_result_event_ancestry',
        'authoritative_basis':[cases['E2-A04']['source'],cases['E2-END']['source'],
            pin(PLANS/(STEM+'CANONICAL_QUALIFICATION_ACCEPTANCE_MATRIX_1.md')),
            pin(PLANS/'qualification/E2_P05_END_INPUT_BINDING_1/stop-and-readiness.json')],
        'binding_requirement':'Actual PREPARE result event linked to retained accepted dossier/handoff state; archive report/knowledge is not an ExecutionEvent.',
        'fields':[{'field':name,'requirement':requirement,'native_rule':rule} for name,requirement,rule in fields],
        'identity_formula':'codec._event_identity hashes canonical(sequence,parent_snapshot,parent_event,result,after_snapshot[,resume_binding]) in planner-event-v1.',
        'no_lossless_hash_without_all_identity_fields':True,
        'scope_rule':'Canonical history or already explicitly accepted replacement evidence only. T02 capability qualification alone and snapshot-only handoff cannot satisfy native ancestry.',
        'occurrence_and_ancestry_are_distinct':True,'assurance':assurance}
    write('ancestry-contract-and-assurance.json',ancestry_contract)

    candidates = [
        {'source':source('E2_P02_RETRY_3_RESULT','/trace/2'),'classification':'REPORT_METADATA',
         'fact':'PREPARE PASS, E2-K-PREPARE, dossier identity, reported sequence=3, pre=6c7efb..., post=391140...',
         'acceptable_native_ancestry':False,'missing':['native event payload','event ID','parent','ledger membership/position']},
        {'source':source('E2_T02_RESULT','/transitions/2'),'classification':'REPORT_METADATA',
         'evidence_origin':'NATIVE_QUALIFICATION',
         'fact':'T02 dossier materialization/ValidationInstances and encode/decode assertions; no serialized event.',
         'acceptable_native_ancestry':False,'supporting_limit':source('E2_T02_RESULT','/runtime_transaction')},
        {'source':source('E2_AUTHORITATIVE_HANDOFF_REPRODUCTION_1_TRACE','/trace/2'),'classification':'REPORT_METADATA',
         'fact':'Fresh authoritative reproduction reports pre=898570..., post=9b3d8e...; still no native parent/event/ledger.',
         'acceptable_native_ancestry':False,'original_event_identity':None},
        {'source':source('E2_AUTHORITATIVE_HANDOFF_SNAPSHOT_1','/snapshot'),'classification':'SNAPSHOT_ONLY',
         'fact':'Authoritative serialized handoff: prepared dossier, six typed validation instances, accepted E2-K-PREPARE and completed PREPARE.',
         'acceptable_native_ancestry':False,'SnapshotId':handoff['SnapshotId']},
        {'source':source('E2_HUMAN_DECISION_ALLOW_POST_SNAPSHOT_1','/snapshot/knowledge'),'classification':'SNAPSHOT_ONLY',
         'fact':'Retains accepted E2-K-PREPARE; KnowledgeRecord producer/source declaration is not occurrence ancestry.',
         'acceptable_native_ancestry':False,'SnapshotId':decision_post['SnapshotId']},
        {'source':source('E2_P04_CANONICAL_TARGET_BUNDLE_1','/bundle/events'),'classification':'CANONICAL_EXECUTION',
         'fact':'Twenty genuine P04-lineage events; PREPARE already completed in initial authored premises. No original PREPARE event.',
         'acceptable_native_ancestry':False,'BundleId':p04['BundleId'],'PREPARE_event_indices':[]},
        {'source':source('E2_P05_A03_PROSPECTIVE_OCCURRENCE_BUNDLE_1','/bundle/events'),'classification':'NATIVE_QUALIFICATION',
         'qualification_scope':'AUTHORIZED_PROSPECTIVE_REPLACEMENT; A03 only',
         'fact':'Two real prospective CHECK/COLLECT events; PREPARE selected afterward but unexecuted. A03 authorization does not extend to A04.',
         'acceptable_native_ancestry':False,'BundleId':a03['BundleId'],'PREPARE_event_indices':[]},
        {'source':pin(PLANS/'qualification/E2_P05_END_INPUT_BINDING_1/canonical-bindings.json','/stage_bindings/3'),
         'classification':'DERIVED','fact':'Prior binding records missing PREPARE ancestry; no new occurrence fact.',
         'acceptable_native_ancestry':False}]
    summary = read(OUT/'search-summary.json')
    corpus = read(OUT/'search-corpus.json')
    bundles = read(OUT/'persistence-bundles.json')
    results = read(OUT/'result-and-report-candidates.json')
    text = read(OUT/'text-search.json')
    assert summary['A04_event_occurrences']==0 and summary['original_state_event_occurrences']==0
    assert summary['parse_errors']==0 and results['A04_event_identity_body_count']==0
    losslessness = {'LOSSLESS_RECOVERY':'NO','ANCESTRY_CLASSIFICATION':'NO_NATIVE_ANCESTRY',
        'PRIMARY_CLASSIFICATION':'IRRECOVERABLE_HISTORICAL_ANCESTRY_IN_RETAINED_INPUTS',
        'native_occurrence_recovered':False,'native_ancestry_recovered':False,
        'historical_A04_occurrence':'UNPROVEN_BY_RETAINED_NATIVE_EVENT; authoritative P02 semantic PASS preserved',
        'required_missing_fields':['actual complete native admission/event payload','event ID','parent event ID',
            'event-bearing ledger identity/root','native ledger position and predecessor/successor links',
            'coherent exact before/after state-to-handoff linkage and result/output enrollment'],
        'partial_descriptive_evidence':'Result/output/dossier, scope/lineage, reported state identities and report ordinal exist; not partial native ancestry.',
        'historical_identity_limits':{'original_in_memory_post':'planner-snapshot-v1:39114028d38b9571c46e211248644b09a3ac63ad9f47cd21a75fc922a2d152e3',
            'old_reconstruction_post':'planner-snapshot-v1:996d1fa73a7c1a880b8cd7a6c27ec48c03386feba4c5a089711482f51aff5069',
            'authoritative_serialized_handoff':handoff['SnapshotId'],
            'original_PREPARE_report_pre':'planner-snapshot-v1:6c7efb221870974d76d12d7ceb372369ef68104bb1f522a16d47f7dc37236677',
            'authoritative_reproduction_report_pre':'planner-snapshot-v1:8985701af4db7bf08327dc5e455fcd9182ca71e7cfde7b2868c253b0e8bd2d5e',
            'equal_native_historical_path_proven':False,
            'identity_divergence_source':source('E2_HANDOFF_IDENTITY_DIVERGENCE_1','/event_differences')},
        'snapshot_limit':'Snapshot identity proves exact retained state; completed PREPARE/knowledge/dossier/validation state does not prove actual native event parent or ledger membership.',
        'supported_loss_point':'Prior identity-divergence analysis documents absent replayable post-T02 dossier-materialization event/payload. Fresh handoff reproduction emitted a snapshot/summary, not an event-bearing prefix.',
        'do_not_infer':'No new claim that PREPARE never executed, every external archive was searched, or a particular ledger was deleted/truncated.',
        'event_reconstruction_or_execution_performed':False}
    write('candidate-and-losslessness-analysis.json',{'candidates':candidates,'losslessness':losslessness,
        'native_candidate_count':0,'acceptable_native_candidate_count':0,
        'candidate_parent':None,'candidate_ledger_membership':None,'native_result_binding':None,
        'search_summary':summary,'bundle_search_summary':{k:v for k,v in bundles.items() if not isinstance(v,list)},
        'native_qualification_search':'No PREPARE native event/payload recovered; T02 and handoff reproduction retain metadata/snapshots only.',
        'text_file_count':text['file_count'],'text_matching_line_count':text['matching_line_count'],
        'embedded_native_JSON_strings_inspected':len(corpus['embedded_native_JSON_strings']),
        'non_event_empty_lock_files':len(corpus['non_event_records'])})

    previous_graph_path = PLANS/'qualification/E2_P05_A03_PROSPECTIVE_OCCURRENCE_EXECUTION_1/P05-binding-rerun.json'
    previous = read(previous_graph_path)
    bound = sum(s['binding_status']=='BOUND' for s in previous['stage_bindings'])
    assert bound==10 and previous['P05_NEXT_MISSING_INPUT']=='E2-A04.prepare_result_event_ancestry'
    old = read(PLANS/'qualification/E2_P05_END_INPUT_BINDING_1/canonical-bindings.json')
    verified = {}
    for stage in old['stage_bindings']:
        if stage['binding_status'] != 'BOUND':
            continue
        for p in stage['sources']+[stage['authoritative_result']]:
            actual = pin(ROOT/p['path'],p.get('pointer',''))
            assert actual['raw_sha256']==p['raw_sha256']
            verified[(p['path'],p.get('pointer',''))] = actual
    for p in a03_report['evidence'].values():
        if isinstance(p,dict) and 'path' in p and 'raw_sha256' in p:
            assert pin(ROOT/p['path'])['raw_sha256']==p['raw_sha256']
    frontier = {'P05_BOUND_STAGE_INPUTS':bound,'P05_TOTAL_STAGE_INPUTS':13,
        'source':pin(previous_graph_path),'current_bindings':previous['stage_bindings'],
        'existing_bound_input_pins_rechecked':list(verified.values()),'existing_A03_qualification_evidence_pins_rechecked':'PASS',
        'A04_new_binding_created':False,'A03_binding_changed':False,
        'E2_A04_PREPARE_RESULT_EVENT_ANCESTRY':'FAIL','P05_NEXT_MISSING_INPUT':'E2-A04.prepare_result_event_ancestry',
        'remaining_stage_gaps':previous['remaining_stage_gaps'],
        'full_END_ancestry_gate':previous['additional_unresolved_END_gate'],
        'P05_EXECUTION_READY':'NO','E2_P05_READY':'YES','P05_EXECUTED':'NO','P06_EXECUTED':'NO',
        'binding_representation':'Read-only evidence manifest; no new canonical graph object/admission.',
        'frontier_continuation':'STOP_AT_A04; no new A05/A06 recovery attempted'}
    write('P05-binding-frontier.json',frontier)

    initial_doc = read(PLANS/(STEM+'E2_P02_INITIAL_SNAPSHOT.json'))
    action_index = next(i for i,x in enumerate(initial_doc['snapshot']['actions']) if x['id']['value']=='E2-PREPARE')
    scope_subject = {'subject':'E2-A04.prepare_result_event_ancestry only',
        'canonical_case':cases['E2-A04'],'definition_source':source('E2_PC01_SOURCES','/declarations/2'),
        'native_Action_source':source('E2_P02_INITIAL_SNAPSHOT','/snapshot/actions/'+str(action_index)),
        'existing_owner_result':source('E2_P02_RETRY_4_RESULT'),
        'current_P05_binding':pin(previous_graph_path), 'canonical_P04_target':p04['source'],
        'assurance_requirements':ancestry_contract,'historical_state_facts':losslessness['historical_identity_limits'],
        'prospective_scope':{'operation':'Bounded new native PREPARE/dossier-readiness ancestry qualification for this one P05 stage input.',
            'required_before_execution':'Separate prospective contract sealing start/inputs/authority/oracles/native durable event path/parent/ledger/persistence/replay/negatives/N12/N13 and explicit END replacement mapping.',
            'success_effect':'May bind only A04 as AUTHORIZED_PROSPECTIVE_REPLACEMENT, with original occurrence/ancestry UNPROVEN and new lineage/event identities distinct.',
            'exclusions':['Historical reconstruction or alias','P05/P06 execution','A05/A06 replacement','Full original END ancestry waiver',
                'New operating/install authority','Runtime implementation or repair','Any live PREPARE execution in this recovery']}}
    subject_id = 'qualification-scope-subject-v1:'+hashlib.sha256(c.canonical_bytes(scope_subject)).hexdigest()
    options = [
        {'option':'RETAIN_P05_A04_NATIVE_ANCESTRY_REQUIREMENT','decision_ready':True,
         'effect':'Keep original requirement; P05 remains at 10/13 and blocked until legitimate native historical ancestry is supplied.',
         'qualification_executed':False},
        {'option':'AUTHORIZE_PROSPECTIVE_P05_A04_ANCESTRY_QUALIFICATION','decision_ready':True,
         'effect':'Authorize only a new prospective replacement qualification scope for A04 under the sealed subject. Prepare/seal its independent execution contract first; no historical reconstruction or permission to change runtime.',
         'future_execution_contract_already_complete':False,
         'original_A04_occurrence_and_ancestry':'UNPROVEN','N12_N13_mapping':'Must be explicitly sealed and qualified before any A04 binding closes.'},
        {'option':'AUTHORIZE_P05_A04_ALTERNATE_NATIVE_ANCESTRY_EVIDENCE','decision_ready':False,
         'candidate':None,'effect':'Could authorize a specifically identified retained alternate native ancestry only after its identities, parent, ledger/result/output and governing scope are reviewed.',
         'current_blocker':'No alternate native A04 ancestry candidate exists in retained inputs; report/snapshot alternatives are insufficient.'}]
    decision = {'SCOPE_DECISION_REQUIRED':'YES','selected_option':None,
        'subject_identity':subject_id,'subject':scope_subject,'options':options,
        'no_option_selected_or_authority_issued':True,
        'existing_A03_option':'AUTHORIZE_PROSPECTIVE_P05_A03_OCCURRENCE_QUALIFICATION; applies to A03 only.',
        'original_A04_ancestry_retained_requirement':'NOT_WAIVED',
        'prospective_A04_execution_ready':'NO; scope unselected and independent execution contract not sealed',
        'next_package':'E2-P05-A04-ANCESTRY-QUALIFICATION-SCOPE-DECISION'}
    write('scope-decision-dossier.json',decision)

    assert not FORBIDDEN_CALLS
    report = {'schema':'DETERMINISTIC-PLANNER-E2-P05-A04-EVENT-ANCESTRY-RECOVERY-1',
        'WORK_PACKAGE':'E2-P05-A04-EVENT-ANCESTRY-RECOVERY','RESULT':'BLOCKED',
        'A04_PURPOSE':inventory['purpose'],'A04_NATIVE_OPERATION':inventory['native_operation'],
        'ANCESTRY_CONTRACT':ancestry_contract,'ANCESTRY_ASSURANCE_PURPOSE':assurance,
        'A04_EVENT':None,'A04_PARENT':None,'LEDGER_MEMBERSHIP':None,
        'RESULT_BINDING':'Native accepted KnowledgeRecord/dossier state exists; binding to an actual original PREPARE event not recovered.',
        'LOSSLESS_RECOVERY':'NO','ANCESTRY_CLASSIFICATION':'NO_NATIVE_ANCESTRY',
        'E2_A04_PREPARE_RESULT_EVENT_ANCESTRY':'FAIL',
        'P05_BOUND_STAGE_INPUTS':10,'P05_NEXT_MISSING_INPUT':'E2-A04.prepare_result_event_ancestry',
        'SCOPE_DECISION_REQUIRED':'YES','SCOPE_OPTIONS':options,'SCOPE_SUBJECT_ID':subject_id,
        'P05_EXECUTION_READY':'NO','E2_P05_READY':'YES','P05_INITIAL_ORACLE':'PASS; prior authoritative evaluation preserved',
        'NEXT_PACKAGE':decision['next_package'], 'CANONICAL_EVENT_SEARCH':summary,
        'PERSISTENCE_SEARCH':{k:v for k,v in bundles.items() if not isinstance(v,list)},
        'QUALIFICATION_SEARCH':'T02 and fresh handoff reproduction metadata/snapshots; no native PREPARE event or event ancestry.',
        'CANDIDATE_WITNESSES':candidates,'LOSSLESSNESS_ANALYSIS':losslessness,
        'P01_P04':'PASS; prior authoritative results preserved','E2_P04_RESULT':'PASS',
        'ORIGINAL_A03_HISTORICAL_OCCURRENCE':'UNPROVEN','ORIGINAL_A04_HISTORICAL_ANCESTRY':'UNPROVEN',
        'P03_HISTORICAL_CORRESPONDENCE':'UNPROVEN','N_REAL_SATISFIED':'NO',
        'A04_REPRODUCED':'NO','P05_EXECUTED':'NO','P06_EXECUTED':'NO','NEW_AUTHORITY_ISSUED':'NO',
        'HISTORICAL_RECORDS_MODIFIED':'NO','NATIVE_EVENT_OR_RESULT_CONSTRUCTED':'NO',
        'NATIVE_EXECUTION_ADMISSION_REPLAY_CALLS':0,'RUNTIME_MODIFIED':'NO',
        'E1_ARTIFACTS_MODIFIED':0,'PRODUCTION_EFFECT':'NO',
        'GIT_DIFF_CHECK':'PENDING_FINAL_VERIFICATION',
        'evidence':{name:pin(OUT/name) for name in ('A04-contract.json','ancestry-contract-and-assurance.json',
            'native-state-and-ledger-inspection.json','search-corpus.json','search-summary.json','native-events.json',
            'persistence-bundles.json','result-and-report-candidates.json','text-search.json',
            'candidate-and-losslessness-analysis.json','P05-binding-frontier.json','scope-decision-dossier.json')},
        'preservation_baseline':pin(OUT/'baseline.json'),
        'recovery_programs':[pin(Path(__file__)),pin(OUT/'search_retained_history.py')]}
    REPORT.write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'RESULT':'BLOCKED','classification':'NO_NATIVE_ANCESTRY','A04_native_events':0,
        'P05_bound':10,'next':report['P05_NEXT_MISSING_INPUT'],'scope_subject':subject_id,
        'guarded_native_transition_calls':len(FORBIDDEN_CALLS)}))


if __name__ == '__main__':
    main()
