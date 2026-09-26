# Deterministic Reasoning and Planning Runtime

**Type:** Architectural backlog item
**Origin:** Experiment 1 (E1) dependency-planning and WorkAuthorization qualification
**Status:** Proposed architecture; documentation only

## Purpose

Build a governed runtime that turns durable, provenance-bound artifact knowledge into deterministic plans. LLM reasoning should focus on semantic uncertainty and propose interpretations or graph changes; deterministic services should own graph state, authority checks, formal validation, and execution planning.

Adopt this principle as the design direction:

> Never use probabilistic reasoning to rediscover information that can be represented, traversed, derived, selected, validated, or scheduled deterministically.

E1 supports this principle for known dependency reconstruction and frontier traversal. It does not demonstrate measured cost savings or show that every dependency can be found without runtime evidence. Those limits remain explicit below.

## Scope and design boundary

The capability consists of an artifact knowledge layer, a typed semantic graph, deterministic graph projections, a Plan Compiler, governed LLM proposal/review interfaces, and execution work routing. Its graph records evidence and authority provenance; it does not create authority. A missing root remains missing until its independent satisfaction criteria are met by accepted evidence, deterministic work or the exact required authority; a human decision cannot supply a missing fact.

The runtime must preserve distinctions among:

- what an artifact says;
- what a graph extraction proposes;
- what a deterministic validator verifies;
- what an authority record authorizes;
- what is currently applicable;
- what operation is permitted now;
- what effect has actually occurred.

An LLM-produced statement, an implementation default, a matching digest, or a historically qualified artifact cannot become operational truth solely by entering the graph.

## Artifact-to-knowledge synchronization

Canonical artifacts are authoritative evidence sources for the assertions they actually establish. The graph is a structured, provenance-preserving projection of artifact contents and explicit authority relations; it is not a replacement authority store.

The ingestion process should:

1. identify and verify an artifact's canonical identity and schema;
2. extract candidate entities, relations, requirements, producers, consumers, constraints, and evidence links;
3. attach exact source provenance (artifact identity plus location such as JSON pointer, field, or document section/line span where available);
4. validate the assertion's scope, lineage, authority status, and freshness;
5. persist the assertion as proposed, validated, accepted, rejected, or stale under governed policy.

The LLM may propose entity resolution, relation extraction, dependencies, authority/producer relationships, semantic constraints, evidence relations, and candidate missing relationships. It must not directly establish operational truth or mutate the accepted graph without deterministic validation and governed acceptance.

Artifact identity changes must trigger deterministic dependency invalidation. For each assertion, record the source artifact identity/version and the derivation/extraction version. When a source changes, the runtime must find all derived assertions and mark them stale or recompute them under a declared rule. No downstream graph state may remain silently current after a depended-on authority artifact changes.

Required invariant:

> No operational graph assertion exists without provenance, and no authoritative artifact change may leave dependent graph assertions silently unchanged.

An assertion lacking usable source location may be retained as an explicitly coarse extraction, but it cannot satisfy a formal requirement or authority check until its evidence is anchored sufficiently for review.

## Typed semantic knowledge graph

Represent nodes for artifacts, authority decisions, requirements, runtime facts, source inputs, derivations, validators, consumers, actions, evidence obligations, evidence objects, execution state, and planning propositions. Node identity must be stable, schema-versioned, and separate from mutable status.

Support at least these directed relation types:

| Relation | Meaning |
|---|---|
| `REQUIRES` | A proposition or operation requires another proposition to be established first. Only relations validated as ordering prerequisites enter the prerequisite DAG. |
| `AUTHORIZED_BY` | An authority record grants a defined permission within a scope. This does not imply that the permission has been exercised. |
| `PRODUCED_BY` | An artifact, fact, or evidence item is produced by a named process, component, or event. |
| `DERIVED_FROM` | A value or artifact is deterministically derived from identified inputs under a versioned rule. |
| `VALIDATED_BY` | An object or proposition is checked by a named validator/contract. |
| `CONSUMED_BY` | An artifact or value is an input to a consumer. |
| `EVIDENCED_BY` | A proposition is supported by a specific evidence object. Evidence alone does not confer authority. |
| `BINDS` | A record binds exact identities or values together; binding is not necessarily ordering. |
| `APPLIES_TO` | An authority/evidence object is scoped to a target and applicability conditions. Existence alone does not establish current applicability. |
| `CONSTRAINS` | A policy or authority limits values/actions available to another node. |
| `SUPERSEDES` | A new record supersedes a prior record prospectively or as explicitly specified; it does not rewrite historical facts. |
| `CORRESPONDS_TO` | Two independently constructed objects have a post-construction consistency relationship. It is not an ordering edge unless separately justified. |

Every assertion should carry at least:

- assertion identity and relation type;
- subject/object node identities and direction;
- exact source artifact identity and provenance location;
- scope, lineage, validity interval/freshness rule, and applicability conditions;
- authority status and relevant authority identities;
- extraction/derivation method and version;
- validation status, validator identity, and result evidence;
- lifecycle state: proposed, accepted, rejected, stale, superseded, or historical.

The graph must distinguish source provenance from authority provenance. A document can evidence a claim without being the authority that grants it.

