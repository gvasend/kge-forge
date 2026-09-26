"""Non-authorizing tests: reuse only parsed pinned catalogs, never a verdict."""
import json,sys,tempfile,unittest,os,copy
from pathlib import Path
from unittest.mock import patch
O=Path(__file__).parent;sys.path.insert(0,str(O/'candidate'))
from adapter.controller_authority_store import ControllerAuthorityStore,AuthorityDenied,encoded,sha,outside,outside_many
from adapter.history_catalogs import historical_store,reuse_history_catalogs,_history_stores
from adapter.attempt_chain import ancestry

class Reuse(unittest.TestCase):
 def setUp(self):
  self.t=tempfile.TemporaryDirectory(prefix='history-catalog-test-');self.root=Path(self.t.name)
  self.grant=self.root/'grant';self.grant.mkdir();self.state=self.root/'state';self.state.mkdir()
  self.b=encoded({'history':['r8','r9','r10'],'disposition':'CANCELLED','effects':0});self.h=sha(self.b);self.id='sha256:'+self.h
  s=ControllerAuthorityStore.materialize(self.root/'store',{self.id:{'bytes':self.b,'evidence':[]}}, {},{'authority_source':{'sha256':'0'*64},'release_identities':{'ReleaseBasisId':'fixture','ReleaseDecisionId':'fixture'}},{'authorization_id':'synthetic'},[str(self.grant)],{'audit':{'path':str(self.state/'audit'),'mutation':'APPEND_ONLY','mechanism':'typed fixture'}})
  self.conf={'root':str(s.root),'catalog_sha256':s.catalog_sha256,'applicability':s.applicability};s.close()
 def tearDown(self):self.t.cleanup()
 def read(self):
  with historical_store(self.conf) as s:
   s.verify_immutable_witness({self.id:self.h});return s.resolve(self.id)
 def test_equal_full_cold_and_reused_bytes(self):
  cold=self.read()
  @reuse_history_catalogs
  def f():return [self.read() for _ in range(3)]
  self.assertEqual(f(),[cold]*3);self.assertIsNone(_history_stores.get())
 def test_single_parse_multiple_fresh_catalog_and_object_reads(self):
  import adapter.controller_authority_store as m
  calls=[];original=m._read
  def read(fd,n):calls.append(n);return original(fd,n)
  @reuse_history_catalogs
  def f():
   for _ in range(3):self.read()
   self.assertEqual(len(_history_stores.get()),1)
  with patch.object(m,'_read',side_effect=read):f()
  self.assertGreaterEqual(calls.count('catalog.json'),6);self.assertGreaterEqual(calls.count(self.h),6)
 def test_historical_bytes_missing_or_substituted_between_borrows(self):
  for value in (None,b'changed history',encoded({'history':['r9','r8','r10']}),encoded({'disposition':'COMPLETED'}),encoded({'effects':1}),encoded({'ownership':'HELD'}),encoded({'release':'different','dispatch':'different'})):
   (self.root/'store'/self.h).write_bytes(self.b);(self.root/'store'/self.h).chmod(0o600)
   @reuse_history_catalogs
   def f():
    self.read()
    p=self.root/'store'/self.h
    if value is None:p.unlink()
    else:p.write_bytes(value)
    with self.assertRaises((ValueError,OSError)):self.read()
   f()
 def test_stale_catalog_between_borrows(self):
  @reuse_history_catalogs
  def f():
   self.read();(self.root/'store/catalog.json').write_bytes(b'{}')
   with self.assertRaises(ValueError):self.read()
  f()
 def test_changed_grant_is_fresh(self):
  @reuse_history_catalogs
  def f():
   self.read();self.grant.rmdir();self.grant.symlink_to(self.root/'store',target_is_directory=True)
   with self.assertRaises(ValueError):self.read()
  f()
 def test_changed_private_state_placement_is_fresh(self):
  @reuse_history_catalogs
  def f():
   self.read();self.state.rmdir();self.state.symlink_to(self.grant,target_is_directory=True)
   with self.assertRaises(ValueError):self.read()
  f()
 def test_unknown_head_cannot_be_authorized(self):
  @reuse_history_catalogs
  def f():
   self.read()
   with historical_store(self.conf) as s:
    with self.assertRaises(ValueError):s.resolve('arbitrary-r12')
  f()
 def test_permission_change_is_fresh(self):
  @reuse_history_catalogs
  def f():
   self.read();(self.root/'store'/self.h).chmod(0o644)
   with self.assertRaises(ValueError):self.read()
  f()
 def test_no_nested_operation_or_session(self):
  @reuse_history_catalogs
  def f():
   with self.assertRaises(ValueError):f()
   with historical_store(self.conf) as s:
    with s.session():
     with self.assertRaises(ValueError):
      with s.session():pass
  f()
 def test_cleanup_failure_and_next_operation_cold(self):
  held=[]
  @reuse_history_catalogs
  def f():
   with historical_store(self.conf) as s:held.append(s)
   raise RuntimeError('fixture interruption')
  with self.assertRaises(RuntimeError):f()
  self.assertIsNone(_history_stores.get());self.assertIsNone(held[0].fd)
  self.assertEqual(self.read(),self.b)
 def test_fresh_authority_selection_key(self):
  @reuse_history_catalogs
  def f():
   self.read();conf=copy.deepcopy(self.conf);conf['applicability']['authorization_id']='another'
   with self.assertRaises(ValueError):
    with historical_store(conf):pass
  f()
 def test_placement_equivalence(self):
  def old(path,roots):
   p=Path(path)
   if not p.is_absolute() or p.resolve()!=p:raise ValueError()
   for raw in roots:
    root=Path(raw).resolve()
    if p==root or root in p.parents or p in root.parents:raise ValueError()
  def accepts(fn,path,roots):
   try:fn(path,roots);return True
   except ValueError:return False
  paths=[self.root,self.root/'store',self.root/'store/object',self.grant,self.grant/'absent','relative','/']
  roots=[[],[str(self.grant)],[str(self.root)],[str(self.root/'store/object')],['/']]
  for p in paths:
   for r in roots:self.assertEqual(accepts(old,p,r),accepts(outside,p,r),(p,r))

