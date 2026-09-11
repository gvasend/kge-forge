# A2.3 — Reasoning-Only Governed Orchestrator

Status: **INCOMPLETE; protocol substrate implemented, real Codex reasoning endpoint not qualified**

Implementation is in `adapter/orchestrator.py` at the A2 adapter revision. The
orchestrator accepts versioned JSON `ActionRequest` objects only; ordinary prose,
unknown actions, malformed requests, stale identity/revision, and replay are
non-effecting denials. It binds session, turn, authorization revision, and
invocation identity before delegating read/write/patch/exec to the A2 governed
host. Authority expansion is recorded as a pending, non-effecting request.

The protocol supports read, write, patch, exec, status, authority expansion, and
finish actions. Results are structured and retained by `ActionRequestId`, so a
replay returns the original result rather than duplicating an effect. Model text
is never parsed as shell or patch instructions. The host remains the sole owner
of authorization and execution scope.

The scratch protocol tests pass (7 total A2 tests including 3 orchestrator tests)
for typed operations, denials, malformed/prose/unknown requests, whole-patch
behavior, and replay. However, the installed Codex app-server cannot provide a
caller-owned reasoning-only tool registry or a lower-level model endpoint in this
environment. Consequently no real Codex turn has exercised this protocol, and
the autonomous programming loop, real tool inventory exclusion, and model/API
failure behavior remain unqualified. Existing A2.1 execution-scope warnings also
remain open.

This increment does not close A2.2 or E1-B01 and does not authorize E1-WP-001.
