"""Authorized typed succession and activation; no model or governed action path."""
import json,os,sys,time
from pathlib import Path
from adapter.context_projection import canonical,digest,sha
from adapter.controller_authority_store import ControllerAuthorityStore,_directory,_put,_read,outside
from adapter.authority_bootstrap import reconstruct_authorization
from adapter.governance_continuation import verify_authorization
from adapter.authorization_lifecycle import dispatch_binding,reconstruct as lifecycle
from adapter.supervisor_succession import check_id,equivalent,append_authorized,reconstruct,legacy_tuple
from adapter.supervisor_observation import observe,process
from adapter.supervisor_amendment import authenticated_policy,readiness
from adapter.activation_transaction import _host,ActivationTransaction
O=Path(__file__).resolve().parent;B=O.parent;F=B/'s2_candidate_qualification_2026-09-17/final'
AUTH='auth-e1-wp-001-r7-94f511dfcdcc43ac837191f8732ced39'
EXPECTED_EVENT='SupervisorSuccession-sha256:e547147d27f88c38fe8dbfafdd6e45330621cf2e59ae156af60b885fa6f83db5'
EXPECTED_FILE='560402ad08262fff3fdea9039c0dce55f0071e0f7ead8fdec5c61fb2dae9e1b7'
EXPECTED_BODY='7d45c8dbd1d9f5d00d713251beb998ec64955e52562c980466a13420ba86e7fd'
BASE=Path('/tmp/kge-forge-controller-authority')/AUTH/'supervisor-succession-adoption-2026-09-17'
def load(p):return json.loads(Path(p).read_bytes())
def write(p,obj):
 data=canonical(obj).encode();fd=_directory(p.parent)
 try:_put(fd,p.name,data);os.fsync(fd)
 finally:os.close(fd)
 return {'path':str(p),'sha256':sha(data)}
def report(name,obj):
 with (O/name).open('xb') as f:f.write(canonical(obj).encode())
 print(canonical({'report':name,**obj}),flush=True)
def selection_pin(path):
 pin=load(path);p=Path(pin['path']);fd=_directory(p.parent)
 try:data=_read(fd,p.name)
 finally:os.close(fd)
 assert sha(data)==pin['sha256'];return json.loads(data)
def selected(stage):return selection_pin(O/(stage+'_PIN.json'))['selected_store']
def event():
 b=(F/'PROPOSED_SUPERVISOR_SUCCESSION.json').read_bytes();assert sha(b)==EXPECTED_FILE
 e=json.loads(b);assert check_id(e,'SupervisorSuccession')==EXPECTED_EVENT
 assert digest({k:v for k,v in e.items() if k not in ('id','architect_authorization')})==EXPECTED_BODY
 return e
def fresh(c):
 assert observe(c)==c,'S2 live identity changed'
 assert not Path('/proc/57950').exists(),'S1 PID now present'
 found=[]
 for p in Path('/proc').iterdir():
  if not p.name.isdigit():continue
  try:a=(p/'cmdline').read_bytes().split(b'\0')
  except FileNotFoundError:continue
  if b'adapter.supervisor_server' in a:found.append(int(p.name))
 assert found==[1098552],('competing supervisor',found)
 host=_host(legacy_tuple(c),True);assert process(1098552)==c['process']
 return {'observed_at_unix_ns':time.time_ns(),'instance':c['id'],'process':c['process'],'supervisor_pids':found,'S1_absent':True,'host':host}
def auth_in(store):
 a=reconstruct_authorization(store,AUTH);op=verify_authorization(a)
 original=load_bytes(store.resolve('sha256:'+op['governance']['material_release']['dispatch_amendment']['sha256']))['original_dispatch']
 ref={'authority_id':'E1-ARCHITECT-DISPATCH-sha256:'+original['sha256'],'sha256':original['sha256']}
 audit=store.state_path(AUTH+':audit');binding=dispatch_binding(a,audit,ref)
 print('Current authority ancestry and dispatch verified',flush=True)
 return a,audit,ref,binding
