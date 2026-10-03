# E1 legacy migration boundary decision 1

**RECOMMENDED_ARCHITECTURE = ADOPT_LEGACY_MIGRATION.** Treat frozen E1 as a versioned legacy source format, compile its required operational contracts into a canonical Planner v0.1 snapshot, and admit that snapshot through the existing strict planner boundaries. Normal runtime restoration should consume canonical state. It should not repeatedly interpret historical report layouts.

This changes the ingestion boundary, not the acceptance bar. Migration cannot close missing semantic bindings merely by assigning new identities. The current0/63 Action admissions and0/3 complete result projections remain unresolved qualification gaps. This decision authorizes no implementation, E1 resume, admission waiver or restoration of QUALIFIED status.

## Actual qualification requirement

The supported answer is **B, with represented reentry obligations retained**: deterministically reconstruct the minimum canonical operational state needed to reproduce the frozen suspension and preserve its supported future reentry contracts. It is not A, generic direct ingestion of every historical E1 artifact. It is also not a four-label checkpoint emulator.

The governing evidence is explicit:

- [Backlog R15 and acceptance N](../backlog/DETERMINISTIC_REASONING_PLANNING_RUNTIME.md): persist graph, plan, ledger, policy, authorities, unresolved conditions, waiting/receipt/reentry routes and resume dependencies; verify identities and restore without conversation history. Isolated accepted-evidence reentry must be qualified, not executed against frozen E1.
- [Implementation plan, graph/ingestion design and P06](DETERMINISTIC_PLANNER_V0_1_IMPLEMENTATION_PLAN.md): use reviewed JSON-pointer/section mappings; do not interpret prose at runtime or feed expected actionable lists into the algorithm. Planner-native bundles are supported. Full cold resume and isolated accepted-receipt reentry are required.
- [Correction plan C06, section6 and N-REAL](DETERMINISTIC_PLANNER_V0_1_CORRECTION_PLAN_1.md): use a finite versioned structured importer, restore actual operational contracts, distinguish historical attempts from current holds, and preserve explicit unsupported reasons. Opaque records cannot replace operational predicates. Required supported contracts must work in isolated positive tests; marking everything unsupported cannot qualify the runtime.
- The [frozen resume manifest](../experiments/E1/E1_RESUME_MANIFEST_1.json) binds exact plan/graph/ledger/state/policy identities and defines receipt/reentry rather than assuming new evidence exists.

Thus migration is compatible with the existing architectural direction. It makes the already-required reviewed normalization an explicit compatibility boundary. The current [17-element restoration contract](DETERMINISTIC_PLANNER_V0_1_C06A_REMAINING_CONTRACT_1.json) remains the coverage floor until a separately justified reconciliation changes it. Merely reproducing MIXED_WAIT cannot waive O01, proof admission or future-reentry tests.

## Historical source classification

Classification is by semantic role and reference closure, not extension, filename or presence under E1. One artifact can contain several roles; classify fields where necessary. The10,911-file preservation inventory is not the planner's operational object inventory.

| Class | E1 source families / examples | Migration disposition |
|---|---|---|
| CANONICAL_OPERATIONAL_SOURCE | Already accepted content-identified domain objects, issued authority records, exact subject identities, policy bytes | Reuse authenticated domain content/identity where its governing contract already defines them. These are not necessarily native Planner snapshots. No native complete Planner v0.1 snapshot has been established in the frozen inputs. |
| LEGACY_OPERATIONAL_SOURCE | Resolution plan/action definitions, embedded ledger/state, typed graph, decision/dossier reports, acceptance and prerequisite records | Versioned schema adapter produces typed operational objects and derivation records. Reports supplying a current rule belong here for that rule, not merely in an archive. |
| PROVENANCE_ONLY | Source locations, extraction methods, original report text surrounding normalized claims, source code locations cited as evidence | Retain immutable references/hashes and necessary selectors; load operational clauses separately. Do not execute cited code or hydrate every historical byte into planner state. |
| HISTORICAL_EVIDENCE | Earlier candidates/rejections, previous action attempts, old policy/snapshot references, superseded observations | Preserve original identities and temporal context. Include attempts affecting current holds/knowledge in the ledger; other history remains referenced. Never promote old observations to current proof. |
| EXTERNAL_GATE_RECORD | Handoff bundles, budget request contract, receipt/reentry routes and known-absence declarations | Restore required propositions, producer competence constraints, request/receipt/reentry identities and waiting states. Do not synthesize the missing evidence. |
| NOT_REQUIRED_FOR_RESUME | Artifacts/sections with no dependency on current operational contracts, their provenance, or represented reentry requirements | Exclude from operational loading with an explicit coverage reason; preserve bytes in the frozen archive. |

