"""T03 synthetic human-choice qualification; never touches live E2 state."""
from dataclasses import replace
import unittest

from adapter.planner import codec, core, model as m
from adapter.planner.human_decision import E2_LINEAGE, E2_SCOPE, OPTIONS, HumanDecisionError, PROTOCOL_TRUST_ROOT, QUALIFICATION_ISSUER
import adapter.planner.human_decision as hd


class E2T03Tests(unittest.TestCase):
    def setUp(self):
        p = m.Provenance('synthetic://e2-t03', m.ArtifactIdentity(
            m.IdentityKind.CONTENT_IDENTITY, 'raw-file-sha256', '1' * 64),
            '/fixture', 'E2-T03 synthetic fixture', 'E2-T03-FIXTURE-1', E2_SCOPE)
        entity = m.GraphEntity(m.EntityId('E2-FIXTURE-SOURCE'), m.EntityKind.VALUE,
            m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY, 'e2-fixture', '2' * 64),
            p, E2_SCOPE, E2_LINEAGE, 'E2-GENERATION-1', 100)
        action_id = m.ActionId('E2-DECIDE')
        checks, predicates, refs = [], [], []
        for label in ('QUESTION_SCOPE', 'SOURCE_PROVENANCE', 'CONCRETE_ALTERNATIVES',
                      'AUTHORITY_BOUNDARY', 'DECISION_FACTS_COMPLETE', 'INDEPENDENT_VALIDATION'):
            predicate_id = m.PredicateId('E2-T03-' + label)
            predicates.append(m.Predicate(predicate_id, m.PredicateKind.TYPED_EQUAL,
                                          entity=entity.id, expected=entity.identity))
            checks.append(m.DecisionCheck(m.DossierCheck[label], predicate_id, p))
            refs.append((predicate_id, label))
        facts = []
        for label in ('E2-T03-FACT-1', 'E2-T03-FACT-2'):
            predicate_id = m.PredicateId(label)
            predicates.append(m.Predicate(predicate_id, m.PredicateKind.TYPED_EQUAL,
                                          entity=entity.id, expected=entity.identity))
            facts.append(predicate_id)
            refs.append((predicate_id, label))
        dossier = m.DecisionDossier(action_id, p, 'qualification choice', E2_SCOPE,
            OPTIONS, tuple(checks), tuple(facts), (), 'E2-GRANT only', 'No production authority')
        dossier_id = hd._dossier_identity(dossier)
        instances = tuple(m.ValidationInstance(pid, label, dossier_id, (), m.ValidationOutcome.PASS,
            E2_SCOPE, E2_LINEAGE, m.ValidationState.ACCEPTED, p) for pid, label in refs)
        action = m.Action(action_id, m.OperationClass.ARCHITECT_CONTRACT_DECISION,
            m.EffectClass.NON_EFFECTING, (), p, (), pass_model_complete=True)
        decision = m.Decision(action_id, None, None, '', m.DecisionStage.DECISION_READY,
            p, dossier=dossier, history=(m.DecisionStage.DECISION_INPUTS_REQUIRED,
            m.DecisionStage.DECISION_INPUT_ACQUISITION, m.DecisionStage.DECISION_DOSSIER_READY,
            m.DecisionStage.DECISION_READY))
        self.snapshot = m.Snapshot((action,), (m.ActionStatus(action_id, m.ActionState.ACTIONABLE),),
            (), (), (), entities=(entity,), predicates=tuple(predicates),
            validation_instances=instances,
            context=m.EvaluationContext(E2_SCOPE, E2_LINEAGE, 'E2-GENERATION-1', 1),
            decisions=(decision,))
        m.validate_model(self.snapshot)
        self.issuer = QUALIFICATION_ISSUER
        self.trust = PROTOCOL_TRUST_ROOT

    def choice(self, option):
        return hd.HumanChoiceInput(option, self.issuer, self.trust,
            hd._dossier_identity(self.snapshot.decisions[0].dossier),
            m.ActionId('E2-DECIDE'), codec.snapshot_id(self.snapshot), 1)

    def test_allow_materializes_record_and_narrow_grant(self):
        result = hd.apply_explicit_choice(self.snapshot, self.choice(OPTIONS[0]), self.trust)
        self.assertEqual(result.event.choice, OPTIONS[0])
        self.assertIsNotNone(result.grant)
        self.assertEqual(result.grant.id.value, 'E2-GRANT')
        self.assertEqual(result.grant.scope, E2_SCOPE)
        self.assertEqual(result.grant.lineage, E2_LINEAGE)
        self.assertEqual(result.snapshot.decisions[0].stage, m.DecisionStage.DECISION_RECORDED)

    def test_decline_is_recorded_without_grant(self):
        result = hd.apply_explicit_choice(self.snapshot, self.choice(OPTIONS[1]), self.trust)
        self.assertEqual(result.event.choice, OPTIONS[1])
        self.assertIsNone(result.grant)
        self.assertNotIn('E2-GRANT', {e.id.value for e in result.snapshot.entities})

    def test_repeated_identical_choice_is_idempotent_and_conflict_fails(self):
        first = hd.apply_explicit_choice(self.snapshot, self.choice(OPTIONS[0]), self.trust)
        repeated_input = hd.HumanChoiceInput(OPTIONS[0], self.issuer, self.trust,
            hd._dossier_identity(self.snapshot.decisions[0].dossier), m.ActionId('E2-DECIDE'),
            codec.snapshot_id(first.snapshot), 1)
        repeated = hd.apply_explicit_choice(first.snapshot, repeated_input, self.trust)
        self.assertEqual(repeated.snapshot, first.snapshot)
        conflicting = replace(repeated_input, option=OPTIONS[1])
        with self.assertRaises(HumanDecisionError):
            hd.apply_explicit_choice(first.snapshot, conflicting, self.trust)

    def test_wrong_trust_root_and_wrong_dossier_fail_closed(self):
        with self.assertRaises(HumanDecisionError):
            hd.apply_explicit_choice(self.snapshot, self.choice(OPTIONS[0]),
                m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY, 'raw-file-sha256', '5' * 64))
        with self.assertRaises(HumanDecisionError):
            bad = replace(self.choice(OPTIONS[0]), dossier=m.ArtifactIdentity(
                m.IdentityKind.CONTENT_IDENTITY, 'planner-dossier-sha256', 'a' * 64))
            hd.apply_explicit_choice(self.snapshot, bad, self.trust)

    def test_runtime_identity_is_deterministic(self):
        a = hd.apply_explicit_choice(self.snapshot, self.choice(OPTIONS[0]), self.trust)
        b = hd.apply_explicit_choice(self.snapshot, self.choice(OPTIONS[0]), self.trust)
        self.assertEqual(codec.snapshot_id(a.snapshot), codec.snapshot_id(b.snapshot))
        self.assertEqual(a.evidence.identity, b.evidence.identity)

    def test_choice_record_and_grant_survive_native_snapshot_round_trip(self):
        result = hd.apply_explicit_choice(self.snapshot, self.choice(OPTIONS[0]), self.trust)
        restored = codec.decode_snapshot(codec.snapshot_bytes(result.snapshot))
        self.assertEqual(codec.snapshot_id(restored), codec.snapshot_id(result.snapshot))
        self.assertEqual(restored.decisions[0].recorded_choice, OPTIONS[0])
        self.assertIn('E2-GRANT', {e.id.value for e in restored.entities})


if __name__ == '__main__':
    unittest.main()
