"""P01 only: partial E1 replay and the applicable bounded negative checks."""
from copy import deepcopy
from dataclasses import FrozenInstanceError, replace
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from adapter.planner import recompute, apply_result, select
from adapter.planner.model import (
    ActionId, ActionState, ActionStatus, ArtifactIdentity, ConditionId,
    ConditionState, EffectClass, Gate, GateKind, IdentityKind, KnowledgeState,
    PlannerError, SuppliedResult, ActionResult, SlotState,
)
from adapter.planner.replay import load_fixture, run_replay, parse_json, decode_result

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / 'adapter/tests/fixtures/planner_v0_1/E_P01.json'


class P01Tests(unittest.TestCase):
    def setUp(self):
        self.fixture = load_fixture(FIXTURE, ROOT)
        self.snapshot = self.fixture.snapshot

    def load_data(self, data, root=ROOT):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'fixture.json'
            path.write_text(json.dumps(data), encoding='utf-8')
            return load_fixture(path, root)

    def test_vertical_slice_knowledge_not_condition_satisfaction(self):
        initial = recompute(self.snapshot)
        self.assertEqual(initial.actionable, (ActionId('S-BINDING'), ActionId('S-CONTEXT')))
        self.assertEqual(initial.selection.selected, ActionId('S-BINDING'))
        self.assertEqual(initial.selection.criterion, 5)
        report = run_replay(self.fixture)
        self.assertEqual(len(report.snapshot.knowledge), 2)
        self.assertEqual({k.state for k in report.snapshot.knowledge},
                         {KnowledgeState.KNOWN_COMPLETE, KnowledgeState.KNOWN_INCOMPLETE})
        self.assertEqual(report.snapshot.roots, self.snapshot.roots)
        self.assertEqual(report.snapshot.slots, self.snapshot.slots)
        self.assertEqual(report.action_transitions, tuple(ActionStatus(ActionId('S-BINDING'), s)
            for s in (ActionState.ACTIONABLE, ActionState.SELECTED, ActionState.COMPLETED)))
        self.assertEqual(report.computation.actionable, (ActionId('S-CONTEXT'),))
        self.assertEqual(report.computation.selection.selected, ActionId('S-CONTEXT'))
        self.assertEqual(report.computation.selection.criterion, 0)  # Only two real actions in slice.
        self.assertEqual(report.computation.blocked, ((ActionId('TEST-AFTER-INVENTORY'),
                            ('CONDITION_SATISFIED:root:binding',)),))
        # The original snapshot and next action remain untouched/unexecuted.
        self.assertEqual(self.snapshot.knowledge, ())
        self.assertNotIn(ActionStatus(ActionId('S-CONTEXT'), ActionState.COMPLETED),
                         report.snapshot.statuses)

    def test_prerequisites_not_structural_membership(self):
        before = dict(recompute(self.snapshot).blocked)[ActionId('TEST-AFTER-INVENTORY')]
        self.assertEqual(before, ('ACTION_COMPLETED:S-BINDING',
                                  'CONDITION_SATISFIED:root:binding'))
        # Positive control on a synthetic starting state, not domain propagation.
        satisfied = replace(self.snapshot, roots=tuple(replace(r, state=ConditionState.SATISFIED)
                                                       for r in self.snapshot.roots))
        after = apply_result(satisfied, self.fixture.supplied_result)
        self.assertIn(ActionId('TEST-AFTER-INVENTORY'), after.computation.actionable)

    def test_reversal_and_repeated_replay(self):
        reverse = replace(self.snapshot, actions=tuple(reversed(self.snapshot.actions)),
                          statuses=tuple(reversed(self.snapshot.statuses)))
        self.assertEqual(recompute(reverse), recompute(self.snapshot))
        expected = apply_result(self.snapshot, self.fixture.supplied_result)
        for _ in range(10):
            report = apply_result(reverse, self.fixture.supplied_result)
            self.assertEqual(report.computation, expected.computation)
            self.assertEqual(report.snapshot.knowledge, expected.snapshot.knowledge)
            self.assertEqual(report.snapshot.roots, expected.snapshot.roots)

    def test_json_order_and_round_trip_are_not_planner_inputs(self):
        data = json.loads(FIXTURE.read_text())
        def reverse_keys(value):
            if isinstance(value, dict):
                return {k: reverse_keys(v) for k, v in reversed(list(value.items()))}
            if isinstance(value, list):
                return [reverse_keys(v) for v in value]
            return value
        canonical = json.dumps(data, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
        self.assertEqual(canonical, json.dumps(parse_json(canonical), sort_keys=True,
                                             separators=(',', ':'), ensure_ascii=False))
        loaded = self.load_data(reverse_keys(data))
        self.assertEqual(loaded, self.fixture)
        self.assertEqual(run_replay(loaded), run_replay(self.fixture))

    def test_selector_fallback_and_empty_boundary(self):
        actions = self.snapshot.actions[:2]
        trace = select(actions)
        self.assertEqual(trace.steps, ('CRITERION_1_NOT_DECISIVE', 'CRITERION_2_NOT_DECISIVE',
            'CRITERION_3_TIED', 'CRITERION_4_TIED_NO_COST', 'CRITERION_5_ACTION_ID'))
        with self.assertRaises(PlannerError):
            select(())
        held = replace(self.snapshot, statuses=tuple(ActionStatus(a.id, ActionState.WAITING)
                                                    for a in self.snapshot.actions))
        self.assertEqual(recompute(held).actionable, ())
        self.assertIsNone(recompute(held).selection)

    def test_effect_priority_never_grants_actionability(self):
        actions = list(self.snapshot.actions)
        actions[0] = replace(actions[0], effect=EffectClass.PRODUCTION_EFFECT)
        self.assertEqual(select(actions[:2]).criterion, 4)
        self.assertEqual(select(actions[:2]).selected, ActionId('S-CONTEXT'))
        state = replace(self.snapshot, actions=tuple(actions))
        self.assertNotIn(ActionId('S-BINDING'), recompute(state).actionable)
        with self.assertRaises(PlannerError):
            apply_result(state, self.fixture.supplied_result)

    def test_invalid_pass_missing_or_changed_knowledge(self):
        event = self.fixture.supplied_result
        changes = [(), event.knowledge[:1], event.knowledge + event.knowledge[:1],
                   (replace(event.knowledge[0], statement='binding producer exists'), event.knowledge[1]),
                   (replace(event.knowledge[0], provenance=event.knowledge[1].provenance), event.knowledge[1])]
        for records in changes:
            with self.subTest(records=records), self.assertRaises(PlannerError):
                apply_result(self.snapshot, replace(event, knowledge=records))
        self.assertEqual(self.snapshot.knowledge, ())
        self.assertTrue(all(r.state is ConditionState.UNRESOLVED for r in self.snapshot.roots))
        self.assertTrue(all(s.state is SlotState.UNRESOLVED for s in self.snapshot.slots))

    def test_direct_root_or_slot_setters_rejected(self):
        value = json.loads(FIXTURE.read_text())['result']
        for key in ('root_state', 'slot_state', 'root_conditions_resolved', 'slots_resolved'):
            with self.subTest(key=key), self.assertRaises(PlannerError):
                decode_result({**value, key: 'SATISFIED'}, self.snapshot)
        with self.assertRaises(TypeError):
            SuppliedResult(ActionId('S-BINDING'), ActionResult.PASS, (), root_state='SATISFIED')

    def test_unselected_or_completed_action_cannot_be_applied(self):
        with self.assertRaises(PlannerError):
            apply_result(self.snapshot, replace(self.fixture.supplied_result, action=ActionId('S-CONTEXT')))
        report = run_replay(self.fixture)
        with self.assertRaises(PlannerError):
            apply_result(report.snapshot, self.fixture.supplied_result)
        # S-CONTEXT has no P01 accepted result contract: selection is not execution.
        with self.assertRaises(PlannerError):
            apply_result(report.snapshot, SuppliedResult(ActionId('S-CONTEXT'), ActionResult.PASS, ()))

    def test_held_action_not_retried(self):
        for state in (ActionState.BLOCKED, ActionState.WAITING, ActionState.COMPLETED):
            snapshot = replace(self.snapshot, statuses=tuple(
                replace(s, state=state) if s.id == ActionId('S-BINDING') else s
                for s in self.snapshot.statuses))
            self.assertNotIn(ActionId('S-BINDING'), recompute(snapshot).actionable)

    def test_unsupported_result_states_fail_closed(self):
        for result in ActionResult:
            if result is not ActionResult.PASS:
                with self.subTest(result=result), self.assertRaises(PlannerError):
                    apply_result(self.snapshot, replace(self.fixture.supplied_result, result=result))

    def test_unknown_schema_state_operation_and_fields(self):
        original = json.loads(FIXTURE.read_text())
        for key, bad in [('state', 'READYISH'), ('operation', 'GOVERNED_OPERATION'),
                         ('effect', 'UNKNOWN'), ('state', True)]:
            data = deepcopy(original)
            data['actions'][0][key] = bad
            with self.subTest(key=key, bad=bad), self.assertRaises(PlannerError):
                self.load_data(data)
        for key in ('schema', 'scope'):
            data = deepcopy(original)
            data[key] = 'unknown'
            with self.assertRaises(PlannerError):
                self.load_data(data)
        with self.assertRaises(PlannerError):
            self.load_data({**original, 'root_override': 'SATISFIED'})
        with self.assertRaises(PlannerError):
            parse_json('{"state":1,"state":2}')
        with self.assertRaises(PlannerError):
            parse_json('{"state":NaN}')

    def test_duplicate_or_dangling_references_rejected(self):
        with self.assertRaises(PlannerError):
            recompute(replace(self.snapshot, actions=self.snapshot.actions + self.snapshot.actions[:1]))
        with self.assertRaises(PlannerError):
            select(self.snapshot.actions[:1] * 2)
        action = replace(self.snapshot.actions[0], prerequisites=(
            Gate(GateKind.ACTION_COMPLETED, ActionId('ABSENT')),))
        with self.assertRaises(PlannerError):
            recompute(replace(self.snapshot, actions=(action,) + self.snapshot.actions[1:]))

    def test_types_and_immutability(self):
        digest = 'a' * 64
        content = ArtifactIdentity(IdentityKind.CONTENT_IDENTITY, 'profile-content', digest)
        authority = ArtifactIdentity(IdentityKind.AUTHORITY_IDENTITY, 'profile-authority', digest)
        self.assertNotEqual(content, authority)
        with self.assertRaises(PlannerError):
            ArtifactIdentity('CONTENT_IDENTITY', 'profile-content', digest)
        self.assertNotEqual(ActionId('same'), ConditionId('same'))
        with self.assertRaises(FrozenInstanceError):
            self.snapshot.knowledge = ()
        for actions in (list(self.snapshot.actions), (replace(self.snapshot.actions[0],
                           operation='SOURCE_ACQUISITION'),) + self.snapshot.actions[1:]):
            with self.assertRaises(PlannerError):
                recompute(replace(self.snapshot, actions=actions))
        source = replace(self.snapshot.actions[0].source, identity=authority)
        with self.assertRaises(PlannerError):
            recompute(replace(self.snapshot, actions=(replace(self.snapshot.actions[0], source=source),)
                              + self.snapshot.actions[1:]))

    def test_pinned_source_and_location_cannot_be_replaced(self):
        original = json.loads(FIXTURE.read_text())
        for key, bad in [('sha256', '0' * 64), ('section', 'Absent'), ('excerpt', 'invented proof'),
                         ('path', '../escape'), ('path', '/tmp/source')]:
            data = deepcopy(original)
            data['sources']['binding'][key] = bad
            with self.subTest(key=key), self.assertRaises(PlannerError):
                self.load_data(data)

    def test_import_does_not_load_effecting_adapter(self):
        code = "import sys; import adapter.planner; assert 'adapter.governed_host' not in sys.modules; assert 'adapter.workauth_lifecycle' not in sys.modules"
        result = subprocess.run([sys.executable, '-B', '-c', code], cwd=ROOT,
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)




class P03CoreTests(unittest.TestCase):
    def load_case(self, case):
        from adapter.planner.replay import load_p03_fixture
        return load_p03_fixture(ROOT / ('adapter/tests/fixtures/planner_v0_1/' + case + '_P03.json'), ROOT)

    def test_c_dispatcher_corrected_before_runtime_probe(self):
        # GIVEN three unresolved recorded prerequisites; WHEN projecting/recomputing;
        # THEN none actionable; MUST NOT reproduce the historical frontier mistake.
        from adapter.planner.core import project
        snapshot, expected = self.load_case('C')
        projection = project(snapshot)
        self.assertEqual(projection.defects, ())
        self.assertEqual(len(projection.edges), 3)
        self.assertEqual(recompute(snapshot).actionable, ())
        reasons = dict(recompute(snapshot).blocked)[ActionId('DISPATCHER_ELIGIBILITY')]
        self.assertEqual(set(reasons), {'CONDITION_SATISFIED:' + r for r in expected['blocked_roots']})
        # Every proper subset still blocks; only all prerequisites can qualify.
        from itertools import combinations
        for size in range(4):
            for ids in combinations([r.id for r in snapshot.roots], size):
                changed = replace(snapshot, roots=tuple(replace(r, state=ConditionState.SATISFIED)
                    if r.id in ids else r for r in snapshot.roots))
                self.assertEqual(bool(recompute(changed).actionable), size == 3)

    def test_d_49_orders_100_replays_and_json_keys(self):
        # GIVEN E1's 15-action tie; WHEN permuted/replayed; THEN S-ANCESTRY/5;
        # MUST NOT rank by file order, time, conversation or invented metric.
        import hashlib
        from adapter.planner.codec import snapshot_bytes, decode_snapshot
        snapshot, expected = self.load_case('D')
        actions = tuple(sorted(snapshot.actions, key=lambda a: a.id.value))
        orders = [actions, tuple(reversed(actions))]
        orders += [actions[n:] + actions[:n] for n in range(15)]
        orders += [tuple(sorted(actions, key=lambda a: hashlib.sha256(
            (str(seed) + ':' + a.id.value).encode()).digest())) for seed in range(32)]
        self.assertEqual(len(orders), 49)
        baseline = recompute(snapshot)
        self.assertEqual(baseline.selection.selected.value, expected['selected'])
        self.assertEqual(baseline.selection.criterion, 5)
        for order in orders:
            state = replace(snapshot, actions=order, statuses=tuple(reversed(snapshot.statuses)))
            self.assertEqual(recompute(state), baseline)
            self.assertEqual(snapshot_bytes(state), snapshot_bytes(snapshot))
        for _ in range(100):
            self.assertEqual(recompute(snapshot), baseline)
        def flip(obj):
            if isinstance(obj, dict):
                return {k: flip(v) for k, v in reversed(list(obj.items()))}
            if isinstance(obj, list):
                return [flip(v) for v in obj]
            return obj
        restored = decode_snapshot(json.dumps(flip(json.loads(snapshot_bytes(snapshot)))))
        self.assertEqual(recompute(restored), baseline)

    def test_selector_complete_partial_metrics_and_static_mapping(self):
        from adapter.planner import model as m
        from adapter.planner.selector import priority_class
        from itertools import permutations
        snapshot, _ = self.load_case('D')
        template = next(a for a in snapshot.actions if a.id.value == 'S-BINDING')
        actions = tuple(replace(template, id=ActionId('TEST-' + c)) for c in 'ABC')
        for order in permutations(actions):
            self.assertEqual(select(order).selected, ActionId('TEST-A'))
        coverage = {a.id: (0, 0, 0) for a in actions}
        coverage[actions[2].id] = (1, 1, 0)
        self.assertEqual(select(actions, coverage).selected, actions[2].id)
        self.assertEqual(select(actions, coverage).criterion, 1)
        self.assertEqual(select(actions, {actions[2].id: (99, 99, 99)}).criterion, 5)
        incomplete = dict(coverage); incomplete[actions[0].id] = (True, 0, 0)
        self.assertEqual(select(actions, incomplete).criterion, 5)
        info = {a.id: m.InformationModel(a.id, ('x', 'y'), (('x', 'y'),), a.source) for a in actions}
        info[actions[1].id] = replace(info[actions[1].id], partitions=(('x',), ('y',)))
        self.assertEqual(select(actions, information=info).selected, actions[1].id)
        self.assertEqual(select(actions, information=info).criterion, 2)
        malformed = dict(info); malformed[actions[0].id] = replace(info[actions[0].id], partitions=(('x',),))
        self.assertEqual(select(actions, information=malformed).criterion, 5)
        cost = tuple(replace(a, cost=1 if a.id == actions[2].id else 2, cost_unit='declared-unit') for a in actions)
        self.assertEqual(select(cost).selected, actions[2].id)
        self.assertEqual(select(cost).criterion, 4)
        self.assertEqual(select((replace(cost[0], cost=None),) + cost[1:]).criterion, 5)
        expected = {m.OperationClass.FACT_ACQUISITION: m.OperationClass.SOURCE_ACQUISITION,
            m.OperationClass.DECISION_INPUT_ACQUISITION: m.OperationClass.ARCHITECT_PREPARATION,
            m.OperationClass.IMPLEMENTATION_REPAIR: m.OperationClass.GOVERNED_OPERATION,
            m.OperationClass.VALIDATOR_IMPLEMENTATION: m.OperationClass.GOVERNED_OPERATION,
            m.OperationClass.ARCHITECT_AUTHORITY: m.OperationClass.GOVERNED_OPERATION}
        for operation, priority in expected.items():
            self.assertEqual(priority_class(replace(template, operation=operation)), priority)
        self.assertEqual(priority_class(replace(template, operation=m.OperationClass.SEMANTIC_RESOLUTION,
            stage=m.ActionStage.DECISION_PREPARATION)), m.OperationClass.ARCHITECT_PREPARATION)
        other = replace(actions[0], operation=m.OperationClass.OTHER)
        self.assertIn('CRITERION_3_NOT_DECISIVE', select((other,) + actions[1:]).steps)

    def test_p03_fixture_source_pins_fail_closed(self):
        from adapter.planner.replay import load_p03_fixture
        data = json.loads((ROOT / 'adapter/tests/fixtures/planner_v0_1/C_P03.json').read_text())
        data['sources'][0]['sha256'] = '0' * 64
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory, 'case.json'); path.write_text(json.dumps(data))
            with self.assertRaises(PlannerError):
                load_p03_fixture(path, ROOT)


