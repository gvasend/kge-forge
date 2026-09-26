"""Read-only negatives on the exact prepared production context."""
import json,sys,os,time
from pathlib import Path
from dataclasses import replace
from unittest.mock import patch
sys.path.insert(0,json.loads((Path(sys.argv[1])/'PREPARED_PUBLICATION.json').read_bytes())['runtime_root'])
from adapter.controller_authority_store import ControllerAuthorityStore
from adapter.authority_bootstrap import reconstruct_authorization
from adapter.context_projection import canonical,digest
from adapter.governance_continuation import verify_authorization
from adapter.authorization_lifecycle import dispatch_binding
from adapter.attempt_chain import decision,ancestry,require_issued
out=Path(sys.argv[1]);pub=json.loads((out/'PREPARED_PUBLICATION.json').read_bytes());s=ControllerAuthorityStore(**pub['selected_store']);results=[]
def denied(name,f):
 start=time.monotonic()
 try:f()
 except (ValueError,RuntimeError,OSError,KeyError) as e:results.append({'name':name,'result':'REJECTED','reason':str(e),'seconds':time.monotonic()-start})
 else:raise AssertionError(name+' accepted')
with s.session():
 a=reconstruct_authorization(s,s.applicability['authorization_id']);g=a.context_binding.governance
 for k,v in [('authorization_id','auth-e1-arbitrary-r11'),('work_package_id','OTHER-TASK'),('read_roots',('/arbitrary',)),('model_transmission','{}'),('execution_profile','{}')]:
  denied('authorization_'+k,lambda k=k,v=v:verify_authorization(replace(a,**{k:v})))
 original=s.resolve
 selection=g.run7['selection'];ar=g.run7['amendment'];continuation=g.run7['continuation']
 targets={'missing_amendment':g.spec['amendment']['authority_id'],'missing_proposal':ar['proposal']['authority_id'],
  'missing_original_dispatch':ar['parent_dispatch']['authority_id'],'missing_continuation':g.spec['continuation']['authority_id']}
 for name,key in targets.items():
  def missing(k):
   if k==key:raise ValueError('synthetic missing private object')
   return original(k)
  with patch.object(s,'resolve',side_effect=missing):denied(name,lambda:decision(g.spec))
 for field in ('ModelPayloadDigest','released_profile_sha256','budget_policy_identity','transmission_retention_identity','release_authority','succession_head','work_package_id'):
  d=json.loads(original(pub['dispatch']['authority_id']));d[field]='substituted'
  fake={'authority_id':'E1-ARCHITECT-DISPATCH-sha256:'+digest(d),'sha256':digest(d)}
  with patch.object(s,'resolve',side_effect=lambda k,d=d,fake=fake:canonical(d).encode() if k==fake['authority_id'] else original(k)):
   denied('dispatch_'+field,lambda:dispatch_binding(a,g.run7['proposal']['audit'],fake))
 # Exact selection cannot be reordered to the old material context.
 selkey=a.authorization_id+':attempt-chain';wrong=dict(selection,amendment=g.run7['predecessor']['governance']['spec']['amendment'])
 with patch.object(s,'resolve',side_effect=lambda k:canonical(wrong).encode() if k==selkey else original(k)):
  denied('reordered_attempt_ancestry',lambda:decision(g.spec))
 # Private checkpoint presence and specific authorization remain required.
 with patch.object(s,'resolve',side_effect=lambda k:(_ for _ in ()).throw(ValueError('missing checkpoint')) if k==ar['predecessor_capture']['authority_id'] else original(k)):
  denied('missing_immutable_predecessor_capture',lambda:g.verify())
 denied('specific_issuance_absent',lambda:require_issued(a))
 assert not os.path.lexists(g.run7['proposal']['audit'])
s.close();(out/'NEGATIVE_CONTEXT.json').write_text(canonical({'result':'PASS','probes':results,'issued':False,'model_requests':0}));print(len(results))
