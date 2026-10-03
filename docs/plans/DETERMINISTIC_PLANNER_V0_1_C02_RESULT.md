# Deterministic Planner v0.1 — C02 result

C02 implements only RC-STALE-OBLIGATION / F01 under the [correction plan](DETERMINISTIC_PLANNER_V0_1_CORRECTION_PLAN_1.md) and [matrix](DETERMINISTIC_PLANNER_V0_1_CORRECTION_MATRIX_1.md). [C01](DETERMINISTIC_PLANNER_V0_1_C01_RESULT.md) remains PASS and F04 remains CLOSED. Current qualification status remains CORRECTION_REQUIRED; the original qualification is historical and unchanged.

## Verification and reproduction

The repository matched C02's prerequisites, assigned modules and interfaces. No CORRECTION_PLAN_MISMATCH occurred. The pre-edit inventory captured every frozen E1 path and raw SHA-256, including bytecode files: 10,911 files. Source-change comparison separately excludes generated Python caches outside E1.

T01 was reproduced through the real `invalidate_sources` → `evaluate_satisfaction` path. The child had accepted independent knowledge, an unresolved parent, and a mandatory REQUIRES assertion with distinct ordering provenance. Before invalidation the child was UNRESOLVED. Invalidating only ordering provenance made it SATISFIED under the reviewed implementation. The new test failed precisely on `SATISFIED == SATISFIED` in the assertion prohibiting satisfaction. An initial fixture setup error omitted existing action metadata edges; that fixture was corrected before recording reproduction or changing implementation. The accepted red run had one expected assertion failure, no setup errors.

The same regression now passes: the ordering obligation remains in projection, the child and dependent slot are stale/unproved, and independent S-BINDING remains actionable. This rejects the invalid conclusion while retaining admissible stale history.

## Correction

- `core.project` retains stale explicit ordering obligations rather than deleting them. Metadata checks and cycle checks continue to apply.
- `gates.unavailable_support` computes the finite transitive unavailable-support closure from the existing typed graph and state. It covers ordering subjects, predicates, action outputs, roots, slots and decision prerequisites without adding a second mutable graph.
- Propagation and direct predicate, decision, evidence-usability and action gates reject those unavailable qualifications. Global control traversal uses current completion qualification rather than a historical COMPLETED label.
- `Action.qualification` is typed ValidationState metadata persisted by the existing canonical codec. Its default is omitted using the codec's additive-field convention, preserving existing valid encoded identities. STALE qualification is explicitly serialized. Historical action completion remains COMPLETED after its source becomes stale, including an action with an empty output inventory; it cannot discharge a current ACTION_COMPLETED prerequisite.
- `invalidate_sources` propagates loss of qualification into current roots, slots, entities, knowledge and actions. It preserves historical execution status. ANY retains a genuinely independent valid alternative; mandatory ordering assertions cannot be bypassed by adding a duplicate accepted edge.
- Requalification requires an explicit accepted replacement binding and independently renewed output qualification. Tests construct that new synthetic state explicitly; invalidation never invents fresh evidence or resets stale qualifications.

This does not repair F02's resume-eligibility reporting rule, F03's real-E1 restoration gap, F05's typed ordering, or F06's policy binding. No frozen E1 action, evidence request, authority or lifecycle transition was executed.

## Tests and oracles

Eight C02 tests exercise the real implementation without mocks:

| Test | Independent acceptance oracle |
|---|---|
| T01 ordering invalidation | Unresolved mandatory parent still prevents child satisfaction after ordering-source invalidation |
| Transitive diamond / slot / mixed support / requalification | Mandatory stale obligation remains blocking across chains and diamonds; duplicate support does not erase it; explicit renewed binding can qualify |
| Historical completion | Completed action remains historical COMPLETED while stale output cannot prove current completion or unlock S-CONTEXT |
| Decision readiness | Previously ready DEC-BUDGET becomes unavailable when its explicit prerequisite binding becomes stale, including direct readiness evaluation before recompute |
| Legitimate ANY / empty inventory | Independent accepted alternative remains usable; source-only completed action persists stale qualification through reload |
| Hash/key determinism | Five fresh-process hash seeds × canonical/reversed object keys produce identical serialized state, actionability, selection and control output |
| Goal/control | Stale goal cannot claim terminal success; independent work remains RUNNABLE; no-work state remains non-success after reload |
| Ordered evidence | Direct evidence usability and predicate validation reject stale ordering support even before invalidation propagation; entity staleness survives reload |

