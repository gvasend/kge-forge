# C06A-3 preflight mismatch closure 1

Result: **PASS — specification closure only**. PF-01 through PF-04 are closed for contract preflight. All eight assigned elements have executable independent contracts. C06A-3 may be retried; it has not been executed. Restored-and-qualified coverage remains **2/17**.

## Governing inputs and boundaries

This is an additive specification following the [RETRY_2 blocked result](DETERMINISTIC_PLANNER_V0_1_C06A_3_RETRY_2_RESULT.md) and its [complete preflight](DETERMINISTIC_PLANNER_V0_1_C06A_3_RETRY_2_PREFLIGHT.json). It preserves that history. Package assignment remains the [remaining-contract matrix](DETERMINISTIC_PLANNER_V0_1_C06A_REMAINING_CONTRACT_1.json): O01, O02, O03, O06, O08, O09, O10, O16.

The [mapping inventory](DETERMINISTIC_PLANNER_V0_1_C06A_2_MAPPING_1.json), [bounded-result oracles](DETERMINISTIC_PLANNER_V0_1_C06A_2_ORACLES_1.json), [oracle completion](DETERMINISTIC_PLANNER_V0_1_C06A_2_ORACLE_COMPLETION_1.md), [O08 admission](DETERMINISTIC_PLANNER_V0_1_O08_VALIDATOR_AUTHORITY_GATE_ADMISSION_1.md), and [O09 admission](DETERMINISTIC_PLANNER_V0_1_O09_BASELINE_SLOT_PROOF_ADMISSION_1.md) remain governing. This document adds the missing source-level qualification profiles; it does not replace their predicates or mappings.

The [backlog](../backlog/DETERMINISTIC_REASONING_PLANNING_RUNTIME.md) and [traceability](../backlog/DETERMINISTIC_REASONING_PLANNING_RUNTIME_E1_TRACEABILITY.md) require separate action/knowledge/proof states, accepted artifact provenance, deterministic projection, and governed invalidation. Frozen source semantics are in the [resolution plan](../experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_PLAN_1.json) and the graph sources pinned by the mapping inventory. Source ordering flags and semantic correspondence are not equivalent to admitted operational prerequisite edges. Historically BLOCKED producers can supply independently accepted current knowledge.

No planner modules, tests, operational registries, historical results, or E1 files are edited. The supplied Python expressions are executable **specifications embedded in documentation**, not a runtime importer or a new planner implementation. No production authority or actual external evidence is supplied.

## Deliverables and execution

- [Contract and reference predicates](DETERMINISTIC_PLANNER_V0_1_C06A_3_PREFLIGHT_CLOSURE_1.json): closed schemas, two independently pinned profiles, source dependency table, exact admission bindings, reference program, governing-artifact pins, eventual registry bindings.
- [Fixtures](DETERMINISTIC_PLANNER_V0_1_C06A_3_PREFLIGHT_CLOSURE_1_FIXTURES.json): two complete source instances, 62 cases, explicit expected clauses and positive projections. Mutations are relative to the indicated base; omission and substitution are distinct operations.
- [Validation](DETERMINISTIC_PLANNER_V0_1_C06A_3_PREFLIGHT_CLOSURE_1_VALIDATION.json): case results, deterministic output digest, specification runner and preservation results.
- [Updated complete preflight](DETERMINISTIC_PLANNER_V0_1_C06A_3_PREFLIGHT_CLOSURE_1_PREFLIGHT.json): all eight assignments and finite retry prerequisites.

To replay the new cases, execute the validation companion's `specification_runner` from the repository root in an isolated qualification process. It reads these documentation companions only. The harness fixes the reference-program pins before supplying candidate objects. It does not import `adapter.planner`, inspect its outputs, or run E1. Run in separate processes with `PYTHONHASHSEED=0`, `17`, and `113`. Existing specification cases use their original independent programs and fixtures unchanged.

## Shared input and trust contract

The typed qualification input is `PF-INPUT-1`, mode `SYNTHETIC_QUALIFICATION_ONLY`. Its exact members are `schema`, `mode`, `profile_pin`, `context`, `sources`, `coverage`, and `admissions`. Unexpected members reject. The independently admitted profile is `PF-ADMITTED-PROFILE-1`. It is a harness premise, never a candidate-controlled allowlist. A candidate may not change both its source and the expected pin to make itself admissible.