## GraphRAG-style semantic ingestion and retrieval

Evaluate GraphRAG-style processing as the semantic ingestion/retrieval layer for:

- artifact-to-graph extraction and entity resolution;
- semantic relationship and requirement extraction;
- retrieval over related artifacts and prior findings;
- missing-producer and missing-relation investigation;
- bounded context generation for semantic review of one unresolved frontier item.

GraphRAG output is an assertion proposal, never the authoritative execution plan. The deterministic runtime validates identities, provenance, edge types, freshness, and projection eligibility; governance accepts or rejects changes. Retrieval ranking or generated summaries cannot satisfy authority, source, schema, or evidence requirements.

**UNTESTED_ARCHITECTURAL_HYPOTHESIS:** GraphRAG-style indexing can reduce the effort required to locate relevant evidence and candidate relationships. E1 did not evaluate a GraphRAG system or establish this performance claim.

## Deterministic graph projections

Derive and validate specialized projections from the typed graph. Each projection must be reproducible from a versioned projection rule and accepted graph snapshot.

1. **Prerequisite DAG:** only genuine temporal/order dependencies. Validate no cycles, dangling nodes, unsupported edge types, or disagreement with node `DependsOn`/`RequiredBy` metadata.
2. **Authority graph:** authority grantors, scopes, delegation, issuance, applicability, and authority class. Detect circular authority and self-authorization.
3. **Producer graph:** producers, required source inputs, derivation functions, and whether a producer exists and is authorized.
4. **Consumer/validator graph:** schema consumers, formal contracts, validator identity/version, validation mode, and whether validation is pure or effecting.
5. **Evidence graph:** obligations, producers, trigger events, produced evidence, validation rules, and acceptance criteria.
6. **Provenance graph:** source artifacts and locations through extraction, derivation, validation, and downstream assertions.

Non-ordering relationships—including binding, correspondence, applicability, evidence, ancestry, and synchronization—remain represented in the semantic graph but do not enter prerequisite traversal unless an explicit, validated rule establishes an actual ordering requirement. Joint construction groups must allow independently identified objects from common authoritative inputs followed by cross-validation; they must not be forced into artificial reciprocal prerequisites.

## Plan Compiler

Before a governed workflow executes, compile its accepted knowledge state into a deterministic plan or a precise blocker report. The compiler does not use an LLM to decide graph reachability, validate canonical hashes, or propagate states.

At minimum, preflight must detect:

- missing nodes, prerequisite edges, or source dependencies;
- missing or ambiguous producers;
- missing/unauthenticated authoritative inputs;
- undefined or non-deterministic derivations;
- incomplete consumer-required field mappings;
- circular authority and self-authorization paths;
- prerequisite and construction cycles;
- invalid actionability or unsatisfied operation prerequisites;
- stale scope, lineage, generation, or freshness;
- missing consumer contract or validator;
- effecting-only consumer validation where qualification requires a pure boundary;
- missing authority class for the proposed operation;
- incomplete evidence obligations or attempts to satisfy them with placeholders;
- unsupported resolution paths;
- historical-only evidence incorrectly used as current authority.

If deterministic preflight identifies one of these blockers, the workflow must not start the blocked operation. It returns an evidence-bounded blocking frontier and its provenance, with explicit minimality limits. Only an authorized, actionable semantic task may invoke an LLM; external waits and human handoffs do not. The compiler reruns after governed acceptance of relevant new evidence or specification changes.

## Planning state and actionability

Keep these states distinct:

- `UNRESOLVED`: satisfaction criteria are not established.
- `STRUCTURAL_FRONTIER`: node is at the satisfied/unsatisfied boundary in prerequisite traversal.
- `ACTIONABLE`: an identified operation can run now; its operation prerequisites, authority, scope, lineage, freshness, and temporal requirements all hold.
- `BLOCKED_FRONTIER`: structurally exposed but not currently actionable because a prerequisite state, authority, construction, runtime observation, or future event is missing.

Frontier membership alone never selects work. Actionability selection must check the specific resolution operation and whether its own required preconditions are satisfied. Future evidence cannot be required before the action that produces it.

When `ACTIONABLE = ∅`, compute:

- `ACTIONABILITY_BLOCKING_CUT`: an evidence-bounded set of unresolved conditions separating current state from actionable operations, with its minimality claim and private witnesses explicit;
- `ACTIONABILITY_SEED`: a smallest supported legitimate input/operation capable of enabling a reentry path; conditional availability is not present actionability. Do not claim global minimality without proof.

The cut must distinguish upstream seeds from downstream blocked conditions and exclude future execution evidence unless it truly prevents execution from beginning. Do not invoke open-ended LLM reasoning merely because the actionable set is empty.

## Work routing

Every actionable item carries an operation class, inputs, expected outputs, authority requirements, effect boundary, and validation rule. Support at least:

- `DECISION_INPUT_ACQUISITION`
- `FACT_ACQUISITION`
- `LOOKUP_REUSE`
- `DETERMINISTIC_VALIDATION`
- `DETERMINISTIC_CONSTRUCTION`
- `JOINT_CONSTRUCTION`
- `DETERMINISTIC_RECONCILIATION`
- `SEMANTIC_EVALUATION`
- `AUTHORITY_DECISION`
- `RUNTIME_EXPERIMENT`
- `GOVERNED_OPERATION`

