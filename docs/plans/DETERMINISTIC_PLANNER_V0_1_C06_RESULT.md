# Deterministic Planner v0.1 — C06 execution result

## Result: BLOCKED at pre-repair regression gate

C06 is **not implemented** and F03 remains open. No implementation, fixture, historical qualification, authority, E1 or existing test file was changed. This is not a correction-plan mismatch finding and does not dispute the adversarial review's structural finding.

The [correction plan](DETERMINISTIC_PLANNER_V0_1_CORRECTION_PLAN_1.md), [matrix](DETERMINISTIC_PLANNER_V0_1_CORRECTION_MATRIX_1.md), and [review](DETERMINISTIC_PLANNER_V0_1_ADVERSARIAL_REVIEW.md) were inspected. C01–C05 satisfy C06's prerequisites. C06 requires full operational contract restoration and positive bounded-result behavior, not merely rejecting an empty result or adding object counts. C07 remains dependent on C06 PASS.

## Reproduction and unsuccessful regression design

A temporary test called the actual `replay.import_e1` against the frozen resume manifest. Direct measurement of its resulting typed state reproduced the review's structural counterexample:

```text
ACTIONS = 63
DECISIONS = 0
GRAPH_ENTITIES = 0
ACTIONS_WITH_REQUIREMENTS = 0
ACTIONS_WITH_AUTHORITY_PREDICATES = 0
ACTIONS_WITH_ACCEPTED_RESULT_PASS = 63
```

The temporary test then used the existing isolated synthetic receipt helper, applied EVIDENCE_RECEIVED, EVIDENCE_VALIDATED and DEPENDENT_ACTION_REENTRY through the actual core, and verified that FACT-BUDGET-APPLICABILITY became actionable. It supplied a PASS with empty knowledge and the exact pre-state identity, expecting a PlannerError.

**That test passed before any repair.** One test passed in 50.919 seconds. Inspection of `gates.validate_result` confirms the existing explicit empty-inventory rejection (`no accepted bounded result contract`). Default `accepted_result=PASS` is not itself permission to accept an empty result.

Thus the structural F03 finding is reproduced, but the chosen rejection regression does **not** expose the defect. It tests an existing safeguard. The review explicitly describes both under-enforcement and inability to continue and does not assert that empty PASS is accepted. The test must not be relabeled FAIL_EXPECTED, nor may this observation close F03.

The prescribed pre-repair failing-regression gate was not met. No correction was applied. The provisional test was removed and its file's raw SHA-256 verified against the pre-task baseline. The only persisted addition is this result record.

This stop is an execution/pre-repair-test gap, not a missing Architect decision, external-evidence request, or a conclusion that the source contracts cannot be restored. No such additional blocker has been established.

## Remaining work within C06

The next C06 attempt needs a failing test for **operational restoration**, independently checked against authoritative source fields, including the restored valid bounded-result acceptance path after isolated reentry. It must distinguish that positive contract from the already-working empty-result rejection. Then the package still requires its reviewed field-to-contract coverage inventory, typed historical/decision/authority/evidence restoration, supported positive and negative variants, and cold persistence/determinism tests. None of those implementation obligations is waived or moved to C07.

No post-repair behavior or regression-suite success is claimed. The affected suite was not run because no correction reached validation. Prior C01–C05 accepted results remain historical and unchanged; they were not independently requalified in this attempt.

## Preservation

Before inspection, an inventory recorded raw SHA-256 for every frozen E1 file. After stopping, all 10,911 paths and hashes remain identical. The compact sorted inventory commitment is `1cf25145f69a2fb133c12f3b15cd1089351e4a9cac8624d4b6e970f2b4b3a044`.

Implementation, existing tests/fixtures, backlog, correction plan/matrix, prior result/status records and historical qualification remain unchanged. Generated Python caches outside E1 are excluded from the source-change comparison. No E1 action was resumed; receipt transitions occurred only in an isolated in-memory synthetic test. No production effect occurred.

## Report

```text
WORK_PACKAGE = C06
RESULT = BLOCKED
FINDINGS_ADDRESSED = [F03: INVESTIGATED_NOT_CLOSED]
PRE_REPAIR_COUNTEREXAMPLES = {F03_STRUCTURAL_OMISSION: REPRODUCED, EMPTY_PASS_ACCEPTANCE: NOT_REPRODUCED_NOT_A_REVIEW_CLAIM}
PRE_REPAIR_REGRESSIONS = {ATTEMPTED_EMPTY_PASS_REJECTION: PASS_BEFORE_REPAIR, REQUIRED_FAIL_EXPECTED_GATE: NOT_MET}
POST_REPAIR_COUNTEREXAMPLES = {F03: NOT_RUN_NO_REPAIR}
POST_REPAIR_REGRESSIONS = {F03: NOT_RUN_NO_REPAIR}
TESTS_PASSED = 1 diagnostic test; no package acceptance claimed
AFFECTED_REPLAY_CASES = {A–N: NOT_RERUN}
AFFECTED_INVARIANTS = {X01–X11: NOT_RERUN}
DETERMINISM_TESTS = NOT_RUN
C01_REGRESSION = NOT_RERUN (prior PASS unchanged)
C02_REGRESSION = NOT_RERUN (prior PASS unchanged)
C03_REGRESSION = NOT_RERUN (prior PASS unchanged)
C04_REGRESSION = NOT_RERUN (prior PASS unchanged)
C05_REGRESSION = NOT_RERUN (prior PASS unchanged)
FINDINGS_CLOSED = [F01, F02, F04, F05, F06] (prior accepted closures; none added)
FINDINGS_REMAINING = [F03]
NEWLY_ELIGIBLE = []
NEXT_CORRECTION_PACKAGE = C06 (not completed)
V0_1_CURRENT_STATUS = CORRECTION_REQUIRED
E1_FILES_VERIFIED = 10911
E1_ARTIFACTS_MODIFIED = 0
IMPLEMENTATION_MODIFIED = NO
DEFERRED_SCOPE_VIOLATIONS = 0
PRODUCTION_EFFECT = NO
```

