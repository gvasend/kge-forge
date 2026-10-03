# C06A-3 retry 2 — complete contract preflight

RESULT = BLOCKED. C06A_3_CONTRACT_PREFLIGHT = FAIL.

All eight assigned elements were examined before stopping. The complete mismatch set identified in the supplied contracts comprises **four groups affecting five elements**. No implementation baseline, implementation change or planner regression was undertaken after this preflight failed. O08 and O09 are not reopened: their specific admission predicates and fixtures pass.

The [machine-readable preflight](DETERMINISTIC_PLANNER_V0_1_C06A_3_RETRY_2_PREFLIGHT.json) contains the per-element inventory, every executed specification case, verified source pins, cross-contract checks, complete mismatch records and the 17-element coverage matrix.

## Authoritative scope

[Remaining-contract matrix](DETERMINISTIC_PLANNER_V0_1_C06A_REMAINING_CONTRACT_1.json), C06A-3, assigns O01/O02/O03/O06/O08/O09/O10/O16. It requires source-driven restoration without M_P05 executable state, source-bound independent predicates, complete assigned-field coverage and explicit blocking for unsupported required semantics. Its tests include an alternate supported source instance, historical overlay conflict, stale prerequisites, bounded non-budget results and two baseline slot proofs.

The inspected specification set comprises:

- [C06A-2 mappings](DETERMINISTIC_PLANNER_V0_1_C06A_2_MAPPING_1.json), including all 2,910 field inventory entries, mapping rules and source pins;
- [bounded result oracles](DETERMINISTIC_PLANNER_V0_1_C06A_2_ORACLES_1.json) and [fixtures](DETERMINISTIC_PLANNER_V0_1_C06A_2_FIXTURES_1.json);
- [completion rules/reference](DETERMINISTIC_PLANNER_V0_1_C06A_2_ORACLE_COMPLETION_1.json) and [fixtures](DETERMINISTIC_PLANNER_V0_1_C06A_2_ORACLE_COMPLETION_1_FIXTURES.json);
- [O08](DETERMINISTIC_PLANNER_V0_1_O08_VALIDATOR_AUTHORITY_GATE_ADMISSION_1.json) and its fixture/validation companions;
- [O09](DETERMINISTIC_PLANNER_V0_1_O09_BASELINE_SLOT_PROOF_ADMISSION_1.json) and its fixture/validation companions;
- the original C06/C06A results, the two prior C06A-3 attempts and the source contracts identified by the remaining-contract matrix.

A field inventory and prose preservation rule can define what must be retained without supplying an executable operational admission/normalization profile. A normalized proof fixture can test a gate after admission without testing how source-shaped records become that admitted state. This preflight checks both layers required by the package. It does not require a particular implementation class layout or a completed importer before implementation begins.

## Complete element inventory

| Element | Mapping / governing oracle | Positive and negative fixture coverage | Classification / target |
|---|---|---|---|
| O01 action envelope | MAP-O01, COPY_TAGGED_FIELDS, operation/stage separation and source boundary rules | Field inventory present; no source-shaped operation/stage profile or required alpha-renamed instance | CONTRACT_INCOMPLETE, PF-01; import_e1/Action/codec |
| O02 prerequisites and holds | MAP-O02; C06 source-bound knowledge; normalized knowledge/prerequisite rules | BLOCKED-PRODUCER-ACCEPTED-KNOWLEDGE and stale support examples present; source-specific hold/override reconciliation profile absent | CONTRACT_INCOMPLETE, PF-02; import_e1/Gate/Predicate/gates |
| O03 bounded results | MAP-O03; OR-BINDING, OR-CONTEXT, OR-PREP-VALIDATOR | 3 positives, 48 negatives, exact output/source/outcome and no root/slot transitions | EXECUTABLE_CONTRACT for the defined bounded profiles; Action result/inventory and apply_result |
| O06 historical attempts/current overlay | MAP-O06; OV01/OV02 | Native ledger and admitted-overlay checks exist; original plan-shaped attempt/result/summary/hold join not instantiated | CONTRACT_INCOMPLETE, PF-02; imported historical lineage/ActionStatus/KnowledgeRecord/codec |
| O08 root proof | MAP-O08; PR01–PR05; ADMIT_VALIDATOR_AUTHORITY_GATE_1 | Gate-specific 1 positive/41 negatives plus generic root proof cases; unknown future rules remain unsatisfied | EXECUTABLE_CONTRACT; RootCondition/Predicate/evaluate_satisfaction |
| O09 slots | MAP-O09; PR01–PR05; both exact O09 predicates | Baseline-specific 2 positives/52 negatives plus generic proof cases; remaining unavailable links remain explicit | EXECUTABLE_CONTRACT; ValueSlot proof admission/evaluate_satisfaction |
| O10 operational graph/provenance | MAP-O10; accepted ordering/epistemic rules | Field inventory present; no source assertion-admission/projection fixture with the required metadata and endpoint variants | CONTRACT_INCOMPLETE, PF-03; GraphEntity/GraphAssertion/project/invalidate_sources |
| O16 source coverage/import | MAP-O16; exact field inventory and no silent omission rule | No two source-shaped composition profiles with independently expected operational field dispositions | CONTRACT_INCOMPLETE, PF-04; import_e1/model/codec and coverage inventory |

