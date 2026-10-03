# Deterministic Planner v0.1 — Acceptance Matrix 1

Status: test specification only; no tests implemented or executed by this document. See the [implementation plan](DETERMINISTIC_PLANNER_V0_1_IMPLEMENTATION_PLAN.md), [requirements](../backlog/DETERMINISTIC_REASONING_PLANNING_RUNTIME.md) and [traceability](../backlog/DETERMINISTIC_REASONING_PLANNING_RUNTIME_E1_TRACEABILITY.md).

All tests run against pinned, read-only E1 artifacts and isolated replay state. They must not change E1, issue authority, construct Template-1/Candidate 3, consume Candidate-3 authority, or produce runtime effects. Source identity checks are not assertions of live applicability. A–N are future runtime acceptance tests, not claims that a planner already passed them.

The harness validates each fixture's schema and source hashes, evaluates actual predicates without access to expected outputs, applies supplied events only, and compares every intermediate state and prohibited transition. Pin evaluation time/generation as data. Record source/rule/selection-policy identities, normalized input hash, event hashes, sorted diagnostics, outputs and output hashes. A computed block may be a passing test; skipped tests are not passes.

## Replay cases A–N

### A. Candidate-2 consumer rejection

**GIVEN:** The exact Candidate-2 JSON and the consumer schema/identity contract; semantic qualification is recorded but is not consumer acceptance. Pin adapter/invocation_constructor.py and the reconciliation contract. Mark use of the later reconciliation as a disclosed counterfactual preflight fixture, not prior historical knowledge.

**WHEN:** The pure registered consumer precheck calls invocation_constructor.identity on Candidate 2, before admitting an issuance-review action.

**THEN:** ConstructionDenied identifies unknown WorkAuthorization schema; consumer acceptance is REJECTED and the candidate-specific issuance-review action is not actionable. Compare the exception category and offending schema/identity requirements, not a hand-authored FAIL label.

**AND MUST NOT:** Call consume_and_issue, construct a replacement artifact, issue authority, accept lowercase workauthorization_id as WorkAuthorizationId, or interpret the prior semantic PASS as full qualification.

**Requirements / packages / evidence limit:** R17–R20,R22,R24; P03/P06; observed rejection, counterfactual earlier gate.

**Exact evidence:** [E1_CURRENT_WORKAUTHORIZATION_CANDIDATE_2](../experiments/E1/E1_CURRENT_WORKAUTHORIZATION_CANDIDATE_2.md); [E1_WORKAUTHORIZATION_CONSUMER_CONTRACT_RECONCILIATION_1](../experiments/E1/E1_WORKAUTHORIZATION_CONSUMER_CONTRACT_RECONCILIATION_1.md); [Candidate-2 bytes](../experiments/E1/E1_CURRENT_WORKAUTHORIZATION_CANDIDATE_2.json)

### B. Missing Template-1 prevents Candidate 3

**GIVEN:** The Candidate-3 authoritative-input validation result and construction authority; current consumer-ready Template-1 source is absent. Include independent source/producer/mapping predicates, not only an arbitrary blocked flag.

**WHEN:** Recompute the Candidate-3 construction action against its required Template-1 gate.

**THEN:** It is BLOCKED with the exact missing authoritative Template-1 input reason; construction is not selected. Candidate-3 authority stays VALID_UNCONSUMED; no Template-1 or Candidate-3 value is emitted.

**AND MUST NOT:** Substitute Template-2, a historical template, placeholder, or authority-to-construct for the missing consumer input; consume single-use authority.

**Requirements / packages / evidence limit:** R01,R17–R20,R22,R24; P03/P06; observed stop.

**Exact evidence:** [E1_CURRENT_WORKAUTHORIZATION_CANDIDATE_3](../experiments/E1/E1_CURRENT_WORKAUTHORIZATION_CANDIDATE_3.md); [Candidate-3 authority](../experiments/E1/E1_CURRENT_WORKAUTHORIZATION_CONSTRUCTION_AUTHORITY_3.json)

### C. Prerequisite projection before dispatcher selection

**GIVEN:** The dispatcher prerequisite review identifies ACTIVE_RECOVERY, OPERATIONAL_CONTEXT_CURRENT and OPERATIONAL_BINDING_CURRENT as unresolved operation prerequisites; preserve non-ordering correspondence/binding records separately.

