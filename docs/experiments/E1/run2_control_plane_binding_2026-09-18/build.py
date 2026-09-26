"""Private qualification binding. No real attempt, lifecycle event or reservation."""
import json,os,sys,uuid,shutil,tempfile
from pathlib import Path
O=Path(__file__).resolve().parent
R=Path(tempfile.mkdtemp(prefix='forge-control-plane-bound-'));R.chmod(0o700)
shutil.copytree(O/'candidate/adapter',R/'adapter',ignore=shutil.ignore_patterns('__pycache__'))
sys.path.insert(0,str(R))
from adapter.context_projection import canonical,digest,sha,derive
from adapter.controller_authority_store import ControllerAuthorityStore,encoded,_put,_directory,_read
from adapter.control_plane_binding import SOURCE_DECISION,ident,derive_dispatch
from adapter.attempt_chain import predecessor_nodes
from adapter.continuation_envelope import seal
from adapter.context_binding import CommittedContext
from adapter.governed_host import WorkAuthorization
proof=json.loads((O/'R12_AUTHENTICATED_CAPTURE.json').read_bytes());pin=proof['publication']
pub=json.loads(Path(pin['path']).read_bytes());assert sha(Path(pin['path']).read_bytes())==pin['sha256']
old=ControllerAuthorityStore(**pub['selected_store']);raw=proof['authorization'];oldop=json.loads(raw['operational_binding']);prior=proof['governance']
base=Path(tempfile.mkdtemp(prefix='kge-control-plane-qualification-'));base.chmod(0o700)
extras={}
def add(v,alias=None):
 data=v if isinstance(v,bytes) else canonical(v).encode();h=sha(data);extras['sha256:'+h]=data
 if alias:extras[alias]=data
 return {'authority_id':'sha256:'+h,'sha256':h}
runtime={'root':str(R),'files':{f.name:sha(f.read_bytes()) for f in (R/'adapter').glob('*.py')}};runtime['identity']='sha256:'+digest(runtime['files']);rr=add(runtime)
previous=json.loads(old.resolve(pub['controller_runtime']['authority_id']))
slots=[]
for name in ('cold','warm1','warm2','warm3','hard-cancellation'):
 token=uuid.uuid4().hex;root=base/name;root.mkdir(mode=0o700)
 inv={'authorization_id':'qualification-control-plane-'+token,'revision':raw['revision'],'session_id':'qualification-session-'+token,'turn_id':'qualification-turn-'+token}
 slots.append({'invocation_identity':inv,'qualification_root':str(root)})
source={'authority':'Architect','channel':'user','decision':SOURCE_DECISION,'parent_publication':pin,
 'runtime_identity':runtime['identity'],'qualification_slots':slots,'real_invocation_authorized':False,'model_requests_authorized':False,'effects_authorized':False,
 'scope':'Exact staged corrections and required binding; genuine production pre-model qualification only; no r13; budgets and progress semantics unchanged'}
