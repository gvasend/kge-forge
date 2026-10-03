"""P02 case-N persistence prerequisites, not full E1 cold resume/reentry."""
from dataclasses import replace
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from adapter.planner import recompute
from adapter.planner import codec
from adapter.planner.model import (ArtifactIdentity, IdentityKind, HashProfile, ArtifactPin,
                                  PersistenceBundle, PlannerError)
from adapter.planner.replay import load_fixture, load_source_manifest

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / 'adapter/tests/fixtures/planner_v0_1'


def fixture_bundle():
    fixture = load_fixture(FIXTURES / 'E_P01.json', ROOT)
    pins = load_source_manifest(FIXTURES / 'sources.json', ROOT)
    policy = next(p for p in pins if p.path.endswith('E1_GRAPH_RESOLUTION_SELECTION_POLICY_1.md'))
    return fixture, PersistenceBundle(fixture.snapshot, (), fixture.snapshot, pins, policy)


def local_pin(path, data, profile=HashProfile.RAW, pointer=''):
    return ArtifactPin(path, ArtifactIdentity(IdentityKind.CONTENT_IDENTITY, profile.value,
                                              hashlib.sha256(data).hexdigest()), profile, pointer)


class P02PersistenceTests(unittest.TestCase):
    def test_n_subset_snapshot_roundtrip_and_permutation(self):
        # GIVEN P01 state; WHEN normalized/parsed; THEN same state identity/selection;
        # MUST NOT depend on unordered input order or resolve any domain condition.
        fixture, bundle = fixture_bundle()
        initial = bundle.initial
        permuted = replace(initial, actions=tuple(reversed(initial.actions)),
                           statuses=tuple(reversed(initial.statuses)), slots=tuple(reversed(initial.slots)))
        raw = codec.snapshot_bytes(initial)
        self.assertEqual(raw, codec.snapshot_bytes(permuted))
        self.assertEqual(raw, codec.snapshot_bytes(codec.decode_snapshot(raw)))
        self.assertEqual(recompute(initial), recompute(codec.decode_snapshot(raw)))
        for _ in range(10):
            self.assertEqual(raw, codec.snapshot_bytes(initial))

    def test_n_subset_bundle_roundtrip_ledger_and_p01_result(self):
        # GIVEN source-pinned P01; WHEN one event is persisted/restored; THEN identical
        # next action/knowledge/roots/slots; MUST NOT apply another action or resume E1.
        fixture, initial = fixture_bundle()
        bundle = codec.record_result(initial, fixture.supplied_result)
        self.assertEqual(bundle.current.roots, initial.current.roots)
        self.assertEqual(bundle.current.slots, initial.current.slots)
        self.assertEqual(len(bundle.events), 1)
        with tempfile.TemporaryDirectory() as directory:
            path, identity = codec.save_bundle(bundle, directory, ROOT)
            restored = codec.restore(path, identity, ROOT)
            self.assertEqual(codec.bundle_bytes(restored), codec.bundle_bytes(bundle))
            self.assertEqual(recompute(restored.current).selection.selected.value, 'S-CONTEXT')
            before = {p.name: p.read_bytes() for p in Path(directory).iterdir()}
            self.assertEqual(codec.save_bundle(bundle, directory, ROOT), (path, identity))
            self.assertEqual(before, {p.name: p.read_bytes() for p in Path(directory).iterdir()})
            self.assertEqual(codec.append_event(bundle, bundle.events[0]), bundle)
            event = bundle.events[0]
            reordered = replace(event, result=replace(event.result,
                                  knowledge=tuple(reversed(event.result.knowledge))))
            self.assertEqual(codec.append_event(bundle, reordered), bundle)

    def test_e1_manifest_raw_and_embedded_pins(self):
        # GIVEN frozen manifest; WHEN reading its pins only; THEN all verify;
        # MUST NOT restore operational state, follow external sources or alter E1.
        _, bundle = fixture_bundle()
        manifest = next(p for p in bundle.sources if p.path.endswith('E1_RESUME_MANIFEST_1.json'))
        pins = codec.read_e1_manifest(ROOT, manifest)
        pointers = {p.pointer for p in pins if p.profile is HashProfile.E1_EMBEDDED_JSON}
        self.assertEqual(pointers, {'/execution_history', '/execution_state', '/selection_policy'})
        self.assertTrue(any(p.path.endswith('CONSTRUCTION_AUTHORITY_3.json') for p in pins))
        history_pin = next(p for p in pins if p.pointer == '/execution_history')
        self.assertIsInstance(codec.load_pinned(ROOT, history_pin), list)
        self.assertEqual(bundle.events, ())

    def test_hash_domains_and_ordered_arrays(self):
        data = {'z': ['β', 'a'], 'a': True}
        raw = codec.canonical_bytes(data)
        self.assertIn('β'.encode(), raw)
        self.assertNotEqual(raw, codec.canonical_bytes({'z': ['a', 'β'], 'a': True}))
        self.assertNotEqual(codec.canonical_bytes(True), codec.canonical_bytes(1))
        with tempfile.TemporaryDirectory() as directory:
            value = {'outer': data}
            Path(directory, 'x.json').write_text(json.dumps(value, indent=2), encoding='utf-8')
            pin = local_pin('x.json', raw, HashProfile.E1_EMBEDDED_JSON, '/outer')
            self.assertEqual(codec.load_pinned(directory, pin), data)
            with self.assertRaises(PlannerError):
                codec.load_pinned(directory, replace(pin, profile=HashProfile.RAW))
            wrong = replace(pin, identity=replace(pin.identity, kind=IdentityKind.AUTHORITY_IDENTITY))
            with self.assertRaises(PlannerError):
                codec.load_pinned(directory, wrong)

    def test_strict_json_and_unknown_typed_state(self):
        for text in ('{"a":1,"a":2}', '{"a":1.0}', '{"a":NaN}', '{"a":Infinity}'):
            with self.subTest(text=text), self.assertRaises(PlannerError):
                codec.parse_json(text)
        for value in (1.0, float('nan'), {1: 'bad'}, ('not', 'json')):
            with self.assertRaises(PlannerError):
                codec.canonical_bytes(value)
        fixture, _ = fixture_bundle()
        raw = codec.snapshot_bytes(fixture.snapshot)
        for changed in (raw.replace(b'ACTION_ELIGIBLE', b'MADE_UP_STATE'),
                        raw.replace(b'"$type":"ActionId"', b'"$type":"UnknownAction"'),
                        raw.replace(b'"$enum":"OperationClass"', b'"$enum":"UnknownClass"')):
            with self.assertRaises(PlannerError):
                codec.decode_snapshot(changed)

    def test_pointer_escaping_and_rejections(self):
        value = {'a/b': {'~': [False, 1]}}
        self.assertEqual(codec.json_pointer(value, '/a~1b/~0/1'), 1)
        for pointer in ('/missing', '/a~2b', '/a~1b/~0/01', '/a~1b/~0/-', '/a~1b/~0/7'):
            with self.subTest(pointer=pointer), self.assertRaises(PlannerError):
                codec.json_pointer(value, pointer)

    def test_sequence_parent_and_outcome_mismatch(self):
        fixture, initial = fixture_bundle()
        bundle = codec.record_result(initial, fixture.supplied_result)
        event = bundle.events[0]
        bad_events = [replace(event, sequence=2), replace(event, sequence=True),
                      replace(event, parent_event=event.identity),
                      replace(event, parent_snapshot=event.after_snapshot),
                      replace(event, after_snapshot=event.parent_snapshot)]
        for bad in bad_events:
            with self.subTest(bad=bad), self.assertRaises(PlannerError):
                codec.append_event(initial, bad)
        with self.assertRaises(PlannerError):
            codec.bundle_bytes(replace(bundle, current=initial.current))
        with self.assertRaises(PlannerError):
            codec.bundle_bytes(replace(bundle, events=bundle.events * 2))

    def test_ledger_blob_and_bundle_tampering(self):
        fixture, initial = fixture_bundle()
        bundle = codec.record_result(initial, fixture.supplied_result)
        with tempfile.TemporaryDirectory() as directory:
            path, identity = codec.save_bundle(bundle, directory, ROOT)
            original = path.read_bytes()
            path.write_bytes(original + b' ')
            with self.assertRaises(PlannerError):
                codec.restore(path, identity, ROOT)
            path.write_bytes(original)
            event = next(Path(directory).glob('event-*.json'))
            event.write_bytes(b'{}')
            with self.assertRaises(PlannerError):
                codec.restore(path, identity, ROOT)
            with self.assertRaises(PlannerError):
                codec.save_bundle(bundle, directory, ROOT)

    def test_source_change_refuses_old_restore_token(self):
        _, bundle = fixture_bundle()
        with tempfile.TemporaryDirectory() as directory:
            copied = Path(directory, 'repo')
            for pin in bundle.sources:
                target = copied / pin.path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes((ROOT / pin.path).read_bytes())
            path, identity = codec.save_bundle(bundle, Path(directory, 'output'), copied)
            source = copied / bundle.initial.actions[0].source.path
            source.write_bytes(source.read_bytes() + b'changed')
            with self.assertRaises(PlannerError):
                codec.restore(path, identity, copied)

    def test_missing_provenance_and_policy_rejected(self):
        _, bundle = fixture_bundle()
        source_path = bundle.initial.actions[0].source.path
        with self.assertRaises(PlannerError):
            codec.bundle_bytes(replace(bundle, sources=tuple(p for p in bundle.sources if p.path != source_path)))
        with self.assertRaises(PlannerError):
            codec.bundle_bytes(replace(bundle, policy_version='unrecognized'))
        with self.assertRaises(PlannerError):
            codec.bundle_bytes(replace(bundle, policy=replace(bundle.policy,
                identity=replace(bundle.policy.identity, kind=IdentityKind.AUTHORITY_IDENTITY))))

    def test_no_e1_writes_or_symlink_redirect(self):
        _, bundle = fixture_bundle()
        with self.assertRaises(PlannerError):
            codec.save_bundle(bundle, ROOT / 'docs/experiments/E1', ROOT)
        with tempfile.TemporaryDirectory() as directory:
            link = Path(directory, 'redirect')
            link.symlink_to(ROOT / 'docs/experiments/E1', target_is_directory=True)
            with self.assertRaises(PlannerError):
                codec.save_bundle(bundle, link, ROOT)

    def test_repeat_bundle_bytes_and_set_order(self):
        fixture, initial = fixture_bundle()
        expected = codec.record_result(initial, fixture.supplied_result)
        flipped = replace(initial, sources=tuple(reversed(initial.sources)),
            initial=replace(initial.initial, actions=tuple(reversed(initial.initial.actions))),
            current=replace(initial.current, actions=tuple(reversed(initial.current.actions))))
        for _ in range(10):
            actual = codec.record_result(flipped, replace(fixture.supplied_result,
                                             knowledge=tuple(reversed(fixture.supplied_result.knowledge))))
            self.assertEqual(codec.bundle_bytes(actual), codec.bundle_bytes(expected))


