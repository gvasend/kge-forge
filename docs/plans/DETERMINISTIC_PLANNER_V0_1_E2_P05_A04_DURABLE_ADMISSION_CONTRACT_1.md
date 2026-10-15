**DETERMINISTIC PLANNER v0.1 — E2-P05 A04 DURABLE PREPARE ADMISSION + REPLAY CONTRACT 1**

`RESULT = PASS — CONTRACT ONLY`. `A04_DURABLE_TRANSACTION_IMPLEMENTATION_READY = YES`. `PROSPECTIVE_A04_EXECUTION_READY = NO`.

This contract closes the durable-admission and replay design gap. It does not implement, execute or qualify that capability. The current native path cannot satisfy the complete contract unchanged. A04, P05 and P06 remain unexecuted; P05 bindings remain **10 / 13**.

The [machine companion](DETERMINISTIC_PLANNER_V0_1_E2_P05_A04_DURABLE_ADMISSION_CONTRACT_1.json) contains the complete contract, source hashes and evidence references. This is a versioned overlay on the immutable [prospective ancestry contract](DETERMINISTIC_PLANNER_V0_1_E2_P05_A04_PROSPECTIVE_ANCESTRY_CONTRACT_1.md) and its [representation reconciliation](DETERMINISTIC_PLANNER_V0_1_E2_P05_A04_EVENT_VALIDATION_RECONCILIATION_1.md). Their original reports and all sealed input/oracle files remain unchanged.

**Authoritative semantics and preserved entry**

Canonical A04 applies the bounded preparation result and recomputes decision readiness. The earliest declarations are the canonical E2 plan `cases[3]`, acceptance matrix A04, PC01 `declarations[2]` and prospective dossier. T02 supplies the native dossier state-admission semantics. A04 establishes a complete dossier and accepted independent checks; it does not record a human choice or issue authority. END requires the native occurrence/ancestry witness. N12 separates selection/readiness from execution; N13 separates declared output from the actual supplied result.

The existing human scope authorization remains `AUTHORIZE_PROSPECTIVE_P05_A04_ANCESTRY_QUALIFICATION`, subject `qualification-scope-subject-v1:4b57d7fc27d1c0b63deaece9d0be47c72e8e6d7b40e7a54ea7a56d6a641c85ac`. There is no additional operating or INSTALL authority to issue. The exact native PREPARE Action has `authority = None`. This contract enrolls provenance with a result transaction; it installs no definition.

| Entry term | Exact sealed value |
|---|---|
| Start | [A03 prospective post-bundle](DETERMINISTIC_PLANNER_V0_1_E2_P05_A03_PROSPECTIVE_OCCURRENCE_BUNDLE_1.json) |
| Bundle | `planner-bundle-v1:b4a7494aa5617b4c913d23addf338361959a75d9cfee13b3ba2308f8ccb69a39` |
| State | `planner-snapshot-v1:3af1c42da8555f4756be47fec23114bc00a8974ef830ef49ece16e67d9d4508f` |
| Root / CHECK | `planner-event-v1:db8bc77aa2f5bd161272ed2e54993bf6d1c74b63d202d15af329ab64b51edd2c` |
| Head / COLLECT / A04 parent | `planner-event-v1:d6ac0bb81a978ed5b8d8eb10195e75f75aba1af34c284e093f0ec8b70a797e8f` |
| A04 append | Sequence **3**, index **2**, immediately after the exact retained two-event prefix |
| Scope | `E2-QUALIFICATION-ONLY` |
| Lineage | `E2-P05-A03-PROSPECTIVE-QUALIFICATION-1`, distinct from original historical lineage |
| Generation | `E2-P05-A03-PROSPECTIVE-GENERATION-1` |
| Policy | Exact retained pin and `E1-SELECTION-1-P06`; bundle scope `PARTIAL_HISTORICAL_REPLAY` |
| New raw source | `raw-file-sha256:f59fa16e93a2e70ba0df3f68425081e9ed2855deac23d234d69c4fd114c91235` |

