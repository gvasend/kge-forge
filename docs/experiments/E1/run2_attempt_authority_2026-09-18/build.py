"""Materialize PREPARED authority only. No audit, allocation, or issuance."""
import json,os,sys,time
from pathlib import Path
from adapter.context_projection import canonical,digest,sha,derive
from adapter.controller_authority_store import ControllerAuthorityStore,encoded,_put,_directory,_read
from adapter.continuation_envelope import seal
from adapter.attempt_context import RULES,REASON,ident,identities,derive_dispatch
from adapter.context_binding import CommittedContext
from adapter.governed_host import WorkAuthorization

O=Path(sys.argv[1]);run=O/sys.argv[2];run.mkdir()
ROOT=Path(__file__).resolve().parent
P=O.parent/'run2_attempt_composition_2026-09-18';D=O.parent/'run2_dispatch_2026-09-18'
def load(p):return json.loads(Path(p).read_bytes())
def report(n,v):(run/n).write_text(canonical(v))
pin=load(D/'CURRENT_PIN.json');b=Path(pin['path']).read_bytes();assert sha(b)==pin['sha256'];pub=json.loads(b)
old=ControllerAuthorityStore(**pub['selected_store']);parent=pub['dispatch_record']
pbytes=(P/'PROPOSED_REPLACEMENT_BINDING.json').read_bytes();assert sha(pbytes)=='cb68a30719e88496504cd38004750b5b6848e4f31f1836387b87984ae92a8adc';p=json.loads(pbytes)
assert not os.path.lexists(p['audit']);A=p['invocation_identity']['authorization_id']
raw=json.loads(old.resolve(parent['invocation_identity']['authorization_id']));oldop=json.loads(raw['operational_binding'])
extras={}
def add(v,alias=None):
 b=v if isinstance(v,bytes) else canonical(v).encode();h=sha(b);extras['sha256:'+h]=b
 if alias:extras[alias]=b
 return {'authority_id':'sha256:'+h,'sha256':h}
proposal=add(pbytes)
source={'authority':'Architect','channel':'user','decision':'AUTHORIZE_RUN2_ATTEMPT_AUTHORITY',
 'predecessor_release_authority':parent['release_authority'],'parent_dispatch':p['dispatch'],
 'accepted_candidate':proposal,'rules':list(RULES),'reason_code':REASON,'issuance_authorized':False}
sr=add(source)
runtime={'root':str(ROOT),'files':{f.name:sha(f.read_bytes()) for f in (ROOT/'adapter').glob('*.py')}}
runtime['identity']='sha256:'+digest(runtime['files']);rr=add(runtime)
artifacts=[]
for name in ('activation_transaction.py','authorization_lifecycle.py','run_control.py','invocation_issuance.py'):
 data=(P/'candidate/adapter'/name).read_bytes();oldfile=Path('/home/gvasend/app/kge-forge/adapter')/name
 artifacts.append({'path':str(oldfile),'old_sha256':sha(oldfile.read_bytes()) if oldfile.exists() else None,
   'new_sha256':sha(data),'new_content':add(data)})
evidence=add((P/'QUALIFICATION.json').read_bytes())
body={'schema':'OPERATIONAL-CONTINUATION-1','type':'NON_MATERIAL_IMPLEMENTATION_CONTINUATION','classification':'NON_MATERIAL_IMPLEMENTATION_CONTINUATION',
 'sequence':1,'predecessor_OperationalContextId':oldop['governance']['identities']['OperationalContextId'],
 'predecessor_chain_digest':oldop['governance']['identities']['continuation_chain_digest'],
 'artifacts':artifacts,'authority':sr,'evidence':evidence,'authority_invariants':p['bindings'],
 'reason':'Integrate exact accepted issuance-ordering and audit-lock corrections as a private controller runtime layer; S3 original source bytes remain unchanged.'}
approval=add({'authority':'Architect','decision':'INTEGRATE_QUALIFIED_ISSUANCE_AND_AUDIT_COMPOSITION_CORRECTIONS',
 'authority_source':sr,'body_sha256':digest(body),'evidence':evidence})
continuation=seal(body,approval);cr=add(continuation)
ab={'schema':'E1-RUN2-ATTEMPT-AUTHORITY-1','predecessor_release_authority':parent['release_authority'],'parent_dispatch':p['dispatch'],
 'accepted_corrections':add((P/'CANDIDATE_IMPLEMENTATION.json').read_bytes()),
 'proposal':proposal,'rules':list(RULES),'reason_code':REASON,'authority_source':sr,
 'supervisor_instance':parent['current_supervisor'],'supervisor_succession':parent['succession_head'],
 'ModelPayloadDigest':parent['ModelPayloadDigest'],'controller_runtime':rr,'correction_continuation':cr,
 'predecessor_publication':pin,'predecessor_verifier':{'path':str(ROOT/'frozen_predecessor.py'),
  'sha256':sha((ROOT/'frozen_predecessor.py').read_bytes()),'python':'/usr/bin/python3.8',
  'python_sha256':sha(Path('/usr/bin/python3.8').read_bytes()),'repository':'/home/gvasend/app/kge-forge'},
 'accepted_proposed_operational_binding_sha256':p['replacement_operational_binding_sha256'],
 'binding_semantics':'Accepted proposal preserves predecessor authority content; this append-only amendment derives the new context and effective dispatch binding without rewriting that proposal.'}