**WHEN:** Compile the explicit ordering projection and evaluate DISPATCHER_ELIGIBILITY.

**THEN:** Dispatcher eligibility is not actionable or selected. Reasons name all unmet operation gates. In isolated positive variants, satisfy the recorded prerequisite proofs individually; only all applicable gates together can expose the action.

**AND MUST NOT:** Select it merely for structural-frontier membership, turn correspondence into ordering, drop unrepresented DependsOn metadata silently, or run a dispatcher probe.

**Requirements / packages / evidence limit:** R01,R12,R16,R20–R22,R24; P03; observed selection defect, future prevention.

**Exact evidence:** [E1_DISPATCHER_PREREQUISITE_REPRESENTATION_REVIEW_1](../experiments/E1/E1_DISPATCHER_PREREQUISITE_REPRESENTATION_REVIEW_1.md)

### D. Total deterministic selection

**GIVEN:** The policy's initial 15-action set: PREP-AUDIT, PREP-BINDING-GRANT, PREP-RUNTIME_HEAD, PREP-SUPERVISOR, PREP-VALIDATOR, S-ANCESTRY, S-APPROVAL, S-BINDING, S-CONTEXT, S-EXEC, SEM-BUDGET, SEM-ELIGIBILITY, SEM-IGNORED, SEM-IMPLEMENTATION, SEM-INTERFACES. All are eligible under the pinned historical stage; complete coverage/information metrics are absent.

**WHEN:** Select under ascending/descending order, all 15 rotations, 32 SHA-256-keyed deterministic orders, 100 identical replays, reordered JSON keys and different ambient clocks with the same pinned evaluation context.

**THEN:** Every run selects S-ANCESTRY, deciding criterion 5; criteria 1/2 NOT_DECISIVE, criterion 3 retains five source actions and criterion 4 ties. All six permutations of an equal-priority synthetic three-ID set select TEST-A. Test complete unequal coverage, information and cost separately; missing metrics fall through. Singleton uses criterion 0, empty set returns no selection at the scheduler boundary.

**AND MUST NOT:** Estimate a missing score, change priorities based on prose usefulness, depend on source/JSON/conversation order, accept conflicting duplicate IDs, or execute S-ANCESTRY.

**Requirements / packages / evidence limit:** R02,R20,R22,R24; P01/P03; observed E1 tests, future runtime reproduction.

**Exact evidence:** [E1_TEMPLATE1_GRAPH_RESOLUTION_SELECTION_1_RESULT](../experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_SELECTION_1_RESULT.md); [E1_GRAPH_RESOLUTION_SELECTION_POLICY_1](../experiments/E1/E1_GRAPH_RESOLUTION_SELECTION_POLICY_1.md)

### E. Knowledge-producing PASS without resolution

**GIVEN:** Separate S-BINDING and S-CONTEXT stage fixtures with unresolved governed roots/slots, their exact bounded inventories and permitted accepted knowledge contracts. Use explicit independent satisfaction predicates that the inventories do not meet.

**WHEN:** Select the eligible action, validate and apply its supplied PASS result, then recompute; test each action independently.

**THEN:** Only the action completes and the inventory knowledge/provenance is persisted. ROOT_CONDITION_TRANSITION and SLOT_TRANSITION remain UNCHANGED; no newly resolved IDs. A subsequent eligible independent action can be selected without running it.

**AND MUST NOT:** Treat PASS as root/slot satisfaction, insert an inferred producer or approved mapping, discard knowledge because no root changed, or revisit the completed action.

**Requirements / packages / evidence limit:** R01,R03,R18,R20,R22,R24; P01/P04; observed bounded outcomes.

**Exact evidence:** [E1_TEMPLATE1_GRAPH_RESOLUTION_S_BINDING_1_RESULT](../experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_S_BINDING_1_RESULT.md); [E1_TEMPLATE1_GRAPH_RESOLUTION_S_CONTEXT_1_RESULT](../experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_S_CONTEXT_1_RESULT.md)

### F. Authority need is not decision readiness