The existing CE-02 inventory identifies nine source classes—PLAN, GRAPH, MANIFEST, HANDOFF, CHECKPOINT, DECISION_AUTHORITY, PROFILE_CANDIDATE, INVOCATION_CANDIDATE and GOVERNED_TEXT—and16 assigned source artifacts/2,733 field records for its bounded slice. That inventory is reusable; it is not evidence that every other E1 artifact is unnecessary. The manifest also references23 result artifacts and other operational dependencies.

This decision classifies source families and defines disposition rules; it does not claim a newly completed per-file dependency census. Migration qualification must enumerate the transitive required-source closure and account for every manifest member. A required rule hidden in a nominally descriptive section cannot be excluded as provenance-only. Unknown required schemas or omitted dependencies fail closed.

## Minimum canonical state and exact frozen target

Use existing typed model, identity, provenance, gates and persistence abstractions. The name `PLANNER_SNAPSHOT_V0_1` below is a target contract name, not a newly implemented file format. Its eventual concrete schema must bind the existing codec version rather than introduce a parallel planner model.

| Canonical category | Required supporting operational state |
|---|---|
| Action definitions | Preserve all63 inventoried definitions and116 declared prerequisite edges under the current coverage contract. Keep operation, stage, effect, scope, authority/evidence/knowledge requirements and bounded output contracts distinct. Do not discard blocked actions to obtain an empty actionable set. |
| Attempts and current state | Preserve the24 recorded ledger entries in causal order, their source identities and outcome meaning. Reconcile current holds/overrides independently;13 completed and50 blocked are comparison summaries, not imported gate facts. |
| Accepted knowledge | Exact claims, types, accepted source bindings and validity dependencies, including non-PASS knowledge. REEVAL-BUDGET's BLOCKED outcome may support accepted knowledge without becoming COMPLETED. |
| Root obligations | Full28 tracked root/gate inventory; gate:validator_authority has its independently admitted chain;27 remain unresolved. Retain the four additional deferred top-level obligations where required by the control contract, not as invented resolved roots. |
| Slots | Full43 tracked slots and proof pipelines, including the two baseline resolved slots, authenticated_inputs.InvocationAttemptId and authenticated_inputs.profile_sha256, under their limited admitted scope. Preserve41 unresolved slots and the separate two policy-fixed inputs. |
| Graph/assertions | Typed endpoints, admitted predicates, source pins, provenance, scope and current/stale dependencies. Preserve all required assertions; do not import proposed corrections as accepted changes. |
| Decisions/authorities | Four issued Architect records and their dossiers/exclusions; Candidate-3 authority remains VALID_UNCONSUMED and candidate-only. Authority existence does not establish applicability, issuance/use or readiness. |
| Evidence/source validity | Required propositions, source-domain distinctions, currentness and stale dependency propagation. Raw file hashes, canonical embedded hashes and governed object identities remain distinct. |
| External gates | Eight active request bundles, no evidence received, exact receipt/reentry routes and producer constraints. Keep latent eligibility obligations distinct from the current frontier. |
| Waiting branches | Budget WAITING_FOR_EXTERNAL_EVIDENCE; seven other missing-fact control-transfer points; downstream contract/mapping/implementation branches DEPENDENCY_BLOCKED. Preserve reasons rather than merging every branch into one wait. |
| Decision readiness | Dossier completeness and factual-input predicates. DEC-EXEC is not decision-ready; implementation input is FACT_BLOCKED. Historic AUTHORITY_REQUIRED does not create a current human-ready action. |
| Policy | Bound selection-policy identity/version, operation/stage priorities and total tie-break semantics. Unsupported criteria remain nondecisive, not inferred scores. |
| Ledger/overlay | Canonical source-linked history plus accepted current overlay, graph/context/policy binding and explicit suspension restriction. Overlay cannot overwrite immutable historical outcomes. |
| Global control | Required-goal inventory, branch classifications, blocking frontier and precedence inputs sufficient to derive MIXED_WAIT. Preserve the distinction between mixed fact/external waits and a human-ready batch. |
| Resume eligibility | Accepted receipt, sufficient current proof, verified source pins, accepted reentry lineage, named-action eligibility and task/effect constraints. Saved false/true labels are not the eligibility algorithm. |

