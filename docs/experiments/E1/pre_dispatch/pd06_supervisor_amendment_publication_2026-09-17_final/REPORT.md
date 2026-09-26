# PD-06 Supervisor Authority Amendment — publication and production consumption

**PUBLISHED; production decision-consumption qualification PASS; independent private restart reconstruction PASS. E1 remains INACTIVE with NO OWNERSHIP. E1-WP-001 remains INELIGIBLE and UNDISPATCHED. S2 is unlaunched.**

## Applied authority

- Applied amendment: `PD06-SUPERVISOR-AUTHORITY-AMENDMENT-sha256:979201e9e2d4269a483ce904ae4e7f9329ab0378836e7ada59070b3e4636d3b6`.
- Exact authorized candidate-file SHA-256: `5a73a14859ddf63a733fcc1941a0a744f9c399863ef7eaf8f6889c4e769d0eae`.
- Resulting release authority: `E1-RELEASE-AUTHORITY-sha256:c0d6aed0894c9d07945b017423b3bb2fedb7207780b5e3d4e6c928aacb82bae3`.
- Separate append-only release decision: `PD06-SUPERVISOR-AMENDMENT-DECISION-sha256:8d55cc3780e48283ad0335640b237f0778ccdf7165439bfc83110aaac6dd4fb4`.
- Dispatch amendment: `ARCHITECT-DISPATCH-AMENDMENT-sha256:3f29a0c359e626b5fe532af6c9fd06218d33bb9644a4906a2214dbf655d67a31`.
- Dispatch amendment file SHA-256: `6b722b7a9713ebfa4b5364cc7aec55350f1f0d6ca6c2f13fcc22ee6beb2da8bd`.
- Accepted frozen succession implementation: `sha256:a90b06ddeaf9d2ba58cfd5ce3807f4e5a529aac8e720a63c1e1800e11e345aa0`.
- Qualified production-consumption implementation: `sha256:ffe10dbfa8efdf7a668489fb14d0310631a81324697e34ca8f4375d96f15d62f`.

The release rule is: **The Execution Supervisor authority holder is historical S1, or exactly one explicitly Architect-authorized, qualified successor selected through authenticated SupervisorSuccession. Missing evidence establishes no ready holder.** The exact fourteen conditions remain in the authorized immutable candidate. Configuration equality is insufficient. Historical S1 remains `SupervisorHistoricalInstance-sha256:8ffe7a419d3953ed54fb1a73a9bd1d793cbe2c540c181cee9c0ca4e30987d572`; missing historical boot/start observations were not manufactured.

The original PD-06 decision, E1-B01 PASS, ReleaseBasisId, ReleaseDecisionId, original dispatch authorization `auth-e1-wp-001-r7-94f511dfcdcc43ac837191f8732ced39`, task, profile, payload and grants remain unchanged. All 716 historical reference fingerprints were rechecked without rewriting them. Profile bytes remain `a0547c7c33b95628d9419a62972f15062bd6fa8ab9236496ceb7d6ab21fbab75`; canonical profile fingerprint remains `b9e7f72d97525f39fbddfe92f276ab6aedd057ef6c5b7284dc163f1db9c9c328`.

No Programmer tool, read/write grant, execution or QUIESCENT rule, sequential execution, ownership mechanism, transmission/destination policy, snapshot/evidence isolation or host authority boundary was expanded. The exact production delta is in `IMPLEMENTATION_DELTA.json`. Material implementation is bound directly through a material release application, not mislabeled as OPERATIONAL-CONTINUATION-1.

## Current operational ancestry

| Identity | Value |
| --- | --- |
| OperationalContextId | `E1-OPERATIONAL-CONTEXT-sha256:3672ba1076042f90563116c57a0e002beb19f03f164c4dfabc71fe721ac72453` |
| ReleaseBasisId | `E1-RELEASE-BASIS-sha256:bc176574817f6b7fe06fdcf87a71c57b2a8bfe74e55ed20f2aa55ad5d4fa5181` |
| ReleaseDecisionId | `E1-RELEASE-DECISION-sha256:43ab22254604a29f3cf2164152803ee5f689f7540e2006c43d27ded87d83d8c0` |
| continuation_chain_digest | `2193231e010af1189bd90e5519bfc1232f84e0de8dfc9fd6ed5d377616f83515` |
| AuthoritativeContextId | `E1-AUTHORITATIVE-CONTEXT-sha256:6e756710102559983a394f2c5119a9a9ff3f437e9fbbd1b973a01b4484d4824e` |
| FullContextDigest | `6e756710102559983a394f2c5119a9a9ff3f437e9fbbd1b973a01b4484d4824e` |
| ModelPayloadDigest | `8e9b1fa28d57a4c4e21e28dbe9be7d70e028438ce425862b43b3728d9c22b577` |
| ModelProjectionBindingDigest | `125db6caa97154c5ce61b082d7ceeaff208a32596363c9cf28edfba74a121e64` |
| ModelProjectionDigest | `ea2ced0e8e128d3afbe2bfb0591f6be2311a8512576159d20d40baf6f0bec610` |

The adopted authority-store context `2f51cf476c9b77eda1dbbb38407e68c8b698137b5732ab20416e9189522882c3` precedes the first material application `439bfbea3b1b75ba832f80e690ccdf7cd3e0414ae88eb063d0d8ecc430735ce0`, which precedes the current corrected application above. After initial publication, final review added exact host-receipt plan/launcher hash comparison against the independent host grant. The first publication is retained; this append-only correction binds its exact private publication and ancestry. Release and dispatch amendment bytes and identities are identical across both applications. No successor, launch, activation or ownership occurred between them. The final external bootstrap pin selects this qualified version.

