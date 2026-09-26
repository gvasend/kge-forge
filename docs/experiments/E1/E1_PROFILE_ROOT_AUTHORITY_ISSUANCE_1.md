# E1 Current Profile Root Authority Issuance 1

Issued the minimum append-only `CURRENT_PROFILE_ROOT_AUTHORITY-1` under the Architect decision approving the exact technically qualified candidate.

```json
{
  "record_type": "CURRENT_PROFILE_ROOT_AUTHORITY-1",
  "schema_version": "E1-AUTHORITY-1",
  "status": "ISSUED",
  "candidate_identity": "CurrentProfileRootCandidate-sha256:83b8cbc0549c64d21eaccaffc1fa45b49be368a878ccecdf9572d476477dfcd6",
  "scope": "LIVE_R4/G4/E1-WP-001/FIRST_PROGRAMMER_REQUEST",
  "runtime": "sha256:b6bcbb437f63c1433167103b1c7e15b723190721518e02ff2e4d2523fd625761",
  "controller_store": "AUTHORITY-STORE-GENERATION-sha256:ab07c7cbd889588fd80976bf5c47b7358722eaf6e2e1b7364e612c03899bf9ff",
  "lineage": "R4-final CURRENT UNIQUE",
  "provider_authority": "CurrentProviderModelAuthority-sha256:95b3d340ec85add69b1a472acffa4eb4372f3e528a8dc29278a8fe0fd58b0939",
  "payload_authority": "CurrentModelPayloadAuthority-sha256:cc20ba70d59acab0b322db7231cb4b77f183994dfb2db5c0b8405d5ed6629ada",
  "retention_authority": "CurrentRetentionAuthority-sha256:c17023b118aeb4ecd7a57a72b0d8f5826415ecb8dd87e83c49a55afde9d60462",
  "transmission_authority": "CurrentTransmissionAuthority-sha256:2adc46e1422ad0934597e398540f2e9f54eb57c601f8b29f8a805b06a611f79c",
  "content_clearance_authority": "CurrentContentClearanceAuthority-sha256:3243f4e84d3434655d8455355bd9ea742c0659cbf49827b9eeb80160b39646b3",
  "lifecycle_template": "WorkAuthorizationTemplate-sha256:d49797c4d2072c310f30f038be6fd597d3a74b2ce6a0a8a06d6dd831989ffee8",
  "least_authority_constraints": "E1_CURRENT_PROFILE_ROOT_CANDIDATE_1",
  "historical_baseline": "E1-PRODUCTION-PROFILE-6 historical only",
  "architect_decision": "APPROVE CURRENT PROFILE ROOT",
  "decision_date": "2026-09-21",
  "single_use": true,
  "authority_expansion": "NONE",
  "profile_release": "NOT_AUTHORIZED",
  "authority_id": "CurrentProfileRootAuthority-sha256:bffbdf78c76cd98a9a07e6176afea526a876439dad589ce427cde9174ace5329"
}
```

Issued identity: `CurrentProfileRootAuthority-sha256:bffbdf78c76cd98a9a07e6176afea526a876439dad589ce427cde9174ace5329`. Identity is SHA-256 over the canonical sorted-key identity body excluding `authority_id`.

## Dependency transition

`PROFILE_ROOTS`: `BLOCKED → SATISFIED`. The transition is bound to candidate `CurrentProfileRootCandidate-sha256:83b8cbc0549c64d21eaccaffc1fa45b49be368a878ccecdf9572d476477dfcd6`, exact R4/G4 scope, and the already-issued provider, payload, retention, transmission, content-clearance, and lifecycle authorities.

The next actionable frontier is `RELEASED_PROFILE_CURRENT`. No profile was released; this authority does not authorize other requests, tools, repositories, shell/network access, or model execution.

## Preservation

Historical Profile-6 remains unchanged and historical only. R4/G4 production state is unchanged. No payload was transmitted, no model request occurred, and no lifecycle/E1 effect occurred.
