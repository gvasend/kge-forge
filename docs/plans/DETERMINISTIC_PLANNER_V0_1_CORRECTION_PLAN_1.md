# Deterministic Planner v0.1 — Adversarial Correction Plan 1

Status: planning only. No implementation, tests, historical qualification records or E1 artifacts are changed by this plan. The adversarial verdict remains QUALIFICATION_REQUIRES_CORRECTION. The original QUALIFIED record remains historical evidence, not a sufficient current completion claim.

Authority: [adversarial review](DETERMINISTIC_PLANNER_V0_1_ADVERSARIAL_REVIEW.md), [original plan](DETERMINISTIC_PLANNER_V0_1_IMPLEMENTATION_PLAN.md), [acceptance matrix](DETERMINISTIC_PLANNER_V0_1_ACCEPTANCE_MATRIX.md), and [historical qualification](DETERMINISTIC_PLANNER_V0_1_QUALIFICATION.md)/[JSON](DETERMINISTIC_PLANNER_V0_1_QUALIFICATION.json). The [correction matrix](DETERMINISTIC_PLANNER_V0_1_CORRECTION_MATRIX_1.md) contains the complete finding normalization and test oracles.

## 1. Scope, root causes and dependency order

The four MAJOR findings F01–F04 and two MINOR findings F05–F06 remain separate findings. Their symptoms overlap but one change does not close them all.

| Root-cause group | Finding | Distinct correction responsibility |
|---|---|---|
| RC-REFERENCE-INTEGRITY | F04 | Validate predicate kinds, typed targets and future-output declarations before use |
| RC-STALE-OBLIGATION | F01 | Preserve invalidated prerequisite obligations and invalidate dependent conclusions |
| RC-RESUME-PROOF | F02 | Compute resume eligibility from current persisted proof and eligible reentry, not stage alone |
| RC-OPERATIONAL-RESTORATION | F03 | Restore operational contracts, not just opaque source text and identity coverage |
| RC-TYPED-ORDERING | F05 | Canonical ordering and unambiguous witnesses for equal-spelling typed IDs |
| RC-POLICY-BINDING | F06 | Bind the executed supported policy version to its verified policy contract |

F01/F04 share a need for a complete dependency/reference inventory; they do not share one repair. A referentially valid stale edge can still disappear from enforcement. F02 depends on current evidence and prerequisite validation but requires its own correction to the resume predicate. F03 must install the contracts those validators operate on; stronger validators cannot reconstruct omitted semantics. F05 is a collection ordering defect, independent of proof validity. F06 is a policy identity/semantics binding defect, not an ordering comparator defect. Fail-open behavior is a consequence of F01/F02, not a seventh root cause.

Seven bounded packages are sufficient: six corrections and one integrated qualification/review package. No unrelated repairs are merged for counting purposes.

```text
C01 reference/contract validation -> C02 stale obligations -> C03 resume proof
C04 typed ordering -----------------------------------------------+
C05 policy binding -----------------------------------------------+
C01, C02, C03, C04, C05 -> C06 full operational import -> C07 requalification/review
```

C04 and C05 can be implemented independently of C01–C03. C06 waits for their stable validation, serialization and policy interfaces. Deterministic package scheduling rule: among incomplete packages with accepted prerequisite results, select the lexicographically smallest canonical package ID. This schedules C01 first; it is a correction-work ordering rule, not a change to the E1 action selector. Package completion never executes a following package.

## 2. Shared constraints and status handling

Retain the existing `model/core/gates/selector/codec/replay/__main__` boundaries. Add only typed fields/rules needed for the represented contracts; do not create a parallel planner or general semantic compiler. No GraphRAG, LLM inference, network acquisition, issuance, production executor, new database or UI. Existing E1 missing facts remain missing.

Preserve historical event/result bytes and source pins. Introduce an explicit versioned additive encoding or reviewed migration for corrected state. Older bundles may remain available as historical replay inputs, but missing proof must not be auto-filled with permissive defaults to make them operationally current. Any migration writes a new isolated bundle, binds the old identity and mapping version, and preserves history. Pure validation must not mutate the supplied state or issue authority.

At the start of C01 implementation, before code edits, create **new** `docs/plans/DETERMINISTIC_PLANNER_V0_1_CURRENT_STATUS_1.md` and `.json` with:

```text
V0_1_CURRENT_STATUS = CORRECTION_REQUIRED
HISTORICAL_QUALIFICATION = QUALIFIED
SUPERSEDING_BASIS = adversarial review identity + correction-plan identity
OPEN_FINDINGS = [F01,F02,F03,F04,F05,F06]
E1_STATE = SUSPENDED_EXTERNAL_HANDOFF
E1_RESUME_ALLOWED = NO
```

