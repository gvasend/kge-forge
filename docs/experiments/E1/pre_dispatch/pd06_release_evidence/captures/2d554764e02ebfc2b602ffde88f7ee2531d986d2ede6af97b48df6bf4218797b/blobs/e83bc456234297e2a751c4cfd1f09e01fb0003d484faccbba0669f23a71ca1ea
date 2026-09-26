# A2 next prerequisite — Effective Profile and Evidence Boundary

Historical verdict for the demonstrated bypass and temporary guard: **PARTIAL; A2/E1-B01 remained BLOCKED on protected-path execution scoping**. The controller-owned snapshot qualification in `A2_CONTROLLER_EXECUTION_WORKSPACE_2026-09-15.md` supersedes this temporary guard while preserving the bypass evidence. A2.1 remains accepted as PASS for the Forge-owned Programmer's
execution admission and quiescence path. This increment found an A2
authorization failure in the writable repository mount, applied a host-side
fail-closed guard, and stopped before any supervisor/profile change.
E1-WP-001 was not dispatched.

## Gate selected

E1-ARCH-1 and the A1 GEI require an effective WorkAuthorization profile,
protected authority/evidence paths inaccessible to the Programmer, denied
out-of-scope effects, and independent audit before the invocation facility can
close E1-B01. A2.1p proved allowed iterative work but its original scratch
audit was under the repository grant. The next narrow prerequisite was to
qualify those grants and protect evidence from both file tools and executable
payloads.

## Evidence and fix

`GovernedHost` now rejects an audit path inside *any* agent read or write root
at construction. The internal path policy also explicitly denies the audit
path. The live real `gpt-5` Programmer fixture was rerun with repository
`/tmp/a21p-programmer-dd307b2b63cb46a891fac9fabe5951dd` and separate
audit root `/tmp/a21p-evidence-1674910c7e884301a215bd025dc5459f`;
it completed eight cycles, two governed
test executions, edit recovery, and authorized finish. A second real rerun
after the fail-closed execution-root policy completed in
`/tmp/a21p-programmer-68f8432112bf4aae94b256f5f0671a6a`, audit root
`/tmp/a21p-evidence-36067484ca7c496486bc6b4f168632cd`, with two
successful execution scopes. Neither audit root was inside the writable
repository bind.

Bounded scratch dispatcher probes denied out-of-root read and write, audit
read and write, and an unregistered direct-shell name. A shell authority
request recorded only `PENDING`. A governed Python network-connect attempt
returned `NETWORK_DENIED` and completed through QUIESCENT. A governed Python
attempt to write the separate host audit returned `AUDIT_UNREACHABLE` and
completed through QUIESCENT. The private sentinel remained unchanged.

An additional scratch probe established a material path-policy bypass:
`governed_write` denied `protected.txt` inside the repository, but a
`governed_exec` Python payload wrote that same file through the existing
writable `/scope` bind and returned a successful, quiescent ActionResult.
This is an A2 authorization failure, not evidence that the accepted
ExecutionScope quiescence mechanism regressed.

The host now fails closed before scope creation unless the entire execution
root is inside a write grant and no `deny_roots` path is inside or above that
root. The protected-path probe was rerun: both governed file write and
governed execution returned DENIED, `protected.txt` remained `UNCHANGED`,
and no execution scope was reserved. This prevents the demonstrated bypass,
but cannot run tests from an E1 repository root containing protected package,
policy, or evidence paths. It also denies execution under a narrow per-file
write grant even when a read-only test would be safe. Nineteen adapter tests
passed, and `git diff --check` passed.

## Remaining prerequisite and host intervention

The qualified production Bubblewrap profile currently binds the whole
execution root writable. To both run tests in a repository with internal
protected paths and enforce file grants against arbitrary interpreter
payloads, the execution mount profile needs a separately reviewed strategy:
read-only repository presentation with only explicitly authorized writable
paths, or a controller-produced execution snapshot with exact source/evidence
provenance and no protected content. The former changes the supervisor-owned
`adapter.exec_barrier` launch profile and requires a host-authorized supervisor
reload. The latter requires an equally strong source-to-snapshot binding
qualification. Neither was implemented in this increment; the external
supervisor PID 30193 was not modified or restarted. Host intervention is
required before choosing or deploying a supervisor-side profile change.

Further A2/E1-B01 gates remain after this issue: exact E1 context and
authorization binding, Git committed-source inspection without indirect
execution, interruption/recovery under uncertain channels, and fresh
pre-dispatch status/release evidence. A2.1 can remain closed for the
Programmer execution-authority path; A2 and E1-B01 cannot close, and
E1-WP-001 is not eligible.
