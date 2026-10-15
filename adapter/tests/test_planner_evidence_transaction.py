"""E07 ordinary transaction qualification; all commits use isolated native fixtures."""
from dataclasses import replace, fields
from unittest.mock import patch
import json, os, subprocess, sys, unittest
from pathlib import Path
from adapter.planner import codec as c, model as m, evidence as ev, core
from adapter.planner import evidence_attestation as ea, evidence_transaction as tx
from adapter.tests.test_planner_authentication_installation import AuthenticationInstallationTests, ROOT


def binding(t):
    return m.SemanticNativeBinding(t.semantic_evidence,t.native_entity,t.content,t.proposition,
        t.source_pin,t.attestor,t.source_predicate,t.gate,t.scope,t.lineage,t.provenance)


class EvidenceTransactionTests(unittest.TestCase):
    def setUp(self):
        self.h=AuthenticationInstallationTests();self.h.setUp()
        _,self.b,_,_=self.h.installed()
        x,t=self.h.candidate(self.b)
        self.expected=binding(t);self.x=tx.bind(x,t,self.expected)
        self.raw={p.path:self.x.entity.provenance.excerpt.encode() for p in self.x.source_additions}
        self.store=self.h.root/'evidence-head'
    def tearDown(self):self.h.doCleanups()
    def preflight(self,x=None,expected=None):
        return c.preflight_external_evidence(self.b,x or self.x,self.raw,self.h.root,
            expected_binding=self.expected if expected is None else expected)
    def commit(self,x=None,store=None):
        return c.admit_external_evidence(self.b,x or self.x,self.raw,store or self.store,
            self.h.root,expected_binding=self.expected)
    def test_positive(self):
        before=c.bundle_bytes(self.b);projected=self.preflight()
        end,bid,noop=self.commit()
        self.assertFalse(noop);self.assertEqual(c.bundle_bytes(end),c.bundle_bytes(projected))
        self.assertEqual(before,c.bundle_bytes(self.b));self.assertFalse(self.b.current.receipt_admissions)
        self.assertEqual(len(end.events),len(self.b.events)+2)
        self.assertEqual(end.current.receipt_admissions[0].attestation,self.x.attestation_operand.attestation.attestation_id)
        self.assertEqual(end.current.external_gates[0].stage,m.ExternalStage.EVIDENCE_RECEIVED)
        self.assertFalse(end.current.receipt_observations)
        self.assertEqual(end.events[-2].result.attestation_operand,self.x.attestation_operand)

    def test_security_negatives_and_substitution(self):
        t=self.x.attestation_operand.attestation
        changes={
            'native_entity':m.EntityId('WRONG-EVIDENCE'),
            'semantic_evidence':replace(t.semantic_evidence,sha256='0'*64),
            'content':replace(t.content,sha256='0'*64),
            'attestor':replace(t.attestor,sha256='0'*64),
            'attestor_authority':replace(t.attestor_authority,sha256='0'*64),
            'source_predicate':m.PredicateId('WRONG-PREDICATE'),
            'source_pin':replace(t.source_pin,sha256='0'*64),
            'scope':'WRONG-SCOPE','lineage':'WRONG-LINEAGE',
            'provenance':replace(t.provenance,sha256='0'*64),
            'proposition':'WRONG-CONTENT-CLAIM'}
        for name,value in changes.items():
            with self.subTest(field=name):
                # Correctly hash the malicious instance: rejection must be semantic.
                args=dict(vars(t));args.pop('attestation_id');args[name]=value
                wrong=ea.materialize(**args)
                x=tx.bind(self.x,wrong,self.expected)
                with self.assertRaises(m.PlannerError):self.preflight(x)
        with self.assertRaises(m.PlannerError):
            self.preflight(replace(self.x,attestation_operand=None))
        with self.assertRaises(m.PlannerError):
            self.preflight(replace(self.x,attestation_operand=True))
        wrong=replace(t,content=replace(t.content,sha256='0'*64))
        with self.assertRaisesRegex(m.PlannerError,'ATTESTATION_SUBSTITUTION'):
            ev.apply(self.b.current,self.x,wrong)
        # Alter both the E02 object and embedded E01 binding; trusted expectation
        # still rejects the apparently self-consistent substitution.
        args=dict(vars(t));args.pop('attestation_id');args['content']=wrong.content
        x=tx.bind(self.x,ea.materialize(**args),replace(self.expected,content_id=wrong.content))
        with self.assertRaisesRegex(m.PlannerError,'TRUSTED_EVIDENCE_BINDING_MISMATCH'):self.preflight(x)
        with self.assertRaisesRegex(m.PlannerError,'TRUSTED_EVIDENCE_BINDING_REQUIRED'):
            c.preflight_external_evidence(self.b,self.x,self.raw,self.h.root)

    def test_parent_state_and_stale_preinstallation_operand(self):
        op=self.x.attestation_operand
        for name,value in [('expected_bundle',c.bundle_id(self.h.bundle)),
                           ('expected_snapshot',c.snapshot_id(self.h.bundle.current)),
                           ('expected_parent_event',self.h.bundle.events[-1].identity)]:
            with self.subTest(field=name):
                x=replace(self.x,attestation_operand=replace(op,**{name:value}))
                x=replace(x,command_key=ev.command_key(x))
                with self.assertRaisesRegex(m.PlannerError,'ATTESTATION_PRE_STATE'):self.preflight(x)
        # Whole command stale after any canonical event, even an ordinary native
        # reevaluation that leaves the domain state otherwise semantically equal.
        change=m.ActionReevaluation((self.b.current.actions[0].id,),c.snapshot_id(self.b.current),self.b.current.actions[0].source)
        after=c.record_result(self.b,change)
        with self.assertRaisesRegex(m.PlannerError,'PARENT_MISMATCH'):
            c.preflight_external_evidence(after,self.x,self.raw,self.h.root,expected_binding=self.expected)

    def test_idempotence_and_conflicting_command(self):
        end,bid,_=self.commit();again,original,noop=self.commit()
        self.assertTrue(noop);self.assertEqual(original,bid);self.assertEqual(c.bundle_bytes(again),c.bundle_bytes(end))
        t=self.x.attestation_operand.attestation
        wrong=replace(self.x,attestation_operand=replace(self.x.attestation_operand,
            attestation=replace(t,attestation_id=replace(t.attestation_id,sha256='0'*64))))
        with self.assertRaisesRegex(m.PlannerError,'IDEMPOTENCY_CONFLICT'):self.commit(wrong)
        self.assertEqual(c.bundle_bytes(c._read_head(self.store,self.b,self.h.root)),c.bundle_bytes(end))

    def test_failure_injection_preserves_canonical_head(self):
        # Fail at private admission, receipt, source publication, and HEAD switch.
        real=c._extend_private
        def fail_receipt(b,r):
            if type(r) is m.ExternalEvent:raise OSError('injected receipt failure')
            return real(b,r)
        real_replace=os.replace
        def fail_head(a,b):
            if str(b).endswith('/HEAD.json'):raise OSError('injected HEAD failure')
            return real_replace(a,b)
        cases=[patch('adapter.planner.codec._extend_private',side_effect=OSError('admission')),
               patch('adapter.planner.codec._extend_private',side_effect=fail_receipt),
               patch('adapter.planner.codec._write_immutable',side_effect=OSError('publication')),
               patch('adapter.planner.codec.os.replace',side_effect=fail_head)]
        for n,case in enumerate(cases):
            store=self.h.root/('failure-'+str(n))
            with case,self.assertRaises(OSError):self.commit(store=store)
            self.assertFalse((store/'HEAD.json').exists())
            self.assertEqual(c.bundle_bytes(c._read_head(store,self.b,self.h.root)),c.bundle_bytes(self.b))
            self.assertFalse(self.b.current.receipt_admissions)

    def test_cold_restore_replay_fresh_readers_and_determinism(self):
        end,bid,_=self.commit();path=self.store/('bundle-'+bid.sha256+'.json')
        with patch('adapter.planner.evidence_attestation.materialize',side_effect=AssertionError('new decision')):
            cold=c.restore(path,bid,self.h.root)
            self.assertEqual(c.bundle_bytes(cold),c.bundle_bytes(end))
            self.assertEqual(c.snapshot_id(c._replay(cold)),c.snapshot_id(end.current))
            prefix=c._prefix_bundle(cold,len(self.b.events))
            self.assertEqual(c.bundle_bytes(prefix),c.bundle_bytes(self.b))
            self.assertFalse(prefix.current.receipt_admissions)
        other,otherid,_=self.commit(store=self.h.root/'independent')
        self.assertEqual(otherid,bid);self.assertEqual(c.bundle_bytes(other),c.bundle_bytes(end))
        program="""from pathlib import Path
from adapter.planner import codec as c,model as m,evidence_attestation as ea
import sys
def forbidden(**args):raise AssertionError('new attestation decision')
ea.materialize=forbidden
b=c.restore(Path(sys.argv[1]),m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY,'planner-bundle-v1',sys.argv[2]),Path(sys.argv[3]))
assert len(b.current.receipt_admissions)==1
assert len(b.current.receipt_observations)==0
assert b.current.receipt_admissions[0].attestation==b.events[-2].result.attestation_operand.attestation.attestation_id
assert b.current.external_gates[0].stage is m.ExternalStage.EVIDENCE_RECEIVED
print(c.snapshot_id(c._replay(b)).sha256)
"""
        for seed in ('0','1','7','101'):
            out=subprocess.check_output([sys.executable,'-c',program,str(path),bid.sha256,str(self.h.root)],text=True,
                env=dict(os.environ,PYTHONPATH=str(ROOT),PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED=seed))
            self.assertEqual(out.strip(),c.snapshot_id(end.current).sha256)

if __name__=='__main__':unittest.main()
