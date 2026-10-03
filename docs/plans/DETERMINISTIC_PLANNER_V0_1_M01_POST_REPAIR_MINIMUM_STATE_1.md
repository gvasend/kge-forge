# M01 minimum-state recomputation after control repair 1

**M01_MINIMUM_STATE_CONTRACT_COMPLETE = NO; M02_READY = NO.** The native unknown-rule defect is closed. Its source-to-native binding is not: the repaired evaluator requires an independently admitted, exactly source-bound `ExternalResolutionContract`. Frozen requests do not acquire that representation merely because the runtime now supports it. All five previous interfaces retain migration work; CUT04 is narrowed from a control-semantic defect to an explicit migration binding contract.

The target remains the minimum state sufficient for C1–C5, not all 35 historical target categories. No compiler, migration contract, prior result or frozen E1 file is changed. No M02, migration/readiness test or E1 action is executed.

## Evidence and reproducibility

This analysis reads the [minimum-state analysis](DETERMINISTIC_PLANNER_V0_1_FROZEN_MINIMUM_SUFFICIENT_STATE_1.md) and all five companions; [reconciliation](DETERMINISTIC_PLANNER_V0_1_EXTERNAL_UNKNOWN_RULE_RECONCILIATION_1.md), [accepted repair](DETERMINISTIC_PLANNER_V0_1_EXTERNAL_UNKNOWN_RULE_REPAIR_1_RESULT.md), [migration plan](DETERMINISTIC_PLANNER_V0_1_E1_MIGRATION_IMPLEMENTATION_PLAN_1.md), [acceptance matrix](DETERMINISTIC_PLANNER_V0_1_E1_MIGRATION_ACCEPTANCE_MATRIX_1.md), M01/closure/retry and CC01 records. It independently rechecks the repaired native functions and frozen plan/manifest inventories.

Additive companions:

- [Dependency cone, native Action field schema, complete action/status inventory, eight routes, source routing and 35-target crosswalk](DETERMINISTIC_PLANNER_V0_1_M01_POST_REPAIR_MINIMUM_STATE_1_DEPENDENCIES.json).
- [Recomputed five-interface cut](DETERMINISTIC_PLANNER_V0_1_M01_POST_REPAIR_MINIMUM_STATE_1_BLOCKING_CUT.json).
- [Finite contract/readiness conjunction and deferred work](DETERMINISTIC_PLANNER_V0_1_M01_POST_REPAIR_MINIMUM_STATE_1_READINESS.json).

The dependency companion pins inspected contract and native module SHA-256 identities. Re-running `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest adapter.tests.test_planner_external_unknown` passed **9 tests in 7.803 seconds**. These independently exercise governed/unexplained unknowns, mixed/runnable/human branches, receipt/reentry, invalidation, source pins and cold ordering/hash-seed restoration. They are synthetic control probes, not frozen E1 migration qualification. The prior full-suite result is preserved, not claimed as rerun here.

## Recomputed C1–C5 dependency cone

The trace starts at [core.py](../../adapter/planner/core.py), [gates.py](../../adapter/planner/gates.py), [model.py](../../adapter/planner/model.py) and [codec.py](../../adapter/planner/codec.py), rather than target-category counts.

| Conclusion | Executable path and necessary canonical input |
|---|---|
| C1 MIXED_WAIT | `recompute → project/validate_model → evaluate_satisfaction → _actionability → _global_control`. Retain source-backed holds, unsatisfied goal targets, exact entry/prerequisite routes, current completion cut points, supported predicates and correct boundary kinds. No selection/human batch, defects or terminal-failure override; a nonempty frontier includes factual boundaries. Reached unknown evidence requirements now additionally use `governed_external_unknown`. |
| C2 no runnable internal actions | `_actionability` scans the entire admitted action universe. Frozen COMPLETED/BLOCKED statuses suppress candidates before `blockers`; `_human` partitions candidates. Missing actions cannot prove universal emptiness. All retained state still passes validation and satisfaction first. |
| C3 no active decision-ready actions | Same admitted universe/status scan and `_human/_human_batches`. No actionable human is an active decision. Retained Decision objects still obey `validate_p04`, including stage-dependent dossier and recorded-choice requirements. |
| C4 no resume | `resume_eligibility → codec._replay → recompute`, then evidence/stage/accepted-event/policy-context binding and named-action checks. Valid baseline, empty new reentry events and no named actionable candidate defeat permission; missing positive proof independently fails it. A replay exception or deliberately omitted source root is not a no-resume certificate. |
| C5 exact eight boundaries | Canonical boundary/gate and frontier state plus authenticated manifest/handoff bijection. No native `len(gates)==8` check authenticates E1 identity or branch kinds. Preserve receipt/reentry/expected-absence correspondence, not just a count. |

