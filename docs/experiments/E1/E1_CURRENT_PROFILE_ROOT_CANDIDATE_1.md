# E1 Current Profile Root Candidate 1

## Disposition

A deterministic current R4 profile-root candidate was constructed and technically qualified as a candidate only. No `CURRENT_PROFILE_ROOT_AUTHORITY-1` was issued and no profile was released.

Candidate artifact: `docs/experiments/E1/E1_CURRENT_PROFILE_ROOT_CANDIDATE_1.json`
Candidate identity: `CurrentProfileRootCandidate-sha256:83b8cbc0549c64d21eaccaffc1fa45b49be368a878ccecdf9572d476477dfcd6`
Canonical identity-body bytes: `2390`
Canonicalization: lexicographically sorted UTF-8 JSON, compact separators, listed array order; identity is SHA-256 over the body before derived identity fields.

## Source manifest

- Historical baseline: `E1-PRODUCTION-PROFILE-6`, `sha256:fb842649d30e5876fb3f299e890e2c555a88be759c29b2c6577552d4885b0226` (technical baseline only; stale current authority).
- Current R4/G4 scope and runtime: exact values authorized by the Architect.
- Provider, payload, retention, transmission, and content-clearance records: exact issued authorities listed in the candidate.
- Lifecycle baseline: previously qualified `WorkAuthorizationTemplate-sha256:d49797c4d2072c310f30f038be6fd597d3a74b2ce6a0a8a06d6dd831989ffee8`.

## Difference report

Every difference from Profile-6 is classified as follows:

- `CURRENT_SCOPE_REBINDING`: R4-final/G4 runtime, controller lineage, and first-request scope replace historical PD06/R8–R11 scope.
- `CURRENT_AUTHORITY_REBINDING`: provider/model, payload, retention, transmission, content-clearance, and lifecycle references bind the issued current authorities.
- `REQUIRED_R4_TECHNICAL_CHANGE`: none identified. Historical least-authority restrictions remain technically compatible.
- `UNEXPECTED_CHANGE`: none.

The historical Profile-6 bytes and embedded status remain unchanged.

## Qualification

| Dimension | Result | Basis |
|---|---|---|
| Tool/action registry | PASS | Empty tools; generic tools/MCP/connectors/additional agents denied |
| Repository/read/write roots | PASS | Explicit roots and qualified task write paths only; promotion denied |
| Execution/shell/network | PASS | Python allowlist; shell and task network denied; endpoint-only model transport |
| Credential/secret handling | PASS | Host-side reference only; model-visible credentials/secrets denied |
| Provider/model boundary | PASS | Issued OpenAI/gpt-5 provider authority |
| Payload/content clearance | PASS | Issued payload and content-clearance authorities |
| Transmission/retention | PASS | Issued single-use transmission and bounded retention authorities |
| Audit | PASS | Append-only audit and restart/no-reset semantics |
| Ownership/recovery | PASS | Shared ownership ledger and qualified lifecycle template |
| Budgets/escalation | PASS | Existing E1 bounded budgets and fail-closed escalation |
| Authority expansion | PASS | Explicitly none |

No unresolved dimension, failure, unexpected change, or new prerequisite was found in this bounded qualification.

## Unissued authority preparation

The candidate is sufficient to prepare, but not issue, `CURRENT_PROFILE_ROOT_AUTHORITY-1` binding `CurrentProfileRootCandidate-sha256:83b8cbc0549c64d21eaccaffc1fa45b49be368a878ccecdf9572d476477dfcd6`, the exact constraints, current authorities, R4/G4 lineage, and first-request scope. Architect release remains required.

## Effects

Dependency topology/status, production R4/G4, r13, and all historical artifacts are unchanged. No payload was transmitted, no model request occurred, and no lifecycle state was activated.
