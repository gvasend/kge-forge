# E2-P05 D01 A14 cold-reader binding closure 29

**RESULT = PASS for static contract/preflight closure.** Independent reader role, guarded source/operands, process isolation, restore/replay behavior, identity oracle, output schema and failure handling are sealed. A14_PERSISTENCE_SEQUENCE_CONTRACT_READY = YES means specified, not executed or execution-authorized. All runtime guards remain unmet. Counts stay 58 resolved / 53 unresolved; first remaining sequence blocker is RUNTIME_PERSISTENCE_SEQUENCE.

Native reader entrypoint is codec.restore(path, expected_identity, repo_root), returning PersistenceBundle. Future wrapper is reader_entrypoint.run_reader(spec, supervisor_evidence, scope_verifier, guard_verifier). Its body is AST-inspected only and never invoked. It requires separately trusted future execution authorization and supervisor guard authentication before physical source access/restore. Restoring proves exact native model/identity/policy/source and owned replay-range reconstruction; actual future file visibility across writer/reader lifetimes is also required. No observed persistence result exists now.

The reader is a fresh executable Python interpreter after writer termination, with no forked writer object graph. Exact repository cwd/PYTHONPATH, PYTHONDONTWRITEBYTECODE=1, hash seeds 0/1/7/101, C.UTF-8 and close_fds isolation are specified. Each recovered cold-reader obligation retains at least three readers per checkpoint/seed. Inputs are persisted spec/handoff/reference and independently trusted configuration/process evidence; stdout/structured JSON is captured by the supervisor. No reader is launched in this package.

Runtime guards are separate and ordered: SAVE_RETURNED_SUCCESSFULLY, PUBLISHED_TARGET_VERIFIED, PERSISTED_HANDOFF_AVAILABLE, WRITER_EXIT_OBSERVED_BY_SUPERVISOR. Save return belongs to the save caller; publication verification to the writer-side verifier and trusted harness corroboration; handoff to persisted qualification metadata and hash/content checks; exit exclusively to parent wait/returncode observation. The writer record cannot attest its own future exit, and JSON booleans alone cannot authenticate process facts. Guard ordering includes writer termination before supervisor exit observation and reader launch. RUNTIME_GUARDS_SATISFIED = 0.

Two exact future row-specific target paths, 153602-byte/hash/native identity commitments, persisted handoff paths/hash/content and scope/lineage/provenance are fixed in reader-spec-operands.json and reader-spec-oracle.json. They remain FUTURE_SAVE_OUTPUT_DEPENDENCY references. Neither saved target nor handoff is asserted to exist. The reader takes its path from verified handoff only if it equals the externally sealed target; expected bundle identity comes from the independent native precommitment, not handoff trust alone.

All native restore arguments are explicit or derived from verified persisted reference: path, expected_identity and repo_root. Restore has no native defaults. Replay scope, selected P06 policy, checkpoint/frame and source identities are independently available comparison/configuration commitments, not warm Planner-state operands. The trusted wrapper’s scope/guard callbacks are supplied by the future qualification owner, not serialized from writer data. Supervisor runtime schema names PID/exit code/wait observation and exact guard fields; their actual values are future conditions, not TBD input definitions or current facts.

Warm-state transfer is prohibited for bundle/Snapshot/decoded model objects, open descriptors, writer caches, Python identity and temporary interpreter state. Persisted typed output may cross from reader to the comparison harness after restoration; it is never fed into native restore as trusted writer state.

Native restore reads a nonsymlink explicit absolute target, verifies planner-bundle-v1 raw identity before decoding, admits exactly PLANNER-BUNDLE-1 and closed native types, checks native canonical serialization/model/policy/replay constraints, authenticates all source/policy files and any required immutable ledger artifacts, then returns a newly reconstructed bundle. With this zero-event frame, initial=current at exact corrected checkpoint and no event is applied. Native scope remains PARTIAL_HISTORICAL_REPLAY; choosing P06 does not activate import_e1 or a full-E1 replay.

Expected restored native bundle identity is planner-bundle-v1:3e91c8e78f5352cc547964409d8d4dfb6643b5bf4f1d223f0268f694f97e9e2e. Snapshot identity is planner-snapshot-v1:7ec95347f9662731ad5254221c03196fe789eb3435d02947eb09a70077ab66b9. The exact frame, P06 policy-binding and replay-scope qualification IDs and ten source identities are independently sealed from Closure26 before any reader output. No future execution output is used as its own oracle.

Output contracts separate identity/persistence verification from full D01 capture. The identity reader reports restore status, native bundle/Snapshot identities, selected policy/scope, event count, source/policy checks, comparison result, process ID and failure classification. Full D01 capture schema includes qualification label, typed Snapshot/bundle, Computation/selection/resume/branches/witnesses, rejections, policy/source pins, Snapshot/bundle/event identities, native result and full field set, derived from preserved V2 capture source. Its complete independent expected values remain unsealed and FULL_OUTPUT_ORACLES remains 0/128. This package seals schema/identity preparation only.

