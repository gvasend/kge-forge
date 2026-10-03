# E1 legacy migration M01 result

**WORK_PACKAGE = M01; RESULT = PARTIAL; M02_READY = NO.** The package definition is precise enough to execute specification work, but its acceptance criterion is not yet satisfied. This attempt defines migration metadata and disposition contracts, inventories all35 target categories/13 source families and evaluates the full preflight. It does not claim complete field normalization, real-source profile admission or compiler qualification.

No runtime, registry, existing tests or historical artifacts were changed. M02–M07, real-E1 readiness, resume and action execution were not performed.

## Verified package and outputs

The authoritative [implementation plan](DETERMINISTIC_PLANNER_V0_1_E1_MIGRATION_IMPLEMENTATION_PLAN_1.md), [machine plan](DETERMINISTIC_PLANNER_V0_1_E1_MIGRATION_IMPLEMENTATION_PLAN_1.json) and [acceptance matrix](DETERMINISTIC_PLANNER_V0_1_E1_MIGRATION_ACCEPTANCE_MATRIX_1.md) assign M01:

- The existing migration-boundary decision and BR/Oxx evidence as inputs; no earlier migration package dependency.
- Closure of four remaining ActionIR semantic domains, three real-source result profiles, native imported-history representation, exact source whitelist and field/disposition coverage.
- All required source classes and canonical target families, not a narrow sample.
- Independent MC01–MC06 oracles: source recognition, coverage, Action admission, result admission, history reconciliation and composition.
- Acceptance only when every required operational field has independent semantics and input schemas/historical result compatibility are qualified. Successful M01 unlocks M02.

The following new companions preserve prior artifacts:

| Artifact | Content and actual status |
|---|---|
| [Contract](DETERMINISTIC_PLANNER_V0_1_E1_MIGRATION_M01_CONTRACT.json) |35 classified target categories with target type/domain/cardinality/source/admission/invalidation/persistence;13 source families; provenance/identity/disposition/manifest contracts;17-element crosswalk. Exact nested semantic maps remain incomplete. |
| [Absence and control](DETERMINISTIC_PLANNER_V0_1_E1_MIGRATION_M01_ABSENCE_AND_CONTROL.json) | All eight real request/receipt/reentry references, preserved absence and independent expected frozen outputs; complete migrated derivation remains pending. |
| [Oracles](DETERMINISTIC_PLANNER_V0_1_E1_MIGRATION_M01_ORACLES.json) | Seven required property families, explicit reused versus bounded versus incomplete status. |
| [Fixtures](DETERMINISTIC_PLANNER_V0_1_E1_MIGRATION_M01_FIXTURES.json) | Synthetic source-shape/metadata cases and executable specification predicates; no compiler or complete native-admission claims. |
| [Validation](DETERMINISTIC_PLANNER_V0_1_E1_MIGRATION_M01_VALIDATION.json) |48 executed bounded specification cases and MC01–MC06 status. |
| [Complete preflight](DETERMINISTIC_PLANNER_V0_1_E1_MIGRATION_M01_PREFLIGHT.json) | All six mismatch groups, conflicts, semantic-input distinction and M02 gate. |

## Canonical target contract

Reuse existing Snapshot/PersistenceBundle and codec identity rules. No second canonical state representation is installed. Required targets are actions/statuses, roots/slots, knowledge, graph/entities/assertions/predicates, context, decisions, evidence/gates/receipts, boundaries/goals, budget contracts, source/policy binding, historical attempts/current overlay, native bundle initial/current/events, expected absences, manifest and derivation index.

Optional targets remain independently computable information/cost metrics. Descriptive narrative and saved control summaries are provenance/oracle-only. Absent positive external evidence and raw unreferenced archive bodies are not required for frozen resume; their required absence/provenance records remain required.

The companion records each category's type, identity domain, cardinality, source classes, migration rule, canonicalization, provenance, currentness, admission, invalidation and persistence. Existing native annotations were inspected rather than inferred from the plans. Full nested-field derivations are explicitly marked missing: this inventory is not proof that all target fields can already be populated. A required field without a supported mapping must block emission of the complete canonical snapshot, not invoke a dataclass default.

