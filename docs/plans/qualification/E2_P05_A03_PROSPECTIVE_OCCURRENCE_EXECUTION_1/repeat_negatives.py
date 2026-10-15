"""Repeat the unchanged sealed negatives in separate immutable fixture copies."""
import json
import os
from pathlib import Path
import shutil

import execution_driver as d
import qualification_checks as q


if __name__ == '__main__':
    original = d.OUT
    seed = os.environ['PYTHONHASHSEED']
    destination = original / 'negative-reproductions' / ('seed-' + seed)
    d.equal('NEW_NEGATIVE_FIXTURE_DIRECTORY', destination.exists(), False)
    destination.mkdir(parents=True)
    shutil.copytree(original / 'writer-main', destination / 'writer-main')
    shutil.copyfile(original / 'entry-gate.json', destination / 'entry-gate.json')
    # This is a harness output-directory binding, not a native state/identity
    # change. The actual event/input/oracle/source/runtime bytes stay exact.
    d.OUT = destination
    try:
        q.negatives()
        actual = d.read(destination / 'negative-results.json')
        primary = d.read(original / 'negative-results.json')
        d.equal('NEGATIVE_RESULTS_SEED_STABILITY', actual, primary)
        d.write(destination / 'rejection-stability.json', {**d.LABELS, 'result': 'PASS',
                'hash_seed': seed, 'independent_process': True, 'PID': os.getpid(),
                'negative_controls': actual['count'], 'variants_rejected': actual['variants_rejected'],
                'new_positive_execution': False, 'primary_fixture_copy_only': True,
                'native_result_events_added': 0, 'primary_lineage_modified': False,
                'identical_rejections_to_primary': True})
        print(json.dumps({'result': 'PASS', 'hash_seed': seed, 'negative_controls': actual['count'],
                          'rejection_semantics_equal': True}))
    except Exception as exc:
        record = {**d.LABELS, 'result': 'FAIL', 'FIRST_COUNTEREXAMPLE': getattr(exc, 'name', type(exc).__name__),
                  'EXPECTED': repr(getattr(exc, 'expected', None)), 'ACTUAL': repr(getattr(exc, 'actual', str(exc))),
                  'STATE_ID': d.STATE['state_id'], 'EVENT_ID': d.STATE['event_id'],
                  'CLASSIFICATION': 'NEGATIVE_REPRODUCTION_DIVERGENCE', 'no_live_repair': True}
        d.write(original / 'STOP.json', record)
        raise
