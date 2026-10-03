# E2-P02 Human-Handoff Boundary Reconciliation

## Finding

The original E2 plan explicitly assigns P02 the lifecycle “canonical
construction, initial selection/results, dossier/decision and external wait”
and names `EXTERNAL_WAIT` as its target. The acceptance matrix also assigns
E2-A05 (synthetic bounded decision/grant) and E2-A06 (external request and
absence) to that pre-external sequence. P02 is therefore not authorized to
terminate successfully at `HUMAN_HANDOFF`.

The plan anticipated a human boundary: `E2-DECIDE` is an
`ARCHITECT_CONTRACT_DECISION`, never automatically executed, and the plan says
the human choice is a predeclared qualification-only test input. It also says
the synthetic grant’s type, scope, issuer trust, and independent applicability
predicate must be pinned before execution. Those concrete decision and issuer
inputs were never defined in the authoritative fixtures.

## Current evidence

Retry 3 plus T02 demonstrate:

- canonical initial selection and actual CHECK/COLLECT results;
- accepted CHECK/COLLECT knowledge;
- PREPARE selection and decision-input routing;
- authoritative DecisionDossier binding;
- 2/2 independent fact proofs;
- 6/6 deterministic validations;
- native dossier admission;
- `E2-DECIDE` readiness and `HUMAN_HANDOFF` control;
- continued enforcement of the E2-FINISH completion prerequisite.

They do not demonstrate recorded decision admission, authority applicability,
external request/absence, or `EXTERNAL_WAIT`.

## Boundary and ownership

The package boundary is clean. The original plan assigns the human decision and
external wait to P02; P03 begins only after P02 PASS and owns persistence, cold
restoration, governed-unknown variation, and post-reload invalidation. P04
owns synthetic source admission, receipt, reentry, and post-reentry execution.
No later package owns the missing P02 decision transition.

The transition required between `HUMAN_HANDOFF` and `EXTERNAL_WAIT` is:

```text
predeclared qualification-only human choice
  -> authenticated authority/grant and recorded decision
  -> E2-DECIDE admitted/completed
  -> normal recomputation and external request/absence
  -> EXTERNAL_WAIT
```

The first two steps are contract-incomplete. Continuing would require
inventing issuer, choice evidence, authority binding, or option semantics.

## Result

`HUMAN_HANDOFF` is a demonstrated intermediate state, not a supported P02
terminal state. The strongest legitimate P02 result remains `PARTIAL` under the
unchanged original exit predicate. `P02_CONTRACT_INCOMPLETE=YES`.

P03 cannot begin from this state because the plan requires P02 PASS. No P03
initial state is authorized. D01, END, and REVIEW remain later dependency
cases; none is executed or changed here.

Missing P02 specification:

- exact synthetic choice value to use for qualification;
- issuer role, identity/trust, and authority issuance relationship;
- native authority entity/predicate binding;
- authenticated choice-evidence and recorded-decision source;
- option-specific consequences, including the DECLINE path;
- exact post-decision control oracle through external request/absence.

No Action was executed in this reconciliation, no option was selected, and E1
remains frozen.
