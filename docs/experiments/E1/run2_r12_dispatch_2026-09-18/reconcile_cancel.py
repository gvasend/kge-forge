"""One cancellation-only recovery. Never constructs RunControl or reopens admission."""
import json,sys,os,time
from pathlib import Path
from dataclasses import replace
O=Path(__file__).parent;pin=json.loads((O/'CURRENT_PIN.json').read_bytes());b=Path(pin['path']).read_bytes();import hashlib
assert hashlib.sha256(b).hexdigest()==pin['sha256'];p=json.loads(b);sys.path.insert(0,p['runtime_root'])
from adapter.controller_authority_store import ControllerAuthorityStore,_directory,_put
from adapter.authority_bootstrap import reconstruct_authorization
from adapter.authorization_lifecycle import reconstruct
from adapter.activation_transaction import ActivationTransaction
from adapter.attempt_ownership import observe
from adapter.governed_host import GovernedHost
from adapter.recovery_ledger import reconstruct as recover_actions
from adapter.run_control import events
from adapter.validation_spans import recording
from adapter.context_projection import canonical,sha
s=ControllerAuthorityStore(**p['selected_store']);tx=None;begin=time.monotonic();audit=Path(p['audit']);B=Path(p['private_run_root'])
fd=os.open(B/'CANCELLATION_RECOVERY_STARTED',os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600);os.write(fd,canonical({'reason':'HARD_NO_PROGRESS_BUDGET_CANCELLATION_RECONCILIATION','wall_time':time.time(),'no_reopening':True}).encode());os.fsync(fd);os.close(fd)
try:
 with s.session(),recording(None):
  a=reconstruct_authorization(s,p['authorization_id']);before=audit.read_bytes();rows=events(audit)
  assert any(r.get('event')=='budget_exhausted' and r['details']['budget']=='no_progress' for r in rows)
  assert any(r.get('event')=='admission_closed' for r in rows)
  assert not any(r.get('event') in ('model_request_start','model_request_content_bound','action_request','execution_scope_created') for r in rows)
  life=reconstruct(before,a,audit);owner,scope,_=observe(a.ownership_ledger);actions=recover_actions(audit,a)
  assert life['state']=='ACTIVE' and not life['uncertain']
  assert owner==life['activation_event']['ownership_reservation'] and owner['authorization_id']==a.authorization_id
  assert scope is None and actions['scope'] is None and not actions['incomplete']
  tx=ActivationTransaction(a,audit,p['dispatch']['authority_id'])
  op=json.loads(a.operational_binding);op['dispatch_authorization']=p['dispatch']
  h=GovernedHost(replace(a,state='ACTIVE',operational_binding=canonical(op)),audit)
  assert h.scope is None and not h._actions_inflight
  h.revoke();result=tx.cancel(h,'HARD_NO_PROGRESS_BUDGET_CANCELLATION_RECOVERY');tx.close();tx=None
  assert result['disposition']=='CANCELLED' and result['ownership']=='RELEASED' and result['uncertainty'] is None
  r=dict(result,schema='CANCELLATION_ONLY_RECOVERY-1',seconds=time.monotonic()-begin,wall_time=time.time(),audit_before_sha256=sha(before),audit_after_sha256=sha(audit.read_bytes()),admission_reopened=False,model_requests_added=0,implementation_changed=False)
  data=canonical(r).encode();fd=_directory(B)
  try:_put(fd,'RECOVERY_CANCELLATION.json',data);os.fsync(fd)
  finally:os.close(fd)
  (O/'RECOVERY_CANCELLATION.json').write_bytes(data);print(canonical(r))
finally:
 if tx:tx.close()
 s.close()
