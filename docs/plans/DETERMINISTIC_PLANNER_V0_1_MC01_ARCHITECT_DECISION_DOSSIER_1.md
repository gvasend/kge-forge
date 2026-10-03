# MC01 Architect semantic decision dossier 1

**Decision input only. Three candidate governing decisions; no option selected and no authority issued. MC01 remains BLOCKED.** This dossier does not change O01, migration contracts, native registries or E1. Proposed rules below are alternatives for review, not recovered historical facts.

The [machine-readable dossier](DETERMINISTIC_PLANNER_V0_1_MC01_ARCHITECT_DECISION_DOSSIER_1.json) contains input SHA-256 pins, all 186 unresolved cells with ActionIds and source references, affected-action lists, six options, eight hypothetical combinations, role-family correspondence and the decision dependency DAG.

## Evidence and unresolved inventory

The [closure-2 review](DETERMINISTIC_PLANNER_V0_1_M01_MC01_CLOSURE_2.md) and all five companions are the inventory authority. Its source matrix evaluates 63 × 13 = 819 fields. There are 633 source-available cells and 186 unresolved cells. Source availability is not canonical admission: the independently reviewed complete expected profile is still missing.

| Unresolved field | Cells | Classification | Owner |
|---|---:|---|---|
| result_contract | 63 | GOVERNING_SEMANTIC_MISSING | AD-R |
| authority_requirements | 63 | AMBIGUOUS_EXISTING_RULE | AD-A |
| omitted knowledge_requirements | 56 | GOVERNING_SEMANTIC_MISSING | AD-K |
| explicitly declared knowledge requirements | 3 | MAPPING_MISSING | Definition/claim/type join |
| nonempty external prerequisites | 1 | MAPPING_MISSING | External identity/routing join |

No new FACT_MISSING item is established by this inventory. This does not mean the eight positive external-evidence absences have been resolved. Those absences remain intentional frozen state.

The three knowledge joins concern INPUT-BUDGET, INPUT-IMPLEMENTATION and FACT-BUDGET-APPLICABILITY. Their definitions already identify accepted producer/outcome/report requirements. The missing work is exact claim/KnowledgeId/type/source correspondence. S-ELIGIBILITY's declared EXT-CURRENT-ELIGIBILITY-EVIDENCE needs the external prerequisite crosswalk. Neither issue asks an Architect to decide what historically happened.

All 13 O01 fields remain required. Twelve are definition-time semantics; provenance also has admission-time validity. Prospective results are types/allowed outcomes, not instantiated historical results. No option establishes executed, completed, actual PASS, result existence, produced knowledge, root satisfaction or slot resolution.

## Architect review package

Each decision governs a separate domain and should receive a separate authority record if issued. Counts describe unresolved matrix cells, not admitted Action candidates. Every option is scoped to a pinned legacy definition schema and fails closed on unknown values, missing mappings or incompatible native types.

### AD-R — prospective result declarations

**Question:** What may an Action class declare it produces on successful execution, and how should possible root/slot transitions appear in that declaration?

**Why required:** Acceptance criteria constrain outputs but do not establish the complete versioned finite `result_contract` registry. The source plan's S-ANCESTRY evidence-or-NOT_FOUND rule and S-BINDING bounded inventory rule illustrate this distinction. The existing synthetic O01 profiles are qualification examples, not authority for all 63 definitions.

**Affected:** 63 actions / 63 result_contract cells; all nine existing operation classes. Role components B01 and B06, with B05 proof-consumer consistency. Review after AD-A; validate both together.

Both options propose this class-level type table. These labels are proposed contract identifiers, not claims that native enums already contain them:

| Existing operation class | Proposed prospective output type |
|---|---|
| SOURCE_ACQUISITION | BOUNDED_SOURCE_INVENTORY |
| SEMANTIC_RESOLUTION | SEMANTIC_CONTRACT_FINDING |
| ARCHITECT_AUTHORITY | BOUNDED_AUTHORITY_RECORD |
| ARCHITECT_CONTRACT_DECISION | GOVERNING_DECISION_RECORD |
| DETERMINISTIC_MAPPING | TYPED_MAPPING_PROOF |
| DETERMINISTIC_CONSTRUCTION | CANONICAL_CONSTRUCTION_CANDIDATE |
| IMPLEMENTATION_REPAIR | IMPLEMENTATION_QUALIFICATION_RECORD |
| VALIDATOR_IMPLEMENTATION | VALIDATOR_QUALIFICATION_RECORD |
| DECISION_INPUT_ACQUISITION | DECISION_INPUT_DOSSIER |