load_bytes=json.loads
def clone(old,root,extras,policy,source,ledger):
 outside(root,old.catalog['programmer_roots']);root.mkdir(mode=0o700)
 cat=json.loads(canonical(old.catalog));rows=cat['objects'];fd=_directory(root)
 try:
  for h in sorted({v['sha256'] for v in rows.values()}):_put(fd,h,_read(old.fd,h))
  allobjects={**extras,AUTH+':supervisor-succession':canonical(policy).encode()}
  for ident,data in allobjects.items():
   h=sha(data)
   if ident in rows:assert rows[ident]['sha256']==h,'attempt to replace authority'
   else:rows[ident]={'sha256':h,'evidence':[],'authority_source':source,'release_identities':{k:v for k,v in old.applicability.items() if k!='authorization_id'},'temporal_applicability':old.applicability,'mutation':'IMMUTABLE'}
   if not (root/h).exists():_put(fd,h,data)
  cat['private_state'][AUTH+':supervisor-succession-events']={'path':str(ledger),'mutation':'APPEND_ONLY','mechanism':'SupervisorSuccession.append_authorized'}
  _put(fd,'catalog.json',canonical(cat).encode());os.fsync(fd)
 finally:os.close(fd)
 return {'root':str(root),'catalog_sha256':digest(cat),'applicability':old.applicability}
