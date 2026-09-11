# Architecture Elicitation Record

Authoritative statement of human intent: [VISION.md](VISION.md).

This record preserves human answers separately from architectural interpretation.
Unanswered questions and unresolved choices do not authorize default behavior.
Subsequent formulation and review establish architectural baseline E1-ARCH-1 as
READY; see EXPERIMENT_1_ARCHITECTURE_READINESS_REVIEW.md. Earlier readiness notes
are historical. No implementation work package has been issued through this record.

## Question 1 — First experiment

**Question:** What representative engineering task must Forge complete, from
what starting condition to what final deliverable, and what activities are
explicitly outside its responsibility?

**Status:** DECIDED for the demonstration objective, new-system starting point,
deliverable, and completion presentation. Service behavior requires further
elicitation before a baseline.

**Human answer (2026-09-10):** “Undecided”

**Human clarification (2026-09-10, verbatim):**

> The first KGE Forge experiment should engineer a new, non-trivial software system from a human-provided vision rather than extend an existing complex system.
>
> The demonstration system should be a resilient task-execution service. At a conceptual level, the system accepts units of work, executes them, records their progress and results, handles failures according to defined policy, and can recover from interruption without losing the ability to determine the authoritative state of submitted work.
>
> The purpose of selecting this problem is not the task-execution capability itself. It is to provide a compact but architecturally meaningful engineering problem involving state, lifecycle, authority, persistence, failure handling, recovery, observable behavior, and verification.
>
> The initial human description should intentionally avoid prescribing implementation technologies or detailed architecture. Those decisions should be derived through the KGE Forge architecture process.
>
> The final deliverable should be a complete software repository containing:
>
> * A working implementation of the system.
> * The authoritative engineering knowledge developed during the project.
> * Automated tests and other evidence sufficient to demonstrate conformance with the derived requirements and acceptance criteria.
> * Traceability sufficient to understand how major architectural decisions relate to the original vision and implementation.
> * A final Architect assessment explaining whether the engineered system satisfies the original human intent and identifying any material unresolved uncertainty.
>
> The experiment ends when the Architect determines that the derived acceptance criteria have been satisfied with adequate evidence and presents the result for human acceptance.
>
> Deployment into a production environment, large-scale performance, distributed multi-host execution, and production operational support are not required unless the architecture process determines that some limited form is necessary to demonstrate the stated system behavior.
>
> The human should judge the final result primarily by whether the resulting system behaves as intended and whether Forge reached that result without requiring the human to continuously engineer the solution.

**Established intent (summary; the clarification above governs):**

- Engineer a new resilient task-execution service from human vision; do not use
  extension of an existing complex system as the demonstration.
- The service accepts work, executes it, records progress and results, handles
  failures under defined policy, and recovers sufficiently to determine the
  authoritative state of submitted work.
- Deliver a complete repository with working implementation, authoritative
  engineering knowledge, automated tests and conformance evidence, architectural
  traceability, and a final Architect assessment including material uncertainty.
- The Architect determines satisfaction of derived acceptance criteria from
  adequate evidence and presents the result for human acceptance.
- Production deployment/support, large-scale performance, and distributed
  multi-host execution are not required unless limited forms are shown necessary
  through architecture elicitation. Question 5 still governs authorization for
  consequential actions; necessity alone does not grant approval.

**Interpretation history:** The earlier “Undecided” answer is superseded by this
explicit selection. No technology, detailed architecture, or implementation work
is selected or authorized by recording it.

**Architectural implications:** The demonstration service and Forge's engineering
process are separate subjects of requirements and verification. Forge's
sequential-agent scope does not by itself decide whether the service executes
tasks concurrently. Recoverable authoritative task state does not by itself
promise exactly-once task effects, automatic retries, or recovery from every
failure. Those consequential behaviors remain open.

**Baseline impact:** The experiment-selection gap is resolved. The service's task
boundary, lifecycle, failure and recovery guarantees, and acceptance criteria
still require elicitation and derivation.

## Question 2 — Delegated authority

**Question:** Which decisions may the Architect make autonomously, and which
require human approval—including baseline establishment, architectural changes,
increment acceptance, and final completion?

**Status:** DECIDED for the three listed decisions; remaining authority boundaries
are UNRESOLVED.

**Human answer (2026-09-10):** “establish the baseline, accepting increments and declaring completion”

**Human clarification (2026-09-10):** “auto”, in response to whether these decisions
require human approval or may be made autonomously by the Architect.

**Established intent:** The Architect may autonomously establish the baseline,
accept increments, and declare completion.

**Interpretation history:** The earlier tentative interpretation that these
decisions were reserved for human approval was not adopted and is superseded by
the explicit clarification above.

**Architectural implications:** Delegation determines who may make these
decisions; it does not establish readiness, acceptance criteria, or completion
criteria. The Vision's evidence, elicitation, and review obligations still apply.
Question 1 now selects the experiment, but no baseline is established by this
delegation. Its later clarification specifies that the Architect presents the
evidence-backed result for human acceptance. The current instruction not to
begin implementation remains in effect.

**Remaining gap:** Authority for other architectural changes and the boundaries
of routine autonomous decisions are further clarified in Question 5. Material
changes to intent and consequential security or architectural tradeoffs require
human approval. The Vision's existing human governance requirements continue to
apply; no blanket delegation of all architectural changes is inferred.

## Question 3 — Authoritative knowledge

**Question:** What makes a clarification or derived decision authoritative, and
who resolves conflicts? Does KGE impose requirements beyond the Vision?

**Status:** DECIDED for authority of Architect answers, required decision logging,
human resolution of conflicts with the Vision or explicit human clarifications,
and sufficiency of the Vision for initial KGE requirements; remaining questions
are UNRESOLVED.

**Human answer (2026-09-10):** “A clarification or derived decision is authoritative if answered by the Architect. The decision should be logged.”

**Human clarification (2026-09-10):** “the human”, in response to who resolves
a conflict between an Architect decision and the Vision or an explicit human
clarification.

**Human clarification (2026-09-10):** “Vision is sufficient”, in response to
whether KGE imposes requirements beyond the Vision or the Vision is sufficient
for the initial experiment.

**Established intent:** A clarification or derived decision answered by the
Architect is authoritative. The decision must be logged. The human resolves
conflicts between Architect decisions and the Vision or explicit human
clarifications. The Vision is sufficient for the initial experiment; no
additional KGE requirements need to be incorporated from outside the Vision.
This does not resolve the architectural gaps identified within the Vision.

**Architectural interpretation:** The Architect can establish authoritative
clarifications and derived decisions, rather than only proposing them for human
ratification. Logging preserves that authority beyond the conversation. This
answer does not explicitly authorize overriding human intent or remove the
Vision's human governance requirements.

**Remaining gaps:**

- Question 7 further establishes that contradictions follow the authority model;
  conflicts involving human intent or not resolvable from existing authoritative
  knowledge escalate to the human.
- Is logging a precondition for acting on a decision, or an obligation that may
  be fulfilled after the answer? No permission to defer logging is inferred.

## Question 4 — Success and acceptable uncertainty

**Question:** What observable results would convince you that the experiment
succeeded, including implementation quality, preserved intent, and reduced human
direction? What residual uncertainty is acceptable at completion?

**Status:** DECIDED for qualitative success criteria and acceptable residual
uncertainty; experiment-specific evaluation details remain UNRESOLVED.

**Human answer (2026-09-10, verbatim):**

> The experiment would be considered successful if KGE Forge can take a human-provided vision and, through the Architect and Implementation Agent, produce a non-trivial engineered result that demonstrably satisfies the intent expressed in that vision while requiring substantially less continuous human engineering direction than the equivalent manual process.
>
> Observable evidence of success should include:
>
> * The resulting implementation satisfies requirements and acceptance criteria traceable to the original human vision.
> * The Architect identifies significant architectural questions, assumptions, and risks early enough to prevent avoidable implementation rework.
> * Implementation work can proceed through multiple increments without significant loss or distortion of the original intent.
> * The Architect detects meaningful inconsistencies or drift among the vision, architecture, implementation, and evidence.
> * Implementation discoveries are correctly distinguished from changes in human intent and are incorporated into the architecture when appropriate.
> * Codex can execute Architect-generated work packages with limited need for the human to rewrite, clarify, or supplement those instructions.
> * Claims of completion are supported by observable evidence rather than agent assertion alone.
> * The system recognizes situations in which authoritative knowledge is insufficient and requests human guidance rather than silently making consequential assumptions.
> * The process retains sufficient knowledge and evidence that consequential engineering decisions can later be understood and traced to the information that governed them.
> * The final result is recognizable to the human originator as the system they intended to create.
>
> Success does not require that the initial architecture predict every issue that will arise during implementation. Architectural discovery is an expected part of engineering. Some uncertainty may remain at completion when it does not materially affect satisfaction of the vision, is explicitly identified, and does not undermine the evidence supporting completion.
>
> The experiment should therefore also record significant issues that escape the stage where they reasonably could have been identified. A late discovery does not necessarily make the experiment unsuccessful, but it provides evidence about where the KGE Forge engineering process should improve.
>
> Likewise, occasional human intervention is acceptable. The objective is not to eliminate the human from engineering but to move human participation toward intent, priorities, consequential tradeoffs, and acceptance while allowing the agents to perform increasingly routine architecture, implementation, verification, and coordination work.
>
> The strongest evidence of success would be that the system reaches a justified completion state with the human primarily confirming that the resulting system reflects their intent, rather than repeatedly directing how the system should be engineered.

**Established intent (summary; the answer above governs):**

- Success requires a non-trivial result demonstrably satisfying human intent,
  with substantially less continuous human engineering direction than the
  equivalent manual process.
- Evidence must address both the resulting implementation and the engineering
  process across multiple increments, including traceability, drift detection,
  discovery handling, work-package usability, and justified completion.
