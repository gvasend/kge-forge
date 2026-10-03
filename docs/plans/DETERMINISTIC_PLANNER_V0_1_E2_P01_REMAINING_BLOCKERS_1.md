# E2-P01 remaining preflight blockers — post E2-T01

**Classification complete; P01 retry remains disallowed.** E2-G01 is closed by the qualified native transaction. All other E2-specific input and oracle gaps remain. No closure package, P01 retry, experiment Action or Planner regression was executed in this task. Existing qualification evidence is reused only after matching its pinned code and contracts.

## Evidence and recomputation

The six original P01 companions were inspected in full. All six O01 profiles and native candidates are still null; 60 of 78 planned O01 cells are unbound. All ten source-role inventory rows lack concrete source identities. Five proof/authority entries remain fixture-incomplete. All 36 original fixture-path slots are null; REG instead names existing native suites and assertions. T01 supplies a separate complete synthetic transaction fixture and 20 new tests, not the E2 six-Action universe. Its 185-test qualification and implementation/contract pins match current files. These observations—not the old status flags—determine the updated classification.

Primary classifications partition the cases: **1 EXECUTABLE, 32 FIXTURE_INCOMPLETE, 3 DEPENDENCY_INCOMPLETE**. No primary CONTRACT_INCOMPLETE, ORACLE_INCOMPLETE, IMPLEMENTATION_CAPABILITY_MISSING or CONTRACT_CONFLICT case is established. Oracle incompleteness overlaps 34 cases (all except REG and REVIEW). REVIEW has a defined review procedure, but its concrete subject/evidence interface remains dependency-incomplete. EXECUTABLE REG means available suites, not a new E2-REG PASS.

Native governing semantics are contract-complete for the operations in the plan. This is not a claim that E2 is completely specified: exact experiment parameters, phase witnesses and mutant rejection stages are missing. N02’s prose “reject or PLAN_DEFECT” is not an executable oracle. A later author must split malformed native admission inputs from admitted-but-invalid route probes and assign exactly one expected stage/result to each. No missing runtime capability is inferred until complete independent inputs and expectations reproduce a failure.

Machine-readable companions:

- [36-case classification, input pins and validation](DETERMINISTIC_PLANNER_V0_1_E2_P01_REMAINING_BLOCKERS_1_PREFLIGHT.json)
- [Complete blocker inventory](DETERMINISTIC_PLANNER_V0_1_E2_P01_REMAINING_BLOCKERS_1_BLOCKERS.json)
- [Dependency graph](DETERMINISTIC_PLANNER_V0_1_E2_P01_REMAINING_BLOCKERS_1_DEPENDENCIES.json)
- [Closure packages and retry predicate](DETERMINISTIC_PLANNER_V0_1_E2_P01_REMAINING_BLOCKERS_1_CLOSURE_PLAN.json)

## Blockers closed by T01

E2-G01 is closed: `EvidenceSourceAdmission` through `codec.admit_external_evidence`, followed by separate native validation/reentry via `commit_event`. Admission and receipt are a durable pair. There is no supported durable admission-only checkpoint. A09’s “ingestion before receipt” describes internal ordering, not two public commits; the reconciled T01 contract already establishes this interpretation.

Direct affected cases: E2-A09, E2-A10, E2-A11, E2-A12, E2-A13, E2-N04, E2-N14, E2-N15, E2-END. Transitive/variant cases: E2-A15, E2-N03, E2-N05, E2-N11, E2-D01, E2-REVIEW. None becomes executable merely by removing G01. A09 changes from CONTRACT_INCOMPLETE to FIXTURE_INCOMPLETE.

Pre-existing independent ATTEST authority must authenticate the exact future content/producer. Route and ingress source classes must match. Required sources must be pinned in the pre-state, while new evidence bytes enter only at the admission event. A receipt cannot bootstrap its own authority, supply an arbitrary new permission, or set an unknown rule to known. These constraints are inputs to E2-G03/G05, not a new unproven defect.

## Remaining shared blockers

