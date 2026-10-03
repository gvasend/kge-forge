# BR-C2 semantic binding closure 1

**RESULT = PARTIAL.** Two of six domains are closed for definition normalization: SCOPE_BINDING and LINEAGE_BINDING. All63 action records were evaluated. Four domains still lack complete independently governed semantic bindings, so complete construction and O01 admission remain0/63. The three report/result routes support authenticated historical-record extraction, but not complete admission through their existing fixed synthetic result profiles. BR-C2 retry remains disallowed.

This is specification work only. No constructor, planner code, operational registry, tests, prior contract, or frozen E1 artifact was modified. No BR-C2 or later package was executed. The29 literal bindings and the shared-constructor source model are preserved.

## Artifacts

Six domain registries:

- [RESULT_BINDING](DETERMINISTIC_PLANNER_V0_1_BR_C2_SEMANTIC_BINDING_CLOSURE_1_RESULT_BINDING.json)
- [AUTHORITY_BINDING](DETERMINISTIC_PLANNER_V0_1_BR_C2_SEMANTIC_BINDING_CLOSURE_1_AUTHORITY_BINDING.json)
- [EVIDENCE_BINDING](DETERMINISTIC_PLANNER_V0_1_BR_C2_SEMANTIC_BINDING_CLOSURE_1_EVIDENCE_BINDING.json)
- [KNOWLEDGE_BINDING](DETERMINISTIC_PLANNER_V0_1_BR_C2_SEMANTIC_BINDING_CLOSURE_1_KNOWLEDGE_BINDING.json)
- [SCOPE_BINDING](DETERMINISTIC_PLANNER_V0_1_BR_C2_SEMANTIC_BINDING_CLOSURE_1_SCOPE_BINDING.json)
- [LINEAGE_BINDING](DETERMINISTIC_PLANNER_V0_1_BR_C2_SEMANTIC_BINDING_CLOSURE_1_LINEAGE_BINDING.json)

Supporting companions contain [normalization rules](DETERMINISTIC_PLANNER_V0_1_BR_C2_SEMANTIC_BINDING_CLOSURE_1_NORMALIZATION_RULES.json), the [complete63-action evaluation matrix](DETERMINISTIC_PLANNER_V0_1_BR_C2_SEMANTIC_BINDING_CLOSURE_1_ACTION_MATRIX.json), [result-route evaluation](DETERMINISTIC_PLANNER_V0_1_BR_C2_SEMANTIC_BINDING_CLOSURE_1_RESULT_PROJECTIONS.json), [fixtures and independent bounded reference predicates](DETERMINISTIC_PLANNER_V0_1_BR_C2_SEMANTIC_BINDING_CLOSURE_1_FIXTURES.json), [validation](DETERMINISTIC_PLANNER_V0_1_BR_C2_SEMANTIC_BINDING_CLOSURE_1_VALIDATION.json), and [complete preflight](DETERMINISTIC_PLANNER_V0_1_BR_C2_SEMANTIC_BINDING_CLOSURE_1_PREFLIGHT.json). A “complete matrix” means every route evaluated, not every route constructible.

Input hashes include the preceding normalization report and its five companions, frozen plan/manifest, O01/CE-01, and the original result predicates. New registries are not installed. No per-ActionId semantic switch or filename-based mapping is introduced.

## Six-category inventory and availability

| Category | Target | Authoritative information | Remaining gap / typed domain |
|---|---|---|---|
| RESULT_BINDING | result_contract | Each action's acceptance criteria; bounded result contracts; separately recorded outcomes | No complete possible Outcome/KnowledgeType/independent transition declaration for all63 |
| AUTHORITY_BINDING | authority_requirements | Three governing rule texts, predecessors, operation/effect boundaries | No complete typed AuthorityRequirementId and conditional grant predicate mapping or justified empty requirement |
| EVIDENCE_BINDING | external_prerequisites, provenance | Located source references, external declarations, acceptance criteria | Provenance source versus live EvidenceRequirementId/GateId classification remains ambiguous |
| KNOWLEDGE_BINDING | knowledge_requirements |56 omitted members,4 explicit empty lists,3 accepted non-PASS requirements | Legacy omission semantics and exact KnowledgeId/KnowledgeType source joins remain incomplete |
| SCOPE_BINDING | scope and provenance context | Exact plan scope, manifest source and target scopes | Closed as declared **definition** scope, with operational scopes retained separately |
| LINEAGE_BINDING | lineage and provenance context | Manifest current-plan pin and recorded subject lineage | Closed as **recorded subject lineage**, not proof of current applicability |

The matrix enumerates each affected ActionId rather than hiding omissions in aggregate counts. Source availability distinguishes raw information from the missing executable interpretation:

