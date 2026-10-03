# Action-definition source model review 1

The 56 groups do not establish a need for 56 constructors. All 63 action definitions reside in one resolution-plan collection and share a recoverable definition core. Recommend **E. HYBRID**: a generic plan-backed Action constructor with independently governed typed rule bindings and explicit source joins. Use graph relations where they actually exist; the frozen knowledge graph cannot supply these Action definitions by itself.

This is a source-model recommendation, not a completed admission contract. Common-core coverage is **63/63**; complete source-to-O01 construction under currently defined rules is **0/63**. BR-C2 retry remains disallowed. No templates, implementation, operational registry, tests, or historical artifacts were changed.

The [machine-readable review](DETERMINISTIC_PLANNER_V0_1_ACTION_DEFINITION_SOURCE_MODEL_REVIEW_1.json) contains all 63 ActionIds, 630 field-origin cells, exact source selectors, constructor coverage, graph coverage, outstanding requirements, and SHA-256 input pins. Origin describes where authoritative information is found; it does not imply that prose has already been converted into a typed executable rule.

## Evidence and field availability

Primary evidence is the frozen [resolution plan](../experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_PLAN_1.json), `/resolution_actions`; the [typed graph](../experiments/E1/E1_TEMPLATE1_TYPED_KNOWLEDGE_GRAPH_1.json); and the [resume manifest](../experiments/E1/E1_RESUME_MANIFEST_1.json). The prior [projection analysis](DETERMINISTIC_PLANNER_V0_1_BR_C2_PROJECTION_CONTRACT_CLOSURE_1.md) and its six companions remain historical evidence. Their hashes are recorded in the companion.

| Semantic field | Origin across 63 actions | Availability limit |
|---|---|---|
| ActionId | DIRECT_IN_ACTION_SOURCE: 63 | Exact `id`; retain ActionId domain |
| Operation class | DIRECT_IN_ACTION_SOURCE: 63 | Exact `primary_operation_class`; not selection priority or executor |
| Prerequisites | DIRECT_IN_ACTION_SOURCE: 63 | Action/external lists exist; knowledge-member absence still needs normalization semantics |
| Produced result/knowledge types | REQUIRES_CROSS_SOURCE_JOIN: 3; MISSING_AUTHORITATIVE_SOURCE: 60 | Three bounded result oracles exist; no complete real-source O01 output binding for any route |
| Authority requirements | DIRECT_IN_ACTION_SOURCE: 63 | `authority_rule`, predecessors and effect boundary govern requirements; normalized typed predicates remain undefined |
| Evidence requirements | DIRECT_IN_ACTION_SOURCE: 63 | Evidence references and acceptance criteria exist; located evidence is not positive applicability proof |
| Effect class | DIRECT_IN_ACTION_SOURCE: 63 | `effect_boundary` |
| Scope | DIRECT_IN_ACTION_SOURCE: 63 | `scope`; definition scope must not silently become runtime authority scope |
| Lineage | REQUIRES_CROSS_SOURCE_JOIN: 63 | Plan/manifest provenance and subject lineage available; per-action target binding semantics remain undefined |
| Acceptance criteria | DIRECT_IN_ACTION_SOURCE: 63 | Governing criteria available as text; not necessarily an executable acceptance predicate |

The “missing source” count for result types means missing authoritative **typed output binding**, not that all governing intent or all future outputs must be obtained externally. Every action has acceptance criteria. Existing bounded result oracles cover S-BINDING, S-CONTEXT and PREP-VALIDATOR; they do not by themselves complete each actual-source Action admission profile. Twenty-three records have an execution result, which must not be used to infer the definition’s complete output contract.

Executor and stage role are direct for all63. Source provenance can be derived from the authenticated plan identity plus exact selector using BR-C1 rules; operational acceptance and target-envelope binding remain separate requirements. The matrix preserves the source values rather than substituting proposed defaults.

## Existing Action model and alternate representations

The plan is an explicit common action-definition record model, although not a complete canonical O01 interchange model. All63 records contain identity, operation, executor, effect boundary, stage, scope, action prerequisites, external prerequisites, authority rule, acceptance criteria and evidence.

Its direct prerequisite lists and `/compiled_action_dependencies` describe exactly the same **116 edges**, with no dangling ActionIds. These are two representations of one action dependency relation. Work-package/decision-package membership, actionability and selection inputs are views or overlays on definitions; an execution result is a different domain object. None should replace authoritative definition fields merely because it contains the same ActionId.

The selection policy consumes operation class and stage role to assign priorities. It does not define result types or grants. The frozen plan's `/selection_policy/criterion_1/current_reason` explicitly records that the graph has no resolution-action entities or formal PASS transitions. Plan reachability is therefore not graph-proven downstream eligibility.

Existing O01 does define a target shape. The `actions` predicate in the [CE-01 executable contract](DETERMINISTIC_PLANNER_V0_1_CE01_CONTRACT_RECONCILIATION_1.json), `/reference/program`, expects:

`id, primary_operation_class, executor, effect_boundary, stage_role, scope, lineage, prerequisite_actions, external_prerequisites, knowledge_requirements, authority_requirements, result_contract, provenance`.