The five required source roles are `plan`, `results`, `graph`, `evidence`, and `override`. Their schemas are respectively `PF-SOURCE-PLAN-1`, `PF-RESULTS-1`, `PF-SOURCE-GRAPH-1`, `PF-EVIDENCE-1`, and `PF-OVERRIDE-1`. Synthetic pins hash canonical UTF-8 JSON: sorted object keys, compact separators, no floating-point/NaN values, no conversion of identity domains. These semantic JSON pins are distinct from the raw-file SHA256 pins of frozen artifacts. Arrays retain their meaning and order; changing source array order changes its pin and requires independent admission. Projection order is separately canonical.

Identity domains remain explicit: action references are `ActionId`, graph action entities are `INSTANCE_IDENTITY`, source pins are content identities, and O08/O09 retain their existing authority/content/instance domains. Hash equality cannot change a domain. Profile, invocation candidate, release-content digest, and authority identity are never interchangeable.

A separate accepted validity view binds the same context and exact source-role identities to CURRENT, STALE, or REVOKED. Neither stored proof booleans nor source existence establish currentness. `results -> evidence` and `graph -> evidence` are explicit dependency bindings in these profiles. Recursive validity checks detect cycles and require all supports current. Runtime evidence admission remains governed by existing receipt semantics; the synthetic validity view does not acquire facts or issue authority.

Context binds base graph, base plan, execution ledger, selection-policy identity/version, instance, scope, runtime and controller store, and typed correspondence. The two qualification instances have distinct instance/ledger/source identities. Actual known invocation candidate and released-profile content identities use the O09 contract. ProgrammerProfile, dispatch, OperationalContext and release authority remain `PROVENANCE_ONLY_NOT_PROVED`; OperationalBinding and WorkAuthorization lineage remain `MISSING`. These explicit absence markers cannot satisfy requirements for those objects. This bounded admission test does not manufacture the missing E1 objects.

## PF-01 / O01 — action definition admission

`ADMIT_ACTION_DEFINITION_1(profile, state, validity)` is `evaluate(..., 'ACTION')`. ACCEPT requires the exact independently reviewed action inventory and each closed action definition:

| Input | Admission rule |
|---|---|
| `id` | Known unique ActionId in the profile, exact source selector |
| `primary_operation_class`, `stage_role` | Exact separately typed values; a stage is not an operation class |
| `executor`, `effect_boundary` | Exact bounded non-effecting execution contract |
| `prerequisite_actions` | Typed ActionId references, targets present, exact required set |
| `external_prerequisites`, `authority_requirements` | Explicit exact requirements; absent authority cannot become permission |
| `knowledge_requirements` | Exact knowledge identities and required result types |
| `result_contract` | Allowed outcomes/types and independent root/slot transitions |
| `scope`, `lineage` | Exact target envelope and qualification lineage |
| `provenance` | Accepted source role, exact record selector and context |
| source/schema | Expected source pin and schema, current source, no extra fields |

The source-shaped fixtures carry `resolution_actions`, not already constructed planner Actions. BASE includes S-BINDING, S-EXEC and explicitly synthetic QUAL-READ-KNOWLEDGE; RENAMED repeats the contract with different IDs. These are qualification instances exercising the frozen source distinctions, not claims that synthetic prerequisites replace the real plan. The original per-record MAP-O01 inventory remains the specification for actual frozen records. Converting source strings to typed references requires resolution in that inventory; an unknown value must not become a new action or enum.

Positive fixtures admit all required definition members. Negative clauses cover unknown action, wrong operation/stage/effect, dangling or wrong-domain prerequisite, wrong result/authority contract, provenance omission, scope/lineage mismatch, stale source, schema substitution and incompatible instance. Exact composition and source pin checks reject individually plausible fields assembled from different definitions. ACCEPT admits a definition only; it does not select it, grant permissions, or satisfy its prerequisites.

Eventual registry entry: predicate `ADMIT_ACTION_DEFINITION_1`, schema/profile version above, MAP-O01, reviewed ActionId/operation/result/reference domains and source-role bindings. This registry entry is specified, not installed.

## PF-02 / O02,O06 — history and hold reconciliation

`RECONCILE_HISTORY_HOLDS_1` is `evaluate(..., 'HISTORY')`. It accepts imported `execution_history`, accepted result records, independently pinned overrides, and current source validity; it computes the current summary and rejects a disagreeing persisted summary. It does not merely round-trip native events or trust `execution_state`.

Each history record has unique identity, contiguous sequence, ActionId, result identity, exact envelope and ledger. Results must belong to that action and match their accepted source record. Knowledge retains identity/type/source/producer/result outcome. Holds retain identity, target action and reason. A hold may be removed only through the explicitly admitted override binding its hold, action, source and basis result. Last-file order is not an override.