No setup event, INSTALL, new genesis, source substitution or changed native Action is permitted before A04. The exact start Action inventory, authored source, six validator rules, result/post-state oracle, ordering, 24 negative expectations, END mapping and N12/N13 mappings are preserved by hash.

**Existing path and missing integrations**

The [path trace](qualification/E2_P05_A04_DURABLE_ADMISSION_CONTRACT_1/existing-path.json) pins the implementation and symbols. `core.admit_dossier_materialization(snapshot, supplied, validation_instances)` checks the selected decision-input Action, bounded PASS result, dossier and complete typed check set. It privately applies knowledge, PREPARE completion, prepared dossier, Decision stages/history and `Snapshot.validation_instances`, then requires native decision readiness. It returns one immutable `TransitionReport`. It creates no event or ledger entry.

`Snapshot` is already the native state value; `snapshot_bytes` and `snapshot_id` can encode and hash it. There is no need to add a second mutable state representation.

The ordinary durable path is `commit_event → record_result → apply_event → apply_result → _publish_head → save_bundle → bundle_bytes/_replay`. It does not route a fresh dossier result through T02. Ordinary `validate_result` requires the supplied dossier to match `Action.prepared_dossier`, which is `None` at the sealed start. `SuppliedResult` also has no validation-tuple operand. Replay currently uses only `event.result`; it has no resolver for the historical `after_snapshot` body. State-only T02 encoding/decoding does not close these gaps.

| Gap | Minimum integration |
|---|---|
| RESULT_APPLICATION | Use unchanged T02 admission for actual result plus independent typed validation tuple. |
| POST_SNAPSHOT_CREATION | Retain the existing native immutable Snapshot bytes after successful private admission. |
| EVENT_APPEND | Construct the existing occurrence envelope from that state effect. |
| EVENT_TO_POST_SNAPSHOT_BINDING | Resolve and verify the body named by existing `after_snapshot`. |
| PERSISTENCE_BUNDLE_COMMIT | Bind the source boundary and publish event, archive and bundle together at HEAD. |
| REPLAY | Recover historical typed operands and verify the complete T02 state projection. |
| OTHER | Detect identical/conflicting durable retries before invoking the producer. |

V02's `ValidationSupportAdmission` is specialized to Evidence/receipt validation and support. Its atomic-publication/replay approach is useful precedent; its payload and lifecycle semantics do not become a dossier transaction.

**Transaction operands, actual execution and outputs**

The generic operation is `GENERIC_PERSISTED_DOSSIER_MATERIALIZATION`, applicable to a selected native `DECISION_INPUT_ACQUISITION` Action with supported independent dossier checks. Its exact [operand/order contract](qualification/E2_P05_A04_DURABLE_ADMISSION_CONTRACT_1/transaction-contract.json) requires:

- The trusted native pre-bundle and external expected `planner-bundle-v1` identity. State, parent event, source/policy pins and EvaluationContext must match that bundle.
- The native ActionId and qualified bounded producer, bound to the current Action and pinned authored source rules. The operation owns its invocation. A caller Boolean or raw oracle result is not execution evidence.
- The exact new source artifacts as immutable `(ArtifactPin, bytes)` pairs, plus repository and transaction-directory roots under the existing filesystem constraints.

The producer creates a fresh native `SuppliedResult` and independently evaluated `Tuple[ValidationInstance, ...]`. It reads the sealed admitted inputs and authored source, never the expected-result/event/Snapshot oracle. The prospective result is bounded synthetic qualification output, with no claim about external-world facts.

Live preflight/admission uses the actual producer outputs. It passes those exact values to T02. Its private frozen candidate retains the trusted prefix, canonical actual result/validation tuple/source bytes, resulting Snapshot, event, binding and proposed bundle. Publication rechecks those same values and parent under the lock. An arbitrary supplied result or constructed expected Snapshot cannot bypass the live producer boundary. Historical replay uses a separate read-only verifier path with recorded outcomes.

Outputs are the committed native bundle/identity, full actual SuppliedResult in the native event, actual KnowledgeRecords/dossier/validation members in the Snapshot, occurrence event/identity, immutable Snapshot/identity, bundle replay binding, archive closure and HEAD/retry disposition. There is no new standalone ActionResult identity, ValidationInstance identity, Proof entity, permission record or authority grant.

