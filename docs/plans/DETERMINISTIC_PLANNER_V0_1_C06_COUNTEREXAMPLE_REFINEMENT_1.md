# C06 / F03 counterexample refinement 1

## Finding and scope

**F03 classification: A — STRUCTURAL_GAP_WITH_PROVEN_OPERATIONAL_EFFECT.** An isolated executable candidate exposes incorrect actionability and selection after invalidation of an explicitly required accepted-knowledge source. No implementation repair was made. F03 remains open; this does not close the rest of C06's restoration inventory.

The [adversarial review](DETERMINISTIC_PLANNER_V0_1_ADVERSARIAL_REVIEW.md), [correction plan, C06 and section 6](DETERMINISTIC_PLANNER_V0_1_CORRECTION_PLAN_1.md), [matrix, T03/T-IMPORT](DETERMINISTIC_PLANNER_V0_1_CORRECTION_MATRIX_1.md), and [previous C06 attempt](DETERMINISTIC_PLANNER_V0_1_C06_RESULT.md) distinguish two things:

- **STRUCTURAL_OMISSION:** the full import uses the M normalization with 63 actions, no Decision/GraphEntity objects, no typed action requirement/authority predicates, and PASS outcome labels. Opaque source records and correctly hashed source pins do not restore their operational relationships.
- **OBSERVABLE_OPERATIONAL_FAILURE:** after isolated receipt/reentry, invalidating the exact source of a mandatory accepted non-PASS knowledge prerequisite does not remove the dependent action from ACTIONABLE or selection. The planner continues to report RUNNABLE solely on that action. Canonical snapshot reload preserves this incorrect behavior.

The previous empty-PASS regression was inadequate: `gates.validate_result` already rejects an empty accepted inventory with `no accepted bounded result contract`. The default PASS label does not bypass that guard. The refined counterexample does not submit an action result and does not depend on defeating this existing safeguard.

## Independent authoritative oracle

The frozen [resolution plan](../experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_PLAN_1.json), raw SHA-256 `2662971aa42bda300dcea7bf591e95c113b4ed5cb32db1381cd25b024c06e91c`, contains the following obligation at:

`/resolution_actions/62/knowledge_requirements/0`

The candidate finds the row by canonical ActionId, not array position:

```text
Action: FACT-BUDGET-APPLICABILITY
Required producer action: REEVAL-BUDGET
Required recorded outcome: BLOCKED
Requirement: Consume accepted missing-proof outcome;
             success of historical reevaluation is not required.
Evidence: docs/experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_REEVAL_BUDGET_1_RESULT.md
Raw SHA-256: 8692f4214410724921e0b1c346b2dfc37c2ae95d0bf2d8cad71949972a130b59
```

The [budget reentry specification](../experiments/E1/E1_BUDGET_APPLICABILITY_REENTRY_1.md), “Actionability,” confirms that accepted decision/blocked-result prerequisites support beginning this action. Correction-plan section 6 explicitly requires restoring `knowledge_requirements` as current-proof dependencies without converting accepted BLOCKED knowledge into successful action completion; T-IMPORT explicitly includes non-PASS accepted knowledge prerequisites and stale-source controls.

The required contract is therefore: accepted knowledge of the missing-proof outcome, derived from the exact owning result artifact, must remain qualified before the dependent action becomes or remains actionable. Invalidating that source must withdraw its current proof support. Historical BLOCKED status/attempt evidence remains historical; it is not rewritten to PASS or erased. The new external receipt addresses separate proof obligations and has no rule superseding this source dependency.

## Real implementation path

| Boundary | Actual implementation | Missing operational effect |
|---|---|---|
| Input/import | `replay.import_e1`, `replay.py:354–356`, loads the pinned M_P05 normalization through `load_p05_fixture` | The action's source prose includes the requirement, but its typed `requirements` tuple omits it. |
| Coverage check | `replay.py:376–379` compares action/root/slot ID sets | ID coverage does not check required accepted-knowledge edges. |
| Source retention | `replay.py:380–405` appends opaque assertions and constructs the source-pinned bundle | The required result artifact is a verified bundle source, but not an operative accepted KnowledgeRecord/predicate dependency of this action. |
| Receipt/reentry | `core.apply_receipt`, `core.py:488–496` | The complete synthetic receipt releases the external gate and makes the named action ACTION_ELIGIBLE, then recomputes normal gates. This is not supposed to waive original prerequisites. |
| Source invalidation | `codec.invalidate_sources`, `codec.py:271–340` | Existing propagation follows typed provenance, evidence and predicate links. The missing imported link cannot propagate staleness to this action. |
| Actionability | `core._actionability`, `core.py:191–207`; `gates.blockers`, `gates.py:98–112` | Existing current-completion gates and present predicates are checked; the missing knowledge predicate is never checked. |
| Selection/control | `core.recompute` and `_global_control` | The one actionable machine action is selected; selection yields RUNNABLE. |
| Snapshot restoration | `codec.snapshot_bytes` → `decode_snapshot` → `core.recompute` | Serialization preserves the omission; it cannot reconstruct the missing relationship from source text. |

