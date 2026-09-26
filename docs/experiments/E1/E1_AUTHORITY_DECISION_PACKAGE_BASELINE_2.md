# E1 Authority Decision Package — Baseline 2

Date: 2026-09-21  
Planning state: `E1_DEPENDENCY_BASELINE_2`  
Status: **PREPARATION ONLY — ALL DRAFTS UNISSUED**

This package identifies the minimum Architect decisions required for the three unresolved frontier authority nodes. It grants no authority, changes no dependency status, and performs no production action.

## 1. `CURRENT_PROVIDER_MODEL_AUTHORITY`

### Decision required

Choose and approve one exact current provider/model boundary for the first E1-WP-001 Programmer request, or explicitly decline/ defer provider handoff. The decision must establish the provider endpoint/boundary, model identity or class, purpose, scope, redirect/proxy constraints, and provider-side retention boundary.

### Why authority is required

The live R4 dispatch contains a payload digest and transmission/retention reference, but the accepted handoff forensic record says no independently current released provider/model selection authorizes the R4 E1 boundary. Transport implementation, provider availability, Profile-6, PD06 qualification, and historical requests do not confer authority.

### Minimum decision scope

The narrowest approval is one provider/model selection for the first E1-WP-001 request under current R4 authority. It must not authorize arbitrary providers, future models, unrelated payloads, repository access, tool expansion, or future invocations.

### Proposed bindings requiring choice

- Provider/service boundary: exact named provider or approved internal boundary.
- Endpoint/proxy: exact endpoint and redirect/proxy restrictions.
- Model: exact model identity or narrowly bounded class.
- Purpose: E1-WP-001 first Programmer request only.
- Runtime: exact current R4 runtime and G4 controller-store lineage.
- Scope/lineage: R4/E1, current dispatch/invocation lineage.
- Freshness: selection must be current at final fresh gate and single-use/replay constrained as applicable.
- Retention: either bind the exact provider retention behavior here or reference a separately authoritative retention record.

### Existing evidence (not authority)

- `CURRENT_R4_HANDOFF_AUTHORITY_ROOT_BLOCKED.json` (SHA-256 `89095b7908da63aa6e851c47164c264b9d9a58b8f5ae899b142e867ad888a66f`) identifies the missing provider/model selector and required semantics.
- `R4_FINAL_CURRENT_DISPATCH.json` identifies the current R4 dispatch and payload/transmission references.
- `adapter/model_transport.py` and `adapter/model_transmission.py` demonstrate implementation behavior only.

### Consequences

If approved, `CURRENT_CONTENT_CLEARANCE_AUTHORITY`, `CURRENT_TRANSMISSION_AUTHORITY`, and `CURRENT_RETENTION_AUTHORITY` become eligible for independent reevaluation against the selected boundary. `HOST_CONSTRUCTION`, `MODEL_REQUEST_READY`, and the final fresh gate remain unsatisfied until their own criteria pass. If declined, the provider handoff path remains blocked.

### Proposed unissued record

```yaml
record_type: CURRENT_PROVIDER_MODEL_AUTHORITY-1
status: UNISSUED
scope: LIVE_R4/E1-WP-001/FIRST_PROGRAMMER_REQUEST
provider: ARCHITECT_CHOICE_REQUIRED
endpoint_boundary: ARCHITECT_CHOICE_REQUIRED
model_identity_or_class: ARCHITECT_CHOICE_REQUIRED
purpose: E1-WP-001 only
runtime_binding: R4-final CURRENT + G4 CURRENT
transmission_boundary: separately-bound-or-explicit
retention_binding: separately-bound-or-explicit
freshness_rule: validate at final fresh gate
replay_rule: single bounded decision; no expansion
architect_decision: UNISSUED
```

## 2. `CURRENT_MODEL_PAYLOAD_AUTHORITY`

### Decision required

Choose the authoritative source for the exact first-request model-visible payload: either approve one canonical immutable payload object, or approve one deterministic derivation from named current source authorities. The decision must identify the exact payload and its R4/E1 scope.

### Why authority is required

The current `ModelPayloadDigest` is a reference-only identity. Existing evidence does not establish a canonical current payload owner or an authorized derivation. A digest copied into dispatch, invocation, or qualification evidence cannot authenticate the payload by itself.

### Minimum decision scope

Approve only the first E1-WP-001 request payload under the selected R4 provider/model boundary. The decision must exclude arbitrary later repository reads, secrets, credentials, unrelated repository content, and dynamically selected content outside the stated envelope.

### Proposed bindings requiring choice

- Payload source: exact canonical payload artifact, or exact named derivation inputs and constructor.
- Payload contents: task/governance projection, model-visible instructions, fixed metadata, and explicitly permitted preloaded knowledge.
- Dynamic content: explicitly prohibited or bounded selection rule for later governed ActionResults.
- Exclusions: secrets, credentials, protected/unrelated files, and unapproved repository content.
- Runtime/scope: current R4/E1 and exact invocation/dispatch lineage.
- Content identity: independently recomputed after the source decision; no target digest assumption.
- Provider/model binding: must match the separately decided current provider/model authority.

### Existing evidence (not authority)

- Current dispatch payload digest `d675d581c80f43e691a31da73ccf17fd4bcc6b00d3a5331f26b9294e294e1538`.
- `CURRENT_R4_HANDOFF_AUTHORITY_ROOT_BLOCKED.json`, which explicitly classifies the digest as reference-only.
- Historical `PD06` content-clearance and projection artifacts, which are qualification/history only and not current R4 payload authority.

### Consequences

