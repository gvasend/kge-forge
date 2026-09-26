"""Synthetic end-to-end dispatcher qualification; never real E1 authority."""
import json,os,sys,tempfile,time,unittest,subprocess
from pathlib import Path
from dataclasses import replace
from unittest.mock import patch
from adapter.context_projection import canonical,sha
from adapter.controller_authority_store import current,ControllerAuthorityStore,AuthorityDenied
from adapter.tests.qualify_activation_transaction import fixture
from adapter.tests.test_controller_authority_store import private_fixture
from adapter.tests import test_governance_continuation as gc
from adapter.invocation_issuance import issue_inactive,start_control
from adapter.activation_transaction import ActivationTransaction
from adapter.orchestration_boundary import recover_boundary,recover_then_dispatch
from adapter.run_control import E1_POLICY,events,status
from adapter.validation_spans import recording
from adapter.operator_projection import project
from adapter.governed_host import GovernedHost

class Session(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory(prefix='synthetic-session-boundary-');self.out=Path(self.temp.name)
  original=gc.prepared
  def prepared(*args,**kw):
   vals=list(original(*args,**kw));a=vals[2];pol=json.loads(a.model_transmission);pol['run_control']=E1_POLICY;vals[2]=replace(a,model_transmission=canonical(pol));return tuple(vals)
  with patch.object(gc,'prepared',side_effect=prepared):
   self.root,self.a,self.audit,self.ref,self.projection=fixture(self.out/'fixture',supervisor_identity={'synthetic':'NON_LIVE'})
  assert self.a.work_package_id!='E1-WP-001'
  self.audit.rename(self.out/'fixture_setup_only.jsonl')
  self.store=private_fixture(self.a,self.audit,self.ref,self.out/'private')
  self.did='E1-ARCHITECT-DISPATCH-sha256:'+self.ref['sha256'];self.dr={'authority_id':self.did,'sha256':self.ref['sha256']}
  self.mock=patch('adapter.activation_transaction._host',return_value={'synthetic':'NON_LIVE'});self.mock.start()
 def tearDown(self):self.mock.stop();self.store.close();self.temp.cleanup()
 def activate(self):
  with self.store.session():
   issue_inactive(self.a,self.audit,self.dr)
   c=start_control(self.a,self.audit,E1_POLICY)
   with recording(c),c.span('validation'):t=ActivationTransaction.activate(self.a,self.audit,self.did)
   t.close()
  return c
 def test_complete_dispatcher_handoff_and_cancellation(self):
  self.activate();calls=[]
  def model(runner,payload):
   self.assertIs(current(),self.store);self.assertTrue(runner.orchestrator.host.activation_transaction.verify_handoff())
   self.assertEqual(runner.orchestrator.host.auth.authorization_id,self.a.authorization_id)
   self.assertNotIn('NEVER_TRANSMIT_MARKER',canonical(payload));calls.append(1)
   return {'id':'synthetic-response','output':[],'usage':{'input_tokens':1,'output_tokens':0,'total_tokens':1}}
  with patch('adapter.responses_orchestrator.ResponsesReasoning._call',model):result=recover_then_dispatch(self.store,self.a.authorization_id)
  self.assertEqual(len(calls),1);self.assertEqual(result['status'],'INCOMPLETE');self.assertIsNone(current())
  observed=project(self.store,self.a.authorization_id);self.assertEqual(observed['lifecycle_state'],'CANCELLED');self.assertEqual(observed['ownership'],'RELEASED')
  self.assertEqual(observed['architectural_state'],'QUIESCENT')
 def test_nested_session_guard_preserved(self):
  self.activate();before=self.audit.read_bytes()
  with self.store.session(),patch('adapter.responses_orchestrator.ResponsesReasoning._call') as model:
   with self.assertRaises(AuthorityDenied):recover_then_dispatch(self.store,self.a.authorization_id)
   from adapter.controlled_dispatch import dispatch
   with self.assertRaises(AuthorityDenied):dispatch(self.store,self.a.authorization_id)
   model.assert_not_called()
  self.assertEqual(before,self.audit.read_bytes())
 def test_failure_between_sessions_no_authority_lost(self):
  self.activate()
  with patch('adapter.orchestration_boundary.dispatch',side_effect=RuntimeError('synthetic boundary interruption')):
   with self.assertRaises(RuntimeError):recover_then_dispatch(self.store,self.a.authorization_id)
  self.assertIsNone(current());r=recover_boundary(self.store,self.a.authorization_id)
  self.assertTrue(r['handoff_eligible']);self.assertEqual(r['ownership']['authorization_id'],self.a.authorization_id)
 def test_binding_substitution_before_dispatch_denied(self):
  self.activate();original=self.store.resolve
  def resolve(k):
   if k==self.a.authorization_id:
    v=json.loads(original(k));v['work_package_id']='substituted';return canonical(v).encode()
   return original(k)
  with patch.object(self.store,'resolve',side_effect=resolve),patch('adapter.responses_orchestrator.ResponsesReasoning._call') as m:
   with self.assertRaises((ValueError,RuntimeError)):recover_then_dispatch(self.store,self.a.authorization_id)
   m.assert_not_called()
 def test_terminal_authority_dominates_stale_provisional_status(self):
  c=self.activate()
  with self.store.session():
   t=ActivationTransaction.recover(self.a,self.audit,self.did)
   c.close('synthetic failure');c.emit('final_disposition',{'disposition':'INDETERMINATE','ownership':'UNKNOWN'})
   h=GovernedHost(t.auth,self.audit);h.revoke();t.cancel(h,'synthetic cancellation');t.close()
  before=self.audit.read_bytes()
  observed=project(self.store,self.a.authorization_id)
  self.assertEqual(observed['lifecycle_state'],'CANCELLED');self.assertEqual(observed['ownership'],'RELEASED');self.assertIsNone(observed['uncertainty'])
  self.assertEqual(before,self.audit.read_bytes())
  with patch('adapter.operator_projection.status',return_value={'freshness':'UNKNOWN','terminal_disposition':{'disposition':'ACTIVE'}}):
   again=project(self.store,self.a.authorization_id);self.assertEqual(again['terminal_disposition']['disposition'],'CANCELLED')
  with patch('adapter.operator_projection.reconstruct_authorization',side_effect=OSError('missing source')):
   self.assertEqual(project(self.store,self.a.authorization_id)['freshness'],'UNKNOWN')
 def test_stale_active_projection_is_unknown(self):
  self.activate()
  with patch('adapter.operator_projection.status',return_value={'freshness':'UNKNOWN','terminal_disposition':{'disposition':'INDETERMINATE'}}):
   v=project(self.store,self.a.authorization_id)
   self.assertEqual(v['freshness'],'UNKNOWN');self.assertIsNone(v['current_subphase']);self.assertFalse(v['handoff_eligible'])
 def test_warning_persisted_under_transaction_without_nested_lock(self):
  c=self.activate()
  with self.store.session():
   t=ActivationTransaction(self.a,self.audit,self.did);ledger,audit=t._locks()
   try:
    c.emit('budget_warning',{'budget':'phase','value':30,'operation':'synthetic-lock-probe'})
   finally:t._unlock(ledger,audit);t.close()
  row=next(r for r in reversed(events(self.audit)) if r['event']=='warning_persisted')
  print('WARNING_TIMING '+canonical(row['details']),flush=True)
  self.assertLess(row['details']['creation_to_persistence_seconds'],.5)
  self.assertLess(row['details']['lock_wait_seconds'],.05)
if __name__=='__main__':unittest.main(verbosity=2)
