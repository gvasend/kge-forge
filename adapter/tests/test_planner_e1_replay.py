"""P04 E–I historical slices and explicitly synthetic lifecycle controls; no E1 execution."""
from dataclasses import replace
import hashlib
import itertools
import json
from pathlib import Path
import tempfile
import unittest

from adapter.planner import model as m, core, codec as c, gates, replay, selector

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / 'adapter/tests/fixtures/planner_v0_1'


def fixture(case):
    return replay.load_p04_fixture(FIXTURES / (case + '_P04.json'), ROOT)


def result(state, action=None):
    action_id = core.recompute(state).selection.selected if action is None else m.ActionId(action)
    a = next(a for a in state.actions if a.id == action_id)
    return m.SuppliedResult(a.id, a.accepted_result, a.accepted_inventory, c.snapshot_id(state), a.prepared_dossier)


def decision(state, name):
    return next(d for d in state.decisions if d.action.value == name)


def bundle(state):
    provenances = c.decision_provenances(state) + [a.source for a in state.actions]
    provenances += [k.provenance for k in state.knowledge]
    provenances += [k.provenance for a in state.actions for k in a.accepted_inventory]
    provenances += [e.provenance for e in state.entities]
    pins = {(p.path, p.identity): m.ArtifactPin(p.path, p.identity) for p in provenances}
    path = 'docs/experiments/E1/E1_GRAPH_RESOLUTION_SELECTION_POLICY_1.md'
    policy = m.ArtifactPin(path, m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY, 'raw-file-sha256', hashlib.sha256((ROOT / path).read_bytes()).hexdigest()))
    return m.PersistenceBundle(state, (), state, tuple(pins.values()), policy, 'E1-SELECTION-1-P04')


def reorder(value):
    if isinstance(value, dict):
        return {k: reorder(v) for k, v in reversed(tuple(value.items()))}
    if isinstance(value, list):
        return [reorder(v) for v in value]
    return value


