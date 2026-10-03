# C06A remaining operational contract 1

Analysis only. **17 finite contract elements: O13 and O14 are restored and qualified within their stated scopes; 15 elements have remaining full-import coverage. C07_RETRY_ALLOWED = NO.** This report neither changes the correction plan nor reopens F03. It proposes a bounded decomposition of the already required C06A work.

## Basis and counting

The IDs retain the reconciliation's O01–O17 inventory. O01–O15 are state/contract families; O16 is their checked import coverage and O17 their cold-restoration qualification. They are not 17 independent new runtime features. No additional state family is inferred from the phrase “full E1.” Qualified subparts of partial rows remain accepted.

Governing evidence: [reconciliation](DETERMINISTIC_PLANNER_V0_1_C06_C07_RECONCILIATION_1.md), [correction plan §6–9](DETERMINISTIC_PLANNER_V0_1_CORRECTION_PLAN_1.md), [first blocked attempt](DETERMINISTIC_PLANNER_V0_1_C06A_RESULT.md), [partial retry](DETERMINISTIC_PLANNER_V0_1_C06A_RETRY_1_RESULT.md), [retry coverage](DETERMINISTIC_PLANNER_V0_1_C06A_RETRY_1_COVERAGE.json), [independent budget oracle](DETERMINISTIC_PLANNER_V0_1_BUDGET_PROOF_MATRIX_ORACLE_1.md), [v0.1 requirement slice](DETERMINISTIC_PLANNER_V0_1_IMPLEMENTATION_PLAN.md), [backlog](../backlog/DETERMINISTIC_REASONING_PLANNING_RUNTIME.md), and [E1 traceability](../backlog/DETERMINISTIC_REASONING_PLANNING_RUNTIME_E1_TRACEABILITY.md). The companion JSON pins inspected bytes and retains every matrix field. A JSON source pointer containing `*` or braces denotes a field family to enumerate by canonical ID, not an executable JSON Pointer.

## What the code establishes

`adapter/planner/replay.py:381` (`import_e1`) verifies pins/schema/ID sets, then calls `load_p05_fixture` using the descriptor's M_P05 normalization. It restores the C06 accepted-knowledge requirements, but retains original graph records, history and manifest/checkpoint data through `retain` as `P06_PINNED_OPAQUE_RECORD`. Opaque bytes do not populate the absent operational predicates or decision dossiers. Merely retaining every record or matching 63 action IDs does not qualify its operative fields.

`model.Action`, `Snapshot`, `Decision`, `GraphEntity`, `EvidenceRequirement` and the existing `gates`/`core` evaluators provide reusable mechanisms. Their existence and the original A–N tests do not prove full source-driven restoration. `test_n_full_import_isolated_receipts_and_cold_reentry` and the N cold-process tests demonstrate reduced projection behavior; neither is an independent full-field inventory oracle.

The budget exception is concrete: `budget.validate_input`, `validate_restored`, `import_budget` and `test_planner_c06a` preserve the exact eight rows, typed envelope, governing/factual records, parameters, proof identity and19 dependencies. Tests inspect individual fields, bounded positive output, negatives, each source invalidation and cold permutations. This is `PARTIAL_SYNTHETIC_BUDGET_QUALIFICATION`, not full frozen E1. C05 policy binding has independent mutation/domain/version tests in `test_planner_resume.py`; C06 source-bound knowledge controls remain covered in `test_planner_c06.py`. The reported156 passing tests are prior RETRY_1 evidence, not tests rerun by this analysis.

## Required contract and remaining matrix

For each remaining row, the missing data/restoration and source binding are stated explicitly. “Type gap” means a missing mapping to the existing type unless a field proves unrepresentable; this analysis does not prescribe unnecessary new parallel types. Positive/negative tests below are qualification requirements, not assertions that they already pass.

### O01 — Action definition envelope

**Coverage:** PARTIALLY_RESTORED. **Scope:** V0_1_REQUIRED. **Oracle:** ORACLE_DERIVABLE_FROM_FROZEN_CONTRACT.

**Requirement:** Correction Plan §6; reconciliation O01; implementation-plan R01/R18. **Frozen/contract fields:** `docs/experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_PLAN_1.json#/resolution_actions/*/{id,primary_operation_class,executor,effect_boundary,stage_role,scope,actionability_scope}`.

**Persisted representation / importer / restoration:** Compile the named source fields into Action plus typed stage/scope/boundary contract; retain typed source identity and exact pointer; reconstruct after canonical reload without M_P05 state or manual patching.

**Exact remaining data/type/source gap:** Basic Action exists; complete frozen stage/scope/executor restriction mapping is absent. Source-derived contract binding is missing, not the ActionId type. Use existing typed destinations above first; missing source-to-type mapping does not prove a new type is needed. Add only a demonstrated unrepresentable contract field. Required source pin and exact field-to-destination provenance are incomplete for the remaining boundary.

**Validation and consumer:** Reject unsupported operation/stage, wrong scope, effect expansion and unresolved affected IDs. Consumer: `gates.blockers; core.recompute; selector`.

**Independent positive oracle/test:** Source-defined bounded action survives import with every operative boundary; alpha-renamed instance behaves identically.

**Negative oracle/test:** Omit scope or substitute governed effect and require rejection/hold, never default permission.

### O02 — Prerequisites and explicit holds

**Coverage:** PARTIALLY_RESTORED. **Scope:** V0_1_REQUIRED. **Oracle:** ORACLE_DERIVABLE_FROM_FROZEN_CONTRACT.

**Requirement:** Correction Plan §6; reconciliation O02; implementation-plan R01/R07/R20. **Frozen/contract fields:** `docs/experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_PLAN_1.json#/resolution_actions/*/{prerequisite_actions,external_prerequisites,knowledge_requirements,unresolved_prerequisites,reentry_gate,blocked_by_batch_review,blocking_result}`.

