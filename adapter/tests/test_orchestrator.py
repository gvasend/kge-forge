import tempfile, pathlib, unittest, json
from adapter.governed_host import GovernedHost, WorkAuthorization
from adapter.orchestrator import ReasoningOrchestrator, ProtocolError, action

class ProtocolTests(unittest.TestCase):
 def setUp(self):
  self.d=tempfile.TemporaryDirectory(); self.root=pathlib.Path(self.d.name); (self.root/'program.py').write_text('print(1)')
  a=WorkAuthorization('a2.3',1,'scratch','session-1','turn-1',(str(self.root),),(str(self.root/'program.py'),str(self.root/'out.py')),(),('python3',),False,False)
  self.o=ReasoningOrchestrator(GovernedHost(a,self.root/'audit.jsonl')); self.base={'session_id':'session-1','turn_id':'turn-1','authorization_id':'a2.3','authorization_revision':1}
 def req(self,typ,**kw): return self.o.request(action(action_request_id='r-'+typ+str(len(self.o.results)),type=typ,**self.base,**kw))
 def test_typed_read_write_exec_and_replay(self):
  self.assertEqual(self.req('read',repository=self.root,path='program.py')['result'],'SUCCEEDED'); w=self.req('write',repository=self.root,path='out.py',content='ok'); self.assertEqual(w['result'],'SUCCEEDED'); self.assertEqual(self.o.request(action(action_request_id=w['action_request_id'],type='write',**self.base,repository=self.root,path='out.py',content='changed')),w); self.assertEqual(self.req('exec',executable='python3',argv=['program.py'],cwd=self.root)['result'],'SUCCEEDED')
 def test_denials_and_malformed(self):
  self.assertEqual(self.req('read',repository=self.root,path='../etc/passwd')['result'],'DENIED'); self.assertEqual(self.req('write',repository=self.root,path='blocked',content='x')['result'],'DENIED'); self.assertEqual(self.req('exec',executable='rm',argv=['-rf','x'],cwd=self.root)['result'],'DENIED'); self.assertEqual(self.req('authority_expansion',capability='read',action='read',resources=['protected'],reason='need')['result'],'SUCCEEDED'); self.assertRaises(ProtocolError,self.o.request,{'type':'write'})
 def test_prose_and_unknown(self):
  self.assertEqual(self.o.request(action(action_request_id='prose',type='run shell',**self.base,text='rm -rf /'))['result'],'DENIED'); self.assertEqual(self.o.request(action(action_request_id='unknown',type='exec_command',**self.base))['result'],'DENIED')

if __name__=='__main__': unittest.main()
