# A2.1 — Execution-Scope Quiescence and No-Bypass Closure

Status: **INCOMPLETE / BLOCKED**

The A2.1 increment strengthened the scratch supervisor to record a process group,
revoke by group (SIGTERM, bounded SIGKILL), and perform an external `/proc`
membership check before setting `QUIESCENT`. The governed-host tests still pass
(4 tests), but Python emits a live-child `ResourceWarning` during the scope test.
The launcher/process-group result is therefore not yet sufficient proof of
namespace-wide quiescence. This remains a fail-closed result.

The larger acceptance gate is also unmet: the actual Codex host tool registry has
not been replaced. Agent-visible `tools.exec_command`, patch, and stdin paths are
still outside this adapter, so no-bypass and real Codex integration cannot pass.

Substrate implementation changed only `adapter/governed_host.py` in Forge. No
Fabrik or `kge-forge-demo` files changed and E1-WP-001 was not dispatched.

Required next increment: use a supervisor whose scope membership is observable
independently of launcher/process-group exit (for example a namespace init/watchdog
with an explicit scope-empty protocol), then integrate the GEI registry at the
host layer that owns Codex tool presentation. Until both are proven, Codex
terminal state cannot become architectural terminal state.
