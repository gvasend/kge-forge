# E1 Dispatcher Prerequisite Representation Review 1

## Classification

`FRONTIER_SELECTION_DEFECT`

The baseline explicitly represents the relevant prerequisites, so the runtime experiment was selected before those unsatisfied nodes were resolved. This is a frontier-selection error, not a newly discovered dependency and not a need to weaken dispatcher criteria.

## Condition mapping

### A. ACTIVE lifecycle recovery

- Baseline node: `ACTIVE_RECOVERY`
- Edges: `ACTIVATION → ACTIVE_RECOVERY`; `ACTIVE_RECOVERY → DISPATCHER_ELIGIBILITY`
- Status: `BLOCKED`
- Criteria: independent recovery establishes `ACTIVE` with exact ownership.
- Classification: `EXPLICIT_PREREQUISITE_NODE`

`ACTIVE_RECOVERY` could not be satisfied because activation, durable intent, and ownership reservation had not occurred. Deterministic traversal should have stopped at this branch before selecting dispatcher eligibility.

### B. Exact ownership

- Baseline representation: exact ownership is part of `ACTIVE_RECOVERY` satisfaction criteria and activation/ownership transaction semantics; pre-activation `OWNERSHIP_NONE` is a separate satisfied node.
- `OWNERSHIP_NONE` is `SATISFIED` only for the pre-activation state.
- Classification: `IMPLICIT_IN_SATISFACTION_CRITERIA` for post-activation ownership; the precondition itself is an explicit node.

The experiment correctly did not assume ownership. The baseline does not have a separate `OWNERSHIP_HELD_BY_EXACT_ATTEMPT` node, but the requirement is already explicit in `ACTIVE_RECOVERY`'s criteria and does not constitute a new dependency.

### C. Current operational context/binding

- Baseline nodes: `OPERATIONAL_CONTEXT_CURRENT` and `OPERATIONAL_BINDING_CURRENT`
- Edges: `OPERATIONAL_CONTEXT_CURRENT → DISPATCHER_ELIGIBILITY`; `OPERATIONAL_BINDING_CURRENT → DISPATCHER_ELIGIBILITY`; context also derives into binding and dispatch.
- Status: both `BLOCKED`
- Criteria: authenticated, current, independently reconstructable context and binding for the exact runtime/invocation/profile/policy.
- Classification: `EXPLICIT_PREREQUISITE_NODE`

These nodes were not instantiated because their current authority roots/derivations remain unresolved. Deterministic traversal should have exposed them before dispatcher eligibility.

## Correct current frontier

Using the existing graph, `DISPATCHER_ELIGIBILITY` is not an actionable leaf. Its unsatisfied prerequisite branches are:

- `ACTIVE_RECOVERY` (through `ACTIVATION` and its prerequisites);
- `OPERATIONAL_CONTEXT_CURRENT` (through `RELEASE_AUTHORITY_CURRENT` and runtime prerequisites);
- `OPERATIONAL_BINDING_CURRENT` (through context, dispatch, invocation, and profile prerequisites).

No edge or node is changed by this review.

## Causal interpretation

The runtime experiment observed that these states were absent; it did not discover a new requirement. The graph already encoded the requirement and should have prevented a dispatcher eligibility experiment from being treated as the next actionable frontier. The experiment remains useful as non-effecting confirmation of the blocked state.

No lifecycle activation, ownership reservation, operational binding instantiation, repository operation, payload transmission, or model request occurred.