**Chosen durable representation**

The event schema and native identity algorithm remain unchanged. Its payload is the existing `SuppliedResult` branch. The event retains full result/knowledge/dossier values and the existing native `after_snapshot` identity. Validation bodies remain exclusively in the immutable Snapshot.

The [binding contract](qualification/E2_P05_A04_DURABLE_ADMISSION_CONTRACT_1/snapshot-event-binding.json) defines two missing pieces for later implementation:

1. A detached native Snapshot archive. For each dossier-materialization event, retain `snapshot-<after_snapshot.sha256>.json` beside the immutable event/bundle artifacts. Its bytes are exactly `codec.snapshot_bytes(snapshot)`, with the existing `PLANNER-SNAPSHOT-1` envelope and `planner-snapshot-v1` hash. The resolver accepts that native identity and rejects missing, symlinked, noncanonical, wrongly typed or hash/model-mismatched content. Historical objects must survive later invalidation and descendant state changes.
2. An additive, default-omitted `PersistenceBundle.dossier_materializations: Tuple[DossierMaterializationBinding, ...]`. The new frozen binding has exactly `event_identity: ArtifactIdentity[planner-event-v1]`, `expected_bundle: ArtifactIdentity[planner-bundle-v1]` and `source_additions: Tuple[ArtifactPin, ...]`. It stores no validation bodies, separate result identity or redundant post-Snapshot reference. The native event supplies those relationships. The binding itself has no standalone identity; the trusted bundle hash covers it.

This bundle field is a **new contract**, currently absent from the native model/closed codec registry. It follows the repository's explicit additive-field/default-omission convention. Empty fields must be omitted so old bundles retain exact bytes and identities. Unknown fields and unregistered tags continue to fail closed. Bindings are an unordered collection unique by event identity; pin additions are an unordered unique collection. Event sequence remains ordered.

The binding is necessary to preserve the exact pre-bundle and when its new source pins became available. A post-Snapshot hash alone does not encode the pre-bundle's source inventory. An unbound report/sidecar cannot provide that native correlation. Exactly one binding must correspond to each dossier-materialization event; orphan/duplicate bindings fail. Prefixes retain only bindings for included events and exclude later source additions. Each binding's `expected_bundle` must match that reconstructed prefix before admission.

For this experiment there is exactly one raw dossier-source addition at A04. All previous source pins, policy, scope and ledger prefix remain unchanged. New pins must be required by dossier/check/ValidationInstance provenance and independently checked against the exact raw bytes. Reused pins are not reintroduced; unrelated pins are rejected.

**Snapshot and typed-validation binding**

The invariant is:

```text
actual result + original typed validation tuple + exact pre-state
    → unchanged T02 state admission
    → immutable post-Snapshot / native SnapshotId
    → native event(result, pre-state, parent, after_snapshot)
    → ledger membership + hash-bound bundle replay binding
    → committed trusted HEAD
```

The six ValidationInstances remain uniquely selected by native `(after_snapshot, PredicateId, dossier ArtifactIdentity)` and their complete canonical native member values. Their predicates cover AUTHORITY_BOUNDARY, CONCRETE_ALTERNATIVES, DECISION_FACTS_COMPLETE, INDEPENDENT_VALIDATION, QUESTION_SCOPE and SOURCE_PROVENANCE. Their subject is the exact dossier; ordered inputs remain `(sealed pre-Snapshot ID, authored raw-source identity)`. Scope/lineage/currentness/provenance must match. Generation is bound through EvaluationContext and native pre/post-state hashes, not an invented ValidationInstance field.

`Snapshot.validation_instances` is unordered under the codec; duplicate PredicateIds are prohibited. **`ValidationInstance.inputs` is ordered.** R05's unordered `ValidationResultRecord.input_identities` contract does not change this distinct field.

A changed validation-covered post-state term changes the native Snapshot identity, and therefore the event identity, or fails model/binding admission. A newly computed forged hash cannot substitute for the externally trusted bundle/event/HEAD anchor. Replay compares the **entire** projected Snapshot, so a correct validation tuple cannot conceal unrelated state changes. Standalone Snapshot availability does not establish occurrence.

