"""Independent native A06 writer/reader processes; no oracle is a Planner operand."""
import argparse
from dataclasses import replace
import json
import os
import sys

from common import (ROOT, OUT, LABELS, SEALED, Divergence, aid, bundle_path, c, core,
                    equal, fixture, identity, m, permutation, read, ref, save,
                    semantic_projection, state_check, trace_check)


def run(args):
    spec = fixture(args.variant)
    store = OUT / 'runs' / args.run
    store.mkdir(parents=True, exist_ok=True)
    meta = dict(LABELS, process_id=os.getpid(), PYTHONHASHSEED=os.environ.get('PYTHONHASHSEED'),
                fixture=args.variant, run=args.run, mode=args.mode)
    if args.mode == 'bootstrap':
        equal('no existing transaction HEAD', (store / 'HEAD.json').exists(), False)
        initial = c.restore(ROOT / spec['START_PATH']['path'], identity(spec['START_BUNDLE_ID']), ROOT)
        initial = permutation(initial, args.presentation)
        equal('permitted presentation preserves identity', aid(c.bundle_id(initial)), spec['START_BUNDLE_ID'])
        report = state_check(initial, spec, 'pre-trace')
        path, value = c.save_bundle(initial, store, ROOT)
        equal('bootstrap exact bundle', aid(value), spec['START_BUNDLE_ID'])
        save(store / 'bootstrap.json', dict(meta, RESULT='PASS', bundle=ref(path),
                                         check=report, presentation=args.presentation,
                                         native_events_created=0))
    elif args.mode == 'commit':
        phase = args.phase
        equal('only phase 1 or 2', phase in (1, 2), True)
        pre_id = spec['START_BUNDLE_ID'] if phase == 1 else spec['EXPECTED_POST_READY_BUNDLE_ID']
        before = c.restore(bundle_path(store, pre_id), identity(pre_id), ROOT)
        state_check(before, spec, 'pre-trace' if phase == 1 else 'request-ready')
        # Construct only from actual restored inputs and explicit native phase;
        # the independently sealed event/Snapshot files are comparison operands.
        stage = m.ExternalStage.EVIDENCE_REQUEST_READY if phase == 1 else m.ExternalStage.WAITING_FOR_EXTERNAL_EVIDENCE
        supplied = m.ExternalEvent(before.current.external_gates[0].id, stage, c.snapshot_id(before.current))
        updated, value = c.commit_event(before, supplied, store, ROOT)
        wanted = spec['EXPECTED_POST_READY_BUNDLE_ID'] if phase == 1 else spec['EXPECTED_POST_WAIT_BUNDLE_ID']
        equal('committed bundle exact', aid(value), wanted, aid(c.snapshot_id(updated.current)))
        check = trace_check(updated, spec, phase)
        save(store / ('commit-%s.json' % phase), dict(meta, RESULT='PASS', actual_command=c._wire(supplied),
                actual_event=c._wire(updated.events[-1]), bundle_id=aid(value), bundle=ref(bundle_path(store, wanted)),
                state_id=aid(c.snapshot_id(updated.current)), event_count=len(updated.events), trace=check,
                semantic_projection=semantic_projection(updated) if phase == 2 else None,
                actual_operation='codec.commit_event', no_oracle_submitted=True, durable_HEAD=ref(store / 'HEAD.json')))
    elif args.mode == 'read':
        boundaries = {'start': ('pre-trace', spec['START_BUNDLE_ID']),
                      'ready': ('request-ready', spec['EXPECTED_POST_READY_BUNDLE_ID']),
                      'wait': ('post-trace', spec['EXPECTED_POST_WAIT_BUNDLE_ID'])}
        boundary, value = boundaries[args.boundary]
        # Replay/restore may apply recorded state effects but may never append
        # or commit or choose a fresh request/wait result.
        append_calls = []
        def forbidden(name):
            def fail(*a, **kw):
                append_calls.append(name)
                raise Divergence('reader/replay attempted new occurrence', [], append_calls)
            return fail
        for name in ('record_result', 'commit_event', 'append_event', 'commit_result', 'admit_external_evidence'):
            setattr(c, name, forbidden(name))
        before_files = {p.name: p.read_bytes() for p in store.iterdir() if p.is_file()}
        restored = c.restore(bundle_path(store, value), identity(value), ROOT)
        state = state_check(restored, spec, boundary)
        replay = c._replay(restored)
        equal('historical replay state', c.snapshot_bytes(replay), c.snapshot_bytes(restored.current))
        second = c._replay(restored)
        equal('repeated replay identity', c.snapshot_id(second), c.snapshot_id(replay))
        prefix = c._prefix_bundle(restored, 0)
        equal('replay starts at exact sealed start', aid(c.bundle_id(prefix)), spec['START_BUNDLE_ID'])
        if args.boundary != 'start':
            trace_check(restored, spec, 1 if args.boundary == 'ready' else 2)
        equal('reader changes no existing files', {p.name: p.read_bytes() for p in store.iterdir() if p.is_file()}, before_files)
        report = dict(meta, RESULT='PASS', boundary=args.boundary, reader_index=args.reader,
                      bundle_id=value, check=state, historical_replay='PASS', repeat_replay='PASS',
                      event_count=len(restored.events), new_occurrences=0, replay_append_calls=append_calls,
                      exact_initial_binding='PASS', writer_memory_available=False,
                      semantic_projection=semantic_projection(restored) if args.boundary == 'wait' else None)
        save(OUT / 'readers' / args.run / ('%s-%s.json' % (args.boundary, args.reader)), report)
    elif args.mode == 'retry':
        final = c.restore(bundle_path(store, spec['EXPECTED_POST_WAIT_BUNDLE_ID']), identity(spec['EXPECTED_POST_WAIT_BUNDLE_ID']), ROOT)
        old = {p.name: p.read_bytes() for p in store.iterdir() if p.is_file()}
        results = []
        for event in final.events:
            same = c.append_event(final, event)
            equal('identity retry creates no event', c.bundle_bytes(same), c.bundle_bytes(final))
            conflicting = replace(event, result=replace(event.result, gate=m.GateId('FOREIGN-GATE')))
            try:
                c.append_event(final, conflicting)
            except m.PlannerError as error:
                results.append({'event_id': aid(event.identity), 'append_retry': 'IDEMPOTENT',
                                'conflicting_retry': 'REJECTED', 'reason': str(error)})
            else:
                raise Divergence('conflicting event retry', 'REJECTED', 'ACCEPTED')
        for phase in (1, 2):
            prior = c.restore(bundle_path(store, spec['START_BUNDLE_ID'] if phase == 1 else spec['EXPECTED_POST_READY_BUNDLE_ID']),
                              identity(spec['START_BUNDLE_ID'] if phase == 1 else spec['EXPECTED_POST_READY_BUNDLE_ID']), ROOT)
            try:
                c.commit_event(prior, final.events[phase - 1].result, store, ROOT)
            except m.PlannerError as error:
                equal('stale durable retry', str(error), 'PARENT_MISMATCH')
                results[phase - 1]['stale_commit_retry'] = 'PARENT_MISMATCH'
            else:
                raise Divergence('stale commit retry', 'REJECTED', 'ACCEPTED')
        equal('retry leaves durable files unchanged', {p.name: p.read_bytes() for p in store.iterdir() if p.is_file()}, old)
        save(OUT / 'retry' / (args.run + '.json'), dict(meta, RESULT='PASS', checks=results,
                                                      durable_history_unchanged=True, events=2))
    else:
        raise ValueError('Unknown mode')
    print(json.dumps({'RESULT': 'PASS', 'mode': args.mode, 'run': args.run,
                      'phase': args.phase, 'boundary': args.boundary}, sort_keys=True))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['bootstrap', 'commit', 'read', 'retry'])
    parser.add_argument('--variant', default='primary')
    parser.add_argument('--run', required=True)
    parser.add_argument('--phase', type=int, default=0)
    parser.add_argument('--boundary', choices=['start', 'ready', 'wait'], default='start')
    parser.add_argument('--reader', type=int, default=0)
    parser.add_argument('--presentation', choices=['original', 'reversed', 'rotated'], default='original')
    args = parser.parse_args()
    try:
        run(args)
    except Exception as exc:
        record = exc.record if isinstance(exc, Divergence) else {
            'FIRST_COUNTEREXAMPLE': 'Native qualification process failure', 'EXPECTED': 'Sealed oracle PASS',
            'ACTUAL': type(exc).__name__ + ':' + str(exc), 'STATE_ID': None, 'EVENT_ID': None,
            'CLASSIFICATION': 'NATIVE_OR_HARNESS_FAILURE_REQUIRES_STOP',
        }
        save(OUT / ('STOP-' + args.run + '-' + args.mode + '-' + str(args.phase) + '.json'), record)
        print(json.dumps(record, sort_keys=True))
        sys.exit(1)
