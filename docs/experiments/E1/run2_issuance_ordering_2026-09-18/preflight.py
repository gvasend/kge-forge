"""Read-only current authority preflight. Never issues or activates."""
import json,os,time
from pathlib import Path
from adapter.context_projection import sha,canonical
from adapter.controller_authority_store import ControllerAuthorityStore
from adapter.authority_bootstrap import reconstruct_authorization
from adapter.authorization_lifecycle import dispatch_binding,reconstruct,LifecycleDenied
from adapter.activation_transaction import invocation,_host,validate_production
from adapter.invocation_ownership import InvocationOwnership
from adapter.supervisor_amendment import readiness,authenticated_policy
from adapter.run_control import events,assert_admission,BudgetExceeded
O=Path(__file__).resolve().parent;D=O.parent/'run2_dispatch_2026-09-18'
pin=json.loads((D/'CURRENT_PIN.json').read_bytes());b=Path(pin['path']).read_bytes();assert sha(b)==pin['sha256'];pub=json.loads(b)
audit=Path(pub['audit']);initial=audit.read_bytes();rows=events(audit)
assert sha(initial)==json.loads((D/'FAIL_CLOSED_RESULT.json').read_bytes())['audit_sha256']
assert not any(r.get('event') in ('authorization_issued','authorization_lifecycle_activated','model_request_start','model_request_content_bound','action_request') for r in rows)
timing={}
def timed(name,fn):
 start=time.monotonic()
 try:return fn()
 finally:timing[name]=time.monotonic()-start
start=time.monotonic();st=timed('private_store_open',lambda:ControllerAuthorityStore(**pub['selected_store']))
with st.session():
 a=timed('cold_private_bootstrap',lambda:reconstruct_authorization(st,st.applicability['authorization_id']))
 ref={'authority_id':pub['dispatch_ref'],'sha256':pub['dispatch_ref'].split(':')[-1]}
 binding=timed('current_dispatch_binding',lambda:dispatch_binding(a,audit,ref))
 policy=timed('supervisor_policy',lambda:authenticated_policy(a,st))
 ready=timed('live_supervisor_readiness',lambda:readiness(a,st,policy['released_supervisor'],True,_host))
 assert ready['SupervisorInstanceId']=='SupervisorInstance-sha256:83f22718a56ab733257208c6e1dfe9767a95e0d10b82f8583f222f88ee9669a2'
 identity={'authorization_id':a.authorization_id,'session_id':a.session_id,'invocation_id':a.turn_id,'work_package_id':a.work_package_id}
 try:assert_admission(audit,json.loads(a.model_transmission)['run_control'],identity)
 except BudgetExceeded as e:admission=str(e)
 else:raise AssertionError('closed admission unexpectedly accepted')
 try:reconstruct(initial,a,audit)
 except LifecycleDenied as e:lifecycle=str(e)
 else:raise AssertionError('malformed failed audit unexpectedly accepted')
 own=InvocationOwnership(a.ownership_ledger);before=Path(a.ownership_ledger).read_bytes();fd=own._locked()
 try:
  assert invocation(fd) is None and own._history(fd) is None
  try:timed('production_validation',lambda:validate_production(a,audit,ref,fd))
  except BudgetExceeded as e:validation=str(e)
  else:raise AssertionError('production unexpectedly admitted closed audit')
 finally:os.close(fd)
 assert before==Path(a.ownership_ledger).read_bytes() and initial==audit.read_bytes()
 r={'verdict':'BLOCKED_REISSUANCE_BINDING_AND_CLOSED_ADMISSION','release_authority':a.context_binding.governance.run2['release_authority'],
  'dispatch_identity':pub['dispatch_ref'],'dispatch_binding':'PASS','supervisor':ready,'timing_seconds':timing,
  'production_validation':'BLOCKED: '+validation,'admission':'BLOCKED: '+admission,'lifecycle_reconstruction':'REJECTED: '+lifecycle,
  'ownership':'NONE','execution_scope':'NONE','authorization_issued':False,'activation':False,'model_requests':0,'effects':0,
  'failed_evidence_unchanged':True,'audit_sha256':sha(initial),'ownership_sha256':sha(before),'total_seconds':time.monotonic()-start}
st.close()
with (O/'PRODUCTION_PREFLIGHT.json').open('x') as f:f.write(canonical(r))
print(canonical(r))
