"""Apply only the exact user-authorized r12 records; never issue lifecycle."""
import json,os,time,sys
from pathlib import Path
sys.path.insert(0,'/tmp/forge-attempt-chain-xjcb_jkz')
from adapter.context_projection import canonical,sha,digest,derive
from adapter.controller_authority_store import ControllerAuthorityStore,_directory,_put,_read,encoded,outside
from adapter.authority_bootstrap import reconstruct_authorization
from adapter.attempt_chain import derive_dispatch,require_issued
O=Path(__file__).parent
pub=json.loads((O/'PREPARED_PUBLICATION.json').read_bytes());pre=json.loads((O/'PREFLIGHT.json').read_bytes())
assert pre['result']=='PASS' and pre['audit_unused'] and not pre['issued']
expected={'amendment_id':'E1-RUN2-ATTEMPT-CHAIN-AMENDMENT-sha256:b8537c0dc64c70de49e29c76a650d44e05d234ba6814c5de4d43f662fa950e8f',
 'continuation_id':'CONTINUATION-sha256:cc0fb1818f524d999fc4efbd76b735b53aedd7f7f19aed74464b35470d9430bd',
 'release_authority':'E1-RELEASE-AUTHORITY-sha256:84b7294bef3e2ccdbae8364b66f202135fcc9def9dd0081b473f847b4636628d'}
assert all(pub[k]==v for k,v in expected.items())
assert pub['amendment']['sha256']=='62a7b65dda8c0c76755967522943d3a1c09e825b714618a3ba5f338d17ba71fe'
assert pub['continuation']['sha256']=='1e1382b569effdcd5b1aad401adf9eb695dca26c8914211ad890f43f94269286'
assert pub['operational_identities']['OperationalContextId']=='E1-OPERATIONAL-CONTEXT-sha256:a59e21566098fee1756bbe991f74e0d2c8c5b756a76d90877911c35d57044a8a'
assert pub['proposal']['sha256']=='39319b6dab6320b3b373a8049f1ae5dee7f7318a71e7491a3643faf3582cb54d'
A='auth-e1-wp-001-r12-86af4f6e7bb64eb384108dec11692c86';s=ControllerAuthorityStore(**pub['selected_store'])
with s.session():
 a=reconstruct_authorization(s,A);g=a.context_binding.governance;p=g.run7['proposal'];body={'authority':'Architect','decision':'ADOPT_EXACT_ATTEMPT_CHAIN_AND_AUTHORIZE_SPECIFIC_INVOCATION','proposal':g.run7['amendment']['proposal'],'amendment':g.spec['amendment'],'continuation':g.spec['continuation'],'release_authority':g.run7['release_authority'],**g.identities,'predecessors':p['predecessors'],'automatic_retry':False}
 assert not os.path.lexists(p['audit']);selection=json.loads(s.resolve(A+':attempt-chain'));assert selection['mode']=='PREPARED'
 q=json.loads(s.resolve(pub['qualification']['authority_id']))
 for path,h in json.loads((O/'HISTORICAL_BASELINE.json').read_bytes()).items():assert sha(Path(path).read_bytes())==h
 for path,h in q['evidence'].items():assert sha((O.parent/'run2_r12_semantic_evidence_2026-09-18'/path).read_bytes())==h
 transport=json.loads(a.model_transport);assert bool(os.environ.get(transport['credential_environment_reference'])),'released credential unavailable'
extras={}
def add(v,alias=None):
 b=canonical(v).encode();h=sha(b);extras['sha256:'+h]=b
 if alias:extras[alias]=b
 return {'authority_id':'sha256:'+h,'sha256':h}
sr=add(dict(body,channel='user'));grant=add(dict(body,authority_source=sr))
attribution=add({'schema':'ARCHITECT-R12-AUTHORITY-APPLICATION-AND-ISSUANCE-1','authority':'Architect','channel':'user',
 'decision':'r12 AUTHORITY APPLICATION, ISSUANCE, ACTIVATION, AND E1-WP-001 DISPATCH AUTHORIZED',
 'normalized_authority_source':sr,'specific_grant':grant,'invocation_authorization_id':A,'proposal':pub['proposal'],
 'authority_basis':expected,'amendment':pub['amendment'],'continuation':pub['continuation'],'operational_identities':pub['operational_identities'],
 'context_identities':pub['context_identities'],'historical_attempts':{'r8':'CLOSED_UNISSUED','r9':'CANCELLED / INTERRUPTED_NO_EFFECTS','r10':'CANCELLED / INTERRUPTED_NO_EFFECTS','r11':'CANCELLED / INTERRUPTED_NO_EFFECTS'},
 'scope':'Exact r12 only; apply exact prepared records, enforce qualified gates and unchanged budgets; no automatic r13',
 'recorded_wall_time':time.time()})
selection.update(mode='ISSUED',specific_invocation_authorization=grant);add(selection,A+':attempt-chain')
child=json.loads(s.resolve(pub['dispatch']['authority_id']));assert child['decision']=='PROPOSED_DISPATCH';child['decision']='DISPATCH_AUTHORIZED'
did='E1-ARCHITECT-DISPATCH-sha256:'+digest(child);dr=add(child,did);dr['authority_id']=did
base=Path('/tmp/kge-forge-controller-authority')/A/'authorized-invocation-2026-09-18';outside(base,s.catalog['programmer_roots']);base.parent.mkdir(mode=0o700);base.mkdir(mode=0o700)
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
publication=dict(pub,status='APPLIED_SPECIFIC_R12_AUTHORIZED_NOT_LIFECYCLE_ISSUED',selected_store=selected,dispatch=dr,
 specific_Architect_issuance_authorization=grant,attributable_decision=attribution,audit=p['audit'],private_run_root=str(base),r12_authorization_id=A)
b=canonical(publication).encode();fd=_directory(base)
try:_put(fd,'ISSUANCE_PUBLICATION.json',b);os.fsync(fd)
finally:os.close(fd)
pin={'path':str(base/'ISSUANCE_PUBLICATION.json'),'sha256':sha(b)}
(O/'CURRENT_PIN.json').write_text(canonical(pin));(O/'AUTHORITY_APPLICATION.json').write_text(canonical({'result':'APPLIED','amendment':pub['amendment'],'continuation':pub['continuation'],'grant':grant,'attribution':attribution,'publication':pin,'lifecycle_issued':False}));print(canonical({'applied':expected,'issued':False,'publication':pin}))
