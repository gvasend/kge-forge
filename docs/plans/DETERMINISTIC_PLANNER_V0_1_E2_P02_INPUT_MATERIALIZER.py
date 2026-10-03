"""Materialize the already-qualified PC01 model as PLANNER-SNAPSHOT-1.

This is input qualification only. It constructs no result event and executes
no E2 Action. The semantic builder is the pinned PC01 whole-model oracle.
"""
import hashlib
import json
import sys
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from adapter.planner import codec
from docs.plans.DETERMINISTIC_PLANNER_V0_1_E2_PC01_WHOLE_MODEL_ORACLE import build


def main():
    snapshot, _root, helper = build()
    try:
        raw = codec.snapshot_bytes(snapshot)
        decoded = codec.decode_snapshot(raw)
        sid = codec.snapshot_id(snapshot).sha256
        assert codec.snapshot_id(decoded).sha256 == sid
        assert raw == codec.snapshot_bytes(decoded)
        out = ROOT / "docs/plans/DETERMINISTIC_PLANNER_V0_1_E2_P02_INITIAL_SNAPSHOT.json"
        out.write_bytes(raw)
        validation = {
            "schema": "E2-P02-input-closure-v1",
            "snapshot_format": "PLANNER-SNAPSHOT-1",
            "snapshot_identity": sid,
            "snapshot_content_identity": hashlib.sha256(raw).hexdigest(),
            "source_model_identity": sid,
            "actions": [a.id.value for a in snapshot.actions],
            "action_count": len(snapshot.actions),
            "decision_routes": [
                {
                    "decision": d.action.value,
                    "input_action": d.input_action.value if d.input_action else None,
                    "semantic_action": d.semantic_action.value if d.semantic_action else None,
                    "stage": d.stage.value,
                    "downstream": [x.value for x in d.downstream],
                    "provenance": d.provenance.path,
                }
                for d in snapshot.decisions
            ],
            "native_encode": "PASS",
            "native_decode": "PASS",
            "semantic_round_trip": "PASS",
            "initial_control": "RUNNABLE",
            "initial_actionable": [x.value for x in __import__("adapter.planner.core", fromlist=["recompute"]).recompute(snapshot).actionable],
            "initial_selection": __import__("adapter.planner.core", fromlist=["recompute"]).recompute(snapshot).selection.selected.value,
            "experiment_actions_executed": 0,
        }
        (ROOT / "docs/plans/DETERMINISTIC_PLANNER_V0_1_E2_P02_INPUT_VALIDATION.json").write_text(json.dumps(validation, indent=2) + "\n")
        print(json.dumps(validation, sort_keys=True))
    finally:
        helper.doCleanups()


if __name__ == "__main__":
    main()
