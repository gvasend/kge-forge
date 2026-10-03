# External-boundary unknown-rule control reconciliation 1

**CLASSIFICATION = PLANNER_CONTROL_DEFECT for independently governed rule acquisition.** An unsupported rule with no valid acquisition route remains a planner defect. The native control check currently conflates that case with a supported obligation whose missing governing rule is itself the subject of a qualified external acquisition contract.

A minimal synthetic counterexample and a mixed-frontier variant reproduce the incorrect global classification. No implementation, codec, migration contract or existing test was changed. This report defines the bounded repair contract; it does not authorize an implementation package or reopen E1.

## Evidence and authority

The [minimum-state analysis](DETERMINISTIC_PLANNER_V0_1_FROZEN_MINIMUM_SUFFICIENT_STATE_1.md) and its dependency-cone, target-classification, operational-subgraph, proof-schema and blocking-cut companions identify CUT04. The [backlog](../backlog/DETERMINISTIC_REASONING_PLANNING_RUNTIME.md) supplies independent semantics:

- Fact acquisition/reentry specifies a named producer/permitted source, proposition, authentication and failure gate; missing facts are not inferred.
- Proof obligations distinguish PROOF_RULE_UNKNOWN from PROOF_RULE_KNOWN_EVIDENCE_MISSING; a convenient validator default cannot fill either.
- External lifecycle separates request, receipt, validation and reentry. Partial, negative or unrelated evidence cannot clear the proof gate.
- Branch suspension preserves unresolved conditions and recomputes independent branches.
- Global controls distinguish legitimate waits from missing routes, and planner-defect handling prohibits diagnosing a valid wait as a defect merely because it has no action.

The [original implementation plan](DETERMINISTIC_PLANNER_V0_1_IMPLEMENTATION_PLAN.md), global-control precedence, also requires PLAN_DEFECT for an unsupported required rule/missing route. These provisions coexist: a missing implementation of a required predicate is not the same as missing external evidence establishing which governing rule applies. A known bounded rule-acquisition/validation procedure is necessary before the second case can be treated as governed waiting.

[BR-C1](DETERMINISTIC_PLANNER_V0_1_BR_C1_CONTRACT.json) provides exact expected-absence/source correspondence. The frozen [request](../experiments/E1/E1_BUDGET_APPLICABILITY_EXTERNAL_EVIDENCE_REQUEST_1.json), [handoff](../experiments/E1/E1_EXTERNAL_HANDOFF_PACKAGE_1.json) and [manifest](../experiments/E1/E1_RESUME_MANIFEST_1.json) are corroborating domain evidence, not the sole basis for this rule. In particular, requesting an applicable governing rule does not itself establish that rule or a ready Architect decision.

Implementation evidence: [core.py](../../adapter/planner/core.py), [gates.py](../../adapter/planner/gates.py), [model.py](../../adapter/planner/model.py). The existing `test_all_seven_global_controls_and_local_defect_precedence` in [test_planner_e1_replay.py](../../adapter/tests/test_planner_e1_replay.py) flips `rule_known=False` and deliberately expects PLAN_DEFECT. That unsupported-rule negative must be preserved with an explicitly ungoverned case; the blanket expectation is too broad for a separately admitted acquisition contract.

The [validation companion](DETERMINISTIC_PLANNER_V0_1_EXTERNAL_UNKNOWN_RULE_RECONCILIATION_1_VALIDATION.json) contains exact synthetic source data, source content hash, executable probe program, six observed outcomes, canonical identities and separate-process reload comparisons. Expected outcomes come from the rules above, not from the probe's outputs. The program constructs typed native state and calls real public computation/codec functions without mocks.

## Exact current execution path

1. `recompute` calls `project`/`validate_model`, then `evaluate_satisfaction` and `_actionability`. Invalid typed references reject before a control result is produced.
2. `_obligation_proof` returns UNKNOWN/PROOF_RULE_UNKNOWN for `EvidenceRequirement.rule_known=False`. `blockers` therefore does not admit the dependent action. An external gate also holds its named actions unless accepted reentry and complete proof exist. Existing BLOCKED/WAITING holds independently suppress actionability.
3. `_global_control.walk` follows unsatisfied prerequisite paths. At a reached EXTERNAL_EVIDENCE boundary it evaluates:

```python
if (not gate.contract_complete
    or gate.validation is not ValidationState.ACCEPTED
    or any(not r.rule_known for r in snapshot.evidence_requirements
           if r.id in gate.requirements)):
    defects.add('UNQUALIFIED_EXTERNAL_CONTRACT:' + gate.id.value)
```

