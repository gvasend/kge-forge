# E1 external handoff package 1

**GLOBAL_CONTROL_STATE = MIXED_WAIT. E1_RESUME_ALLOWED = NO.** Eight scoped requests identify the external inputs needed before any bounded reentry can become eligible. No request is sent and no receipt, fact acquisition, decision or construction runs.

## Consolidation and owner limits

One handoff package contains eight independently scoped bundles. No concrete common qualified producer is established, so cross-branch obligations are not merged. A producer may respond once with several request IDs only if its authenticated competence and evidence satisfy each independently. Shared R4/G4 identifiers do not establish shared authority. The implementation owner/selector pair is one coherent source-contract request; budget uses its existing eight-proof evidence contract. No new publication or authority is requested as a substitute for missing evidence.

## Normalized requests

### E1-EXTERNAL-REQUEST-BUDGET-1

- **Handoff / type:** HANDOFF-BUDGET / EXTERNAL_EVIDENCE_REQUEST.
- **Frontier:** EXT-BUDGET-APPLICABILITY-EVIDENCE.
- **Blocked root:** root:budget.
- **Missing proposition / acceptable source:** The full eight-proposition contract in E1_BUDGET_APPLICABILITY_EXTERNAL_EVIDENCE_REQUEST_1.json is incorporated unchanged.
- **Expected owner:** Owning authority/catalog, lineage/runtime/profile/current-state and governing phase-rule owners; concrete qualified endpoints UNKNOWN.
- **Authentication:** Supply exact source bytes or explicitly admitted retrievable locator, raw hash, semantic identity/domain and canonicalization rule. Verify identity and producer competence via existing trusted owning-domain chain/rules. Self-hash, wrapper signature, prose or copied references alone are insufficient.
- **Freshness/currentness:** Bind evidence to exact target and coherent owning snapshot/generation with governing effective/currentness rule and trusted anchor. Reject stale/inapplicable/ambiguous evidence; no arbitrary TTL or currentness inference from static identity.
- **Scope/lineage:** Exact R4/G4/E1-WP-001 invocation/dispatch/release/context envelope pinned in resume subject; preserve source-specific scopes. Do not equate EXECUTION with REQUEST or substitute historical releases/contexts.
- **Receipt:** RECEIVE-BUDGET-APPLICABILITY-EVIDENCE.
- **Reentry:** FACT-BUDGET-APPLICABILITY -> REEVAL-BUDGET.
- **Downstream blocked actions (not unlocked automatically):** BUILD-BINDING, BUILD-EXECUTION_PROFILE, CHECK-READINESS, CONTRACT-T1, DEC-INTERFACES, IMPL-CONTEXT, IMPL-GOVERNANCE, IMPL-TRANSMISSION, IMPL-VALIDATOR, MAP-ANCESTRY, MAP-APPROVAL, MAP-ARGV, MAP-AUDIT, MAP-BUDGET, MAP-CONTEXT_ID, MAP-CONTEXT_PROJECTION, MAP-DISPATCH, MAP-ELIGIBILITY, MAP-EXEC_BINS, MAP-IGNORED, MAP-IMPLEMENTATION, MAP-LIFECYCLE, MAP-PATHS, MAP-PAYLOAD, MAP-RELEASE, MAP-RETENTION, MAP-RUNTIME, MAP-RUNTIME_HEAD, MAP-SHELL_NETWORK, MAP-SUCCESSION, MAP-SUPERVISOR, MAP-TRANSPORT, REEVAL-BUDGET, S-ELIGIBILITY, S-SUCCESSION.
- **Evidence:** `docs/experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_FACT_BUDGET_APPLICABILITY_1_RESULT.md`, SHA-256 `6b3f486f72b1beeca3ae3a2beb6b1a3e5156f4d85ee35068bf5f6cb1f0d46b2d`.

The [budget external evidence contract](E1_BUDGET_APPLICABILITY_EXTERNAL_EVIDENCE_REQUEST_1.md) is normative: all eight current-proof obligations and producer/current-anchor requirements remain intact.

### E1-EXTERNAL-REQUEST-ANCESTRY-1

