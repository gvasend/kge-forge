"""Capture pure supervisor-authority verification through its original runtime.
All live observations remain fresh in consumers; this is not a readiness cache.
"""
import json,sys,time
from pathlib import Path
O=Path(__file__).resolve().parent
proof=json.loads((O/'R12_AUTHENTICATED_CAPTURE.json').read_bytes());node=proof
while 'run7' in node['governance'] or 'run6' in node['governance']:
 g=node['governance'];node=g.get('run7',g.get('run6'))['predecessor']
a=node['governance']['run5']['amendment'];pin=a['predecessor_publication'];conf=a['predecessor_verifier']
sys.path.insert(0,conf['repository'])
from adapter.context_projection import canonical,sha,digest,read_exact
from adapter.controller_authority_store import ControllerAuthorityStore
from adapter.authority_bootstrap import reconstruct_authorization
from adapter.run2_context import supervisor_policy,supervisor_readiness
from adapter.supervisor_succession import reconstruct
from adapter.activation_transaction import _host
pub=json.loads(read_exact(pin['path'],pin['sha256']));s=ControllerAuthorityStore(**pub['selected_store']);start=time.monotonic()
try:
 with s.session():
  reconstruct_authorization(s,s.applicability['authorization_id'])
 with s.session(),s.witness() as witness:
  auth=reconstruct_authorization(s,s.applicability['authorization_id']);policy=supervisor_policy(auth,s)
  ledger=s.state_path(policy['ledger_id']);data=ledger.read_bytes();selected=reconstruct(s,policy,data)
  host=supervisor_readiness(auth,s,None,True,_host)
  assert host['SupervisorInstanceId']==selected['instance']['id']
  g=auth.context_binding.governance
  mutable={p:r['new_sha256'] for p,r in g.changes.items()};mutable.update({p:r['sha256'] for p,r in g.supplement['inputs'].items()})
  for source in auth.context_binding.sources.values():
   path=str(auth.context_binding.repos[source['repository']]/source['path']);mutable[path]=g.current_hash(path,source['sha256'])
  current_runtime={str(p):sha(p.read_bytes()) for p in Path(conf['repository'],'adapter').glob('*.py')}
  for p,h in mutable.items():read_exact(p,h)
  for packed,h,inner in getattr(s,'_run2_verified_history',{}).values():witness.update(inner)
  result={'schema':'SUPERVISOR-IMMUTABLE-VERIFICATION-1','producer':{'path':str(Path(__file__).resolve()),'sha256':sha(Path(__file__).read_bytes()),'python':sys.executable,'python_sha256':sha(Path(sys.executable).read_bytes()),'implementation':current_runtime},
   'parent_publication':pin,'selected_store':pub['selected_store'],'immutable_witness':dict(witness),'mutable':mutable,
   'succession_ledger':{'path':str(ledger),'sha256':sha(data),'logical_identity':policy['ledger_id']},
   'policy':policy,'instance':selected['instance'],'head':selected['head'],'original_readiness':host,
   'reuse_scope':'PURE_AUTHORITY_VERIFICATION_ONLY_FRESH_KERNEL_AND_HEAD_REQUIRED','seconds':time.monotonic()-start}
  result['id']='SUPERVISOR-IMMUTABLE-VERIFICATION-sha256:'+digest(result)
  assert ledger.read_bytes()==data
  (O/'SUPERVISOR_IMMUTABLE_VERIFICATION.json').write_text(canonical(result))
  print(canonical({'identity':result['id'],'seconds':result['seconds'],'S3':host['SupervisorInstanceId']}))
finally:s.close()
