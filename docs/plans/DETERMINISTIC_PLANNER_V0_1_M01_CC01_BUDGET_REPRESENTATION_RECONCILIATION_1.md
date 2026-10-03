# M01-CC01 budget representation reconciliation 1

M01-CC01 is a **migration contract defect caused by conflating unresolved obligation inventory with accepted synthetic proof**. Frozen E1 requires all eight obligations and their unresolved status, source-bound historical knowledge, expected absence and the external gate. It requires **no positive `BudgetProofMatrix` instance**. The native synthetic-scope guard must remain intact. No model or codec correction is required to resolve this frozen-state representation conflict.

This is a representation contract, not a completed migration mapping or readiness test. Real positive evidence admission remains a separate contract requirement; the existing synthetic profile does not establish that capability for arbitrary real evidence. M01 closure may resume on this basis; M02 remains disallowed.

## Governing evidence

- [M01 result](DETERMINISTIC_PLANNER_V0_1_E1_MIGRATION_M01_RESULT.md), [closure result](DETERMINISTIC_PLANNER_V0_1_E1_MIGRATION_M01_CLOSURE_1.md) and [35-category matrix](DETERMINISTIC_PLANNER_V0_1_E1_MIGRATION_M01_CLOSURE_1_CONTRACT.json): CC01 is explicitly conditional on representing the unsatisfied contract as a nonempty native matrix.
- [Migration plan](DETERMINISTIC_PLANNER_V0_1_E1_MIGRATION_IMPLEMENTATION_PLAN_1.md) and [acceptance matrix](DETERMINISTIC_PLANNER_V0_1_E1_MIGRATION_ACCEPTANCE_MATRIX_1.md): faithful suspended state, source provenance, native admission, no fabricated external evidence; positive synthetic reentry is a separate qualification case.
- [Frozen FACT result](../experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_FACT_BUDGET_APPLICABILITY_1_RESULT.json), `/proof_matrix`: all eight rows have `result=EVIDENCE_NOT_FOUND`; none establishes applicability. Its source evidence distinguishes verified recorded bytes from currentness.
- [Frozen request](../experiments/E1/E1_BUDGET_APPLICABILITY_EXTERNAL_EVIDENCE_REQUEST_1.json), `/receipt_action`, `/reentry_route`, `/historical_outcome`, `/generic_external_gate_lifecycle`: no received evidence; FACT historically EXTERNAL_GATE_REQUIRED/BLOCKED; complete positive coverage is required before bounded FACT revalidation, then a separate REEVAL attempt.
- [Resume manifest](../experiments/E1/E1_RESUME_MANIFEST_1.json), [checkpoint](../experiments/E1/E1_SUSPENSION_CHECKPOINT_1.json), [global recomputation](../experiments/E1/E1_GLOBAL_CONTROL_RECOMPUTATION_1.json): the whole frozen instance is suspended; budget is one of eight external boundaries.
- [Budget oracle](DETERMINISTIC_PLANNER_V0_1_BUDGET_PROOF_MATRIX_ORACLE_1.md) and [normative companion](DETERMINISTIC_PLANNER_V0_1_BUDGET_PROOF_MATRIX_ORACLE_1.json): absent submission returns false/EVIDENCE_NOT_YET_AVAILABLE; positive EXACT_CHECKPOINT_1 trust/rules apply only in synthetic qualification. [C06A retry result](DETERMINISTIC_PLANNER_V0_1_C06A_RETRY_1_RESULT.md) qualifies that bounded profile, not full E1 restoration.
- Native evidence: [model.py](../../adapter/planner/model.py) (`EvidenceRequirement`, `ExternalGate`, `ReceiptAdmission`, `BudgetProofMatrix`); [budget.py](../../adapter/planner/budget.py) (`validate_input`, `validate_matrix`, `validate_restored`, `import_budget`); [codec.py](../../adapter/planner/codec.py) (`_replay`); [gates.py](../../adapter/planner/gates.py) (`_obligation_proof`, `_check_receipt`, `_external_complete`); [core.py](../../adapter/planner/core.py) (`apply_receipt`, `_global_control`, `resume_eligibility`). These implementation paths were inspected, not inferred from passing output labels.

## Three representations

