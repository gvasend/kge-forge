# E2-P05 A05 RecordedDecision event-ancestry recovery 1

**RESULT = BLOCKED.** The required original A05 occurrence ancestry is irrecoverable from the retained artifacts searched. A complete, already-qualified native `RecordedDecision` event does exist in the prospective P03 checkpoint and the canonical P04 descendant. It binds a different record, dossier and qualification lineage; the current P05 scope does not authorize substituting it for A05. **P05 remains 11/13, with A05 first missing.** No A05 capture, application, execution, replay, event append or authority issuance occurred.

## Canonical A05 and T03 relationship

The earliest [canonical plan](DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_EXPERIMENT_1.md:20) declares `E2-DECIDE` as a synthetic, NON_EFFECTING `ARCHITECT_CONTRACT_DECISION`. [A05](DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_ACCEPTANCE_MATRIX_1.md:61), owned by P02, requires a ready human decision with predefined qualification-only choices and an independently pinned record. Its operation is **`apply_recorded_decision` through `append_event`**, using the exact permitted record. The target is recorded decision history and independently evaluated bounded authority, with no automatic root/slot satisfaction. Canonical before/after identities and an event trace are mandatory.

Native preconditions are the admitted current dossier/checklist, independently ready/actionable E2-DECIDE, exact accepted choice knowledge, authenticated record, applicable DECIDE predicate, exact command pre-Snapshot, option and scope. The positive P02 choice is `ALLOW_QUALIFICATION_MAPPING`; `DECLINE` produces no grant and is a separate control. Inputs and full native Action definition are in [the definition/model inventory](qualification/E2_P05_A05_DECISION_ANCESTRY_RECOVERY_1/A05-definition-and-model.json).

T03 is a **capability precedent, not the A05 occurrence itself**. Its qualified [materializer](../../adapter/planner/human_decision.py:148) invokes the exact native [apply_recorded_decision](../../adapter/planner/core.py:489) path used by A05. The subsequent immutable [ALLOW Retry 1](DETERMINISTIC_PLANNER_V0_1_E2_HUMAN_DECISION_ALLOW_RETRY_1_RESULT.md) reports the actual selected choice and retained state. T03's reported persistence and test cover a native **Snapshot round trip**; `DecisionMaterialization.event` is a `RecordedDecision` command, not an enclosing ledger `ExecutionEvent`. No serialized original enclosing event was found.

## Native representation and retained decision

`RecordedDecision` has exactly five fields: `decision: ActionId`, `choice`, `record: EntityId`, `authority: PredicateId`, and `expected_snapshot`. It has no separate result identity. Issuer, trust root, dossier, scope, lineage and provenance are bound through the exact native choice entity, authority predicate, accepted knowledge, dossier and referenced Snapshots. The old report's “recorded_decision_identity” is an **EntityId**, not a `planner-event-v1` identity.

| Retained term | Exact identity/value |
|---|---|
| Subject / choice | E2-DECIDE / ALLOW_QUALIFICATION_MAPPING |
| Issuer | qualification-authority:ed59567bbe5e7c719975a4e64db157696bf349d42cb0e73695115a50606c330a |
| Protocol trust root | raw-file-sha256:d7478df57c6c7619eff262daa6e258103cd31e226db6e523e5d2de6a5a603da0 |
| Dossier | planner-dossier-sha256:6a507317bc9cc323fbaa626e97b5954cf3ad934b0bd92d9dc96bd4f63e07bddb |
| Choice content | raw-file-sha256:6bebc233783b5faa0898ecccb20cf51ce529086c74ca672a113450f6e270a411 |
| Record EntityId | E2-CHOICE-RECORD:6bebc233783b5faa0898ecccb20cf51ce529086c74ca672a113450f6e270a411 |
| Native DECIDE predicate | E2-CHOICE-AUTHORITY:6bebc233783b5faa0898ecccb20cf51ce529086c74ca672a113450f6e270a411 |
| Bounded USE grant | e2-grant:cddac13f5e0b0f460e5d58a68d4ce753ce43cb5d17481be408d9b5f43d616574 |
| Handoff Snapshot | planner-snapshot-v1:9b3d8e6a074687a7aef9dca0279262cf2888492de73b7207768dc48bb0f5edfa |
| Post-materialization Snapshot | planner-snapshot-v1:8d77f7f1997ca884e07490c4c93f5fbe3a31b09278fd57c6c6ea1f9fa26b3aaf |
| Context | E2-QUALIFICATION-ONLY / E2-CANONICAL-BASELINE-1 / E2-GENERATION-1 |

