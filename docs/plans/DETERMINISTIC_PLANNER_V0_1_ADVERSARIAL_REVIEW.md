# Deterministic Planner v0.1 — Adversarial implementation review

VERDICT = QUALIFICATION_REQUIRES_CORRECTION

Four major findings contradict the blanket qualification. Two minor findings concern deterministic reporting and policy binding. Three observations delimit trust, goal scope and the otherwise useful implementation. Existing passing tests are not discarded, but they do not establish the claimed completion gate under the counterexamples below.

This is review only. No fixes, test edits, qualification edits, authority changes or E1 resumption were performed. “Independent” describes fresh adversarial constructions and code tracing independent of qualification oracles; it does not claim a separate author or organizational audit. Temporary probes ran with `python3 -B` outside the repository. No real-manifest restore command or `import_e1` invocation was performed during this review. The M replay fixture was read and recomputed in isolation.

Authoritative basis: [implementation plan](DETERMINISTIC_PLANNER_V0_1_IMPLEMENTATION_PLAN.md), [acceptance matrix](DETERMINISTIC_PLANNER_V0_1_ACCEPTANCE_MATRIX.md), [backlog](../backlog/DETERMINISTIC_REASONING_PLANNING_RUNTIME.md), [E1 traceability](../backlog/DETERMINISTIC_REASONING_PLANNING_RUNTIME_E1_TRACEABILITY.md), and the existing [qualification](DETERMINISTIC_PLANNER_V0_1_QUALIFICATION.md)/[JSON](DETERMINISTIC_PLANNER_V0_1_QUALIFICATION.json). Implementation evidence below comes from executable code and probes, not those documents' PASS labels.

## Findings

### F01 — MAJOR — Stale ordering evidence removes a prerequisite and can satisfy a root

**Evidence:** `adapter/planner/core.py:20` (`project`) skips every non-ACCEPTED assertion before handling REQUIRES. `evaluate_satisfaction` at line 72 subsequently evaluates only the remaining projection. `adapter/planner/codec.py:266` (`invalidate_sources`) stales the ordering assertion but does not necessarily stale its subject or preserve an unresolved ordering obligation.

**Observed counterexample:** Two unresolved roots, `child` and `prerequisite`; an accepted explicit `child REQUIRES prerequisite` assertion; an independently accepted knowledge predicate proving `child`. Initially `child` remains UNRESOLVED. Invalidate only the ordering assertion's source, keeping the independent knowledge source current. The edge becomes STALE, disappears from the projection, and `child` becomes SATISFIED while `prerequisite` remains unresolved. This was reproduced through `invalidate_sources`, not just by manually assigning STALE. Ordering and proof provenance used different verified fixture source identities.

**Affected:** R16/R20; C/N; X02/X10; fail-closed prerequisite and propagation requirements. Action metadata can protect duplicated action prerequisites, but does not protect root/slot ordering expressed only by assertions.

**Failure scenario:** Editing or invalidating an ordering source weakens the conditions for readiness. A downstream action depending on the newly satisfied root can subsequently become eligible without resolving the original prerequisite.

**Qualification:** Requires correction; stale invalidation is not uniformly fail-closed.

**Minimum correction:** Preserve invalidated ordering as an explicit unsatisfied obligation or stale/block affected dependents transitively. Do not silently delete its enforcement meaning. Add independent root/slot ordering invalidation controls, including downstream actionability. Not applied.

### F02 — MAJOR — Resume eligibility remains true after its supporting evidence is stale

**Evidence:** `adapter/planner/replay.py:401` (`plan_output`) computes `resume_allowed` solely by finding a gate whose stage is DEPENDENT_ACTION_REENTRY. It does not require `external_complete`, a current eligible reentry action, or the absence of another applicable gate. The gates/core correctly reject the stale evidence; the presentation disagrees.