if __name__ == '__main__':
    unittest.main()


class P06ColdResumeTests(unittest.TestCase):
    def cli(self,*args,code=0):
        import subprocess,sys
        run=subprocess.run([sys.executable,'-B','-m','adapter.planner']+list(map(str,args)),
                           cwd=str(ROOT),stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False)
        self.assertEqual(run.returncode,code,run.stderr.decode())
        if code==0:
            value=codec.parse_json(run.stdout)
            self.assertEqual(run.stdout,codec.canonical_bytes(value)+b'\n')
        return run

    def test_n_cold_process_manifest_then_native_bundle_identical(self):
        # GIVEN only persisted manifest/pinned sources, no in-process planner state;
        # WHEN separate CLI processes restore to fresh directories; THEN identical
        # canonical bundles and all control/state/provenance; MUST NOT resume E1.
        manifest=ROOT/'docs/experiments/E1/E1_RESUME_MANIFEST_1.json'
        with tempfile.TemporaryDirectory() as directory:
            base=Path(directory)
            first=self.cli('restore',manifest,'--out',base/'first')
            second=self.cli('restore',manifest,'--out',base/'second')
            self.assertEqual(first.stdout,second.stdout)
            a=next((base/'first').glob('bundle-*.json'));b=next((base/'second').glob('bundle-*.json'))
            self.assertEqual(a.read_bytes(),b.read_bytes())
            third=self.cli('restore',a,'--out',base/'native')
            self.assertEqual(first.stdout,third.stdout)
            self.assertEqual(a.read_bytes(),next((base/'native').glob('bundle-*.json')).read_bytes())
            output=codec.parse_json(first.stdout)
            self.assertEqual(output['control'],'MIXED_WAIT');self.assertEqual(output['actionable'],[])
            self.assertIsNone(output['next_action']);self.assertFalse(output['resume_allowed'])
            self.assertEqual(sum(v!='SATISFIED' for v in output['roots'].values()),27)
            self.assertEqual(sum(v!='RESOLVED' for v in output['slots'].values()),41)
            a.write_bytes(a.read_bytes()+b' ')
            self.cli('restore',a,'--out',base/'tampered',code=2)
            self.assertFalse((base/'tampered').exists())

    def test_cli_validate_plan_replay_apply_and_exit_contract(self):
        from adapter.planner import replay,model as m
        fixture=FIXTURES/'B_P06.json'
        for command in ('validate','plan'):
            self.assertEqual(codec.parse_json(self.cli(command,fixture).stdout)['actionable'],[])
        with tempfile.TemporaryDirectory() as directory:
            base=Path(directory)
            self.cli('replay',fixture,'--out',base/'replay')
            data=codec.parse_json(fixture.read_bytes());data['expected']['actionable']=['invented']
            bad=base/'bad.json';bad.write_bytes(codec.canonical_bytes(data))
            self.cli('replay',bad,'--out',base/'bad-output',code=3)
            self.assertFalse((base/'bad-output').exists())
            bad.write_text('{"schema":"unknown"}')
            self.cli('validate',bad,code=2)
            # One supplied bounded P01 event through the new structured fixture/CLI.
            original,bundle=fixture_bundle()
            data=dict(schema='PLANNER-REPLAY-1',case_id='E',mode='HISTORICAL',
                source_manifest=[codec._wire(p) for p in bundle.sources],initial=codec.parse_json(codec.snapshot_bytes(bundle.initial)),
                policy=codec._wire(bundle.policy),events=[],expected={},prohibited=[])
            fp=base/'e.json';fp.write_bytes(codec.canonical_bytes(data))
            event=base/'event.json';event.write_bytes(codec.canonical_bytes(codec._wire(original.supplied_result)))
            output=codec.parse_json(self.cli('apply',fp,'--event',event,'--out',base/'applied').stdout)
            self.assertEqual(output['next_action'],'S-CONTEXT')
            self.assertTrue(all(v=='UNRESOLVED' for v in output['roots'].values()))
            self.cli('restore',next((base/'applied').glob('bundle-*.json')),'--out',base/'again')
            data['events']=[codec._wire(original.supplied_result)]
            data['expected']={'steps':[{'next_action':'S-CONTEXT'}],'final':{'next_action':'S-CONTEXT'}}
            fp.write_bytes(codec.canonical_bytes(data))
            repeated=codec.parse_json(self.cli('replay',fp,'--out',base/'steps').stdout)
            self.assertEqual(output,repeated)
            data['expected']['steps'][0]['next_action']='invented'
            fp.write_bytes(codec.canonical_bytes(data))
            self.cli('replay',fp,'--out',base/'bad-step',code=3)
            self.assertFalse((base/'bad-step').exists())

    def test_n_import_permutation_canonical_identity_and_pins(self):
        from adapter.planner import replay
        b=replay.import_e1(ROOT/'docs/experiments/E1/E1_RESUME_MANIFEST_1.json',ROOT)
        s=b.current
        reverse=replace(s,actions=tuple(reversed(s.actions)),statuses=tuple(reversed(s.statuses)),
            assertions=tuple(reversed(s.assertions)),roots=tuple(reversed(s.roots)),slots=tuple(reversed(s.slots)))
        permuted=replace(b,initial=reverse,current=reverse,sources=tuple(reversed(b.sources)))
        self.assertEqual(codec.bundle_bytes(b),codec.bundle_bytes(permuted))
        self.assertEqual(replay.plan_output(b),replay.plan_output(permuted))
        for _ in range(3):
            raw=codec.snapshot_bytes(s);s=codec.decode_snapshot(raw)
            self.assertEqual(raw,codec.snapshot_bytes(s))
            self.assertEqual(replay.plan_output(b),replay.plan_output(replace(b,initial=s,current=s)))
        self.assertTrue(any(p.pointer=='/execution_history' for p in b.sources))
        self.assertTrue(any(p.path.endswith('CONSTRUCTION_AUTHORITY_3.json') for p in b.sources))
        self.assertTrue(any(p.path.endswith('SELECTION_POLICY_1.md') for p in b.sources))