Every row shares the existing source-pin, exact-selector, canonical identity and provenance requirements. Source invalidation must retain mandatory dependencies while withdrawing current support; reload must preserve invalidity. Those rules are defined. Missing source-normalization qualification in the rows above must not be mistaken for absence of the native invalidation mechanism or for a new failure of C06.

O08/O09 additionally have explicit predicate/profile/schema/target registry bindings, specified but not installed. Their admission is scoped to the pinned snapshot. No row permits action PASS, source knowledge or cached state labels to stand in for completion proof. Undefined future source/domain rules may stay UNKNOWN, but blanket UNKNOWN is not a substitute for implementing the supported assigned contracts.

## Complete mismatch set

### PF-01 — O01 source action-definition profile

MAP-O01 requires preserving `primary_operation_class`, `executor`, `effect_boundary`, `stage_role`, `scope` and `actionability_scope`, with stage separate from operation. The remaining-contract matrix specifically requires a source-defined bounded action and an alpha-renamed supported instance, plus unknown-stage/effect-expansion rejection.

The completion reference's exact action schema is:

```text
executor effect initial_state proofs knowledge completed_prerequisites
execution_scope route decision authority_decision
```

It has no operation or stage member. Result fixtures identify an action and its bounded output, not its source action definition. Therefore the supplied executable cases cannot detect loss or substitution of those required operation/stage fields during admission. The copy-field inventory remains useful, but does not close this fixture requirement.

Minimum completion: one independent source-shaped action-definition profile, its supported renamed instance and exact expected operative boundary preservation; rejection cases for omitted/unknown stage, effect expansion, missing scope and affected-reference substitution. This is finite qualification input definition, not authorization to redesign action semantics.

### PF-02 — O02/O06 source history, holds and overlay reconciliation

MAP-O02 names `prerequisite_actions`, `external_prerequisites`, `knowledge_requirements`, `unresolved_prerequisites`, `reentry_gate`, `blocked_by_batch_review` and `blocking_result`. MAP-O06 joins ordered `execution_history`, per-action `execution_result`, current `execution_state` and manifest result-artifact bindings. It forbids fabricated native history and conflicting summary/result admission.

The completion reference starts from already normalized `initial_state`, computes `expected_actions` from it, and checks an imported overlay using an admitted claim about `ledger_head`, `action_states`, `base_graph` and `policy`. Of 104 fixtures, 103 use NATIVE ledger kind; the sole IMPORTED case is `C03-IMPORTED-REENTRY`. It tests the admitted-overlay/reentry boundary, not normalization of original E1 attempt records and competing current holds. `REORDERED-LEDGER` tests native causal events, not that missing source-history join.

Minimum completion: a finite source-history-to-current-overlay acceptance table/profile, with a positive retaining an earlier attempt, accepted knowledge from a BLOCKED producer and a later admitted override. Include conflicting/reordered source history, spoofed current summary, removed mandatory hold and missing result-source negatives. Preserve original records and identify current precedence by accepted source lineage, not file order or a new synthetic native execution event. One shared profile legitimately covers O02 and O06.