**GIVEN:** S-EXEC inventory knowledge and the recorded DEC-EXEC readiness defect: neither a concrete independent source/projector nor an exact independent permission-policy proposal is established.

**WHEN:** Apply accepted authority-required/gap knowledge and evaluate the corrected decision-input/readiness route.

**THEN:** DEC-EXEC is FACT_BLOCKED and excluded from actionable human decisions/batches. Report the concrete missing decision inputs and external/input route. Preserve historical premature readiness as historical evidence, not current truth.

**AND MUST NOT:** Derive exec_bins from argv, manufacture policy facts, interpret AUTHORITY_REQUIRED as DECISION_READY, or ask the Architect to decide absent facts.

**Requirements / packages / evidence limit:** R04,R05,R09,R16,R20,R22,R24; P04; observed contained readiness defect.

**Exact evidence:** [E1_TEMPLATE1_ARCHITECT_DECISION_BATCH_1](../experiments/E1/E1_TEMPLATE1_ARCHITECT_DECISION_BATCH_1.json); [E1_DECISION_INPUT_REENTRY_SEMANTICS_1](../experiments/E1/E1_DECISION_INPUT_REENTRY_SEMANTICS_1.md)

### G. INPUT-BUDGET complete representation dossier

**GIVEN:** Accepted SEM-BUDGET knowledge and exact INPUT-BUDGET dossier JSON, source hashes and bounded representation-only proposition. All nine readiness predicates below are supported; current applicability is explicitly outside this decision proposition.

**WHEN:** Validate the supplied dossier and PASS result; independently evaluate DEC-BUDGET readiness.

**THEN:** INPUT-BUDGET completes, accepted knowledge is retained, DEC-BUDGET becomes DECISION_READY. Alternatives A/B/C remain unadopted; roots/slots unchanged. In the recorded full stage ACTIONABLE is [DEC-BUDGET, INPUT-IMPLEMENTATION]; NEXT_ACTION is INPUT-IMPLEMENTATION, criterion 3.

**AND MUST NOT:** Approve Option A, execute MAP-BUDGET, claim present applicability from snapshot identity, or satisfy root:budget merely by preparing a dossier.

**Requirements / packages / evidence limit:** R03–R06,R20,R22,R24; P04; observed PASS/readiness.

**Exact evidence:** [E1_TEMPLATE1_GRAPH_RESOLUTION_INPUT_BUDGET_1_RESULT](../experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_INPUT_BUDGET_1_RESULT.md); [Budget dossier JSON](../experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_INPUT_BUDGET_1_DOSSIER.json)

### H. INPUT-IMPLEMENTATION fact-blocked dossier

**GIVEN:** Accepted implementation semantic knowledge and partial dossier: runtime reference is not verified runtime bytes; the distinct-domain IMPLEMENTATION-OWNING-SOURCE and IMPLEMENTATION-SELECTOR remain absent.

**WHEN:** Validate supplied INPUT-IMPLEMENTATION partial output against all readiness predicates.

**THEN:** ACTION_RESULT is BLOCKED, accepted partial knowledge remains, action is not completed, DEC-IMPLEMENTATION is FACT_BLOCKED. Roots/slots unchanged. In its full historical stage ACTIONABLE is [DEC-BUDGET], control is HUMAN_HANDOFF, NEXT_ACTION is NONE.

**AND MUST NOT:** Choose runtime equivalence, invent an owning source/canonical selector, label the dossier complete, discard accepted partial gaps, or execute DEC-BUDGET.

**Requirements / packages / evidence limit:** R01,R03–R05,R09,R18,R20,R22,R24; P04; observed blocked result.

**Exact evidence:** [E1_TEMPLATE1_GRAPH_RESOLUTION_INPUT_IMPLEMENTATION_1_RESULT](../experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_INPUT_IMPLEMENTATION_1_RESULT.md); [Implementation dossier JSON](../experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_INPUT_IMPLEMENTATION_1_DOSSIER.json)

### I. Machine work before independent human batch

**GIVEN:** Two stage fixtures: (1) DEC-BUDGET ready while INPUT-IMPLEMENTATION is actionable; (2) Batch-1 dossiers for DEC-BINDING, DEC-IGNORED, DEC-VALIDATOR passing readiness, with DEC-EXEC fact-blocked. These are separate historical stages, not one invented combined state.