- Residual uncertainty is acceptable only when explicitly identified, immaterial
  to satisfaction of the vision, and compatible with the completion evidence.
- Significant issues discovered later than reasonably expected must be recorded
  as process-improvement evidence. Neither late discovery nor occasional human
  intervention automatically constitutes failure.
- The human originator's recognition of the intended system is part of success.

**Architectural implications:** Evaluating Forge requires evidence of how the
engineering process performed, in addition to evidence that the engineered
result works. Human effort, significant late discoveries, and continuity of
intent must be assessable. The previously delegated authority to declare
completion remains in effect; this answer does not explicitly introduce a new
human approval gate.

**Remaining gaps:**

- Question 1 now selects a resilient task-execution service. Its specific
  acceptance criteria remain to be derived from further behavioral elicitation.
- The equivalent manual comparison and how to assess “substantially less” human
  direction and “limited” instruction repair remain unspecified. No numerical
  threshold or comparison method is assumed.
- Question 1 now establishes that the Architect determines evidence-backed
  satisfaction of acceptance criteria and presents the result for human
  acceptance. Human acceptance must not be represented as already obtained by
  virtue of the Architect's completion declaration.

**Baseline impact:** General success intent is now established. Scope and
experiment-specific evaluation obligations still need resolution before the
initial baseline can be justified.

## Question 5 — Trust and consequences

**Question:** What data and environments may agents access, what actions may they
perform autonomously, and which risks or actions require human approval?

**Status:** DECIDED for the initial trust model and action boundaries; concrete
environment designation and resource limits remain UNRESOLVED.

**Human answer (2026-09-10, verbatim):**

> For the first experiment, agents may access the designated project repository, its version-controlled engineering knowledge, implementation files, tests, build artifacts, and other project-local information needed to perform architecture, implementation, and verification work.
>
> The Architect should have sufficient read access to inspect the repository and relevant project evidence independently. The Implementation Agent may read and modify files within the designated project repository and execute normal development activities needed to implement and verify authorized work.
>
> Agents may autonomously perform routine, reversible engineering actions within the project boundary, including:
>
> * Reading project files and engineering knowledge.
> * Searching the repository and inspecting version history.
> * Creating and modifying source code, tests, documentation, and project-local configuration when authorized by the current work.
> * Running builds, compilers, test suites, static analysis, benchmarks, and other project-local verification activities.
> * Creating temporary or generated artifacts needed for engineering work.
> * Proposing architectural changes, requirements, assumptions, or decisions for review.
> * Recording implementation evidence and project status.
> * Reverting or correcting their own uncommitted or otherwise safely reversible project-local changes when necessary.
>
> The initial experiment should favor a least-privilege model. Access to information or capabilities outside the designated project environment should not be assumed merely because it is technically available.
>
> Human approval should be required before an agent performs actions that materially extend beyond the normal project-development boundary, including:
>
> * Accessing unrelated private, confidential, classified, regulated, or sensitive information.
> * Introducing or using credentials, secrets, privileged accounts, or protected external systems that were not already explicitly authorized for the project.
> * Deploying software to production, operational, customer-facing, mission, or other consequential environments.
> * Publishing or transmitting project information outside approved boundaries.
> * Making destructive or difficult-to-reverse changes to external systems or data.
> * Incurring material financial cost or committing resources beyond established limits.
> * Changing security boundaries, access-control policies, trust relationships, or permissions in a consequential way.
> * Modifying authoritative human intent or making architectural tradeoffs that materially change the intended system.
> * Performing actions that could create safety, legal, regulatory, security, or operational consequences beyond the defined experimental environment.
>
> The Architect may identify that one of these actions is necessary and recommend it, but should not interpret technical necessity as authorization.
>
> Within the designated development environment, routine actions should not require repeated human approval merely because they modify code or execute tests. The objective is to avoid turning human approval into a bottleneck for ordinary engineering while preserving human authority over consequential actions.
>
> When uncertainty exists about whether an action falls within the authorized boundary, the system should prefer to pause that specific action and surface the issue for human decision rather than silently expanding its own authority.
>
> For the first experiment, the trust model should remain intentionally narrow. Broader autonomy, additional environments, external integrations, production deployment, or access to sensitive information may be introduced later only after the basic Architect–Implementation Agent loop has demonstrated reliable behavior within this constrained boundary.

**Established intent (summary; the answer above governs):**

- Routine, reversible work within the designated project boundary is autonomous
  when authorized by the current work and appropriate to the agent's role.
- The Architect independently inspects repository facts and evidence; the
  Implementation Agent performs authorized implementation and verification.
- Access follows least privilege. Technical availability or necessity does not
  confer authorization.
- The listed consequential actions and extensions beyond approved boundaries
  require human approval. Routine engineering does not require repeated approval.
- Boundary uncertainty pauses the specific affected action for human decision.
- Broader trust and autonomy may be introduced only after the constrained loop
  has demonstrated reliable behavior, with the applicable human approvals.

**Architectural implications:** Authorization depends on the action's scope and
effects, not merely where a command starts or a file resides. An otherwise routine
build or test is not blanket authorization for unapproved external effects.
Pausing an uncertain action does not itself require stopping independent,
already-authorized work. The Architect's authority to answer clarifications and
derived decisions does not override the human approvals specified here.

**Remaining gaps:**

- The experiment's designated repository, development environment, approved
  information destinations, and any pre-authorized external capabilities must
  be identified before affected work begins. The current workspace alone does
  not settle the experiment's full boundary.
- Question 8 establishes that no strict quantitative resource limits are needed
  initially. The human-approval requirement for material financial cost remains;
  no numerical definition of materiality is established.
- The evidence needed to justify later expansion of the trust boundary remains
  unspecified; expansion is not authorized by this answer.

**Current phase:** These are operating requirements for the experiment, not an
instruction to begin implementation. Architecture elicitation continues under
the existing restriction against implementation work and technology selection.

## Question 6 — Operating envelope

**Question:** Should the first experiment support multiple projects, overlapping
agent work, human edits during execution, unattended operation, and recovery
after interruption—or which should be excluded?

**Status:** DECIDED for initial operating scope and interruption/change-handling
obligations; detailed acceptance criteria remain to be derived.

**Human answer (2026-09-10, verbatim):**

> The first experiment should deliberately use a narrow operating envelope so that its results reflect the effectiveness of the Architect–Implementation Agent process rather than complexity introduced by concurrency, distributed execution, or multi-project coordination.
>
> The initial experiment should support:
>
> * One active project.
> * One Architect Agent.
> * One Implementation Agent.
> * Sequential work rather than overlapping implementation activity.
> * Human review and intervention at defined decision points.
> * Normal interruption and later resumption of the engineering process.
> * Detection and reconciliation of human changes to project knowledge or implementation before dependent autonomous work continues.
>
> The first experiment does not need to support:
>
> * Multiple concurrent projects.
> * Multiple Implementation Agents working in parallel.
> * Overlapping work packages.
> * Concurrent architectural decisions.
> * Autonomous merging of competing implementation changes.
> * Fully unattended long-duration operation.
> * Distributed agents operating across multiple hosts.
> * General-purpose concurrency control for simultaneous human and agent edits.
>
> Human edits during execution should be permitted, because they are realistic and may represent legitimate changes in intent, knowledge, or implementation. However, the system should not assume that work started before such a change remains valid. Relevant changes should be detected and reconciled before dependent work is accepted or continued.
>
> The system should support interruption and recovery at the level necessary to preserve authoritative project knowledge and avoid dependence on an individual model invocation or conversation. After interruption, the system should be able to determine the current authoritative project state sufficiently to continue safely or identify that human intervention is required.
>
> The first experiment does not require transparent recovery from every possible mid-operation failure. If an interruption leaves the completion state of an action uncertain, that uncertainty should be surfaced rather than guessed.
>
> Unattended operation may be tested later, after the basic sequential engineering loop has demonstrated that it can preserve intent, maintain architectural coherence, detect drift, and evaluate evidence reliably.
>
> The guiding principle for the first experiment is to introduce only enough operational complexity to test the core hypothesis:
>
> **Can an Architect Agent and an Implementation Agent transform authoritative human intent into a verified implementation while maintaining alignment across vision, architecture, implementation, and evidence?**
>
> Capabilities such as parallel agents, multi-project scheduling, distributed execution, and fully unattended operation should be treated as later extensions rather than prerequisites for the initial proof.

**Established intent (summary; the answer above governs):**

- Initial operation is one active project, one Architect, and one Implementation
  Agent, with sequential work and defined human decision points.
- Parallel implementation, overlapping work packages, concurrent architectural
  decisions, autonomous merging of competing changes, multi-project concurrency,
  distributed agents, general-purpose simultaneous-edit control, and fully
  unattended long-duration operation are not initial requirements.
- Human edits are permitted during execution. Relevant changes must be detected
  and reconciled before dependent work continues or is accepted; previously
  started work is not presumed valid after such changes.
- Normal interruption and later resumption must preserve authoritative knowledge
  and establish enough current state to continue safely or request human help.
- Uncertain action completion must be surfaced. Transparent recovery from every
  mid-operation failure is not required.

**Architectural implications:** Sequential agent execution does not remove the
need to detect stale authority, context, implementation, or evidence caused by
human edits. Resumption requires reassessing current authoritative state, rather
than trusting conversational memory. An uncertain interrupted action cannot be
assumed completed, failed without effects, or safe to repeat. These are behavior
constraints; no recovery or change-detection mechanism is selected here.

**Remaining derivation:** Define review/continuation boundaries, criteria for
change relevance and work/evidence validity, and observable resumption outcomes.
Any tradeoff that would weaken the stated change-detection or recovery
obligations must be surfaced rather than inferred from the concurrency exclusions.

**Baseline impact:** Initial concurrency and recovery scope are now established.
Future parallelism, distribution, and unattended operation do not block this
initial baseline. The representative experiment and remaining assurance and
practical-limit questions still require resolution.

