"""Current E01-E05/T01/G01-G04 regressions using immutable evidence inputs."""
from dataclasses import replace
import json
from pathlib import Path
import unittest
from adapter.planner import codec as c, model as m, core, genesis_bundle as gb
from adapter.planner import evidence_transitions as transitions
from adapter.planner import evidence_materializer as materializer, evidence_lifecycle as lifecycle
from adapter.planner import evidence_attestation as attestation

D = Path(__file__).resolve().parents[2] / 'docs/plans'


class E06HistoricalRegressions(unittest.TestCase):
    def test_e01_e02_t01_materialization(self):
        request = c._unwire(json.loads((D/'DETERMINISTIC_PLANNER_V0_1_E2_P03_SEMANTIC_NATIVE_EVIDENCE_BINDING_1_CANDIDATE.json').read_text()))
        b = gb.decode_bundle((D/'DETERMINISTIC_PLANNER_V0_1_E2_P03_POST_RECEIPT_BUNDLE.json').read_bytes())
        e01 = json.loads((D/'DETERMINISTIC_PLANNER_V0_1_EVIDENCE_E01_MATERIALIZER_RESULT.json').read_text())
        requirement = next(r for r in b.current.evidence_requirements if r.id == request.requirements[0])
        semantic = m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY, 'semantic', e01['semantic_evidence_id'])
        content = m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY, 'content', e01['content_id'])
        result = materializer.materialize(semantic_evidence_id=semantic, content_id=content, gate=request.gate, context=b.current.context, proposition=requirement.proposition, source_pin=request.entity.identity, attestor=request.admission.producer, attestor_predicate=request.admission.authentication, admission=request.admission)
        self.assertEqual(result.entity.id, request.entity.id)
        self.assertEqual(result.entity.identity, request.entity.identity)
        source = request.entity.identity
        bound = attestation.materialize(attestor_authority=request.admission.producer, attestor=request.admission.producer, source_predicate=request.admission.authentication, source_pin=source, native_entity=result.entity.id, semantic_evidence=semantic, content=content, proposition=requirement.proposition, gate=request.gate, scope=b.scope, lineage=b.lineage, provenance=result.entity.provenance.identity)
        contract = next(x for x in b.current.external_gates if x.id == request.gate)
        # validate expects an ingress contract; only its typed gate/scope/lineage
        # fields are relevant to this exact existing attestation boundary.
        from types import SimpleNamespace
        ingress = SimpleNamespace(gate=request.gate, scope=b.scope, lineage=b.lineage)
        args = dict(entity=result.entity, contract=ingress, gate=request.gate, context=b.current.context, source_pin=source, semantic_evidence=semantic, content=content, proposition=requirement.proposition, attestor=request.admission.producer)
        self.assertTrue(attestation.validate(bound, **args))
        with self.assertRaises(m.PlannerError): attestation.validate(replace(bound, lineage='wrong'), **args)

    def test_e03_separated_lifecycle(self):
        state = lifecycle.received(m.EntityId('generic-received-evidence'))
        with self.assertRaises(m.PlannerError): lifecycle.prove(state, 'proof')
        state = lifecycle.validate(state, 'validation', True)
        state = lifecycle.prove(state, 'proof')
        with self.assertRaises(m.PlannerError): lifecycle.reentry(state, False)
        state = lifecycle.reentry(state, True)
        self.assertEqual(lifecycle.complete_reenter(state).stage, lifecycle.EvidenceStage.REENTER_COMPLETED)

    def test_e04_e05_native_replay(self):
        b = gb.decode_bundle((D/'DETERMINISTIC_PLANNER_V0_1_E2_P03_POST_RECEIPT_BUNDLE.json').read_bytes())
        s = b.current
        e = next(e for e in s.entities if e.id.value.startswith('EVIDENCE:'))
        r = s.evidence_requirements[0]; p = next(p for p in s.predicates if p.id.value == 'E2-PROOF')
        s, validation = transitions.validate_evidence(s, e.id, p.id, r.proposition, (e.identity,e.provenance.identity,r.provenance.identity), r.provenance.identity, True, e.provenance)
        s, proof = transitions.admit_proof(s, s.external_gates[0].id, e.id, r.id, validation, r.proposition, r.producers[0], s.context.scope, s.context.lineage, e.provenance)
        s, reentry = transitions.evaluate_reentry(s, s.external_gates[0].id, s.context.scope, s.context.lineage, e.provenance)
        self.assertTrue(reentry.eligible)
        self.assertEqual(core.recompute(s).selection.selected, m.ActionId('E2-REENTER'))
        corrected = c.decode_snapshot((D/'DETERMINISTIC_PLANNER_V0_1_E2_P03_E05_CORRECTED_SNAPSHOT.json').read_bytes())
        target = c.decode_snapshot((D/'DETERMINISTIC_PLANNER_V0_1_E2_P03_E05_TARGET_SNAPSHOT.json').read_bytes())
        from adapter.planner.action_materializer import materialize_action
        source = json.loads((D/'DETERMINISTIC_PLANNER_V0_1_E2_PC01_SOURCES.json').read_text())
        declaration = next(x for x in source['declarations'] if x['id']=='E2-REENTER')
        action = next(a for a in s.actions if a.id == m.ActionId('E2-REENTER'))
        replay_start = replace(s, actions=tuple(materialize_action(a,declaration) if a.id==action.id else a for a in s.actions))
        self.assertEqual(c.snapshot_id(replay_start), c.snapshot_id(corrected))
        inventory = next(a for a in corrected.actions if a.id == action.id).accepted_inventory
        replayed = core.apply_result(corrected, m.SuppliedResult(action.id,m.ActionResult.PASS,inventory,c.snapshot_id(corrected))).snapshot
        self.assertEqual(c.snapshot_id(replayed), c.snapshot_id(target))
        self.assertNotIn(m.ActionId('E2-FINISH'), core.recompute(target).actionable)

    def test_g01_g04_and_t01_ancestry(self):
        b = gb.decode_bundle((D/'DETERMINISTIC_PLANNER_V0_1_E2_GENESIS_PERSISTENCE_BUNDLE.json').read_bytes())
        self.assertTrue(gb.validate_genesis_bundle(b)); self.assertTrue(b.trusted)
        self.assertEqual(gb.bundle_identity(gb.decode_bundle(gb.encode_bundle(b))), gb.bundle_identity(b))
        from adapter.planner.genesis_event import validate_genesis_event
        from adapter.planner.genesis_ledger import validate_ledger
        self.assertTrue(validate_genesis_event(b.genesis_event)); self.assertTrue(validate_ledger(b.ledger))
        from types import SimpleNamespace
        contract = SimpleNamespace(source_snapshot=c.snapshot_id(b.current), scope=b.scope, lineage=b.lineage)
        report = json.loads((D/'DETERMINISTIC_PLANNER_V0_1_GENESIS_G04_RESULT.json').read_text())
        auth = m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY, 'authorization-evidence-v1', report['e2_authorization_evidence'])
        rebuilt = gb.begin_event_lineage(b.current, auth, contract, b.provenance)
        self.assertEqual(gb.bundle_identity(rebuilt),gb.bundle_identity(b))
        with self.assertRaises(m.PlannerError): validate_genesis_event(replace(b.genesis_event,parent_event_id=b.source_snapshot))
        post = gb.decode_bundle((D/'DETERMINISTIC_PLANNER_V0_1_E2_P03_POST_RECEIPT_BUNDLE.json').read_bytes())
        self.assertTrue(validate_ledger(post.ledger)); self.assertTrue(post.trusted)

if __name__ == '__main__': unittest.main()
