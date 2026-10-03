# N-REAL release requirement reconciliation 1

**Primary conclusion: E — an explicit qualification/release-scope decision is required to change N-REAL.** Under the current requirements, E2 **complements** N-REAL (C). It plans to cover substantial portable lifecycle assurance, but not actual frozen-E1 reconstruction. It neither satisfies N-REAL literally (A) nor establishes equivalence to its entire assurance objective (B). No requirement or release authority is changed here.

**E2 should proceed in parallel with reconciliation**, beginning with its own P01 contract preflight when separately executed. It has independent qualification value. This recommendation does not execute any package or permit requalification while the current N-REAL gate remains unmet.

The [machine-readable obligation/coverage matrix](DETERMINISTIC_PLANNER_V0_1_N_REAL_RECONCILIATION_1.json) preserves the exact original requirement and gate text, all 36 literal references found in the bounded repository search, 12 atomic obligations, case mappings, residuals, four alternatives and separate readiness gates.

## Exact requirement and origin

The first named N-REAL definition in the inspected authoritative chain is [Correction Plan 1 §8](DETERMINISTIC_PLANNER_V0_1_CORRECTION_PLAN_1.md:229), “Actual frozen-manifest readiness test (N-REAL).” Its opening scope states:

> This is a **future C06/C07 non-effecting validation test**, not executed by this planning task. It does not release suspension or run any selected action.

The exact first step is:

> Start a new Python process with an empty temporary output directory and no prior planner objects. Inputs are the actual frozen `docs/experiments/E1/E1_RESUME_MANIFEST_1.json`, its checkpoint, pinned referenced sources, supported policy and reviewed mapping version. Do not supply the M replay snapshot as initial state.

The companion reproduces all nine steps and §9 verbatim, with the source SHA-256. The remaining acceptance criteria are summarized here without changing their force:

1. Verify raw/embedded identity domains, checkpoint, ledger/state/policy/authority/proof bindings; never repin a mismatch or upgrade historical currentness.
2. Import the complete §6 operational inventory; enforce C01/C02; reject missing required semantics explicitly.
3. Independently recompute root/slot qualification, readiness, actionability, selection, holds, frontier, control and C03 resume proof.
4. Compare to the separately read real manifest/handoff/checkpoint oracle: MIXED_WAIT, empty machine/human-ready sets, no receipt, 27 unresolved roots, 41 unresolved slots, Candidate-3 VALID_UNCONSUMED. These are not computation inputs.
5. Persist the newly reconstructed bundle, terminate and cold-restore in another process; compare complete semantic state and identities.
6. In separate synthetic copies, qualify supported renamed continuation, legitimate receipt/reentry, bounded results and decision/dossier enforcement under the restored contracts.
7. Reject mutations of targets, required goals/contracts, overlays, policy, stale ordering, receipts and source bytes.
8. Preserve all 10,911 E1 paths/hashes; no authority consumption, requests, runtime acquisition, E1 action, implementation effect or construction.

The [correction matrix N-REAL row](DETERMINISTIC_PLANNER_V0_1_CORRECTION_MATRIX_1.md:43) independently states actual frozen inputs, fresh process, no M snapshot, complete typed computation and semantic cold restoration. Its C06/C07 dependency and final checklist retain that obligation.

The release effect is explicit in [Correction Plan §9](DETERMINISTIC_PLANNER_V0_1_CORRECTION_PLAN_1.md:245): the requirements are conjunctive, and actual frozen-E1 import/validation must pass alongside baseline regressions, corrections, determinism, persistence and independent review. The original QUALIFIED record is historical, not authority to bypass this gate.

The literal-reference census covers `N-REAL` and `N_REAL` in `docs/plans` and `docs/backlog` before these outputs were created. It found 36 occurrences, including machine-readable mirrors and later references; that is not 36 independent requirements. Semantic predecessors without that spelling were separately examined. The corpus boundary is stated rather than claiming to discover undocumented authority elsewhere.

## Requirement history and rationale

