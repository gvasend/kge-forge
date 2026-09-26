import json,sys
from pathlib import Path
from types import SimpleNamespace
O=Path(__file__).resolve().parent;d=json.loads((O/'RUNTIME_QUALIFICATION_FINAL.json').read_text());p=json.loads((O/'R12_AUTHENTICATED_CAPTURE.json').read_text())
sys.path.insert(0,d['R3']['root'])
from adapter.controller_authority_store import roots_for,outside
from adapter.attempt_chain import classify_terminal
from adapter.run_control import events
roots=roots_for(SimpleNamespace(**p['authorization']))
paths=[d['R3']['root'],d['R4']['root'],d['selected_store']['root'],d['integration']['anchor_verifier']['root']]
for path in paths:outside(path,roots)
verdict=classify_terminal(events(p['terminal']['audit']),p['terminal'],p['authorization']['authorization_id'],True)
assert verdict=='ACTIVE_CANCELLED_PRE_MODEL_NO_EFFECTS'
result={'private_paths_outside_programmer_authority':paths,'boundary':'PASS','r12_predecessor':verdict,'model_requests':0,'effects':0}
(O/'BOUNDARY_PREDECESSOR.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
