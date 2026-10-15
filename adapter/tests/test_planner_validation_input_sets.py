"""Generic codec/input-set invariants; no installed or lifecycle fixture."""
import itertools
import unittest
from dataclasses import replace
from adapter.planner import codec as c,model as m,validation_transaction as vt

class ValidationInputSetTests(unittest.TestCase):
 def identity(self,n,namespace='test-input'):
  return m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY,namespace,'%064x'%n)
 def assessment(self,inputs):
  identity=self.identity(99)
  provenance=m.Provenance('TEST/input.json',identity,'/','{}','SYNTHETIC_TEST','TEST')
  value=m.ValidationAssessment(identity,identity,inputs,identity,'TEST-RULE',(),m.ValidationOutcome.FAIL,'TEST','TEST-LINEAGE','TEST-GENERATION',provenance)
  return vt.identified(value,'planner-validation-assessment-v1')
 def test_equivalent_permutations_preserve_identity_and_canonical_projection(self):
  for size in (0,1,2,3,5):
   expected=tuple(self.identity(n) for n in range(size))
   original=self.assessment(expected)
   for permutation in itertools.permutations(expected):
    actual=self.assessment(permutation)
    self.assertEqual(actual.id,original.id)
    self.assertEqual(c.canonical_bytes(c._wire(actual)),c.canonical_bytes(c._wire(original)))
    self.assertEqual(vt.canonical_inputs(permutation),expected)
 def test_duplicates_rejected_not_silently_deduplicated(self):
  a=self.identity(1)
  with self.assertRaises(m.PlannerError):vt.canonical_inputs((a,a))
  self.assertNotEqual(c.canonical_bytes(c._wire(self.assessment((a,a)))),c.canonical_bytes(c._wire(self.assessment((a,)))))
 def test_identity_domains_and_membership_are_not_collapsed(self):
  a=self.identity(1,'a');b=self.identity(1,'b');other=self.identity(2,'b')
  self.assertEqual(vt.canonical_inputs((b,a)),(a,b))
  self.assertNotEqual(self.assessment((a,b)).id,self.assessment((a,other)).id)
  self.assertNotEqual(self.assessment((a,)).id,self.assessment((a,b)).id)
 def test_boolean_or_untyped_identity_rejected(self):
  with self.assertRaises(m.PlannerError):vt.canonical_inputs((True,))
 def test_legacy_projection_order_remains_part_of_its_identity(self):
  a,b=self.identity(1),self.identity(2);provenance=m.Provenance('TEST/input.json',a,'/','{}','SYNTHETIC_TEST','TEST')
  projection=m.ValidationInstance(m.PredicateId('TEST-PREDICATE'),'TEST-PROPOSITION',a,(a,b),m.ValidationOutcome.FAIL,'TEST','TEST-LINEAGE',m.ValidationState.REJECTED,provenance)
  self.assertNotEqual(c.canonical_bytes(c._wire(projection)),c.canonical_bytes(c._wire(replace(projection,inputs=(b,a)))))
if __name__=='__main__':unittest.main()
