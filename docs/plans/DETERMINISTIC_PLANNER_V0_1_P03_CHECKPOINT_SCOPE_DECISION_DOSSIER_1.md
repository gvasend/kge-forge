# P03 checkpoint qualification scope decision dossier 1

DECISION_SUBJECT = P03 irreproducible historical checkpoint qualification  
P03_CHECKPOINT_SCOPE_DECISION_READY = YES  
SELECTED_OPTION = NONE  
QUALIFICATION_SCOPE_CHANGED = NO

This dossier prepares a qualification-authority choice. It makes no choice, changes no acceptance clause, and declares no P03 PASS. The exact original checkpoint `8d77f7f…` has no matching full source/policy-pinned native bundle. The [reproduction record](DETERMINISTIC_PLANNER_V0_1_E2_P03_MAINLINE_CHECKPOINT_REPRODUCTION_1.md) stopped because historical policy bindings, physical source closure and an applicable event-backed start are absent. Runtime defects established by this blocker: NONE.

## Original assurance purpose

The [canonical plan](DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_EXPERIMENT_1.md) lines 32–34, 57–61 and P03 package allocation, together with [matrix A07/A08/A14/A15/A16](DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_ACCEPTANCE_MATRIX_1.md), require:

- Source identities, bytes/currentness and dependent contracts preserved, preventing another source from silently taking their place.
- Exact supported selection policy identity/rules preserved, preventing policy changes from masquerading as state restoration.
- Complete native operational state persisted, including definitions/statuses, knowledge, roots/slots, authority, evidence, external route and source validity.
- A terminated writer and genuinely independent fresh reader; hidden process memory and cached control labels cannot stand in for computation.
- Canonical native snapshot/bundle identities and ordered parent-bound event ancestry preserved, with honest history boundaries.
- Authority, provenance, scope/lineage and generation preserved without new permission, accepted evidence or result being invented.
- Replay, independent recomputation, determinism and post-reload invalidation demonstrated; source loss withdraws support without deleting obligations.

Exact raw source/policy bytes matter; raw JSON formatting of an envelope is not an independently imposed byte-equality predicate. Original checkpoint correspondence is an additional assurance: these properties were established for the named historical mainline state and its own sources/policy/event history, rather than only for a newly authored fixture.

## Evidence available and its limits

| Evidence | Independently demonstrated assurance | Limit |
| --- | --- | --- |
| G04 | Qualified genesis/state/ledger/root/head/authority/context binding, cold persistence, deterministic lineage start with NOT_REPRESENTED prior history | Different `c549…` source checkpoint; no full source/policy index; cannot replace original `8d77…` |
| T01-D | Qualified live source admission/receipt, exact native Evidence and parent-event ancestry, trusted post-receipt bundle and cold persistence | Later receipt checkpoint. Event-only replay from G04 lacks complete authentication/transaction inputs |
| E03/E04 | Received/validated/proved/reentry distinctions, native lifecycle validation and source-bearing snapshots | Snapshot evidence is not complete integrated original source/policy/event history |
| E05 | Actual E2-REENTER completion/result and current accepted E2-K-REENTER | Does not reconstruct original bundle envelope |
| E06 | Typed slot/root proof admission, independent satisfaction, persistence/replay/invalidation, bounded nonterminal Action reevaluation, FINISH readiness | Proof-event replay has a declared E06 boundary; full original checkpoint correspondence remains unqualified |
| 32 fresh readers | Available Snapshot/GenesisBoundBundle identities, complete Computation, serialized provenance/context; repeated original snapshot reloads across seeds | Comparison baseline was an existing file; no recovered historical writer/full source-policy envelope |
| 12 targeted tests | Generic positive/fail-closed proof/reevaluation capabilities and package regression correspondence | Bounded tests; neither complete broad suite nor exact historical mainline bundle equality |
| Mainline/unknown snapshots and invalidation controls | Known-rule mainline wait, independent governed-unknown wait; bounded grant withdrawal and acquisition invalidation exposing PLAN_DEFECT | Full A14/A15/A16 bundle reload/all-disjoint-source coverage is not upgraded by this dossier |

