"""Pinned read-only legacy runtime reconstruction. No state writes."""
import json,sys,hashlib,signal
from pathlib import Path
request=json.load(sys.stdin)
signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('legacy verification 120s limit')));signal.alarm(120)
root=request['runtime_root'];sys.path.insert(0,root)
from adapter.context_projection import sha,digest,canonical
from adapter.controller_authority_store import ControllerAuthorityStore
from adapter.authority_bootstrap import reconstruct_authorization
from adapter.authorization_lifecycle import reconstruct as lifecycle,dispatch_binding
from adapter.activation_transaction import invocation,_read
from adapter.invocation_ownership import InvocationOwnership
from adapter.recovery_ledger import reconstruct as actions
import os
pin=request['publication'];raw=Path(pin['path']).read_bytes();assert sha(raw)==pin['sha256'];pub=json.loads(raw)
s=ControllerAuthorityStore(**pub['selected_store'])
try:
 with s.session():
  auth=reconstruct_authorization(s,s.applicability['authorization_id']);g=auth.context_binding.governance
  rt=json.loads(s.resolve(pub['controller_runtime']['authority_id']))
  actual={f.name:sha(f.read_bytes()) for f in Path(root,'adapter').glob('*.py')}
  assert rt['root']==root and actual==rt['files'] and rt['identity']=='sha256:'+digest(actual)
  audit=Path(pub['audit']);auditbytes=audit.read_bytes();state=lifecycle(auditbytes,auth,audit);effect=actions(audit,auth)
  fd=os.open(auth.ownership_ledger,os.O_RDONLY|os.O_NOFOLLOW)
  try:
   ledger=_read(fd);owner=invocation(fd);scope=InvocationOwnership.__new__(InvocationOwnership)._history(fd);assert ledger==_read(fd)
  finally:os.close(fd)
  assert state['state']=='CANCELLED' and not state['uncertain'] and owner is None and scope is None
  assert effect['scope'] is None and not effect['incomplete'] and not effect['results']
  assert auditbytes==audit.read_bytes() and ledger==Path(auth.ownership_ledger).read_bytes()
  result={'runtime':rt['identity'],'release_context':dict(g.identities,release_authority=g.run7['release_authority']),'terminal':'CANCELLED','ownership':None,'ExecutionScope':None,'audit_sha256':sha(auditbytes),'ledger_sha256':sha(ledger)}
  print(canonical(result))
finally:s.close()
