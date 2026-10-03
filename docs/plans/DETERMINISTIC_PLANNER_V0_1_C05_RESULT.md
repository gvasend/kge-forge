# Deterministic Planner v0.1 — C05 result

## Scope and prerequisite verification

C05 addresses F06 (selection-policy identity/implementation binding), RC-POLICY-BINDING, and T06/T-POLICY under the [correction plan](DETERMINISTIC_PLANNER_V0_1_CORRECTION_PLAN_1.md), [matrix](DETERMINISTIC_PLANNER_V0_1_CORRECTION_MATRIX_1.md), and [adversarial review](DETERMINISTIC_PLANNER_V0_1_ADVERSARIAL_REVIEW.md). C01–C04 remain accepted. Repository inspection found no correction-plan mismatch. C05 has no additional domain prerequisite; C06 requires completion of C01–C05.

## Before/after evidence

Before implementation changes, the new regression loaded the real B_P06 fixture, replaced its policy ArtifactPin with its independently valid Candidate-3 construction-authority source pin, and called the real structured importer. Import succeeded. The rejection assertion failed with `AssertionError: PlannerError not raised` (one test, one expected failure). No gate or importer was mocked.

After repair the identical input raises `PlannerError: unsupported selection policy identity/version binding` before state decoding/use. The same test passes. Additional tests reject altered policies even when their bytes and caller-supplied hashes agree: class-map edits, opposite tie-break/effect rules, and unsupported extensions cannot silently become admitted policy. Direct selection and canonical native restore reject these substitutions. Wrong identity domain, profile, pointer, path, digest, unsupported version and stale policy bytes are also covered.

## Correction

- `selector.py`: closed immutable policy descriptors bind `E1-SELECTION-1`, each already-supported historical replay version, exact artifact pin, `E1-SELECTOR-RULES-1`, class priority/mappings, stage-sensitive semantic mapping, effect priority, cost/fallthrough semantics and lexical tie-break. Canonically serialized descriptors have explicit reviewed SHA-256 commitments. Admission checks the supplied pin/version against this registry and rejects descriptor/configuration drift before even singleton selection. Static selection semantics are unchanged.
- `codec.py`: shared replay admission validates this binding before graph/event replay; canonical persistence and restore use this same path. Existing byte authentication remains required at source-aware import/save/restore boundaries.
- `replay.py`: structured fixture import and frozen-manifest descriptor import admit the policy before consuming it. This is policy admission only, not C06 operational contract restoration.
- `test_planner_resume.py`: five C05 tests, plus the existing C03 altered-policy test now requires the earlier admission error. Valid C03 policy-version/context changes still fail their independent resume-event binding checks.

The exact admitted policy is `docs/experiments/E1/E1_GRAPH_RESOLUTION_SELECTION_POLICY_1.md`, raw-file-sha256 `475bef0b28d7b484ba2641c654b37e9ce3d6f6ae1b0e13dfdcadaa3f79a2a3b5`, CONTENT_IDENTITY, empty projection. Its accepted decision-input extension is retained. P01-SUBSET/P03/P04/P05/P06 remain distinct historical bundle versions, all explicitly bound to the existing reviewed selector; admission does not upgrade a version. Unsupported policy changes require explicit implementation/registry qualification.

Pure selection authenticates the admitted descriptor, not filesystem bytes. Source-aware boundaries separately authenticate bytes. An arbitrary matching content hash is therefore insufficient, and no policy text is interpreted as executable rules. Existing typed state, ledger, stale-proof and resume-proof models remain unchanged; no second persistence model was introduced.

## Validation

Full affected suite:

```sh
python3 -m unittest adapter.tests.test_planner_core adapter.tests.test_planner_invariants adapter.tests.test_planner_resume adapter.tests.test_planner_e1_replay adapter.tests.test_invocation_constructor -v
```

**142 tests PASS in 675.157 seconds**, including all 137 pre-C05 tests and five new C05 tests.

The suite covers A–N, X01–X11, C01–C04 adversarial regressions, importer, CLI, persistence/replay, cold resume, selection, global controls and constructor regressions. N remains its existing scope; this result does not close F03 or claim actual frozen-E1 operational cold-resume readiness.

Additional final-code runs under hash seeds 0, 1, 37 and 12345 each pass the five C05 tests plus case D's 49 input orders / 100 replays / reversed JSON keys. Supported-version round trips preserve canonical bytes and historical version strings. Reversing decision-input candidates still selects INPUT-BUDGET at criterion 5. Tests deliberately change implementation map/effect/tie descriptors and verify rejection through the real selector; these configuration-variant tests do not replace the enforcing path.

## Preservation

The pre-edit path/raw-SHA inventory contains all 10,911 frozen E1 files, including bytecode files. The final inventory is identical, with compact sorted inventory commitment `1cf25145f69a2fb133c12f3b15cd1089351e4a9cac8624d4b6e970f2b4b3a044`. Backlog, plans/matrices, historical qualification, prior correction results and current-status records remain unchanged. Only the four implementation/test files listed below changed; this result is the sole added source artifact. Generated caches outside E1 are excluded from the source-change inventory. Whitespace and link checks pass, including untracked-file checks because prior planner work is untracked in this checkout.

C06/C07 were not executed. No E1 resumption, authority issuance, construction, production effects or deferred capabilities occurred. Historical qualification is preserved; current status remains CORRECTION_REQUIRED.

## Report

```text
WORK_PACKAGE = C05
RESULT = PASS
FINDINGS_ADDRESSED = [F06]
FILES_ADDED = [docs/plans/DETERMINISTIC_PLANNER_V0_1_C05_RESULT.md]
FILES_MODIFIED = [adapter/planner/selector.py, adapter/planner/codec.py, adapter/planner/replay.py, adapter/tests/test_planner_resume.py]
PRE_REPAIR_COUNTEREXAMPLES = {T06/F06: REPRODUCED}
PRE_REPAIR_REGRESSIONS = {T06: FAIL_EXPECTED}
POST_REPAIR_COUNTEREXAMPLES = {T06/F06: REJECTED_CORRECTLY}
POST_REPAIR_REGRESSIONS = {T06: PASS, T-POLICY: PASS}
TESTS_PASSED = 142
AFFECTED_REPLAY_CASES = {A: PASS, B: PASS, C: PASS, D: PASS, E: PASS, F: PASS, G: PASS, H: PASS, I: PASS, J: PASS, K: PASS, L: PASS, M: PASS, N: PASS}
AFFECTED_INVARIANTS = {X01: PASS, X02: PASS, X03: PASS, X04: PASS, X05: PASS, X06: PASS, X07: PASS, X08: PASS, X09: PASS, X10: PASS, X11: PASS}
DETERMINISM_TESTS = PASS (four additional hash seeds; D permutations/replay/key reversal; supported-policy canonical round trips; decision-input reversal; existing cold-process/control tests)
C01_REGRESSION = PASS
C02_REGRESSION = PASS
C03_REGRESSION = PASS
C04_REGRESSION = PASS
FINDINGS_CLOSED = [F01, F02, F04, F05, F06]
FINDINGS_REMAINING = [F03]
NEWLY_ELIGIBLE = [C06]
NEXT_CORRECTION_PACKAGE = C06
V0_1_CURRENT_STATUS = CORRECTION_REQUIRED
E1_FILES_VERIFIED = 10911
E1_ARTIFACTS_MODIFIED = 0
DEFERRED_SCOPE_VIOLATIONS = 0
PRODUCTION_EFFECT = NO
```
