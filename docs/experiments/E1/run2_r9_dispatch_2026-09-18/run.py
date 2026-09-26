"""Single Architect-authorized r9 attempt using frozen typed production operations.

No retry, no authority edits, no production-module changes, no host tool delegation.
"""
import json,os,sys,time,subprocess,traceback
from pathlib import Path
from adapter.context_projection import canonical,sha
from adapter.controller_authority_store import ControllerAuthorityStore,_directory,_put
from adapter.authority_bootstrap import reconstruct_authorization
from adapter.invocation_attempt import claim,predecessor_no_effects
from adapter.invocation_issuance import issue_inactive,start_control
from adapter.activation_transaction import ActivationTransaction,_host,invocation
from adapter.invocation_ownership import InvocationOwnership
from adapter.supervisor_amendment import readiness
from adapter.validation_spans import recording
from adapter.run_control import events,BudgetExceeded,status
from adapter.controlled_dispatch import dispatch
O=Path('/home/gvasend/app/kge-forge/docs/experiments/E1/run2_r9_dispatch_2026-09-18')
pin=json.loads((O/'CURRENT_PIN.json').read_bytes());data=Path(pin['path']).read_bytes();assert sha(data)==pin['sha256'];pub=json.loads(data)
B=Path(pub['private_run_root']);A=pub['r9_authorization_id'];audit=Path(pub['audit']);begin=time.monotonic();control=None;tx=None
# Exclusive start marker is operational diagnostics, never authorization lifecycle.
fd=os.open(B/'ONE_ATTEMPT_STARTED',os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600);os.write(fd,canonical({'wall_time':time.time(),'pid':os.getpid(),'automatic_retry':False}).encode());os.fsync(fd);os.close(fd)
def report(name,value):
 value=dict(value,wall_time=time.time(),controller_elapsed=time.monotonic()-begin)
 b=canonical(value).encode();fd=_directory(B)
 try:_put(fd,name,b);os.fsync(fd)
 finally:os.close(fd)
 (O/name).write_bytes(b);print(canonical({'event':name,**value}),flush=True)
def recover(label):
 r=subprocess.run([sys.executable,'-B',str(Path(__file__).with_name('r9_recover.py')),str(O/'CURRENT_PIN.json')],capture_output=True,text=True,timeout=120)
 if r.returncode:
  report(label+'_FAILURE.json',{'result':'FAIL','returncode':r.returncode,'stderr_sha256':sha(r.stderr.encode())})
  raise RuntimeError('independent recovery failed')
 result=json.loads(r.stdout);report(label+'.json',result);return result