- RESULT_BINDING and AUTHORITY_BINDING: raw governing text is DIRECTLY_AVAILABLE; complete typed declarations are NOT_PRESENT in the inspected source/contract layer. This does not claim no authority exists anywhere in E1.
- EVIDENCE_BINDING: raw evidence is DIRECTLY_AVAILABLE; its complete requirement-role normalization is AMBIGUOUS for all63. A source-located assertion cannot become a required or satisfied operational gate by default.
- KNOWLEDGE_BINDING:56 missing-member interpretations are NOT_PRESENT; three declarations need an AMBIGUOUS type/identity join; four explicit empty declarations are AVAILABLE_BY_EXISTING_TYPED_RULE.
- SCOPE_BINDING: DIRECTLY_AVAILABLE.
- LINEAGE_BINDING: AVAILABLE_BY_AUTHORIZED_JOIN through `/current_plan/raw_sha256` to the exact plan bytes. Paths are locators, not the basis of correspondence.

The affected explicit-empty actions are DEC-BUDGET, REEVAL-BUDGET, DEC-IMPLEMENTATION and REEVAL-IMPLEMENTATION. The three source-bound accepted-knowledge cases are INPUT-BUDGET, INPUT-IMPLEMENTATION and FACT-BUDGET-APPLICABILITY. All remaining56 ActionIds are listed in the matrix with the missing omission rule.

## Closed normalizers

### NORMALIZE_SCOPE_BINDING

Canonical semantic value: EXACT_DECLARED_DEFINITION_SCOPE. Input is an authenticated selected action record, accepted BR-C1 binding, exact plan/manifest pins and provenance. Return the action's nonempty `scope` string unchanged. Retain the manifest's `source_scope` and `target_scope` separately in provenance and preserve their identity roles.

This explicitly settles the previously open definition/operational-scope choice: ActionIR.scope records definition scope. It does not claim the definition is executable in that scope or that a runtime grant applies. Existing synthetic O01 profiles used another profile-specific scope; their values are neither overwritten nor copied into real-source definitions. A future real-source expected O01 profile must independently bind this stated meaning.

Validation requires unique ActionId correspondence, exact source pins, exact original scope, matching envelope and current accepted **source binding**. Unknown scope substitutions, missing values, wrong domains and cross-envelope inputs reject. No inference uses ActionId prefixes, neighboring records or filenames.

### NORMALIZE_LINEAGE_BINDING

Canonical semantic value: EXACT_RECORDED_SUBJECT_LINEAGE. Join the manifest to the definition container by exact content identity; then return `/subject_pins/recorded_lineage` unchanged. Retain plan/manifest identity, runtime, G4, profile and subject correspondence as separately typed provenance.

The frozen value is a recorded lineage statement. The word CURRENT within that string is not a machine validity attestation. Source and target phase remain distinct. This normalizer does not establish EXECUTION-to-REQUEST applicability, satisfy a root or authorize resume. Missing/substituted manifest, a failed plan join, stale source binding, wrong lineage or conflicting envelope rejects.

These two contracts close only the definition fields. Their fixtures supply a trusted qualification validity view corresponding to BR-C1 admission; a runtime must verify the binding rather than trust an imported `CURRENT_ACCEPTED_BINDING` string. No new live evidence or real-source validity attestation is created here.

## Four incomplete semantic domains

The registries deliberately do not invent allowed values for these domains. Unknown or unbound semantics produce no ActionIR.

**RESULT_BINDING:** operation class does not determine all possible outputs. S-EXEC permits source discovery or a dossier; semantic actions can produce authority requirements; DEC-EXEC can be waived by validated existing evidence. Historical PASS is not a complete prospective result schema. Required closure input is a governed finite declaration of possible outcomes, knowledge types and independent root/slot proof guards, keyed by semantic rule rather than ActionId.

**AUTHORITY_BINDING:** source rules distinguish specification, later bounded execution and exact effect authority. Normalizing every non-effecting action to an empty requirement would overstate permission; normalizing every governance sentence to an outstanding gate would overblock. Required input is a typed requirement predicate identifying the exact grant route, conditions, scope/lineage and justified no-outstanding-requirement case. O01 compares these bindings; it does not derive them from English.

**EVIDENCE_BINDING:** a source cited to justify a definition is not necessarily a live prerequisite. Required input is the governed relation identifying each reference's role—definition provenance, accepted knowledge support, current proposition requirement or external gate—and its currentness rule. Existing plan evidence objects do not supply a universal role discriminator.

