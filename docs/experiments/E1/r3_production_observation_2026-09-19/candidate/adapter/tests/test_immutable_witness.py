import json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from adapter.controller_authority_store import ControllerAuthorityStore,encoded,sha,AuthorityDenied

class WitnessTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(prefix='immutable-witness-test-');self.root=Path(self.tmp.name)
  self.grant=self.root/'grant';self.grant.mkdir()
  data=encoded({'immutable':'history'});self.h=sha(data);self.id='sha256:'+self.h
  self.s=ControllerAuthorityStore.materialize(self.root/'store',{self.id:{'bytes':data,'evidence':[]}}, {},
   {'authority_source':{'sha256':'0'*64},'release_identities':{'ReleaseBasisId':'fixture','ReleaseDecisionId':'fixture'}},
   {'authorization_id':'fixture'},[str(self.grant)])
  with self.s.witness() as seen:self.s.resolve(self.id)
  self.w=dict(seen)
 def tearDown(self):self.s.close();self.tmp.cleanup()
 def test_all_immutable_bytes_revalidated(self):
  self.s.verify_immutable_witness(self.w)
  (self.s.root/self.h).write_bytes(b'substitution')
  with self.assertRaises(AuthorityDenied):self.s.verify_immutable_witness(self.w)
 def test_fresh_grant_placement(self):
  self.grant.rmdir();self.grant.symlink_to(self.s.root,target_is_directory=True)
  with self.assertRaises(AuthorityDenied):self.s.verify_immutable_witness(self.w)
 def test_catalog_change_during_batch_rejected(self):
  import adapter.controller_authority_store as m
  original=m._read
  def read(fd,name):
   data=original(fd,name)
   if name==self.h:(self.s.root/'catalog.json').write_bytes(b'{}')
   return data
  with patch.object(m,'_read',side_effect=read):
   with self.assertRaises(AuthorityDenied):self.s.verify_immutable_witness(self.w)
 def test_missing_dependency_and_permissions(self):
  (self.s.root/self.h).chmod(0o644)
  with self.assertRaises(AuthorityDenied):self.s.verify_immutable_witness(self.w)
 def test_unknown_dependency(self):
  with self.assertRaises(AuthorityDenied):self.s.verify_immutable_witness({'absent':self.h})

if __name__=='__main__':unittest.main()
