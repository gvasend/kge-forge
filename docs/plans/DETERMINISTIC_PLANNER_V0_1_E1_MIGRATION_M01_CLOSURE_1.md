# M01 contract closure 1

**RESULT = PARTIAL; M02_READY = NO.** All six open groups,13 source families and35 target categories were evaluated. This pass establishes an executable selection/execution separation rule, completes mutually exclusive source-disposition criteria, and narrows target coverage. It does not close any of the six whole gap groups: their remaining admission/field-mapping obligations are still required. One conditional native-target incompatibility is newly recorded as M01-CC01.

The original M01 PARTIAL result and all prior contracts remain unchanged. No migration/runtime implementation, existing test or operational registry was modified; M02 and real-E1 readiness were not executed.

## Evidence and companions

Read the authoritative [migration plan](DETERMINISTIC_PLANNER_V0_1_E1_MIGRATION_IMPLEMENTATION_PLAN_1.md), its [machine plan](DETERMINISTIC_PLANNER_V0_1_E1_MIGRATION_IMPLEMENTATION_PLAN_1.json), [acceptance matrix](DETERMINISTIC_PLANNER_V0_1_E1_MIGRATION_ACCEPTANCE_MATRIX_1.md), [boundary decision](DETERMINISTIC_PLANNER_V0_1_E1_MIGRATION_BOUNDARY_DECISION_1.md), original [M01 result](DETERMINISTIC_PLANNER_V0_1_E1_MIGRATION_M01_RESULT.md) and its six companions. Native type/replay evidence was inspected in [model.py](../../adapter/planner/model.py) and [codec.py](../../adapter/planner/codec.py); source history comes from the frozen [resolution plan](../experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_PLAN_1.json).

New companions:

- [Contract and complete gap/source/target matrices](DETERMINISTIC_PLANNER_V0_1_E1_MIGRATION_M01_CLOSURE_1_CONTRACT.json).
- [Fixtures, executable specification and24-record history inventory](DETERMINISTIC_PLANNER_V0_1_E1_MIGRATION_M01_CLOSURE_1_FIXTURES.json).
- [Validation](DETERMINISTIC_PLANNER_V0_1_E1_MIGRATION_M01_CLOSURE_1_VALIDATION.json).
- [Complete preflight](DETERMINISTIC_PLANNER_V0_1_E1_MIGRATION_M01_CLOSURE_1_PREFLIGHT.json).

No undocumented canonical field has been supplied to make completeness counts increase. “Contract complete” below describes the specific field contract, not that a full native snapshot exists.

## Six-gap normalization and shared causes

| Gap | Sources / targets | Missing contract; affected cases; downstream |
|---|---|---|
| M01-G01 | PLAN/MANIFEST/governed rules → Action/Predicate/KnowledgeRecord | Complete prospective result, authority/evidence and knowledge bindings for63 definitions; MC03; M03. Historical text/outcomes are present; the missing typed interpretation is not fabricated. |
| M01-G02 | Reports and exact plan ledger joins → result/knowledge records | Independently parameterized real-source profiles for OR-BINDING, OR-CONTEXT, OR-PREP-VALIDATOR; MC04; M04. Fixed synthetic identity forms cannot authenticate real report bytes. |
| M01-G03 | Plan history, result reports, authority records → planning/selection history, result history and current overlay | Native passive planning-history storage and complete O02/O06 imported-history/hold interface; MC05; M04. Selection/result separation now specified, full handoff remains open. |
| M01-G04 | All13 families → recognized records/source pins | Exact nested field whitelist, authenticated text selectors and domain-subtype registry; MC01; M02. Broad recognition families are not complete source schemas. |
| M01-G05 | All required sources →35 target categories /17-element operational coverage | Complete field derivation/disposition, currentness/dependency and native composition crosswalk; MC02/MC06; M02–M07. Required fields still marked unexplained prevent a successful snapshot. |
| M01-G06 | All required classes → independently admitted native targets | Complete source-shaped positives/negatives and composition qualification; MC01–MC06; M02–M07. Shape-only fixtures cannot replace these. |

