# Deterministic Planner v0.1 — E2-P05 authoritative contract recovery and readiness

**RESULT = PARTIAL. CONTRACT_RECOVERY = PASS. P05_INITIAL_ORACLE = PASS. P05_EXECUTION_READY = NO.** The exact canonical P04 target is trusted, cold-restored and consistent with its presealed terminal oracle. Immediate execution of the complete P05 package still needs a current, independently bound E2-END A01–A13 input graph. No P05 or P06 case was executed, and no runtime, authority, definition or successful canonical state was changed.

The [machine-readable companion](DETERMINISTIC_PLANNER_V0_1_E2_P05_READINESS.json) records recovered ownership, input and capability classifications, authority limits, sealed negative expectations, persistence/replay plans, gates and preservation. [Source pins](qualification/E2_P05_READINESS_1/source-pins.json) distinguish raw file hashes from native state, content, event and authority identities.

The [canonical plan](DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_EXPERIMENT_1.md:73) makes P04 PASS the package prerequisite. Its linked JSON assigns **19 cases** to P05: E2-D01, E2-END, E2-REG and E2-N01–N16. The [acceptance matrix](DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_ACCEPTANCE_MATRIX_1.md:229) supplies their exact initial states, operations, expected states, invariants and persistence/determinism obligations. All 36 matrix case contracts were recovered and checked against the canonical JSON: [field correspondence and package allocation](qualification/E2_P05_READINESS_1/canonical-case-contracts.json). P06 owns only E2-REVIEW. The historical planning statuses are specifications, not current execution verdicts.

P05 evaluates the full experiment and produces qualification evidence ready for fresh review. It does not own another live Planner Action, a new canonical lifecycle event, a permission flag or a replacement terminal control state. Its isolated negative/invalidation probes, independent lifecycle reproduction, process/order determinism and current baseline tests are substantive qualification work. It therefore does not meet the exception for executing P05 as an already prepared read-only terminal-state evaluation in this recovery package.

| Exact P05 entry identity | Value |
|---|---|
| Authoritative bundle | `planner-bundle-v1:3e36b39884db3ea4ecaea0b2371d2af910c34b984fc69c5d3e2b42bc26ce13c2` |
| Current Snapshot | `planner-snapshot-v1:046fdc270a0060503729151368a68672f76af122830b86e65d372e6bc5d7dea4` |
| Native ledger anchor | `planner-event-v1:a0413d075c0ec54dfa6f2fe6a16a540a6cb185a104efe143e02cc0985fb44ee0` |
| Append head | `planner-event-v1:1797a108353285b2458cc84129338b783d889cf788fead9276cb7f850dbe132e` |
| Context | E2-QUALIFICATION-ONLY / E2-P03-PROSPECTIVE-QUALIFICATION-1 / E2-P03-PROSPECTIVE-GENERATION-1 |
| Supported policy | E1-SELECTION-1-P06, exact retained source/content pin |
| Native history | Twenty ordered events; exactly two authorized deferred INSTALLs inside P04, at sequences 16 and 18 |

The [initial oracle](qualification/E2_P05_READINESS_1/initial-oracle.json) was written before native inspection. Expected full semantics come from the existing F03 sealed target oracle; trusted identities also match the canonical P04 PASS record. A separate interpreter called native `codec.restore` on exactly [the required P04 target](DETERMINISTIC_PLANNER_V0_1_E2_P04_CANONICAL_TARGET_BUNDLE_1.json), then recomputed current state, typed-proof usability and C03. Native restoration checks canonical bytes, event/source files, supported policy and historical replay; expected-answer files remain comparison inputs. [All 37 term-by-term entry comparisons pass](qualification/E2_P05_READINESS_1/target-inspection.json).

The independent initial state requires received Evidence and receipt, accepted ValidationResult and support, both required reentry events, admitted actual REENTER/FINISH result witnesses and current knowledge, usable SLOT_PROOF/ROOT_PROOF, E2-SLOT **RESOLVED**, E2-ROOT **SATISFIED**, all six Actions completed and **TERMINAL_SUCCESS**. Actionable and selected inventories are empty. Final ResumeEligibility is false because the named Action has completed; eligibility at the earlier A11/A12 boundary is not persistent permission. Exact source/policy pins, context, parent/state continuity and full typed Computation match the existing seal.

