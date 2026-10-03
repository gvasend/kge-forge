# Deterministic Planner v0.1 — Implementation Plan 1

Status: design only; no implementation authorized by this document. Scope: a small deterministic Python planner, local replay harness, and E1 acceptance A–N. E1 remains SUSPENDED_EXTERNAL_HANDOFF, with no resumption permission. All fixture mutations occur in isolated copies outside `docs/experiments/E1/`.

Requirements: [architectural backlog](../backlog/DETERMINISTIC_REASONING_PLANNING_RUNTIME.md) and [E1 traceability](../backlog/DETERMINISTIC_REASONING_PLANNING_RUNTIME_E1_TRACEABILITY.md). Test contract: [acceptance matrix](DETERMINISTIC_PLANNER_V0_1_ACCEPTANCE_MATRIX.md).

OBSERVED_E1_FINDING means an artifact-recorded event or specification, not a qualified planner implementation. This plan is SUPPORTED_ARCHITECTURAL_INFERENCE. Performance, scalability, globally optimal scheduling/cuts and broad generality remain UNTESTED_ARCHITECTURAL_HYPOTHESIS. No semantic extraction, LLM calls, external service, database, UI, authority issuance, or production executor is needed for v0.1.

## 1. Requirement slice and classification

Classification applies to the bounded subrequirement named in each row. A required area does not pull its broader automation ambitions into scope. Every numbered backlog area is covered here; the following legacy-section and original-acceptance crosswalk covers the requirements predating R01–R24.

| Area | Classification | Minimum v0.1 obligation | Cases |
|---|---|---|---|
| R01 | V0_1_REQUIRED | Typed action state; independent outcome/knowledge/root/slot dimensions | C,E–N |
| R02 | V0_1_REQUIRED | E1 selector, deterministic fallthrough and trace | D,I,L |
| R03 | V0_1_REQUIRED | Accepted knowledge and explicit incomplete facts, source fingerprint | E–H,N |
| R04 | V0_1_REQUIRED | Decision readiness independent of authority need | F–I |
| R05 | V0_1_REQUIRED | Explicit decision-input routes driven by supplied accepted dossiers | F–H |
| R06 | V0_1_REQUIRED | Machine-work priority and independent human review batch | I |
| R07 | V0_1_REQUIRED | Bounded fact outcomes and append-only reentry | J–N |
| R08 | V0_1_REQUIRED | Identity, applicability and freshness are separate gates | J,N |
| R09 | V0_1_REQUIRED | Typed evidence obligations; known-rule/missing-evidence distinction | F,H,J,K |
| R10 | V0_1_REQUIRED | Receipt contract and external evidence lifecycle in replay | K–N |
| R11 | V0_1_REQUIRED | Branch-local wait and independent work | L,M |
| R12 | V0_1_REQUIRED | Deterministic global control classification | I,K–N |
| R13 | V0_1_REQUIRED | Current control-transfer frontier, not every blocked descendant | M,N |
| R14 | V0_1_SUPPORTING | Read existing handoff bundle contracts; generic package generation deferred | K,M,N |
| R15 | V0_1_REQUIRED | Verified persisted restore; resume predicate; no history dependency | N |
| R16 | V0_1_REQUIRED | Typed invariant/route defects, fail closed and replay | C,D,F,M |
| R17 | V0_1_REQUIRED | Tagged identities, no hash-shaped substitution | A,B,J,N |
| R18 | V0_1_REQUIRED | Explicit producer/source/contract gates; Candidate-2 actual rejection | A,B,E,H |
| R19 | V0_1_REQUIRED | Pure-only validation registry and reject effecting-only qualification | A,B,J; invariant X09 |
| R20 | V0_1_REQUIRED | Exact provenance; pinned fixture assertions; stale-source invalidation | A–N |
| R21 | V0_1_REQUIRED | No probabilistic fallback on empty actionability | M,N |
| R22 | V0_1_REQUIRED | Fourteen replay cases and negative variants | A–N |
| R23 | V0_1_SUPPORTING | Exact evidence inventory and epistemic labeling | A–N |
| R24 | V0_1_REQUIRED | Frozen-source, authority and production preservation | A–N |

Numbered-area count: 22 V0_1_REQUIRED, 2 V0_1_SUPPORTING, 0 wholly deferred. Ten larger subcapabilities are explicitly deferred below; this is not a plan to implement all of each required area's architecture.

