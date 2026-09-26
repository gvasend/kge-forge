# r13 issuance gate

The narrow current-state checks pass, but issuance is blocked fail-closed by the exact candidate binding.

Verdict: `BLOCKED_BEFORE_ISSUANCE`.

The malformed artifact remains historical only. The corrected [canonical binding](./CANONICAL_R13_BINDING.json) uses the production constructor's complete schema. Its structured `InvocationAttemptId` is `InvocationAttempt-sha256:5a740034573fbd4889ec9e0d647bbf244ae347bb1b41ba0b44f947834ce5df8c`; its canonical binding SHA-256 is `b73707fe29554fd73eec80847eec06550789a4318f6bdff83403a482f3588a75`.

The current R3 runtime, runtime-head authority, release authority, OperationalContextId, exact S3 succession/readiness, profile, payload, transmission, and budget bindings all match the accepted production state. The r12 audit hash is `d1d2b4a202843b16ced71fec21fa7a55e459e8f2bd6f57c743a3cf64d1dd853f`; its ownership is released, no ExecutionScope remains, and QUIESCENT is established. The r13 audit namespace is absent and unused; no r13 record, ownership, activation, model request, or effect exists.

The canonical preflight is recorded in [CANONICAL_PREFLIGHT.json](./CANONICAL_PREFLIGHT.json). The malformed candidate never entered the authoritative allocation ledger, so the human-visible `r13` number remains available; the corrected candidate has a new structured identity and new bytes. No production runtime, release authority, supervisor authority, or historical evidence was changed. No r13 lifecycle record, ownership, activation, model request, or effect exists.

The fresh issuance gate is recorded in [R13_FRESH_GATE_BLOCKED.json](./R13_FRESH_GATE_BLOCKED.json). The R3 production consumer rejects reconstruction of the r12 predecessor with `AuthorityDenied: bootstrap operational binding mismatch`. Issuance therefore stopped before the first lifecycle fact; the canonical candidate remains unissued and the production context/authority binding requires Architect review.

The corrected canonical object has no extra authority-bearing fields: its external SHA-256 is `b73707fe29554fd73eec80847eec06550789a4318f6bdff83403a482f3588a75`. Dispatch bindings match the authenticated Architect dispatch `E1-ARCHITECT-DISPATCH-sha256:6e676c5decd4ae745d8977c2392e559896403ce5d6507db7dafc4f7a92ddd1ab`; the r12 predecessor audit hash and fresh audit path validate, and the structured attempt identity recomputes exactly.