These retain their qualified scope. None is a contractual substitute for the missing exact checkpoint. Detailed IDs, reader comparisons and limits remain in the [checkpoint qualification record](DETERMINISTIC_PLANNER_V0_1_E2_P03_CHECKPOINT_BUNDLE_QUALIFICATION_1.md) and [E06](DETERMINISTIC_PLANNER_V0_1_EVIDENCE_E06_ROOT_SLOT_REEVALUATION_RESULT.md).

## Assurance unavailable from current historical inputs

The actual original policy pin/file and physical source-index bindings cannot be independently established by selecting them now. The choice/grant provenance URI names two distinct raw hashes without a supported immutable physical mapping. The original event-backed start, actual event chronology, trusted bundle identity, writer process baseline/termination and full source-aware cold/replay comparison cannot be recovered from snapshot-only trace or report metadata. A new experiment cannot prove that the original bundle existed or that those original-process checks happened.

“Irrecoverable” here means unavailable under supplied inputs, not permanently impossible if genuine historical artifacts emerge. A plausible replacement policy, freshly generated source files, G04 state or similar control label is insufficient.

## Three decision options

| Option | Qualification semantics | Work and assurance consequence | P03 / P04 | Planner v0.1 / N-REAL |
| --- | --- | --- | --- | --- |
| RETAIN_ORIGINAL_P03_CHECKPOINT_REQUIREMENT | Keep the exact original requirement and gate | Recover authentic original source/policy/index/start/ledger/bundle and genuine writer/cold evidence; complete full equality plus other required controls. No substitute accepted. All original assurance stays required. | P03 PARTIAL; P04 NO until original predicate PASS | No automatic requalification; existing aggregate gates remain. N-REAL unchanged |
| AUTHORIZE_PROSPECTIVE_P03_CHECKPOINT_QUALIFICATION | Explicitly amend A07/A08 acceptance to a named new prospective fidelity test; original historical comparison becomes SUPERSEDED_UNPROVED, never PASS | Run the sealed contract below, including residual A14/A15/A16 controls. Preserve portable source/policy/state/ancestry/cold-replay/invalidation assurance at the same semantic boundary. Lose exact original historical correspondence and historical writer/prefix execution assurance. | P03 stays PARTIAL until new suite and every retained term PASS. Only issued amended gate may map PASS_UNDER_REVISED_P03_SCOPE to P04 readiness | Qualification label must state amended scope/exclusions; regressions/review/aggregate gates still apply. N-REAL unchanged |
| DEFER_P03_HISTORICAL_CHECKPOINT_REQUIREMENT | Explicitly accept a narrower reproducible evidence scope, carrying OPEN_UNQUALIFIED historical debt | Accept already demonstrated functional/artifact evidence at its true scope. Historical integrated source/policy/writer/cold assurance remains absent, with no new test equivalent asserted. Retained reproducible controls still must pass. | Original P03 remains PARTIAL. Separate scoped acceptance can be ACCEPTED_WITH_HISTORICAL_CHECKPOINT_DEBT. P04 only through explicit revised gate AND retained-term acceptance | Current full release predicate still requires no deferred-scope violation. C alone cannot release it; narrower release needs separate explicit authority. N-REAL unchanged |

No option is recommended or selected. Authorization alone yields no new test PASS.

## Option A: exact unblocking information

Recover the actual typed policy ArtifactPin (path/profile/pointer/kind/namespace/hash), supported version, ordered rule binding and immutable policy bytes; every historical provenance source's exact raw bytes and complete source index; reviewed choice/grant URI-to-physical bindings; exact initial event state and legitimate original ledger/bundle/parent identities; original expected bundle identity and independent pre-persistence inventory/process/allowlist/hash evidence. Recovered artifacts must match original Snapshot `8d77f7f…` and known-rule EXTERNAL_WAIT boundary exactly. Restore/replay and remaining A14/A15/A16 controls must pass without repinning, provenance mutation or invented history. Newly recovered information that permits prospective reproduction is still distinct from evidence of actual historical execution.

## Option B: complete prospective test contract