class C01ReferenceAdmissionTests(unittest.TestCase):
    def test_matching_hash_native_restore_cannot_admit_dangling_predicate(self):
        from adapter.planner import model as m
        _, bundle = fixture_bundle()
        bad = m.Predicate(m.PredicateId('bad'), m.PredicateKind.ACTION_COMPLETED, action=m.ActionId('absent'))
        state = replace(bundle.initial, predicates=(bad,))
        bundle = replace(bundle, initial=state, current=state)
        # Match bytes/hash deliberately: content identity is not contract validity.
        raw = codec.canonical_bytes({'schema':'PLANNER-BUNDLE-1', 'bundle':codec._wire(bundle)})
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'bad.json'; path.write_bytes(raw)
            identity = ArtifactIdentity(IdentityKind.CONTENT_IDENTITY,'planner-bundle-v1',hashlib.sha256(raw).hexdigest())
            with self.assertRaisesRegex(PlannerError,'REFERENCE_CONTRACT'):
                codec.restore(path,identity,ROOT)

    def test_structured_import_rejects_hostile_reference_before_use(self):
        from adapter.planner import model as m, replay
        data = codec.parse_json((FIXTURES/'B_P06.json').read_bytes())
        data['initial']['snapshot']['predicates'].append(codec._wire(m.Predicate(
            m.PredicateId('bad'), m.PredicateKind.SOURCE_IDENTITY,
            entity=m.EntityId('absent'),expected=ArtifactIdentity(IdentityKind.CONTENT_IDENTITY,'test','a'*64))))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'bad.json';path.write_bytes(codec.canonical_bytes(data))
            with self.assertRaisesRegex(PlannerError,'REFERENCE_CONTRACT'):
                replay.import_fixture(path, ROOT)

    def test_c01_hash_seed_invariance_in_fresh_process(self):
        import os, subprocess, sys
        script = '''from adapter.tests.test_planner_invariants import p03_proof_world
from adapter.planner import codec as c, gates as g, model as m
from adapter.planner import recompute
_, b = p03_proof_world()
s=c.decode_snapshot(c.snapshot_bytes(b.current))
print(c.snapshot_id(s).sha256, recompute(s).selection.selected.value)
print(g.evaluate_predicate(s,m.PredicateId('known')).state.value)
'''
        outputs = [subprocess.check_output([sys.executable,'-c',script],cwd=str(ROOT),
                   env=dict(os.environ,PYTHONHASHSEED=seed)) for seed in ('0','1','7','42','999')]
        self.assertTrue(all(o==outputs[0] for o in outputs))


