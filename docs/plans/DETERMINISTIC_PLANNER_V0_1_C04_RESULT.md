# Deterministic Planner v0.1 — C04 result

C04 addresses F05 / RC-TYPED-ORDERING under the [correction plan](DETERMINISTIC_PLANNER_V0_1_CORRECTION_PLAN_1.md), [matrix](DETERMINISTIC_PLANNER_V0_1_CORRECTION_MATRIX_1.md), and [adversarial review](DETERMINISTIC_PLANNER_V0_1_ADVERSARIAL_REVIEW.md). It has no unfulfilled prerequisite. The repository matches the planned defect and interfaces. C01–C03 remain accepted; current qualification remains CORRECTION_REQUIRED.

## Reproduction and correction

Before implementation edits, T05 reproduced the exact adversarial failure. A satisfied ConditionId('same') and resolved SlotId('same') had goals in both orders. Canonical snapshot bytes were identical, but `recompute` returned different complete Computation values because the branch tuple followed input order. The new regression failed on full Computation equality, not a scalar control or selected-action comparison.

The implementation correction changes two expressions in `core._global_control`:

- Sort goals by the existing `_key(goal.target)` = (canonical ID type name, exact value).
- Preserve that same typed key in frontier witnesses for both goal and action-path identities.

No ordering obligation, ActionId priority, condition, slot, decision, authority or lifecycle behavior is changed. No parallel model/validation path is added. Unknown or malformed state still passes through the existing fail-closed admission checks.

The post-repair exact regression passes: both valid permutations produce the same complete output. `REJECTED_CORRECTLY` below means the divergent-output counterexample is eliminated; valid reordered inputs are normalized, not rejected as malformed.

Typed witness variants retain four distinct witnesses for two same-spelling goals and two paths. The old bare-string representation collapsed the two goal domains; the new representation explicitly distinguishes ('ConditionId','same') from ('SlotId','same'), and each path member carries its ActionId tag.

## Ordering audit

- Prerequisite projection already uses the existing typed `_key` for its heterogeneous IDs and edges.
- Other core ordering sites operate on single-domain ActionIds, KnowledgeIds, GateIds or predicate/evidence IDs. Their lexical order is unchanged.
- Resume-support identities already sort by identity kind, namespace and digest.
- Imported artifact pins already use complete path/pointer/profile keys. The codec's set-valued collections sort canonical encoded values containing type tags. Predicate operands and reference collections remain set-valued.
- The importer/codec do not select input artifacts through filesystem enumeration. Tests vary unrelated directory-entry creation order while loading exact pinned paths.
- Event arrays, parent-event chaining, receipt observations and lifecycle histories retain their existing causal order. Existing negative ledger-sequence/parent and lifecycle-shortcut tests remain in the full regression suite.

No model or codec change is necessary: frontier witnesses are derived Computation output, not persisted snapshot fields. CLI output currently exposes frontier gate IDs, not full branch/witness detail. CLI comparisons therefore cover the actual exposed projection; direct complete-Computation equality and a test-only type-preserving canonical encoder cover every Computation field, branch and witness. The encoder preserves tuple order and does not sort away the defect under test.

## Tests

Six new tests cover:

1. T05: equal canonical input identity, reversed same-spelling typed goals, complete Computation equality.
2. All root/slot satisfied/unresolved state combinations and both goal orders, canonical output equality and serialize/reload stability.
3. Four type-preserving witnesses under action, status, goal, entry-reference and boundary-reference permutations.
4. Fresh processes with hash seeds 1, 7, 42, 123 and 999, each with canonical and recursively reversed JSON object keys.
5. Set-valued predicate/operand/reference permutations with independently missing proof inputs.
6. Native bundle persistence, reversed source-pin order, cold process restoration, CLI output equality, and opposite filesystem entry creation orders.

The full required command is:

```sh
python3 -m unittest adapter.tests.test_planner_core adapter.tests.test_planner_invariants adapter.tests.test_planner_resume adapter.tests.test_planner_e1_replay adapter.tests.test_invocation_constructor -v
```

Final full run: **137 tests PASS in 663.588 seconds**, including all 131 pre-C04 tests and six new tests.

This includes A–N, X01–X11, C01–C03 adversarial regressions, importer, ledger/persistence, selection, global control, cold resume, CLI and constructor tests. Test helper serialization is not a second runtime codec or a change to persisted identities.

## Preservation and limits

The pre-edit inventory captured all 10,911 frozen E1 files, including bytecode files. Every path and raw SHA-256 remains identical. The complete sorted compact JSON inventory commitment remains `1cf25145f69a2fb133c12f3b15cd1089351e4a9cac8624d4b6e970f2b4b3a044`.

Backlog, implementation/correction plans and matrices, historical qualification, existing correction results, E1 state and authority records remain unchanged. No fixtures changed. The source-change comparison separately excludes generated caches outside E1. Only core.py and the two assigned test files changed; this result is the only new repository artifact. `git diff --check`, whitespace checks on previously untracked changed files, and document-link checks pass.

F03 and F06 remain open. C05–C07 were not implemented. No real E1 resume, authority issuance, construction, production operation or final requalification occurred.

## Report

```text
WORK_PACKAGE = C04
RESULT = PASS
FINDINGS_ADDRESSED = [F05]
FILES_ADDED = [docs/plans/DETERMINISTIC_PLANNER_V0_1_C04_RESULT.md]
FILES_MODIFIED = [adapter/planner/core.py, adapter/tests/test_planner_core.py, adapter/tests/test_planner_resume.py]
PRE_REPAIR_COUNTEREXAMPLES = {T05/F05: REPRODUCED}
PRE_REPAIR_REGRESSIONS = {T05: FAIL_EXPECTED}
POST_REPAIR_COUNTEREXAMPLES = {T05/F05: REJECTED_CORRECTLY}
POST_REPAIR_REGRESSIONS = {T05: PASS, T-ORDER: PASS}
TESTS_PASSED = 137
AFFECTED_REPLAY_CASES = {A: PASS, B: PASS, C: PASS, D: PASS, E: PASS, F: PASS, G: PASS, H: PASS, I: PASS, J: PASS, K: PASS, L: PASS, M: PASS, N: PASS}
AFFECTED_INVARIANTS = {X01: PASS, X02: PASS, X03: PASS, X04: PASS, X05: PASS, X06: PASS, X07: PASS, X08: PASS, X09: PASS, X10: PASS, X11: PASS}
DETERMINISM_TESTS = PASS (C04 scope: complete outputs/witnesses, permutations, reversed object keys, five hash seeds, canonical reload, cold restore and CLI)
C01_REGRESSION = PASS
C02_REGRESSION = PASS
C03_REGRESSION = PASS
FINDINGS_CLOSED = [F01, F02, F04, F05]
FINDINGS_REMAINING = [F03, F06]
NEWLY_ELIGIBLE = []
NEXT_CORRECTION_PACKAGE = C05
V0_1_CURRENT_STATUS = CORRECTION_REQUIRED
E1_FILES_VERIFIED = 10911
E1_ARTIFACTS_MODIFIED = 0
DEFERRED_SCOPE_VIOLATIONS = 0
PRODUCTION_EFFECT = NO
```

C05 was already independently eligible and is next under the plan's lexicographic rule. C06 still requires C05; C07 still requires integrated correction/requalification. No next package was executed.