Include raw identities of the historical qualification, review and this plan/matrix, current implementation revision/inventory, and scope. “Superseding” concerns current status, not rewriting the first run's results. No existing convention requires this metadata during planning, so this task creates neither status artifact. Each correction produces an append-only `DETERMINISTIC_PLANNER_V0_1_Cxx_RESULT.md` (JSON optional) with changed files, tests, finding closure evidence and remaining gates. C07 creates a new qualification record and, only after independent review acceptance, a new `CURRENT_STATUS_2` record superseding status 1. Reusing the old qualification filename or overwriting the review is prohibited.

Record the 10,911-file E1 path/raw-SHA inventory before each implementation package and compare it afterward. Changes outside the package's declared scope block acceptance. Planning and qualification do not grant permission to run E1.

## 3. Correction work packages

Test paths below are under `adapter/tests/`; implementation paths are under `adapter/planner/`. Use existing test files and `fixtures/planner_v0_1/`; a bounded versioned contract-mapping fixture belongs there. Do not edit frozen evidence to accommodate a test.

### C01 — Predicate and reference-contract validation

- **FINDINGS_ADDRESSED:** F04.
- **PREREQUISITES:** Current code and review available; no reliance on the disputed QUALIFIED claim. Record status 1 and preservation inventory first.
- **FILES:** `model.py`, `gates.py`, `codec.py`, `replay.py`; `test_planner_invariants.py`, `test_planner_resume.py`; necessary versioned fixtures; new status/result artifacts.
- **IMPLEMENTATION_CHANGE:** A closed per-PredicateKind structural contract: required/optional/forbidden fields, typed target collection, identity domain, operand cardinality, declared outputs, and cycle rules. Apply it at import/decode, native restore and direct planner/transition entry points before use. Distinguish an intentionally unavailable source from an ID naming an absent object. Bind future knowledge to a declared bounded output contract/producer; absence of produced evidence remains UNKNOWN, not a dangling reference or permission. Establish current-proof validation for stale/invalid targets without discarding their historical records.
- **TESTS:** Matrix T04 and T-REFERENCE; direct decode, structured import, native restore and planner API. Missing entity/action/condition/knowledge target; unknown predicate kind or ID; wrong target domain; stale target incorrectly marked usable; conflicting duplicate IDs/bindings; invalid fields; permitted declared future output; undeclared future output; predicate dependency cycle.
- **REPLAY_CASES:** B/C/F/H/J/N plus existing structural regressions.
- **NEGATIVE_INVARIANTS:** X02/X05/X06/X08/X10/X11.
- **ADVERSARIAL_COUNTEREXAMPLE:** SOURCE_IDENTITY predicate names `EntityId('absent')` and currently round-trips successfully.
- **ACCEPTANCE:** Malformed declared references rejected before planner use with typed diagnostics. Valid absent/future facts retained explicitly as unavailable; they never prove gates. Finite cyclic proof definitions rejected as unsupported/invalid at admission, not recursively guessed. All prior legitimate forward-output fixtures remain representable and fail closed until their outputs are accepted.
- **UNLOCKS:** C02; stable predicate/reference contracts for C06.

### C02 — Stale prerequisite enforcement and transitive invalidation

- **FINDINGS_ADDRESSED:** F01.
- **PREREQUISITES:** C01 PASS.
- **FILES:** `model.py` only for required validation metadata; `core.py`, `gates.py`, `codec.py`; `test_planner_core.py`, `test_planner_invariants.py`, `test_planner_e1_replay.py`.
- **IMPLEMENTATION_CHANGE:** Keep invalidated explicit ordering obligations in the enforcement dependency graph, marked unavailable. Do not implement staleness as edge deletion. Extend invalidation through ordering subjects, dependent predicates, current output qualifications, roots, slots, decision checklists, gates and goal/control conclusions. Preserve historical action completion/result separately from whether its outputs still establish a current prerequisite. A stale completed action's output cannot discharge a current ACTION_COMPLETED dependency merely because its historical attempt passed. Build this on existing assertions/projection, not a second mutable graph.
- **TESTS:** T01 and T-STALE: actual `invalidate_sources` on disjoint proof/ordering source identities; direct and transitive root/slot ordering; current action output used downstream; decision readiness; mixed valid/stale support; explicit requalification with a new accepted source/edge; canonical reload; independent unaffected branch stays runnable.
- **REPLAY_CASES:** C/E/F/I/L/M/N.
- **NEGATIVE_INVARIANTS:** X02/X07/X10; retain X03/X04/X05.
- **ADVERSARIAL_COUNTEREXAMPLE:** `child REQUIRES parent`, parent unresolved, child otherwise proved. Invalidate only edge provenance. Current code changes child UNRESOLVED -> SATISFIED.
- **ACCEPTANCE:** Invalidating proof cannot increase readiness through removal of an obligation. Child and its dependent root/slot/action/decision remain unresolved, stale or blocked with an explicit reason. No dependent human review, resume eligibility or terminal-success claim follows from the missing edge. Independent valid work remains selectable where the invalidity is localized. Historical facts are preserved, not converted to failed executions.
- **UNLOCKS:** C03; safe enforcement projection for C06.