Route lookup, graph traversal, hash/canonicalization checks, deterministic construction, reconciliation, and projection validation to deterministic services where possible. Route semantic uncertainty to bounded LLM reasoning. Route authority decisions to the authorized human/Architect process. Route runtime experiments and governed operations only when their exact authority and effect boundary are established.

## Canonical construction contracts

Every canonical artifact type must declare a machine-readable construction contract containing:

- producer and producer version;
- authoritative input identities and required currentness/applicability;
- derivation rules and explicit field-level source-to-output mappings;
- canonical schema/version and allowed fields/types;
- serialization, ordering, and normalization rules;
- identity body and deterministic identity rule;
- validators and validation sequence;
- consumer and consumer contract/version;
- `AUTHORITY_TO_CONSTRUCT` requirements;
- `AUTHORITY_TO_ISSUE` and/or `AUTHORITY_TO_RELEASE` requirements;
- `AUTHORITY_TO_USE` requirements;
- `AUTHORITY_TO_EXPAND` requirements, where applicable;
- expected effects and prohibited effects.

Before construction begins, every consumer-required field must have exactly one defined authoritative source and deterministic production rule, or a declared multi-source composition rule. Missing input, missing mapping, or ambiguous ownership blocks construction. Matching digests, copied fields, historical defaults, or LLM-selected values cannot fill these gaps.

### Template-1 case

E1's adopted architecture separates reusable Template-2 lifecycle semantics from invocation-specific Template-1. A binding-input record may compose references to already-authoritative sources but creates no authority. `binding_digest` and `fields_values` require explicit mappings from those inputs. Template-1 cannot authorize its own sources or depend on its own, Candidate 3's, or WorkAuthorization's final identity. The unresolved current source and projection gaps must remain visible as blockers until grounded; this backlog item does not resolve them.

## Formal consumer validation

The formal consumer owns its formal invariants. A canonical artifact used by deterministic production software is not `FULLY_QUALIFIED` until its exact representation is accepted by the authoritative consumer or by a demonstrably equivalent validator running the same validation logic.

Where validation is currently coupled to effects, require a pure boundary such as:

```text
validate_for_issuance(candidate, current_state) -> ValidationResult
```

The effecting consumer must call the same authoritative validation implementation before its effect path; it must not maintain a divergent validator. The pure path must not issue, consume, activate, assign ownership, write repository/audit state, or perform production effects. The effect path must check the separately applicable authority and protect against state changes between validation and use.

Qualification gates are separate and ordered: authoritative-input validation; schema validation; identity/canonicalization validation; consumer acceptance; semantic qualification; authority qualification. A semantic pass alone is not full qualification. Validation success is not issuance or permission to use.

## Persistent semantic results

Persist a governed semantic result with:

- target node/proposition and exact question;
- bounded input subgraph and evidence identities;
- scope, lineage, applicability, freshness, and satisfaction criteria;
- result classification and rationale;
- evaluator/model/prompt or method identity;
- validation/acceptance status and reviewer/authority provenance.

Reuse the result without repeating semantic reasoning only while the complete relevant input fingerprint and criteria remain unchanged, or have only changed monotonically in a way explicitly declared safe. A change to relevant evidence, source identity, scope, lineage, freshness, criteria, or governing authority requires reevaluation. Reuse never promotes historical conclusions to current authority.

## Authority model

Represent authority classes independently:

- `AUTHORITY_TO_CONSTRUCT`
- `AUTHORITY_TO_ISSUE`
- `AUTHORITY_TO_USE`
- `AUTHORITY_TO_RELEASE`
- `AUTHORITY_TO_EXPAND`

No class implies another unless the governing authority explicitly says so. Candidate construction does not issue; issuance does not activate; activation does not establish applicability beyond its binding; use does not authorize expansion. The plan compiler must verify the required class, exact target identity, scope, lineage, replay semantics, temporal validity, and currentness for each proposed operation.

## Evidence lifecycle

Represent separately:

- `EVIDENCE_PLAN`: known obligations, producers, triggers, provenance, and validation rules;
- `EVIDENCE_OBLIGATION`: a specific required evidence item;
- `EVIDENCE_PRODUCED`: actual immutable evidence emitted by its producer/event;
- `EVIDENCE_VALIDATED`: evidence accepted against its validation rule and applicability;
- `ACCEPTANCE`: a conclusion over the complete applicable validated evidence set.

An unresolved placeholder is an obligation descriptor, not evidence, and cannot satisfy its criterion. Evidence expected only during/post execution must not be required to exist before execution begins. Acceptance criteria and acceptance results are distinct.

## LLM and deterministic runtime responsibilities

### LLM: semantic compiler and ambiguity resolver

Use the LLM primarily to:

- extract candidate knowledge from artifacts;
- propose graph assertions or missing relations/producers;
- interpret genuinely ambiguous requirements;
- compare semantic meanings and identify conflicts;
- propose field mappings where no deterministic mapping is already defined;
- explain a bounded blocker using a prepared local context.

