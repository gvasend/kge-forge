# Deterministic Planner v0.1 — C01 result

WORK_PACKAGE = C01
RESULT = PASS
V0_1_CURRENT_STATUS = CORRECTION_REQUIRED

C01 implements only the predicate/reference admission correction for **F04**, root-cause group **RC-REFERENCE-INTEGRITY**, from [Correction Plan 1](DETERMINISTIC_PLANNER_V0_1_CORRECTION_PLAN_1.md) and [Correction Matrix 1](DETERMINISTIC_PLANNER_V0_1_CORRECTION_MATRIX_1.md). The implementation and prerequisites matched the plan. C02–C07 remain unimplemented. The original qualification and adversarial review remain historical, unchanged artifacts.

## Reproduction and regression

Before implementation, `Predicate(PredicateId('x'), SOURCE_IDENTITY, entity=EntityId('absent'))` in an otherwise empty Snapshot survived `decode_snapshot(snapshot_bytes(state))`. No entity with that ID existed. This reproduced the exact F04 counterexample.

The new `C01ReferenceContractTests.test_adversarial_dangling_entity_rejected_at_decode` constructs hostile typed JSON directly, so a rejecting serializer cannot mask a permissive decoder. Before the repair it failed with `AssertionError: PlannerError not raised`. After the repair the decoder raises `PlannerError` at the shared reference-contract admission boundary. The same malformed state cannot be serialized or used by the planner.

```text
PRE_REPAIR_COUNTEREXAMPLE = REPRODUCED
PRE_REPAIR_REGRESSION = FAIL_EXPECTED
POST_REPAIR_COUNTEREXAMPLE = REJECTED_CORRECTLY
POST_REPAIR_REGRESSION = PASS
```

## Correction

`model.validate_predicate_contracts` defines required, optional and forbidden fields for every PredicateKind. It validates references against their typed entity/action/root/knowledge/evidence collections, enforces operation-specific entity domains and the AUTHORITY_IDENTITY domain, rejects duplicate output owners or conflicting output bindings, and rejects cyclic proof definitions at admission. Cycles include predicate operands, root-proof dependencies and receipt authentication dependencies. Slot value references are also checked.

A future KnowledgeId must be present in an existing action's bounded `accepted_inventory`; that declaration supplies neither produced knowledge nor proof. An accepted record is still independently required. Predicate `unavailable` is an explicit nonempty reason with **no operative bindings**; it evaluates UNKNOWN, including after persistence/reload. This distinguishes intentional missing facts from misspelled or absent target IDs. Binding a previously unavailable predicate requires a new, structurally valid record.

`gates.evaluate_predicate` admits the typed snapshot before direct evaluation; recursive evaluation operates on admitted state. Historical stale, unproduced or unvalidated entity records remain representable but cannot prove current facts. A typed identity mismatch remains a disproved comparison, not hash-based coercion. This package does not repair C02's separate stale ordering-edge enforcement defect.

The existing codec, structured importer, native restore, recomputation and transition entry points use the shared validation path. The existing core import now uses the admitted predicate evaluator after its existing `validate_model/project` boundary; the public predicate, decision-readiness and receipt/proof queries validate before use. This minimal call-site integration avoids repeating full-snapshot admission for every predicate, without caching or changing scheduling/propagation logic. No parallel planner state or validation policy was introduced.

## Fixture migration

A/B replay schemas and F/M fixture schemas advance from version 1 to version 2 where explicit missing bindings are needed. Their paths remain stable; N's normalization pin follows the changed M fixture identity. No frozen E1 source or pin to an E1 artifact changed.

- A: the unbound `consumer-contract` claim becomes explicitly unavailable until the existing independently pinned pure consumer check supplies an actual result. Only a successful check can bind accepted success knowledge; rejection cannot.
- B: missing source, producer and mapping remain three explicit unavailable predicates.
- F: 27 undeclared decision-input facts remain unavailable; authority-required does not make them complete.
- M: 27 placeholder root-proof references become explicit unavailable facts, without inventing a producer or resolving a root.
- Existing correctly declared future-output references remain unchanged and UNKNOWN until accepted output is present.

Older well-formed snapshots retain canonical bytes because the additive field omits its default. Older malformed snapshots are rejected; the runtime does not silently migrate them or infer missing bindings. Fixture version 2 encodes the reviewed migration explicitly. This does not implement C06's missing full operational E1 contract restoration.

## Validation

