# MC01 Architect decision readiness review 1

**AD-K is ready for review as a bounded schema-policy decision. AD-R and AD-A are CONTRACT_BLOCKED.** All eight role families require deterministic mapping work; none is wholly determined by selecting these options. No additional role decision or missing frozen fact is established. NEXT_CONTROL_STEP = MIXED: review AD-K independently while completing option contracts and mappings. No option is selected and no authority is issued.

The [machine-readable companion](DETERMINISTIC_PLANNER_V0_1_MC01_ARCHITECT_DECISION_READINESS_1.json) contains the three option audits, eight role records with selectors, all eight consequence/preflight traces, 63-action conditional AD-K coverage and preservation evidence. The [original dossier](DETERMINISTIC_PLANNER_V0_1_MC01_ARCHITECT_DECISION_DOSSIER_1.md) remains unchanged.

## Readiness findings

The review uses all 819 cells from closure 2. Its 186 unresolved cells comprise 63 result contracts, 63 authority requirements, 56 omitted knowledge declarations, three explicit knowledge joins and one external prerequisite join. The last four remain mapping obligations. The other 633 cells have source information; this is not proof of complete O01 admission.

O01's executable specification checks all 13 fields and compares result, authority, knowledge and provenance values against independently trusted definitions. It does not derive those definitions. See `reference.program/actions` in the [preflight contract](DETERMINISTIC_PLANNER_V0_1_C06A_3_PREFLIGHT_CLOSURE_1.json). Native Action validation is a separate layer; the [Planner model](../../adapter/planner/model.py) supplies the existing operation, result and authority enums and route restrictions. Leaving both unchanged is necessary but insufficient to prove compatibility of a proposed new rule.

| Decision | Question/options | Affected actions/fields | Role impact | Readiness |
|---|---|---:|---|---|
| AD-R | R1 independent transition evaluation versus R2 explicit proof-guarded transitions; both use proposed class output types | 63 / 63 result_contract cells | B01, B06; B05 proof compatibility | CONTRACT_BLOCKED |
| AD-A | A1 task scope plus explicit grants versus A2 authority predicate for every operation | 63 / 63 authority_requirements cells | B01, B05 | CONTRACT_BLOCKED |
| AD-K | K1 omitted knowledge member means empty independent prerequisite map versus K2 reject until explicitly declared | 56 / 56 knowledge_requirements cells | B01 policy component; explicit B06 joins unchanged | DECISION_READY |

All six options are distinguishable and conceptually bounded, and prohibit historical-execution inference. Their executable completeness differs:

- **R1 is underspecified.** Proposed output names do not define payload/type interpretation. “Only where native routes permit” leaves the actual allowed-outcome correspondence unresolved. An Architect cannot yet assess whether the proposed operation-class grouping preserves every acceptance criterion.
- **R2 has those same gaps**, plus an unresolved mapping from affected targets to actual proof capabilities and canonical transition representation. Merely declaring PROOF_GATED does not settle that mapping. R1 and R2 can be distinguished conceptually, but their native compatibility and consequences are not established.
- **A1 is underspecified.** “Accepted execution-task scope” has no exact target requirement expression here. The mapping from operation, declared grant and effect boundary to native AuthorityClass and exact predicate remains open. That mapping can materially alter what the option permits.
- **A2 is also underspecified.** It adds authority requirements for non-effecting operations without defining their typed predicate or assessing the additional permission-source obligations. A declared requirement would not provide the authority. This is an incomplete option contract, not proof that frozen evidence must be acquired now.
- **K1 and K2 are executable at the decision's boundary.** For pinned schema `E1-TEMPLATE1-GRAPH-RESOLUTION-PLAN-1`, missing-member detection and empty-map versus reject behavior are deterministic. Explicit nonempty declarations remain untouched and require their existing joins. Unknown schema or malformed input fails closed. This choice does not depend on the unresolved result/authority mappings to define its meaning.

Reject-on-missing is not enough to make R/A executable: their nominal supported route still lacks a defined successful construction. K2, by contrast, deliberately chooses rejection as its complete policy outcome for the specified omission case.

No new taxonomy is needed. Existing effect classes and definition/execution separation are retained. Declarations do not establish execution, completion, results, knowledge, root/slot satisfaction, authority, applicability or decision readiness.

## Human review: the one ready decision

**DECISION ID: AD-K**

**Question:** For the pinned legacy plan schema, should an omitted `knowledge_requirements` member mean no independent knowledge prerequisite, or an incomplete definition?

**Option A — K1:** Normalize omission to an empty independent knowledge-prerequisite map. Preserve explicit declarations and every separate action dependency, authority requirement and evidence gate. This is a new compatibility policy, not a recovered historical fact.

**Option B — K2:** Reject the incomplete definition until an authoritative definition supplement supplies that member. No historical result may act as the missing declaration.