class C03ResumeEligibilityTests(unittest.TestCase):
    def native(self, mutate=None, claims=None):
        from adapter.planner import model as m
        from adapter.tests.test_planner_e1_replay import P05ReplayTests, synthetic_receipt, p05_bundle, external_event
        state,evidence=synthetic_receipt(P05ReplayTests().waiting(),claims)
        if mutate:
            state=mutate(state)
        b=p05_bundle(state)
        for stage in (m.ExternalStage.EVIDENCE_RECEIVED,m.ExternalStage.EVIDENCE_VALIDATED):
            b=codec.record_result(b,external_event(b.current,stage,evidence.id if stage is m.ExternalStage.EVIDENCE_RECEIVED else None))
        if b.current.external_gates[0].stage is m.ExternalStage.EVIDENCE_VALIDATED:
            b=codec.record_result(b,external_event(b.current,m.ExternalStage.DEPENDENT_ACTION_REENTRY))
        return b

    def sources(self,b,root):
        for pin in b.sources+(b.policy,):
            path=root/pin.path;path.parent.mkdir(parents=True,exist_ok=True)
            if pin.path.startswith('synthetic/'):
                entity=next(e for e in b.initial.entities if e.provenance.path==pin.path)
                text=entity.provenance.excerpt
                if text.startswith('COUNTERFACTUAL_SYNTHETIC '):text=text[len('COUNTERFACTUAL_SYNTHETIC '):]
                path.write_text(text)
            else:path.write_bytes((ROOT/pin.path).read_bytes())

    def test_native_proof_positive_stale_attestor_and_cold_cli(self):
        from adapter.planner import model as m,core,replay
        import subprocess,sys
        b=self.native()
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);self.sources(b,root)
            good=core.resume_eligibility(b,root)
            self.assertTrue(good.allowed)
            self.assertEqual([a.value for a in good.actions],['FACT-BUDGET-APPLICABILITY'])
            self.assertTrue(good.supporting_identities)
            self.assertFalse(core.resume_eligibility(b).allowed)
            trust=next(e for e in b.current.entities if e.id.value=='TEST-TRUST')
            stale=codec.record_result(b,m.SourceInvalidation((trust.provenance.identity,),codec.snapshot_id(b.current)))
            proof=core.resume_eligibility(stale,root)
            self.assertFalse(proof.allowed)
            self.assertTrue(any('PRODUCER_AUTHENTICATION_UNPROVED' in r for r in proof.reasons))
            self.assertEqual(stale.current.external_gates[0].history,b.current.external_gates[0].history)
            for candidate in (b,stale):
                path,identity=codec.save_bundle(candidate,root/'out',root)
                expected=replay.plan_output(candidate,root)
                script='from adapter.planner import codec as c,model as m,replay;import sys; b=c.restore(sys.argv[1],m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY,"planner-bundle-v1",sys.argv[2]),sys.argv[3]);sys.stdout.buffer.write(c.canonical_bytes(replay.plan_output(b,sys.argv[3])))'
                import os
                for seed in ('1','7','42'):
                    actual=subprocess.check_output([sys.executable,'-B','-c',script,str(path),identity.sha256,str(root)],env=dict(os.environ,PYTHONHASHSEED=seed))
                    self.assertEqual(codec.parse_json(actual),expected)
                script='from adapter.planner import __main__ as cli;from pathlib import Path;import sys;cli.ROOT=Path(sys.argv[1]);sys.exit(cli.main(["plan",sys.argv[2]]))'
                actual=subprocess.check_output([sys.executable,'-B','-c',script,str(root),str(path)])
                self.assertEqual(codec.parse_json(actual),expected)
            (root/'synthetic/trust.json').write_text('changed')
            self.assertFalse(core.resume_eligibility(b,root).allowed)

    def test_phase_only_policy_changes_and_original_holds(self):
        from adapter.planner import model as m,core
        b=self.native()
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);self.sources(b,root)
            phase=replace(b,initial=b.current,events=())
            self.assertFalse(core.resume_eligibility(phase,root).allowed)
            changed=replace(b,policy=replace(b.policy,identity=replace(b.policy.identity,sha256='c'*64)))
            with self.assertRaisesRegex(PlannerError, 'policy'):
                core.resume_eligibility(changed,root)
            changed=replace(b,policy_version='E1-SELECTION-1-P06')
            self.assertFalse(core.resume_eligibility(changed,root).allowed)
            changed=replace(b,scope='FULL_FROZEN_E1_REPLAY',policy_version='E1-SELECTION-1-P06')
            self.assertFalse(core.resume_eligibility(changed,root).allowed)
            # A recorded reentry does not remove an original unresolved requirement.
            def prerequisite(s):
                parent=m.RootCondition(m.ConditionId('C03:missing'),m.ConditionState.UNRESOLVED)
                actions=tuple(replace(a,prerequisites=a.prerequisites+(m.Gate(m.GateKind.CONDITION_SATISFIED,parent.id),))
                    if a.id in s.external_gates[0].reentry else a for a in s.actions)
                return replace(s,actions=actions,roots=s.roots+(parent,))
            held=self.native(prerequisite);self.sources(held,root)
            self.assertFalse(core.resume_eligibility(held,root).allowed)
            # Historical completed route remains complete, never executable twice.
            def completed(s):
                return replace(s,statuses=tuple(replace(x,state=m.ActionState.COMPLETED)
                    if x.id in s.external_gates[0].reentry else x for x in s.statuses))
            done=self.native(completed);self.sources(done,root)
            self.assertFalse(core.resume_eligibility(done,root).allowed)

    def test_receipt_negative_variants_and_conflicting_proof(self):
        from adapter.planner import model as m,core,gates
        from adapter.tests.test_planner_e1_replay import P05ReplayTests,synthetic_receipt
        refs=P05ReplayTests().waiting().external_gates[0].requirements
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            for claims in ((m.EvidenceClaim(refs[0],m.ProofState.PROVED),),
                    tuple(m.EvidenceClaim(r,m.ProofState.DISPROVED) for r in refs)):
                b=self.native(claims=claims);self.sources(b,root)
                self.assertFalse(core.resume_eligibility(b,root).allowed)
            for mutation in (
                lambda s:replace(s,receipt_admissions=()),
                lambda s:replace(s,context=replace(s.context,tick=21)),
                lambda s:replace(s,evidence_requirements=tuple(replace(r,target=replace(r.target,sha256='c'*64)) for r in s.evidence_requirements))):
                b=self.native(mutation);self.sources(b,root)
                self.assertFalse(core.resume_eligibility(b,root).allowed)
            with self.assertRaises(m.PlannerError):
                self.native(claims=(m.EvidenceClaim(m.EvidenceId('unrelated'),m.ProofState.PROVED),))
            def conflict(s):
                negative,_=synthetic_receipt(P05ReplayTests().waiting(),tuple(m.EvidenceClaim(r,m.ProofState.DISPROVED) for r in refs))
                eid,tid,pid=m.EntityId('C03:negative'),m.EntityId('C03:attestor'),m.PredicateId('C03:authentication')
                entities=tuple(replace(e,id=eid if e.kind is m.EntityKind.EVIDENCE else tid,
                    provenance=replace(e.provenance,path=e.provenance.path.replace('synthetic/','synthetic/negative-')))
                    for e in negative.entities)
                pred=replace(negative.predicates[-1],id=pid,entity=tid)
                admission=replace(negative.receipt_admissions[0],artifact=eid,authentication=pid,
                    provenance=replace(negative.receipt_admissions[0].provenance,path='synthetic/negative-receipt.json'))
                return replace(s,entities=s.entities+entities,predicates=s.predicates+(pred,),receipt_admissions=s.receipt_admissions+(admission,),
                    receipt_observations=(m.ReceiptObservation(s.external_gates[0].id,eid,True,(),admission.claims),))
            b=self.native(conflict);self.sources(b,root)
            self.assertFalse(core.resume_eligibility(b,root).allowed)
            self.assertIn('CONFLICTING_PROOFS',gates.obligation_proof(b.current,refs[0]).reasons)

    def test_shared_gate_blocks_but_independent_wait_does_not(self):
        from adapter.planner import model as m,core
        def other_gate(s,independent):
            original=s.external_gates[0]
            if independent:
                a=replace(s.actions[0],id=m.ActionId('C03:independent'),accepted_inventory=())
                s=replace(s,actions=s.actions+(a,),statuses=s.statuses+(m.ActionStatus(a.id,m.ActionState.WAITING),))
                targets=(a.id,)
            else:targets=original.reentry
            gate=replace(original,id=m.GateId('C03:other'),reentry=targets,held_actions=targets)
            return replace(s,external_gates=s.external_gates+(gate,))
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            for independent in (False,True):
                b=self.native(lambda s:other_gate(s,independent));self.sources(b,root)
                proof=core.resume_eligibility(b,root)
                self.assertEqual(proof.allowed,independent)
                if independent:self.assertEqual([a.value for a in proof.actions],['FACT-BUDGET-APPLICABILITY'])

    def test_missing_event_binding_contract_tampering_and_key_permutation(self):
        from adapter.planner import model as m,core,replay
        b=self.native()
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);self.sources(b,root)
            # Historical old event hashes can replay but cannot authorize resumption.
            events=list(b.events);e=events[-1]
            events[-1]=replace(e,resume_binding=None,identity=codec._event_identity(e.sequence,e.parent_snapshot,e.parent_event,e.result,e.after_snapshot))
            self.assertFalse(core.resume_eligibility(replace(b,events=tuple(events)),root).allowed)
            for change in (replace(b.current,external_gates=tuple(replace(g,contract_complete=False) for g in b.current.external_gates)),
                    replace(b.current,receipt_admissions=()),
                    replace(b.current,context=replace(b.current.context,generation='changed'))):
                with self.assertRaises(m.PlannerError):core.resume_eligibility(replace(b,current=change),root)
            # The replay lineage cannot silently accept changed current contracts.
            data=codec.parse_json(codec.bundle_bytes(b));data['bundle']['resume_allowed']=True
            with self.assertRaises(m.PlannerError):codec._unwire(data['bundle'])
            permuted=replace(b,sources=tuple(reversed(b.sources)))
            self.assertEqual(core.resume_eligibility(b,root),core.resume_eligibility(permuted,root))
            self.assertEqual(replay.plan_output(b,root),replay.plan_output(permuted,root))

    def test_stale_ordering_after_accepted_reentry_remains_persisted_hold(self):
        from adapter.planner import model as m,core
        def ordering(s):
            raw='ordering';identity=m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY,'raw-file-sha256',hashlib.sha256(raw.encode()).hexdigest())
            provenance=replace(s.actions[0].source,path='synthetic/order.json',identity=identity,excerpt=raw)
            parent=m.RootCondition(m.ConditionId('C03:ordered-parent'),m.ConditionState.SATISFIED)
            entity=m.GraphEntity(m.EntityId('C03:ordering-source'),m.EntityKind.PRODUCER,identity,provenance,
                s.context.scope,s.context.lineage,s.context.generation,20)
            actions=tuple(replace(a,prerequisites=a.prerequisites+(m.Gate(m.GateKind.CONDITION_SATISFIED,parent.id),))
                if a.id in s.external_gates[0].reentry else a for a in s.actions)
            edges=tuple(m.GraphAssertion(m.AssertionId('C03:'+a.id.value+':'+g.target.value),
                provenance if g.target==parent.id else a.source,relation=m.Relation.REQUIRES,
                subject=a.id,object=g.target,ordering_justification='mandatory original prerequisite')
                for a in actions for g in a.prerequisites)
            return replace(s,roots=s.roots+(parent,),entities=s.entities+(entity,),actions=actions,assertions=s.assertions+edges)
        b=self.native(ordering)
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);self.sources(b,root)
            self.assertTrue(core.resume_eligibility(b,root).allowed)
            source=next(e for e in b.current.entities if e.id.value=='C03:ordering-source')
            changed=codec.record_result(b,m.SourceInvalidation((source.provenance.identity,),codec.snapshot_id(b.current)))
            self.assertFalse(core.resume_eligibility(changed,root).allowed)
            self.assertEqual(changed.current.external_gates[0].stage,m.ExternalStage.DEPENDENT_ACTION_REENTRY)
            path,identity=codec.save_bundle(changed,root/'out',root)
            self.assertEqual(core.resume_eligibility(changed,root),core.resume_eligibility(codec.restore(path,identity,root),root))

    def test_shared_gate_needs_its_own_accepted_reentry_not_phase_text(self):
        from adapter.planner import model as m,core
        def second(s):
            gate=replace(s.external_gates[0],id=m.GateId('C03:phase-only'),
                stage=m.ExternalStage.DEPENDENT_ACTION_REENTRY,history=tuple(m.ExternalStage))
            return replace(s,external_gates=s.external_gates+(gate,))
        b=self.native(second)
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);self.sources(b,root)
            self.assertTrue(core.recompute(b.current).actionable)
            proof=core.resume_eligibility(b,root)
            self.assertFalse(proof.allowed)
            self.assertTrue(any('C03:phase-only:ACCEPTED_REENTRY_EVENT_MISSING' in r for r in proof.reasons))


