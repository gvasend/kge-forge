"""Apply only the exact user-authorized r10 records; never issue lifecycle."""
import json,os,time,sys
from pathlib import Path
sys.path.insert(0,'/tmp/forge-r10-transition-jxppjwou')
from adapter.context_projection import canonical,sha,digest,derive
from adapter.controller_authority_store import ControllerAuthorityStore,_directory,_put,_read,encoded,outside
from adapter.authority_bootstrap import reconstruct_authorization
from adapter.attempt_transition import derive_dispatch,issuance_expectation,require_issued
O=Path(__file__).parent
pub=json.loads((O/'PREPARED_PUBLICATION.json').read_bytes());pre=json.loads((O/'PREFLIGHT.json').read_bytes())
assert pre['result']=='PASS_PROSPECTIVE_R10_PENDING_SPECIFIC_ARCHITECT_ISSUANCE'
expected={'amendment_id':'E1-RUN2-TERMINAL-ATTEMPT-AMENDMENT-sha256:5ea9aff23455234d856d8f16392323448b6e7fbd6f38ba049bccf810b1354d47',
 'continuation_id':'CONTINUATION-sha256:20caff43a3d75a1d78e288358a12a37bd871315584a8c33c9b1feceb98390cd6',
 'release_authority':'E1-RELEASE-AUTHORITY-sha256:c9b00cdf029e657936ba3e51fa8a3c9361e315483eeda58e428aff5f1c3b6d3c'}
assert all(pub[k]==v for k,v in expected.items())
assert pub['amendment']['sha256']=='6c96d18f737d91ced40fe81da74ee7f80b700d0ab1a0e3855cb221fab9bae855'
assert pub['continuation']['sha256']=='501230a6a068cd2b4d875f6014e5fcaea393c71ddaf8c365864c139a6e201bdd'
assert pub['operational_identities']['OperationalContextId']=='E1-OPERATIONAL-CONTEXT-sha256:109c1fb95fee2e95f58cce8ca7723384092706fa33a4ef7ec051abfdcacea125'
assert pub['proposal']['sha256']=='35fde13e12ee9318fca076c5a28aa898718e83074e65c3ada7f14e54830363e4'
A='auth-e1-wp-001-r10-4c92a8521b2f4c9986f948a1c83f5f10';s=ControllerAuthorityStore(**pub['selected_store'])
with s.session():
 a=reconstruct_authorization(s,A);g=a.context_binding.governance;p=g.run6['proposal'];body=issuance_expectation(a)
 assert not os.path.lexists(p['audit']);selection=json.loads(s.resolve(A+':terminal-attempt-context'));assert selection['mode']=='PREPARED'
 q=json.loads(s.resolve(pub['qualification']['authority_id']))
 for path,h in q['historical_hashes'].items():assert sha(Path(path).read_bytes())==h
 for path,h in q['evidence'].items():assert sha(Path(path).read_bytes())==h
 transport=json.loads(a.model_transport);assert bool(os.environ.get(transport['credential_environment_reference'])),'released credential unavailable'
extras={}
def add(v,alias=None):
 b=canonical(v).encode();h=sha(b);extras['sha256:'+h]=b
 if alias:extras[alias]=b
 return {'authority_id':'sha256:'+h,'sha256':h}
sr=add(dict(body,channel='user'));grant=add(dict(body,authority_source=sr))
attribution=add({'schema':'ARCHITECT-R10-AUTHORITY-APPLICATION-AND-ISSUANCE-1','authority':'Architect','channel':'user',
 'decision':'r10 AUTHORITY APPLICATION, ISSUANCE, ACTIVATION, AND E1-WP-001 DISPATCH AUTHORIZED',
 'normalized_authority_source':sr,'specific_grant':grant,'invocation_authorization_id':A,'proposal':pub['proposal'],
 'authority_basis':expected,'amendment':pub['amendment'],'continuation':pub['continuation'],'operational_identities':pub['operational_identities'],
 'context_identities':pub['context_identities'],'historical_attempts':{'r8':'CLOSED_UNISSUED','r9':'CANCELLED / INTERRUPTED_NO_EFFECTS'},
 'scope':'Exact r10 only; apply exact prepared records, enforce qualified gates and unchanged budgets; no automatic r11',
 'recorded_wall_time':time.time()})
selection.update(mode='ISSUED',specific_invocation_authorization=grant);add(selection,A+':terminal-attempt-context')
child=json.loads(s.resolve(pub['dispatch']['authority_id']));assert child['decision']=='PROPOSED_DISPATCH';child['decision']='DISPATCH_AUTHORIZED'
did='E1-ARCHITECT-DISPATCH-sha256:'+digest(child);dr=add(child,did);dr['authority_id']=did
base=Path('/tmp/kge-forge-controller-authority')/A/'authorized-invocation-2026-09-18';outside(base,s.catalog['programmer_roots']);base.mkdir(mode=0o700)
root=base/'authority';root.mkdir(mode=0o700);cat=json.loads(encoded(s.catalog));fd=_directory(root)
try:
 for h in sorted({r['sha256'] for r in cat['objects'].values()}):_put(fd,h,_read(s.fd,h))
 for key,b in extras.items():
  h=sha(b)
  if not (root/h).exists():_put(fd,h,b)
  cat['objects'][key]={'sha256':h,'evidence':[],'authority_source':sr,'release_identities':pub['operational_identities'],'temporal_applicability':s.applicability,'mutation':'IMMUTABLE'}
 _put(fd,'catalog.json',canonical(cat).encode());os.fsync(fd)
finally:os.close(fd)
selected={'root':str(root),'catalog_sha256':digest(cat),'applicability':s.applicability};s.close()
st=ControllerAuthorityStore(**selected)
with st.session():
 a=reconstruct_authorization(st,A);require_issued(a);assert derive_dispatch(a)==child
 d=derive(json.loads(a.context_projection),a.context_binding);assert {k:d[k] for k in pub['context_identities']}==pub['context_identities']
st.close()
publication=dict(pub,status='APPLIED_SPECIFIC_R10_AUTHORIZED_NOT_LIFECYCLE_ISSUED',selected_store=selected,dispatch=dr,
 specific_Architect_issuance_authorization=grant,attributable_decision=attribution,audit=p['audit'],private_run_root=str(base),r10_authorization_id=A)
b=canonical(publication).encode();fd=_directory(base)
try:_put(fd,'ISSUANCE_PUBLICATION.json',b);os.fsync(fd)
finally:os.close(fd)
pin={'path':str(base/'ISSUANCE_PUBLICATION.json'),'sha256':sha(b)}
(O/'CURRENT_PIN.json').write_text(canonical(pin));(O/'AUTHORITY_APPLICATION.json').write_text(canonical({'result':'APPLIED','amendment':pub['amendment'],'continuation':pub['continuation'],'grant':grant,'attribution':attribution,'publication':pin,'lifecycle_issued':False}));print(canonical({'applied':expected,'issued':False,'publication':pin}))
