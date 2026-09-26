"""Independent recovery, with timing owned by the recovery process itself."""
import json,sys,time
from pathlib import Path
sys.path.insert(0,'/tmp/forge-attempt-chain-slo3xg5p')
from adapter.context_projection import canonical,sha,derive
from adapter.controller_authority_store import ControllerAuthorityStore
from adapter.authority_bootstrap import reconstruct_authorization
from adapter.activation_transaction import ActivationTransaction
from adapter.attempt_chain import require_issued,derive_dispatch
from adapter.orchestration_boundary import recover_boundary
O=Path(__file__).parent;pin=json.loads((O/'CURRENT_PIN.json').read_bytes());b=Path(pin['path']).read_bytes();assert sha(b)==pin['sha256'];p=json.loads(b)
s=ControllerAuthorityStore(**p['selected_store']);begin=time.monotonic();mode=sys.argv[1]
try:
 if mode=='ACTIVE':r=recover_boundary(s,p['r11_authorization_id'])
 else:
  with s.session():
   a=reconstruct_authorization(s,p['r11_authorization_id'])
   if mode=='AUTHORITY':
    require_issued(a);assert derive_dispatch(a)==json.loads(s.resolve(p['dispatch']['authority_id']))
    derived=derive(json.loads(a.context_projection),a.context_binding)
    assert {k:derived[k] for k in p['context_identities']}==p['context_identities']
    assert a.context_binding.governance.identities==p['operational_identities']
    assert a.context_binding.governance.run7['release_authority']==p['release_authority']
    assert not Path(p['audit']).exists()
    r={'result':'PASS','release_authority':p['release_authority'],'operational_identities':p['operational_identities'],'context_identities':p['context_identities'],'lifecycle_issued':False,'audit_unused':True}
   else:
    t=ActivationTransaction.recover(a,p['audit'],p['dispatch']['authority_id'])
    try:r=dict(t.recovery)
    finally:t.close()
 r.update(seconds=time.monotonic()-begin,independent_process=True,publication_pin=pin)
 print(canonical(r))
finally:s.close()
