"""Permanent refined C06 regression and source-bound outcome controls."""
from dataclasses import replace
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from adapter.planner import codec as c, core, model as m, replay
from adapter.tests.counterexamples import c06_f03_candidate as candidate


class C06AcceptedKnowledgeTests(candidate.F03OperationalCounterexample):
    def bound_record(self, state=None):
        return next(k for k in (state or self.ready).knowledge if k.provenance.identity == self.identity)

    def test_blocked_producer_and_wrong_missing_binding_variants(self):
        known = self.bound_record()
        self.assertEqual(known.outcome, m.ActionResult.BLOCKED)
        self.assertEqual(next(s.state for s in self.ready.statuses if s.id == known.producer), m.ActionState.BLOCKED)
        for bad in (replace(known, state=m.KnowledgeState.KNOWN_INCOMPLETE),
                    replace(known, producer=None, outcome=None),
                    replace(known, outcome=m.ActionResult.PASS),
                    replace(known, producer=self.action),
                    replace(known, provenance=replace(known.provenance,
                        identity=replace(known.provenance.identity, sha256='e'*64)))):
            state=replace(self.ready, knowledge=tuple(bad if k.id==known.id else k for k in self.ready.knowledge))
            self.assertNotIn(self.action, core.recompute(c.decode_snapshot(c.snapshot_bytes(state))).actionable)
        for bad in (replace(known, provenance=None),
                    replace(known, outcome='BLOCKED'),
                    replace(known, provenance=replace(known.provenance,
                        identity=replace(known.provenance.identity,kind=m.IdentityKind.AUTHORITY_IDENTITY)))):
            with self.assertRaises(m.PlannerError):
                c.snapshot_bytes(replace(self.ready,knowledge=tuple(bad if k.id==known.id else k for k in self.ready.knowledge)))

    def test_stale_roundtrip_never_revalidates_from_bytes_or_phase(self):
        stale=c.invalidate_sources(self.ready,(self.identity,))
        known=self.bound_record(stale)
        self.assertEqual(known.validation,m.ValidationState.STALE)
        original=core.recompute(stale)
        raw=c.snapshot_bytes(stale)
        permuted=replace(stale,actions=tuple(reversed(stale.actions)),
            knowledge=tuple(reversed(stale.knowledge)),predicates=tuple(reversed(stale.predicates)))
        self.assertEqual(c.snapshot_bytes(permuted),raw)
        self.assertEqual(core.recompute(permuted),original)
        for _ in range(3):
            stale=c.decode_snapshot(raw)
            self.assertEqual(core.recompute(stale),original)
            self.assertNotIn(self.action,original.actionable)
            self.assertEqual(c.snapshot_bytes(stale),raw)
        # A new authenticated import is a distinct historical replay baseline,
        # not an in-place requalification event or authorization to retry E1.
        self.assertEqual(self.bound_record(self.bundle.current).validation,m.ValidationState.ACCEPTED)
        self.assertNotIn(self.action,core.recompute(self.bundle.current).actionable)
        self.assertIn(self.action,core.recompute(self.ready).actionable)
        # Replacing a knowledge qualification flag alone is not an authorized retry.
        flags_only=replace(stale,knowledge=tuple(replace(k,validation=m.ValidationState.ACCEPTED)
            if k.id==known.id else k for k in stale.knowledge))
        self.assertNotIn(self.action,core.recompute(flags_only).actionable)
        self.assertEqual(stale.roots,self.ready.roots)
        self.assertEqual(stale.slots,self.ready.slots)

    def test_contract_admission_and_alpha_renamed_supported_instance(self):
        plan=json.loads((candidate.ROOT/'docs/experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_PLAN_1.json').read_text())
        base=replace(self.bundle.current,
            knowledge=tuple(k for k in self.bundle.current.knowledge if k.producer is None),
            predicates=tuple(p for p in self.bundle.current.predicates if p.required_outcome is None),
            actions=tuple(replace(a,requirements=tuple(p for p in a.requirements if not p.value.startswith('accepted-outcome:')))
                          for a in self.bundle.current.actions))
        for change in ('missing_pin','wrong_outcome','wrong_producer'):
            altered=json.loads(json.dumps(plan)); pins=self.bundle.sources
            req=next(a for a in altered['resolution_actions'] if a['id']==self.action.value)['knowledge_requirements'][0]
            if change=='missing_pin':pins=tuple(p for p in pins if p.identity!=self.identity)
            elif change=='wrong_outcome':req['required_recorded_outcome']='PASS'
            else:req['action']='S-ANCESTRY'
            with self.assertRaises(m.PlannerError):replay.restore_accepted_knowledge(base,altered,pins,candidate.ROOT)
        # Generic rule is driven by source fields, not the E1 action's spelling.
        import hashlib
        producer=replace(base.actions[0],id=m.ActionId('RENAMED-PRODUCER'),prerequisites=(),requirements=(),
            operation=m.OperationClass.SOURCE_ACQUISITION,effect=m.EffectClass.NON_EFFECTING)
        consumer=replace(producer,id=m.ActionId('RENAMED-CONSUMER'))
        state=replace(base,actions=(producer,consumer),statuses=(m.ActionStatus(producer.id,m.ActionState.BLOCKED),
            m.ActionStatus(consumer.id,m.ActionState.ACTION_ELIGIBLE)),roots=(),slots=(),knowledge=(),assertions=(),
            predicates=(),entities=(),decisions=(),external_gates=(),evidence_requirements=(),receipt_admissions=(),
            receipt_observations=(),goals=(),boundaries=(),information=())
        raw=b'```text\nACTION = RENAMED-PRODUCER\nACTION_RESULT = AUTHORITY_REQUIRED\n```\n'
        identity=m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY,'raw-file-sha256',hashlib.sha256(raw).hexdigest())
        pin=m.ArtifactPin('result.md',identity)
        spec={'resolution_actions':[{'id':producer.id.value,'execution_result':{'result':'AUTHORITY_REQUIRED','result_artifact':pin.path}},
            {'id':consumer.id.value,'knowledge_requirements':[{'action':producer.id.value,'required_recorded_outcome':'AUTHORITY_REQUIRED',
             'evidence':{'path':pin.path,'sha256':identity.sha256,'location':'report'},'requirement':'accepted outcome only'}]}]}
        with tempfile.TemporaryDirectory() as directory:
            Path(directory,'result.md').write_bytes(raw)
            restored=replay.restore_accepted_knowledge(state,spec,(pin,),directory)
            Path(directory,'result.md').write_bytes(raw+b'changed')
            with self.assertRaises(m.PlannerError):
                replay.restore_accepted_knowledge(state,spec,(pin,),directory)
        self.assertIn(consumer.id,core.recompute(restored).actionable)
        self.assertNotIn(consumer.id,core.recompute(c.invalidate_sources(restored,(identity,))).actionable)

    def test_hash_seed_and_reversed_key_cold_recomputation(self):
        stale=c.invalidate_sources(self.ready,(self.identity,))
        raw=c.snapshot_bytes(stale)
        def reverse(x):
            if isinstance(x,dict):return {k:reverse(x[k]) for k in reversed(list(x))}
            if isinstance(x,list):return [reverse(v) for v in x]
            return x
        script='''import sys,json
from adapter.planner import codec as c,core
s=c.decode_snapshot(open(sys.argv[1],'rb').read());r=core.recompute(s)
print(json.dumps({'identity':c.snapshot_id(s).sha256,'actionable':[a.value for a in r.actionable],'selected':r.selection.selected.value if r.selection else None,'control':r.control.value},sort_keys=True))
'''
        outputs=[]
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory,'state.json')
            for seed in ('0','19','311'):
                for data in (raw,json.dumps(reverse(json.loads(raw))).encode()):
                    path.write_bytes(data)
                    run=subprocess.run([sys.executable,'-B','-c',script,str(path)],env=dict(os.environ,PYTHONHASHSEED=seed),
                        cwd=str(candidate.ROOT),capture_output=True,text=True)
                    self.assertEqual(run.returncode,0,run.stderr)
                    outputs.append(run.stdout)
        self.assertEqual(len(set(outputs)),1)
        self.assertNotIn(self.action.value,json.loads(outputs[0])['actionable'])