The [native inspection](qualification/E2_P05_A05_DECISION_ANCESTRY_RECOVERY_1/native-state-and-ledger-inspection.json) verified both archived Snapshot identities and native model admission, exact choice content/dossier/provenance, accepted choice knowledge and bounded USE grant's choice/dossier/content linkage. This proves retained state and its source bindings. It does not establish event occurrence/ancestry.

Human choice evidence, recorded decision state, bounded grant and occurrence event remain distinct. `apply_recorded_decision` imports an already authenticated record and changes native decision history/status; it explicitly never issues authority. T03's ALLOW wrapper adds the grant after that application. Thus the wrapper's reported handoff pre-state and final grant-containing post-Snapshot cannot simply be asserted as the missing event's native `expected_snapshot` and `after_snapshot`.

## Required ancestry and assurance

The [adopted P05 input oracle](qualification/E2_P05_END_INPUT_BINDING_1/input-oracle.json) currently requires the **exact original native lifecycle event witness**, supported by authoritative source pins and ordinary event ancestry; it forbids a Snapshot/KnowledgeId/result label or unapproved qualification-instance substitution. A03/A04 replacement authorizations apply only to their own slots. No A05 replacement authority is selected.

| Mandatory assurance | Native witness | Original recovery |
|---|---|---|
| Occurrence and payload | ExecutionEvent containing exact RecordedDecision | Missing |
| Record/choice/authentication | Native record, accepted choice knowledge, dossier, issuer/trust and provenance | Retained in state; event link missing |
| Parent and pre-state | Exact parent_event and parent_snapshot; command expected_snapshot equality | Missing |
| Post-state/effects | Event after_snapshot and exact decision/grant relationships | Snapshot retained; enclosing event reference missing |
| Ledger and position | Exact bundle `/bundle/events`, sequence/index and predecessor/successor | Missing for original |
| Scope/currentness/provenance | Referenced native context and pinned records at occurrence | State retained; original event binding missing |
| Ordering | Governed prepare → decision → external-wait path | Not recoverable by report chronology |

An ordinary PersistenceBundle exposes an ordered event tuple, **no separate LedgerId**. Its content identity plus exact `/bundle/events` enrollment supplies membership; the first and last identities supply root/head. Choice-evidence sequence 1 is not a native event ledger position. Native event identity binds sequence, parent Snapshot, parent event, complete typed result and after Snapshot, with optional resume binding. No missing identity is computed from inferred values.

[END](DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_ACCEPTANCE_MATRIX_1.md:467) needs an actual stage transition on a coherent lifecycle, beyond “the decision exists.” [N12](DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_ACCEPTANCE_MATRIX_1.md:383) prevents selection/history from masquerading as result/completion. [N13](DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_ACCEPTANCE_MATRIX_1.md:397) prevents prospective definitions/output declarations from masquerading as an actual result. The required composite native witness supplies those distinctions; a post-state alone does not. [Term-by-term requirements](qualification/E2_P05_A05_DECISION_ANCESTRY_RECOVERY_1/ancestry-contract-and-assurance.json) preserve the existing assurance. This recovery does not claim newly executed N12/N13 suites or close their A05 ancestry mapping.

## Search results and candidate classifications

The search examined **4,169 structured artifacts**, all with recorded hashes and no JSON parse failures; **388 matching text/code/log artifacts**, including 324 decoded JSON fragments; embedded native JSON strings; all retained native event/result/record/grant representations; and event-bearing bundles/HEADs/genesis ledgers. Frozen E1 was excluded as a witness source and preserved. Search terms included E2-DECIDE, record/choice/grant/dossier identities, original pre/post states, typed results, event/parent/head/payload/command fields. The [manifest](qualification/E2_P05_A05_DECISION_ANCESTRY_RECOVERY_1/file-search-manifest.json), [event inventory](qualification/E2_P05_A05_DECISION_ANCESTRY_RECOVERY_1/event-search.json), [bundle inventory](qualification/E2_P05_A05_DECISION_ANCESTRY_RECOVERY_1/persistence-search.json), [record inventory](qualification/E2_P05_A05_DECISION_ANCESTRY_RECOVERY_1/native-record-search.json) and [text audit](qualification/E2_P05_A05_DECISION_ANCESTRY_RECOVERY_1/text-audit.json) retain exact paths/pointers/encodings.

