# Deterministic Planner v0.1 — E2-P05 A04 event/validation reconciliation 1

**RESULT = PASS for representation reconciliation. PROSPECTIVE_A04_EXECUTION_READY = NO.** The prior prospective contract overconstrained the event payload. P05 requires complete typed validation/result/ancestry assurance, but does not require the six validation values inline in one event. Native `ExecutionEvent.after_snapshot` binds the complete canonical Snapshot, which already serializes the six typed `ValidationInstance` records separately from the event result.

The remaining gap is **durable transaction and historical replay integration**. The qualified T02 operation accepts the validation tuple and returns the complete state atomically. The ordinary persisted event route does not call that operation or recover its historical validation operands. An immutable post-state reference establishes a content binding; it does not supply the missing execution/replay operation.

**PRIMARY_CLASSIFICATION = COMBINED:** `DOSSIER_OVERCONSTRAINED_EVENT_PAYLOAD` + `MISSING_ATOMIC_TRANSACTION_CAPABILITY`. No event-schema defect, missing identity domain or incomplete P05 assurance contract was established. A04/P05 remain unexecuted, P05 remains **10/13**, and runtime/E1 are unchanged.

The [machine companion](DETERMINISTIC_PLANNER_V0_1_E2_P05_A04_EVENT_VALIDATION_RECONCILIATION_1.json) contains all requested report fields. Evidence and the contract correction are under [qualification/E2_P05_A04_EVENT_VALIDATION_RECONCILIATION_1](qualification/E2_P05_A04_EVENT_VALIDATION_RECONCILIATION_1/). Every constructed event/state value is a comparison oracle, not an admitted occurrence witness.

## Authoritative representation and assurance

[Canonical A04](DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_ACCEPTANCE_MATRIX_1.md:47) requires applying the preparation result, then recomputing readiness only after complete dossier/checks. It requires canonical before/after identities and an event trace. The [P05 input oracle](qualification/E2_P05_END_INPUT_BINDING_1/input-oracle.json), `required_stage_inputs` for E2-A04, explicitly requires a `planner-event-v1` occurrence identity; Snapshot, KnowledgeId or a result label cannot substitute for that event. Neither source specifies that every typed check outcome must be inline in the event.

The [qualified T02 result](DETERMINISTIC_PLANNER_V0_1_E2_T02_RESULT.md) and its machine companion establish six admitted typed validation values, native dossier readiness, state-level atomicity and encode/decode retention. The machine report explicitly has `append_only_parallel_store=false`; its replay evidence is `encode_decode=PASS`. Those claims do not establish a complete event-bearing transaction and ledger replay for A04.

The selected scope decision remains exactly `AUTHORIZE_PROSPECTIVE_P05_A04_ANCESTRY_QUALIFICATION`, bound to unchanged subject:

`qualification-scope-subject-v1:4b57d7fc27d1c0b63deaece9d0be47c72e8e6d7b40e7a54ea7a56d6a641c85ac`

The original A04 historical ancestry and original A03 occurrence remain UNPROVEN. No authority was issued, no historical record rewritten, and no P05 binding created. The new contract overlay changes representation requirements only.

## Dossier validation inventory

All six expected values are native **ValidationInstance** records: result PASS, currentness ACCEPTED. Their common subject is dossier:

`planner-dossier-sha256:d0bbd6202b0a36b2524be8c85062c4e5015a0a30c55db90b4623b8769ce56f8b`

Their source is the unchanged [authored prospective dossier packet](qualification/E2_P05_A04_PROSPECTIVE_ANCESTRY_CONTRACT_1/inputs/dossier-source.json), raw identity:

`raw-file-sha256:f59fa16e93a2e70ba0df3f68425081e9ed2855deac23d234d69c4fd114c91235`

Each carries the exact sealed Provenance and ordered inputs `(pre-state SnapshotId, source identity)`. Scope is E2-QUALIFICATION-ONLY, lineage is E2-P05-A03-PROSPECTIVE-QUALIFICATION-1. Generation is bound through the exact Snapshot context/pre-state; ValidationInstance has no separate generation field. These are expected records, not currently admitted instances.