## Question 7 — Context and audit assurance

**Question:** Is reconstructing a consequential decision's governing information
and justification sufficient, or must the system reproduce the same result?
What should happen when required context is missing, stale, or contradictory?

**Status:** DECIDED for auditability, proportional context assurance, uncertainty
handling, and reconsideration of decisions and dependent work. Detailed acceptance
criteria remain to be derived.

**Human answer (2026-09-10, verbatim):**

> For the first experiment, it is sufficient to reconstruct the governing information and justification for a consequential decision. The system does not need to reproduce the identical model response, reasoning process, or decision when that information is processed again.
>
> A consequential engineering decision should retain sufficient information to determine:
>
> * What human intent and authoritative project knowledge governed the decision.
> * What architectural requirements, constraints, invariants, and prior decisions were relevant.
> * What implementation state and evidence were considered.
> * What assumptions or unresolved uncertainties were known at the time.
> * What decision was made and the justification for that decision.
> * What subsequent engineering work depended upon the decision.
>
> The objective is **decision auditability and traceability**, not deterministic reproduction of model behavior.
>
> A later Architect may reach a different conclusion when presented with the same information. That does not by itself invalidate the earlier decision. The important questions are whether the original decision was reasonable given the authoritative information available at the time and whether subsequent information now provides sufficient reason to reconsider it.
>
> Required context should be current and sufficiently complete for the consequence of the decision being made. The system does not need to prove that every potentially relevant piece of information in the project has been considered. It should instead establish reasonable confidence that omitted information is unlikely to materially change the decision.
>
> When required context is known to be missing, the system should not make a consequential decision that depends upon that context. It should identify the missing information and either obtain it, reduce the scope of the decision to something that can be justified from available information, or request human guidance.
>
> When relevant context is stale, the system should refresh or revalidate it before relying upon it for a consequential decision. Work or evidence based upon superseded authoritative information should not automatically remain valid.
>
> When authoritative information is contradictory, the system should not silently choose whichever source is most convenient, newest, or most strongly represented in the available context. The contradiction should be made explicit and resolved according to the established authority model. If the conflict involves human intent or cannot be resolved from existing authoritative knowledge, it should be escalated to the human.
>
> When uncertainty exists but does not materially affect the decision, the Architect may proceed while recording the uncertainty where appropriate. The required level of context assurance should therefore be proportional to the consequence and reversibility of the decision.
>
> The system should preserve enough provenance to distinguish between:
>
> * What was authoritative at the time.
> * What was assumed.
> * What was inferred by an agent.
> * What was reported by an Implementation Agent.
> * What was directly observed from implementation or evidence.
> * What became known only after the decision was made.
>
> If later information demonstrates that an earlier consequential decision is no longer justified, the system should identify the affected decision and dependent work, determine the potential impact, and reconcile the affected architecture and implementation rather than simply replacing the old knowledge and continuing.
>
> The guiding principle is:
>
> **KGE Forge should be able to explain why a consequential engineering decision was justified given what was authoritatively known at the time, without requiring AI reasoning itself to be exactly reproducible.**

**Established intent (summary; the answer above governs):**

- Consequential decisions must be auditable through governing intent, knowledge,
  requirements, implementation state, evidence, known uncertainty, justification,
  and dependent work. Identical model behavior need not be reproduced.
- Context assurance is proportional to consequence and reversibility. Exhaustive
  consideration of all potentially relevant information is not required;
  reasonable confidence against material omission is required.
- Missing required context blocks dependent consequential decisions until it is
  obtained, the decision is narrowed to a justified scope, or human guidance
  resolves the issue. Stale context must be refreshed or revalidated.
- Contradictions must be explicit and follow established authority. Conflicts
  involving human intent or not resolvable from authoritative knowledge escalate
  to the human; convenience, recency, and prominence do not establish precedence.
- Immaterial uncertainty permits progress with appropriate recording.
- Provenance must distinguish authority, assumptions, agent inference, agent
  reports, direct observations, and information learned after the decision.
- Later disagreement alone does not invalidate a decision. Information that
  undermines its justification requires impact assessment and reconciliation of
  affected decisions, architecture, implementation, and dependent work.

**Architectural implications:** A decision's historical justification and its
continued applicability are separate questions. Updating knowledge cannot erase
the historical basis needed for audit or automatically validate dependent work.
An inference's origin remains distinguishable even if an Architect establishes
it as authoritative under Question 3. Context sufficiency must have an assessable
basis rather than relying solely on an agent's assertion of confidence.

**Remaining derivation:** Define observable acceptance criteria for provenance,
context sufficiency, freshness, contradiction handling, and impact reconciliation
within the selected experiment. No numerical confidence threshold, deterministic
replay requirement, or context-management technology is introduced here.

**Baseline impact:** The assurance target and required responses to context
uncertainty are now established. The representative experiment, its evaluation
details, and practical limits remain open; this answer does not establish a
baseline or authorize implementation.

## Question 8 — Practical limits

**Question:** What cost, elapsed-time, data-retention, and human-availability
limits should govern the first experiment, and what should happen when those
limits are reached?

**Status:** DECIDED for initial resource policy, retention purpose and scope,
human-unavailability behavior, and handling of limits and lack of progress.
Detailed evaluation and retention endpoints remain to be established.

**Human answer (2026-09-10, verbatim):**

> The first experiment should prioritize learning whether the KGE Forge engineering model works over optimizing cost, execution time, or resource consumption. No strict monetary, token, compute, or elapsed-time limits need to be established initially.
>
> Reasonable resource efficiency is expected. Agents should avoid obviously redundant work, unnecessary repeated analysis, or continued activity that is not producing meaningful progress or evidence. However, resource optimization should not compromise architectural rigor, verification, preservation of authoritative knowledge, or the integrity of the experiment.
>
> Elapsed time is not itself a primary success criterion for the first experiment. The system may take the time reasonably necessary to perform architecture elicitation, implementation, verification, and reconciliation correctly. Persistent lack of progress, repeated unsuccessful attempts, or cycles that do not materially advance the objective should be recognized and surfaced rather than allowed to continue indefinitely.
>
> Project knowledge necessary to understand and evaluate the experiment should be retained for the duration of the project and sufficiently beyond completion to permit review of how the result was produced. This includes authoritative human intent, architectural decisions, requirements, assumptions, significant changes, implementation work packages, consequential evidence, and information necessary to reconstruct important engineering decisions.
>
> Retention of every transient model interaction, intermediate output, command result, or temporary artifact is not required unless it contributes materially to a consequential decision, verification result, unresolved issue, or evaluation of the experiment.
>
> Human availability should not be assumed to be continuous. The system should be capable of progressing autonomously while work remains within established authority and sufficient knowledge exists to justify the next action.
>
> When human judgment is required, the system should preserve its current state and clearly identify the decision or information needed. It should not substitute an agent-generated assumption merely because the human is unavailable.
>
> Human unavailability should therefore pause only work that actually depends upon the unresolved human decision. Work that remains independently authorized and does not depend upon that decision may continue when doing so cannot create conflicting or invalid work.
>
> If an established resource, time, or authority limit is reached, the system should stop or suspend the affected work in a recoverable state and report:
>
> * What objective was being pursued.
> * What progress has been made.
> * What remains incomplete.
> * What evidence has been produced.
> * Why further progress cannot currently be justified.
> * What decision, resource, information, or authorization would permit work to continue.
>
> The system should not respond to resource pressure by silently weakening acceptance criteria, omitting required verification, discarding authoritative knowledge, or declaring incomplete work complete.
>
> For the first experiment, explicit quantitative limits may be introduced if experience demonstrates that they are useful. The initial objective is to observe actual resource usage and human involvement so that later limits can be based upon empirical evidence rather than arbitrary assumptions.
>
> The guiding principle is:
>
> **Resource limits may constrain how much work KGE Forge performs, but they should not silently change the meaning of correctness, authority, or completion.**

**Established intent (summary; the answer above governs):**

- No strict monetary, token, compute, or elapsed-time limits are required
  initially. Learning and engineering integrity take priority over optimization.
- Avoid redundant activity; recognize and surface persistent lack of meaningful
  progress. Observe actual resource use and human involvement to inform later
  limits. Elapsed time alone is not a primary success criterion.
- Retain knowledge and evidence needed to understand and evaluate the experiment
  throughout the project and sufficiently beyond completion for review.
  Transient material need not be retained unless materially relevant to a
  decision, verification, unresolved issue, or evaluation.
- Human unavailability blocks dependent work, not independently authorized work
  that can proceed without conflicts or invalid results. It never authorizes
  substituting assumptions for required human judgment.
- Reaching an established limit requires recoverable suspension of affected
  work and a report of objective, progress, incomplete work, evidence, reason
  for suspension, and what would permit continuation.
- Resource pressure must not silently weaken correctness, authority, acceptance,
  verification, knowledge preservation, or completion standards.

**Architectural implications:** Lack of quantitative limits is an explicit
initial policy, not an omission to fill with arbitrary budgets. It does not
authorize material financial commitments or external access contrary to Question
5. Continuing independent work during human unavailability remains subject to
Question 6's sequential operating envelope; fully unattended long-duration
operation is still not an initial requirement. Suspension must preserve both
completed evidence and unresolved state without overstating action completion.

**Remaining derivation and clarification:** Define observable progress and
resource-use evidence and the basis for identifying unproductive cycles without
inventing human-approved thresholds. The post-completion retention endpoint is
not specified; no automatic deletion deadline is authorized. If a proposed cost
raises materiality uncertainty under Question 5, surface that action for human
decision rather than treating absent numeric limits as permission.

## Service Question 1 — Task scope and effects

**Question:** What kinds of work should users submit, and what effects may those
tasks have—for example, producing results within the service versus modifying
files or external systems?