Every operational target still requires its native admission: O01 for definitions, O02/O06 for current prerequisite/history/hold reconciliation, O08 for the validator authority chain, O09 for exact baseline slot proofs, O10 for operational graph projection, O16 for complete composition, plus budget, decision/authority, root/slot and native model/reference/codec checks. Migration success does not imply admission. An input claiming `admitted=true` is not an admission receipt.

## Disposition, recognition and provenance

Each relevant source instance receives exactly one primary disposition. Mixed-role artifacts use MIGRATED_OPERATIONAL if any operational clause is required, with separate field-level dispositions. MIGRATED_PROVENANCE_ONLY cannot conceal a gate. HISTORICAL_ONLY preserves evidence without claiming current truth. NOT_REQUIRED needs an audited exclusion from the required dependency closure. REPRESENTED_AS_EXPECTED_ABSENCE names a virtual expected source attached to an actual gate contract; it cannot label a malformed missing required file.

Structural recognition reuses the nine CE-02 class descriptions. Additional planned external-request, candidate-authority and global-control schemas are identified, but their nested profiles remain to be completed. GOVERNED_TEXT needs an authenticated kind and reviewed section selectors; PINNED_SUBJECT needs a closed exact domain-schema whitelist. Neither may become an arbitrary text/JSON catchall. Unknown or competing class matches reject. Paths locate bytes; they do not establish schema or authority.

The new positive recognition cases cover the eight available machine-discriminated CE-02 shapes. Empty collection placeholders in these synthetic shape fixtures test recognition only; they are deliberately not accepted operational graph/plan snapshots. Complete source-shaped native positive fixtures for every required class remain a preflight gap.

FieldDerivation has exact required members: legacy identity, content identity, schema, migration contract, canonical target identity/field, source selector, transformation, dependencies and validity. Transformations are DIRECT, TYPED_DERIVATION, AUTHORIZED_JOIN or CONTRACT_CONSTANT. Current accepted support, historical-only evidence, stale support and unresolved support remain distinct. Structural presence does not authenticate a provenance record: every selector, domain and supporting pin must subsequently satisfy its existing source/admission contract.

## Identity and manifest rules

Preserve legacy declared identities and raw/embedded content hashes separately. ActionId remains the exact declared identifier. Authority identity is the governing authenticated record identity, not a hash minted by migration. Proof identity remains governed by its target-specific admission. Canonical result and graph projection identities require the approved typed migrated representation and retain original identities as dependencies. Snapshot identity remains the native codec's identity.

Metadata uses domain-separated hashes of canonical `{schema, domain, payload}`. Sort object keys and declared sets; preserve causal event order. Equal digest text across domains does not imply equivalence. A source or migration-rule change invalidates dependent canonical support after reload; retaining historical records does not make them current again.

MigrationManifest is defined with an exact field set: source/target format, native schema, migration-contract identity, source-inventory identity, source pins, output-inventory identity, snapshot/bundle identities, provenance-index identity, source dispositions, expected absences, unresolved prerequisites, qualification state and qualification-record reference. Unknown fields reject.

Avoid identity cycles: hash output artifacts and derivation index first; the output inventory excludes the manifest; qualification evidence refers to those immutable outputs rather than its containing manifest identity; hash the manifest last. An incomplete diagnostic manifest has no usable output identity and remains NOT_QUALIFIED. QUALIFIED_MIGRATION requires independently verified output admission and qualification evidence, not a saved label. This task tests diagnostic-manifest rules only, not a successful migration manifest.

## History contract: new concrete boundary

Inspection of `/execution_history/0` in the frozen plan establishes a selection attempt with `status=SELECTION_BLOCKED`, `planner_exception=PLANNER_TIE_BREAK_UNDEFINED` and `action_result=null`. Its explanation says no action was selected or executed. It must not become an ActionResult.PASS, an executed BLOCKED action, or a fabricated native event. All24 ledger records still need coverage; not all are action-result records.

Define the imported-history envelope as immutable record identity, ordinal, recorded kind, original plan/selector/record hash, optional action/outcome, result source pins, knowledge references and support dependencies. Kind is SELECTION_ATTEMPT or ACTION_ATTEMPT determined from recorded structure, never ordinal or filename. Preserve selection diagnostics as historical diagnostics. Subsequent native ExecutionEvents begin at a proved canonical migrated baseline; do not fabricate historical parent/after snapshot identities.

