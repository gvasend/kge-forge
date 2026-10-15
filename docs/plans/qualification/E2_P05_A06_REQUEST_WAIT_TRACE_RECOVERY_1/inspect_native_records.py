"""Pure native decode, pin, identity and state queries; lifecycle paths barred."""
import hashlib
import json
from pathlib import Path

from adapter.planner import codec as c, core, gates, human_decision as hd, model as m

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
PLANS = ROOT / 'docs/plans'
PREFIX = 'DETERMINISTIC_PLANNER_V0_1_'
BARRED = []


def deny(name):
    def rejected(*args, **kwargs):
        BARRED.append(name)
        raise RuntimeError('Read-only recovery cannot invoke ' + name)
    return rejected


for module, names in (
    (hd, ('capture_choice', 'materialize_choice', 'apply_explicit_choice')),
    (core, ('apply_result', '_inventory', 'coverage_scores', 'admit_dossier_materialization',
            'apply_recorded_decision', 'apply_decision_reentry', 'apply_event', 'apply_receipt', 'resume_eligibility')),
    (c, ('_replay', '_prefix_bundle', 'append_event', 'record_result', 'bundle_bytes', 'bundle_id',
         'save_bundle', 'restore', 'commit_event', '_publish_head', '_read_head',
         'admit_external_evidence', 'apply_event', '_extend_private')),
):
    for name in names:
        setattr(module, name, deny(module.__name__ + '.' + name))


def aid(value):
    return None if value is None else value.namespace + ':' + value.sha256