**Status:** DECIDED for the initial task boundary and effect-attribution
requirements. Submission authority and detailed recovery/retry semantics remain
UNRESOLVED.

**Human answer (2026-09-10, verbatim):**

> For the first experiment, users should submit bounded computational or file-oriented tasks whose inputs, outputs, and effects can be represented and observed within the service’s controlled execution environment.
>
> Representative tasks may include:
>
> * Performing a computation and returning a result.
> * Transforming supplied input data into an output artifact.
> * Reading designated task input files and producing derived files.
> * Running a bounded analysis or command within an authorized workspace.
> * Producing logs, status information, metrics, or other execution evidence associated with the task.
>
> Tasks may create or modify artifacts within a task-specific or otherwise explicitly authorized service-controlled workspace.
>
> Tasks should not, for the first experiment, be permitted to make arbitrary external changes such as:
>
> * Modifying unrelated files outside the authorized workspace.
> * Changing operating-system configuration.
> * Accessing unrestricted host resources.
> * Calling external services that create consequential side effects.
> * Modifying databases, cloud resources, repositories, accounts, or other external systems.
> * Using credentials or secrets to perform privileged actions.
>
> Read-only external access is also not required for the first experiment unless the architecture process determines that a narrowly bounded form is necessary to demonstrate a requirement.
>
> The service should distinguish the execution of a task from the effects produced by that task. A task should have an identifiable execution state, and any persistent artifact or result produced by it should be attributable to that execution.
>
> For the initial experiment, task effects should be sufficiently bounded that the system can determine whether they occurred, associate them with the responsible task, and reason about the consequences of retrying or recovering that task after interruption.
>
> The system should not assume that every task is inherently safe to execute more than once. The architecture should therefore explicitly address the relationship among task execution, persistent effects, retries, and recovery rather than relying on the assumption that duplicate execution is harmless.
>
> The first experiment does not need to support arbitrary user-supplied programs with unrestricted authority. It is sufficient to support a constrained task model that is expressive enough to demonstrate meaningful lifecycle, failure, persistence, and recovery behavior.
>
> The guiding principle is:
>
> **Tasks may perform meaningful work, but their effects should remain inside a controlled boundary where KGE Forge can observe, attribute, and verify what happened.**

**Established intent (summary; the answer above governs):**

- Support bounded computation and file-oriented work with observable inputs,
  outputs, and effects inside the controlled execution environment. The listed
  examples are representative possibilities, not a mandatory task catalog.
- Task effects may include artifact creation and modification in a task-specific
  or explicitly authorized service-controlled workspace.
- Arbitrary external changes, unrestricted host access, privileged actions using
  secrets, and unrestricted user-supplied programs are outside initial scope.
  External read access is not initially required; any proposed necessity remains
  subject to the established authorization boundaries.
- Execution state and persistent effects must be distinguishable. Persistent
  artifacts and results must be attributable to the responsible execution.
- Effects must be bounded enough to determine their occurrence and assess retry
  and recovery consequences. Repeated execution is not presumed harmless.

**Architectural implications:** Task execution success and the existence or
validity of its effects are separate facts to verify. Failure does not establish
that no effects occurred, and an existing artifact alone does not establish task
completion. The constrained task model must support inspectable attribution and
recovery; it cannot silently rely on arbitrary commands being well behaved.
These constraints do not select an isolation mechanism, execution technology,
artifact-publication scheme, or retry policy.

**Remaining questions:** Submission authority, treatment of partial effects,
and safe retry behavior remain to be elicited. Service Question 2 establishes
the recovery failure envelope and permits explicit uncertainty when evidence is
insufficient. Shared workspaces are permitted only when explicitly authorized;
no default sharing or interference policy is inferred.

## Service Question 2 — Acceptance and interruption guarantees

**Question:** Once the service acknowledges a task as accepted, what must survive
interruption, which interruptions must it tolerate, and may it report an
explicitly uncertain outcome when it cannot establish whether execution or
effects completed?

**Status:** DECIDED for accepted-work preservation, supported interruptions,
evidence-based recovery, and explicit uncertain outcomes. Retry and uncertainty-
resolution policies remain UNRESOLVED.

**Human answer (2026-09-10, verbatim):**

> Once the service acknowledges a task as accepted, it must preserve enough authoritative task state to ensure that the task does not become silently lost as a result of a supported interruption.
>
> At minimum, the service should preserve information sufficient to determine:
>
> * The identity of the accepted task.
> * The inputs or authoritative references necessary to understand what work was accepted.
> * The current known lifecycle state of the task.
> * Whether execution has been started, completed, failed, or remains unresolved to the degree that this can be established.
> * Any durable result or service-controlled effect that has been successfully established.
> * Any evidence needed to support the task’s reported outcome.
> * Any retry or recovery state necessary to continue safely.
>
> For the first experiment, the service should tolerate ordinary interruption and restart of the service process and recovery of the host environment where persistent service state remains available.
>
> The first experiment does not need to guarantee recovery from permanent loss or corruption of the persistent storage itself, catastrophic loss of the execution environment, or failures outside the explicitly controlled service boundary.
>
> After restart, the service should reconstruct a defensible authoritative view of previously accepted tasks rather than relying upon transient process memory.
>
> The service should not assume that interruption occurs only between clean lifecycle transitions. An interruption may occur while a task is executing or while persistent effects or results are being established.
>
> When the service can determine from durable evidence that execution or an effect completed, it may report that outcome.
>
> When it can determine that execution or an effect did not complete, it may report failure or retry according to the established policy.
>
> When the service cannot reliably determine whether execution or a persistent effect completed, it may and should report an explicitly uncertain outcome rather than incorrectly declaring success or failure.
>
> An uncertain outcome should remain distinguishable from ordinary execution failure. It means that the service lacks sufficient authoritative evidence to determine the result of an interrupted operation.
>
> The existence of an uncertain outcome does not automatically require the task to be retried. The system must consider whether retry could duplicate a persistent effect or otherwise violate the task’s intended semantics.
>
> The architecture should therefore define how uncertain tasks are surfaced, whether they may be automatically retried, when human or caller intervention is required, and what evidence can later resolve the uncertainty.
>
> The first experiment does not require that every accepted task eventually reach either success or failure without ambiguity. It is acceptable for some tasks to remain explicitly unresolved when the system cannot establish the truth safely.
>
> The guiding principles are:
>
> **Acknowledged work must not be silently forgotten.**
>
> and
>
> **When the system cannot establish whether an interrupted action completed, preserving uncertainty is preferable to inventing certainty.**

**Established intent (summary; the answer above governs):**

- Acknowledged tasks must remain accounted for after supported interruptions,
  with sufficient identity, input meaning, known lifecycle state, established
  results/effects, outcome evidence, and retry/recovery information.
- Supported recovery covers ordinary service-process interruption/restart and
  host-environment recovery with persistent service state still available.
  Permanent storage loss/corruption, catastrophic environment loss, and failures
  outside the controlled boundary have no required recovery guarantee.
- Recovery must use durable evidence and cover interruption during execution
  and establishment of effects/results, not only between clean transitions.
- Report established outcomes when evidence supports them. Otherwise preserve
  explicit uncertainty, distinct from ordinary failure.
- Uncertainty does not authorize retry. Accepted tasks may remain unresolved
  when a truthful outcome cannot safely be determined.

**Architectural implications:** Acknowledging acceptance must not precede the
preservation needed to uphold the supported-interruption guarantee. Acknowledged
acceptance is not a promise of successful execution or eventual certain outcome.
Preserving a task as unresolved can satisfy accountability, but uncertainty must
not substitute for an outcome that durable evidence can establish. Service
Question 1's effect-observation requirement is therefore bounded by the supported
failure model and available evidence, rather than an absolute guarantee of
knowing every interrupted effect. A failure report cannot by itself establish
that no partial effects occurred.

**Remaining questions:** Service Question 3 establishes retry authorization
conditions. Handling of partial effects, authority/evidence for resolving
uncertainty, and caller behavior when an acceptance response is interrupted
remain open. No rollback, submission-deduplication, or exactly-once guarantee is
inferred. Recovery verification must include interruptions within operations;
specific test mechanisms remain to be derived later.

## Service Question 3 — Retry and recovery authorization

**Question:** Under what conditions may the service automatically retry failed
or uncertain work, and when should caller or human authorization be required—
especially if persistent effects may already exist?

**Status:** DECIDED for retry safety and authorization principles, decision
information, attributable authorization, and distinctions among recovery actions.
Caller authority and detailed operation policies remain to be established.

**Human answer (2026-09-10, verbatim):**