Every output remains a proposal. The LLM does not set operational status, authenticate source identity, accept its own graph mutation, assign authority, hash authoritative objects, or execute the compiled plan.

### Deterministic runtime: state, validation, and planning

The deterministic runtime owns:

- canonical artifact identity, serialization, and provenance;
- accepted graph state and mutation history;
- stale-assertion invalidation from changed source identities;
- relation typing and projection rules;
- prerequisite reachability, cycle detection, and propagation;
- authority/source applicability and freshness checks;
- producer completeness and field-mapping checks;
- schema, canonicalization, and consumer validation;
- actionability, blocking cuts, and plan compilation;
- evidence obligation/production/validation states;
- bounded context construction for an LLM frontier task.

## Governance of graph mutations

LLM mutation proposals must specify affected nodes/edges, relation type/direction, provenance, source locations, scope/lineage/freshness, rationale, confidence, projection consequences, and proposed satisfaction impact. The validator checks source identities, schemas, relation legality, edge direction, cycle behavior, missing nodes, freshness, authority-root rules, and projection consistency. A proposal is either rejected with reasons or accepted under an authorized review/policy path; acceptance is append-only and replayable.

No proposal may silently alter an authoritative artifact, issue an authority, or modify E1 dependency state. Graph mutation acceptance and operational authority are separate decisions.

## Post-E1 control-runtime requirements

The following numbered areas are **SUPPORTED_ARCHITECTURAL_INFERENCE** requirements for a future runtime, grounded in the separately cited **OBSERVED_E1_FINDING** records. They are not claims that Forge already implements the runtime. The traceability appendix uses the shorter labels OBSERVED, SUPPORTED_INFERENCE and HYPOTHESIS respectively; HYPOTHESIS means **UNTESTED_ARCHITECTURAL_HYPOTHESIS** and is never silently promoted to a requirement.

Frozen source baseline: E1_STATE = SUSPENDED_EXTERNAL_HANDOFF; E1_RESUME_ALLOWED = NO; GLOBAL_CONTROL_STATE = MIXED_WAIT; no runnable internal or decision-ready actions; 27 roots and 41 slots remain unresolved; Candidate-3 authority VALID_UNCONSUMED. This backlog update neither resumes E1 nor alters any experiment artifact. Counts/states in earlier experiment reports are historical snapshots, not current global state.

### R01 — Action state and independent result dimensions

Model `ACTION_ELIGIBLE` (structural/knowledge preconditions exposed), `ACTIONABLE` (all operation-specific inputs, authority and effect constraints permit the bounded stage), `SELECTED` (deterministically chosen), `COMPLETED` (its own acceptance passed), `BLOCKED` (a named unsatisfied gate), and `WAITING` (control transferred pending a named event). Structural eligibility is not permission. For human work, ACTIONABLE means ready for an explicit human decision, never automatic execution.

Keep `ACTION_RESULT`, `ACTION_KNOWLEDGE_PRODUCED`, `ROOT_CONDITION_TRANSITION` and `SLOT_TRANSITION` independent. PASS may mean a bounded inventory, proof-obligation specification, alternatives or dossier was accepted. BLOCKED can retain accepted partial knowledge. AUTHORITY_REQUIRED and EXTERNAL_GATE_REQUIRED do not complete an action. Historical outcomes are immutable; reentry appends a new attempt/acceptance overlay.

### R02 — Total deterministic selector

For a finite non-empty set of unique canonical ActionIds, apply: (1) descending graph-computable triple of directly resolved unresolved roots, affected unresolved slots through those roots, and actually potentially unlocked actions; (2) formally represented comparable information gain; (3) stable operation-class priority; (4) effect priority and explicit comparable cost; (5) smallest canonical ActionId. If criteria 1 or 2 cannot be computed completely and consistently for every tied candidate, skip the entire criterion without estimates. Descendant counts are not unlock counts. Missing cost is not zero.

Retain E1 class order: DETERMINISTIC_VALIDATION, DETERMINISTIC_CONSTRUCTION, SOURCE_ACQUISITION, DETERMINISTIC_MAPPING, IMPLEMENTATION_PREPARATION, SEMANTIC_EVALUATION, ARCHITECT_PREPARATION, RUNTIME_EXPERIMENT, GOVERNED_OPERATION. Version explicit mappings, including DECISION_INPUT_ACQUISITION to ARCHITECT_PREPARATION and the E1 FACT_ACQUISITION stage under SOURCE_ACQUISITION. Effects rank NON_EFFECTING, QUALIFICATION_EFFECT_ONLY, PRODUCTION_EFFECT. Never silently remap semantics to gain priority.

Each applicable criterion retains a non-empty best subset; exact case-sensitive Unicode ActionId order guarantees one final result (existing IDs are ASCII). Reject malformed duplicate IDs. Selection is independent of LLM preference, source-file/JSON/conversation order and ambient wall-clock timing. Eligibility may depend on an explicit pinned freshness input; hidden time cannot affect replay. Singleton selection needs no tie-break. Empty-set handling and human-only handoff are control routing outside the selector's finite non-empty automatic-work domain.

### R03 — Knowledge-producing actions

