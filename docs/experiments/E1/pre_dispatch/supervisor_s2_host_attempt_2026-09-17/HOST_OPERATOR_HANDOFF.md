# Authenticated host-terminal handoff — one attempt only

Jerry's host authorization is recorded as `HostLaunchAuthorization-sha256:9242abecc9896585a6f1fd2a8701be7d7e99716fa6c422bd24153301f5058c25`. Consent is complete; this agent session lacks noninteractive sudo authentication. Its first `sudo -n` prerequisite command failed before any installation or launcher invocation. No candidate attempt has been consumed. Do not share a sudo password with the agent.

Use the already-qualified host terminal and your normal OS authentication. This handoff uses the exact approved package and completed attributable authorization, not an alternate launcher. Stop on any mismatch or command failure; do not rerun the launcher, choose another plan or broaden permissions. If any frozen precondition no longer holds, return the evidence to the Architect.

Review `HOST_AUTHORIZATION_SOURCE.json`, `HOST_OPERATOR_AUTHORIZATION.json`, `HOST_LAUNCH_AUTHORIZATION.json` and `AUTHORIZED_INSTALLATION.json`. The installed authorization hash is `fadb9bfd204efb8fc0f16152dbaed9ff9ac73d6b8064f7224b17ae596fa0caef`. Conditional socket removal is true solely under the frozen procedure's independent stale/safe checks. A live or indeterminate socket must not be deleted.

The following commands are for the human operator's authenticated host terminal. They have not been executed successfully by this agent:

```sh
set -eu
sha256sum --check <<'APPROVED_SOURCE_HASHES'
bf98d94070c5fdcc7861fc6383529f31e8de228571f184342c4cbd414b9be7d6  /home/gvasend/app/kge-forge/docs/experiments/E1/pre_dispatch/supervisor_succession_2026-09-17/host_launch.py
b71bb732ae2206c00911fe50abe4806618ca5709185743c7f9af3a6e2ddc7a43  /home/gvasend/app/kge-forge/docs/experiments/E1/pre_dispatch/supervisor_succession_attempt_2026-09-17/LAUNCH_SPEC.json
fadb9bfd204efb8fc0f16152dbaed9ff9ac73d6b8064f7224b17ae596fa0caef  /home/gvasend/app/kge-forge/docs/experiments/E1/pre_dispatch/supervisor_s2_host_attempt_2026-09-17/HOST_LAUNCH_AUTHORIZATION.json
APPROVED_SOURCE_HASHES
sudo test ! -e /var/lib/kge-forge-supervisor-succession
sudo install -d -o root -g root -m 0700 /var/lib/kge-forge-supervisor-succession
sudo install -d -o root -g root -m 0755 /var/cache/kge-forge-supervisor-succession/S2
sudo install -o root -g root -m 0600 /home/gvasend/app/kge-forge/docs/experiments/E1/pre_dispatch/supervisor_succession_2026-09-17/host_launch.py /var/lib/kge-forge-supervisor-succession/host_launch.py
sudo install -o root -g root -m 0600 /home/gvasend/app/kge-forge/docs/experiments/E1/pre_dispatch/supervisor_succession_attempt_2026-09-17/LAUNCH_SPEC.json /var/lib/kge-forge-supervisor-succession/LAUNCH_SPEC.json
sudo install -o root -g root -m 0600 /home/gvasend/app/kge-forge/docs/experiments/E1/pre_dispatch/supervisor_s2_host_attempt_2026-09-17/HOST_LAUNCH_AUTHORIZATION.json /var/lib/kge-forge-supervisor-succession/HOST_LAUNCH_AUTHORIZATION.json
sudo sha256sum --check <<'APPROVED_INSTALLED_HASHES'
bf98d94070c5fdcc7861fc6383529f31e8de228571f184342c4cbd414b9be7d6  /var/lib/kge-forge-supervisor-succession/host_launch.py
b71bb732ae2206c00911fe50abe4806618ca5709185743c7f9af3a6e2ddc7a43  /var/lib/kge-forge-supervisor-succession/LAUNCH_SPEC.json
fadb9bfd204efb8fc0f16152dbaed9ff9ac73d6b8064f7224b17ae596fa0caef  /var/lib/kge-forge-supervisor-succession/HOST_LAUNCH_AUTHORIZATION.json
APPROVED_INSTALLED_HASHES
sudo stat -c '%n %U:%G %a' /var/lib/kge-forge-supervisor-succession /var/cache/kge-forge-supervisor-succession/S2 /var/lib/kge-forge-supervisor-succession/host_launch.py /var/lib/kge-forge-supervisor-succession/LAUNCH_SPEC.json /var/lib/kge-forge-supervisor-succession/HOST_LAUNCH_AUTHORIZATION.json
sudo /usr/bin/python3.11 /var/lib/kge-forge-supervisor-succession/host_launch.py /var/lib/kge-forge-supervisor-succession/LAUNCH_SPEC.json /var/lib/kge-forge-supervisor-succession/HOST_LAUNCH_AUTHORIZATION.json
```

The checksum expectations above are literal values bound to the reviewed authorization; repository checksum files are documentary copies and are not authority selectors. The final command is the sole authorized launch attempt. The wrapper must independently enforce predecessor absence, no competing supervisor/listener, empty delegated parent and scopes, exact audit/source/interpreter hashes, safe root-owned files/cache, and safe stale-socket conditions. Its root child enters the delegated cgroup before credential drop. No checks may be bypassed.

On success, retain the foreground root parent: it holds the launch lock and the candidate's host-parent identity. Do not close it, restart it or treat the candidate as an accepted supervisor. Preserve its printed candidate identity and the root-owned evidence under `/var/lib/kge-forge-supervisor-succession/S2/`, including `PRELAUNCH.json`, any `STALE_SOCKET_REMOVAL.json`, `PLACEMENT_BEFORE_DROP.json`, `HOST_LAUNCH.json`, `CANDIDATE_S2.json`, and any failure/exit evidence. Return that evidence for independent qualification and specific Architect acceptance. The candidate has no current execution authority merely because it started.

On failure, preserve evidence and return to the Architect without retry or cleanup. No E1 activation, ownership, model request, work execution, dispatch or SupervisorSuccession commit is authorized.