> The service may automatically retry work only when it can establish that retry is consistent with the task’s defined semantics and will not create an unacceptable duplicate persistent effect.
>
> Automatic retry is appropriate when at least one of the following is true:
>
> * The task is explicitly defined as safely repeatable or idempotent.
> * The prior attempt is known not to have produced any persistent effect.
> * The service can reliably detect and suppress duplicate effects.
> * The task uses a mechanism that allows the service to determine whether the intended effect has already been committed and to avoid applying it again.
> * The failure occurred before execution reached any point capable of producing a persistent effect.
>
> Ordinary transient failures may therefore be retried automatically when the service has sufficient evidence that repeating the task cannot change its meaning or create an unintended additional effect.
>
> Automatic retry should not be based solely on a generic failure classification such as timeout, crash, or lost connection. The service must consider what is known about the execution and its possible effects.
>
> An uncertain outcome requires stronger treatment.
>
> If the service cannot determine whether a persistent effect may already have occurred, the task should not be automatically retried unless the task’s semantics explicitly permit repetition or the service has an established mechanism for preventing duplicate effects.
>
> Where such assurance does not exist, the task should enter an explicit state requiring caller or human decision.
>
> Caller or human authorization should be required when:
>
> * A prior attempt may have produced a persistent effect that cannot be reliably detected.
> * Retrying could create duplicate, conflicting, or otherwise consequential effects.
> * The task’s repeatability or idempotency is unknown.
> * Available evidence about the previous attempt is contradictory or insufficient.
> * Recovery would require changing the task’s original intent or execution semantics.
> * The retry would cross an established trust, security, cost, or operational boundary.
> * An explicit policy requires human approval for the type of effect involved.
>
> The system should clearly present the information needed to make that decision, including:
>
> * What is known about the previous attempt.
> * What remains uncertain.
> * What persistent effects may exist.
> * What could happen if the task is retried.
> * Whether the system can detect or suppress duplicate effects.
> * What recovery options are available.
>
> Caller or human authorization to retry should be explicit and attributable. The system should retain enough information to show that the retry occurred under that authorization.
>
> The service should distinguish between:
>
> * **retrying the same task**, where the original task identity and intent remain authoritative;
> * **resubmitting equivalent work as a new task**, which creates a new unit of accountable work;
> * **continuing an interrupted task**, where execution can safely resume from established durable state;
> * and **reconciling an uncertain task**, where the objective is first to determine what actually happened rather than immediately execute again.
>
> These operations should not be treated as interchangeable.
>
> The first experiment does not require the service to eliminate every possibility of duplicate execution. It does require the service to make the risk explicit and to avoid silently converting uncertainty into authorization to repeat consequential work.
>
> The guiding principle is:
>
> **Retry is an authorization to perform work again, not merely a response to failure.**
>
> Automatic retry is therefore justified only when the service can establish that repeating the work preserves the intended task semantics and does not create an unacceptable duplicate effect.

**Established intent (summary; the answer above governs):**

- Automatic retry requires established semantic safety against unacceptable
  duplicate effects. Supported grounds include defined repeatability, evidence
  of no prior effect, reliable duplicate suppression, established effect-commit
  detection with prevention of reapplication, or failure before effects were
  possible. These are alternative justifications, not mandated mechanisms.
- Generic failure labels alone do not establish retry safety. Uncertain effects
  require permitted repetition or established duplicate prevention; otherwise
  an explicit caller/human decision is required.
- Approval requirements cover uncertain or consequential effects, unknown
  repeatability, contradictory/insufficient evidence, changed intent or
  semantics, crossed boundaries, and explicitly approval-governed effects.
- Present prior-attempt knowledge, uncertainty, possible effects and retry
  consequences, duplicate controls, and recovery options for that decision.
  Authorization must be explicit, attributable, and retained with the retry.
- Retry preserves task identity and intent; resubmission creates new accountable
  work; continuation resumes safely from established durable state;
  reconciliation determines what happened. These are distinct operations.
- Eliminating all duplicate execution is not required. Exposing risk and avoiding
  unsupported repetition of consequential work are required.

**Architectural implications:** Retry safety and permission are separate
conditions: technical repeatability does not override an explicit approval rule
or an established trust boundary. Permission to retry does not prove that the
earlier attempt failed or resolve uncertainty about its effects. A change to
task intent cannot be silently represented as a retry of the same authoritative
intent. Resubmission must not disguise uncertain prior work as resolved. The
service must retain enough attempt attribution and authorization context to
explain repeated execution without replacing the earlier evidence.

**Remaining questions:** Service Question 4 establishes a single trusted human
operator and human-only recovery boundaries. Define handling of an unconfirmed acceptance
response, partial effects, and the evidence/authority needed to resolve an
uncertain outcome. Retry scheduling, limits, cancellation interactions, and which
recovery operations the constrained task model supports remain to be derived or
elicited as appropriate. Forge's absence of initial resource caps does not imply
unlimited service-task retries. No specific retry or effect-control mechanism is
selected here.

## Service Question 4 — Operator and recovery authority

**Question:** Who may submit, inspect, and authorize recovery of tasks in the
first experiment—a single trusted operator, or multiple callers with different
permissions? Which recovery decisions must remain human-only?

**Status:** DECIDED for the single-operator trust model, recovery authority,
decision attribution, and provenance of human-supplied facts. Detailed
cancellation, abandonment, and reconciliation behavior remains to be derived or
elicited where it requires further human intent.

**Human answer (2026-09-10, verbatim):**

> For the first experiment, the service should assume a single trusted human operator.
>
> That operator may:
>
> * Submit tasks.
> * Inspect task state, results, evidence, and uncertainty.
> * Review recovery options.
> * Authorize retries or other recovery actions that require human judgment.
> * Cancel or abandon work when the task semantics and current state permit it.
> * Accept or resolve explicitly uncertain outcomes when sufficient external knowledge is available.
>
> The first experiment does not need to support multiple callers with different roles, permissions, ownership boundaries, or authorization levels. Identity and access-control models involving multiple users should be treated as a later extension.
>
> The service should still preserve attribution for consequential decisions. Even with a single trusted operator, it should remain possible to determine that a recovery, retry, abandonment, or other consequential action occurred because of explicit human authorization rather than autonomous agent choice.
>
> Routine recovery actions may remain autonomous when the previously established retry and recovery rules demonstrate that the action preserves task semantics and cannot create unacceptable duplicate or consequential effects.
>
> Human-only authorization should be required when the service cannot establish that recovery is safe from authoritative information already available to it. This includes situations such as:
>
> * An uncertain task may already have produced a persistent effect that cannot be reliably determined.
> * Retry or continuation could create a duplicate or conflicting persistent effect.
> * The service lacks sufficient evidence to determine which recovery action preserves the original task intent.
> * Available evidence is materially contradictory.
> * Recovery requires changing the original task, its intended effects, or its established execution semantics.
> * A recovery action would cross an established trust, security, resource, or operational boundary.
> * The service proposes abandoning or overriding an unresolved task when doing so could conceal a potentially consequential outcome.
>
> The human should not be required to authorize routine technical recovery solely because an interruption occurred. If the system can establish that an action is safe and consistent with previously authorized task semantics, it may perform that action autonomously.
>
> Human decisions should be based on a clear presentation of:
>
> * The task and its original intent.
> * The last authoritative state known before interruption or failure.
> * What the service knows happened.
> * What remains uncertain.
> * What effects may already exist.
> * The available recovery choices.
> * The potential consequence of each choice.
>
> The service should distinguish human authorization from human assertion of external fact.
>
> For example, the operator might provide information that an effect was independently observed outside the service. That information may help reconcile an uncertain task, but the system should preserve its provenance rather than representing the information as something the service itself observed.
>
> The initial trust model is therefore:
>
> **One trusted operator, broad visibility, explicit authority over consequential recovery decisions, and autonomous recovery only where safety and task semantics are already established.**
>
> A future version may introduce multiple callers, ownership, roles, delegated authority, approval thresholds, or separation of duties, but those capabilities are outside the first experiment.

**Established intent (summary; the answer above governs):**

- One trusted human operator submits and inspects work, reviews recovery choices,
  authorizes consequential recovery, and may cancel, abandon, or resolve uncertain
  work under the stated task-state and knowledge conditions.
- Multiple users, roles, ownership boundaries, permission levels, delegated
  authority, and separation of duties are outside initial scope.
- Consequential actions must remain attributable to explicit human authorization
  or autonomous choice, despite there being only one operator.
- Routine recovery is autonomous when safety and consistency with authorized
  semantics are established. Interruption alone does not create an approval gate.
- Unsafe or insufficiently justified recovery, material contradictions, changed
  intent, boundary crossings, and potentially concealing abandonment require
  human authorization.
- Present intent, last authoritative state, observed facts, uncertainty, possible
  effects, options, and consequences to support human decisions.
- Human-supplied external facts retain their provenance and remain distinct from
  both service observations and human authorization.

**Architectural implications:** Architect authority over engineering decisions
does not delegate the service operator's human-only recovery authority to an
agent. A trusted operator's permission to act does not itself establish what
happened previously. External observations may support reconciliation without
authorizing external task effects otherwise excluded by Service Question 1.
Abandonment cannot erase a potentially consequential unresolved history.

**Remaining questions:** The effect of cancellation and abandonment on active
execution, existing artifacts, and uncertainty; the evidence needed to justify
an outcome change when operator facts conflict with service evidence; and task
workspace interference remain to be specified. Single-operator scope does not
itself decide task concurrency or authorize unrestricted execution.

## Service Question 5 — Interrupted submission and logical task identity

**Question:** If submission is interrupted before the operator receives
acceptance confirmation, should repeating that submission identify the same
task, or may it create a new task? What should the operator be able to determine
before risking duplicate work?

**Status:** DECIDED for stable submission identity, repeated-submission behavior,
acceptance uncertainty, and explicit submission as new work. Identity-conflict
and retention details remain to be derived or elicited as appropriate.

**Human answer (2026-09-10, verbatim):**

> If submission is interrupted before the operator receives confirmation that the task was accepted, repeating the submission should be capable of identifying the same logical task rather than automatically creating a new task.
>
> The operator should not have to choose between risking duplicate work and abandoning a task whose acceptance status is unknown.
>
> For the first experiment, a submission should therefore have a stable identity or equivalent caller-supplied reference that allows the service to determine whether an apparently repeated submission corresponds to:
>
> * a task that was never accepted;
> * a task that was accepted but whose acknowledgement was not received;
> * a task that is currently executing;
> * a task that already completed;
> * or a task whose state is explicitly uncertain.
>
> If the repeated submission identifies the same logical task, the service should not create a second independent unit of work merely because the original acknowledgement was lost.
>
> Before any new execution is authorized, the operator should be able to determine, to the extent supported by authoritative state:
>
> * Whether the original submission was accepted.
> * The identity of the accepted task, if one exists.
> * Whether execution has started.
> * Whether execution completed.
> * Whether persistent effects or results may already exist.
> * Whether retrying, continuing, reconciling, or resubmitting would preserve the original task semantics.
> * What uncertainty remains.
>
> If the service can establish that the original submission was never accepted, the work may be accepted normally.
>
> If the service establishes that the task was already accepted, the repeated submission should resolve to that existing task rather than create duplicate work.
>
> If the service cannot determine whether acceptance occurred, it should preserve that uncertainty rather than silently create a new task whose execution might duplicate the original.
>
> The operator should still be able to intentionally submit equivalent work as a new and distinct task, but that action should be explicit and should result in a new task identity. An intentional resubmission as new work must remain distinguishable from retrying an uncertain submission.
>
> The first experiment does not need a multi-client distributed deduplication model, but it should demonstrate the semantic principle that communication failure around acceptance does not automatically justify creating duplicate work.
>
> The guiding principle is:
>
> **Loss of an acceptance acknowledgement must not convert uncertainty about one task into two independently authorized tasks.**