Contract ID: **P03-PROSPECTIVE-CHECKPOINT-QUALIFICATION-1**. This is a NEW_PROSPECTIVE_QUALIFICATION_CHECKPOINT, not reconstruction of historical `8d77…`. Evaluation scope stays E2-QUALIFICATION-ONLY; new lineage is E2-P03-PROSPECTIVE-QUALIFICATION-1, generation E2-P03-PROSPECTIVE-GENERATION-1, tick 0 and validity bound 100. No production effect or FINISH/P04 execution is authorized.

**Start and history.** Author a new native initial HUMAN_HANDOFF-equivalent fixture from the pinned canonical six-Action earlier handoff semantic template. Adopt prefix completion/knowledge/dossier as explicit author-declared qualification initial premises. They are not executions in the new event ledger and do not prove historical execution. Construct a fresh native PersistenceBundle with initial=current=start and events=(), validating every current premise and actual source pin. PRE_GENESIS_HISTORY = NOT_REPRESENTED is a provenance statement; no G04 GENESIS or prior event is invented. The existing codec accepts the coverage tag PARTIAL_HISTORICAL_REPLAY with supported policy version E1-SELECTION-1-P06; this tag does not make the fixture historical. Planner context uses the new prospective lineage. If any current native contract cannot represent this honest start/transaction, stop with a bounded counterexample; this dossier does not authorize a runtime patch.

**Source files.** Under `docs/plans/qualification/P03_PROSPECTIVE_CHECKPOINT_1/`, author canonical UTF-8 JSON for action definitions, accepted prefix knowledge, dossier/proof inputs, decision options/issuer, separate choice evidence and grant source, external gate/requirements, resolution contract, root/slot model, qualification-scope authority, fixture initial state, fixture contract and independent expected-state oracle. Keep the six ActionIds, operations/prerequisites/output/dossier/decision semantics. Replace logical URI provenance with unique actual physical relative sources; set all prospective context fields consistently; compute every affected native identity through existing identity functions. Empty/unresolved pre-proof root/slot semantics remain explicit. These are newly adopted prospective definitions, never edits of historical artifacts.

Every Action/knowledge/proof/contract/authority provenance must cite actual file, exact typed raw identity, section, method and prospective scope/context. Choice and grant use distinct immutable files. Materialize and freeze all input bytes, derive all ArtifactPins and prospective start identity before any execution. Store path/profile/pointer/identity kind/namespace/hash for every pin. Hash source/code/contracts/oracles and record a complete input allowlist in a sealed immutable run manifest. Derived hashes are mechanical consequences of specified bytes, not unspecified semantic decisions. A missing mapping or required template field stops preflight. No event/source may be added after execution without a separately sealed variant/run.

**Policy.** Explicitly adopt the existing supported selector policy for this NEW test: read-only `docs/experiments/E1/E1_GRAPH_RESOLUTION_SELECTION_POLICY_1.md`, CONTENT_IDENTITY/raw-file-sha256 `475bef0b28d7b484ba2641c654b37e9ce3d6f6ae1b0e13dfdcadaa3f79a2a3b5`, raw profile and empty pointer, version E1-SELECTION-1-P06. This prospective candidate comes from native selector.POLICY_PIN/SUPPORTED_POLICIES; it is not evidence that the original historical bundle carried that pin. Verify actual file bytes and native validate_policy before execution; pin rule version, class/effect order/map and ordered RULES. Stop on mismatch, never repin. Frozen E1 is read only.

**Execution and persistence.** A fresh writer loads only sealed files/runtime/contracts, validates the independently expected initial handoff, and performs the newly authorized bounded ALLOW_QUALIFICATION_MAPPING capture through the ordinary authenticated RecordedDecision transaction/application path, retaining exact subject/dossier/options/choice/grant bindings. Append the actual event through existing native bundle APIs. The scope decision approves only this synthetic fixture choice; it does not bypass ordinary runtime authority checks.

