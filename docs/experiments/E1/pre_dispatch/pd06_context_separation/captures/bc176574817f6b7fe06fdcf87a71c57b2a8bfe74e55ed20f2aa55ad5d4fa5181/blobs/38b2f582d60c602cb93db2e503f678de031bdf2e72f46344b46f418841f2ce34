# Service architecture module — E1-SVC-1

Source: Forge baseline E1-ARCH-1, commit `411cb5a9fabc71e482a414ed58387de0ff557e93`.
Local source repository: `/home/gvasend/app/kge-forge`.
The original human answers and frozen source remain retrievable at that commit.

Status: Active service-owned module of reviewed baseline E1-ARCH-1.
Sections 6–13 below are extracted without semantic changes; original section
numbers are retained for review traceability. The integrated architecture and
its constraints remain governing source; this publication is not a new baseline.
The service cannot acquire Forge permissions by sharing its Linux host.
Changes require Architect impact assessment and the applicable human authority.

## 6. Task-service responsibilities and trust boundary

The runtime has five logical responsibilities:

1. **Operator command boundary:** validate commands, stable identities, expected
   state and authority; provide task/evidence/recovery views.
2. **Control owner:** serialize lifecycle decisions, scheduling, attempt permission,
   cancellation and administrative decisions.
3. **Task ledger:** durable authoritative records and ordered, inspectable history.
4. **Constrained executor and effect controller:** run admitted task definitions
   in bounded steps; access only accepted inputs and owned workspace capabilities.
5. **Recovery and evidence evaluator:** reconstruct accepted work, inspect owned
   material, derive claims, or preserve/escalate uncertainty.

The service is one process lifetime with one active execution, although operator
requests remain serviceable at bounded execution checkpoints. Approved task
definitions expose finite steps and typed inputs, not arbitrary commands, plugins,
scripts, process creation, network access, or host paths. Initial task families
are bounded computation over supplied data and bounded file-data transformation
into owned artifacts. They exercise both replay-safe and decision-required
recovery profiles; no unrestricted workload is required.

All file access is mediated by the service using task/attempt-scoped object
identities, not caller-provided unrestricted paths. Reject traversal, links or
aliases escaping ownership, references to Forge/service source authority, and
cross-task mutable sharing. The initial architecture selects isolated task-owned
workspaces instead of the optionally permitted shared workspace alternative.
Normal tooling permission belongs to engineering agents, not runtime tasks.

Only the control owner can publish authoritative outcomes or issue effect
permission. The constrained executor cannot write the ledger or change accepted
inputs. The operator interface is local to the trusted operator boundary; no
public or remote interface is required. A compromised privileged host is outside
the promised boundary, but ordinary operator edits and changed artifacts are
detected or rendered irrelevant by immutable captured inputs.

## 7. Persistent task concepts

| Record | Meaning and required associations |
|---|---|
| Submission | Stable operator reference, canonical accepted specification identity, acceptance sequence, task identity. |
| Task specification | Versioned task definition, captured input content identities, requested result meaning, allowed effects, repeatability/recovery profile, finite execution bounds, finite attempt allowance. |
| Attempt | Task identity, distinct attempt identity, execution request order, authorization basis, accepted input/definition versions, start/stop knowledge, progress, effect intents and evidence. |
| Effect | Owner task/attempt, operation meaning, target owned object, intent, observed/committed material identity, integrity evidence, possible partial state. |
| Outcome claim | Claim scope, supported conclusion, evidence/provenance, remaining uncertainty, evaluator and any required human judgment. |
| Operator decision | Explicit action/decision identity, task/attempt and state basis, known risks, scope, human attribution, and disposition. |
| Control history | Acceptance, eligibility, dispatch, cancellation, retries, reconciliation, abandonment and their order/causes. |

Progress reports are observations, not authoritative completion. The query view
distinguishes execution knowledge (not started, executing, stopped with supported
outcome, or uncertain), outcome (success, failure, cancelled, unresolved), pending
control request, and administrative disposition (open or abandoned). These are
semantic dimensions, not a prescribed schema. A task with an unresolved attempt
does not become certainly successful merely because a later attempt succeeds.

## 8. Durability and acknowledgement contract

The task ledger supports serialized, all-or-none durable state transitions with
an unambiguous committed boundary after crash. A successful acknowledgement may
be sent only after all required records and referenced input material are durable.
It is the implementation's obligation to select storage primitives that satisfy
this contract; a successful buffered write alone is insufficient.

Torn or incomplete writes caused by supported interruption must recover as the
prior committed state or the new complete state. This is not excluded as
"storage corruption." Genuine permanent media corruption/loss is outside the
guarantee; detected inability to establish store integrity enters recovery-required
mode and cannot be interpreted as an empty history.

