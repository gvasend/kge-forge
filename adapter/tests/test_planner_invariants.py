"""P02 X10 plus typed persistence negatives; other domains remain deferred."""
from dataclasses import replace
import unittest

from adapter.planner import recompute, apply_result
from adapter.planner.codec import invalidate_sources, snapshot_bytes, decode_snapshot
from adapter.planner.model import (AssertionId, GraphAssertion, ValidationState, ConditionState,
                                  SlotState, PlannerError, ActionId, ActionState, IdentityKind)
from adapter.tests.test_planner_resume import fixture_bundle


class P02InvalidationTests(unittest.TestCase):
    def annotated_snapshot(self):
        fixture, bundle = fixture_bundle()
        source = fixture.snapshot.actions[0].source
        # Distinct independent source identity for the positive control.
        independent = replace(source, identity=replace(source.identity, sha256='f' * 64))
        a, b, c = (AssertionId(v) for v in ('source', 'derived', 'independent'))
        assertions = (GraphAssertion(a, source), GraphAssertion(b, independent, (a,)),
                      GraphAssertion(c, independent))
        snapshot = replace(bundle.initial, assertions=assertions,
            roots=tuple(replace(r, state=ConditionState.SATISFIED, evidence=(b,))
                        for r in bundle.initial.roots),
            slots=tuple(replace(s, state=SlotState.RESOLVED, evidence=(b,))
                        for s in bundle.initial.slots),
            actions=tuple(replace(action, source=independent, evidence=(b,))
                          if action.id == ActionId('S-CONTEXT') else action
                          for action in bundle.initial.actions),
            knowledge=(replace(fixture.supplied_result.knowledge[0], evidence=(b,)),))
        return snapshot, source, independent

    def test_x10_transitive_invalidation_and_independent_positive_control(self):
        # GIVEN accepted source->derived assertions with dependent proof/readiness;
        # WHEN source bytes/identity changes; THEN derived acceptance becomes STALE;
        # MUST NOT keep dependent readiness or invalidate independent assertions.
        snapshot, source, _ = self.annotated_snapshot()
        changed = invalidate_sources(snapshot, (source.identity,))
        states = {a.id.value: a.validation for a in changed.assertions}
        self.assertEqual(states, {'source': ValidationState.STALE,
                                 'derived': ValidationState.STALE,
                                 'independent': ValidationState.ACCEPTED})
        self.assertTrue(all(r.state is ConditionState.STALE for r in changed.roots))
        self.assertTrue(all(s.state is SlotState.STALE for s in changed.slots))
        self.assertEqual(changed.knowledge[0].validation, ValidationState.STALE)
        self.assertNotIn(ActionId('S-CONTEXT'), recompute(changed).actionable)
        self.assertEqual(snapshot.roots[0].state, ConditionState.SATISFIED)
        self.assertEqual(snapshot_bytes(changed), snapshot_bytes(decode_snapshot(snapshot_bytes(changed))))
        # No change is not an excuse to invalidate everything.
        self.assertEqual(invalidate_sources(snapshot, ()), snapshot)

    def test_silently_current_derived_state_cannot_be_loaded(self):
        snapshot, source, _ = self.annotated_snapshot()
        changed = invalidate_sources(snapshot, (source.identity,))
        bad = replace(changed, assertions=tuple(
            replace(a, validation=ValidationState.ACCEPTED) if a.id.value == 'derived' else a
            for a in changed.assertions))
        with self.assertRaises(PlannerError):
            snapshot_bytes(bad)
        with self.assertRaises(PlannerError):
            recompute(replace(changed, roots=tuple(
                replace(r, state=ConditionState.SATISFIED) for r in changed.roots)))

    def test_invalidation_is_permutation_invariant(self):
        snapshot, source, other = self.annotated_snapshot()
        reversed_snapshot = replace(snapshot, assertions=tuple(reversed(snapshot.assertions)))
        left = invalidate_sources(snapshot, (source.identity, other.identity))
        right = invalidate_sources(reversed_snapshot, (other.identity, source.identity))
        self.assertEqual(snapshot_bytes(left), snapshot_bytes(right))

    def test_stale_inventory_cannot_be_used_for_pass(self):
        fixture, _ = fixture_bundle()
        stale = invalidate_sources(fixture.snapshot, (fixture.snapshot.actions[0].source.identity,))
        with self.assertRaises(PlannerError):
            apply_result(stale, fixture.supplied_result)
        # Even if a caller clears a historical hold, stale contract cannot qualify.
        cleared = replace(stale, statuses=tuple(replace(s, state=ActionState.ACTION_ELIGIBLE)
                                                for s in stale.statuses))
        with self.assertRaises(PlannerError):
            apply_result(cleared, fixture.supplied_result)

    def test_unknown_assertion_references_fail_closed(self):
        fixture, _ = fixture_bundle()
        action = replace(fixture.snapshot.actions[0], evidence=(AssertionId('missing'),))
        with self.assertRaises(PlannerError):
            recompute(replace(fixture.snapshot, actions=(action,) + fixture.snapshot.actions[1:]))

    def test_wrong_identity_domain_cannot_trigger_invalidation(self):
        snapshot, source, _ = self.annotated_snapshot()
        with self.assertRaises(PlannerError):
            invalidate_sources(snapshot, (replace(source.identity, kind=IdentityKind.AUTHORITY_IDENTITY),))




