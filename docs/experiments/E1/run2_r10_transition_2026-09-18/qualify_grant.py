import unittest
from unittest.mock import patch
from adapter.attempt_transition import verify_specific_grant
class Grant(unittest.TestCase):
 def setUp(self):
  self.e={'authority':'Architect','decision':'AUTHORIZE_EXACT_TERMINAL_ATTEMPT_ISSUANCE','proposal':{'authority_id':'synthetic-p','sha256':'p'},'amendment':'m','continuation':'c','release_authority':'r','OperationalContextId':'o','continuation_chain_digest':'d','predecessor':'a','automatic_retry':False}
  self.s={'mode':'ISSUED','specific_invocation_authorization':'g'};self.db={'g':dict(self.e,authority_source='source'),'source':dict(self.e,channel='user')}
 def test_exact_specific_grant(self):
  with patch('adapter.attempt_transition.read',side_effect=lambda r:self.db[r]):self.assertEqual(verify_specific_grant(self.s,self.e),self.db['g'])
 def test_prepared_and_missing_grant(self):
  for s in ({'mode':'PREPARED','specific_invocation_authorization':None},{'mode':'ISSUED','specific_invocation_authorization':None}):
   with self.assertRaises(ValueError):verify_specific_grant(s,self.e)
 def test_wrong_release_ancestry_proposal_predecessor(self):
  for k in ('proposal','amendment','continuation','release_authority','OperationalContextId','continuation_chain_digest','predecessor'):
   with self.subTest(k=k),patch('adapter.attempt_transition.read',side_effect=lambda r:self.db[r]):
    e=dict(self.e);e[k]='other'
    with self.assertRaises(ValueError):verify_specific_grant(self.s,e)
 def test_grant_is_not_self_attributing(self):
  self.db['source']['channel']='caller'
  with patch('adapter.attempt_transition.read',side_effect=lambda r:self.db[r]):
   with self.assertRaises(ValueError):verify_specific_grant(self.s,self.e)
if __name__=='__main__':unittest.main(verbosity=2)