amendment=dict(ab,id=ident('E1-RUN2-ATTEMPT-AUTHORITY-AMENDMENT',ab));ar=add(amendment)
release,ids=identities(amendment,continuation,dict(oldop['governance']['identities'],release_authority=parent['release_authority']))
spec={k:oldop['governance'][k] for k in ('release_basis','release_decision','released_profile','clearance')}
spec.update(schema=5,amendment=ar,continuation=cr,identities=ids)
sel={'mode':'PREPARED','amendment':ar,'continuation':cr,'specific_invocation_authorization':None,'qualification':None};add(sel,A+':attempt-context')
app=dict(ids,authorization_id=A)
base=Path('/tmp/kge-forge-controller-authority')/A/('attempt-authority-'+sys.argv[2]);base.mkdir(parents=True,mode=0o700)
attempts=base/'attempt-allocation.jsonl';fd=os.open(attempts,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600);os.fsync(fd);os.close(fd)
def clone(name):
 root=base/name;root.mkdir(mode=0o700);cat=json.loads(encoded(old.catalog));cat['applicability']=app
 for row in cat['objects'].values():row['temporal_applicability']=app
 fd=_directory(root)
 try:
  for h in sorted({v['sha256'] for v in cat['objects'].values()}):_put(fd,h,_read(old.fd,h))
  for key,data in extras.items():
   h=sha(data)
   if not (root/h).exists():_put(fd,h,data)
   cat['objects'][key]={'sha256':h,'evidence':[],'authority_source':sr,'release_identities':ids,'temporal_applicability':app,'mutation':'IMMUTABLE'}
  cat['private_state'][A+':ownership']=dict(old.catalog['private_state'][raw['authorization_id']+':ownership'])
  cat['private_state'][p['DispatchAuthorizationId']+':attempt-ledger']={'path':str(attempts),'mutation':'APPEND_ONLY','mechanism':'invocation_attempt.claim'}
  cat['private_state'][A+':audit']={'path':p['audit'],'mutation':'APPEND_ONLY','mechanism':'invocation_issuance / ActivationTransaction / RunControl'}
  _put(fd,'catalog.json',canonical(cat).encode());os.fsync(fd)
 finally:os.close(fd)
 return {'root':str(root),'catalog_sha256':digest(cat),'applicability':app}
pre=clone('preparation');st=ControllerAuthorityStore(**pre)
start=time.monotonic()
with st.session():
 context=CommittedContext(raw['context_binding']['path'],raw['context_binding']['capture_commit'],spec)
 derived=derive(json.loads(raw['context_projection']),context)
 require_payload=derived['ModelPayloadDigest']==p['bindings']['ModelPayloadDigest'];assert require_payload
 keys=('AuthoritativeContextId','FullContextDigest','ModelProjectionDigest','ModelPayloadDigest','ModelProjectionBindingDigest')
 op={'governance':spec,'released_launch':oldop['released_launch'],'invocation_identity':p['invocation_identity'],
     'context_identities':{k:derived[k] for k in keys}}
 actual=dict(raw);actual.update(p['invocation_identity']);actual['operational_binding']=canonical(op)
 authraw=dict(actual,context_binding=context)
 for k in ('read_roots','write_roots','deny_roots','exec_bins','read_deny_roots','write_deny_roots','write_directory_roots'):authraw[k]=tuple(authraw[k])
 authraw['exec_argv_allowlist']=tuple(tuple(x) for x in authraw['exec_argv_allowlist'])
 auth=WorkAuthorization(**authraw);child=derive_dispatch(auth)
st.close()
dr=add(child,'E1-ARCHITECT-DISPATCH-sha256:'+digest(child));dr['authority_id']='E1-ARCHITECT-DISPATCH-sha256:'+digest(child)
add(actual,A);add(canonical(op).encode(),ids['OperationalContextId'])
final=clone('prepared-context');old.close()
publication={'status':'PREPARED_NO_INVOCATION_ISSUANCE_AUTHORITY','selected_store':final,'dispatch':dr,
 'amendment':ar,'amendment_id':amendment['id'],'continuation':cr,'continuation_id':continuation['continuation_id'],
 'release_authority':release,'operational_identities':ids,'context_identities':op['context_identities'],
 'proposal':proposal,'controller_runtime':rr,'controller_runtime_identity':runtime['identity'],'construction_seconds':time.monotonic()-start,
 'r9_audit_unused':not os.path.lexists(p['audit'])}
report('PREPARED_PUBLICATION.json',publication);report('MATERIAL_AMENDMENT.json',amendment);report('IMPLEMENTATION_CONTINUATION.json',continuation)
report('PROPOSED_OPERATIONAL_BINDING.json',op);report('PROPOSED_AUTHORIZATION_TEMPLATE.json',actual)
print(canonical(publication))
