"""Publish read-only evidence of the completed prospective qualification."""
import hashlib
import json
from pathlib import Path

import execution_driver as d
from qualification_checks import primary_evidence, validate_occurrence_evidence
from adapter.planner import codec as c


def main():
    d.verify_entry()
    d.equal('NO_STOP_RECORD', (d.OUT / 'STOP.json').exists(), False)
    driver = d.read(d.OUT / 'driver-seal.json')
    for name, digest in driver['driver_files'].items():
        d.equal('EXECUTION_DRIVER_UNCHANGED', hashlib.sha256((d.ROOT / name).read_bytes()).hexdigest(), digest)
    primary = d.read(d.OUT / 'writer-main/writer-result.json')
    cold = d.read(d.OUT / 'cold-restore-and-replay.json')
    deterministic = d.read(d.OUT / 'independent-reproduction-and-determinism.json')
    negatives = d.read(d.OUT / 'negative-results.json')
    graph = d.read(d.OUT / 'P05-binding-rerun.json')
    for name, value in [('PRIMARY', primary), ('COLD', cold), ('DETERMINISM', deterministic), ('NEGATIVES', negatives)]:
        d.equal(name, value['result'], 'PASS')
    d.equal('COLD_READER_COUNT', cold['independent_reader_count'], 36)
    d.equal('INDEPENDENT_WRITER_COUNT', deterministic['independent_writer_count'], 12)
    d.equal('NEGATIVE_COUNT', negatives['count'], 24)
    d.equal('GRAPH_COUNT', graph['P05_BOUND_STAGE_INPUTS'], 10)
    bundle = validate_occurrence_evidence(primary_evidence())
    expected_events = d.read(d.SEALED / 'oracles/expected-events.json')['event_oracles']
    expected_results = d.read(d.SEALED / 'oracles/expected-results.json')['result_oracles']
    checks = []

    def term(name, actual, expected):
        d.equal(name, actual, expected)
        checks.append({'term': name, 'actual': actual, 'expected': expected, 'result': 'PASS'})

    for index, event in enumerate(bundle.events):
        oracle = expected_events[index]
        checkpoint = primary['boundaries'][index + 1]
        trace = primary['events'][index]
        prefix = c._prefix_bundle(bundle, index + 1)
        label = event.result.action.value
        term(label + ':type', type(event).__name__, 'ExecutionEvent')
        term(label + ':event_id', d.uid(event.identity), oracle['EXPECTED_EVENT_ID'])
        term(label + ':payload', c._wire(event.result), oracle['expected_native_wire']['result'])
        term(label + ':parent', d.uid(event.parent_event), None if index == 0 else expected_events[index - 1]['EXPECTED_EVENT_ID'])
        term(label + ':pre_state', d.uid(event.parent_snapshot), oracle['PRE_STATE_ID'])
        term(label + ':post_state', d.uid(event.after_snapshot), oracle['POST_STATE_ID'])
        term(label + ':sequence', event.sequence, index + 1)
        term(label + ':post_bundle', d.uid(c.bundle_id(prefix)), checkpoint['bundle_id'])
        term(label + ':post_snapshot', c._wire(prefix.current), expected_results[index]['post_state'])
        term(label + ':typed_result', type(event.result).__name__, 'SuppliedResult')
        term(label + ':knowledge', [c._wire(k) for k in event.result.knowledge], expected_results[index]['knowledge'][-1:] if index == 0 else [k for k in expected_results[index]['knowledge'] if k['producer']['value'] == label])
        term(label + ':result_outcome', event.result.result.value, expected_results[index]['outcome'])
        term(label + ':ledger_anchor', trace['lineage_ledger_anchor'], d.read(d.SEALED / 'prospective-start.json')['LEDGER_ID'])
        term(label + ':scope', trace['SCOPE'], bundle.current.context.scope)
        term(label + ':lineage', trace['LINEAGE'], bundle.current.context.lineage)
        term(label + ':generation', trace['GENERATION'], bundle.current.context.generation)
        event_file = d.ROOT / trace['durable_event_file']['path']
        term(label + ':durable_event_bytes', hashlib.sha256(event_file.read_bytes()).hexdigest(), hashlib.sha256(c.canonical_bytes(c._wire(event))).hexdigest())
        term(label + ':provider_oracle_reads', trace['provider_invocation']['oracle_files_read_by_provider'], [])
        term(label + ':native_transaction', trace['actual_native_transaction'], True)
    comparison = {**d.LABELS, 'result': 'PASS', 'checks': checks,
                  'actual_event_count': len(bundle.events), 'original_event_identity_populated': False,
                  'cold_restore': 'PASS', 'replay': 'PASS', 'determinism': 'PASS', 'negatives': 'PASS',
                  'not_external_world_executor_attestation': True}
    d.write(d.OUT / 'occurrence-oracle-comparison.json', comparison)

    # Immutable copies of the actual committed bundle/events, no new transaction.
    native_path, native_id = c.save_bundle(bundle, d.PLANS, d.ROOT)
    alias = d.PLANS / 'DETERMINISTIC_PLANNER_V0_1_E2_P05_A03_PROSPECTIVE_OCCURRENCE_BUNDLE_1.json'
    if alias.exists():
        d.equal('IMMUTABLE_BUNDLE_ALIAS', alias.read_bytes(), native_path.read_bytes())
    else:
        alias.write_bytes(native_path.read_bytes())
    restored = c.restore(alias, native_id, d.ROOT)
    d.equal('PUBLISHED_NATIVE_BUNDLE', c._wire(restored), c._wire(bundle))
    d.write(d.OUT / 'persistence.json', {**d.LABELS, 'result': 'PASS',
        'primary_native_head': d.pin(d.OUT / 'writer-main/native-head/HEAD.json'),
        'native_immutable_bundle': d.pin(native_path), 'named_bundle': d.pin(alias),
        'bundle_id': d.uid(native_id), 'root': d.uid(bundle.events[0].identity),
        'append_head': d.uid(bundle.events[-1].identity), 'new_semantic_events_from_copy': 0,
        'named_bundle_trusted_restore': 'PASS'})

    last = bundle.events[-1]
    report = {
        **d.LABELS, 'schema': 'E2-P05-A03-PROSPECTIVE-OCCURRENCE-EXECUTION-RESULT-1',
        'WORK_PACKAGE': 'E2-P05-A03-PROSPECTIVE-OCCURRENCE-EXECUTION', 'RESULT': 'PASS',
        'SELECTED_OPTION': 'AUTHORIZE_PROSPECTIVE_P05_A03_OCCURRENCE_QUALIFICATION',
        'ENTRY_GATE': 'PASS', 'ENTRY_CHECK_COUNT': 35,
        'PROSPECTIVE_A03_EXECUTION': 'PASS; one primary experiment, CHECK and COLLECT each committed once',
        'ACTUAL_A03_RESULT': [{'ActionId': e.result.action.value, 'native_type': type(e.result).__name__,
                               'outcome': e.result.result.value, 'knowledge': [k.id.value for k in e.result.knowledge],
                               'native_payload': c._wire(e.result)} for e in bundle.events],
        'PROSPECTIVE_A03_EVENT_ID': d.uid(last.identity),
        'PROSPECTIVE_A03_EVENT_IDS': [d.uid(e.identity) for e in bundle.events],
        'PROSPECTIVE_A03_EVENT_ID_MEANING': 'Final COLLECT event; complete A03 witness requires both new CHECK/COLLECT events',
        'EVENT_PAYLOAD': [c._wire(e.result) for e in bundle.events],
        'PARENT_EVENT_ID': d.uid(last.parent_event),
        'PARENT_EVENT_IDS': [d.uid(e.parent_event) for e in bundle.events],
        'LEDGER_ID': d.uid(native_id) + '#/bundle/events',
        'START_LEDGER_ANCHOR': d.read(d.SEALED / 'prospective-start.json')['LEDGER_ID'],
        'LEDGER_ID_DOMAIN': 'Ordinary native BundleId/events coordinate; no standalone LedgerId invented',
        'LEDGER_POSITION': [e.sequence for e in bundle.events],
        'RESULT_BINDING': 'PASS', 'OUTPUT_BINDING': 'PASS', 'PROSPECTIVE_A03_OCCURRENCE': 'PASS',
        'POST_A03_BUNDLE_ID': d.uid(native_id), 'POST_A03_STATE_ID': d.uid(c.snapshot_id(bundle.current)),
        'POST_A03_LEDGER_ROOT': d.uid(bundle.events[0].identity), 'POST_A03_APPEND_HEAD': d.uid(last.identity),
        'POST_A03_BUNDLE': d.pin(alias), 'PERSISTENCE': 'PASS',
        'COLD_RESTORE': 'PASS; 36 independent readers after writer termination',
        'REPLAY': 'PASS; exact empty/CHECK/COLLECT prefixes, no provider invocation',
        'INDEPENDENT_REPRODUCTION': 'PASS; 12 isolated writer processes, three per hash seed',
        'DETERMINISM': 'PASS; seeds 0,1,7,101; original/reversed/rotated native unordered presentations and object keys; full Computation equal',
        'REPRODUCTION_IDENTITY_DOMAIN': deterministic['native_identity_semantics'],
        'NEGATIVE_SUITE': 'PASS; 24 sealed controls, 40 rejected variants; no durable partial state',
        'END_MAPPING': 'PASS; AUTHORIZED_PROSPECTIVE_REPLACEMENT; no historical identity alias or ancestry splice',
        'N12_MAPPING': 'PASS', 'N13_MAPPING': 'PASS',
        'N12_MAPPING_PRESERVED': 'YES', 'N13_MAPPING_PRESERVED': 'YES',
        'P05_WIDE_NEGATIVE_CASE_VERDICT': 'NOT_EVALUATED; these are scoped prospective N12/N13 mappings',
        'E2_A03_NATIVE_RESULT_EVENT_TRACE': 'PASS',
        'P05_BOUND_STAGE_INPUTS': graph['P05_BOUND_STAGE_INPUTS'], 'P05_TOTAL_STAGE_INPUTS': 13,
        'P05_NEXT_MISSING_INPUT': graph['P05_NEXT_MISSING_INPUT'],
        'P05_EXECUTION_READY': 'NO', 'E2_P05_READY': 'YES',
        'P05_EXECUTED': 'NO', 'P06_EXECUTED': 'NO', 'E2_END_EXECUTED': 'NO',
        'NEXT_PACKAGE': graph['NEXT_PACKAGE'], 'next_missing_input_resolved': False,
        'PROSPECTIVE_A03_EXECUTED': 'YES', 'CANONICAL_P04_MODIFIED': 'NO',
        'E2_P04_RESULT': 'PASS', 'P03_HISTORICAL_CORRESPONDENCE': 'UNPROVEN', 'N_REAL_SATISFIED': 'NO',
        'ADDITIONAL_AUTHORITY_REQUIRED': 'NO', 'NEW_AUTHORITY_ISSUED': 'NO',
        'NEW_DEFINITIONS_INSTALLED': 0, 'RUNTIME_MODIFIED': 'NO',
        'E1_ARTIFACTS_MODIFIED': 0, 'PRODUCTION_EFFECT': 'NO',
        'evidence': {name: d.pin(d.OUT / filename) for name, filename in [
            ('entry', 'entry-gate.json'), ('execution_driver', 'driver-seal.json'),
            ('primary_actual_execution', 'writer-main/writer-result.json'),
            ('occurrence_oracle', 'occurrence-oracle-comparison.json'), ('persistence', 'persistence.json'),
            ('cold_restore_replay', 'cold-restore-and-replay.json'),
            ('independent_reproduction_determinism', 'independent-reproduction-and-determinism.json'),
            ('negative_results', 'negative-results.json'), ('END_P05_mapping', 'P05-binding-rerun.json')]},
        'contract': d.pin(d.REPORT_PATH), 'reporting_driver_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'runtime_and_authoritative_inputs_changed': False,
        'full_END_original_ancestry_qualified': False,
        'FIRST_COUNTEREXAMPLE': None,
    }
    path = d.PLANS / 'DETERMINISTIC_PLANNER_V0_1_E2_P05_A03_PROSPECTIVE_OCCURRENCE_RESULT_1.json'
    d.write(path, report)
    print(json.dumps({'result': 'PASS', 'bundle_id': report['POST_A03_BUNDLE_ID'],
                      'occurrence_checks': len(checks), 'P05_bound': 10, 'next_input': report['P05_NEXT_MISSING_INPUT']}))


if __name__ == '__main__':
    main()
