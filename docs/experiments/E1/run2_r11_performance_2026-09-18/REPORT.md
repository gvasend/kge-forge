# r11 validation performance closure

RUN2_R11_READY_FOR_ARCHITECT_ISSUANCE

Functional qualification PASS. Three final warm production samples and sealed-store validation are below the unchanged 30-second soft threshold. No required production phase exceeded 120 seconds. No issuance, activation, reservation, model request or dispatch occurred.

## Root cause and correction

The profiled baseline spent 25.026 seconds in 1,260 catalog checks, including 18.458 seconds in repeated private-placement predicates. Repeated historical-store construction reparsed and froze the same pinned catalogs. The three model projections repeated that work. Profiling overhead is excluded from acceptance samples.

The staged correction shares canonical grant resolution and component comparisons within each fresh placement predicate. It reuses parsed pinned historical catalogs only for one production validation operation. Each borrow rechecks the catalog hash, applicability and placement; every historical witness object, audit, runtime inventory and mutable context input is still read and hashed. Current ownership, scopes, lifecycle, namespace, selected ancestry and genuine supervisor readiness remain fresh. Exceptions close every borrowed store; nested authority sessions still fail closed.

No new authoritative checkpoint or stored PASS is introduced. The existing authenticated historical capture remains unchanged: `sha256:12dd7834ae675d8eb704d930ab09732629b082d858189420f107270eef2a1873`. This is deliberately conservative reuse of parsed immutable structure, not constant-time authorization from a summary.

## Qualification

86 test methods passed: 16 performance/freshness probes, 24 integrated non-E1 lifecycle/session/status/budget tests, 8 actual historical-identity tests, 6 specific-grant tests and 32 host regressions. The actual-context suite also rejected 19 substituted/missing authority cases. The outer sandbox initially prevented the bubblewrap namespace test; all 32 regressions subsequently passed on the host.

Tamper, missing data, reordered/substituted predecessors, disposition/effect/ownership changes, wrong dispatch/context bindings, unknown head, stale catalog/applicability, changed grants/private paths and permissions fail closed. Fresh ownership/scope changes are observed between repeated calls. New-process reconstruction reproduces the exact sealed prepared context from pinned private objects and original evidence. See HISTORY_QUALIFICATION_MATRIX.json for all 16 requested history requirements; no new sufficient checkpoint is being qualified.

## Production timing

| Operation | Seconds |
|---|---:|
| Cold private bootstrap (sealed) | 2.538 |
| Cold production validation | 24.705 |
| Warm production validation 1 | 24.657 |
| Warm production validation 2 | 24.432 |
| Warm production validation 3 | 24.714 |
| Sealed-store validation | 24.216 |
| Independent cold reconstruction | 20.182 |

The sealed validation allocates 12.582s to the unchanged fresh supervisor peer and 8.378s to three complete model projections. The remaining 3.256s covers other controller predicates, store/context/dispatch/history checks and observation bookkeeping. Nested history spans must not be added again to enclosing projection spans. FINAL_PROFILE_SUMMARY.json accounts for native catalog hashing and resolver work; PRE_ISSUANCE_DIAGNOSTICS.json preserves correlated wall/monotonic spans. No interval is attributed to a model/provider.

## Complexity

The representative synthetic hash-linked history kernel uses the real private store and eight validation passes per operation. It is not a substitute for the production timings above.

| Attempts | Complete catalog reconstruction median | Operation-scoped reuse median |
|---:|---:|---:|
| 1 | 0.0104s | 0.0090s |
| 4 | 0.0209s | 0.0191s |
| 16 | 0.0658s | 0.0618s |
| 64 | 0.2898s | 0.2778s |
| 128 | 0.6983s | 0.6113s |

Complete historical-byte verification remains approximately linear over the measured range. Catalog parsing is once per distinct store per operation, rather than once per recursive use. No constant-time guarantee is claimed. This closes the current production threshold without changing what historical evidence is sufficient; very large ancestry will still require measurement.

## Applicability and exact candidate

Performance-only changes are a NON_MATERIAL_IMPLEMENTATION_CONTINUATION candidate: equivalent fresh placement checks, parsed pinned-catalog reuse and non-authorizing spans. The already-proposed material attempt-chain policy/capture representation is kept separate and remains unadopted. Performance artifacts are compared with the accepted functional candidate; they are not mislabeled as a non-material introduction of the entire new attempt policy.