Track `UNKNOWN -> KNOWN_INCOMPLETE -> KNOWN_COMPLETE` for a named question/input contract independently of governed-condition satisfaction. Persist accepted facts, explicit gaps, rejected interpretations, alternatives and proof obligations with source artifact identity/location and method/acceptance provenance. Reuse them only while the relevant fingerprint remains valid. A changed source/rule can stale knowledge; the progression is not an unconditional monotonicity assumption. Proposed alternatives never become adopted contracts merely through persistence.

### R04 — Decision-readiness lifecycle

Represent `SEMANTIC_GAP_IDENTIFIED -> DECISION_INPUTS_REQUIRED -> DECISION_INPUT_ACQUISITION -> DECISION_DOSSIER_READY -> DECISION_READY -> ARCHITECT_DECISION -> DECISION_RECORDED -> DOWNSTREAM_REEVALUATION` with separate entry/exit evidence.

`AUTHORITY_REQUIRED != DECISION_READY`. Readiness requires a bounded question, concrete alternatives, all decision-dependent factual inputs, exact scope, consequences and provenance. Accepted authority need alone cannot expose an Architect action. Independently check dossier readiness; missing facts return to input acquisition or an external gate. A recorded decision triggers reevaluation, not satisfaction. DEC-EXEC's inventory PASS did not supply a concrete independent source/projector or permission proposal.

### R05 — Decision-input acquisition and reentry

Make DECISION_INPUT_ACQUISITION a first-class operation: inspect its authoritative source set, construct bounded unadopted alternatives, state exact representation consequences, and prepare a dossier. It cannot decide, invent evidence, grant authority or satisfy the governed condition. A conditional option may defer only facts outside the proposition being decided, never facts defining that proposition.

Compile explicit A/B/C routing: complete accepted decision inputs -> readiness check; bounded work possible -> input action; external facts missing -> explicit fact/evidence gate. Consume a semantic AUTHORITY_REQUIRED outcome as knowledge, not as semantic success. Retain E1's contrasting paths: SEM-BUDGET -> INPUT-BUDGET -> DEC-BUDGET ready; SEM-IMPLEMENTATION -> INPUT-IMPLEMENTATION -> FACT_BLOCKED. New REEVAL stages must meet the original criteria; specification repair cannot erase them.

### R06 — Human decision batching

Continue eligible independent machine work while decisions await attention. When only independent DECISION_READY human actions remain, aggregate review without lexical selection of one human decision. Check dependencies or option interference; order dependent decisions explicitly instead of pretending independence. Batch attention, not authority semantics: each retains its own evidence, scope, alternatives, authority identity when issued, consequences and approval/rejection state. Exclude fact-blocked/semantically incomplete decisions. Minimized human interruption is a design objective, not an E1-measured optimum.

### R07 — Fact acquisition and reentry

Represent `FACT_REQUIRED -> FACT_ACQUISITION -> EVIDENCE_VALIDATION -> DEPENDENT_ACTION_REENTRY`. Name the exact producer, permitted source set, proposition, authentication and failure gate. Missing facts cannot become semantic inference, Architect choice or compatibility assumptions. Per-proposition results are PROVED, DISPROVED, EVIDENCE_NOT_FOUND, AUTHORITY_DECISION_REQUIRED or EXTERNAL_EVIDENCE_REQUIRED. Retain partial facts independently; partial PASS is legal only if the action's own acceptance allows it. FACT-BUDGET-APPLICABILITY required complete proof and returned EXTERNAL_GATE_REQUIRED, not partial PASS. Reentry appends a bounded attempt without rewriting prior outcomes.

### R08 — Authority-reference applicability

`REFERENCE_TO_AUTHORITY` does not imply `CURRENT_APPLICABILITY` or `FRESHNESS`. Compile `authority reference -> applicability/freshness proof -> dependent reevaluation` when required by the governing contract. Separate authenticity, exact identity, publication/availability, scope, lineage, runtime, store generation, profile and temporal validity/usage. No publication from file existence, freshness from stable identity, REQUEST applicability from EXECUTION scope, or authority from technical compatibility. DEC-BUDGET Option A settled representation only; REEVAL-BUDGET and fact acquisition retained missing currentness evidence.

### R09 — Typed proof obligations

Represent `Condition -> PROVEN_BY -> EvidenceRequirement` and `EvidenceRequirement -> SATISFIED_BY -> EvidenceArtifact`. These are proof semantics, not implicit ordering edges. Distinguish `PROOF_RULE_UNKNOWN` (governing predicate/derivation unresolved) from `PROOF_RULE_KNOWN_EVIDENCE_MISSING` (rule known, qualified evidence absent); preserve both on composite requirements where necessary. Unknown rules cannot be filled with a convenient validator default. SEM-ELIGIBILITY specified proof obligations/cycle guards without producing eligibility; the budget matrix retained eight missing current-proof obligations separately from verified snapshot identity.

### R10 — External-evidence lifecycle and receipts

