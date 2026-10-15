# D01 A15 capture and full-output contract recovery 36

**PARTIAL.** Native transition/capture/persistence semantics and the acceptance conjunction are recovered. The exact disjoint target predicate remains unsealed, so no SourceInvalidation descriptor, local full-output oracle or execution dossier is created. The tracked frontier remains **109 resolved / 52 unresolved**.

The [sealed graph inventory](qualification/E2_P05_D01_A15_CAPTURE_OUTPUT_CONTRACT_36/accepted-support-graph.json) contains **131 nodes, 474 recorded associations and 54 native source pins**, bound to the exact A15 Snapshot and P03 prospective context. Nodes preserve native identities, records, source/provenance associations and typed dependency references; qualification node IDs are not native occurrence/authority identities. The full native records and pinned semantic definitions preserve predicate/typed-proof/installation distinctions. Recorded reference direction alone does not invent required-support necessity or an AND/OR cut.

The [target analysis](qualification/E2_P05_D01_A15_CAPTURE_OUTPUT_CONTRACT_36/target-contract.json) exhibits three deterministic but different diagnostic source projections: **45** current-provenance pins, **49** referenced/dependency/grant pins and **14** knowledge/proof/entity-role pins. None is selected. The local qualified P03 suite enumerates direct Provenance sources, but that local component rule is not an authoritative complete required-support partition for the P04 post-root-proof capsule. The frozen A15 text requires every disjoint required source without selecting a required-support root/consumer boundary or resolving provenance versus transitive installation/admission support. That missing rule, not list order, prevents target uniqueness.

Disjointness must distinguish exact content identities and isolate each target's variant from the same accepted pre-state. Different paths aliasing one content identity do not make distinct targets. Shared downstream dependency branches do not by themselves establish source disjointness. The SourceInvalidation native schema has only changed content identities and expected_snapshot. The exact expected_snapshot is fixed; changed members are not. Route, receipt, reason, scope, lineage and provenance are qualified context/dependency/output terms rather than invented native descriptor fields. No native descriptor identity field exists; a qualification-only body identity can be computed only once both fields are exact.

The [apply contract](qualification/E2_P05_D01_A15_CAPTURE_OUTPUT_CONTRACT_36/apply-event-contract.json) admits the native typed input, checks the exact optimistic Snapshot, requires CONTENT_IDENTITY targets, applies support staleness/withdrawal, propagates dependencies, performs native typed reevaluation and returns `TransitionReport(updated, (), recompute(updated))`. It does not append or persist an ExecutionEvent. Computation/control are derived; resume is later computed from a replay-valid updated bundle, sources, policy and actual reentry history, not a persisted permission Boolean.

The frozen requirement “reload preserves invalidation,” together with canonical before/after identities and ordered native event trace, requires a persisted occurrence for full A15 assurance. Existing native capability supplies it: **record_result -> save_bundle -> restore**. `record_result` owns the apply_event transition and native event construction/append. The caller must not apply first and feed a TransitionReport to recording or fabricate the event. Parent Snapshot is the exact pre-state, parent_event the exact existing head, sequence len(events)+1. For the unchanged A15 bundle, the retained 19-event prefix ends at `88fb01de...98fcc6` and the new occurrence would have sequence 20; its result/after-state/event identity are not computed here.

The [capture contract](qualification/E2_P05_D01_A15_CAPTURE_OUTPUT_CONTRACT_36/capture-contract.json) distinguishes pure immutable native construction from persistence. save_bundle publishes exact event files, native bundle and required archives using immutable fsync-before-link writes. Staged event/archive files may exist before final bundle publication; there is no multi-file atomic transaction or HEAD update in that path. Failure does not justify read eligibility; a complete successful return/publication verification is required. Native identical-file retry is different from repeating semantic execution. Exact per-row targets, publication/reader association and failure/retry evidence remain unsealed.

`commit_event` is an existing stronger alternative: local lock, authoritative parent/HEAD audit, native recording, bundle publication and atomic HEAD replacement with directory fsync. Frozen A15 does not mandate HEAD transaction atomicity. No backend, target, transaction or stronger durability claim is silently selected, and A14's narrower save-only guarantee remains unchanged. No native capability change is required; a future A15 dispatch/capture composition must independently satisfy the contract.

The [ordered-trace contract](qualification/E2_P05_D01_A15_CAPTURE_OUTPUT_CONTRACT_36/ordered-trace-contract.json) pins the actual 19-event prefix and the rule for one new native invalidation entry per independent variant. Computed TransitionReport, native occurrence, persisted event, causal ordering and qualification process metadata are distinct. No trace entry is manufactured. Branch-specific proof states, complete Computation/control, resume reasons/support and exact after-state/bundle/event identities depend on the unknown target partition. Therefore expected post-state/proof/control/resume values and the full local oracle remain absent. No prospective operation, replay, recomputation or mutable result was used to generate expected values.

The [acceptance conjunction](qualification/E2_P05_D01_A15_CAPTURE_OUTPUT_CONTRACT_36/acceptance-contract.json) requires exact pre-state and target coverage, correct stale/held/blocked effects, mandatory ordering, complete independent state/proof/control/resume comparison, canonical identities, native ordered occurrence, immutable persistence and reload preservation, determinism and unchanged scope/source/policy/provenance with no E1/authority leakage. Every term must pass; a local P03 scalar oracle cannot replace it.

There is **no native A15-output-to-A16 handoff** in the canonical cases. A16 begins from restored A14 governed-unknown state, independently of A15's accepted-support invalidation output. Post-state/descriptor/occurrence/proof/control/resume/trace artifacts from A15 are not A16 inputs. The existing A16 capsule mismatch is not explained by A15 and remains preserved.

