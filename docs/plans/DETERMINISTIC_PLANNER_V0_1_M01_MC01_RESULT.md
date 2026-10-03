# M01 minimum-state MC01 result

**RESULT = PARTIAL; MC02_READY = NO.** Shared identity, recorded frozen scope, source-role restriction and binding qualification are defined below. The reused BR-C1 source relationships pass. The authoritative package also requires resolved source-to-native signatures and minimal Action/O01 compatibility; those remain incomplete. No native admission or restoration is inferred from a valid source pin.

This executes only `M01-MINIMUM-CLOSURE-1/MC01` from the [closure plan](DETERMINISTIC_PLANNER_V0_1_M01_MINIMUM_STATE_CLOSURE_PLAN_1.md). It does not execute MC02–MC04, migration M02, or a compiler. The native unknown-rule repair remains CLOSED. No implementation, registry, prior contract/result or E1 file changes.

## Package verification and artifacts

MC01 addresses shared prerequisites of CUT01–CUT05, binding families B01–B08, and the root dependency component CUT01/CUT02/CUT03. Its assigned work is a finite identity/reference registry, source-role schema, frozen scope allocation, required/default/empty Action semantics and unchanged O01 compatibility. Its acceptance demands independent pin/domain/selector/disposition coverage and resolved source-to-native signatures; enumerating missing signatures alone does not satisfy acceptance. Its expected output is shared signatures, not completed cut interfaces.

Inputs include the post-repair dependency/cut/readiness companions, original minimum-state analysis, accepted control repair, Action normalization/semantic closure, BR-C1 and the existing Oxx admission contracts. Reuse does not authorize changing any predicate.

New machine-readable artifacts:

- [Shared identity/source-role/scope contract](DETERMINISTIC_PLANNER_V0_1_M01_MC01_CONTRACT.json).
- [Complete known binding inventory and source-role rows](DETERMINISTIC_PLANNER_V0_1_M01_MC01_BINDINGS.json).
- [Qualification fixtures and reference wrapper](DETERMINISTIC_PLANNER_V0_1_M01_MC01_FIXTURES.json).
- [Validation, reproducible read-only runner and readiness](DETERMINISTIC_PLANNER_V0_1_M01_MC01_VALIDATION.json).

The contract pins the unchanged BR-C1 contract and fixture identities. Its source locators are resolved only from that independently supplied registry. Filenames do not determine roles. Qualification uses pinned historical bytes and BR-C1's explicitly synthetic CURRENT_AT_PINNED_SNAPSHOT premise; it does not create real currentness evidence.

## Identity contract

There are 32 identity-domain/role descriptors. They distinguish native identities from recorded legacy references; descriptors marked unresolved do not issue native identities.

| Domain family | Canonical form / equality | Source/target boundary |
|---|---|---|
| ActionId, ConditionId, SlotId, KnowledgeId, AssertionId, EntityId, PredicateId, GateId, EvidenceId | Exact typed nonempty string; equality requires same type and value; no trimming or prefix guessing | Exact source identity/selector plus approved mapping. A missing typed crosswalk remains unresolved |
| ArtifactIdentity | `(IdentityKind, namespace, lowercase SHA-256)`; all three components participate | Seven existing native kinds retained: content, authority, instance, release, canonical object, WorkAuthorization and binding digest |
| Raw source content | Exact unmodified bytes and raw content domain | Neither a source locator nor a declared semantic authority identity |
| Extracted ledger/state/policy | Existing BR-C1 EXTRACTED_JSON_VALUE identity of the selected canonical JSON value | Not the raw plan digest; ledger, embedded policy and policy-document roles remain distinct |
| Runtime, controller store/G4, profile, invocation, dispatch, context, release, budget authority | Exact `SUBJECT_REFERENCE:<role>` tag and recorded manifest value | Retained as recorded references. No automatic conversion to native authority/instance/proof merely because a digest matches |
| Graph | Pinned source identity plus graph role and selected entity/assertion identity | Graph artifact identity is not a native EntityId or proof |
| Proof and OperationalBinding | Existing target-specific PredicateId/AssertionId/EntityId or explicitly governed ArtifactIdentity | Real-source native signatures remain unresolved; no invented “proof hash” or binding object |

