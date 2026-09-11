import tempfile, pathlib, unittest, json, time
from adapter.governed_host import GovernedHost, WorkAuthorization, Denied

class A2Tests(unittest.TestCase):
 def setUp(self):
  self.d=tempfile.TemporaryDirectory(); self.root=pathlib.Path(self.d.name); (self.root/'ok').write_text('input'); (self.root/'protected').mkdir(); (self.root/'protected'/'x').write_text('secret')
  self.auth=WorkAuthorization('auth-a2',1,'scratch','s','t',(str(self.root),),(str(self.root/'ok'),str(self.root/'new')),(str(self.root/'protected'),),('python3',),False,False)
  self.h=GovernedHost(self.auth,self.root/'audit.jsonl')
 def tearDown(self): self.d.cleanup()
 def test_read_write_and_denials(self):
  self.assertEqual(self.h.governed_read(self.root,'ok')['content'],'input'); self.h.governed_write(self.root,'new','x'); self.assertRaises(Denied,self.h.governed_read,self.root,'protected/x'); self.assertRaises(Denied,self.h.governed_write,self.root,'protected/x','bad'); self.assertFalse((self.root/'protected'/'x').read_text()=='bad')
 def test_whole_patch(self):
  self.assertRaises(Denied,self.h.governed_patch,self.root,[{'op':'write','path':'new','content':'ok'},{'op':'write','path':'protected/x','content':'bad'}]); self.assertFalse((self.root/'new').exists()); self.assertEqual((self.root/'protected/x').read_text(),'secret')
 def test_scope_revocation_and_reuse(self):
  r=self.h.governed_exec(('python3','-c','import time; time.sleep(30)'),self.root); self.assertTrue(r['scope']); sid=self.h.scope.id; self.assertEqual(self.h.revoke(),'QUIESCENT'); self.assertEqual(self.h.status()['scope_state'],'QUIESCENT'); h2=GovernedHost(WorkAuthorization('a2',1,'s','s','t2',(str(self.root),),(str(self.root/'ok'),),(),('python3',),False,False),self.root/'audit2'); h2.governed_exec(('python3','-c','print(1)'),self.root); self.assertNotEqual(sid,h2.scope.id)
 def test_expansion_is_non_effecting(self):
  e=self.h.expansion('protected_write','write',['protected/x'],'need fixture'); self.assertEqual(e['decision'],'PENDING'); self.assertEqual((self.root/'protected/x').read_text(),'secret')

if __name__=='__main__': unittest.main()
