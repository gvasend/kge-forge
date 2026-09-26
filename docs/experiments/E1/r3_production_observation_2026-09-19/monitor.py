import json,sys,time,os,importlib.util
from pathlib import Path
O=Path(__file__).resolve().parent;p=next(x for x in json.loads((O/'QUALIFICATION_BINDINGS.json').read_bytes()) if x['name']==sys.argv[1]);sys.path.insert(0,p['runtime_root'])
overlay=O/'candidate'/'adapter'/'control_plane_binding.py'
spec=importlib.util.spec_from_file_location('adapter.control_plane_binding',overlay)
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);sys.modules['adapter.control_plane_binding']=module
from adapter.controller_authority_store import ControllerAuthorityStore
from adapter.operator_projection import project
from adapter.context_projection import canonical
s=ControllerAuthorityStore(**p['selected_store']);root=Path(p['audit']).parent
try:
 while True:
  v=project(s,p['authorization_id'])
  with (root/'STATUS.jsonl').open('a') as f:f.write(canonical(v)+'\n');f.flush();os.fsync(f.fileno())
  if (root/'MONITOR_STOP').exists():break
  time.sleep(2)
finally:s.close()