Represent `EXTERNAL_EVIDENCE_REQUIRED -> EVIDENCE_REQUEST_READY -> WAITING_FOR_EXTERNAL_EVIDENCE -> EVIDENCE_RECEIVED -> EVIDENCE_VALIDATED -> DEPENDENT_ACTION_REENTRY`. Request creation/sending, byte receipt, authentication and acceptance are separate states. A defined receipt action checks producer competence, identity, provenance, scope/lineage/currentness and per-proposition coverage; it may add supported assertions or reject evidence. It cannot repair evidence, infer missing propositions or create authority. Partial/negative/unrelated data cannot clear a complete proof gate. No receipt can become actionable without a concrete admitted submission and required trust rules.

### R11 — Branch suspension

Suspend a branch at WAITING_FOR_EXTERNAL_EVIDENCE without failing, cancelling, resolving or removing its conditions. Exclude work whose only eligibility path requires the waiting gate; independently recompute all other branches rather than globally stopping or relaxing their prerequisites. Resume only on relevant accepted input. E1's global replay found no independent runnable work after budget suspension; actual concurrent progress of another branch during that wait remains a future validation case, not an observed success.

### R12 — Global control states

Compute RUNNABLE, HUMAN_HANDOFF, EXTERNAL_WAIT, MIXED_WAIT, PLAN_DEFECT, TERMINAL_SUCCESS or TERMINAL_FAILURE. RUNNABLE takes precedence when legitimate independent machine work exists. An empty ACTIONABLE set must trigger deterministic control classification, not another LLM call. Distinguish unresolved producer facts, ready human work, external wait, missing implementation authority, planner defect and true completion/failure. Stop at a valid wait until accepted evidence or an authorized relevant state change occurs; elapsed time or conversation continuation is not progress.

### R13 — Global blocking frontier

Keep the current control-transfer frontier separate from the complete unresolved dependency set and the closure slot-cover cut. Report only currently exposed human/external/implementation/planner boundaries, preserving downstream blockers in the graph. E1 ended with 27 unresolved root conditions, 41 unresolved slots and an eight-member control frontier; these counts measure different things. Preserve evidence-bounded irredundancy/minimality limits and do not claim global minimum optimization.

### R14 — External handoff packages

Generate requests containing missing proposition, expected competent producer if known, acceptable evidence, authentication, freshness, scope/lineage, receipt action and reentry action. Do not invent missing producers or classify facts as decisions because a human may supply them. Consolidate only where one authenticated producer/response can actually cover each obligation. E1 used eight separately scoped bundles within one transport package; no qualified cross-branch producer merger was established. Preparation is not sending or obtaining evidence.

### R15 — Governed suspension and resume

Persist a content-identified checkpoint and resume manifest: graph, plan, execution ledger, selection policy, current authority identities, unresolved roots/slots, waiting request IDs, receipt/reentry routes, candidate-authority state and global control state. Include canonicalization rules for embedded identities and exact source locators; verify dependencies and reject stale tokens.

`RESUME_ALLOWED = TRUE` only when accepted new evidence or another authorized relevant state change makes at least one legitimate reentry action eligible. Unrelated input cannot resume a run. Commit only supported assertions, reevaluate the affected branch, recompute global eligibility and select under normal authority/effect constraints. Conversation history must not be required. E1 froze a manifest/checkpoint; no post-suspension evidence receipt/resume was exercised.

### R16 — Planner self-diagnosis

Represent planner defects as typed findings with exact evidence, violated invariant, affected scope and bounded repair/replay contract. E1 observed prerequisite/frontier confusion, undefined tie-break, premature DEC-EXEC readiness, missing budget/implementation decision-input reentry, and missing authority-reference applicability reentry. Fail closed and preserve domain state; permit separately governed specification correction and replay against unchanged substantive evidence. Repairing scheduling or a missing route does not supply missing facts or satisfy roots/slots. Do not diagnose a valid external wait as a new defect merely because it has no action.

### R17 — Identity semantics

Require at least CONTENT_IDENTITY, AUTHORITY_IDENTITY, INSTANCE_IDENTITY, RELEASE_IDENTITY, CANONICAL_OBJECT_IDENTITY, WORKAUTHORIZATION_ID and BINDING_DIGEST. Pin byte domain, identity rule and owning source per field; equal hash syntax does not establish interchangeability. WP-08 distinguished released-profile content from ReleasedProfileAuthority and ProgrammerProfile. A binding subobject identity, full authenticated-input binding_digest, T1 content identity and WorkAuthorization identity also remain distinct. Approved conversions require exact provenance and validation, never implicit coercion.

### R18 — Producer and consumer contracts

Every canonical value must answer: who/what produces it; from which authoritative inputs; by which deterministic transformation; under which authority; with what canonicalization; which validator; which consumer; and what accepted evidence proves the complete contract. Missing links are explicit. Preserve E1 cases: context JSON/live-object mismatch; OperationalBinding governance member; independent exec_bins mapping; transmission mapping and digest-domain separation; T1 content-identity verification. WP-10's validated JSON-array/runtime-tuple boundary repair did not solve exec_bins. A producer inventory or working serializer is not consumer acceptance.

### R19 — Pure validation boundary

Where governance needs qualification before effect authorization, consumers must provide a non-effecting validation boundary sharing the authoritative pre-effect logic used by the effect path. Retain identity/schema/source/applicability checks and an atomic freshness recheck before an authorized effect. Qualification must cover differential behavior, malformed inputs, zero-effect state preservation and active consumer linkage. A validation PASS grants no authority to accept, issue, consume, activate, own, transmit or execute. DEC-VALIDATOR approved bounded implementation/testing with CONTRACT-T1 retained; it did not demonstrate a finished qualified implementation.

