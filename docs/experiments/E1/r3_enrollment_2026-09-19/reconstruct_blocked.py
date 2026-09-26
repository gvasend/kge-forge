"""Read-only independent reconciliation after rejected enrollment intake."""
import json,sys,time
from pathlib import Path
O=Path(__file__).resolve().parent;pin=json.loads((O/'AUTHORIZED_ENROLLMENT_SELECTION.json').read_bytes());sys.path.insert(0,pin['consumer_root'])
from adapter import runtime_adoption as r,runtime_bootstrap as b
from adapter.controller_authority_store import ControllerAuthorityStore,encoded,sha
base=ControllerAuthorityStore(**pin['base_store']);state=r.reconstruct(base);bootstrap=b.reconstruct(base);policy=r.policy(base)
root=Path(pin['enrollment_module']).parent
checks={path:sha(Path(path).read_bytes())==h for path,h in pin['baseline'].items()}
assert all(checks.values());assert state['current_runtime']==pin['R1'] and state['pending'] is None
assert (root/'enrollment.jsonl').read_bytes()==b''
assert not (root/'ENROLLMENT_INTENT.json').exists() and not (root/'ENROLLMENT_RESULT.json').exists()
try:
 r.validate_invocation_runtime(base,dict(pin['base_binding'],runtime=pin['runtime']['identity']),pin['runtime']['root'])
 raise AssertionError('unadopted R3 accepted')
except ValueError as exc:rejection=str(exc)
_,record,_=b.verify_records(base);b.fresh_supervisor(base,record)
out={'verdict':'BLOCKED_ENROLLMENT_EVIDENCE_REPRESENTATION','independent_reconstruction':'PASS','R1':state['current_runtime'],'head':state['head_event'],'runtime_head_authority':policy['id'],'bootstrap_state':bootstrap['state'],'bootstrap_unchanged':True,'baseline_checks':checks,'enrollment_records':0,'enrollment_journal_sha256':sha((root/'enrollment.jsonl').read_bytes()),'intent_exists':False,'R3_enrolled':False,'R3_adopted':False,'R3_current':False,'production_R3_rejection':rejection,'S3':'READY','real_model_requests':0,'E1_effects':0,'r13_created':False,'failure':'Qualification attestation referenced raw Markdown report/instruction bytes. Qualified evidence reader requires JSON objects; JSONDecodeError before enrollment intent or append. No retry.'}
with (O/'BLOCKED_RECONSTRUCTION.json').open('xb') as f:f.write(encoded(out))
base.close();print(json.dumps(out,indent=2))
