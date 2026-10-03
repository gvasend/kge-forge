# C06A-3 RETRY_4 result

**RESULT = BLOCKED — new CONTRACT_EXCEPTION CE-02.** CE-01 remains reconciled. This attempt found an unresolved boundary between the assigned source-restoration scope and the fixed synthetic admission profiles. No implementation, registry, oracle, previous result, or E1 artifact was modified.

## Pinned contract set

[Contract manifest](DETERMINISTIC_PLANNER_V0_1_C06A_3_RETRY_4_CONTRACT_SET.json) records raw-file hashes of the authoritative contract, reconciliation, mapping, oracle, fixture, validation and prior-result inputs, including referenced source pins.

```text
CONTRACT_SET_IDENTITY = C06A3-ContractSet-sha256:b8680b082f25baa96fefbd832b9b37cfa120d9c702ad5a443d1e1fc4e06d0fa4
```

Its aggregate is SHA256 of the sorted compact UTF-8 JSON path/hash mapping. The CE-01 program is used as the refined reference; the original closure program is not substituted for it.

## CE-02: assigned source scope versus executable profile bridge

The [remaining-contract package](DETERMINISTIC_PLANNER_V0_1_C06A_REMAINING_CONTRACT_1.md), C06A-3 IMPLEMENTATION, requires replacing the M executable dependency in `replay.import_e1` with finite mapping to the existing model/codec. Its ACCEPTANCE requires a complete field inventory for the assigned rows. MAP-O01/O02/O06/O10/O16 specify the pinned frozen plan/graph sources, not just the two small synthetic instances.

The [closure](DETERMINISTIC_PLANNER_V0_1_C06A_3_PREFLIGHT_CLOSURE_1.md) explicitly says that its synthetic records do not replace the real plan, that the original per-record inventory governs actual frozen records, and that the small O16 witness does not claim restoration of the real inventory. Those limitations are correct. However, the executable profile and fixture set does not define the admission/normalization bridge from that inventory to the fixed source-shaped profiles.

Observed contract facts:

- The pinned source plan has **63 actions**.
- BASE permits exactly `S-BINDING`, `S-EXEC`, `QUAL-READ-KNOWLEDGE`; RENAMED permits the three ALT counterparts. Sixty-one actual source actions are absent from BASE; QUAL-READ-KNOWLEDGE is synthetic.
- Each trusted profile fixes its complete definition table, three history records, expected results, override, graph entities/assertions/predicates, source-role pins and coverage manifest.
- The source admission program requires exact equality with those tables and expected source bytes. These are independently trusted harness premises, not candidate-generated profiles.
- MAP-O01 and the inventory establish source pointers, tagged field copying and value hashes; they explicitly distinguish field mapping from operational oracle coverage. They do not instantiate the missing full source profile or define the bridge's expected operational outputs.

For example, actual S-ANCESTRY carries `scope=READINESS_PLAN`, an `actionability_scope` restriction, prose acceptance criteria, evidence records, BLOCKED/NOT_FOUND execution result, unresolved-prerequisite text and an external reentry gate. The synthetic action schema instead requires a profile-fixed `lineage`, structured `result_contract`, `knowledge_requirements`, `authority_requirements` and normalized `provenance`. Copying source fields is defined, but it is not itself authority to invent those normalized acceptance tables or their transition meanings for every assigned source record.

The assigned inventory contains the following field records (not an implementation coverage claim):

| Element | Inventory records |
|---|---:|
| O01 | 560 |
| O02 | 204 |
| O03 | 252 |
| O06 | 112 |
| O08 | 95 |
| O09 | 106 |
| O10 | 1,262 |
| O16 | 142 |

### Compatibility diagnostics and limits

The [baseline companion](DETERMINISTIC_PLANNER_V0_1_C06A_3_RETRY_4_BASELINE.json) records read-only compatibility probes for both fixed profiles:

| Source substituted into source-role input | Reference rejection |
|---|---|
| frozen plan, ACTION | ACTION_INVENTORY |
| frozen plan, HISTORY | HISTORY_ORDER_OR_SUBSTITUTION |
| frozen graph, GRAPH | GRAPH_SCHEMA |

These rejections are **correct for the pinned synthetic profiles**. They are not evidence that the oracle should accept arbitrary raw E1 input, nor a request to weaken its pin checks. They demonstrate that these profiles are not the raw-source bridge. A successful fixture-suite replay alone cannot establish that missing bridge or qualify all assigned rows.

CE-02 is therefore a **scope/normalization contract gap**, not the recurring CE-01 payload-check defect. A synthetic-only implementation could match these profiles while retaining the M dependency and failing the package acceptance criterion. Conversely, compiling all assigned frozen records by inventing a new trusted profile during this run would supply its own acceptance semantics, contrary to the instruction against contract design.

Affected boundary: O01/O02/O06/O10/O16 source restoration and complete assigned-field coverage. No new inconsistency is demonstrated in the O03 bounded result rules, O08 grant admission, O09 baseline proof predicates, or CE-01 source checks.

Required resolution, not performed here: either supply the independently pinned source-to-admission/operational binding contract and its source-shaped expected-output tests for the assigned inventory, or explicitly reconcile package scope so that a bounded synthetic slice is accepted separately from the later source bridge. This report chooses neither route, changes no contract, and does not move work between packages.

## Current implementation baseline

All **313 independent fixture submissions** were presented unchanged at the existing public structured-import boundary, `adapter.planner.replay.import_fixture`, using temporary files. All **1,000 CE-01 generated input states** were also presented there. Both valid composed cases reject alongside the negative cases with `unknown or missing object fields`.

