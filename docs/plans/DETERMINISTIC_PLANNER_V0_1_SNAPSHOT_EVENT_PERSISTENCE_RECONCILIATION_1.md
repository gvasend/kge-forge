# Snapshot / Event-Bearing Persistence Reconciliation 1

The native `Snapshot` and `PersistenceBundle` are distinct models. A Snapshot serializes validated canonical state with `planner-snapshot-v1` identity, but carries no event ledger, append head, parent event, or causal ancestry. A PersistenceBundle serializes an initial Snapshot plus an ordered `ExecutionEvent` ledger and source/policy pins; its `planner-bundle-v1` identity and replay validation bind each event to the prior state and parent event.

The native architecture supports bundle → restored Snapshot through replay. It does not define a supported Snapshot → trusted PersistenceBundle conversion or event-genesis operation. T01 requires a bundle because append ordering, causal ancestry, pre-state binding, idempotence, replay, provenance, and fork/conflict detection cannot be established from a snapshot hash.

E2 persistence history is snapshot-only for P01, P02, T02, HUMAN_HANDOFF reproduction, T03, T04, and P03 gate qualification. Event ancestry was never established; there is no first package where an existing ledger was dropped. The prior `c1d87905...` remains a pre-native fixture identifier.

Consequently T01 and E2 are currently `INCOMPLETE`, not semantically contradictory. Retrospective event creation from the qualified snapshots is prohibited because it would launder state into false historical execution. A legitimate forward path would require an explicit, trusted event-genesis contract authorizing a new ledger at a current canonical state, or re-execution of the qualified prefix using event persistence from the start. That genesis capability must bind the exact snapshot, scope, lineage, provenance, trust root, and a genesis event without claiming prior events occurred.

The minimum next package is **EVENT_GENESIS_CONTRACT**. It must decide whether a new event-bearing lineage may begin at the current P02/T04 state and define its authority/security boundary. Until then T01-B remains blocked.

```
SNAPSHOT_TO_BUNDLE_SUPPORTED = NO
BUNDLE_TO_SNAPSHOT_SUPPORTED = YES
T01_EVENT_ANCESTRY_REQUIREMENT = append ordering + causal parent + pre-state binding + idempotence + replay + fork/conflict detection + provenance
FIRST_ANCESTRY_LOSS = EVENT_ANCESTRY_NEVER_ESTABLISHED
EVENT_ANCESTRY_NEVER_ESTABLISHED = YES
T01_E2_COMPATIBILITY = INCOMPLETE
RETROSPECTIVE_ANCESTRY_ALLOWED = NO
FORWARD_EVENT_GENESIS_SUPPORTED = NO
GENESIS_AUTHORITY_REQUIRED = YES
MINIMUM_REEXECUTION_POINT = REEXECUTE_E2_PREFIX_WITH_EVENT_PERSISTENCE
RUNTIME_CAPABILITY_CLASSIFICATION = NEW_RUNTIME_CAPABILITY_REQUIRED
CLASSIFICATION = COMBINED
T01_B_RESULT = BLOCKED
T01_ADMISSION_BUNDLE_RETRY_ALLOWED = NO
E2_P03_RETRY_ALLOWED = NO
E2_P04_READY = NO
EXTERNAL_EVIDENCE_ADMITTED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
```

Semantic qualification remains preserved; only persistence/ancestry claims are invalidated. No event, bundle, evidence, receipt, Action, or E1 artifact was created.