| Earlier backlog section / obligation | Classification and bounded disposition |
|---|---|
| Purpose; scope; preservation | V0_1_REQUIRED: deterministic operations and authority separation (all cases). Broader runtime integration is D10. |
| Artifact-to-knowledge synchronization | V0_1_REQUIRED: identity/location verification, accepted/stale status, deterministic invalidation (N,X10). V0_1_SUPPORTING: reviewed fixture extraction map. Automated semantic extraction is D01. |
| Typed graph, all assertion metadata | V0_1_REQUIRED: relation/provenance/scope/lineage/freshness/acceptance fields (C,E,J,N); optional non-applicable fields must be explicitly absent with reason. General entity resolution is D01. |
| GraphRAG ingestion/retrieval and LLM responsibilities | DEFER_POST_V0_1: D01. Import accepted facts, never infer them. |
| Six deterministic projections | V0_1_REQUIRED: prerequisite projection plus on-demand typed authority/producer/consumer/evidence/provenance queries (A–N). No six separately persisted engines. General projection framework is D09. |
| Plan Compiler preflight list | V0_1_REQUIRED: finite typed gate evaluation, missing references/producers/mappings, cycles, identity/scope/currentness, pure-validator and authority checks for these fixtures (A–C,F,H,J,N). Unknown contract/rule blocks, not a guessed evaluator. |
| Frontier/cut/seed planning | V0_1_REQUIRED: exposed boundary traversal (M). DEFER_POST_V0_1: global minimum cuts, seed synthesis and optimization D04. |
| Work routing | V0_1_REQUIRED: typed operation/executor/effect labels, pure replay and human handoff (D,I–N). Executing governed/semantic/runtime actions is D02/D10. |
| Canonical construction contracts; Template-1 | V0_1_REQUIRED: read contract requirements and identify missing sources (A,B). Actual constructors, field mapping and joint construction are D03. |
| Formal consumer validation | V0_1_REQUIRED: reuse existing pure Candidate-2 rejection and deny unqualified/effecting validators (A,X09). Full shared issuance-validator refactor and effect-path qualification are D05. |
| Persistent semantic results | V0_1_REQUIRED: supplied accepted knowledge and complete source fingerprint (E–H,N); no model/prompt evaluation runtime (D01). |
| Authority model | V0_1_REQUIRED: exact construct/issue/use/release/expand scopes and replay restrictions as read-only records (B,J,N); no delegation service or issuance (D06). |
| Evidence lifecycle | V0_1_REQUIRED: obligation/produced/validated/accepted distinction and causal gates (J–N). Real acquisition connectors are D02. |
| Deterministic runtime responsibilities | V0_1_REQUIRED: bounded identity, graph, gate, replay and transition functions listed in section 4. LLM context construction is D01. |
| Graph mutation governance | V0_1_REQUIRED: reject unsupported assertions; append accepted evidence deltas under pinned fixture policy (E,N). General proposal review/mutation UI is D09. |
| Observations and hypotheses | V0_1_SUPPORTING: fixture sources and explicit historical limits. Not additional implementation requirements; performance investigation D08. |

The original fourteen measurable criteria remain backlog obligations. Their v0.1 slice is explicit:

| Original criterion | Classification for v0.1 |
|---|---|
| 1 Pre-R4 reconstruction | V0_1_SUPPORTING: ingest reviewed known assertions; automatic reconstruction DEFER_POST_V0_1 (D01) |
| 2 Template-1 preflight | V0_1_REQUIRED B: missing authoritative Template-1 and represented field gates; no general mapping discovery |
| 3 Candidate-2 rejection | V0_1_REQUIRED A |
| 4 Dispatcher actionability | V0_1_REQUIRED C |
| 5 Joint construction | DEFER_POST_V0_1 D03; non-ordering relationships tested in X02 |
| 6 Deterministic invalidation | V0_1_REQUIRED N,X10 |
| 7 Replayable planning | V0_1_REQUIRED D,N |
| 8 Operation readiness | V0_1_REQUIRED C–N |
| 9 No premature qualification | V0_1_REQUIRED A,B,F,H,J |
| 10 Projection soundness | V0_1_REQUIRED C,X02 |
| 11 Authority separation | V0_1_REQUIRED B,J,X03 |
| 12 Evidence causality | V0_1_REQUIRED J–N,X08 |
| 13 Mutation governance | V0_1_REQUIRED accepted-fixture guard (E,N); general LLM proposal workflow D09 |
| 14 Pure consumer validation | V0_1_REQUIRED rejection guard (A,X09); complete shared effect-path implementation D05 |

Deferred capabilities (10): D01 GraphRAG/LLM extraction, semantic evaluation and context retrieval; D02 live external acquisition and messaging; D03 Template-1/Candidate-3/joint production construction and actual mappings; D04 global cut/seed or information-gain optimization; D05 WorkAuthorization shared issuance-validator repair; D06 authority issuance/delegation administration; D07 generic handoff generation/producer consolidation; D08 performance/scalability/interrupt-optimality studies; D09 general graph database, projection/plugin and mutation-review framework; D10 UI, distributed/concurrent scheduling and production execution. Optional selector metrics fallthrough is required, metric discovery/optimization is not.

## 2. Repository fit and smallest module boundary

Inspected repository: Python control-plane code and unittest convention live in [adapter](../../adapter/README.md); `src/kge_forge/context` and `tests/context` contain no tracked implementation. No existing generic graph planner, packaging manifest or planner database was found. Use `adapter/planner/` as a small pure subpackage, not a second host/orchestrator or a new language/toolchain.

