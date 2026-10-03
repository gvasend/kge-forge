# C06 / C07 operational-contract reconciliation 1

Analysis and prospective planning only. **Primary classification: IMPLEMENTATION_GAP. F03 remains CLOSED under the accepted refined operational repair contract. C07 retry is not yet allowed.** Remaining full-import requirements are tracked below as C06A requirements, not as an unsupported reopening of the repaired counterexample. No qualification is granted.

## Sources and authority

- [Correction Plan 1](DETERMINISTIC_PLANNER_V0_1_CORRECTION_PLAN_1.md): C06/C07 definitions; sections 6 (restoration inventory), 8 (N-REAL), 9 (conjunctive gate).
- [Correction Matrix 1](DETERMINISTIC_PLANNER_V0_1_CORRECTION_MATRIX_1.md): F03, T03, T-IMPORT, N-REAL, state/persistence table and qualification checklist.
- [Adversarial review](DETERMINISTIC_PLANNER_V0_1_ADVERSARIAL_REVIEW.md): F03 and its distinction between wrong enforcement and inability to continue.
- [Refinement](DETERMINISTIC_PLANNER_V0_1_C06_COUNTEREXAMPLE_REFINEMENT_1.md): independent source oracle, executable invariant, repair and limitations.
- [C06 result](DETERMINISTIC_PLANNER_V0_1_C06_RESULT.md): original BLOCKED attempt and appended refined PASS, especially “scope” and validation evidence.
- [C07 result](DETERMINISTIC_PLANNER_V0_1_C07_RESULT.md): prerequisite mismatch, no qualification execution.
- [v0.1 implementation plan](DETERMINISTIC_PLANNER_V0_1_IMPLEMENTATION_PLAN.md): R01/R04/R07/R15/R17/R18/R20/R22; sections 4, 7, 8; P06 and completion gate.

The original plan permits reviewed normalization and opaque **non-operational** relations. It requires unsupported necessary rules to block. The correction plan adds the explicit full field-coverage inventory, independent positive continuation tests and prohibition on copying M as the actual full import. These are explicit correction-gate requirements, even where their precise testing mechanism is more specific than the original v0.1 requirement.

The refinement originally said its local repair was necessary but insufficient for full C06. The subsequent resumed instruction expressly accepted a narrower repair gate; the appended C06 result records that scope. Both statements remain historical facts. This reconciliation preserves the accepted narrow result while assigning outstanding full-import work separately. It does not retrospectively assert that all original C06 acceptance criteria passed.

## Original contract, difference and implementation coverage

Categories: **A** required by the proven refined F03 defect; **B** independent v0.1 requirement; **C** explicit C07 prerequisite; **D** obsolete after refinement; **E** unsupported by current requirements. B/C classification preserves requirement strength without claiming every field was independently implicated by the refined counterexample.

Coverage labels apply to the stated boundary, not to whether a similarly named generic type exists. `IMPLEMENTED_AND_TESTED` refers to inspected enforcing code and existing regression tests, not a new test run in this analysis. A split row separates implemented substrate from unimplemented full-import coverage.

