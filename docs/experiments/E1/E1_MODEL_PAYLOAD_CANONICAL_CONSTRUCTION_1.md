# E1 Model Payload — Canonical Construction 1

Date: 2026-09-21  
Status: **CANDIDATE ONLY — NOT AUTHORIZED, NOT TRANSMITTED**

## Input manifest

- `E1-WP-001`: `docs/experiments/E1/pre_dispatch/E1-WP-001.md`, SHA-256 `1d0c276f2e0e818b89c128bfd6185cfa21968374d9868db833500e1e283c774c`; current E1 task projection and acceptance scope.
- E1 requirements: `docs/EXPERIMENT_1_REQUIREMENTS_SYNTHESIS.md`, SHA-256 `6fe78c3a27507dfe0d36012d5a878ed107780e6bc1fcef53b70c62f60084a8b2`; applicable task/governance constraints.
- E1 architecture: `docs/EXPERIMENT_1_ARCHITECTURE.md`, SHA-256 `951fb5736a7a16093ed5d995293496f8a2e18b1cca45f52e9f3c5be38f699ca8`; applicable governance/role constraints.
- Issued provider authority: `CurrentProviderModelAuthority-sha256:95b3d340ec85add69b1a472acffa4eb4372f3e528a8dc29278a8fe0fd58b0939`; fixed endpoint/model/storage metadata only.
- Issued retention authority: `CurrentRetentionAuthority-sha256:c17023b118aeb4ecd7a57a72b0d8f5826415ecb8dd87e83c49a55afde9d60462`; bounded retention acceptance only.
- Current R4/G4 lineage: runtime `sha256:b6bcbb437f63c1433167103b1c7e15b723190721518e02ff2e4d2523fd625761`; store `AUTHORITY-STORE-GENERATION-sha256:ab07c7cbd889588fd80976bf5c47b7358722eaf6e2e1b7364e612c03899bf9ff`.

No proposed input lacked current applicable authority for this candidate construction. No current profile, dynamic repository content, tool schema, or protected content was included because no such current authority was established.

## Canonical construction

The candidate is [E1_MODEL_PAYLOAD_CANDIDATE_1.json](./E1_MODEL_PAYLOAD_CANDIDATE_1.json). Canonicalization is JSON UTF-8 with lexicographically sorted object keys, listed array order, compact separators, no insignificant whitespace, and SHA-256 over the canonical bytes without the trailing artifact newline.

- Canonical payload byte length: `2842`
- Candidate payload SHA-256: `sha256:768fd8806adafad25d00db39c949cef00b129c34241129e5aecd0c2b30135d88`
- Canonicalization version: `E1-MODEL-PAYLOAD-CANONICAL-1`
- Independent reproducibility: **PASS** (constructed bytes and digest reproduced by the same deterministic serializer).

## Content inventory

- Task projection: E1-WP-001 objective, boundary, acceptance IDs, and source identity.
- Governance projection: bounded role, no permission expansion, fail-closed missing evidence, no network/model request for the offline utility, and stop-on-mismatch rules.
- Fixed metadata: issued provider/model facts, issued bounded retention acceptance, first-request purpose, and current R4/G4 lineage.
- Preloaded knowledge: empty.
- Tool schemas: empty.
- Dynamic repository content: empty.
- Excluded: secrets, credentials, unrelated repository content, unapproved dynamic content, unnecessary implementation/environment information, and unrelated authority.

No secret, credential, unrelated file bytes, hidden dynamic content, or authority expansion is present in the candidate. The payload contains references and semantic projections, not source-file contents beyond the explicitly authorized task projection.

## Historical digest comparison

Historical `ModelPayloadDigest` reference: `d675d581c80f43e691a31da73ccf17fd4bcc6b00d3a5331f26b9294e294e1538`. Candidate digest: `sha256:768fd8806adafad25d00db39c949cef00b129c34241129e5aecd0c2b30135d88`. Result: **MISMATCH**. The historical digest was not a construction target and does not alter this candidate.

## Unissued authority preparations

### `CURRENT_MODEL_PAYLOAD_AUTHORITY-1` — UNISSUED

```yaml
record_type: CURRENT_MODEL_PAYLOAD_AUTHORITY-1
status: UNISSUED
payload_identity: sha256:768fd8806adafad25d00db39c949cef00b129c34241129e5aecd0c2b30135d88
byte_length: 2842
canonicalization: E1-MODEL-PAYLOAD-CANONICAL-1
source_authorities: E1-WP-001 + E1 requirements + E1 architecture + issued provider authority + issued retention authority
runtime: sha256:b6bcbb437f63c1433167103b1c7e15b723190721518e02ff2e4d2523fd625761
controller_store: AUTHORITY-STORE-GENERATION-sha256:ab07c7cbd889588fd80976bf5c47b7358722eaf6e2e1b7364e612c03899bf9ff
purpose: first E1-WP-001 Programmer request only
content_scope: exact candidate inventory in E1_MODEL_PAYLOAD_CANDIDATE_1.json
architect_decision: UNISSUED
```

### `CURRENT_TRANSMISSION_AUTHORITY-1` — UNISSUED

```yaml
record_type: CURRENT_TRANSMISSION_AUTHORITY-1
status: UNISSUED
payload_identity: sha256:768fd8806adafad25d00db39c949cef00b129c34241129e5aecd0c2b30135d88
provider: OpenAI
endpoint: https://api.openai.com/v1/responses
model: gpt-5
transport: HTTPS TLSv1.2 minimum
configured_proxy: NONE
redirects: DENY
store: false
provider_authority: CurrentProviderModelAuthority-sha256:95b3d340ec85add69b1a472acffa4eb4372f3e528a8dc29278a8fe0fd58b0939
retention_authority: CurrentRetentionAuthority-sha256:c17023b118aeb4ecd7a57a72b0d8f5826415ecb8dd87e83c49a55afde9d60462
purpose: first E1-WP-001 Programmer request only
single_use: true
architect_decision: UNISSUED
```

Neither authority is issued. No dependency status changes are made. No transmission or model request occurred.

## Preservation

R4/G4 remains current; r13 remains unissued/unowned; provider/model requests and E1 effects remain zero. The candidate is inspectable as an immutable artifact only.
