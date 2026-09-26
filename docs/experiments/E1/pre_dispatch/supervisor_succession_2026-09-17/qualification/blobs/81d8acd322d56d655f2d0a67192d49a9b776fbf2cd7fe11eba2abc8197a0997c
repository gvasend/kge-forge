# Proposed host-only S2 procedure — NOT EXECUTED / NOT AUTHORIZED

This procedure is for the human host operator after the Architect resolves the
material implementation applicability, accepts the legacy S1 evidence-anchor
rule, and grants genuine host-launch authority. It is not a command for the
Forge governed environment. The current `PROPOSED_HOST_LAUNCH_SPEC.json` is
intentionally not executable authority: its status is PROPOSED_NOT_AUTHORIZED
and its fresh prelaunch audit hash is null.

The previously qualified boundary is the external supervisor running as
1000:1000 in `0::/kge-forge/executor`, serving `/tmp/a21m.sock`, with governed
children admitted before their start barriers open. The A2 live readiness and
PD05 receipts establish that boundary. The historical failed unprivileged
migration is recorded in `A2_1C_LIFECYCLE_QUALIFICATION_2026-09-15.md`. The new
procedure uses a root child for cgroup placement and drops credentials only
after verifying placement. It does not attempt post-start migration from
`user.slice`, enlarge delegation, recreate cgroups, or change their permissions.
The original root launch command is not in S1's available receipts; this exact
wrapper is a new proposed host procedure, not claimed to be that old command.

## Required authority and preparation

1. Approve the candidate's material authority change through an appropriate
   release/applicability decision. Do not issue a non-material continuation to
   conceal that change. Deploy only the resulting exact qualified implementation.
2. From the host authority boundary, reconcile PID 57950, all supervisor module
   processes, the Unix listener, executor-parent members, every existing scope's
   recursive membership/population, and the preserved supervisor recovery audit.
   No active or uncertain old work may be cleared by this procedure. Capture the
   fresh audit SHA-256 and root observation provenance for Architect review.
3. Produce the final `LAUNCH_SPEC.json` from the proposal, with status
   `AUTHORIZED_FOR_HOST_LAUNCH`, the genuine effective runtime-binding identities,
   and fresh `prelaunch_supervisor_audit_sha256`. If applicability or any qualified
   implementation/configuration changes, requalify and repin the plan before use.
4. Obtain the genuine `HOST_LAUNCH_AUTHORIZATION.json`, with:
   `authority: Architect`, `decision: AUTHORIZE_HOST_SUPERVISOR_LAUNCH`, real
   `authorization_id`, real `host_operator_authorization_id`, exact final
   `launch_spec_sha256`, exact `launcher_sha256`, `predecessor_id`,
   `runtime_binding`, and `qualification_acceptance_id`. If a stale socket must
   be removed, authorization must explicitly set `remove_verified_stale_socket`
   to true. No sample approval or fabricated authorization is supplied here.
5. The human operator stages these externally approved files under
   `/root/approved-supervisor-succession/`. Their authenticity is established by
   that host/Architect channel, not by an editable repository copy.

## Exact commands for the human host operator

After the prerequisites above, execute these in a dedicated host terminal.
Do not execute them during this qualification:

```sh
sudo install -d -o root -g root -m 0700 /var/lib/kge-forge-supervisor-succession
sudo install -d -o root -g root -m 0755 /var/cache/kge-forge-supervisor-succession/S2
sudo install -o root -g root -m 0600 /home/gvasend/app/kge-forge/docs/experiments/E1/pre_dispatch/supervisor_succession_2026-09-17/host_launch.py /var/lib/kge-forge-supervisor-succession/host_launch.py
sudo install -o root -g root -m 0600 /root/approved-supervisor-succession/LAUNCH_SPEC.json /var/lib/kge-forge-supervisor-succession/LAUNCH_SPEC.json
sudo install -o root -g root -m 0600 /root/approved-supervisor-succession/HOST_LAUNCH_AUTHORIZATION.json /var/lib/kge-forge-supervisor-succession/HOST_LAUNCH_AUTHORIZATION.json
sudo /usr/bin/python3.11 /var/lib/kge-forge-supervisor-succession/host_launch.py /var/lib/kge-forge-supervisor-succession/LAUNCH_SPEC.json /var/lib/kge-forge-supervisor-succession/HOST_LAUNCH_AUTHORIZATION.json
```