The positive history retains an earlier BLOCKED result for S-BINDING, a later PASS and separately admitted H1 release; S-EXEC remains BLOCKED under H2 while its K-BLOCKED knowledge is independently current. The synthetic consumer requires current K-BLOCKED and the current completed-action prerequisite. Expected projection is fixed in fixtures: S-BINDING COMPLETED, S-EXEC BLOCKED, consumer PENDING, H2 retained, consumer prerequisite-eligible. Roots and slots remain untouched.

When evidence becomes stale, history remains admissible **as history**. Historical completion remains recorded, both knowledge records lose current validity, and the consumer ceases to be prerequisite-eligible. A BLOCKED producer does not invalidate current knowledge; a COMPLETED producer does not rescue stale knowledge. This is a qualification projection of prerequisite eligibility, not a replacement global scheduler.

Rejections cover substituted result/history, reordered sequence, wrong ledger/envelope, forged completion, omitted hold, unsupported release, stale override and incompatible validity context. Cold reload replays accepted records and holds against current validity; it must not copy an old eligibility conclusion. O02 and O06 share this predicate because one deterministic reconciliation addresses their common source-history boundary. Their mapping identities remain separate.

## PF-03 / O10 — graph admission and operational projection

`ADMIT_SOURCE_GRAPH_1` is `evaluate(..., 'GRAPH')`; `PROJECT_OPERATIONAL_GRAPH_1` returns its output only on ACCEPT. Inputs include exact graph/source identity, unique typed entities/assertions/predicates, accepted provenance, source pins, currentness, scope/lineage/context, and reviewed relationship rules.

Endpoint presence, predicate presence, identity domain, known relationship, provenance and evidence targets are checked before projection. Conflicting claims for the same subject/relation/object reject. All required assertions and transitive source supports must be current. An ordering cycle rejects; no malformed edge is dropped.

The profiles distinguish three source records:

1. EDGE1 is independently accepted REQUIRES evidence. BASE uses DETERMINISTIC_EXTRACTED / EXISTING_BASELINE; RENAMED uses ARTIFACT_REPORTED / READINESS_GATES. Its accepted provenance and reviewed rule admit a prerequisite edge.
2. EDGE2 is LLM_PROPOSED REQUIRES with a source ordering flag. Its provenance is descriptive only. Preserve it, but do not project it as an operational prerequisite.
3. EDGE3 is descriptive CORRESPONDS_TO. It never implies prerequisite ordering.

This preserves the frozen graph distinction between an ordering annotation and governed acceptance. Neither class alone grants truth. Only a reviewed admitted class/layer/provenance combination projects an operational edge. Other frozen relationship types remain subject to their original MAP-O10 rules; this finite profile does not invent scheduling semantics for them.

Projection returns accepted and descriptive assertion identities, sorted typed prerequisite pairs (prerequisite, dependent), and deterministic topological batches sorted by canonical entity ID. Source declaration order cannot resolve competing meanings. A source-array permutation is a different pinned artifact; once separately admitted, its set-like projection must use the same canonical order.

Negatives exercise dangling entity/predicate/evidence, unknown relation, wrong domain, missing accepted provenance, wrong graph identity/envelope, stale required support, conflicting claims, and illegal correspondence-as-ordering. Invalidation propagates through graph/evidence support and prevents admission after reload rather than restoring unsupported conclusions.

## PF-04 / O16 — composed operational instance

`ADMIT_COMPOSED_OPERATIONAL_INSTANCE_1` is **`compose(...)`**, not `evaluate(..., 'INSTANCE')` alone. The latter is only its internal source-profile check.

ACCEPT requires all five role sources, their exact pins and current dependencies, the reviewed context, complete field coverage, ACTION/HISTORY/GRAPH acceptance, and fresh evaluation of the independently pinned O08 predicate and both actual O09 slot predicates. Stored `accepted=true` values are not inputs. O08 must match the graph, plan and selection policy; both O09 submissions must match the graph and exact envelope. Submission/program identities are bound independently; a compatible-looking substituted proof fails.

The coverage manifest accounts for every source scalar or empty-container leaf by role, JSON pointer, canonical value digest, and preservation/validation disposition. Missing operational members, omitted coverage or substituted values reject. This is a small qualification witness of the same field-accounting requirement as the original MAP-O16 inventory; it does not claim that the real 2,910-entry source inventory has been restored by implementation.

Required correspondence is enforced for every represented member: graph/plan, runtime, controller-store generation, profile content, invocation, binding/dispatch/context absence or presence state, release/WorkAuthorization lineage state, ledger, selection policy and decision/proof submissions. A missing external object stays explicitly missing. Historical/provenance-only artifacts need references, not fabricated operational objects or a general artifact database.

