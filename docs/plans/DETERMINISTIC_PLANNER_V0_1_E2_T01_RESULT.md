# E2-T01 — Post-restore evidence admission

RESULT = PASS. The fixed-version qualification passed 185 distinct tests (180 Planner and 5 invocation-constructor tests). This package implements native admission only. No E2-P01 or E2 experiment Action executes, and no E1 evidence or qualification authority is created.

## Pinned contract and counterexample

The exact SHA-256 identities of the reconciliation Markdown and event/state JSON are recorded in [validation](DETERMINISTIC_PLANNER_V0_1_E2_T01_VALIDATION.json). Both governing files remain unchanged.

Before implementation, an independent fresh interpreter restored a canonical synthetic waiting bundle as EXTERNAL_WAIT and found neither the admission API nor the registered event. The complete qualification request was subsequently checked against an isolated copy of the **exact hash-matched unchanged runtime**: cold restore passed and submission rejected with `unknown typed tag`. The isolated runtime was reconstructed and checked against every pre-change Planner source hash; it was not the modified implementation with its handler disabled. No existing supported interface was found.

The [pinned synthetic input](DETERMINISTIC_PLANNER_V0_1_E2_T01_FIXTURE.json) contains the initial canonical bundle, source bytes, request and separately stated expected receipt/proof/resume outcomes. Its receipt bytes are qualification-only and absent from initial Planner state. Construction of the test inputs is distinct from execution of an experiment Action. Historical control-regression fixtures are reused as source-bound synthetic starting contracts, not as real E1 migration evidence.

## Implementation

`EvidenceSourceAdmission` is the new native event. `EvidenceIngressContract` and `EvidenceFieldProvenance` describe the independently pinned ingress envelope and field sources. The event retains the specified parent bundle/snapshot/event identities, command key, gate, receipt action, requirements, source additions, evidence entity, ReceiptAdmission and field provenance.

The shared admission checker in `adapter/planner/evidence.py` is used by the existing event dispatcher and canonical replay. It accepts one current EVIDENCE entity and one independently authenticated ReceiptAdmission. It verifies the exact active gate, required proposition/target/producer correspondence, source class, scope/lineage/generation, expiry, pinned ingress bytes, canonical payload, source identity domain, bounded claim set and existing ATTEST authority. No authority, predicate, Action definition, rule-known update or arbitrary snapshot patch is accepted from evidence input.

`ReceiptAdmission.dependencies` is an additive provenance tuple. Its empty default is omitted from existing encodings, preserving old canonical bytes. New admissions retain ingress, gate, requirement, acquisition-route and independent trust sources. Source invalidation withdraws the dependent evidence support while preserving the original ledger receipt. The prefix replay check also rejects a source already invalidated before admission, including an ingress source not yet referenced by a received object.

`codec.admit_external_evidence` appends admission and ordinary EVIDENCE_RECEIVED events as a single durable pair. It verifies the complete candidate before writing source bytes. A published bundle cannot end with a standalone admission; direct `record_result`/CLI apply cannot bypass that pair requirement. The intermediate state is private to transaction construction/replay and conveys no accepted evidence observation.

The final source index is checked against disjoint event source additions. Replay reconstructs the initial source set and makes each addition available only at its own sequence. Each admission verifies its exact prefix bundle identity. This prevents newly received bytes from appearing as historical checkpoint input.

`codec.commit_event` commits later validation, reentry or invalidation under the same durable head discipline. CLI `admit-evidence` takes an explicit checkpoint identity, request, payload, source root and output store. CLI apply on a bundle containing admissions uses the same commit mechanism. The existing pure event/replay machinery, canonical bundle format and identity algorithms remain the state authority; no separate snapshot implementation was introduced.

## Atomicity, durability and replay

A single local writer lock serializes commands against the expected committed head. Immutable sources, events and bundle files are persisted before atomic head publication; file and directory fsync establish the acknowledgement boundary. The head's recorded predecessor and command are independently checked against the actual ledger prefix. A head is a discovery pointer, not a replacement for the caller's trusted checkpoint identity and verified lineage.

An exact committed retry returns its original transaction identity and the current bundle with `idempotent_noop=true`. It does not append, revalidate history as a new request or rewind later state. Conflicting reuse of the key rejects. A different command against an old parent rejects and must be revalidated against the new head. Two identical concurrent submissions create only one semantic receipt; two different gates can commit sequentially against successive parents.

Crash qualification terminates fresh subprocesses after actual fsync/link/replace boundaries. Recovery observes either the old committed parent or the complete two-event receipt, never admission-only state. Orphan immutable files are not treated as commits. These tests exercise process-crash recovery under the local POSIX rename/flock/fsync contract; they are not a hardware power-cut certification or a distributed-writer protocol.

## Staged semantics and invalidation

