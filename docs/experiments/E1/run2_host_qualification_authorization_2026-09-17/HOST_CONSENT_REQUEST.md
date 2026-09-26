AWAITING_HOST_AUTHORIZATION

This is a request to Jerry in the human/host-operator role, not a record of consent. The Architect has authorized one conditional candidate attempt: `SupervisorSuccessionAttemptAuthorization-sha256:33b1d5b85a536e28b27c63cbc4a07247be5fbc3d88a9ae78ac550561dabc4e6f`. No privileged operation has been executed. The frozen package is unchanged.

Authorize exactly one installation/start attempt under frozen installation manifest SHA-256 `15c7dbf1a607cc67fec731d854a84078f6cd38699a087d558fe8a1df76489a8b`, launch specification SHA-256 `f9b79b3ac85eb5cbb73d0209cf034c041236dd6519275b6529f139e5b322d309`, and the candidate/runtime bindings in ARCHITECT_ATTEMPT_AUTHORIZATION.json. Do not reuse the consumed Run-1 S2 consent.

Every installed file:

| Source | Destination | Owner / mode | SHA-256 |
|---|---|---|---|
| `/home/gvasend/app/kge-forge/docs/experiments/E1/run2_nonhost_closure_2026-09-17/host_package/host_launch.py` | `/var/lib/kge-forge-supervisor-run2/host_launch.py` | root:root / 0600 | `cfa2c0d945092105556775c75b7fd28b3082463d43c1cda3d38c5ef51553468a` |
| `/home/gvasend/app/kge-forge/docs/experiments/E1/run2_nonhost_closure_2026-09-17/host_package/LAUNCH_SPEC.json` | `/var/lib/kge-forge-supervisor-run2/LAUNCH_SPEC.json` | root:root / 0600 | `f9b79b3ac85eb5cbb73d0209cf034c041236dd6519275b6529f139e5b322d309` |
| `/home/gvasend/app/kge-forge/docs/experiments/E1/run2_nonhost_closure_2026-09-17/host_package/kge-forge-supervisor-run2.service` | `/etc/systemd/system/kge-forge-supervisor-run2.service` | root:root / 0644 | `7e098ea2bcdfaa0229d02d5f9f534bf980b16f292f970d71494595dffba90afe` |
| New HOST_LAUNCH_AUTHORIZATION.json, completed only after genuine consent | `/var/lib/kge-forge-supervisor-run2/HOST_LAUNCH_AUTHORIZATION.json` | root:root / 0600 | Not yet created. Record and verify the exact completed file hash before installation and after installation. |

The pending authorization template is NOT executable authority. After consent, only host_operator_authorization_id (attributable to Jerry’s actual decision) and remove_verified_stale_socket (the explicit choice) are completed. All Architect/package/runtime fields remain exactly fixed. No other package content or launch specification changes are permitted. The finalized receipt and its exact hash will be returned before execution.

Privileged operations requested, exhaustively:

1. Read-only checks of target absence, prior service state, installed hashes, `/proc`, cgroup membership/events, socket/listener, root receipts and journal evidence. Capture the authenticated launching host session/terminal and independent post-closure session; do not retain credentials.
2. Create `/var/lib/kge-forge-supervisor-run2` root:root 0700 and `/var/cache/kge-forge-supervisor-run2/S3` root:root 0755, empty. Ordinary missing intermediate cache directories may be created by install -d; no existing file/directory is overwritten or repurposed. Abort on any pre-existing target package, service/unit or S3 cache/evidence.
3. Install the four files listed above at their exact destinations/owners/modes. Verify all sources before mutation and all installed hashes before start.
4. `sudo /bin/systemctl daemon-reload` to discover the exact unit; then **one** `sudo /bin/systemctl start kge-forge-supervisor-run2.service`. No enable, restart, second start, alternate launcher, transient service or fallback path.
5. The frozen service launches a root parent that creates/holds its exclusive host-launch.lock, performs preflight, creates root-owned 0700 S3 evidence directory and 0600 durable receipts under `/var/lib/kge-forge-supervisor-run2/S3`, and forks one child. The child writes its own PID to `/sys/fs/cgroup/unified/kge-forge/executor/cgroup.procs` while root, verifies `0::/kge-forge/executor`, then drops supplementary groups to [], GID to 1000 and UID to 1000 before exec. No migration from user.slice after unprivileged startup.
6. The candidate binds `/tmp/a21m.sock`, owner 1000:1000 mode0600, and uses the existing supervisor audit at `/tmp/a21m.sock.supervisor-audit.jsonl` under frozen protocol semantics. Its runtime workspace is `/home/gvasend/app/kge-forge`; interpreter `/usr/bin/python3.11`; argv `/usr/bin/python -m adapter.supervisor_server /tmp/a21m.sock`. The root parent remains managed by systemd, waiting for the child while retaining launch provenance and lock. Journal output and durable launch/exit receipts are preserved.

