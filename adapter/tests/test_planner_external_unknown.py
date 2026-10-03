"""Source-bound control admission never supplies positive proof or resume permission."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from dataclasses import replace, fields, is_dataclass
from adapter.planner import core, gates, codec, model as m
from adapter.tests import test_planner_e1_replay as replay_tests
from adapter.tests.test_planner_e1_replay import synthetic_receipt, external_event, fixture

ROOT = Path(__file__).resolve().parents[2]
VALIDATION = ROOT / 'docs/plans/DETERMINISTIC_PLANNER_V0_1_EXTERNAL_UNKNOWN_RULE_RECONCILIATION_1_VALIDATION.json'


def source(path, body):
    raw = codec.canonical_bytes(body)
    Path(path).write_bytes(raw)
    identity = m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY, 'raw-file-sha256', hashlib.sha256(raw).hexdigest())
    return m.Provenance(Path(path).name, identity, '/', raw.decode(), 'QUALIFICATION_ONLY', 'TEST/scope')


def attach(state, directory):
    """Encode the independent acquisition premise, not a new positive proof.

    Existing unbound gates remain ungoverned. The versioned typed binding supplies
    the reconciliation's exact correspondence that the old gate type lacked.
    """
    gate = state.external_gates[0]
    requirement = state.evidence_requirements[0]
    context = m.EvaluationContext('TEST/scope', 'TEST/lineage', 'TEST/generation', 0)
    record = m.ExternalResolutionContract('TEST-REQUEST', gate.id, requirement.id,
        requirement.proposition, requirement.target, requirement.producers,
        'TEST-rule-owner governing-rule source', requirement.provenance.identity,
        gate.provenance.identity, gate.receipt_action, gate.reentry, gate.held_actions,
        context.scope, context.lineage, context.generation, gate.provenance)
    body = codec._wire(record)
    del body['$type']; del body['provenance']
    record = replace(record, provenance=source(Path(directory)/'resolution.json',
        {'schema':'EXTERNAL-RESOLUTION-CONTRACT-1', 'contract':body}))
    return replace(state, context=context, external_gates=(replace(gate, resolution_contracts=(record,)),))


class ExternalUnknownTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        # Exact original counterexample, no mocks or replacement of core/gates.
        program = json.loads(VALIDATION.read_text())['probe_program'].split('results=[]')[0]
        # Isolate the source locator; its semantic contents are unchanged.
        program = program.replace('/tmp/unknown-rule-source.json', self.temp.name+'/source.json')
        ns = {}; exec(program, ns)
        original = ns['s']
        provenance = replace(original.actions[0].source, path='source.json')
        self.original = replace(original,
            actions=tuple(replace(a,source=provenance) for a in original.actions),
            evidence_requirements=tuple(replace(r,provenance=provenance) for r in original.evidence_requirements),
            external_gates=tuple(replace(g,provenance=provenance) for g in original.external_gates),
            boundaries=tuple(replace(b,provenance=provenance) for b in original.boundaries),
            goals=tuple(replace(g,provenance=provenance) for g in original.goals))
        self.state = attach(self.original, self.temp.name)

    def bundle(self, state):
        # Supported policy from prior fixture, source pins independently supplied.
        from adapter.tests.test_planner_resume import fixture_bundle
        _, base = fixture_bundle()
        policy_path = Path(self.temp.name)/base.policy.path
        policy_path.parent.mkdir(parents=True,exist_ok=True)
        policy_path.write_bytes((ROOT/base.policy.path).read_bytes())
        provenances = [a.source for a in state.actions] + codec.external_provenances(state)
        pins = tuple({(p.path,p.identity):m.ArtifactPin(p.path,p.identity) for p in provenances}.values())
        return m.PersistenceBundle(state, (), state, pins, base.policy, 'E1-SELECTION-1-P05')

    def test_governed_external_unknown(self):
        s=self.state; comp=core.recompute(s)
        self.assertEqual(comp.control,m.ControlState.EXTERNAL_WAIT)
        self.assertEqual(comp.defects,());self.assertEqual(comp.actionable,())
        self.assertFalse(s.evidence_requirements[0].rule_known)
        self.assertEqual(gates.obligation_proof(s,s.evidence_requirements[0].id).state,m.ProofState.UNKNOWN)
        self.assertEqual(s.roots,self.original.roots);self.assertEqual(s.slots,self.original.slots)
        self.assertFalse(core.resume_eligibility(self.bundle(s),self.temp.name).allowed)
        self.assertEqual((s.knowledge,s.receipt_admissions,s.receipt_observations),((),(),()))

    def test_unbound_missing_and_incomplete_routes(self):
        self.assertEqual(core.recompute(self.original).control,m.ControlState.PLAN_DEFECT)
        for s in [replace(self.state,external_gates=(),boundaries=()),
                  replace(self.state,external_gates=(replace(self.state.external_gates[0],contract_complete=False),))]:
            self.assertEqual(core.recompute(s).control,m.ControlState.PLAN_DEFECT)

    def test_every_bound_dimension_rejects_substitution(self):
        s=self.state; g=s.external_gates[0]; c=g.resolution_contracts[0]
        mutations=dict(request='',gate=m.GateId('OTHER'),requirement=m.EvidenceId('OTHER'),
            proposition='other',target=replace(c.target,namespace='OTHER'),producers=(),
            source_class='',requirement_source=replace(c.requirement_source,sha256='d'*64),
            gate_source=replace(c.gate_source,sha256='d'*64),receipt_action='OTHER',
            reentry=(),held_actions=(),scope='OTHER',lineage='OTHER',generation='OTHER')
        for key,value in mutations.items():
            with self.subTest(key=key):
                bad=replace(c,**{key:value})
                state=replace(s,external_gates=(replace(g,resolution_contracts=(bad,)),))
                self.assertEqual(core.recompute(state).control,m.ControlState.PLAN_DEFECT)
        # Correctly hashed but wrong lineage must fail correspondence, not checksum.
        bad=replace(c,lineage='OTHER');body=codec._wire(bad);del body['$type'];del body['provenance']
        bad=replace(bad,provenance=source(Path(self.temp.name)/'wrong-lineage.json',
            {'schema':'EXTERNAL-RESOLUTION-CONTRACT-1','contract':body}))
        self.assertEqual(core.recompute(replace(s,external_gates=(replace(g,resolution_contracts=(bad,)),))).control,m.ControlState.PLAN_DEFECT)
        # Typed source pins are mandatory for bundle admission and actual restore.
        with self.assertRaises(m.PlannerError):codec.bundle_bytes(replace(self.bundle(s),sources=()))
        (Path(self.temp.name)/c.provenance.path).write_text('substituted bytes')
        with self.assertRaises(m.PlannerError):codec.load_pinned(self.temp.name,m.ArtifactPin(c.provenance.path,c.provenance.identity))

    def test_branch_correspondence_and_invalidation(self):
        s=codec.decode_snapshot(codec.snapshot_bytes(self.state))
        detached=replace(s,actions=(replace(s.actions[0],requirements=()),))
        self.assertEqual(core.recompute(detached).control,m.ControlState.PLAN_DEFECT)
        for identity in [s.external_gates[0].resolution_contracts[0].provenance.identity,
                         s.external_gates[0].provenance.identity,
                         s.evidence_requirements[0].provenance.identity]:
            invalid=codec.invalidate_sources(s,(identity,))
            self.assertEqual(core.recompute(invalid).control,m.ControlState.PLAN_DEFECT)
            self.assertEqual(core.recompute(codec.decode_snapshot(codec.snapshot_bytes(invalid))).control,m.ControlState.PLAN_DEFECT)
            self.assertFalse(core.resume_eligibility(self.bundle(invalid),self.temp.name).allowed)

    def test_mixed_runnable_human_and_internal_acquisition(self):
        s=self.state; a=m.ActionId('INDEPENDENT');r=m.ConditionId('INDEPENDENT-ROOT')
        independent=replace(s.actions[0],id=a,requirements=())
        live=replace(s,actions=s.actions+(independent,),statuses=s.statuses+(m.ActionStatus(a,m.ActionState.ACTION_ELIGIBLE),))
        self.assertEqual(core.recompute(live).control,m.ControlState.RUNNABLE)
        self.assertEqual(core.recompute(live).defects,())
        mixed=replace(live,roots=s.roots+(m.RootCondition(r,m.ConditionState.UNRESOLVED),),
            boundaries=s.boundaries+(m.ControlBoundary(m.GateId('FACT'),m.BoundaryKind.EXTERNAL_FACT,(a,),s.actions[0].source),),
            goals=s.goals+(m.Goal(r,(a,),s.actions[0].source),))
        self.assertEqual(core.recompute(mixed).control,m.ControlState.MIXED_WAIT)
        human,_=fixture('I')
        h=replace(s,actions=s.actions+human.actions,statuses=s.statuses+human.statuses,
            roots=s.roots+human.roots,slots=human.slots,knowledge=human.knowledge,
            entities=human.entities,assertions=human.assertions,predicates=s.predicates+human.predicates,
            decisions=human.decisions)
        self.assertEqual(core.recompute(h).control,m.ControlState.HUMAN_HANDOFF)
        both=replace(h,actions=h.actions+(independent,),statuses=h.statuses+(m.ActionStatus(a,m.ActionState.ACTION_ELIGIBLE),))
        self.assertEqual(core.recompute(both).control,m.ControlState.RUNNABLE)
        internal=replace(live,external_gates=(),boundaries=(),actions=(replace(s.actions[0],prerequisites=(m.Gate(m.GateKind.ACTION_COMPLETED,a),)),independent))
        self.assertEqual(core.recompute(internal).control,m.ControlState.RUNNABLE)
        self.assertNotIn(s.actions[0].id,core.recompute(internal).actionable)

    def test_receipt_and_positive_reentry_unchanged(self):
        s=self.state
        with self.assertRaises(m.PlannerError):core.apply_receipt(s,external_event(s,m.ExternalStage.EVIDENCE_VALIDATED))
        # Exercise existing independent trust/receipt fixtures, including unknown rule.
        base=replay_tests.P05ReplayTests().waiting();received,entity=synthetic_receipt(base)
        unknown=replace(received,evidence_requirements=tuple(replace(r,rule_known=False) for r in received.evidence_requirements))
        self.assertNotEqual(gates.check_receipt(unknown,unknown.external_gates[0],entity.id).state,m.ProofState.PROVED)
        invalid=replace(received,receipt_admissions=())
        rejected=replay_tests.P05ReplayTests().receive(invalid,entity)
        self.assertEqual(rejected.external_gates[0].stage,m.ExternalStage.WAITING_FOR_EXTERNAL_EVIDENCE)
        valid=replay_tests.P05ReplayTests().receive(received,entity)
        self.assertEqual(valid.external_gates[0].stage,m.ExternalStage.EVIDENCE_VALIDATED)
        after=core.apply_receipt(valid,external_event(valid,m.ExternalStage.DEPENDENT_ACTION_REENTRY)).snapshot
        self.assertTrue(core.recompute(after).actionable)

    def test_control_matrix_independent_branch_cross_product(self):
        s=self.state;gate=s.external_gates[0]
        base=replay_tests.P05ReplayTests().waiting()
        supplied,entity=synthetic_receipt(base)
        invalid=replay_tests.P05ReplayTests().receive(replace(supplied,receipt_admissions=()),entity)
        valid=replay_tests.P05ReplayTests().receive(supplied,entity)
        states=[('known_missing',replace(s,evidence_requirements=(replace(s.evidence_requirements[0],rule_known=True),)),m.ControlState.EXTERNAL_WAIT),
            ('unknown_governed',s,m.ControlState.EXTERNAL_WAIT),
            ('unknown_missing_route',replace(s,external_gates=(),boundaries=()),m.ControlState.PLAN_DEFECT),
            ('unknown_malformed_route',replace(s,external_gates=(replace(gate,contract_complete=False),)),m.ControlState.PLAN_DEFECT),
            ('received_invalid',invalid,m.ControlState.EXTERNAL_WAIT),
            ('validated_before_reentry',valid,m.ControlState.EXTERNAL_WAIT)]
        human_state,_=fixture('I')
        def rename(value):
            if isinstance(value,m.Identifier):return type(value)('INDEPENDENT-HUMAN-'+value.value)
            if isinstance(value,tuple):return tuple(rename(x) for x in value)
            if is_dataclass(value):return replace(value,**{f.name:rename(getattr(value,f.name)) for f in fields(value)})
            return value
        human_state=rename(human_state)
        for label,state,otherwise in states:
            for machine,human in ((False,False),(True,False),(False,True),(True,True)):
                with self.subTest(case=label,machine=machine,human=human):
                    candidate=state
                    if human:
                        candidate=replace(candidate,**{field:getattr(candidate,field)+getattr(human_state,field)
                            for field in ('actions','statuses','roots','slots','knowledge','entities','assertions','predicates','decisions')})
                    if machine:
                        action=replace(s.actions[0],id=m.ActionId('INDEPENDENT-MATRIX'),requirements=())
                        candidate=replace(candidate,actions=candidate.actions+(action,),statuses=candidate.statuses+(m.ActionStatus(action.id,m.ActionState.ACTION_ELIGIBLE),))
                    expected=m.ControlState.RUNNABLE if machine else m.ControlState.HUMAN_HANDOFF if human else otherwise
                    self.assertEqual(core.recompute(candidate).control,expected)

    def test_two_gate_branch_and_contract_ordering(self):
        s=self.state;g=s.external_gates[0];c=g.resolution_contracts[0]
        a=m.ActionId('SECOND');root=m.ConditionId('SECOND-ROOT')
        req=replace(s.evidence_requirements[0],id=m.EvidenceId('SECOND-PROOF'))
        pred=replace(s.predicates[0],id=m.PredicateId('SECOND-PREDICATE'),obligation=req.id)
        other=replace(g,id=m.GateId('SECOND-GATE'),requirements=(req.id,),reentry=(a,),held_actions=(a,))
        contract=replace(c,request='SECOND-REQUEST',gate=other.id,requirement=req.id,reentry=(a,),held_actions=(a,))
        body=codec._wire(contract);del body['$type'];del body['provenance']
        contract=replace(contract,provenance=source(Path(self.temp.name)/'second-resolution.json',
            {'schema':'EXTERNAL-RESOLUTION-CONTRACT-1','contract':body}))
        other=replace(other,resolution_contracts=(contract,))
        state=replace(s,actions=s.actions+(replace(s.actions[0],id=a,requirements=(pred.id,)),),
            statuses=s.statuses+(m.ActionStatus(a,m.ActionState.ACTION_ELIGIBLE),),
            roots=s.roots+(m.RootCondition(root,m.ConditionState.UNRESOLVED),),
            predicates=s.predicates+(pred,),evidence_requirements=s.evidence_requirements+(req,),
            external_gates=s.external_gates+(other,),
            boundaries=s.boundaries+(m.ControlBoundary(other.id,m.BoundaryKind.EXTERNAL_EVIDENCE,(a,),g.provenance),),
            goals=s.goals+(m.Goal(root,(a,),g.provenance),))
        reverse=replace(state,**{field:tuple(reversed(getattr(state,field))) for field in
            ('actions','statuses','roots','predicates','evidence_requirements','external_gates','boundaries','goals')})
        self.assertEqual(core.recompute(state).control,m.ControlState.EXTERNAL_WAIT)
        self.assertEqual(len(core.recompute(state).frontier),2)
        self.assertEqual(core.recompute(state),core.recompute(reverse))
        self.assertEqual(codec.snapshot_bytes(state),codec.snapshot_bytes(reverse))
        for candidate in (state, reverse, self.original):
            path=Path(self.temp.name)/'ordered.json';path.write_bytes(codec.snapshot_bytes(candidate))
            code="from adapter.planner import codec,core; import sys; s=codec.decode_snapshot(open(sys.argv[1],'rb').read()); print(codec.snapshot_id(s).sha256, core.recompute(s).control.value)"
            answers=[subprocess.check_output([sys.executable,'-c',code,str(path)],cwd=ROOT,
                env=dict(os.environ,PYTHONHASHSEED=seed,PYTHONDONTWRITEBYTECODE='1'),text=True)
                for seed in ('1','7','101')]
            self.assertEqual(len(set(answers)),1)
            self.assertIn(core.recompute(candidate).control.value,answers[0])

    def test_cold_reload_hash_seeds_orderings_and_repeated_control(self):
        s=self.state;raw=codec.snapshot_bytes(s)
        permuted=replace(s,actions=tuple(reversed(s.actions)),external_gates=tuple(reversed(s.external_gates)),boundaries=tuple(reversed(s.boundaries)))
        self.assertEqual(codec.snapshot_bytes(permuted),raw)
        path=Path(self.temp.name)/'state.json';path.write_bytes(raw)
        code='''import json,sys
from adapter.planner import codec,core
s=codec.decode_snapshot(open(sys.argv[1],'rb').read()); c=core.recompute(s)
print(json.dumps([codec.snapshot_id(s).sha256,c.control.value,list(c.defects),[a.value for a in c.actionable]]))'''
        outputs=[]
        for seed in ['1','7','101']:
            env=dict(os.environ,PYTHONHASHSEED=seed,PYTHONDONTWRITEBYTECODE='1')
            outputs.append(subprocess.check_output([sys.executable,'-c',code,str(path)],cwd=ROOT,env=env,text=True))
        self.assertEqual(len(set(outputs)),1);self.assertIn('EXTERNAL_WAIT',outputs[0])
        def reverse_keys(v):
            if isinstance(v,dict):return {k:reverse_keys(v[k]) for k in reversed(list(v))}
            if isinstance(v,list):return [reverse_keys(x) for x in v]
            return v
        self.assertEqual(codec.snapshot_bytes(codec.decode_snapshot(json.dumps(reverse_keys(json.loads(raw))).encode())),raw)
        for _ in range(10):self.assertEqual(core.recompute(s),core.recompute(codec.decode_snapshot(raw)))
        # Full native bundle source pin/replay verification, separate from snapshot-only checks.
        path,identity=codec.save_bundle(self.bundle(s),Path(self.temp.name)/'bundle',self.temp.name)
        restored=codec.restore(path,identity,self.temp.name)
        self.assertEqual(core.recompute(restored.current).control,m.ControlState.EXTERNAL_WAIT)
        self.assertFalse(core.resume_eligibility(restored,self.temp.name).allowed)