Candidate: `auth-e1-wp-001-r11-4dae6644072f42c0b4ffd00be7e80a5d`. Binding SHA-256: `50cd9be1a0f068ae05506380e3b8847820438098e48d345e5c70e56225694887`. Both remain unchanged. Its binding pins the applied predecessor and unchanged task/profile/payload/budget/dispatch/supervisor invariants. The complete new prepared runtime, effective amendment/continuation and context identities are recomputed below; accepting the old proposal does not by itself authorize these records.

| Prepared record (not applied) | Exact identity |
|---|---|
| Implementation | `sha256:0463e73a610e0402d836daa6d2656c26cf1fd5099a137550251883c82087b65f` |
| Material amendment | `E1-RUN2-ATTEMPT-CHAIN-AMENDMENT-sha256:cff07f9975d27df4c9102be4e927e0ec4d1d7802cf070a53a9eb33469a618090` |
| Amendment file SHA-256 | `e992399bfc6a3e398fd3b06e98e7b3e8c6fd083c90e4bd8ea3a524167bb5ce03` |
| Implementation continuation | `CONTINUATION-sha256:cc0fb1818f524d999fc4efbd76b735b53aedd7f7f19aed74464b35470d9430bd` |
| Continuation file SHA-256 | `1e1382b569effdcd5b1aad401adf9eb695dca26c8914211ad890f43f94269286` |
| Resulting release authority | `E1-RELEASE-AUTHORITY-sha256:9783a81890bcc9bd7be61a6c2a9a2d5b84b038ce9d02e44344e45c6e0f95f2e1` |
| OperationalContextId | `E1-OPERATIONAL-CONTEXT-sha256:3901e53c00099d566fbb41151b9fbf3f026fd789403cbeaa742ffd0a0ace8959` |
| ReleaseBasisId | `E1-RELEASE-BASIS-sha256:bc176574817f6b7fe06fdcf87a71c57b2a8bfe74e55ed20f2aa55ad5d4fa5181` |
| ReleaseDecisionId | `E1-RELEASE-DECISION-sha256:43ab22254604a29f3cf2164152803ee5f689f7540e2006c43d27ded87d83d8c0` |
| continuation_chain_digest | `9f347f5885448701d47de5e682b18721affd48c8443c404661c522dda365f5da` |
| AuthoritativeContextId | `E1-AUTHORITATIVE-CONTEXT-sha256:af0ccbb2f4ac3de66087f3e96910a95d1ec9e0420b7f26b6e57882e7a152088f` |
| FullContextDigest | `af0ccbb2f4ac3de66087f3e96910a95d1ec9e0420b7f26b6e57882e7a152088f` |
| ModelPayloadDigest | `d675d581c80f43e691a31da73ccf17fd4bcc6b00d3a5331f26b9294e294e1538` |
| ModelProjectionBindingDigest | `3ef70b31331472e57a546845d122fd28bef8c8f7ebb71e7dfb59f4740fdc0a02` |
| ModelProjectionDigest | `2603a89f241081052a10775fb2b9c17779dd22b75e725c1451c39eec230b9ca6` |

The currently applied release remains `E1-RELEASE-AUTHORITY-sha256:c9b00cdf029e657936ba3e51fa8a3c9361e315483eeda58e428aff5f1c3b6d3c`, with context `E1-OPERATIONAL-CONTEXT-sha256:109c1fb95fee2e95f58cce8ca7723384092706fa33a4ef7ec051abfdcacea125` and chain `c34a47deb5b0c8ffc3839fd3520a10e1eeb065f6a9e4d4b4e180945c9cb22483`. No prepared record was adopted.

## Current state and preservation

S3 remains exact and READY: `SupervisorInstance-sha256:83f22718a56ab733257208c6e1dfe9767a95e0d10b82f8583f222f88ee9669a2`, succession `SupervisorSuccession-sha256:b86bbb15d9d9d468b2de87926ad6b1cb4063218fd71eb5426089f689c0aecce8`. Fresh verification observes PID 1465900 / PPID 1465890 and the qualified socket/cgroup/workspace identity. Ownership NONE; ExecutionScope NONE; r11 namespace ABSENT. The qualified status/budget regressions pass; no live r11 status is claimed for an unissued invocation.

258 historical files, including prior qualification, r8/r9/r10 records and shared-ledger evidence, hash unchanged. r10 remains CANCELLED / INTERRUPTED_NO_EFFECTS. Zero real r11 model requests, ActionRequests, executions or implementation effects.

The next step remains an Architect decision covering the exact prepared records and r11 issuance. No automatic invocation or retry is authorized.
