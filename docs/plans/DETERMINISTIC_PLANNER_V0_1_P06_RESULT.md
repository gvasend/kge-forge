# Deterministic Planner v0.1 — P06 result

WORK_PACKAGE = P06
RESULT = PASS
V0_1_STATUS = QUALIFIED

P06 implements the bounded importer, pure consumer integration, CLI and full cold-resume qualification from the [authoritative plan](DETERMINISTIC_PLANNER_V0_1_IMPLEMENTATION_PLAN.md) and [acceptance matrix](DETERMINISTIC_PLANNER_V0_1_ACCEPTANCE_MATRIX.md). P01–P05 prerequisites were verified; no plan/implementation mismatch remains. No later package or deferred feature was introduced.

## Files added

- `adapter/planner/__main__.py`
- `adapter/tests/fixtures/planner_v0_1/A_P06.json`
- `adapter/tests/fixtures/planner_v0_1/B_P06.json`
- `adapter/tests/fixtures/planner_v0_1/N_P06.json`
- `docs/plans/DETERMINISTIC_PLANNER_V0_1_P06_RESULT.md`
- `docs/plans/DETERMINISTIC_PLANNER_V0_1_QUALIFICATION.md`
- `docs/plans/DETERMINISTIC_PLANNER_V0_1_QUALIFICATION.json`

## Files modified

- `adapter/planner/replay.py`
- `adapter/planner/codec.py`
- `adapter/tests/test_planner_e1_replay.py`
- `adapter/tests/test_planner_invariants.py`
- `adapter/tests/test_planner_resume.py`

These lists are relative to the P06 start inventory. The repository already contained untracked P01–P05 work; it was preserved. No implementation-plan execution-status convention was introduced and the plan/matrix were not edited.

## Implementation and acceptance

- `import_fixture` reads the closed `PLANNER-REPLAY-1` schema into the existing typed model. It verifies pinned sources and exact provenance projections, identity types, enums, references and event types. Oracles remain outside core evaluation. Malformed inputs fail closed.
- `consumer_identity_precheck` verifies the actual constructor code pin and calls only `invocation_constructor.identity`. The actual Candidate-2 JSON raises `ConstructionDenied` with `unknown WorkAuthorization schema`, keeping issuance review blocked. This is an explicitly counterfactual earlier preflight using the later reconciliation evidence.
- B retains the actual candidate-only authority identity and independent missing source, producer and mapping predicates. A valid construction grant cannot supply Template-1 or authorize issuance/use. The fixture's bounded evaluation context is historical/synthetic, not a new live applicability finding.
- `import_e1` verifies the frozen resume manifest, checkpoint identity, raw source pins and embedded ledger/state/policy hashes. A versioned, pinned M normalization supplies the executable action/root/slot projection. Coverage is checked against every final plan action, root and graph slot. All 343 graph entities and 962 original assertions are retained verbatim with source pointers as provenance records; original relationships are not silently promoted into ordering. Authority references, execution history, manifest routes and checkpoint metadata survive native persistence. Report oracles are not actionability inputs.
- The canonical bundle format adds an explicitly versioned `FULL_FROZEN_E1_REPLAY` scope while preserving prior P01–P05 encodings. Historical E1 ledger entries remain pinned source records; newly supplied replay events use the existing append-only event chain. No historical prose is semantically extracted.
- CLI: `python3 -m adapter.planner validate FIXTURE`, `plan FIXTURE`, `apply FIXTURE --event EVENT --out DIR`, `replay FIXTURE --out DIR`, `restore MANIFEST --out DIR`. Restore accepts the pinned E1 manifest or a content-addressed native bundle. Machine stdout is canonical JSON; diagnostics go to stderr. Exit 0 includes valid blocks/waits, 2 rejects invalid input/contracts, and 3 reports replay oracle mismatches. Apply performs exactly one supplied event; replay only applies fixture events, including per-step oracle checks. No selected operation is automatically executed.
- Full N restores in independent Python processes into fresh directories and reproduces byte-identical bundles, graph/provenance, action/root/slot state, references, waiting gates, policy version and control. The frozen run remains MIXED_WAIT, with 27 unresolved roots, 41 unresolved slots, no actionable work and no resumption.
- Complete synthetic receipt qualification is isolated from E1. Unrelated, stale, malformed, partial and negative evidence cannot reenter the branch. Complete independently authenticated evidence enables only the named fact-acquisition reentry; roots and slots remain unchanged. The positive reentry ledger is cold-restored in another process; tampered independent trust is rejected.

## Results

E1_REPLAY_CASE_RESULTS = {A: PASS, B: PASS, C: PASS, D: PASS, E: PASS, F: PASS, G: PASS, H: PASS, I: PASS, J: PASS, K: PASS, L: PASS, M: PASS, N: PASS}

NEGATIVE_INVARIANTS = {X01: PASS, X02: PASS, X03: PASS, X04: PASS, X05: PASS, X06: PASS, X07: PASS, X08: PASS, X09: PASS, X10: PASS, X11: PASS}

TESTS_PASSED = 107 unique tests: 102 planner tests and 5 affected constructor regressions. The complete planner suite passed with PYTHONHASHSEED=1 and 97. Repetitions are not counted as additional tests.

P01_REGRESSION = PASS
P02_REGRESSION = PASS
P03_REGRESSION = PASS
P04_REGRESSION = PASS
P05_REGRESSION = PASS
IMPORTER = PASS
CLI = PASS
COLD_RESUME = PASS
DETERMINISM_QUALIFICATION = PASS
PERSISTENCE_ROUND_TRIP = PASS
GLOBAL_CONTROL_TESTS = PASS

The [qualification record](DETERMINISTIC_PLANNER_V0_1_QUALIFICATION.md) and [machine record](DETERMINISTIC_PLANNER_V0_1_QUALIFICATION.json) contain the completion gate and exact deterministic output identities.

## Preservation and scope

All 10,911 frozen E1 paths and SHA-256 values were compared before and after P06. Canonical inventory digest (sorted compact JSON of repository-relative path to raw SHA-256): `1cf25145f69a2fb133c12f3b15cd1089351e4a9cac8624d4b6e970f2b4b3a044`.

Backlog, plan, acceptance matrix, prior package results, authority records and E1 production state are unchanged. `git diff --check` and explicit whitespace checks for the untracked changed files pass. No unrelated source changes were found against the initial inventory.

E1_ARTIFACTS_MODIFIED = 0
DEFERRED_SCOPE_VIOLATIONS = 0
PRODUCTION_EFFECT = NO

NEXT_STEP = Review the qualified v0.1 implementation. E1 remains SUSPENDED_EXTERNAL_HANDOFF with E1_RESUME_ALLOWED = NO; this qualification grants no operational authority.