These paths use the unchanged implementation. No gate, importer, evaluator, selector or codec is mocked. C02's invalidation mechanism is not shown to be broken for represented dependencies; the candidate includes a control invalidating the represented action-definition source. The correction belongs at operational contract import/representation, not a new exception in the selector.

## Executable invariant and minimal mutation

**GIVEN** the actual frozen manifest has been imported into isolated replay state, and the existing case-N synthetic trust/receipt setup has passed all receipt/reentry validations, with FACT-BUDGET-APPLICABILITY selected by the current implementation;

**WHEN** the exact content identity of the independently declared REEVAL-BUDGET accepted-knowledge source is invalidated through the real invalidation API, followed by canonical snapshot serialization/reload and recomputation;

**THEN** FACT-BUDGET-APPLICABILITY must be absent from ACTIONABLE and must not be selected while that mandatory support is unqualified;

**AND MUST NOT** treat a historical status, opaque source text, bundle source-pin membership, or the independent external receipt as replacement accepted knowledge. No root/slot is resolved and no historical attempt is rewritten.

Only the invalidation input differs from the baseline. The test uses the complete imported state to preserve the real importer path; it is a minimal causal mutation, not a claim of globally minimal graph size. The baseline is known-valid under the existing implementation's validators and case-N setup—not claimed to satisfy every source-level contract that F03 says was omitted.

All receipt evidence is explicitly COUNTERFACTUAL_SYNTHETIC. The test does not obtain real evidence, alter frozen files, execute the selected action, issue authority, or resume E1.

## Isolated candidate and observed failure

Candidate: [c06_f03_candidate.py](../../adapter/tests/counterexamples/c06_f03_candidate.py).

It is intentionally outside the default `test*.py` discovery pattern. Run explicitly:

```sh
python3 -m unittest adapter.tests.counterexamples.c06_f03_candidate -v
```

The candidate reads the source requirement independently from the pinned plan, verifies the result artifact's actual raw hash and bundle pin membership, and uses the existing synthetic receipt helper only to discharge the separate external gate. The expected rejection comes from the source contract, not from the importer or normalization's expected output fields.

Observed after the one-source invalidation and snapshot round trip:

```json
{
  "actionable": ["FACT-BUDGET-APPLICABILITY"],
  "selected": "FACT-BUDGET-APPLICABILITY",
  "control": "RUNNABLE",
  "same_snapshot_identity": true
}
```

The candidate's `assertNotIn` fails because the action is still actionable. The unchanged snapshot identity further localizes the loss: this required source's invalidation has no operational state effect at all.

The first run had one expected failure and two passing controls. The final candidate run executed four tests in 89.348 seconds: **one intentional failing regression and three passing controls**, exit status 1. The failure is `AssertionError: ActionId(value='FACT-BUDGET-APPLICABILITY') unexpectedly found in (ActionId(value='FACT-BUDGET-APPLICABILITY'),)`.

Controls cover:

1. The baseline receipt setup selects the target, while its empty PASS is still rejected by the existing result-contract guard.
2. Invalidation of an unrelated content identity leaves the baseline computation unchanged; the desired repair is not blanket blocking on any invalidation.
3. Invalidation of the represented action-definition source does block the action, distinguishing missing imported support from failure of the existing represented-source invalidation path.

This proves an actionability/selection defect in isolated replay. It does **not** prove that changing actual pinned source bytes bypasses source-aware bundle restore; existing raw-pin checks remain separate. It does not assert that real E1 can resume, that `resume_eligibility` returns true, or that an effect/action result is accepted. The revised regression needs none of those broader claims.

## Minimum C06 repair contract — not implemented

The exact counterexample needs the importer to restore the declared accepted non-PASS knowledge dependency, with authenticated producer/outcome/source provenance, into the existing predicate and invalidation graph:

1. Compile the plan's `knowledge_requirements` through a versioned, pinned, reviewed mapping. Match the producer action, expected recorded result, exact artifact identity/location, scope and accepted current overlay. Do not parse arbitrary prose as executable rules.
2. Restore the accepted knowledge of the bounded missing-proof outcome separately from the producer's historical BLOCKED action state. `KNOWN_COMPLETE` for that bounded historical observation must not mean budget applicability is complete or that the producer passed.
3. Attach a `KNOWLEDGE_ACCEPTED` requirement (or bounded additive contract type if the existing type cannot retain the producer/outcome binding) to the dependent action. Connect its provenance/evidence to the exact result source so existing invalidation makes its support unavailable.
4. Missing, stale, mismatched or unqualified support must block actionability after external reentry as well as before it. Do not add an `ACTION_COMPLETED(REEVAL-BUDGET)` substitute: that would incorrectly require a historical BLOCKED action to have succeeded.
5. Persist/reload this contract and provenance canonically. Verify the isolated positive case with authentic qualified prerequisite knowledge still selects the action. Keep the existing empty-result rejection until C06 independently restores the actual bounded output contract.

