# E2-P04 A09 receipt control-transition reconciliation

WORK_PACKAGE = E2-P04-A09-CONTROL-RECONCILIATION  
RESULT = PASS

The failure was an **overstrict precommit oracle**, not an actual control transition. For the exact I04 input, pre-A09, simulated post-A09 and independently expected post-A09 control are all **EXTERNAL_WAIT**. The old assertion compared the entire Computation and rejected changed blocker diagnostics. A bounded generic correction now passes complete execution-level precommit against all 18 independent oracle terms. **A09_READY = YES; P04_EXECUTION_READY = NO.** No canonical A09 transaction committed.

## Authoritative contracts and independent oracle

The original [acceptance matrix](DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_ACCEPTANCE_MATRIX_1.md), sections E2-A09 and E2-A10, governs phase ownership. A09 independently authenticates bytes/producer/claims, then records EVIDENCE_RECEIVED. Its postcondition is admitted source, gate pending artifact, and no accepted ReceiptObservation or resume. A10 starts with received, current scoped source and authentic independent claims; it separately performs EVIDENCE_VALIDATED through append_event. Accepted observations/external completion are A10 work; named reentry is A11 and actual REENTER selection/result is A12.

[E03](DETERMINISTIC_PLANNER_V0_1_EVIDENCE_E03_LIFECYCLE_RESULT.md) additionally requires received Evidence to have `validated = FALSE`, `ValidationState = NOT_EVALUATED`, no proof, and derived blocked Action statuses. Its qualified received-only boundary recomputes EXTERNAL_WAIT. Gate contract `validation = ACCEPTED` is distinct from Evidence validation.

The canonical matrix does not explicitly name a new post-A09 control enum. For this sealed fixture, control is **DERIVABLE**, rather than an invented RUNNABLE validation state: no A10 validation Action is declared; the independent Evidence proof and accepted named reentry are absent; and the unsatisfied goal path still exposes its qualified EXTERNAL_EVIDENCE boundary. `governed_external_unknown` explicitly covers EVIDENCE_RECEIVED without supplying a positive proof. Receipt fixes absence of bytes but does not resolve the governing-rule validation/proof dependency causing the wait.

The [independent oracle](qualification/E2_P04_A09_CONTROL_RECONCILIATION_1/independent-oracle.json) was sealed before simulation and before runtime modification:

| Domain | PRE_A09 | POST_A09 / PRE_A10 |
|---|---|---|
| Evidence | Absent | Exact authenticated entity, RECEIVED; NOT_EVALUATED |
| Receipt | None for this entity; pending absent | One exact authenticated admission; pending identifies received entity |
| External stage | WAITING_FOR_EXTERNAL_EVIDENCE | EVIDENCE_RECEIVED |
| Validation / proof | Absent | Absent; no accepted observation |
| Reentry / REENTER completion | False | False |
| REENTER / FINISH | Not actionable | Not actionable; derived statuses BLOCKED |
| Root/slot/knowledge | Qualified input inventory | Unchanged |
| Actionable / selected / decision-ready | Empty / none / empty | Empty / none / empty |
| CONTROL | EXTERNAL_WAIT | EXTERNAL_WAIT |

A10's **receipt-stage prerequisite is ready** and its next legal external stage is EVIDENCE_VALIDATED. That does not create a scheduler Action or make all A10 inputs executable. The prospective current validation definition and event-bearing validation composition still require closure/installation authority. Thus `VALIDATION_READY_AFTER_RECEIPT = NO` denotes complete operational readiness, while `VALIDATION_RECEIPT_PREREQUISITE_READY = YES` records the satisfied lifecycle prerequisite. This preparation gap is not the cause of the A09 control assertion failure.

## Exact reproduction and equality-check purpose

The input remains the published [I04 post-ATTEST bundle](DETERMINISTIC_PLANNER_V0_1_E2_P04_POST_ATTEST_INSTALL_BUNDLE_1.json):

- Bundle: `fa86ce94d76651ce5eccfa76c2d862243548d6d8dcaae91e74dca4e9c571c7d1`
- State: `c5c85434ddfb69be7f327e9e8fd72d2c7270505cf4908ea4fd9b4918075c1591`
- Parent: `549e41859f55cd3414d91b5ce97f023ab9e150f55ed01ae81a9a9dc5ef2f362c`

