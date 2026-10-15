"""Audit retained bytes and metadata consistency without loading native operations."""
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
REPORT = ROOT / 'docs/plans/DETERMINISTIC_PLANNER_V0_1_E2_P05_A05_ALTERNATE_NATIVE_EVIDENCE_RESULT_1.json'


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()


def main():
    baseline = json.loads((OUT / 'baseline.json').read_bytes())['files']
    changed, missing = [], []
    for path, expected in baseline.items():
        source = ROOT / path
        if not source.is_file():
            missing.append(path)
        elif hashlib.sha256(source.read_bytes()).hexdigest() != expected:
            changed.append(path)
    assert not changed and not missing, (changed, missing)
    report = json.loads(REPORT.read_bytes())
    mapping = json.loads((OUT / 'END-acceptance-mapping.json').read_bytes())
    graph = json.loads((OUT / 'P05-binding-rerun.json').read_bytes())
    prior = json.loads((ROOT / graph['binding_source']['path']).read_bytes())
    contract = json.loads((OUT / 'mapping-contract.json').read_bytes())
    rows = graph['stage_bindings']
    assert len(rows) == 13 and sum(r['binding_status'] == 'BOUND' for r in rows) == 12
    assert graph['P05_NEXT_MISSING_INPUT'] == 'E2-A06.request_wait_event_trace'
    assert graph['additional_unresolved_END_gate'] == prior['additional_unresolved_END_gate']
    assert rows[5] == prior['stage_bindings'][5]
    for index in range(13):
        if index != 4:
            assert rows[index] == prior['stage_bindings'][index]
    assert graph['P05_EXECUTION_READY'] == report['P05_EXECUTION_READY'] == 'NO'
    assert report['E2_A05_RECORDED_DECISION_EVENT_ANCESTRY'] == 'PASS'
    assert report['ALTERNATE_EVENT_ID'] == mapping['native_event_id']
    assert report['N12_MAPPING'] == report['N13_MAPPING'] == 'PASS'
    assert report['E1_ARTIFACTS_MODIFIED'] == 0
    for key in ('NEW_A05_OCCURRENCE_CREATED', 'NEW_HUMAN_CHOICE_CREATED',
                'NEW_NATIVE_GRANT_ISSUED', 'P03_EVENT_IS_ORIGINAL_A05_EVENT',
                'HISTORICAL_RECONSTRUCTION', 'P05_EXECUTED', 'P06_EXECUTED',
                'RUNTIME_MODIFIED', 'PRODUCTION_EFFECT', 'N_REAL_SATISFIED'):
        assert report[key] == 'NO', key
    for key in ('ORIGINAL_A03_HISTORICAL_OCCURRENCE', 'ORIGINAL_A04_HISTORICAL_ANCESTRY',
                'ORIGINAL_A05_HISTORICAL_ANCESTRY', 'P03_HISTORICAL_CORRESPONDENCE'):
        assert report[key] == 'UNPROVEN', key
    for key in ('N12', 'N13'):
        data = mapping[key + '_MAPPING']
        assert data['result'] == 'PASS' and all(t['pass'] for t in data['terms'])
        assert [t['term'] for t in data['terms']] == contract[key + '_terms']
    assert all(r['classification'] in ('EXACT_NATIVE_MATCH', 'SEMANTICALLY_EQUIVALENT_UNDER_AUTHORIZED_SCOPE')
               for r in mapping['semantic_correspondence'] if r['required_in_local_mapping'])
    expected_comparison = 'qualification-a05-alternate-mapping-v1:' + hashlib.sha256(canonical(mapping)).hexdigest()
    assert report['DETERMINISM']['mapping_comparison_identity'] == expected_comparison
    fresh = json.loads((OUT / 'fresh-reader-determinism.json').read_bytes())
    assert fresh['reader_count'] == 12
    assert {r['hash_seed'] for r in fresh['readers']} == {0, 1, 7, 101}
    for row in fresh['readers']:
        reader = json.loads((ROOT / row['evidence']['path']).read_bytes())
        assert reader['mapping'] == mapping and reader['mapping_comparison_identity'] == expected_comparison
        assert not reader['barred_calls'] and reader['reader']['native_operation_or_replay_calls'] == 0
    negatives = json.loads((OUT / 'negative-results.json').read_bytes())
    assert negatives['result'] == 'PASS' and negatives['passed'] == negatives['control_count'] == 26
    assert all(r['actual_rejection'] == r['expected_rejection'] for r in negatives['controls'])
    checked_pins = {}
    def walk(value):
        if isinstance(value, dict):
            if 'path' in value and 'raw_sha256' in value:
                path = ROOT / value['path']
                assert path.is_file(), value['path']
                assert hashlib.sha256(path.read_bytes()).hexdigest() == value['raw_sha256'], value['path']
                if value.get('pointer') and path.suffix == '.json':
                    selected = json.loads(path.read_bytes())
                    for part in value['pointer'].lstrip('/').split('/'):
                        part = part.replace('~1', '/').replace('~0', '~')
                        selected = selected[int(part)] if isinstance(selected, list) else selected[part]
                checked_pins[value['path']] = value['raw_sha256']
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)
    for path in OUT.glob('*.json'):
        if path.name not in ('baseline.json', 'verification.json'):
            walk(json.loads(path.read_bytes()))
    walk(report)
    source_count = len(list(OUT.glob('*.py')))
    for path in OUT.glob('*.py'):
        ast.parse(path.read_text(), filename=str(path))
    markdown = REPORT.with_suffix('.md')
    link_count = 0
    for target in re.findall(r'\]\(([^)]+)\)', markdown.read_text()):
        path = target.split(':')[0]
        resolved = markdown.parent / path
        # Verification is the only forward reference, produced below.
        assert resolved.is_file() or resolved == OUT / 'verification.json', target
        link_count += 1
    whitespace = []
    for path in list(OUT.glob('*.py')) + list(OUT.glob('*.json')) + [REPORT, markdown]:
        for number, line in enumerate(path.read_text().splitlines(), 1):
            if line.rstrip() != line:
                whitespace.append((str(path.relative_to(ROOT)), number))
    assert not whitespace, whitespace
    diff = subprocess.run(['git', 'diff', '--check'], cwd=str(ROOT), capture_output=True, text=True)
    assert diff.returncode == 0, diff.stdout + diff.stderr
    result = {
        'schema': 'A05-ALTERNATE-PRESERVATION-VERIFICATION-1', 'result': 'PASS',
        'baseline_files_checked': len(baseline), 'changed_baseline_files': changed,
        'missing_baseline_files': missing,
        'native_planner_files_checked': sum(p.startswith('adapter/planner/') for p in baseline),
        'adapter_files_checked': sum(p.startswith('adapter/') for p in baseline),
        'frozen_E1_files_checked': sum(p.startswith('docs/experiments/E1/') for p in baseline),
        'E1_ARTIFACTS_MODIFIED': 0, 'RUNTIME_MODIFIED': 'NO', 'PRODUCTION_EFFECT': 'NO',
        'new_native_events': 0, 'new_native_grants': 0, 'new_human_choices': 0,
        'native_operations_or_replay': 0,
        'scope_seal_and_native_source_references': 'PASS', 'checked_distinct_hash_pins': len(checked_pins),
        'JSON_native_pointers': 'PASS', 'markdown_links_checked': link_count,
        'own_Python_syntax_checked': source_count, 'new_artifact_whitespace': 'PASS',
        'git_diff_check': {'result': 'PASS', 'exit_code': diff.returncode,
                           'stdout': diff.stdout, 'stderr': diff.stderr},
        'P05_binding_only_A05_changed': True, 'P05_BOUND_STAGE_INPUTS': 12,
        'P05_EXECUTION_READY': 'NO', 'P05_EXECUTED': 'NO', 'P06_EXECUTED': 'NO',
        'original_prefix_and_A06_limitations_preserved': True,
        'qualification_comparison_identity': expected_comparison,
        'all_existing_file_immutability_domain': 'Compared to the baseline taken before this package; inherited workspace changes preserved',
        'report': {'path': str(REPORT.relative_to(ROOT)), 'raw_sha256': hashlib.sha256(REPORT.read_bytes()).hexdigest()},
        'markdown_report': {'path': str(markdown.relative_to(ROOT)), 'raw_sha256': hashlib.sha256(markdown.read_bytes()).hexdigest()},
        'verification_code': {'path': str(Path(__file__).resolve().relative_to(ROOT)),
                              'raw_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
        'binding_report_code': {'path': str((OUT / 'record_binding_and_report.py').relative_to(ROOT)),
                                'raw_sha256': hashlib.sha256((OUT / 'record_binding_and_report.py').read_bytes()).hexdigest()}}
    (OUT / 'verification.json').write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
    print(json.dumps({'verification': 'PASS', 'unchanged_baseline_files': len(baseline),
                      'checked_pins': len(checked_pins), 'git_diff_check': 'PASS'}))


if __name__ == '__main__':
    main()
