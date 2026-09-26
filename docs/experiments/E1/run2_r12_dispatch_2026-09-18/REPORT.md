# E1 Run-2 r12 terminal report

`CANCELLED / INTERRUPTED_NO_EFFECTS` — independent terminal recovery PASS. Trigger: HARD_BUDGET_STOP (no substantive progress).

r12 completed INACTIVE issuance, independent INACTIVE recovery, activation with exact ownership, independent ACTIVE recovery and dispatcher entry. It did not reach a model request or ActionRequest. E1-WP-001 was not exercised. No implementation, repository or canonical knowledge change, governed test or ExecutionScope occurred. FIRST_REAL_PROGRAMMER_ACTION_REQUEST was not reached. WP1-AC01..09 remain NOT_EXERCISED.

## Budget and timing

The unchanged 300-second no-progress hard threshold fired at 300.051753s during pre-model validation. There were 5 soft warnings and 1 hard exhaustion event. No substantive-progress event occurred. All elapsed pre-handoff work was controller work, not model/provider processing. Token accounting is USAGE_UNKNOWN; no provider request or usage response exists. No token ceiling is claimed.

| Closed outer timing span | Seconds |
|---|---:|
| validation | 58.319 |
| activation_recovery | 53.678 |
| private_bootstrap | 4.138 |
| activation_recovery | 56.707 |
| host_construction | 65.667 |
| reasoning_construction | 15.136 |
| validation | 7.774 |

Independent ACTIVE recovery took 69.358s including reconstruction outside its inner span. Cancellation-only recovery took 39.616s; independent terminal recovery took 12.746s. The final 7.774-second validation span ended by budget interruption, not successful validation. Pre-issuance production preflight took 26.556s. PHASE_TIMING.json retains all nested spans; summing nested spans would double-count. TIMELINE.json distinguishes durable timestamps from the terminal result-file persistence time.

## Cancellation anomaly and resolution

Automatic cancellation encountered BudgetExceeded during ActivationTransaction.cancel → lifecycle reconstruction → dispatch verification → instrumented attempt-history decision. The telemetry sink was already closed, so its span admission check blocked cancellation reconstruction. The orchestration wrapper also attempted to construct RunControl on durably closed admission and failed. The initial terminal recovery correctly refused ACTIVE ownership with closed admission. These failures are preserved in ORCHESTRATION_STOP.json, CANCELLATION_UNRESOLVED.json and INDEPENDENT_TERMINAL_RECOVERY_FAILURE.json.

The agent then invoked the unchanged typed cancellation operation in a separate cancellation-only recovery session with the optional telemetry sink unset. It checked exact ACTIVE ownership, closed admission, zero model/provider requests and actions, and absence of scopes/uncertainty; reconstructed the governed host, requested interruption, and called ActivationTransaction.cancel. No effect admission, handoff or model continuation was enabled. Only r12 ownership was released. No runtime implementation or budget was changed. Independent recovery now establishes CANCELLED, no ownership, no reconciliation required and no handoff eligibility.

## Observability and practical outcome

Live projection captured 16 snapshots: {'UNKNOWN': 9, 'FRESH': 7}. Authoritative lifecycle observations were {'UNKNOWN': 9, 'INACTIVE': 5, 'ACTIVE': 2}. UNKNOWN causes: {'EVIDENCE_UNAVAILABLE_OR_INVALID:FileNotFoundError': 3, 'UNSTABLE_SNAPSHOT': 4, 'PROJECTION_DEADLINE': 2}. The original observer stopped after failed automatic recovery; a separate fresh terminal projection establishes CANCELLED / RELEASED / QUIESCENT. Live observability was intermittent during authority/audit reconstruction; this limitation is preserved, not represented as uninterrupted healthy status.

The actual issued/owned path exceeded the earlier prepared preflight timings and consumed the complete no-progress allowance before provider entry. Successful warm pre-issuance timing did not guarantee practical end-to-end dispatch startup. The budget stopped the invocation correctly, but automatic cancellation composition and actual-path validation cost require Architect assessment before another attempt. No remediation was implemented during this run.

## Exact durable identities

- Invocation: `auth-e1-wp-001-r12-86af4f6e7bb64eb384108dec11692c86`
- Release: `E1-RELEASE-AUTHORITY-sha256:84b7294bef3e2ccdbae8364b66f202135fcc9def9dd0081b473f847b4636628d`
- Context: `E1-OPERATIONAL-CONTEXT-sha256:a59e21566098fee1756bbe991f74e0d2c8c5b756a76d90877911c35d57044a8a`
- Activation: `E1-AUTHORIZATION-LIFECYCLE-sha256:52b847cc26722a7fe71eac698ae257920e370bc64a66c51f00d96704175098ab`
- Reservation: `INVOCATION-RESERVATION-sha256:49cd515b0ce10f73c47c1bc86346e4f35037280292a6302fda9e15ec30b10aba`
- Cancellation: `E1-AUTHORIZATION-LIFECYCLE-sha256:af752e81a15df18f5f5528bbd38988bfa07a2a9e10d36312df13fd6f6ba7ac11`
- Final audit SHA-256: `d1d2b4a202843b16ced71fec21fa7a55e459e8f2bd6f57c743a3cf64d1dd853f`

EVENT_TRACE.json and ACTION_TRACE.json provide policy-safe event identity/hash traceability to the private audit. No protected model text was retained by the wrapper. BUDGET_HISTORY.json and USAGE.json preserve all available budget/usage evidence.

## Preservation and intervention

156 immutable historical files verified unchanged. The ownership ledger retains its exact original prefix and appends only r12 reservation/release. r8, r9, r10, r11 and Run-1 evidence remain unchanged. The applied r12 authority records remain applied; the invocation is terminal and must not be reused.

No authority-expansion request, tool denial/correction, model interruption, host restart or human engineering decision occurred. The recovery intervention was cancellation-only orchestration after automatic cancellation failed; sandbox execution approvals were used. There is no unresolved invocation uncertainty after independent terminal recovery. No r13 was created and no retry occurred. Experiment 1 PASS and KGE Forge v0.1 acceptance are not established.