**WHEN:** Compute control, select machine work where present, and recompute the human-only stage after supplied bounded outcomes.

**THEN:** Stage 1 chooses INPUT-IMPLEMENTATION (criterion 3); after its blocked result, [DEC-BUDGET] forms a human handoff. Stage 2 batches exactly DEC-BINDING, DEC-IGNORED, DEC-VALIDATOR, retaining independent evidence, scope, alternatives and decision identities. NEXT_ACTION is NONE for either human-only handoff.

**AND MUST NOT:** Lexically auto-select/execute a human decision, include DEC-EXEC or fact-blocked decisions, merge authority semantics, or claim measured optimal interruption counts. Synthetic dependency/interference variant must split/order conflicting decisions rather than batch them as independent.

**Requirements / packages / evidence limit:** R04–R06,R12,R20,R22,R24; P04; observed batches and machine-first stage.

**Exact evidence:** [E1_TEMPLATE1_ARCHITECT_DECISION_BATCH_1](../experiments/E1/E1_TEMPLATE1_ARCHITECT_DECISION_BATCH_1.md); [E1_TEMPLATE1_ARCHITECT_DECISION_BATCH_1_ISSUANCE_RESULT](../experiments/E1/E1_TEMPLATE1_ARCHITECT_DECISION_BATCH_1_ISSUANCE_RESULT.md); [E1_TEMPLATE1_GRAPH_RESOLUTION_INPUT_BUDGET_1_RESULT](../experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_INPUT_BUDGET_1_RESULT.md); [E1_TEMPLATE1_GRAPH_RESOLUTION_INPUT_IMPLEMENTATION_1_RESULT](../experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_INPUT_IMPLEMENTATION_1_RESULT.md)

### J. Authority reference needs applicability proof

**GIVEN:** DEC-BUDGET Option A authority record and exact StatusBudgetAuthority identity, with representation approved but eight applicability/currentness obligations unproved.

**WHEN:** Validate the authority identity separately, then evaluate REEVAL-BUDGET and the fact-acquisition result.

**THEN:** Reference consistency is established only within its recorded scope. REEVAL-BUDGET remains BLOCKED; FACT-BUDGET-APPLICABILITY records EXTERNAL_GATE_REQUIRED. Eight current proof obligations stay unresolved; no root:budget or slot resolution, no MAP-BUDGET eligibility.

**AND MUST NOT:** Infer publication from file existence, freshness from identity stability, REQUEST applicability from FIRST_PROGRAMMER_EXECUTION, or technical compatibility as an authority grant.

**Requirements / packages / evidence limit:** R07–R09,R17,R20,R22,R24; P05; observed approved policy with missing proof.

**Exact evidence:** [E1_TEMPLATE1_ARCHITECT_DEC_BUDGET_AUTHORITY_1](../experiments/E1/E1_TEMPLATE1_ARCHITECT_DEC_BUDGET_AUTHORITY_1.json); [E1_TEMPLATE1_GRAPH_RESOLUTION_REEVAL_BUDGET_1_RESULT](../experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_REEVAL_BUDGET_1_RESULT.md); [E1_TEMPLATE1_GRAPH_RESOLUTION_FACT_BUDGET_APPLICABILITY_1_RESULT](../experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_FACT_BUDGET_APPLICABILITY_1_RESULT.md)

### K. Missing evidence suspends its branch

**GIVEN:** Budget missing evidence result plus exact external request/receipt contract; no external response exists.

**WHEN:** Apply the supplied request-ready/control-transfer event and recompute the gate lifecycle.

**THEN:** EXT-BUDGET-APPLICABILITY-EVIDENCE is WAITING_FOR_EXTERNAL_EVIDENCE; receipt remains ineligible until an admitted response; budget-dependent fact revalidation/REEVAL/MAP remain blocked. Existing identity observations persist.

**AND MUST NOT:** Treat creation of a request as sending or evidence arrival; synthesize evidence; clear any proof obligation; poll/reason automatically or reopen the branch.

**Requirements / packages / evidence limit:** R07,R10–R12,R14,R20,R22,R24; P05; observed waiting specification, not actual receipt.