mode=sys.argv[1];e=event()
if mode=='prepare':
 predecessor=selection_pin(B/'pd06_supervisor_amendment_publication_2026-09-17_final/PRIVATE_PUBLICATION_PIN.json')
 old=ControllerAuthorityStore(**predecessor['selected_store'])
 try:
  with old.session():
   a,audit,ref,binding=auth_in(old)
   assert AUTH+':supervisor-succession' not in old.catalog['objects'],'authority already selected'
   assert lifecycle(audit.read_bytes(),a,audit)['state']=='INACTIVE' and not Path(a.ownership_ledger).read_bytes()
   for name,h in load(F/'EVIDENCE_HASHES.json').items():assert sha((F/name).read_bytes())==h
   c=load('/tmp/kge-forge-s2-verification/CANDIDATE_S2.json');live=fresh(c)
   assert c['id']==e['successor_instance']
   assert c['runtime_binding']==e['runtime_binding']
   assert {k:c['runtime_binding'][k] for k in old.applicability}==old.applicability
   for name,h in load(F/'HOST_HASH_ATTESTATION.json')['original_receipt_sha256'].items():assert sha((Path('/tmp/kge-forge-s2-verification')/name).read_bytes())==h
   outside(BASE,old.catalog['programmer_roots']);BASE.mkdir(mode=0o700)
   source={'authority':'Architect','channel':'user','decision':'AUTHORIZE_EXACT_SUPERVISOR_SUCCESSION_AND_CONDITIONAL_E1_ACTIVATION','event_identity':EXPECTED_EVENT,'event_file_sha256':EXPECTED_FILE,'authorization_body_sha256':EXPECTED_BODY,'predecessor':e['predecessor_instance'],'successor':c['id'],'material_amendment':predecessor['amendment_identity'],'release_authority':predecessor['resulting_release_authority'],'dispatch_amendment':predecessor['dispatch_amendment'],'runtime_binding':e['runtime_binding'],'quote':'The Architect accepts S2_CANDIDATE_QUALIFIED and authorizes the exact proposed SupervisorSuccession event.','scope':'Exact supplied event and instance; activation only after recovery/readiness/dispatch pass; stop before any model request.'}
   srcpin=write(BASE/'ARCHITECT_AUTHORIZATION_SOURCE.json',source)
   grant=load(B/'supervisor_s2_host_attempt_2026-09-17/HOST_OPERATOR_AUTHORIZATION.json')
   approval={'schema':'SUPERVISOR-SUCCESSION-AUTHORIZATION-1','authority':'Architect','decision':'AUTHORIZE_SUPERVISOR_SUCCESSION','authorization_id':e['architect_authorization'],'event_body_sha256':EXPECTED_BODY,'event_identity':EXPECTED_EVENT,'event_file_sha256':EXPECTED_FILE,'predecessor_instance':e['predecessor_instance'],'successor_instance':c['id'],'reason':e['reason'],'runtime_binding':e['runtime_binding'],'host_authorization':grant['authorization_id'],'launch_spec_sha256':grant['launch_spec_sha256'],'launcher_sha256':grant['launcher_sha256'],'authority_source':'sha256:'+srcpin['sha256']}
   extras={}
   def add(data,identity=None):
    if not isinstance(data,bytes):data=canonical(data).encode()
    extras['sha256:'+sha(data)]=data
    if identity:extras[identity]=data
   add(source);add(approval,e['architect_authorization']);add(grant,grant['authorization_id'])
   add((B/'supervisor_s2_host_attempt_2026-09-17/HOST_AUTHORIZATION_SOURCE.json').read_bytes())
   att=load(B/'supervisor_succession_attempt_2026-09-17/ARCHITECT_ATTEMPT_AUTHORIZATION.json');add(att,att['authorization_id'])
   for p in F.iterdir():
    if p.is_file():add(p.read_bytes())
   for name in load(F/'HOST_HASH_ATTESTATION.json')['original_receipt_sha256']:add((Path('/tmp/kge-forge-s2-verification')/name).read_bytes())
   add(c,c['id']);h=load(B/'supervisor_succession_2026-09-17/HISTORICAL_S1.json');add(h,h['id'])
   plan=load(B/'supervisor_succession_attempt_2026-09-17/LAUNCH_SPEC.json')
   for p in [B/'supervisor_succession_attempt_2026-09-17/LAUNCH_SPEC.json',B/'supervisor_succession_2026-09-17/host_launch.py',B/'supervisor_s2_host_attempt_2026-09-17/HOST_LAUNCH_AUTHORIZATION.json']:add(p.read_bytes())
   ledger=BASE/'succession.jsonl';fd=os.open(ledger,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600);os.fsync(fd);os.close(fd)
   op=json.loads(a.operational_binding);profile=json.loads(old.resolve('sha256:'+op['governance']['released_profile']['sha256']))
   policy={'schema':'SUPERVISOR-SUCCESSION-POLICY-1','runtime_binding':e['runtime_binding'],'anchor_id':h['id'],'requirements':equivalent(c),'authorized_succession_ids':[e['architect_authorization']],'pinned_head':None,'ledger_id':AUTH+':supervisor-succession-events','release_authority':predecessor['resulting_release_authority'],'dispatch_amendment':predecessor['dispatch_amendment'],'released_supervisor':profile['supervisor_binding'][0]}
   src={'authority_id':'sha256:'+srcpin['sha256'],'sha256':srcpin['sha256']}
   prep=clone(old,BASE/'prepared-authority',extras,policy,src,ledger)
   post=clone(old,BASE/'selected-authority',extras,{**policy,'pinned_head':e['id']},src,ledger)
   for stage,sel in [('PREPARED',prep),('POST',post)]:
    pin=write(BASE/(stage+'_SELECTION.json'),{'selected_store':sel,'event':e['id'],'predecessor_publication':load(B/'pd06_supervisor_amendment_publication_2026-09-17_final/PRIVATE_PUBLICATION_PIN.json'),'architect_source':srcpin,'status':'PREPARED_NOT_APPLIED'})
    report(stage+'_PIN.json',pin)
   report('PREFLIGHT.json',{'result':'PASS','live':live,'dispatch_binding':binding,'authorization_source':srcpin,'state':'INACTIVE','ownership':'NONE','event_identity':e['id'],'event_sha256':EXPECTED_FILE})
 finally:old.close()