- 113 distinct native event identities overall; **one** distinct RecordedDecision event for E2-DECIDE, repeated in **273 retained representations**. Copies do not establish additional occurrences.
- 590 PersistenceBundle representations, 173 HEAD records and 4 genesis-ledger representations inspected. No original choice-record command/event or original-state neighbor event was found.
- Seventeen pure bundle comparison decodes encounter two descriptive operand schemas and fifteen obsolete ValidationSupportOutcome representations. Every underlying JSON/event record was still structurally searched; none contains the matching A05 event. These are retained format limitations, not new runtime failures or skipped ancestry candidates.

| Candidate | Classification | Result |
|---|---|---|
| Original post-decision Snapshot/choice/USE grant | NATIVE_RECORDED_DECISION_WITHOUT_EVENT / CHOICE_EVIDENCE_ONLY / native grant state | Exact native state/content retained; no parent or event enrollment |
| T03 report/test, ALLOW Retry trace, P02 Retry 4 chain | REPORT_METADATA / DERIVED | Semantic PASS retained; no native event payload, parent or ledger position |
| P03 prospective RecordedDecision | QUALIFIED_NATIVE_EVENT | Complete ancestry exists, different record/context and current acceptance scope |
| Same event in canonical P04 target | CANONICAL_NATIVE_EVENT carrying qualified prefix | Same identity and exact enrollment; not original P02/A05 occurrence |
| G04 genesis and descendants | SNAPSHOT_ONLY for old decision; other native genesis events | No pre-genesis A05 occurrence established |
| A04 prospective bundle | OTHER: actual CHECK/COLLECT/PREPARE native history | DECISION_READY, no RecordedDecision; no A05 continuation performed |

Every candidate family and exact native pointer is in [the candidate/losslessness record](qualification/E2_P05_A05_DECISION_ANCESTRY_RECOVERY_1/candidate-and-losslessness-analysis.json).

## Complete alternate native event

| Term | Verified retained native value |
|---|---|
| Event | planner-event-v1:9f00d563a015969d02179c7a991d2efec97b763448fbc27c34e7bd634d36a728 |
| Exact result | RecordedDecision(E2-DECIDE, ALLOW_QUALIFICATION_MAPPING, E2-PROSPECTIVE-CHOICE, E2-PROSPECTIVE-CHOICE-AUTHORITY, exact pre-Snapshot) |
| Parent / ledger root | planner-event-v1:a0413d075c0ec54dfa6f2fe6a16a540a6cb185a104efe143e02cc0985fb44ee0 |
| Pre-Snapshot | planner-snapshot-v1:c48cc70219d9d7df5aa8dd93221cf678eeb32b4696a2a5a8f6d6ff5052c7dfc8 |
| Post-Snapshot | planner-snapshot-v1:576fe3a99286bcbceee1587dedf7db8e3073517e251d6a064821f286b77b5324 |
| Enrollment | Sequence 2, zero-based index 1 |
| P03 checkpoint bundle | planner-bundle-v1:d1944fe18626778bebfc6c7693c7bdb5303e079668683e5fb99676ecbe46b859 |
| Canonical descendant bundle | planner-bundle-v1:3e36b39884db3ea4ecaea0b2371d2af910c34b984fc69c5d3e2b42bc26ce13c2 |
| Context | E2-QUALIFICATION-ONLY / E2-P03-PROSPECTIVE-QUALIFICATION-1 / E2-P03-PROSPECTIVE-GENERATION-1 |
| Choice content | raw-file-sha256:daba5011fd851f567737e8ede4d6e73479af694c68a546004bed94b1d86b3cdf |
| P03 dossier | planner-dossier-sha256:53da6ec10eec4bb05ba229e25be4869315fe5ab1074f4048a28d9b9c95fcd5a1 |

Exact pointers are `/bundle/events/1` in both bundles. The preceding event is ordinary ActionReevaluation sequence 1; the P04 successor is installation event sequence 3, `planner-event-v1:a19b52ab601c6d3c7668b78c6e20cc87e54cfc317595e4da641fcbb7d107fb1e`. Pure comparison verifies event hashes, parent/pre-state continuity, ledger position, post/head relationships and physical source/policy pins. No native decision replay was run.

