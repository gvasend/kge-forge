"""Seal definitions and algebraic oracles; never execute an A03 transition.

Only the empty starting bundle is passed to native replay validation. Expected
successors and events are comparison-only data, authored from the bounded
result contract. No positive result application, event append, commit, restore
of an occurred result, or qualification execution is available in this script.
"""
import copy
import hashlib
import json
from dataclasses import fields, replace
from pathlib import Path

from adapter.planner import codec as c, model as m
from adapter.planner.action_materializer import materialize_action
from adapter.planner.selector import POLICY_PIN, validate_policy

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
PLANS = ROOT / 'docs/plans'
PREFIX = 'DETERMINISTIC_PLANNER_V0_1_'
SELECTED = 'AUTHORIZE_PROSPECTIVE_P05_A03_OCCURRENCE_QUALIFICATION'
SCOPE = 'E2-QUALIFICATION-ONLY'
LINEAGE = 'E2-P05-A03-PROSPECTIVE-QUALIFICATION-1'
GENERATION = 'E2-P05-A03-PROSPECTIVE-GENERATION-1'
POLICY_VERSION = 'E1-SELECTION-1-P06'
REPLAY_SCOPE = 'PARTIAL_HISTORICAL_REPLAY'
LABELS = {
    'QUALIFICATION_TYPE': 'PROSPECTIVE_REPLACEMENT',
    'ORIGINAL_HISTORICAL_OCCURRENCE': 'UNPROVEN',
    'HISTORICAL_RECONSTRUCTION': 'NO',
    'PROSPECTIVE_EVENT_IS_ORIGINAL_EVENT': 'NO',
}


def canon(value):
    return c.canonical_bytes(value)


def raw_id(raw, namespace='raw-file-sha256'):
    return c._identity(raw, namespace)


def identity_text(value):
    return value.namespace + ':' + value.sha256


def relative(path):
    return str(path.relative_to(ROOT))


