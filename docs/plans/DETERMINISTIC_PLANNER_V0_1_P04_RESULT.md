# Deterministic Planner v0.1 — P04 result

WORK_PACKAGE = P04
RESULT = PASS
PLAN_IMPLEMENTATION_MISMATCH = NO

## Scope and prerequisites

Verified P04 against the [implementation plan](DETERMINISTIC_PLANNER_V0_1_IMPLEMENTATION_PLAN.md), [acceptance matrix](DETERMINISTIC_PLANNER_V0_1_ACCEPTANCE_MATRIX.md), and accepted [P01](DETERMINISTIC_PLANNER_V0_1_P01_RESULT.md), [P02](DETERMINISTIC_PLANNER_V0_1_P02_RESULT.md), and [P03](DETERMINISTIC_PLANNER_V0_1_P03_RESULT.md) results. The 56 existing planner tests passed before implementation.

P04 implements decision readiness, bounded decision-input reentry, partial knowledge retention, human review batching, and importing an already authenticated scoped decision followed by an explicit reevaluation event. The fixture adapter consumes reviewed historical assertions and pinned dossier evidence; it does not author dossiers or interpret prose at runtime.

P05 external receipt/gate lifecycles, branch suspension, global frontier/control classification, and P06 complete E1 import/cold restore/CLI remain deferred. `HumanRouting.NO_INTERNAL_ACTION` means only that this scheduler has no internal selection; it does not classify global exhaustion as a defect, wait, or terminal state. No E1 action was executed or resumed.

## Files

FILES_ADDED:

- [E_P04.json](../../adapter/tests/fixtures/planner_v0_1/E_P04.json)
- [F_P04.json](../../adapter/tests/fixtures/planner_v0_1/F_P04.json)
- [G_P04.json](../../adapter/tests/fixtures/planner_v0_1/G_P04.json)
- [H_P04.json](../../adapter/tests/fixtures/planner_v0_1/H_P04.json)
- [I_P04.json](../../adapter/tests/fixtures/planner_v0_1/I_P04.json)
- [test_planner_e1_replay.py](../../adapter/tests/test_planner_e1_replay.py)
- This result document.

FILES_MODIFIED:

- [model.py](../../adapter/planner/model.py): extends existing immutable snapshots/actions/results with typed decision stages, readiness classifications, nine checklist kinds, bounded dossiers, routes, dependencies/interference, and recorded-decision/reentry events. Reuses existing identities, predicates, provenance and authority entities.
- [gates.py](../../adapter/planner/gates.py): independent readiness evaluation, mandatory factual inputs, exact bounded outcome/dossier validation, non-effecting input requirements, and review-only human actionability. Missing input routes, stale evidence and incomplete checks fail closed.
- [core.py](../../adapter/planner/core.py): lifecycle transitions, accepted partial knowledge, explicit reentry of the affected held decision, machine-first scheduling, independent human groups, dependency-cycle checks, record import and separate downstream reevaluation.
- [codec.py](../../adapter/planner/codec.py): canonical persistence of P04 additions in the existing snapshot/bundle/append-only ledger; source invalidation through dossiers/checks; explicit `E1-SELECTION-1-P04` policy version. New default fields are omitted to preserve earlier canonical forms.
- [replay.py](../../adapter/planner/replay.py): bounded E–I fixture loader with raw-file pins and exact JSON-pointer or section/excerpt verification. Expected results remain harness-only.

The selector module, existing P01–P03 tests, source manifest, backlog, implementation plan, acceptance matrix, earlier result artifacts, and production implementation are unchanged.

## Decision semantics

An accepted semantic authority requirement records a route; it is not readiness. An existing complete dossier must independently pass every check before human review can become actionable. Otherwise the named input action or external input requirement remains explicit. The external route here is metadata only, not P05 evidence acquisition or receipt handling.

Input execution retains its own bounded outcome. PASS requires the supplied dossier to match the action contract and all nine independent checks to pass. BLOCKED can preserve accepted partial knowledge and a fact-blocked dossier without completing the action. Required decision facts and explicitly deferred downstream facts are separate fields; unknown owner/selector facts cannot be silently deferred. Dossier alternatives remain proposals.

