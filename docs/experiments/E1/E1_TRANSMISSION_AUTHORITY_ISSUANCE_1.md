# E1 Transmission Authority Issuance 1

## Issuance

The Architect approved transmission authority for exactly one first E1-WP-001 Programmer request. The append-only `CURRENT_TRANSMISSION_AUTHORITY-1` record below is issued; it authorizes no transmission by itself beyond the exact bound payload and boundary.

```json
{
  "record_type": "CURRENT_TRANSMISSION_AUTHORITY-1",
  "schema_version": "E1-AUTHORITY-1",
  "status": "ISSUED",
  "scope": "LIVE_R4/E1-WP-001/FIRST_PROGRAMMER_REQUEST",
  "provider_authority": "CurrentProviderModelAuthority-sha256:95b3d340ec85add69b1a472acffa4eb4372f3e528a8dc29278a8fe0fd58b0939",
  "payload_authority": "CurrentModelPayloadAuthority-sha256:cc20ba70d59acab0b322db7231cb4b77f183994dfb2db5c0b8405d5ed6629ada",
  "retention_authority": "CurrentRetentionAuthority-sha256:c17023b118aeb4ecd7a57a72b0d8f5826415ecb8dd87e83c49a55afde9d60462",
  "payload_sha256": "768fd8806adafad25d00db39c949cef00b129c34241129e5aecd0c2b30135d88",
  "payload_byte_length": 2842,
  "provider": "OpenAI",
  "endpoint": "https://api.openai.com/v1/responses",
  "model": "gpt-5",
  "runtime": "sha256:b6bcbb437f63c1433167103b1c7e15b723190721518e02ff2e4d2523fd625761",
  "controller_store": "AUTHORITY-STORE-GENERATION-sha256:ab07c7cbd889588fd80976bf5c47b7358722eaf6e2e1b7364e612c03899bf9ff",
  "transport": "HTTPS",
  "tls_minimum": "1.2",
  "configured_proxy": "none",
  "redirects": "denied",
  "store": false,
  "retention_configuration": "UNRESOLVED_ACCEPTED_FOR_SINGLE_BOUNDED_REQUEST",
  "purpose": "first E1-WP-001 Programmer request only",
  "single_use": true,
  "substitution": "REJECT",
  "dynamic_content": "REJECT",
  "authority_expansion": "NONE",
  "architect_decision": "APPROVE TRANSMISSION 1",
  "decision_date": "2026-09-21",
  "authority_id": "CurrentTransmissionAuthority-sha256:2adc46e1422ad0934597e398540f2e9f54eb57c601f8b29f8a805b06a611f79c"
}
```

Issued identity: `CurrentTransmissionAuthority-sha256:2adc46e1422ad0934597e398540f2e9f54eb57c601f8b29f8a805b06a611f79c`. Identity is SHA-256 over the canonical sorted-key JSON identity body excluding `authority_id`.

## Dependency transition

`CURRENT_TRANSMISSION_AUTHORITY`: `BLOCKED → SATISFIED`. Its existing baseline criteria are met by the exact provider, payload, retention, endpoint, runtime/G4, transport, single-use, and no-expansion bindings.

Deterministic propagation did not satisfy downstream execution nodes. `MODEL_REQUEST_READY` remains `BLOCKED`; its existing unsatisfied prerequisites are `HOST_CONSTRUCTION` and `CURRENT_CONTENT_CLEARANCE_AUTHORITY` (retention is satisfied). `HOST_CONSTRUCTION` remains blocked by its own existing prerequisites, including dispatcher/profile dependencies.

The recalculated actionable frontier is:

```text
CURRENT_CONTENT_CLEARANCE_AUTHORITY
```

## Prohibitions and preservation

No payload was sent; `/v1/responses` was not called; no model was invoked; lifecycle state was not activated; ownership was not assumed; E1-WP-001 was not executed. R4-final/G4, historical evidence, and existing authorities remain unchanged.