Receipt leaves the evidence obligation UNKNOWN and resume false. Separate native validation records observations and may complete the evidence gate. Accepted claims do not themselves provide accepted reentry lineage; C03 still requires current proof, verified source/policy pins and named-action eligibility. Separate reentry may make the synthetic named Action eligible, but no Action is executed by these tests.

A DISPROVED claim does not become positive applicability. A governed unknown remains unknown and returns to waiting when validation cannot establish a known proof. A stale ingress, route, evidence or independent attestor withdraws support. A stale gate rejects later receipt/validation as required by the existing lifecycle. Received history remains replayable, and no positive resume verdict survives the invalidation checks.

Authority requirement versus possession, proof requirement versus proof, selection versus execution and prospective versus actual results retain their existing native boundaries. No root/slot satisfaction, knowledge production or Action completion is synthesized by the admission transaction.

## Qualification evidence

The validation companion maps every reconciliation case T01–T20 to permanent tests in `adapter/tests/test_planner_evidence_admission.py`. Coverage includes cold-process CLI admission, separate validation/reentry, malformed/missing/cross-envelope inputs, provenance loss, source substitution, stale sources, duplicate/conflicting events, stale-parent rejection, historical claim conflict, pair completeness, source availability by prefix, route invalidation before receipt, invalidation after receipt, head audit tampering, process-crash recovery and concurrent writers.

Determinism checks use hash seeds 0,1,7,101, independent interpreters, source/predicate/field-provenance/dependency ordering, canonical object-key serialization and three cold restores per seed. They compare canonical transaction identities and full typed persistence round trips. Chronological ledger entries are not permuted as an unordered collection.

The full Planner discovery suite covers the existing A–N replay cases, X01–X11 invariants, C01–C06/refined C06, C06A budget, external-unknown correction, importer, CLI, persistence/replay, cold resume, selection, global controls and constructor-related native regressions. The separate invocation-constructor suite is also run. Counts and actual command outputs are retained in the validation companion; overlapping focused invocations are not counted as additional distinct tests.

## P01 reentry and release boundaries

Only E2-G01 is addressed by this capability. E2-G02–G07 remain: six complete O01/native Action definitions; concrete source roles/policy; root/slot proof and authority/dossier contracts; exact E2 external boundary; complete independent fixtures/oracles; and the checkpoint/cold-process harness. E2-G08 retains integrated-case/downstream dependencies. None is closed by these transaction tests.

Therefore E2_P01_RETRY_ALLOWED and E2_P02_READY remain NO. E2-P01 was not executed. N_REAL_SATISFIED, CANONICAL_E2_QUALIFIED and PLANNER_V0_1_REQUALIFICATION_READY remain NO. Planner status remains CORRECTION_REQUIRED.

## Final report

```text
WORK_PACKAGE = E2-T01
RESULT = PASS
PRE_IMPLEMENTATION_COUNTEREXAMPLE = REPRODUCED
POST_IMPLEMENTATION_RESULT = POST_RESTORE_LIVE_ADMISSION_PASS
EVENT_TYPE = EvidenceSourceAdmission
POST_RESTORE_LIVE_ADMISSION = PASS
ATOMICITY = PASS
DURABILITY = PASS
IDEMPOTENCE = PASS
REPLAY = PASS
FAIL_CLOSED_CONTROLS = PASS
PROVENANCE = PASS
DETERMINISM = PASS
TESTS_PASSED = 185 distinct (180 Planner + 5 invocation-constructor)
BASELINE_REGRESSIONS = PASS (160 existing Planner tests + 5 constructor tests)
POST_RESTORE_TRANSACTION_SUPPORTED = YES
OTHER_E2_P01_BLOCKERS = [E2-G02, E2-G03, E2-G04, E2-G05, E2-G06, E2-G07, E2-G08]
E2_P01_RETRY_ALLOWED = NO
E2_P02_READY = NO
N_REAL_SATISFIED = NO
CANONICAL_E2_QUALIFIED = NO
PLANNER_V0_1_REQUALIFICATION_READY = NO
V0_1_CURRENT_STATUS = CORRECTION_REQUIRED
IMPLEMENTATION_MODIFIED = YES
REAL_E1_EVIDENCE_CREATED = NO
E1_ARTIFACTS_MODIFIED = 0
DEFERRED_SCOPE_VIOLATIONS = 0
PRODUCTION_EFFECT = NO
git diff --check = PASS
```

The accepted fixed-version run consists of C06 (8 tests), C06A (6), remaining Planner modules (166), and invocation constructors (5). A preceding mixed-version discovery run had four failures in new subprocess checks while the source-class guard changed; it is retained as superseded evidence, not counted as a pass. The complete fixed-version rerun passed, and all tested code hashes remained unchanged afterward.

Preservation verification compared the exact path set and SHA-256 content of all 10,911 frozen E1 files against the pre-work inventory. Every pre-existing file in the baseline remained unchanged except the four native implementation files listed in the validation companion. Existing tests, governing contracts, prior planning results and E1 history were preserved. No E2 package or experiment Action executed.
