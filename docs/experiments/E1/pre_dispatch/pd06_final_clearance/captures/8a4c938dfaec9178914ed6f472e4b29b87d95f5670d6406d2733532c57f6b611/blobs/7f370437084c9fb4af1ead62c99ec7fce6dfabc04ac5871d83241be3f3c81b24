# Experiment 1 — Architecture Readiness Review

Decision: **READY — architectural baseline E1-ARCH-1 established.**

Date: 2026-09-10. Authority: Architect, as explicitly delegated in elicitation Q2
and the current instruction to formulate, review, and reconcile Experiment 1.

This decision establishes the logical architecture as sufficiently complete to
govern bounded implementation planning. It does not assert implemented capability,
passing runtime tests, experimental success, or human acceptance. No implementation
work package is issued by this review.

## 1. Reviewed basis

- [Authoritative Vision](VISION.md).
- [Human elicitation and clarifications](ARCHITECTURE_ELICITATION.md).
- [Requirements and acceptance obligations](EXPERIMENT_1_REQUIREMENTS_SYNTHESIS.md).
- [Architecture Gap Analysis](ARCHITECTURE_GAP_ANALYSIS.md).
- [Reconciled architecture E1-ARCH-1](EXPERIMENT_1_ARCHITECTURE.md).
- [Adversarial architecture review E1-AAR-1](EXPERIMENT_1_ADVERSARIAL_ARCHITECTURE_REVIEW.md).
- [Human intervention history](EXPERIMENT_1_HUMAN_INTERVENTIONS.md).

The [baseline manifest](EXPERIMENT_1_BASELINE_MANIFEST.json) records the exact
content identities of this review and its source set. Content changes require an
impact decision and refreshed review/manifest as appropriate; a filename alone
does not identify the reviewed architecture.

The manifest identifies a point-in-time baseline. Preserve that source set in
version-controlled history before dispatch; later live intervention records may
append without rewriting the historical baseline. Such additions require context
freshness/impact assessment, but only material changes to governing intent or
architecture reopen architectural readiness. Future manifests must retain the
relationship to prior source revisions instead of erasing the reviewed history.

## 2. Readiness criteria

| Criterion | Finding | Result |
|---|---|---|
| Human purpose and boundaries are explicit. | New task service; separate colocated repositories; controlled effects; one operator; no additional external destinations; AI-service permission is role-scoped. | PASS |
| Authority and lifecycle are coherent. | Persisted decisions, bounded invocation authority, command identity and single-use recovery approval, separate factual and administrative state. | PASS |
| Durability and supported failure behavior are defined. | Acceptance follows durable state; interrupted writes remain in scope; recovery examines authoritative state; uncertainty is valid and does not permit silent repetition. | PASS |
| Sequential execution can be preserved across interruption. | One process-lifetime execution domain, exclusive owner, no detached task programs; ambiguous ownership blocks new execution. | PASS |
| Context and cross-repository knowledge can govern work. | Mandatory roots, source/dependency manifests, current-state checks, activation of verified source pairs, historical provenance. | PASS |
| Human edits and contradictory evidence cannot silently redefine work. | Stable captured inputs, verified consumed material, impact reconciliation, explicit source conflict and human escalation. | PASS |
| Acceptance is observable and traceable. | All 30 requirements and all 16 acceptance obligations map to architecture responsibilities and review evidence below. | PASS |
| Required adversarial review is complete. | Seven material findings reconciled; crash/authority traces rechecked; review limitations explicit. | PASS |
| Remaining uncertainty has a bounded disposition. | Runtime feasibility assumptions are verification gates with stop/review behavior; deferred scope does not require arbitrary semantics. | PASS |
| No unresolved human intent blocks the selected architecture. | No change to purpose, boundary expansion, or newly required human risk tradeoff was needed. | PASS |

PASS here means an architectural criterion is satisfied by the reviewed design,
not that an executable implementation has passed a test.

## 3. Requirement coverage

Section numbers refer to E1-ARCH-1. Each row identifies the responsibility that
implements the requirement at the architecture level; runtime proof remains due.

| Requirement | Architecture sections | Governing mechanism or contract |
|---|---|---|
| F-01 | 1, 3–4 | Separate ownership and verified cross-repository activation. |
| F-02 | 1, 5 | Distinct roles, single orchestration owner, one active invocation. |
| F-03 | 1, 4–5 | Bounded action capability and human escalation. |
| F-04 | 1, 4, 6 | Engineering AI permission separated from runtime task permissions. |
| F-05 | 3, 5, 14, 16 | Reviewed baseline, Architect conformance, human acceptance. |
| F-06 | 2–4 | Decision register, source authority, durable activation and supersession. |
| F-07 | 4 | Mandatory context roots, explicit retrieval closure, sufficiency checks. |
| F-08 | 3–5 | Current-state validation and impact reconciliation. |
| F-09 | 4–5 | Persistent process state, ambiguous invocation recovery. |
| F-10 | 5, 8, 14–15 | Non-progress suspension and consequential retention. |
| F-11 | 14 | Intervention timing, trigger, category, avoidability and continuation evidence. |
| F-12 | 1, 3, 14 | Service deliverable plus process evidence and final assessment. |
| S-01 | 6, 10 | Constrained task definitions and mediated owned effects. |
| S-02 | 1, 6 | No arbitrary programs/paths/network or inherited Forge authority. |
| S-03 | 7–9 | Durable accepted identity, specification, state and evidence. |
| S-04 | 8, 11 | Supported interruption contract and ordered recovery. |
| S-05 | 8–9 | Stable submission identity and verified non-acceptance lookup. |
| S-06 | 7, 9, 11–12 | Distinct retry, new task, continuation and reconciliation. |
| S-07 | 9–10 | Immutable accepted meaning and identity conflict. |
| S-08 | 6, 10–11 | Sole execution domain and observable eligibility order. |
| S-09 | 7, 10–13 | Independent execution/effect/outcome/control facts. |
| S-10 | 10, 12 | Semantic safety plus finite execution grants, revalidated before effects. |
| S-11 | 10, 12–13 | Human-bound recovery basis and single-use permission. |
| S-12 | 12 | History-aware cancellation serialized with execution. |
| S-13 | 7, 12 | Explicit abandonment retaining prior facts and authorization. |
| S-14 | 7, 12 | Administrative closure without rollback or invented certainty. |
| S-15 | 7, 13 | Claim-specific evidence, provenance and authorization. |
| S-16 | 13 | Preserved conflicts and factual versus administrative conclusions. |
| S-17 | 6, 9–10 | Verified private inputs and change-aware effect permission. |
| S-18 | 6, 13 | Local operator commands and inspectable task/recovery views. |