The exact target is an independently derived state satisfying:

```text
GLOBAL_CONTROL_STATE = MIXED_WAIT
RUNNABLE_INTERNAL_ACTIONS = []
DECISION_READY_ACTIONS = []
NEXT_ACTION = NONE
E1_RESUME_ALLOWED = NO
E1_STATE = SUSPENDED_EXTERNAL_HANDOFF
```

The [global-control record](../experiments/E1/E1_GLOBAL_CONTROL_RECOMPUTATION_1.json), `/global_wait_basis` and `/control_state_rule`, explains the mix: budget external wait plus seven missing-fact frontier points, no approved internal producer work, no ready human batch, and dependent implementation work. Its31 unresolved top-level classifications cover27 counted obligations plus four deferred obligations. Neither a count nor its saved MIXED_WAIT label is sufficient as algorithm input.

The manifest's eight request IDs concern budget, ancestry, approval, audit, runtime head, supervisor, executable policy and implementation. Its receipt IDs are contract endpoints, not silently inserted completed/runnable actions. The text `DEC-EXEC readiness reevaluation` must be normalized through an explicit route contract rather than accepted as an arbitrary ActionId. The latent EXT-CURRENT-ELIGIBILITY-EVIDENCE is not a ninth active independent transfer point.

Expected summaries belong in the independent qualification oracle. The migration derives predicates from source clauses, attempts, accepted decisions and gates; canonical planner recomputation derives the summaries. A migration that simply writes all actions BLOCKED would fail this requirement even if the four output labels match.

## Migration boundary

Define a versioned, non-effecting transformation:

```text
E1_LEGACY_V1 source bundle + reviewed migration contract + accepted binding evidence
    -> source recognition and strict validation
    -> semantic normalization with field provenance
    -> canonical Planner IR candidates
    -> unchanged typed admission/proof/reference/policy checks
    -> canonical snapshot + migration coverage/derivation manifest
    -> fresh-process planner recomputation
```

Compile once **per pinned source-and-contract revision**, not once forever. A changed source, migration rule or semantic binding invalidates the dependent compiled object and snapshot eligibility. Canonical state remains linked to its legacy evidence; migration is not provenance erasure.

The adapter may recognize the finite historical schema classes, normalize identities and known absences, assemble the common ActionIR, and preserve historical results. It may not invent a producer, select an Architect option, grant authority, create positive external evidence, infer applicability from compatible identities, or bypass O01/O08/O09/O16. Unknown required rules produce explicit unsupported diagnostics. Such diagnostics can be useful failure output but do not qualify the missing required contract.

### Generic versus legacy-specific work

| Generic reusable mechanism | E1_LEGACY_V1 compatibility rule |
|---|---|
| Strict parsing, typed identities, canonical encoding, hashing and reference validation | Recognize E1 schema/version discriminators and documented legacy field variants |
| Source dependency/provenance graph and transitive invalidation | Join manifest.current_plan to its raw plan identity; distinguish embedded ledger/policy hashes |
| Common plan-backed Action construction and admission | Interpret the historical plan's declaration/omission rules only when documented and reviewed |
| Typed result/knowledge records, ledger append/reconciliation | Extract legacy ledger outcomes and report claims through pinned selectors/sections |
| Canonical gate, decision, authority, control and resume models | Translate historical WAITING_FOR_EXTERNAL_INPUT terminology and route descriptions through explicit equivalence rules |

A LEGACY_SCHEMA_ADAPTER selects rules by schema/version and semantic record kind, with ActionIds only as data and references. It passes renamed synthetic instances and changed-but-supported values. A FIXTURE_SPECIAL_CASE branches on a known ActionId to mark it ready/blocked, copies expected control labels, chooses sources by filename, or fills fields from an expected profile. Those remain prohibited.

## Action and result feasibility

The63 common cores are migratable in principle using one constructor plus a versioned semantic adapter. This does not make them63 complete O01 definitions today.

