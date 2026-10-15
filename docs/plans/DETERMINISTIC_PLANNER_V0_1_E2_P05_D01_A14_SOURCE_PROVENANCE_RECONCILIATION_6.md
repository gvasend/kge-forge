# E2-P05 D01 A14 source/provenance contract reconciliation 6

`WORK_PACKAGE = E2-P05-D01-A14-SOURCE-PROVENANCE-RECONCILIATION-6`

**RESULT = PASS for contract reconciliation only.** The conflict is a qualification materializer/fixture representation defect. Source A is authenticated choice content; source B is the bounded USE-grant content derived from that choice. Existing native provenance fields can represent them as two distinct physical sources without weakening key/path validation. The exact minimum correction and its assurance effects are specified in an **unselected** bounded dossier.

No Snapshot/source is rewritten, source file materialized, authority issued, operand resolved, A14 executed, runtime result saved, qualification reader launched, or output oracle constructed. Counts remain **52 resolved / 59 unresolved**. A14 handoff remains non-executable.

## Exact source semantics

| Term | Source A | Source B |
| --- | --- | --- |
| Content identity | raw-file-sha256:6bebc233783b5faa0898ecccb20cf51ce529086c74ca672a113450f6e270a411 | raw-file-sha256:cddac13f5e0b0f460e5d58a68d4ce753ce43cb5d17481be408d9b5f43d616574 |
| Native content domain | CONTENT_IDENTITY | CONTENT_IDENTITY |
| Semantic role | Authenticated ALLOW_QUALIFICATION_MAPPING choice for E2-DECIDE | Derived E2-GRANT, USE permission for E2-REENTER |
| Provenance method | E2-T03-AUTHENTICATED-CHOICE-1 | E2-T03-QUALIFICATION-GRANT-1 |
| Existing section | /choice | /grant |
| Native authority domain | AUTHORITY_IDENTITY/e2-choice-record with same content digest | AUTHORITY_IDENTITY/e2-grant with same content digest |

Both name `qualification://E2-P02-human-decision`. Choice provenance occurs on the native choice entity and accepted decision-choice KnowledgeRecord; grant provenance occurs on the E2-GRANT entity. Native replay independently includes all of these in required provenance coverage. The Snapshot source/pointers and full payloads are pinned in conflicting-source-semantics.json.

T03’s `_digest` hashes compact sorted-key UTF-8 JSON. Parsing the retained excerpts and applying that exact rule reproduces both content digests; hashing the spaced excerpt text itself is not the rule. Grant payload B explicitly contains `choice = A.sha256`, matching dossier, scope and lineage; it has USE permission and a different subject. Thus the primary relationship is **SOURCE_AND_DERIVED_ARTIFACT**, with two distinct content sources. They are neither duplicate history nor the same content viewed through different identity domains. Authority IDs remain separate from raw content IDs.

## Key, path and representation classification

The authoritative implementation key is `(ArtifactPin.path, ArtifactPin.pointer, HashProfile)`. RAW pointer must be empty and profile/domain must be raw-file-sha256. Digest, semantic role, source type and Provenance.section do not add lookup coordinates. Duplicate RAW keys would require one immutable byte object to authenticate two different hashes. The rule protects unambiguous lookup and deterministic identity-bound replay; preventing laundering is a consequence of these checks. No reason to relax it was recovered.

The native path rule requires a nonempty canonical relative POSIX path under one source root, excludes traversal and symlink aliases, and supports no qualification URI resolver. The lexical POSIX form of the old URI is `qualification:/E2-P02-human-decision`, but that spelling provides no unique semantic physical source and leaves the raw-key collision intact. Canonicalization alone is insufficient.

The URI was introduced by T03 `_raw_provenance` as logical qualification notation and embedded in native historical Snapshot provenance. It is not merely a display path in a report. The Snapshot preserves the separate payload identities and existing /choice and /grant roles. Flattening occurs in their shared physical-locator assignment, not in loss of the payload distinction. The choice/grant semantics are defined, but their source-persistence representation is invalid. This is not a generic native provenance schema gap.

