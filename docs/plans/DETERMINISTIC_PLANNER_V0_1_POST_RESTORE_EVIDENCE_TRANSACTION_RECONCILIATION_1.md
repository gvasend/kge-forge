# Post-restore evidence transaction reconciliation 1

**CLASSIFICATION = MISSING_RUNTIME_CAPABILITY. EVENT_TYPE_CLASSIFICATION = NEW_EVENT_TYPE_REQUIRED.** Cold restore already returns a bundle capable of accepting the five registered event types. What is missing is authenticated, source-indexed evidence insertion into that bundle's replay lineage. Existing receipt events reference previously admitted evidence; they do not perform source admission. This contract defines the bounded addition, without implementing or qualifying it.

E2-P01 remains blocked. This document neither satisfies E2-G01's implementation prerequisite nor completes its remaining fixture/oracle work. E2-P01 retry and E2-P02 readiness remain NO. N-REAL is unchanged and unsatisfied.

The [event/state/test companion](DETERMINISTIC_PLANNER_V0_1_POST_RESTORE_EVIDENCE_TRANSACTION_RECONCILIATION_1.json) pins the P01 report and all six companions, E2 plan/matrix, N-REAL reconciliation, control repair and inspected runtime sources. All proposed names below are contract declarations, not currently available APIs. No authority, evidence bundle, Action execution or runtime modification is created here.

## Current input surface

| Interface | Classification | Capability / boundary |
|---|---|---|
| decode_snapshot / constructors | INITIAL_LOAD_ONLY | Build initial canonical state; not a live transition or ledger-preserving substitute. |
| replay.import_fixture / load_p03/p04/p05 / import_budget | INITIAL_LOAD_ONLY | Pinned bounded historical/synthetic fixture imports; PLANNER-REPLAY cases A-N, not live evidence ingestion. |
| replay.import_e1 / restore_accepted_knowledge | INITIAL_LOAD_ONLY | Frozen import reconstruction, not live receipt; cannot reset a restored ledger. |
| codec.restore / _replay | REPLAY_ONLY | Verify canonical bundle/source pins/event files; replay event history and return immutable live bundle. |
| core.apply_result / SuppliedResult | LIVE_COMMAND | Add only bounded declared knowledge and status; no evidence entity/source-index insertion. |
| core.apply_recorded_decision / RecordedDecision | LIVE_COMMAND | Record independently applicable decision and permitted result; no arbitrary grant/entity ingestion. |
| core.apply_decision_reentry / DecisionReentry | LIVE_COMMAND | Reenable declared routes subject to native checks; no evidence import. |
| core.apply_receipt / ExternalEvent | LIVE_EVIDENCE_RECEIPT | Lifecycle reference to existing produced entity; validation evaluates independent ReceiptAdmission. |
| core.apply_event / SourceInvalidation | LIVE_COMMAND | Mark dependent state stale; cannot create positive evidence. |
| codec.record_result / append_event | LIVE_APPEND | Construct/verify sequenced events and replay lineage; source table is not extended. |
| CLI apply --event | LIVE_COMMAND | Decode registered event, record_result, plan_output and save_bundle; same closed union. |
| CLI replay | REPLAY_ONLY | Apply fixture supplied event list and compare harness expectations; no extra event capability. |
| CLI validate / plan / restore | OTHER | Read/compute/save existing state; no new evidence transaction. |
| save_bundle | OTHER | Immutable persistence of already valid replay state; not admission. |
| tests synthetic_receipt / dataclass replace | OTHER | Test setup, not supported live runtime transaction. |

The core's pure transition functions produce candidate snapshots, not durable commits. `record_result` constructs an ExecutionEvent; `append_event` validates lineage and returns a new immutable bundle. The CLI's `apply` delegates to these, then `save_bundle`. Importing a fresh fixture or frozen E1 constructs a different initial state; it does not extend the restored history.

