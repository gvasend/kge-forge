# C06A-3 — contract verification stop

WORK_PACKAGE = C06A-3  
RESULT = BLOCKED  
EXCEPTION = C06A_3_CONTRACT_MISMATCH

No implementation or test changes were made. Execution stopped at the independent-contract prerequisite. This result does not supersede the accepted C06 repair, reopen F03, or alter the historical C06A-2 completion record.

## Assigned scope and prerequisite

The authoritative [remaining-contract matrix](DETERMINISTIC_PLANNER_V0_1_C06A_REMAINING_CONTRACT_1.json), `/closure_packages` entry `C06A-3`, assigns O01, O02, O03, O06, O08, O09, O10 and O16. Its prerequisite is C06A-2 PASS. The original partial result plus additive [oracle completion](DETERMINISTIC_PLANNER_V0_1_C06A_2_ORACLE_COMPLETION_1.md) records that prerequisite as complete; this implementation attempt independently checked the supporting executable contract.

The assigned implementation boundary is `adapter/planner/replay.py:import_e1`, using existing model/codec/gates and persistence. It must replace the M executable projection with finite source mappings, restore historical overlays and independent root/slot proofs, and preserve refined C06 accepted knowledge. Decision/authority integration, receipt/reentry integration and complete control/cold integration remain assigned to later packages.

Inputs consumed during verification:

- [Mapping registry](DETERMINISTIC_PLANNER_V0_1_C06A_2_MAPPING_1.json): MAP-O01, MAP-O02, MAP-O03, MAP-O06, MAP-O08, MAP-O09, MAP-O10 and MAP-O16, with exact field inventory and source pins.
- [Bounded result oracles](DETERMINISTIC_PLANNER_V0_1_C06A_2_ORACLES_1.json) and [fixtures](DETERMINISTIC_PLANNER_V0_1_C06A_2_FIXTURES_1.json): OR-BINDING, OR-CONTEXT and OR-PREP-VALIDATOR; three positives and 48 negative cases declared by that contract. Their implementation tests were not run after the prerequisite stop.
- [Completion contract](DETERMINISTIC_PLANNER_V0_1_C06A_2_ORACLE_COMPLETION_1.json) and [fixtures](DETERMINISTIC_PLANNER_V0_1_C06A_2_ORACLE_COMPLETION_1_FIXTURES.json): proof, decision and overlay reference semantics. Only assigned portions would be integrated in this package.

Acceptance includes canonical member preservation, source-bound predicates, explicit blocking for unsupported required semantics, no root/slot promotion from action results, and complete assigned-field inventory. Required tests explicitly include **two baseline slot proofs**, in addition to non-budget bounded results, stale prerequisites, history conflicts and alternate source instances.

## Exact contract mismatch: O09 baseline proof admission

The completion's `/family_rules/root_slot/target_registry` records these two baseline targets:

| Target | Independent recorded restriction | Executable admission profile supplied |
|---|---|---|
| `slot:authenticated_inputs.InvocationAttemptId` | INSTANCE_IDENTITY; candidate identity only, no issuance/use | Absent |
| `slot:authenticated_inputs.profile_sha256` | CONTENT_IDENTITY; released profile content digest, not authority identity | Absent |

Both registry entries use `registered_rule = ALL_CURRENT_INDEPENDENT_SLOT_OBLIGATIONS`. They preserve values, pipeline status, source graph pointers and resolution scope. They do **not** instantiate the reference evaluator's required `proof_contracts` for those targets: exact required source records, record kinds/roles/claims, dependency predicates and proof-support bindings. The entries themselves warn that current state is a cache, not proof; their validator pipeline is partial. Merely copying `baseline_value` or `ESTABLISHED_FOR_RESOLVED_VALUE` into an accepted proof would evade that distinction.

This is not a demand for new live evidence or full issuance qualification of either baseline value. The missing contract must establish precisely the already-recorded limited historical resolution scope, with independently specified source predicates and invalidation behavior.

Concrete executable evidence:

1. The reference specification's `proof(target)` reads `state.base.proof_contracts[target]` and checks the explicit `requirements` records, their claims/roles/kinds, dependencies, optional authority decision and slot value/type. It does not consume the 77-target registry or implement `ALL_CURRENT_INDEPENDENT_SLOT_OBLIGATIONS` as a registered source-specific rule.
2. Across all 104 completion fixtures, the complete set of executable proof-contract target keys is exactly `[root:qualified, slot:qualified]`. Neither baseline target occurs anywhere in those fixtures.
3. The positive generic proof demonstrates that admitted SOURCE and MAPPING predicates can compose. It does not establish which source claims constitute either baseline E1 proof. Pinning an implementation-chosen admission profile would make that choice its own oracle.
4. MAP-O09 explicitly distinguishes field-mapping completeness from operational oracle coverage. Its transformation preserves pipeline links, partial status, baseline value and scope; it supplies no missing proof-admission predicate.

Therefore the required two baseline proof tests lack the independent instantiated acceptance contract required at entry to C06A-3. This contradicts the completion's readiness claim **for this concrete assigned acceptance obligation**. It does not establish that all other completed oracle families are defective.

Current code inspection confirms `import_e1` still loads the descriptor's `normalization` through `load_p05_fixture` and retains raw graph records as `P06_PINNED_OPAQUE_RECORD`. That identifies the planned implementation boundary; it is not used to define the missing oracle. No actual E1 import/readiness/resume operation was performed.

