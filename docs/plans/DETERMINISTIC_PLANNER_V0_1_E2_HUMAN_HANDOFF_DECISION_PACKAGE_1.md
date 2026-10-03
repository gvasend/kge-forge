# E2 Human-Handoff Decision Package

## Decision

**Subject:** `E2-DECIDE`.

The Planner reached human handoff because the admitted DecisionDossier is
decision-ready and `E2-DECIDE` is actionable, but the operation is an
`ARCHITECT_CONTRACT_DECISION`. The Planner cannot select or issue a human
decision autonomously. The downstream control depends on an authenticated
recorded decision before the route can proceed toward `E2-REENTER` and the
governed external-evidence boundary.

## Allowed options

The dossier defines exactly two options:

- `ALLOW_QUALIFICATION_MAPPING` — semantic meaning beyond the option label is
  **NOT SPECIFIED**. The dossier states only that approval would be prospective
  qualification-only `USE` permission for the E2 mapping target; it grants no
  production, E1, proof, root, or slot authority.
- `DECLINE` — semantic meaning and downstream consequences are **NOT
  SPECIFIED**.

No recommendation or option selection is made here. Assumptions,
option-specific risks, and downstream effects are not separately defined in
the admitted dossier.

## Verified information

Common evidence for either option:

- `E2-K-CHECK` and `E2-K-COLLECT` were admitted from the qualified CHECK and
  COLLECT results.
- Independent fact proofs: `E2-KP-CHECK` and `E2-KP-COLLECT`, both PASS.
- Six deterministic dossier validations, all PASS: `QUESTION_SCOPE`,
  `SOURCE_PROVENANCE`, `CONCRETE_ALTERNATIVES`, `AUTHORITY_BOUNDARY`,
  `DECISION_FACTS_COMPLETE`, and `INDEPENDENT_VALIDATION`.
- DecisionDossier identity:
  `6a507317bc9cc323fbaa626e97b5954cf3ad934b0bd92d9dc96bd4f63e07bddb`.

No option-specific evidence is defined.

## Authority required

The PC02 authority fixture names `E2-GRANT` in the `AUTHORITY_IDENTITY`
domain, with permission `USE`, subject `E2-REENTER`, scope
`E2-QUALIFICATION-ONLY`, and lineage `E2-CANONICAL-BASELINE-1`. Applicability
requires the exact choice, target, permission, scope, lineage, and a current
independent predicate. The issuer/owner and concrete native authority record
are **UNDEFINED** in the current experiment material.

The dossier explicitly excludes production authority, E1 authority, proof
satisfaction, and root/slot satisfaction.

## Required recorded decision

The native interface requires a `RecordedDecision` containing:

- selected option (`choice`),
- decision subject (`E2-DECIDE`),
- authority predicate reference,
- authenticated record/entity reference,
- exact pre-state snapshot identity,
- and the native provenance/currentness carried by the referenced objects.

The referenced record must bind the decision subject and selected option; the
authority predicate must be an applicable current `DECIDE` predicate bound to
the exact dossier. Choice evidence must be an accepted, current knowledge
record named `decision-choice:E2-DECIDE`, whose statement equals the selected
option and whose provenance equals the authenticated record provenance.

The native shape is defined, but the experiment does not define an issuer,
concrete authority entity/predicate, selected option, record identity, or
choice-evidence source. Therefore the issuance/materialization mechanism is
incomplete: `CHOICE_EVIDENCE_CONTRACT_MISSING` for execution purposes.

## Human review format

**QUESTION:** Permit this qualification-only bounded mapping after independently
valid evidence?

**WHY PLANNER STOPPED:** The dossier is admitted and `E2-DECIDE` is actionable,
but issuing a decision requires an authenticated authority and pinned choice
evidence that are not present in the canonical state.

**OPTION A:** `ALLOW_QUALIFICATION_MAPPING` — prospective qualification-only
`USE` permission is documented; other consequences are not specified.

**OPTION B:** `DECLINE` — consequences are not specified.

**VERIFIED FACTS:** 2/2 independent fact proofs PASS.

**VALIDATIONS:** 6/6 deterministic dossier validations PASS.

**AUTHORITY REQUIRED:** Current applicable `E2-GRANT`-class authority for
`E2-REENTER`, exact scope/lineage and decision choice, with an authenticated
issuer/record.

**WHAT HAPPENS AFTER A CHOICE:** If the native authority and choice evidence
are supplied and admitted, `apply_recorded_decision` records the choice and
the Planner recomputes normally. No later transition is executed here.

**MISSING INFORMATION:** Issuer/owner, selected option, native authority
entity/predicate, authenticated record identity, and pinned choice-evidence
source.

## Readiness

`HUMAN_DECISION_READY = NO`.

Blockers are the undefined issuer/authority materialization, unspecified
choice-evidence issuance source, and unspecified option consequences. No
option was selected, no authority was issued, and no decision was recorded.

`E2_P02_RETRY_ALLOWED=NO`, `E2_P03_READY=NO`, `N_REAL_SATISFIED=NO`,
`IMPLEMENTATION_MODIFIED=NO`, `EXPERIMENT_ACTIONS_EXECUTED=0`,
`E1_ARTIFACTS_MODIFIED=0`, and `PRODUCTION_EFFECT=NO`.
