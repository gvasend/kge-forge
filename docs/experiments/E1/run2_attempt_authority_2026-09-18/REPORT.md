# Run-2 r9 attempt authority qualification

RUN2_R9_READY_FOR_ARCHITECT_ISSUANCE

The material attempt-authority amendment and separately pinned implementation continuation are qualified in the private controller runtime. The immutable original Run-2 dispatch is preserved. Specific r9 issuance authority is still absent; no r9 authorization has been issued, activated, owned or dispatched.

The exact accepted replacement proposal remains byte-identical. Its historical release/context fields identify the predecessor authority; the append-only amendment derives the effective new authority and context without rewriting the proposal. The required replacement reason is PRE_ISSUANCE_ORCHESTRATION_FAILURE_NO_EFFECTS.

| Record | Identity / fingerprint |
|---|---|
| Material amendment | `E1-RUN2-ATTEMPT-AUTHORITY-AMENDMENT-sha256:2698e91a74ffe563c5ebd52e9f9be9d90a055dcabc569fd3a2b159d545964566` |
| Amendment file SHA-256 | `d465d852b4e819fa82ba4d25667ef55491c50a53e86877475bb412203ba4a983` |
| Non-material continuation | `CONTINUATION-sha256:b65358caaf9d2f4aa6e6e2a15aabc488cd7a26c56539594193a220923f8b0fd4` |
| Continuation file SHA-256 | `1a31ae31bd73a194b565a551396b4154e635bbd9060ec3cb2cdb6359e6d60b40` |
| Resulting release authority | `E1-RELEASE-AUTHORITY-sha256:a8e228850a699e201cd2202b76c6de7de976e7aa34890f3247afda4a599f0708` |
| OperationalContextId | `E1-OPERATIONAL-CONTEXT-sha256:9814f88f64b966a633d0fcc5142a2bfdb1564c8f92f5c07e81455ff1414c58ce` |
| Continuation/amendment chain | `45d9e90c1308d1f73b5c3d347e6a567ecf557a42fb2c486a2dc61c316deff0e9` |
| FullContextDigest | `e67c86fcda8be39605c48b974362fe5b20fbc8b3f181cf8f822d9bcce37815fc` |
| ModelProjectionBindingDigest | `0de148d39e6979f96d1d7aaa88cf5ae1dd353d0d8781f0d36f1b7b54bb4f0e20` |
| Unchanged ModelPayloadDigest | `d675d581c80f43e691a31da73ccf17fd4bcc6b00d3a5331f26b9294e294e1538` |
| Unchanged profile SHA-256 | `fb842649d30e5876fb3f299e890e2c555a88be759c29b2c6577552d4885b0226` |
| Qualified private controller implementation | `sha256:2f2b3aef4c0f29b42cad77fd5d394eda03242b93b76d69a3ffd7f0f79a4d72d9` |
| Qualification SHA-256 | `ab10a1adb4901f97347ce29af261106f1b512c20485bf56f63e780e951639357` |

Ancestry preserves original ReleaseBasis/ReleaseDecision, the supervisor material amendment, adopted continuations, the Run-2 material amendment and existing S2→S3 succession. The new attempt-authority amendment is appended to release authority c43f1191e2b631bb42bb1c48aaa6ba9a96d286bd169f93a8fac315c4cdb20286 and operational context 5e24ed8beba0c7c4e431852cb483e37531c6ab45d7199b91b626badd87825521. The new non-material continuation binds that exact predecessor and its chain.

Original DispatchAuthorization: `E1-ARCHITECT-DISPATCH-sha256:e20ee636c728511681bf45513147e0087ef86598b0454e90c28f5b7184468758`. It is not replaced or consumed. The prepared derived dispatch representation is a compatibility record, not a new Architect dispatch decision or an issued child authorization.

r8 remains `UNISSUED_PROPOSED_AUTHORIZATION_WITH_FAILED_CLOSED_AUDIT_NAMESPACE`. Independent recovery returns "original INACTIVE authorization missing". Its closed audit, Run-1 audit and ownership ledger retain their prior SHA-256 values.

r9 candidate: `auth-e1-wp-001-r9-6fad26f3eb6113d5cd4f0237d2b6f224`. Accepted binding SHA-256: `cb68a30719e88496504cd38004750b5b6848e4f31f1836387b87984ae92a8adc`. Its audit is absent: `/tmp/kge-forge-e1-evidence/auth-e1-wp-001-r9-6fad26f3eb6113d5cd4f0237d2b6f224/session-e1-run2-replacement-313ad15bc23fa5e2/turn-e1-run2-replacement-d1b79a64e4df9d8f/controller.jsonl`. The separate attempt-allocation ledger is empty. No lifecycle, owner, counters, effects or namespace are inherited.

