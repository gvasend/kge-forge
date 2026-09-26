"""Read-only evidence projection and first-action observation; never authority."""
import sys,json,time,os
from pathlib import Path
sys.path.insert(0,'/tmp/forge-attempt-chain-xjcb_jkz')
from adapter.context_projection import canonical,sha
from adapter.controller_authority_store import ControllerAuthorityStore,_directory,_put
from adapter.operator_projection import project
from adapter.run_control import events
O=Path(__file__).parent;pin=json.loads((O/'CURRENT_PIN.json').read_bytes());b=Path(pin['path']).read_bytes();assert sha(b)==pin['sha256'];p=json.loads(b)
B=Path(p['private_run_root']);A=p['r12_authorization_id'];audit=Path(p['audit']);s=ControllerAuthorityStore(**p['selected_store'])
(B/'operator_status').mkdir(mode=0o700,exist_ok=True);(O/'operator_status').mkdir(exist_ok=True)
def record(name,value):
 data=canonical(value).encode();fd=_directory(B)
 try:_put(fd,name,data);os.fsync(fd)
 finally:os.close(fd)
 (O/name).write_bytes(data)
def milestone(rows):
 idx=next((i for i,r in enumerate(rows) if r.get('event')=='action_request'),None)
 if idx is None:return
 action=rows[idx];rid=action['action_request_id'];timing=[r for r in rows[:idx] if r.get('schema')=='E1-RUN-CONTROL-1']
 cycle=timing[-1]['cycle'] if timing else None
 auth=next((r['details'].get('decision') for r in rows if r.get('event')=='authorization_decision' and r['details'].get('action_request_id')==rid),None)
 result=next((r for r in rows if r.get('event')=='action_result' and r.get('action_request_id')==rid),None)
 disposition=auth or (result.get('result') if result else 'PENDING')
 starts=[];intervals=[]
 for r in timing:
  if r['event']=='span_start' and r['details']['name']=='provider_transport':starts.append(r)
  if r['event']=='span_end' and r['details']['name']=='provider_transport' and starts:
   start=starts.pop();intervals.append({'cycle':r['cycle'],'seconds':r['monotonic']-start['monotonic'],'classification':'LOCAL_TRANSPORT_INTERVAL_NOT_PROVIDER_COMPUTE'})
 marker=json.loads((B/'ONE_ATTEMPT_STARTED').read_bytes())
 value={'milestone':'FIRST_REAL_PROGRAMMER_ACTION_REQUEST','authorization_id':A,'action_request_id':rid,'model_cycle':cycle,'operation':action.get('type'),
  'authorization_disposition':disposition,'elapsed_controller_seconds':action['time']-marker['monotonic'] if 'time' in action else None,
  'request_digest':action.get('request_sha256'),'action_record_sha256':sha(canonical(action).encode()),'observed_wall_time':time.time(),
  'provider_transport_intervals':intervals,'provider_processing_duration':'UNKNOWN','budget_history_at_request':[r['details'] for r in timing if r['event'] in ('budget_warning','budget_exhausted')],
  'source':'READ_ONLY_DURABLE_AUDIT_PROJECTION','does_not_interrupt':True}
 request=next((r for r in reversed(timing) if r['event']=='model_request_start' and r['cycle']==cycle),None)
 response=next((r for r in reversed(timing) if r['event']=='response_received' and r['cycle']==cycle),None)
 progress=next((r for r in reversed(timing) if r['event']=='substantive_progress'),None)
 value.update(model_request_identity=(request['details'].get('request_digest') if request else None),
  model_response_identity=(response['details'].get('response_id') if response else None),
  request_event_sha256=(request['record_sha256'] if request else None),response_event_sha256=(response['record_sha256'] if response else None),
  request_wall_time=(request['wall_time'] if request else None),response_wall_time=(response['wall_time'] if response else None),
  substantive_progress=(progress['details'] if progress else None),
  substantive_progress_monotonic=(progress['monotonic'] if progress else None),
  budget_policy_unchanged=True)
 if not (B/'FIRST_REAL_PROGRAMMER_ACTION_REQUEST.json').exists():record('FIRST_REAL_PROGRAMMER_ACTION_REQUEST.json',value)
 if disposition!='PENDING' and not (B/'FIRST_REAL_PROGRAMMER_ACTION_REQUEST_DISPOSITION.json').exists():record('FIRST_REAL_PROGRAMMER_ACTION_REQUEST_DISPOSITION.json',value)
try:
 while True:
  try:
   v=project(s,A)
   rows=events(audit) if audit.exists() else [];milestone(rows)
  except Exception as e:v={'freshness':'UNKNOWN','uncertainty':type(e).__name__,'projection_generated':time.time(),'authorization_id':A,'handoff_eligible':False}
  name=str(time.time_ns())+'.json';data=canonical(v).encode();fd=_directory(B/'operator_status')
  try:_put(fd,name,data);os.fsync(fd)
  finally:os.close(fd)
  (O/'operator_status'/name).write_bytes(data)
  print(canonical({k:v.get(k) for k in ('lifecycle_state','freshness','cycle','current_subphase','model_requests','responses','action_requests','ownership','budget_state','terminal_disposition')}),flush=True)
  if (O/'CONTROLLER_RETURN.json').exists() or ((O/'ORCHESTRATION_STOP.json').exists() and ((O/'INDEPENDENT_TERMINAL_RECOVERY.json').exists() or (O/'RECOVERY_UNRESOLVED.json').exists())):
   record('FINAL_OPERATOR_STATUS.json',v);break
  time.sleep(5)
finally:s.close()