**Persisted representation / importer / restoration:** Compile the named source fields into Gate/Predicate/KnowledgeRecord and current hold provenance; retain typed source identity and exact pointer; reconstruct after canonical reload without M_P05 state or manual patching.

**Exact remaining data/type/source gap:** C06 typed source-bound non-PASS knowledge is qualified. Remaining original holds, batch overrides, external/current requirements are not completely source-mapped. Use existing typed destinations above first; missing source-to-type mapping does not prove a new type is needed. Add only a demonstrated unrepresentable contract field. Required source pin and exact field-to-destination provenance are incomplete for the remaining boundary.

**Validation and consumer:** All mandatory supports remain conjunctive; stale/absent source fails closed; accepted knowledge does not require producer completion. Consumer: `gates.blockers/evaluate_predicate; core.project`.

**Independent positive oracle/test:** Restore every original prerequisite plus accepted BLOCKED knowledge and current overlay holds.

**Negative oracle/test:** Stale one mandatory support, remove a hold or spoof historical completion; eligibility must not increase.

### O03 — Bounded result contracts

**Coverage:** PARTIALLY_RESTORED. **Scope:** V0_1_REQUIRED. **Oracle:** ORACLE_MISSING.

**Requirement:** Correction Plan §6; reconciliation O03; implementation-plan R01/R07/R18. **Frozen/contract fields:** `docs/experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_PLAN_1.json#/resolution_actions/*/{acceptance_criteria,completion_does_not_imply,closes_conditions_only_on_accepted_output,secondary_stages}`.

**Persisted representation / importer / restoration:** Compile the named source fields into Action accepted result/inventory and supported per-outcome rule bindings; retain typed source identity and exact pointer; reconstruct after canonical reload without M_P05 state or manual patching.

**Exact remaining data/type/source gap:** Non-budget frozen actions still inherit default PASS/empty inventory. Missing reviewed finite output schemas and their source bindings, not permission to accept arbitrary output. Budget positive is excluded from this gap. Use existing typed destinations above first; missing source-to-type mapping does not prove a new type is needed. Add only a demonstrated unrepresentable contract field. Required source pin and exact field-to-destination provenance are incomplete for the remaining boundary.

**Validation and consumer:** Exact allowed output type/source/outcome; no automatic root/slot promotion; unsupported required prose blocks. Consumer: `gates.validate_result; core._inventory/apply_result`.

**Independent positive oracle/test:** Independently define one source-supported non-budget bounded acquisition result and decision-preparation result; admit exact outputs after restore.

**Negative oracle/test:** Unknown output, incomplete output, wrong source/outcome and root promotion from PASS rejected.

### O04 — Action authority requirements

**Coverage:** NOT_RESTORED. **Scope:** V0_1_REQUIRED. **Oracle:** ORACLE_DERIVABLE_FROM_FROZEN_CONTRACT.

**Requirement:** Correction Plan §6; reconciliation O04; implementation-plan R17/R18. **Frozen/contract fields:** `docs/experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_PLAN_1.json#/resolution_actions/*/{authority_rule,accepted_decision_requirements,evidence}`.

**Persisted representation / importer / restoration:** Compile the named source fields into Authority predicates and scoped typed authority entities; retain typed source identity and exact pointer; reconstruct after canonical reload without M_P05 state or manual patching.

**Exact remaining data/type/source gap:** Native evaluator exists; full imported permission/target/exclusion/currentness requirements and source bindings absent. Use existing typed destinations above first; missing source-to-type mapping does not prove a new type is needed. Add only a demonstrated unrepresentable contract field. Required source pin and exact field-to-destination provenance are incomplete for the remaining boundary.

**Validation and consumer:** Construction permission cannot imply issuance/use; missing or stale authority blocks; content identity cannot substitute authority identity. Consumer: `gates.evaluate_predicate; actionability`.

**Independent positive oracle/test:** Restore granted bounded permission and independently retain exclusions/currentness gates.

**Negative oracle/test:** Wrong target, wrong identity domain, stale attestation or expanded permission does not authorize action.

### O05 — Decision readiness and dossiers

**Coverage:** NOT_RESTORED. **Scope:** V0_1_REQUIRED. **Oracle:** ORACLE_DERIVABLE_FROM_FROZEN_CONTRACT.

**Requirement:** Correction Plan §6; reconciliation O05; implementation-plan R04. **Frozen/contract fields:** `docs/experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_PLAN_1.json#/resolution_actions/*/{decision_readiness_requirements,readiness_gate,accepted_decision_requirements}; /decision_input_reentry_semantics; linked dossiers`.

**Persisted representation / importer / restoration:** Compile the named source fields into Decision/DecisionDossier/DecisionCheck and RecordedDecision/reentry bindings; retain typed source identity and exact pointer; reconstruct after canonical reload without M_P05 state or manual patching.

**Exact remaining data/type/source gap:** Actual frozen import does not populate Decision objects/checklists, alternatives, dossier source identities or chosen option contracts. Native F–I mechanisms already exist. Use existing typed destinations above first; missing source-to-type mapping does not prove a new type is needed. Add only a demonstrated unrepresentable contract field. Required source pin and exact field-to-destination provenance are incomplete for the remaining boundary.

**Validation and consumer:** Nine source-backed checklist facts, bounded alternatives, interference and accepted choice checked separately; fact absence remains FACT_BLOCKED. Consumer: `gates.decision_readiness/recorded_decision_valid; core._human_batches/apply_decision_reentry`.

**Independent positive oracle/test:** Restore already issued DEC-BUDGET choice/dossier (no new issuance); separate synthetic source-derived ready dossier enables review only.

