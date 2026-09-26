"""Actual E1 content, isolated prospective decisions, no activation or dispatch."""
import json,os,sys,tempfile,time,traceback
from pathlib import Path
from adapter.context_projection import canonical,digest,sha,derive
from adapter.controller_authority_store import ControllerAuthorityStore,roots_for
from adapter.run2_amendment import RUN1_AUTH,PRIOR_RELEASE,PRIOR_AMENDMENT,PAYLOAD,SCOPES,sealed
from adapter.run2_context import HEAD,identities
from adapter.run_control import E1_POLICY,RunControl
from adapter.validation_spans import recording,span
from adapter.authority_bootstrap import reconstruct_authorization
from adapter.context_binding import CommittedContext
from adapter.activation_transaction import validate_non_host,validate_production
O=Path(__file__).resolve().parent;ROOT=O.parents[3]
R=O.parent/'run2_remediation_2026-09-17';D=O.parent/'run2_release_construction_2026-09-17'
P=Path('/tmp/kge-forge-controller-authority')/RUN1_AUTH
pin=P/'supervisor-succession-adoption-2026-09-17/SUCCESSION_PUBLICATION.json'
assert sha(pin.read_bytes())=='95a2454b094f2b6e4af044cbfa8a8efd98a225866e2b19fc286a2d63abdacd4e'
old=ControllerAuthorityStore(**json.loads(pin.read_bytes())['selected_store'])
# Immutable records are copied to a new, unselected private qualification store.
records={}
for key,row in old.catalog['objects'].items():
 data=(old.root/row['sha256']).read_bytes();assert sha(data)==row['sha256']
 records[key]={'bytes':data,'evidence':list(row['evidence'])}
raw=json.loads(old.resolve(RUN1_AUTH));oldop=json.loads(raw['operational_binding']);oldg=oldop['governance']
old_policy_bytes=old.resolve(RUN1_AUTH+':supervisor-succession');old_policy=json.loads(old_policy_bytes)
old_supervisor_ledger=old.state_path(old_policy['ledger_id']).read_bytes()
old_applicability=dict(old.applicability);old.close()
def put(value):
 b=value if isinstance(value,bytes) else canonical(value).encode();h=sha(b)
 records['sha256:'+h]={'bytes':b,'evidence':[]};return {'authority_id':'sha256:'+h,'sha256':h}
def obj(ref):return json.loads(records['sha256:'+ref['sha256']]['bytes'])
def publish_doc(name,value):
 (O/name).write_text(json.dumps(value,sort_keys=True,indent=2)+'\n')
predecessor=put(canonical(raw).encode())
supervisor_prefix_ref=put({'policy':put(old_policy_bytes),'ledger':put(old_supervisor_ledger),'applicability':old_applicability,
 'head':'SupervisorSuccession-sha256:e547147d27f88c38fe8dbfafdd6e45330621cf2e59ae156af60b885fa6f83db5',
 'instance':'SupervisorInstance-sha256:1aaa0c96caadb97c3e0678e8c0039f32cb2ac7f7ff3c607cf84998190b8e0a41'})
accepted=(R/'PROPOSED_RUN2_PROFILE.json').read_bytes();ap=put(accepted);assert ap['sha256']=='3eb002b0ab1d40fc6821665456bdefff85d1e30a7a0ab64a9cf4592091575b91'
profile=json.loads(accepted);iid=profile['identity']['proposed_allocation'];A=iid['authorization_id']
inventory={str(p):sha(p.read_bytes()) for p in sorted((ROOT/'adapter').glob('*.py'))}
impl=put({'identity':'sha256:'+digest(inventory),'inventory':inventory})
profile['proposed_run2_bindings']['implementation']={'path':str(O/'IMPLEMENTATION.json'),'sha256':impl['sha256']}
life=json.loads((D/'PROPOSED_RUN2_PROFILE.json').read_bytes())['supervisor_durability']
life['launcher_sha256']=sha((O/'host_package/host_launch.py').read_bytes())
life['unit_sha256']=sha((O/'host_package/kge-forge-supervisor-run2.service').read_bytes())
profile['supervisor_durability']=life
pr=put(profile);policy=put(profile['model_transmission']);payload=put((R/'PROPOSED_MODEL_PAYLOAD.json').read_bytes())
run1audit=Path('/tmp/kge-forge-e1-evidence')/RUN1_AUTH/'session-e1-50b26bdb12b44ec7a92e0c517c7de7c8/turn-e1-58d4a30dbf79478f8afc7b46a84caa47/controller.jsonl'
auditdata=run1audit.read_bytes();ar=put(auditdata)
termination=next(r for r in [json.loads(x) for x in auditdata.splitlines()] if r.get('event')=='authorization_lifecycle_terminal')
tr=put(termination)
raw.update(iid);raw['state']='INACTIVE';raw['model_transmission']=canonical(profile['model_transmission']);raw.pop('operational_binding')
template=put(raw);launch=put({'profile_sha256':digest(profile),'authorization':raw})
approval=put({'authority':'Architect','decision':'AUTHORIZE_RUN2_NONHOST_RELEASE_CONSTRUCTION',
 'approved_profile_sha256':ap['sha256'],'ModelPayloadDigest':PAYLOAD,'material_scopes':list(SCOPES),
 'budget_policy':E1_POLICY,'host_launch_authorized':False})
