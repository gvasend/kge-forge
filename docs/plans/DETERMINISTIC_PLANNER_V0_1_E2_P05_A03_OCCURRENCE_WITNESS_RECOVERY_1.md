# Deterministic Planner v0.1 — E2-P05 A03 occurrence-witness recovery 1

**RESULT = BLOCKED. PRIMARY_CLASSIFICATION = IRRECOVERABLE_HISTORICAL_WITNESS. LOSSLESS_RECOVERY = NO.** No acceptable native CHECK/COLLECT occurrence witness was found in the retained authoritative inputs. This classification is bounded to those inputs: it does not prove that no transient event ever existed, that an event was never published in an unavailable process, or that particular historical files were deleted. It establishes that the required witness cannot be recovered from the records available here.

The [machine-readable companion](DETERMINISTIC_PLANNER_V0_1_E2_P05_A03_OCCURRENCE_WITNESS_RECOVERY_1.json) records the recovered contract, searches, candidate classifications, lossless-recovery assessment, scope-decision structure and preservation. Evidence is under [qualification/E2_P05_A03_OCCURRENCE_WITNESS_RECOVERY_1](qualification/E2_P05_A03_OCCURRENCE_WITNESS_RECOVERY_1/). P05 remains **9/13 bound**, with `E2-A03.native_result_event_trace` still the first missing input. No graph binding was changed and no downstream binding rerun was performed.

The earliest governing A03 declaration is [the canonical acceptance matrix, A03](DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_ACCEPTANCE_MATRIX_1.md:33), mirrored by case index 2 in the [canonical experiment JSON](DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_EXPERIMENT_1.json). Its purpose is **bounded execution and accepted knowledge**. Its initial condition is a selected acquisition Action with an independently specified output contract; its operation is **record_result/append_event with supplied bounded result**. Only declared knowledge may be accepted; stale/missing outputs cannot complete current prerequisites, and PASS alone cannot resolve root or slot. It requires canonical before/after identities and an event trace. The [plan](DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_EXPERIMENT_1.md:70) assigns construction, selection/results and the subsequent dossier/decision/wait stages to **E2-P02**.

The exact native Actions are E2-CHECK and E2-COLLECT, with permitted PASS outputs E2-K-CHECK and E2-K-COLLECT. [PC01 source declarations](DETERMINISTIC_PLANNER_V0_1_E2_PC01_SOURCES.json) classify CHECK as DETERMINISTIC_VALIDATION and COLLECT as SOURCE_ACQUISITION; both are NON_EFFECTING, qualification-only, with empty authority declarations. “Acquisition” describes their role in obtaining the preparation inputs, not an instruction to change CHECK's native operation class. This A03 check/result is not A10's persisted ValidationResult/support transaction.

The final authoritative [P02 retry 4 PASS](DETERMINISTIC_PLANNER_V0_1_E2_P02_RETRY_4_RESULT.json) consumes the accepted acquisition prefix retained in [retry 3](DETERMINISTIC_PLANNER_V0_1_E2_P02_RETRY_3_RESULT.json). Its reported sequence is:

| Action / permitted output | Reported pre-state SHA256 | Reported post-state SHA256 |
|---|---|---|
| CHECK / E2-K-CHECK | `545ad19184d8dd7dfb5b2737e081b043d13982f05d05326939ac2cbb89bf54e2` | `e381424d14336d918fd3bafff16698361395c77ef03fef628d7d74d36af8a9da` |
| COLLECT / E2-K-COLLECT | `e381424d14336d918fd3bafff16698361395c77ef03fef628d7d74d36af8a9da` | `6c7efb221870974d76d12d7ceb372369ef68104bb1f522a16d47f7dc37236677` |

The first missing occurrence is CHECK; the canonical acquisition prefix consumed by PREPARE also needs COLLECT in the declared order. Report-local sequences 1 and 2 cannot be promoted to native ledger positions without the actual ledger. Their required original context is E2-QUALIFICATION-ONLY / E2-CANONICAL-BASELINE-1 / E2-GENERATION-1.

`native_result_event_trace` is a **logical P05 evidence-slot name**, not a field or event type in the Planner model. Its meaning comes from A03 and END's event-trace obligations. The native occurrence representation is [ExecutionEvent](../../adapter/planner/model.py:678) carrying [SuppliedResult](../../adapter/planner/model.py:524), not an invented A03_COMPLETED event. [The recovered witness contract](qualification/E2_P05_A03_OCCURRENCE_WITNESS_RECOVERY_1/A03-and-witness-contract.json) distinguishes mandatory and optional terms:

