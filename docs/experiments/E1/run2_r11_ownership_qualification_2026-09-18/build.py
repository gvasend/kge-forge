"""Construct PREPARED private authority; never issue an invocation."""
import json,os,sys,uuid,shutil,tempfile
from pathlib import Path
O=Path(__file__).parent
R=Path(tempfile.mkdtemp(prefix='forge-attempt-chain-'))
shutil.copytree(O/'candidate/adapter',R/'adapter',ignore=shutil.ignore_patterns('__pycache__'))
sys.path.insert(0,str(R))
from adapter.context_projection import canonical,digest,sha,derive
from adapter.controller_authority_store import ControllerAuthorityStore,encoded,_put,_directory,_read
from adapter.attempt_chain import RULES,ident,identities,derive_dispatch,predecessor_nodes
from adapter.continuation_envelope import seal
from adapter.context_binding import CommittedContext
from adapter.governed_host import WorkAuthorization

proof=json.loads((O/'R10_AUTHENTICATED_CAPTURE.json').read_bytes())
pin=proof['publication'];publication=json.loads(Path(pin['path']).read_bytes());assert sha(Path(pin['path']).read_bytes())==pin['sha256']
old=ControllerAuthorityStore(**publication['selected_store']);raw=proof['authorization'];oldop=json.loads(raw['operational_binding']);prior=proof['governance']
existing=O/'PROPOSED_R11_BINDING.json'
token=json.loads(existing.read_bytes())['invocation_identity']['authorization_id'].rsplit('-',1)[-1] if existing.exists() else uuid.uuid4().hex
inv={'authorization_id':'auth-e1-wp-001-r11-'+token,'session_id':'session-e1-run2-r11-'+token[:16],'turn_id':'turn-e1-run2-r11-'+token[16:],'revision':11}
audit=str(Path('/tmp/kge-forge-e1-evidence')/inv['authorization_id']/inv['session_id']/inv['turn_id']/'controller.jsonl')
assert not os.path.lexists(Path(audit).parents[2])
nodes,failed=predecessor_nodes(proof)
ancestors=[{k:failed[k] for k in ('authorization_id','audit','audit_sha256')}]+[{'authorization_id':n['authorization']['authorization_id'],'audit':n['terminal']['audit'],'audit_sha256':n['terminal']['audit_sha256']} for n in nodes]
bindings=dict(prior['run6']['proposal']['bindings']);bindings.update(prior['identities']);bindings.update({k:proof['context'][k] for k in ('FullContextDigest','ModelPayloadDigest','ModelProjectionBindingDigest')})
bindings.update(release_authority=publication['release_authority'],controller_runtime_identity=publication['controller_runtime_identity'])
p={'schema':'PROPOSED-AUTHENTICATED-ATTEMPT-CHAIN-1','status':'PROPOSED_NOT_AUTHORIZED_NOT_ISSUED',
 'DispatchAuthorizationId':prior['run6']['proposal']['DispatchAuthorizationId'],'dispatch':prior['run6']['proposal']['dispatch'],
 'predecessors':ancestors,'invocation_identity':inv,'audit':audit,'bindings':bindings,
 'proposed_initial_state':'INACTIVE','ownership':'NONE','automatic_retry':False,'inheritance':{k:False for k in ('audit_namespace','counters','effects','lifecycle','ownership')},
 'replacement_reason':'PRE_MODEL_ACTIVE_RECOVERY_ATTEMPT_OWNERSHIP_ATTRIBUTION_FAILURE_NO_EFFECTS'}
p['InvocationAttemptId']='InvocationAttempt-sha256:'+digest({'dispatch':p['DispatchAuthorizationId'],'predecessors':ancestors,'invocation_identity':inv,'audit':audit})
extras={}
def add(v,alias=None):
 b=v if isinstance(v,bytes) else canonical(v).encode();h=sha(b);extras['sha256:'+h]=b
 if alias:extras[alias]=b
 return {'authority_id':'sha256:'+h,'sha256':h}
pr=add(p);capture=add((O/'R10_AUTHENTICATED_CAPTURE.json').read_bytes())
source={'authority':'Architect','channel':'user','decision':'QUALIFY_ATTEMPT_SCOPED_OWNERSHIP_AND_PREPARE_SUCCESSOR','predecessor_release_authority':publication['release_authority'],'predecessor_publication':pin,'rules':list(RULES),'issuance_authorized':False}
sr=add(source)
runtime={'root':str(R),'files':{f.name:sha(f.read_bytes()) for f in (R/'adapter').glob('*.py')}};runtime['identity']='sha256:'+digest(runtime['files']);rr=add(runtime)
artifacts=[]
for name in ('attempt_ownership.py','attempt_transition.py','operator_projection.py'):
 before=Path('/tmp/forge-r10-transition-jxppjwou/adapter')/name;data=(R/'adapter'/name).read_bytes()
 artifacts.append({'path':str(before),'old_sha256':sha(before.read_bytes()) if before.exists() else None,'new_sha256':sha(data),'new_content':add(data)})
