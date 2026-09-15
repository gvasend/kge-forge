# A2.1c authoritative lifecycle qualification — 2026-09-15

Status at this earlier attempt: **INDETERMINATE / FAIL-CLOSED**. Superseded by
`A2_1C_FINAL_LIFECYCLE_QUALIFICATION_2026-09-15.md` after host restoration.

The earlier diagnostic scope established supervisor-owned admission, closure,
late governed-admission rejection, `populated 0`, and an empty-scope
`QUIESCENT` response. These are not result-before-quiescence evidence.

The existing supervisor code was extended with a bounded `qual_spawn` operation
that admits a launcher before releasing its start barrier, forks a `setsid`
child and double-fork descendant, records a nominal result, and holds the final
descendant until `qual_release`. The `quiescent` method was also changed to
consult `cgroup.events` and fail if population is indeterminate. Syntax checks
and eight existing adapter tests passed. An isolated launcher smoke check
returned `ok` with the launcher exited and descendant PID still present,
then released the hold. This was not an authoritative cgroup observation.
The new path has **not** been run or
qualified on the host. No timing order for launcher admission, payload start,
descendant creation, result, launcher exit, admission closure, populated 1,
descendant exit, populated 0, or final QUIESCENT is established.

To load the updated code, the original supervisor PID 22468 was stopped.
The attempted restart first moved its shell into the delegated executor cgroup,
but the kernel rejected that migration with `Permission denied`. The command
originated in `0::/user.slice/user-1000.slice/session-2.scope`; the executor
parent now reports `populated 0`. The original listener is therefore **down**.
No authority above `/kge-forge/executor` was used to force a restart.

Admission paths identified in this implementation:

* The supervisor's `admit` and `spawn_barrier`/`qual_spawn` operations write
  `cgroup.procs`; its logical `CLOSED` state rejects subsequent `admit` calls.
* A host process with the same UID (1000) can open scope `cgroup.procs` for
  writing based on its owner/mode (1000:1000, 0644), as a write-open probe
  confirmed. An unbuffered PID write from this command's `user.slice` into
  the CLOSED scope failed with `EACCES` at the kernel migration boundary, but
  that does not prove that an already in-executor same-UID process is fenced.
* The current Codex command sandbox sees the cgroup mount as read-only:
  opening scope `cgroup.procs` for writing failed with `EROFS`. This is direct
  sandbox evidence, not evidence about all future payload sandboxes.
* Bubblewrap payloads in `adapter/governed_host.py` bind their scope work tree
  and system libraries, not the host cgroup mount. This is a code-level boundary;
  a live late-admission payload probe has not been run.
* The governed control protocol validates operation bindings and replay IDs,
  but its current process does not forward requests to this supervisor. Live
  replay and reopening probes after CLOSED have not been run.

The exact authority establishing CLOSED is the supervisor's in-memory scope
state under its lock. It prevents **governed** `admit` calls but is not a
kernel-level admission fence. Same-UID host write authority inside the executor
subtree remains unresolved. Do not treat a previous empty observation, launcher
exit, nominal result, or logical closure as race-safe QUIESCENT.

Verdicts: result-before-quiescence **INDETERMINATE**; descendant inheritance,
detachment, and launcher-exit-with-survivor **INDETERMINATE**; populated 1 after
result **NOT OBSERVED**; final populated 0 for the new qualification scope
**NOT OBSERVED**; race safety **UNPROVED**. A2.1c, A2.1, A2, and E1-B01 remain
open; E1-WP-001 remains ineligible and was not dispatched.
