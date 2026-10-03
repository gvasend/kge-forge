# Action definition normalization contract 1

**Result: PARTIAL.** This defines a common ActionIR structure, deterministic construction/projection rules, and29 exact literal bindings covering all63 plan records. It does **not** establish63 complete O01-admissible real-source definitions. The semantic bindings listed below remain required; all63 rows are classified MISSING_RULE_BINDING. No constructor, operational registry or planner implementation was changed.

The source-model recommendation remains HYBRID_PLAN_BACKED_CONSTRUCTOR. A shared constructor does not authorize translating arbitrary acceptance prose into new output types or treating synthetic qualification scope as real authority. BR-C2 retry remains disallowed, independently also because its three report/result contracts remain incomplete.

## Artifacts and authority

The following companions are specification artifacts, not installed runtime schemas or registries:

- [ActionIR field schema](DETERMINISTIC_PLANNER_V0_1_ACTION_DEFINITION_NORMALIZATION_CONTRACT_1_ACTION_IR_SCHEMA.json): exact field set, types, domains, cardinality, provenance and validation.
- [Typed rule registry](DETERMINISTIC_PLANNER_V0_1_ACTION_DEFINITION_NORMALIZATION_CONTRACT_1_TYPED_RULE_REGISTRY.json): finite literal domains,29 concrete bindings, semantic binding domains and pinned governing inputs.
- [63-action normalization table](DETERMINISTIC_PLANNER_V0_1_ACTION_DEFINITION_NORMALIZATION_CONTRACT_1_NORMALIZATION_TABLE.json): source selectors, bindings, missing inputs and unissued IR/profile identities.
- [Fixtures](DETERMINISTIC_PLANNER_V0_1_ACTION_DEFINITION_NORMALIZATION_CONTRACT_1_FIXTURES.json): source-core positives, negatives and existing independent O01 controls.
- [Validation results](DETERMINISTIC_PLANNER_V0_1_ACTION_DEFINITION_NORMALIZATION_CONTRACT_1_VALIDATION.json): actual checks separated from unexecuted complete-constructor obligations.

Governing inputs are the [source-model review](DETERMINISTIC_PLANNER_V0_1_ACTION_DEFINITION_SOURCE_MODEL_REVIEW_1.md), frozen [resolution plan](../experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_PLAN_1.json), [BR-C1 bindings](DETERMINISTIC_PLANNER_V0_1_BR_C1_CONTRACT.json), and unchanged O01 `actions` predicate in [CE-01](DETERMINISTIC_PLANNER_V0_1_CE01_CONTRACT_RECONCILIATION_1.json), `/reference/program`. The [prior result contracts](DETERMINISTIC_PLANNER_V0_1_BR_C2_PROJECTION_CONTRACT_CLOSURE_1_RESULT_CONTRACTS.json) remain authoritative for the three separate report routes.

## Canonical ActionIR

An emitted ActionIR contains exactly the14 O01 definition keys. Identity metadata wraps the IR; it is not an extra O01 field. Evidence and rule provenance are retained inside provenance, without pretending O01 separately evaluates those propositions.

| Field | Type/domain; cardinality | Governing normalization |
|---|---|---|
| id | ActionId string;1 | Exact unique plan action identity |
| primary_operation_class | Operation enum;1 | Exact plan literal; no prefix-based inference |
| executor | Executor enum;1 | Exact plan literal; not permission to invoke that executor |
| effect_boundary | Effect enum;1 | Exact plan literal; independent of authorization |
| stage_role | Stage enum;1 | Exact plan literal; not selection priority |
| scope | Bound Scope string;1 | Explicit definition-to-operational-scope binding |
| lineage | Bound Lineage string;1 | Explicit accepted context/source correspondence |
| prerequisite_actions | Typed ActionId references;0..N | Declared dependencies; no condition-satisfaction inference |
| external_prerequisites | Tagged requirement references;0..N | Exact external proposition, gate or independently bound requirement |
| knowledge_requirements | KnowledgeId → KnowledgeType;0..N | Accepted source/type binding; no producer-completion substitution |
| authority_requirements | AuthorityRequirementId references;0..N | Exact scoped requirement, not a grant or satisfied gate |
| result_contract | ResultDeclaration;1 | Possible results/knowledge and separately guarded proof transitions |
| provenance | Source pins/selectors/rules/context;1 | Definition scope, subject envelope and evidence retained separately |

The schema companion supplies the full field-by-field contract. Missing mandatory members, unknown members, duplicate keys, wrong types, unresolved references and invalid domain substitutions reject before emitting an IR. Empty collections require a governing empty interpretation; emptiness is not a fallback for unresolved normalization.

