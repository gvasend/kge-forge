# D01 SOURCE_BYTES.pin selection-contract reconciliation 32

Result: **PARTIAL**. The source-role contract is recovered, but its singular V2 operand cannot legitimately be bound to one aggregate representative. No source was selected; the operand frontier remains **58 resolved / 53 unresolved**.

The frozen obligation requires “Each current/prefix-available source; future additions excluded from earlier replay.” Its aggregate cardinality is all source dependencies for every selected checkpoint. V2 instead maps `D01-OBL:SOURCE_BYTES` to one `adapter.planner.codec.load_pinned(root, pin)` invocation. That native entrypoint correctly consumes exactly one `ArtifactPin`; the missing part is per-member runner orchestration. Closure 1's `common.py` encoded the reduction as `SOURCE_BYTES -> LOAD_PIN`, and Closure 2 preserved it in V2. The capsule carries a bundle and source collection, but no singular `pin`.

The [complete capsule inventory](qualification/E2_P05_D01_SOURCE_BYTES_PIN_RECONCILIATION_32/source-collection.json) records 51 exact pins, payload hashes, content identities, documentary positions, native provenance references and applicability contexts. All 51 are eligible required members; none is eligible to stand for the entire collection. This is the P04/P03 prospective capsule context, not the A14 ten-source context. The original recovery additionally names sixteen unselected checkpoint candidates; their pin/provenance inventories are recorded separately without merging lineages or selecting a replacement. A complete aggregate matrix still requires explicit checkpoint ownership.

Native `PersistenceBundle.sources` is unordered and unique by path/pointer/hash profile. Event-source availability is temporal: this capsule's exact prefix counts are 16, 16, 16, 18, 25, 27, 35, 37, 49 and 51. Event order remains unchanged. The selector policy is a separately versioned `POLICY` role. Native complete-bundle source validation checks all source pins plus that policy; this does not make the policy a primary SOURCE_BYTES source.

All eleven recovered runner-code candidates were inspected without execution. None seals a primary, first or last source for this obligation. Existing native `_verify_sources` enumerates the required source pins and policy, corroborating the all-members interpretation. No historical runner was adopted. The original PC04/acceptance contracts and the frozen 128-obligation inventory supply no singular preference discriminator.

The defect is **CARDINALITY_MODELING_ERROR / DISPATCH_ADAPTER_GAP**, classified as **RUNNER_CONTRACT_DEFECT**. Choosing any one member changes the invocation/content comparison subject and omits fifty current dependencies. It would violate the frozen coverage requirement, rather than settle a legitimate choice among equally valid aggregate representatives.

The [sealed minimum correction proposal](qualification/E2_P05_D01_SOURCE_BYTES_PIN_RECONCILIATION_32/dispatch-correction-proposal.json) expands the source collection into singular native LOAD_PIN jobs per required member and owned prefix. Membership must be exact; zero, missing, duplicate, foreign or future-at-earlier-prefix members fail closed. Canonical presentation stabilizes job records without making source order semantic. Results are captured by checkpoint, prefix and exact pin identity; independent expected output values remain unconstructed. Native Planner semantics and source state need no change.

The proposal is not applied: the authoritative V2 dispatch and capsules remain unchanged. Applying it must produce new runner/dispatch, invocation and future matrix identities and independently validate the affected row. No bounded single-source decision is offered because no such option preserves the authoritative obligation. The deterministic all-members correction requires no new source-choice authority; this finding grants no execution or scope authority and does not choose broader checkpoint candidates.

Static controls reject ordinal selection, missing/multiple membership, wrong role/identity/provenance, foreign/cross-case sources, collection-as-singular input, A14 persistence artifact substitution and premature source availability. Original, reversed, rotated and four-seed presentations leave the no-selection outcome and proposed complete projections invariant. Native pin type/domain, canonical paths and retained hashes passed for all 51 members. LOAD_PIN and qualification operations were not invoked.

The [111-reference audit](qualification/E2_P05_D01_SOURCE_BYTES_PIN_RECONCILIATION_32/operand-frontier.json) preserves every binding and unresolved reference. SOURCE_BYTES remains first pending dispatch cardinality correction. The next exact unresolved reference in the preserved audit order is **D01-OBL:E2-A15_OPERANDS.event**, whose invalidation-target source identity remains unsealed; its oracle counterpart follows. A16 is not next and remains unchanged with its Snapshot mismatch and unbound invalidation event.

A14 qualification evidence and both persisted bundle/handoff pairs remain unchanged. No new save, writer termination, cold reader, A14/D01 execution or output-oracle construction occurred. E1 and production remain untouched. Complete invocation preflight is NOT_RUN; output oracles remain 0/128; END remains 4/6.

```text
WORK_PACKAGE = E2-P05-D01-SOURCE-BYTES-PIN-RECONCILIATION-32
RESULT = PARTIAL
OPERAND = SOURCE_BYTES.pin
OWNING_OBLIGATIONS = ["D01-OBL:SOURCE_BYTES"]
OWNING_DISPATCHES = ["D01-DISPATCH:SOURCE_BYTES"]
SEMANTIC_ROLE = Every required native source availability/pinned-byte member at its current or owned event-prefix boundary; not a primary source or mutation target
EXPECTED_TYPE = ArtifactPin
EXPECTED_CARDINALITY = 1
SOURCE_COLLECTION_COUNT = 51
COLLECTION_SEMANTICS = Native unordered/set-like pins keyed by (path,pointer,profile); temporal availability and causal event history ordered
SELECTION_RULE_RECOVERED = NO
SELECTION_RULE = No rule selecting exactly one aggregate representative. Authoritative rule is FOR_EACH current/prefix-available source.
SOURCE_BYTES_PIN_SELECTION_UNIQUE = NO
DISPATCH_PROJECTION = qualification-source-bytes-dispatch-correction-v1:bc5c21c942a48361f2d9907c0a030ed636ee8384ae3fc1855c7ff306e1a7fa17
STATIC_OPERAND_PREFLIGHT = NOT_RUN; no unique singular operand bound
AMBIGUITY_CLASSIFICATION = RUNNER_CONTRACT_DEFECT
DECISION_REQUIRED = NO
DECISION_READY = NO
DECISION_OPTIONS = []
NEGATIVE_SUITE = 21/21 PASS
DETERMINISM = PASS; seeds 0,1,7,101; invariant inventory/eligibility/unresolved singular outcome and proposed projections
PREVIOUSLY_RESOLVED = 58
RESOLVED_BY_SOURCE_BYTES_PIN = 0
TOTAL_RESOLVED = 58
TOTAL_UNRESOLVED = 53
NEXT_BLOCKER = {"CURRENT": "SOURCE_BYTES_PIN_CARDINALITY_CORRECTION", "NEXT_AFTER_SOURCE_BYTES": {"GAP": "EXACT_INVALIDATION_TARGET_SOURCE_IDENTITY_NOT_SEALED; baseline alone does not establish role", "OBLIGATION_ID": "D01-OBL:E2-A15_OPERANDS", "OPERAND": "event"}, "OBLIGATION_ID": "D01-OBL:SOURCE_BYTES"}
A16_SNAPSHOT_IDENTITY_MISMATCH = PRESERVED
A16_INVALIDATION_EVENT = UNBOUND
FULL_OUTPUT_ORACLES = 0/128
END_INTERFACES_BOUND = 4/6
P05_EXECUTION_READY = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
git diff --check = PASS
```
