# E2 Human-Handoff State-Identity Divergence Analysis

## Finding

The CHECK and COLLECT post-state identities reproduce exactly:

```text
initial   545ad19184d8dd7dfb5b2737e081b043d13982f05d05326939ac2cbb89bf54e2
CHECK     e381424d14336d918fd3bafff16698361395c77ef03fef628d7d74d36af8a9da
COLLECT   6c7efb221870974d76d12d7ceb372369ef68104bb1f522a16d47f7dc37236677
```

The first divergence is therefore at `POST_DOSSIER_BINDING` (the PREPARE
materialization/admission boundary). The qualified result records `391140…`,
but does not preserve its complete native state or its materialization inputs.
The independent reconstruction produced `996d1f…` after supplying the
missing canonical predicate definitions needed to admit the six validation
instances.

## Identity algorithm

Both identities use the same native algorithm when computed by the current
codec: `snapshot_id(snapshot)` validates the model, serializes
`{"schema":"PLANNER-SNAPSHOT-1","snapshot":...}` as UTF-8 JSON with sorted
object keys, compact separators and enum/dataclass type tags, then hashes the
exact bytes with SHA-256 in the `planner-snapshot-v1` content-identity domain.
Collections retain their canonical tuple order; object-key insertion order is
removed by JSON canonicalization. The algorithm excludes no semantic Snapshot
field except fields absent under the codec's versioned-default rules. No
timestamp, UUID, process address or random value is used by the codec.

The algorithm matches. The complete left-hand input does not.

## Structural comparison

| Component | Comparison |
|---|---|
| Actions/statuses | IDENTICAL through CHECK/COLLECT; handoff left state unavailable beyond trace summary |
| Prerequisites | IDENTICAL for the recoverable action model |
| Actual results/knowledge | CHECK/COLLECT IDENTICAL; PREPARE result recorded as PASS on both, complete left payload unavailable |
| DecisionDossier | Same declared identity `6a5073…`; left canonical object bytes unavailable |
| `prepared_dossier` binding | RIGHT reconstructed; LEFT only asserted by T02 result |
| Fact proofs | 2/2 asserted by T02; complete left proof representation unavailable |
| ValidationInstances | 6/6 asserted by T02; right instances required added predicate definitions; left definitions/provenance unavailable |
| Roots/slots/authority/evidence | No semantic change shown; complete left representation unavailable |
| Source validity/provenance | Right reconstructed from fixture sources; left post-T02 provenance not retained |
| Decision readiness/control | Observable equality: E2-DECIDE actionable, HUMAN_HANDOFF |
| Event/ledger position | T02 reports `events_admitted=0`; no canonical post-T02 event artifact exists |

The only supported concrete value difference is the resulting state identity;
the exact first differing field cannot be proven because the complete 391 state
was never emitted.

## Event and ephemeral-state analysis

Retry 3 records the three prefix transitions and their identities. T02 records
the same prefix plus a direct `admit_dossier_materialization` transaction, but
does not emit a replayable event containing the dossier, validation predicate
definitions, validation instances and their provenance. The original 391
identity is therefore a trace/result identity from an in-memory native state,
not a recoverable serialized handoff artifact. The replay's 996 identity is a
native codec identity of a newly reconstructed state, not an equivalent replay
of the original post-T02 state.

The missing post-T02 materialization payload is `SHOULD_BE_PERSISTED`, not
legitimately ephemeral. The handoff identity cannot depend on it being hidden
in process memory.

No nondeterministic identity input was found. The divergence is a
representation/persistence gap, not a hash-seed or ordering defect.

## Semantic equality and authority

The observable semantics are compatible: both states are reported as the same
DecisionDossier-admitted HUMAN_HANDOFF with E2-DECIDE actionable and no
decision, choice evidence or grant. Full semantic equality is `UNPROVABLE`
because the complete 391 state is missing.

```text
391140_AUTHORITY_CLASS = T02_RESULT_RECORDED_IN_MEMORY_NATIVE_STATE_IDENTITY
996D1F_AUTHORITY_CLASS = CURRENT_NATIVE_REPLAY_RECONSTRUCTION_CODEC_IDENTITY
391140_AUTHORITATIVE = NO
996D1F_AUTHORITATIVE = NO
```

Neither identity can safely serve as the human-choice pre-state.

## Classification and correction

```text
CLASSIFICATION = COMBINED
  - PERSISTENCE_DEFECT: post-T02 state was not emitted as a replayable artifact
  - TRACE_ARTIFACT_DEFECT: 391140 is recorded without complete state inputs
  - QUALIFICATION_RECORD_DEFECT: T02 identity evidence is not independently recoverable
```

Minimum correction, not applied here: emit the exact native post-T02
`PLANNER-SNAPSHOT-1` bytes plus the canonical materialization/event inputs
(prepared dossier, six validation predicate definitions and instances, fact
proof state, provenance and ordering), decode them in a fresh process, and
require the resulting identity to equal the recorded execution identity.
Only that emitted artifact may become the human-choice pre-state.

## Qualification and human-choice impact

Semantic T02 evidence, the CHECK/COLLECT/PREPARE prefix, dossier admission,
T03 protocol and the explicit human intent are preserved. T02 post-state
identity, persistence and cold-restore evidence are invalidated until the
artifact is emitted. P02 Retry 3 remains partial and cannot resume.

`HUMAN_CHOICE_RECONFIRMATION_REQUIRED = UNRESOLVED`: the decision subject,
dossier, options, scope and lineage are preserved in the available records,
but the required exact pre-state binding is not.

```text
HUMAN_DECISION_CAPTURE_RETRY_ALLOWED = NO
E2_P02_RETRY_ALLOWED = NO
E2_P03_READY = NO
SELECTED_HUMAN_OPTION = ALLOW_QUALIFICATION_MAPPING
CHOICE_EVIDENCE_CREATED = NO
RECORDED_DECISION_CREATED = NO
AUTHORITY_ISSUED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
```