class P04ReplayTests(unittest.TestCase):
    def assert_unchanged(self, before, after):
        self.assertEqual(before.roots, after.roots)
        self.assertEqual(before.slots, after.slots)
        self.assertTrue(all(d.recorded_choice is None and d.record is None for d in after.decisions))

    def test_e_inventory_pass_keeps_domains_unchanged(self):
        # GIVEN original E slice; WHEN both bounded inventories PASS; THEN knowledge only;
        # MUST NOT interpret completion as root/slot satisfaction.
        initial, _ = fixture('E')
        first = core.apply_result(initial, result(initial))
        self.assertEqual(first.computation.selection.selected.value, 'S-CONTEXT')
        second = core.apply_result(first.snapshot, result(first.snapshot))
        self.assert_unchanged(initial, second.snapshot)
        self.assertGreater(len(second.snapshot.knowledge), len(first.snapshot.knowledge))

    def test_f_authority_required_routes_without_ready_decision(self):
        # GIVEN independent exec policy absent; WHEN accepted semantic gap arrives;
        # THEN retain gap and explicit route; MUST NOT invent policy or human readiness.
        s, oracle = fixture('F'); after = s
        d = decision(after, 'DEC-EXEC')
        self.assertEqual(d.stage, m.DecisionStage.DECISION_INPUTS_REQUIRED)
        self.assertEqual(d.external_input, 'EXT-REENTRY-DEC-EXEC')
        self.assertEqual(gates.decision_readiness(after, d).state, m.DecisionReadiness.FACT_BLOCKED)
        self.assertEqual(core.recompute(after).actionable, ())
        self.assertTrue(after.knowledge)
        self.assert_unchanged(s, after)

    def test_g_budget_ready_keeps_machine_priority(self):
        # GIVEN accepted semantic inputs and exact unadopted dossier; WHEN input PASS;
        # THEN all nine checks independently prove readiness; MUST NOT adopt a policy.
        s, oracle = fixture('G'); after = core.apply_result(s, result(s)).snapshot
        d = decision(after, 'DEC-BUDGET'); comp = core.recompute(after)
        self.assertEqual(d.stage, m.DecisionStage.DECISION_READY)
        self.assertEqual(d.history, (m.DecisionStage.DECISION_INPUTS_REQUIRED,
            m.DecisionStage.DECISION_INPUT_ACQUISITION, m.DecisionStage.DECISION_DOSSIER_READY, m.DecisionStage.DECISION_READY))
        self.assertEqual(gates.decision_readiness(after, d).state, m.DecisionReadiness.DECISION_READY)
        self.assertEqual([a.value for a in comp.actionable], oracle['actionable'])
        self.assertEqual(comp.selection.selected.value, oracle['next'])
        self.assertEqual(comp.selection.criterion, oracle['criterion'])
        self.assertEqual(comp.human_batches, ())
        self.assertTrue(d.dossier.deferred_downstream_facts)
        self.assert_unchanged(s, after)

    def test_h_partial_knowledge_survives_blocked_result(self):
        # GIVEN missing implementation owner/selector; WHEN partial output accepted;
        # THEN blocked action + accepted knowledge; MUST NOT choose runtime equivalence.
        s, oracle = fixture('H'); after = core.apply_result(s, result(s)).snapshot
        d = decision(after, 'DEC-IMPLEMENTATION'); ready = gates.decision_readiness(after, d)
        self.assertEqual(ready.state, m.DecisionReadiness.FACT_BLOCKED)
        self.assertEqual(set(ready.missing), {'DEC-IMPLEMENTATION:IMPLEMENTATION-OWNING-SOURCE', 'DEC-IMPLEMENTATION:IMPLEMENTATION-SELECTOR'})
        self.assertEqual(next(a.state for a in after.statuses if a.id.value == 'INPUT-IMPLEMENTATION'), m.ActionState.BLOCKED)
        self.assertGreater(len(after.knowledge), len(s.knowledge))
        comp = core.recompute(after)
        self.assertEqual([a.value for a in comp.actionable], oracle['actionable'])
        self.assertIsNone(comp.selection)
        self.assertEqual(comp.human_routing, m.HumanRouting.HUMAN_HANDOFF)
        self.assertEqual(comp.human_batches, ((m.ActionId('DEC-BUDGET'),),))
        self.assert_unchanged(s, after)

    def test_i_batch_retains_independent_semantics_no_automatic_decision(self):
        # GIVEN separate Batch-1 stage; WHEN readiness recomputed;
        # THEN exactly three ready decisions batched; MUST NOT include fact-blocked EXEC.
        s, oracle = fixture('I'); comp = core.recompute(s)
        self.assertEqual([[a.value for a in b] for b in comp.human_batches], oracle['batches'])
        self.assertIsNone(comp.selection)
        self.assertEqual(comp.human_routing, m.HumanRouting.HUMAN_HANDOFF)
        self.assertEqual([a.value for a in comp.actionable], oracle['actionable'])
        self.assertEqual(len({decision(s, a.value).dossier.scope for a in comp.actionable}), 3)
        # Pure selector remains total; scheduler does not call it for human-only work.
        self.assertIsNotNone(selector.select(tuple(a for a in s.actions if a.id in comp.actionable)))
        with self.assertRaises(m.PlannerError):
            core.apply_result(s, result(s, 'DEC-BINDING'))

    def test_i_synthetic_interference_and_dependencies_not_merged(self):
        s, _ = fixture('I'); left = decision(s, 'DEC-BINDING'); right = decision(s, 'DEC-IGNORED')
        s = replace(s, decisions=tuple(replace(d, interferes_with=(right.action,)) if d == left else d for d in s.decisions))
        groups = core.recompute(s).human_batches
        self.assertFalse(any(left.action in g and right.action in g for g in groups))
        s = replace(s, decisions=tuple(replace(d, depends_on=(left.action,)) if d == right else d for d in s.decisions))
        self.assertNotIn(right.action, core.recompute(s).actionable)
        self.assertIn(left.action, core.recompute(s).actionable)

    def test_x05_all_nine_checks_required_not_majority_vote(self):
        s, _ = fixture('G'); good = core.apply_result(s, result(s)).snapshot
        d = decision(good, 'DEC-BUDGET')
        for check in d.dossier.checks:
            mutated = replace(good, predicates=tuple(replace(p, knowledge=None, unavailable='Required decision check unavailable') if p.id == check.predicate else p for p in good.predicates))
            self.assertNotEqual(gates.decision_readiness(mutated, decision(mutated, 'DEC-BUDGET')).state, m.DecisionReadiness.DECISION_READY)
            self.assertNotIn(d.action, core.recompute(mutated).actionable)
        for kind in m.DossierCheck:
            incomplete = replace(d, dossier=replace(d.dossier, checks=tuple(ch for ch in d.dossier.checks if ch.kind != kind)))
            self.assertNotEqual(gates.decision_readiness(good, incomplete).state, m.DecisionReadiness.DECISION_READY)

    def test_x05_missing_facts_cannot_be_deferred_into_choices(self):
        s, _ = fixture('H'); after = core.apply_result(s, result(s)).snapshot
        d = decision(after, 'DEC-IMPLEMENTATION')
        for ref in d.dossier.required_facts:
            # Proving only one missing fact cannot qualify both.
            p = next(p for p in after.predicates if p.id == ref)
            modified = replace(after, knowledge=tuple(replace(k, state=m.KnowledgeState.KNOWN_COMPLETE) if k.id == p.knowledge else k for k in after.knowledge))
            self.assertEqual(gates.decision_readiness(modified, d).state, m.DecisionReadiness.FACT_BLOCKED)
        self.assert_unchanged(s, after)

    def test_x07_pass_cannot_bypass_incomplete_input_contract(self):
        s, _ = fixture('H'); r = result(s)
        with self.assertRaises(m.PlannerError):
            core.apply_result(s, replace(r, result=m.ActionResult.PASS))
        actions = tuple(replace(a, accepted_result=m.ActionResult.PASS) if a.id == r.action else a for a in s.actions)
        forged = replace(s, actions=actions)
        with self.assertRaises(m.PlannerError):
            core.apply_result(forged, result(forged))
        with self.assertRaises(m.PlannerError):
            core.apply_result(s, replace(r, dossier=None))
        with self.assertRaises(m.PlannerError):
            core.apply_result(s, replace(r, knowledge=()))

    def test_missing_semantic_input_blocks_acquisition(self):
        s, _ = fixture('G'); missing = {k.id for k in s.knowledge}
        s = replace(s, knowledge=())
        # C01 rejects dangling references. Intentional missing facts must be
        # explicit; removing facts alone cannot leave an admitted reference.
        with self.assertRaises(m.PlannerError):
            core.recompute(s)
        s = replace(s, predicates=tuple(replace(p, knowledge=None,
            unavailable='Required semantic input unavailable') if p.knowledge in missing else p
            for p in s.predicates))
        self.assertEqual(core.recompute(s).actionable, ())
        with self.assertRaises(m.PlannerError):
            core.apply_result(s, result(s, 'INPUT-BUDGET'))

    def test_out_of_order_reentry_and_lifecycle_shortcuts_rejected(self):
        s, _ = fixture('G')
        with self.assertRaises(m.PlannerError):
            core.apply_decision_reentry(s, m.DecisionReentry(m.ActionId('DEC-BUDGET'), c.snapshot_id(s)))
        d = decision(s, 'DEC-BUDGET')
        bad = replace(d, history=(m.DecisionStage.SEMANTIC_GAP_IDENTIFIED, m.DecisionStage.DECISION_READY), stage=m.DecisionStage.DECISION_READY)
        with self.assertRaises(m.PlannerError):
            c.snapshot_bytes(replace(s, decisions=(bad,)))
        after = core.apply_result(s, result(s)).snapshot
        with self.assertRaises(m.PlannerError):
            core.apply_result(after, result(s))

    def test_x10_stale_dossier_and_indirect_checks_block_readiness(self):
        s, _ = fixture('G'); after = core.apply_result(s, result(s)).snapshot
        d = decision(after, 'DEC-BUDGET')
        for source in (d.dossier.provenance.identity, d.dossier.checks[-1].provenance.identity):
            stale = c.invalidate_sources(after, (source,))
            self.assertEqual(gates.decision_readiness(stale, decision(stale, 'DEC-BUDGET')).state, m.DecisionReadiness.STALE)
            self.assertNotIn(d.action, core.recompute(stale).actionable)
            restored = c.decode_snapshot(c.snapshot_bytes(stale))
            self.assertEqual(core.recompute(stale), core.recompute(restored))
            self.assertIn(m.ActionId('INPUT-IMPLEMENTATION'), core.recompute(stale).actionable)

    def test_each_case_roundtrip_append_only_replay(self):
        for case in 'EFGHI':
            s, _ = fixture(case); b = bundle(s)
            if case not in ('F', 'I'):
                b = c.record_result(b, result(s))
                self.assertEqual(len(b.events), 1)
                self.assertEqual(c.append_event(b, b.events[0]), b)
            with tempfile.TemporaryDirectory() as directory:
                path, identity = c.save_bundle(b, directory, ROOT)
                restored = c.restore(path, identity, ROOT)
                self.assertEqual(c.bundle_bytes(b), c.bundle_bytes(restored))
                self.assertEqual(core.recompute(b.current), core.recompute(restored.current))
                self.assertEqual(c.snapshot_bytes(b.current), c.snapshot_bytes(restored.current))
                self.assertEqual(c.snapshot_bytes(b.initial), c.snapshot_bytes(restored.initial))

    def test_permutation_key_reversal_and_repeated_replay(self):
        for case in 'FGHI':
            s, _ = fixture(case); expected = core.recompute(s); before = c.snapshot_bytes(s)
            expected_after = None if case in ('F', 'I') else c.snapshot_bytes(core.apply_result(s, result(s)).snapshot)
            for order in itertools.permutations(s.actions):
                shuffled = replace(s, actions=order, statuses=tuple(reversed(s.statuses)),
                    predicates=tuple(reversed(s.predicates)), knowledge=tuple(reversed(s.knowledge)),
                    decisions=tuple(reversed(s.decisions)))
                self.assertEqual(c.snapshot_bytes(shuffled), before)
                self.assertEqual(core.recompute(shuffled), expected)
                if case not in ('F', 'I'):
                    self.assertEqual(c.snapshot_bytes(core.apply_result(shuffled, result(shuffled)).snapshot), expected_after)
            for _ in range(10):
                s = c.decode_snapshot(json.dumps(reorder(json.loads(c.snapshot_bytes(s)))))
                self.assertEqual(c.snapshot_bytes(s), before)
                self.assertEqual(core.recompute(s), expected)

    def test_unknown_enums_fields_duplicates_and_prestate_fail_closed(self):
        s, _ = fixture('G'); raw = c.snapshot_bytes(s)
        with self.assertRaises(m.PlannerError):
            c.decode_snapshot(raw.replace(b'DECISION_INPUTS_REQUIRED', b'IMPLICITLY_READY'))
        with self.assertRaises(m.PlannerError):
            c.snapshot_bytes(replace(s, decisions=s.decisions + (s.decisions[0],)))
        with self.assertRaises(m.PlannerError):
            core.apply_result(s, replace(result(s), expected_snapshot=None))
        with self.assertRaises(m.PlannerError):
            c.bundle_bytes(replace(bundle(s), policy_version='E1-SELECTION-1-P03'))
        after=core.apply_result(s,result(s)).snapshot
        d=decision(after,'DEC-BUDGET')
        bad=replace(after,decisions=tuple(replace(x,dossier=replace(d.dossier,decision=m.ActionId('DEC-IMPLEMENTATION')))
            if x.action==d.action else x for x in after.decisions))
        with self.assertRaises(m.PlannerError): core.recompute(bad)
        orphan=replace(s,decisions=(),actions=tuple(replace(a,prepared_dossier=None) for a in s.actions if a.id.value=='INPUT-BUDGET'),
            statuses=(m.ActionStatus(m.ActionId('INPUT-BUDGET'),m.ActionState.ACTION_ELIGIBLE),))
        with self.assertRaises(m.PlannerError):
            core.recompute(orphan)
        known = {k.id for k in orphan.knowledge} | {k.id for a in orphan.actions for k in a.accepted_inventory}
        orphan = replace(orphan, predicates=tuple(replace(p, knowledge=None,
            unavailable='Output producer absent from isolated route') if p.knowledge is not None and p.knowledge not in known else p
            for p in orphan.predicates))
        self.assertEqual(core.recompute(orphan).actionable,())

    def test_fixture_projection_and_source_tampering_rejected(self):
        data = json.loads((FIXTURES / 'G_P04.json').read_text())
        for field, value in (('excerpt', 'invented'), ('sha256', '0' * 64)):
            variant = json.loads(json.dumps(data)); variant['sources'][0][field] = value
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / 'fixture.json'; path.write_text(json.dumps(variant))
                with self.assertRaises(m.PlannerError):
                    replay.load_p04_fixture(path, ROOT)


    def test_semantic_authority_requirement_needs_independent_readiness(self):
        # Synthetic semantic-result mutation, not the historical S-EXEC PASS result.
        s, _ = fixture('F'); d = s.decisions[0]; aid = m.ActionId('TEST-SEMANTIC')
        old = next(a for a in s.actions if a.id.value == 'S-EXEC')
        action = replace(old, id=aid, operation=m.OperationClass.SEMANTIC_RESOLUTION, accepted_result=m.ActionResult.AUTHORITY_REQUIRED)
        s = replace(s, actions=tuple(action if a==old else a for a in s.actions),
            statuses=tuple(m.ActionStatus(a.id,m.ActionState.ACTION_ELIGIBLE) for a in (action,next(a for a in s.actions if a.id.value=='DEC-EXEC'))),
            decisions=(replace(d, semantic_action=aid, stage=m.DecisionStage.SEMANTIC_GAP_IDENTIFIED),),knowledge=())
        after = core.apply_result(s, result(s)).snapshot
        self.assertEqual(decision(after,'DEC-EXEC').stage, m.DecisionStage.DECISION_INPUTS_REQUIRED)
        self.assertEqual(core.recompute(after).actionable, ())
        self.assertTrue(after.knowledge)
        self.assert_unchanged(s,after)
        b=c.record_result(bundle(s),result(s))
        with tempfile.TemporaryDirectory() as directory:
            path,identity=c.save_bundle(b,directory,ROOT)
            self.assertEqual(c.bundle_bytes(c.restore(path,identity,ROOT)),c.bundle_bytes(b))

    def test_machine_priority_even_when_coverage_prefers_human(self):
        s,_=fixture('H')
        # Pure selector may favor a human by an explicit comparable metric. Scheduler
        # never auto-executes one while machine work is independently available.
        from unittest.mock import patch
        with patch('adapter.planner.core.coverage_scores', return_value={
            m.ActionId('DEC-BUDGET'):(10,10,10),m.ActionId('INPUT-IMPLEMENTATION'):(0,0,0)}):
            self.assertEqual(core.recompute(s).selection.selected,m.ActionId('INPUT-IMPLEMENTATION'))

    def test_recorded_decision_import_and_explicit_reentry_are_separate_events(self):
        # COUNTERFACTUAL_SYNTHETIC admitted record, scoped to one dossier. No authority is issued.
        s,_=fixture('I');d=decision(s,'DEC-BINDING');p=d.provenance
        target=m.ActionId('TEST-DOWNSTREAM')
        actions=s.actions+(m.Action(target,m.OperationClass.DETERMINISTIC_MAPPING,m.EffectClass.NON_EFFECTING,(),p,()),)
        record=m.GraphEntity(m.EntityId('TEST-RECORDED-DECISION'),m.EntityKind.AUTHORITY,
            m.ArtifactIdentity(m.IdentityKind.AUTHORITY_IDENTITY,'test-record','1'*64),p,
            d.dossier.scope,'TEST-LINEAGE','TEST-GENERATION',10,
            permissions=(m.AuthorityClass.DECIDE,),target=d.dossier.provenance.identity,decision=d.action,choice=d.dossier.alternatives[0])
        predicate=m.Predicate(m.PredicateId('TEST-RECORD-AUTH'),m.PredicateKind.AUTHORITY,entity=record.id,
            expected=d.dossier.provenance.identity,permission=m.AuthorityClass.DECIDE)
        choice=d.dossier.alternatives[0]
        observation=m.KnowledgeRecord(m.KnowledgeId('decision-choice:'+d.action.value),m.KnowledgeState.KNOWN_COMPLETE,choice,p)
        s=replace(s,actions=actions,statuses=s.statuses+(m.ActionStatus(target,m.ActionState.BLOCKED),),
            decisions=tuple(replace(x,downstream=(target,)) if x.action==d.action else x for x in s.decisions),
            entities=(record,),predicates=s.predicates+(predicate,),knowledge=s.knowledge+(observation,),
            context=m.EvaluationContext(d.dossier.scope,'TEST-LINEAGE','TEST-GENERATION',1))
        event=m.RecordedDecision(d.action,choice,record.id,predicate.id,c.snapshot_id(s))
        for mutated in (replace(event,choice='UNLISTED'),replace(event,expected_snapshot=m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY,'planner-snapshot-v1','0'*64))):
            with self.assertRaises(m.PlannerError): core.apply_recorded_decision(s,mutated)
        for badrecord in (replace(record,decision=m.ActionId('DEC-IGNORED')),replace(record,choice='UNLISTED'),replace(record,permissions=(m.AuthorityClass.CONSTRUCT,)),replace(record,consumed=True),replace(record,scope='WRONG'),replace(record,valid_until=0),replace(record,target=m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY,'raw-file-sha256','2'*64))):
            bad=replace(s,entities=(badrecord,))
            with self.assertRaises(m.PlannerError): core.apply_recorded_decision(bad,replace(event,expected_snapshot=c.snapshot_id(bad)))
        b=c.record_result(bundle(s),event);after=b.current
        self.assertEqual(decision(after,d.action.value).stage,m.DecisionStage.DECISION_RECORDED)
        self.assertNotIn(target,core.recompute(after).actionable)
        self.assertEqual(s.roots,after.roots);self.assertEqual(s.slots,after.slots)
        self.assertEqual(s.entities,after.entities)
        with self.assertRaises(m.PlannerError):
            core.apply_recorded_decision(after,replace(event,expected_snapshot=c.snapshot_id(after)))
        self.assertFalse(core.resume_eligibility(b,ROOT).allowed)
        reentry=m.DecisionReentry(d.action,c.snapshot_id(after));b=c.record_result(b,reentry)
        self.assertTrue(core.resume_eligibility(b,ROOT).allowed)
        self.assertEqual(core.resume_eligibility(b,ROOT).actions,(target,))
        self.assertEqual(decision(b.current,d.action.value).stage,m.DecisionStage.DOWNSTREAM_REEVALUATION)
        self.assertIn(target,core.recompute(b.current).actionable)
        self.assertEqual(s.roots,b.current.roots);self.assertEqual(s.slots,b.current.slots)
        with tempfile.TemporaryDirectory() as directory:
            path,identity=c.save_bundle(b,directory,ROOT)
            restored=c.restore(path,identity,ROOT)
            self.assertEqual(c.bundle_bytes(b),c.bundle_bytes(restored))
        # An accepted conflicting decision makes the other dossier unusable pending revalidation.
        conflict=replace(s,decisions=tuple(replace(x,interferes_with=(m.ActionId('DEC-IGNORED'),)) if x.action==d.action else x for x in s.decisions))
        changed=core.apply_recorded_decision(conflict,replace(event,expected_snapshot=c.snapshot_id(conflict))).snapshot
        self.assertEqual(gates.decision_readiness(changed,decision(changed,'DEC-IGNORED')).state,m.DecisionReadiness.STALE)
        self.assertNotIn(m.ActionId('DEC-IGNORED'),core.recompute(changed).actionable)
        # Stale source blocks reentry even though the historical record remains recorded.
        stale=c.invalidate_sources(after,(p.identity,))
        with self.assertRaises(m.PlannerError):
            core.apply_decision_reentry(stale,m.DecisionReentry(d.action,c.snapshot_id(stale)))


    def test_accepted_input_reenters_only_its_held_decision(self):
        s,_=fixture('G')
        s=replace(s,statuses=tuple(replace(st,state=m.ActionState.BLOCKED) if st.id.value.startswith('DEC-') else st for st in s.statuses))
        after=core.apply_result(s,result(s)).snapshot
        self.assertIn(m.ActionId('DEC-BUDGET'),core.recompute(after).actionable)
        self.assertNotIn(m.ActionId('DEC-IMPLEMENTATION'),core.recompute(after).actionable)

    def test_nested_dossier_permutation_accepts_same_semantic_event(self):
        s,_=fixture('G');event=result(s)
        def permute(dossier):
            return replace(dossier,checks=tuple(reversed(dossier.checks)),alternatives=tuple(reversed(dossier.alternatives)),
                required_facts=tuple(reversed(dossier.required_facts)),deferred_downstream_facts=tuple(reversed(dossier.deferred_downstream_facts))) if dossier is not None else None
        reordered=replace(s,actions=tuple(replace(a,prepared_dossier=permute(a.prepared_dossier)) for a in s.actions))
        self.assertEqual(c.snapshot_id(s),c.snapshot_id(reordered))
        self.assertEqual(c.snapshot_bytes(core.apply_result(s,event).snapshot),c.snapshot_bytes(core.apply_result(reordered,event).snapshot))

    def test_human_review_is_not_effect_permission_and_input_cannot_effect(self):
        from unittest.mock import patch
        s,_=fixture('I')
        self.assertTrue(all(a.effect is m.EffectClass.PRODUCTION_EFFECT for a in s.actions))
        with patch('builtins.open',side_effect=AssertionError('no file effect')), patch('socket.socket',side_effect=AssertionError('no network')):
            self.assertEqual(core.recompute(s).human_routing,m.HumanRouting.HUMAN_HANDOFF)
            with self.assertRaises(m.PlannerError):core.apply_result(s,result(s,'DEC-BINDING'))
        s,_=fixture('G')
        bad=replace(s,actions=tuple(replace(a,effect=m.EffectClass.PRODUCTION_EFFECT) if a.id.value=='INPUT-BUDGET' else a for a in s.actions))
        with self.assertRaises(m.PlannerError): core.recompute(bad)

    def test_decision_dependency_cycle_fails_closed(self):
        s,_=fixture('I');left=m.ActionId('DEC-BINDING');right=m.ActionId('DEC-IGNORED')
        cycle=replace(s,decisions=tuple(replace(d,depends_on=(right,)) if d.action==left else
            replace(d,depends_on=(left,)) if d.action==right else d for d in s.decisions))
        self.assertIn('PREREQUISITE_CYCLE',core.project(cycle).defects)
        self.assertEqual(core.recompute(cycle).actionable,())



