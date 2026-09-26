"""Read-only current authority/predecessor capture through the frozen runtime."""
import json,os,sys,time,signal
from pathlib import Path
sys.path.insert(0,'/tmp/forge-r10-transition-jxppjwou')
from adapter.context_projection import canonical,sha,derive
from adapter.controller_authority_store import ControllerAuthorityStore
from adapter.authority_bootstrap import reconstruct_authorization
from adapter.authorization_lifecycle import reconstruct,dispatch_binding
from adapter.recovery_ledger import reconstruct as actions
from adapter.activation_transaction import invocation,_read
from adapter.invocation_ownership import InvocationOwnership
from adapter.attempt_transition import readiness

O=Path(__file__).parent
pin=json.loads((O.parent/'run2_r10_dispatch_2026-09-18/CURRENT_PIN.json').read_bytes())
b=Path(pin['path']).read_bytes();assert sha(b)==pin['sha256'];pub=json.loads(b)
s=ControllerAuthorityStore(**pub['selected_store']);begin=time.monotonic()
signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('120s hard phase budget')))
signal.alarm(120)
try:
 with s.session(),s.witness() as witness:
  a=reconstruct_authorization(s,s.applicability['authorization_id']);g=a.context_binding.governance
  raw=Path(pub['audit']).read_bytes();life=reconstruct(raw,a,Path(pub['audit']));act=actions(Path(pub['audit']),a)
  fd=os.open(a.ownership_ledger,os.O_RDONLY|os.O_NOFOLLOW)
  try:
   data=_read(fd);owner=invocation(fd);scope=InvocationOwnership.__new__(InvocationOwnership)._history(fd)
   assert data==_read(fd)
  finally:os.close(fd)
  assert life['state']=='CANCELLED' and not life['uncertain'] and owner is None and scope is None
  assert act['scope'] is None and not act['incomplete'] and not act['results']
  projection=derive(json.loads(a.context_projection),a.context_binding)
  mutable={p:r['new_sha256'] for p,r in g.changes.items()};mutable.update({p:r['sha256'] for p,r in g.supplement['inputs'].items()})
  for source in a.context_binding.sources.values():
   path=str(a.context_binding.repos[source['repository']]/source['path']);mutable[path]=g.current_hash(path,source['sha256'])
  mutable[pub['audit']]=sha(raw)
  result={'publication':pin,'governance':g.__dict__,'mutable':mutable,'context':projection,
   'authorization':json.loads(s.resolve(a.authorization_id)), 'dispatch':json.loads(s.resolve(pub['dispatch']['authority_id'])),
   'terminal':{'lifecycle':life,'actions':act,'ownership':owner,'scope':scope,'audit':pub['audit'],'audit_sha256':sha(raw),'ledger_sha256':sha(data)},
   'immutable_witness':dict(witness),'capture_seconds':time.monotonic()-begin}
  (O/'R10_AUTHENTICATED_CAPTURE.json').write_text(canonical(result))
  start=time.monotonic();host=readiness(a,s,None,True,None)
  (O/'S3_READINESS.json').write_text(canonical({'result':'PASS','observation':host,'seconds':time.monotonic()-start,'wall':time.time()}))
  assert raw==Path(pub['audit']).read_bytes() and data==Path(a.ownership_ledger).read_bytes()
  print(canonical({'capture_seconds':result['capture_seconds'],'S3':'PASS','r10':'CANCELLED','owner':owner}))
finally:signal.alarm(0);s.close()
