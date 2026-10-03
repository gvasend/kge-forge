# E2-P02 Decision / Authority Materialization Closure

## Result

`E2-P02-DECISION-AUTHORITY-MATERIALIZATION-CLOSURE = BLOCKED`.

Retry 3 reaches the qualified `HUMAN_HANDOFF` state after dossier admission.
The native decision admission path exists (`apply_recorded_decision`), but the
pinned canonical snapshot contains no authenticated authority entity/predicate,
recorded decision, issuer binding, or pinned choice knowledge with which to call
it. The PC02 fixture is qualification metadata and an applicability oracle; it
does not materialize those runtime objects.

## Recovered contract

`E2-DECIDE` is an `ARCHITECT_CONTRACT_DECISION` for subject `E2-DECIDE`. Its
authoritative dossier is `6a507317bc9cc323fbaa626e97b5954cf3ad934b0bd92d9dc96bd4f63e07bddb`,
with options `ALLOW_QUALIFICATION_MAPPING` and `DECLINE`, scope
`E2-QUALIFICATION-ONLY`, and lineage `E2-CANONICAL-BASELINE-1`. The decision
must be admitted as an authenticated recorded decision; it cannot be selected
or completed autonomously.

The qualified authority fixture defines the intended authority shape:
`E2-GRANT`, `AUTHORITY_IDENTITY`, permission `USE`, target `E2-REENTER`, the
same scope/lineage, and applicability requiring the exact choice, target,
permission, scope, and current independent predicate. It does not provide a
native authority entity, authority predicate, issuer/owner admission record, or
choice-evidence knowledge in the pinned snapshot.

The intended input class is `PREAUTHORIZED_SYNTHETIC_QUALIFICATION_DECISION`,
but the selected option and independently pinned record are still undefined.
No option was selected in this closure.

## Native path and closure boundary

The existing `apply_recorded_decision` path requires, and fail-closes without:

- an `AUTHORITY` predicate bound to an authority entity and the dossier;
- an authority entity with the decision subject, choice, permission, and
  current provenance;
- an authenticated `RecordedDecision` with exact scope and lineage;
- accepted `decision-choice:E2-DECIDE` knowledge matching the record.

Therefore:

- authority admission: `MATERIALIZER_OMISSION` (fixture metadata has no native
  admitted authority object);
- decision admission: `EXISTING_SUPPORTED_PATH` (the native path is present,
  but its required inputs are absent);
- implementation package: **not established**.

The required next closure is a bounded fixture/materialization package that
pins issuer, selected option, authority entity/predicate, record identity,
choice evidence, and provenance, then admits them through the existing native
interface. It must not mark `E2-DECIDE` complete directly.

Negative cases remain fail-closed: missing authority, non-applicable authority,
wrong subject/dossier/option/scope/lineage, stale authority or dossier,
duplicate/conflicting decision, and unauthorized issuer all reject.

## Gates

`E2_P02_RETRY_ALLOWED=NO` because the required authority and decision inputs are
not complete. `E2_P03_READY=NO`. The qualified prefix and HUMAN_HANDOFF replay
remain preserved; no additional Action or decision event was executed.

`N_REAL_SATISFIED=NO`, `CANONICAL_E2_QUALIFIED=NO`,
`PLANNER_V0_1_REQUALIFICATION_READY=NO`.

`IMPLEMENTATION_MODIFIED=NO`, `E1_ARTIFACTS_MODIFIED=0`, and
`PRODUCTION_EFFECT=NO`.