### R20 — Graph and artifact synchronization

LLM/GraphRAG may propose assertions; operational truth requires governed acceptance. Every assertion retains artifact identity, source location, extraction method, validation state, scope, lineage and freshness where applicable. Changed artifact identity stales affected derivations under declared dependency rules. Coarse or unverified extraction cannot satisfy a formal gate. E1 preserved manual artifact/ledger/graph provenance and checked snapshot hashes; automated ingestion, acceptance and invalidation are future requirements, not exercised GraphRAG capabilities.

### R21 — Know when not to reason

Never use probabilistic reasoning to rediscover information that can be represented, traversed, derived, selected, validated, or scheduled deterministically. The planner must also know when NOT to reason: when no legitimate internal action exists, transfer control to the appropriate human, external evidence source, implementation boundary or terminal state. Do not manufacture progress by repeated semantic turns. General cost/performance gains and an optimal interruption policy remain UNTESTED_ARCHITECTURAL_HYPOTHESIS claims, not correctness prerequisites.

## Measurable acceptance criteria

The future implementation is acceptable only when the following criteria pass against a frozen, content-identified E1 artifact set and deterministic compiler version:

1. **Pre-R4 dependency reconstruction:** Given the E1 artifacts available immediately before R4 execution, the system reconstructs the known prerequisite assertions with source provenance without requiring repeated execution attempts. Any unresolved extraction ambiguity is explicitly reported rather than silently omitted.
2. **Template-1 preflight:** Before Candidate-3 construction begins, preflight reports every missing Template-1 producer, authoritative source, and field-level mapping identified by the consumer contract.
3. **Candidate-2 rejection:** Candidate 2 is rejected before Architect issuance review by deterministic schema/identity/consumer-contract validation, with the failure pointing to the actual mismatch.
4. **Dispatcher actionability:** `DISPATCHER_ELIGIBILITY` is not selected as actionable while `ACTIVE_RECOVERY`, `OPERATIONAL_CONTEXT_CURRENT`, or `OPERATIONAL_BINDING_CURRENT` remains an unmet operation prerequisite.
5. **Joint construction:** InvocationCandidate and OperationalBinding can be jointly constructed from common authoritative inputs, independently identified, then cross-validated without either final identity appearing as a prerequisite of the other.
6. **Deterministic invalidation:** Changing an authoritative source artifact identity marks or recomputes every dependent assertion and projection under declared rules; no affected accepted assertion remains silently current.
7. **Replayable planning:** Repeated planning over the same content-identified graph snapshot, authority state, freshness time input, and compiler version produces byte-equivalent plan/frontier output and requires no LLM call.
8. **Operation readiness:** Every selected actionable node identifies operation class, required inputs, effect boundary, current authority class, scope/lineage checks, and validation result before execution.
9. **No premature qualification:** No canonical artifact is `FULLY_QUALIFIED` while a required producer, source authority, field mapping, schema check, identity check, or consumer validation is unresolved.
10. **Projection soundness:** The prerequisite projection excludes non-ordering semantic relations, is acyclic, has no dangling references, and is reproducible from the accepted typed graph snapshot.
11. **Authority separation:** Tests demonstrate that construct, issue, release, use, and expand permissions are independently checked and cannot be inferred from one another.
12. **Evidence causality:** Placeholders cannot satisfy obligations; future evidence cannot block the action that produces it; acceptance requires the complete applicable validated evidence set.
13. **Mutation governance:** Invalid or unsupported LLM-proposed edges are rejected or left proposed; accepted mutations retain provenance and an append-only decision record.
14. **Pure consumer validation:** Validation PASS and FAIL create no lifecycle, issuance, ownership, repository, host, model, or production effects, and the effecting path calls the same authoritative validator.

Acceptance runs must record counts, identities, decisions, and output hashes. E1 did not measure tokens, latency, cost, or labor; future measurements may be collected but are not prerequisites to the correctness criteria above.

### R22 — Post-E1 replay acceptance suite

These are future runtime acceptance obligations, not instructions to execute/resume E1. Use content-identified copies and non-effecting fixtures. Pin the evidence availability at each historical operation boundary; do not claim retrospective detectability from later-acquired knowledge. Counterfactual/preflight tests must state any later contract supplied as a fixture. Separate currentness inputs from ambient clock time.

