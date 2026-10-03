# C06A-2 — independent mapping and non-budget result oracles

**RESULT = PARTIAL. C06A_3_READY = NO.** Fifteen field-mapping contracts and three bounded positive-result specifications are recorded. The remaining operational rule compilation is explicitly incomplete; lossless source extraction is not being represented as a complete planner oracle. No restoration package was executed and no coverage element became RESTORED_AND_QUALIFIED.

## Package verification

The authoritative [remaining-contract matrix](DETERMINISTIC_PLANNER_V0_1_C06A_REMAINING_CONTRACT_1.json), `closure_packages[id=C06A-2]`, assigns specification work only: the finite source-field inventory, independent non-budget per-outcome schemas, supported decision-dossier probe, and positive/negative acceptance rules. Its elements are O01–O12 and O15–O17. Its prerequisite is the accepted reconciliation and RETRY_1 scope. It explicitly assigns **IMPLEMENTATION = NONE** and requires an exact remaining acceptance gap to stop dependent implementation. The package definition itself is sufficiently clear; this is not C06A_2_CONTRACT_INCOMPLETE.

Governing sources remain [reconciliation](DETERMINISTIC_PLANNER_V0_1_C06_C07_RECONCILIATION_1.md), [partial budget retry](DETERMINISTIC_PLANNER_V0_1_C06A_RETRY_1_RESULT.md), [retry coverage](DETERMINISTIC_PLANNER_V0_1_C06A_RETRY_1_COVERAGE.json), [backlog](../backlog/DETERMINISTIC_REASONING_PLANNING_RUNTIME.md), and [traceability](../backlog/DETERMINISTIC_REASONING_PLANNING_RUNTIME_E1_TRACEABILITY.md). The existing [budget oracle](DETERMINISTIC_PLANNER_V0_1_BUDGET_PROOF_MATRIX_ORACLE_1.json) and selection-policy qualification are preserved.

Expected complete package output is a reviewed field map **plus** independent operational acceptance rules and fixtures, not simply an exported copy of the frozen records. This attempt supplies the former at field-family level and the following explicitly bounded result profiles; the unresolved difference is listed below.

## Artifacts and independent basis

- [Mapping and coverage specification](DETERMINISTIC_PLANNER_V0_1_C06A_2_MAPPING_1.json): 15 mapping definitions and 2,910 exact pinned selector entries. Each entry retains document identity, exact pointer, record ID, selected-value hash and owning O-element. Each mapping defines source type/domain/selector, target type/domain, transformation, canonicalization, provenance/currentness and acceptance/rejection rules. Object-level entries include all nested fields; a nested object hash is evidence of retention, not a claim that its rules are operationally compiled.
- [Result-oracle specification](DETERMINISTIC_PLANNER_V0_1_C06A_2_ORACLES_1.json): three independent bounded result profiles, fixed parameter/source identities, closed typed input shapes, declarative acceptance expressions, and two proposed importer counterexample probes.
- [Synthetic specification fixtures](DETERMINISTIC_PLANNER_V0_1_C06A_2_FIXTURES_1.json): three positive inputs and 48 single-dimension negative mutations. These are documentation artifacts, not additions to the repository qualification test suite.

No planner module was imported and no implementation output was used as expected truth. Constants were extracted from the action criteria and accepted source/result contracts. The expression vocabulary is `all`, strict typed canonical `eq`, and `keys_exact`; unknown opcodes, missing pointers or wrong types return FALSE. Equality distinguishes JSON booleans, integers, strings and null. A future evaluator must reject duplicate keys before evaluation. The parameter registry is an independently pinned test input; accepting a caller-selected replacement parameter pin is forbidden.

The synthetic source bodies model **already admitted bounded source statements** for these profiles. Their hashes prove fixture integrity, not producer competence or real E1 applicability. Thus these profiles qualify transcription/admission of accepted inventory or preparation knowledge; they do not qualify independently establishing all the underlying source facts. Positive inputs are never evidence for frozen E1.

## Defined non-budget result profiles

