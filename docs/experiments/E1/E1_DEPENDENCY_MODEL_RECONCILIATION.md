# E1 Dependency Model — Structural Reconciliation

Reconciliation date: 2026-09-21. This update reconciles declarations already present in the model only. It does not resolve blockers, execute production actions, issue authority, or modify implementation code.

## Assessment

**PARTIAL / FAIL as a DAG.** All 60 previously identified missing `DependsOn` pairs with existing node identifiers are represented explicitly. The resulting graph has 106 unique edges, 3 connected components, 47 nodes reaching `E1_TERMINAL`, and 2 cycles. It is structurally more explicit, but not an acyclic dependency DAG because reciprocal declarations remain.

## Before and after counts

- Before: 49 nodes, 46 edges; the prior adversarial review identified 60 missing prerequisite pairs.
- After: 49 nodes, 106 unique edges, 0 duplicate edges, 0 dangling references, 0 self-edges.
- Connected components: 3 (sizes: [47, 1, 1]).
- Nodes able to reach `E1_TERMINAL` through prerequisite edges: 47; unable: ['PROFILE6', 'R0_HISTORY'].
- Cycles: 2.

## Disposition of all 60 previously missing pairs

Every one of the 60 pairs identified by the adversarial review came from an existing-node `DependsOn` declaration. Each is recorded in `StructuralReconciliation.DependsOnDispositions` in the JSON with its source location, dependency type, and `Action: ADDED`. No new semantic dependency was invented. The pre-existing edge set is preserved and the missing declared prerequisites are made explicit.

`RequiredBy` is now normalized to the reverse of the active edge set. This prevents active metadata from silently disagreeing with edges. The JSON retains the reconciled declarations and records the normalization rule. Relationships that were ambiguous or named absent nodes remain dispositions rather than fabricated nodes.

## Remaining ambiguous relationships

1. `R4_CURRENT ↔ G4_CURRENT`: reciprocal current-state declarations create a cycle. The model does not decide whether this is authority, consistency, or derivation.
2. `INVOCATION_CANDIDATE ↔ OPERATIONAL_BINDING_CURRENT`: invocation declares the binding as a prerequisite while the pre-existing consistency edge binds the binding to invocation. Both are represented; their semantic direction remains unresolved.
3. Historical/qualification roots such as `R0_HISTORY` and `PROFILE6` remain non-current authority, even where they participate in ancestry or qualification relationships.

## Graph validation

- `NodeCount=49`
- `EdgeCount=106`
- `DuplicateEdges=0`
- `DanglingNodeRefs=0`
- `SelfEdges=0`
- `ConnectedComponentCount=3`
- `CycleCount=2`
- `NodesReachableToTerminal=47`
- `NodesUnableToReachTerminal=['PROFILE6', 'R0_HISTORY']

Cycles detected:

- `R4_CURRENT → G4_CURRENT → R4_CURRENT`
- `INVOCATION_CANDIDATE → OPERATIONAL_BINDING_CURRENT → INVOCATION_CANDIDATE`

The two singleton components are `R0_HISTORY` and `PROFILE6`; they remain disconnected because the reconciled active edge set treats them as historical/qualification roots rather than current execution prerequisites.

## CurrentProviderModelAuthority path

Using only actual graph edges, the explicit path is:

`CURRENT_PROVIDER_MODEL_AUTHORITY` → `CURRENT_CONTENT_CLEARANCE_AUTHORITY` → `RELEASED_PROFILE_CURRENT` → `RELEASE_AUTHORITY_CURRENT` → `OPERATIONAL_CONTEXT_CURRENT` → `OPERATIONAL_BINDING_CURRENT` → `CONCRETE_WORKAUTH` → `INACTIVE_ISSUANCE` → `ACTIVATION` → `ACTIVE_RECOVERY` → `DISPATCHER_ELIGIBILITY` → `HOST_CONSTRUCTION` → `MODEL_REQUEST_READY` → `FINAL_FRESH_GATE` → `E1_TERMINAL`

This is a structural traversal only. `CURRENT_PROVIDER_MODEL_AUTHORITY` remains `BLOCKED`; no authority was inferred or resolved.

## Semantic versus structural consistency

`DependsOn` metadata and active edges now agree for all existing-node prerequisite declarations. `RequiredBy` is maintained as the reverse adjacency projection. Any unresolved semantic direction remains explicitly reported above rather than silently used to authorize work.

## Remaining disconnected nodes

`R0_HISTORY` and `PROFILE6` are the only nodes unable to reach `E1_TERMINAL`. They are historical/stale evidence roots, not omitted current execution prerequisites. Their disconnection is intentional and does not promote them to authority.

## Preservation

R4/G4 state, r13 state, provider/model request count, E1 effects, unresolved authority leaves, historical artifacts, and implementation bytes are unchanged.
