# E2-P03 mainline checkpoint reproduction 1

WORK_PACKAGE = E2-P03-MAINLINE-CHECKPOINT-REPRODUCTION  
RESULT = BLOCKED  
CHECKPOINT_REPRODUCIBILITY = CONTRACT_INCOMPLETE

Stopped at **Step 4**: required immutable source/policy inputs and an event-backed start are missing. No reproduction transition ran, no bundle was created, and no runtime defect was established. Existing functional P03 continuation remains qualified within its previously recorded limits; E2_P03_RESULT remains PARTIAL.

## Exact checkpoint and boundary

CHECKPOINT_ID = E2-EXTERNAL-CHECKPOINT  
CHECKPOINT_PHASE = EXTERNAL_CHECKPOINT, post-authenticated RecordedDecision, original P03 A07/A08  
EXPECTED_STATE_ID = `8d77f7f1997ca884e07490c4c93f5fbe3a31b09278fd57c6c6ea1f9fa26b3aaf`  
EXPECTED_CONTROL = EXTERNAL_WAIT  
EXPECTED_SCOPE = E2-QUALIFICATION-ONLY  
EXPECTED_LINEAGE = E2-CANONICAL-BASELINE-1  
EXPECTED_GENERATION = E2-GENERATION-1

The [original P03 result](DETERMINISTIC_PLANNER_V0_1_E2_P03_RESULT.md) names this exact [mainline Snapshot](DETERMINISTIC_PLANNER_V0_1_E2_HUMAN_DECISION_ALLOW_POST_SNAPSHOT_1.json), rather than a later equivalent state. Native identity and recomputation were independently checked in this package: EXTERNAL_WAIT, no actionable Actions, validation rule known, absent evidence. All Action statuses and knowledge records, including their provenance/currentness fields, are listed exactly in the machine checkpoint contract. E2-COLLECT, CHECK, PREPARE and DECIDE are completed; REENTER and FINISH have their original non-actionable states. No later accepted E2-K-REENTER, SLOT_PROOF or ROOT_PROOF is introduced here.

The exact last qualified transition is authenticated native RecordedDecision admission/application, yielding the choice record, E2-GRANT and DECISION_RECORDED stage. The [retry trace](DETERMINISTIC_PLANNER_V0_1_E2_HUMAN_DECISION_ALLOW_RETRY_1_TRACE.json) binds earlier HUMAN_HANDOFF `9b3d8e6a…` to exact checkpoint `8d77f7f…`. This is a historical transition trace, not a native ExecutionEvent ledger. The next transition that has **not** occurred is EvidenceSourceAdmission/RECEIVED. Validation, proof, reentry and REENTER result are beyond this boundary. There is no unsupported assertion that a new external request event occurred after the recorded decision.

Expected source state is the exact Snapshot's source validity, gate/requirements/authority and provenance, with evidence/admissions/observations absent. Expected policy is described in [PC01 whole model](DETERMINISTIC_PLANNER_V0_1_E2_PC01_COMPLETION_1_WHOLE_MODEL.json) as `E1-SELECTION-1-P06 supported binding, exact content pin`; the exact pin/file is not supplied by that description.

## Required source and policy inventory

Every native Snapshot field is AUTHORITATIVELY_DEFINED by the immutable checkpoint file. Defaults omitted by the native codec are DERIVABLE only through its versioned schema. This defines canonical state, but does not supply a complete PersistenceBundle source index, selection policy, initial event state or ledger. The JSON inventories the complete serialized Action, knowledge, authority, root/slot, gate, evidence, dossier, predicate and context models without replacing them with later definitions.

