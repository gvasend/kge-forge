# Frozen E1 minimum sufficient state analysis 1

**A bounded current-control projection is the right dependency target; a complete historical reconstruction is not.** The existing native API nevertheless requires an admitted Snapshot and PersistenceBundle, not a standalone list of blocked branches. All63 action identities/statuses must be accounted for to prove the universal empty-actionability claim; the native API requires corresponding typed Action objects. This does **not** prove that every prospective output contract or historical result needs reconstruction to establish the frozen conclusions.

The analysis identifies ten state components and five unresolved contract interfaces. It does not construct a qualified canonical snapshot or prove a minimum-cardinality graph. Exact instance minimization is currently blocked by missing source-to-native predicate/goal mappings. A conservative transitive dependency specification and exact source routing inventory are supplied instead of inventing that mapping.

No migration target or admission contract is modified. M02 remains disallowed. The current35-target contract coverage (13 complete,19 incomplete,3 not required) is historical input, not changed by the different dependency classifications below.

## Inputs and outputs

Governing scope: [migration plan](DETERMINISTIC_PLANNER_V0_1_E1_MIGRATION_IMPLEMENTATION_PLAN_1.md), [acceptance matrix](DETERMINISTIC_PLANNER_V0_1_E1_MIGRATION_ACCEPTANCE_MATRIX_1.md), [original M01](DETERMINISTIC_PLANNER_V0_1_E1_MIGRATION_M01_RESULT.md), [closure1](DETERMINISTIC_PLANNER_V0_1_E1_MIGRATION_M01_CLOSURE_1.md), [CC01](DETERMINISTIC_PLANNER_V0_1_M01_CC01_BUDGET_REPRESENTATION_RECONCILIATION_1.md), [retry1](DETERMINISTIC_PLANNER_V0_1_E1_MIGRATION_M01_CLOSURE_RETRY_1.md) and its target/contract/preflight companions.

Executable evidence: [core.py](../../adapter/planner/core.py), [gates.py](../../adapter/planner/gates.py), [model.py](../../adapter/planner/model.py), [codec.py](../../adapter/planner/codec.py). Source evidence: frozen [plan](../experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_PLAN_1.json), [manifest](../experiments/E1/E1_RESUME_MANIFEST_1.json), [global-control record](../experiments/E1/E1_GLOBAL_CONTROL_RECOMPUTATION_1.json), and the exact eight source-bound absence records retained by the [retry contract](DETERMINISTIC_PLANNER_V0_1_E1_MIGRATION_M01_CLOSURE_RETRY_1_CONTRACT.json).

Additive machine-readable analysis:

- [Backward/transitive dependency cone](DETERMINISTIC_PLANNER_V0_1_FROZEN_MINIMUM_SUFFICIENT_STATE_1_DEPENDENCY_CONE.json).
- [All35 targets and all19 incomplete-target dispositions](DETERMINISTIC_PLANNER_V0_1_FROZEN_MINIMUM_SUFFICIENT_STATE_1_TARGET_CLASSIFICATION.json).
- [Source routing inventory and minimum native closure rules](DETERMINISTIC_PLANNER_V0_1_FROZEN_MINIMUM_SUFFICIENT_STATE_1_OPERATIONAL_SUBGRAPH.json).
- [FrozenControlProof JSON schema and verifier obligations](DETERMINISTIC_PLANNER_V0_1_FROZEN_MINIMUM_SUFFICIENT_STATE_1_PROOF_SCHEMA.json).
- [Five-interface blocking cut](DETERMINISTIC_PLANNER_V0_1_FROZEN_MINIMUM_SUFFICIENT_STATE_1_BLOCKING_CUT.json).

## C1–C5: backward executable trace

Admission is a prerequisite to all conclusions. A validation exception, missing action, empty invented universe or PLAN_DEFECT is not a valid proof of frozen waiting.