## 4. Acceptance and adversarial coverage

| Obligation | Architecture sections | Review coverage |
|---|---|---|
| A-01 | 8–9, 11, 14 | Acceptance crash and torn-write challenges. |
| A-02 | 9, 14 | Lost acknowledgement trace; stable identity challenge. |
| A-03 | 9, 14 | Same-identity changed-input/policy challenge. |
| A-04 | 8, 10–11, 14 | Partial-effect and missing-publication challenge. |
| A-05 | 10, 12–14 | AR-01, AR-06, AR-07; unsafe-timeout retry challenge. |
| A-06 | 12, 14 | AR-02; interrupted cancellation trace. |
| A-07 | 12–14 | AR-01; abandonment with unresolved outcome challenge. |
| A-08 | 13–14 | Conflicting human/service evidence challenge. |
| A-09 | 6, 11–12, 14 | Surviving executor and exclusive-owner challenge. |
| A-10 | 9–10, 14 | AR-03, AR-07; input change-and-restore trace. |
| A-11 | 10, 12, 14 | Retry eligibility order and observable-cause challenge. |
| A-12 | 1, 4, 6, 14 | AR-04; co-hosted permissions challenge. |
| A-13 | 3–5, 14 | AR-05; interrupted activation and context reconstruction. |
| A-14 | 4–5, 14 | Source edits, missing closure, stale summary challenges. |
| A-15 | 5, 8, 14 | Lost dispatch acknowledgement and non-progress challenges. |
| A-16 | 1, 5, 14 | Human coordination versus measured process behavior challenge. |

## 5. Residual assumptions and dispatch prerequisites

These do not conceal unresolved architectural behavior. Each has a defined gate
before the work that depends on it. None is represented as already verified.

| Item | Present evidence/status | Required disposition |
|---|---|---|
| Storage durability and process-lifetime ownership primitives. | Contract specified; no implementation selected or tested. | Select and verify conforming primitives before runtime behavior is relied on. If infeasible, revise and re-review; do not weaken guarantees. |
| Agent adapter scope enforcement and invocation-status access. | Required interface and suspension paths specified; current adapter capability not established by this review. | Validate before dependent dispatch. Missing enforcement blocks it; ambiguous status invokes the documented stop/escalation path. |
| Baseline version-control capture. | Current docs are untracked in the working tree. This manifest fingerprints local content, not a commit. | Preserve the reviewed artifacts in version-controlled history before implementation dispatch. No claim of a committed baseline is made here. |
| Separate service repository and authoritative service-contract publication. | Designated conceptually on this Linux host; repository not created. | Establish location and publish owned service contract during authorized setup before service-source work; verify ownership/source mapping. |
| Task numeric bounds and concrete implementation technologies. | Behavioral contracts and positive finite allowance fixed; concrete values/tools deferred. | Log contract-preserving choices and validate capacity before accepting executable tasks. Material tradeoffs reopen review. |
| Retention after review and future extensions. | No automatic deletion/identity reuse; extensions excluded. | Seek scoped human judgment before disposal or widening boundaries. No immediate blocker. |
| Historical intervention timestamps and later autonomy. | Retrospective record has explicit unknowns; engineering outcomes not observed yet. | Capture future events; carry limitations into human assessment. Do not fabricate missing history. |

Architectural readiness is therefore **READY**. Implementation dispatch is
**NOT ISSUED / operational prerequisites not yet verified**, and runtime conformance
and experiment success are **NOT EVALUATED**. These are different decisions.

## 6. Baseline activation and future changes

The Architect adopts E1-ARCH-1 as the reviewed logical baseline under the authority
already delegated by the human. No repeated human baseline approval is requested.
The final source set is fingerprinted in the manifest. The earlier elicitation
and synthesis readiness judgments are historical and superseded by this review.

Before any later implementation work is issued, check that this readiness decision
still applies to unchanged governing content, operational prerequisites applicable
to that package are met, and the work is bounded by the baseline. Missing prerequisites
stop the affected dispatch; they must not be silently waived because architecture
readiness passed.

Changes to intent, guarantees, authority, task/effect boundaries, or material
architecture assumptions reopen impact assessment and review. Ordinary choices
within the specified contracts remain Architect-derived and logged. This review
ends with the baseline decision; it does not issue implementation work.
