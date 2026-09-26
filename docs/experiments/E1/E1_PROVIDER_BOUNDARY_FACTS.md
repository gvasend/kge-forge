# E1 Provider Boundary Facts

Date: 2026-09-21  
Purpose: fact acquisition for an unissued `CURRENT_PROVIDER_MODEL_AUTHORITY-1`.  
Production/model-request state: unchanged; no E1-WP-001 request was made.

## Fact classifications

### Observed runtime/configuration facts

The qualified governed adapter is `adapter/model_transport.py`, SHA-256:

`1f041eefa6e799701d1c5d986332055d4b56f9b39f588fe1e93e7a6e4c6af113`

Its current configuration function returns:

```yaml
provider: OpenAI
interface: Responses API
endpoint: https://api.openai.com/v1/responses
configured_model: gpt-5
store: false
proxy: NONE
redirects: DENY
timeout_seconds: 60
tls_minimum: TLSv1.2
ca_file: /etc/ssl/certs/ca-certificates.crt
credential_reference: OPENAI_API_KEY
```

The adapter constructs a direct HTTPS request to the endpoint, uses an empty `ProxyHandler`, and installs a no-redirect handler. No proxy, gateway, or redirect is configured in the governed adapter. The adapter does not itself prove the absence of infrastructure outside the process; an actual network path was not exercised.

The companion transmission-policy implementation is `adapter/model_transmission.py`, SHA-256:

`4c77db57e44cf8cca6f3e906db5a97005d73ba3126276a18e4330c537df8a39b`

It defaults disclosure to deny, excludes credentials, secrets, and controller-private state, and requires exact clearance records for initial context and later tool results. These are implementation/configuration facts, not authority.

### Provider-documented facts

