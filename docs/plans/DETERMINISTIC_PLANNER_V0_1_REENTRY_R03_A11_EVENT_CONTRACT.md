# REENTRY-R03 — native A11 reentry event contract

RESULT = PARTIAL. Native event semantics are recovered. No A11 event was admitted. Positive P04 event/C03, retry and storage-failure qualification remains outstanding.

## Occurrence, proof and authority

DEPENDENT_ACTION_REENTRY records the qualified external gate accepting its transition from EVIDENCE_VALIDATED to its declared dependent-action reentry stage after all independent obligations hold, reopening only its named noncompleted Actions for ordinary recomputation. It records neither Action execution nor a persisted permission.

The canonical matrix, E2-A11 (lines 145–157), requires this event followed by resume_eligibility with source_root. Native core.apply_receipt (577–627) validates the model, exact expected snapshot, known gate, legal predecessor, accepted gate qualification, artifact absent and every current independent obligation via _external_complete_admitted. The Proof is a computed precondition/admission oracle, not an event operand or stable identity. Its inputs are recomputed from the exact admitted pre-state; a cached Proof cannot bypass that check.

There is **no separate event-operating authority operand or grant** on ExternalEvent. Authentication and current support are inherited from admitted receipt/proof premises. Action authority is independently checked by blockers/actionability and C03; accepting the event does not grant or consume it. Therefore wrong Action authority may permit this historical gate transition while still making C03 false. Requiring event rejection for a nonexistent authority operand would invent semantics. No new human event-authority decision or installation grant is required by the recovered native path.

## Event identity and state

Payload: ExternalEvent(gate=E2-GATE, stage=DEPENDENT_ACTION_REENTRY, expected_snapshot=exact current snapshot, artifact=None). codec.record_result wraps it in ExecutionEvent with sequence, exact pre-state, ordinary current parent event, resulting snapshot identity and resume_binding. The event identity is planner-event-v1 SHA256 over native canonical bytes of sequence, parent, parent_event, typed result, after, and resume_binding when present. The binding separately hashes exact policy pin/version and bundle.scope. No command key, Proof ID, authority or new provenance field is added. Scope/lineage/generation and existing provenance are bound through complete state and its native premises.

The transition advances gate.stage and its ordered history. Only noncompleted Actions in gate.reentry are assigned native ACTION_ELIGIBLE; actual actionability remains the conjunction of all prerequisites. Knowledge, stored root/slot and authority records are unchanged. The event envelope appends history and advances canonical state/head. Proof and ResumeEligibility remain computed. No ActionResult or E2-K-REENTER output is created, and REENTER does not complete.

For P04, native append/replay must verify the current ordinary parent, exact pre-state, sequence, identity and post-state. A foreign or stale envelope fails these checks. DecisionReentry is a separate native event if the existing decision route requires downstream reevaluation; it must not be silently merged into ExternalEvent.

## C03 and A12

C03 requires current obligation PROVED, qualified complete gate, accepted reentry stage/event, exact event resume binding, current context, named E2-REENTER in recompute.actionable and no failed overlapping route. Source_root must verify all source/policy bytes. Its typed result is current eligibility evidence, not authority or a persistent permission token.

Positive A11 terminal state comprises post-A10 authoritative receipt/validation/support plus the accepted native reentry event(s). Fresh Proof and C03 must pass with only the intended named Action eligible. A12 is not performed; ACTION_COMPLETED(E2-REENTER) is false; root/slot Proof instances remain absent and FINISH is not completed. A12 consumes the event-bearing canonical state and freshly recomputed readiness/eligibility before selection and independently permitted result admission.

After validation/support/source/authority invalidation, loss of proof qualification, changed context or policy binding, current eligibility must fail where its premises fail. Historical reentry events remain immutable/auditable. An old accepted event alone is never sufficient. Replay reconstructs historical state transitions; current C03 queries verify current source bytes and gates.

## Admission, retry and persistence

Native record_result/append_event construct and replay-check a complete immutable bundle or raise. The input remains unchanged on semantic failure. append_event accepts exact identical event identity and bytes idempotently; conflicting bytes under that identity fail closed. A fresh record_result retry after acceptance instead fails its obsolete pre-state or illegal repeated stage. ExternalEvent has no command_key, so this is not a claimed general command-key transaction contract.

save_bundle writes immutable fsynced event sidecars and the canonical bundle. An interruption may leave unreferenced sidecars; it does not imply a published valid new bundle. The recovered path has no dedicated reentry command/CAS/HEAD transaction. No storage-failure injection was performed, and stronger durable retry/HEAD guarantees are not claimed. Restore verifies canonical bytes, source pins and event sidecars. Replay verifies every ordered parent/pre/post identity exactly once; it does not serialize Proof or ResumeEligibility.

## Prospective definitions and readiness

The exact E2-GATE named reentry list, E2-EXTERNAL-REQUIREMENT, native ExternalEvent, C03 function and existing authority references are already represented/available. No missing installable A11 definition set is identified. Event instances, Proof results and ResumeEligibility are not prospective definitions. No adapter, definition/content identities or bounded INSTALL grant is fabricated. Existing route/ATTEST/A10 grants remain bounded.

P04_A11_DEFINITION_INSTALLATION_DECISION_REQUIRED = NO; decision ready = NO (not applicable). P04_A11_EVENT_AUTHORITY_DECISION_REQUIRED = NO; decision ready = NO (not applicable). AUTHORIZE_P04_A11_REENTRY_DEFINITIONS / DECLINE_P04_A11_REENTRY_DEFINITIONS are conditional labels only until an actual missing sealed set exists. No option was selected.

The companion defines the negatives at their actual boundaries: proof/input rejection, stale/foreign envelopes, unsupported payloads, current authority/C03 failures, substitution of Boolean permission, and historical event reliance after premise withdrawal. These are contract oracles, not executed test results. A11_EVENT_IMPLEMENTATION_READY = NO under the requested full acceptance gate because positive P04 precommit, decision-route applicability and retry/storage qualification are still outstanding; the ordinary native event implementation itself exists.

## Preservation

The exact post-A10-install configuration bundle was natively restored and replayed read-only. No A09–A11 or A12 transition occurred. A09_READY = YES; A10_READY = YES; A11_READY = NO; P04_EXECUTION_READY = NO. A11_EVENT_ADMITTED = NO; PROOF_RESULT_PERSISTED = NO; RESUME_ELIGIBILITY_PERSISTED = NO. P03_RESULT = PASS; historical correspondence = UNPROVEN; N_REAL_SATISFIED = NO; RUNTIME_MODIFIED = NO; E1_ARTIFACTS_MODIFIED = 0; PRODUCTION_EFFECT = NO.

The [machine-readable companion](DETERMINISTIC_PLANNER_V0_1_REENTRY_R03_A11_EVENT_CONTRACT.json) contains exact source/hash references, native identity fields, authority mapping, negative suite and preservation checks. Next work is isolated native A11 event/C03 precommit qualification against simulated post-A10 inputs, preserving canonical P04 until execution is separately authorized.