Both source instances admit independently. Swapping one admitted graph into the other rejects SOURCE_PIN. Negatives also cover runtime, controller store, scope, profile, invocation, binding, authority lineage, release, ledger, policy, context, dispatch, partial instance, mixed stale/current support, coverage and admission substitution. Component validity is necessary but insufficient.

## O08/O09 interaction, invalidation and persistence

Composition invokes the existing O08 and O09 reference predicates, with their independent program pins and full submissions. Their source/provenance, authority exclusions, slot-specific proof types and envelope constraints are preserved, not reduced to graph booleans. O08 still grants only bounded implementation/test authority; it does not establish implementation completion or issuance authority. O09 still separates knowledge/PASS from exact slot-completion proofs.

Persist source objects, profile identity, role pins, accepted validity/dependency bindings, history/holds, context, admission submissions and program/schema identities. After cold decoding, revalidate the chain and recompute outputs. No conversation or previous Python objects are necessary for the specification. Invalidating any required source rejects composed admission; invalidating evidence preserves historical records while removing current proof use. Existing O08/O09 source-invalidation rules remain mandatory for their submissions. No invalidation is repaired by marking a historical producer COMPLETED.

## Validation and complete preflight

**313 specification cases PASS**: 251 existing cases replayed unchanged plus 62 new cases. Eight positive projections are checked against explicitly specified expected structures. Ten additional sequences invalidate each source role after canonical reload across both profiles; one additional sequence mixes independently admitted graphs. All 62 new cases also pass recursive object-key reversal, canonical round trip, reversed fixture execution order and repeated cold-process execution under seeds 0, 17 and 113. Semantic digest:

`4066636d7965eb02642ca73a8cb1463ddcc9e2e83d1e89727ddac96a43d72001`

These are specification conformance checks, not planner regression or restoration qualification. No runtime acceptance is inferred from them.

| Element | Independent mapping and executable rule | Complete preflight |
|---|---|---|
| O01 | MAP-O01 + ACTION source profile | EXECUTABLE_CONTRACT |
| O02 | MAP-O02 + imported HISTORY reconciliation | EXECUTABLE_CONTRACT |
| O03 | MAP-O03 + OR-BINDING/CONTEXT/PREP-VALIDATOR | EXECUTABLE_CONTRACT |
| O06 | MAP-O06 + hold/override HISTORY reconciliation | EXECUTABLE_CONTRACT |
| O08 | MAP-O08 + exact validator-authority admission | EXECUTABLE_CONTRACT |
| O09 | MAP-O09 + both baseline slot predicates | EXECUTABLE_CONTRACT |
| O10 | MAP-O10 + source GRAPH admission/projection | EXECUTABLE_CONTRACT |
| O16 | MAP-O16 + full `compose` profile | EXECUTABLE_CONTRACT |

No shared-domain conflict was found: all profiles use the same accepted-source/currentness separation, ledger and graph binding, explicit identity domains, and fixed selection-policy binding. No new contract promotes descriptive graph assertions, historical knowledge, or a compatible-looking grant into current proof.

C06A-3 retry requires the conjunction recorded in the preflight companion: pinned original mappings and O03/O08/O09 pass; source ACTION/HISTORY/GRAPH profiles pass; both composed instances pass including O08/O09; negative/invalidation/reload/order cases pass; eventual registry requirements are completely specified. All hold for specification preflight. Implementation conformance must still be established during the authorized retry; registry installation has not occurred.

```text
PF_01_STATUS = CLOSED
PF_02_STATUS = CLOSED
PF_03_STATUS = CLOSED
PF_04_STATUS = CLOSED
O01_EXECUTABLE = YES
O02_EXECUTABLE = YES
O06_EXECUTABLE = YES
O10_EXECUTABLE = YES
O16_EXECUTABLE = YES
O08_EXECUTABLE = YES
O09_EXECUTABLE = YES
SPECIFICATION_CASES = 313 PASS; 11 additional sequences PASS
C06A_3_CONTRACT_MISMATCH_SET = []
C06A_3_CONTRACT_CONFLICT_SET = []
C06A_3_RETRY_ALLOWED = YES
RESTORED_AND_QUALIFIED = 2/17
C06A_4_READY = NO
C07_RETRY_ALLOWED = NO
F03_STATUS = CLOSED
V0_1_CURRENT_STATUS = CORRECTION_REQUIRED
IMPLEMENTATION_MODIFIED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
```
