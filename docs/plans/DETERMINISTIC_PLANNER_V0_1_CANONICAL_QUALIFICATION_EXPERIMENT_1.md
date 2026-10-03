# Canonical Planner qualification experiment 1 — E2

**Planning only. E2 is not executed and Planner v0.1 is not requalified.** E2 will exercise the canonical Planner lifecycle without translating E1 legacy artifacts. No existing E2 experiment directory was found in the inspected repository; reserve identifier **E2** for this plan. Do not create execution evidence until its contract/fixture preflight passes.

The [acceptance matrix](DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_ACCEPTANCE_MATRIX_1.md) defines 36 planned cases with initial state, operation, expected state, invariants, persistence and determinism requirements. The [JSON companion](DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_EXPERIMENT_1.json) contains the six packages, all cases and explicit coverage of all 30 requested semantics.

## Scope and canonical boundary

SOURCE_FORMAT = PLANNER_SNAPSHOT_V0_1 is the logical format; use existing `PLANNER-SNAPSHOT-1`, native Snapshot/PersistenceBundle types and codec. It is not a new parallel snapshot implementation. Use `validate_model`, independently pinned O01 expectations, `core.recompute`, selector, typed events, `append_event`/`record_result`, `save_bundle`, `restore`, and C03 `resume_eligibility`. Relevant event routes include `SuppliedResult`, `RecordedDecision`, `ExternalEvent` and `SourceInvalidation`.

No `import_e1` or historical source projection is part of E2. Independent canonical definitions and qualification-only source/authority/proof fixtures are authored for this experiment. The existing supported selection-policy contract may be reused with its exact admitted identity/version; an E2 label cannot substitute a new policy hash under an old version.

Use six Actions, namespaced to E2:

| Action | Operation and prospective purpose | Prerequisites/consumer |
|---|---|---|
| E2-COLLECT | SOURCE_ACQUISITION; deterministic bounded synthetic inventory | Initially eligible; supplies declared accepted knowledge |
| E2-CHECK | DETERMINISTIC_VALIDATION; independent bounded check | Initially eligible; gives genuine selection competition |
| E2-PREPARE | DECISION_INPUT_ACQUISITION; bounded dossier | Accepted current acquisition/check prerequisites |
| E2-DECIDE | ARCHITECT_CONTRACT_DECISION; simulated qualification-only recorded choice | Independently complete dossier/checklist; never automatically executed by selector |
| E2-REENTER | DETERMINISTIC_MAPPING; bounded external-evidence consumer | Recorded decision/appropriate authority, current knowledge, exact receipt/reentry and proof gates |
| E2-FINISH | DETERMINISTIC_VALIDATION; final consumer/proof check | Accepted reentry output and independent root/slot proof obligations |

P01 must define all 13 O01 fields and native reference/output contracts for each Action before state construction. These prospective purposes are not complete fixtures or assertions of execution. All operations are synthetic and NON_EFFECTING; the human choice is a predeclared test input, not real Architect authority. A synthetic grant's exact type, scope, issuer trust and independent applicability predicate are pinned before execution. Authority-object presence alone does not satisfy the consuming action.

Use a bounded root and slot with separate typed proof predicates, declared provenance and independent source dependencies. Native accepted knowledge/proof contracts determine their transitions; neither a supplied PASS nor the final Action name establishes satisfaction. Freeze complete goal coverage and status inventory so removing blocked work cannot fabricate success. No production or real-world action is permitted.

## Lifecycle and checkpoint

The mainline is canonical construction → native validation → deterministic selection among initial actions → bounded supplied results/knowledge → preparation → simulated recorded decision → external request/wait → canonical persistence → writer termination → cold restore → synthetic evidence ingestion/receipt → validation → accepted reentry → deterministic selection/result continuation → independent proof/control recomputation.

Choose **EXTERNAL_WAIT**, not MIXED_WAIT, for the main checkpoint. By then no internal Action or human decision is ready; the relevant consumer is held on one valid external-evidence boundary. Evidence is absent, the receipt and reentry routes are exact, and no positive obligation proof or resume permission exists. The validation rule is known on this mainline, but its required evidence/proposition is not established. Values are computed from canonical inputs, not loaded as trusted expected labels.