`PRIMARY_CLASSIFICATION = COMBINED_FIXTURE_PROVENANCE_KEY_COLLISION_AND_NONCANONICAL_SOURCE_PATH`

`NATIVE_MODEL_CAN_REPRESENT_INTENT = YES`; `NATIVE_CAPABILITY_CHANGE_REQUIRED = NO`.

## Minimum proposed correction

Keep both exact compact JSON payloads and their recorded content identities. Use two canonical relative physical source paths, derived from the already-authoritative choice/grant roles and content digests:

- `docs/plans/qualification/E2_P05_D01_A14_PROSPECTIVE_SOURCE_CORRECTION_1/sources/choice-6bebc233783b5faa0898ecccb20cf51ce529086c74ca672a113450f6e270a411.json`.
- `docs/plans/qualification/E2_P05_D01_A14_PROSPECTIVE_SOURCE_CORRECTION_1/sources/grant-cddac13f5e0b0f460e5d58a68d4ce753ce43cb5d17481be408d9b5f43d616574.json`.

The correction contract binds exactly three provenance.path assignments: both A occurrences and the B occurrence. It preserves section, method, excerpt, scope, content IDs, semantic authority IDs, payload/dossier/choice linkage, permission, validity, lineage/generation and every other Snapshot field. Each file contains only the exact compact payload bytes, without a newline or wrapper; RAW ArtifactPin.pointer stays empty. The existing /choice and /grant section annotations remain descriptive provenance roles, not RAW JSON projections. No materializer choice/grant function is rerun.

Changing a native provenance path changes the Snapshot and any affected bundle/event identities. Therefore this is **FIXTURE_CORRECTION**, with an explicit prospective representation label and bounded authorization; it is not an automatically authorized normalization of the historical artifact. Original Snapshot 91017c39… remains immutable and cannot be relabeled as the corrected input. No new native ID is computed in this package.

Contract identity: `qualification-A14-provenance-correction-v1:c6cc35ce0f1d0a15fbff354498d76275c4a4ac101bb825996c4c08e820adb863`.

This local correction does not claim other missing source files, exact policy, complete ledger/history, source root or cold-reader handoff are solved. Those remain independently required.

## Correction candidates and assurance

| Candidate | Classification | Disposition |
| --- | --- | --- |
| Normalize the URI spelling only | Representation normalization candidate | Insufficient: duplicate RAW key remains; Snapshot identity still changes |
| Separate exact choice/grant physical sources | Fixture correction | Minimum supported local correction; content and authority facts preserved; new native fixture identities |
| Author a complete new governed-unknown A14 source fixture | Qualification scope replacement | Supported broader path, requires explicit scope; not the minimum selected proposal |
| Add role-key/URI-loader semantics | Native model change | Not justified; existing fields already represent the intended sources |
| Publish changed content under old Snapshot identity | Historical rewrite | Unacceptable identity/provenance laundering |

Prior P03 scope dossiers explicitly distinguish separate choice/grant physical sources and prospective fixtures from the unchanged original checkpoint. They provide precedent, not transferable authorization for the D01 A14 correction. The proposed correction preserves A14 behavior, source-currentness and identity-domain distinctions, N12 selection/history and N13 prospective/actual exclusions. It neither proves original historical bundle/occurrence nor substitutes an approved END qualification.

## Obligation and operand impact

Eight direct/transitive frozen obligation rows have an explicit A14 source boundary:

- `D01-OBL:E2-A14_OPERANDS`.
- `D01-OBL:E2-A14_ORACLE`.
- `D01-OBL:E2-A16_OPERANDS`.
- `D01-OBL:E2-A16_ORACLE`.
- `D01-OBL:E2-N01_OPERANDS`.
- `D01-OBL:E2-N01_ORACLE`.
- `D01-OBL:E2-N02_OPERANDS`.
- `D01-OBL:E2-N02_ORACLE`.

