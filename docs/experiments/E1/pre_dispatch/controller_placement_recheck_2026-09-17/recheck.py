"""Bounded read-only E1 recheck; synthetic tool denials never use E1 identity.

This is evidence collection, not a relocation implementation or activation entrypoint.
No model transport, supervisor launch, or activation mutation is called.
Run from the repository root with PYTHONPATH=.
"""
import fcntl
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from adapter.context_projection import canonical, digest, sha, read_exact, derive
from adapter.governance_continuation import GovernanceContinuation, reference
from adapter.context_binding import CommittedContext
from adapter.governed_host import WorkAuthorization, GovernedHost, Denied
from adapter.authorization_lifecycle import dispatch_binding, historical_original, reconstruct
from adapter.activation_transaction import validate_production, invocation, _host
from adapter.execution_snapshot import construct, SnapshotDenied

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / 'docs/experiments/E1/pre_dispatch'
OUT = Path(__file__).resolve().parent
ADOPTION = BASE / 'complete_continuation_adoption_2026-09-16'
PLACEMENT = BASE / 'controller_artifact_placement_2026-09-16'


def load(path):
    return json.loads(Path(path).read_bytes())


def rebuild():
    record = load(ADOPTION / 'ADOPTION_RECORD.json')
    for ref in record['durable_inputs']:
        read_exact(ref['path'], ref['sha256'])
    spec = load(ADOPTION / 'ADOPTED_SPECIFICATION.json')
    governance = GovernanceContinuation(spec)
    op = load(ADOPTION / 'OPERATIONAL_BINDING.json')
    launch = json.loads(read_exact(**{'path': op['released_launch']['path'],
                                     'expected': op['released_launch']['sha256']}))
    context = CommittedContext(BASE / 'CONTEXT_MANIFEST.json',
        launch['authorization']['context_binding']['capture_commit'], spec)
    derived = derive(json.loads(launch['authorization']['context_projection']), context)
    assert all(derived[k] == v for k, v in op['context_identities'].items())
    assert derived['projection']['payload'] == governance.anchor_projection['payload']
    dispatch = reference(BASE / 'dispatch_authorization_2026-09-16/DISPATCH_RECORD.json')
    decision = load(dispatch['path'])
    audit = Path(decision['all_authorized_bindings']['audit'])
    issued = next(json.loads(line)['authorization'] for line in audit.read_text().splitlines()
                  if json.loads(line).get('event') == 'authorization_issued')
    raw = dict(issued, context_binding=context, operational_binding=canonical(op))
    for key in ('read_roots', 'write_roots', 'deny_roots', 'exec_bins',
                'read_deny_roots', 'write_deny_roots', 'write_directory_roots'):
        raw[key] = tuple(raw[key])
    raw['exec_argv_allowlist'] = tuple(tuple(x) for x in raw['exec_argv_allowlist'])
    auth = WorkAuthorization(**raw)
    assert historical_original(auth) == issued
    binding = dispatch_binding(auth, audit, dispatch)
    return auth, audit, dispatch, binding


def denied(call, types=(ValueError, RuntimeError, Denied, OSError)):
    try:
        call()
    except types as exc:
        return {'result': 'DENIED', 'exception': type(exc).__name__, 'reason': str(exc)}
    raise AssertionError('expected fail-closed denial')


