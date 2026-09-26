"""Exact sealed prepared store, full production predicate, no issuance."""
import json,sys,os,time,signal,cProfile,pstats
from pathlib import Path
O=Path(__file__).parent;pin=json.loads((O/'CURRENT_PIN.json').read_bytes());b=Path(pin['path']).read_bytes()
import hashlib
assert hashlib.sha256(b).hexdigest()==pin['sha256'];pub=json.loads(b);sys.path.insert(0,pub['runtime_root'])
from adapter.controller_authority_store import ControllerAuthorityStore
from adapter.authority_bootstrap import reconstruct_authorization
from adapter.activation_transaction import _validate_production,invocation
from adapter.invocation_ownership import InvocationOwnership
from adapter.context_projection import canonical,sha
signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('120 second phase budget')))
s=ControllerAuthorityStore(**pub['selected_store'])
try:
 with s.session():
  signal.alarm(120);start=time.monotonic();a=reconstruct_authorization(s,pub['authorization_id']);bootstrap=time.monotonic()-start
  signal.alarm(120);before=Path(a.ownership_ledger).read_bytes();own=InvocationOwnership(a.ownership_ledger);fd=own._locked()
  start=time.monotonic();wall=time.time()
  try:
   assert invocation(fd) is None and own._history(fd) is None
   prof=cProfile.Profile();prof.enable()
   result=_validate_production(a,Path(pub['audit']),pub['dispatch'],fd,_preissuance=True)
  finally:
   prof.disable();prof.dump_stats(str(O/"BASELINE_PROFILE.pstats"));os.close(fd)
  duration=time.monotonic()-start;signal.alarm(0)
  assert not Path(pub['audit']).exists() and not Path(pub['audit']).parents[2].exists()
  assert before==Path(a.ownership_ledger).read_bytes()
  value={'schema':'NON_AUTHORIZING_SEALED_STORE_PREFLIGHT-1','result':'PASS','publication':pin,'runtime_identity':pub['controller_runtime_identity'],
   'bootstrap_seconds':bootstrap,'validation_seconds':duration,'monotonic_start':start,'wall_start':wall,
   'soft_warning':duration>=30,'hard_exceeded':duration>=120,'soft_seconds':30,'hard_seconds':120,
   'production_result':result,'ledger_sha256':sha(before),'audit_unused':True,'issued':False,'activated':False,'model_requests':0,'effects':0}
  (O/'BASELINE_PREFLIGHT.json').write_text(canonical(value));print(canonical({'result':'PASS','validation_seconds':duration,'soft_warning':duration>=30}))
finally:signal.alarm(0);s.close()
