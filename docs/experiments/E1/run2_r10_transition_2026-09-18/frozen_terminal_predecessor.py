"""Pinned read-only r9 verifier, executed with the unchanged r9 runtime."""
import json,sys,os
from pathlib import Path
from adapter.context_projection import canonical,sha,derive
from adapter.controller_authority_store import ControllerAuthorityStore
from adapter.authority_bootstrap import reconstruct_authorization
from adapter.authorization_lifecycle import dispatch_binding,reconstruct
from adapter.recovery_ledger import reconstruct as actions
from adapter.activation_transaction import invocation,_read
from adapter.invocation_ownership import InvocationOwnership
from adapter.attempt_context import readiness
pin=json.loads(sys.argv[1]);b=Path(pin['path']).read_bytes();assert sha(b)==pin['sha256'];pub=json.loads(b)
s=ControllerAuthorityStore(**pub['selected_store'])
with s.session():
 a=reconstruct_authorization(s,s.applicability['authorization_id']);g=a.context_binding.governance
 with s.witness() as witness:
  g.verify();dispatch_binding(a,pub['audit'],pub['dispatch'])
  if sys.argv[2]=='readiness':result=readiness(a,s,None,True,None)
  elif sys.argv[2]=='context':
   projection=derive(json.loads(a.context_projection),a.context_binding)
   before=Path(pub['audit']).read_bytes();life=reconstruct(before,a,Path(pub['audit']));act=actions(Path(pub['audit']),a)
   fd=os.open(a.ownership_ledger,os.O_RDONLY|os.O_NOFOLLOW)
   try:
    ledger=_read(fd);owner=invocation(fd);scope=InvocationOwnership.__new__(InvocationOwnership)._history(fd)
    assert ledger==_read(fd)
   finally:os.close(fd)
   assert before==Path(pub['audit']).read_bytes()
   mutable={p:r['new_sha256'] for p,r in g.changes.items()};mutable.update({p:r['sha256'] for p,r in g.supplement['inputs'].items()})
   for source in a.context_binding.sources.values():
    path=str(a.context_binding.repos[source['repository']]/source['path']);mutable[path]=g.current_hash(path,source['sha256'])
   mutable[pub['audit']]=sha(before)
   result={'governance':g.__dict__,'mutable':mutable,'context':projection,'dispatch':json.loads(s.resolve(pub['dispatch']['authority_id'])),
    'authorization':json.loads(s.resolve(a.authorization_id)),'terminal':{'lifecycle':life,'actions':act,'ownership':owner,'scope':scope,'audit':pub['audit'],'audit_sha256':sha(before),'ledger_sha256':sha(ledger)}}
  else:raise ValueError('unknown read-only operation')
  result['immutable_witness']=dict(witness)
print(canonical(result));s.close()