Conditional stale-socket permission requested: remove `/tmp/a21m.sock` only through the frozen launcher after successful preflight: historical PIDs absent, no competing supervisor/listener, delegated scopes empty/unpopulated, exact prelaunch audit hash and implementation/interpreter identities, and verified UID-1000 socket with no listener. The launcher records device/inode/owner/mode before unlinking and rechecks absence/listeners before launch. No deletion of a live, indeterminate, symlink or otherwise unattributable socket; no manual rm; no other cleanup. Jerry may decline this permission, in which case an existing socket blocks launch.

Exact service definition:

```ini
[Unit]
Description=One authorized E1 successor candidate; no automatic retry
After=local-fs.target

[Service]
Type=simple
User=root
Group=root
ExecStart=/usr/bin/python3.11 /var/lib/kge-forge-supervisor-run2/host_launch.py /var/lib/kge-forge-supervisor-run2/LAUNCH_SPEC.json /var/lib/kge-forge-supervisor-run2/HOST_LAUNCH_AUTHORIZATION.json
Restart=no
RemainAfterExit=no
StandardInput=null
StandardOutput=journal
StandardError=journal
UMask=0077
# The launcher moves only the child into the existing delegated executor before
# credential drop. The root parent remains managed here and retains its lock.
KillMode=control-group
TimeoutStopSec=15s
```

The unit’s exact root ExecStart is `/usr/bin/python3.11 /var/lib/kge-forge-supervisor-run2/host_launch.py /var/lib/kge-forge-supervisor-run2/LAUNCH_SPEC.json /var/lib/kge-forge-supervisor-run2/HOST_LAUNCH_AUTHORIZATION.json`. Do not invoke it from the interactive shell: the launcher requires the qualified system-service lifetime (PPID 1, independent session/no TTY, exact unit, no drop-ins, root identity, InvocationID and Restart=no).

Stop/rollback behavior: set -euo pipefail stops the handoff at the first failed prerequisite or command. No automatic retry or rollback, no deletion of evidence/socket/cache, and no automatic process kill are authorized. Preserve partial installation and reconcile before any further action. Restart=no prevents service-manager retry. A failed launcher or successful systemctl start is not proof of candidate death/readiness. The child is in a separate delegated cgroup: `systemctl stop` on the root parent alone is NOT an authoritative QUIESCENT proof and is not included in this request. If a candidate exists after failure, stop qualification and request exact governed/host reconciliation; never relaunch.

Durability procedure: capture genuine launch receipts, same-instance birth identity, socket/listener, read-only READY and exclusivity before closure. Record the launching authenticated session/TTY, close it normally, then use a new independent authenticated session to reobserve the same PID/start ticks/boot/namespace/parent identity and recompute the same SupervisorInstanceId. Recheck socket, protocol readiness, cgroup, implementation, workspace and configuration. Preserve attributable before/after evidence and perform only non-effecting production timing validation. Session closure must never trigger a relaunch. No ExecutionScope or work-package action is authorized.

Attempt limit: ONE start/candidate attempt total. A launch, placement, credential, evidence or terminal-durability failure ends the attempt; no reset/removal of the exclusive attempt record. A pre-installation verification failure leaves no launch consumed but still stops this handoff for review.

Suggested consent (not already given): “I, Jerry, authorize the exact privileged operations in this HOST_CONSENT_REQUEST.md, bound to installation manifest SHA-256 15c7dbf1a607cc67fec731d854a84078f6cd38699a087d558fe8a1df76489a8b and launch-spec SHA-256 f9b79b3ac85eb5cbb73d0209cf034c041236dd6519275b6529f139e5b322d309, for one candidate attempt only. I authorize removal of the existing socket only under the frozen conditional stale-socket rule. I do not authorize a live/indeterminate socket deletion, alternate package, retry, release application, succession application, Run-2 activation/ownership/model request or dispatch.”

Exact handoff script SHA-256: `57f4a1f3e8eb70eb8d4511f8b7ace609d51518dadd9f614c40b0d8e5fb63a36a`. Its commands are supplied in HOST_OPERATOR_HANDOFF.sh; do not execute until the separately attributable host decision and completed authorization-file hash have been reviewed.
