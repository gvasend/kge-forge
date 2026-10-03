# M01 minimum-state blocking-cut closure plan 1

**Four specification/qualification packages address the five interfaces. First package: MC01. M01_MINIMUM_STATE_CONTRACT_COMPLETE = NO; M02_READY = NO.** This is a closure plan, not closure evidence. No interface is promoted by this document.

Scope is C1–C5: derive MIXED_WAIT, no runnable internal actions, no active decision-ready actions, no resume permission, and the exact eight source-bound external boundaries. It is not all-35-target migration closure. The native control repair remains accepted; CUT04 now needs migration source binding, not another runtime repair.

The [machine-readable dependency/closure plan](DETERMINISTIC_PLANNER_V0_1_M01_MINIMUM_STATE_CLOSURE_PLAN_1.json) contains all interfaces, field classifications, source-binding requirements, dependency edges, packages and gate expressions. Input hashes pin the [post-repair analysis](DETERMINISTIC_PLANNER_V0_1_M01_POST_REPAIR_MINIMUM_STATE_1.md) and its three companions, migration plan/acceptance matrix, Action source-model/normalization/semantic-closure work and BR-C1 contract.

**Naming:** package MC01–MC04 below belongs to namespace `M01-MINIMUM-CLOSURE-1`. These are not the existing migration acceptance-case IDs MC01–MC26. References to an old test use `acceptance-case MCxx`. No old package or acceptance record is overwritten.

## Five normalized interfaces

| Interface | Required canonical state and native consumer | Frozen sources | Missing contract/normalization and proof |
|---|---|---|---|
| CUT01 | 63 native Actions and matching 13 COMPLETED/50 BLOCKED statuses; typed prerequisites, qualification and necessary support. `validate_model`, `project`, `_actionability`, `current_completion` | Resolution plan `/resolution_actions`, `/compiled_action_dependencies`, `/execution_state`; pinned manifest state; referenced current-support sources | Shared constructor's common core exists, but source-backed native field semantics and unchanged O01 compatibility are incomplete. Need exact authority/evidence/knowledge roles, justified optional/empty fields and independently expected 63-row profile. Current holds need source-backed support, not fabricated replay. |
| CUT02 | Retained root/slot goals, prerequisite paths, current cut points, eight boundary/receipt/reentry/held-action correspondences. `project`, `evaluate_satisfaction`, `_global_control.walk` | Plan normalized/deferred conditions and compiled routes; graph slot identities; manifest request_routes; handoff and receipt contracts | Typed conditional-route and native identity crosswalk; implementation composite frontier and DEC-EXEC readiness-reevaluation correspondence. Need independently expected frontier/bijection and omitted/dangling/cross-route negatives. |
| CUT03 | Reached predicates/entities/knowledge/assertions/context and root/slot/decision/current-completion support. Native gates, `unavailable_support`, proof evaluation and validation | Source claims reached through CUT01/02, including accepted preparation/decision/grant and baseline slot-proof sources where retained | Exact proof identity/type/source assignments, context joins and transitive currentness closure. Need O08/O09 source-specific admission and stale/reload withdrawal proof only for retained support. |
| CUT04 | Unknown EvidenceRequirement plus current ExternalResolutionContract, exact consumer predicate, gate and context. `governed_external_unknown`, `_global_control`, `_obligation_proof` | Budget request and its eight obligations; request/handoff/receipt records; manifest envelope; requirement/gate provenance | Runtime semantics complete. Missing versioned legacy-to-canonical contract-body derivation, exact source pins and consumer/held/reentry correspondence. Need independent source-shaped contract-binding fixtures; canonical self-hash alone is not authority. |
| CUT05 | Admitted identical initial/current baseline, zero new native events, exact policy/version/scope/source pins, FrozenControlProof references. Codec replay/restore, recompute and C03 resume | Checkpoint, manifest, independently pinned policy; admitted outputs/source dependencies of CUT01–04 | Baseline/certificate source coverage, domain-separated identities and complete reference/route/universe proof. Need composed oracle and cold/reload/invalidation expectations, without reconstructing historical transition chains. |

