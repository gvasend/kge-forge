# E1 WorkAuthorization Consumer Contract Reconciliation 1

## Outcome

`CONSUMER_CONTRACT_IDENTIFIED`; Candidate 2 is preserved and is invalid for the qualified consumer.

| Required report field | Result |
|---|---|
| `FAILED_CANDIDATE_PRESERVED` | YES |
| `CANONICAL_CONSUMER_CONTRACT_IDENTIFIED` | YES |
| `ROOT_CAUSE` | Candidate 2 uses a proposal-summary schema rather than the consumer's exact `WORK-AUTHORIZATION-1` artifact, omits `WorkAuthorizationId`, and lacks the constructor's complete authenticated input set. |
| `PREVIOUS_QUALIFICATION_INTERPRETATION` | `SEMANTIC_PASS_ONLY`; schema, canonical identity, and actual consumer acceptance were not demonstrated. |
| `CONSTRUCTION_AUTHORITY_STATUS` | `NEW_CONSTRUCTION_AUTHORITY_REQUIRED` |
| `CANDIDATE_3_SPECIFICATION_READY` | YES (specification only; no construction performed) |
| `NEW_DEPENDENCY_DISCOVERED` | NO |
| `BASELINE_DEFECT` | YES — qualification treated semantic/binding comparison as candidate readiness without gating on the actual consumer contract. |
| `PRODUCTION_EFFECT` | NO |

## Preserved failed candidate

The immutable artifact [Candidate 2](E1_CURRENT_WORKAUTHORIZATION_CANDIDATE_2.json) remains exactly:

`WorkAuthorizationCandidate-sha256:72c1d3882fb94367c8062663036a9b322cd23eb4bc51cd564b8b60a060102475`

The qualified consumer's `identity()` rejected it with `ConstructionDenied: unknown WorkAuthorization schema`. Its file has `record_type` and `schema_version`, but no top-level `schema`; it uses lowercase `workauthorization_id` rather than `WorkAuthorizationId`, and it is a summary with top-level `bindings`, not the canonical authenticated input object. Classify it `CONSUMER_INVALID / REJECTED_FOR_ISSUANCE`. It is not repaired, regenerated, or rehashed here. The prior issuance attempt created neither issuance authority nor a WorkAuthorization.

## Canonical consumer contract

The authoritative implementation is [invocation_constructor.py](../../../adapter/invocation_constructor.py), consumed by [workauth_lifecycle.py](../../../adapter/workauth_lifecycle.py). Its constraints, rather than Candidate 2's representation, define the accepted form.

### Canonical authority artifact

The serialized artifact is a JSON object with exactly these top-level members:

| Field | Contract class | Required meaning/check |
|---|---|---|
| `schema` | CONSUMER_REQUIRED | Exact string `WORK-AUTHORIZATION-1`. |
| `InvocationAttemptId` | CONSUMER_REQUIRED | Exact invocation attempt identifier; must equal the same value in `canonical_binding`. |
| `binding_sha256` | CONSUMER_REQUIRED | SHA-256 of the canonical serialized `canonical_binding`. |
| `canonical_binding` | CONSUMER_REQUIRED | Canonical invocation binding; its dispatch, release-authority, and OperationalContext references must agree with the sibling fields below. |
| `DispatchAuthorizationId` | CONSUMER_REQUIRED | Exact dispatch authority identifier; must equal the binding's `DispatchAuthorizationId`. |
| `specific_approval_id` | CONSUMER_REQUIRED | Specific approval reference. |
| `predecessor` | CONSUMER_REQUIRED | Predecessor/attempt-chain reference. |
| `eligibility` | CONSUMER_REQUIRED | Eligibility evidence/value consumed by the existing constructor. |
| `release_authority` | CONSUMER_REQUIRED | Release authority identity; must equal `canonical_binding.bindings.release_authority`. |
| `OperationalContextId` | CONSUMER_REQUIRED | Current operational-context identity; must equal `canonical_binding.bindings.OperationalContextId`. |
| `runtime` | CONSUMER_REQUIRED | Runtime identity. |
| `runtime_head` | CONSUMER_REQUIRED | Runtime-head authority reference. |
| `supervisor` | CONSUMER_REQUIRED | Supervisor authority/reference. |
| `succession_head` | CONSUMER_REQUIRED | Supervisor-succession head reference. |
| `profile_sha256` | CONSUMER_REQUIRED | Profile identity. |
| `ModelPayloadDigest` | CONSUMER_REQUIRED | Exact model-payload identity. |
| `transmission_retention` | CONSUMER_REQUIRED | Applicable transmission/retention authority binding. |
| `budget_policy` | CONSUMER_REQUIRED | Applicable budget-policy binding. |
| `implementation_identity` | CONSUMER_REQUIRED | Implementation/runtime identity binding. |
| `audit` | CONSUMER_REQUIRED | Audit binding/state reference; also used as the constructed lifecycle ledger value. |
| `initial_state` | CONSUMER_REQUIRED | Exact value `INACTIVE`. |
| `ownership` | CONSUMER_REQUIRED | Exact value `NONE`. |
| `lifecycle_envelope` | CONSUMER_REQUIRED | Lifecycle envelope identifier; the current contract uses `WORK-AUTHORIZATION-1`. |
| `WorkAuthorizationId` | DERIVED, serialized as required | `WorkAuthorization-sha256:` plus the canonical digest of every artifact member except `WorkAuthorizationId` itself. Caller-supplied ID is checked, not trusted. |

