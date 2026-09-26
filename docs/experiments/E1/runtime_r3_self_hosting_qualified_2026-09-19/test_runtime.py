"""Bounded negative/recovery probes from exact R3, isolated authority state."""
import json,sys,tempfile,shutil,unittest,subprocess,multiprocessing,signal
from pathlib import Path
from unittest.mock import patch
O=Path(__file__).resolve().parent;Q=json.loads((O/'RUNTIME_QUALIFICATION_FINAL.json').read_bytes())
sys.path.insert(0,Q['R3']['root'])
from adapter import ordinary_runtime as a,runtime_adoption as r
from adapter.controller_authority_store import ControllerAuthorityStore,encoded,sha

def child_validate(pin,root,binding):
 code='import sys,json;sys.path.insert(0,sys.argv[1]);from adapter.controller_authority_store import ControllerAuthorityStore;from adapter.ordinary_runtime import validate_executing_runtime;s=ControllerAuthorityStore(**json.loads(sys.argv[2]));print(json.dumps(validate_executing_runtime(s,json.loads(sys.argv[3]))));s.close()'
 return subprocess.run([sys.executable,'-B','-c',code,root,json.dumps(pin),json.dumps(binding)],capture_output=True,text=True,timeout=30)

class Fixture:
 def __init__(self,grant=True,changes=None):
  self.root=Path(tempfile.mkdtemp(prefix='r3-runtime-negatives-'));self.root.chmod(0o700)
  old=ControllerAuthorityStore(**Q['selected_store']);self.records={k:{'bytes':old.resolve(k),'evidence':[]} for k in old.catalog['objects']};self.app=dict(old.applicability)
  self.private={}
  for key,row in old.catalog['private_state'].items():
   path=self.root/Path(row['path']).name;path.write_bytes(Path(row['path']).read_bytes());path.chmod(0o600);self.private[key]=dict(row,path=str(path))
  old.close();self.ledger=Path(self.private['qualification:runtime']['path']);self.enrollment=Path(self.private['qualification:enrollment']['path'])
  body={'schema':'ENROLLED-RUNTIME-ADOPTION-DECISION-1','authority':'Architect','decision':'ADOPT_EXACT_ENROLLED_CONTINUATION','binding_kind':'QUALIFICATION_BINDING','lineage':Q['delegation']['lineage'],'delegation':Q['delegation']['id'],'candidate':Q['R4_ref'],'enrollment':Q['R4_enrollment']['id'],'qualification':Q['R4_enrollment']['qualification'],'predecessor':Q['R3']['identity'],'successor':Q['R4']['identity'],'head_event':Q['synthetic_current']['head']}
  if changes:body.update(changes)
  data=encoded(r.seal('ENROLLED-RUNTIME-ADOPTION-DECISION',body));h=sha(data);self.grant={'authority_id':'sha256:'+h,'sha256':h};self.records['sha256:'+h]={'bytes':data,'evidence':[]}
  if grant:self.records['runtime-adoption-decision:'+h]={'bytes':data,'evidence':[]}
  self.s=ControllerAuthorityStore.materialize(self.root/'store',self.records,{}, {'authority_source':Q['adoption_ref'],'release_identities':Q['delegation']['context']},self.app,[],self.private)
  self.pin={'root':str(self.s.root),'catalog_sha256':self.s.catalog_sha256,'applicability':self.s.applicability}
 def adopt(self):return a.adopt(self.s,None,Q['R4_ref'],Q['R4_enrollment']['id'],self.grant)
 def close(self):self.s.close()

def worker(pin,grant,out):
 s=ControllerAuthorityStore(**pin)
 try:out.put(('PASS',a.adopt(s,None,Q['R4_ref'],Q['R4_enrollment']['id'],grant)['runtime']))
 except Exception as exc:out.put(('REJECT',str(exc)))
 finally:s.close()

