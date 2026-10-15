"""Generic A09 postcondition qualification; no canonical P04 commits."""
from dataclasses import replace
import unittest
from unittest.mock import patch
from adapter.planner import codec as c,core,model as m,evidence_transaction as tx
from adapter.tests.test_planner_evidence_transaction import EvidenceTransactionTests
from adapter.tests.test_planner_evidence_admission import setup_fixture
from adapter.tests.test_planner_typed_proofs import fixture,candidate


class ReceiptPostconditionTests(unittest.TestCase):
    def setUp(self):
        self.h=EvidenceTransactionTests();self.h.setUp();self.addCleanup(self.h.tearDown)
        self.b,self.x=self.h.b,self.h.x
        self.expected=tx.receipt_oracle(self.b.current,self.x)
    def test_exact_delta_and_unordered_collections(self):
        end=self.h.preflight()
        tx.check_receipt_postcondition(self.expected,end.current)
        self.assertEqual(c.snapshot_id(self.expected),c.snapshot_id(end.current))
        # The codec declares entities/statuses unordered, while history is causal.
        unordered=replace(end.current,entities=tuple(reversed(end.current.entities)),statuses=tuple(reversed(end.current.statuses)))
        tx.check_receipt_postcondition(self.expected,unordered)
        self.assertFalse(any(e.validated for e in end.current.entities if e.kind is m.EntityKind.EVIDENCE))
        self.assertFalse(end.current.receipt_observations)
        self.assertFalse(end.current.validation_instances)
        self.assertFalse(end.current.typed_proofs)
        self.assertFalse(core.resume_eligibility(end,self.h.h.root).allowed)

    def test_received_only_frame_rejects_lifecycle_skips(self):
        s=self.expected;e=next(e for e in s.entities if e.id==self.x.entity.id);g=s.external_gates[0]
        proof_state=fixture();proof=candidate(proof_state.proof_contracts[0])
        validation=m.ValidationInstance(self.x.admission.authentication,'unsupplied validation',e.identity,(e.identity,),m.ValidationOutcome.PASS,s.context.scope,s.context.lineage,m.ValidationState.ACCEPTED,e.provenance)
        tests={
          'validated_Evidence':replace(s,entities=tuple(replace(e,validated=True,validation=m.ValidationState.ACCEPTED) if z.id==e.id else z for z in s.entities)),
          'validation_result':replace(s,validation_instances=(validation,)),
          'proof_admission':replace(s,typed_proofs=(proof,)),
          'proof_contract_installation':replace(s,proof_contracts=proof_state.proof_contracts),
          'accepted_observation':replace(s,receipt_observations=(m.ReceiptObservation(g.id,e.id,True,(),self.x.admission.claims),)),
          'validated_gate':replace(s,external_gates=(replace(g,stage=m.ExternalStage.EVIDENCE_VALIDATED),)),
          'reentry_gate':replace(s,external_gates=(replace(g,stage=m.ExternalStage.DEPENDENT_ACTION_REENTRY),)),
          'action_completion':replace(s,statuses=tuple(replace(z,state=m.ActionState.COMPLETED) if z.id==s.actions[0].id else z for z in s.statuses)),
          'actionability':replace(s,statuses=tuple(replace(z,state=m.ActionState.ACTIONABLE) if z.id==s.actions[0].id else z for z in s.statuses)),
          'knowledge':replace(s,knowledge=proof_state.knowledge),
          'root':replace(s,roots=tuple(replace(z,state=m.ConditionState.SATISFIED) for z in s.roots)),
          'source_policy_context':replace(s,context=replace(s.context,generation='foreign')),
          'auth_configuration':replace(s,ingress_contracts=()),
          'receipt_identity':replace(s,receipt_admissions=tuple(replace(z,attestation=e.identity) for z in s.receipt_admissions)),
          'causal_history':replace(s,external_gates=(replace(g,history=tuple(reversed(g.history))),))}
        # Generic fixture may have no roots; use its independently typed root to
        # test forbidden root addition instead of a no-op replacement.
        tests['root']=replace(s,roots=proof_state.roots)
        tests['slot']=replace(s,slots=proof_state.slots)
        for name,wrong in tests.items():
            with self.subTest(name=name),self.assertRaises(m.PlannerError):
                tx.check_receipt_postcondition(s,wrong)

    def test_postcondition_failure_cannot_publish(self):
        with patch('adapter.planner.evidence_transaction.check_receipt_postcondition',side_effect=m.PlannerError('RECEIPT_POSTCONDITION')):
            with self.assertRaisesRegex(m.PlannerError,'RECEIPT_POSTCONDITION'):self.h.commit()
        self.assertFalse((self.h.store/'HEAD.json').exists())
        self.assertFalse(any((self.h.h.root/p.path).exists() for p in self.x.source_additions))

    def test_legacy_derived_blocker_diagnostics_are_not_control_transition(self):
        root,b,x,raw=setup_fixture(self)
        # This fixture's raw statuses are prospective; admission must publish
        # the E03 derived BLOCKED projection, not leave ACTION_ELIGIBLE cached.
        before=core.recompute(b.current)
        projected=c.preflight_external_evidence(b,x,{x.entity.provenance.path:raw},root)
        after=core.recompute(projected.current)
        self.assertEqual(before.control,after.control)
        self.assertEqual(before.actionable,after.actionable)
        self.assertNotEqual(before.blocked,after.blocked)
        self.assertFalse(projected.current.receipt_observations)
        end,bid,noop=c.admit_external_evidence(b,x,{x.entity.provenance.path:raw},root/'fixed-head',root)
        self.assertFalse(noop)
        self.assertEqual(c.bundle_bytes(end),c.bundle_bytes(projected))
        cold=c.restore(root/'fixed-head'/('bundle-'+bid.sha256+'.json'),bid,root)
        self.assertEqual(core.recompute(cold.current),after)

if __name__=='__main__':unittest.main()