Reuse [invocation_constructor.identity](../../adapter/invocation_constructor.py) for case A's real schema/identity rejection. It is a pure early validation step, not a complete consumer-acceptance certificate. [workauth_lifecycle.consume_and_issue](../../adapter/workauth_lifecycle.py) includes effects and must never be called by this replay harness. [corrected_workauth_lifecycle](../../adapter/corrected_workauth_lifecycle.py) is also an issuance boundary, not a generic planner. [workauth_issuance.validate](../../adapter/workauth_issuance.py) checks a specific issuance record, not all planner authority classes; do not repurpose it as an authority engine. Preserve these modules unchanged.

[context_projection.canonical](../../adapter/context_projection.py) uses sorted compact JSON with default ASCII escaping. E1's manifest hashes embedded ledger/policy with `ensure_ascii=False`. Reuse the existing function only for its exact artifact domain via the constructor. Define the planner snapshot codec separately with an explicit canonicalization tag; a global serializer refactor would be unsafe and unnecessary. Existing [constructor tests](../../adapter/tests/test_invocation_constructor.py) demonstrate synthetic, non-effecting fixtures and unittest mocks; reuse that testing convention, not their production host path.

Proposed files below are design targets, not files created by this task. Eight package files (including entrypoint and initializer), four test files and a fixture directory suffice.

| Proposed file | Responsibility / public API | Dependencies | Tests |
|---|---|---|---|
| `adapter/planner/__init__.py` | Narrow exports of Snapshot, recompute, select, apply_result; no initialization effects | model/core/selector | import has no I/O |
| `adapter/planner/model.py` | Frozen dataclasses/enums; schema decode validation; `validate_model` | stdlib only | test_planner_core |
| `adapter/planner/codec.py` | `load_pinned`, `canonical_bytes`, `snapshot_id`, `save_bundle`, `restore`; raw and embedded hash profiles | model, stdlib JSON/hashlib/pathlib | test_planner_resume |
| `adapter/planner/gates.py` | `evaluate_predicate`, `check_authority`, `check_receipt`, `decision_readiness`; finite pure rule registry | model; injected pinned artifact reader; constructor.identity for explicit contract check | test_planner_invariants; A,B,F–K |
| `adapter/planner/selector.py` | `select(nonempty_actions, policy, metrics) -> SelectionTrace` | model only | test_planner_core D |
| `adapter/planner/core.py` | `project`, `recompute`, `apply_result`, `apply_receipt`, `apply_recorded_decision`; propagation, frontier, control and resume gates | model/gates/selector | test_planner_core; replay E–N |
| `adapter/planner/replay.py` | `load_fixture`, `import_e1`, `run_replay`; explicit source-pointer mapping; compare computed outputs to oracle | codec/core; no network | test_planner_e1_replay |
| `adapter/planner/__main__.py` | argparse JSON CLI; one supplied event per apply; never auto-execute selected work | replay/codec/core | subprocess smoke tests in test_planner_resume |
| `adapter/tests/test_planner_core.py` | State/projection/selector tests including smallest vertical slice | unittest + planner | C,D,E and control truth table |
| `adapter/tests/test_planner_e1_replay.py` | Parameterized A–N with exact fixture source pins | unittest + replay | all 14 cases |
| `adapter/tests/test_planner_invariants.py` | X01–X11 adversarial changes, no-effect sentinels | unittest.mock + planner | all 11 invariants |
| `adapter/tests/test_planner_resume.py` | Codec, hash chains, cold-process restore/CLI tests | unittest/tempfile/subprocess + planner | N and deterministic byte equality |
| `adapter/tests/fixtures/planner_v0_1/` | `sources.json`, `policy.json`, `A.json`…`N.json`, shared typed snapshots and synthetic receipt/event files | frozen E1 source references | structural validation and fixture coverage |

No new third-party dependency, service, migration or general database. Source-reading adapters remain explicit and local. Do not import or instantiate a host, controller, resolver or network client to authenticate replay evidence. A fixture trust policy is a pinned historical acceptance contract, not current operational trust.

## 3. Minimum typed model

Use frozen dataclasses and enums; IDs are distinct validated value objects, not interchangeable strings. Collection order is meaningful only where the schema says it is. Missing, unknown, rejected and false are not the same value.

