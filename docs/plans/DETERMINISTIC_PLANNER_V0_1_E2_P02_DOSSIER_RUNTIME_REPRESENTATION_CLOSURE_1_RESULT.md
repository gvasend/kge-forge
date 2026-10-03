# E2-P02 Dossier Runtime Representation Closure

## Result

`E2-P02-DOSSIER-RUNTIME-REPRESENTATION-CLOSURE = BLOCKED`.

Two distinct gaps were confirmed:

1. `prepared_dossier` is already a native field on `Action` and
   `SuppliedResult.dossier`; the E2 materializer omitted the authoritative
   dossier binding. This is an `E2_MATERIALIZER_OMISSION`.
2. Native dossier admission evaluates predicate IDs already present in the
   snapshot. There is no supported runtime transaction that creates the six
   evaluated validation predicate instances after PREPARE. This is a
   `MISSING_NATIVE_RUNTIME_CAPABILITY` / representation gap.

No implementation was changed because the second gap requires a complete
runtime contract for durable, replayable validation-result admission.

## Native lifecycle

The supported shape is:

```text
SuppliedResult.dossier
    -> Action.prepared_dossier correspondence
    -> Decision.dossier
    -> snapshot.predicates referenced by DecisionCheck
    -> gates.decision_readiness
```

`validate_result` compares the supplied dossier with
`action.prepared_dossier`; `_decision_result` attaches it to the Decision.
`decision_readiness` then evaluates required facts and every referenced
predicate. It does not create predicate instances or persist validator
results. The current `apply_result` path cannot append the six missing
predicates.

## Reached counterexamples

The qualified replay reaches PREPARE with the same CHECK/COLLECT selections
and results. A PASS result without its dossier is rejected. A candidate with
the dossier still cannot pass native model validation because the six
referenced predicate IDs are absent. These remain permanent negative cases:

```text
PREPARE result without dossier -> binding unavailable/reject
oracle-valid validations without typed predicates -> admission unavailable
```

Independent fact proofs remain `2/2` and the six external validator results
remain `6/6`; neither is admitted into the native snapshot.

## Required bounded implementation package

Before implementation, define a canonical runtime event/API that atomically
binds the dossier and admits six typed predicate results, with source/content
identity, scope, lineage, provenance, currentness, persistence, replay,
idempotence and invalidation semantics. It must reject missing, stale, wrong
predicate, wrong dossier, wrong producer and failed results. This package is
not executed here.

```text
PREPARED_DOSSIER_CLASSIFICATION = E2_MATERIALIZER_OMISSION
VALIDATION_INSTANCE_CLASSIFICATION = MISSING_NATIVE_RUNTIME_CAPABILITY
IMPLEMENTATION_REQUIRED = YES
IMPLEMENTATION_MODIFIED = NO
PREPARED_DOSSIER = NOT MATERIALIZED
PREPARED_DOSSIER_IDENTITY = 6a507317bc9cc323fbaa626e97b5954cf3ad934b0bd92d9dc96bd4f63e07bddb
FACT_PROOFS = 2/2 (independent oracle)
VALIDATION_EVALUATIONS = 6/6 (independent oracle)
TYPED_VALIDATION_INSTANCES = 0/6
DOSSIER_ADMISSION = NOT REACHED
NEGATIVE_REGRESSIONS = PREPARE-without-dossier preserved; native admission negatives blocked
INVALIDATION = CONTRACT_REQUIRED
REPLAY = PREPARE boundary reproduced; runtime admission not available
DETERMINISM = reached states PASS
POST_DOSSIER_DECISION_READY = []
POST_DOSSIER_ACTIONABLE = []
POST_DOSSIER_SELECTED = NONE
POST_DOSSIER_CONTROL = NOT_REACHED
NEW_RUNTIME_DEFECTS = []
E2_P02_RETRY_ALLOWED = NO
OTHER_P02_BLOCKERS = [RUNTIME_VALIDATION_RESULT_ADMISSION_CONTRACT]
E2_P03_READY = NO
N_REAL_SATISFIED = NO
CANONICAL_E2_QUALIFIED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
```
