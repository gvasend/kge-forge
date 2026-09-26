"""Fresh-process qualified terminal recovery; no effects or model continuation."""
import json,os,time
from pathlib import Path
from adapter.context_projection import canonical,sha
from adapter.controller_authority_store import ControllerAuthorityStore,_directory,_read,_put
from adapter.authority_bootstrap import reconstruct_authorization
from adapter.activation_transaction import ActivationTransaction
AUTH='auth-e1-wp-001-r7-94f511dfcdcc43ac837191f8732ced39'
BASE=Path('/tmp/kge-forge-controller-authority')/AUTH
OUT=BASE/'e1-programmer-dispatch-2026-09-17'
assert (OUT/'TERMINATION_RESULT.json').exists()
p=BASE/'supervisor-succession-adoption-2026-09-17/SUCCESSION_PUBLICATION.json'
fd=_directory(p.parent)
try:data=_read(fd,p.name)
finally:os.close(fd)
assert sha(data)=='95a2454b094f2b6e4af044cbfa8a8efd98a225866e2b19fc286a2d63abdacd4e'
store=ControllerAuthorityStore(**json.loads(data)['selected_store']);tx=None
try:
 with store.session():
  auth=reconstruct_authorization(store,AUTH);audit=store.state_path(AUTH+':audit')
  op=json.loads(auth.operational_binding)
  d=json.loads(store.resolve('sha256:'+op['governance']['material_release']['dispatch_amendment']['sha256']))
  ref='E1-ARCHITECT-DISPATCH-sha256:'+d['original_dispatch']['sha256']
  print('Independent terminal reconstruction started',flush=True)
  tx=ActivationTransaction.recover(auth,audit,ref)
  assert tx.recovery['lifecycle_state']=='CANCELLED'
  assert tx.recovery['ownership'] is None and not tx.recovery['handoff_eligible']
  assert not tx.recovery['reconciliation_required']
  assert tx.ownership.active() is None
  value={'result':'PASS','recovery':tx.recovery,'execution_ownership':None,'classification':'INTERRUPTED_NO_EFFECTS','time_unix_ns':time.time_ns(),'audit_sha256':sha(audit.read_bytes())}
  data=canonical(value).encode();fd=_directory(OUT)
  try:_put(fd,'TERMINATION_INDEPENDENT_RECOVERY.json',data);os.fsync(fd)
  finally:os.close(fd)
  print(canonical(value),flush=True)
finally:
 if tx:tx.close()
 store.close()
