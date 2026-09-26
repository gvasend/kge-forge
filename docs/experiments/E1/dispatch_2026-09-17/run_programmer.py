"""One authorized first dispatch using the unchanged qualified production interfaces."""
import json,os,time
from pathlib import Path
from adapter.context_projection import canonical,sha
from adapter.controller_authority_store import ControllerAuthorityStore,_directory,_read,_put,outside
from adapter.authority_bootstrap import reconstruct_authorization
from adapter.activation_transaction import ActivationTransaction
from adapter.governed_host import GovernedHost
from adapter.orchestrator import ReasoningOrchestrator
from adapter.responses_orchestrator import ResponsesReasoning
O=Path(__file__).resolve().parent
AUTH='auth-e1-wp-001-r7-94f511dfcdcc43ac837191f8732ced39'
PRIVATE=Path('/tmp/kge-forge-controller-authority')/AUTH/'e1-programmer-dispatch-2026-09-17'
pin={'path':'/tmp/kge-forge-controller-authority/'+AUTH+'/supervisor-succession-adoption-2026-09-17/SUCCESSION_PUBLICATION.json','sha256':'95a2454b094f2b6e4af044cbfa8a8efd98a225866e2b19fc286a2d63abdacd4e'}
p=Path(pin['path']);fd=_directory(p.parent)
try:data=_read(fd,p.name)
finally:os.close(fd)
assert sha(data)==pin['sha256'];publication=json.loads(data)
store=ControllerAuthorityStore(**publication['selected_store']);tx=None;reasoning=None;host=None
outside(PRIVATE,store.catalog['programmer_roots']);PRIVATE.mkdir(mode=0o700)
def save(name,obj):
 data=canonical(obj).encode();fd=_directory(PRIVATE)
 try:_put(fd,name,data);os.fsync(fd)
 finally:os.close(fd)
 return {'path':str(PRIVATE/name),'sha256':sha(data)}
def phase(name):
 save('PHASE_'+name+'.json',{'phase':name,'time_unix_ns':time.time_ns()});print(name,flush=True)
save('ARCHITECT_DISPATCH_SOURCE.json',{'authority':'Architect','channel':'user','decision':'E1-WP-001 DISPATCH AUTHORIZED','authorization_id':AUTH,'activation_event':'E1-AUTHORIZATION-LIFECYCLE-sha256:390c05fbcb0697e679749226ba3fab47401c337a8d2bdaf98556c405288bffd1','ownership_reservation':'INVOCATION-RESERVATION-sha256:e5bd9403e16bcd61ce0bae40c31d300e8a8a94e4c266e26a705e5d6f0c8f7363','supervisor_instance':'SupervisorInstance-sha256:1aaa0c96caadb97c3e0678e8c0039f32cb2ac7f7ff3c607cf84998190b8e0a41','succession':publication['event_identity'],'scope':'First real Programmer turn and autonomous governed continuation; no ambient host authority or silent authority expansion; return to Architect for assessment.'})
try:
 with store.session():
  phase('PRIVATE_BOOTSTRAP')
  raw=json.loads(store.resolve(AUTH));transport=json.loads(raw['model_transport'])
  if not os.environ.get(transport['credential_environment_reference']):raise ValueError('released credential environment reference unavailable')
  auth=reconstruct_authorization(store,AUTH);audit=store.state_path(AUTH+':audit')
  before=audit.read_bytes();save('AUDIT_BEFORE.json',{'path':str(audit),'sha256':sha(before),'bytes':len(before)})
  if any(json.loads(line).get('event')=='model_request_content_bound' for line in before.splitlines()):raise ValueError('prior E1 model attempt exists; uncertain request must not be replayed')
  op=json.loads(auth.operational_binding)
  d=json.loads(store.resolve('sha256:'+op['governance']['material_release']['dispatch_amendment']['sha256']))
  ref='E1-ARCHITECT-DISPATCH-sha256:'+d['original_dispatch']['sha256']
  phase('RECOVER_EXISTING_ACTIVATION')
  tx=ActivationTransaction.recover(auth,audit,ref)
  assert tx.recovery['handoff_eligible'] and tx.recovery['lifecycle_state']=='ACTIVE'
  assert tx.reservation['reservation_id']=='INVOCATION-RESERVATION-sha256:e5bd9403e16bcd61ce0bae40c31d300e8a8a94e4c266e26a705e5d6f0c8f7363'
  commits=[json.loads(x) for x in audit.read_bytes().splitlines() if json.loads(x).get('event')=='authorization_lifecycle_activated']
  assert len(commits)==1 and commits[0]['event_id']=='E1-AUTHORIZATION-LIFECYCLE-sha256:390c05fbcb0697e679749226ba3fab47401c337a8d2bdaf98556c405288bffd1'
  phase('CONSTRUCT_GOVERNED_HOST')
  host=GovernedHost(tx.auth,audit);tx.attach(host)
  phase('CONSTRUCT_RELEASED_REASONING_INTERFACE')
  reasoning=ResponsesReasoning(ReasoningOrchestrator(host),model=transport['model'],endpoint=transport['endpoint'])
  payload=reasoning.projection.verify()['projection']['payload']
  phase('RUN_PROGRAMMER')
  result=reasoning.run(payload['task'],payload['context'],max_cycles=10000)
  receipt=save('PROGRAMMER_RESULT.json',{'result':result,'authorization_id':AUTH,'audit':str(audit),'audit_sha256':sha(audit.read_bytes()),'ownership_ledger_sha256':sha(Path(auth.ownership_ledger).read_bytes()),'scope_state':host.scope.state if host.scope else None,'finished':reasoning.finished,'terminal_action_id':getattr(reasoning,'terminal_action_id',None),'acceptance':'Architect and subsequent human assessment required; no Experiment 1 PASS inferred.'})
  with (O/'RESULT_RECEIPT.json').open('xb') as f:f.write(canonical(receipt).encode())
  print(canonical(receipt),flush=True)
except BaseException as ex:
 # Never print arbitrary provider diagnostics or credential-bearing messages.
 receipt=save('INTERRUPTION.json',{'status':'STOPPED_NO_AUTOMATIC_RETRY','exception_type':type(ex).__name__,'phase_files':sorted(p.name for p in PRIVATE.glob('PHASE_*.json')),'private_error_text':str(ex),'model_records':reasoning.records if reasoning else [],'finished':reasoning.finished if reasoning else False,'scope_state':host.scope.state if host and host.scope else None,'scope_id':host.scope.id if host and host.scope else None,'time_unix_ns':time.time_ns()})
 with (O/'INTERRUPTION_RECEIPT.json').open('xb') as f:f.write(canonical(receipt).encode())
 print(canonical({'status':'STOPPED_NO_AUTOMATIC_RETRY','exception_type':type(ex).__name__,'evidence':receipt}),flush=True)
 raise SystemExit(2)
finally:
 if tx:tx.close()
 store.close()