# Explicit synthetic proof world: no facts/authorities are added to frozen E1.
def p03_proof_world():
    from adapter.planner import model as m
    fixture, bundle = fixture_bundle()
    source = fixture.snapshot.actions[0].source
    value_id = m.ArtifactIdentity(m.IdentityKind.CANONICAL_OBJECT_IDENTITY, 'TEST:object', 'a' * 64)
    def entity(name, kind, digit, **kwargs):
        identity = m.ArtifactIdentity(m.IdentityKind.AUTHORITY_IDENTITY if kind is m.EntityKind.AUTHORITY
            else m.IdentityKind.CONTENT_IDENTITY, 'TEST:' + name, digit * 64)
        return m.GraphEntity(m.EntityId(name), kind, identity, source, 'TEST', 'TEST-L', 'TEST-G', 10, **kwargs)
    value = replace(entity('value', m.EntityKind.VALUE, 'a'), identity=value_id)
    producer = entity('producer', m.EntityKind.PRODUCER, 'b')
    mapping = entity('mapping', m.EntityKind.MAPPING, 'c', target=value_id)
    authority = entity('authority', m.EntityKind.AUTHORITY, 'd', permissions=(m.AuthorityClass.CONSTRUCT,), target=value_id)
    validator = entity('validator', m.EntityKind.VALIDATOR, 'e', validator=m.ValidatorRule.PURE_IDENTITY_MATCH)
    def pred(name, kind, **kwargs):
        return m.Predicate(m.PredicateId(name), kind, **kwargs)
    predicates = (
        pred('source', m.PredicateKind.SOURCE_IDENTITY, entity=value.id, expected=value_id),
        pred('producer', m.PredicateKind.PRODUCER_AVAILABLE, entity=value.id, other=producer.id),
        pred('mapping', m.PredicateKind.MAPPING_AVAILABLE, entity=mapping.id),
        pred('authority', m.PredicateKind.AUTHORITY, entity=authority.id,
             permission=m.AuthorityClass.CONSTRUCT, expected=value_id),
        pred('validator', m.PredicateKind.CONSUMER_CHECK, entity=validator.id, other=value.id, expected=value_id),
        pred('known', m.PredicateKind.KNOWLEDGE_ACCEPTED, knowledge=fixture.supplied_result.knowledge[0].id),
    )
    root = m.RootCondition(m.ConditionId('TEST:inventory-contract'), m.ConditionState.UNRESOLVED,
                          predicate=m.PredicateId('known'))
    slot = m.ValueSlot(m.SlotId('TEST:value'), m.SlotState.UNRESOLVED, m.IdentityKind.CANONICAL_OBJECT_IDENTITY,
                      value=value.id, requirements=tuple(p.id for p in predicates[:5]), root_requirements=(root.id,))
    relation = m.GraphAssertion(m.AssertionId('TEST:producer'), source, relation=m.Relation.PRODUCED_BY,
                               subject=value.id, object=producer.id)
    state = replace(fixture.snapshot, roots=fixture.snapshot.roots + (root,), slots=fixture.snapshot.slots + (slot,),
        predicates=predicates, entities=(value, producer, mapping, authority, validator), assertions=(relation,),
        context=m.EvaluationContext('TEST', 'TEST-L', 'TEST-G', 1, (m.EffectClass.NON_EFFECTING,)))
    return fixture, replace(bundle, initial=state, current=state, policy_version='E1-SELECTION-1-P03')


