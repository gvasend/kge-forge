# E1 WorkAuthorization Template-1 Authoritative Source Resolution 1

## Result

| Required report field | Result |
|---|---|
| `BINDING_DIGEST_SOURCE` | Deterministic digest of the exact `authenticated_inputs` object; rule exists, but the complete current authenticated input object/source set is not available as a canonical authoritative artifact. `DERIVATION_DEFINED_INPUT_MISSING`. |
| `FIELDS_VALUES_SOURCE` | No qualified Template-1 producer or complete source-to-field derivation exists. Historical authority analysis names source domains, but explicitly excludes invocation-specific values from Template-2. `MISSING_PRODUCER`. |
| `TEMPLATE1_PRODUCTION_CONTRACT` | INCOMPLETE |
| `NEXT_OPERATION` | `TEMPLATE_PRODUCTION_CONTRACT_DEFECT` |
| `AUTHORITY_REQUIRED` | YES — Architect/lifecycle authority owner must resolve which non-circular consumer/template model is to govern; no issuance is authorized. |
| `MISSING_PRODUCER` | YES |
| `CANDIDATE_3_AUTHORITY_REMAINS_VALID` | YES — no Candidate 3 was constructed; the one-candidate grant remains unconsumed. |
| `NEW_DEPENDENCY_DISCOVERED` | NO |
| `BASELINE_GRANULARITY_DEFECT` | YES — semantics-qualified and consumer-ready states are conflated. |
| `PRODUCTION_EFFECT` | NO |

**Graph classification:** `SEMANTIC_STATE_DISTINCTION_REQUIRED`.

## 1. Consumer semantics

The T1 consumer contract is implemented by `adapter/invocation_constructor.py` and called by `adapter/workauth_lifecycle.py::consume_and_issue`. It does not load a T1 JSON Schema; its Python checks are the effective acceptance contract. The separate `adapter/workauth_template_v2.py` implements a different, constraint-only `WORK-AUTHORIZATION-TEMPLATE-2` contract.

### `binding_digest`

The consumer compares `template["binding_digest"]` to `digest(authenticated_inputs)`. `digest` is SHA-256 over UTF-8 JSON serialized with lexicographically sorted keys and compact `(',', ':')` separators. Thus its meaning/type is a lowercase 64-hex digest string binding a template value projection to the exact complete invocation-specific authenticated-input map passed to the constructor. It does not establish those input values' authority and cannot be computed from a subset or summary.

The authenticated input map includes the exact required constructor members: `InvocationAttemptId`, `binding_sha256`, `canonical_binding`, `DispatchAuthorizationId`, `specific_approval_id`, `predecessor`, `eligibility`, `release_authority`, `OperationalContextId`, `runtime`, `runtime_head`, `supervisor`, `succession_head`, `profile_sha256`, `ModelPayloadDigest`, `transmission_retention`, `budget_policy`, `implementation_identity`, `audit`, `initial_state`, `ownership`, and `lifecycle_envelope`. Its internal binding checks require the invocation/dispatch, release authority, and context to agree.

This digest is not the `WorkAuthorizationId`: it is stored in the template and checked against the input map. `WorkAuthorizationId` is independently derived from the `WORK-AUTHORIZATION-1` artifact body (schema plus authenticated inputs), excluding its own ID field. The lifecycle consumer then reconstructs the artifact and typed `WorkAuthorization` and requires equality. The template digest is not itself a grant or an independent proof of source authority.

**Intended producer:** deterministic construction from a fully validated current authenticated-input object. **Current status:** the rule is defined; no complete canonical current input object with independently validated sources was located. The only issued Candidate-3 construction grant was not consumed, and Candidate 2 is not a valid source for reconstruction.

### `fields_values`

The consumer requires a mapping containing exactly every `WorkAuthorization` dataclass field. The values are copied into a `WorkAuthorization` constructor. Four fields are then overwritten by consumer code: `authorization_id` from `InvocationAttemptId`, `revision=1`, `state="INACTIVE"`, and `ownership_ledger` from the authenticated `audit` input. The implementation validates the exact key set but does not validate the types, provenance, or authority of each copied value; downstream behavior consumes those values as the typed host authorization.

The complete required key set is:

`authorization_id`, `revision`, `work_package_id`, `session_id`, `turn_id`, `read_roots`, `write_roots`, `deny_roots`, `exec_bins`, `shell`, `network`, `state`, `context_binding`, `exec_argv_allowlist`, `read_deny_roots`, `write_deny_roots`, `ownership_ledger`, `write_directory_roots`, `execution_profile`, `model_transport`, `model_transmission`, `context_projection`, `operational_binding`.

