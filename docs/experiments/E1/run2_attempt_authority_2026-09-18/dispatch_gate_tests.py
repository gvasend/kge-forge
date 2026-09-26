"""Synthetic dispatch-entry boundary probes, never E1 identities."""
import json,tempfile,unittest
from pathlib import Path
from contextlib import nullcontext
from types import SimpleNamespace
from unittest.mock import patch
from adapter.context_projection import canonical
from adapter.controlled_dispatch import dispatch
from adapter.authorization_lifecycle import LifecycleDenied
from adapter.run_control import E1_POLICY
class Gate(unittest.TestCase):
 def test_no_telemetry_before_valid_issuance_even_if_private_selection_is_issued(self):
  for initial in (b'',b'{"event":"activity"}\n'):
   with self.subTest(initial=initial),tempfile.TemporaryDirectory(prefix='synthetic-dispatch-gate-') as root:
    audit=Path(root)/'audit';audit.write_bytes(initial)
    raw={'operational_binding':canonical({'governance':{'schema':5}}),'model_transmission':canonical({'run_control':E1_POLICY}),
      'session_id':'synthetic-session','turn_id':'synthetic-turn','work_package_id':'synthetic-task'}
    store=SimpleNamespace(session=nullcontext,resolve=lambda _:canonical(raw).encode(),state_path=lambda _:audit)
    auth=SimpleNamespace(authorization_id='synthetic-unissued')
    with patch('adapter.attempt_context.selected',return_value={'mode':'ISSUED'}),patch('adapter.controlled_dispatch.reconstruct_authorization',return_value=auth),patch('adapter.controlled_dispatch.ResponsesReasoning') as model:
     with self.assertRaises(LifecycleDenied):dispatch(store,'synthetic-unissued')
     model.assert_not_called()
    self.assertEqual(audit.read_bytes(),initial)
 def test_schema5_specific_authorization_and_durable_issuance_are_separate_checks(self):
  from adapter.invocation_issuance import issue_inactive
  # Exercise the schema5 branch without issuing even a synthetic authorization:
  # the existing durable-issuance checker is reached after the synthetic host stub.
  with tempfile.TemporaryDirectory(prefix='synthetic-issuance-gate-') as root:
   audit=Path(root)/'audit';auth=SimpleNamespace(operational_binding=canonical({'governance':{'schema':5}}),
    state='INACTIVE',ownership_ledger=str(Path(root)/'ledger'),context_binding=SimpleNamespace(governance=SimpleNamespace(run5={'amendment':{'proposal':{}}})))
   import os
   fence=os.open(root,os.O_RDONLY)
   owner=SimpleNamespace(_locked=lambda:os.open(root,os.O_RDONLY),_history=lambda _:None)
   with patch('adapter.attempt_context.require_issued') as specific,patch('adapter.invocation_attempt.require_claim'),patch('adapter.invocation_issuance._lease',return_value=fence),patch('adapter.invocation_issuance.InvocationOwnership',return_value=owner),patch('adapter.invocation_issuance.invocation',return_value=None),patch('adapter.invocation_issuance.dispatch_binding'),patch('adapter.invocation_issuance.GovernedHost'),patch('adapter.invocation_issuance.require_issued',side_effect=LifecycleDenied('synthetic missing original issuance')) as durable:
    with self.assertRaisesRegex(LifecycleDenied,'synthetic missing original issuance'):issue_inactive(auth,audit,{})
    specific.assert_called_once_with(auth);durable.assert_called_once_with(auth,audit)
   self.assertFalse(audit.exists())
if __name__=='__main__':unittest.main(verbosity=2)
