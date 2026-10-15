# REENTRY-R02 — computed obligation proof and C03 closure

RESULT = PARTIAL. The computed-result model is recovered. Event-free completion of canonical A11 is not supported.

The [canonical matrix](DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_ACCEPTANCE_MATRIX_1.md), lines 145–157, explicitly requires **DEPENDENT_ACTION_REENTRY event and resume_eligibility with source root**. R01 preserves that requirement. Proof and ResumeEligibility are computed results, but their being computed does not eliminate the accepted reentry-event prerequisite. No new combined Proof/eligibility event is required or defined.

## Native model

`gates.Proof(state, reasons)` is a typed computed value over admitted state. It has no ArtifactIdentity. `obligation_proof` admits the model and evaluates the exact EvidenceRequirement. It requires known rule/current matching validation, independently checked accepted receipt and a unique claim outcome for the exact obligation. No outcome gives UNKNOWN; conflicting outcomes give UNKNOWN. Validation/support records are not Proof values. Consumers include external_complete and C03; query results from another state cannot substitute for recomputation.

The sealed obligation is E2-EXTERNAL-REQUIREMENT: “Authenticated governing rule for target operation; no rule currently received”, with its exact TEST-target and TEST-rule-owner producer bindings. V02 defines the actual accepted validation/current support prerequisites. Semantic Evidence, native Evidence, content, receipt, ValidationResult, support and source identity domains remain distinct. No new standalone Proof entity or prospective result is needed.

`ResumeEligibility(allowed, actions, reasons, supporting_identities)` is a separate computed return value, not a field of native Computation. It has no stable ArtifactIdentity. Model.py:1218 explicitly says “Derived proof, never a persisted permission Boolean.” A comparison report may serialize its value, but cannot become canonical permission. Persist authoritative inputs, events and bindings; restore/replay and recompute the result.

C03 requires the external gate's reentry stage, qualified complete receipt contract, every obligation PROVED, accepted named reentry event with exact resume binding, current context, named Action in native actionable set and no failing overlapping external/decision route. Source_root must be provided and all source/policy bytes independently verified. Its supporting identities reference the accepted event, parent snapshot, policy/scope binding and source pins. Existing operating Action/ATTEST/decision authority must pass its own native checks. Eligibility is neither authority, selection nor execution and may disappear on changed inputs.

## State and boundary

The pure queries `obligation_proof`, `core.recompute` and `resume_eligibility` leave canonical state and append head unchanged. However full A11 must append the existing ordinary DEPENDENT_ACTION_REENTRY event. A required DecisionReentry remains a separate event if the recorded-decision route requires it. The current canonical state has neither accepted A11 event nor received/validated lifecycle inputs. Post-A10 can have PROVED obligation support while C03 remains false. Native C03 emits REENTRY_STAGE_REQUIRED and ACCEPTED_REENTRY_EVENT_MISSING until the required event exists.

Therefore PRE_STATE_ID == POST_QUERY_STATE_ID is correct for computation; PRE_A11_STATE_ID == POST_COMPLETE_A11_STATE_ID is not the canonical phase contract. No state change was performed here. No eligibility Boolean or Proof result was persisted. The accepted event records reentry history, not an epistemic result or Action completion.

A12 begins only after current named eligibility is established: exact accepted/current Evidence and validation/support, PROVED obligations, accepted reentry ancestry, matching policy/context/source bindings and all other prerequisites. Ordinary recomputation must still pass immediately before deterministic selection. E2-REENTER is not executed by A11; accepted result inventory and A12 Action execution remain separate requirements. Root/slot proof and FINISH completion are not produced.

## Definitions and authority

The requirement/proposition, E2-GATE named reentry list, native C03 function, typed Proof and ResumeEligibility models and ExternalEvent already exist. A09 supplies Evidence/receipt; A10 supplies ValidationResult/support/accepted observation. The accepted reentry event is an A11 lifecycle prerequisite, not an installed definition. No additional canonical computation definition set is established by these artifacts, so no typed adapter or new INSTALL grant is required for this native path. Prior grants are not broadened.

P04_A11_INSTALLATION_DECISION_REQUIRED = NO. P04_A11_INSTALLATION_DECISION_READY = NO (not applicable: no exact installable subject). AUTHORIZE_P04_A11_COMPUTATION_DEFINITIONS and DECLINE_P04_A11_COMPUTATION_DEFINITIONS are recorded as conditional, unselected labels; they cannot authorize installation of computed results or remove the canonical event requirement. No definition IDs/content IDs are invented for a nonexistent set.

The companion gives the complete input classifications, proof/C03 contracts, independent boundary oracles and negative plan. Fail-closed cases include missing/wrong/stale validation/support/source/proposition/authority/context, wrong named route, missing reentry event, changed binding, caller eligibility Boolean, stale-state Proof/eligibility and A11 attempting REENTER execution. Source/validation/support/authority/context invalidation must be reflected by current native recomputation; historical records remain auditable.

## Qualification limits and preservation

Four independent fresh processes with hash seeds 0,1,7,101 natively restored and replayed the exact post-A10-install configuration bundle, then computed Proof, ResumeEligibility and Computation. Full native output/state identities matched, canonical bundle bytes remained unchanged, and eligibility was false with missing accepted reentry ancestry. These checks qualify only the current pre-receipt checkpoint. They do not qualify positive post-A10/A11 behavior, invalidation fixtures or unordered permutations. No A09–A12 transition was simulated or executed.

A11_IMPLEMENTATION_READY = NO for the requested event-free closure. The next package is bounded qualification of the existing native A11 reentry-event/C03 path on isolated post-A10 simulation, retaining computed results. A new durable combined event is neither needed nor authorized.

A09_READY = YES; A10_READY = YES; A11_READY = NO; P04_EXECUTION_READY = NO. A09/A10/A12_EXECUTED = NO; A11_STATE_MUTATION = NO performed; PROOF_RESULT_PERSISTED = NO; RESUME_ELIGIBILITY_PERSISTED = NO. P03_RESULT = PASS; historical correspondence = UNPROVEN; N_REAL_SATISFIED = NO; RUNTIME_MODIFIED = NO; E1_ARTIFACTS_MODIFIED = 0; PRODUCTION_EFFECT = NO.

Preservation hashes and git diff --check results are in the [machine-readable companion](DETERMINISTIC_PLANNER_V0_1_REENTRY_R02_A11_COMPUTATION_CONTRACT.json).