| Conclusion | Native computation | Required premises |
|---|---|---|
| C1 MIXED_WAIT | `core.recompute → project → evaluate_satisfaction → _actionability → _global_control` | Valid typed projection; no machine selection or active human batch; no projection/control defect; at least one unsatisfied goal; no applicable terminal-failure override; nonempty exposed frontier with at least one boundary whose kind is not EXTERNAL_EVIDENCE. Reproducing E1 also requires the exact budget evidence frontier plus seven factual frontiers. |
| C2 internal runnable set empty | `_actionability`, then `_human` partition in `recompute` | Complete ActionId universe and statuses; all current statuses held/completed in frozen E1. On other states, blockers include prerequisites, currentness, evidence/authority, effects and decision/gate relationships. Native validation still runs before the hold shortcut. |
| C3 active decision-ready action set empty | `_actionability`, `_human`, `_human_batches` and human routing | Complete human-action subset of the universe; no active actionable human action. If a human action is not held/completed, its stage and `gates.decision_readiness` nine-check proof are needed. Historical dossier readiness alone is not a currently available human decision. |
| C4 resume false | `core.resume_eligibility → codec._replay → recompute`, then route proofs | Valid baseline/policy/replay; enumerate external and relevant decision reentry routes. Each requires current proof, proper stage, accepted native reentry event bound to policy/context, and a named actionable action. Empty native reentry events and empty actionable set independently defeat the conjunction for every frozen route. |
| C5 exactly eight recorded external boundaries | Native `external_gates`, `boundaries`, derived `frontier`, plus independently verified manifest/handoff route bijection | Exact request/proposition/receipt/reentry/absence identities, no duplicates or omitted/extra active route. There is no native function that authenticates “the eight E1 gates” merely by returning len(external_gates). The seven factual boundaries are not automatically seven EXTERNAL_EVIDENCE boundary kinds. |

`_global_control` precedence is RUNNABLE, HUMAN_HANDOFF, PLAN_DEFECT, TERMINAL_SUCCESS, TERMINAL_FAILURE, then EXTERNAL_WAIT/MIXED_WAIT from frontier kinds. MIXED_WAIT alone is weaker than E1 equivalence: even one factual frontier could produce that enum. C5 and the branch/source coverage obligations prevent that shortcut.

C3 means the currently actionable human decision set, consistent with the frozen report. Calling `decision_readiness` on every historical recorded dossier and counting DECISION_READY would answer a different question. Recorded decisions can have complete dossiers while no new human action is eligible.

### Newly exposed reached-wait dependency

`core._global_control.walk` explicitly adds `UNQUALIFIED_EXTERNAL_CONTRACT:<gate>` for a reached EXTERNAL_EVIDENCE boundary when **any** associated EvidenceRequirement has `rule_known=False`. That defect has precedence over MIXED_WAIT. CC01's suggestion to encode unknown positive governing rules as `rule_known=False` is therefore not sufficient to derive C1 through this path, although it correctly keeps obligation proof UNKNOWN and rejects reentry.

This is a live dependency issue, not a reason to restore a synthetic matrix. It requires an explicit analysis of whether `rule_known` denotes a known receipt/wait evaluation contract or an available governing positive applicability rule. The frozen request can be complete while positive rules/evidence are absent. This task neither sets the Boolean true, changes the core, nor silently revises CC01. The unresolved semantic interface is CUT04. No new absent external evidence is demanded. CC01's empty-positive-matrix separation remains valid; its full native-control sufficiency was not qualified.

## Transitive state closure

Follow computation operands and also native admission/reference dependencies to a fixed point. Do not include a field solely because hashing serializes it: canonical identity authenticates the chosen representation; it does not make every historical field a semantic input.

