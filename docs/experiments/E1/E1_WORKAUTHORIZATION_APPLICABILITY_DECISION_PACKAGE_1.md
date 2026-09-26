# E1 WorkAuthorization Applicability Decision Package 1

## Architect decision required

`WORKAUTHORIZATION = WorkAuthorization-sha256:bc53d20ea0383febbd7ce1c10e2e00b2461a722942b853f43ea5001b42976c61`

`TARGET = exact current R4/G4 execution envelope`

Semantic comparison: **FAIL for applicability preservation** because invocation, dispatch, OperationalContext, and OperationalBinding identities differ from the existing WorkAuthorization's original bindings. Other dimensions are exact or compatible current rebindings, but compatibility does not confer applicability.

Expansion: `NONE`. The existing WorkAuthorization remains unchanged, valid under its original scope, unconsumed, and single-use.

`ARCHITECT_DECISION_REQUIRED = DECLINE_APPLICABILITY` for this candidate, or issue a separate reauthorization/replacement decision for exact current bindings. This package does not make that decision.

## Candidate

Canonical unissued candidate: `E1_WORKAUTHORIZATION_APPLICABILITY_RECONCILIATION_CANDIDATE_1.json`

Candidate identity: `WorkAuthorizationApplicabilityReconciliationCandidate-sha256:5a587140795abc041183aba21df1a599648ea6491c08a037ab3677602e426b57`
Canonical identity-body length: `3271` bytes

The candidate references rather than modifies the existing WorkAuthorization, preserves INACTIVE/NO OWNERSHIP, replay/single-use, and no-expansion constraints, and records `REAUTHORIZATION_REQUIRED`. It is evidence only and is not an issuable applicability approval.

## Consequences

Approval cannot satisfy applicability for this candidate. A new exact-current WorkAuthorization/issuance path would be required before `CONCRETE_WORKAUTH` and `INACTIVE_ISSUANCE` can become eligible. No dependency status changed.

`NEW_DEPENDENCY_DISCOVERED = NO`
`BASELINE_DEFECT = NO`
`PRODUCTION_EFFECT = NO`

No lifecycle, ownership, repository, host, transmission, or model action occurred.
