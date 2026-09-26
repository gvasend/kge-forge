# E1 decision-input and reentry semantics 1

Planner-specification correction only. Two new non-effecting preparation actions are actionable: INPUT-BUDGET and INPUT-IMPLEMENTATION. The validated selector chooses **INPUT-BUDGET at Criterion 5**. Nothing is executed. No root, slot, authority, implementation, graph or lifecycle state is changed.

## Decision lifecycle

| State | Exact entry | Exact exit |
|---|---|---|
| SEMANTIC_GAP_IDENTIFIED | Accepted outcome/gap evidence names exact unresolved contract question, scope and provenance. | Register named decision requirement; no decision eligibility inferred. |
| DECISION_INPUTS_REQUIRED | Named question exists; inventory records each input as ESTABLISHED, BOUNDED_PREPARATION_REQUIRED or EXTERNAL_FACT_REQUIRED. | Deterministically classify A/B/C using completeness predicates below; unknown inputs fail closed. |
| DECISION_INPUT_ACQUISITION | Branch B; approved bounded source set and preparation scope, no external fact required merely to begin. | PASS only for exact dossier acceptance; missing facts return BLOCKED with receiver gate; no missing fact guessed. |
| DECISION_DOSSIER_READY | Accepted dossier artifact has question, concrete alternatives, exact scope, evidence/provenance, consequences, exclusions and all decision-dependent facts. | Independent readiness checklist verifies source identities, completeness and no unresolved decision-dependent fact; otherwise return to inputs required. |
| DECISION_READY | Every required factual input and dossier predicate verified; no decision outcome asserted. | Only explicit Architect instruction may execute decision; scheduler recommendation is not authority. |
| ARCHITECT_DECISION | Explicit scoped Architect instruction identifies dossier, option and exclusions. | Record approve/reject/defer separately; reject/defer leave downstream blocked, no implicit grant. |
| DECISION_RECORDED | Separate authenticated append-only decision record matches exact dossier/scope; accepted decision payload present. | Schedule non-effecting downstream reevaluation, or preserve rejection/defer; no root or slot transition inferred. |
| DOWNSTREAM_REEVALUATION | Accepted applicable decision and required source evidence available; reevaluation action explicitly defined. | Accepted proof of type/selector or remaining source gate; only independent root/slot criteria may later resolve state. |

The arrows define evidence transitions, not elapsed phases. For existing complete evidence, branch A may establish dossier/readiness states without rerunning preparation; every predicate must already have an accepted attestation. Authority-required, a proposal, a passed inventory, or a permission to prepare is never a readiness attestation. Receipt, acceptance, action completion, governing decision and root/slot satisfaction remain separate.

## New bounded action type

DECISION_INPUT_ACQUISITION inspects its named accepted corpus and prepares explicit unadopted alternatives, scope, projections and consequences. It cannot supply missing external facts, decide, issue authority or execute downstream work. Its effect class is NON_EFFECTING. Its static selector class is ARCHITECT_PREPARATION; this extends class mapping only, preserving the validated criterion order and rankings. The existing selector’s coverage/information metrics remain unavailable and are not estimated.

## Deterministic A/B/C reentry

A: all exact dossier predicates and independent readiness attestations exist -> enable the named decision stage, subject to explicit Architect execution. B: an exact bounded preparation operation is possible from accepted sources -> enable its input action. C: a concrete factual prerequisite of the next operation is absent -> register the named external-evidence receiver and remain blocked. Unknown completeness cannot select A.

Preparation may begin with unresolved downstream facts only when its bounded purpose is to define alternatives and identify their requirements. It may PASS as a decision-ready dossier only if every fact necessary to choose is present. A conditional alternative must exclude deferred source qualification from its decision proposition explicitly; if that cannot be done without guessing, return BLOCKED. No blanket implementation-domain or source-equality choice is allowed.

Route IDs are stable and unique per requirement. Replay creates no duplicate actions. Unknown future gaps require a bounded specification, not implicit LLM creation of runtime actions. A new source identity stales dependent readiness. External receipts are append-only; accepted reevaluation creates a new attempt overlay rather than rewriting historical outcomes.

## Budget route

SEM-BUDGET accepted AUTHORITY_REQUIRED knowledge -> INPUT-BUDGET -> DEC-BUDGET -> REEVAL-BUDGET -> DEC-INTERFACES / CONTRACT-T1 / MAP-BUDGET.

INPUT-BUDGET requires the hash-bound accepted SEM-BUDGET result, not successful SEM-BUDGET completion. The known authoritative budget identity, recorded bounds and representation question suffice to begin preparation. Its exact acceptance criterion is:

> Prepare authority-reference, full policy-body and explicitly typed-projection alternatives using only accepted StatusBudgetAuthority identity/bounds. Specify exact JSON type, source field/selector, canonical bytes rule, authority/source linkage, compatibility and validation per alternative; preserve every bound and scope. Choose nothing. PASS requires all common dossier predicates; a partial dossier may retain knowledge but must not enable DEC-BUDGET. Do not acquire external facts; stop at missing required decision facts.

