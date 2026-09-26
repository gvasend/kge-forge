"""Read-only host prerequisite observation. Never starts or signals a supervisor."""
from pathlib import Path
import json
from adapter.activation_transaction import _host
from adapter.context_projection import read_exact, canonical

out = Path(__file__).resolve().parent
h = 'a0547c7c33b95628d9419a62972f15062bd6fa8ab9236496ceb7d6ab21fbab75'
p = Path('/tmp/kge-forge-e1-controller/auth-e1-wp-001-r7-94f511dfcdcc43ac837191f8732ced39')/h
profile = json.loads(read_exact(str(p),h))
try:
    observed = _host(profile['supervisor_binding'][0])
    result = {'result':'PASS','observation':observed,'restart_required':False}
except Exception as exc:
    result = {'result':'BLOCKED','exception':type(exc).__name__,'reason':str(exc),
              'restart_required':'Host reconciliation required; a different PID would need an authorized binding change.'}
result.update({'execution_context':'host-authorized observation outside Codex sandbox PID namespace',
               'supervisor_restarted':False,'E1_activation_validation':False,
               'E1_activation':False,'E1_ownership_created':False,'E1_model_requests':0})
(out/'HOST_PREREQUISITE.json').write_text(canonical(result)+'\n')
print(canonical(result))