Every interface remains CONTRACT_INCOMPLETE. Their sources establish frozen records/absences; their native interpretation is not yet complete. No new positive external evidence is requested. The companion identifies each interface's missing bindings B01–B08, normalization, proof and dependencies explicitly.

## Dependency graph and shared roots

Edges mean “consumer needs the prerequisite's contract,” not chronological execution. There are 13 directed edges:

- CUT01 → CUT02; CUT02 → CUT01: action identity coverage and prerequisite/goal correspondence.
- CUT01 → CUT03; CUT02 → CUT03: support seeds and reached paths.
- CUT03 → CUT01; CUT03 → CUT02: current completion/support and valid frontier cut points.
- CUT01, CUT02, CUT03 → CUT04: consumer identity, external routing, proof/context/source binding.
- CUT01, CUT02, CUT03, CUT04 → CUT05: composed baseline and certificate.

Thus there is **no independent singleton root cut member**. The root strongly connected component is `{CUT01,CUT02,CUT03}`; its dependents are CUT04 then CUT05. Treating these as five independent repairs would cause repeated discovery of reference gaps. The package DAG breaks specification cycles by declaring shared typed identities/interfaces first, then filling definitions, then closing their support fixed point. Provisional signatures are not operational admission.

Parallelizable work is bounded: source inventory and independent oracle/scope review within MC01; Action-field and goal-route drafting against the same signatures in MC02; retained O08/O09 proof and governed-wait binding fixtures within MC03. Final qualification joins those results and cannot run ahead of dependencies. This plan does not dispatch parallel work.

Shared root causes:

1. **Missing source-to-native typed reference/role contract:** affects action prerequisites, evidence versus provenance, knowledge joins and all external routes.
2. **Missing bounded support/currentness closure:** affects current completion, satisfied cut points, slot/root proof and external source validity.
3. **Missing independent minimal-profile/composition oracle:** affects O01 compatibility, source coverage and the final baseline certificate.

BR-C1 already supplies generic pinned identity, source context, provenance, explicit joins and expected absence mechanisms. It does not supply all native instance bindings or interpret missing semantic roles. Reusing it avoids another binding framework; it does not make CUT01–05 complete.

## Action-universe gap and all native fields

Common plan-backed construction covers 63 identities/literal records. It does not yet supply 63 independently admitted frozen native definitions. No canonical partial-Action type was found: Snapshot.actions contains `Action`, `validate_model` checks all retained types/references, and action/status identities must match. A hold bypasses `blockers`, not snapshot validation, graph projection or global traversal.

The table separates control use from native field obligation. Classifications can coexist: a field can have future operational meaning but still require a justified native value now. `REQUIRED_BY_NATIVE_ACTION_VALIDATION` includes dataclass type and codec representation obligations; optional fields may use None/empty only under an independently established mapping. Python defaults are not source semantics.

| Action field | Classification and exact present obligation |
|---|---|
| id | REQUIRED_BY_FROZEN_CONTROL; exact ActionId and universe correspondence |
| operation | REQUIRED_BY_FROZEN_CONTROL and native validation; human/machine and decision-input type distinctions |
| effect | REQUIRED_BY_NATIVE_ACTION_VALIDATION; retained decision-input effect checks. Real effect permission is execution-only, but do not replace the source effect |
| prerequisites | REQUIRED_BY_FROZEN_CONTROL; exact typed action/condition references and ordering |
| source | REQUIRED_BY_FROZEN_CONTROL and native validation; valid provenance and source pin |
| accepted_inventory | REQUIRED_BY_FROZEN_CONTROL for retained stale-support propagation and REQUIRED_BY_NATIVE_ACTION_VALIDATION for the collection/knowledge records. Rich prospective outputs are deferrable only outside this closure and after O01 compatibility is settled |
| evidence | REQUIRED_BY_FROZEN_CONTROL where retained; assertions must exist and currentness propagate |
| requirements | REQUIRED_BY_FROZEN_CONTROL; reached rule evaluation and exact EVIDENCE_OBLIGATION binding |
| authority | REQUIRED_BY_FROZEN_CONTROL where retained; transitive stale authority affects completion; referenced predicate must validate |
| stage | REQUIRED_BY_NATIVE_ACTION_VALIDATION; preserve source-governed stage, not narrative reconstruction |
| cost | NOT_REQUIRED by frozen computation with no candidates; native optional type/nonnegative constraint still applies |
| cost_unit | NOT_REQUIRED for frozen selection; REQUIRED_BY_NATIVE_ACTION_VALIDATION if cost present |
| pass_model_complete | NOT_REQUIRED by frozen held-path selection; native Boolean still requires governed representation |
| accepted_result | Native typed field REQUIRED_NOW; future result application/reentry semantics are deferred. `validate_p04` rejects non-PASS outside bounded fact/decision routes. Do not claim default PASS means execution |
| prepared_dossier | REQUIRED_BY_NATIVE_ACTION_VALIDATION if retained; source-backed route, checks and references. Full future dossier preparation is deferred, not a license to keep an invalid partial dossier |
| qualification | REQUIRED_BY_FROZEN_CONTROL; stale/support propagation and current completion |