| Blocker | Shared cause | Remaining work | Prerequisites |
|---|---|---|---|
| E2-G02 | ACTION_DEFINITION | Six profiles/native candidates; declared outputs only; producer/prerequisite and authority/evidence references; Independent 78-field/reference closure, selection competition, result boundaries | E2-G03 |
| E2-G03 | SOURCE_ROLE | Pinned source bytes/registry, context, policy; no filename-derived role; Domain/scope/currentness/role exclusivity and source-pin assertions | Pinned native contracts/T01 |
| E2-G04 | PROOF_AND_AUTHORITY_ADMISSION | Distinct proof/authority sources, exact predicate operands and negative mutants; Independent proof and decision-readiness witnesses; requirement != possession; PASS != root/slot | E2-G02, E2-G03 |
| E2-G05 | EXTERNAL_LIFECYCLE | Known-rule mainline plus unknown variant; absent evidence checkpoint; future payload and independent ATTEST premise; Received != validated; validated != resume; unknown stays unknown; C03 named eligibility | E2-G02, E2-G03 |
| E2-G06 | INDEPENDENT_PHASE_AND_MUTATION_ORACLES | Complete phase and one-dimension mutation inputs using one shared fixture universe; Full-state expected outputs, exact rejection stages, selected identities and semantic hashes derived independently | E2-G02, E2-G03, E2-G04, E2-G05 |
| E2-G07 | PERSISTENCE_AND_COLD_RESTORE | Writer/reader harness contract, allowlist, checkpoint manifest and tamper copies; Fresh-process full-state equality, sources and trusted identities; no expected-output files as input | E2-G02, E2-G03, E2-G04, E2-G05 |
| E2-G08 | INTEGRATED_QUALIFICATION_DEPENDENCIES | Integrated runner entrypoints and dependency/evidence manifest; actual execution later; D01/END compositional oracle and fresh-review checklist; no missing fixture hidden by aggregation | E2-G06, E2-G07 |

Each inventory record supplies affected cases, contract, fixture, oracle, runtime consumer, dependencies and reason. G02–G07 are authorable synthetic qualification preparation, not missing historical E1 semantics. G08 is split: missing integrated fixture/oracle interfaces block preflight; later P02–P06 execution evidence blocks running END/REVIEW at that later stage, not writing or approving P01 fixtures. This removes the potential circular dependency without waiving a lifecycle case.

## All 36 cases

