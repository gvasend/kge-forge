# MC01 Action semantic model — Architect design 1

**Two coherent design candidates are presented; neither is selected or decision-ready as a complete executable model.** The common design is a typed Action definition plus claim-admission and snapshot-correspondence interfaces. An Action definition alone cannot govern execution-history truth, proof acceptance, external receipts or snapshot policy. Treating all eight role families as Action attributes would erase these boundaries.

The [machine-readable companion](DETERMINISTIC_PLANNER_V0_1_MC01_ACTION_SEMANTIC_MODEL_DOSSIER_1.json) maps all 13 fields, all 819 Action cells, all 186 unresolved cells, eight families, proposed derivation rules and both candidate consequences. It contains no selected model, issued authority, concrete hypothetical Action values or changes to existing contracts.

## Common model and native boundary

The [closure-2 field matrix](DETERMINISTIC_PLANNER_V0_1_M01_MC01_CLOSURE_2_SOURCE_MATRIX.json) remains the definition inventory. O01 requires complete prospective definitions and an independently trusted expected profile. The [native Action model](../../adapter/planner/model.py) separately validates typed references, evidence, accepted inventory, authority predicates and status coverage. A generic result-schema reference cannot be placed into native `accepted_inventory`, which contains KnowledgeRecords, or used to manufacture their acceptance.

Eight semantic dimensions cover the inspected interfaces:

| Axis | Question and allowed domain | O01 fields | Principal interaction |
|---|---|---|---|
| ID | Which exact typed ActionId is declared? | id | CTX/SUP prevent identity substitution |
| OP | Which existing operation, executor and stage? Existing nine plan operation classes and retained literal bindings | primary_operation_class, executor, stage_role | IN/OUT/AUTH/EFF constrain operation contracts |
| IN | Which typed prerequisites? Action-completion gate, condition gate, external requirement, accepted-knowledge requirement | prerequisite_actions, external_prerequisites, knowledge_requirements | OUT/SUP establish claim-type correspondence, not satisfaction |
| OUT | Which finite native outcomes and versioned output/claim schemas, with independently guarded target relationships? | result_contract | OP determines applicable contract; SUP governs actual proof |
| AUTH | Which exact native permission expression, including an explicitly justified no-additional-authority-object case? | authority_requirements | EFF/CTX distinguish permission, effect and applicability |
| EFF | Existing NON_EFFECTING, QUALIFICATION_EFFECT_ONLY, PRODUCTION_EFFECT | effect_boundary | AUTH must not be inferred from effect label |
| CTX | Which exact definition scope and typed subject lineage/envelope? | scope, lineage | ID/SUP preserve frozen/live and REQUEST/EXECUTION distinctions |
| SUP | Which authenticated claim does a source support for this consumer? | provenance | Applies to all other axes and runtime support interfaces |

SUP's design vocabulary distinguishes DEFINITION, SELECTION, EXECUTION_EVENT, ACCEPTED_KNOWLEDGE, PREPARATION, DOSSIER, ISSUED_GRANT, TARGET_PROOF, EXTERNAL_REQUEST, EXPECTED_ABSENCE, GRAPH_ASSERTION, POLICY, CHECKPOINT, INVENTORY and PROVENANCE_ONLY. These are proposed claim-kind tags, not additions to native enums. Their existing role counterparts remain unchanged.

Allowed OUT/AUTH domains are typed schema/predicate references, not arbitrary prose or callbacks. A closed registry must enumerate their legal references and interpretation. That registry is still missing; naming the domain does not fill it. Unknown values, ambiguous matches and unbound required references reject.

These axes are separate because identity, operation, requirement, output, permission, effect, context and support answer different questions. Eight is a supported decomposition, not a global mathematical minimum. Combining them into a single opaque “Action policy” would conceal rather than resolve dependencies.

## AD-K, AD-R and AD-A disposition

The three questions are **subdecisions of one Action-definition model**, not redundant policies:

- AD-K governs IN's legacy missing-member interpretation. It affects 56 knowledge cells and a B01 component; it does not resolve B06's three explicit claim joins.
- AD-R governs OUT's prospective contract. It affects 63 result cells, B01 and type relationships with B05/B06. A declared possible output is not an actual result.
- AD-A governs AUTH's permission expressions. It affects 63 authority cells, B01 and B05 consumption requirements. A requirement is not an issued grant.

