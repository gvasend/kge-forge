# Package 107 — Direct-Host Calibration Guard Assessment

**Result: PARTIAL.** Existing host mechanisms are candidates, not a qualified calibration boundary. No negative inference about host capability is drawn from Codex restrictions.

Package 106 and its inputs authenticate. The retained model remains four simultaneous application processes, six lifetimes, five child launches and a proposed 144,359-byte allocation with a 32,694-byte protected reserve. These are not measured or enforced limits.

Historical owner-supplied direct-shell evidence identifies ubuntu01, Ubuntu 20.04.6, kernel 5.4.0-216-generic and successful Bubblewrap 0.4.0 user/PID/network namespace creation. Direct Python version is reported as 3.8.10 in Package 85, but its direct raw executable hash and startup closure are missing. Current executable hashes, namespace sysctls, mount metadata and security observations are separately labelled Codex-context. They do not establish direct permissions or independently reproduce the historical namespace result.

The smallest candidate guard combines finite per-process CPU/address-space/descriptor limits, explicit aggregate/observer budgets, a dedicated qualified kernel workload boundary, an external monotonic observer, bounded cumulative output with a critical reserve, and exact filesystem/network restrictions. A dedicated cgroup is a candidate; PID namespace teardown is an alternative requiring lifecycle evidence. Neither a parent process group nor installed timeout/prlimit commands establishes complete descendant termination. Independent helper sessions and unknown descendants must remain covered.

Read-only direct-shell metadata was requested. Missing observations are exact interpreter/Bubblewrap hashes and startup inputs, current direct limits/security, controller mount/path ownership and permissions, namespace configuration, and exact disposable-store filesystem/mount metadata. No store was created. A subsequent active check requires exact executable/arguments, finite independently justified safety caps and a pinned observer; these inputs are incomplete, so no selectable dossier is offered. Existing construction grants are not expanded.

The graph is acyclic and does not depend on future pids probe output. Four fresh static reconstructions agree and eleven negative classifications are rejected. These results do not demonstrate active resource enforcement. LL-11 and all prior evidence remain preserved.

```text
WORK_PACKAGE = E2-P05-D01-H77-02-DIRECT-HOST-CALIBRATION-GUARD-107
RESULT = PARTIAL
DIRECT_HOST_PROFILE_COMPLETE = NO
CPU_CONTROL_AVAILABLE = UNDETERMINED
MEMORY_CONTROL_AVAILABLE = UNDETERMINED
FD_CONTROL_AVAILABLE = UNDETERMINED
INDEPENDENT_WATCHDOG_BOUND = NO
PROCESS_CONTAINMENT_QUALIFIED = NO
FILESYSTEM_CONFINEMENT_QUALIFIED = NO
CALIBRATION_GUARD_COMPLETE = NO
CALIBRATION_DECISION_READY = NO
CALIBRATION_EXECUTION_READY = NO
FOUR_SEED_DETERMINISM = PASS: 0,1,7,101
NEGATIVE_SUITE = PASS: 11/11 static negatives
TOTAL_REFERENCES = 161
TOTAL_RESOLVED = 109
TOTAL_UNRESOLVED = 52
NEXT_CRITICAL_BLOCKER = Fresh direct-shell executable/startup, limits/security, cgroup controller path ownership/permissions and mount metadata; then separately pinned observer and finite whole-boundary safety contract.
BRIDGE_SOURCE_FILES_MODIFIED = 0
CALIBRATION_OPERATIONS_EXECUTED = 0
BRIDGE_TESTS_EXECUTED = 0
SYSTEM_LEVEL_PROBES_EXECUTED = 0
H77_02_PROBE_EXECUTED = NO
A15_EXECUTED = NO
A15_EXECUTION_AUTHORITY_ISSUED = NO
A15_CAPTURE_AUTHORITY_ISSUED = NO
STOPPED_CAMPAIGN_MODIFIED = NO
LL_11_PRESERVED = YES
PRODUCTION_EFFECT = NO
DECISION_OPTIONS = []
```