This closes that semantic distinction, not the full imported-history model. Exact native codec integration, result/knowledge typing, hold/override reconciliation and independently complete O02/O06 real-source profiles remain M01-G03. No new runtime type was implemented.

## Semantic normalization inventory

| Requirement | Classification | Evidence / remaining obligation |
|---|---|---|
| Common63-action core and29 literals | CONTRACT_REUSED | Existing plan-backed ActionIR work |
| Exact definition scope / recorded subject lineage | CONTRACT_REUSED | Prior semantic closure; recorded lineage is not current applicability |
| Complete prospective result declarations | CONTRACT_MISSING | Acceptance text and historical results do not provide complete typed output/transition bindings |
| Conditional authority requirements | CONTRACT_MISSING | Existing grant evidence/rules must become exact typed requirements without invented empty defaults |
| Evidence role normalization | CONTRACT_MISSING | Definition provenance and operational evidence requirements are not interchangeable |
| Knowledge omission/type/identity interpretation | CONTRACT_MISSING |56 omitted members and three accepted non-PASS requirements; four explicit empties already governed |
| Three real-source result profiles | CONTRACT_MISSING | Fixed synthetic identities cannot authenticate actual report bytes; independent parameterization still required |
| Identity/provenance/disposition metadata | CONTRACT_COMPLETE at metadata layer | Native authentication and full field coverage remain separately required |
| Selection-attempt versus action-attempt history distinction | CONTRACT_COMPLETE at semantic envelope layer | Full native history/hold admission remains incomplete |
| Graph/proof/decision/budget/receipt semantics | CONTRACT_REUSED | Existing oracles retained; full real-source bindings/composition not yet qualified |
| Positive external evidence absent at suspension | NOT_REQUIRED_FOR_FROZEN_RESUME | Eight expected absences remain typed operational state |

No new positive factual input needed for the frozen state was proven absent in this task. Accordingly SEMANTIC_INPUT_MISSING_SET is empty; this is not a claim that all semantics are known. Unestablished interpretation rules remain CONTRACT_MISSING. The eight external evidence gaps remain genuine absent positive-reentry facts, intentionally outside the missing-frozen-input set.

## Absence, frozen oracle and synthetic reentry

The absence companion enumerates all eight manifest request routes: budget, ancestry, approval, audit, runtime head, supervisor, executable policy and implementation. Each retains request and handoff identity, receipt endpoint, named reentry and false evidence-received state. Exact missing propositions/producer competence must resolve through the referenced handoff/BR-C1 contracts; no invented positive producer attestation is added. Legacy WAITING_FOR_EXTERNAL_INPUT remains recorded, and its canonical branch classification must preserve fact/dependency distinctions.

The independent frozen expectation is MIXED_WAIT, no internal runnable actions, no decision-ready actions, resume=false and eight unresolved active external gates. These are comparison oracles only. Full derivation from admitted canonical fields is incomplete, so FROZEN_STATE_ORACLE is reported INCOMPLETE for the integrated migration acceptance test, even though the expected labels are known.

The separate synthetic reentry contract reuses the budget proof oracle and canonical receipt/resume predicates. A complete independently admitted synthetic budget bundle and every other named-action prerequisite may enable its reentry in an isolated migrated clone; the other seven branches remain waiting/blocked. It creates no real E1 evidence. The integrated migrated positive base is missing, so SYNTHETIC_REENTRY_ORACLE is INCOMPLETE; the existing bounded budget oracle itself is not reopened.

## Executed specification checks and complete preflight

The48 checks exercise structural source recognition, source-disposition guards, metadata identity-domain/hash validation, provenance shape, synthetic absence envelopes and diagnostic-manifest qualification guards. They do not claim native admission or operational completeness. All48 passed. The validation companion reports positives and negatives separately. Unexecuted required families are explicitly listed in the fixture companion.

| M01 acceptance case | Result | Reason |
|---|---|---|
| MC01 source recognition | PARTIAL | Bounded structural cases pass; full nested profiles/closed subject whitelist missing |
| MC02 dispositions/completeness | PARTIAL | Disposition rules defined; exhaustive semantic source/target closure pending |
| MC03 Action admission | BLOCKED | Four required semantic normalization domains incomplete |
| MC04 real-source results | BLOCKED | Three parameterized profiles incomplete |
| MC05 history | PARTIAL | Selection/action distinction defined; complete canonical history admission missing |
| MC06 composition | BLOCKED | No complete real-source admitted component set |

