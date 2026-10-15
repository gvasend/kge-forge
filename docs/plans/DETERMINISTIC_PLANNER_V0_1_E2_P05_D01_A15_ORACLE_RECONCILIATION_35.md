# D01 A15 oracle-event reconciliation 35

**PARTIAL.** The ORACLE row's `.event` field is a native invocation input, not the independent expected oracle. The oracle contract is recovered, but no concrete expected values or exact descriptor are independently sealable now. Accounting remains **109 resolved / 52 unresolved, 161 references**.

One reference consumes `D01-OBL:E2-A15_ORACLE.event`. V3 dispatches that row to `core.apply_event(snapshot, supplied)`, with the same operative bindings and canonical case variant/capsule as the OPERANDS row. `supplied` must be SourceInvalidation, cardinality one per concrete invocation. This is not an ExecutionEvent witness or an expected event. The frozen ORACLE role separately requires `ExpectedFullStateAndNegativeInvariants`, one independent exact full oracle per variant. The runner opens `row.oracle_reference.expected_full_output` only after native invocation and capture. That concrete oracle reference/value is not sealed.

The relationship is **same logical operative-input projection on two distinct job rows, with a separate independent output oracle**. The frozen roles remain distinct and neither reference is collapsed. An expected Snapshot/event/descriptor cannot be fed into `.event` just because the row is named ORACLE. The native input still has only changed content-source identities and expected_snapshot; it has no reason, route, receipt, parent-event or occurrence-ID field.

The [closed comparison schema](qualification/E2_P05_D01_A15_ORACLE_RECONCILIATION_35/oracle-field-domains.json) has sixteen captured fields: full typed Snapshot/bundle/native result; complete Computation/selection/branches/witnesses/rejections/resume; policy/source pins; exact Snapshot/bundle/event identities; qualification label and closed output_field_set. Nested native schemas are pinned. Only declared native unordered collections are canonicalized; causal/event/policy order is exact. `resume=false` alone, a descriptor body, one occurrence, a Snapshot or report cannot satisfy this full oracle.

The exact A15 pre-state remains `planner-snapshot-v1:ce54ff49907abcad564ec0ddfe8c7a019fab129936172b67f4ce0ff5ed013586`, in the P03 prospective lineage/generation with P06 policy and PARTIAL_HISTORICAL_REPLAY. The qualified A14 corrected state is `7ec95347...ab66b9` in a governed-unknown variant. They are separate state boundaries, not aliases. Every retained invalidation body's expected Snapshot differs from A15's boundary. Future transition creation changes post-state only; it cannot legalize a wrong optimistic pre-state commitment.

The [independent retained search](qualification/E2_P05_D01_A15_ORACLE_RECONCILIATION_35/recovered-oracle-contract.json) separates 39 descriptor bodies, 36 native invalidation occurrences, one result projection, 44 Snapshot projections, nine reports and six authored local P03 oracles. No complete expected_full_output candidate exists. Retained bodies/occurrences have wrong pre-states or types; Snapshot/result/report projections are partial or producer-derived. The authored P03 oracles govern different local checkpoint boundaries and lack the complete A15 invalidation schema. No candidate was selected by similarity, chronology or proximity.

The [descriptor constraints](qualification/E2_P05_D01_A15_ORACLE_RECONCILIATION_35/descriptor-constraints.json) uniquely fix expected_snapshot and the CONTENT_IDENTITY kind of each changed source. Native invalidate_sources rejects authority/occurrence identity substitution. Exact target/pin/proof/receipt dependency ownership and the disjoint variant partition remain unsealed; the oracle's required effects constrain them but do not uniquely choose members. Scope, lineage, generation, source provenance and policy applicability come from the exact A15 state and retained pin contracts. Route/receipt selectors and an invalidation-reason field are not invented in SourceInvalidation.

The [post-state contract](qualification/E2_P05_D01_A15_ORACLE_RECONCILIATION_35/post-state-contract.json) requires dependent support to become stale, affected descendants held/blocked, resume false, ordering obligations retained and invalidation preserved after reload. Native invalidation propagates through assertions, entity/knowledge/predicate/receipt/installation/proof dependencies and typed reevaluation. Exact resulting states, witnesses, reasons, control and identities depend on the still-unbound changed source. Therefore **A15_ORACLE_DERIVABLE = NO** for a complete concrete oracle. Reading unchanged native semantics does not supply missing inputs or an independent complete model. No future/case/runner output was used; actual oracle independence is not evaluated because no expected values were derived.

A descriptor is required before application. Full original A15 bundle/event-trace/reload acceptance additionally requires observing the new native transition/occurrence and durable invalidation, not supplying an old event witness. Current V3 APPLY_EVENT alone returns TransitionReport without updating the input bundle; capture reads bundle/resume/ledger from the prior bundle. That path cannot by itself prove appended, persisted invalidation. The gap is recorded without changing V3 or introducing a save/history transaction. No new descriptor, native occurrence or output expectation is constructed.

A15 provides no output to A16 under the authoritative canonical contract: A16 independently consumes the restored A14 unknown-rule state and its own route-source invalidation descriptor. A16's existing Snapshot mismatch and unbound event remain untouched.