| Remaining domain | Recoverability and frozen-state relevance |
|---|---|
| RESULT_BINDING | Historical outcomes and bounded criteria are recoverable; a complete prospective allowed-result/knowledge declaration is not established for every action. Some future positive payloads are unnecessary for the frozen observation, but O01-required result declarations and represented reentry acceptance remain required. Preserve an explicit unsupported rule rather than default PASS. |
| AUTHORITY_BINDING | Issued records, exclusions and predecessor constraints are recoverable. Complete outstanding conditional requirement/empty-requirement normalization still needs a governed rule. Missing grants remain explicit; they need not be manufactured to represent blocking. |
| EVIDENCE_BINDING | Source references and known missing propositions are recoverable. Classifying every reference as provenance versus operational evidence prerequisite needs reviewed semantic mapping. Required missing external facts become gate state, not migration defects or positive evidence. |
| KNOWLEDGE_BINDING | Named accepted claims and their source bindings are recoverable. Unkeyed historical inventory and omitted declaration semantics require an explicit legacy rule. A derived identifier can name an observed record; it cannot establish an absent semantic type or authority. |

Do not omit a mandatory O01 field because this particular snapshot happens to wait. A narrower read-only observational checkpoint could be useful, but it would not satisfy the current complete v0.1 restoration contract. Conversely, descriptive titles and future external payload bytes need not be loaded as operational state when they cannot affect any required predicate; keep their references/dispositions.

For the three reports, canonical result identities **should be derived by the migration layer** from a versioned, typed result representation, with the original report hash and ledger-record identity retained separately. Legacy documents need not have been authored using future Planner identity syntax. A canonical result ID names a migrated record; it does not authenticate its claims by itself.

The [latest semantic closure](DETERMINISTIC_PLANNER_V0_1_BR_C2_SEMANTIC_BINDING_CLOSURE_1.md) demonstrated that the existing three result qualification predicates pin synthetic source hashes/provenance/envelopes. Those fixtures are not a universal production identity allowlist. A reviewed real-source profile parameterization must independently bind the same semantic constraints to actual source identities. Do not rewrite historical fixtures, substitute synthetic hashes into real provenance, weaken O01, or call the parameterization complete before it is qualified. No result/knowledge type missing in the source is recovered merely by hashing the record.

## Trust and independent qualification

Every migrated object must retain original declared identity/domain, raw source hash, canonical embedded/object hash where applicable, exact source selectors, migration contract/version, deterministic transformation identity, accepted rule binding, and all supporting dependencies. Field-level derivation distinguishes direct extraction, deterministic derivation, authorized join and contract constant. Unknown provenance or an unexplained required field rejects.

Qualification must independently establish:

1. Source-class fixtures and an exhaustive required-field/reference coverage matrix, including expected absence and unsupported cases.
2. Expected typed values/proof predicates derived from governing sources before running migration, not from serialized migration output.
3. Positive and malformed/duplicate/dangling/wrong-domain/wrong-envelope/stale-source negatives, plus changed supported values and renamed identities.
4. Repeated migration under key, set/source order and hash-seed variations; causal history order remains fixed. Compare canonical object/snapshot identities and semantic state.
5. Cold canonical reload and recomputation without original Python objects or conversation history.
6. Source/rule invalidation after persistence, preserving historical facts while removing current support. Pin failure must not be repaired by rebinding altered frozen bytes as accepted.
7. Actual frozen-source, non-effecting readiness derivation compared with separately pinned manifest/handoff/checkpoint summaries.
8. Isolated synthetic positive reentry that works only after complete admitted evidence, and negative receipt/resume cases; no real E1 evidence acquisition or action execution.
9. Existing A–N, X01–X11 and correction regressions, all required17-element coverage, preservation and subsequent independent adversarial review.

No migration output is its own oracle. Checksums prove identity, not semantic acceptance. Matching the four frozen labels is necessary but insufficient.

## Options and future architecture

