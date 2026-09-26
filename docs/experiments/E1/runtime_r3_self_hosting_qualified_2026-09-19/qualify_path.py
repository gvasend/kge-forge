"""Genuine production functions; isolated identity/ledger, exact released payload.
No validator, host, supervisor or provider function is mocked.
"""
import json,os,sys,time,signal,subprocess
from pathlib import Path
O=Path(__file__).resolve().parent
publications=json.loads((O/'QUALIFICATION_BINDINGS.json').read_bytes());p=next(x for x in publications if x['name']==sys.argv[1])
sys.path.insert(0,p['runtime_root'])
from adapter.context_projection import canonical,sha
from adapter.controller_authority_store import ControllerAuthorityStore
from adapter.authority_bootstrap import reconstruct_authorization
from adapter.activation_transaction import ActivationTransaction,_validate_production
from adapter.invocation_issuance import issue_inactive,start_control
from adapter.orchestration_boundary import recover_boundary
from adapter.controlled_dispatch import dispatch
from adapter.run_control import E1_POLICY,BudgetExceeded,events
from adapter.validation_spans import recording
from adapter.operator_projection import project
root=Path(p['audit']).parent
assert not os.path.lexists(p['audit']) and Path(p['ownership_ledger']).read_bytes()==b''
log=root/'qualification-phases.jsonl';phase_rows=[];begin=time.monotonic();seq=0;control=None

def save_event(event,**data):
 global seq
 seq+=1;row={'schema':'NON_AUTHORIZING_QUALIFICATION_TIMING-1','sequence':seq,'authorization_id':p['authorization_id'],'event':event,'monotonic':time.monotonic(),'wall':time.time(),**data}
 with log.open('a') as f:f.write(canonical(row)+'\n');f.flush();os.fsync(f.fileno())
 return row

def phase(name,fn):
 started=time.monotonic();save_event('phase_start',phase=name)
 previous=signal.getsignal(signal.SIGALRM)
 def hard(*_):raise BudgetExceeded('qualification phase hard threshold: '+name)
 if control is None:signal.signal(signal.SIGALRM,hard);signal.setitimer(signal.ITIMER_REAL,120)
 try:return fn()
 finally:
  if control is None:signal.setitimer(signal.ITIMER_REAL,0);signal.signal(signal.SIGALRM,previous)
  seconds=time.monotonic()-started;phase_rows.append({'phase':name,'seconds':seconds,'soft_warning':seconds>=30,'hard_exceeded':seconds>=120});save_event('phase_end',**phase_rows[-1])

# Controlled scheduling only in the hard-budget stress case. No production
# function is replaced and no verifier result is supplied. Independent readers
# observe real committed bytes after the actual typed append returns.
profile_seen=set()
if p['name']=='hard-cancellation':
 import threading
 from adapter.authorization_lifecycle import _append as typed_append
 target=typed_append.__code__
 checkpoints={'authorization_issued','authorization_lifecycle_activation_intent','invocation_reserved','authorization_lifecycle_activated','invocation_released'}
 def committed_profile(frame,event,arg):
  if event!='return' or frame.f_code is not target:return
  name=frame.f_locals.get('row',{}).get('event')
  if name not in checkpoints or name in profile_seen:return
  profile_seen.add(name);started=time.monotonic();answer=[]
  def observe_transition():
   other=ControllerAuthorityStore(**p['selected_store'])
   try:answer.append(project(other,p['authorization_id']))
   finally:other.close()
  reader=threading.Thread(target=observe_transition);reader.start();reader.join(timeout=25)
  if reader.is_alive():raise RuntimeError('bounded transition observer exceeded 25 seconds')
  if not answer:raise RuntimeError('transition observer failed')
  row={'schema':'NON_AUTHORIZING_TRANSITION_OBSERVATION-1','committed_event':name,'monotonic':time.monotonic(),'wall':time.time(),'pause_seconds':time.monotonic()-started,'snapshot':answer[0]}
  with (root/'TRANSITION_STATUS.jsonl').open('a') as f:f.write(canonical(row)+'\n');f.flush();os.fsync(f.fileno())
 sys.setprofile(committed_profile)

