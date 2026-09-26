# Run-2 bound control-plane qualification

`RUN2_CONTROL_PLANE_READY_FOR_NEXT_ATTEMPT`

The exact candidate runtime completed the production pre-model path using original Run-2 private authority objects, complete r8–r12 history, released profile/payload and genuine current S3. Production validators and recovery functions were not mocked. Five finite, explicitly qualification-only invocation bindings used isolated private lifecycle/ownership namespaces. All stopped before provider handoff. No r13 or real invocation was created.

The qualification continuation was bound and exercised. The separate ordinary production continuation is prepared, **not applied**. Real release authority and real historical operational head remain unchanged. Readiness here qualifies the implementation and next-attempt preparation; it does not authorize an invocation or select a replacement attempt.

| Phase (seconds) | Cold | Warm 1 | Warm 2 | Warm 3 |
|---|---:|---:|---:|---:|
| private_bootstrap | 3.546 | 3.576 | 3.798 | 3.793 |
| preflight | 3.822 | 3.823 | 3.858 | 4.127 |
| INACTIVE_issuance | 5.135 | 4.947 | 4.830 | 4.889 |
| INACTIVE_recovery | 0.065 | 0.045 | 0.053 | 0.045 |
| activation | 16.274 | 16.415 | 16.534 | 16.418 |
| independent_ACTIVE_recovery | 15.301 | 15.049 | 15.142 | 15.037 |
| dispatcher activation_recovery | 7.485 | 7.463 | 7.477 | 7.482 |
| dispatcher host_construction | 12.839 | 12.766 | 12.944 | 13.031 |
| dispatcher reasoning_construction | 8.105 | 7.880 | 7.988 | 8.139 |
| Model-cycle preparation (overlaps nested validation) | 13.287 | 13.232 | 13.547 | 13.482 |
| Cumulative preparation to MODEL_REQUEST_READY | 104.758 | 103.806 | 104.764 | 105.026 |

Every normal individual phase was below 30 seconds (maximum 16.535s); all four samples had zero soft warnings. Cumulative preparation was below two minutes, retaining at least 194.974s against the unchanged 300s no-progress limit. Model-cycle preparation includes its nested validations and must not be added twice. Detailed ordered spans, dispatcher bootstrap and controller glue accounting are in PRODUCTION_MEASUREMENTS.json; no unallocated multi-minute interval remains.

The largest repeated cost was reconstruction of immutable supervisor authority and historical captures at adjacent gates, compounded by repeated catalog parsing and audit-prefix hashing. The dependency graph and producer/consumer contracts are in CROSS_PHASE_REUSE.md. Reuse is limited to verified pure results and exact bytes within bounded scopes. Original historical evidence is rechecked at the scope boundary; changed/missing dependencies fail closed. Catalog placement and content, implementation/schema, source identities and authoritative bindings constrain reuse. No authoritative checkpoint or caller-supplied PASS is introduced. Lifecycle, ownership, ExecutionScope, admission, uncertainty, authority/attempt heads and live supervisor identity/readiness remain freshly verified. The common supervisor verifier serves ordinary attempt validation and qualification bindings.

Cancellation qualification deliberately waited with the real monotonic clock at MODEL_REQUEST_READY. No-progress exhaustion occurred at 300.181s. The ordinary automatic path closed admission, cancelled, released ownership, established QUIESCENT and independently reconstructed terminal CANCELLED without reopening admission or a separate cancellation-only recovery. Independent terminal recovery took 5.859s. This stress case included read-only scheduling probes after committed transitions; its 43.320s activation phase correctly generated a soft warning, and remained below the 120s hard threshold. It is not a normal timing sample. Three stress warnings covered phase, no-progress and cycle limits. All budgets and substantive-progress semantics remained unchanged; all five cases contained zero substantive-progress events.

Live projection produced 84/84 FRESH periodic lifecycle samples and four additional FRESH committed-transition observations. Coverage included pre-issuance, INACTIVE, activation intent, ownership reservation, ACTIVE/recovery, dispatcher preparation, warning, exhaustion, cancellation and terminal recovery. At reservation-before-ACTIVE it accurately reported ACTIVATING / HELD_FOR_RECONCILIATION. Terminal state was CANCELLED / RELEASED / QUIESCENT. Conservative terminal-convergence upper bounds were below 10.82s; these bounds use surrounding durable events because lifecycle records do not supply an exact transition timestamp. Stale activity/supervisor observations are explicitly marked stale/UNKNOWN rather than treated as fresh readiness. They do not erase independently reconstructed lifecycle authority.

