"""Fresh terminal projection from the unchanged applied r11 runtime."""
import json,sys,time,signal
from pathlib import Path
O=Path(__file__).parent
pin=json.loads((O.parent/'run2_r11_dispatch_2026-09-18/CURRENT_PIN.json').read_bytes());pub=json.loads(Path(pin['path']).read_bytes());sys.path.insert(0,pub['runtime_root'])
from adapter.context_projection import canonical,sha
from adapter.controller_authority_store import ControllerAuthorityStore
from adapter.operator_projection import project
assert sha(Path(pin['path']).read_bytes())==pin['sha256']
s=ControllerAuthorityStore(**pub['selected_store'])
try:
 result=project(s,pub['authorization_id'])
 assert result['freshness']=='FRESH' and result['lifecycle_state']=='CANCELLED' and result['ownership']=='RELEASED' and result['architectural_state']=='QUIESCENT' and not result['uncertainty']
 (O/'FRESH_PREDECESSOR_STATUS.json').write_text(canonical(result));print(canonical({'result':'PASS','seconds':result['projection_seconds'],'state':result['lifecycle_state']}))
finally:s.close()
