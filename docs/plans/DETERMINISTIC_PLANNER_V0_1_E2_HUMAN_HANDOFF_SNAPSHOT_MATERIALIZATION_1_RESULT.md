# E2 Human-Handoff Snapshot Materialization

`RESULT = BLOCKED`.

The native initial snapshot was available and decoded successfully. Native
replay reproduced the qualified CHECK/COLLECT prefix exactly, but the
handoff state reconstructed from the available artifacts did not match the
qualified handoff identity recorded by Retry 3. The reconstruction therefore
cannot be accepted or used for human-decision capture.

## Replay and mismatch

```text
INITIAL_SNAPSHOT = 545ad19184d8dd7dfb5b2737e081b043d13982f05d05326939ac2cbb89bf54e2
E2-CHECK_POST_STATE = e381424d14336d918fd3bafff16698361395c77ef03fef628d7d74d36af8a9da
E2-COLLECT_POST_STATE = 6c7efb221870974d76d12d7ceb372369ef68104bb1f522a16d47f7dc37236677
QUALIFIED_HANDOFF_STATE = 39114028d38b9571c46e211248644b09a3ac63ad9f47cd21a75fc922a2d152e3
RECONSTRUCTED_HANDOFF_STATE = 996d1fa73a7c1a880b8cd7a6c27ec48c03386feba4c5a089711482f51aff5069
MISMATCH = HANDOFF_STATE_IDENTITY_MISMATCH
```

The reconstructed state did contain `E2-DECIDE` actionable, the admitted
dossier identity, six validation instances, and `HUMAN_HANDOFF`, but the
identity mismatch proves that at least one canonical state component is not
recoverable from the supplied artifacts. No state was serialized as the
authoritative handoff snapshot.

## Report

```text
WORK_PACKAGE = E2-HUMAN-HANDOFF-SNAPSHOT-MATERIALIZATION
HANDOFF_TRACE_REPLAY = PARTIAL; CHECK/COLLECT PASS, handoff identity mismatch
QUALIFIED_PREFIX = CHECK PASS; COLLECT PASS; PREPARE/DOSSIER semantics reconstructed
DECISION_SUBJECT = E2-DECIDE
OPTIONS = [ALLOW_QUALIFICATION_MAPPING, DECLINE]
DECISION_DOSSIER = 6a507317bc9cc323fbaa626e97b5954cf3ad934b0bd92d9dc96bd4f63e07bddb
FACT_PROOFS = 2/2 (qualified evidence)
VALIDATION_INSTANCES = 6/6 (qualified evidence)
HANDOFF_SNAPSHOT_FORMAT = PLANNER-SNAPSHOT-1 (not emitted as authoritative)
HANDOFF_SNAPSHOT_IDENTITY = NONE
HANDOFF_SNAPSHOT_CONTENT_IDENTITY = NONE
NATIVE_DECODE = PASS (initial snapshot)
SEMANTIC_ROUND_TRIP = NOT_REACHED_FOR_ACCEPTED_HANDOFF
COLD_RESTORE_HANDOFF_ORACLE = NOT_REACHED
DETERMINISM = RECONSTRUCTION DETERMINISTIC, IDENTITY DOES NOT MATCH QUALIFIED TRACE
TAMPER_NEGATIVES = NOT_REACHED
SELECTED_OPTION = NONE
CHOICE_EVIDENCE = ABSENT
RECORDED_DECISION = ABSENT
E2_GRANT = ABSENT
HUMAN_CHOICE_COMPATIBLE_WITH_HANDOFF = NO (exact handoff not accepted)
HUMAN_DECISION_CAPTURE_RETRY_ALLOWED = NO
OTHER_CAPTURE_BLOCKERS = [HANDOFF_STATE_IDENTITY_MISMATCH]
E2_P02_RETRY_ALLOWED = NO
E2_P03_READY = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
```

The ALLOW choice was not captured, and no Planner or E1 state was modified.
