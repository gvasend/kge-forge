# E1 Graph-Directed Frontier Experiment

Date: 2026-09-21  
Baseline: `E1_DEPENDENCY_BASELINE_1`  
Scope: the six frontier nodes recorded in `E1_DEPENDENCY_FRONTIER_1.md`.

This report evaluates each frontier node independently. It does not modify the baseline, resolve blockers, issue authority, execute downstream work, or change implementation/production state.

## Summary

- Total frontier nodes: **6**
- `KNOWN_LEAF_RESOLVED`: **3**
- `KNOWN_LEAF_REQUIRES_AUTHORITY`: **3**
- `NEW_DEPENDENCY_DISCOVERED`: **0**
- `BASELINE_DEFECT`: **0**
- Runtime experiments required: **0**
- Authority decisions required: **3 current-authority leaves**

The three resolved nodes are historical/forensic leaves. Their resolution establishes preservation and interpretation, not current execution authority.

## Results

### `CURRENT_PROVIDER_MODEL_AUTHORITY`

- **Classification:** `KNOWN_LEAF_REQUIRES_AUTHORITY`
- **Prior result:** `AUTHORITY_REQUIRED` in `E1_GRAPH_DIRECTED_RESOLUTION_1.md`
- **New dependency discovery:** No
- **LLM semantic reasoning required:** No new reasoning; the accepted blocker classification is explicit.
- **Deterministic evaluation sufficient:** Yes, for the existing evidence classification.
- **Runtime experimentation required:** No
- **External/human authority required:** Yes
- **Basis:** `CURRENT_R4_HANDOFF_AUTHORITY_ROOT_BLOCKED.json` identifies the exact missing current provider/model selector, endpoint boundary, model identity/class, provider-scoped transmission, and retention semantics. Dispatch, implementation transport, Profile-6, and provider availability cannot substitute for authority.

### `CURRENT_MODEL_PAYLOAD_AUTHORITY`

- **Classification:** `KNOWN_LEAF_REQUIRES_AUTHORITY`
- **New dependency discovery:** No
- **LLM semantic reasoning required:** No new reasoning; the source is already classified as reference-only.
- **Deterministic evaluation sufficient:** Yes, for digest-owner/source verification.
- **Runtime experimentation required:** No
- **External/human authority required:** Yes, if a canonical payload owner or derivation must be established and approved.
- **Basis:** The current dispatch carries ModelPayloadDigest `d675d581c80f43e691a31da73ccf17fd4bcc6b00d3a5331f26b9294e294e1538`, but the blocker evidence records no canonical current payload owner or authorized deterministic derivation. The digest therefore does not satisfy the node.

### `LIFECYCLE_TEMPLATE`

- **Classification:** `KNOWN_LEAF_REQUIRES_AUTHORITY`
- **New dependency discovery:** No
- **LLM semantic reasoning required:** No new reasoning; the accepted lifecycle blocker explicitly records that the production consumer lacks an authenticated `WORK-AUTHORIZATION-TEMPLATE-1`.
- **Deterministic evaluation sufficient:** Yes, for distinguishing qualification-only template evidence from production authority.
- **Runtime experimentation required:** No for this leaf evaluation; prior lifecycle qualification is already recorded and is not repeated.
- **External/human authority required:** Yes, for a bounded production template and issuance authority.
- **Basis:** Corrected template/instance/issuance separation and lifecycle boundary tests passed in qualification, but the template remains qualification-only and no production-consumable template is current. It must not be synthesized from the concrete WorkAuthorization or implementation defaults.

### `R3_HISTORY`

- **Classification:** `KNOWN_LEAF_RESOLVED`
- **New dependency discovery:** No
- **LLM semantic reasoning required:** No new reasoning; historical predecessor status is explicitly accepted.
- **Deterministic evaluation sufficient:** Yes, by authenticated R3→R4 ancestry and historical-state checks.
- **Runtime experimentation required:** No
- **External/human authority required:** No new authority for preservation.
- **Basis:** R3 is preserved as the authenticated historical predecessor of R4. It is not current authority and requires no repair, promotion, or replay.

### `RELEASE_BB1808A`

- **Classification:** `KNOWN_LEAF_RESOLVED`
- **New dependency discovery:** No
- **LLM semantic reasoning required:** No new reasoning; forensic provenance is already accepted.
- **Deterministic evaluation sufficient:** Yes, using `BB1808A_HISTORICAL_PROVENANCE.json` and its accepted classification.
- **Runtime experimentation required:** No
- **External/human authority required:** No authority to preserve the classification; a separate prospective release-root decision would be required for current authority, but that is outside this leaf evaluation.
- **Basis:** `bb1808a…` is classified as a qualification/prospective reference promoted into production-facing artifacts without a canonical owner or complete issuance chain. It is preserved and explicitly excluded from current authority.

### `RELEASE_C43F119`

- **Classification:** `KNOWN_LEAF_RESOLVED`
- **New dependency discovery:** No
- **LLM semantic reasoning required:** No new reasoning; its role as last independently established historical Run-2 ancestry is accepted.
- **Deterministic evaluation sufficient:** Yes, for historical identity and scope.
- **Runtime experimentation required:** No
- **External/human authority required:** No new authority for preservation; a prospective current release-root decision remains separately required.
- **Basis:** `c43f119…` is valid historical authenticated release ancestry. It is not current merely because it is the last valid historical release authority.

## Independence and stop behavior

Each node was evaluated against its own local criteria and cited evidence. No node’s classification was used to satisfy another node. No unrepresented prerequisite was discovered during these evaluations, so no `NEW_DEPENDENCY_DISCOVERED` stop occurred.

The authority-required results remain leaves: this experiment did not construct or approve provider/model authority, payload authority, or a lifecycle template. The historical results remain preservation classifications, not current execution permissions.

## Preservation

`R4-final = CURRENT + UNIQUE`; `LIVE_R4_FINAL_CONTROLLER_STORE = G4 CURRENT`; r13 remains `UNISSUED + UNOWNED`; provider/model requests remain zero; E1 effects remain zero. No dependency-model artifact was modified.
