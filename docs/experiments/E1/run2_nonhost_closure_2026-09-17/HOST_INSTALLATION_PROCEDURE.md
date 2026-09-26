Host procedure for review only. Do not execute before new separate approvals. No enable, restart, fallback, manual launcher invocation, or second attempt. A pre-existing or uncertain state stops the procedure.

```bash
set -euo pipefail
# Only after the exact new package and authorization-file digest receive separate Architect and Jerry approval.
sha256sum --check <<'FROZEN_SOURCES'
cfa2c0d945092105556775c75b7fd28b3082463d43c1cda3d38c5ef51553468a  /home/gvasend/app/kge-forge/docs/experiments/E1/run2_nonhost_closure_2026-09-17/host_package/host_launch.py
f9b79b3ac85eb5cbb73d0209cf034c041236dd6519275b6529f139e5b322d309  /home/gvasend/app/kge-forge/docs/experiments/E1/run2_nonhost_closure_2026-09-17/host_package/LAUNCH_SPEC.json
7e098ea2bcdfaa0229d02d5f9f534bf980b16f292f970d71494595dffba90afe  /home/gvasend/app/kge-forge/docs/experiments/E1/run2_nonhost_closure_2026-09-17/host_package/kge-forge-supervisor-run2.service
FROZEN_SOURCES
# Verify the separately issued authorization file and its approved SHA-256 before ANY privileged mutation.
# Abort if the service, launch lock, S3 evidence directory, or package is already installed; reconcile; never retry or overwrite an attempt.
sudo install -d -o root -g root -m 0700 /var/lib/kge-forge-supervisor-run2
sudo install -d -o root -g root -m 0755 /var/cache/kge-forge-supervisor-run2/S3
sudo install -o root -g root -m 0600 /home/gvasend/app/kge-forge/docs/experiments/E1/run2_nonhost_closure_2026-09-17/host_package/host_launch.py /var/lib/kge-forge-supervisor-run2/host_launch.py
sudo install -o root -g root -m 0600 /home/gvasend/app/kge-forge/docs/experiments/E1/run2_nonhost_closure_2026-09-17/host_package/LAUNCH_SPEC.json /var/lib/kge-forge-supervisor-run2/LAUNCH_SPEC.json
sudo install -o root -g root -m 0644 /home/gvasend/app/kge-forge/docs/experiments/E1/run2_nonhost_closure_2026-09-17/host_package/kge-forge-supervisor-run2.service /etc/systemd/system/kge-forge-supervisor-run2.service
# Install the separately approved authorization file root:root 0600 at /var/lib/kge-forge-supervisor-run2/HOST_LAUNCH_AUTHORIZATION.json.
# Its source path/hash cannot be fabricated before the new decisions. Verify that approved installed hash separately.
sudo sha256sum --check <<'FROZEN_INSTALLED'
cfa2c0d945092105556775c75b7fd28b3082463d43c1cda3d38c5ef51553468a  /var/lib/kge-forge-supervisor-run2/host_launch.py
f9b79b3ac85eb5cbb73d0209cf034c041236dd6519275b6529f139e5b322d309  /var/lib/kge-forge-supervisor-run2/LAUNCH_SPEC.json
7e098ea2bcdfaa0229d02d5f9f534bf980b16f292f970d71494595dffba90afe  /etc/systemd/system/kge-forge-supervisor-run2.service
FROZEN_INSTALLED
sudo /bin/systemctl daemon-reload
sudo /bin/systemctl start kge-forge-supervisor-run2.service
```

The unit invokes `/usr/bin/python3.11 /var/lib/kge-forge-supervisor-run2/host_launch.py /var/lib/kge-forge-supervisor-run2/LAUNCH_SPEC.json /var/lib/kge-forge-supervisor-run2/HOST_LAUNCH_AUTHORIZATION.json` under root system service authority. The launcher checks the independent service lifetime and exclusive state, then places the child in the delegated cgroup before credential drop. Only its qualified conditional rule may remove an explicitly authorized stale socket; a live/indeterminate socket stops launch. No host operations were executed during this qualification.
