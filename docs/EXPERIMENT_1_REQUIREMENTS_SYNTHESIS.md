# Experiment 1 — Behavioral Requirements Synthesis

Status: Architect-derived requirements and acceptance obligations for architecture
formulation. Not an architectural baseline or an implementation work package.

Authority: [VISION.md](VISION.md) and human answers in
[ARCHITECTURE_ELICITATION.md](ARCHITECTURE_ELICITATION.md). Source abbreviations:
Q1–Q8 denote the original experiment questions; S1–S8 denote Service Questions
1–8; Evaluation and Environment denote the named later clarifications.

This is a Forge experiment artifact. It records derived obligations for review,
not a replacement for the service's eventual authoritative requirements in its
own repository. No implementation technology or mechanism is selected.

## Boundaries and authority

| ID | Required behavior | Source |
|---|---|---|
| F-01 | Keep Forge and the service in separate repositories on the same Linux host initially. Preserve their distinct knowledge and evidence ownership. | Environment |
| F-02 | Operate one Architect and one Implementation Agent sequentially for one active project. Keep architectural reasoning and implementation execution distinguishable. | Vision §§5–6, 16; Q6 |
| F-03 | Permit routine authorized, reversible engineering within the designated repositories and tooling boundary. Consequential boundary changes require human approval; technical necessity is not authority. | Q5; Environment |
| F-04 | Permit AI-service communication needed for the two engineering roles. Do not infer permission for other external publication, storage, telemetry, deployment, or service-task communication. | Environment; S1 |
| F-05 | The Architect may establish a reviewed baseline, accept increments, and declare evidence-backed conformance. Present the final result for human acceptance; the human judges comparative autonomy. | Q1–Q4; Evaluation |
| F-06 | Architect clarifications and derived decisions are authoritative and logged. Escalate intent conflicts to the human. Preserve authority, inference origin, rationale, and supersession history. | Q3, Q7; Vision §§7–14 |
| F-07 | Assemble decision-relevant, sufficiently current context with provenance. Known material omissions block dependent decisions; retrieve, revalidate, narrow justified scope, or escalate. | Q7 |
| F-08 | Reconcile relevant human edits and new knowledge before dependent work continues or is accepted. Assess affected decisions and evidence without erasing historical justification. | Q6–Q7 |
| F-09 | Resume after normal interruption from persistent authoritative knowledge and inspectable current state. Surface uncertain action completion; never assume safe repetition. | Q6 |
| F-10 | Preserve consequential knowledge/evidence through the project and later review. Surface non-progress and suspend affected work recoverably at established limits without weakening correctness. | Q8 |
| F-11 | Capture meaningful interventions with timing, trigger, type, avoidability assessment, and subsequent autonomy evidence. Separate observed facts from judgments and unknowns. | Evaluation |
| F-12 | Deliver the service repository, its knowledge and verification evidence, traceability to intent, and an Architect assessment of conformance and material uncertainty. Support human acceptance and reasoned manual-workflow comparison. | Q1, Q4; Evaluation |

## Service obligations

