"""Read-only production authority check. Never calls adoption or bootstrap mutation."""
import json, sys, time
from pathlib import Path

O = Path(__file__).resolve().parent
E = O.parent
selection = json.loads((E/'runtime_bootstrap_application_2026-09-19/AUTHORIZED_SELECTION.json').read_bytes())
sys.path.insert(0, selection['consumer_root'])
from adapter import runtime_adoption as r, runtime_bootstrap as b
from adapter.controller_authority_store import ControllerAuthorityStore, encoded, sha

start = time.monotonic()
s = ControllerAuthorityStore(**selection['selected_store'])
try:
    p = r.policy(s)
    paths = [s.state_path(p[key]) for key in ('journal', 'bootstrap_journal')]
    before = {str(path): sha(path.read_bytes()) for path in paths}
    t = time.monotonic()
    state = b.reconstruct(s)
    current = r.reconstruct(s)
    d = r.descriptor(s, current['current_descriptor'], live=True)
    reconstruction_seconds = time.monotonic()-t
    assert d['identity'] == 'sha256:1b31ac92d38952444076e3997083cf035e0862f1bc0182261826d6690ec31c15'
    assert state['bootstrap_consumed'] and current['pending'] is None
    files = {f.name: sha(f.read_bytes()) for f in (Path(selection['consumer_root'])/'adapter').glob('*.py')}
    delta = [{'path': n, 'old_sha256': d['files'].get(n), 'new_sha256': files.get(n)} for n in sorted(set(d['files']) | set(files)) if d['files'].get(n) != files.get(n)]
    candidate = {'schema': 'C2-CONTENT-CANDIDATE-1', 'status': 'BLOCKED_NOT_QUALIFIED_FOR_ADOPTION',
                 'predecessor': d['identity'], 'successor': 'sha256:'+sha(encoded(files)),
                 'successor_files': files, 'delta': delta, 'runtime_head_authority': p['id'],
                 'Architect_adoption_required': True,
                 'limitation': 'No established enrollment operation for a new continuation/qualification under this immutable runtime-head policy.'}
    candidate = r.seal('C2-CONTENT-CANDIDATE', candidate)
    (O/'CONTENT_CANDIDATE.json').write_bytes(encoded(candidate))
    # Exercise the real transition gate, without appending an intent or inventing approval.
    candidate_ref = {'authority_id': candidate['id'], 'sha256': sha(encoded(candidate))}
    missing_grant = {'authority_id': 'unissued:architect:C2', 'sha256': '0'*64}
    try:
        r.transition(s, p, candidate_ref, missing_grant)
        raise AssertionError('unselected continuation accepted')
    except ValueError as exc:
        rejection = str(exc)
    assert rejection == 'unselected adoption authority'
    _, record, _ = b.verify_records(s)
    assert record['runtime_head_authority'] == p['id']
    assert record['consumer_files'] == files
    selected = [r.read(s, a['continuation'])['id'] for a in p['adoptions']]
    assert selected == current['continuations']
    # A changed selection list necessarily changes the content-addressed authority.
    altered = {k:v for k,v in p.items() if k != 'id'}
    altered['adoptions'] = p['adoptions'] + [{'continuation': candidate_ref, 'grant': missing_grant}]
    assert r.seal('RUNTIME-HEAD-AUTHORITY', altered)['id'] != record['runtime_head_authority']
    t = time.monotonic()
    b.fresh_supervisor(s, record)
    supervisor_seconds = time.monotonic()-t
    Q = E/'run2_control_plane_binding_2026-09-18'
    R = E/'run2_r12_dispatch_2026-09-18'
    baseline = json.loads((R/'HISTORICAL_BASELINE.json').read_bytes())
    baseline.update({str(R/k):v for k,v in json.loads((R/'EVIDENCE_HASHES.json').read_bytes()).items()})
    proof = json.loads((Q/'R12_AUTHENTICATED_CAPTURE.json').read_bytes())
    baseline[proof['publication']['path']] = proof['publication']['sha256']
    baseline['/tmp/kge-forge-e1-invocations.jsonl'] = proof['terminal']['ledger_sha256']
    assert all(sha(Path(path).read_bytes()) == digest for path,digest in baseline.items())
    from adapter.attempt_chain import classify_terminal
    from adapter.run_control import events
    assert sha(Path(proof['terminal']['audit']).read_bytes()) == proof['terminal']['audit_sha256']
    classification = classify_terminal(events(proof['terminal']['audit']), proof['terminal'], proof['authorization']['authorization_id'], True)
    assert classification == 'ACTIVE_CANCELLED_PRE_MODEL_NO_EFFECTS'
    assert before == {str(path):sha(path.read_bytes()) for path in paths}
    result = {'verdict': 'BLOCKED_C2_ORDINARY_ADOPTION_ENROLLMENT', 'current_R1': d['identity'],
              'runtime_head_authority': p['id'], 'runtime_head': current['head_event'],
              'bootstrap_consumed': True, 'selected_continuations': selected,
              'qualified_evidence_count': len(p['qualified_evidence']),
              'candidate': candidate['id'], 'R2_content_identity': candidate['successor'], 'delta': delta,
              'unselected_C2_rejection': rejection, 'policy_extension_changes_bootstrap_bound_identity': True,
              'R2_adoption_and_self_selection': 'NOT_ESTABLISHED',
              'historical_files_verified':len(baseline), 'r12_safe_predecessor':classification,
              'S3':'READY_EXACT_EXCLUSIVE', 'reconstruction_seconds': reconstruction_seconds,
              'S3_verification_seconds':supervisor_seconds, 'total_seconds': time.monotonic()-start,
              'production_journals_before_and_after':before, 'real_model_requests':0, 'E1_effects':0,
              'production_adoption_performed':False}
    (O/'RESULT.json').write_bytes(encoded(result))
    print(json.dumps(result, indent=2))
finally:
    s.close()