Lifecycle histories persist the permitted transitions through semantic gap, required inputs, acquisition, dossier readiness and decision readiness. Already complete admitted inputs can take the explicit required-inputs-to-dossier route. Unknown stages, illegal shortcuts, wrong-decision dossiers, changed pre-state identities, missing routes and repeated completed attempts are rejected. No supplied result contains root or slot setters. Preparation transitions preserve domain root/slot state.

Human actionability permits review only. The human action retains the recorded production-effect classification of the external decision; this is not permission for the scheduler to execute it. Independent machine work is selected while available. For human-only work, `NEXT_ACTION` is absent and independent ready decisions form a batch. Explicit dependencies block dependent decisions until their records are valid; interference splits review groups and invalidates an affected dossier after a conflicting recorded choice. Fact-blocked decisions never join a batch. The pure selector remains total; human-only scheduling deliberately does not call it.

`apply_recorded_decision` imports already admitted, authenticated evidence bound to the exact decision ID, dossier identity, scope, choice and DECIDE permission. It rejects wrong class, target, decision, scope, expiry, consumed evidence, unlisted choice, missing choice evidence and replay. It creates no authority entity and changes no root/slot. `apply_decision_reentry` is a separate pre-state-bound ledger event; it reopens only named downstream routes and recomputes their original gates. Synthetic controls test this API without issuing or importing an actual E1 decision.

## Replay acceptance

E1_REPLAY_CASES_IMPLEMENTED = [E, F, G, H, I]
E1_REPLAY_CASE_RESULTS = {E: PASS, F: PASS, G: PASS, H: PASS, I: PASS}

Each fixture includes GIVEN, WHEN, THEN and MUST NOT and identifies itself as a partial historical slice. It does not claim to reconstruct the complete E1 graph.

| Case | Evidence and result | Rejected behavior |
|---|---|---|
| E | Existing S-BINDING inventory plus [S-CONTEXT result](../experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_S_CONTEXT_1_RESULT.md): both bounded inventories PASS, retain knowledge, leave roots/slots unchanged. | Treating inventory completion as field production or condition satisfaction |
| F | [S-EXEC result](../experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_S_EXEC_1_RESULT.md) and [Batch-1 corrected assessment](../experiments/E1/E1_TEMPLATE1_ARCHITECT_DECISION_BATCH_1.json): historical S-EXEC remains PASS; DEC-EXEC remains FACT_BLOCKED with its external input route. A separately labeled synthetic authority-required result tests the lifecycle invariant. | Rewriting historical S-EXEC as AUTHORITY_REQUIRED, exposing premature human readiness, or inventing independent executable policy |
| G | [Budget dossier](../experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_INPUT_BUDGET_1_DOSSIER.json) and [independent readiness attestation](../experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_INPUT_BUDGET_1_RESULT.md): INPUT-BUDGET completes, all nine checks pass, DEC-BUDGET becomes ready, INPUT-IMPLEMENTATION is selected at criterion 3. | Adopting A/B/C, inferring current applicability, executing mapping, or promoting budget root/slot |
| H | [Implementation dossier](../experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_INPUT_IMPLEMENTATION_1_DOSSIER.json) and [result](../experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_INPUT_IMPLEMENTATION_1_RESULT.md): BLOCKED preserves partial knowledge; missing IMPLEMENTATION-OWNING-SOURCE and IMPLEMENTATION-SELECTOR remain explicit; DEC-BUDGET alone forms a human handoff. | Inventing a domain/selector, completing the blocked input action, or executing DEC-BUDGET |
| I | Separate [Batch-1 dossier stage](../experiments/E1/E1_TEMPLATE1_ARCHITECT_DECISION_BATCH_1.json): exactly DEC-BINDING, DEC-IGNORED and DEC-VALIDATOR are batched. Their questions, scopes, alternatives and exclusions remain independent. | Including DEC-EXEC, mixing this stage with later G/H knowledge, merging authority semantics, or lexical human execution |

Frozen provenance is checked against raw hashes and exact source locations before use. Checklist assertions are reviewed deterministic normalizations of the accepted dossiers/attestations, not automated semantic extraction. Source identity authenticates the recorded snapshot, not live applicability. The earlier C/D fixtures and selector expectations remain passing.

## Tests and invariants

Commands:

- `python3 -B -m unittest discover -s adapter/tests -p 'test_planner*.py' -q`: 79 tests passed, including 56 existing tests and 23 P04 tests.
- `python3 -B -m unittest discover -s adapter/tests -p 'test_invocation_constructor.py' -q`: 5 affected-boundary repository regressions passed.