The existing importer dispatch supports PLANNER-REPLAY-1/2 and the budget qualification schema. PF-INPUT-1 and the independent O08/O09 source-shaped admission formats are not implemented there. `import_e1` still calls `load_p05_fixture` through M normalization and retains original source records opaquely. It was inspected, not executed as a real E1 resume/readiness operation.

These are **schema-boundary baseline probes**, not 1,313 domain-admission tests passed. Negative schema rejection does not prove the specified negative clause; no normalization adapter was invented to hide that distinction. See the [composition baseline](DETERMINISTIC_PLANNER_V0_1_C06A_3_RETRY_4_COMPOSITION_BASELINE.json).

| Element | Current disposition |
|---|---|
| O01/O02/O06/O10/O16 | NEW_CONTRACT_EXCEPTION CE-02 for assigned-scope bridge; synthetic-source import is also nonconformant |
| O03 | NONCONFORMANT_REPRODUCED at raw source-result import boundary; existing native result behavior not thereby declared defective |
| O08 | NONCONFORMANT_REPRODUCED at raw proof-chain import boundary |
| O09 | NONCONFORMANT_REPRODUCED at raw baseline-proof import boundary |

`ALREADY_CONFORMANT = []` means no complete assigned source-restoration element was independently qualified by these probes. It does not deny previously accepted native typed planner behavior. Once CE-02 was identified, implementation stopped as required. No domain-specific regression was manufactured from an unrelated schema rejection.

## Specification checks versus implementation qualification

The unchanged independent programs were rerun:

- 251 existing specification cases: PASS.
- 62 reconciled closure cases: PASS; total **313**.
- 11 closure sequences: PASS.
- CE-01 bounded cross-product: **1,000 PASS**.
- Five CE-01 composition meta-invariants: PASS.
- Twelve CE-01 reproductions now rejected, 24 additional substitutions, and 12 invalidation/reload sequences: PASS.
- The 62-case/11-sequence semantic digest remains `4066636d7965eb02642ca73a8cb1463ddcc9e2e83d1e89727ddac96a43d72001`.

This does not satisfy the user's required **against-implementation** qualification gate. The source-shaped implementation path is absent, and neither implementation admission nor its operational persistence/actionability effects have been qualified. Ordered invalidation, cold restoration and global-control behavior cannot be claimed for a state that never entered the importer.

A–N, X01–X11, C01–C06, budget runtime, CLI, constructor and full runtime determinism/regression suites were not rerun after the contract stop. F03 remains CLOSED under its unchanged accepted result; this attempt neither reopens it nor claims a new runtime regression pass.

## Preservation, coverage and next gate

No element is newly qualified. All eight assigned rows remain BLOCKED for this attempt pending CE-02 resolution; existing qualified subparts remain preserved. O13/O14 remain the two previously qualified elements, leaving 15/17 remaining. C06A-4 requires C06A-3 PASS and is not eligible. C07 is not eligible.

All previous attempts and CE-01 history remain unchanged. The [validation record](DETERMINISTIC_PLANNER_V0_1_C06A_3_RETRY_4_VALIDATION.json) records comparison with task-entry hashes, all 10,911 frozen E1 files, pinned contracts, internal links and `git diff --check`. Only RETRY_4 result/evidence artifacts were added. No synthetic evidence was added to E1 and no E1 action was executed.

```text
WORK_PACKAGE = C06A-3
ATTEMPT = RETRY_4
RESULT = BLOCKED
ALREADY_CONFORMANT = []
NONCONFORMANT_REPRODUCED = [O01,O02,O03,O06,O08,O09,O10,O16: source-shaped import boundary]
NEW_CONTRACT_EXCEPTIONS = [CE-02: assigned-source scope / executable profile bridge]
O01 = BLOCKED
O02 = BLOCKED
O06 = BLOCKED
O08 = NOT_QUALIFIED
O09 = NOT_QUALIFIED
O10 = BLOCKED
O16 = BLOCKED
SPECIFICATION_CASES = 313 PASS as specification; implementation qualification NOT_PASS
SEQUENCES = 11 PASS as specification; implementation qualification NOT_RUN
CE01_COMBINATORIAL_CASES = 1000 PASS as specification; 1000 implementation schema rejections, NOT_PASS
META_INVARIANTS = 5 PASS as specification; implementation qualification NOT_RUN
TESTS_PASSED = specification only; no implementation qualification claimed
E1_REPLAY_CASES = NOT_RUN
NEGATIVE_INVARIANTS = NOT_RUN
C01_C06_REGRESSIONS = NOT_RUN
F03_STATUS = CLOSED (prior accepted status preserved)
DETERMINISM_TESTS = specification round-trip checks PASS; runtime NOT_RUN
COLD_RESUME = NOT_RUN
PERSISTENCE_ROUND_TRIP = specification PASS; runtime NOT_RUN
CONTRACT_ELEMENTS_NEWLY_QUALIFIED = []
TOTAL_REQUIRED_CONTRACT_ELEMENTS = 17
RESTORED_AND_QUALIFIED = 2
REMAINING_COVERAGE = 15
C06A_4_READY = NO
NEXT_PACKAGE = CE-02 scope/bridge reconciliation; no implementation package unlocked
C07_RETRY_ALLOWED = NO
V0_1_CURRENT_STATUS = CORRECTION_REQUIRED
REAL_E1_EVIDENCE_CREATED = NO
IMPLEMENTATION_MODIFIED = NO
E1_ARTIFACTS_MODIFIED = 0
DEFERRED_SCOPE_VIOLATIONS = 0
PRODUCTION_EFFECT = NO
```
