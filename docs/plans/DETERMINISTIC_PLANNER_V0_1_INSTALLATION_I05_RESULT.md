# INSTALLATION-I05 — Action-definition replacement and A12 readiness

WORK_PACKAGE = INSTALLATION-I05  
RESULT = PASS  
SELECTED_OPTION = AUTHORIZE_P04_A12_REENTER_RESULT_INSTALLATION

The generic Action-definition replacement adapter is qualified, and the exact R06 replacement is installed. A09, A10, A11 and A12 readiness are YES. Canonical A09–A12 remain unexecuted. P04 execution readiness remains NO because A13 preparation is incomplete.

## Authorization and canonical replacement

The explicit human selection is captured through authenticated session transport, with the R06 contract identity, old/new native Action content hashes, exact prefix, context, consumer and exclusions. No cryptographic signature or new operating permission is claimed. Both R06 body hashes and its authoritative declaration source hash were checked before application. R06 and all earlier qualification reports remain unchanged.

The bounded INSTALL authority permits only REPLACE of the existing E2-REENTER definition. The exact changes are:

- accepted_inventory: exactly PASS plus E2-K-REENTER, statement “Bounded reentry mapping produced”, producer E2-REENTER;
- pass_model_complete: TRUE.

Every other native Action field is preserved. Other Action definitions, statuses, actual knowledge, source/policy configuration and lifecycle state are unchanged. Installing the prospective KnowledgeRecord-shaped output contract does not admit actual knowledge or create an ActionResult.

The adapter is generic: it contains no E2/P04 identifiers. It validates a closed canonical native body, complete required Action fields under the codec's default-field rules, logical role, exact old definition and authorized change frame. Native type/model admission governs references. Relationships outside the Action are preserved; the adapter cannot silently alter route/Decision registries. This capability supports governed replacement of an existing unexecuted Action. Adding a new Action/status role is not enabled.

The existing trusted INSTALL transaction supplies ordinary-parent compare-and-swap, authority applicability, command identity, atomic publication and historical replay. Action currentness requires the active definition, context and valid installation authority/support. Invalidation withdraws the Action's qualification and readiness without deleting history. Definition comparisons use canonical native bytes, respecting codec-declared unordered fields.

## Identities and handoff

| Domain | Identity |
|---|---|
| INSTALL authority | `73da39fd1c0569ad8f1c7007809ecc826ff9ed567cc128bcadadf3da8c053cb7` |
| Install event / append head | `45cec78291bd025c2ad9b8d2853ee8a9cedd2f63b956321899bed6b7b3ab4da5` |
| Installable definition | `4c7f4632ad618c92c7d77faed32f9f5478594b2e104e240d1d1ab444e6a61acb` |
| Installed-definition instance | `b9a1752c54aaaa35133335de1aca2d032bcdd8175bb4c59db58ea7e0b9bbe4cc` |
| Post-install snapshot | `023be7ec986722356f3871e7831e2cf2dd1ab1e8c45fb1f46103619557253513` |
| Post-install bundle | `359ab5424030c4482292bb546e83acd36dd140a8f618766a9a35ce61282f4445` |

These are distinct native identity domains; logical ActionId remains E2-REENTER. The new canonical configuration artifact is [the post-definition-install bundle](DETERMINISTIC_PLANNER_V0_1_E2_P04_POST_REENTER_DEFINITION_INSTALL_BUNDLE_1.json). It contains seven events and no A09 receipt or A10 validation instance. Prefix six equals the prior canonical bundle exactly; the old Action remains visible before event seven.

Identical installation retry is a semantic no-op. An independent installation store produces the same bundle bytes/identity. Prior A09 candidates are stale under the new prefix. A fresh candidate and transient E02 operand bind the new state/head; no old candidate is edited.

## Qualification

The final generic suite has seven tests covering replacement/frame/history, independent inventory and completeness changes, both changes together, a two-output unordered inventory permutation, bounded substitutions, closed-body rejection, injected failure before publication and invalidation. Security controls reject unauthorized identities/bytes/inventory/completeness/prerequisites/context, wrong authority/parent/operation and embedded result/completion state. An ActionResult cannot substitute for a definition. Exact grants bind all content, preventing broader alternatives.

The current regression run passes 57 tests for installation, authentication, validation/support, input sets and atomic Evidence transactions. The final seven-test adapter suite includes the additional unordered-inventory regression. The pinned O01 checker admits six of six current-context projected Action definitions; source/native binding and whole-model admission are verified separately. O01 does not issue execution authority.

Four fresh generic readers and four P04 configuration readers pass cold restore/replay across seeds 0, 1, 7 and 101. Four independent complete A09–A12 qualification executions produce identical native post-A12 bundle/state/head; fresh readers verify their actual event ancestry and prior C03/Proof/selection boundary. Replay reproduces historical results rather than issuing authority, making a new validation decision or persisting eligibility permission.

