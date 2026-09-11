# Architecture Gap Analysis — Experiment 1

Status: **Architecture READY — baseline E1-ARCH-1 established.** See the
[Architecture Readiness Review](EXPERIMENT_1_ARCHITECTURE_READINESS_REVIEW.md).
This document retains the original gap categories and records their disposition.

Authority: [VISION.md](VISION.md), with human clarifications preserved separately
in [ARCHITECTURE_ELICITATION.md](ARCHITECTURE_ELICITATION.md). This analysis
distinguishes human decisions from architectural derivation. It selects no
technology, specifies no implementation mechanism, and authorizes no implementation.

## Explicitly established

The Vision establishes human-governed engineering through distinct Architect and
Implementation Agent responsibilities, persistent authoritative knowledge,
deliberate context management, evidence-based review, and reconciliation of
implementation with intent. Model memory and agent assertion are insufficient
authority. Material architectural uncertainty must be exposed before dependent
implementation. Major baselines require adversarial review (Vision §§1–17).

The elicitation establishes:

- One project, one Architect, one Implementation Agent, sequential engineering,
  bounded project-local authority, normal interruption/resumption, and detection
  of human changes before dependent work proceeds.
- Autonomous Architect baseline establishment, increment acceptance, and
  evidence-backed completion assessment. Humans retain consequential intent and
  boundary decisions, conflict resolution involving intent, final acceptance,
  and the comparative assessment of autonomy.
- Architect answers establish authoritative clarifications and derived decisions;
  decisions must be logged. The Vision supplies sufficient KGE requirements.
- Auditability of decisions and their governing information, not deterministic
  reproduction of model behavior. Context assurance is proportional to consequence.
- No initial quantitative resource caps, with reasonable efficiency, visible
  non-progress, recoverable suspension, and retention of consequential knowledge.
  Material financial commitments still require the established human approval.
- A new resilient task-execution service as the demonstration, delivered as a
  complete repository with implementation, knowledge, tests/evidence, traceability,
  and a final Architect assessment presented for human acceptance.
- Bounded computational/file-oriented tasks, controlled effects, one trusted
  operator, sequential task execution, observable ordering, and stable accepted inputs.
- Durable accountability for acknowledged work through supported process/host
  interruption when persistent state remains available. Mid-operation uncertainty
  is valid; permanent storage loss/corruption is outside the recovery guarantee.
- Stable logical submission identity; lost acknowledgement does not justify
  duplicate independent work. Retry requires semantic safety and authorization.
- Cancellation governs future execution; abandonment closes further work while
  preserving history and uncertainty. Neither implies rollback.
- Evidence-based reconciliation with source provenance, preserved conflicts, and
  a distinction between administrative decisions and historical facts.
- Intervention-based evaluation and reasoned human comparison with the expected
  manual Architect/Codex workflow. No measured manual control run is required.
- Separate Forge and service repositories on the same Linux host initially.
  Forge owns process knowledge/evidence; the service owns its implementation and
  service knowledge/evidence. Necessary engineering AI-service communication is
  permitted; additional external destinations require explicit authorization.

## Strongly implied architectural properties

These are derivations from the above, not independent statements of human intent.

1. Authority, evidence, assumptions, and agent interpretations must remain
   distinguishable even when they describe the same decision or task.
2. Decision history and current applicability are separate. New information can
   invalidate dependent work without erasing why earlier work was authorized.
3. Logical submission, execution attempts, effects, permission, and administrative
   disposition have distinct meanings. Collapsing them risks false completion,
   hidden duplicates, or apparent certainty created by abandonment.
4. Accepted task meaning must remain stable through interrupted submission,
   execution, retry, and recovery. A mutable reference alone does not establish
   that the accepted input is unchanged.
5. Sequential execution requires addressing whether prior execution has stopped
   after restart/cancellation. An uncertain past effect and a still-running task
   are different conditions.
6. The service's conformance and Forge's engineering effectiveness need separate
   evidence. A correct service alone cannot prove reduced human direction.
7. Intervention evaluation must distinguish intent elicitation from avoidable
   engineering direction. Raw counts cannot establish comparative success.

## Assumptions not adopted

- FIFO execution, unlimited retries, safe repetition, guaranteed eventual success,
  exactly-once execution/effects, implicit rollback, or automatic abandonment.
- Identical task identity authorizing changed inputs or another execution attempt.
- Single-operator trust permitting unrestricted host access or external effects.
- Human authorization proving historical execution facts.
- All uncertainty blocking every independent activity, or no uncertainty blocking any.
- A measured manual comparison, fixed numerical success threshold, or retention
  of every transient interaction.
- The current repository automatically being the authorized demonstration runtime
  or the destination of its final repository.

## Gap disposition after architectural review

