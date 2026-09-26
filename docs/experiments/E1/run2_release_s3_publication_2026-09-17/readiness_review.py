"""Read-only pre-dispatch review using production verifiers; no activation proof."""
import json,time,os,fcntl
from pathlib import Path
from adapter.context_projection import canonical,digest,sha,derive,ContextProjection
from adapter.controller_authority_store import ControllerAuthorityStore,read_authority_ref,outside,roots_for
from adapter.authority_bootstrap import reconstruct_authorization
from adapter.governance_continuation import verify_authorization
from adapter.supervisor_amendment import authenticated_policy,readiness
from adapter.activation_transaction import _host,invocation
from adapter.invocation_ownership import InvocationOwnership
from adapter.governed_host import GovernedHost
from adapter.run_control import RunControl,E1_POLICY,status
from adapter.validation_spans import recording,span
from adapter.run2_context import verify_dispatch
from adapter.model_transport import validate as validate_transport
from adapter.runnable_profile import validate as validate_execution
from adapter.directory_provisioning import open_directory
O=Path(__file__).resolve().parent;F=O.parent/'run2_nonhost_closure_2026-09-17'
def read(p):return json.loads(Path(p).read_bytes())
pin=read(O/'CURRENT_PIN.json');b=Path(pin['path']).read_bytes();assert sha(b)==pin['sha256'];pub=json.loads(b)
base=Path(pin['path']).parent;telemetry=base/'readiness-review.jsonl';assert not telemetry.exists()
control=RunControl(telemetry,{'authorization_id':'RELEASE_READINESS_REVIEW_NO_INVOCATION','session_id':'S3-post-succession','invocation_id':'NO_INVOCATION','work_package_id':'E1-WP-001'},E1_POLICY)
r={'model_requests':0,'activation':False,'ownership_acquired':False,'dispatch_authorized':False,'checks':{}}
try:
 with recording(control):
  with span('private_bootstrap'):
   store=ControllerAuthorityStore(**pub['selected_store'])
   with store.session():auth=reconstruct_authorization(store,store.applicability['authorization_id'])
  with store.session():
   with span('validation'):
    op=verify_authorization(auth);g=auth.context_binding.governance;policy=authenticated_policy(auth,store)
    supervisor=readiness(auth,store,policy['released_supervisor'],True,_host)
    assert supervisor['SupervisorInstanceId']=='SupervisorInstance-sha256:83f22718a56ab733257208c6e1dfe9767a95e0d10b82f8583f222f88ee9669a2'
    r['checks']['issued_release_context_and_current_supervisor']='PASS'
   with span('validation'):
    projection=derive(json.loads(auth.context_projection),auth.context_binding)
    assert all(projection[k]==op['context_identities'][k] for k in op['context_identities'])
    assert projection['ModelPayloadDigest']=='d675d581c80f43e691a31da73ccf17fd4bcc6b00d3a5331f26b9294e294e1538'
    profile=json.loads(read_authority_ref(op['governance']['released_profile']));assert digest(profile)=='fb842649d30e5876fb3f299e890e2c555a88be759c29b2c6577552d4885b0226'
    assert profile['model_transmission']==json.loads(auth.model_transmission)
    assert profile['model_transmission']['run_control']==E1_POLICY
    proxy=GovernedHost.__new__(GovernedHost);proxy.auth=auth;proxy.audit=telemetry;buffered=[];proxy._write=buffered.append
    ContextProjection(proxy).verify()
    r['checks']['profile_payload_projection_transmission_retention_budgets']='PASS'
   with span('validation'):
    transport=json.loads(auth.model_transport);validate_transport(transport,transport['endpoint'],transport['model'])
    runtime=json.loads(auth.execution_profile);validate_execution(runtime,runtime['argv'],runtime['cwd'],runtime['inputs'])
    assert not auth.shell and not auth.network and profile['ownership']['ledger']==auth.ownership_ledger and profile['ownership']['override_permitted'] is False
    required=set(auth.write_directory_roots)|{str(Path(p).parent) for p in auth.write_roots}
    provisioning=profile['provisioning_plan'];assert required<={x['path'] for x in provisioning['directories']}
    for row in provisioning['directories']:
     fd=open_directory(row['path']);os.close(fd)
    basis=json.loads(read_authority_ref(op['governance']['release_basis']));inputs=basis.get('current_inputs',basis.get('inputs'))
    refs=[{'path':p,'sha256':v['sha256']} for p,v in inputs.items() if v['sha256']==profile['provisioning_receipt_sha256']];assert len(refs)==1
    receipt=json.loads(read_authority_ref(refs[0]));assert receipt['result']=='PASS' and receipt['plan_sha256']==sha(json.dumps(provisioning,sort_keys=True).encode())
    assert receipt['created']==[x['path'] for x in provisioning['directories'] if x['controller_provisioning_required']]
    assert receipt['state']=='INACTIVE' and receipt['profile_activated'] is False
    store.require(auth);outside(store.root,roots_for(auth));outside(telemetry,roots_for(auth))
    fd=os.open(auth.ownership_ledger,os.O_RDONLY)
    try:
     fcntl.flock(fd,fcntl.LOCK_SH|fcntl.LOCK_NB)
     assert invocation(fd) is None and InvocationOwnership.__new__(InvocationOwnership)._history(fd) is None
     assert sha(Path(auth.ownership_ledger).read_bytes())=='651ced1160af0760f8b46073972a88f9d1ffc2c8ed0394e900bfa05fec586fe7'
    finally:os.close(fd)
    audit=Path('/tmp/kge-forge-e1-evidence/auth-e1-wp-001-r7-94f511dfcdcc43ac837191f8732ced39/session-e1-50b26bdb12b44ec7a92e0c517c7de7c8/turn-e1-58d4a30dbf79478f8afc7b46a84caa47/controller.jsonl')
    assert sha(audit.read_bytes())=='23d46d0fe282d322b731b309f7d48beebd676894ca0701e75c5468ed4fde427f'
    r['checks']['runtime_provisioning_store_isolation_Run1_terminal_no_ownership']='PASS'
   with span('validation'):
    proposed=json.loads(store.resolve(g.run2['selection']['dispatch_decision']['authority_id']))
    try:verify_dispatch(auth,proposed)
    except ValueError as ex:r['dispatch_gate']=str(ex)
    else:raise AssertionError('proposed dispatch accepted after release')
    assert r['dispatch_gate']=='Run-2 dispatch cannot inherit from historical dispatch'
    r['checks']['separate_dispatch_required']='PASS'
   control.emit('governance_observation',{'authorization':'INACTIVE_NOT_ISSUED','ownership':'NONE','supervisor':'READY','source_publication_sha256':pin['sha256']})
   projected=status(telemetry);assert projected['freshness']=='FRESH' and projected['ownership']=='NONE' and projected['supervisor_readiness']=='READY' and projected['model_requests']==0
   stale=status(telemetry,now=projected['projection_generated']+61);assert stale['freshness']=='UNKNOWN' and stale['supervisor_readiness']=='UNKNOWN'
   r['operator_status']=projected;r['checks']['operator_projection_fresh_and_stale']='PASS'
   r.update(result='RUN2_READY_FOR_ARCHITECT_DISPATCH_DECISION',operational_identities=g.identities,context_identities={k:projection[k] for k in op['context_identities']},
    supervisor=supervisor,release_authority=g.run2['release_authority'],invocation_identity=json.loads(auth.operational_binding)['invocation_identity'],
    activation_validation='NOT_ISSUED: separate dispatch decision and invocation issuance required; no activation-validation proof manufactured',
    scope='Pre-dispatch production-component readiness review; standard dispatch/activation gate remains closed')
  store.close()
except BaseException as ex:
 r.update(result='BLOCKED',error=type(ex).__name__+': '+str(ex));raise
finally:
 (O/'READINESS_REVIEW.json').write_text(json.dumps(r,sort_keys=True,indent=2)+'\n')
 (O/'READINESS_TIMING.jsonl').write_bytes(telemetry.read_bytes())
 print(json.dumps(r,sort_keys=True))