if __name__ == '__main__':
    unittest.main()


def c04_computation_bytes(value):
    """Test-only complete output encoding; preserve every type and tuple order."""
    from dataclasses import fields,is_dataclass
    from enum import Enum
    from adapter.planner import codec as c
    def encode(item):
        if isinstance(item,Enum):return {'type':type(item).__name__,'value':item.value}
        if is_dataclass(item):return {'type':type(item).__name__, 'fields':{f.name:encode(getattr(item,f.name)) for f in fields(item)}}
        if isinstance(item,tuple):return [encode(v) for v in item]
        return item
    return c.canonical_bytes(encode(value))


class C04TypedControlTests(unittest.TestCase):
    def state(self, root_state=ConditionState.SATISFIED, slot_state=SlotState.RESOLVED):
        from adapter.planner import model as m
        base=load_fixture(FIXTURE,ROOT).snapshot
        source=base.actions[0].source
        return replace(base, actions=(),statuses=(),roots=(m.RootCondition(m.ConditionId('same'),root_state),),
            slots=(m.ValueSlot(m.SlotId('same'),slot_state,m.IdentityKind.CONTENT_IDENTITY),),
            goals=(m.Goal(m.ConditionId('same'),(),source),m.Goal(m.SlotId('same'),(),source)))

    def test_t05_equal_canonical_state_requires_equal_complete_computation(self):
        from adapter.planner import codec as c
        state=self.state(); reverse=replace(state,goals=tuple(reversed(state.goals)))
        self.assertEqual(c.snapshot_bytes(state),c.snapshot_bytes(reverse))
        self.assertEqual(recompute(state),recompute(reverse))

    def test_distinct_states_all_goal_orders_and_canonical_reload(self):
        from adapter.planner import model as m,codec as c
        from itertools import permutations
        for root_state in (ConditionState.SATISFIED,ConditionState.UNRESOLVED):
            for slot_state in (SlotState.RESOLVED,SlotState.UNRESOLVED):
                state=self.state(root_state,slot_state)
                expected=recompute(state)
                for goals in permutations(state.goals):
                    candidate=replace(state,goals=goals)
                    raw=c.snapshot_bytes(candidate)
                    self.assertEqual(raw,c.snapshot_bytes(state))
                    self.assertEqual(recompute(candidate),expected)
                    self.assertEqual(recompute(c.decode_snapshot(raw)),expected)
                    self.assertEqual(c04_computation_bytes(recompute(candidate)),c04_computation_bytes(expected))
                branches=dict(expected.branches)
                self.assertEqual(branches[m.ConditionId('same')] is m.BranchState.TERMINAL_SUCCESS,root_state is ConditionState.SATISFIED)
                self.assertEqual(branches[m.SlotId('same')] is m.BranchState.TERMINAL_SUCCESS,slot_state is SlotState.RESOLVED)

    def witnessed_state(self):
        from adapter.planner import model as m
        state=self.state(ConditionState.UNRESOLVED,SlotState.UNRESOLVED)
        source=state.goals[0].provenance
        actions=tuple(m.Action(m.ActionId(name),m.OperationClass.SOURCE_ACQUISITION,m.EffectClass.NON_EFFECTING,(),source,())
            for name in ('same','other'))
        return replace(state,actions=actions,statuses=tuple(m.ActionStatus(a.id,m.ActionState.WAITING) for a in actions),
            goals=tuple(replace(g,entry_actions=tuple(a.id for a in actions)) for g in state.goals),
            boundaries=(m.ControlBoundary(m.GateId('same'),m.BoundaryKind.EXTERNAL_FACT,tuple(a.id for a in actions),source),))

    def test_witnesses_preserve_domains_and_paths_under_all_orders(self):
        from adapter.planner import codec as c
        from itertools import permutations
        state=self.witnessed_state();expected=recompute(state)
        witnesses=expected.frontier[0][1]
        self.assertEqual(len(witnesses),4)
        self.assertEqual({goal for goal,path in witnesses},{('ConditionId','same'),('SlotId','same')})
        self.assertEqual({path for goal,path in witnesses},{(('ActionId','same'),),(('ActionId','other'),)})
        for goals in permutations(state.goals):
            for actions in permutations(state.actions):
                candidate=replace(state,actions=actions,statuses=tuple(reversed(state.statuses)),
                    goals=tuple(replace(g,entry_actions=tuple(reversed(g.entry_actions))) for g in goals),
                    boundaries=tuple(replace(b,actions=tuple(reversed(b.actions))) for b in state.boundaries))
                self.assertEqual(c.snapshot_bytes(state),c.snapshot_bytes(candidate))
                self.assertEqual(expected,recompute(candidate))
                self.assertEqual(expected,recompute(c.decode_snapshot(c.snapshot_bytes(candidate))))

    def test_process_hash_seeds_and_reversed_object_keys(self):
        import os
        from adapter.planner import codec as c
        state=self.witnessed_state()
        def reverse(value):
            if isinstance(value,dict):return {k:reverse(v) for k,v in reversed(tuple(value.items()))}
            if isinstance(value,list):return [reverse(v) for v in value]
            return value
        raw=c.snapshot_bytes(state)
        script='from adapter.planner import codec as c,core;from adapter.tests.test_planner_core import c04_computation_bytes;import sys;s=c.decode_snapshot(sys.stdin.buffer.read());sys.stdout.buffer.write(c04_computation_bytes(core.recompute(s)))'
        expected=c04_computation_bytes(recompute(state))
        for seed in ('1','7','42','123','999'):
            for data in (raw,json.dumps(reverse(json.loads(raw))).encode()):
                actual=subprocess.check_output([sys.executable,'-B','-c',script],input=data,env=dict(os.environ,PYTHONHASHSEED=seed))
                self.assertEqual(actual,expected)

    def test_set_valued_predicate_and_reference_orders(self):
        from adapter.planner import model as m,codec as c
        state=self.witnessed_state()
        a=m.Predicate(m.PredicateId('a'),m.PredicateKind.SOURCE_IDENTITY,unavailable='source A missing')
        b=m.Predicate(m.PredicateId('b'),m.PredicateKind.SOURCE_IDENTITY,unavailable='source B missing')
        both=m.Predicate(m.PredicateId('both'),m.PredicateKind.ALL,operands=(a.id,b.id))
        state=replace(state,predicates=(a,b,both),roots=tuple(replace(r,predicate=both.id) for r in state.roots))
        reverse=replace(state,predicates=(replace(both,operands=(b.id,a.id)),b,a),goals=tuple(reversed(state.goals)))
        self.assertEqual(c.snapshot_bytes(state),c.snapshot_bytes(reverse))
        self.assertEqual(recompute(state),recompute(reverse))
        self.assertEqual(recompute(state),recompute(c.decode_snapshot(c.snapshot_bytes(reverse))))