**Observed counterexample:** In an isolated K-derived synthetic state, admit and validate a complete independently attested receipt and advance to reentry. Invalidate the independent attestor's source with `invalidate_sources`, then call `plan_output` on the resulting canonical bundle. Results:

```json
{"complete":false,"actionable":[],"resume_allowed":true,"control":"EXTERNAL_WAIT"}
```

**Affected:** R08/R10/R15/R20; J/N; X01/X04/X10. The plan requires accepted evidence sufficient to enable a legitimate reentry, not merely a historical stage label.

**Failure scenario:** A CLI/control consumer treats the resume field as permission to transfer control even though the scheduler has no eligible action. Core actionability itself stayed closed in this probe; no actual E1 resumption occurred.

**Qualification:** Resume eligibility qualification requires correction.

**Minimum correction:** Derive the flag from current validated proof and actual reentry eligibility; keep historical lifecycle progress separate. Test stale, conflicting and independently blocked reentry after prior successful receipt. Not applied.

### F03 — MAJOR — Full E1 import preserves contract text without restoring corresponding operational semantics

**Evidence:** `adapter/planner/replay.py:315` (`import_e1`) loads the pinned `M_P05.json` normalization, checks action/root/slot identity coverage, then adds source graph entities, assertions, history and manifest fields as provenance-only GraphAssertions with `relation=None`. The full-source records are retained faithfully, but their typed operational meaning is not installed.

Direct inspection of the executable M normalization found:

```text
63 actions
0 Decision objects
0 GraphEntity objects
0 actions with typed requirement predicates
0 actions with authority predicates
all action accepted_result contracts default to PASS
```

These values were computed from the decoded snapshot, not copied from an expected report. The input includes historical authority-required/external-gate outcomes, decision dossiers and authority records. Those records are not equivalent to the default future action acceptance contracts. Native serialization faithfully retains this reduced state; it cannot reconstruct omitted operational contracts from opaque JSON text.

**Affected:** R01/R04/R07/R15/R17/R18/R20/R22; full N, M and P06's importer/full-state completion gate. The plan permits unsupported relationships to remain opaque and permits a reviewed normalization. It does not make opaque retention of all decision/authority semantics equivalent to restoring every state element governing future eligibility and accepted results.

**Failure scenario:** The frozen MIXED_WAIT report is reproduced using prior-attempt holds and explicit boundaries. After a boundary is released, a source/fact action has no restored source/authority predicates or original bounded result inventory; human actions lack Decision objects and fail closed for the wrong reason. The qualified full-state receipt test deliberately stops at selecting FACT-BUDGET-APPLICABILITY and does not exercise the restored action contract. This is a mixture of under-enforcement and inability to continue, not proof that the current frozen wait result is wrong.

**Qualification:** Full semantic cold-resume readiness is not established. Byte-preserving cold reconstruction of the reduced model is established by the existing test design.

**Minimum correction:** Restore the applicable typed action contracts, decision stages/dossiers, authority/evidence references and reentry requirements from a reviewed versioned mapping. Where a rule is unsupported, represent an explicit blocking rule rather than an empty requirement/default PASS contract. Test a supplied bounded action result after isolated reentry and decision-route reconstruction. Not applied.

### F04 — MAJOR — Structured decoding accepts dangling predicate references

**Evidence:** `adapter/planner/model.py:610` (`validate_p03`) checks predicate operands and references *to* predicate IDs, but does not comprehensively validate `Predicate.entity`, `other`, `action`, `condition` or `knowledge` against their applicable target collections. `codec.decode_snapshot` consequently accepts structurally dangling input.

**Observed counterexample:** A SOURCE_IDENTITY predicate with `entity=EntityId('absent')`, no such GraphEntity, survives `decode_snapshot(snapshot_bytes(state))`. A self-referential ALL predicate also survives decoding; evaluation returns UNKNOWN rather than a schema/cycle diagnostic. The dangling reference is a definite importer violation; whether every logical predicate cycle must be rejected deserves an explicit rule rather than reliance on recursion fallback.