Eight new tests cover the exact decoder counterexample, target/field/domain variants, duplicates and conflicting declarations, unknown predicate kinds/IDs, direct planner/gate admission, cyclic definitions, declared future output versus produced knowledge, explicit unavailability, stale and invalid targets, structured import, correctly hashed hostile native bundles, key/collection permutations, deterministic diagnostics for competing invalid references, repeated serialization/reload, and five fresh-process hash seeds (`0`, `1`, `7`, `42`, `999`). Existing invariant tests that previously represented absence with malformed references now use explicit unavailability or an existing unproduced entity; their missing-fact/mandatory-proof assertions remain intact. Cycles now require rejection rather than UNKNOWN. Existing structural negatives in `test_planner_e1_replay.py` also need this representation migration: deleted semantic facts and removed output producers first require rejection as dangling references, then become explicit unavailable facts for the intended blocked-route checks. Missing decision checks use explicit unavailability instead of an UNSUPPORTED kind retaining forbidden fields. Removing the admitted validator-grant fact still raises the unresolved-root count to 28 after its predicate is explicitly made unavailable. The receipt trust negative requires an admission error for a wrong authority identity domain; self-authentication and consumed-authority checks still require a non-proving result. These retain the existing independent readiness/count/trust assertions; they add no P04/P05 functionality.

The declared future-output positive control applies a real bounded action result pinned to its pre-state before proving its knowledge predicate. Root/slot satisfaction continues to require its independent predicates. The native-restore negative supplies matching content hashes deliberately, proving that content identity does not bypass structural validation.

Affected regression command:

```sh
python3 -m unittest adapter.tests.test_planner_core adapter.tests.test_planner_invariants adapter.tests.test_planner_resume adapter.tests.test_planner_e1_replay adapter.tests.test_invocation_constructor -v
```

The final full run completed with **115 tests passing in 367.558 seconds**, with no skips or failures (20 core, 30 invariant, 18 persistence/resume, 42 E1 replay, 5 constructor tests). Replay N remains the existing isolated regression subset and is not a claim that F03 or real E1 operational cold-resume readiness is repaired. Likewise, passing existing tests does not close other adversarial findings or requalify v0.1.

## Preservation and scope

The pre-edit path/raw-SHA256 inventory covers all 10,911 E1 files. Verification compares the complete path set and every file hash, rather than relying on Git's treatment of previously untracked files. [Current status 1](DETERMINISTIC_PLANNER_V0_1_CURRENT_STATUS_1.json) binds the pre-correction implementation inventory, historical qualification/review/plan identities and frozen inventory commitment. Its companion [status note](DETERMINISTIC_PLANNER_V0_1_CURRENT_STATUS_1.md) preserves CORRECTION_REQUIRED.

Existing planner/test/plan files were already untracked on entry. They have not been staged or committed. Per-file pre/post inventories distinguish this package's edits from that pre-existing work. Backlog, correction plan/matrix, original qualification and frozen E1 must remain unchanged. No authority, E1 execution, external evidence acquisition, production effects or deferred capability is introduced.

## Files and remaining work

FILES_ADDED:

- `docs/plans/DETERMINISTIC_PLANNER_V0_1_CURRENT_STATUS_1.md`
- `docs/plans/DETERMINISTIC_PLANNER_V0_1_CURRENT_STATUS_1.json`
- `docs/plans/DETERMINISTIC_PLANNER_V0_1_C01_RESULT.md`

FILES_MODIFIED:

- `adapter/planner/model.py`
- `adapter/planner/core.py`
- `adapter/planner/gates.py`
- `adapter/planner/codec.py`
- `adapter/planner/replay.py`
- `adapter/tests/test_planner_invariants.py`
- `adapter/tests/test_planner_resume.py`
- `adapter/tests/test_planner_e1_replay.py`
- `adapter/tests/fixtures/planner_v0_1/A_P06.json`
- `adapter/tests/fixtures/planner_v0_1/B_P06.json`
- `adapter/tests/fixtures/planner_v0_1/F_P04.json`
- `adapter/tests/fixtures/planner_v0_1/M_P05.json`
- `adapter/tests/fixtures/planner_v0_1/N_P06.json`

The validation below passes: C01 closes F04 at the package acceptance boundary. C02 becomes newly eligible; C04 and C05 were already independently eligible. The plan's lexical correction-package ordering chooses C02 next. It is not executed here. Remaining findings are F01, F02, F03, F05 and F06; observations are unchanged. C07 must independently review closure and requalification evidence before QUALIFIED can be restored.

## Accepted result and preservation evidence