| Case | Classification | Recomputed remaining requirement |
|---|---|---|
| E2-A01 | FIXTURE_INCOMPLETE | Six O01/native definitions still null; 60 of 78 planned definition cells lack concrete values; no field/reference oracle. [E2-G02, E2-G03, E2-G06] |
| E2-A02 | FIXTURE_INCOMPLETE | No concrete pair of eligible E2 Actions, admitted policy source or independently derived selection winner. [E2-G02, E2-G03, E2-G06] |
| E2-A03 | FIXTURE_INCOMPLETE | No supplied-result/knowledge fixture with exact producer contract and current source dependencies. [E2-G02, E2-G03, E2-G06] |
| E2-A04 | FIXTURE_INCOMPLETE | No E2 dossier alternatives, checklist and preparation output bound to the human readiness predicate. [E2-G02, E2-G03, E2-G04, E2-G06] |
| E2-A05 | FIXTURE_INCOMPLETE | No bounded E2 simulated decision/grant, target, permission and independent applicability witnesses. [E2-G02, E2-G03, E2-G04, E2-G06] |
| E2-A06 | FIXTURE_INCOMPLETE | Request, absence, held/reentry identities and resolution source are not instantiated for E2. [E2-G02, E2-G03, E2-G05, E2-G06] |
| E2-A07 | FIXTURE_INCOMPLETE | Canonical save exists; no E2 checkpoint input bundle, complete source pins or independently specified manifest. [E2-G02, E2-G03, E2-G04, E2-G05, E2-G06, E2-G07] |
| E2-A08 | FIXTURE_INCOMPLETE | T01 demonstrates fresh-process restoration; E2 state inventory, reader allowlist and full-state comparison remain absent. [E2-G02, E2-G03, E2-G04, E2-G05, E2-G06, E2-G07] |
| E2-A09 | FIXTURE_INCOMPLETE | EvidenceSourceAdmission is qualified; E2-specific ingress bytes, exact ATTEST premise, claim payload, parent and source delta are absent. [E2-G02, E2-G03, E2-G05, E2-G06, E2-G07] |
| E2-A10 | FIXTURE_INCOMPLETE | Native separate validation exists; E2 claim/requirement/authentication correspondence and phase witnesses remain unbound. [E2-G02, E2-G03, E2-G04, E2-G05, E2-G06] |
| E2-A11 | FIXTURE_INCOMPLETE | C03/native reentry exists; complete E2 named Action eligibility, current proofs, accepted lineage and source/policy pins are unspecified. [E2-G02, E2-G03, E2-G04, E2-G05, E2-G06] |
| E2-A12 | FIXTURE_INCOMPLETE | No complete E2-REENTER output/knowledge contract or E2-FINISH prerequisite and selection oracle. T01 does not execute these Actions. [E2-G02, E2-G03, E2-G04, E2-G05, E2-G06] |
| E2-A13 | FIXTURE_INCOMPLETE | No E2 root/slot-specific proof candidate and exact independent typed admission witnesses. [E2-G02, E2-G03, E2-G04, E2-G05, E2-G06] |
| E2-A14 | FIXTURE_INCOMPLETE | Governed-unknown native repair and T01 test remain valid; E2 unknown-variant source/route and exact state witness are absent. [E2-G02, E2-G03, E2-G05, E2-G06] |
| E2-A15 | FIXTURE_INCOMPLETE | Source invalidation is supported; E2 disjoint knowledge/proof/authority/evidence pins and dependent-state oracle after reload absent. [E2-G02, E2-G03, E2-G04, E2-G05, E2-G06, E2-G07] |
| E2-A16 | FIXTURE_INCOMPLETE | Route invalidation native semantics exist; E2 unknown variant and exact no-alternative-route defect witness absent. [E2-G02, E2-G03, E2-G05, E2-G06] |
| E2-N01 | FIXTURE_INCOMPLETE | No E2 unknown baseline and sole no-route mutation with exact PLAN_DEFECT witness. [E2-G02, E2-G03, E2-G05, E2-G06] |
| E2-N02 | FIXTURE_INCOMPLETE | No designated structurally valid wrong-route mutation versus malformed admission mutation; rejection stage must be individually pinned, not an OR assertion. [E2-G02, E2-G03, E2-G05, E2-G06] |
| E2-N03 | FIXTURE_INCOMPLETE | No E2 wrong-lineage mutant; ingress rejection and unknown-route PLAN_DEFECT probes need distinct cases within this case. [E2-G02, E2-G03, E2-G05, E2-G06] |
| E2-N04 | FIXTURE_INCOMPLETE | T01 covers evidence/attestor staleness; E2 received checkpoint, dependency pins and cold invalidation oracle absent. [E2-G02, E2-G03, E2-G05, E2-G06, E2-G07] |
| E2-N05 | FIXTURE_INCOMPLETE | No concrete E2 source-substitution pair; T01 source-pin negatives do not supply the E2 source universe. [E2-G03, E2-G05, E2-G06] |
| E2-N06 | FIXTURE_INCOMPLETE | No applicable E2 grant baseline and designated unrelated/wrong-class/scope mutants. [E2-G02, E2-G03, E2-G04, E2-G06] |
| E2-N07 | FIXTURE_INCOMPLETE | No exact E2 root/slot proof baseline and wrong-target/placeholder mutants. [E2-G02, E2-G03, E2-G04, E2-G06] |
| E2-N08 | FIXTURE_INCOMPLETE | No complete E2 native Action candidate for a single dangling/wrong-domain prerequisite mutation. [E2-G02, E2-G03, E2-G06] |
| E2-N09 | FIXTURE_INCOMPLETE | No E2 current knowledge/history pair with descendant blocking and source invalidation expectations. [E2-G02, E2-G03, E2-G06, E2-G07] |
| E2-N10 | FIXTURE_INCOMPLETE | No E2 bundle/policy fixture and exact alternate pin/version mutation; supported policy contract itself exists. [E2-G03, E2-G06, E2-G07] |
| E2-N11 | FIXTURE_INCOMPLETE | T01 head/ledger controls exist; E2 trusted checkpoint, designated byte/event/source mutation and unchanged anchor absent. [E2-G03, E2-G06, E2-G07] |
| E2-N12 | FIXTURE_INCOMPLETE | No E2 selected-only record and typed rejection/unchanged ledger knowledge oracle; selection is still not a result event. [E2-G02, E2-G03, E2-G06] |
| E2-N13 | FIXTURE_INCOMPLETE | No complete E2 prospective declaration and invalid actual-result input; no definition may itself instantiate execution. [E2-G02, E2-G03, E2-G06] |
| E2-N14 | FIXTURE_INCOMPLETE | Admission/receipt pairing exists; E2 baseline and exact out-of-order validation/reentry mutants absent. [E2-G02, E2-G03, E2-G05, E2-G06] |
| E2-N15 | FIXTURE_INCOMPLETE | No E2 accepted-receipt state with one independently unsatisfied named-Action prerequisite and C03 rejection witness. [E2-G02, E2-G03, E2-G04, E2-G05, E2-G06] |
| E2-N16 | FIXTURE_INCOMPLETE | No E2 independent machine/human/factual-frontier variants and exact precedence witnesses. [E2-G02, E2-G03, E2-G05, E2-G06] |
| E2-D01 | DEPENDENCY_INCOMPLETE | Dimensions are defined, but E2 full-state oracles, concrete identities and permutation runner inputs remain unavailable. [E2-G06, E2-G07, E2-G08] |
| E2-END | DEPENDENCY_INCOMPLETE | Transaction capability is present; integrated E2 fixture/oracle composition and process/continuation runner contract remain incomplete. [E2-G06, E2-G07, E2-G08] |
| E2-REG | EXECUTABLE | Native test suites and assertions exist; fixed-version T01 evidence matches current code. No new E2-REG execution claimed. [none] |
| E2-REVIEW | DEPENDENCY_INCOMPLETE | Review procedure exists; review-subject/evidence manifest and integrated case interfaces are not instantiated. Actual P05 evidence is a later run dependency, not P01 prerequisite. [E2-G08] |

