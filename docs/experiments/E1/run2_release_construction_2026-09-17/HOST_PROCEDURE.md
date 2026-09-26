# Proposed durable host lifetime — NOT AUTHORIZED FOR EXECUTION

The old one-attempt consent was consumed by S2. It does not authorize this package.
S2 remains the historical predecessor of any S3 candidate. Do not recreate S2,
change its birth observations, delete its receipts, or reuse its consent.

The proposed root system service owns the launcher lifetime, with Restart=no,
no terminal input, and journal output. There is no Install section, boot enablement,
Restart=always, user service, SSH dependency, or unprivileged cgroup migration.
The unchanged child-placement sequence writes the child into the existing
executor cgroup as root, records that placement, then drops groups/GID/UID.
The parent remains in the system-service cgroup and retains the exclusive lock.
The existing exclusive evidence-directory creation prevents launch replay.

Before installation, the Architect must accept the exact completed release,
implementation and launch package and authorize one candidate attempt. Jerry must
separately authorize installation and system-service start against those exact
hashes. The proposed launch specification deliberately contains unresolved
runtime bindings and an absent recovery-audit observation. It is not executable
launch authority. No host authorization file has been fabricated.

After those prerequisites, freeze LAUNCH_SPEC.json and attributable
HOST_LAUNCH_AUTHORIZATION.json. Independently check S1/S2 unavailability, all
supervisor processes/listeners, current release/dispatch ancestry, empty delegated
execution scopes, and the fresh recovery-audit hash. Any mismatch stops the handoff.

The proposed installation scope, after exact byte approval, is:

* root-owned /var/lib/kge-forge-supervisor-run2, mode 0700;
* host_launch.py, LAUNCH_SPEC.json, HOST_LAUNCH_AUTHORIZATION.json there, root:root 0600;
* root-owned empty /var/cache/kge-forge-supervisor-run2/S3, mode 0755;
* /etc/systemd/system/kge-forge-supervisor-run2.service, root:root 0644.

Verify source hashes before mutation and installed hashes before start. Then the
specific privileged manager commands would be `sudo /bin/systemctl daemon-reload`
and `sudo /bin/systemctl start kge-forge-supervisor-run2.service`. These commands
have not been executed or authorized here. Do not enable the unit at boot.

The unit invokes:

```
/usr/bin/python3.11 /var/lib/kge-forge-supervisor-run2/host_launch.py /var/lib/kge-forge-supervisor-run2/LAUNCH_SPEC.json /var/lib/kge-forge-supervisor-run2/HOST_LAUNCH_AUTHORIZATION.json
```

Conditional stale-socket removal retains the old launcher checks and separately
requires remove_verified_stale_socket=true from the new host authorization.
Existence of the old socket alone is not sufficient permission or evidence.

Immediately capture PRELAUNCH, PLACEMENT_BEFORE_DROP, optional
STALE_SOCKET_REMOVAL, HOST_LAUNCH and CANDIDATE_S3 receipts; independently observe
all modern SupervisorInstance fields. Host-lifetime provenance additionally binds
the exact unit hash, system-manager parent, service invocation ID, service
properties, session identity and absence of a controlling terminal.

Close the operator terminal/session. From an independently opened host session,
re-observe the same candidate birth identity, launcher parent, service state,
cgroup, socket/listener and bounded protocol readiness. Record both observations
with attributable host timestamps and hashes. Neither a running service nor
configuration equality grants succession authority. Return the observed S3 and
exact S2→S3 event to the Architect for a separate specific succession decision.

Service stop is not a qualified execution reconciliation mechanism: the payload
supervisor is deliberately in the delegated executor cgroup. Unexpected service
failure must leave readiness unresolved, preserve evidence, and use existing
governed interruption/recovery. No automatic restart or second attempt.