class Tests(unittest.TestCase):
 def setUp(self):
  signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('30 second qualification deadlock detector')));signal.alarm(30)
 def tearDown(self):signal.alarm(0)
 def fixture(self,**kwargs):
  f=Fixture(**kwargs);self.addCleanup(f.close);return f
 def test_exact_R3_independent_self_hosting(self):
  f=self.fixture();child=child_validate(f.pin,Q['R3']['root'],Q['R3_binding']);self.assertEqual(child.returncode,0,child.stderr)
  result=json.loads(child.stdout);self.assertEqual(result['runtime'],Q['R3']['identity']);self.assertEqual(result['executing_root'],Q['R3']['root'])
 def test_R4_enrolled_does_not_select(self):
  f=self.fixture();a.eligible(f.s,Q['R4_ref'],Q['R4_enrollment']['id']);self.assertEqual(a.reconstruct(f.s)['runtime'],Q['R3']['identity'])
  child=child_validate(f.pin,Q['R4']['root'],Q['R3_binding']);self.assertNotEqual(child.returncode,0)
 def test_R4_separate_adoption_and_self_hosting(self):
  f=self.fixture();s=f.adopt();self.assertEqual(s['runtime'],Q['R4']['identity'])
  child=child_validate(f.pin,Q['R4']['root'],a.binding(f.s));self.assertEqual(child.returncode,0,child.stderr)
  self.assertNotEqual(child_validate(f.pin,Q['R3']['root'],a.binding(f.s)).returncode,0)
 def test_missing_adoption(self):
  f=self.fixture(grant=False)
  with self.assertRaises(Exception):f.adopt()
 def test_wrong_adoption_actor(self):
  f=self.fixture(changes={'authority':'R4'})
  with self.assertRaises(ValueError):f.adopt()
 def test_wrong_predecessor(self):
  f=self.fixture(changes={'predecessor':Q['R1']['identity']})
  with self.assertRaises(ValueError):f.adopt()
 def test_wrong_head(self):
  f=self.fixture();binding=dict(Q['R3_binding'],head_event='wrong')
  with self.assertRaises(ValueError):a.validate_executing_runtime(f.s,binding)
 def test_stale_enrollment_after_adoption(self):
  f=self.fixture();f.adopt()
  with self.assertRaisesRegex(ValueError,'stale'):a.eligible(f.s,Q['R4_ref'],Q['R4_enrollment']['id'])
 def test_replay(self):
  f=self.fixture();f.adopt();before=f.ledger.read_bytes()
  with self.assertRaises(ValueError):f.adopt()
  self.assertEqual(before,f.ledger.read_bytes())
 def test_competing_adoption(self):
  f=self.fixture();out=multiprocessing.Queue();ps=[multiprocessing.Process(target=worker,args=(f.pin,f.grant,out)) for _ in range(2)]
  for p in ps:p.start()
  for p in ps:p.join(12);self.assertFalse(p.is_alive())
  self.assertEqual(sorted(out.get(timeout=1)[0] for _ in ps),['PASS','REJECT'])
 def test_interrupted_intent(self):
  f=self.fixture();original=a.append;n=[0]
  def cut(*args):
   if n[0]==1:raise InterruptedError()
   n[0]+=1;return original(*args)
  with patch.object(a,'append',side_effect=cut):
   with self.assertRaises(InterruptedError):f.adopt()
  self.assertEqual(a.recover(f.s,None)['runtime'],Q['R3']['identity'])
 def test_interrupted_commit(self):
  f=self.fixture();original=a.append;n=[0]
  def cut(*args):
   if n[0]==2:raise InterruptedError()
   n[0]+=1;return original(*args)
  with patch.object(a,'append',side_effect=cut):
   with self.assertRaises(InterruptedError):f.adopt()
  self.assertEqual(a.recover(f.s,None)['runtime'],Q['R4']['identity'])
 def test_unknown_and_torn_evidence(self):
  f=self.fixture();f.ledger.write_bytes(f.ledger.read_bytes()+b'{')
  with self.assertRaises(ValueError):a.reconstruct(f.s)
 def test_substituted_executing_bytes(self):
  f=self.fixture();root=f.root/'wrong-runtime';shutil.copytree(Q['R3']['root'],root,ignore=shutil.ignore_patterns('__pycache__'))
  with (root/'adapter/ordinary_runtime.py').open('a') as out:out.write('\n# substituted bytes\n')
  self.assertNotEqual(child_validate(f.pin,str(root),Q['R3_binding']).returncode,0)
 def test_missing_enrollment(self):
  f=self.fixture();rows=f.enrollment.read_bytes().splitlines(True);f.enrollment.write_bytes(rows[0])
  with self.assertRaises(ValueError):f.adopt()
 def test_historical_bootstrap_mutation_paths_unused(self):
  f=self.fixture();a.reconstruct(f.s)
  modules=[v for k,v in sys.modules.items() if k.startswith('_forge_frozen_runtime_') and k.endswith('.runtime_bootstrap')]
  self.assertTrue(modules)
  with patch.object(modules[0],'establish',side_effect=AssertionError('bootstrap reused')),patch.object(modules[0],'recover',side_effect=AssertionError('bootstrap recovery reused')):
   f.adopt();a.reconstruct(f.s)

if __name__=='__main__':unittest.main(verbosity=2)