Control precedence is unchanged: selected internal work, human handoff, defects, terminal success, terminal failure, then frontier wait classification. An arbitrary waiting label cannot suppress a defect. MIXED_WAIT alone does not prove equivalence to E1: exact frontier and action-universe coverage remain independently necessary.

The transitive responsibilities remain S01–S10: complete Action/status universe; current completion/hold support; goals/root/slot routing; reached predicates/knowledge/entities/context; eight external correspondences; unresolved budget requirements and governed wait; human routing; baseline/events/policy; source pins; native structural/reference closure. **S06 now has a defined native representation** and S09 includes the resolution-contract content source and its legacy derivation. It no longer requires a known positive budget rule. The fixed point still follows predicates, evidence assertions, ordering edges, decision references and source-invalidation dependencies. Unreferenced historical payload is excluded.

The 35-category dependency roles remain 13 critical, 11 supporting, 2 outside, 5 provenance-only and 4 not-required-as-positive-content. This is not an all-35 completion gate. The former 19 incomplete categories still contain 17 potentially required reached subsets; full `historical_attempts` and `DerivationIndex` reconstruction remain provenance-only. Runtime repair does not complete their source mappings or promote migration coverage.

## Repair impact and recomputed cut

| Interface | Before | After / remaining requirement | Source sufficiency | Contract sufficiency |
|---|---|---|---|---|
| CUT01 Action/control projection | Open | Open: exact 63 source-backed native Actions/statuses and typed references; reviewed minimal projection compatible with O01 | Common core and status partition available; semantic joins incomplete | Incomplete |
| CUT02 goal/frontier correspondence | Open | Open: root/slot entry paths, conditional dependencies, eight request-to-boundary/receipt/reentry/held-action mappings | Routing recorded; composite implementation frontier and DEC-EXEC readiness require typed interpretation | Incomplete |
| CUT03 proof/currentness support | Open | Open: reached predicates, entities, knowledge types, evaluation context, source-bound completion; retained O08/O09 support | Present evidence available; native support closure remains ambiguous | Incomplete |
| CUT04 wait qualification | Native defect plus mapping gap | Native defect **closed**; frozen request-to-resolution-contract binding still open | Missing proposition, expected source role and routes available; target/context/provenance normalization incomplete | Native contract complete; migration contract incomplete |
| CUT05 baseline completeness | Open | Open: admitted initial=current baseline, policy/version/scope, empty new events, exact source pins and independent coverage certificate | Checkpoint/policy sources available | Incomplete; depends on CUT01–04 |

CLOSED_BY_PLANNER_REPAIR contains **CUT04/native unknown-rule interpretation**, not an entire migration interface. No prior migration target is established as having had *only* that runtime blocker: evidence_requirements, external_gates, predicates, context, provenance and action/goal bindings all still need canonical instantiation. Full result narratives, unused selector metrics and positive absent evidence stay outside the frozen control cone.

Every remaining cut member is primarily **MISSING CONTRACT**, not a demand for the eight missing positive evidence bundles. No additional canonical type defect or genuinely absent frozen-state source is established here. Exact minimal instance counts cannot be proved before the native mappings exist. This is a dependency-responsibility cut, not a minimum-cardinality graph cut; CUT04's remaining binding can share work with CUT02/03, and CUT05 aggregates their coverage.

