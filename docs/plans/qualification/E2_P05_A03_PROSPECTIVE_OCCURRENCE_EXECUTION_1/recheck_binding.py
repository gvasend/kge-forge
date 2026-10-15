"""Recheck P05 evidence, applying only the selected A03 replacement mapping.

No original artifact is rewritten and no P05/END operation is executed.
"""
import hashlib
import os
from pathlib import Path
import sys

import execution_driver as d
from qualification_checks import primary_evidence, validate_occurrence_evidence
from adapter.planner import codec as c, model as m, typed_proofs as tp

OLD = d.OUT.with_name('E2_P05_END_INPUT_BINDING_1')


def verify_pins(value, pins):
    if isinstance(value, dict):
        if 'path' in value and 'raw_sha256' in value:
            path = d.ROOT / value['path']
            d.equal('PRIOR_BINDING_PIN:' + value['path'], hashlib.sha256(path.read_bytes()).hexdigest(), value['raw_sha256'])
            pins.add((value['path'], value['raw_sha256']))
            pointer = value.get('pointer')
            if pointer:
                current = d.read(path)
                for part in pointer[1:].split('/'):
                    part = part.replace('~1', '/').replace('~0', '~')
                    current = current[int(part)] if isinstance(current, list) else current[part]
        for item in value.values():
            verify_pins(item, pins)
    elif isinstance(value, list):
        for item in value:
            verify_pins(item, pins)


