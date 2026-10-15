**DETERMINISTIC PLANNER v0.1 — DURABLE ADMISSION D01**

`RESULT = PASS`. `DURABLE_ADMISSION_CAPABILITY = PASS`.

The generic durable dossier-result transaction and historical replay are implemented and independently qualified. `A04_DURABLE_TRANSACTION_COMPATIBILITY = PASS`; `PROSPECTIVE_A04_EXECUTION_READY = YES`. Prospective A04 remains **unexecuted**. P05 remains **10 / 13**, with `P05_EXECUTION_READY = NO`.

The [machine companion](DETERMINISTIC_PLANNER_V0_1_DURABLE_ADMISSION_D01_RESULT.json) records the qualification gates, actual generic transaction, comparison identities, negatives, regressions and preservation hashes. This result closes the capability blocker in the immutable [durable-admission contract](DETERMINISTIC_PLANNER_V0_1_E2_P05_A04_DURABLE_ADMISSION_CONTRACT_1.md). Prior A04 contracts, inputs, oracles and reports remain unchanged.

**Implementation and transaction**

[dossier_transaction.py](../../adapter/planner/dossier_transaction.py) implements the narrow integration specified by the contract: a selected `DECISION_INPUT_ACQUISITION` Action with a qualified `NON_EFFECTING` producer and typed independent dossier validations. It contains no E2, P05, A04 or specific PREPARE identity. It reuses unchanged T02 `core.admit_dossier_materialization`, native result and Snapshot semantics, the existing event identity, source/policy pins, and the existing local commit primitives.

```text
trusted pre-bundle / exact parent / current contracts and pins
  → gate selected bounded producer before invocation
  → invoke actual producer; receive SuppliedResult + typed validations
  → check applicability, source, subject, context and ordered input bindings
  → apply through unchanged T02 native result admission
  → immutable post-Snapshot / unchanged native Snapshot identity
  → unchanged native occurrence-event payload / identity
  → hash-bound source-boundary replay binding
  → complete native PersistenceBundle
  → immutable source/archive/event/bundle staging and fsync
  → atomic publication of the unchanged PLANNER-HEAD-1 envelope
```

`register_producer` is a trusted application hook. Wire/data inputs cannot register executable code or turn an expected result into an executed candidate. `prepare` retains an origin-checked frozen actual effect; `commit` verifies that effect and the original prefix under the local lock. `execute` checks committed retries before calling the producer. Result declarations, raw supplied values, Boolean flags and manufactured candidate objects cannot bypass this boundary.

The admitted post-state comes from T02. The expected generic post-state was independently sealed before invocation and serves only as a comparison oracle. The positive fixture uses `GENERIC-ACQUIRE`, `GENERIC-DOSSIER-BUILD` and `GENERIC-REVIEW`; it uses no prospective A04 inputs, operation or result oracle. The actual bounded producer reads its authored source and admitted prerequisites, evaluates six rules and produces fresh native values.

**Native representation and identity**

[model.py](../../adapter/planner/model.py) adds exactly the frozen `DossierMaterializationBinding(event_identity, expected_bundle, source_additions)` and default-empty `PersistenceBundle.dossier_materializations`. [codec.py](../../adapter/planner/codec.py) omits that field when empty, preserving old canonical bundle bytes and identities. The binding has no standalone identity; the separate native bundle comparison hash covers it.

`ExecutionEvent`, `SuppliedResult` and `Snapshot` schemas remain unchanged. Validation bodies remain in the detached immutable `snapshot-<after_snapshot.sha256>.json` archive. The event retains its native result and existing `after_snapshot` reference. No dossier-only validation fields are added to its payload.

Each original validation member is selected by `(after_snapshot, PredicateId, dossier identity)` and its complete typed values. Admission checks the dossier subject, rule proposition, provenance, scope, lineage, accepted outcome and ordered `(pre-Snapshot, raw source)` inputs. Generation is bound by EvaluationContext and Snapshot identities. `Snapshot.validation_instances` is unordered and duplicate PredicateIds fail; `ValidationInstance.inputs` remains ordered. R05 does not declare this distinct input tuple unordered.

Identity construction is acyclic: existing pre-bundle/context/pins → actual result/typed values → post-Snapshot → event → temporal binding → post-bundle → HEAD. No identity is patched after publication. The [identity record](qualification/DURABLE_ADMISSION_D01/identity-qualification.json) contains both the actual generic identities and the unchanged A04 comparison-only identities.

