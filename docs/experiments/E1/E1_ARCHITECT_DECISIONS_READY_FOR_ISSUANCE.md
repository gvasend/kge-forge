# E1 Architect Decisions — Records Ready for Issuance

Date: 2026-09-21  
State: **PREPARED / UNISSUED**  
Scope: `E1_DEPENDENCY_BASELINE_2`, current R4/G4 E1 envelope.

These are canonical record drafts prepared from current qualified evidence. They do not issue, select, publish, or activate authority. No dependency status, implementation, or production state changed.

## 1. `CURRENT_PROVIDER_MODEL_AUTHORITY-1`

```yaml
record_type: CURRENT_PROVIDER_MODEL_AUTHORITY-1
status: UNISSUED
scope: LIVE_R4/E1-WP-001/FIRST_PROGRAMMER_REQUEST
runtime: sha256:b6bcbb437f63c1433167103b1c7e15b723190721518e02ff2e4d2523fd625761
controller_store: AUTHORITY-STORE-GENERATION-sha256:ab07c7cbd889588fd80976bf5c47b7358722eaf6e2e1b7364e612c03899bf9ff
dispatch: E1-ARCHITECT-DISPATCH-R4-FINAL-sha256:43654010c1048e6899a561878475e1fcd3bdecc0de98fea24f2e64c36e2f91ad
provider_endpoint: UNRESOLVED
provider_boundary: UNRESOLVED
model_identity_or_class: UNRESOLVED
transmission_boundary: UNRESOLVED
provider_retention_behavior: UNRESOLVED
purpose: E1-WP-001 first Programmer request only
redirect_proxy_constraints: UNRESOLVED
freshness: validate against current R4/G4 at final gate
replay: single bounded decision; no expansion
identity: UNISSUED_UNHASHED
architect_decision: UNISSUED
```

### Missing facts

The current qualified evidence does not establish any of the unresolved provider-bound fields. `CURRENT_R4_HANDOFF_AUTHORITY_ROOT_BLOCKED.json` (SHA-256 `89095b7908da63aa6e851c47164c264b9d9a58b8f5ae899b142e867ad888a66f`) explicitly reports:

- no independently current provider/model selection;
- no canonical provider endpoint or boundary;
- no model identity/class selection;
- transmission/retention reference present but not provider-scoped;
- implementation transport and provider availability are not authority.

No value was substituted from Profile-6, PD06, implementation defaults, or provider availability. Consequently this record is prepared but cannot be content-complete or issued.

## 2. `CURRENT_MODEL_PAYLOAD_AUTHORITY-1`

This record uses construct-then-hash semantics. Its identity remains unresolved until the named source authorities produce canonical current values.

```yaml
record_type: CURRENT_MODEL_PAYLOAD_AUTHORITY-1
status: UNISSUED
scope: LIVE_R4/E1-WP-001/FIRST_PROGRAMMER_REQUEST
source_authorities:
  task_scope: docs/experiments/E1/pre_dispatch/E1-WP-001.md
  current_runtime: sha256:b6bcbb437f63c1433167103b1c7e15b723190721518e02ff2e4d2523fd625761
  current_controller_store: AUTHORITY-STORE-GENERATION-sha256:ab07c7cbd889588fd80976bf5c47b7358722eaf6e2e1b7364e612c03899bf9ff
  current_dispatch: E1-ARCHITECT-DISPATCH-R4-FINAL-sha256:43654010c1048e6899a561878475e1fcd3bdecc0de98fea24f2e64c36e2f91ad
  provider_model_authority: CURRENT_PROVIDER_MODEL_AUTHORITY-1 / UNISSUED
payload_derivation:
  rule: canonicalize authenticated source authorities and fixed first-request projection, then hash
  canonical_order: source-authority identities, task/governance projection, fixed metadata, exclusions
  dynamic_repository_selection: FORBIDDEN_FOR_INITIAL_PAYLOAD
  identity: UNRESOLVED_PENDING_CANONICAL_SOURCE_VALUES
content_classes:
  task_and_governance: REQUIRE_CANONICAL_CURRENT_SOURCE
  fixed_model_projection: REQUIRE_CANONICAL_CURRENT_SOURCE
  tool_schemas: ONLY_IF_IN_EXPLICIT_CURRENT_PROFILE
  preloaded_knowledge: ONLY_IF_EXPLICITLY_BOUND
  repository_content: NEVER_TRANSMIT_INITIAL_PAYLOAD_UNLESS_EXPLICITLY_BOUND
exclusions:
  secrets: NEVER_TRANSMIT
  credentials: NEVER_TRANSMIT
  unrelated_repository_content: NEVER_TRANSMIT
  protected_files: NEVER_TRANSMIT_UNLESS_EXPLICITLY_CLEARED
  arbitrary_future_reads: NEVER_TRANSMIT_INITIAL_PAYLOAD
provider_binding: reference to separately issued provider/model authority
architect_decision: UNISSUED
```