| Stage | Evidence and effect |
|---|---|
| Original implementation/acceptance | [P06](DETERMINISTIC_PLANNER_V0_1_IMPLEMENTATION_PLAN.md:265) calls for full E1 import, cold restore, CLI and isolated reentry. [Acceptance N](DETERMINISTIC_PLANNER_V0_1_ACCEPTANCE_MATRIX.md:195) already requires exact frozen inputs and separately synthetic continuation. N-REAL makes the stronger mechanism explicit; the real-input objective was not invented after migration became difficult. |
| Original qualification | [Qualification](DETERMINISTIC_PLANNER_V0_1_QUALIFICATION.md) records the then-passing suite. It does not override later discovered coverage defects. |
| Adversarial review/F03 | [Review, cold-resume analysis](DETERMINISTIC_PLANNER_V0_1_ADVERSARIAL_REVIEW.md:178) identifies reduced M normalization plus opaque original records. Serialization preserved omissions. Real action/decision/authority/result semantics were not completely reconstructed. This is the documented risk motivating stronger coverage. |
| Correction plan/matrix | C06 supplies operational restoration; C07 owns integrated N-REAL/requalification and fresh review. The requirement explicitly prohibits the reduced M fixture as the real test's initial state. |
| Refined C06 and C06A reconciliation | Refined F03 was closed, but [C06A retry](DETERMINISTIC_PLANNER_V0_1_C06A_RETRY_1_RESULT.md) and [C06/C07 reconciliation](DETERMINISTIC_PLANNER_V0_1_C06_C07_RECONCILIATION_1.md) retain full-import/field-coverage and N-REAL obligations. Narrow finding closure is not broad capability qualification. |
| Legacy boundary and bridge findings | Versioned migration was adopted; source/profile, Action and role analyses found missing authoritative semantic mappings. These findings explain why reconstruction is blocked, not why actual-source assurance has already been supplied. |
| Governed-unknown defect | The native control defect was separately reproduced and repaired. Its correction enables valid governed waiting but supplies neither absent positive proof nor legacy source-to-contract bindings. |
| Disposition and E2 | The [legacy disposition](DETERMINISTIC_PLANNER_V0_1_E1_LEGACY_BRANCH_DISPOSITION_1.md) defers migration while preserving the explicit release gate. [E2](DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_EXPERIMENT_1.md) is canonical and unexecuted; it deliberately does not ingest E1. |

The record establishes this artifact/dependency sequence; no unsupported date or commit chronology is assigned. Explicit rationale is omitted-contract detection and meaningful source-driven cold restoration. The broader interpretation “avoid fixture overfitting” is an inference supported by the no-M-input and renamed-continuation requirements, not a replacement statement of the requirement.

## Mechanism versus assurance

Mechanism: actual frozen manifest/checkpoint/source closure → reviewed full operational import → independent computation → real frozen oracle comparison → fresh-process semantic restoration, plus separate synthetic continuation and mutations.

Assurance properties: REAL_ARTIFACT_INGESTION, REAL_OPERATIONAL_STATE_RECONSTRUCTION, REAL_E1_COLD_RESUME, FULL_CONTRACT_RESTORATION, REAL_SOURCE_PROVENANCE, REAL_ACTIONABILITY, deterministic native continuation under restored contracts, source/authority preservation and resistance to fixture-specific shortcuts.

“Real E1” is therefore both the chosen vehicle **and an explicitly required compatibility/correspondence scope**. The mechanism exercises source-to-native semantics that a directly authored canonical fixture omits. It does not prove generic ingestion of every possible historical format. Conversely, N-REAL forbids actual E1 runtime execution: its end-to-end positive continuation is synthetic. It cannot be expanded into a live-production assurance requirement.

## Atomic coverage matrix

Coverage below is **planned E2 capability**, not passed tests. All E2 packages are unexecuted. FULLY_COVERED means the planned obligation matches, not that it has been discharged. The companion supplies required input, operation, output, invariant and why real input matters for every row.

