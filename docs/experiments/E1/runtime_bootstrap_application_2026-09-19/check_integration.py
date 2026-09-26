"""Read-only actual implementation/entry boundary checks. No invocation issued."""
import json,sys,time,subprocess,ast
from pathlib import Path
O=Path(__file__).resolve().parent;pin=json.loads((O/'AUTHORIZED_SELECTION.json').read_bytes());rec=json.loads((O/'INDEPENDENT_RECONSTRUCTION.json').read_bytes());sys.path.insert(0,pin['consumer_root'])
from adapter import runtime_adoption as r
from adapter.controller_authority_store import ControllerAuthorityStore,encoded,sha
s=ControllerAuthorityStore(**pin['selected_store']);start=time.monotonic()
try:
 binding=rec['runtime_binding'];selected=r.validate_invocation_runtime(s,binding,rec['runtime']['root']);assert selected['current_runtime']==binding['runtime']
 try:r.validate_invocation_runtime(s,binding,pin['consumer_root'])
 except ValueError as e:consumer_error=str(e)
 else:raise AssertionError('consumer bundle substituted for selected R1')
 assert consumer_error=='unaccounted runtime'
 root=Path(rec['runtime']['root']);source=root/'adapter/attempt_chain.py';text=source.read_text()
 assert sha(source.read_bytes())==rec['runtime']['files']['attempt_chain.py']
 tree=ast.parse(text);decision=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='decision')
 source_segment=ast.get_source_segment(text,decision)
 assert 'unaccounted runtime' in source_segment and 'validate_invocation_runtime' not in source_segment and 'runtime_adoption' not in source_segment
 # This negative is explicitly a historical-context check, not an authorized new
 # invocation. R12 keeps its R0 binding and must not be silently rebound to R1.
 oldpin=json.loads((O.parent/'run2_r12_dispatch_2026-09-18/CURRENT_PIN.json').read_bytes())
 payload={'runtime':str(root),'publication':oldpin}
 code="""import json,sys
from pathlib import Path
p=json.load(sys.stdin);sys.path.insert(0,p['runtime'])
from adapter.controller_authority_store import ControllerAuthorityStore,sha
from adapter.authority_bootstrap import reconstruct_authorization
b=Path(p['publication']['path']).read_bytes();assert sha(b)==p['publication']['sha256'];old=json.loads(b);s=ControllerAuthorityStore(**old['selected_store'])
try:
 with s.session():
  try:reconstruct_authorization(s,s.applicability['authorization_id'])
  except ValueError as e:print(json.dumps({'rejected':str(e)}))
  else:raise AssertionError('historical invocation silently rebound')
finally:s.close()
"""
 t=time.monotonic();child=subprocess.run(['/usr/bin/python3.11','-c',code],input=encoded(payload),capture_output=True,timeout=120,check=True);negative=json.loads(child.stdout)
 assert negative=={'rejected':'unaccounted runtime'}
 result={'verdict':'BLOCKED_R1_ORDINARY_VALIDATOR_CONSUMPTION','R1_actual_bytes_equal_current_head':'PASS','bootstrap_consumer_as_R1':'REJECTED_UNACCOUNTED_RUNTIME','historical_R12_rebinding':negative,'historical_negative_seconds':time.monotonic()-t,
 'R1_attempt_validator':{'path':str(source),'sha256':sha(source.read_bytes()),'decision_line':decision.lineno,'runtime_head_consumer_present':False},
 'bootstrap_consumer_attempt_validator':{'path':str(Path(pin['consumer_root'],'adapter/attempt_chain.py')),'sha256':sha(Path(pin['consumer_root'],'adapter/attempt_chain.py').read_bytes())},
 'ordinary_production_context_integration':'NOT_ESTABLISHED','complete_production_premodel_timing':None,'seconds':time.monotonic()-start,'r13_created':False,'real_invocations':0,'model_requests':0,'E1_effects':0}
 (O/'INTEGRATION_GATE.json').write_bytes(encoded(result));print(encoded(result).decode())
finally:s.close()
