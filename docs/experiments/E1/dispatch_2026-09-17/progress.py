import json,time
from pathlib import Path
p=Path('/tmp/kge-forge-controller-authority/auth-e1-wp-001-r7-94f511dfcdcc43ac837191f8732ced39/e1-programmer-dispatch-2026-09-17')
b=json.loads((p/'AUDIT_BEFORE.json').read_bytes());rows=[json.loads(x) for x in Path(b['path']).read_bytes()[b['bytes']:].splitlines()]
phase=max((json.loads(x.read_bytes()) for x in p.glob('PHASE_*.json')),key=lambda x:x['time_unix_ns'])
print(json.dumps({'phase':phase['phase'],'phase_seconds':round((time.time_ns()-phase['time_unix_ns'])/1e9),'model_request_intents':sum(r.get('event')=='model_request_content_bound' for r in rows),'action_requests':sum(r.get('event')=='action_request' for r in rows),'action_results':sum(r.get('event')=='action_result' for r in rows),'last_events':[r.get('event') for r in rows[-4:]]}))