Every row retains source pin, selector, governing binding/version, target domain and dependencies. Equal-looking hashes across kinds, namespaces, roles or selectors never imply equivalence. Unknown native namespace or identity conversion rejects rather than copying the printable digest. Source inventory recognition is not native proof admission.

## Source roles and exact frozen scope

All 37 explicit BR-C1 source payloads are inventoried with identities, governing references and allowed roles. The role contract authorizes only the following recorded relationships:

- Plan: ACTION_DEFINITION_SOURCE, ROUTING_SOURCE and LEDGER_SOURCE, selected separately. A planning/selection record does not establish execution, completion, result or knowledge.
- Manifest: FROZEN_ENVELOPE_SOURCE, SOURCE_INVENTORY_SOURCE and EXPECTED_ABSENCE_SOURCE.
- Checkpoint: FROZEN_CHECKPOINT_SOURCE and EXPECTED_ABSENCE_SOURCE.
- Handoff and incorporated budget request: EXTERNAL_GATE_SOURCE; handoff also supports EXPECTED_ABSENCE_SOURCE.
- Graph: GRAPH_SOURCE, without asserting native projection or accepted proof.
- Independently checkpoint-bound policy document: SELECTION_POLICY_SOURCE, distinct from embedded policy.
- Four pinned records with `E1-ARCHITECT-DECISION-AUTHORITY-1` schema and decision/issuer/scope/source/exclusion fields: AUTHORITY_RECORD_SOURCE. This admits their declared bounded records, not current applicability or effects.
- Other referenced reports/subjects: PROVENANCE_ONLY_SOURCE at this shared layer. Their raw references are authenticated, but operational claim/proof roles require the independent semantic selectors and source-to-native signatures. This does **not** declare those reports unnecessary for the eventual reached support cone.

A source can have multiple roles only through these independently enumerated governing relationships. The role wrapper rejects an arbitrary role change even when bytes/hash remain correct. “Authority record source” is deliberately narrower than “authority applicable to a gate.”

The contract retains BR-C1's exact frozen context and all subject pins. In particular:

- source scope: `LIVE_R4/G4/E1-WP-001/FIRST_PROGRAMMER_EXECUTION`;
- target scope: `LIVE_R4/G4/E1-WP-001/FIRST_PROGRAMMER_REQUEST`;
- recorded lineage: `R4-final CURRENT UNIQUE`;
- exact checkpoint, manifest, plan and graph content identities;
- exact runtime, controller-store generation, ProgrammerProfile, invocation, dispatch, context, release and budget authority references;
- separate extracted ledger, embedded policy and policy-document identities.

These are recorded checkpoint relationships, not a new assertion of live validity. Source/target scopes must not be equated. Historical validity outside this context cannot support current proof. Recorded lineage wording does not prove freshness. Native `EvaluationContext` scope/lineage/generation correspondence still requires an explicit mapping; MC01 does not invent that mapping from the words R4/G4.

## Binding semantics and BR-C1 reuse

A permitted source-role binding requires exactly one independently registered source identity, permitted role, exact frozen context and target relation. The source and target domains, selector, any join, dependencies and provenance must match. Duplicate candidates, ambiguous correspondence, wrong source/target/domain/context or stale support reject. Currentness is source validity at the pinned checkpoint, never positive subject applicability.

BR-C1's 54 present bindings are reused unchanged: 37 raw identities, three extracted ledger/state/policy identities, 11 recorded subject references and three hold-input bindings. Its exact join rules and independent admission checks remain authoritative. Candidate output is compared with independently fixed targets; candidate-derived expected identities do not count as qualification.

All B01–B08 signature requirements are recorded separately:

| Binding family | Shared relationship now available | Remaining native signature |
|---|---|---|
| B01 plan/actions | Plan pin, selector/ActionId source and complete inventory context | Minimal native/O01 field-role and requirement mapping |
| B02 current status/support | Recorded state/ledger pins and bounded hold inputs | Complete source-backed current-completion/hold support |
| B03 goals/slots/routing | Source graph/plan identity and routing provenance | Typed condition/slot/predicate and conditional route crosswalk |
| B04 eight routes | Exact expected-absence request/handoff/receipt/reentry joins | Native gate/requirement/held-action mapping; special composite/readiness routes |
| B05 authority/slot proofs | Pinned source records and O08/O09 target-specific requirements | Reached real-source native proof parameterization |
| B06 accepted knowledge | Producer/report/source references without producer-completion inference | Accepted claim, KnowledgeId/type and current support mapping |
| B07 governed unknown | Pinned external request and frozen envelope; repaired native contract available | Independently derived canonical resolution-contract body, source pin and native consumer correspondence |
| B08 baseline/certificate | Policy/checkpoint/source inventory identities | Complete native baseline and proof-reference signatures |

These requirements are evaluated as AMBIGUOUS target signatures, not silently labelled BOUND. BR-C1 provides the generic mechanism; B01/B03/B05/B06/B07 additionally need semantic role interpretation. No missing external positive evidence is demanded to resolve them.

## Eight expected absences

All eight existing source-level absence contracts pass unchanged: BUDGET, ANCESTRY, APPROVAL, AUDIT, RUNTIME-HEAD, SUPERVISOR, EXEC and IMPLEMENTATION. Each companion record contains exact request identity, missing proposition, expected owner/source class, frontier, receipt action, reentry declaration, source-specific scope/lineage/currentness and manifest/handoff/checkpoint provenance.

The premise is `evidence_received=false` plus the exact matching handoff/receipt route. Positive evidence is null and positive reentry false. Missing an authoritative *present* source remains malformed; missing the explicitly requested external evidence is a valid expected absence. The eight records do not fabricate producer endpoints or evidence entities.

BR-C1's generic wait label is not a native branch-kind mapping. Budget's evidence frontier and the seven factual frontiers retain their separate governing semantics. In particular, `DEC-EXEC readiness reevaluation` remains a source declaration, not an automatically constructed ActionId; the composite implementation frontier remains explicitly unresolved for native projection. B04/B07 carry these downstream requirements.

## Action compatibility and scoped acceptance

The authoritative MC01 package includes an O01 compatibility decision; it is not legitimate to defer that prerequisite simply because MC02 will later instantiate actions. Existing O01 requires exact independently reviewed result contract, authority/evidence/knowledge requirements, scope, lineage and provenance. Native Action has required field/type/reference obligations even on held paths. No canonical partial-Action type or approved omission rule was established in the inspected contracts.

The decision supported here is **no implicit omission/default conversion**. All 16 native Action field requirements from the closure plan are retained. A source-backed None/empty value is permitted only under a governing field rule; a Python default is insufficient. Existing explicit empty knowledge declarations and definition-scope/recorded-lineage rules may be reused. The remaining default/empty and source-role interpretation for required result/authority/evidence/knowledge fields is not established. A complete minimal expected O01 profile therefore cannot be signed off here without inventing semantics.

Scope allocation is explicit: old acceptance-case MC01/02 recognition/disposition and MC03/06 native admission/composition apply to retained state; MC04/05 apply to current source-backed support now. Full passive history and future positive/effecting detail outside the control cone remain later work. This allocation does not waive a mandatory native/O01 field. The unresolved minimal profile, rather than all-35-target completion, prevents MC01 PASS.

## Qualification and cross-contract consistency

Executed specification checks:

- 54 present bindings and eight expected-absence records passed unchanged BR-C1 project/admit.
- **16 negative cases PASS:** wrong identity domain; same digest/wrong target type; changed source bytes; wrong role; wrong scope; historical source promoted to current proof; wrong lineage; stale source; duplicate correspondence; different runtime envelope; missing present source; unsupported role; missing absence/gate record; invented evidence; wrong receipt route; provenance loss.
- **37 invalidation cases PASS:** independently stale each required source, reload the candidate and require rejection.
- Canonical JSON round-trip and reversed input record order retain admission.

The validation companion includes actual rejecting clauses and a read-only reproducible runner using the pinned BR-C1 source fixture. The currentness view is synthetic qualification data. These are contract checks, not Planner restoration tests or a rerun of every Oxx suite.

Static handoff consistency:

