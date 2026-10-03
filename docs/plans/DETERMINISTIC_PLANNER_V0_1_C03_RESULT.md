# Deterministic Planner v0.1 — C03 result

C03 addresses F02 / RC-RESUME-PROOF under the [correction plan](DETERMINISTIC_PLANNER_V0_1_CORRECTION_PLAN_1.md), section 5, and [correction matrix](DETERMINISTIC_PLANNER_V0_1_CORRECTION_MATRIX_1.md). [C01](DETERMINISTIC_PLANNER_V0_1_C01_RESULT.md) and [C02](DETERMINISTIC_PLANNER_V0_1_C02_RESULT.md) are accepted prerequisites. Repository assumptions matched the plan. No CORRECTION_PLAN_MISMATCH was found.

Current qualification remains CORRECTION_REQUIRED. Historical qualification and all E1 state remain unchanged.

## Pre-repair proof

T02 was reproduced before implementation edits through the actual K-derived synthetic receipt lifecycle: REQUEST_READY → WAITING → RECEIVED → VALIDATED → REENTRY. Invalidating TEST-TRUST's provenance through `invalidate_sources` made `external_complete` false and ACTIONABLE empty while `plan_output` still returned `resume_allowed=true`. The new regression failed exactly on `True is not false`. No mock bypassed receipt authentication, invalidation, recomputation or output.

The same counterexample now denies resume. An additional native-ledger version records reentry followed by source invalidation, persists it, and restores it in a fresh process. Historical reentry remains in the gate history, while current eligibility is false with obligation, attestor and named-action reasons.

## Implementation

`core.resume_eligibility(bundle, source_root=None)` is the shared pure computation. It returns typed `ResumeEligibility`: allowed, eligible named ActionIds, remaining reasons, and supporting typed identities. `replay.plan_output` uses it; the CLI passes its source root to that same path. Restore output recomputes from the restored bundle, not a saved Boolean.

The computation verifies the native ledger and current state through the existing codec; recomputes actionability; requires the route's accepted reentry event; verifies its exact policy/context binding; rechecks the receipt contract and each current proof obligation; and requires the exact incomplete, unheld named action to remain actionable. Every applicable shared gate must have its own qualifying route proof. An unrelated waiting branch does not veto an independently eligible route. Missing evaluation context or source-pin verification prevents permission. Invalid structured state fails admission instead of being converted to an eligible route.

Native reentry events now carry an optional typed `resume_binding`, included in their immutable event hash. It commits to the exact policy pin, policy version and run scope. The event's existing pre-state and parent-event identities bind the contract, target, context, evidence, admission, observations and original action requirements. Existing ledger replay independently verifies that sequence. An old event without the new binding still replays as historical evidence but cannot authorize resume; no permissive migration is performed.

A typed `SourceInvalidation` event records exact source identities and pre-state identity through the existing append-only ledger. It applies the existing C02 invalidation function and cannot produce evidence, grant authority or reset qualifications. This makes loss of current proof replayable without erasing an accepted historical reentry. No parallel planner/persistence model or trusted resume cache was introduced.

Generic admitted decision reentry uses the existing RecordedDecision/DecisionReentry contract and current decision validation; it does not fabricate an external receipt. Its native reentry event receives the same exact-context binding. The existing counterfactual decision test now checks no permission before reentry and permission only for the named downstream action afterward.

Source verification is read-only. Callers without a source root receive `SOURCE_VERIFICATION_REQUIRED` for an otherwise eligible route. The CLI supplies its configured root. Synthetic positive tests materialize their explicitly synthetic pins in temporary roots. They neither supply real E1 evidence nor resume E1.

The additive codec field defaults to absent for historical events; their canonical bytes and hashes remain valid. A new event with a resume binding hashes that binding. Unknown fields, including a supplied `resume_allowed` cache, remain rejected by the existing closed codec.

## Tests

Eight new tests plus strengthened existing decision-reentry assertions cover:

- Exact T02 pre-repair failure and post-repair denial.
- Complete native positive proof, source verification, stale independent attestor, unchanged lifecycle history, canonical persistence, fresh-process API and CLI equality, and source-byte tampering.
- Missing native event, legacy event without binding, changed policy identity/version/scope, original unresolved prerequisites, and a completed named action.
- Partial, negative, unrelated and conflicting evidence; missing admission; expired evidence; wrong target; and current-state contract/context tampering.
- Multiple gates on one route; a shared gate with only fabricated phase/history text; and a genuinely independent waiting branch.
- C02 stale ordering after accepted reentry, retaining historical phase while persisting a current hold.
- Reversed source-pin ordering, canonical reload, and fresh-process hash seeds 1, 7 and 42.
- A supplied saved-true field cannot substitute for proof.

The full regression command is:

```sh
python3 -m unittest adapter.tests.test_planner_core adapter.tests.test_planner_invariants adapter.tests.test_planner_resume adapter.tests.test_planner_e1_replay adapter.tests.test_invocation_constructor -v
```

Final full run: **131 tests PASS in 674.836 seconds**, including all 123 pre-C03 tests and eight new tests.

These are C03 closure and regression results, not final requalification. Existing N passes do not close F03. Exact policy-context binding here does not implement C05's semantic qualification of policy contents/version. F05's cross-domain control ordering is also unchanged. Imported historical checkpoint-to-contract restoration remains C06 work; unproven imported stage text never authorizes resume.

## Preservation

A pre-edit complete path/raw-SHA256 inventory contains all 10,911 frozen E1 files, including their bytecode files. Every path and byte remains unchanged after testing. The frozen inventory SHA-256 is `1cf25145f69a2fb133c12f3b15cd1089351e4a9cac8624d4b6e970f2b4b3a044`, using sorted compact UTF-8 JSON of the path-to-raw-SHA256 map.

Backlog, implementation/correction plans, matrices, historical qualification, authority records and C01/C02 results are unchanged. Only the assigned implementation/test files listed below changed, and this result is the only new repository file. Source-file inventory checks exclude generated caches outside E1. `git diff --check`, separate whitespace checks of previously untracked changed files, and result-document links pass.

## Report

```text
WORK_PACKAGE = C03
RESULT = PASS
FINDINGS_ADDRESSED = [F02]
FILES_ADDED = [docs/plans/DETERMINISTIC_PLANNER_V0_1_C03_RESULT.md]
FILES_MODIFIED = [adapter/planner/model.py, adapter/planner/core.py, adapter/planner/codec.py, adapter/planner/replay.py, adapter/planner/__main__.py, adapter/tests/test_planner_invariants.py, adapter/tests/test_planner_resume.py, adapter/tests/test_planner_e1_replay.py]
PRE_REPAIR_COUNTEREXAMPLES = {T02/F02: REPRODUCED}
PRE_REPAIR_REGRESSIONS = {T02: FAIL_EXPECTED}
POST_REPAIR_COUNTEREXAMPLES = {T02/F02: REJECTED_CORRECTLY}
POST_REPAIR_REGRESSIONS = {T02: PASS, T-RESUME: PASS}
TESTS_PASSED = 131
AFFECTED_REPLAY_CASES = {A: PASS, B: PASS, C: PASS, D: PASS, E: PASS, F: PASS, G: PASS, H: PASS, I: PASS, J: PASS, K: PASS, L: PASS, M: PASS, N: PASS}
AFFECTED_INVARIANTS = {X01: PASS, X02: PASS, X03: PASS, X04: PASS, X05: PASS, X06: PASS, X07: PASS, X08: PASS, X09: PASS, X10: PASS, X11: PASS}
DETERMINISM_TESTS = PASS (C03 scope; source ordering, canonical reload, fresh-process seeds 1/7/42; inherited selector/key-order tests)
C01_REGRESSION = PASS
C02_REGRESSION = PASS
F01_STATUS = CLOSED
F04_STATUS = CLOSED
FINDINGS_CLOSED = [F01, F02, F04]
FINDINGS_REMAINING = [F03, F05, F06]
NEWLY_ELIGIBLE = []
NEXT_CORRECTION_PACKAGE = C04
V0_1_CURRENT_STATUS = CORRECTION_REQUIRED
E1_FILES_VERIFIED = 10911
E1_ARTIFACTS_MODIFIED = 0
DEFERRED_SCOPE_VIOLATIONS = 0
PRODUCTION_EFFECT = NO
```

C04 and C05 were already independently eligible. C03 satisfies one prerequisite of C06, which still waits for C04/C05. The plan's lexicographic scheduling rule selects C04 next. No next package was executed.