### C03 — Persisted resume eligibility proof

- **FINDINGS_ADDRESSED:** F02.
- **PREREQUISITES:** C01 and C02 PASS.
- **FILES:** `core.py`, `gates.py`, `model.py` if a typed result is needed, `replay.py`, `codec.py`, `__main__.py`; `test_planner_resume.py`, `test_planner_e1_replay.py`, `test_planner_invariants.py`.
- **IMPLEMENTATION_CHANGE:** One pure, shared resume-eligibility computation used by API/CLI/restore output. Recompute from the persisted contract, admissions/observations, proof applicability, exact target, accepted reentry event and current actionability. No trusted saved Boolean. Return reasons and supporting identities. Preserve the historical lifecycle stage even when its eligibility proof is now stale.
- **TESTS:** T02/T-RESUME: complete then stale attestor, stale ordering, conflicting/partial/negative/unrelated receipts, changed target/policy/contract, missing admission or reentry event, unfulfilled other prerequisites, held/completed reentry action, multiple gates on the same route, fresh-process restore. Positive isolated complete evidence enables only the named route; unrelated waiting branches do not veto an independently valid route.
- **REPLAY_CASES:** J/K/L/M/N.
- **NEGATIVE_INVARIANTS:** X01/X03/X04/X07/X08/X10/X11.
- **ADVERSARIAL_COUNTEREXAMPLE:** After complete synthetic receipt/reentry, invalidate TEST-TRUST. Core has no actionable action and `external_complete=false`; current output says `resume_allowed=true`.
- **ACCEPTANCE:** Shared output says false with exact remaining gates in that case. True requires every condition in section 5 and an eligible named reentry action. No root/slot transition, authority issuance or action execution is performed by computing the flag.
- **UNLOCKS:** C06; final N receipt/resume qualification.

### C04 — Canonical typed ordering of control outputs

- **FINDINGS_ADDRESSED:** F05; FIX_BEFORE_REQUALIFICATION.
- **PREREQUISITES:** None beyond current code/review and preservation checks; can run independently.
- **FILES:** `core.py`; `codec.py`/`model.py` only if typed witness serialization needs an additive version; `test_planner_core.py`, `test_planner_resume.py`.
- **IMPLEMENTATION_CHANGE:** Use a total typed key, such as `(canonical ID type tag, exact value)`, for set-valued cross-domain goal/branch outputs. Preserve type tags in witnesses so equal spellings do not collapse. Audit related collection sorting and imported-reference output using the same rule. Do not change canonical ActionId comparison or reorder causal ledger/history arrays.
- **TESTS:** T05/T-ORDER: ConditionId('same') and SlotId('same') in every order, with distinct states and shared-spelling witnesses. Compare complete Computation, canonical serialized output, CLI output where exposed, and cold-reloaded state. Include reversed dictionary keys and reference-list permutations.
- **REPLAY_CASES:** D/M/N; existing I/L selection controls.
- **NEGATIVE_INVARIANTS:** X02/X11 remain PASS; deterministic typed-domain distinction is an additional counterexample test.
- **ADVERSARIAL_COUNTEREXAMPLE:** Same canonical snapshot, reversed goals, different `branches` tuples.
- **ACCEPTANCE:** Identical canonical semantic state yields identical complete output, including branches/witnesses. No changed ActionId priority or historical event ordering.
- **UNLOCKS:** C06/C07.

### C05 — Selection-policy identity and implementation binding

- **FINDINGS_ADDRESSED:** F06; FIX_BEFORE_REQUALIFICATION.
- **PREREQUISITES:** None beyond current code/review and preservation checks; can run independently.
- **FILES:** `selector.py`, `codec.py`, `replay.py`, `model.py` only for the bounded policy-binding type; `test_planner_core.py`, `test_planner_invariants.py`, `test_planner_resume.py`; versioned policy fixture/map if needed.
- **IMPLEMENTATION_CHANGE:** A closed supported-policy registry binds canonical policy ID/version, exact admitted artifact identity/projection, static operation-class map and implementation rule version. Verify it before selection/import/restore. Code may retain a static algorithm; its accepted policy pin must identify that algorithm's contract. Unsupported changes require a new explicit policy version or rejection, not silent rebinding. Content hash alone is not semantic policy qualification.
- **TESTS:** T06/T-POLICY: substitute valid construction-authority bytes; mismatched version/digest; altered class map/tie-break/effect rule; stale supported policy; unsupported extension. Valid original policy and supported decision-input extension retain D's expected selector behavior.
- **REPLAY_CASES:** D/I/L/M/N.
- **NEGATIVE_INVARIANTS:** X10/X11; retain X03.
- **ADVERSARIAL_COUNTEREXAMPLE:** B imports with its construction-authority ArtifactPin in the selection-policy field.
- **ACCEPTANCE:** Reject before selection and restore use. Historical policy pins/versions remain historical; no silently promoted current policy. Complete supported rules are canonically pinned and permutation invariant.
- **UNLOCKS:** C06/C07.