| Term | Native requirement |
|---|---|
| Result | Typed SuppliedResult.action ActionId, ActionResult outcome and full KnowledgeRecord tuple |
| Pre-state | ExecutionEvent.parent_snapshot; supplied.expected_snapshot matches it for the extended P02 state |
| Parent event | Explicit actual parent_event; it may be null for the genuinely first ordinary event of the declared native bundle, rather than an assumed empty history |
| Post-state | ExecutionEvent.after_snapshot, matching the admitted native transition and successor pre-state |
| Event identity | CONTENT_IDENTITY in `planner-event-v1`, bound to native sequence, parent snapshot, parent event, full result and after snapshot |
| Outputs | Exact permitted, producer-bound, accepted KnowledgeRecords with their native provenance and scope |
| Context | Actual event-bearing state context and source/result provenance; no invented top-level scope/lineage/generation fields |
| Enrollment/order | Membership in the authoritative ordered native ledger, with parent/state continuity, CHECK → COLLECT → PREPARE ordering and required source/policy bindings |

Native [ActionResult](../../adapter/planner/model.py:99) is an **enum**, not a separately identified persistent ActionResult record. `SuppliedResult:E2-CHECK` and `SuppliedResult:E2-COLLECT` in older reports are descriptive labels, not content or occurrence identities. The event ID identifies the admitted occurrence. Optional dossier/resume-binding fields are absent or null for these results; no C03 permission is involved. Ordinary record_result has no independent command-ID or A03 event-authority operand. A persisted HEAD command reference, if present, must resolve the actual payload; its hash alone cannot provide the payload.

The native call path is [codec.record_result](../../adapter/planner/codec.py:565) → apply_event → apply_result → result validation/inventory update → append_event. The identity body is defined by [codec._event_identity](../../adapter/planner/codec.py:438). [Legacy tracked/current source comparison](qualification/E2_P05_A03_OCCURRENCE_WITNESS_RECOVERY_1/native-contract-source-comparison.json) confirms that these A03 result/event fields and hash-body semantics already exist in the tracked implementation. The later added event kinds do not imply another earlier A03 event representation. This is a contract comparison, not a claim about which source revision ran in the historical writer.

The witness provides assurance that the then-selected native Action's exact bounded result was admitted against that pre-state, at that event position, producing the declared transition. It binds outputs to the admission and their order relative to preparation. It is stronger than a final completed status, known output or selection report. Because the canonical operation accepts a supplied synthetic result, it is not independent proof of external-world executor invocation or I/O.

The search used artifact contents and native structure, extending the prior state-hash-only search:

| Search dimension | Observed result |
|---|---|
| Structured corpus | **3,268** retained JSON/JSONL/NDJSON files; zero parse errors; full per-file hashes recorded |
| Native events | **107 distinct identities** across canonical and qualification artifacts; zero CHECK/COLLECT event occurrences or original/superseded prefix-state event matches |
| Native result payloads | Zero typed CHECK/COLLECT SuppliedResult payloads; zero alternative A03 native identity-body candidates |
| PersistenceBundle ledgers | **449 occurrences**, including 313 with the E2 Action universe; zero A03 event memberships |
| Other persisted ancestry | **76 HEAD records** and **4 genesis-ledger occurrences**; zero resolved A03 membership |
| Embedded serialized forms | **537 native-related JSON strings** inspected; no A03 event/payload |
| Alternate text | **48 files / 69 matching lines**; no full A03 event representation, multiline JSON event block or constructor/Action occurrence candidate |

The search covers Action IDs, Knowledge/output IDs, native type, original and superseded pre/post-state identities, parent/head identities, HEAD commands, payloads, ordinary/genesis ledgers and embedded native JSON. Content-based expansion outside `docs/plans` found no additional non-E1 experiment/adapter structured artifact with the target identifiers. No legacy E1 history was treated as an E2 witness. The [search corpus](qualification/E2_P05_A03_OCCURRENCE_WITNESS_RECOVERY_1/search-corpus.json), [native event index](qualification/E2_P05_A03_OCCURRENCE_WITNESS_RECOVERY_1/native-events.json), [bundle/HEAD/genesis index](qualification/E2_P05_A03_OCCURRENCE_WITNESS_RECOVERY_1/persistence-bundles.json), [payload/report candidates](qualification/E2_P05_A03_OCCURRENCE_WITNESS_RECOVERY_1/result-and-report-candidates.json), [alternate text query](qualification/E2_P05_A03_OCCURRENCE_WITNESS_RECOVERY_1/alternate-text-representations.json) and [multiline audit](qualification/E2_P05_A03_OCCURRENCE_WITNESS_RECOVERY_1/multiline-text-audit.json) retain the evidence.