class P03InvariantTests(unittest.TestCase):
    def proof(self, state, name):
        from adapter.planner.gates import evaluate_predicate
        from adapter.planner.model import PredicateId
        return evaluate_predicate(state, PredicateId(name))

    def test_positive_independent_root_and_slot_proof_not_pass_shortcut(self):
        # GIVEN explicit synthetic criteria; WHEN their evidence is complete;
        # THEN exactly TEST root/slot resolve; MUST NOT resolve E1's actual gaps.
        from adapter.planner import model as m
        from adapter.planner.core import evaluate_satisfaction
        from adapter.planner.codec import snapshot_id, record_result, bundle_bytes, save_bundle, restore
        import tempfile
        from adapter.tests.test_planner_resume import ROOT
        fixture, bundle = p03_proof_world()
        state = bundle.current
        self.assertEqual(evaluate_satisfaction(state).roots[-1].state, m.ConditionState.UNRESOLVED)
        supplied = replace(fixture.supplied_result, expected_snapshot=snapshot_id(state))
        result = apply_result(state, supplied)
        self.assertEqual(result.snapshot.roots[-1].state, m.ConditionState.SATISFIED)
        self.assertEqual(result.snapshot.slots[-1].state, m.SlotState.RESOLVED)
        self.assertEqual(result.snapshot.roots[0].state, m.ConditionState.UNRESOLVED)
        self.assertEqual(result.snapshot.slots[:2], state.slots[:2])
        persisted = record_result(bundle, supplied)
        with tempfile.TemporaryDirectory() as directory:
            path, identity = save_bundle(persisted, directory, ROOT)
            loaded = restore(path, identity, ROOT)
            self.assertEqual(bundle_bytes(loaded), bundle_bytes(persisted))
            self.assertEqual(recompute(loaded.current), recompute(persisted.current))
        with self.assertRaises(PlannerError):
            apply_result(state, fixture.supplied_result)  # Missing P03 pre-state pin.

    def test_x02_correspondence_not_ordering_and_true_cycles_fail_closed(self):
        from adapter.planner import model as m
        from adapter.planner.core import project
        fixture, bundle = p03_proof_world()
        a, b = bundle.current.actions[:2]
        def rel(id, subject, object, kind, why=''):
            return m.GraphAssertion(m.AssertionId(id), a.source, relation=kind,
                                    subject=subject, object=object, ordering_justification=why)
        semantic = (rel('ab', a.id, b.id, m.Relation.CORRESPONDS_TO), rel('ba', b.id, a.id, m.Relation.BINDS))
        state = replace(fixture.snapshot, assertions=semantic)
        self.assertEqual(project(state).defects, ())
        self.assertNotIn((a.id, b.id), project(state).edges)
        cyclic = tuple(replace(r, relation=m.Relation.REQUIRES, ordering_justification='TEST:explicit') for r in semantic)
        result = recompute(replace(fixture.snapshot, assertions=cyclic))
        self.assertIn('PREREQUISITE_CYCLE', result.defects)
        self.assertIsNone(result.selection)
        self.assertTrue(any('METADATA_MISMATCH' in d for d in result.defects))
        wrong = replace(semantic[0], ordering_justification='not allowed')
        self.assertIn('NON_ORDERING_RELATION:ab', project(replace(state, assertions=(wrong,))).defects)

    def test_x03_exact_permission_scope_target_and_replay(self):
        from adapter.planner import model as m
        _, bundle = p03_proof_world(); state = bundle.current
        self.assertEqual(self.proof(state, 'authority').state, m.ProofState.PROVED)
        for permission in (m.AuthorityClass.ISSUE, m.AuthorityClass.USE, m.AuthorityClass.RELEASE, m.AuthorityClass.EXPAND):
            predicates = tuple(replace(p, permission=permission) if p.id.value == 'authority' else p for p in state.predicates)
            self.assertEqual(self.proof(replace(state, predicates=predicates), 'authority').state, m.ProofState.DISPROVED)
        for updates in ({'consumed': True}, {'scope': 'OTHER'}, {'lineage': 'OLD'}, {'generation': 'OLD'}, {'valid_until': 0}):
            entities = tuple(replace(e, **updates) if e.kind is m.EntityKind.AUTHORITY else e for e in state.entities)
            self.assertEqual(self.proof(replace(state, entities=entities), 'authority').state, m.ProofState.DISPROVED)

    def test_x05_missing_fact_cannot_be_replaced_by_authority_choice(self):
        # This tests the pure completeness predicate, not P04's decision lifecycle.
        from adapter.planner import model as m
        _, bundle = p03_proof_world(); state = bundle.current
        missing = m.Predicate(m.PredicateId('missing-owner'), m.PredicateKind.SOURCE_IDENTITY,
                              unavailable='Authoritative owning source not established')
        dossier = m.Predicate(m.PredicateId('dossier'), m.PredicateKind.DOSSIER_COMPLETE,
                              operands=(missing.id, m.PredicateId('authority')))
        state = replace(state, predicates=state.predicates + (missing, dossier))
        self.assertEqual(self.proof(state, 'authority').state, m.ProofState.PROVED)
        self.assertEqual(self.proof(state, 'dossier').state, m.ProofState.UNKNOWN)
        with self.assertRaises(m.PlannerError):
            self.proof(replace(state, predicates=state.predicates[:-1] +
                (replace(dossier, operands=()),)), 'dossier')

    def test_x06_missing_producer_is_not_inferred(self):
        from adapter.planner import model as m
        _, bundle = p03_proof_world(); state = bundle.current
        self.assertEqual(self.proof(state, 'producer').state, m.ProofState.PROVED)
        missing = replace(state, assertions=())
        self.assertEqual(self.proof(missing, 'producer').state, m.ProofState.UNKNOWN)
        nearby = replace(state.assertions[0], relation=m.Relation.CORRESPONDS_TO)
        self.assertEqual(self.proof(replace(state, assertions=(nearby,)), 'producer').state, m.ProofState.UNKNOWN)

    def test_x08_placeholders_do_not_satisfy_evidence(self):
        from adapter.planner import model as m
        _, bundle = p03_proof_world(); state = bundle.current
        evidence = replace(state.entities[0], kind=m.EntityKind.EVIDENCE)
        predicate = m.Predicate(m.PredicateId('proof'), m.PredicateKind.EVIDENCE, entity=evidence.id)
        state = replace(state, entities=(evidence,) + state.entities[1:], predicates=state.predicates + (predicate,))
        self.assertEqual(self.proof(state, 'proof').state, m.ProofState.PROVED)
        for updates in ({'produced': False}, {'validated': False}, {'validation': m.ValidationState.STALE}):
            self.assertNotEqual(self.proof(replace(state, entities=(replace(evidence, **updates),) +
                state.entities[1:]), 'proof').state, m.ProofState.PROVED)

    def test_x09_effecting_validator_never_runs_or_grants_authority(self):
        from adapter.planner import model as m
        from unittest.mock import patch
        _, bundle = p03_proof_world(); state = bundle.current
        self.assertEqual(self.proof(state, 'validator').state, m.ProofState.PROVED)
        bad = replace(state, entities=tuple(replace(e, validator=m.ValidatorRule.EFFECTING_ONLY)
            if e.kind is m.EntityKind.VALIDATOR else e for e in state.entities))
        with patch('builtins.open', side_effect=AssertionError('effect')), \
                patch('socket.socket', side_effect=AssertionError('network')):
            self.assertEqual(self.proof(bad, 'validator').state, m.ProofState.UNKNOWN)
            self.assertEqual(state, bundle.current)
        # A pure validator PASS has no effect authority. A missing operation grant blocks.
        action = replace(state.actions[0], effect=m.EffectClass.PRODUCTION_EFFECT,
                         requirements=(m.PredicateId('validator'),))
        self.assertNotIn(action.id, recompute(replace(state, actions=(action,) + state.actions[1:])).actionable)

    def test_x11_hash_syntax_cannot_substitute_identity_types(self):
        from adapter.planner import model as m
        _, bundle = p03_proof_world(); state = bundle.current
        self.assertEqual(self.proof(state, 'source').state, m.ProofState.PROVED)
        for kind in m.IdentityKind:
            if kind is m.IdentityKind.CANONICAL_OBJECT_IDENTITY:
                continue
            value = replace(state.entities[0], identity=replace(state.entities[0].identity, kind=kind))
            self.assertEqual(self.proof(replace(state, entities=(value,) + state.entities[1:]), 'source').state,
                             m.ProofState.DISPROVED)
        value = replace(state.entities[0], identity=replace(state.entities[0].identity, namespace='another-owner'))
        self.assertEqual(self.proof(replace(state, entities=(value,) + state.entities[1:]), 'source').state,
                         m.ProofState.DISPROVED)

    def test_slots_require_all_value_bound_contracts_even_under_any(self):
        from adapter.planner import model as m
        from adapter.planner.core import evaluate_satisfaction
        _, bundle = p03_proof_world(); state = bundle.current
        state = replace(state, knowledge=state.actions[0].accepted_inventory)
        self.assertEqual(evaluate_satisfaction(state).slots[-1].state, m.SlotState.RESOLVED)
        for name in ('source', 'producer', 'mapping', 'authority', 'validator'):
            reduced = replace(state, slots=state.slots[:-1] + (replace(state.slots[-1],
                requirements=tuple(p for p in state.slots[-1].requirements if p.value != name)),))
            self.assertEqual(evaluate_satisfaction(reduced).slots[-1].state, m.SlotState.UNRESOLVED)
        # Unrelated successful alternative cannot hide a missing mapping.
        missing = replace(state, entities=tuple(replace(e, produced=False) if e.id.value == 'mapping' else e for e in state.entities))
        any_p = m.Predicate(m.PredicateId('any'), m.PredicateKind.ANY, operands=state.slots[-1].requirements)
        missing = replace(missing, predicates=missing.predicates + (any_p,), slots=missing.slots[:-1] +
                          (replace(missing.slots[-1], requirements=(any_p.id,)),))
        self.assertEqual(evaluate_satisfaction(missing).slots[-1].state, m.SlotState.UNRESOLVED)

    def test_unknown_and_recursive_predicates_do_not_self_prove(self):
        from adapter.planner import model as m
        from adapter.planner.core import evaluate_satisfaction
        _, bundle = p03_proof_world(); state = bundle.current
        unsupported = m.Predicate(m.PredicateId('unknown'), m.PredicateKind.UNSUPPORTED)
        recursive = m.Predicate(m.PredicateId('recursive'), m.PredicateKind.ALL,
                                operands=(m.PredicateId('recursive'),))
        state = replace(state, predicates=state.predicates + (unsupported,))
        self.assertEqual(self.proof(state, 'unknown').state, m.ProofState.UNKNOWN)
        cyclic = replace(state, predicates=state.predicates + (recursive,))
        with self.assertRaises(m.PlannerError):
            self.proof(cyclic, 'recursive')
        with self.assertRaises(m.PlannerError):
            evaluate_satisfaction(cyclic)

    def test_coverage_is_single_pass_not_descendant_count(self):
        from adapter.planner import model as m
        from adapter.planner.core import coverage_scores
        _, bundle = p03_proof_world(); state = bundle.current
        state = replace(state, actions=tuple(replace(a, pass_model_complete=True) for a in state.actions))
        # S-CONTEXT has no formal result model, so it prevents criterion 1 ranking.
        computed = recompute(state)
        self.assertEqual(computed.selection.criterion, 5)
        scores = coverage_scores(state, state.actions[:2], computed.blocked)
        self.assertEqual(scores[state.actions[0].id], (1, 1, 0))
        self.assertNotIn(state.actions[1].id, scores)

    def test_new_proof_state_stales_and_roundtrips(self):
        from adapter.planner.core import evaluate_satisfaction
        from adapter.planner import model as m
        _, bundle = p03_proof_world(); state = bundle.current
        state = evaluate_satisfaction(replace(state, knowledge=state.actions[0].accepted_inventory))
        stale = invalidate_sources(state, (state.actions[0].source.identity,))
        self.assertEqual(stale.roots[-1].state, m.ConditionState.STALE)
        self.assertEqual(stale.slots[-1].state, m.SlotState.STALE)
        self.assertEqual(snapshot_bytes(decode_snapshot(snapshot_bytes(stale))), snapshot_bytes(stale))
        self.assertFalse(recompute(stale).actionable)

    def test_p03_state_all_metadata_roundtrip_and_permutation(self):
        from adapter.planner import model as m
        from adapter.planner.core import evaluate_satisfaction
        from adapter.planner.codec import bundle_bytes
        _, bundle = p03_proof_world(); state = bundle.current
        info = m.InformationModel(state.actions[0].id, ('x', 'y', 'z'), (('x', 'y'), ('z',)),
                                  state.actions[0].source)
        state = replace(state, information=(info,), knowledge=state.actions[0].accepted_inventory)
        reversed_state = replace(state, entities=tuple(reversed(state.entities)),
            predicates=tuple(reversed(state.predicates)), roots=tuple(reversed(state.roots)),
            slots=tuple(reversed(state.slots)), information=(replace(info, alternatives=('z', 'y', 'x'),
                                                  partitions=(('z',), ('y', 'x'))),))
        for _ in range(5):
            self.assertEqual(snapshot_bytes(state), snapshot_bytes(reversed_state))
            self.assertEqual(recompute(state), recompute(decode_snapshot(snapshot_bytes(reversed_state))))
            self.assertEqual(snapshot_bytes(evaluate_satisfaction(state)),
                             snapshot_bytes(evaluate_satisfaction(reversed_state)))
        with self.assertRaises(PlannerError):
            bundle_bytes(replace(bundle, policy_version='E1-SELECTION-1-P01-SUBSET'))

    def test_scope_generation_and_effect_permissions_are_pinned_not_ambient(self):
        from adapter.planner import model as m
        _, bundle = p03_proof_world(); state = bundle.current
        allowed = replace(state.actions[0], effect=m.EffectClass.QUALIFICATION_EFFECT_ONLY,
                          authority=m.PredicateId('authority'))
        scoped = replace(state, actions=(allowed,) + state.actions[1:], context=replace(
            state.context, allowed_effects=(m.EffectClass.QUALIFICATION_EFFECT_ONLY,)))
        self.assertIn(allowed.id, recompute(scoped).actionable)
        expired = replace(scoped, context=replace(scoped.context, tick=11))
        self.assertNotIn(allowed.id, recompute(expired).actionable)
        mismatched = replace(scoped, context=replace(scoped.context, generation='NEW'))
        self.assertNotIn(allowed.id, recompute(mismatched).actionable)
        # Permission to construct is not permission to perform a use/issuance effect.
        denied = replace(scoped, predicates=tuple(replace(p, permission=m.AuthorityClass.USE)
            if p.id.value == 'authority' else p for p in scoped.predicates))
        self.assertNotIn(allowed.id, recompute(denied).actionable)

    def test_coverage_counts_direct_roots_transitive_slots_actual_unlocks(self):
        from adapter.planner import model as m
        from adapter.planner.core import coverage_scores
        _, bundle = p03_proof_world(); state = bundle.current
        direct = state.roots[-1]
        dependent_pred = m.Predicate(m.PredicateId('dependent-root'), m.PredicateKind.CONDITION_SATISFIED,
                                     condition=direct.id)
        dependent_root = m.RootCondition(m.ConditionId('TEST:downstream-root'), m.ConditionState.UNRESOLVED,
                                         predicate=dependent_pred.id)
        slot = replace(state.slots[-1], id=m.SlotId('TEST:transitive-slot'), root_requirements=(dependent_root.id,))
        ready = replace(state.actions[1], id=ActionId('TEST:ready'), prerequisites=(
            m.Gate(m.GateKind.CONDITION_SATISFIED, dependent_root.id),))
        state = replace(state, roots=state.roots + (dependent_root,), slots=state.slots + (slot,),
            predicates=state.predicates + (dependent_pred,),
            actions=tuple(replace(a, pass_model_complete=True) for a in state.actions) + (ready,),
            statuses=state.statuses + (m.ActionStatus(ready.id, m.ActionState.ACTION_ELIGIBLE),))
        computed = recompute(state)
        scores = coverage_scores(state, state.actions[:2], computed.blocked)
        self.assertEqual(scores[state.actions[0].id], (1, 2, 1))

    def test_p02_wire_contract_omits_p03_defaults(self):
        import json
        from adapter.planner.codec import snapshot_bytes
        fixture, _ = fixture_bundle()
        wire = json.loads(snapshot_bytes(fixture.snapshot))['snapshot']
        self.assertNotIn('entities', wire)
        self.assertNotIn('predicates', wire)
        self.assertNotIn('context', wire)
        for action in wire['actions']:
            self.assertNotIn('requirements', action)
            self.assertNotIn('cost', action)
            self.assertNotIn('stage', action)
        self.assertEqual(snapshot_bytes(decode_snapshot(snapshot_bytes(fixture.snapshot))),
                         snapshot_bytes(fixture.snapshot))


    def test_unknown_operation_and_human_decision_are_not_auto_actionable(self):
        from adapter.planner import model as m
        fixture, _ = fixture_bundle()
        for operation in (m.OperationClass.OTHER, m.OperationClass.ARCHITECT_AUTHORITY,
                          m.OperationClass.ARCHITECT_CONTRACT_DECISION, m.OperationClass.GOVERNED_OPERATION):
            action = replace(fixture.snapshot.actions[0], operation=operation)
            state = replace(fixture.snapshot, actions=(action,) + fixture.snapshot.actions[1:])
            self.assertNotIn(action.id, recompute(state).actionable)


    def test_x08_future_produced_evidence_does_not_invent_ordering(self):
        from adapter.planner import model as m
        from adapter.planner.core import project
        _, bundle = p03_proof_world(); state = bundle.current
        future = replace(state.entities[0], id=m.EntityId('future-evidence'),
                         kind=m.EntityKind.EVIDENCE, produced=False)
        link = m.GraphAssertion(m.AssertionId('future-output'), state.actions[0].source,
            relation=m.Relation.PRODUCED_BY, subject=future.id, object=state.actions[0].id)
        state = replace(state, entities=state.entities + (future,), assertions=state.assertions + (link,))
        self.assertNotIn((future.id, state.actions[0].id), project(state).edges)
        self.assertIn(state.actions[0].id, recompute(state).actionable)
        proof = m.Predicate(m.PredicateId('future-proof'), m.PredicateKind.EVIDENCE, entity=future.id)
        self.assertEqual(self.proof(replace(state, predicates=state.predicates + (proof,)), 'future-proof').state,
                         m.ProofState.UNKNOWN)