Reader success requires trusted guard ownership/order, actual independent process, exact handoff/file/native identities, source/policy/model validation and empty-frame equality. Exit code 0 alone is insufficient. Full D01 qualification additionally requires independent full-output comparisons; an identity-reader PASS does not satisfy that later gate. Missing file, checksum/identity/Snapshot/policy/scope/source mismatch, decode/model failures, premature launch and warm leakage retain exact wrapper/native exceptions and failing boundary; no failure repairs state or becomes a PASS.

HEAD_REQUIRED = NO. The reader uses the explicit persisted target/identity, never HEAD. Durability claim remains normal native publication and process-lifetime visibility, not directory-fsync or arbitrary power-loss/general crash durability. No HEAD, directory-fsync or stronger durability claim is introduced.

Static preflight checks entrypoint AST, complete native operands/specs, future-reference types, guard ownership/order, existing restore operation, independent identity oracle, complete output/failure schemas, HEAD independence and process isolation. COLD_READER_BINDING_PREFLIGHT = PASS. Save/writer/reader sequence operands and guards are now specified, but trusted runtime authorization and all four actual observations are still absent. A14_PERSISTENCE_SEQUENCE_CONTRACT_READY = YES; SEQUENCE_EXECUTION_AUTHORIZED = NO.

No previously missing reference is determined solely by this reader contract: all six A14 save/restore native operands were already statically sealed, and runtime conditions do not count as newly resolved values. PREVIOUSLY_RESOLVED = TOTAL_RESOLVED = 58; RESOLVED_BY_COLD_READER_BINDING = 0; TOTAL_UNRESOLVED = 53; total = 111. Remaining source/mutation/invalidation boundaries are unchanged. FIRST_REMAINING_BLOCKER = RUNTIME_PERSISTENCE_SEQUENCE for this now-specified A14 sequence; no execution or other repairs occur. Complete 128-row invocation preflight remains NOT_RUN.

Four fresh static verification processes under seeds 0/1/7/101 reconstruct exact reader specs, identity oracle and semantic contract identity. They do not import/run the reader entrypoint or perform restore. Twenty-two static guards reject premature launch at each boundary, writer exit self-attestation, warm objects/descriptors, target/hash/identity/Snapshot/policy/source/scope/history substitutions, HEAD/durability claims, exit-only success and static satisfaction of actual runtime guards.

| Report field | Value |
| --- | --- |
| WORK_PACKAGE | E2-P05-D01-A14-COLD-READER-BINDING-CLOSURE-29 |
| RESULT | PASS |
| COLD_READER_BINDING_PREFLIGHT | PASS |
| HEAD_REQUIRED | NO |
| PREVIOUSLY_RESOLVED | 58 |
| RESOLVED_BY_COLD_READER_BINDING | 0 |
| TOTAL_RESOLVED | 58 |
| TOTAL_UNRESOLVED | 53 |
| A14_PERSISTENCE_SEQUENCE_CONTRACT_READY | YES |
| SEQUENCE_EXECUTION_AUTHORIZED | NO |
| FIRST_REMAINING_BLOCKER | RUNTIME_PERSISTENCE_SEQUENCE |
| SAVES_PERFORMED | 0 |
| WRITERS_TERMINATED | 0 |
| COLD_READERS_EXECUTED | 0 |
| RUNTIME_GUARDS_SATISFIED | 0 |
| INVOCATION_STATIC_PREFLIGHT | NOT_RUN |
| FULL_OUTPUT_ORACLES | 0/128 |
| END_INTERFACES_BOUND | 4/6 |
| P05_EXECUTION_READY | NO |
| E1_ARTIFACTS_MODIFIED | 0 |
| PRODUCTION_EFFECT | NO |

All 17427 pre-existing files remain unchanged, including save/writer contracts, native candidate, ten sources, frame/Snapshot, 117 capsules, 58 bindings, native runtime and E1. Historical UNPROVEN/UNRECOVERED labels are preserved; END stays 4/6 and P05 stages 13/13.

`A14_EXECUTED = NO`; `D01_CASES_EXECUTED = 0`; `E1_IMPORTED = NO`; `HEAD_UPDATED = NO`; `DIRECTORY_FSYNC_CLAIMED = NO`; `GENERAL_CRASH_DURABILITY_CLAIMED = NO`; `INSTALL_EVENTS = 0`; `NEW_AUTHORITIES = 0`; `N_REAL_SATISFIED = NO`; `git diff --check = PASS`.

The [JSON companion](DETERMINISTIC_PLANNER_V0_1_E2_P05_D01_A14_COLD_READER_BINDING_CLOSURE_29.json) pins reader callable/specs, process/guard contracts, independent identity oracle, native restore behavior, output/failure schemas, negatives and four-seed evidence under [the evidence directory](qualification/E2_P05_D01_A14_COLD_READER_BINDING_CLOSURE_29/).
