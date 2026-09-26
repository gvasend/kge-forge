# r10 session-composition remediation — BLOCKED

This package stages an unadopted correction and records non-effecting qualification. It does not establish `RUN2_R10_READY_FOR_ARCHITECT_ISSUANCE`. No r10 authorization, activation, ownership or model request was created. Historical r9 and its two soft warnings remain unchanged.

## Root cause and correction

The historical r9 `run.py` calls `controlled_dispatch.dispatch` from inside `with s.session()`. Dispatcher entry itself acquires `store.session()`, so the qualified nested-session guard rejects it before a model request. That guard is correct and unchanged.

Candidate `orchestration_boundary.py` reconstructs the issued authorization and ACTIVE ownership under one session, releases the transaction/controller fence and session in `finally`, then calls the existing dispatcher with only store and exact authorization identity. Dispatcher acquires its own session and independently reconstructs/revalidates authority. No recovered PASS flag grants effects. Failure at the boundary leaves durable state recoverable. The original driver is historical evidence and was not edited.

## Qualification

- Six initial session probes PASS: actual synthetic issuance/activation, valid dispatcher/model handoff, nested-session rejection, boundary interruption/recovery, substituted task rejection, cancellation/status reconciliation, and warning persistence under the transaction lock. The handoff uses a stub transport and non-E1 task, not a real provider request.
- Separate process restart at the session boundary, dispatcher acquisition and synthetic handoff PASS; terminal projection reconstructed in that process.
- Interruptions at private bootstrap, activation recovery, host construction and reasoning construction PASS after typed cancellation/reconciliation. No model call occurs in these negative probes. Unreconciled early failures remain explicit until cancellation; status does not invent release of ownership.
- Prior attempt/lifecycle suite: 22 tests PASS, including issuance-first, competing ownership, restart transition cuts, admission closure and no pre-ACTIVE handoff.
- Existing budget/lifecycle/private-store regression suite: 40/41 PASS in sandbox; the remaining Bubblewrap isolation test failed because sandbox permissions deny NETLINK_ROUTE setup. The exact same test PASS outside sandbox (1 test, 1.420s). No validator weakened.
- Test processes are bounded by 180s external deadlock detectors; restart subprocess is additionally bounded by 90s. No detector fired. These are qualification watchdogs, not changes to released budgets.
- Initial added phase-cancellation fixture incorrectly constructed an INACTIVE host for an ACTIVE cancellation and was rejected. The fixture now reconstructs effective ACTIVE identity through the existing cancellation pattern, or recognizes an already-CANCELLED state. No production acceptance rule changed. Both test logs are retained.

See `session.log`, `prior_attempt.log`, `regressions.log`, `restart-final.log`, `warning-status-final.log`, and `stale-active.log` for exact results. This synthetic coverage is not a claim that an authenticated r10 production context exists.

## Historical r9 timing

| Operation | Evidence-supported allocation |
|---|---|
| Context reconstruction | 17.4054s |
| Activation/validation transaction | 33.8555s total; three projection spans total 13.0408s; 20.8147s not finely segmented |
| Independent ACTIVE recovery | 47.4955s parent span; child reported 47.2334s, without fine-grained child spans |
| Activation warning persistence lag | 0.000119s |
| Recovery warning persistence lag | 17.3861s |

The parent wrapped the recovery subprocess in a timed span. Its alarm tried to append a warning while the child held the audit flock during recovery validation. The same-process descriptor-composition capability does not cross process boundaries. Source ordering plus warning timestamps support lock contention as the cause. There is no evidence of provider wait: r9 sent no model request. Store materialization preceded these phases; status projection was not inside the recovery child.

Projection verification is the largest separately measured repeated activation operation. Cold reconstruction plus validation is a plausible explanation for much of recovery duration, but no exact historical allocation to supervisor checks, reconstruction, fsync or other unspanned work can be recovered. Those allocations remain UNKNOWN, not fabricated measurements. Both soft warnings remain valid; neither phase exceeded 120s.

The new wrapper places the recovery timing sink in the transaction-owning process, eliminating the parent/child warning writer conflict. Warning creation, lock acquisition, append/fsync and persistence completion are now explicitly recorded. The new `warning_persisted` event uses the same borrowed transaction descriptor, without nested lock acquisition. It is telemetry, not lifecycle authority or substantive progress.

Measured warning creation→durability: **0.051628s**, including **0.051600s** append/fsync and **0.000000187s** lock wait. This is a synthetic host observation, not a universal storage-latency guarantee. The implementation does not weaken fsync or audit ordering. Unrelated cross-process writers or a stalled filesystem can still delay persistence; they are not proven bounded by this probe.

## Operator status

Candidate `operator_projection.py` reads and reconstructs lifecycle, action recovery and ownership ledger; it verifies a stable before/after snapshot without taking a mutation lock. Terminal lifecycle plus released ownership and reconciled no-scope state overrides stale provisional INDETERMINATE/ACTIVE telemetry. Old telemetry freshness remains separately visible. Missing, corrupted, changing or deadline-exceeded sources yield UNKNOWN. Stale active activity never becomes a freshly optimistic active subphase.

