# E1 Current Profile Release 1

## Issued authority

The minimum canonical `ReleasedProfileAuthority-1` record was issued for the exact Architect decision and exact first E1-WP-001 request scope.

```json
{
  "record_type": "RELEASED-PROFILE-AUTHORITY-1",
  "schema_version": "E1-AUTHORITY-1",
  "status": "ISSUED",
  "candidate_profile_identity": "CurrentProfileRootCandidate-sha256:83b8cbc0549c64d21eaccaffc1fa45b49be368a878ccecdf9572d476477dfcd6",
  "profile_root_authority": "CurrentProfileRootAuthority-sha256:bffbdf78c76cd98a9a07e6176afea526a876439dad589ce427cde9174ace5329",
  "runtime": "sha256:b6bcbb437f63c1433167103b1c7e15b723190721518e02ff2e4d2523fd625761",
  "controller_store": "AUTHORITY-STORE-GENERATION-sha256:ab07c7cbd889588fd80976bf5c47b7358722eaf6e2e1b7364e612c03899bf9ff",
  "scope": "LIVE_R4/G4/E1-WP-001/FIRST_PROGRAMMER_REQUEST",
  "lineage": "R4-final CURRENT UNIQUE",
  "provider_authority": "CurrentProviderModelAuthority-sha256:95b3d340ec85add69b1a472acffa4eb4372f3e528a8dc29278a8fe0fd58b0939",
  "payload_authority": "CurrentModelPayloadAuthority-sha256:cc20ba70d59acab0b322db7231cb4b77f183994dfb2db5c0b8405d5ed6629ada",
  "retention_authority": "CurrentRetentionAuthority-sha256:c17023b118aeb4ecd7a57a72b0d8f5826415ecb8dd87e83c49a55afde9d60462",
  "transmission_authority": "CurrentTransmissionAuthority-sha256:2adc46e1422ad0934597e398540f2e9f54eb57c601f8b29f8a805b06a611f79c",
  "content_clearance_authority": "CurrentContentClearanceAuthority-sha256:3243f4e84d3434655d8455355bd9ea742c0659cbf49827b9eeb80160b39646b3",
  "least_authority_constraints": "E1_CURRENT_PROFILE_ROOT_CANDIDATE_1",
  "historical_profile_6": "HISTORICAL_ONLY",
  "single_use": true,
  "authority_expansion": "NONE",
  "architect_decision": "APPROVE CURRENT PROFILE RELEASE",
  "decision_date": "2026-09-21",
  "authority_id": "ReleasedProfileAuthority-sha256:ec39636dc469f50ab460844d68fef31129035ea1a556e98e7a4b2951f1faa407"
}
```

Issued identity: `ReleasedProfileAuthority-sha256:ec39636dc469f50ab460844d68fef31129035ea1a556e98e7a4b2951f1faa407`. Identity is SHA-256 over the canonical sorted-key identity body excluding `authority_id`.

Historical Profile-6 remains historical-only. Least-authority constraints are preserved; no other profile, request, tool, repository, shell/network, lifecycle, or authority expansion is covered.

## Dependency transition and propagation

`RELEASED_PROFILE_CURRENT`: `BLOCKED → SATISFIED`. The next actionable frontier is `PROGRAMMER_PROFILE`, whose prerequisites are now satisfied and which requires its own existing criteria evaluation.

`PROGRAMMER_PROFILE`: `FRONTIER` (eligible for evaluation; not automatically satisfied).
`HOST_CONSTRUCTION`: `BLOCKED` (dispatcher eligibility remains unsatisfied).
`MODEL_REQUEST_READY`: `BLOCKED` (host construction remains unsatisfied).

No topology changed and no downstream semantic result was inferred.

## Effects

No host was constructed, no lifecycle state was activated, no ownership was assumed, no payload was transmitted, and no model request occurred. R4/G4 and historical evidence remain unchanged.