def reconstruct():
    d.verify_entry()
    for name in ('cold-restore-and-replay.json', 'independent-reproduction-and-determinism.json', 'negative-results.json'):
        d.equal('QUALIFICATION_GATE:' + name, d.read(d.OUT / name)['result'], 'PASS')
    negative = d.read(d.OUT / 'negative-results.json')
    d.equal('N12_GATE', negative['N12_MAPPING'], 'PASS')
    d.equal('N13_GATE', negative['N13_MAPPING'], 'PASS')
    mapping = d.read(d.SEALED / 'END-acceptance-mapping.json')
    prospective = validate_occurrence_evidence(primary_evidence())
    prior = d.read(OLD / 'canonical-bindings.json')
    original_report = d.read(d.PLANS / 'DETERMINISTIC_PLANNER_V0_1_E2_P05_END_INPUT_BINDING_1.json')
    old_comparison = d.read(OLD / 'input-oracle-comparison.json')
    pins = set()
    for name in ('canonical-bindings.json', 'input-oracle.json', 'input-oracle-comparison.json',
                 'dependency-DAG.json', 'configuration-history.json', 'P03-replacement-treatment.json'):
        verify_pins(d.read(OLD / name), pins)
    d.equal('PRIOR_BOUND_COUNT', sum(row['binding_status'] == 'BOUND' for row in prior['stage_bindings']), 9)
    d.equal('PRIOR_DECLARED_COUNT', original_report['A01_A13_BOUND_COUNT'], 9)
    for row in old_comparison['per_slot_comparisons']:
        binding = next(item for item in prior['stage_bindings'] if item['STEP_ID'] == row['slot'])
        if binding['binding_status'] == 'BOUND':
            d.equal('PRIOR_SLOT_ORACLE:' + row['slot'], row['binding_result'], 'PASS')

    target_path = d.ROOT / prior['actual_target']['path']
    target_raw = target_path.read_bytes()
    target = c._unwire(c.parse_json(target_raw)['bundle'])
    m.validate_types(target, m.PersistenceBundle)
    d.equal('CANONICAL_P04_BYTES', c._bundle_bytes_admitted(target), target_raw)
    p04_report = d.read(d.PLANS / 'DETERMINISTIC_PLANNER_V0_1_E2_P04_CANONICAL_EXECUTION_RETRY_1_RESULT.json')
    d.equal('P04_RESULT', p04_report['E2_P04_RESULT'], 'PASS')
    d.equal('P04_TARGET_BUNDLE', d.uid(c._identity(target_raw, 'planner-bundle-v1')), p04_report['FINAL_P04_BUNDLE_ID'])
    d.equal('P04_TARGET_STATE', d.uid(c.snapshot_id(target.current)), p04_report['FINAL_STATE_ID'])
    parent, parent_snapshot = None, c.snapshot_id(target.initial)
    for number, event in enumerate(target.events, 1):
        d.equal('P04_EVENT_SEQUENCE', event.sequence, number)
        d.equal('P04_EVENT_PARENT', event.parent_event, parent)
        d.equal('P04_PRE_STATE_CONTINUITY', event.parent_snapshot, parent_snapshot)
        d.equal('P04_EVENT_IDENTITY', event.identity, c._event_identity(number, event.parent_snapshot, event.parent_event, event.result, event.after_snapshot, event.resume_binding))
        path = target_path.parent / ('event-' + event.identity.sha256 + '.json')
        d.equal('P04_EVENT_BYTES', path.read_bytes(), c.canonical_bytes(c._wire(event)))
        parent, parent_snapshot = event.identity, event.after_snapshot
    d.equal('P04_LAST_STATE', parent_snapshot, c.snapshot_id(target.current))
    for proof in target.current.typed_proofs:
        d.equal('P04_TYPED_PROOF_CURRENT', tp.usable(target.current, proof), True)

    checkpoint_path = d.PLANS / 'DETERMINISTIC_PLANNER_V0_1_P03_PROSPECTIVE_CHECKPOINT_BUNDLE_1.json'
    checkpoint_raw = checkpoint_path.read_bytes()
    checkpoint = c._unwire(c.parse_json(checkpoint_raw)['bundle'])
    d.equal('P03_PREFIX_INITIAL', c._wire(checkpoint.initial), c._wire(target.initial))
    d.equal('P03_PREFIX_EVENTS', c._wire(checkpoint.events), c._wire(target.events[:2]))
    d.equal('P03_POLICY_PRESERVED', checkpoint.policy, target.policy)
    scope = d.read(d.PLANS / 'qualification/P03_PROSPECTIVE_CHECKPOINT_1/sources/qualification-scope-authority.json')
    d.equal('P03_SCOPE_DECISION', scope['selected_option'], 'AUTHORIZE_PROSPECTIVE_P03_CHECKPOINT_QUALIFICATION')

    stages = []
    for old in prior['stage_bindings']:
        name = old['STEP_ID']
        if old['binding_status'] == 'BOUND':
            for event in old['EVENTS']:
                d.equal(name + ':EXACT_CANONICAL_EVENT', event, c._wire(target.events[event['sequence'] - 1]))
            if name in ('E2-A07', 'E2-A08'):
                d.equal(name + ':CHECKPOINT_ID', old['actual_identity']['bundle'], d.uid(c._identity(checkpoint_raw, 'planner-bundle-v1')))
            stages.append({'stage': name, 'binding_status': 'BOUND', 'classification': old['source_classification'],
                           'recheck': 'PASS; exact prior source pins/pointers/native identity and governing scope',
                           'identity': old['actual_identity'], 'original_binding': d.pin(OLD / 'canonical-bindings.json'),
                           'new_execution': False, 'original_record_changed': False})
        elif name == 'E2-A03':
            stages.append({'stage': name, 'logical_required_input': mapping['logical_required_slot'],
                           'binding_status': 'BOUND', 'classification': 'AUTHORIZED_PROSPECTIVE_REPLACEMENT',
                           'governing_decision': d.read(d.SEALED / 'authorization-capture.json')['selected_option'],
                           'original_historical_occurrence': 'UNPROVEN', 'original_historical_event_ids': None,
                           'original_binding': d.pin(OLD / 'canonical-bindings.json'),
                           'replacement_term': mapping['replacement_term'],
                           'replacement_native_event_ids': [d.uid(event.identity) for event in prospective.events],
                           'replacement_start_bundle_id': mapping['replacement_expected_ledger']['start_bundle_id'],
                           'replacement_post_bundle_id': d.uid(c.bundle_id(prospective)),
                           'replacement_context': c._wire(prospective.current.context),
                           'replacement_writer': d.pin(d.OUT / 'writer-main/writer-result.json'),
                           'replacement_oracle': d.pin(d.SEALED / 'END-acceptance-mapping.json'),
                           'N12_MAPPING': 'PASS', 'N13_MAPPING': 'PASS', 'mapping_result': 'PASS',
                           'historical_identity_alias': False, 'original_history_splice': False,
                           'provenance_and_currentness': 'Exact fresh native supplied-result/current selection/source/parent bindings at the sealed qualification scope'})
        else:
            stages.append({'stage': name, 'binding_status': old['binding_status'],
                           'classification': 'MISSING_ORIGINAL_NATIVE_OCCURRENCE',
                           'identity': old['actual_identity'], 'original_record_changed': False,
                           'new_execution': False, 'resolved_in_this_package': False})
    d.equal('RECONSTRUCTED_STAGE_UNIVERSE', [row['stage'] for row in stages], ['E2-A%02d' % number for number in range(1, 14)])
    count = sum(row['binding_status'] == 'BOUND' for row in stages)
    d.equal('A03_ONLY_BINDING_EFFECT', count, 10)
    next_missing = next(row['stage'] for row in stages if row['binding_status'] != 'BOUND')
    d.equal('FIRST_NEW_FRONTIER', next_missing, 'E2-A04')
    return {**d.LABELS, 'schema': 'E2-P05-A03-AUTHORIZED-PROSPECTIVE-BINDING-RESULT-1',
            'result': 'PASS_FOR_A03_MAPPING; FULL_GRAPH_INCOMPLETE',
            'E2_A03_NATIVE_RESULT_EVENT_TRACE': 'PASS', 'END_MAPPING': 'PASS',
            'END_type': mapping['END_type'], 'binding_representation': mapping['binding_representation'],
            'stage_bindings': stages, 'P05_PREVIOUS_BOUND_STAGE_INPUTS': 9,
            'P05_BOUND_STAGE_INPUTS': count, 'P05_TOTAL_STAGE_INPUTS': 13,
            'P05_NEXT_MISSING_INPUT': mapping['A04_future_frontier'].split(';')[0],
            'remaining_stage_gaps': mapping['remaining_stage_gaps'],
            'additional_unresolved_END_gate': mapping['additional_unresolved_END_gate'],
            'original_ancestry_edges_changed': False,
            'canonical_P04_event_count': len(target.events), 'canonical_P04_unchanged': True,
            'prior_source_hash_pins_rechecked': len(pins),
            'P03_scope_decision_reopened': False, 'P03_HISTORICAL_CORRESPONDENCE': 'UNPROVEN',
            'N_REAL_SATISFIED': 'NO', 'P05_INITIAL_ORACLE': 'PASS; exact prior oracle/pins preserved',
            'P05_EXECUTION_READY': 'NO', 'E2_END_INPUT_GRAPH': 'FAIL_COMPLETENESS',
            'P05_EXECUTED': 'NO', 'P06_EXECUTED': 'NO',
            'next_missing_input_resolved': False,
            'NEXT_PACKAGE': 'E2-P05-A04-NATIVE-OCCURRENCE-WITNESS-RECOVERY',
            'new_native_objects_or_authority_from_graph_binding': 0}


if __name__ == '__main__':
    try:
        graph = reconstruct()
        seed = os.environ.get('PYTHONHASHSEED')
        d.write(d.OUT / 'graph-readers' / ('seed-' + seed + '.json'), graph)
        print(__import__('json').dumps({'result': 'PASS', 'A03_mapping': graph['END_MAPPING'],
              'P05_bound_stage_inputs': graph['P05_BOUND_STAGE_INPUTS'],
              'next_missing_input': graph['P05_NEXT_MISSING_INPUT'], 'hash_seed': seed}))
    except Exception as exc:
        record = {**d.LABELS, 'result': 'FAIL', 'FIRST_COUNTEREXAMPLE': getattr(exc, 'name', type(exc).__name__),
                  'EXPECTED': repr(getattr(exc, 'expected', None)), 'ACTUAL': repr(getattr(exc, 'actual', str(exc))),
                  'STATE_ID': None, 'EVENT_ID': None, 'CLASSIFICATION': 'BINDING_RECHECK_FAILED', 'no_live_repair': True}
        d.write(d.OUT / 'STOP.json', record)
        print(__import__('json').dumps(record, sort_keys=True))
        raise