- **Handoff / type:** HANDOFF-ANCESTRY / EXTERNAL_EVIDENCE_REQUEST.
- **Frontier:** EXT-REENTRY-S-ANCESTRY.
- **Blocked root:** root:ancestry.
- **Missing proposition / acceptable source:** Exact current allocation record, predecessor/attempt-chain source and concrete session/turn ownership for pinned invocation; complete identity, chronology and owning provenance. R12_HISTORY or R13_NAMESPACE strings alone are not records.
- **Expected owner:** Authoritative invocation allocator/history/session-turn owner; concrete source not established.
- **Authentication:** Supply exact source bytes or explicitly admitted retrievable locator, raw hash, semantic identity/domain and canonicalization rule. Verify identity and producer competence via existing trusted owning-domain chain/rules. Self-hash, wrapper signature, prose or copied references alone are insufficient.
- **Freshness/currentness:** Bind evidence to exact target and coherent owning snapshot/generation with governing effective/currentness rule and trusted anchor. Reject stale/inapplicable/ambiguous evidence; no arbitrary TTL or currentness inference from static identity.
- **Scope/lineage:** Exact R4/G4/E1-WP-001 invocation/dispatch/release/context envelope pinned in resume subject; preserve source-specific scopes. Do not equate EXECUTION with REQUEST or substitute historical releases/contexts.
- **Receipt:** RECEIVE-ANCESTRY-EVIDENCE.
- **Reentry:** S-ANCESTRY.
- **Downstream blocked actions (not unlocked automatically):** BUILD-BINDING, BUILD-EXECUTION_PROFILE, CHECK-READINESS, MAP-ANCESTRY, MAP-ELIGIBILITY, S-ELIGIBILITY.
- **Evidence:** `docs/experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_S_ANCESTRY_1_RESULT.md`, SHA-256 `09a9f1279ef9e4c4dc8c397c7460295385f619bef1572de01e7764e33032181f`.

### E1-EXTERNAL-REQUEST-APPROVAL-1

- **Handoff / type:** HANDOFF-APPROVAL / EXTERNAL_EVIDENCE_REQUEST.
- **Frontier:** EXT-REENTRY-S-APPROVAL.
- **Blocked root:** root:approval.
- **Missing proposition / acceptable source:** Existing issued specific-approval record with exact decision identity and target applicability/lineage/freshness. Do not substitute another grant or request a new approval to fill a missing fact. If absent, report absence.
- **Expected owner:** Owning specific-approval issuer/domain; concrete applicable record not established.
- **Authentication:** Supply exact source bytes or explicitly admitted retrievable locator, raw hash, semantic identity/domain and canonicalization rule. Verify identity and producer competence via existing trusted owning-domain chain/rules. Self-hash, wrapper signature, prose or copied references alone are insufficient.
- **Freshness/currentness:** Bind evidence to exact target and coherent owning snapshot/generation with governing effective/currentness rule and trusted anchor. Reject stale/inapplicable/ambiguous evidence; no arbitrary TTL or currentness inference from static identity.
- **Scope/lineage:** Exact R4/G4/E1-WP-001 invocation/dispatch/release/context envelope pinned in resume subject; preserve source-specific scopes. Do not equate EXECUTION with REQUEST or substitute historical releases/contexts.
- **Receipt:** RECEIVE-APPROVAL-EVIDENCE.
- **Reentry:** S-APPROVAL.
- **Downstream blocked actions (not unlocked automatically):** CHECK-READINESS, MAP-APPROVAL.
- **Evidence:** `docs/experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_S_APPROVAL_1_RESULT.md`, SHA-256 `4b896d8522ab08c4926dc2fe3e3889a9ff5dd499ab193f3e65fe719b5345d850`.

### E1-EXTERNAL-REQUEST-AUDIT-1

