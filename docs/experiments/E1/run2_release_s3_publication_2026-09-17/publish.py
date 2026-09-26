"""Exact Architect-authorized release and typed S3 succession; never activate/dispatch."""
import json,os,sys,time,base64,socket,struct
from pathlib import Path
from adapter.context_projection import canonical,digest,sha,derive
from adapter.controller_authority_store import ControllerAuthorityStore,_directory,_put,_read,outside,encoded
from adapter.authority_bootstrap import reconstruct_authorization
from adapter.governance_continuation import verify_authorization
from adapter.run2_amendment import sealed,PRIOR_RELEASE
from adapter.run2_context import supervisor_prefix,verify_dispatch
from adapter.supervisor_succession import append_authorized,reconstruct,equivalent,check_id,legacy_tuple
from adapter.supervisor_amendment import authenticated_policy,readiness
from adapter.supervisor_observation import observe
from adapter.activation_transaction import _host
O=Path(__file__).resolve().parent;E=O.parent;F=E/'run2_nonhost_closure_2026-09-17';Q=E/'run2_live_supervisor_qualification_2026-09-17/final';J=E/'run2_host_consent_2026-09-17'
A='auth-e1-wp-001-r8-3251a47bce19fcec0dab883d9e5e6c56'
BASE=Path('/tmp/kge-forge-controller-authority')/A/'release-s3-publication-2026-09-17-complete'
def load(p):return json.loads(Path(p).read_bytes())
def write(p,v):
 b=canonical(v).encode();fd=_directory(p.parent)
 try:_put(fd,p.name,b);os.fsync(fd)
 finally:os.close(fd)
 return {'path':str(p),'sha256':sha(b)}
def report(n,v):
 with (O/n).open('xb') as f:f.write(canonical(v).encode())
 print(n+': '+canonical(v),flush=True)
def pin(stage):
 r=load(O/(stage+'_PIN.json'));b=Path(r['path']).read_bytes();assert sha(b)==r['sha256'];return json.loads(b)
def fresh(c):
 assert observe(c)==c
 assert not Path('/proc/57950').exists() and not Path('/proc/1098552').exists()
 found=[]
 for p in Path('/proc').iterdir():
  if not p.name.isdigit():continue
  try:cmd=(p/'cmdline').read_bytes().split(b'\0')
  except FileNotFoundError:continue
  if b'adapter.supervisor_server' in cmd:found.append(int(p.name))
 assert found==[1465900]
 host=_host(legacy_tuple(c),True)
 with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as s:
  s.settimeout(3);s.connect('/tmp/a21m.sock');assert struct.unpack('3i',s.getsockopt(socket.SOL_SOCKET,socket.SO_PEERCRED,12))==(1465900,1000,1000)
  b=b'{"op":"status"}';s.sendall(struct.pack('!I',len(b))+b)
  def rec(n):
   b=b''
   while len(b)<n:
    x=s.recv(n-len(b));assert x;b+=x
   return b
  n=struct.unpack('!I',rec(4))[0];assert n<=65536;assert json.loads(rec(n))=={'status':'READY'}
 assert observe(c)==c
 return {'instance':c['id'],'process':c['process'],'READY':True,'exclusive':True,'host':host,'observed_at_ns':time.time_ns()}