TESTS_PASSED = 84
P01_REGRESSION = PASS
P02_REGRESSION = PASS
P03_REGRESSION = PASS

| Invariant | Status through P04 | Evidence/limit |
|---|---|---|
| X01 historical evidence/currentness | NOT_YET_APPLICABLE | Existing pinned scope/generation checks pass; complete budget applicability replay remains P05 |
| X02 semantic versus ordering | PASS | Existing P03 controls preserved; explicit decision dependency cycles also fail closed |
| X03 permission classes | PASS | Existing controls preserved; record import rejects CONSTRUCT in place of DECIDE, wrong target/scope and consumed grants |
| X04 authority reference/applicability | NOT_YET_APPLICABLE | Complete reference-to-applicability reentry remains P05 |
| X05 missing facts versus decisions | PASS | Actual F/H gaps block readiness; all nine checks are mandatory; each missing owner/selector blocks; G is the positive complete control |
| X06 missing producer | PASS | Existing negative and positive P03 controls preserved |
| X07 PASS versus satisfaction | PASS | E/G preparation leaves roots/slots unchanged; incomplete input cannot be relabeled PASS; P03 independent positive proof controls preserved |
| X08 placeholders versus evidence | PASS | Existing P03 controls preserved; missing factual inputs/dossiers cannot become ready by label or majority vote |
| X09 effecting versus pure validation | PASS | Existing closed pure-validator controls preserved; human-review computation touches no file/network effect sentinel; production-effect input acquisition is rejected |
| X10 stale-source invalidation | PASS | Existing P02/P03 controls preserved; stale dossier or independent check source blocks readiness, preserves unrelated input actionability and survives round trip |
| X11 identity semantics | PASS | Existing typed-domain controls preserved; P04 records also bind exact decision/dossier identity and choice |

These PASS classifications cover the implemented guards. They do not claim P05/P06 completion, live authority authentication infrastructure, full WorkAuthorization issuance qualification, or actual E1 resume.

## Determinism and persistence

DETERMINISM_TESTS = PASS
PERSISTENCE_ROUND_TRIP = PASS

Tests cover all action permutations of F/G/H/I, reversed state collections, ten repeated reload/recomputation cycles per case, reversed JSON object keys, nested dossier/check/alternative permutations, canonical serialization, identical semantic pre-state IDs, deterministic selections and transitions. Human batches remain stable and do not introduce an automatic next action. The 49-order/100-replay C/D controls still pass.

New decision stages, histories, dossier provenance/checklists, required/deferred facts, action outcome contracts, human dependencies/interference and recorded choices are in the existing canonical snapshot. Readiness and scheduling are recomputed from these persisted inputs. Default-field omission preserves P01–P03 wire forms; P04 state is rejected under a pre-P04 bundle policy.

E–I persistence tests use the existing source verification, immutable bundle/event files and append-only hash chain. New result types use the same ledger. Synthetic recorded-decision and explicit reentry events round-trip without changing authority entities or root/slot state. No process-only fact is required to recover the tested actionability, selection, readiness or routing.

## Preservation and next package

Baseline inventories are recorded in `/tmp/planner_p04_before.json` and `/tmp/planner_p04_untracked.json`. The complete E1 inventory was additionally cross-checked against the prior P03 inventory, including its frozen cache files. All 10,911 E1 files remain byte-for-byte unchanged, with no additions/deletions. Backlog, implementation plan, acceptance matrix and P01–P03 results remain unchanged. Only the five modified and seven added files above belong to P04. Existing untracked work was preserved.

Validation includes source-pin/projection checks, result-document links, complete frozen inventory comparison, change-scope verification, `git diff --check` and whitespace checks for the untracked implementation/fixture files. No execution-status convention is defined by the plan, so its bytes were not changed.

NEWLY_ELIGIBLE = []
ALREADY_ELIGIBLE = [P05]
NEXT_WORK_PACKAGE = P05

P05 was already eligible after P02/P03 and is next by the listed package sequence. P04 supplies one prerequisite for P06; P06 still requires P05. Neither P05 nor P06 was implemented.

E1_ARTIFACTS_MODIFIED = 0
DEFERRED_SCOPE_VIOLATIONS = 0
PRODUCTION_EFFECT = NO