If approved, `CURRENT_CONTENT_CLEARANCE_AUTHORITY` becomes eligible for content-inventory and boundary reevaluation. `HOST_CONSTRUCTION`, `MODEL_REQUEST_READY`, and final-gate checks still require independent validation. If the payload is changed from the historical digest, existing dispatch/invocation applicability must be reevaluated; no replacement is implied by this package.

### Proposed unissued record

```yaml
record_type: CURRENT_MODEL_PAYLOAD_AUTHORITY-1
status: UNISSUED
scope: LIVE_R4/E1-WP-001/FIRST_PROGRAMMER_REQUEST
payload_source: ARCHITECT_CHOICE_REQUIRED
payload_derivation: NONE_UNLESS_EXPLICITLY_APPROVED
content_inventory: REQUIRED_BEFORE_ISSUANCE
exclusions: secrets_credentials_unrelated_repository_content
runtime_binding: R4-final CURRENT + G4 CURRENT
provider_model_binding: reference-to-separately-issued-authority
identity_rule: construct-then-hash; no caller-supplied digest
architect_decision: UNISSUED
```

## 3. `LIFECYCLE_TEMPLATE`

### Decision required

Approve one canonical production `WORK-AUTHORIZATION-TEMPLATE-1` with bounded lifecycle semantics, and separately approve the applicable issuance authority for the exact concrete WorkAuthorization. The decision must state whether the template is reusable for a bounded compatible class or scoped to this exact R4/E1 authority envelope.

### Why authority is required

Corrected template/instance/issuance separation and lifecycle tests passed in qualification, but no production-consumable template is current. The R4 consumer requires an authenticated template; implementation defaults and the concrete WorkAuthorization cannot supply it without circular authority.

### Minimum decision scope

Authorize only:

`authenticated template + exact applicable WorkAuthorization + issuance authority → INACTIVE + NO OWNERSHIP`

under current R4/E1 lifecycle semantics. The template must not authorize a particular model request, repository effect, runtime adoption, authority expansion, or arbitrary invocation unless separately bound by qualified records.

### Proposed bindings requiring choice

- Schema/version: `WORK-AUTHORIZATION-TEMPLATE-1` or the qualified production schema.
- Initial state: exactly `INACTIVE + NO OWNERSHIP`.
- Lifecycle transitions: only already-qualified activation, ownership, recovery, cancellation, and terminal rules.
- Scope: exact R4/E1 authority envelope or explicitly bounded compatible class.
- Required authority classes: concrete WorkAuthorization, invocation/dispatch/context/profile/ownership/audit proofs as required by the corrected consumer.
- Replay/duplicate rules: single-use issuance and competing issuance rejection.
- Issuance authority: exact Architect-approved r13 WorkAuthorization decision, represented separately.
- Runtime/release binding: current R4/G4 at consumption, with final freshness validation.

### Existing evidence (not authority)

- Corrected template identity `WorkAuthorizationTemplate-sha256:d49797c4d2072c310f30f038be6fd597d3a74b2ce6a0a8a06d6dd831989ffee8` and issuance identity `WorkAuthorizationIssuance-sha256:fe7b757c66d9071fd0e7866044daad9cb85e2b57b52dd2bca682ba4b228b7a4e` are qualification artifacts only.
- Targeted lifecycle qualification established the canonical INACTIVE boundary and negative/replay behavior.
- Existing WorkAuthorization remains exact, unpublished, and unconsumed.

### Consequences

If approved, the lifecycle issuance path becomes eligible for independent validation against the exact template, issuance authority, and concrete WorkAuthorization. `INACTIVE_ISSUANCE`, activation, ownership, recovery, dispatcher, and `MODEL_REQUEST_READY` remain unsatisfied until their own criteria pass. If approval is scoped differently, the concrete WorkAuthorization and lifecycle applicability must be reevaluated.

### Proposed unissued records

```yaml
record_type: WORK-AUTHORIZATION-TEMPLATE-1
status: UNISSUED
scope: ARCHITECT_CHOICE_REQUIRED
initial_state: INACTIVE
initial_ownership: NONE
permitted_transitions: previously-qualified-R4-lifecycle-only
replay_rule: duplicate-and-competing-issuance-rejected
expansion_rule: no invocation/provider/repository/runtime authority
architect_decision: UNISSUED

record_type: WORKAUTHORIZATION-ISSUANCE-AUTHORITY-1
status: UNISSUED
scope: EXACT_SINGLE_WORKAUTHORIZATION_INACTIVE
workauthorization: exact-existing-r13-artifact
invocation: exact-current-candidate-required
runtime_release: current-R4/G4-at-consumption
single_use: true
architect_decision: UNISSUED
```

## Cross-node consistency

The three authorities constrain one another but must not be merged for convenience:

- Provider/model authority constrains the provider boundary that content clearance and payload authority must bind.
- Payload authority must identify the exact model-visible content used by content clearance; it does not select the provider.
- Lifecycle template/issuance authority governs lifecycle instantiation only; it does not authorize provider transmission or payload contents.
- Current R4/E1 scope, runtime lineage, dispatch/invocation identity, and freshness checks must agree across records.

A single Architect session may decide all three, but each decision should remain a distinct append-only authority record with distinct scope and replay rules.

## Architect Decision Summary

1. Select or decline one exact provider/model endpoint and model boundary for the first R4/E1 Programmer request, including transmission and retention scope.
2. Approve one exact current model payload source or authorized deterministic payload derivation for that request, with explicit content inventory and exclusions.
3. Approve one bounded production `WORK-AUTHORIZATION-TEMPLATE-1` and the separate issuance authority permitting the exact concrete WorkAuthorization to establish `INACTIVE + NO OWNERSHIP`.

All three draft records remain **UNISSUED**. No authority is granted by this package.