| Priority | Gap | Required next work | Who supplies the answer |
|---|---|---|---|
| P0 — baseline readiness | Architecture formulation and required review. | CLOSED: E1-ARCH-1 formulated; seven material adversarial findings reconciled; readiness passed. | Architect decision recorded in Readiness Review. |
| P1 — authority enforcement | Different task/agent permissions and cross-repository provenance. | Architecture §§1–6 and review AR-04/05 define capability boundaries, source-pair activation and version-control dispatch gate. Runtime enforcement remains to verify. | Architect governs contract; human approves expansions. |
| P1 — expensive drift risk | Recovery, partial effects, retry, cancellation, abandonment, sequential restart. | Architecture §§7–13 separates facts/permissions; AR-01/02/06/07 closes command replay, prior effects, continuation bounds and stale approval gaps. Runtime proof remains due. | Implementation evidence and Architect review. |
| P1 — knowledge validity | Stable input meaning, identity conflict, evidence and dependencies. | Architecture §§3–4, 9, 13; AR-03 adds verified consumed input, not just pre/post checks. Runtime proof remains due. | Implementation evidence and Architect review. |
| P1 — experimental evidence | Historical timing and engineering autonomy incompletely observable. | Architecture §14 and intervention ledger preserve limitations and require prospective evidence. Human comparative judgment remains pending experiment execution. | Architect records/analyzes; human assesses. |
| P1 — context integrity | Sufficiency, freshness, provenance across invocations. | Architecture §§3–5 defines mandatory roots, source closure, summary validation and safe suspension. No exhaustive-retrieval claim. | Runtime verification against A-13–15. |
| P2 — future lifecycle boundary | Post-completion retention endpoint and any task-identity expiry are unspecified. | Preserve uncertainty; resolve before introducing deletion, expiry, or reuse that weakens auditability or submission guarantees. | Human retention tradeoffs where needed; Architect derives constraints. |
| P2 — deferred extensions | Multi-user roles, concurrency, distribution, large-scale operation, and fully unattended operation are not initial requirements. | Track exclusions; do not add them as baseline prerequisites. | Human governs any later scope expansion. |

P0 denotes a prerequisite to a justified baseline or the specified dependent work.
P1 findings must be addressed in the baseline review where they affect the scoped
behavior. P2 items may remain explicitly deferred without invented defaults.

## Ambiguities and tensions reconciled by elicitation

No direct contradiction requiring rejection of the Vision has been identified.

- Architect completion authority and human acceptance coexist: the Architect
  establishes evidence-backed conformance and presents the result; it cannot
  represent human acceptance or comparative autonomy judgment as already obtained.
- Effect observability does not promise certainty after every supported interruption.
  Preserve accepted work and report evidence-backed uncertainty when necessary.
- Human authority governs action, while evidence governs historical claims.
  An administrative resolution may leave the operational outcome unknown.
- Sequential operation still needs protection against external edits and surviving
  execution. Excluding general concurrency does not erase those requirements.
- Absence of numerical budgets does not remove consequential-cost approval or
  permit unproductive loops to continue indefinitely.
- Necessity discovered through architecture can justify proposing limited scope
  expansion; it does not independently authorize production or external effects.
- Two repositories are one experiment, not multi-project concurrency. AI-service
  permission applies to engineering roles and does not grant tasks network access.

## Highest-risk omissions to test during review

- Treating repeated submission as an execution retry, or identity conflict as
  permission to replace accepted intent.
- Reporting cancellation or abandonment as proof that effects did not occur.
- Starting a new task while earlier execution may still be active.
- Accepting evidence produced from materially changed inputs as evidence for
  the originally accepted work.
- Replacing conflicting historical evidence with an operator preference.
- Calling the experiment autonomous while the human repeatedly repairs prompts,
  restores persisted context, coordinates agents, or detects drift for them.
- Losing provenance or intervention evidence before the final assessment.

## Readiness and minimum next questions

The [architecture](EXPERIMENT_1_ARCHITECTURE.md) has been formulated against the
[requirements synthesis](EXPERIMENT_1_REQUIREMENTS_SYNTHESIS.md), subjected to
[adversarial architecture review](EXPERIMENT_1_ADVERSARIAL_ARCHITECTURE_REVIEW.md),
and reconciled. All 30 requirements and 16 acceptance obligations are mapped in
the Architecture Readiness Review. No material architectural finding remains open.

The environment and information-boundary question is resolved by the latest human
clarification. The demonstration repository name/path is a later setup detail;
it need not block architectural reasoning or prompt another intent questionnaire.

**No further human intent question is required for this baseline.** New material
intent conflicts, tradeoffs, or boundary changes still return to the human.

**Architecture READY.** Operational dispatch checks and runtime conformance remain
separate: reviewed artifacts currently require version-control capture, the service
repository has not been created, and relevant adapter/storage capabilities must
be verified before dependent work. These are explicit gates, not waived assumptions.
No implementation package has been issued; no technology product has been selected.