if __name__ == '__main__':
    unittest.main()


class P06ImporterInvariantTests(unittest.TestCase):
    def test_structured_import_fail_closed_and_oracles_are_not_facts(self):
        import copy,json,tempfile
        from pathlib import Path
        from adapter.planner import replay,codec,model as m,core
        root=Path(__file__).resolve().parents[2]
        path=root/'adapter/tests/fixtures/planner_v0_1/B_P06.json'
        original=codec.parse_json(path.read_bytes())
        changes=[lambda d:d.update(schema='UNKNOWN'),
                 lambda d:d['initial']['snapshot']['statuses'][0]['state'].update(value='UNKNOWN'),
                 lambda d:d['initial']['snapshot']['actions'][0]['requirements'][0].update(value='dangling'),
                 lambda d:d['initial']['snapshot']['entities'][0]['identity']['kind'].update(value='SHA256_ANY'),
                 lambda d:d['source_manifest'][0]['identity'].update(sha256='0'*64),
                 lambda d:d['initial']['snapshot']['entities'][0]['provenance'].update(excerpt='invented')]
        with tempfile.TemporaryDirectory() as directory:
            target=Path(directory)/'fixture.json'
            for change in changes:
                data=copy.deepcopy(original);change(data);target.write_bytes(codec.canonical_bytes(data))
                with self.assertRaises(m.PlannerError):replay.import_fixture(target,root)
            data=copy.deepcopy(original);data['expected']={'actionable':['invented'],'roots':{'root:B':'SATISFIED'}}
            target.write_bytes(codec.canonical_bytes(data))
            bundle,_,_=replay.import_fixture(target,root)
            self.assertEqual(core.recompute(bundle.current).actionable,())
            self.assertEqual(bundle.current.roots[0].state,m.ConditionState.UNRESOLVED)
            # Object order, not source-list order, cannot change typed identity.
            reverse=lambda value: {k:reverse(v) for k,v in reversed(list(value.items()))} if isinstance(value,dict) else [reverse(x) for x in value] if isinstance(value,list) else value
            data=reverse(original);data['source_manifest'].reverse()
            target.write_text(json.dumps(data))
            other,_,_=replay.import_fixture(target,root)
            self.assertEqual(codec.bundle_bytes(bundle),codec.bundle_bytes(other))