- **S01 — Complete action universe and admitted action/status structure** (C1, C2, C3, C4). 63 exact plan ActionIds and current 13 COMPLETED/50 BLOCKED partition; Action objects still required by validate_model/project; future result schemas are not read by held-action actionability. Source availability: **AVAILABLE**. Code: `core.project; core._actionability; model.validate_model`.
- **S02 — Current holds/completion support and transitive stale-support closure** (C1, C2, C3, C4). Current statuses plus necessary source/evidence/qualification support; do not replay all historical attempts to prove holds. Source availability: **AVAILABLE**. Code: `gates.current_completion; gates.unavailable_support`.
- **S03 — Goal/root/slot state and typed prerequisite routing** (C1, C4). Unsatisfied goal targets, entry/recovery/failure paths, required action/condition edges and satisfied cut points; no invented empty goal set. Source availability: **AVAILABLE_AS_UNRESOLVED_STATE**. Code: `core.evaluate_satisfaction; core._global_control.walk`.
- **S04 — Reached proof/predicate/entity/knowledge and evaluation-context closure** (C1, C4). Only support reachable from satisfaction, current completion, action requirements inspected by control, decision reentry and native reference validation; native real-source joins unresolved. Source availability: **AMBIGUOUS**. Code: `gates._evaluate_predicate; gates.usable; gates.unavailable_support; model.validate_predicate_contracts`.
- **S05 — Eight exact request/frontier/receipt/reentry correspondences** (C1, C4, C5). Pinned request/handoff absence inventory; one budget evidence frontier and seven factual frontiers; typed canonical mapping still required. Source availability: **AVAILABLE_AS_EXPECTED_ABSENCE**. Code: `core._global_control; model.validate_p05; pinned manifest request_routes`.
- **S06 — Budget unresolved requirements, qualified wait contract and empty receipts** (C1, C4, C5). Evidence obligations and no receipts present in source; meaning of rule_known across wait classification versus unknown real applicability requires reconciliation. Source availability: **AMBIGUOUS**. Code: `core._global_control EXTERNAL_EVIDENCE rule_known check; gates._obligation_proof`.
- **S07 — Active human-action universe, holds/stages and necessary decision links** (C3, C1, C4). All human actions held/completed; active ready set is not set of historically complete dossiers; retain stages/routes used by C4 and validation. Source availability: **AVAILABLE**. Code: `core._human; core._actionability; gates.decision_readiness; core.resume_eligibility`.
- **S08 — Admitted canonical baseline/replay envelope and empty new event inventory** (C4). Initial/current identical admitted baseline, zero new native events; no historical selection converted to execution; policy/version/scope valid. Source availability: **AVAILABLE**. Code: `codec._replay; core.resume_eligibility`.
- **S09 — Source pins and independently verifiable field/source bindings** (C1, C2, C3, C4, C5). Authenticate control premises and universe completeness; exact required source closure contract still incomplete; no need full historical payload database. Source availability: **AVAILABLE**. Code: `codec._replay provenance pins; codec.load_pinned; source-bound certificate verification`.
- **S10 — Native structural/reference and projection integrity** (C1, C2, C3, C4, C5). Least closure including all retained typed references, source provenance, cycles/order and output-reference compatibility; missing mappings cannot be replaced by placeholders. Source availability: **AMBIGUOUS**. Code: `model.validate_model/validate_p03/validate_p04/validate_p05; core.project`.

This is the minimum *set of dependency responsibilities* justified by the trace, not ten complete native objects. Each collection is restricted to necessary instances and their typed/source closure. A field may be structurally required for retained objects without its complete historical inventory being required. No sufficient instantiated canonical proof is claimed while the indicated AMBIGUOUS mappings remain.

### Action necessity

The frozen plan contains63 actions,13 completed and50 blocked. `_actionability` unconditionally skips COMPLETED/BLOCKED/WAITING actions before evaluating blockers. Given independently admitted current holds, this directly proves C2 and the active C3 without reexecuting historical actions or filling positive external proofs.

However, `validate_model` requires the Action and ActionStatus id sets to be equal; `project` reads action prerequisites and validates the entire retained state. `_global_control` traverses those prerequisites, current completion and action requirements to reach the actual frontier. A reduced list of eight blocked receiving actions cannot establish that the other55 contain no runnable work. The current API has no certificate-as-Snapshot entry point that accounts for omitted actions.