Projection calls in synthetic restart/cancellation tests complete under 30s. The function checks a 30s deadline and retries at most three unstable snapshots. This is a call-level convergence test, not a deployed periodic-refresh guarantee: no production status service was changed or started. A scheduler/process deadline and authenticated runtime adoption still need production qualification. No historical provisional status file was rewritten.

## Current non-effecting production preflight

The unchanged, released r9 controller reconstructed its private store and current authority. Host-side verification was necessary: sandbox `/proc` did not expose S3. Host systemd remains active/running; readiness recomputed the exact S3 identity and applied succession, with PID 1465900, parent 1465890 and socket inode 4203637.

| Measured phase | Seconds |
|---|---:|
| Cold current-authority bootstrap | 16.8091 |
| Independent terminal recovery | 2.1059 |
| Fresh supervisor readiness | 12.9605 |
| Current model-projection validation | 4.3079 |

All measured phases are below the 30s soft and 120s hard limits. These are current historical-context/readiness checks, **not r10 activation-validation timing**. r10 production activation validation is blocked because no authenticated r10 context exists. No closed admission was reopened.

Current release remains `E1-RELEASE-AUTHORITY-sha256:a8e228850a699e201cd2202b76c6de7de976e7aa34890f3247afda4a599f0708`; current OperationalContextId remains `E1-OPERATIONAL-CONTEXT-sha256:9814f88f64b966a633d0fcc5142a2bfdb1564c8f92f5c07e81455ff1414c58ce`. Exact ancestry, projection identities and S3 evidence are in `PRODUCTION_PREFLIGHT.json`. Payload remains `d675d581c80f43e691a31da73ccf17fd4bcc6b00d3a5331f26b9294e294e1538`.

r9 independently reconstructs CANCELLED, ownership null, handoff false and no reconciliation required. Its immutable accepted classification is INTERRUPTED_NO_EFFECTS. Zero model requests, actions, executions, repository or knowledge effects were produced by r9.

## Proposed r10 and remaining authority blocker

`PROPOSED_R10_BINDING.json` identifies a new unused namespace and binds original Run-2 dispatch, current release/context/S3, exact task/profile/payload/budget/transmission policy, r8 historical evidence, and r9 terminal evidence. It expressly forbids automatic retry and inheritance of state, ownership, counters, effects or audit namespace. It is a proposal, not an operational authorization.

The amendment's general conditions permit consideration of a sufficiently established cancelled, effect-free predecessor. However, the frozen production implementation is narrower:

1. `attempt_context.decision` authenticates the exact accepted r9 proposal and pre-issuance-failure reason.
2. `invocation_attempt.authenticate` binds the predecessor to original r8 dispatch identity/audit.
3. `predecessor_no_effects` accepts only an unissued, closed telemetry-only predecessor ending BLOCKED_BEFORE_AUTHORIZATION_ISSUANCE. A direct read-only probe against genuine cancelled r9 rejects it: “effecting, issued or uncertain predecessor is not replaceable here”. This wording does not mean r9 is actually effecting or uncertain; it denotes the helper's supported predecessor class.
4. Existing allocation and private context selection must not be reused to impersonate r9.

No arbitrary-child rule, changed reason code or substituted proposal hash was introduced. A specifically authenticated r10 selection, a qualified terminal-predecessor proof consumer, and explicit applicability/Architect approval are still required. The proposal deliberately does not claim a complete runtime operational binding under a context that rejects it.

## Applicability

- Session correction: NON_MATERIAL_IMPLEMENTATION_CONTINUATION candidate. Restores the existing single-session ownership contract; nested guard, dispatch revalidation and all effect gates unchanged.
- Warning/status correction: NON_MATERIAL_IMPLEMENTATION_CONTINUATION candidate, subject to complete production qualification. Adds timing and read-only reconciliation; no thresholds, progress definitions, transmission or lifecycle authority changed.
- Production bindings: **no change applied**. Current authority pins the r9 proposal/runtime. A canonical adopted continuation and authenticated r10 binding cannot be claimed from these engineering files. Supporting a terminal r9 predecessor changes the current exact accepted production applicability; whether that is implementation of the general accepted rule or requires a further material amendment must be explicitly resolved and qualified. It is not hidden inside the session fix.

Candidate code and hashes are in `candidate/adapter`, `IMPLEMENTATION.patch`, and `CANDIDATE_IMPLEMENTATION.json`. They are unadopted. Historical repository adapter and frozen r9 runtime remain untouched. No release decision, continuation adoption, replacement dispatch, r10 authorization or allocation was created.

**Verdict: BLOCKED — not RUN2_R10_READY_FOR_ARCHITECT_ISSUANCE.** Remaining gates: authenticated exact r10 production applicability/binding, terminal-predecessor consumer qualification, adopted runtime continuation, and full production status/activation/dispatcher integration against that context. Zero real r10 model requests or effects. No automatic retry.
