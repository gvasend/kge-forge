# E2-P05 D01 A14 E2-PREPARE source-bytes recovery 18

**RESULT = PASS for source recovery and an unselected bounded decision dossier.** The exact 91-byte value survives losslessly in authoritative provenance. No standalone source copy was found. E2-PREPARE.json and later missing sources remain absent; accepted materialization requires a new decision.

E2-PREPARE.json is the scoped authored source marker for the E2-PREPARE decision-input-acquisition Action. The same provenance also belongs to its E2-K-PREPARE accepted-inventory and existing Snapshot KnowledgeRecord. Three corrected Snapshot occurrences share one identical RAW pin. The file is plain JSON with exactly action, lineage and scope; it is not a complete native Action/KnowledgeRecord, validation result, event, E2-DECIDE, source.json acquisition premise, choice, grant, route or policy. The already-retained Snapshot knowledge and declared inventory are inspected; no new PREPARE occurrence or knowledge admission occurs here.

`EXPECTED_PATH = E2-PREPARE.json` under `/home/gvasend/app/kge-forge`.

`EXPECTED_SIZE = RECOVERED_BYTE_LENGTH = 91`

`EXPECTED_SHA256 = RECOVERED_SHA256 = 0a1daaa24eea752c83ed20aad3f7756b72e2e6b76b7e0c4c2033e5f6a9bc0f99`

Identity domain: CONTENT_IDENTITY/raw-file-sha256. Provenance method: E2-PC01-WHOLE-MODEL-1. Scope: E2-QUALIFICATION-ONLY; lineage: E2-CANONICAL-BASELINE-1; generation: E2-GENERATION-1.

Exact retained byte value:

```json
{"action":"E2-PREPARE","lineage":"E2-CANONICAL-BASELINE-1","scope":"E2-QUALIFICATION-ONLY"}
```

The displayed code fence is explanatory; the actual isolated candidate is exactly 91 UTF-8 bytes without a newline, at candidates/recovered-source-bytes.bin. Native RAW lookup requires the entire physical byte hash. Semantically equivalent JSON with changed whitespace/order is insufficient.

Repository search examined 17720 retained files, excluding .git, symlinks and this new package. Every extension was considered for exact-size file hashing; listed source/document text extensions were searched for path/hash/raw/base64 mentions and JSON pointers. There are 0 exact standalone matches, 270 matching lossless UTF-8 string values and 1441 reference records. All concrete candidate records retain separate container paths/pointers and match the full A14 pin; there is one byte-equivalence class. Search limits are explicit in the manifest.

The strongest recovery pointer is `docs/plans/qualification/E2_P05_D01_A14_PROVENANCE_FIXTURE_CORRECTION_7/corrected-prospective-snapshot.json#/snapshot/actions/5/source/excerpt`. This is an unchanged native Provenance.excerpt, not a report summary. The original PC01 writer calls codec.canonical_bytes(body), writes raw bytes and stores raw.decode() in Provenance. The writer source and serializer are pinned; AST inspection confirms the calls without executing the constructor. JSON-string decoding followed by UTF-8 encoding is lossless for this original raw.decode() value.

Canonical serialization is also specified: exactly three string fields action/lineage/scope, sorted keys, compact comma/colon separators, ensure_ascii=False, UTF-8, allow_nan=False and no terminating newline. Independent serialization matches the retained bytes, but the recovery classification is LOSSLESS_EMBEDDED_SOURCE because retained raw text already suffices. No byte reconstruction from a semantic report is accepted. Original raw-byte content is retained; original standalone-file retention is not established.

Native plain-JSON decode, isolated RAW pin lookup, Provenance validation and Snapshot/model validation pass. The expected path passes unchanged native canonical-path rules. Materializing these exact bytes at the already-pinned path would require no repinning, path/provenance/content identity change, authority change or Snapshot field change.