| VALIDATION_ID: native PredicateId | Proposition / why required | Old proposed event position |
|---|---|---|
| E2-CHECK-AUTHORITY_BOUNDARY | Preserve prospective USE boundary, independent-grant requirement and production/E1/proof exclusions | descriptor `validation_instances[0]` |
| E2-CHECK-CONCRETE_ALTERNATIVES | Exact ALLOW_QUALIFICATION_MAPPING and DECLINE alternatives | descriptor `validation_instances[1]` |
| E2-CHECK-DECISION_FACTS_COMPLETE | Accepted CHECK/COLLECT facts and completed producers satisfy the dossier fact requirements | descriptor `validation_instances[2]` |
| E2-CHECK-INDEPENDENT_VALIDATION | Checks evaluated independently from source/current inputs, with exact typed result/subject/currentness | descriptor `validation_instances[3]` |
| E2-CHECK-QUESTION_SCOPE | Exact question and bounded qualification-only subject/scope | descriptor `validation_instances[4]` |
| E2-CHECK-SOURCE_PROVENANCE | Exact source/raw pin and retained CHECK/COLLECT native result/input provenance | descriptor `validation_instances[5]` |

The old positions were fields of a **contract descriptor**, not registered event fields. The actual native storage is `Snapshot.validation_instances`, with unique PredicateId membership. The common consumer is [_evaluate_predicate](../../adapter/planner/gates.py:178) → [decision_readiness](../../adapter/planner/gates.py:289) → dossier admission/Planner Computation.

In the requested storage classification these are **SEPARATE_NATIVE_ENTITY** values: separately typed state records. This label does not make them GraphEntity objects or assign EntityIds. No standalone native ValidationInstance content-identity field exists. Their immutable occurrence binding is the Snapshot content identity plus the unique PredicateId and matching dossier identity, verified against the full typed member bytes.

The separate fact predicates E2-KP-CHECK/E2-KP-COLLECT are not additional validation instances. ASSUMPTIONS_CONSEQUENCES, DOWNSTREAM_QUALIFICATION and NO_INVENTED_FACTS remain descriptive/rehomed checks, not newly required dossier outcomes. The [inventory](qualification/E2_P05_A04_EVENT_VALIDATION_RECONCILIATION_1/dossier-validation-inventory.json) records exact source/provenance/content, consumers and locators for each value.

## Native event, result and validation schemas

The native envelope is [ExecutionEvent](../../adapter/planner/model.py:679), with the following supported fields:

| Field | Native type and role |
|---|---|
| sequence | int; ledger ordinal |
| parent_snapshot | ArtifactIdentity; exact pre-state |
| parent_event | Optional ArtifactIdentity; actual predecessor |
| result | Native typed result union; A04's existing representational branch is SuppliedResult |
| after_snapshot | ArtifactIdentity; immutable post-state reference |
| identity | ArtifactIdentity; canonical event content identity |
| resume_binding | Optional ArtifactIdentity; applies to qualified resume/reentry events, absent for PREPARE |

There is no generic `references`, `validation_instances`, `event_payload`, `command_id`, `scope` or `lineage` field on this envelope. Event payload means its `result` value. The codec rejects unknown fields rather than allowing arbitrary metadata wrappers.

The exact [SuppliedResult](../../adapter/planner/model.py:525) fields are `action: ActionId`, `result: ActionResult`, `knowledge: Tuple[KnowledgeRecord,...]`, `expected_snapshot: Optional[ArtifactIdentity]`, and `dossier: Optional[DecisionDossier]`. The event stores this typed value **inline**, not by a standalone ActionResult entity ID. PASS is an outcome enum, not an independently persisted result entity.

The dossier contains decision, provenance, question, scope, alternatives, checks, required_facts, deferred_downstream_facts, authority_granted_if_approved, authority_excluded and validation. Its DecisionChecks contain check kind, PredicateId and provenance. They are metadata/references; they do not contain the six evaluated validation outcomes. `DecisionDossier.validation` is dossier currentness and cannot replace those outcomes.

The [ValidationInstance](../../adapter/planner/model.py:431) fields are `predicate`, `proposition`, `dossier`, `inputs`, `result`, `scope`, `lineage`, `currentness` and `provenance`. T02 receives these through a separate tuple argument. They do not belong to SuppliedResult or the event body under the current schema, although semantically they are part of the preparation admission's supporting results.

Their original typed outcomes are persistent state inputs. On restore they are retained, not replaced by freshly evaluated independent validator decisions. Proof views, Readiness, selection and control are recomputed from those admitted values. Existing codec types and field/default/set rules are recorded in [native-schemas.json](qualification/E2_P05_A04_EVENT_VALIDATION_RECONCILIATION_1/native-schemas.json).

## Atomicity and current capability boundary

The exact qualified state operation is [admit_dossier_materialization](../../adapter/planner/core.py:338):

```text
snapshot + actual SuppliedResult + independently evaluated ValidationInstance tuple
    -> verify selected input Action, exact pre-state/result/dossier/bindings
    -> one returned state containing knowledge, PREPARE completion,
       dossier, six validations and decision readiness
```