The companion exhaustively enumerates these 16 fields. No whole native field is unconditionally erased. Deferred material is richer content outside the retained dependency closure, not a competing lightweight Action implementation. Matching `ActionStatus(id,state)` is also required. Definition scope and recorded lineage live in normalized provenance/context relationships; they are not invented native Action attributes.

### Four unresolved domains

| Domain | Required now / derivable | Deferrable / missing |
|---|---|---|
| RESULT_BINDING | Native accepted_result and retained inventory validity/type/reference obligations. Recorded source outcomes and bounded fact/decision route rules are available; they are not a complete prospective contract | Future outputs/transitions outside current support DEFERABLE. Justified minimal result/inventory projection and O01 compatibility MISSING. No blanket default PASS or empty inventory |
| AUTHORITY_BINDING | Exact retained authority predicate and currentness/support relation REQUIRED_NOW. Existing O08 governs the bounded validator chain where reached | New effect grants/applicability checks used only for execution DEFERABLE. Source rule → native requirement or justified absence remains MISSING |
| EVIDENCE_BINDING | Provenance/current support/required proposition classification and external consumer binding REQUIRED_NOW. BR-C1 source pins/absence records DERIVABLE using its existing contract | Positive external evidence DEFERABLE. Role and native EvidenceId/PredicateId/context projection MISSING |
| KNOWLEDGE_BINDING | Reached KnowledgeId/type/source predicates and currentness REQUIRED_NOW; four explicitly empty declarations have existing rules | Unused prospective knowledge DEFERABLE. Omission semantics and three accepted non-PASS source/type joins remain MISSING where retained |

Existing scope/lineage normalizers are reused as definition/recorded-subject bindings, not proofs of current applicability. Fields not consumed on a held path can still be mandatory under native/O01 admission. MC01 must settle the minimal admissible representation using those existing rules. If unchanged O01 requires a field whose semantics are unavailable, report that exact blocker; do not import all future execution detail automatically or silently weaken O01.

## Deterministic source bindings

The companion records SOURCE IDENTITY, TARGET IDENTITY, domains, join key, scope, lineage, currentness and provenance for B01–B08. These are requirements to instantiate, not issued target identities:

