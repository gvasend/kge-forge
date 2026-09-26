"""One exact authorized invocation; frozen typed operations, no automatic retry."""
import json,os,sys,time,subprocess,traceback
from pathlib import Path
from dataclasses import replace
sys.path.insert(0,'/tmp/forge-attempt-chain-xjcb_jkz')
from adapter.context_projection import canonical,sha
from adapter.controller_authority_store import ControllerAuthorityStore,current,_directory,_put
from adapter.authority_bootstrap import reconstruct_authorization
from adapter.invocation_issuance import issue_inactive,start_control
from adapter.activation_transaction import ActivationTransaction,_host,invocation
from adapter.invocation_ownership import InvocationOwnership
from adapter.supervisor_amendment import readiness
from adapter.authorization_lifecycle import reconstruct
from adapter.governed_host import GovernedHost
from adapter.validation_spans import recording
from adapter.run_control import events,BudgetExceeded
from adapter.controlled_dispatch import dispatch
O=Path(__file__).parent;pin=json.loads((O/'CURRENT_PIN.json').read_bytes());b=Path(pin['path']).read_bytes();assert sha(b)==pin['sha256'];p=json.loads(b)
B=Path(p['private_run_root']);A=p['r12_authorization_id'];audit=Path(p['audit']);begin=time.monotonic();control=None;tx=None;stage='PRE_ISSUANCE'
independent=json.loads((O/'INDEPENDENT_AUTHORITY_RECOVERY.json').read_bytes());assert independent['result']=='PASS' and independent['publication_pin']==pin
fd=os.open(B/'ONE_ATTEMPT_STARTED',os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
os.write(fd,canonical({'wall_time':time.time(),'monotonic':begin,'pid':os.getpid(),'automatic_retry':False}).encode());os.fsync(fd);os.close(fd)
def report(name,value):
 value=dict(value,wall_time=time.time(),controller_elapsed=time.monotonic()-begin)
 data=canonical(value).encode();fd=_directory(B)
 try:_put(fd,name,data);os.fsync(fd)
 finally:os.close(fd)
 (O/name).write_bytes(data);print(canonical({'event':name,**value}),flush=True)
def recovery(mode,label):
 # No parent timing writer while the child owns the audit transaction.
 result=subprocess.run([sys.executable,'-B',str(O/'recover.py'),mode],capture_output=True,text=True,timeout=120)
 if result.returncode:
  report(label+'_FAILURE.json',{'result':'FAIL','returncode':result.returncode,'stderr_sha256':sha(result.stderr.encode())})
  raise RuntimeError('independent recovery failed')
 r=json.loads(result.stdout);report(label+'.json',r);return r
s=ControllerAuthorityStore(**p['selected_store'])
try:
 with s.session():
  a=reconstruct_authorization(s,A);g=a.context_binding.governance
  assert g.run7['release_authority']==p['release_authority'] and g.identities==p['operational_identities']
  assert p['proposal']['sha256']=='39319b6dab6320b3b373a8049f1ae5dee7f7318a71e7491a3643faf3582cb54d'
  assert not os.path.lexists(audit)
  own=InvocationOwnership(a.ownership_ledger);fd=own._locked()
  try:assert invocation(fd) is None and own._history(fd) is None
  finally:os.close(fd)
  ready=readiness(a,s,{},True,_host)
  assert ready['SupervisorInstanceId']=='SupervisorInstance-sha256:83f22718a56ab733257208c6e1dfe9767a95e0d10b82f8583f222f88ee9669a2'
  assert ready['SupervisorSuccessionHead']=='SupervisorSuccession-sha256:b86bbb15d9d9d468b2de87926ad6b1cb4063218fd71eb5426089f689c0aecce8'
  report('IMMEDIATE_PRE_ISSUANCE.json',{'result':'PASS','supervisor':ready['SupervisorInstanceId'],'r8_r9_r10_r11_immutable':True,'audit_unused':True,'ownership':'NONE'})
  issue_inactive(a,audit,p['dispatch']);stage='INACTIVE'
  rows=events(audit);assert rows[0]['event']=='authorization_issued' and rows[0]['authorization']['state']=='INACTIVE'
  control=start_control(a,audit,json.loads(a.model_transmission)['run_control'])
  report('INACTIVE_ISSUANCE.json',{'state':'INACTIVE','first_event':'authorization_issued','audit_sha256':sha(audit.read_bytes()),'ownership':'NONE'})
  r=recovery('INACTIVE','INDEPENDENT_INACTIVE_RECOVERY')
  assert r['lifecycle_state']=='INACTIVE' and r['ownership'] is None and not r['handoff_eligible'] and not r['reconciliation_required']
  control.emit('governance_observation',{'authorization':'INACTIVE','ownership':'NONE','supervisor':'READY'})
  stage='ACTIVATION'
  with recording(control),control.span('validation'):tx=ActivationTransaction.activate(a,audit,p['dispatch']['authority_id'])
  report('ACTIVE_COMMIT.json',{'state':tx.auth.state,'reservation':tx.reservation,'audit_sha256':sha(audit.read_bytes())})
  tx.close();tx=None
 # Parent authority session is closed before dispatcher takes ownership.
 assert current() is None;stage='ACTIVE_RECOVERY'
 r=recovery('ACTIVE','INDEPENDENT_ACTIVE_RECOVERY')
 assert r['lifecycle_state']=='ACTIVE' and r['ownership'] is not None and r['handoff_eligible'] and not r['reconciliation_required']
 stage='PROGRAMMER_DISPATCH';assert current() is None
 result=dispatch(s,A)
 report('PROGRAMMER_RETURN.json',{'status':result.get('status'),'model_content_retained_by_wrapper':False})
 stage='POST_RUN_RECOVERY';r=recovery('TERMINAL','INDEPENDENT_TERMINAL_RECOVERY')
 report('CONTROLLER_RETURN.json',{'result':'RETURNED','recovery':r})
except BaseException as exc:
 if tx:tx.close();tx=None
 rows=events(audit) if audit.exists() else []
 report('ORCHESTRATION_STOP.json',{'stage':stage,'exception_type':type(exc).__name__,'frames':[{'file':f.filename,'line':f.lineno,'function':f.name} for f in traceback.extract_tb(exc.__traceback__)],
  'model_requests':sum(r.get('event')=='model_request_start' for r in rows),'automatic_retry':False,'pre_issuance_admission':'CLOSED_NO_RETRY' if control is None else 'SEE_RUN_CONTROL'})
 if control is not None:
  # Close admission, then reconcile through the unchanged typed cancellation.
  # A partial/uncertain transition is not repaired or inferred complete.
  try:
   with s.session():
    a=reconstruct_authorization(s,A);state=reconstruct(audit.read_bytes(),a,audit)
    if state['state']=='ACTIVE':
     fresh=start_control(a,audit,json.loads(a.model_transmission)['run_control']);fresh.close('R12_ORCHESTRATION_INTERRUPTED')
     tx=ActivationTransaction(a,audit,p['dispatch']['authority_id'])
     op=json.loads(a.operational_binding);op['dispatch_authorization']=p['dispatch']
     h=GovernedHost(replace(a,state='ACTIVE',operational_binding=canonical(op)),audit);h.revoke()
     cancelled=tx.cancel(h,'R12_ORCHESTRATION_INTERRUPTED');tx.close();tx=None
     fresh.emit('final_disposition',dict(cancelled,provider_uncertainty='REQUEST_OUTCOME_UNKNOWN' if fresh.requests!=fresh.responses else None))
     report('CANCELLATION.json',cancelled)
    elif state['state'] not in ('CANCELLED','COMPLETED','REVOKED'):
     fresh=start_control(a,audit,json.loads(a.model_transmission)['run_control']);fresh.close('R12_ORCHESTRATION_INTERRUPTED')
     report('UNRESOLVED_LIFECYCLE.json',{'state':state['state'],'phase':state['phase'],'uncertain':state['uncertain'],'no_inferred_ownership_release':True})
  except BaseException as failure:
   report('CANCELLATION_UNRESOLVED.json',{'exception_type':type(failure).__name__,'no_inferred_ownership_release':True})
  finally:
   if tx:tx.close();tx=None
 try:recovery('TERMINAL','INDEPENDENT_TERMINAL_RECOVERY')
 except BaseException as failure:report('RECOVERY_UNRESOLVED.json',{'exception_type':type(failure).__name__,'no_inferred_success':True})
 sys.exit(1)
finally:s.close()
