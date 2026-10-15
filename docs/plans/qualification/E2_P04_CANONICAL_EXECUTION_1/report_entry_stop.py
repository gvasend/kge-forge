"""Publish the read-only contract stop; never run a native transaction."""
import hashlib
import json
import subprocess
from pathlib import Path

from adapter.planner import codec as c, model as m

ROOT = Path(__file__).resolve().parents[4]
D = ROOT / "docs/plans"
O = Path(__file__).resolve().parent
Q = D / "qualification/FINISH_F02_1"
P = "DETERMINISTIC_PLANNER_V0_1_"


def read(path):
    return json.loads(path.read_text())


def uid(value):
    return value.namespace + ":" + value.sha256


def ref(path):
    return {"path": str(path.relative_to(ROOT)),
            "raw_file_sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    entry = read(O / "entry-reader-seed-0.json")
    workflow = read(Q / "bounded-installation-workflow.json")
    oracles = read(Q / "boundary-oracles.json")
    preservation = read(O / "preservation.json")
    assert all(entry["checks"].values())
    assert not entry["proof_contracts"]
    assert all(not x["native_contract_current"] for x in entry["prospective_proof_declarations"])
    target_path = D / (P + "E2_P04_CANONICAL_TARGET_BUNDLE.json")
    assert not target_path.exists()
    bundle = c._unwire(read(D / (P + "E2_P04_FINAL_PREEXECUTION_CONFIGURATION_BUNDLE_1.json"))["bundle"])
    state = bundle.current
    checkpoints = read(D / "qualification/FINISH_F03_1/isolated-checkpoints.json")
    required = []
    for step, name, previous in [(workflow["steps"][2], "slot-contract", "post-a12"),
                                (workflow["steps"][3], "root-contract", "post-slot-proof")]:
        qualified = c._unwire(read(Path(checkpoints[name]["path"]))["bundle"])
        event = qualified.events[-1]
        assert type(event.result) is m.InstallDefinition
        assert event.result.operation is m.InstallationOperation.INSTALL
        definition = step["definition"]
        body = read(ROOT / definition["body"]["path"])
        contract = c._unwire(body["contract"])
        required.append({
            "workflow_ordinal": step["ordinal"], "boundary": step["boundary"],
            "operation": step["operation"], "event_type": "INSTALL_DEFINITION",
            "definition": definition, "native_contract_id": uid(contract.id),
            "actual_current_in_entry": False, "required_support_precondition": step["pre_state"],
            "qualified_prior_boundary": previous, "qualified_install_event_id": uid(event.identity),
            "qualified_event_role": "PRIOR_ISOLATED_QUALIFICATION_ONLY; NOT_CANONICAL_EXECUTION_IN_THIS_PACKAGE",
            "ordinary_parent_required": True, "allowed_in_requested_run": False,
        })
    terms = {}

    def term(name, expected, actual, passed):
        terms[name] = {"expected": expected, "actual": actual, "pass": bool(passed)}

    term("actual_A09_Evidence_and_receipt", "admitted/current",
         {"receipt_admissions": len(state.receipt_admissions)}, bool(state.receipt_admissions))
    term("actual_A10_ValidationResult", "accepted/current",
         {"validation_results": len(state.validation_results)}, bool(state.validation_results))
    term("actual_A10_support", "present/current",
         {"support_records": len(state.validation_support_records)}, bool(state.validation_support_records))
    reentry_events = [e for e in bundle.events if type(e.result) is m.DecisionReentry or
                      (type(e.result) is m.ExternalEvent and
                       e.result.stage is m.ExternalStage.DEPENDENT_ACTION_REENTRY)]
    term("required_A11_reentry_event_history", "both native reentry events accepted",
         [uid(e.identity) for e in reentry_events], len(reentry_events) == 2)
    statuses = {x.id.value: x.state.value for x in state.statuses}
    knowledge = {x.id.value: x for x in state.knowledge}
    term("A12_REENTER_completed", "COMPLETED", statuses["E2-REENTER"],
         statuses["E2-REENTER"] == "COMPLETED")
    for action, output in [("E2-REENTER", "E2-K-REENTER"), ("E2-FINISH", "E2-K-FINISH")]:
        accepted = next(a for a in state.actions if a.id.value == action).accepted_inventory
        actual = knowledge.get(output)
        term(output + "_actual_admitted_current", "exact sealed accepted inventory",
             c._wire(actual) if actual else None,
             actual is not None and actual in accepted and statuses[action] == "COMPLETED")
    term("slot_concrete_contract_current", True, False, False)
    term("root_concrete_contract_current", True, False, False)
    expected_proofs = oracles["oracles"]["P04_TARGET"]["typed_proofs"]
    actual_proofs = [{"kind": p.id.kind.value, "namespace": p.id.namespace, "sha256": p.id.sha256}
                     for p in state.typed_proofs]
    term("exact_typed_SLOT_and_ROOT_proofs", expected_proofs, actual_proofs,
         sorted(expected_proofs, key=lambda x: x["sha256"]) == sorted(actual_proofs, key=lambda x: x["sha256"]))
    slot = next(x for x in state.slots if x.id.value == "E2-SLOT")
    root = next(x for x in state.roots if x.id.value == "E2-ROOT")
    term("E2_SLOT_state", "RESOLVED", slot.state.value, slot.state is m.SlotState.RESOLVED)
    term("E2_ROOT_state", "SATISFIED", root.state.value, root.state is m.ConditionState.SATISFIED)
    term("FINISH_completed", "COMPLETED", statuses["E2-FINISH"], statuses["E2-FINISH"] == "COMPLETED")
    term("all_six_Actions_completed", 6, sum(x.state is m.ActionState.COMPLETED for x in state.statuses),
         all(x.state is m.ActionState.COMPLETED for x in state.statuses))
    satisfied_roots = {x.id for x in state.roots if x.state is m.ConditionState.SATISFIED}
    term("all_declared_goals_satisfied", True, all(g.target in satisfied_roots for g in state.goals),
         all(g.target in satisfied_roots for g in state.goals))
    expected_goals = oracles["oracles"]["P04_TARGET"]["goal_inventory"]
    term("goal_inventory_preserved", expected_goals, c._wire(state.goals),
         c.canonical_bytes(expected_goals) == c.canonical_bytes(c._wire(state.goals)))
    term("final_control", "TERMINAL_SUCCESS", entry["control"], entry["control"] == "TERMINAL_SUCCESS")
    term("independent_root_source_and_semantic_authority_current", True,
         entry["checks"]["source_semantic_authority_applicability"],
         entry["checks"]["source_semantic_authority_applicability"])
    pins_current = entry["checks"]["source_pins_exact"] and entry["checks"]["policy_pin_exact"]
    term("exact_source_and_policy_pins", True, pins_current, pins_current)
    term("scope_lineage_generation_preserved", True, entry["checks"]["scope_lineage_generation_exact"],
         entry["checks"]["scope_lineage_generation_exact"])
    term("complete_A09_A13_causal_event_prefix", "canonical lifecycle appended at ordinary parents",
         {"new_events": 0, "configuration_event_count": len(bundle.events)}, False)
    term("entry_ledger_ancestry_preserved", True, True, True)
    term("no_computed_eligibility_persisted", True, True, True)
    term("no_P05_P06_executed", True, True, True)
    assert not all(t["pass"] for t in terms.values())
    counterexample = {
        "kind": "PRE_EXECUTION_CONTRACT_COMPATIBILITY_COUNTEREXAMPLE", "boundary": "BEFORE_A09",
        "classification": "SEALED_WORKFLOW_CONFLICTS_WITH_NO_INSTALL_EXECUTION_RESTRICTION",
        "expected": "Reach the canonical target through the exact qualified A09-A13 path with zero prospective definition installation events.",
        "actual": {"concrete_proof_contract_count": 0, "declared_contract_native_currentness": [False, False],
                   "required_prohibited_events": [{"ordinal": x["workflow_ordinal"],
                                                    "type": x["definition"]["definition_type"],
                                                    "operation": x["operation"], "boundary": x["boundary"]}
                                                   for x in required]},
        "state_id": entry["state_id"], "event_id": None,
        "last_accepted_event_id": entry["append_head"],
        "actual_runtime_admission_failure_observed": False,
        "runtime_error_not_executed": "proof does not match independent contract",
        "runtime_error_role": "SOURCE_CODE_BRANCH_ONLY; NO_PROOF_SUBMISSION_MADE",
        "live_repair_attempted": False,
    }
    predicates = [
        {"path": "adapter/planner/typed_proofs.py", "line": 45,
         "predicate": "TypedProof.contract must resolve in Snapshot.proof_contracts and all independent contract fields must match.",
         "absent_contract_error": "proof does not match independent contract"},
        {"path": "adapter/planner/proof_installation.py", "line": 180,
         "predicate": "Configured target requires a corresponding current installed concrete contract record.",
         "observed_entry_result": False},
        {"path": "adapter/planner/proof_installation.py", "line": 219,
         "predicate": "Slot contract INSTALL requires exact actual current completed REENTER knowledge."},
        {"path": "adapter/planner/proof_installation.py", "line": 222,
         "predicate": "Root contract INSTALL requires the sole usable expected slot proof and resolved slot."},
        {"path": "adapter/planner/proof_installation.py", "line": 225,
         "predicate": "Governed INSTALL inserts the concrete contract; ordinary proof admission does not install it."},
    ]
    writer = read(D / "qualification/FINISH_F03_1/reader-manifests/final-preexecution.json")
    report = {
        "schema": "PLANNER-CANONICAL-E2-P04-EXECUTION-RESULT-1",
        "WORK_PACKAGE": "CANONICAL-E2-P04-A09-A13-EXECUTION", "RESULT": "BLOCKED",
        "ENTRY_GATE": "PASS", "EXECUTION_CONTRACT_COMPATIBILITY": "FAIL", "FIRST_COUNTEREXAMPLE": counterexample,
        "A09_RESULT": "NOT_EXECUTED", "EVIDENCE_ID": None, "RECEIPT_ID": None,
        "A10_RESULT": "NOT_EXECUTED", "VALIDATION_RESULT_ID": None, "SUPPORT_ID": None,
        "A11_RESULT": "NOT_EXECUTED", "A11_REENTRY_EVENT_IDS": [], "C03_RESULT": entry["semantic"]["resume"],
        "A12_RESULT": "NOT_EXECUTED", "E2_REENTER_RESULT_ID": None, "E2_K_REENTER": "ABSENT",
        "SLOT_PROOF_ID": None, "E2_SLOT_STATE": "UNRESOLVED",
        "ROOT_SOURCE": "INSTALLED_CURRENT_SEALED_DECLARATION", "ROOT_SOURCE_INDEPENDENCE": "PASS_INSTALLED_DECLARATIONS",
        "ROOT_PROOF_ID": None, "E2_ROOT_STATE": "UNRESOLVED", "FINISH_REEVALUATION": "NOT_EXECUTED",
        "E2_FINISH_RESULT_ID": None, "E2_K_FINISH": "ABSENT", "P04_EXIT_PREDICATE": False, "E2_P04_RESULT": "BLOCKED",
        "FINAL_P04_BUNDLE_ID": None, "FINAL_LEDGER_ROOT": None, "FINAL_APPEND_HEAD": None,
        "PERSISTENCE": "NOT_RUN_NO_CANONICAL_TARGET", "COLD_RESTORE": "PASS_ENTRY_ONLY; TARGET_NOT_RUN",
        "REPLAY": "PASS_ENTRY_CONFIGURATION_PREFIX_ONLY; P04_LIFECYCLE_NOT_RUN",
        "DETERMINISM": "NOT_RUN_NO_CANONICAL_TARGET", "SEALED_NEGATIVES": "NOT_RUN_AFTER_STOP",
        "E2_P05_READY": "NO", "NEXT_PACKAGE": "P04_EXECUTION_CONTRACT_RECONCILIATION",
        "F03_P04_EXECUTION_READY": "YES",
        "P04_EXECUTION_READY": "NO", "E2_P04_READY": "NO",
        "CANONICAL_A09_A13_EXECUTED": "NO", "E2_FINISH_EXECUTED": "NO", "NEW_SEMANTIC_AUTHORITY_ISSUED": "NO",
        "NEW_INSTALL_AUTHORITY_ADMITTED": "NO", "DEFINITIONS_INSTALLED": "NO", "RUNTIME_MODIFIED": "NO",
        "P03_RESULT": "PASS", "P03_HISTORICAL_CORRESPONDENCE": "UNPROVEN", "N_REAL_SATISFIED": "NO",
        "CANONICAL_E2_QUALIFIED": "NO", "E1_ARTIFACTS_MODIFIED": 0, "PRODUCTION_EFFECT": "NO",
        "entry_gate": {"result": "PASS", "independent_checks": entry["checks"], "input_bundle_id": entry["bundle_id"],
                       "state_id": entry["state_id"], "append_head": entry["append_head"],
                       "native_ledger_anchor": entry["native_ledger_anchor"],
                       "ledger_identity_domain": "FIRST_NATIVE_EVENT; NO_SEPARATE_LEDGER_ID_OR_MERKLE_ROOT_FIELD",
                       "event_count": entry["event_count"], "installed_definitions": entry["installed_definitions"],
                       "concrete_contracts": entry["proof_contracts"], "prospective_declarations": entry["prospective_proof_declarations"],
                       "reader_evidence": ref(O / "entry-reader-seed-0.json")},
        "execution_guard": {"result": "FAIL", "literal_snapshot_entry_gate_passed": True,
                            "restriction": "No prospective definition installation is permitted during this run.",
                            "F03_qualified_path_requires_deferred_installation": True,
                            "existing_F03_PASS_not_changed": True, "required_deferred_steps": required},
        "readiness_scopes": {"F03_published_readiness": "YES_FOR_QUALIFIED_DEFERRED_INSTALLATION_PATH",
                             "current_execution_readiness": "NO_FOR_REQUESTED_NO_INSTALL_PATH",
                             "F03_declared_stages": {a + "_READY": "YES" for a in ["A09", "A10", "A11", "A12", "A13"]}},
        "native_predicates": predicates,
        "execution_trace": [{"stage": a, "status": "NOT_EXECUTED", "reason": "PREFLIGHT_WORKFLOW_CONFLICT",
                             "pre_state_id": entry["state_id"], "post_state_id": entry["state_id"],
                             "append_head_unchanged": entry["append_head"], "event_ids": []}
                            for a in ["A09", "A10", "A11", "A12", "A13"]],
        "actual_ActionResults": [], "proof_admissions": [], "new_event_count": 0,
        "sealed_boundary_oracles": ref(Q / "boundary-oracles.json"),
        "target_exit_evaluation": {"evaluated_state_role": "UNCHANGED_PREEXECUTION_STATE; NOT_A_TARGET",
                                   "terms": terms, "predicate": False},
        "persistence": {"canonical_target_bundle_created": False,
                        "requested_target_bundle_path": str(target_path.relative_to(ROOT)),
                        "reason": "TARGET_NOT_REACHED; NO_PREEXECUTION_OR_ISOLATED_BUNDLE_RELABELED_AS_TARGET",
                        "entry_bundle_unchanged": True},
        "cold_restore": {"entry_result": "PASS", "reader_pid": entry["pid"],
                         "reader_pid_namespace": entry["pid_namespace"], "reader_hash_seed": entry["hash_seed"],
                         "reader_exit_code": 0, "prior_F03_writer_pid": writer["writer_pid"],
                         "prior_F03_writer_pid_namespace": writer["writer_pid_namespace"],
                         "prior_F03_writer_termination_record": writer["writer_terminated"],
                         "fresh_reader_independent_of_recorded_writer": entry["pid_namespace"] != writer["writer_pid_namespace"],
                         "target_result": "NOT_RUN"},
        "replay": {"entry_prefix": "PASS_NATIVE_RESTORE_REPLAY", "event_count": 9, "new_lifecycle_replay": "NOT_RUN"},
        "determinism": {"canonical_target_comparisons": "NOT_RUN", "reason": "NO_CANONICAL_TARGET; STOP_BEFORE_A09",
                        "prior_F03_qualification": "UNCHANGED; QUALIFIES_DEFERRED_INSTALLATION_PATH_ONLY"},
        "sealed_negatives": {"current_run": "NOT_RUN_AFTER_STOP", "prior_F03_negative_suite": "PASS_HISTORICAL_QUALIFICATION_ONLY",
                             "current_run_claims_no_negative_suite_PASS": True},
        "P05_readiness": {"P04_PASS_prerequisite": False, "E2_P05_READY": "NO",
                          "downstream_prerequisites": "NOT_EVALUATED; P04_NOT_PASS", "P05_EXECUTED": False, "P06_EXECUTED": False},
        "regressions": {"current_run": "NOT_RUN_NO_RUNTIME_CHANGE_AND_EXECUTION_STOPPED",
                        "prior_frozen_E1_broad_suite_collection_issue": "REMAINS_SEPARATE; NO_BROAD_SUITE_PASS_CLAIM",
                        "prior_three_legacy_Evidence_admission_fixture_failures": "REMAINS_SEPARATE"},
        "preservation": preservation,
    }
    paths = [D / (P + "E2_P04_FINAL_PREEXECUTION_CONFIGURATION_BUNDLE_1.json"),
             D / (P + "FINISH_F03_RESULT.md"), D / (P + "FINISH_F03_RESULT.json"),
             D / (P + "CANONICAL_QUALIFICATION_EXPERIMENT_1.md"),
             D / (P + "CANONICAL_QUALIFICATION_ACCEPTANCE_MATRIX_1.md"),
             Q / "sealed-manifest.json", Q / "bounded-installation-workflow.json", Q / "boundary-oracles.json",
             D / "qualification/FINISH_F03_1/isolated-checkpoints.json",
             D / "qualification/FINISH_F03_1/isolated-execution-trace.json"]
    report["authoritative_inputs"] = [ref(path) for path in paths]
    subprocess.run(["git", "diff", "--check"], cwd=ROOT, check=True, capture_output=True)
    report["GIT_DIFF_CHECK"] = "PASS"
    report["preservation"]["git_diff_check"] = "PASS"
    (O / "contract-conflict.json").write_bytes(c.canonical_bytes({
        "schema": "PLANNER-P04-EXECUTION-CONTRACT-COMPATIBILITY-1", "result": "FAIL",
        "counterexample": counterexample, "required_deferred_steps": required, "native_predicates": predicates}))
    (D / (P + "E2_P04_CANONICAL_EXECUTION_RESULT.json")).write_bytes(c.canonical_bytes(report))
    print(json.dumps({"RESULT": "BLOCKED", "ENTRY_GATE": "PASS", "snapshot_checks": len(entry["checks"]),
                      "forbidden_required_INSTALL_events": len(required), "canonical_lifecycle_events_submitted": 0,
                      "canonical_target_bundle_created": False, "exit_terms": len(terms), "P04_EXIT_PREDICATE": False}))


if __name__ == "__main__":
    main()