**What changes:** One member-presence normalization rule across **56 actions / 56 fields**. K1 conditionally covers those cells; K2 leaves them requiring supplements. The companion lists all affected ActionIds. Four explicitly empty and three explicitly nonempty declarations are unaffected by this choice.

**Role impact:** B01 gains a policy component; no complete role family closes. B06's three producer/claim/type joins remain independent mapping work.

**Downstream consequences:** K1 does not admit any complete Action while result/authority/profile gaps remain. K2 intentionally retains 56 definition gaps. Neither modifies current holds, supplies evidence or permits execution. O01 stays unchanged; any eventual full candidate still requires independent expected-profile and native validation.

**Dependencies:** None on AD-R or AD-A for choosing this omission policy. Later application requires authenticated decision identity/version, the exact pinned source schema, provenance and ordinary source validity checks. Review **individually**, with a separate authority record if subsequently issued. No choice is recommended here.

## Eight role families

The [closure-2 role records](DETERMINISTIC_PLANNER_V0_1_M01_MC01_CLOSURE_2_ROLES.json) and [14-role registry](DETERMINISTIC_PLANNER_V0_1_M01_MC01_COMPLETION_1_ROLE_REGISTRY.json) already prescribe role discrimination. All eight families classify **DETERMINISTIC_MAPPING_REQUIRED**. B01 has decision-dependent field components, but selecting an option does not identify an exact source claim, target identity, context or admitted consumer.

| Family | Source and selector basis | Target/consumer | Current ambiguity and required mapping |
|---|---|---|---|
| B01 | Plan `/resolution_actions`, `/compiled_action_dependencies` | ACTION_DEFINITION_SOURCE → ActionId/O01 | Shared field construction, issued rules and independent expected profiles; all 63 definitions |
| B02 | Plan `/execution_state`, `/execution_history`; manifest state, completed/blocked actions and ledger | LEDGER_SOURCE → ActionStatus/current_completion, O02/O06 | Exact current support/hold reconciliation; selection entries cannot supply execution events |
| B03 | Plan root/deferred conditions and dependencies; graph entities/assertions/prerequisite projection | ROUTING_SOURCE/GRAPH_SOURCE → ConditionId/SlotId/Goal/PredicateId, O10 | Native identity and conditional predicate crosswalk for the bounded control graph |
| B04 | Manifest `/request_routes` joined by request/handoff IDs to `/control_transfer_items`; checkpoint `/resume_condition` | Absence/gate/routing roles → GateId/EvidenceId/receipt/reentry | Eight native routes, including composite implementation and DEC-EXEC readiness correspondence |
| B05 | Validator authority `/decision`, `/source_artifacts`, `/authority_id`, scope, preconditions and exclusions; pinned proof claims | AUTHORITY_RECORD_SOURCE or PROOF_SOURCE → O08/O09 | Exact chain/proof parameterization; proof role cannot issue authority |
| B06 | Plan's explicit knowledge requirements and their exact pinned report/claim references | ACCEPTED_KNOWLEDGE_SOURCE → KnowledgeId/type/predicate | INPUT-BUDGET, INPUT-IMPLEMENTATION and FACT-BUDGET-APPLICABILITY claim/type joins |
| B07 | Budget obligations/producers/receipt/reentry and subject pins; B04 routing | External-gate/envelope roles → ExternalResolutionContract/context | Canonical contract body and source dependency conversion; generic waiting label insufficient |
| B08 | Manifest policy, ledger, subject/current graph/plan pins; checkpoint bindings/basis | Policy/checkpoint/inventory roles → baseline/FrozenControlProof | Raw versus extracted policy identity, joined source inventory and canonical baseline references |

The companion provides exact inspected source paths, selectors and pins, source/target types, identity domains, fields, consumer lists and affected-action scopes. For B05, named validator-chain actions are known; the complete reached O09/downstream consumer set is still a mapping output, not an invented exhaustive list. B04/B07 retain recorded reentry labels separately from recognized ActionIds. All-action coverage in B02/B03/B08 denotes possible consumers, not 63 already admitted bindings.

The mapping contract common to every row is:

1. Use the pinned record and semantic selector authorized by the existing role/consumer contract; filenames identify inputs but do not establish roles.
2. Join exact typed subject, role, scope, lineage and consumer references. Legacy identity, raw content hash and native target identity remain distinct even when digests match.
3. Require exactly one authorized correspondence per binding. Zero required matches leaves an unresolved mapping; incompatible multiple matches reject. Multiple roles are allowed only for separately supported claims with separate provenance.
4. Verify schema, raw pin, dependencies, frozen scope and currentness; then invoke the native admission consumer. Source invalidation withdraws the binding and dependent state after reload.

These specify deterministic obligations, not completed native conversion recipes. Existing O01/O02/O06/O08/O09/O10/O16, BR-C1, C03 and governed-unknown restrictions are retained. A missing typed selector/crosswalk must remain open rather than be filled by LLM judgment.

