# C06A-3 retry 1 — independent contract verification

WORK_PACKAGE = C06A-3  
ATTEMPT = RETRY_1  
RESULT = BLOCKED  
EXCEPTION = C06A_3_CONTRACT_MISMATCH

O09's prior mismatch is addressed at specification level. A separate O08 root-proof admission gap prevents this retry from proceeding to implementation. No implementation, existing test, frozen E1, registry or historical result was changed.

## Scope and sources

The [remaining-contract matrix](DETERMINISTIC_PLANNER_V0_1_C06A_REMAINING_CONTRACT_1.json), C06A-3 entry, assigns O01/O02/O03/O06/O08/O09/O10/O16. Its acceptance requires source-bound predicates, independently restored root/slot proofs and explicit blocking of unsupported required semantics. Later authority integration is C06A-4; later receipt/control work is not authorized here.

Inputs checked include the [mapping registry](DETERMINISTIC_PLANNER_V0_1_C06A_2_MAPPING_1.json), [bounded result contracts](DETERMINISTIC_PLANNER_V0_1_C06A_2_ORACLES_1.json), [completion contract](DETERMINISTIC_PLANNER_V0_1_C06A_2_ORACLE_COMPLETION_1.json), completion fixtures, and the [O09 admission contract](DETERMINISTIC_PLANNER_V0_1_O09_BASELINE_SLOT_PROOF_ADMISSION_1.json) with its fixtures. The [original blocked attempt](DETERMINISTIC_PLANNER_V0_1_C06A_3_RESULT.md) is preserved.

## O09 revalidation

Both actual baseline SlotIds have named, pinned admission profiles. The invocation predicate preserves candidate-identity-only scope; the profile predicate preserves released-content identity rather than authority identity. Historically BLOCKED WP-01 need not become COMPLETED.

Executed independently of planner code:

- O09 positive fixtures: 2/2 ACCEPT.
- O09 negative fixtures: 52/52 REJECT with each expected failed clause.
- Completion specification cases: 104/104 match their expected output fields.

These specification results do not establish that the current importer implements them. Prior source-invalidation/reload/determinism qualification of the O09 specification remains recorded in its unchanged validation companion; this attempt does not report that as new planner test coverage.

## O08 mismatch: authority-conditioned baseline root proof

The completion registry entry at `/family_rules/root_slot/target_registry`, selected by `target = gate:validator_authority`, requires:

```text
special_case = ISSUED_BOUNDED_VALIDATOR_GRANT_PROOF
required_proof_class = ACCEPTED_COMPLETE_PROOF
required_final_action = DEC-VALIDATOR
ancestor_actions = [PREP-VALIDATOR]
all_ancestor_outputs_must_be_accepted = true
registered_rule = ALL_CURRENT_INDEPENDENT_OBLIGATIONS
```

The same contract's `/family_rules/decision_authority/issued_bindings` identifies DEC-VALIDATOR, APPROVED_OPTION_1, its pinned authority record, source/dossier records, exact scope/exclusions and IMPL-VALIDATOR reevaluation route. It explicitly sets `root_or_slot_shortcut = false`. These are sufficient documentary identities to name the obligation; they are not the instantiated independent root-proof acceptance profile.

The executable reference evaluates a root through `state.base.proof_contracts[target]`. Each such contract must identify `requirements` records with exact role/kind/claims, dependencies and an optional `authority_decision`. Its proof object must bind the exact target/contract/support set. The evaluator does not compile `ISSUED_BOUNDED_VALIDATOR_GRANT_PROOF` or `ALL_CURRENT_INDEPENDENT_OBLIGATIONS` from the registry.

The exhaustive supplied completion-fixture scan finds:

- The only executable ROOT target is `root:qualified`.
- **Zero** proof contracts in any of the 104 fixtures have a non-null `authority_decision`.
- No supplied positive/negative profile exercises the bridge from the bounded DEC-VALIDATOR grant plus accepted PREP-VALIDATOR output to the independent `gate:validator_authority` proof.
- O09 adds baseline slot predicates; it does not add this root predicate.

Generic SOURCE/MAPPING proof tests and standalone decision/authority tests do not test this composition. In particular they do not independently specify whether a recorded grant with a missing/stale preparation acceptance, wrong dossier/option/scope, or missing root-completion proof can establish this root. The broader rules require rejection of shortcuts, but no supplied executable baseline profile instantiates those conjuncts.

This is a missing **contract fixture/predicate composition**, not missing external E1 evidence. It is also not a demand to implement C06A-4 during C06A-3. The minimum bridge can describe admission of the already recorded limited grant as root proof while deferring future authority use to C06A-4. Its acceptance must be independently defined before implementation creates the bridge.

Marking the root UNSUPPORTED/UNKNOWN is a safe interim representation, but the C06A-3 contract explicitly says unsupported required semantics block completion. Treating the cached satisfied label, decision approval or final action status as proof would instead violate O08.

## Read-only implementation observations

A read-only call to the existing `replay.import_e1` loaded an isolated bundle. No planner action, E1 reentry/resume, or real-E1 readiness test was executed. Inspection of the initial bundle found:

