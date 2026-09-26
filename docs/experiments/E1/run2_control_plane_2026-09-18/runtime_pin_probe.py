"""Negative probe: staged code must not masquerade as the released runtime."""
import hashlib,json,sys
from pathlib import Path
O=Path(__file__).resolve().parent
pin=json.loads((O.parent/'run2_r12_dispatch_2026-09-18/CURRENT_PIN.json').read_bytes())
b=Path(pin['path']).read_bytes();assert hashlib.sha256(b).hexdigest()==pin['sha256'];p=json.loads(b)
sys.path.insert(0,str(O/'candidate'))
from adapter.controller_authority_store import ControllerAuthorityStore
from adapter.authority_bootstrap import reconstruct_authorization
s=ControllerAuthorityStore(**p['selected_store'])
try:
 try:
  with s.session():reconstruct_authorization(s,p['r12_authorization_id'])
 except ValueError as e:
  assert str(e)=='unaccounted runtime'
  result={'result':'PASS_REJECTED','reason':str(e),'meaning':'Staged runtime cannot consume current authority as its own implementation binding','production_qualification':'NOT_ESTABLISHED'}
 else:raise AssertionError('unbound candidate runtime accepted')
finally:s.close()
(O/'RUNTIME_PIN_NEGATIVE.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
