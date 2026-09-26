"""Exact sealed prepared store, full production predicate, no issuance."""
import json,sys,os,time,signal
from pathlib import Path
O=Path(__file__).parent;pin=json.loads((O/'PREDECESSOR_PIN.json').read_bytes());b=Path(pin['path']).read_bytes()
import hashlib
assert hashlib.sha256(b).hexdigest()==pin['sha256'];pub=json.loads(b);sys.path.insert(0,pub['runtime_root'])
from adapter.controller_authority_store import ControllerAuthorityStore
from adapter.authority_bootstrap import reconstruct_authorization
from adapter.activation_transaction import _validate_production,invocation
from adapter.invocation_ownership import InvocationOwnership
from adapter.context_projection import canonical,sha
from contextlib import contextmanager
from unittest.mock import patch
import adapter.attempt_chain as chain
import adapter.controller_authority_store as cas
from adapter.validation_spans import recording
signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('120 second phase budget')))
spans=[]
class Observer:
 @contextmanager
 def span(self,name):
  st=time.monotonic();wall=time.time()
  try:yield
  finally:spans.append({'schema':'READ_ONLY_QUALIFICATION_SPAN-1','operation':name,'start':st,'wall':wall,'seconds':time.monotonic()-st,'authorization_id':pub['authorization_id'],'authoritative':False})
obs=Observer();original_peer=chain.peer

def observed_peer(*args,**kwargs):
 with obs.span('fresh_supervisor_peer'):return original_peer(*args,**kwargs)
s=ControllerAuthorityStore(**pub['selected_store'])
try:
 with s.session(),recording(obs),patch.object(chain,'peer',side_effect=observed_peer):
  signal.alarm(120);start=time.monotonic();a=reconstruct_authorization(s,pub['authorization_id']);bootstrap=time.monotonic()-start
  signal.alarm(120);before=Path(a.ownership_ledger).read_bytes();own=InvocationOwnership(a.ownership_ledger);fd=own._locked()
  start=time.monotonic();wall=time.time()
  try:
   assert invocation(fd) is None and own._history(fd) is None
   result=_validate_production(a,Path(pub['audit']),pub['dispatch'],fd,_preissuance=True)
  finally:os.close(fd)
  duration=time.monotonic()-start;signal.alarm(0)
  assert not Path(pub['audit']).exists() and not Path(pub['audit']).parents[2].exists()
  assert before==Path(a.ownership_ledger).read_bytes()
  value={'schema':'NON_AUTHORIZING_SEALED_STORE_PREFLIGHT-1','result':'PASS','publication':pin,'runtime_identity':pub['controller_runtime_identity'],
   'bootstrap_seconds':bootstrap,'validation_seconds':duration,'monotonic_start':start,'wall_start':wall,
   'soft_warning':duration>=30,'hard_exceeded':duration>=120,'soft_seconds':30,'hard_seconds':120,
   'spans':spans,'production_result':result,'ledger_sha256':sha(before),'audit_unused':True,'issued':False,'activated':False,'model_requests':0,'effects':0}
  (O/'PREFLIGHT.json').write_text(canonical(value));print(canonical({'result':'PASS','validation_seconds':duration,'soft_warning':duration>=30}))
finally:signal.alarm(0);s.close()