s=ControllerAuthorityStore(**pub['selected_store']);stage='PRE_ISSUANCE'
try:
 with s.session():
  a=reconstruct_authorization(s,A);g=a.context_binding.governance;p=g.run5['proposal']
  assert g.run5['release_authority']==pub['release_authority'] and g.identities==pub['operational_identities']
  assert pub['proposal']['sha256']=='cb68a30719e88496504cd38004750b5b6848e4f31f1836387b87984ae92a8adc'
  assert not os.path.lexists(audit);predecessor_no_effects(p)
  ledger_id=p['DispatchAuthorizationId']+':attempt-ledger';assert s.state_path(ledger_id).read_bytes()==b''
  own=InvocationOwnership(a.ownership_ledger);fd=own._locked()
  try:assert invocation(fd) is None and own._history(fd) is None
  finally:os.close(fd)
  ready=readiness(a,s,{},True,_host)
  assert ready['SupervisorInstanceId']=='SupervisorInstance-sha256:83f22718a56ab733257208c6e1dfe9767a95e0d10b82f8583f222f88ee9669a2'
  assert ready['SupervisorSuccessionHead']=='SupervisorSuccession-sha256:b86bbb15d9d9d468b2de87926ad6b1cb4063218fd71eb5426089f689c0aecce8'
  report('IMMEDIATE_PRE_ISSUANCE.json',{'result':'PASS','supervisor':ready['SupervisorInstanceId'],'r8_immutable':True,'audit_unused':True,'ownership':'NONE'})
  allocation=claim(s,pub['proposal'],ledger_id);stage='ALLOCATED_NOT_ISSUED'
  report('ATTEMPT_ALLOCATION.json',{'allocation_id':allocation['id'],'authorization_id':A,'lifecycle_issued':False,'ownership':'NONE'})
  issue_inactive(a,audit,pub['dispatch']);stage='INACTIVE'
  rows=events(audit);assert rows[0]['event']=='authorization_issued' and rows[0]['authorization']['state']=='INACTIVE'
  control=start_control(a,audit,json.loads(a.model_transmission)['run_control'])
  report('INACTIVE_ISSUANCE.json',{'state':'INACTIVE','first_event':'authorization_issued','audit_sha256':sha(audit.read_bytes()),'ownership':'NONE'})
  with recording(control),control.span('context_reconstruction'):
   recovered=recover('INDEPENDENT_INACTIVE_RECOVERY')
  assert recovered['lifecycle_state']=='INACTIVE' and recovered['ownership'] is None and not recovered['handoff_eligible'] and not recovered['reconciliation_required']
  control.emit('governance_observation',{'authorization':'INACTIVE','ownership':'NONE','supervisor':'READY'})
  stage='ACTIVATION'
  with recording(control),control.span('validation'):
   tx=ActivationTransaction.activate(a,audit,pub['dispatch']['authority_id'])
  report('ACTIVE_COMMIT.json',{'state':tx.auth.state,'reservation':tx.reservation,'audit_sha256':sha(audit.read_bytes())})
  tx.close();tx=None;stage='ACTIVE_RECOVERY'
  with recording(control),control.span('activation_recovery'):
   recovered=recover('INDEPENDENT_ACTIVE_RECOVERY')
  assert recovered['lifecycle_state']=='ACTIVE' and recovered['ownership'] is not None and recovered['handoff_eligible'] and not recovered['reconciliation_required']
  control.emit('governance_observation',{'authorization':'ACTIVE','ownership':'OWNERSHIP_HELD','supervisor':'READY'})
  stage='PROGRAMMER_DISPATCH'
  result=dispatch(s,A)
  # Preserve only safe summary. Protected model content is not copied here.
  report('PROGRAMMER_RETURN.json',{'status':result.get('status'),'model_content_retained_by_wrapper':False})
  stage='POST_RUN_RECOVERY';recovered=recover('INDEPENDENT_TERMINAL_RECOVERY')
  report('CONTROLLER_RETURN.json',{'result':'RETURNED','recovery':recovered})
except BaseException as exc:
 if tx:tx.close();tx=None
 rows=events(audit) if audit.exists() else []
 final=next((r['details'] for r in reversed(rows) if r.get('event')=='final_disposition'),None)
 if control is not None and final is None:
  control.close('R9_ORCHESTRATION_INTERRUPTED')
  # No inferred cancellation or ownership release if a qualified transaction did not establish it.
  control.emit('final_disposition',{'disposition':'INDETERMINATE','ownership':'UNKNOWN','uncertainty':'ORCHESTRATION_INTERRUPTED_RECONCILIATION_REQUIRED','reason':type(exc).__name__})
 report('ORCHESTRATION_STOP.json',{'stage':stage,'exception_type':type(exc).__name__,'frames':[{'file':f.filename,'line':f.lineno,'function':f.name} for f in traceback.extract_tb(exc.__traceback__)],
  'model_requests':sum(r.get('event')=='model_request_start' for r in rows),'automatic_retry':False,
  'pre_issuance_admission':'CLOSED_NO_RETRY' if control is None else 'SEE_DURABLE_RUN_CONTROL','qualified_final_disposition':final})
 try:recover('INDEPENDENT_STOP_RECOVERY')
 except BaseException as recovery_exc:report('RECOVERY_UNRESOLVED.json',{'exception_type':type(recovery_exc).__name__,'no_inferred_ownership_release':True})
 sys.exit(1)
finally:s.close()