### C06 — Complete operational contract import and persistence

- **FINDINGS_ADDRESSED:** F03; apply O01/O02 boundaries without expanding scope.
- **PREREQUISITES:** C01–C05 PASS.
- **FILES:** `model.py`, `replay.py`, `codec.py`; necessary `gates.py`/`core.py`/`__main__.py` integration; all four existing planner test files; new versioned import contract map/fixtures under `fixtures/planner_v0_1/`. Do not modify E1.
- **IMPLEMENTATION_CHANGE:** Restore the contract families inventoried in section 6 into existing typed operational models, with only bounded additive types for currently absent concepts. Separate action definition, immutable historical attempts, accepted knowledge, current hold and evidence-triggered reentry. Replace default-empty requirements/default PASS for restored actions with qualified bounded acceptance rules or an explicit UNSUPPORTED_CONTRACT hold. Do not equate a historical result with every future allowable result. Restore actual decision/dossier and authority/evidence bindings. Version and pin the reviewed source-pointer/section mapping; every required semantic field receives a mapping or explicit unsupported reason. Opaque records may supplement, never substitute for required operational predicates.
- **TESTS:** T03/T-IMPORT/N-REAL as below; semantic reference/contract inventory comparison independent of imported output; isolated post-reentry result acceptance/rejection, decision reentry, stale-source and conflicting overlay controls; cold round-trips preserving each operational field; alpha-renamed synthetic contract instances and changed-but-supported values to prevent fixture-specific shortcuts.
- **REPLAY_CASES:** A–N, particularly E/F/G/H/J/M/full N.
- **NEGATIVE_INVARIANTS:** X01–X11.
- **ADVERSARIAL_COUNTEREXAMPLE:** M normalization has 63 actions, no Decision/GraphEntity objects, no typed action requirements or authority predicates, and default PASS acceptance for every action; full import merely adds opaque source records.
- **ACCEPTANCE:** Contract coverage and enforced semantics, not object counts alone. Every decision/source/authority/result/reentry contract relevant to current control and represented future reentry is typed or explicitly blocked. Required supported contracts must actually work in isolated positive tests; replacing everything with UNSUPPORTED_CONTRACT does not close F03. Frozen-data readiness validation runs no action. Unsupported authoritative rules necessary to complete that validation are a precise BLOCKED acceptance gap, not invented facts or permission to broaden v0.1.
- **UNLOCKS:** C07 only; no E1 runtime resumption.

### C07 — Integrated requalification and fresh adversarial review

- **FINDINGS_ADDRESSED:** Closure verification of F01–F06; observations' agreed disposition.
- **PREREQUISITES:** C01–C06 PASS, source-preservation checks accepted.
- **FILES:** Existing tests/isolated fixtures only where final integration requires bounded additions; new `DETERMINISTIC_PLANNER_V0_1_REQUALIFICATION_1.md/.json`, `DETERMINISTIC_PLANNER_V0_1_ADVERSARIAL_REVIEW_2.md`, C07 result, and subsequently status 2. No historical qualification edits. Any discovered implementation defect returns to its owning correction package; do not hide an opportunistic repair in qualification.
- **IMPLEMENTATION_CHANGE:** None planned. Execute and record the gate, compare exact input/output identities, then perform fresh adversarial review independent of original test oracles.
- **TESTS:** All A–N, X01–X11, all T01–T06/expanded counterexamples, importer/CLI/source-integrity, real-manifest readiness test, complete persistence/control/determinism variations and affected repository regressions.
- **REPLAY_CASES:** A–N, no waiver or skip.
- **NEGATIVE_INVARIANTS:** X01–X11, no NOT_YET_APPLICABLE.
- **ADVERSARIAL_COUNTEREXAMPLE:** Original suite can pass while review examples fail; a repeat of old tests alone is explicitly insufficient.
- **ACCEPTANCE:** Section 9 conjunctive gate plus fresh review confirms no open MAJOR or required MINOR finding. Any new applicable safety/determinism defect keeps CORRECTION_REQUIRED.
- **UNLOCKS:** Current-status qualification update and code review. Does not unlock E1 execution; its external handoff remains governed separately.

## 4. Exact validation and stale-enforcement contract

