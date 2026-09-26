# E1 WorkAuthorization Template — Canonical Object Reconciliation 1

## Outcome

| Required report field | Result |
|---|---|
| `CANONICAL_TEMPLATE_OBJECT_STATUS` | A canonical, qualification-only `WORK-AUTHORIZATION-TEMPLATE-2` object exists; the current consumer-compatible and production-authoritative `WORK-AUTHORIZATION-TEMPLATE-1` object is missing. |
| `D49797_ARTIFACT_TYPE` | `CANONICAL_TEMPLATE_OBJECT` for schema 2, qualification-only; not a Template-1 production consumer object. The separate Template-1 material is an authority/summary record referring to this identity. |
| `BINDING_DIGEST_STATUS` | MISSING from the d49797 schema-2 object and from the Template-1 summary; required at runtime by the Template-1 constructor and must equal the digest of the exact authenticated inputs. |
| `FIELDS_VALUES_STATUS` | MISSING from both; no authoritative source for the exact lifecycle dataclass field values was found. |
| `PRIOR_LIFECYCLE_TEMPLATE_STATUS` | `PRIOR_STATUS_CORRECT_DIFFERENT_PROPOSITION` for qualified lifecycle constraint semantics, but `PRIOR_STATUS_INCOMPLETE` for the consumer-compatible current template proposition. Stored status was not changed. |
| `ROOT_CAUSE` | Template-2 constraint-only authority and Template-1 invocation-specific consumer input were conflated under one identity/summary. The actual current consumer needs T1 fields that the authorized T2 model intentionally excludes. |
| `RESOLUTION_PATH` | `BASELINE_CORRECTION_REQUIRED` + `TEMPLATE_REQUALIFICATION_REQUIRED` + `ARCHITECT_TEMPLATE_AUTHORITY_REQUIRED`; no reconstruction from current evidence is authorized. |
| `CANDIDATE_3_CONSTRUCTION_AUTHORITY_STATUS` | `AUTHORITY_REMAINS_VALID` — Candidate 3 was not constructed, and the grant authorizes exactly one construction. |
| `NEW_DEPENDENCY_DISCOVERED` | NO — the missing T1 fields/template and absence from G4 were already documented. The planner edge/gate omission is a baseline defect. |
| `BASELINE_DEFECT` | YES |
| `PRODUCTION_EFFECT` | NO |

## 1. Consumer template contract

The qualified implementation is [invocation_constructor.py](../../../adapter/invocation_constructor.py), with consumption through [workauth_lifecycle.py](../../../adapter/workauth_lifecycle.py). Its `construct_work_authorization(authenticated_inputs, template)` path requires the template to provide:

| Field / property | Classification | Contract |
|---|---|---|
| `schema` | CONSUMER_REQUIRED | Exact value `WORK-AUTHORIZATION-TEMPLATE-1`. |
| `state` | CONSUMER_REQUIRED | Exact value `INACTIVE`. |
| `ownership` | CONSUMER_REQUIRED | Exact value `NONE`. |
| `binding_digest` | CONSUMER_REQUIRED | Must equal `digest(authenticated_inputs)` using canonical sorted-key compact JSON, UTF-8, SHA-256. It binds this template projection to the exact complete authenticated input set. |
| `fields_values` | CONSUMER_REQUIRED | Mapping whose keys equal exactly all `WorkAuthorization` dataclass fields; these values instantiate the typed lifecycle object, after constructor-owned fields are assigned. |
| `WorkAuthorizationTemplateId` | DERIVED / downstream-consumer-required | Not checked by `construct_work_authorization`; the separate issuance validator requires this exact ID to bind its `template_id`. The Template-2 constructor derives this from the canonical body, but that ID does not make a T2 object satisfy T1. |
| Extra template keys | OPTIONAL to T1 constructor, with no authority effect | The constructor does not enforce an exact template key set, but additional data cannot supply missing authorized values and has no accepted authority semantics here. |
| Caller/default-derived authority values | PROHIBITED by source/authority rules | A matching value or implementation default cannot establish its owning authority. |

`fields_values` must contain exactly: `authorization_id`, `revision`, `work_package_id`, `session_id`, `turn_id`, `read_roots`, `write_roots`, `deny_roots`, `exec_bins`, `shell`, `network`, `state`, `context_binding`, `exec_argv_allowlist`, `read_deny_roots`, `write_deny_roots`, `ownership_ledger`, `write_directory_roots`, `execution_profile`, `model_transport`, `model_transmission`, `context_projection`, and `operational_binding`. The constructor overwrites `authorization_id` from the authenticated `InvocationAttemptId`, `revision` with 1, `state` with `INACTIVE`, and `ownership_ledger` with the authenticated `audit` value. That overwrite behavior does not authorize the remaining values.