**Negative oracle/test:** Delete factual input, change dossier hash/choice, or set AUTHORITY_REQUIRED alone: no readiness/reentry.

### O06 — Historical attempts and current overlays

**Coverage:** PARTIALLY_RESTORED. **Scope:** V0_1_REQUIRED. **Oracle:** ORACLE_DERIVABLE_FROM_FROZEN_CONTRACT.

**Requirement:** Correction Plan §6; reconciliation O06; implementation-plan R01/R07/R15. **Frozen/contract fields:** `docs/experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_PLAN_1.json#/execution_history; /execution_state; /resolution_actions/*/execution_result; docs/experiments/E1/E1_RESUME_MANIFEST_1.json#/execution_result_artifacts`.

**Persisted representation / importer / restoration:** Compile the named source fields into Authenticated historical attempt records, KnowledgeRecord and ActionStatus overlay lineage; retain typed source identity and exact pointer; reconstruct after canonical reload without M_P05 state or manual patching.

**Exact remaining data/type/source gap:** Native event ledger and three accepted knowledge dependencies work; complete imported attempt/outcome/source and hold-overlay cross-check absent. Old history stays historical, not invented native events. Use existing typed destinations above first; missing source-to-type mapping does not prove a new type is needed. Add only a demonstrated unrepresentable contract field. Required source pin and exact field-to-destination provenance are incomplete for the remaining boundary.

**Validation and consumer:** Join attempts to pinned results and current overlays; reject contradictory status/result/source/lineage; retain causal order. Consumer: `current_completion; blockers; source invalidation; replay admission`.

**Independent positive oracle/test:** Historical BLOCKED knowledge stays usable when current; later accepted overlay does not erase earlier attempts.

**Negative oracle/test:** Spoof COMPLETED summary or reorder conflicting history: reject before planner use.

### O07 — Receipt and decision reentry routes

**Coverage:** PARTIALLY_RESTORED. **Scope:** V0_1_REQUIRED. **Oracle:** ORACLE_DERIVABLE_FROM_FROZEN_CONTRACT.

**Requirement:** Correction Plan §6; reconciliation O07; implementation-plan R07/R15. **Frozen/contract fields:** `docs/experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_PLAN_1.json#/decision_input_reentry_semantics; /budget_applicability_reentry_semantics; /resolution_actions/*/reentry_on_accepted_evidence; docs/experiments/E1/E1_RESUME_MANIFEST_1.json#/request_routes`.

**Persisted representation / importer / restoration:** Compile the named source fields into ExternalGate/DecisionReentry/ExternalEvent with typed route and new-attempt binding; retain typed source identity and exact pointer; reconstruct after canonical reload without M_P05 state or manual patching.

**Exact remaining data/type/source gap:** Generic routes exist; all eight named request-to-dependent routes plus original holds/result contracts are not restored operationally. Use existing typed destinations above first; missing source-to-type mapping does not prove a new type is needed. Add only a demonstrated unrepresentable contract field. Required source pin and exact field-to-destination provenance are incomplete for the remaining boundary.

**Validation and consumer:** Accepted evidence must cover exact route and current original prerequisites; partial/negative receipt cannot grant reentry. Consumer: `core.apply_receipt/apply_decision_reentry/resume_eligibility`.

**Independent positive oracle/test:** Synthetic admissible input releases only its declared reentry attempt, preserving original conditions.

**Negative oracle/test:** Unrelated receipt, wrong route/attempt, stale support and fact-incomplete decision do not reopen.

### O08 — Root completion obligations

**Coverage:** PARTIALLY_RESTORED. **Scope:** V0_1_REQUIRED. **Oracle:** ORACLE_DERIVABLE_FROM_FROZEN_CONTRACT.

**Requirement:** Correction Plan §6; reconciliation O08; implementation-plan R01/R18. **Frozen/contract fields:** `docs/experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_PLAN_1.json#/normalized_root_conditions/*/{graph_prerequisites,condition_completion_rule,required_authority,evidence}; /deferred_conditions`.

**Persisted representation / importer / restoration:** Compile the named source fields into RootCondition predicates/evidence with cut/deferred classification; retain typed source identity and exact pointer; reconstruct after canonical reload without M_P05 state or manual patching.

**Exact remaining data/type/source gap:** Root IDs and generic satisfaction exist; full source-derived independent completion rules/ancestors and proof bindings missing. Use existing typed destinations above first; missing source-to-type mapping does not prove a new type is needed. Add only a demonstrated unrepresentable contract field. Required source pin and exact field-to-destination provenance are incomplete for the remaining boundary.

**Validation and consumer:** Count cut roots separately from deferred conditions; require all independent proof, never final action PASS alone. Consumer: `core.evaluate_satisfaction; global goal evaluation`.

**Independent positive oracle/test:** Source-supported satisfied root remains satisfied only with all typed current support; unresolved/unknown rules remain explicit.

**Negative oracle/test:** Remove one ancestor/proof or change counted/deferred membership; reject incomplete import or keep unresolved, never silently satisfy.

### O09 — Slot pipelines and baseline values

**Coverage:** PARTIALLY_RESTORED. **Scope:** V0_1_REQUIRED. **Oracle:** ORACLE_DERIVABLE_FROM_FROZEN_CONTRACT.

**Requirement:** Correction Plan §6; reconciliation O09; implementation-plan R17/R18/R20. **Frozen/contract fields:** `docs/experiments/E1/E1_TEMPLATE1_TYPED_KNOWLEDGE_GRAPH_1.json#/entities[entity_type=TEMPLATE1_SLOT]`.

**Persisted representation / importer / restoration:** Compile the named source fields into ValueSlot plus typed source/producer/transformation/authority/validator/consumer links; retain typed source identity and exact pointer; reconstruct after canonical reload without M_P05 state or manual patching.