### PF-03 — O10 source graph admission/projection

MAP-O10 requires preserving `relation`, `assertion_class`, `establishes_ordering`, `projection_layer` and source provenance. It separates accepted ordering from proposed/descriptive semantics and requires typed endpoint validation.

The completion reference accepts normalized proof/dependency records; its closed state schema has no source graph assertion collection through which those source metadata combinations are admitted. Generic transitive-proof negatives therefore do not test whether a descriptive/proposed source relation was wrongly compiled into an ordering prerequisite. Native graph tests can protect native behavior but cannot independently supply this missing source-import qualification case.

Minimum completion: a source-shaped graph profile with an operative ordering relation and a descriptive/proposed non-ordering relation, exact expected typed endpoint/admission/projection dispositions, and negatives for correspondence promoted to ordering, wrong-domain/dangling endpoints and stale required support.

### PF-04 — O16 composed source-instance coverage

The required positive is **two supported source-shaped instances**, not a count match or M_P05 state. The 2,910-entry inventory identifies source values/mapping families; it is not that pair of operational import fixtures. Current executable families consume normalized synthetic records, bounded result submissions, or isolated O08/O09 pinned proofs. None is the full assigned source-shaped composition with an independently expected field-to-operational-disposition manifest.

Minimum completion: compose PF-01–PF-03 with existing bounded results, O08/O09 and explicit UNKNOWN rules. Supply two supported source instances, per-field enforcement/provenance-only/unknown-with-hold expectations and negatives for missing required fields, schema drift, same-count substitution and incompatible cross-family bindings. Preserve the C06A-3 scope boundary; do not require C06A-4 authority-use integration, C06A-5 receipts or C06A-6 final controls in this profile.

PF-04 is the composition/coverage boundary, not a demand to duplicate the standalone admission predicates. Its dependent gaps are grouped here so they can be completed together rather than discovered in successive retries.

## Cross-contract preflight

No demonstrated contradictory identity/type/relationship was found: C06A_3_CONTRACT_CONFLICT_SET = []. That is not a claim of complete composition qualification.

| Shared dimension | Result |
|---|---|
| Graph identity | O08 context graph pin equals both O09 snapshot pins |
| Plan and selection policy | O08 pins explicit plan/policy context; prior mapping source pins verify. O09 pins graph and source semantics; do not invent a policy field within its value proof |
| Runtime and G4/controller-store | Both O09 baseline envelope tuples agree. Generic completion fixtures use explicitly synthetic identities; they are not interchangeable with actual pinned documentary identities |
| ProgrammerProfile | O09 profile content must not substitute for ProgrammerProfile. O08 grant declares no profile applicability member; no extra factual requirement invented |
| Invocation/binding | O09 invocation is candidate identity only. Neither O08 nor O09 manufactures canonical binding. Synthetic context/binding IDs remain qualification-only |
| Authority/source lineage | O08 authenticates exact dossier/preparation/grant source chain. O09 preserves its own limited source lineage; differing lineage roles are not automatically equated |
| Proof sources | Exact source roles/pins remain independent; recorded invalidation withdraws support. All mapping source pins checked against current frozen bytes |
| Execution ledger/overlay | Normalized overlay rules and tests exist; source-to-overlay normalization remains PF-02 |
| Cross-family operational composition | No implicit joining of synthetic completion contexts to frozen-profile contexts. Supported composed instance profiles and rejection expectations remain PF-04 |

The different O08 permission scope and O09 value-resolution scopes are intentional distinct semantic domains, not a conflict requiring string equality. This preflight does not create missing runtime applicability facts or demand unrelated authority decisions.

## Executed checks and implementation stop

All supplied executable specification families were evaluated independently of planner code:

| Family | Cases passing |
|---|---:|
| Bounded result expressions, including every nested negative mutation | 51 |
| Completion reference | 104 |
| O08 gate admission | 42 |
| O09 baseline slot admission | 54 |
| Total | **251** |

The declared `all`, `keys_exact` and typed canonical `eq` semantics were used for the bounded result expressions. Embedded independent reference specifications evaluated the remaining cases. Unknown expression operations fail closed. Source pins and common O08/O09 graph/envelope bindings were checked separately.

