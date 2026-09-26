# E1 budget applicability/freshness reentry 1

The approved representation remains unchanged. REEVAL-BUDGET remains BLOCKED. A missing proof-acquisition route is established in the planner specification only. **FACT-BUDGET-APPLICABILITY is actionable to begin bounded read-only inspection; it has not run and no applicability proposition is newly satisfied.**

## Exact proof obligations

ESTABLISHED_FOR_RECORDED_SOURCE_ONLY means accepted snapshot proof, not current owning-domain applicability. The approved authority identity is `StatusBudgetAuthority-sha256:02cc22de4ad70612c8b1e39e4df6f3bf8733c777d4729fb66d59d519fc6edc99`.

| Proposition | Existing evidence status | Required factual proof | Producer/source | Resolution stages |
|---|---|---|---|
| BUDGET-PROOF-AUTHENTICITY | ESTABLISHED_FOR_RECORDED_SOURCE_ONLY: Recorded issued source provenance and canonical body were authenticated by accepted results; current owning-domain trust/publication remains unqualified. | Issued record plus current trusted owning-domain resolution/validation evidence. | StatusBudgetAuthority issuer / owning authority domain | FACT_ACQUISITION, DETERMINISTIC_VALIDATION |
| BUDGET-PROOF-IDENTITY | ESTABLISHED_FOR_RECORDED_SOURCE_ONLY: Exact authority identity and body hash match accepted record. Any newly retrieved bytes must independently reproduce the same identity and source type. | Canonical body excluding authority_id; exact identity prefix/type and complete required members. | Recorded StatusBudgetAuthority; any current owning source | DETERMINISTIC_VALIDATION |
| BUDGET-PROOF-AVAILABILITY_PUBLICATION | UNRESOLVED: Local issuance bytes exist; current authoritative accessibility/publication and its required publication rule are not established. | Current owning-store resolution/provenance or independently authoritative publication/availability record. If publication is not required, cite governing rule explicitly. | Authority publisher/store owner; exact current locator not established | FACT_ACQUISITION, EXTERNAL_EVIDENCE |
| BUDGET-PROOF-SCOPE | UNRESOLVED: Source is FIRST_PROGRAMMER_EXECUTION; target inventory is FIRST_PROGRAMMER_REQUEST. Similar E1 prefixes do not prove applicability. | Exact target invocation/dispatch/context plus governing applicability rule connecting the two phases, or an explicitly bounded later applicability decision. | Governing scope/phase contract owner; accepted target inventory | FACT_ACQUISITION, DETERMINISTIC_VALIDATION, ARCHITECT_APPLICABILITY_DECISION if no existing rule |
| BUDGET-PROOF-LINEAGE | UNRESOLVED: R4-final CURRENT UNIQUE is a recorded source claim, not proof of current applicable lineage at the target. | Authenticated current lineage/adoption/selection evidence relating source and exact target; no stale successor substitution. | Release/lineage owning authority | FACT_ACQUISITION, DETERMINISTIC_VALIDATION, EXTERNAL_EVIDENCE |
| BUDGET-PROOF-RUNTIME | UNRESOLVED: Source and target inventories name R4 runtime; matching references alone do not qualify applicability. | Independently authenticated applicable runtime selection/content linkage under the governing source contract; verify exact digest and target linkage, without constructing/replacing runtime. | Runtime/release owning source and target invocation/context | FACT_ACQUISITION, DETERMINISTIC_VALIDATION, EXTERNAL_EVIDENCE |
| BUDGET-PROOF-CONTROLLER_STORE_G4 | UNRESOLVED: Recorded G4 identity is available; actual current generation membership/accessibility and source applicability are unproved. | Authenticated store-generation and applicable authority-resolution evidence for exact source and target; no guessed catalog path. | Controller-store generation/authority domain owner | FACT_ACQUISITION, DETERMINISTIC_VALIDATION, EXTERNAL_EVIDENCE |
| BUDGET-PROOF-PROGRAMMER_PROFILE | UNRESOLVED: Source pins a ProgrammerProfile identity; target applicability must be checked independently wherever required by its contract. | Authenticated owning profile and governing target/profile binding; exact identity domain must match. Applicability-not-required needs explicit governing evidence, not omission. | ProgrammerProfile owner and target authority bindings | FACT_ACQUISITION, DETERMINISTIC_VALIDATION, EXTERNAL_EVIDENCE |
| BUDGET-PROOF-TEMPORAL_CURRENTNESS | UNRESOLVED: No accepted proof of current validity, non-supersession or remaining single-use status for exact target is present. A recorded FRESH flag or date is insufficient. | Authoritative current snapshot/event/selection evidence with target identity and applicable revocation/supersession/single-use rules. Pin evidence identity and freshness evaluation rule; reject uncertainty. | Owning authority/store/lifecycle or usage producer under existing governing policy; exact qualified producer not established | FACT_ACQUISITION, DETERMINISTIC_VALIDATION, EXTERNAL_EVIDENCE |
| BUDGET-PROOF-EXECUTION_REQUEST_PHASE | UNRESOLVED: Constructing a reference for a request and exercising execution authority are distinct operations; neither implication is inferred. | Existing phase-specific rule stating whether this execution authority may supply the preconstruction request input, with exclusions and source-use gates; otherwise decision inputs after facts complete. | Governing contract owner | FACT_ACQUISITION, DETERMINISTIC_VALIDATION, ARCHITECT_APPLICABILITY_DECISION if required |