The [pre-repair trace](qualification/E2_P04_A09_CONTROL_RECONCILIATION_1/diagnose-trace.json) reproduces RECEIPT_CHANGED_CONTROL with all 18 independent post-receipt oracle terms passing. Only `Computation.blocked` changes:

| Action | Pre diagnostic | Post diagnostic |
|---|---|---|
| E2-REENTER | DECISION_REENTRY_REQUIRED; EXTERNAL_GATE:E2-GATE; PREDICATE:E2-PROOF:UNKNOWN | PRIOR_ATTEMPT_HOLD:BLOCKED |
| E2-FINISH | ACTION_COMPLETED:E2-REENTER | PRIOR_ATTEMPT_HOLD:BLOCKED |

E03's native admission publishes recomputed blocked statuses. The next `core._actionability` recomputation uses its existing prior-attempt hold branch. The control enum, actionable population, selection, branches and frontier do not change. This is not evidence of premature validation, reentry or FINISH.

The old `codec.preflight_external_evidence` assertion required full `recompute(pre) == recompute(post)`. Its source of expectation was a legacy runtime assertion intended to prohibit unauthorized planning/lifecycle advancement, not an authoritative demand for unchanged blocker diagnostics. It was neither the stale-parent guard nor the atomic-publication guard; both are separate and remain in force. The error label incorrectly suggested unequal control.

CLASSIFICATION = PRECOMMIT_ORACLE_DEFECT. No new control enum, A10 Action or A10 route was invented. Control is derived from canonical receipt state, not forced to match the input.

## Bounded generic correction

The [bounded repair contract](qualification/E2_P04_A09_CONTROL_RECONCILIATION_1/bounded-repair-contract.json) was sealed after the complete diagnosis and before editing runtime.

`evidence_transaction.receipt_oracle` computes only an expected postcondition from the immutable pre-state and authenticated request **before native simulation**: one unvalidated Evidence entity, its exact authenticated receipt association, target gate RECEIVED/pending/history, and E03's ordinary derived status projection. Every other canonical field is preserved. This helper is an oracle, not a receipt execution or publication path.

The actual private state continues to come exclusively from ordinary native EvidenceSourceAdmission and ExternalEvent application. After complete replay verification, the transaction compares its canonical snapshot identity and full native Computation against the expected **post-state**, rather than against the pre-state. Native-declared unordered collections use canonical identities; event/gate histories remain causal and ordered. The correction has no E2/P04 IDs or special cases.

The exact frame rejects validation instances, accepted observations, typed proof/contracts, reentry, newly completed/actionable Actions, knowledge, root/slot changes, configuration changes, foreign context and incorrect authentication associations. Authentication, source pins, exact four-record provenance, command/typed operand, parent/pre-state, transient E02 boundary, atomic HEAD publication, idempotence and replay checks are retained. Core, gates, Evidence E03 semantics, model and authority contracts were not modified.

Only `adapter/planner/codec.py` and `adapter/planner/evidence_transaction.py` changed from the pre-work runtime. No native state or Action status was set by the qualification procedure.

## Requalification and future persistence oracle

The [requalification trace](qualification/E2_P04_A09_CONTROL_RECONCILIATION_1/requalify-trace.json) reports full A09 execution-level precommit **PASS**, all 18 oracle terms PASS, and the exact canonical input unchanged. The transient attestation remains in memory; only identities/check outcomes are archived for canonical P04. No new post-A09 canonical bundle was published.

- **53 targeted tests PASS:** ten receipt-postcondition/E07 tests; 40 installation, authentication, T01/T01-D, E01-E06, G01-G04 and root/slot regressions; three receipt lifecycle/persistence/replay tests.
- **72 independent fresh-reader comparisons PASS** on the archived committed non-E2 E07 fixture. Replay is forbidden from calling new E02 attestation materialization.
- Failure injection retains atomic no-partial-head semantics. A rejected postcondition publishes neither new source nor HEAD.
- Sixteen postcondition tamper cases reject receipt-to-validation/proof/reentry, Action completion/actionability, knowledge/root/slot/configuration/context changes, authentication substitution and causal-history reversal.

