"""Independent non-effecting reconstruction; no lifecycle creation."""
import json,os,sys,time,signal
from pathlib import Path
O=Path(__file__).parent;pin=json.loads((O/'CURRENT_PIN.json').read_bytes());data=Path(pin['path']).read_bytes()
import hashlib
assert hashlib.sha256(data).hexdigest()==pin['sha256'];pub=json.loads(data);sys.path.insert(0,pub['runtime_root'])
from adapter.context_projection import canonical,sha,derive
from adapter.controller_authority_store import ControllerAuthorityStore
from adapter.authority_bootstrap import reconstruct_authorization
from adapter.attempt_chain import require_issued,readiness
from adapter.attempt_ownership import observe
from adapter.authorization_lifecycle import dispatch_binding
signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('120s phase budget')));signal.alarm(120)
start=time.monotonic();s=ControllerAuthorityStore(**pub['selected_store'])
try:
 with s.session():
  a=reconstruct_authorization(s,pub['authorization_id']);g=a.context_binding.governance
  assert g.identities==pub['operational_identities'] and g.run7['release_authority']==pub['release_authority']
  projection=derive(json.loads(a.context_projection),a.context_binding)
  assert {k:projection[k] for k in pub['context_identities']}==pub['context_identities']
  q=json.loads(s.resolve(pub['qualification']['authority_id']));assert q['result']=='PASS'
  assert q['amendment']==pub['amendment'] and q['controller_runtime']==pub['controller_runtime'] and q['accepted_proposal']==pub['proposal']
  for name,h in q['evidence'].items():assert sha((O/name).read_bytes())==h
  dispatch_binding(a,pub['audit'],pub['dispatch'])
  owner,scope,_=observe(a.ownership_ledger);assert owner is None and scope is None
  assert not Path(pub['audit']).exists() and not Path(pub['audit']).parents[2].exists()
  try:require_issued(a)
  except ValueError as exc:denial=str(exc)
  else:raise AssertionError('unissued candidate acquired issuance authority')
  host=readiness(a,s,None,True,None)
  result={'result':'PASS_QUALIFIED_PREPARED','seconds':time.monotonic()-start,'authorization_id':a.authorization_id,'release_authority':g.run7['release_authority'],
   'identities':g.identities,'context':{k:projection[k] for k in pub['context_identities']},'host':host,'owner':owner,'scope':scope,
   'audit_unused':True,'issuance_denial':denial,'handoff_eligible':False,'amendment_applied':False,'real_model_requests':0,'effects':0}
  result.update(soft_exceeded=result['seconds']>=30,hard_exceeded=result['seconds']>=120)
  (O/'INDEPENDENT_RECONSTRUCTION.json').write_text(canonical(result));print(canonical(result))
finally:signal.alarm(0);s.close()