Thus **ALL_63_ACTIONS_REQUIRED=YES for the complete native ActionId/status universe and corresponding valid Action records under the unchanged API**. It does not mean all rich prospective definitions are semantically consulted on held paths. A separate reviewed minimal control projection could narrow unused Action fields, but cannot fill missing fields from defaults, erase already-governed output references or bypass O01. Whether such a projection satisfies the existing O01 contract is CUT01; it is not authorized by this dependency analysis. The plan's MC03 requirement remains until explicitly reconciled.

### Results and history

**ALL_3_RESULTS_REQUIRED=NO as complete canonical historical ActionResult projections for C1–C5.** The control functions do not read the three original report documents or call `apply_result`/`validate_result`. They read current statuses, qualification, assertions, knowledge and predicates. Extracted facts from S-BINDING/S-CONTEXT/PREP-VALIDATOR can still belong to current support (especially authority/proof/currentness), so their source pins and bounded claims must remain when referenced. “No complete result projection” is not “no source evidence.”

The selection-only record cannot become a result or knowledge. All24 chronological records are unnecessary to evaluate current holds. The accepted migrated baseline still needs independent source-backed reconciliation; neither a forged current status label nor fabricated parent/after snapshots substitute for it. Passive full historical reconstruction is outside the current-control cone, while the source references proving current state are inside S02/S09.

### Graph necessity

**FULL_GRAPH_REQUIRED=NO.** Start with the complete action universe, retained goal/condition/slot targets, typed prerequisite routes, exposed boundaries and necessary proofs. Close predicate operands, knowledge/producer bindings, authority/mapping/validator/value relationships, source assertions and transitive invalidation dependencies. Include context only for retained support evaluated by `usable`; its scope/lineage/generation/tick affect proof. Exclude unrelated archived graph objects and prose.

The companion enumerates all63 source ActionIds,116 compiled source action edges,31 top-level source goal routes and the eight frontiers. These are an exact **source routing inventory**, not a claim that every source edge has already been proved necessary or that a canonical graph with those counts exists. Conditional goal routes, positive cut points, native predicate identities and reference closure still need their independent mappings. Existing `project` requires declared ordering relations to agree with Action prerequisite metadata; stripping inconvenient edges can create a projection defect. Unreferenced baseline slots or proofs may be outside a smaller cone, but no blanket deletion is justified until all native goal/predicate/ordering references are closed.

## Gate and resume sufficiency

For every route retain a verified missing proposition and expected source role, exact request/frontier identity, receipt specification, reentry correspondence, source-pinned absence and its correct branch kind. Missing concrete producer identity is not a fabricated producer. There are no admitted received observations at the checkpoint. The eight routes are:

| Request | Frontier | Receipt | Reentry | Frozen state |
|---|---|---|---|---|
| E1-EXTERNAL-REQUEST-BUDGET-1 | EXT-BUDGET-APPLICABILITY-EVIDENCE | RECEIVE-BUDGET-APPLICABILITY-EVIDENCE | FACT-BUDGET-APPLICABILITY, REEVAL-BUDGET | WAITING_FOR_EXTERNAL_EVIDENCE |
| E1-EXTERNAL-REQUEST-ANCESTRY-1 | EXT-REENTRY-S-ANCESTRY | RECEIVE-ANCESTRY-EVIDENCE | S-ANCESTRY | FACT_BLOCKED |
| E1-EXTERNAL-REQUEST-APPROVAL-1 | EXT-REENTRY-S-APPROVAL | RECEIVE-APPROVAL-EVIDENCE | S-APPROVAL | FACT_BLOCKED |
| E1-EXTERNAL-REQUEST-AUDIT-1 | EXT-REENTRY-PREP-AUDIT | RECEIVE-AUDIT-SOURCE-EVIDENCE | PREP-AUDIT | FACT_BLOCKED |
| E1-EXTERNAL-REQUEST-RUNTIME-HEAD-1 | EXT-REENTRY-PREP-RUNTIME_HEAD | RECEIVE-RUNTIME-HEAD-EVIDENCE | PREP-RUNTIME_HEAD | FACT_BLOCKED |
| E1-EXTERNAL-REQUEST-SUPERVISOR-1 | EXT-REENTRY-PREP-SUPERVISOR | RECEIVE-SUPERVISOR-EVIDENCE | PREP-SUPERVISOR | FACT_BLOCKED |
| E1-EXTERNAL-REQUEST-EXEC-1 | EXT-REENTRY-DEC-EXEC | RECEIVE-EXEC-POLICY-EVIDENCE | DEC-EXEC readiness reevaluation | FACT_BLOCKED |
| E1-EXTERNAL-REQUEST-IMPLEMENTATION-1 | IMPLEMENTATION-OWNING-SOURCE + IMPLEMENTATION-SELECTOR | RECEIVE-IMPLEMENTATION-SOURCE-EVIDENCE | INPUT-IMPLEMENTATION | FACT_BLOCKED |

