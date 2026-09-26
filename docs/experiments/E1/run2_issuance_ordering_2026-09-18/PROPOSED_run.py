"""Architect-authorized invocation orchestration; no production implementation changes."""
import json,os,sys,time
from pathlib import Path
from adapter.context_projection import canonical,digest,sha
from adapter.controller_authority_store import ControllerAuthorityStore,_directory,_put,_read,encoded,outside
from adapter.authority_bootstrap import reconstruct_authorization
from adapter.run2_context import verify_dispatch
from adapter.authorization_lifecycle import dispatch_binding
from adapter.activation_transaction import ActivationTransaction
from adapter.governed_host import GovernedHost
O=Path(__file__).resolve().parent.parent/'run2_dispatch_2026-09-18'
P=O.parent/'run2_release_s3_publication_2026-09-17'
F=O.parent/'run2_nonhost_closure_2026-09-17'
A='auth-e1-wp-001-r8-3251a47bce19fcec0dab883d9e5e6c56'
B=Path('/tmp/kge-forge-controller-authority')/A/'dispatch-2026-09-18'
def load(p):return json.loads(Path(p).read_bytes())
def save(p,v):
 b=canonical(v).encode();fd=_directory(p.parent)
 try:_put(fd,p.name,b);os.fsync(fd)
 finally:os.close(fd)
 return {'path':str(p),'sha256':sha(b)}
def report(n,v):
 with (O/n).open('xb') as f:f.write(canonical(v).encode())
 print(n+': '+canonical(v),flush=True)
mode=sys.argv[1]
if mode=='prepare':
 d=load(P/'PROPOSED_RUN2_DISPATCH_BINDINGS.json')
 assert d['succession_head']=='SupervisorSuccession-sha256:b86bbb15d9d9d468b2de87926ad6b1cb4063218fd71eb5426089f689c0aecce8'
 assert d['invocation_identity']['authorization_id']==A
 assert d['release_authority']=='E1-RELEASE-AUTHORITY-sha256:c43f1191e2b631bb42bb1c48aaa6ba9a96d286bd169f93a8fac315c4cdb20286'
 assert d['context_identities']['ModelPayloadDigest']=='d675d581c80f43e691a31da73ccf17fd4bcc6b00d3a5331f26b9294e294e1538'
 for n,h in load(F/'PACKAGE_MANIFEST.json').items():assert sha((F/n).read_bytes())==h,n
 inv=load(F/'FINAL_IMPLEMENTATION.json');assert inv['identity']==d['implementation_identity']
 for p,h in inv['inventory'].items():assert sha(Path(p).read_bytes())==h,p
 pin=load(P/'CURRENT_PIN.json');assert pin==d['current_private_publication'];raw=Path(pin['path']).read_bytes();assert sha(raw)==pin['sha256']
 old=ControllerAuthorityStore(**json.loads(raw)['selected_store'])
 audit=Path(d['all_authorized_bindings']['audit']);assert not audit.exists() or audit.read_bytes()==b''
 with old.session():
  auth=reconstruct_authorization(old,A);g=auth.context_binding.governance
  assert g.run2['release_authority']==d['release_authority'] and g.run2['release_decision']==d['release_decision_id']
  op=json.loads(auth.operational_binding)
  assert op['context_identities']==d['context_identities'] and op['governance']['identities']==d['operational_identities']
  assert digest(op)==d['all_authorized_bindings']['operational_binding_sha256']
  assert op['governance']['released_profile']['sha256']==d['profile_sha256']
  transport=json.loads(auth.model_transport);assert bool(os.environ.get(transport['credential_environment_reference'])),'released credential unavailable'
  sel=json.loads(old.resolve(A+':run2-context'));pol=json.loads(old.resolve(A+':supervisor-succession'))
  assert pol['pinned_head']==d['succession_head']
  from adapter.supervisor_amendment import readiness
  from adapter.activation_transaction import _host
  ready=readiness(auth,old,pol['released_supervisor'],True,_host)
  assert ready['SupervisorInstanceId']==d['current_supervisor']
 outside(B,old.catalog['programmer_roots']);B.mkdir(mode=0o700)
 extras={}
 def add(v,alias=None):
  b=canonical(v).encode();h=sha(b);extras['sha256:'+h]=b
  if alias:extras[alias]=b
  return {'authority_id':'sha256:'+h,'sha256':h}
 expected={'authority':'Architect','decision':'DISPATCH_AUTHORIZED','release_authority':d['release_authority'],'release_decision':d['release_decision_id'],
  'ModelPayloadDigest':d['context_identities']['ModelPayloadDigest'],'invocation_identity':d['invocation_identity']}
 source=dict(expected,channel='user',binding_sha256=digest(d['all_authorized_bindings']))
 sr=add(source)
 decision=dict(expected,authority_source=sr,all_authorized_bindings=d['all_authorized_bindings'],work_package_id=d['work_package_id'],released_profile_sha256=d['profile_sha256'],
  current_supervisor=d['current_supervisor'],succession_head=d['succession_head'],material_amendment=d['material_amendment'],implementation_identity=d['implementation_identity'],
  budget_policy_identity=d['budget_policy_identity'],transmission_retention_identity=d['transmission_retention_identity'],authorized_request_identity=d['id'],
  **d['operational_identities'],**{k:v for k,v in d['context_identities'].items() if k!='ModelPayloadDigest'})
 ref='E1-ARCHITECT-DISPATCH-sha256:'+digest(decision);dr=add(decision,ref)
 dr['authority_id']=ref;sel['dispatch_decision']=dr;pol['dispatch_amendment']=ref
 add(sel,A+':run2-context');add(pol,A+':supervisor-succession')
 root=B/'authority';root.mkdir(mode=0o700);cat=json.loads(encoded(old.catalog));fd=_directory(root)
 try:
  for h in sorted({v['sha256'] for v in cat['objects'].values()}):_put(fd,h,_read(old.fd,h))
  for ident,b in extras.items():
   h=sha(b)
   if not (root/h).exists():_put(fd,h,b)
   cat['objects'][ident]={'sha256':h,'evidence':[],'authority_source':sr,'release_identities':d['operational_identities'],'temporal_applicability':old.applicability,'mutation':'IMMUTABLE'}
  cat['private_state'][A+':audit']={'path':str(audit),'mutation':'APPEND_ONLY','mechanism':'GovernedHost/ActivationTransaction/RunControl'}
  _put(fd,'catalog.json',canonical(cat).encode());os.fsync(fd)
 finally:os.close(fd)
 selected={'root':str(root),'catalog_sha256':digest(cat),'applicability':old.applicability};old.close()
 st=ControllerAuthorityStore(**selected)
 with st.session():
  auth=reconstruct_authorization(st,A);verify_dispatch(auth,decision);dispatch_binding(auth,audit,dr)
 st.close()
 publication={'selected_store':selected,'dispatch_ref':ref,'dispatch_record':decision,'predecessor_publication':pin,'corrected_succession':d['succession_head'],'audit':str(audit)}
 p=save(B/'DISPATCH_PUBLICATION.json',publication);report('CURRENT_PIN.json',p)
 report('DISPATCH_PUBLICATION.json',{'dispatch_ref':ref,'publication':p,'validation':'PASS','activation':False,'model_requests':0})