- Both baseline slots have cached RESOLVED state and zero requirements.
- No root in that initial snapshot is marked SATISFIED.
- Zero graph assertions have operative relations.
- The source list still includes `adapter/tests/fixtures/planner_v0_1/M_P05.json`.

These observations locate intended implementation gaps but are **not** complete independent operational counterexamples or qualification. No regression was added before the contract stop, and no state was persisted back to E1.

## Element classification and coverage

| Element | Contract-check outcome in this retry | Implementation qualification |
|---|---|---|
| O01 action definition | Existing field mapping retained; no new mismatch established | Not completed after stop |
| O02 prerequisites/knowledge | Existing mapping and C06 contract retained | Not completed after stop |
| O03 bounded result contracts | Existing three bounded profiles retained | Not completed after stop |
| O06 history overlay | Existing overlay specification retained | Not completed after stop |
| O08 root proof | CONTRACT_MISMATCH: missing authority-conditioned baseline root admission profile | BLOCKED |
| O09 baseline slots | Both specific predicate/fixture sets pass independent specification | READY_FOR_IMPLEMENTATION; not restored |
| O10 graph/provenance | Existing mapping retained | Not completed after stop |
| O16 source-driven import | Existing inventory retained | Not completed after stop |

No incomplete runtime check is classified ALREADY_CONFORMANT or NONCONFORMANT_REPRODUCED. No element is promoted. Total 17, restored-and-qualified 2, remaining 15. Later-package elements are unchanged.

The O09 report's retry permission was explicitly based on no **additional recorded** prerequisite gap. This retry's broader inspection found the O08 gap above. The O09 predicates remain executable; their correctness is not revoked. Neither prior document is rewritten.

## Minimum retry prerequisite

Define one independent O08 profile for `gate:validator_authority`, binding the exact root proof type, grant identity/type, dossier/choice/scope/exclusions, and accepted PREP-VALIDATOR evidence under the frozen source rules. Specify the exact required support set and currentness/invalidation semantics. Include a positive proof and negative cases for missing completion proof, stale support, wrong grant/dossier/option/scope, and missing or unaccepted preparation output. Exercise this composition through the independent root-proof evaluator, without requiring implementation/test completion or treating grant acceptance as slot resolution.

After this prerequisite is accepted, retry C06A-3's contract gate and implementation tests. This task does not define that missing acceptance policy, implement the bridge, or execute later packages.

## Preservation and report

Per-file SHA-256 comparison against the pre-task inventory verifies all pre-existing inventoried implementation, tests, backlog, plans/results and all **10,911 E1 files unchanged**. Only this result and its [contract-check companion](DETERMINISTIC_PLANNER_V0_1_C06A_3_RETRY_1_CONTRACT_CHECK.json) are added. JSON/local links and `git diff --check` pass. No real E1 evidence or production effect occurred.

```text
WORK_PACKAGE = C06A-3
ATTEMPT = RETRY_1
RESULT = BLOCKED
CONTRACT_ELEMENTS_ASSIGNED = [O01, O02, O03, O06, O08, O09, O10, O16]
ALREADY_CONFORMANT = []
NONCONFORMANT_REPRODUCED = []
CONTRACT_MISMATCH = [O08_VALIDATOR_AUTHORITY_ROOT_PROOF_ORACLE_UNINSTANTIATED]
O09_BASELINE_SLOT_PROOFS = PASS (independent specification only)
POSITIVE_FIXTURES = O09 2/2 PASS
NEGATIVE_FIXTURES = O09 52/52 PASS
COMPLETION_SPECIFICATION_CASES = 104/104 PASS
CROSS_ORACLE_TESTS = INCOMPLETE_O08_AUTHORITY_ROOT_COMPOSITION
SOURCE_INVALIDATION_TESTS = NOT_RUN_AGAINST_PLANNER
FILES_ADDED = [DETERMINISTIC_PLANNER_V0_1_C06A_3_RETRY_1_RESULT.md,
               DETERMINISTIC_PLANNER_V0_1_C06A_3_RETRY_1_CONTRACT_CHECK.json]
FILES_MODIFIED = []
TESTS_PASSED = 158 specification cases; planner regressions NOT_RUN
E1_REPLAY_CASES = NOT_RUN
NEGATIVE_INVARIANTS = NOT_RUN
C01_C06_REGRESSIONS = NOT_RUN
F03_STATUS = CLOSED
DETERMINISM_TESTS = NOT_RUN
COLD_RESUME = NOT_RUN
PERSISTENCE_ROUND_TRIP = NOT_RUN_AGAINST_PLANNER
TOTAL_REQUIRED_CONTRACT_ELEMENTS = 17
RESTORED_AND_QUALIFIED = 2
REMAINING_COVERAGE = 15
C06A_4_READY = NO
NEXT_PACKAGE = C06A-3_RETRY_AFTER_O08_ROOT_PROOF_CONTRACT_COMPLETION
C07_RETRY_ALLOWED = NO
V0_1_CURRENT_STATUS = CORRECTION_REQUIRED
REAL_E1_EVIDENCE_CREATED = NO
E1_ARTIFACTS_MODIFIED = 0
IMPLEMENTATION_MODIFIED = NO
DEFERRED_SCOPE_VIOLATIONS = 0
PRODUCTION_EFFECT = NO
```