**KNOWLEDGE_BINDING:** explicit empty lists normalize to empty maps. No rule supplied by the inspected contract says an omitted member is semantically equivalent to empty. The three non-PASS requirements specify producers, recorded outcomes and report pins but do not complete the target map's KnowledgeId/KnowledgeType binding. Required input is the source-schema omission rule and accepted record/type identity mapping. Producer COMPLETED must not be invented to resolve this gap.

These are contract-definition boundaries, not requests for the eight external positive-reentry facts. Static definitions and suspended-state restoration must not require those facts to exist.

## Cross-category consistency

The rules companion defines CC01–CC06:

- Definition scope equals its source declaration; source/target scopes equal their manifest fields. These three values need not equal each other.
- Recorded lineage belongs to the exact plan-linked subject envelope. Its text does not establish current proof.
- Effect classification remains exactly the governing source value. Result normalization cannot downgrade an effect.
- PASS alone supplies no root/slot proof transition.
- Accepted knowledge preserves producer, recorded outcome, type and source currentness independently of historical completion.
- Any missing result/authority/evidence binding prevents complete construction even if every literal field passes.

These are necessary consistency predicates, not an invented operation-to-result compatibility table. Complete combination tests for still-unbound semantic domains remain unexecuted. No such test is marked PASS through vacuous absence.

## All63 actions and O01

The complete matrix classifies every action MISSING_AUTHORITATIVE_INPUT because each lacks at least RESULT_BINDING and AUTHORITY_BINDING. Secondary evidence/knowledge ambiguities are separately recorded. All63 have normalized partial scope and recorded lineage; four also have a justified empty knowledge map. IR and O01 identities remain null until complete construction.

O01 admission is not attempted on incomplete IRs. O01_ADMITTED therefore remains0/63, not63 fabricated rejects or63 synthetic copies. O01's trusted expected definition set cannot be supplied by copying the candidate constructor's output into its oracle. An independently governed real-source profile remains necessary.

No intrinsic contract contradiction was established: incomplete real-source bindings and fixed synthetic profiles are different boundaries, not mutually inconsistent rules. The conflict set is empty; the mismatch set is not.

## Three report/result routes

The [frozen execution ledger](../experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_PLAN_1.json) supplies authenticated report joins:

| Route | Producer | Ledger selector | Recorded state | Recorded knowledge |
|---|---|---|---|---|
| OR-BINDING | S-BINDING | /execution_history/3 | PASS | Unkeyed bounded inventory with explicit gaps |
| OR-CONTEXT | S-CONTEXT | /execution_history/4 | PASS | Five named claims with provenance indices |
| OR-PREP-VALIDATOR | PREP-VALIDATOR | /execution_history/14 | PASS | Four named preparation claims; dossier unissued |

Each actual report hash matches its ledger reference. The result companion records the exact source paths, content identities, canonical ledger-record identities, source bindings and knowledge values. Report text and ledger both record bounded PASS; this is not an inference from report presence. All three have empty resolved-root and resolved-slot arrays; the later two explicitly record unchanged transitions.

A shared partial `PROJECT_REPORT_TO_RESULT` can select exactly one ledger record by producer and report identity, authenticate both, preserve the explicit recorded result and claims, and emit RECORDED_BOUNDED_RESULT_CANDIDATE. Zero/multiple matches, producer mismatch, substituted sources or inconsistent claims reject. Canonical record identity is not authority identity. Current usability requires separate validity/type/profile admission.

`PROJECT_RESULT_TO_KNOWLEDGE` may preserve existing claim IDs and provenance indices; it cannot synthesize KnowledgeType or accepted-current status. S-BINDING's unkeyed inventory must remain unkeyed until a governed derived-identity rule exists. No per-action special mapping is used to manufacture one.

### Proven fixed-profile boundary

The original [result oracle expressions](DETERMINISTIC_PLANNER_V0_1_C06A_2_ORACLES_1.json) require exact equality for `mode = SYNTHETIC_QUALIFICATION_ONLY`, `/source_sha256`, provenance, subject and parameter pin. Each real report hash differs from its oracle's fixed synthetic source hash. The validation companion records all three required/actual pairs and the failed `/source_sha256` equality.

Consequently, preserving real source identity cannot satisfy the existing fixed profile. Supplying the expected synthetic digest/provenance would violate source authentication. This is not repaired by copying fixture payloads or by changing only their labels. Required closure is an independently governed real-source parameterization with exact payload selectors, identity/type bindings and scope/lineage correspondence. Existing O01 and result predicates were not weakened or rewritten.

RESULT_PROJECTIONS_COMPLETE remains0/3. The three historical-candidate positives are explicitly not complete result-admission positives.

## BR-C3 history interface