Stop at post-decision known-rule EXTERNAL_WAIT before EvidenceSourceAdmission/RECEIVED: actionable/human-ready sets empty, receipt/admissions/accepted observation/positive external proof absent, resume false, REENTER and FINISH non-actionable. Compare independently pinned expected full state through the harness. Only after all source/policy/state/authority/context oracle checks PASS, save_bundle, record its actual native bundle_id and start/current Snapshot IDs, retain trusted expected identity independently, record writer PID/exit and terminate.

A separate fresh reader restores with only that bundle, trusted identity, sealed sources/policy/contracts, then native replay/recompute. Compare full definitions/statuses/readiness, knowledge/producers/outcomes, roots/slots, authority/dossiers/predicates/consumption, evidence/route/source validity, branch/witness/reason/selection/control/resume, provenance/context and ordered ledger/identities. Use native PersistenceBundle.events and parent_event/parent_snapshot/after_snapshot identities; do not invent a G04-style standalone ledger-ID/root field absent from this model. Expected answers remain harness-only.

**Independent repetition.** Fresh writer directories and processes repeat equal prospective semantic inputs. Require canonical native identities and full Computation equality; three independent cold readers per seed 0/1/7/101. Reverse/rotate unordered collections and object keys; preserve event chronology and policy order. Alternate alpha-renamed compatible fixtures remain semantic-generalization controls with appropriately different identities, not hash-equal to the named run.

**Residual controls.** Independently seal an A14 variant before running it: unknown rule, admitted exact resolution route, EXTERNAL_WAIT/unknown proof/resume false, full persist/terminate/restore equality. Never patch mainline rule_known or use the variant as its substitute. Separately sealed A15 support fixtures adopt current synthetic knowledge/proof/authority premises and apply native SourceInvalidation for each disjoint required source, retain obligations, withdraw support, persist/restore the after-state. A16 invalidates the restored unknown acquisition source, requires PLAN_DEFECT and persists/restores it. No FINISH or P04 execution is used to construct those premises.

**Negatives.** Seal one-dimension mutations before their runs: later/earlier/G04 checkpoint, wrong source/path/hash/domain, wrong policy/version/rules, wrong scope/lineage/generation, absent provenance, unrelated event parent/head, semantically similar differently pinned state, retained-trusted-identity bundle/source-index/current tamper, malformed/stale/missing route, or invalidated support still usable. Preserve expected identity; record native rejection separately from semantic oracle failure. An unsupported native negative path is a counterexample requiring a separate correction, not a fabricated PASS.

**Acceptance mapping.** All prospective preflights, checkpoint oracle/equality domains, independent reproductions, residual A14/A15/A16 controls and negatives must PASS, as must every retained applicable P03 term. Then an independently reviewed issued mapping may record PASS_UNDER_REVISED_P03_SCOPE and unlock the amended P04 prerequisite. Original historical comparison stays SUPERSEDED_UNPROVED. All functional evidence retains its own provenance/boundary. The replacement preserves portable fidelity at the external wait boundary; it does not preserve original bytes/ledger/writer correspondence or demonstrate executed original prefix.

The machine companion fixes file roles, transformations, pin schema, all execution steps, oracle inventory and acceptance domains. Prospective bytes/hashes are deliberately not claimed to exist now: they must be created and sealed before execution under the selected authorization. That is execution preparation, not a further qualification-scope choice.

## Option C: deferred-debt contract

Debt ID: **P03-HISTORICAL-CHECKPOINT-DEBT-1**, status OPEN_UNQUALIFIED, exact original Snapshot `8d77f7f…`, clauses canonical plan 57–59 and matrix A07/A08 original full historical checkpoint correspondence. Record all unavailable original policy/source/index/start/ledger/writer comparisons and the original authoritative hashes. Owner is the qualification-scope authority, with future closure package owner assigned in the issued decision. Carry the debt in every downstream P03/P04/qualification/release record; review at each next v0.1 qualification/release review and whenever genuine artifacts emerge. No expiry, inferred closure or automatic PASS.

The remaining evidence **may be accepted for a narrowed current v0.1 evidence scope**: functional receipt→validation→proof→reentry→result→typed slot/root→FINISH readiness and available artifact reload/replay capabilities. It cannot support a full original mainline source/policy restoration claim. Original P03 remains PARTIAL. Only a separate scoped acceptance verdict, ACCEPTED_WITH_HISTORICAL_CHECKPOINT_DEBT, can express this bounded acceptance after every retained reproducible term passes.