The action must concretize the alternatives; this specification does not prepare that dossier or choose among them. DEC-BUDGET additionally requires the accepted dossier and DOSSIER-READY-BUDGET attestation, and explicit Architect instruction. REEVAL-BUDGET verifies the recorded decision against the original semantic criterion. Missing applicability/source facts still block; no budget field or bounds are changed.

## Implementation-identity route

SEM-IMPLEMENTATION accepted AUTHORITY_REQUIRED knowledge -> INPUT-IMPLEMENTATION -> DEC-IMPLEMENTATION -> REEVAL-IMPLEMENTATION -> DEC-INTERFACES / CONTRACT-T1 / MAP-IMPLEMENTATION.

The accepted domain ambiguity suffices to begin bounded alternative preparation, not to approve an identity. Its exact acceptance criterion is:

> Prepare runtime-content-domain and distinct-implementation-domain alternatives. Distinguish recorded runtime reference from verified frozen bytes and a qualified implementation selector. Specify identity type, owning source domain/record, canonical selector and verification obligations per alternative; mark every unknown source/byte/applicability fact. Choose no domain and assert no equivalence. A conditional option may defer downstream source qualification only if its governing proposition can be decided without that fact; otherwise dossier remains BLOCKED. PASS requires all common dossier predicates; a partial dossier may retain knowledge but must not enable DEC-IMPLEMENTATION. Do not acquire external facts; stop at missing required decision facts.

DEC-IMPLEMENTATION requires DOSSIER-READY-IMPLEMENTATION and all decision-dependent facts. REEVAL-IMPLEMENTATION must establish the original complete semantic type/domain/selector proof from the applicable record and sources. A selected distinct domain without a qualified owning source remains blocked. Current runtime reference presence does not authenticate frozen bytes. No fact acquisition is performed here.

## Removing the terminal semantic entry without weakening gates

The four named downstream consumers replace SEM-BUDGET/SEM-IMPLEMENTATION success dependencies with the corresponding REEVAL output dependencies. REEVAL must prove the full original semantic criterion, so this is not a success bypass. Historical semantic actions remain attempted/blocked with unchanged AUTHORITY_REQUIRED records. Accepted gap knowledge unlocks preparation; a later independent accepted reevaluation supplies the required downstream proof. New action edges belong to the resolution-plan specification only; the typed graph and existing E1 dependency DAG are unchanged.

## Dossier and decision acceptance

Every dossier/readiness check requires:
- exact question and scope.
- hash-bound source inventory and provenance.
- concrete alternatives with exact canonical value/type/projection contracts.
- per-alternative factual assumptions and consequences.
- authority granted and explicitly excluded.
- downstream acceptance/qualification obligations.
- no invented fact or unqualified identity equivalence.
- all facts necessary to choose are established; deferred downstream facts clearly excluded from decision proposition.
- independent readiness check and freshness/source identity validation.

Decision records must authenticate the exact reviewed dossier and selected proposition, scope, source/identity rules and exclusions. Rejection/defer does not enable reevaluation as if approved. No action automatically issues authority. New records must retain separate authority semantics and append-only history.

## Six fact-receipt routes and DEC-EXEC regression

The prior cut named the evidence but lacked uniform machine-readable receipt/reentry predicates. Six explicit gates now record pending input, provenance/applicability checks and the receiving action. None is satisfied, no input is acquired and no blocked action is retried.

| Receiver gate | Exact missing facts | Receiving action |
|---|---|---|
| EXT-REENTRY-DEC-EXEC | Concrete independently authoritative executable-policy source with exact projector, or a fully specified independent permission proposal with scope and consequences. No permissions inferred from argv. | DEC-EXEC |
| EXT-REENTRY-PREP-AUDIT | Exact proposed namespace/store identity, owner/provenance, R4/G4 release/context applicability and independently evidenced outside-agent-root placement. | PREP-AUDIT |
| EXT-REENTRY-PREP-RUNTIME_HEAD | Concrete proposed current R4/G4 head selector and authority body/identity, exact publication target, owning authority domain/selection mechanism, and release/context/lineage evidence. | PREP-RUNTIME_HEAD |
| EXT-REENTRY-PREP-SUPERVISOR | Concrete proposed supervisor selector and owning selection evidence applicable to current release/context, with lineage/freshness evidence. | PREP-SUPERVISOR |
| EXT-REENTRY-S-ANCESTRY | Authenticated current attempt allocation, predecessor and session/turn owning evidence for the exact current envelope. A repeated NOT_FOUND or the already resolved attempt ID alone is insufficient. | S-ANCESTRY |
| EXT-REENTRY-S-APPROVAL | An independently authenticated, applicable owning specific-approval record and exact current scope/lineage selector; prose references and historical approvals cannot substitute. | S-APPROVAL |