| Type | Minimum fields / invariants |
|---|---|
| ArtifactIdentity | semantic kind, namespace, algorithm, digest, identity-domain/canonicalization version; raw-file hash separately from semantic identity; no implicit conversion |
| IdentityKind | CONTENT_IDENTITY, AUTHORITY_IDENTITY, INSTANCE_IDENTITY, RELEASE_IDENTITY, CANONICAL_OBJECT_IDENTITY, WORKAUTHORIZATION_ID, BINDING_DIGEST; required domain-qualified namespace distinguishes profile/release/programmer identities |
| Provenance | artifact reference, JSON pointer or document section plus excerpt hash, extraction/rule version, acceptance record, scope, lineage, explicit validity/freshness input; no unanchored accepted claim |
| GraphEntity | EntityId, EntityKind, immutable semantic identity reference where applicable; artifact/action/condition/slot/producer/validator/evidence/authority/decision kinds |
| GraphAssertion | AssertionId, subject, Relation, object, Provenance, accepted/proposed/rejected/stale/historical status, optional ordering justification |
| RootCondition | ConditionId, independent predicate ID/inputs, derived UNRESOLVED/SATISFIED/DISPROVED/STALE state, proof references; not writable by action outcome |
| ValueSlot | SlotId, consumer path, required IdentityKind or ValueType, source/producer/mapping/validator/authority requirements, derived UNRESOLVED/RESOLVED/STALE, accepted value reference |
| Action | ActionId, branch, OperationClass, executor MACHINE/HUMAN, effect class, prerequisite predicates, permitted source/result contract, explicit reentry route and allowed knowledge delta kinds |
| ActionState | ACTION_ELIGIBLE, ACTIONABLE, SELECTED, COMPLETED, BLOCKED, WAITING; attempt ledger separate from current eligibility projection; blocked retry requires accepted relevant new input |
| ActionResult | PASS, FAIL, BLOCKED, AUTHORITY_REQUIRED, EXTERNAL_GATE_REQUIRED; result does not carry root/slot state setters |
| KnowledgeRecord | KnowledgeId, question, UNKNOWN/KNOWN_INCOMPLETE/KNOWN_COMPLETE, accepted facts/gaps/alternatives, provenance, source fingerprint; proposals remain proposals |
| OperationClass | E1 source classes plus FACT_ACQUISITION and DECISION_INPUT_ACQUISITION, explicit stage; fixed map to selector priority class, never runtime LLM mapping |
| AuthorityRequirement | exact authority class (CONSTRUCT/ISSUE/USE/RELEASE/EXPAND/IMPLEMENT_TEST/DECIDE), target, scope, lineage, validity, replay status, applicable rule and evidence; no implication among classes |
| EvidenceRequirement | RequirementId, proposition, rule-known flag, expected producer/type, identity/scope/lineage/currentness predicates, status MISSING/PROVED/DISPROVED; rule unknown is separate from missing bytes |
| DecisionReadiness | lifecycle stage plus readiness status DECISION_READY/FACT_BLOCKED/SEMANTICALLY_INCOMPLETE/NOT_READY, named predicate results and dossier reference; not approval |
| ExternalGate | GateId, branch, lifecycle stage, request/receipt/reentry IDs, required evidence set, accepted/rejected receipts; sending/arrival/acceptance are separate |
| ControlState | RUNNABLE, HUMAN_HANDOFF, EXTERNAL_WAIT, MIXED_WAIT, PLAN_DEFECT, TERMINAL_SUCCESS, TERMINAL_FAILURE |
| ResumeManifest | version; graph/plan/ledger/state/policy identities; authority/evidence references; waiting gate and reentry IDs; root/slot counts; candidate-authority status; control; bundle identity and explicit resume predicate |
| Snapshot / ExecutionEvent | Snapshot is immutable graph + state + pinned evaluation context. Event includes sequence, prior snapshot identity, action/attempt, result/evidence references, acceptance checks and resulting snapshot identity; deterministic event identity |

ValueType supports only fixture-needed JSON null, bool, integer, string, array, object and tagged references; bool must not satisfy integer. Identity typing complements source identity authentication; neither substitutes for applicability. Structural eligibility is not actionability. A human ACTIONABLE action is eligible for review only. A successful attempt becomes COMPLETED only when its own bounded acceptance passes; BLOCKED attempts may still retain separately accepted knowledge. WAITING is the current scheduling overlay and cannot rewrite the historical result.

## 4. Graph and deterministic planner core

Load reviewed, deterministic fixture assertions. Do not parse prose semantically at runtime. `import_e1` uses a versioned mapping of exact JSON pointers and section-bound normalized facts, with raw source hashes and acceptance provenance. It never uses a report's expected actionable list as its algorithm input. Historical cases must carry stage-specific assertions/events, not reuse the final graph as though all later knowledge existed earlier.

| Relationship | Required use; projection rule |
|---|---|
| REQUIRES | Prerequisite only with accepted explicit ordering justification; edge prerequisite -> dependent internally |
| PRODUCED_BY | Producer completeness checks; absence stays absent |
| DERIVED_FROM | Value/provenance dependency and stale propagation, not automatic ordering |
| AUTHORIZED_BY | Exact permission checks |
| VALIDATED_BY / CONSUMED_BY | Pure consumer-contract gate, source of acceptance criteria |
| EVIDENCED_BY | Proof support, not authority |
| BINDS / APPLIES_TO | Exact identities and scope/lineage/currentness constraints, never automatic prerequisite edges |
| HAS_SLOT / HAS_IDENTITY_TYPE | Consumer required values and semantic type checks |
| PROVEN_BY / SATISFIED_BY | Condition-to-obligation and obligation-to-accepted-evidence chain |
| CORRESPONDS_TO | Preserve semantic consistency without invented ordering; X02 requires it |

