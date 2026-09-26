import json,sys,importlib.util,time
from pathlib import Path
sys.path.insert(0,'/tmp/forge-r9-context-69itwolf')
from adapter.context_projection import sha,canonical
from adapter.controller_authority_store import ControllerAuthorityStore
out=Path(__file__).parent
path='/tmp/forge-r10-transition-jxppjwou/adapter/operator_projection.py'
spec=importlib.util.spec_from_file_location('adapter.operator_projection',path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
pin=json.loads((out.parent/'run2_r9_dispatch_2026-09-18/CURRENT_PIN.json').read_bytes());b=Path(pin['path']).read_bytes();assert sha(b)==pin['sha256'];pub=json.loads(b)
s=ControllerAuthorityStore(**pub['selected_store']);before=Path(pub['audit']).read_bytes()
try:
 result=module.project(s,s.applicability['authorization_id']);assert result['lifecycle_state']=='CANCELLED' and result['ownership']=='RELEASED' and result['architectural_state']=='QUIESCENT' and result['freshness']=='FRESH';assert before==Path(pub['audit']).read_bytes()
 (out/'ACTUAL_TERMINAL_STATUS.json').write_text(canonical({'code_sha256':sha(Path(path).read_bytes()),'result':result,'historical_audit_unchanged':True}));print(result['projection_seconds'])
finally:s.close()