**Additional-decision test:** Existing role exclusions settle selection versus result, proof versus grant, historical versus current and absence versus positive evidence. No family meets the stronger test that all existing authority is insufficient, no candidate decision governs it, deterministic mapping is impossible and facts cannot resolve it. Additional decision roles = [].

**Fact-gap test:** Within the supplied 37-payload/BR-C1 inventory and recorded routes, no missing frozen fact requiring acquisition is established. The complete reached support inventory remains unqualified, so this is not a claim of global source sufficiency. Unknown concrete future evidence producers and the eight requested positive evidence bundles remain expected external absences; authority cannot manufacture them and they are not prerequisites to this readiness review.

## Eight option combinations and post-decision simulation

No combination is ranked. The prior dossier's 182/126 figures are **conditional governing coverage bounds**, assuming completed rule annexes. They are not fields resolved by the current options. The revised preflight explicitly stops before candidate generation rather than treating underspecified options as executable registries.

| Options | Prior possible coverage / 186 | Demonstrated fields resolved | Complete / incomplete actions | Resolved / unresolved role families | O01 admissible |
|---|---:|---:|---:|---:|---:|
| R1 A1 K1 | 182 | 0 | 0 / 63 | 0 / 8 | 0 |
| R1 A1 K2 | 126 | 0 | 0 / 63 | 0 / 8 | 0 |
| R1 A2 K1 | 182 | 0 | 0 / 63 | 0 / 8 | 0 |
| R1 A2 K2 | 126 | 0 | 0 / 63 | 0 / 8 | 0 |
| R2 A1 K1 | 182 | 0 | 0 / 63 | 0 / 8 | 0 |
| R2 A1 K2 | 126 | 0 | 0 / 63 | 0 / 8 | 0 |
| R2 A2 K1 | 182 | 0 | 0 / 63 | 0 / 8 | 0 |
| R2 A2 K2 | 126 | 0 | 0 / 63 | 0 / 8 | 0 |

For **each** row: no established contract conflict, but compatibility is not proven; native O01 failure count = **NOT RUN**, not 63 observed rejections. There are no complete candidates/independent real-source profiles to submit. Unmet comparison obligations include RESULT_CONTRACT, AUTHORITY_BINDING, explicit KNOWLEDGE_REQUIREMENT/PREREQUISITE_SET joins and PROVENANCE. The companion records these separately from observed failures.

The full simulated pipeline is: hypothetical issuance assumed → typed registry blocked by R/A option incompleteness → no whole-family decision-derived role mapping → independent B01–B08 mappings remain open → 819-cell coverage audit only → no complete 63-candidate set → MC01 BLOCKED. Even granting the prior optimistic bounds leaves four explicit joins with K1 or 60 original cells with K2, plus independent expected profiles and native role conversion. Missing contracts cannot be silently treated as performed mapping work.

Thus **DECISION_PATH_TO_MC01_CLOSURE = DOES_NOT_EXIST** as a demonstrated executable witness from these inputs, including the requested post-decision mapping stage. This does not prove eventual closure impossible. Completing R/A option specifications and deterministic mappings may permit a later witness without additional facts or decisions.

## Next step and checks

Present AD-K alone for review. Independently make AD-A and AD-R precise enough to evaluate: typed scope/authority correspondence, output schemas, allowed native outcome routes, and guarded transition mappings. Preserve separate records and the eventual AD-A → AD-R review order; validate their interaction jointly. Then complete the existing-authority mapping work and independent profiles. This review neither executes that work nor broadens MC01 into implementation.

Checks performed: 819-cell/63-action inventory, 186 unresolved-cell coverage, eight combinations, eight role records, existence of the listed JSON selectors, and 126 conditional AD-K evaluations (two options × 63 sources). The latter verify omission/explicit-empty/preserve-and-join behavior only, not O01 qualification. All historical input files and all 10,911 frozen E1 paths/content hashes remain unchanged. `git diff --check` passes.

```text
CANDIDATE_DECISIONS = 3
DECISION_READINESS = {AD-R: CONTRACT_BLOCKED, AD-A: CONTRACT_BLOCKED,
 AD-K: DECISION_READY}
ROLE_FAMILIES = 8
DECISION_DERIVED_ROLES = []
DETERMINISTIC_MAPPING_ROLES = [B01,B02,B03,B04,B05,B06,B07,B08]
ADDITIONAL_DECISION_ROLES = []
FACT_BLOCKED_ROLES = []
DECISION_COMBINATIONS = 8
COMBINATIONS_WITH_MC01_CLOSURE_PATH = []
DECISION_PATH_TO_MC01_CLOSURE = DOES_NOT_EXIST
NON_DECISION_BLOCKERS = [four explicit joins, independent expected profiles,
 B01-B08 native conversions/reached inventory, native type/route qualification]
ARCHITECT_REVIEW_READY = YES (AD-K only)
READY_DECISIONS = [AD-K]
NEXT_CONTROL_STEP = MIXED
MC01 = BLOCKED
MC02_READY = NO
M02_READY = NO
IMPLEMENTATION_MODIFIED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
```
