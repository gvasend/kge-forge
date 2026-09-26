# A2.1n — Production Governed Execution Integration

Status: **live adapter path qualified; overall A2.1 no-bypass gate remains
FAIL**. The production integration completed live requalification against the
restarted external supervisor. A2.1c remains accepted as PASS. The actual
Codex host tool registry still exposes execution outside this adapter, so
A2.1, A2, E1-B01, and E1-WP-001 eligibility remain open/denied. E1-WP-001
was not dispatched.

## Implemented path

`ResponsesReasoning` now registers a strict `governed_exec` schema with
`executable`, `argv`, and `cwd`, maps that name to A2.3 `exec`, and assigns the
model call ID as ActionRequestId. It does not expose scope IDs, Bubblewrap,
bridge, or supervisor operations to the model.

`ReasoningOrchestrator` verifies session, turn, authorization ID/revision, and
ActionRequestId. It rejects caller-supplied `scope_id` or
`execution_scope_id`, then issues a sealed execution permit from `GovernedHost`.
The permit binds action ID, immutable host-generated ExecutionScopeId, argv,
and root. Direct `GovernedHost.governed_exec` without that permit and legacy
`Scope.launch` are denied. The old direct Bubblewrap payload launch was
removed from `governed_host.py`.

The intended production request chain is:

`ActionRequest` -> `ReasoningOrchestrator` -> `GovernedHost` ->
Bubblewrap-isolated `control_process` -> fixed-destination `ForwardBridge` ->
external supervisor -> `create` -> `production_spawn` ->
`adapter.exec_barrier` -> pre-execution `cgroup.procs` admission ->
unchanged Bubblewrap payload profile -> bounded result line -> `close` ->
recursive kernel quiescence poll -> `production_status` -> terminal ActionResult.

The control process validates action/session/authorization/scope identity and
one framed request. The bridge forwards that validated frame over the existing
Unix socket and verifies the correlated response. The supervisor's new
`production_spawn` operation owns the launcher, admits and independently
checks its `0::` membership before releasing the start barrier, then records
the first bounded payload result line. The restarted supervisor loaded this
operation.

`GovernedHost` records result availability separately from terminal success.
It marks the scope CLOSED, polls the supervisor's authoritative quiescence
decision, checks launcher exit status, and only then returns a successful
governed ActionResult with the same scope ID. If the channel, admission,
closure, observation, drain, or launcher status is uncertain, it records
INDETERMINATE and leaves dependent actions blocked. A second effect action or
finish request is denied while the prior scope is not QUIESCENT. After a
QUIESCENT scope, the next execution may receive a fresh scope ID.

## Tests and current limits

Fourteen adapter tests passed. New production tests cover valid model-facing
mapping, scope/action binding and audit, supervisor operation order, result
before quiescence, second action denied during drain and eligible afterward,
replay non-effecting, caller scope mismatch denied, direct legacy launch
denied, authorized executable denial for Bubblewrap, channel loss fail-closed,
and the start barrier refusing payload execution before release. A host-side
smoke check used the unchanged Bubblewrap flags, the isolated control process,
and a local synthetic Unix socket; it completed a correlated framed `create`
round trip. `git diff --check` passed. Existing tests still emit temporary
directory ResourceWarnings.

## Live requalification after host-authorized restart

The host-visible supervisor was PID 30193, UID/GID 1000:1000, with
`0::/kge-forge/executor` membership and cwd
`/home/gvasend/app/kge-forge`. `/tmp/a21m.sock` was owned 1000:1000,
mode 0600, and `ss` showed PID 30193 fd 3 listening on it. A final host
sample after the live scenarios showed the same process, membership, cwd,
socket ownership/mode, and listener. The supervisor was not changed.

A bounded fixture supplied one registered `governed_exec` model function call
with call ID `model-call-a21n-1`; `ResponsesReasoning` mapped it to the
ActionRequest ID. Its scratch payload printed `A21N_RESULT` and slept for two
seconds. The live audit recorded scope
`scope-a2c9a95457b747e6878b9d728fdf6b53` reserved, created, result
available from launcher PID 31716 with initial
`0::/kge-forge/executor/scope-a2c9a95457b747e6878b9d728fdf6b53`
membership, CLOSED, authoritative QUIESCENT with `populated 0`, and only then
the successful ActionResult and correlated function-call output. At result
availability, an independent kernel sample showed `populated 1` and
`cgroup.procs` members 31716, 31717, and 31718. A dependent exec and a finish
request were DENIED while the prior scope was not QUIESCENT. After QUIESCENT,
a fresh ActionRequest succeeded in a different scope,
`scope-760af64260974bf3a18da4610f68e98e`; replay of the first ID returned
the cached result without a new invocation.

The first scratch scenario, which attempted to create a surviving sleep child,
returned `INDETERMINATE` with `SupervisorError: payload result unavailable`.
Its scope `scope-ac7a4485cf30437b859a1e7b4980755f` never received a
QUIESCENT audit event or successful ActionResult, and later kernel observation
showed `populated 0`. A standalone host Bubblewrap and start-barrier diagnostic
both produced output, but this does not explain the first failure. A minimal
scratch retry and the timed scenario completed. The failure remains a material
limit on claims about payloads that fork and exit before the result channel is
observed; the fail-closed behavior was correct.

Final adapter probes denied caller-supplied `scope_id` and
`execution_scope_id`, identity mismatch, direct `GovernedHost.governed_exec`
without an ActionRequest permit, legacy `Scope.launch`, and Bubblewrap as an
authorized executable. A write-open attempt on the scope's `cgroup.procs`
from the current command sandbox failed with `EROFS`. Thirteen targeted
adapter tests passed; they emitted existing temporary-directory
ResourceWarnings. These probes qualify the local registered adapter surface.
The actual Codex host registry still offers `exec_command`, patch, and stdin
paths outside it, so the broader no-bypass closure is not met and no A2.1 PASS
or E1 dispatch eligibility is claimed.

Trusted host/administrator placement of another same-UID process inside the
executor remains outside the governed payload threat model. CLOSED is not
absolute kernel fencing against that separate host authority. No cgroup
permissions, Bubblewrap protections, transport types, or registered tool
names were broadened. Fabrik and `kge-forge-demo` were untouched.