def p05_fixture(case):
    return replay.load_p05_fixture(FIXTURES/(case+'_P05.json'),ROOT)


def p05_bundle(state):
    b=bundle(state)
    pins={(p.path,p.identity):p for p in b.sources}
    for p in c.external_provenances(state)+[a.provenance for a in state.assertions]:
        pins[(p.path,p.identity)]=m.ArtifactPin(p.path,p.identity)
    return replace(b,sources=tuple(pins.values()),policy_version='E1-SELECTION-1-P05')


def external_event(state,stage,artifact=None):
    return m.ExternalEvent(state.external_gates[0].id,stage,c.snapshot_id(state),artifact)


def synthetic_receipt(state,claims=None,auth=True):
    """COUNTERFACTUAL_SYNTHETIC admitted trust; never actual E1 evidence."""
    context=m.EvaluationContext('TEST-REQUEST','TEST-LINEAGE','TEST-GENERATION',10)
    producer=m.ArtifactIdentity(m.IdentityKind.AUTHORITY_IDENTITY,'TEST-attestor','a'*64)
    target=m.ArtifactIdentity(m.IdentityKind.AUTHORITY_IDENTITY,'TEST-budget','b'*64)
    requirements=tuple(replace(r,producers=(producer,),target=target) for r in state.evidence_requirements)
    claims=tuple(m.EvidenceClaim(r.id,m.ProofState.PROVED) for r in requirements) if claims is None else claims
    raw=c.canonical_bytes({'producer':c._wire(producer),'target':c._wire(target),
                          'claims':sorted((c._wire(cl) for cl in claims),key=c.canonical_bytes)})
    identity=m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY,'raw-file-sha256',hashlib.sha256(raw).hexdigest())
    source=m.Provenance('synthetic/receipt.json',identity,'/','COUNTERFACTUAL_SYNTHETIC '+raw.decode(),'TEST_ADMISSION','TEST-REQUEST')
    entity=m.GraphEntity(m.EntityId('TEST-RECEIPT'),m.EntityKind.EVIDENCE,identity,source,context.scope,context.lineage,context.generation,20)
    trust_raw=c.canonical_bytes({'test_only':'COUNTERFACTUAL_SYNTHETIC_TRUST_ROOT','producer':c._wire(producer),'target':c._wire(identity)})
    trust_source=m.Provenance('synthetic/trust.json',m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY,'raw-file-sha256',hashlib.sha256(trust_raw).hexdigest()),'/',trust_raw.decode(),'EXPLICIT_SYNTHETIC_TRUST','TEST-REQUEST')
    trust=replace(entity,id=m.EntityId('TEST-TRUST'),kind=m.EntityKind.AUTHORITY,identity=producer,provenance=trust_source,
                  permissions=(m.AuthorityClass.ATTEST,) if auth else (),target=identity)
    pid=m.PredicateId('TEST-AUTHENTICATION')
    predicate=m.Predicate(pid,m.PredicateKind.AUTHORITY,entity=trust.id,expected=identity,permission=m.AuthorityClass.ATTEST)
    admission=m.ReceiptAdmission(entity.id,producer,target,claims,pid,source)
    state=replace(state,context=context,evidence_requirements=requirements,entities=state.entities+(entity,trust),
                  predicates=state.predicates+(predicate,),receipt_admissions=(admission,))
    return state,entity