| Obligation | Property / original clause | E2 mapping | Classification | Preserved E1 support and limit |
|---|---|---|---|---|
| NR01 | Actual source-driven fresh import; §8.1 | A01, END | NOT_COVERED | Pinned source inventory exists; E2 starts from canonical definitions |
| NR02 | Complete real identity/provenance/context closure; §8.2 | A01, N03/N05/N10 | PARTIALLY_COVERED | Real pins and 54 shared bindings verified; complete reached native correspondence missing |
| NR03 | Complete operational contract restoration; §8.3 | A01/A04/A05 | COVERED_ONLY_SYNTHETICALLY | 819-field inventory identifies 186 gaps and eight incomplete families; no complete migrated universe |
| NR04 | Admission/invalidation enforcement on restored state; §8.3 | A15, N07/N08/N09, REG | COVERED_ONLY_SYNTHETICALLY | Closed native corrections retained; full real-restored state not exercised |
| NR05 | Real actionability/control/reentry computation; §8.4 | A02/A06/A11/A13/A14 | COVERED_ONLY_SYNTHETICALLY | Real histories/frontier and bounded replay exist; full recomputation absent |
| NR06 | Independent frozen-oracle agreement; §8.5 | END, A08 | NOT_COVERED | Real suspension oracle preserved; E2's independent oracle describes a different experiment |
| NR07 | Full real-derived canonical cold resume; §8.6 | A07/A08/D01 | COVERED_ONLY_SYNTHETICALLY | Native and reduced-N cold tests retained; no complete E1-derived bundle |
| NR08 | Renamed supported continuation/results/decisions; §8.7 | A09–A13, N14/N15 | PARTIALLY_COVERED | Bounded receipt/decision/budget tests exist; real restored-contract correspondence unproved |
| NR09 | Full-import mutation rejection; §8.8 | N01–N05, N07–N11, N14, REG | PARTIALLY_COVERED | Existing negatives retained; real-import composition suite absent; explicit omitted-goal/conflicting-overlay E2 cases also need traceability |
| NR10 | Real corpus preservation; §8.9 | REG, END | FULLY_COVERED | Repeated 10,911-file checks, including this review; repeat around future executed qualification |
| NR11 | No real resume, request or authority effect; §8.9 | END, REG | FULLY_COVERED | Frozen Candidate-3 and suspension records preserved; future-run isolation still must be checked |
| NR12 | Determinism/no hidden state; §9 and original N | D01, A08, REG | PARTIALLY_COVERED | Native determinism evidence retained; full real importer ordering/process coverage missing |

Totals: 2 FULLY_COVERED, 4 PARTIALLY_COVERED, 4 COVERED_ONLY_SYNTHETICALLY, 2 NOT_COVERED, 0 NOT_APPLICABLE. No original N-REAL obligation is declared inapplicable by this review.

Preserved authority records, graph, actionability/selection history, external handoff and checkpoint authenticate historical claims and expected outcomes. They are valuable oracles and source premises. They are not evidence that a complete canonical reconstruction executed. Prior A–N replay and adversarial findings are retained with their original scope; none is silently relabeled N-REAL PASS.

## Residual assurance gap

Two residuals must be kept separate:

- **Current execution residual:** N-REAL has no accepted complete run, and E2 has no run. No one may subtract a planned E2 case as passed evidence. Existing partial/preservation evidence remains credited within scope.
- **Projected structural residual, assuming E2 passes as planned:** NR01–NR09 and NR12 still lack their required real-import/correspondence portions. NR10/NR11 can be satisfied by E2's actual preservation/isolation checks, but must be repeated around whichever future real-import test is claimed.

The projected residual groups are:

1. Real-source recognition, typed identity/provenance/context correspondence and complete reached inventory (NR01/NR02).
2. Authoritative complete Action/decision/authority/proof/history/route contracts and their source-to-native construction (NR03).
3. Real-state enforcement, independently derived suspended conclusions and comparison with the actual frozen oracle (NR04–NR06).
4. Cold equality of that real-derived state, including all operational contract members (NR07).
5. Supported continuation, decision/result and mutation behavior demonstrably attached to those restored contracts rather than unrelated canonical fixtures (NR08/NR09).
6. Full-source import determinism across processes/orderings (NR12).

These gaps are not erased by immutable archived bytes plus a passing unrelated runtime lifecycle. Combining two pieces of evidence requires proof of their semantic correspondence; that correspondence is precisely where legacy reconstruction is incomplete.

## Four unselected release alternatives

| Alternative | Assurance comparison | What remains / what would be lost |
|---|---|---|
| KEEP_UNCHANGED | PRESERVES_ASSURANCE | E2 adds independent value; existing release stays blocked until full N-REAL succeeds. No obligation lost. |
| DECOMPOSE | PRESERVES_ASSURANCE and CHANGES_ASSURANCE_MECHANISM **only if the whole conjunction is retained** | Allocate portable native lifecycle checks to E2 and retain real-source recognition/coverage/oracle/cold/mutation correspondence in a separate lane. Explicit coupling evidence required. This does not unblock release now. Archive-only checks cannot replace the real execution lane. |
| REPLACE_WITH_E2 | REDUCES_ASSURANCE relative to the original claim | Current E2 loses NR01, the real portions of NR02–NR09 and full-import NR12. It is not an equivalent replacement. Describing it as such would be false; a deliberately narrower release claim would instead require explicit scope authority. |
| TWO_TIER | CHANGES_ASSURANCE_MECHANISM; narrower first-tier claim, not equivalent broad qualification | Proposed canonical-runtime and E1-legacy-compatibility evidence statuses remain separate. Original broad claim requires both; a canonical-only release must explicitly exclude legacy compatibility. No property is lost if the second tier remains visible and unqualified rather than being silently waived. |

