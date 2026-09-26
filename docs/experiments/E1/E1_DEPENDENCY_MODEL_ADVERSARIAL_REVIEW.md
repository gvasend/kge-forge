# E1 Dependency Model — Adversarial Review

Review date: 2026-09-21  
Review scope: `E1_DEPENDENCY_MODEL.md`, `E1_DEPENDENCY_MODEL.json`, E1 requirements/architecture, R1–R4 evidence, and blocker history.  
Review constraint: read-only review; no model, implementation, authority, or production state was changed.

## Overall assessment

**FAIL as a complete dependency DAG; PARTIAL as a useful blocker inventory.**

The model captures many important blockers and preserves the distinction between historical evidence, qualification artifacts, and live authority. It correctly identifies `CurrentProviderModelAuthority` as unresolved and records a useful conceptual path to the terminal condition. However, the machine-readable graph is not structurally equivalent to the dependencies declared by its own nodes: 49 nodes and 46 edges leave most declared prerequisites without corresponding edges, and reverse reachability from `E1_TERMINAL` reaches only two nodes. The result is a set of partially connected dependency notes rather than a traversable DAG.

No production action is authorized by this review.

## 1. Structural validity

### Edge direction

The stated convention is prerequisite `From` → dependent `To`. The edges that exist generally follow that direction. Examples such as `CURRENT_PROVIDER_MODEL_AUTHORITY → CURRENT_CONTENT_CLEARANCE_AUTHORITY` and `MODEL_REQUEST_READY → FINAL_FRESH_GATE` are directionally coherent.

The graph nevertheless contradicts itself. Node `DependsOn` declarations are not materialized as edges. There are **60 declared prerequisite pairs with no matching edge**, including:

- `FINAL_FRESH_GATE`, `PROGRAMMER_LOOP`, `ACCEPTANCE_EVIDENCE`, and `TERMINAL_QUIESCENCE` → `E1_TERMINAL`;
- `CURRENT_PROVIDER_MODEL_AUTHORITY` → transmission and retention authority;
- `CURRENT_CONTENT_CLEARANCE_AUTHORITY` → `PROFILE_ROOTS`;
- `PROFILE_ROOTS` → `RELEASED_PROFILE_CURRENT`;
- `RELEASED_PROFILE_CURRENT` → `OPERATIONAL_BINDING_CURRENT`;
- invocation/operational binding → WorkAuthorization;
- WorkAuthorization, lifecycle proof, and ownership → activation;
- activation-context and dispatcher prerequisites;
- profile/repository/budget prerequisites for the Programmer loop.

Thus `DependsOn` cannot be treated as an executable adjacency list, while `Edges` cannot be treated as a complete representation of the declared model.

### Reachability and topology

With the edge direction used by the file, reverse traversal from `E1_TERMINAL` reaches only `E1_SCOPE` and `E1_TERMINAL`. The remaining 47 nodes are disconnected from the terminal in the actual edge graph. This is not an expected consequence of having more nodes than edges; it is a structural defect. A valid decomposition may have many roots, but every prerequisite that is required by the terminal must have a directed path to that terminal.

The 49-node/46-edge count is therefore not, by itself, evidence of a valid sparse DAG. It is consistent with a graph in which the majority of prerequisites were recorded only in node metadata. The topology is incomplete until those declared relationships are represented as edges or explicitly marked informational.

### Roots and disconnected components

The JSON exposes 22 zero-incoming nodes. Several are legitimate external roots or historical facts (`E1_SCOPE`, `R12_HISTORY`, `R13_NAMESPACE`, `RUNTIME_HEAD`), but others are execution/dependency nodes incorrectly left root-like: `ACTIVATION_CONTEXT`, `CANCELLATION`, `PROGRAMMER_PROFILE`, `REPOSITORY_AUTHORITY`, `STATUS_BUDGET`, `LIFECYCLE_TEMPLATE`, and `PROFILE_ROOTS`. Their own `DependsOn` fields state prerequisites, so they are not roots in the graph actually traversed by the edges.

`R4_CURRENT` and `G4_CURRENT` mutually list one another as prerequisites, but neither relationship is an edge. If that mutuality is intended as a consistency relation, it must be represented as a typed consistency/authority relation that does not create a DAG cycle. If it is intended as derivation, one side must be identified as the authority root.

### Duplicate or merged semantics

Several nodes merge distinct authority domains or lifecycle phases:

- `CURRENT_CONTENT_CLEARANCE_AUTHORITY` combines content inventory, provider boundary, transmission permission, and retention permission even though the blocker history treats these as separate unresolved sources.
- `STATUS_BUDGET` combines status projection, token/action budgets, no-progress policy, cancellation, and recovery.
- `ACTIVATION` combines precondition validation, durable intent, and ownership reservation.
- `CANCELLATION` combines admission closure, ownership release, ExecutionScope reconciliation, QUIESCENT, and terminal recovery.
- `PROGRAMMER_LOOP` combines model response, ActionRequest/ActionResult governance, repository effects, and terminal handling.

These combinations are understandable summaries, but they are not equivalent nodes for dependency traversal. The review does not require splitting them now; it finds that the current model does not identify them as aggregation nodes or preserve their internal edges.

### Informational/history nodes

`R0_HISTORY`, `R3_HISTORY`, `RELEASE_BB1808A`, `RELEASE_C43F119`, and `PROFILE6` are correctly labelled historical in substance. They are not execution authority. However, the graph mixes their historical/consistency relationships with live prerequisite lists without a distinct edge semantics for “historical ancestry only” in all places. This risks treating a historical node as a current root if a consumer traverses `DependsOn` rather than status and edge type.

## 2. Dependency completeness

The model includes the main runtime, release, context, binding, dispatch, invocation, applicability, WorkAuthorization, lifecycle, dispatcher, host, and model-request chain. It is incomplete relative to the authoritative architecture and blocker history in these areas:

- **Provider/model boundary:** present as a blocker node, but provider endpoint, model identity/class, redirect/proxy constraints, provider response authority, and provider-side retention boundary are not separate dependencies.
- **Content clearance:** no explicit content-inventory, protected-governing-content, secrets/credentials exclusion, dynamic-retrieval, or first-request model-payload node. `CURRENT_MODEL_PAYLOAD_AUTHORITY` is only a summary.
- **Profile/policy:** no separate governed tool registry, repository capability, execution profile, network/credential restrictions, transmission policy, retention policy, escalation policy, or authority-expansion policy nodes.
- **Authority roots:** no explicit current `SupervisorAuthority`, `SuccessionAuthority`, material-policy authority, Architect decision nodes, or current release-root source leaves. These appear only indirectly in descriptions/evidence.
- **Lifecycle:** no separate issuance journal, lifecycle recovery evidence, activation intent, ownership ledger transition, ExecutionScope, audit state, or terminal disposition evidence nodes.
- **Execution/evidence:** no explicit provider response, ActionRequest, ActionResult, governed tool execution, repository state/effect evidence, model-cycle evidence, or WP1 acceptance-obligation nodes beyond a single aggregate `ACCEPTANCE_EVIDENCE`.
- **Temporal/applicability:** freshness is recorded as free text on nodes, but no explicit version/fingerprint checks, TOCTOU revalidation, runtime-race edge, or “current generation at effect” node is present.
- **Scope/lineage:** task scope, profile scope, provider purpose, release scope, and R4/R5 exact-runtime binding are not separate typed dependencies.

These are omissions from the traversable model, not recommendations to invent new authority.

## 3. Authority validity

The model is conservative in several important respects:

- it marks `bb1808a…` noncanonical and Profile-6 stale;
- it treats implementation code, provider availability, copied digests, and qualification artifacts as insufficient authority;
- it rejects `WorkAuthorization → OperationalBinding → WorkAuthorization` self-authentication;
- it keeps content clearance and provider/model authority unresolved.

No direct invalid authority derivation was found in the node statuses. The principal hidden risk is structural: because prerequisite declarations are not edges, a naïve graph consumer could start at a root-like `PROGRAMMER_PROFILE`, `ACTIVATION_CONTEXT`, or `REPOSITORY_AUTHORITY` and bypass the missing upstream authority. The model therefore needs an explicit rule that `DependsOn` is authoritative graph data or must equal the edge set; currently it has neither.

The `G4_CURRENT` and `R4_CURRENT` mutual prerequisites also require clarification to avoid an implicit self-authorizing current-state loop. The accepted evidence can support G4 as the live store selection and R4 as the selected runtime; the graph should distinguish those authority/consistency directions rather than leave both as undeclared reciprocal prerequisites.

## 4. Satisfaction criteria

Every node currently receives the same generic criterion: “authenticated, independently reconstructable, and applicable.” That is insufficient for adversarial verification. It does not state:

- what artifact or journal proves satisfaction;
- what exact identity/hash must recompute;
- what freshness window or generation must match;
- what negative tests reject substitution;
- whether the node is evidence, authority, execution, or applicability state;
- whether the node is allowed to be historical.

