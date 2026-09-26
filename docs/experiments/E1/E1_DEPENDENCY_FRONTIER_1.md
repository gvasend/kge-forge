# E1 Dependency Frontier 1

Evaluation date: 2026-09-21  
Baseline: `E1_DEPENDENCY_BASELINE_1`  
Source: `docs/experiments/E1/E1_DEPENDENCY_MODEL.json`

This is a graph evaluation only. The dependency model, implementation, authority state, and production state were not changed.

## Evaluation result

Prerequisite edges only were traversed backward from `E1_TERMINAL`. Semantic edges were excluded.

- E1-terminal-reachable nodes: **47 of 49**
- Currently `SATISFIED`: **9** reachable nodes
- Currently `BLOCKED` or `UNRESOLVED`: **32** reachable nodes
- Frontier nodes: **6**
- `CurrentProviderModelAuthority` on frontier: **YES**
- Prerequisite cycles: **0**
- Missing authority roots remain as recorded by the baseline

The two nodes outside the terminal-reachable component are `R0_HISTORY` and `PROFILE6`; both are preserved historical/stale roots and are not current execution prerequisites.

## Frontier

### `CURRENT_PROVIDER_MODEL_AUTHORITY`

- **Type/status:** authority / `BLOCKED`
- **Satisfaction criterion:** a canonical current provider/model selector independently authenticates endpoint boundary, model identity/class, purpose, redirect/proxy constraints, and provider-side retention boundary for the R4 E1 handoff.
- **Governing authority:** external provider/model authority and the Architect’s bounded E1 execution authority.
- **Immediate RequiredBy:** `CURRENT_CONTENT_CLEARANCE_AUTHORITY`, `CURRENT_RETENTION_AUTHORITY`, `CURRENT_TRANSMISSION_AUTHORITY`, `FINAL_FRESH_GATE`, `FIRST_REAL_MODEL_REQUEST`, `HOST_CONSTRUCTION`.
- **Shortest dependent path:** `CURRENT_PROVIDER_MODEL_AUTHORITY → FINAL_FRESH_GATE → E1_TERMINAL`.
- **Traversal stop:** current provider/model authority is an external blocked root; the current dispatch contains references but no canonical selector or authorized derivation.
- **Resolution category:** `EXTERNAL_AUTHORITY`, then `HUMAN_AUTHORITY` for bounded approval. No resolution was attempted.

### `CURRENT_MODEL_PAYLOAD_AUTHORITY`

- **Type/status:** authority / `UNRESOLVED`
- **Satisfaction criterion:** a canonical owner or authorized deterministic derivation reconstructs the exact current model-visible payload represented by the payload digest.
- **Governing authority:** current E1 content/payload authority.
- **Immediate RequiredBy:** `CURRENT_CONTENT_CLEARANCE_AUTHORITY`, `HOST_CONSTRUCTION`, `RELEASE_AUTHORITY_CURRENT`.
- **Shortest dependent path:** `CURRENT_MODEL_PAYLOAD_AUTHORITY → CURRENT_CONTENT_CLEARANCE_AUTHORITY → FINAL_FRESH_GATE → E1_TERMINAL`.
- **Traversal stop:** the digest is reference-only; no current canonical payload owner or approved derivation is established.
- **Resolution category:** `DETERMINISTIC_EVALUATION` to identify/verify the owning object, followed by `EXTERNAL_AUTHORITY`/`HUMAN_AUTHORITY` if a source must be established. No resolution was attempted.

### `LIFECYCLE_TEMPLATE`

