# A2.1c external supervisor admission check — 2026-09-15

Status: **PARTIAL / FAIL-CLOSED**. E1-WP-001 was not dispatched.

The external supervisor at PID 22468 was independently observed as UID/GID
1000:1000, with `0::/kge-forge/executor` membership. `/tmp/a21m.sock` was
owned by 1000:1000, mode 0600, and `ss` showed a Unix stream `LISTEN` socket
held by PID 22468, fd 3. Its local `status` response was `READY`.

Through that socket, the supervisor created
`/kge-forge/executor/a21c-20260915-verify`, spawned launcher PID 23707 with
a start barrier, admitted it, verified it in `cgroup.procs`, and released the
barrier. An independent `/proc/23707/cgroup` read showed
`0::/kge-forge/executor/a21c-20260915-verify`. The launcher then became a
zombie under the supervisor; its scope had empty `cgroup.procs`, no child
cgroups, and `cgroup.events` reported `populated 0`.

The supervisor returned `CLOSED` for admission closure, rejected a later
`admit` request with `scope not admissible`, and returned `QUIESCENT` after
the empty-scope observation. The late-admission probe named PID 22468 and was
rejected before any cgroup write; the supervisor remained in the executor
parent scope.

This is not full A2.1c acceptance. The live `spawn_barrier` operation uses a
one-byte child that exits immediately, so it supplies no payload result or
descendant-containment observation. The live `quiescent` implementation reads
only the scope's direct `cgroup.procs` members and does not couple its terminal
decision to `cgroup.events` (`populated 0`), descendant cgroups, or an
external-writer exclusion mechanism. Therefore result-before-quiescence and
final race-safe QUIESCENT remain unproved. No permission above
`/kge-forge/executor` was requested or used.
