import copy,unittest
from adapter.terminal_attempt import classify
class Predecessors(unittest.TestCase):
 def setUp(self):
  self.a='synthetic-predecessor';self.rows=[{'event':'authorization_issued','authorization':{'state':'INACTIVE','authorization_id':self.a}},
   {'schema':'E1-RUN-CONTROL-1','event':'admission_closed','identity':{'authorization_id':self.a},'cycle':0},
   {'event':'authorization_lifecycle_terminal','resulting_state':'CANCELLED'}]
  self.life={'state':'CANCELLED','uncertain':False};self.actions={'scope':None,'incomplete':False,'results':{}}
 def call(self,rows=None,life=None,actions=None,owner=None,scope=None):return classify(self.rows if rows is None else rows,self.life if life is None else life,self.actions if actions is None else actions,owner,scope,self.a)
 def test_issued_INACTIVE_cancelled(self):self.assertEqual(self.call(),'ISSUED_INACTIVE_CANCELLED_NO_EFFECTS')
 def test_ACTIVE_cancelled(self):
  self.rows.insert(1,{'event':'authorization_lifecycle_activated'});self.assertEqual(self.call(),'ACTIVE_CANCELLED_PRE_MODEL_NO_EFFECTS')
 def test_unissued_not_accepted_by_terminal_mechanism(self):
  with self.assertRaises(ValueError):self.call(rows=self.rows[1:])
 def test_completed(self):
  with self.assertRaises(ValueError):self.call(life={'state':'COMPLETED','uncertain':False})
 def test_effecting_cancelled(self):
  with self.assertRaises(ValueError):self.call(actions={'scope':None,'incomplete':False,'results':{'action':'effect'}})
 def test_action_even_denied_rejected(self):
  self.rows.insert(1,{'event':'action_request'})
  with self.assertRaises(ValueError):self.call()
 def test_INDETERMINATE(self):
  with self.assertRaises(ValueError):self.call(life={'state':'INDETERMINATE','uncertain':True})
 def test_provider_request_uncertain(self):
  self.rows.insert(1,{'event':'model_request_content_bound'})
  with self.assertRaises(ValueError):self.call()
 def test_active_ownership(self):
  with self.assertRaises(ValueError):self.call(owner={'authorization_id':self.a})
 def test_surviving_scope(self):
  with self.assertRaises(ValueError):self.call(scope={'id':'scope-test'})
 def test_unknown_fact(self):
  self.rows.insert(1,{'event':'unknown'})
  with self.assertRaises(ValueError):self.call()
 def test_uncertainty_cannot_be_hidden_by_CANCELLED(self):
  with self.assertRaises(ValueError):self.call(life={'state':'CANCELLED','uncertain':True})
if __name__=='__main__':unittest.main(verbosity=2)
