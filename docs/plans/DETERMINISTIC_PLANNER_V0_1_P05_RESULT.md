# Deterministic Planner v0.1 — P05 result

WORK_PACKAGE = P05
RESULT = PASS
PLAN_IMPLEMENTATION_MISMATCH = NO

## Scope verification

Verified P05's P02/P03 prerequisites, evidence-gate/control interfaces, J–M replay cases, X01/X04/X08 criteria, and P06 boundary against the [implementation plan](DETERMINISTIC_PLANNER_V0_1_IMPLEMENTATION_PLAN.md) and [acceptance matrix](DETERMINISTIC_PLANNER_V0_1_ACCEPTANCE_MATRIX.md). The accepted [P01](DETERMINISTIC_PLANNER_V0_1_P01_RESULT.md), [P02](DETERMINISTIC_PLANNER_V0_1_P02_RESULT.md), [P03](DETERMINISTIC_PLANNER_V0_1_P03_RESULT.md) and [P04](DETERMINISTIC_PLANNER_V0_1_P04_RESULT.md) contracts remain regression-protected. The prior 79 planner tests passed during integration.

P05 adds explicit proof obligations, bounded fact outcomes, external receipt validation, branch-local holds/reentry, seven global control states, and prerequisite-path frontier witnesses. It extends the existing snapshot, predicates, identities, provenance, action results and append-only ledger. No alternate state store or runtime integration is introduced.

M is a reviewed, source-pinned normalization of all 28 cut roots, 43 Template-1 slots and 63 current resolution actions, with the relevant accepted overlays and deferred-condition routes. It is not P06's general E1 importer, operational resume loader or CLI. No frozen E1 state is resumed or changed.

## Files

FILES_ADDED:

- [J_P05.json](../../adapter/tests/fixtures/planner_v0_1/J_P05.json)
- [K_P05.json](../../adapter/tests/fixtures/planner_v0_1/K_P05.json)
- [L_P05.json](../../adapter/tests/fixtures/planner_v0_1/L_P05.json)
- [M_P05.json](../../adapter/tests/fixtures/planner_v0_1/M_P05.json)
- This result document.

FILES_MODIFIED:

- [model.py](../../adapter/planner/model.py): typed evidence/gate IDs, obligations, claims, independently admitted receipt attestations, observations, external lifecycle events, boundaries, goals and branch/global control enums. Explicit non-identity/undefined value-type tags preserve the frozen graph's slot classifications without inventing hash identities.
- [gates.py](../../adapter/planner/gates.py): independent obligation evaluation and receipt identity/producer/target/scope/lineage/generation/currentness checks; waiting and control-boundary gates; no reference-to-applicability implication.
- [core.py](../../adapter/planner/core.py): explicit request/wait/receive/validate/reentry events, accepted partial/negative observations, branch-local scheduling, seven-state control precedence, and deduplicated frontier paths with goal witnesses.
- [codec.py](../../adapter/planner/codec.py): P05 fields/events in the existing canonical codec and ledger, explicit P05 policy version, provenance pins, and stale invalidation through receipt/attestor/obligation dependencies. Legacy default-field omission is preserved.
- [replay.py](../../adapter/planner/replay.py): shared strict pinned fixture reader for P04/P05, including exact JSON-pointer and section evidence. Expectations remain outside planner state.
- [test_planner_e1_replay.py](../../adapter/tests/test_planner_e1_replay.py): 15 P05 tests covering J–M, control truth table, substantive X01/X04/X08 adversarial and positive controls, receipt trust, persistence, invalidation and deterministic replay.

The selector, existing P01–P03 test files, source manifest, backlog, authoritative plan, acceptance matrix and P01–P04 result artifacts are unchanged. P04 tests remain in the extended replay test file and still pass.

## Evidence and reentry semantics

A proof obligation names its proposition, exact target, expected competent producer identities if established, governing source and whether its rule is known. No concrete producer identity is invented for the real budget request. Unknown rules and known rules with missing evidence are separate outcomes. The authority reference retains its approved AUTHORITY_IDENTITY type and `/authority_id` selector; it does not supply any of the eight current applicability proofs.

Receipt events reference concrete admitted evidence; they cannot inject an authority, producer, new proof rule or repaired claim. A separately admitted authentication predicate must establish ATTEST permission for the exact receipt content identity and match the required producer. An identical raw hash, a self-authored wrapper, or a producer with another permission is insufficient. The receipt's canonical body binds producer, target and claims; changing a claim without changing/authenticating those bytes fails identity validation. Scope, lineage, generation and validity use the pinned evaluation context, never wall-clock inference.

Request-ready and waiting are explicit events and imply no sending or receipt. Received is separate from validated. Each accepted partial or negative proposition is retained with its receipt/contract provenance while the gate remains waiting. Rejected evidence retains reasons and contributes no facts. Neither rejected nor partial validation records a successful whole-gate VALIDATED stage. Conflicting accepted proof outcomes cannot prove a proposition.