These 14 relation kinds suffice. Other frozen relations are retained as opaque provenance-only records by an explicit importer map, never dropped silently or admitted to ordering. If an unimplemented relation is needed by a satisfaction rule, report UNSUPPORTED_RULE and block; do not infer an equivalent supported relation. TRANSFORMED_BY can be represented in a slot's versioned mapping reference, with original assertion provenance retained. General relation extensibility is deferred.

Pure predicate vocabulary: all/any over named requirements; accepted-source identity; exact typed equality; authority permission/applicability; action completed; accepted knowledge contract; producer/mapping available; consumer check; complete dossier; complete receipt. Unknown rule evaluates UNKNOWN with blocker, never true. Rules are registered functions, not evaluated arbitrary Python or expressions from fixtures. Facts may be PROVED/DISPROVED/UNKNOWN; conjunction requires every operand PROVED.

| Component | Deterministic algorithm / output |
|---|---|
| 1 Prerequisite projection | Validate accepted ordering edges, references, metadata consistency and cycles; stable topological traversal. Report discrepancies, do not repair source topology. |
| 2 Actionability | Evaluate all required predicates, source/trust/scope/lineage/effect constraints and prior-attempt hold. Emit eligible/actionable/blocked reason sets; rank cannot override a failed gate. |
| 3 Action transition | Verify selected action and pre-state ID; validate result contract and each knowledge delta separately; append one event. No auto retry or next-action execution. |
| 4 Selection | Section 5; select machine work; human-only set becomes batch. |
| 5 Root propagation | Evaluate independent root predicates against accepted facts to fixed point; no result-to-root shortcut. Keep failed and missing proofs distinguishable. |
| 6 Slot propagation | Resolve only exact typed accepted value with all source/producer/mapping/authority/validator gates PROVED; root satisfaction alone need not resolve a slot. |
| 7 Decision readiness | Evaluate complete factual input/dossier checklist, not result label; produce ready, fact-blocked or semantically incomplete status. |
| 8 Decision-input reentry | Explicit accepted semantic knowledge routes to ready-check, input action, or external fact gate; original AUTHORITY_REQUIRED action remains historical. |
| 9 Fact reentry | Accept per-obligation observations; create a new attempt eligibility token only when declared prerequisite evidence changes sufficiently. Partial evidence cannot silently clear complete gates. |
| 10 Authority-reference reentry | Exact reference check plus independent applicability/currentness obligations before reevaluation; DEC-BUDGET policy is not currentness evidence. |
| 11 External gates | Apply admitted receipt contract; track each proof and lifecycle; negative/partial results persist without enabling downstream use. |
| 12 Branch suspension | Exclude only dependent actions lacking alternate satisfied prerequisite paths; independently evaluate all other actions. |
| 13 Global control | Section 7 truth table; no reasoning fallback. |
| 14 Blocking frontier | Starting from unresolved targets, follow explicit unsatisfied gate dependencies to first exposed control-transfer records; deduplicate by GateId, retain witnesses/affected targets. Do not emit all downstream blocked actions. No minimum-cut claim. |
| 15 Resume | Verify complete snapshot bundle and accepted relevant receipt/authorized change; require at least one declared reentry action actionable; restore alone never resumes. |

Recompute order: validate identities/schema -> stale dependent assertions -> evaluate predicates/root/slot fixed point -> actionability/readiness/reentry -> frontier/control -> selector. Finite positive evidence rules terminate; cycles without independent evidence cannot prove themselves. Explicit invalidation first permits states to become stale; propagation does not retain historical satisfaction as current. Terminal success requires all declared goals and acceptance gates, not empty queues.

`apply_result(snapshot, validated_result) -> TransitionReport` accepts knowledge proposals and result evidence only. `evaluate_satisfaction(snapshot) -> SatisfactionProofs` is a separate internal function; only it creates RootTransition/SlotTransition values. Deserializing an event with user-provided `root_state=SATISFIED` or `slot_state=RESOLVED` is rejected. Acceptance of knowledge and acceptance of the action's full result are distinct; a blocked implementation dossier may add accepted gaps. A forged PASS lacking its required evidence is rejected without mutation. Positive synthetic proof tests must also show that genuine independent satisfaction can propagate, so the implementation cannot pass by never resolving anything.

## 5. Selector contract

Use the [validated E1 policy](../experiments/E1/E1_GRAPH_RESOLUTION_SELECTION_POLICY_1.md), including its static decision-input extension. For each remaining tied set:

1. Maximize the complete lexicographic coverage triple: directly satisfied unresolved roots, distinct unresolved slots dependent through those roots, and blocked actions becoming eligible after this action alone passes. Compute only from explicit accepted transition rules and all gate predicates; no descendant proxy. If incomplete/inconsistent for any candidate, record CRITERION_1_NOT_DECISIVE and retain the set.
2. Maximize a comparable explicit outcome-partition/relationship-elimination score. No formal complete model means CRITERION_2_NOT_DECISIVE. v0.1 E1 fixtures have no such model; accept only validated complete metric fixtures in selector unit tests, not subjective estimates.
3. Minimize class rank: DETERMINISTIC_VALIDATION, DETERMINISTIC_CONSTRUCTION, SOURCE_ACQUISITION, DETERMINISTIC_MAPPING, IMPLEMENTATION_PREPARATION, SEMANTIC_EVALUATION, ARCHITECT_PREPARATION, RUNTIME_EXPERIMENT, GOVERNED_OPERATION. Exact E1 static mapping: SEMANTIC_RESOLUTION -> SEMANTIC_EVALUATION unless explicit DECISION_PREPARATION; decision/input preparation -> ARCHITECT_PREPARATION; FACT_ACQUISITION -> SOURCE_ACQUISITION; actual repairs/decisions -> GOVERNED_OPERATION. Unmapped class skips ranking for the tied set, never grants actionability.
4. Minimize effect rank NON_EFFECTING, QUALIFICATION_EFFECT_ONLY, PRODUCTION_EFFECT; then cost only if every remaining candidate has comparable explicit cost. Unknown effects skip ranking but fail upstream effect permission where required. Missing cost is not zero.
5. Exact case-sensitive Unicode-code-point minimum canonical ActionId, without normalization/locale. Duplicate/conflicting IDs are malformed input, not a valid actionable set.

Each criterion retains a nonempty subset; final unique minimum proves totality over finite nonempty valid action sets. A singleton returns criterion 0. All collections used as sets are sorted at serialization. No ambient time, conversation, JSON key order or input order enters selection. Freshness uses a pinned evaluation-context value and source generation, never `now()` inside ranking.

The pure selector is total even on a valid all-human set; the scheduler deliberately does not call it there. Independent machine work gets scheduled while human work waits; all-human readiness yields a batch and NEXT_ACTION = NONE. This is a control boundary, not a change to the E1 selector's ranking semantics. In E1's 15-action fixture, criteria 1/2 fall through, 3 retains five source actions, 4 ties and 5 selects S-ANCESTRY.

## 6. Decision and external state machines

Decision stages have these entry/exit requirements:

| Stage | Entry / permitted exit |
|---|---|
| SEMANTIC_GAP_IDENTIFIED | Accepted bounded gap finding; name governing question, do not infer readiness |
| DECISION_INPUTS_REQUIRED | Explicit missing-input checklist; route to bounded acquisition or external gate |
| DECISION_INPUT_ACQUISITION | Its own prerequisites and source scope hold; supplied accepted dossier can advance, absent facts set FACT_BLOCKED |
| DECISION_DOSSIER_READY | Bounded question, concrete alternatives, source pins, consequences and authority exclusions supplied; independent checklist pending |
| DECISION_READY | All decision-dependent facts/checks pass; human review allowed only |
| DECISION_RECORDED | Imported authenticated scoped human decision; never created by the planner |
| DOWNSTREAM_REEVALUATION | Reevaluate only explicit dependent routes; no automatic satisfaction |

ARCHITECT_DECISION is the human boundary between READY and RECORDED, not an automatic action. FACT_BLOCKED is a separate readiness dimension at any input-dependent stage. AUTHORITY_REQUIRED supplies a routing fact only. G/H consume pre-existing accepted dossiers; v0.1 is not a semantic dossier author. All nine E1 dossier checklist predicates must be represented, including separation of decision-dependent facts from permitted deferred downstream facts. Partial alternatives never count as adoption.

External lifecycle: EXTERNAL_EVIDENCE_REQUIRED (named missing proofs) -> EVIDENCE_REQUEST_READY (complete request/receipt contract) -> WAITING_FOR_EXTERNAL_EVIDENCE (control transferred; not proof of sending) -> EVIDENCE_RECEIVED (admitted concrete bytes) -> EVIDENCE_VALIDATED (identity, authentication, producer competence, scope/lineage/currentness and required coverage pass) -> DEPENDENT_ACTION_REENTRY (original gates reevaluated). Invalid receipts are rejected and retained separately; partial/negative facts may be accepted at proposition level but leave the complete gate waiting. Distinguish received from validated from sufficient. In replay, a pinned accepted historical record or explicitly synthetic trust root supplies authenticity; a matching hash alone does not authenticate a producer.

## 7. Global control and persistence