def file_pin(path, pointer=''):
    return {'path': relative(path), 'pointer': pointer,
            'raw_sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def save(path, value, *, canonical=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = canon(value) if canonical else (json.dumps(value, sort_keys=True, indent=2) + '\n').encode()
    if path.exists() and path.read_bytes() != raw:
        raise ValueError('sealed output conflict: ' + relative(path))
    path.write_bytes(raw)
    return file_pin(path)


def descendants(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from descendants(child)
    elif isinstance(value, list):
        for child in value:
            yield from descendants(child)


def source(name, body):
    packet = dict(body, **LABELS)
    packet.update(scope=SCOPE, lineage=LINEAGE, generation=GENERATION,
                  qualification_only=True, production_effect=False)
    path = OUT / 'inputs/sources' / name
    save(path, packet, canonical=True)
    raw = path.read_bytes()
    pin = m.ArtifactPin(relative(path), raw_id(raw))
    provenance = m.Provenance(pin.path, pin.identity, '/', raw.decode(),
                              'PROSPECTIVE_A03_AUTHORED_DEFINITION', SCOPE)
    return provenance, pin


def main():
    recovery_path = PLANS / (PREFIX + 'E2_P05_A03_OCCURRENCE_WITNESS_RECOVERY_1.json')
    recovery = json.loads(recovery_path.read_bytes())
    assert recovery['PRIMARY_CLASSIFICATION'] == 'IRRECOVERABLE_HISTORICAL_WITNESS'
    assert recovery['A03_NATIVE_RESULT_EVENT_TRACE'] == 'FAIL'
    dossier_path = ROOT / recovery['QUALIFICATION_SCOPE_DECISION']['path']
    assert hashlib.sha256(dossier_path.read_bytes()).hexdigest() == recovery['QUALIFICATION_SCOPE_DECISION']['raw_sha256']
    dossier = json.loads(dossier_path.read_bytes())
    subject_id = 'qualification-scope-subject-v1:' + hashlib.sha256(canon(dossier['subject'])).hexdigest()
    assert subject_id == dossier['subject_content_id']
    option = next(row for row in dossier['options'] if row['option'] == SELECTED)
    assert option['assurance_limit'].startswith('Original A03 occurrence/ancestry remains unproven')

    canonical_path = PLANS / (PREFIX + 'CANONICAL_QUALIFICATION_EXPERIMENT_1.json')
    cases = json.loads(canonical_path.read_bytes())['cases']
    cases_by_id = {row['CASE_ID']: row for row in cases}
    assert cases_by_id['E2-A03']['OPERATION'] == 'record_result/append_event with supplied bounded result'
    assert cases_by_id['E2-N12']['EXPECTED_STATE'] == 'No native result accepted; ledger/knowledge not fabricated'
    assert cases_by_id['E2-N13']['EXPECTED_STATE'] == 'Reject wrong event/result; knowledge/root/slot unchanged'

    template_path = PLANS / (PREFIX + 'E2_P02_INITIAL_SNAPSHOT.json')
    template = c.decode_snapshot(template_path.read_bytes())
    assert not template.knowledge and not template.entities
    assert all(row.state is m.ActionState.ACTION_ELIGIBLE for row in template.statuses)
    assert all(row.authority is None for row in template.actions if row.id.value in ('E2-CHECK', 'E2-COLLECT'))
    assert template.context.lineage != LINEAGE
    declaration_path = PLANS / (PREFIX + 'E2_PC01_SOURCES.json')
    authored = json.loads(declaration_path.read_bytes())
    declarations = {row['id']: row for row in authored['declarations']}
    assert set(declarations) == {row.id.value for row in template.actions}

    # Rebind only definition provenance/context, never prior completion facts.
    # Every copied historical source is explicitly a non-operative template.
    old_wire = c._wire(template)
    original_provenances = sorted({canon(row) for row in descendants(old_wire)
                                   if row.get('$type') == 'Provenance'})
    provenance_map, identity_map, source_pins, source_rows = {}, {}, [], []
    for index, encoded in enumerate(original_provenances):
        old = json.loads(encoded)
        action_ids = sorted(a.id.value for a in template.actions if canon(c._wire(a.source)) == encoded)
        rows = [copy.deepcopy(declarations[action_id]) for action_id in action_ids]
        for row in rows:
            row.update(scope=SCOPE, lineage=LINEAGE, generation=GENERATION)
        body = {
            'schema': 'E2-P05-A03-PROSPECTIVE-DEFINITION-SOURCE-1',
            'role': 'Authored initial definition; no result or occurrence asserted',
            'governing_PC01': file_pin(declaration_path),
            'template_snapshot': file_pin(template_path),
            'nonoperative_template_provenance': old,
            'action_declarations': rows,
            'scope_decision': SELECTED,
            'historical_occurrence_asserted': False,
        }
        provenance, pin = source('definition-%02d.json' % index, body)
        provenance_map[encoded] = c._wire(provenance)
        identity_map[canon(old['identity'])] = c._wire(pin.identity)
        source_pins.append(pin)
        source_rows.append({'input_id': 'DEFINITION-SOURCE-%02d' % index,
                            'type': 'Authored qualification source / ArtifactPin',
                            'content_identity': identity_text(pin.identity),
                            'source': file_pin(ROOT / pin.path),
                            'provenance': c._wire(provenance), 'Actions': action_ids,
                            'scope': SCOPE, 'lineage': LINEAGE, 'generation': GENERATION,
                            'currentness': 'Exact raw pin and native source binding; tick 0',
                            'historical_source_authority_carried_over': False})

    def rebind(value):
        if isinstance(value, list):
            return [rebind(child) for child in value]
        if isinstance(value, dict):
            if value.get('$type') == 'Provenance':
                return provenance_map[canon(value)]
            if value.get('$type') == 'ArtifactIdentity' and canon(value) in identity_map:
                return identity_map[canon(value)]
            return {key: LINEAGE if key == 'lineage' else GENERATION if key == 'generation'
                    else rebind(child) for key, child in value.items()}
        return value

    start = c._unwire(rebind(old_wire))
    # This preserves PC01's exact output statement, producer and PASS contract.
    # It creates prospective accepted inventories, never actual knowledge.
    updated_actions = []
    for action in start.actions:
        if action.id.value in ('E2-CHECK', 'E2-COLLECT'):
            action = materialize_action(action, declarations[action.id.value])
        updated_actions.append(action)
    start = replace(start, actions=tuple(updated_actions))
    m.validate_model(start)
    validate_policy(POLICY_PIN, POLICY_VERSION)
    bundle = m.PersistenceBundle(start, (), start, tuple(source_pins), POLICY_PIN,
                                 POLICY_VERSION, REPLAY_SCOPE)
    # Native validation/replay of an empty declared start has no event to apply.
    start_raw = c.bundle_bytes(bundle)
    c._verify_sources(bundle, ROOT)
    start_id = c.snapshot_id(start)
    start_bundle_id = raw_id(start_raw, 'planner-bundle-v1')
    start_path = OUT / 'inputs/starting-bundle.json'
    start_path.write_bytes(start_raw)
    save(OUT / 'inputs/starting-snapshot.json', {'schema': 'PLANNER-SNAPSHOT-1', 'snapshot': c._wire(start)}, canonical=True)
    assert not bundle.events and bundle.current == bundle.initial

    prospective_declarations = []
    for action_id in ('E2-CHECK', 'E2-COLLECT'):
        row = copy.deepcopy(declarations[action_id])
        row.update(scope=SCOPE, lineage=LINEAGE, generation=GENERATION)
        assert row['authority'] == [] and row['effect'] == 'NON_EFFECTING'
        prospective_declarations.append(row)
    producer_path = OUT / 'inputs/bounded-result-producer.json'
    save(producer_path, {
        'schema': 'E2-P05-A03-BOUNDED-SUPPLIED-RESULT-PRODUCER-1', **LABELS,
        'scope': SCOPE, 'lineage': LINEAGE, 'generation': GENERATION,
        'native_operation': 'Record a newly supplied bounded synthetic result; no external-world executor receipt claimed',
        'declarations': prospective_declarations,
        'producer': 'QUALIFICATION_DETERMINISTIC',
        'construct_at_execution': 'Create a fresh typed KnowledgeRecord from this authored declaration and the selected Action source; wrap in SuppliedResult with current expected_snapshot. Never read oracle files or copy a saved result instance.',
        'invocation_order': ['E2-CHECK', 'E2-COLLECT'],
        'no_execution_asserted': True,
    }, canonical=True)

    # Independent postconditions: exact bounded knowledge and statuses change;
    # all other native fields retain their authored values. Do not apply_event,
    # _inventory, recompute, record_result, append_event or replay these oracles.
    expected_states = [start]
    event_specs, expected_events, expected_payloads, result_specs = [], [], [], []
    previous_event = None
    for index, action_id in enumerate(('E2-CHECK', 'E2-COLLECT'), start=1):
        before = expected_states[-1]
        action = next(row for row in start.actions if row.id.value == action_id)
        assert action.operation.value == declarations[action_id]['operation']
        record = action.accepted_inventory[0]
        assert record.statement == declarations[action_id]['output']['statement']
        after = replace(before,
            statuses=tuple(sorted((replace(row, state=m.ActionState.COMPLETED)
                                   if row.id == action.id else row for row in before.statuses), key=lambda row: row.id.value)),
            knowledge=tuple(sorted(before.knowledge + (record,), key=lambda row: row.id.value)))
        m.validate_model(after)
        before_id, after_id = c.snapshot_id(before), c.snapshot_id(after)
        supplied = m.SuppliedResult(action.id, m.ActionResult.PASS, (record,), before_id)
        event_id = c._event_identity(index, before_id, previous_event, supplied, after_id)
        # These objects are descriptors under comparison-only oracle files, not
        # admitted event files, execution outputs, or input ledger members.
        expected_event = m.ExecutionEvent(index, before_id, previous_event, supplied, after_id, event_id)
        expected_events.append(expected_event)
        expected_payloads.append(supplied)
        expected_states.append(after)
        unchanged = {field.name: getattr(after, field.name) == getattr(before, field.name)
                     for field in fields(m.Snapshot) if field.name not in ('statuses', 'knowledge')}
        assert all(unchanged.values()) and all(root.state is m.ConditionState.UNRESOLVED for root in after.roots)
        expected_bundle = replace(bundle, events=tuple(expected_events), current=after)
        expected_bundle_id = raw_id(c._bundle_bytes_admitted(expected_bundle), 'planner-bundle-v1')
        event_specs.append({
            'role': 'EXPECTED_ORACLE_ONLY_NOT_OCCURRED', **LABELS,
            'EVENT_TYPE': 'ExecutionEvent carrying SuppliedResult',
            'sequence': index, 'ActionId': action_id,
            'PARENT_EVENT_ID': identity_text(previous_event) if previous_event else None,
            'PRE_STATE_ID': identity_text(before_id), 'POST_STATE_ID': identity_text(after_id),
            'EXPECTED_EVENT_ID': identity_text(event_id),
            'EXPECTED_POST_BUNDLE_ID': identity_text(expected_bundle_id),
            'EXPECTED_LEDGER_ROOT': identity_text(expected_events[0].identity),
            'EXPECTED_APPEND_HEAD': identity_text(event_id),
            'EVENT_PAYLOAD': c._wire(supplied), 'expected_native_wire': c._wire(expected_event),
            'scope': SCOPE, 'lineage': LINEAGE, 'generation': GENERATION,
            'provenance': c._wire(record.provenance),
            'identity_body': ['sequence', 'parent', 'parent_event', 'result', 'after'],
            'resume_binding': 'Omitted/None; ordinary acquisition result, not C03',
            'canonical_hash': 'codec._event_identity; CONTENT_IDENTITY / planner-event-v1',
            'ledger_membership': 'Append exactly this event to this experiment ledger, after matching current native bundle/state/head',
        })
        result_specs.append({
            'role': 'EXPECTED_RESULT_ONLY_NOT_CREATED', **LABELS,
            'ActionId': action_id, 'result_type': 'SuppliedResult.result: ActionResult enum',
            'outcome': 'PASS', 'knowledge': c._wire((record,)),
            'semantic_output': declarations[action_id]['output'],
            'POST_STATE_ID': identity_text(after_id), 'post_state': c._wire(after),
            'native_fields_unchanged': unchanged,
            'control': 'RUNNABLE',
            'actionable': ['E2-COLLECT'] if index == 1 else ['E2-PREPARE'],
            'selected': 'E2-COLLECT' if index == 1 else 'E2-PREPARE',
            'reentry_eligible': False, 'root': 'UNRESOLVED', 'slot_inventory': [],
            'other_Action_completion': 'UNCHANGED; PREPARE/DECIDE/REENTER/FINISH unexecuted',
        })
        previous_event = event_id

    oracle_events_pin = save(OUT / 'oracles/expected-events.json', {
        'schema': 'E2-P05-A03-EXPECTED-EVENT-ORACLES-1', **LABELS,
        'comparison_only': True, 'not_execution_input': True,
        'occurred_event_count': 0, 'event_oracles': event_specs,
        'identity_derivation': 'Pure native canonical encoding of independently authored postconditions; never observed runtime result or historical event reconstruction',
    })
    result_pin = save(OUT / 'oracles/expected-results.json', {
        'schema': 'E2-P05-A03-EXPECTED-RESULT-ORACLES-1', **LABELS,
        'comparison_only': True, 'not_execution_input': True,
        'result_oracles': result_specs,
        'postcondition_derivation': 'Source PC01 outputs plus native bounded-result effect on statuses/knowledge; no result execution or positive replay called',
    })

    original_assurance = {
        'semantic_result': 'Only the PC01-declared bounded PASS outputs are accepted',
        'state_transition': 'Then-selected CHECK/COLLECT transition to completed with exact accepted knowledge; root/slot cannot be inferred from PASS',
        'native_occurrence': 'Actual typed SuppliedResult admission is recorded as ExecutionEvent, beyond definitions or selection',
        'parent_ancestry': 'Exact historical pre-state/parent/post-state continuity',
        'ledger_membership': 'Actual native ordered ledger with identified event positions',
        'ordering': 'Selection precedes supplied result; CHECK then COLLECT precede PREPARE in the acquisition prefix',
        'result_output_provenance': 'Exact producer/source/outcome/native KnowledgeRecords linked to the admitted event',
        'END_dependency': 'A03 stage coverage and lifecycle ancestry consumed by experiment acceptance case END',
        'N12': cases_by_id['E2-N12'], 'N13': cases_by_id['E2-N13'],
        'lost_historical_assurance': ['Actual submitted payload', 'Actual parent and native event identity',
                                     'Native ledger membership/position', 'Original adjacent-event continuity and admission provenance'],
        'retained_but_insufficient': 'PASS reports, before/after state hashes and archived knowledge/statuses; they do not prove occurrence',
    }
    assurance_pin = save(OUT / 'assurance-mapping.json', {
        'schema': 'E2-P05-A03-PROSPECTIVE-ASSURANCE-MAPPING-1', **LABELS,
        'original': original_assurance,
        'prospective': {
            'preserved_at_new_scope': ['Bounded semantic result', 'Exact native state transition', 'Actual event admission',
                'Complete new parent/state ancestry', 'New ledger membership and CHECK/COLLECT ordering',
                'Producer/source/result linkage', 'Selection/result and definition/actual-result separation'],
            'not_preserved': ['Original historical occurrence identity', 'Original historical parent/ledger position',
                'Original A02-to-A03-to-A04 history continuity', 'Whole END historical correspondence'],
            'independent_assurance_limit': 'Native admission of supplied synthetic results, not proof of external-world I/O or executor invocation',
        },
        'N12_mapping': {
            'source': file_pin(canonical_path, '/cases/' + str(cases.index(cases_by_id['E2-N12']))),
            'original_assurance': cases_by_id['E2-N12']['EXPECTED_STATE'],
            'prospective_assurance': 'Fresh selection/recompute without a supplied result leaves exact start bytes and empty ledger/knowledge; selection trace cannot serve as A03 occurrence or completion',
            'assurance_preserved': 'Selection remains read-only; only ordinary supplied-result admission creates event/knowledge',
            'assurance_not_preserved': 'Occurrence in original historical lineage remains unproven; no original N12 execution result is inferred',
            'mapping_preserved': 'YES', 'negative_execution': 'NOT_EXECUTED',
            'acceptance': 'Use original N12 expected-state predicate unchanged in isolated prospective fixtures; keep P05-wide case verdict separate',
        },
        'N13_mapping': {
            'source': file_pin(canonical_path, '/cases/' + str(cases.index(cases_by_id['E2-N13']))),
            'original_assurance': cases_by_id['E2-N13']['EXPECTED_STATE'],
            'prospective_assurance': 'Admitted definition and output declaration create no actual knowledge/event. Declaration alone or wrong event/result is rejected with state/root/slot unchanged',
            'assurance_preserved': 'Typed result/inventory admission still checks exact bounded outcome and records actual occurrence; expected files and accepted inventory alone are never actual execution evidence',
            'assurance_not_preserved': 'Original historical N13/A03 occurrence remains unproven',
            'mapping_preserved': 'YES', 'negative_execution': 'NOT_EXECUTED',
            'native_limit': 'Matching immutable output values are permitted after a typed actual supplied-result admission. Native value equality does not attest independent external execution; this contract makes no such claim.',
            'acceptance': 'Use original N13 expected-state predicate unchanged; reject declaration/selection/oracle as occurrence evidence, and separately reject prospective-to-historical relabeling',
        },
    })

    capture = {
        'schema': 'E2-P05-A03-PROSPECTIVE-SCOPE-DECISION-CAPTURE-1', **LABELS,
        'selected_option': SELECTED,
        'issuer': 'Authenticated human user of this session',
        'authentication': 'Explicit user-role decision through trusted conversation transport; no signature or external issuer identity fabricated',
        'original_decision_subject': subject_id,
        'original_decision_dossier': file_pin(dossier_path),
        'recovery_report': file_pin(recovery_path),
        'bounded_permission': 'Define and seal a new A03 occurrence experiment; later separately requested execution may qualify only the authorized prospective A03 replacement term',
        'prospective_start_bundle_id': identity_text(start_bundle_id),
        'prospective_start_state_id': identity_text(start_id),
        'scope': SCOPE, 'lineage': LINEAGE, 'generation': GENERATION,
        'Actions': ['E2-CHECK', 'E2-COLLECT'],
        'result_producer': file_pin(producer_path),
        'definition_source_ids': [identity_text(pin.identity) for pin in source_pins],
        'scope_authentication_result': 'PASS',
        'source_and_fixture_applicability': 'PASS for fresh NON_EFFECTING authored initial fixture preserving PC01 A03 semantics',
        'native_operating_authority_required': False,
        'native_authorities_issued': 0,
        'historical_or_P03_authorities_reused': False,
        'GENESIS_required': False,
        'GENESIS_reason': 'Fresh independently declared all-unexecuted ordinary PersistenceBundle, not adoption of a completed historical checkpoint. Existing ordinary sequence-1/null-parent semantics apply. No begin_event_lineage/GENESIS transaction is used.',
        'INSTALL_required': False,
        'INSTALL_reason': 'No existing canonical P04 lineage or definition is changed; initial fixture construction only',
        'exclusions': ['Historical reconstruction or identity replacement', 'Original ancestry bridge', 'P05/P06 execution',
                       'P03 scope changes', 'Other unbound stages', 'Production effect', 'Native grants or installations',
                       'PREPARE/DECIDE/REENTER/FINISH execution', 'N-REAL or aggregate release qualification'],
    }
    authorization_pin = save(OUT / 'authorization-capture.json', capture)

    end_mapping = {
        'schema': 'E2-P05-A03-AUTHORIZED-PROSPECTIVE-END-MAPPING-1', **LABELS,
        'END_type': 'EXPERIMENT_ACCEPTANCE_CASE; not native Action/root/input-slot entity',
        'logical_required_slot': 'E2-A03.native_result_event_trace',
        'original_requirement': 'Historical A03 native result occurrence and full original ancestry',
        'original_evidence': {'status': 'UNPROVEN', 'native_event_ids': None, 'never_overwrite': True,
                              'recovery': file_pin(recovery_path)},
        'replacement_term': 'E2-A03.authorized_prospective_native_result_event_trace',
        'authorization': authorization_pin,
        'replacement_expected_native_event_ids': [row['EXPECTED_EVENT_ID'] for row in event_specs],
        'replacement_expected_ledger': {'start_bundle_id': identity_text(start_bundle_id), 'scope': SCOPE,
                                        'lineage': LINEAGE, 'generation': GENERATION},
        'acceptance': 'Only after genuine future native execution, cold restore, replay, deterministic reproduction and sealed negatives pass, bind this separate authorized replacement evidence to the A03 stage-coverage requirement',
        'binding_representation': 'Read-only acceptance evidence manifest; no native object or canonical persisted binding',
        'historical_identity_mapping': 'NONE; no event identity alias, substitution or lineage splice is permitted',
        'edges': [
            {'source': 'Original A03 historical requirement', 'target': 'E2-END.A03 historical correspondence', 'status': 'UNPROVEN'},
            {'source': SELECTED, 'target': 'E2-END.A03 adopted qualification mapping', 'type': 'EXPLICIT_SCOPE_ACCEPTANCE'},
            {'source': 'New prospective native CHECK/COLLECT event ledger', 'target': 'E2-END.A03 authorized replacement coverage', 'status': 'PENDING_FUTURE_EXECUTION'},
        ],
        'ordering': 'New selection/check/collect chronology only; no invented original A02/A04 parent connection',
        'A04_future_frontier': 'E2-A04.prepare_result_event_ancestry; no PREPARE execution in this experiment',
        'success_effect': 'A03 stage binding only may become BOUND / AUTHORIZED_REPLACEMENT_QUALIFICATION; bound-stage count becomes 10/13 if all prior bindings remain valid',
        'remaining_stage_gaps': ['E2-A04.prepare_result_event_ancestry', 'E2-A05.recorded_decision_event_ancestry', 'E2-A06.request_wait_event_trace'],
        'additional_unresolved_END_gate': 'Original prefix-to-checkpoint-to-target ancestry or separately governing full END acceptance mapping remains unresolved',
        'P05_EXECUTION_READY_after_A03_alone': 'NO',
        'N12_mapping_preserved': 'YES', 'N13_mapping_preserved': 'YES',
        'current_binding_status': 'NOT_BOUND; prospective A03 not executed; prior 9/13 graph retained unchanged',
    }
    end_pin = save(OUT / 'END-acceptance-mapping.json', end_mapping)

    start_spec = {
        'form': 'Fresh prospectively authored all-unexecuted ordinary PersistenceBundle; native empty ledger',
        'source_template': file_pin(template_path),
        'START_BUNDLE_ID': identity_text(start_bundle_id), 'START_STATE_ID': identity_text(start_id),
        'start_bundle': file_pin(start_path),
        'LEDGER_ID': identity_text(start_bundle_id) + '#/bundle/events',
        'LEDGER_ID_domain': 'Exact sealed native bundle/events coordinate; ordinary PersistenceBundle has no standalone LedgerId field. Not a GENESIS ledger identity.',
        'LEDGER_ROOT': None, 'APPEND_HEAD': None, 'PARENT_EVENT_ID': None,
        'null_meaning': 'Explicit empty authored ledger, not missing/TBD ancestry. First admitted event establishes root/head; no historical parent inferred.',
        'event_count': 0, 'scope': SCOPE, 'lineage': LINEAGE, 'generation': GENERATION,
        'PROSPECTIVE_LINEAGE_DIFFERS_FROM_ORIGINAL': True,
        'original_lineage': template.context.lineage,
        'PREEXPERIMENT_OCCURRENCES_ASSERTED': 0,
        'context': c._wire(start.context), 'policy': c._wire(POLICY_PIN),
        'policy_version': POLICY_VERSION,
        'native_bundle_scope': REPLAY_SCOPE,
        'native_bundle_scope_meaning': 'Existing codec policy/serialization scope, not a claim of historical reconstruction; qualification meaning is explicitly prospective',
        'entry_oracle': {'actions': sorted(declarations), 'actual_knowledge': [],
                         'native_events': [], 'completed_Actions': [], 'authority_entities': [],
                         'actionable': ['E2-CHECK', 'E2-COLLECT'], 'selected': 'E2-CHECK',
                         'control': 'RUNNABLE', 'root': 'UNRESOLVED', 'slots': [],
                         'receipt_instances': [], 'reentry_eligible': False},
        'selection_oracle': 'CHECK/COLLECT have equal (0,0,0) coverage and no information metric. Admitted policy class priority ranks DETERMINISTIC_VALIDATION ahead of SOURCE_ACQUISITION; after CHECK only COLLECT is eligible, then PREPARE becomes ready but remains unexecuted.',
        'native_empty_bundle_validation': 'PASS', 'physical_source_pin_checks': 'PASS',
        'operating_authority_reference_CHECK': None, 'operating_authority_reference_COLLECT': None,
    }
    start_pin = save(OUT / 'prospective-start.json', dict(start_spec, **LABELS))

    input_inventory = {
        'schema': 'E2-P05-A03-PROSPECTIVE-INPUT-INVENTORY-1', **LABELS,
        'scope': SCOPE, 'lineage': LINEAGE, 'generation': GENERATION,
        'native_start': start_spec,
        'definition_sources': source_rows,
        'bounded_result_producer': {'INPUT_ID': 'A03-BOUNDED-SUPPLIED-RESULT-PRODUCER',
            'TYPE': 'Authored declaration provider; not actual result instance', 'source': file_pin(producer_path),
            'content_identity': identity_text(raw_id(producer_path.read_bytes())),
            'provenance': file_pin(declaration_path), 'scope': SCOPE, 'lineage': LINEAGE,
            'generation': GENERATION, 'currentness': 'Exact presealed raw bytes; no generation/field substitution'},
        'policy': {'INPUT_ID': 'E1-SELECTION-1', 'TYPE': 'Native supported PolicyBinding',
                   'pin': c._wire(POLICY_PIN), 'source': file_pin(ROOT / POLICY_PIN.path),
                   'version': POLICY_VERSION, 'currentness': 'Supported registry and exact physical policy pin',
                   'scope': 'Selection policy input only; frozen E1 execution is prohibited',
                   'lineage': 'Policy is shared; new state lineage remains prospective', 'generation': 'E1-SELECTOR-RULES-1'},
        'scope_decision': authorization_pin,
        'runtime_and_native_contracts': {relative(path): hashlib.sha256(path.read_bytes()).hexdigest()
                                         for path in sorted((ROOT / 'adapter/planner').glob('*.py'))},
        'execution_operand_allowlist': ['inputs/starting-bundle.json', 'inputs/bounded-result-producer.json',
                                        'inputs/sources/*.json', POLICY_PIN.path],
        'execution_guard_inputs': ['authorization-capture.json', 'prospective-start.json', 'input-inventory.json', 'seal.json'],
        'excluded_from_Planner_and_result_provider_inputs': ['oracles/*', 'END-acceptance-mapping.json',
            'assurance-mapping.json', 'negative-contract.json', 'any prior execution result or completed historical snapshot'],
        'actual_lifecycle_inputs_at_seal': {'SuppliedResult_admitted': 0, 'native_events': 0, 'knowledge': 0},
    }
    input_pin = save(OUT / 'input-inventory.json', input_inventory)

    negative_rows = [
        ('wrong_A03_input', 'Native result admission / sealed input guard', 'Substitute CHECK/COLLECT action/source declaration', 'REJECT; current selection/result-source contract exact'),
        ('wrong_result', 'Native gates.validate_result', 'Use FAIL instead of declared PASS', 'REJECT; result differs from bounded outcome contract'),
        ('wrong_output', 'Native gates.validate_result', 'Wrong/missing/extra knowledge output or producer', 'REJECT; exact inventory and unique KnowledgeIds required'),
        ('wrong_parent', 'Native ledger replay / sealed event oracle', 'Use foreign/non-null first parent or wrong second parent', 'REJECT; expected native parent continuity'),
        ('wrong_pre_state', 'Native core.apply_result', 'Supply a stale/foreign expected_snapshot', 'REJECT; supplied result pre-state mismatch'),
        ('wrong_event_payload', 'Native event identity/replay / sealed oracle', 'Change typed supplied result while retaining trusted event/bundle identity', 'REJECT; event identity or admitted transition mismatch'),
        ('wrong_ledger', 'Native bundle trust / sealed ledger coordinate', 'Move event into another bundle/initial/source set', 'REJECT; start bundle/events lineage coordinate differs'),
        ('wrong_append_position', 'Native event replay / sealed event oracle', 'Skip/reverse/duplicate sequence position', 'REJECT; exact two-event chronology and sequence'),
        ('wrong_authority', 'Authenticated scope/fixture boundary', 'Use prior P03/GENESIS/INSTALL/USE grant instead of selected scope decision, or add an operating authority to CHECK/COLLECT', 'REJECT; no native operating authority is required or authorized for this fixture'),
        ('wrong_scope', 'Sealed start/context guard and native provenance', 'Change E2-QUALIFICATION-ONLY', 'REJECT; exact source/state/capture scope'),
        ('wrong_lineage', 'Sealed start/context guard and native bundle identity', 'Use original or foreign lineage', 'REJECT; prospective lineage identity exact'),
        ('wrong_generation', 'Sealed start/source guard', 'Use prior or foreign generation', 'REJECT; exact prospective generation'),
        ('wrong_provenance', 'Native result inventory / physical pins', 'Change KnowledgeRecord.provenance or source bytes', 'REJECT; exact result/source binding or raw pin mismatch'),
        ('foreign_event', 'Native ledger identity/parent replay / mapping guard', 'Supply a same-named event from a different lineage', 'REJECT; correct name does not establish identity/membership'),
        ('event_without_actual_A03_admission', 'Occurrence evidence admission', 'Offer only expected event descriptors without actual native writer/admission/persisted event artifacts', 'REJECT; oracle is not an occurred event, no occurrence PASS'),
        ('snapshot_as_occurrence', 'END prospective mapping guard', 'Offer expected/actual post Snapshot only', 'REJECT; SnapshotId is not event identity or native occurrence'),
        ('report_as_occurrence', 'END prospective mapping guard', 'Offer PASS/selection/result label/report only', 'REJECT; no typed ledger event payload/membership'),
        ('prospective_labeled_historical', 'END qualification labeling guard', 'Change ORIGINAL_HISTORICAL_OCCURRENCE to PROVEN or claim recovery', 'REJECT; original remains UNPROVEN'),
        ('prospective_bound_as_original_identity', 'END identity-domain guard', 'Populate original historical event slot or splice prospective event into original P04 ancestry', 'REJECT; separate replacement binding only'),
        ('selection_as_execution_N12', 'Native typed boundary and occurrence guard', 'Use select/recompute trace as result/completion, with no SuppliedResult', 'REJECT; exact start bytes/ledger/knowledge unchanged'),
        ('output_declaration_as_result_N13', 'Native typed SuppliedResult boundary', 'Submit Action/output declaration/KnowledgeRecord itself instead of typed actual SuppliedResult', 'REJECT wrong event/result; knowledge/root/slot/ledger unchanged'),
        ('oracle_loaded_as_operand', 'Comparison-only input separation', 'Read expected-results/events as provider or submit an oracle event directly as actual evidence', 'REJECT; allowlisted authored input provider and native admission evidence required'),
        ('duplicate_KnowledgeId', 'Native unique/supplied-result validation', 'Submit duplicate identical knowledge record identities', 'REJECT duplicate identifier; unordered fields are not multisets'),
        ('repeat_committed_command', 'Native codec.commit_event current parent guard', 'Resubmit a pre-commit operand against head after success', 'REJECT stale pre-state/parent; no third semantic event'),
    ]
    negatives = [{'id': 'A03-PROSPECTIVE-N%02d' % (i + 1), 'name': name,
                  'layer': layer, 'mutation': mutation, 'expected': expected,
                  'base': 'Isolated copy of presealed start or relevant expected boundary, never canonical target',
                  'on_rejection': 'No durable successor/event/knowledge; prior committed bytes/head unchanged',
                  'qualification_status': 'SEALED_NOT_EXECUTED'}
                 for i, (name, layer, mutation, expected) in enumerate(negative_rows)]
    negative_pin = save(OUT / 'negative-contract.json', {
        'schema': 'E2-P05-A03-PROSPECTIVE-NEGATIVE-CONTRACT-1', **LABELS,
        'comparison_only': True, 'count': len(negatives), 'cases': negatives,
        'N12_original_expected_state': cases_by_id['E2-N12']['EXPECTED_STATE'],
        'N13_original_expected_state': cases_by_id['E2-N13']['EXPECTED_STATE'],
        'not_a_P05_execution': True,
        'wrong_parent_mutation': 'One dimension at a time; retain trusted expected bundle/event identity; attacker rehash is not a new trust anchor',
        'mapping_negatives_layer': 'Qualification evidence manifest/acceptance guard, not invented native END API',
    })

    future_root = 'docs/plans/qualification/E2_P05_A03_PROSPECTIVE_OCCURRENCE_EXECUTION_1'
    persistence = {
        'write_now': False, 'future_output_root': future_root,
        'ordinary_native_head_directory': future_root + '/writer-main/native-head',
        'start': {'file': relative(start_path), 'trusted_bundle_identity': identity_text(start_bundle_id),
                  'native_restore': 'codec.restore with exact expected start identity; empty events requires no event files'},
        'boundaries': [
            {'boundary': 'POST_CHECK', 'native_bundle_id': event_specs[0]['EXPECTED_POST_BUNDLE_ID'],
             'state_id': event_specs[0]['POST_STATE_ID'], 'event_count': 1,
             'head': event_specs[0]['EXPECTED_EVENT_ID'], 'parent': None,
             'path': future_root + '/writer-main/checkpoints/post-check'},
            {'boundary': 'POST_COLLECT', 'native_bundle_id': event_specs[1]['EXPECTED_POST_BUNDLE_ID'],
             'state_id': event_specs[1]['POST_STATE_ID'], 'event_count': 2,
             'head': event_specs[1]['EXPECTED_EVENT_ID'], 'parent': event_specs[0]['EXPECTED_EVENT_ID'],
             'path': future_root + '/writer-main/checkpoints/post-collect'},
        ],
        'commit': 'codec.commit_event using actual freshly supplied result and exact current bundle. It verifies the current HEAD, saves complete native bundle/event files and atomically publishes HEAD. No manual status or knowledge changes.',
        'preserve': ['Initial/current snapshots', 'Complete typed SuppliedResults/KnowledgeRecords', 'Ordered ExecutionEvents',
                     'Parent/pre/post/sequence/content identities', 'Physical source and policy pins',
                     'Scope/lineage/generation/provenance', 'HEAD.previous and command=None audit semantics'],
        'checkpoint_publication': 'Save actual native bundle/event artifacts beside each checkpoint bundle via codec.save_bundle; duplicating immutable bytes is not another semantic event',
        'atomicity': 'Only a consistent published head is canonical for this isolated qualification run; orphan files cannot establish an occurred result. Stop on partial/failed commit and report it.',
        'root': 'CHECK event identity after first append; ordinary native event root, not GENESIS root commitment',
        'ledger_container_identity': 'Native BundleId at each boundary plus /bundle/events; no standalone ordinary LedgerId is invented',
    }
    cold_restore = {
        'execute_now': False, 'writer_termination': 'Writer process must exit before independent readers start',
        'hash_seeds': [0, 1, 7, 101], 'cold_readers_per_checkpoint_per_seed': 3,
        'checkpoints': ['SEALED_START', 'POST_CHECK', 'POST_COLLECT'],
        'total_minimum_reader_comparisons': 36,
        'checks': ['Trusted exact raw BundleId', 'Exact immutable event bytes/identities and positions',
                   'Current/initial native state identities', 'Parent and source/policy audit',
                   'Exact admitted result/output/currentness', 'Recomputed full Computation/selection',
                   'Read-only END replacement mapping and historical UNPROVEN marker'],
        'END_mapping_restore': 'Re-read pinned authorization and mapping manifest separately; recompute evidence binding from actual restored events. No native END object serialized.',
        'forbid': 'Reading writer-memory, saved control/permission labels as authority, or oracle data as Planner input',
    }
    replay = {
        'execute_now': False, 'start_bundle_id': identity_text(start_bundle_id),
        'sequence': ['E2-CHECK actual SuppliedResult/event 1', 'E2-COLLECT actual SuppliedResult/event 2'],
        'native_function': 'codec._replay of actual persisted ordinary bundle plus prefix validation',
        'exactness': 'Same typed results, KnowledgeRecords, parent chain, state/bundle/event identities, full recomputed native Computation; exactly two semantic events',
        'not_new_decision': 'Consume recorded supplied results; do not reacquire outputs or call provider/executor as a new operation',
        'historical_limit': 'Replay of this new lineage proves no original A03 occurrence, parent or historical P04 ancestry',
    }
    determinism = {
        'execute_now': False, 'hash_seeds': [0, 1, 7, 101],
        'independent_writer_processes_per_seed': 3,
        'cold_readers_per_checkpoint_per_seed': 3,
        'unordered_presentations': ['Original', 'Reversed', 'Rotated'],
        'unordered_fields': ['Snapshot.actions/statuses/roots/predicates/goals/knowledge', 'PersistenceBundle.sources',
                             'Action.accepted_inventory and prerequisites where codec declares set semantics', 'SuppliedResult.knowledge'],
        'object_key_permutations': True,
        'nonpermutable': ['Causal event order CHECK -> COLLECT', 'sequence/parent links', 'ordered selector clauses',
                          'result-provider invocation order', 'non-set native fields'],
        'compare': ['Canonical state/bundle/event bytes and native identities', 'Complete typed results/provenance',
                    'Full Computation, witnesses, reasons, selections', 'Rejections and exact END mapping semantics'],
        'no_runtime_entropy': 'Writer labels, PID, time and output directories are report metadata only, never native identity fields',
        'membership_negatives': 'Different source/output membership must remain different; duplicate native identifiers reject',
    }
    occurrence = {
        'status_now': 'NOT_EXECUTED', 'PASS_requires_all': [
            'Exact selected Action and current sealed pre-state', 'Fresh typed actual supplied result matches PC01 bounded oracle',
            'Actual native commit/admission produces expected transition and event payload',
            'Exact expected native event identity/parent/sequence and source/result binding',
            'Membership in exact newly declared ordered ledger, one CHECK then one COLLECT event',
            'No PREPARE/DECIDE/REENTER/FINISH event or extra authority/configuration',
            'Durable native bundle/event/HEAD and independent cold restoration',
            'Historical replay preserves exact new semantic occurrence', 'All sealed negative controls and determinism pass',
            'Separate END authorized replacement mapping and historical UNPROVEN label remain exact'],
        'not_sufficient': ['Expected event hash', 'Definition/accepted inventory', 'Selection trace', 'Post-state alone',
                          'Result/report label', 'Retained historical PASS report'],
        'original_historical_occurrence_result': 'UNPROVEN even after future prospective PASS',
    }
    execution = {
        'package': 'E2-P05-A03-PROSPECTIVE-OCCURRENCE-EXECUTION-1',
        'request_required_before_execution': 'This contract package performs no execution; later execution instruction must invoke the sealed contract',
        'entry': 'Load exact native sealed start, not historical completed snapshots; verify every input/runtime/source/policy/capture pin and explicit empty head/ledger',
        'sequence': [
            'Read-only recompute/select twice; CHECK exact; canonical bytes/ledger/knowledge unchanged (N12 boundary)',
            'Invoke bounded synthetic provider for CHECK using authored input declarations, not oracle files',
            'Run native typed/current-selection/result validation; commit via ordinary codec.commit_event exactly once',
            'Compare actual CHECK result/event/post-state with independently sealed oracle; persist checkpoint',
            'Recompute current selection COLLECT; freshly provide and commit COLLECT exactly once, parent CHECK',
            'Compare actual COLLECT result/event/post-state; PREPARE may be ready but must not execute',
            'Persist final exact two-event qualification bundle and all event files; terminate writer',
            'Run cold-reader, replay, independent-writer/permutation and isolated negative dimensions',
            'Only on all PASS bind read-only authorized prospective A03 evidence into P05 with original history UNPROVEN',
            'Recheck prior bindings and identify only next missing input A04; stop without P05/P06 execution'],
        'STOP_on': ['Any definition/source/content/policy/runtime/input identity divergence',
                    'Wrong authority/scope/lineage/generation', 'Different selected Action/result/output/parent/pre/post/sequence',
                    'Extra event/install/authority or failure of N12/N13 mapping',
                    'Oracle used as input or post-hoc fixture/expected-answer changes',
                    'Any persistence/replay/negative/determinism mismatch'],
        'failure_record': ['FIRST_COUNTEREXAMPLE', 'EXPECTED', 'ACTUAL', 'STATE_ID', 'EVENT_ID', 'CLASSIFICATION'],
        'no_live_repair': True,
        'retry': 'Do not reexecute an already committed positive Action. Existing writer-main head or incomplete run requires stop/audit; independent reproductions use separate isolated output directories and the same sealed inputs.',
        'native_API_limit': 'Ordinary supplied-result transaction has no command-ID operand; current bundle/head lock, expected_snapshot and event chronology provide the native binding',
    }
    plans_pin = save(OUT / 'execution-and-persistence-contract.json', {
        'schema': 'E2-P05-A03-PROSPECTIVE-EXECUTION-PLAN-1', **LABELS,
        'occurrence': occurrence, 'persistence': persistence, 'cold_restore': cold_restore,
        'replay': replay, 'determinism': determinism, 'execution': execution,
    })

    relevant = [recovery_path, recovery_path.with_suffix('.md'), dossier_path,
        PLANS/(PREFIX+'E2_P05_END_INPUT_BINDING_1.json'), PLANS/(PREFIX+'E2_P05_END_INPUT_BINDING_1.md'),
        PLANS/(PREFIX+'E2_P05_READINESS.json'), PLANS/(PREFIX+'E2_P05_READINESS.md'),
        canonical_path, canonical_path.with_suffix('.md'),
        PLANS/(PREFIX+'CANONICAL_QUALIFICATION_ACCEPTANCE_MATRIX_1.md'),
        template_path, declaration_path, ROOT/POLICY_PIN.path,
        ROOT/'adapter/tests/qualify_p03_prospective.py', ROOT/'adapter/planner/action_materializer.py',
        ROOT/'adapter/planner/codec.py', ROOT/'adapter/planner/model.py', ROOT/'adapter/planner/core.py',
        ROOT/'adapter/planner/gates.py', ROOT/'adapter/planner/selector.py',
        ROOT/'docs/plans/qualification/E2_P05_END_INPUT_BINDING_1/input-oracle.json',
        ROOT/'docs/plans/qualification/E2_P05_READINESS_1/sealed-negative-oracles.json']
    sources_pin = save(OUT / 'authoritative-source-pins.json', {'sources': [file_pin(path) for path in relevant]})
    artifacts = [authorization_pin, start_pin, input_pin, oracle_events_pin, result_pin,
                 assurance_pin, end_pin, negative_pin, plans_pin, sources_pin,
                 file_pin(start_path), file_pin(OUT/'inputs/starting-snapshot.json'), file_pin(producer_path)]
    artifacts.extend(file_pin(ROOT/pin.path) for pin in source_pins)
    seal = {
        'schema': 'E2-P05-A03-PROSPECTIVE-PREEXECUTION-SEAL-1', **LABELS,
        'selected_option': SELECTED,
        'definition_semantics': 'Exact PC01 A03 CHECK/COLLECT bounded result declarations; source/context rebound prospectively',
        'START_BUNDLE_ID': identity_text(start_bundle_id), 'START_STATE_ID': identity_text(start_id),
        'scope': SCOPE, 'lineage': LINEAGE, 'generation': GENERATION,
        'LEDGER_ID': start_spec['LEDGER_ID'], 'LEDGER_ROOT': None, 'APPEND_HEAD': None, 'PARENT_EVENT_ID': None,
        'explicit_empty_ledger': True, 'all_inputs_oracles_negatives_sealed_before_execution': True,
        'artifacts': artifacts, 'native_runtime_sha256': input_inventory['runtime_and_native_contracts'],
        'sealing_procedure_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'positive_transition_functions_called': [],
        'native_empty_start_validation': True,
        'expected_native_events_are_comparison_only': True,
        'execution_started': False, 'PROSPECTIVE_A03_EXECUTED': 'NO',
        'N12_MAPPING_PRESERVED': 'YES', 'N13_MAPPING_PRESERVED': 'YES',
        'authority_applicable': 'YES; selected qualification-scope decision; native CHECK/COLLECT authority=None',
        'additional_authority_required': False, 'new_native_authorities_issued': 0,
        'TBD_terms': [], 'execution_contract_ready': True,
    }
    seal_pin = save(OUT / 'seal.json', seal)
    report = {
        'schema': 'E2-P05-A03-PROSPECTIVE-OCCURRENCE-CONTRACT-1',
        'WORK_PACKAGE': 'E2-P05-A03-PROSPECTIVE-OCCURRENCE-CONTRACT',
        'RESULT': 'PASS', 'CONTRACT_ONLY': True, 'SELECTED_OPTION': SELECTED, **LABELS,
        'ORIGINAL_A03_HISTORICAL_OCCURRENCE': 'UNPROVEN',
        'AUTHORIZATION_AUTHENTICATION': 'PASS',
        'ORIGINAL_ASSURANCE': original_assurance,
        'PROSPECTIVE_ASSURANCE': {'source': assurance_pin, 'status': 'SEALED_NOT_EXECUTED'},
        'A03_DEFINITION': {'A03_ID': 'E2-A03', 'A03_TYPE': 'Acceptance case / bounded native supplied-result operation',
            'A03_PRECONDITIONS': cases_by_id['E2-A03']['INITIAL_STATE'], 'canonical_case': cases_by_id['E2-A03'],
            'native_Actions': prospective_declarations,
            'A03_NATIVE_OPERATION': 'codec.commit_event -> codec.record_result -> apply_event/apply_result -> append_event/native ledger replay -> atomic HEAD publication',
            'A03_AUTHORITY': 'None for ordinary NON_EFFECTING CHECK/COLLECT; qualification scope decision is separate',
            'A03_POSTCONDITION': cases_by_id['E2-A03']['EXPECTED_STATE'],
            'owner': 'E2-P02 historically; this is a separately authorized prospective qualification for the P05 A03 evidence term'},
        'PROSPECTIVE_START': start_spec, 'PROSPECTIVE_INPUTS': input_pin,
        'AUTHORITY': authorization_pin, 'EXPECTED_RESULT_ORACLE': result_pin,
        'EXPECTED_EVENT_ORACLE': oracle_events_pin, 'OCCURRENCE_ORACLE': occurrence,
        'END_MAPPING': end_pin, 'N12_MAPPING': {'source': assurance_pin, 'pointer': '/N12_mapping'},
        'N13_MAPPING': {'source': assurance_pin, 'pointer': '/N13_mapping'},
        'N12_MAPPING_PRESERVED': 'YES', 'N13_MAPPING_PRESERVED': 'YES',
        'PERSISTENCE_CONTRACT': persistence, 'COLD_RESTORE_CONTRACT': cold_restore,
        'REPLAY_CONTRACT': replay, 'DETERMINISM_CONTRACT': determinism,
        'NEGATIVE_SUITE': negative_pin, 'NEGATIVE_CASE_COUNT': len(negatives),
        'EXECUTION_CONTRACT': execution, 'PREEXECUTION_SEAL': seal_pin,
        'AUTHORITATIVE_SOURCE_PINS': sources_pin,
        'PROSPECTIVE_A03_AUTHORITY_DECISION_REQUIRED': 'NO',
        'PROSPECTIVE_A03_AUTHORITY_DECISION_READY': 'NO',
        'AUTHORITY_DECISION_READY_MEANING': 'NOT_REQUIRED; applicable scope decision already selected, no new native operating grant',
        'PROSPECTIVE_A03_EXECUTION_READY': 'YES',
        'EXECUTION_READY_MEANING': 'Sealed contract ready for a separately requested prospective execution package; no positive experiment verdict claimed',
        'PROSPECTIVE_A03_EXECUTED': 'NO', 'P05_EXECUTED': 'NO', 'P06_EXECUTED': 'NO',
        'P05_BOUND_STAGE_INPUTS': 9, 'P05_TOTAL_STAGE_INPUTS': 13, 'P05_EXECUTION_READY': 'NO',
        'P05_BINDING_GRAPH_CHANGED': 'NO', 'P05_NEXT_MISSING_INPUT': 'E2-A03.native_result_event_trace',
        'AFTER_FUTURE_A03_SUCCESS_NEXT_MISSING_INPUT': 'E2-A04.prepare_result_event_ancestry',
        'P01_RESULT': 'PASS', 'P02_RESULT': 'PASS', 'P03_RESULT': 'PASS', 'P04_RESULT': 'PASS',
        'P05_INITIAL_ORACLE': 'PASS', 'P03_HISTORICAL_CORRESPONDENCE': 'UNPROVEN', 'N_REAL_SATISFIED': 'NO',
        'RUNTIME_MODIFIED': 'NO', 'E1_ARTIFACTS_MODIFIED': 0, 'PRODUCTION_EFFECT': 'NO',
        'NEW_NATIVE_AUTHORITIES': 0, 'NATIVE_EVENTS_ADMITTED': 0,
        'NEXT_PACKAGE': 'E2-P05-A03-PROSPECTIVE-OCCURRENCE-EXECUTION-1',
    }
    report_path = PLANS / (PREFIX + 'E2_P05_A03_PROSPECTIVE_OCCURRENCE_CONTRACT_1.json')
    # Verification records are added after the semantic contract is sealed.
    # Preserve only these separately pinned audit fields on a repeat sealing
    # check; all contract/input/oracle fields still require exact byte equality.
    if report_path.exists():
        prior_report = json.loads(report_path.read_bytes())
        for key in ('PRESERVATION', 'METADATA_VALIDATION', 'GIT_DIFF_CHECK'):
            if key in prior_report:
                report[key] = prior_report[key]
    save(report_path, report)
    print(json.dumps({'result': report['RESULT'], 'start_state': identity_text(start_id),
                     'start_bundle': identity_text(start_bundle_id), 'source_files': len(source_pins),
                     'expected_event_ids': [row['EXPECTED_EVENT_ID'] for row in event_specs],
                     'negative_cases': len(negatives), 'positive_execution': False}, indent=2))


if __name__ == '__main__':
    main()