| ID / exact original requirement (Correction Plan §6 unless specified) | Difference from refined repair / category | Current implementation coverage and evidence |
|---|---|---|
| O01 Action class/stage/effect/scope from P `/resolution_actions` | Full stage/scope restoration beyond accepted outcome edge: B,C (R01/R18) | Basic Action class/effect/source model and fixture loading: IMPLEMENTED_AND_TESTED. Full source-derived action contract: NOT_IMPLEMENTED; `replay.import_e1` loads the M normalization, not these full fields. |
| O02 Prerequisites, external/current holds, `knowledge_requirements`, reentry gates | Exact typed accepted non-PASS prerequisite: A,B,C, fulfilled. Remaining hold/overlay semantics: B,C | Source-bound producer/outcome requirement: IMPLEMENTED_AND_TESTED by `restore_accepted_knowledge`, `gates` KNOWLEDGE_ACCEPTED and `test_planner_c06`. Complete plan prerequisite/hold family restoration: NOT_IMPLEMENTED. |
| O03 `acceptance_criteria`, `completion_does_not_imply`, accepted outputs, secondary stages | B,C (R01/R07/R18); not needed to reject refined stale selection | Generic exact output checking: IMPLEMENTED_AND_TESTED (`gates.validate_result`, core result tests). Full imported per-outcome contracts: NOT_IMPLEMENTED. Empty inventory rejects every supplied result; that is safe rejection, not a functioning supported positive contract. |
| O04 `authority_rule`, accepted decisions, scope/permission/exclusions | B,C (R17/R18) | Typed authority evaluation exists and is tested in core/invariant suites. Actual complete authority predicates/bindings for imported actions: NOT_IMPLEMENTED; opaque authority references cannot substitute. |
| O05 Decision readiness/dossier/alternatives/choice/reentry | B,C (R04) | `Decision`, `DecisionDossier`, `decision_readiness`, recorded decision and reentry APIs: IMPLEMENTED_AND_TESTED in F–I fixtures and `test_recorded_decision_import_and_explicit_reentry_are_separate_events`. Actual frozen-plan decision/dossier restoration: NOT_IMPLEMENTED. |
| O06 Execution history, attempt outcomes, accepted knowledge, current overlay lineage | B,C (R01/R07/R15); bounded outcome part fulfilled by A | Native append-only events: IMPLEMENTED_AND_TESTED. Three structured accepted-outcome dependencies restored and tested. Complete authenticated historical attempts/current-overlay cross-check: NOT_IMPLEMENTED; history remains opaque. Do not fabricate native executed events for old prose. |
| O07 Named receipt -> factual revalidation -> reevaluation with original gates and result contract | B,C (R07/R15) | Generic receipt/reentry and budget gate plus refined prerequisite: IMPLEMENTED_AND_TESTED. All represented routes with supported bounded future result contracts: NOT_IMPLEMENTED. |
| O08 Normalized roots' independent completion, ancestors, accepted proof and deferred counts | B,C (R01/R18) | Generic independent satisfaction and stale propagation: IMPLEMENTED_AND_TESTED (`core.evaluate_satisfaction`, C02). Full source-field completion-rule mapping/coverage: NOT_IMPLEMENTED; matching root ID sets is insufficient. |
| O09 Slots' mandatory source/producer/mapping/authority/validator/consumer links and accepted baseline values | B,C (R17/R18/R20) | Typed slot predicates and identity distinction: IMPLEMENTED_AND_TESTED in core/invariants. Complete operational source-link restoration for frozen slots: NOT_IMPLEMENTED. Missing facts must stay explicit. |
| O10 Operational graph assertions/entities versus non-operative records | B,C (R18/R20) | Typed relation projection/admission: IMPLEMENTED_AND_TESTED. Original graph records retained opaque by `import_e1`: implemented and tested for byte retention. Full semantic disposition/mapping: NOT_IMPLEMENTED. Opaque non-operative records are permitted; operational ones cannot use that disposition. |
| O11 Architect records and Candidate-3 identity/scope/exclusions/consumption | B,C (R15/R17/R18) | Manifest pins and opaque preservation: IMPLEMENTED_AND_TESTED. Full operational binding of choices/dossiers/exclusions and historical accepted authority state: NOT_IMPLEMENTED. No new current applicability grant may be inferred. |
| O12 All handoff frontier contracts: producer, authentication, scope/lineage/currentness, receipt/reentry | B,C (R07/R15) | Generic external gate and detailed budget receipt substrate: IMPLEMENTED_AND_TESTED in J–N. Full per-frontier operational evidence-contract restoration: NOT_IMPLEMENTED; endpoint IDs and boundary holds are insufficient. |
| O13 Eight budget obligations plus owning-source/decision applicability constraints | B,C (R07/R17/R18) | Eight requirement/receipt checks: IMPLEMENTED_AND_TESTED in J–N. Full source/decision relationship mapping and positive bounded proof-matrix result contract: NOT_IMPLEMENTED. Reference identity alone never establishes applicability. |
| O14 Selection policy identity/version/static rules and extensions | B,C (R02/R15/R20); independent of refined F03 | IMPLEMENTED_AND_TESTED: `selector.validate_policy`, import and bundle policy admission; C05 policy-substitution regression. Retain, do not reimplement. |
| O15 Full-run goal coverage, suspension/resume proof, oracle comparison after computation | B,C (R15/R22) | Generic resume proof, persisted route binding and source verification: IMPLEMENTED_AND_TESTED (C03; cold-process tests). Independent full imported required-goal/contract inventory: NOT_IMPLEMENTED. Existing M/N control assertions do not prove inventory completeness. |
| O16 Reviewed versioned pinned per-field coverage map, unknown required fields fail closed, no old M executable-state import | C; general deterministic ingestion/provenance also B (R20/P06) | Source pins, typed decoding and normalized fixtures: IMPLEMENTED_AND_TESTED. Required complete coverage inventory and replacement actual-manifest mapping: NOT_IMPLEMENTED. `N_P06.json` still pins `M_P05.json`; `import_e1` calls `load_p05_fixture`. |
| O17 Full semantic N-REAL cold restoration and supported renamed continuation/decision tests | C; cold restore itself B (R15/R22/P06) | Reduced-state cold restoration: IMPLEMENTED_AND_TESTED. Full required operational N-REAL qualification: NOT_IMPLEMENTED as a complete test path; dependent contract implementation also missing. |