## Lifecycle and continuation

| Edge | Native support / qualification evidence | E2-specific gap |
|---|---|---|
| Governed unknown → external wait | Existing control repair and T01 unknown negative/positive controls; rule remains unknown | G02/G03/G05/G06: exact E2 gate/route/held Action witness absent |
| Wait → persist → cold restore | Native save/restore and T01 fresh-process CLI/crash qualification | G07: E2 checkpoint, trusted identity, complete state comparison and input allowlist absent |
| Cold state → admission + receipt | T01 qualified atomic pair, prefix replay, idempotence and source validation | G03/G05/G06: exact E2 ingress, attestor, future payload and parent bindings absent |
| Receipt → validation/proof | `core.apply_receipt` and native independent claim/obligation proof; T01 separate validation test | G04/G05/G06: exact claim/requirement/proof and received/validated state witnesses absent |
| Validated proof → eligible reentry | Native accepted reentry event plus C03 current evidence, verified source/policy pins and named eligibility | G02/G04/G05/G06: all E2 named-action prerequisites and exact accepted lineage absent |
| Reentry → selection → permitted result → next planning | Native selector and supplied-result validator; no E2 Action executed by T01 | G02/G04/G06: exact E2-REENTER outputs and E2-FINISH prerequisite/proof/selection oracle absent |

**First remaining unqualified edge:** concrete E2 governed-external-boundary inputs → derived external wait. The native edge is supported; the exact E2 Action/route/source fixture and independent witness are missing. Upstream, even initial six-Action construction is incomplete. No further unsupported native edge has been demonstrated.

The mainline must keep a known validation rule with missing evidence; A14 is a separate unknown-rule variant. T01 does not turn the latter into a positive rule-acquisition path. Unknown-rule positive continuation is not required by the E2 plan and must not be smuggled into the mainline.

Post-reentry contract checklist: E2-REENTER is named and its operation/purpose is planned; concrete prerequisite identities, authority applicability, evidence/current proof, prospective result/knowledge and selected-action witness are missing. E2-FINISH is named but its exact dependency/proof operands remain absent. The policy must select from normal actionability; an imposed “run REENTER then FINISH” script is insufficient. G02/G04/G05/G06 cover every item. No final control label or terminal success is guessed.

## Cross-case, negative and determinism checks

