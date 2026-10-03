# E2 Authenticated Human Decision Capture — ALLOW

`RESULT = BLOCKED`.

The human explicitly supplied `ALLOW_QUALIFICATION_MAPPING` for
`E2-DECIDE`, but the authoritative inputs provide only the historical
handoff identity and metadata. They do not provide a native serialized
`PLANNER-SNAPSHOT-1` that can be decoded and verified as the current live
state. The capture contract therefore cannot safely bind evidence to the
exact pre-state.

No choice evidence, RecordedDecision, E2-GRANT, or Planner state was created.

## Pinning result

```text
DECISION_SUBJECT = E2-DECIDE
SELECTED_OPTION = ALLOW_QUALIFICATION_MAPPING
EXPECTED_HANDOFF_STATE_IDENTITY = 545ad19184d8dd7dfb5b2737e081b043d13982f05d05326939ac2cbb89bf54e2
DECISION_DOSSIER_IDENTITY = 6a507317bc9cc323fbaa626e97b5954cf3ad934b0bd92d9dc96bd4f63e07bddb
LIVE_NATIVE_SNAPSHOT = NOT_AVAILABLE
LIVE_HANDOFF_VERIFICATION = NOT_REACHED
BLOCKER = LIVE_HANDOFF_NATIVE_SNAPSHOT_UNAVAILABLE
```

The T03 path remains qualified. Its pinned protocol trust root is
`raw-file-sha256:d7478df57c6c7619eff262daa6e258103cd31e226db6e523e5d2de6a5a603da0`
and its qualification issuer identity is
`qualification-authority:ed59567bbe5e7c719975a4e64db157696bf349d42cb0e73695115a50606c330a`.
Those values were not used to fabricate a decision against an unverified
state.

## Report

```text
CHOICE_AUTHENTICATION = NOT_REACHED
CHOICE_EVIDENCE_IDENTITY = NONE
RECORDED_DECISION = NOT_CREATED
RECORDED_DECISION_IDENTITY = NONE
DECISION_ADMISSION = NOT_REACHED
E2_GRANT = NOT_CREATED
E2_GRANT_IDENTITY = NONE
E2_GRANT_APPLICABILITY = NOT_REACHED
APPLY_RECORDED_DECISION = NOT_REACHED
ATOMICITY = PRESERVED_BY_NO_COMMIT
IDEMPOTENCE = NOT_REACHED
PERSISTENCE = NOT_REACHED
COLD_RESTORE = NOT_REACHED
POST_DECISION_ACTIONABLE = NONE
POST_DECISION_SELECTED = NONE
POST_DECISION_CONTROL = NONE
E2_P02_RETRY_ALLOWED = NO
OTHER_P02_BLOCKERS = [LIVE_HANDOFF_NATIVE_SNAPSHOT_UNAVAILABLE]
E2_P03_READY = NO
N_REAL_SATISFIED = NO
CANONICAL_E2_QUALIFIED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
```

The next safe step is to provide or materialize the exact native handoff
snapshot, then rerun verification and capture against that pinned state.