s=ControllerAuthorityStore(**p['selected_store']);out={'qualification_only':True,'production_functions_mocked':False,'provider_calls':0};tx=None;monitor=None
try:
 monitor=subprocess.Popen([sys.executable,'-B',str(O/'monitor.py'),p['name']],stdout=(root/'monitor.log').open('w'),stderr=subprocess.STDOUT)
 with s.session():
  auth=phase('private_bootstrap',lambda:reconstruct_authorization(s,p['authorization_id']))
  fd=os.open(p['ownership_ledger'],os.O_RDONLY|os.O_NOFOLLOW)
  try:pre=phase('preflight',lambda:_validate_production(auth,p['audit'],p['dispatch'],fd,_preissuance=True))
  finally:os.close(fd)
  out['preflight']=pre
  # Issuance is the first authorization-lifecycle fact. Outer diagnostics above
  # are explicitly separate from the authorization audit and cannot issue it.
  phase('INACTIVE_issuance',lambda:issue_inactive(auth,p['audit'],p['dispatch']))
  tx=phase('INACTIVE_recovery',lambda:ActivationTransaction.recover(auth,p['audit'],p['dispatch']['authority_id']))
  assert tx.recovery['lifecycle_state']=='INACTIVE' and tx.recovery['ownership'] is None and not tx.recovery['handoff_eligible'];tx.close();tx=None
  control=start_control(auth,p['audit'],E1_POLICY)
  with recording(control):
   def activate():
    with control.span('validation'):return ActivationTransaction.activate(auth,p['audit'],p['dispatch']['authority_id'])
   tx=phase('activation',activate)
  tx.close();tx=None
 # Independent process, own authority-store session and durable reconstruction.
 save_event('phase_start',phase='independent_ACTIVE_recovery');t=time.monotonic();child=subprocess.run([sys.executable,'-B',str(O/'independent.py'),p['name'],'ACTIVE'],capture_output=True,text=True,timeout=120)
 phase_rows.append({'phase':'independent_ACTIVE_recovery','seconds':time.monotonic()-t,'soft_warning':time.monotonic()-t>=30,'hard_exceeded':False});save_event('phase_end',**phase_rows[-1])
 assert child.returncode==0,child.stderr
 out['independent_active']=json.loads(child.stdout);assert out['independent_active']['handoff_eligible']
 # Dispatcher owns its session. The bound implementation stops before the
 # model_request_content_bound/model_request_start/transport boundary.
 started=time.monotonic();save_event('phase_start',phase='dispatcher_to_ready_or_stop')
 try:result=dispatch(s,p['authorization_id']);out['dispatcher']=result
 except BudgetExceeded as exc:
  out['dispatcher']={'status':'HARD_BUDGET_STOP','reason':str(exc)}
 out['dispatcher_wall_seconds']=time.monotonic()-started
 save_event('phase_end',phase='dispatcher_through_automatic_cancellation',seconds=out['dispatcher_wall_seconds'])
 rows=events(p['audit']);ready=[r for r in rows if r.get('event')=='model_request_ready']
 if ready:out['cumulative_model_request_ready_seconds']=ready[0]['monotonic']-begin
 out['ready_reached']=bool(ready)
 assert not any(r.get('event') in ('model_request_start','transport_start','action_request','execution_scope_created','model_request_content_bound') for r in rows)
 terminal=subprocess.run([sys.executable,'-B',str(O/'independent.py'),p['name'],'TERMINAL'],capture_output=True,text=True,timeout=120)
 assert terminal.returncode==0,terminal.stderr;out['terminal_recovery']=json.loads(terminal.stdout)
 assert out['terminal_recovery']['lifecycle_state']=='CANCELLED' and out['terminal_recovery']['ownership'] is None
 out['result']='PASS' if out['ready_reached'] else 'BLOCKED_BEFORE_MODEL_REQUEST_READY'
except BaseException as exc:
 out.update(result='BLOCKED',error=type(exc).__name__+': '+str(exc))
 raise
finally:
 sys.setprofile(None)
 if tx:tx.close()
 out.update(phases=phase_rows,total_seconds=time.monotonic()-begin,real_invocations=0,real_model_requests=0,real_effects=0)
 (root/'PATH_RESULT.json').write_text(canonical(out));(O/('PATH_'+p['name']+'.json')).write_text(canonical(out))
 (root/'MONITOR_STOP').write_text('qualification ended')
 if monitor:
  try:monitor.wait(timeout=45)
  except subprocess.TimeoutExpired:monitor.terminate();monitor.wait(timeout=10)
 s.close()
print(canonical(out))
