"""Read-only terminal evidence, status and bounded source-based failure analysis."""
import json,sys,time,os,copy,hashlib,traceback
from pathlib import Path
sys.path.insert(0,'/tmp/forge-r10-transition-jxppjwou')
from adapter.context_projection import canonical,sha
from adapter.controller_authority_store import ControllerAuthorityStore,_directory,_put
from adapter.authority_bootstrap import reconstruct_authorization
from adapter.authorization_lifecycle import reconstruct
from adapter.recovery_ledger import reconstruct as recover_actions
from adapter.activation_transaction import invocation
from adapter.invocation_ownership import InvocationOwnership
from adapter.operator_projection import project
from adapter.run_control import events
from adapter.attempt_transition import terminal
O=Path(__file__).parent;pin=json.loads((O/'CURRENT_PIN.json').read_bytes());b=Path(pin['path']).read_bytes();assert sha(b)==pin['sha256'];p=json.loads(b);B=Path(p['private_run_root'])
s=ControllerAuthorityStore(**p['selected_store']);begin=time.monotonic()
def save(n,v):
 b=canonical(v).encode();fd=_directory(B)
 try:_put(fd,n,b);os.fsync(fd)
 finally:os.close(fd)
 (O/n).write_bytes(b)
try:
 with s.session():
  a=reconstruct_authorization(s,p['r10_authorization_id']);g=a.context_binding.governance;rows=events(p['audit']);raw=Path(p['audit']).read_bytes()
  life=reconstruct(raw,a,Path(p['audit']));actions=recover_actions(p['audit'],a)
  fd=os.open(a.ownership_ledger,os.O_RDONLY|os.O_NOFOLLOW)
  try:owner=invocation(fd);scope=InvocationOwnership.__new__(InvocationOwnership)._history(fd)
  finally:os.close(fd)
  assert life['state']=='CANCELLED' and not life['uncertain'] and owner is None and scope is None and actions['scope'] is None and not actions['incomplete']
  counts={k:sum(r.get('event')==v for r in rows) for k,v in {'model_requests':'model_request_start','model_responses':'response_received','model_content_bindings':'model_request_content_bound','ActionRequests':'action_request','ActionResults':'action_result','ExecutionScopes':'execution_scope_created'}.items()}
  assert all(v==0 for v in counts.values())
  facts={'disposition':'CANCELLED','classification':'INTERRUPTED_NO_EFFECTS','ownership':'RELEASED','architectural_state':'QUIESCENT','ExecutionScope':'NONE','reconciliation_required':False,'counts':counts,
   'audit_sha256':sha(raw),'ownership_ledger_sha256':sha(Path(a.ownership_ledger).read_bytes()),'terminal_event_id':life['last_event_id'],'activation_event_id':life['activation_event']['event_id'],
   'reservation_id':life['activation_event']['ownership_reservation']['reservation_id'],'uncertainty':None,'provider_activity':'NO_R10_MODEL_OR_PROVIDER_REQUEST_INITIATED','budget_state':'NO_HARD_EXHAUSTION_OBSERVED'}
  save('TERMINAL_EVIDENCE.json',facts)
  # Isolated in-memory forensic reproduction, no real lifecycle/store mutation.
  proof=copy.deepcopy(g.run6['predecessor']);reservation=json.loads((O/'ACTIVE_COMMIT.json').read_bytes())['reservation'];proof['terminal']['ownership']=reservation
  try:terminal(s,g.run6['amendment'],g.run6['proposal'],proof)
  except ValueError as e:
   diagnosis={'result':'REPRODUCED_IN_MEMORY','reason':str(e),'source':'frozen terminal-attempt verifier','input_difference':'predecessor proof captured shared-ledger current owner r10 rather than None','predecessor_lifecycle':proof['terminal']['lifecycle']['state'],
    'predecessor_authorization':g.run6['proposal']['predecessor']['authorization_id'],'observed_successor_authorization':reservation['authorization_id'],
    'does_not_change_real_ownership':True,'original_failure_stderr_sha256':json.loads((O/'INDEPENDENT_ACTIVE_RECOVERY_FAILURE.json').read_bytes())['stderr_sha256'],
    'limitation':'Original recovery stderr was retained only as a fingerprint; diagnosis is based on durable ownership ordering, frozen source and isolated reproduction, not recovered original message text.',
    'mechanism':'Cold predecessor peer reports the shared ledger current owner; terminal() additionally requires captured proof ownership to be None, rejecting successor ownership even though fresh ownership is correctly filtered by predecessor identity.',
    'cache_implication':'Warm parent proof captured before reservation had ownership None; cold recovery after reservation captures r10 ownership. A monitor that caches the latter proof can continue UNKNOWN after cancellation until a fresh reconstruction.'}
   save('FAILURE_ANALYSIS.json',diagnosis)
  else:raise AssertionError('expected captured-owner rejection not reproduced')
 # Warm authority reconstruction retains immutable evidence reuse, but project
 # still performs its qualified fresh lifecycle/ledger consistency checks.
 status=project(s,a.authorization_id);save('FRESH_TERMINAL_OPERATOR_STATUS.json',status)
 assert status['lifecycle_state']=='CANCELLED' and status['ownership']=='RELEASED' and status['architectural_state']=='QUIESCENT'
 assert raw==Path(p['audit']).read_bytes()
 save('POST_TERMINAL_INSPECTION.json',{'result':'PASS','seconds':time.monotonic()-begin,'audit_unchanged':True,'status_freshness':status['freshness'],'real_model_requests_added':0})
 print(canonical({'terminal':facts,'status':status['lifecycle_state'],'diagnosis':diagnosis['reason']}))
finally:s.close()