- **Handoff / type:** HANDOFF-AUDIT / EXTERNAL_SOURCE_IDENTIFICATION.
- **Frontier:** EXT-REENTRY-PREP-AUDIT.
- **Blocked root:** root:audit.
- **Missing proposition / acceptable source:** Concrete proposed namespace/store identity and owning source, exact location plus independently evidenced placement outside agent roots, target release/context applicability. Supplying a candidate target does not select/authorize it or create a ledger.
- **Expected owner:** Audit namespace/store owner; exact competent producer and target UNKNOWN.
- **Authentication:** Supply exact source bytes or explicitly admitted retrievable locator, raw hash, semantic identity/domain and canonicalization rule. Verify identity and producer competence via existing trusted owning-domain chain/rules. Self-hash, wrapper signature, prose or copied references alone are insufficient.
- **Freshness/currentness:** Bind evidence to exact target and coherent owning snapshot/generation with governing effective/currentness rule and trusted anchor. Reject stale/inapplicable/ambiguous evidence; no arbitrary TTL or currentness inference from static identity.
- **Scope/lineage:** Exact R4/G4/E1-WP-001 invocation/dispatch/release/context envelope pinned in resume subject; preserve source-specific scopes. Do not equate EXECUTION with REQUEST or substitute historical releases/contexts.
- **Receipt:** RECEIVE-AUDIT-SOURCE-EVIDENCE.
- **Reentry:** PREP-AUDIT.
- **Downstream blocked actions (not unlocked automatically):** CHECK-READINESS, DEC-AUDIT, MAP-AUDIT.
- **Evidence:** `docs/experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_PREP_AUDIT_1_RESULT.md`, SHA-256 `48bd8c492aa1cbf7cd8b3b7ee31b75e85488dca7ddbf0082965aa1fc44b3dfb1`.

### E1-EXTERNAL-REQUEST-RUNTIME-HEAD-1

- **Handoff / type:** HANDOFF-RUNTIME-HEAD / EXTERNAL_SELECTOR.
- **Frontier:** EXT-REENTRY-PREP-RUNTIME_HEAD.
- **Blocked root:** root:runtime_head.
- **Missing proposition / acceptable source:** Concrete proposed current R4/G4 head selector and source authority body/identity, exact publication target/domain/mechanism and current release/context/lineage facts. Distinguish already-published authority from a proposal; no R3 or unpublished R4 substitution.
- **Expected owner:** Runtime-head selection/release authority and owning catalog publisher; concrete current selector UNKNOWN.
- **Authentication:** Supply exact source bytes or explicitly admitted retrievable locator, raw hash, semantic identity/domain and canonicalization rule. Verify identity and producer competence via existing trusted owning-domain chain/rules. Self-hash, wrapper signature, prose or copied references alone are insufficient.
- **Freshness/currentness:** Bind evidence to exact target and coherent owning snapshot/generation with governing effective/currentness rule and trusted anchor. Reject stale/inapplicable/ambiguous evidence; no arbitrary TTL or currentness inference from static identity.
- **Scope/lineage:** Exact R4/G4/E1-WP-001 invocation/dispatch/release/context envelope pinned in resume subject; preserve source-specific scopes. Do not equate EXECUTION with REQUEST or substitute historical releases/contexts.
- **Receipt:** RECEIVE-RUNTIME-HEAD-EVIDENCE.
- **Reentry:** PREP-RUNTIME_HEAD.
- **Downstream blocked actions (not unlocked automatically):** CHECK-READINESS, DEC-RUNTIME_HEAD, MAP-RUNTIME_HEAD.
- **Evidence:** `docs/experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_PREP_RUNTIME_HEAD_1_RESULT.md`, SHA-256 `6ebfe3a8f57ba309cc810fdb27610ad14ee6b048f2a5f989a05e61338b094897`.

### E1-EXTERNAL-REQUEST-SUPERVISOR-1