The wrapper checks its own exact hash against the genuine authorization before
launch. The approved launcher hash is also recorded in the proposal and closure.
The cache prefix must be newly provisioned and empty of bytecode. Root ownership
prevents the runtime UID from planting bytecode; `PYTHONDONTWRITEBYTECODE=1`
prevents cache writes. The supervisor receives only the exact environment in the
approved spec, with no model credentials or inherited caller environment.

The wrapper locks a root-owned singleton launch file, refuses existing supervisor
processes/listeners or unresolved cgroups, checks all source/interpreter hashes,
and creates an exclusive S2 evidence directory. It records any explicitly
authorized removal of a verified stale socket. A forked root child writes its
own PID to `/sys/fs/cgroup/unified/kge-forge/executor/cgroup.procs`, verifies
`0::/kge-forge/executor`, emits its pre-drop receipt, clears supplementary groups,
sets GID 1000, sets UID 1000, and execs the exact interpreter/argv. It never
requests privileged cgroup migration after becoming unprivileged.

The root parent stays alive, holds the singleton launch lock, and waits for the
child. Keep that host terminal/session alive: its PID/start relationship is part
of the evidence. The wrapper never starts Forge, a model request, E1 activation,
or a succession append. Failure after child creation requires explicit host
reconciliation; do not blindly rerun, remove the lock/evidence, or treat a partial
receipt as readiness. It does not automatically kill a candidate process.

## Immediate post-launch evidence

The wrapper writes exclusive root-owned files under
`/var/lib/kge-forge-supervisor-succession/S2/`:

- `PRELAUNCH.json`: authorization/spec hashes, parent birth identity, exact
  supervisor-audit hash and empty/populated-zero scope observations.
- `PLACEMENT_BEFORE_DROP.json`: child PID, root UID and verified delegated
  membership before credential reduction.
- `HOST_LAUNCH.json`: genuine authorization identities, command/launcher/spec
  hashes, complete child and parent birth identity, UID/GID/groups, interpreter
  path/hash/argv, complete implementation inventory, workspace path/device/inode,
  full cgroup membership including `0::`, delegated directory identity, socket
  path/device/inode/UID/GID/mode, listener PID/start ticks and Unix-socket inode,
  full protocol/configuration/environment identity, observation Unix time,
  kernel boot time and clock-tick rate for translating process-start ticks.
- `CANDIDATE_S2.json`: immutable full instance body and derived
  `SupervisorInstance-sha256:<canonical body hash>`.
- `PROCESS_EXIT.json`, if it later exits: exit observation, never a succession
  approval or clean-work completion claim.

Forge must independently repeat the candidate's measurements immediately,
including `/proc/PID/stat`, boot ID, PID namespace, parent start, all UID/GID
columns/groups, `/proc/PID/exe` bytes, cmdline/environment/cwd, implementation
bytes, cgroup membership, socket lstat, `/proc/PID/net/unix` listener and its FD
ownership. Birth is read before and after. A mismatch blocks qualification.
Do not derive the candidate from guessed PID, merely equal configuration, or a
`READY` string. Do not substitute the candidate for S1.

Import approved immutable representations through the private-store materializer
with original root receipt hashes/provenance. Capture fresh successor protocol,
owner-bound admission, recovery, and authoritative QUIESCENT qualification using
separately authorized non-E1 fixtures; no E1 activation is implied. Produce the
exact succession body and obtain the Architect's authorization bound to its
hash and observed S2 ID. Then use the typed append operation and separately
approved catalog-head selection. A successful new process alone remains a
candidate and has no current execution-authority role.

The post-launch S2 identity and exact event authorization cannot be supplied
before the process exists. `PROPOSED_S1_TO_S2.json` therefore leaves them null,
explicitly invalid for the event verifier. No real succession journal was
created or appended in this qualification.