The machine matrix includes source artifact kind, canonical type, governing requirement, semantic-input distinction and downstream ownership for every group.

Shared causes are RG1 SEMANTIC_NORMALIZATION (G01/G02), RG2 SELECTION/EXECUTION AND HISTORY/RESULT DISTINCTION (G03), RG3 SOURCE_RECOGNITION/TARGET_COMPLETENESS (G04/G05), and RG4 NATIVE_ADMISSION_HANDOFF (G06, dependent on the others). These are dependency groups, not claims that one code change will solve multiple contracts. Identity/provenance metadata was already defined and does not supply missing semantics by itself.

## Selection and execution invariant

The frozen `/execution_history/0` is a selection attempt. It contains `selection_attempt`, `status=SELECTION_BLOCKED`, `planner_exception=PLANNER_TIE_BREAK_UNDEFINED` and `action_result=null`. Its explanation explicitly says no action was selected or executed. It is neither an executed BLOCKED action nor a result with a missing default outcome.

The complete ledger has24 records: this selection-only record and23 records referencing separate result artifacts. All23 referenced report/authority artifact raw hashes match the ledger pins. These identity checks establish historical source correspondence, not native acceptance of every reported claim.

The executable classification contract establishes:

```text
ACTION_SELECTED != ACTION_EXECUTED
ACTION_SELECTED != ACTION_COMPLETED
ACTION_SELECTED != ACTION_RESULT_EXISTS
ACTION_SELECTED != KNOWLEDGE_PRODUCED
```

A recorded selection with no separate execution/result evidence admits only SELECTION_HISTORY. An actual result candidate requires explicit producer/outcome and the exact independently bound result source. A later result does not mutate an earlier selection record into execution. Knowledge needs a further independent type/acceptance/currentness proof; a result record alone cannot establish it.

The native model has ActionState.SELECTED but no PlanningHistoryRecord or SelectionHistory type. ExecutionEvent instead requires parent snapshot, after snapshot, event identity and replayable transition. Consequently the migration may retain the selection record as pinned historical provenance now; it must not falsely emit a native ExecutionEvent or SuppliedResult. Defining and admitting a passive canonical planning-history carrier is still M01-G03, not an existing implemented capability. No historical parent snapshots are fabricated.

The35 specification cases cover24 source-record classifications plus synthetic selected-only, correct independent result, absent/wrong producer/source, stale support and unsupported knowledge-promotion variants. All pass; canonical JSON reload preserves all35 outcomes. These are classification tests, not migration execution or complete native-admission tests.

## History roles and exclusive source dispositions

The source matrix covers each family:

| Source family | History it can directly support |
|---|---|
| PLAN | PLAN_HISTORY, SELECTION_HISTORY; EXECUTION_HISTORY only for independently joined result records |
| GRAPH | EVIDENCE_HISTORY/provenance; current assertions require O10/currentness admission |
| MANIFEST, CHECKPOINT | Provenance and bindings; saved outcome labels are comparison evidence |
| HANDOFF, EXTERNAL_REQUEST | EVIDENCE_HISTORY of requests/absences, not receipt or positive evidence |
| DECISION_AUTHORITY, CANDIDATE_AUTHORITY | AUTHORITY_HISTORY; usable grant requires independent authority admission |
| PROFILE_CANDIDATE, INVOCATION_CANDIDATE, PINNED_SUBJECT | EVIDENCE_HISTORY of the identified object; no automatic proof admission |
| GOVERNED_TEXT | PROVENANCE_ONLY until a reviewed section/result/dossier contract assigns a stronger role |
| GLOBAL_CONTROL | PLAN_HISTORY and oracle/provenance; not authoritative current control labels |

ACTION_RESULT requires the execution/report join; ACCEPTED_KNOWLEDGE additionally requires its typed admission. No family receives these stronger roles through chronological proximity.

Disposition is determined per source instance and field roles, not by filename or family alone:

