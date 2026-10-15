"""Final source/oracle/identity/frontier/preservation audit; no native execution."""
import ast
import json
import re
import subprocess
from common_v2 import (ROOT, OUT, BASE_OUT, DOCS, Q, PREFIX, PRIOR, HISTORICAL,
    TERMS, read, sha, ref, at, pins, qid, save, equal)
from oracle_v2 import normalize


def main():
    p = read(OUT / 'END-projection.json'); body = p['projection']
    mf = read(OUT / 'invocation-input-manifest.json')
    seal = read(OUT / 'oracle-seal.json')
    expected = read(OUT / 'expected-oracle.json')
    expected_manifest = read(OUT / 'expected-manifest-oracle.json')
    equal('whole independently expected projection', body, expected['expected_projection'])
    equal('whole independently expected manifest', mf['manifest'], expected_manifest['expected_manifest'])
    equal('qualification projection identity', p['identity'], qid('qualification-PC03-END-projection-v1', body))
    equal('qualification manifest identity', mf['identity'], qid('qualification-PC03-END-manifest-v1', mf['manifest']))
    equal('process v2 comparison identity', body['process']['identity'], qid('qualification-PC03-END-process-v2', body['process']['definition']))
    equal('seal projection ID', p['identity'], seal['expected_projection_identity'])
    equal('seal manifest ID', mf['identity'], seal['expected_manifest_identity'])
    equal('exact model roles', len(body['models']), 16)
    for model in body['models']:
        spec = model['selected_model']; raw = at(read(ROOT / spec['source']['path']), spec['source']['pointer'])
        raw_state = normalize(raw['bundle']['current'] if spec['type'] == 'PersistenceBundle' else raw)
        equal('whole source state canonical comparison', model['full_state_comparison_identity'], qid('qualification-PC03-full-state-view-v1', raw_state))
        equal('exact native Snapshot comparison domain', model['native_snapshot_identity'], spec['native_snapshot'])
        equal('source context exact', model['semantic_summary']['context'], spec['context'])
        if spec['type'] == 'PersistenceBundle':
            equal('native Bundle ID vs exact raw source bytes', spec['native_bundle'], 'planner-bundle-v1:' + sha(ROOT / spec['source']['path']))
            equal('no event omitted from ordered input view', len(model['ordered_event_trace']), len(raw['bundle']['events']))
            equal('ordered actual event membership', [x['event_id'] for x in model['ordered_event_trace']],
                [e['identity']['namespace'] + ':' + e['identity']['sha256'] for e in raw['bundle']['events']])
    equal('original PC03 phases remain ordered', [x['phase'] for x in body['original_PC03_fixture']['phase_oracle']],
        ['INITIAL', 'PRE_EXTERNAL', 'EXTERNAL_CHECKPOINT', 'COLD_RESTORED', 'EVIDENCE_RECEIVED', 'EVIDENCE_VALIDATED', 'REENTRY_ELIGIBLE', 'POST_REENTRY'])
    equal('independent phase comparisons count', len(body['independent_boundary_bindings']), 8)
    equal('current post-A12 keeps sealed PLAN_DEFECT', body['independent_boundary_bindings'][0]['expected']['control'], 'PLAN_DEFECT')
    equal('original scaffold remains original', body['original_PC03_fixture']['phase_oracle'][-1]['control'], 'RUNNABLE')
    equal('exact input manifest count', len(mf['manifest']['inputs']), 91)
    equal('no duplicate manifest input ID', len(set(x['INPUT_ID'] for x in mf['manifest']['inputs'])), 91)
    for row in mf['manifest']['inputs']:
        if row['INPUT_ID'].startswith(('ORACLE_', 'BOUNDARY_', 'MUTATION_CONTRACT_')) or row['INPUT_ID'] == 'INDEPENDENT_BINDING_ORACLE':
            equal('oracle never becomes a Planner operand', row['input_role'], 'COMPARISON_ONLY')
    equal('explicit process edges', len(mf['manifest']['process_edges']), 3)
    equal('native mutating process operations absent', mf['manifest']['native_mutating_operations'], [])
    equal('hidden writer memory prohibited', mf['manifest']['hidden_process_memory'], False)
    preflight = read(OUT / 'preflight.json')
    equal('all nine interface terms pass', preflight['terms'], {key: 'PASS' for key in TERMS})
    equal('native structural and source checks', preflight['native_validation']['RESULT'], 'PASS')
    equal('all selected models validated', preflight['native_validation']['model_count'], 16)
    equal('all independent boundary assertions pass', [x['RESULT'] for x in preflight['native_validation']['independent_boundary_checks']], ['PASS'] * 8)
    equal('no actual native transaction/replay/commit', preflight['native_mutating_calls'], [])
    plan = read(OUT / 'negative-plan.json'); negative = read(OUT / 'negative-results.json')
    equal('exact sealed binding negatives run', [x['name'] for x in plan['cases']], [x['name'] for x in negative['cases']])
    equal('negative count', negative['count'], 24)
    equal('all fixed controls fail closed', all(x['RESULT'] == 'PASS' for x in negative['cases']), True)
    ordered = next(x for x in negative['cases'] if x['name'] == 'ordered_ancestry_permutation')
    equal('native ordered ledger check independently rejects', ordered['native_ordered_ledger_rejection'], 'native ordered ledger sequence')
    readers = [read(path) for path in (OUT / 'readers').glob('*.json')]
    equal('36 independent reader processes', len(readers), 36)
    for seed in ('0', '1', '7', '101'):
        for form in ('original', 'reversed', 'rotated'):
            equal('three readers per native presentation/seed', len([x for x in readers if x['seed'] == seed and x['presentation'] == form]), 3)
    equal('reader semantics and source identities exact', all(x['PC03_END_INTERFACE'] == 'PASS' and
        x['projection_identity'] == p['identity'] and x['manifest_identity'] == mf['identity'] and
        not x['native_mutating_calls'] and not x['writer_memory_available'] and not x['ordered_events_permuted'] for x in readers), True)
    frontier = read(OUT / 'six-interface-frontier.json'); previous = read(PRIOR / 'six-interface-frontier.json')
    equal('PC01/PC02 records unchanged', frontier['interfaces'][:2], previous['interfaces'][:2])
    equal('last three records unchanged', frontier['interfaces'][3:], previous['interfaces'][3:])
    equal('interface frontier advances once', frontier['END_INTERFACES_BOUND'], 3)
    equal('next interface in original order', frontier['NEXT_UNRESOLVED_INTERFACE'], previous['interfaces'][3]['SOURCE'] + ' -> E2-END')
    assessment = read(OUT / 'remaining-pattern-classification.json')
    equal('informational classifications only', all(x['no_binding_created'] and x['informational_only'] for x in assessment['classifications'].values()), True)
    baseline = read(BASE_OUT / 'baseline.json')['file_sha256']
    changed = [name for name, digest in baseline.items() if not (ROOT / name).is_file() or sha(ROOT / name) != digest]
    equal('all pre-existing native/source/oracle/runtime artifacts unchanged', changed, [])
    diagnostic = read(BASE_OUT / 'attempt-1-diagnostic.json')
    for name, digest in diagnostic['retained_attempt_files'].items():
        equal('original new-checker attempt retained verbatim', sha(BASE_OUT / name), digest)
    report_path = DOCS / (PREFIX + 'E2_P05_PC03_END_BINDING_1.json'); report = read(report_path)
    for key, value in {'RESULT': 'PASS', 'PC03_END_INTERFACE': 'PASS', 'PC01_END_INTERFACE': 'PASS', 'PC02_END_INTERFACE': 'PASS',
        'END_INTERFACES_BOUND': 3, 'END_INTERFACE_COUNT': 6, 'P05_STAGE_BINDINGS': '13/13',
        'FOUR_SEMANTIC_BRIDGES': 'PASS', 'AGGREGATE_N12': 'PASS', 'AGGREGATE_N13': 'PASS',
        'COMPOSITE_P05_END_QUALIFICATION': 'FAIL', 'P05_EXECUTION_READY': 'NO', 'P05_EXECUTED': 'NO', 'P06_EXECUTED': 'NO',
        'NATIVE_STATE_CHANGED': 'NO', 'RUNTIME_MODIFIED': 'NO', 'INSTALL_EVENTS': 0, 'NEW_AUTHORITIES': 0,
        'E1_ARTIFACTS_MODIFIED': 0, 'PRODUCTION_EFFECT': 'NO', 'N_REAL_SATISFIED': 'NO',
        'CONTINUOUS_ORIGINAL_A01_A13_LINEAGE_PROVEN': 'NO'}.items():
        equal('final report ' + key, report[key], value)
    for key, value in HISTORICAL.items(): equal('historical exclusion', report[key], value)
    checked = set()
    for path in list(BASE_OUT.rglob('*.json')) + [report_path]:
        if path.name in ('baseline.json', 'verification.json'): continue
        for pin in pins(read(path)):
            source = ROOT / pin['path']
            equal('exact pin bytes', sha(source), pin['raw_sha256'])
            if pin.get('pointer') and source.suffix == '.json': at(read(source), pin['pointer'])
            checked.add((pin['path'], pin.get('pointer', ''), pin['raw_sha256']))
    for path in BASE_OUT.glob('*.py'): ast.parse(path.read_text(), str(path))
    for link in re.findall(r'\]\(([^)]+)\)', report_path.with_suffix('.md').read_text()):
        target = report_path.parent / re.sub(r':\d+$', '', link)
        equal('report evidence link', target.is_file() or target == OUT / 'verification.json', True)
    check = subprocess.run(['git', 'diff', '--check'], cwd=str(ROOT), capture_output=True, text=True)
    equal('git diff check', check.returncode, 0)
    save('verification.json', {'RESULT': 'PASS', 'PC03_END_INTERFACE': 'PASS',
        'projection_identity': p['identity'], 'manifest_identity': mf['identity'], 'process_identity': body['process']['identity'],
        'source_reference_checks': len(checked), 'native_models_validated': 16, 'independent_boundary_comparisons': 8,
        'sealed_binding_negatives_passed': 24, 'fresh_readers': 36, 'ordered_ledger_permutation_rejected_natively': True,
        'END_INTERFACES_BOUND': 3, 'END_INTERFACE_COUNT': 6, 'NEXT_UNRESOLVED_INTERFACE': frontier['NEXT_UNRESOLVED_INTERFACE'],
        'previous_two_and_remaining_three_interface_records_unchanged': True,
        'prior_files_unchanged': len(baseline), 'runtime_files_unchanged': sum(p.startswith('adapter/planner/') for p in baseline),
        'E1_files_unchanged': sum(p.startswith('docs/experiments/E1/') for p in baseline),
        'NATIVE_STATE_CHANGED': 'NO', 'INSTALL_EVENTS': 0, 'NEW_AUTHORITIES': 0,
        'RUNTIME_MODIFIED': 'NO', 'P05_EXECUTED': 'NO', 'P06_EXECUTED': 'NO', 'P05_EXECUTION_READY': 'NO',
        'E1_ARTIFACTS_MODIFIED': 0, 'PRODUCTION_EFFECT': 'NO', 'git_diff_check': 'PASS',
        'checker_attempt_1_and_v2_seals_preserved': True,
        'reports': [ref(report_path), ref(report_path.with_suffix('.md'))],
        'harnesses': [ref(p) for p in sorted(BASE_OUT.glob('*.py'))]})
    print(json.dumps({'VERIFICATION': 'PASS', 'PC03_END_INTERFACE': 'PASS', 'interfaces': '3/6',
        'next_interface': frontier['NEXT_UNRESOLVED_INTERFACE'], 'prior_files_preserved': len(baseline), 'git_diff_check': 'PASS'}))


if __name__ == '__main__':
    main()
