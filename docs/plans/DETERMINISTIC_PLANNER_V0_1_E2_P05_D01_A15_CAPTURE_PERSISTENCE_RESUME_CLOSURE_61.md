# A15 capture, persistence, and resume-reason closure — Package 61

`WORK_PACKAGE = E2-P05-D01-A15-CAPTURE-PERSISTENCE-RESUME-CLOSURE-61`

`RESULT = PASS` for static contract closure. Both complete expected outputs and the future isolated execution specification are sealed for the **unadopted Package 59 scenario**. This is neither an observed A15 PASS nor permission to execute. Normative scope adoption, exact issuer/version/grant binding, and execution authority remain for Package 62.

Package 60's evidence index matches exactly. Its retained-input state/event/bundle derivations are preserved; none were recomputed by invalidation execution. The retained A14 evidence index, 55 source/policy pins, native code, frozen acceptance, and selected V3 runner are authenticated in [authentication.json](qualification/E2_P05_D01_A15_CAPTURE_PERSISTENCE_RESUME_CLOSURE_61/authentication.json). All 17,475 files in the original persistence preservation inventory still match. LL-01–LL-10 remain intact; ten evidence reviews were appended, with no new lesson or proven causal hypothesis.

The exact initial Snapshot is `CONTENT_IDENTITY/planner-snapshot-v1:ce54ff49907abcad564ec0ddfe8c7a019fab129936172b67f4ce0ff5ed013586`. Both variants independently begin from that same immutable bundle. They do not inherit each other's outputs. The original capsule names the existing native checkpoint `docs/plans/qualification/E2_P04_CANONICAL_EXECUTION_RETRY_1/checkpoints/post-root-proof/post-root-proof.json`, whose native bundle identity is `CONTENT_IDENTITY/planner-bundle-v1:6dcd63b9cb4b6e6b074bd8112f24bf2c570615e1acab38c7afcb63df606ab0e0`. Its canonical bundle bytes and all nineteen adjacent ledger files match exactly. Future writers must each natively restore that source and compare the entire initial bundle before invalidation, including the full starting computation (RUNNABLE, FINISH actionable) and both current proofs usable. These starting-state values were checked through non-effecting queries of retained before-state metadata. This selection follows the capsule's exact provenance, without preferring a newer alias. Those two initial restores are separately included in execution scope; the eight later cold readers remain distinct.

| Proposed variant | Source content hash (`CONTENT_IDENTITY/raw-file-sha256`) | Expected Snapshot hash (`planner-snapshot-v1`) | Expected event 20 hash (`planner-event-v1`) | Expected bundle hash (`planner-bundle-v1`) |
|---|---|---|---|---|
| ROOT provenance withdrawal | e7bb37c91329dd58c80c14ac4319fbd1f4e562ef6c59a65bcad99ccf8ed6f8a4 | 9330a5e3b915f9646a738d8717059011eddc1b763df6d7fc9dc7fefa640e1e85 | 3447587e9ba40133513c095f3bc1151b13db75e5208aa1947f0271b704e85122 | 744cf8638403bcc24ff93b120afb9a025525431a2061efcd5cd895efb0085efe |
| SLOT provenance withdrawal | d5ffca80b0bd5e0d2776dc50d16c5d5ba7a9f31f7cf129c9cafed2ce50773107 | 0816f00046640f0ca9d4a6ec711129dd7856eb85194ef52e57a816f0905f4bae | 346a4b374c1c78072091cd91b7f3c9cf9d98a1cd5daaf93f707cd6beeee1a203 | 6bd2744afff2f9d79ed6e84d5f017809e6dad7a8a5eabd71e1705a693ed8c600 |

Each complete expected record contains the exact wire state, all native bundle fields, the 20-event sequence, the full 16-field V3-compatible normalized capture DTO, supplemental native proof-usability comparisons, protection comparisons, and canonical serialized bytes. Those byte artifacts are qualification expectations, not native saved bundles or publications. A pure native metadata codec round-trip also agrees byte-for-byte with the independent encoders; it invokes no replay, invalidation, capture, save, or restore. Each has exactly **1,215,025 bytes**; its SHA-256 equals the corresponding expected bundle hash above.

The capture inputs and observation stages are explicit. Future `record_result(original_bundle, supplied_SourceInvalidation, snapshot_resolver=None)` performs application internally and returns a new `PersistenceBundle`. The supplied body is the already specified SourceInvalidation wire value, not a TransitionReport. Sequence 20 binds the exact initial Snapshot, prior event 19, prescribed body, and derived after-Snapshot. No separate pre-application is permitted. Compare `POST_RECORD_RESULT` using the returned updated bundle as subject, bundle, and native result; compare `POST_COLD_RESTORE` using the restored updated bundle in the same roles. The complete capture DTOs at those stages are identical.