| ID | Source → target | Deterministic join and remaining work |
|---|---|---|
| B01 | Plan action/dependency records → ActionId/Gate targets | Exact ActionId and typed condition identity; shared constructor's missing semantic roles |
| B02 | Plan/manifest current state plus supporting claims → ActionStatus/current completion | Exact ActionId, pinned plan and extracted state/ledger identity; source-backed hold reconciliation for complete universe |
| B03 | Conditions/slots/compiled goal routes → ConditionId/SlotId/Goal/PredicateId | Exact source IDs and selectors plus reviewed typed crosswalk; conditional and composite correspondence incomplete |
| B04 | Manifest requests + handoff + receipt contracts → GateId/EvidenceId/receipt/reentry/held actions | Request identity, handoff identity, exact route fields; BR-C1 gives eight source absence bindings, not final native projection |
| B05 | PREP-VALIDATOR/dossier/decision/grant and baseline proof sources → retained O08/O09 state | Exact dossier/decision/authority and slot/predicate/source identities under native admission; real-source parameterization incomplete |
| B06 | Accepted source reports/non-PASS claims → KnowledgeId/type/source predicates | Producer ActionId + exact report content identity + accepted claim/outcome; no chronology-based inference |
| B07 | Budget request + B04 + envelope → ExternalResolutionContract | Exact requirement/gate/proposition/target/source class/route fields. Canonical contract bytes and raw content pin with every field traced to legacy sources/rule version |
| B08 | Checkpoint/policy/manifest and admitted baseline → PersistenceBundle/certificate | Distinct raw policy, extracted policy, canonical snapshot and source inventory identities; no same-hash domain substitution |

Every join must yield exactly one typed correspondence or reject. Retain source and target scopes separately; enforce equality only where the governing native contract requires it. Preserve recorded lineage separately from current validity. Provenance includes original source identity/content hash, exact selector, transformation-contract version, target identity and dependencies. Source changes invalidate dependent bindings and force native re-evaluation. A fresh checksum does not authorize substitution.

For B07 the repaired contract requires matching scope/lineage/generation across context and acquisition record, provenance scope, exact gate/requirement sources and actual consumer's obligation predicate. The canonical body pin is additional to, not a replacement for, legacy derivation. BR-C1 provides generic provenance/pin/absence mechanisms; B03/B05/B06/B07 also lack semantic normalization, so the remaining work is **not merely populating IDs**.

## Minimum support and operational graph

Retain only support reached from current completion/holds, root/slot satisfaction, inspected action requirements, necessary decision references and all native validation references. A historical BLOCKED producer may have valid current knowledge; a historical COMPLETED producer may have stale support. Selection is neither execution nor a result. Current claims can be extracted without rebuilding all three ActionResult histories.

Native node types in the required projection are ActionId, ConditionId, SlotId and referenced EntityId; PredicateId, KnowledgeId, AssertionId, GateId and EvidenceId remain their distinct support domains. Root/slot proof cannot be replaced by a copied Boolean. O08 applies to retained validator-authority gate proof; O09 applies to each retained baseline slot proof. Exact membership must be established by MC02/03, not assumed from a complete historical graph.

Finite graph vocabulary, using the existing model:

- Ordering: `Relation.REQUIRES`, with ordering justification, must agree with Action prerequisite metadata. No other relation creates ordering.
- Retained provenance/proof relationships, when the selected source proof requires them: `PRODUCED_BY`, `DERIVED_FROM`, `AUTHORIZED_BY`, `VALIDATED_BY`, `CONSUMED_BY`, `EVIDENCED_BY`, `BINDS`, `APPLIES_TO`, `HAS_SLOT`, `HAS_IDENTITY_TYPE`, `PROVEN_BY`, `SATISFIED_BY`, `CORRESPONDS_TO`. This is the exact native whitelist, **not a requirement to import every instance or every relation kind**. A proof reference may instead be expressed by the native typed field that actually consumes it.
- Reached EntityKind values: SOURCE/PRODUCER for provenance, AUTHORITY for grants/decisions, VALUE/MAPPING/VALIDATOR for retained slot admission, EVIDENCE/TARGET for required proof and receipt targets. No positive absent evidence entity is invented.
- Predicate closure starts from root predicates, slot requirements, action requirements/authority and retained dossier checks. Close their typed operands/entities/knowledge/conditions; use existing predicate kinds including EVIDENCE_OBLIGATION. An unrecognized required predicate remains defective, not an invented UNKNOWN placeholder.

The source inventory has 63 actions, 116 dependency edges and 31 top-level routes; those counts are not asserted as the final minimum native graph. Full historical graph restoration is not required. MC03 must produce the exact bounded instance list and a reason for each retained node/edge, plus reference and transitive stale-invalidation closure. No exact smaller graph is claimed before those mappings are defined.