class C01ReferenceContractTests(unittest.TestCase):
    def test_adversarial_dangling_entity_rejected_at_decode(self):
        from adapter.planner import model as m, codec as c
        p = m.Predicate(m.PredicateId('x'), m.PredicateKind.SOURCE_IDENTITY,
                        entity=m.EntityId('absent'))
        state = m.Snapshot((), (), (), (), (), predicates=(p,))
        # Construct hostile bytes directly: do not let the writer be the oracle.
        raw = c.canonical_bytes({'schema': 'PLANNER-SNAPSHOT-1', 'snapshot': c._wire(state)})
        with self.assertRaises(m.PlannerError):
            c.decode_snapshot(raw)

    def hostile(self, state):
        from adapter.planner import codec as c
        return c.canonical_bytes({'schema': 'PLANNER-SNAPSHOT-1', 'snapshot': c._wire(state)})

    def test_missing_targets_wrong_fields_domains_and_cycles(self):
        from adapter.planner import model as m, gates as g, codec as c
        _, bundle = p03_proof_world(); state = bundle.current
        K = m.PredicateKind
        cases = [
            m.Predicate(m.PredicateId('bad'), K.SOURCE_IDENTITY, entity=m.EntityId('missing'), expected=state.entities[0].identity),
            m.Predicate(m.PredicateId('bad'), K.ACTION_COMPLETED, action=m.ActionId('missing')),
            m.Predicate(m.PredicateId('bad'), K.CONDITION_SATISFIED, condition=m.ConditionId('missing')),
            m.Predicate(m.PredicateId('bad'), K.KNOWLEDGE_ACCEPTED, knowledge=m.KnowledgeId('undeclared-future')),
            m.Predicate(m.PredicateId('bad'), K.EVIDENCE_OBLIGATION, obligation=m.EvidenceId('missing')),
            m.Predicate(m.PredicateId('bad'), K.MAPPING_AVAILABLE, entity=state.entities[0].id),
            m.Predicate(m.PredicateId('bad'), K.CONSUMER_CHECK, entity=state.entities[0].id, other=state.entities[0].id, expected=state.entities[0].identity),
            m.Predicate(m.PredicateId('bad'), K.PRODUCER_AVAILABLE, entity=state.entities[0].id, other=state.entities[0].id),
            m.Predicate(m.PredicateId('bad'), K.SOURCE_IDENTITY, entity=state.entities[0].id, expected=state.entities[0].identity, action=state.actions[0].id),
            m.Predicate(m.PredicateId('bad'), K.ALL),
            m.Predicate(m.PredicateId('bad'), K.ANY, operands=(m.PredicateId('absent'),)),
            m.Predicate(m.PredicateId('bad'), K.ALL, operands=(m.PredicateId('bad'),)),
            m.Predicate(m.PredicateId('bad'), K.KNOWLEDGE_ACCEPTED, unavailable=' '),
            m.Predicate(m.PredicateId('bad'), K.SOURCE_IDENTITY, unavailable='missing', entity=state.entities[0].id),
        ]
        for p in cases:
            bad = replace(state, predicates=state.predicates + (p,))
            for operation in (m.validate_model, recompute, lambda s: c.decode_snapshot(self.hostile(s)),
                              lambda s: g.evaluate_predicate(s, p.id)):
                with self.subTest(predicate=p, operation=operation), self.assertRaises(m.PlannerError):
                    operation(bad)
        for mutate in (lambda s: replace(s, predicates=s.predicates + (s.predicates[0],)),
                       lambda s: replace(s, entities=s.entities + (replace(s.entities[0], produced=False),))):
            with self.assertRaises(m.PlannerError):
                c.decode_snapshot(self.hostile(mutate(state)))
        with self.assertRaises(m.PlannerError):
            g.evaluate_predicate(state, m.PredicateId('unknown'))
        raw = self.hostile(state).replace(b'"SOURCE_IDENTITY"', b'"UNKNOWN_PREDICATE"')
        with self.assertRaises(m.PlannerError):
            c.decode_snapshot(raw)

    def test_declared_future_output_and_explicit_unavailable_never_prove(self):
        from adapter.planner import model as m, gates as g, codec as c
        fixture, bundle = p03_proof_world(); state = bundle.current
        p = next(p for p in state.predicates if p.kind is m.PredicateKind.KNOWLEDGE_ACCEPTED)
        self.assertEqual(g.evaluate_predicate(state, p.id).state, m.ProofState.UNKNOWN)
        produced = apply_result(state, replace(fixture.supplied_result, expected_snapshot=c.snapshot_id(state))).snapshot
        self.assertEqual(g.evaluate_predicate(produced, p.id).state, m.ProofState.PROVED)
        missing = replace(p, knowledge=None, unavailable='No authoritative source established')
        explicitly_missing = replace(produced, predicates=tuple(missing if q.id == p.id else q for q in produced.predicates))
        self.assertEqual(g.evaluate_predicate(explicitly_missing, p.id).state, m.ProofState.UNKNOWN)
        restored = c.decode_snapshot(c.snapshot_bytes(explicitly_missing))
        self.assertEqual(g.evaluate_predicate(restored, p.id).state, m.ProofState.UNKNOWN)
        duplicate_owner = replace(state.actions[1], accepted_inventory=state.actions[0].accepted_inventory)
        with self.assertRaises(m.PlannerError):
            m.validate_model(replace(state, actions=(state.actions[0], duplicate_owner)))
        for updates in ({'statement': 'conflicting claim'},):
            wrong_binding = replace(state, knowledge=(replace(state.actions[0].accepted_inventory[0], **updates),))
            with self.assertRaises(m.PlannerError):
                m.validate_model(wrong_binding)
        bad_domain = replace(state, entities=tuple(replace(e, identity=replace(e.identity, kind=m.IdentityKind.CONTENT_IDENTITY))
            if e.kind is m.EntityKind.AUTHORITY else e for e in state.entities))
        with self.assertRaises(m.PlannerError):
            m.validate_model(bad_domain)
        undeclared = replace(state, actions=tuple(replace(a, accepted_inventory=()) for a in state.actions))
        with self.assertRaises(m.PlannerError):
            m.validate_model(undeclared)

    def test_stale_invalid_targets_and_condition_cycles(self):
        from adapter.planner import model as m, gates as g, codec as c
        _, bundle = p03_proof_world(); state = bundle.current
        source = m.PredicateId('source')
        for updates in ({'validation': m.ValidationState.STALE}, {'validated': False}, {'produced': False}):
            held = replace(state, entities=(replace(state.entities[0], **updates),) + state.entities[1:])
            restored = c.decode_snapshot(c.snapshot_bytes(held))
            self.assertEqual(g.evaluate_predicate(restored, source).state, m.ProofState.UNKNOWN)
        p = m.Predicate(m.PredicateId('cycle-root'), m.PredicateKind.CONDITION_SATISFIED, condition=state.roots[0].id)
        cycle = replace(state, roots=(replace(state.roots[0], predicate=p.id),) + state.roots[1:], predicates=state.predicates + (p,))
        with self.assertRaises(m.PlannerError):
            c.decode_snapshot(self.hostile(cycle))
        a=m.Predicate(m.PredicateId('cycle-a'),m.PredicateKind.ALL,operands=(m.PredicateId('cycle-b'),))
        b=m.Predicate(m.PredicateId('cycle-b'),m.PredicateKind.ANY,operands=(a.id,))
        with self.assertRaises(m.PlannerError):
            m.validate_model(replace(state,predicates=state.predicates+(a,b)))

    def test_c01_permutation_key_order_and_reload(self):
        import json
        from adapter.planner import model as m, codec as c
        _, bundle = p03_proof_world(); state = bundle.current
        expected=c.snapshot_bytes(state)
        def reverse(obj):
            if isinstance(obj,dict): return {k:reverse(v) for k,v in reversed(list(obj.items()))}
            if isinstance(obj,list): return [reverse(v) for v in obj]
            return obj
        for _ in range(3):
            state=replace(state, predicates=tuple(reversed(state.predicates)),entities=tuple(reversed(state.entities)),actions=tuple(reversed(state.actions)))
            self.assertEqual(c.snapshot_bytes(state),expected)
            state=c.decode_snapshot(json.dumps(reverse(json.loads(expected))).encode())
            self.assertEqual(c.snapshot_bytes(state),expected)
            self.assertEqual(recompute(state).selection.selected.value,'S-BINDING')

        # Rejected input is deterministic too: competing malformed references
        # must report the same canonical first error regardless of tuple order.
        bad = tuple(m.Predicate(m.PredicateId(name), m.PredicateKind.SOURCE_IDENTITY,
                    entity=m.EntityId('absent-' + name), expected=state.entities[0].identity)
                    for name in ('z-bad', 'a-bad'))
        messages = []
        for order in (bad, tuple(reversed(bad))):
            with self.assertRaises(m.PlannerError) as caught:
                m.validate_model(replace(state, predicates=state.predicates + order))
            messages.append(str(caught.exception))
        self.assertEqual(messages[0], messages[1])
        self.assertIn('a-bad', messages[0])