The first inspection harness incorrectly required every retained installation record to remain applicable at the terminal state. Its sole failure is [retained unchanged](qualification/E2_P05_READINESS_1/target-inspection-first-inspection.json). The installed external-resolution route uses `installation.current -> gates.governed_external_unknown`; that predicate explicitly accepts evidence-acquisition stages and excludes **DEPENDENT_ACTION_REENTRY** ([native predicate](../../adapter/planner/gates.py:421), [currentness](../../adapter/planner/installation.py:317)). At this completed boundary the acquisition role is no longer applicable. Its canonical bytes, source pin, installation witness and `route_support_current` remain exact; all eight other required active installation records are current. The corrected inspection checks these separate obligations. It changes only the new inspection harness, preserving the first expected file, failed comparison, F03 seal, runtime and canonical P04 state.

P05 consumes P04's actual outputs and historical comparisons. It does not resubmit P04 commands merely to obtain them. [Ten pinned P04 input checkpoints](qualification/E2_P05_READINESS_1/P04-input-checkpoints.json), the actual Evidence/attestation/receipt, ValidationResult/support, reentry events, native result witnesses, root/slot proofs, independent root source, authorities and event ancestry are present. Prior A01–A08/A14–A16 evidence retains its own package scope. The matrix's explicit E2-END reproduction is a separate qualification obligation, not permission to overwrite or continue the already successful P04 ledger.

| P05-owned case group | Required operation and independent expected result |
|---|---|
| N01–N03 | No/malformed/foreign-lineage governed route fails at native admission or the specified PLAN_DEFECT boundary; no usable waiting/reentry shortcut |
| N04–N07 | Stale Evidence/authentication, substituted source/domain, wrong authority and invalid root/slot proof withdraw acceptance; no satisfaction from PASS alone |
| N08–N11 | Dangling prerequisite rejects before computation; stale knowledge is not rescued by producer history; wrong policy/tampered persistence rejects against independently retained trust |
| N12–N15 | Selection, declarations, premature receipt/reentry and incomplete named prerequisites never establish execution, knowledge, proof or C03 permission |
| N16 | Independently ready machine/human/factual frontier produces RUNNABLE/HUMAN_HANDOFF/MIXED_WAIT as specified; unknown remains unknown |
| D01 | Equal supported semantics preserve full Computation, selection and canonical identities across seeds, declared unordered/key permutations and fresh processes; causal history stays ordered |
| END | Independently authored canonical A01–A13 lifecycle across real writer termination/fresh reader, repeated under D01; every stage oracle passes; no E1 migration |
| REG | All affected current native/CLI/importer/constructor baseline requirements pass; all prior closed findings remain closed; no skips or historical-count substitution |

The [16 sealed negative oracles](qualification/E2_P05_READINESS_1/sealed-negative-oracles.json) preserve each matrix's full exact expected outcome, mutation domain and available seed input pins. They distinguish native rejection from a computed fail-closed state. They were sealed before any P05 execution and are not claimed negative PASS results. Most concrete isolated operands are derivable from actual P04 boundary bundles or the qualified P03 governed-unknown variant. N08's initial candidate and N12's selected-without-result candidate depend on the missing current initial-state binding. Future operand construction must retain these expectations and the successful target; it must not weaken authentication, change trust anchors, issue authority or repair runtime inside qualification.

The [input inventory](qualification/E2_P05_READINESS_1/input-inventory.json) finds the canonical sources, target, P04 boundary bundles, P03 unknown/invalidation fixtures, comparison dimensions, regression programs and review-subject template **PRESENT_CURRENT**. Case operands and process manifests are **DERIVABLE** where their pinned native starting inputs exist. The complete current E2-END graph and its initial/selected-unexecuted fixtures remain **MUST_MATERIALIZE**. Future P05 PASS logs are execution outputs, not circular preparation prerequisites.

The first dependency-ordered blocker is **E2-END_CURRENT_NATIVE_INPUT_GRAPH_NOT_BOUND**. The earlier PC01–PC04 interfaces describe E2-CANONICAL-BASELINE-1; the successful P04 input describes E2-P03-PROSPECTIVE-QUALIFICATION-1. The prospective bundle's initial Snapshot already marks COLLECT, CHECK and PREPARE completed. Its first nine events contain governed reevaluation/decision/configuration history, not those original Action executions. The earlier P02 report's initial `545ad191…` and post-decision `8d77f7f…` snapshots do not join this ledger. The [input-closure trace](qualification/E2_P05_READINESS_1/E2-END-input-closure-trace.json) records these exact discrepancies.

There is also a concrete oracle mismatch if old interfaces are used unchanged: PC03's generic POST_REENTRY scaffold expects RUNNABLE with resume true, whereas the F03/P04 sealed actual post-A12 frontier is PLAN_DEFECT pending its authorized deferred configuration, and completed REENTER supplies no persistent resume permission. This does not reopen P01/P02/P03/P04 PASS. [All fourteen earlier P01 qualification pins still match](qualification/E2_P05_READINESS_1/P01-preflight-pin-checks.json). Their historical preflight does not itself bind later prospective state, source, parent and oracle identities.