1. A virtual expected-source record with a valid exact gate contract, no received evidence and the specified missing proposition is REPRESENTED_AS_EXPECTED_ABSENCE. It cannot also be a present-source record.
2. An actual source with any required operational clause is MIGRATED_OPERATIONAL; preserve historical/provenance role tags on its other fields.
3. Otherwise, an explicitly historical-role source is HISTORICAL_ONLY.
4. Otherwise, a referenced authentication dependency is MIGRATED_PROVENANCE_ONLY.
5. Otherwise, only an audited irrelevant source is NOT_REQUIRED. Unknown relevance remains unresolved; it does not fall through to exclusion.

This priority makes primary dispositions exclusive while retaining multiple justified field/history roles. It applies to all13 families. Therefore SOURCE_DISPOSITIONS_COMPLETE=13/13 **for decision rules**, not for completed source inventories or semantic relevance determinations. G04/G05 still block that latter claim.

## Target completeness and missing semantics

All35 target categories were reclassified individually:

| Classification | Count |
|---|---:|
| CONTRACT_COMPLETE |11 |
| CONTRACT_INCOMPLETE |21 |
| SEMANTIC_INPUT_MISSING |0 newly demonstrated |
| NOT_REQUIRED_FOR_FROZEN_RESUME |3 |

Complete field contracts are: frozen receipt admission and observation inventories (explicitly empty); native subsequent event inventory (empty until migration actually executes a native transition); policy artifact/version through the existing qualified registry; full-run scope with mandatory coverage validation; MigrationManifest metadata; optional information/cost fields with no invented metrics; descriptive provenance; and saved control/actionability/resume labels as comparison-only provenance.

An empty native event inventory is valid only from an independently admitted migrated baseline, with legacy history retained separately. This does not prove the initial/current baseline fields complete. An empty receipt inventory does not omit the receipt contracts carried by gates. Optional metrics being absent means deterministic selector fallthrough, not cost zero or information gain zero.

The three not-required categories are positive external evidence absent at suspension, audited unreferenced archive payloads, and embedding entire raw source bodies in the snapshot. Required references, claims and expected absences still persist. All other categories remain contract-incomplete; the machine matrix does not hide them under a generic success status.

Per-field derivation categories are DIRECT_SOURCE_FIELD, DETERMINISTIC_DERIVATION, AUTHORIZED_CROSS_SOURCE_JOIN, VERSIONED_LEGACY_NORMALIZATION, EXPECTED_ABSENCE, NOT_REQUIRED or PROVENANCE_ONLY. Required target rows lacking a complete field mapping remain explicitly unexplained; the requested “no unexplained REQUIRED field” acceptance condition is **not met**. Merely attaching a derivation-category name to such a row is not a derivation proof.

Available historical fields are RECOVERABLE_FROM_LEGACY_SCHEMA; existing proof/currentness/policy rules are RECOVERABLE_FROM_EXISTING_BR/OXX_CONTRACT; manifest/plan and report/ledger identities are RECOVERABLE_BY_AUTHORIZED_JOIN. Positive external facts are NOT_REQUIRED_FOR_FROZEN_RESUME. No additional GENUINELY_MISSING frozen fact was proven. Unestablished semantic interpretation remains CONTRACT_MISSING, not evidence that a value may be invented or that no governing source could exist.

## Native handoff and M01-CC01

All operational destinations remain subject to O01, O02/O06, O08/O09, O10, O16 and the applicable budget/decision/authority/root/slot/native model contracts. Metadata success cannot waive admission. Source invalidation must preserve historical facts while removing current admission support and recomputing dependents after reload. The new history fixtures include stale source rejection; full migrated-native invalidation tests remain blocked by the missing target profiles.

**M01-CC01 — budget target/native-scope incompatibility:** `codec._replay` rejects any nonempty `Snapshot.budget_matrices` unless the bundle scope is PARTIAL_SYNTHETIC_BUDGET_QUALIFICATION. The full frozen import scope is FULL_FROZEN_E1_REPLAY. The migration plan requires restoring the budget proof contract in the full frozen target. Encoding that unsatisfied contract as a nonempty BudgetProofMatrix would therefore fail unchanged native admission, even if no positive evidence were fabricated.