class Actual(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.proof=json.loads((O/'R10_AUTHENTICATED_CAPTURE.json').read_bytes());cls.p=json.loads((O/'PROPOSED_R11_BINDING.json').read_bytes())
 def test_complete_exact_history_and_new_head(self):
  self.assertEqual(len(self.p['predecessors']),3)
  @reuse_history_catalogs
  def f():return ancestry(self.proof,self.p)
  self.assertEqual(f(),ancestry(self.proof,self.p));self.assertFalse(f()['handoff_eligible'])
 def test_reorder_missing_substitution(self):
  for records in (self.p['predecessors'][::-1],self.p['predecessors'][:-1],[dict(x,authorization_id='substitution') for x in self.p['predecessors']]):
   p=copy.deepcopy(self.p);p['predecessors']=records
   with self.assertRaises(ValueError):ancestry(self.proof,p)
 def test_mutable_owner_scope_fresh_between_calls(self):
  @reuse_history_catalogs
  def f():
   ancestry(self.proof,self.p)
   with patch('adapter.attempt_chain.observe',return_value=({'authorization_id':'unknown'},None,b'')):
    with self.assertRaises(ValueError):ancestry(self.proof,self.p)
   with patch('adapter.attempt_chain.observe',return_value=(None,{'authorization_id':'unknown'},b'')):
    with self.assertRaises(ValueError):ancestry(self.proof,self.p)
  f()
 def test_evidence_identity_changes_for_each_byte(self):
  b=(O/'R10_AUTHENTICATED_CAPTURE.json').read_bytes()
  for i in (0,len(b)//2,len(b)-1):self.assertNotEqual(sha(b),sha(b[:i]+bytes([b[i]^1])+b[i+1:]))

if __name__=='__main__':unittest.main(verbosity=2)
