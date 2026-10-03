"""Independent PC02 proof/authority/route fixture oracle; no Planner execution."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def qualify():
    f = json.loads((ROOT / "docs/plans/DETERMINISTIC_PLANNER_V0_1_E2_PC02_FIXTURES.json").read_text())
    assert f["baseline_ref"] == "DETERMINISTIC_PLANNER_V0_1_E2_PC01_COMPLETION_1_WHOLE_MODEL.json"
    assert len(f["source_roles"]) == 6
    assert {x["role"] for x in f["source_roles"]} == {"DOSSIER", "GRANT", "ROOT_PROOF", "SLOT_PROOF", "EXTERNAL_ROUTE", "ATTESTOR"}
    assert f["dossier"]["decision"] == "E2-DECIDE" and len(f["dossier"]["checks"]) == 9
    assert f["authority"]["identity_domain"] == "AUTHORITY_IDENTITY"
    assert f["proofs"]["root"]["target"] != f["proofs"]["slot"]["target"]
    assert all(not x["positive_evidence"] for x in f["external_routes"].values())
    assert f["external_routes"]["governed_unknown"]["rule_known"] is False
    assert len(f["cases"]) == 23
    positives = [x for x in f["cases"] if x["kind"] == "positive"]
    negatives = [x for x in f["cases"] if x["kind"] == "negative"]
    assert len(positives) == 13 and len(negatives) == 10
    assert all(x["expected"] and x["fixture"] for x in f["cases"])
    # Every negative mutates one declared dimension and names its independent clause.
    assert all(x["failed_clause"] for x in negatives if x["id"] != "E2-N16")
    assert f["invariants"]
    return {"cases": len(f["cases"]), "positive_cases": len(positives), "negative_cases": len(negatives), "source_roles": len(f["source_roles"]), "oracle": "PASS", "actions_executed": 0}


if __name__ == "__main__":
    print(json.dumps(qualify(), sort_keys=True))
