# E1 Architectural Finding — Explicit Dependency Planning

Date: 2026-09-21  
Scope: Experiment 1 dependency reconstruction, structural reconciliation, cycle review, baseline finalization, and frontier evaluation.

This document records an architectural finding. It does not modify the dependency model, resolve authority blockers, issue authority, or change implementation or production state.

## Observed sequence

Historical E1 progression used repeated LLM-directed turns. Prerequisites were often discovered incrementally through blocked qualification or execution attempts. The resulting history contains distinct findings for live-store lineage, generation selection, applicability, lifecycle templates, authority-source ownership, release provenance, profile scope, content clearance, payload ownership, and provider/model authority.

A dependency model was then reconstructed from the requirements, architecture, acceptance obligations, R1–R4 evidence, authority records, and blocker history. The first representation contained meaningful semantic information but did not encode all declared prerequisites in the machine-readable edge set. It had 49 nodes and 46 edges while 60 declared prerequisite pairs were absent from the edge representation.

Structural reconciliation made those declared prerequisites explicit, producing 104 prerequisite edges after the cycle-semantics corrections. The cycle review found that the two apparent reciprocal cycles were not genuine construction-order cycles:

- `R4_CURRENT ↔ G4_CURRENT` combined G4 derivation with live-currentness correspondence.
- `INVOCATION_CANDIDATE ↔ OPERATIONAL_BINDING_CURRENT` combined binding derivation with post-derivation applicability/consistency validation.

Those non-ordering relationships were preserved as semantic edges and excluded from the prerequisite projection. `E1_DEPENDENCY_BASELINE_1` therefore has an acyclic prerequisite projection.

Deterministic frontier evaluation from `E1_TERMINAL` identified six frontier nodes. Each was evaluated independently using its local subgraph and existing evidence:

- `KNOWN_LEAF_RESOLVED`: 3
- `KNOWN_LEAF_REQUIRES_AUTHORITY`: 3
- `NEW_DEPENDENCY_DISCOVERED`: 0
- `BASELINE_DEFECT`: 0
- Runtime experiments required: 0

The resolved nodes were historical/forensic leaves (`R3_HISTORY`, `RELEASE_BB1808A`, and `RELEASE_C43F119`). The authority-required leaves were `CurrentProviderModelAuthority`, `CurrentModelPayloadAuthority`, and `LIFECYCLE_TEMPLATE`.

## What the experiment establishes

### Observed

- E1’s prior blocker history contains prerequisite discoveries that were repeated across planning turns.
- The same evidence can be represented as nodes, typed relations, statuses, provenance, scope, lineage, and freshness constraints.
- The initial machine-readable representation was incomplete even though much of the dependency knowledge was already present in prose and node metadata.
- Deterministic reconciliation found and represented the 60 missing declared prerequisite pairs.
- Separating derivation/order from correspondence, applicability, and currentness removed the two prerequisite cycles without discarding the semantic relationships.
- Deterministic traversal reached a bounded frontier and evaluated all six frontier nodes without discovering another dependency.
- The current provider/model blocker remained unresolved because existing evidence did not contain a current canonical provider/model authority.

### Supported inference

E1 supports externalizing durable reasoning structure instead of retaining all prerequisite state in transient LLM context. A graph can preserve known blocker discoveries, prevent repeated rediscovery, and expose the exact frontier requiring judgment or authority.

E1 supports deterministic prerequisite traversal for planning. Once a directed prerequisite projection exists, reachability, leaves, cycles, connected components, and dependent paths can be computed without asking an LLM to rediscover graph structure.

E1 supports separating planning from semantic reasoning. The graph determined which nodes were ready for evaluation and which were blocked; bounded reasoning was then applied to a single frontier node using its local evidence.

E1 supports separating typed semantic relationships from prerequisite ordering. Currentness, binding, correspondence, applicability, and freshness remain important, but treating them all as construction prerequisites creates false cycles and circular satisfaction semantics.

E1 supports using LLM reasoning on bounded frontier problems. The frontier evaluation did not broaden into unrelated dependency discovery, and it preserved the distinction between a known leaf requiring authority and a newly discovered dependency.

E1 supports persistent reasoning state across LLM turns when the state is canonical, provenance-bound, and independently traversable. The baseline, reconciliation, cycle review, frontier report, and directed-resolution report provide durable state that later turns can consume.