No outstanding original requirement is classified D or E merely because the refined test did not exercise it. No row is called IMPLEMENTED_NOT_INDEPENDENTLY_TESTED to disguise missing import logic. The narrower existing code/test paths are separately identified above. No new broad test pass is claimed.

Two rejected interpretations are outside the governing requirements: “require the BLOCKED producer to become COMPLETED” and “default PASS permits empty PASS.” The former contradicts the accepted knowledge contract; the latter is disproved by the original C06 attempt and `gates.validate_result`. Neither is an implementation obligation to preserve in C06A. These are unsupported interpretations (E), not obsolete original requirements.

## Refined proven contract and current enforcement

**Invalid pre-repair state:** after an isolated synthetic accepted receipt/reentry, the imported action omitted its required typed REEVAL-BUDGET accepted-knowledge dependency. Invalidation of that exact result source left FACT-BUDGET-APPLICABILITY actionable and selected after snapshot reload; its snapshot identity did not change.

The independent oracle is frozen plan `/resolution_actions/62/knowledge_requirements/0` (resolved by ActionId, not index), binding REEVAL-BUDGET's BLOCKED result source to the consumer. The refinement records exact raw hashes and source location. No historical producer completion is required.

**Accepted repair:** [replay.py](../../adapter/planner/replay.py) `restore_accepted_knowledge` authenticates the pinned result, checks producer/outcome/source consistency and creates a source-bound KnowledgeRecord plus KNOWLEDGE_ACCEPTED predicate. [model.py](../../adapter/planner/model.py) validates typed producer/outcome and complete predicate bindings; [gates.py](../../adapter/planner/gates.py) compares them. Existing invalidation follows provenance; [codec.py](../../adapter/planner/codec.py) persists the additive fields. Roots/slots are not satisfied by this repair.

**Post-repair evidence:** the preserved candidate and permanent [C06 tests](../../adapter/tests/test_planner_c06.py) exercise real import, receipt, invalidation, codec and recomputation. The exact stale action is absent from actionability/selection. Controls preserve valid knowledge from a BLOCKED producer, unrelated-source independence and represented-source invalidation. Permanent variants cover incomplete knowledge, missing producer/outcome, wrong producer/outcome/source identity/domain, changed bytes, missing pin, alpha-renaming, stale round trips, permutations and six cold-process seed/key-order combinations. Flag-only revalidation does not release the held action. These tests do not prove a general authorized replacement-source transition or positive full proof-matrix result acceptance; those remain separate coverage requirements.

The C06 result records 142 prior tests passing plus the corrected eight-test C06 run, with its earlier test-fixture failure disclosed. That evidence is not rewritten as one clean full run. This analysis inspected code and tests without rerunning qualification.