All eight external boundaries remain **source-absence contract complete but native migration contract incomplete**. CUT02 supplies identity/routing, CUT01 consumer definitions/statuses, CUT03 context/support and CUT04 the governed-unknown contract where required. Budget remains EXTERNAL_EVIDENCE waiting; the other seven remain factual frontiers, not forcibly relabelled as evidence boundaries. The implementation composite frontier and DEC-EXEC readiness route require explicit canonical mappings. No route is qualified merely by a saved waiting label.

## Dependency-ordered closure packages

### MC01 — shared identity, source-role and frozen-scope contract

- **Next operation:** CONTRACT_DEFINITION. Prerequisites: pinned post-repair cone, source inventories, BR-C1 and unchanged native/Oxx contracts.
- **Addresses:** shared signatures across CUT01–05; B01–B08 source/domain schema.
- **Work:** declare finite native identity/reference and field-role registry; settle required/optional/empty frozen Action semantics; specify explicit allocation of the old acceptance cases to frozen versus later milestones. Independently resolve minimal O01 profile compatibility. Do not define positive absent facts.
- **Acceptance:** every proposed native field has a source/rule/justified absence, independently expected type/identity and negative case; ambiguity is surfaced; source-class/selector/pin coverage exact. Scope allocation cannot waive native validity.
- **New state:** shared contract signatures, not admitted runtime objects. **Unlocks MC02.**

### MC02 — Action universe and control routing contract

- **Next operation:** MIXED, meaning contract definition + source binding + specification fixtures, **no implementation**. Prerequisite MC01.
- **Addresses:** CUT01/CUT02; B01–B04/B06.
- **Work:** one common constructor and 63 instance bindings; exact statuses/current-support interfaces; typed prerequisites, goals, slots and eight request routes. Resolve the two special frontier/reentry correspondences. Declare the support references MC03 must qualify.
- **Acceptance:** 63 unique complete construction rows, exact 13/50 partition, no extra/missing action; source-backed route coverage; class-level semantic fixtures plus all concrete bindings; substitution/dangling/ambiguous/default-dependent rows reject. Unchanged O01 incompatibility blocks the package.
- **New state:** complete definition/routing contracts subject to support closure; not yet operational admission. **Unlocks MC03.**

### MC03 — reached support and governed-wait binding contract

- **Next operation:** MIXED, meaning contract/source-binding qualification only. Prerequisite MC02 signatures and fixtures.
- **Addresses:** CUT03/CUT04 and completion of CUT01/CUT02 support; B02–B07.
- **Work:** finite reached-support fixed point; exact currentness/context/knowledge/predicate joins; retained O08/O09 profiles; canonical external-resolution source body and legacy derivation. Check provisional MC02 references against this closed support set.
- **Acceptance:** independent positive, unresolved, absence and negative fixtures; all references resolve; current historical knowledge remains distinct from completion; stale support fails after reload; wrong envelope/route/source fails; all eight source routes preserve exact branch kind; unknown budget rule remains unknown and resume false.
- **New state:** jointly complete CUT01–04 contract candidates. **Unlocks MC04.**

### MC04 — baseline certificate and integrated contract qualification

- **Next operation:** QUALIFICATION of specifications/oracles. Prerequisite MC03. No compiler, actual migration or real frozen readiness execution.
- **Addresses:** CUT05 plus integrated closure of CUT01–04; B08 and inherited pins.
- **Work:** define initial=current canonical baseline, empty new events, policy and source closure; finish FrozenControlProof verification obligations; execute independent specification fixtures and complete preflight at pinned identities.
- **Acceptance:** five contract-completion records PASS; field/source/reference coverage exact; independent C1–C5 expectation derived from facts; negative omission/substitution/staleness/cross-envelope cases; executable cold/determinism/invalidation oracles; no semantic input or conflict remaining in the cone.
- **New state:** M01 minimum-state **contract** milestone complete. **Unlocks M02 gate evaluation**, not M02 execution or migration qualification.

These four packages are the smallest supported grouping here by shared contract boundary; no mathematical minimality claim is made. MC01 prevents repeated identity/scope redesign, MC02 defines routing seeds, MC03 closes the support fixed point, and MC04 proves their composition. Combining them into one opaque task would hide these prerequisite checks. No package presently contains implementation work. M02 begins compiler implementation only after their contract gate passes.