E2-END requires a complete independent canonical A01–A13 input graph under its own exact definitions, source/policy pins, synthetic decisions/grants, parent contracts and boundary oracles. It may be an independently prepared qualification reproduction; proving original P03 historical correspondence is not imposed as a new P05 prerequisite. Conversely, the P03 prospective amendment replaced the named A07/A08 fidelity comparison and did not waive E2-END's full lifecycle coverage. No unsupported stitching, retroactive history, manual completion or presumed extension of old authority is permitted. This recovery identifies input binding work; it establishes neither a new native capability defect nor a new human authority decision.

The [capability inventory](qualification/E2_P05_READINESS_1/capability-inventory.json) records already qualified canonical/O01/selection/codec, bounded result/dossier/decision, G01–G04 native start, cold restoration/source invalidation, E07 Evidence/receipt, V02 validation/support, R05 Proof/reentry/C03, I01–I05 installation and F03/E06 root/slot/reevaluation capabilities. Generic semantics may be reused; historical instances remain bound to their own identities and lineage. No additional native capability is established as required. No capability was implemented here.

The [authority inventory](qualification/E2_P05_READINESS_1/authority-inventory.json) separates qualification evaluation from bounded operating, semantic and INSTALL authority. P05 specifies no new canonical authority issuance, installation or P05-wide grant. Existing P04 witnesses retain their exact subjects, content, pre-state, parent, scope/lineage/generation and consumer bounds. Root/slot proof usability was verified on the trusted target. Completed Actions and historical grants do not authorize reexecution or unrelated configuration. A separately bound END reproduction must demonstrate applicable authority at its own required boundaries; this recovery does not broaden any grant or presume new authorization necessary before that input graph is defined. Source-shaped isolated negative construction is qualification input preparation, never an out-of-band mutation of the successful canonical state.

The [persistence plan](qualification/E2_P05_READINESS_1/persistence-plan.json) requires the native bundle/current/initial state, ordered event ledger, exact source index, supported policy, trusted expected bundle identity and independently reviewed contracts. Record writer/reader PIDs and exits, input allowlists, source/code/contract hashes, before/after identities and full semantic comparisons. Terminate the writer; use at least **three independent cold readers per checkpoint per seed 0, 1, 7 and 101**. Check END's stage boundaries/external wait, actual P04 history, governed-unknown and post-invalidation states, and isolated negative boundaries. A rejected candidate has rejection evidence and an unchanged accepted starting state, not a fabricated durable successor.

Reverse/rotate only native-declared unordered Action/source/goal/proof/authority collections and permute object keys. Preserve causal event chronology and ordered policy clauses; retain R05's declared unordered validation-input semantics and membership distinctions. Compare complete typed inventories, branches, witnesses, reasons, selection, authority/receipt/proof/resume, context, source/policy validity and snapshot/bundle/event identities. Cold readers receive only the persisted bundle, independent trusted identity, pinned sources/policy and reviewed contracts. Expected answers belong only to the comparison harness.

The [replay plan](qualification/E2_P05_READINESS_1/replay-plan.json) reconstructs accepted historical native events, not new authority, validation or epistemic decisions. Evidence ingress and receipt form one atomic boundary; an ingress-only prefix is private. Proof and C03/ResumeEligibility are recomputed over restored authoritative state, never stored as permission. Historical P04's two deferred INSTALLs remain history. No new INSTALL is required merely because P05 consumes them. Independent END reproduction requires its full bound source/parent graph rather than a splice of older P02 and prospective P04 states.

REG includes A–N, X01–X11, C01–C06/refined C06, external-unknown repair, C06A budget and current native/importer/CLI/constructor/selection/control/receipt/resume/persistence tests. The canonical planned command is `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s adapter/tests -p 'test_planner*.py'`, supplemented by affected registered E2/constructor paths. [Static AST inventory](qualification/E2_P05_READINESS_1/static-test-inventory.json) finds 18 modules and 246 declared test methods; this is not a collected or passed test count. No unittest discovery, regression, permutation, invalidation or negative suite ran here. Known broad/legacy failures remain historical records to classify separately during the current REG execution; they neither count as current PASS nor receive a waiver. Read-only importer regression is explicitly part of REG, while `import_e1` remains excluded from canonical END.