| ID | Required behavior | Source |
|---|---|---|
| S-01 | Support meaningful bounded computational/file-oriented work with observable inputs, outputs, and attributable effects in authorized service-controlled workspaces. | S1 |
| S-02 | Exclude unrestricted programs, host access, privileged effects, and arbitrary changes outside the controlled boundary. Single-operator trust does not enlarge task permissions. | S1, S4 |
| S-03 | Preserve enough accepted-task identity, input meaning, known lifecycle state, established effects/results, evidence, and recovery state to avoid silently losing acknowledged work after supported interruption. | S2 |
| S-04 | Recover from process interruption/restart and host recovery with persistent service state available, including interruption during execution/effect establishment. Permanent storage loss/corruption has no initial recovery guarantee. | S2 |
| S-05 | Recognize repeated submission of the same logical task through stable identity. Resolve to existing accepted work; accept normally only if non-acceptance is established; preserve acceptance uncertainty otherwise. | S5 |
| S-06 | Distinguish retry under existing identity/intent, explicit new-task resubmission, safe continuation, and reconciliation. None silently substitutes for another. | S3, S5 |
| S-07 | Keep accepted input meaning stable. Do not silently replace accepted work when its reference accompanies changed inputs. Any replacement must be explicitly defined and traceable. | S5, S7 |
| S-08 | Execute sequentially under a defined policy. Make acceptance/execution orders observable without implying equality. Account for lifecycle/operator causes of scheduling deviations. | S7 |
| S-09 | Distinguish task execution, persistent effects, control requests, and administrative disposition. Report only what evidence supports, including uncertainty distinct from failure. | S1–S2, S6 |
| S-10 | Automatically retry only with established semantic safety against unacceptable duplicate effects and within existing authorization. Generic failure labels do not establish safety. | S3 |
| S-11 | Require explicit, attributable human authorization where recovery safety is not established or policy requires judgment. Retain the knowledge, risks, choices, and authorization governing the action. | S3–S4 |
| S-12 | A queued task cancelled before execution must not start. Running cancellation is a stop request: attempt safe stopping where supported and report actual evidence, including partial effects, prior completion, or uncertainty. | S6 |
| S-13 | Abandonment closes further execution/recovery/reconciliation efforts without changing history. Retain identity, intent, state, history, effects, uncertainty, authorization, and any provided reason. | S6 |
| S-14 | Permit administrative closure with unresolved outcome. Neither cancellation nor abandonment implies rollback or proves cessation of execution. | S6 |
| S-15 | Resolve uncertainty only with defensible claim-specific evidence. Record conclusion, provenance, remaining uncertainty, and required authorization. Distinguish human-supplied facts from direct observations. | S4, S8 |
| S-16 | Preserve conflicting sources and assess relevance/reliability, timing, scope, identity, and interpretation. Escalate unresolved conflicts; an administrative decision cannot manufacture historical certainty. | S8 |
| S-17 | Distinguish authoritative inputs, working state, outputs, and external edits. Prevent, assess, invalidate/stop, or reconcile meaningful changes before relying on affected work. | S7 |
| S-18 | Give the single trusted operator visibility into task state, evidence, effects, uncertainty, and consequential recovery choices. Support the specified submission, recovery, cancellation, and abandonment actions without a multi-user role model. | S4–S6 |

## Acceptance obligations

These are observable conditions to demonstrate, not executable tests or prescribed
test mechanisms. They do not assert that any implementation currently passes.

| ID | Scenario and required observation | Requirements |
|---|---|---|
| A-01 | Interrupt after acknowledged acceptance and restart with persistent state available. The task remains identifiable with defensible state and governing input meaning. | S-03–04 |
| A-02 | Lose an acknowledgement and repeat the same logical submission. Existing work is identified without creating another independent task; unresolved acceptance does not silently authorize one. | S-05–06 |
| A-03 | Present different input meaning under an accepted identity. No silent mutation or execution under a falsely unchanged task occurs. | S-07 |
| A-04 | Interrupt during execution and effect establishment. Recovery distinguishes known outcomes, partial effects, and insufficient evidence; it never equates absent completion evidence with absent effects. | S-04, S-09 |
| A-05 | Compare a justified repeatable attempt with an attempt whose effects are uncertain and unsafe to repeat. Only the justified case proceeds automatically; the latter requires the documented human decision. | S-10–11 |
| A-06 | Request cancellation before start, during execution, and after completion. Reports distinguish those conditions, retain effects, and do not claim rollback or stopping without evidence. | S-12, S-14 |
| A-07 | Abandon uncertain work. Administrative closure and unresolved operational outcome coexist; history and authorization remain inspectable. | S-13–14 |
| A-08 | Supply resolving evidence and then a conflicting operator account. Preserve source provenance, justify any outcome change, and retain material uncertainty when only an administrative decision is possible. | S-15–16 |
| A-09 | Recover or cancel while earlier execution may still be active. Do not start overlapping task execution on the unsupported assumption that the earlier task stopped. | S-08, S-14 |
| A-10 | Change relevant task input/workspace state during work. The result is not falsely attributed to unchanged accepted input; demonstrate the applicable prevention, assessment, invalidation, or reconciliation behavior. | S-07, S-17 |
| A-11 | Exercise acceptance, execution, retry, cancellation, and intervention. The operator can reconstruct ordering and reasons for a changed next task without an invented FIFO promise. | S-08, S-18 |
| A-12 | Attempt work outside the constrained task boundary. The service does not silently permit forbidden effects merely because the operator is trusted or both repositories share a host. | S-01–02; F-01–04 |
| A-13 | Across multiple increments and resumed agent invocations, reconstruct consequential decisions from governing intent, repository facts, assumptions, evidence, and dependent work. | F-06–09 |
| A-14 | Introduce stale/missing context or relevant human changes. Dependent work is not silently accepted or continued under invalid knowledge; independent authorized work may continue safely. | F-07–09 |
| A-15 | Reach an unresolved human decision or persistent non-progress. Preserve recoverable state and evidence, surface what is needed, and do not invent authority or weaken completion criteria. | F-03, F-09–10 |
| A-16 | At experiment conclusion, inspect intervention history and conformance evidence. Separate human intent/acceptance from avoidable routine direction; preserve limitations and the human's comparative judgment. | F-05, F-11–12 |