E1 supports reducing repeated dependency rediscovery as an architectural objective. Known blocker categories became explicit graph nodes and statuses rather than recurring implicit context. The evidence demonstrates structural reduction of rediscovery opportunities, not a measured performance saving.

### Not yet demonstrated

E1 did not measure token, latency, monetary, or human-time savings. No claim of a numerical reduction is supported.

E1 did not demonstrate that an LLM-generated graph mutation can be safely accepted automatically. The reconciliation was governed by explicit instructions and human review boundaries.

E1 did not demonstrate production execution from the graph. R4 remained current, r13 remained unissued and unowned, provider/model requests remained zero, and E1 effects remained zero.

E1 did not establish that all future dependency classes can be discovered statically. Lifecycle interruption, cancellation, provider behavior, response handling, and repository effects still require runtime qualification.

E1 did not prove that a graph alone resolves semantic authority questions. Missing provider/model authority, payload ownership, and lifecycle authority still require external or human authority.

## Architectural principle

Candidate principle:

> Externalize durable reasoning structure and use deterministic dependency traversal for planning; invoke LLM reasoning for bounded semantic problems at the unresolved frontier.

E1 evidence supports adopting this as a Forge architecture principle, with two qualifications. First, the externalized structure must distinguish authority, derivation, evidence, applicability, temporal/freshness, lineage, and semantic correspondence. Second, only the prerequisite/derivation projection may drive construction and execution ordering; semantic relations must be validated without being treated as ordering prerequisites.

The principle does not grant the graph authority. It does not allow an LLM, graph node, implementation default, or historical artifact to manufacture missing authority. It makes the missing decision visible and bounded.

## Recommended representation

Forge should represent both of the following:

1. A typed semantic knowledge graph containing canonical nodes, provenance, authority domains, evidence, scope, lineage, freshness, applicability, and relations such as authority dependency, derivation, binding, correspondence, constraint, applicability, historical ancestry, and synchronization.
2. An acyclic prerequisite projection derived from the semantic graph and used for planning, readiness, frontier calculation, and execution ordering.

The prerequisite projection should be materialized or reproducibly generated, validated for cycles and dangling references, and never allowed to silently disagree with the semantic graph. A semantic relationship may be retained without appearing in the prerequisite projection.

## Minimum future Forge capability

Without implementing it here, the minimum capability would need to provide:

- canonical dependency assertions with stable identities, source locations, scope, lineage, and evidence;
- typed semantic relationships with explicit direction and relation semantics;
- a declared rule for projecting eligible relation types into a prerequisite DAG;
- deterministic validation for node identity, edge direction, duplicates, dangling references, cycles, reachability, status legality, and metadata/edge agreement;
- deterministic frontier calculation from a selected terminal node, including stopping rules for satisfied, unresolved, blocked, historical, and external-authority leaves;
- an LLM proposal format for graph mutations that includes proposed nodes/edges, relation type, rationale, evidence references, and confidence without granting authority;
- governed acceptance/rejection of graph mutations by an Architect or validated policy, with append-only history and rejection reasons;
- persistent node status, evidence, authority provenance, freshness, applicability, and supersession state;
- bounded context generation that supplies an LLM only the target frontier node, its local prerequisite/dependent subgraph, relevant evidence, and permitted result classifications;
- explicit separation of semantic edges from prerequisite edges so that correspondence and applicability checks cannot create execution-order cycles;
- replayable graph snapshots and validation reports so a later turn can reconstruct exactly which model was evaluated.

## Limits and preservation

The capability should preserve historical evidence without promoting it to current authority, require external authority for authority roots, and keep runtime experiments as evidence-producing actions rather than implicit graph mutations. It should also retain the distinction between a proposed mutation and an accepted canonical mutation.

Current production remains `R4-final = CURRENT + UNIQUE` with `LIVE_R4_FINAL_CONTROLLER_STORE = G4 CURRENT`; r13 remains unissued and unowned; provider/model requests and E1 effects remain zero.

## Actionability correction

E1 also establishes that dependency traversal and actionability selection are distinct. Reachability/frontier calculation alone is insufficient for execution planning. A node may be a `BLOCKED_FRONTIER` member when its resolution operation requires unresolved runtime state, authority, freshness, or a future effect. The corrected rule selects work only after operation prerequisites and temporal conditions are satisfied; the dispatcher experiment demonstrates the failure mode when structural frontier membership is treated as actionable.