**Affected:** R16/R18/R20; P06 strict importer requirement; malformed-reference qualification. Existing tests reject dangling action requirement IDs, but not the referenced objects inside valid Predicate records.

**Failure scenario:** An input presented as structurally validated can contain misspelled or missing authoritative objects. These examples remain unknown during evaluation rather than granting authority, but invalid-input rejection and reliable defect diagnosis are not established. Optional missing bindings need explicit representation distinct from dangling declared IDs. Future knowledge outputs are legitimate forward references and need validation against their declared producer contracts, not a blanket rejection of all not-yet-produced knowledge.

**Qualification:** Importer PASS requires correction.

**Minimum correction:** Validate each predicate kind's required/optional fields, target domains and declared references, including explicit future-output bindings. Decide and enforce forbidden predicate-cycle semantics. Not applied.

### F05 — MINOR — Equal-spelling typed goal IDs produce order-dependent branch reports

**Evidence:** `core._global_control` sorts goals by `goal.target.value` alone, whereas the model permits distinct `ConditionId('same')` and `SlotId('same')`. The codec treats goals as a set-valued collection.

**Observed:** Reverse the two goals in an otherwise identical satisfied state. Canonical snapshot bytes are identical, but `core.recompute` results differ: the `branches` tuple retains input order for the tied spellings. The scalar control remains TERMINAL_SUCCESS; no selected ActionId changed.

**Affected:** R02/R12/R15/R22; complete semantic-output determinism beyond hash-seed tests.

**Qualification:** The broad deterministic-output claim needs a narrow correction. This is not evidence of nondeterministic scheduling.

**Minimum correction:** Use the existing typed `_key` ordering consistently for goal sorting and avoid collapsing typed witnesses to ambiguous bare strings. Add equal-spelling cross-domain permutation controls. Not applied.

### F06 — MINOR — An unrelated artifact is accepted as the pinned selection policy

**Evidence:** `replay.import_fixture` verifies the supplied policy ArtifactPin's bytes, then installs hard-coded `E1-SELECTION-1-P05`. `codec._replay` allowlists version labels but does not bind them to an expected policy identity. `selector.py` uses its static priority map rather than the policy artifact's content.

**Observed:** Replace only B's policy pin with its already verified Candidate-3 construction-authority pin. Import succeeds and reports that authority file as the policy artifact.

**Affected:** R02/R15/R20; policy provenance and replay trust.

**Failure scenario:** A valid content hash is mislabeled as selection-policy identity. The attacker did not change the selector in this probe; the defect is incorrect assurance and audit binding.

**Qualification:** Policy-binding claims need correction; current fixed-selector replay results are not thereby disproved.

**Minimum correction:** Bind each supported policy/version to its admissible policy artifact identity or a canonical parsed policy contract. Reject unrelated valid hashes. Not applied.

## Implementation trace of all 22 required areas

Module paths below are under `adapter/planner/`; tests under `adapter/tests/`. `core`, `invariants`, `resume`, and `e1_replay` denote the four `test_planner_*.py` files. Supporting R14/R23 are not silently promoted into additional runtime requirements.

