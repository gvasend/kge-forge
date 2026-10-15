"""Read-only P05 entry inspection; no tests, events, installations or issuance."""
import hashlib
import json
import os
from pathlib import Path

from adapter.planner import codec as c, core, gates, installation as install
from adapter.planner import model as m, typed_proofs as tp
from adapter.tests.qualify_finish_f03 import semantic_view

ROOT = Path(__file__).resolve().parents[4]
DOCS = ROOT / 'docs/plans'
OUT = Path(__file__).resolve().parent
PREFIX = 'DETERMINISTIC_PLANNER_V0_1_'


def read(path):
    return json.loads(path.read_text())


def uid(value):
    return value.namespace + ':' + value.sha256


def main():
    expected = read(OUT / 'initial-oracle.json')
    target_path = ROOT / expected['entry_path']
    identity = m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY, 'planner-bundle-v1',
                                  expected['bundle_id'].split(':', 1)[1])
    bundle = c.restore(target_path, identity, ROOT)
    state = bundle.current
    comp = core.recompute(state)
    actual_semantic = semantic_view(bundle, ROOT)
    sealed = read(ROOT / expected['semantic_oracle_path'])['semantic_oracle']
    checks = {}

    def check(name, wanted, actual):
        checks[name] = {'expected': wanted, 'actual': actual, 'pass': wanted == actual}

    check('P04_result', 'PASS', read(ROOT / expected['P04_report_path'])['E2_P04_RESULT'])
    check('bundle_identity', expected['bundle_id'], uid(c.bundle_id(bundle)))
    check('snapshot_identity', expected['state_id'], uid(c.snapshot_id(state)))
    check('ledger_anchor', expected['ledger_anchor'], uid(bundle.events[0].identity))
    check('append_head', expected['append_head'], uid(bundle.events[-1].identity))
    check('event_count', 20, len(bundle.events))
    check('source_pins_exact', sealed['sources'], actual_semantic['sources'])
    check('policy_pin_exact', sealed['policy'], actual_semantic['policy'])
    check('policy_version', 'E1-SELECTION-1-P06', bundle.policy_version)
    check('scope', 'E2-QUALIFICATION-ONLY', state.context.scope)
    check('lineage', 'E2-P03-PROSPECTIVE-QUALIFICATION-1', state.context.lineage)
    check('generation', 'E2-P03-PROSPECTIVE-GENERATION-1', state.context.generation)
    check('context_exact', sealed['context'], actual_semantic['context'])
    check('control', 'TERMINAL_SUCCESS', comp.control.value)
    check('action_universe', expected['actions'], sorted(a.id.value for a in state.actions))
    check('all_actions_completed', expected['actions'],
          sorted(s.id.value for s in state.statuses if s.state is m.ActionState.COMPLETED))
    check('actionable', [], [a.value for a in comp.actionable])
    check('selected', None, comp.selection.selected.value if comp.selection else None)
    check('known_REENTER_FINISH', ['E2-K-FINISH', 'E2-K-REENTER'],
          sorted(k.id.value for k in state.knowledge if k.id.value in ('E2-K-REENTER', 'E2-K-FINISH')
                 and k.state is m.KnowledgeState.KNOWN_COMPLETE and k.validation is m.ValidationState.ACCEPTED))
    check('root', ['SATISFIED'], [r.state.value for r in state.roots])
    check('slot', ['RESOLVED'], [s.state.value for s in state.slots])
    check('ValidationResults', 1, len(state.validation_results))
    check('support_records', 1, len(state.validation_support_records))
    check('typed_proof_instances', 2, len(state.typed_proofs))
    check('typed_proof_currentness', True, all(tp.usable(state, p) for p in state.typed_proofs))
    check('obligation_Proof', 'PROVED', gates.obligation_proof(state, state.evidence_requirements[0].id).state.value)
    check('ResumeEligibility_after_completion', False, core.resume_eligibility(bundle, ROOT).allowed)
    records = [{'id': uid(r.id), 'type': install.descriptor(r.request.definition)[0]['definition_type'],
                'current': install.current(bundle, r)} for r in state.installed_definitions]
    check('required_active_definitions_current', True,
          all(row['current'] for row in records if row['type'] != 'EXTERNAL_RESOLUTION_CONTRACT'))
    route_record = next(r for r in state.installed_definitions
                        if install.descriptor(r.request.definition)[0]['definition_type'] == 'EXTERNAL_RESOLUTION_CONTRACT')
    route_descriptor, original_route = install.descriptor(route_record.request.definition)
    route_gate = next(g for g in state.external_gates if g.id == original_route.gate)
    check('retained_route_stage', expected['retained_route_oracle']['gate_stage'], route_gate.stage.value)
    check('retained_route_acquisition_applicability', expected['retained_route_oracle']['installation_current'],
          install.current(bundle, route_record))
    check('retained_route_support_integrity', expected['retained_route_oracle']['support_current'],
          install.route_support_current(state, original_route))
    check('retained_route_body_exact', True, original_route in route_gate.resolution_contracts)
    new = bundle.events[9:]
    check('P04_sequence', expected['P04_sequence'], [type(e.result).__name__ for e in new])
    check('authorized_deferred_INSTALL_boundaries', [16, 18],
          [e.sequence for e in new if type(e.result) is m.InstallDefinition])
    check('full_presealed_native_semantics', sealed, actual_semantic)
    check('event_parent_chain', True, all(e.parent_event == bundle.events[pos-1].identity
                                       for pos, e in enumerate(bundle.events) if pos))
    check('event_state_continuity', True, all(e.parent_snapshot == bundle.events[pos-1].after_snapshot
                                           for pos, e in enumerate(bundle.events) if pos))
    result = {'RESULT': 'PASS' if all(v['pass'] for v in checks.values()) else 'FAIL',
              'operation': 'READ_ONLY_P05_ENTRY_INSPECTION', 'P05_EXECUTED': 'NO', 'P06_EXECUTED': 'NO',
              'pid': os.getpid(), 'pid_namespace': os.readlink('/proc/self/ns/pid'),
              'bundle_trust': 'PASS', 'cold_restore': 'PASS', 'native_historical_replay_inside_restore': 'PASS',
              'target_path': expected['entry_path'], 'target_raw_sha256': hashlib.sha256(target_path.read_bytes()).hexdigest(),
              'checks': checks, 'installed_definition_inventory': records,
              'current_snapshot': c._wire(state), 'full_native_Computation': actual_semantic,
              'historical_prefix_inventory': [{'sequence': e.sequence, 'id': uid(e.identity),
                                              'native_type': type(e.result).__name__} for e in bundle.events[:9]],
              'initial_context': c._wire(bundle.initial.context),
              'initial_completed_actions': sorted(s.id.value for s in bundle.initial.statuses
                                                  if s.state is m.ActionState.COMPLETED),
              'no_mutating_native_API_called': True}
    (OUT / 'target-inspection.json').write_bytes(c.canonical_bytes(result))
    print(json.dumps({'RESULT': result['RESULT'], 'entry_checks': len(checks),
                      'bundle': uid(c.bundle_id(bundle)), 'state': uid(c.snapshot_id(state)),
                      'control': comp.control.value, 'P05_EXECUTED': 'NO'}))
    if result['RESULT'] != 'PASS':
        raise SystemExit(1)


if __name__ == '__main__':
    main()