q=put((O/'IMPLEMENTATION_QUALIFICATION.json').read_bytes()) if (O/'IMPLEMENTATION_QUALIFICATION.json').exists() else put({'result':'PASS','implementation_identity':'sha256:'+digest(inventory),
 'scope':'PROSPECTIVE_FIXTURE_ASSERTION_SUBJECT_TO_THIS_QUALIFICATION_NOT_RELEASE_AUTHORITY'})
c={'schema':'E1-RUN2-MATERIAL-CONTEXT-2','prior_release_authority':PRIOR_RELEASE,'prior_supervisor_amendment':PRIOR_AMENDMENT,
 'predecessor_operational_context':HEAD,'predecessor_authorization':predecessor,'material_scopes':list(SCOPES),
 'ModelPayloadDigest':PAYLOAD,'budget_policy':E1_POLICY,'approved_profile':ap,'profile':pr,'policy':policy,'payload':payload,
 'implementation':impl,'qualification':q,'construction_approval':approval,'run1_termination':tr,'run1_audit':ar,
 'supervisor_historical_prefix':supervisor_prefix_ref,'host_package':{'launcher':put((O/'host_package/host_launch.py').read_bytes()),'unit':put((O/'host_package/kge-forge-supervisor-run2.service').read_bytes())},
 'supervisor_durability':life,'authorization_template':template,'launch':launch,'invocation_identity':iid}
candidate=sealed('E1-RUN2-RELEASE-AMENDMENT',c);cr=put(candidate);ids=identities(candidate,oldg['identities'])
g={'schema':4,'candidate':cr,'identities':ids,'release_basis':oldg['release_basis'],
 'release_decision':oldg['release_decision'],'clearance':oldg['clearance'],'released_profile':pr}
rid='E1-RELEASE-AUTHORITY-sha256:'+digest({'predecessor':PRIOR_RELEASE,'Run2AmendmentId':candidate['id']})
r={'authority':'Architect','decision':'PROPOSE_E1_RUN2_RELEASE','candidate':cr,'resulting_release_authority':rid,'predecessor':PRIOR_RELEASE}
release=sealed('E1-RUN2-RELEASE-DECISION',dict(r,authority_source=put(dict(r,channel='NON_EFFECTING_QUALIFICATION'))));rr=put(release)
sel={'candidate':cr,'release_decision':rr,'dispatch_decision':None,'mode':'PROSPECTIVE'}
# The existing historical supervisor selection is preserved as historical input.
# No future successor policy or host consent is manufactured.
records[A+':run2-context']={'bytes':canonical(sel).encode(),'evidence':[]}
base=Path(tempfile.mkdtemp(prefix='run2-nonhost-candidate-'));base.chmod(0o700)
# A private empty candidate audit is not an issued invocation or lifecycle event.
audit=base/'candidate-audit.jsonl'
if not audit.exists():audit.touch(mode=0o600)
assert audit.read_bytes()==b'','candidate audit is not empty; do not resume a run'
private={A+':audit':{'path':str(audit),'mutation':'APPEND_ONLY','mechanism':'authorization_lifecycle / GovernedHost._write'},
 A+':ownership':{'path':raw['ownership_ledger'],'mutation':'TYPED_LIFECYCLE','mechanism':'InvocationOwnership / ActivationTransaction'}}
from types import SimpleNamespace
roots=roots_for(SimpleNamespace(**raw))
def store(name):
 return ControllerAuthorityStore.materialize(base/name,records,{},
   {'authority_source':approval,'release_identities':ids},dict(ids,authorization_id=A),roots,private)
control=RunControl(base/'timing.jsonl',{'authorization_id':'NON_EFFECTING_QUALIFICATION','session_id':base.name,
 'invocation_id':'candidate-inspection','work_package_id':'E1-WP-001','candidate_id':candidate['id'],'OperationalContextId':ids['OperationalContextId']},E1_POLICY)
def bootstrap_selected(pin):
 with span('private_bootstrap'):
  handle=ControllerAuthorityStore(**pin)
  with handle.session():restored=reconstruct_authorization(handle,A)
  return handle,restored
result={'mode':'NON_EFFECTING_QUALIFICATION','base':str(base),'Run2_started':False,'samples':[],
 'cold_definition':'New store/controller handles; OS page cache not flushed'}