OUT and AUTH interact through operation/effect constraints. AD-K's omission choice can be considered independently, but eventual full model validation is joint. Existing options remain historical input; none is selected or silently superseded. A later model authority could incorporate subordinate choices only by naming their exact resolved policies. AD-R/AD-A need more precise contract annexes before that is possible.

## Shared rule form

A prospective declarative registry would use these records, rather than 186 field assignments:

```text
DefinitionSignature = {
  signature_identity, schema_version,
  operation, stage, executor, effect,
  source_contract_variant,
  typed_input_rules, output_schema_refs, allowed_outcomes,
  permission_expression_ref, target_relationship_rules,
  definition_scope_rule, lineage_rule
}
ClaimBinding = {
  source_identity, raw_content_pin, source_schema, selector,
  claim_kind, declared_subject_identity, target_identity_domain,
  consumer_contract_identity, scope, lineage, source_dependencies
}
```

These are design interfaces, not installed canonical Planner types. A signature variant must be selected by an authoritative structural discriminator or explicit governing contract reference. It cannot be selected by filename, ActionId-specific guessing, acceptance-prose interpretation or observed runtime result. Literal differences that do not change construction semantics remain data.

The proposed general role rule is:

1. Authenticate the source schema, identity, pin and selector.
2. Resolve exactly one declared claim kind and typed subject relationship.
3. Match a versioned consumer contract allowing that claim kind and identity domain.
4. Validate exact scope/lineage/currentness and all dependencies.
5. Return the authorized role and target relation; otherwise reject.

Two independently supported claims in one container may have different roles. One claim cannot acquire a stronger role because its container also holds another record. No precedence chooses the most permissive interpretation.

## What governs the eight families

| Family | Semantic meaning | Governing interface / axes | Does the Action model alone suffice? |
|---|---|---|---|
| B01 | Source declares what an Action is and requires | Definition signature; all axes | Only after closed signatures and expected profiles exist |
| B02 | Source records selected/executed/held/current support separately | Claim admission; SUP/CTX/ID | No: occurrence and current proof are runtime claims |
| B03 | Source declares operational dependency relationships | Snapshot correspondence; IN/CTX/SUP | No: exact graph predicate/target correspondence needed |
| B04 | Source records request, no receipt and receipt/reentry route | Snapshot correspondence; IN/CTX/SUP | No: external lifecycle and route bindings needed |
| B05 | Source supplies preparation, decision, grant or target proof | Claim admission; AUTH/OUT/SUP/CTX | No: O08/O09 independently govern acceptance |
| B06 | Source establishes accepted typed knowledge | Claim admission; IN/OUT/SUP/CTX | No: declared requirement is not accepted claim |
| B07 | Source governs resolution of an unknown rule | Snapshot correspondence; IN/SUP/CTX | No: exact ExternalResolutionContract/body/pins needed |
| B08 | Source fixes checkpoint, policy, ledger and inventory identities | Snapshot correspondence; ID/CTX/SUP | No: composition and canonical snapshot identity needed |

The families can share **two supporting interfaces**, claim admission and snapshot correspondence, instead of eight unrelated policies. B02/B05/B06 require semantics independent of the Action-definition authority's scope; B03/B04/B07/B08 require versioned source-to-snapshot correspondence. This does not prove seven new Architect decisions are necessary: existing admission semantics should be reused, while any genuinely new correspondence policy must be explicitly reviewed.

Defining claim kinds alone will not generate native identifiers, current-support proofs or receipt routes. Complete role derivability remains **0/8** now. All eight have a place in the design; conditional interface coverage is not completed mapping.

## Deterministic derivation of 186 cells

The companion lists every Action, field, exact original source reference, semantic axes and derivation-rule ID. No cell is an individual Architect choice.