Also require **E2-A14**, an isolated canonical checkpoint variant with `rule_known=false` and an exact admitted `ExternalResolutionContract`. It must persist/restore as EXTERNAL_WAIT with unknown proof and resume false. Missing/malformed/wrong-lineage/stale route variants must remain PLAN_DEFECT under the repaired contract. This variant exercises governed unknown semantics without assuming receipt magically defines a missing rule.

The current native receipt path does not set `rule_known=true`. Therefore positive receipt continuation is performed on the known-rule/missing-evidence mainline. If a future requirement demands unknown-rule acquisition followed by positive continuation, it needs a separately established native rule-admission contract; direct flag mutation is prohibited. Independent branch variants cover RUNNABLE, HUMAN_HANDOFF and MIXED_WAIT precedence; baseline regressions retain all seven global controls.

## Evidence admission is a mandatory preflight interface

`core.apply_receipt` requires an already admitted concrete produced entity when receiving evidence, and validation consumes independently admitted ReceiptAdmission/authentication claims. ExternalEvent does not itself ingest arbitrary bytes or create producer competence.

E2-P01 must identify the exact supported canonical source/evidence admission transaction and its immutable bundle/source-index/ledger representation. It must accept new synthetic bytes only after verifying source identity, target domain, expected producer, scope, lineage, currentness, provenance, payload/claim schema and receipt binding. Then explicit native lifecycle events perform RECEIVED → VALIDATED → REENTRY.

If the existing APIs cannot represent this transaction while preserving cold replay, **stop P01 with E2_CONTRACT_INCOMPLETE or a separately reproduced implementation gap**. Do not invent an event, replace the restored Snapshot with a fixture containing accepted evidence, reset the ledger, repin an unrelated current state, or treat test-helper dataclass replacement as qualification. Any required bounded runtime repair is separately scoped; this planning task modifies no implementation.

Expected separation:

- RECEIVED records the pending admitted artifact; no accepted observation or resume is implied.
- VALIDATED independently proves the exact claims and records an accepted observation; resume remains false before accepted reentry lineage and named eligibility.
- REENTRY must satisfy current evidence, correct lineage, verified source/policy pins and every other named-action prerequisite.
- After eligibility, recompute/select E2-REENTER and apply its independently permitted supplied result. Require a new event/state identity and evaluated downstream E2-FINISH state. A Boolean flip is insufficient.

All synthetic receipt bytes, trust premises and simulated decisions are marked QUALIFICATION_ONLY and isolated under future E2 fixtures/results or temporary directories. Nothing is written to E1 and no external request is sent.

## Cold restoration and independent oracles

Persist the canonical bundle and trusted expected bundle identity at the external checkpoint. Terminate the writer process. A separate fresh interpreter loads only the persisted bundle, pinned source files, policy and reviewed contracts. Expected-answer files are available to the comparison harness only, not Planner input.

Compare complete semantic inventories: definitions/statuses, knowledge, roots/slots, authority entities/predicates, evidence requirements/admissions/observations, external route, source validity, policy, ledger, branch witnesses, global control and resume proof. Compare canonical snapshot and bundle identities as well. Record process IDs, exit status, input allowlists and source/code/contract hashes. A same-process encode/decode check is additional evidence, not a substitute.

Repeat accepted-source invalidation after cold restore through native SourceInvalidation events. Stale proof, authority, knowledge and ordering dependencies must withdraw current support without deleting obligations. Invalidate the acquisition-contract source separately in the governed-unknown variant: it must cease supporting waiting and expose PLAN_DEFECT when no valid alternative route exists.

Independent fixtures specify expected contracts/results before implementation output. Alpha-renamed compatible inputs and changed supported payload values prevent dependence on E2 names or fixed expected fixture output. No source hash by itself proves authority or applicability.

## Packages and qualification