**Established intent (summary; the answer above governs):**

- Submissions have a stable identity or equivalent caller-supplied reference that
  supports recognition of the same logical task after interrupted communication.
- If previously accepted, repeated submission resolves to existing work without
  creating a second independent task. If demonstrably never accepted, normal
  acceptance may proceed. If acceptance cannot be determined, preserve uncertainty.
- Before new execution authorization, make authoritative acceptance, task
  identity, execution status, possible effects/results, recovery implications,
  and remaining uncertainty available to the operator.
- Intentionally submitting equivalent work as new requires an explicit action
  and a new task identity, distinct from retrying uncertain submission.
- Multi-client distributed deduplication is not an initial requirement.

**Architectural implications:** Logical task identity must remain meaningful
across lost acknowledgements and supported restarts. Recognition of existing
work is not authorization for another execution attempt; Service Question 3's
retry rules still apply. Submission identity and execution-attempt attribution
serve distinct purposes. Missing evidence of acceptance is not automatically
evidence of non-acceptance. Resolving repeated submissions must not silently
replace previously accepted inputs or intent. No protocol, identifier format,
storage technology, or exactly-once execution guarantee is selected here.

**Remaining derivation:** Define how to handle the same submission reference
accompanying materially different work without silently changing task intent,
and preserve enough identity history for the promised submission behavior.
Any proposed identity expiry or reuse that weakens that guarantee requires an
explicit scope decision. Detailed identity-conflict responses and retention
rules are not established by this answer.

## Service Question 6 — Cancellation and abandonment

**Question:** What should cancellation and abandonment mean for queued, running,
or uncertain tasks—particularly for effects already produced and outcomes that
remain unknown?

**Status:** DECIDED for cancellation and abandonment semantics, truthful outcome
reporting, retained history, and exclusion of implicit rollback.

**Human answer (2026-09-10, verbatim):**

> Cancellation and abandonment should have different meanings.
>
> **Cancellation** is a request to prevent further execution of a task, to the extent that the service can still do so safely and honestly.
>
> For a queued task that has not begun execution, cancellation should prevent the task from starting and should result in a terminal state indicating that the task was cancelled before execution.
>
> For a running task, cancellation should be treated as a request to stop further work rather than as proof that execution or effects have ceased. The service should attempt to stop the task when the execution model supports doing so safely, but the reported outcome must reflect what can actually be established.
>
> If a running task has already produced persistent effects, cancellation does not erase or reverse those effects unless reversal is separately defined, authorized, and verified. A task may therefore be cancelled from further execution while retaining evidence that some effects already occurred.
>
> If interruption or cancellation leaves the service unable to determine whether execution or a persistent effect completed, the task should remain explicitly uncertain rather than being reported as successfully cancelled.
>
> Cancellation should therefore not be treated as equivalent to rollback.
>
> **Abandonment** is an explicit decision to stop further attempts to execute, recover, reconcile, or otherwise resolve a task.
>
> Abandonment may be appropriate when:
>
> * Further recovery is not justified.
> * The remaining uncertainty cannot reasonably be resolved.
> * Continuing would create unacceptable risk or cost.
> * The task is no longer needed.
> * The human operator decides that preserving the unresolved state is preferable to additional action.
>
> Abandonment does not change historical facts. It does not imply that the task failed, that it never executed, or that no effects exist.
>
> An abandoned task should retain:
>
> * Its original identity and intent.
> * Its last authoritative state.
> * Known execution history.
> * Known persistent effects or results.
> * Any unresolved uncertainty.
> * The fact that abandonment was explicitly authorized.
> * The reason for abandonment when provided.
>
> For an uncertain task, abandonment should allow the system to reach a terminal administrative state without falsely resolving the operational uncertainty. The system should therefore be capable of expressing a state equivalent to:
>
> **Abandoned with outcome unresolved.**
>
> The operator should be able to distinguish among:
>
> * Cancelled before execution.
> * Cancellation requested while running.
> * Cancelled after partial execution.
> * Completed before cancellation took effect.
> * Uncertain following attempted cancellation.
> * Abandoned with known outcome.
> * Abandoned with unresolved outcome.
>
> The service does not need to guarantee rollback of persistent effects for the first experiment. If compensation or reversal is later supported, those actions should be treated as separate accountable operations rather than implied consequences of cancellation.
>
> The guiding principles are:
>
> **Cancellation governs future execution; it does not rewrite the past.**
>
> and
>
> **Abandonment closes the obligation to keep working on a task, but it does not manufacture certainty about what happened.**

**Established intent (summary; the answer above governs):**

- Cancellation of queued, not-yet-started work prevents execution and produces a
  terminal cancelled-before-execution outcome.
- Cancellation during execution is a stop request, not proof of stopping. Attempt
  safe stopping where supported, and report what evidence actually establishes.
- Existing effects survive cancellation unless separately defined, authorized,
  and verified reversal occurs. Uncertain execution/effects must remain uncertain.
- Abandonment explicitly ends further execution, recovery, reconciliation, or
  resolution efforts, without altering historical facts or inventing an outcome.
- Retain identity, intent, last authoritative state, execution history, effects,
  results, uncertainty, explicit authorization, and any provided abandonment reason.
- Administrative terminality may coexist with operational uncertainty. The seven
  listed cancellation/abandonment situations must be distinguishable to the operator.
- Rollback is not required. Any later compensation or reversal is a separate
  accountable operation.

**Architectural implications:** Execution outcome, pending control requests, and
administrative closure cannot be treated as interchangeable facts. A late stop
request cannot turn demonstrated completion into non-execution. Abandonment
does not establish that a running task stopped; reporting must remain truthful
about any execution or effects whose cessation is not established. Distinct
observable meanings are required, but no state representation or stopping
mechanism is selected here.

**Remaining derivation:** Define acceptance criteria for cancellation around
execution start, completion, partial effects, and interruption, and for abandoned
tasks retaining unresolved history. Any proposed reopening or further execution
of abandoned work would require explicit semantics; it is not inferred here.

## Service Question 7 — Sequential execution and stable inputs

**Question:** Should the service execute tasks sequentially or concurrently,
are ordering guarantees required, and may the operator modify task inputs or
workspaces while work is active?

**Status:** DECIDED for sequential execution, observable ordering, stable accepted
inputs, and controlled handling of workspace changes. Scheduling and validation
details remain architectural derivation within these constraints.

**Human answer (2026-09-10, verbatim):**

> For the first experiment, the service should execute tasks sequentially.
>
> The purpose of the initial experiment is to exercise task identity, lifecycle, durability, recovery, uncertainty, retry, cancellation, and evidence. Concurrent execution is not required to demonstrate those behaviors and would introduce additional scheduling and consistency concerns that are better deferred.
>
> Tasks should therefore begin execution one at a time according to a defined service policy.
>
> The service should provide enough ordering information for the operator to understand the relationship among accepted tasks and executions. However, the first experiment does not require a strong general-purpose ordering model beyond what is necessary to make behavior deterministic and observable.
>
> In particular:
>
> * Acceptance order should be observable.
> * Execution order should be observable.
> * The service should not imply that acceptance order and execution order are necessarily identical unless that guarantee is explicitly established.
> * Recovery, retry, cancellation, or operator intervention may legitimately affect which task executes next.
> * If the service provides a deterministic scheduling rule for the first experiment, deviations from that rule should be attributable to explicit lifecycle events or operator decisions.
>
> Concurrent execution, task priorities, dependency scheduling, fairness policies, distributed ordering, and parallel worker coordination are outside the initial scope.
>
> Task inputs that define the accepted work should become stable once the task has been acknowledged as accepted.
>
> The operator should not be able to silently modify an accepted task's authoritative inputs while preserving the appearance that it is still the same task. If different inputs are desired, that should ordinarily constitute new work with a distinct task identity or an explicit, traceable replacement operation defined by the architecture.
>
> Likewise, a task's execution workspace should not be subject to uncontrolled modification while the task is active.
>
> The service should distinguish between:
>
> * immutable or otherwise authoritative task inputs;
> * service-controlled working state created during execution;
> * output artifacts produced by the task;
> * and external human modifications.
>
> If an operator or external process changes information on which an active task depends, the service should not silently continue as though the original execution context remains valid.
>
> Depending upon what changed and when it changed, the service should either:
>
> * detect that the change does not affect the active task;
> * prevent the modification;
> * invalidate or stop affected execution;
> * mark the task or result as requiring reconciliation;
> * or require explicit operator action before dependent work continues.
>
> The first experiment does not need to support collaborative live editing of active task workspaces.
>
> Where practical, the execution of a task should be attributable to a stable set of authoritative inputs so that the resulting output and evidence can be understood in relation to what was actually accepted.
>
> The service should not represent a result as the outcome of one set of inputs when execution may have depended upon materially different inputs introduced during processing.
>
> The guiding principles are:
>
> **Keep execution sequential until concurrency is needed to prove something important.**
>
> and
>
> **Once work is accepted, its authoritative meaning should not change invisibly while it is being executed.**

**Established intent (summary; the answer above governs):**