Each full missing-proposition/owner/currentness record is retained verbatim in the companion. Budget is WAITING_FOR_EXTERNAL_EVIDENCE; the other request routes await factual input with fact-blocked frontiers. Dependent actions remain dependency-blocked. A known request's absence is authoritative source state, not malformed missing evidence. No actual receipt action is executed or made actionable.

C5 requires a bijection of these identities, not merely eight arbitrary records. The composite implementation frontier text and DEC-EXEC readiness-reevaluation description need explicit typed correspondence; neither is silently converted into a literal native id. Native ExternalGate validation requires valid requirement/reentry/action references. ControlBoundary distinguishes EXTERNAL_EVIDENCE from EXTERNAL_FACT. C1 would become EXTERNAL_WAIT rather than MIXED_WAIT if every reached boundary were normalized to the former.

For C4, each native external route is not at accepted dependent reentry, has no complete current proof and has no accepted native reentry event. Any decision-downstream route also lacks a new accepted DecisionReentry event. There are no named actionable candidates. Consequently the conjunction fails without proving positive authority/receipt/evidence. `resume_eligibility` verifies source bytes for granting permission only when eligible candidates survive; an analysis certificate must still authenticate the negative premises independently. Intentionally omitting source_root is not a faithful no-resume proof. Likewise a replay exception is not allowed=false.

## All35 targets mapped to the cone

“Critical/supporting” applies to the reached subset or mandatory structural envelope, not the entire category inventory. The machine companion gives code-path/node evidence for every retained category.

| Target | Cone classification | Required dependency nodes |
|---|---|---|
| Snapshot.actions | CONTROL_CRITICAL | S01, S10 |
| Snapshot.statuses | CONTROL_CRITICAL | S01, S02 |
| Snapshot.roots | CONTROL_CRITICAL | S03, S04 |
| Snapshot.slots | CONTROL_CRITICAL | S03, S04 |
| Snapshot.knowledge | CONTROL_SUPPORTING | S04 |
| Snapshot.assertions | CONTROL_SUPPORTING | S02, S04, S10 |
| Snapshot.entities | CONTROL_SUPPORTING | S04, S10 |
| Snapshot.predicates | CONTROL_CRITICAL | S04, S10 |
| Snapshot.context | CONTROL_SUPPORTING | S04 |
| Snapshot.decisions | CONTROL_CRITICAL | S07, S08 |
| Snapshot.evidence_requirements | CONTROL_CRITICAL | S06 |
| Snapshot.external_gates | CONTROL_CRITICAL | S05, S06 |
| Snapshot.receipt_admissions | CONTROL_CRITICAL | S06 |
| Snapshot.receipt_observations | CONTROL_CRITICAL | S06 |
| Snapshot.boundaries | CONTROL_CRITICAL | S05 |
| Snapshot.goals | CONTROL_CRITICAL | S03 |
| Snapshot.budget_matrices | NOT_REQUIRED | None; see separation rules |
| PersistenceBundle.initial | CONTROL_SUPPORTING | S08 |
| PersistenceBundle.events | CONTROL_SUPPORTING | S08 |
| PersistenceBundle.current | CONTROL_CRITICAL | S08 |
| PersistenceBundle.sources | CONTROL_SUPPORTING | S09 |
| PersistenceBundle.policy | CONTROL_SUPPORTING | S08 |
| PersistenceBundle.policy_version | CONTROL_SUPPORTING | S08 |
| PersistenceBundle.scope | CONTROL_SUPPORTING | S08 |
| historical_attempts | PROVENANCE_ONLY | None; see separation rules |
| expected_external_absence_records | CONTROL_SUPPORTING | S05, S09 |
| MigrationManifest | PROVENANCE_ONLY | None; see separation rules |
| DerivationIndex | PROVENANCE_ONLY | None; see separation rules |
| Snapshot.information | OUTSIDE_FROZEN_CONTROL_CONE | None; see separation rules |
| Action.cost/cost_unit | OUTSIDE_FROZEN_CONTROL_CONE | None; see separation rules |
| descriptive titles/report narrative/source annotation | PROVENANCE_ONLY | None; see separation rules |
| global-control/actionable/resume summary labels | PROVENANCE_ONLY | None; see separation rules |
| positive external evidence absent at suspension | NOT_REQUIRED | None; see separation rules |
| unreferenced archived experiment payloads | NOT_REQUIRED | None; see separation rules |
| complete raw source bodies embedded inside snapshot | NOT_REQUIRED | None; see separation rules |