`apply_event` returns `TransitionReport(snapshot, action_transitions, computation)`; proof usability and resume are separate queries, not extra fields on that result. `save_bundle` returns `(Path, ArtifactIdentity)`; `restore` returns `PersistenceBundle`. Exact signatures, source hashes, types, and error contracts are in [native-interface-inventory.json](qualification/E2_P05_D01_A15_CAPTURE_PERSISTENCE_RESUME_CLOSURE_61/native-interface-inventory.json). None of these effect/capture/replay entrypoints was invoked.

The selected V3 A15 dispatch still supplies the prior bundle after `apply_event`. It remains unchanged and cannot stand in for this future sequence. The specification binds an updated-bundle capture adapter without promoting a V3 operand or repairing its dispatch. Any later matrix/capsule/invocation amendment requires its own exact governing decision.

Native resume output exposes exactly `allowed`, `actions`, `reasons`, and `supporting_identities`. Both variants expect `allowed=false`, empty actions and supporting identities, and this exact ordered reason list:

```text
DECISION:E2-DECIDE:E2-REENTER:COMPLETED_OR_UNAVAILABLE
DECISION:E2-DECIDE:NAMED_REENTRY_NOT_ACTIONABLE
EXTERNAL:E2-GATE:E2-REENTER:COMPLETED_OR_UNAVAILABLE
EXTERNAL:E2-GATE:NAMED_REENTRY_NOT_ACTIONABLE
```

These reasons derive from the two preserved named routes to completed `E2-REENTER`, their current receipt/decision authority, and their accepted event bindings. The exact policy/suspension binding remains `CONTENT_IDENTITY/planner-resume-binding-v1:639c8cc943fd7394dda03aabfd82498ee5971f56e685eaea898cd84d576b1e37`. Neither route has an actionable member, so source-verification-for-permission is not entered and no supporting permission identity is returned. Save/restore must nevertheless validate all 55 pins independently.

`FINISH` is not a named native resume route. Its ActionStatus is separately expected `BLOCKED`; global `Computation.control` is `PLAN_DEFECT`, with no actionable selection. A FINISH-specific reason, reason-code identity, blocking-dependency field, authority-state field, or currentness-state field is not invented. Supporting evidence is retained separately. A false Boolean with a wrong reason or reason order fails comparison.

The matching proof and contract's current validation become `STALE`; the other proof's validation stays accepted. Both native proof-usability results are false because the shared ROOT/SLOT configuration loses currentness. Native `ANY` is preserved across all retained alternatives; the full retained proof list is compared, with no suppressed alternative. SLOT and ROOT are unresolved. The original nineteen events remain exact immutable history; the stale witness is the appropriate current validation field. Full-state comparison permits only the Package 59 specified indirect effects and preserves all protected identities, authority, policy, context, unrelated evidence, and E1.

The future lifecycle is fully specified in [writer-handoff-cold-reader-contracts.json](qualification/E2_P05_D01_A15_CAPTURE_PERSISTENCE_RESUME_CLOSURE_61/writer-handoff-cold-reader-contracts.json): one supervisor, two fresh writers, and eight fresh readers, four per variant under hash seeds `0,1,7,101`. Each writer compares the complete post-record output, invokes native save to its isolated row target, verifies the returned identity and all 20 ledger files plus bundle bytes, then publishes an immutable handoff. The supervisor must observe its own child successfully terminate and independently verify publication before launching readers. A handoff is not evidence of its writer's exit.

The two reserved future output namespaces are below `docs/plans/qualification/A15_PROSPECTIVE_SCENARIO_1_RUNTIME/`, one per exact variant ID. Paths, bundle filenames, ledger byte hashes, handoff paths, supervisor evidence, and reader evidence paths are specified in [save-target-contracts.json](qualification/E2_P05_D01_A15_CAPTURE_PERSISTENCE_RESUME_CLOSURE_61/save-target-contracts.json). Both namespaces are currently absent and have no symlink substitution. No target was created. These checks must be repeated under future authority immediately before use. There is no HEAD transaction or cross-variant publication. The input has no dossier materializations, so no additional Snapshot archive is required by the native save guard.

Persistence assurance is the existing native file-fsync-before-immutable-hard-link publication and survival across writer lifetime. No directory-fsync, atomic multi-file transaction, or general crash/power-loss guarantee is added. A14's retained saves, supervisor exits, and 24 reader comparisons establish capability only; its authority is not transferred and its sequence was not rerun.

