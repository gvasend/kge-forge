"""Read-only native entry checks; never submit a lifecycle or INSTALL event."""
import hashlib
import json
import os
import sys
from pathlib import Path

from adapter.planner import codec as c, core, gates, installation as install
from adapter.planner import model as m, proof_installation as pi
from adapter.tests.qualify_finish_f03 import semantic_view

ROOT = Path(__file__).resolve().parents[4]
PLANS = ROOT / "docs/plans"
F03 = json.loads((PLANS / "DETERMINISTIC_PLANNER_V0_1_FINISH_F03_RESULT.json").read_text())
MANIFEST = F03["configuration_bundle"]
PATH = PLANS / "DETERMINISTIC_PLANNER_V0_1_E2_P04_FINAL_PREEXECUTION_CONFIGURATION_BUNDLE_1.json"


def identity(value):
    return value.namespace + ":" + value.sha256


def main():
    raw_before = PATH.read_bytes()
    bundle = c.restore(PATH, c._unwire(MANIFEST["bundle_id"]), ROOT)
    state = bundle.current
    computation = core.recompute(state)
    definitions = []
    for record in state.installed_definitions:
        descriptor, _ = install.descriptor(record.request.definition)
        definitions.append({
            "definition_type": descriptor["definition_type"],
            "subject": descriptor["subject"],
            "installed_definition_id": identity(record.id),
            "installation_event_id": identity(bundle.events[record.request.sequence - 1].identity),
            "current": install.current(bundle, record),
        })
    configuration = pi.records(state, "ROOT_SLOT_CONFIGURATION_SET")
    assert len(configuration) == 1
    _, _, _, slot, root, source_authorities, declared_contracts = pi.configuration(configuration[0].request)
    required_authorities = {a.authority for a in state.actions if a.authority is not None}
    required_authorities.update(p.authority for p in declared_contracts)
    authority_checks = []
    for ref in sorted(required_authorities, key=lambda item: item.value):
        entity = next(e for e in state.entities if e.id == ref)
        proof = gates.usable(entity, state)
        authority_checks.append({"id": ref.value, "permissions": [p.value for p in entity.permissions],
                                 "current_proof": proof.state.value, "consumed": entity.consumed})
    pins = []
    for pin in bundle.sources + (bundle.policy,):
        loaded = c.load_pinned(ROOT, pin)
        pins.append({"pin": c._wire(pin), "verified": True,
                     "source_file_sha256": hashlib.sha256((ROOT / pin.path).read_bytes()).hexdigest()})
    lifecycle = {
        "A09": not state.receipt_admissions and all(g.pending is None for g in state.external_gates),
        "A10": not state.validation_results and not state.validation_support_records,
        "A11": not any(type(e.result) is m.DecisionReentry or
                         (type(e.result) is m.ExternalEvent and e.result.stage is m.ExternalStage.DEPENDENT_ACTION_REENTRY)
                         for e in bundle.events),
        "A12": not gates.current_completion(state, m.ActionId("E2-REENTER")),
        "A13": not state.typed_proofs and not gates.current_completion(state, m.ActionId("E2-FINISH")),
        "E2-FINISH": not gates.current_completion(state, m.ActionId("E2-FINISH")),
    }
    oracle = json.loads((PLANS / "qualification/FINISH_F03_1/reader-manifests/final-preexecution.json").read_text())["semantic_oracle"]
    actual_semantic = semantic_view(bundle, ROOT)
    semantics_equal = actual_semantic == oracle
    model_hashes = [{"path": str(Path(path).relative_to(ROOT)),
                     "expected_sha256": digest,
                     "actual_sha256": hashlib.sha256(Path(path).read_bytes()).hexdigest()}
                    for path, digest in F03["generic_qualification"]["hashes"].items()]
    checks = {
        "F03_PASS": F03["RESULT"] == "PASS",
        "F03_DECLARED_P04_EXECUTION_READY": F03["P04_EXECUTION_READY"] == "YES",
        **{a + "_F03_READY": F03[a + "_READY"] == "YES" for a in ("A09", "A10", "A11", "A12", "A13")},
        "bundle_trust": True, "cold_restore": True,
        "bundle_identity_exact": c._identity(raw_before, "planner-bundle-v1") == c._unwire(MANIFEST["bundle_id"]),
        "state_identity_exact": c.snapshot_id(state) == c._unwire(MANIFEST["state_id"]),
        "append_head_exact": bundle.events[-1].identity == c._unwire(MANIFEST["head"]),
        "ledger_event_count_exact": len(bundle.events) == MANIFEST["event_count"],
        "ledger_anchor_exact": c._wire(bundle.events[0].identity) == oracle["ledger_root"],
        "source_pins_exact": sorted(c._wire(bundle.sources), key=c.canonical_bytes) == oracle["sources"],
        "policy_pin_exact": c._wire(bundle.policy) == oracle["policy"] and bundle.policy_version == oracle["policy_version"],
        "scope_lineage_generation_exact": c._wire(state.context) == oracle["context"],
        "all_installed_definitions_current": all(d["current"] for d in definitions),
        "required_authority_entities_current": all(a["current_proof"] == "PROVED" and not a["consumed"] for a in authority_checks),
        "source_semantic_authority_applicability": all(gates.usable(e, state).state is m.ProofState.PROVED for e in source_authorities),
        "complete_F03_initial_semantic_oracle": semantics_equal,
        "qualified_runtime_code_unchanged": all(h["actual_sha256"] == h["expected_sha256"] for h in model_hashes),
        "canonical_lifecycle_unexecuted": all(lifecycle.values()),
        "initial_control_external_wait": computation.control is m.ControlState.EXTERNAL_WAIT,
        "input_bytes_unchanged": PATH.read_bytes() == raw_before,
    }
    result = {
        "role": "READ_ONLY_ENTRY_VERIFICATION; NO_LIFECYCLE_SUBMISSION",
        "pid": os.getpid(), "pid_namespace": os.readlink("/proc/self/ns/pid"),
        "hash_seed": os.environ.get("PYTHONHASHSEED"),
        "checks": checks, "lifecycle_unexecuted": lifecycle,
        "bundle_id": identity(c._unwire(MANIFEST["bundle_id"])),
        "state_id": identity(c.snapshot_id(state)), "append_head": identity(bundle.events[-1].identity),
        "native_ledger_anchor": identity(bundle.events[0].identity), "event_count": len(bundle.events),
        "control": computation.control.value, "context": c._wire(state.context),
        "pins": pins, "installed_definitions": definitions, "required_authorities": authority_checks,
        "qualified_runtime_hashes": model_hashes,
        "proof_contracts": [identity(p.id) for p in state.proof_contracts],
        "typed_proof_instances": [identity(p.id) for p in state.typed_proofs],
        "prospective_proof_declarations": [{
            "id": identity(contract.id), "type": contract.proof_type.value,
            "target": contract.target.value, "supports": c._wire(contract.supports),
            "declared_in_current_configuration": True,
            "present_in_snapshot_proof_contracts": contract in state.proof_contracts,
            "native_contract_current": pi.contract_current(state, contract),
        } for contract in declared_contracts],
        "canonical_events": [{"sequence": e.sequence, "id": identity(e.identity),
                              "parent": identity(e.parent_event) if e.parent_event else None,
                              "result_type": type(e.result).__name__} for e in bundle.events],
        "semantic": actual_semantic,
        "mutation_operations_invoked": [],
    }
    Path(sys.argv[1]).write_bytes(c.canonical_bytes(result))
    print(json.dumps({"checks": len(checks), "all_snapshot_checks_pass": all(checks.values()),
                      "concrete_proof_contracts": len(state.proof_contracts),
                      "declared_proof_contracts_current": [d["native_contract_current"] for d in result["prospective_proof_declarations"]]}))
    assert all(checks.values()), {k: v for k, v in checks.items() if not v}


if __name__ == "__main__":
    main()
