# CE-02 bridge projection gap closure 1

**Result: PARTIAL. BR-04 is closed for the bounded O08/O09 documentary routes. BR-01, BR-02, BR-03 and BR-05 remain open. CE-02 is not closed and C06A-3 retry is not allowed.**

This specification adds three executable source-document-to-proof projections. It does not complete the requested nine-class bridge. In particular, no full-source action/history/graph projection is qualified by the partial composition checks below. No implementation, operational registry, existing admission predicate, historical result or frozen E1 artifact is changed.

## Governing inputs and reproducibility

The governing inputs remain the [CE-02 analysis](DETERMINISTIC_PLANNER_V0_1_CE02_SOURCE_PROFILE_BRIDGE_1.md), [complete source inventory](DETERMINISTIC_PLANNER_V0_1_CE02_SOURCE_PROFILE_BRIDGE_1_SOURCE_CLASSES.json), [assigned selector inventory](DETERMINISTIC_PLANNER_V0_1_CE02_SOURCE_PROFILE_BRIDGE_1_PROJECTIONS.json), [preflight closure](DETERMINISTIC_PLANNER_V0_1_C06A_3_PREFLIGHT_CLOSURE_1.md), [CE-01 reconciliation](DETERMINISTIC_PLANNER_V0_1_CE01_CONTRACT_RECONCILIATION_1.md), and [remaining-contract scope](DETERMINISTIC_PLANNER_V0_1_C06A_REMAINING_CONTRACT_1.md).

New companions:

- [Mappings and executable documentary projection](DETERMINISTIC_PLANNER_V0_1_CE02_BRIDGE_GAP_CLOSURE_1_MAPPINGS.json): pinned governing inputs, identity rules, 225 candidate leaf-field ownership records, pure projection program.
- [Explicit joins](DETERMINISTIC_PLANNER_V0_1_CE02_BRIDGE_GAP_CLOSURE_1_JOINS.json): join keys, domains, scope, lineage, currentness and ambiguity rules.
- [Source-shaped qualification fixtures](DETERMINISTIC_PLANNER_V0_1_CE02_BRIDGE_GAP_CLOSURE_1_FIXTURES.json): explicit source locators and pins, independent governing profiles and qualification validity inputs. Source bytes are loaded only from those explicit inputs; there is no discovery search.
- [Validation and executable runner](DETERMINISTIC_PLANNER_V0_1_CE02_BRIDGE_GAP_CLOSURE_1_VALIDATION.json): positive/negative verdicts, rejection stages, invalidation cases and bounded composition results. `reference_validation_program` reruns these checks from the repository root without modifying files.
- [Complete artifact/class preflight](DETERMINISTIC_PLANNER_V0_1_CE02_BRIDGE_GAP_CLOSURE_1_PREFLIGHT.json): all 16 artifact identities, nine classes, remaining target-field obligations and gate decisions.

The projection takes an independently accepted existing profile as a contract parameter. It does **not** generate that profile from the candidate it is testing. The input documents are pinned historical bytes. The constructed proof candidates and the supplied `CURRENT_AT_PINNED_SNAPSHOT` validity view are qualification-only inputs, not new E1 evidence or claims of live currentness.

## Normalized gaps and shared causes