**Commit order and atomicity**

The [commit/retry contract](qualification/E2_P05_A04_DURABLE_ADMISSION_CONTRACT_1/durable-commit-contract.json) uses the existing local transaction lock, immutable file creation, fsync and atomic HEAD replacement. It defines no distributed-writer semantics.

```text
verify sealed pre-bundle/pins
  → lock; restore/audit HEAD; check retry
  → require exact current parent and selected unexecuted producer
  → run actual bounded producer and independent checks
  → verify typed operands/provenance; apply T02 privately
  → require sealed independent result/postcondition
  → hash immutable post-Snapshot
  → construct native event; source-boundary binding; bundle
  → verify complete historical replay and ancestry oracle
  → stage immutable source/Snapshot/event/bundle files; fsync
  → reverify pins and parent
  → publish HEAD atomically; fsync
```

Every durable accepted effect belongs to that semantic transaction. Before HEAD replacement, failures leave the authoritative pre-state, ledger and HEAD unchanged. Files staged before a crash can remain as unaccepted orphans; their existence must not be represented as admitted occurrence. Trusted readers must verify complete archive/event/source closure before exposing a restored bundle.

No accepted result/knowledge/dossier may lack its occurrence event; no accepted event may lack the corresponding archived Snapshot and validation set. No head advancement may expose an incomplete bundle. A Snapshot/report cannot be qualified as occurrence without the native admitted event. Failure injection is required after producer, validation, T02, Snapshot/event construction, each staging step, fsync/pin verification and HEAD publication.

Existing `PLANNER-HEAD-1` is preserved: new bundle identity, `previous = exact pre-bundle identity`, `command = None` for this SuppliedResult event. HEAD audit and prefix reconstruction must learn the new bundle binding. A failure after replacement creates an uncertain acknowledgement, not a guaranteed rollback; retry reads and validates HEAD to determine the outcome.

**Idempotence and conflicts**

The intent is the tuple of existing native identities `(trusted original pre-bundle ID, original parent Snapshot ID, original parent event ID, ActionId)`. No new command-identity namespace is introduced. Effect equality covers the full canonical result, original typed validation members, source pins/bytes, Snapshot and event/bundle identities.

Before invoking a producer on retry, find the original exact native prefix and its next event. If that committed transaction matches the intent and effect, return its historical committed identity and the current verified head without another result, event, ledger entry, Snapshot object or bundle. Preserve descendants. A prepared-candidate retry must match the archived committed result/tuple/source effect exactly. A changed result, validation, source, context, consumed parent or unprovable prefix fails closed.

After a precommit failure, the same verified pre-state can be retried; immutable orphan artifacts must match or conflict. This is exactly once **durable semantic occurrence**, not exactly once producer callback invocation across crashes. The bounded producer is NON_EFFECTING here. Reasserting a new current parent for an already completed producer cannot create a second occurrence. The old state-level T02 no-op alone is insufficient.

**Cold restore and historical replay**

The [replay contract](qualification/E2_P05_A04_DURABLE_ADMISSION_CONTRACT_1/replay-contract.json) requires trusted bundle/HEAD identity, canonical bundle, immutable event files, detached Snapshot files and raw source/policy pins. It must work after writer termination without its memory or expected-state oracle.

Replay starts with the original native initial Snapshot. Initial sources are the final source manifest minus all explicitly bound introductions, including existing ingress/INSTALL mechanisms. For each event, verify sequence, exact pre-state, parent, identity and historical source boundary. At a dossier binding, require the reconstructed prefix's native bundle identity to equal `expected_bundle`.

Resolve `event.after_snapshot` from the archive. Select the original complete typed validation members by the native dossier/check predicates, verify subject, ordered inputs, provenance, context and exact source introductions, then use `event.result` and these historical outcomes for the unchanged T02 **state projection**. Compare all resulting canonical Snapshot bytes to the archived Snapshot, then its hash to `after_snapshot`. Do not call the live PREPARE producer, acquire inputs or rerun independent validators. Native model/readiness checks can recompute over the recorded authoritative values.

