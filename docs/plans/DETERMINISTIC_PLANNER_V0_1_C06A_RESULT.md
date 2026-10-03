# C06A — contract verification result

```text
WORK_PACKAGE = C06A
RESULT = BLOCKED
STOP_REASON = C06A_CONTRACT_INCOMPLETE
V0_1_CURRENT_STATUS = CORRECTION_REQUIRED
```

Stopped during Step 1, before implementation or a claimed red regression. The full-import gap remains documented; this attempt does not claim the reconciliation's proposed positive counterexample was reproduced. F03's accepted refined repair remains CLOSED.

## Verified package scope

The [reconciliation](DETERMINISTIC_PLANNER_V0_1_C06_C07_RECONCILIATION_1.md) assigns remaining O01–O13/O15–O17 full-import obligations to C06A, preserving the refined O02 dependency and O14 policy binding. Required work includes reviewed source-to-contract mapping; action/result, decision/dossier, authority/evidence, history/overlay, root/slot/goal and frontier contracts; field coverage/disposition; cold persistence; independent positive/negative continuation tests. Existing model/core/gates/codec/replay boundaries must be retained. C06A must not run C07 or grant qualification.

The package specifically requires first pinning an independently supported positive bounded result contract, supplying that valid result through the actual importer/result path, and demonstrating erroneous rejection. It also requires a supported decision-route example. It explicitly instructs stopping if exact evidence does not define the supported positive contract. The present instruction independently requires stopping when executable requirements are insufficient.

## Exact unresolved contract

The frozen plan's `FACT-BUDGET-APPLICABILITY` acceptance criteria require a complete exact matrix covering authenticity, identity/type, publication, scope/phase, lineage, runtime, G4/store, profile and temporal/single-use facts. They distinguish missing evidence, incompatible evidence and missing normative applicability. These are meaningful requirements, but they do not supply the missing governing evidence-validation rules themselves.

The referenced [external evidence request](../experiments/E1/E1_BUDGET_APPLICABILITY_EXTERNAL_EVIDENCE_REQUEST_1.md) makes the limitations explicit:

- Common contract/currentness: a governing freshness rule and independently trusted current anchor are required; no invented TTL.
- Temporal-currentness obligation: concrete qualified producer is unknown; governing validity/usage rule and current anchor must accompany evidence.
- Execution-to-request obligation: an existing adopted phase rule or scoped applicability decision and exact application must be supplied; receiver cannot create applicability.
- Minimum evidence set: actual source formats, trust chains and producer availability are unknown.
- Receipt prerequisites: existing trust anchors and governing identity/validation rules must be available; missing anchors block.

Consequently, the specified source-level positive oracle still needs a finite reviewed rule mapping for the governing proof inputs and their acceptance, and an independently justified complete supplied-result instance. The reconciliation names this as future work but does not establish a supported concrete positive instance. Calling arbitrary typed claims PROVED would assume the conclusion being tested.

This is **not** a claim that real external evidence must arrive before any planner testing or implementation is possible. Synthetic tests are permitted. What is missing for this mandated pre-repair proof is an explicit supported synthetic contract that instantiates those rule/authority inputs without being mistaken for restoration of an existing adopted E1 rule. A test fixture may invent test data, but cannot be the sole authority for the source-level validity it purports to test.

## Current code inspection

- [replay.py](../../adapter/planner/replay.py), `import_e1`, still starts with the pinned M normalization and adds accepted-knowledge dependencies plus opaque source records. That establishes the known structural gap, not a new successful red test.
- [gates.py](../../adapter/planner/gates.py), `validate_result`, rejects an empty accepted inventory with `no accepted bounded result contract`. The new positive test needs an independently valid supplied result before this rejection can be classified as incorrect. The already-passing empty-PASS rejection remains valid and is not relabeled a failure.
- `gates._check_receipt` checks admitted typed claims and producer authentication. It rejects unknown proof rules/producers. It does not independently derive an absent governing E1 freshness/phase rule from a claim.
- [test_planner_e1_replay.py](../../adapter/tests/test_planner_e1_replay.py), `synthetic_receipt`, explicitly creates COUNTERFACTUAL_SYNTHETIC trust and a TEST-attestor. It is appropriate for testing the represented receipt/reentry mechanism. Passing that helper alone is not independent evidence that the complete source-level bounded result satisfies the additional governing rules.

No speculative accepted inventory, new authority, placeholder proof or alternate validation path was added. The decision-route probe and broad regression work were not pursued after the mandatory contract stop.

## Minimum input needed to continue