- **Handoff / type:** HANDOFF-SUPERVISOR / EXTERNAL_SELECTOR.
- **Frontier:** EXT-REENTRY-PREP-SUPERVISOR.
- **Blocked root:** root:supervisor.
- **Missing proposition / acceptable source:** Concrete proposed supervisor selector and supporting owning authority/selection facts for exact current release/context, lineage and freshness. Immutable stale instances cannot be rebound by response or copied runtime identity.
- **Expected owner:** Supervisor selection/release owner; concrete current selection UNKNOWN.
- **Authentication:** Supply exact source bytes or explicitly admitted retrievable locator, raw hash, semantic identity/domain and canonicalization rule. Verify identity and producer competence via existing trusted owning-domain chain/rules. Self-hash, wrapper signature, prose or copied references alone are insufficient.
- **Freshness/currentness:** Bind evidence to exact target and coherent owning snapshot/generation with governing effective/currentness rule and trusted anchor. Reject stale/inapplicable/ambiguous evidence; no arbitrary TTL or currentness inference from static identity.
- **Scope/lineage:** Exact R4/G4/E1-WP-001 invocation/dispatch/release/context envelope pinned in resume subject; preserve source-specific scopes. Do not equate EXECUTION with REQUEST or substitute historical releases/contexts.
- **Receipt:** RECEIVE-SUPERVISOR-EVIDENCE.
- **Reentry:** PREP-SUPERVISOR.
- **Downstream blocked actions (not unlocked automatically):** CHECK-READINESS, DEC-SUPERVISOR, MAP-SUCCESSION, MAP-SUPERVISOR, S-SUCCESSION.
- **Evidence:** `docs/experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_PREP_SUPERVISOR_1_RESULT.md`, SHA-256 `1c1d280b85a3a92e36780776af96c9287a9212780c3fa9a7eff7f4c2e48a7a7e`.

### E1-EXTERNAL-REQUEST-EXEC-1

- **Handoff / type:** HANDOFF-EXEC / EXTERNAL_POLICY_SOURCE.
- **Frontier:** EXT-REENTRY-DEC-EXEC.
- **Blocked root:** root:exec_bins.
- **Missing proposition / acceptable source:** Existing independently authoritative executable-policy source and exact projector, or exact independently grounded permission proposal with source/scope/semantics/consequences. No executable permissions inferred from argv; proposal is not granted policy.
- **Expected owner:** Independent executable-policy owner/proposal producer; not established by argv/profile inventory.
- **Authentication:** Supply exact source bytes or explicitly admitted retrievable locator, raw hash, semantic identity/domain and canonicalization rule. Verify identity and producer competence via existing trusted owning-domain chain/rules. Self-hash, wrapper signature, prose or copied references alone are insufficient.
- **Freshness/currentness:** Bind evidence to exact target and coherent owning snapshot/generation with governing effective/currentness rule and trusted anchor. Reject stale/inapplicable/ambiguous evidence; no arbitrary TTL or currentness inference from static identity.
- **Scope/lineage:** Exact R4/G4/E1-WP-001 invocation/dispatch/release/context envelope pinned in resume subject; preserve source-specific scopes. Do not equate EXECUTION with REQUEST or substitute historical releases/contexts.
- **Receipt:** RECEIVE-EXEC-POLICY-EVIDENCE.
- **Reentry:** DEC-EXEC readiness reevaluation.
- **Downstream blocked actions (not unlocked automatically):** BUILD-BINDING, BUILD-EXECUTION_PROFILE, CHECK-READINESS, CONTRACT-T1, IMPL-CONTEXT, IMPL-GOVERNANCE, IMPL-TRANSMISSION, IMPL-VALIDATOR, MAP-ANCESTRY, MAP-APPROVAL, MAP-ARGV, MAP-AUDIT, MAP-BUDGET, MAP-CONTEXT_ID, MAP-CONTEXT_PROJECTION, MAP-DISPATCH, MAP-ELIGIBILITY, MAP-EXEC_BINS, MAP-IGNORED, MAP-IMPLEMENTATION, MAP-LIFECYCLE, MAP-PATHS, MAP-PAYLOAD, MAP-RELEASE, MAP-RETENTION, MAP-RUNTIME, MAP-RUNTIME_HEAD, MAP-SHELL_NETWORK, MAP-SUCCESSION, MAP-SUPERVISOR, MAP-TRANSPORT, S-ELIGIBILITY, S-SUCCESSION.
- **Evidence:** `docs/experiments/E1/E1_TEMPLATE1_ARCHITECT_DECISION_BATCH_1.json`, SHA-256 `c00c4cf3553cd4f0b372e34cd1d79958b8a398dedf5aa804b589c9ee7570f1c9`.

### E1-EXTERNAL-REQUEST-IMPLEMENTATION-1

