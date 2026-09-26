# A2.1 final governed-execution integration and no-bypass qualification

Verdict: **FAIL**. A2.1c's authoritative lifecycle qualification remains
accepted as PASS within the trusted-host model and was not repeated or changed.
The registered governed execution path bypasses that supervisor. A2, E1-B01,
and E1-WP-001 eligibility remain open/denied; E1-WP-001 was not dispatched.

## Actual path and registered surface

`ResponsesReasoning` registers `governed_read`, `governed_list`,
`governed_search`, `governed_write`, `governed_patch`, `governed_exec`,
`governed_status`, `governed_git_status`, `governed_git_diff`,
`authority_expansion_request`, and `finish_task`. No built-in shell or code
tool is requested by this local registry. `governed_exec` is the sole declared
execution-capable tool. Write and patch are project-effect tools, not process
execution. The other declared names are read/status/control requests.

The current execution implementation is:

`ActionRequest` -> `ReasoningOrchestrator.request(type='exec')` ->
`GovernedHost.governed_exec` -> legacy `Scope.launch` -> direct Bubblewrap
`subprocess.Popen`. The process starts in the caller's host cgroup. Neither
`adapter/control_process.py` nor `adapter/forward_bridge.py` is called by this
path, and no socket request reaches the external supervisor. The legacy `Scope`
decides quiescence from a process group, not recursive kernel population.

The A2.4 model-facing registry is not yet a working dispatch contract either:
the strict `governed_exec` tool schema has no executable/argv/cwd fields, and
`ResponsesReasoning` forwards its tool name as the action type
`governed_exec`, whereas A2.3 accepts `exec`. A model-supplied request through
that declared name cannot exercise the valid `exec` branch. This is not a
substitute for an end-to-end production qualification.

## Live scratch evidence and negative probes

Only `/tmp/a21-no-bypass` was used. A valid synthetic ActionRequest
`req-a21-real-path` returned `SUCCEEDED`, scope
`scope-cde20b17f4c948c38be233901fff510f`, and PID 27445. An independent
`/proc/27445/cgroup` read showed
`0::/user.slice/user-1000.slice/session-2.scope`, not a scope under
`/kge-forge/executor`. Host status showed `scope_state: ACTIVE` and
`architectural_state: RUNNING` after ActionResult. Its audit had authorization,
invocation, and ActionResult entries but no supervisor request, cgroup
membership, CLOSED, populated-zero, or authoritative QUIESCENT event.

| Probe | Observation |
|---|---|
| Direct execution without ActionRequest | Direct `GovernedHost.governed_exec` launched PID 27527 in `user.slice`; audit contained no ActionRequestId. This internal host method is not itself a registered reasoning tool, but A2.3 reaches it. |
| Old host path / direct Bubblewrap bypass | The registered `exec` branch launched PID 27445 through `Scope.launch`, outside the supervisor. **Effect-capable bypass.** |
| Replayed ActionRequest | A repeated `req-first` returned the cached ActionResult; invocation count stayed 1. Non-effecting replay, but not a fresh rejection. |
| Mismatched ActionRequestId / ExecutionScopeId | A second request carrying `execution_scope_id: mismatched-scope` was `SUCCEEDED` with PID 27495; A2.3 does not validate or bind this field. The generated ActionRequestId is not carried to the supervisor. |
| Execution after locally CLOSED legacy scope | A scratch legacy `Scope` with state `CLOSED` denied launch (`scope is not active`). No authoritative supervisor CLOSED was reached by production execution. |
| Dependent action while prior work remained | `req-second` returned `SUCCEEDED` while first PID 27494 was still alive and the legacy scope was `ACTIVE`. **Quiescence-before-dependent-work gate failed.** |
| Direct cgroup mutation from current command sandbox | Write-open on the diagnostic scope's `cgroup.procs` failed with `EROFS`; no migration occurred. The accepted A2.1c Bubblewrap payload probe had found the cgroup path absent. |
| Legacy/diagnostic adapter reachability | Legacy `Scope.launch` is reachable through `governed_exec`; `qual_client` is not registered. Control process and forwarding bridge exist but are disconnected. |

The complete model/tool-call -> ActionRequest -> authorization -> ExecutionScopeId
-> supervisor request -> pre-execution admission -> kernel membership -> result
-> CLOSED/populated zero -> QUIESCENT -> ActionResult/dependent eligibility chain
was **not demonstrated** and cannot be reached through the current code.
The live chain stopped at the old host launch and premature ActionResult.

## Trust boundary and next integration requirement

A trusted host operator can deliberately place another same-UID process inside
`/kge-forge/executor`; A2.1c does not claim absolute kernel fencing against
that authority. Governed payloads and the reasoning session have no such
authority. The failure here is independent of that assumption: the registered
governed execution path itself never enters the qualified scope.

The existing supervisor operations spawn only fixed diagnostic children
(`spawn_barrier` and `qual_spawn`). None accepts an authorized production
payload through the control/bridge path. Completing the specified production
chain would require host-coordinated supervisor and adapter integration, then
fresh A2.1 integration testing; it does not require reopening A2.1c lifecycle
semantics. No supervisor was stopped, restarted, replaced, or reconfigured in
this qualification. No production code was changed in this A2.1 turn. Eight
existing adapter tests passed, but they do not cover the failing integration
path and emitted existing Bubblewrap/resource warnings.
