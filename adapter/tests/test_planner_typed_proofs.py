"""E06 generic contract, persistence, invalidation and reevaluation qualification."""
from dataclasses import replace
from pathlib import Path
import tempfile
import unittest
from adapter.planner import model as m, codec as c
from adapter.planner.core import apply_event, recompute, evaluate_satisfaction
from adapter.planner import typed_proofs as t

ZERO = m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY, 'placeholder', '0'*64)


def fixture(scope='QUALIFICATION', lineage='fixture-v1'):
    raw = b'generic independently reviewed fixture'
    pin = c._identity(raw, 'raw-file-sha256')
    provenance = m.Provenance('source.json', pin, '/', raw.decode(), 'QUALIFICATION_CONTRACT', scope)
    ctx = m.EvaluationContext(scope, lineage, '1', 0, (m.EffectClass.NON_EFFECTING,))
    authority = m.GraphEntity(m.EntityId('fixture-authority'), m.EntityKind.AUTHORITY, pin, provenance, scope, lineage, '1', 100, permissions=(m.AuthorityClass.DECIDE,))
    k = m.KnowledgeRecord(m.KnowledgeId('knowledge'), m.KnowledgeState.KNOWN_COMPLETE, 'bounded result', provenance)
    root = m.RootCondition(m.ConditionId('root'), m.ConditionState.UNRESOLVED)
    slot = m.ValueSlot(m.SlotId('slot'), m.SlotState.UNRESOLVED, m.ValueType.NON_IDENTITY_VALUE)
    action = m.Action(m.ActionId('dependent'), m.OperationClass.DETERMINISTIC_MAPPING, m.EffectClass.NON_EFFECTING, (m.Gate(m.GateKind.CONDITION_SATISFIED, root.id),), provenance, (), blocked_terminal=False)
    unrelated = replace(action, id=m.ActionId('unrelated'), prerequisites=(), blocked_terminal=False)
    s = m.Snapshot((action, unrelated), (m.ActionStatus(action.id, m.ActionState.BLOCKED), m.ActionStatus(unrelated.id, m.ActionState.BLOCKED)), (root,), (slot,), (k,), entities=(authority,), context=ctx)
    contract = m.TypedProofContract(ZERO, m.TypedProofKind.SLOT_PROOF, 'bounded slot proposition', slot.id, (k.id,), (t.support_identity(s, k.id),), scope, lineage, '1', 100, authority.id, authority.identity, provenance)
    contract = replace(contract, id=t.identity(contract))
    return replace(s, proof_contracts=(contract,))


def candidate(contract):
    p = m.TypedProof(ZERO, contract.id, contract.proof_type, contract.proposition, contract.target, contract.supports, contract.support_identities, contract.scope, contract.lineage, contract.generation, contract.valid_until, contract.authority, contract.authority_identity, contract.provenance)
    return replace(p, id=t.identity(p))


def admit(s, p):
    return apply_event(s, m.TypedProofAdmission(p, c.snapshot_id(s))).snapshot


def root_contract(s):
    base = s.proof_contracts[0]
    x = replace(base, proof_type=m.TypedProofKind.ROOT_PROOF, proposition='independent root proposition', target=s.roots[0].id, supports=(s.slots[0].id,), support_identities=(t.support_identity(s, s.slots[0].id),))
    return replace(x, id=t.identity(x))


def lifecycle():
    s = fixture()
    p = candidate(s.proof_contracts[0])
    slot = admit(s, p)
    rc = root_contract(slot)
    # Root definition is independently reviewed before admitting its proof.
    start = replace(s, proof_contracts=s.proof_contracts + (rc,))
    slot = admit(start, p)
    root = admit(slot, candidate(rc))
    return start, slot, root