```text
WORK_PACKAGE = C01
RESULT = PASS
FINDINGS_ADDRESSED = [F04]
PRE_REPAIR_COUNTEREXAMPLE = REPRODUCED
PRE_REPAIR_REGRESSION = FAIL_EXPECTED
POST_REPAIR_COUNTEREXAMPLE = REJECTED_CORRECTLY
POST_REPAIR_REGRESSION = PASS
TESTS_PASSED = 115
AFFECTED_REPLAY_CASES = {A: PASS, B: PASS, C: PASS, D: PASS, E: PASS, F: PASS, G: PASS, H: PASS, I: PASS, J: PASS, K: PASS, L: PASS, M: PASS, N: PASS}
AFFECTED_INVARIANTS = {X01: PASS, X02: PASS, X03: PASS, X04: PASS, X05: PASS, X06: PASS, X07: PASS, X08: PASS, X09: PASS, X10: PASS, X11: PASS}
DETERMINISM_TESTS = PASS (C01 scope; fresh-process hash seeds, input/key permutations, repeated canonical reload and deterministic invalid-reference diagnostics)
FINDINGS_CLOSED = [F04]
FINDINGS_REMAINING = [F01, F02, F03, F05, F06]
NEWLY_ELIGIBLE = [C02]
NEXT_CORRECTION_PACKAGE = C02
V0_1_CURRENT_STATUS = CORRECTION_REQUIRED
E1_FILES_VERIFIED = 10911
E1_ARTIFACTS_MODIFIED = 0
BACKLOG_CHANGED = NO
CORRECTION_PLAN_OR_MATRIX_CHANGED = NO
ORIGINAL_QUALIFICATION_CHANGED = NO
UNRELATED_SOURCE_CHANGES = 0
GIT_DIFF_CHECK = PASS
UNTRACKED_FILE_WHITESPACE_CHECK = PASS
DOCUMENT_LINKS_AND_JSON = PASS
DEFERRED_SCOPE_VIOLATIONS = 0
PRODUCTION_EFFECT = NO
```

C01 specifically assigns B/C/F/H/J/N and X02/X05/X06/X08/X10/X11; the broader existing suite was also run as regression protection. Existing X10 and N passes do not close F01/F02/F03. Existing determinism passes do not close F05. No later correction package or independent requalification review was executed.

The frozen path/raw-SHA256 inventory commitment is `1cf25145f69a2fb133c12f3b15cd1089351e4a9cac8624d4b6e970f2b4b3a044`, identical before and after correction. Both inventories contain exactly 10,911 files. The rule is SHA-256 over UTF-8 JSON of the complete path-to-raw-SHA256 mapping with sorted keys, compact comma/colon separators and `ensure_ascii=True`. The changed/added file set equals the file lists above; generated Python bytecode caches are excluded from the source-change comparison, but no E1 file is excluded from preservation checks.

Final code, fixture, test and status-record raw identities (the result record itself is excluded to avoid a self-reference):

| Artifact | Raw SHA-256 |
|---|---|
| `adapter/planner/codec.py` | `c820af07acc18f3d19cce3421a2e2b33dc4a5aa628239f37928eb6e8f5319323` |
| `adapter/planner/core.py` | `d2e65c3ba92ea626d4be92bf4381b65e4c32f47a5c8906056c30d0179a4cb8bd` |
| `adapter/planner/gates.py` | `9eb082fffddd79af064eda7b7548de9c9d22c7fd30517e5ac41a6c108a393a28` |
| `adapter/planner/model.py` | `42baa0913b106ea00fe0676ebe0a7b74d901d9b9a580ac060a49e013ec1c39c5` |
| `adapter/planner/replay.py` | `c54ed125e613a0e63a84b01c86b07ae7b024a72043cffb225a09eddea74a6a21` |
| `adapter/tests/fixtures/planner_v0_1/A_P06.json` | `f53da157f14d471e8605d8256eef7cbc04e914da64e43800ab14fdb48de0b6f8` |
| `adapter/tests/fixtures/planner_v0_1/B_P06.json` | `08f81655399896de3a760deb6583ca81af380f75c58ff4134aa659c22ec8ce57` |
| `adapter/tests/fixtures/planner_v0_1/F_P04.json` | `89bfc56448ba9ece4fbe793955d91bd2c058d5849c80a9f29167cf3f6ba4f033` |
| `adapter/tests/fixtures/planner_v0_1/M_P05.json` | `79252daf79857becea4637bb4f0495ce7133c95dd52e890d8e9e49f92afe35f6` |
| `adapter/tests/fixtures/planner_v0_1/N_P06.json` | `4f134504c0c53dee2bf561f13aee09af045727fa9bd6ee456cce151652594621` |
| `adapter/tests/test_planner_e1_replay.py` | `41a225a8d9cde358fd00bce39b260f62b32af98b66b4f2cc6d81acafb39118fb` |
| `adapter/tests/test_planner_invariants.py` | `a9d16600bb41c350e0e838474f18aeb89d84fd5ec1b08f49933a39a70fbd88d3` |
| `adapter/tests/test_planner_resume.py` | `f87a97a50e7e33b32990d5bbaf1804f3bdddacfe8d14e9d439d3b4afbc86fa6b` |
| `docs/plans/DETERMINISTIC_PLANNER_V0_1_CURRENT_STATUS_1.json` | `6ed78af6fa35551dc0f19a727ecd2c1f2bbbc2ecae725d9993904ee863dc23ec` |
| `docs/plans/DETERMINISTIC_PLANNER_V0_1_CURRENT_STATUS_1.md` | `7551a20c1b3f1cfcfcf1732882446b83c5cbe1e15eb7777af7af82d296a49df5` |

Final full-run log raw SHA-256: `646fde3e15996f937fd9d1c27d3ccc9203aa45a0135b2fd00435d8a5e36d26b2`. The reproduction command and final test command above make this evidence repeatable; the log is an execution-session artifact, not a modification to historical qualification.