## Mechanical exit and M02 gate

For each CUT, a completion record must identify pinned contract/source/oracle/fixture identities; required-field coverage; source joins; native admission handoff; positive/negative results; invalidation/reload expectations; no unresolved required semantic field; and all referenced completion records. A count or manually written PASS flag alone is not a completion record.

```text
M01_MINIMUM_STATE_CONTRACT_COMPLETE =
    CUT01_contract_complete AND CUT02_contract_complete
    AND CUT03_contract_complete AND CUT04_contract_complete
    AND CUT05_contract_complete
    AND transitive_source_and_field_coverage_complete
    AND native_and_O01_compatibility_preserved
    AND minimum_scope_allocation_accepted
    AND independent_contract_qualification_passes

M02_READY = M01_MINIMUM_STATE_CONTRACT_COMPLETE
    AND all_required_migration_oracles_executable
    AND no_unresolved_semantic_input_in_minimum_cone
    AND no_contract_conflict
```

Only transitive prerequisites of those five interfaces enter this predicate. Full historical result migration, future positive evidence, complete historical graph and unrelated 35-target completion do not. The old migration acceptance-case MC01/02 recognition/disposition rules remain for required sources; MC03/06 admission/composition remain for retained native state. MC04/05 result/history requirements are allocated to current-support preservation now and complete historical reconstruction only before its later required use. MC01 package must make that scope allocation explicit; this plan does not silently mark it accepted or mutate the authoritative historical matrix.

Future work remains tracked: synthetic positive reentry must qualify actual received proof/receipt validation/accepted reentry and named eligibility in a clone; actual Phase B needs real current evidence and C03 plus required correction/readiness/review gates; effecting execution needs complete applicable result/effect/authority contracts. Full historical ledger/result reconstruction and non-control graph material stay in the broader migration roadmap where independently required, outside this milestone. They cannot be represented as already qualified by minimum-state success.

```text
CUT_MEMBERS = 5
CUT_DEPENDENCY_EDGES = 13 (companion enumerates)
ROOT_CUT_MEMBERS = [SCC(CUT01,CUT02,CUT03)]
SHARED_ROOT_CAUSES = [typed source-role/reference projection, reached support/currentness closure, independent minimal-profile/composition oracle]
ACTION_UNIVERSE_GAP = 63 common-core records; minimal native/O01 semantic bindings and current-support admission incomplete
ACTION_FIELDS_REQUIRED_NOW = all 16 native fields require justified representation; control-relevant content enumerated above
ACTION_FIELDS_DEFERRED = richer future result/ranking/effect/dossier content outside retained closure, not unvalidated native fields
SOURCE_BINDING_GAPS = [B01,B02,B03,B04,B05,B06,B07,B08]
PROOF_SUPPORT_GAPS = [reached predicates/knowledge/context/current completion, retained O08/O09, source invalidation]
OPERATIONAL_GRAPH_GAPS = [exact typed routing/reference crosswalk, reached support fixed point, ordering correspondence]
CLOSURE_PACKAGES = [M01-MINIMUM-CLOSURE-1/MC01, MC02, MC03, MC04]
FIRST_PACKAGE = M01-MINIMUM-CLOSURE-1/MC01
M01_MINIMUM_STATE_CONTRACT_COMPLETE = NO
M02_READY = NO
PLANNER_CONTROL_DEFECT = CLOSED
V0_1_CURRENT_STATUS = CORRECTION_REQUIRED
IMPLEMENTATION_MODIFIED = NO
REAL_E1_EVIDENCE_CREATED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
```

Validation is planning/inventory validation only: five cut records, 13 dependency edges, four acyclic packages, all 16 Action fields and eight binding families accounted for; source pins, local links and JSON checked. No runtime test or migration package was executed. All pre-existing captured implementation/planning/backlog files and all 10,911 E1 file paths/content hashes remain unchanged. `git diff --check` and new-artifact whitespace checks PASS.
