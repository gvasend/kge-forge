"""Independent, read-only r12 recovery through the unchanged applied verifier."""
import hashlib,json,sys,time
from pathlib import Path
O=Path(__file__).resolve().parent;R=O.parent/'run2_r12_dispatch_2026-09-18'
pin=json.loads((R/'CURRENT_PIN.json').read_bytes());raw=Path(pin['path']).read_bytes()
assert hashlib.sha256(raw).hexdigest()==pin['sha256'];p=json.loads(raw)
sys.path.insert(0,p['runtime_root'])
from adapter.controller_authority_store import ControllerAuthorityStore
from adapter.authority_bootstrap import reconstruct_authorization
from adapter.authorization_lifecycle import reconstruct
from adapter.recovery_ledger import reconstruct as recover_actions
from adapter.attempt_ownership import observe
from adapter.attempt_chain import classify_terminal
from adapter.run_control import events,assert_admission,BudgetExceeded,E1_POLICY
s=ControllerAuthorityStore(**p['selected_store']);start=time.monotonic()
try:
 with s.session():
  a=reconstruct_authorization(s,p['r12_authorization_id']);audit=Path(p['audit']);before=audit.read_bytes()
  expected=json.loads((R/'TERMINAL_EVIDENCE.json').read_bytes())
  assert hashlib.sha256(before).hexdigest()==expected['audit_sha256']
  life=reconstruct(before,a,audit);actions=recover_actions(audit,a);owner,scope,ledger=observe(a.ownership_ledger)
  assert owner is None and scope is None
  rows=events(audit);result=classify_terminal(rows,{'lifecycle':life,'actions':actions},a.authorization_id,True)
  assert result=='ACTIVE_CANCELLED_PRE_MODEL_NO_EFFECTS'
  identity={'authorization_id':a.authorization_id,'session_id':a.session_id,'invocation_id':a.turn_id,'work_package_id':a.work_package_id}
  try:assert_admission(audit,E1_POLICY,identity)
  except BudgetExceeded:closed=True
  else:raise AssertionError('admission open')
  assert audit.read_bytes()==before
  output={'result':'PASS','safe_predecessor':result,'admission':'CLOSED','ownership':None,'scope':None,
   'lifecycle':life,'actions':actions,'seconds':time.monotonic()-start,'audit_sha256':hashlib.sha256(before).hexdigest(),
   'ledger_sha256':hashlib.sha256(ledger).hexdigest(),'policy':'EXISTING_APPLIED_SEMANTIC_POLICY','new_attempt_created':False}
  (O/'R12_PREDECESSOR.json').write_text(json.dumps(output,indent=2))
  print(result)
finally:s.close()