| Actual isolated generic object | Native comparison identity |
|---|---|
| Event | `planner-event-v1:ddc44c096a2931654b63248b5339fe381923001f0bc6407e1be32da47215cbaa` |
| Post-Snapshot | `planner-snapshot-v1:3ef49429f0c9540188eb3c1ba68441e508840be1515483c2b1d1bf53e37c603e` |
| Post-bundle | `planner-bundle-v1:2d4cf2f419f67ab85f5de344dd742ee18e3a2743bf4a0b8440eee80e13c68406` |

The [actual transaction trace](qualification/DURABLE_ADMISSION_D01/generic-transaction-trace.json) binds the complete supplied result, six native validation members, source introduction, parent, sequence **2** / index **1**, archive, ledger and HEAD. Its independently sealed oracle predates execution.

**Atomicity, retries and historical replay**

All accepted effects become durable at HEAD publication. Precommit failures preserve the authoritative original state/head. Staged orphan files may remain, but their availability does not advance the accepted transaction head. Recovery after publication sees the complete new state. The scope is the existing single local writer lock and exactly-once **durable semantic occurrence**; a bounded producer may be invoked again following a precommit crash.

Qualification injects failures at all twelve named hooks: producer, typed validation, T02 application, Snapshot, event/binding, source staging, archive staging, event staging, bundle staging, files fsync, before HEAD replacement and after replacement. An actual replacement I/O failure is also tested. Four separate writers terminate at archive staging, files fsync, before replacement and after replacement; fresh recovery sees a complete old/new state and a clean commit or exact no-op retry.

Identical retries preserve one result/event/archive/bundle and return the historical transaction identity with the current verified head. Descendants remain intact. A prepared conflicting result, validation/provenance effect, source or stale/foreign parent fails closed. A retry of a committed transaction returns its recorded effect before invoking the qualified producer again.

Historical replay resolves each original `after_snapshot` from its native archive, verifies the temporal source boundary and exact pre-bundle binding, then uses the recorded result and typed outcomes for pure T02 state projection. It compares the **entire** projected Snapshot against the archive. It invokes neither the live producer nor independent validators and publishes no HEAD or second occurrence.

Archive resolution rejects missing, symlinked, noncanonical, wrong-domain and hash/model-mismatched objects. There is no fallback to latest `bundle.current`. Prefixes exclude future sources/bindings. After later invalidation, original accepted outcomes remain auditable in the archive while current validation becomes stale. Explicit resolvers supply historical objects to pure `bundle_bytes`, `bundle_id` and `_replay`; durable restore obtains the resolver from its archive directory.

**Independent qualification and regressions**

All **23 new test methods PASS**: the [20-test run](qualification/DURABLE_ADMISSION_D01/generic-tests.json) and [three additional controls](qualification/DURABLE_ADMISSION_D01/generic-extra-tests.json). They cover native applicability, typed bindings, immutable archive closure, complete post-state projection, atomic publication, retry/conflict, source/ledger tampering and declared unordered equivalence.

The [process qualification](qualification/DURABLE_ADMISSION_D01/process-qualification.json) passes twelve independent writers and twelve cold readers across hash seeds **0, 1, 7, 101** and original/reversed/rotated unordered presentations. A [final runtime writer/reader](qualification/DURABLE_ADMISSION_D01/final-runtime-process-check.json) also passes, bringing the totals to **13 writers / 13 readers**. Equal generic contexts in separate stores yield identical native event, Snapshot, bundle and descendant identities. Readers run after writer termination, reconstruct from native artifacts and perform three read-only replays with live admission/publication hooks barred.

The [negative matrix](qualification/DURABLE_ADMISSION_D01/negative-qualification.json) maps all 24 durable contract cases. Twenty-three are tested at the generic native transaction layer. Historical relabeling is tested separately by the qualification-overlay validator, which rejects five false history labels. The inherited **24 A04 negative expectations remain sealed and unchanged**; no A04 transaction or END mapping is performed in D01.

The [regression comparison](qualification/DURABLE_ADMISSION_D01/regression-comparison.json) records **153 / 157 affected test executions PASS**, covering result admission, dossier readiness, Snapshot/codec, event ledger, installation adapters/transactions, V02 validation/support, E07 ingress, typed root/slot proofs, receipt postconditions and invalidation. The same four failures occurred in the captured 275-test baseline; there are **no new failures**:

- `P04ReplayTests.test_x05_all_nine_checks_required_not_majority_vote`: legacy nine-check readiness expectation.
- `AdditionalAdmissionTests.test_conflicting_claims_are_not_overwritten`: missing legacy receipt observation.
- `AdditionalAdmissionTests.test_pinned_source_shaped_fixture`: `FIELD_PROVENANCE` rejection.
- `AdmissionTests.test_validation_and_reentry_separate`: legacy validation-stage expectation.

