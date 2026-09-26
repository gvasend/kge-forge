"""Publish the specific user-authorized r9 grant, never lifecycle issuance."""
import json,os,time
from pathlib import Path
from adapter.context_projection import canonical,sha,digest
from adapter.controller_authority_store import ControllerAuthorityStore,_directory,_put,_read,encoded,outside
from adapter.authority_bootstrap import reconstruct_authorization
from adapter.attempt_context import derive_dispatch
O=Path('/home/gvasend/app/kge-forge/docs/experiments/E1/run2_r9_dispatch_2026-09-18')
def save(path,v):
 b=canonical(v).encode();fd=_directory(path.parent)
 try:_put(fd,path.name,b);os.fsync(fd)
 finally:os.close(fd)
 return {'path':str(path),'sha256':sha(b)}
pub=json.loads((O/'PREPARED_PUBLICATION.json').read_bytes());pre=json.loads((O/'PREFLIGHT.json').read_bytes())
assert pre['result']=='PASS_PENDING_SPECIFIC_ARCHITECT_ISSUANCE'
expected={'amendment_id':'E1-RUN2-ATTEMPT-AUTHORITY-AMENDMENT-sha256:2698e91a74ffe563c5ebd52e9f9be9d90a055dcabc569fd3a2b159d545964566',
 'continuation_id':'CONTINUATION-sha256:b65358caaf9d2f4aa6e6e2a15aabc488cd7a26c56539594193a220923f8b0fd4',
 'release_authority':'E1-RELEASE-AUTHORITY-sha256:a8e228850a699e201cd2202b76c6de7de976e7aa34890f3247afda4a599f0708'}
assert all(pub[k]==v for k,v in expected.items())
assert pub['amendment']['sha256']=='d465d852b4e819fa82ba4d25667ef55491c50a53e86877475bb412203ba4a983'
assert pub['continuation']['sha256']=='1a31ae31bd73a194b565a551396b4154e635bbd9060ec3cb2cdb6359e6d60b40'
assert pub['operational_identities']['OperationalContextId']=='E1-OPERATIONAL-CONTEXT-sha256:9814f88f64b966a633d0fcc5142a2bfdb1564c8f92f5c07e81455ff1414c58ce'
assert pub['operational_identities']['continuation_chain_digest']=='45d9e90c1308d1f73b5c3d347e6a567ecf557a42fb2c486a2dc61c316deff0e9'
A='auth-e1-wp-001-r9-6fad26f3eb6113d5cd4f0237d2b6f224';assert pub['r9_authorization_id']==A
s=ControllerAuthorityStore(**pub['selected_store'])
with s.session():
 a=reconstruct_authorization(s,A);g=a.context_binding.governance;p=g.run5['proposal']
 assert pub['proposal']['sha256']=='cb68a30719e88496504cd38004750b5b6848e4f31f1836387b87984ae92a8adc'
 assert not os.path.lexists(p['audit']);assert s.state_path(p['DispatchAuthorizationId']+':attempt-ledger').read_bytes()==b''
 transport=json.loads(a.model_transport);assert bool(os.environ.get(transport['credential_environment_reference'])),'released credential unavailable'
 selection=json.loads(s.resolve(A+':attempt-context'));assert selection['mode']=='PREPARED' and selection['specific_invocation_authorization'] is None
extras={}
def add(v,alias=None):
 b=canonical(v).encode();h=sha(b);extras['sha256:'+h]=b
 if alias:extras[alias]=b
 return {'authority_id':'sha256:'+h,'sha256':h}
body={'authority':'Architect','decision':'AUTHORIZE_SPECIFIC_REPLACEMENT_INVOCATION','proposal':pub['proposal'],
 'DispatchAuthorizationId':p['DispatchAuthorizationId'],'InvocationAttemptId':p['InvocationAttemptId'],'automatic_retry':False}
sr=add(dict(body,channel='user'))
attribution=add({'schema':'ARCHITECT-R9-ISSUANCE-AUTHORIZATION-1','authority':'Architect','channel':'user',
 'decision':'r9 ISSUANCE, ACTIVATION, AND RUN-2 DISPATCH AUTHORIZED','normalized_authority_source':sr,
 'invocation_authorization_id':A,'proposal':pub['proposal'],'authority_basis':expected,'amendment':pub['amendment'],
 'continuation':pub['continuation'],'operational_identities':pub['operational_identities'],'context_identities':pub['context_identities'],
 'predecessor_disposition':'UNISSUED_PROPOSED_AUTHORIZATION_WITH_FAILED_CLOSED_AUDIT_NAMESPACE',
 'scope':'Exact r9 only; qualified gates and released budgets; no automatic replacement attempt',
 'recorded_wall_time':time.time()})
approval=dict(body,authority_source=sr,attributable_decision=attribution)
ar=add(approval,p['DispatchAuthorizationId']+':replacement-approval')
selection.update(mode='ISSUED',specific_invocation_authorization=ar);add(selection,A+':attempt-context')
child=json.loads(s.resolve(pub['dispatch']['authority_id']));assert child['decision']=='PROPOSED_DISPATCH';child['decision']='DISPATCH_AUTHORIZED'
did='E1-ARCHITECT-DISPATCH-sha256:'+digest(child);dr=add(child,did);dr['authority_id']=did
base=Path('/tmp/kge-forge-controller-authority')/A/'authorized-invocation-2026-09-18';outside(base,s.catalog['programmer_roots']);base.mkdir(mode=0o700)
root=base/'authority';root.mkdir(mode=0o700);cat=json.loads(encoded(s.catalog));fd=_directory(root)
try:
 for h in sorted({v['sha256'] for v in cat['objects'].values()}):_put(fd,h,_read(s.fd,h))
 for key,b in extras.items():
  h=sha(b)
  if not (root/h).exists():_put(fd,h,b)
  cat['objects'][key]={'sha256':h,'evidence':[],'authority_source':sr,'release_identities':pub['operational_identities'],
   'temporal_applicability':dict(s.applicability),'mutation':'IMMUTABLE'}
 _put(fd,'catalog.json',canonical(cat).encode());os.fsync(fd)
finally:os.close(fd)
selected={'root':str(root),'catalog_sha256':digest(cat),'applicability':dict(s.applicability)};s.close()
st=ControllerAuthorityStore(**selected)
with st.session():
 a=reconstruct_authorization(st,A);assert derive_dispatch(a)==child
 from adapter.attempt_context import require_issued
 require_issued(a)
st.close()
publication=dict(pub,status='SPECIFIC_R9_AUTHORIZED_NOT_LIFECYCLE_ISSUED',selected_store=selected,dispatch=dr,
 specific_Architect_issuance_authorization=ar,attributable_decision=attribution,audit=p['audit'],private_run_root=str(base))
pin=save(base/'ISSUANCE_PUBLICATION.json',publication)
(O/'CURRENT_PIN.json').write_text(canonical(pin));(O/'ISSUANCE_AUTHORITY.json').write_text(canonical({'approval':ar,'attribution':attribution,'dispatch':dr,'publication':pin,'issued':False}))
print(canonical({'specific_authorization':'PUBLISHED','issued':False,'publication':pin}))