ebytes=(Q/'PROPOSED_SUPERVISOR_SUCCESSION.json').read_bytes();assert sha(ebytes)=='2a240244e9c2f04943e677b9ecf588b175f2189e899e709864f83d63402800d9'
e=json.loads(ebytes);assert check_id(e,'SupervisorSuccession')=='SupervisorSuccession-sha256:b86bbb15d9d9d468b2de87926ad6b1cb4063218fd71eb5426089f689c0aecce8'
bodyhash=digest({k:v for k,v in e.items() if k not in ('id','architect_authorization')});assert bodyhash=='5363653f7301b1e4c82d2aaaa89a778ae47e532325634a74f9cfa4a108f182bc'
raw=Path('/tmp/kge-forge-s3-host-verification/HOST_EXPORT.json').read_bytes();assert sha(raw)=='1cbf36e93771828484dcb570a66b2f061608e813d65bd4efe0456db619e15361'
files={Path(x['path']).name:base64.b64decode(x['base64']) for x in json.loads(raw)['body']['files'] if not x.get('absent')};c=json.loads(files['CANDIDATE_S3.json']);assert c['id']==e['successor_instance']
mode=sys.argv[1];r=load(F/'PROBE_RESULT.json')
if mode=='prepare':
 for n,h in load(F/'PACKAGE_MANIFEST.json').items():assert sha((F/n).read_bytes())==h,n
 inv=load(F/'FINAL_IMPLEMENTATION.json');assert inv['identity']=='sha256:befdf3f2c7c293278c58b96676cf8d865113442f1ab34e4e2d3a1f60e7cb93a3'
 assert all(sha(Path(k).read_bytes())==v for k,v in inv['inventory'].items());live=fresh(c)
 old=ControllerAuthorityStore(**r['selected_store'])
 with old.session():
  auth=reconstruct_authorization(old,A);verify_authorization(auth);prefix=supervisor_prefix(old)
  assert c['runtime_binding']==e['runtime_binding']
 outside(BASE,old.catalog['programmer_roots']);BASE.parent.mkdir(mode=0o700,exist_ok=True);BASE.mkdir(mode=0o700)
 extras={}
 def add(v,alias=None):
  b=v if isinstance(v,bytes) else canonical(v).encode();h=sha(b);extras['sha256:'+h]=b
  if alias:extras[alias]=b
  return {'authority_id':'sha256:'+h,'sha256':h}
 source={'authority':'Architect','decision':'AUTHORIZE_E1_RUN2_RELEASE','candidate':load(F/'OPERATIONAL_BINDING.json')['governance']['candidate'],
  'resulting_release_authority':r['release_authority'],'predecessor':PRIOR_RELEASE,'channel':'user'}
 sr=add(source);decision=sealed('E1-RUN2-RELEASE-DECISION',{k:v for k,v in source.items() if k!='channel'}|{'authority_source':sr}) if sys.version_info>=(3,9) else sealed('E1-RUN2-RELEASE-DECISION',dict({k:v for k,v in source.items() if k!='channel'},authority_source=sr))
 dr=add(decision,decision['id'])
 sel=json.loads(old.resolve(A+':run2-context'));sel.update(mode='ISSUED',release_decision=dr)
 # Preserve the explicitly PROPOSED dispatch as non-authorizing documentary content.
 # No DISPATCH_AUTHORIZED record/source is fabricated or selected.
 add(sel,A+':run2-context')
 release_receipt={'decision':'RUN2_RELEASED','release_decision':dr,'release_decision_id':decision['id'],'amendment_identity':r['candidate_identity'],'release_authority':r['release_authority'],
  'scope':'Exact user release decision; separate dispatch withheld; S3 succession conditional on fresh checks','S3_event':e['id'],'activation_authorized':False,'dispatch_authorized':False}
 add(release_receipt)
 succession_source=add({'authority':'Architect','channel':'user','decision':'AUTHORIZE_EXACT_SUPERVISOR_SUCCESSION_AFTER_RUN2_RELEASE',
  'event_identity':e['id'],'event_file_sha256':sha(ebytes),'authorization_body_sha256':bodyhash,'successor_instance':c['id'],'release_authority':r['release_authority'],'activate_or_dispatch':False})
 j=load(J/'JERRY_HOST_AUTHORIZATION.json');launch=json.loads(files['HOST_LAUNCH_AUTHORIZATION.json'])
 hs=add({'operator':'Jerry','channel':'user','authorization_id':j['id'],'source_text':j['source_text'],'source_text_sha256':j['source_text_sha256']})
 grant={'authority':'HOST_OPERATOR','operator':'Jerry','decision':'AUTHORIZE_HOST_SUPERVISOR_LAUNCH','authorization_id':j['id'],'authority_source':hs['authority_id'],
  'runtime_binding':c['runtime_binding'],'predecessor_id':e['predecessor_instance'],'launch_spec_sha256':launch['launch_spec_sha256'],'launcher_sha256':launch['launcher_sha256'],'original_host_consent_receipt':add((J/'JERRY_HOST_AUTHORIZATION.json').read_bytes())}
 gr=add(grant)
 approval={'schema':'SUPERVISOR-SUCCESSION-AUTHORIZATION-1','authority':'Architect','decision':'AUTHORIZE_SUPERVISOR_SUCCESSION','authorization_id':e['architect_authorization'],
  'event_body_sha256':bodyhash,'event_identity':e['id'],'event_file_sha256':sha(ebytes),'predecessor_instance':e['predecessor_instance'],'successor_instance':c['id'],
  'reason':e['reason'],'runtime_binding':e['runtime_binding'],'host_authorization':gr['authority_id'],'launch_spec_sha256':launch['launch_spec_sha256'],'launcher_sha256':launch['launcher_sha256'],'authority_source':succession_source['authority_id']}
 add(approval,e['architect_authorization'])
 for p in Q.iterdir():
  if p.is_file():add(p.read_bytes())
 for b in files.values():add(b)
 add(c,c['id'])
 ledger=BASE/'succession.jsonl';fd=os.open(ledger,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600);os.fsync(fd);os.close(fd)
 closure=add((Q/'TERMINAL_CLOSURE_QUALIFICATION.json').read_bytes())
 profile=load(F/'FINAL_PROFILE.json')
 policy={'schema':'SUPERVISOR-SUCCESSION-POLICY-2','runtime_binding':c['runtime_binding'],'historical_prefix':prefix['reference'],'anchor_id':e['predecessor_instance'],
  'requirements':equivalent(c),'authorized_succession_ids':[e['architect_authorization']],'pinned_head':prefix['head'],'ledger_id':A+':supervisor-succession-events',
  'release_authority':r['release_authority'],'dispatch_amendment':sel['dispatch_decision']['authority_id'],'released_supervisor':profile['supervisor_binding'][0],
  'terminal_closure_qualification':closure['authority_id']}
 def clone(name,pol):
  root=BASE/name;root.mkdir(mode=0o700);cat=json.loads(encoded(old.catalog));fd=_directory(root)
  try:
   for h in sorted({v['sha256'] for v in cat['objects'].values()}):_put(fd,h,_read(old.fd,h))
   for ident,b in dict(extras,**{A+':supervisor-succession':canonical(pol).encode()}).items():
    h=sha(b)
    if not (root/h).exists():_put(fd,h,b)
    cat['objects'][ident]={'sha256':h,'evidence':[],'authority_source':sr,'release_identities':r['operational_identities'],'temporal_applicability':old.applicability,'mutation':'IMMUTABLE'}
   # Do not select the synthetic qualification audit as an actual invocation audit.
   cat['private_state'].pop(A+':audit',None)
   cat['private_state'][policy['ledger_id']]={'path':str(ledger),'mutation':'APPEND_ONLY','mechanism':'SupervisorSuccession.append_authorized'}
   _put(fd,'catalog.json',canonical(cat).encode());os.fsync(fd)
  finally:os.close(fd)
  return {'root':str(root),'catalog_sha256':digest(cat),'applicability':old.applicability}
 pre=clone('released-authority',policy);post=clone('successor-authority',dict(policy,pinned_head=e['id']))
 old.close()
 # Verify issued release before publishing its selection.
 st=ControllerAuthorityStore(**pre)
 with st.session():
  aa=reconstruct_authorization(st,A);verify_authorization(aa);pp=authenticated_policy(aa,st)
  assert reconstruct(st,pp,b'')['instance']['id']==e['predecessor_instance']
 st.close()
 publication=write(BASE/'RELEASE_PUBLICATION.json',dict(release_receipt,selected_store=pre,next_prepared_selection=post,
  OperationalContextId=r['operational_identities']['OperationalContextId'],state='RELEASED_NOT_ACTIVATION_READY_INELIGIBLE_UNDISPATCHED'))
 report('RELEASE_PIN.json',publication);report('RELEASE_PUBLICATION.json',dict(release_receipt,private_pin=publication,live_preparation=live))
 report('POST_PIN.json',write(BASE/'POST_SELECTION.json',{'selected_store':post,'status':'PREPARED_NOT_APPLIED'}))
