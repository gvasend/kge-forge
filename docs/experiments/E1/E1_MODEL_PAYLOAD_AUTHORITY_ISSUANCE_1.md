# E1 Model Payload Authority Issuance 1

## Disposition

The Architect decision `APPROVE CANDIDATE` issued the minimum append-only `CURRENT_MODEL_PAYLOAD_AUTHORITY-1` for the exact first E1-WP-001 Programmer request. No payload bytes were changed and no request was transmitted.

## Issued authority

```json
{
  "record_type": "CURRENT_MODEL_PAYLOAD_AUTHORITY-1",
  "schema_version": "E1-AUTHORITY-1",
  "status": "ISSUED",
  "scope": "LIVE_R4/E1-WP-001/FIRST_PROGRAMMER_REQUEST",
  "payload_sha256": "768fd8806adafad25d00db39c949cef00b129c34241129e5aecd0c2b30135d88",
  "payload_byte_length": 2842,
  "payload_canonicalization": "E1-MODEL-PAYLOAD-CANONICAL-1",
  "provider_authority": "CurrentProviderModelAuthority-sha256:95b3d340ec85add69b1a472acffa4eb4372f3e528a8dc29278a8fe0fd58b0939",
  "provider": "OpenAI",
  "endpoint": "https://api.openai.com/v1/responses",
  "model": "gpt-5",
  "retention_authority": "CurrentRetentionAuthority-sha256:c17023b118aeb4ecd7a57a72b0d8f5826415ecb8dd87e83c49a55afde9d60462",
  "store": false,
  "retention_configuration": "UNRESOLVED_ACCEPTED_FOR_SINGLE_BOUNDED_REQUEST",
  "runtime": "sha256:b6bcbb437f63c1433167103b1c7e15b723190721518e02ff2e4d2523fd625761",
  "controller_store": "AUTHORITY-STORE-GENERATION-sha256:ab07c7cbd889588fd80976bf5c47b7358722eaf6e2e1b7364e612c03899bf9ff",
  "purpose": "first E1-WP-001 Programmer request only",
  "single_use": true,
  "substitution": "REJECT",
  "additional_content": "REJECT",
  "authority_expansion": "NONE",
  "architect_decision": "APPROVE CANDIDATE",
  "decision_date": "2026-09-21",
  "authority_id": "CurrentModelPayloadAuthority-sha256:cc20ba70d59acab0b322db7231cb4b77f183994dfb2db5c0b8405d5ed6629ada"
}
```

Authority identity: `CurrentModelPayloadAuthority-sha256:cc20ba70d59acab0b322db7231cb4b77f183994dfb2db5c0b8405d5ed6629ada`. The identity is SHA-256 over the canonical sorted-key JSON serialization of the identity body (excluding `authority_id`); the complete record is independently reproducible.

The authority binds payload `sha256:768fd8806adafad25d00db39c949cef00b129c34241129e5aecd0c2b30135d88` (2842 canonical bytes), current R4-final/G4 lineage, issued provider authority, issued retention authority, OpenAI Responses endpoint, `gpt-5`, `store=false`, single use, and the exact bounded purpose. Provider retention remains explicitly unresolved and accepted only for this request. Substitution, additional content, and authority expansion are rejected.

## Dependency transition

`CURRENT_MODEL_PAYLOAD_AUTHORITY`: `UNRESOLVED → SATISFIED`, supported by this issued record and the Architect decision. No graph edge or other node status was changed.

The recalculated frontier removes `CURRENT_MODEL_PAYLOAD_AUTHORITY`. The remaining frontier is:

```text
CURRENT_TRANSMISSION_AUTHORITY
```

No newly exposed node was semantically resolved.

## Preservation and effects

R4-final and live G4 remain unchanged. Provider/model and retention authorities remain unchanged. No transmission authority was issued, no lifecycle authority was issued, no WorkAuthorization was consumed, and no provider/model request or E1 effect occurred. Historical payload and dependency evidence remain preserved.
