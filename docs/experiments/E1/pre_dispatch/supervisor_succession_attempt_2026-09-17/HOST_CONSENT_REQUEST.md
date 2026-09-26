# Separate human/host authorization required — not issued

The Architect has authorized one candidate-S2 attempt, conditional on genuine human/host consent. This document requests that consent; it does not record Jerry as having given it.

The reviewable launch specification is [LAUNCH_SPEC.json](LAUNCH_SPEC.json), SHA-256 `b71bb732ae2206c00911fe50abe4806618ca5709185743c7f9af3a6e2ddc7a43`.

Frozen launcher SHA-256: `bf98d94070c5fdcc7861fc6383529f31e8de228571f184342c4cbd414b9be7d6`.

Architect attempt identity: `SupervisorSuccessionAttemptAuthorization-sha256:843b06e105f701081bc7720fda792f2c482c1c09bdac77c0932b6a4c1442a64e`.

The plan differs from the frozen proposal only in the two finalization fields prescribed by the approved procedure: `status=AUTHORIZED_FOR_HOST_LAUNCH` and `prelaunch_supervisor_audit_sha256=0e61d05208459051bda9772783ebded01067caa131e7253371805c42c3d040b7`. The audit hash is an actual unprivileged read, not a host observation attestation. The human operator must independently verify it and all host prerequisites before privileged launch. Any mismatch stops this attempt's preparation; do not silently choose another plan/hash.

Jerry must explicitly authorize, in the human/host-operator role:

1. Root-owned staging and installation of the exact qualified launcher, this exact plan, and an authorization file completed solely with the genuine host authorization identity and the explicitly chosen stale-socket permission. The final authorization file hash must then be recorded and checked before execution. The pending template is not valid host authority.
2. Read-only host prerequisite checks: historical predecessor absence, no competing supervisor/listener, correct delegated subtree and no unaccounted scopes, exact recovery audit, implementation and interpreter identities, and required root-owned empty cache.
3. One execution, with no automatic retry, of:

```sh
sudo /usr/bin/python3.11 /var/lib/kge-forge-supervisor-succession/host_launch.py /var/lib/kge-forge-supervisor-succession/LAUNCH_SPEC.json /var/lib/kge-forge-supervisor-succession/HOST_LAUNCH_AUTHORIZATION.json
```

4. The qualified root-child cgroup placement before dropping to UID/GID 1000:1000 with no supplementary groups, followed by genuine host evidence capture.
5. An explicit choice concerning `/tmp/a21m.sock`: authorize its removal **only** if the frozen root procedure proves it is the UID-1000 socket with no listener and passes the other preflight checks, or leave removal unauthorized. It currently exists in the unprivileged observation. Existing permission remains false; its presence is not proof of staleness. No other deletion or cleanup is requested.

Bind consent to the launcher and plan hashes above, the Architect attempt identity, historical S1 `SupervisorHistoricalInstance-sha256:8ffe7a419d3953ed54fb1a73a9bd1d793cbe2c540c181cee9c0ca4e30987d572`, and the complete runtime binding in the plan, including OperationalContextId `E1-OPERATIONAL-CONTEXT-sha256:3672ba1076042f90563116c57a0e002beb19f03f164c4dfabc71fe721ac72453` and chain `2193231e010af1189bd90e5519bfc1232f84e0de8dfc9fd6ed5d377616f83515`.

The exact source/destination/owner/mode requirements are in [INSTALLATION_MANIFEST.json](INSTALLATION_MANIFEST.json). Installation follows the frozen [HOST_INSTALLATION_PROCEDURE.md](../pd06_supervisor_amendment_publication_2026-09-17_final/HOST_INSTALLATION_PROCEDURE.md), with this finalized plan as the reviewed source for `/root/approved-supervisor-succession/LAUNCH_SPEC.json`.

No candidate gains supervisor authority by launching. Any failure stops without retry and preserves evidence. No SupervisorSuccession commit, E1 activation, ownership acquisition, model request, work execution or dispatch is covered by this host consent request.