**Exact remaining data/type/source gap:** Slot IDs/state/type alone are restored; mandatory pipeline links, accepted two baseline values with exact resolution scope and complete source bindings absent. Use existing typed destinations above first; missing source-to-type mapping does not prove a new type is needed. Add only a demonstrated unrepresentable contract field. Required source pin and exact field-to-destination provenance are incomplete for the remaining boundary.

**Validation and consumer:** Unknown producer/mapping remains absence; type domains distinct; all mandatory support required for resolution. Consumer: `slot predicates; core.evaluate_satisfaction`.

**Independent positive oracle/test:** Restore all43 slot contracts, two evidenced baseline resolutions and41 independently unresolved obligations.

**Negative oracle/test:** Delete mapping or substitute identity domain; same slot count is insufficient; fail closed.

### O10 — Operational graph and provenance

**Coverage:** PARTIALLY_RESTORED. **Scope:** V0_1_REQUIRED. **Oracle:** ORACLE_DERIVABLE_FROM_FROZEN_CONTRACT.

**Requirement:** Correction Plan §6; reconciliation O10; implementation-plan R18/R20. **Frozen/contract fields:** `docs/experiments/E1/E1_TEMPLATE1_TYPED_KNOWLEDGE_GRAPH_1.json#/entities; /assertions; /relation_semantics; /synchronization`.

**Persisted representation / importer / restoration:** Compile the named source fields into GraphEntity/GraphAssertion/Predicate with provenance and required-support edges; retain typed source identity and exact pointer; reconstruct after canonical reload without M_P05 state or manual patching.

**Exact remaining data/type/source gap:** Frozen records retained opaque; operative relations/source acceptance/scope/lineage/currentness not completely mapped. Native graph/ref/stale mechanisms qualified separately. Use existing typed destinations above first; missing source-to-type mapping does not prove a new type is needed. Add only a demonstrated unrepresentable contract field. Required source pin and exact field-to-destination provenance are incomplete for the remaining boundary.

**Validation and consumer:** Only ordering REQUIRES edges project to prerequisites; typed endpoints, accepted extraction, current support and transitive invalidation enforced. Consumer: `core.project; gates; codec.invalidate_sources`.

**Independent positive oracle/test:** Import supported operational relations with exact source pointers, preserve descriptive relations without ordering effect.

**Negative oracle/test:** Dangling/wrong-domain edge, stale required support, semantic correspondence promoted to ordering: reject or block.

### O11 — Issued authority and subject bindings

**Coverage:** PARTIALLY_RESTORED. **Scope:** V0_1_REQUIRED. **Oracle:** ORACLE_DERIVABLE_FROM_FROZEN_CONTRACT.

**Requirement:** Correction Plan §6; reconciliation O11; implementation-plan R15/R17/R18. **Frozen/contract fields:** `docs/experiments/E1/E1_RESUME_MANIFEST_1.json#/architect_records; /candidate3_construction_authority; /subject_pins; docs/experiments/E1/E1_SUSPENSION_CHECKPOINT_1.json#/bindings`.

**Persisted representation / importer / restoration:** Compile the named source fields into Typed authority/content identities, choice/dossier/subject/scope/exclusion and historical consumption evidence; retain typed source identity and exact pointer; reconstruct after canonical reload without M_P05 state or manual patching.

**Exact remaining data/type/source gap:** Raw pins retained; complete imported decision/authority contract bindings and candidate-only unconsumed status not operationally restored. Use existing typed destinations above first; missing source-to-type mapping does not prove a new type is needed. Add only a demonstrated unrepresentable contract field. Required source pin and exact field-to-destination provenance are incomplete for the remaining boundary.

**Validation and consumer:** Hash authenticates bytes, not a new grant; distinguish historical validity/unconsumed from current applicability. Consumer: `authority predicates; recorded_decision_valid; resume scope binding`.

**Independent positive oracle/test:** Restore issued choices and Candidate-3 recorded VALID_UNCONSUMED with original limitations.

**Negative oracle/test:** Substitute authority/content identity, dossier, target or claim issuance permission: reject.

### O12 — All external frontier evidence contracts

**Coverage:** PARTIALLY_RESTORED. **Scope:** V0_1_REQUIRED. **Oracle:** ORACLE_DERIVABLE_FROM_FROZEN_CONTRACT.

**Requirement:** Correction Plan §6; reconciliation O12; implementation-plan R07/R15. **Frozen/contract fields:** `docs/experiments/E1/E1_EXTERNAL_HANDOFF_PACKAGE_1.json#/control_transfer_items; /external_request_bundles; /common_evidence_contract; /resume_rule; docs/experiments/E1/E1_RESUME_MANIFEST_1.json#/request_routes`.

**Persisted representation / importer / restoration:** Compile the named source fields into EvidenceRequirement/ExternalGate/ControlBoundary/ReceiptAdmission contract; retain typed source identity and exact pointer; reconstruct after canonical reload without M_P05 state or manual patching.

**Exact remaining data/type/source gap:** Endpoint holds and budget substrate exist; seven other full contract mappings and cross-link of frozen budget waiting route to absence are incomplete. Missing producer competence remains an explicit gate, not invented producer. Use existing typed destinations above first; missing source-to-type mapping does not prove a new type is needed. Add only a demonstrated unrepresentable contract field. Required source pin and exact field-to-destination provenance are incomplete for the remaining boundary.

**Validation and consumer:** Per-proposition identity/scope/lineage/freshness/authentication requirements; unavailable source and unresolved rule distinct; no external retrieval. Consumer: `gates.check_receipt/external_complete; core._global_control`.

**Independent positive oracle/test:** Restore all eight frontier contracts as missing evidence, preserving fact-blocked decisions and named owners/unknowns.

