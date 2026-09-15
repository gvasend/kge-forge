import io, json, pathlib, tempfile, threading, time, unittest
from unittest.mock import patch

from adapter import exec_barrier
from adapter.forward_bridge import BridgeError
from adapter.governed_host import Denied, GovernedHost, WorkAuthorization
from adapter.orchestrator import ReasoningOrchestrator, action
from adapter.responses_orchestrator import ResponsesReasoning, tool_definitions


class FakeSupervisorBridge:
    def __init__(self, owner, session, authorization, scope, action_id, root):
        self.owner=owner; self.scope=scope; self.action_id=action_id
        self.owner.bindings.append((session,authorization,scope,action_id,str(root)))
    def exchange(self, op, **fields):
        self.owner.calls.append((self.scope,self.action_id,op,fields))
        if self.owner.loss: raise BridgeError('socket lost')
        if op=='create': return {'scope_id':self.scope}
        if op=='production_spawn':
            self.owner.result_available.set()
            return {'scope_id':self.scope,'action_request_id':self.action_id,
                    'admitted':True,'launcher_pid':411,'initial_cgroup':
                    '0::/kge-forge/executor/'+self.scope,'result':'known-result'}
        if op=='close': return {'state':'CLOSED'}
        if op=='quiescent':
            return {'quiescent':self.owner.release.is_set(),
                    'state':'QUIESCENT' if self.owner.release.is_set() else 'DRAINING'}
        if op=='production_status': return {'returncode':0}
        raise AssertionError(op)


class BridgeFactory:
    def __init__(self):
        self.calls=[]; self.bindings=[]; self.release=threading.Event()
        self.result_available=threading.Event(); self.loss=False
    def __call__(self, session, authorization, scope, action_id, root):
        return FakeSupervisorBridge(self,session,authorization,scope,action_id,root)


class ProductionExecTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.root=pathlib.Path(self.temp.name)
        authorization=WorkAuthorization('auth-prod',1,'scratch','session','turn',
                                        (str(self.root),),(str(self.root),),(),('python3',),False,False)
        self.audit_temp=tempfile.TemporaryDirectory(); self.audit=pathlib.Path(self.audit_temp.name)/'audit.jsonl'
        self.host=GovernedHost(authorization,self.audit)
        self.orchestrator=ReasoningOrchestrator(self.host)
        self.bridge=BridgeFactory()
        self.patch=patch('adapter.governed_host.ForwardBridge',self.bridge); self.patch.start()
    def tearDown(self):
        self.bridge.release.set(); self.patch.stop(); self.temp.cleanup(); self.audit_temp.cleanup()
    def request(self, rid='req-1', **extra):
        return self.orchestrator.request(action(action_request_id=rid,type='exec',
            session_id='session',turn_id='turn',authorization_id='auth-prod',
            authorization_revision=1,executable='python3',argv=['-c','print(1)'],
            cwd=str(self.root),**extra))

    def test_model_facing_schema_and_mapping(self):
        schema={tool['name']:tool for tool in tool_definitions()}['governed_exec']
        self.assertEqual(set(schema['parameters']['properties']),{'executable','argv','cwd','inputs'})
        self.assertEqual(set(schema['parameters']['required']),{'executable','argv','cwd','inputs'})
        self.assertNotIn('execution_scope_id',schema['parameters']['properties'])
        self.bridge.release.set()
        class FakeResponses(ResponsesReasoning):
            def __init__(self, orchestrator): super().__init__(orchestrator); self.calls=0
            def _call(self, _payload):
                self.calls+=1
                if self.calls==1:
                    return {'id':'response-1','output':[{'type':'function_call',
                        'name':'governed_exec','call_id':'model-call-1',
                        'arguments':json.dumps({'executable':'python3','argv':['-c','print(1)'],
                                                'cwd':str(root),'inputs':[]})}]}
                return {'id':'response-2','output':[]}
        root=self.root
        runner=FakeResponses(self.orchestrator)
        self.assertEqual(runner.run('scratch execution',{},max_cycles=2)['status'],'INCOMPLETE')
        self.assertEqual(self.orchestrator.results['model-call-1']['result'],'SUCCEEDED')

    def test_identity_supervisor_path_replay_and_terminal_result(self):
        self.bridge.release.set()
        first=self.request()
        self.assertEqual(first['result'],'SUCCEEDED')
        sid=first['data']['execution_scope_id']
        self.assertEqual(first['data']['action_request_id'],'req-1')
        self.assertEqual([c[2] for c in self.bridge.calls],
                         ['create','production_spawn','close','quiescent','production_status'])
        self.assertTrue(all(c[0]==sid and c[1]=='req-1' for c in self.bridge.calls))
        self.assertEqual(self.bridge.calls[1][3]['argv'],['python3','-c','print(1)'])
        self.assertEqual(self.request(),first)
        self.assertEqual(len(self.bridge.bindings),1)
        audit=self.audit.read_text()
        self.assertIn('execution_scope_quiescent',audit)
        self.assertIn('"execution_scope_id": "'+sid+'"',audit)
        self.assertIn('"action_request_id": "req-1"',audit)

    def test_mismatched_scope_and_direct_legacy_are_denied(self):
        self.assertEqual(self.request(execution_scope_id='wrong')['result'],'DENIED')
        self.assertEqual(self.request('req-scope',scope_id='wrong')['result'],'DENIED')
        self.assertEqual(self.bridge.calls,[])
        with self.assertRaises(Denied):
            self.host.governed_exec(('python3','-c','print(1)'),self.root)
        from adapter.governed_host import Scope
        with self.assertRaises(Denied):
            Scope('scope-legacy',self.root,'req-legacy').launch(['python3'],self.root)
        raw=action(action_request_id='req-bwrap',type='exec',session_id='session',
                   turn_id='turn',authorization_id='auth-prod',authorization_revision=1,
                   executable='/usr/bin/bwrap',argv=[],cwd=str(self.root))
        self.assertEqual(self.orchestrator.request(raw)['result'],'DENIED')

    def test_result_before_quiescence_blocks_second_action(self):
        first=[]
        thread=threading.Thread(target=lambda:first.append(self.request()),daemon=True)
        thread.start(); self.assertTrue(self.bridge.result_available.wait(2))
        time.sleep(.08)
        self.assertTrue(thread.is_alive())
        self.assertNotIn('req-1',self.orchestrator.results)
        self.assertEqual(self.request('req-2')['result'],'DENIED')
        self.assertEqual(len([c for c in self.bridge.calls if c[2]=='production_spawn']),1)
        self.bridge.release.set(); thread.join(2)
        self.assertEqual(first[0]['result'],'SUCCEEDED')
        self.assertEqual(self.request('req-3')['result'],'SUCCEEDED')
        self.assertEqual(len([c for c in self.bridge.calls if c[2]=='production_spawn']),2)

    def test_supervisor_loss_is_indeterminate_and_fail_closed(self):
        self.bridge.loss=True
        first=self.request()
        self.assertEqual(first['result'],'INDETERMINATE')
        self.assertEqual(self.host.scope.state,'INDETERMINATE')
        self.assertEqual(self.request('req-2')['result'],'DENIED')
        self.assertNotIn('execution_scope_quiescent',self.audit.read_text())

    def test_start_barrier_prevents_payload_before_release(self):
        class Stdin: buffer=io.BytesIO(b'')
        with patch.object(exec_barrier.sys,'stdin',Stdin), patch.object(exec_barrier.os,'execve') as launch:
            self.assertEqual(exec_barrier.run(str(self.root),['python3','-c','print(1)']),2)
            launch.assert_not_called()
        class Released: buffer=io.BytesIO(b'1')
        with patch.object(exec_barrier.sys,'stdin',Released), patch.object(exec_barrier.os,'execve') as launch:
            exec_barrier.run(str(self.root),['python3','-c','print(1)'])
            self.assertEqual(launch.call_args.args[0],'/usr/bin/bwrap')
            self.assertIn('--die-with-parent',launch.call_args.args[1])
            self.assertIn('--unshare-pid',launch.call_args.args[1])
            self.assertEqual(set(launch.call_args.args[2]),{'PATH','LANG'})


if __name__=='__main__': unittest.main()
