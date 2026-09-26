# E1 Template-1 Typed Knowledge Graph 1

Manual, provenance-linked expansion of the completed closure sweep. No blocker is repaired and no authority, prerequisite status, implementation, lifecycle or production state is changed. The existing DAG remains the baseline projection.

| Measure | Result |
|---|---:|
| Graph entities | 339 |
| Graph assertions | 958 |
| Tracked Template-1 slots | 43 |
| Resolved / unresolved | 2 / 41 |
| Additional already-fixed inputs | 2 |
| Baseline nodes / prerequisite edges / semantic edges | 49 / 104 / 2 |
| Next eligible work package | NONE |
| Template-1 construction / Candidate-3 resumption ready | NO / NO |
| Production effect | NO |

The 43-slot inventory follows Closure Plan 1: 20 initially unresolved authenticated inputs plus 23 field values. The two policy-fixed authenticated inputs, INACTIVE and NONE, are represented separately; the complete consumer has 22 + 23 = 45 value positions. Only InvocationAttemptId (candidate identity, not issued attempt) and profile_sha256 (released content digest) are resolved.

The full machine-readable graph is [E1_TEMPLATE1_TYPED_KNOWLEDGE_GRAPH_1.json](E1_TEMPLATE1_TYPED_KNOWLEDGE_GRAPH_1.json). The [blocking cut](E1_TEMPLATE1_CLOSURE_BLOCKING_CUT_1.md) includes exact slot memberships, mechanisms and conditional re-evaluation consequences.

## Evidence and assertion semantics

All 58 input snapshots are content-hashed in `source_manifest`. Every entity and edge has source path, raw content identity, declared identities where available, selector/line, extraction method and validation status. `DETERMINISTIC_EXTRACTED` records copied structure; `ARTIFACT_REPORTED` retains findings without rerunning production checks; `LLM_PROPOSED` marks causal grouping, mechanism choices and proposed overlay relations. Proposed relationships are not authority or state changes.

Each slot carries its semantic meaning, source requirement, type/annotation, producer, transform, representation, partial validator, consumer, governing source domain, pipeline links and missing links. A named authority/source domain is not an authenticated current object. A Python annotation is not a complete type validator. Null producer/transform references explicitly record unknown links; no placeholder producer is invented.

## Slot inventory

| Slot | State | Root condition(s) |
|---|---|---|
| `authenticated_inputs.InvocationAttemptId` | RESOLVED | Accepted exact source identity |
| `authenticated_inputs.binding_sha256` | UNRESOLVED | binding |
| `authenticated_inputs.canonical_binding` | UNRESOLVED | binding |
| `authenticated_inputs.DispatchAuthorizationId` | UNRESOLVED | dispatch |
| `authenticated_inputs.specific_approval_id` | UNRESOLVED | approval |
| `authenticated_inputs.predecessor` | UNRESOLVED | ancestry |
| `authenticated_inputs.eligibility` | UNRESOLVED | eligibility |
| `authenticated_inputs.release_authority` | UNRESOLVED | release |
| `authenticated_inputs.OperationalContextId` | UNRESOLVED | context_id |
| `authenticated_inputs.runtime` | UNRESOLVED | runtime |
| `authenticated_inputs.runtime_head` | UNRESOLVED | runtime_head |
| `authenticated_inputs.supervisor` | UNRESOLVED | supervisor |
| `authenticated_inputs.succession_head` | UNRESOLVED | succession |
| `authenticated_inputs.profile_sha256` | RESOLVED | Accepted exact source identity |
| `authenticated_inputs.ModelPayloadDigest` | UNRESOLVED | payload |
| `authenticated_inputs.transmission_retention` | UNRESOLVED | retention |
| `authenticated_inputs.budget_policy` | UNRESOLVED | budget |
| `authenticated_inputs.implementation_identity` | UNRESOLVED | implementation |
| `authenticated_inputs.audit` | UNRESOLVED | audit |
| `authenticated_inputs.lifecycle_envelope` | UNRESOLVED | lifecycle |
| `fields_values.authorization_id` | UNRESOLVED | ignored |
| `fields_values.revision` | UNRESOLVED | ignored |
| `fields_values.work_package_id` | UNRESOLVED | dispatch |
| `fields_values.session_id` | UNRESOLVED | binding |
| `fields_values.turn_id` | UNRESOLVED | binding |
| `fields_values.read_roots` | UNRESOLVED | paths |
| `fields_values.write_roots` | UNRESOLVED | paths |
| `fields_values.deny_roots` | UNRESOLVED | paths |
| `fields_values.read_deny_roots` | UNRESOLVED | paths |
| `fields_values.write_deny_roots` | UNRESOLVED | paths |
| `fields_values.exec_bins` | UNRESOLVED | exec_bins |
| `fields_values.exec_argv_allowlist` | UNRESOLVED | argv |
| `fields_values.shell` | UNRESOLVED | shell_network |
| `fields_values.network` | UNRESOLVED | shell_network |
| `fields_values.state` | UNRESOLVED | ignored |
| `fields_values.context_binding` | UNRESOLVED | context_hydration |
| `fields_values.context_projection` | UNRESOLVED | context_projection |
| `fields_values.ownership_ledger` | UNRESOLVED | audit, ignored |
| `fields_values.write_directory_roots` | UNRESOLVED | paths |
| `fields_values.execution_profile` | UNRESOLVED | execution_profile |
| `fields_values.model_transport` | UNRESOLVED | transport |
| `fields_values.model_transmission` | UNRESOLVED | transmission |
| `fields_values.operational_binding` | UNRESOLVED | governance |