All plan entries retain one six-Action baseline, native typed identity domains, the supported policy, source-bound proof/authority predicates, known-rule mainline, isolated unknown variant, canonical bundle and native control computation. No conflicting requirement was established by this review. Concrete cross-case consistency is **not yet proven** because the shared fixture is absent. PC01 must close all references; PC03 must make each mutant reference that baseline and list only designated semantic deltas. Derived content hashes may change mechanically with a mutation; unrelated semantic changes may not.

| Positive boundary | Required negative/control cases | Current coverage |
|---|---|---|
| Governed waiting | N01 no route, N02 malformed route, N03 lineage, A16 invalidation | Native regressions retained; E2 fixtures missing |
| Receipt | N03/N05 invalid source/lineage, N14 lifecycle bypass | T01 rejects invalid ingress atomically; E2 mutants missing |
| Validation/proof | N04 stale evidence, N07 invalid proof, N14 received-only | Native/T01 stage separation retained; E2 witnesses missing |
| Authority and readiness | N06 wrong grant, A04 readiness prerequisites | E2 bounded authority/dossier fixtures missing |
| Resume | N15 independent blocked Action, N03/N05/N04 lineage/source/currentness | C03 unchanged; E2 complete conjunction fixture missing |
| Knowledge and dependency | N08 dangling reference, N09 stale knowledge, A15 reload invalidation | E2 current-source/history pair missing |
| Persistence/policy | N10 policy, N11 tamper | Native/T01 protections present; E2 pinned baseline missing |
| Definition/selection | N12 selection is not execution, N13 prospective is not actual | E2 declaration/result mutants missing |
| Control precedence | N16 independent branch states | Native control semantics present; E2 witnesses missing |

Determinism contract retained: seeds 0/1/7/101; original/reversed/rotated unordered Actions, sources, goals, proofs and authorities; recursive object-key permutations; repeated computation; independent processes and three cold readers per checkpoint/seed. Compare full Computation, witnesses, selection, typed state, policy, resume proof, snapshot/bundle/event identities. Causal ledger history and ordered policy clauses are not permutable sets. Exact E2 canonical identities remain unbound, so D01 is dependency-incomplete and its E2 oracle incomplete. No actual order/hash/process-dependent expected identity was demonstrated; no identity is accepted from implementation output as its own oracle. REG uses existing executable deterministic assertions.

## Dependency-ordered closure packages

### E2-PC01 — FIXTURE

Prerequisites: Pinned current native contracts and qualified T01. Blockers: E2-G03, E2-G02.

Author one closed typed source/identity/policy/envelope registry and all six full O01/native definitions in two ordered substeps. References may be forward-declared then resolved uniquely.

Acceptance: 6/6 complete and independently admissible; 78 O01 cells bound; native required fields/references present; no actual outputs or execution asserted; no null role/policy binding.

Unlocks: E2-PC02.
### E2-PC02 — MIXED

Prerequisites: E2-PC01. Blockers: E2-G04, E2-G05.

Instantiate independent root/slot and decision/authority predicates plus exact external lifecycle contracts. MIXED means fixture and oracle authoring only, not implementation.

Acceptance: Proof/authority source-disjoint positive/negative witnesses; T01 ingress pins, matching route source class and pre-existing ATTEST; no checkpoint evidence; known mainline and unknown variant; C03 and post-reentry Action predicates fully bound.

Unlocks: E2-PC03.
### E2-PC03 — MIXED

Prerequisites: E2-PC02. Blockers: E2-G06, E2-G07.

Author full-state independent phase/mutation oracle and canonical process/checkpoint runner fixtures. No experiment Action execution.

Acceptance: All A/N cases have exact input, operation and independent expected state/rejection; prospective outputs not actual results; each critical edge has negative; trusted identity and source prefix; input allowlist excludes oracle; continuation selection derivable.

Unlocks: E2-PC04.
### E2-PC04 — ORACLE

Prerequisites: E2-PC03. Blockers: E2-G08.

Assemble D01/END and future REVIEW input/evidence schemas and mechanically audit case references/cross-case invariants. Do not run P01 or downstream packages.

Acceptance: 36 runnable case specifications/runner interfaces including deferred execution dependency declarations; no null required input/oracle; no circular preflight requirement on future PASS evidence; consistency and retry predicate clean.

Unlocks: P01 retry eligibility evaluation only.