| Rule | Cells | Source inputs and deterministic operation | Remaining preparation |
|---|---:|---|---|
| D-RESULT | 63 | Operation/stage/effect + authoritative contract variant → unique finite output/outcome/transition signature | Closed payload schemas, allowed route correspondence and source acceptance-constraint table |
| D-AUTH | 63 | Authority literal + effect/context + declared grant relationship → exact permission expression | Complete native class/predicate/scope table and justified empty branch |
| D-K-OMITTED | 56 | Pinned schema + member presence → candidate-specific empty map or rejection | Unissued model policy |
| D-K-EXPLICIT | 3 | Producer/outcome/report pin + exact accepted claim/type/context → typed knowledge requirement | INPUT-BUDGET, INPUT-IMPLEMENTATION and FACT-BUDGET-APPLICABILITY crosswalks |
| D-EXTERNAL | 1 | Declared external prerequisite + unique request/handoff/receipt/reentry correspondence → typed reference | S-ELIGIBILITY native proposition/route mapping |

The other 633 cells retain their source-availability status and are revalidated under the full model; they are not assumed admitted. Definition origin and currentness remain separate provenance obligations. No result artifact supplies a prospective output contract unless independently authorized as a definition source.

## Candidate SM-S — signature-centred definitions

**What it means:** A versioned finite signature registry owns prospective inputs, outputs and permission expressions. The plan selects a signature through a governing schema/contract discriminator; literal values instantiate it. Consumer proof rules independently evaluate any actual root/slot consequence.

**Policy:** Preserve existing operation/effect/literal domains. Keep prerequisite categories distinct. For the pinned E1 legacy schema, omitted knowledge requirements would mean an empty independent knowledge map; explicit declarations and other gates remain unchanged. Each signature declares exact prospective types/outcomes and a permission expression, including an empty-authority-object case only where explicitly governed. Result admission itself does not assert target satisfaction.

**What changes:** A new versioned definition-signature registry and legacy omission policy. The omission proposal is part of this unselected alternative, not issuance of AD-K. It does not purport to recover historical intent.

**What resolves:** Conditional omission semantics for 56 cells are precise. The common construction rule covers all 63 records structurally. It does not yet resolve 63 result contracts, 63 permission expressions or four explicit joins.

**Compatibility and risks:** Preserves O01's complete-field comparison and native gates in principle. A single operation label may conceal different acceptance constraints; therefore a proposed signature cannot be admitted merely because its class matches. Missing contract-variant selectors reject. Output schema references cannot masquerade as accepted KnowledgeRecords.

**Authority scope:** Planner v0.1/E1_LEGACY_V1 minimum frozen-state migration only. No general future-experiment or execution permission is implied.

## Candidate SM-C — consumer-contract-centred definitions

**What it means:** Exact declared consumer relationships determine required input claim types, prospective output schemas and permission expressions. A deterministic compatibility join forms the Action contract; it rejects incompatible or missing consumer contracts.

**Policy:** Preserve operation/effect/literal domains and typed prerequisites. Omitted knowledge declarations reject until explicitly supplemented. Each consumer use/effect contract specifies its permission expression; no absent authority declaration means permission. Prospective target relationships carry independent proof obligations, never satisfaction. Compatible claim requirements may be combined; contradictory constraints reject rather than use precedence.

**What changes:** A typed consumer-contract construction rule, compatibility relation and explicit-definition requirement. This alternative does not infer outputs from historical consumer success or authorization from mere use.

**What resolves:** It explains how proof, authority, route and knowledge consumers could share role derivation. It currently resolves none of the 186 cells: concrete consumer contracts/crosswalks remain missing, and 56 omissions deliberately require definition supplements.

**Compatibility and risks:** Preserves native admission boundaries in principle. Consumer routes may be cyclic or underspecified; cycle handling and compatible-join semantics must be closed before generation. A consumer's need does not establish that a producer may supply it. That capability must come from a governing prospective contract.

**Authority scope:** The same bounded legacy migration scope. General consumer-driven Planner construction would require separately reviewed authority.

Neither candidate is presented as a completed executable semantic policy. They are the smallest useful contrasting construction models identified here, with exact limits below. Inventing payload or permission tables to label them complete would exceed the evidence and conceal material design work.

## Hypothetical evaluation and alignment

Both candidates were assessed against all 63 Actions, 819 field records and eight families. No hypothetical values or complete candidates were persisted.

| Candidate | Prior source-available cells | Additional conditional field derivations | Still unresolved | O01 admissible | Role families resolved/unresolved |
|---|---:|---:|---:|---:|---:|
| SM-S | 633 | 56 omission cells | 130 | 0/63 | 0/8 |
| SM-C | 633 | 0 | 186 | 0/63 | 0/8 |