def pin(path, pointer=''):
    return {'path': str(path.relative_to(ROOT)), 'pointer': pointer,
            'raw_sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def save(name, value):
    (OUT / name).write_text(json.dumps(value, sort_keys=True, indent=2) + '\n')


def state_view(snapshot, source, compute_wait=False):
    m.validate_types(snapshot, m.Snapshot)
    m.validate_model(snapshot)
    state_id = c.snapshot_id(snapshot)
    gate = next(g for g in snapshot.external_gates if g.id.value == 'E2-GATE')
    requirement = next(r for r in snapshot.evidence_requirements if r.id.value == 'E2-EXTERNAL-REQUIREMENT')
    contracts = []
    for contract in gate.resolution_contracts:
        relations = {
            'gate': contract.gate == gate.id,
            'requirement': contract.requirement == requirement.id,
            'proposition': contract.proposition == requirement.proposition,
            'target': contract.target == requirement.target,
            'producers': set(contract.producers) == set(requirement.producers),
            'requirement_source': contract.requirement_source == requirement.provenance.identity,
            'gate_source': contract.gate_source == gate.provenance.identity,
            'receipt_action': contract.receipt_action == gate.receipt_action,
            'reentry': set(contract.reentry) == set(gate.reentry),
            'held_actions': set(contract.held_actions) == set(gate.held_actions),
            'scope': contract.scope == snapshot.context.scope,
            'lineage': contract.lineage == snapshot.context.lineage,
            'generation': contract.generation == snapshot.context.generation}
        assert all(relations.values()), (source, relations)
        contracts.append({'native_contract': c._wire(contract), 'relations': relations,
                          'request': contract.request,
                          'identity_domain': 'request is str, not RequestId, EventId or native issuance instance',
                          'native_source_identity': aid(contract.provenance.identity)})
    result = {'source': source, 'snapshot_identity': aid(state_id), 'model_admission': 'PASS',
        'context': c._wire(snapshot.context), 'gate': c._wire(gate), 'requirement': c._wire(requirement),
        'resolution_contracts': contracts,
        'request_contract_present': bool(contracts), 'known_validation_rule': requirement.rule_known,
        'pending_receipt': c._wire(gate.pending), 'receipt_observations': c._wire(snapshot.receipt_observations),
        'boundaries': [c._wire(b) for b in snapshot.boundaries if b.id == gate.id],
        'decision_stage': next(d.stage.value for d in snapshot.decisions if d.action.value == 'E2-DECIDE'),
        'reenter_status': next(s.state.value for s in snapshot.statuses if s.id.value == 'E2-REENTER'),
        'original_A06_event_occurrence': 'NOT_ESTABLISHED_BY_SNAPSHOT_OR_GATE_HISTORY',
        'enclosing_event_or_ledger_in_Snapshot': False}
    if compute_wait:
        statuses, blocked, actions = core._actionability(snapshot)
        assert not actions, (source, 'Expected no internal/human action ready at retained wait checkpoint')
        projection = core.project(snapshot)
        # There is no selection or result model to simulate: the actual query
        # finds zero ready Actions. Feed native statuses/blocks into control.
        computation = core.Computation((), statuses, blocked, None, projection.defects)
        computation = core._global_control(snapshot, computation)
        proof = gates.obligation_proof(snapshot, requirement.id)
        result['read_only_wait_query'] = {
            'control': computation.control.value,
            'actionable': [a.value for a in computation.actionable],
            'human_ready': [], 'selected': None,
            'defects': list(computation.defects), 'frontier': c._wire(computation.frontier),
            'obligation_proof': {'native_computed_type': 'gates.Proof',
                                 'state': proof.state.value, 'reasons': list(proof.reasons)},
            'reentry_event_present_in_this_query': False,
            'accepted_observation_present': any(o.accepted for o in snapshot.receipt_observations)}
        assert computation.control is m.ControlState.EXTERNAL_WAIT and not computation.defects
        assert proof.state is not m.ProofState.PROVED and gate.pending is None and not snapshot.receipt_observations
        assert not any(s.id.value == 'E2-REENTER' and s.state is m.ActionState.COMPLETED for s in snapshot.statuses)
    assert c.snapshot_id(snapshot) == state_id
    return result


def snapshot_file(name, compute_wait=False):
    path = PLANS / (PREFIX + name + '.json')
    snapshot = c._unwire(json.loads(path.read_bytes())['snapshot'])
    return state_view(snapshot, pin(path, '/snapshot'), compute_wait)


def bundle_file(name, compute_wait=False):
    path = PLANS / (PREFIX + name + '.json')
    bundle = c._unwire(json.loads(path.read_bytes())['bundle'])
    m.validate_types(bundle, m.PersistenceBundle)
    m.validate_model(bundle.initial)
    m.validate_model(bundle.current)
    c._verify_sources(bundle, ROOT)
    rows = []
    for index, event in enumerate(bundle.events):
        expected = c._event_identity(event.sequence, event.parent_snapshot, event.parent_event,
                                     event.result, event.after_snapshot, event.resume_binding)
        checks = {
            'event_identity': expected == event.identity,
            'position_sequence': event.sequence == index + 1,
            'parent_event': event.parent_event == (bundle.events[index - 1].identity if index else None),
            'pre_snapshot': event.parent_snapshot == (bundle.events[index - 1].after_snapshot if index else c.snapshot_id(bundle.initial)),
            'command_pre_snapshot': not hasattr(event.result, 'expected_snapshot') or event.result.expected_snapshot == event.parent_snapshot}
        assert all(checks.values()), (name, index, checks)
        rows.append({'source': pin(path, '/bundle/events/' + str(index)), 'identity': aid(event.identity),
                     'index': index, 'sequence': event.sequence, 'parent': aid(event.parent_event),
                     'pre_state': aid(event.parent_snapshot), 'post_state': aid(event.after_snapshot),
                     'result_type': type(event.result).__name__,
                     'gate': event.result.gate.value if hasattr(event.result, 'gate') else None,
                     'stage': event.result.stage.value if hasattr(event.result, 'stage') else None,
                     'checks': checks})
    assert (bundle.events[-1].after_snapshot if bundle.events else c.snapshot_id(bundle.initial)) == c.snapshot_id(bundle.current)
    comparison = c._identity(c._bundle_bytes_admitted(bundle), 'planner-bundle-v1')
    request_wait = [row for row in rows if row['stage'] in
                    ('EVIDENCE_REQUEST_READY', 'WAITING_FOR_EXTERNAL_EVIDENCE')]
    return {'source': pin(path, '/bundle'), 'bundle_comparison_identity': aid(comparison),
        'native_source_and_policy_pins': 'PASS', 'source_pin_count': len(bundle.sources),
        'policy_pin': c._wire(bundle.policy),
        'ledger_id': 'NOT_EXPOSED_BY_NATIVE_PERSISTENCEBUNDLE',
        'membership': aid(comparison) + '#/bundle/events',
        'event_count': len(rows), 'root': rows[0]['identity'] if rows else None,
        'head': rows[-1]['identity'] if rows else None, 'events': rows,
        'request_wait_events': request_wait,
        'initial': state_view(bundle.initial, pin(path, '/bundle/initial')),
        'current': state_view(bundle.current, pin(path, '/bundle/current'), compute_wait),
        'native_result_application_or_replay': 'NOT_RUN'}


def main():
    original_initial = snapshot_file('E2_P02_INITIAL_SNAPSHOT')
    original_handoff = snapshot_file('E2_AUTHORITATIVE_HANDOFF_SNAPSHOT_1')
    original_wait = snapshot_file('E2_HUMAN_DECISION_ALLOW_POST_SNAPSHOT_1', True)
    checkpoint = bundle_file('P03_PROSPECTIVE_CHECKPOINT_BUNDLE_1', True)
    target = bundle_file('E2_P04_CANONICAL_TARGET_BUNDLE_1')
    a04 = bundle_file('E2_P05_A04_PROSPECTIVE_ANCESTRY_BUNDLE_1')
    for state in (original_initial, original_handoff, original_wait, checkpoint['initial'], checkpoint['current'], target['initial'], a04['initial'], a04['current']):
        assert state['gate']['stage']['value'] == 'WAITING_FOR_EXTERNAL_EVIDENCE'
        assert state['gate']['history'] == []
    assert original_wait['snapshot_identity'] == 'planner-snapshot-v1:8d77f7f1997ca884e07490c4c93f5fbe3a31b09278fd57c6c6ea1f9fa26b3aaf'
    assert not checkpoint['request_wait_events'] and not target['request_wait_events'] and not a04['request_wait_events']
    search = json.loads((OUT / 'event-search.json').read_bytes())
    assert not search['request_wait_events']
    assert all(row['event']['result']['stage']['value'] in ('EVIDENCE_RECEIVED', 'DEPENDENT_ACTION_REENTRY') for row in search['external_events'])
    assert not BARRED
    result = {'schema': 'A06-NATIVE-STATE-AND-LEDGER-INSPECTION-1', 'result': 'PASS_READ_ONLY_INSPECTION',
        'original_initial': original_initial, 'original_handoff': original_handoff, 'original_post_decision_wait': original_wait,
        'P03_prospective_checkpoint': checkpoint, 'P04_canonical_target': target,
        'A04_prospective_frontier': a04,
        'original_and_checkpoint_wait_is_retained_initial_state_not_event_occurrence': True,
        'request_ready_and_wait_events_absent': True, 'request_identity_domain': 'ExternalResolutionContract.request:str',
        'same_literal_request_name_does_not_bind_foreign_context': True,
        'A06_NATIVE_OPERATION_CALLS': 0, 'native_events_created': 0, 'native_replay_calls': 0,
        'barred_calls': BARRED}
    save('native-state-and-ledger-inspection.json', result)
    print(json.dumps({'inspection': 'PASS', 'original_wait': original_wait['snapshot_identity'],
        'request_name': original_wait['resolution_contracts'][0]['request'],
        'original_control': original_wait['read_only_wait_query']['control'],
        'request_wait_native_events': 0, 'barred_calls': BARRED}))


if __name__ == '__main__':
    main()