These fields are not part of the canonical WorkAuthorization artifact body and do not directly affect its `WorkAuthorizationId`. They determine the typed lifecycle/host object that must correspond to it. The template itself is separately referenced by issuance authority; consequently equality/reconstruction semantics depend on it even though `fields_values` is not included in the WorkAuthorization artifact identity.

The producer expected by T1 is therefore a component with access to authoritative sources for every effective field, plus an explicit projection rule and provenance validation. No such T1 producer exists in the qualified code. `construct_work_authorization()` consumes a supplied template; it does not create or authenticate one.

## 2–3. Producer trace and derivation status

The prior [template model correction evidence](run2_r13_preparation_2026-09-19/WORKAUTH_TEMPLATE_MODEL_CORRECTION.json) records the source analysis below and recommends the non-circular T2 constraint model. It is qualification evidence, not issuance authority. “Source identified” in that matrix does not mean a canonical field projection or producer was implemented.

| T1 field/value | Intended source and producer classification | Rule/evidence | Current finding |
|---|---|---|---|
| `schema` | Qualified consumer implementation | Literal must equal `WORK-AUTHORIZATION-TEMPLATE-1` | Deterministic constant is defined, but this does not make a template authoritative. |
| `state` | Architect lifecycle policy input | Must be `INACTIVE` | The Architect approved the initial-state semantic; field belongs to T1 contract. |
| `ownership` | Architect lifecycle policy input | Must be `NONE` | The Architect approved no initial ownership; field belongs to T1 contract. |
| `binding_digest` | DETERMINISTIC_DERIVATION | `digest(authenticated_inputs)` | Rule defined; `DERIVATION_DEFINED_INPUT_MISSING` for a complete, current canonical input object. |
| `fields_values.authorization_id` | DERIVED_IDENTITY | Consumer overwrites with `InvocationAttemptId` | No incoming value affects output, but T1 still requires the key; no placeholder/value rule is specified. |
| `fields_values.revision` | Issuance protocol / runtime state | Consumer overwrites with `1` | No incoming value affects output; key still required; no placeholder rule is specified. |
| `fields_values.work_package_id` | CURRENT_AUTHORITY_INPUT | Canonical dispatch / E1-WP-001 | Source class identified; T1 projection/validator rule not defined. |
| `fields_values.session_id`, `turn_id` | CURRENT_AUTHORITY_INPUT | Invocation identity | Source class identified; exact field mapping/provenance validation not implemented. |
| `fields_values.read_roots`, `write_roots` | CURRENT_AUTHORITY_INPUT | Released profile / dispatch policy | Authority domains identified; exact projection and consumer cross-check not implemented. |
| `fields_values.deny_roots`, `exec_bins`, `exec_argv_allowlist`, `read_deny_roots`, `write_deny_roots`, `write_directory_roots`, `shell` | CURRENT_AUTHORITY_INPUT / policy constraints | Released profile | Sources are named in the field matrix; T1 has no selector/projector or independent verification for these values. |
| `fields_values.network` | CURRENT_AUTHORITY_INPUT | Transmission policy | Source class identified; exact mapping is not defined by T1 implementation. |
| `fields_values.context_binding`, `context_projection` | DETERMINISTIC_DERIVATION / CURRENT_AUTHORITY_INPUT | Current release/context authority and current context projection | Source class named; no T1 field construction/validation function is defined. |
| `fields_values.state` | Architect lifecycle policy input | Initial state must be `INACTIVE` | Consumer overwrites it with INACTIVE; no incoming value affects output. |
| `fields_values.ownership_ledger` | CURRENT_AUTHORITY_INPUT | Audit/ownership policy; consumer overwrites it with authenticated `audit` | Value is not selected from `fields_values`, but required key is still demanded; no canonical placeholder semantics. |
| `fields_values.execution_profile` | CURRENT_AUTHORITY_INPUT | Released profile identity | Source named; exact projection and type contract absent. |
| `fields_values.model_transport`, `model_transmission` | CURRENT_AUTHORITY_INPUT | Transmission and transmission/retention authorities | Source classes named; mapping/verification absent. |
| `fields_values.operational_binding` | CURRENT_AUTHORITY_INPUT | Canonical dispatch/invocation/runtime authority | Source class named; a binding identity exists, but T1 construction/consistency rule is not specified. |
| `fields_values` as a whole | MISSING_PRODUCER | Exact WorkAuthorization dataclass projection | T1 consumer requires it; no producer, authority map completeness check, or field-specific validation exists. |