## Verification and stopping boundary

The embedded reference program's SHA-256 was checked against its declared digest. All **104 existing specification cases** were evaluated with the independently supplied profiles and matched their declared expected fields. These are specification checks, **not planner qualification tests**. Passing them does not fill the absent baseline profiles.

The machine-readable [contract check](DETERMINISTIC_PLANNER_V0_1_C06A_3_CONTRACT_CHECK.json) records each result, fixture target inventory and preservation check.

- O09: CONTRACT_MISMATCH for baseline proof admission.
- O01/O02/O03/O06/O08/O10/O16: implementation conformance NOT_EVALUATED after prerequisite stop; no claim of ALREADY_CONFORMANT or NONCONFORMANT_REPRODUCED.
- Pre-repair planner counterexamples and new failing regressions: NOT_RUN, because the contract-verification stop precedes implementation testing.
- Positive/negative planner fixtures, cross-oracle integration, source invalidation, A–N, X01–X11, C01–C06, cold resume, CLI and constructor regressions: NOT_RUN in this attempt. Prior accepted results are not relabeled as new test passes.
- Planner determinism and persistence round trip: NOT_RUN. No implementation changed.

## Minimum prerequisite repair

Before retrying C06A-3, independently instantiate the two baseline proof contracts using their existing governing artifacts:

1. Enumerate exact source assertions/evidence and their selectors, identity domains, acceptance predicates and provenance/currentness scope for each limited baseline value.
2. Define executable positive profiles for those targets and a deterministic bridge from the recorded source contracts to the proof inputs. Keep partial consumer validation separate from the accepted limited resolution.
3. Supply negatives for missing/stale support, wrong identity domain/value/target, substituted source, scope expansion and unsupported mapping; include source invalidation through persistence/reload.
4. Demonstrate those profiles against the independent reference specification without planner-derived expected proofs. If governing evidence does not support a required predicate, preserve that gap explicitly instead of inventing admission.

This result defines no implementation repair and does not perform that prerequisite contract work.

## Coverage, next gate and preservation

No elements are promoted. Total remains 17; RESTORED_AND_QUALIFIED remains 2 (O13 synthetic budget profile and O14 policy binding); remaining coverage remains 15. O09 is blocked at the baseline proof-oracle gate. Other prior readiness labels are not revoked wholesale, but this package cannot proceed with an unsatisfied assigned prerequisite.

C06A-4 requires successful C06A-3, so C06A_4_READY = NO. NEXT_PACKAGE = C06A-3 retry after independent baseline proof-oracle completion; C06A-4 is not eligible. C07_RETRY_ALLOWED = NO.

Before verification, per-file SHA-256 was recorded for all files under `adapter`, `docs/plans`, `docs/backlog` and `docs/experiments/E1`. Afterwards every pre-existing inventoried file was unchanged. All 10,911 frozen E1 files were present and byte-identical. Historical plans/results, original qualification, backlog, implementation and tests remain unchanged. Only this result and its contract-check companion are added. No real E1 evidence was created, and no external or production action occurred.

## Report

```text
WORK_PACKAGE = C06A-3
RESULT = BLOCKED
CONTRACT_ELEMENTS_ASSIGNED = [O01, O02, O03, O06, O08, O09, O10, O16]
ALREADY_CONFORMANT = []
NONCONFORMANT_REPRODUCED = []
CONTRACT_MISMATCH = [O09_BASELINE_PROOF_ADMISSION_ORACLE_MISSING]
FILES_ADDED = [DETERMINISTIC_PLANNER_V0_1_C06A_3_RESULT.md,
               DETERMINISTIC_PLANNER_V0_1_C06A_3_CONTRACT_CHECK.json]
FILES_MODIFIED = []
SPECIFICATION_CASES_PASSED = 104
PLANNER_TESTS_PASSED = NOT_RUN_CONTRACT_STOP
POSITIVE_FIXTURES = NOT_RUN_AGAINST_PLANNER
NEGATIVE_FIXTURES = NOT_RUN_AGAINST_PLANNER
CROSS_ORACLE_TESTS = NOT_RUN_AGAINST_PLANNER
SOURCE_INVALIDATION_TESTS = NOT_RUN_AGAINST_PLANNER
E1_REPLAY_CASES = NOT_RUN
NEGATIVE_INVARIANTS = NOT_RUN
C01_C06_REGRESSIONS = NOT_RUN
F03_STATUS = CLOSED
DETERMINISM_TESTS = NOT_RUN
COLD_RESUME = NOT_RUN
PERSISTENCE_ROUND_TRIP = NOT_RUN
TOTAL_REQUIRED_CONTRACT_ELEMENTS = 17
RESTORED_AND_QUALIFIED = 2
REMAINING_COVERAGE = 15
C06A_4_READY = NO
NEXT_PACKAGE = C06A-3_RETRY_AFTER_BASELINE_PROOF_ORACLE_COMPLETION
C07_RETRY_ALLOWED = NO
V0_1_CURRENT_STATUS = CORRECTION_REQUIRED
REAL_E1_EVIDENCE_CREATED = NO
E1_ARTIFACTS_MODIFIED = 0
IMPLEMENTATION_MODIFIED = NO
DEFERRED_SCOPE_VIOLATIONS = 0
PRODUCTION_EFFECT = NO
```