Source acceptance criteria remain additional constraints. A type label cannot replace target-specific payload validation. Proposed outcomes are PASS/FAIL/BLOCKED, with AUTHORITY_REQUIRED/EXTERNAL_GATE_REQUIRED only for routes independently permitted by native bounded fact/decision semantics. Unknown route correspondence rejects; the native non-PASS knowledge restrictions remain in force.

- **R1 — independent transition evaluation.** Declare the class output and `root_transition=UNCHANGED`, `slot_transition=UNCHANGED` for Action-result admission. Independently accepted proofs may subsequently change conditions through existing native recomputation. Rationale: separate result admission from satisfaction. Precedent: **CONSISTENT_WITH_EXISTING_PATTERN**; the complete type table is a **NEW_ARCHITECTURAL_CHOICE**. Limitation: this cannot suppress independent proof reevaluation or erase an explicitly governed transition.
- **R2 — explicitly proof-guarded transition declarations.** Use the same output policy, but declare possible transitions against exact source-declared affected conditions/slots, guarded by their independent native proof predicates and valid dependencies. Missing proof-capability correspondence rejects. Rationale: make possible consequences visible in the definition. Support: **NEW_ARCHITECTURAL_CHOICE**, with the no-PASS-implies-satisfaction guard **DIRECTLY_SUPPORTED**. Limitation: an affected-target list is not proof that every listed target can be completed; native representation and exact capability mappings still need qualification.

Neither alternative changes O01's comparison/admission rule. An approved expected profile must encode the chosen representation independently. Neither alternative authorizes future execution or creates proof.

### AD-A — definition-time authority requirements

**Question:** Is accepted task scope sufficient for a non-effecting operation absent an explicit grant requirement, or must every such operation also require a separately admitted authority object?

**Why required:** The three plan authority literals preserve scope and prohibit invented grants, but do not supply a complete typed conditional requirement policy. They must not be converted into current authority by inference.

**Affected:** 63 actions / 63 authority_requirements cells; all nine operation classes. B01 and B05 consumption requirements. Mutually constraining with AD-R; independent of AD-K.

- **A1 — scope plus explicit requirements.** Non-effecting operations require accepted execution-task scope/envelope and every explicit source-declared authority requirement, without an additional authority object solely because of their operation class. Qualification and production effects require exact corresponding scope authorization and all declared grants. Architect-decision routes remain human review/recording routes. Rationale: distinguish task permission from authority objects. Support: **CONSISTENT_WITH_EXISTING_PATTERN**; its complete typed normalization is a **NEW_ARCHITECTURAL_CHOICE**. Risk: task scope must not become a generic substitute for a required grant.
- **A2 — explicit authority for every operation.** Retain A1's effectful requirements and additionally require an independently admitted scoped authority predicate for every non-effecting operation. Rationale: uniform explicit permission evidence. Support: **NEW_ARCHITECTURAL_CHOICE**. Risk: introduces a permission-source requirement not established for every frozen action. Declaring that requirement does not supply its authority or justify changing the frozen control outcome.

Both use existing native AuthorityClass values and exact authorized operation/grant correspondence; no digest-based or operation-name guess selects a class. Missing correspondence rejects. Authority requirement is not authority granted, existence is not applicability, and neither implies decision readiness.

### AD-K — omitted knowledge prerequisite declaration

**Question:** Does omission of knowledge_requirements in the pinned legacy action schema mean no independent knowledge prerequisite, or an incomplete definition?

**Why required:** Four explicitly empty declarations do not establish equivalence for 56 omissions. Three explicit nonempty declarations remain separate mapping work.

**Affected:** 56 actions / 56 knowledge_requirements cells; concrete operation-class lists are in the companion. B01; B06 remains an explicit-claim mapping obligation. No decision dependency.

