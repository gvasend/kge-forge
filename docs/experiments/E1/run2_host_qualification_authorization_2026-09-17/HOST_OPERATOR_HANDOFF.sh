#!/bin/bash
# REVIEW ONLY UNTIL JERRY APPROVES HOST_CONSENT_REQUEST.md.
# Arguments: exact finalized authorization file, its independently reviewed SHA-256.
# No retry, restart, cleanup or alternate path.
set -euo pipefail
[[ $# -eq 2 ]] || { echo 'Require finalized authorization file and reviewed SHA-256' >&2; exit 2; }
s2_host_auth_file=$1
s2_host_auth_sha=$2
[[ "$s2_host_auth_file" = /* && -f "$s2_host_auth_file" && ! -L "$s2_host_auth_file" ]]
[[ "$s2_host_auth_sha" =~ ^[0-9a-f]{64}$ ]]
printf '%s  %s\n' "$s2_host_auth_sha" "$s2_host_auth_file" | sha256sum --check --strict -
sha256sum --check --strict <<'FROZEN_SOURCES'
cfa2c0d945092105556775c75b7fd28b3082463d43c1cda3d38c5ef51553468a  /home/gvasend/app/kge-forge/docs/experiments/E1/run2_nonhost_closure_2026-09-17/host_package/host_launch.py
f9b79b3ac85eb5cbb73d0209cf034c041236dd6519275b6529f139e5b322d309  /home/gvasend/app/kge-forge/docs/experiments/E1/run2_nonhost_closure_2026-09-17/host_package/LAUNCH_SPEC.json
7e098ea2bcdfaa0229d02d5f9f534bf980b16f292f970d71494595dffba90afe  /home/gvasend/app/kge-forge/docs/experiments/E1/run2_nonhost_closure_2026-09-17/host_package/kge-forge-supervisor-run2.service
15c7dbf1a607cc67fec731d854a84078f6cd38699a087d558fe8a1df76489a8b  /home/gvasend/app/kge-forge/docs/experiments/E1/run2_nonhost_closure_2026-09-17/HOST_INSTALLATION_MANIFEST.json
e669add322aaa0b39df973c48a8938deef784354669a52d848cb34bf3093578a  /home/gvasend/app/kge-forge/docs/experiments/E1/run2_host_qualification_authorization_2026-09-17/HOST_LAUNCH_AUTHORIZATION.PENDING.json
63374c630fe4ed088f1951bee3e0a4c0140beab5dc9bc3163ed47cd1e34ed423  /home/gvasend/app/kge-forge/docs/experiments/E1/run2_host_qualification_authorization_2026-09-17/ARCHITECT_ATTEMPT_AUTHORIZATION.json
12d7cef0067b0d99f69573c5030d7319bbfb08aec0a07f44551364da5d889210  /home/gvasend/app/kge-forge/docs/experiments/E1/run2_host_qualification_authorization_2026-09-17/ARCHITECT_QUALIFICATION_ACCEPTANCE.json
FROZEN_SOURCES
/usr/bin/python3.8 - "$s2_host_auth_file" <<'VERIFY_AUTH'
import json,sys,hashlib
from pathlib import Path
expected=json.loads(Path('/home/gvasend/app/kge-forge/docs/experiments/E1/run2_host_qualification_authorization_2026-09-17/HOST_LAUNCH_AUTHORIZATION.PENDING.json').read_bytes())
actual=json.loads(Path(sys.argv[1]).read_bytes())
assert set(actual)==set(expected), 'Unexpected authorization fields'
for key,value in expected.items():
    if key not in ('host_operator_authorization_id','remove_verified_stale_socket'):
        assert actual[key]==value, 'Authorization/package binding changed: '+key
assert isinstance(actual['host_operator_authorization_id'],str) and actual['host_operator_authorization_id'].strip(), 'Genuine host authorization not supplied'
assert type(actual['remove_verified_stale_socket']) is bool, 'Explicit socket choice required'
plan=json.loads(Path('/home/gvasend/app/kge-forge/docs/experiments/E1/run2_nonhost_closure_2026-09-17/host_package/LAUNCH_SPEC.json').read_bytes())
for path,wanted in plan['implementation'].items():
    assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==wanted, 'Implementation changed: '+path
assert hashlib.sha256(Path(plan['interpreter']).read_bytes()).hexdigest()==plan['interpreter_sha256'], 'Interpreter changed'
VERIFY_AUTH
# Read-only target/service checks before privileged mutation. No overwrite/resume.
[[ "$(/bin/systemctl show kge-forge-supervisor-run2.service --property=LoadState --value)" = not-found ]]
sudo test ! -e /var/lib/kge-forge-supervisor-run2
sudo test ! -L /var/lib/kge-forge-supervisor-run2
sudo test ! -e /var/cache/kge-forge-supervisor-run2/S3
sudo test ! -L /var/cache/kge-forge-supervisor-run2/S3
sudo test ! -e /etc/systemd/system/kge-forge-supervisor-run2.service
sudo test ! -L /etc/systemd/system/kge-forge-supervisor-run2.service
sudo install -d -o root -g root -m 0700 /var/lib/kge-forge-supervisor-run2
sudo install -d -o root -g root -m 0755 /var/cache/kge-forge-supervisor-run2/S3
sudo install -o root -g root -m 0600 /home/gvasend/app/kge-forge/docs/experiments/E1/run2_nonhost_closure_2026-09-17/host_package/host_launch.py /var/lib/kge-forge-supervisor-run2/host_launch.py
sudo install -o root -g root -m 0600 /home/gvasend/app/kge-forge/docs/experiments/E1/run2_nonhost_closure_2026-09-17/host_package/LAUNCH_SPEC.json /var/lib/kge-forge-supervisor-run2/LAUNCH_SPEC.json
sudo install -o root -g root -m 0644 /home/gvasend/app/kge-forge/docs/experiments/E1/run2_nonhost_closure_2026-09-17/host_package/kge-forge-supervisor-run2.service /etc/systemd/system/kge-forge-supervisor-run2.service
sudo install -o root -g root -m 0600 "$s2_host_auth_file" /var/lib/kge-forge-supervisor-run2/HOST_LAUNCH_AUTHORIZATION.json
sudo sha256sum --check --strict <<'FROZEN_INSTALLED'
cfa2c0d945092105556775c75b7fd28b3082463d43c1cda3d38c5ef51553468a  /var/lib/kge-forge-supervisor-run2/host_launch.py
f9b79b3ac85eb5cbb73d0209cf034c041236dd6519275b6529f139e5b322d309  /var/lib/kge-forge-supervisor-run2/LAUNCH_SPEC.json
7e098ea2bcdfaa0229d02d5f9f534bf980b16f292f970d71494595dffba90afe  /etc/systemd/system/kge-forge-supervisor-run2.service
FROZEN_INSTALLED
printf '%s  %s\n' "$s2_host_auth_sha" /var/lib/kge-forge-supervisor-run2/HOST_LAUNCH_AUTHORIZATION.json | sudo sha256sum --check --strict -
sudo /bin/systemctl daemon-reload
sudo /bin/systemctl start kge-forge-supervisor-run2.service
# No second start. Successful command return is NOT candidate qualification.