def main():
    # Fingerprint every production source before any qualification; never edit them.
    implementation = {str(p): sha(p.read_bytes()) for p in (ROOT / 'adapter').glob('*.py')}
    auth, audit, dispatch, inheritance = rebuild()
    op = json.loads(auth.operational_binding)
    ledger = Path(auth.ownership_ledger)
    preserved = [audit, ledger, Path(dispatch['path']),
                 ADOPTION / 'OPERATIONAL_BINDING.json', ADOPTION / 'ADOPTION_RECORD.json',
                 Path(op['governance']['released_profile']['path'])]
    before = {str(p): sha(p.read_bytes()) for p in preserved}
    materialized = load(PLACEMENT / 'MATERIALIZATION.json')
    copy = Path(materialized['OperationalProfileLocation'])
    profile_ref = op['governance']['released_profile']
    exact = read_exact(str(copy), profile_ref['sha256'])
    assert exact == read_exact(profile_ref['path'], profile_ref['sha256'])
    profile = json.loads(exact)
    runtime = profile['runtime']
    roots = sorted(set((*auth.read_roots, *auth.write_roots,
                        *auth.write_directory_roots, runtime['cwd'],
                        *(str(Path(runtime['cwd']) / p) for p in runtime['inputs']))))

    def outside(path):
        p = Path(path)
        assert p.is_absolute() and p.resolve() == p and not p.is_symlink()
        return all(p != Path(r) and Path(r) not in p.parents for r in roots)

    inventory = []
    for row in materialized['inventory']:
        old, new = row['historical_reference'], row['controller_copy']
        assert read_exact(new['path'], new['sha256']) == read_exact(old['path'], old['sha256'])
        inventory.append({'historical_reference': old, 'controller_copy': new,
                          'historical_location_inside_grant': not outside(old['path']),
                          'copy_outside_all_roots': outside(new['path']),
                          'operationally_bound': False})
    # Production validation additionally consumes the original provisioning
    # receipt. An archival blob of its bytes is not an operational binding.
    basis_ref = op['governance']['release_basis']
    basis = json.loads(read_exact(basis_ref['path'], basis_ref['sha256']))
    receipts = [{'path': p, 'sha256': r['sha256']} for p, r in
                basis.get('current_inputs', basis.get('inputs')).items()
                if r['sha256'] == profile['provisioning_receipt_sha256']]
    assert len(receipts) == 1
    receipt_ref = receipts[0]
    receipt_copy = copy.parent / receipt_ref['sha256']
    assert read_exact(str(receipt_copy), receipt_ref['sha256']) == read_exact(
        receipt_ref['path'], receipt_ref['sha256'])
    if not any(r['historical_reference'] == receipt_ref for r in inventory):
        inventory.append({'historical_reference': receipt_ref,
                          'controller_copy': reference(receipt_copy),
                          'historical_location_inside_grant': not outside(receipt_ref['path']),
                          'copy_outside_all_roots': outside(receipt_copy),
                          'operationally_bound': False,
                          'discovery': 'additional direct production activation input'})
    # No production controller or E1 tool is constructed for boundary probes.
    # A separate synthetic identity uses the released path grants only.
    with tempfile.TemporaryDirectory(prefix='e1-placement-recheck-') as directory:
        synthetic_root = Path(directory)
        synthetic = WorkAuthorization('synthetic-placement', 1, 'SYNTHETIC',
            'synthetic-session', 'synthetic-turn', read_roots=auth.read_roots,
            write_roots=auth.write_roots, deny_roots=auth.deny_roots,
            read_deny_roots=auth.read_deny_roots, write_deny_roots=auth.write_deny_roots,
            write_directory_roots=auth.write_directory_roots)
        host = GovernedHost(synthetic, synthetic_root / 'audit.jsonl')
        private_repo, relative = str(copy.parent), copy.name
        probes = {
            'read': denied(lambda: host.governed_read(private_repo, relative)),
            'list': denied(lambda: host.governed_list(private_repo, '.')),
            'search': denied(lambda: host.governed_search(private_repo, '.', 'schema')),
            'write': denied(lambda: host.governed_write(private_repo, relative, 'SUBSTITUTION')),
            'patch': denied(lambda: host.governed_patch(private_repo,
                [{'op': 'write', 'path': relative, 'content': 'SUBSTITUTION'}])),
            'read_absolute_escape': denied(lambda: host.governed_read(str(ROOT), str(copy))),
        }
        def snapshot(source, inputs):
            return construct(source, inputs, lambda p: host._path(str(source), p),
                             synthetic_root, 'synthetic-denied')
        probes['snapshot_absolute_input'] = denied(lambda: snapshot(ROOT, [str(copy)]))
        probes['snapshot_private_source_root'] = denied(lambda: snapshot(copy.parent, [copy.name]))
        # Never substitute real released bytes, even temporarily.
        substituted = synthetic_root / 'substituted-profile.json'
        substituted.write_bytes(exact + b'\n')
        probes['substituted_bytes'] = denied(lambda: read_exact(str(substituted), profile_ref['sha256']))
        child = subprocess.run([sys.executable, '-c',
            'from adapter.context_projection import read_exact,sha; import sys; '
            'print(sha(read_exact(sys.argv[1],sys.argv[2])))', str(copy), profile_ref['sha256']],
            cwd=ROOT, capture_output=True, text=True, check=True)
        assert child.stdout.strip() == profile_ref['sha256']

    # Re-test existing location-only candidate in memory, without changing issuance.
    candidate = json.loads(canonical(op['governance']))
    candidate['released_profile'] = {'path': str(copy), 'sha256': profile_ref['sha256']}
    relocation = denied(lambda: GovernanceContinuation(candidate))
    # Read-only production validation under the same three locks; no durable intent,
    # audit append, ownership reservation, or transaction activation is requested.
    fds = []
    try:
        for path in (Path(str(ledger) + '.controller-lock'), ledger, audit):
            fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
            fds.append(fd)
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        production = denied(lambda: validate_production(auth, audit, dispatch, fds[1]))
        state = reconstruct(audit.read_bytes(), auth, audit)
        owner = invocation(fds[1])
        assert state['state'] == 'INACTIVE' and not state['uncertain'] and owner is None
    finally:
        for fd in reversed(fds):
            os.close(fd)
    # This is a separate unchanged production prerequisite, not a claim that the
    # complete validator reached the host check after its placement denial.
    host_check = denied(lambda: _host(profile['supervisor_binding'][0]))
    after = {str(p): sha(p.read_bytes()) for p in preserved}
    assert before == after
    assert implementation == {str(p): sha(p.read_bytes()) for p in (ROOT / 'adapter').glob('*.py')}
    assert read_exact(str(copy), profile_ref['sha256']) == exact
    audit_events = [json.loads(line)['event'] for line in audit.read_text().splitlines()]
    assert set(audit_events) <= {'authorization_issued', 'context_projection_verified',
                                'controller_reconstructed'}
    report = {
        'result': 'BLOCKED', 'E1': 'INACTIVE', 'E1_WP_001': 'INELIGIBLE_AND_UNDISPATCHED',
        'authorization_id': auth.authorization_id,
        'ReleasedProfileContentId': profile_ref['sha256'],
        'canonical_profile_fingerprint': digest(profile),
        'candidate_OperationalProfileLocation': str(copy),
        'profile_copy_bytes_identical': True, 'candidate_outside_all_roots': outside(copy),
        'authority_roots_examined': roots,
        'materialized_reference_count': len(inventory),
        'placement_defect_count': sum(r['historical_location_inside_grant'] for r in inventory),
        'inventory': inventory,
        'mutable_controller_locations': {str(p): {'outside_roots': outside(p)} for p in
            (audit, ledger, Path(str(ledger) + '.controller-lock'))},
        'synthetic_boundary_probes': probes,
        'independent_copy_load_sha256': child.stdout.strip(),
        'location_only_candidate': relocation,
        'operational_continuation': None,
        'current_operational_identities': op['governance']['identities'],
        'current_context_identities': op['context_identities'],
        'existing_dispatch_inheritance': {'result': 'PASS', 'binding': inheritance},
        'production_activation_validation': production,
        'separate_released_host_prerequisite': host_check,
        'expected_supervisor': profile['supervisor_binding'][0],
        'independent_current_lifecycle': state,
        'ownership_reservation': owner, 'activation_event': None,
        'model_handoff_eligible': False,
        'qualification_limits': [
            'No content-versus-location binding mechanism implemented or adopted.',
            'Independent child loaded exact candidate bytes, not a relocated operational binding.',
            'No payload execution or live QUIESCENT regression: released supervisor absent.',
            'Other copied controller inputs remain unbound.',
            'Complete ten-point relocation qualification is not satisfied.',
        ],
        'preserved_fingerprints': after, 'production_implementation_unchanged': True,
        'E1_model_requests_this_step': 0, 'E1_implementation_effects_this_step': 0,
        'E1_audit_event_names': sorted(set(audit_events)),
        'E1_model_requests_total': 0, 'E1_implementation_effects_total': 0,
    }
    (OUT / 'RECHECK.json').write_text(canonical(report) + '\n')
    print(canonical({k: report[k] for k in ('result', 'profile_copy_bytes_identical',
        'materialized_reference_count', 'placement_defect_count', 'location_only_candidate',
        'production_activation_validation', 'separate_released_host_prerequisite',
        'model_handoff_eligible')}))


if __name__ == '__main__':
    main()
