"""Independent final document/native-reference/decision integrity verification."""
import ast
import hashlib
import json
import re
import subprocess

from reconcile import ROOT, OUT, DOCS, PREFIX, CURRENT, CALLS, c, read, ref, save, pins, pointers, sha, qid


def main():
    report_path = DOCS / (PREFIX + 'E2_P05_END_ANCESTRY_RECONCILIATION_1.json')
    report = read(report_path)
    wrapper = read(OUT / 'qualified-evidence-graph.json')
    graph = wrapper['graph']
    assert wrapper['identity'] == report['COMPOSITE_GRAPH_IDENTITY'] == qid('qualification-END-evidence-graph-v1', graph)
    baseline = read(OUT / 'baseline.json')['files']
    changed = [path for path, expected in baseline.items() if not (ROOT / path).is_file() or sha(ROOT / path) != expected]
    assert not changed, changed
    current = read(CURRENT)
    assert [n['original_stage_binding_retained_exact'] for n in graph['stage_nodes']] == current['stage_bindings']
    assert len(graph['stage_nodes']) == 13
    assert all(n['original_stage_binding_retained_exact']['binding_status'] == 'BOUND' for n in graph['stage_nodes'])
    edges = graph['edges']
    assert len({e['edge_id'] for e in edges}) == len(edges) == 70
    native_parent_edges = [e for e in edges if e['native_parent_asserted']]
    assert all(e['relationship'] in ('EVENT_PARENT_AND_PRE_POST_SNAPSHOT', 'LIFECYCLE_STATE_INPUT') for e in native_parent_edges)
    assert all(e['classification'] == 'CANONICAL_NATIVE_ANCESTRY' for e in native_parent_edges)
    cross = [e for e in edges if e['classification'] == 'UNPROVEN']
    assert {(e['source'], e['target']) for e in cross} == {
        ('E2-A02','E2-A03'), ('E2-A04','E2-A05'), ('E2-A05','E2-A06'), ('E2-A06','E2-A07')}
    assert not any(e['native_parent_asserted'] for e in cross)
    segments = graph['native_ledger_segments']
    a03 = c._unwire(read(ROOT / segments['A03']['source']['path'])['bundle'])
    a04 = c._unwire(read(ROOT / segments['A04']['source']['path'])['bundle'])
    assert a04.initial == a03.initial and a04.events[:2] == a03.events
    # Native artifact selectors differ by bundle path even for the shared
    # P03/P04 records; their complete typed native event bodies must match.
    p03 = c._unwire(read(ROOT / segments['P03']['source']['path'])['bundle'])
    p04 = c._unwire(read(ROOT / segments['P04']['source']['path'])['bundle'])
    assert p04.initial == p03.initial and p04.events[:2] == p03.events
    assert len(p04.events) == 20 and len(segments['A06']['events']) == 2
    assert graph['P04_canonical_tail']['owned_A09_A13_sequence'] == list(range(10,21))
    assert p03.initial.context.lineage != c._unwire(read(ROOT / segments['A06']['source']['path'])['bundle']).initial.context.lineage
    dossier = read(OUT / 'aggregate-END-decision-dossier.json')
    assert dossier['subject_identity'] == qid('qualification-scope-subject-v1', dossier['subject'])
    assert dossier['subject_identity'] == report['AGGREGATE_SCOPE_SUBJECT_ID']
    assert dossier['selected_option'] == report['AGGREGATE_END_SELECTED_OPTION'] == 'NONE'
    assert all(not option['selected'] for option in dossier['options'])
    assert set(dossier['subject']['cross_component_edge_ids']) == {e['edge_id'] for e in cross}
    assert dossier['subject']['graph_identity'] == wrapper['identity']
    assert not dossier['native_operating_grant_issued']
    oracle = read(OUT / 'END-qualification-oracle.json')
    assert len(oracle['stage_terms']) == 13 and oracle['edge_terms'] == edges
    assert oracle['aggregate_scope_check'] == 'NOT_SELECTED' and oracle['END_case_verdict'] == 'NOT_EXECUTED_NOT_ACCEPTED'
    assurance = read(OUT / 'aggregate-N12-N13-contract.json')
    assert len(assurance['N12']['terms']) == len(assurance['N13']['terms']) == 6
    assert assurance['N12']['canonical_case']['CASE_ID'] == 'E2-N12'
    assert assurance['N13']['canonical_case']['CASE_ID'] == 'E2-N13'
    assert not assurance['N13']['N13_inferred_from_N12']
    assert not any(x['full_original_native_handoff_assurance_preserved'] for x in assurance.values())
    readers = [read(p) for p in (OUT / 'readers').glob('*.json')]
    assert len(readers) == 12 and {r['seed'] for r in readers} == {'0','1','7','101'}
    assert all(r['RESULT'] == 'PASS' and r['graph_identity'] == wrapper['identity'] and not r['native_lifecycle_calls'] for r in readers)
    for seed in ('0','1','7','101'):
        assert len([r for r in readers if r['seed'] == seed]) == 3
    checked = set()
    for path in sorted(OUT.rglob('*.json')) + [report_path]:
        if path.name in ('baseline.json', 'verification.json'):
            continue
        obj = read(path)
        for item in pins(obj):
            target = ROOT / item['path']
            assert sha(target) == item['raw_sha256'], item['path']
            if item.get('pointer') and target.suffix == '.json':
                pointers(read(target), item['pointer'])
            checked.add((item['path'], item['raw_sha256'], item.get('pointer','')))
    for path in OUT.glob('*.py'):
        ast.parse(path.read_text(), str(path))
    md_path = report_path.with_suffix('.md')
    for target in re.findall(r'\]\(([^)]+)\)', md_path.read_text()):
        filename = re.sub(r':\d+$', '', target)
        candidate = md_path.parent / filename
        assert candidate.is_file() or candidate == OUT / 'verification.json', target
    for value in (graph, dossier, oracle, report):
        assert not re.search(r'\b(?:TBD|TODO|TO_BE_DETERMINED)\b', json.dumps(value)), 'unsealed placeholder'
    assert report['P05_EXECUTION_READY'] == report['P05_EXECUTED'] == report['P06_EXECUTED'] == 'NO'
    assert report['P05_BOUND_STAGE_INPUTS'] == 13 and report['EXISTING_STAGE_BINDINGS_ALTERED'] == 0
    assert report['NEW_NATIVE_AUTHORITY_ISSUED'] == 'NO'
    assert not CALLS
    check = subprocess.run(['git','diff','--check'],cwd=str(ROOT),capture_output=True,text=True)
    assert check.returncode == 0
    save(OUT / 'verification.json', {
        'RESULT': 'PASS', 'baseline_files_unchanged': len(baseline), 'all_13_existing_stage_bindings_unchanged': True,
        'native_reference_checks': 'PASS', 'four_cross_component_relations_still_not_native_ancestry': True,
        'full_P04_native_tail_preserved': True, 'native_role_overlap_not_fabricated': True,
        'source_identity_pointer_checks': len(checked), 'aggregate_scope_subject': dossier['subject_identity'],
        'aggregate_selected_option': 'NONE', 'decision_ready': True, 'graph_identity': wrapper['identity'],
        'fresh_readers': 12, 'hash_seeds': [0,1,7,101], 'native_lifecycle_calls': CALLS,
        'P05_EXECUTED': 'NO', 'P06_EXECUTED': 'NO', 'P05_EXECUTION_READY': 'NO',
        'RUNTIME_MODIFIED': 'NO', 'E1_ARTIFACTS_MODIFIED': 0, 'PRODUCTION_EFFECT': 'NO', 'git_diff_check': 'PASS',
        'reports': [ref(report_path), ref(md_path)],
        'scripts': [ref(p) for p in sorted(OUT.glob('*.py'))],
        'dossier': ref(OUT / 'aggregate-END-decision-dossier.json'),
    })
    print(json.dumps({'VERIFICATION':'PASS','baseline_unchanged':len(baseline),'stage_bindings':'13/13',
                      'P05_EXECUTION_READY':'NO','aggregate_option_selected':'NONE','native_calls':CALLS}))


if __name__ == '__main__':
    main()
