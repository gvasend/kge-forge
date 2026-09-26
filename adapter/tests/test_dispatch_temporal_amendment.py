import copy
import unittest

from adapter.dispatch_temporal_amendment import (
    DispatchAmendmentError, authenticate, current_dispatch, digest,
)


ORIGINAL = {
    "id": "E1-ARCHITECT-DISPATCH-sha256:historical",
    "authority": "Architect", "decision": "DISPATCH_AUTHORIZED",
    "work_package_id": "E1-WP-001", "profile": "profile-v2",
    "ModelPayloadDigest": "payload-v2", "transmission": "retention-v2",
    "budget": "budget-v2",
}
TRANSITION = {"id": "TEMPORAL-AMENDMENT-sha256:temporal", "status": "ADOPTED"}
CURRENT = {
    "runtime": "sha256:r3", "runtime_head_authority": "RUNTIME-HEAD-r3",
    "release_authority": "E1-RELEASE-AUTHORITY-sha256:current",
    "OperationalContextId": "E1-OPERATIONAL-CONTEXT-sha256:current",
    "profile": "profile-v2", "ModelPayloadDigest": "payload-v2",
    "transmission": "retention-v2", "budget": "budget-v2",
    "supervisor": "S3", "work_package_id": "E1-WP-001",
}


def amendment():
    return {"schema": "E1-DISPATCH-TEMPORAL-AMENDMENT-1",
            "original_dispatch": ORIGINAL["id"],
            "original_dispatch_sha256": digest(ORIGINAL),
            "temporal_authority_amendment": TRANSITION["id"],
            "current": CURRENT, "authority": "Architect",
            "id": "dispatch-amendment", "current_dispatch": "dispatch-current"}


class DispatchTemporalTests(unittest.TestCase):
    def test_positive_and_immutable_derivation(self):
        a = amendment(); authenticate(ORIGINAL, a, TRANSITION, CURRENT)
        derived = current_dispatch(ORIGINAL, a)
        self.assertEqual(ORIGINAL["id"], derived["historical_dispatch"])
        self.assertEqual(ORIGINAL["id"], ORIGINAL["id"])

    def test_negative_bindings(self):
        cases = [("original_dispatch", "wrong"),
                 ("temporal_authority_amendment", "wrong"),
                 ("authority", "caller"),
                 ("current", {**CURRENT, "runtime": "sha256:wrong"})]
        for key, value in cases:
            a = amendment(); a[key] = value
            with self.assertRaises(DispatchAmendmentError):
                authenticate(ORIGINAL, a, TRANSITION, CURRENT)

    def test_unrelated_scope_changes_fail(self):
        for key in ("work_package_id", "profile", "ModelPayloadDigest", "budget"):
            a = amendment(); a["current"] = {**CURRENT, key: "changed"}
            with self.assertRaises(DispatchAmendmentError):
                authenticate(ORIGINAL, a, TRANSITION, CURRENT)


if __name__ == "__main__":
    unittest.main()