| Aspect | Frozen E1 source | Independent positive qualification profile | Native representation/capability |
|---|---|---|---|
| Facts | Recorded authority and exact target identities; absence of current applicability evidence | Explicit synthetic authenticated facts AND separately admitted governing rules | Source-pinned entities/assertions/knowledge; subject identity is not applicability |
| Obligations | Eight named independent propositions, all EVIDENCE_NOT_FOUND | Exactly eight positive fact/rule rows, with full envelope correspondence | Eight EvidenceRequirement identities and EVIDENCE_OBLIGATION predicates can describe unresolved requirements; BudgetProofMatrix describes the separate supported positive profile |
| Evidence | No accepted external applicability bundle | Complete source authentication, competent grants, facts, rules, trusted checkpoint | Empty receipt inventories represent no receipt; accepted claims require independent authentication and current sources |
| Absence | Expected external evidence absent; not an absent action definition or malformed input | No required positive premise absent | Gate plus unresolved requirements and pinned absence provenance; no native ExpectedAbsence object is implied |
| Waiting | EXT-BUDGET-APPLICABILITY-EVIDENCE, WAITING_FOR_EXTERNAL_EVIDENCE | Partial qualification snapshot, not the frozen waiting instance | ExternalGate stage, pending=None, route and held actions; controls derived from complete goal/frontier state |
| Knowledge | Accepted historical knowledge of missing proofs; historical producer can remain BLOCKED | Additional accepted complete matrix knowledge | Keep separate identities, outcomes, source bindings and dependency validity |
| Applicability | Unproved; not DISPROVED merely because evidence is absent | Proven only within explicit synthetic envelope/anchor | UNKNOWN obligation proofs versus accepted positive proof; no saved applicability Boolean is authoritative |
| Currentness | Recorded bytes verified does not establish current applicability | Every required fact/rule/anchor current and independently trusted | Source invalidation removes current admission support after reload |
| Reentry | Receipt contract specified, not executed; no positive reentry | Bounded qualified FACT/reevaluation behavior | Legal receipt lifecycle plus current prerequisites; eligibility is not automatic execution or blanket E1 resume |

The eight row IDs have prefix `BUDGET-PROOF-` and suffixes:
`AVAILABILITY_PUBLICATION`, `SCOPE`, `LINEAGE`, `RUNTIME`, `CONTROLLER_STORE_G4`, `PROGRAMMER_PROFILE`, `TEMPORAL_CURRENTNESS`, `EXECUTION_REQUEST_PHASE`.
Eight propositions are not eight received artifacts and are not the eight separate external boundaries of the entire frozen experiment. A competent evidence artifact may cover multiple propositions; no physical artifact count is invented.

## Canonical frozen-budget contract

**Requirement classification D: COMBINATION of B (proof-obligation/status matrix) and C (expected absence and gate).** A full positive matrix is not required. The historical source's `proof_matrix` is a diagnostic obligation/status table, not the native `BudgetProofMatrix` type.

The minimum logical representation is:

1. `Snapshot.budget_matrices=()` in both frozen initial and current snapshots. No knowledge with `BUDGET_ORACLE_1` provenance is synthesized. This emptiness records the absence of a supported accepted positive profile, not the absence of budget obligations.
2. Eight distinct typed `EvidenceRequirement` records using the exact row IDs. Preserve each proposition, exact target subject binding, request/report selector and content provenance. The request's complete subject tuple (authority, invocation, dispatch, context, release, runtime, store, profile, scope pair and recorded lineage) remains pinned and recoverable; a single target identity is not permission to discard the other correspondence requirements.
3. `PredicateKind.EVIDENCE_OBLIGATION` references for the eight requirements, with a conjunctive requirement where the consumer requires full coverage. Unknown real governing rules and unestablished concrete producers remain explicitly unknown (`rule_known=False` and no fabricated producer identity where applicable). A request describing the desired proof does not make its governing rule known. Defaults must not manufacture this information. These are supported unresolved evidence obligations, not arbitrary UNSUPPORTED predicates used to hide a plan defect.
4. `ExternalGate` bound to `EXT-BUDGET-APPLICABILITY-EVIDENCE`, the eight requirement identities, `RECEIVE-BUDGET-APPLICABILITY-EVIDENCE`, the governed FACT revalidation route and downstream REEVAL dependency. Stage is WAITING_FOR_EXTERNAL_EVIDENCE; pending evidence is absent; no accepted receipt admission/observation is created. Preserve the request identity and missing propositions in pinned provenance/absence records. A complete request contract is not a complete positive proof or a known real producer.
5. Keep existing accepted REEVAL-BUDGET missing-proof knowledge, including its required type, producer/outcome and current source binding. Its producer need not become COMPLETED. FACT remains historically BLOCKED/EXTERNAL_GATE_REQUIRED; no new result is created. Roots and the budget-policy slot remain unresolved. A receipt must not bypass FACT's other prerequisites or directly grant REEVAL completion.
6. Persist graph dependencies, held-action relationships, goals and control boundaries needed to reach the budget external frontier and dependent branches. Other frozen branches remain independently represented. Budget waiting alone cannot determine MIXED_WAIT: the entire frontier, absence of internal work and decision readiness must be recomputed by existing control/resume logic.