A14 supplies the governed-unknown baseline; A16 consumes its restored route; N01/N02 consume copies before missing/malformed-route negatives. Six existing capsule associations use the exact old governed-unknown file (A14/A16/N01); N02’s current later known-rule capsules remain a boundary conflict. Their eight rows are normative dependencies, not evidence that those capsules were corrected here. Cross-cutting cold-reader, permutation, full-comparison and scope requirements remain unchanged and must bind the future source explicitly.

All 16 unresolved A14-dependent operand occurrences are mapped to the proposal without being resolved. New source/bundle/reader identities and boundary associations require future authorized construction and independent validation. The 52 resolved bindings remain byte/semantically identical.

## Replay oracle and negatives

The replay contract requires all provenance pins, unique canonical RAW keys, exact A/B hashes and roles, B-to-A/dossier/scope/lineage linkage, separate native identity domains, deterministic physical lookup, preserved ordered history, explicit new native IDs, and no pin omission, source collapse, authority creation or historical relabeling. Full source/policy closure still applies.

Fifteen static correction-contract negatives reject duplicate keys, missing A/B, reciprocal source substitution, wrong role/domain/path, canonical path drift, traversal/alias, source omission/collapse, historical relabeling, laundering and silent application. The positive check validates an unselected correction specification; it is not native replay, corrected-source materialization or A14 execution. Independent verification reconstructs payload hashes/role linkage and rechecks all existing 52 bindings.

## Bounded decision

`DECISION_REQUIRED = YES`; `DECISION_READY = YES` for the local fixture correction subject only.

Options in bounded-correction-decision-dossier.json:

- `AUTHORIZE_BOUNDED_PROSPECTIVE_A14_PROVENANCE_FIXTURE_CORRECTION`.
- `DECLINE_A14_PROVENANCE_CORRECTION`.

No option is selected. The decision subject binds the exact base Snapshot/pins, two byte commitments, role paths, three path-only assignments, unchanged-field contract, historical exclusions, replay assurance and affected obligations/operands. It would permit a new versioned prospective fixture; it excludes editing the original, issuing/reissuing authority, native-rule changes, A14/runner execution, runtime saves/readers, full-output oracles and END binding. Complete prospective D01 execution-scope readiness remains NO.

`A14_SOURCE_RECONCILIATION_READY = YES` means the exact local correction is specified. It does not mean the corrected source exists, its full closure passes, or the A14 handoff is executable.

## Report and preservation

`RESOLVED_OPERANDS = 52`; `UNRESOLVED_OPERANDS = 59`; `A14_OPERAND_IMPACT = 16`; `A14_EXECUTED = NO`; `SAVES_PERFORMED = 0`; `COLD_READERS_EXECUTED = 0`; `FULL_OUTPUT_ORACLES = 0/128`; `END_INTERFACES_BOUND = 4/6`; `NATIVE_STATE_CHANGED = NO`; `E1_ARTIFACTS_MODIFIED = 0`; `PRODUCTION_EFFECT = NO`; `git diff --check = PASS`.

All pre-existing adapter/docs file hashes are unchanged, including original source/Snapshot, 117 capsules, native key/path implementations and all 52 bindings. No choice, grant, authority, Evidence, receipt, event or native bundle is created. Historical UNPROVEN and original D01 matrix UNRECOVERED labels remain. P05/P06 are not executed.

All machine-readable evidence is under `qualification/E2_P05_D01_A14_SOURCE_PROVENANCE_RECONCILIATION_6/`: source semantics; native key/path contract; correction candidates and exact minimum contract; eight-obligation and 16-operand impacts; replay oracle contract; unselected bounded dossier; independent verification; static negatives; preservation; and metadata-only recovery/check/report scripts.