**Exact evidence:** [E1_BUDGET_APPLICABILITY_EXTERNAL_EVIDENCE_REQUEST_1](../experiments/E1/E1_BUDGET_APPLICABILITY_EXTERNAL_EVIDENCE_REQUEST_1.md); [E1_EXTERNAL_HANDOFF_PACKAGE_1](../experiments/E1/E1_EXTERNAL_HANDOFF_PACKAGE_1.json)

### L. Independent work survives branch wait

**GIVEN:** A copy of K's waiting fixture plus a clearly synthetic independent non-effecting action TEST-INDEPENDENT with all prerequisites, sources and authority constraints explicitly met. Label it COUNTERFACTUAL_SYNTHETIC, never an actual E1 action.

**WHEN:** Recompute globally, select and apply only its bounded synthetic result.

**THEN:** Global control is RUNNABLE and TEST-INDEPENDENT is selected; budget gate stays waiting and all dependent work blocked. After the event, only its permitted knowledge/conditions may change; rerun all independent gate checks.

**AND MUST NOT:** Resume the budget branch, stop all scheduling due to one waiting branch, borrow budget authority, or claim E1 observed productive concurrent work during final suspension.

**Requirements / packages / evidence limit:** R02,R11,R12,R20,R22,R24; P05; synthetic future qualification.

**Exact evidence:** [E1_GLOBAL_CONTROL_RECOMPUTATION_1](../experiments/E1/E1_GLOBAL_CONTROL_RECOMPUTATION_1.md); [E1_GLOBAL_CONTROL_RECOMPUTATION_1](../experiments/E1/E1_GLOBAL_CONTROL_RECOMPUTATION_1.json)

### M. Global exhaustion means MIXED_WAIT

**GIVEN:** The full final typed graph, resolution plan/ledger, handoff routes and control report, normalized with their accepted overlays. Expected report fields are oracle-only, never fed into actionability. All 28 root definitions and 43 slot definitions are represented.

**WHEN:** Recompute gates, actionability, root/slot states, frontier and global control without a supplied new event.

**THEN:** ACTIONABLE, RUNNABLE_INTERNAL and DECISION_READY are empty; NEXT_ACTION is NONE; 27 unresolved roots, 41 unresolved slots; eight frontier control points listed below; MIXED_WAIT. Both construction/readiness flags remain false.

**AND MUST NOT:** Invent a reasoning action, classify empty as PLAN_DEFECT solely because it is empty, declare terminal success, repair missing inputs, or silently count downstream blocked conditions as new frontier members.

**Requirements / packages / evidence limit:** R12,R13,R16,R20–R22,R24; P05; observed final control state.

**Exact evidence:** [E1_GLOBAL_CONTROL_RECOMPUTATION_1](../experiments/E1/E1_GLOBAL_CONTROL_RECOMPUTATION_1.md); [E1_SUSPENSION_CHECKPOINT_1](../experiments/E1/E1_SUSPENSION_CHECKPOINT_1.json); [Final graph](../experiments/E1/E1_TEMPLATE1_TYPED_KNOWLEDGE_GRAPH_1.json); [Final plan/ledger](../experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_PLAN_1.json)

### N. Cold restore and controlled hypothetical reentry

**GIVEN:** Exact frozen resume manifest, checkpoint, referenced graph/plan/ledger/policy/authorities/evidence and handoff contracts. New subprocess, no conversation history, no network and an empty temporary output directory.

**WHEN:** Restore and recompute; then in separate isolated synthetic fixtures test unrelated, stale, malformed, partial, negative and complete authenticated evidence under a pinned test trust contract.

**THEN:** Initial restore yields SUSPENDED_EXTERNAL_HANDOFF, MIXED_WAIT, 27/41, empty actionability, E1_RESUME_ALLOWED false and Candidate-3 VALID_UNCONSUMED. Valid complete synthetic evidence enables only its named reentry after original gates pass; recompute global selection without executing it. Identical source/context/event inputs produce byte-identical outputs in fresh processes.

**AND MUST NOT:** Resume actual E1, trust manifest counts without recomputation, accept missing/tampered policy or authority pins, treat partial/negative/unrelated evidence as sufficient, mutate historical outcomes, consume authority or use ambient conversation/time to reconstruct state.

