# Deterministic Planner v0.1 — E2-P02 Retry 2

## Result

`E2-P02 = PARTIAL`.

The corrected snapshot and the closed control route reproduce the qualified
CHECK/COLLECT prefix and expose `E2-PREPARE` normally. Native Planner then
rejects the supplied PASS result for `E2-PREPARE` because the materialized
result contains no independently admitted `DecisionDossier`. This is a
fixture/materialization gap, not a Planner runtime defect.

P02 stopped at that boundary. No decision, external evidence, or P03
transition was executed.

## Pinned input and prefix

```text
SNAPSHOT_FORMAT = PLANNER-SNAPSHOT-1
PINNED_INITIAL_SNAPSHOT = 33c0bb5c4ed55496cde6ec0ce3eb5ee74307872697d8202a06db65c2c731e9b5
INITIAL_ORACLE = actionable [E2-CHECK,E2-COLLECT], selected E2-CHECK, RUNNABLE
E2-FINISH = NON_ACTIONABLE
```

The initial snapshot decodes and round-trips successfully. Native selection
chooses the expected Action at each reached state.

## Trace

1. `E2-CHECK` → `PASS` → `E2-K-CHECK`.
2. `E2-COLLECT` → `PASS` → `E2-K-COLLECT`.
3. Post-COLLECT state: actionable `[E2-PREPARE]`, selected `E2-PREPARE`,
   control `RUNNABLE`.
4. The native `SuppliedResult(E2-PREPARE, PASS, ...)` is rejected with:
   `input PASS requires complete independently proved dossier`.

The qualified route itself passes: `DecisionRoute:E2-DECIDE:E2-PREPARE`,
stage `DECISION_INPUTS_REQUIRED`, source facts `E2-K-CHECK` and
`E2-K-COLLECT`, downstream `E2-REENTER`. The failure occurs when the
decision-input result is admitted, because the snapshot Action/result
materialization does not carry the source-declared dossier into the supplied
result.

## Counterexample and scope

```text
FAILURE_CLASS = RESULT_MISMATCH
COUNTEREXAMPLE = P02-PREPARE-001
ERROR = input PASS requires complete independently proved dossier
```

This is the native contract’s expected fail-closed behavior. The source
fixture already contains the dossier; the corrected next package must bind
that dossier through the qualified decision-input route and independently
prove its required facts/checks. No dossier, decision readiness, authority,
or evidence was fabricated here.

The earlier CHECK/COLLECT evidence and route closure remain valid. The P02
target `EXTERNAL_WAIT` was not reached, so the exit predicate is false.

```text
CHECK_COLLECT_PREFIX = PASS
PREPARE_ROUTE = PASS
P02_TARGET_STATE = EXTERNAL_WAIT (NOT REACHED)
P02_EXIT_PREDICATE = FALSE
PREREQUISITE_ENFORCEMENT = PASS
TRANSITION_ORACLES = CHECK/COLLECT PASS; PREPARE admission blocked
PROVENANCE = PASS for reached results; dossier missing at admission
REPLAY = NOT RUN AFTER FAILED PREPARE ADMISSION
DETERMINISM = PASS for initial and reached states
COUNTEREXAMPLES = [P02-PREPARE-001]
NEW_RUNTIME_DEFECTS = []
E2_P02_RESULT = PARTIAL
E2_P03_READY = NO
NEXT_PACKAGE = E2-P02-DECISION-DOSSIER-CLOSURE
N_REAL_SATISFIED = NO
CANONICAL_E2_QUALIFIED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
```