Twenty static negatives and four-seed reconstruction pass. Both A15 input and complete oracle contracts still lack exact values, so **A15_EXECUTION_CONTRACT_READY = NO** and **DECISION_READY = NO**. Future native execution requires authority, but no vague execution dossier is created. The next current reference remains A15_OPERANDS.event, followed by A15_ORACLE.event; A16 work has not begun.

V3, its 51 source instances, all 128 frozen obligations, 220 prospective jobs, A14 qualification and persisted evidence remain unchanged. No A15/A16/D01 case or persistence sequence ran. E1/production are unchanged. Full invocation preflight is NOT_RUN and output oracles remain 0/128.

```text
WORK_PACKAGE = E2-P05-D01-A15-ORACLE-RECONCILIATION-35
RESULT = PARTIAL
OPERAND = E2-A15_ORACLE.event
ORACLE_SEMANTIC_TYPE = ExpectedFullStateAndNegativeInvariants / independent closed full-output envelope; .event on this job is an operative input, not the expected oracle
ORACLE_IDENTITY_DOMAIN = Field-specific exact native post-Snapshot/bundle/event/source/policy identities plus full typed-state/result/computation/proof/selection/resume content; input descriptor fields are separate domains
A15_INPUT_ORACLE_RELATIONSHIP = OTHER: same logical input projection on two distinct obligation/job rows; independent expected_full_output is a separate object, not .event. References and duties are not collapsed.
A15_PRE_STATE = {"A14_CORRECTED_SNAPSHOT_MATCH": false, "CONTEXT": {"$type": "EvaluationContext", "allowed_effects": [], "generation": "E2-P03-PROSPECTIVE-GENERATION-1", "lineage": "E2-P03-PROSPECTIVE-QUALIFICATION-1", "scope": "E2-QUALIFICATION-ONLY", "tick": 0}, "MISMATCH_CLASSIFICATION": "Separate accepted-support versus A14 governed-unknown variants; plus unsealed prospective A15 input descriptor. Wrong input pre-state is not legitimized by future A15 transition.", "POLICY_VERSION": "E1-SELECTION-1-P06", "REPLAY_SCOPE": "PARTIAL_HISTORICAL_REPLAY", "SNAPSHOT_ID": {"$type": "ArtifactIdentity", "kind": {"$enum": "IdentityKind", "value": "CONTENT_IDENTITY"}, "namespace": "planner-snapshot-v1", "sha256": "ce54ff49907abcad564ec0ddfe8c7a019fab129936172b67f4ce0ff5ed013586"}}
A15_OPERATION = core.apply_event(snapshot, SourceInvalidation descriptor); full original persistence/event-trace acceptance additionally needs independently sealed native recording/reload boundary
ORACLE_FIELDS = ["Computation", "branches", "bundle_identity", "event_identities", "native_result", "output_field_set", "policy", "qualification_label", "rejections", "resume", "selection", "snapshot_identity", "source_pins", "typed_bundle", "typed_snapshot", "witnesses"]
ORACLE_COMPARISON_MODE = Exact complete normalized expected_full_output equality; native SET_FIELDS canonicalize only unordered membership, ordered event/causal/policy/input sequences exact; process evidence compared separately
CANDIDATE_COUNTS = {"COMPLETE_EXPECTED_OUTPUT_CANDIDATES": 0, "DESCRIPTORS": 39, "INDEPENDENT_LOCAL_ORACLES": 6, "OCCURRENCES": 36, "REPORTS": 9, "RESULT_EVENT_PROJECTIONS": 1, "SNAPSHOTS": 44}
A15_ORACLE_SELECTION_UNIQUE = NO
A15_ORACLE_DERIVABLE = NO
ORACLE_INDEPENDENCE = NOT_EVALUATED_NO_CONCRETE_ORACLE_DERIVED; contract sources independently recovered without case/runner execution
DESCRIPTOR_CONSTRUCTION_FEASIBILITY = Exact retained descriptor absent. Pure static preparation possible only after exact disjoint target/variant ownership is sealed; complete descriptor not derivable now; no native construction/execution here.
DESCRIPTOR_REQUIRED = YES
NATIVE_OCCURRENCE_REQUIRED = YES for full persisted ordered-event/reload A15 acceptance; NO as a preexisting input witness
A15_OUTPUT_TO_A16 = NONE; A16 starts independently from restored A14 governed-unknown variant, not A15 invalidated accepted-support output
A16_REQUIRED_IDENTITY_DOMAIN = Its own exact restored A14 pre-Snapshot commitment and SourceInvalidation changed content-source identities; does not consume A15 event/occurrence ID
NEGATIVE_SUITE = 20/20 PASS
DETERMINISM = PASS; seeds 0,1,7,101; contract/inventories/classifications/no-selection identical
A15_EXECUTION_CONTRACT_READY = NO
DECISION_REQUIRED = YES for future native execution, not for selecting a lookalike oracle
DECISION_READY = NO
PREVIOUSLY_RESOLVED = 109
RESOLVED_BY_A15_ORACLE = 0
TOTAL_RESOLVED = 109
TOTAL_UNRESOLVED = 52
NEXT_UNRESOLVED_REFERENCE = D01-OBL:E2-A15_OPERANDS.event; then E2-A15_ORACLE.event; A16 not started
A15_EXECUTED = NO
A16_EXECUTED = NO
FULL_OUTPUT_ORACLES = 0/128
END_INTERFACES_BOUND = 4/6
P05_EXECUTION_READY = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
git diff --check = PASS
```