`EXPECTED_SNAPSHOT_ID_BEFORE = EXPECTED_SNAPSHOT_ID_AFTER = planner-snapshot-v1:7ec95347f9662731ad5254221c03196fe789eb3435d02947eb09a70077ab66b9`

`EXPECTED_SNAPSHOT_EFFECT = UNCHANGED`. This is a static expectation, not an accepted materialization result or full bundle replay qualification.

`DECISION_REQUIRED = YES`; `DECISION_READY = YES`. The ready dossier proposes AUTHORIZE_BOUNDED_A14_E2_PREPARE_LOSSLESS_SOURCE_MATERIALIZATION or DECLINE_E2_PREPARE_MATERIALIZATION and remains NOT_SELECTED. It pins the exact bytes/hash, authoritative recovery pointer, root/path, all three existing provenance occurrences, content identity, unchanged Snapshot effect and exclusions. Subject identity: `qualification-A14-E2PREPARE-materialization-v1:a6d8a9c5084d8d14d9bf5687e80ccef50128d0e94f7f847615c066021824ee9e`. Prior choice/grant, E2-DECIDE and source.json grants are not reused. No later-source dossier or bundled source authority is prepared.

The informational native source frontier has 10 unique physical RAW pins, 8 present with matching native pins and 2 missing. Order is first occurrence in native replay.provenance_records, with identical RAW keys deduplicated. Every inventory row contains only path, expected identity/hash, presence, first lookup order and directly available role. Missing order:

1. E2-PREPARE.json
2. resolution.json

Later missing sources were checked for availability only. Their bytes were not recovered, decoded into replacement fixtures or materialized. No decision dossier was created for them. The first physical blocker remains E2-PREPARE.json; the recovery package’s next action blocker is E2_PREPARE_MATERIALIZATION_AUTHORIZATION.

Historical/current PREPARE comparison is independently sealed against three named later checkpoints: the P03 prospective checkpoint, P04 final pre-execution configuration and P04 canonical target. The entire retained native Action inventory contains 1,431 PREPARE occurrences grouped into 17 exact native-body/context variants. Every group retains its original paths/pointers, full inputs/outputs/dossier/inventory/result contract, dependencies, context and source identity, and receives an explicit classification. These inventories are comparison evidence only, never a selected replacement or execution result.

The A14 Action is DECISION_INPUT_ACQUISITION, gated by completed E2-CHECK and E2-COLLECT. Its accepted inventory names E2-K-PREPARE; its prepared DecisionDossier belongs to E2-DECIDE and requires E2-KP-CHECK / E2-KP-COLLECT. Dossier/check provenance is separately pinned to PC01_SOURCES, not the three-field E2-PREPARE marker. Later P03/P04 definitions overlap in operation, action/knowledge IDs and gates but use prospective authored source and dossier/inventory provenance, E2-P03-PROSPECTIVE-QUALIFICATION-1 lineage and E2-P03-PROSPECTIVE-GENERATION-1 generation. All compared scope values remain E2-QUALIFICATION-ONLY. Exact full field comparisons are machine-readable.

HISTORICAL_CURRENT_RELATIONSHIP = DIFFERENT_VERSION; CURRENT_PREPARE_SUBSTITUTION_ALLOWED = NO. The later physical source mainline-source-06.json is 780 bytes with raw SHA256 8bf34241624ae07559203a278855c08626aabd3eedf6675d27a64a2a6f6b0236, while A14 requires the 91-byte marker with hash 0a1daaa24eea752c83ed20aad3f7756b72e2e6b76b7e0c4c2033e5f6a9bc0f99. Nested template provenance can retain exact A14 text without making the outer wrapper byte-identical. Historical identical-source groups are recorded separately from later different versions; no Action object or semantic summary substitutes for physical RAW bytes.

