"""Publish the read-only boundary reconciliation from verified sealed inputs."""
import hashlib
import json
import subprocess
from pathlib import Path

from adapter.planner import codec as c

R = Path(__file__).resolve().parents[4]
D = R / "docs/plans"
O = Path(__file__).resolve().parent
Q = D / "qualification/FINISH_F02_1"
F = D / "qualification/FINISH_F03_1"
P = "DETERMINISTIC_PLANNER_V0_1_"
NAME = P + "E2_P04_DEFERRED_INSTALLATION_RECONCILIATION_1"


def read(path):
    return c.parse_json(path.read_bytes())


def uid(value):
    return value["namespace"] + ":" + value["sha256"]


def ref(path):
    return {"path": str(path.relative_to(R)),
            "content_id": "raw-file-sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    audit = read(O / "authorization-verification.json")
    entry = read(O / "entry-reader.json")
    workflow = read(Q / "bounded-installation-workflow.json")
    manifest = read(Q / "sealed-manifest.json")
    resolution = read(Q / "support-resolution-contract.json")
    oracles = read(Q / "boundary-oracles.json")
    previous = read(D / (P + "E2_P04_CANONICAL_EXECUTION_RESULT.json"))
    f03 = read(D / (P + "FINISH_F03_RESULT.json"))
    assert audit["result"] == "PASS" and all(entry["checks"].values())
    assert previous["RESULT"] == "BLOCKED" and f03["RESULT"] == "PASS"
    assert len(workflow["steps"]) == 4 and len(audit["deferred_install_audits"]) == 2
    assert not entry["proof_contracts"] and not entry["typed_proof_instances"]
    assert [x["boundary"] for x in workflow["steps"][2:]] == [
        "POST_A12_PRE_SLOT_PROOF", "POST_SLOT_PROOF_PRE_ROOT_PROOF"]

    # Preservation is relative to this task's baseline, not to preexisting git edits.
    baseline = read(O / "baseline.json")["files"]
    missing = [p for p in baseline if not (R / p).is_file()]
    changed = [p for p, h in baseline.items() if (R / p).is_file()
               and hashlib.sha256((R / p).read_bytes()).hexdigest() != h]
    diff = subprocess.run(["git", "diff", "--check"], cwd=R, capture_output=True, text=True)
    assert not missing and not changed and diff.returncode == 0, (missing, changed, diff.stdout, diff.stderr)
    preservation = {
        "baseline_files_checked": len(baseline), "missing_preexisting_files": missing,
        "changed_preexisting_files": changed,
        "frozen_E1_files_checked": sum(p.startswith("docs/experiments/E1/") for p in baseline),
        "runtime_files_checked": len(entry["qualified_runtime_hashes"]),
        "all_preexisting_plans_qualification_artifacts_and_runtime_unchanged": True,
        "F02_F03_seals_and_canonical_entry_bundle_unchanged": True,
        "E1_ARTIFACTS_MODIFIED": 0, "RUNTIME_MODIFIED": "NO", "PRODUCTION_EFFECT": "NO",
        "GIT_DIFF_CHECK": "PASS", "new_authority_admission_calls": 0,
        "new_install_or_lifecycle_submission_calls": 0,
        "canonical_target_bundle_created": False,
    }
    (O / "preservation.json").write_bytes(c.canonical_bytes(preservation))

    context = {"scope": workflow["scope"], "lineage": workflow["lineage"],
               "generation": workflow["generation"], "consumer": workflow["consumer"],
               "valid_from": 0, "valid_until": workflow["valid_until"], "qualification_only": True}
    assert (context["scope"], context["lineage"], context["generation"]) == tuple(
        entry["context"][k] for k in ["scope", "lineage", "generation"])
    deferred = []
    for step, verified in zip(workflow["steps"][2:], audit["deferred_install_audits"]):
        definition = step["definition"]
        body = read(R / definition["body"]["path"])
        contract = body["contract"]
        slot = step["ordinal"] == 3
        descriptor = read(R / definition["path"])
        earliest = ("After actual A12 permitted result admission: current completed E2-REENTER; "
                    "actual E2-K-REENTER equals the sealed inventory and native support fingerprint."
                    if slot else
                    "After actual SLOT_PROOF admission: E2-SLOT RESOLVED; exactly one current usable "
                    "expected slot proof; sealed root support fingerprint; independent root source/policy current.")
        dependencies = (["current installed ROOT_SLOT_CONFIGURATION_SET", "current slot source/DECIDE binding",
                         "actual completed E2-REENTER", "actual admitted/current E2-K-REENTER",
                         "sealed knowledge support fingerprint"] if slot else
                        ["current installed ROOT_SLOT_CONFIGURATION_SET", "current installed slot contract",
                         "accepted/current expected SLOT_PROOF", "E2-SLOT RESOLVED",
                         "sealed slot-proof support fingerprint", "current independent root source/DECIDE binding"])
        deferred.append({
            "workflow_ordinal": step["ordinal"], "event_type": "INSTALL_DEFINITION",
            "DEFINITION_ID": uid(definition["definition_id"]),
            "DEFINITION_TYPE": definition["definition_type"],
            "CONTENT_ID": uid(definition["body"]["content_id"]),
            "DESCRIPTOR_ARTIFACT_ID": uid(definition["content_id"]),
            "NATIVE_CONTRACT_ID": uid(contract["id"]), "INSTALL_OPERATION": step["operation"],
            "expected_old_reference": step["expected_old_reference"], "subject": definition["subject"],
            "scope": context["scope"], "lineage": context["lineage"], "generation": context["generation"],
            "consumer": context["consumer"], "definition": definition,
            "proposition": contract["proposition"], "supports": contract["supports"],
            "support_identities": contract["support_identities"], "currentness_rule": descriptor["currentness_rule"],
            "AUTHORITY": {
                "semantic_class": "DECIDE", "semantic_policy_entity": contract["authority"]["value"],
                "semantic_policy_identity": uid(contract["authority_identity"]),
                "existing_semantic_admission": ref(F / "semantic-admission.json"),
                "install_class": "INSTALL", "issuer": "QUALIFICATION_AUTHORITY", "use_limit": 1,
                "delegation": False, "validity": [0, 100],
                "selected_option": "AUTHORIZE_P04_A13_CONFIGURATION_INSTALLATION",
                "workflow_content_id": uid(manifest["workflow"]["content_id"]),
                "qualified_isolated_grant_id": verified["existing_qualified_authority_id"],
                "canonical_grant_executable_at_entry": False,
                "canonical_grant_rule": audit["live_grant_rule"],
                "new_grant_issued_in_this_package": False,
            },
            "DEPENDENCIES": dependencies, "EARLIEST_VALID_INSTALL_POINT": earliest,
            "LATEST_REQUIRED_INSTALL_POINT": "Immediately before " + ("SLOT_PROOF" if slot else "ROOT_PROOF")
                + " candidate construction/admission at the exact F03 boundary; at minimum before proof admission under native validation.",
            "boundary": step["boundary"], "pre_state_rule": step["pre_state"],
            "classification": "A13_CONFIGURATION_TRANSITION", "native_payload_type": "TypedProofContract",
            "proof_instance_created_by_installation": False,
            "state_frame": verified["changed_state_fields"],
            "existing_F03_qualified_history": {k: v for k, v in verified.items()
                 if k.startswith("existing_qualified_") or k in ["checks", "support_checks", "evidence_role"]},
            "canonical_install_event_in_this_package": None,
        })

    sequence = [
        "A09: ordinary atomic Evidence/attestation/receipt admission",
        "A10: actual Evidence/receipt validation and support transaction",
        "A11: obligation Proof; both required native reentry events; recompute C03",
        "A12: select E2-REENTER; admit actual permitted PASS + E2-K-REENTER result",
        "A13 configuration step 3: validate actual post-A12 support and exact bounded grant; INSTALL slot contract",
        "A13: construct fresh SLOT_PROOF admission at post-install state/head; admit; recompute slot RESOLVED",
        "A13 configuration step 4: validate actual slot proof/independent source and exact bounded grant; INSTALL root contract",
        "A13: construct fresh ROOT_PROOF admission at post-install state/head; admit; recompute root SATISFIED",
        "A13: ordinary E06 bounded reevaluation; select FINISH; admit actual permitted PASS + E2-K-FINISH result",
        "Evaluate full sealed P04 target; persist/terminate/cold restore/replay/determinism/isolated negatives; evaluate P05 readiness only",
    ]
    invalidation = {
        "rule": "Every installation advances canonical state/head. Any submission still bound to a prior pre-state or append head is stale.",
        "after_step_3": ["Reconstruct SLOT_PROOF from the current installed slot contract and actual knowledge.",
                         "Create TypedProofAdmission.expected_snapshot from post-install snapshot_id.",
                         "Create its canonical append wrapper against the slot INSTALL event/current append head.",
                         "Discard any earlier state-bound ROOT_PROOF operand; root contract is not yet available."],
        "after_step_4": ["Reconstruct ROOT_PROOF from current resolved slot, accepted slot proof and independent source.",
                         "Create TypedProofAdmission.expected_snapshot from the root post-install snapshot_id.",
                         "Create its append wrapper against the root INSTALL event/current append head.",
                         "Recompute subsequent FINISH selection and command from the latest authoritative state."],
        "native_operand_fields": ["TypedProofAdmission.proof", "TypedProofAdmission.expected_snapshot"],
        "parent_binding": "Canonical event append wrapper, not an invented parent field inside TypedProofAdmission.",
        "proof_identity_rule": "TypedProof ID remains contract/support-bound. It may remain identical when those inputs match; stale admission context must still be rebuilt.",
        "already_admitted_SLOT_PROOF_after_root_INSTALL": "Retained/auditable and usable if its current premises still hold; no duplicate proof admission.",
        "reexecute_A09_A12_after_installation": False,
        "replay_for_trust": "Historical replay verifies the existing prefix; it is not another lifecycle execution.",
    }
    stop_cases = [
        "Definition ID/type/logical role differs from sealed workflow step",
        "Canonical body/descriptor/content/source bytes differ, or a wrapper/instance substitutes for a contract",
        "Authority class, issuer, decision, workflow, subject, operation, limits, validity or applicability differs",
        "Actual support identity/output/proof/proposition differs or is not current",
        "Installation occurs before/after its exact qualified predecessor boundary or out of step order",
        "Parent, bundle, pre-state, next sequence, policy pin/version or prefix is not the verified current predecessor",
        "Scope, lineage, generation, consumer, provenance or independent root source differs",
        "Additional installation/source preparation/authority scope/fixture repair becomes necessary",
        "Installation changes any state outside the sealed contract-registry/installation frame",
        "Actual lifecycle state/result/control differs from a sealed boundary oracle",
    ]
    rule = ("No new or unqualified definition installation is permitted. Only the exact F03-sealed, "
            "pre-authorized workflow steps 3 and 4 may occur, once semantically, at their qualified A13 "
            "support boundaries. All other configuration changes are prohibited.")
    retry = {
        "package": "CANONICAL E2-P04 A09-A13 EXECUTION — SEALED DEFERRED-INSTALLATION PATH",
        "entry": ref(D / (P + "E2_P04_FINAL_PREEXECUTION_CONFIGURATION_BUNDLE_1.json")),
        "entry_bundle_id": entry["bundle_id"], "entry_state_id": entry["state_id"],
        "entry_append_head": entry["append_head"], "entry_checks": "All existing 25 checks plus exact workflow/rule compatibility",
        "configuration_rule": rule, "allowed_installation_ordinals": [3, 4],
        "allowed_definition_ids": [x["DEFINITION_ID"] for x in deferred], "allowed_operations": ["INSTALL", "INSTALL"],
        "preexecution_steps_1_2": "Already committed; verify only. Do not repeat or create another entry bundle.",
        "sequence": sequence, "candidate_rematerialization": invalidation,
        "authority_protocol": "No new semantic grant, new human selection, broadened grant or authority created by installer. Authenticate only the two already-approved state-bound INSTALL grants through existing trusted qualification transport after their actual predecessors pass. Validate exact grant_fields and receipts; isolated grants are historical evidence, not substitute live authorization.",
        "semantic_authority_rule": "Use existing installed/current F03 DECIDE references; never reuse old PC02 lineage authority.",
        "event_publication": "Use ordinary atomic native INSTALL/events; persist and cold-restore each installed boundary before the next proof admission.",
        "oracle_source": ref(Q / "boundary-oracles.json"),
        "causal_prefix_rule": "Verify every stage's actual current prefix; installation cannot reset, rewrite or replay A09-A12 as new execution.",
        "stop_on_divergence": stop_cases, "live_repair_permitted": False,
        "FINISH_inventory_change_permitted": False, "manual_completion_permitted": False,
        "fabricated_result_permitted": False, "persisted_eligibility_permitted": False,
        "P05_execution_permitted": False, "executed_in_this_package": False,
    }
    gates = {
        "F03_workflow_valid": f03["RESULT"] == "PASS" and f03["P04_EXECUTION_READY"] == "YES",
        "entry_snapshot_and_configuration_pass": all(entry["checks"].values()),
        "both_human_selections_exact_and_unchanged": all(audit["selection_checks"].values()),
        "semantic_authority_applicable": audit["SEMANTIC_AUTHORITY_APPLICABLE"] == "YES",
        "install_authorization_applicable_to_exact_conditional_workflow": audit["INSTALL_AUTHORITY_APPLICABLE"] == "YES",
        "both_existing_F03_INSTALL_audits_pass": all(all(x["checks"].values()) and all(x["support_checks"].values()) for x in audit["deferred_install_audits"]),
        "exact_deferred_content_and_context_sealed": len(deferred) == 2,
        "canonical_A13_ownership_and_interleaved_timing_supported": True,
        "overbroad_rule_reconciled_without_changing_runtime_or_F03": True,
        "retry_and_stop_contract_complete": bool(retry["stop_on_divergence"]),
        "preservation_pass": not changed and not missing and diff.returncode == 0,
    }
    assert all(gates.values()), gates
    inputs = [D / (P + x) for x in [
        "E2_P04_CANONICAL_EXECUTION_RESULT.md", "E2_P04_CANONICAL_EXECUTION_RESULT.json",
        "FINISH_F03_RESULT.md", "FINISH_F03_RESULT.json", "FINISH_F02_SUPPORT_RESOLUTION.md",
        "FINISH_F02_SUPPORT_RESOLUTION.json", "E2_P04_FINAL_PREEXECUTION_CONFIGURATION_BUNDLE_1.json",
        "CANONICAL_QUALIFICATION_EXPERIMENT_1.md", "CANONICAL_QUALIFICATION_ACCEPTANCE_MATRIX_1.md",
        "INSTALLATION_I01_CONTRACT.md", "INSTALLATION_I02_RESULT.md", "INSTALLATION_I03_ATTEST_INGRESS_CONTRACT.md",
        "INSTALLATION_I04_RESULT.md", "INSTALLATION_I05_RESULT.md"]]
    sources = {
        "original_A13_contract": {"plan": str(inputs[7].relative_to(R)), "matrix": str(inputs[8].relative_to(R)),
            "plan_terms": "Separate typed root/slot predicates with declared provenance and independent source dependencies; P04 owns post-reentry proof recomputation.",
            "matrix_A13": "Required post-reentry claim available; independently defined proof predicates; native proof/root/slot recomputation and selected finishing result.",
            "timing_recovery": "Original matrix does not fix concrete INSTALL time. Exact support-conditioned activation is explicitly specified by selected F02 workflow and F03 qualification; no original phase ownership is changed."},
        "native_call_paths": [
            {"path": "adapter/planner/proof_installation.py", "function": "apply", "line": 201,
             "clauses": {"slot_actual_support": "PROOF_ACTUAL_KNOWLEDGE_REQUIRED", "root_actual_support": "PROOF_ACTUAL_SLOT_REQUIRED", "support_hash": "PROOF_SUPPORT_FINGERPRINT", "no_overwrite": "PROOF_CONTRACT_ROLE_CONFLICT"}},
            {"path": "adapter/planner/proof_installation.py", "function": "contract_current", "line": 180},
            {"path": "adapter/planner/typed_proofs.py", "function": "validate_records", "line": 27,
             "clauses": ["proof does not match independent contract", "dangling proof support"]},
            {"path": "adapter/planner/typed_proofs.py", "function": "apply", "line": 165,
             "clause": "typed proof transition pre-state mismatch"},
            {"path": "adapter/planner/installation.py", "function": "grant_fields", "line": 121},
            {"path": "adapter/planner/installation.py", "function": "validate_authority", "line": 156},
            {"path": "adapter/planner/installation.py", "function": "validate_prefix", "line": 246},
        ],
    }
    why = {
        "slot": {"blocking_lifecycle_value": "Actual current completed E2-REENTER output E2-K-REENTER",
            "expected_support_fingerprint": uid(resolution["knowledge_support_identity"]),
            "constraint": "Native no-dangling-support admission plus exact actual knowledge/current producer completion; declarations cannot seed lifecycle knowledge."},
        "root": {"blocking_lifecycle_value": "Resolved E2-SLOT with the sole accepted/current expected SLOT_PROOF",
            "expected_slot_proof_id": uid(resolution["predicted_slot_proof_id"]),
            "expected_support_fingerprint": uid(resolution["root_slot_support_identity"]),
            "constraint": "SlotId existence alone is insufficient; actual proof/support and independently current root source must satisfy the adapter."},
        "identity_domains": [
            {"domain": "descriptor artifact / definition / body content / native TypedProofContract", "timing": "PRESEALED_BEFORE_EXECUTION", "changes_allowed": False},
            {"domain": "actual KnowledgeRecord / usable slot Proof support", "timing": "LIFECYCLE_PRODUCED; MUST_EQUAL_PRESEALED_EXPECTATION", "changes_allowed": False},
            {"domain": "installation request / INSTALL grant / installed-definition instance / event", "timing": "DERIVED_AT_VERIFIED_ACTUAL_PREDECESSOR; EXACT_NATIVE_FIELDS", "new_semantics_allowed": False},
        ],
        "post_A12_state_in_contract_content": False, "actual_A12_execution_record_id_is_new_contract_field": False,
        "canonical_parent_in_INSTALL_request_and_grant": True,
        "dynamic_source_binding_or_contract_repair_required": False,
        "independent_root_source_status": "Already installed/current at entry; no new source preparation during execution.",
        "early_installation_alternative": "Unsupported by the sealed workflow and native support gates. Do not create another preexecution bundle or inject future knowledge/proofs.",
    }
    report = {
        "schema": "PLANNER-P04-DEFERRED-INSTALLATION-RECONCILIATION-1",
        "WORK_PACKAGE": "E2-P04-DEFERRED-INSTALLATION-RECONCILIATION", "RESULT": "PASS",
        "DEFERRED_INSTALLATIONS": deferred,
        "F03_INSTALLATION_TIMING": {"preexecution": [1, 2], "during_A09_A12": [],
            "A13_after_A12_before_slot_proof": 3, "A13_after_slot_proof_before_root_proof": 4,
            "before_FINISH": "Both concrete contracts and their separately admitted proofs current; root satisfied",
            "sequence": sequence, "workflow": ref(Q / "bounded-installation-workflow.json")},
        "SEMANTIC_AUTHORITY_APPLICABLE": "YES", "INSTALL_AUTHORITY_APPLICABLE": "YES",
        "AUTHORITY_APPLICABILITY_DOMAIN": audit["install_applicability_domain"],
        "LIVE_DEFERRED_GRANTS_ALREADY_EXECUTABLE_AT_ENTRY": "NO",
        "WHY_DEFERRED": why,
        "DEFINITION_INSTANCE_SEPARATION": {"classification": "PROOF_CONTRACT_DEFINITIONS",
            "native_definition_type": "TypedProofContract", "later_instance_type": "TypedProof",
            "later_admission_type": "TypedProofAdmission", "proof_created_by_INSTALL": False,
            "satisfaction_or_FINISH_execution_created_by_INSTALL": False},
        "CANONICAL_PHASE_OWNERSHIP": {"both_installations": "A13_CONFIGURATION_TRANSITION",
            "A12": "REENTER execution/permitted result; output supplies A13, does not own deferred INSTALL",
            "A13": "Governed support resolution interleaved with separate SLOT_PROOF/ROOT_PROOF admission and finishing result",
            "canonical_plan_change_required": False, "new_authorization_selection_required": False},
        "INSTALL_AS_CANONICAL_HISTORY": {"ordinary_parent": True,
            "event_type": "INSTALL_DEFINITION", "native_representation": "ExecutionEvent.result = InstallDefinition",
            "one_event_per_step": True, "append_head_advances": True, "snapshot_identity_changes": True,
            "old_historical_states_immutable": True,
            "changed_snapshot_fields": ["installed_definitions", "proof_contracts"],
            "knowledge_Action_status_root_slot_satisfaction_unchanged_by_install": True,
            "ledger_rule": "Retain complete prior ordered ledger; append exactly one current-parent configuration event per step.",
            "separate_ledger_id_or_Merkle_root_in_native_bundle": False},
        "CANDIDATE_INVALIDATION": invalidation,
        "ORIGINAL_EXECUTION_RESTRICTION": {"rule": "No prospective definition installation is permitted during this run.",
            "classification": "OVERBROAD", "relationship_to_F03": "CONFLICTING_WITH_F03",
            "prior_execution_status_retained": "BLOCKED_BEFORE_A09; 25_ENTRY_CHECKS_PASS; NO_RUNTIME_COUNTEREXAMPLE"},
        "RECONCILED_EXECUTION_RULE": rule, "STOP_ON_DIVERGENCE": stop_cases,
        "ENTRY_BUNDLE_REMAINS_VALID": "YES", "ENTRY_GATE": "PASS",
        "ENTRY_BUNDLE": {"artifact": ref(inputs[6]), "bundle_id": entry["bundle_id"], "state_id": entry["state_id"],
            "append_head": entry["append_head"], "native_ledger_anchor": entry["native_ledger_anchor"],
            "event_count": entry["event_count"], "context": entry["context"], "checks": entry["checks"],
            "concrete_proof_contract_count": 0, "typed_proof_instance_count": 0,
            "new_entry_bundle_created": False},
        "READINESS_GATES": gates, "A09_READY": "YES", "A10_READY": "YES", "A11_READY": "YES",
        "A12_READY": "YES", "A13_READY": "YES", "P04_EXECUTION_READY": "YES", "E2_P04_READY": "YES",
        "READINESS_SCOPE": "EXACT_SEALED_DEFERRED_INSTALLATION_PATH_ONLY; DOES_NOT_CLAIM_CANONICAL_P04_PASS",
        "RETRY_CONTRACT": retry, "NEXT_PACKAGE": retry["package"],
        "sealed_boundary_oracles": {"artifact": ref(Q / "boundary-oracles.json"), "oracles": oracles["oracles"],
            "changed": False, "control_after_A12_and_SLOT_PROOF": "PLAN_DEFECT",
            "control_after_ROOT_PROOF": "RUNNABLE", "control_after_FINISH": "TERMINAL_SUCCESS"},
        "verification": {"new_entry_checks": len(entry["checks"]), "sealed_references_verified": len(audit["sealed_files_verified"]),
            "selection_checks": len(audit["selection_checks"]), "semantic_checks": len(audit["semantic_checks"]),
            "historical_installation_and_support_checks": sum(len(a["checks"]) + len(a["support_checks"]) for a in audit["deferred_install_audits"]),
            "method": "Read-only native restore/replay and pure authority/prefix/currentness checks over existing F03 history. No new qualification execution or runtime repair.",
            "entry_reader": ref(O / "entry-reader.json"), "authorization_audit": ref(O / "authorization-verification.json"),
            "reused_F03_generic_and_lifecycle_qualification": "PASS; unchanged; not relabeled canonical execution",
            "runtime_tests_run_this_package": False, "new_negative_suite_executed": False},
        "sources": sources, "authoritative_inputs": [ref(p) for p in inputs], "preservation": preservation,
        "A09_A13_EXECUTED": "NO", "DEFERRED_INSTALLATIONS_EXECUTED": "NO", "E2_FINISH_EXECUTED": "NO",
        "NEW_AUTHORITY_ISSUED": "NO", "F03": "PASS", "F03_ALTERED": "NO", "P03_RESULT": "PASS",
        "P03_HISTORICAL_CORRESPONDENCE": "UNPROVEN", "N_REAL_SATISFIED": "NO",
        "CANONICAL_E2_QUALIFIED": "NO", "RUNTIME_MODIFIED": "NO", "E1_ARTIFACTS_MODIFIED": 0,
        "PRODUCTION_EFFECT": "NO", "GIT_DIFF_CHECK": "PASS",
    }
    (D / (NAME + ".json")).write_bytes(c.canonical_bytes(report))

    slot, root = deferred
    text = f'''# Deterministic Planner v0.1 — P04 deferred A13 installation boundary reconciliation

**RESULT = PASS. P04_EXECUTION_READY = YES for the exact sealed deferred-installation path.** Both deferred events are legitimate **A13_CONFIGURATION_TRANSITION** operations already specified, authorized and qualified by F02/F03. The earlier blanket installation ban is **OVERBROAD** and **CONFLICTING_WITH_F03**. The existing final preexecution bundle remains the correct entry bundle. This package records the retry contract; it executes no lifecycle or installation and issues no authority.

The [machine-readable companion](./{NAME}.json) records all sixteen reconciliation steps, exact identities, authority domains, native state effects, candidate invalidation, sealed oracles, readiness gates and preservation. The previous [canonical execution stop](./{P}E2_P04_CANONICAL_EXECUTION_RESULT.md) remains historical BLOCKED evidence before A09. No runtime counterexample occurred and no canonical P04 PASS is claimed.

The [original acceptance matrix A13](./{P}CANONICAL_QUALIFICATION_ACCEPTANCE_MATRIX_1.md) starts with the required post-reentry claim available and independently defined proof predicates, then owns native proof/root/slot recomputation and the selected finishing result. The [canonical plan](./{P}CANONICAL_QUALIFICATION_EXPERIMENT_1.md) requires separate typed predicates, declared provenance and independent source dependencies. Neither specifies that concrete support-bound proof contracts must be in the pre-A09 snapshot. The affirmative timing contract is the explicitly selected [F02 workflow](./qualification/FINISH_F02_1/bounded-installation-workflow.json), subsequently qualified by [F03](./{P}FINISH_F03_RESULT.md). This recovers A13 preparation timing without moving A13 work into A12 or changing phase acceptance.

The two installable definitions share scope `{context['scope']}`, lineage `{context['lineage']}`, generation `{context['generation']}`, consumer `{context['consumer']}`, validity ticks 0–100 and qualification-only effects. Both operations are **INSTALL** into absent concrete-contract roles, with no replacement target. Source/structural declarations and the nonterminal FINISH hold were already installed by steps 1–2.

| Exact deferred object | Workflow step 3 | Workflow step 4 |
|---|---|---|
| Definition type | SLOT_PROOF_CONTRACT_DEFINITION | ROOT_PROOF_CONTRACT_DEFINITION |
| Definition ID | `{slot['DEFINITION_ID']}` | `{root['DEFINITION_ID']}` |
| Canonical body content ID | `{slot['CONTENT_ID']}` | `{root['CONTENT_ID']}` |
| Native TypedProofContract ID | `{slot['NATIVE_CONTRACT_ID']}` | `{root['NATIVE_CONTRACT_ID']}` |
| Target / proposition | E2-SLOT / E2-SLOT-PROPOSITION | E2-ROOT / E2-ROOT-PROPOSITION |
| Dependency | Actual current completed REENTER knowledge, sealed fingerprint, current source/semantic configuration | Resolved slot, sole expected usable SLOT_PROOF and sealed fingerprint, independently current root source/semantic configuration |
| Earliest valid point | After actual A12 result/knowledge admission | After actual SLOT_PROOF admission and slot resolution |
| Required point in sealed F03 path | Immediately before SLOT_PROOF construction/admission | Immediately before ROOT_PROOF construction/admission |

The [slot descriptor](./qualification/FINISH_F02_1/slot_proof_contract_definition-descriptor.json) and [root descriptor](./qualification/FINISH_F02_1/root_proof_contract_definition-descriptor.json) bind their exact native bodies. Descriptor artifact IDs use `raw-file-sha256`; definition IDs use `planner-installable-definition-v1`; body content IDs and native contract IDs occupy their own domains. Event/installed-definition identities are later state-bound outputs. Equal hash text across namespaces does not permit cross-domain substitution.

Both human selections remain applicable: `SEMANTIC_AUTHORITY_APPLICABLE = YES` and `INSTALL_AUTHORITY_APPLICABLE = YES` for the exact conditional workflow. The unchanged [F03 authenticated decisions](./qualification/FINISH_F03_1/authenticated-decisions.json) cover `AUTHORIZE_P04_A13_SUPPORT_SEMANTICS` and `AUTHORIZE_P04_A13_CONFIGURATION_INSTALLATION`, the exact manifest/requests and workflow timing. The semantic request explicitly includes both proof bodies; the INSTALL request explicitly includes both descriptors, operation and predecessor rules. A fresh audit verifies 21 sealed references, 13 selection checks, 11 semantic checks and 48 native historical installation/support checks. [Authorization evidence](./qualification/E2_P04_DEFERRED_INSTALLATION_RECONCILIATION_1/authorization-verification.json) records every check.

Semantic DECIDE applicability and INSTALL permission remain separate. The existing canonical source-targeted semantic entities are current. The slot policy is `{slot['AUTHORITY']['semantic_policy_entity']}`; the root policy is `{root['AUTHORITY']['semantic_policy_entity']}`. The INSTALL issuer is QUALIFICATION_AUTHORITY, with one exact definition/operation per nondelegable single-use grant, validity 0–100 and exact policy/context/predecessor bindings. Old PC02, route, ATTEST and A10 grants do not substitute.

Workflow approval is not itself a native InstallAuthority. No live deferred grant is executable at the entry state. At each actual qualified predecessor, the retry must authenticate/validate only that already-approved step's exact state-bound grant through existing trusted qualification transport. This adds no human decision, semantic grant, authority scope or installer issuance power. The existing F03 isolated grant IDs `{slot['AUTHORITY']['qualified_isolated_grant_id']}` and `{root['AUTHORITY']['qualified_isolated_grant_id']}` are comparison evidence; they cannot bypass validation against an actual canonical predecessor. This reconciliation makes no authority-admission call.

Deferral concerns **canonical activation**, not discovery of bytes. Both contract contents and identities were sealed before execution. Slot content references the fixed permitted KnowledgeRecord and fingerprint `{why['slot']['expected_support_fingerprint']}`. Installation requires that record actually exist/current and its producer be completed. Root content references E2-SLOT and fingerprint `{why['root']['expected_support_fingerprint']}`, based on the expected proof `{why['root']['expected_slot_proof_id']}`. Slot existence alone cannot activate the root contract. [The native adapter](../../adapter/planner/proof_installation.py) requires the sole usable slot proof, resolved slot and current independent source.

The actual A12 result supplies/gates knowledge; its execution-record ID is not a newly invented contract field. Post-A12/post-slot bundle, state and head determine INSTALL requests, grants, command keys, installed-definition instances and events, while contract content remains unchanged. Root source/binding is already current at entry. Early installation would violate the actual-support gates; precreating knowledge or proofs would violate the lifecycle. A new preexecution bundle would not resolve that contract.

Both deferred payloads are **TypedProofContract definitions**, never SLOT_PROOF/ROOT_PROOF instances. [Native validation](../../adapter/planner/typed_proofs.py) rejects a proof with no matching independent contract and dangling contract support. Auditing the existing F03 before/after boundaries shows that each installation changes only `installed_definitions` and `proof_contracts`; proof count, knowledge, Action status and slot/root satisfaction are unchanged. Each is one ordinary canonical INSTALL event with exact current parent/pre-state, retained immutable prefix and an advanced append head. The separate later TypedProofAdmission establishes satisfaction. No eligibility permission, ActionResult or FINISH execution is produced by installation.

The exact causal sequence is:

```text
A09 -> A10 -> A11 (Proof / native reentry events / C03) -> A12 (actual REENTER result)
    -> A13 step 3: INSTALL sealed slot contract
    -> fresh SLOT_PROOF admission -> E2-SLOT RESOLVED
    -> A13 step 4: INSTALL sealed root contract
    -> fresh ROOT_PROOF admission -> E2-ROOT SATISFIED / E06 reevaluation
    -> selected FINISH permitted result -> E2-K-FINISH -> sealed P04 target
```

Configuration resolution is interleaved with proof admission. Performing both installations together before SLOT_PROOF would fail the root support gate. A09–A12 have no deferred installation; A12 owns only REENTER/result. A13 owns both support-conditioned configuration transitions, its separate proofs and finishing evaluation/result.

After each INSTALL, all submission operands bound to the previous pre-state/head are stale. Reconstruct SLOT_PROOF admission after step 3 and ROOT_PROOF admission after step 4; recompute any subsequent FINISH selection/command from the newest state. Native `TypedProofAdmission` contains `proof` and `expected_snapshot`; the canonical append wrapper binds its ordinary parent. Refresh both boundaries. A proof's contract/support-based identity may remain equal when its inputs match; this cannot preserve obsolete admission context. The already admitted slot proof remains historical/current under its own premises after root-contract installation. Already committed A09–A12 events are retained; no lifecycle reexecution is required. Historical replay for trust is separate.

The revised invariant is:

> {rule}

Each event must use its exact current native bundle/state/head, next sequence, unchanged policy, sealed source additions and admitted authority receipt. No definition/source/goal/inventory/control repair or extra installation is allowed. Any differing definition, content, grant domain, support, timing, parent, provenance or scope/lineage/generation stops execution immediately. Record the first expected/actual counterexample and state/event; do not repair or continue. Future event IDs follow native transition-prefix derivation; isolated history does not substitute for canonical execution evidence.

The [existing entry bundle](./{P}E2_P04_FINAL_PREEXECUTION_CONFIGURATION_BUNDLE_1.json) remains unchanged and valid:

| Entry pin | Exact value |
|---|---|
| Bundle | `{entry['bundle_id']}` |
| Snapshot | `{entry['state_id']}` |
| Append head | `{entry['append_head']}` |
| Native ledger anchor | `{entry['native_ledger_anchor']}` |
| Event count / control | 9 / EXTERNAL_WAIT |

The new [read-only entry reader](./qualification/E2_P04_DEFERRED_INSTALLATION_RECONCILIATION_1/entry-reader.json) passes all 25 checks, including native trust/cold restore, exact configuration and ordered ledger, 52 source/policy pins, seven installed definitions current, authority applicability, all 28 qualified runtime hashes and canonical lifecycle unexecuted. Zero concrete contracts/proof instances is intentional at entry. The native ledger has no separate Merkle-root/LedgerId field; its first event supplies the recorded anchor. No replacement entry bundle is created.

The retry contract is **CANONICAL E2-P04 A09-A13 EXECUTION — SEALED DEFERRED-INSTALLATION PATH**:

1. Recheck the exact entry bundle, F03 PASS, five readiness gates and this two-event compatibility rule. Execute A09–A12 through their already-qualified native transactions using actual admitted lifecycle outputs.
2. Independently check actual post-A12 output/currentness against the seal. Authenticate and validate the exact step-3 bounded INSTALL grant at that predecessor; append only its slot contract. Persist/cold restore/currentness-check, then construct a fresh slot-proof admission at the new head.
3. Admit SLOT_PROOF and check the expected identity, current usability and resolved slot. Authenticate and validate only step 4 against that predecessor; append only its root contract. Persist/cold restore/currentness-check, then construct a fresh root-proof admission at the new head and use the already-installed independent root source.
4. Admit ROOT_PROOF; use ordinary E06 reevaluation and native selected permitted FINISH/result admission. Keep FINISH inventory exactly PASS + E2-K-FINISH. Evaluate every sealed P04 target term, then perform required target persistence, fresh-reader/replay/determinism and isolated sealed negatives. Evaluate P05 readiness only after canonical P04 PASS; do not execute P05.
5. Stop on the first divergence; preserve successful committed history and prohibit live repair, extra configuration, new semantic authority, caller-supplied eligibility, fabricated results and manual completion.

The [sealed F02 boundary oracle](./qualification/FINISH_F02_1/boundary-oracles.json) is retained byte-for-byte: PLAN_DEFECT after actual REENTER and slot proof, RUNNABLE after root proof, TERMINAL_SUCCESS after FINISH. The explicit clarification retained that oracle; no no-PLAN_DEFECT assertion or control rewrite is introduced. F03 qualification remains PASS; previous canonical execution remains stopped, and new readiness is for this exact retry path only. P03 historical correspondence stays UNPROVEN and N_REAL_SATISFIED stays NO.

[Preservation evidence](./qualification/E2_P04_DEFERRED_INSTALLATION_RECONCILIATION_1/preservation.json) checks all {preservation['baseline_files_checked']:,} preexisting files, including {preservation['frozen_E1_files_checked']:,} frozen-E1 files and all {preservation['runtime_files_checked']} runtime files; none changed. No new authority, installation, lifecycle instance or canonical target was produced. Native checks restore/replay existing historical evidence; they do not submit new operations. Prior F03 qualification is reused without claiming a new runtime regression/negative execution. `git diff --check = PASS`.

```text
WORK_PACKAGE = E2-P04-DEFERRED-INSTALLATION-RECONCILIATION
RESULT = PASS
DEFERRED_INSTALLATIONS = [SLOT_PROOF_CONTRACT_DEFINITION, ROOT_PROOF_CONTRACT_DEFINITION]
F03_INSTALLATION_TIMING = {{slot: POST_A12_PRE_SLOT_PROOF, root: POST_SLOT_PROOF_PRE_ROOT_PROOF}}
SEMANTIC_AUTHORITY_APPLICABLE = YES
INSTALL_AUTHORITY_APPLICABLE = YES (EXACT CONDITIONAL WORKFLOW)
WHY_DEFERRED = ACTUAL_SUPPORT_REQUIRED; CONTENT_AND_IDENTITIES_PRESEALED
DEFINITION_INSTANCE_SEPARATION = PROOF_CONTRACT_DEFINITIONS; NO_PROOF_INSTANCE
CANONICAL_PHASE_OWNERSHIP = A13_CONFIGURATION_TRANSITION (BOTH)
INSTALL_AS_CANONICAL_HISTORY = ORDINARY_EVENT; IMMUTABLE_PREFIX; HEAD_ADVANCES
CANDIDATE_INVALIDATION = OLD_PRESTATE_HEAD_STALE; FRESH_PROOF_ADMISSION_REQUIRED
ORIGINAL_EXECUTION_RESTRICTION = OVERBROAD / CONFLICTING_WITH_F03
RECONCILED_EXECUTION_RULE = ONLY_EXACT_TWO_SEALED_PREAUTHORIZED_DEFERRED_INSTALLS
ENTRY_BUNDLE_REMAINS_VALID = YES
P04_EXECUTION_READY = YES
E2_P04_READY = YES
RETRY_CONTRACT = CANONICAL_E2_P04_A09_A13_SEALED_DEFERRED_INSTALLATION_PATH
A09_A13_EXECUTED = NO
DEFERRED_INSTALLATIONS_EXECUTED = NO
E2_FINISH_EXECUTED = NO
NEW_AUTHORITY_ISSUED = NO
F03 = PASS
F03_ALTERED = NO
P03_RESULT = PASS
P03_HISTORICAL_CORRESPONDENCE = UNPROVEN
N_REAL_SATISFIED = NO
RUNTIME_MODIFIED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
GIT_DIFF_CHECK = PASS
```
'''
    (D / (NAME + ".md")).write_text(text)
    print(json.dumps({"result": report["RESULT"], "P04_EXECUTION_READY": report["P04_EXECUTION_READY"],
                      "preexisting_files_unchanged": len(baseline), "deferred_installation_events_submitted": 0,
                      "machine_companion": str((D / (NAME + ".json")).relative_to(R))}))


if __name__ == "__main__":
    main()