| Gap | Source classes and available fields | Target fields still missing / exact failure |
|---|---|---|
| BR-01 | PLAN action identity, operation, executor, effect, prerequisites, scope, evidence and prose acceptance criteria; GOVERNED_TEXT bounded result reports | O01 `result_contract`, typed authority/knowledge requirements and independently accepted full definition table; O03 source-to-bounded-result admission. The source's semantic acceptance text is not an executable result-type table. |
| BR-02 | PLAN history, execution state and result pointers; MANIFEST ledger binding | O02/O06 typed selection-only versus action-attempt records, result identities, current proof-source links and hold/override reconciliation. Selection attempt 1 explicitly has `action_result=null` and no selected/executed action. It cannot be silently projected into an action attempt. |
| BR-03 | GRAPH entity IDs/types, assertion triples, provenance, assertion class, ordering and projection layer | O10 predicate identities/contracts, claim disposition and complete accepted support references. `SOURCE_LOCATED` cannot become `ACCEPTED` merely because a source digest matches. |
| BR-04 | Exact existing O08 preparation/dossier/authority/propagation supports; O09 invocation candidate/acceptance and profile candidate/acceptance/release supports | Closed here: candidate proof fields have direct selectors, deterministic derivations, explicit joins or existing contract constants, and all three candidates pass unchanged predicates. |
| BR-05 | PLAN/GRAPH/MANIFEST/HANDOFF/CHECKPOINT identities, selectors, ledger/policy bindings and partial proof submissions | O16 full-source component tables, source-to-component coverage and independently trusted composed profile. Existing BASE/RENAMED profiles govern synthetic normalized inventories, not all 2,733 assigned frozen-source fields. |

The machine-readable preflight associates each gap with exact source owners and raw identities. These owners are the same 16 identities as the preceding CE-02 inventory; no archive-wide expansion is introduced.

Three shared abstractions explain the gaps:

1. **Governed semantic normalization** (BR-01/02/03): preserve source facts while deriving only authorized action contracts, current history meaning and operational graph predicates. Source extraction is insufficient.
2. **Typed identity, provenance and explicit joins** (BR-04 and part of BR-05): raw content, semantic authority, candidate instance, projected proof and governing profile identities must remain distinct. This abstraction is executable here for the three documentary routes.
3. **Independent profile trust and composition coverage** (BR-05): a projected candidate cannot supply its own expected allowlist. O16 additionally needs every component's qualified source projection and coverage.

The first and third causes cannot be closed by reusing the documentary constructor. They require explicit finite per-source normalization and acceptance rules, rather than filling missing fields with synthetic BASE/RENAMED values.

## Closed documentary projection contract

`project(route, profile, records, validity, context_sources)` is pure. `records` is an explicit role-keyed source set containing raw text and a typed CONTENT_IDENTITY. `context_sources` contains supplied graph/plan bytes. `profile` is one of the existing independently governed O08 or O09 contracts. This is a specification program embedded in the mapping companion, not planner implementation.

Stages are recognition, source validation, currentness validation, exact join/projection, then the **unchanged** O08/O09 admission predicate. An accepted projection is only a candidate. It does not by itself admit the gate or slot. Unknown routes, malformed role sets, duplicate roles, wrong domains, substitutions and missing joins fail closed.

### O08 validator authority

The authority document must have the exact issued decision schema/type. Its semantic authority ID is verified over its canonical body, separately from the raw file digest. Preparation and dossier each join to exactly one `source_artifacts` member using their independently pinned content identity and declared locator.

The proof's decision option, decision identity, authority record, scope, source lineage and implementation preconditions come from that document. Preparation type, predicate, gate, proof type, evaluation boundary and downstream exclusions are existing governing contract constants. They are not extracted from a passing test or inferred from implementation existence. The unchanged admission predicate additionally validates the documentary preparation/dossier/propagation semantics.

The proof preserves `CONTRACT-T1`, conditional `IMPL-VALIDATOR`, no resolved slots and `validator_complete=false`. No issuance, acceptance or runtime effect authority is introduced.

### O09 InvocationAttemptId

The candidate canonical body and byte length must verify against its instance identity. Its runtime, controller store, scope, allocation and predecessor supply the envelope and lineage. The graph slot is joined by exact SlotId with exactly one match; its source pointer is derived from the supplied graph, not from an expected fixture index.

The exact closure source remains mandatory. The existing O09 predicate decides whether the source set supports this slot's completion proof. Candidate existence alone is not admission, and a BLOCKED producer does not invalidate an independently current accepted proof.

### O09 profile_sha256

