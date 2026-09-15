import json, pathlib, tempfile, unittest
from adapter.governed_host import GovernedHost, WorkAuthorization, Denied
from adapter.orchestrator import ReasoningOrchestrator, action
from adapter.recovery_ledger import reconstruct, RecoveryDenied

class RecoveryLedgerTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.base=pathlib.Path(self.temp.name)
        self.root=self.base/'source'; self.root.mkdir()
        self.evidence=self.base/'evidence'; self.evidence.mkdir()
        self.audit=self.evidence/'controller.jsonl'
        self.auth=WorkAuthorization('auth-recovery',1,'scratch','session','turn',
            (str(self.root),),(str(self.root),),(),('python3',),False,False)
    def tearDown(self): self.temp.cleanup()
    def test_restart_replays_exact_result_and_rejects_changed_request_or_grant(self):
        first=ReasoningOrchestrator(GovernedHost(self.auth,self.audit))
        original=action(action_request_id='req-write',type='write',session_id='session',
            turn_id='turn',authorization_id='auth-recovery',authorization_revision=1,
            repository=str(self.root),path='file.py',content='original')
        result=first.request(original)
        self.assertEqual(result['result'],'SUCCEEDED')
        restored=ReasoningOrchestrator(GovernedHost(self.auth,self.audit))
        self.assertEqual(restored.request(original),result)
        changed={**original,'content':'changed'}
        self.assertEqual(restored.request(changed)['result'],'DENIED')
        self.assertEqual((self.root/'file.py').read_text(),'original')
        expanded=WorkAuthorization('auth-recovery',1,'scratch','session','turn',
            (str(self.base),),(str(self.base),),(),('python3',),False,False)
        with self.assertRaises(Denied): GovernedHost(expanded,self.audit)
    def test_active_and_uncertain_scope_require_live_evidence(self):
        GovernedHost(self.auth,self.audit)
        sid='scope-'+'a'*32; rid='req-active'
        with self.audit.open('a') as stream:
            for event in ({'event':'action_request','action_request_id':rid,'type':'exec',
                'session_id':'session','turn_id':'turn','authorization_id':'auth-recovery',
                'authorization_revision':1,'request_sha256':'digest'},
                {'event':'execution_snapshot_created','action_request_id':rid,
                 'execution_scope_id':sid,'workspace_root':str(self.root),
                 'source_root':str(self.root)},
                {'event':'execution_scope_reserved','action_request_id':rid,'execution_scope_id':sid},
                {'event':'execution_scope_created','action_request_id':rid,'execution_scope_id':sid}):
                stream.write(json.dumps(event)+'\n')
        supervisor=self.base/'supervisor.jsonl'
        supervisor.write_text(json.dumps({'event':'scope_created','scope_id':sid,
            'owner':['session','auth-recovery',rid]})+'\n')
        cgroup=self.base/'executor'; cgroup.mkdir()
        scope=cgroup/sid; scope.mkdir()
        (scope/'cgroup.procs').write_text('123')
        (scope/'cgroup.events').write_text('populated 1\n')
        state=reconstruct(self.audit,self.auth,supervisor,cgroup)
        self.assertEqual(state['category'],'ACTIVE')
        self.assertEqual(state['scope']['observation']['members'],[123])
        self.assertEqual(state['results'][rid]['result'],'INDETERMINATE')
        (scope/'cgroup.events').unlink()
        state=reconstruct(self.audit,self.auth,supervisor,cgroup)
        self.assertEqual(state['category'],'UNCERTAIN')
        self.assertFalse(state['scope']['eligible_for_reconcile'])
    def test_contradictory_result_digest_fails_closed(self):
        first=ReasoningOrchestrator(GovernedHost(self.auth,self.audit))
        first.request(action(action_request_id='req-status',type='status',session_id='session',
            turn_id='turn',authorization_id='auth-recovery',authorization_revision=1))
        lines=self.audit.read_text().splitlines()
        records=[json.loads(line) for line in lines]
        for record in records:
            if record.get('event')=='action_result': record['digest']='0'*64
        self.audit.write_text(''.join(json.dumps(record)+'\n' for record in records))
        with self.assertRaises(RecoveryDenied): reconstruct(self.audit,self.auth)
    def test_rejected_unknown_action_remains_rejected_after_restart(self):
        first=ReasoningOrchestrator(GovernedHost(self.auth,self.audit))
        raw=action(action_request_id='req-unknown',type='exec_command',
            session_id='session',turn_id='turn',authorization_id='auth-recovery',
            authorization_revision=1)
        self.assertEqual(first.request(raw)['result'],'DENIED')
        restored=ReasoningOrchestrator(GovernedHost(self.auth,self.audit))
        self.assertEqual(restored.request(raw)['result'],'DENIED')
        self.assertEqual(restored.request({**raw,'type':'exec'})['result'],'DENIED')

if __name__=='__main__': unittest.main()