The complete mismatch set is:

- M01-G01: complete four ActionIR semantic domains for63 definitions, including59 unresolved knowledge bindings.
- M01-G02: three real-source result profile normalizations.
- M01-G03: native imported-history/holds/knowledge interface and full admission.
- M01-G04: exact nested source profiles, authenticated text selectors and closed subject-schema whitelist.
- M01-G05: exhaustive field derivation/disposition and17-element native admission crosswalk.
- M01-G06: complete source-to-native positive/negative fixtures and composition qualification across all required classes.

No contract conflict was established. All13 families and35 target categories were considered; this result did not stop after the first gap. Required full positive fixtures cannot be replaced by recognition-only or metadata-only cases. M02_READY remains NO; next work is bounded M01 contract closure, not M02 implementation.

## Traceability and report

BR-C1 bindings/absences and identity/invalidation rules are REUSED_DIRECTLY and REUSED_AS_ORACLE. CE-01 and O01/O02/O06/O08/O09/O10/O16, budget and decision/proof/receipt oracles are REUSED_AS_ORACLE; full real-source binding remains STILL_REQUIRED. BR-C2 is SUSPENDED; its common model and accepted partial bindings are reused, while source-specific projection packaging is SUPERSEDED_BY_MIGRATION. BR-C3 history, BR-C4 graph and BR-C5 composition obligations are STILL_REQUIRED within migration packages. CE-02 remains OPEN. No prior result, fixture, contract or count was rewritten.

```text
WORK_PACKAGE = M01
RESULT = PARTIAL
MIGRATION_TARGET_ELEMENTS = 35 classified categories in CONTRACT.target_elements
LEGACY_SOURCE_CLASSES = [PLAN, GRAPH, MANIFEST, HANDOFF, CHECKPOINT,
  DECISION_AUTHORITY, PROFILE_CANDIDATE, INVOCATION_CANDIDATE, GOVERNED_TEXT,
  EXTERNAL_REQUEST, CANDIDATE_AUTHORITY, GLOBAL_CONTROL, PINNED_SUBJECT]
CONTRACTS_REUSED = [BR-C1, CE-01, ActionIR/literals, O01/O02/O06/O08/O09/O10/O16,
  budget, decision/authority/proof/receipt, identity, policy, invalidation, persistence]
CONTRACTS_DEFINED = [dispositions, metadata identities, field provenance envelope,
  migration manifest, imported-history kind distinction]
CONTRACTS_MISSING = [M01-G01, M01-G02, M01-G03, M01-G04, M01-G05, M01-G06]
SEMANTIC_INPUTS_MISSING = [] newly established frozen-state inputs; contract gaps remain
MIGRATION_ORACLES = seven families inventoried; bounded executable subsets and reused authorities
POSITIVE_FIXTURES = 24 bounded cases PASS; 0 complete migration positives
NEGATIVE_FIXTURES = 24 bounded cases PASS
SPECIFICATION_CASES = 48 PASS (not complete migration qualification)
M01_CONTRACT_MISMATCH_SET = [M01-G01, M01-G02, M01-G03, M01-G04, M01-G05, M01-G06]
M01_CONTRACT_CONFLICT_SET = []
M01_SEMANTIC_INPUT_MISSING_SET = []
MIGRATION_MANIFEST = DEFINED
FROZEN_STATE_ORACLE = INCOMPLETE
SYNTHETIC_REENTRY_ORACLE = INCOMPLETE
M02_READY = NO
NEXT_PACKAGE = M01 contract closure follow-up
CE_02_STATUS = OPEN
V0_1_CURRENT_STATUS = CORRECTION_REQUIRED
IMPLEMENTATION_MODIFIED = NO
REAL_E1_EVIDENCE_CREATED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
```

Preservation validation: all10,911 frozen paths and byte hashes unchanged; all other pre-existing protected files unchanged. Seven new specification/result artifacts only. JSON, relative links, whitespace and `git diff --check` passed.