**Negative oracle/test:** Unrelated or partially matching bundle must not release a gate; negative/stale evidence preserved, not repaired.

### O13 — Qualified synthetic budget proof profile

**Coverage:** RESTORED_AND_QUALIFIED. **Scope:** V0_1_REQUIRED. **Oracle:** ORACLE_COMPLETE.

**Requirement:** Correction Plan §6; reconciliation O13; implementation-plan R07/R17/R18. **Frozen/contract fields:** `docs/plans/DETERMINISTIC_PLANNER_V0_1_BUDGET_PROOF_MATRIX_ORACLE_1.json#/qualification_parameters; /positive_submission`.

**Persisted representation / importer / restoration:** Compile the named source fields into BudgetProofMatrix/BudgetEnvelope/BudgetProofRow and19 required source assertions; retain typed source identity and exact pointer; reconstruct after canonical reload without M_P05 state or manual patching.

**Exact remaining data/type/source gap:** NONE within registered synthetic profile. Actual frozen association/absence belongs to O04/O07/O11/O12; this does not require synthetic proof for E1. Use existing typed destinations above first; missing source-to-type mapping does not prove a new type is needed. Add only a demonstrated unrepresentable contract field. No missing binding within qualified scope.

**Validation and consumer:** Eight rows, authentication, governing rules, exact envelope, source currentness and parameter pin; invalidation survives reload. Consumer: `budget.validate_input/validate_restored; native predicates and result gate`.

**Independent positive oracle/test:** Existing independent oracle, field-by-field restoration and bounded result tests.

**Negative oracle/test:** Existing negative matrix and every required source invalidation; retain refined BLOCKED-producer control.

### O14 — Selection-policy binding

**Coverage:** RESTORED_AND_QUALIFIED. **Scope:** V0_1_REQUIRED. **Oracle:** ORACLE_COMPLETE.

**Requirement:** Correction Plan §6; reconciliation O14; implementation-plan R02/R15/R20. **Frozen/contract fields:** `docs/experiments/E1/E1_RESUME_MANIFEST_1.json#/embedded_selection_policy; docs/experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_PLAN_1.json#/selection_policy; docs/experiments/E1/E1_SUSPENSION_CHECKPOINT_1.json#/bindings`.

**Persisted representation / importer / restoration:** Compile the named source fields into ArtifactPin plus supported policy version/static mapping; retain typed source identity and exact pointer; reconstruct after canonical reload without M_P05 state or manual patching.

**Exact remaining data/type/source gap:** NONE in C05 qualified scope; extend importer without bypassing registered policy validation. Use existing typed destinations above first; missing source-to-type mapping does not prove a new type is needed. Add only a demonstrated unrepresentable contract field. No missing binding within qualified scope.

**Validation and consumer:** Exact identity/domain/version/map and deterministic fallback; reject substitution. Consumer: `selector.validate_policy/select; codec bundle admission`.

**Independent positive oracle/test:** Existing registered policy executes reproducibly through reload.

**Negative oracle/test:** Existing C05 policy mutation/version/domain/stale tests.

### O15 — Goals, control and suspension inputs

**Coverage:** PARTIALLY_RESTORED. **Scope:** V0_1_REQUIRED. **Oracle:** ORACLE_DERIVABLE_FROM_FROZEN_CONTRACT.

**Requirement:** Correction Plan §6; reconciliation O15; implementation-plan R15/R22. **Frozen/contract fields:** `docs/experiments/E1/E1_SUSPENSION_CHECKPOINT_1.json#/state; /resume_condition; docs/experiments/E1/E1_RESUME_MANIFEST_1.json#/resume_rule; /mismatch_rule; docs/experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_PLAN_1.json#/preflight_protocol; /excluded_post_readiness_operations`.

**Persisted representation / importer / restoration:** Compile the named source fields into Goal/full-run scope, ControlBoundary, waiting state and C03 persisted resume proof inputs; retain typed source identity and exact pointer; reconstruct after canonical reload without M_P05 state or manual patching.

**Exact remaining data/type/source gap:** Reduced M goals/control operate; independent complete required-goal inventory and suspension constraints not source-derived. Summary counts/control are comparison oracles only. Use existing typed destinations above first; missing source-to-type mapping does not prove a new type is needed. Add only a demonstrated unrepresentable contract field. Required source pin and exact field-to-destination provenance are incomplete for the remaining boundary.

**Validation and consumer:** All required goals/branches accounted; no input evidence implies no resume; partial snapshots distinct from full run; excluded constructions stay excluded. Consumer: `core._global_control/resume_eligibility`.

**Independent positive oracle/test:** Source-derived full snapshot computes frontier/control; separately compare report values; synthetic partial goal can succeed.

**Negative oracle/test:** Delete required goal/branch, insert unrelated receipt or make waiting gate alone a resume proof: reject/no resume.

### O16 — Versioned source-field coverage and importer

**Coverage:** NOT_RESTORED. **Scope:** V0_1_REQUIRED. **Oracle:** ORACLE_DERIVABLE_FROM_FROZEN_CONTRACT.

**Requirement:** Correction Plan §6; reconciliation O16; implementation-plan R20/P06. **Frozen/contract fields:** `docs/experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_PLAN_1.json; docs/experiments/E1/E1_TEMPLATE1_TYPED_KNOWLEDGE_GRAPH_1.json; docs/experiments/E1/E1_RESUME_MANIFEST_1.json; docs/experiments/E1/E1_EXTERNAL_HANDOFF_PACKAGE_1.json; docs/experiments/E1/E1_SUSPENSION_CHECKPOINT_1.json`.