It returns one immutable TransitionReport after all required checks pass. This is a native state-level atomic boundary. It does not create an event, append a ledger or publish a PersistenceBundle.

The existing durable framework uses [commit_event](../../adapter/planner/codec.py:868), a local head lock, trusted parent comparison, result application, immutable event/bundle writes, and [_publish_head](../../adapter/planner/codec.py:716). The canonical publication boundary is the atomic replacement of HEAD after validation/persistence. It already separates physical immutable artifacts from semantic transaction visibility: crash-created orphan files are not accepted canonical history. **Atomic does not mean one serialized payload.** E07's qualified source-admission/receipt path also illustrates a multi-object semantic transaction; it is not an A04 dossier adapter.

For the sealed A04 start, ordinary [apply_event](../../adapter/planner/core.py:547) dispatches SuppliedResult to apply_result. It never calls T02 with the six ValidationInstances. Ordinary [validate_result](../../adapter/planner/gates.py:122) also compares the supplied dossier with `Action.prepared_dossier=None` at this start. Preloading the dossier or validations would alter the sealed state and omit their actual atomic admission relationship.

Current [_replay](../../adapter/planner/codec.py:446) invokes `apply_event(state, event.result)` and checks the resulting state against `event.after_snapshot`. It does not resolve the post-Snapshot or final `bundle.current` as historical validation operands. PersistenceBundle contains initial/events/current; the event's post-state hash is not an implemented archive lookup. Historical intermediate typed outcomes must remain recoverable even after later changes; using the latest mutable state cannot supply them.

Source enrollment also needs integration: the new dossier source remains offline. Existing historical source-addition handling has explicit paths for other typed admissions, not T02 materialization. [ValidationSupportAdmission](../../adapter/planner/model.py:1544) and V02's commit/replay operation are specialized to Evidence/receipt/validation/support semantics, and cannot be substituted for dossier checks without semantic change.

Consequently **NATIVE_COMPOSITE_TRANSACTION_ALREADY_SUPPORTED = NO for complete A04 durable admission/replay**, even though all individual native values and content-reference fields already exist. The [transaction/replay trace](qualification/E2_P05_A04_EVENT_VALIDATION_RECONCILIATION_1/transaction-and-replay-gap.json) pins these implementations and distinguishes T02's state/snapshot retention evidence from missing ledger integration.

## Minimum composite native witness and identity correlation

The recovered representation is **D: an existing native composite witness**, with **C: transaction-level atomic commitment** required:

```text
actual enrolled ExecutionEvent
    -> inline SuppliedResult / KnowledgeRecord / DecisionDossier
    -> after_snapshot: immutable SnapshotId
        -> exact typed ValidationInstances + admitted output/dossier/state
    -> native PersistenceBundle: event membership, current state, source/policy pins
```

**A is not a P05 requirement.** **B has no dedicated native validation-object-ID field**, but the existing `after_snapshot` content reference provides lossless transitive binding to the exact typed state members. No new validation identity namespace, loose report pointer or eligibility Boolean is needed for that binding.

For each validation, verify canonical Snapshot bytes against `event.after_snapshot`, locate the unique native PredicateId, require the exact dossier identity and complete typed value, and compare scope/lineage/input/source/currentness to the sealed contract. The dossier content hash must match both the event's supplied dossier and the post-state's Action/Decision dossier. The output must match both `event.result.knowledge` and post-state knowledge with the exact producer/provenance.

The event hash binds sequence, pre-state, parent event, full typed result and post-state identity. Thus changing a validation's value/provenance changes the post-state identity and the event's content binding even when the validation is not inline. The post-bundle identity additionally binds event history, state and source/policy index. Native HEAD.previous correlates the exact prior bundle. SuppliedResult has no command identity, and its native HEAD command is None; no report transaction label substitutes for these bindings.

The [native correlation record](qualification/E2_P05_A04_EVENT_VALIDATION_RECONCILIATION_1/native-correlation.json) lists all these relationships. It proves a lossless representational association, not that the event was executed or the state durably admitted.

Using unchanged sealed result/state values, the existing codec can hash this **unadmitted comparison-only** event representation:

`planner-event-v1:2c71adfce820b0fc997e7d1f872439e9ddb43170c95edbeafaf461a4065760f0`

It references unchanged expected post-state:

`planner-snapshot-v1:38682b3fd1d13af1d056613048d85af131be2a31c0c918cc49e15c7cf6a808a4`