Counts:13 CONTROL_CRITICAL,11 CONTROL_SUPPORTING,2 OUTSIDE_FROZEN_CONTROL_CONE,5 PROVENANCE_ONLY,4 NOT_REQUIRED. These are **dependency roles**, not replacements for the prior completeness counts. `Snapshot.budget_matrices` is NOT_REQUIRED as positive content and must be empty for the frozen bundle. Native required empty collections still need valid serialization. Selection information/cost ranking is not reached when no action is actionable; it remains on the future-execution roadmap. A full MigrationManifest or DerivationIndex is not read by native control; the certificate needs only independently authenticated source/field references sufficient for this projection.

### The19 incomplete categories

- `Snapshot.actions`: **A_REQUIRED_TO_DERIVE_C1_C5** — required subset only; no demand for the entire historical collection.
- `Snapshot.statuses`: **A_REQUIRED_TO_DERIVE_C1_C5** — required subset only; no demand for the entire historical collection.
- `Snapshot.roots`: **A_REQUIRED_TO_DERIVE_C1_C5** — required subset only; no demand for the entire historical collection.
- `Snapshot.slots`: **A_REQUIRED_TO_DERIVE_C1_C5** — required subset only; no demand for the entire historical collection.
- `Snapshot.knowledge`: **A_REQUIRED_TO_DERIVE_C1_C5** — required subset only; no demand for the entire historical collection.
- `Snapshot.assertions`: **A_REQUIRED_TO_DERIVE_C1_C5** — required subset only; no demand for the entire historical collection.
- `Snapshot.entities`: **A_REQUIRED_TO_DERIVE_C1_C5** — required subset only; no demand for the entire historical collection.
- `Snapshot.predicates`: **A_REQUIRED_TO_DERIVE_C1_C5** — required subset only; no demand for the entire historical collection.
- `Snapshot.context`: **A_REQUIRED_TO_DERIVE_C1_C5** — required subset only; no demand for the entire historical collection.
- `Snapshot.decisions`: **A_REQUIRED_TO_DERIVE_C1_C5** — required subset only; no demand for the entire historical collection.
- `Snapshot.evidence_requirements`: **A_REQUIRED_TO_DERIVE_C1_C5** — required subset only; no demand for the entire historical collection.
- `Snapshot.external_gates`: **A_REQUIRED_TO_DERIVE_C1_C5** — required subset only; no demand for the entire historical collection.
- `Snapshot.boundaries`: **A_REQUIRED_TO_DERIVE_C1_C5** — required subset only; no demand for the entire historical collection.
- `Snapshot.goals`: **A_REQUIRED_TO_DERIVE_C1_C5** — required subset only; no demand for the entire historical collection.
- `PersistenceBundle.initial`: **A_REQUIRED_TO_DERIVE_C1_C5** — required subset only; no demand for the entire historical collection.
- `PersistenceBundle.current`: **A_REQUIRED_TO_DERIVE_C1_C5** — required subset only; no demand for the entire historical collection.
- `PersistenceBundle.sources`: **A_REQUIRED_TO_DERIVE_C1_C5** — required subset only; no demand for the entire historical collection.
- `historical_attempts`: **E_PROVENANCE_ONLY** — retain provenance references; full reconstruction is not a frozen-control blocker.
- `DerivationIndex`: **E_PROVENANCE_ONLY** — retain provenance references; full reconstruction is not a frozen-control blocker.