A complete, retrievable new submission permits only a separately authorized read-only validation attempt. Validation rejection preserves the hold; acceptance removes only its matching hold and recomputes remaining criteria. PREP-AUDIT/RUNTIME_HEAD/SUPERVISOR must still produce accepted preparation outputs before their decisions can be considered. S-ANCESTRY/S-APPROVAL must still satisfy their exact acquisition criteria. This route is not an invented fact-finding operation or permission to retry without new input.

DEC-EXEC is branch C. S-EXEC PASS records only the bounded missing-policy inventory; it cannot meet the dossier predicates. EXT-REENTRY-DEC-EXEC requires a concrete independent source/projector or exact independently grounded policy proposal, never argv-derived permissions. Readiness is checked after that submission; the existing BATCH1-ACTIONABILITY-01 hold stays in force. This lifecycle would have prevented its premature exposure. No policy proposal is constructed here.

## Issued decisions and remaining gates

Existing DEC-BINDING deterministically reevaluates BUILD-BINDING; DEC-IGNORED reevaluates CONTRACT-T1/MAP-IGNORED; DEC-VALIDATOR reevaluates IMPL-VALIDATOR. These routes retain their exact grant scopes and all source/schema prerequisites. New DEC-BUDGET and DEC-IMPLEMENTATION records route to their respective REEVAL actions. Every other DEC-* stage retains its declared downstream consumers with the same independent source/readiness checks. Recording a decision never runs those consumers.

## Current replay and invariants

The current plan has 62 actions: 11 completed, 49 blocked and 2 actionable. All six external receipt gates and both dossier-ready gates are unsatisfied. INPUT-BUDGET and INPUT-IMPLEMENTATION alone have complete prerequisites to begin bounded work. No decision, mapping, repair or construction becomes actionable. Original static waves remain historical planning projections; the current replay is authoritative for scheduling.

Criteria 1 and 2 are not decisive: no complete graph outcome metric exists. Criterion 3 maps both inputs to ARCHITECT_PREPARATION; Criterion 4 ties at NON_EFFECTING and has no cost metadata. Criterion 5 selects INPUT-BUDGET. Twenty-two deterministic action orderings and 100 identical-state replays agree. Negative readiness tests reject authority-required alone, incomplete dossiers and each missing predicate. Complete synthetic dossier predicates can establish readiness but confer no authority. Action edges remain acyclic.

Historical action results and execution_history are unchanged; prior execution-state snapshot is retained in planner_specification_revisions. Current eligible/blocked sets are recomputed, while the last executed action’s report remains explicitly historical. No production implementation of the selector or lifecycle is installed. Existing graph, authority and closure files are byte-checked unchanged.

## Source identities

Machine-readable evidence, source hashes, action definitions, lifecycle predicates, six receiver gates, prerequisite rewrites, validation and replay are recorded under `decision_input_reentry_semantics` in the plan. The pre-correction plan hash is a snapshot, not an asserted hash of the changed file. All semantic evidence retains its exact original artifact identity; stale inputs close readiness until revalidated.

```text
PLANNER_CORRECTION = DECISION_INPUT_REENTRY_1_SPECIFICATION_ONLY
NEW_ACTION_TYPES = ["DECISION_INPUT_ACQUISITION"]
BUDGET_REENTRY_ROUTE = ["SEM-BUDGET accepted AUTHORITY_REQUIRED knowledge", "INPUT-BUDGET", "DEC-BUDGET", "REEVAL-BUDGET", "DEC-INTERFACES / CONTRACT-T1 / MAP-BUDGET"]
IMPLEMENTATION_REENTRY_ROUTE = ["SEM-IMPLEMENTATION accepted AUTHORITY_REQUIRED knowledge", "INPUT-IMPLEMENTATION", "DEC-IMPLEMENTATION", "REEVAL-IMPLEMENTATION", "DEC-INTERFACES / CONTRACT-T1 / MAP-IMPLEMENTATION"]
EXEC_REENTRY_ROUTE = ["S-EXEC accepted gap knowledge", "EXT-REENTRY-DEC-EXEC", "independent complete dossier/readiness check", "DEC-EXEC", "CONTRACT-T1 / MAP-EXEC_BINS"]
FACT_ACQUISITION_ROUTES = ["EXT-REENTRY-DEC-EXEC", "EXT-REENTRY-PREP-AUDIT", "EXT-REENTRY-PREP-RUNTIME_HEAD", "EXT-REENTRY-PREP-SUPERVISOR", "EXT-REENTRY-S-ANCESTRY", "EXT-REENTRY-S-APPROVAL"]
ACTIONABLE = ["INPUT-BUDGET", "INPUT-IMPLEMENTATION"]
NEXT_ACTION = INPUT-BUDGET
DECIDING_CRITERION = 5
ROOT_CONDITIONS_RESOLVED = 0
ROOT_CONDITIONS_REMAINING = 27
SLOTS_RESOLVED = 0
SLOTS_REMAINING = 41
TEMPLATE1_CONSTRUCTION_READY = NO
CANDIDATE3_RESUMPTION_READY = NO
PRODUCTION_EFFECT = NO
```