class C02StaleOrderingTests(unittest.TestCase):
    def world(self):
        from adapter.planner import model as m
        fixture, bundle = p03_proof_world()
        state = bundle.current
        source = state.actions[0].source
        ordering = replace(source, identity=replace(source.identity, sha256='f' * 64))
        parent = m.RootCondition(m.ConditionId('C02:parent'), m.ConditionState.UNRESOLVED)
        child = state.roots[-1]
        edge = m.GraphAssertion(m.AssertionId('C02:ordering'), ordering,
            relation=m.Relation.REQUIRES, subject=child.id, object=parent.id,
            ordering_justification='C02 explicit mandatory prerequisite')
        metadata = tuple(m.GraphAssertion(m.AssertionId('C02:meta:' + a.id.value + ':' + g.target.value), source,
            relation=m.Relation.REQUIRES, subject=a.id, object=g.target,
            ordering_justification='existing action prerequisite') for a in state.actions for g in a.prerequisites)
        state = replace(state, roots=state.roots + (parent,),
            knowledge=fixture.supplied_result.knowledge, assertions=state.assertions + metadata + (edge,))
        return state, ordering, parent, child

    def test_t01_ordering_invalidation_must_not_satisfy_child(self):
        from adapter.planner.core import evaluate_satisfaction, project
        state, ordering, parent, child = self.world()
        before = evaluate_satisfaction(state)
        self.assertEqual(next(r.state for r in before.roots if r.id == child.id), ConditionState.UNRESOLVED)
        changed = invalidate_sources(state, (ordering.identity,))
        after = evaluate_satisfaction(changed)
        self.assertNotEqual(next(r.state for r in after.roots if r.id == child.id), ConditionState.SATISFIED)
        self.assertIn((parent.id, child.id), project(changed).edges)
        self.assertNotEqual(after.slots[-1].state, SlotState.RESOLVED)
        self.assertIn(ActionId('S-BINDING'), recompute(changed).actionable)
        self.assertEqual(snapshot_bytes(after), snapshot_bytes(decode_snapshot(snapshot_bytes(after))))

    def test_transitive_diamond_slot_and_mixed_support_requalification(self):
        from adapter.planner import model as m
        from adapter.planner.core import evaluate_satisfaction
        state, ordering, parent, child = self.world()
        source = state.actions[0].source
        leaf = m.RootCondition(m.ConditionId('C02:leaf'), m.ConditionState.UNRESOLVED, predicate=child.predicate)
        edges = tuple(m.GraphAssertion(m.AssertionId('C02:' + name), source,
            relation=m.Relation.REQUIRES, subject=subject, object=obj,
            ordering_justification='mandatory') for name, subject, obj in (
                ('leaf-child', leaf.id, child.id), ('leaf-parent', leaf.id, parent.id),
                ('slot-leaf', state.slots[-1].id, leaf.id)))
        state = replace(state, roots=tuple(replace(r, state=m.ConditionState.SATISFIED) if r.id == parent.id else r
            for r in state.roots) + (leaf,), assertions=state.assertions + edges)
        self.assertEqual(evaluate_satisfaction(state).slots[-1].state, SlotState.RESOLVED)
        changed = invalidate_sources(state, (ordering.identity,))
        self.assertTrue(all(r.state is ConditionState.STALE for r in changed.roots if r.id in (child.id,leaf.id)))
        self.assertEqual(changed.slots[-1].state, SlotState.STALE)
        # A duplicate accepted path cannot erase the mandatory stale obligation.
        old = next(a for a in state.assertions if a.id.value == 'C02:ordering')
        duplicate = replace(old, id=m.AssertionId('C02:duplicate'), provenance=source)
        mixed = replace(changed, assertions=changed.assertions + (duplicate,))
        self.assertNotEqual(evaluate_satisfaction(mixed).slots[-1].state, SlotState.RESOLVED)
        # Explicit qualification replaces the old binding and independently resets
        # the stale output qualifications. No mutation of the historical snapshot.
        renewed = replace(changed,
            assertions=tuple(replace(a, provenance=source, validation=m.ValidationState.ACCEPTED)
                if a.id == old.id else a for a in changed.assertions),
            roots=state.roots, slots=state.slots)
        self.assertEqual(evaluate_satisfaction(renewed).slots[-1].state, SlotState.RESOLVED)
        for permuted in (changed, replace(changed, roots=tuple(reversed(changed.roots)),
                assertions=tuple(reversed(changed.assertions)), slots=tuple(reversed(changed.slots)))):
            loaded = decode_snapshot(snapshot_bytes(permuted))
            self.assertEqual(snapshot_bytes(evaluate_satisfaction(changed)), snapshot_bytes(evaluate_satisfaction(loaded)))
            self.assertEqual(recompute(changed).actionable, recompute(loaded).actionable)

    def test_completed_history_is_not_current_output_qualification(self):
        from adapter.planner import model as m
        from adapter.planner.gates import evaluate_predicate
        fixture, _ = fixture_bundle()
        completed = apply_result(fixture.snapshot, fixture.supplied_result).snapshot
        action = fixture.supplied_result.action
        predicate = m.Predicate(m.PredicateId('C02:completion'), m.PredicateKind.ACTION_COMPLETED, action=action)
        completed = replace(completed, predicates=(predicate,))
        self.assertEqual(evaluate_predicate(completed, predicate.id).state, m.ProofState.PROVED)
        changed = invalidate_sources(completed, (completed.actions[0].source.identity,))
        self.assertEqual(next(s.state for s in changed.statuses if s.id == action), ActionState.COMPLETED)
        self.assertEqual(evaluate_predicate(changed, predicate.id).state, m.ProofState.UNKNOWN)
        self.assertNotIn(ActionId('S-CONTEXT'), recompute(changed).actionable)
        self.assertEqual(snapshot_bytes(changed), snapshot_bytes(decode_snapshot(snapshot_bytes(changed))))

    def test_stale_ordering_blocks_decision_before_recompute(self):
        from adapter.planner import model as m
        from adapter.planner import gates
        from adapter.tests.test_planner_e1_replay import fixture, result, decision
        state, _ = fixture('G')
        state = apply_result(state, result(state)).snapshot
        d = decision(state, 'DEC-BUDGET')
        self.assertEqual(gates.decision_readiness(state, d).state, m.DecisionReadiness.DECISION_READY)
        ordering = replace(state.actions[0].source, identity=replace(state.actions[0].source.identity, sha256='f'*64))
        parent = m.RootCondition(m.ConditionId('C02:decision-parent'), ConditionState.SATISFIED)
        # Metadata and explicit assertion describe the same mandatory requirement.
        actions = tuple(replace(a, prerequisites=a.prerequisites + (m.Gate(m.GateKind.CONDITION_SATISFIED,parent.id),))
            if a.id == d.action else a for a in state.actions)
        metadata = tuple(m.GraphAssertion(m.AssertionId('C02:gate:' + a.id.value + ':' + g.target.value),
            ordering if a.id == d.action and g.target == parent.id else a.source,
            relation=m.Relation.REQUIRES, subject=a.id, object=g.target, ordering_justification='mandatory')
            for a in actions for g in a.prerequisites)
        state = replace(state, actions=actions, roots=state.roots + (parent,), assertions=state.assertions + metadata)
        changed = invalidate_sources(state, (ordering.identity,))
        self.assertNotEqual(gates.decision_readiness(changed, decision(changed,'DEC-BUDGET')).state, m.DecisionReadiness.DECISION_READY)
        self.assertNotIn(d.action, recompute(changed).actionable)

    def test_legitimate_any_alternative_and_empty_output_completion(self):
        from adapter.planner import model as m
        from adapter.planner.core import evaluate_satisfaction
        from adapter.planner.gates import evaluate_predicate
        state, ordering, _, _ = self.world()
        value = state.entities[0]
        alternate = replace(value, id=m.EntityId('C02:alternate'), provenance=ordering,
            identity=replace(value.identity, sha256='9'*64))
        alt = m.Predicate(m.PredicateId('C02:alternate'), m.PredicateKind.SOURCE_IDENTITY,
            entity=alternate.id, expected=alternate.identity)
        either = m.Predicate(m.PredicateId('C02:either'), m.PredicateKind.ANY,
            operands=(m.PredicateId('source'), alt.id))
        root = m.RootCondition(m.ConditionId('C02:either'), ConditionState.UNRESOLVED, predicate=either.id)
        state = replace(state, entities=state.entities + (alternate,), predicates=state.predicates + (alt,either),
            roots=state.roots + (root,))
        changed = invalidate_sources(state, (value.provenance.identity,))
        self.assertEqual(evaluate_predicate(changed, either.id).state, m.ProofState.PROVED)
        self.assertEqual(next(r.state for r in evaluate_satisfaction(changed).roots if r.id == root.id), ConditionState.SATISFIED)
        # An action with no output inventory must still persist lost qualification.
        fixture, _ = fixture_bundle()
        a = replace(fixture.snapshot.actions[0], accepted_inventory=())
        pred = m.Predicate(m.PredicateId('C02:empty-completed'), m.PredicateKind.ACTION_COMPLETED, action=a.id)
        state = replace(fixture.snapshot, actions=(a,) + fixture.snapshot.actions[1:], predicates=(pred,),
            statuses=tuple(replace(s,state=ActionState.COMPLETED) if s.id == a.id else s for s in fixture.snapshot.statuses))
        changed = invalidate_sources(state, (a.source.identity,))
        loaded = decode_snapshot(snapshot_bytes(changed))
        self.assertEqual(next(s.state for s in loaded.statuses if s.id == a.id), ActionState.COMPLETED)
        self.assertEqual(evaluate_predicate(loaded,pred.id).state,m.ProofState.UNKNOWN)

    def test_hash_seed_and_key_order_replay(self):
        import json, os, subprocess, sys
        state, ordering, _, _ = self.world()
        raw = snapshot_bytes(state)
        def reverse_keys(value):
            if isinstance(value, dict):
                return {k: reverse_keys(v) for k,v in reversed(tuple(value.items()))}
            if isinstance(value,list):
                return [reverse_keys(v) for v in value]
            return value
        reversed_keys = json.dumps(reverse_keys(json.loads(raw)), indent=2).encode()
        script = '''import sys,json
from adapter.planner import core,codec
from adapter.planner.model import AssertionId
s=codec.decode_snapshot(sys.stdin.buffer.read())
p=next(a.provenance for a in s.assertions if a.id==AssertionId('C02:ordering'))
s=codec.invalidate_sources(s,(p.identity,))
c=core.recompute(s)
print(codec.snapshot_bytes(s).hex())
print(c.selection.selected)
print(c.actionable)
print(c.control)
'''
        outputs = [subprocess.check_output([sys.executable,'-c',script], input=data,
            env=dict(os.environ,PYTHONHASHSEED=seed)) for seed in ('1','7','42','123','999')
            for data in (raw,reversed_keys)]
        self.assertEqual(len(set(outputs)),1)

    def test_stale_goal_cannot_be_terminal_success_or_hide_independent_work(self):
        from adapter.planner import model as m
        from adapter.planner.core import evaluate_satisfaction
        state, ordering, parent, child = self.world()
        state = replace(state, roots=tuple(replace(r,state=ConditionState.SATISFIED) if r.id == parent.id else r
            for r in state.roots), goals=(m.Goal(child.id,(ActionId('S-BINDING'),),state.actions[0].source),))
        state = evaluate_satisfaction(state)
        changed = invalidate_sources(state, (ordering.identity,))
        comp = recompute(changed)
        self.assertEqual(comp.control,m.ControlState.RUNNABLE)
        self.assertNotIn((child.id,m.BranchState.TERMINAL_SUCCESS),comp.branches)
        held = replace(changed,statuses=tuple(replace(s,state=ActionState.WAITING) for s in changed.statuses))
        self.assertNotEqual(recompute(held).control,m.ControlState.TERMINAL_SUCCESS)
        self.assertEqual(recompute(held),recompute(decode_snapshot(snapshot_bytes(held))))

    def test_ordered_evidence_is_unusable_even_before_propagation(self):
        from adapter.planner import model as m
        from adapter.planner.gates import usable, evaluate_predicate
        state, ordering, parent, _ = self.world()
        value = state.entities[0]
        edge = m.GraphAssertion(m.AssertionId('C02:entity-order'),ordering,
            relation=m.Relation.REQUIRES, subject=value.id, object=parent.id,
            ordering_justification='evidence qualification prerequisite')
        state = replace(state,assertions=state.assertions+(edge,))
        stale = replace(state,assertions=tuple(replace(a,validation=m.ValidationState.STALE)
            if a.id == edge.id else a for a in state.assertions))
        self.assertEqual(usable(value,stale).state,m.ProofState.UNKNOWN)
        self.assertEqual(evaluate_predicate(stale,m.PredicateId('source')).state,m.ProofState.UNKNOWN)
        propagated = invalidate_sources(state,(ordering.identity,))
        self.assertEqual(propagated.entities[0].validation,m.ValidationState.STALE)
        self.assertEqual(snapshot_bytes(propagated),snapshot_bytes(decode_snapshot(snapshot_bytes(propagated))))


class C03ResumeProofTests(unittest.TestCase):
    def test_t02_stale_attestor_cannot_authorize_resume(self):
        from adapter.planner import model as m, core, gates, replay
        from adapter.tests.test_planner_e1_replay import P05ReplayTests, synthetic_receipt, external_event, p05_bundle
        state = P05ReplayTests().waiting()
        state, evidence = synthetic_receipt(state)
        for stage in (m.ExternalStage.EVIDENCE_RECEIVED,m.ExternalStage.EVIDENCE_VALIDATED,m.ExternalStage.DEPENDENT_ACTION_REENTRY):
            state = core.apply_receipt(state,external_event(state,stage,evidence.id if stage is m.ExternalStage.EVIDENCE_RECEIVED else None)).snapshot
        trust = next(e for e in state.entities if e.id.value == 'TEST-TRUST')
        stale = invalidate_sources(state,(trust.provenance.identity,))
        self.assertFalse(gates.external_complete(stale,stale.external_gates[0]))
        self.assertEqual(core.recompute(stale).actionable,())
        self.assertFalse(replay.plan_output(p05_bundle(stale))['resume_allowed'])
        self.assertEqual(stale.external_gates[0].history,state.external_gates[0].history)