Private store: `/tmp/kge-forge-controller-authority/auth-e1-wp-001-r7-94f511dfcdcc43ac837191f8732ced39/material-supervisor-amendment-qualified-final`. Catalog SHA-256: `f7fc8a264c3e5b47646bfb0655a91331cf5c7ea4e443d2b96663b8758bc5f493`. All 558 logical objects / 552 distinct content objects were verified privately. Store placement remains outside all Programmer grants and execution/transmission roots. Repository files are documentary provenance, not operational authority.

Private publication pin: `/tmp/kge-forge-controller-authority/auth-e1-wp-001-r7-94f511dfcdcc43ac837191f8732ced39/material-amendment-publication-2026-09-17-final/PUBLICATION_RECORD.json`, SHA-256 `60579ec3410ceca6692bedc6e8c5fd1c80e9acae86995bff0ec98ab78a99f239`. Restart verification read the private pin with an explicit expected hash, opened the pinned store, checked every object, reconstructed full operational ancestry, authenticated the original dispatch plus the explicit amendment, and reconstructed the original authorization lifecycle without acquiring an ownership fence. See `POST_PUBLICATION_RECONSTRUCTION.json`.

## Qualification

All twelve requested cases are mapped in `QUALIFICATION_COVERAGE.json`. Seventeen targeted synthetic amendment tests pass. Twenty-seven current regression tests pass; the unchanged payload namespace isolation probe also passed its explicitly permitted retry outside the sandbox after the sandbox rejected NETLINK_ROUTE. Original failed sandbox output remains evidence; no validator exception was introduced.

Tests cover original-release S1 behavior, private release/dispatch decision authentication, missing/invalid amendments, wrong composite authority, absent/wrong dispatch inheritance, inability to self-authorize S2, separate specific succession authority, separately attributable Jerry host consent, exact receipt-to-grant hashes, private substitution, replay/reordering, correction ancestry and fresh-process reconstruction. Regressions cover private authority isolation, production activation/ownership/handoff/recovery synthetically, transmission filtering, governed execution and authoritative QUIESCENT, lifecycle and context/payload preservation. No synthetic fixture uses real E1 ownership.

Production readiness remains **BLOCKED**: no private specifically authorized successor policy or genuinely observed S2 exists. This is the expected stop point, not a failed amendment qualification. The original dispatch inherits only through the authenticated explicit dispatch amendment; neither amendment supplies a successor identity.

## Frozen host package and exact proposed installation

Frozen launcher SHA-256: `bf98d94070c5fdcc7861fc6383529f31e8de228571f184342c4cbd414b9be7d6`.
Frozen launch-proposal SHA-256: `b09b279b896625b44446b1c5c77e7c4139b33357d07a83110192ef889f25e39c`.
The accepted full succession inventory and qualification closure remain exact. The installation target `/var/lib/kge-forge-supervisor-succession/` remains absent.

`HOST_INSTALLATION_MANIFEST.json` contains source/destination/owner/mode and exact hashes. `PROPOSED_LAUNCH_SPEC.json` contains every proposed field with the current operational binding and qualified consumption inventory: interpreter `/usr/bin/python3.11`, argv `[/usr/bin/python, -m, adapter.supervisor_server, /tmp/a21m.sock]`, UID/GID 1000:1000, supplementary groups [], workspace `/home/gvasend/app/kge-forge`, delegated cgroup `/sys/fs/cgroup/unified/kge-forge/executor`, socket `/tmp/a21m.sock`, exact environment and unchanged protocol constants. It retains `PROPOSED_NOT_AUTHORIZED` and a null prelaunch audit hash.

`HOST_INSTALLATION_PROCEDURE.md` gives exact human installation commands and post-launch capture requirements. The frozen wrapper places the root child in the delegated cgroup before credential drop. It does not rely on unprivileged startup in user.slice followed by migration. No command in that document was executed.

Architect pre-launch fields that can be proposed now are `authority`, decision type, predecessor S1, current `runtime_binding`, frozen `launcher_sha256`, implementation/qualification identities and proposed plan fields. Actual `authorization_id`, `qualification_acceptance_id`, executable plan status and final `launch_spec_sha256` require the separate Architect launch decision and fresh host observations. Specific succession acceptance remains post-launch and must bind genuine S2 identity and the exact event body; all current S2/event/approval fields are null.

Jerry must explicitly provide a separately attributable HOST_OPERATOR launch authorization: operator, decision, authorization ID/source, exact launch-spec/launcher hashes, predecessor, runtime binding and command/scope. Its ID becomes `host_operator_authorization_id` in the wrapper input. Root staging/installation, cgroup placement before credential drop and launch must be covered. `remove_verified_stale_socket` remains false unless Jerry separately authorizes deletion after a genuine no-listener check. See `HOST_AUTHORIZATION_BOUNDARIES.json` for exact schemas. The root wrapper authenticates file ownership and exact bytes but does not itself verify signatures; the root operator must authenticate both actual decisions before staging, and the production controller additionally requires the private attributed host grant and matching receipt.

Final approved plan and authorization file hashes are intentionally unset: those files and consents do not yet exist. Proposal hashes are exact and are not represented as executable authority. The unchanged final launch command, for the separately authorized human operator only, is:

```sh
sudo /usr/bin/python3.11 /var/lib/kge-forge-supervisor-succession/host_launch.py /var/lib/kge-forge-supervisor-succession/LAUNCH_SPEC.json /var/lib/kge-forge-supervisor-succession/HOST_LAUNCH_AUTHORIZATION.json
```

## Stop confirmation

S2 unlaunched; no host package installed; no SupervisorSuccession event; no real E1 activation event or ownership; zero E1 model requests and zero E1 implementation effects. Model-handoff eligibility is false. E1-WP-001 remains INELIGIBLE and UNDISPATCHED. No human/host consent was fabricated.
