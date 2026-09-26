"""Read-only actual-context substitution probes; never writes lifecycle state."""
import json,sys,os,time
from pathlib import Path
from unittest.mock import patch
from dataclasses import replace
from adapter.context_projection import canonical,sha
from adapter.controller_authority_store import ControllerAuthorityStore
from adapter.authority_bootstrap import reconstruct_authorization
from adapter.governance_continuation import verify_authorization
from adapter.attempt_context import decision,verify_dispatch
from adapter.authorization_lifecycle import dispatch_binding
from adapter.invocation_issuance import issue_inactive
from adapter.controlled_dispatch import dispatch
run=Path(sys.argv[1]);pub=json.loads((run/'PREPARED_PUBLICATION.json').read_bytes());store=ControllerAuthorityStore(**pub['selected_store']);results=[]
def denied(name,fn):
 t=time.monotonic()
 try:fn()
 except (ValueError,FileNotFoundError,KeyError) as e:results.append({'probe':name,'result':'REJECTED','type':type(e).__name__,'reason':str(e),'seconds':time.monotonic()-t})
 else:raise AssertionError('accepted '+name)
with store.session():
 a=reconstruct_authorization(store,store.applicability['authorization_id']);g=a.context_binding.governance;p=g.run5['proposal'];audit=Path(p['audit'])
 snapshots={x:Path(x).read_bytes() for x in (p['predecessor']['audit'],a.ownership_ledger)}
 assert not os.path.lexists(audit)
 original=store.resolve
 refs={'material_amendment':g.spec['amendment'],'continuation':g.spec['continuation'],
  'parent_dispatch':g.run5['amendment']['parent_dispatch'],'accepted_proposal':g.run5['amendment']['proposal'],
  'material_Architect_decision':g.run5['amendment']['authority_source'],'runtime_inventory':g.run5['amendment']['controller_runtime'],
  'released_profile':g.spec['released_profile']}
 for name,ref in refs.items():
  def missing(k,ref=ref):
   if k==ref['authority_id']:raise FileNotFoundError('synthetic missing selected object')
   return original(k)
  with patch.object(store,'resolve',side_effect=missing):denied('missing_'+name,lambda:dispatch_binding(a,audit,pub['dispatch']))
  def substituted(k,ref=ref):return b'{}' if k==ref['authority_id'] else original(k)
  with patch.object(store,'resolve',side_effect=substituted):denied('hash_substitution_'+name,lambda:dispatch_binding(a,audit,pub['dispatch']))
 for field,value in [('authorization_id','synthetic-arbitrary-r10'),('work_package_id','other-task'),('model_transmission','{}'),('revision',10)]:
  denied('authorization_substitution_'+field,lambda field=field,value=value:verify_authorization(replace(a,**{field:value})))
 d=json.loads(original(pub['dispatch']['authority_id']))
 for field in ('release_authority','current_supervisor','succession_head','ModelPayloadDigest','budget_policy_identity','transmission_retention_identity','implementation_identity'):
  bad=dict(d);bad[field]='synthetic-substitution'
  denied('dispatch_substitution_'+field,lambda bad=bad:verify_dispatch(a,bad))
 for field in ('OperationalContextId','continuation_chain_digest'):
  bad=json.loads(a.operational_binding);bad['governance']['identities'][field]='synthetic-stale-ancestry'
  denied('stale_'+field,lambda bad=bad:verify_authorization(replace(a,operational_binding=canonical(bad))))
 denied('issuance_without_specific_Architect_decision',lambda:issue_inactive(a,audit,pub['dispatch']))
 denied('handoff_before_recovered_ACTIVE',lambda:dispatch(store,a.authorization_id))
 assert not os.path.lexists(audit)
 assert all(Path(k).read_bytes()==v for k,v in snapshots.items())
 result={'result':'PASS','schema':'ACTUAL-PREPARED-CONTEXT-NEGATIVE-QUALIFICATION-1','probes':results,'model_requests':0,'effects':0,'real_issuance':False,'r8_immutable':True,'r9_audit_unused':True}
 (run/'NEGATIVE_PROBES.json').write_text(canonical(result));print(canonical({'result':'PASS','probes':len(results)}))
store.close()