**Persisted representation / importer / restoration:** Compile the named source fields into Pinned reviewed mapping plus per-field disposition/acceptance/source/destination inventory; retain typed source identity and exact pointer; reconstruct after canonical reload without M_P05 state or manual patching.

**Exact remaining data/type/source gap:** Complete independent inventory absent; N descriptor still loads M_P05 executable normalization. Budget coverage explicitly partial. Use existing typed destinations above first; missing source-to-type mapping does not prove a new type is needed. Add only a demonstrated unrepresentable contract field. Required source pin and exact field-to-destination provenance are incomplete for the remaining boundary.

**Validation and consumer:** Every required field ENFORCED or genuinely unavailable with enforced hold; unsupported necessary semantics blocks completion; descriptive opaque allowed with reason. Consumer: `replay.import_e1; model.validate_model; codec admission`.

**Independent positive oracle/test:** Two supported source-shaped instances map independently without M state; exact pointer inventory compared, not just counts.

**Negative oracle/test:** Unknown required field, omitted operative rule, missing source-manifest member, blanket unsupported and same-count substitution rejected.

### O17 — Full semantic cold-restoration qualification

**Coverage:** PARTIALLY_RESTORED. **Scope:** V0_1_REQUIRED. **Oracle:** ORACLE_DERIVABLE_FROM_FROZEN_CONTRACT.

**Requirement:** Correction Plan §6; reconciliation O17; implementation-plan R15/R22/P06. **Frozen/contract fields:** `Correction Plan §§8–9; docs/experiments/E1/E1_RESUME_MANIFEST_1.json; docs/experiments/E1/E1_SUSPENSION_CHECKPOINT_1.json`.

**Persisted representation / importer / restoration:** Compile the named source fields into Canonical operational bundle plus independent field and semantic output evidence; retain typed source identity and exact pointer; reconstruct after canonical reload without M_P05 state or manual patching.

**Exact remaining data/type/source gap:** Native/reduced N and synthetic budget cold reload qualified; full source-derived semantic restoration and positive decision/continuation coverage not qualified. This is an acceptance element, not a seventeenth domain data family. Use existing typed destinations above first; missing source-to-type mapping does not prove a new type is needed. Add only a demonstrated unrepresentable contract field. Required source pin and exact field-to-destination provenance are incomplete for the remaining boundary.

**Validation and consumer:** Fresh processes need only pinned artifacts; full member equality plus correct consumers; no actions/effects on real E1. Consumer: `codec.restore; replay.plan_output; CLI`.

**Independent positive oracle/test:** C06A source-shaped synthetic complete cold import and renamed continuation; C07 owns final actual N-REAL/requalification/review.

**Negative oracle/test:** Omitted member despite equal control scalar, stale source, policy substitution, or process-memory dependence fails.

## Oracle availability and stop boundary

ORACLE_COMPLETE = [O13, O14]. ORACLE_MISSING = [O03: independently serialized non-budget per-outcome acceptance schemas]. All other rows have governing requirements derivable from the frozen contracts, but their complete independent field-by-field executable oracle has not yet been delivered. “Derivable” is not “qualified.” O03's gap is the finite machine acceptance specification, not proof that the source prose has no governing meaning. C06A-2 must identify the exact supported outputs and predicates before any repair; if it cannot, that dependent work remains blocked with a specific unresolved rule. Implementation output must not fill the gap.

No new budget oracle is required. Reuse its registered synthetic scope without interpreting it as actual authority. Real external facts for the eight handoffs are EXTERNAL_EVIDENCE_REQUIRED, but their absence is a complete negative/waiting-state oracle. Qualification of waiting must not wait for their arrival. An unknown producer or rule must be represented as unknown; a positive receipt requiring that unknown rule cannot be invented merely to cover a test. Supported synthetic continuation tests use explicitly source-supported bounded contracts, with qualification evidence labelled synthetic.

## Finite scope: operational, reporting, historical and absent

| Class | Required handling | Examples / limit |
|---|---|---|
| A — operational | Restore only values/rules consumed by actionability, proof, readiness, selection, control or resume, with typed source bindings | O01–O15 operative subset; accepted baseline slots and current holds; all eight frontier routes; authority exclusions; no whole artifact database |
| B — reporting | Pin and compare after independent computation; do not feed expected answers into gates | Counts27/41, reported MIXED_WAIT, empty actionable/decision lists, titles and WP labels; preserve human-readable details by reference |
| C — historical | Keep raw pin/pointer and accepted attempt/outcome identity; load only needed current overlays and knowledge dependencies | Old dossiers/results, prerequisite baseline and proposed DAG corrections; do not execute historical events again or apply proposed topology corrections |
| D — intentionally absent | Persist unsatisfied requirement and gate, never synthesize positive evidence | Budget currentness/applicability, ancestry, approval, audit/R4/supervisor inputs, independent exec policy, implementation source/selector |

A historical record's authority exclusion is class A when it constrains a current action. A descriptive key is not automatically class B if its contents contain a governing rule. All source-manifest entries need an accounting disposition, not necessarily loaded operational payloads. Byte-preservation checks over10,911 files do not turn those files into a planner database.

DEFERRED: GraphRAG/LLM extraction, general artifact databases, external evidence retrieval, online trust services and optimization. NOT_REQUIRED: executing E1 actions, acquiring missing facts to prove a waiting state, recreating all historical objects/events in memory, or implementing arbitrary future prose contracts. Necessary unsupported semantics block completion; arbitrary unrepresented future capability does not become a v0.1 requirement.

## Bounded closure packages

These are proposed C06A subpackages, not executed or silently added to execution state. Five boundaries are used: independent contract specification, shared source admission, decision/authority binding, receipt/reentry binding, and full-scope composition. C06A-4 and C06A-5 are independent after C06A-3; their shared core is not duplicated. C06A-2 lists all remaining rows because it specifies their source map, not because it implements them.