Expected absence is a positive statement about the request/waiting contract and a negative statement about receipt inventory. It is not an invented evidence entity, proof of incompatibility, or assumed authority to fetch evidence. The exact cross-source and native field mappings still belong to the open M01 contracts; this representation choice does not claim they have been implemented or independently qualified.

At cold load, `_obligation_proof` returns UNKNOWN for missing governing rules or no current accepted observations. `_external_complete` requires every row PROVED, so it cannot accept this state. `apply_receipt` cannot advance directly from WAITING to reentry. `resume_eligibility` still requires current evidence, accepted reentry lineage, verified source pins and named-action eligibility. Combined with the independently restored other branches, the acceptance oracle remains MIXED_WAIT, no runnable internal actions, no decision-ready actions and no E1 resume. These are expected conclusions, not manifest permission labels.

## Positive reentry is separate

The positive representation must preserve the complete eight-row proof and its evidence/rule dependencies, source authentication, exact subject envelope, current anchor, accepted provenance and invalidation state. A receipt wrapper or eight PROVED labels alone is insufficient. A validated complete bundle may support FACT revalidation; only the accepted FACT result supports the subsequent REEVAL attempt. Root/slot completion remains separately governed.

For **synthetic qualification**, retain the existing native `BudgetProofMatrix`, `BudgetEnvelope`, eight `BudgetProofRow` records, canonical parameter/submission payloads, typed matrix knowledge, assertions and consumer requirements, under `PARTIAL_SYNTHETIC_BUDGET_QUALIFICATION`. The independent parameter pin and synthetic competent grants remain mandatory. Current source-bound historical knowledge remains a separate prerequisite. This existing positive oracle remains valid and is reused in synthetic reentry qualification; it is not evidence for frozen E1.

For **real future evidence**, retain original source identities and competent authentication/rule bindings, independently validate every obligation, then admit the canonical evidence/receipt/knowledge representation through the existing lifecycle. The generic receipt mechanism is a handoff for independently admitted proofs; it does not implement the eight real governing rules itself. The current synthetic budget profile explicitly rejects real mode. No existing real-mode matrix adapter is established by this reconciliation, and changing a bundle scope or copying synthetic trust is prohibited. Actual source formats/rules must receive a separately reviewed native admission mapping before real positive reentry can be claimed. If that work establishes that a new native positive carrier is needed, its model/codec change is a separate bounded proposal, not removal of the present guard.

Persist all required fact/rule/source/anchor dependencies. Invalidation after reload must remove the supporting admission and recompute actionability, even when the historical receipt/result remains recorded. Revalidation requires the defined new evidence/admission transition, not clearing a stale bit. Receipt alone does not prove validation; validation alone does not establish resume eligibility.

## Codec contract and conflict classification

`codec._replay` rejects any nonempty matrix in either initial/current snapshot unless scope is PARTIAL_SYNTHETIC_BUDGET_QUALIFICATION. Independently, `budget.validate_matrix` calls `validate_input`, which requires synthetic mode, pinned parameters, all eight positive rows and current evidence. Therefore removing the scope check would neither provide an unresolved-matrix type nor establish real evidence trust.

