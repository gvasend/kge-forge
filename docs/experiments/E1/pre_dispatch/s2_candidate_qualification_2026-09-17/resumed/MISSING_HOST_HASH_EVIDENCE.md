# Missing host evidence capture

The receipt copies pass content/schema/hash-linkage checks and match fresh live observations. To complete the requested original/copy provenance verification, the host operator must supply the existing SHA-256 capture (preferred), or capture these read-only hashes. This procedure performs no launch, installation, permission change, socket operation, or authority mutation.

```bash
sudo /usr/bin/sha256sum \
  /var/lib/kge-forge-supervisor-succession/S2/CANDIDATE_S2.json \
  /var/lib/kge-forge-supervisor-succession/S2/HOST_LAUNCH.json \
  /var/lib/kge-forge-supervisor-succession/S2/PLACEMENT_BEFORE_DROP.json \
  /var/lib/kge-forge-supervisor-succession/S2/PRELAUNCH.json \
  /var/lib/kge-forge-supervisor-succession/S2/STALE_SOCKET_REMOVAL.json \
  /var/lib/kge-forge-supervisor-succession/host_launch.py \
  /var/lib/kge-forge-supervisor-succession/LAUNCH_SPEC.json \
  /var/lib/kge-forge-supervisor-succession/HOST_LAUNCH_AUTHORIZATION.json
/usr/bin/sha256sum \
  /tmp/kge-forge-s2-verification/CANDIDATE_S2.json \
  /tmp/kge-forge-s2-verification/HOST_LAUNCH.json \
  /tmp/kge-forge-s2-verification/PLACEMENT_BEFORE_DROP.json \
  /tmp/kge-forge-s2-verification/PRELAUNCH.json \
  /tmp/kge-forge-s2-verification/STALE_SOCKET_REMOVAL.json
```

Return the attributable captured output. Do not relaunch S2 or change access permissions to the original evidence.