class TypedProofTests(unittest.TestCase):
    def test_positive_and_invalidation(self):
        start, slot, root = lifecycle()
        self.assertEqual(slot.slots[0].state, m.SlotState.RESOLVED)
        self.assertEqual(slot.roots[0].state, m.ConditionState.UNRESOLVED)
        self.assertNotIn(m.ActionId('dependent'), recompute(slot).actionable)
        self.assertEqual(root.roots[0].state, m.ConditionState.SATISFIED)
        self.assertIn(m.ActionId('dependent'), recompute(root).actionable)
        self.assertEqual(root.reevaluations[-1].old_state, m.ActionState.BLOCKED)
        self.assertEqual(dict((s.id, s.state) for s in root.statuses)[m.ActionId('unrelated')], m.ActionState.BLOCKED)
        terminal_contract = replace(root, actions=tuple(replace(a, blocked_terminal=True) for a in root.actions))
        terminal_withdrawn = apply_event(terminal_contract, m.ProofDependencyChange((root.knowledge[0].id,), c.snapshot_id(terminal_contract), root.knowledge[0].provenance)).snapshot
        self.assertEqual(next(s.state for s in terminal_withdrawn.statuses if s.id == m.ActionId('dependent')), m.ActionState.BLOCKED)
        for dependency in (root.knowledge[0].id, root.slots[0].id, root.roots[0].id, root.entities[0].id, root.typed_proofs[0].id, root.proof_contracts[0].id):
            with self.subTest(dependency=dependency):
                after = apply_event(root, m.ProofDependencyChange((dependency,), c.snapshot_id(root), root.knowledge[0].provenance)).snapshot
                self.assertEqual(after.roots[0].state, m.ConditionState.UNRESOLVED)
                self.assertNotIn(m.ActionId('dependent'), recompute(after).actionable)
                self.assertEqual(len(after.typed_proofs), 2)

    def test_fail_closed_atomic_and_idempotent(self):
        start, slot, root = lifecycle()
        p = candidate(start.proof_contracts[0])
        for change in ({'proposition':'wrong'}, {'proof_type':m.TypedProofKind.ROOT_PROOF}, {'target':m.SlotId('wrong')}, {'scope':'wrong'}, {'lineage':'wrong'}, {'generation':'wrong'}, {'valid_until':-1}, {'authority':m.EntityId('wrong')}, {'supports':(m.KnowledgeId('wrong'),)}, {'support_identities':(ZERO,)}, {'validation':m.ValidationState.STALE}, {'provenance':replace(p.provenance, scope='wrong')}):
            with self.subTest(change=change):
                invalid = replace(p, **change); invalid = replace(invalid, id=t.identity(invalid))
                before = c.snapshot_bytes(start)
                with self.assertRaises(m.PlannerError): admit(start, invalid)
                self.assertEqual(c.snapshot_bytes(start), before)
        self.assertEqual(admit(slot, p), slot)
        self.assertEqual(t.reevaluate(root, root, (p.id,), p.provenance), root)
        with self.assertRaises(m.PlannerError):
            admit(start, candidate(start.proof_contracts[1]))
        for change in ({'tick':101}, {'scope':'wrong'}, {'lineage':'wrong'}, {'generation':'wrong'}):
            stale = replace(root, context=replace(root.context, **change))
            self.assertNotIn(m.ActionId('dependent'), recompute(t.reevaluate(root, stale, (p.id,), p.provenance)).actionable)

    def test_terminal_failure_and_other_prerequisite(self):
        start, slot, root = lifecycle()
        failed = replace(slot, statuses=tuple(replace(s, terminal_failure=True) if s.id == m.ActionId('dependent') else s for s in slot.statuses))
        self.assertNotIn(m.ActionId('dependent'), recompute(admit(failed, candidate(slot.proof_contracts[1]))).actionable)
        invalidated = apply_event(failed, m.SourceInvalidation((failed.knowledge[0].provenance.identity,), c.snapshot_id(failed))).snapshot
        self.assertTrue(next(s for s in invalidated.statuses if s.id == m.ActionId('dependent')).terminal_failure)
        held = replace(slot, actions=tuple(replace(a, requirements=(m.PredicateId('missing'),)) if a.id == m.ActionId('dependent') else a for a in slot.actions), predicates=(m.Predicate(m.PredicateId('missing'), m.PredicateKind.UNSUPPORTED),))
        self.assertNotIn(m.ActionId('dependent'), recompute(admit(held, candidate(slot.proof_contracts[1]))).actionable)

    def test_source_invalidation_and_unrelated_admission(self):
        start, slot, root = lifecycle()
        after = apply_event(root, m.SourceInvalidation((root.knowledge[0].provenance.identity,), c.snapshot_id(root))).snapshot
        self.assertNotIn(m.ActionId('dependent'), recompute(after).actionable)
        self.assertEqual(after.roots[0].state, m.ConditionState.UNRESOLVED)
        self.assertEqual(t.affected_actions(start, (m.EntityId('unrelated-source'),)), set())

    def test_generic_explicit_reevaluation_without_typed_proofs(self):
        start = fixture()
        predicate = m.Predicate(m.PredicateId('accepted'), m.PredicateKind.KNOWLEDGE_ACCEPTED, knowledge=start.knowledge[0].id)
        start = replace(start, proof_contracts=(), slots=(), predicates=(predicate,), roots=(replace(start.roots[0], predicate=predicate.id),))
        event = m.ActionReevaluation((start.knowledge[0].id,), c.snapshot_id(start), start.knowledge[0].provenance)
        after = apply_event(start, event).snapshot
        self.assertIn(m.ActionId('dependent'), recompute(after).actionable)
        self.assertEqual(apply_event(after, replace(event, expected_snapshot=c.snapshot_id(after))).snapshot, after)
        with self.assertRaises(m.PlannerError):
            apply_event(start, replace(event, dependencies=(m.EntityId('unknown'),)))

    def test_authority_identity_substitution(self):
        start, slot, root = lifecycle()
        wrong_target = replace(slot, entities=tuple(replace(e, target=ZERO) for e in slot.entities))
        with self.assertRaises(m.PlannerError): admit(wrong_target, candidate(slot.proof_contracts[1]))
        changed = replace(slot, entities=tuple(replace(e, identity=ZERO) for e in slot.entities))
        with self.assertRaises(m.PlannerError): admit(changed, candidate(slot.proof_contracts[1]))
        after = apply_event(replace(root, entities=changed.entities), m.ActionReevaluation((root.entities[0].id,), c.snapshot_id(replace(root, entities=changed.entities)), root.knowledge[0].provenance)).snapshot
        self.assertNotIn(m.ActionId('dependent'), recompute(after).actionable)

    def test_unrelated_proof_and_reevaluation_failure_atomicity(self):
        start, slot, root = lifecycle()
        extra_slot = replace(start.slots[0], id=m.SlotId('other-slot'))
        extra_contract = replace(start.proof_contracts[0], target=extra_slot.id, proposition='other proposition')
        extra_contract = replace(extra_contract, id=t.identity(extra_contract))
        expanded = replace(start, slots=start.slots + (extra_slot,), proof_contracts=start.proof_contracts + (extra_contract,))
        after = admit(expanded, candidate(extra_contract))
        self.assertEqual(after.statuses, expanded.statuses)
        self.assertEqual(after.reevaluations, ())
        # A structurally admitted cyclic prerequisite graph must reject before
        # committing the otherwise-valid proof, preserving the immutable state.
        provenance = start.knowledge[0].provenance
        cycle = m.GraphAssertion(m.AssertionId('cycle'), provenance, relation=m.Relation.REQUIRES, subject=start.slots[0].id, object=start.slots[0].id, ordering_justification='invalid cycle')
        edge = m.GraphAssertion(m.AssertionId('edge'), provenance, relation=m.Relation.REQUIRES, subject=m.ActionId('dependent'), object=start.roots[0].id, ordering_justification='required root')
        broken = replace(start, assertions=(cycle, edge))
        before = c.snapshot_bytes(broken)
        with self.assertRaises(m.PlannerError): admit(broken, candidate(start.proof_contracts[0]))
        self.assertEqual(c.snapshot_bytes(broken), before)
        cross = replace(cycle, subject=start.slots[0].id, object=start.roots[0].id)
        implicit_cycle = replace(start, assertions=(cross, edge))
        self.assertIn('PREREQUISITE_CYCLE', recompute(implicit_cycle).defects)
        manually_resolved = replace(start, slots=tuple(replace(v, state=m.SlotState.RESOLVED) for v in start.slots))
        with self.assertRaises(m.PlannerError): admit(manually_resolved, candidate(start.proof_contracts[1]))

    def test_native_ledger_cold_restore_replay(self):
        start, slot, root = lifecycle()
        with tempfile.TemporaryDirectory() as directory:
            d = Path(directory)
            d.joinpath('source.json').write_bytes(b'generic independently reviewed fixture')
            # Use the current native P06 selection policy, pinned exactly.
            from adapter.planner.selector import POLICY_PIN
            policy = POLICY_PIN
            policy_path = Path(__file__).resolve().parents[2] / policy.path
            destination = d / policy.path
            destination.parent.mkdir(parents=True)
            destination.write_bytes(policy_path.read_bytes())
            source = m.ArtifactPin('source.json', start.knowledge[0].provenance.identity, m.HashProfile.RAW)
            bundle = m.PersistenceBundle(start, (), start, (source,), policy, 'E1-SELECTION-1-P06')
            command = m.TypedProofAdmission(candidate(start.proof_contracts[0]), c.snapshot_id(bundle.current))
            # Durable transaction rejection leaves no canonical head or proof.
            invalid = replace(command.proof, proposition='wrong')
            invalid = replace(invalid, id=t.identity(invalid))
            with self.assertRaises(m.PlannerError):
                c.commit_event(bundle, m.TypedProofAdmission(invalid, command.expected_snapshot), d/'rejected', d)
            self.assertFalse(any((d/'rejected').glob('bundle-*.json')))
            bundle, _ = c.commit_event(bundle, command, d/'committed', d)

            bundle = c.record_result(bundle, m.TypedProofAdmission(candidate(start.proof_contracts[1]), c.snapshot_id(bundle.current)))
            self.assertEqual(c.snapshot_id(bundle.current), c.snapshot_id(root))
            path, bid = c.save_bundle(bundle, d/'out', d)
            restored = c.restore(path, bid, d)
            self.assertEqual(c.snapshot_id(c._replay(restored)), c.snapshot_id(root))
            self.assertEqual(c.snapshot_bytes(c.decode_snapshot(c.snapshot_bytes(root))), c.snapshot_bytes(root))

if __name__ == '__main__': unittest.main()
