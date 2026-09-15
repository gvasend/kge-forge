# A2.1c final authoritative lifecycle qualification — 2026-09-15

Verdict: **PASS within the established trusted-host KGE Forge authority model**.
This is not absolute kernel fencing against a trusted operator or an arbitrary
same-UID host process already inside the delegated executor subtree. A2.1 and
A2 remain open for the other host-integration and no-bypass gates. E1-B01 is
open; E1-WP-001 is ineligible and was not dispatched.

## Restored supervisor

The host listener was independently identified as PID 25455, UID/GID
1000:1000, `0::/kge-forge/executor`. `/tmp/a21m.sock` was a 1000:1000 socket,
mode 0600, in Unix stream `LISTEN` state, fd 3. It returned `READY`. The
supervisor was not stopped, restarted, replaced, or reconfigured in this run.

## Result-before-quiescence sequence

The diagnostic scope was `a21c-lifecycle-20260915`. All timestamps below are
monotonic nanoseconds from the qualification process and supervisor, and only
establish order, not a wall-clock timebase.

| Event | Time / evidence |
|---|---|
| Supervisor-owned launcher admission | 6569239878542; `admitted: true`, launcher PID 26293 |
| Payload start | 6569271962169, after admission barrier release |
| Double-fork descendant creation | 6569272780353; `setsid` child PID 26295, final descendant PID 26296 |
| Nominal result available | 6569273442054; `result: ok` |
| Launcher exited | 6569281036939; return code 0; `/proc/26293` absent at first observation |
| Populated-1 observation after result/launcher exit | 6569281419462; `cgroup.events: populated 1`, `cgroup.procs: 26296` |
| Admission closure | Supervisor returned `CLOSED`; closed-with-survivor sample at 6569283106884 remained `populated 1` |
| Descendant release | 6569285839445 |
| Final descendant exit and populated-0 observation | By 6569386803372; descendant `/proc` absent, `cgroup.procs` empty, `cgroup.events: populated 0` |
| QUIESCENT decision | After populated 0; supervisor returned `quiescent: true`, `state: QUIESCENT`; follow-up sample at 6569387850768 remained `populated 0` |

The detached PID 26296 was sleeping, had PPid 1, UID/GID 1000:1000, and
`0::/kge-forge/executor/a21c-lifecycle-20260915` while PID 26293 was gone.
This proves inheritance, `setsid`/double-fork detachment, and launcher exit
with a survivor. The supervisor returned `quiescent: false` in `ACTIVE` before
closure and again in `DRAINING` after closure while the kernel reported
`populated 1`. Dependent work remained ineligible despite the nominal result.
Only `CLOSED` plus kernel `populated 0` led to QUIESCENT.

A second bounded scope, `a21c-lifecycle-live-20260915`, independently closed
the live-launcher membership gap without changing the supervisor. A host-side
poller captured 39 `/proc/26810/cgroup` samples before payload start at
6823019775580. They showed
`0::/kge-forge/executor/a21c-lifecycle-live-20260915` after supervisor
admission (6822990442297) and before payload execution. That launcher's
result was `ok` at 6823021135361 and it exited at 6823028707762. At
6823029380619, kernel `cgroup.events` was `populated 1`, `cgroup.procs`
contained detached/reparented PID 26813, and `/proc/26810` was absent.
Closure, late/replayed rejection, `DRAINING` while populated, release, final
`populated 0` at 6823134222347, and final `QUIESCENT` repeated in the second
scope. This independently verifies launcher membership before payload start.

## Closure and admission authorities

`CLOSED` is the supervisor's in-memory state under its admission/quiescence
lock. A late `admit` request naming PID 26296 and its repeated request both
returned `scope not admissible`. A `create` request with the same scope ID
returned `scope already exists`; no reopening path was observed. The governed
broker protocol separately rejected a repeated request ID with
`replay or missing request`. That protocol is not yet connected end-to-end to
this supervisor, so this check is a local control validation, not A2 closure.

Kernel membership authority is `cgroup.events`' recursive `populated` field,
corroborated by `cgroup.procs` and `/proc/<pid>/cgroup`. It includes descendant
cgroups and does not infer emptiness from ancestry, result, or launcher exit.

The scope and executor-parent `cgroup.procs` files are both 1000:1000 mode
0644. Linux cgroup-v2 migration requires write access to the destination and
the source/destination common ancestor. A same-UID process already within the
delegated executor subtree can therefore migrate a process within that subtree
directly, bypassing supervisor `CLOSED`. This capability is an inference from
the observed permissions and the kernel's documented migration rule, not a
live write from an already-in-executor rogue process. The current executor
parent contained only supervisor PID 25455 at the final observation. A
same-UID host write-open succeeded from `user.slice`, but its unbuffered PID
migration into the closed scope failed with `EACCES` because the common
ancestor lies outside the delegated subtree.

The existing Bubblewrap payload profile (`--die-with-parent`, PID namespace,
separate session, work-tree bind, read-only system binds, network unshare)
could not see the host cgroup path: payload PID 2 reported the path absent and
`os.open(..., O_WRONLY)` failed with `ENOENT`. The current Codex command sandbox
also failed write-open with `EROFS`. No payload self-admission or direct
cgroup-write capability was observed through these sandbox paths. The bounded
qualification launcher itself was an unsandboxed diagnostic, so its authority
while alive is not used to establish governed-payload confinement.

Trusted operator/host-administrator authority can place or run another
same-UID process in the executor subtree. Such a process could bypass CLOSED;
the cgroup filesystem does not provide an absolute seal. The established E1
model trusts the host/GEI boundary, excludes unmediated Agent tools, and treats
operator intervention as a separate authority. **Within that model**, the
only resident executor-parent runtime process at final zero was the supervisor,
the supervisor rejected admission after CLOSED, and payloads lacked a direct
cgroup path. CLOSED plus authoritative recursive zero membership therefore
supports race-safe QUIESCENT conditionally. If another same-UID host process is
admitted to the executor outside the supervisor, or if a payload can see a
writable cgroup mount, the guarantee fails and status must revert to
INDETERMINATE/fail-closed.

Linux kernel semantics used for this classification:
https://docs.kernel.org/admin-guide/cgroup-v2.html (delegation containment,
`cgroup.procs`, and recursive `cgroup.events populated`).