class P05ReplayTests(unittest.TestCase):
    def waiting(self):
        s,_=p05_fixture('K')
        for stage in (m.ExternalStage.EVIDENCE_REQUEST_READY,m.ExternalStage.WAITING_FOR_EXTERNAL_EVIDENCE):
            s=core.apply_receipt(s,external_event(s,stage)).snapshot
        return s

    def receive(self,s,entity):
        s=core.apply_receipt(s,external_event(s,m.ExternalStage.EVIDENCE_RECEIVED,entity.id)).snapshot
        return core.apply_receipt(s,external_event(s,m.ExternalStage.EVIDENCE_VALIDATED)).snapshot

    def test_j_authority_reference_does_not_prove_applicability(self):
        # GIVEN reference only; WHEN fact result accepted; THEN eight unknowns;
        # MUST NOT turn identity consistency into scope, freshness or permission.
        s,_=p05_fixture('J');after=core.apply_result(s,result(s)).snapshot
        self.assertEqual(len(after.knowledge),1)
        contract=json.loads(after.knowledge[0].statement)
        self.assertEqual(contract['identity_type'],'AUTHORITY_IDENTITY')
        self.assertEqual(contract['authoritative_selector'],'/authority_id')
        self.assertEqual(contract['exact_value'],'StatusBudgetAuthority-sha256:'+after.evidence_requirements[0].target.sha256)
        for r in after.evidence_requirements:
            self.assertEqual(gates.obligation_proof(after,r.id).state,m.ProofState.UNKNOWN)
        self.assertEqual(after.roots,s.roots);self.assertEqual(after.slots,s.slots)
        self.assertEqual(core.recompute(after).actionable,())
        self.assertEqual(next(st.state for st in after.statuses if st.id.value=='FACT-BUDGET-APPLICABILITY'),m.ActionState.BLOCKED)

    def test_k_request_wait_received_validated_are_separate(self):
        # GIVEN request contract only; WHEN control transfers; THEN waiting;
        # MUST NOT infer sending, evidence arrival or domain satisfaction.
        s=self.waiting();comp=core.recompute(s)
        self.assertEqual(comp.control,m.ControlState.EXTERNAL_WAIT)
        self.assertEqual(comp.actionable,());self.assertIsNone(comp.selection)
        self.assertEqual(s.receipt_observations,())
        with self.assertRaises(m.PlannerError):
            core.apply_receipt(s,external_event(s,m.ExternalStage.EVIDENCE_VALIDATED))
        with self.assertRaises(m.PlannerError):
            core.apply_receipt(s,external_event(s,m.ExternalStage.EVIDENCE_RECEIVED))
        self.assertEqual([g.value for g,_ in comp.frontier],['EXT-BUDGET-APPLICABILITY-EVIDENCE'])

    def test_l_independent_work_runs_while_budget_waits(self):
        # GIVEN explicitly synthetic independent work; WHEN PASS; THEN only its
        # knowledge changes; MUST NOT reopen the waiting budget branch.
        s,_=p05_fixture('L');comp=core.recompute(s)
        self.assertEqual(comp.control,m.ControlState.RUNNABLE)
        self.assertEqual(comp.selection.selected.value,'TEST-INDEPENDENT')
        after=core.apply_result(s,result(s)).snapshot
        self.assertEqual(after.external_gates,s.external_gates)
        self.assertEqual(after.roots,s.roots);self.assertEqual(after.slots,s.slots)
        self.assertEqual(core.recompute(after).control,m.ControlState.EXTERNAL_WAIT)

    def test_m_full_readiness_population_and_exact_frontier(self):
        # GIVEN all frozen root/slot/action definitions, not report totals; WHEN
        # recomputed; THEN exact frontier/counts; MUST NOT select reasoning work.
        s,oracle=p05_fixture('M');comp=core.recompute(s)
        self.assertEqual((len(s.roots),len(s.slots),len(s.actions)),(28,43,63))
        self.assertEqual((comp.unresolved_roots,comp.unresolved_slots),(27,41))
        self.assertEqual(comp.control,m.ControlState.MIXED_WAIT)
        self.assertEqual(comp.actionable,());self.assertEqual(comp.defects,())
        self.assertEqual({g.value for g,_ in comp.frontier},set(oracle['frontier']))
        self.assertTrue(all(witnesses for _,witnesses in comp.frontier))
        self.assertNotIn('EXT-CURRENT-ELIGIBILITY-EVIDENCE',{g.value for g,_ in comp.frontier})
        # Removing the admitted validator grant changes the count: no hardcoded 27.
        removed = {k.id for k in s.knowledge}
        changed=replace(s,knowledge=(), predicates=tuple(replace(p, knowledge=None,
            unavailable='Validator grant evidence unavailable') if p.knowledge in removed else p
            for p in s.predicates))
        self.assertEqual(core.recompute(changed).unresolved_roots,28)
        graph=json.loads((ROOT/'docs/experiments/E1/E1_TEMPLATE1_TYPED_KNOWLEDGE_GRAPH_1.json').read_text())
        self.assertEqual({v.id.value for v in s.slots},{e['id'] for e in graph['entities'] if e['entity_type']=='TEMPLATE1_SLOT'})

    def test_x01_current_scope_lineage_generation_and_expiry_are_independent(self):
        s,entity=synthetic_receipt(self.waiting());gate=s.external_gates[0]
        self.assertEqual(gates.check_receipt(s,gate,entity.id).state,m.ProofState.PROVED)
        for field,value in (('scope','TEST-EXECUTION'),('lineage','HISTORICAL'),('generation','OLD'),('valid_until',9)):
            old=replace(entity,**{field:value});variant=replace(s,entities=tuple(old if e.id==entity.id else e for e in s.entities))
            self.assertNotEqual(gates.check_receipt(variant,gate,entity.id).state,m.ProofState.PROVED)
            after=self.receive(variant,entity)
            self.assertFalse(after.receipt_observations[-1].accepted)
            self.assertEqual(after.external_gates[0].stage,m.ExternalStage.WAITING_FOR_EXTERNAL_EVIDENCE)
        # Same bytes/identity without producer authority also fails.
        untrusted,entity=synthetic_receipt(self.waiting(),auth=False)
        self.assertNotEqual(gates.check_receipt(untrusted,untrusted.external_gates[0],entity.id).state,m.ProofState.PROVED)

    def test_x04_every_proposition_required_and_complete_positive_control(self):
        s=self.waiting()
        for missing in range(8):
            claims=tuple(m.EvidenceClaim(r.id,m.ProofState.PROVED) for i,r in enumerate(s.evidence_requirements) if i!=missing)
            variant,entity=synthetic_receipt(s,claims);after=self.receive(variant,entity)
            self.assertTrue(after.receipt_observations[-1].accepted)
            self.assertEqual(after.external_gates[0].stage,m.ExternalStage.WAITING_FOR_EXTERNAL_EVIDENCE)
            self.assertFalse(gates.external_complete(after,after.external_gates[0]))
        complete,entity=synthetic_receipt(s);validated=self.receive(complete,entity)
        self.assertEqual(validated.external_gates[0].stage,m.ExternalStage.EVIDENCE_VALIDATED)
        self.assertTrue(gates.external_complete(validated,validated.external_gates[0]))
        self.assertEqual(core.recompute(validated).actionable,())
        reopened=core.apply_receipt(validated,external_event(validated,m.ExternalStage.DEPENDENT_ACTION_REENTRY)).snapshot
        self.assertEqual(core.recompute(reopened).selection.selected.value,'FACT-BUDGET-APPLICABILITY')
        self.assertEqual(reopened.roots,s.roots);self.assertEqual(reopened.slots,s.slots)
        self.assertNotIn(m.ActionId('MAP-BUDGET'),core.recompute(reopened).actionable)

    def test_negative_partial_unrelated_and_malformed_receipts(self):
        base=self.waiting()
        negative=tuple(m.EvidenceClaim(r.id,m.ProofState.DISPROVED if i==0 else m.ProofState.PROVED) for i,r in enumerate(base.evidence_requirements))
        s,entity=synthetic_receipt(base,negative);after=self.receive(s,entity)
        self.assertTrue(after.receipt_observations[-1].accepted)
        self.assertEqual(gates.obligation_proof(after,base.evidence_requirements[0].id).state,m.ProofState.DISPROVED)
        self.assertEqual(core.recompute(after).control,m.ControlState.EXTERNAL_WAIT)
        # No failure terminality inferred from a negative currentness proposition.
        s,entity=synthetic_receipt(base,());self.assertFalse(self.receive(s,entity).receipt_observations[-1].accepted)
        s,entity=synthetic_receipt(base)
        for e in (replace(entity,produced=False),replace(entity,validated=False),replace(entity,kind=m.EntityKind.SOURCE)):
            changed=replace(s,entities=tuple(e if x.id==e.id else x for x in s.entities))
            self.assertNotEqual(gates.check_receipt(changed,changed.external_gates[0],e.id).state,m.ProofState.PROVED)
        bad=replace(s,receipt_admissions=(replace(s.receipt_admissions[0],target=m.ArtifactIdentity(m.IdentityKind.AUTHORITY_IDENTITY,'TEST-other','c'*64)),))
        self.assertNotEqual(gates.check_receipt(bad,bad.external_gates[0],entity.id).state,m.ProofState.PROVED)
        # Modifying an admitted claim without changing receipt bytes fails identity.
        bad=replace(s,receipt_admissions=(replace(s.receipt_admissions[0],claims=negative),))
        self.assertIn('RECEIPT_CONTENT_IDENTITY_MISMATCH',gates.check_receipt(bad,bad.external_gates[0],entity.id).reasons)

    def test_all_seven_global_controls_and_local_defect_precedence(self):
        s=self.waiting();self.assertEqual(core.recompute(s).control,m.ControlState.EXTERNAL_WAIT)
        mixed=replace(s,boundaries=(replace(s.boundaries[0],kind=m.BoundaryKind.EXTERNAL_FACT),))
        self.assertEqual(core.recompute(mixed).control,m.ControlState.MIXED_WAIT)
        missing=replace(s,boundaries=())
        self.assertEqual(core.recompute(missing).control,m.ControlState.PLAN_DEFECT)
        success=replace(s,roots=tuple(replace(r,state=m.ConditionState.SATISFIED) for r in s.roots),slots=tuple(replace(v,state=m.SlotState.RESOLVED) for v in s.slots))
        self.assertEqual(core.recompute(success).control,m.ControlState.TERMINAL_SUCCESS)
        record=replace(s.knowledge[0],id=m.KnowledgeId('TEST-UNRECOVERABLE'),statement='COUNTERFACTUAL_SYNTHETIC: required goal has a proven unrecoverable failure')
        p=m.Predicate(m.PredicateId('TEST-UNRECOVERABLE'),m.PredicateKind.KNOWLEDGE_ACCEPTED,knowledge=record.id)
        failed=replace(s,knowledge=s.knowledge+(record,),predicates=s.predicates+(p,),goals=tuple(replace(g,failure=p.id) for g in s.goals))
        self.assertEqual(core.recompute(failed).control,m.ControlState.TERMINAL_FAILURE)
        recovery=replace(failed,goals=tuple(replace(g,recovery=(m.ActionId('FACT-BUDGET-APPLICABILITY'),)) for g in failed.goals))
        self.assertEqual(core.recompute(recovery).control,m.ControlState.EXTERNAL_WAIT)
        human,_=fixture('I');human=replace(human,goals=(m.Goal(human.roots[0].id,(m.ActionId('DEC-BINDING'),),human.actions[0].source),))
        self.assertEqual(core.recompute(human).control,m.ControlState.HUMAN_HANDOFF)
        live,_=p05_fixture('L');live=replace(live,boundaries=(replace(live.boundaries[0],kind=m.BoundaryKind.PLAN_DEFECT),))
        self.assertEqual(core.recompute(live).control,m.ControlState.RUNNABLE)
        self.assertTrue(core.recompute(live).defects)
        # An unsupported required proof cannot be labelled an ordinary evidence wait.
        unknown=replace(s,evidence_requirements=tuple(replace(r,rule_known=False) for r in s.evidence_requirements))
        self.assertEqual(core.recompute(unknown).control,m.ControlState.PLAN_DEFECT)

    def test_control_roundtrip_permutation_and_no_oracle_dependency(self):
        for case in 'JKLM':
            s,oracle=p05_fixture(case);expected=core.recompute(s)
            for state in (s,replace(s,actions=tuple(reversed(s.actions)),statuses=tuple(reversed(s.statuses)),
                    boundaries=tuple(reversed(s.boundaries)),goals=tuple(reversed(s.goals)),
                    evidence_requirements=tuple(reversed(s.evidence_requirements)))):
                for _ in range(2):
                    state=c.decode_snapshot(json.dumps(reorder(json.loads(c.snapshot_bytes(state)))))
                    self.assertEqual(c.snapshot_id(state),c.snapshot_id(s))
                    self.assertEqual(core.recompute(state),expected)
            self.assertEqual(c.bundle_bytes(p05_bundle(s)),c.bundle_bytes(p05_bundle(c.decode_snapshot(c.snapshot_bytes(s)))))

    def test_append_only_wait_lifecycle_persistence(self):
        s,_=p05_fixture('K');b=p05_bundle(s)
        for stage in (m.ExternalStage.EVIDENCE_REQUEST_READY,m.ExternalStage.WAITING_FOR_EXTERNAL_EVIDENCE):
            event=external_event(b.current,stage);b=c.record_result(b,event)
            with tempfile.TemporaryDirectory() as directory:
                path,identity=c.save_bundle(b,directory,ROOT);restored=c.restore(path,identity,ROOT)
                self.assertEqual(c.bundle_bytes(restored),c.bundle_bytes(b))
                self.assertEqual(core.recompute(restored.current),core.recompute(b.current))
        with self.assertRaises(m.PlannerError):c.bundle_bytes(replace(b,policy_version='E1-SELECTION-1-P04'))

    def test_stale_receipt_invalidates_obligations_and_reentry(self):
        s,entity=synthetic_receipt(self.waiting());after=self.receive(s,entity)
        ready=core.apply_receipt(after,external_event(after,m.ExternalStage.DEPENDENT_ACTION_REENTRY)).snapshot
        changed=c.invalidate_sources(ready,(entity.provenance.identity,))
        self.assertEqual(core.recompute(changed).actionable,())
        self.assertFalse(gates.external_complete(changed,changed.external_gates[0]))
        self.assertEqual(core.recompute(c.decode_snapshot(c.snapshot_bytes(changed))),core.recompute(changed))

    def test_receipt_and_reentry_ledger_roundtrip_with_pinned_synthetic_trust(self):
        # Complete synthetic trust is injected before the receipt, never created by it.
        s,entity=synthetic_receipt(self.waiting());b=p05_bundle(s)
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'synthetic').mkdir()
            for pin in b.sources+(b.policy,):
                target=root/pin.path;target.parent.mkdir(parents=True,exist_ok=True)
                if pin.path=='synthetic/receipt.json':
                    admission=s.receipt_admissions[0]
                    target.write_bytes(c.canonical_bytes({'producer':c._wire(admission.producer),'target':c._wire(admission.target),
                        'claims':sorted((c._wire(cl) for cl in admission.claims),key=c.canonical_bytes)}))
                elif pin.path=='synthetic/trust.json':
                    target.write_text(next(e.provenance.excerpt for e in s.entities if e.id.value=='TEST-TRUST'))
                else:target.write_bytes((ROOT/pin.path).read_bytes())
            for stage in (m.ExternalStage.EVIDENCE_RECEIVED,m.ExternalStage.EVIDENCE_VALIDATED,m.ExternalStage.DEPENDENT_ACTION_REENTRY):
                event=external_event(b.current,stage,entity.id if stage is m.ExternalStage.EVIDENCE_RECEIVED else None)
                b=c.record_result(b,event)
                path,identity=c.save_bundle(b,root/'out',root);restored=c.restore(path,identity,root)
                self.assertEqual(c.bundle_bytes(restored),c.bundle_bytes(b))
                self.assertEqual(core.recompute(restored.current),core.recompute(b.current))
                self.assertEqual(c.snapshot_bytes(b.current),c.snapshot_bytes(c.decode_snapshot(c.snapshot_bytes(b.current))))
            with self.assertRaises(m.PlannerError):core.apply_receipt(b.current,event)
            (root/'synthetic/trust.json').write_text('changed trust bytes')
            with self.assertRaises(m.PlannerError):c.restore(path,identity,root)

    def test_receipt_trust_is_not_self_hash_or_shared_digest_type(self):
        s,entity=synthetic_receipt(self.waiting());trust=next(e for e in s.entities if e.id.value=='TEST-TRUST')
        for invalid in (replace(trust,provenance=entity.provenance),replace(trust,consumed=True)):
            bad=replace(s,entities=tuple(invalid if e.id==trust.id else e for e in s.entities))
            self.assertNotEqual(gates.check_receipt(bad,bad.external_gates[0],entity.id).state,m.ProofState.PROVED)
        wrong_domain=replace(trust,identity=replace(trust.identity,kind=m.IdentityKind.CONTENT_IDENTITY))
        bad=replace(s,entities=tuple(wrong_domain if e.id==trust.id else e for e in s.entities))
        with self.assertRaisesRegex(m.PlannerError,'wrong authority identity domain'):
            gates.check_receipt(bad,bad.external_gates[0],entity.id)
        bad=replace(s,receipt_admissions=())
        self.assertNotEqual(gates.check_receipt(bad,bad.external_gates[0],entity.id).state,m.ProofState.PROVED)
        bad=replace(s,receipt_observations=(m.ReceiptObservation(s.external_gates[0].id,entity.id,True,(),()),))
        with self.assertRaises(m.PlannerError):c.snapshot_bytes(bad)

    def test_negative_receipt_canonical_reload_preserves_failed_proposition(self):
        s=self.waiting();claims=tuple(m.EvidenceClaim(r.id,m.ProofState.DISPROVED if i==0 else m.ProofState.PROVED) for i,r in enumerate(s.evidence_requirements))
        s,entity=synthetic_receipt(s,claims);s=self.receive(s,entity)
        restored=c.decode_snapshot(c.snapshot_bytes(s))
        self.assertEqual(core.recompute(s),core.recompute(restored))
        self.assertEqual(gates.obligation_proof(restored,claims[0].requirement).state,m.ProofState.DISPROVED)
        self.assertFalse(gates.external_complete(restored,restored.external_gates[0]))

    def test_stale_attestor_propagates_to_independent_root_predicates(self):
        s,entity=synthetic_receipt(self.waiting());s=self.receive(s,entity)
        root=s.roots[0];predicate=s.predicates[0]
        synthetic=replace(s,roots=(replace(root,predicate=predicate.id),))
        evaluated=core.evaluate_satisfaction(synthetic)
        self.assertEqual(evaluated.roots[0].state,m.ConditionState.SATISFIED)
        trust=next(e for e in s.entities if e.id.value=='TEST-TRUST')
        stale=c.invalidate_sources(evaluated,(trust.provenance.identity,))
        self.assertEqual(stale.roots[0].state,m.ConditionState.STALE)
        self.assertFalse(gates.external_complete(stale,stale.external_gates[0]))