A bounded executable contract supplement must identify:

1. The supported proof-matrix result schema and precise mapping into typed knowledge/outcome acceptance, including the additional authenticity/identity facts versus the eight applicability rows.
2. Finite supported governing-rule inputs and evaluators for producer competence, freshness/current anchor and phase application; missing/unsupported inputs must remain explicit holds. This is a planner test/import contract, not issuance of E1 authority.
3. An independently reviewed synthetic positive instance, pinned source-rule relationships, and corresponding negative mutations. State exactly which assumptions are synthetic. The positive oracle must not simply reuse the importer or receipt helper's answer.
4. A supported source-declared decision route with exact dossier/choice/authority bindings and positive/negative input expectations, as required by the second counterexample.

These inputs would permit a truthful FAIL_EXPECTED regression before repair. No external evidence acquisition or Architect decision was attempted here. The broader restoration requirements have not been waived or declared impossible.

## C07 retry predicate

| Predicate from reconciliation | Current result |
|---|---|
| Explicit adoption of C06A without waiving section 9 | Satisfied by this request |
| Preserve accepted C01–C06 scope/status records | Preserved; refined F03 remains CLOSED; its regression was not rerun in this stopped attempt |
| C06A PASS with candidate/mapping/source identities and complete coverage | Not satisfied: BLOCKED, no repair or coverage artifact |
| Positive/negative C06A and correction tests on the candidate identities | Not satisfied: no qualifying pre-repair positive oracle or candidate implementation |
| Preservation and no pending acceptance gap | Preservation passes; executable-contract gap remains |

`C07_RETRY_ALLOWED = NO`. C07 and its historical blocked result are untouched.

## Evidence identities and preservation

Raw SHA-256 identities inspected:

| Artifact | SHA-256 |
|---|---|
| Reconciliation 1 | `c238020a48671b8537ed20b675c3a9002d388ec0162f26b41d5a3190ce6b6c31` |
| Frozen graph-resolution plan | `2662971aa42bda300dcea7bf591e95c113b4ed5cb32db1381cd25b024c06e91c` |
| Budget applicability external evidence request | `db073d877995aa7c1665db2252d10bf35a2a93f90a93ff0b84ae77fc44af5ad4` |

The start/end path and raw-SHA inventory comparison confirms all 10,911 frozen E1 files unchanged. All pre-existing adapter, plans, backlog and E1 files are unchanged. Only this result artifact was added. Protected plans, correction history and qualification records are preserved. Relative links, trailing-whitespace checks and `git diff --check` pass.

## Report

```text
WORK_PACKAGE = C06A
RESULT = BLOCKED
STOP_REASON = C06A_CONTRACT_INCOMPLETE
IMPLEMENTATION_GAPS_ADDRESSED = []
TEST_COVERAGE_GAPS_ADDRESSED = []
PRE_REPAIR_COUNTEREXAMPLE = NOT_REPRODUCED (structural gap inspected; valid positive operational oracle not established)
PRE_REPAIR_REGRESSION = NOT_CREATED
POST_REPAIR_COUNTEREXAMPLE = NOT_RUN
POST_REPAIR_REGRESSION = NOT_RUN
FULL_IMPORT_CONTRACT = FAIL (package acceptance not met)
OPERATIONAL_RESTORATION = FAIL (package acceptance not met)
REFERENCE_INTEGRITY = NOT_RUN (no new regression claim)
TESTS_PASSED = 0 (test suites not run after Step 1 stop)
E1_REPLAY_CASES = NOT_RUN
NEGATIVE_INVARIANTS = NOT_RUN
C01_C06_REGRESSIONS = NOT_RUN
F03_STATUS = CLOSED
DETERMINISM_TESTS = NOT_RUN
COLD_RESUME = NOT_RUN
PERSISTENCE_ROUND_TRIP = NOT_RUN
C07_RETRY_ALLOWED = NO
C07_RETRY_PREREQUISITES = [executable positive contract/oracle, C06A repair and complete coverage, passing C06A/correction regressions, full source-preservation gate]
V0_1_CURRENT_STATUS = CORRECTION_REQUIRED
E1_ARTIFACTS_MODIFIED = 0
IMPLEMENTATION_MODIFIED = NO
DEFERRED_SCOPE_VIOLATIONS = 0
PRODUCTION_EFFECT = NO
```

NOT_RUN is used rather than fabricating a PASS/FAIL for tests not executed. The package acceptance failures above are missing acceptance evidence, not newly demonstrated regressions of existing validated paths.