These four packages group shared preparation: common universe → proof/lifecycle bindings → independent state/process oracles → integrated preflight interfaces. G04 and G05 can be authored independently once the shared universe is pinned, then checked together. This is a bounded sufficient plan, not a mathematical proof of minimum package count. None is executed here. No implementation package is authorized: any later complete oracle/fixture failure must first reproduce a defect and receive a bounded repair scope.

## Retry predicate and preservation

`E2_P01_RETRY_ALLOWED = all 36 preflight case specifications executable AND all required fixtures complete AND all independent oracles complete AND no contract conflict AND all required runtime capabilities implemented/qualified.` Executable is a callable case with explicitly declared future run dependencies, not evidence that its operation already passed. PC04 must not demand future P05 results to retry P01; actual review execution still requires those results.

Predicate is FALSE: 32 incomplete case fixtures plus three integrated dependency interfaces; 34 overlapping independent-oracle gaps. E2-P02 eligibility still requires a later P01 PASS. E2-T01’s test count is preserved historical evidence, not a new execution of the 36 E2 cases.

Verified unchanged content/path set for all 10,911 frozen E1 files; implementation, tests, prior plans, transaction contract and N-REAL artifacts unchanged. No new E1 evidence, authority, runtime transaction or experiment Action was created. N-REAL remains an independent unmet release requirement.

```text
ACCEPTANCE_CASES = 36
EXECUTABLE_CASES = 1 [E2-REG]
CONTRACT_INCOMPLETE_CASES = []
FIXTURE_INCOMPLETE_CASES = [E2-A01, E2-A02, E2-A03, E2-A04, E2-A05, E2-A06, E2-A07, E2-A08, E2-A09, E2-A10, E2-A11, E2-A12, E2-A13, E2-A14, E2-A15, E2-A16, E2-N01, E2-N02, E2-N03, E2-N04, E2-N05, E2-N06, E2-N07, E2-N08, E2-N09, E2-N10, E2-N11, E2-N12, E2-N13, E2-N14, E2-N15, E2-N16]
ORACLE_INCOMPLETE_CASES = [E2-A01, E2-A02, E2-A03, E2-A04, E2-A05, E2-A06, E2-A07, E2-A08, E2-A09, E2-A10, E2-A11, E2-A12, E2-A13, E2-A14, E2-A15, E2-A16, E2-N01, E2-N02, E2-N03, E2-N04, E2-N05, E2-N06, E2-N07, E2-N08, E2-N09, E2-N10, E2-N11, E2-N12, E2-N13, E2-N14, E2-N15, E2-N16, E2-D01, E2-END]  # overlapping findings
DEPENDENCY_INCOMPLETE_CASES = [E2-D01, E2-END, E2-REVIEW]
IMPLEMENTATION_CAPABILITY_MISSING_CASES = []
CONTRACT_CONFLICT_CASES = []
BLOCKERS_CLOSED_BY_T01 = [E2-G01]
REMAINING_BLOCKERS = [E2-G02, E2-G03, E2-G04, E2-G05, E2-G06, E2-G07, E2-G08]
ROOT_CAUSE_GROUPS = [ACTION_DEFINITION, SOURCE_ROLE, PROOF_AND_AUTHORITY_ADMISSION, EXTERNAL_LIFECYCLE, INDEPENDENT_PHASE_AND_MUTATION_ORACLES, PERSISTENCE_AND_COLD_RESTORE, INTEGRATED_QUALIFICATION_DEPENDENCIES]
EXTERNAL_LIFECYCLE_FIRST_REMAINING_GAP = E2-specific governed boundary fixture/oracle -> derived external wait
CLOSURE_PACKAGES = [E2-PC01, E2-PC02, E2-PC03, E2-PC04]
FIRST_CLOSURE_PACKAGE = E2-PC01
E2_P01_RETRY_ALLOWED = NO
E2_P02_READY = NO
N_REAL_SATISFIED = NO
CANONICAL_E2_QUALIFIED = NO
PLANNER_V0_1_REQUALIFICATION_READY = NO
IMPLEMENTATION_MODIFIED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
```

Artifact verification: 36 unique case IDs, complete blocker/case cross-references, acyclic blocker dependencies, complete closure-package coverage, unchanged input pins and `git diff --check` all PASS. These are document/preflight integrity checks, not execution of P01 or E2 cases.
