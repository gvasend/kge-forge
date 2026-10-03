# C06A-3 RETRY_3 result

**RESULT = BLOCKED — CONTRACT_EXCEPTION CE-01.** No implementation or operational registry was changed. The closed-contract preflight's source-admission claim conflicts with its standalone executable predicates. Implementing either behavior without reconciliation would silently choose semantics, which this attempt forbids.

## Frozen inputs

[Contract-set manifest](DETERMINISTIC_PLANNER_V0_1_C06A_3_RETRY_3_CONTRACT_SET.json) records 48 exact raw-file SHA256 pins, including contracts, mapping/oracle/fixture/validation companions, prior results, and mapping source pins. Its aggregate hashes the canonical path/hash map; metadata is not part of that aggregate.

```text
CONTRACT_SET_IDENTITY = C06A3-ContractSet-sha256:e6069693ec559dcf1531e07fc3ba6fb1de6b47828a2ab1e7600878e4334f7643
```

The [remaining-contract package](DETERMINISTIC_PLANNER_V0_1_C06A_REMAINING_CONTRACT_1.md) assigns O01, O02, O03, O06, O08, O09, O10, O16. The [closure specification](DETERMINISTIC_PLANNER_V0_1_C06A_3_PREFLIGHT_CLOSURE_1.md) is unchanged. Earlier initial, RETRY_1 and RETRY_2 blocked records are preserved.

## CE-01 — required supporting sources are not admitted by standalone predicates

Affected contracts: **O02/O06 HISTORY and O10 GRAPH**; composition interaction: **O16**.

The closure requires pinned current supporting sources for accepted knowledge, hold release and operative graph assertions. It exposes HISTORY and GRAPH as executable admission entry points, with independently supplied trusted profile/validity view and candidate source objects. O16 separately composes those admissions.

Actual executable code is the frozen closure JSON's `/reference/program`:

- `current()` checks the independently supplied validity identity/state and dependency table. It does **not** compare candidate supporting-source bytes with their pin or require their presence.
- `history()` uses that currentness result to admit knowledge and release holds, then calls `source()` only for `plan` and `results`. Required `evidence` and `override` bytes are not checked.
- `graph()` admits the operative assertion using currentness and then checks only the `graph` source bytes. Its required `evidence` source is not checked.
- INSTANCE/`compose()` checks every source role and rejects these same candidates.

This is an admission-contract conflict, not evidence that the existing planner has this runtime defect. The new source-profile path is not implemented. The aggregate protects its own entry point, but no contract declares a mandatory aggregate-only precondition for the independently exposed HISTORY/GRAPH entry points. They are documented as independently testable admission predicates. The implementation cannot silently introduce that precondition or change the frozen reference result.

### Minimal counterexamples

Start with BASE (repeat independently with RENAMED), trusted profile and validity unchanged. Baseline standalone and composed admissions ACCEPT.

| Candidate mutation only | Standalone observed behavior | Composed behavior |
|---|---|---|
| Change evidence `knowledge_type` to `UNRELATED-KNOWLEDGE-TYPE`, or omit evidence source | HISTORY ACCEPT; K-PASS and K-BLOCKED remain current; consumer remains prerequisite-eligible | REJECT |
| Change override source `action` to `UNRELATED-ACTION`, or omit override source | HISTORY ACCEPT; H1 still released and H2 retained | REJECT |
| Change evidence `knowledge_type`, or omit evidence source | GRAPH ACCEPT; EDGE1 and its operational prerequisite edge retained | REJECT |

All mutations are applied before canonical serialization/reload. In substitution cases, the actual source digest differs from the unchanged trusted expected digest. Omission leaves no source payload. No profile, validity attestation, accepted-result record, graph assertion, or expected pin is edited to admit the mutation.

**12/12 variants reproduce CE-01** (three paths × two mutations × two independent bases). Exact inputs are reconstructible from the pinned fixture bases and the mutation descriptions. [Baseline evidence](DETERMINISTIC_PLANNER_V0_1_C06A_3_RETRY_3_BASELINE.json) records all observed outputs and a standalone reproduction program.

Required contract clarification, not performed here: establish whether each standalone predicate must authenticate all source payloads it relies upon, or is explicitly callable only after a separately defined mandatory source-admission step. Then reconcile its executable acceptance result, call preconditions, negative fixtures, and composition contract. This report chooses neither alternative and changes no oracle.

## Baseline and stopping boundary

The existing `replay.import_fixture()` dispatches PLANNER-REPLAY-1/2 and the budget qualification schema. It does not admit PF-INPUT-1. All 62 closure fixture candidates were submitted unchanged to that real structured-import boundary using temporary files; all reject `unknown or missing object fields`.

This demonstrates the source-profile import gap for its positive instances. A negative candidate's generic schema rejection is **not** qualification for its specified admission clause. No adapter or manual post-load state patch was invented to manufacture conformance. `import_e1()` remains dependent on the M normalization and retains opaque source records; it was inspected, not used to resume E1.