- **Handoff / type:** HANDOFF-IMPLEMENTATION / EXTERNAL_SOURCE_IDENTIFICATION.
- **Frontier:** IMPLEMENTATION-OWNING-SOURCE + IMPLEMENTATION-SELECTOR.
- **Blocked root:** root:implementation.
- **Missing proposition / acceptable source:** Provide the actual authoritative identity-domain object/contract, owning record/identity, exact canonical byte domain/serialization/hash or reference rule, source field/path/selector, target scope/lineage and supported runtime relationship. An unadopted proposal must be labeled; it is not an authoritative object.
- **Expected owner:** Implementation identity-domain contract owner/source producer; concrete distinct-domain owner UNKNOWN.
- **Authentication:** Supply exact source bytes or explicitly admitted retrievable locator, raw hash, semantic identity/domain and canonicalization rule. Verify identity and producer competence via existing trusted owning-domain chain/rules. Self-hash, wrapper signature, prose or copied references alone are insufficient.
- **Freshness/currentness:** Bind evidence to exact target and coherent owning snapshot/generation with governing effective/currentness rule and trusted anchor. Reject stale/inapplicable/ambiguous evidence; no arbitrary TTL or currentness inference from static identity.
- **Scope/lineage:** Exact R4/G4/E1-WP-001 invocation/dispatch/release/context envelope pinned in resume subject; preserve source-specific scopes. Do not equate EXECUTION with REQUEST or substitute historical releases/contexts.
- **Receipt:** RECEIVE-IMPLEMENTATION-SOURCE-EVIDENCE.
- **Reentry:** INPUT-IMPLEMENTATION.
- **Downstream blocked actions (not unlocked automatically):** BUILD-BINDING, BUILD-EXECUTION_PROFILE, CHECK-READINESS, CONTRACT-T1, DEC-IMPLEMENTATION, DEC-INTERFACES, IMPL-CONTEXT, IMPL-GOVERNANCE, IMPL-TRANSMISSION, IMPL-VALIDATOR, MAP-ANCESTRY, MAP-APPROVAL, MAP-ARGV, MAP-AUDIT, MAP-BUDGET, MAP-CONTEXT_ID, MAP-CONTEXT_PROJECTION, MAP-DISPATCH, MAP-ELIGIBILITY, MAP-EXEC_BINS, MAP-IGNORED, MAP-IMPLEMENTATION, MAP-LIFECYCLE, MAP-PATHS, MAP-PAYLOAD, MAP-RELEASE, MAP-RETENTION, MAP-RUNTIME, MAP-RUNTIME_HEAD, MAP-SHELL_NETWORK, MAP-SUCCESSION, MAP-SUPERVISOR, MAP-TRANSPORT, REEVAL-IMPLEMENTATION, S-ELIGIBILITY, S-SUCCESSION.
- **Evidence:** `docs/experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_INPUT_IMPLEMENTATION_1_RESULT.md`, SHA-256 `a1000808e24e1a5193a79023d9f23384c03e343cb4be308273401ca4ccd97205`.

Do not select runtime-digest equivalence. Identify the distinct domain and owning source with qualified selector. Any claimed relationship to runtime must have explicit existing governing proof; otherwise mark UNKNOWN and retain it as a future decision input. Runtime reference/another adapter path is not a substitute.

The response must identify the actual object/contract rather than invent a schema to fill missing values. Its source selector must state exact source fields, canonical bytes/identity algorithm, provenance and applicability. Qualified equality, distinctness or a transformation relative to runtime must cite governing evidence; otherwise preserve the relationship as unknown. Receipt only enables INPUT-IMPLEMENTATION to prepare its complete decision dossier, not DEC-IMPLEMENTATION approval.

## Receipt contracts

Every named receipt contract is deterministic and non-effecting except authorized local evidence/provenance recording. No receipt is currently actionable because no submission is present. Each requires an admitted exact manifest, producer competence proof, exact byte/semantic identities and governing validation rules. No guessed endpoint, unsolicited external request or recursive source hunt is permitted.

For each bundle: receive -> authenticate -> validate its exact factual/scope/lineage/currentness propositions -> retain a per-proposition acceptance matrix -> record only supported assertions. Reject malformed, untrusted, stale or inapplicable responses. Preserve authenticated negative facts and explicit unknowns; do not repair or grant applicability. Partial data cannot close a whole request. Source changes stale dependent assertions.

