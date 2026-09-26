"""Actual immutable identities; mutable candidate ownership simulated in memory only."""
import copy,json,sys,time,unittest
from pathlib import Path
from unittest.mock import patch
O=Path(__file__).parent;sys.path.insert(0,str(O/'candidate'))
from adapter.attempt_transition import terminal
from adapter.attempt_chain import ancestry,historical_capture,classify_terminal
from adapter.attempt_ownership import attribute
from adapter.terminal_attempt import classify
from adapter.context_projection import sha

class ActualIdentities(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.capture=json.loads((O/'R10_AUTHENTICATED_CAPTURE.json').read_bytes())
  cls.proposal=json.loads((O/'PROPOSED_R11_BINDING.json').read_bytes())
  cls.commit=json.loads((O.parent/'run2_r10_dispatch_2026-09-18/ACTIVE_COMMIT.json').read_bytes())
 def test_r10_existing_predicate_gap_exactly_identified(self):
  t=self.capture['terminal'];raw=Path(t['audit']).read_bytes();self.assertEqual(sha(raw),t['audit_sha256'])
  rows=[json.loads(x) for x in raw.splitlines()]
  self.assertEqual(rows[-1]['event'],'final_disposition');self.assertEqual(rows[-2]['event'],'authorization_lifecycle_terminal')
  self.assertEqual(rows[-1]['details']['terminal_event_id'],rows[-2]['event_id'])
  self.assertEqual(t['lifecycle']['state'],'CANCELLED');self.assertFalse(t['lifecycle']['uncertain'])
  with self.assertRaisesRegex(ValueError,'authoritative terminal fact must close predecessor'):
   classify(rows,t['lifecycle'],t['actions'],None,None,self.capture['authorization']['authorization_id'])
  # Prefix probe is diagnostic only; never replace the real immutable audit.
  self.assertEqual(classify(rows[:-1],t['lifecycle'],t['actions'],None,None,self.capture['authorization']['authorization_id']),'ACTIVE_CANCELLED_PRE_MODEL_NO_EFFECTS')
  self.assertEqual(Path(t['audit']).read_bytes(),raw)
 def test_captured_current_owner_no_longer_poisoning_terminal_predicate(self):
  r=self.capture['governance']['run6'];proof=copy.deepcopy(r['predecessor'])
  proof['terminal']['ownership']=self.commit['reservation']
  with patch('adapter.attempt_ownership.observe',return_value=(self.commit['reservation'],None,b'simulated snapshot')):
   terminal(None,r['amendment'],r['proposal'],proof)
  # Cancellation changes fresh mutable ownership; stale capture is no authority.
  with patch('adapter.attempt_ownership.observe',return_value=(None,None,b'simulated released snapshot')):
   terminal(None,r['amendment'],r['proposal'],proof)
 def test_exact_r11_attribution_and_all_ancestor_negatives(self):
  p=self.proposal;ids=[x['authorization_id'] for x in p['predecessors']]
  owner=dict(self.commit['reservation'],authorization_id=p['invocation_identity']['authorization_id'],session_id=p['invocation_identity']['session_id'],controller_audit=p['audit'])
  self.assertFalse(attribute(owner,None,ids,p['invocation_identity'],p['audit'])['handoff_eligible'])
  for identity in ids+['unknown','auth-arbitrary-alternative']:
   with self.subTest(identity=identity),self.assertRaises(ValueError):attribute(dict(owner,authorization_id=identity),None,ids,p['invocation_identity'],p['audit'])
 def test_proposed_material_policy_exact_ancestry(self):
  result=ancestry(self.capture,self.proposal)
  self.assertIsNone(result['current_ownership']);self.assertFalse(result['handoff_eligible'])
 def test_terminal_telemetry_suffix_negatives(self):
  t=self.capture['terminal'];rows=[json.loads(x) for x in Path(t['audit']).read_bytes().splitlines()]
  for k,v in [('terminal_event_id','wrong'),('ownership','HELD'),('uncertainty','unknown'),('provider_uncertainty','unknown')]:
   changed=copy.deepcopy(rows);changed[-1]['details'][k]=v
   with self.subTest(field=k),self.assertRaises(ValueError):classify_terminal(changed,t,self.capture['authorization']['authorization_id'])
  with self.assertRaises(ValueError):classify_terminal(rows+[rows[-1]],t,self.capture['authorization']['authorization_id'])
  for event in ('action_request','model_request_content_bound','unknown','authorization_lifecycle_activated'):
   with self.subTest(event=event),self.assertRaises(ValueError):classify_terminal(rows+[{'event':event}],t,self.capture['authorization']['authorization_id'])
 def test_reordered_or_missing_attempt_ancestry(self):
  for entries in (list(reversed(self.proposal['predecessors'])),self.proposal['predecessors'][:-1]):
   p=copy.deepcopy(self.proposal);p['predecessors']=entries
   with self.assertRaises(ValueError):ancestry(self.capture,p)
 def test_actual_namespace_unused(self):
  self.assertFalse(Path(self.proposal['audit']).exists())
  self.assertFalse(Path(self.proposal['audit']).parents[2].exists())
 def test_prior_evidence_and_shared_ledger_unchanged(self):
  baseline=json.loads((O/'HISTORICAL_BASELINE.json').read_bytes())
  for path,h in baseline.items():self.assertEqual(sha(Path(path).read_bytes()),h,path)

if __name__=='__main__':unittest.main(verbosity=2)
