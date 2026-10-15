# D01 A15 required-support semantics recovery 38

**PARTIAL. Primary gap: MISSING_CONSUMER_ROOT_OWNERSHIP.** The recovered contracts name scoped required-support relationships, but they do not assign A15 to one, all or a contract-defined subset of those owners. Therefore no complete REQUIRED_SUPPORT(source, consumer, root, state) predicate or target set is recovered. No projection is selected and the frontier remains **109 resolved / 52 unresolved**.

This package recovers rule provenance rather than another source-count heuristic. The [fourteen-term provenance table](qualification/E2_P05_D01_A15_REQUIRED_SUPPORT_SEMANTICS_RECOVERY_38/contract-provenance.json) distinguishes explicit frozen/scoped contract requirements, native implementation constraints/behavior and local qualification recipes. Native behavior is not promoted to target-selection authority.

**Traceable scoped ownership.** FINISH-F02 explicitly requires actual current E2-K-REENTER as slot proof support; separately admitted E2-SLOT proof supports the E2-ROOT contract/proof; E2-ROOT is a CONDITION_SATISFIED prerequisite of E2-FINISH. The frozen graph contains the exact native contracts/proofs, their support fingerprints, authority references, target identities, scope/lineage/generation and independent source provenance. This is an explicit scoped ownership chain, not an inference from graph proximity. PC02 independently binds ROOT_PROOF to E2-ROOT, SLOT_PROOF to E2-SLOT and GRANT applicability to E2-REENTER. PC03 separately defines knowledge, root, slot, grant, external-route and receipt invalidation outcomes.

**What the rules actually require.** FINISH-F02's invalidation-dependency normalization uses only matching active configuration/contract descriptors; affected concrete contract IDs/targets and the original dependency feed bounded E06 reevaluation. Source/support invalidation withdraws live proof usability and recomputes affected FINISH. Native typed-proof usability requires accepted proof/contract, current installed role, matching context/expiry/authority/support fingerprints and retained prerequisites. A proof source's provenance can therefore be operational support in its explicit contract; it is not safe to declare every provenance field optional. Conversely, an arbitrary provenance or source_additions association does not prove that the A15 case must invalidate it.

**Why ownership is still missing.** The frozen A15 text says restored accepted knowledge/proof/authority state and “each disjoint required source.” It does not designate FINISH's root chain as the whole A15 subject, state that every PC03 role belongs to A15, or map knowledge/authority/receipt consumers into a complete owner set. The existence of one Goal targeting E2-ROOT cannot resolve that normative case mapping. Selecting only FINISH, all current records, or a smaller role slice would introduce a rule absent from the source. Scoped support necessity is recovered; its A15 universe is not.

The [source-role classification](qualification/E2_P05_D01_A15_REQUIRED_SUPPORT_SEMANTICS_RECOVERY_38/source-role-classification.json) records exact identities/associations and contract citations for all 54 source pins, including scoped proof-source owners where explicitly matched. It gives no unsupported must/must-not A15 verdict. The four declaration-only references cannot become required support by declaration alone. The 45-source provenance view cannot become target coverage by proximity. The 14-source type slice cannot become the required consumer universe by size. Optional versus required, historical versus current and superseded versus active must be decided by each owning contract and currentness rule, not retention or list position.

**Dependency direction versus selection.** The normative F02 chain is source/support -> matching contract/proof -> E2-ROOT -> consuming FINISH prerequisite. Native invalidation propagates forward through affected assertions, predicates, support and descendants. Discovering sources from an owning consumer/root would be a reverse query with a qualified necessity predicate; it is not native invalidation traversal. The graph's generic recorded-reference edges do not all assert required support, and reversing them does not create the missing rule.

**Closure.** Native staleness and affected-action closures are finite monotone fixed points. Changed identities deduplicate through frozenset; shared support may fan out to several consumers; cycles do not cause unlimited growth in those set computations, while independent structural validity rules remain applicable. These are effect-closure semantics after targets are supplied. They do not establish direct-only targets, a transitive source target set, all-support enumeration or a minimal invalidating cut for A15. That target-closure criterion remains missing.