4. The same reached boundary still produces branch WAITING_FOR_EXTERNAL_EVIDENCE. The global precedence then chooses PLAN_DEFECT when there is no machine selection or ready human batch. This can yield a waiting branch alongside a global defect whose only cause is the unknown rule flag.
5. `_check_receipt` independently rejects claims when the proof rule or producer is unknown. `external_complete` requires every obligation PROVED. `resume_eligibility` additionally requires stage, accepted reentry event/lineage, policy/context binding, current sources and named-action eligibility. Fixing control classification must not relax any of these proof or permission checks.

There is a second relevant guard: reached Action requirements evaluated as `UNSUPPORTED_RULE` add `UNSUPPORTED_REQUIRED_RULE`. A real missing predicate implementation must retain that diagnostic. Do not replace an unsupported predicate with a waiting label to evade it.

## Semantic distinction and existing types

These are **derived contract classifications**, not proposed new enum members:

| Classification | Meaning and existing representation | Expected behavior |
|---|---|---|
| UNEXPLAINED_UNKNOWN | Required rule absent/unsupported; no independently admitted acquisition path | Block dependent action; report precise PLAN_DEFECT when no higher-precedence independent work exists |
| INTERNAL_ACQUISITION_PENDING | Supported bounded acquisition Action and typed prerequisites/acceptance route exist; required rule/evidence not yet acquired | Dependent stays blocked; acquisition runnable only if its own gates pass; otherwise follow its actual prerequisite frontier |
| EXTERNAL_ACQUISITION_PENDING | EvidenceRequirement plus qualified ExternalGate, boundary and receipt/reentry correspondence govern acquisition of the missing rule | Preserve UNKNOWN proof and held work; expose external wait rather than a defect solely for absence |
| RECEIVED_INVALID | Concrete receipt/observation exists but authentication, correspondence, currentness or positive proof fails | No reentry; retain rejection and qualified wait for replacement, unless the acquisition contract itself is defective |
| KNOWN_VALID | Independently admitted rule and applicable evidence are current | Evaluate normal obligation/receipt/reentry semantics; existence of a rule alone does not prove its application |

Action, Predicate, EvidenceRequirement, ExternalGate, ReceiptAdmission/Observation, ExternalStage and source/context identities already represent the main lifecycle. No new five-value enum is necessary. What is missing is an enforcing **governed-acquisition correspondence check**, distinct from `rule_known`. A Boolean `contract_complete=True` is insufficient by itself. If the existing typed references cannot persist all necessary correspondence, implementation must propose the smallest explicit reference binding; prose provenance or a new unvalidated enum must not become authority.

## Independent governed-path admission contract

Let `governed_unknown(requirement, branch, snapshot, pinned_contract)` be true only if all these obligations hold:

1. The missing proposition has an exact EvidenceId, target identity/domain and source-pinned definition. It explicitly identifies the missing rule/application evidence; it is not an unknown operation or arbitrary opaque callback.
2. An independently accepted bounded acquisition contract specifies the allowed source class/competence role, permitted inputs and deterministic receipt validation. A concrete positive producer may remain unestablished where the contract says so; then positive receipt cannot yet authenticate. Missing authentication semantics cannot be disguised as an unspecified producer.
3. The requirement belongs to the exact gate. The gate/boundary covers the actual blocked consumer, with the correct request, receipt and reentry actions and any downstream dependency. Typed identities and action references resolve uniquely. An unrelated gate cannot explain this unknown.
4. Scope, lineage and target/envelope correspondence agree with the independently pinned acquisition contract. Required source pins and current acceptance are verified. A matching name or compatible-looking payload is not correspondence.
5. The gate is in a legal pending/received-but-unaccepted lifecycle state, its acquisition contract is current, and no accepted complete proof is asserted. No source invalidation has withdrawn the governing route itself.
6. The positive proof remains unsatisfied, and the receipt/reentry path retains its normal evidence, authority and lifecycle checks. Acquiring rule bytes cannot install executable semantics or mark `rule_known=True` without separately governed validation.

These clauses are the minimum repair's admission requirements. They must be enforced through the existing typed model and validation path; this report does not claim that today's model independently checks them all. The synthetic fixture author supplies a pinned, qualification-only complete acquisition contract as an independent premise. Native control ignores that distinction and rejects solely on `rule_known`; this is the reproduced defect. It is not proof that self-asserted metadata or arbitrary gates are safe to admit.

## Bounded control-state matrix

Assume structurally admitted state, an unresolved goal and no terminal-failure proof. “Machine”/“human” columns mean legitimate independent runnable/decision-ready work, not merely a declared action or dossier. Local defects remain reported even when higher-precedence work controls the global state.

