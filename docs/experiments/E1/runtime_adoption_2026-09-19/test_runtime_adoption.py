"""Synthetic private stores; never production grants or invocation lifecycle."""
import json, os, sys, tempfile, unittest, multiprocessing, time
from pathlib import Path
from unittest.mock import patch
O=Path(__file__).resolve().parent;sys.path.insert(0,str(O/'candidate'))
from adapter import runtime_adoption as r
from adapter.controller_authority_store import ControllerAuthorityStore,encoded,sha

class Fixture:
 def __init__(self,kind='PRODUCTION_ADOPTION',actual=False):
  self.root=Path(tempfile.mkdtemp(prefix='runtime-adoption-qualification-'));self.root.chmod(0o700);self.records={};self.kind=kind
  self.ledger=self.root/'runtime.jsonl';self.ledger.touch(mode=0o600)
  def runtime(name,content):
   root=self.root/name;root.mkdir(mode=0o700);(root/'adapter').mkdir(mode=0o700);(root/'adapter'/'x.py').write_bytes(content);self.add(content)
   return self.add({'schema':'RUNTIME-INVENTORY-1','root':str(root),'identity':'sha256:'+sha(encoded({'x.py':sha(content)})),'files':{'x.py':sha(content)}})
  self.r0=runtime('r0',b'old\n');self.r1=runtime('r1',b'new\n');self.r2=runtime('r2',b'other\n')
  self.ancestry={'release_authority':'fixture-release','OperationalContextId':'fixture-context','continuation_chain_digest':'fixture-chain','ReleaseBasisId':'fixture-basis','ReleaseDecisionId':'fixture-decision'}
  mechanism=self.add(Path(r.__file__).read_bytes())
  amendment=self.add(r.seal('RUNTIME-CONSUMPTION-AMENDMENT',{'schema':'RUNTIME-CONSUMPTION-AMENDMENT-1','classification':'MATERIAL','release_context':self.ancestry,'mechanism':mechanism,'rules':r.RULES}))
  md={'authority':'Architect','decision':'ADOPT_RUNTIME_CONSUMPTION_AMENDMENT','amendment':amendment,'binding_kind':kind};mdref=self.add(dict(md,authority_source=self.add(dict(md,channel='user'))))
  self.p={'schema':'RUNTIME-HEAD-AUTHORITY-1','binding_kind':kind,'material_amendment':amendment,'material_decision':mdref,'release_context':self.ancestry,'mechanism':mechanism,'genesis':self.r0,'journal':'fixture-runtime-journal','adoptions':[],'qualified_evidence':[]}
  self.c1,self.g1=self.add_transition(self.r0,self.r1)
  self.c2,self.g2=self.add_transition(self.r0,self.r2)
  self.c3,self.g3=self.add_transition(self.r1,self.r2)
  self.finish()
 def obj(self,ref):return json.loads(self.records[ref['authority_id']]['bytes'])
 def add(self,value):
  b=value if isinstance(value,bytes) else encoded(value);h=sha(b);self.records['sha256:'+h]={'bytes':b,'evidence':[]};return {'authority_id':'sha256:'+h,'sha256':h}
 def add_transition(self,before,after):
  b=self.obj(before);a=self.obj(after);delta=[{'path':n,'old_sha256':b['files'].get(n),'new_sha256':a['files'].get(n)} for n in sorted(set(b['files'])|set(a['files'])) if b['files'].get(n)!=a['files'].get(n)]
  q=self.add(r.seal('RUNTIME-QUALIFICATION',{'schema':'RUNTIME-QUALIFICATION-1','result':'PASS','delta':delta,'predecessor':b['identity'],'successor':a['identity'],'classification':'NON_MATERIAL_IMPLEMENTATION_CONTINUATION','evidence':[self.add({'synthetic':True})]}))
  c=self.add(r.seal('IMPLEMENTATION-RUNTIME-CONTINUATION',{'schema':'IMPLEMENTATION-RUNTIME-CONTINUATION-1','predecessor':before,'successor':after,'delta':delta,'classification':'NON_MATERIAL_IMPLEMENTATION_CONTINUATION','qualification':q,'original_continuation':None,'release_context':self.ancestry}))
  grant={'authority':'Architect','decision':'ADOPT_EXACT_RUNTIME_CONTINUATION','continuation':c,'predecessor':b['identity'],'successor':a['identity'],'release_context':self.ancestry,'binding_kind':self.kind,'material_amendment':self.p['material_amendment']}
  g=self.add(dict(grant,authority_source=self.add(dict(grant,channel='user'))));self.p['adoptions'].append({'continuation':c,'grant':g});self.p['qualified_evidence'].append(q);return c,g
 def finish(self):
  self.p=r.seal('RUNTIME-HEAD-AUTHORITY',{k:v for k,v in self.p.items() if k!='id'});pref=self.add(self.p)
  self.s=ControllerAuthorityStore.materialize(self.root/'store',self.records,{r.POLICY:pref['authority_id']},{'authority_source':pref,'release_identities':self.ancestry},{'runtime_head_authority':self.p['id']},['/home/gvasend/app/kge-forge'],{'fixture-runtime-journal':{'path':str(self.ledger),'mutation':'APPEND_ONLY','mechanism':'RUNTIME-ADOPTION-JOURNAL-1'}})
  self.pin={'root':str(self.s.root),'catalog_sha256':self.s.catalog_sha256,'applicability':self.s.applicability}
 def adopt(self,c=None,g=None):return r.adopt(self.s,c or self.c1,g or self.g1,binding_kind=self.kind)
 def binding(self,s):return {'runtime_head_authority':self.p['id'],'runtime':s['current_runtime'],'head_event':s['head_event']}

