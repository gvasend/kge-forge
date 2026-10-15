"""Independent final references/identity/results/preservation audit, read-only."""
import ast
import json
import re
import subprocess
from pathlib import Path
from contract import (ROOT, OUT, DOCS, PREFIX, PRIOR, HISTORICAL, FIELDS, TERMS,
    read, sha, ref, at, pins, save, equal, qid)
from oracle import normalize


def main():
    p = read(OUT / 'END-projection.json'); body = p['projection']
    mf = read(OUT / 'invocation-input-manifest.json')
    expected = read(OUT / 'expected-oracle.json')
    expected_manifest = read(OUT / 'expected-manifest-oracle.json')
    seal = read(OUT / 'oracle-seal.json')
    equal('complete projection equals independent seal', body, expected['expected_projection'])
    equal('complete manifest equals independent seal', mf['manifest'], expected_manifest['expected_manifest'])
    equal('exact projection identity', p['identity'], qid('qualification-PC02-END-projection-v1', body))
    equal('exact manifest identity', mf['identity'], qid('qualification-PC02-END-manifest-v1', mf['manifest']))
    equal('sealed projection identity match', p['identity'], seal['expected_projection_identity'])
    equal('sealed manifest identity match', mf['identity'], seal['expected_manifest_identity'])
    equal('process identity', body['process']['identity'], qid('qualification-PC02-END-process-v1', body['process']['process']))
    equal('three primary pinned sources', len(body['primary_sources']), 3)
    equal('complete native view membership', [x['view']['field'] for x in body['native_views']], list(FIELDS))
    for view in body['native_views']:
        equal('native source view qualification identity', view['identity'], qid('qualification-PC02-native-view-v1', view['view']))
        source = view['view']['source']
        values = normalize(at(read(ROOT / source['path']), source['pointer']))
        for index, member in enumerate(view['view']['members']):
            equal('native member immutable source value', member['native_value'], values[index])
            equal('source pointer resolves actual member', normalize(at(read(ROOT / source['path']), member['source_pointer'])), member['native_value'])
        equal('complete source member count', len(values), len(view['view']['members']))
    equal('original roles all explicitly bound', sorted(x['original_role'] for x in body['role_bindings']),
        ['ATTESTOR', 'DOSSIER', 'EXTERNAL_ROUTE', 'GRANT', 'ROOT_PROOF', 'SLOT_PROOF'])
    equal('concrete manifest inputs', len(mf['manifest']['inputs']), 36)
    equal('unique manifest input slots', len(set(x['INPUT_ID'] for x in mf['manifest']['inputs'])), 36)
    equal('independent oracle comparator-only', next(x for x in mf['manifest']['inputs'] if x['INPUT_ID'] == 'INDEPENDENT_ORACLE')['role'], 'COMPARISON_ONLY')
    preflight = read(OUT / 'preflight.json')
    equal('native full model validation', preflight['native_validation']['RESULT'], 'PASS')
    equal('nine independent interface terms', preflight['terms'], {key: 'PASS' for key in TERMS})
    equal('mutation barrier has no calls', preflight['native_mutating_calls'], [])
    equal('nine governed current/history versions', len(preflight['native_validation']['definition_currentness']), 9)
    equal('exact supported route distinction',
        [(x['support_current'], x['consumer_applicable_now']) for x in preflight['native_validation']['definition_currentness'] if x['type'] == 'EXTERNAL_RESOLUTION_CONTRACT'], [(True, False)])
    plan = read(OUT / 'negative-plan.json')
    negative = read(OUT / 'negative-results.json')
    equal('sealed negatives all covered', [x['name'] for x in plan['cases']], [x['name'] for x in negative['cases']])
    equal('negative count', negative['count'], 22)
    equal('all negative controls fail closed', all(x['RESULT'] == 'PASS' for x in negative['cases']), True)
    readers = [read(path) for path in sorted((OUT / 'readers').glob('*.json'))]
    equal('fresh reader count', len(readers), 36)
    for seed in ('0', '1', '7', '101'):
        for form in ('original', 'reversed', 'rotated'):
            equal('readers per seed and native presentation', len([x for x in readers if x['seed'] == seed and x['presentation'] == form]), 3)
    equal('all reader native/source/projection preflights', all(x['PC02_END_INTERFACE'] == 'PASS' and
        x['projection_identity'] == p['identity'] and x['manifest_identity'] == mf['identity'] and
        not x['native_mutating_calls'] and not x['ordered_event_ledger_permuted'] for x in readers), True)
    frontier = read(OUT / 'six-interface-frontier.json')
    old = read(PRIOR / 'six-interface-frontier.json')
    equal('prior PC01 record unchanged', frontier['interfaces'][0], old['interfaces'][0])
    equal('remaining four records unchanged', frontier['interfaces'][2:], old['interfaces'][2:])
    equal('new interface frontier exact', frontier['END_INTERFACES_BOUND'], 2)
    equal('next failure in authoritative order', frontier['NEXT_UNRESOLVED_INTERFACE'], old['interfaces'][2]['SOURCE'] + ' -> E2-END')
    report_path = DOCS / (PREFIX + 'E2_P05_PC02_END_BINDING_1.json')
    report = read(report_path)
    for field, value in {'RESULT': 'PASS', 'PC02_END_INTERFACE': 'PASS', 'PC01_END_INTERFACE': 'PASS',
        'PC01_BINDING_PATTERN_REUSABLE': 'YES', 'P05_STAGE_BINDINGS': '13/13', 'FOUR_SEMANTIC_BRIDGES': 'PASS',
        'AGGREGATE_N12': 'PASS', 'AGGREGATE_N13': 'PASS', 'END_INTERFACES_BOUND': 2, 'END_INTERFACE_COUNT': 6,
        'COMPOSITE_P05_END_QUALIFICATION': 'FAIL', 'P05_EXECUTION_READY': 'NO', 'P05_EXECUTED': 'NO', 'P06_EXECUTED': 'NO',
        'NATIVE_STATE_CHANGED': 'NO', 'RUNTIME_MODIFIED': 'NO', 'INSTALL_EVENTS': 0, 'NEW_AUTHORITIES': 0,
        'E1_ARTIFACTS_MODIFIED': 0, 'PRODUCTION_EFFECT': 'NO', 'N_REAL_SATISFIED': 'NO'}.items():
        equal('report ' + field, report[field], value)
    for field, value in HISTORICAL.items():
        equal('historical exclusion unchanged', report[field], value)
    equal('continuous original native lineage not claimed', report['CONTINUOUS_ORIGINAL_A01_A13_LINEAGE_PROVEN'], 'NO')
    correspondence = read(OUT / 'contract-correspondence.json')
    equal('PC02 root/slot source independence retained', all(correspondence['root_slot_independence'][key] for key in
        ('source_content_identities_differ', 'propositions_differ', 'origin_identities_differ', 'native_semantic_authority_identities_differ')), True)
    checked = set()
    for path in list(OUT.rglob('*.json')) + [report_path]:
        if path.name in ('baseline.json', 'verification.json'):
            continue
        for pin in pins(read(path)):
            source = ROOT / pin['path']
            equal('exact reference content', sha(source), pin['raw_sha256'])
            if pin.get('pointer') and source.suffix == '.json':
                at(read(source), pin['pointer'])
            checked.add((pin['path'], pin['raw_sha256'], pin.get('pointer', '')))
    for source in OUT.glob('*.py'):
        ast.parse(source.read_text(), str(source))
    for link in re.findall(r'\]\(([^)]+)\)', report_path.with_suffix('.md').read_text()):
        target = report_path.parent / re.sub(r':\d+$', '', link)
        equal('report link exists', target.is_file() or target == OUT / 'verification.json', True)
    baseline = read(OUT / 'baseline.json')['file_sha256']
    changed = [path for path, digest in baseline.items() if not (ROOT / path).is_file() or sha(ROOT / path) != digest]
    equal('entire prior workspace preserved', changed, [])
    check = subprocess.run(['git', 'diff', '--check'], cwd=str(ROOT), capture_output=True, text=True)
    equal('git diff check', check.returncode, 0)
    save('verification.json', {'RESULT': 'PASS', 'PC02_END_INTERFACE': 'PASS',
        'projection_identity': p['identity'], 'manifest_identity': mf['identity'],
        'process_identity': body['process']['identity'], 'source_reference_checks': len(checked),
        'independent_oracle_and_manifest_exact': True, 'native_model_validation': 'PASS',
        'native_semantic_view_count': len(FIELDS), 'negative_cases_passed': 22, 'fresh_reader_count': 36,
        'END_INTERFACES_BOUND': 2, 'END_INTERFACE_COUNT': 6,
        'NEXT_UNRESOLVED_INTERFACE': frontier['NEXT_UNRESOLVED_INTERFACE'],
        'PC01_record_and_remaining_four_records_unchanged': True, 'prior_files_unchanged': len(baseline),
        'E1_files_unchanged': sum(path.startswith('docs/experiments/E1/') for path in baseline),
        'runtime_files_unchanged': sum(path.startswith('adapter/planner/') for path in baseline),
        'NATIVE_STATE_CHANGED': 'NO', 'RUNTIME_MODIFIED': 'NO', 'INSTALL_EVENTS': 0, 'NEW_AUTHORITIES': 0,
        'P05_EXECUTED': 'NO', 'P06_EXECUTED': 'NO', 'P05_EXECUTION_READY': 'NO',
        'E1_ARTIFACTS_MODIFIED': 0, 'PRODUCTION_EFFECT': 'NO', 'git_diff_check': 'PASS',
        'reports': [ref(report_path), ref(report_path.with_suffix('.md'))],
        'harnesses': [ref(path) for path in sorted(OUT.glob('*.py'))]})
    print(json.dumps({'VERIFICATION': 'PASS', 'PC02_END_INTERFACE': 'PASS', 'interfaces_bound': '2/6',
        'next_interface': frontier['NEXT_UNRESOLVED_INTERFACE'], 'prior_files_preserved': len(baseline),
        'git_diff_check': 'PASS'}))


if __name__ == '__main__':
    main()