## Source existence and external boundary

The named issuance, invocation, dispatch, release, context and binding artifacts exist as static records. Current qualified publication, revocation/supersession, single-use/currentness and scope-bridge evidence is not established by the accepted corpus. Whether it exists elsewhere or is merely unrepresented is UNKNOWN for each unresolved row; this task does not search for it. Expected producers are roles, not assertions that a qualified concrete producer exists.

The JSON companion has per-obligation existence, unrepresented-evidence, effect and external-action fields. Read-only access to existing evidence is non-effecting. If the named corpus cannot establish a proposition, the action must return the exact missing-input gate. Creating, refreshing, publishing or renewing evidence is not authorized acquisition. No new TTL, date cutoff, scope equivalence or non-revocation claim is invented. `ResolvedAuthorityValue.from_bytes` defaults to a FRESH label; that helper label alone is not independently sourced temporal evidence and must not satisfy the proof row. No resolver was invoked.

## Why the specification needs a route

REEVAL-BUDGET persists REEVAL-BUDGET-CURRENT-APPLICABILITY, but no resolution_action receives/validates its evidence. Existing six fact-receipt routes cover different cut members and omit budget; MAP-BUDGET cannot substitute for proof acquisition.

The new action consumes the accepted BLOCKED outcome as knowledge and the issued DEC-BUDGET record as a prerequisite. The six existing fact-receipt routes remain unchanged. It does not require its missing proof as a prerequisite to beginning a bounded evidence attempt; it does require the complete proof to PASS. There is no automatic retry or reopening of a historical action.

Permitted first-attempt scope: only the exact files and byte identities listed below. No recursive store/repository discovery, guessed catalog paths, writes or service operations. Current producer/store locators are not invented. New external evidence needs a separately accepted exact source manifest before a later attempt can read it.

## Fact versus authority and deterministic outcomes

- PASS: Every required proposition independently verified (or inapplicability of a check proved by governing rule) for exact subject/source. Emit hash-bound evidence matrix and proof receipt. Enable one new REEVAL-BUDGET attempt overlay; do not mark prior attempt PASS or execute mapping.
- FAIL: Evidence proves a named incompatibility/staleness/invalid identity; record exact failed proposition and evidence. No reentry PASS.
- BLOCKED: Required concrete facts/rule inputs absent: retain named external gate and stop. No missing input invented.
- EXTERNAL_GATE_REQUIRED: Existing evidence is outside permitted/retrievable corpus: record exact required producer/locator/evidence and stop, with no acquisition effect.
- AUTHORITY_REQUIRED: Technical facts complete but existing scope/phase rule does not authorize applicability. Record separate bounded decision-input requirement; no implied grant or ready decision.

Technical compatibility does not grant normative applicability. Existing governing rule may establish it deterministically only with exact evidence. Otherwise complete facts -> bounded dossier -> independent readiness -> explicit Architect applicability decision -> accepted record -> REEVAL-BUDGET. No ready decision or grant is created now.