evidence=add({'status':'PASS_SYNTHETIC_CORRECTIONS_NON_ADOPTED','evidence':{name:sha((O/name).read_bytes()) for name in ('SYNTHETIC_FINAL.log','ACTUAL_IDENTITIES_POLICY_CANDIDATE.log','REGRESSIONS.log','HOST_NAMESPACE_REGRESSION.log')},'regression_interpretation':'31 sandbox PASS; one bubblewrap sandbox restriction requalified PASS on host','capture_sha256':capture['sha256']})
body={'schema':'OPERATIONAL-CONTINUATION-1','type':'NON_MATERIAL_IMPLEMENTATION_CONTINUATION','classification':'NON_MATERIAL_IMPLEMENTATION_CONTINUATION','sequence':1,
 'predecessor_OperationalContextId':prior['identities']['OperationalContextId'],'predecessor_chain_digest':prior['identities']['continuation_chain_digest'],
 'artifacts':artifacts,'authority':sr,'evidence':evidence,'authority_invariants':bindings,
 'reason':'Staged attempt-attributable ownership and independently fresh lifecycle/activity projections. No adoption or issuance.'}
c=seal(body,None);cr=add(c)
ab={'schema':'E1-RUN2-ATTEMPT-CHAIN-1','predecessor_release_authority':publication['release_authority'],'parent_dispatch':p['dispatch'],
 'proposal':pr,'rules':list(RULES),'authority_source':sr,'controller_runtime':rr,'correction_continuation':cr,
 'predecessor_publication':pin,'predecessor_capture':capture,
 'capture_semantics':'Qualified frozen verifier output; immutable witnesses and mutable inputs rechecked; captured ownership never authorizes current ownership.',
 'ModelPayloadDigest':bindings['ModelPayloadDigest']}
amendment=dict(ab,id=ident('E1-RUN2-ATTEMPT-CHAIN-AMENDMENT',ab));ar=add(amendment)
release,ids=identities(amendment,c,dict(prior['identities'],release_authority=publication['release_authority']))
spec={k:oldop['governance'][k] for k in ('release_basis','release_decision','released_profile','clearance')};spec.update(schema=7,amendment=ar,continuation=cr,identities=ids)
add({'mode':'PREPARED','amendment':ar,'continuation':cr,'specific_invocation_authorization':None,'qualification':None},inv['authorization_id']+':attempt-chain')
app=dict(ids,authorization_id=inv['authorization_id'])
base=Path(tempfile.mkdtemp(prefix='kge-forge-attempt-chain-authority-'));os.chmod(base,0o700)
def clone(name):
 root=base/name;root.mkdir(mode=0o700);cat=json.loads(encoded(old.catalog));cat['applicability']=app
 for row in cat['objects'].values():row['temporal_applicability']=app
 fd=_directory(root)
 try:
  for h in sorted({x['sha256'] for x in cat['objects'].values()}):_put(fd,h,_read(old.fd,h))
  for key,data in extras.items():
   h=sha(data)
   if not (root/h).exists():_put(fd,h,data)
   cat['objects'][key]={'sha256':h,'evidence':[],'authority_source':sr,'release_identities':ids,'temporal_applicability':app,'mutation':'IMMUTABLE'}
  cat['private_state'][inv['authorization_id']+':ownership']=dict(old.catalog['private_state'][raw['authorization_id']+':ownership'])
  cat['private_state'][inv['authorization_id']+':audit']={'path':audit,'mutation':'APPEND_ONLY','mechanism':'qualified lifecycle only; PREPARED'}
  _put(fd,'catalog.json',canonical(cat).encode());os.fsync(fd)
 finally:os.close(fd)
 return {'root':str(root),'catalog_sha256':digest(cat),'applicability':app}
pre=clone('construction');store=ControllerAuthorityStore(**pre)
with store.session():
 context=CommittedContext(raw['context_binding']['path'],raw['context_binding']['capture_commit'],spec)
 projection=derive(json.loads(raw['context_projection']),context);assert projection['ModelPayloadDigest']==bindings['ModelPayloadDigest']
 keys=('AuthoritativeContextId','FullContextDigest','ModelProjectionDigest','ModelPayloadDigest','ModelProjectionBindingDigest')
 op={'governance':spec,'released_launch':oldop['released_launch'],'invocation_identity':inv,'context_identities':{k:projection[k] for k in keys}}
 actual=dict(raw);actual.update(inv);actual['operational_binding']=canonical(op)
 values=dict(actual,context_binding=context)
 for k in ('read_roots','write_roots','deny_roots','exec_bins','read_deny_roots','write_deny_roots','write_directory_roots'):values[k]=tuple(values[k])
 values['exec_argv_allowlist']=tuple(tuple(x) for x in values['exec_argv_allowlist'])
 auth=WorkAuthorization(**values);dispatch=derive_dispatch(auth)
store.close()
did='E1-ARCHITECT-DISPATCH-sha256:'+digest(dispatch);dr=add(dispatch,did);dr['authority_id']=did
add(actual,inv['authorization_id']);add(canonical(op).encode(),ids['OperationalContextId']);final=clone('prepared')
pub={'status':'PREPARED_NOT_ADOPTED_NOT_ISSUED','selected_store':final,'dispatch':dr,'proposal':pr,'amendment':ar,'amendment_id':amendment['id'],
 'continuation':cr,'continuation_id':c['continuation_id'],'release_authority':release,'operational_identities':ids,'context_identities':op['context_identities'],
 'controller_runtime':rr,'controller_runtime_identity':runtime['identity'],'runtime_root':str(R),'audit':audit,'authorization_id':inv['authorization_id']}
for name,v in [('PREPARED_PUBLICATION.json',pub),('PROPOSED_R11_BINDING.json',p),('MATERIAL_AMENDMENT.json',amendment),('IMPLEMENTATION_CONTINUATION.json',c),('PROPOSED_OPERATIONAL_BINDING.json',op),('PROPOSED_AUTHORIZATION_TEMPLATE.json',actual)]:
 (O/name).write_text(canonical(v))
old.close();print(canonical(pub))
