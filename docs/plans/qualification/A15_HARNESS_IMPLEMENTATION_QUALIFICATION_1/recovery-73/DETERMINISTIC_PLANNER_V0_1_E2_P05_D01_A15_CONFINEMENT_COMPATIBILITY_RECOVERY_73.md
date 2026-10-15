# A15 confinement compatibility and recovery — Package 73

`RESULT = PARTIAL`. The exact failed socket operation is localized; the underlying rejecting policy is **not established**. The existing physical host is **UNDETERMINED**, rather than generally incapable. No Bubblewrap retry, fake/native test, system change, migration, source edit or privilege request occurred.

The Package72 index, six unchanged implementation files, recorded metadata-child status 1, stderr, empty stdout hash, parent/child observations and stopped append-only campaign ledger authenticate. The diagnostic is:

```text
bwrap: loopback: Failed to create NETLINK_ROUTE socket: Operation not permitted
```

The installed executable is upstream version 0.4.0, Ubuntu package `0.4.0-1ubuntu4.1`, mode0755 without setuid/setgid. Its exact approved binary hash matches. Read-only disassembly shows socket arguments AF_NETLINK=16, type0x80003 and protocol0; a negative return branches to the exact error string. This independently localizes the failing operation. [Upstream network setup](https://raw.githubusercontent.com/containers/bubblewrap/v0.4.0/network.c) and [launcher ordering](https://raw.githubusercontent.com/containers/bubblewrap/v0.4.0/bubblewrap.c) corroborate that the matching diagnostic occurs during loopback initialization before later binding/configuration; full distro-patched source was not reconstructed.

The attempted argv is derived from the sealed launch recipe, recorded scratch/repository/probe inputs and currently observed conditional system paths. Package72 did not retain original argv or the failed child's filter/capability/LSM snapshot. This reconstruction is not presented as an observed historical argument capture. Requested isolation includes user, PID, network, IPC, UTS and mount setup, readonly code/fixture mounts, one writable output row, dropped capabilities and parent-linked lifetime. Resource pre-exec configuration matches the approved limits; no successful inner probe or complete enforcement claim is inferred.

Passive inventory observes Linux 5.4.0-216-generic/x86_64, Python3.8.10 with the unchanged interpreter identity, `unprivileged_userns_clone=1`, positive user/network/mount namespace limits, current `Seccomp=2`, `NoNewPrivs=1`, and zero current capability bounding/effective sets. Current AppArmor attr is `unconfined`, while AppArmor is enabled. Its loaded profile list is permission-denied, no SELinux enforcement value is available, and the readable kernel log supplies no matching denial. The actual effective seccomp program and historical child state are not observable. Current proc metadata is not substituted for historical evidence.

The mount view contains hybrid cgroup-v1/v2 hierarchy and readonly cgroup mounts in this execution context. The existing delegated executor path is project-user-owned, but write access is not established through the readonly view; no control file was written. Kernel rlimit interfaces/current values are observable, but lowering/enforcing them was not tested here. A syscall's EPERM may come from an effective filter, LSM or another outer policy. These observations do not identify which one. Namespace setup reached the reported loopback stage according to the matching code path; that is not proof that all required namespace/mount/network behavior works.

The approved-control matrix preserves OS-enforced filesystem and network isolation, controlled process lifecycle/limits, CPU/address-space/file/descriptor rlimits, wall/campaign accounting, immutable publication, independently observed writer termination, exact handoff/full oracle comparison and zero retries. Application path checks and process names do not replace OS confinement. Direct-child accounting is not automatically proof of arbitrary-descendant control. No recovery may drop `--unshare-net`, enable host networking, run unrestricted subprocesses, ignore unsupported caps or reset a stopped ledger.

**Option A: existing host.** First obtain effective policy or precise denial-audit evidence from the actual outer launcher/security owner. Only a separately authorised dedicated qualification context preserving every mandatory protection can be considered. No global policy relaxation, blanket capabilities, privileged container or unconfined seccomp recommendation is made. The project qualification charter grants no administrative/system rights. Existing-host compatibility remains unknown until all controls and actual scoped permissions are independently verified.

**Option B: compatible host or VM.** A minimum requirements profile is specified: exact approved or separately qualified interpreter/launcher/dependency identities, authorised namespaces/private-network loopback setup, readonly inputs and isolated row outputs, child/resource limits, lifecycle/full comparisons, trusted audit and actual actor ownership/permissions. No actual host ID, security profile, permission evidence or dependency seal is invented. A different host/workspace fingerprint requires exact subject/profile authority and a fresh bounded campaign. No files were migrated. A VM retaining the same launcher may reduce source changes, but superiority or effort savings are not established.

**Option C: alternative confinement.** VM/container/another launcher remain unselected, unqualified candidates. Every mandatory control needs equal-or-stronger evidence. Host isolation alone does not prove per-variant writable mounts, descendant limits, fresh readers or independent writer termination. Replacing hardcoded Bubblewrap/probe assumptions requires a bounded source/subject amendment and independent validation; unrestricted subprocess execution is not an equivalent.

Recovery has two additional static bindings. The code pins original grant digest `25395fb3c06be58a8c538c618b9e50b9d118aa415d0843968254d3f8e83dd8fa`, and its source-relative shared `campaign-budget.jsonl` already has `stop`. Environment repair alone does not allow another reservation or silently substitute a fresh grant. A future decision must explicitly qualify current-authority versus original protocol-context binding and a new immutable campaign/journal namespace—through a bounded source amendment or an explicitly governed equivalent renewed context/fresh workspace. Neither approach is selected or proven valid. The old source/evidence/journal remains unchanged.

The immutable Package71 issuance remains authenticated. Package72's campaign is terminated under the approved rule; the old effective reference is not permission to repeat it. `AUTOMATIC_RETRIES=0`, and extra campaigns require fresh explicit bounded approval. The preservation label “effective grant reference” describes authenticated historical issuance, not a currently active campaign. No new authority is issued and no incomplete selectable campaign dossier is offered.

The shortest currently defensible next action is **read-only policy/denial attribution by the actual security/launcher owner**, followed by an exact permitted environment/control and source/grant/journal binding specification. If no acceptable same-host context exists, qualify a dedicated host/VM candidate. Any later metadata probe or campaign needs its own applicable permission; this package launches neither. Root-cause investigation does not require returning to broad historical A15 graph recovery.

Independent verification reconstructs the recorded error/source/binary mapping, passive metadata, mandatory controls, candidate equivalence/authority limits and readiness. Four fresh read-only reconstructions agree. Sixteen static corruption controls reject false success, unknown capability as available, disabled network isolation, application-only isolation, ignored limits, host changes, assumed equivalence, expired-campaign reuse, retries, unqualified host, unsupported cause attribution, invented argv capture, unrestricted subprocess and A15 scope expansion. These are metadata checks, not confinement or test execution.

LL-01 through LL-10 were reviewed without a new lesson or register modification. Existing strategy/completeness/scope/authority distinctions gain bounded supporting evidence; the earlier package's correct fail-closed stop is counterevidence against treating every delay as a model defect. All six sources, prior artifacts, original A14 preservation frame, checkpoint/oracles, V3, frozen acceptance and E1 remain exact. Accounting remains 161 total/109 resolved/52 unresolved. `git diff --check = PASS`.

```text
WORK_PACKAGE = E2-P05-D01-A15-CONFINEMENT-COMPATIBILITY-RECOVERY-73
RESULT = PARTIAL
PACKAGE_72_FAILURE_AUTHENTICATED = YES (retained error/exit/source/binary; argv source-derived, not recorded at runtime)
FAILURE_CAUSE_ESTABLISHED = NO
FAILURE_POINT_ESTABLISHED = YES
FAILURE_CLASSIFICATION = EPERM at NETLINK_ROUTE socket creation during Bubblewrap loopback setup
EXISTING_HOST_COMPATIBLE = UNDETERMINED
ALTERNATIVE_HOST_PROFILE_COMPLETE = NO (minimum requirements defined; actual host/profile/permission bindings absent)
ALTERNATIVE_CONFINEMENT_EQUIVALENT = UNDETERMINED
RESOURCE_ENFORCEMENT_READY = NO
FRESH_CAMPAIGN_AUTHORITY_REQUIRED = YES
RECOMMENDED_RECOVERY_PATH = Read-only authoritative outer policy/denial attribution; scoped same-host qualification context if independently permitted, otherwise qualified dedicated host/VM; preserve all controls and explicitly bind fresh grant/journal/workspace
NEXT_CRITICAL_BLOCKER = Authenticated denying-policy/owner evidence and exact permitted recovery environment/control/campaign binding; no complete campaign approval option yet
FOUR_SEED_DETERMINISM = PASS STATIC (0,1,7,101)
NEGATIVE_SUITE = 16/16 PASS STATIC (15 general plus explicit actual-A15 escalation control)
FAKE_PROTOCOL_TESTS_EXECUTED = 0
NATIVE_SYNTHETIC_TESTS_EXECUTED = 0
A15_EXECUTED = NO
A15_EXECUTION_AUTHORITY_ISSUED = NO
A15_CAPTURE_AUTHORITY_ISSUED = NO
TOTAL_REFERENCES = 161
TOTAL_RESOLVED = 109
TOTAL_UNRESOLVED = 52
A15_NORMATIVE_MANDATE_EFFECTIVE = YES
CHARTER_EFFECTIVE = YES
IMPLEMENTATION_TEST_GRANT_EFFECTIVE_REFERENCE_AUTHENTICATED = YES (immutable Package71 historical issuance)
IMPLEMENTATION_TEST_GRANT_EFFECTIVE = YES_AS_P71_ISSUANCE_REFERENCE_ONLY; current stopped campaign inactive
CURRENT_CAMPAIGN_ACTIVE = NO
ADAPTER_SOURCE_FILES_MODIFIED = 0
BASELINE_AMENDED = NO
V3_SELECTED = YES
FROZEN_OBLIGATIONS = 128
CONCRETE_DISPATCH_JOBS = 220
A14_PERSISTENCE_RERUN = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
GIT_DIFF_CHECK = PASS
```