**Requirements / packages / evidence limit:** R07,R10–R15,R17,R20–R24; P02/P06; persisted manifest observed, cold resume qualification untested until implementation.

**Exact evidence:** [E1_EXTERNAL_HANDOFF_PACKAGE_1](../experiments/E1/E1_EXTERNAL_HANDOFF_PACKAGE_1.json); [E1_RESUME_MANIFEST_1](../experiments/E1/E1_RESUME_MANIFEST_1.json); [E1_SUSPENSION_CHECKPOINT_1](../experiments/E1/E1_SUSPENSION_CHECKPOINT_1.json)

## Shared decision-readiness checklist for F–I

Check independently: (1) exact question/scope; (2) pinned source inventory/provenance; (3) concrete alternatives with canonical values/types/selectors; (4) factual assumptions and consequences for each option; (5) authority granted and excluded; (6) downstream qualification obligations; (7) no invented fact/unqualified identity equivalence; (8) all facts defining the choice established, separately identified downstream deferrals; (9) independent readiness and source/freshness checks for the bounded proposition. G passes these for representation only. H fails 3,4,8 and remains FACT_BLOCKED; do not use a count threshold or majority vote.

## Budget proof matrix for J–N

Track eight independent propositions: publication/availability; scope; lineage; runtime; G4/controller-store; ProgrammerProfile; temporal freshness/currentness; FIRST_PROGRAMMER_EXECUTION-to-target-REQUEST applicability. Snapshot identity/reference consistency is separate. Each proof is PROVED, DISPROVED, EVIDENCE_NOT_FOUND, AUTHORITY_DECISION_REQUIRED or EXTERNAL_EVIDENCE_REQUIRED with an exact source/receipt contract. No one proposition implies another without a pinned governing rule. Negative evidence stays accepted knowledge while the dependent gate remains blocked.

## Full final frontier oracle for M/N

Compare set equality, not merely size:

- EXT-BUDGET-APPLICABILITY-EVIDENCE
- EXT-REENTRY-S-ANCESTRY
- EXT-REENTRY-S-APPROVAL
- EXT-REENTRY-PREP-AUDIT
- EXT-REENTRY-PREP-RUNTIME_HEAD
- EXT-REENTRY-PREP-SUPERVISOR
- EXT-REENTRY-DEC-EXEC
- IMPLEMENTATION-OWNING-SOURCE + IMPLEMENTATION-SELECTOR (one compound control point with both proof requirements)

The satisfied root gate:validator_authority and the two already resolved slots retain their evidence. All other 27 roots/41 slots remain unresolved. Derive their identities from the graph/accepted state, not invented names. The source report and manifest are the oracle; the runtime must reconstruct these counts from independent predicates/accepted overlays.

## Negative invariants X01–X11

For every row, run an adversarial variant and a positive control. A fail-closed implementation that refuses every input does not meet the suite. Rejected mutation leaves source/state/authority bytes unchanged; permitted partial evidence is retained only with its original proof scope.