**Disjointness and state.** SourceInvalidation consumes exact CONTENT_IDENTITY targets; semantic authority or occurrence identity cannot substitute. Distinct physical paths do not prove distinct content identity. The local P03 recipe demonstrates independent singleton source trials, but does not define A15's complete pairwise/group/protected-set/effect-disjointness rule at the installed P04 boundary. Membership must refer to the exact sealed A15 pre-state `ce54ff49...013586`, with its P03 prospective scope/lineage/generation; later or historical state membership cannot be imported. Current-state commitment is recovered, while consumer ownership/role necessity/closure/disjointness remain incomplete.

For **14, 45 and 49**, MATCHES_NORMATIVE_RULE remains **UNDETERMINED**. Exact normative false inclusions/exclusions cannot be computed without the rule. What is provable is the insufficiency of their inclusion arguments: P49 includes source-addition declarations, P45 records provenance incidence, and P14 filters record types. The verified subset relationships remain unchanged; no target set reconstruction runs.

The [normative-gap dossier](qualification/E2_P05_D01_A15_REQUIRED_SUPPORT_SEMANTICS_RECOVERY_38/normative-gap-dossier.json) asks for a separate contract-definition resolution: exact A15 consumer/root identifiers and one/all/subset coverage, per-owner operative/current source necessity, target closure mode and disjointness partition. It contains no 14/45/49 options and no unsupported predicate presented as qualified. **DECISION_REQUIRED = YES for that normative definition; DECISION_READY = NO.** No execution authority is issued.

Twenty static negatives and four-seed reconstruction pass. Incomplete predicates, wrong owners/directions/context/content domains, physical-path disjointness, source-role/count/order heuristics and implementation-as-authority promotions fail closed. All 161 tracked references are preserved, with no promotion; A15_OPERANDS.event remains next. Descriptor, full independent state/proof/control/resume/ordered-trace oracle and execution contract remain incomplete. Record_result -> save_bundle -> restore stays the recovered capture boundary. A16 remains independently rooted in restored A14; no new A15-to-A16 dependency is established.

V3, 128 obligations, 220 dispatch jobs, A14 PASS/persisted evidence, the 131/474/54 graph, source identities and frozen E1 are unchanged. No descriptor, expected-output values, append, save, restore, invalidation or native case is created/executed. Full-output oracles remain 0/128; END remains 4/6 and P05 execution readiness NO. The stop condition is observed.