### OR-BINDING — recorded-input inventory PASS

Source: [S-BINDING result](../experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_S_BINDING_1_RESULT.md), “Identified inputs” and “Explicit missing inputs and producer requirements”; plan action `S-BINDING/acceptance_criteria`.

Required typed inputs include the exact registered action/profile/source identity, pinned source-bound provenance, recorded subject, inventory payload, prerequisite scope and independent transition dimensions. The source criterion has no action/external prerequisites. The source registry and parameter profile must be valid and current for the qualification snapshot.

The positive payload names invocation, dispatch, release, context and OperationalBinding; distinguishes checked invocation/dispatch body identities from declared references; and retains all seven gap categories: canonical binding, binding digest, session, turn, dispatch authority projection, release/context consumer projection and construction scope. PASS requires the entire bounded inventory and its limitations, not complete domain inputs.

A passing result leaves roots/slots unchanged, issues no authority and constructs nothing. Missing or stale source, wrong identity domain/envelope, missing provenance, wrong mapping, incomplete inventory or promoted root/slot transitions rejects. This is a concrete positive acquisition contract; it does not require an empty PASS to succeed.

### OR-CONTEXT — per-field inventory PASS

Source: [S-CONTEXT result](../experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_S_CONTEXT_1_RESULT.md), “Accepted inventory knowledge”; plan action `S-CONTEXT/acceptance_criteria`.

The payload separately retains context-binding summary versus hydration, incomplete projection, PRE_EXECUTION_STRUCTURE_ONLY acceptance with NOT_YET_PRODUCED obligations, and unconstructed execution-profile inputs. Context and acceptance identities/references are observations, not proofs of completed acceptance or consumer compatibility. Context and acceptance scopes are explicitly separate; the oracle does not introduce equality between them.

Acceptance requires the exact bounded per-field inventory, source binding and unchanged root/slot dimensions. Converting a verified acceptance-manifest reference into completed acceptance, losing a limitation, or substituting source/currentness fails the contract.

### OR-PREP-VALIDATOR — unissued preparation dossier PASS

Source: [PREP-VALIDATOR result](../experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_PREP_VALIDATOR_1_RESULT.md), “Proposed DEC-VALIDATOR dossier,” “Required future qualification” and “Exclusions.”

The positive dossier names the three active consumer/construction boundaries and proposed pure API; the seven shared-helper check groups; six qualification-test groups; deferred CONTRACT-T1 body/schema policy; separately required actual grant and CONTRACT-T1; and effect/authority exclusions. It remains UNISSUED. It is not authority to implement the validator.

This acceptance oracle answers whether the **preparation result** is complete under its bounded contract. It deliberately does **not** answer whether an independently attested DEC-VALIDATOR decision is ready, approved or issued. Missing checklist facts cannot be supplied by this preparation PASS. The separate decision/authority oracle remains in GAP-01.

## Negative fixtures and invalidation

For each profile, 16 mutations reject: missing source, wrong source, stale source, wrong identity domain, wrong scope, wrong lineage, wrong mapping method, substituted release-identity domain, missing provenance, dangling source reference, conflicting runtime envelope, incomplete result, root promotion, slot promotion, unregistered parameter pin, and authority issuance. These cover the registered synthetic profile boundaries; they are not a claim that every future arbitrary dossier must share the same global envelope.

The contract requires:

```text
historical accepted result retained unchanged
AND required support invalidated
=> operational result usability = FALSE
```

Source identity/domain, selector, mapping version, accepted scope, payload and invalidation state must survive canonical persistence. Reload must not revalidate stale knowledge merely because raw bytes still exist. Current accepted knowledge from a historical BLOCKED producer remains usable where its required type/outcome/source binding is valid; producer completion is not added as a requirement. No new revalidation or authority transition is introduced.

## Independent mapping contract and cross-contract composition