| Requirement | Actual enforcing path/types | Tests and cases/invariants | Assessment |
|---|---|---|---|
| R01 typed independent states | `model.ActionState/ActionResult/RootCondition/ValueSlot`; `core._inventory/evaluate_satisfaction` | core vertical slice; replay E; X07 | Separation exists; F01 undermines one propagation path |
| R02 total selection | `selector.select/priority_class`; `core.recompute` | core D orders/replay/metrics; I/L | Selection guard strong; F05/F06 qualify broader claims |
| R03 accepted knowledge | `validate_result`; `_inventory`; `KnowledgeRecord` | E–H inventory rejection/partial results | Explicit bounded inventory, no PASS-to-root shortcut |
| R04 decision readiness | `gates.decision_readiness`; `core._decision_result` | F–I; nine-check negative controls/X05 | Enforced in decision fixtures; omitted by full importer F03 |
| R05 input routes | typed Decision stages; `_decision_result` | F/G/H and out-of-order transition tests | Enforced where route objects exist |
| R06 human batches | `_human`, `_human_batches`, `recompute` | I and machine-priority controls | Machine work precedes review; no automatic decision execution |
| R07 fact outcomes/reentry | `_inventory`, `apply_receipt`, `ExternalEvent` | J–N | Typed replay routes exist; F03 loses full imported contracts |
| R08 applicability | `usable`, `obligation_proof`, `external_complete` | J; X01/X04 | Reference alone insufficient; F02 misreports resume |
| R09 proof obligations | EvidenceRequirement, ProofState; `evaluate_predicate` | F/H/J/K; X08 | Rule/absence distinguished; F04 structural gap |
| R10 receipt lifecycle | `apply_receipt`, `check_receipt`; typed admissions/observations | K and synthetic receipts; X08/X10 | Independent attestation/coverage checks exist |
| R11 branch waits | `gates.blockers`; `_global_control.walk` | L/M | Independent runnable work preserved |
| R12 global controls | `core._global_control` | P05 control table; new combinations below | Declared-goal semantics; F05 ordering; scope caveat O02 |
| R13 frontier | `_global_control.walk`, frontier witnesses | M/N | Traverses prerequisite boundaries rather than dumping all roots |
| R15 resume/persistence | `codec._wire/_replay/save_bundle/restore`; `replay.plan_output/import_e1` | resume tests/full N | Hash-chain mechanics exist; F02/F03/F06 limit qualification |
| R16 defects/fail-closed | `validate_model/project`, finite gate evaluation | C/D/F; invariants | F01/F04 are counterexamples to completeness |
| R17 identity types | ArtifactIdentity/IdentityKind; typed equality/authority gates | A/B/J; X11 | Hash-domain distinctions enforced on typed operational fields |
| R18 producer/consumer | `evaluate_predicate`, slot mandatory-link checks; `consumer_identity_precheck` | A/B; X06 | Real A identity call; F03 loses full imported links |
| R19 pure validation | closed consumer check; pinned `invocation_constructor.identity` | A and pure/effecting negative controls/X09 | No issuance path executed |
| R20 provenance/staleness | fixture source projections, `load_pinned`, `invalidate_sources` | all sources, resume/invariants; X10 | Byte verification strong; F01/F04/F06 gaps |
| R21 no probabilistic fallback | `recompute/_global_control`; no LLM connector | M/N | Empty actionability never invokes reasoning |
| R22 replay suite | four test files, pinned fixtures, subprocess CLI | A–N/X01–X11 | Useful suite, not exhaustive; weaknesses below |
| R24 preservation | output-path exclusion, isolated fixtures, source pins | resume no-E1-write checks | Review inventory confirms no E1 changes |

## Replay independence and strength