if __name__ == '__main__':
    unittest.main()


class P06IntegrationTests(unittest.TestCase):
    def test_a_actual_candidate_consumer_rejects_before_review(self):
        # GIVEN actual Candidate 2 and the later pinned reconciliation (explicit
        # counterfactual earlier gate); WHEN the pure identity adapter runs;
        # THEN schema rejection blocks review; MUST NOT issue or construct.
        from unittest.mock import patch
        from adapter import invocation_constructor as consumer
        with patch.object(consumer, 'construct_work_authorization', side_effect=AssertionError('effect forbidden')):
            b, events, _ = replay.import_fixture(FIXTURES/'A_P06.json', ROOT)
        self.assertEqual(events, ())
        self.assertEqual(b.current.knowledge[0].statement, 'unknown WorkAuthorization schema')
        self.assertEqual(core.recompute(b.current).actionable, ())
        self.assertTrue(all(r.state is m.ConditionState.UNRESOLVED for r in b.current.roots))
        # Plausibility is not an accepted consumer-proof record.
        for phrase in ('semantically plausible', 'Architect likes it'):
            knowledge=replace(b.current.knowledge[0],id=m.KnowledgeId('unreviewed-opinion'),statement=phrase)
            self.assertEqual(core.recompute(replace(b.current,knowledge=(knowledge,))).actionable,())

    def test_b_valid_construction_authority_does_not_supply_template(self):
        # GIVEN actual candidate-only grant and independently absent Template1
        # source/producer/mapping; WHEN checking construction; THEN blocked;
        # MUST NOT manufacture input or consume the grant.
        b, _, _ = replay.import_fixture(FIXTURES/'B_P06.json',ROOT)
        s=b.current;a=s.actions[0]
        self.assertEqual(gates.evaluate_predicate(s,a.authority).state,m.ProofState.PROVED)
        self.assertEqual(core.recompute(s).actionable,())
        self.assertFalse(s.entities[0].consumed)
        for ref in a.requirements:
            self.assertEqual(gates.evaluate_predicate(s,ref).state,m.ProofState.UNKNOWN)
        self.assertNotIn(m.AuthorityClass.ISSUE,s.entities[0].permissions)
        self.assertNotIn(m.AuthorityClass.USE,s.entities[0].permissions)
        with self.assertRaises(m.PlannerError):
            core.apply_result(s,m.SuppliedResult(a.id,m.ActionResult.PASS,(),c.snapshot_id(s)))

    def test_full_import_retains_all_records_and_never_uses_report_oracles(self):
        b=replay.import_e1(ROOT/'docs/experiments/E1/E1_RESUME_MANIFEST_1.json',ROOT)
        graph=json.loads((ROOT/'docs/experiments/E1/E1_TEMPLATE1_TYPED_KNOWLEDGE_GRAPH_1.json').read_text())
        retained=[a for a in b.current.assertions if a.provenance.method=='P06_PINNED_OPAQUE_RECORD']
        for section in ('entities','assertions'):
            rows=[a for a in retained if a.provenance.path.endswith('TYPED_KNOWLEDGE_GRAPH_1.json') and a.provenance.section.startswith('/'+section+'/')]
            self.assertEqual(len(rows),len(graph[section]))
            self.assertEqual([json.loads(a.provenance.excerpt) for a in rows],graph[section])
            self.assertTrue(all(a.relation is None for a in rows))
        output=replay.plan_output(b)
        self.assertEqual(output['control'],'MIXED_WAIT');self.assertEqual(output['actionable'],[])
        self.assertEqual(sum(v!='SATISFIED' for v in output['roots'].values()),27)
        self.assertEqual(sum(v!='RESOLVED' for v in output['slots'].values()),41)
        self.assertFalse(output['resume_allowed'])

    def test_n_full_import_isolated_receipts_and_cold_reentry(self):
        import subprocess,sys
        b=replay.import_e1(ROOT/'docs/experiments/E1/E1_RESUME_MANIFEST_1.json',ROOT)
        baseline=b.current
        variants=('unrelated','stale','malformed','partial','negative','complete')
        for variant in variants:
            claims=None
            if variant=='partial':claims=(m.EvidenceClaim(baseline.evidence_requirements[0].id,m.ProofState.PROVED),)
            if variant=='negative':claims=tuple(m.EvidenceClaim(r.id,m.ProofState.DISPROVED) for r in baseline.evidence_requirements)
            if variant=='unrelated':claims=(m.EvidenceClaim(m.EvidenceId('not-requested'),m.ProofState.PROVED),)
            s,entity=synthetic_receipt(baseline,claims)
            if variant in ('stale','malformed'):
                entity=replace(entity,valid_until=0) if variant=='stale' else replace(entity,identity=replace(entity.identity,sha256='0'*64))
                s=replace(s,entities=tuple(entity if e.id==entity.id else e for e in s.entities))
            before=s
            if variant=='unrelated':
                with self.assertRaises(m.PlannerError):c.snapshot_bytes(s)
                continue
            for stage in (m.ExternalStage.EVIDENCE_RECEIVED,m.ExternalStage.EVIDENCE_VALIDATED):
                s=core.apply_receipt(s,external_event(s,stage,entity.id if stage is m.ExternalStage.EVIDENCE_RECEIVED else None)).snapshot
            self.assertEqual(s.roots,before.roots);self.assertEqual(s.slots,before.slots)
            if variant!='complete':
                self.assertEqual(core.recompute(s).actionable,())
                with self.assertRaises(m.PlannerError):core.apply_receipt(s,external_event(s,m.ExternalStage.DEPENDENT_ACTION_REENTRY))
                continue
            # Persist the complete isolated receipt/reentry sequence; a new Python
            # process must restore exactly the same next action without memory.
            pins={(p.path,p.pointer,p.profile):p for p in b.sources}
            for p in replay.provenance_records(before):
                pin=m.ArtifactPin(p.path,p.identity);pins[(pin.path,pin.pointer,pin.profile)]=pin
            isolated=replace(b,initial=before,current=before,sources=tuple(pins.values()))
            for stage in (m.ExternalStage.EVIDENCE_RECEIVED,m.ExternalStage.EVIDENCE_VALIDATED,m.ExternalStage.DEPENDENT_ACTION_REENTRY):
                isolated=c.record_result(isolated,external_event(isolated.current,stage,entity.id if stage is m.ExternalStage.EVIDENCE_RECEIVED else None))
            output=replay.plan_output(isolated)
            self.assertEqual(output['actionable'],['FACT-BUDGET-APPLICABILITY'])
            self.assertEqual(output['next_action'],'FACT-BUDGET-APPLICABILITY')
            self.assertEqual(isolated.current.roots,baseline.roots);self.assertEqual(isolated.current.slots,baseline.slots)
            with tempfile.TemporaryDirectory() as directory:
                root=Path(directory)
                for pin in isolated.sources+(isolated.policy,):
                    if pin.pointer:continue
                    target=root/pin.path;target.parent.mkdir(parents=True,exist_ok=True)
                    if pin.path=='synthetic/receipt.json':
                        ad=before.receipt_admissions[0]
                        target.write_bytes(c.canonical_bytes({'producer':c._wire(ad.producer),'target':c._wire(ad.target),'claims':sorted((c._wire(cl) for cl in ad.claims),key=c.canonical_bytes)}))
                    elif pin.path=='synthetic/trust.json':target.write_text(next(e.provenance.excerpt for e in before.entities if e.id.value=='TEST-TRUST'))
                    else:target.write_bytes((ROOT/pin.path).read_bytes())
                path,identity=c.save_bundle(isolated,root/'out',root)
                script='from adapter.planner import codec as c,model as m,replay; import sys; b=c.restore(sys.argv[1],m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY,"planner-bundle-v1",sys.argv[2]),sys.argv[3]);sys.stdout.buffer.write(c.canonical_bytes(replay.plan_output(b)))'
                run=subprocess.run([sys.executable,'-B','-c',script,str(path),identity.sha256,str(root)],cwd=str(ROOT),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                self.assertEqual(run.returncode,0,run.stderr.decode())
                self.assertEqual(run.stdout,c.canonical_bytes(output))
                (root/'synthetic/trust.json').write_text('stale authentication source')
                with self.assertRaises(m.PlannerError):c.restore(path,identity,root)