| Case | Required behavior | Evidence limit |
|---|---|---|
| A | Reject Candidate 2 before Architect issuance review using the actual consumer schema/identity contract. | Observed failure; preflight prevention is a future replay target, not a claim that historical review was prevented. |
| B | Block Candidate-3 construction when authoritative consumer-ready Template-1 is absent. | Observed input-validation stop; preserve candidate authority unconsumed. |
| C | Do not select dispatcher eligibility before actual recovery/context/binding prerequisites. | Observed premature selection; corrected future scheduler must prevent it. |
| D | Replay the same Wave-1 set under permutations, JSON reorderings and repeated runs; select the same ActionId. Test missing metrics and final tie-break totality. | E1 selection-policy tests observed; future runtime must reproduce them. |
| E | Allow S-BINDING and S-CONTEXT inventory PASS with knowledge persisted and roots/slots unchanged. | Observed bounded knowledge outcomes. |
| F | Authority need alone cannot expose DEC-EXEC without its concrete source/projector or exact independent policy proposal. | Observed premature-readiness defect and contained correction. |
| G | INPUT-BUDGET can produce a complete representation-only decision dossier without adopting any option. | Observed PASS and decision readiness. |
| H | INPUT-IMPLEMENTATION retains partial knowledge and FACT_BLOCKED when distinct owning source/selector are absent. | Observed blocked dossier; no invented choice. |
| I | Continue machine work while decisions wait; batch only ready independent human work and preserve separate records. | E1 selected INPUT-IMPLEMENTATION while DEC-BUDGET was ready; Batch 1 excluded DEC-EXEC. No measured interrupt optimum. |
| J | DEC-BUDGET authority reference approval must not close current applicability/freshness or budget slot. | Observed REEVAL-BUDGET BLOCKED and fact-action external gate. |
| K | Missing external evidence suspends its branch with exact receipt/reentry contract. | Observed waiting request/control specification; no external receipt occurred. |
| L | Inject a separately qualified independent machine action into a copy of the E1 waiting fixture; run it without reopening the waiting branch. | SUPPORTED_INFERENCE acceptance test; E1 global replay itself found none runnable. |
| M | Final E1 fixture yields MIXED_WAIT, eight control points, no automatic LLM task and no false terminal success. | Observed global recomputation and suspension. |
| N | Cold-load the exact resume manifest/checkpoint without conversation history; verify hashes and reject unrelated/partial/stale evidence. In isolated fixtures, accepted complete evidence enables only valid reentry and recomputes eligibility. | Manifest creation observed; end-to-end cold resume is untested and must be qualified, not executed against frozen E1. |

Record action/result/knowledge/root/slot transitions, receipt decisions, control handoffs, source identities, selector traces and output hashes. Negative tests must verify no authority inference, evidence fabrication or effect. Minimality, performance, scalability and general applicability beyond these fixtures are not established by E1.

## E1-supported evidence and limits

### OBSERVED_E1_FINDING — observed in E1

- Repeated LLM-directed progression encountered prerequisites incrementally; a durable model later represented known conditions.
- The initial graph had 49 nodes and 46 edges while 60 already-declared prerequisite pairs were absent from its edge set; reconciliation produced 104 prerequisite edges.
- Two apparent cycles were semantic relationships (derivation plus correspondence/currentness, and derivation plus binding/applicability) rather than true ordering cycles.
- The final prerequisite projection was acyclic; deterministic traversal found a bounded six-node frontier and the directed evaluations discovered no new dependency among those six.
- Frontier membership was confused with actionability; runtime eligibility testing occurred before explicit recovery/context/binding prerequisites were resolved. The actionability review identified the correction.
- An empty actionable set was usefully analyzed as a blocking cut and seed rather than as an invitation to continue open-ended discovery.
- InvocationCandidate and OperationalBinding were independently constructed from common inputs and cross-validated with no identity recursion.
- Candidate 2 received semantic qualification but failed the actual consumer schema. Candidate-3 authoritative-input validation then stopped at the missing consumer-required Template-1 source.
- Template-2 lifecycle semantics and Template-1 invocation-specific consumer requirements are distinct; the latter also lacks current sources and deterministic field mappings.
- The consumer path coupled validation with issuance and lacked a full non-effecting consumer acceptance boundary.
- Construction, issuance, lifecycle, ownership, applicability, and use needed separate authority/state treatment.

### SUPPORTED_ARCHITECTURAL_INFERENCE

E1 supports durable, provenance-preserving reasoning state; deterministic prerequisite traversal; separating ordering from semantic relations; bounded LLM work on unresolved semantic questions; and reducing opportunities to rediscover already-recorded prerequisites. It supports a Plan Compiler as a response to observed structural, producer, mapping, actionability, and consumer-contract failures.

### UNTESTED_ARCHITECTURAL_HYPOTHESIS — not demonstrated

E1 did not demonstrate automated LLM graph-mutation acceptance, GraphRAG retrieval quality, complete static discovery of future dependencies, production execution from a compiled plan, or numerical token/latency/cost savings. These remain hypotheses and require separate implementation qualification. Runtime experiments and human authority decisions remain necessary where propositions cannot be established from existing artifacts.

## E1 traceability appendix

R23 requires every numbered area and replay case to retain exact artifact traceability with its epistemic label. R24 preserves the frozen experiment: this task changes only the two backlog documents and implements nothing.

See [DETERMINISTIC_REASONING_PLANNING_RUNTIME_E1_TRACEABILITY.md](DETERMINISTIC_REASONING_PLANNING_RUNTIME_E1_TRACEABILITY.md) for the requirement-to-observation mapping and source artifact references.

## Non-goals and preservation

This backlog item does not implement the runtime, change E1 dependency topology/status, resolve the Template-1 blocker, grant authority, or authorize production execution. It does not change production state. Historical E1 artifacts remain immutable evidence and are interpreted only within their established scope.