## Frozen Action schema and normalization

**Complete native action universe required: YES.** The source plan has 63 actions, with 13 COMPLETED and 50 BLOCKED in the checkpoint/manifest. Native `validate_model` requires equal Action and ActionStatus identity sets. `project` reads prerequisite metadata; `_global_control` walks it despite the actionability hold shortcut. Eight blocked receiving actions alone cannot establish C2.

FROZEN_ACTION_SCHEMA is the existing `Action` type plus its matching status and retained support. It is a field-dependency specification, not a new permissive Action type:

| Fields | Frozen role |
|---|---|
| `id`, status | Complete source-backed universe and exact current partition |
| `operation`, `stage`, `effect` | Typed admission and human/decision-input distinctions; do not substitute a generic non-effecting operation |
| `prerequisites` | Exact typed action/condition edges for ordering and frontier traversal |
| `source`, `qualification`, `evidence` | Provenance/currentness and reference closure; qualifications cannot be invented from a hold |
| `requirements` | Reached supported rules; exact evidence-obligation predicate required by the governed-unknown check |
| `authority` | Retained authority reference/type and transitive unavailable-support semantics; stale authority can change current completion |
| `accepted_inventory` | Native required collection; retained members' validity and evidence affect current completion. Future outputs are not executed, but an empty collection is not automatically a justified projection |
| `prepared_dossier` | Retained objects validate fully; no complete historical narrative required merely to prove no active human |
| `cost`, `cost_unit`, `pass_model_complete` | No candidate means no selector invocation; richer ranking inputs outside this frozen query, with structural constraints respected if retained |
| `accepted_result` | Native typed field, not evidence of execution; applying a future result is outside C1–C5 |

The companion enumerates **every current Action dataclass field** and checks that none is omitted. Action does not store standalone scope/lineage strings: provenance and referenced predicates/entities/context carry those native relationships. Definition scope, operational scope and source identity remain distinct.

Mapping the shared ActionIR constructor and 29 literal bindings yields:

| Semantic domain | Minimum-state disposition |
|---|---|
| RESULT_BINDING | Prospective possible outputs/transitions: NOT_REQUIRED_UNTIL_EXECUTION. Retained `accepted_inventory` support and mandatory native/O01 fields: REQUIRED_FOR_FROZEN_ACTION_SCHEMA. No blanket empty-result exemption. |
| AUTHORITY_BINDING | Required for retained authority/support and admissible definition; grant applicability needed only for future eligibility is deferred. No inference from authority existence. |
| EVIDENCE_BINDING | Required: distinguish definition provenance, current support and obligation/gate routing, especially the new exact consumer binding. Positive receipts absent at suspension are deferred. |
| KNOWLEDGE_BINDING | Required for reached knowledge predicates/current support; unused prospective knowledge is execution-only. The three non-PASS source/type joins remain necessary where retained; BLOCKED producer is not invalid knowledge. |
| SCOPE_BINDING | Existing declared-definition normalizer reused; operational context/source correspondence still required, not implied by the closed definition field. |
| LINEAGE_BINDING | Existing recorded-lineage normalizer reused; exact current gate/context correspondence required. Recorded text does not prove applicability. |

Therefore common structure remains **63/63**, but **0/63 complete independently qualified source-to-native/O01 frozen constructions are established** by this analysis. The repair is not an action constructor. A reviewed control projection can defer unused prospective detail, but cannot erase governing requirements or bypass O01 by relying on Python defaults. That compatibility proof belongs to CUT01; neither 56 bespoke projections nor full future execution contracts are requested here.

## Results, graph, decisions and resume

No complete reconstruction of all three historical ActionResult routes is required for C1–C5. Current claims from S-BINDING/S-CONTEXT/PREP-VALIDATOR remain if reached proof depends on them. Preserve their pins and bounded claims without fabricating execution events. Selection-only evidence proves neither execution, completion, result existence nor produced knowledge. Empty *new native events* is compatible with a source-backed migrated baseline; it is not erasure of necessary current support.

