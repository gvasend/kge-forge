"""Freeze documentary qualification output. No production authority mutation."""
import json, sys, time
from pathlib import Path
O=Path(__file__).resolve().parent;sys.path.insert(0,str(O))
import test_enrollment as t
from adapter.controller_authority_store import encoded,sha
from adapter import runtime_adoption as r
log=Path('/tmp/a2_1i-tests-locked.log').read_bytes()
assert b'\nOK\n' in log and b'FAILED' not in log
f=t.Fixture()
try:
 begin=time.monotonic();row=f.enroll();elapsed=time.monotonic()-begin
 assert f.eligible(row)==row
 prior=json.loads((O.parent/'a2_1i_enrollment_2026-09-19/EVIDENCE.json').read_bytes())
 assert all(sha(Path(p).read_bytes())==h for p,h in prior['journal_hashes_unchanged'].items())
 R=O.parent/'run2_r12_dispatch_2026-09-18'
 historical=json.loads((R/'HISTORICAL_BASELINE.json').read_bytes())
 historical.update({str(R/k):v for k,v in json.loads((R/'EVIDENCE_HASHES.json').read_bytes()).items()})
 proof=json.loads((O.parent/'run2_control_plane_binding_2026-09-18/R12_AUTHENTICATED_CAPTURE.json').read_bytes())
 historical[proof['publication']['path']]=proof['publication']['sha256']
 historical['/tmp/kge-forge-e1-invocations.jsonl']=proof['terminal']['ledger_sha256']
 assert all(sha(Path(p).read_bytes())==h for p,h in historical.items())
 state=r.reconstruct(f.base)
 assert state['current_runtime']==prior['current_runtime'] and state['head_event']==prior['head_event']
 sample={'binding_kind':'QUALIFICATION_BINDING','not_production_authority':True,
   'private_store_pin':f.pin,'delegation':f.d,'candidate':f.c,'qualification':f.q,'decision':f.g,
   'enrollment':row,'enrollment_seconds':elapsed,
   'qualification_scope':'SYNTHETIC_ENROLLMENT_CONTRACT_ONLY_NOT_COMPLETE_C2_RUNTIME_QUALIFICATION'}
 output={'verdict':'ENROLLMENT_COMPONENT_QUALIFICATION_PASS',
   'production_capability_adopted':False,'production_C2_enrolled':False,'production_R2_adopted':False,
   'current_R1':state['current_runtime'],'current_head':state['head_event'],
   'runtime_head_authority':f.d['lineage'],
   'mechanism_sha256':sha(Path(t.en.__file__).read_bytes()),
   'Architect_delegation_source_sha256':sha((O/'ARCHITECT_DELEGATION_SOURCE.md').read_bytes()),
   'tests_log_sha256':sha(log),'historical_preservation_files':len(historical),
   'authority_journals_unchanged':prior['journal_hashes_unchanged'],
   'sample_qualification_enrollment_identity':row['id'],
   'R2_readiness':'NOT_ESTABLISHED_ORDINARY_ADOPTION_INTEGRATION_NOT_QUALIFIED',
   'real_model_requests':0,'E1_effects':0}
 destination=O/'head_locked';destination.mkdir()
 for name,data in [('TESTS.log',log),('ISOLATED_SAMPLE.json',encoded(sample)),('PUBLICATION.json',encoded(output))]:
  with (destination/name).open('xb') as stream:stream.write(data)
 print(json.dumps(output,indent=2))
finally:f.close()
