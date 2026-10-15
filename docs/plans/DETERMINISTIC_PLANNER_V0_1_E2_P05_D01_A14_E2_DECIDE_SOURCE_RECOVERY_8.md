# E2-P05 D01 A14 E2-DECIDE source-bytes recovery 8

`WORK_PACKAGE = E2-P05-D01-A14-E2-DECIDE-SOURCE-RECOVERY-8`

**RESULT = PASS for source-byte recovery.** The exact required 90-byte source is retained losslessly in authoritative provenance strings. No standalone original file was found. An isolated evidence copy matches the original RAW identity and validates natively. Accepted integration at the A14 source root remains behind an exact, unselected bounded decision. No Snapshot or accepted source is changed.

## Source contract and assurance

`E2-DECIDE.json` is the scoped authored **Action-definition provenance envelope**, with exactly `action`, `lineage`, and `scope` string fields. It identifies E2-DECIDE/E2-CANONICAL-BASELINE-1/E2-QUALIFICATION-ONLY. Generation comes from the consuming EvaluationContext: E2-GENERATION-1. It is not the complete native Action definition, a decision input, a RecordedDecision command, authenticated choice, USE grant, or policy.

The Action.source Provenance uses method E2-PC01-WHOLE-MODEL-1, section `/`, and CONTENT_IDENTITY/raw-file-sha256. Native replay requires that source in its pin inventory; codec.load_pinned authenticates the complete raw bytes. Equal decoded JSON is insufficient. Expected identity/hash:

`raw-file-sha256:030cd5b248c3de5a89b512d8e044a1520462cc2fb558f2ff1711f8a84034401e`

Exact byte count: **90**, with no newline.

## Retained and embedded searches

The repository search enumerated 17518 retained files through rg --files -uu, excluding .git internals, symlinks and this new package. Every extension was considered for an exact whole-file hash at the required size. Source/document text extensions were searched for filename, expected digest, raw body and base64; matching JSON containers were decoded and walked for provenance references and literal embedded bytes. Search scope and parse limitations are recorded rather than hidden.

No exact standalone E2-DECIDE.json bytes were retained. 128 matching lossless JSON strings were found. All matching source references/pins and their container pointers are recorded in retained-references.json and embedded-source-search.json, including Snapshot/bundle/manifest/invocation representations. Copies are not independent occurrences.

The primary source is Correction 7’s exact native Action.source.excerpt. The original PC01 `_source` writer computes raw=codec.canonical_bytes(body), writes exactly raw, hashes exactly raw, and stores raw.decode() in the excerpt. Thus decoding the retained JSON string and encoding UTF-8 recovers the original source byte value without inference from Action semantics. The recovered hash matches the expected pin.

`RECOVERY_CLASSIFICATION = LOSSLESS_EMBEDDED_SOURCE`; `LOSSLESS_BYTE_RECOVERY = YES`.

The original canonical serializer independently corroborates all bytes: sorted keys action/lineage/scope, compact comma/colon separators, UTF-8, ensure_ascii=False, native constrained JSON number rules, no trailing newline, and exactly three string-valued fields. This is not unverified regenerated JSON. The recovery uses literal embedded bytes first.

## Isolated recovery and validation

Candidate: `qualification/E2_P05_D01_A14_E2_DECIDE_SOURCE_RECOVERY_8/candidates/E2-DECIDE.json`.

Native codec.parse_json validates the plain source object and closed string-valued field set; unchanged native RAW pin/path validation and load_pinned verify exact bytes and identity at the isolated evidence path. No native Action/RecordedDecision decode is asserted for this envelope. Semantically equivalent native Actions, commands and choice/grant payloads are inventoried separately and rejected as byte replacements.

HISTORICAL_SOURCE_RETAINED is **NO for the original standalone physical file**, while HISTORICAL_RAW_BYTE_CONTENT_RETAINED is **YES in lossless embedded form**. The newly written isolated evidence copy is prospective extraction of identical bytes. It is not proof the original physical file survived or that any historical operation was executed.

## Scope and decision boundary

Correction 7’s selected dossier authorizes only its two choice/grant source files and three provenance substitutions. It does not cover another accepted physical source at the active A14 root. The current package authorizes isolated recovery evidence; accepted materialization is explicitly conditional on applicable scope. Therefore the two NO_NEW_DECISION paths do not establish accepted integration here: no standalone exact file was found, and this source recovery is outside the selected A/B correction.

