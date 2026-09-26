# Service requirements — E1-SVC-1

Source: Forge baseline E1-ARCH-1, commit `411cb5a9fabc71e482a414ed58387de0ff557e93`.
Local source repository: `/home/gvasend/app/kge-forge`.
The original human answers and frozen source remain retrievable at that commit.

Status: Published service-owned contract. Source requirements retain their IDs.
S1–S8 in the source column refer to the Service Questions in the Forge elicitation
record. Forge process requirements remain owned by Forge; F-* references preserve
that cross-system constraint, not service runtime permission.

## Requirements

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

## Service acceptance obligations

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

## Verification status

No implementation or verification exists yet. Publication does not claim conformance.