MINIMUM_OPERATIONAL_GRAPH starts with all 63 Action/status identities, retained root/slot goals and current proof cut points, exact prerequisite/conditional routing, eight frontier correspondences, then closes predicate operands, entities, knowledge, source assertions, decision references and invalidation dependencies. The companion preserves the independently checked source inventory of 116 dependency edges and 31 top-level goal routes as **source inventory**, not a fabricated native graph. `project` requires declared REQUIRES ordering and Action metadata to agree. Full historical graph restoration is unnecessary; omitting inconvenient required edges is invalid.

C3 requires source-backed holds/completions for the entire human subset. Historical dossier readiness is not an active decision. For any Decision retained for proof, references or resume, native stage/dossier/record/choice validation still applies; one cannot drop a required dossier while retaining a recorded stage. Which bounded dossier facts survive follows CUT03 reference closure, not narrative completeness.

C4 remains the C03 conjunction: current proof, accepted reentry lineage, policy/context-bound event, verified source pins and named-action eligibility. Waiting gates, empty observations/admissions and no new accepted reentry events supply negative premises; all named actions remain held/completed. The repaired control binding proves none of the positive conjuncts. A valid replayable baseline and independently verified source coverage remain required before this can be a frozen E1 certificate.

## Eight external boundaries

| Request suffix | Frozen frontier / branch | Native capability after repair | Remaining migration issue |
|---|---|---|---|
| BUDGET | EXT-BUDGET-APPLICABILITY-EVIDENCE / waiting | Unknown obligations plus valid typed external-resolution contract can wait | Exact eight-obligation target/source/context and consumer projection; canonical resolution-contract bytes/pins |
| ANCESTRY | EXT-REENTRY-S-ANCESTRY / fact blocked | EXTERNAL_FACT frontier needs no positive fact | Exact requirement/receipt/reentry/source mapping |
| APPROVAL | EXT-REENTRY-S-APPROVAL / fact blocked | Same | Exact scope/lineage and route mapping |
| AUDIT | EXT-REENTRY-PREP-AUDIT / fact blocked | Same | Exact missing owning-source requirement and route |
| RUNTIME-HEAD | EXT-REENTRY-PREP-RUNTIME_HEAD / fact blocked | Same | Exact head/producer-role/currentness correspondence |
| SUPERVISOR | EXT-REENTRY-PREP-SUPERVISOR / fact blocked | Same | Exact release/context and route correspondence |
| EXEC | EXT-REENTRY-DEC-EXEC / fact blocked | Same; human readiness remains blocked | Readiness-reevaluation text to exact native route, without inventing an ActionId |
| IMPLEMENTATION | IMPLEMENTATION-OWNING-SOURCE + IMPLEMENTATION-SELECTOR / fact blocked | Same | Composite frontier to canonical boundary mapping |

Full request, receipt, reentry and missing-proposition identities are retained in the dependency companion and checked against the manifest's eight request_routes. **8/8 source boundaries have representable waiting/absence semantics; 0/8 complete frozen source-to-native chains are newly qualified here.** All eight retain mapping work. This count is a capability/source-inventory statement, not a native frozen acceptance result.

Do not relabel seven factual boundaries as EXTERNAL_EVIDENCE: that can change MIXED_WAIT to EXTERNAL_WAIT. Where an evidence boundary has an unknown requirement, the repair requires exact request/gate/requirement/target/producers or expected source class, receipt/reentry/held actions, matching scope/lineage/generation, gate/requirement source identities, provenance and actual consumer EVIDENCE_OBLIGATION. Canonical acquisition-contract content pins must also retain derivation back to legacy inputs. Self-hashing invented source bytes would not close this migration requirement. No positive external producer identity or evidence is manufactured.

## M01 milestone and M02 gate

Recommend the **MINIMUM_SUFFICIENT_FROZEN_STATE_CONTRACT** milestone. Its finite gate is G01–G09 in the readiness companion: reviewed scope allocation; required source classes/dispositions/selectors; admitted action/status universe; exact routing and absences; reached proof/decision/reference closure; qualified governed-unknown runtime semantics; real-source resolution binding; pinned baseline/certificate contracts; and no remaining minimum-state mismatch/conflict.

