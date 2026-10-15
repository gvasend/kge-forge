# D01 A15 event-operand reconciliation 34

**PARTIAL.** A15's exact input role is recovered, but no retained descriptor qualifies at its sealed pre-state. No event was selected or manufactured. The frontier remains **109 resolved / 52 unresolved**, out of 161 tracked references.

Two references consume the same role: `D01-OBL:E2-A15_OPERANDS.event` and `D01-OBL:E2-A15_ORACLE.event`, each with one canonical variant/capsule and one native `core.apply_event(snapshot, supplied)` operation. The frozen purpose is post-reload source invalidation: each disjoint required source must be invalidated in an independent accepted knowledge/proof/authority state; dependent support becomes stale while ordering obligations remain, descendants are held/blocked, resume is false and later reload preserves invalidation.

The parameter name `.event` denotes a **SourceInvalidation input descriptor**, not a previous lifecycle occurrence. Native fields are only `changed: Tuple[ArtifactIdentity, ...]` and `expected_snapshot: ArtifactIdentity`. Scope, lineage, subject and provenance are supplied by the exact pre-state and qualified input ownership; inventing those as extra native descriptor fields would change the schema. No producer Action ID, parent_event, ledger position or occurrence identity is consumed by this input.

The exact [state/type contract](qualification/E2_P05_D01_A15_EVENT_RECONCILIATION_34/event-input-contract.json) pins pre-state `CONTENT_IDENTITY/planner-snapshot-v1:ce54ff49907abcad564ec0ddfe8c7a019fab129936172b67f4ce0ff5ed013586`, P03 prospective lineage/generation, and the post-root-proof bundle's existing 19-event history ending at `planner-event-v1:88fb01def0514728ab17bc53f3885448725cd5a968ede91c8a0e52ea7c98fcc6`. An equivalent state with another identity cannot satisfy the optimistic precondition.

`core.apply_event` applies the invalidation and returns a TransitionReport; it does not create or append an ExecutionEvent. Native `codec.record_result` separately applies the transition and records an occurrence with exact sequence, parent_snapshot, preceding parent_event, typed result and after_snapshot. For the unchanged 19-event bundle that sequence would be 20, but no future event or post-state identity is computed here. `codec.commit_event` additionally performs a persistence/HEAD transaction and is outside this package. Existing ledger inventory “root” markers identify the first ordered event for documentation only; they are not invented native ledger-root commitments or input operands.

The [retained evidence inventory](qualification/E2_P05_D01_A15_EVENT_RECONCILIATION_34/recovered-inventory.json) searches standalone and embedded JSON across docs and adapter artifacts. It finds **39 distinct SourceInvalidation bodies and 36 native invalidation occurrences**. Copies/containers are recorded losslessly and deduplicated by body/occurrence identity. Every body has a different expected Snapshot from the sealed A15 state. Whole ExecutionEvent candidates also have the wrong input type; projecting their `.result` does not repair the pre-state mismatch. Actual containing bundles provide ordered IDs, positions, parent/state, scope, lineage and policy evidence. Retained P03 accepted/typed-support invalidations are locally qualified analogues, not automatic applicability to the P04 post-root-proof capsule.

There is no requirement for an original historical A15 event already to exist. The frozen prospective qualification permits native source-invalidation application, but its input targets must first be sealed. The capsule carries 54 source pins and accepted knowledge/typed proofs; an informational provenance/support inventory records their roles without selecting a target or constructing a changed tuple. A15 requires every disjoint required source, so selecting one convenient retained source or occurrence would also omit required variants.

Qualification 31 produced persisted bundle/publication/process/restore evidence over a zero-event A14 frame; these are not Planner invalidation inputs or lifecycle events. A15 and A16 are independent variants: canonical A16 starts from restored A14 governed-unknown state, not the invalidated A15 accepted-support state. A16's corrected-Snapshot/capsule mismatch and unbound invalidation input remain unchanged.

Future input preparation is a static construction step, distinct from native transition/occurrence execution. Existing native support is available, but no selected A14/source/history/policy/engineering authorization grants A15 execution. The [unready prospective frontier](qualification/E2_P05_D01_A15_EVENT_RECONCILIATION_34/prospective-event-frontier.json) records the missing exact target partition, restore applicability, event-trace/persistence capture contract and independent acceptance/oracle requirements. **DECISION_REQUIRED = YES for future execution; DECISION_READY = NO.** No sufficiently pinned execution dossier or option is issued. APPLY_EVENT alone cannot satisfy a future claim of persisted occurrence/reload history.

Static negatives discriminate input type, producer/subject/pre-state domains, unexpected ledger/position fields, scope/lineage/provenance, report/Snapshot/A14 evidence substitution, foreign occurrence identity and future-existence claims. These are metadata controls; no native event body was constructed. Existing body structure and occurrence identity checks pass, and inventory/classification/no-selection are deterministic across seeds 0, 1, 7 and 101.