`DECISION_REQUIRED = YES`; `DECISION_READY = YES`. The bounded-source-decision-dossier.json pins the exact 90 bytes/hash, authoritative embedded pointer, existing provenance, corrected Snapshot identity, and proposed existing canonical path `E2-DECIDE.json` under the declared repository root. Options:

- `AUTHORIZE_BOUNDED_A14_E2_DECIDE_LOSSLESS_SOURCE_MATERIALIZATION`.
- `DECLINE_E2_DECIDE_SOURCE_MATERIALIZATION`.

No option is selected. The proposal changes no source/provenance identity or path, authority, native schema or Snapshot field. It excludes repinning, unrelated sources/root/policy/history, installation, A14/D01 execution, save/reader, output oracles and END binding. A byte-identical copy under the existing expected path would leave the Snapshot identity unchanged; no copy is accepted here.

## Frontier and verification

Correction 7 Snapshot remains `planner-snapshot-v1:7ec95347f9662731ad5254221c03196fe789eb3435d02947eb09a70077ab66b9`. Native Snapshot/model validation and identity checks pass unchanged. Static lookup at the actual fixture root still returns `pinned source unavailable` for E2-DECIDE.json; the isolated candidate directory is not substituted as a new source root. The first blocker is accepted source materialization authority/integration. No later source is repaired or declared the active frontier.

`PREVIOUSLY_RESOLVED = 52`; `RESOLVED_BY_E2_DECIDE = 0`; `TOTAL_RESOLVED = 52`; `TOTAL_UNRESOLVED = 59`.

Four fresh processes under seeds 0, 1, 7 and 101 reproduce the exact bytes/hash and unchanged corrected fixture identity, and revalidate all 52 bindings. Fourteen static negatives reject wrong bytes, semantic-equal byte-different JSON, wrong hash/domain/path/encoding/newline, report/RecordedDecision/choice/grant substitution, unverified regeneration and false historical-retention claims. No native save/cold-reader operation or qualification case is executed.

## Report

| Field | Result |
| --- | --- |
| EXPECTED_BYTE_HASH / BYTE_HASH | 030cd5b248c3de5a89b512d8e044a1520462cc2fb558f2ff1711f8a84034401e |
| LOSSLESS_BYTE_RECOVERY | YES |
| RECOVERY_CLASSIFICATION | LOSSLESS_EMBEDDED_SOURCE |
| HISTORICAL_SOURCE_RETAINED | NO physical file; YES embedded byte content |
| PROSPECTIVE_REPRODUCTION | YES isolated identical extraction copy |
| DECISION_REQUIRED / DECISION_READY | YES / YES; unselected |
| SOURCE_VALIDATION | PASS isolated candidate; not accepted fixture input |
| SNAPSHOT_IDENTITY_CHANGED | NO |
| TOTAL_RESOLVED / TOTAL_UNRESOLVED | 52 / 59 |
| E1_ARTIFACTS_MODIFIED | 0 |
| PRODUCTION_EFFECT | NO |

## Artifacts and preservation

Supporting machine records and metadata-only scripts are under `qualification/E2_P05_D01_A14_E2_DECIDE_SOURCE_RECOVERY_8/`: source contract, exhaustive file manifest, exact-file and embedded search, retained references, canonical serialization rules, isolated candidate/hash validation, semantic candidates, bounded subject/dossier, 14 negatives, four-seed determinism, unchanged frontier and preservation.

All pre-existing adapter/docs files retain their baseline hashes. Original artifacts, corrected A14 fixture, 52 bindings and frozen E1 are unchanged. All historical UNPROVEN labels and original D01 matrix UNRECOVERED status remain.

`A14_EXECUTED = NO`; `D01_QUALIFICATION_CASES_EXECUTED = 0`; `SAVES_PERFORMED = 0`; `COLD_READERS_EXECUTED = 0`; `FULL_OUTPUT_ORACLES = 0/128`; `END_INTERFACES_BOUND = 4/6`; `P05_EXECUTED = NO`; `P06_EXECUTED = NO`; `ORIGINAL_ARTIFACTS_MODIFIED = NO`; `NEW_AUTHORITIES = 0`; `INSTALL_EVENTS = 0`; `N_REAL_SATISFIED = NO`; `E1_ARTIFACTS_MODIFIED = 0`; `PRODUCTION_EFFECT = NO`; `git diff --check = PASS`.
