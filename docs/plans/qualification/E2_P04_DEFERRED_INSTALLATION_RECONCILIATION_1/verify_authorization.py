"""Audit sealed decisions and existing qualified history; submit no operation."""
import hashlib
import json
import os
from pathlib import Path

from adapter.planner import codec as c, gates, installation as i, model as m
from adapter.planner import proof_installation as pi, typed_proofs as tp

R = Path(__file__).resolve().parents[4]
D = R / "docs/plans"
Q = D / "qualification/FINISH_F02_1"
F = D / "qualification/FINISH_F03_1"
O = Path(__file__).resolve().parent
P = "DETERMINISTIC_PLANNER_V0_1_"


def read(path):
    return c.parse_json(path.read_bytes())


def uid(value):
    return value.namespace + ":" + value.sha256


def main():
    decisions_path = F / "authenticated-decisions.json"
    decisions = read(decisions_path)
    decision_id = c._identity(decisions_path.read_bytes(), "raw-file-sha256")
    manifest = read(Q / "sealed-manifest.json")
    workflow = read(Q / "bounded-installation-workflow.json")
    resolution = read(Q / "support-resolution-contract.json")
    semantic_request = read(Q / "semantic-authority-request.json")
    install_request = read(Q / "install-authority-request.json")
    f03 = read(D / (P + "FINISH_F03_RESULT.json"))
    seals = {}

    def verify_refs(value):
        if isinstance(value, dict):
            if "path" in value and "content_id" in value:
                pin = value["content_id"]
                assert pin["namespace"] == "raw-file-sha256"
                path = R / value["path"]
                actual = hashlib.sha256(path.read_bytes()).hexdigest()
                assert actual == pin["sha256"], str(path)
                seals[str(path.relative_to(R))] = actual
            for nested in value.values():
                verify_refs(nested)
        elif isinstance(value, list):
            for nested in value:
                verify_refs(nested)

    for subject in decisions["sealed_subjects"].values():
        assert hashlib.sha256((R / subject["path"]).read_bytes()).hexdigest() == subject["sha256"]
        seals[subject["path"]] = subject["sha256"]
    for value in (manifest, workflow, semantic_request, install_request):
        verify_refs(value)
    selected_checks = {
        "explicit_selected_semantic_option": decisions["selected_semantic_option"] == "AUTHORIZE_P04_A13_SUPPORT_SEMANTICS",
        "explicit_selected_install_option": decisions["selected_install_option"] == "AUTHORIZE_P04_A13_CONFIGURATION_INSTALLATION",
        "semantic_request_exact_selection": semantic_request["required_selection"] == decisions["selected_semantic_option"],
        "install_request_exact_selection": install_request["required_selection"] == decisions["selected_install_option"],
        "sealed_terms_unchanged": decisions["material_sealed_terms_changed"] is False,
        "human_transport_and_role": decisions["authentication"] == "EXPLICIT_CURRENT_SESSION_HUMAN_DECISION_TRANSPORT" and decisions["role"] == "QUALIFICATION_AUTHORITY",
        "qualification_only": decisions["qualification_only"] is True,
        "no_lifecycle_permission_in_INSTALL_decision": decisions["permits_canonical_lifecycle_execution"] is False,
        "F03_PASS": f03["RESULT"] == "PASS",
        "F03_ready_under_exact_workflow": f03["P04_EXECUTION_READY"] == "YES",
        "no_control_oracle_change": decisions["scope_conflict"]["clarification"] == "retain that sealed oracle and qualify the remaining path",
        "workflow_timing_covered_by_selected_request": install_request["workflow"] == manifest["workflow"],
        "workflow_permission_is_not_native_grant": install_request["approval_is_not_native_grant"] is True,
    }
    assert all(selected_checks.values()), selected_checks
    bundle = c.restore(D / (P + "E2_P04_FINAL_PREEXECUTION_CONFIGURATION_BUNDLE_1.json"),
                       c._unwire(f03["configuration_bundle"]["bundle_id"]), R)
    state = bundle.current
    config = pi.records(state, "ROOT_SLOT_CONFIGURATION_SET")
    assert len(config) == 1
    config = config[0]
    descriptor, body, files, slot, root, entities, declarations = pi.configuration(config.request)
    semantic_binding = config.request.authority_bindings[0]
    grant = read(F / "semantic-admission.json")["grant"]
    semantic_checks = {
        "existing_config_current": i.current(bundle, config),
        "existing_semantic_binding_matches_F03": c.parse_json(semantic_binding.issued_authorization_json.encode()) == grant,
        "trusted_decision_exact": grant["decision_id"] == i.simple(decision_id),
        "semantic_request_exact": grant["semantic_request_id"] == manifest["semantic_authority_request"]["content_id"],
        "semantic_binding_class_distinct_from_INSTALL": semantic_binding.authority_class is m.AuthorityClass.DECIDE,
        "installed_source_policy_entities_exact_current": all(e in state.entities and gates.usable(e, state).state is m.ProofState.PROVED for e in entities),
        "scope_lineage_generation_exact": (state.context.scope, state.context.lineage, state.context.generation) == (descriptor["scope"], descriptor["lineage"], descriptor["generation"]),
        "semantic_validity_current": grant["valid_from"] <= state.context.tick <= grant["valid_until"],
        "semantic_subjects_include_both_deferred_contracts": all(x["definition"]["body"] in semantic_request["definition_subjects"] for x in workflow["steps"][2:]),
        "no_automatic_semantic_issuance": grant["automatic_issuance_by_install"] is False,
        "concrete_contracts_intentionally_absent": not state.proof_contracts and not state.typed_proofs,
    }
    assert all(semantic_checks.values()), semantic_checks
    checkpoints = read(F / "isolated-checkpoints.json")
    audits = []
    for index, before_name, after_name in [(2, "post-a12", "slot-contract"), (3, "post-slot-proof", "root-contract")]:
        step = workflow["steps"][index]
        request = c._unwire(read(F / ("install-request-" + str(index) + ".json")))
        authority_receipt = read(F / ("install-authority-" + str(index) + ".json"))
        before = c.restore(Path(checkpoints[before_name]["path"]), c._unwire(checkpoints[before_name]["bundle_id"]), R)
        after = c.restore(Path(checkpoints[after_name]["path"]), c._unwire(checkpoints[after_name]["bundle_id"]), R)
        definition_descriptor, native_body = pi.descriptor(request.definition)
        native_contract = c._unwire(native_body["contract"])
        authority_grant = c.parse_json(request.authority.grant_json.encode())
        i.validate_authority(request, before.current.context)
        i.validate_prefix(before, request)
        event = after.events[-1]
        definition = step["definition"]
        checks = {
            "INSTALL_exact_operation": request.operation is m.InstallationOperation.INSTALL and step["operation"] == "INSTALL",
            "definition_id_sealed": i.simple(request.definition.id) == definition["definition_id"],
            "definition_type_sealed": definition_descriptor["definition_type"] == definition["definition_type"],
            "content_id_sealed": definition_descriptor["content_id"] == definition["body"]["content_id"],
            "native_contract_sealed_and_declared": native_contract in declarations and native_contract.id == tp.identity(native_contract),
            "definition_is_contract_not_instance": type(native_contract) is m.TypedProofContract,
            "install_request_contains_exact_step_definition": definition in install_request["definition_subjects"],
            "trusted_decision_exact": authority_grant["decision_id"] == i.simple(decision_id),
            "sealed_workflow_contract_exact": authority_grant["contract_id"] == manifest["workflow"]["content_id"],
            "issuer_class_limit_separate": authority_grant["issuer"] == "QUALIFICATION_AUTHORITY" and authority_grant["authority_class"] == "INSTALL" and authority_grant["use_limit"] == 1 and authority_grant["delegation"] is False,
            "accepted_authority_receipt_exact": c.parse_json(request.authority.admission_provenance.excerpt.encode()) == authority_receipt,
            "native_authority_validation": True,
            "native_prefix_validation": True,
            "ordinary_parent_current": request.expected_parent_event == before.events[-1].identity and event.parent_event == before.events[-1].identity,
            "event_operand_exact": event.result == request,
            "post_contract_present_current": native_contract in after.current.proof_contracts and pi.contract_current(after.current, native_contract),
            "proof_count_unchanged_by_install": len(before.current.typed_proofs) == len(after.current.typed_proofs),
            "one_historical_configuration_event": len(after.events) == len(before.events) + 1,
            "prestate_immutable_historical_prefix": c._bundle_bytes_admitted(c._prefix_bundle(after, len(before.events))) == Path(checkpoints[before_name]["path"]).read_bytes(),
        }
        before_wire, after_wire = c._wire(before.current), c._wire(after.current)
        changed_fields = sorted(k for k in set(before_wire) | set(after_wire) if before_wire.get(k) != after_wire.get(k))
        checks["only_contract_registry_and_install_witness_changed"] = changed_fields == ["installed_definitions", "proof_contracts"]
        if index == 2:
            knowledge = next(k for k in before.current.knowledge if k.id == native_contract.supports[0])
            support_checks = {
                "actual_knowledge_equals_sealed_inventory": c._wire(knowledge) == resolution["knowledge_output"],
                "actual_REENTER_current_completion": gates.current_completion(before.current, m.ActionId("E2-REENTER")),
                "support_fingerprint_sealed": i.simple(tp.support_identity(before.current, knowledge.id)) == resolution["knowledge_support_identity"],
                "contract_references_actual_knowledge": native_contract.supports == (knowledge.id,),
            }
        else:
            proofs = [p for p in before.current.typed_proofs if p.target == native_contract.supports[0] and tp.usable(before.current, p)]
            support_checks = {
                "exactly_one_usable_expected_slot_proof": len(proofs) == 1 and i.simple(proofs[0].id) == resolution["predicted_slot_proof_id"],
                "slot_RESOLVED": any(s.id == native_contract.supports[0] and s.state is m.SlotState.RESOLVED for s in before.current.slots),
                "support_fingerprint_sealed": i.simple(tp.support_identity(before.current, native_contract.supports[0])) == resolution["root_slot_support_identity"],
                "independent_source_and_semantic_configuration_current": pi.support_current(before.current, pi.records(before.current, "ROOT_SLOT_CONFIGURATION_SET")[0]),
            }
        assert all(checks.values()), {k: v for k, v in checks.items() if not v}
        assert all(support_checks.values()), support_checks
        audits.append({
            "workflow_ordinal": index + 1, "boundary": step["boundary"], "definition": definition,
            "native_contract_id": uid(native_contract.id), "checks": checks, "support_checks": support_checks,
            "changed_state_fields": changed_fields,
            "existing_qualified_authority_id": uid(request.authority.id),
            "existing_qualified_event_id": uid(event.identity),
            "existing_qualified_pre_state": uid(c.snapshot_id(before.current)),
            "existing_qualified_post_state": uid(c.snapshot_id(after.current)),
            "existing_qualified_parent": uid(before.events[-1].identity),
            "existing_qualified_post_head": uid(after.events[-1].identity),
            "native_grant_currently_executable_at_entry": False,
            "evidence_role": "AUDIT_OF_EXISTING_F03_ISOLATED_HISTORY; NO_NEW_AUTHORITY_OR_INSTALLATION",
        })
    result = {
        "schema": "PLANNER-P04-DEFERRED-INSTALLATION-AUTHORIZATION-AUDIT-1", "result": "PASS",
        "reader_pid": os.getpid(), "pid_namespace": os.readlink("/proc/self/ns/pid"),
        "decision_id": uid(decision_id), "sealed_files_verified": seals,
        "selection_checks": selected_checks, "semantic_checks": semantic_checks,
        "deferred_install_audits": audits,
        "SEMANTIC_AUTHORITY_APPLICABLE": "YES", "INSTALL_AUTHORITY_APPLICABLE": "YES",
        "install_applicability_domain": "PREAUTHORIZED_EXACT_WORKFLOW; CURRENT_NATIVE_GRANTS_VALIDATED_ON_THEIR_EXISTING_QUALIFIED_PREDECESSORS",
        "live_deferred_canonical_grants_issued_now": False,
        "live_grant_rule": "Fresh PLANNER-INSTALL-GRANT-1 must be authenticated under the already-selected exact workflow against each actual verified canonical predecessor. Prior isolated grant instances are not substitutes for that validation.",
        "new_authority_admission_calls": 0, "new_install_or_lifecycle_submission_calls": 0,
        "entry_bundle_id": uid(c._unwire(f03["configuration_bundle"]["bundle_id"])),
        "entry_state_id": uid(c.snapshot_id(state)), "entry_append_head": uid(bundle.events[-1].identity),
    }
    (O / "authorization-verification.json").write_bytes(c.canonical_bytes(result))
    print(json.dumps({"result": "PASS", "sealed_files": len(seals), "selection_checks": len(selected_checks),
                      "semantic_checks": len(semantic_checks), "qualified_installation_audits": len(audits),
                      "new_authority_or_event_submissions": 0}))


if __name__ == "__main__":
    main()