All 161 references are preserved. The first blocker remains A15_OPERANDS.event. The **next reference is A15_ORACLE.event**; after the affected pair comes A16_OPERANDS.event. No unrelated repair occurred. V3 remains selected with 51/51 SOURCE_BYTES instances, 128 frozen obligations and 220 prospective jobs. A14 qualification and persisted outputs are unchanged; no new save, qualification writer exit or cold reader occurred. E1/production are unchanged. Complete invocation preflight is NOT_RUN and output oracles remain 0/128.

```text
WORK_PACKAGE = E2-P05-D01-A15-EVENT-RECONCILIATION-34
RESULT = PARTIAL
OPERAND = E2-A15_OPERANDS.event
OWNING_OBLIGATIONS = ["D01-OBL:E2-A15_OPERANDS", "D01-OBL:E2-A15_ORACLE"]
OWNING_DISPATCHES = ["D01-DISPATCH:E2-A15_OPERANDS", "D01-DISPATCH:E2-A15_ORACLE"]
AFFECTED_REFERENCE_COUNT = 2
A15_PURPOSE = Post-reload source invalidation
EVENT_ROLE = INPUT_INVALIDATION_DESCRIPTOR; operative SourceInvalidation body, not an existing occurrence witness
EVENT_PRODUCER = Static fixture preparation defines the input; core.apply_event consumes it; codec.record_result later creates any ledger ExecutionEvent
EVENT_TYPE = adapter.planner.model.SourceInvalidation(changed, expected_snapshot)
EVENT_IDENTITY_DOMAIN = No native event ID consumed. changed[] use exact source ArtifactIdentity domains; expected_snapshot uses CONTENT_IDENTITY/planner-snapshot-v1. Event occurrence planner-event-v1 is separate.
PARENT_REQUIREMENT = Exact expected_snapshot equals sealed A15 pre-state; no parent_event operand on SourceInvalidation
LEDGER_REQUIREMENT = apply_event consumes no ledger/root/head/position and appends no event. If native occurrence recording is later selected, record_result binds exact preceding bundle head/parent Snapshot and sequence.
STATE_BOUNDARY = {"AFTER_INVALIDATION": "Unknown; not constructed or executed", "CONTEXT": {"$type": "EvaluationContext", "allowed_effects": [], "generation": "E2-P03-PROSPECTIVE-GENERATION-1", "lineage": "E2-P03-PROSPECTIVE-QUALIFICATION-1", "scope": "E2-QUALIFICATION-ONLY", "tick": 0}, "RETAINED_BUNDLE_EVENT_COUNT": 19, "RETAINED_BUNDLE_HEAD": {"$type": "ArtifactIdentity", "kind": {"$enum": "IdentityKind", "value": "CONTENT_IDENTITY"}, "namespace": "planner-event-v1", "sha256": "88fb01def0514728ab17bc53f3885448725cd5a968ede91c8a0e52ea7c98fcc6"}, "SNAPSHOT": {"$type": "ArtifactIdentity", "kind": {"$enum": "IdentityKind", "value": "CONTENT_IDENTITY"}, "namespace": "planner-snapshot-v1", "sha256": "ce54ff49907abcad564ec0ddfe8c7a019fab129936172b67f4ce0ff5ed013586"}}
RETAINED_DESCRIPTOR_COUNT = 39
RETAINED_NATIVE_INVALIDATION_EVENT_COUNT = 36
A15_EVENT_SELECTION_UNIQUE = NO
SELECTED_EVENT = None
HISTORICAL_EVENT_REQUIRED = NO
PROSPECTIVE_EVENT_PERMITTED = YES; qualification-native input/application/occurrence, no historical claim
A14_PERSISTENCE_EVENT_APPLICABLE = NO
A16_DEPENDENCY = None: A16 independently begins at restored A14 unknown-rule variant, not A15 post-invalidation state
STATIC_OPERAND_PREFLIGHT = NOT_RUN; no exact retained input bound. Retained body structural/occurrence identity checks PASS
DECISION_REQUIRED = YES; future native execution only, not to fabricate a preexisting witness
DECISION_READY = NO
DECISION_OPTIONS = []
NEGATIVE_SUITE = 18/18 PASS
DETERMINISM = PASS; seeds 0,1,7,101; identical candidates, classifications and no selection
PREVIOUSLY_RESOLVED = 109
RESOLVED_BY_A15_EVENT = 0
TOTAL_RESOLVED = 109
TOTAL_UNRESOLVED = 52
NEXT_UNRESOLVED_REFERENCE = D01-OBL:E2-A15_ORACLE.event; same unbound descriptor role
V3_SELECTED = YES
A14_PERSISTENCE_RERUN = NO
FULL_OUTPUT_ORACLES = 0/128
END_INTERFACES_BOUND = 4/6
P05_EXECUTION_READY = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
git diff --check = PASS
```