O02/O06 require ordered ledger events with identity, sequence, action, result reference, envelope and ledger; results with identity, producer, outcome, typed knowledge and holds; accepted override sources; and a consistent current action/hold summary. Mandatory supporting plan/results/evidence/override sources must remain pinned.

Available partial projections expose report/ledger identities, producer, recorded outcome, raw claims and provenance, and unchanged transition evidence. Missing fields are:

1. Independently admitted normalized ResultId references in the complete ordered execution ledger.
2. Governed KnowledgeType for claims and an identity rule for any consumed unkeyed inventory.
3. Complete hold/override correspondence and current-summary reconciliation.
4. Real-source admission profile and dependency inventory, with currentness separate from history.

Therefore BR_C3_HISTORY_INTERFACE is INCOMPLETE. A stale source must prevent current knowledge consumption without rewriting the historical PASS. An external wait or hold must not become proof absence, nor may current accepted proof require a historically BLOCKED producer to become COMPLETED.

## Fixtures, determinism and preservation

Executed independent specification checks:

- 63 scope/recorded-lineage source cases accepted their bounded definition fields.
- 10 scope/lineage negatives rejected substitution, wrong plan join/domain/action/scope/lineage/envelope, stale/unknown validity and an invented current-applicability claim.
- 3 historical-result candidates accepted their recorded fields.
- 33 historical-result negatives rejected wrong producer/type/outcome, report/ledger substitution, provenance or claim loss, cross-envelope composition, PASS-to-proof transitions and historical-to-current claims.

Total:66 bounded positives and43 bounded negatives. Eight complete-constructor/history cases are specified but unexecuted pending missing contracts. Complete action/result positive chains remain0. All109 executed cases retained outcomes after key reversal and canonical JSON reload. These checks do not qualify a runtime constructor, cold planner restore or BR-C2 implementation.

Source/currentness invalidation is explicit: a stale required source removes support for current admission after reload; historical existence remains recorded. No result fixture asserts that restoring a record makes it current evidence.

## Complete preflight and next boundary

The complete mismatch set is:

- SB-01 RESULT_BINDING, all63 actions.
- SB-02 AUTHORITY_BINDING, all63.
- SB-03 EVIDENCE_BINDING, all63.
- SB-04 KNOWLEDGE_BINDING,59.
- RP-01 OR-BINDING real-source admission parameterization.
- RP-02 OR-CONTEXT real-source admission parameterization.
- RP-03 OR-PREP-VALIDATOR real-source admission parameterization.
- HI-01 complete BR-C3 typed history output interface.

O10 remains excluded and BR-C4-owned. No new56-template or63-bespoke-projection obligation is created. Further closure must supply the listed shared semantic contracts and independently parameterized real-source result profiles; repeatedly applying the existing literal rules cannot supply them.

```text
RESULT = PARTIAL
SEMANTIC_BINDING_CATEGORIES = [RESULT_BINDING, AUTHORITY_BINDING, EVIDENCE_BINDING,
  KNOWLEDGE_BINDING, SCOPE_BINDING, LINEAGE_BINDING]
SEMANTIC_DOMAINS_COMPLETE = 2/6 (definition scope and recorded subject lineage)
ACTION_ROUTES_TOTAL = 63
CONSTRUCTIBLE = 0/63
O01_ADMITTED = 0/63
MISSING_AUTHORITATIVE_INPUTS = [SB-01, SB-02, SB-04, RP-01, RP-02, RP-03, HI-01]
UNKNOWN_SEMANTIC_VALUES = [] (unbound values are not invented)
AMBIGUOUS_BINDINGS = [SB-03; three accepted-knowledge type/identity joins within SB-04]
CROSS_CATEGORY_CONFLICTS = []
RESULT_PROJECTIONS_COMPLETE = 0/3
BR_C3_HISTORY_INTERFACE = INCOMPLETE
POSITIVE_CASES = 66 bounded specification PASS; 0 complete admission chains
NEGATIVE_CASES = 43 bounded specification PASS; 8 complete-contract cases NOT_EXECUTED
DETERMINISM = 109 bounded key-order/JSON-reload checks PASS; complete constructor NOT_QUALIFIED
BR_C2_CONTRACT_MISMATCH_SET = [SB-01, SB-02, SB-03, SB-04, RP-01, RP-02, RP-03, HI-01]
BR_C2_CONTRACT_CONFLICT_SET = []
BR_C2_RETRY_ALLOWED = NO
RESTORED_AND_QUALIFIED = 2/17
CE_02_CLOSED = NO
C06A_3_RETRY_ALLOWED = NO
C07_RETRY_ALLOWED = NO
IMPLEMENTATION_MODIFIED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
```
