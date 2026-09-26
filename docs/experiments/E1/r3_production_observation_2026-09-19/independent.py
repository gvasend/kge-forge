import json,sys,time,importlib.util
from pathlib import Path
O=Path(__file__).resolve().parent;p=next(x for x in json.loads((O/'QUALIFICATION_BINDINGS.json').read_bytes()) if x['name']==sys.argv[1]);sys.path.insert(0,p['runtime_root'])
_overlay=O/'candidate/adapter/control_plane_binding.py';_spec=importlib.util.spec_from_file_location('adapter.control_plane_binding',_overlay);_module=importlib.util.module_from_spec(_spec);_module.__package__='adapter';sys.modules['adapter.control_plane_binding']=_module;_spec.loader.exec_module(_module)
from adapter.controller_authority_store import ControllerAuthorityStore
from adapter.authority_bootstrap import reconstruct_authorization
from adapter.activation_transaction import ActivationTransaction
from adapter.orchestration_boundary import recover_boundary
s=ControllerAuthorityStore(**p['selected_store']);start=time.monotonic()
try:
 if sys.argv[2]=='ACTIVE':r=recover_boundary(s,p['authorization_id'])
 else:
  with s.session():
   a=reconstruct_authorization(s,p['authorization_id']);t=ActivationTransaction.recover(a,p['audit'],p['dispatch']['authority_id'])
   try:r=t.recovery
   finally:t.close()
 r.update(independent_process=True,seconds=time.monotonic()-start);print(json.dumps(r))
finally:s.close()