Earlier UNKNOWN results came from status snapshot rejection of legitimate observation suffixes, including nonzero-cycle verification and legacy context-projection evidence. The corrected UI checks exact schema/identity and audit prefix; unknown, effecting or lifecycle-changing suffixes still force reconstruction. This UI interpretation does not extend safe-predecessor policy or confer authority.

Qualification: eight reuse/tamper tests, twelve cancellation/session/status regressions, thirty bound budget/store/isolation regressions and ten bound negative/readiness probes passed. Genuine original-runtime supervisor reconstruction independently reproduced the immutable verification result. Final S3 identity/readiness recheck passed. Historical preservation verified 227 files, including unchanged real ownership ledger and r12 evidence.

r12 remains CANCELLED / INTERRUPTED_NO_EFFECTS, classified ACTIVE_CANCELLED_PRE_MODEL_NO_EFFECTS under the applied policy: terminal, admission closed, ownership released, no ExecutionScope, QUIESCENT, zero model/provider requests and effects, no unresolved uncertainty. Its safe-predecessor verdict is PASS. This creates no successor authority.

The changes are assessed separately as non-material implementation corrections: catalog/history composition and exact verification reuse; cancellation observer isolation restoring existing reconciliation; and read-only status reconciliation. Authority, lifecycle outcomes, budgets, progress, transmission and retention permissions remain unchanged. New observational timings do not grant authority or silently extend predecessor eligibility. Finite qualification bindings select isolated synthetic namespaces only. No real release amendment was applied. See APPLICABILITY_ASSESSMENT.json for per-dimension classification.

Exact publication identities:

- Qualified runtime: `sha256:1b31ac92d38952444076e3997083cf035e0862f1bc0182261826d6690ec31c15`
- Bound qualification continuation: `CONTINUATION-sha256:08d2096b6f642c0ed056ca537263c46b787be39cbe82bae45b675a04ee98649e`
- Prepared ordinary production continuation (unapplied): `CONTINUATION-sha256:b9476d2017ea8528a6d22759c0c692481fd4234d7e360a744c160e013ca69cea`
- Prepared continuation file SHA-256: `3516703b7da670e89bef39e2aad40c1774345c3e28edccbe095927bfa4ddf57c`
- Proposed ordinary context (not current): `E1-OPERATIONAL-CONTEXT-sha256:47adf514b62b8c3930405e3cf5d660142dcbe2f29968316df992f29f03d09453`
- Proposed chain digest: `3e1912b964491781adb494f6dd604a80e7cbc29587d59b4862682c640741c73b`
- Unchanged real release authority: `E1-RELEASE-AUTHORITY-sha256:84b7294bef3e2ccdbae8364b66f202135fcc9def9dd0081b473f847b4636628d`
- Unchanged real OperationalContextId: `E1-OPERATIONAL-CONTEXT-sha256:a59e21566098fee1756bbe991f74e0d2c8c5b756a76d90877911c35d57044a8a`
- Unchanged real chain: `ddf509e2283fe93aa9bb9b857a45dc449ff5ca309c66f9bdfd18c45dcf2dedfd`
- ModelPayloadDigest unchanged: `d675d581c80f43e691a31da73ccf17fd4bcc6b00d3a5331f26b9294e294e1538`.
- Profile SHA-256 unchanged: `fb842649d30e5876fb3f299e890e2c555a88be759c29b2c6577552d4885b0226`.
- S3: `SupervisorInstance-sha256:83f22718a56ab733257208c6e1dfe9767a95e0d10b82f8583f222f88ee9669a2`.

QUALIFIED_PUBLICATION.json records every exercised synthetic OperationalContextId, ancestry, FullContextDigest, ModelProjectionBindingDigest and private-store catalog identity. These distinct qualification contexts are not represented as the current real context.

Zero new real model/provider requests, E1 ActionRequests, executions, repository/knowledge/implementation effects or real ownership reservations occurred. Authorized staged controller changes and synthetic lifecycle evidence are the qualification work itself. No r13 was constructed or issued. Historical attempts remain immutable. No Experiment 1 acceptance judgment is made.
