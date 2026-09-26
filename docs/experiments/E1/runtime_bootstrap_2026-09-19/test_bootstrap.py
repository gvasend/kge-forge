import sys,json,tempfile,os,importlib.util,multiprocessing,unittest
from pathlib import Path
from unittest.mock import patch
O=Path(__file__).resolve().parent;sys.path.insert(0,str(O/'candidate'))
from adapter import runtime_adoption as r, runtime_bootstrap as b
from adapter.controller_authority_store import ControllerAuthorityStore,encoded,sha
spec=importlib.util.spec_from_file_location('prior_fixture',O.parent/'runtime_adoption_2026-09-19/test_runtime_adoption.py');prior=importlib.util.module_from_spec(spec);spec.loader.exec_module(prior)

class Fixture(prior.Fixture):
 def __init__(self,mutation=None):
  self.mutation=mutation;super().__init__('QUALIFICATION_BINDING')
 def finish(self):
  if hasattr(self,'r2'):
   third=self.root/'r3';third.mkdir(mode=0o700);(third/'adapter').mkdir(mode=0o700);data=b'third successor\n';(third/'adapter/x.py').write_bytes(data);self.add(data)
   self.r3=self.add({'schema':'RUNTIME-INVENTORY-1','root':str(third),'identity':'sha256:'+sha(encoded({'x.py':sha(data)})),'files':{'x.py':sha(data)}})
   self.c4,self.g4=self.add_transition(self.r2,self.r3)
  self.bjournal=self.root/'bootstrap.jsonl';self.bjournal.touch(mode=0o600)
  self.p.update(bootstrap_journal='fixture-bootstrap-journal',bootstrap_lineage='fixture-legacy-lineage')
  self.p=r.seal('RUNTIME-HEAD-AUTHORITY',{k:v for k,v in self.p.items() if k!='id'});pref=self.add(self.p)
  sentinel=self.root/'legacy-sentinel';sentinel.write_bytes(b'legacy authority')
  expected={'runtime':self.obj(self.r0)['identity'],'release_context':self.ancestry}
  inputref=self.add({'sentinel':str(sentinel),'sha256':sha(sentinel.read_bytes()),'expected':expected})
  driver=O/'fixture_legacy_verifier.py';consumer={p.name:sha(p.read_bytes()) for p in Path(b.__file__).parent.glob('*.py')}
  q=self.add({'result':'PASS','scope':'BOUNDED_BOOTSTRAP','consumer_files':consumer,'legacy_runtime':expected['runtime'],'first_continuation':self.c1})
  record={'schema':'RUNTIME-AUTHORITY-BOOTSTRAP-1','lineage':self.p['bootstrap_lineage'],'binding_kind':self.kind,'runtime_head_authority':self.p['id'],'material_amendment':self.p['material_amendment'],
    'legacy_runtime':expected['runtime'],'successor_runtime':self.obj(self.r1)['identity'],'release_context':self.ancestry,'consumer_files':consumer,'qualification':q,'supervisor':None,
    'first_continuation':self.c1,'first_adoption_authority':self.g1,'legacy_verifier':{'python':sys.executable,'python_sha256':sha(Path(sys.executable).read_bytes()),'path':str(driver),'sha256':sha(driver.read_bytes()),'input':inputref,'expected':expected}}
  if self.mutation:self.mutation(record)
  self.record=r.seal('RUNTIME-AUTHORITY-BOOTSTRAP',record);self.recordref=self.add(self.record)
  grant={'authority':'Architect','decision':'AUTHORIZE_ONE_TIME_RUNTIME_AUTHORITY_BOOTSTRAP','record':self.recordref,'lineage':record['lineage'],'binding_kind':self.kind}
  self.grant=self.add(dict(grant,authority_source=self.add(dict(grant,channel='user'))));selector=self.add({'record':self.recordref,'Architect_authorization':self.grant})
  self.s=ControllerAuthorityStore.materialize(self.root/'store',self.records,{r.POLICY:pref['authority_id'],b.SELECTOR:selector['authority_id']},{'authority_source':pref,'release_identities':self.ancestry},{'runtime_head_authority':self.p['id']},['/home/gvasend/app/kge-forge'],{
   'fixture-runtime-journal':{'path':str(self.ledger),'mutation':'APPEND_ONLY','mechanism':'RUNTIME-ADOPTION-JOURNAL-1'},'fixture-bootstrap-journal':{'path':str(self.bjournal),'mutation':'APPEND_ONLY','mechanism':'ONE-TIME-RUNTIME-BOOTSTRAP-1'}})
  self.pin={'root':str(self.s.root),'catalog_sha256':self.s.catalog_sha256,'applicability':self.s.applicability}
 def establish(self):return b.establish(self.s,binding_kind=self.kind)