## Isolated A09–A12 path

Fresh A09 execution preflight and received-only postcondition PASS. V02 A10 accepted validation/support preflight PASS, with proof/reentry/completion separation preserved. A11 checks the computed typed obligation Proof, admits both required external and decision reentry events, reopens the named Action, and computes current C03 ResumeEligibility. REENTER is selected but unexecuted at the A12 boundary; FINISH is non-actionable.

The canonical acceptance matrix defines A12's execution protocol as `recompute → deterministic select → supplied permitted result → append_event`. The qualification driver supplies the exact authored bounded fixture only after native selection. Unchanged native result admission validates it and derives completion/current knowledge. This is a synthetic qualification execution of that native protocol, not an independently obtained production result or a fabricated external-domain outcome.

The isolated actual result is PASS with exactly E2-K-REENTER. Native admission marks REENTER completed and admits the current output. The isolated post-A12 bundle is `afba02b422c0a8df7e5941e180e8d430630f26acadf90fa3ee8c9150a8ebe4d7`. Twelve primary and two supplemental negatives reject missing/stale eligibility, wrong/missing/extra result inventory, wrong Action/context provenance, prospective definition-as-result, inconsistent manual completion, invalid definition and old pre-install Action substitution. Persistence/replay preserve the actual result and completion exactly once.

Canonical completion and knowledge remain absent. The actual result/completion claims above apply only to isolated qualification artifacts.

## A13 frontier and limits

A12's owned predicates pass: new event/state, accepted declared knowledge, completion and downstream finishing computation. In the current partial configuration, that computation returns:

- E2-ROOT = UNRESOLVED; no E2-SLOT or typed root/slot proof contracts;
- FINISH = BLOCKED and unexecuted;
- CONTROL = PLAN_DEFECT, reason UNRESOLVED_GOAL_WITHOUT_CONTROL_PATH.

This is recorded, not forced to RUNNABLE. A13 owns independent root/slot proof recomputation and selected finishing result. Its first blocker is P04-bound root/slot definition and independent root-source preparation, installation/currentness and the corresponding control path. No unrelated definitions or authority were installed here. The A13 initial oracle must retain actual current REENTER output/completion and native ancestry, then qualify its independent domain proofs and control before FINISH selection.

A12_NATIVE_PATH_QUALIFIED = PASS  
A12_READY = YES  
P04_EXECUTION_READY = NO  
NEXT_PACKAGE = P04 A13 prospective definition/currentness/readiness closure

## Audit and preservation

Two qualification-report checks were corrected without changing lifecycle semantics. The first report writer supplied tuple-valued Proof reasons to canonical JSON; the native checkpoints had already succeeded, and four independently emitted artifacts were subsequently verified in fresh readers. Those process errors remain in the audit. A post-A12 reader initially demanded acquisition-route applicability remain true after receipt; it now checks exact history/pins and current Action definition. Acquisition applicability is lifecycle-dependent. Native provenance or authentication rules were not weakened.

Three legacy Evidence-admission failures reproduce the names and reasons in the prior A09 control reconciliation: `test_validation_and_reentry_separate`, `test_conflicting_claims_are_not_overwritten`, and `test_pinned_source_shaped_fixture`. They remain separate from current-path qualification. An initial test command used a nonexistent module name; the successful regression command uses `test_planner_validation_input_sets`. No broad-suite PASS is claimed; the prior frozen-E1 duplicate-import collection blocker remains separate.

CANONICAL_A09_A12_EXECUTED = NO  
CANONICAL_ACTION_RESULT_CREATED = NO  
E2_FINISH_EXECUTED = NO  
P03_RESULT = PASS  
P03_HISTORICAL_CORRESPONDENCE = UNPROVEN  
N_REAL_SATISFIED = NO  
E1_ARTIFACTS_MODIFIED = 0  
PRODUCTION_EFFECT = NO  
git diff --check = PASS

Runtime changes are confined to the new Action adapter and its INSTALL dispatch, currentness/selection and invalidation integration. All existing documentation, prior bundles and R06 artifacts pass preservation hashes.

The [machine-readable result](DETERMINISTIC_PLANNER_V0_1_INSTALLATION_I05_RESULT.json) contains identities and qualification detail. [Native transition trace](qualification/INSTALLATION_I05_1/native-transition-trace.json), [authority capture](qualification/INSTALLATION_I05_1/authenticated-selection.json), [fresh A09 candidate](qualification/INSTALLATION_I05_1/fresh-a09-candidate.json), and [A12 evidence](qualification/INSTALLATION_I05_1/a09-a12-qualification.json) are retained. The reproducible driver is `adapter/tests/qualify_planner_i05.py`.