- Task execution is sequential under a defined service policy. Concurrency,
  priorities, dependency scheduling, fairness policies, distributed ordering,
  and parallel worker coordination are outside initial scope.
- Acceptance and execution order must be observable, without implying they are
  identical. Recovery, retry, cancellation, or operator decisions may affect
  which task executes next; deviations from a deterministic rule are attributable.
- Accepted authoritative inputs remain stable. Different inputs ordinarily mean
  new work, or an explicitly defined and traceable replacement; no silent mutation
  may preserve the appearance of unchanged task intent.
- Distinguish authoritative inputs, service working state, task outputs, and
  external modifications. Active workspaces must not undergo uncontrolled changes.
- Relevant changes require prevention, demonstrated irrelevance, invalidation or
  stopping, reconciliation, or explicit operator action as appropriate. Outputs
  must not be misattributed to inputs that may differ materially from those used.
- Collaborative live editing is not an initial requirement.

**Architectural implications:** Sequential execution constrains actual task
activity, not just the order in which starts are requested. After interruption
or attempted cancellation, uncertainty about whether an earlier execution is
still active must be considered before starting another task. An unresolved
historical outcome does not by itself prove that execution remains active;
execution cessation and effect certainty are separate facts. Stable input
meaning and provenance must survive retries and supported restart. A mutable
input reference alone cannot justify assuming the accepted content is unchanged.
No scheduling algorithm, storage format, isolation mechanism, or input-capture
technology is selected here.

**Remaining derivation:** Establish an observable scheduling rule and its
lifecycle exceptions, criteria for safely starting subsequent work, and checks
for meaningful input/workspace change. Define same-identity/different-input
handling consistently with Service Question 5. A replacement operation is
permitted as an explicitly defined alternative, not required by this answer.
Escalate any proposed weakening of stable-input or sequential-execution guarantees.

## Service Question 8 — Evidence and resolution of uncertainty

**Question:** What evidence should permit an uncertain outcome to become resolved,
and how should the service handle an operator's account that conflicts with its
recorded evidence?

**Status:** DECIDED for evidence adequacy, provenance, conflict handling, and the
distinction between factual resolution and administrative human decisions.

**Human answer (2026-09-10, verbatim):**

> An uncertain outcome may become resolved when new evidence provides sufficient confidence to establish what actually occurred.
>
> Potential resolving evidence may include:
>
> * Durable service records created before or during the interrupted execution.
> * Verified output artifacts attributable to the task.
> * Persistent effect records that can be reliably associated with the task.
> * Execution logs, checkpoints, or completion markers whose integrity and provenance are sufficient for the decision.
> * Reconciliation with the controlled execution workspace.
> * Independent observation of an expected effect when that observation can be reliably tied to the task.
> * Explicit operator-supplied facts based on information available outside the service.
>
> The service should not require one specific type of evidence in every case. Evidence adequacy should depend upon the claim being resolved and the consequences of being wrong.
>
> For example, evidence sufficient to conclude that a harmless computation completed may be weaker than evidence required to conclude that a persistent consequential effect was committed exactly once.
>
> An uncertain task should be resolved only when the available evidence supports a defensible conclusion about its outcome. Resolution should identify:
>
> * The conclusion reached.
> * The evidence supporting it.
> * The provenance of that evidence.
> * Any remaining uncertainty.
> * Who or what authorized the resolution when judgment was required.
>
> The system should distinguish between evidence it directly observed and information supplied by the operator.
>
> An operator may provide external knowledge that the service could not independently observe. For example, the operator may confirm that a particular output or effect exists based on an external inspection.
>
> Such information may be used in reconciliation, but it should retain its provenance as a human-supplied fact rather than being represented as a direct service observation.
>
> An operator statement should not automatically overwrite conflicting recorded evidence.
>
> When operator-supplied information conflicts with existing service evidence, the system should:
>
> * Make the conflict explicit.
> * Preserve both sources and their provenance.
> * Determine whether the apparent conflict can be explained by differences in timing, scope, identity, or interpretation.
> * Assess the reliability and relevance of each source to the specific claim being resolved.
> * Avoid silently rewriting or discarding historical evidence.
> * Escalate for human judgment when the conflict cannot be resolved from established evidence and authority rules.
>
> The trusted operator may ultimately authorize a resolution when the available evidence remains conflicting or incomplete, but the resulting record should distinguish between:
>
> * an outcome established by service evidence;
> * an outcome established through external human-provided evidence;
> * and an administrative human decision made despite unresolved factual uncertainty.
>
> Human authority to decide what the service should do next does not necessarily establish what objectively happened in the past.
>
> For example, an operator may decide to abandon an uncertain task even though its execution outcome remains unknown. The administrative disposition is then authoritative, while the historical execution outcome remains unresolved.
>
> Likewise, an operator should not be able to convert contradictory evidence into false certainty merely by asserting a preferred interpretation. Where uncertainty remains material, the system should preserve that uncertainty.
>
> The first experiment does not require a formal probabilistic evidence model. It is sufficient that the architecture define clear evidence provenance, reconciliation rules, and conditions under which an uncertain outcome may be considered resolved.
>
> The guiding principles are:
>
> **Uncertainty should be resolved by evidence, not erased by preference.**
>
> and
>
> **Human authority governs decisions, but human authority does not automatically rewrite historical fact.**

**Established intent (summary; the answer above governs):**

- Resolve an uncertain outcome only when evidence supports a defensible conclusion.
  Evidence adequacy depends on the claim and consequences of error, without a
  universal evidence type or required formal probabilistic model.
- Record conclusion, supporting evidence, provenance, remaining uncertainty, and
  authorization where judgment was required.
- Distinguish service-observed evidence from operator-supplied facts. Both can
  contribute, but neither source's mere presence automatically resolves a conflict.
- Preserve conflicting sources; assess timing, scope, identity, interpretation,
  reliability, and relevance. Escalate conflicts not resolvable under established
  evidence and authority rules. Do not silently overwrite historical evidence.
- Distinguish service-evidenced outcomes, externally evidenced outcomes, and
  administrative human decisions made with unresolved factual uncertainty.
- Human authority may determine subsequent action without establishing past fact.
  Material uncertainty survives a preferred interpretation or administrative closure.

**Architectural implications:** Reconciliation must be scoped to the actual claim
supported by the evidence. Evidence that an artifact exists does not necessarily
establish its task attribution or whether an effect occurred only once. These
examples do not introduce an exactly-once service guarantee. Administrative
resolution cannot be presented as factual success or failure when the evidence
does not support it. A traceable correction may change a current conclusion while
preserving the historical evidence and rationale that led to the earlier view.

**Remaining derivation:** Establish claim-specific evidence and reconciliation
acceptance criteria for the constrained demonstration tasks, including conflicting
operator and service accounts. No scoring model, universal evidence hierarchy,
technology, or implementation work is selected here.

## Experiment evaluation clarification — Human intervention evidence

**Question:** To assess “substantially less continuous human direction,” is a
recorded intervention history plus a reasoned comparison with a manual workflow
sufficient, or must the experiment include a measured manual comparison?

**Status:** DECIDED for the initial comparison method, intervention evidence,
classification principles, and human authority over the comparative assessment.

**Human answer (2026-09-10, verbatim):**

> For the first experiment, a recorded history of human interventions together with a reasoned comparison against the expected manual Architect/Codex workflow is sufficient to assess whether KGE Forge required substantially less continuous human direction.
>
> A separate measured manual control run is not required for the initial experiment.
>
> The experiment should record each meaningful human intervention, including:
>
> * When the intervention occurred.
> * What triggered it.
> * Whether the intervention supplied human intent, resolved a consequential tradeoff, corrected architectural misunderstanding, repaired implementation drift, or provided routine engineering direction.
> * Whether the intervention could reasonably have been avoided by a better architecture, better knowledge capture, better context management, or better agent behavior.
> * Whether subsequent work was able to proceed autonomously after the intervention.
>
> The assessment should distinguish between desirable human participation and undesirable continuous direction.
>
> Human involvement should not count against the experiment when it concerns matters that properly remain under human authority, such as:
>
> * Clarifying vision or intent.
> * Resolving genuinely consequential tradeoffs.
> * Approving material changes to the intended system.
> * Accepting the final engineered result.
>
> Human involvement should count as evidence against the intended autonomy when the human repeatedly must:
>
> * Decompose routine engineering work.
> * Rewrite implementation prompts.
> * Remind the Architect of previously established knowledge.
> * Detect architectural drift that the system should have detected.
> * Explain ordinary implementation details.
> * Manually coordinate Architect and Implementation Agent activity.
> * Re-establish project state after interruption.
> * Supply information that was already available in authoritative project artifacts.
>
> At completion, the human should make a reasoned assessment of whether the amount and character of intervention were substantially lower than would normally be required when manually directing Codex through an equivalent project.
>
> The experiment should preserve enough evidence to support that assessment rather than relying only on retrospective impression.
>
> A future experiment may use a measured manual comparison, such as implementing comparable systems with and without KGE Forge and comparing intervention count, intervention type, elapsed effort, rework, and outcome quality. Such a controlled comparison would be valuable after the initial methodology has demonstrated basic viability.
>
> For Experiment 1, the objective is to establish a baseline of actual Forge behavior and human intervention patterns that can later support more rigorous comparative evaluation.
>
> The guiding principle is:
>
> **The first experiment should measure where and why the human was needed before attempting to optimize or formally benchmark how much the human was needed.**

**Established intent (summary; the answer above governs):**

- An intervention history and reasoned comparison against the expected manual
  Architect/Codex workflow suffice. A separate measured manual control is not
  required in Experiment 1.
- Record meaningful interventions with timing, trigger, type, assessable
  avoidability, and whether subsequent work proceeded autonomously.
- Intent clarification, consequential human tradeoffs/approvals, and final
  acceptance are appropriate human participation, not evidence against autonomy.
