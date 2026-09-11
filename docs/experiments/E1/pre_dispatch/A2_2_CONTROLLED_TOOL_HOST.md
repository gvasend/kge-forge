# A2.2 — Controlled Codex Tool Host and Registry Ownership

Status: **BLOCKED — CODEX_HOST_INTERFACE_UNSUITABLE**

The audit of the available Codex app-server confirms that its `command/exec`
protocol is a controller API, not a replacement for the host tool registry. In
the actual session, the model received a custom `exec` tool whose body called the
surrounding host's `tools.exec_command`; `apply_patch` and `write_stdin` were also
host-provided. The registry therefore belongs to the surrounding Codex host/runtime,
not to the app-server invocation controlled by this project.

The AQ3.1 supervisor cannot be made authoritative by adding governed tools beside
those built-ins. That would leave an unsupervised effect-capable bypass and violates
the A1 invariant. No production product repository was touched and no E1-WP-001
work was dispatched.

## Candidate decision

The current app-server-plus-host-tools architecture is rejected. A caller-owned
function registry or app-server configuration that removes these built-ins was not
available in the installed 0.153.4 interface. The selected next architecture is a
reasoning-only external orchestrator: Codex receives no local effect tools, emits
structured governed requests, and the orchestrator owns the GEI registry,
WorkAuthorization, audit, and AQ3 supervisor. A custom host around a lower-level
model API is an equivalent fallback; maintaining a broad Codex fork is last resort.

## Evidence

AQ2's actual tool journal (`aq2-agent-tool-evidence.json`) records model custom
tool calls named `exec` invoking `tools.exec_command`, plus direct `apply_patch` and
`write_stdin` facilities. The generated app-server schemas expose thread/turn
operations and controller `command/exec`, but no caller-owned tool-registry
replacement or built-in suppression contract. The recorded inventory also exposed
non-governed capabilities. These are direct observations, not agent assertions.

No real Codex turn can satisfy A2.2's required negative inventory while this host
boundary remains active. Consequently governed_read/patch/exec iterative tests,
raw-bypass tests, and registry-owned provenance are not claimed as passing.

## Disposition

A2.2: **INCOMPLETE**. Tool-registry ownership: **OPEN**. A2.1 execution
quiescence: **OPEN**. E1-B01: **OPEN**. E1-WP-001 eligible: **NO**. AQ4 remains
deferred. The next authorized increment must implement the reasoning-only
orchestrator (or prove a supported caller-owned registry), then run scratch fake
repository qualification before any E1 adapter use.