The relevant consumer does not itself define a template-ID hash or template-level exact key set for T1. `adapter/workauth_template_v2.py` defines a separate canonical schema, `WORK-AUTHORIZATION-TEMPLATE-2`, with an exact ten-field body: `schema`, `lifecycle_schema`, `initial_state`, `initial_ownership`, `required_binding_classes`, `policy_constraints`, `runtime_scope`, `release_scope`, `replay_policy`, and `lifecycle_envelope`. It hashes that body (excluding `WorkAuthorizationTemplateId`) using sorted-key, compact JSON. T2 intentionally has no invocation-specific `binding_digest` or concrete `fields_values`.

Validation rejects wrong T1 schema, wrong state/ownership, mismatched input digest, absent/incomplete dataclass field set, wrong issuance template ID, or failed downstream WorkAuthorization reconstruction/identity/equality. T1 and T2 are distinct contracts in the codebase; the T2 validator cannot satisfy the T1 consumer by identity resemblance.

## 2–3. Existing d49797… artifact and comparison

The exact object bytes are [R5_CORRECTED_TEMPLATE.json](run2_r13_preparation_2026-09-19/R5_CORRECTED_TEMPLATE.json). Independent calculation gives:

- object schema: `WORK-AUTHORIZATION-TEMPLATE-2`;
- `WorkAuthorizationTemplateId`: `WorkAuthorizationTemplate-sha256:d49797c4d2072c310f30f038be6fd597d3a74b2ce6a0a8a06d6dd831989ffee8`;
- identity body SHA-256: `d49797c4d2072c310f30f038be6fd597d3a74b2ce6a0a8a06d6dd831989ffee8`;
- serialized file SHA-256: `17fb2610fcff3bf398b040ba9d33c96cb4f86d8abd805dbb03be98aa52d68307`.

Thus d49797… is not merely an unbacked digest: exact canonical Template-2 bytes exist and recompute. Its provenance is R5 qualification material, however, and it is not a live G4 production template or a T1 object. The separately recorded Template-1 summary in [E1_RETENTION_LIFECYCLE_AUTHORITY_ISSUANCE_1.md](E1_RETENTION_LIFECYCLE_AUTHORITY_ISSUANCE_1.md) repeats d49797… and supplies state/ownership/lifecycle prose plus the serialization hash. It does not contain canonical T1 bytes or the required T1 fields. The R4/G4 source record explicitly says the production-consumable T1 template is absent.

| Required field / proposition | Consumer contract | d49797… exact object (T2) | Template-1 summary / historical evidence | Reconciliation |
|---|---|---|---|---|
| Schema | `WORK-AUTHORIZATION-TEMPLATE-1` | Present, but `WORK-AUTHORIZATION-TEMPLATE-2` | Summary labels record type T1; not the referenced object's schema | MISMATCH; T2 cannot pass T1 consumer |
| `state` | T1 requires `INACTIVE` | `initial_state: INACTIVE` only | Summary states initial state INACTIVE | Semantically compatible constraint, wrong field/schema shape |
| `ownership` | T1 requires `NONE` | `initial_ownership: NONE` only | Summary calls it `initial_ownership` | Semantically compatible constraint, wrong field/schema shape |
| `binding_digest` | Exact digest of invocation authenticated inputs | MISSING by T2 design | MISSING | MISSING; cannot be synthesized from summary or concrete authorization |
| `fields_values` | Exact lifecycle dataclass key set and authorized values | MISSING by T2 design | MISSING; [R4 blocked-source report](run2_r13_preparation_2026-09-19/R4_WORKAUTH_TEMPLATE_BLOCKED_SOURCE_FIELDS.json) names this source missing | MISSING / no authorized source |
| `WorkAuthorizationTemplateId` | Required by separate issuance validator | PRESENT and identity recomputes | Summary references same ID | MATCHES T2 only; does not prove T1 content |
| Lifecycle policy | Already-qualified bounded lifecycle constraints | Present as T2 policy constraints, replay, and envelope | Summary states previously qualified R4 transitions and no expansion | HISTORICAL_PRESENT as qualification; not sufficient to supply T1 concrete values |
| Runtime/release scope | Current, applicable authority | Present as R4/R5 scope in T2 | Summary says live R4/E1 | Qualification scope matches claimed envelope, but publication/current authority is absent |
| Current production publication | Authenticated current template source | No evidence of T2 publication | [G4 selection block](run2_r13_preparation_2026-09-19/LIVE_R4_G4_SELECTION_EXECUTION_BLOCKED.json) says no production-consumable T1 in G4 | MISSING / not current |

Historical R4 qualification records repeat that the production T1 object and its source `fields_values` were absent. R5 qualification demonstrates the separate T2 constraint-only design; it does not qualify T2 as input to the T1 consumer. The report in this table does not reconstruct any omitted bytes from a summary.

## 4. Prior `LIFECYCLE_TEMPLATE` status

The dependency model currently marks `LIFECYCLE_TEMPLATE` `SATISFIED` with criterion “Corrected WorkAuthorization lifecycle template semantics is authenticated, independently reconstructable, and applicable to its scope.” Its support references include R4 downstream qualification and the September 21 lifecycle issuance report. That transition established the bounded lifecycle semantics and a qualified Template-2 identity for R4 qualification. It did not establish a current consumer-compatible T1 object published in G4.

