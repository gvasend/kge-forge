import hashlib, json, pathlib, subprocess, tempfile, unittest
from adapter.context_binding import CommittedContext, ContextDenied
from adapter.authority_profile import programmer_authorization
from adapter.governed_host import GovernedHost, WorkAuthorization
from adapter.orchestrator import ReasoningOrchestrator, action
from adapter.responses_orchestrator import ResponsesReasoning

class CommittedContextTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.root=pathlib.Path(self.temp.name)
        self.audit=tempfile.TemporaryDirectory()
        def git(*args):
            return subprocess.check_output(['/usr/bin/git','-C',str(self.root),
                '-c','core.hooksPath=/dev/null',*args],stderr=subprocess.DEVNULL,
                text=True).strip()
        git('init','-q')
        (self.root/'package.txt').write_text('DECIDED bounded task\n')
        (self.root/'code.py').write_text('print(1)\n')
        digest=hashlib.sha256((self.root/'package.txt').read_bytes()).hexdigest()
        manifest={'schema_version':'E1-CONTEXT-1','baseline_id':'scratch-baseline',
            'work_id':'scratch-work','status':'DIAGNOSTIC_AUTHORIZED',
            'repositories':{'forge':{'root':str(self.root)}},
            'sources':[{'id':'package','repository':'forge','path':'package.txt',
                'sha256':digest,'revision_binding':'package_capture_commit',
                'knowledge_status':'DECIDED','dependencies':[]}],
            'mandatory_roots':['package'],'scope':{'read_roots':[str(self.root)],
                'writable_paths':['code.py'],'protected_paths':['package.txt'],
                'task_tool_network':'DENIED','unrelated_connectors':'DENIED'},
            'prerequisites':[]}
        self.manifest=self.root/'CONTEXT_MANIFEST.json'
        self.manifest.write_text(json.dumps(manifest))
        git('add','package.txt','CONTEXT_MANIFEST.json')
        git('-c','user.name=Scratch','-c','user.email=scratch@example.invalid',
            'commit','-qm','capture')
        self.commit=git('rev-parse','HEAD')
        self.binding=CommittedContext(self.manifest,self.commit)
        self.auth=programmer_authorization(self.binding,'auth',1,'s','t',
            exec_argv_allowlist=(('python3','code.py'),),diagnostic=True)
        self.host=GovernedHost(self.auth,pathlib.Path(self.audit.name)/'audit.jsonl')
        self.orch=ReasoningOrchestrator(self.host)
    def tearDown(self): self.temp.cleanup(); self.audit.cleanup()
    def request(self,typ,rid,**fields):
        return self.orch.request(action(type=typ,action_request_id=rid,session_id='s',
            turn_id='t',authorization_id='auth',authorization_revision=1,**fields))
    def test_captured_context_bound_to_agent_and_protected(self):
        self.assertTrue(self.binding.verify())
        self.assertEqual(self.request('read','read-package',repository=str(self.root),
            path='package.txt')['result'],'SUCCEEDED')
        self.assertEqual(self.request('read','deny-git',repository=str(self.root),
            path='.git/config')['result'],'DENIED')
        self.assertEqual(self.request('exec','deny-unattributed',executable='python3',
            argv=['code.py'],cwd=str(self.root),inputs=['code.py'])['result'],'DENIED')
        self.assertIsNone(self.host.scope)
        self.assertEqual(self.request('read','read-code',repository=str(self.root),
            path='code.py')['result'],'SUCCEEDED')
        self.assertEqual(self.request('write','deny-package',repository=str(self.root),
            path='package.txt',content='alter')['result'],'DENIED')
        self.assertEqual(self.request('write','write-code',repository=str(self.root),
            path='code.py',content='print(2)\n')['result'],'SUCCEEDED')
        events=[json.loads(line) for line in self.host.audit.read_text().splitlines()]
        intent=next(i for i,event in enumerate(events) if event.get('event')=='action_request'
                    and event.get('action_request_id')=='write-code')
        result=next(i for i,event in enumerate(events) if event.get('event')=='action_result'
                    and event.get('action_request_id')=='write-code')
        self.assertLess(intent,result)
        self.assertEqual(events[intent]['capture_commit'],self.commit)
        self.assertEqual(self.host.audit.stat().st_mode & 0o777,0o600)
        self.assertEqual(self.request('exec','deny-command',executable='python3',
            argv=['-c','print(3)'],cwd=str(self.root),inputs=['code.py'])['result'],'DENIED')
        self.assertIsNone(self.host.scope)
        runner=ResponsesReasoning(self.orch)
        with self.assertRaises(ValueError): runner.run('scratch',{'work_id':'forged'},0)
    def test_stale_or_contradictory_source_denies_next_action(self):
        (self.root/'package.txt').write_text('changed\n')
        self.assertEqual(self.request('write','stale-write',repository=str(self.root),
            path='code.py',content='effect')['result'],'DENIED')
        self.assertEqual((self.root/'code.py').read_text(),'print(1)\n')
        with self.assertRaises(ContextDenied): self.binding.verify()
        (self.root/'package.txt').write_text('DECIDED bounded task\n')
        self.manifest.write_text('{}')
        self.assertEqual(self.request('exec','stale-exec',executable='python3',argv=['-c','print(1)'],
            cwd=str(self.root),inputs=[])['result'],'DENIED')
        self.assertIsNone(self.host.scope)
    def test_prepared_profile_is_not_agent_release(self):
        prepared=programmer_authorization(self.binding,'prepared',1,'ps','pt',
            exec_argv_allowlist=(('python3','code.py'),))
        self.assertEqual(prepared.state,'INACTIVE')
        host=GovernedHost(prepared,pathlib.Path(self.audit.name)/'prepared.jsonl')
        orch=ReasoningOrchestrator(host)
        denied=orch.request(action(type='write',action_request_id='prepared-effect',
            session_id='ps',turn_id='pt',authorization_id='prepared',
            authorization_revision=1,repository=str(self.root),path='code.py',
            content='effect'))
        self.assertEqual(denied['result'],'DENIED')
        self.assertEqual((self.root/'code.py').read_text(),'print(1)\n')
        with self.assertRaises(ValueError): ResponsesReasoning(orch).run('task',
            self.binding.model_context(),1)

if __name__=='__main__': unittest.main()