### C06A-2 — Finite mapping and non-budget result-oracle definition

**PREREQUISITES:** accepted C06A reconciliation and RETRY_1 scope

**CONTRACT_ELEMENTS:** O01, O02, O03, O04, O05, O06, O07, O08, O09, O10, O11, O12, O15, O16, O17

**ORACLE:** Derive exact pointer/rule/destination inventory from frozen contracts; complete O03 independent per-outcome positive/negative schemas before implementation. This is specification work, not implementing all listed elements.

**PRE_REPAIR_COUNTEREXAMPLE:** Define source-shaped independently accepted non-budget result and decision-dossier restoration probes. A probe that merely tests empty PASS is invalid. Pin expected field records and prohibited transitions before calling importer.

**IMPLEMENTATION:** NONE. Define reviewed finite mapping version, required/optional keys, scoped positive contracts and missing-fact holds; identify any genuinely undefined acceptance rule and stop that dependent package.

**TESTS:** Contract consistency review: every O row/required pointer covered; alternatives and root criteria do not come from implementation; oracle mutations; no descriptive field promoted to authority.

**ACCEPTANCE:** Independent source-field inventory and executable specification complete. O03 ORACLE_MISSING discharged or exact remaining rule documented; no speculative implementation authorized by a prose umbrella.

**UNLOCKS:** C06A-3

### C06A-3 — Source-driven graph, action and history admission

**PREREQUISITES:** C06A-2 PASS

**CONTRACT_ELEMENTS:** O01, O02, O03, O06, O08, O09, O10, O16

**ORACLE:** C06A-2 pinned inventory; existing native typed/reference/stale invariants; budget profile reused unchanged.

**PRE_REPAIR_COUNTEREXAMPLE:** Source-shaped supported action/output and operative graph/slot fields survive raw pin checks but current import loses fields/defaults result inventory or depends on M. Demonstrate missing positive contract through actual result gate, then member-by-member loss.

**IMPLEMENTATION:** Replace M executable dependency in replay.import_e1 with finite mapping to existing model/codec. Restore history overlay and independent root/slot proof contracts; add bounded fields only when demonstrated. Do not create parallel planner or execute E1.

**TESTS:** Non-budget valid bounded result; missing/wrong/unknown field; stale transitive prerequisites; historical overlay conflict; two baseline slot proofs; missing goal-source record; renamed/supported alternative source instance; C06 regression.

**ACCEPTANCE:** Assigned fields survive canonical round trip; required predicates source-bound; unsupported required semantics explicit and block completion; no root/slot promotion from result; field inventory complete for assigned rows.

**UNLOCKS:** C06A-4, C06A-5

### C06A-4 — Decision and authority contract restoration

**PREREQUISITES:** C06A-3 PASS

**CONTRACT_ELEMENTS:** O04, O05, O11

**ORACLE:** C06A-2 source-derived nine readiness checks, pinned dossiers/issued choices, exact scope/exclusions; existing decision APIs are mechanisms, not oracle.

**PRE_REPAIR_COUNTEREXAMPLE:** Full source-shaped import cannot reconstruct supported dossier/choice/authority requirements; compare actual members and attempt synthetic permitted decision reentry versus incomplete dossier. Never issue a real decision.

**IMPLEMENTATION:** Map existing Decision/Dossier and authority predicates/identity domains from pinned records; preserve historical consumed/unconsumed facts and separate current applicability requirements.

**TESTS:** Supported dossier/recorded choice reload; missing facts, wrong choice/dossier, wrong authority domain/scope and stale binding; independent batching; negative construct-to-issue substitution.

**ACCEPTANCE:** All source-supported choices/readiness/permissions represented and independently tested; fact-blocked decisions remain blocked; no new authority.

**UNLOCKS:** C06A-6

### C06A-5 — Handoff receipts and branch reentry restoration

**PREREQUISITES:** C06A-3 PASS

**CONTRACT_ELEMENTS:** O07, O12

**ORACLE:** C06A-2 mapping of eight manifest request routes and H contracts, plus retained budget oracle. Unknown producer/rule must remain explicit unavailable input.

**PRE_REPAIR_COUNTEREXAMPLE:** Source-shaped handoff import lacks required evidence/route member although endpoint IDs/control count match; synthetic unrelated/partial receipt must not unlock route.

**IMPLEMENTATION:** Populate existing external evidence requirements, named receipts, lineage and hold contracts; preserve no-evidence state and budget source-bound prerequisite. Readiness integration consumes C06A-4; no real evidence acquisition.

**TESTS:** Eight absence states, wrong/partial/stale/unrelated receipt; source-backed supported synthetic route; missing normative rule stays blocked; branch-local waiting and valid knowledge from BLOCKED producer.

**ACCEPTANCE:** All frontier contract members restored, missing competence explicitly gated; supported receipt reenters only correct branch; no blanket unsupported substitute for known rules.

**UNLOCKS:** C06A-6

### C06A-6 — Full-scope composition and cold-restoration coverage

**PREREQUISITES:** C06A-4 PASS, C06A-5 PASS, O13/O14 regression evidence valid for candidate revision

**CONTRACT_ELEMENTS:** O15, O17

**ORACLE:** C06A-2 independent full-goal/field inventory and suspension contract; report scalars used only after computation.

**PRE_REPAIR_COUNTEREXAMPLE:** Delete a required operational field/goal while preserving aggregate ID counts and reported MIXED_WAIT; importer must reject, not declare full restored scope.

**IMPLEMENTATION:** Compose restored contracts into existing full-run bundle and resume proof; finish finite coverage validator. No new domain capability and no actual E1 action.

