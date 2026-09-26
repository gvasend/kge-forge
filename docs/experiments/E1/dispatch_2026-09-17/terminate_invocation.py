"""One authorized cancellation; uses existing lifecycle, recovery and ledger primitives.
No model calls, supervisor launches, implementation changes, or retries.
"""
import json,os,time
from pathlib import Path
from adapter.context_projection import canonical,sha
from adapter.controller_authority_store import ControllerAuthorityStore,_directory,_read as private_read,_put
from adapter.authority_bootstrap import reconstruct_authorization
from adapter.activation_transaction import ActivationTransaction,invocation
from adapter.authorization_lifecycle import _read,_append
from adapter.recovery_ledger import reconstruct

AUTH='auth-e1-wp-001-r7-94f511dfcdcc43ac837191f8732ced39'
BASE=Path('/tmp/kge-forge-controller-authority')/AUTH
OUT=BASE/'e1-programmer-dispatch-2026-09-17'
def save(name,value):
    data=canonical(value).encode();fd=_directory(OUT)
    try:_put(fd,name,data);os.fsync(fd)
    finally:os.close(fd)
    print(name,flush=True)
    return {'path':str(OUT/name),'sha256':sha(data)}
pin=BASE/'supervisor-succession-adoption-2026-09-17/SUCCESSION_PUBLICATION.json'
fd=_directory(pin.parent)
try:data=private_read(fd,pin.name)
finally:os.close(fd)
assert sha(data)=='95a2454b094f2b6e4af044cbfa8a8efd98a225866e2b19fc286a2d63abdacd4e'
store=ControllerAuthorityStore(**json.loads(data)['selected_store']);tx=None
try:
 with store.session():
  save('TERMINATION_AUTHORIZATION.json',{'source':'Architect user-channel RUN-TERMINATION AUTHORIZATION','reason':'NO_OBSERVABLE_PROGRAMMER_PROGRESS / RESOURCE_BUDGET','authorization_id':AUTH,'scope':'Current invocation only; no release revocation, replacement, retry, or implementation change','recorded_time_unix_ns':time.time_ns()})
  assert not Path('/proc/1109889').exists(),'original controller still exists; stop'
  result=json.loads((OUT/'PROGRAMMER_RESULT.json').read_bytes())
  assert result['result']['status']=='INCOMPLETE' and result['finished'] is False
  auth=reconstruct_authorization(store,AUTH);audit=store.state_path(AUTH+':audit')
  op=json.loads(auth.operational_binding)
  amendment=json.loads(store.resolve('sha256:'+op['governance']['material_release']['dispatch_amendment']['sha256']))
  ref='E1-ARCHITECT-DISPATCH-sha256:'+amendment['original_dispatch']['sha256']
  tx=ActivationTransaction(auth,audit,ref) # exclusive controller fence prevents concurrent effects
  ledger,afd=tx._locks()
  try:
   recovery=reconstruct(audit,auth)
   assert recovery['scope'] is None and not recovery['incomplete']
   assert all(r['result']=='DENIED' for r in recovery['results'].values())
   assert tx.ownership._history(ledger) is None
   owner=invocation(ledger)
   assert owner['reservation_id']=='INVOCATION-RESERVATION-sha256:e5bd9403e16bcd61ce0bae40c31d300e8a8a94e4c266e26a705e5d6f0c8f7363'
   previous=recovery['authorization_lifecycle'];assert previous['state']=='ACTIVE'
   prefix=sha(_read(afd));ledger_prefix=sha(_read(ledger))
   _append(afd,{'event':'interruption_requested','scope_id':None,'reason':'NO_OBSERVABLE_PROGRAMMER_PROGRESS / RESOURCE_BUDGET','time':time.monotonic(),'time_unix_ns':time.time_ns(),'source':'Architect termination authorization'})
   _append(afd,{'event':'architectural_state','state':'QUIESCENT','scope':'NONE','interruption_requested':True,'time':time.monotonic(),'basis':'Original controller exited INCOMPLETE; recovery proves no ExecutionScope, no pending ActionRequest, no execution ownership; exclusive controller fence held'})
   terminal=tx._event(afd,previous,'terminal','CANCELLED',reason='NO_OBSERVABLE_PROGRAMMER_PROGRESS / RESOURCE_BUDGET',invocation_classification='INTERRUPTED_NO_EFFECTS',time_unix_ns=time.time_ns(),termination_authorization_sha256=sha((OUT/'TERMINATION_AUTHORIZATION.json').read_bytes()),programmer_result_sha256=sha((OUT/'PROGRAMMER_RESULT.json').read_bytes()))
   release={'event':'invocation_released','reservation_id':owner['reservation_id'],'terminal_event_id':terminal['event_id'],'reason':'Architect-authorized cancellation after no-scope recovery','time_unix_ns':time.time_ns()}
   _append(ledger,release)
   assert tx.ownership._history(ledger) is None and invocation(ledger) is None
   save('TERMINATION_RESULT.json',{'terminal':terminal,'release':release,'release_sha256':sha(canonical(release).encode()),'classification':'INTERRUPTED_NO_EFFECTS','scope':'NONE','architectural_state':'QUIESCENT','audit_prefix_sha256':prefix,'ledger_prefix_sha256':ledger_prefix,'audit_sha256':sha(_read(afd)),'ledger_sha256':sha(_read(ledger)),'provider_status':'Two responses completed before attempted signal; no outstanding request known; no provider cancellation sent','time_unix_ns':time.time_ns()})
  finally:os.close(afd);os.close(ledger)
finally:
 if tx:tx.close()
 store.close()
