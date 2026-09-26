"""Read-only authority provenance analysis; no enrollment/adoption implementation."""
import json, sys, time
from pathlib import Path
O = Path(__file__).resolve().parent
E = O.parent
pin = json.loads((E/'runtime_bootstrap_application_2026-09-19/AUTHORIZED_SELECTION.json').read_bytes())
sys.path.insert(0, pin['consumer_root'])
from adapter import runtime_adoption as r, runtime_bootstrap as b
from adapter.controller_authority_store import ControllerAuthorityStore, encoded, sha

begin = time.monotonic()
s = ControllerAuthorityStore(**pin['selected_store'])
try:
    p = r.policy(s)
    journals = [s.state_path(p[k]) for k in ('journal', 'bootstrap_journal')]
    baseline = {str(f): sha(f.read_bytes()) for f in journals}
    state = b.reconstruct(s)
    current = r.reconstruct(s)
    descriptor = r.descriptor(s, current['current_descriptor'], live=True)
    _, bootstrap, selector = b.verify_records(s)
    provenance = {'policy':p, 'bootstrap':bootstrap,
        'bootstrap_grant':r.read(s, selector['Architect_authorization']),
        'material_amendment':r.read(s,p['material_amendment']),
        'material_grant':r.read(s,p['material_decision']),
        'selected_adoptions':[]}
    for name in ('bootstrap_grant','material_grant'):
        provenance[name+'_source'] = r.read(s,provenance[name]['authority_source'])
    for pair in p['adoptions']:
        c = r.read(s,pair['continuation']); g = r.read(s,pair['grant'])
        provenance['selected_adoptions'].append({'continuation':c,'grant':g,
            'source':r.read(s,g['authority_source']), 'qualification':r.read(s,c['qualification'])})
    assert len(p['adoptions']) == len(p['qualified_evidence']) == 1
    assert current['continuations'] == [provenance['selected_adoptions'][0]['continuation']['id']]
    candidate_path = E/'runtime_c2_qualification_2026-09-19/CONTENT_CANDIDATE.json'
    c2 = json.loads(candidate_path.read_bytes())
    r.unseal('C2-CONTENT-CANDIDATE',c2)
    assert c2['predecessor'] == descriptor['identity']
    files = {f.name:sha(f.read_bytes()) for f in (Path(pin['consumer_root'])/'adapter').glob('*.py')}
    assert files == c2['successor_files']
    ref = {'authority_id':c2['id'],'sha256':sha(candidate_path.read_bytes())}
    # These are transition admission probes, not invented enrollment records.
    probes = {}
    for label, grant in [('candidate_without_grant', {'authority_id':'absent:C2-grant','sha256':'0'*64}),
                         ('candidate_with_C1_grant',p['adoptions'][0]['grant'])]:
        try:
            r.transition(s,p,ref,grant)
            raise AssertionError('unselected C2 admitted')
        except ValueError as exc:
            assert str(exc) == 'unselected adoption authority'
            probes[label] = str(exc)
    R = E/'run2_r12_dispatch_2026-09-18'
    historical = json.loads((R/'HISTORICAL_BASELINE.json').read_bytes())
    historical.update({str(R/k):v for k,v in json.loads((R/'EVIDENCE_HASHES.json').read_bytes()).items()})
    proof = json.loads((E/'run2_control_plane_binding_2026-09-18/R12_AUTHENTICATED_CAPTURE.json').read_bytes())
    historical[proof['publication']['path']] = proof['publication']['sha256']
    historical['/tmp/kge-forge-e1-invocations.jsonl'] = proof['terminal']['ledger_sha256']
    assert all(sha(Path(f).read_bytes()) == h for f,h in historical.items())
    assert baseline == {str(f):sha(f.read_bytes()) for f in journals}
    assert r.reconstruct(s)['current_runtime'] == descriptor['identity']
    evidence = {'verdict':'BLOCKED_NO_DELEGATED_FUTURE_ENROLLMENT_AUTHORITY',
        'provenance':provenance, 'candidate_identity':c2['id'], 'candidate_file_sha256':sha(candidate_path.read_bytes()),
        'candidate_runtime_identity':c2['successor'], 'current_runtime':descriptor['identity'],
        'head_event':current['head_event'], 'bootstrap_consumed':state['bootstrap_consumed'],
        'C2_qualification_identity':None,'enrollment_identity':None,'C2_adoption_decision':None,
        'admission_negative_probes':probes,
        'enrollment_tests':'NOT_RUN_NO_LEGITIMATE_AUTHORITY_OR_MECHANISM',
        'qualified_C2_without_enrollment_test':'NOT_CLAIMED_C2_HAS_NO_COMPLETE_QUALIFICATION_IDENTITY',
        'historical_files_verified':len(historical),'journal_hashes_unchanged':baseline,
        'seconds':time.monotonic()-begin,'real_model_requests':0,'E1_effects':0}
    with (O/'EVIDENCE.json').open('xb') as f: f.write(encoded(evidence))
    print(json.dumps({k:v for k,v in evidence.items() if k!='provenance'},indent=2))
finally:
    s.close()