C does not waive residual A14 full bundle preservation, A15 all-disjoint-source invalidation/reload, A16 full bundle reload or missing source-backed transaction replay by silently calling them “historical debt.” They require explicit allocation and actual evidence. The prior record identifies their limits. P04 is NO until an issued C decision explicitly replaces its P03 gate AND all narrowed acceptance terms PASS; native Action readiness prerequisites remain unchanged. Neither deferral nor the functional target alone opens P04.

Debt closes by evidence only when genuine original input/bundle/process records satisfy the original comparison. If later inputs permit exact reproduction, preserve reproduced-versus-historical provenance and separately dispose of any historical-process assurance it cannot establish. A future authenticated scope decision may retire/supersede debt by disposition, which is never evidence PASS. A new prospective run alone is complementary and requires Option B's separate acceptance amendment to replace the governing historical clause.

The current aggregate release predicate includes deferred_scope_violations == 0. C alone does not amend that release predicate; full Planner v0.1 requalification remains gated. Any narrower release with this debt requires a separate explicit release-scope decision and a label stating exclusions. N-REAL remains independent and unchanged.

## Required authority and decision admission

Required authority is the authenticated owner of canonical E2 qualification/release scope, or an Architect with **explicitly delegated qualification-scope authority**. Repository precedent does not establish that every Architect/Action permission can change acceptance. Ordinary DECIDE/USE, ATTEST, GENESIS or bounded fixture authority is insufficient. This dossier introduces no runtime AuthorityClass.

The [N-REAL reconciliation](DETERMINISTIC_PLANNER_V0_1_N_REAL_RECONCILIATION_1.md) provides the procedural precedent: complementary canonical evidence does not imply literal satisfaction/full equivalence; a qualification/release-scope choice must be explicit. Its earlier execution-state descriptions are historical and are not adopted as current E2 facts. No option here resolves N-REAL or frozen-E1 compatibility assurance.

The issued decision must bind this dossier's exact SHA-256 and authoritative input hashes; authenticated issuer/role/delegation; exactly one option token; the exact original clauses; immutable prospective/debt contract version where applicable; revised or unchanged P03 acceptance predicate; named P03 verdict and exact P04 prerequisite mapping; qualification/release/N-REAL limits; and issuance/provenance/version/supersession identity. Review/authenticate this record before any scope change. Selecting A records unchanged gates; selecting B adopts the prospective contract/mapping; selecting C adopts debt/exclusions/scoped gate with all retained obligations. None grants production or native execution authority beyond its explicit synthetic scope.

## Decision readiness and preservation

All three alternatives, required evidence/work, assurance limits, prospective test, debt closure, authority and downstream consequences are defined. P03_CHECKPOINT_SCOPE_DECISION_READY = YES is decision readiness, not input-seal readiness, execution approval or qualification PASS.

```text
DECISION_SUBJECT = P03 irreproducible historical checkpoint qualification
OPTIONS = [
  RETAIN_ORIGINAL_P03_CHECKPOINT_REQUIREMENT,
  AUTHORIZE_PROSPECTIVE_P03_CHECKPOINT_QUALIFICATION,
  DEFER_P03_HISTORICAL_CHECKPOINT_REQUIREMENT
]
P03_CHECKPOINT_SCOPE_DECISION_READY = YES
SELECTED_OPTION = NONE
QUALIFICATION_SCOPE_CHANGED = NO
E2_P03_RESULT = PARTIAL
E2_P04_READY = NO
RUNTIME_MODIFIED = NO
E2_FINISH_EXECUTED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
git diff --check = PASS
```

[Machine-readable dossier](DETERMINISTIC_PLANNER_V0_1_P03_CHECKPOINT_SCOPE_DECISION_DOSSIER_1.json) records all options, assurance mappings, prospective/debt contracts, unchanged gates and immutable input/runtime hashes. Only these two dossier files are authored by this package; no test, fixture, runtime transition, authority issuance, P04 or FINISH execution occurs.