def child(pin,c,g,out):
 s=ControllerAuthorityStore(**pin)
 try:out.put(('PASS',r.adopt(s,c,g)['current_runtime']))
 except ValueError as e:out.put(('REJECT',str(e)))
 finally:s.close()

class Tests(unittest.TestCase):
 def setUp(self):self.f=Fixture();self.addCleanup(self.f.s.close)
 def test_genesis_and_unadopted(self):
  f=self.f;s=r.reconstruct(f.s);self.assertEqual(s['current_runtime'],f.obj(f.r0)['identity'])
  b=f.binding(s);b['runtime']=f.obj(f.r1)['identity']
  with self.assertRaises(ValueError):r.validate_invocation_runtime(f.s,b,f.obj(f.r1)['root'])
 def test_adoption_independent_restart(self):
  f=self.f;s=f.adopt();q=multiprocessing.Queue()
  def recover():
   st=ControllerAuthorityStore(**f.pin);q.put(r.reconstruct(st));st.close()
  p=multiprocessing.Process(target=recover);p.start();p.join(5);self.assertFalse(p.is_alive());self.assertEqual(q.get(timeout=1)['current_runtime'],s['current_runtime']);self.assertEqual(len(s['events']),3)
  r.validate_invocation_runtime(f.s,f.binding(s),f.obj(f.r1)['root']);self.assertTrue(Path(f.obj(f.r0)['root'],'adapter/x.py').exists())
 def test_replay(self):
  f=self.f;f.adopt();before=f.ledger.read_bytes()
  with self.assertRaises(ValueError):f.adopt()
  self.assertEqual(before,f.ledger.read_bytes())
 def test_skipped_predecessor(self):
  with self.assertRaises(ValueError):self.f.adopt(self.f.c3,self.f.g3)
 def test_ordered_two_hops(self):
  f=self.f;f.adopt();s=f.adopt(f.c3,f.g3);self.assertEqual(s['current_runtime'],f.obj(f.r2)['identity']);self.assertEqual(len(s['continuations']),2)
 def test_competing_threads_processes(self):
  f=self.f;q=multiprocessing.Queue();ps=[multiprocessing.Process(target=child,args=(f.pin,c,g,q)) for c,g in [(f.c1,f.g1),(f.c2,f.g2)]]
  for p in ps:p.start()
  for p in ps:p.join(5);self.assertFalse(p.is_alive())
  self.assertEqual(sorted(q.get(timeout=1)[0] for _ in ps),['PASS','REJECT']);self.assertEqual(len(r.reconstruct(f.s)['continuations']),1)
 def test_byte_substitution(self):
  f=self.f;Path(f.obj(f.r1)['root'],'adapter/x.py').write_text('substituted')
  with self.assertRaisesRegex(ValueError,'unaccounted runtime'):f.adopt()
  self.assertEqual(f.ledger.read_bytes(),b'')
 def test_changed_reference(self):
  with self.assertRaises(ValueError):self.f.adopt(dict(self.f.c1,sha256='0'*64))
 def test_unpinned_PASS(self):
  with self.assertRaises(ValueError):self.f.adopt(self.f.c1,self.f.add({'result':'PASS','authority':'Architect'}))
 def test_stale_grant(self):
  with self.assertRaises(ValueError):self.f.adopt(self.f.c1,self.f.g2)
 def test_qualification_not_production(self):
  f=Fixture('QUALIFICATION_BINDING');self.addCleanup(f.s.close)
  with self.assertRaises(ValueError):r.adopt(f.s,f.c1,f.g1)
  s=f.adopt()
  with self.assertRaises(ValueError):r.validate_invocation_runtime(f.s,f.binding(s),f.obj(f.r1)['root'])
 def test_interruption_boundaries(self):
  for count in (0,1,2,3):
   f=Fixture();self.addCleanup(f.s.close);calls=[0];original=r.append
   def cut(*args):
    if calls[0]==count:raise InterruptedError('fault injection')
    original(*args);calls[0]+=1
   with patch.object(r,'append',cut):
    try:f.adopt()
    except InterruptedError:pass
   s=r.recover(f.s);expected=f.r0 if count<2 else f.r1
   self.assertEqual(s['current_runtime'],f.obj(expected)['identity']);self.assertIsNone(s['pending'])
 def test_torn_journal(self):
  f=self.f;f.adopt();f.ledger.write_bytes(f.ledger.read_bytes()[:-1]);before=f.ledger.read_bytes()
  with self.assertRaisesRegex(ValueError,'INDETERMINATE'):r.recover(f.s)
  self.assertEqual(before,f.ledger.read_bytes())
 def test_reordered_journal(self):
  f=self.f;f.adopt();rows=f.ledger.read_bytes().splitlines(True);f.ledger.write_bytes(rows[1]+rows[0]+rows[2])
  with self.assertRaises(ValueError):r.reconstruct(f.s)
 def test_missing_history(self):
  f=self.f;f.adopt();f.ledger.write_bytes(b'\n'.join(f.ledger.read_bytes().splitlines()[1:])+b'\n')
  with self.assertRaises(ValueError):r.reconstruct(f.s)
 def test_changed_commit(self):
  f=self.f;f.adopt();rows=f.ledger.read_bytes().splitlines();v=json.loads(rows[1]);v['successor']='arbitrary';rows[1]=encoded(v);f.ledger.write_bytes(b'\n'.join(rows)+b'\n')
  with self.assertRaises(ValueError):r.recover(f.s)
 def test_historical_invocation_not_rebound(self):
  f=self.f;old=f.binding(r.reconstruct(f.s));f.adopt();self.assertEqual(old['runtime'],f.obj(f.r0)['identity'])
  with self.assertRaises(ValueError):r.validate_invocation_runtime(f.s,old,f.obj(f.r0)['root'])
 def test_release_context(self):
  f=self.f;s=f.adopt();ids=dict(f.ancestry);release=ids.pop('release_authority');r.production_identities(f.s,release,ids,f.binding(s))
  with self.assertRaises(ValueError):r.production_identities(f.s,'wrong',ids,f.binding(s))
 def test_runtime_source_still_guarded(self):
  f=self.f;s=f.adopt()
  with self.assertRaisesRegex(ValueError,'unaccounted runtime'):r.validate_invocation_runtime(f.s,f.binding(s),f.obj(f.r0)['root'])
 def test_unknown_event(self):
  f=self.f;f.adopt();rows=f.ledger.read_bytes().splitlines();v=json.loads(rows[0]);v.pop('id');v['event']='PASS';rows[0]=encoded(r.seal('RUNTIME-ADOPTION-EVENT',v));f.ledger.write_bytes(b'\n'.join(rows)+b'\n')
  with self.assertRaises(ValueError):r.recover(f.s)

class FrozenIntegrationTests(unittest.TestCase):
 def test_schema8_remains_qualification_only(self):
  prior=O.parent/'run2_control_plane_binding_2026-09-18/candidate/adapter/control_plane_binding.py'
  self.assertEqual(prior.read_bytes(),(O/'candidate/adapter/control_plane_binding.py').read_bytes())

if __name__=='__main__':unittest.main(verbosity=2)