Admission has two distinct checks. Structural validation rejects malformed types, domains, references, duplicate/conflicting definitions, forbidden cycles and unknown required predicates. Operational proof validation rejects use of missing, invalid or stale targets as current support. A known historical stale object can remain in persisted state only as explicitly non-current evidence; it cannot silently remain an accepted proof target. The user requirement to reject stale targets before planner use does not license deleting stale prerequisites or destroying historical evidence.

For each PredicateKind, record field cardinalities and domains. `entity/other` must identify compatible GraphEntity kinds; `action/condition/obligation` must resolve to the correct typed collections; `operands` must identify admitted predicates. Knowledge references must resolve to accepted records or explicit declared future outputs owned by a bounded action contract. A future declaration confers no production or acceptance status. An intentional missing source uses a typed unavailable binding/reason, not a dangling string ID. Cross-domain equal digest text or equal-spelling IDs cannot substitute.

Invalidate through this closure:

```text
source identity or acceptance changes
 -> affected assertion/producer/authority/evidence validity
 -> explicit prerequisite obligation remains present but unavailable
 -> predicate/current-output proof validity
 -> dependent roots, slots, action gates, dossier checks and receipt proofs
 -> decision readiness, reentry eligibility, branch/global conclusions
```

Follow explicit ordering plus actual proof dependencies. Do not promote CORRESPONDS_TO or other semantic links into prerequisite order. Mixed supported/stale alternatives must be evaluated under the exact contract: an independently permitted alternative can pass, but a mandatory stale prerequisite cannot be bypassed through an unrelated ANY operand. Unknown dependency structure is a diagnostic/hold, never evidence of independence. Prefer localized holds where the validated graph establishes independence; globally invalid projection fails closed.

Historical ACTION_RESULT/COMPLETED is preserved. “This completed action's output still satisfies the current prerequisite” needs current accepted evidence under its contract. Root/slot satisfaction and decision readiness are recomputed from that evidence. A stale dependency cannot be made current by serialization, replay order, a previous PASS, or a remembered Boolean.

## 5. Persisted resume proof

Define a typed derived result with `allowed`, eligible named reentry IDs, remaining reasons and supporting identities. Persist its inputs and optionally its result as a checked cache; the cached result has no independent authority.

`RESUME_ALLOWED = TRUE` only if at least one route satisfies **all** of:

1. Verified snapshot/bundle, source/provenance pins, qualified policy binding, evaluation scope/lineage/target/generation and the applicable suspension/resume rule.
2. An accepted permitted state-change record for that route. For E1's frozen handoff this means received, independently authenticated external evidence satisfying the exact receipt contract; unrelated authority changes or information do not substitute. Generic admitted decision reentry uses its own explicitly authorized contract, not a fabricated external receipt.
3. Current evidence for every required proof obligation, exact producer competence/authority, source identity/domain, target and required freshness. No stale attestor, conflicting proof, missing fact or inferred applicability.
4. An accepted lineage-bound transition to dependent reentry, supported by the immutable event history or authenticated imported checkpoint/overlay. Stage text alone is insufficient; native events must replay, and imported historical transitions must have source-bound support.
5. The exact reentry action is incomplete, has an authorized reentry from its prior hold, passes all original requirements plus C02's prerequisite validity and C01's reference checks, and is in recomputed ACTIONABLE. A different independent action does not satisfy this route's resume contract.
6. No unresolved gate or governance exclusion applies to this route. Other independent waiting branches do not veto it; a shared missing prerequisite does. Calculation itself has no execution effect.

Persisted support includes contract/policy IDs, named route/action and target, admissible producer/trust reference, obligation IDs, evidence/admission/observation IDs, current evaluation context, accepted transition/attempt lineage, and current prerequisite proof references. Store no ambient-time inference. If currentness requires unavailable external time/generation evidence, keep the corresponding hold. Cold restore recomputes the same predicate as warm evaluation and CLI output.

For the actual frozen E1 snapshot, no external bundle has been accepted. Both branch eligibility and E1 resumption remain false. Isolated synthetic reentry tests must be distinctly labeled and cannot rewrite that rule or state.

## 6. Full frozen-E1 operational restoration inventory

This comparison used the actual frozen manifest/checkpoint/handoff and resolution-plan fields, plus the current importer/model. No real resume was executed. Raw pin reading, embedded hash verification, action/root/slot identity coverage and opaque record retention already exist. They are retained; the corrections below address semantic omissions or incomplete validation.

Let `P` be the manifest-pinned resolution plan, `G` its pinned typed graph, `H` the pinned handoff package, `M` the resume manifest and `S` the suspension checkpoint. Array elements must be joined by canonical typed ID, not by array order. The versioned mapping records exact source pointers after lookup, raw identities, extraction rule/version and acceptance status.