| Criterion | A: continue direct BR-C2…BR-C5 projection | B: explicit legacy migration |
|---|---|---|
| Semantic correctness | Can be correct with complete reviewed mappings; current partial fields remain blockers | Same admission obligations; clearer source-to-canonical boundary, no automatic semantic repair |
| Bespoke mapping | Historical layouts remain entangled with runtime ingestion/profile preparation | Historical compatibility is finite/versioned; generic canonical mechanisms are reused |
| Invention risk | Repeated profile reconstruction risks treating fixture values as authority | Derivation manifests expose missing semantics; still unsafe if compiler defaults or hard-codes outcomes |
| Maintainability | Runtime ingestion carries growing historical cases | Canonical runtime stable; adapter isolated and retired only when provenance dependencies permit |
| Qualification | Many direct paths and compositions; profile/source mismatch repeatedly rediscovered | Adds a compiler proof boundary, then reuses canonical admission/reload tests; not necessarily fewer semantic tests |
| Reuse | Some mapping utilities reusable, E1 layouts remain prominent | Canonical IR/persistence reusable; E1 semantics deliberately compatibility-specific |
| Architectural fit | Already resembles an implicit compiler, but boundary is unclear | Makes the plan's reviewed normalization/native-bundle design explicit |

Select B because it preserves source semantics and admission boundaries while separating legacy representation from operational state. Lower implementation effort is not assumed or the deciding criterion.

Future experiments should follow `artifact/knowledge ingestion -> canonical Planner IR -> governed admission -> persistent canonical snapshot`. Persist immutable attempts, accepted knowledge and current overlays as distinct canonical objects at creation time. Human/LLM proposals remain proposals until governed acceptance. Native snapshots reduce future migration needs; schema upgrades and source revalidation remain necessary. No GraphRAG, general artifact database, online authority service or autonomous retrieval is implied.

## Existing work and next work

Reuse CE-02's source classes and inventories; BR-C1's54 present bindings/eight expected absences; the common63-action model and29 literal bindings; scope/recorded-lineage normalizers; O01/O02/O06/O08/O09/O10/O16 admission and composition contracts; CE-01 source-support rules; result-history inventories; budget, stale, policy and resume regressions. Preserve all blocked attempts and partial coverage evidence.

New bounded work is required before implementation:

- Reconcile package ownership so CE-02's source/profile work becomes the legacy migration boundary, retaining BR-C4 graph and later history/composition responsibilities rather than silently moving them into BR-C2.
- Specify E1_LEGACY_V1 input closure and canonical snapshot/derivation-manifest binding to the existing codec; map the17 required elements to destinations and tests.
- Resolve the four remaining semantic domains and real-source result parameterization, explicitly separating recoverable historical schema rules from genuinely absent evidence or governing rules.
- Define independent source-to-canonical qualification fixtures and coverage, including working supported reentry contracts. Only then authorize a bounded adapter implementation and full readiness qualification.

**BR_C2_STATUS = SUSPENDED for further direct-bridge implementation under this decision; all prior BR-C2 contracts/results are preserved.** This is not a retrospective PASS or cancellation of obligations. CE-02 remains OPEN pending a reconciled migration contract and qualification. This document does not alter prior plan files, counts, F03 closure or C07 gates.

```text
REAL_E1_READINESS_REQUIREMENT = B plus enforced represented reentry contracts; not all-artifact ingestion
HISTORICAL_ARTIFACT_CLASSIFICATION = role-based six-class taxonomy; per-file transitive closure required at migration qualification
CANONICAL_RESUME_STATE = [actions, prerequisites, attempts, knowledge, roots, slots,
  graph/provenance, authorities, evidence/validity, gates, waiting branches, decisions,
  policy, ledger/overlay, goals/control, resume proof]
DIRECT_BRIDGE_ASSESSMENT = technically possible; implicit legacy normalization boundary remains unclear
MIGRATION_ASSESSMENT = supported architecture; semantic completeness not yet established
RECOMMENDED_ARCHITECTURE = ADOPT_LEGACY_MIGRATION
EXISTING_BR_WORK_REUSED = [source inventory, BR-C1 bindings, ActionIR/core, literal rules,
  admitted predicates, result inventories, CE-01, budget/policy/stale/resume tests]
NEW_WORK_REQUIRED = [versioned migration/coverage contract, missing semantic rules,
  real-source result profiles, independent migration qualification, bounded implementation]
BR_C2_STATUS = SUSPENDED
CE_02_STATUS = OPEN
C06A_3_RETRY_ALLOWED = NO
C07_RETRY_ALLOWED = NO
V0_1_CURRENT_STATUS = CORRECTION_REQUIRED
IMPLEMENTATION_MODIFIED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
```

Validation: all10,911 frozen E1 paths and byte hashes remain unchanged against the pre-task inventory; all other pre-existing protected files are unchanged. Only this decision document was added. Relative links, whitespace and `git diff --check` pass. No migration, readiness test, planner action or implementation test was executed.