NOT_RERUN is deliberately used rather than fabricating a PASS/FAIL result for tests not executed in this attempt. C07 and final requalification were not executed.

---

## Resumed execution — refined source-bound prerequisite repair

This section supersedes the **execution outcome** of the original blocked attempt above. That attempt and its diagnostic results remain unchanged historical evidence. The [counterexample refinement](DETERMINISTIC_PLANNER_V0_1_C06_COUNTEREXAMPLE_REFINEMENT_1.md) remains unchanged. The resumed user instruction explicitly defines C06 acceptance around the refined accepted-knowledge prerequisite repair; this is not the former broad importer redesign or C07 qualification.

### Accepted repair and boundaries

`restore_accepted_knowledge` in `adapter/planner/replay.py` implements the finite `E1_ACCEPTED_OUTCOME_1` source projection. For each declared structured `knowledge_requirements` row, it checks the producer/consumer, typed expected outcome, independently pinned source identity, exact report ACTION/ACTION_RESULT fields, and the producer's recorded outcome/source in the authenticated plan. Unknown fields, missing pins, ambiguous reports and conflicting bindings fail closed. It creates no producer completion state.

The same rule restores the three existing declared requirements (SEM-BUDGET → INPUT-BUDGET; SEM-IMPLEMENTATION → INPUT-IMPLEMENTATION; REEVAL-BUDGET → FACT-BUDGET-APPLICABILITY), without action-name-specific logic. The first two AUTHORITY_REQUIRED observations and the last BLOCKED observation are accepted bounded knowledge, not successful producer execution or resolved budget facts.

`KnowledgeRecord` gains optional typed producer/outcome bindings; `KNOWLEDGE_ACCEPTED` predicates may bind an exact raw CONTENT_IDENTITY, producer ActionId and expected ActionResult. Partial predicate bindings and wrong identity domains fail admission. Evaluation requires all supplied bindings to match accepted KNOWN_COMPLETE knowledge. KNOWN_COMPLETE applies to the bounded observation of the recorded outcome; it does not describe completion of the governed condition. Existing unbound knowledge predicates retain their prior semantics.

The existing invalidator follows the restored KnowledgeRecord provenance and predicate edge, marks the proof stale and holds the consumer. The existing selector cannot select it. No new invalidation algorithm, action/root/slot model or lifecycle was introduced. Additive codec fields omit their defaults, preserving historical fixture encodings and canonical identities. Conflicting producer/outcome output declarations and dangling producers are rejected by existing model validation extended for these bindings.

The scope is the refined missing accepted-knowledge edge. Other opaque graph records, broad operational import capabilities, and future action-output contract restoration are not claimed implemented by this change. In particular, empty action-result inventories remain rejected; no acceptance rule was weakened to make a future result pass. F03 closure below follows the resumed instruction's refined acceptance gate. Full readiness and any residual broad-import concerns remain for C07's independent review; QUALIFIED status is not restored.

### Reproduction and regression

The pre-repair counterexample and FAIL_EXPECTED are established in the preserved refinement report. The exact isolated candidate was rerun after implementation: **4 tests PASS**. It now reports:

```text
ACTIONABLE = []
SELECTED = NONE
SAME_SNAPSHOT_IDENTITY_AFTER_INVALIDATION = false
```

The synthetic stale scenario reports PLAN_DEFECT because no recovery control-transfer route is represented for that invalidated prerequisite; it does not report RUNNABLE. This repair does not invent such a lifecycle route. The unchanged real frozen-state import still reports MIXED_WAIT with no action or resumption eligibility.

[Permanent regression](../../adapter/tests/test_planner_c06.py) subclasses the preserved isolated candidate to run all four exact tests under normal test discovery and adds four variant tests. The original candidate and refinement report were not rewritten.

Variants cover typed outcome/producer/source mismatches, incomplete knowledge, missing binding, malformed provenance, wrong identity domain, missing source pin, changed source bytes, conflicting historical outcome, stale canonical round trips, a BLOCKED producer's usable knowledge, unrelated-source control, an alpha-renamed AUTHORITY_REQUIRED producer/consumer with changed supported source bytes, and current-vs-stale actionability.