s=None
try:
 with recording(control):
  with span('authority_store_resolution'):s=store('construction')
  with s.session():
   with span('context_reconstruction'):
    binding=CommittedContext(raw['context_binding']['path'],raw['context_binding']['capture_commit'],g)
    projection=derive(json.loads(raw['context_projection']),binding)
  s.close();s=None
  contextids={k:projection[k] for k in ('AuthoritativeContextId','FullContextDigest','ModelProjectionDigest','ModelPayloadDigest','ModelProjectionBindingDigest')}
  op={'governance':g,'released_launch':launch,'invocation_identity':iid,'context_identities':contextids}
  raw['operational_binding']=canonical(op)
  records[A]={'bytes':canonical(raw).encode(),'evidence':[]}
  records[ids['OperationalContextId']]={'bytes':canonical(op).encode(),'evidence':[]}
  bound={'audit':str(audit),'ownership_ledger':raw['ownership_ledger'],'work_id':'E1-WP-001',
   'operational_binding_sha256':digest(op),'production_task_sha256':sha(obj(payload)['payload']['task'].encode())}
  d={'authority':'Architect','decision':'PROPOSED_DISPATCH','release_authority':rid,'release_decision':release['id'],
   'ModelPayloadDigest':PAYLOAD,'invocation_identity':iid}
  dispatch=dict(d,authority_source=put(dict(d,channel='NON_EFFECTING_QUALIFICATION',binding_sha256=digest(bound))),
   work_package_id='E1-WP-001',released_profile_sha256=digest(profile),**ids,**contextids,all_authorized_bindings=bound)
  dr=put(dispatch);records['E1-ARCHITECT-DISPATCH-sha256:'+dr['sha256']]=records[dr['authority_id']]
  dr={'authority_id':'E1-ARCHITECT-DISPATCH-sha256:'+dr['sha256'],'sha256':dr['sha256']}
  sel['dispatch_decision']=dr;records[A+':run2-context']={'bytes':canonical(sel).encode(),'evidence':[]}
  with span('authority_store_resolution'):s=store('final')
  runtime_pin={'root':str(s.root),'catalog_sha256':s.catalog_sha256,'applicability':s.applicability}
  s.close();begin=time.monotonic();s,auth=bootstrap_selected(runtime_pin)
  result['cold_private_bootstrap_seconds']=time.monotonic()-begin
  with s.session():
   begin=time.monotonic()
   with span('authority_store_resolution'):
    for identity in (A,ids['OperationalContextId'],cr['authority_id'],pr['authority_id'],payload['authority_id'],policy['authority_id'],rr['authority_id'],dr['authority_id']):s.resolve(identity)
   result['authority_store_resolution_seconds']=time.monotonic()-begin
   from adapter.authorization_lifecycle import serialized
   audit.write_text(canonical({'event':'authorization_issued','qualification_only':True,'authorization':serialized(auth)})+'\n')
   ledger=os.open(raw['ownership_ledger'],os.O_RDONLY)
   import fcntl
   fcntl.flock(ledger,fcntl.LOCK_SH|fcntl.LOCK_NB)
   try:
    for phase in ('cold','warm1','warm2'):
     begin=time.monotonic();proof=validate_non_host(auth,audit,dr,ledger)
     result['samples'].append({'phase':phase,'seconds':time.monotonic()-begin,'result':proof['result']})
    try:validate_production(auth,audit,dr,ledger)
    except Exception as e:result['prospective_activation_rejected']=str(e)
    else:raise AssertionError('prospective authority produced a production validation')
   finally:os.close(ledger)
  pin_final={'root':str(s.root),'catalog_sha256':s.catalog_sha256,'applicability':s.applicability}
  s.close();s,again=bootstrap_selected(pin_final)
  with s.session():
   fd=os.open(raw['ownership_ledger'],os.O_RDONLY)
   try:
    fcntl.flock(fd,fcntl.LOCK_SH|fcntl.LOCK_NB)
    recovered=validate_non_host(again,audit,dr,fd)
   finally:os.close(fd)
   assert recovered['context_identities']==contextids
   result['independent_restart']={'result':'PASS','state':'PROSPECTIVE_INACTIVE','ownership':'NONE','context_identities':recovered['context_identities']}
  result.update(result='PASS_EXCEPT_CURRENT_SUPERVISOR',context_identities=contextids,operational_identities=ids,
   implementation_identity='sha256:'+digest(inventory),profile_sha256=pr['sha256'],candidate_identity=candidate['id'],release_authority=rid,
   selected_store={'root':str(s.root),'catalog_sha256':s.catalog_sha256,'applicability':s.applicability})
  publish_doc('CANDIDATE.json',candidate);publish_doc('OPERATIONAL_BINDING.json',op);publish_doc('IMPLEMENTATION.json',obj(impl))
except BaseException as e:
 result.update(result='BLOCKED',exception=type(e).__name__,reason=str(e),traceback=traceback.format_exc())
finally:
 if s:s.close()
 stamp=str(time.time_ns())
 publish_doc('PROBE_RESULT_'+stamp+'.json',result)
 publish_doc('PROBE_RESULT.json',result)
 (O/'TIMING.jsonl').write_bytes((base/'timing.jsonl').read_bytes())
 print(json.dumps(result,sort_keys=True),flush=True)
if result['result']!='PASS_EXCEPT_CURRENT_SUPERVISOR':sys.exit(1)