The P03 choice has its own physical source and pinned scope authorization; its existing native DECIDE and USE entities bind that dossier/context. **The candidate USE grant is already present before the event**. Direct before/after inspection shows knowledge/entities/predicates/actions/root/slot definitions unchanged; native decision history/status changes are retained. It proves decision admission and authority relationships, not a new grant-issuance event.

The [existing P03 authority](qualification/P03_PROSPECTIVE_CHECKPOINT_1/sources/qualification-scope-authority.json) authorizes its prospective checkpoint and bounded synthetic ALLOW capture. Its scope amendment supplies A07/A08 and the actual P04 starting prefix. It does not authorize replacing A05's END input, relabeling this event as the old choice, or waiving full original-prefix ancestry. [Scope applicability](qualification/E2_P05_A05_DECISION_ANCESTRY_RECOVERY_1/scope-applicability.json) preserves P03 PASS and its prior decision unchanged. The genuine alternate is recorded, not silently bound.

## Losslessness and binding frontier

**LOSSLESS_RECOVERY = NO. PRIMARY_CLASSIFICATION = IRRECOVERABLE_HISTORICAL_WITNESS**, specifically the original A05 witness required by current P05 scope. The alternate native event's own ancestry is directly retained and verified; this conclusion does not deny its existence. Missing original payload/pre-state/parent/enrollment cannot be recovered from Snapshot contents or chronological report labels. No direct event, native identity body, HEAD command or old-lineage ledger supplies those fields. This does not assert that A05 never ran or that a particular archive was truncated/deleted.

The current graph is rechecked and retained unchanged. **E2_A05_RECORDED_DECISION_EVENT_ANCESTRY = FAIL; END/N12/N13 mapping for this original-ancestry requirement remains unclosed.** No substitute binding is created. A03/A04 remain separately authorized replacements, with both original historical claims UNPROVEN. [Frontier evidence](qualification/E2_P05_A05_DECISION_ANCESTRY_RECOVERY_1/P05-binding-frontier.json) keeps **11/13** and first missing **E2-A05.recorded_decision_event_ancestry**. If a later legitimate A05 mapping closes, A06.request_wait_event_trace is next; it was not recovered or resolved here. The wider original-prefix/END linkage also remains separately unresolved.

## Unselected scope options and human-choice reuse

[The bounded decision dossier](qualification/E2_P05_A05_DECISION_ANCESTRY_RECOVERY_1/scope-decision-dossier.json) seals source hashes, original identities, the exact alternate event/source/parent/ledger/context, retained A04 frontier and assurance/exclusion terms. Subject: `qualification-scope-subject-v1:a210e434c3424bb8919fea0ca1156785f2c42625a38cd4a887b753ca97f913a2`. This is a qualification dossier identity, not an issued native grant. **No option is selected.**

| Option | Exact bounded consequence |
|---|---|
| RETAIN_P05_A05_NATIVE_ANCESTRY_REQUIREMENT | Keep the original requirement and 11/13 until legitimate original native ancestry is supplied |
| AUTHORIZE_PROSPECTIVE_P05_A05_DECISION_ANCESTRY_QUALIFICATION | Permit a separately contracted new A05 ancestry experiment with a new authenticated choice, distinct occurrence identities and explicit A05-only END replacement mapping; no historical rewrite or P05 execution |
| AUTHORIZE_P05_A05_ALTERNATE_NATIVE_EVIDENCE | Permit a separately sealed A05-only acceptance mapping for the **exact already-retained P03 event** above. Preserve its P03 choice identity/context, original A05 UNPROVEN, its pre-existing-grant limitation and unresolved original-prefix/A06/END gaps. No new A05 reproduction is required merely to recover that event |

Both replacement options are bounded **scope decisions**, not automatic binding PASS or authority to execute. Later END/N12/N13 mapping must explicitly retain native occurrence assurance and all historical labels. The alternate option is now supportable because a complete native candidate is retained; it does not permit reports/Snapshots to stand in for ancestry.