| Required provenance source | Expected raw identity | Physical source check |
| --- | --- | --- |
| docs/plans/DETERMINISTIC_PLANNER_V0_1_E2_PC01_SOURCES.json | d821e2b08fa623c78d01014708b43fb9361f5921bca482f9893cb20d6d980121 | PASS |
| source.json | d8caaee52fc8a043db22eab3e405e66c7fa2873ea4f89773e20cc22bb9f05c25 | ABSENT |
| E2-CHECK.json | 537ed482e8aaa4dede6dfd3039c1eb2ce53f4cfd95660f8f8022b7970ec93fb6 | ABSENT |
| E2-COLLECT.json | 10c07a62e01c907b47d78fa9ddf2560f45b9862a9362eda04549e841edb6f617 | ABSENT |
| E2-DECIDE.json | 030cd5b248c3de5a89b512d8e044a1520462cc2fb558f2ff1711f8a84034401e | ABSENT |
| E2-FINISH.json | 81b1ce2c58cfaf0cc43aa6b43d838e59ce7bef3ad9ed26c9215a8b02786b85dd | ABSENT |
| E2-PREPARE.json | 0a1daaa24eea752c83ed20aad3f7756b72e2e6b76b7e0c4c2033e5f6a9bc0f99 | ABSENT |
| docs/plans/DETERMINISTIC_PLANNER_V0_1_E2_PC01_SOURCES.json | d821e2b08fa623c78d01014708b43fb9361f5921bca482f9893cb20d6d980121 | PASS |
| qualification://E2-P02-human-decision | cddac13f5e0b0f460e5d58a68d4ce753ce43cb5d17481be408d9b5f43d616574 | ABSENT |
| resolution.json | d31c57f258c8b82dafdaad33671d0851c4905d8a30c1846e50baa441b4ecbbef | ABSENT |
| qualification://E2-P02-human-decision | 6bebc233783b5faa0898ecccb20cf51ce529086c74ca672a113450f6e270a411 | ABSENT |

Each expected typed identity, section, scope, method and excerpt is preserved separately in JSON. Existing PC01_SOURCES bytes pass their raw pin. Missing files remain MISSING even when an excerpt happens to hash correctly: the excerpt does not define a reviewed immutable source-index entry or supported location. No files were manufactured from those excerpts.

Two authority provenance records name `qualification://E2-P02-human-decision` but pin different hashes (`6bebc233…` choice and `cddac13f…` grant). Their exact logical provenance is defined; their physical source/pin mapping is AMBIGUOUS. A single immutable raw file at one path cannot have both hashes. The native source codec expects canonical relative physical paths; selecting new paths or changing these records would change the exact checkpoint identity. No such change is authorized by a reproduction of the pinned checkpoint.

| Required bundle element | Classification | Missing authoritative input |
| --- | --- | --- |
| Complete canonical current Snapshot | AUTHORITATIVELY_DEFINED | None; exact file/hash available |
| Supported codec default fields | DERIVABLE | Only existing schema defaults; no new state inferred |
| Physical source bytes and complete ArtifactPin index | MISSING | Exact immutable files for declared missing paths and reviewed bindings |
| Same-URI authority source mapping | AMBIGUOUS | Supported immutable binding for distinct choice/grant raw hashes |
| Exact policy ArtifactPin and ordered policy bytes | MISSING | Path, profile, pointer, typed identity/namespace/hash and corresponding file |
| Event-backed initial state and ordered transition inputs | MISSING | Complete earlier source/policy envelope and legitimate prospective ancestry |
| Applicable prospective mainline genesis authority | MISSING | Existing G04 authority binds `c549…`, not mainline `8d77…` or earlier HUMAN_HANDOFF |

