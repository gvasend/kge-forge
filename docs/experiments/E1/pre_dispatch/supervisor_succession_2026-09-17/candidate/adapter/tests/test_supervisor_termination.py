import json, pathlib, signal, tempfile, unittest
from unittest.mock import patch
from adapter.host_supervisor import HostScopeSupervisor, SupervisorError
from adapter.supervisor_server import recovery_request
from adapter.launch_broker import BrokerProtocol
from adapter.termination import PidfdSignaler, TerminationError

SID='scope-'+'a'*32
OWNER=('session','authorization','action')
RID='recovery-'+'1'*32

class FakeSignaler:
    def __init__(self,clear=None): self.calls=[]; self.clear=clear
    def signal(self,pid,signum,scope_cgroup):
        self.calls.append((pid,signum,scope_cgroup))
        if self.clear: self.clear(pid,signum)
        return 'DELIVERED'

class TerminationTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.root=pathlib.Path(self.temp.name)
        self.base=self.root/'executor'; self.base.mkdir()
        (self.base/'cgroup.procs').write_text('')
        self.audit=self.root/'supervisor.jsonl'
        self.fake=FakeSignaler()
        self.sup=HostScopeSupervisor(self.base,self.audit,self.fake,
            termination_seconds=.4,grace_seconds=.12,poll_seconds=.01)
        self.sup.create(SID,OWNER)
        self.path=self.base/SID
        self.members([101],1)
    def tearDown(self): self.temp.cleanup()
    def members(self,pids,populated):
        (self.path/'cgroup.procs').write_text('\n'.join(str(pid) for pid in pids))
        (self.path/'cgroup.events').write_text('populated %s\nfrozen 0\n'%populated)
    def events(self): return [json.loads(line) for line in self.audit.read_text().splitlines()]
    def request(self,rid=RID,**changes):
        req={'protocol_version':1,'broker_request_id':'action:1:terminate_reconcile',
            'session_id':OWNER[0],'authorization_id':OWNER[1],
            'action_request_id':OWNER[2],'execution_scope_id':SID,'scope_id':SID,
            'op':'terminate_reconcile','recovery_request_id':rid}
        req.update(changes); return req
    def test_valid_termination_is_scope_selected_and_reconciled(self):
        self.fake.clear=lambda _pid,_sig:self.members([],0)
        result=recovery_request(self.sup,self.request())
        self.assertEqual(result['result'],'QUIESCENT')
        self.assertEqual(result['final_observation']['members'],[])
        self.assertEqual(self.sup.state(SID),'QUIESCENT')
        self.assertEqual(self.fake.calls[0],(101,signal.SIGTERM,
            '/kge-forge/executor/'+SID))
        events=self.events()
        names=[event['event'] for event in events]
        self.assertLess(names.index('recovery_authorized'),names.index('termination_intent'))
        self.assertLess(names.index('termination_action'),names.index('recovery_final'))
        self.assertEqual(events[-1]['result'],'QUIESCENT')
        self.assertEqual(events[-1]['final_observation']['populated'],0)
    def test_mismatched_identity_scope_substitution_and_generic_pid_denied(self):
        for change in ({'authorization_id':'other'},
                       {'execution_scope_id':'scope-'+'b'*32},
                       {'scope_id':'scope-'+'b'*32},
                       {'pid':101},{'cgroup':'/other'}):
            with self.assertRaises(SupervisorError):
                recovery_request(self.sup,self.request(**change))
        self.assertEqual(self.fake.calls,[])
        self.assertFalse(any(event['event']=='recovery_authorized' for event in self.events()))
        self.assertEqual(sum(event['event']=='recovery_denied' for event in self.events()),5)
        with self.assertRaises(SupervisorError):
            self.sup.create(str(self.root/'outside'))
        self.assertFalse((self.root/'outside').exists())
    def test_replayed_request_and_restart_adoption_do_not_reopen_admission(self):
        self.fake.clear=lambda _pid,_sig:self.members([],0)
        self.assertEqual(recovery_request(self.sup,self.request())['result'],'QUIESCENT')
        with self.assertRaises(SupervisorError): recovery_request(self.sup,self.request())
        restored=HostScopeSupervisor(self.base,self.audit,FakeSignaler(),
            termination_seconds=.4,grace_seconds=.12,poll_seconds=.01)
        self.assertEqual(restored.state(SID),'INDETERMINATE')
        with self.assertRaises(SupervisorError): restored.admit(SID,999)
        with self.assertRaises(SupervisorError): recovery_request(restored,self.request())
        fresh=self.request('recovery-'+'2'*32)
        self.assertEqual(recovery_request(restored,fresh)['result'],'QUIESCENT')
    def test_restart_adopts_active_members_for_closed_reconciliation(self):
        restored_fake=FakeSignaler(lambda _pid,_sig:self.members([],0))
        restored=HostScopeSupervisor(self.base,self.audit,restored_fake,
            termination_seconds=.4,grace_seconds=.12,poll_seconds=.01)
        self.assertEqual(restored.state(SID),'INDETERMINATE')
        with self.assertRaises(SupervisorError): restored.admit(SID,999)
        result=recovery_request(restored,self.request('recovery-'+'4'*32))
        self.assertEqual(result['result'],'QUIESCENT')
        self.assertEqual(result['initial_observation']['members'],[101])
        self.assertEqual(restored_fake.calls[0][0],101)
    def test_already_quiescent_requires_fresh_kernel_observation(self):
        self.members([],0); self.sup.close(SID)
        self.assertTrue(self.sup.quiescent(SID))
        result=recovery_request(self.sup,self.request())
        self.assertEqual(result['result'],'QUIESCENT')
        self.assertEqual(result['termination_action_count'],0)
        self.assertEqual(self.fake.calls,[])
    def test_post_quiescent_population_is_identity_uncertain(self):
        self.members([],0); self.sup.close(SID); self.assertTrue(self.sup.quiescent(SID))
        self.members([101],1)
        result=recovery_request(self.sup,self.request())
        self.assertEqual(result['result'],'INDETERMINATE')
        self.assertIn('post-quiescent',result['reason'])
        self.assertEqual(self.fake.calls,[])
    def test_descendant_cgroup_member_is_attributable_to_scope(self):
        child=self.path/'child'; child.mkdir()
        (child/'cgroup.procs').write_text('202')
        self.members([],1)
        self.fake.clear=lambda _pid,_sig:((child/'cgroup.procs').write_text(''),
                                      self.members([],0))
        result=recovery_request(self.sup,self.request())
        self.assertEqual(result['result'],'QUIESCENT')
        self.assertEqual(self.fake.calls[0][0],202)
        self.assertEqual(result['initial_observation']['directories'],2)
    def test_surviving_member_reports_indeterminate_and_blocks_admission(self):
        self.sup.termination.window=1
        self.sup.termination.grace=.05
        result=recovery_request(self.sup,self.request())
        self.assertEqual(result['result'],'INDETERMINATE')
        self.assertEqual(result['final_observation']['populated'],1)
        self.assertIn('surviving',result['reason'])
        self.assertEqual(self.sup.state(SID),'INDETERMINATE')
        self.assertTrue(any(sig==signal.SIGKILL for _,sig,_ in self.fake.calls))
        with self.assertRaises(SupervisorError): self.sup.admit(SID,202)
    def test_observation_failure_is_indeterminate_without_signal(self):
        (self.path/'cgroup.events').unlink()
        result=recovery_request(self.sup,self.request())
        self.assertEqual(result['result'],'INDETERMINATE')
        self.assertIn('observation failed',result['reason'])
        self.assertEqual(self.fake.calls,[])
        self.assertEqual(self.events()[-1]['result'],'INDETERMINATE')
    def test_disappearance_or_signal_delivery_is_not_quiescence(self):
        class Disappeared(FakeSignaler):
            def signal(self,pid,signum,scope_cgroup):
                self.calls.append((pid,signum,scope_cgroup)); return 'DISAPPEARED'
        self.sup.termination.signaler=Disappeared()
        first=recovery_request(self.sup,self.request())
        self.assertEqual(first['result'],'INDETERMINATE')
        self.members([],0)
        second=recovery_request(self.sup,self.request('recovery-'+'3'*32))
        self.assertEqual(second['result'],'QUIESCENT')
        self.assertEqual(second['termination_action_count'],0)
    def test_broker_rejects_replayed_or_unbound_recovery(self):
        protocol=BrokerProtocol(*OWNER[:2],SID,OWNER[2])
        req=self.request()
        self.assertTrue(protocol.validate(req))
        with self.assertRaises(ValueError): protocol.validate(req)
        protocol=BrokerProtocol(*OWNER[:2],SID,OWNER[2])
        with self.assertRaises(ValueError): protocol.validate(self.request(session_id='other'))
    def test_pidfd_member_check_prevents_outside_scope_signal(self):
        signaler=PidfdSignaler()
        with patch.object(signaler,'_open',return_value=7), \
             patch.object(signaler,'_send') as delivered, \
             patch('adapter.termination.Path.read_text',return_value='0::/outside\n'), \
             patch('adapter.termination.os.close'):
            with self.assertRaises(TerminationError):
                signaler.signal(101,signal.SIGTERM,'/kge-forge/executor/'+SID)
            delivered.assert_not_called()

if __name__=='__main__': unittest.main()