- Repeated routine direction, prompt repair, reminders, human-detected drift,
  manual coordination, state reconstruction, or resupplying persisted knowledge
  count as evidence against intended autonomy.
- The human makes the final reasoned comparative assessment using preserved
  evidence. Actual Forge behavior provides a basis for later controlled studies.

**Architectural implications:** Intervention count alone cannot establish success
or failure. An agent may classify and analyze interventions, but must preserve
the evidence and distinguish its interpretation from human judgment. Avoidability
and autonomous continuation require support; an unanswered or unobserved outcome
must not be recorded as successful autonomous progress. The Architect's technical
completion assessment is distinct from the human's comparative autonomy assessment.
No causal or quantitative improvement claim is established by this evaluation
method alone. This clarification supplies experimental intent and is not itself
evidence of a failure of autonomy.

**Record limitations:** Existing elicitation answers preserve human intent and
their prompting questions, but are not yet a complete intervention history.
Exact historical timestamps, effort, avoidability, and subsequent autonomy must
not be invented where not available. The intervention record must expose those
limits and capture meaningful interventions as the experiment proceeds.

**Subsequent record:** [EXPERIMENT_1_HUMAN_INTERVENTIONS.md](EXPERIMENT_1_HUMAN_INTERVENTIONS.md)
now provides a retrospective intervention ledger through the environment
clarification, with missing timestamps and unobserved engineering outcomes explicit.

## Environment clarification — Separate repositories on one Linux host

**Question:** Which repository and development environment should contain the
demonstration service, and what external information destinations, if any, are
approved?

**Status:** DECIDED for repository separation, initial host colocation, knowledge
ownership, and permitted communication boundaries. The demonstration repository's
name and path remain setup details; no repository has been created by this record.

**Human answer (2026-09-10, verbatim):**

> The demonstration service should be implemented in a separate repository from KGE Forge itself.
>
> KGE Forge should remain the engineering environment and authoritative process repository. The demonstration service should have its own repository so that the experiment can clearly distinguish:
>
> * the system performing the engineering;
> * the system being engineered;
> * Forge project knowledge and evidence;
> * implementation artifacts belonging to the demonstration service.
>
> For the first experiment, the demonstration repository should be hosted on the same Linux development environment as KGE Forge unless there is a compelling reason to separate them.
>
> Keeping both repositories on the same Linux host is preferred initially because it minimizes communication, filesystem, authentication, and cross-platform complexity while still preserving a clear repository boundary.
>
> A suitable structure would conceptually be:
>
> KGE Forge repository
>
> * Vision and architecture of Forge
> * Experiment records
> * Human intervention history
> * Work packages
> * Architect assessments
> * Forge-level evidence
>
> Demonstration service repository
>
> * Service source code
> * Service-specific architecture and requirements derived through Forge
> * Tests
> * Build artifacts
> * Service-specific verification evidence
>
> The first experiment should not require external information destinations.
>
> Agents may access information contained in the two designated repositories and normal development tooling needed to build and verify the demonstration service.
>
> Project information should not be automatically transmitted to unrelated external systems, repositories, collaboration tools, cloud storage, or other destinations.
>
> Communication with the AI services required to operate the Architect and Implementation Agent is implicitly permitted as part of the experiment, subject to the previously established project trust boundary.
>
> No additional external publication, deployment, telemetry destination, issue tracker, document repository, or data service is required for the first experiment.
>
> If an external destination later becomes useful, such as a remote Git repository, artifact store, or deployment environment, it should be explicitly introduced and authorized rather than assumed.
>
> The guiding principle is:
>
> **Keep Forge and the engineered system separate, but colocate them initially to minimize experimental complexity.**

**Established intent (summary; the answer above governs):**

- Forge remains the engineering environment and authoritative process repository.
  The demonstration service has a separate repository on the same Linux host
  initially, unless a compelling reason for separation is established.
- Forge holds its vision/architecture, experiment and intervention records, work
  packages, assessments, and Forge-level evidence. The service repository holds
  service implementation, service architecture/requirements, tests, build
  artifacts, and service verification evidence.
- Access to both designated repositories and normal development tooling is
  permitted within the established trust boundary.
- Necessary Architect/Implementation Agent AI-service communication is permitted.
  No other external information destinations are required or implicitly approved.
  New publication, deployment, telemetry, remote repository, or storage destinations
  must be explicitly introduced and authorized.

**Architectural implications:** One active project may span the engineering and
engineered-system repositories without becoming multi-project operation. Their
knowledge and evidence must remain attributable to the correct system. Work and
review must retain enough provenance to connect governing Forge knowledge with
the relevant service state; independent repository histories do not automatically
provide that connection. Shared host access does not grant tasks access to Forge
records or unrestricted host resources. Permission for engineering agents to use
AI services does not grant demonstration tasks arbitrary external-service access.

**Record placement:** Service-specific material recorded here is elicitation
evidence in the Forge process repository. Its later authoritative service
requirements belong in the service repository with traceability to these human
answers; this record does not silently establish competing authoritative copies.

**Current scope:** Repository name/path selection and creation are deferred to
authorized setup. No remote repository, new external destination, implementation,
or technology selection is authorized by this clarification alone.

## Historical readiness assessment — after environment clarification and synthesis

This assessment updates the earlier baseline-impact notes; it does not erase
their historical context.

**Not yet ready for an architectural baseline.** All eight initial elicitation
questions now have substantive human answers. The principal governance policies
and the demonstration objective are established. This resolves the experiment-
selection blocker. Eight service-specific answers now provide sufficient intent
for behavioral requirements synthesis; a reviewed baseline has not yet been
established. Service Question 1 establishes
bounded computational/file-oriented tasks and attributable controlled effects.
Service Question 2 now establishes durable accountability for acknowledged work,
the supported interruption boundary, and explicitly uncertain outcomes.
Service Question 3 now establishes when automatic retry is justified, when
explicit authorization is required, and distinct recovery-action meanings.
Service Question 4 establishes a single trusted human operator, human-only
recovery boundaries, and provenance for externally supplied facts.
Service Question 5 establishes stable submission identity and prevention of
duplicate independent work caused solely by a lost acceptance acknowledgement.
Service Question 6 establishes cancellation and abandonment semantics, including
administrative closure with an unresolved outcome and no implied rollback.
Service Question 7 establishes sequential task execution, observable ordering,
stable accepted inputs, and explicit treatment of workspace changes.
Service Question 8 establishes evidence-based outcome resolution, preservation
of conflicting sources, and administrative decisions distinct from factual truth.

**Remaining work, prioritized by architectural impact:**

1. **Architectural formulation and review:** The requirements synthesis and
   adversarial requirements review in
   [EXPERIMENT_1_REQUIREMENTS_SYNTHESIS.md](EXPERIMENT_1_REQUIREMENTS_SYNTHESIS.md)
   consolidate the behavioral obligations and expose remaining architecture
   obligations. Formulate and review the architecture before declaring a baseline.
2. **Experimental evidence:** Preserve meaningful interventions with their
   context and limitations; do not equate this answer log with a complete record
   of engineering autonomy. The comparative assessment remains human judgment.

The environment clarification resolves the repository and communication policy:
separate repositories, initially on the same Linux host, with necessary AI-service
communication permitted and no additional external destinations presumed.
The service repository's concrete name/path remains an authorized-setup detail,
not a reason for another architectural-intent question.

The evaluation method is now established in the clarification above. The human
assesses comparative autonomy using recorded interventions and a reasoned manual-
workflow comparison; a measured manual control run is not required. Remaining
work includes making intervention capture reviewable and deriving verification
obligations, not asking the human to invent a numerical success threshold.

See [ARCHITECTURE_GAP_ANALYSIS.md](ARCHITECTURE_GAP_ANALYSIS.md) for the
consolidated assessment following this elicitation round.

Further interface features are not presumed necessary to complete elicitation.
Derive observable requirements from the already established operator actions and
evidence obligations before asking for more detail. Scheduling, state
representation, and evidence mechanisms must not be shifted to the human as
implementation-design questions. Technology selection remains outside this phase.

**Next architectural derivation:** Using that scope and the recorded answers,
derive testable acceptance criteria for both the engineered result and Forge's
process, including the manual-workflow comparison, continuity across increments,
human edits, interruption/resumption, context failures, and auditability. Keep
process-level recovery distinct from the service's task-recovery obligations.
The Architect's evidence-backed completion assessment and presentation for human
acceptance are now established; human acceptance is not presumed in advance.

**Other tracked questions:** Logging timing, the post-completion retention
endpoint, and action-specific authorization uncertainties remain visible. They
do not justify inventing defaults or demanding arbitrary quantitative budgets.
Future parallelism, distribution, and fully unattended operation are excluded
from initial requirements and do not block the initial baseline.

Material findings must be reconciled through architecture review before a
baseline is established. No implementation work or technology selection is
authorized by this record.

## Architecture formulation instruction and current disposition

**Human instruction (2026-09-10, verbatim):**

> Proceed with architectural formulation for Experiment 1 using the authoritative Vision, elicitation record, requirements synthesis, and gap analysis. Derive the architecture necessary to satisfy those requirements. Then perform the required adversarial architecture review and reconcile its findings. Do not issue implementation work until the Architecture Readiness Review determines that the baseline is ready.

**Status:** DECIDED — architectural formulation, adversarial review and
reconciliation are authorized; implementation issuance is gated by readiness.

**Architect disposition:** Formulated E1-ARCH-1, reconciled seven material review
findings, and established architectural readiness in
[EXPERIMENT_1_ARCHITECTURE_READINESS_REVIEW.md](EXPERIMENT_1_ARCHITECTURE_READINESS_REVIEW.md).
No new human intent decision was needed. This supersedes the historical readiness
assessment above without changing the human answers. Runtime verification and
operational dispatch prerequisites remain explicit and unverified. No implementation
package has been issued.