NEW_AUTHORITY is a separate conditional branch only if a qualified existing authority cannot govern and an external owner determines replacement/renewal is required. Never silently renew, widen, republish or change this authority; stop for separately scoped work. Not currently proven necessary.

Technical source equality and governance permission are distinct stages. FACT_ACQUISITION obtains evidence; DETERMINISTIC_VALIDATION tests existing rules; ARCHITECT_APPLICABILITY_DECISION is conditional on no existing rule after facts complete; EXTERNAL_EVIDENCE is a missing-input gate; NEW_AUTHORITY is a separate unproven future need. Neither missing technical facts nor unknown source availability can be supplied by human preference.

## Reentry and failure preservation

Accepted full PASS proof -> one new REEVAL-BUDGET attempt. The evidence receipt must identify the source/target, exact proof matrix, governing rule and snapshot provenance; source changes stale the proof. A new attempt overlay can discharge only REEVAL-BUDGET-CURRENT-APPLICABILITY, never rewrite the historical BLOCKED result. Partial, negative or missing evidence cannot enable a PASS. If normative applicability requires a decision: complete facts -> bounded decision dossier -> independent readiness gate -> explicit Architect decision -> authenticated record -> REEVAL-BUDGET. No such dossier or decision is created now.

MAP-BUDGET remains separately gated by accepted REEVAL-BUDGET and CONTRACT-T1. The approved reference shape, bounds and controls remain unchanged.

## Supported generalization

AUTHORITY_REFERENCE does not imply CURRENT_APPLICABILITY / FRESHNESS. WP-03 runtime-head publication/currentness, WP-04 supervisor stale bindings, applicable specific approval and WP-06 audit-source gaps support requiring explicit applicability/freshness proof routes for authority-reference mappings generally. No other route, field or blocker is repaired here.

## Current actionability

The named initial files exist and the accepted decision/blocked-result prerequisites match. This supports beginning one bounded new action, not confidence that it will succeed. If only historical references are available, it stops at the explicit external gate. Replay yields ACTIONABLE = [FACT-BUDGET-APPLICABILITY]. The existing selector returns that singleton at entry (Criterion 0); no policy ranking change is needed. It was not executed.

63 actions now: 13 completed, 49 blocked, 1 actionable. Current execution-history results and root/slot states are unchanged; previous static wave counts remain baseline projections. The current specification replay governs scheduling.

## Source manifest