Classifications:

- `PRIOR_STATUS_CORRECT_DIFFERENT_PROPOSITION`: the restricted lifecycle semantics and canonical T2 constraint object were technically qualified.
- `PRIOR_STATUS_INCOMPLETE`: T1 consumer compatibility, current production availability, and required field-value provenance were not established.
- `QUALIFICATION_PIPELINE_DEFECT`: the prior status treated a summary/semantic approval as though it supplied the exact runtime consumer object.
- `CANONICAL_OBJECT_MISSING`: the T1 object required by the consumer is absent; T2 bytes do exist.
- `BASELINE_GRANULARITY_DEFECT`: lifecycle-policy qualification and production-consumable template availability were represented by one node/status.

The historical report and graph remain unchanged. For current consumer use, the stored `SATISFIED` status cannot be relied on as proof that a T1 object exists or validates.

## 5. Minimum resolution path

No deterministic construction is justified from the current evidence. The missing T1 fields carry lifecycle execution values; the T2 model deliberately excludes invocation-specific concrete values, while the R4 blocked-source evidence prohibits deriving them from the concrete WorkAuthorization or defaults. The implementation also contains two incompatible template interfaces (T1 value projection and T2 constraint-only contract).

The minimum legitimate next path is:

1. Architect/lifecycle authority owner resolves which template contract is authoritative for current R4 consumption: adapt/qualify a consumer for the already qualified constraint-only T2 model, or explicitly authorize a T1 source with independent authority for every required value and resolve its invocation-binding semantics.
2. If the result requires a new or adapted canonical template, obtain distinct authority to construct its candidate and distinct authority to issue/publish it. Technical qualification or d49797… alone does not grant either.
3. Validate the exact candidate template against the selected consumer before any issuance/publication. For the existing T1 consumer this includes required schema/state/ownership, exact `binding_digest`, all dataclass `fields_values`, and independent source/provenance validation. For T2, validate its exact constraint schema/identity and qualify the consumer adaptation separately.
4. Issue/publish only after the proper Architect decision, preserving R4/G4 immutability until separately authorized.

Classifications: `EXISTING_CANONICAL_TEMPLATE_LOCATED` applies only to the qualification-only T2 object; `DETERMINISTIC_TEMPLATE_CONSTRUCTION_REQUIRED` is not currently authorized or source-grounded; `ARCHITECT_TEMPLATE_AUTHORITY_REQUIRED`, `TEMPLATE_REQUALIFICATION_REQUIRED`, and `BASELINE_CORRECTION_REQUIRED` apply to resolving the live consumer contract.

## 6. Candidate-3 construction grant

The grant `WorkAuthorizationCandidateConstructionAuthority-sha256:46a00d2c619b6e3dbbe5dc59683d3d4144f64f23b375e5fe1a959deb2b6e9c8c` is explicitly limited to exactly one Candidate 3 construction and qualification. The prior attempt stopped at input validation and produced no candidate bytes or identity. It did not consume the single construction. Therefore `AUTHORITY_REMAINS_VALID`, subject to its stated scope; no alteration or extension is inferred.

## 7. Planner consequence

The stored graph still says `LIFECYCLE_TEMPLATE=SATISFIED`; mechanically traversing the unchanged status set yields `STRUCTURAL_FRONTIER = [APPLICABILITY_RECONCILIATION]` on the relevant dependency path. That is only the stored-graph result. The evidence-aware view treats the T1 consumer proposition as unsatisfied, without changing stored state:

- corrected local `STRUCTURAL_FRONTIER = [LIFECYCLE_TEMPLATE, APPLICABILITY_RECONCILIATION]` — template status is disputed by consumer-contract evidence; applicability reconciliation remains blocked for the historical WorkAuthorization/current envelope.
- `ACTIONABLE = []`.
- `BLOCKED_FRONTIER = [LIFECYCLE_TEMPLATE, APPLICABILITY_RECONCILIATION]` — neither issue can be resolved by deterministic construction from available authority. Template resolution requires the contract/authority decision above; Candidate 3 remains gated on that prerequisite.
- Downstream blocked nodes: `[LIFECYCLE_ISSUANCE, CONCRETE_WORKAUTH, INACTIVE_ISSUANCE, ACTIVATION, ACTIVE_RECOVERY, DISPATCHER_ELIGIBILITY, HOST_CONSTRUCTION, MODEL_REQUEST_READY]` — these cannot be acted on until the canonical template/consumer issue and exact applicable WorkAuthorization are resolved.

This is an analytical planner correction only. No node status, dependency edge, or actionability state was changed. The missing template is an already recorded blocker, so no new dependency was discovered in this reconciliation; the fact that the baseline does not distinguish qualified template semantics from consumer-ready template input is a baseline defect.

No template was constructed or issued. Candidate 2 and Candidate 3 remain untouched; there was no lifecycle, ownership, repository, host, payload, provider, model, or other production effect.
