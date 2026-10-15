"""Read-only native key/set presentation equivalence; causal order is preserved."""
from dataclasses import replace
import json

from common import OUT, ROOT, aid, bundle_path, c, core, equal, fixture, identity, permutation, report_view, save


def rearrange(value, form):
    if isinstance(value, dict):
        keys = list(value)
        if form == 'reversed':
            keys.reverse()
        elif form == 'rotated':
            keys = keys[1:] + keys[:1]
        return {key: rearrange(value[key], form) for key in keys}
    if isinstance(value, list):
        return [rearrange(child, form) for child in value]
    return value


def main():
    spec = fixture('primary')
    store = OUT / 'runs/primary-seed-0'
    final = c.restore(bundle_path(store, spec['EXPECTED_POST_WAIT_BUNDLE_ID']), identity(spec['EXPECTED_POST_WAIT_BUNDLE_ID']), ROOT)
    expected_snapshot = c.snapshot_bytes(final.current)
    expected_bundle = c.bundle_bytes(final)
    expected_computation = report_view(core.recompute(final.current))
    results = []
    for form in ('original', 'reversed', 'rotated'):
        native = c._unwire(rearrange(c._wire(permutation(final, form)), form))
        # Presentation reconstruction is comparison only, never a writer operand.
        equal('unordered/key Snapshot bytes', c.snapshot_bytes(native.current), expected_snapshot)
        equal('unordered/key bundle bytes', c.bundle_bytes(native), expected_bundle)
        equal('unordered/key Computation', report_view(core.recompute(native.current)), expected_computation)
        equal('causal ledger order unchanged', native.events, final.events)
        equal('gate history order unchanged', native.current.external_gates[0].history, final.current.external_gates[0].history)
        results.append({'presentation': form, 'RESULT': 'PASS', 'snapshot_id': aid(c.snapshot_id(native.current)),
                        'bundle_id': aid(c.bundle_id(native)), 'causal_order_permuted': False,
                        'comparison_only': True})
    save(OUT / 'presentation-comparison.json', {'RESULT': 'PASS', 'cases': results,
         'declared_unordered_fields': ['object keys', 'Snapshot.predicates', 'PersistenceBundle.sources'],
         'native_identity_semantics_changed': False})
    print(json.dumps({'PRESENTATION_COMPARISON': 'PASS', 'cases': len(results)}))


if __name__ == '__main__':
    main()