P05's target is complete pinned qualification evidence and a ready independent-review subject, with the successful P04 terminal bundle unchanged. [Every exit term is separately enumerated](qualification/E2_P05_READINESS_1/readiness-gates.json): prerequisite P04 PASS; complete positive-case coverage at governing scope; all 19 assigned cases PASS; END; D01; current REG; all 16 negatives; persistence/replay; preservation with no deferred-scope violation; complete final review subject. FINISH completion alone cannot establish P05 PASS.

P06 is mechanically ready only when **P05 PASS and complete pinned END/D01/REG/full-matrix evidence and the fresh independent review subject are ready**. P06 then owns the new adversarial review, with any finding returning to bounded correction and affected requalification. It is not ready or executed here. Legacy N-REAL and original P03 correspondence remain independent release/assurance limits; this recovery does not add them as new P05/P06 prerequisites or infer aggregate Planner qualification.

`E2_P05_READY = YES` preserves the earlier P04 report's explicitly stated **package-prerequisite** meaning: P04 PASS. The stricter gate requested here is `P05_EXECUTION_READY = NO` until the current END input graph, dependent initial negative inputs and concrete D01/process bindings are sealed. The next package is **E2-P05 CURRENT END / MATRIX INPUT-BINDING CLOSURE**, followed by a separate qualification execution package. This recovery neither runs that closure nor selects an authority/scope option.

Preservation is checked against the before-work hashes of every preexisting file: 14,747 total, including 10,677 frozen-E1 files and all 28 runtime files. The [final preservation record](qualification/E2_P05_READINESS_1/preservation.json) records the completed audit. Only the two requested report files and new readiness evidence under `qualification/E2_P05_READINESS_1/` are authored. P04 stays PASS; P05/P06 stay unexecuted; P03 historical correspondence stays UNPROVEN; N_REAL_SATISFIED stays NO. No authority, definition or canonical lifecycle state is created. `git diff --check = PASS`.

```text
WORK_PACKAGE = E2-P05-READINESS
RESULT = PARTIAL
CONTRACT_RECOVERY = PASS

P05_PURPOSE = Integrated qualification, baseline regressions and determinism
P05_INITIAL_ORACLE = PASS (37 READ_ONLY CHECKS)

P04_OUTPUTS_CONSUMED = [trusted terminal target, actual lifecycle/results/proofs, pins/authorities/ancestry, sealed boundary evidence]
P05_OWNED_TRANSITIONS = [full-matrix evidence evaluation, isolated N01-N16, D01, END reproduction, REG, review-subject preparation]
P05_REQUIRED_INPUTS = input-inventory.json
P05_REQUIRED_AUTHORITIES = authority-inventory.json
P05_REQUIRED_CAPABILITIES = capability-inventory.json
P05_CONFIGURATION_REQUIREMENTS = NONE_TO_SUCCESSFUL_CANONICAL_TARGET; NO_NEW_DEFINITION_ESTABLISHED

P05_NEGATIVE_ORACLES = SEALED (16 CASE CONTRACTS; NOT_EXECUTED)
P05_PERSISTENCE_PLAN = CONTRACT_COMPLETE; CURRENT_END_CHECKPOINT_BINDING_REQUIRED
P05_REPLAY_PLAN = CONTRACT_COMPLETE; CURRENT_END_SOURCE_PARENT_BINDING_REQUIRED

P05_TARGET = Complete pinned qualification evidence and independent-review subject; P04 terminal state unchanged
P05_EXIT_PREDICATE = ALL_19_ASSIGNED_CASES_PASS AND FULL_MATRIX_COVERAGE AND END AND D01 AND REG AND NEGATIVES AND PERSISTENCE_REPLAY AND PRESERVATION AND REVIEW_READY
P06_READINESS_PREDICATE = P05_PASS AND COMPLETE_PINNED_END_D01_REG_FULL_MATRIX_EVIDENCE AND INDEPENDENT_REVIEW_SUBJECT_READY
E2_P06_READY = NO

P05_EXECUTION_READY = NO
E2_P05_READY = YES (P04_PASS PACKAGE_PREREQUISITE_ONLY)
FIRST_PREPARATION_BLOCKER = E2-END_CURRENT_NATIVE_INPUT_GRAPH_NOT_BOUND
NEXT_PACKAGE = E2-P05 CURRENT END / MATRIX INPUT-BINDING CLOSURE

P05_EXECUTED = NO
P06_EXECUTED = NO
E2_P04_RESULT = PASS
P03_HISTORICAL_CORRESPONDENCE = UNPROVEN
N_REAL_SATISFIED = NO

RUNTIME_MODIFIED = NO
NEW_AUTHORITY_ISSUED = NO
NEW_DEFINITIONS_INSTALLED = 0
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
GIT_DIFF_CHECK = PASS
```