## Status and classification

**F03_STATUS = CLOSED**, scoped to the accepted refined operational failure, as required by the resumed C06 acceptance. There is no new evidence that this repaired source-bound dependency fails. The original review's broader restoration concern remains relevant requirement evidence; it does not disappear, but its remaining work is now tracked as O01–O17/C06A rather than silently changing a historical finding status. This is not a claim that the original broad F03 wording was fully implemented.

**PRIMARY_CLASSIFICATION = IMPLEMENTATION_GAP.** Generic mechanisms exist, but the full importer does not populate their required operational contracts. New tests alone cannot supply missing contracts. The independent v0.1 requirements and explicit correction gate prevent a plan-only deletion of the prerequisites.

Plan bookkeeping also needs reconciliation: “C06 PASS unlocks C07” must distinguish the accepted refined scope from completion of remaining full-import obligations. This report proposes a separate dependency, not a weakening of the gate. There is no basis to call the full gate obsolete or overbroad as a whole. Original plan/matrix remain unchanged because this is not a plan-only reconciliation.

## Proposed bounded package C06A — full operational import coverage

**FINDINGS/REQUIREMENTS_ADDRESSED:** remaining B/C obligations O01–O13 and O15–O17; preserve completed O02 refined portion and O14. No automatic reopening of F01–F06. This is fulfillment of existing requirements, not a new planner capability program.

**PREREQUISITES:** accepted C01–C06 results; this reconciliation adopted as the C06A execution contract by an explicit implementation instruction; pinned unchanged sources and inventory; preservation of C06 red/green history. No external E1 facts or decisions are acquired.

**FILES:** existing `adapter/planner/replay.py` and versioned mapping/fixtures under `adapter/tests/fixtures/planner_v0_1/`; bounded additive model/codec fields only where a required represented contract cannot use existing types. Gates/core integration only if a concrete gap in enforcing restored typed contracts is demonstrated. Existing planner tests plus a focused C06A test file and new C06A result/coverage artifacts. No parallel importer state model.

**IMPLEMENTATION:** compile an explicit reviewed mapping from pinned plan/graph/manifest/handoff/checkpoint/source contracts into existing typed objects. Account for each required field with source identity/location, rule/version, destination, acceptance basis and disposition. Preserve opaque descriptive records, but mark unsupported necessary rules with explicit blocking reasons. Restore required supported action/result, decision/dossier, authority, history-overlay, goal/slot and receipt/reentry contracts. Retain immutable historical evidence separately from current validity. Do not execute prose, infer missing facts or repin altered frozen sources. Replace the old M executable-state dependency for actual import; M may remain a historical replay fixture/oracle.

**PRE_REPAIR_COUNTEREXAMPLE:** first independently pin a supported bounded result contract from the source action's acceptance criteria (T03 proof-matrix case), then construct a separate synthetic complete receipt plus all original prerequisite proofs. Supply a complete valid bounded result through the real import/result path. The existing imported empty accepted inventory is expected to reject it with `no accepted bounded result contract`, despite the source-level contract permitting that bounded acquisition result. Also demonstrate a supported source-declared decision route cannot reconstruct/enforce its dossier from full import. These are proposed executable red tests, **not reproduced in this analysis**. If exact evidence does not define a supported positive contract, report that precise gap and stop rather than inventing a valid output. Do not reuse the already-passing empty-PASS rejection as a red test.

**REGRESSION:** independent source-field inventory oracle; positive complete result and supported decision route; missing/partial/wrong source/authority/dossier rejection; unknown required fields and omitted contract/goal fail closed; historical/current overlay conflicts; alpha-renamed and changed-but-supported instances. Restore every relevant field through canonical persistence. Preserve the refined C06 stale prerequisite test. Test authorized replacement/revalidation only where a defined contract exists, otherwise explicit hold. No test may inject an expected actionable/control answer as a gate.