Revalidation boundary: a fresh authenticated historical import remains held until the already-defined receipt/reentry path completes in isolated replay. It is not an in-place retry of a stale live run. Reload and changing a knowledge qualification flag alone cannot clear a persisted stale action hold. No automatic requalification from identity stability, old bytes, or lifecycle phase is implemented, and no new live revalidation authority/transition is issued. A future live retry must use an explicitly admitted transition; this task does not manufacture one.

Determinism checks compare stale-state actionability, selected ID, control state and canonical identity under hash seeds 0/19/311, canonical and reversed JSON key ordering, reversed action/knowledge/predicate collections, repeated recomputation and serialization/reload. Existing suite tests retain all C01–C05 determinism/ledger/source checks.

### Validation results

The broad run executed **150 tests in 1024.406 seconds**: all **142 prior tests passed**, plus seven of the new tests; its sole failure was the pre-correction alpha-renamed test fixture described below. That process had loaded the test before its fixture correction. The final corrected permanent C06 suite then supplied **8 PASS in 338.694 seconds**. Thus passing evidence covers **150 distinct tests** against the final implementation, not a claim that the earlier broad command exited successfully. The exact isolated candidate separately passed all four tests in 100.952 seconds. The standalone invariant run also passed 39 tests.

All A–N, X01–X11, C01–C05 adversarial regressions, importer, CLI, persistence/replay, cold resume, deterministic selection, global controls and constructor regressions have passing results. Only the new test fixture/controls changed after the broad process started; no implementation changed after that launch. The corrected C06 rerun includes the added collection-permutation and changed-source controls.

Commands:

```sh
python3 -m unittest adapter.tests.counterexamples.c06_f03_candidate -v
python3 -m unittest adapter.tests.test_planner_core adapter.tests.test_planner_invariants adapter.tests.test_planner_resume adapter.tests.test_planner_e1_replay adapter.tests.test_planner_c06 adapter.tests.test_invocation_constructor -v
python3 -m unittest adapter.tests.test_planner_c06 -v
```

A transient new-test fixture failure was diagnosed before acceptance: the alpha-renamed positive control inherited BUILD-BINDING's QUALIFICATION_EFFECT_ONLY class, and the existing authority gate correctly blocked it. The isolated source-acquisition control was corrected to NON_EFFECTING. No implementation gate was relaxed. The corrected permanent C06 tests were rerun. Test-code-only refinements added collection-order and changed-source-byte controls.

### Preservation and final report

All 10,911 frozen E1 paths/raw hashes are identical to the pre-repair inventory, including bytecode files. Inventory commitment: `1cf25145f69a2fb133c12f3b15cd1089351e4a9cac8624d4b6e970f2b4b3a044`. Backlog, correction plan/matrix, historical qualification, prior correction records, refinement report and isolated candidate are unchanged. The original C06 result remains a byte-identical prefix of this file. Only the four implementation files, new permanent test, and this appended result changed (generated caches outside E1 excluded). `git diff --check`, added/untracked-file whitespace checks and report-link checks pass.

```text
WORK_PACKAGE = C06
RESULT = PASS
FINDINGS_ADDRESSED = [F03]
FILES_ADDED = [adapter/tests/test_planner_c06.py]
FILES_MODIFIED = [adapter/planner/model.py, adapter/planner/gates.py, adapter/planner/codec.py, adapter/planner/replay.py, docs/plans/DETERMINISTIC_PLANNER_V0_1_C06_RESULT.md]
PRE_REPAIR_COUNTEREXAMPLE = REPRODUCED
PRE_REPAIR_REGRESSION = FAIL_EXPECTED
POST_REPAIR_COUNTEREXAMPLE = REJECTED_CORRECTLY
POST_REPAIR_REGRESSION = PASS
TESTS_PASSED = 150 distinct suite tests (142 prior + 8 permanent C06), plus exact isolated candidate rerun
AFFECTED_REPLAY_CASES = {A: PASS, B: PASS, C: PASS, D: PASS, E: PASS, F: PASS, G: PASS, H: PASS, I: PASS, J: PASS, K: PASS, L: PASS, M: PASS, N: PASS}
AFFECTED_INVARIANTS = {X01: PASS, X02: PASS, X03: PASS, X04: PASS, X05: PASS, X06: PASS, X07: PASS, X08: PASS, X09: PASS, X10: PASS, X11: PASS}
DETERMINISM_TESTS = PASS
C01_REGRESSION = PASS
C02_REGRESSION = PASS
C03_REGRESSION = PASS
C04_REGRESSION = PASS
C05_REGRESSION = PASS
FINDINGS_CLOSED = [F01, F02, F03, F04, F05, F06]
FINDINGS_REMAINING = []
NEWLY_ELIGIBLE = [C07]
NEXT_CORRECTION_PACKAGE = C07
V0_1_CURRENT_STATUS = CORRECTION_REQUIRED
E1_FILES_VERIFIED = 10911
E1_ARTIFACTS_MODIFIED = 0
DEFERRED_SCOPE_VIOLATIONS = 0
PRODUCTION_EFFECT = NO
```

C07, final requalification, E1 resumption and production activity were not executed.
