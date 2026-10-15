"""Read-only fresh-reader and mapping-rejection qualification; no native replay."""
import copy
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

import qualify_mapping as q

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]


def save(name, value):
    (OUT / name).write_text(json.dumps(value, sort_keys=True, indent=2) + '\n')


def pin(path):
    return {'path': str(path.relative_to(ROOT)),
            'raw_sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def invoke(task):
    seed, mode, invocation = task
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONPATH='.',
                       PYTHONHASHSEED=str(seed))
    process = subprocess.run([sys.executable, str(OUT / 'qualify_mapping.py'), mode],
                             cwd=str(ROOT), env=environment, capture_output=True,
                             text=True, timeout=60)
    return task, process


def main():
    contract = json.loads((OUT / 'mapping-contract.json').read_bytes())
    q.authenticate(contract)
    primary = json.loads((OUT / 'primary-reader.json').read_bytes())
    assert primary['result'] == 'PASS' and primary['barred_calls'] == []
    code_pins = [pin(OUT / name) for name in
                 ('seal_mapping.py', 'qualify_mapping.py', 'run_qualification.py')]
    save('qualification-code-pins.json', {'schema': 'A05-ALTERNATE-QUALIFICATION-CODE-PINS-1',
         'pins': code_pins, 'native_runtime_changes': False})
    tasks = []
    for seed in contract['fresh_readers']['seeds']:
        for mode in contract['fresh_readers']['modes']:
            tasks.append((seed, mode, len(tasks) + 1))
    with ThreadPoolExecutor(max_workers=3) as executor:
        readers = list(executor.map(invoke, tasks))
    rows = []
    for (seed, mode, invocation), process in readers:
        name = 'reader-{:02d}-seed-{}-{}.json'.format(invocation, seed, mode)
        if process.returncode != 0:
            save('reader-failure.json', {'seed': seed, 'mode': mode, 'exit_code': process.returncode,
                                        'stderr': process.stderr, 'stdout': process.stdout})
            raise AssertionError('Fresh reader failed: ' + name)
        result = json.loads(process.stdout)
        save(name, result)
        assert result['result'] == 'PASS'
        assert result['mapping'] == primary['mapping']
        assert result['mapping_comparison_identity'] == primary['mapping_comparison_identity']
        assert result['barred_calls'] == []
        assert result['reader']['native_operation_or_replay_calls'] == 0
        rows.append({'invocation': invocation, 'hash_seed': seed, 'presentation_mode': mode,
                     'process_pid_in_reader_namespace': result['reader']['pid'],
                     'exit_code': process.returncode, 'status': 'PASS', 'evidence': pin(OUT / name),
                     'mapping_comparison_identity': result['mapping_comparison_identity'],
                     'native_event_and_source_identities_exact': True,
                     'native_events_written': 0, 'native_operation_or_replay_calls': 0})
    save('fresh-reader-determinism.json', {'schema': 'A05-ALTERNATE-FRESH-READER-DETERMINISM-1',
         'result': 'PASS', 'readers': rows, 'reader_count': len(rows),
         'hash_seeds': contract['fresh_readers']['seeds'],
         'presentation_modes': contract['fresh_readers']['modes'],
         'ordered_events_history_and_policy_rules_permuted': False,
         'independence': 'Each invocation is a new interpreter with no retained writer memory. Namespace PID reuse does not identify a shared process.',
         'cold_decode_and_native_source_checks': 'PASS',
         'new_native_history_or_decision_replay': False,
         'comparison_identity': primary['mapping_comparison_identity']})
    plan = json.loads((OUT / 'negative-plan.json').read_bytes())
    results = []
    for control in plan['controls']:
        proposed = copy.deepcopy(contract['expected_proposal'])
        parts = control['mutation_path'].split('/')
        destination = proposed
        for part in parts[:-1]:
            destination = destination[part]
        destination[parts[-1]] = copy.deepcopy(control['value'])
        try:
            q.qualify(proposed, contract)
        except q.MappingRejected as exc:
            actual = str(exc)
        else:
            actual = 'INCORRECTLY_ACCEPTED'
        row = dict(control, actual_rejection=actual,
                   status='PASS' if actual == control['expected_rejection'] else 'FAIL',
                   native_objects_modified=0, native_events_created=0)
        results.append(row)
    save('negative-results.json', {'schema': 'A05-ALTERNATE-NEGATIVE-RESULTS-1',
         'domain': plan['domain'], 'plan': pin(OUT / 'negative-plan.json'),
         'result': 'PASS' if all(x['status'] == 'PASS' for x in results) else 'FAIL',
         'control_count': len(results), 'passed': sum(x['status'] == 'PASS' for x in results),
         'controls': results, 'native_execution_tests': False,
         'isolated_fixture': 'In-memory copy of qualification mapping proposal; pinned native witness untouched'})
    assert all(x['status'] == 'PASS' for x in results)
    assert not q.BARRED
    for source in code_pins:
        q.load_pin_bytes(source)
    q.authenticate(contract)
    save('END-acceptance-mapping.json', primary['mapping'])
    save('N12-mapping.json', dict(primary['mapping']['N12_MAPPING'],
         domain='A05 alternate native occurrence assurance only; no complete N12 suite executed',
         expected_terms=contract['N12_terms'], source=pin(OUT / 'END-acceptance-mapping.json')))
    save('N13-mapping.json', dict(primary['mapping']['N13_MAPPING'],
         domain='A05 alternate native result/declaration assurance only; evaluated independently of N12',
         expected_terms=contract['N13_terms'], source=pin(OUT / 'END-acceptance-mapping.json')))
    save('qualification-summary.json', {'schema': 'A05-ALTERNATE-QUALIFICATION-SUMMARY-1',
         'result': 'PASS', 'scope_authentication': 'PASS', 'native_ancestry': 'PASS',
         'RecordedDecision_binding': 'PASS', 'semantic_correspondence': 'PASS',
         'END_mapping': 'PASS_FOR_A05_ONLY', 'N12_mapping': 'PASS', 'N13_mapping': 'PASS',
         'negatives': {'passed': len(results), 'total': len(results)},
         'fresh_readers': len(rows), 'determinism': 'PASS',
         'mapping_comparison_identity': primary['mapping_comparison_identity'],
         'native_operations_or_replay': 0, 'native_events_created': 0,
         'human_choices_created': 0, 'native_grants_issued': 0, 'barred_calls': q.BARRED,
         'original_A05_ancestry': 'UNPROVEN', 'original_full_END_ancestry': 'UNRESOLVED',
         'A06_gap_closed': False,
         'evidence': {name: pin(OUT / name) for name in
                      ('primary-reader.json', 'authorization-authentication.json',
                       'END-acceptance-mapping.json', 'N12-mapping.json', 'N13-mapping.json',
                       'fresh-reader-determinism.json', 'negative-results.json', 'qualification-code-pins.json')}})
    print(json.dumps({'qualification': 'PASS', 'fresh_readers': len(rows),
                      'negative_controls': len(results), 'native_events_created': 0}))


if __name__ == '__main__':
    main()