Artifact bytes are stored and verified before ledger records refer to them as
durable. This does not require an atomic transaction across metadata and every
file: unreferenced or partially staged material remains owned recovery evidence,
while only verified referenced material supports a committed result claim.
Write failure, full storage, or uncertain commit suppresses success acknowledgement
and further dependent effects until the outcome is inspected. Existing accepted
work remains accounted for; admission rejection is explicit.

There is no automatic garbage collection or identity expiry during Experiment 1
and its review period. Temporary material may be removed only after proving it
is not needed for a decision, unresolved issue, result, or evaluation. Exhausted
capacity suspends admission/work rather than deleting evidence to make room.

## 9. Submission and input stability

The operator supplies a stable submission reference before the first submission.
Validation resolves a task definition and captures inputs into service-owned
immutable content, verifies their integrity, and forms a canonical specification.
Parameters, input content, definition version, effect semantics, and retry policy
participate in identity comparison; incidental request timing does not.

Acceptance atomically associates reference, specification, task identity and order.
For an existing reference: an equivalent specification returns the existing task
without an execution side effect; different work returns IDENTITY_CONFLICT with
the existing task intact. No in-place replacement operation is provided in E1.
The operator may explicitly submit different/equivalent work under a new identity.

For an absent reference in a verified complete authoritative ledger, accept normally.
If ledger completeness or identity is uncertain, return ACCEPTANCE_UNCERTAIN and
do not create work. Lost reply after committed acceptance is resolved by repeated
submission/query. Staged input without a committed acceptance record is not an
accepted task and cannot execute.

Imported source files must be captured consistently or rejected for unstable
input; the accepted object is the captured data shown to the operator, not a
promise that a subsequently mutable source path remains unchanged. Execution uses
the captured content. Integrity is checked before execution and publication;
changed owned input/workspace evidence invalidates affected claims and triggers
reconciliation. Earlier valid observations remain historical evidence, not proof
of the current artifact's integrity.

Execution reads verified private material whose content identity matches the
accepted specification, not a live mutable path checked only before and after
use. For larger bounded inputs, every consumed segment must be verified against
the captured content manifest before use. Owned intermediate artifacts have
explicit expected content/progress identities. A change that affects bytes
actually consumed invalidates the result claim; restoring the old file later
does not repair that evidence. This requirement covers the time between checks,
without promising protection against a malicious privileged host.

## 10. Scheduling, execution, and effect protocol

Eligible execution requests carry a durable increasing order. Select the oldest
eligible request after accounting for cancellation, abandonment, blocked recovery,
and explicit authorized retry/continuation. New retries enter the eligible order
at the tail, not at their original acceptance position. Record eligibility and
dispatch causes. There is no priority, dependency, or fairness subsystem.

Before starting, verify exclusive service ownership, absence of active execution,
open disposition, no cancellation prohibition, valid inputs/definition, attempt
allowance, authority, and known-safe or explicitly authorized effect risk. Persist
the new attempt and authorization before executing a step. The accepted task
declares positive finite work bounds and attempt allowance; missing or unsupported
bounds are rejected at admission rather than filled with an arbitrary promise.

The allowance includes the initial execution grant and each new retry or recovered
continuation grant. A reserved grant is retained after interruption even if actual
execution cannot be established. Same-command replay returns that grant instead
of allocating another. Continuation must advance validated durable progress and
remain within the accepted work bounds; it cannot reset those bounds indefinitely.

For each persistent effect:

1. Persist the effect intent and owned target identity under the attempt.
2. Perform the bounded operation inside the attempt workspace.
3. Verify resulting bytes and meaning against the declared task operation; preserve
   partial artifacts and their attribution if verification cannot finish.
4. Publish established artifact/effect references through a durable ledger
   transition. Publication is the service's committed-result boundary; physical
   staged bytes still count as possible effects and evidence.
5. Report task success only when its defined result criteria, all relevant effects,
   input validity, and execution completion have supported durable claims.

The controller does not permit a task to bypass this protocol. Reconciliation
examines intent records and owned artifacts after interruption. Missing completion
does not prove non-execution; staged artifacts do not alone prove intended result
completion. An uncertain effect can remain unresolved even though the execution
has certainly stopped.

Before issuing each new effect permission, check that accepted inputs, authority,
control requests and the recovery evidence basis remain applicable. A newly
recorded material contradiction or invalidating workspace change suspends further
dependent steps for reconciliation; it does not undo effects already started.
The serialized controller orders that change against effect permission. If a
change arrives after permission and during the operation, retain the actual effect
evidence/uncertainty and do not authorize the next operation on the stale basis.

## 11. Recovery and execution ownership

Only one service owner may control the persistent state and active executor.
Ownership is tied to live process lifetime, not a stale PID file or expiring lease.
The executor cannot outlive the service process because detached task processes
and external workers are not admitted. A second instance that cannot establish
exclusive ownership cannot execute tasks or mutate authority.

