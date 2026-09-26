"""Fresh-process activation recovery; stop immediately after qualified recovery PASS."""
import json,os
from pathlib import Path
from adapter.context_projection import canonical,sha
from adapter.controller_authority_store import ControllerAuthorityStore,_directory,_read
from adapter.authority_bootstrap import reconstruct_authorization
from adapter.activation_transaction import ActivationTransaction
from adapter.supervisor_succession import reconstruct
O=Path(__file__).resolve().parent
pin=json.loads((O/'CURRENT_PRIVATE_PIN.json').read_bytes());p=Path(pin['path']);fd=_directory(p.parent)
try:data=_read(fd,p.name)
finally:os.close(fd)
assert sha(data)==pin['sha256'];pub=json.loads(data)
store=ControllerAuthorityStore(**pub['selected_store']);tx=None
try:
 with store.session():
  auth=reconstruct_authorization(store,store.applicability['authorization_id'])
  audit=store.state_path(auth.authorization_id+':audit')
  op=json.loads(auth.operational_binding)
  d=json.loads(store.resolve('sha256:'+op['governance']['material_release']['dispatch_amendment']['sha256']))
  ref='E1-ARCHITECT-DISPATCH-sha256:'+d['original_dispatch']['sha256']
  print('Private bootstrap reconstructed; starting independent qualified activation recovery',flush=True)
  tx=ActivationTransaction.recover(auth,audit,ref)
  assert tx.recovery['lifecycle_state']=='ACTIVE' and tx.recovery['handoff_eligible'] and tx.reservation
  assert not tx.recovery['reconciliation_required']
  # recover has just authenticated dispatch, validated production readiness,
  # compared resource identities with the activation commit, and reacquired its fence.
  policy=json.loads(store.resolve(auth.authorization_id+':supervisor-succession'))
  selected=reconstruct(store,policy,store.state_path(policy['ledger_id']).read_bytes())
  assert selected['head']==pub['event_identity']
  rows=[json.loads(x) for x in audit.read_bytes().splitlines()]
  commits=[r for r in rows if r.get('event')=='authorization_lifecycle_activated']
  assert len(commits)==1 and commits[0]['ownership_reservation']==tx.reservation
  result={'result':'ACTIVATED_AND_READY_TO_DISPATCH','current_supervisor':selected['instance']['id'],'succession_head':selected['head'],'supervisor_readiness':'PASS','dispatch_inheritance':'PASS','CURRENT_RELEASE_BINDINGS_VALID':True,'CURRENT_SUPERVISOR_READY':True,'state':'ACTIVE','ownership':'OWNERSHIP_HELD','recovery':tx.recovery,'activation_event':commits[0],'handoff_eligible':True,'operational_ancestry':op['governance']['identities'],'E1_model_requests':0,'E1_implementation_effects':0,'E1_WP_001_dispatched':False,'verification':'Fresh-process ActivationTransaction.recover; production validation and ownership/resource checks unchanged; no redundant activation retry.'}
  with (O/'FINAL_RECOVERY.json').open('xb') as f:f.write(canonical(result).encode());f.flush();os.fsync(f.fileno())
  print(canonical({k:v for k,v in result.items() if k not in ('activation_event','recovery')}),flush=True)
finally:
 if tx:tx.close()
 store.close()
