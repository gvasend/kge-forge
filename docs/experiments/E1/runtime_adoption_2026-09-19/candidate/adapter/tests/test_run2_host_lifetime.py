"""No host launch. Qualify frozen guards and preservation of the child boundary."""
import ast,hashlib,os,runpy,unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
PACKAGE=ROOT/'docs/experiments/E1/run2_nonhost_closure_2026-09-17/host_package'
class Unit:
 def __init__(self,data):self.data=data
 def resolve(self):return self
 def stat(self):return SimpleNamespace(st_uid=0,st_mode=0o100644)
 def read_bytes(self):return self.data
 def __str__(self):return '/etc/systemd/system/kge-forge-supervisor-run2.service'
class HostLifetimeTests(unittest.TestCase):
 def setUp(self):
  self.ns=runpy.run_path(str(PACKAGE/'host_launch.py'))
  self.unit=Unit((PACKAGE/'kge-forge-supervisor-run2.service').read_bytes())
  self.plan={'host_lifetime':{'unit_sha256':hashlib.sha256(self.unit.data).hexdigest()}}
  self.properties={'MainPID':'1234','User':'root','Group':'root','Restart':'no',
   'StandardInput':'null','StandardOutput':'journal','StandardError':'journal',
   'FragmentPath':str(self.unit),'DropInPaths':'','InvocationID':'a'*32}
 def run_guard(self,parent=1,session=1234,tty=False):
  fn=self.ns['lifetime'];g=fn.__globals__
  with patch.dict(g,{'Path':lambda p:self.unit if str(p)==str(self.unit) else Path(p),
                     'start':lambda p:{'ppid':0,'start_ticks':1}}), \
       patch('os.getppid',return_value=parent),patch('os.getpid',return_value=1234), \
       patch('os.getsid',return_value=session),patch('os.isatty',return_value=tty), \
       patch.dict(os.environ,{'INVOCATION_ID':'a'*32}), \
       patch('subprocess.check_output',return_value='\n'.join(k+'='+v for k,v in self.properties.items()).encode()):
   return fn(self.plan)
 def test_expected_independent_service(self):self.assertTrue(self.run_guard()['terminal_independent'])
 def test_terminal_parent_session_rejected(self):
  for kwargs in ({'parent':10},{'session':2},{'tty':True}):
   with self.subTest(kwargs=kwargs),self.assertRaises(RuntimeError):self.run_guard(**kwargs)
 def test_restart_or_dropin_rejected(self):
  for key,value in [('Restart','always'),('DropInPaths','/tmp/override'),('User','1000'),('InvocationID','')]:
   saved=dict(self.properties);self.properties[key]=value
   with self.subTest(key=key),self.assertRaises(RuntimeError):self.run_guard()
   self.properties=saved
 def test_unit_substitution_rejected(self):
  self.plan['host_lifetime']['unit_sha256']='0'*64
  with self.assertRaises(RuntimeError):self.run_guard()
 def test_qualified_child_placement_and_credential_drop_unchanged(self):
  original=ROOT/'docs/experiments/E1/pre_dispatch/supervisor_succession_2026-09-17/host_launch.py'
  self.assertEqual(hashlib.sha256(original.read_bytes()).hexdigest(),'bf98d94070c5fdcc7861fc6383529f31e8de228571f184342c4cbd414b9be7d6')
  def child(p):
   tree=ast.parse(p.read_text())
   return next(ast.dump(n,include_attributes=False) for n in ast.walk(tree) if isinstance(n,ast.If) and ast.dump(n.test)==ast.dump(ast.parse('pid == 0',mode='eval').body))
  self.assertEqual(child(original),child(PACKAGE/'host_launch.py'))
if __name__=='__main__':unittest.main()