Recovery precedes new execution:

1. Establish sole ownership and that no previous execution remains active; if
   uncertain, suspend execution globally while allowing safe inspection.
2. Recover the ledger's committed boundary and verify referenced identities.
3. Reconstruct accepted tasks, attempts, controls, and pending decisions.
4. Inspect recorded effects and attributable workspace material; evaluate claims.
5. Record supported outcomes or explicit uncertainty. Re-evaluate retry authority,
   cancellation and abandonment before enqueuing any execution.

No transparent resume of an arbitrary interrupted instruction is provided. Safe
continuation is allowed only at a task-definition-declared durable checkpoint
whose inputs, progress and effects can be validated. Otherwise reconcile and use
the retry decision path. If the initial admitted task definitions have no such
checkpoint, continuation is reported as unavailable rather than treated as retry.

## 12. Retry, cancellation, and abandonment

Automatic retry needs both a permitted policy and evidence of semantic safety:
approved repeatability, proved absence of effects, or verified prevention of
duplicate effects. A task-definition profile supplies the meaning; a caller flag
alone cannot declare an arbitrary operation idempotent. Existing partial effects
and every unresolved prior attempt participate in the assessment. A finite
attempt budget limits frequency, not risk. Once exhausted, stop further execution
and present status/options; do not invent a factual failure for uncertain work.

Decision-required recovery presents intent, last state, observed facts, uncertainty,
possible effects, options and consequences. Human approval is explicit and bound
to that basis. Changed evidence or scope requires reassessment; no blanket approval
permits new external effects or modified intent. New intent requires a new task,
with lineage to prior work if appropriate. Continuing, retrying, and inspecting
for reconciliation are separate commands and histories.

Control decisions are serialized with dispatch/publication. A cancellation that
is accepted before the first execution prevents dispatch and records cancelled-
before-execution. Cancelling a queued retry inhibits the future attempt but retains
all prior attempt outcomes and effects; it cannot claim the task never executed.
If execution started first, persist cancellation-requested, inhibit
additional task steps at the next safe checkpoint, and determine actual outcome.
Published completion before cancellation remains completion. Partial effects
remain attributed. Unknown cessation/effect completion is not successful cancellation.

Abandonment requires explicit operator authorization and preserves history. For
running work, first request stopping and establish cessation before recording
administrative closure; until then show abandonment requested and its uncertainty.
Once abandoned, no automatic attempts or active reconciliation continue. The
historical outcome may remain unresolved. Inspection remains available; later
unsolicited evidence is retained as an annotation, not permission to reopen work.
E1 provides no reopen or rollback command. Explicit new work is still possible.

## 13. Evidence reconciliation and operator contract

Every consequential operator command carries a stable command identity, canonical
action, target, and expected authoritative state revision. An equivalent repeated
command returns its recorded disposition; different content under the same command
identity is a conflict. Revalidate expected state before accepting a new decision.
The durable transition records acceptance of the decision and any execution grant
it authorizes together. Consuming a human recovery approval, reserving attempt
allowance, and allocating that single grant is all-or-none. A lost response or
restart cannot consume the approval twice. If command acceptance is uncertain,
inspect by command identity before repeating the effect.

Human-only commands must be received through the trusted operator control path
and recorded as such. An agent-authored assertion that approval exists is not
operator authorization. Cancellation and abandonment commands similarly preserve
their idempotent request identity even when their operational result is pending.

Each outcome claim must identify its exact proposition: execution completed,
artifact content verified, effect committed, no effect occurred, or something
else explicitly defined. Attribution, integrity, relevance, and the supported
failure model determine evidence sufficiency; no universal source ranking exists.

Direct service observations, task reports, external operator facts, inferences,
and administrative choices remain distinguishable. Preserve conflicting sources
and assess timing, scope, identity and meaning before adopting a new conclusion.
Unresolvable material conflicts require the trusted human; a human administrative
choice does not erase factual uncertainty. Record superseding claims with their
basis instead of rewriting history.

The operator can submit/query by stable reference, inspect identity/specification,
acceptance/execution order, attempts, effects, claims and evidence, request
cancellation, inspect recovery choices, explicitly authorize recovery, provide
external facts, and abandon work. Responses distinguish pending request, applied
decision, uncertain action, and established outcome. No user-visible label may
collapse abandoned-unresolved into ordinary failure or requested-stop into stopped.


## Scope and verification

The initial service is sequential, local and single-operator, with controlled
task effects and no arbitrary programs, subprocesses, network tasks, or automatic
retention expiry. Runtime storage/ownership feasibility remains unverified.
Service acceptance obligations are in REQUIREMENTS.md; no service source exists.
