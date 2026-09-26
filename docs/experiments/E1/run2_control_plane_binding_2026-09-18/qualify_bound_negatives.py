"""Fresh bound-context negatives; no audit/ledger mutation or provider calls."""
import json,sys,time
from dataclasses import replace
from pathlib import Path
O=Path(__file__).resolve().parent;p=json.loads((O/'QUALIFICATION_BINDINGS.json').read_bytes())[0];sys.path.insert(0,p['runtime_root'])
from adapter.controller_authority_store import ControllerAuthorityStore
from adapter.authority_bootstrap import reconstruct_authorization
from adapter.control_plane_binding import verify_authorization,forbid_effect,readiness
from adapter.context_projection import canonical,read_exact
from adapter.activation_transaction import _host
s=ControllerAuthorityStore(**p['selected_store']);rows=[]
def rejects(name,fn):
 try:fn()
 except (ValueError,KeyError,OSError) as e:rows.append({'probe':name,'result':'PASS_REJECTED','reason':str(e)})
 else:raise AssertionError('accepted '+name)
try:
 with s.session():
  a=reconstruct_authorization(s,p['authorization_id']);verify_authorization(a)
  for key,value in [('authorization_id','qualification-control-plane-arbitrary'),('work_package_id','substituted'),('ownership_ledger','/tmp/alternate-unbound-ledger'),('model_transmission','{}'),('execution_profile','{}'),('state','COMPLETED')]:
   rejects('substituted_'+key,lambda k=key,v=value:verify_authorization(replace(a,**{k:v})))
  rejects('real_model_or_governed_effect',lambda:forbid_effect(a))
  rejects('unknown_private_identity',lambda:s.resolve('unknown'))
  b=a.context_binding.governance.run8['binding'];ref=b['supervisor_verification'];bad=dict(ref,sha256='0'*64)
  from adapter.control_plane_binding import read
  rejects('substituted_supervisor_verification_ref',lambda:read(bad))
  started=time.monotonic();live=readiness(a,s,None,True,_host);rows.append({'probe':'fresh_same_S3','result':'PASS','seconds':time.monotonic()-started,'observation':live})
 (O/'BOUND_NEGATIVES.json').write_text(canonical({'result':'PASS','probes':rows,'model_requests':0,'effects':0}))
finally:s.close()
print(canonical({'result':'PASS','probes':len(rows)}))