It compares normalized source definitions with trusted profile definitions, checks typed ActionId prerequisites and current supporting sources. The earlier BASE/RENAMED profiles instantiate only three synthetic actions each. Thus the missing layer is authoritative normalization and rule binding for the real63, not discovery of63 unrelated schemas or permission to copy expected profiles into source projections.

## Semantic classes and constructor hypotheses

There is **one supported common construction schema**, with the following nine operation data variants. This does not prove that all missing admission semantics are already specified.

| Existing operation class | Actions |
|---|---:|
| DETERMINISTIC_MAPPING | 26 |
| SEMANTIC_RESOLUTION | 11 |
| SOURCE_ACQUISITION | 8 |
| ARCHITECT_AUTHORITY | 5 |
| ARCHITECT_CONTRACT_DECISION | 5 |
| IMPLEMENTATION_REPAIR | 3 |
| DETERMINISTIC_CONSTRUCTION | 2 |
| DECISION_INPUT_ACQUISITION | 2 |
| VALIDATOR_IMPLEMENTATION | 1 |

All concrete memberships are in the companion. Different operation values warrant distinct output/authority rules where governed; they do not alone require different construction algorithms. No EXTERNAL_RECEIPT operation occurs among these63. REEVAL actions remain DETERMINISTIC_MAPPING; FACT-BUDGET-APPLICABILITY remains SOURCE_ACQUISITION with FACT_ACQUISITION stage.

Prerequisite representation has three real variants:

- 56 records omit `knowledge_requirements`.
- DEC-BUDGET, REEVAL-BUDGET, DEC-IMPLEMENTATION and REEVAL-IMPLEMENTATION explicitly contain empty lists.
- INPUT-BUDGET, INPUT-IMPLEMENTATION and FACT-BUDGET-APPLICABILITY require accepted non-PASS knowledge. The first two consume AUTHORITY_REQUIRED findings; the third consumes REEVAL-BUDGET's BLOCKED missing-proof knowledge.

Omitted and explicitly empty members must not be equated without a governing rule. Accepted current knowledge from a BLOCKED producer must not require invented producer completion.

A proposed `CONSTRUCT_ACTION_DEFINITION(action_identity, typed_graph, authoritative_sources)` can locate every action and assemble its common core from the plan. It cannot currently emit a fully admitted O01 Action for any of the63 without resolving the outstanding bindings below. The graph may corroborate mapped targets and evidence; it cannot manufacture missing output or authority rules.

The minimum justified proposed family is **PLAN_BACKED_ACTION_DEFINITION_WITH_TYPED_RULE_BINDINGS**, covering63 common cores and0 complete existing-contract admissions. A final minimum number of complete constructors is not proven while normalization rules are missing. Splitting immediately into nine operation constructors or56 text-signature constructors would be premature. Permit a split only when a governed field requires a different construction rule, not a different value.

## Graph assembly assessment

The frozen graph has343 entities and962 assertions. It has no resolution ACTION entity type, and no entity matches any of the63 ActionIds exactly or as a colon-delimited terminal identifier.

| Requested Action relation | Existing graph representation | Action-definition coverage |
|---|---|---|
| REQUIRES | 185 assertions | No action-origin relation; use plan's116 dependency edges |
| PRODUCES | Absent; PRODUCED_BY exists9 times | No authorized inverse mapping to Action output contracts |
| AUTHORIZED_BY | 6 assertions | Does not bind the63 Action definitions |
| EVIDENCED_BY | 444 assertions | Graph evidence, not an Action requirement normalization rule |
| HAS_OPERATION_CLASS | Absent | Plan supplies operation values |
| HAS_SCOPE | Absent | Plan supplies definition scope |

Other relations include HAS_IDENTITY_TYPE, HAS_SLOT, DERIVED_FROM, VALIDATED_BY, APPLIES_TO and BINDS. Their existence does not establish missing Action endpoints. **Graph-only assembly coverage is0/63.** A future graph normalization could materialize plan actions, but requiring new graph relations before constructing these definitions is unnecessary and would invert the authoritative dependency: the plan already supplies the definitions. No frozen graph amendment is proposed.

## Remaining authoritative information

| ID | Missing or incomplete item | Classification and consequence |
|---|---|---|
| M1 | Actual-source canonical O01 field/rule-reference semantics | MISSING_REQUIRES_CONTRACT; target shape exists, real-source normalization does not |
| M2 | Produced result/knowledge types and acceptance-rule bindings | MISSING_REQUIRES_CONTRACT; bind each Action to governed output types, including the three bounded result profiles |
| M3 | Typed authority/evidence requirement normalization | MISSING_REQUIRES_CONTRACT; distinguish governance text, requirement reference, issued grant and satisfied gate |
| M4 | Knowledge prerequisite typing and absent-member semantics | MISSING_REQUIRES_CONTRACT; preserve56/4/3 variants and accepted non-PASS knowledge |
| M5 | Definition lineage versus subject lineage, accepted provenance/profile binding | MISSING_REQUIRES_CONTRACT; do not copy runtime lineage into every definition by default |
| M6 | Positive evidence at eight external reentry boundaries | MISSING_REQUIRES_EXTERNAL_SOURCE; not required to construct definitions or preserve waiting state |
| M7 | Tagged action prerequisite references and provenance selectors | MISSING_BUT_DERIVABLE; exact identities and BR-C1 pin rules exist;116-edge correspondence checked |
| M8 | New graph Action entities/relations as mandatory construction inputs | NOT_REQUIRED; optional later representation, not a missing authoritative source |