| Contract | Preserved rule / limit |
|---|---|
| O01 | Source reference/role does not admit a complete definition; exact required fields remain mandatory |
| O02/O06 and CE-01 | Supporting source payloads retained; historical completion and current proof separate; holds do not invalidate independently accepted knowledge |
| O08 | Preparation, dossier/decision and bounded authority chain still required; authority-record role does not satisfy the gate |
| O09 | Exact baseline slot-specific admission still required; source/value existence does not resolve a slot |
| O10 | Source graph role is not operational projection; mandatory source payload and provenance retained |
| O16 | Individually bound references cannot bypass shared-envelope composition or missing members |
| Repaired unknown-rule gate | Exact independently admitted resolution contract still required; generic absence/wait label is insufficient |
| C03 resume | No positive proof, accepted reentry event, named eligibility or permission is created by binding |

No weakening/conflict was established by these restrictions. Complete native cross-oracle composition remains unexecuted and cannot be claimed PASS from source-level checks.

## Coverage, remaining work and readiness

The known binding inventory contains **70 rows**: 54 reused present bindings, eight expected absences and eight unresolved B01–B08 native signature records. Counts use those rows, not unique files or all eventual native entities. The 37 source payloads and their allowed roles are a separate complete registry of the reused BR-C1 inventory.

This is not proof that the final reached support inventory contains only those 37 payloads or 70 bindings. Exact membership depends on the unresolved native reference signatures. Potential proof sources are retained as provenance until their operational role is independently defined; no source is silently dropped or converted into evidence.

Two MC01 acceptance gaps remain:

1. **MC01-01:** minimal native Action/O01 compatibility and justified optional/empty semantics for mandatory result/authority/evidence/knowledge fields.
2. **MC01-02:** complete minimum-cone source-role/target-signature inventory for B01–B08; source pins alone do not settle operational role or exact native identity conversion.

These are shared interface prerequisite gaps, not a request to execute MC02's constructor or MC03's proof restoration. Each CUT receives generic identity-domain discipline, exact recorded envelope and reusable source bindings; none receives a fully resolved native signature. The readiness companion marks IDENTITY_READY and SOURCE_ROLE_READY as PARTIAL, FROZEN_SCOPE_READY as RECORDED_ENVELOPE_ONLY and SOURCE_BINDING_READY=false for every CUT.

`MC02_READY = MC01 acceptance complete AND shared target signatures resolved AND scope/native/O01 compatibility established AND required role/source inventory complete AND independent cases pass`. The last condition passes for the bounded common bindings; the preceding completion conditions do not. NEXT_PACKAGE is continued MC01 signature/compatibility closure, not MC02.

```text
WORK_PACKAGE = MC01
RESULT = PARTIAL
CUT_MEMBERS_ADDRESSED = [CUT01,CUT02,CUT03,CUT04,CUT05] shared prerequisites only
IDENTITY_DOMAINS = 32 descriptors; native, recorded-reference and unresolved target distinctions retained
SOURCE_ROLES = enumerated in contract; no filename-derived roles
FROZEN_SCOPE = exact BR-C1 pinned checkpoint envelope; not live applicability
INSTANCE_COVERAGE = {BOUND:54, EXPECTED_ABSENCE:8, PROVENANCE_ONLY:0,
 AMBIGUOUS:8, UNSUPPORTED:0, MISSING_REQUIRED_SOURCE:0}
INSTANCE_COVERAGE_LIMIT = 70 known binding rows; complete reached native inventory unresolved
NEGATIVE_CASES = 16 PASS
SOURCE_INVALIDATION_CASES = 37 PASS
CROSS_CONTRACT_CONSISTENCY = no weakening established; complete native composition pending
MC02_READY = NO
NEXT_PACKAGE = MC01 remaining signature and minimal-O01 compatibility closure
M01_MINIMUM_STATE_CONTRACT_COMPLETE = NO
M02_READY = NO
PLANNER_CONTROL_DEFECT = CLOSED
V0_1_CURRENT_STATUS = CORRECTION_REQUIRED
IMPLEMENTATION_MODIFIED = NO
REAL_E1_EVIDENCE_CREATED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
```

Preservation: all 10,911 frozen file paths and SHA-256 hashes, and all captured pre-existing implementation/planning/backlog files, are unchanged. New JSON/links and whitespace checks and `git diff --check` PASS. No historical artifact is rewritten.