Fold each historical event once. Replay does not publish HEAD, append an occurrence or create a new permission/authority/result. Finish by checking exact current Snapshot and source inventory. `bundle.current` cannot supply historical outcomes for an earlier materialization. Missing archives fail even if a later state/report retains equivalent values. Later invalidation events replay separately: the original event/archive remains auditable while current usability/readiness can change.

Cold readers must recover A04's full native event/result, exact parent, ledger membership, sequence3/index2, bounded output, post-Snapshot and all six typed member bindings. There is no separate native LedgerId: membership is the trusted bundle identity plus `#/bundle/events`. The original root and A04 head relationship must remain exact. END continues to consume event ancestry, not state equivalence.

**Identity construction order**

The [identity DAG](qualification/E2_P05_A04_DURABLE_ADMISSION_CONTRACT_1/identity-order.json) has `IDENTITY_CYCLE = NO`:

```text
existing pre-bundle / pins / context
    → actual result / dossier / validation values
    → post-Snapshot bytes / ID
    → event bytes / ID
    → bundle temporal binding
    → post-bundle bytes / ID
    → HEAD
```

Native Snapshot contains no ledger/head field. Its inputs refer to the existing pre-state/source, never the new event or bundle. The event then references that immutable post-Snapshot. The binding references the **pre**-bundle and event; the final bundle hashes the binding. Reader ledger pointers do not feed back into these hashes. No mutable identity or post-publication patch is permitted.

The [comparison oracle](qualification/E2_P05_A04_DURABLE_ADMISSION_CONTRACT_1/oracles/prospective-native-binding.json) preserves:

- Dossier: `planner-dossier-sha256:d0bbd6202b0a36b2524be8c85062c4e5015a0a30c55db90b4623b8769ce56f8b`.
- Post-Snapshot: `planner-snapshot-v1:38682b3fd1d13af1d056613048d85af131be2a31c0c918cc49e15c7cf6a808a4`.
- Unchanged native event: `planner-event-v1:2c71adfce820b0fc997e7d1f872439e9ddb43170c95edbeafaf461a4065760f0`.
- Future post-bundle with the proposed binding: `planner-bundle-v1:45c06e9617034dfd86d96a2b5e7a86e156075751973fecb0112d671edb221bc7`.

These are **comparison-only identities**, not occurred/admitted state or a new PersistenceBundle accepted by the current runtime. The existing codec rejects the proposed additional binding today. No native target/archive/HEAD has been published.

**Negatives, scope and overlay**

All original 24 negative expectations remain sealed and unexecuted. The [durable negative contract](qualification/E2_P05_A04_DURABLE_ADMISSION_CONTRACT_1/negative-contract.json) adds 24 explicit cases covering the requested result/execution/pre-state/parent/Snapshot/state/event/ledger/head mismatches, foreign or missing validation binding, event without result, result without event, duplicate/conflicting retry and second replay occurrence. It also covers pin/source-boundary changes, archive loss after descendant invalidation, orphan acceptance, binding/member duplicates, ordered-input reversal and historical relabeling. Identical retry is a valid no-op; the rejected behavior is a second semantic append.

Future generic qualification must run positive durable admission, all inherited/durable negatives, failure injection, retries including descendants, writer-exit cold readers, historical replay after later invalidation and seeds **0,1,7,101** with native-declared unordered permutations. Replay must demonstrate zero producer/independent-validator calls. These are requirements, not completed runtime tests in this package.

The [versioned overlay](qualification/E2_P05_A04_DURABLE_ADMISSION_CONTRACT_1/versioned-overlay.json) supersedes only the already-reconciled inline-payload mandate and the formerly unresolved durable/archive/source-boundary/retry/replay design. It preserves all actual inputs, result/post-state semantics, authority scope, END mapping, N12/N13 expectations and historical labels. The new future bundle binding changes only the prospective post-bundle identity; it leaves the sealed start, native event and post-Snapshot exact.