Canonical encoding is UTF-8 JSON with lexicographically sorted object keys, compact separators and preserved Unicode. Reject non-finite numbers, floats and duplicate keys. Sort only declared sets by typed identity; preserve genuinely ordered values. Duplicate set members reject rather than disappearing during sorting.

ActionIRIdentity is domain-separated content identity of `{schema: ACTION-IR-1, action: IR}`. A complete O01 candidate's identity covers its entire sorted definition set and provenance context, not one isolated action. Identity-domain equality requires both domain and digest. Hash equality cannot substitute ActionId, source content identity, authority identity or profile identity. Incomplete rows have null identities, not hashes of partial states mislabeled as usable definitions.

## Common construction and projection

`CONSTRUCT_ACTION_IR(plan_action, typed_rule_bindings, BR-C1 bindings, provenance)` has one contract for all63 actions:

1. Verify source bytes, schema, unique ActionId selector and BR-C1 binding. Reject stale, substituted or ambiguous supporting sources.
2. Resolve exactly one binding per required rule domain. Verify binding type/version, selector, current source support and correspondence to this action. No “closest” literal or filename lookup is permitted.
3. Copy the four enum fields through their exact literal rules. Resolve typed dependencies against the complete action inventory. Keep declared external/knowledge requirements distinct.
4. Resolve result, authority, evidence, knowledge, scope and lineage through independently governed bindings. Missing bindings produce a structured failure and **no ActionIR**.
5. Assemble provenance with every dependency, rule identity, original definition scope and accepted subject context. Preserve typed known absence; do not manufacture missing positive evidence.
6. Validate the exact14-field structure and cross-field correspondence, then canonicalize and issue the IR identity.

This describes a specification, not executable constructor code. The constructor must not query current process history, derive permissions from result records, silently choose a lineage, or generate its own acceptance oracle.

`PROJECT_ACTION_IR_TO_O01` copies the14 fields losslessly into the O01 normalized definition set, sorting definitions by ActionId. It reads no original artifact. Context and source authentication must already be captured and validated. O01 is a whole-profile predicate: it compares normalized source definitions with **independently bound expected definitions**, checks references and authenticates the plan source. A single IR cannot create the expected profile by copying itself and thereby prove admission. The current trusted real-source expected profile remains missing; unchanged BASE/RENAMED qualification controls are not substitutes.

## Typed rule domains

The registry defines six literal domains with29 exact values:

| Domain | Values/count | Meaning |
|---|---|---|
| OPERATION_LITERAL |9 existing operation classes | Preserve operation semantics; no outcome/authority inferred |
| EXECUTOR_LITERAL |4 | Architect, LLM semantic evaluation, deterministic runtime, implementation |
| EFFECT_LITERAL |3 | NON_EFFECTING, QUALIFICATION_EFFECT_ONLY, PRODUCTION_EFFECT |
| STAGE_LITERAL |7 | ACQUISITION, AUTHORITY_PREREQUISITE, DECISION_PREPARATION, DECISION_REENTRY, FACT_ACQUISITION, RESOLUTION, SPECIFICATION |
| DEFINITION_SCOPE_LITERAL |3 exact source strings | Preserve source scope; not automatically the O01 operational scope |
| GOVERNANCE_TEXT_LITERAL |3 exact source strings | Preserve governing limitations; not executable grant predicates |

The registry includes the full operation/scope/governance literals and concrete action memberships. Literal identities are domain/version/value hashes, so ordering cannot change them. Recognition of a governance string does not mean its authority requirements are fully normalized.

Semantic domains are ACTION_DEPENDENCY, ACCEPTED_KNOWLEDGE, EXTERNAL_REQUIREMENT, AUTHORITY_BINDING, EVIDENCE_BINDING, RESULT_BINDING, SCOPE_BINDING and LINEAGE_BINDING. Their values must be explicit independently accepted bindings with source selectors, domain/version, target fields and support pins. There is no wildcard “any authority,” “any evidence,” implicit empty binding, or interpretation callback. Unknown values fail closed.

### Prerequisites and accepted knowledge

Plan `prerequisite_actions` supplies116 exact dependencies. Normalize each as `{domain: ActionId, id: exact_id}` and validate the complete inventory. A dependency is not interchangeable with an eligibility gate, decision readiness, external evidence, authority or accepted knowledge. Keep these as separately tagged requirement references or source-bound knowledge entries.

Fifty-six source records omit `knowledge_requirements`; four explicitly declare an empty list; three declare accepted non-PASS knowledge. The four explicit empties can normalize directly to an empty knowledge map. The other59 require additional binding semantics: omission must have an authoritative schema interpretation, and declared knowledge needs exact KnowledgeId/KnowledgeType bindings. A name invented from the producer ActionId is not source-backed knowledge identity.

