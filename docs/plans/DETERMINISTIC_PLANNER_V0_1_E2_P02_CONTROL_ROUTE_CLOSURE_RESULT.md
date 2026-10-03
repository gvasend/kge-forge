# Deterministic Planner v0.1 — E2-P02 Control-Route Closure

## Result

`E2-P02-CONTROL-ROUTE-CLOSURE = PASS`.

The counterexample was a missing native decision-input route, not a Planner
runtime defect. The qualified source model already declares the
`E2-PREPARE` dossier for decision `E2-DECIDE`; the whole-model materializer
had omitted the corresponding typed `Decision` route. The materializer now
derives that route from the source dossier and prerequisite graph.

The route is an internal decision-input acquisition route. It does not create
decision input, mark `E2-PREPARE` complete, or bypass any decision, proof,
authority, evidence, or reentry gate.

## Route contract

| Field | Value |
|---|---|
| Route ID | `DecisionRoute:E2-DECIDE:E2-PREPARE` |
| Route type | `INTERNAL_DECISION_INPUT_ACQUISITION` |
| Source | qualified `E2-PREPARE` dossier; required facts `E2-K-CHECK`, `E2-K-COLLECT` |
| Target | `E2-PREPARE` |
| Decision action | `E2-DECIDE` |
| Semantic action | `E2-DECIDE` |
| Stage | `DECISION_INPUTS_REQUIRED` |
| Downstream | `E2-REENTER` |
| Scope / lineage | `E2-QUALIFICATION-ONLY` / `E2-CANONICAL-BASELINE-1` |
| Admission | native `validate_model` Decision route checks |
| Fail closed | absent, malformed, stale, or mismatched route remains a control defect |

The route is derived generically: each source Action with a qualified
`prepared_dossier` supplies its dossier decision; downstream Actions are the
Actions whose typed prerequisites name that decision. No E2 ActionId-specific
special case was added.

## Qualification and impact

The pre-repair counterexample remains preserved in
`DETERMINISTIC_PLANNER_V0_1_E2_P02_RETRY_1_TRACE.json`. Its two successful
CHECK/COLLECT results are historical evidence; they were not regenerated or
rewritten. The old model/snapshot and its post-COLLECT control result are
invalid for the corrected model because they contain no Decision route.

The corrected native snapshot is:

`33c0bb5c4ed55496cde6ec0ce3eb5ee74307872697d8202a06db65c2c731e9b5`

It is `PLANNER-SNAPSHOT-1`, and native encode/decode plus semantic round-trip
pass. The P01 whole-model oracle, O01/source-role admission, policy binding,
composition negatives, and deterministic identity checks pass with the route.

Preserved evidence includes the six Action definitions, generic prerequisite
repair, PC01–PC04 qualification outside the route-dependent cone, E2-T01,
and the original CHECK/COLLECT counterexample trace. Requalification is
limited to the route, whole-model identity, initial/reached actionability,
selection, and P02 phase expectations.

## Replayed reached state

From the corrected snapshot, ordinary native execution replays:

1. `E2-CHECK` → `PASS`, knowledge `E2-K-CHECK`.
2. `E2-COLLECT` → `PASS`, knowledge `E2-K-COLLECT`.

Both transition oracles pass. At the post-COLLECT state:

```text
ACTIONABLE = [E2-PREPARE]
SELECTED   = E2-PREPARE
CONTROL    = RUNNABLE
DEFECTS    = []
```

`E2-PREPARE` is now reachable through its completed CHECK/COLLECT
prerequisites and the typed route. It is not executed in this package.
`E2-DECIDE` remains blocked by `ACTION_COMPLETED:E2-PREPARE` and
`DECISION_NOT_READY`; reentry remains separately gated by decision,
authority, evidence, proof, and external-route semantics.

## Gates

`MISSING_CONTROL_ROUTE:E2-PREPARE` is closed. No new runtime defect was
established. The corrected snapshot is the only valid future P02 input;
the prior snapshot remains historical evidence and must not be reused.

`E2_P02_RETRY_ALLOWED = YES` for the next P02 retry, subject to the existing
P02 contract. `E2_P03_READY = NO`; P02 itself has not passed. N-REAL remains
unsatisfied, E1 remains frozen, and no experiment Action beyond the bounded
CHECK/COLLECT replay was executed here.

```text
WORK_PACKAGE = E2-P02-CONTROL-ROUTE-CLOSURE
RESULT = PASS
COUNTEREXAMPLE = MISSING_CONTROL_ROUTE:E2-PREPARE
CHECK_REPLAY = PASS
COLLECT_REPLAY = PASS
POST_COLLECT_ACTIONABLE = [E2-PREPARE]
POST_COLLECT_SELECTED = E2-PREPARE
POST_COLLECT_CONTROL = RUNNABLE
MISSING_CONTROL_ROUTE_CLOSED = YES
NEW_RUNTIME_DEFECTS = []
E2_P02_RETRY_ALLOWED = YES
E2_P03_READY = NO
N_REAL_SATISFIED = NO
CANONICAL_E2_QUALIFIED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
```