The [candidate assessment](qualification/E2_P05_A03_OCCURRENCE_WITNESS_RECOVERY_1/candidate-witnesses.json) rejects substitutions individually:

| Candidate | Classification and limit |
|---|---|
| Final accepted P02 prefix | REPORT_METADATA: actual result/state summaries, but no native event operands, identity or membership; it explicitly reports `events_admitted = 0` |
| Final P02 PASS evidence chain | DERIVED_SUMMARY: preserves owner PASS, but its operation labels are not a ledger |
| Earlier retry 1/2 traces | REPORT_METADATA: descriptive result labels and superseded state identities, not native events |
| Authoritative handoff reproduction trace | REPORT_METADATA: matching CHECK/COLLECT state hashes, without event identity/enrollment |
| Original handoff/post-decision snapshots | SNAPSHOT_ONLY: completed statuses and producer-bound accepted knowledge, without an event tuple |
| Initial Action accepted_inventory | Prospective native definition: permitted output declaration, not an occurred result |
| Prospective P03/P04 initial premises | SNAPSHOT_ONLY for A03: CHECK/COLLECT already completed before the represented history begins; amendment covers checkpoint fidelity, not original A03 occurrence |
| Actual canonical P04 events | NATIVE_CANONICAL_EVENT: valid persisted later lifecycle; supplied results are REENTER/FINISH, rather than CHECK/COLLECT |
| Other qualification ledgers | NATIVE_QUALIFICATION_EVENT: actual native events at their own scope, with no A03 event; genesis expressly preserves an unrepresented pre-history boundary |

The native result trace therefore consists of retained PASS summaries and final KnowledgeRecords/statuses, with **no retained standalone execution record, result-admission event or completion event for A03**. The source declarations are result definitions. KnowledgeId, output provenance hash, SnapshotId, descriptive result label and event identity remain separate domains.

[Native record inspection](qualification/E2_P05_A03_OCCURRENCE_WITNESS_RECOVERY_1/native-record-inspection.json) decoded the original initial, handoff and post-decision snapshots and preserved their canonical bytes exactly. It also decoded the actual P04 target and verified all **20 stored event identities** from their existing serialized fields, with native parent-event/state continuity. The target matches the canonical PASS bundle identity. Its initial Snapshot and first two events exactly match the prospective P03 prefix. CHECK/COLLECT are completed initial premises there; the first event is ActionReevaluation. This is evidence that the later ledger is genuine at its scope, not a connection to unrepresented A03 history. No native replay, result application, event admission or writer commit was called.

No acceptable A03 candidate was found to admit into the P05 graph. Parent continuity, membership and scope cannot be proven for a nonexistent retained candidate. The old mainline checkpoint recovery independently records [the historical boundary](DETERMINISTIC_PLANNER_V0_1_E2_P03_MAINLINE_CHECKPOINT_REPRODUCTION_1.json) as `NOT_REPRESENTED_HISTORICAL_SNAPSHOT_ONLY`. The [existing P03 scope decision](qualification/P03_PROSPECTIVE_CHECKPOINT_1/sources/qualification-scope-authority.json) remains unchanged and explicitly excludes historical reconstruction.

**Lossless derivation is unavailable.** An authoritative alternate ledger body could suffice if every native identity-defining value and enrollment were already retained. Here the exact submitted payload, actual parent/root/head and native event position are unavailable. Deriving them from permitted inventory, output names, local report sequence, final state or the current hash function requires inference. Computing a hash after making those choices would create a hypothetical new event, not recover the past event. [Lossless-recovery.json](qualification/E2_P05_A03_OCCURRENCE_WITNESS_RECOVERY_1/lossless-recovery.json) records these missing terms. Final/post state alone cannot satisfy the occurrence requirement.

The primary classification is **IRRECOVERABLE_HISTORICAL_WITNESS under the retained inputs**. The prefix's zero-admission record and snapshot-only archive are observed non-retention evidence. Neither a truncation/deletion mechanism nor universal proof that no event was ever persisted is established. No binding omission or acceptable alternate native witness was demonstrated. No new runtime defect is inferred, and P02/P03/P04 PASS is not reversed.

Recovery stops at A03. [The qualification-scope dossier](qualification/E2_P05_A03_OCCURRENCE_WITNESS_RECOVERY_1/qualification-scope-decision.json) seals the present decision subject and defines these unselected alternatives:

- **RETAIN_P05_A03_NATIVE_OCCURRENCE_REQUIREMENT**: retain the original assurance and block pending genuine historical artifacts.
- **AUTHORIZE_PROSPECTIVE_P05_A03_OCCURRENCE_QUALIFICATION**: explicitly amend the acceptance mapping to a separately sealed future native reproduction. Its events must be labeled new; original occurrence remains unproven. Exact future inputs, authority applicability, oracles and END ancestry mapping must be sealed before execution.
- **AUTHORIZE_P05_A03_ALTERNATE_NATIVE_EVIDENCE**: name and pin the exact alternative and its assurance mapping. No acceptable alternate occurrence witness is available. Snapshot/report acceptance would be a weaker state-evidence scope, not original occurrence proof or unchanged END/N12/N13 assurance.
- **DEFER_P05_A03_HISTORICAL_OCCURRENCE_REQUIREMENT**: explicitly amend the acceptance profile, record the residual assurance and affected coverage conclusions. It cannot mark the original witness or unamended END PASS.

The subject content identity is `qualification-scope-subject-v1:adac1bcae367498700848ecb7a6189877830e7bee25681c040c37d7c0ab38173`. This is dossier content identity, not a native grant. Any substitution requires an explicit authenticated Architect/qualification-scope acceptance decision. Prior P03, INSTALL, GENESIS or operating authority does not make that decision. None is selected, issued or applied. The prospective execution inputs/alternate candidate are not yet sealed, so this recovery does not claim a complete future execution authorization. Other A04–A06 gaps, END ancestry/replay and P05/P06 gates remain enforceable; no option automatically qualifies the Planner or changes N-REAL.

The [preservation audit](qualification/E2_P05_A03_OCCURRENCE_WITNESS_RECOVERY_1/preservation.json) checks all 14,789 files in the before-work artifact/runtime inventory, including 10,677 frozen-E1 files and all 28 runtime files. Prior binding files, canonical target and scope decisions remain unchanged. Only the new recovery reports and evidence are authored. `git diff --check = PASS`.

```text
WORK_PACKAGE = E2-P05-A03-OCCURRENCE-WITNESS-RECOVERY
RESULT = BLOCKED

A03_PURPOSE = Bounded execution and accepted knowledge
A03_NATIVE_OPERATION = record_result/append_event with typed SuppliedResult; CHECK then COLLECT
A03_CONTRACT_RECOVERY = PASS
WITNESS_CONTRACT = ExecutionEvent + exact result/output + parent/pre/post/identity + context/provenance + actual ledger membership/order
WITNESS_ASSURANCE_PURPOSE = Native result occurrence and admission ancestry; state/selection/declaration alone insufficient

CANONICAL_EVENT_SEARCH = 3268_FILES; 107_DISTINCT_NATIVE_EVENT_IDENTITIES; 0_A03_EVENT_MATCHES
PERSISTENCE_SEARCH = 449_BUNDLE_OCCURRENCES; 76_HEADS; 4_GENESIS_LEDGERS; 0_A03_MEMBERSHIPS
QUALIFICATION_SEARCH = 0_NATIVE_A03_EVENT_OR_TYPED_RESULT_PAYLOAD; REPORT_AND_SNAPSHOT_EVIDENCE_RETAINED
CANDIDATE_WITNESSES = candidate-witnesses.json; ACCEPTABLE_COUNT=0

LOSSLESS_RECOVERY = NO
PRIMARY_CLASSIFICATION = IRRECOVERABLE_HISTORICAL_WITNESS (RETAINED_INPUTS_ONLY)
A03_NATIVE_RESULT_EVENT_TRACE = FAIL
LEGITIMATE_WITNESS_BOUND = NO

P05_BOUND_STAGE_INPUTS = 9 / 13
P05_NEXT_MISSING_INPUT = E2-A03.native_result_event_trace
P05_GRAPH_RERUN = NO (A03_NOT_CLOSED)
P05_EXECUTION_READY = NO
E2_P05_READY = YES (P04_PASS_PREREQUISITE)
SELECTED_SCOPE_OPTION = NONE

P04 = PASS
P05_EXECUTED = NO
P06_EXECUTED = NO
A03_REEXECUTED = NO
NEW_NATIVE_EVENTS = 0
NEW_AUTHORITIES = 0
P03_HISTORICAL_CORRESPONDENCE = UNPROVEN
N_REAL_SATISFIED = NO

RUNTIME_MODIFIED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
GIT_DIFF_CHECK = PASS
```
