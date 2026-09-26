import copy
import unittest

from adapter.temporal_authority import (
    TemporalAuthorityError,
    validate_current_eligibility,
    validate_historical_validity,
    validate_transition_ancestry,
)


R12 = "sha256:r12-runtime"
R3 = "sha256:r3-runtime"
BOOTSTRAP = "RUNTIME-AUTHORITY-BOOTSTRAP-sha256:bootstrap"
ADOPTION = "ENROLLED-RUNTIME-ADOPTION-DECISION-sha256:adoption"


def predecessor():
    return {
        "authorization_id": "auth-e1-wp-001-r12",
        "runtime_identity": R12,
        "operational_binding": "historical-a59-binding",
        "disposition": "CANCELLED / INTERRUPTED_NO_EFFECTS",
        "ownership": "RELEASED", "quiescent": True,
        "model_requests": 0, "provider_requests": 0, "action_requests": 0,
        "executions": 0, "repository_effects": 0, "knowledge_effects": 0,
        "unresolved_uncertainty": False,
    }


def transition():
    return {"bootstrap": BOOTSTRAP, "adoption": ADOPTION,
            "predecessor_runtime": R12, "successor_runtime": R3,
            "status": "ADOPTED"}


class TemporalAuthorityTests(unittest.TestCase):
    def test_historical_and_current_are_separate(self):
        old = validate_historical_validity(predecessor(), runtime_identity=R12,
                                           operational_binding="historical-a59-binding")
        validate_transition_ancestry(transition(), historical_runtime=R12,
                                     current_runtime=R3, bootstrap_id=BOOTSTRAP,
                                     adoption_id=ADOPTION)
        result = validate_current_eligibility(
            old, transition(), current_runtime=R3,
            current_operational_binding="current-1ab-binding",
            predecessor_id="auth-e1-wp-001-r12")
        self.assertTrue(result["historical_binding_preserved"])

    def test_historical_mutation_fails(self):
        row = predecessor(); row["operational_binding"] = "current-1ab-binding"
        with self.assertRaises(TemporalAuthorityError):
            validate_historical_validity(row, runtime_identity=R12,
                                         operational_binding="historical-a59-binding")

    def test_transition_tampering_fails(self):
        for field, value in (("bootstrap", "wrong"), ("adoption", "wrong"),
                             ("predecessor_runtime", R3), ("successor_runtime", R12)):
            bad = transition(); bad[field] = value
            with self.assertRaises(TemporalAuthorityError):
                validate_transition_ancestry(bad, historical_runtime=R12,
                                             current_runtime=R3,
                                             bootstrap_id=BOOTSTRAP,
                                             adoption_id=ADOPTION)

    def test_effect_or_uncertainty_fails(self):
        for field, value in (("model_requests", 1), ("repository_effects", 1),
                             ("unresolved_uncertainty", True), ("ownership", "HELD")):
            bad = predecessor(); bad[field] = value
            with self.assertRaises(TemporalAuthorityError):
                validate_historical_validity(bad, runtime_identity=R12,
                                             operational_binding="historical-a59-binding")


if __name__ == "__main__":
    unittest.main()
