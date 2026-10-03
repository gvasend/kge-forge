# C06A retry 1 — budget profile restoration

**RESULT = PARTIAL.** The complete bounded synthetic budget profile passes; broader reconciled full-E1 import coverage remains incomplete. C07 was not executed; current qualification remains CORRECTION_REQUIRED.

## Scope and independent red proof

The [independent budget oracle](DETERMINISTIC_PLANNER_V0_1_BUDGET_PROOF_MATRIX_ORACLE_1.md) and its [JSON instance](DETERMINISTIC_PLANNER_V0_1_BUDGET_PROOF_MATRIX_ORACLE_1.json) supply the synthetic qualification contract. The original blocked [C06A result](DETERMINISTIC_PLANNER_V0_1_C06A_RESULT.md), refined [C06 result](DETERMINISTIC_PLANNER_V0_1_C06_RESULT.md), refinement and blocked C07 result remain unchanged.

Before implementation, the new regression independently evaluated the eight positive equations and exact pinned parameter contract, without importing a planner validation result as its oracle. It then called the unchanged public `replay.import_fixture` with the contract-derived synthetic input. The real importer rejected the missing profile at its schema boundary: `PlannerError: unknown or missing object fields`. The test ran once and failed as expected. This is the oracle's explicitly permitted missing-input-contract variant, not a claim that empty PASS had been incorrectly accepted or that the red run reached result validation.

No post-load state patch or mocked importer was used. The pre-repair test required a successful typed import, complete restoration and valid bounded result acceptance; its unexpected exception is FAIL_EXPECTED. The exact observation and command were captured in `/tmp/c06a_red.log`.

## Implementation and operational coverage

- [budget.py](../../adapter/planner/budget.py) implements the closed synthetic profile with strict schema/type/reference checking, the independently pinned parameter contract, eight fact/rule expressions, producer competence grants, complete envelope equality, source authentication, exact checkpoint validity, and invalidation rejection. The importer reads exact raw source members supplied by the fixture author; it does not create evidence files, repin mismatches or issue authority.
- [model.py](../../adapter/planner/model.py) adds BudgetEnvelope, BudgetProofRow and BudgetProofMatrix to the existing Snapshot. Decoding verifies complete typed rows, their exact source identities, envelope, content identity, required evidence dependencies, consumer predicate and result contract. Removing the matrix or any necessary binding is rejected before use.
- [codec.py](../../adapter/planner/codec.py) canonically persists the additive state. Empty additions preserve older snapshot encodings. Native ledger/source verification and stale propagation remain the existing mechanisms. A budget qualification matrix cannot be relabeled as FULL_FROZEN_E1_REPLAY.
- [replay.py](../../adapter/planner/replay.py) dispatches the new `PLANNER-BUDGET-QUALIFICATION-1` input through the public importer. Actual `import_e1` is unchanged. The qualification snapshot has a historically BLOCKED producer, an eligible bounded FACT action, and a separate synthetic reevaluation continuation. It retains unresolved root/slot objects and explicit goals.
- [test_planner_c06a.py](../../adapter/tests/test_planner_c06a.py) provides the independent positive equations, complete member checks, semantic negatives, restore tampering, source invalidation, cold processes, permutations and CLI checks.

The exact scoped PASS result contains the complete proof-matrix knowledge contract: source-authentication reference, parameter identity, full typed envelope, anchor, eight source/rule/PROVED rows and invalidation set. Its content identity is independently checked. Complete supplied result acceptance uses existing `gates.validate_result` and `core.apply_result`; it does not satisfy the root or slot. Only the named synthetic continuation becomes eligible; it is not executed.

All 17 source/rule/authentication records, the parameter record, and the submitted matrix are raw pinned dependencies. The action-definition plan is also independently pinned, not hashed and silently adopted from changed bytes. Each dependency remains effective after canonical reload. Missing members cannot be hidden by a matching actionable set. The [coverage companion](DETERMINISTIC_PLANNER_V0_1_C06A_RETRY_1_COVERAGE.json) records code/oracle identities and the implemented boundary.

## Source validity and refined C06 preservation

The importer invokes the existing `restore_accepted_knowledge` for the pinned REEVAL-BUDGET BLOCKED result. Qualified accepted knowledge remains usable while its producer is BLOCKED. Invalidation of that source separately blocks FACT; it does not require a fabricated producer COMPLETED state. The exact existing candidate is rerun independently.

For the matrix itself, invalidating any of its 19 required source assertions after reload makes its knowledge prerequisite unproved and dependent actionability non-runnable. SourceInvalidation events persist through the existing append-only ledger and cold restore. A saved acceptance flag or reordered bytes cannot refresh stale proof. This partial fixture has no new external recovery authority; it does not invent a revalidation route after invalidation.

## Remaining package boundary and C07 predicate

This retry implements the budget proof profile requested under the oracle. It does **not** replace the full frozen-E1 M normalization or complete all original C06A restoration families. The [reconciliation](DETERMINISTIC_PLANNER_V0_1_C06_C07_RECONCILIATION_1.md) still requires source-driven full action/decision/dossier/authority/history/root/slot/frontier contracts, an independent complete field-coverage inventory, supported decision-route tests and full semantic N-REAL acceptance.

Accordingly the overall C06A classification is PARTIAL even if the bounded budget tests pass. `FULL_IMPORT_CONTRACT` for the broader reconciled package is not passed. Legacy N regression success is not represented as the stronger N-REAL gate. No finding is reopened: F03 remains CLOSED under the accepted refined repair.