## Identity and contract findings

CONTENT_IDENTITY, AUTHORITY_IDENTITY, INSTANCE_IDENTITY, RELEASE_IDENTITY, CANONICAL_OBJECT_IDENTITY, WORKAUTHORIZATION_ID and BINDING_DIGEST are separate domains. A digest's syntax is never a substitution rule. Undefined field semantics remain undefined, including runtime/implementation equivalence and some authority-versus-policy representations.

WP-08 explicitly separates released profile content `83b8cbc0…` from root authority `bffbdf78…`, release authority `ec39636d…`, and ProgrammerProfile projection `0a0718f2…`. `profile_sha256` selects content. `execution_profile` instead requires canonical JSON runtime specification from concrete binding/acceptance inputs; it is not another profile identity.

| Finding | Retained disposition |
|---|---|
| WP01-binding: Canonical current binding producer/object gap | OPEN; [E1_TEMPLATE1_CLOSURE_WP01_RESULT.md](E1_TEMPLATE1_CLOSURE_WP01_RESULT.md) |
| WP03-head: Current R4/G4 head authority/publication missing | OPEN; [E1_TEMPLATE1_CLOSURE_WP03_RESULT.md](E1_TEMPLATE1_CLOSURE_WP03_RESULT.md) |
| WP04-supervisor: Historical supervisor release/context bindings stale | OPEN; [E1_TEMPLATE1_CLOSURE_WP04_RESULT.md](E1_TEMPLATE1_CLOSURE_WP04_RESULT.md) |
| WP06-audit: Current namespace authority missing | OPEN; [E1_TEMPLATE1_CLOSURE_WP06_RESULT.md](E1_TEMPLATE1_CLOSURE_WP06_RESULT.md) |
| WP09-context: JSON/runtime context hydration mismatch | OPEN; [E1_TEMPLATE1_CLOSURE_WP09_RESULT.md](E1_TEMPLATE1_CLOSURE_WP09_RESULT.md) |
| WP09-governance: OperationalBinding missing governance member | OPEN; [E1_TEMPLATE1_CLOSURE_WP09_RESULT.md](E1_TEMPLATE1_CLOSURE_WP09_RESULT.md) |
| WP10-argv: JSON list versus runtime tuple mismatch | SUPERSEDED_BY_LOCAL_REPAIR; [E1_TEMPLATE1_CLOSURE_WP10_RESULT.md](E1_TEMPLATE1_CLOSURE_WP10_RESULT.md) |
| WP10-bins: Independent exec_bins mapping gap | OPEN; [E1_TEMPLATE1_CLOSURE_WP10_RERUN_1_RESULT.md](E1_TEMPLATE1_CLOSURE_WP10_RERUN_1_RESULT.md) |
| WP11-transmission: Payload clearance / task-context consumer mapping gap | OPEN; [E1_TEMPLATE1_CLOSURE_WP11_RESULT.md](E1_TEMPLATE1_CLOSURE_WP11_RESULT.md) |
| WP12-policy: Canonical ignored-input policy undefined | OPEN; [E1_TEMPLATE1_CLOSURE_WP12_RESULT.md](E1_TEMPLATE1_CLOSURE_WP12_RESULT.md) |
| WP13-identity: T1 content identity not authenticated by inspected boundary | OPEN; [E1_TEMPLATE1_CLOSURE_WP13_RESULT.md](E1_TEMPLATE1_CLOSURE_WP13_RESULT.md) |