| ID | GIVEN / WHEN | THEN / AND MUST NOT | Tests and evidence basis |
|---|---|---|---|
| X01 Historical evidence | Replace current required generation/scope with an authenticated historical proof while retaining a matching identity; evaluate | Current gate remains unproved with exact stale/scope reason; never promote historical acceptance to current | J,N; budget reentry and fact result |
| X02 Semantic versus ordering | Add reciprocal CORRESPONDS_TO/BINDS relations with no ordering justification; project; then add an explicit true REQUIRES cycle | Semantic relations remain outside DAG; actual ordering cycle is a defect. Do not invent order or silently remove a genuine cycle | C; dependency cycle review |
| X03 Permission classes | Supply CONSTRUCT-only authority to ISSUE/USE requirement; evaluate | Reject each absent class even with same target/hash; construct remains separately admissible under its own gates | B,N; Candidate-3 authority |
| X04 Reference versus proof | Supply valid authority identity without applicability/currentness evidence | Identity succeeds; applicability fails; no root/slot promotion. Positive control supplies each independently authenticated required proof | J; DEC-BUDGET / REEVAL-BUDGET |
| X05 Missing fact versus decision | Remove owner/selector or concrete exec policy from otherwise complete dossier | FACT_BLOCKED, no human-ready action; absent fact cannot become an option implicitly | F,H; dossiers and readiness defect |
| X06 Missing producer | Remove PRODUCED_BY/source from a required value; add semantically similar nearby artifact | Value/action stays blocked; no inferred producer edge. Explicit accepted producer evidence in synthetic control may pass | B,E; source/consumer reconciliation |
| X07 PASS versus satisfaction | Supply inventory PASS and attempt to include direct root_state/slot_state fields; separately apply well-formed knowledge-only result | Illegal state setters rejected; valid inventory completes action only. Positive independent proof resolves only its declared condition/slot | E; source action results |
| X08 Placeholders | Submit request descriptors, null placeholders, empty purported receipts or future evidence plans as proof | Remain requirements, never SATISFIED_BY; executing a proof-producing action is not blocked by its own future output where its contract permits execution | K,N; external request and temporal evidence review |
| X09 Effecting validation | Register an effecting validator for a pure-required contract; instrument issuance/ownership/host/network/write callbacks | Reject before invocation; every effect sentinel remains untouched. Pure identity rejection in A runs. Validator PASS cannot grant effect authority | A; consumer reconciliation and DEC-VALIDATOR authority |
| X10 Source invalidation | Change one source byte/semantic identity in an isolated copy; recompute all dependent derivations | Direct/transitive dependent assertions and readiness become STALE/unusable; unaffected independent facts remain. Old resume token rejected; no silent re-pin | N; graph synchronization contract and manifest mismatch rule |
| X11 Typed identity | Supply identical digest payload tagged as CONTENT_IDENTITY where AUTHORITY_IDENTITY/RELEASE_IDENTITY/WORKAUTHORIZATION_ID is required, including profile-domain substitutions | Reject by semantic kind/domain before equality; correct domain and valid evidence is the positive control. Never coerce by shared SHA-256 syntax | A,J,N; WP-08 profile finding |

Additional exact invariant evidence: [cycle review](../experiments/E1/E1_DEPENDENCY_MODEL_CYCLE_REVIEW.md), [temporal evidence review](../experiments/E1/E1_ACCEPTANCE_EVIDENCE_TEMPORAL_REVIEW_1.md), [validator authority](../experiments/E1/E1_TEMPLATE1_ARCHITECT_DEC_VALIDATOR_AUTHORITY_1.json), [profile identity finding](../experiments/E1/E1_TEMPLATE1_CLOSURE_WP08_RESULT.md). Automated stale propagation is a supported architectural requirement, not an observed E1 implementation.

## Structural and deterministic qualification

Beyond the 11 domain invariants, test strict unknown-enum/duplicate-key rejection, duplicate IDs/dangling edges, unsupported required rules, conflicting event replay, ordered-array preservation, canonical hash domain separation (raw file versus embedded JSON versus authority body), Unicode IDs and cost/metric completeness. Test all seven global states with small synthetic fixtures, including empty-but-valid external wait and independent runnable work alongside a localized defect. A missing reentry route is a defect; a present route awaiting external facts is not.

Selection tests must demonstrate first-decisive-criterion traces, not only final equality. Resume tests must restore in a fresh process and independently recompute states. Importer tests must not read expected actionable/control fields as input facts. Cross-check normalized provenance against exact source locations and accepted overlays; record any later contract used for historical preflight explicitly.

Preservation checks compare the complete frozen E1 file inventory and raw SHA-256 values before/after, including additions/deletions, plus implementation/authority state where appropriate. The replay runner may write only its explicit temporary output directory. Tests must not instantiate live host/controller clients or send external requests. No cold-resume test is permission to resume E1.

## Completion evidence

Required result: 14/14 A–N cases, 11/11 X01–X11 families and all structural/deterministic variants pass, with no skips; identical outputs under repeated inputs, no LLM call and no production effects; complete frozen-source preservation. Record test version, fixture version, source inventory identity, test command and per-case result. A positive synthetic receipt/resume test is reported separately from historical replay. Failure or missing fixture knowledge leaves v0.1 incomplete rather than allowing inference to fill the gap.