elif mode=='apply':
 store=ControllerAuthorityStore(**selected('PREPARED'))
 try:
  with store.session():
   a,audit,ref,binding=auth_in(store);policy=authenticated_policy(a,store)
   c=json.loads(store.resolve(e['successor_instance']));live=fresh(c)
   assert lifecycle(audit.read_bytes(),a,audit)['state']=='INACTIVE' and not Path(a.ownership_ledger).read_bytes()
   assert not store.state_path(policy['ledger_id']).read_bytes(),'succession already appended; recovery required'
   assert reconstruct(store,policy,b'')['instance']['id']==e['predecessor_instance']
   prospective=reconstruct(store,{**policy,'pinned_head':e['id']},canonical(e).encode()+b'\n')
   assert prospective['instance']==c
   print('Exact event prospectively validated; applying typed append',flush=True)
   assert append_authorized(store,policy,store.state_path(policy['ledger_id']),e)
   pin=write(BASE/'SUCCESSION_PUBLICATION.json',{'event':'authorized_supervisor_succession_applied','event_identity':e['id'],'event_file_sha256':EXPECTED_FILE,'selected_store':selected('POST'),'predecessor_selection':load(O/'PREPARED_PIN.json'),'architect_source':load(O/'PREFLIGHT.json')['authorization_source'],'ledger_sha256':sha(store.state_path(policy['ledger_id']).read_bytes()),'live_before_append':live,'E1_state':'INACTIVE','ownership':'NONE'})
   report('CURRENT_PRIVATE_PIN.json',pin)
   report('APPLICATION.json',{'result':'APPLIED','event_identity':e['id'],'event_file_sha256':EXPECTED_FILE,'private_pin':pin,'E1_state':'INACTIVE','ownership':'NONE'})
 finally:store.close()
else:
 publication=selection_pin(O/'CURRENT_PRIVATE_PIN.json');store=ControllerAuthorityStore(**publication['selected_store'])
 try:
  with store.session():
   a,audit,ref,binding=auth_in(store);policy=authenticated_policy(a,store)
   recovered=reconstruct(store,policy,store.state_path(policy['ledger_id']).read_bytes())
   assert recovered['head']==e['id'] and recovered['instance']['id']==e['successor_instance']
   live=fresh(recovered['instance'])
   ready=readiness(a,store,policy['released_supervisor'],True,_host)
   assert ready['SupervisorInstanceId']==e['successor_instance']
   if mode=='recover_supervisor':
    assert lifecycle(audit.read_bytes(),a,audit)['state']=='INACTIVE' and not Path(a.ownership_ledger).read_bytes()
    report('SUPERVISOR_RECOVERY.json',{'result':'PASS','current_instance':recovered['instance']['id'],'succession_head':recovered['head'],'supervisor_ready':ready,'dispatch_binding':binding,'E1_state':'INACTIVE','ownership':'NONE'})
   elif mode=='activate':
    assert load(O/'SUPERVISOR_RECOVERY.json')['result']=='PASS'
    try:tx=ActivationTransaction.activate(a,audit,ref['authority_id'])
    except Exception as ex:
     report('ACTIVATION_RESULT.json',{'result':'BLOCKED','exception':type(ex).__name__,'reason':str(ex),'lifecycle':lifecycle(audit.read_bytes(),a,audit),'ownership_ledger_sha256':sha(Path(a.ownership_ledger).read_bytes()),'E1_model_requests':0,'E1_implementation_effects':0});raise
    else:
     try:report('ACTIVATION_RESULT.json',{'result':'DURABLE_ACTIVE_REQUIRES_INDEPENDENT_RECOVERY','state':lifecycle(audit.read_bytes(),tx.auth,audit),'reservation':tx.reservation,'E1_model_requests':0,'E1_implementation_effects':0})
     finally:tx.close()
   elif mode=='recover_activation':
    tx=ActivationTransaction.recover(a,audit,ref['authority_id'])
    try:
     assert tx.recovery['lifecycle_state']=='ACTIVE' and tx.recovery['handoff_eligible'] and tx.reservation
     assert tx.verify_handoff()
     state=lifecycle(audit.read_bytes(),tx.auth,audit)
     report('FINAL_RECOVERY.json',{'result':'ACTIVATED_AND_READY_TO_DISPATCH','current_supervisor':recovered['instance']['id'],'succession_head':recovered['head'],'supervisor_readiness':'PASS','dispatch_inheritance':'PASS','CURRENT_RELEASE_BINDINGS_VALID':True,'CURRENT_SUPERVISOR_READY':True,'state':'ACTIVE','ownership':'OWNERSHIP_HELD','recovery':tx.recovery,'activation_event':state['activation_event'],'handoff_eligible':True,'operational_ancestry':json.loads(a.operational_binding)['governance']['identities'],'E1_model_requests':0,'E1_implementation_effects':0,'E1_WP_001_dispatched':False})
    finally:tx.close()
   else:raise ValueError('unknown mode')
 finally:store.close()
