# REENTRY-R01 — canonical proof and named C03 boundary

RESULT = PARTIAL. The A11/A12 ownership conflict is resolved; a new persisted Proof-plus-eligibility transaction is not established by the authoritative contracts.

A11 consumes validated supporting Evidence, verifies typed obligation proofs and establishes named C03 eligibility. A12 starts with that eligibility and owns actual REENTER selection/result. This preserves the canonical matrix, E2-A11 and E2-A12, and the plan's RECEIVED → VALIDATED → REENTRY separation. It does not require moving eligibility into A12.

The distinction that remains is representation. Native `gates.Proof` is a typed computed result. `ResumeEligibility` is explicitly a “Derived proof, never a persisted permission Boolean” (model.py:1218). C03 recomputes from replayed persisted inputs and independently loaded source bytes. The canonical contract does not prescribe a new durable EvidenceProof instance, eligibility instance or combined event. Claiming those already exist would change semantics rather than reconcile ownership.

## Canonical proof and eligibility

The exact current requirement is `E2-EXTERNAL-REQUIREMENT`, proposition “Authenticated governing rule for target operation; no rule currently received”, target canonical TEST-target identity and permitted TEST-rule-owner producer. The wording is the sealed authored proposition, not a generic TRUE assertion. The native proof rule requires known rule/current matching validation, accepted independently authenticated receipt and exactly one outcome for the exact requirement. No outcomes or conflicting outcomes yield UNKNOWN. V02's accepted ValidationResult/support and native observation are persisted inputs; the typed proof query remains distinct from those inputs.

Named reentry is `E2-GATE.reentry=(E2-REENTER)`. C03 is a composed, current, non-effecting eligibility proof, not a standalone PredicateId. It requires the accepted DEPENDENT_ACTION_REENTRY stage/event, every obligation PROVED, exact event resume binding to current policy/context, all other named Action prerequisites, native actionability and independently verified source/policy pins. A failing overlapping external or decision route can forbid the Action. DecisionReentry remains a separate native transition where its current recorded-decision route requires it; it must not be silently omitted or merged.

C03 returns typed `ResumeEligibility(allowed, actions, reasons, supporting_identities)`. Its deterministic sorted support includes event/pre-state, resume binding and verified source/policy identities. It has no native ArtifactIdentity. A report digest could identify a comparison artifact but cannot become permission. Currentness is recomputed before A12; historical eligibility evidence cannot authorize changed inputs.

## Composition, events and failure

Canonical A11 checks typed proof, appends the ordinary native reentry event(s), then checks C03 on the resulting bundle with source_root. Each append is atomic under existing native persistence. The matrix requires before/after identities and trace; it does not require a single atomic Proof+eligibility commit. Valid proof with C03 false is persistable: post-A10/pre-A11 already has this distinction. Proof failure blocks the external reentry operation. A successfully appended reentry event with failed C03 does not satisfy A11's exit and cannot permit A12.

The native ExternalEvent supplies gate, stage and expected snapshot; its ExecutionEvent wrapper binds ordinary parent, sequence, pre/post-state and resume binding. Proof, ValidationResult and support are consumed through canonical state references, not new event operands. The requested new event with explicit Proof and eligibility objects therefore needs a separate complete contract if still desired. No retrospective proof admission or persisted permission is inferred.

Positive A11 exit requires accepted validation/current support, all exact typed obligation proofs PROVED, accepted named reentry ancestry, C03 permission for only the intended Action, current source/policy/context/other prerequisites, and no REENTER execution. REENTER completion remains false; root/slot proof instances remain absent; FINISH is not completed. A12 may assume that boundary but must use ordinary recomputation before selection. Its result inventory must independently be complete; A11 does not manufacture an ActionResult.

Evidence, validation, support, proof qualification, source or authority invalidation withdraws proof and/or eligibility. Scope/lineage/generation or policy changes invalidate bindings. Historical records remain auditable. Cold restore and replay preserve receipt, A10 result/support and reentry event ancestry; proof and C03 are derived again without a new validation decision.

## P01 reuse and installation

P01's typed proposition, exact identity domains, independent validation/support, current source/context, fail-closed dependency checks and separation from Action execution remain supported. Its proof-only A11 boundary is rejected. A new durable EvidenceProof/event and a single combined transaction are compatible design possibilities, not canonical requirements. Persisting allowed=true as permission conflicts with C03.

The requirement, gate/named reentry definitions, native Proof query, ExternalEvent and ResumeEligibility representation already exist. No newly required A11 installation set has been identified. Their actual lifecycle outputs are not prospective definitions. The companion classifies every requested prospective object and all P01 elements. No typed adapter or exact new content identities are invented for a set the canonical contract does not require.

A new set, if separately specified, would need its own bounded INSTALL grant for exact IDs/content, operation, current bundle/state/parent, scope/lineage/generation/consumer, validity and provenance. Route, ATTEST and A10 grants do not apply. The requested AUTHORIZE_P04_A11_REENTRY_INSTALLATION / DECLINE_P04_A11_REENTRY_INSTALLATION options are recorded without selection, but are not decision-ready until there is an exact sealed installable subject. Existing canonical operation needs operating applicability checks, not a duplicate definition installation grant.

A11_IMPLEMENTATION_READY = NO for the requested new persisted composite. The existing native path is available, but its exact positive P04 composition/currentness qualification is still pending. A11_READY = NO. P04_A11_INSTALLATION_DECISION_READY = NO. This report does not claim adapter, negative suite or execution qualification PASS. The complete negative plan is in the companion.

## Verification and preservation

The exact post-A10-install bundle was natively restored and replayed read-only. Source pins, canonical bytes and event sidecars passed native restore. No A09–A12 transition or Proof/eligibility instance was created. No runtime or prior artifact was changed.

A09_READY = YES; A10_READY = YES; A11_READY = NO; P04_EXECUTION_READY = NO. P03_RESULT = PASS; historical correspondence = UNPROVEN; N_REAL_SATISFIED = NO; E1_ARTIFACTS_MODIFIED = 0; PRODUCTION_EFFECT = NO.

Exact source citations, input hashes, object mapping, transaction distinctions, authority template, negative suite and preservation checks are in the [machine-readable companion](DETERMINISTIC_PLANNER_V0_1_REENTRY_R01_A11_CONTRACT.json).