| Replay | Strength | What is actually exercised / limitation |
|---|---|---|
| A | STRONG | Actual pinned Candidate-2 bytes reach actual pure identity function. Mock forbids construction; it does not replace identity validation. Later reconciliation is explicitly counterfactual. |
| B | ADEQUATE | Three independent missing predicates and a construct-only grant block the action. Missing links are manually normalized facts; producer/source discovery is not tested. |
| C | STRONG | Actual projection and positive prerequisite variants; not a supplied selected ID. |
| D | STRONG | Selector computes the result across permutations, fallbacks, metrics and replay; oracle IDs are compared afterward. Does not cover F05's control-output ordering. |
| E | STRONG | Selected bounded PASS updates knowledge and completion; roots/slots are separately asserted unchanged and invalid inventory variants are rejected. |
| F | ADEQUATE | Corrected decision-input route evaluates missing facts rather than historical premature-ready state. Trusts reviewed fact normalization. |
| G | ADEQUATE | Applies the supplied accepted dossier and independently evaluates all checklist predicates. Test helper copies the action's accepted inventory, so it tests acceptance/state machinery rather than independent semantic dossier derivation; appropriate to v0.1, with that limit. |
| H | ADEQUATE | Missing owner/selector predicates produce FACT_BLOCKED and partial knowledge survives. Missingness is normalized fixture input, not discovered by the runtime. |
| I | STRONG | Actual machine/human routing, interference and dependency variants; no decision is executed. |
| J | STRONG | Reference-only knowledge leaves eight obligations unproved; no identity-to-currentness coercion. |
| K | STRONG | Explicit external stages, malformed/partial receipts and separate reentry; no request-sending shortcut. |
| L | STRONG | Adds genuinely independent work to a waiting branch and recomputes actual selection. |
| M | WEAK | Real traversal computes the eight-member frontier, but input already encodes historical holds/boundaries and omits operational decision/authority contracts. No expected actionable list is passed to core; this is not tautological, but it cannot establish full-graph actionability soundness. |
| N | WEAK | Fresh-process byte reconstruction is substantial and non-tautological. Semantic completeness is checked mainly through the same normalized projection/implementation, counts and opaque record preservation. Synthetic reentry rewrites trust/context outside E1 and stops before the restored selected action's bounded contract is applied. F02/F03 are missed. |

No replay was classified TAUTOLOGICAL. `expected` is kept outside core evaluation. The main shared-oracle risk is completeness: using the same normalization and serializer on both sides proves repeatability, not that every authoritative contract was represented. Post-hoc final-state snapshots are appropriate to M's historical wait, but cannot substitute for earlier-stage decision fixtures or complete future operational state.

## Adversarial global-control results

These used assembled typed states and existing source provenance, not the qualified expected-result dictionaries. All seven scalar states were inspected; MIXED_WAIT was independently recomputed from the M replay fixture (27 unresolved roots, 41 slots, eight frontier members).

| Combination | Observed result | Assessment |
|---|---|---|
| Runnable + external waiting | RUNNABLE | Correct machine precedence |
| Human ready + runnable | RUNNABLE, independent action selected | Correct batching boundary |
| Human ready + external waiting | HUMAN_HANDOFF | Correct human precedence after machine exhaustion |
| Local missing-route defect + independent runnable | RUNNABLE with defect retained | Matches plan's localized-defect rule |
| Structural prerequisite self-cycle + potential runnable | PLAN_DEFECT, no selection | Matches whole-projection failure rule |
| Pure admitted external wait | EXTERNAL_WAIT | Correct |
| Mixed final source/evidence boundaries | MIXED_WAIT | Correct for supplied normalization |
| No actions; explicit proved goal | TERMINAL_SUCCESS | Correct |
| No actions; explicit unrecoverable proved goal failure | TERMINAL_FAILURE | Correct |
| No actions; unresolved root but no goals | `control=None`, NO_INTERNAL_ACTION | Partial model has no global classification; see O02 |
| No actions; one proved goal and an undeclared unresolved root | TERMINAL_SUCCESS, unresolved count 1 | Consistent with declared-goal rule, not proof that all represented roots are ready |

## Persistence, cold resume and real frozen-E1 readiness

Canonical snapshots represent the implemented action, root, slot, predicate, dossier, gate, context and receipt fields. Native event records include sequence, parent snapshot, parent event, supplied event and resulting identity; `_replay` recomputes event outcomes and checks current-state equality. Source pins and separately persisted event bytes are checked on restore. No hidden Python object or conversation dependency was found in the native codec.