| C07 retry conjunct | Result |
|---|---|
| Explicit adoption of C06A / oracle | Satisfied by user instructions |
| Preserve C01–C06 scopes and refined F03 | Preserved; regression evidence recorded below |
| C06A PASS with complete O01–O17 contract coverage | Not satisfied: this is partial budget-profile coverage |
| Required full-import positive/negative tests including decision route and full N-REAL | Not satisfied by this scoped profile |
| Source preservation and no remaining acceptance gap | Preservation verified separately; broader acceptance gaps remain |

`C07_RETRY_ALLOWED = NO` follows from the failed conjunction, regardless of budget test count. The next operation is remaining C06A full-import contract work, not C07 or final requalification. No implementation outside this bounded profile was attempted.

## Validation evidence

The integrated regression command passed **156 tests in 1100.265 seconds**:

```sh
python3 -m unittest adapter.tests.test_planner_core adapter.tests.test_planner_invariants adapter.tests.test_planner_resume adapter.tests.test_planner_e1_replay adapter.tests.test_planner_c06 adapter.tests.test_planner_c06a adapter.tests.test_invocation_constructor -v
```

This includes A–N legacy replay, X01–X11, C01–C06, importer/CLI, native persistence/cold restore, selector, global controls and constructor regressions. The exact unchanged `adapter.tests.counterexamples.c06_f03_candidate` separately passed **4 tests in 102.340 seconds**; the standalone invariant suite passed **39 tests in 7.760 seconds**. The final focused budget run passed **6 tests in 26.919 seconds**, including the additional noncanonical embedded-contract rejection. These supporting reruns are not counted as additional distinct tests.

The budget tests include 23 negative semantic/schema mutations; independently admitted negative variants recompute their synthetic record/grant hashes before checking the row equations, so they do not merely fail an old checksum. The public importer additionally rejects unregistered parameter substitutions. Every required matrix source is invalidated separately after reload. Tests check each row's source/rule identity, every envelope field, all retained records, result fields/content identity, root/slot preservation, and rejected removal of contract metadata. Three fresh-process seeds (0, 31, 777), proof/record permutation, key reversal, repeated import/recompute, native ledger reload and repeated CLI output agree. No fabricated authority or real E1 receipt enters these tests.

An earlier integrated run started during development and ended with four new-profile errors from old/new in-process model versions; it is not acceptance evidence. The subsequent integrated command above passed on the settled implementation. A final canonical-contract rejection was checked by the focused rerun; existing historical results are not rewritten. Logs are identified in the coverage companion with hashes.

## Preservation and final report

All 10,911 frozen E1 paths and raw SHA-256 values match the pre-repair inventory. Existing backlog, plans/matrices, qualification and correction/oracle result artifacts remain unchanged. Only the three modified implementation files, the new budget module/test, and this retry result/coverage companion changed (generated non-E1 Python caches excluded). Raw synthetic source members are temporary qualification inputs outside E1. No runtime effect, E1 resumption, external evidence acquisition or authority issuance occurred. The frozen budget branch remains WAITING_FOR_EXTERNAL_EVIDENCE.

No GraphRAG, LLM, service, database, UI or generalized optimization was introduced. `git diff --check`, untracked-source whitespace checks, JSON parsing, artifact links and source-preservation checks passed.

```text
WORK_PACKAGE = C06A
ATTEMPT = RETRY_1
RESULT = PARTIAL
ORACLE_INDEPENDENCE = PASS
POSITIVE_ORACLE = PASS
NEGATIVE_ORACLE = PASS
PRE_REPAIR_COUNTEREXAMPLE = REPRODUCED (missing profile rejected at public import boundary)
PRE_REPAIR_REGRESSION = FAIL_EXPECTED
POST_REPAIR_COUNTEREXAMPLE = REJECTED_CORRECTLY (restoration loss prevented; valid matrix accepted)
POST_REPAIR_REGRESSION = PASS
BUDGET_PROFILE_IMPORT_CONTRACT = PASS
FULL_IMPORT_CONTRACT = FAIL (broader reconciled O01–O17 coverage remains incomplete)
OPERATIONAL_RESTORATION = PASS (complete scoped budget profile only)
REFERENCE_INTEGRITY = PASS
SOURCE_INVALIDATION = PASS
TESTS_PASSED = 156 integrated; supporting reruns: 4 refined C06, 39 invariants, 6 budget
E1_REPLAY_CASES = {A: PASS, B: PASS, C: PASS, D: PASS, E: PASS, F: PASS, G: PASS, H: PASS, I: PASS, J: PASS, K: PASS, L: PASS, M: PASS, N: PASS}
NEGATIVE_INVARIANTS = {X01: PASS, X02: PASS, X03: PASS, X04: PASS, X05: PASS, X06: PASS, X07: PASS, X08: PASS, X09: PASS, X10: PASS, X11: PASS}
C01_C06_REGRESSIONS = PASS
F03_STATUS = CLOSED
DETERMINISM_TESTS = PASS
COLD_RESUME = PASS (native budget profile and legacy N; not full reconciled N-REAL)
PERSISTENCE_ROUND_TRIP = PASS
REAL_E1_EVIDENCE_CREATED = NO
C07_RETRY_ALLOWED = NO
C07_RETRY_PREREQUISITES = [complete remaining full-import contracts and field coverage, supported decision-route tests, full semantic N-REAL, C06A PASS against reconciled gate]
V0_1_CURRENT_STATUS = CORRECTION_REQUIRED
E1_ARTIFACTS_MODIFIED = 0
DEFERRED_SCOPE_VIOLATIONS = 0
PRODUCTION_EFFECT = NO
```