| Required family and authoritative fields | Current limitation | Minimum restored/validated representation |
|---|---|---|
| P `/resolution_actions`: `id`, `primary_operation_class`, `executor`, `effect_boundary`, `stage_role`, `scope`, `actionability_scope` | Basic class/effect imported; contract stage/scope not fully executable | Action contract with exact class/stage/allowed boundary and scope. Explicitly map legacy SOURCE_ACQUISITION plus FACT_ACQUISITION stage without changing semantics. Executor label does not execute anything. |
| `prerequisite_actions`, `external_prerequisites`, `knowledge_requirements`, `unresolved_prerequisites`, `reentry_gate`, `blocked_by_batch_review`, `blocking_result` | Mostly completion prerequisites/status holds; accepted non-PASS knowledge dependencies and factual hold details not fully operative | Typed action, current-proof, knowledge and gate dependencies; accepted AUTHORITY_REQUIRED/BLOCKED knowledge is not coerced to successful completion. Explicit hold reasons/owners. |
| `acceptance_criteria`, `completion_does_not_imply`, `closes_conditions_only_on_accepted_output`, `secondary_stages` | Default PASS/empty inventory on imported action definitions | Bounded rule and per-outcome evidence contract, permitted knowledge outputs, independent root/slot satisfaction obligations. Finite recognized rules only; uninterpreted required prose yields explicit unsupported hold. Secondary stage ordering only when actually required. |
| `authority_rule`, evidence and accepted decision requirements | No authority predicates/entities installed in M | Scoped typed authority/decision references, exact permission class and target, exclusions, consumption/currentness proof, policy governing acceptance. Unknown required authority blocks. |
| `decision_readiness_requirements`, `readiness_gate`, `accepted_decision_requirements`; P decision/input reentry semantics; linked dossiers | No Decision objects | Actual Decision stage/readiness, nine checklist facts, source/dossier identities, alternative/choice bindings, dependencies/interference and reentry routes. Missing input stays FACT_BLOCKED. |
| P `/execution_history`, `/execution_state`, each action `execution_result`; M `/execution_result_artifacts`, `/completed_actions`, `/blocked_actions` | History retained as text; current statuses omit bounded attempts/result contracts | Immutable authenticated historical attempts and accepted knowledge, outcome/result identities, current hold/overlay lineage. Cross-check summaries against accepted evidence; do not trust status lists as readiness proofs. Do not fabricate native events for prose history. |
| `reentry_on_accepted_evidence`, P budget/decision-input reentry semantics | Generic receipt can select an action with default contract | Named receipt -> factual revalidation -> reevaluation routes, current original conditions, new attempt identity and outcome contract; accepted partial/negative evidence does not reopen the route. |
| P `/normalized_root_conditions`: prerequisites, `condition_completion_rule`, resolution actions, authority, evidence; deferred conditions | Placeholder proof knowledge and final-action routes | Independent completion predicates for accepted complete proof, required ancestors and conditional rules; explicit unresolved/stale/unsupported states. A final action PASS alone is not satisfaction. Preserve cut-count versus deferred-condition counting. |
| G TEMPLATE1_SLOT fields: source, producer, derivation, validator, consumer, identity/value types, governing authority, pipeline links, missing links, root dependencies, resolved value/scope | Mostly type/state/evidence identity; missing operational field-contract links | Existing ValueSlot/GraphEntity/Predicate relationships for all relevant links and accepted baseline resolution evidence. Mandatory source/producer/mapping/authority/consumer links stay separately provable; UNKNOWN is not an invented entity. |
| G assertions/entities: identity domains, acceptance class, source, scope/lineage/currentness, REQUIRES and other operational relations | All original records appended as opaque assertions | Explicit map of operational rules to supported typed relationships/predicates, with source acceptance preserved. Non-operative relations remain opaque with a disposition. Unsupported rule needed for a decision/slot must block explicitly. |
| M `/architect_records`, `/candidate3_construction_authority`, `/subject_pins`; associated records and S authority bindings | References retained without all operational authority state | Exact content and authority identity separation, decision/dossier/choice/target bindings, historical accepted scope and exclusions, consumed/unconsumed evidence. Preserve candidate-only VALID_UNCONSUMED; not a live applicability grant. |
| H `/control_transfer_items`, `/external_request_bundles`, `/common_evidence_contract`, `/resume_rule`; M `/request_routes`, waiting/receipt/reentry lists | Boundaries mostly hold endpoint IDs; only budget has detailed typed gate | Typed representation of each represented frontier contract: missing propositions, acceptable producer (or explicitly unknown), authentication, freshness, scope/lineage, identity boundary, receipt admission criteria and named downstream reevaluation. Unknown producer competence remains a gate. No automatic external request. |
| Budget external contract `/proof_obligations`, source/target pins and normative phase rules | Eight obligations represented; source/decision relationships not fully restored | All eight independent currentness/applicability proofs plus source authenticity/identity constraints and decision exclusion. EXECUTION-to-REQUEST requires its stated normative support. |
| M `/embedded_selection_policy`; P `/selection_policy` including extensions; S policy document binding | Policy bytes verified but not bound to executed map | C05 verified supported policy/version/static class map and fallthrough rules. No file-path-based trust alone. |
| S `/state`, `/bindings`, `/resume_condition`; M resume/mismatch rules, state/control/count summaries; P goals/readiness definitions | Suspended report reproduced from reduced projection; full run goal coverage not a checked import contract | Explicit full-run scope and required-goal inventory, authority-preserving suspension restriction and C03 proof predicate. Validate redundant counts and control/actionable summaries only after independent computation; they are oracles, not algorithm inputs. |

