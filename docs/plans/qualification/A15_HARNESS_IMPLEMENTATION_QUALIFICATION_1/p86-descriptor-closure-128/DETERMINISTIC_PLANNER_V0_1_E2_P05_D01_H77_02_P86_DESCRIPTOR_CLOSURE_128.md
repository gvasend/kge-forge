# Package 128 — Inherited descriptor closure

RESULT = PARTIAL. The installed CPython launch API is a minimal candidate, but no exact existing caller is independently qualified. No owner options are prepared.

`candidate-python-invocation.json` binds the proposed `Popen` parameters: unchanged127 argv, executable `/usr/bin/prlimit`, explicit clean env and cwd, `close_fds=True`, empty `pass_fds`, `shell=False`, no `preexec_fn`, read-only null stdin and distinct output pipes. These are a static invocation specification, not an implemented launcher or host-enforcement receipt. FD0–2 are constrained by backing object/type/direction, not assumed safe by number.

Independent AST inspection of pinned `/usr/lib/python3.8/subprocess.py` establishes that this invocation excludes the local posix_spawn fast path and passes close_fds to built-in fork_exec. The inspected Python callsite does not prove the embedded native close-all/error-pipe implementation or its build correspondence. No target module was imported or executed. The libbsd closefrom manual is documentary evidence only; it ignores closing errors and does not supply a qualified existing callsite. Kernel close_range support is not inferred.

The first requested native target is prlimit. The report says FIRST_NATIVE_EXECUTABLE_IDENTIFIED=NO because the actual upstream invoking context is not bound: if Python must first be launched, Python is an earlier executable. Closing before prlimit cannot retroactively protect interpreter startup. The smallest missing proof is an authenticated existing caller/configuration with safe startup, explicit closure invocation and independently verified standard endpoints. Native closure correspondence and wrapper descriptor lifetime also remain pending. Seek existing host/operator receipts rather than construct a generic supervisor.

Descriptor possession is not an exploit demonstration. Read-only regular handles do not themselves grant writes; writable files, directory handles, sockets and aliases can convey capabilities not removed by later mount restrictions. Neither a mount profile nor post-write hashes prove inherited-capability closure.

The sealed124 profile and127 parent proposal remain byte-identical. Aggregate CPU/memory/tasks/scratch enforcement, full-workload termination, independent observation and bounded durable publication remain separate unresolved gates. A hypothetical harmless synthetic FD census is described separately and remains unsealed/incomplete; it cannot replace findmnt or qualify its own launch.

All36 earliest phase classifications are retained. Actual census/mount/exit outcomes remain execution-produced evidence; independently enforceable entry controls remain prior obligations. The graph is acyclic and no future witness qualifies its own launch or observer.

Four fresh static reconstructions (seeds0,1,7,101) agree on `a0df4f8170f6671b764988a985be678750a6aeb7defdae52a6ed22fd9ccf819f`. There are27 distinct negative designs and108 actual rejected executions. These are static admission mutations, not runtime confinement tests. All20293 prior files were hash-compared unchanged. The lessons register was reviewed and unchanged. `git diff --check` passed. Historical161/109/52 is not frontier progress.

```text
WORK_PACKAGE = E2-P05-D01-H77-02-P86-DESCRIPTOR-CLOSURE-128
RESULT = PARTIAL
PACKAGE_124_ARGV_UNCHANGED = YES
PACKAGE_127_PARENT_PROCEDURE_AUTHENTICATED = YES
FIRST_NATIVE_EXECUTABLE_IDENTIFIED = NO
DESCRIPTOR_ALLOWLIST_COMPLETE = YES
DESCRIPTOR_CLOSURE_PRE_ENTRY_VERIFIED = NO
INTERMEDIATE_EXEC_CLOSURE_VERIFIED = NO
PROTECTED_FD_ESCAPE_EXCLUDED = NO
INDEPENDENT_OBSERVER_READY = NO
AGGREGATE_RESOURCE_BOUNDARY_READY = NO
PUBLICATION_BOUNDARY_READY = NO
ENTRY_EXECUTION_SCOPE_MATRIX_COMPLETE = YES
DEPENDENCY_GRAPH_ACYCLIC = YES
CAPABILITY_CHECK_DECISION_READY = NO
CAPABILITY_CHECK_ENTRY_READY = NO
REAL_PROBE_EXECUTION_READY = NO
DECISION_OPTIONS = []
FOUR_SEED_DETERMINISM = PASS
NEGATIVE_DESIGNS = 27
NEGATIVE_EXECUTIONS_REJECTED = 108
NEXT_CRITICAL_BLOCKER = Authenticated actual existing caller configuration and safe interpreter-startup FD boundary for the explicit Popen route; no such caller receipt is retained.
TOTAL_REFERENCES = 161
TOTAL_RESOLVED = 109
TOTAL_UNRESOLVED = 52
SOURCE_FILES_MODIFIED = 0
CAPABILITY_CHECKS_EXECUTED = 0
SERVICES_CREATED = 0
SYSTEM_LEVEL_PROBES_EXECUTED = 0
H77_02_PROBE_EXECUTED = NO
A15_EXECUTED = NO
AUTHORITY_ISSUED = NO
PRODUCTION_EFFECT = NO
GIT_DIFF_CHECK = PASS
```