The profile candidate's canonical body is verified. The release source must contain exactly one governing JSON block whose semantic release authority identity verifies. `candidate_profile_identity` must equal the verified candidate instance identity. Release and candidate runtime/controller/lineage must correspond and match the governing envelope.

The slot value is the verified candidate body content digest. It is **not** the release authority identity, candidate instance identity or ProgrammerProfile identity. The exact acceptance source and unchanged O09 admission rules remain required.

## Field ownership, identities and provenance

The mapping companion records all **225 leaf fields** in the three constructed candidate inputs. Each is classified as DIRECT_SOURCE_FIELD, DETERMINISTIC_DERIVATION, AUTHORIZED_CROSS_SOURCE_JOIN or CONTRACT_CONSTANT. There are no unexplained fields **within these constructed candidates**. This is not a claim of complete field provenance for the remaining action/history/graph/composition targets; their unresolved fields are explicitly retained in the preflight.

Canonical proof serialization uses UTF-8, sorted object keys, compact separators and rejects non-finite JSON values. The proof identity hashes the canonical body excluding its identity member, with the existing proof namespace. Profile pins hash the independently supplied governing profile. Neither operation changes a source pin or authority domain.

Provenance has two levels:

- The exact O08/O09 candidate schema retains source role, raw content identity, declared path/selector, graph binding and required method. Existing schema fields are not enlarged to bypass admission.
- The bridge record retains governing profile/program pins, explicit source inputs, projection version and field ownership. Persisting this record with the candidate supplies the dependency information needed to rerun projection in a cold process.

Locators identify explicitly supplied bytes after the contract has selected a source role. They never choose the predicate. Documentary text roles require an independently authenticated governing support binding; Markdown structure alone does not establish authority.

Runtime and controller identities are copied only from verified governing source envelopes. Dispatch, OperationalContext, OperationalBinding, ProgrammerProfile, WorkAuthorization lineage and ledger identities are not manufactured by these three projections. Their absent/provenance-only status cannot be upgraded by successful gate/slot proof admission. Full ledger/composed-context projection remains BR-02/BR-05.

## Join and invalidation rules

The join companion defines J-ROLE, J-VALIDATOR, J-INV, J-PROFILE and J-CONTEXT. Every join operates on explicit inputs. Zero or multiple valid correspondences reject. Exact typed identities, source pins, scope and lineage must match; compatible-looking content is not a substitute.

Required support validity is independent input. A source that becomes stale or invalid causes candidate projection/admission to fail after persistence/reload exactly as it would in a fresh evaluation. Source bytes do not gain freshness from an unchanged hash. The original source relationship is retained transitively through the bridge record and proof supports.

Nine per-source invalidation cases cover every documentary support independently. These are specification checks: the required downstream planner consequence is to remove support and recompute dependent conclusions, but no planner transition is implemented or executed in this task.

## Executed cases and composition limits

The new specification checks pass:

- **3 positive source-to-Oxx chains**: O08 and both actual O09 baseline slots.
- **30 negative cases**: missing/duplicate source role, wrong domain, substituted bytes/identity, stale source, wrong role, wrong graph context, wrong currentness context, and structurally valid but inadmissible projected proof type, for each route.
- **9 source invalidations**, one per support role, after canonical reload.
- **3 canonical reload/input-order checks**.
- **4 partial O16 composition cases**: two accepted combinations using newly projected proofs plus the pre-existing BASE/RENAMED action/history/graph components; two rejected cross-envelope substitutions.

Negative results record the actual rejecting stage and clause. The proof-type negative intentionally reaches the existing Oxx predicate; it cannot be counted as an early source-validation failure.

The O16 checks demonstrate that the new proofs compose with the existing qualified component fixtures and that an incompatible proof does not. They **do not** demonstrate full frozen-source-to-O16 restoration: action/history/graph components still come from prior synthetic source profiles. Full source-to-O16 positive count remains **0**. No existing Oxx predicate is weakened or rewritten.

The positive sources use actual pinned documentary bytes with a synthetic qualification wrapper and explicit historical validity premise. They are not nine newly generated arbitrary-schema source instances; that broader requested coverage remains incomplete.

