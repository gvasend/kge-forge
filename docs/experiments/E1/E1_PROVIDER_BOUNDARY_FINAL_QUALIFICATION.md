# E1 Provider Boundary — Final Fact Qualification

Date: 2026-09-21  
Purpose: qualify externally observable provider-boundary facts only.  
Authority status: `CURRENT_PROVIDER_MODEL_AUTHORITY-1` remains **UNISSUED**.

## Model availability

A harmless authenticated metadata request was performed:

```text
GET https://api.openai.com/v1/models/gpt-5
```

Result:

```yaml
classification: OBSERVED_RUNTIME_FACT
result: AVAILABLE
http_status: 200
model_id: gpt-5
object: model
owned_by: system
request_id: 2ae05d75-d91a-4cca-ab9f-40d0df340042
server_date: 2026-09-21T14:16:04Z
project_identifier: NOT_RETURNED_BY_MODEL_OBJECT
freshness: response observed 2026-09-21; server date recorded above
```

This establishes that `gpt-5` is available to the authenticated credential/project context used by E1. It does not issue model-selection authority and does not disclose a project ID. No Responses request and no E1-WP-001 payload transmission occurred.

## Effective retention configuration

The environment exposed an API credential but no admin credential (`OPENAI_ADMIN_KEY` was absent). The official admin retrieval operations are:

- `GET /organization/data_retention` for organization configuration;
- `GET /organization/projects/{project_id}/data_retention` for project configuration.

Both require admin authority. Because that authority was unavailable, no retention-configuration request was made.

| Fact | Classification | Result |
|---|---|---|
| `/v1/responses` with `store=false` avoids normal foreground application-state retention | `PROVIDER_DOCUMENTED_BEHAVIOR` | Established from official OpenAI data-controls documentation. |
| Default abuse-monitoring retention | `PROVIDER_DOCUMENTED_BEHAVIOR` | Generally 30 days, subject to organization controls and exceptions. |
| E1 organization retention setting | `UNRESOLVED` | Admin authority unavailable. |
| E1 project retention setting | `UNRESOLVED` | Admin authority unavailable. |
| Effective E1 retention boundary | `UNRESOLVED` | Cannot combine undocumented project/org settings. |

Sources: [OpenAI data controls](https://developers.openai.com/api/docs/guides/your-data), [organization retention retrieval](https://developers.openai.com/api/reference/python/resources/admin/subresources/organization/subresources/data_retention/methods/retrieve), and [project retention retrieval](https://developers.openai.com/api/reference/python/resources/admin/subresources/organization/subresources/projects/subresources/data_retention/methods/retrieve).

## Client-side transmission boundary

```yaml
endpoint: https://api.openai.com/v1/responses
interface: Responses API
provider: OpenAI
tls_minimum: TLSv1.2
configured_proxy: NONE
redirects: DENY
configured_gateway: NONE
external_infrastructure_intermediaries: OUTSIDE_QUALIFIED_CLIENT_BOUNDARY
```

These are observed adapter configuration facts. No attempt was made to prove absence of Internet, cloud-provider, or OpenAI-internal intermediaries.

## Proposed unissued authority record

```yaml
record_type: CURRENT_PROVIDER_MODEL_AUTHORITY-1
status: UNISSUED
scope: LIVE_R4/E1-WP-001/FIRST_PROGRAMMER_REQUEST
provider: OpenAI
interface: Responses API
endpoint: https://api.openai.com/v1/responses
endpoint_fact: OBSERVED_RUNTIME_FACT
model_identity: gpt-5
model_availability: AVAILABLE_FOR_E1_CREDENTIAL_CONTEXT
model_availability_evidence: GET /v1/models/gpt-5 HTTP 200; request_id 2ae05d75-d91a-4cca-ab9f-40d0df340042
project_identifier: UNRESOLVED_NOT_RETURNED
transmission_boundary:
  endpoint: https://api.openai.com/v1/responses
  tls_minimum: TLSv1.2
  configured_proxy: NONE
  redirects: DENY
  external_intermediaries: OUTSIDE_QUALIFIED_CLIENT_BOUNDARY
request_storage: store=false
provider_application_state: NO_FOREGROUND_APPLICATION_STATE_PER_DOCUMENTATION
provider_abuse_monitoring_retention: GENERALLY_30_DAYS_PER_DOCUMENTATION
organization_retention_configuration: UNRESOLVED
project_retention_configuration: UNRESOLVED
effective_retention_boundary: UNRESOLVED
purpose: E1-WP-001 first Programmer request only
runtime: sha256:b6bcbb437f63c1433167103b1c7e15b723190721518e02ff2e4d2523fd625761
controller_store: AUTHORITY-STORE-GENERATION-sha256:ab07c7cbd889588fd80976bf5c47b7358722eaf6e2e1b7364e612c03899bf9ff
transmission_authority: UNRESOLVED
freshness: revalidate configuration, project context, and retention before issuance/effect
identity: UNISSUED_UNHASHED
architect_decision: UNISSUED
```

## Remaining field classifications

- **FACT_ACQUISITION:** effective organization/project retention configuration, if admin authority is later made available; exact project identifier if required for binding.
- **ARCHITECT_DECISION:** whether to issue this exact provider/model record for the first E1 request, and whether the unresolved retention configuration is acceptable under Architect policy.
- **EXTERNAL_AUTHORITY:** current content-transmission authority and any provider/project retention control not present in the API credential context.

The record is not issuance-ready while effective retention and transmission authority remain unresolved. No authority was issued, no dependency status changed, and no model request was made.