Source entity, source contract, gate, authority, Action model and root/slot model are explicitly inventoried from the original Snapshot, including provenance. No E06 root/slot models or T01-D source pins are inherited. [PC03's cold-restore contract](DETERMINISTIC_PLANNER_V0_1_E2_PC03_FIXTURES.json) explicitly requires initial/current snapshots, ordered ledger, source pins, policy pin and trusted bundle identity; descriptive names do not fill these missing fields.

## Reproduction start and stop

The nearest earlier qualified candidate is HUMAN_HANDOFF `9b3d8e6a074687a7aef9dca0279262cf2888492de73b7207768dc48bb0f5edfa`, immediately before RecordedDecision. It is not selected for execution: an authoritative event-backed start/source-policy envelope and applicable genesis authority are absent. Starting from the target Snapshot alone would neither reproduce the preceding transition nor establish ancestry. No P01/P02/P03 restart was attempted.

REPRODUCTION_TRACE = []  
TRANSITIONS_EXECUTED = 0  
MAINLINE_CHECKPOINT_STATE_ID = NOT_CREATED (expected state above)  
MAINLINE_CHECKPOINT_BUNDLE_ID = NOT_CREATED  
LEDGER_ID = NOT_CREATED  
LEDGER_ROOT = NOT_CREATED  
APPEND_HEAD = NOT_CREATED

HISTORICAL_ORIGINAL = NO  
QUALIFICATION_REPRODUCTION = YES (prospective purpose; **no reproduction artifact exists**)

If inputs become complete, the resulting artifact must be classified REPRODUCED_QUALIFICATION_CHECKPOINT and retain any applicable PRE_GENESIS_HISTORY = NOT_REPRESENTED boundary. This package does not claim that such a bundle historically existed. The conditional requested MAINLINE_CHECKPOINT_BUNDLE_1.json was deliberately not created.

## Equality and negative checks

SEMANTIC_EQUALITY = NOT_RUN_REPRODUCTION_STOPPED  
SOURCE_PIN_EQUALITY = UNQUALIFIED_MISSING_PHYSICAL_ENVELOPE  
POLICY_PIN_EQUALITY = UNQUALIFIED_EXACT_PIN_MISSING  
SCOPE_LINEAGE_EQUALITY = EXPECTATIONS_DEFINED; REPRODUCTION_NOT_RUN  
PROVENANCE_QUALIFICATION = INCOMPLETE  
EVENT_ANCESTRY = NOT_ESTABLISHED_FOR_PROSPECTIVE_MAINLINE  
COLD_RESTORE_EQUALITY = NOT_RUN  
REPLAY_EQUALITY = NOT_RUN  
FULL_CHECKPOINT_EQUALITY = UNQUALIFIED_CONTRACT_INCOMPLETE

G04_SUBSTITUTION = REJECTED. An independent native identity comparison confirms G04 source `c5494ac4…` differs from `8d77f7f…`; its rule_known=false differs from the required mainline rule_known=true. G04's qualified trust/ancestry is preserved. The earlier HUMAN_HANDOFF identity also differs from the exact expected checkpoint and cannot be substituted. These are read-only oracle checks, not bundle-admission negative tests. Wrong source/policy/scope/lineage/provenance/unrelated-ledger and differently pinned-state bundle tests are NOT_RUN because the required Step 4 stop occurs before a valid candidate exists; none is falsely reported PASS.

## Exit, readiness and preservation

Applicable existing functional lifecycle terms remain true in the unchanged E06 target: reentry completed, knowledge current, slot/root proofs admitted and satisfied, FINISH actionable and unexecuted. These later facts do not repair the original mainline checkpoint envelope. Original A07/A08 equality and the prior package's other unqualified P03 bundle terms remain unqualified.

P03_EXIT_PREDICATE = FALSE  
E2_P03_RESULT = PARTIAL  
E2_P04_READY = NO  
NEXT_PACKAGE = P03 mainline immutable source/policy and event-backed start contract closure

P04's explicit prerequisite in the canonical plan is P03 PASS; it is mechanically false. Neither P04 nor FINISH was executed.

RUNTIME_MODIFIED = NO  
E2_FINISH_ACTIONABLE = YES (existing E06 target; original checkpoint FINISH remains non-actionable)  
E2_FINISH_EXECUTED = NO  
TARGETED_TESTS = prior 12 PASS and 32 fresh readers retained; current read-only identity/control/non-substitution checks PASS  
BROAD_REGRESSION_STATUS = prior current-runtime failures and frozen-E1 duplicate-import collection blocker retained separately  
E1_ARTIFACTS_MODIFIED = 0  
PRODUCTION_EFFECT = NO  
git diff --check = PASS

No runtime repair was attempted: incomplete authoritative inputs prevent a complete-contract runtime counterexample. The [machine-readable result](DETERMINISTIC_PLANNER_V0_1_E2_P03_MAINLINE_CHECKPOINT_REPRODUCTION_1.json) records exact checkpoint fields, each provenance pin and physical check, missing/ambiguous envelope inputs, empty reproduction trace, equality limits, provenance intent, P03/P04 gates and runtime preservation hashes.