class C04ControlPersistenceTests(unittest.TestCase):
    def test_cold_restore_and_cli_preserve_complete_typed_control(self):
        import subprocess,sys
        from adapter.planner import core,replay
        from adapter.tests.test_planner_core import C04TypedControlTests,c04_computation_bytes
        state=C04TypedControlTests().witnessed_state()
        _,base=fixture_bundle()
        bundle=replace(base,initial=state,current=state,policy_version='E1-SELECTION-1-P05')
        variants=(bundle,replace(bundle,sources=tuple(reversed(bundle.sources)),
            initial=replace(state,goals=tuple(reversed(state.goals))),current=replace(state,goals=tuple(reversed(state.goals)))))
        expected=c04_computation_bytes(core.recompute(state));cli_expected=codec.canonical_bytes(replay.plan_output(bundle,ROOT))
        with tempfile.TemporaryDirectory() as directory:
            for index,candidate in enumerate(variants):
                store=Path(directory)/str(index);store.mkdir()
                # Unrelated directory entries in opposite creation orders are not inputs.
                for name in (('z','a') if index else ('a','z')):(store/name).write_text('unrelated')
                path,identity=codec.save_bundle(candidate,store,ROOT)
                restored=codec.restore(path,identity,ROOT)
                self.assertEqual(codec.bundle_bytes(bundle),codec.bundle_bytes(restored))
                self.assertEqual(c04_computation_bytes(core.recompute(restored.current)),expected)
                script='from adapter.planner import codec as c,core,model as m;from adapter.tests.test_planner_core import c04_computation_bytes;import sys;b=c.restore(sys.argv[1],m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY,"planner-bundle-v1",sys.argv[2]),sys.argv[3]);sys.stdout.buffer.write(c04_computation_bytes(core.recompute(b.current)))'
                self.assertEqual(subprocess.check_output([sys.executable,'-B','-c',script,str(path),identity.sha256,str(ROOT)]),expected)
                output=subprocess.check_output([sys.executable,'-B','-m','adapter.planner','plan',str(path)],cwd=str(ROOT))
                self.assertEqual(output.strip(),cli_expected)