Likely files/functions: `replay.py:import_e1` and the reviewed versioned import mapping; `model.py` only for absent bounded historical-attempt/result binding; `codec.py` for any additive persisted type and source/provenance inventory. Existing `gates.blockers`, `evaluate_predicate(KNOWLEDGE_ACCEPTED)`, `core.recompute` and `invalidate_sources` should enforce the restored dependency; strengthen those only if a demonstrated integration gap remains. Do not add a parallel invalidator/state model or ActionId-specific special case.

This local repair would make the refined counterexample pass. It is **necessary but not sufficient for all C06 acceptance**. The full contract-coverage inventory, decisions/dossiers, authority semantics, bounded positive result acceptance, other source/slot/root contracts and actual-manifest readiness obligations remain required by the unchanged correction plan. This refinement neither narrows F03 to one edge nor authorizes C07.

### Nearby variants for the repair

- Required accepted outcome remains BLOCKED/AUTHORITY_REQUIRED while its bounded knowledge is qualified: positive actionability, no fabricated producer COMPLETED state.
- Source missing, same digest in a wrong identity domain, wrong producing action/outcome, stale qualification, or conflicting history/current overlay: reject or hold before use.
- Invalidation before receipt, after receipt, after reentry, and through a persisted `SourceInvalidation` event: original requirement remains enforced; the gate alone never waives it.
- Required and unrelated source changes together; independent supported branches still run.
- Accepted replacement/requalification bound to its new source and permitted overlay restores only the affected route; no automatic retry from unrelated information.
- Alpha-renamed actions/knowledge/source paths with unchanged supported contract semantics; no special-case dependence on the E1 identifier spelling.
- Canonical round trip, source/action/assertion permutations, reversed JSON keys, fresh-process/hash-seed replay: identical actionable/selected/control outputs and canonical semantic identity; causal histories are not reordered.
- Positive complete supplied proof-matrix result versus missing/partial output after reentry: still a separate C06 result-contract test, not satisfied by this refinement.

Affected replay coverage: directly M/full N, with J–L receipt/reentry, E knowledge-versus-completion and F–I decision-knowledge regressions; retain A–D as specified by C06. Direct invariants are X10 (source staleness), X01 (historical/current distinction), X07 (knowledge/PASS versus satisfaction) and X08 (missing proof is not evidence); retain X02/X03/X04/X05/X06/X09/X11 and C01–C05 under C06's full regression requirement. These are proposed repair checks, not new PASS claims from this refinement.

## Preservation and report

All 10,911 frozen E1 files retain their pre-task path/raw-SHA identities (inventory commitment `1cf25145f69a2fb133c12f3b15cd1089351e4a9cac8624d4b6e970f2b4b3a044`). Implementation, existing tests/fixtures, backlog, plans/matrices, prior C06 result and historical/current qualification records remain unchanged. Only this report and the isolated candidate file were added. Generated caches outside E1 are excluded from the source-change comparison. `git diff --check`, added-file whitespace checks and document-link checks pass. No repair, C07, real E1 resumption or full requalification was performed.

```text
F03_STRUCTURAL_OMISSION = REPRODUCED
F03_REQUIRED_OPERATIONAL_CONTRACT = source-bound accepted non-PASS knowledge must gate dependent actionability and survive invalidation/reload
ORIGINAL_REGRESSION_WAS_INADEQUATE = YES
COUNTEREXAMPLE = required REEVAL-BUDGET result source invalidated; FACT-BUDGET-APPLICABILITY remains actionable/selected
PRE_REPAIR_COUNTEREXAMPLE = REPRODUCED
PRE_REPAIR_REGRESSION = FAIL_EXPECTED
F03_CLASSIFICATION = A. STRUCTURAL_GAP_WITH_PROVEN_OPERATIONAL_EFFECT
C06_REPAIR_READY = YES (pre-repair counterexample established; full C06 scope unchanged)
PROPOSED_REPAIR = restore typed producer/outcome/source-bound accepted-knowledge prerequisite and its provenance dependency
PROPOSED_REGRESSION = adapter/tests/counterexamples/c06_f03_candidate.py
NEARBY_VARIANTS = [non-PASS positive knowledge, missing/stale/wrong-domain source, conflicting overlay, pre/post-reentry invalidation, unrelated-source control, authorized requalification, alpha-renaming, cold/permuted replay, separate bounded-result acceptance]
F03_STATUS = OPEN
V0_1_CURRENT_STATUS = CORRECTION_REQUIRED
IMPLEMENTATION_MODIFIED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
```