Only complete independently proved obligations permit EVIDENCE_VALIDATED. A separate DEPENDENT_ACTION_REENTRY event then releases the named reentry action's hold; its original prerequisites still apply. It neither executes that action nor releases downstream MAP-BUDGET. Roots/slots are not result setters. Tests use an explicitly synthetic trust root and budget target for positive receipt controls; no accepted E1 external evidence is manufactured.

## Replay results

E1_REPLAY_CASES_IMPLEMENTED = [J, K, L, M]
E1_REPLAY_CASE_RESULTS = {J: PASS, K: PASS, L: PASS, M: PASS}

Each fixture encodes GIVEN, WHEN, THEN and MUST NOT, with raw source identities and exact locations. They are read-only test inputs, not operational evidence.

| Case | Evidence and computed behavior | Prohibited transition checked |
|---|---|---|
| J | [DEC-BUDGET authority](../experiments/E1/E1_TEMPLATE1_ARCHITECT_DEC_BUDGET_AUTHORITY_1.json) and [eight-proof contract](../experiments/E1/E1_BUDGET_APPLICABILITY_EXTERNAL_EVIDENCE_REQUEST_1.json): exact approved reference is retained; bounded fact result is EXTERNAL_GATE_REQUIRED; all eight current proof obligations remain unproved. | Reference/identity consistency cannot prove applicability, freshness, phase compatibility, root satisfaction or slot resolution |
| K | The [request/receipt contract](../experiments/E1/E1_BUDGET_APPLICABILITY_EXTERNAL_EVIDENCE_REQUEST_1.json): explicit request-ready then waiting events leave the budget branch waiting, with no receipt and no internal selection. | Request creation is not sending or evidence arrival; a skipped receipt stage is rejected |
| L | K plus an explicitly COUNTERFACTUAL_SYNTHETIC independent action: RUNNABLE takes precedence, that action's bounded PASS records only its knowledge, and budget remains suspended. | A waiting branch must not stop independent work or borrow its authority |
| M | [Current plan](../experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_PLAN_1.json), [typed graph](../experiments/E1/E1_TEMPLATE1_TYPED_KNOWLEDGE_GRAPH_1.json), and [handoff routes](../experiments/E1/E1_EXTERNAL_HANDOFF_PACKAGE_1.json): recomputation yields empty actionability, 27 unresolved roots, 41 unresolved slots, exact eight exposed boundaries, MIXED_WAIT and no next action. | Empty actionability is not automatically PLAN_DEFECT, terminal success or permission to create reasoning work |

M normalizes definitions/prerequisites and accepted historical results, not expected actionable/control lists. Root satisfaction is independent of action PASS. The validator-authority root uses its pinned issued grant evidence; removing that accepted evidence changes the computed unresolved count to 28. Both already resolved slots retain their pinned graph resolution evidence. Unresolved non-identity/undefined slot types remain opaque and unresolved, without coercion.

Eligibility and succession remain required through their explicit deferred-condition action chains even though they are outside the 28-root upstream cut. The future current-eligibility boundary is represented but not emitted while earlier prerequisites still block its action. The fixture's expected totals and frontier are harness-only oracle fields.

## Control and frontier

GLOBAL_CONTROL_TESTS = PASS

All seven states are exercised with positive/adversarial controls:

- RUNNABLE: valid independent machine work takes precedence over waiting or a localized declared defect.
- HUMAN_HANDOFF: P04 readiness and independent batching remain in force; a human action is never automatically executed.
- EXTERNAL_WAIT: exposed boundaries have admitted external-evidence contracts and no internal work is available.
- MIXED_WAIT: exposed source/fact or implementation/authority boundaries remain alongside, or instead of, external-evidence waits.
- PLAN_DEFECT: missing control route, unknown required proof rule, unqualified external contract or structural prerequisite defect; no invented repair action.
- TERMINAL_SUCCESS: every declared goal is proved, not merely an empty queue.
- TERMINAL_FAILURE: an explicit proved unrecoverable required-goal failure has no recovery route. Negative currentness evidence alone is not terminal failure.

Frontier traversal follows unsatisfied prerequisite routes from unresolved goals. It stops at exposed control-transfer records, deduplicates by GateId and retains goal/path witnesses. It does not output all blocked descendants or claim mathematical minimum-cut optimality.

M's exact frontier:

- EXT-BUDGET-APPLICABILITY-EVIDENCE
- EXT-REENTRY-S-ANCESTRY
- EXT-REENTRY-S-APPROVAL
- EXT-REENTRY-PREP-AUDIT
- EXT-REENTRY-PREP-RUNTIME_HEAD
- EXT-REENTRY-PREP-SUPERVISOR
- EXT-REENTRY-DEC-EXEC
- IMPLEMENTATION-OWNING-SOURCE + IMPLEMENTATION-SELECTOR

## Tests and negative invariants

Commands:

- `python3 -B -m unittest discover -s adapter/tests -p 'test_planner*.py' -q`: 94 tests passed (79 prior + 15 P05).
- `python3 -B -m unittest discover -s adapter/tests -p 'test_invocation_constructor.py' -q`: 5 repository regressions passed.
- `python3 -B -m unittest adapter.tests.test_planner_e1_replay.P05ReplayTests -q`: 15 P05 tests passed, including the final fixture qualification.

TESTS_PASSED = 99 unique tests
P01_REGRESSION = PASS
P02_REGRESSION = PASS
P03_REGRESSION = PASS
P04_REGRESSION = PASS
C–I_REPLAY_REGRESSION = PASS

| Invariant | Status through P05 | Evidence |
|---|---|---|
| X01 historical evidence/currentness | PASS | Same identity with historical scope, lineage, generation or expired validity is rejected separately; correctly scoped current synthetic evidence is the positive control |
| X02 semantic versus ordering | PASS | Prior semantic-edge, real-cycle and decision-dependency controls preserved |
| X03 permission classes | PASS | Prior construct/issue/use and decision controls preserved; receipt authentication requires the exact ATTEST class and target |
| X04 authority reference versus applicability | PASS | Reference-only J remains unproved; each of eight omitted propositions independently prevents completion; complete authenticated synthetic evidence permits only explicit reentry |
| X05 missing fact versus decision | PASS | P04 F/H missing policy/owner/selector and all-nine-check controls preserved |
| X06 missing producer | PASS | Prior controls preserved; absent concrete budget producer competence cannot be supplied by hash equality |
| X07 PASS versus satisfaction | PASS | Prior inventory/decision controls preserved; fact and receipt outcomes leave governed roots/slots unchanged |
| X08 placeholders versus evidence | PASS | Request-only, no-artifact, empty-claim, unproduced, unvalidated and wrong-kind receipts cannot prove obligations; complete synthetic receipt is the positive control |
| X09 effecting versus pure validation | PASS | Prior pure-registry and no-effect controls preserved; receipt checks perform no issuance or external operation |
| X10 stale invalidation | PASS | Receipt and independent attestor changes invalidate proof/readiness and block reentry; stale independent root proof and tampered persisted trust are rejected |
| X11 typed identities | PASS | Prior domain checks preserved; same producer digest tagged CONTENT_IDENTITY cannot substitute for AUTHORITY_IDENTITY |

All eleven implemented invariant families pass; none is marked PASS merely because its triggering condition is absent. Full A/B/N consumer/cold-resume qualification remains P06, including the actual constructor identity adapter. Synthetic positive trust is reported separately from historical replay and is not new E1 authority.

## Determinism and persistence

DETERMINISM_TESTS = PASS
PERSISTENCE_ROUND_TRIP = PASS

Tests compare repeated replay, reversed action/status/goal/boundary/requirement order, reversed JSON object keys, canonical serialization/reload, selected action, frontier witnesses and branch/global control. Prior selector permutation/replay tests remain passing. Receipt content hashes normalize claim order; ordered ledger/history arrays remain ordered.

All future-planning inputs are in the existing immutable snapshot: obligations, competent-producer requirements, admitted trust references, receipt observations, lifecycle stages/history, holds/reentry targets, goal routes and failure/recovery rules. The explicit `E1-SELECTION-1-P05` version is required for this state; earlier bundles retain their prior bytes/default behavior.

The existing append-only ledger stores each supplied external event. Tests save, restore and recompute after request-ready, waiting, received, validated and explicit reentry transitions. Partial/negative observations survive canonical reload without becoming positive evidence. Changed attestor bytes fail pinned restore. No database, service, ambient clock or conversation history participates in these planner-native round trips.

## Preservation and next package

The before-state inventory and untracked-file baseline are recorded in `/tmp/planner_p05_before.json` and `/tmp/planner_p05_untracked.json`. Final preservation checks compare the complete E1 path set and every raw SHA-256, including its frozen cache files. All 10,911 files are unchanged, with no additions/deletions.

Backlog documents, authoritative plan, acceptance matrix, P01–P04 result artifacts and unrelated files are unchanged. Only the six modified and five added files listed above belong to P05. Existing untracked work is preserved. Result-document links, source references, scope checks, `git diff --check` and whitespace checks for untracked changes pass. The plan defines no execution-status editing convention, so it is unchanged.

NEWLY_ELIGIBLE = [P06]
NEXT_WORK_PACKAGE = P06

REMAINING_V0_1_ACCEPTANCE_GAPS:

- A/B: pure constructor identity adapter and complete Candidate-2/Candidate-3 consumer/input replay.
- N: complete E1 import, manifest-based cold subprocess restore and isolated controlled receipt/reentry qualification.
- P06 developer CLI and final integrated A–N/X01–X11 completion gate, including repeated fresh-process byte equality.

P06 is eligible because P04 and P05 now pass. It was not implemented. Planner v0.1 as a whole is not yet complete.

E1_ARTIFACTS_MODIFIED = 0
DEFERRED_SCOPE_VIOLATIONS = 0
PRODUCTION_EFFECT = NO