- `docs/experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_REEVAL_BUDGET_1_RESULT.md` — SHA-256 `8692f4214410724921e0b1c346b2dfc37c2ae95d0bf2d8cad71949972a130b59` — whole artifact; authority fields /scope /lineage /runtime /controller_store /programmer_profile and exact source selector where applicable.
- `docs/experiments/E1/E1_TEMPLATE1_ARCHITECT_DEC_BUDGET_AUTHORITY_1.json` — SHA-256 `2439eeb699057196323ed5373dc72082c4a7210d745713995a9c3e2fd494e1f4` — whole artifact; authority fields /scope /lineage /runtime /controller_store /programmer_profile and exact source selector where applicable.
- `docs/experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_INPUT_BUDGET_1_DOSSIER.json` — SHA-256 `50ba6151aaa86c5e62f5f26e8960e4bad902009e82b8d5aa2e16d6583d356957` — whole artifact; authority fields /scope /lineage /runtime /controller_store /programmer_profile and exact source selector where applicable.
- `docs/experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_S_BINDING_1_RESULT.md` — SHA-256 `829ecbd2bba6cbf4cb0c45c8886f80097c754db11d607a296840714569f465b7` — whole artifact; authority fields /scope /lineage /runtime /controller_store /programmer_profile and exact source selector where applicable.
- `docs/experiments/E1/E1_HOST_PREREQUISITE_AUTHORITY_ISSUANCE_1.md` — SHA-256 `5cf24bf05643e69543a9db154af7e2a6edc1943fe32280ea7d7762b06a43132f` — whole artifact; authority fields /scope /lineage /runtime /controller_store /programmer_profile and exact source selector where applicable.
- `docs/experiments/E1/E1_INVOCATION_CANDIDATE_1.json` — SHA-256 `c0fdde77ba3dddd1fcaecc798b5a7252e5b333238063aec750bbaa522ede7c6a` — whole artifact; authority fields /scope /lineage /runtime /controller_store /programmer_profile and exact source selector where applicable.
- `docs/experiments/E1/E1_CURRENT_DISPATCH_1.json` — SHA-256 `475861a32de000a8527074748bfbaaf8b0b0efa6e405e9a3f9a0a1f27dfc7b35` — whole artifact; authority fields /scope /lineage /runtime /controller_store /programmer_profile and exact source selector where applicable.
- `docs/experiments/E1/E1_CURRENT_RELEASE_AUTHORITY_1.json` — SHA-256 `66f7834aaf9d0b3e5b569e5b9865781340e6e3e7da8420557f09ff65c7fbd991` — whole artifact; authority fields /scope /lineage /runtime /controller_store /programmer_profile and exact source selector where applicable.
- `docs/experiments/E1/E1_OPERATIONAL_CONTEXT_1.json` — SHA-256 `3450887d8821a9bc53446499e4bbb2ef5fc1e94acdf830e5d03488a6fe25ef9b` — whole artifact; authority fields /scope /lineage /runtime /controller_store /programmer_profile and exact source selector where applicable.
- `docs/experiments/E1/E1_OPERATIONAL_BINDING_1.json` — SHA-256 `e07ed04a43a2345108662d878537d6698457c6c6c7dc549047b1c1773b0fe173` — whole artifact; authority fields /scope /lineage /runtime /controller_store /programmer_profile and exact source selector where applicable.
- `docs/experiments/E1/E1_WORKAUTHORIZATION_PRODUCTION_CONTRACT_DECISION_1.md` — SHA-256 `b916edc33d1534b516a187118146364c88aa360f0c8ff4f2dcc91a205aca1ad6` — whole artifact; authority fields /scope /lineage /runtime /controller_store /programmer_profile and exact source selector where applicable.
- `docs/experiments/E1/E1_DECISION_INPUT_REENTRY_SEMANTICS_1.md` — SHA-256 `52827b823847a66266322c86818ae62826f761e30954f179e8282f96d79a5367` — whole artifact; authority fields /scope /lineage /runtime /controller_store /programmer_profile and exact source selector where applicable.
- `adapter/authority_resolution.py` — SHA-256 `62bbf793ae1b714b4d3156d764a61762aaa124bd804a37a3123a6d15d1a79acc` — ResolvedAuthorityValue.from_bytes default freshness and compose_activation_inputs; interface semantics only, no call executed.

Only planner specification JSON/MD and these two new analysis artifacts change. No graph/authority/implementation/lifecycle state changes. Source identities here bind inspection scope, not substantive currentness proofs.

```text
BUDGET_REPRESENTATION = APPROVED_OPTION_A_AUTHORITY_REFERENCE
REEVAL_BUDGET = BLOCKED
UNRESOLVED_PROOF_OBLIGATIONS = ["BUDGET-PROOF-AVAILABILITY_PUBLICATION", "BUDGET-PROOF-SCOPE", "BUDGET-PROOF-LINEAGE", "BUDGET-PROOF-RUNTIME", "BUDGET-PROOF-CONTROLLER_STORE_G4", "BUDGET-PROOF-PROGRAMMER_PROFILE", "BUDGET-PROOF-TEMPORAL_CURRENTNESS", "BUDGET-PROOF-EXECUTION_REQUEST_PHASE"]
REENTRY_ROUTE = ["FACT-BUDGET-APPLICABILITY", "accepted complete proof or explicit external/authority gate", "REEVAL-BUDGET new attempt only after proof acceptance"]
NEW_PLANNER_RULE_REQUIRED = YES
ACTIONABLE = ["FACT-BUDGET-APPLICABILITY"]
NEXT_ACTION = FACT-BUDGET-APPLICABILITY
DECIDING_CRITERION = SINGLETON_AT_ENTRY (0)
ROOT_CONDITIONS_RESOLVED = 0
ROOT_CONDITIONS_REMAINING = 27
SLOTS_RESOLVED = 0
SLOTS_REMAINING = 41
TEMPLATE1_CONSTRUCTION_READY = NO
CANDIDATE3_RESUMPTION_READY = NO
PRODUCTION_EFFECT = NO
```