For a future committed A09 checkpoint, cold restore and historical replay must reproduce the same exact received-only inventory and **EXTERNAL_WAIT**, without performing A10 or another attestation decision. The corrected generic transactions satisfy this oracle, including the isolated fixture with changing blocker diagnostics. Canonical P04 cold restoration/replay **after A09 commit was not performed**, because A09 remains unexecuted.

The legacy Evidence-admission suite now has **17 PASS, 1 FAIL, 2 ERROR**, compared with E07's 4 PASS, 4 FAIL, 12 ERROR. The remaining source-shaped fixture still fails FIELD_PROVENANCE. Two old validation tests now reach their later assertions and assume an external validation event alone validates the E03-unvalidated entity. The unchanged native check instead returns EVIDENCE_MISSING_OR_UNVALIDATED, rejects observation acceptance and preserves false resume. See the [legacy classification](qualification/E2_P04_A09_CONTROL_RECONCILIATION_1/legacy-classification.json). Those tests and lifecycle validation were not weakened to obtain a broad-suite PASS. E07's pre-existing DecisionDossier finding and frozen-E1 duplicate-import collection blocker remain separately recorded.

## Continuation readiness and preservation

A09_READY = YES, but P04_EXECUTION_READY = NO. A10 still requires a complete/current validation contract, typed installation support, bounded installation authority and native event-bearing validation composition. A11 proof/named-reentry, A12 accepted REENTER result inventory, and A13 root/slot/finishing-result contracts remain preparation dependencies. No unrelated definition was installed. Any future configuration event stales the uncommitted A09 operand and requires rematerialization against its new append head.

NEXT_PACKAGE = P04-A10-VALIDATION-INSTALLATION-CONTRACT.

The [preservation record](qualification/E2_P04_A09_CONTROL_RECONCILIATION_1/preservation.json) verifies 10,967 frozen E1 files unchanged, and every prior qualification artifact—including P03, I04 and E07—unchanged. P03 remains PASS, historical correspondence remains UNPROVEN, and N-REAL remains NO. No release qualification is inferred. `git diff --check` passes.

```text
WORK_PACKAGE = E2-P04-A09-CONTROL-RECONCILIATION
RESULT = PASS
PRE_A09_CONTROL = EXTERNAL_WAIT
SIMULATED_POST_A09_CONTROL = EXTERNAL_WAIT
EXPECTED_POST_A09_CONTROL = EXTERNAL_WAIT
A09_POSTCONDITION = RECEIVED_ONLY
A10_INITIAL_CONTRACT = RECEIVED_CURRENT_AUTHENTIC_SOURCE; SEPARATE_VALIDATION
RECEIPT_RESOLVES_EXTERNAL_WAIT = NO
VALIDATION_READY_AFTER_RECEIPT = NO
VALIDATION_RECEIPT_PREREQUISITE_READY = YES
PRECOMMIT_CONTROL_CHECK = EXACT_POSTCONDITION_AND_NATIVE_COMPUTATION
PRECOMMIT_CHECK_PURPOSE = NO_UNAUTHORIZED_LIFECYCLE_ADVANCEMENT
LIFECYCLE_SEPARATION = PASS
CLASSIFICATION = PRECOMMIT_ORACLE_DEFECT
MINIMUM_CORRECTION = GENERIC_RECEIVED_ONLY_POSTCONDITION_ORACLE
CORRECTION_APPLIED = YES
E07_REGRESSION = PASS
E03_REGRESSION = PASS
A09_EXECUTION_PREFLIGHT = PASS
A09_READY = YES
P04_EXECUTION_READY = NO
NEXT_PACKAGE = P04-A10-VALIDATION-INSTALLATION-CONTRACT
A09_A13_EXECUTED = NO
E2_FINISH_EXECUTED = NO
P03_RESULT = PASS
P03_HISTORICAL_CORRESPONDENCE = UNPROVEN
N_REAL_SATISFIED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
```

The [machine-readable companion](DETERMINISTIC_PLANNER_V0_1_E2_P04_A09_CONTROL_RECONCILIATION_1.json) includes both control traces, recovered contracts, independent oracle, check-purpose/classification, bounded correction, regressions and continuation DAG.
