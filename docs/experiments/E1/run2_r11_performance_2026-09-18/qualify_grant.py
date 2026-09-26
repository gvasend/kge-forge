"""In-memory synthetic decisions only. No real Architect decision is fabricated."""
import sys,unittest,copy
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).parent/'candidate'))
from adapter import attempt_chain as chain

class SpecificGrant(unittest.TestCase):
 def setUp(self):
  self.g=SimpleNamespace(verify=lambda:None,spec={'amendment':'synthetic-amendment','continuation':'synthetic-continuation'},
   identities={'OperationalContextId':'synthetic-context','continuation_chain_digest':'synthetic-chain'},
   run7={'amendment':{'proposal':'synthetic-exact-proposal','controller_runtime':'synthetic-runtime'},
         'release_authority':'synthetic-release','proposal':{'predecessors':['synthetic-A','synthetic-B']}})
  self.auth=SimpleNamespace(context_binding=SimpleNamespace(governance=self.g))
  expected={'authority':'Architect','decision':'ADOPT_EXACT_ATTEMPT_CHAIN_AND_AUTHORIZE_SPECIFIC_INVOCATION',
   'proposal':'synthetic-exact-proposal','amendment':'synthetic-amendment','continuation':'synthetic-continuation',
   'release_authority':'synthetic-release',**self.g.identities,'predecessors':['synthetic-A','synthetic-B'],'automatic_retry':False}
  self.data={'synthetic-grant':dict(expected,authority_source='synthetic-source'),'synthetic-source':dict(expected,channel='user'),
   'synthetic-qualification':{'result':'PASS','amendment':'synthetic-amendment','controller_runtime':'synthetic-runtime','accepted_proposal':'synthetic-exact-proposal'}}
  self.selection={'mode':'ISSUED','specific_invocation_authorization':'synthetic-grant','qualification':'synthetic-qualification'}
 def call(self):
  with patch.object(chain,'selected',return_value=self.selection),patch.object(chain,'read',side_effect=self.data.__getitem__):
   return chain.require_issued(self.auth)
 def test_exact_synthetic_grant(self):self.assertEqual(self.call(),self.data['synthetic-grant'])
 def test_prepared_never_issues(self):
  self.selection['mode']='PREPARED'
  with self.assertRaises(ValueError):self.call()
 def test_missing_specific_authority(self):
  self.selection['specific_invocation_authorization']=None
  with self.assertRaises(ValueError):self.call()
 def test_alternate_successor_or_release(self):
  for field in ('proposal','release_authority','amendment','continuation','OperationalContextId','continuation_chain_digest','predecessors'):
   before=copy.deepcopy(self.data);self.data['synthetic-grant'][field]='substitute'
   with self.subTest(field=field),self.assertRaises(ValueError):self.call()
   self.data=before
 def test_missing_attributable_source(self):
  self.data['synthetic-source']['channel']='caller-assertion'
  with self.assertRaises(ValueError):self.call()
 def test_wrong_qualification(self):
  for field in ('result','amendment','controller_runtime','accepted_proposal'):
   before=copy.deepcopy(self.data);self.data['synthetic-qualification'][field]='wrong'
   with self.subTest(field=field),self.assertRaises(ValueError):self.call()
   self.data=before

if __name__=='__main__':unittest.main(verbosity=2)
