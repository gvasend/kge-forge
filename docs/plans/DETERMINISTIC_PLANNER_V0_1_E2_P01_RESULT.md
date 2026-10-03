# E2-P01 — Canonical experiment preflight result

**RESULT = BLOCKED — E2_CONTRACT_INCOMPLETE.** The mandatory admission transaction cannot be identified in the current native event/replay interface. The plan explicitly requires P01 to stop on this condition. No E2 Action, P02–P06 package, evidence receipt, migration, baseline regression or authority issuance was executed. All 36 planned cases were inventoried; missing fixtures and oracles are recorded rather than treated as passes.

This is a bounded preflight finding, not a claim that Planner's existing receipt evaluator is incorrect. No runtime counterexample was executed and no repair is included. A separate interface-contract review must determine the admissible transaction and whether a bounded implementation correction is necessary.

## Exact P01 contract

Authoritative [experiment plan](DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_EXPERIMENT_1.md), its JSON package record, and [36-case matrix](DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_ACCEPTANCE_MATRIX_1.md) are pinned with inspected native code in the preflight companion.

- **Purpose:** “Canonical experiment contract and independent fixture/oracle preflight.”
- **Inputs:** this E2 plan, matrix, current native contracts and supported policy; N-REAL reconciliation permits independent parallel preparation but does not waive a gate.
- **Work, exact JSON:** “Pin6 complete Action definitions, sources/types,13-field O01 expectations,native correspondence,policy,decision/grant/proof/receipt contracts; resolve canonical evidence ingestion transaction and immutable bundle/source-index replay before execution. Stop on unsupported contract; no silent new event or rule-known setter.”
- **Outputs:** complete pinned definitions, source/claim/proof/grant/receipt interfaces, independent expected-state/negative fixtures and clean preflight. This attempt instead produces incomplete inventories and the complete blocking set below.
- **Acceptance, exact JSON:** “All30 requirements assigned; source-shaped negatives and independent expected states complete; no unresolved implementation/interface prerequisite.”
- **Assigned case:** the package JSON lists E2-A01. Its acceptance additionally requires preflight of the whole lifecycle and all 30 semantic coverage obligations; this run audits all 36 cases as requested. Those are not 36 executions assigned to P01.
- **Prerequisites:** JSON has an empty package-prerequisite list; prose requires the plan and existing native contracts. P01 can investigate without any other E2 package executing.
- **Unlocks:** P02 only after PASS and clean preflight. No unlock here.

## Mandatory admission boundary: E2-G01

The code inspection is reproducible by reading these pinned definitions:

1. [ExecutionEvent](../../adapter/planner/model.py#L606) admits only `SuppliedResult`, `RecordedDecision`, `DecisionReentry`, `ExternalEvent`, `SourceInvalidation`.
2. [apply_event](../../adapter/planner/core.py#L430) dispatches exactly those types and rejects unsupported events. The CLI delegates to `record_result`; it does not add an ingestion path.
3. [apply_receipt](../../adapter/planner/core.py#L450) requires `event.artifact` to resolve to a **produced** entity already present in `snapshot.entities`. Validation separately looks up ReceiptAdmission and evaluates authentication/claims. Receipt cannot add arbitrary bytes, entity or admission.
4. `_inventory` adds only supplied knowledge and action status, then readiness/satisfaction recomputation. RecordedDecision and DecisionReentry alter decisions/statuses/knowledge as prescribed; they do not add a new evidence entity/receipt admission. SourceInvalidation withdraws validity, not inserts positive support.
5. [codec replay and append_event](../../adapter/planner/codec.py#L430) recompute current state from initial+events, verify event outcomes and enforce exact current snapshot identity. Editing `bundle.current` to add new evidence cannot preserve that replay equation. Source provenance must also have exact bundle pins; `append_event` changes events/current, not sources.
6. `synthetic_receipt` in [existing replay tests](../../adapter/tests/test_planner_e1_replay.py#L401) builds counterfactual admitted trust with `replace(... entities=..., predicates=..., receipt_admissions=...)`. This is legitimate fixture setup for existing unit tests, but explicitly prohibited as E2 post-cold-load evidence ingestion by the governing E2 plan.

Static AST extraction of the closed event union passed; the extracted dispatch and source/code hashes are recorded in companions. No native state transition was used to establish this finding. No searched supported alternative transaction was found in model/core/codec/replay/CLI. This bounded result does not prove that an alternate architecture is impossible.

The checkpoint must contain absent evidence. Preloading produced evidence, replacing the cold-restored snapshot, resetting the initial ledger, introducing an unregistered event, or directly making a rule known would change the experiment or bypass its trust boundary. They are not repairs made by P01.

## Complete preflight blocking inventory

| ID | Classification | Finding | Closure required |
|---|---|---|---|
| E2-G01 | CONTRACT_INCOMPLETE | Post-cold-load new evidence source admission is not represented by the closed native event/persistence contract. Receipt requires a produced entity; the supported transitions do not add entities/ReceiptAdmission/source pins. | Establish a supported authenticated source admission transaction with immutable source-index and replay lineage, or separately scope a bounded correction. Do not change the experiment to preload positive evidence. |
| E2-G02 | FIXTURE_INCOMPLETE | Six planned Action purposes are not six complete 13-field profiles/native Action definitions. | Author six definitions and cross-references directly, then independently validate O01 and validate_model; no legacy projections. |
| E2-G03 | FIXTURE_INCOMPLETE | Concrete E2 source bytes/pins, role/target/scope/lineage/consumer bindings and policy pin are not yet frozen. | Pin the complete native source-role registry; reuse supported policy identity/version exactly. |
| E2-G04 | FIXTURE_INCOMPLETE | Root/slot proof predicates, bounded decision/dossier/grant applicability and independent expected witnesses are not instantiated. | Author source-bound predicates and positive/negative claim fixtures without positive evidence at checkpoint. |
| E2-G05 | FIXTURE_INCOMPLETE | Concrete request/receipt/reentry contracts, absence records and independent governed-unknown variant are not instantiated. | Bind exact proposition/producer/target/lineage/pins/held and reentry Actions; retain known-rule mainline and unknown variant. |
| E2-G06 | ORACLE_INCOMPLETE | Phase-level prose is not a pinned full-state oracle and concrete negative mutation/assertion suite. | Define state references, exact expected admissions/rejections/selected identities and no-result/no-resume invariants for each case. |
| E2-G07 | FIXTURE_INCOMPLETE | No E2 cold-process harness, input allowlist, trusted bundle identity or complete checkpoint fixture exists. | Bind native save/restore and process evidence; no in-memory helper replacement. Preserve chronological ledger. |
| E2-G08 | DEPENDENCY_INCOMPLETE | Integrated END/determinism/review require completed case fixtures and downstream evidence. | Finish P01 contract preflight, then execute only separately eligible packages. |

E2-G01 is the mandatory stop. E2-G02–G07 are outstanding authorized P01 fixture/contract preparation, not claims of absent historical E1 authority and not proven runtime defects. The E2 author can supply synthetic definition semantics directly when P01 resumes. This run does not create misleading “complete” candidates around an unsupported lifecycle interface. E2-G08 records execution dependencies, not an additional requirement to execute P02 during P01.

## Actions and native contract distinction

The six Actions remain E2-COLLECT, E2-CHECK, E2-PREPARE, E2-DECIDE, E2-REENTER and E2-FINISH. Their operation classes and NON_EFFECTING scope are declared by the plan. The Action inventory explicitly marks all uninstantiated fields null; null is an inventory marker, **not a native candidate value**. No O01 rejection or success is manufactured.

The existing O01 qualification profile's 13 definition fields are:

`authority_requirements, effect_boundary, executor, external_prerequisites, id, knowledge_requirements, lineage, prerequisite_actions, primary_operation_class, provenance, result_contract, scope, stage_role`.

The native `model.Action` has its own typed members (including accepted_inventory, evidence, requirements, authority, stage, cost, result/dossier and qualification). It is not literally a 13-member serialization. Both independently specified O01 expectations **and** native validation must pass; filling one does not automatically supply the other. No legacy profile or E1 envelope is renamed into an E2 source. No prospective declaration establishes an actual result, execution, completion, knowledge, root or slot satisfaction.

## Roles, authority, proofs and absence

The source-role companion inventories required native carriers/consumers for definitions, knowledge, dossier, grant, proof, route, absence, receipt, attestor and policy. These labels are report categories, not new runtime enums. Source identities, target identities, pins, scope/lineage/generation, currentness and provenance still require concrete E2 values. There is no complete source set against which to claim zero ambiguous bindings.

RootCondition.predicate and ValueSlot typed value/requirements/root_requirements must admit the exact root/slot proof. A generic valid entity or Action PASS cannot stand in for either. Authority requires the exact target/permission/context and independent provenance; existence is insufficient. Decision/dossier readiness and grant applicability remain separate. The proof/authority registry records every outstanding binding and its native consumer.

ExternalGate + EvidenceRequirement + ExternalResolutionContract must agree on proposition, requirement/target identity, producers, gate/request, receipt, reentry/held Actions, context and pinned governing sources. Absence carries no positive claim. The mainline uses a known validation rule with missing evidence; A14 is a separate deliberate `rule_known=false` checkpoint. The repair governs waiting only, and receipt does not set a missing rule true. Concrete E2 route fixtures remain incomplete even though the native repaired contract exists.

## Phase control and continuation

The following are independently planned constraints, not trusted manifest labels or observed results. Exact state/witness oracles remain incomplete.

| Phase | Planned control | Canonical reason / remaining specification |
|---|---|---|
| INITIAL | RUNNABLE | E2-COLLECT and E2-CHECK eligible; selected identity must be independently pinned |
| PRE_EXTERNAL | PHASE_DEPENDENT | RUNNABLE until dossier complete; HUMAN_HANDOFF when only simulated decision is ready; then external boundary |
| EXTERNAL_CHECKPOINT | EXTERNAL_WAIT | No eligible internal/human action; evidence absent; known mainline rule, exact external route |
| COLD_RESTORED | EXTERNAL_WAIT | Identical canonical checkpoint inputs and independent recomputation |
| EVIDENCE_RECEIVED | EXTERNAL_WAIT | Pending entity only; no accepted observations; no resume |
| EVIDENCE_VALIDATED | NOT_YET_PINNED | Receipt completeness alone is not accepted reentry; native held-action statuses and boundaries must be fixed before exact control can be asserted |
| REENTRY_ELIGIBLE | RUNNABLE | Current receipt + accepted lineage + verified pins + named eligibility |
| POST_REENTRY | NOT_YET_PINNED | Native next selection and root/slot outcomes depend on independent complete predicates; no guaranteed terminal success from PASS |

PRE_EXTERNAL includes several phases and cannot honestly be assigned one constant control label. Evidence validation cannot automatically grant resume. The C03 conjunction remains current evidence + accepted reentry lineage + verified source/policy pins + named-action eligibility and all its native prerequisites. There is no direct resume toggle. The future E2-REENTER → E2-FINISH path must be proven through normal actionability/selection and bounded supplied output; the names alone are not a proof that the path exists.

## Persistence, invalidation and determinism

Use native PLANNER-SNAPSHOT-1 inside PLANNER-BUNDLE-1: initial and current full Snapshots, ordered execution events with parent/outcome identities and resume binding, source pins, policy pin/version and declared bundle scope. Snapshots include all applicable Action/status, knowledge, root/slot, assertion/entity/predicate, context, information, decision, evidence requirement/gate/admission/observation, boundary and goal state. Do not store computed control labels as an oracle input.

`codec.snapshot_id` hashes canonical typed bytes under `planner-snapshot-v1`; `codec.bundle_id` hashes replay-validated bundle bytes under `planner-bundle-v1`. `_wire`, `SET_FIELDS` and `canonical_bytes` own serialization, with sorted keys and canonical unordered collections. Different identity domains/profiles are not interchangeable even with equal digests. Concrete E2 identities are not yet available.

Cold qualification requires actual writer termination and independent fresh readers using only pinned bundle/source/contracts and a trusted expected bundle identity. Compare the complete semantic state, selection, branch witnesses and resume proof. Expected-answer files belong to the comparison harness only. Existing codec support is not a completed E2 checkpoint contract.

Required invalidation covers knowledge, exact root/slot proof, authority, external route and received evidence after reload. Native SourceInvalidation must withdraw dependent support; route invalidation with no alternative exposes PLAN_DEFECT in the unknown variant. Concrete source-disjoint E2 mutants remain to be authored.

The determinism companion defines seeds 0,1,7,101; reversed/rotated action/source/proof/authority/goal sets; recursive JSON-key reversal; repeated computation; independent processes; at least three cold readers per checkpoint/seed. Compare full admission, Computation/reasons/branches, selected identity, root/slot/knowledge/authority/evidence validity, policy, resume proof and snapshot/bundle/event identities. Do not permute causal ledger chronology or ordered policy clauses. Matrix definition is complete as a plan, not an executed determinism result.

## All 36 acceptance cases

A primary classification partitions the 36 cases: **31 FIXTURE_INCOMPLETE, 1 CONTRACT_INCOMPLETE, 3 DEPENDENCY_INCOMPLETE, 1 EXECUTABLE**. Additional oracle findings overlap and are listed separately in JSON. EXECUTABLE E2-REG means the existing baseline command/assertions are available, **not that they ran or passed**. REVIEW's downstream evidence dependency is expected; it is not an instruction to run review before P01. No new concrete E2 fixture or negative executable oracle is counted as complete.

| Case | Primary classification | Exact remaining input/interface |
|---|---|---|
| E2-A01 | FIXTURE_INCOMPLETE | All six complete profiles/native definitions and exact reference universe absent. |
| E2-A02 | FIXTURE_INCOMPLETE | Two eligible canonical initial Actions, supported policy pin and independently selected tie-break winner absent. |
| E2-A03 | FIXTURE_INCOMPLETE | Concrete SuppliedResult/KnowledgeRecord inventory and producer/source assertions absent. |
| E2-A04 | FIXTURE_INCOMPLETE | DecisionDossier alternatives/checklist/facts and prepared-result/readiness oracle absent. |
| E2-A05 | FIXTURE_INCOMPLETE | Bounded synthetic choice, grant target/permission and applicability predicate absent. |
| E2-A06 | FIXTURE_INCOMPLETE | Exact evidence requirement, gate, held/reentry relation and source-bound external route absent. |
| E2-A07 | FIXTURE_INCOMPLETE | No complete E2 bundle, pinned checkpoint/source index or trusted identity manifest. |
| E2-A08 | FIXTURE_INCOMPLETE | No E2 checkpoint/process harness/input allowlist and full semantic comparison fixture. |
| E2-A09 | CONTRACT_INCOMPLETE | Mandatory new-source admission transaction unavailable in inspected event/replay interface (E2-G01). |
| E2-A10 | FIXTURE_INCOMPLETE | Concrete authenticated ReceiptAdmission/claims absent; depends on E2-G01. |
| E2-A11 | FIXTURE_INCOMPLETE | Exact receipt reentry/named-action contract and C03 source/policy/lineage proof absent; depends on E2-G01. |
| E2-A12 | FIXTURE_INCOMPLETE | No accepted reentry output inventory, selected-action oracle or native post-reentry event fixture; depends on E2-G01. |
| E2-A13 | FIXTURE_INCOMPLETE | Exact root/slot-specific proof identities and predicate operands absent; no PASS-to-satisfaction shortcut. |
| E2-A14 | FIXTURE_INCOMPLETE | Existing repaired unknown-rule regressions reusable; E2 checkpoint variant and exact resolution-contract pins absent. |
| E2-A15 | FIXTURE_INCOMPLETE | No separate E2 accepted knowledge/proof/authority sources and dependent-state mutation expectations. |
| E2-A16 | FIXTURE_INCOMPLETE | No E2 bound route fixture/source pin to invalidate; existing regression is not this fixture. |
| E2-N01 | FIXTURE_INCOMPLETE | No E2-A14 base/mutation and exact expected defect witness. |
| E2-N02 | FIXTURE_INCOMPLETE | No exact malformed E2 route fixture or pinned rejection stage; prose offers admission-or-control alternatives. |
| E2-N03 | FIXTURE_INCOMPLETE | No exact wrong-lineage candidate/pin and consumer rejection assertion. |
| E2-N04 | FIXTURE_INCOMPLETE | No E2 evidence/attestor invalidation fixture after receipt/cold load; depends on E2-G01. |
| E2-N05 | FIXTURE_INCOMPLETE | No concrete E2 source/pin/domain-substitution pair. |
| E2-N06 | FIXTURE_INCOMPLETE | No E2 applicable grant and unrelated/wrong-class/out-of-scope variants. |
| E2-N07 | FIXTURE_INCOMPLETE | No E2 root/slot proof baseline and exact malformed/wrong-target proof mutants. |
| E2-N08 | FIXTURE_INCOMPLETE | No complete E2 initial Action fixture to mutate with dangling/wrong-domain prerequisite. |
| E2-N09 | FIXTURE_INCOMPLETE | No E2 producer history/current knowledge-source pair or exact held descendant oracle. |
| E2-N10 | FIXTURE_INCOMPLETE | No admitted E2 bundle/policy baseline and unrelated supported pin mutant. |
| E2-N11 | FIXTURE_INCOMPLETE | No E2 trusted checkpoint identity/event-parent/source-index tamper fixture. |
| E2-N12 | FIXTURE_INCOMPLETE | No concrete E2 selected-only event candidate and rejection/unchanged-state assertions. |
| E2-N13 | FIXTURE_INCOMPLETE | No complete E2 declaration and corresponding wrong SuppliedResult candidate. |
| E2-N14 | FIXTURE_INCOMPLETE | No E2 waiting/received baseline and exact out-of-order event mutants; depends on E2-G01. |
| E2-N15 | FIXTURE_INCOMPLETE | No E2 accepted receipt fixture with independently blocked named Action; depends on E2-G01. |
| E2-N16 | FIXTURE_INCOMPLETE | No E2 independent machine/human/fact-blocked variants and exact branch witnesses. |
| E2-D01 | DEPENDENCY_INCOMPLETE | Dimensions specified below; complete semantic fixtures and canonical identities unavailable. |
| E2-END | DEPENDENCY_INCOMPLETE | Depends on A01-A13 fixtures plus D01 and the unresolved new-source admission transaction. |
| E2-REG | EXECUTABLE | Existing baseline test suites and plan command are present; execution belongs to P05, not P01. |
| E2-REVIEW | DEPENDENCY_INCOMPLETE | Procedure specified, but independent review subject requires END/D01/REG execution evidence from P05. |

Cross-case design preserves six shared Actions, the existing policy requirement, the native formats, prospective/actual separation and known-rule/unknown-variant separation. No contract conflict is established. Full concrete cross-case compatibility is **not proven** while definitions and bindings are incomplete. All 30 semantic requirements remain mapped to cases in the authoritative JSON; that mapping is coverage planning, not execution coverage.

## Gate and preservation

P02 readiness is the conjunction of six complete O01/native definitions, complete concrete role/proof/authority/route contracts, supported replayable source admission, complete independent fixtures/oracles for all 36 cases, and no conflict. That predicate is false. The next control step is bounded E2-G01 admission-contract/correction scoping, followed by P01 completion; no new repair package is executed here.

N-REAL remains unchanged and unsatisfied. E2-P01 is synthetic canonical preflight and supplies no real E1 reconstruction evidence. E2 remains unqualified and Planner v0.1 remains CORRECTION_REQUIRED. Historical closed findings were not reopened or newly retested by this document.

Preservation compares all pre-existing files under adapter, docs/plans, docs/backlog and frozen E1 against a pre-write SHA-256 inventory. Exact E1 path set and all 10,911 content hashes are checked. Existing regression files, Planner implementation, plan/acceptance/N-REAL artifacts and prior results remain unchanged. No evidence bundle, E1 request, authority record or experiment execution artifact was created. Only these new planning/preflight outputs were written. `git diff --check` is required and recorded in JSON validation.

## Companions

- [DETERMINISTIC_PLANNER_V0_1_E2_P01_ACTIONS.json](DETERMINISTIC_PLANNER_V0_1_E2_P01_ACTIONS.json)
- [DETERMINISTIC_PLANNER_V0_1_E2_P01_SOURCE_ROLES.json](DETERMINISTIC_PLANNER_V0_1_E2_P01_SOURCE_ROLES.json)
- [DETERMINISTIC_PLANNER_V0_1_E2_P01_PROOF_AUTHORITY.json](DETERMINISTIC_PLANNER_V0_1_E2_P01_PROOF_AUTHORITY.json)
- [DETERMINISTIC_PLANNER_V0_1_E2_P01_PREFLIGHT.json](DETERMINISTIC_PLANNER_V0_1_E2_P01_PREFLIGHT.json)
- [DETERMINISTIC_PLANNER_V0_1_E2_P01_FIXTURES_ORACLES.json](DETERMINISTIC_PLANNER_V0_1_E2_P01_FIXTURES_ORACLES.json)
- [DETERMINISTIC_PLANNER_V0_1_E2_P01_DETERMINISM.json](DETERMINISTIC_PLANNER_V0_1_E2_P01_DETERMINISM.json)

## Report

```text
WORK_PACKAGE = E2-P01
RESULT = BLOCKED
REASON = E2_CONTRACT_INCOMPLETE
E2_ACTIONS = 6
ACTION_DEFINITIONS_COMPLETE = 0/6
O01_ADMISSIBLE = 0/6 proven; validation not run on absent candidates
SOURCE_ROLES_COMPLETE = NO
ROOT_SLOT_PROOFS_COMPLETE = NO
AUTHORITY_EVIDENCE_MODEL_COMPLETE = NO
EXTERNAL_BOUNDARY_COMPLETE = NO
COLD_RESTORE_CONTRACT_COMPLETE = NO (native codec exists; E2 concrete checkpoint incomplete)
SYNTHETIC_REENTRY_CONTRACT_COMPLETE = NO
POST_REENTRY_PATH_COMPLETE = NO
ACCEPTANCE_CASES = 36
EXECUTABLE_CASES = 1
CONTRACT_INCOMPLETE_CASES = ["E2-A09"]
FIXTURE_INCOMPLETE_CASES = ["E2-A01", "E2-A02", "E2-A03", "E2-A04", "E2-A05", "E2-A06", "E2-A07", "E2-A08", "E2-A10", "E2-A11", "E2-A12", "E2-A13", "E2-A14", "E2-A15", "E2-A16", "E2-N01", "E2-N02", "E2-N03", "E2-N04", "E2-N05", "E2-N06", "E2-N07", "E2-N08", "E2-N09", "E2-N10", "E2-N11", "E2-N12", "E2-N13", "E2-N14", "E2-N15", "E2-N16"]
ORACLE_INCOMPLETE_CASES = ["E2-A01", "E2-A02", "E2-A03", "E2-A04", "E2-A05", "E2-A06", "E2-A07", "E2-A08", "E2-A10", "E2-A11", "E2-A12", "E2-A13", "E2-A14", "E2-A15", "E2-A16", "E2-N01", "E2-N02", "E2-N03", "E2-N04", "E2-N05", "E2-N06", "E2-N07", "E2-N08", "E2-N09", "E2-N10", "E2-N11", "E2-N12", "E2-N13", "E2-N14", "E2-N15", "E2-N16"]
DEPENDENCY_INCOMPLETE_CASES = ["E2-A09", "E2-D01", "E2-END", "E2-REVIEW"]
CONTRACT_CONFLICTS = []
DETERMINISM_MATRIX = DEFINED; NOT EXECUTED; concrete fixtures pending
E2_P02_READY = NO
NEXT_PACKAGE = Bounded E2-G01 source-admission contract review/correction scoping, then resume E2-P01; P02 not eligible
N_REAL_SATISFIED = NO
CANONICAL_E2_QUALIFIED = NO
PLANNER_V0_1_REQUALIFICATION_READY = NO
V0_1_CURRENT_STATUS = CORRECTION_REQUIRED
IMPLEMENTATION_MODIFIED = NO
E1_ARTIFACTS_MODIFIED = 0
REAL_E1_EVIDENCE_CREATED = NO
PRODUCTION_EFFECT = NO
```
