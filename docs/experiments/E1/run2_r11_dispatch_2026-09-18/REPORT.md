# E1 Run-2 r11 terminal report

`CANCELLED / INTERRUPTED_NO_EFFECTS` — independent terminal recovery PASS. Trigger: HARD_BUDGET_STOP (no substantive progress).

r11 completed INACTIVE issuance, independent INACTIVE recovery, activation with exact ownership, independent ACTIVE recovery and dispatcher entry. It did not reach a model request or ActionRequest. E1-WP-001 was not exercised. No implementation, repository or canonical knowledge change, governed test or ExecutionScope occurred. FIRST_REAL_PROGRAMMER_ACTION_REQUEST was not reached. WP1-AC01..09 remain NOT_EXERCISED.

## Budget and timing

The unchanged 300-second no-progress hard threshold fired at 300.000122s during pre-model validation. There were 6 soft warnings and 1 hard exhaustion event. No substantive-progress event occurred. All elapsed pre-handoff work was controller work, not model/provider processing. Token accounting is USAGE_UNKNOWN; no provider request or usage response exists. No token ceiling is claimed.

| Recorded outer controller span | Seconds |
|---|---:|
| validation | 49.388 |
| activation_recovery | 46.891 |
| private_bootstrap | 3.411 |
| activation_recovery | 49.622 |
| host_construction | 57.193 |
| reasoning_construction | 12.975 |
| pre-model validation — interrupted | 51.021 |

Independent ACTIVE recovery took 58.438s including reconstruction outside its inner span. Cancellation-only recovery took 31.519s; independent terminal recovery took 9.951s. PHASE_TIMING.json retains all nested spans; summing nested spans would double-count. TIMELINE.json distinguishes durable timestamps from the terminal result-file persistence time.

## Cancellation anomaly and resolution

Automatic cancellation encountered BudgetExceeded during ActivationTransaction.cancel → lifecycle reconstruction → dispatch verification → instrumented attempt-history decision. The telemetry sink was already closed, so its span admission check blocked cancellation reconstruction. The orchestration wrapper also attempted to construct RunControl on durably closed admission and failed. The initial terminal recovery correctly refused ACTIVE ownership with closed admission. These failures are preserved in ORCHESTRATION_STOP.json, CANCELLATION_UNRESOLVED.json and INDEPENDENT_TERMINAL_RECOVERY_FAILURE.json.

The agent then invoked the unchanged typed cancellation operation in a separate cancellation-only recovery session with the optional telemetry sink unset. It checked exact ACTIVE ownership, closed admission, zero model/provider requests and actions, and absence of scopes/uncertainty; reconstructed the governed host, requested interruption, and called ActivationTransaction.cancel. No effect admission, handoff or model continuation was enabled. Only r11 ownership was released. No runtime implementation or budget was changed. Independent recovery now establishes CANCELLED, no ownership, no reconciliation required and no handoff eligibility.

## Observability and practical outcome

Live projection captured 16 snapshots: {'UNKNOWN': 10, 'FRESH': 6}. Authoritative lifecycle observations were {'UNKNOWN': 10, 'INACTIVE': 4, 'ACTIVE': 2}. UNKNOWN causes: {'EVIDENCE_UNAVAILABLE_OR_INVALID:FileNotFoundError': 3, 'UNSTABLE_SNAPSHOT': 7}. The original observer stopped after failed automatic recovery; a separate fresh terminal projection establishes CANCELLED / RELEASED / QUIESCENT. Live observability was intermittent during authority/audit reconstruction; this limitation is preserved, not represented as uninterrupted healthy status.

The actual issued/owned path exceeded the earlier prepared preflight timings and consumed the complete no-progress allowance before provider entry. Successful warm pre-issuance timing did not guarantee practical end-to-end dispatch startup. The budget stopped the invocation correctly, but automatic cancellation composition and actual-path validation cost require Architect assessment before another attempt. No remediation was implemented during this run.

## Exact durable identities

- Invocation: `auth-e1-wp-001-r11-4dae6644072f42c0b4ffd00be7e80a5d`
- Release: `E1-RELEASE-AUTHORITY-sha256:9783a81890bcc9bd7be61a6c2a9a2d5b84b038ce9d02e44344e45c6e0f95f2e1`
- Context: `E1-OPERATIONAL-CONTEXT-sha256:3901e53c00099d566fbb41151b9fbf3f026fd789403cbeaa742ffd0a0ace8959`
- Activation: `E1-AUTHORIZATION-LIFECYCLE-sha256:773b9ea02aa39c7a0359132df0957150e306eec9a5af8d494b4fedb024b0d1a9`
- Reservation: `INVOCATION-RESERVATION-sha256:b61fb6f68e2acf2f59f7207f1ef7e240301480fc959efce7175030d6f22ed620`
- Cancellation: `E1-AUTHORIZATION-LIFECYCLE-sha256:283c25e43f78362304bccb03e2103696815b8ce0815cd42eaa71dc27f1be27f9`
- Final audit SHA-256: `a18877e1a414fc99c7202ed00f32cdb5ecf9827705130065b526a30129a92712`

EVENT_TRACE.json and ACTION_TRACE.json provide policy-safe event identity/hash traceability to the private audit. No protected model text was retained by the wrapper. BUDGET_HISTORY.json and USAGE.json preserve all available budget/usage evidence.

## Preservation and intervention

422 immutable historical files verified unchanged. The ownership ledger retains its exact original prefix and appends only r11 reservation/release. r8, r9, r10 and Run-1 evidence remain unchanged. The applied r11 authority records remain applied; the invocation is terminal and must not be reused.

No authority-expansion request, tool denial/correction, model interruption, host restart or human engineering decision occurred. The recovery intervention was cancellation-only orchestration after automatic cancellation failed; sandbox execution approvals were used. There is no unresolved invocation uncertainty after independent terminal recovery. No r12 was created and no retry occurred. Experiment 1 PASS and KGE Forge v0.1 acceptance are not established.