| State | Required codec behavior | Current behavior / conclusion |
|---|---|---|
| Full frozen unresolved budget, empty positive matrices, valid native requirements/gates and otherwise complete snapshot | Accept after all native validation/replay/policy/coverage checks | Budget representation is compatible; no full frozen migration acceptance is claimed |
| Supported complete synthetic positive matrix in synthetic scope | Accept with dependency and canonical-form validation; reject invalid evidence | Supported by existing budget qualification; preserve it |
| Synthetic positive matrix relabeled full E1 | Reject | Correct intentional trust/schema boundary |
| Historical unresolved status table inserted as BudgetProofMatrix | Reject | Correct type mismatch; missing fact/rule proof cannot be fabricated |
| Actual future positive evidence submitted to synthetic-only profile | Fail closed until independently admitted real mapping exists | Correct rejection of unsupported input; not proof of full real positive capability |

`CODEC_REJECTION_CLASSIFICATION=INTENTIONAL_SCHEMA_BOUNDARY`; the attempted input also has a `MIGRATION_TARGET_MISMATCH`. `M01_CC01_CLASSIFICATION=MIGRATION_CONTRACT_DEFECT`. No native implementation defect is established by this conflict. The minimum correction is this explicit frozen/positive contract separation and its incorporation into the next M01 target crosswalk. The required budget contract inventory stays nonempty logically, carried by obligations and source provenance; the positive-native collection stays empty at suspension.

Subsequent qualification must independently check: eight exact unresolved rows retained; missing/duplicate/wrong-target row rejected by migration completeness; no fabricated producer/rule/receipt; empty positive matrices in both snapshots; synthetic full-scope substitution rejected; all frozen gate/knowledge bindings survive reload and invalidation; valid synthetic positive matrices still pass their original oracle. This task defines those expectations and does not execute migration or claim those integration tests passed.

## All 35 target categories rechecked

Only `Snapshot.budget_matrices` changes conceptual classification to CONTRACT_COMPLETE **for the frozen empty inventory contract**. Twenty other incomplete categories retain their independent mapping/admission obligations. In particular evidence requirements, gates, predicates, knowledge, assertions, source pins, absence records and derivation index do not become complete merely because this ambiguity is resolved. Initial/current full snapshots also remain incomplete. Receipt inventories were already correctly empty. Positive absent evidence remains NOT_REQUIRED_FOR_FROZEN_RESUME.

| Target category | Updated conceptual classification |
|---|---|
| Snapshot.actions | CONTRACT_INCOMPLETE |
| Snapshot.statuses | CONTRACT_INCOMPLETE |
| Snapshot.roots | CONTRACT_INCOMPLETE |
| Snapshot.slots | CONTRACT_INCOMPLETE |
| Snapshot.knowledge | CONTRACT_INCOMPLETE |
| Snapshot.assertions | CONTRACT_INCOMPLETE |
| Snapshot.entities | CONTRACT_INCOMPLETE |
| Snapshot.predicates | CONTRACT_INCOMPLETE |
| Snapshot.context | CONTRACT_INCOMPLETE |
| Snapshot.decisions | CONTRACT_INCOMPLETE |
| Snapshot.evidence_requirements | CONTRACT_INCOMPLETE |
| Snapshot.external_gates | CONTRACT_INCOMPLETE |
| Snapshot.receipt_admissions | CONTRACT_COMPLETE |
| Snapshot.receipt_observations | CONTRACT_COMPLETE |
| Snapshot.boundaries | CONTRACT_INCOMPLETE |
| Snapshot.goals | CONTRACT_INCOMPLETE |
| Snapshot.budget_matrices | CONTRACT_COMPLETE |
| PersistenceBundle.initial | CONTRACT_INCOMPLETE |
| PersistenceBundle.events | CONTRACT_COMPLETE |
| PersistenceBundle.current | CONTRACT_INCOMPLETE |
| PersistenceBundle.sources | CONTRACT_INCOMPLETE |
| PersistenceBundle.policy | CONTRACT_COMPLETE |
| PersistenceBundle.policy_version | CONTRACT_COMPLETE |
| PersistenceBundle.scope | CONTRACT_COMPLETE |
| historical_attempts | CONTRACT_INCOMPLETE |
| expected_external_absence_records | CONTRACT_INCOMPLETE |
| MigrationManifest | CONTRACT_COMPLETE |
| DerivationIndex | CONTRACT_INCOMPLETE |
| Snapshot.information | CONTRACT_COMPLETE |
| Action.cost/cost_unit | CONTRACT_COMPLETE |
| descriptive titles/report narrative/source annotation | CONTRACT_COMPLETE |
| global-control/actionable/resume summary labels | CONTRACT_COMPLETE |
| positive external evidence absent at suspension | NOT_REQUIRED_FOR_FROZEN_RESUME |
| unreferenced archived experiment payloads | NOT_REQUIRED_FOR_FROZEN_RESUME |
| complete raw source bodies embedded inside snapshot | NOT_REQUIRED_FOR_FROZEN_RESUME |

