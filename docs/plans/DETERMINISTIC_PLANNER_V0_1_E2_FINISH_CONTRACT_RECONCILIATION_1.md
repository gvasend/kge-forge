# E2-FINISH initial-actionability contract reconciliation

## Contradiction

The qualified PC01 source fixture and the canonical experiment agree that
`E2-FINISH` is a post-reentry consumer. The whole-model builder used by the
PC01 qualification, however, constructed `E2-FINISH` with no native
prerequisite gates. The resulting snapshot therefore exposes it as
actionable at the initial state.

| Item | Qualified source/plan | Materialized whole-model state |
|---|---|---|
| ActionId | `E2-FINISH` | `E2-FINISH` |
| Operation | `DETERMINISTIC_VALIDATION` | same |
| Initial status | `ACTION_ELIGIBLE` declaration | `ACTION_ELIGIBLE` |
| Prerequisites | `ACTION_COMPLETED(E2-REENTER)` in PC01 source fixture | empty tuple |
| Prospective output | `E2-K-FINISH`, produced by E2-FINISH | same declaration |
| Required consumer input | accepted reentry output | no native gate enforcing it |
| P01 expectation | six complete O01 definitions and whole-model acceptance | whole-model oracle reports ACCEPT |
| P02 expectation | only E2-COLLECT/E2-CHECK initially actionable; FINISH held | E2-CHECK, E2-COLLECT, E2-FINISH actionable |

No Action or event was executed while producing this analysis.

## Intended lifecycle semantics

The canonical experiment explicitly describes E2-FINISH as the “final
consumer/proof check” whose prerequisite is “accepted reentry output and
independent root/slot proof obligations.” The lifecycle text requires a new
E2-REENTER result before downstream E2-FINISH evaluation. Acceptance cases
A12 and A13 likewise place finishing selection after reentry and its proof
inputs. This is explicit plan/matrix semantics, not an inference from the
runtime label.

The reentry output is the prospective/result contract for `E2-REENTER`:

```text
TYPE       = KnowledgeRecord
IDENTITY   = KnowledgeId(E2-K-REENTER)
PRODUCER   = ActionId(E2-REENTER)
CONSUMER   = E2-FINISH
CREATED    = only after a permitted E2-REENTER result transition
PERSISTED  = as accepted knowledge in the canonical snapshot/ledger
PROVENANCE = E2-REENTER source, E2 scope, E2 lineage, currentness and producer
```

The source-shaped PC01 fixture encodes the enabling relation as
`E2-FINISH REQUIRES ACTION_COMPLETED(E2-REENTER)`. The whole-model oracle's
`extras` construction did not carry that relation into its six Action objects.

## P01 versus P02

P01 verified definition shape, native typing, negative schema cases and a
metadata-level whole-model composition. It did not verify the semantic
actionability sequence required by P02. The absence of the FINISH gate was
therefore not detected by P01's whole-model oracle.

P02's expected initial state is supported directly by the canonical plan and
acceptance matrix. The P02 oracle is consistent with that contract; it is not
the source of the lifecycle rule. Its failure reveals that the P01 materialized
model does not preserve a required definition-time prerequisite.

## As-is selection trace (analysis only)

Native recomputation over the unchanged materialized state gives:

```text
INITIAL:
  actionable = [E2-CHECK, E2-COLLECT, E2-FINISH]
  selected   = E2-CHECK
  control    = RUNNABLE

after hypothetical completion of E2-CHECK (no event applied):
  actionable = [E2-COLLECT, E2-FINISH]
  selected   = E2-FINISH
  control    = RUNNABLE

after hypothetical completion of E2-CHECK and E2-COLLECT (no event applied):
  actionable = [E2-FINISH]
  selected   = E2-FINISH
  control    = RUNNABLE
```

Thus initial non-selection is insufficient. The selector's deterministic
validation-class priority allows E2-FINISH to win before reentry. The model
cannot test the intended lifecycle as-is.

## Classification and minimum correction

`CLASSIFICATION = P01_ACTION_MODEL_DEFECT` (specifically, a whole-model
construction/qualification defect; no Planner runtime defect was shown).

The minimum legitimate correction is:

```text
ACTION_PREREQUISITE_CORRECTION:
preserve the authoritative E2-FINISH prerequisite
ACTION_COMPLETED(E2-REENTER)
in the canonical six-Action model/materializer,
then requalify the model and its derived snapshot.
```

This analysis does not apply that correction. It does not alter the Action,
snapshot, status, Planner implementation or E1.

## Impact and requalification

Affected qualification cases are every case consuming the six-Action whole
model or its derived initial/checkpoint state:

```text
E2-A01, E2-A02, E2-A03, E2-A04, E2-A05, E2-A06,
E2-A07, E2-A08, E2-A09, E2-A10, E2-A11, E2-A12, E2-A13,
E2-A14, E2-A15, E2-A16,
E2-N01..E2-N16,
E2-D01, E2-END, E2-REVIEW
```

The individual six O01 schema/type admissions and source-role identity
checks remain valid as definition evidence. Whole-model admission,
actionability, selection, phase, persistence and all downstream aggregate
qualification claims depending on the incorrect snapshot are invalid until
the prerequisite correction is applied and requalified. No runtime repair is
authorized.

The snapshot identity `2e37f24a…` is **INVALID_IF_CORRECTION_APPLIED**. A
corrected Action graph necessarily produces a different canonical snapshot
identity; the old artifact must not be used as P02 input.

```text
E2_FINISH_INITIAL_STATUS = ACTION_ELIGIBLE (declared), but prematurely actionable
E2_FINISH_PREREQUISITES = ACTION_COMPLETED(E2-REENTER) in source fixture; absent in materialized model
P01_EXPECTATION = definition/whole-model acceptance; semantic sequence not checked
P02_EXPECTATION = E2-FINISH blocked until reentry output
REENTRY_OUTPUT = KnowledgeRecord(E2-K-REENTER), producer E2-REENTER
E2_FINISH_CONSUMES_REENTRY_OUTPUT = YES
CLASSIFICATION = P01_ACTION_MODEL_DEFECT
MINIMUM_CORRECTION = ACTION_PREREQUISITE_CORRECTION
ACTION_MODEL_CHANGE_REQUIRED = YES
ORACLE_CHANGE_REQUIRED = NO
ACCEPTANCE_MATRIX_CHANGE_REQUIRED = NO
E2_P02_RETRY_ALLOWED = NO
E2_P03_READY = NO
N_REAL_SATISFIED = NO
CANONICAL_E2_QUALIFIED = NO
IMPLEMENTATION_MODIFIED = NO
EXPERIMENT_ACTIONS_EXECUTED = 0
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
```
