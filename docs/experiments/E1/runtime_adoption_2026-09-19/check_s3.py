"""Read-only current S3 verification; no supervisor operation other than readiness."""
import json,sys,time
from pathlib import Path
O=Path(__file__).resolve().parent;Q=O.parent/'run2_control_plane_binding_2026-09-18'
original=json.loads((Q/'PROPOSED_PRODUCTION_CONTINUATION.json').read_bytes());sys.path.insert(0,str(Path(original['artifacts'][0]['new_blob']).parent.parent))
from adapter.supervisor_observation import observe
from adapter.supervisor_succession import legacy_tuple
from adapter.activation_transaction import _host
from adapter.context_projection import canonical,sha
expected=json.loads((Q/'SUPERVISOR_IMMUTABLE_VERIFICATION.json').read_bytes());begin=time.monotonic();instance=expected['instance']
assert observe(instance)==instance
ready=_host(legacy_tuple(instance),check_scopes=True)
assert observe(instance)==instance
ledger=expected['succession_ledger'];assert sha(Path(ledger['path']).read_bytes())==ledger['sha256']
result={'result':'PASS','SupervisorInstanceId':instance['id'],'succession_head':expected['head'],'readiness':ready,'seconds':time.monotonic()-begin,'wall_time':time.time(),'model_requests':0,'effects':0}
(O/'S3_READINESS.json').write_text(canonical(result));print(canonical(result))
