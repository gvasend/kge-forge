"""Execute the 27 unchanged sealed mutations on isolated native/acceptance fixtures."""
from dataclasses import replace
import json
import sys

from common import (OUT, ROOT, SEALED, LABELS, Divergence, aid, bundle_path, c, equal,
                    fixture, identity, m, read, ref, save, state_check, trace_check)


def rejected(operation, kind):
    try:
        operation()
    except (m.PlannerError, Divergence) as error:
        return {'rejected': True, 'boundary': kind, 'exception_type': type(error).__name__,
                'reason': error.record if isinstance(error, Divergence) else str(error)}
    raise Divergence('sealed negative accepted at ' + kind, 'REJECTED', 'ACCEPTED')


def main():
    spec = fixture('primary')
    source = OUT / 'runs/primary-seed-0'
    good = c.restore(bundle_path(source, spec['EXPECTED_POST_WAIT_BUNDLE_ID']), identity(spec['EXPECTED_POST_WAIT_BUNDLE_ID']), ROOT)
    start = c.restore(bundle_path(source, spec['START_BUNDLE_ID']), identity(spec['START_BUNDLE_ID']), ROOT)
    ready = c.restore(bundle_path(source, spec['EXPECTED_POST_READY_BUNDLE_ID']), identity(spec['EXPECTED_POST_READY_BUNDLE_ID']), ROOT)
    untouched = {p.name: p.read_bytes() for p in source.iterdir() if p.is_file()}
    original_state = c.snapshot_bytes(start.current)
    command = good.events[0].result
    cases = read(SEALED / 'sealed-negative-oracles.json')['cases']
    results = []

    def start_guard(candidate):
        # This is the already sealed exact-input comparison boundary. It adds
        # no semantic runtime rule and treats attacker rehashing as untrusted.
        state_check(candidate, spec, 'pre-trace')

    def native_command(candidate):
        store = OUT / 'negative-stores' / active['id']
        before = c.bundle_bytes(start)
        answer = rejected(lambda: c.commit_event(start, candidate, store, ROOT), 'native commit_event/apply_receipt')
        equal('negative native authoritative pre-state unchanged', c.bundle_bytes(start), before)
        equal('negative has no durable HEAD', (store / 'HEAD.json').exists(), False)
        equal('negative has no durable event/bundle', list(store.glob('*.json')), [])
        return answer

    def corrupt_ledger(which, **changes):
        events = list(good.events)
        event = replace(events[which], **changes)
        event = replace(event, identity=c._event_identity(event.sequence, event.parent_snapshot,
                        event.parent_event, event.result, event.after_snapshot, event.resume_binding))
        events[which] = event
        return rejected(lambda: c._replay(replace(good, events=tuple(events))), 'native ledger/replay')

    def resolution_change(**changes):
        gate = start.current.external_gates[0]
        request = replace(gate.resolution_contracts[0], **changes)
        modified = replace(start.current, external_gates=(replace(gate, resolution_contracts=(request,)),))
        return replace(start, initial=modified, current=modified)

    def context_change(**changes):
        modified = replace(start.current, context=replace(start.current.context, **changes))
        return replace(start, initial=modified, current=modified)

    def mapping_guard(candidate):
        for key, expected in LABELS.items():
            equal('mapping label ' + key, candidate.get(key), expected)
        equal('replacement only', candidate.get('classification'), 'AUTHORIZED_PROSPECTIVE_REPLACEMENT')
        equal('only A06 input', candidate.get('input'), 'E2-A06.request_wait_event_trace')
        equal('no original identity alias', candidate.get('original_event_ids'), None)
        equal('no prefix waiver', candidate.get('original_prefix_closed'), False)
        equal('no A05 scope expansion', candidate.get('A05_closed_by_this_mapping'), False)

    def mapping_change(**changes):
        value = dict(LABELS, classification='AUTHORIZED_PROSPECTIVE_REPLACEMENT',
                     input='E2-A06.request_wait_event_trace', original_event_ids=None,
                     original_prefix_closed=False, A05_closed_by_this_mapping=False)
        value.update(changes)
        return rejected(lambda: mapping_guard(value), 'sealed historical/END scope mapping guard')

    for active in cases:
        name = active['name']
        if name == 'wrong_request':
            result = rejected(lambda: start_guard(resolution_change(request='WRONG-REQUEST')), 'sealed exact-input guard')
        elif name == 'wrong_gate':
            result = native_command(replace(command, gate=m.GateId('WRONG-GATE')))
        elif name == 'wrong_dependency':
            requirement = replace(start.current.evidence_requirements[0], proposition='DIFFERENT PROPOSITION')
            altered = replace(start.current, evidence_requirements=(requirement,))
            result = rejected(lambda: start_guard(replace(start, initial=altered, current=altered)), 'sealed known-rule requirement')
        elif name == 'wrong_parent':
            result = corrupt_ledger(0, parent_event=good.events[1].identity)
        elif name == 'wrong_pre_state':
            result = native_command(replace(command, expected_snapshot=c.snapshot_id(ready.current)))
        elif name == 'wrong_event_type':
            altered = m.SuppliedResult(start.current.actions[0].id, m.ActionResult.PASS, (), c.snapshot_id(start.current))
            result = native_command(altered)
        elif name == 'wrong_event_payload':
            result = native_command(replace(command, artifact=m.EntityId('FOREIGN-EVIDENCE')))
        elif name == 'wrong_request_binding':
            result = rejected(lambda: start_guard(resolution_change(source_class='DIFFERENT SOURCE CLASS')), 'sealed request source/context')
        elif name == 'wrong_gate_binding':
            result = rejected(lambda: start_guard(resolution_change(reentry=(m.ActionId('UNRELATED-ACTION'),))), 'sealed gate binding')
        elif name == 'wrong_event_ordering':
            reverse = replace(good, events=tuple(reversed(good.events)))
            result = rejected(lambda: c._replay(reverse), 'native ledger causal ordering')
        elif name == 'wrong_ledger':
            other = fixture('reproduction-1')
            foreign = c.restore(bundle_path(OUT / 'runs/reproduction-1', other['EXPECTED_POST_WAIT_BUNDLE_ID']),
                                identity(other['EXPECTED_POST_WAIT_BUNDLE_ID']), ROOT)
            result = rejected(lambda: trace_check(foreign, spec), 'trusted exact native ledger oracle')
        elif name == 'wrong_ledger_position':
            result = corrupt_ledger(1, sequence=3)
        elif name == 'wrong_authority':
            auth = read(SEALED / 'authorization-capture.json')
            altered = dict(auth, SELECTED_OPTION='USE_AUTHORITY', event_authority_operand='INSTALL')
            result = rejected(lambda: equal('qualification scope authority', altered['SELECTED_OPTION'],
                              'AUTHORIZE_PROSPECTIVE_P05_A06_REQUEST_WAIT_QUALIFICATION'), 'sealed scope/context authority preflight')
        elif name == 'wrong_scope':
            result = rejected(lambda: start_guard(context_change(scope='PRODUCTION')), 'trusted input scope identity')
        elif name == 'wrong_lineage':
            result = rejected(lambda: start_guard(context_change(lineage='E2-CANONICAL-BASELINE-1')), 'trusted input lineage identity')
        elif name == 'wrong_generation':
            result = rejected(lambda: start_guard(context_change(generation='FOREIGN-GENERATION', tick=1)), 'trusted generation/currentness identity')
        elif name == 'wrong_provenance':
            gate = start.current.external_gates[0]
            altered = replace(start.current, external_gates=(replace(gate, provenance=replace(gate.provenance, method='DIFFERENT-ORIGIN')),))
            result = rejected(lambda: start_guard(replace(start, initial=altered, current=altered)), 'sealed source/Snapshot provenance guard')
        elif name == 'wait_without_request_ready':
            result = native_command(replace(command, stage=m.ExternalStage.WAITING_FOR_EXTERNAL_EVIDENCE))
        elif name == 'request_without_wait':
            state_check(ready, spec, 'request-ready')
            result = rejected(lambda: trace_check(ready, spec), 'complete two-event occurrence oracle')
            result['intermediate_native_state_legal'] = True
        elif name == 'snapshot_substituted_for_trace':
            result = rejected(lambda: trace_check(good.current, spec), 'native occurrence type oracle')
        elif name == 'report_substituted_for_trace':
            result = rejected(lambda: trace_check({'RESULT': 'PASS', 'CONTROL': 'EXTERNAL_WAIT'}, spec), 'native occurrence type oracle')
        elif name == 'preexisting_wait_instead_of_occurrence':
            fake = replace(start, initial=good.current, current=good.current)
            result = rejected(lambda: start_guard(fake), 'sealed nonwaiting pre-occurrence start')
            result['legitimate_pre_control_EXTERNAL_WAIT_rejected'] = False
        elif name == 'later_evidence_transition':
            # Received has no admitted evidence; native path rejects. Complete
            # post oracle separately allows only the two presealed phases.
            store = OUT / 'negative-stores' / active['id']
            later = m.ExternalEvent(good.current.external_gates[0].id, m.ExternalStage.EVIDENCE_RECEIVED,
                                    c.snapshot_id(good.current))
            result = rejected(lambda: c.commit_event(good, later, store, ROOT), 'native absent-evidence receipt admission')
            equal('no later phase HEAD', (store / 'HEAD.json').exists(), False)
        elif name == 'prospective_labeled_historical':
            result = mapping_change(ORIGINAL_A06_HISTORICAL_REQUEST_WAIT_TRACE='PROVEN', HISTORICAL_RECONSTRUCTION='YES')
        elif name == 'prospective_identity_substituted_original':
            result = mapping_change(original_event_ids=[aid(e.identity) for e in good.events])
        elif name == 'oracle_used_as_operation_input':
            candidate = {'operand_source': 'COMPARISON_ORACLE', 'object': read(ROOT / spec['EXPECTED_EVENT_ORACLE'][0]['expected_event_file']['path'])}
            result = rejected(lambda: equal('writer native operand origin', candidate['operand_source'], 'ACTUAL_RESTORED_STATE_COMMAND'),
                              'sealed writer input allowlist; comparison event never submitted')
        elif name == 'broadened_full_END_or_A05_mapping':
            result = mapping_change(original_prefix_closed=True, A05_closed_by_this_mapping=True)
        else:
            raise Divergence('sealed negative coverage', 'Known immutable case', name)
        equal('negative modified successful native store', {p.name: p.read_bytes() for p in source.iterdir() if p.is_file()}, untouched)
        equal('negative modified authoritative pre-state', c.snapshot_bytes(start.current), original_state)
        results.append(dict(active, actual_execution='EXECUTED_ISOLATED', RESULT='PASS', actual=result,
                            no_canonical_or_successful_lineage_mutation=True))
    equal('27 sealed cases covered exactly', [r['id'] for r in results], [r['id'] for r in cases])
    save(OUT / 'negative-results.json', dict(LABELS, RESULT='PASS', sealed_count=27, executed_count=27,
        cases=results, sealed_expectations=ref(SEALED / 'sealed-negative-oracles.json'),
        native_and_acceptance_boundaries_distinguished=True, historical_P05_negatives_not_executed=True,
        successful_lineage_unchanged=True))
    print(json.dumps({'NEGATIVE_SUITE': 'PASS', 'cases': len(results)}))


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        save(OUT / 'STOP-negative-suite.json', error.record if isinstance(error, Divergence) else {'error': str(error)})
        raise
