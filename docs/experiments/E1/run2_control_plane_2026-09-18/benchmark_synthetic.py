"""Whole non-E1 path including automatic cleanup; fake provider boundary only."""
import json,sys,time
from pathlib import Path
from unittest.mock import patch
from qualify import fixture,O
from adapter.invocation_issuance import issue_inactive,start_control
from adapter.activation_transaction import ActivationTransaction
from adapter.orchestration_boundary import recover_boundary,recover_then_dispatch
from adapter.responses_orchestrator import ResponsesReasoning
from adapter.run_control import E1_POLICY
from adapter.operator_projection import project
from adapter.validation_spans import recording
measurements=[]
for sample in range(4):
 f=fixture.Session('test_complete_dispatcher_handoff_and_cancellation');f.setUp();phases=[]
 start=time.monotonic()
 def record(name,fn):
  begin=time.monotonic();value=fn();phases.append({'phase':name,'seconds':time.monotonic()-begin});return value
 try:
  with f.store.session():
   record('INACTIVE_issuance',lambda:issue_inactive(f.a,f.audit,f.dr))
   tx=record('INACTIVE_recovery',lambda:ActivationTransaction.recover(f.a,f.audit,f.did));tx.close()
   c=start_control(f.a,f.audit,E1_POLICY)
   with recording(c):tx=record('activation',lambda:ActivationTransaction.activate(f.a,f.audit,f.did));tx.close()
  record('ACTIVE_recovery',lambda:recover_boundary(f.store,f.a.authorization_id))
  reached=[]
  def model(runner,payload):
   assert runner.orchestrator.host.auth.work_package_id!='E1-WP-001'
   assert runner.orchestrator.host.activation_transaction.verify_handoff()
   reached.append(time.monotonic()-start)
   return {'id':'synthetic-only-no-provider','output':[]}
  with patch.object(ResponsesReasoning,'_call',model):record('dispatcher_through_synthetic_response_and_cancel',lambda:recover_then_dispatch(f.store,f.a.authorization_id))
  terminal=record('terminal_status',lambda:project(f.store,f.a.authorization_id))
  assert terminal['lifecycle_state']=='CANCELLED' and terminal['ownership']=='RELEASED'
  measurements.append({'sample':sample,'phases':phases,'model_boundary_seconds':reached[0],'terminal_state':terminal['lifecycle_state']})
 finally:f.tearDown()
(O/'SYNTHETIC_TIMING.json').write_text(json.dumps({'scope':'SYNTHETIC_NON_E1_SUPERVISOR_STUB_NO_PROVIDER','actual_context':False,'samples':measurements},indent=2))
print(json.dumps(measurements))