There are no optional or additional members in the constructor input set: `_body()` requires the input key set to equal the 22 named authenticated inputs exactly, and `artifact()` adds only `schema` and the derived `WorkAuthorizationId`. The constructor does not define detailed JSON sub-schemas for every nested value. Types are therefore constrained by JSON representability and by the actual comparisons/digest use shown in implementation; stronger type requirements must come from the authoritative upstream schema/template, not be guessed here.

### Binding, serialization, and identity rules

`canonical(value)` is JSON serialization with sorted object keys and separators `(',', ':')`, UTF-8 encoded. `binding_sha256` is SHA-256 of those canonical `canonical_binding` bytes. Before construction, the consumer verifies:

1. exact authenticated-input key set;
2. `initial_state == "INACTIVE"` and `ownership == "NONE"`;
3. canonical binding digest matches `binding_sha256`;
4. binding invocation and dispatch IDs match the top-level values;
5. binding release authority and OperationalContext IDs match the top-level values.

The artifact is `{ "schema": "WORK-AUTHORIZATION-1", ...authenticated_inputs }`, then `WorkAuthorizationId` is calculated over that full object before the ID member is inserted. `identity()` recomputes that value and rejects an unknown schema or mismatch. No input ordering is semantically significant; canonical output ordering is sorted-key JSON. No extra fields are accepted by the constructor input set.

### Template and lifecycle-consumer requirements

`construct_work_authorization()` additionally requires a template whose `schema` is `WORK-AUTHORIZATION-TEMPLATE-1`, whose `state` is `INACTIVE`, whose `ownership` is `NONE`, and whose `binding_digest` equals `digest(authenticated_inputs)`. Its `fields_values` keys must exactly equal all `WorkAuthorization` dataclass fields in [governed_host.py](../../../adapter/governed_host.py): `authorization_id`, `revision`, `work_package_id`, `session_id`, `turn_id`, `read_roots`, `write_roots`, `deny_roots`, `exec_bins`, `shell`, `network`, `state`, `context_binding`, `exec_argv_allowlist`, `read_deny_roots`, `write_deny_roots`, `ownership_ledger`, `write_directory_roots`, `execution_profile`, `model_transport`, `model_transmission`, `context_projection`, and `operational_binding`. The constructor sets `authorization_id` from `InvocationAttemptId`, `revision=1`, `state="INACTIVE"`, and `ownership_ledger` from `audit`.

`workauth_lifecycle.consume_and_issue()` verifies the supplied bytes' SHA-256, parses JSON, validates the canonical WorkAuthorization identity, independently reconstructs both the artifact and typed `WorkAuthorization` from authenticated inputs plus template, and requires exact object equality. It then requires the typed state to remain INACTIVE with a ledger and only then delegates to `issue_inactive()`. This equality check makes actual reconstruction/consumer acceptance a mandatory gate; a merely compatible summary object is insufficient.

The separate issuance-authority consumer requires schema `WORKAUTH-ISSUANCE-AUTHORITY-1` and exactly `schema`, `template_id`, `workauthorization_id`, `invocation_attempt_id`, `dispatch_id`, `runtime`, `release_context`, `architect_decision`, `scope`, and `replay`, plus derived `IssuanceAuthorityId`. Scope must be `EXACT_SINGLE_WORKAUTHORIZATION_INACTIVE`, replay must be `REJECT`, and all candidate/template/invocation/dispatch/runtime/release bindings are checked. This is distinct from the WorkAuthorization artifact schema.

### Rejection conditions established by implementation

The consumer rejects unknown schema, incomplete or extra authenticated-input keys, non-INACTIVE or owned initial state, mismatched canonical binding digest, mismatched invocation/dispatch/release/context bindings, incorrect derived WorkAuthorizationId, wrong template schema/state/ownership/binding digest, incomplete template field set, mismatched reconstruction bytes/object, and invalid initial typed state/ledger. Issuance validation separately rejects wrong schema/fields, expanded scope, replay policy other than REJECT, identity mismatch, or any binding mismatch.