For completeness, action `title`, `notes`, affected WP labels and source annotations can remain descriptive if they do not establish a gate; affected roots/slots must still resolve as typed references. Any such field containing an actual rule must be mapped or marked unsupported, not ignored because its key sounds descriptive. Graph baseline/proposed DAG corrections remain historical or proposed unless accepted evidence grants a correction; importing does not apply them. M's `source_changes`, `production_effect`, handoff review/global-control references and S preservation metadata remain pinned constraints/audit records, never inferred authorizations.

C06 must create a machine-checked **contract coverage inventory** during implementation: for every required field/record, its source location/identity, operational destination/rule, acceptance basis, and disposition (`ENFORCED`, `EXPLICITLY_UNAVAILABLE`, `UNSUPPORTED_REQUIRED`, or `OPAQUE_NON_OPERATIONAL` with reason). No planner-relevant field may use the last disposition. Every source-manifest member is accounted for; unknown required schema fields fail closed. Omitted obligations must be detectable even if aggregate counts still match.

This is a finite structured contract importer with reviewed normalization, not runtime prose interpretation. The reviewed mapping itself is pinned and tested with more than one supported synthetic instance. Do not copy the old M executable state as the actual-manifest import result. Do not special-case an action's spelling to mark it ready or blocked. Supported source contracts must determine the predicates; IDs merely bind them. When frozen evidence is insufficient to define a necessary rule, record the exact acceptance gap and stop C06 qualification—do not acquire facts, choose an Architect policy or fabricate an evaluator.

## 7. Determinism and observation disposition

The review identified one demonstrated nondeterministic path: sorting cross-domain goals by untyped spelling. Its observable effect is branch tuple ordering for identical canonical state; C04 fixes it. No filesystem-order, wall-clock, random ActionId, predicate-iteration or process-memory dependency was demonstrated. Nevertheless qualification must challenge filesystem enumeration order, all set-valued collections, predicate/operand/reference order, policy-map object keys, action/root/slot/goal order, and source-manifest order. Compare complete semantic outputs and canonical identities, not just selected ID or scalar control. Preserve causal array order; reordered event histories must be rejected rather than normalized.

Both minor findings are **FIX_BEFORE_REQUALIFICATION**: F05 affects determinism; F06 affects persistence and policy trust. Neither meets the user's deferral criteria. No minor finding is deferred.

| Observation | Primary disposition | Bounded handling |
|---|---|---|
| O01 trusted fixture/admission boundary | DOCUMENT_ONLY | C06/C07 document reviewed mapping acceptance versus hash identity and explicitly synthetic trust. Retain existing receipt adversarial controls. Do not add online signatures or an authority service. |
| O02 declared-goal scope | TEST_HARDENING | Preserve valid partial-snapshot semantics; C06 verifies full imported run's required-goal coverage. Add a partial goal success control and reject missing required goals in full-run import. Do not call O02 a newly discovered fail-open bug. |
| O03 existing guardrails/deferred absence | TEST_HARDENING | Re-run current negative controls and audit no effects/deferred integrations. No additional runtime feature. |

## 8. Actual frozen-manifest readiness test (N-REAL)

This is a **future C06/C07 non-effecting validation test**, not executed by this planning task. It does not release suspension or run any selected action.

