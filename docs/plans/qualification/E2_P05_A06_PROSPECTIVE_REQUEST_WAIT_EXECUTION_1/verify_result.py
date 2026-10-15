"""Final fresh-reader audit of exported native evidence; never creates an occurrence."""
import ast
import hashlib
import json
import re
import subprocess

from common import ROOT, OUT, SEALED, aid, c, equal, fixture, identity, read, ref, refs, save, trace_check


def main():
    report_path = ROOT / 'docs/plans/DETERMINISTIC_PLANNER_V0_1_E2_P05_A06_PROSPECTIVE_REQUEST_WAIT_RESULT_1.json'
    report = read(report_path)
    spec = fixture('primary')
    named = ROOT / report['POST_A06_BUNDLE_PATH']
    # Export verification occurs in a fresh reader after all writers terminated.
    calls = []
    def forbid(name):
        def fail(*args, **kwargs):
            calls.append(name)
            raise AssertionError('Fresh exported reader attempted ' + name)
        return fail
    for name in ('record_result', 'commit_event', 'append_event', 'commit_result', 'admit_external_evidence'):
        setattr(c, name, forbid(name))
    bundle = c.restore(named, identity(spec['EXPECTED_POST_WAIT_BUNDLE_ID']), ROOT)
    trace_check(bundle, spec)
    equal('exported native state identity', aid(c.snapshot_id(bundle.current)), spec['EXPECTED_POST_WAIT_STATE_ID'])
    equal('exact two exported events', len(bundle.events), 2)
    snapshots = {}
    for path in sorted((OUT / 'readers').rglob('*.json')):
        value = read(path)
        key = (value['fixture'], value['boundary'])
        metadata = value['check']['native_Computation_metadata']
        if key in snapshots:
            equal('full native computed semantics across same-fixture readers/seeds/presentations', metadata, snapshots[key])
        else:
            snapshots[key] = metadata

    # HEAD is a mutable publication pointer. Phase-one records retain the exact
    # bytes hash observed at that commit, while the pointer now names phase two.
    # Archive its lossless epoch from native bundle/ledger fields and verify the
    # pre-existing captured hash. Do not edit writer records or native history.
    epoch_refs = {}
    epochs = []
    for path in sorted((OUT / 'runs').glob('*/commit-*.json')):
        record = read(path)
        own = fixture(record['fixture'])
        phase = len(record['trace']['events'])
        previous = own['START_BUNDLE_ID'] if phase == 1 else own['EXPECTED_POST_READY_BUNDLE_ID']
        head = {'schema': 'PLANNER-HEAD-1', 'bundle': c._wire(identity(record['bundle_id'])),
                'previous': c._wire(identity(previous)), 'command': None}
        raw = c.canonical_bytes(head)
        captured = record['durable_HEAD']['raw_sha256']
        equal('lossless HEAD epoch equals hash captured by actual writer', hashlib.sha256(raw).hexdigest(), captured)
        archive = OUT / 'head-epochs' / record['run'] / ('phase-%s-HEAD.json' % phase)
        archive.parent.mkdir(parents=True, exist_ok=True)
        if archive.exists():
            equal('immutable epoch archive', archive.read_bytes(), raw)
        else:
            archive.write_bytes(raw)
        epoch_refs[(record['durable_HEAD']['path'], captured)] = archive
        epochs.append({'writer': ref(path), 'phase': phase, 'actual_commit_captured_HEAD': record['durable_HEAD'],
                       'immutable_lossless_HEAD_epoch': ref(archive), 'native_fields_only': True,
                       'event_or_result_created': False})
    save(OUT / 'head-epoch-bindings.json', {'RESULT': 'PASS', 'epochs': epochs,
         'original_writer_records_modified': False, 'native_history_modified': False,
         'HEAD_epoch_hashes_match_writer_capture': True})

    cache = {}
    resolved = set()
    for path in list(OUT.rglob('*.json')) + [report_path]:
        if path.name in ('baseline.json', 'final-verification.json'):
            continue
        document = read(path)
        for binding in refs(document):
            target = ROOT / binding['path']
            actual = cache.setdefault(str(target), hashlib.sha256(target.read_bytes()).hexdigest())
            if actual != binding['raw_sha256']:
                epoch = epoch_refs.get((binding['path'], binding['raw_sha256']))
                equal('only native captured mutable HEAD epochs may need historic resolution', epoch is not None, True)
                equal('trusted historical HEAD epoch', hashlib.sha256(epoch.read_bytes()).hexdigest(), binding['raw_sha256'])
            resolved.add((binding['path'], binding['raw_sha256']))
    baseline = read(OUT / 'baseline.json')['files']
    changed = [name for name, expected in baseline.items() if not (ROOT / name).is_file() or
               hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != expected]
    equal('all entry artifacts preserved', changed, [])
    ready = read(OUT / 'P05-complete-readiness-result.json')
    sealed = read(SEALED / 'post-A06-complete-P05-readiness-oracle.json')
    equal('all and only sealed readiness terms', [t['id'] for t in ready['terms']], [t['id'] for t in sealed['terms']])
    equal('all sealed predicates preserved', [t['predicate'] for t in ready['terms']], [t['predicate'] for t in sealed['terms']])
    equal('first non-stage blocker', ready['FIRST_NON_STAGE_BLOCKER']['term'], 'GLOBAL_END_BINDINGS')
    equal('P05 remains unexecuted', report['P05_EXECUTED'], 'NO')
    equal('P05 readiness false', report['P05_EXECUTION_READY'], 'NO')
    equal('13/13 stage bindings', report['P05_BOUND_STAGE_INPUTS'], 13)
    for path in OUT.glob('*.py'):
        ast.parse(path.read_text(), str(path))
    md_path = report_path.with_suffix('.md')
    for target in re.findall(r'\]\(([^)]+)\)', md_path.read_text()):
        equal('report link resolves ' + target, (md_path.parent / target).exists(), True)
    check = subprocess.run(['git', 'diff', '--check'], cwd=str(ROOT), capture_output=True, text=True)
    equal('git diff --check', check.returncode, 0)
    equal('fresh reader created no native occurrence', calls, [])
    save(OUT / 'final-verification.json', {
        'RESULT': 'PASS', 'exported_bundle_native_cold_restore': 'PASS',
        'all_native_computed_semantics_across_same_fixture_readers': 'PASS',
        'native_HEAD_epoch_lossless_bindings': ref(OUT / 'head-epoch-bindings.json'),
        'file_identity_bindings_verified': len(resolved), 'baseline_files_unchanged': len(baseline),
        'runtime_and_frozen_E1_unchanged': True, 'report_links_and_harness_syntax': 'PASS',
        'readiness_terms_preserved_exact': True, 'readiness_criteria_added': 0,
        'P05_stage_bindings': '13/13', 'P05_EXECUTION_READY': 'NO', 'P05_EXECUTED': 'NO', 'P06_EXECUTED': 'NO',
        'native_event_count': 2, 'native_append_or_commit_calls': calls, 'git_diff_check': 'PASS',
        'reports': [ref(report_path), ref(md_path)], 'native_bundle': ref(named),
        'harnesses': [ref(path) for path in sorted(OUT.glob('*.py'))],
    })
    print(json.dumps({'FINAL_VERIFICATION': 'PASS', 'native_events': 2,
                      'P05_bindings': '13/13', 'P05_EXECUTION_READY': 'NO',
                      'baseline_unchanged': len(baseline), 'git_diff_check': 'PASS'}))


if __name__ == '__main__':
    main()