| Package | Prerequisites | Work / acceptance | Unlocks |
|---|---|---|---|
| E2-P01 | This plan and existing native contracts | Complete six definitions, source/claim/proof/grant/receipt interfaces, independent oracles and negative fixtures; resolve admission transaction; all 30 coverage obligations assigned | P02 only after clean preflight |
| E2-P02 | P01 PASS | Canonical construction, initial selection/results, dossier/decision and external wait; derive empty actionable/human-ready and false resume | P03 |
| E2-P03 | P02 PASS | Persist/terminate/cold restore; full equality; governed-unknown variant and post-reload invalidation | P04 |
| E2-P04 | P03 PASS | Synthetic source admission, receipt validation, exact reentry, actual post-reentry selection/result and proof recomputation | P05 |
| E2-P05 | P04 PASS | Full E2 acceptance matrix, baseline regressions, adversarial negatives, ordering/hash/process determinism and preservation | Fresh review ready; not QUALIFIED |
| E2-P06 | P05 PASS | New independent adversarial review of final implementation/contracts/evidence | Accepted review evidence or bounded correction loop |

FIRST_PACKAGE = E2-P01. No package executes in this task. Contracts/supporting fixtures and tests may be authored in those future packages; an unexpected native defect must return to an explicitly bounded correction package, not be hidden inside qualification.

Required negative controls are in the matrix: no-route unknown, malformed/wrong-lineage route, stale evidence, substitution, wrong authority, invalid proof, dangling prerequisite, stale knowledge, policy mismatch, tampered persistence, selection/history-as-execution, prospective-output-as-result, lifecycle bypass and blocked named-action reentry.

Determinism uses seeds 0,1,7,101, reversed/rotated unordered Action/source/goal/proof/authority collections, object-key permutations, fresh processes and at least three cold restores per checkpoint/seed. Compare full typed outputs, branches/witnesses/reasons and canonical identities. Causal event histories and ordered policy clauses are not freely permuted as though sets. Repeat importer/CLI/canonical constructor paths where applicable without introducing legacy migration.

## Qualification and release gates

BASELINE_REGRESSION remains A–N + X01–X11 + C01–C06/refined C06 + external-unknown repair + C06A budget + current importer/CLI/constructor/selection/controls/receipt/resume/persistence tests. Historical passes remain evidence, not current PASS claims. A planned command is `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s adapter/tests -p 'test_planner*.py'`, supplemented by affected constructor and E2 suites as they are registered. No test runs here.

E2 adds lifecycle evidence; it neither erases past findings nor proves frozen E1 migration. The [legacy disposition](DETERMINISTIC_PLANNER_V0_1_E1_LEGACY_BRANCH_DISPOSITION_1.md) records the explicit N-REAL release obligation that still exists.

```text
PLANNER_V0_1_REQUALIFICATION_READY =
  prior_closed_findings_remain_closed
  AND baseline_regressions_pass
  AND canonical_E2_pass
  AND cold_restore_pass
  AND synthetic_receipt_reentry_pass
  AND post_reentry_continuation_pass
  AND determinism_pass
  AND deferred_scope_violations == 0
  AND fresh_independent_review_ready
  AND legacy_release_obligation_resolved

legacy_release_obligation_resolved =
  N_REAL_PASS
  OR separately_approved_explicit_release_scope_reconciliation
```

Neither legacy alternative is satisfied by writing this plan. Fresh review readiness differs from review acceptance: final qualification additionally requires an accepted fresh independent adversarial verdict with no open correctness/determinism/persistence/authority/resume finding and all governing release obligations met. The reviewer must probe hidden state/nondeterminism, fail-open admission, substitution, stale support, authority leakage, receipt/reentry bypass, canonical identity weakness, composition and selection/definition versus execution conflation. No review is conducted here.

```text
CANONICAL_EXPERIMENT_ID = E2
CANONICAL_SOURCE_FORMAT = PLANNER_SNAPSHOT_V0_1
CANONICAL_WORK_PACKAGES = [E2-P01,E2-P02,E2-P03,E2-P04,E2-P05,E2-P06]
FIRST_PACKAGE = E2-P01
BASELINE_REGRESSION_REQUIRED = YES
COLD_RESTORE_REQUIRED = YES
SYNTHETIC_REENTRY_REQUIRED = YES
POST_REENTRY_CONTINUATION_REQUIRED = YES
FRESH_ADVERSARIAL_REVIEW_REQUIRED = YES
PLANNER_V0_1_REQUALIFICATION_READY = NO
V0_1_CURRENT_STATUS = CORRECTION_REQUIRED
IMPLEMENTATION_MODIFIED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
```
