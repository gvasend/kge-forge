"""Read-only E2-P04 pin/oracle preflight; never repairs or advances a fixture."""
import dataclasses
from enum import Enum
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

from adapter.planner import codec as c, core, model as m

ROOT = Path(__file__).resolve().parents[2]
D = ROOT / 'docs/plans'
P = 'DETERMINISTIC_PLANNER_V0_1_'
BUNDLE = D / (P + 'P03_PROSPECTIVE_CHECKPOINT_BUNDLE_1.json')
EXPECTED = m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY,
    'planner-bundle-v1', 'd1944fe18626778bebfc6c7693c7bdb5303e079668683e5fb99676ecbe46b859')
OUT = D / 'qualification/E2_P04_PREFLIGHT_1'


def serial(x):
    if isinstance(x, Enum):
        return {'type': type(x).__name__, 'value': x.value}
    if dataclasses.is_dataclass(x):
        return {f.name: serial(getattr(x, f.name)) for f in dataclasses.fields(x)}
    if isinstance(x, (tuple, list)):
        return [serial(y) for y in x]
    if isinstance(x, dict):
        return {k: serial(v) for k, v in x.items()}
    return x


def hashes():
    # Existing runtime, frozen E1, and every prior plan artifact are preserved.
    paths = list((ROOT / 'adapter/planner').rglob('*.py'))
    paths += [p for p in (ROOT / 'docs/experiments/E1').rglob('*') if p.is_file()]
    paths += [p for p in D.rglob('*') if p.is_file() and OUT not in p.parents
              and p.name not in (P+'E2_P04_RESULT.md', P+'E2_P04_RESULT.json')]
    return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(paths)}


def load_view():
    b = c.restore(BUNDLE, EXPECTED, ROOT)
    computation = core.recompute(b.current)
    return b, {'snapshot': c._wire(b.current),
        'snapshot_id': c._wire(c.snapshot_id(b.current)),
        'bundle_id': c._wire(c.bundle_id(b)),
        'source_pins': sorted(c._wire(b.sources), key=c.canonical_bytes),
        'policy': c._wire(b.policy), 'policy_version': b.policy_version,
        'events': c._wire(b.events), 'computation': serial(computation),
        'resume': c._wire(core.resume_eligibility(b, ROOT))}


