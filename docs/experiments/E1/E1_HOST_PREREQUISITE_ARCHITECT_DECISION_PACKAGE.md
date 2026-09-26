# E1 Host Prerequisite — Architect Decision Package

No authority is issued by this package.

## Repository authority

Proposed `CURRENT_REPOSITORY_AUTHORITY-1` scope:

- Profile: `ProgrammerProfile-sha256:0a0718f285a942c13a9f00e4b367cbea2394937fa18c4d7e11ed2c6c2803dd67`
- Released profile: `ReleasedProfileAuthority-sha256:ec39636dc469f50ab460844d68fef31129035ea1a556e98e7a4b2951f1faa407`
- Runtime: `sha256:b6bcbb437f63c1433167103b1c7e15b723190721518e02ff2e4d2523fd625761`
- Controller store: G4 `AUTHORITY-STORE-GENERATION-sha256:ab07c7cbd889588fd80976bf5c47b7358722eaf6e2e1b7364e612c03899bf9ff`
- Scope: E1-WP-001 first Programmer execution only

Permissions are the already qualified least-authority values:

- Read roots: `/home/gvasend/app/kge-forge`, `/home/gvasend/app/kge-forge-demo`.
- Write roots: `/home/gvasend/app/kge-forge/src/kge_forge/__init__.py`, `/home/gvasend/app/kge-forge/src/kge_forge/context`, `/home/gvasend/app/kge-forge/tests/context`, and `/home/gvasend/app/kge-forge/docs/implementation/E1-WP-001.md`.
- Denied: `.git`, `.codex`, `.agents`, the demo equivalents, protected requirements/architecture/governance files, all other write paths, secrets, credentials, and unrelated content.
- Promotion: none; separate governed write/patch authority is required.
- Dynamic expansion: denied. Paths cannot be added by caller, model, profile, or runtime defaults.
- Restart/recovery: same authenticated profile, invocation, scope, and append-only audit/ownership identities; no reset or truncation. Active or uncertain reservations block.

Architect choice: `REAUTHORIZE_QUALIFIED_VALUES` for this exact scope, or reject/replace a listed permission. No broader repository authority is proposed.

## Status and budget authority

Proposed `CURRENT_STATUS_BUDGET_AUTHORITY-1` adopts the qualified `E1-RUN-CONTROL-1` policy for the same exact scope:

```json
{"schema":"E1-RUN-CONTROL-1","seconds":{"cycle":[120,300],"no_progress":[180,300],"invocation":[1200,1800],"phase":[30,120],"requests":[8,12],"tokens":[100000,150000],"automatic_retry":false,"usage_unknown":"TIME_AND_REQUEST_LIMITS_ONLY"}
```

Dimensions and behavior:

- Cycle, no-progress, invocation, and phase time limits: `QUALIFIED_VALUE` above; current applicability must be accepted for R4/G4.
- Request and token limits: `QUALIFIED_VALUE` above; no extension or reset.
- Status: append-only fresh status; stale/unknown or malformed evidence fails closed.
- Hard exhaustion: close admission, prevent future execution, reconcile ownership/ExecutionScope, and reach QUIESCENT/terminal recovery through the qualified path.
- Cancellation: authoritative cancellation dominates telemetry; ownership releases where held; no cancellation claim is made for an unconfirmed provider transmission.
- Escalation: fail closed; no automatic retry (`automatic_retry=false`); uncertain restart or request outcome blocks.
- Recovery: reconstruct counters, policy digest, identity, and evidence from durable records; changed boot, policy substitution, truncation, or ambiguous request outcome blocks; consumed budget is not reset.
- Authority expansion: none.

Architect choice: `REAUTHORIZE_QUALIFIED_VALUES` for the exact first request, or identify a narrower correction. This is not a new budget allocation.

## Current applicability

The values are technically qualified against the current Programmer Profile and current R4/G4 bindings. The remaining action is human reauthorization of the exact bounded repository and status/budget scopes; no unrelated requalification is required.

## Unissued records

Both proposed records remain `UNISSUED`; no signatures, timestamps, identities, or issuance markers are assigned. If issued, deterministic propagation would make `REPOSITORY_AUTHORITY` and `STATUS_BUDGET` eligible for their existing satisfaction checks. Host construction would still require its other existing prerequisites.

## Architect decision summary

- `REAUTHORIZE_QUALIFIED_VALUES` for the exact listed repository roots and permissions.
- `REAUTHORIZE_QUALIFIED_VALUES` for the exact qualified E1-RUN-CONTROL-1 status/budget policy.