| Element | Baseline disposition |
|---|---|
| O01 | NONCONFORMANT_REPRODUCED at new source-profile import boundary; positive source definitions not imported |
| O02 | CONTRACT_EXCEPTION CE-01; runtime qualification stopped |
| O03 | NOT_EVALUATED against implementation after contract stop; bounded specification cases pass |
| O06 | CONTRACT_EXCEPTION CE-01; runtime qualification stopped |
| O08 | NOT_EVALUATED against implementation after contract stop; independent specification remains executable |
| O09 | NOT_EVALUATED against implementation after contract stop; both independent specification profiles remain executable |
| O10 | CONTRACT_EXCEPTION CE-01; runtime qualification stopped |
| O16 | NONCONFORMANT_REPRODUCED at new source-profile import boundary; implementation blocked by required CE-01 components |

The exception set collected by this audit is `[CE-01]`, with three affected standalone paths. No new exception was demonstrated for O01/O03/O08/O09. This is not a claim that unexecuted implementation qualification passed. Per the stop instruction, no implementation or implementation-regression tests were added or altered.

## Executed validation

- Existing 251 independent specification cases replayed: PASS.
- Closure 62 independent specification cases: PASS.
- Closure 11 additional mixed-source/invalidation sequences: PASS.
- Repeated closure suite under hash seeds 0, 17, 113: identical semantic digest `4066636d7965eb02642ca73a8cb1463ddcc9e2e83d1e89727ddac96a43d72001`.
- Persisted documentation runner also executed directly: same digest. Its key reversal, fixture reversal, positive projection checks and canonical reload checks pass.
- New CE-01 diagnostics: 12 reproduced contract violations after reload.
- Existing implementation importer boundary: 62 recorded schema rejections; no domain-specific conformance claimed.

A–N, X01–X11, C01–C06, budget runtime, CLI, constructor and full runtime determinism/regression suites were **not run** after the contract stop. No implementation change was made to qualify. F03 remains CLOSED under its unchanged prior accepted correction; it is not reopened or requalified by this attempt.

## Preservation and coverage

No assigned element transitions to RESTORED_AND_QUALIFIED. O13/O14 remain the two previously qualified elements; 15 remain. C06A-4 requires C06A-3 PASS and remains ineligible. C07 remains ineligible. No E1 receipt, action, authority, state transition or readiness execution occurred.

The task-entry hash inventory is compared against all existing adapter, backlog, plan and E1 files. All 10,911 E1 files must remain identical in both membership and bytes. The validation companion records the final comparison and whitespace check. New artifacts belong only to this RETRY_3 result; historical contracts/results are unchanged.

```text
WORK_PACKAGE = C06A-3
ATTEMPT = RETRY_3
RESULT = BLOCKED
ALREADY_CONFORMANT = []
NONCONFORMANT_REPRODUCED = [O01 source-profile import, O16 source-profile import]
CONTRACT_EXCEPTIONS = [CE-01: O02/O06/O10 standalone supporting-source admission]
O01 = FAIL (not qualified)
O02 = FAIL (contract exception)
O06 = FAIL (contract exception)
O08 = NOT_RUN (implementation qualification)
O09 = NOT_RUN (implementation qualification)
O10 = FAIL (contract exception)
O16 = FAIL (not qualified)
SPECIFICATION_CASES = 313 PASS
ADDITIONAL_SEQUENCES = 11 PASS
TESTS_PASSED = specification checks only; runtime qualification not completed
E1_REPLAY_CASES = NOT_RUN
NEGATIVE_INVARIANTS = NOT_RUN
C01_C06_REGRESSIONS = NOT_RUN
F03_STATUS = CLOSED (prior status preserved)
DETERMINISM_TESTS = specification suite PASS; runtime NOT_RUN
COLD_RESUME = NOT_RUN
PERSISTENCE_ROUND_TRIP = specification PASS; runtime NOT_RUN
CONTRACT_ELEMENTS_NEWLY_QUALIFIED = []
TOTAL_REQUIRED_CONTRACT_ELEMENTS = 17
RESTORED_AND_QUALIFIED = 2
REMAINING_COVERAGE = 15
C06A_3_RETRY_ALLOWED = NO pending CE-01 reconciliation
C06A_4_READY = NO
NEXT_PACKAGE = CE-01 contract reconciliation; no implementation package unlocked
C07_RETRY_ALLOWED = NO
V0_1_CURRENT_STATUS = CORRECTION_REQUIRED
REAL_E1_EVIDENCE_CREATED = NO
IMPLEMENTATION_MODIFIED = NO
E1_ARTIFACTS_MODIFIED = 0
DEFERRED_SCOPE_VIOLATIONS = 0
PRODUCTION_EFFECT = NO
```