However, serialization preserves what the importer supplies. An opaque original decision JSON record is not a `Decision`; an authority reference in an excerpt is not a usable `GraphEntity`/authority predicate. In the inspected full-import path, the operational model comes from repository fixture `M_P05.json`, whose hash is in `N_P06.json`, not from a complete reconstruction of the manifest's execution and contract semantics. This dependency is explicit and pinned, not hidden in-memory state. The original ledger is retained as historical source assertions; only new planner events are replayed by the native ledger engine.

The implementation can read the frozen manifest with the checked-in normalization and reproduce its suspended wait report. That narrow capability differs from independently restoring every state element needed for correct future planning. For that stronger user-requested readiness, **REAL_E1_COLD_RESUME_READY = NO**, pending F03 and the other relevant corrections. This review did not call real E1 restore, acquire evidence or resume the experiment.

The current suite's identical-byte subprocess comparisons are valid mechanical evidence. They do not validate an omitted contract, and ordinary source hash matching does not turn historical source statements into present applicability. No wall-clock dependency or random ActionId generation was found. Temporary filename randomness in immutable persistence does not enter canonical output. F05 is an actual same-canonical-state/different-computation counterexample independent of hash seeds.

## Security and trust boundaries

| Input | Classification | Enforced boundary / residual assumption |
|---|---|---|
| JSON syntax, enum tags and primitive types | VALIDATED | Duplicate keys, floats, unknown tags and mismatched dataclass fields rejected |
| Raw artifacts / embedded manifest values | TRUSTED_BY_IDENTITY | Raw and domain-specific hashes verified; content identity is not authority |
| Reviewed initial fixtures and normalization choices | ASSUMED | Source bytes/locations validated; acceptance of the authored semantic mapping is external to the engine |
| Typed graph assertions | VALIDATED structurally, ASSUMED accepted semantics | Tags/IDs/evidence dependencies checked; F01/F04 expose incomplete structural enforcement |
| Opaque frozen graph records | TRUSTED_BY_IDENTITY | Preserved source records, not operational graph truth; F03 |
| Authority entities / accepted decision records | ASSUMED admission; VALIDATED use | Context, target, permission class, consumption and dossier/choice bindings checked after admission |
| Receipt bytes | UNTRUSTED until VALIDATED | Canonical body, independent attestor, producer competence, scope/currentness and obligation coverage checked |
| Synthetic trust roots | ASSUMED, explicitly synthetic | Useful negative/positive controls, not actual E1 evidence |
| Supplied action results/events | UNTRUSTED until VALIDATED | Selected-action/prestate/inventory/transition checks; no arbitrary root setters |
| Policy pin/version | TRUSTED_BY_IDENTITY plus ASSUMED correspondence | Fixed implementation executes the policy; F06 permits unrelated bytes to be labeled policy |
| Persisted ledger | VALIDATED integrity and replay | Hash/parent/sequence/event-file checks; initial-state admissibility remains the fixture trust boundary |
| Evaluation scope/generation/tick | ASSUMED admitted context, then VALIDATED comparisons | Deterministic supplied data, not an external currentness oracle |

O01 — OBSERVATION: The plan explicitly allows pinned historical acceptance contracts and synthetic trust roots. Therefore the absence of online signatures or a live authority service is not itself a defect in v0.1. A self-consistent hash is nevertheless not external authorization; consumers must not treat arbitrary user-authored initial snapshots as governed accepted state. Fixture source-excerpt checks establish location/content consistency, not semantic entailment of every normalized field.

O02 — OBSERVATION: Global control is defined over **declared goals**, not every object stored in a partial snapshot. Consequently an undeclared unresolved root can coexist with terminal goal success. This is consistent with plan section 7 and is not counted as a fail-open finding. Callers must establish complete required-goal coverage before interpreting the output as whole-run readiness; a no-goals partial fixture does not receive one of the seven global states.

O03 — OBSERVATION: The implementation has useful explicit guardrails: strict typed parsing, exact identity-domain comparisons, pure consumer rejection, separate knowledge/condition transitions, independent receipt attestation checks and no effect executor. No GraphRAG, LLM semantic extraction, external service, generalized optimizer, production database, UI or autonomous evidence retrieval dependency was found. These positives do not neutralize F01–F04.