- **K1 — closed-world optional member.** For this exact schema/version, omission normalizes to an empty independent knowledge-prerequisite map. Explicit declarations are preserved; action dependencies and authority/evidence gates are unchanged. Unknown schemas reject. Rationale: define optional-member semantics. Support: **NEW_ARCHITECTURAL_CHOICE**; explicit-empty examples support only the explicit-empty case. Risk: must be issued as a compatibility rule, not asserted as recovered historical intent.
- **K2 — explicit declaration required.** Omission rejects until an authoritative definition supplement supplies an explicit declaration. Rationale: preserve fail-closed interpretation. Support: **CONSISTENT_WITH_EXISTING_PATTERN**. Consequence: 56 fields remain unresolved; historical execution reports cannot supply the missing declarations.

A BLOCKED producer may still have independently accepted current knowledge. Neither option imposes producer completion as a substitute for knowledge admission.

## Control, selection and execution consequences

There is no missing effect-taxonomy decision: all 63 definitions already declare NON_EFFECTING (47), QUALIFICATION_EFFECT_ONLY (6), or PRODUCTION_EFFECT (10). New control-plane/runtime effect labels would be unrelated design. Existing effect declarations remain intact.

For all three domains, definitions alone create no eligibility. Requirement changes affect actionability only through native prerequisite/authority/evidence evaluation. Selection policy is unchanged; only independently eligible candidates participate. No option writes a control label or removes frozen holds. Receipt, validation, accepted reentry lineage, verified pins and named-action eligibility remain separate requirements. Actual future effects require independent execution authority. Proposed rules inconsistent with a source acceptance constraint must be rejected, not used to weaken it.

## Source-role questions versus mapping work

The [closure-2 role companion](DETERMINISTIC_PLANNER_V0_1_M01_MC01_CLOSURE_2_ROLES.json) already defines semantic role discrimination and exclusivity for all eight families. It reports zero concrete native families closed. This is not evidence for eight new governing decisions.

| Family | Existing role and source family | Target / consumer | Remaining non-decision work |
|---|---|---|---|
| B01 | Plan → ACTION_DEFINITION_SOURCE | ActionId / O01 | Issued definition rules, independent expected profile and exact field joins |
| B02 | Checkpoint/hold → LEDGER_SOURCE | ActionStatus/current_completion; O02/O06 | All-action current support reconciliation |
| B03 | Goal/prerequisite/slot declarations → ROUTING_SOURCE/GRAPH_SOURCE | ConditionId, SlotId, Goal, PredicateId; O10 | Typed identity/predicate/conditional-route crosswalk |
| B04 | Request/handoff → absence/gate/routing roles | GateId/EvidenceId/receipt/reentry | Native projection, composite implementation and DEC-EXEC routes |
| B05 | Accepted proof or issued grant claims | O08 authority/gate; O09 exact slot proof | Source-specific admitted parameterization |
| B06 | Accepted typed claims → ACCEPTED_KNOWLEDGE_SOURCE | KnowledgeId/type/source predicate | Producer/report/claim/type join |
| B07 | External acquisition contract/envelope | ExternalResolutionContract/content identity | Canonical body, derivation selectors, source pin and context |
| B08 | Checkpoint/inventory/policy roles | PersistenceBundle/FrozenControlProof | Integrated baseline/policy/certificate binding |

For every family, source identity, raw content identity and native typed target identity remain distinct. Exact recorded scope/lineage, source selectors, pins and currentness determine applicability. Shape alone cannot establish role. There is no permissive precedence: conflicting claims reject; multiple roles require independently supported claims and separate consumers/provenance. Selection is not execution/result, proof is not authority issuance, historical validity is not current applicability, and absence is not positive evidence.

B01 overlaps the three decisions, B05 overlaps authority requirements, and B06 overlaps prospective types and explicit knowledge correspondence. The role semantics themselves require no additional authority record. Resolving source mappings remains mandatory; classifying them as non-decisions does not close them.

## Hypothetical consequence simulation

The companion evaluates all six options individually and all eight R×A×K combinations against the immutable 819-cell inventory. No hypothetical Action value is written as authoritative state. Simulation measures governing-rule coverage, not semantic qualification of proposed candidates.