## Three-way representation comparison

Historical object: [R4_FINAL_REPLACEMENT_WORKAUTH.json](run2_r13_preparation_2026-09-19/R4_FINAL_REPLACEMENT_WORKAUTH.json), identity `WorkAuthorization-sha256:bc53d20ea0383febbd7ce1c10e2e00b2461a722942b853f43ea5001b42976c61`. Candidate 2: the immutable candidate above. The historical artifact has the exact consumer schema and complete constructor field set; it is the shape consumed by the lifecycle bridge. Candidate 2 is not that shape.

| Consumer field/semantic | Historical valid artifact | Candidate 2 | Consumer result |
|---|---|---|---|
| `schema = WORK-AUTHORIZATION-1` | HISTORICAL_PRESENT / MATCH | MISSING (`record_type`, `schema_version` instead) | CONSUMER_REQUIRED; immediate unknown-schema rejection |
| `WorkAuthorizationId` | HISTORICAL_PRESENT / MATCH | MISSING (lowercase `workauthorization_id` contains a Candidate ID) | CONSUMER_REQUIRED + DERIVED; mismatch of field name and identity namespace |
| InvocationAttemptId | HISTORICAL_PRESENT | CANDIDATE_PRESENT as nested `invocation`; not canonical top-level field | CONSUMER_REQUIRED; MISSING in accepted representation |
| `binding_sha256`, `canonical_binding` | HISTORICAL_PRESENT | MISSING | CONSUMER_REQUIRED; no independently verifiable binding projection |
| DispatchAuthorizationId | HISTORICAL_PRESENT | CANDIDATE_PRESENT as `dispatch` summary/reference | CONSUMER_REQUIRED; canonical field/binding absent |
| specific approval, predecessor, eligibility | HISTORICAL_PRESENT | MISSING as contract fields (some scope/task prose is not equivalent) | CONSUMER_REQUIRED |
| release authority, OperationalContextId | HISTORICAL_PRESENT | CANDIDATE_PRESENT as lowercase summary fields | CONSUMER_REQUIRED; stale/incompatible binding remains to be evaluated against current values after construction |
| runtime, runtime_head, supervisor, succession_head | HISTORICAL_PRESENT | runtime present; the other canonical references MISSING | CONSUMER_REQUIRED |
| profile, ModelPayloadDigest | HISTORICAL_PRESENT | profile/payload present as summary objects | CONSUMER_REQUIRED; canonical scalar bindings absent |
| transmission_retention, budget_policy, implementation_identity | HISTORICAL_PRESENT | only partial/renamed nested summaries, not contract fields | CONSUMER_REQUIRED |
| audit, initial_state, ownership, lifecycle_envelope | HISTORICAL_PRESENT | initial-state/ownership concepts present but renamed; audit/lifecycle envelope absent | CONSUMER_REQUIRED; values are not accepted by field-name resemblance |
| exact top-level field set | HISTORICAL_PRESENT; the constructor-required fields are present | MISMATCH; unrelated extra summary fields and required canonical fields absent | Exact key-set check required |
| canonical identity | Historical ID is consistent with the consumer's WorkAuthorization identity semantics | Candidate uses `WorkAuthorizationCandidate-...` and does not have `WorkAuthorizationId` | Candidate's own digest is not a WorkAuthorization identity |
| typed template projection | Historical artifact is paired with qualified template/consumer evidence | Candidate was not shown to reconstruct the full `WorkAuthorization` dataclass | Required for lifecycle acceptance; Candidate 2 qualification did not establish it |

The historical artifact's presence of `schema`, exact required authority-input names, and a derived `WorkAuthorizationId` explains why it is recognizable by the consumer. It does not establish current applicability of its old identities. Candidate 2's intended scope and least-authority semantics may be semantically similar, but similarity does not satisfy schema, binding, or identity requirements.

## Qualification gap and prior PASS

The Candidate-2 report [E1_CURRENT_WORKAUTHORIZATION_CANDIDATE_2.md](E1_CURRENT_WORKAUTHORIZATION_CANDIDATE_2.md) said “Qualification PASS” based on semantic scope/difference assertions and listed current bindings. It did not show:

- validation against the actual `WORK-AUTHORIZATION-1` schema;
- exact authenticated-input key-set validation;
- deterministic construction with the qualified constructor;
- canonical `WorkAuthorizationId` recomputation;
- independent canonical serialization reproduction;
- typed template projection construction;
- successful call through the exact consumer acceptance path.