These passes establish the supplied profiles behave as specified; they do not cover source-import inputs absent from those profiles. No tests against the current planner were run, because Step 2 requires stopping before Step 4 when the complete mismatch set is non-empty. No ALREADY_CONFORMANT or NONCONFORMANT_REPRODUCED implementation classifications are assigned. No failing runtime regression was fabricated.

A–N, X01–X11, C01–C06, budget/importer/CLI/native persistence/cold-resume/control/constructor regressions and implementation determinism are NOT_RUN in this attempt. F03 retains its accepted CLOSED status; that is preservation of the prior result, not new regression qualification.

## Coverage and next gate

Mechanically recorded in the companion:

- RESTORED_AND_QUALIFIED: O13, O14 — **2**.
- BLOCKED by this contract preflight: O01, O02, O06, O10, O16 — **5**.
- READY_FOR_IMPLEMENTATION at contract level: O03, O04, O05, O07, O08, O09, O11, O12, O15, O17 — **10**. This label does not waive package dependencies or authorize later-package execution.
- Total **17**; remaining restoration coverage **15**; no element promoted.

C06A_4_READY = NO, because C06A-3 has not passed. C07_RETRY_ALLOWED = NO. The next operation is one bounded contract/fixture completion batch for PF-01 through PF-04, followed by a new complete C06A-3 preflight. No additional external evidence acquisition, authority issuance or domain resolution is required for that specification work.

## Preservation and report

The pre-task per-file SHA-256 inventory covers implementation/tests, backlog, plans/results and frozen E1. Every pre-existing inventoried file and all **10,911** E1 files remain byte-identical. Both prior C06A-3 attempts and all admission registries/contracts remain unchanged. Only this result and the preflight JSON are added. JSON/local links and `git diff --check` pass.

```text
WORK_PACKAGE = C06A-3
ATTEMPT = RETRY_2
RESULT = BLOCKED
CONTRACT_ELEMENTS_ASSIGNED = [O01, O02, O03, O06, O08, O09, O10, O16]
C06A_3_CONTRACT_PREFLIGHT = FAIL
C06A_3_CONTRACT_MISMATCH_SET = [PF-01(O01), PF-02(O02/O06), PF-03(O10), PF-04(O16)]
C06A_3_CONTRACT_CONFLICT_SET = []
ALREADY_CONFORMANT = []
NONCONFORMANT_REPRODUCED = []
O08 = PASS (standalone specification)
O09 = PASS (standalone specification)
FILES_ADDED = [DETERMINISTIC_PLANNER_V0_1_C06A_3_RETRY_2_RESULT.md,
               DETERMINISTIC_PLANNER_V0_1_C06A_3_RETRY_2_PREFLIGHT.json]
FILES_MODIFIED = []
TESTS_PASSED = 251 independent specification cases
E1_REPLAY_CASES = NOT_RUN_CONTRACT_STOP
NEGATIVE_INVARIANTS = NOT_RUN_CONTRACT_STOP
C01_C06_REGRESSIONS = NOT_RUN_CONTRACT_STOP
F03_STATUS = CLOSED
DETERMINISM_TESTS = NOT_RUN_AGAINST_PLANNER
COLD_RESUME = NOT_RUN
PERSISTENCE_ROUND_TRIP = NOT_RUN_AGAINST_PLANNER
TOTAL_REQUIRED_CONTRACT_ELEMENTS = 17
RESTORED_AND_QUALIFIED = 2
REMAINING_COVERAGE = 15
C06A_4_READY = NO
NEXT_PACKAGE = COMPLETE_PF-01_THROUGH_PF-04_CONTRACT_BATCH_THEN_RETRY_C06A-3
C07_RETRY_ALLOWED = NO
V0_1_CURRENT_STATUS = CORRECTION_REQUIRED
REAL_E1_EVIDENCE_CREATED = NO
E1_ARTIFACTS_MODIFIED = 0
IMPLEMENTATION_MODIFIED = NO
DEFERRED_SCOPE_VIOLATIONS = 0
PRODUCTION_EFFECT = NO
```
