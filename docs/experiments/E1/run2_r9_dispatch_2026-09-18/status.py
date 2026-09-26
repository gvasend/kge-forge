"""Read-only operator projection; never participates in lifecycle authority."""
from pathlib import Path
import json,time
from adapter.run_control import status
from adapter.context_projection import canonical,sha
O=Path('/home/gvasend/app/kge-forge/docs/experiments/E1/run2_r9_dispatch_2026-09-18')
pin=json.loads((O/'CURRENT_PIN.json').read_bytes());b=Path(pin['path']).read_bytes();assert sha(b)==pin['sha256'];p=json.loads(b)
try:r=status(p['audit'])
except (ValueError,KeyError):r={'state':'UNKNOWN','reason':'INCOMPLETE_OR_INVALID_OBSERVATION','projection_generated':time.time()}
d=O/'operator_status';d.mkdir(exist_ok=True);(d/(str(time.time_ns())+'.json')).write_text(canonical(r))
print(canonical({k:r.get(k) for k in ('state','reason','freshness','lifecycle_state','ownership','supervisor_readiness','cycle','current_subphase','last_event_age','progress_age','model_requests','responses','action_requests','action_results','executions','authoritative_effects','budget_state','terminal_disposition','usage_state','reported_cumulative_tokens','uncertainty')}))