SM-S's 689-field upper bound is not 689 admitted fields: the 633 source-available cells and full expected profiles still need validation. No native O01 invocation on complete candidates was possible. Zero admissible denotes no demonstrated admission, not 63 observed runtime failures. No proven contract conflict is established, but compatibility is incomplete. Neither candidate passes the full MC01 closure test.

Directly supported semantics in both: typed identities, all 13 mandatory O01 fields, existing effect classes, prospective/runtime separation, independent proof and authority predicates, provenance, currentness and source invalidation. New semantics: registry/consumer selection rules, bounded omission interpretation, and claim-specific correspondence annexes. No native concept is removed. Legacy normalization would change only through separately issued scope-bound authority. No option can create an event, grant, accepted proof, receipt or trusted global-control label.

## Authority and post-authority pipeline

The appropriate proposed decomposition is **multiple orthogonal semantic authorities**, not a single broad permission:

1. **Definition-model authority:** versioned Action signature/construction rules, with explicit subordinate K/R/A policies and all required finite annexes.
2. **Claim-role authority:** shared claim-kind/consumer relationships and exclusions, reusing existing admission semantics rather than overriding them.
3. **Legacy-correspondence authority:** exact source schema/selector/identity/context transformations for E1, dependent on the first two and the native snapshot contracts.

These are proposed authority scopes, not records created by this task. Any later record must bind its model/version, Planner version, source-format version, approved rule-table digest, decision identity, exclusions and exact migration scope. E1-specific normalization must not automatically govern future Planner inputs. No record authorizes 186 manually selected values, current applicability, external evidence or execution.

After authority issuance: validate its identities/scope → load closed typed registries → authenticate and derive source-role relations → derive 186 fields and revalidate all 819 → construct 63 complete definitions → compare to independently derived expected profiles under unchanged O01 → validate native claim/graph/reference state → qualify reload/invalidation and run MC01 preflight. Unknown or missing inputs reject. No LLM preference or free-form callback remains in that pipeline.

## Readiness and missing preparation

**ARCHITECT_MODEL_DECISION_READY = NO.** The missing preparation is specific:

- Finite proposed result payload/type schemas, outcome-route tables and contract-variant selectors preserving all source acceptance constraints.
- Finite permission-expression/native AuthorityClass/scope correspondence for the declared authority-rule variants.
- Exact three knowledge and one external-reference joins.
- Claim-specific native identity/current-support/route/envelope crosswalks for B01–B08 and the complete reached source set.
- Independent expected profiles and source-shaped qualification fixtures, including malformed/ambiguous/stale/cross-context cases.

A missing mapping contract is not proof of a missing historical fact. Conversely, authority cannot manufacture a fact if preparation later finds one genuinely absent. The eight external positive-evidence absences stay unresolved frozen state. No synthetic positive proof belongs in that migration by virtue of this design.

```text
UNRESOLVED_FIELDS = 186
ROLE_FAMILIES = 8
SEMANTIC_AXES = [ID,OP,IN,OUT,AUTH,EFF,CTX,SUP]
MODEL_CANDIDATES = [SM-S,SM-C]
AD_K_DISPOSITION = subordinate IN/schema policy; unissued
AD_R_DISPOSITION = subordinate OUT policy; contract preparation required
AD_A_DISPOSITION = subordinate AUTH policy; contract preparation required
ROLE_FAMILIES_DERIVABLE = 0/8 complete; 8/8 design-interface coverage only
MODEL_CONSEQUENCES = {
 SM-S: {conditional_new_fields:56, unresolved:130, O01:0/63, roles:0/8},
 SM-C: {conditional_new_fields:0, unresolved:186, O01:0/63, roles:0/8}
}
CANDIDATES_WITH_FULL_MC01_CLOSURE_PATH = []
ARCHITECT_MODEL_DECISION_READY = NO
MC01 = BLOCKED
MC02_READY = NO
M02_READY = NO
IMPLEMENTATION_MODIFIED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
```

Preservation checks cover all 10,911 frozen E1 paths/content hashes and the prior implementation/planning/backlog baseline. Companion coverage/count checks, JSON and `git diff --check` pass. This design changes no runtime, historical contract or authority record.