Current branch states: RUNNABLE_INTERNAL, HUMAN_DECISION_REQUIRED, WAITING_FOR_EXTERNAL_EVIDENCE, FACT_ACQUISITION_REQUIRED, IMPLEMENTATION_AUTHORITY_REQUIRED, BLOCKED_BY_PLAN_DEFECT, DEPENDENCY_BLOCKED, TERMINAL_SUCCESS, TERMINAL_FAILURE. A fact-blocked decision never counts as HUMAN_DECISION_REQUIRED. Follow dependency-blocked branches to their concrete control-transfer records.

Deterministic global precedence:

1. Invalid snapshot or a defect affecting all candidate evaluation -> PLAN_DEFECT, no selection. A localized defect blocks only its dependent actions and remains reported.
2. Any independently valid machine-actionable action -> RUNNABLE (even if other branches wait).
3. Otherwise any genuinely decision-ready human action -> HUMAN_HANDOFF, batch only independent ready decisions (order dependency groups explicitly).
4. Otherwise unresolved required branch with a missing route/unsupported required rule -> PLAN_DEFECT; return exact defect, never create a reasoning action.
5. Otherwise all declared goals proved -> TERMINAL_SUCCESS; proven unrecoverable required-goal failure with no remaining recovery route -> TERMINAL_FAILURE. BLOCKED or negative evidence alone is not terminal failure.
6. Otherwise exposed waits all have admitted external-evidence contracts -> EXTERNAL_WAIT. A mixture of external gates, external source/fact identification or implementation/authority boundaries -> MIXED_WAIT. A single non-ready external source/implementation boundary also uses MIXED_WAIT with its exact subtype; do not mislabel it ready human work.

Every unresolved goal must have a supported frontier path or a defect. E1's final eight boundaries include budget evidence plus source/fact acquisition routes; reproduce MIXED_WAIT, 27 unresolved roots and 41 slots, not inferred completion.

Persistence: one versioned canonical JSON snapshot bundle plus append-only event records; no database. Bundle references graph, plan definitions, current planner state, execution ledger, policy version, authority/evidence pins, waiting gates, candidate authority and pinned evaluation context. Resume manifest references the bundle components by hash; redundant counts are validated against recomputation rather than trusted. Event sequence and parent hash detect replay/reordering; applying an already accepted EventId is an idempotent no-op only if bytes and parent lineage agree. Conflicting replay fails closed.

Planner JSON profile: UTF-8, sorted keys, compact separators, ensure_ascii=False, no floats/nonfinite values, duplicate keys rejected, integers and booleans distinct. Preserve ordered arrays; sort only explicitly set-valued ID lists. Hash raw artifacts as bytes; for E1 embedded pointers use the exact canonicalization rule recorded in the manifest, not the planner profile by assumption. Record hash domain in every identity. New files are atomically written only to an explicit replay output directory, never E1. Ledger timestamp is optional supplied metadata, not ambient time. Deterministic output excludes filesystem timestamps and unordered diagnostics.

Restore checks every referenced artifact and relevant proof pin, not just the manifest. Mismatch refuses resume and reports stale assertions; no silent rebuilding of trust. E1 restore yields suspended state, not live currentness. An accepted synthetic complete receipt can demonstrate eligible reentry in an isolated fixture; it cannot lift E1's actual suspension. Existing Candidate-3 authority is read-only VALID_UNCONSUMED throughout.

## 8. Replay fixture and CLI contract

Each fixture is versioned JSON with required members:

| Member | Content |
|---|---|
| schema / case_id / mode | PLANNER-REPLAY-1; A–N; HISTORICAL or COUNTERFACTUAL_SYNTHETIC |
| source_manifest | Repository-relative path, raw SHA-256, optional typed semantic identity and its rule, pointer/section, extraction version, historical availability boundary |
| initial | Typed graph/assertions, actions and attempt states, root/slot predicates and values, knowledge, authority/evidence, decision stages, external gates, goals and evaluation context |
| policy | Pinned selection policy and static operation map |
| events | Supplied bounded results/dossiers/receipts/recorded decisions; prior-state reference and evidence contract; no expected root states as inputs |
| expected | Per-step actionable IDs, selected ID or null, criterion/trace, action/knowledge/root/slot transitions, global control, frontier, resume flag |
| prohibited | Forbidden transitions/effects, e.g. issue/use, root promotion from PASS, automatic DEC execution, source writes |

`expected` and `prohibited` are harness-only oracle fields and never passed to core evaluation. The source manifest at implementation time records exact current hashes, not placeholders. Fixture authoring is reviewed deterministic normalization, not automated interpretation. Missing historical snapshots require explicitly justified event reconstruction with source pointers; never back-project later decisions into earlier knowledge. The importer must account for all final graph roots/slots and plan actions for M/N, even when a rule can only conservatively block them. Historical reports may retain old metadata; explicit accepted overlays and provenance must be represented rather than silently changing them.