For a **new prospective A05** using the retained A04 frontier, the semantic subject and exact option vocabulary may be reused, but **fresh authenticated synthetic choice evidence is required**. A04's dossier `planner-dossier-sha256:d0bbd6202b0a36b2524be8c85062c4e5015a0a30c55db90b4623b8769ce56f8b`, state `planner-snapshot-v1:38682b3fd1d13af1d056613048d85af131be2a31c0c918cc49e15c7cf6a808a4` and prospective lineage/generation differ from the old T03 choice. The native capture checks exact subject/dossier/Snapshot, and the current T03 materializer is baseline-lineage bounded. Reusing or retagging the old ALLOW evidence would not meet those bindings. A later contract must resolve issuer/trust/DECIDE/USE applicability and obtain a new choice bound to its sealed context; this recovery chooses no option and issues no authority.

For **acceptance of the existing alternate event**, a fresh choice is unnecessary to recover evidence already authorized/captured in P03. A new **A05 acceptance-scope decision** is still required. That distinction never represents the P03 synthetic choice as the original historical human selection.

## Preservation and report

Pure native inspection barred capture/materialization, result application, event append/commit, save/restore and replay entry points; zero barred calls occurred. Only new recovery reports/evidence were written. All pre-existing inventoried files are compared against the before-work hash baseline, including 29 native planner files, 177 adapter files and 10,677 frozen-E1 files. [Verification](qualification/E2_P05_A05_DECISION_ANCESTRY_RECOVERY_1/verification.json) records zero changed/missing baseline files and `git diff --check = PASS`.

```text
WORK_PACKAGE = E2-P05-A05-DECISION-ANCESTRY-RECOVERY
RESULT = BLOCKED
A05_PURPOSE = SYNTHETIC_BOUNDED_DECISION_GRANT
A05_NATIVE_OPERATION = APPLY_RECORDED_DECISION_THROUGH_APPEND_EVENT
RECORDED_DECISION_MODEL = FIVE_TYPED_FIELDS; NO_STANDALONE_RESULT_ID
ANCESTRY_CONTRACT = EXACT_ORIGINAL_NATIVE_EVENT_PARENT_STATE_LEDGER_AND_CHOICE_BINDINGS
T03_MAPPING = NATIVE_SEMANTIC_CAPABILITY_PROVEN; ORIGINAL_OCCURRENCE_NOT_RECOVERED
CANONICAL_EVENT_SEARCH = COMPLETE; QUALIFIED_ALTERNATE_RETAINED
PERSISTENCE_SEARCH = COMPLETE; ORIGINAL_ANCESTRY_ABSENT
ALTERNATE_NATIVE_SEARCH = COMPLETE; ONE_DISTINCT_EVENT_VERIFIED
LOSSLESS_RECOVERY = NO
PRIMARY_CLASSIFICATION = IRRECOVERABLE_HISTORICAL_WITNESS
E2_A05_RECORDED_DECISION_EVENT_ANCESTRY = FAIL
END_MAPPING = BLOCKED_NO_APPLICABLE_A05_REPLACEMENT_SCOPE
N12_MAPPING = NOT_CLOSED_FOR_ORIGINAL_A05_ANCESTRY
N13_MAPPING = NOT_CLOSED_FOR_ORIGINAL_A05_ANCESTRY
P05_BOUND_STAGE_INPUTS = 11 / 13
P05_NEXT_MISSING_INPUT = E2-A05.recorded_decision_event_ancestry
SCOPE_DECISION_REQUIRED = YES
SCOPE_OPTIONS = [RETAIN_P05_A05_NATIVE_ANCESTRY_REQUIREMENT, AUTHORIZE_PROSPECTIVE_P05_A05_DECISION_ANCESTRY_QUALIFICATION, AUTHORIZE_P05_A05_ALTERNATE_NATIVE_EVIDENCE]
SELECTED_SCOPE_OPTION = NONE
P05_EXECUTION_READY = NO
P05_EXECUTED = NO
P06_EXECUTED = NO
A05_REEXECUTED = NO
ORIGINAL_A03_HISTORICAL_OCCURRENCE = UNPROVEN
ORIGINAL_A04_HISTORICAL_ANCESTRY = UNPROVEN
ORIGINAL_A05_HISTORICAL_ANCESTRY = UNPROVEN
P03_HISTORICAL_CORRESPONDENCE = UNPROVEN
N_REAL_SATISFIED = NO
RUNTIME_MODIFIED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
git diff --check = PASS
```