INPUT-BUDGET and INPUT-IMPLEMENTATION consume recorded AUTHORITY_REQUIRED findings. FACT-BUDGET-APPLICABILITY consumes REEVAL-BUDGET's accepted BLOCKED missing-proof outcome. Their usable knowledge depends on current accepted evidence, not producer COMPLETED. Conversely historical completion does not establish current proof. Existing typed prerequisite mechanisms must preserve these distinctions after reload.

### Results, knowledge and proof transitions

A ResultDeclaration enumerates governed possible outcomes and knowledge types; it does not contain an outcome that has already occurred. Root/slot declarations must be UNCHANGED or reference independently admitted proof guards. PASS alone never satisfies roots or resolves slots. A mapping action's potential proof output is not an unconditional transition.

Result bindings must cite acceptance criteria and an independently governed type contract. Operation class alone cannot determine these types: S-EXEC permits source discovery or a decision dossier; SEM actions may produce AUTHORITY_REQUIRED; DEC-EXEC permits a validated-source waiver rather than necessarily a new decision. Blanket PASS/BLOCKED or a single invented generic knowledge type would lose those contracts.

The bounded S-BINDING, S-CONTEXT and PREP-VALIDATOR result oracles provide useful constraints, but the prior report-to-result contract still records missing payload selectors, envelope parameterization and source normalization. No actual result schema is inferred from report existence or the23 historical execution-result fields.

### Authority, evidence and effect

Authority requirements identify the exact governing grant/decision requirement, scope, lineage, prerequisite bindings and exclusions. Evidence requirements identify the proposition, expected source/type and currentness rule. Governing evidence references in provenance remain distinct from unsatisfied external evidence requirements.

AUTHORITY_REQUIRED does not establish DECISION_READY. An authority object does not establish applicability. A requirement does not establish evidence satisfaction. Unknown/unbound rule values reject; empty authority requirements require an explicit supported interpretation, not merely NON_EFFECTING classification.

NON_EFFECTING, QUALIFICATION_EFFECT_ONLY and PRODUCTION_EFFECT are retained exactly. Operation and stage distinguish source inspection, fact acquisition, dossier acquisition and deterministic construction even when their effect classification matches. Admission never permits effects; qualification effects do not authorize production, and a definition's executor label does not initiate LLM or external work.

### Scope and lineage

Preserve original definition scope in provenance. Bind operational scope and lineage through an authenticated correspondence, not a neighboring action, directory name or synthetic profile. The frozen plan uses READINESS_PLAN and DECISION_INPUT_REENTRY_1 as well as an exact budget-envelope restriction; existing synthetic O01 definitions use a runtime request scope and QUALIFICATION lineage. Those synthetic values do not resolve the real-source mapping.

Required context members retain their identity domains, including graph/plan, runtime, G4, profile, invocation/binding, ledger and policy where the governing BR-C1/O01 context requires them. Missing operational objects may remain typed absence if allowed by that context. Static Action definitions do not require obtaining the eight absent positive-reentry evidence sources. Validating a waiting definition must not make its branch runnable.

## Source invalidation and determinism

IR support includes all source and rule-binding identities. Invalidating any required support invalidates current admission; retaining historical bytes does not restore validity. Persist those dependencies and validity inputs so cold revalidation produces the same rejection. Revalidation requires the defined accepted-source transition; reload cannot silently mark sources current.

Future constructor qualification must compare canonical IR and complete O01 candidate identities under source/rule/key ordering changes, repeated processes and cold reload. It must also compare admission, not just digests. Source pin changes are semantically changed inputs even when selected fields look identical. Qualification of those future constructor properties has not occurred in this task.

## Complete63-action evaluation and missing inputs

Every route is individually present in the normalization table. All63 have authoritative common-core fields and exact literal bindings. Each has MISSING_RULE_BINDING as its primary construction status; four can directly normalize an explicitly empty knowledge declaration, but none can emit a complete IR.

| Missing binding | Routes affected | Exact information still needed |
|---|---:|---|
| RESULT_BINDING |63 | Source-governed possible outcome/knowledge types and proof-transition guards; no complete source-to-profile instantiation |
| AUTHORITY_BINDING |63 | Normalize governing limitations and predecessors into exact outstanding typed requirements or independently justified empty requirements |
| EVIDENCE_BINDING |63 | Separate provenance evidence from required current propositions, with target identity/type and selectors |
| KNOWLEDGE_BINDING |59 |56 omission interpretations;3 exact accepted KnowledgeId/KnowledgeType/source joins |
| SCOPE_BINDING |63 | Definition-scope versus operational-scope correspondence |
| LINEAGE_BINDING |63 | Exact per-definition/subject lineage correspondence and accepted profile context |

These are semantic specification inputs, not63 bespoke projection templates. The six domains are defined, but their missing instance semantics are not disguised as approved opaque strings. No ambiguity is silently selected and no contract conflict is asserted merely because a binding is absent. The table records null identities and exact missing inputs for each ActionId.