Its parent remains the actual prospective COLLECT event `planner-event-v1:d6ac0bb81a978ed5b8d8eb10195e75f75aba1af34c284e093f0ec8b70a797e8f`, with exact pre-state `planner-snapshot-v1:3af1c42da8555f4756be47fec23114bc00a8974ef830ef49ece16e67d9d4508f` and future sequence 3. No event was enrolled, no native store was written, and no actual A04 bundle was created. A representable event value is not an admissible transaction. The [representation oracle](qualification/E2_P05_A04_EVENT_VALIDATION_RECONCILIATION_1/oracles/composite-representation.json) is excluded from execution inputs.

## P05 assurance and N12/N13

| Assurance term | Minimum native evidence | Must be inline? |
|---|---|---|
| Occurrence | Actual admitted event enrolled exactly once in the continued ledger | Actual event is mandatory |
| Payload/prepare result | Full supported SuppliedResult, Action, PASS, output and dossier | Existing inline result |
| Parent/pre-state | Exact event parent, pre-state and supplied expected_snapshot with enrolled predecessor continuity | Existing event/result fields |
| Ledger position | sequence 3 / index 2, exact prefix/root/head and membership | Sequence in event; membership in bundle |
| Six validations | Exact typed members of the immutable referenced Snapshot, with dossier/input/provenance bindings | **No** |
| Output | Exact result KnowledgeRecord and matching post-state admitted record | Result and state |
| Post-state | Complete native Snapshot with identity equal to after_snapshot and deterministic transaction projection | Reference in event; body separate |
| Provenance | Complete native record values and raw source/policy pins at the same semantic boundary | Result/state/bundle |
| Readiness/control | Fresh Proof/Readiness/Computation over admitted authoritative inputs | Computed |

These terms remain jointly required. A Snapshot without the occurrence event, an event without parent/membership, or a tuple of accepted validations without atomic occurrence evidence is insufficient. Native correlation must establish the same A04 transition, not merely similar final state. See [P05-N12-N13-assurance.json](qualification/E2_P05_A04_EVENT_VALIDATION_RECONCILIATION_1/P05-N12-N13-assurance.json).

**N12 mapping is preserved:** selection/history alone cannot create completion, knowledge, event or head advancement. The composite witness still requires actual typed result admission and enrolled event ancestry.

**N13 mapping is preserved:** a prospective Action/output declaration, expected oracle or report cannot be used as the actual result. The future producer must supply a fresh bounded result and independently evaluated typed checks; native transaction admission and exact output/event/state binding remain required. No root/slot/knowledge advancement is permitted on rejection.

These are representation/assurance mappings, not fresh runtime negative qualification. All 24 sealed negatives remain required and unexecuted. Payload negatives apply to supported payload and immutable reference/body associations; omission of a nonexistent inline field is not itself a new negative. No original historical identity/ancestry edge is rewritten. The A04 replacement remains conditional and may eventually close only one P05 stage input.

## Contract correction and minimum required capability

The [versioned overlay](qualification/E2_P05_A04_EVENT_VALIDATION_RECONCILIATION_1/contract-revision-overlay.json) withdraws mandatory inline validation/source-addition fields and the conclusion that an event identity is unavailable merely because validations are not inline. It replaces them with exact native event/result/post-Snapshot/bundle correlation and atomic historical retention requirements. The earlier sealed files are unchanged; their start, source bytes, result oracle, validation values, post-state identity, negatives and assurance boundaries remain pinned.

**CONTRACT_REVISION_REQUIRED = YES; CONTRACT_REVISION_APPLIED = YES_AS_VERSIONED_OVERLAY.** The original contract's PARTIAL result is not rewritten or relabeled PASS. This reconciliation supplies its bounded representation correction.

The [minimum generic capability contract](qualification/E2_P05_A04_EVENT_VALIDATION_RECONCILIATION_1/minimum-generic-capability.json) requires:

1. Consume the actual SuppliedResult, independently evaluated typed validation tuple and exact raw source inputs against the trusted pre-bundle/state/head.
2. Invoke unchanged T02 semantics; atomically publish complete result/dossier/validation/output state, the native occurrence event, source pins and post-bundle. No accepted event may expose missing or misbound validation, and validations alone may not imply occurrence.
3. Retain original typed outcomes in a deterministically recoverable native historical representation. Replay verifies immutable identity/subject/pre-state/parent/source bindings and reproduces the state, without making a new validator decision.
4. Preserve source-enrollment boundaries, failure atomicity, exact retry/conflict behavior, cold restore and deterministic unordered-set semantics. No latest-state or writer-memory operand shortcut is allowed.

An inline typed materialization operand is one possible future implementation. A detached/reference implementation requires an explicit native archive/resolver and historical operand contract. Neither is currently an implemented A04 operation. This package does not select an unqualified storage layout, add fields/types, reuse A10 as A04, or implement either approach. The full native operation/replay contract must be established before runtime changes.