sr=add(source)
bindings=dict(prior['run7']['proposal']['bindings']);bindings.update(prior['identities']);bindings.update({k:proof['context'][k] for k in ('FullContextDigest','ModelPayloadDigest','ModelProjectionBindingDigest')});bindings.update(release_authority=pub['release_authority'],controller_runtime_identity=pub['controller_runtime_identity'])
changed=sorted(n for n in set(previous['files'])|set(runtime['files']) if previous['files'].get(n)!=runtime['files'].get(n))
artifacts=[{'path':str(Path('/home/gvasend/app/kge-forge/adapter')/n),'old_sha256':previous['files'].get(n),'new_sha256':runtime['files'][n],'old_blob':str(Path(previous['root'])/'adapter'/n) if n in previous['files'] else None,'new_blob':str(R/'adapter'/n)} for n in changed]
supervisor_verification=add((O/'SUPERVISOR_IMMUTABLE_VERIFICATION.json').read_bytes())
evidence=add({'supervisor_verification':supervisor_verification,'status':'QUALIFICATION_IN_PROGRESS_NOT_PRODUCTION_ADOPTION','candidate_files':runtime['files'],'baseline_corrections':{'path':str(O.parent/'run2_control_plane_2026-09-18/EVIDENCE_HASHES.json'),'sha256':sha((O.parent/'run2_control_plane_2026-09-18/EVIDENCE_HASHES.json').read_bytes())},'authority_invariants':bindings,'qualification_scope':'isolated controller lifecycle only'})
c=seal({'schema':'OPERATIONAL-CONTINUATION-1','type':'NON_MATERIAL_IMPLEMENTATION_CONTINUATION','sequence':1,'predecessor_OperationalContextId':prior['identities']['OperationalContextId'],'predecessor_chain_digest':prior['identities']['continuation_chain_digest'],'artifacts':artifacts,'authority':sr,'classification':'NON_MATERIAL_IMPLEMENTATION_CONTINUATION','evidence':evidence,'authority_invariants':bindings,'reason':'Bind scoped control-plane correction candidate for actual-context qualification; production adoption requires completed qualification'},sr);cr=add(c)
capture=add((O/'R12_AUTHENTICATED_CAPTURE.json').read_bytes());nodes,failed=predecessor_nodes(proof)
ancestors=[{k:failed[k] for k in ('authorization_id','audit','audit_sha256')}]+[{'authorization_id':n['authorization']['authorization_id'],'audit':n['terminal']['audit'],'audit_sha256':n['terminal']['audit_sha256']} for n in nodes]
outputs=[]
for slot in slots:
 root=Path(slot['qualification_root']);inv=slot['invocation_identity'];audit=str(root/'controller.jsonl');ledger=root/'ownership.jsonl'
 ledger.write_bytes(b'');ledger.chmod(0o600)
 b={'schema':'CONTROL-PLANE-QUALIFICATION-BINDING-1','mode':'QUALIFICATION_ONLY',**slot,'authority_source':sr,'runtime':rr,'continuation':cr,'parent_capture':capture,'supervisor_verification':supervisor_verification,'parent_publication':pin,'preserved_bindings':bindings,'release_authority':pub['release_authority'],'predecessors':ancestors,'audit':audit,'ownership_ledger':str(ledger)};br=add(b)
 ids={k:prior['identities'][k] for k in ('ReleaseBasisId','ReleaseDecisionId')};ids.update(OperationalContextId=ident('E1-OPERATIONAL-CONTEXT',{'continuation':c['continuation_id'],'qualification_binding':br}),continuation_chain_digest=digest({'predecessor':prior['identities']['continuation_chain_digest'],'continuation':c['continuation_id'],'qualification_binding':br}))
 spec={k:oldop['governance'][k] for k in ('release_basis','release_decision','released_profile','clearance')};spec.update(schema=8,binding=br,identities=ids)
 add({'mode':'QUALIFICATION_ONLY','binding':br},inv['authorization_id']+':control-plane');app=dict(ids,authorization_id=inv['authorization_id'])
 def clone(name):
  target=root/name;target.mkdir(mode=0o700);cat=json.loads(encoded(old.catalog));cat['applicability']=app
  for row in cat['objects'].values():row['temporal_applicability']=app
  fd=_directory(target)
  try:
   from concurrent.futures import ThreadPoolExecutor
   def copy_object(h):_put(fd,h,_read(old.fd,h))
   with ThreadPoolExecutor(max_workers=8) as pool:list(pool.map(copy_object,sorted({x['sha256'] for x in cat['objects'].values()})))
   for key,data in extras.items():
    h=sha(data)
    if not (target/h).exists():_put(fd,h,data)
    cat['objects'][key]={'sha256':h,'evidence':[],'authority_source':sr,'release_identities':ids,'temporal_applicability':app,'mutation':'IMMUTABLE'}
   cat['private_state']={inv['authorization_id']+':ownership':{'path':str(ledger),'mutation':'TYPED_LIFECYCLE','mechanism':'ActivationTransaction / InvocationOwnership; isolated qualification only'},inv['authorization_id']+':audit':{'path':audit,'mutation':'APPEND_ONLY','mechanism':'typed qualified lifecycle; model/effects forbidden'}}
   _put(fd,'catalog.json',canonical(cat).encode());os.fsync(fd)
  finally:os.close(fd)
  return {'root':str(target),'catalog_sha256':digest(cat),'applicability':app}
 pre=clone('construction');store=ControllerAuthorityStore(**pre)
 with store.session():
  context=CommittedContext(raw['context_binding']['path'],raw['context_binding']['capture_commit'],spec)
  projection=derive(json.loads(raw['context_projection']),context);assert projection['ModelPayloadDigest']==bindings['ModelPayloadDigest']
  keys=('AuthoritativeContextId','FullContextDigest','ModelProjectionDigest','ModelPayloadDigest','ModelProjectionBindingDigest')
  op={'governance':spec,'released_launch':oldop['released_launch'],'invocation_identity':inv,'context_identities':{k:projection[k] for k in keys}}
  actual=dict(raw);actual.update(inv);actual['ownership_ledger']=str(ledger);actual['operational_binding']=canonical(op)
  values=dict(actual,context_binding=context)
  for k in ('read_roots','write_roots','deny_roots','exec_bins','read_deny_roots','write_deny_roots','write_directory_roots'):values[k]=tuple(values[k])
  values['exec_argv_allowlist']=tuple(tuple(x) for x in values['exec_argv_allowlist'])
  auth=WorkAuthorization(**values);dispatch=derive_dispatch(auth)
 store.close()
 did='E1-ARCHITECT-DISPATCH-sha256:'+digest(dispatch);dr=add(dispatch,did);dr['authority_id']=did
 add(actual,inv['authorization_id']);add(canonical(op).encode(),ids['OperationalContextId']);final=clone('selected')
 output={'name':root.name,'qualification_only':True,'selected_store':final,'runtime_root':str(R),'controller_runtime':rr,'controller_runtime_identity':runtime['identity'],'continuation':cr,'continuation_id':c['continuation_id'],'binding':br,'dispatch':dr,'operational_identities':ids,'context_identities':op['context_identities'],'release_authority':pub['release_authority'],'authorization_id':inv['authorization_id'],'audit':audit,'ownership_ledger':str(ledger)}
 (root/'PUBLICATION.json').write_text(canonical(output));(root/'PUBLICATION.json').chmod(0o600);outputs.append(output)
old.close()
for name,value in [('QUALIFICATION_BINDINGS.json',outputs),('PROPOSED_IMPLEMENTATION_CONTINUATION.json',c),('IMPLEMENTATION_APPLICABILITY.json',{'runtime':runtime,'changed_files':changed,'production_adopted':False,'qualification_only':True,'artifacts':artifacts})]:
 (O/name).write_text(canonical(value))
print(canonical({'runtime':runtime['identity'],'continuation':c['continuation_id'],'qualification_cases':len(outputs),'real_invocations_created':0}))