To complete these bindings, the next contract work must establish a source-cited rule value for each distinct semantic output/requirement, an explicit omission rule for the legacy source schema, and accepted real-source scope/lineage/profile correspondences. That work must preserve existing O01 and the three non-PASS knowledge requirements. This report does not claim those choices were already authorized by the literal source values.

## Fixtures and validation limits

The63 source-shaped core fixtures cover every observed literal value and combination. They are qualification copies, never new E1 evidence. All63 pass core validation; nine mutations reject unknown operation, wrong rule type, missing/substituted ActionId, missing scope, invalid effect, malformed/dangling/wrong-domain prerequisite. These are **core validation**, not full constructor positives.

Eight further complete-contract negatives specify missing prerequisite/result bindings, invalid authority/evidence bindings, wrong lineage, incompatible envelope, ambiguity and stale source. They are explicitly unexecuted because there is no complete real-source positive base. No result is marked PASS merely because a fixture is missing.

The unchanged O01 BASE and RENAMED synthetic controls both accept. They establish that the admission authority was preserved, not real-source normalization completeness. Complete source-to-IR-to-O01 positives remain0. Key-reversal and canonical JSON reload equality passed for63 core records; route-order reversal passed. Cold constructor-process/IR identity qualification remains pending because no constructor was implemented.

## Graph and BR-C2 relationship

The plan/artifacts remain authoritative sources. The graph is a synchronized normalized knowledge representation. Current graph-only coverage remains0/63. After construction, a later graph projection may represent ActionId entities with separately typed dependency, accepted-knowledge, external gate, authority/evidence requirement, result declaration, operation, scope, lineage and provenance relations. Proposed relations must not silently reinterpret existing graph edge semantics. An output declaration is not a PRODUCED fact, and a requirement edge is not a satisfied gate.

No new graph Action layer is a precondition for normalizing the authoritative plan. O10 graph projection remains BR-C4-owned. BR-C2 can eventually replace63 source-specific action projections with one constructor, typed rule registry and63 instances, **only after** all missing bindings and independent O01 expected definitions are complete. This report defines that replacement boundary but does not claim the replacement acceptance gate passed or amend historical package scope.

The three report/result routes remain unchanged and non-executable: their prior companion reports `complete_projection_count = 0`. Therefore action normalization alone would not permit BR-C2 retry. BR-C3 history reconciliation and later composition remain separately owned.

## Report

```text
SOURCE_MODEL = HYBRID_PLAN_BACKED_CONSTRUCTOR
RESULT = PARTIAL
ACTION_IR = DEFINED (structure); complete real-source bindings INCOMPLETE
TYPED_RULE_DOMAINS = [OPERATION_LITERAL, EXECUTOR_LITERAL, EFFECT_LITERAL, STAGE_LITERAL,
  DEFINITION_SCOPE_LITERAL, GOVERNANCE_TEXT_LITERAL, ACTION_DEPENDENCY,
  ACCEPTED_KNOWLEDGE, EXTERNAL_REQUIREMENT, AUTHORITY_BINDING, EVIDENCE_BINDING,
  RESULT_BINDING, SCOPE_BINDING, LINEAGE_BINDING]
RULE_BINDINGS_DEFINED = 29 exact literal bindings; semantic instance bindings incomplete
ACTION_ROUTES_TOTAL = 63
CONSTRUCTIBLE = 0/63
MISSING_RULE_BINDINGS = [RESULT_BINDING, AUTHORITY_BINDING, EVIDENCE_BINDING,
  KNOWLEDGE_BINDING, SCOPE_BINDING, LINEAGE_BINDING]
MISSING_AUTHORITATIVE_FIELDS = [] common-core fields; missing target semantics recorded as rule bindings
AMBIGUOUS_RULES = [] no unresolved choice selected
CONTRACT_CONFLICTS = []
SEMANTIC_FIXTURES = 63 core positives PASS; 2 unchanged O01 controls PASS; 0 complete real-source positives
NEGATIVE_FIXTURES = 9 core negatives PASS; 8 complete-contract negatives specified, NOT_EXECUTED
DETERMINISM = core key-order/reload and route ordering PASS; complete constructor qualification pending
BR_C2_ACTION_REQUIREMENT_RECONCILED = NO (replacement boundary defined; acceptance incomplete)
RESULT_PROJECTION_CONTRACTS_EXECUTABLE = NO
BR_C2_RETRY_ALLOWED = NO
RESTORED_AND_QUALIFIED = 2/17
CE_02_CLOSED = NO
C06A_3_RETRY_ALLOWED = NO
C07_RETRY_ALLOWED = NO
IMPLEMENTATION_MODIFIED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
```