## Verification, readiness and preservation

Static probes verify existing schema round trips, immutable Snapshot/member/event correlation, unchanged identities under validation-record presentation permutations, identity changes under member-content changes, duplicate-selector rejection and rejection of an invented inline SuppliedResult field. They never invoke A04, model result application, event append/commit, native ledger replay or store publication. Expected Snapshot typing is not occurrence qualification.

Independent static readers repeat the representation checks across seeds 0,1,7,101 and original/reverse/rotate unordered validation presentations. Ordered ValidationInstance.inputs and event ancestry remain ordered. [verification.json](qualification/E2_P05_A04_EVENT_VALIDATION_RECONCILIATION_1/verification.json) records checks and byte-preservation of all pre-existing inventoried artifacts, including the sealed contract, 28 runtime files and 10,677 frozen E1 files. `git diff --check = PASS`.

Readiness stays NO because the native durable operation, source boundary and historical replay operand path remain unqualified. There is no missing authority decision in this package and no A04 execution. The next package is **GENERIC-PERSISTED-DOSSIER-MATERIALIZATION-TRANSACTION-CONTRACT**; P05 is not executed.

```text
WORK_PACKAGE = E2-P05-A04-EVENT-VALIDATION-RECONCILIATION
RESULT = PASS

DOSSIER_VALIDATIONS = SIX_TYPED_VALIDATIONINSTANCES; EXPECTED_NOT_ADMITTED
NATIVE_EVENT_SCHEMA = EXECUTIONEVENT_WITH_SUPPORTED_SUPPLIEDRESULT_BRANCH
NATIVE_RESULT_SCHEMA = ACTION_OUTCOME_KNOWLEDGE_EXPECTED_SNAPSHOT_OPTIONAL_DOSSIER
NATIVE_VALIDATION_REPRESENTATION = SEPARATE_TYPED_SNAPSHOT_MEMBERS; NO_STANDALONE_ENTITY_ID

TRANSACTION_BOUNDARY = T02_STATE_ATOMICITY_SUPPORTED; DURABLE_EVENT_INTEGRATION_MISSING
ATOMICITY_MODEL = ONE_SEMANTIC_COMMIT; NO_SINGLE_PAYLOAD_REQUIREMENT
EVENT_REQUIRED_FIELDS = [sequence, parent_snapshot, parent_event, result, after_snapshot, identity]
SEPARATELY_BOUND_FIELDS = [validation_instances, dossier_state, knowledge_state, context, source_policy_pins]
COMPUTED_FIELDS = [Proof, DecisionReadiness, Computation, selection, control]

NATIVE_CORRELATION = IMMUTABLE_EVENT_RESULT_DOSSIER_SNAPSHOT_MEMBER_BUNDLE_BINDINGS
REPLAY_CORRELATION = HISTORICAL_TYPED_OPERAND_RESOLUTION_AND_T02_DISPATCH_MISSING
P05_ANCESTRY_ASSURANCE = UNCHANGED; EVENT_AND_NATIVE_LEDGER_STILL_REQUIRED
N12_MAPPING = PRESERVED; RUNTIME_QUALIFICATION_NOT_RUN
N13_MAPPING = PRESERVED; RUNTIME_QUALIFICATION_NOT_RUN

PRIMARY_CLASSIFICATION = COMBINED
CLASSIFICATION_COMPONENTS = [DOSSIER_OVERCONSTRAINED_EVENT_PAYLOAD, MISSING_ATOMIC_TRANSACTION_CAPABILITY]
MINIMUM_CORRECTION = VERSIONED_COMPOSITE_WITNESS_OVERLAY_PLUS_GENERIC_DURABLE_DOSSIER_TRANSACTION_CONTRACT
CONTRACT_REVISION_REQUIRED = YES
CONTRACT_REVISION_APPLIED = YES_AS_VERSIONED_OVERLAY
RUNTIME_CAPABILITY_REQUIRED = YES

PROSPECTIVE_A04_EXECUTION_READY = NO
A04_EXECUTED = NO
P05_EXECUTED = NO
P06_EXECUTED = NO
P05_BOUND_STAGE_INPUTS = 10
P05_NEXT_MISSING_INPUT = E2-A04.prepare_result_event_ancestry

ORIGINAL_A04_HISTORICAL_ANCESTRY = UNPROVEN
ORIGINAL_A03_HISTORICAL_OCCURRENCE = UNPROVEN
P03_HISTORICAL_CORRESPONDENCE = UNPROVEN
N_REAL_SATISFIED = NO
RUNTIME_MODIFIED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
git diff --check = PASS
```