```text
WORK_PACKAGE = E2-P05-D01-A15-REQUIRED-SUPPORT-SEMANTICS-RECOVERY-38
RESULT = PARTIAL
GRAPH_NODES = 131
GRAPH_ASSOCIATIONS = 474
SOURCE_PINS = 54
SOURCE_ROLE_CLASSIFICATION = {"A15_REQUIRED_MEMBER_TRUTH": "UNDETERMINED until case owning root/consumer scope is specified", "DECLARATION_AND_PROVENANCE_ALONE_ARE_NOT_TARGET_PROOF": true, "PATH": "docs/plans/qualification/E2_P05_D01_A15_REQUIRED_SUPPORT_SEMANTICS_RECOVERY_38/source-role-classification.json", "SCOPED_REQUIRED_SUPPORT_RULES_RECOVERED": true, "SOURCES": 54}
DEPENDENCY_DIRECTION = {"CASE_WIDE_TARGET_DEPENDENCY_RULE_COMPLETE": false, "INVALIDATION_EFFECT_DIRECTION": "source/dependency -> supported objects -> consuming/held descendants", "REVERSE_TRAVERSAL_IS_NOT_NATIVE_INVALIDATION": true, "SCOPED_NORMATIVE_CHAIN": ["root source content identity -> root contract/proof provenance.identity -> E2-ROOT", "actual slot support -> root contract -> E2-ROOT", "E2-ROOT -> FINISH CONDITION_SATISFIED prerequisite via native implicit project edges"], "SUPPORT_DISCOVERY_DIRECTION": "consumer/root -> declared required supports would be a reverse query, but its A15 owner and qualifying edge predicate are absent"}
CLOSURE_SEMANTICS = {"CYCLES_TERMINATION": "Finite monotone set stabilization prevents growth forever; independent native structural/model validity still applies; no cycle acceptance invented", "DUPLICATES": "changed converted to frozenset; identical content source references share one seed identity", "MINIMAL_CUT_RULE_RECOVERED": false, "MISSING": "Specify direct/transitive/all-support/minimal-cut or another exact target criterion for the A15 owning roots", "NATIVE_EFFECT_CLOSURE": "Monotone finite staleness/reachability fixed points in codec.invalidate_sources and typed_proofs.affected_actions; native predicates/alternatives/currentness govern propagation", "NORMATIVE_TARGET_TRANSITIVE_CLOSURE_RECOVERED": false, "SHARED_SUPPORT": "One seed may fan out to several consumers; does not prove effect-disjoint target branches", "TARGET_CLOSURE_MODE": null}
DISJOINTNESS_SEMANTICS = {"COMPLETE": false, "FULL_A15_PAIRWISE_GROUP_PROTECTED_SET_OR_EFFECT_RULE": null, "IDENTITY_DOMAIN": "Full source CONTENT_IDENTITY kind/namespace/hash, not physical path or event ID", "LOCAL_SINGLETON_RECIPE": true}
STATE_APPLICABILITY = {"COMPLETE_FOR_STATE_COMMITMENT": true, "CONTEXT": {"$type": "EvaluationContext", "allowed_effects": [], "generation": "E2-P03-PROSPECTIVE-GENERATION-1", "lineage": "E2-P03-PROSPECTIVE-QUALIFICATION-1", "scope": "E2-QUALIFICATION-ONLY", "tick": 0}, "EXPECTED_SNAPSHOT": {"$type": "ArtifactIdentity", "kind": {"$enum": "IdentityKind", "value": "CONTENT_IDENTITY"}, "namespace": "planner-snapshot-v1", "sha256": "ce54ff49907abcad564ec0ddfe8c7a019fab129936172b67f4ce0ff5ed013586"}, "RULE": "Exact restored A15 accepted pre-state; no historical or future state substitution"}
REQUIRED_SUPPORT_PREDICATE = None
REQUIRED_SUPPORT_PREDICATE_COMPLETE = NO
CANDIDATE_14 = {"COUNT": 14, "FALSE_EXCLUSIONS": null, "FALSE_INCLUSIONS": null, "MATCHES_NORMATIVE_RULE": "UNDETERMINED", "PROVABLE_LIMIT": "Provenance/type-slice association is not A15 root-necessity proof"}
CANDIDATE_45 = {"COUNT": 45, "FALSE_EXCLUSIONS": null, "FALSE_INCLUSIONS": null, "MATCHES_NORMATIVE_RULE": "UNDETERMINED", "PROVABLE_LIMIT": "Provenance/type-slice association is not A15 root-necessity proof"}
CANDIDATE_49 = {"COUNT": 49, "FALSE_EXCLUSIONS": null, "FALSE_INCLUSIONS": null, "MATCHES_NORMATIVE_RULE": "UNDETERMINED", "PROVABLE_LIMIT": "Contains declaration-only references with no necessity proof"}
TARGET_SELECTION_UNIQUE = NO
SELECTED_TARGET_SET = None
MISSING_NORMATIVE_TERMS = ["MISSING_CONSUMER_ROOT_OWNERSHIP", "MISSING_SOURCE_ROLE_PREDICATE", "MISSING_CLOSURE_RULE", "MISSING_DISJOINTNESS_RULE"]
PRIMARY_NORMATIVE_GAP = MISSING_CONSUMER_ROOT_OWNERSHIP
FIRST_MISSING_RULE = Exact A15 case mapping: which named accepted consumers/roots (one/all/subset), under which source-role necessity and target-closure rule. F02 FINISH ownership is not stated to exhaust A15 knowledge/authority/receipt invalidation coverage.
A15_DESCRIPTOR_COMPLETE = NO
A15_FULL_OUTPUT_ORACLE_COMPLETE = NO
CONTRACT_PROVENANCE = docs/plans/qualification/E2_P05_D01_A15_REQUIRED_SUPPORT_SEMANTICS_RECOVERY_38/contract-provenance.json
NEGATIVE_SUITE = 20/20 PASS
FOUR_SEED_DETERMINISM = PASS; ownership, role classification, direction/closure, candidate comparison and provenance identities stable. Target reconstruction NOT_RUN because normative predicate incomplete.
DECISION_REQUIRED = YES
DECISION_READY = NO
PREVIOUSLY_RESOLVED = 109
TOTAL_RESOLVED = 109
TOTAL_UNRESOLVED = 52
NEXT_UNRESOLVED_REFERENCE = D01-OBL:E2-A15_OPERANDS.event
A15_EXECUTED = NO
A16_EXECUTED = NO
A14_PERSISTENCE_RERUN = NO
END_INTERFACES_BOUND = 4/6
P05_EXECUTION_READY = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
git diff --check = PASS
```