This is conditional on that target representation; it is not a request to remove the existing guard. The contract must either establish the equivalent frozen obligation representation through native EvidenceRequirement/Predicate/source-bound knowledge with an empty synthetic matrix collection, preserving every budget oracle obligation, or explicitly define and review an appropriate canonical type-compatibility extension. No such complete equivalence contract is established in this pass. No synthetic matrix is inserted, guard disabled or runtime modified.

The conflict is recorded in addition to all six original mismatch groups. Existing Oxx predicates were not weakened, and this finding does not reopen F03 or alter accepted correction history without a separate finding review.

## External absence and complete preflight

Eight active external evidence boundaries remain unresolved. The original M01 absence routes and BR-C1 contracts are reused. Selection, result classification, source disposition and metadata rules cannot create received evidence, a new authority or positive reentry. EXPECTED_RESUME_ALLOWED remains NO.

MIGRATION_MANIFEST is DEFINED as metadata. The integrated FROZEN_STATE_ORACLE and SYNTHETIC_REENTRY_ORACLE remain INCOMPLETE because their native field/profile derivation is not complete; known expected output labels and the existing budget oracle are not themselves missing.

All six original gaps remain OPEN at their full acceptance scope. The selection distinction and disposition subcontracts improve them but do not justify closing the groups. M01 acceptance requires complete required semantics and independent native positives, so missing contracts cannot be deferred into M02 merely to start implementation. No plan waiver was applied.

```text
RESULT = PARTIAL
M01_GAPS_INITIAL = 6
M01_GAPS_CLOSED = 0
M01_GAPS_REMAINING = [M01-G01, M01-G02, M01-G03, M01-G04, M01-G05, M01-G06]
M01_ROOT_CAUSE_GROUPS = [SEMANTIC_NORMALIZATION, SELECTION_EXECUTION_DISTINCTION,
  SOURCE_RECOGNITION_AND_TARGET_COMPLETENESS, NATIVE_ADMISSION_HANDOFF]
SELECTION_EXECUTION_INVARIANT = PASS (bounded specification)
SOURCE_FAMILIES = 13
SOURCE_DISPOSITIONS_COMPLETE = 13/13 (exclusive criteria, not source-instance qualification)
TARGET_CATEGORIES = 35
TARGET_CONTRACTS_COMPLETE = 11/35
TARGET_CONTRACTS_INCOMPLETE = 21/35
TARGET_NOT_REQUIRED_FOR_FROZEN_RESUME = 3/35
TARGET_SEMANTIC_INPUT_MISSING = [] newly established; unresolved contracts remain
M01_CONTRACT_MISMATCH_SET = [M01-G01, M01-G02, M01-G03, M01-G04, M01-G05, M01-G06]
M01_CONTRACT_CONFLICT_SET = [M01-CC01]
M01_SEMANTIC_INPUT_MISSING_SET = []
MIGRATION_MANIFEST = DEFINED_METADATA_CONTRACT
FROZEN_STATE_ORACLE = INCOMPLETE
SYNTHETIC_REENTRY_ORACLE = INCOMPLETE
M02_READY = NO
NEXT_PACKAGE = M01 follow-up: resolve M01-CC01 and remaining semantic/native contracts
EXPECTED_EXTERNAL_GATES = 8
EXPECTED_RESUME_ALLOWED = NO
V0_1_CURRENT_STATUS = CORRECTION_REQUIRED
IMPLEMENTATION_MODIFIED = NO
REAL_E1_EVIDENCE_CREATED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
```

Validation: 26 bounded positive classifications and 9 negative cases passed;35 canonical JSON reload comparisons passed. No native migration positive is claimed. All10,911 frozen paths/hashes and all pre-existing protected files are unchanged. Five new specification/result artifacts only. JSON, links, whitespace and `git diff --check` passed.