Twenty-one metadata negatives and four-seed reconstruction pass. No native operating-authority token is created or required merely to define a static proof-withdrawal descriptor; future qualification execution and append/save/reader effects still require exact scope authority. The missing target rule, complete independent output and concrete capture/retry bindings keep **A15_EXECUTION_CONTRACT_READY = NO** and **DECISION_READY = NO**. No execution dossier is prepared.

All 161 references remain unchanged. The next blocker is A15_OPERANDS.event, then A15_ORACLE.event; A16 work is gated. V3, 51 source instances, 128 frozen obligations, 220 prospective jobs, A14 qualification/evidence, A15/A16 artifacts and frozen E1 remain unchanged. No descriptor/event/expected-output values were created; no native case, save, writer termination or cold reader ran. Global full-output oracles remain 0/128, END 4/6, P05 execution readiness NO.

```text
WORK_PACKAGE = E2-P05-D01-A15-CAPTURE-OUTPUT-CONTRACT-36
RESULT = PARTIAL
ACCEPTED_SUPPORT_GRAPH = {"EDGES": 474, "NODES": 131, "PATH": "docs/plans/qualification/E2_P05_D01_A15_CAPTURE_OUTPUT_CONTRACT_36/accepted-support-graph.json", "QUALIFICATION_DOMAIN": "Recorded native source/provenance/reference associations; mandatory-root/cut semantics not assumed", "SOURCE_NODES": 54}
GRAPH_IDENTITY = qualification-A15-support-graph-v1:36c6188226bfc396f85c97ca24492deabc7afbebb087f590d1037a1df58e5675
DISJOINT_SOURCE_RULE = Distinct exact source content identities in separate variant copies; alias paths with same content identity do not create independent targets. Overlapping descendant branches may share support; branch-disjointness is not established.
TARGETS_UNIQUE = NO
SOURCE_INVALIDATION_DESCRIPTOR = NOT_CONSTRUCTED; two-field schema recovered, expected_snapshot sealed; changed targets remain unsealed
DESCRIPTOR_IDENTITY = None
PERSISTED_OCCURRENCE_REQUIRED = YES
CAPTURE_ENTRYPOINT = codec.record_result(bundle, SourceInvalidation, snapshot_resolver=...) -> native updated bundle; codec.save_bundle -> immutable event/bundle publication; codec.restore -> later reconstruction
APPLY_CAPTURE_ATOMICITY = No stronger atomicity requirement recovered. Native record_result owns application/append; save publication is separate. commit_event provides existing lock/HEAD transaction if later explicitly selected; not required or used here.
EXPECTED_POST_STATE = None
EXPECTED_PROOF = None
EXPECTED_CONTROL = None
EXPECTED_RESUME = None
A15_FULL_OUTPUT_ORACLE_COMPLETE = NO
ORACLE_INDEPENDENCE = NOT_EVALUATED_NO_CONCRETE_ORACLE; contract-source recovery independent; no future/case/runner output used
A15_TO_A16_HANDOFF = {"A15_OUTPUT_TO_A16": null, "A16_DESCRIPTOR": "UNBOUND", "A16_MISMATCH": "PRESERVED", "A16_NATIVE_PRESTATE_OWNER": "Restored E2-A14 governed-unknown variant, independently sealed; not A15 accepted-support invalidation output", "A16_SNAPSHOT_MISMATCH_EXPLAINED_BY_A15": false, "DESCRIPTOR_ID_SUPPLIED": null, "EVIDENCE": {"CASE_ID": "E2-A16", "DETERMINISM_REQUIREMENT": "Repeat equal semantic inputs; canonical identities and full computation equal.", "EXPECTED_STATE": "PLAN_DEFECT when no other valid route; waiting label does not suppress defect", "INITIAL_STATE": "Restored E2-A14 variant", "NEGATIVE_INVARIANTS": "No E1 mutation, authority leakage, fabricated proof or bypass.", "OPERATION": "Invalidate required acquisition-contract source", "PERSISTENCE_REQUIREMENT": "Canonical before/after identities and event trace required.", "PURPOSE": "Governed route invalidation", "status": "PLANNED_NOT_EXECUTED"}, "OCCURRENCE_ID_SUPPLIED": null, "POST_STATE_ID_SUPPLIED": null, "PROOF_CONTROL_RESUME_SUPPLIED": null, "TRACE_REFERENCE_SUPPLIED": null}
A15_EXECUTION_CONTRACT_READY = NO
DECISION_REQUIRED = YES for future qualification execution/capture effects; no native operating-authority token for static proof-withdrawal descriptor
DECISION_READY = NO
DECISION_OPTIONS = []
NEGATIVE_SUITE = 21/21 PASS
DETERMINISM = PASS; graph, candidate predicates, descriptor schema, output frontier, trace and acceptance contracts stable under seeds 0,1,7,101. No concrete target/descriptor/oracle value exists.
PREVIOUSLY_RESOLVED = 109
RESOLVED_BY_A15_CONTRACT = 0
TOTAL_RESOLVED = 109
TOTAL_UNRESOLVED = 52
NEXT_UNRESOLVED_REFERENCE = D01-OBL:E2-A15_OPERANDS.event; then E2-A15_ORACLE.event; A16 gated
A15_EXECUTED = NO
A16_EXECUTED = NO
END_INTERFACES_BOUND = 4/6
P05_EXECUTION_READY = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
git diff --check = PASS
```
