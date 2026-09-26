from qualify_session import *
from contextlib import contextmanager
class Restart(Session):
 def test_restart_boundary_to_model_and_terminal_projection(self):
  self.activate();recover_boundary(self.store,self.a.authorization_id)
  spec={'root':str(self.store.root),'catalog_sha256':self.store.catalog_sha256,'applicability':self.store.applicability}
  code='''import sys,json
from unittest.mock import patch
from adapter.controller_authority_store import ControllerAuthorityStore,current
from adapter.orchestration_boundary import recover_then_dispatch
from adapter.operator_projection import project
s=ControllerAuthorityStore(**json.loads(sys.argv[1]));a=sys.argv[2];calls=[]
def model(r,p):
 assert current() is s and r.orchestrator.host.activation_transaction.verify_handoff()
 calls.append(1);return {'id':'synthetic','output':[]}
with patch('adapter.activation_transaction._host',return_value={'synthetic':'NON_LIVE'}),patch('adapter.responses_orchestrator.ResponsesReasoning._call',model):
 r=recover_then_dispatch(s,a)
assert calls==[1] and r['status']=='INCOMPLETE' and current() is None
v=project(s,a);assert v['lifecycle_state']=='CANCELLED' and v['ownership']=='RELEASED'
print(json.dumps(v));s.close()
'''
  p=subprocess.run([sys.executable,'-c',code,canonical(spec),self.a.authorization_id],capture_output=True,text=True,timeout=90)
  self.assertEqual(p.returncode,0,p.stderr);v=json.loads(p.stdout);self.assertLess(v['projection_seconds'],30)
 def test_cancellation_at_major_pre_model_phases(self):
  from adapter.run_control import RunControl
  original=RunControl.span
  for phase in ('private_bootstrap','activation_recovery','host_construction','reasoning_construction'):
   with self.subTest(phase=phase):
    # Each phase has a unique synthetic fixture/namespace, never an E1 attempt.
    case=Session();case.setUp()
    try:
     case.activate()
     @contextmanager
     def interrupted(c,name):
      with original(c,name):
       if name==phase:raise RuntimeError('synthetic interruption at '+phase)
       yield
     from adapter.controlled_dispatch import dispatch
     with patch.object(RunControl,'span',interrupted),patch('adapter.responses_orchestrator.ResponsesReasoning._call') as m:
      with self.assertRaises(RuntimeError):dispatch(case.store,case.a.authorization_id)
      m.assert_not_called()
     self.assertIsNone(current())
     # Typed cancellation reconciles any ownership left before host construction.
     with case.store.session():
      t=ActivationTransaction(case.a,case.audit,case.did)
      try:
       from adapter.authorization_lifecycle import reconstruct
       state=reconstruct(case.audit.read_bytes(),case.a,case.audit)
       if state['state']=='ACTIVE':
        op=json.loads(case.a.operational_binding);op['dispatch_authorization']=case.dr
        h=GovernedHost(replace(case.a,state='ACTIVE',operational_binding=canonical(op)),case.audit)
        h.revoke();t.cancel(h,'synthetic operator reconciliation')
       else:self.assertEqual(state['state'],'CANCELLED')
      finally:t.close()
     v=project(case.store,case.a.authorization_id)
     self.assertEqual(v['lifecycle_state'],'CANCELLED');self.assertEqual(v['ownership'],'RELEASED');self.assertLess(v['projection_seconds'],30)
     with patch('adapter.operator_projection.status',return_value={'freshness':'UNKNOWN','terminal_disposition':None}):
      self.assertEqual(project(case.store,case.a.authorization_id)['lifecycle_state'],'CANCELLED')
     self.assertEqual(project(case.store,case.a.authorization_id,max_seconds=0)['freshness'],'UNKNOWN')
    finally:case.tearDown()
if __name__=='__main__':unittest.main(verbosity=2)
