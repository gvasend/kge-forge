# E1 Released Profile Current Resolution 1

## Result

`KNOWN_LEAF_REQUIRES_AUTHORITY`

The current profile-root authority is sufficient prerequisite evidence, but it does not itself release the profile. `RELEASED_PROFILE_CURRENT` requires a distinct Architect profile-release authority.

## Local subgraph

- Node: `RELEASED_PROFILE_CURRENT`
- Prerequisites: `CURRENT_CONTENT_CLEARANCE_AUTHORITY` = `SATISFIED`; `PROFILE_ROOTS` = `SATISFIED`
- Immediate dependents: `ACTIVATION_CONTEXT`, `HOST_CONSTRUCTION`, `OPERATIONAL_BINDING_CURRENT`, `PROGRAMMER_PROFILE`, `RELEASE_AUTHORITY_CURRENT`
- Scope: `LIVE_R4/E1`
- Lineage: `Profile-6 → current candidate`

## Release conditions

| Condition | Result | Basis |
|---|---|---|
| Exact candidate profile is technically qualified | SATISFIED | `CurrentProfileRootCandidate-sha256:83b8cbc0549c64d21eaccaffc1fa45b49be368a878ccecdf9572d476477dfcd6` |
| Current profile-root authority authenticates candidate | SATISFIED | `CurrentProfileRootAuthority-sha256:bffbdf78c76cd98a9a07e6176afea526a876439dad589ce427cde9174ace5329` |
| Current content clearance and related bindings are present | SATISFIED | Issued current content, payload, provider, retention, and transmission authorities |
| Exact R4/G4 and first-request scope | SATISFIED | Candidate/root scope bindings |
| Architect profile-release decision | **AUTHORITY_REQUIRED** | No release decision has been issued |
| Current `ReleasedProfileAuthority` record | **UNSATISFIED** | No canonical released-profile record exists |

Technical qualification and profile-root authority do not imply release authority under the existing baseline. Profile-6 remains historical-only and is not released or reauthorized.

## Minimum Architect decision

Approve release of exactly the candidate profile identified by `CurrentProfileRootCandidate-sha256:83b8cbc0549c64d21eaccaffc1fa45b49be368a878ccecdf9572d476477dfcd6`, bound to `CurrentProfileRootAuthority-sha256:bffbdf78c76cd98a9a07e6176afea526a876439dad589ce427cde9174ace5329`, exact current R4-final/G4 lineage, and E1-WP-001 first Programmer request only.

The decision must authorize no other profile, request, tool, repository, model, lifecycle, or authority expansion.

## Unissued release record prepared for inspection

```json
{
  "record_type": "RELEASED-PROFILE-AUTHORITY-1",
  "status": "UNISSUED",
  "candidate_profile_identity": "CurrentProfileRootCandidate-sha256:83b8cbc0549c64d21eaccaffc1fa45b49be368a878ccecdf9572d476477dfcd6",
  "profile_root_authority": "CurrentProfileRootAuthority-sha256:bffbdf78c76cd98a9a07e6176afea526a876439dad589ce427cde9174ace5329",
  "runtime": "sha256:b6bcbb437f63c1433167103b1c7e15b723190721518e02ff2e4d2523fd625761",
  "controller_store": "AUTHORITY-STORE-GENERATION-sha256:ab07c7cbd889588fd80976bf5c47b7358722eaf6e2e1b7364e612c03899bf9ff",
  "scope": "LIVE_R4/G4/E1-WP-001/FIRST_PROGRAMMER_REQUEST",
  "historical_profile_6": "HISTORICAL_ONLY",
  "architect_release_decision": "ARCHITECT_CHOICE_REQUIRED",
  "authority_expansion": "NONE",
  "single_use": true
}
```

No identity, signature, timestamp, or issuance marker is assigned to this unissued proposal.

## Effects

No dependency status or topology changed. No profile was released, no host was constructed, no lifecycle state was activated, and no payload or provider request occurred.