| Required-rule/route case | Neither independent branch | Human only | Machine only | Both |
|---|---|---|---|---|
| Known rule, valid route, positive evidence missing | EXTERNAL_WAIT; MIXED_WAIT if other factual frontier present | HUMAN_HANDOFF | RUNNABLE | RUNNABLE |
| Unknown rule, no governed route | PLAN_DEFECT | HUMAN_HANDOFF with local defect | RUNNABLE with local defect | RUNNABLE with local defect |
| Unknown rule, internal acquisition itself actionable | RUNNABLE (the acquisition action) | RUNNABLE | RUNNABLE | RUNNABLE |
| Unknown rule, qualified external acquisition | EXTERNAL_WAIT; MIXED_WAIT with independent fact-blocked frontier | HUMAN_HANDOFF | RUNNABLE | RUNNABLE |
| Rule/evidence received but invalid; acquisition route still valid | EXTERNAL_WAIT; MIXED_WAIT with factual frontier | HUMAN_HANDOFF | RUNNABLE | RUNNABLE |
| Rule/evidence received and validated | Normal reentry evaluation: no automatic resume; WAIT until required transition, RUNNABLE only if named action becomes actionable | HUMAN_HANDOFF if no newly runnable machine action | RUNNABLE | RUNNABLE |

An internally blocked acquisition is not automatically RUNNABLE or PLAN_DEFECT: recursively classify its actual prerequisite route. An unsupported internal acquisition or missing route is defective. A malformed external contract yields PLAN_DEFECT in the first column. Structural malformation can instead raise PlannerError before control classification; this is fail-closed rejection, never a valid wait. Invalid snapshot-wide admission cannot be rescued by an independent branch. Completed goals/irrecoverable failure retain their existing terminal rules; this matrix does not override them.

For valid received evidence, a known rule without complete applicability facts is still incomplete. Even complete proof needs the accepted reentry transition. Do not invent a single control enum for all “validated” states.

## Counterexample and negative controls

The primary fixture has one SOURCE_ACQUISITION action, one unresolved root/goal, one supported EVIDENCE_OBLIGATION predicate, one unknown EvidenceRequirement, one exact waiting ExternalGate and its EXTERNAL_EVIDENCE boundary. Its source contract fixes the missing proposition, producer role, target, receipt/reentry action, scope and lineage. No evidence or authority is granted. The action begins ACTION_ELIGIBLE so the real gate/proof checks, rather than a preexisting BLOCKED hold, suppress actionability.

| Probe | Independent expectation | Current native result |
|---|---|---|
| Qualified external unknown | EXTERNAL_WAIT | PLAN_DEFECT; only `UNQUALIFIED_EXTERNAL_CONTRACT:TEST-GATE`; branch WAITING; actionable=[]; obligation UNKNOWN |
| Same state with known rule, missing evidence | EXTERNAL_WAIT | EXTERNAL_WAIT, no defects |
| Unknown with gate and boundary removed | PLAN_DEFECT | PLAN_DEFECT; `MISSING_CONTROL_ROUTE:TEST-ACTION` |
| Unknown with incomplete acquisition contract | PLAN_DEFECT | PLAN_DEFECT; UNQUALIFIED_EXTERNAL_CONTRACT |
| Qualified external unknown plus independent factual frontier | MIXED_WAIT | PLAN_DEFECT; budget-like branch WAITING, other FACT_ACQUISITION_REQUIRED |
| Qualified external unknown plus independent runnable action | RUNNABLE | RUNNABLE, but spurious local UNQUALIFIED_EXTERNAL_CONTRACT remains |

All six states pass native snapshot encoding/decoding. All six classifications/defects/actionable sets reproduce after a separate process cold-loads their canonical snapshot bytes. These are snapshot-level probes, not full PersistenceBundle resume qualification. No actual E1 state or migration was loaded into the planner. The source contract/program and exact identities are saved in the validation companion; temporary synthetic source/snapshots reside under `/tmp`.

`PRE_REPAIR_COUNTEREXAMPLE=REPRODUCED`. The positive fixture's expected wait assertion would fail against current code. `NEGATIVE_CONTROL=PASS`: removing the route preserves PLAN_DEFECT. No passing repair test is claimed.

## Minimum repair contract; no implementation in this task

Introduce/reuse one typed governed-acquisition validation check at the existing admission/control boundary. In `_global_control`, an unknown obligation may avoid the unknown-rule defect **only** when that exact requirement/consumer is covered by the independently admitted current acquisition/reentry contract above. Keep incomplete/stale/unbound gate rejection and unsupported-predicate defects. Do not remove the `rule_known` test unconditionally or set it true during migration.