```text
QUALIFICATION_TYPE = PROSPECTIVE_REPLACEMENT
ORIGINAL_A04_HISTORICAL_ANCESTRY = UNPROVEN
ORIGINAL_A03_HISTORICAL_OCCURRENCE = UNPROVEN
HISTORICAL_RECONSTRUCTION = NO
PROSPECTIVE_A04_EVENT_IS_ORIGINAL_EVENT = NO
```

A successful later execution can close only `E2-A04.prepare_result_event_ancestry` through the authorized replacement mapping. It does not insert the new event into original historical ancestry. This package applies no mapping; P05 stays 10/13, A05/A06 remain unbound and the full original END-history gap remains separate. N12/N13 assurance is preserved because actual complete native occurrence remains mandatory.

**Readiness and preservation**

All eleven implementation-contract gates are complete: operands, outputs, Snapshot/event binding, atomicity, idempotence, bundle, cold restore, replay, identity order and negatives. The missing capability belongs at the generic dossier/PREPARE integration layer. It composes T02, existing Snapshot/result/event identities, source pins and existing local commit primitives; it does not require an A04-specific persistence system or a wholesale result-transaction redesign.

Execution remains blocked on implementation and independent qualification of the Snapshot archive/resolver, minimal bundle binding, T02 event dispatch, prefix-source handling, retry and historical replay. The next package implements/qualifies those generic pieces without executing the primary prospective A04. A later execution package must pass every sealed entry check and stop on any divergence, with no live repair.

Verification in this package is static contract/schema/hash/identity inspection only. Twelve fresh static readers cover four hash seeds and three unordered presentations. The [verification record](qualification/E2_P05_A04_DURABLE_ADMISSION_CONTRACT_1/verification.json) distinguishes those checks from unrun native commit/cold-restore/replay/negative qualification and verifies preservation of 15,318 existing files, including 28 runtime files and 10,677 E1 files.

```text
WORK_PACKAGE = E2-P05-A04-DURABLE-ADMISSION-CONTRACT
RESULT = PASS — CONTRACT ONLY
EXISTING_PREPARE_PATH = T02 STATE ADMISSION; DURABLE INTEGRATION ABSENT
DURABILITY_GAPS = RESULT_APPLICATION, POST_SNAPSHOT_RETENTION, EVENT_APPEND,
                  EVENT_SNAPSHOT_RESOLUTION, BUNDLE_COMMIT, REPLAY, RETRY
TRANSACTION_OPERANDS = SEALED
TRANSACTION_OUTPUTS = SEALED
TRANSACTION_ORDER = SEALED
POST_SNAPSHOT_BINDING = NATIVE SNAPSHOT ARCHIVE + EXISTING after_snapshot
EVENT_BINDING = UNCHANGED NATIVE ENVELOPE/IDENTITY
ATOMICITY = SEALED HEAD-PUBLICATION CONTRACT
IDEMPOTENCE = SEALED NATIVE-INTENT/EFFECT NO-OP/CONFLICT CONTRACT
PERSISTENCE_BUNDLE_CONTRACT = SEALED DEFAULT-OMITTED REPLAY BINDING
COLD_RESTORE_CONTRACT = SEALED; NOT EXECUTED
REPLAY_CONTRACT = HISTORICAL PROJECTION; NO NEW PREPARE DECISION
IDENTITY_DEPENDENCY_ORDER = STATE → EVENT → BINDING → BUNDLE → HEAD
IDENTITY_CYCLE = NO
NEW_CAPABILITY = GENERIC DOSSIER/PREPARE DURABLE ADMISSION + REPLAY
NEGATIVE_CONTRACT = ORIGINAL 24 PRESERVED + 24 DURABLE CASES; NOT RUN
A04_DURABLE_TRANSACTION_IMPLEMENTATION_READY = YES
PROSPECTIVE_A04_EXECUTION_READY = NO
A04_EXECUTED = NO
P05_EXECUTED = NO
P06_EXECUTED = NO
P05_BOUND_STAGE_INPUTS = 10
P03_HISTORICAL_CORRESPONDENCE = UNPROVEN
N_REAL_SATISFIED = NO
RUNTIME_MODIFIED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
git diff --check = PASS
```