Case A loads actual Candidate-2 JSON and invokes the current pinned pure identity check; qualification tests pin relevant implementation bytes so drift cannot silently change the oracle. Cases G/H load actual accepted dossier JSON and validate their declared predicates/identities; they do not merely read a PASS/BLOCKED label. M/N recompute from typed definitions/evidence/routes, comparing final report fields only afterward.

Proposed CLI (not executed in this task): `python3 -m adapter.planner validate FIXTURE`; `plan FIXTURE`; `apply FIXTURE --event EVENT --out DIR`; `replay FIXTURE --out DIR`; `restore MANIFEST --out DIR`. `plan` prints actionable IDs, next action, trace, frontier, control, counts and resume eligibility. `apply` performs one validated supplied event and recomputes; `replay` consumes only fixture events, never executes selected actions. `restore` imports E1's manifest using the explicit E1 reader or a planner-native bundle, verifies pins and writes an isolated restored representation. JSON stdout, diagnostics stderr; exit 0 valid processing (including blocked/wait outcomes), 2 invalid schema/identity/contract, 3 replay expectation mismatch. No network, LLM, host execution or implicit external request. Tests use `python3 -m unittest discover -s adapter/tests -p 'test_planner*.py'`.

## 9. Dependency-ordered implementation packages

Each package ends with executable non-effecting tests; no package resolves a frozen E1 blocker.

| WORK_PACKAGE | PREREQUISITES | FILES | IMPLEMENTATION | TESTS / ACCEPTANCE | UNLOCKS |
|---|---|---|---|---|---|
| P01 — First vertical slice | Approved implementation task; this plan | model, minimal gates/core/selector/replay, initializer; test_planner_core; E fixture slice | Typed state -> prerequisite actionability -> E1 selector fallback -> supplied S-BINDING PASS -> accepted knowledge only -> recompute | Small source-pinned E1 slice, second independent action; knowledge grows, roots/slots unchanged, next selection stable under reversal; invalid PASS rejected | P02,P03 |
| P02 — Fixture trust and persistence | P01 | codec; model/replay; sources.json; test_planner_resume/invariants | Strict parsing/canonicalization, provenance and hash domains, append ledger, transitive stale invalidation, E1 manifest pointer reader | Raw/embedded pins, duplicate keys, identity-type mismatch, parent-chain mismatch, exact round trip and no E1 writes | P04,P05,P06 |
| P03 — Full gates, projection and selector | P01 | gates/core/selector; test_planner_core/invariants | All finite predicates, independent root/slot evaluators, prerequisite cycle checks, authority/effect gating, coverage completeness and static policy maps | C,D; X02,X03,X05–X09,X11; positive independent proof test; all 49 orders/100 replays; no optimistic unknowns | P04,P05 |
| P04 — Decision readiness and human routing | P02,P03 | gates/core/replay; F–I fixtures; test_planner_e1_replay | Explicit lifecycle/checklist, input reentry, partial knowledge, human batches and no automatic decisions | E,F,G,H,I; actual dossier evidence verified, no governed-condition promotions | P06 |
| P05 — Evidence gates and branch control | P02,P03 | gates/core/replay; J–M fixtures; test_planner_e1_replay | Fact/applicability routes, receipt checks, branch waits, control truth table and frontier witnesses | J,K,L,M; X01,X04,X08; full 27/41/eight frontier replay; synthetic independent work remains runnable | P06 |
| P06 — Complete replay and cold resume | P04,P05 | replay/codec/__main__; A,B,N fixtures; all four test files | Pure constructor identity adapter; missing Template-1 gate; full E1 import, manifest restore, CLI and isolated accepted-receipt reentry | A–N and X01–X11; cold subprocess restore, identical bytes across repeated runs, accepted evidence only reopens its branch, no effects/source changes | v0.1 completion review |

P02/P03 and P04/P05 may be developed independently after their prerequisites; no scheduling optimization is required. P01 is the first functioning planner, not just a schema layer. It uses a minimal E1 slice explicitly marked partial, so its test counts are not mistaken for the complete current experiment. Full frozen-state import and every acceptance case are mandatory before v0.1 completion; partial success cannot be labeled complete.

## 10. Completion gate and risks

Complete only when all 14 A–N tests, 11 negative invariants, selector completeness/fallback tests, deterministic serialization, pure-boundary guards and cold resume pass; identical pinned inputs yield identical outputs; all E1 bytes remain unchanged; no expected outcome requires LLM judgment. Report exact test commands, counts and fixture/source identities. No real E1 resumption, authority consumption or production effect is part of qualification.

Primary implementation risks: confusing raw versus canonical hashes; trusting historical report status instead of recomputing gates; using later knowledge for earlier preflight; importing effecting consumers; treating receipt contracts as already executable actions; treating a missing rule as false terminality or inventing its semantics. The acceptance matrix tests each boundary. If a fixture contract cannot be deterministically normalized from accepted evidence, record a specific fixture/specification defect; do not implement inference or claim the case passed.