**TESTS:** Source-shaped synthetic full cold import/renamed continuation+decision; complete semantic member equality; keys/set orders/seeds/new processes; A–N/X01–X11/C01–C06 regression and10911-file preservation. Prepare actual N-REAL path, do not perform C07 final readiness here.

**ACCEPTANCE:** All17 elements within declared scope restored and qualified at pinned candidate revision; no necessary unsupported acceptance semantics; new aggregate C06A closure result PASS; finite retry predicate passes. Historical partial/blocked artifacts unchanged.

**UNLOCKS:** C07 retry only

## Minimum real frozen-E1 readiness boundary

The eventual readiness path needs: pinned graph/plan/manifest/checkpoint/policy and relevant sources; complete source-derived action prerequisites/current overlays; independent root/slot and full-goal inventory; issued decisions and authority restrictions; all eight unsatisfied receipt contracts and reentry lineage; source validity and accepted-knowledge bindings; and persisted no-receipt/suspension inputs. Native replay/persistence machinery is reused. Descriptive history stays referenced.

It must derive the eight-member control-transfer frontier:

1. EXT-BUDGET-APPLICABILITY-EVIDENCE
2. EXT-REENTRY-S-ANCESTRY
3. EXT-REENTRY-S-APPROVAL
4. EXT-REENTRY-PREP-AUDIT
5. EXT-REENTRY-PREP-RUNTIME_HEAD
6. EXT-REENTRY-PREP-SUPERVISOR
7. EXT-REENTRY-DEC-EXEC
8. IMPLEMENTATION-OWNING-SOURCE + IMPLEMENTATION-SELECTOR

The manifest's eight request routes are the bindings; the eighth frontier member is a compound fact requirement, not permission to add a ninth received bundle. Compute blocked/waiting branches and decision readiness before comparing to the frozen report. No accepted receipt means no newly eligible reentry; the suspended current state must yield MIXED_WAIT, no runnable internal action, no decision-ready action and resume=false. Preserve Candidate-3 historical VALID_UNCONSUMED without promoting it to runtime applicability. Counts27/41 and the two accepted slots are checked independently against the source inventory.

This analysis did not call the real importer, resume path, or readiness test. C06A composition qualifies source-shaped synthetic cold restoration and prepares the real contract path. **C07 itself owns the actual N-REAL readiness test, integrated section9 requalification and fresh independent adversarial review.** They are not waived or deferred past a C07 PASS. C07 retry readiness is not qualification; requiring C07's own final review before permitting its retry would be circular.

## Finite C07 retry predicate

Each term below must have evidence bound to the same candidate code/mapping/test/source identities. A missing/mismatched term is FALSE. O13/O14 retain their bounded existing acceptance, but integration regressions must cover the candidate revision; partial synthetic scope cannot be relabelled full.

```text
C07_RETRY_ALLOWED =
    explicit_C06A_scope_adoption_without_section9_waiver
    AND accepted_C01_C06_result_pins_and_F03_CLOSED
    AND all_O01_to_O17_required_scope_coverage_tests_PASS_at_candidate_code_mapping_source_identities
    AND all_required_positive_negative_oracles_complete
    AND no_UNSUPPORTED_REQUIRED_acceptance_gap_or_opaque_operational_field
    AND C06A_aggregate_closure_result_PASS_preserving_attempt_history
    AND A_N_X01_X11_C01_C06_and_refined_C06_regressions_PASS_same_revision
    AND canonical_cold_synthetic_full_contract_and_ordering_determinism_PASS_same_revision
    AND all_10911_E1_and_protected_artifact_hashes_unchanged
    AND deferred_scope_violations_zero
```

The quantified O01–O17 term means this report's17 named elements and the C06A-2 enumerated required source fields, not an open-ended “everything in E1” condition. Every field has one explicit disposition: ENFORCED; EXPLICITLY_UNAVAILABLE with an enforced unsatisfied gate; UNSUPPORTED_REQUIRED (fails retry); OPAQUE_NON_OPERATIONAL with documented reason. No operative field may take the last disposition. Presence of expected unknown external facts does not fail retry; missing semantics for representing/enforcing that absence does.

Current evaluation: FALSE. O01–O12 and O15–O17 are incomplete, the non-budget positive result specification is not independently established, and no aggregate C06A closure PASS exists. Original C06/C06A blocked attempts, refinement, accepted F03 repair and partial retry remain historical evidence. F03 stays CLOSED; this report does not independently rerun or requalify it.

## Report

```text
TOTAL_REQUIRED_CONTRACT_ELEMENTS = 17
RESTORED_AND_QUALIFIED = [O13 (synthetic budget profile), O14 (selection policy)]
REMAINING_OPERATIONAL_CONTRACT = [O01, O02_remaining, O03_nonbudget, O04, O05, O06_remaining, O07_remaining, O08, O09, O10_operational, O11_operational, O12_full_frontier, O15, O16, O17]
ORACLE_COMPLETE = [O13, O14]
ORACLE_MISSING = [O03 independent non-budget per-outcome schemas]
EXTERNAL_EVIDENCE_REQUIRED = [eight real handoff bundles; not required to qualify their suspended absence]
CLOSURE_PACKAGES = [C06A-2, C06A-3, C06A-4, C06A-5, C06A-6]
NEXT_PACKAGE = C06A-2 (contract/oracle definition only)
C07_RETRY_ALLOWED = NO
F03_STATUS = CLOSED
V0_1_CURRENT_STATUS = CORRECTION_REQUIRED
IMPLEMENTATION_MODIFIED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
```

## Analysis validation

JSON counts, source hashes, internal links and whitespace checks passed; `git diff --check` passed. Baseline byte comparison found no pre-existing file changed, including all10,911 E1 files, implementation, tests and protected documents. Only this report and its companion matrix were added. No implementation tests, real-E1 readiness test or planner actions were executed.