The subsequent non-effecting consumer probe failed at the first schema gate, before semantic binding or lifecycle acceptance. Thus the prior PASS must be narrowed to `SEMANTIC_PASS_ONLY` (intended bounded semantics/no expansion), not candidate qualification or consumer acceptance. This is a `QUALIFICATION_PIPELINE_DEFECT` and `CANDIDATE_CONSTRUCTION_DEFECT`; presentation of Candidate 2 as qualified/ready was unsupported. The actual lifecycle consumer correctly failed closed. No historical report is rewritten.

Canonical WorkAuthorization consumer acceptance must be a mandatory pre-Architect-review qualification gate: schema and exact field set, canonical identity/serialization, template reconstruction, and actual consumer acceptance must all pass on the exact immutable candidate bytes before it is called qualified for issuance review. Semantic and authority qualification remain separate later gates.

## Construction-authority status

The issued [candidate-construction authority](E1_CURRENT_WORKAUTHORIZATION_CONSTRUCTION_AUTHORITY_1.json) says `EXACT_SINGLE_NEW_WORKAUTHORIZATION_CANDIDATE`, `candidate_only: true`, and `issuance_authority: false`; the corresponding Architect decision authorized construction and qualification of exactly one candidate and expressly did not authorize issuance or reconstruction. That one construction produced Candidate 2. It was not a reusable-until-success grant, and later approval to issue the exact immutable Candidate 2 did not authorize changing it or producing a replacement. Therefore:

`CONSTRUCTION_AUTHORITY_STATUS = NEW_CONSTRUCTION_AUTHORITY_REQUIRED`

Candidate 3 may not be built under the consumed single-candidate authority. A new explicit construction authority must name the bounded replacement construction. No such authority is requested or issued here.

## Candidate-3 construction specification (not executed)

The construction protocol is defined, but all runtime authority inputs must be revalidated from their owning current sources at execution time. Do not copy values out of Candidate 2 to fill canonical fields. The exact sequence is:

1. Obtain new Architect authority for exactly one replacement candidate, with candidate-only scope and no issuance, consumption, lifecycle, ownership, repository, host, provider, or execution effect.
2. Resolve the constructor's exact 22-field authenticated input set from current authoritative records: `InvocationAttemptId`, `binding_sha256`, `canonical_binding`, `DispatchAuthorizationId`, `specific_approval_id`, `predecessor`, `eligibility`, `release_authority`, `OperationalContextId`, `runtime`, `runtime_head`, `supervisor`, `succession_head`, `profile_sha256`, `ModelPayloadDigest`, `transmission_retention`, `budget_policy`, `implementation_identity`, `audit`, `initial_state`, `ownership`, `lifecycle_envelope`. Require INACTIVE/NONE and the binding consistency rules stated above. Missing or stale source means stop.
3. Resolve the exact current `WORK-AUTHORIZATION-TEMPLATE-1`; verify its `fields_values` exactly match the typed dataclass fields, initial state/ownership, and authenticated-input digest. Do not synthesize missing values from a different domain.
4. Deterministically construct the canonical `WORK-AUTHORIZATION-1` artifact; derive `WorkAuthorizationId` from the artifact body excluding that ID; serialize with sorted keys and compact separators.
5. Run schema/exact-key validation, canonical byte and identity recomputation, template validation, and the actual lifecycle consumer's independent reconstruction/equality acceptance check against those exact bytes. Do this in a non-effecting validation mode; do not call the issuance/effectful boundary.
6. Only after consumer acceptance, separately qualify semantics, exact current authority bindings, scope/lineage/freshness, least authority, lifecycle/cancellation/recovery/replay properties, and no expansion. Freeze the new identity and report all evidence.
7. Submit that immutable candidate to the Architect for review. Any edit requires a new identity and new construction authority; no approval is inferred.
8. If approved, obtain a new candidate-specific issuance authority, then issue only the exact approved candidate under the issuance consumer.

This task defines the construction and validation contract only. It has not resolved the current presence, provenance, freshness, or applicability of every field source for a future candidate, and does not authorize their resolution by copying Candidate 2.

## Dependency/planner consequence

No dependency node or edge is changed here, and no candidate is treated as satisfying `CONCRETE_WORKAUTH` or lifecycle issuance. The baseline's prior construction/qualification flow has a gate omission: consumer acceptance must precede candidate-ready/Architect issuance review. Since the actual consumer contract already exists in the qualified implementation, this reconciliation discovers no new domain prerequisite; it exposes a missing mandatory validation stage in the qualification pipeline. A future planning baseline may need to represent that gate explicitly if its existing satisfaction criteria do not already require it, but this report does not modify topology or status.

No WorkAuthorization, issuance authority, lifecycle event, ownership record, repository effect, host execution, payload transmission, provider request, or E1 production effect was created.