No alternative is selected. E2 can increase evidence depth for canonical continuation, but added synthetic depth does not compensate for lost real-source scope. The proposed two-tier labels are scoped reporting concepts, not existing aliases for the repository's QUALIFIED status.

## Authority, decision readiness and E2 consequence

**RECONCILIATION_AUTHORITY_REQUIRED = QUALIFICATION_AUTHORITY_DECISION.** The governing requirement/release owner must explicitly approve any changed claim, coverage allocation, residual disclosure and status terminology. Architectural input can explain semantic consequences; it cannot by itself issue release acceptance. The inspected repository specifies the correction/review/status gate, not a named individual's delegated release authority. This report invents no such delegation.

Keeping the requirement requires no authority change. Passing it requires additional evidence. A decomposition or scope change is not merely deterministic renaming because it changes what a release claim means or how evidence is accepted.

**N_REAL_DECISION_READY = YES for this bounded release-scope choice.** The original text, missing assurance and consequences of all four alternatives are exposed. Replacement equivalence is not established and is not offered as a valid equivalent option. A future selected decomposition/tier would still need a precise issued gate and acceptance allocation before use. Decision readiness does not mean implementation or qualification readiness.

**E2_EXECUTION_RECOMMENDATION = PROCEED_IN_PARALLEL.** Its canonical validation, lifecycle, cold persistence and receipt/reentry tests provide value under every alternative. Only E2-P01 is the first eligible planned operation; it must settle its own evidence-ingestion and source-index/event preflight interfaces. No package runs here, and N-REAL remains active meanwhile.

## Separate gates

These predicates distinguish evidence statuses; they do not establish new release authority:

```text
CANONICAL_E2_QUALIFIED =
  E2-P01..P05 accepted against pinned contracts and independent oracles
  AND E2-P06 fresh review accepted
  AND no open required canonical defect
  AND preservation/scope/source/code/policy evidence complete

N_REAL_SATISFIED =
  accepted execution evidence for NR01..NR12
  under original actual-source, full-coverage and no-effect constraints

LEGACY_E1_COMPATIBILITY =
  reviewed complete legacy migration contracts
  AND actual E1 canonical construction/native admission
  AND N_REAL_SATISFIED

PLANNER_V0_1_REQUALIFICATION_READY (current unrevised gate) =
  prior findings remain closed
  AND baseline regressions pass
  AND E2 lifecycle/cold/reentry/continuation/determinism pass
  AND no deferred-scope violation
  AND fresh independent review ready
  AND N_REAL_SATISFIED
```

Review-ready is distinct from review-accepted: final QUALIFIED additionally requires accepted independent review, no open required findings and the governing append-only qualification/status approval. No alternate branch is activated unless a separate explicit reconciliation is issued. C07 ownership of integrated requalification remains unchanged.

```text
N_REAL_EXACT_REQUIREMENT = Correction Plan 1 §8 nine steps; §9 conjunctive release gate
N_REAL_ASSURANCE_PROPERTY = [real ingestion, full operational restoration,
 real provenance/actionability/oracle correspondence, real cold resume,
 supported continuation, mutation resistance, determinism, preservation/no-effects]
N_REAL_ATOMIC_OBLIGATIONS = [NR01,NR02,NR03,NR04,NR05,NR06,NR07,NR08,NR09,NR10,NR11,NR12]
N_REAL_RESIDUAL_GAP = [NR01-NR09 and NR12 real-source/correspondence portions;
 all unexecuted required checks remain pending]
ALTERNATIVES = [KEEP_UNCHANGED,DECOMPOSE,REPLACE_WITH_E2,TWO_TIER]
RECONCILIATION_AUTHORITY_REQUIRED = QUALIFICATION_AUTHORITY_DECISION
N_REAL_DECISION_READY = YES
E2_EXECUTION_RECOMMENDATION = PROCEED_IN_PARALLEL
CANONICAL_E2_QUALIFIED = NO
N_REAL_SATISFIED = NO
LEGACY_E1_COMPATIBILITY = NOT_QUALIFIED_DEFERRED
PLANNER_V0_1_REQUALIFICATION_READY = NO
IMPLEMENTATION_MODIFIED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
```

Preservation checks cover all 10,911 frozen E1 paths/content hashes and the prior implementation/planning/backlog baseline. Reference pins, obligation/case identifiers, JSON and `git diff --check` are validated. No experiment, release decision, migration or runtime test was executed.