Those failures are recorded without repair. Execution counts include imported TestCase repetitions; they are not presented as counts of unique regression tests.

**Read-only A04 compatibility and preservation**

The [A04 compatibility record](qualification/DURABLE_ADMISSION_D01/A04-compatibility.json) passes **97 checks**. It restores only the retained CHECK/COLLECT start, verifies sealed inputs/authority/currentness and inspects the typed comparison oracles. A04 producer registration, execution, T02 admission and publication are barred. The native event and Snapshot comparisons remain exact:

- Event: `planner-event-v1:2c71adfce820b0fc997e7d1f872439e9ddb43170c95edbeafaf461a4065760f0`.
- Snapshot: `planner-snapshot-v1:38682b3fd1d13af1d056613048d85af131be2a31c0c918cc49e15c7cf6a808a4`.
- Future bundle **comparison only**: `planner-bundle-v1:45c06e9617034dfd86d96a2b5e7a86e156075751973fecb0112d671edb221bc7`.

The installed runtime can represent every sealed transaction requirement. Start, native Action, source bytes, inputs, result/event/ancestry oracles, END mapping, N12/N13 and all 24 negative expectations are unchanged. The originally missing native type now decodes and serializes to the exact sealed comparison wire. This check creates no accepted A04 result, archive, event or post-bundle and performs no A04 replay.

D01's readiness overlay sets `PROSPECTIVE_A04_EXECUTION_READY = YES`. Old PARTIAL/NO readiness reports remain immutable historical artifacts. Additional authority remains unnecessary under the exact sealed scope decision. The later execution package must load the exact start, invoke the bounded actual producer, verify all sealed oracles and stop on divergence.

The [preservation audit](qualification/DURABLE_ADMISSION_D01/preservation.json) verifies **15,333 prior files**. Only the two authorized pre-existing runtime files, `model.py` and `codec.py`, changed. All prior plan artifacts and all **10,677 frozen E1 files** retain their hashes. New runtime/tests/evidence are confined to D01. `git diff --check = PASS`.

```text
WORK_PACKAGE = DURABLE-ADMISSION-D01
RESULT = PASS
DURABLE_ADMISSION_CAPABILITY = PASS
IMPLEMENTATION_LAYER = GENERIC DOSSIER-RESULT / T02 DURABLE INTEGRATION
REUSED_NATIVE_CAPABILITIES = T02, RESULT/SNAPSHOT/EVENT CODECS, PINS,
                             LOCAL LOCK, IMMUTABLE FILES, FSYNC, HEAD
RESULT_APPLICATION = PASS
POST_SNAPSHOT = PASS
VALIDATION_BINDING = PASS
EVENT_CONSTRUCTION = PASS
LEDGER_APPEND = PASS
PERSISTENCE_BUNDLE = PASS
EVENT_COMPARISON_IDENTITY = UNCHANGED NATIVE ALGORITHM
SNAPSHOT_COMPARISON_IDENTITY = UNCHANGED NATIVE CODEC
BUNDLE_COMPARISON_IDENTITY = EXACT; NEW DEFAULT-OMITTED REPLAY BINDING
ATOMICITY = PASS
IDEMPOTENCE = PASS
FAILURE_INJECTION = PASS
COLD_RESTORE = PASS
HISTORICAL_REPLAY = PASS
REPLAY_IDEMPOTENCE = PASS
NEGATIVE_SUITE = PASS
DETERMINISM = PASS
REGRESSIONS = 153/157 PASS; FOUR UNCHANGED PRE-EXISTING FAILURES
A04_DURABLE_TRANSACTION_COMPATIBILITY = PASS
PROSPECTIVE_A04_EXECUTION_READY = YES
PROSPECTIVE_A04_EXECUTED = NO
P05_EXECUTED = NO
P06_EXECUTED = NO
P05_BOUND_STAGE_INPUTS = 10
P05_EXECUTION_READY = NO
ORIGINAL_A04_HISTORICAL_ANCESTRY = UNPROVEN
ORIGINAL_A03_HISTORICAL_OCCURRENCE = UNPROVEN
P03_HISTORICAL_CORRESPONDENCE = UNPROVEN
N_REAL_SATISFIED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
git diff --check = PASS
NEXT_PACKAGE = E2-P05-A04-PROSPECTIVE-ANCESTRY-QUALIFICATION-EXECUTION-1
```