Additional permutation checks reverse root, slot and assertion order. Canonical serialization/reload preserves results. Existing tests cover A–N replay, X01–X11, importer, append-only persistence, cold resume, selector, all global controls, C01 hostile inputs and constructor regressions.

Final command:

```sh
python3 -m unittest adapter.tests.test_planner_core adapter.tests.test_planner_invariants adapter.tests.test_planner_resume adapter.tests.test_planner_e1_replay adapter.tests.test_invocation_constructor -v
```

Final run: **123 tests PASS in 549.798 seconds**. This includes all 115 pre-C02 tests and eight new C02 regressions.

Passing existing N remains a replay regression result, not closure of F02 or F03. No final requalification or independent adversarial review is claimed.

## Preservation and scope

Only the four assigned implementation modules and invariant tests changed. No fixture, backlog, implementation/correction plan, matrix, original qualification, C01 result or authority artifact changed. This result is the only added repository file. All 10,911 E1 files retain their exact paths and bytes. The frozen inventory commitment remains `1cf25145f69a2fb133c12f3b15cd1089351e4a9cac8624d4b6e970f2b4b3a044` (SHA-256 of sorted compact UTF-8 JSON path-to-raw-SHA256 map). `git diff --check` and per-file whitespace checks for the previously untracked implementation pass. Result-document links resolve.

## Report

```text
WORK_PACKAGE = C02
RESULT = PASS
FINDINGS_ADDRESSED = [F01]
FILES_ADDED = [docs/plans/DETERMINISTIC_PLANNER_V0_1_C02_RESULT.md]
FILES_MODIFIED = [adapter/planner/model.py, adapter/planner/core.py, adapter/planner/gates.py, adapter/planner/codec.py, adapter/tests/test_planner_invariants.py]
PRE_REPAIR_COUNTEREXAMPLES = {T01/F01: REPRODUCED}
PRE_REPAIR_REGRESSIONS = {T01: FAIL_EXPECTED}
POST_REPAIR_COUNTEREXAMPLES = {T01/F01: REJECTED_CORRECTLY}
POST_REPAIR_REGRESSIONS = {T01: PASS, T-STALE: PASS}
TESTS_PASSED = 123
AFFECTED_REPLAY_CASES = {A: PASS, B: PASS, C: PASS, D: PASS, E: PASS, F: PASS, G: PASS, H: PASS, I: PASS, J: PASS, K: PASS, L: PASS, M: PASS, N: PASS}
AFFECTED_INVARIANTS = {X01: PASS, X02: PASS, X03: PASS, X04: PASS, X05: PASS, X06: PASS, X07: PASS, X08: PASS, X09: PASS, X10: PASS, X11: PASS}
DETERMINISM_TESTS = PASS (C02 scope: seeds 1/7/42/123/999, key reversal, input permutations, canonical reload)
C01_REGRESSION = PASS
F04_STATUS = CLOSED
FINDINGS_CLOSED = [F01, F04]
FINDINGS_REMAINING = [F02, F03, F05, F06]
NEWLY_ELIGIBLE = [C03]
NEXT_CORRECTION_PACKAGE = C03
V0_1_CURRENT_STATUS = CORRECTION_REQUIRED
E1_FILES_VERIFIED = 10911
E1_ARTIFACTS_MODIFIED = 0
DEFERRED_SCOPE_VIOLATIONS = 0
PRODUCTION_EFFECT = NO
```

C04 and C05 remain independently eligible. C03 is next under the correction plan's lexicographic package rule. No next package was executed.
