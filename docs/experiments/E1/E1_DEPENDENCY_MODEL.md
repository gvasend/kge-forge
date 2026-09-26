# E1 Dependency Model

Generated 2026-09-21. This is a discovery artifact only: no implementation, production authority, live store, invocation, or provider state was changed.

## Current boundary

`R4-final = CURRENT + UNIQUE`; `LIVE_R4_FINAL_CONTROLLER_STORE = G4 CURRENT`; `r13 = UNISSUED + UNOWNED`; provider/model requests and E1 effects are zero. The graph preserves historical artifacts without promoting them to current authority.

## Terminal condition

`E1_TERMINAL` requires a fresh final gate, a real first model request, first Programmer ActionRequest, first authorized repository operation, governed Programmer execution, WP1-AC01–09 evidence, and independently reconstructed terminal/QUIESCENT state. Every path to that terminal is blocked before transmission.

## Dependency path from CurrentProviderModelAuthority

The explicit path is:

`CurrentProviderModelAuthority` → `CurrentE1ContentClearanceAuthority` → `ReleasedProfileAuthority(current)` → `ReleaseAuthority(current)` → `OperationalContext(current)` → `OperationalBinding(current)` → `current dispatch` → `invocation candidate` → `applicability reconciliation` → `concrete WorkAuthorization` → `issuance authority/template` → `INACTIVE` → activation/ownership → ACTIVE recovery → dispatcher → GovernedHost → `MODEL_REQUEST_READY` → final fresh gate → first real model request → first ActionRequest → first repository operation → governed loop → acceptance evidence → `E1_TERMINAL`.

`CurrentProviderModelAuthority` is `BLOCKED`: the current dispatch references a boundary but no canonical current provider/model authority record or authorized derivation selects the provider/model. Ability to call a transport implementation is not transmission authority.

## Frontier and missing roots

The current dependency frontier is the set of blocked or unresolved prerequisites that prevent safe downward traversal: `CurrentProviderModelAuthority`, `CurrentModelPayloadAuthority`, `CurrentTransmissionAuthority`, `CurrentRetentionAuthority`, current `ReleasedProfileAuthority`, current `ReleaseAuthority`, `OperationalContext`, `OperationalBinding`, and their dependent dispatch/invocation/lifecycle records.

The lowest currently-known missing authority roots are the provider/model boundary, model-payload owner/derivation, provider-scoped transmission and retention authority, current profile inputs, and the release-root DAG. The settled PD06 manifest identity `e6d71ca6…` is reference-only and is not reintroduced as a blocker target. Profile-6 is historical/stale for R4.

## Status semantics

`SATISFIED` means current, independently reconstructable authority/evidence. `HISTORICAL_ONLY` and `STALE` remain useful for ancestry but cannot authorize current execution. `BLOCKED` means a known prerequisite is absent or explicitly fail-closed. `UNRESOLVED` means the graph identifies a required source whose canonical owner/derivation is not established. No status in this document grants authority.

## Rejected cycles

No permitted authority cycle exists. The graph explicitly rejects `WorkAuthorization → OperationalBinding → WorkAuthorization`, because an object cannot authenticate itself, and rejects a prospective release/profile/content-clearance cycle. Historical copies of identities in downstream artifacts are consistency assertions or forensic evidence, not upstream authority.

## Dependencies discovered through blocked execution

Repeated qualification exposed missing lifecycle templates, unauthenticated lifecycle projections, ActivationTransaction adapters, authority-domain resolvers, operational context and binding owners, noncanonical `bb1808a…` release authority, stale Profile-6, unselected PD06 content clearance, reference-only payload identity, and the current provider/model authority gap. These are represented as nodes and do not imply that any blocker was resolved.

## Evidence and preservation

The machine-readable graph is in [`E1_DEPENDENCY_MODEL.json`](./E1_DEPENDENCY_MODEL.json). Supporting requirements and evidence include the E1 requirements/architecture, WP1-AC01–09, PD06 verification, R4 downstream qualification, current handoff blocker, bb1808a forensic provenance, current profile root blocker, and operational context/binding qualification. Historical artifacts and G4 remain unchanged; no authority was issued and no provider request occurred.

## Node inventory

The JSON is authoritative for the complete node fields (`NodeId`, type, description, prerequisites, required-by, criteria, status, authority, evidence, scope, lineage, and freshness/applicability). Edge records classify requirement, execution, evidence, authority, applicability, historical, consistency, derivation, and temporal dependencies.


## Structural reconciliation

The machine-readable edge set has been reconciled with the declared `DependsOn` relationships. The reconciled graph contains 49 nodes and 106 unique edges. It has two explicit reciprocal cycles (`R4_CURRENT ↔ G4_CURRENT` and `INVOCATION_CANDIDATE ↔ OPERATIONAL_BINDING_CURRENT`), three connected components, and 47 nodes that reach `E1_TERMINAL`; `R0_HISTORY` and `PROFILE6` remain historical/stale roots. See [E1_DEPENDENCY_MODEL_RECONCILIATION.md](./E1_DEPENDENCY_MODEL_RECONCILIATION.md) for dispositions and validation details.

## Final prerequisite projection

The cycle-semantics corrections are applied in the machine-readable model. The prerequisite projection excludes the live-currentness correspondence `G4_CURRENT → R4_CURRENT` and the post-derivation binding constraint `OPERATIONAL_BINDING_CURRENT → INVOCATION_CANDIDATE`. Those relationships remain in `SemanticEdges`; they are not prerequisites. The resulting prerequisite projection is designated `E1_DEPENDENCY_BASELINE_1`. See [E1_DEPENDENCY_MODEL_FINALIZATION.md](./E1_DEPENDENCY_MODEL_FINALIZATION.md).