For example, `R4_CURRENT` requires unique live runtime-head reconstruction; `CURRENT_PROVIDER_MODEL_AUTHORITY` requires a canonical provider/model selector and boundary constraints; `FIRST_REAL_MODEL_REQUEST` requires actual provider transmission evidence; and `E1_TERMINAL` requires acceptance and terminal/quiescent reconstruction. The common criterion cannot prove any of those states and is not itself circular only because it is too weak.

`E1_TERMINAL` also lists `FINAL_FRESH_GATE`, `PROGRAMMER_LOOP`, `ACCEPTANCE_EVIDENCE`, and `TERMINAL_QUIESCENCE` in `DependsOn`, but the edge graph does not connect them. This makes the terminal satisfaction test observably incomplete.

## 5. Historical blocker classification

| Historical blocker | Represented? | Classification | Could deterministic traversal have found it before execution? | Runtime evidence still needed? |
|---|---:|---|---|---|
| G0/G1/G2/G3/G4 live-vs-qualification confusion | Yes, partially (`G4_CURRENT`, history/status) | PRECOMPUTABLE, but authority-domain distinction was under-specified | Yes, by store-lineage and consumer checks | No, except reconstruction validation |
| R4 stale dispatch/context/release applicability | Yes, partially | PRECOMPUTABLE/SEMANTICALLY_UNCERTAIN | The missing authority inputs were statically visible; applicability preservation required qualification | Yes, for lifecycle semantics |
| Missing applicability-reconciliation authority | Yes (`APPLICABILITY_RECONCILIATION`) | PRECOMPUTABLE | Yes, by checking authority schema before dispatch | No new runtime effect needed |
| Missing G4 canonical reconciliation identity | Not explicitly as a node; only folded into applicability/G4 history | NOT_REPRESENTED | Yes, canonical publication schema could be checked before selection | No |
| Missing WorkAuthorization template and issuance authority | Yes, but merged (`LIFECYCLE_TEMPLATE`, `LIFECYCLE_ISSUANCE`) | PRECOMPUTABLE | Yes, consumer schema and authority inputs could be inspected before lifecycle execution | Integration tests still needed |
| Circular `fields_values` template model | Not explicitly represented as a node | NOT_REPRESENTED | Yes, dependency-DAG/cycle analysis could detect it | No, unless consumer behavior was ambiguous |
| Unauthenticated lifecycle projection / ActivationTransaction adapter | Partially (`ACTIVATION_CONTEXT`) | PRECOMPUTABLE/NOT_REPRESENTED | Interface authority-source matrix could expose it | Integration/recovery tests needed |
| Missing operational-context authority | Yes (`OPERATIONAL_CONTEXT_CURRENT`) | PRECOMPUTABLE | Yes, source-owner check | No production runtime needed |
| Missing operational-binding authority | Yes (`OPERATIONAL_BINDING_CURRENT`) | PRECOMPUTABLE | Yes, source-owner/DAG check | No production runtime needed |
| Noncanonical `bb1808a…` release authority | Yes (`RELEASE_BB1808A`, `RELEASE_AUTHORITY_CURRENT`) | PRECOMPUTABLE after provenance review | The reference was discoverable; its historical classification required forensic evidence | Yes, to verify provenance |
| Profile-6 stale/superseded | Yes (`PROFILE6`, `RELEASED_PROFILE_CURRENT`) | PRECOMPUTABLE | Scope/currentness check could find it | Technical profile compatibility may still need qualification |
| PD06 content clearance unselected / noncanonical | Partially (`CURRENT_CONTENT_CLEARANCE_AUTHORITY`) | PRECOMPUTABLE, but manifest/source detail absent | Yes, release/readiness fields were explicit | No for the blocker itself |
| Current model payload owner missing | Yes (`CURRENT_MODEL_PAYLOAD_AUTHORITY`) | PRECOMPUTABLE | Yes, digest-owner lookup | No unless dynamic payload behavior is tested |
| Current transmission/retention provider scope missing | Yes, merged into two nodes | PRECOMPUTABLE | Yes, provider-bound policy lookup | Runtime boundary tests may still be needed |
| `CurrentProviderModelAuthority` missing | Yes | PRECOMPUTABLE | Yes, current dispatch/provider selector audit | No provider request should be made |
| Closed telemetry/cancellation and recovery behavior | Partially (`CANCELLATION`, `STATUS_BUDGET`) | RUNTIME_DISCOVERABLE | Static graph can require tests, not prove behavior | Yes, interruption/recovery tests needed |

