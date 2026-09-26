"""Non-E1 fixtures only. Kernel supervisor observation is explicitly mocked."""
import json,os,subprocess,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from adapter.tests.qualify_activation_transaction import fixture
from adapter.tests.test_controller_authority_store import private_fixture
from adapter.authorization_lifecycle import reconstruct,LifecycleDenied
from adapter.activation_transaction import ActivationTransaction,_lease
from adapter.controller_authority_store import ControllerAuthorityStore
from adapter.run_control import E1_POLICY,RunControl,BudgetExceeded,events,status
from adapter.context_projection import canonical
from adapter.governed_host import GovernedHost,Denied
from issuance import issue_inactive,start_control

class Ordering(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(prefix='issuance-order-synthetic-');self.root=Path(self.tmp.name)
  _,self.auth,self.audit,self.ref,_=fixture(self.root/'fixture',supervisor_identity={'synthetic':'not live'})
  self.store=private_fixture(self.auth,self.audit,self.ref,self.root/'private')
  self.ref={'authority_id':'E1-ARCHITECT-DISPATCH-sha256:'+self.ref['sha256'],'sha256':self.ref['sha256']}
  self.audit.rename(self.root/'fixture-setup-issuance.evidence')
  self.session=self.store.session();self.session.__enter__()
  self.mock=patch('adapter.activation_transaction._host',return_value={'synthetic':'mocked'});self.mock.start()
 def tearDown(self):
  self.mock.stop();self.session.__exit__(None,None,None);self.store.close();self.tmp.cleanup()
 def issue(self):return issue_inactive(self.auth,self.audit,self.ref)
 def control(self):return start_control(self.auth,self.audit,E1_POLICY)
 def restart(self):
  spec={'root':str(self.store.root),'catalog_sha256':self.store.catalog_sha256,'applicability':self.store.applicability}
  code='''import json,sys
from unittest.mock import patch
from adapter.controller_authority_store import ControllerAuthorityStore
from adapter.authority_bootstrap import reconstruct_authorization
from adapter.activation_transaction import ActivationTransaction
s=ControllerAuthorityStore(**json.loads(sys.argv[1]))
with s.session(),patch('adapter.activation_transaction._host',return_value={'synthetic':'mocked'}):
 a=reconstruct_authorization(s,sys.argv[2]);tx=ActivationTransaction.recover(a,sys.argv[3],sys.argv[4])
 print(json.dumps(tx.recovery));tx.close()
s.close()
'''
  r=subprocess.run([sys.executable,'-c',code,canonical(spec),self.auth.authorization_id,str(self.audit),self.ref['authority_id']],capture_output=True,text=True,timeout=45)
  self.assertEqual(r.returncode,0,r.stderr);return json.loads(r.stdout)
 def test_01_first_fact_and_restart_inactive(self):
  self.issue();rows=events(self.audit)
  self.assertEqual(rows[0]['event'],'authorization_issued');self.assertEqual(rows[0]['authorization']['state'],'INACTIVE')
  self.assertEqual(self.restart()['lifecycle_state'],'INACTIVE')
 def test_02_telemetry_requires_issuance(self):
  with self.assertRaises(FileNotFoundError):self.control()
  self.assertFalse(self.audit.exists())
 def test_03_telemetry_then_restart(self):
  self.issue();c=self.control();c.emit('activity',{})
  self.assertEqual(self.restart()['lifecycle_state'],'INACTIVE')
  self.assertEqual(events(self.audit)[0]['event'],'authorization_issued')
 def test_04_transaction_and_independent_active_owned(self):
  self.issue();self.control()
  tx=ActivationTransaction.activate(self.auth,self.audit,self.ref['authority_id']);tx.close()
  r=self.restart();self.assertEqual(r['lifecycle_state'],'ACTIVE');self.assertIsNotNone(r['ownership']);self.assertTrue(r['handoff_eligible'])
  names=[r['event'] for r in events(self.audit)]
  self.assertLess(names.index('authorization_lifecycle_activation_intent'),names.index('authorization_lifecycle_activated'))
 def test_05_premature_telemetry_and_missing_auth_rejected(self):
  RunControl(self.audit,{'synthetic':'malformed'},E1_POLICY)
  before=self.audit.read_bytes()
  with self.assertRaises(LifecycleDenied):reconstruct(before,self.auth,self.audit)
  with self.assertRaises(LifecycleDenied):self.issue()
  with self.assertRaises(LifecycleDenied):self.control()
  self.assertEqual(before,self.audit.read_bytes())
 def test_06_duplicate_issue_rejected_without_effect(self):
  self.issue();before=self.audit.read_bytes()
  with self.assertRaises(LifecycleDenied):self.issue()
  self.assertEqual(before,self.audit.read_bytes())
 def test_07_competing_controller_rejected(self):
  fd=_lease(Path(self.auth.ownership_ledger))
  try:
   with self.assertRaises(LifecycleDenied):self.issue()
   self.assertFalse(self.audit.exists())
  finally:os.close(fd)
 def test_08_closed_admission_never_reopened(self):
  self.issue();self.control().close('SYNTHETIC_STOP');before=self.audit.read_bytes()
  with self.assertRaises(BudgetExceeded):self.control()
  self.assertEqual(before,self.audit.read_bytes())
 def test_09_model_gate_before_active(self):
  host=self.issue()
  from adapter.responses_orchestrator import ResponsesReasoning
  from types import SimpleNamespace
  runner=ResponsesReasoning.__new__(ResponsesReasoning);runner.orchestrator=SimpleNamespace(host=host)
  with self.assertRaises(ValueError):runner._run('synthetic','synthetic',1)
  self.assertFalse(self.restart()['handoff_eligible'])
 def test_10_status_and_budgets(self):
  self.issue();c=self.control();c.emit('governance_observation',{'authorization':'INACTIVE','ownership':'NONE','supervisor':'UNKNOWN'})
  s=status(self.audit);self.assertEqual(s['model_requests'],0);self.assertEqual(s['authorization_state'],'INACTIVE')
  self.assertEqual(c.policy,E1_POLICY)

if __name__=='__main__':unittest.main(verbosity=2)