Updated conceptual counts: **12 complete, 20 incomplete, 3 not required; total 35**. No additional genuinely missing semantic input is established here. All six original whole gap groups remain open; restoration qualification remains 2/17. This is an additive reconciliation and does not alter historical counts/results.

## M01 reentry and preservation

The exact reentry predicate is:

```text
M01_CLOSURE_REENTRY_ALLOWED =
    CC01 explicitly separates unresolved obligations from accepted positive proof
    AND frozen target requires all eight obligations plus absence/gate/source dependencies
    AND no synthetic positive evidence is admitted into frozen E1
    AND existing positive qualification and native admission requirements remain intact
    AND (no model/codec correction is needed for this frozen representation
         OR a separately authorized required correction has completed)
```

This predicate is satisfied at the representation-contract level: M01 closure may continue resolving G01–G06. It does not waive their acceptance criteria or authorize M02. There is no prerequisite to fabricate real positive evidence before representing suspension. The separate future real-positive admission gap must remain visible in the reentry contract and cannot be counted as already qualified.

```text
FROZEN_BUDGET_STATE = WAITING_FOR_EXTERNAL_EVIDENCE; eight EVIDENCE_NOT_FOUND obligations
POSITIVE_REENTRY_BUDGET_STATE = complete independently accepted current eight-row proof, then governed receipt/FACT/REEVAL transitions
FROZEN_REPRESENTATION_REQUIREMENT = COMBINATION [PROOF_OBLIGATION_MATRIX_REQUIRED, EXPECTED_ABSENCE_AND_GATE_REQUIRED]
POSITIVE_REPRESENTATION_REQUIREMENT = authenticated complete fact/rule matrix with source/envelope/currentness dependencies
CODEC_REJECTION_CLASSIFICATION = INTENTIONAL_SCHEMA_BOUNDARY
M01_CC01_CLASSIFICATION = MIGRATION_CONTRACT_DEFECT
PLANNER_MODEL_CHANGE_REQUIRED = NO (for CC01 frozen-state reconciliation)
CODEC_CHANGE_REQUIRED = NO (for CC01 frozen-state reconciliation)
MIGRATION_CONTRACT_CHANGE_REQUIRED = YES
M01_TARGET_CATEGORIES_AFFECTED = [Snapshot.budget_matrices; clarification only: Snapshot.evidence_requirements, Snapshot.external_gates, Snapshot.predicates, Snapshot.knowledge, Snapshot.assertions, Snapshot.receipt_admissions, Snapshot.receipt_observations, expected_external_absence_records, PersistenceBundle.sources, DerivationIndex, PersistenceBundle.initial, PersistenceBundle.current]
UPDATED_CONCEPTUAL_TARGET_COUNTS = {COMPLETE:12, INCOMPLETE:20, NOT_REQUIRED:3, TOTAL:35}
M01_CLOSURE_REENTRY_ALLOWED = YES
M01_CLOSURE_REENTRY_PREREQUISITES = [use reconciled frozen target crosswalk, preserve synthetic trust boundary, retain all six remaining M01 gap groups, separately qualify future positive admission]
M02_READY = NO
V0_1_CURRENT_STATUS = CORRECTION_REQUIRED
IMPLEMENTATION_MODIFIED = NO
E1_ARTIFACTS_MODIFIED = 0
REAL_E1_EVIDENCE_CREATED = NO
PRODUCTION_EFFECT = NO
```

Verification is limited to source/code inspection, the exact eight historical row statuses, mechanical 35-category recount and preservation checks. No migration, E1 action, receipt transition or real-E1 readiness test was executed. All 10,911 frozen files and all pre-existing files in the captured adapter/plans/backlog/E1 baseline retain their hashes. `git diff --check` passes. Only this new reconciliation document is added by this task.
