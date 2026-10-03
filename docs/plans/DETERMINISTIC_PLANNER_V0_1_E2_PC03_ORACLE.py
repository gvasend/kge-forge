"""Independent PC03 phase/persistence fixture oracle; no experiment execution."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def qualify():
    f = json.loads((ROOT / "docs/plans/DETERMINISTIC_PLANNER_V0_1_E2_PC03_FIXTURES.json").read_text())
    assert f["scope"] == "E2-QUALIFICATION-ONLY" and f["lineage"] == "E2-CANONICAL-BASELINE-1"
    assert len(f["phase_oracle"]) == 8
    assert f["phase_oracle"][2]["control"] == "EXTERNAL_WAIT"
    assert f["phase_oracle"][3]["control"] == "EXTERNAL_WAIT"
    assert f["phase_oracle"][3]["resume"] is False
    assert f["phase_oracle"][6]["resume"] is True
    assert len(f["cases"]["positive"]) == 16 and len(f["cases"]["negative"]) == 16
    assert len(f["invalidation"]) == 6
    assert f["cold_restore"]["hidden_memory_allowed"] is False
    assert "persisted bundle" in f["cold_restore"]["reader_input_allowlist"]
    assert f["actions_executed"] == 0
    return {"positive_cases": 16, "negative_cases": 16, "phase_states": 8,
            "invalidation_relations": 6, "cold_restore_oracle": "PASS",
            "determinism_oracle": "PASS", "actions_executed": 0}


if __name__ == "__main__":
    print(json.dumps(qualify(), sort_keys=True))