else:
 pub=pin('RELEASE' if mode in ('recover_release','apply') else 'CURRENT');st=ControllerAuthorityStore(**pub['selected_store'])
 begin=time.monotonic()
 with st.session():
  auth=reconstruct_authorization(st,A);op=verify_authorization(auth);policy=authenticated_policy(auth,st)
  projection=derive(json.loads(auth.context_projection),auth.context_binding)
  assert all(projection[k]==r['context_identities'][k] for k in r['context_identities'])
  assert auth.context_binding.governance.run2['release_authority']==r['release_authority']
  ledger=st.state_path(policy['ledger_id']);data=ledger.read_bytes()
  if mode=='recover_release':
   recovered=reconstruct(st,policy,data);assert recovered['instance']['id']==e['predecessor_instance']
   report('RELEASE_RECOVERY.json',{'result':'PASS','release_authority':r['release_authority'],'release_decision':auth.context_binding.governance.run2['release_decision'],'context_identities':r['context_identities'],'operational_identities':r['operational_identities'],'supervisor_current':False,'activation_ready':False,'dispatch_authorized':False,'seconds':time.monotonic()-begin})
  elif mode=='apply':
   assert load(O/'RELEASE_RECOVERY.json')['result']=='PASS';assert data==b'','existing append: recover instead of retry'
   live=fresh(c)
   assert reconstruct(st,dict(policy,pinned_head=e['id']),canonical(e).encode()+b'\n')['instance']==c
   assert append_authorized(st,policy,ledger,e)
   publication=write(BASE/'SUCCESSION_PUBLICATION.json',{'event_identity':e['id'],'event_file_sha256':sha(ebytes),'release_publication':load(O/'RELEASE_PIN.json'),
    'selected_store':pin('POST')['selected_store'],'ledger_sha256':sha(ledger.read_bytes()),'live_before_append':live,'activation':False,'dispatch':False})
   report('CURRENT_PIN.json',publication);report('SUCCESSION_APPLICATION.json',{'result':'APPLIED','event':e['id'],'event_file_sha256':sha(ebytes),'publication':publication})
  elif mode=='recover':
   recovered=reconstruct(st,policy,data);assert recovered['instance']==c and recovered['head']==e['id']
   ready=readiness(auth,st,policy['released_supervisor'],True,_host);live=fresh(c)
   assert ready['SupervisorInstanceId']==c['id']
   report('INDEPENDENT_RECOVERY.json',{'result':'PASS','release_authority':r['release_authority'],'current_supervisor':c['id'],'succession_head':e['id'],
    'readiness':ready,'live':live,'operational_identities':r['operational_identities'],'context_identities':{k:projection[k] for k in r['context_identities']},'seconds':time.monotonic()-begin,
    'context_semantics':'Content context unchanged; authenticated succession head and private catalog binding changed separately under existing schema4.',
    'activation':False,'ownership':'NONE','dispatch_authorized':False})
  else:raise ValueError(mode)
 st.close()
