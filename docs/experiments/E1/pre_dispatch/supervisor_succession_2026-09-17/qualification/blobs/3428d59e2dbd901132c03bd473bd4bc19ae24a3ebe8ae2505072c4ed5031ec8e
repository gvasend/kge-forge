# Supervisor instance and succession schemas

All hashes use SHA-256 over UTF-8 canonical JSON (sorted keys, compact separators).
An object's `id` is excluded from its own identity hash. Immutable objects are
resolved through the existing Controller Authority Store; repository paths are
engineering provenance. `sha256:` references hash exact private object bytes.
An authority label alone is never trusted: the externally approved catalog pins
both the policy and the exact authorization objects admitted by that policy.

## SupervisorInstanceId

`SupervisorInstance-sha256:<SHA256(instance body)>`, schema
`SUPERVISOR-INSTANCE-1`, binds:

| Field | Required contents |
| --- | --- |
| `process` | PID, PPID, kernel boot UUID, `/proc/PID/stat` start ticks, PID namespace inode, parent start ticks, UID, GID, supplementary groups |
| `executable` | Resolved interpreter path, exact binary SHA-256, complete argv |
| `implementation` | Complete selected supervisor/controller implementation path → byte-hash inventory; launch and readiness both verify it |
| `workspace` | Canonical path, device and inode |
| `cgroup` | Canonical delegated path, device/inode, exact `0::` membership, complete cgroup membership text |
| `socket` | Canonical path, filesystem device/inode, UID/GID/mode, listener PID/start ticks, kernel Unix-socket inode |
| `protocol_configuration` | Protocol version, socket/cgroup paths, exact environment and qualified source-bound configuration/constants |
| `host_launch` | Exact private host-launch evidence content ID; binds the root parent/start identity, genuine operator authorization, command hash and placement-before-credential-drop evidence |
| `runtime_binding` | Existing authorization, release and operational-context IDs, continuation-chain digest, profile/execution content digests and the authority-store applicability-epoch digest |

The catalog itself is separately pinned by controller bootstrap and activation
receipts. The instance binds its applicability epoch rather than recursively
containing the hash of a catalog that contains the instance.

PID, PPID and configuration equality never equate two births. Readiness measures
start identity before/after observation; checks source/binary/argv/environment,
workspace/cgroup identity and socket listener ownership; performs the unchanged
legacy scope/readiness checks; then repeats observation and ledger comparison.
The Unix listener is attributed by `/proc/PID/net/unix` and the owning process's
socket FD. No status request or E1 request is sent by this observation.

## Historical S1 evidence

The old release did not capture boot UUID/start ticks. It is impossible to
retroactively issue a truthful complete `SUPERVISOR-INSTANCE-1` for S1. The
candidate therefore uses an explicitly different historical-evidence schema,
`SUPERVISOR-HISTORICAL-INSTANCE-1`, with
`SupervisorHistoricalInstance-sha256:<hash>`. It binds the exact released tuple,
released-profile identities and private release-capture evidence; unknown birth
and launch details remain listed as unknown.

This is an immutable evidence anchor, not a new assertion about S1's birth.
It can be an explicitly authorized succession predecessor; it cannot establish a
live current instance. Seeing PID 57950 again never promotes it to full S1.
Accepting this legacy-anchor rule is part of the proposed material authority
change, not an inferred approval from this qualification.

## SupervisorSuccession

Schema `SUPERVISOR-SUCCESSION-1`; identity
`SupervisorSuccession-sha256:<SHA256(event body)>`.

| Field | Binding |
| --- | --- |
| `sequence`, `predecessor_event` | Exact ordered head and next sequence |
| `predecessor_instance`, `predecessor_status` | Exact S1/Sn identity; UNAVAILABLE, or explicitly authorized FENCED |
| `predecessor_evidence` | Private host observation, time/observation ID, absence or explicit fencing, listener absence, outstanding scopes accounted |
| `successor_instance` | Complete immutable distinct SupervisorInstanceId |
| `reason` | Exact Architect-approved reason |
| `architect_authorization` | Private logical ID of an independently admitted Architect authorization |
| `host_launch` | Exact authenticated launch evidence; must equal the successor's bound evidence |
| `qualification` | PASS capture bound to that exact instance/configuration and operational epoch |
| `runtime_binding` | Current OperationalContextId, chain digest and all related authority/runtime identities |
| `id` | Event fingerprint/identity |

The authorization uses `SUPERVISOR-SUCCESSION-AUTHORIZATION-1`, decision
`AUTHORIZE_SUPERVISOR_SUCCESSION`. Its `event_body_sha256` binds every event field
except the derived event ID and authorization reference (avoids a hash cycle).
The policy admits exact authorization IDs; importing an arbitrary document with
`authority: Architect` does not authorize it.

A live predecessor is rejected unless explicitly authorized and host evidence
establishes that its execution authority is fenced and its old listener cannot
serve. The prepared actual host procedure is narrower: it supports only absent
S1 and refuses any existing supervisor. No live-predecessor fencing operation is
claimed qualified by this package.

## Selection, durability and mutation

`<authorization_id>:supervisor-succession` resolves an immutable policy containing
the historical anchor, exact successor requirements, applicability, admitted
approval IDs, registered ledger role, and expected terminal event ID.
`<authorization_id>:supervisor-succession-events` resolves the private append-only
ledger through the existing store state registry.

Only `append_authorized` mutates the journal. It first takes the existing
invocation fence and ownership-ledger lock and rejects outstanding invocation or
execution ownership. It then takes the succession-ledger lock, reconstructs the
pinned predecessor, verifies the exact approved event, appends/fsyncs it, and
never overwrites/truncates history. A stale competing append fails its head
comparison. Exact replay is non-effecting. Different configuration under an old
ID, corrupt/truncated records, missing events, branch/reorder, stale context and
unknown approval IDs fail closed.

Appending does not select the new head. A separately approved private catalog
must pin it. Between append and catalog selection, the old head is inconsistent
with the journal and readiness blocks. A pinned new head with an absent event
also blocks. A fresh controller reconstructs from private objects plus the
journal; no process-local remembered successor or repository fallback exists.
A current holder is established only when this chain and fresh readiness agree.
No current holder is reported as an explicit denial, never silently replaced.