class C05PolicyBindingTests(unittest.TestCase):
    def test_construction_authority_cannot_be_selection_policy(self):
        from adapter.planner import replay
        data = json.loads((FIXTURES / 'B_P06.json').read_text())
        data['policy'] = next(p for p in data['source_manifest']
            if 'CONSTRUCTION_AUTHORITY_3.json' in str(p))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'fixture.json'
            path.write_text(json.dumps(data))
            with self.assertRaisesRegex(PlannerError, 'policy'):
                replay.import_fixture(path, ROOT)

    def test_policy_contract_mutations_fail_before_selection_and_restore(self):
        from adapter.planner import selector
        fixture, bundle = fixture_bundle()
        original = (ROOT / selector.POLICY_PIN.path).read_bytes()
        mutations = {
            'class_map': original + b'\nSOURCE_ACQUISITION -> GOVERNED_OPERATION',
            'tie_break': original + b'\nSelect largest ActionId instead.',
            'effect_rule': original + b'\nPrefer PRODUCTION_EFFECT.',
            'extension': original + b'\nUnsupported semantic extension.',
        }
        for label, raw_policy in mutations.items():
            with self.subTest(label=label), tempfile.TemporaryDirectory() as directory:
                pin = replace(bundle.policy, identity=replace(bundle.policy.identity,
                    sha256=hashlib.sha256(raw_policy).hexdigest()))
                # Even honestly rehashed policy bytes cannot qualify a new rule.
                policy_path = Path(directory) / pin.path
                policy_path.parent.mkdir(parents=True)
                policy_path.write_bytes(raw_policy)
                self.assertEqual(codec.load_pinned(directory, pin), raw_policy)
                with self.assertRaisesRegex(PlannerError, 'policy'):
                    selector.select(fixture.snapshot.actions, policy=pin)
                bad = replace(bundle, policy=pin)
                raw = codec.canonical_bytes({'schema': 'PLANNER-BUNDLE-1', 'bundle': codec._wire(bad)})
                path = Path(directory) / 'bundle.json'
                path.write_bytes(raw)
                identity = codec._identity(raw, 'planner-bundle-v1')
                with self.assertRaisesRegex(PlannerError, 'policy'):
                    codec.restore(path, identity, directory)

    def test_version_domain_projection_and_stale_policy(self):
        from adapter.planner import selector
        fixture, bundle = fixture_bundle()
        for pin in (replace(bundle.policy, pointer='/other'),
                    replace(bundle.policy, profile=HashProfile.PLANNER_JSON),
                    replace(bundle.policy, path='other-policy.md'),
                    replace(bundle.policy, identity=replace(bundle.policy.identity,
                        kind=IdentityKind.AUTHORITY_IDENTITY)),
                    replace(bundle.policy, identity=replace(bundle.policy.identity, sha256='0'*64))):
            with self.subTest(pin=pin), self.assertRaisesRegex(PlannerError, 'policy'):
                codec.bundle_bytes(replace(bundle, policy=pin))
        with self.assertRaisesRegex(PlannerError, 'policy'):
            selector.select(fixture.snapshot.actions, policy_version='E1-SELECTION-2')
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / 'repo'
            for pin in bundle.sources + (bundle.policy,):
                path = root / pin.path
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes((ROOT / pin.path).read_bytes())
            path, identity = codec.save_bundle(bundle, Path(directory) / 'out', root)
            (root / bundle.policy.path).write_bytes(b'stale policy')
            with self.assertRaises(PlannerError):
                codec.restore(path, identity, root)

    def test_supported_versions_preserve_binding_and_extension_selection(self):
        from adapter.planner import selector, model as m
        fixture, bundle = fixture_bundle()
        action = fixture.snapshot.actions[0]
        inputs = tuple(replace(action, id=m.ActionId(name),
            operation=m.OperationClass.DECISION_INPUT_ACQUISITION)
            for name in ('INPUT-IMPLEMENTATION', 'INPUT-BUDGET'))
        for binding in selector.SUPPORTED_POLICIES:
            self.assertEqual(selector.validate_policy(bundle.policy, binding.version), binding)
            for actions in (inputs, tuple(reversed(inputs))):
                trace = selector.select(actions, policy=bundle.policy, policy_version=binding.version)
                self.assertEqual((trace.selected.value, trace.criterion), ('INPUT-BUDGET', 5))
            candidate = replace(bundle, policy_version=binding.version)
            raw = codec.bundle_bytes(candidate)
            decoded = codec._unwire(codec.parse_json(raw)['bundle'])
            self.assertEqual(codec.bundle_bytes(decoded), raw)
            self.assertEqual(decoded.policy_version, binding.version)

    def test_implementation_contract_drift_is_not_silently_admitted(self):
        from unittest.mock import patch
        from adapter.planner import selector
        fixture, bundle = fixture_bundle()
        # These replace rule configuration, not validation: exercise real select.
        for name, value in (('CLASS_MAP', ()),
                            ('EFFECT_PRIORITY', tuple(reversed(selector.EFFECT_PRIORITY))),
                            ('RULES', selector.RULES[:-1] + ('tie:largest-id',))):
            with self.subTest(name=name), patch.object(selector, name, value):
                with self.assertRaisesRegex(PlannerError, 'policy'):
                    selector.select(fixture.snapshot.actions)
        for binding in selector.SUPPORTED_POLICIES:
            raw = selector.policy_contract_bytes(binding)
            self.assertEqual(hashlib.sha256(raw).hexdigest(), selector.CONTRACT_DIGESTS[binding.version])
            self.assertEqual(raw, codec.canonical_bytes(json.loads(raw)))
