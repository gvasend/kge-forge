"""Bounded, non-E1 ownership/status/session qualification."""
import sys,json,copy,tempfile,unittest,os,importlib.util,subprocess
from pathlib import Path
from unittest.mock import patch
O=Path(__file__).parent;sys.path.insert(0,str(O/'candidate'))
from adapter.attempt_ownership import attribute,lifecycle_ownership,observe
from adapter.context_projection import canonical,digest
from adapter.operator_projection import project
from adapter.run_control import E1_POLICY
from adapter.authorization_lifecycle import reconstruct
from adapter.invocation_issuance import issue_inactive,start_control
from adapter.activation_transaction import ActivationTransaction
from adapter.governed_host import GovernedHost
from adapter.validation_spans import recording

spec=importlib.util.spec_from_file_location('prior_session',O.parent/'run2_r10_transition_2026-09-18/qualify_session.py')
prior=importlib.util.module_from_spec(spec);spec.loader.exec_module(prior)

class Ownership(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(prefix='synthetic-attempt-ownership-');self.root=Path(self.tmp.name)
  self.audit=self.root/'audit';self.current={'authorization_id':'synthetic-current','session_id':'synthetic-session'}
  self.predecessors=['synthetic-r8','synthetic-r9','synthetic-r10']
  self.owner={'event':'invocation_reserved',**self.current,'controller_audit':str(self.audit),'intent_event_id':'synthetic-intent'}
  self.owner['reservation_id']='INVOCATION-RESERVATION-sha256:'+digest(self.owner)
 def tearDown(self):self.tmp.cleanup()
 def call(self,owner=None,scope=None):return attribute(owner,scope,self.predecessors,self.current,self.audit)
 def test_unowned_initial(self):self.assertIsNone(self.call()['current_ownership'])
 def test_exact_current_owner_is_attribution_not_handoff(self):
  result=self.call(self.owner);self.assertEqual(result['current_ownership'],self.owner);self.assertFalse(result['handoff_eligible'])
 def test_each_predecessor_owner_blocks(self):
  for predecessor in self.predecessors:
   with self.subTest(predecessor=predecessor),self.assertRaises(ValueError):self.call(dict(self.owner,authorization_id=predecessor))
 def test_unknown_owner_blocks(self):
  for owner in ({},dict(self.owner,authorization_id='unknown'),dict(self.owner,authorization_id=None)):
   with self.subTest(owner=owner),self.assertRaises(ValueError):self.call(owner)
 def test_competing_tuple_blocks(self):
  for field in ('session_id','controller_audit'):
   with self.subTest(field=field),self.assertRaises(ValueError):self.call(dict(self.owner,**{field:'wrong'}))
 def test_scope_attribution(self):
  scope={**self.current,'controller_audit':str(self.audit)}
  self.call(self.owner,scope)
  with self.assertRaises(ValueError):self.call(None,scope)
  with self.assertRaises(ValueError):self.call(self.owner,dict(scope,authorization_id=self.predecessors[-1]))
 def test_duplicate_or_self_ancestry(self):
  for predecessors in (self.predecessors*2,[self.current['authorization_id']]):
   with self.assertRaises(ValueError):attribute(None,None,predecessors,self.current,self.audit)
 def test_lifecycle_reservation_exact(self):
  life={'state':'ACTIVE','phase':'ACTIVE','activation_event':{'ownership_reservation':self.owner}}
  self.assertEqual(lifecycle_ownership(life,self.owner,None),'OWNERSHIP_HELD')
  for owner in (None,dict(self.owner,reservation_id='wrong')):
   with self.assertRaises(ValueError):lifecycle_ownership(life,owner,None)
 def test_wrong_lifecycle_blocks(self):
  for state in ('INACTIVE','CANCELLED','COMPLETED','REVOKED'):
   with self.subTest(state=state),self.assertRaises(ValueError):lifecycle_ownership({'state':state,'phase':state},self.owner,None)
 def test_intent_owned_remains_uncertain(self):
  self.assertEqual(lifecycle_ownership({'state':'INACTIVE','phase':'ACTIVATION_INDETERMINATE'},self.owner,None),'HELD_FOR_RECONCILIATION')
 def ledger(self,rows):
  p=self.root/'ledger';p.write_text(''.join(canonical(x)+'\n' for x in rows));return p
 def test_duplicate_reservations_rejected(self):
  with self.assertRaises(RuntimeError):observe(self.ledger([self.owner,self.owner]))
 def test_restart_owner_attribution_and_release(self):
  p=self.ledger([self.owner]);owner,scope,_=observe(p);self.assertEqual(owner,self.owner);self.call(owner,scope)
  with self.assertRaises(RuntimeError):observe(self.ledger([self.owner,{'event':'invocation_released','reservation_id':'wrong'}]))
  owner,scope,_=observe(self.ledger([self.owner,{'event':'invocation_released','reservation_id':self.owner['reservation_id']}]))
  self.assertIsNone(owner);self.assertIsNone(scope)
 def test_reservation_substitution_rejected(self):
  with self.assertRaises(RuntimeError):observe(self.ledger([dict(self.owner,authorization_id='wrong')]))

class Integrated(prior.Session):
 def test_actual_predecessor_chain_under_synthetic_current_activation_and_dispatch(self):
  from adapter.attempt_chain import ancestry
  from adapter import activation_transaction as at
  from adapter.orchestration_boundary import recover_then_dispatch
  proof=json.loads((O/'R10_AUTHENTICATED_CAPTURE.json').read_bytes())
  p=json.loads((O/'PROPOSED_R11_BINDING.json').read_bytes())
  # Actual immutable r8/r9/r10 evidence; ONLY current attempt/ledger belongs to
  # this explicitly non-E1 fixture. No real candidate reservation is written.
  proof['authorization']['ownership_ledger']=self.a.ownership_ledger
  p['invocation_identity']={'authorization_id':self.a.authorization_id,'session_id':self.a.session_id,'turn_id':self.a.turn_id}
  p['audit']=str(self.audit)
  validate=at._validate_production;captured=[];model_calls=[]
  def checked(*args,**kwargs):
   result=validate(*args,**kwargs);owner=ancestry(proof,p)
   captured.append(owner['current_ownership']);return result
  from adapter import operator_projection as op
  bootstrap=op.reconstruct_authorization
  def status_bootstrap(*args,**kwargs):
   auth=bootstrap(*args,**kwargs);ancestry(proof,p);return auth
  def response(runner,payload):
   self.assertNotEqual(runner.orchestrator.host.auth.work_package_id,'E1-WP-001')
   self.assertTrue(runner.orchestrator.host.activation_transaction.verify_handoff())
   model_calls.append(1)
   return {'id':'synthetic-chain-response','output':[]}
  with patch.object(at,'_validate_production',side_effect=checked),patch.object(op,'reconstruct_authorization',side_effect=status_bootstrap):
   self.activate()
   fixture_data=self.out/'synthetic-history.json'
   fixture_data.write_text(canonical({'proof':proof,'proposal':p,'store':{'root':str(self.store.root),'catalog_sha256':self.store.catalog_sha256,'applicability':self.store.applicability},'authorization_id':self.a.authorization_id}))
   code='''import sys,json
from pathlib import Path
sys.path.insert(0,sys.argv[1])
from unittest.mock import patch
from adapter.attempt_chain import ancestry
from adapter import activation_transaction as at
from adapter.controller_authority_store import ControllerAuthorityStore
from adapter.orchestration_boundary import recover_boundary
v=json.loads(Path(sys.argv[2]).read_bytes());s=ControllerAuthorityStore(**v['store']);original=at._validate_production

def checked(*args,**kwargs):
 result=original(*args,**kwargs);ancestry(v['proof'],v['proposal']);return result
with patch.object(at,'_host',return_value={'synthetic':'NON_LIVE'}),patch.object(at,'_validate_production',side_effect=checked):
 r=recover_boundary(s,v['authorization_id']);assert r['handoff_eligible'];assert r['ownership']['authorization_id']==v['authorization_id'];print(json.dumps(r))
s.close()
'''
   child=subprocess.run([sys.executable,'-B','-c',code,str(O/'candidate'),str(fixture_data)],capture_output=True,text=True,timeout=90)
   self.assertEqual(child.returncode,0,child.stderr)
   self.assertTrue(json.loads(child.stdout)['handoff_eligible'])
   active=project(self.store,self.a.authorization_id)
   self.assertEqual(active['lifecycle_state'],'ACTIVE');self.assertEqual(active['ownership'],'OWNERSHIP_HELD')
   with patch('adapter.responses_orchestrator.ResponsesReasoning._call',response):
    result=recover_then_dispatch(self.store,self.a.authorization_id)
   terminal=project(self.store,self.a.authorization_id)
  self.assertEqual(len(model_calls),1);self.assertEqual(result['status'],'INCOMPLETE')
  self.assertEqual(terminal['lifecycle_state'],'CANCELLED');self.assertEqual(terminal['ownership'],'RELEASED')
  self.assertTrue(any(x is not None for x in captured));self.assertTrue(any(x is None for x in captured))
 def test_stale_active_projection_is_unknown(self):
  self.activate()
  with patch('adapter.operator_projection.status',return_value={'freshness':'UNKNOWN','terminal_disposition':{'disposition':'INDETERMINATE'}}):
   v=project(self.store,self.a.authorization_id)
   self.assertEqual(v['lifecycle_state'],'ACTIVE');self.assertEqual(v['ownership'],'OWNERSHIP_HELD')
   self.assertEqual(v['authority_freshness'],'FRESH');self.assertEqual(v['activity_freshness'],'UNKNOWN')
   self.assertEqual(v['current_subphase'],'UNKNOWN');self.assertFalse(v['handoff_eligible'])
 def test_live_all_phases_with_exact_ownership(self):
  snapshots=[]
  with self.store.session():issue_inactive(self.a,self.audit,self.dr)
  v=project(self.store,self.a.authorization_id);snapshots.append(v)
  self.assertEqual(v['lifecycle_state'],'INACTIVE');self.assertEqual(v['ownership'],'NONE')
  with self.store.session():c=start_control(self.a,self.audit,E1_POLICY)
  from adapter import activation_transaction as at
  append=at._append
  def stop_after_intent(fd,row):
   append(fd,row)
   if row['event']=='authorization_lifecycle_activation_intent':raise RuntimeError('synthetic crash at durable intent')
  with self.store.session(),patch.object(at,'_append',side_effect=stop_after_intent):
   with self.assertRaises(RuntimeError):ActivationTransaction.activate(self.a,self.audit,self.did)
  v=project(self.store,self.a.authorization_id);snapshots.append(v)
  self.assertEqual(v['operational_state'],'ACTIVATING');self.assertFalse(v['handoff_eligible'])
  # Do not replay a partial activation. A separate fixture tests ACTIVE→dispatch.
  print('INTENT_STATUS '+canonical(snapshots),flush=True)
 def test_dispatching_projection_from_authoritative_ACTIVE(self):
  c=self.activate()
  with c.span('reasoning_construction'):
   v=project(self.store,self.a.authorization_id)
   self.assertEqual(v['lifecycle_state'],'ACTIVE');self.assertEqual(v['operational_state'],'DISPATCHING')
   self.assertEqual(v['ownership'],'OWNERSHIP_HELD');self.assertFalse(v['handoff_eligible'])
   print('ACTIVE_STATUS '+canonical(v),flush=True)
 def test_ownership_gating_survives_restart_and_cancellation(self):
  self.activate()
  from adapter.orchestration_boundary import recover_boundary
  result=recover_boundary(self.store,self.a.authorization_id)
  self.assertTrue(result['handoff_eligible']);self.assertEqual(result['ownership']['authorization_id'],self.a.authorization_id)
  with self.store.session():
   tx=ActivationTransaction.recover(self.a,self.audit,self.did)
   host=GovernedHost(tx.auth,self.audit);host.revoke();tx.cancel(host,'synthetic stop');tx.close()
  v=project(self.store,self.a.authorization_id)
  self.assertEqual((v['lifecycle_state'],v['ownership'],v['architectural_state']),('CANCELLED','RELEASED','QUIESCENT'))

if __name__=='__main__':unittest.main(verbosity=2)