else:
 p=load(O/'CURRENT_PIN.json');b=Path(p['path']).read_bytes();assert sha(b)==p['sha256'];pub=json.loads(b)
 st=ControllerAuthorityStore(**pub['selected_store']);audit=Path(pub['audit']);begin=time.monotonic()
 with st.session():
  if mode=='dispatch':
   from adapter.controlled_dispatch import dispatch
   try:
    result=dispatch(st,A);save(B/'PROGRAMMER_RESULT.json',result)
    report('DISPATCH_RETURN.json',{'status':result.get('status'),'seconds':time.monotonic()-begin,'private_result':str(B/'PROGRAMMER_RESULT.json')})
   except BaseException as exc:
    report('DISPATCH_EXCEPTION.json',{'type':type(exc).__name__,'message':str(exc),'seconds':time.monotonic()-begin});raise
  else:
   from adapter.run_control import RunControl
   from adapter.validation_spans import recording
   from issuance import issue_inactive, start_control
   # Bootstrap and dispatch checks occur before authorization-bound telemetry.
   with recording(None):auth=reconstruct_authorization(st,A)
   raw=json.loads(st.resolve(A))
   if mode=='activate':
    dispatch_ref={'authority_id':pub['dispatch_ref'],'sha256':pub['dispatch_ref'].split(':')[-1]}
    issue_inactive(auth,audit,dispatch_ref)
   control=start_control(auth,audit,json.loads(raw['model_transmission'])['run_control'])
   if mode=='activate':
    with recording(control),control.span('activation'):tx=ActivationTransaction.activate(auth,audit,pub['dispatch_ref'])
    try:report('ACTIVATION.json',{'state':tx.auth.state,'reservation':tx.reservation,'seconds':time.monotonic()-begin})
    finally:tx.close()
   elif mode=='recover':
    with recording(control),control.span('independent_activation_recovery'):tx=ActivationTransaction.recover(auth,audit,pub['dispatch_ref'])
    try:report('INDEPENDENT_RECOVERY.json',dict(tx.recovery,seconds=time.monotonic()-begin))
    finally:tx.close()
   else:raise ValueError(mode)
 st.close()
