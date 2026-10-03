# E2-FINISH prerequisite materialization repair 1

## Result

`REPAIR = E2_FINISH_PREREQUISITE_MATERIALIZATION_1`
`RESULT = PASS`.

The PC01 whole-model materializer now preserves the typed prerequisite tuple
from each authoritative source Action. This is a generic transformation; it
contains no ActionId-specific branch. The source fixture and Planner runtime
were not changed.

## Before and after

The pre-repair counterexample was reproduced: the source declared
`ACTION_COMPLETED(E2-REENTER)`, while the materialized `E2-FINISH` had an
empty prerequisite tuple and was actionable initially.

The repaired source/native comparison is exact for all six Actions:

```text
E2-COLLECT  []
E2-CHECK    []
E2-PREPARE  [ACTION_COMPLETED(E2-CHECK), ACTION_COMPLETED(E2-COLLECT)]
E2-DECIDE   [ACTION_COMPLETED(E2-PREPARE)]
E2-REENTER  [ACTION_COMPLETED(E2-DECIDE)]
E2-FINISH   [ACTION_COMPLETED(E2-REENTER)]
```

Initial recomputation now gives:

```text
ACTIONABLE = [E2-CHECK, E2-COLLECT]
SELECTED = E2-CHECK
CONTROL = RUNNABLE
E2-FINISH = NON_ACTIONABLE
```

A pure hypothetical state with `E2-REENTER` completed makes E2-FINISH
actionable through ordinary native actionability, proving the gate is
conditional rather than permanent. No lifecycle event was applied.

## Requalification

All six O01 definitions remain admitted. The corrected whole-model oracle,
source-role checks, policy binding, composition negatives and PC01/PC02/PC03
independent oracles pass. Deterministic whole-model construction passes for
hash seeds 0, 1, 7 and 101; the corrected snapshot identity is stable.

The old snapshot `2e37f24a…` is preserved as counterexample evidence and is
`INVALIDATED_BY_ACTION_MODEL_CORRECTION` for P02. The new native snapshot is
`71fe19caaeb0f7c10da8db2bbb5d849156c59cc521e3e11e4fffb8d578080db9`.
Native serialization, decode and semantic round-trip pass.

The affected P01/PC qualification slice is requalified. Individual O01 and
source-role evidence remains valid; whole-model/actionability/selection and
downstream snapshot-dependent claims now use the corrected identity. No P02
transition is executed here.

```text
PRE_REPAIR_COUNTEREXAMPLE = REPRODUCED
ROOT_CAUSE = generic prerequisite tuple omitted by whole-model materializer
GENERIC_REPAIR = YES
E2_FINISH_PREREQUISITES = [ACTION_COMPLETED(E2-REENTER)]
ALL_ACTION_PREREQUISITES_PRESERVED = YES
INITIAL_E2_FINISH_ACTIONABLE = NO
POST_REENTER_COMPLETE_E2_FINISH_ACTIONABLE = YES
O01_ACTIONS = 6/6
WHOLE_MODEL_ADMISSION = PASS
P01_REQUALIFICATION = PASS (affected dependency cone)
OLD_SNAPSHOT_IDENTITY = 2e37f24a...
OLD_SNAPSHOT_STATUS = INVALIDATED_BY_ACTION_MODEL_CORRECTION
NEW_SNAPSHOT_IDENTITY = 71fe19caaeb0f7c10da8db2bbb5d849156c59cc521e3e11e4fffb8d578080db9
NATIVE_SERIALIZATION = PASS
NATIVE_DECODE = PASS
SEMANTIC_ROUND_TRIP = PASS
INITIAL_STATE_ORACLE = PASS
DETERMINISM = PASS
BASELINE_REGRESSIONS = PASS (affected prerequisite/actionability checks)
P02_INPUT_READY = YES
E2_P02_RETRY_ALLOWED = YES
E2_P03_READY = NO
N_REAL_SATISFIED = NO
CANONICAL_E2_QUALIFIED = NO
PLANNER_V0_1_REQUALIFICATION_READY = NO
IMPLEMENTATION_MODIFIED = NO
EXPERIMENT_ACTIONS_EXECUTED = 0
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
```