S3 remains `SupervisorInstance-sha256:83f22718a56ab733257208c6e1dfe9767a95e0d10b82f8583f222f88ee9669a2` through `SupervisorSuccession-sha256:b86bbb15d9d9d468b2de87926ad6b1cb4063218fd71eb5426089f689c0aecce8`. Genuine independent readiness, identity, placement, socket/listener and exclusivity checks passed. PID 1465900 / parent 1465890 remain the qualified process relationship. All 39 released repository implementation files are unchanged.

| Independent production phase | Seconds |
|---|---|
| private_bootstrap | 16.983 |
| cold_private_bootstrap | 16.983 |
| cold_preissuance_production_validation | 26.977 |
| warm_preissuance_production_validation | 27.441 |
| operational_context_reconstruction | 0.369 |
| model_projection_validation | 4.273 |

All measured validation/preparation phases remained below the 30-second soft / 120-second hard thresholds. No budget was relaxed. New-invocation counters have not started. Token ceilings are not claimed without reliable accounting; the released USAGE_UNKNOWN behavior is preserved.

Qualification: 22 bounded synthetic lifecycle/composition tests, 2 dispatch-entry boundary tests, 29 actual-context negative probes and 41 regressions passed. The deadlock detector was 40 seconds; the longest integrated test took 11.009 seconds.

| Required check | Evidence result |
|---|---|
| 1_r8_closed | PASS: byte-identical closed audit; original recovery rejects missing initial issuance |
| 2_dispatch_authentic | PASS: original released controller independently authenticates immutable original decision |
| 3_material_amendment | PASS: private selected material decision and exact authority-source/body hashes |
| 4_exact_r9_binding | PASS: exact accepted proposal hash; issuance approval remains absent |
| 5_arbitrary_r10 | PASS: actual prepared-context substitution rejected |
| 6_unused_namespace | PASS: no audit path or attempt allocation |
| 7_INACTIVE_first | PASS SYNTHETIC: original issuance first; schema5 dispatch-entry guard exercised |
| 8_telemetry_after_issuance | PASS SYNTHETIC: start_control rejects missing/malformed initial authorization |
| 9_deadlock | PASS SYNTHETIC: 22 bounded tests, 40-second detector, no timeout |
| 10_exclusive_ownership | PASS SYNTHETIC: competing candidate/ownership and replay rejected |
| 11_ACTIVE_restart | PASS SYNTHETIC: separate process recovers ACTIVE and owner |
| 12_handoff_gate | PASS: actual prepared r9 rejected; synthetic eligibility only after recovered ACTIVE+ownership |
| 13_budgets_status | PASS: released budget/status/cancellation/uncertainty regressions |
| 14_S3_READY | PASS: fresh genuine observation in independent production preflight |
| 15_production_timing | PASS: cold/warm phases below soft threshold without relaxed checks |

Positive INACTIVE→intent→reservation→ACTIVE and restart tests use synthetic identities/stores, with only genuine kernel-supervisor observation mocked there. Actual r9 production qualification is non-effecting and includes genuine S3 readiness. This report does not claim real r9 activation or model-handoff eligibility.

The production runtime is `/tmp/forge-r9-context-69itwolf`. Its exact inventory is authenticated by the material amendment. The unchanged released controller verifies historical authority in a bounded read-only process; current ownership, lifecycle, context inputs and supervisor readiness remain freshly checked. The qualified private-store root is `/tmp/kge-forge-controller-authority/auth-e1-wp-001-r9-6fad26f3eb6113d5cd4f0237d2b6f224/attempt-authority-candidate6/qualified-prepared-v2`. It contains 678 logical entries / 656 distinct hash-verified single-link objects under mode 0700.

Materiality: the attempt-authority rules, versioned-context integration and exact child-decision gates are material and bound to the amendment. The accepted issuance ordering and audit-lock composition artifacts retain their exact non-material continuation evidence. Telemetry remains non-authoritative; the lock remains non-reentrant. Profile authority, tool schemas, payload, transmission/retention, budgets, supervisor authority, execution, ownership and recovery acceptance rules are unchanged.

Preparation defects were preserved and corrected before the final snapshot: an issuance-helper name collision; the dispatch entry needed a durable-issuance guard; an incorrectly scoped missing-profile test; and a snapshot-copy optimization that violated the existing single-link object invariant. The rejected snapshot is historical preparation evidence only. The final snapshot uses independent byte-identical objects and passed fresh-process reconstruction.

Evidence: [final result](FINAL_RESULT.json), [publication](AUTHORITY_PUBLICATION.json), [external private pin](CURRENT_PIN.json), [qualification](candidate6/QUALIFICATION.json), [fresh reconstruction](independent_reconstruction_v2/PREFLIGHT.json), [negative probes](candidate6/NEGATIVE_PROBES.json), [implementation delta](IMPLEMENTATION_DELTA.json), [source diff](IMPLEMENTATION.diff).

Stop condition: await the specific Architect issuance decision. No r9 issuance, activation, ownership acquisition, model request, execution or implementation effect occurred.
