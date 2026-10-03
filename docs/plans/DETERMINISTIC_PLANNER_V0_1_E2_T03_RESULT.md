# E2-T03 Human Decision Capture + Authority Materialization

`RESULT = PASS` for the bounded runtime capability qualification. The
implementation accepts only an explicit option identifier and does not select
an option during T03.

## Implemented boundary

`adapter/planner/human_decision.py` authenticates a future choice against the
E2 subject, admitted DecisionDossier, pinned snapshot, qualification issuer
identity (`qualification-authority:ed59567bbe5e7c719975a4e64db157696bf349d42cb0e73695115a50606c330a`), independent trust-root identity, scope, lineage and sequence. It
constructs the native choice-record entity and accepted
`decision-choice:E2-DECIDE` knowledge, then invokes the unchanged
`apply_recorded_decision` path. Identical resubmission is idempotent and a
conflicting second choice fails closed.

The ALLOW synthetic path materializes exactly `E2-GRANT` with `USE` for
`E2-REENTER`, scope `E2-QUALIFICATION-ONLY`, lineage
`E2-CANONICAL-BASELINE-1`, and no production authority. The DECLINE path
records an authenticated choice and creates no grant. `ControlState` includes
the qualification-only `QUALIFICATION_DECLINED` value for a declined branch;
the live E2 state was not changed.

## Qualification results

| Area | Result |
|---|---|
| Human choice capture | PASS; exact option IDs only |
| Choice authentication | PASS; issuer/trust/dossier/scope/lineage binding |
| RecordedDecision materializer | PASS |
| E2-GRANT materializer | PASS in test-only ALLOW fixture; narrowly scoped |
| `apply_recorded_decision` integration | PASS; native admission unchanged |
| ALLOW synthetic path | PASS |
| DECLINE synthetic path | PASS; no grant |
| Atomicity | PASS; immutable preparation and native admission commit, no partial live mutation |
| Idempotence | PASS |
| Persistence/round-trip | PASS; native `PLANNER-SNAPSHOT-1` encode/decode preserves record/grant once |
| Negative controls | PASS |
| Determinism | PASS; repeated construction has identical evidence/snapshot identities |
| Live handoff preflight | PASS; future choice can be submitted without preselecting one |

The implementation does not create a choice, issue authority, or call the
live E2 Planner. `E2_P02_HUMAN_CHOICE_READY = YES` means the runtime path is
available; `E2_P02_RETRY_ALLOWED = NO` until an actual authenticated choice is
supplied and admitted.

## Report

```text
WORK_PACKAGE = E2-T03
RESULT = PASS
HUMAN_CHOICE_CAPTURE = PASS
CHOICE_AUTHENTICATION = PASS
RECORDED_DECISION_MATERIALIZER = PASS
E2_GRANT_MATERIALIZER = PASS (synthetic ALLOW fixture only)
APPLY_RECORDED_DECISION_INTEGRATION = PASS
ALLOW_TEST_PATH = PASS
DECLINE_TEST_PATH = PASS
ATOMICITY = PASS
IDEMPOTENCE = PASS
PERSISTENCE = PASS
REPLAY = PASS (native snapshot round-trip; no live choice replayed)
NEGATIVE_CONTROLS = PASS
DETERMINISM = PASS
LIVE_HANDOFF_PREFLIGHT = PASS
HUMAN_DECISION_READY = YES
E2_P02_HUMAN_CHOICE_READY = YES
SELECTED_OPTION = NONE
AUTHORITY_ISSUED = NO
DECISION_RECORDED = NO
E2_P02_RETRY_ALLOWED = NO
E2_P03_READY = NO
N_REAL_SATISFIED = NO
CANONICAL_E2_QUALIFIED = NO
IMPLEMENTATION_MODIFIED = YES (bounded T03 capability only)
LIVE_E2_DECISION_MODIFIED = NO
EXPERIMENT_ACTIONS_EXECUTED = 0
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
```