The official OpenAI Models API reference documents `GET /v1/models` as the endpoint that lists models available to an API project and describes each model by an identifier. It does not establish which models are enabled for this E1 project without an authenticated project-scoped observation. [OpenAI Models API reference](https://developers.openai.com/api/reference/resources/models)

The official data-controls documentation states that `/v1/responses` has a 30-day application-state retention period by default or when `store=true`; `store=false` avoids that application-state storage for a foreground request. The same documentation states that abuse-monitoring retention is generally 30 days, subject to organization controls and documented exceptions, and that background mode has temporary polling storage. This E1 configuration does not enable background mode. [OpenAI data controls](https://developers.openai.com/api/docs/guides/your-data)

These provider-documented facts describe platform behavior. They do not authorize transmission of E1 content and do not establish this project’s organization-level retention controls.

## Required fact evaluation

| Required fact | Result | Classification | Evidence/freshness |
|---|---|---|---|
| Exact Responses endpoint | `https://api.openai.com/v1/responses` | `OBSERVED_RUNTIME_FACT` + `CONFIGURATION_FACT` | `adapter/model_transport.py`, SHA above; current working-tree inspection 2026-09-21; matches R4 qualified implementation identity. |
| Provider | OpenAI | `CONFIGURATION_FACT` | Adapter endpoint and Architect intent; not independently issued authority. |
| Configured model identity | `gpt-5` | `CONFIGURATION_FACT` | `model_transport.configuration()` and `validate()` require `gpt-5`; current file inspection 2026-09-21. |
| Exact model availability for the E1 credential/project | `AVAILABLE` for `gpt-5` | `OBSERVED_RUNTIME_FACT` | Authenticated `GET https://api.openai.com/v1/models/gpt-5` returned HTTP 200, `id=gpt-5`, `object=model`, `owned_by=system`, request ID `2ae05d75-d91a-4cca-ab9f-40d0df340042`, server date `2026-09-21T14:16:04Z`; exact project identifier was not returned. |
| Direct adapter boundary | `https://api.openai.com/v1/responses`, HTTPS, no configured proxy, redirects denied | `OBSERVED_RUNTIME_FACT` | `model_transport.py`; no network request made, so only configured process boundary is observed. |
| Proxy/gateway/intermediary | No configured proxy or gateway; infrastructure-level intermediary `UNRESOLVED` | `OBSERVED_RUNTIME_FACT` + `UNRESOLVED` | Empty `ProxyHandler`, no-redirect handler; actual route not exercised. |
| Request storage intent | `store=false` required by adapter validation | `CONFIGURATION_FACT` | `model_transport.py` rejects any payload whose `store` is not false. |
| Provider application-state behavior | Foreground Responses request with `store=false` is documented not to retain application state; exact project controls remain `UNRESOLVED` | `PROVIDER_DOCUMENTED_FACT` + `UNRESOLVED` | OpenAI data-controls documentation; organization/project controls not observed. |
| Abuse-monitoring retention | Documented default generally 30 days; exact effective project/org setting `UNRESOLVED` | `PROVIDER_DOCUMENTED_FACT` + `UNRESOLVED` | OpenAI data-controls documentation. |
| Background/temporary storage | Not configured by adapter; if background mode were used, provider documents temporary polling storage | `CONFIGURATION_FACT` + `PROVIDER_DOCUMENTED_FACT` | No background parameter in the adapter path; no request made. |
| Transmission authorization | `UNRESOLVED` | `UNRESOLVED` | Existing E1 blocker explicitly says implementation and references do not authorize provider transmission. |

## Proposed unissued `CURRENT_PROVIDER_MODEL_AUTHORITY-1`

This is a prepared record, not an issued authority. Values marked `CONFIGURATION_FACT` or `PROVIDER_DOCUMENTED_FACT` remain evidence inputs and do not become authority merely by appearing here.

```yaml
record_type: CURRENT_PROVIDER_MODEL_AUTHORITY-1
status: UNISSUED
scope: LIVE_R4/E1-WP-001/FIRST_PROGRAMMER_REQUEST
provider: OpenAI
interface: Responses API
endpoint: https://api.openai.com/v1/responses
endpoint_fact_class: OBSERVED_RUNTIME_FACT
configured_model_identity: gpt-5
configured_model_fact_class: CONFIGURATION_FACT
project_available_models: [gpt-5]
project_model_availability: AVAILABLE_FOR_E1_CREDENTIAL_CONTEXT
project_model_availability_evidence: GET /v1/models/gpt-5 HTTP 200; request_id 2ae05d75-d91a-4cca-ab9f-40d0df340042; server_date 2026-09-21T14:16:04Z
project_identifier: NOT_RETURNED_BY_MODEL_OBJECT
proxy: NONE_CONFIGURED
redirects: DENY
configured_gateway_or_intermediary: NONE
infrastructure_intermediary: UNRESOLVED
transport: HTTPS
minimum_tls: TLSv1.2
request_storage_parameter: store=false
provider_application_state_with_store_false: NO_FOREGROUND_APPLICATION_STATE_PER_PROVIDER_DOCUMENTATION
provider_abuse_monitoring_retention: GENERALLY_30_DAYS_PER_PROVIDER_DOCUMENTATION
organization_retention_configuration: UNRESOLVED_NO_ADMIN_KEY
project_retention_configuration: UNRESOLVED_NO_ADMIN_KEY
project_effective_retention_controls: UNRESOLVED
background_mode: NOT_CONFIGURED
purpose: E1-WP-001 first Programmer request only
runtime: sha256:b6bcbb437f63c1433167103b1c7e15b723190721518e02ff2e4d2523fd625761
controller_store: AUTHORITY-STORE-GENERATION-sha256:ab07c7cbd889588fd80976bf5c47b7358722eaf6e2e1b7364e612c03899bf9ff
transmission_authority: UNRESOLVED
freshness: revalidate all configuration and project-availability facts at final gate
lineage: R4-final → first E1 request
identity: UNISSUED_UNHASHED
architect_decision: UNISSUED
```

## Exact unresolved facts

1. **Project model availability:** the adapter is configured for `gpt-5`, but no authenticated project model-list observation establishes that `gpt-5` is currently available to the E1 project. A harmless model-list request would require explicit fact-acquisition authority; none was exercised here.
2. **Effective retention controls:** provider documentation describes default behavior, but the E1 organization/project’s effective abuse-monitoring, Zero Data Retention, Modified Abuse Monitoring, or related controls were not observed.
3. **Infrastructure-level intermediary:** the adapter configures no proxy or gateway, but no network request or independent route observation was performed.
4. **Transmission authority:** configuration and provider documentation do not authorize disclosure of E1 content. The existing E1 content-clearance/transmission authority remains unresolved.

Because these facts remain unresolved, the proposed record is fully enumerated but not content-complete for issuance. No provider/model authority is issued.

## Preservation

`R4-final = CURRENT + UNIQUE`; `LIVE_R4_FINAL_CONTROLLER_STORE = G4 CURRENT`; r13 remains `UNISSUED + UNOWNED`; provider/model requests remain zero; E1 effects remain zero. No dependency status, implementation, or production state was modified.


## Final fact qualification update

### Model availability observation

A read-only authenticated request was made to `GET https://api.openai.com/v1/models/gpt-5` using the existing E1 credential context. No Responses or model-inference request was made and no E1 payload was transmitted. The provider returned HTTP `200` with `id=gpt-5`, `object=model`, and `owned_by=system`. Request ID: `2ae05d75-d91a-4cca-ab9f-40d0df340042`. Server date: `2026-09-21T14:16:04Z`.

Result: **`AVAILABLE` for the credential/project context used by E1**. The model object does not disclose a project identifier; therefore the exact project name/ID remains `UNRESOLVED`, while credential-scoped availability is established.

### Retention configuration observation

The environment exposes `OPENAI_API_KEY` but no `OPENAI_ADMIN_KEY`. The official admin endpoints for organization and project retention require an admin API key, so no read-only organization/project configuration retrieval was attempted. Effective organization/project retention controls remain `UNRESOLVED`. Provider-documented behavior remains: foreground `/v1/responses` with `store=false` avoids application-state retention; abuse-monitoring retention is generally 30 days, subject to organization controls and exceptions.

### Transmission boundary qualification

The established client-side boundary remains: `https://api.openai.com/v1/responses`, TLS 1.2 minimum, no configured proxy, redirects denied. This qualification makes no claim about Internet, cloud, or OpenAI-internal intermediaries outside the controlled client boundary.