Keep `_obligation_proof` UNKNOWN for unavailable rules and `_check_receipt` fail closed until actual positive governing rules and trusted evidence are admitted. Keep all resume conjunctions unchanged. Prefer one shared route-validation predicate consumed by validation and control, rather than a parallel planner or a string-based special case. Preserve deterministic ordering and persisted source dependencies. The existing unknown-rule regression remains a negative for an ungoverned/unsupported requirement; add the governed counterexample as a separate positive.

Required repair qualification:

- Exact external unknown → EXTERNAL_WAIT; plus factual wait → MIXED_WAIT, with no unknown-rule defect.
- No route, unrelated/malformed route, missing requirement, incorrect consumer, wrong receipt/reentry lineage, substituted source/target, stale acquisition contract and unknown validator → PLAN_DEFECT or typed admission rejection as appropriate; never ordinary waiting.
- Received invalid evidence retains wait/rejection, not proof; valid evidence follows receipt→validation→accepted reentry and all C03 checks.
- Internal bounded acquisition may be runnable, but does not make its consumer runnable prematurely.
- Independent machine/human branches preserve precedence and local diagnostics.
- Canonical cold reload, source invalidation and relevant input/hash ordering preserve every classification.
- Existing A–N, X01–X11, C01–C06, external/control/resume and synthetic budget suites remain required. The historical BLOCKED producer does not invalidate independently current accepted knowledge.

Wrong-lineage data that is structurally well-formed must be rejected by semantic route admission, not merely because an arbitrary bad string happens to violate a schema. Tests must distinguish loss of positive evidence (continue governed wait) from loss of the acquisition contract's own validity (defect/unqualified route).

## Frozen-state and migration consequences

A qualified rule-acquisition route would allow the relevant unresolved frozen boundary to be represented without an automatic unknown-rule defect. Budget still has no accepted positive matrix; the seven other factual boundaries retain their own kinds. This repairs the CUT04 semantic obstacle only. CUT01–05 remain the recorded dependency interfaces; closing CUT04 requires separate implementation and qualification. The full frozen certificate, other four interfaces, full migration and requalification do not pass by inference.

Affected M01 categories: Snapshot.evidence_requirements, external_gates, boundaries, predicates and their action/goal bindings; source/derivation metadata and initial/current bundle preservation support the route. M01-G05/G06 require the clarified handoff and independent positive/negative tests. No new external evidence is required. Migration must carry governed pending state faithfully after the native admission contract is available; it must not force `rule_known=True`, rewrite actual waiting as positive proof, or hide the route as provenance-only.

`MIGRATION_CHANGE_REQUIRED=NO` means no workaround or change to frozen semantics is warranted. A later implementation must populate the reviewed typed acquisition correspondence, which is still pending migration contract work. No current migration implementation was changed. No existing correction convention cited here explicitly authorizes analysis-plus-repair; this task therefore stops at the repair contract.

```text
CURRENT_RULE = unknown rule at reached EXTERNAL_EVIDENCE boundary => UNQUALIFIED_EXTERNAL_CONTRACT => PLAN_DEFECT absent higher-priority work
GOVERNING_RULE = governed acquisition pending => wait/block by that path; unexplained unsupported rule => defect; neither permits positive proof or resume
UNKNOWN_RULE_STATES = [UNEXPLAINED_UNKNOWN, INTERNAL_ACQUISITION_PENDING, EXTERNAL_ACQUISITION_PENDING, RECEIVED_INVALID, KNOWN_VALID] (derived classifications)
CONTROL_STATE_MATRIX = six bounded rows with independent machine/human precedence, above
PRE_REPAIR_COUNTEREXAMPLE = REPRODUCED
NEGATIVE_CONTROL = PASS (PLAN_DEFECT)
CLASSIFICATION = PLANNER_CONTROL_DEFECT
PLANNER_CHANGE_REQUIRED = YES
MIGRATION_CHANGE_REQUIRED = NO (no semantic workaround; typed route mapping still required)
MINIMUM_REPAIR = independently validate exact governed acquisition correspondence; exempt only that pending unknown from control-defect classification; preserve proof/receipt/resume rejection
FROZEN_MINIMUM_STATE_IMPACT = CUT04 repair candidate established; no full frozen certificate qualified
M01_TARGETS_AFFECTED = [evidence_requirements, external_gates, boundaries, predicates, actions/goals route bindings, provenance/source dependencies, initial/current]
M01_CLOSURE_REENTRY_ALLOWED = NO
M02_READY = NO
V0_1_CURRENT_STATUS = CORRECTION_REQUIRED
IMPLEMENTATION_MODIFIED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
```

Preservation checks: all10,911 frozen E1 files and all pre-existing captured implementation/plan/backlog/E1 files retain their hashes. Only this report and its validation companion are new. Local links, JSON and `git diff --check` passed. No existing tests or migration contracts were edited; no E1 evidence was created or action executed.