Budget accepted full proof permits FACT-BUDGET-APPLICABILITY revalidation; only its accepted full proof permits REEVAL-BUDGET. Ancestry and approval evidence permit their named new bounded attempts. Audit/runtime-head/supervisor facts permit preparation reentry only; their Architect decisions still need complete dossiers and separate approval. Executable evidence permits DEC-EXEC readiness reevaluation only, not a decision or permission inference. Implementation source/selector evidence permits INPUT-IMPLEMENTATION reentry only.

Receipt identifiers here are specifications, not added executable planner nodes. Future evidence handling must explicitly invoke these contracts and append accepted-receipt/attempt records. Original historical blocked outcomes remain immutable.

## Resume manifest and rule

The [resume manifest](E1_RESUME_MANIFEST_1.json) pins current graph and plan file hashes, execution_history and execution_state canonical identities, policy/reentry artifacts, eight request/receipt/reentry routes, all action partitions and current authority evidence. It identifies the Candidate-3 authority without consuming it.

E1_RESUME_ALLOWED becomes true only when at least one authenticated accepted bundle supplies sufficient evidence to make its reentry eligible under all remaining gates. Unrelated or partial input cannot resume E1. Human-only readiness permits review handoff, not automatic decision execution.

Resume sequence:
1. Verify resume manifest identities against persisted files; mismatch fails closed and requires new global snapshot/recomputation, not old assertions.
2. Receive only admitted requested evidence; authenticate/validate with bundle contract.
3. Commit supported graph assertions with exact provenance; preserve historical outcomes.
4. Reevaluate affected branch only against original acceptance gates; append attempt overlays rather than overwrite blocked history.
5. Recompute global actionability and all independent authority/effect gates.
6. Apply validated deterministic selector; if only decision-ready human actions remain, use human handoff without automatic Architect execution.
7. Continue normal planner protocol only under task authorization; never consume Candidate-3 authority or execute downstream work implicitly.

## State preservation

Candidate-3 authority remains VALID_UNCONSUMED as recorded in the authoritative persisted state. Its record identity is independently recomputed; this status is not a fresh live issuance/lifecycle qualification. No current authority is broadened. No root or slot is resolved. Only these three handoff artifacts are created. Stop awaiting accepted external evidence.

```text
GLOBAL_CONTROL_STATE = MIXED_WAIT
EXTERNAL_REQUEST_BUNDLES = ["E1-EXTERNAL-REQUEST-BUDGET-1", "E1-EXTERNAL-REQUEST-ANCESTRY-1", "E1-EXTERNAL-REQUEST-APPROVAL-1", "E1-EXTERNAL-REQUEST-AUDIT-1", "E1-EXTERNAL-REQUEST-RUNTIME-HEAD-1", "E1-EXTERNAL-REQUEST-SUPERVISOR-1", "E1-EXTERNAL-REQUEST-EXEC-1", "E1-EXTERNAL-REQUEST-IMPLEMENTATION-1"]
RECEIPT_ACTIONS = ["RECEIVE-BUDGET-APPLICABILITY-EVIDENCE", "RECEIVE-ANCESTRY-EVIDENCE", "RECEIVE-APPROVAL-EVIDENCE", "RECEIVE-AUDIT-SOURCE-EVIDENCE", "RECEIVE-RUNTIME-HEAD-EVIDENCE", "RECEIVE-SUPERVISOR-EVIDENCE", "RECEIVE-EXEC-POLICY-EVIDENCE", "RECEIVE-IMPLEMENTATION-SOURCE-EVIDENCE"]
REENTRY_ACTIONS = ["FACT-BUDGET-APPLICABILITY", "REEVAL-BUDGET", "S-ANCESTRY", "S-APPROVAL", "PREP-AUDIT", "PREP-RUNTIME_HEAD", "PREP-SUPERVISOR", "DEC-EXEC readiness reevaluation", "INPUT-IMPLEMENTATION"]
E1_RESUME_ALLOWED = NO
RUNNABLE_INTERNAL_ACTIONS = []
DECISION_READY_ACTIONS = []
ROOT_CONDITIONS_REMAINING = 27
SLOTS_REMAINING = 41
CANDIDATE3_AUTHORITY_STATUS = VALID_UNCONSUMED
PRODUCTION_EFFECT = NO
```
