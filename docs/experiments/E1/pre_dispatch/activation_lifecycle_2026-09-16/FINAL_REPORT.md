# E1 authorization lifecycle qualification — 2026-09-16

**Synthetic lifecycle qualification PASS. Existing E1 activation BLOCKED.**

The existing Architect dispatch decision and invocation
`auth-e1-wp-001-r7-94f511dfcdcc43ac837191f8732ced39` are preserved. No new
dispatch authorization, replacement identity, operational binding, or release
profile was generated. The historical E1 audit and common ownership ledger are
byte-unchanged. PD-06 remains RELEASED, E1-B01 PASS, E1 INACTIVE, and E1-WP-001
INELIGIBLE and UNDISPATCHED.

## Implemented lifecycle

`adapter/authorization_lifecycle.py` adds controller-only, identity-bound
dispatch-authorized, activation-intent, activation-commit and terminal-history
recognition. Activation retains the original INACTIVE authorization. The commit
binds the exact dispatch reference, release basis/decision, operational context,
continuation chain, full context, model projection, profile, task, session/turn,
audit and ownership ledger. Its canonical SHA-256 determines the event identity.

The normal activation phase locks the shared ownership ledger and the existing
audit, checks for conflicting ownership, invokes the controller's complete
dispatch validator under those locks, and accepts only the complete PASS result
set. It fsyncs dispatch and intent records before fsyncing ACTIVE. An incomplete
intent is non-active and explicitly uncertain; automatic retry is denied.
Recovery independently reconstructs the resulting ACTIVE authorization before
returning. Identical replay performs no write or repeated effect; distinct
competing transitions fail closed.

Recovery validates the original authorization, byte-prefix audit commitment,
event fingerprints, event ordering and effective authorization. It distinguishes
INACTIVE, DISPATCH_AUTHORIZED-but-inactive, ACTIVATION_INDETERMINATE, ACTIVE,
COMPLETED, REVOKED and CANCELLED. Contradictory or truncated history is rejected.
The host, dispatcher and model continuation recheck lifecycle state. A dispatch
permission alone no longer permits ACTIVE on a fresh audit without activation
history. Existing legacy diagnostic profiles released directly ACTIVE retain
their previous behavior; the new lifecycle is required for profiles released
INACTIVE.

The lifecycle activation phase does not itself issue model requests, reserve an
ExecutionScope or run payloads. Invocation ownership and host activation remain
subsequent prerequisites. Synthetic qualification supplies controlled validator
observations; it is not evidence that current E1 host prerequisites passed.

## Qualification results

`QUALIFICATION.txt`: **30 tests passed**, comprising 16 lifecycle tests and 14
focused continuation, context separation, recovery, ownership, dispatcher and
tool-registry regressions. No API calls or payload executions occurred in these
tests. The context-separation regression uses local simulated model responses.

| Required case | Result |
|---|---|
| Valid INACTIVE → ACTIVE; original bytes preserved | PASS |
| Restart before activation remains INACTIVE | PASS |
| Restart after durable activation reconstructs exact ACTIVE | PASS |
| ACTIVE without event rejected | PASS |
| Wrong dispatch reference rejected | PASS |
| Wrong authorization identity rejected | PASS |
| Wrong context/profile/task binding rejected | PASS |
| Exact replay non-effecting | PASS |
| Competing duplicate transition rejected | PASS |
| COMPLETED/REVOKED/CANCELLED cannot reactivate | PASS |
| Truncated audit and incomplete activation fail closed | PASS |
| Original INACTIVE record mutation detected | PASS |

Additional tests cover failed validation with no append, interrupted commit with
no automatic retry, dispatch authorization without activation remaining inactive,
and rejection after activation evidence is removed from a live host's audit.

`SYNTHETIC_PROOF.json` preserves a complete positive example, original audit
bytes, effective authorization, ordered audit, restart result, event identity and
fixture-file fingerprints. Its event is synthetic, not an E1 activation event:
`E1-AUTHORIZATION-LIFECYCLE-sha256:f20ac0b372d22fa82f1a9a88803229cfa56c74552b09f4cb43fb7b038af48b4a`.

## Existing E1 validation

`E1_VALIDATION.json` records the actual fail-closed preflight. The normal
CommittedContext/governance verifier rejected current controller bytes with
`context artifact content changed`, before an activation intent or model request.
The shared ledger and exact audit were locked for this read-only check.

The authorized lifecycle correction changed four runtime files pinned by the
existing operational implementation supplement:

- `adapter/governed_host.py`
- `adapter/orchestrator.py`
- `adapter/recovery_ledger.py`
- `adapter/responses_orchestrator.py`

The new `adapter/authorization_lifecycle.py` is also absent from that existing
supplement. Exact authorized/current hashes are recorded in `E1_VALIDATION.json`
and `SOURCE_SHA256.json`. These are attributable implementation changes required
by the current instruction, not unexplained repository drift. They change
authorization/recovery enforcement and cannot be treated as a non-material
governance-document append or silently substituted under the existing exact
FullContextDigest and operational binding.

The release profile, launch artifact, release basis/decision, continuation
records, transmission-clearance manifest, work-package bytes, existing dispatch
record and stored operational binding retain their authorized fingerprints.
No replacement current-context/projection digests were invented. The remaining
live host/scope/provisioning checks are not claimed to have completed atomic
dispatch validation after the binding failure.

| Requested E1 outcome | Actual result |
|---|---|
| Activation event identity/fingerprint | None; event not created |
| Effective authorization | Historical INACTIVE unchanged; current binding rejected |
| ACTIVE restart/recovery | Not reached for E1; qualified on synthetic identities |
| Invocation ownership reservation | Not acquired; ledger empty and unchanged |
| Released-profile activation | Not performed |
| First model request / implementation effect | None |
| ACTIVATED_AND_READY_TO_DISPATCH | Not established |

Return to the Architect for applicability/binding disposition of the qualified
lifecycle implementation. The existing dispatch decision is preserved; its
conditional execution prerequisites have not passed. No audit rewrite, reset,
alternate audit path, new authorization identity, uncertain-effect retry or
dispatch occurred.

The existing controller/audit integrity assumption remains applicable. Events
are hash-bound, ordered and fsynced; neither this mechanism nor the evidence
package is claimed to provide privileged write-once storage against a hostile
controller or host.