Evidence: [model.ExecutionEvent](../../adapter/planner/model.py#L606), [core.apply_event](../../adapter/planner/core.py#L430), [core.apply_receipt](../../adapter/planner/core.py#L450), [codec.append_event](../../adapter/planner/codec.py#L454), [CLI](../../adapter/planner/__main__.py). No additional runtime server, streaming ingress or mutable Planner session interface is defined in this inspected Planner package. `replay.import_fixture` restricts replay case identifiers to A–N; it must not be repurposed as a live E2 importer. Initial canonical construction may use native types as planned.

## Cold restore to live input

1. `save_bundle` validates replay, checks source pins, writes immutable event artifacts and canonical bundle bytes, and returns the bundle path/identity. Snapshot and bundle identities use distinct `planner-snapshot-v1` and `planner-bundle-v1` namespaces. The process may terminate after persistence.
2. A fresh process supplies the exact trusted expected bundle identity to `restore`; the CLI obtains it from the requested content-addressed filename. A filename is a transport for a caller-chosen pin, not independent trust if the attacker can replace both name and bytes.
3. `restore` rejects symlinks, incorrect identity/schema/canonical bytes, altered sources and missing/changed immutable event files. `bundle_bytes` invokes `_replay`: validate initial/current types, policy and provenance pins; replay sequential events; check sequence/parent/event/outcome identities and equality with stored current snapshot.
4. The returned `PersistenceBundle` is immediately an input to `record_result`/`append_event`. There is no additional session activation step. `plan_output`/`recompute` derive current state and C03 resume proof. Source verification is mandatory for a positive resume verdict.

Restoration replays historical commands; it does not resubmit them as fresh requests. A new live command must name the current snapshot and ledger parent, producing sequence n+1. Replay never reassigns a sequence number, consumes current wall-clock time, or obtains new trust through repository search.

## Why a new event is required

`ExternalEvent` contains gate, lifecycle stage, expected_snapshot and optional artifact EntityId. `EVIDENCE_RECEIVED` requires an already-produced entity. [ReceiptAdmission](../../adapter/planner/model.py#L909) explicitly represents independently admitted trust, never supplied by the receipt event. [_check_receipt](../../adapter/planner/gates.py#L318) independently verifies content, producer competence and claims. Neither `SuppliedResult` nor RecordedDecision inserts new GraphEntity/ReceiptAdmission objects. SourceInvalidation withdraws support only.

Extending ExternalEvent to accept arbitrary snapshot fragments would mix evidence admission and receipt and weaken this separation. The minimum contract is **one new bounded EvidenceSourceAdmission payload**, followed by the existing ExternalEvent receipt. There is no second semantic Planner path and no generic snapshot-patch interface. The current native event union/codec does not admit the new payload yet.

This is a missing capability with a missing event/source-evolution contract, now specified here; it is not a P01 fixture defect or an overlooked supported interface. Existing receipt evaluation remains valid for pre-admitted inputs. The new live behavior has not been reproduced by executing a failing experiment in this task.

## Proposed bounded transaction

`admit_external_evidence(expected_bundle, expected_snapshot, expected_parent_event, canonical_request, immutable_source_bytes, committed_head)` is a proposed transaction API. It must:

1. Acquire the single-writer serialization boundary and verify the caller's expected committed head and parent. Check an identical committed retry before rejecting its old parent; that retry returns the original outcome, never reexecutes it.
2. Verify the pre-state and all required source/trust/route pins. The gate must be current, contract-complete and WAITING_FOR_EXTERNAL_EVIDENCE. Resolve the exact receipt action, requirements/propositions, producer, target and operational context. No inference from filenames or arbitrary waiting labels.
3. Validate bytes/schema/content pins and deterministic field provenance. Stage immutable source bytes privately. New bytes are untrusted input; no public state change or proof follows from staging.
4. Apply EvidenceSourceAdmission privately, producing ledger event n+1 and a source-index delta. Independently verify the source/producer authentication contract; receipt authority does not imply proposition truth. Only the declared evidence entity and ReceiptAdmission may be inserted.
5. Apply ordinary `ExternalEvent(... EVIDENCE_RECEIVED, expected_snapshot=intermediate_identity, artifact=new_entity)` privately as event n+2. This changes pending receipt and lifecycle history, not accepted observations. Verify the two-event pair and its final state.
6. Persist the source blobs, both events and resulting bundle; commit the trusted head last. Return success only after the durability boundary. Do not expose the intermediate admitted-only snapshot to planning or execute any Action.
7. Later commands use the unchanged validation and reentry events, each durably recorded through the same commit discipline. Recompute never directly sets resume permission.

The input request may arrive before source validation; it is not an accepted canonical ledger entry until verified. This reconciles “receipt request → persistence” with fail-closed admission: malformed requests may be separately logged as diagnostics but never become canonical accepted receipts.

### Event and source derivation

| Field | Contract |
|---|---|
| schema | literal PLANNER-EVIDENCE-ADMISSION-1 |
| expected_bundle | ArtifactIdentity CONTENT_IDENTITY/planner-bundle-v1 of exact pre-transaction prefix |
| expected_snapshot | ArtifactIdentity CONTENT_IDENTITY/planner-snapshot-v1 |
| expected_parent_event | last ExecutionEvent.identity or null for empty ledger |
| command_key | content identity of canonical request excluding this key; namespace planner-evidence-command-v1; includes exact parent and request fields |
| gate | existing GateId at WAITING_FOR_EXTERNAL_EVIDENCE |
| receipt_action | exact gate.receipt_action string, not inferred ActionId |
| requirements | sorted nonempty distinct EvidenceId subset of gate requirements; proposition and typed target must match pre-state declarations |
| contract_pin | current pinned ingress contract content identity, part of pre-state source table |
| source_additions | nonempty sorted unique ArtifactPin list for new immutable evidence bytes only; RAW content identities; no replacement pins |
| entity | one GraphEntity EVIDENCE with deterministic EntityId, typed raw-content identity, provenance, exact context scope/lineage/generation, expiry |
| admission | one ReceiptAdmission bound to entity, producer, target, unique claims and existing independently trusted authentication PredicateId |
| field_provenance | selectors into new bytes or pinned pre-state ingress/requirement/route/trust records for every inserted field; no implementation defaults |

The source payload uses the existing canonical receipt body, exactly `producer`, `target`, `claims`, with typed identities and claims sorted by native canonical bytes. Content identity is CONTENT_IDENTITY / raw-file-sha256 over those bytes; file whitespace must not silently change that contract. Each claim names a declared EvidenceId and native non-UNKNOWN ProofState. Duplicate claims, undeclared fields and unrelated requirements reject. DISPROVED is a possible received claim, never coerced to PROVED.

Define the inserted EntityId deterministically as `EVIDENCE:` plus SHA-256 of canonical typed `{gate, content_identity, scope, lineage, generation}` under the explicit evidence-entity-v1 derivation contract. Entity identity and raw content identity remain distinct. Claim producer/target come from the payload and must exactly match the pre-state requirement and trust; they are not copied from a known expected output. Scope/lineage/generation come from the pinned ingress contract and equal EvaluationContext and governing route. `valid_until` is an explicit pinned ingress expiry, checked against the pre-state deterministic context tick; never a hidden clock/default. Provenance identifies exact new bytes/selector, contract version and supporting current route/trust identities. Source path is an immutable content-addressed storage locator; it does not confer a semantic role.

The new entity has kind EVIDENCE, produced=true meaning bytes were admitted, validated=true meaning the source object passed structural admission, and native ACCEPTED source validation. These existing flags do **not** establish an accepted evidence observation. No permissions, consumed authority, decision choice or validator power can be supplied by this payload. Explicit native neutral fields remain false/empty/null. Entity and admission provenance must agree with verified bytes. Provenance dependencies must remain sufficient for native invalidation after reload; support cannot exist only in the new command's transient memory.

The ingress contract is a versioned, pinned declaration in the pre-state source set, bound to the exact gate/receipt/requirement/source class/envelope. It defines allowed payload schema, field selectors, identity derivation, expiry and the existing authentication PredicateId. Its identity is checked on live admission and replay. It cannot define arbitrary executable callbacks or broaden permission. New source additions are raw evidence bytes only; the payload cannot import its own authority, policy, predicate, ingress contract or new Action.

### Independent receipt authority

The active route authorizes delivery for a missing proposition. Producer competence additionally requires a pre-existing current AUTHORITY predicate with ATTEST permission, expected exact evidence content identity, and an independently sourced authority entity whose identity equals the producer. This preserves native `_check_receipt` semantics. The trust source and evidence source may not share the same identity/path. Verified pins establish bytes, not competence by themselves.

This bounded contract supports evidence whose exact authentication premise is already pinned. E2 can declare the expected synthetic content identity and qualification-only attestor ahead of time without storing or receiving positive evidence before the checkpoint. It cannot count the attestor as applicability proof. An unknown future producer, changed payload needing a different grant, or new authority issuance requires a separately governed trust-admission contract; this package does not invent that capability.

On the mainline, obligations are evaluated through ReceiptObservation/EVIDENCE_OBLIGATION, so merely adding the evidence object cannot satisfy them. Reject ingress configurations where source admission or receipt alone changes required root/slot proof, accepted knowledge, positive applicability, Action eligibility or resume. Authentication can be PROVED while the delivered proposition remains unvalidated. Exact current consumer/gate correspondence must be tested; an arbitrary consumer predicate referencing bare evidence availability is not a receipt proof.

## Native lifecycle, not new success flags

| From | Operation | To | Meaning |
|---|---|---|---|
| WAITING | authenticated source admission candidate | PRIVATE_ADMITTED | New evidence entity+ReceiptAdmission; no observation/proof or gate-stage change |
| PRIVATE_ADMITTED | existing ExternalEvent EVIDENCE_RECEIVED | RECEIVED | Set pending entity/history only; both ledger entries atomically durable before return |
| RECEIVED | existing ExternalEvent EVIDENCE_VALIDATED, accepted and all obligations PROVED | VALIDATED | ReceiptObservation accepted; C03 still requires accepted reentry lineage and eligibility |
| RECEIVED | validation rejected or obligations not all PROVED | WAITING | Native observation outcome preserved; no forced new enum; valid DISPROVED claim may have accepted observation but gate returns waiting |
| VALIDATED | existing DEPENDENT_ACTION_REENTRY then recompute | REENTRY_ELIGIBLE_OR_BLOCKED | All C03 pins/currentness/lineage and named prerequisites independently tested |
| ANY_COMMITTED | SourceInvalidation | STALE_DEPENDENTS | Native recomputation and replay; no in-memory-only validity |

EVIDENCE_ACCEPTED/EVIDENCE_REJECTED are explanatory outcomes, not newly introduced native ExternalStage enums. Native validation records ReceiptObservation; if all obligations are not PROVED, gate stage returns to WAITING_FOR_EXTERNAL_EVIDENCE. A validly authenticated negative claim can have `observation.accepted=true` but still not complete the gate. An invalid receipt has a rejected observation with no accepted claims. Preserve this distinction rather than treating every return to waiting as identical rejection.

Received ≠ validated; accepted claims ≠ positive obligations; positive obligations ≠ accepted reentry; accepted reentry ≠ named-action eligibility. C03 still checks source pins, policy/context lineage and the eligible named action. Governed unknown remains unknown: receipt cannot define a missing rule. Its validation cannot supply positive proof until a separately supported rule-admission mechanism exists.

## Replay, source indexes and idempotence

Reuse current canonical snapshot/bundle/event encodings and identity algorithms with an additive registered payload. Old bundles with no new events retain bytes and identities. Unknown event schemas remain fail-closed. No new E2 policy version or permissive bundle scope is silently added.

For bundles containing admission events, enforce a source availability schedule:

- Every admission carries its exact disjoint `source_additions`. No existing pin key may be replaced; no identity-domain alias is accepted.
- Final source table must equal initial source set union all authorized deltas. The initial source set is derived by removing those disjoint additions from the final table; all initial-state provenance must resolve there.
- Replay checks each event using only its prefix source index; a source added at n+1 is unavailable at checkpoint n. Reconstruct the prefix bundle with that source index and verify admission.expected_bundle against its identity. This prevents source additions from retroactively changing historical input.
- Final persisted source pins and event deltas must agree exactly. Contradictory, duplicate or unused unauthorized additions fail. `_replay`, provenance checking and source verification must share this one rule.
- An admission entry must be immediately followed by its exact same-gate/receipt-entity EVIDENCE_RECEIVED event. Published bundles may never end on an unpaired admission. Intermediate state is private; no accepted observations or proofs are inserted there.

The event identity continues binding sequence, prior snapshot/event, payload and resulting snapshot. Admission additionally binds its exact prior bundle/source context through expected_bundle. The original checkpoint and old event files remain immutable. This is monotonic history extension, not backdating evidence into initial state.

The canonical command key includes exact parent plus gate/receipt/source/contract identities and normalized request body. Exact retries return the stored original committed result without appending or rewinding the current head. The response also names the present head; it does not imply the old receipt remains current after later invalidation. Reusing the key with different bytes rejects. Submitting the same old event under a different key does not bypass the expected-parent or active-stage check. A byte-identical entity collision outside the original committed retry is rejected in this bounded API; no implicit cross-gate object reuse or overwrite.

## Atomicity, durability and ordering

v0.1 uses one serialized writer per canonical head. Admission+receipt is one two-entry commit; validate and reentry are later separate commits. Competing commands must compare expected head under the same lock. The winner determines the ledger order; the loser must obtain the new head and be revalidated. This contract guarantees determinism for identical **ordered** command input, not commutativity of different arrival histories. No distributed ordering protocol is required.

Existing `save_bundle` uses temporary-file fsync and immutable link publication. It does not define a multi-file durable head transaction or directory-fsync crash protocol. The bounded package must add that commit boundary rather than claim current fsync already establishes it:

1. Write/hash/verify immutable source blobs, events and bundle in the non-E1 store; fsync each file and affected directories. Conflicting content-addressed names reject; never overwrite.
2. Under the single writer lock, compare the durable head to expected_bundle. Atomically publish a local head record containing the committed bundle identity, transaction key and previous head identity. Fsync the head file and its directory before acknowledgement. Historical events/bundles are still append-only; this small mutable head is a discovery pointer, not semantic or release authority.
3. Consumers use only that committed bundle/pin. On restart, verify the head's canonical bundle and lineage against the trusted prior checkpoint/chain, never select the lexically largest filename or trust a self-consistent attacker replacement. No recovery fallback may repin stale sources.
4. Crash before head publication leaves the old head authoritative; staged orphan files have no semantic effect. Crash after publication recovers the entire new pair. Lost acknowledgement is handled by transaction-key lookup. Fault injection must prove these outcomes at every boundary.

An in-memory candidate is not “accepted” for caller use before commit. Do not run planning/Action execution on it or return a success response while receipt persistence is missing. Validation/reentry commits follow the same rule. Disk failure leaves no acknowledged acceptance; changing a source between validation and commit fails revalidation. External edits after commit are detected by source pins/invalidation, not hidden by caches.

## Fail-closed test specifications

| Case | Input | Deterministic reason/outcome class | Required behavior |
|---|---|---|---|
| T01 | no matching gate | NO_ACTIVE_GATE | No commit; old bundle/head unchanged |
| T02 | wrong proposition/requirement/target | RECEIPT_CORRESPONDENCE | No commit |
| T03 | unexpected source/producer or same hash wrong domain | SOURCE_DOMAIN_OR_PRODUCER | No commit |
| T04 | wrong scope/lineage/generation | ENVELOPE_MISMATCH | No commit |
| T05 | expired/stale evidence or stale attestor | SOURCE_NOT_CURRENT | No commit; later stale invalidation withdraws support |
| T06 | same transaction key and canonical request bytes retried | DUPLICATE_IDENTICAL | Return original committed outcome, no new event; also report current head, do not rewind it |
| T07 | same transaction key with different payload | IDEMPOTENCY_CONFLICT | Reject without overwrite |
| T08 | old live receipt/event against a new head | PARENT_MISMATCH | Reject unless exact previously committed transaction retry |
| T09 | entity/source identity collision with changed bytes/claims | IDENTITY_CONFLICT | Reject; no overwrite/rebinding |
| T10 | conflicting claim outcomes against prior accepted claims for same gate obligation | CLAIM_CONFLICT | Reject receipt admission; preserve prior history. Independent legacy conflicting observations remain UNKNOWN under native rules |
| T11 | malformed bytes/unknown schema/unexplained fields | MALFORMED_RECEIPT | No commit |
| T12 | gate/route source invalidated before receipt | ROUTE_NOT_CURRENT | No commit; recompute native defect/wait semantics |
| T13 | wrong expected bundle/snapshot/event parent | PARENT_MISMATCH | No commit |
| T14 | validly authenticated DISPROVED claim | NOT_POSITIVE_PROOF | May be received; native validation/obligation recompute does not grant positive completion or resume |
| T15 | source invalidated between received and validate | VALIDATION_FAILED | Native negative observation, return to waiting, no reentry |
| T16 | attempt to import authority/predicate/Action via evidence payload | ADMISSION_SCOPE_EXCEEDED | No commit |
| T17 | unknown rule with valid route and evidence | RULE_STILL_UNKNOWN | Receipt cannot set rule_known; native validation cannot prove unknown obligation |
| T18 | commit/crash at any write boundary | ATOMIC_RECOVERY | Old or full new committed bundle; never admission-only committed state |
| T19 | concurrent requests with same parent | SERIALIZATION_CONFLICT | Only first serialized commit succeeds; second must revalidate against new head |
| T20 | source deleted/substituted after commit before cold restore | PIN_FAILURE | Restore rejects; no cached bytes used to silently repin |

Ingress rejects structurally malformed or unauthorized delivery without a canonical success event. Independently admitted but substantively negative evidence can proceed to the existing validation stage. Later invalidation must stale support across cold replay. The new admission provenance and authority references must integrate with `invalidate_sources` and native receipt rechecks; tests must not repair validity with dataclass replacement.

## Bounded implementation package — E2-T01

**Not executed.** Scope is one native source-admission event, its typed ingress contract, two-event atomic receipt API, source-index replay schedule, durable commit/idempotence support and focused qualification.

| Module | Required bounded work |
|---|---|
| model.py | Closed EvidenceSourceAdmission payload and typed ingress contract validation; explicit identities/provenance; extend ExecutionEvent union. No arbitrary patches or authority imports. |
| gates.py | Reuse native source/authority/receipt primitives; add scoped ingress preconditions without replacing proposition validation. |
| core.py | Pure bounded admission transition and existing receipt dispatch; no direct proof/resume or rule-known setters. |
| codec.py | Registered wire types; prefix source-index validation, parent bundle binding, pair completeness, immutable atomic commit/recovery and idempotence. Preserve old encodings. |
| __main__.py | One admission command using the shared transaction API with explicit parent pin/source inputs/output store; existing apply cannot bypass pairing. |
| tests | Independent synthetic contract fixtures, mutation/fault injection, cold-process replay, current regression suites; no E1 mutation. |

Before implementation, pin independent source-shaped fixture bytes, pre-state ingress/trust contract, field selectors and expected admissions/rejections. The JSON test specifications are not executable runtime fixtures and do not assert PASS. The package must demonstrate: absent evidence at cold checkpoint; admission+receipt exactly once; source-index temporal consistency; independent validate/reentry; stale withdrawal; source/authority/scope/lineage rejection; tampering and crash recovery; deterministic independent processes; continued C03 checks. Preserve A–N, X01–X11, C01–C06/refined C06, C06A budget, external-unknown repair, CLI/importer, constructors, cold persistence, append-only replay, selection and all native controls. No existing closed finding is waived.

No E2 Action must execute merely to test source admission. The package may use bounded synthetic test states; full E2 progression remains P02–P06. Acceptance requires all new tests and affected full baseline pass, no E1 changes or production effects, and diff hygiene. Do not call the package complete just because a unit helper can insert evidence.

## E2 impact and reentry gate

Direct lifecycle dependencies: **E2-A09, E2-A10, E2-A11, E2-A12, E2-A13, E2-N04, E2-N14, E2-N15, E2-END**. Additional transaction-specific variants or downstream qualification dependencies: **E2-A15, E2-N03, E2-N05, E2-N11, E2-D01, E2-REVIEW**. N03/N05/N11 have initial-state variants independent of ingress but also require live-transaction lineage/source/persistence mutants. A15 requires post-receipt evidence invalidation as well as independently seeded knowledge/authority/proof invalidation. D01 and REVIEW depend on the final transaction implementation. This does not make all other missing E2 fixtures executable.

E2-G02–G07 remain: six complete O01/native Actions; complete concrete source roles/policy; root/slot/authority/dossier contracts; exact external route and expected absence; independent full-state oracles/negative fixtures; complete checkpoint/cold-process harness. G08 records integrated-case/downstream evidence dependencies, not a demand that P02 run before P01. No existing P01 count or historical result is rewritten.

```text
E2_P01_RETRY_ALLOWED =
  transaction contract has independently executable qualification fixtures
  AND bounded implementation is accepted against the native persistence/receipt contracts
  AND remaining P01 fixture/contract blockers are resolved
  AND no unresolved cross-contract conflict
```

This predicate is currently false. Defining this transaction is not executing it, making it durable, or proving its compatibility with a complete E2 fixture. E2-P02 still requires P01 PASS. N-REAL remains an independent real-E1 assurance gate, unaffected by this synthetic runtime addition.

## Report

```text
CURRENT_LIVE_INPUT_INTERFACES = [SuppliedResult, RecordedDecision, DecisionReentry, ExternalEvent, SourceInvalidation via record_result/append_event; CLI apply]
REQUIRED_TRANSACTION = restored waiting prefix -> bounded evidence admission -> existing receipt -> atomic durable two-event commit
EVENT_TYPE_CLASSIFICATION = NEW_EVENT_TYPE_REQUIRED
TRANSACTION_STATE_MACHINE = WAITING -> RECEIVED -> separate native validation outcome -> reentry evaluation
ATOMICITY = admission+receipt pair; validation and reentry separate
DURABILITY = verified immutable files + fsync + last atomic trusted-head publication
IDEMPOTENCE = exact committed request retry returns original outcome without append
REPLAY_SEMANTICS = sequence/parents/source-prefix reconstruction; no historical rewrite
ORDERING = single serialized writer, compare expected head
FAIL_CLOSED_CASES = [T01..T20]
CLASSIFICATION = MISSING_RUNTIME_CAPABILITY
IMPLEMENTATION_PACKAGE_REQUIRED = YES
IMPLEMENTATION_PACKAGE = E2-T01 (specified, not executed)
E2_CASES_BLOCKED = ["E2-A09", "E2-A10", "E2-A11", "E2-A12", "E2-A13", "E2-N04", "E2-N14", "E2-N15", "E2-END", "E2-A15", "E2-N03", "E2-N05", "E2-N11", "E2-D01", "E2-REVIEW"]
OTHER_E2_P01_BLOCKERS = [E2-G02,E2-G03,E2-G04,E2-G05,E2-G06,E2-G07,E2-G08]
E2_P01_RETRY_ALLOWED = NO
E2_P02_READY = NO
N_REAL_SATISFIED = NO
CANONICAL_E2_QUALIFIED = NO
PLANNER_V0_1_REQUALIFICATION_READY = NO
V0_1_CURRENT_STATUS = CORRECTION_REQUIRED
IMPLEMENTATION_MODIFIED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
```

Preservation validation is recorded in the companion: all pre-existing implementation/tests/plans/backlog files and all 10,911 frozen E1 paths/content hashes compared with the pre-write inventory; `git diff --check` passes. No runtime tests, experiment Actions, authority issuance, E1 requests or migration were executed. Only these two new reconciliation artifacts are produced.