M1–M5 stop full construction, but do not justify inventing evidence. Static definitions can describe unsatisfied requirements. READINESS_PLAN scope, manifest source/target phases, subject lineage and definition provenance must retain distinct meanings. Report existence, historical PASS, authority reference and source-location validation cannot become current proof by normalization.

## Why the previous analysis produced56 groups

The prior class registry grouped a signature containing literal operation, executor, stage, effect, scope, authority-rule text, acceptance-criterion text, completion exclusions, knowledge shape, and prerequisite-presence flags. Only repeated signatures merged: the runtime-head/supervisor/audit PREP, DEC and MAP triplets, and DEC-BUDGET/DEC-IMPLEMENTATION. The remaining52 singleton signatures plus4 shared groups yielded56.

That is a conservative equality partition of recorded values. It is not a proof of56 construction semantics. Different acceptance criteria or prerequisite identities can be arguments or governed rule references within one constructor. All63 come from the same resolution-plan schema; filename and source-layout diversity do not explain this result.

Cause: **COMBINATION**, principally OVER_CONSERVATIVE_LLM_GROUPING, with incomplete action-schema normalization and absent graph Action normalization. There is genuine operation/rule diversity, but no evidence that it requires56 constructors. SOURCE_SHAPE_FRAGMENTATION is not the primary demonstrated cause; INSUFFICIENT_GRAPH_NORMALIZATION explains why a graph-only alternative presently fails, not why56 is a minimum.

## BR-C2 consequence

Replace the proposed56-template obligation with the following bounded contract-definition requirement, subject to governing plan acceptance:

1. Define one actual-source ActionDefinition normalization schema using the common plan record. Preserve O01 admission and BR-C1 identity/provenance rules.
2. Define typed rule bindings for M1–M5. Identify every field's direct selector, existing derivation or authorized join. Reject unresolved fields; never fill them from implementation defaults, historical outcomes or synthetic expected outputs.
3. Retain all63 concrete ActionId/source bindings and per-route coverage. A shared constructor does not waive any route's positive, negative, stale-source or reload checks.
4. Separate construction of a candidate definition from O01 admission, runtime actionability and effect authority. Source projection supplies data; an independent oracle admits it.
5. Preserve the three report-to-result projection contracts as separate work. BR-C2 must expose definitions, result identities, accepted knowledge and source pins distinctly to BR-C3 history reconciliation.
6. Leave O10 graph projection with BR-C4 and composed operational admission with the later owning package. The recommendation does not pull either into BR-C2.

This specifies the replacement work boundary, not the missing executable rules themselves. Stop attempting to infer M1–M5 through further source-specific fragmentation. BR-C2 may retry only after those rules and all63 bindings are independently complete, its three result routes are complete, and corrected package preflight is clean.

## Report

```text
ACTION_ROUTES = 63
PRIOR_PROJECTION_GROUPS = 56
FIELD_AVAILABILITY = companion.field_availability / field_matrix (630 cells)
SEMANTIC_ACTION_CLASSES = 1 supported common construction schema; 9 operation data variants
GENERIC_CONSTRUCTOR_COVERAGE = 0/63 complete under existing rules; 63/63 common core
CONSTRUCTOR_FAMILIES = [PLAN_BACKED_ACTION_DEFINITION_WITH_TYPED_RULE_BINDINGS]
GRAPH_ASSEMBLY_COVERAGE = 0/63
MISSING_AUTHORITATIVE_FIELDS = [M1, M2, M3, M4, M5]; M6 external reentry boundary; M7 derivable
PRIOR_GROUPING_CAUSE = COMBINATION
RECOMMENDED_SOURCE_MODEL = E. HYBRID
BR_C2_PROJECTION_REQUIREMENT_RECONCILIATION = shared normalization/rule-binding contract plus63 concrete bindings; not56 templates
BR_C2_RETRY_ALLOWED = NO
RESTORED_AND_QUALIFIED = 2/17
C06A_3_RETRY_ALLOWED = NO
C07_RETRY_ALLOWED = NO
F03_STATUS = CLOSED
V0_1_CURRENT_STATUS = CORRECTION_REQUIRED
IMPLEMENTATION_MODIFIED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
```

Validation:63 unique rows and630 field cells;1,144 JSON-pointer references resolved;42 input hashes checked. All11,236 pre-existing files in the protected comparison inventory were unchanged, including all10,911 frozen E1 files. Only this report and its JSON companion were added. Relative links, new-file whitespace and `git diff --check` passed. No planner tests or BR-C2 execution were performed for this analysis-only review.