Every fresh reader must restore the prescribed bundle identity, compare all canonical bundle and ledger bytes, the complete capture DTO, all native typed-proof usability results, source/policy pins, admission validation, ROOT/SLOT satisfaction, FINISH status/control, complete resume fields/reasons, and protected state. Logical calculations do not invent ledger events. Persistence and restore preserve exactly the same expected output and event prefix/order.

[Failure/retry rules](qualification/E2_P05_D01_A15_CAPTURE_PERSISTENCE_RESUME_CLOSURE_61/failure-retry-matrix.json) fail closed on identity, capture, publication, handoff, termination, reader, replay, reason, or protection failure. No blind retry follows semantic/identity mismatch. A separately permitted transient retry starts only from the original immutable bundle; identical staged files may be reused only after exact manifest verification. No retry starts from a partially updated object, deletes evidence, overwrites a conflict, or promotes a failed result by majority vote.

Static construction used read-only predicate queries on the retained **before-state**, inspected native source rules, and verified preservation frames. The separate verifier reconstructs the expected states through Package 60's original-input overlay path, evaluates receipt/decision/currentness predicates directly from wire inputs without native replay, reconstructs all resume fields, and independently encodes canonical expected bytes. Four fresh static verifier processes produce identical semantic hashes. All **22 static negative controls pass**. These are corruption/protocol checks, not runtime fault injection or cold-reader execution.

Normative scope authority must adopt the exact two-variant admission-provenance boundary, owner set, requiredness, partition and nonempty protection policy. Execution/capture authority must bind the native sequence, immutable paths, process limits and failure rules. A native baseline replacement is not currently justified. Package 62 may prepare the exact bounded decision subject and authenticate its issuer/version; it cannot obtain authority from these readiness flags. No historical global-owner completeness or original A15 occurrence is claimed.

```text
WORK_PACKAGE = E2-P05-D01-A15-CAPTURE-PERSISTENCE-RESUME-CLOSURE-61
RESULT = PASS
PACKAGE_60_AUTHENTICATED = YES
PROSPECTIVE_VARIANTS = 2
CAPTURE_RESULT_BINDINGS = 2 EXACT_STATIC
EXPECTED_BUNDLE_IDENTITIES = 2 EXACT
EXPECTED_SERIALIZED_BYTES = 2 EXACT; 1215025 BYTES EACH
RESUME_REASON_SCHEMA = ResumeEligibility(allowed, actions, reasons, supporting_identities)
VARIANT_1_RESUME_REASON_COMPLETE = YES
VARIANT_2_RESUME_REASON_COMPLETE = YES
VARIANT_1_FULL_ORACLE_READY = YES
VARIANT_2_FULL_ORACLE_READY = YES
FULL_A15_ORACLE_READY = YES
SAVE_TARGET_CONTRACTS = 2 SEALED_STATIC; 0 CREATED
WRITER_EXIT_CONTRACTS = 2; SUPERVISOR_OBSERVED_EXIT_REQUIRED
COLD_READER_CONTRACTS = 8; 4 SEEDS PER VARIANT; 0 LAUNCHED
FAILURE_RETRY_CONTRACT = SEALED_FAIL_CLOSED
STATIC_HARNESS_READY = YES
AUTHORITY_PREPARATION_ELIGIBLE = YES
NEGATIVE_SUITE = 22/22 PASS STATIC
FOUR_SEED_DETERMINISM = PASS
LESSONS_REVIEWED = 10
NEW_LESSONS = 0
TOTAL_REFERENCES = 161
TOTAL_RESOLVED = 109
TOTAL_UNRESOLVED = 52
NEXT_CRITICAL_BLOCKER = PACKAGE_62_ISSUER_VERSION_SCOPE_AND_SEPARATE_AUTHORITY_BINDING
A15_EXECUTED = NO
A16_EXECUTED = NO
A14_PERSISTENCE_RERUN = NO
NORMATIVE_AUTHORITY_ISSUED = NO
EXECUTION_AUTHORITY_ISSUED = NO
BASELINE_AMENDED = NO
END_INTERFACES_BOUND = 4/6
P05_EXECUTION_READY = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
git diff --check = PASS
```

`STATIC_HARNESS_READY` denotes the complete static execution specification; no supervisor executable was installed or launched. `FULL_A15_ORACLE_READY` denotes the two independently checked prospective outputs under the proposed scope. The selected V3 ledger still has `FULL_OUTPUT_ORACLES = 0/128`; no operand is promoted and no frozen qualification PASS is asserted.