The model therefore captures the existence of the most important blockers but not all discovery events as first-class nodes. In particular, G4 reconciliation identity, circular template semantics, and unauthenticated projection are absent or overly compressed.

## 6. Counterfactual turn analysis

A deterministic graph and authority-owner traversal before R4 would likely have avoided repeated reasoning about live-vs-qualification stores, `bb1808a…`, stale Profile-6, missing reconciliation authority, missing template/issuance inputs, operational-context/binding ownership, and the current provider/model root. These are source-existence, scope, lineage, or schema prerequisites that can be checked without executing production.

The graph would not eliminate:

- Architect decisions to establish or release missing authority roots;
- semantic judgments about whether a runtime change preserves applicability;
- qualification of lifecycle integration, interruption, cancellation, status, and dispatcher behavior;
- actual provider/model behavior, response handling, Programmer ActionRequests, repository effects, and WP1 acceptance evidence;
- final fresh-state and TOCTOU checks immediately before an authorized effect.

No recorded evidence supports a precise token, latency, or cost saving estimate. The supported claim is category-level: deterministic traversal could replace repeated rediscovery of known authority/schema blockers, while runtime qualification and human authority decisions would remain necessary.

## 7. CurrentProviderModelAuthority path audit

The report’s named path is conceptually correct but is not fully represented by edges. The following required links are absent from `Edges` even though they appear in node `DependsOn` or the JSON path:

- `CURRENT_CONTENT_CLEARANCE_AUTHORITY → RELEASED_PROFILE_CURRENT`;
- `RELEASED_PROFILE_CURRENT → OPERATIONAL_BINDING_CURRENT`;
- `INVOCATION_CANDIDATE → CONCRETE_WORKAUTH`;
- `CONCRETE_WORKAUTH → LIFECYCLE_ISSUANCE`;
- `APPLICABILITY_RECONCILIATION → LIFECYCLE_ISSUANCE`;
- `INACTIVE_ISSUANCE → ACTIVATION`;
- `CURRENT_DISPATCH`/`OPERATIONAL_CONTEXT_CURRENT`/`OPERATIONAL_BINDING_CURRENT → DISPATCHER_ELIGIBILITY`;
- `CURRENT_CONTENT_CLEARANCE_AUTHORITY`/`CURRENT_RETENTION_AUTHORITY → MODEL_REQUEST_READY`;
- `MODEL_REQUEST_READY → E1_TERMINAL` through final gate and execution evidence.

The blocker itself is supported by `CURRENT_R4_HANDOFF_AUTHORITY_ROOT_BLOCKED.json` (SHA-256 `89095b7908da63aa6e851c47164c264b9d9a58b8f5ae899b142e867ad888a66f`): the dispatch has a payload digest and transmission/retention reference, but no independently current provider/model selection. The blocker should remain unresolved. The model should not claim that the conceptual path is a valid traversable path until the missing edges are represented.

## 8. Recommended corrections (not applied)

1. Make one representation authoritative: either materialize every `DependsOn` pair as a typed edge or remove `DependsOn` and derive it from `Edges`.
2. Add explicit edges from all prerequisites to `E1_TERMINAL`; then run reachability and cycle checks.
3. Add typed aggregation nodes or decompose content clearance, profile policy, lifecycle, cancellation, and execution evidence into separately traversable nodes.
4. Add explicit nodes for provider/model selector, model payload owner, content inventory/protected governing content, transmission authority, retention authority, profile/tool/repository policy, supervisor/succession, issuance journal, ownership ledger, audit, provider response, ActionRequest/ActionResult, and terminal evidence.
5. Separate authority, derivation, consistency, applicability, temporal, historical, and evidence edges everywhere; do not rely on free-text descriptions.
6. Replace the generic satisfaction criterion with node-specific observable predicates and negative checks.
7. Encode the G4/R4 relationship as a non-cyclic authority/consistency relation.
8. Add a machine-checkable invariant that every non-informational node has a path to `E1_TERMINAL` and every declared prerequisite has exactly one edge record.

These are review findings only. They have not been applied.

## 9. DAG hypothesis conclusion

E1 evidence **supports the dependency-DAG hypothesis**, but the submitted artifact does not yet implement a complete DAG. The repeated blockers are strongly explained by missing authority roots, schema prerequisites, applicability decisions, and temporal gates that can be represented deterministically. However, the current JSON is structurally incomplete and semantically compressed, so it cannot reliably replace LLM reasoning or serve as a sound traversal engine without the corrections listed above.
