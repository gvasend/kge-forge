# A2 — Governed Codex Host Implementation

Status: **INCOMPLETE; qualification blocked on scope-wide quiescence verification**

Implementation location: `adapter/` in Forge, revision pending review. This is
control-plane substrate code only; Fabrik and `kge-forge-demo` are untouched and
E1-WP-001 was not dispatched.

The implementation provides immutable `WorkAuthorization`, default-deny path
grants and denies, bounded governed read/write/patch/exec operations, typed
authority-expansion records, independent JSONL audit, per-turn `ExecutionScopeId`,
and a bubblewrap PID-namespace launcher. Raw host tools are not registered by this
package. The scope uses AQ3.1's containment primitive and a bounded terminate/kill
sequence.

The scratch test suite currently covers authorized read/write, protected denial,
whole-patch preflight, expansion recording without effect, scope identity, and
fresh-scope reuse. Four tests pass. A resource warning during revocation indicates
that the launcher exit is not yet sufficient proof that all namespace descendants
have ceased. The supervisor therefore does not yet satisfy the independent
quiescence gate, detached/stubborn worker matrix, normal-completion leak gate,
crash ownership, or no-bypass audit required for A2 acceptance.

The selected A2 host architecture remains a small custom Codex host with an
explicit GEI registry and no raw effect-capable built-ins. Completion requires
fixing scope membership/quiescence verification, then running actual Codex turns
through this registry. No E1 or AQ4 work may begin from this increment.
