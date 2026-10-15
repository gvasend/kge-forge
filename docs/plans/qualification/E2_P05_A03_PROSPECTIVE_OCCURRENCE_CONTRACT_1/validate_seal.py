"""Check the sealed contract without executing an A03 transition."""
import hashlib
import json
import re
import runpy
import subprocess
from pathlib import Path

from adapter.planner import codec as c, model as m, core

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
REPORT = ROOT / 'docs/plans/DETERMINISTIC_PLANNER_V0_1_E2_P05_A03_PROSPECTIVE_OCCURRENCE_CONTRACT_1.json'


def main():
    counts = {}
    protected = []
    for module, name in [(core, 'apply_result'), (core, 'apply_event'), (core, '_inventory'),
                         (core, 'recompute'), (c, 'apply_event'), (c, 'record_result'),
                         (c, 'append_event'), (c, 'commit_event'), (c, 'save_bundle'),
                         (c, 'restore')]:
        key = module.__name__ + '.' + name
        counts[key] = 0
        original = getattr(module, name)

        def forbidden(*args, _key=key, **kwargs):
            counts[_key] += 1
            raise AssertionError('Positive operation forbidden during seal audit: ' + _key)

        protected.append((module, name, original))
        setattr(module, name, forbidden)
    original_replay = c._replay
    empty_replay_count = [0]

    def empty_replay_only(bundle):
        assert not bundle.events, 'No positive event replay permitted in contract package'
        empty_replay_count[0] += 1
        return original_replay(bundle)

    c._replay = empty_replay_only
    try:
        sealer = runpy.run_path(str(OUT / 'seal_contract.py'), run_name='seal_metadata_audit')
        sealer['main']()
    finally:
        c._replay = original_replay
        for module, name, original in protected:
            setattr(module, name, original)
    assert not any(counts.values())
    report = json.loads(REPORT.read_bytes())
    seal = json.loads((OUT / 'seal.json').read_bytes())
    start = c._unwire(json.loads((OUT / 'inputs/starting-bundle.json').read_bytes())['bundle'])
    expected = json.loads((OUT / 'oracles/expected-events.json').read_bytes())
    results = json.loads((OUT / 'oracles/expected-results.json').read_bytes())
    inputs = json.loads((OUT / 'input-inventory.json').read_bytes())
    mapping = json.loads((OUT / 'END-acceptance-mapping.json').read_bytes())
    assurance = json.loads((OUT / 'assurance-mapping.json').read_bytes())
    capture = json.loads((OUT / 'authorization-capture.json').read_bytes())
    negatives = json.loads((OUT / 'negative-contract.json').read_bytes())
    prior = json.loads((ROOT / 'docs/plans/DETERMINISTIC_PLANNER_V0_1_E2_P05_END_INPUT_BINDING_1.json').read_bytes())
    pins, pointers, cache = set(), set(), {}

    def verify_pin(pin, pointer=None):
        name, expected_hash = pin['path'], pin['raw_sha256']
        if name not in cache:
            cache[name] = (ROOT / name).read_bytes()
        assert hashlib.sha256(cache[name]).hexdigest() == expected_hash, name
        pins.add((name, expected_hash))
        pointer = pin.get('pointer', '') if pointer is None else pointer
        if pointer:
            obj = json.loads(cache[name])
            for key in pointer[1:].split('/'):
                key = key.replace('~1', '/').replace('~0', '~')
                obj = obj[int(key)] if isinstance(obj, list) else obj[key]
            pointers.add((name, pointer))

    documents = list(OUT.rglob('*.json')) + [REPORT]
    for path in documents:
        if path.name in ('baseline.json', 'metadata-validation.json', 'preservation.json'):
            continue
        value = json.loads(path.read_bytes())
        queue = [value]
        while queue:
            obj = queue.pop()
            if isinstance(obj, dict):
                if 'path' in obj and 'raw_sha256' in obj:
                    verify_pin(obj)
                if isinstance(obj.get('source'), dict) and 'raw_sha256' in obj['source'] and isinstance(obj.get('pointer'), str):
                    verify_pin(obj['source'], obj['pointer'])
                queue.extend(obj.values())
            elif isinstance(obj, list):
                queue.extend(obj)
    assert hashlib.sha256((OUT / 'seal_contract.py').read_bytes()).hexdigest() == seal['sealing_procedure_sha256']
    for name, sha in inputs['runtime_and_native_contracts'].items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == sha
    assert start.events == () and start.current == start.initial and not start.current.knowledge
    assert not start.current.entities and not start.current.installed_definitions
    assert start.current.context.lineage == 'E2-P05-A03-PROSPECTIVE-QUALIFICATION-1'
    assert all(row.state is m.ActionState.ACTION_ELIGIBLE for row in start.current.statuses)
    assert all(row.authority is None and row.effect is m.EffectClass.NON_EFFECTING for row in start.current.actions if row.id.value in ('E2-CHECK', 'E2-COLLECT'))
    start_id = c.snapshot_id(start.current)
    sid_text = start_id.namespace + ':' + start_id.sha256
    assert report['PROSPECTIVE_START']['START_STATE_ID'] == sid_text
    assert report['PROSPECTIVE_START']['START_BUNDLE_ID'].endswith(hashlib.sha256((OUT / 'inputs/starting-bundle.json').read_bytes()).hexdigest())
    assert report['PROSPECTIVE_START']['LEDGER_ROOT'] is None
    assert report['PROSPECTIVE_START']['APPEND_HEAD'] is None
    assert report['PROSPECTIVE_START']['PARENT_EVENT_ID'] is None
    assert len(expected['event_oracles']) == len(results['result_oracles']) == 2
    assert expected['occurred_event_count'] == 0 and expected['not_execution_input'] is True
    assert results['not_execution_input'] is True
    previous = None
    for index, row in enumerate(expected['event_oracles'], start=1):
        event = c._unwire(row['expected_native_wire'])
        # Pure hash consistency only: no replay/admission of oracle descriptors.
        assert event.identity == c._event_identity(event.sequence, event.parent_snapshot, event.parent_event, event.result, event.after_snapshot)
        assert event.sequence == index and event.parent_event == previous
        assert row['role'] == 'EXPECTED_ORACLE_ONLY_NOT_OCCURRED'
        assert event.result.result is m.ActionResult.PASS and len(event.result.knowledge) == 1
        assert event.result.action.value == ['E2-CHECK', 'E2-COLLECT'][index-1]
        assert event.result.expected_snapshot == event.parent_snapshot
        if index == 1:
            assert event.parent_snapshot == start_id
        else:
            assert row['PRE_STATE_ID'] == expected['event_oracles'][index-2]['POST_STATE_ID']
        previous = event.identity
    assert negatives['count'] == len(negatives['cases']) == 24
    assert all(row['qualification_status'] == 'SEALED_NOT_EXECUTED' for row in negatives['cases'])
    assert assurance['N12_mapping']['mapping_preserved'] == 'YES'
    assert assurance['N13_mapping']['mapping_preserved'] == 'YES'
    assert assurance['N12_mapping']['negative_execution'] == assurance['N13_mapping']['negative_execution'] == 'NOT_EXECUTED'
    assert mapping['original_evidence']['status'] == 'UNPROVEN'
    assert mapping['original_evidence']['native_event_ids'] is None
    assert mapping['historical_identity_mapping'].startswith('NONE')
    assert mapping['replacement_expected_native_event_ids'] == [row['EXPECTED_EVENT_ID'] for row in expected['event_oracles']]
    assert prior['A01_A13_BOUND_COUNT'] == report['P05_BOUND_STAGE_INPUTS'] == 9
    assert report['P05_EXECUTION_READY'] == prior['P05_EXECUTION_READY'] == 'NO'
    assert report['PROSPECTIVE_A03_EXECUTED'] == report['P05_EXECUTED'] == report['P06_EXECUTED'] == 'NO'
    assert report['PROSPECTIVE_A03_EXECUTION_READY'] == 'YES'
    assert capture['native_authorities_issued'] == 0
    assert capture['native_operating_authority_required'] is False
    assert capture['historical_or_P03_authorities_reused'] is False
    assert not seal['TBD_terms'] and seal['execution_started'] is False
    assert seal['positive_transition_functions_called'] == []
    native_source_paths = {row.path for row in start.sources}
    assert not any('/oracles/' in name for name in native_source_paths)
    assert not any((name.endswith('/END-acceptance-mapping.json') or name.endswith('/assurance-mapping.json')) for name in native_source_paths)
    md = REPORT.with_suffix('.md')
    links = []
    for link in re.findall(r'\[[^\]]+\]\(([^)]+)\)', md.read_text()):
        if link.startswith(('http:', 'https:', '#')):
            continue
        target = (md.parent / re.sub(r':\d+$', '', link)).resolve()
        assert target.exists(), link
        links.append(link)
    diff = subprocess.run(['git', 'diff', '--check'], cwd=ROOT, capture_output=True, text=True)
    assert diff.returncode == 0, diff.stdout + diff.stderr
    result = {
        'result': 'PASS', 'kind': 'Static sealing and no-execution instrumentation only',
        'hash_seed': __import__('os').environ.get('PYTHONHASHSEED'),
        'native_empty_bundle_replay_validation_calls': empty_replay_count[0],
        'forbidden_positive_operation_calls': counts,
        'actual_events_admitted': 0, 'native_authorities_issued': 0,
        'file_hash_pins_checked': len(pins), 'JSON_pointers_checked': len(pointers),
        'Markdown_links_checked': len(links), 'native_runtime_files_checked': len(inputs['runtime_and_native_contracts']),
        'start_and_expected_hashes_exact': True, 'anticipated_event_descriptors_are_not_actual_events': True,
        'N12_N13_mappings_sealed_not_executed': True, 'END_historical_identity_separate': True,
        'P05_stage_binding_count': 9, 'oracle_files_excluded_from_execution_inputs': True,
        'git_diff_check': 'PASS',
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