def worker(pin,q):
 s=ControllerAuthorityStore(**pin)
 try:q.put(('PASS',b.establish(s,binding_kind='QUALIFICATION_BINDING')))
 except Exception as e:q.put(('REJECT',str(e)))
 finally:s.close()

class Tests(unittest.TestCase):
 def setUp(self):self.f=Fixture();self.addCleanup(self.f.s.close)
 def test_legacy_reconstructs(self):
  f=self.f;self.assertEqual(b.reconstruct(f.s)['state'],'PREDECESSOR_CURRENT');self.assertEqual(b.legacy(f.s,f.p,f.record)['runtime'],f.obj(f.r0)['identity'])
 def test_ordinary_head_not_available_before_bootstrap(self):
  with self.assertRaisesRegex(ValueError,'not established'):r.reconstruct(self.f.s)
  with self.assertRaisesRegex(ValueError,'not established'):self.f.adopt()
 def test_wrong_legacy(self):
  f=Fixture(lambda row:row.update(legacy_runtime='wrong'));self.addCleanup(f.s.close)
  with self.assertRaisesRegex(ValueError,'wrong legacy'):f.establish()
 def test_changed_R0(self):
  f=self.f;Path(f.obj(f.r0)['root'],'adapter/x.py').write_bytes(b'wrong')
  with self.assertRaisesRegex(ValueError,'unaccounted runtime'):f.establish()
 def test_missing_authorization(self):
  f=self.f;source=f.s.root/f.grant['sha256'];source.unlink()
  with self.assertRaises(Exception):f.establish()
  self.assertEqual(f.bjournal.read_bytes(),b'')
 def test_wrong_amendment(self):
  f=Fixture(lambda row:row.update(material_amendment={'authority_id':'wrong','sha256':'0'*64}));self.addCleanup(f.s.close)
  with self.assertRaises(ValueError):f.establish()
 def test_wrong_head_authority(self):
  f=Fixture(lambda row:row.update(runtime_head_authority='wrong'));self.addCleanup(f.s.close)
  with self.assertRaises(ValueError):f.establish()
 def test_wrong_successor(self):
  f=Fixture(lambda row:row.update(successor_runtime='wrong'));self.addCleanup(f.s.close)
  with self.assertRaises(ValueError):f.establish()
  self.assertEqual(f.bjournal.read_bytes(),b'')
 def test_success_and_independent_reconstruction(self):
  f=self.f;s=f.establish();self.assertEqual(s['runtime'],f.obj(f.r1)['identity']);self.assertEqual(r.reconstruct(f.s)['current_runtime'],s['runtime'])
  q=multiprocessing.Queue()
  def read():
   st=ControllerAuthorityStore(**f.pin);q.put(b.reconstruct(st));st.close()
  child=multiprocessing.Process(target=read);child.start();child.join(5);self.assertFalse(child.is_alive());self.assertEqual(q.get(timeout=1),s)
  self.assertEqual(Path(f.obj(f.r0)['root'],'adapter/x.py').read_bytes(),b'old\n')
 def test_replay(self):
  f=self.f;f.establish();before=f.bjournal.read_bytes()
  with self.assertRaises(ValueError):f.establish()
  self.assertEqual(before,f.bjournal.read_bytes())
 def test_competing_bootstrap(self):
  f=self.f;q=multiprocessing.Queue();ps=[multiprocessing.Process(target=worker,args=(f.pin,q)) for _ in range(2)]
  for p in ps:p.start()
  for p in ps:p.join(5);self.assertFalse(p.is_alive())
  self.assertEqual(sorted(q.get(timeout=1)[0] for _ in ps),['PASS','REJECT'])
 def test_distinct_competing_bootstrap_records(self):
  f=self.f;other=dict(f.record);other.pop('id');other['first_continuation']=f.c2;other['first_adoption_authority']=f.g2;other['successor_runtime']=f.obj(f.r2)['identity']
  q=f.obj(other['qualification']);q['first_continuation']=f.c2;other['qualification']=f.add(q);other=r.seal('RUNTIME-AUTHORITY-BOOTSTRAP',other);ref=f.add(other)
  body={'authority':'Architect','decision':'AUTHORIZE_ONE_TIME_RUNTIME_AUTHORITY_BOOTSTRAP','record':ref,'lineage':other['lineage'],'binding_kind':f.kind};grant=f.add(dict(body,authority_source=f.add(dict(body,channel='user'))));selector=f.add({'record':ref,'Architect_authorization':grant});pref=f.add(f.p)
  st=ControllerAuthorityStore.materialize(f.root/'competing-store',f.records,{r.POLICY:pref['authority_id'],b.SELECTOR:selector['authority_id']},{'authority_source':pref,'release_identities':f.ancestry},f.s.applicability,[],dict(f.s.catalog['private_state']))
  self.addCleanup(st.close);f.establish();before=f.bjournal.read_bytes()
  with self.assertRaises(ValueError):b.establish(st,binding_kind=f.kind)
  self.assertEqual(before,f.bjournal.read_bytes())
 def test_durable_intent_before_runtime_writes(self):
  f=self.f;original=r.append
  def observe(*args):
   self.assertEqual(json.loads(f.bjournal.read_bytes().splitlines()[0])['event'],'BOOTSTRAP_INTENT');return original(*args)
  with patch.object(r,'append',observe):f.establish()
 def test_bootstrap_interruptions(self):
  for stop in range(4):
   f=Fixture();self.addCleanup(f.s.close);old=b.append;calls=[0]
   def fault(*args):
    if calls[0]==stop:raise InterruptedError('bootstrap fault')
    old(*args);calls[0]+=1
   with patch.object(b,'append',fault):
    try:f.establish()
    except InterruptedError:pass
   state=b.recover(f.s);self.assertEqual(state['runtime'],f.obj(f.r0 if stop<2 else f.r1)['identity'])
   if stop>0:
    with self.assertRaises(ValueError):f.establish()
 def test_interrupted_staging_not_current(self):
  for stop in range(3):
   f=Fixture();self.addCleanup(f.s.close);old=r.append;calls=[0]
   def fault(*args):
    if calls[0]==stop:raise InterruptedError('runtime stage fault')
    old(*args);calls[0]+=1
   with patch.object(r,'append',fault):
    try:f.establish()
    except InterruptedError:pass
   self.assertEqual(b.recover(f.s)['state'],'PREDECESSOR_CURRENT')
   with self.assertRaises(ValueError):r.reconstruct(f.s)
 def test_second_ordinary_successor_without_bootstrap(self):
  f=self.f;f.establish();before=f.bjournal.read_bytes();state=f.adopt(f.c3,f.g3)
  self.assertEqual(state['current_runtime'],f.obj(f.r2)['identity']);self.assertEqual(before,f.bjournal.read_bytes());self.assertEqual(len(state['continuations']),2)
  third=f.adopt(f.c4,f.g4);self.assertEqual(third['current_runtime'],f.obj(f.r3)['identity']);self.assertEqual(len(third['continuations']),3);self.assertEqual(before,f.bjournal.read_bytes())
 def test_arbitrary_bytes_rejected_after_bootstrap(self):
  f=self.f;f.establish();Path(f.obj(f.r1)['root'],'adapter/x.py').write_bytes(b'arbitrary')
  with self.assertRaises(ValueError):r.reconstruct(f.s)
 def test_torn_bootstrap(self):
  f=self.f;f.establish();f.bjournal.write_bytes(f.bjournal.read_bytes()[:-1])
  with self.assertRaisesRegex(ValueError,'INDETERMINATE'):b.recover(f.s)
 def test_qualification_not_production(self):
  with self.assertRaises(ValueError):b.establish(self.f.s)
 def test_changed_legacy_authority(self):
  f=self.f;(f.root/'legacy-sentinel').write_bytes(b'changed')
  with self.assertRaises(Exception):f.establish()
  self.assertEqual(f.bjournal.read_bytes(),b'')
 def test_exact_bootstrap_code(self):
  f=Fixture(lambda row:row['consumer_files'].update(unknown='0'*64));self.addCleanup(f.s.close)
  with self.assertRaisesRegex(ValueError,'implementation substitution'):f.establish()

if __name__=='__main__':unittest.main(verbosity=2)