The argv transformation is locally regression-qualified and explicitly preserves order, duplicate commands and literal strings. It does not resolve independent exec_bins or full source qualification. Historical list/tuple mismatch evidence remains; the repair supersedes only that finding. No full T1 schema, identity validation, source map or pure shared validator is invented by this graph.

WP-01's exception is restored to the knowledge inventory because its result explicitly reports it; later cumulative omission is retained as a documentation discrepancy, not silently rewritten. Historical supervisor observations remain distinct from current applicable authority.

## Prerequisite projection and preservation

The 49-node, 104-edge existing prerequisite projection is preserved exactly, is acyclic; raw DependsOn metadata has six pair discrepancies described below. Its two semantic correspondence edges remain non-prerequisites. Baseline node records, statuses and authority-update metadata are retained verbatim in the JSON. The expanded ordering view includes only REQUIRES edges explicitly marked ordering; bindings, applicability, evidence and identity-type relations are not promoted to prerequisite edges. Its semantic proposals are separate from the immutable baseline.

PC-01 proposes a separate current canonical T1 consumer-ready gate, retaining LIFECYCLE_TEMPLATE as semantics-qualified. Candidate-3 and production-contract records support this granularity distinction. It is not applied and no existing edge/status is removed. PC-02 proposes metadata reconciliation only: DependsOn still contains `G4_CURRENT → R4_CURRENT` and `OPERATIONAL_BINDING_CURRENT → INVOCATION_CANDIDATE`, which finalization explicitly demoted to semantic relations. It omits four edges present in PrerequisiteEdges: `CURRENT_PROVIDER_MODEL_AUTHORITY → FIRST_REAL_MODEL_REQUEST`, `E1_SCOPE → E1_TERMINAL`, `RELEASE_BB1808A → RELEASE_AUTHORITY_CURRENT`, and `RELEASE_C43F119 → RELEASE_AUTHORITY_CURRENT`. The designated PrerequisiteEdges stays authoritative for this projection; no topology/status change is applied.

Baseline source/currentness descriptions that conflict with later SATISFIED metadata are surfaced without automatic correction.

## Retrospective preflight

Only four failures meet the prior-evidence test. Later code observations are not silently backdated. Generic earlier knowledge that a mapping was incomplete is not proof that the exact later consumer mismatch was known.

| Failure | Classification | Prior-evidence / limitation |
|---|---|---|
| Candidate 2 consumer-schema failure | `DETECTABLE_BY_EXPANDED_GRAPH` | Candidate 2 bytes existed before attempted issuance; historical R4 canonical artifact existed on 2026-09-19. Issuance report identifies the consumer as already qualified. No current code timestamp is used as proof. |
| Candidate 3 missing canonical T1 input | `DETECTABLE_BY_EXPANDED_GRAPH` | Candidate-3 report explicitly cites historical G4 blocked record and preceding consumer reconciliation. |
| Dispatcher frontier-selection failure | `DETECTABLE_BY_EXPANDED_GRAPH` | Review explicitly establishes that the baseline already contained these prerequisites before the experiment; current later statuses are not backdated. |
| WP-09 context/governance mismatch | `NOT_DETECTABLE_FROM_AVAILABLE_PRIOR_KNOWLEDGE` | Earlier contract names missing typed projections, but exact code-version availability establishing manifest/verify and governance checks before WP-09 is not pinned by the pre-operation records used here. |
| WP-10 independent exec_bins gap | `DETECTABLE_BY_EXPANDED_GRAPH` | Production contract explicitly predates closure plan/sweep and says deriving bins from argv is not authorized/defined. |
| WP-11 transmission mapping gap | `NOT_DETECTABLE_FROM_AVAILABLE_PRIOR_KNOWLEDGE` | Full-payload clearance and generic mapping absence were prior facts; the exact empty-initial-clearances producer/consumer code snapshot is first pinned by WP-11 in this evidence set. |
| WP-13 content-identity verification gap | `NOT_DETECTABLE_FROM_AVAILABLE_PRIOR_KNOWLEDGE` | Generic T1 identity-contract incompleteness predates WP-13; the exact separate issuance-validator trust comparison is first evidenced by WP-13 in this corpus. |

