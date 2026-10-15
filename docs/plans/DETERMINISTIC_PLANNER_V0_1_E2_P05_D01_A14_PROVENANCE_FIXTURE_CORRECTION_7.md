# E2-P05 D01 A14 bounded provenance fixture correction 7

`WORK_PACKAGE = E2-P05-D01-A14-PROVENANCE-FIXTURE-CORRECTION-7`

**RESULT = PASS for the authorized bounded correction.** Two exact physical source files and a new prospective Snapshot are materialized. Exactly three provenance paths changed; all other native fields and all content/authority/semantic facts are preserved. Native model validation, local replay provenance key/path checks, seventeen negatives and four-seed independent reconstruction pass. Full A14 source/replay/handoff remains blocked by separate missing source bytes.

## Scope authentication

`SELECTED_OPTION = AUTHORIZE_BOUNDED_PROSPECTIVE_A14_PROVENANCE_FIXTURE_CORRECTION`

The explicit current user selection matches Reconciliation 6’s exact option, correction subject and sealed dossier hashes. `SCOPE_AUTHENTICATION = PASS`. The subject is `qualification-A14-provenance-correction-v1:c6cc35ce0f1d0a15fbff354498d76275c4a4ac101bb825996c4c08e820adb863`; dossier identity is `qualification-A14-provenance-correction-v1:9a8a5ecc45083d5a6d64d9f23a30ed2b6cdb9820f6b732ee7ff18c60eadc17e4`. The earlier dossier/template is not edited. This records fixture-correction authorization only; it creates no native execution/INSTALL/P05/schema/authority grant.

## Physical sources and exact correction

- Choice: `docs/plans/qualification/E2_P05_D01_A14_PROSPECTIVE_SOURCE_CORRECTION_1/sources/choice-6bebc233783b5faa0898ecccb20cf51ce529086c74ca672a113450f6e270a411.json`.
- Grant: `docs/plans/qualification/E2_P05_D01_A14_PROSPECTIVE_SOURCE_CORRECTION_1/sources/grant-cddac13f5e0b0f460e5d58a68d4ce753ce43cb5d17481be408d9b5f43d616574.json`.

The files contain the exact compact UTF-8 JSON bytes committed in the authorized dossier, without newline or wrapper. Native RAW pin validation and lookup read those bytes and reproduce the original content digests. The native choice and grant authority identities, permissions, targets, choice/dossier linkage, scope, lineage, generation and all non-path provenance fields are unchanged. Materializing these fixture source bytes does not issue or reissue a choice/grant.

`PROVENANCE_PATH_CHANGES = 3`:

- `/canonical_content/subject/entities/0/provenance/path`.
- `/canonical_content/subject/entities/1/provenance/path`.
- `/canonical_content/subject/knowledge/3/provenance/path`.

The three replacements are applied only to a new prospective subject. Reversing those exact paths makes the entire subject identical to the original. No fourth field differs. The original Snapshot and all 117 capsule artifacts remain untouched. The corrected input is published with its own identity and prospective fixture manifest, rather than copying stale original capsule identities/arguments.

| Identity | Native planner-snapshot-v1 SHA256 |
| --- | --- |
| Original | `91017c3947096a0470ba44aff95901872768fa205205d39c7bf60f840f848c9c` |
| Corrected | `7ec95347f9662731ad5254221c03196fe789eb3435d02947eb09a70077ab66b9` |

`SNAPSHOT_IDENTITY_CHANGED = YES`. This change is solely attributable to the authorized provenance paths. No original historical identity is relabeled.

## Native validation and replay preflight

Unchanged `model.validate_model`, `model.validate_provenance`, `model.unique`, codec Snapshot serialization/identity, native pin/path validation and RAW source lookup validate the corrected fixture. `replay.provenance_records` enumerates the native required provenance set without applying events. Deduplicating repeated identical references yields unique RAW lookup keys; every provenance path is now canonical under the unchanged native validator. Choice and grant resolve to different physical files with their exact content identities.

All required provenance pin **requirements** are inventoried, but all physical source bytes are **not** present. Native lookup of `E2-DECIDE.json` under the existing declared repository source root reports `pinned source unavailable`; it is the first remaining blocker in native provenance traversal. Other legacy Action/source/route files are also unavailable. Correcting their bytes, roots, policy or history is outside the selected authorization.

Local replay-contract preflight now passes the duplicate RAW-key and noncanonical-path conditions. Complete native bundle replay is not run: no exact complete authorized bundle/policy/history input exists. No placeholder bundle, empty ledger, borrowed policy or report-as-bundle is supplied to force replay. There is no A14 operation, native result application, save_bundle/restore call or save/cold-reader transaction.

