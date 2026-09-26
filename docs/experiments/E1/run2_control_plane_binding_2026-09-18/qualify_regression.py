"""Non-E1 probes; never selects a new production attempt or calls a provider."""
import importlib.util, json, sys, tempfile, time, unittest
from pathlib import Path
from unittest.mock import patch
O=Path(__file__).resolve().parent
sys.path.insert(0,str(O/'candidate'))
from adapter.run_control import RunControl,E1_POLICY,BudgetExceeded,events,decode_events,assert_admission
from adapter.validation_spans import recording,span
from adapter.operator_projection import observational_extension,project
from adapter.activation_transaction import ActivationTransaction
from adapter.governed_host import GovernedHost
from adapter.context_projection import canonical,sha
spec=importlib.util.spec_from_file_location('session_fixture',O.parent/'run2_r10_transition_2026-09-18/qualify_session.py')
fixture=importlib.util.module_from_spec(spec);spec.loader.exec_module(fixture)

class ControlPlane(fixture.Session):
 # Inherited fixtures expose synthetic authority only. Select focused tests below.
 def test_closed_telemetry_typed_cancel(self):
  c=self.activate()
  with self.store.session():
   t=ActivationTransaction.recover(self.a,self.audit,self.did)
   h=GovernedHost(t.auth,self.audit);t.attach(h);h.revoke()
   c.progress=c.clock()-301
   with self.assertRaises(BudgetExceeded):c.check()
   with recording(c):
    with self.assertRaises(BudgetExceeded):
     with span('attempt_history_ancestry'):pass
    original=__import__('adapter.activation_transaction',fromlist=['reconstruct']).reconstruct
    def instrumented(*args,**kw):
     with span('attempt_history_ancestry'):return original(*args,**kw)
    with patch('adapter.activation_transaction.reconstruct',side_effect=instrumented):
     result=t.cancel(h,'HARD_BUDGET_STOP')
    with self.assertRaises(BudgetExceeded):
     with span('validation'):pass
   self.assertEqual(result['disposition'],'CANCELLED');t.close()
   recovered=ActivationTransaction.recover(self.a,self.audit,self.did)
   try:
    self.assertEqual(recovered.recovery['lifecycle_state'],'CANCELLED')
    self.assertIsNone(recovered.recovery['ownership'])
   finally:recovered.close()
  with self.assertRaises(BudgetExceeded):assert_admission(self.audit,E1_POLICY,c.identity)
  v=project(self.store,self.a.authorization_id)
  self.assertEqual(v['architectural_state'],'QUIESCENT');self.assertEqual(v['ownership'],'RELEASED')
 def test_observational_suffix_and_negatives(self):
  c=self.activate();before=self.audit.read_bytes()
  c.emit('activity',{'operation':'model_projection'})
  self.assertTrue(observational_extension(before,self.audit.read_bytes(),self.a))
  for event,details in [('activity',{'operation':'unknown'}),('model_request_start',{}),('budget_exhausted',{'budget':'no_progress','value':300,'operation':'model_projection','last_progress':c.progress})]:
   prefix=self.audit.read_bytes();c.emit(event,details)
   self.assertFalse(observational_extension(prefix,self.audit.read_bytes(),self.a))
  data=self.audit.read_bytes()
  self.assertFalse(observational_extension(before,data.replace(b'authorization_issued',b'authorization_forged'),self.a))
 def test_status_telemetry_during_reconstruction(self):
  c=self.activate()
  import adapter.operator_projection as op
  original=op.reconstruct
  def busy(*args,**kw):
   result=original(*args,**kw);c.emit('activity',{'operation':'model_projection'});return result
  with patch.object(op,'reconstruct',side_effect=busy):v=project(self.store,self.a.authorization_id,snapshot_attempts=1)
  self.assertEqual(v['freshness'],'FRESH');self.assertEqual(v['ownership'],'OWNERSHIP_HELD')
  self.assertTrue(v['authority_basis']['observation_only_extension'])
 def test_current_catalog_tamper_not_cached(self):
  p=self.store.root/'catalog.json';before=p.read_bytes();self.store._verify_catalog()
  try:
   p.write_bytes(before+b' ')
   with self.assertRaises(ValueError):self.store._verify_catalog()
  finally:p.write_bytes(before)
  self.store._verify_catalog()
 def test_no_progress_unchanged(self):
  c=self.activate();progress=c.progress
  for _ in range(3):
   c.emit('activity',{'operation':'model_projection'})
   with recording(c),span('validation'):pass
  self.assertEqual(c.progress,progress)
 def test_automatic_pre_model_budget_cancellation(self):
  self.activate()
  from adapter.orchestration_boundary import recover_then_dispatch
  from adapter.responses_orchestrator import ResponsesReasoning
  def exhausted(runner,*args,**kwargs):
   runner.control.progress=runner.control.clock()-301
   runner.control.check()
  with patch.object(ResponsesReasoning,'_run',exhausted),patch.object(ResponsesReasoning,'_call') as provider:
   with self.assertRaises(BudgetExceeded):recover_then_dispatch(self.store,self.a.authorization_id)
   provider.assert_not_called()
  v=project(self.store,self.a.authorization_id)
  self.assertEqual(v['lifecycle_state'],'CANCELLED');self.assertEqual(v['ownership'],'RELEASED')
  self.assertEqual(v['architectural_state'],'QUIESCENT')
  self.assertFalse(any(r.get('event')=='model_request_start' for r in events(self.audit)))
 def test_closed_telemetry_does_not_clear_uncertainty(self):
  c=self.activate()
  with self.store.session():
   t=ActivationTransaction.recover(self.a,self.audit,self.did)
   h=GovernedHost(t.auth,self.audit);t.attach(h);h.revoke()
   h._actions_inflight.add('synthetic-unresolved-action');c.close('TEST_CLOSED')
   try:
    with recording(c):result=t.cancel(h,'TEST_CLOSED')
    self.assertEqual(result['disposition'],'INDETERMINATE')
    self.assertEqual(result['ownership'],'HELD_FOR_RECONCILIATION')
   finally:t.close()

if __name__=='__main__':
 names=['test_closed_telemetry_typed_cancel','test_closed_telemetry_does_not_clear_uncertainty','test_automatic_pre_model_budget_cancellation','test_observational_suffix_and_negatives',
 'test_status_telemetry_during_reconstruction','test_current_catalog_tamper_not_cached',
 'test_no_progress_unchanged','test_complete_dispatcher_handoff_and_cancellation',
 'test_nested_session_guard_preserved','test_failure_between_sessions_no_authority_lost',
 'test_binding_substitution_before_dispatch_denied','test_terminal_authority_dominates_stale_provisional_status']
 suite=unittest.TestSuite(ControlPlane(n) for n in names)
 result=unittest.TextTestRunner(verbosity=2).run(suite)
 (O/'QUALIFICATION.json').write_text(json.dumps({'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'result':'PASS' if result.wasSuccessful() else 'FAIL','scope':'NON_E1_SYNTHETIC','real_model_requests':0},indent=2))
 sys.exit(not result.wasSuccessful())