- **Type/status:** authority / `HISTORICAL_ONLY`
- **Satisfaction criterion:** an authenticated production-consumable WorkAuthorization lifecycle template is available to the current consumer and bounded to the accepted lifecycle semantics.
- **Governing authority:** Architect lifecycle authority and the R4 lifecycle consumer.
- **Immediate RequiredBy:** `LIFECYCLE_ISSUANCE`.
- **Shortest dependent path:** `LIFECYCLE_TEMPLATE → LIFECYCLE_ISSUANCE → INACTIVE_ISSUANCE → CANCELLATION → PROGRAMMER_LOOP → E1_TERMINAL`.
- **Traversal stop:** the accepted template exists only as qualification evidence; no production-consumable template is current. Its status is historical rather than a satisfied current authority.
- **Resolution category:** `EXTERNAL_AUTHORITY` and `HUMAN_AUTHORITY`; the template must not be synthesized from the concrete WorkAuthorization. No resolution was attempted.

### `R3_HISTORY`

- **Type/status:** runtime ancestry / `HISTORICAL_ONLY`
- **Satisfaction criterion:** preserved authenticated R3 predecessor evidence remains available for R4 lineage and historical checks.
- **Governing authority:** accepted R3→R4 transition history.
- **Immediate RequiredBy:** `R4_CURRENT`.
- **Shortest dependent path:** `R3_HISTORY → R4_CURRENT → FINAL_FRESH_GATE → E1_TERMINAL`.
- **Traversal stop:** this is a preserved historical predecessor, not an unsatisfied current authority root. It requires no repair or promotion.
- **Resolution category:** `NOT_APPLICABLE` to current execution; historical preservation only.

### `RELEASE_BB1808A`

- **Type/status:** authority history / `HISTORICAL_ONLY`
- **Satisfaction criterion:** the noncanonical `bb1808a…` provenance remains preserved and explicitly excluded from current authority.
- **Governing authority:** forensic historical correction.
- **Immediate RequiredBy:** `RELEASE_AUTHORITY_CURRENT`.
- **Shortest dependent path:** `RELEASE_BB1808A → RELEASE_AUTHORITY_CURRENT → CURRENT_DISPATCH → DISPATCHER_ELIGIBILITY → HOST_CONSTRUCTION → MODEL_REQUEST_READY → FINAL_FRESH_GATE → E1_TERMINAL`.
- **Traversal stop:** `bb1808a…` has no canonical owner or authenticated issuance chain and must not be repaired or promoted.
- **Resolution category:** `NOT_APPLICABLE` to current execution; preserve as historical evidence. Current release authority requires a separate prospective root.

### `RELEASE_C43F119`

- **Type/status:** authority ancestry / `HISTORICAL_ONLY`
- **Satisfaction criterion:** the last independently established Run-2 release ancestry remains preserved without being mislabeled current.
- **Governing authority:** authenticated historical Run-2 release derivation.
- **Immediate RequiredBy:** `RELEASE_AUTHORITY_CURRENT`.
- **Shortest dependent path:** `RELEASE_C43F119 → RELEASE_AUTHORITY_CURRENT → CURRENT_DISPATCH → DISPATCHER_ELIGIBILITY → HOST_CONSTRUCTION → MODEL_REQUEST_READY → FINAL_FRESH_GATE → E1_TERMINAL`.
- **Traversal stop:** historical ancestry alone does not establish the current R4 release root; no current root decision is inferred.
- **Resolution category:** `HUMAN_AUTHORITY` is required for any prospective current root, but this historical node itself requires preservation only. No resolution was attempted.

## Frontier interpretation

The actionable frontier consists of `CURRENT_PROVIDER_MODEL_AUTHORITY`, `CURRENT_MODEL_PAYLOAD_AUTHORITY`, and the production lifecycle template gap. The three release/R3 nodes are historical leaves encountered through the graph and are not candidates for promotion or repair. They remain useful lineage evidence while current authority is reconstructed independently.

The frontier is not a list of tasks to execute automatically. Each node remains blocked, unresolved, or historical under the baseline’s authority rules.

## Current production preservation

`R4-final = CURRENT + UNIQUE`; `LIVE_R4_FINAL_CONTROLLER_STORE = G4 CURRENT`; r13 remains `UNISSUED + UNOWNED`; provider/model requests and E1 effects remain zero. No dependency was added, no blocker was resolved, and no authority was issued.