There are17 category-level A entries and2 E entries. At field/instance level the reduction is larger: prospective result inventories and positive receipt proofs belong to later execution/reentry; full dossiers for held historical decisions need not be reconstructed solely to establish an empty active-ready set; unrelated graph/history material stays outside. Categories are coarse containers, so moving a category outside merely because some members are unnecessary would be unsound. Historical source facts needed for current proofs are retained in S02/S04/S09 rather than requiring full `historical_attempts` reconstruction.

## FrozenControlProof

The companion JSON schema defines a reference certificate, **not a second planner state or trusted permission record**. It pins code/contract/bundle identities; complete action/status universe sources; canonical node/goal/route references; per-action canonical status witnesses; the exact eight request/frontier/receipt/absence correspondences; decision-universe and native-event references; and native query identifiers. It contains no trusted fields asserting MIXED_WAIT, empty runnable sets or resume=false.

A verifier must authenticate source and canonical references, check complete universes and joins, perform native validation/project/replay, run `recompute` and `resume_eligibility`, and independently check the eight-route bijection. Then compare derived results with C1–C5. Schema validity alone is not a proof. Reject omitted action, duplicate/substituted gate, forged hold, unknown positive proof, malformed required reference, changed source/policy and any native defect. Source invalidation must change proof validity; a certificate is bound to the exact source/state/code identities. No populated valid certificate is issued here because CUT01–05 remain unresolved.

## True blocking cut and source sufficiency

- **CUT01 — Admitted action-universe/control projection** (S01, S02, S10): O01/source Action definition still needs reviewed native representation; all63 identities/statuses and required typed references must exist. Rich prospective outputs unused on held path must not be fabricated or silently erased. Resolve minimal admissible projection contract separately.
- **CUT02 — Goal/prerequisite/frontier correspondence** (S03, S05, S10): Exact typed entry/condition/slot/deferred-goal routes and eight request-to-boundary/receipt/reentry/held-action mappings; do not interpret composite frontier text as an ActionId/GateId.
- **CUT03 — Reached proof and currentness support** (S02, S04, S07, S09, S10): Typed native predicate/entity/knowledge/context support and source pins for reached proofs and current completion; positive existing O08/O09 support only where retained/required, no need every report-result projection.
- **CUT04 — Frozen wait qualification semantics** (S06): _global_control marks reached EXTERNAL_EVIDENCE boundary PLAN_DEFECT if any requirement.rule_known is false. CC01 permits false for unknown real governing rules. Need explicit distinction between known receipt/wait evaluation contract and absent positive applicability rule; do not set true or change code here.
- **CUT05 — Native baseline integrity and proof completeness** (S08, S09, S10): Admit initial/current identical canonical baseline and exact policy/pins; independent certificate must prove universe/route coverage, canonical reference closure and no accepted reentry events. Full passive imported history/manifest/index not required.

Frozen sources contain the action/status universe, compiled routing, unresolved conditions, missing propositions, request/receipt/reentry records and checkpoint absence. The principal shortfall is native interpretation/admission, not eight absent positive external bundles. Reached proof/context semantics and the wait-rule Boolean interface remain AMBIGUOUS. No external positive evidence belongs in this cut.

This is a supported dependency cut, not a graph-theoretic minimum cut proof: CUT05 depends on the earlier interfaces, and exact retained proof nodes depend on unresolved source mappings. Claiming a fully enumerated minimal canonical snapshot now would invent the contracts this task explicitly does not close. The companion marks that limitation machine-readably.