## Complete inventory preflight and remaining work

All 16 owners and nine classes are classified in the preflight companion; no first-failure truncation is used.

- Nine documentary support owners now have an end-to-end O08/O09 route.
- Seven owners still lack their complete assigned operational bridge: PLAN, GRAPH, MANIFEST, HANDOFF, CHECKPOINT, S-BINDING result and S-CONTEXT result.
- PLAN/GRAPH serve as checked context inputs in the successful proof routes, but that does not qualify their full assigned field projections.
- DECISION_AUTHORITY, INVOCATION_CANDIDATE and PROFILE_CANDIDATE classes have their bounded assigned documentary routes. GOVERNED_TEXT is only partially covered because the two O03 result owners remain. The other five classes are not fully supported.
- No ambiguous actual join or new Oxx contradiction was demonstrated. This does not turn the remaining gaps into passes.

BR-01 still needs a source-derived, independently governed typed definition/result table for the assigned actions, including exact scope and typed evidence/authority/knowledge requirements. BR-02 needs explicit event variants and their ledger/result/current-overlay correspondences, including the selection-only event. BR-03 needs a relation/predicate and provenance-admission projection for all assigned assertions. BR-05 then needs coverage and trust bindings for those projected components and the manifest/handoff/checkpoint dependencies. None may be repaired by copying expected BASE/RENAMED values or by declaring all located sources accepted.

These are finite remaining projection-contract obligations, not requests for external budget evidence, an E1 database or an implementation lifecycle redesign. The requested closure of all five groups has **not** been achieved in this artifact.

```text
BR_01_STATUS = OPEN
BR_02_STATUS = OPEN
BR_03_STATUS = OPEN
BR_04_STATUS = CLOSED (bounded O08/O09 documentary projections)
BR_05_STATUS = OPEN
BRIDGE_ROOT_CAUSE_GROUPS = [GOVERNED_SEMANTIC_NORMALIZATION, IDENTITY_PROVENANCE_AND_EXPLICIT_JOIN, INDEPENDENT_PROFILE_TRUST_AND_COMPOSITION_COVERAGE]
TARGET_FIELDS = 225 constructed candidate leaves; remaining target families explicitly unresolved
UNEXPLAINED_TARGET_FIELDS = [BR-01 typed definition/result requirements, BR-02 event/hold/current-proof reconciliation, BR-03 operational predicate/provenance disposition, BR-05 full-source trust/coverage]
CROSS_SOURCE_JOINS = [J-ROLE, J-VALIDATOR, J-INV, J-PROFILE, J-CONTEXT]
AMBIGUOUS_JOINS = [] (supplied documentary source sets)
SOURCE_TO_OXX_POSITIVES = 3
SOURCE_TO_OXX_NEGATIVES = 30
O16_COMPOSITION_CASES = 4 partial; 0 complete source-to-instance cases
END_TO_END_SUPPORTED = 9 documentary support identities in preflight companion
BRIDGE_GAPS_REMAINING = [BR-01, BR-02, BR-03, BR-05]
CONTRACT_CONTRADICTIONS = []
CE_02_CLOSED = NO
C06A_3_CONTRACT_MISMATCH_SET = [BR-01, BR-02, BR-03, BR-05]
C06A_3_CONTRACT_CONFLICT_SET = []
C06A_3_CONTRACT_EXCEPTION_SET = [CE-02]
C06A_3_RETRY_ALLOWED = NO
RESTORED_AND_QUALIFIED = 2/17
C06A_4_READY = NO
C07_RETRY_ALLOWED = NO
F03_STATUS = CLOSED
V0_1_CURRENT_STATUS = CORRECTION_REQUIRED
IMPLEMENTATION_MODIFIED = NO
E1_ARTIFACTS_MODIFIED = 0
REAL_E1_EVIDENCE_CREATED = NO
PRODUCTION_EFFECT = NO
```