The JSON retains prior evidence separately from outcome reports, a graph rule for each case, and the reasoning for its classification. NOT_DETECTABLE_FROM_AVAILABLE_PRIOR_KNOWLEDGE means the exact historical version/order is not demonstrated by this corpus; it does not assert that static analysis could never detect the defect. No listed case is claimed to require production execution. Runtime recovery/freshness qualification still cannot be established by graph traversal alone.

## Manual synchronization protocol

A source raw-hash or canonical-identity change stales all assertions extracted from it. Keep the old snapshot and mark new/current applicability STALE_PENDING_REEXTRACTION; re-locate selectors and revalidate affected derivation and validator claims transitively. Even append-only plan changes require selector validation. Independently sufficient surviving evidence must be reviewed explicitly. Missing-source assertions are snapshot/domain-limited. Re-extraction cannot issue authority, change dependency status or consume Candidate-3 authority.

No GraphRAG or synchronization implementation is provided. This is a manual prototype with reproducible structural checks, not a production planner.

## Validation

Validated unique IDs, referential integrity, provenance for every entity/assertion, 43/2/41 inventory, explicit pipelines/missing links, root coverage/private witnesses, baseline edge preservation, metadata discrepancy detection and acyclicity, expanded ordering acyclicity, and unchanged input hashes. No adapter or production operation was executed. Candidate-3 authority remains valid/unconsumed as recorded.

## Requested report

```json
{
  "GRAPH_ENTITIES": 339,
  "GRAPH_ASSERTIONS": 958,
  "TEMPLATE1_SLOTS": 43,
  "RESOLVED_SLOTS": 2,
  "UNRESOLVED_SLOTS": 41,
  "ROOT_BLOCKERS": [
    "root:binding",
    "root:dispatch",
    "root:ancestry",
    "root:approval",
    "root:release",
    "root:context_id",
    "root:runtime",
    "root:implementation",
    "root:runtime_head",
    "root:supervisor",
    "root:audit",
    "root:payload",
    "root:retention",
    "root:budget",
    "root:lifecycle",
    "root:ignored",
    "root:paths",
    "root:exec_bins",
    "root:argv",
    "root:shell_network",
    "root:context_hydration",
    "root:context_projection",
    "root:execution_profile",
    "root:transport",
    "root:transmission",
    "root:governance",
    "gate:schema",
    "gate:validator_authority"
  ],
  "ARCHITECT_DECISIONS": [
    "root:runtime_head",
    "root:supervisor",
    "root:audit",
    "gate:validator_authority",
    "gate:construction_release",
    "root:ignored",
    "root:exec_bins"
  ],
  "IMPLEMENTATION_ACTIONS": [
    "root:context_hydration",
    "root:transmission",
    "root:governance",
    "gate:identity_check",
    "gate:validator"
  ],
  "DETERMINISTIC_ACTIONS": [
    "root:binding",
    "root:execution_profile",
    "root:dispatch",
    "root:release",
    "root:context_id",
    "root:runtime",
    "root:payload",
    "root:retention",
    "root:lifecycle",
    "root:paths",
    "root:argv",
    "root:shell_network",
    "root:context_projection",
    "root:transport"
  ],
  "PREFLIGHT_DETECTABLE_FAILURES": [
    "candidate2",
    "candidate3",
    "dispatcher",
    "wp10"
  ],
  "PROPOSED_DAG_CORRECTIONS": [
    "PC-01",
    "PC-02"
  ],
  "PRODUCTION_EFFECT": "NO"
}
```