## Reproduction notes

The probes were ephemeral scripts in `/tmp`; no repository tests were added or changed. The following minimal construction reproduces F01 using existing typed APIs and independently pinned fixture sources:

```python
from adapter.planner import model as m, core, codec
from adapter.tests.test_planner_e1_replay import fixture, p05_fixture
E, _ = fixture('E')
K, _ = p05_fixture('K')
proof_source, ordering_source = E.actions[0].source, K.actions[0].source
known = m.KnowledgeRecord(m.KnowledgeId('proof'), m.KnowledgeState.KNOWN_COMPLETE,
                          'accepted independent proof', proof_source)
predicate = m.Predicate(m.PredicateId('proof'), m.PredicateKind.KNOWLEDGE_ACCEPTED,
                        knowledge=known.id)
child = m.RootCondition(m.ConditionId('child'), m.ConditionState.UNRESOLVED,
                        predicate=predicate.id)
parent = m.RootCondition(m.ConditionId('parent'), m.ConditionState.UNRESOLVED)
edge = m.GraphAssertion(m.AssertionId('order'), ordering_source,
    relation=m.Relation.REQUIRES, subject=child.id, object=parent.id,
    ordering_justification='explicit prerequisite')
s = m.Snapshot((), (), (child, parent), (), (known,),
               assertions=(edge,), predicates=(predicate,))
assert core.evaluate_satisfaction(s).roots[0].state is m.ConditionState.UNRESOLVED
stale = codec.invalidate_sources(s, (ordering_source.identity,))
assert core.evaluate_satisfaction(stale).roots[0].state is m.ConditionState.SATISFIED
```

For F02, use the existing synthetic receipt helper only to construct initial independently admitted bytes/trust; the oracle is external: after invalidating that trust, no resume permission is justified. Apply REQUEST_READY, WAITING, RECEIVED, VALIDATED, REENTRY in order to K, invalidate TEST-TRUST's provenance identity, and compare `gates.external_complete` with `replay.plan_output(p05_bundle(stale))['resume_allowed']`. They are false and true respectively.

For F04, add `Predicate(PredicateId('x'), SOURCE_IDENTITY, entity=EntityId('absent'))` to a valid state and round-trip with `decode_snapshot(snapshot_bytes(...))`: it is accepted. For F05, create a satisfied root and resolved slot both spelled `same`, give each a goal, reverse the goals and compare canonical bytes versus `recompute(...).branches`. For F06, replace B's policy pin in a temporary fixture with its existing construction-authority pin and invoke `import_fixture`; import succeeds. All mutations are isolated and require no E1 write or external operation.

## Final review report

```text
VERDICT = QUALIFICATION_REQUIRES_CORRECTION
CRITICAL_FINDINGS = 0
MAJOR_FINDINGS = 4
MINOR_FINDINGS = 2
OBSERVATIONS = 3
REPLAY_STRENGTH = {A:STRONG, B:ADEQUATE, C:STRONG, D:STRONG,
 E:STRONG, F:ADEQUATE, G:ADEQUATE, H:ADEQUATE, I:STRONG,
 J:STRONG, K:STRONG, L:STRONG, M:WEAK, N:WEAK}
HIDDEN_NONDETERMINISM_FOUND = YES
HIDDEN_STATE_FOUND = NO
FAIL_OPEN_PATH_FOUND = YES
REAL_E1_COLD_RESUME_READY = NO
E1_ARTIFACTS_MODIFIED = 0
IMPLEMENTATION_MODIFIED = NO
PRODUCTION_EFFECT = NO
```

The original qualification artifacts remain unchanged as historical records. The present verdict concerns their sufficiency, not a silent rewrite of them. No correction is authorized or implemented by this report.
