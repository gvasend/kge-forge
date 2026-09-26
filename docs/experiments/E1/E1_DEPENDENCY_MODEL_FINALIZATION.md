# E1 Dependency Model — Prerequisite Projection Finalization

Finalization date: 2026-09-21. Only the two corrections recommended by the cycle semantics review were applied. No dependency was newly discovered, no blocker was resolved, and no production or implementation state changed.

## Designation

The resulting model is designated **`E1_DEPENDENCY_BASELINE_1`**.

The prerequisite projection contains only ordering/derivation relationships. Non-ordering currentness and binding relationships remain preserved in `SemanticEdges`.

## Corrections applied

- Moved `G4_CURRENT → R4_CURRENT` from prerequisite edges to semantic edge `currentness_correspondence`. `R4_CURRENT → G4_CURRENT` remains the generation derivation/temporal prerequisite.
- Moved `OPERATIONAL_BINDING_CURRENT → INVOCATION_CANDIDATE` from prerequisite edges to semantic edge `binding_applicability_constraint`. `INVOCATION_CANDIDATE → OPERATIONAL_BINDING_CURRENT` remains the binding derivation prerequisite.

No other edges were removed.

## Mechanical validation

- Node count: **49**
- Prerequisite edge count: **104**
- Semantic edge count: **2**
- Duplicate prerequisite edges: **0**
- Dangling references: **0**
- Self edges: **0**
- Connected components: **3**, sizes `[47, 1, 1]`
- Cycles in prerequisite projection: **0**
- Nodes reachable from `E1_TERMINAL`: **47**
- Nodes unable to reach `E1_TERMINAL`: `['PROFILE6', 'R0_HISTORY']`
- Unresolved leaves: `['CURRENT_PROVIDER_MODEL_AUTHORITY', 'CURRENT_MODEL_PAYLOAD_AUTHORITY', 'CURRENT_RETENTION_AUTHORITY', 'CURRENT_TRANSMISSION_AUTHORITY', 'PROFILE_ROOTS', 'RELEASE_AUTHORITY_CURRENT', 'OPERATIONAL_CONTEXT_CURRENT', 'OPERATIONAL_BINDING_CURRENT']`
- Missing authority roots: `['CurrentProviderModelAuthority', 'CurrentModelPayloadAuthority', 'CurrentTransmissionAuthority', 'CurrentRetentionAuthority', 'ReleasedProfileAuthority/current profile roots', 'CurrentReleaseAuthority', 'OperationalContext', 'OperationalBinding']`

The prerequisite projection is a DAG: no prerequisite cycles remain. The two historical/stale singleton roots remain outside the current execution chain and are not promoted to authority.

## CurrentProviderModelAuthority path

Using prerequisite edges only:

`CURRENT_PROVIDER_MODEL_AUTHORITY` → `CURRENT_CONTENT_CLEARANCE_AUTHORITY` → `RELEASED_PROFILE_CURRENT` → `RELEASE_AUTHORITY_CURRENT` → `OPERATIONAL_CONTEXT_CURRENT` → `OPERATIONAL_BINDING_CURRENT` → `CONCRETE_WORKAUTH` → `INACTIVE_ISSUANCE` → `ACTIVATION` → `ACTIVE_RECOVERY` → `DISPATCHER_ELIGIBILITY` → `HOST_CONSTRUCTION` → `MODEL_REQUEST_READY` → `FINAL_FRESH_GATE` → `E1_TERMINAL`

`CURRENT_PROVIDER_MODEL_AUTHORITY` remains `BLOCKED`; this path is structural only and does not infer or issue provider authority.

## Semantic preservation

`G4_CURRENT → R4_CURRENT` remains available as a live-consumer currentness constraint. `OPERATIONAL_BINDING_CURRENT → INVOCATION_CANDIDATE` remains available as a binding/applicability constraint. Removing them from prerequisite traversal preserves the knowledge while preventing circular satisfaction semantics.

Production remains R4/G4 unchanged, r13 remains unissued/unowned, and provider/model requests and E1 effects remain zero.