### Identity rule and missing inputs

The payload body must be constructed from independently authenticated current authorities, serialized canonically, and hashed only after construction. The existing `ModelPayloadDigest` (`d675d581c80f43e691a31da73ccf17fd4bcc6b00d3a5331f26b9294e294e1538`) is retained as a reference only and is not used as a target. A canonical current payload owner/derivation and the provider/model boundary remain unavailable, so no payload identity is assigned.

## 3. `WORK-AUTHORIZATION-TEMPLATE-1`

```yaml
record_type: WORK-AUTHORIZATION-TEMPLATE-1
status: UNISSUED
scope: LIVE_R4/E1 exact authority envelope
schema: WORK-AUTHORIZATION-TEMPLATE-1
qualified_template_identity: WorkAuthorizationTemplate-sha256:d49797c4d2072c310f30f038be6fd597d3a74b2ce6a0a8a06d6dd831989ffee8
qualified_serialization_sha256: 17fb2610fcff3bf398b040ba9d33c96cb4f86d8abd805dbb03be98aa52d68307
initial_state: INACTIVE
initial_ownership: NONE
permitted_lifecycle: previously-qualified corrected R4 lifecycle only
required_inputs: authenticated concrete WorkAuthorization, issuance authority, lifecycle proof, activation-context proofs
replay: duplicate and competing issuance rejected
expansion: no provider, payload, repository, runtime-adoption, or authority-expansion scope
runtime_binding: R4-final CURRENT / G4 CURRENT at consumption
architect_decision: UNISSUED
```

The listed identity and serialization are qualification evidence for the corrected template semantics. They do not constitute production publication or release.

## 4. `WORKAUTHORIZATION-ISSUANCE-AUTHORITY-1`

```yaml
record_type: WORKAUTHORIZATION-ISSUANCE-AUTHORITY-1
status: UNISSUED
scope: EXACT_SINGLE_WORKAUTHORIZATION_INACTIVE
workauthorization_id: WorkAuthorization-sha256:bc53d20ea0383febbd7ce1c10e2e00b2461a722942b853f43ea5001b42976c61
invocation_attempt: InvocationAttempt-sha256:bce363cb3dfd25deaff6f6ef4ed67c9d70af859fe998c09ff133deb11f346ba8
invocation_binding_sha256: 757f52b9567658040da134bff8292f5663146b1611cba6d61fcd35c2cdcfd224
dispatch: E1-ARCHITECT-DISPATCH-R4-FINAL-sha256:43654010c1048e6899a561878475e1fcd3bdecc0de98fea24f2e64c36e2f91ad
runtime: sha256:b6bcbb437f63c1433167103b1c7e15b723190721518e02ff2e4d2523fd625761
controller_store: AUTHORITY-STORE-GENERATION-sha256:ab07c7cbd889588fd80976bf5c47b7358722eaf6e2e1b7364e612c03899bf9ff
issuance_effect: INACTIVE + NO OWNERSHIP ONLY
single_use: true
replay: reject duplicate, competing, stale, or mismatched issuance
freshness: revalidate runtime, dispatch, context, release, audit namespace, and ownership at consumption
architect_decision: UNISSUED
identity: UNISSUED_UNHASHED
```

This draft represents the scope of the existing Architect r13 decision operationally; it does not itself grant that decision and does not consume the WorkAuthorization. The WorkAuthorization remains unpublished and unconsumed.

## Cross-record constraints

- Provider/model authority is incomplete; no payload or clearance record may be issued against an invented provider boundary.
- Payload identity must be derived from authenticated current sources and bound to the selected provider/model authority if that authority is later issued.
- The lifecycle template and issuance authority govern only lifecycle instantiation. They do not authorize provider transmission or payload content.
- All records must remain bound to current R4/G4 and the exact R4/E1 scope at any future issuance gate.

## Preservation

`R4-final = CURRENT + UNIQUE`; `LIVE_R4_FINAL_CONTROLLER_STORE = G4 CURRENT`; r13 remains `UNISSUED + UNOWNED`; WorkAuthorization remains unpublished/unconsumed; provider/model requests and E1 effects remain zero. All four records above are **UNISSUED**.
