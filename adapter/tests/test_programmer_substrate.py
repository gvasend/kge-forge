import json, pathlib, tempfile, unittest
from adapter.governed_host import GovernedHost, WorkAuthorization
from adapter.orchestrator import ReasoningOrchestrator
from adapter.responses_orchestrator import ResponsesReasoning, tool_definitions

class ProgrammerSubstrateTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.root=pathlib.Path(self.temp.name)
        self.auth=WorkAuthorization('auth',1,'scratch','session','turn',
                                    (str(self.root),),(str(self.root),),(),('python3',))
        self.audit_temp=tempfile.TemporaryDirectory(); self.audit=pathlib.Path(self.audit_temp.name)/'audit.jsonl'
        self.host=GovernedHost(self.auth,self.audit)
        self.orch=ReasoningOrchestrator(self.host)
    def tearDown(self): self.temp.cleanup(); self.audit_temp.cleanup()
    def test_registry_rejects_unregistered_execution_and_scope_injection(self):
        runner=ResponsesReasoning(self.orch)
        for name in ('shell','exec_command','python','subprocess','bwrap','mcp_exec'):
            result=runner._dispatch({'name':name,'call_id':'deny-'+name,
                                      'arguments':json.dumps({'command':'touch marker'})})
            self.assertEqual(result['result'],'DENIED')
        result=runner._dispatch({'name':'governed_exec','call_id':'deny-scope',
            'arguments':json.dumps({'executable':'python3','argv':['-c','print(1)'],
                                    'cwd':str(self.root),'inputs':[],
                                    'execution_scope_id':'caller'})})
        self.assertEqual(result['result'],'DENIED')
        self.assertIsNone(self.host.scope)
        root_request=runner._dispatch({'name':'governed_exec','call_id':'deny-root',
            'arguments':json.dumps({'executable':'python3','argv':['-c','print(1)'],
                                    'cwd':str(self.root),'inputs':['.']})})
        self.assertEqual(root_request['result'],'DENIED')
        self.assertIsNone(self.host.scope)
        self.assertEqual([x['name'] for x in tool_definitions() if x['name']=='governed_exec'],
                         ['governed_exec'])
    def test_stateless_continuation_requires_authorized_finish(self):
        class Fixture(ResponsesReasoning):
            def __init__(self,orch): super().__init__(orch); self.payloads=[]
            def _call(self,payload):
                self.payloads.append(payload)
                n=len(self.payloads)
                if n==1: return {'id':'r1','output':[{'type':'function_call',
                    'name':'governed_status','call_id':'status-1','arguments':'{}'}]}
                if n==2: return {'id':'r2','output':[{'type':'function_call',
                    'name':'finish_task','call_id':'finish-1',
                    'arguments':'{"summary":"scratch done"}'}]}
                return {'id':'r3','output':[{'type':'message','content':[]}]}
        runner=Fixture(self.orch)
        result=runner.run('scratch',{},3)
        self.assertEqual(result['status'],'COMPLETE')
        self.assertTrue(all(p['store'] is False and p['parallel_tool_calls'] is False
                            for p in runner.payloads))
        self.assertEqual([t['name'] for t in runner.payloads[0]['tools']],
                         [t['name'] for t in tool_definitions()])
        self.assertTrue(any(x.get('type')=='function_call_output' for x in
                            runner.payloads[1]['input']))
        self.assertEqual(self.orch.results['finish-1']['result'],'SUCCEEDED')
    def test_list_search_are_bounded_by_read_grant(self):
        (self.root/'src').mkdir()
        (self.root/'src'/'module.py').write_text('needle = 1\n')
        listed=self.host.governed_list(str(self.root),'src',10)
        self.assertEqual([x['name'] for x in listed['entries']],['module.py'])
        searched=self.host.governed_search(str(self.root),'src','needle',10)
        self.assertEqual(len(searched['matches']),1)
        from adapter.governed_host import Denied
        with self.assertRaises(Denied): self.host.governed_list(str(self.root),'../',10)
        with self.assertRaises(Denied): self.host.governed_search(str(self.root),'src','needle',101)
    def test_effective_profile_protects_evidence_and_denies_self_expansion(self):
        runner=ResponsesReasoning(self.orch)
        def call(name,rid,args):
            return runner._dispatch({'name':name,'call_id':rid,
                                     'arguments':json.dumps(args)})
        original=self.audit.read_bytes()
        for index,(name,args) in enumerate((
            ('governed_read',{'repository':str(self.root),'path':str(self.audit),'limit':100}),
            ('governed_write',{'repository':str(self.root),'path':str(self.audit),'content':'tamper'}),
            ('governed_write',{'repository':str(self.root),'path':'../outside','content':'tamper'}))):
            self.assertEqual(call(name,'deny-'+str(index),args)['result'],'DENIED')
        self.assertIn(original,self.audit.read_bytes())
        from adapter.governed_host import Denied
        with self.assertRaises(Denied):
            GovernedHost(self.auth,self.root/'audit.jsonl')
        expansion=call('authority_expansion_request','expansion',{
            'capability':'shell','action':'run','resources':['/bin/sh'],
            'reason':'scratch request'})
        self.assertEqual(expansion['data']['decision'],'PENDING')
        self.assertEqual(self.auth.exec_bins,('python3',))
        self.assertIsNone(self.host.scope)
    def test_execution_snapshot_omits_protected_source_and_has_no_promotion(self):
        (self.root/'src').mkdir()
        (self.root/'src'/'allowed.txt').write_text('ALLOWED')
        protected=self.root/'src'/'protected.txt'; protected.write_text('UNCHANGED')
        profile=WorkAuthorization('protected',1,'scratch','s','t',(str(self.root),),
                                  (), (str(protected),),('python3',))
        host=GovernedHost(profile,pathlib.Path(self.audit_temp.name)/'protected.jsonl')
        from unittest.mock import patch
        class Bridge:
            def __init__(self,session,authorization,scope,action,root):
                self.scope=scope; self.action=action; self.root=pathlib.Path(root)
                (self.root/'src'/'protected.txt').write_text('SNAPSHOT_ONLY')
            def exchange(self,op,**fields):
                return {'create':{'scope_id':self.scope},
                  'production_spawn':{'scope_id':self.scope,'action_request_id':self.action,
                    'admitted':True,'launcher_pid':1,'initial_cgroup':'0::/kge-forge/executor/'+self.scope,
                    'result':'SNAPSHOT_ONLY'},'close':{'state':'CLOSED'},
                  'quiescent':{'quiescent':True,'state':'QUIESCENT'},
                  'production_status':{'returncode':0}}[op]
        runner=ResponsesReasoning(ReasoningOrchestrator(host))
        with patch('adapter.governed_host.ForwardBridge',Bridge):
            result=runner._dispatch({'name':'governed_exec','call_id':'snapshot',
              'arguments':json.dumps({'executable':'python3','argv':['-c','print(1)'],
                'cwd':str(self.root),'inputs':['src']})})
        self.assertEqual(result['result'],'SUCCEEDED')
        self.assertNotEqual(host.scope.root,self.root)
        self.assertNotIn('src/protected.txt',host.scope.snapshot['files'])
        self.assertEqual(protected.read_text(),'UNCHANGED')
    def test_explicit_snapshot_inputs_reject_protected_and_symlink_paths(self):
        (self.root/'allowed.py').write_text('print(1)\n')
        (self.root/'protected.py').write_text('secret\n')
        (self.root/'linked.py').symlink_to(self.root/'allowed.py')
        from adapter.execution_snapshot import construct, observe, SnapshotDenied
        def authorize(rel):
            if rel=='protected.py': raise ValueError('protected')
            return self.root/rel
        with self.assertRaises(SnapshotDenied):
            construct(self.root,['protected.py'],authorize,self.audit_temp.name,'scope-protected')
        with self.assertRaises(SnapshotDenied):
            construct(self.root,['linked.py'],authorize,self.audit_temp.name,'scope-linked')
        workspace,manifest,_=construct(self.root,['allowed.py'],authorize,
                                       self.audit_temp.name,'scope-allowed')
        self.assertEqual((workspace/'allowed.py').read_text(),'print(1)\n')
        self.assertEqual(manifest['files']['allowed.py']['sha256'],
                         __import__('hashlib').sha256(b'print(1)\n').hexdigest())
        (workspace/'allowed.py').write_text('changed only in snapshot')
        self.assertEqual((self.root/'allowed.py').read_text(),'print(1)\n')
        self.assertIn('allowed.py',observe(workspace,manifest)['changed'])
        (self.root/'allowed.py').write_text('authoritative drift')
        with self.assertRaises(SnapshotDenied): observe(workspace,manifest)

if __name__=='__main__': unittest.main()