## M01 progression recommendation

Recommend **MINIMUM_SUFFICIENT_STATE**, meaning a separately scoped frozen-state contract milestone that includes unchanged native admission, complete action-universe/route coverage, authoritative negative premises and an independent control certificate. It must not mean just four output labels or an eight-node stand-in graph. Full historical result reconstruction, unused prospective output profiles, complete dossier narrative, selector metrics and positive evidence acquisition should not gate that milestone solely because they occur in broader35-category inventories.

This is a proposed scope reconciliation, not a change to the authoritative plan. Current M01 explicitly includes MC01–06,63 complete O01 definitions, three result profiles and reentry requirements. Those cannot be silently waived here. A reviewed split must assign unused positive/reentry/future-execution work to later bounded milestones while retaining it before relevant qualification or Phase B use. Native structural/reference validation cannot be postponed if it prevents loading the frozen projection. CUT04 must be resolved without inventing governing rules or suppressing PLAN_DEFECT. Therefore **M02_READY=NO** under both the existing gate and the proposed minimum-state gate.

Existing synthetic budget qualification remains required for positive reentry and is not invalidated. Full migrated receipt→validated evidence→accepted proof→named reentry qualification remains separate. This task neither executes it nor declares it complete.

```text
REQUIRED_CONCLUSIONS = [C1,C2,C3,C4,C5]
MINIMUM_SUFFICIENT_STATE = [S01,S02,S03,S04,S05,S06,S07,S08,S09,S10]
TARGET_CATEGORIES_TOTAL = 35
CONTROL_CRITICAL = 13 categories (enumerated above and in companion)
CONTROL_SUPPORTING = 11 categories
OUTSIDE_FROZEN_CONTROL_CONE = [Snapshot.information, Action.cost/cost_unit]
PROVENANCE_ONLY = [historical_attempts, MigrationManifest, DerivationIndex,
 descriptive titles/report narrative/source annotation, global-control/actionable/resume summary labels]
NOT_REQUIRED = [positive Snapshot.budget_matrices, positive external evidence absent at suspension,
 unreferenced archived experiment payloads, complete raw source bodies embedded inside snapshot]
INCOMPLETE_TARGETS_TOTAL = 19
INCOMPLETE_REQUIRED_FOR_C1_C5 = 17 reached-category subsets, enumerated in companion
INCOMPLETE_OUTSIDE_C1_C5 = [historical_attempts, DerivationIndex] as full reconstruction products
ALL_63_ACTIONS_REQUIRED = YES (native identity/status universe and valid Action objects; not all historical/prospective detail)
ALL_3_RESULTS_REQUIRED = NO (complete result projections; required current source claims remain)
FULL_GRAPH_REQUIRED = NO
MINIMUM_OPERATIONAL_SUBGRAPH = bounded routing + reached proof/reference/invalidation closure; exact source inventory in companion
MINIMUM_MIGRATION_BLOCKING_CUT = [CUT01,CUT02,CUT03,CUT04,CUT05]
FROZEN_SOURCE_SUFFICIENCY = AVAILABLE negative-state/routing evidence; AMBIGUOUS remaining native interpretation; no positive external evidence required
M01_COMPLETION_RECOMMENDATION = MINIMUM_SUFFICIENT_STATE (explicit scoped plan reconciliation required)
M02_READY = NO
V0_1_CURRENT_STATUS = CORRECTION_REQUIRED
IMPLEMENTATION_MODIFIED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
```

Validation is static code-path/source dependency analysis and mechanical inventory/schema checks, not native frozen readiness qualification. All35 categories and19 incomplete categories were covered exactly once;63 ActionIds,116 source edges and31 source goal routes were inventoried. All10,911 frozen file paths/hashes and all pre-existing captured implementation/plan/backlog/E1 files remain unchanged. Local links, JSON syntax, dependency references, target counts and `git diff --check` pass. No migration contract was edited, M02 executed or E1 action resumed.
