"""Isolated intentionally red F03 candidate; not part of default test discovery.

Run explicitly: python3 -m unittest adapter.tests.counterexamples.c06_f03_candidate -v
No implementation/E1 mutation. Synthetic receipt is the existing case-N setup;
only the required source invalidation differs between the paired states.
"""
from dataclasses import replace
import hashlib
import json
from pathlib import Path
import unittest

from adapter.planner import codec as c, core, model as m, replay
from adapter.tests.test_planner_e1_replay import synthetic_receipt, external_event

ROOT = Path(__file__).resolve().parents[3]


class F03OperationalCounterexample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bundle = replay.import_e1(ROOT / 'docs/experiments/E1/E1_RESUME_MANIFEST_1.json', ROOT)
        plan = json.loads((ROOT / 'docs/experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_PLAN_1.json').read_text())
        cls.action = m.ActionId('FACT-BUDGET-APPLICABILITY')
        spec = next(a for a in plan['resolution_actions'] if a['id'] == cls.action.value)
        required = next(k for k in spec['knowledge_requirements'] if k['action'] == 'REEVAL-BUDGET')
        assert required['required_recorded_outcome'] == 'BLOCKED'
        cls.source = required['evidence']
        raw = (ROOT / cls.source['path']).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == cls.source['sha256']
        cls.identity = m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY,
            'raw-file-sha256', cls.source['sha256'])
        assert any(p.identity == cls.identity and p.path == cls.source['path'] for p in cls.bundle.sources)
        state, entity = synthetic_receipt(cls.bundle.current)
        for stage in (m.ExternalStage.EVIDENCE_RECEIVED, m.ExternalStage.EVIDENCE_VALIDATED,
                      m.ExternalStage.DEPENDENT_ACTION_REENTRY):
            state = core.apply_receipt(state, external_event(state, stage,
                entity.id if stage is m.ExternalStage.EVIDENCE_RECEIVED else None)).snapshot
        cls.ready = state

    def test_valid_receipt_setup_and_empty_pass_guard(self):
        before = core.recompute(self.ready)
        self.assertIn(self.action, before.actionable)
        self.assertEqual(before.selection.selected, self.action)
        self.assertEqual(before.control, m.ControlState.RUNNABLE)
        with self.assertRaisesRegex(m.PlannerError, 'no accepted bounded result contract'):
            core.apply_result(self.ready, m.SuppliedResult(self.action, m.ActionResult.PASS, (),
                                                         c.snapshot_id(self.ready)))

    def test_required_nonpass_knowledge_source_invalidation_blocks_selection(self):
        # GIVEN the imported action requires accepted REEVAL-BUDGET BLOCKED knowledge
        # and the independent external receipt gate has legitimately passed in replay;
        # WHEN that exact required source identity is invalidated, then cold-decoded;
        # THEN the dependent action must no longer be actionable or selected.
        # MUST NOT use the historical action-status summary as current knowledge proof.
        changed = c.invalidate_sources(self.ready, (self.identity,))
        restored = c.decode_snapshot(c.snapshot_bytes(changed))
        result = core.recompute(restored)
        print('F03_OBSERVATION', json.dumps({
            'invalidated_source': self.source['path'], 'sha256': self.identity.sha256,
            'same_snapshot_identity': c.snapshot_id(self.ready) == c.snapshot_id(changed),
            'actionable': [a.value for a in result.actionable],
            'selected': result.selection.selected.value if result.selection else None,
            'control': result.control.value,
        }, sort_keys=True), flush=True)
        self.assertNotIn(self.action, result.actionable,
            'required accepted non-PASS source was invalidated but imported action remains actionable')
        self.assertTrue(result.selection is None or result.selection.selected != self.action)

    def test_unrelated_invalidation_does_not_blanket_block(self):
        changed = c.invalidate_sources(self.ready, (replace(self.identity, sha256='f'*64),))
        self.assertEqual(core.recompute(changed), core.recompute(self.ready))

    def test_represented_action_source_invalidation_still_blocks(self):
        action = next(a for a in self.ready.actions if a.id == self.action)
        changed = c.invalidate_sources(self.ready, (action.source.identity,))
        self.assertNotIn(self.action, core.recompute(changed).actionable)