Sixteen normative A14-dependent references require the complete corrected Snapshot source/bundle closure. They include bundle/save/reader inputs and transitive N02 unknown-rule-boundary dependencies. Recoverable bytes are not complete invocation operands, and no reference is promoted. RESOLVED_OPERANDS = 52; UNRESOLVED_OPERANDS = 59; total = 111. The existing 52 bindings were reconstructed unchanged by the fresh verification chain.

Four fresh structural reader processes under hash seeds 0, 1, 7 and 101 independently reproduce the recovered bytes/hash/content identity, existing provenance and Snapshot identity, and confirm the unselected decision subject. Static in-memory fail-closed negatives reject byte-different/semantic-equal JSON, wrong hash/domain/path/root/candidate, lossy representation, report and other-source substitution, unverified regeneration, unauthorized materialization, hidden repinning and later-source materialization under E2-PREPARE scope. These processes do not invoke qualification cases or save/restore.

| Report field | Value |
| --- | --- |
| WORK_PACKAGE | E2-P05-D01-A14-E2-PREPARE-SOURCE-RECOVERY-18 |
| RESULT | PASS |
| EXPECTED_PATH | E2-PREPARE.json |
| EXPECTED_SHA256 | 0a1daaa24eea752c83ed20aad3f7756b72e2e6b76b7e0c4c2033e5f6a9bc0f99 |
| RECOVERED_BYTE_LENGTH | 91 |
| LOSSLESS_BYTE_RECOVERY | YES |
| RECOVERY_CLASSIFICATION | LOSSLESS_EMBEDDED_SOURCE |
| HISTORICAL_CURRENT_RELATIONSHIP | DIFFERENT_VERSION |
| CURRENT_PREPARE_SUBSTITUTION_ALLOWED | NO |
| SOURCE_PINS_TOTAL | 10 |
| SOURCE_PINS_PRESENT | 8 |
| SOURCE_PINS_MISSING | 2 |
| MATERIALIZATION_REQUIRES_REPIN | NO |
| DECISION_REQUIRED | YES |
| DECISION_READY | YES |
| E2_PREPARE_DEPENDENT_REFERENCES | 16 |
| RESOLVED_OPERANDS | 52 |
| UNRESOLVED_OPERANDS | 59 |
| NEXT_BLOCKER | E2_PREPARE_MATERIALIZATION_AUTHORIZATION |
| E2_PREPARE_MATERIALIZED | NO |
| A14_EXECUTED | NO |
| D01_CASES_EXECUTED | 0 |
| END_INTERFACES_BOUND | 4/6 |
| E1_ARTIFACTS_MODIFIED | 0 |
| PRODUCTION_EFFECT | NO |

All 17195 pre-existing baseline files remained unchanged, including the accepted source.json/E2-DECIDE sources, separate choice/grant sources, current corrected Snapshot, 117 capsules, 52 bindings, frozen E1 and native implementation. No output oracle, native runtime state, event, receipt, bundle or authority was created. P05 stage bindings remain 13/13 and END remains 4/6; historical UNPROVEN/UNRECOVERED claims remain unchanged.

`SAVES_PERFORMED = 0`; `COLD_READERS_EXECUTED = 0`; `FULL_OUTPUT_ORACLES = 0/128`; `P05_EXECUTED = NO`; `P06_EXECUTED = NO`; `NATIVE_STATE_CHANGED = NO`; `INSTALL_EVENTS = 0`; `NEW_AUTHORITIES = 0`; `N_REAL_SATISFIED = NO`; `git diff --check = PASS`.

The [JSON companion](DETERMINISTIC_PLANNER_V0_1_E2_P05_D01_A14_E2_PREPARE_SOURCE_RECOVERY_18.json) pins supporting evidence under [the recovery directory](qualification/E2_P05_D01_A14_E2_PREPARE_SOURCE_RECOVERY_18/). The [bounded decision dossier](qualification/E2_P05_D01_A14_E2_PREPARE_SOURCE_RECOVERY_18/bounded-source-decision-dossier.json) remains unselected.