The source matrix in the historical correction marks several values as sourced from profile, dispatch, transmission, context, or audit authority. It does not provide canonical value bytes, independent source identities for every field, deterministic mapping code, freshness rules, or a field-provenance proof format. Repeated references in dispatch, WorkAuthorization, and qualification reports cannot fill that gap.

## 4. Authority analysis

The prior Architect decision approved bounded lifecycle semantics: exact current R4/E1 envelope, INACTIVE/NONE initial boundary, previously qualified transitions, duplicate/competing issuance rejection, and no expansion. This covers those policy propositions. It does not designate a producer for all 23 host dataclass values, authorize values to be copied across authority domains, define the invocation-specific template projection, or resolve T1 versus T2 consumer semantics.

No additional authority is needed merely to calculate a digest after the full authenticated input object exists; the missing issue is that the object and field projector are not established. A new or corrected template contract/consumer requires a distinct Architect/lifecycle authority decision before issuance or publication. Minimum decision: designate either (a) the constraint-only T2 template and a qualified consumer that validates each concrete WorkAuthorization field directly against its owner, or (b) a non-circular T1 production contract with independently sourced values and an explicit producer/provenance rule for every field, including how the invocation-specific binding is allowed. The current task grants neither choice, and the earlier T1 summary approval does not settle the technical contradiction.

## 5. Template-1 production contract completeness

The only complete T1 contract currently established is the consumer's *shape and checks*: schema literal, INACTIVE/NONE, digest equality to the full authenticated input object, exact dataclass-key set, then construction with four consumer-owned overrides. A complete *production* contract is not established because:

1. No canonical current `authenticated_inputs` object exists from which the digest can be calculated and independently validated.
2. No component produces T1 or resolves `fields_values` from owning authority domains.
3. The T1 consumer does not validate provenance/type/authority for most `fields_values`; it only tests keys and instantiates the dataclass.
4. The T2 constructor and correction explicitly define templates as constraint-only and exclude invocation-specific values, which conflicts with T1's per-input digest and concrete typed projection.
5. For overwritten `fields_values` members, the consumer still requires keys but provides no accepted sentinel/placeholder value rule.

Therefore `TEMPLATE1_PRODUCTION_CONTRACT = INCOMPLETE`. A compliant future producer cannot be determined without making policy/architecture choices or inventing semantics. No construction should proceed under the current T1 contract from the material found.

## 6. Graph granularity

The current `LIFECYCLE_TEMPLATE` dependency node represents “corrected WorkAuthorization lifecycle template semantics” and is already `SATISFIED`; the consumer-ready T1 object proposition is different. The production path requires both:

- `LIFECYCLE_TEMPLATE_SEMANTICS_QUALIFIED`: lifecycle constraints and transitions have technical qualification and bounded policy approval;
- `WORKAUTHORIZATION_TEMPLATE_CURRENT_CONSUMER_READY`: an authenticated, current, independently reconstructable template/consumer contract is available and accepted by the exact issuance consumer.

These propositions must be separate states because the first can be satisfied while the second is false, as the current T2/T1 split demonstrates. Classification: `SEMANTIC_STATE_DISTINCTION_REQUIRED` (and the existing one-node baseline has a granularity defect). No graph changes were made.

## 7. Actionability and Candidate-3 grant

The legitimate next operation is `TEMPLATE_PRODUCTION_CONTRACT_DEFECT`, not deterministic construction. The Architect/lifecycle authority owner must first resolve the T1/T2 contract and producer gap; this is a semantic/authority boundary decision, not a missing hash calculation. `MISSING_PRODUCER = YES`; `AUTHORITY_REQUIRED = YES` for selecting/authorizing a production contract. No template decision is issued here.

Candidate-3 construction authority `WorkAuthorizationCandidateConstructionAuthority-sha256:46a00d2c619b6e3dbbe5dc59683d3d4144f64f23b375e5fe1a959deb2b6e9c8c` remains valid and unconsumed. The prior attempt stopped before producing Candidate 3, so it did not exhaust the one-candidate grant. It must not be consumed until the resolved template inputs are authoritative and the full candidate validation sequence can run.

No new dependency was discovered: the template source gap and T1/T2 distinction are already represented in prior R4 qualification/correction evidence. No dependency status/topology changed; no Template 1, Candidate 3, or authority was constructed/issued; no lifecycle, ownership, repository, host, provider, model, or production effect occurred.
