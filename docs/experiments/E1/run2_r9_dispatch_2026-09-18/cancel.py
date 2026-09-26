"""Governed cancellation of this stopped r9 only. Never reopen admission."""
import json,os,time
from pathlib import Path
from dataclasses import replace
from adapter.context_projection import canonical,sha
from adapter.controller_authority_store import ControllerAuthorityStore,_directory,_put
from adapter.authority_bootstrap import reconstruct_authorization
from adapter.activation_transaction import ActivationTransaction,invocation
from adapter.authorization_lifecycle import reconstruct
from adapter.recovery_ledger import reconstruct as recover_actions
from adapter.governed_host import GovernedHost
from adapter.run_control import events
O=Path('/home/gvasend/app/kge-forge/docs/experiments/E1/run2_r9_dispatch_2026-09-18');pin=json.loads((O/'CURRENT_PIN.json').read_bytes());b=Path(pin['path']).read_bytes();assert sha(b)==pin['sha256'];p=json.loads(b)
s=ControllerAuthorityStore(**p['selected_store']);tx=None;begin=time.monotonic()
try:
 with s.session():
  a=reconstruct_authorization(s,s.applicability['authorization_id']);audit=Path(p['audit']);rows=events(audit)
  assert any(r.get('event')=='admission_closed' for r in rows)
  assert not any(r.get('event') in ('model_request_start','model_request_content_bound','action_request','action_result','execution_scope_created') for r in rows)
  state=reconstruct(audit.read_bytes(),a,audit);assert state['state']=='ACTIVE' and not state['uncertain']
  recovered=recover_actions(audit,a);assert recovered['scope'] is None and not recovered['incomplete'] and not recovered['results']
  # Acquire the qualified controller fence without reopening model/effect admission.
  tx=ActivationTransaction(a,audit,p['dispatch']['authority_id']);ledger=tx.ownership._locked()
  try:
   owner=invocation(ledger);assert owner==state['activation_event']['ownership_reservation'];assert tx.ownership._history(ledger) is None
  finally:os.close(ledger)
  before={'audit_sha256':sha(audit.read_bytes()),'ledger_sha256':sha(Path(a.ownership_ledger).read_bytes())}
  # Reconstruct the effective ACTIVE identity solely for governed interruption.
  op=json.loads(a.operational_binding);op['dispatch_authorization']=p['dispatch'];effective=replace(a,state='ACTIVE',operational_binding=canonical(op))
  host=GovernedHost(effective,audit)
  host.revoke()
  assert host.scope is None and host.architectural_state=='QUIESCENT'
  result=tx.cancel(host,'ORCHESTRATION_FAILURE_NESTED_AUTHORITY_SESSION_BEFORE_MODEL_HANDOFF')
  assert result['disposition']=='CANCELLED' and result['ownership']=='RELEASED'
  result.update(classification='INTERRUPTED_NO_EFFECTS',execution_scope='NONE',architectural_state=host.architectural_state,
    model_requests=0,model_responses=0,action_requests=0,action_results=0,implementation_effects=0,
    admission_reopened=False,automatic_retry=False,provider_activity='NO_R9_MODEL_REQUEST_INITIATED',
    prior_observation='Historical provisional INDETERMINATE telemetry preserved; this typed lifecycle cancellation resolves controller ownership.',
    before=before,audit_sha256=sha(audit.read_bytes()),ledger_sha256=sha(Path(a.ownership_ledger).read_bytes()),seconds=time.monotonic()-begin,wall_time=time.time())
  fd=_directory(Path(p['private_run_root']))
  try:_put(fd,'CANCELLATION.json',canonical(result).encode());os.fsync(fd)
  finally:os.close(fd)
  (O/'CANCELLATION.json').write_text(canonical(result));print(canonical(result))
finally:
 if tx:tx.close()
 s.close()
