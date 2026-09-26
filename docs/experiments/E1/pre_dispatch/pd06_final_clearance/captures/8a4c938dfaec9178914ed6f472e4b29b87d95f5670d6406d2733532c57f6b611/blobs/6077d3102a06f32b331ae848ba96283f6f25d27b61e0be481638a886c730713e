# E1 adapter capability review — preparation only

Date: 2026-09-11. Finding: **INTERFACES OBSERVED; END-TO-END QUALIFICATION NOT ESTABLISHED**.
This is host/tooling evidence, not service implementation or an agent work result.

## Local observations

- Installed executable resolves to the local `@openai/codex` CLI; reported version
  is `codex-cli 0.153.4`.
- `codex exec --help` exposes working-root selection, sandbox selection, JSONL
  events, schema-constrained final output, and configuration/rule controls.
- `codex app-server --help` exposes local transports and protocol-schema export.
- Local generated schemas expose thread read/status, turn interruption, and
  sandboxed command execution interfaces. Snapshot extracts are in
  adapter_schema_evidence.json; the full diagnostic export was temporary.
- The installed sandbox command syntax is `codex sandbox [OPTIONS] [COMMAND]...`.
  An initial `codex sandbox linux --help` probe was inappropriate for this version.
  Its nested sandbox failed on a read-only mount-registry lock; an escalated retry
  exposed the invalid `linux` executable argument. The original probe was stopped
  and ended with exit 130. Correct help inspection succeeded. These are diagnostic
  failures, not evidence that a correctly configured adapter cannot work.
- No model turn or implementation session was launched. No account credential,
  authentication file, unrelated session content, or external repository was read.

## What remains unproved

CLI presence and schema fields do not prove effective confinement of all tools,
protection of baseline/package files, exclusion of unrelated connectors and read
access, event attribution, or stop/recovery behavior in the intended invocation.
The current Architect tool environment is not silently adopted as a distinct
qualified Implementation Agent. Broad root write access or process termination
alone cannot substitute for E1-ARCH-1 §§4–5.

Required qualification evidence before E1-WP-001 dispatch:

1. A specifically identified local invocation facility and effective configuration
   that confines reads/writes to the approved source/runtime/scratch scope and
   prevents modification of authority, package files, and the other repository.
2. Denial of out-of-scope writes, reads, commands, network/tool destinations and
   approval expansion, demonstrated with nonsensitive scratch sentinels.
3. One attributable session/turn, recorded status transitions, interruption to a
   confirmed terminal outcome, and handling of a lost response without duplicate
   dispatch. Observe state without inspecting unrelated user sessions.
4. Proof that allowed work is possible within the same boundary; a profile that
   denies everything is not a conforming implementation facility.
5. Persisted qualification evidence bound to the exact runtime version, profile,
   work scope and tested capabilities; repeat checks when relevant configuration changes.

This separate diagnostic must not implement Forge or the service. No full-access
agent, broad permission change, alternate external destination, or human assertion
without supporting evidence can close this gate. PD-05 records the needed
bootstrap-facility designation/qualification authorization.

## Documentation corroboration

Official documentation describes thread inspection and turn interruption, but
does not establish behavior of this local configuration. See
[OpenAI App Server documentation](https://learn.chatgpt.com/docs/app-server).
Sandbox behavior also depends on effective configuration and enforcement; see
[OpenAI sandbox documentation](https://learn.chatgpt.com/docs/sandboxing).
These sources support interface discovery only, not a dispatch-readiness claim.