1. Start a new Python process with an empty temporary output directory and no prior planner objects. Inputs are the actual frozen `docs/experiments/E1/E1_RESUME_MANIFEST_1.json`, its checkpoint, pinned referenced sources, supported policy and reviewed mapping version. Do not supply the M replay snapshot as initial state.
2. Verify raw and embedded identity domains, checkpoint identity, full ledger/state/policy bindings, authority semantic identity rules and every required contract proof pin. Never repin a mismatch. Historical stale references are retained as historical with explicit acceptance/currentness limits; no silent freshness upgrade.
3. Import the complete operational contract inventory in section 6. Run C01 admission and C02 enforcement validation. Check goal/slot/root/action coverage and exact typed authority/evidence/decision/result/reentry contracts. Incomplete required semantics produce a precise failing readiness diagnostic.
4. Recompute all root/slot qualifications, readiness, ACTIONABLE, selection, holds, frontier, control and C03 resume proof solely from admitted contracts and evidence. Retain source identities and derivation traces.
5. Separately read the pinned manifest, handoff and checkpoint as an **oracle**. Compare their mutual consistency and the computed state. The frozen records currently describe suspension/MIXED_WAIT, empty machine/human-ready sets, no received evidence, 27 unresolved roots, 41 unresolved slots and Candidate-3 authority VALID_UNCONSUMED. These values are not injected into predicates or control calculation, and are not numeric shortcuts in the importer.
6. Persist a new isolated canonical bundle; terminate the process. Restore it in another fresh process, recompute and compare operational objects, all reference/contract identities, canonical state, actionable/blocked sets, typed branch/frontier output, policy binding and resume eligibility. Compare meaningful fields, not merely opaque byte counts.
7. In **separate explicitly synthetic copies**, test a supported renamed contract/target and supplied evidence. A complete accepted receipt enables only its legitimate route; applying a separately supplied result in the replay harness must obey that restored action's actual acceptance contract. Empty default PASS, partial proofs or invented output are rejected. A declared decision route must reconstruct and enforce its dossier/authority checks. This extension tests semantics, never modifies or operates actual E1.
8. Negative copies outside E1: dangling/stale/wrong-domain target, omitted required contract/goal, conflicting overlay, changed policy, stale ordering, missing receipt proof and changed source bytes. Fail before operational use with exact diagnostics. Their checksums may be recomputed only for synthetic fixture identity, never to authenticate altered frozen evidence.
9. Compare the complete frozen file inventory before/after, require 10,911 identical paths and hashes, and assert no authority consumption, network acquisition, request sending, implementation effect, Template-1/Candidate-3 construction or planner action execution in the real-manifest readiness path.

“Ready to restore and compute a suspended state” is separate from `E1_RESUME_ALLOWED`. Successful N-REAL must still report no actual E1 resumption permission for the frozen input.

## 9. Requalification gate

All conditions below are conjunctive. A failing/missing item keeps current status CORRECTION_REQUIRED; passing the original suite alone does not restore qualification.

- F01–F04 CLOSED with independent before-fails/after-passes counterexamples; F05/F06 CLOSED; observations handled as above.
- C01–C06 accepted; original A–N and X01–X11 PASS with no waiver, skip or NOT_YET_APPLICABLE.
- Importer, CLI, policy binding, full cold resume, actual frozen-E1 operational import/validation, persistence and seven global controls PASS.
- Fresh-process repeated suites and controlled permutations preserve complete outputs and canonical identities. Equal-spelling typed IDs, source/predicate/reference ordering and phase/history distinctions are included; two hash seeds alone are insufficient.
- Required fail-open counterexamples no longer reproduce; **fail-open paths = 0 and hidden nondeterminism = 0 within the tested v0.1 scope**, not an unprovable universal software-security claim.
- All 10,911 frozen E1 files byte-identical; historical qualification/review/authority records preserved; no E1 resume; no production effects; deferred-scope violations = 0; affected repository regressions PASS; links/JSON/whitespace/change scope validated.
- New qualification evidence records commands, test identities, rule/mapping/policy/code/source hashes, exact output identities, counterexample results and limits. Evidence for closing a finding must not reuse the failing computation as its only oracle.
- A fresh independent adversarial review examines corrected enforcing paths and new mutations. Only QUALIFICATION_CONFIRMED or QUALIFICATION_CONFIRMED_WITH_MINOR_FINDINGS with **no open correctness/determinism/persistence/authority/resume-affecting finding** permits status 2 to say QUALIFIED. Any required new correction returns to its owning package or an explicitly bounded follow-up plan.

## 10. Planning report

```text
ADVERSARIAL_VERDICT = QUALIFICATION_REQUIRES_CORRECTION
MAJOR_FINDINGS = 4
MINOR_FINDINGS = 2
OBSERVATIONS = 3
ROOT_CAUSE_GROUPS = [RC-REFERENCE-INTEGRITY, RC-STALE-OBLIGATION,
 RC-RESUME-PROOF, RC-OPERATIONAL-RESTORATION, RC-TYPED-ORDERING,
 RC-POLICY-BINDING]
CORRECTION_WORK_PACKAGES = [C01, C02, C03, C04, C05, C06, C07]
FIRST_CORRECTION_PACKAGE = C01
REQUALIFICATION_GATE = ALL_REQUIRED_CORRECTIONS_AND_COUNTEREXAMPLES_PASS +
 A_N + X01_X11 + N_REAL + DETERMINISM_PERSISTENCE_CONTROLS +
 PRESERVATION + FRESH_INDEPENDENT_ADVERSARIAL_REVIEW
REAL_E1_COLD_RESUME_TEST_DEFINED = YES
E1_ARTIFACTS_MODIFIED = 0
IMPLEMENTATION_MODIFIED = NO
PRODUCTION_EFFECT = NO
```