Only the native governed-unknown condition G06 is established by the repair. M01 is contract/oracle closure: these conditions require independently executable source mappings and expected-state fixtures, not premature execution of M02/M07. Later implementation must satisfy those contracts and cold native queries. The current missing contracts prevent either gate from passing.

The authoritative plan still assigns MC01–06 and broader result/history/reentry work to M01. This additive analysis specifies the necessary scope split rather than silently editing that plan. MC01/02 retain exact required source classification/disposition; MC03/06 retain native/O01 validity and composition for all 63 actions; MC04/05 narrow to current source-backed support for the frozen milestone, with complete historical result profiles and passive ledger reconstruction assigned before their later use. This allocation must be explicitly accepted in the scoped milestone; **G01 is not marked complete merely by this recommendation**. Even if that allocation were accepted now, CUT01–05 still block M02. No unrelated all-35 requirement is used as a substitute blocker.

Deferred before synthetic positive reentry: complete received-evidence authentication/applicability, positive budget matrix, receipt-to-validation transition, accepted reentry event and named-action proof in an isolated clone. Deferred before actual Phase B: actual current external sources and exact receipt contracts, all C03 checks, required qualification/readiness/review gates. Deferred before effecting execution: prospective output/result contracts outside current-support closure, exact effect authority and scope, execution-ready action definitions and required history/result profiles. None is waived or satisfied by empty frozen actionability.

```text
PLANNER_CONTROL_DEFECT = CLOSED
REQUIRED_CONCLUSIONS = [C1,C2,C3,C4,C5]
PREVIOUS_BLOCKING_INTERFACES = 5
CLOSED_BY_PLANNER_REPAIR = [CUT04.native_unknown_rule_interpretation]
REMAINING_BLOCKING_INTERFACES = [CUT01,CUT02,CUT03,CUT04.source_binding,CUT05]
COMPLETE_ACTION_UNIVERSE_REQUIRED = YES
FROZEN_ACTION_SCHEMA = existing typed Action fields with status, reached support and native/O01 validation; companion enumerates every field
RESULT_PROJECTIONS_REQUIRED = [] as complete historical ActionResult reconstructions; reached source claims remain required
MINIMUM_OPERATIONAL_GRAPH = action universe + goal/prerequisite/frontier + reached proof/reference/invalidation closure
EXTERNAL_GATES_REPRESENTABLE = 8/8 capability; 0/8 newly qualified frozen native chains
MINIMUM_MIGRATION_BLOCKING_CUT_V2 = [CUT01,CUT02,CUT03,CUT04.source_binding,CUT05]
M01_MINIMUM_STATE_CONTRACT_COMPLETE = NO
M01_CLOSURE_REENTRY_ALLOWED = YES
M02_READY = NO
NEXT_PACKAGE = M01 minimum-state contract closure and explicit scoped acceptance allocation
EXPECTED_GLOBAL_CONTROL_STATE = MIXED_WAIT
EXPECTED_RUNNABLE_ACTIONS = []
EXPECTED_DECISION_READY_ACTIONS = []
EXPECTED_RESUME_ALLOWED = NO
EXPECTED_EXTERNAL_BOUNDARIES = 8
RESTORED_AND_QUALIFIED = 2/17 (unchanged)
C06A_3_RETRY_ALLOWED = NO
C07_RETRY_ALLOWED = NO
V0_1_CURRENT_STATUS = CORRECTION_REQUIRED
IMPLEMENTATION_MODIFIED = NO
REAL_E1_EVIDENCE_CREATED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
```

Validation: focused native regression 9 PASS; mechanical action/status/route and dataclass-field coverage checks PASS; companion JSON, cross-references and readiness-conjunction checks PASS. All 10,911 frozen files and all captured pre-existing implementation/planning/backlog files match pre-task hashes. `git diff --check` and new-artifact whitespace checks PASS. These checks validate this analysis and repaired synthetic control behavior; they do not qualify migration.