| Scenario | Governing cells potentially covered | Original cells remaining | Rows without an original cell gap | O01 admissions |
|---|---:|---:|---:|---:|
| R1 or R2 alone | 63 | 123 | 0 | 0 |
| A1 or A2 alone | 63 | 123 | 0 | 0 |
| K1 alone | 56 | 130 | 0 | 0 |
| K2 alone | 0 | 186 | 0 | 0 |
| Either R + either A + K1 (4 combinations) | 182 | 4 | 59 | 0 |
| Either R + either A + K2 (4 combinations) | 126 | 60 | 4 | 0 |

These are conditional upper bounds assuming issued complete rule annexes. The remaining four K1-case actions are INPUT-BUDGET, INPUT-IMPLEMENTATION, FACT-BUDGET-APPLICABILITY and S-ELIGIBILITY. Every combination still needs independent expected profiles and concrete B01–B08 mappings; zero role families become closed by this simulation. No established logical boundary conflict was found, but full native satisfiability is unproved. In particular, R2 requires proof-target compatibility and A2 adds authority-source obligations. No option is preferred because of its coverage count.

## Interaction, minimum set and post-decision work

The supported candidate set is **[AD-R, AD-A, AD-K]**. This is minimal at the level of the three distinct unresolved governing questions found in the inspected inventory, not a proof of global mathematical minimality. Combining them into one broad grant would conceal distinct semantics.

Review DAG: **AD-A → AD-R**, with AD-K independent. AD-A/AD-R are mutually constraining in substance; the directed edge defines review order, followed by joint consistency validation. AD-R/AD-K and AD-A/AD-K are independent policy questions; later explicit knowledge joins use the issued output types. Review in dependency-ordered batches: [AD-A, AD-K], then [AD-R], preserving separate authority records.

After separately authenticated decisions are issued, a later authorized package must:

1. Verify decision identity, selected option, version, exact scope, lineage and governing sources.
2. Materialize the typed semantic registry and deterministic selectors/joins; reject unknown or ambiguous values.
3. Recompute all 819 cells using the shared constructor and 29 literal bindings. Never use historical results as defaults for prospective definitions.
4. Produce 63 candidates and compare them with independently derived, pinned O01 expectations; constructor output cannot become its own oracle.
5. Recompute native source-role bindings and their exact admitted consumers.
6. Qualify invalidation/reload, cross-contract consistency and the complete MC01 gate before evaluating MC02 readiness.

No LLM preference belongs in this derivation. Missing source/type correspondence remains an explicit failure requiring mapping work.

**DECISION_PATH_TO_MC01_CLOSURE = DOES_NOT_EXIST as an established decision-only path.** This is not a theorem that later derivation cannot succeed. Even the best conditional governing coverage leaves four explicit joins, DEF-EXPECTED-PROFILE, native representation qualification and eight concrete binding families. Consequently this dossier cannot demonstrate 63/63 O01 admission plus zero role ambiguities from option issuance alone. No new historical fact or external evidence is proposed to bridge those gaps.

## Report and preservation

```text
UNRESOLVED_CONCRETE_FIELDS = 186
UNRESOLVED_ROLE_FAMILIES = 8
FACT_GAPS = [] established in the definition inventory
MAPPING_GAPS = [three knowledge joins, S-ELIGIBILITY external join,
 DEF-EXPECTED-PROFILE, B01-B08 concrete native mappings]
GOVERNING_SEMANTIC_GAPS = [DEF-RESULT, DEF-AUTHORITY policy,
 DEF-KNOWLEDGE omission policy]
DECISION_DOMAINS = [AD-R, AD-A, AD-K]
DECISION_COUNT = 3
DECISION_DEPENDENCY_DAG = [AD-A -> AD-R]; AD-K independent
MINIMUM_DECISION_SET = [AD-R, AD-A, AD-K]
DECISION_PATH_TO_MC01_CLOSURE = DOES_NOT_EXIST
NON_DECISION_BLOCKERS = mapping gaps above plus native representation qualification
ARCHITECT_DECISION_REQUIRED = YES
SELECTED_OPTIONS = []
AUTHORITY_ISSUED = NO
MC01_RESULT = BLOCKED
MC02_READY = NO
M02_READY = NO
IMPLEMENTATION_MODIFIED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
```

Preservation validation compares all 10,911 frozen E1 paths/content hashes and the pre-existing implementation/planning/backlog baseline. Matrix counts, eight coverage combinations, input pins, JSON parsing and `git diff --check` are checked for this dossier. These checks do not qualify migration, O01 candidates or runtime restoration.
