# System-Level Process-Tree Enforcement Qualification — Package 86

RESULT = PARTIAL. The prospective system-level command, finite resource/security boundary and independent observation contract are sealed. Actual system-management authority and the live direct-host profile remain unverified, so no selectable authorization dossier or execution grant was created.

Read-only metadata identifies installed systemd245 and exact `systemd-run`, `systemctl`, Python and documentation hashes. The system-manager `show` query failed with `Failed to connect to bus: Operation not permitted` in the managed context. This does not establish the direct system manager's state, actual permission, or the exact denying policy. No sudo, transient unit, system configuration change or capability probe was invoked.

The installed primary resource-control documentation explicitly maps TasksMax to pids.max and states that resource control is disabled for the systemd user instance on the legacy hierarchy. This supports investigating the system manager separately from the retained user-level observation. It does not prove that a system transient service on ubuntu01 is currently enforceable. Pids membership must be read independently from name=systemd membership; configured properties alone are insufficient.

The proposal is one default-system-instance transient service (no --user or --scope), explicitly UID/GID1000, named from a stable Package86 seed independent of future approval. Its inert inline Python payload reads only its own proc/cgroup metadata and sysfs pids.max/current, emits two bounded records with actual observation times, sleeps8s between them and exits. It imports no project modules and accesses no runtime/history data. TasksMax8 is a preliminary metadata setting, not a replacement for the approved four-child campaign ceiling. No excess-task creation is included; matched kernel/configuration values demonstrate only configured service-specific enforcement, while rejection of excess tasks requires a separate bounded test.

The exact command sets task/memory/CPU/address-space/descriptor/output-file limits, RuntimeMaxSec20, bounded stop, control-group kill, Restart=no, non-root execution, NoNewPrivileges, PrivateNetwork, strict filesystem/home protection and readonly cgroups. --wait/--collect and exact-unit cleanup checks are mandatory. Payload regular-file writes are zero; transient-manager/cgroup/private-temp bookkeeping and bounded observer evidence are separately declared permissible effects for any future authorization. Actual enforcement/security property support and observer permissions remain entry gates.

An independent observer must capture the live service MainPID and configured TasksMax, read that PID's own pids and name=systemd paths, compare kernel pids.max/current against the unique service path, then observe exit and absence of a persistent/active unit. Service self-report cannot prove termination. Output is capped at64KiB and one service launch is permitted with zero retries; original failure evidence survives cleanup failures. A qualified observer and durable prelaunch attempt record are still required before activation. No issued identity or actual observation timestamp was invented.

The qualification charter does not create operating-system administration authority. An authenticated resource administrator or applicable existing narrow Polkit/systemd-management delegation must authorize this exact unit, command, properties, UID/GID and cleanup. Root service payloads, sudoers/polkit changes, persistent settings and broad permissions are excluded. Current policy metadata is not proof that the current caller is authorized. The smallest missing prerequisite is the actual administrator designation and scoped authorization/delegation evidence, followed by independent completion of the direct entry profile.

TasksMax does not qualify Bubblewrap composition, network/filesystem isolation, child limits, hard campaign deadlines, independent observation or cumulative writes. The cumulative-byte gap from Package85 remains unchanged: capacity, file size, final retained size and block-I/O totals are not automatically cumulative content-write accounting. No approved meaning was amended and the entire H77-02 campaign remains unqualified.

Four fresh metadata/AST reconstructions under seeds0,1,7,101 agree and12/12 static negatives reject hierarchy, root, resource, permission, cleanup, network, scope and readiness substitutions. The prospective payload was only parsed/compiled for syntax, never executed. The121-event lessons chain and all prior source/evidence seals are preserved; no duplicate lesson or efficiency claim was appended.

## Required report

```text
WORK_PACKAGE = E2-P05-D01-H77-02-SYSTEM-LEVEL-PROCESS-ENFORCEMENT-86
ADMINISTRATIVE_AUTHORITY_VERIFIED = NO
EVIDENCE_CONTRACT_COMPLETE = YES
PROBE_COMMAND_COMPLETE = YES
RESOURCE_BOUNDARY_COMPLETE = YES
RESULT = PARTIAL
SYSTEM_LEVEL_PROBE_DECISION_READY = NO
SYSTEM_LEVEL_PROBE_EXECUTION_READY = NO
SYSTEM_LEVEL_PROFILE_COMPLETE = NO
FOUR_SEED_DETERMINISM = PASS:0,1,7,101
NEGATIVE_SUITE = 12/12 PASS (static)
SYSTEM_LEVEL_PROBES_EXECUTED = 0
SYNTHETIC_TESTS_EXECUTED = 0
H77_02_PROBE_EXECUTED = NO
A15_EXECUTED = NO
TOTAL_REFERENCES = 161
TOTAL_RESOLVED = 109
TOTAL_UNRESOLVED = 52
NEXT_CRITICAL_BLOCKER = Actual ubuntu01 system-management administrator designation and scoped permission for this exact transient service/user/command and bounded observer/cleanup; live direct manager profile and entry evidence remain unverified
PRODUCTION_EFFECT = NO
GATE_SOURCE_FILES_MODIFIED = 0
A15_ADAPTER_SOURCE_FILES_MODIFIED = 0
STOPPED_CAMPAIGN_MODIFIED = NO
A15_EXECUTION_AUTHORITY_ISSUED = NO
A15_CAPTURE_AUTHORITY_ISSUED = NO
BASELINE_AMENDED = NO
E1_ARTIFACTS_MODIFIED = 0
git_diff_check = PASS
DECISION_OPTIONS = []
NEW_LESSONS = 0
```

Evidence: [inventory](system-manager-capability-inventory.json), [readonly commands](readonly-command-observations.json), [primary documentation](native-documentation-evidence.json), [exact service specification](transient-service-specification.json), [administrative authority](administrative-authority-assessment.json), [cgroup procedure](cgroup-verification-procedure.json), [resource/security boundary](resource-security-boundary.json), [compatibility](h77-compatibility-assessment.json), [cumulative writes](cumulative-write-limitation.json), [unissued subject](proposed-authorization-subject.json), [remaining gaps](remaining-gap-dossier.json), [independent verification](independent-static-verification.json), [four seeds](four-seed-reconstruction.json), [negatives](negative-controls.json), [preservation](preservation-audit.json).
