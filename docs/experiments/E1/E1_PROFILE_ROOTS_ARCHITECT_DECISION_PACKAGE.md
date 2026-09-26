# E1 Profile Roots — Architect Decision Package

## Decision status

`PROFILE_ROOTS` remains `BLOCKED` and this package is **UNISSUED**. It prepares the narrowest current R4/E1 profile-root decision for the first E1-WP-001 Programmer request.

## Semantics and dimensions

`PROFILE_ROOTS` supplies independently authoritative current policy/configuration inputs for a `ReleasedProfileAuthority`. It does not itself release a profile and cannot be sourced from Profile-6, G4 metadata, implementation defaults, or the payload.

| Dimension | Profile-6 qualified value | Current R4 assessment | Downstream effect |
|---|---|---|---|
| Task/profile scope | E1-WP-001, Profile-6 revision 6 | Reuse only if explicitly reauthorized for exact R4/G4 and first request | Programmer profile and host construction |
| Provider/model | OpenAI Responses, `gpt-5`, `store=false`, no proxy, redirects denied, TLS 1.2 | Technically compatible baseline; current authority is supplied separately and must be bound | Provider and transmission validation |
| Model/content clearance | PD06 manifest/reference and historical projection | Historical value is not current; exact current payload/content-clearance authorities are now issued and must be referenced | Model-visible content and transmission |
| Tool/action registry | Empty initial tool schemas; no generic tools/MCP/connectors/additional agents | Reusable only after current-scope requalification | Action surface and authority expansion |
| Repository/read/write scope | Explicit governed roots; writes restricted to qualified task paths; promotion none | Reusable baseline only with current R4 source map and requalification | Repository authority and Programmer actions |
| Execution/shell/network | Python allowlist; shell false; task network false; model endpoint only | Reusable baseline subject to current runtime/profile qualification | Governed host execution |
| Credentials/secrets | Host credential reference only; no model-visible credentials | Unchanged restriction; must remain explicit | Secret exclusion and transport safety |
| Transmission/retention | Provider endpoint and `store=false`; PD06 required selections unresolved | Current issued provider, transmission, retention, payload and content-clearance authorities must be bound | Model request readiness |
| Audit/ownership/recovery | Append-only audit, shared ownership ledger, restart same identity/no reset | Reusable only if bound to current R4 lifecycle and audit authorities | Lifecycle and recovery |
| Budgets/escalation | Existing E1 budget and fail-closed escalation rules | Requires current R4 applicability confirmation | Status, cancellation, hard exhaustion |
| Authority expansion | No dispatch, repository, model, or scope expansion from profile alone | Must remain none | All downstream authority gates |

## Historical Profile-6 reconstruction

Historical profile bytes: `sha256:fb842649d30e5876fb3f299e890e2c555a88be759c29b2c6577552d4885b0226` (`E1-PRODUCTION-PROFILE-6`). It is technically qualified for historical PD06/R8–R11 scope and stale/superseded for current R4 scope. Its `architect_status = PENDING_ARCHITECT_REVIEW`, `eligible = false`, and `dispatch_issued = false` are preserved.

The historical profile records the baseline runtime, repository roots, Python execution allowlist, no task network, model endpoint restrictions, append-only audit, shared ownership ledger, and no-promotion policy. Those are `QUALIFIED_VALUE` plus `HISTORICAL_ONLY`; they are not current release authority. Current values for scope, content clearance, policy roots, and release applicability remain `CURRENT_VALUE_UNKNOWN` until this decision and technical requalification.

## Minimum proposed authority

Prepare one bounded `CURRENT_PROFILE_ROOT_AUTHORITY-1` record, unissued, scoped exactly to:

- runtime `sha256:b6bcbb437f63c1433167103b1c7e15b723190721518e02ff2e4d2523fd625761`;
- live controller store G4 `AUTHORITY-STORE-GENERATION-sha256:ab07c7cbd889588fd80976bf5c47b7358722eaf6e2e1b7364e612c03899bf9ff`;
- current R4 unique lineage;
- E1-WP-001 first Programmer request only;
- previously issued provider, payload, retention, transmission, and content-clearance authorities.

Proposed fields:

```text
record_type = CURRENT_PROFILE_ROOT_AUTHORITY-1
status = UNISSUED / PENDING_ARCHITECT_DECISION
scope = LIVE_R4/G4/E1-WP-001/FIRST_PROGRAMMER_REQUEST
historical_baseline = E1-PRODUCTION-PROFILE-6 (reference only)
profile_constraints = exact technically requalified least-authority constraints
content_clearance = CurrentContentClearanceAuthority-sha256:3243f4e84d3434655d8455355bd9ea742c0659cbf49827b9eeb80160b39646b3
provider = CurrentProviderModelAuthority-sha256:95b3d340ec85add69b1a472acffa4eb4372f3e528a8dc29278a8fe0fd58b0939
payload = CurrentModelPayloadAuthority-sha256:cc20ba70d59acab0b322db7231cb4b77f183994dfb2db5c0b8405d5ed6629ada
transmission = CurrentTransmissionAuthority-sha256:2adc46e1422ad0934597e398540f2e9f54eb57c601f8b29f8a805b06a611f79c
retention = CurrentRetentionAuthority-sha256:c17023b118aeb4ecd7a57a72b0d8f5826415ecb8dd87e83c49a55afde9d60462
architect_decision = ARCHITECT_CHOICE_REQUIRED
profile_content_identity = ARCHITECT_CHOICE_REQUIRED after current candidate qualification
qualification_evidence = CURRENT_R4_PROFILE_QUALIFICATION.json plus new current-root qualification
```

The Architect choice is: approve these exact technically qualified profile-root values for the stated scope, or identify the narrower replacements. No choice may release Profile-6 retroactively or authorize future requests.

## Consequences

If the proposed profile-root authority is issued, only deterministic prerequisites become eligible for reevaluation. `RELEASED_PROFILE_CURRENT` becomes eligible for bounded semantic/technical evaluation; it is not automatically satisfied. Downstream `PROGRAMMER_PROFILE`, `HOST_CONSTRUCTION`, `OPERATIONAL_BINDING_CURRENT`, and `RELEASE_AUTHORITY_CURRENT` remain blocked until their own criteria pass.

## Preservation

No authority was issued, no dependency status or topology changed, and no production action occurred. R4/G4, Profile-6, r13, and all historical qualification evidence remain unchanged.