`MAP-O01` through `MAP-O12`, `MAP-O15`, `MAP-O16`, `MAP-O17` name target **contract concepts**, not new Python classes or a parallel state model. Later implementation must reuse existing compatible types. Exact source fields are joined by typed record ID; ordinal pointers are provenance only. Raw artifact CONTENT_IDENTITY, AUTHORITY_IDENTITY, INSTANCE_IDENTITY, RELEASE_IDENTITY, CANONICAL_OBJECT_IDENTITY, WORKAUTHORIZATION_ID and BINDING_DIGEST remain distinct.

Canonicalization preserves ordered histories and argv, while declared sets are unique and sorted by tagged identity. It rejects coercion and unexpected required schema fields. Each source's own canonical identity/exclusion rule takes precedence over the contract-container encoding; no generic “strip identity fields” operation is permitted.

Cross-contract constraints are recorded in the mapping JSON:

- Binding references must correspond to the same recorded invocation/dispatch/release/context and the source-required scope/runtime/G4 references. Matching a hash in another identity domain is insufficient.
- Context-to-acceptance reference equality and runtime/G4 correspondence do not create scope equality or completed acceptance.
- Released profile content, ReleasedProfileAuthority and ProgrammerProfile remain separate. Only source-required profile correspondence may be imposed.
- A recorded lineage is not proof of temporal or EXECUTION-to-REQUEST applicability. Keep the governing rule and the subject fact separate.
- Pure validator preparation has a bounded code/qualification scope, not a universal runtime/G4/profile matching requirement. The synthetic fixture envelope prevents fixture mixing; it does not enlarge the actual governing preconditions.

All action field names currently present are explicitly assigned to an O-element. Graph entities/assertions, root records, historical attempts, eight handoff items and request routes, and remaining top-level contract sections are inventoried. The inventory's `REQUIRES_RULE_COMPILATION` label is intentional: preserved prose or bytes have not become an executable operational predicate by being hashed.

## Exact remaining acceptance gaps

These are incomplete independent specifications, not new E1 facts to acquire and not a claim that all their rules are absent from the governing artifacts. They prevent a full C06A-2 PASS; they must not be hidden by the three successful bounded profiles.

| Gap | Affected elements | Missing executable contract | Minimum remaining specification work |
|---|---|---|---|
| GAP-01 | O03, O04, O05, O11 | Decision/authority rule registry for exact dossier, independently established readiness checks, admitted choice, target/permission/exclusion and historical grant state | Compile the existing four issued records and source-backed dossier gates into separate typed acceptance expressions and positive/negative fixtures. Preparation acceptance cannot stand in for decision readiness or grant admission. |
| GAP-02 | O08, O09, O10, O15 | Per-root/per-slot proof-member and accepted-ancestor registry, including baseline proof scope and operational versus proposed relationship projection | Compile supported baseline proof schemas and absent future-proof states. `ACCEPTED_COMPLETE_PROOF` is a required outcome label, not by itself an executable certificate schema. Preserve the two baseline slots' limited resolution scopes and accepted validator-authority evidence. |
| GAP-03 | O06, O07, O12, O15, O16, O17 | Full historical/current overlay, receipt/reentry and required-goal correspondence oracle | Compile original hold precedence and all eight no-evidence route states. Define supported synthetic route positives only from admitted receipt rules, and independently derive control/coverage rather than using reported MIXED_WAIT as a predicate. |

The exact source documents/selectors and next specification operation for each gap are in the machine-readable `gaps` array. Missing actual ancestry, approval, budget applicability or other external bundles remain intentionally absent. **Their acquisition is not a prerequisite for this specification task or for qualifying the restored waiting state.** Unknown producer competence must remain an explicit unknown gate; no positive real receipt is fabricated to close the matrix.

The definitions above therefore do not authorize C06A-3. They also do not turn “full E1” into a demand for arbitrary future schemas, all historical payloads, or an E1 database.

## Counterexample probes for later implementation

The oracle JSON defines two probes, not executed here:

1. Independently admit OR-BINDING's complete inventory-with-gaps; import/reload the source-shaped action; apply its bounded result. It must be accepted with retained knowledge and no root/slot promotion. An omitted imported accepted inventory must not cause rejection of this independently valid output.
2. Independently admit OR-PREP-VALIDATOR's complete unissued dossier; import/reload and admit the preparation result. It must retain exact tests/exclusions/T1 prerequisites. It must not manufacture an independent decision-readiness attestation or issue a grant.

These are positive bounded contracts. Neither reuses the inadequate empty-PASS regression. `PRE_REPAIR_COUNTEREXAMPLE = NOT_EXECUTED_SPECIFICATION_ONLY`; no red/green implementation claim is made.

## Mechanical coverage and next-package gate

The companion `coverage` array covers exactly O01–O17, with restoration labels copied unchanged from the authoritative matrix. O13 and O14 remain the only restored-and-qualified scopes. O01/O02 field-mapping subsets are defined for later reuse; no whole remaining O-element is newly restored or fully qualified. O03/O05 have bounded result/dossier fixtures, not their complete operational oracle.

```text
C06A_3_READY =
    all assigned mapping definitions complete
    AND all required operational result/state oracles complete
    AND independent positive/negative fixture contracts complete
    AND no unresolved necessary rule compilation
```

The second, third and fourth terms are false for the full assigned package because GAP-01–GAP-03 remain. C06A-3 requires C06A-2 PASS; isolated field subsets do not bypass that prerequisite. Next work remains bounded C06A-2 specification closure, not implementation.

## Validation and report

Specification validation used an isolated temporary evaluator of the declared JSON expression language, with no planner imports: all three positive cases accepted; all48 declared negative mutations rejected; each positive survived three canonical JSON round trips. This validates the finite specification cases only. No existing test, implementation module, E1 file or historical qualification artifact was modified; no E1 importer, planner action or real-readiness operation ran.

```text
WORK_PACKAGE = C06A-2
RESULT = PARTIAL
CONTRACT_ELEMENTS_ADDRESSED = [O01, O02, O03, O04, O05, O06, O07, O08, O09, O10, O11, O12, O15, O16, O17]
MAPPINGS_DEFINED = [MAP-O01, MAP-O02, MAP-O03, MAP-O04, MAP-O05, MAP-O06, MAP-O07, MAP-O08, MAP-O09, MAP-O10, MAP-O11, MAP-O12, MAP-O15, MAP-O16, MAP-O17]
ORACLES_DEFINED = [OR-BINDING, OR-CONTEXT, OR-PREP-VALIDATOR]
POSITIVE_FIXTURES_DEFINED = [OR-BINDING-positive, OR-CONTEXT-positive, OR-PREP-VALIDATOR-positive]
NEGATIVE_FIXTURES_DEFINED = 48
CROSS_CONTRACT_CONSISTENCY = DEFINED_FOR_BOUNDED_PROFILES_AND_MAPPING_CONSTRAINTS
SOURCE_INVALIDATION_RULES = CURRENT_USABILITY_FAILS_CLOSED; HISTORICAL_RESULT_PRESERVED
ELEMENTS_READY_FOR_IMPLEMENTATION = [] (whole assigned elements; O01/O02 mapping subsets defined)
ELEMENTS_BLOCKED = [O03, O04, O05, O06, O07, O08, O09, O10, O11, O12, O15, O16, O17]
TOTAL_REQUIRED_CONTRACT_ELEMENTS = 17
RESTORED_AND_QUALIFIED = 2
REMAINING_COVERAGE = 15
C06A_3_READY = NO
NEXT_PACKAGE = C06A-2 remaining specification (GAP-01, GAP-02, GAP-03)
C07_RETRY_ALLOWED = NO
F03_STATUS = CLOSED
V0_1_CURRENT_STATUS = CORRECTION_REQUIRED
IMPLEMENTATION_MODIFIED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
```

Preservation validation passed: all2,910 inventoried selectors resolve and match their recorded selected-value hashes; source pins, JSON parsing,17-row coverage consistency, document links and whitespace checks passed. `git diff --check` passed. Byte comparison found no pre-existing file changed, including all10,911 frozen E1 files. Only the four C06A-2 specification/result artifacts were added.