## Adversarial requirements review

This reviews the consistency of derived obligations. It is not a review of a
proposed implementation architecture and does not satisfy that later review gate.

| Finding | Consequence if missed | Disposition |
|---|---|---|
| Shared host can blur engineering-agent and service-task permissions. | Tasks could alter Forge knowledge or transmit data using permissions intended only for engineering agents. | Addressed as a requirement by F-01–04 and S-02; enforcement remains an architecture obligation. |
| Two repositories can describe different governing states. | Evidence could be accepted against a different requirement revision than the one governing implementation. | F-06–08 and A-13 require inspectable cross-repository provenance; the architecture must explain how consistency is established. |
| Stable task identity does not suppress duplicate effects by itself. | A repeated request or failed attempt could authorize unsafe execution. | S-05–11 distinguish identity, attempts, and permission; A-02 and A-05 exercise both. |
| Unresolved outcome can coexist with stopped execution, while an apparently stopped process can leave work active. | Either unnecessary global blocking or overlapping execution. | S-08–09, S-14, and A-09 require separate assessment of activity and historical effect uncertainty. |
| Human authority can be mistaken for factual evidence. | Recovery records conceal contradiction or assert unverified success. | S-15–16 and A-08 preserve factual versus administrative conclusions. |
| General resource policy can be misread as unlimited task retries. | Correct but unproductive cycling undermines the experiment. | No unlimited-retry behavior is authorized; the architecture must define bounded task/retry policy consistent with semantics and F-10. |
| An answer log can be mistaken for full autonomy evidence. | Final evaluation relies on incomplete retrospective impressions. | F-11 and A-16 require intervention capture with timing/avoidability/continuation limitations explicitly recorded. |
| Building the service can be mistaken for proving Forge's whole loop. | Good task-service results hide manual coordination and context repair. | F-12 and A-13–16 require separate process evidence; human comparison remains authoritative. |

No new contradiction requiring human intent was found in this requirements-level
review. The architecture must still establish evidence sufficiency, permission
enforcement, current-state reconciliation, scheduling/retry behavior, persistence
and recovery guarantees, and cross-repository knowledge consistency. These are
derivation obligations, not permission to choose arbitrary user-visible behavior.

## Readiness

This requirements synthesis and its requirements-level review are complete.
Subsequent architectural formulation and adversarial review have now established
baseline E1-ARCH-1 as READY; see the
[Architecture Readiness Review](EXPERIMENT_1_ARCHITECTURE_READINESS_REVIEW.md).
The readiness decision maps every requirement and acceptance obligation here.

No further general elicitation question is required now. Return to the human for
material tradeoffs, conflicts, or boundary changes exposed during formulation.
No repository setup, source changes, technology-product selection, or implementation
work-package issuance has been performed as part of this formulation/review task.