**ACCEPTANCE:** every required field has an independently checked operational or explicit unavailable/unsupported disposition; no operational field is merely opaque or omitted. Necessary supported positive contracts work; blanket unsupported holds are not completion. Missing authoritative semantics necessary for readiness yield BLOCKED, not invented rules. A–N, X01–X11 and C01–C06 remain passing; full required-goal coverage is checked; actual-manifest cold restoration uses sources rather than old M state. Compare full semantic outputs and identities across permutations, reversed keys, source/reference ordering, seeds and fresh processes. All 10,911 E1 files unchanged; no effects. C06A does not requalify.

**UNLOCKS:** C07 prerequisite retry only. C07 still owns integrated section 9 qualification, N-REAL verification and fresh independent review before any status update. No E1 execution is unlocked.

## C07 reentry predicate

`C07_RETRY_ALLOWED` is the conjunction of independently verifiable evidence, not the existence of this report:

1. An explicit instruction adopts C06A as the remaining requirement package without waiving section 9.
2. Preserved C01–C06 result identities identify their accepted scopes; refined F03 is CLOSED and its regression passes against the candidate code.
3. C06A result is PASS, pinned to candidate code, mapping, tests and source identities; its coverage manifest accounts for every required O-row/field. No unresolved necessary contract is hidden as opaque or default-empty.
4. Positive/negative C06A tests and correction regressions have passing evidence for those same code/mapping identities, including full cold import and source preservation. Results from another revision do not satisfy the predicate.
5. Protected-artifact/E1 inventory matches; no pending acceptance gap remains. Any mismatch makes retry false.

These proposed artifact fields and equality checks make the gate mechanically evaluable during C06A/C07; this analysis does not claim a new automated gate has been implemented. Current value: **NO**, because C06A has not been executed and the remaining required operational contracts are absent. Completion of this analysis alone changes no actionability or qualification.

## Report and preservation

```text
ORIGINAL_OPERATIONAL_CONTRACT = [O01, O02, O03, O04, O05, O06, O07, O08, O09, O10, O11, O12, O13, O14, O15, O16, O17]
REFINED_C06_CONTRACT = [typed accepted producer/outcome/source binding, stale prerequisite enforcement, persistence/reload, knowledge distinct from producer completion]
UNRESOLVED_CONTRACT_ELEMENTS = [O01, O02_remaining, O03, O04, O05, O06_remaining, O07_remaining, O08, O09, O10_operational, O11_operational, O12_full_frontier, O13_remaining, O15_full_goal_coverage, O16, O17]
F03_STATUS = CLOSED
PRIMARY_CLASSIFICATION = IMPLEMENTATION_GAP
IMPLEMENTATION_GAPS = [full source-driven operational mapping, action/result contracts, decision/authority restoration, history-overlay validation, full goal/slot/frontier contract coverage]
TEST_COVERAGE_GAPS = [independent field inventory, supported positive result/decision continuation, full semantic N-REAL, full-contract mutation and cold-replay tests]
PLAN_GAPS = [refined C06 closure and broader C07 prerequisite ownership need separate package tracking]
ADDITIONAL_CORRECTION_REQUIRED = YES
ADDITIONAL_PACKAGE = C06A (proposed, not executed)
C07_RETRY_ALLOWED = NO
C07_RETRY_PREREQUISITES = [C06A adoption, accepted C01-C06 scopes, C06A PASS with pinned coverage and tests, refined F03 regression PASS, protected-source preservation]
V0_1_CURRENT_STATUS = CORRECTION_REQUIRED
E1_ARTIFACTS_MODIFIED = 0
IMPLEMENTATION_MODIFIED = NO
PRODUCTION_EFFECT = NO
```

No machine-readable execution state was changed. This Markdown package definition follows the existing correction plan/matrix convention; no companion JSON is required for this analysis. No tests, C07, readiness execution or requalification ran. Raw path/SHA-256 comparison verified all 10,911 frozen E1 files and every pre-existing file under adapter/plans/backlog/E1 unchanged. Only this report was added. Relative links, whitespace and `git diff --check` passed. Original correction plan/matrix, blocked C06 attempt, refinement, accepted repair and blocked C07 record are preserved.