## Negatives and determinism

Seventeen static fixture negatives reject shared paths/duplicate keys, changed bytes, changed content/authority IDs, changed decision/grant semantics, noncanonical paths, reciprocal source substitution, missing sources, a fourth changed path, retention of the old Snapshot identity and historical rewrite. Negative candidates are isolated in-memory records; published fixtures and historical files are not altered.

Fresh structural readers under PYTHONHASHSEED 0, 1, 7 and 101 reconstruct paths independently by existing choice/grant roles and identities, compare all corrected fields, validate native model/identity and reread the exact source bytes. All return the same corrected Snapshot and provenance semantic identity. These are metadata/structural verification processes, not qualification cold readers. Existing 52 bindings are independently revalidated unchanged.

## Operand and handoff frontier

`PREVIOUSLY_RESOLVED = 52`; `RESOLVED_BY_CORRECTION = 0`; `TOTAL_RESOLVED = 52`; `TOTAL_UNRESOLVED = 59`; total = 111. All 16 A14-dependent unresolved references remain. The new Snapshot identity uniquely identifies the corrected input but does not supply missing bundle, save identity, reader source or N02 mutation operands.

`NEXT_A14_BLOCKER = OTHER_DECLARED_RAW_SOURCE_FILES_UNAVAILABLE_AT_EXISTING_SOURCE_ROOT`, first native lookup `E2-DECIDE.json`.

The static handoff frontier is updated to the corrected fixture association. Its former duplicate-key/noncanonical-path contradiction is removed for this version, while other source/policy/history closure and save-to-reader transfer remain blocked. No unrelated gap is repaired. Another bounded decision dossier is not ready because an exact unique correction for those sources/root/policy/history has not been specified. The present authorization is not reused for that work.

## Report

| Field | Result |
| --- | --- |
| SCOPE_AUTHENTICATION | PASS |
| CHOICE_BYTES_PRESERVED | PASS |
| GRANT_BYTES_PRESERVED | PASS |
| CONTENT_IDENTITIES_PRESERVED | PASS |
| AUTHORITY_IDENTITIES_PRESERVED | PASS |
| SEMANTIC_FACTS_PRESERVED | PASS |
| PROVENANCE_PATH_CHANGES | 3 |
| RAW_PIN_KEYS_UNIQUE | PASS |
| PATHS_CANONICAL | PASS |
| NATIVE_STRUCTURAL_VALIDATION | PASS |
| REPLAY_PREFLIGHT | Local key/path/source A/B PASS; other source closure BLOCKED; full bundle replay NOT_RUN |
| NEGATIVE_SUITE | 17/17 rejected |
| DETERMINISM | PASS: seeds 0/1/7/101 |
| TOTAL_RESOLVED / TOTAL_UNRESOLVED | 52 / 59 |
| END_INTERFACES_BOUND | 4/6 |
| P05_EXECUTION_READY | NO |
| E1_ARTIFACTS_MODIFIED | 0 |
| PRODUCTION_EFFECT | NO |

## Artifacts and preservation

Corrected prospective fixture artifacts and verification records are under `qualification/E2_P05_D01_A14_PROVENANCE_FIXTURE_CORRECTION_7/`: scope authentication, corrected native Snapshot, prospective fixture manifest, exact semantic/path preservation, native structural/replay preflight, physical-source checks, 16-reference frontier, negatives, determinism and preservation. The two source files are at the exact paths sealed by Reconciliation 6.

All pre-existing adapter/docs file hashes remain unchanged, including the original historical fixture, native implementations, frozen E1, all 117 capsules and 52 bindings. Historical UNPROVEN/UNRECOVERED labels remain. P05 stage bindings stay 13/13 and END stays 4/6; E2-D01 stays BLOCKED.

`A14_EXECUTED = NO`; `D01_QUALIFICATION_CASES_EXECUTED = 0`; `SAVES_PERFORMED = 0`; `COLD_READERS_EXECUTED = 0`; `MUTATIONS_APPLIED = 0`; `INVALIDATIONS_APPLIED = 0`; `ORIGINAL_HISTORICAL_FIXTURE_MODIFIED = NO`; `FULL_OUTPUT_ORACLES = 0/128`; `P05_EXECUTED = NO`; `P06_EXECUTED = NO`; `INSTALL_EVENTS = 0`; `NEW_AUTHORITIES = 0`; `E1_ARTIFACTS_MODIFIED = 0`; `PRODUCTION_EFFECT = NO`; `git diff --check = PASS`. Authorized path-only substitutions belong to prospective fixture construction, not native mutation/invalidation transitions.