def run():
    before = hashes()
    b, view = load_view()
    oracle_path = D / 'qualification/P03_PROSPECTIVE_CHECKPOINT_1/mainline-oracle.json'
    oracle = json.loads(oracle_path.read_text())
    initial = {
        'complete_snapshot': c.snapshot_bytes(b.current) == c.snapshot_bytes(c._unwire(oracle['checkpoint'])),
        'source_pins': view['source_pins'] == sorted(oracle['pins'], key=c.canonical_bytes),
        'policy': c._wire(b.policy) == oracle['policy'],
        'scope_lineage': c._wire(b.current.context) == oracle['context'],
        'control_external_wait': core.recompute(b.current).control is m.ControlState.EXTERNAL_WAIT,
        'no_actionable': not core.recompute(b.current).actionable,
        'no_receipt': not b.current.receipt_observations and not b.current.receipt_admissions,
        'no_resume': not core.resume_eligibility(b, ROOT).allowed,
        'native_replay': c.snapshot_bytes(c._replay(b)) == c.snapshot_bytes(b.current),
    }
    assert all(initial.values()), initial
    readers = []
    for seed in (0, 1, 7, 101):
        for repetition in range(3):
            result = subprocess.run([sys.executable, str(Path(__file__)), 'reader'],
                cwd=str(ROOT), env=dict(os.environ, PYTHONPATH=str(ROOT),
                PYTHONDONTWRITEBYTECODE='1', PYTHONHASHSEED=str(seed)),
                capture_output=True, text=True)
            assert result.returncode == 0, result.stderr
            fresh = json.loads(result.stdout)
            assert fresh['view'] == view
            readers.append({'seed': seed, 'repetition': repetition,
                'pid': fresh['pid'], 'exit_status': result.returncode,
                'full_view_equal': True, 'domains': ['canonical_snapshot',
                'canonical_bundle', 'semantic_state', 'source_pins', 'policy_pins',
                'scope_lineage', 'provenance', 'event_ancestry', 'control', 'resume'],
                'input_allowlist': ['pinned_bundle', 'its_event_files',
                'its_physical_source_and_policy_files', 'native_runtime'],
                'expected_oracle_not_reader_input': True})
    candidate_path = D / (P + 'E2_P03_SEMANTIC_NATIVE_EVIDENCE_BINDING_1_CANDIDATE.json')
    a = c._unwire(json.loads(candidate_path.read_text()))
    try:
        core.apply_event(b.current, a)
    except m.PlannerError as exc:
        rejection = str(exc)
    else:
        raise AssertionError('Historical candidate unexpectedly admitted')
    assert rejection == 'PARENT_MISMATCH', rejection
    assert load_view()[1] == view
    contract = json.loads((D / (P+'CANONICAL_QUALIFICATION_EXPERIMENT_1.json')).read_text())
    package = next(x for x in contract['packages'] if x['id'] == 'E2-P04')
    cases = [x for x in contract['cases'] if x['CASE_ID'] in package['cases']]
    entities = {e.id for e in b.current.entities}
    predicates = {p.id for p in b.current.predicates}
    reenter = next(x for x in b.current.actions if x.id.value == 'E2-REENTER')
    missing = {
        'candidate_expected_bundle_matches': a.expected_bundle == c.bundle_id(b),
        'candidate_expected_snapshot_matches': a.expected_snapshot == c.snapshot_id(b.current),
        'candidate_expected_parent_event_matches': a.expected_parent_event == b.events[-1].identity,
        'candidate_authentication_predicate_present': a.admission.authentication in predicates,
        'at_least_one_native_ATTEST_authority': any(m.AuthorityClass.ATTEST in e.permissions for e in b.current.entities),
        'REENTER_declared_output_materialized': bool(reenter.accepted_inventory),
        'REENTER_pass_model_complete': reenter.pass_model_complete,
        'E2_SLOT_definition_present': any(s.id.value == 'E2-SLOT' for s in b.current.slots),
        'typed_proof_contracts_present': bool(b.current.proof_contracts),
    }
    after = hashes()
    assert before == after, 'preserved artifacts changed'
    OUT.mkdir(parents=True, exist_ok=True)
    result = {'schema': 'E2-P04-READ-ONLY-PREFLIGHT-1', 'result': 'BLOCKED',
        'interpreter': sys.version, 'writer_pid': os.getpid(),
        'package_contract': package, 'owned_cases': cases,
        'initial_oracle_source': str(oracle_path.relative_to(ROOT)),
        'initial_oracle': initial, 'initial_view': view,
        'fresh_readers': readers, 'applicable_input_checks': missing,
        'historical_candidate_rejection': {'candidate': str(candidate_path.relative_to(ROOT)),
            'expected_bundle': c._wire(a.expected_bundle),
            'actual_bundle': c._wire(c.bundle_id(b)),
            'expected_snapshot': c._wire(a.expected_snapshot),
            'actual_snapshot': c._wire(c.snapshot_id(b.current)),
            'expected_parent_event': c._wire(a.expected_parent_event),
            'actual_parent_event': c._wire(b.events[-1].identity),
            'native_reason': rejection, 'accepted_event': False,
            'canonical_state_unchanged': True},
        'execution_trace': [], 'accepted_P04_events': 0,
        'historical_candidate_is_not_prospective_fixture': True,
        'preserved_file_hashes': before, 'preservation_equal': before == after,
        'runtime_modified': False, 'E1_artifacts_modified': 0}
    (OUT / 'preflight.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'result': 'BLOCKED', 'readers_pass': len(readers),
        'oracle': initial, 'missing_checks': missing, 'rejection': rejection}))


if __name__ == '__main__':
    if sys.argv[1:] == ['reader']:
        print(json.dumps({'pid': os.getpid(), 'view': load_view()[1]}))
    else:
        run()
