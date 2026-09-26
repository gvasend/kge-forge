# E1 Actionability Semantics 1

## State definitions

- `UNRESOLVED`: satisfaction criteria are not established.
- `FRONTIER`: the node is at the satisfied/unsatisfied boundary under prerequisite traversal.
- `ACTIONABLE`: an authorized, known resolution operation can run now; all operation prerequisites, scope, lineage, freshness, and temporal conditions hold.
- `BLOCKED_FRONTIER`: the node is unresolved and reachable at the boundary, but its resolution operation cannot run because required runtime state, authority, construction, evidence, or a prior branch is absent.

Frontier membership does not imply actionability.

## Selection rule

Select a node only when it is unresolved, its operation is known, every prerequisite needed before that operation is satisfied, no criterion depends on unresolved runtime state from another branch, applicable authority exists, scope/lineage/freshness permit the operation, and the operation does not presuppose a future effect.

## Defect replay

Immediately before `E1_DISPATCHER_ELIGIBILITY_EXPERIMENT_1`, the node was unresolved and structurally reachable, but `ACTIVE_RECOVERY`, `OPERATIONAL_CONTEXT_CURRENT`, and `OPERATIONAL_BINDING_CURRENT` were unresolved prerequisites. Exact ownership was part of ACTIVE recovery criteria. Therefore dispatcher eligibility was `BLOCKED_FRONTIER`, not actionable, and should not have been selected. No historical record is changed.

## Validation

The corrected procedure preserves all dependency edges and satisfaction criteria, does not infer authority, and does not treat runtime requirements as semantic assumptions. It separates graph traversal from operation selection and cannot hide unresolved branches.
