# E1 WorkAuthorization Production Contract Decision 1

## Result

| Field | Determination |
|---|---|
| `PRODUCTION_ARCHITECTURE` | `ADOPTED` for formal validation by the Architect decision in this task; adoption does not issue or publish any artifact or implementation authority. |
| `FIELD_SOURCE_GAPS` | `canonical_binding` / `binding_sha256`; current `specific_approval_id`; current eligibility evidence; current runtime-head, supervisor and succession-head authorities; audit/ownership namespace; invocation session/turn values; exact current context-binding/projection source. |
| `FIELD_MAPPING_GAPS` | Exact binding-input-to-22-input projection; all effective `fields_values` mappings and types; consumer-overwritten required-key semantics; T1 identity; T2-to-T1 lifecycle-envelope projection; provider transmission/retention composition. |
| `PURE_VALIDATION_REQUIRED` | `YES` |
| `VALIDATOR_IMPLEMENTATION_AUTHORITY` | `ARCHITECT_REQUIRED` |
| `PLANNER_STATE_DISTINCTIONS` | `LIFECYCLE_TEMPLATE_SEMANTICS_QUALIFIED`; `WORKAUTHORIZATION_BINDING_INPUT_CURRENT`; `WORKAUTHORIZATION_TEMPLATE1_CONSUMER_READY`; `WORKAUTHORIZATION_CANDIDATE_CONSUMER_VALIDATED`; `WORKAUTHORIZATION_ISSUANCE_AUTHORIZED`. |
| `TEMPLATE1_CONSTRUCTION_READY` | `NO` |
| `CANDIDATE_3_AUTHORITY_REMAINS_VALID` | `YES` |
| `NEW_DEPENDENCY_DISCOVERED` | `NO` |
| `BASELINE_DEFECT` | `YES` — the current planner/qualification distinction does not represent the separately required input, template-consumer, candidate-validation, and issuance states. |
| `PRODUCTION_EFFECT` | `NO` |

No binding-input object, Template-1, Candidate 3, validator implementation, authority, or dependency update was created. The existing artifacts remain unchanged.

## 1. Remaining Template-1 production gaps

The accepted architecture is acyclic if the binding-input object is a provenance/composition record only. It must resolve to owning current sources before projection. It cannot promote a reference, choose a value, or be used as authority for itself. The executable Template-1 constructor contract currently has 22 exact `authenticated_inputs` keys and requires `fields_values` to contain the exact `WorkAuthorization` dataclass key set. The constructor checks shape and selected internal consistency, but does not verify the authority or provenance of most field values. The adopted production contract must add those checks before construction.

### Authenticated-input values

| Consumer input | Outstanding source or mapping gap | Minimum resolution |
|---|---|---|
| `InvocationAttemptId` | Current invocation identity is referenced, but the binding-input producer must resolve the owning canonical invocation and verify current attempt allocation. | Bind the exact current invocation record and define its identity resolver/currentness check. |
| `binding_sha256`, `canonical_binding` | No canonical current binding-input bytes/object is established; the sibling InvocationCandidate and OperationalBinding carry correspondence references, not the required canonical binding object. | Establish the canonical binding representation and its owning source/derivation; hash those exact bytes. Exclude final sibling identities to prevent recursion. |
| `DispatchAuthorizationId` | Current dispatch identity exists, but the consumer field's exact encoding/mapping from the current dispatch authority is unspecified. | Define and validate the one-to-one projection from canonical dispatch authority identity. |
| `specific_approval_id` | The exact current Architect decision identifier to place in this field has not been established. | Identify the applicable issued decision record and define its field projection; do not substitute a prose decision or another authority ID. |
| `predecessor` | `R12_HISTORY` is a reference; current predecessor/attempt-allocation proof and serialized value are not bound into this input map. | Resolve the authoritative attempt-chain record and define its canonical predecessor value, or explicitly define the first/current-attempt representation. |
| `eligibility` | No current canonical eligibility evidence/value is bound. Dispatcher eligibility has not been established by the listed references alone. | Establish the exact current eligibility proposition and producer/evidence record before projection. |
| `release_authority` | Current ReleaseAuthority identity is available. The binding-input still needs a source resolver and currentness check. | Reference its canonical owning artifact; verify exact active R4/G4 applicability at construction. |
| `OperationalContextId` | Current context identity is available as a reference, while the binding-input needs source resolution and applicability validation. | Resolve the canonical context record and verify the context/release/dispatch agreement. |
| `runtime` | Current runtime identity is known; exact field semantics are not yet tied to an authenticated runtime source in this producer contract. | Bind the current runtime object and define identity extraction. |
| `runtime_head` | The cited older runtime-head reference does not establish a current owning R4/G4 runtime-head authority. | Locate or establish the current authorized runtime-head record; no copied digest can fill it. |
| `supervisor`, `succession_head` | Historical WorkAuthorization references do not establish current R4/G4 supervisor/succession authority objects. | Resolve current canonical supervisor and succession-head sources, including applicability/freshness. |
| `profile_sha256` | Several distinct current identities exist (profile content, profile-root candidate/authority, ReleasedProfileAuthority, ProgrammerProfile); the expected value is unspecified. | Choose the consumer's exact semantic referent in the schema and define a single projection to it. Do not interchange identity domains. |
| `ModelPayloadDigest` | Approved payload content identity exists, with a separate payload-authority identity. | Define that this field projects the approved payload content digest, resolve its owning immutable bytes, and validate the authority binding. |
| `transmission_retention` | Transmission and retention are separate authorities; no canonical combined field format/rule exists. | Define a typed composition that references both exact authorities and preserves unresolved retention behavior. |
| `budget_policy` | Current StatusBudgetAuthority exists, but it is unclear whether this field is the authority identity, policy body, or a projection. | Define the expected type and canonical policy-value mapping; bind the policy record as provenance. |
| `implementation_identity` | Runtime identity is available, but the exact relationship between implementation identity and runtime identity has not been qualified for this field. | Define whether it is the runtime digest or a distinct implementation identity and provide the corresponding authenticated source. |
| `audit` | Current OperationalBinding explicitly says `CANONICAL_AUDIT_NAMESPACE_UNBOUND_UNUSED`; no current audit namespace/store identity is established. | Resolve the authorized audit namespace/reference before this field can seed the ownership ledger. Do not assume a future ledger state. |
| `initial_state`, `ownership` | Architect lifecycle decision establishes `INACTIVE` and `NONE`. | Map those exact approved constants and validate against qualified T2 semantics. |
| `lifecycle_envelope` | T2's reusable lifecycle envelope and T1's expected value are different representations; no projection rule is defined. | Define a deterministic projection from the exact qualified T2 lifecycle semantics to the T1 consumer value. |

For all 22 inputs, the binding-input schema also needs a field-level provenance entry: source domain, canonical record identity, independently recomputed content identity, resolver/projection rule version, scope, lineage, and freshness. References should be preferred over copied values where the consumer contract allows it. A reference is usable only after the source record is independently authenticated.

### `fields_values` outputs

The consumer requires 23 keys corresponding to `WorkAuthorization` fields. The values below remain unprojectable until the source map and rules are completed:

| Output field(s) | Remaining source/mapping gap |
|---|---|
| `authorization_id` | Consumer overwrites it from `InvocationAttemptId`; Template-1 still requires a key, but no canonical ignored-input/sentinel rule is specified. |
| `revision` | Consumer overwrites it with `1`; required input key has no defined sentinel/value rule. |
| `work_package_id` | E1-WP-001/dispatch is the source domain, but exact canonical value and type projection are not specified. |
| `session_id`, `turn_id` | Invocation source class is named, but current values and field mapping are absent. |
| `read_roots`, `write_roots` | Profile/repository authority sources are identifiable; exact typed value projection and host-equivalence validation are not defined in the consumer. |
| `deny_roots`, `read_deny_roots`, `write_deny_roots` | Profile constraints are source classes; exact values, normalization, overlap semantics, and validation mapping are missing. |
| `exec_bins`, `exec_argv_allowlist`, `shell`, `network` | Profile/provider/transmission policy domains are known, but there is no qualified deterministic mapping to these host fields; in particular `exec_bins` cannot be inferred from an argv allowlist. |
| `state` | Consumer overwrites with `INACTIVE`; required key has no canonical ignored-input/sentinel rule. |
| `context_binding`, `context_projection` | Current context/projection identity is referenced, but no typed canonical value projection and verification contract exists. |
| `ownership_ledger` | Consumer overwrites from `audit`; current audit namespace source is missing, and the required input key semantics are undefined. |
| `write_directory_roots` | Profile/repository policy source exists, but the exact typed directory-grant projection and validation rule are absent. |
| `execution_profile` | It is not established whether this means ProgrammerProfile content identity, ReleasedProfileAuthority identity, or another profile binding. |
| `model_transport`, `model_transmission` | Provider, transmission, retention and clearance authorities exist separately; exact host-field encodings and composition are undefined. |
| `operational_binding` | A current OperationalBinding identity is referenced, but the field's accepted value type and required consistency checks are not specified. |

The minimum completion decision is not to pick convenient values. It is to approve/qualify one exact source-to-field mapping contract for every row above, with explicit types, canonical encodings, source authority, and verification rules. Where the source itself is missing, that source authority must first be resolved. The binding digest algorithm can remain deterministic SHA-256 over canonical sorted-key compact JSON for the exact resolved `authenticated_inputs` object; the present blocker is its incomplete input bytes/source chain.

Template-1 also needs its own canonical identity rule and consumer validation rule. The Template-2 identity algorithm applies to Template-2 only. The binding-input identity is separate from `binding_digest`; the latter must cover exactly the consumer-defined resolved input map, not arbitrary provenance-wrapper fields.

## 2. Pure validation boundary

### Minimum change

Refactor the current pre-issuance path into one pure internal validator, then expose the requested public validation operation:

```text
_validate_for_issuance(candidate_bytes, candidate_digest, inputs,
                       template, current_state) -> ValidationResult

validate_for_issuance(candidate, current_state) -> ValidationResult
    # resolves authenticated inputs/template and calls the same helper

consume_and_issue(candidate, current_state, issuance_authority, ...):
    result = _validate_for_issuance(...)
    require result.valid and applicable issuance authority
    recheck mutable current-state generation under the issuance lock
    -> existing issue/effect path
```

The helper must own all existing pre-effect checks in one place: exact candidate-byte digest; parsing; schema and `WorkAuthorizationId` recomputation; exact authenticated-input key set and source verification; template identity/schema/state/ownership/binding-digest checks; deterministic reconstruction of both artifact and typed WorkAuthorization; byte/object equality; INACTIVE/unowned boundary; current-state and scope/freshness checks. It returns a structured result with failures and verified bindings. It must not call issuance, lifecycle, ownership, audit-write, repository, host, or provider functions. The effect path must use that same result and revalidate current mutable state atomically before issuance to avoid a validation-to-use race.

### Current code-path finding

`adapter/invocation_constructor.py` supplies pure primitives (`identity`, `construct_artifact`, `construct_work_authorization`). It checks exact input keys, binding digest and selected correspondence fields, then constructs a typed `WorkAuthorization`; it does not authenticate field provenance or validate every policy binding. `adapter/workauth_lifecycle.py::consume_and_issue()` verifies bytes/identity, reconstructs and compares the typed object, checks initial state, then immediately calls `issue_inactive()`. There is no validation-only branch, and no shared `ValidationResult` gate. Thus, at the source level, both paths cannot currently be shown to use a single authoritative full validation routine.

Additionally, `workauth_lifecycle.py` imports `.invocation_issuance`, but that module is not present in the active `adapter/` tree. A historical copy under a prior candidate tree is not the current implementation. This prevents execution-level proof of the bridge/effect boundary in the current checkout. The code-path conclusion is limited to the visible source: pre-issuance checks precede a direct issuance call; no pure full-consumer acceptance entrypoint exists.

### Required qualification tests

Before the new boundary can be relied upon, test that:

1. For identical candidate, template, source inputs and current-state snapshot, `validate_for_issuance()` and the pre-effect stage of `consume_and_issue()` produce identical accept/reject decisions and equivalent binding results.
2. Valid and malformed candidates (bad byte hash, schema, ID, keys/types, binding digest, template ID, state/ownership, stale or mismatched authority bindings) are rejected/accepted identically by the shared validator.
3. Validation PASS leaves the candidate unissued and does not invoke the issuance function; validation failure has the same zero-effect property.
4. Lifecycle state, ownership ledger, audit/issuance records, repository tree, host state, and provider/model counters are byte/state-identical before and after both validation PASS and FAIL.
5. A validated candidate remains only a validation result: no issued identity/state or ownership appears until a separately authorized consume/issue operation.
6. The effect path uses the exact same validation helper, checks the exact applicable issuance authority, and rechecks generation/currentness under a lock or equivalent atomic boundary before effects.

These are qualification requirements, not tests run in this task.

## 3. Authority to implement

`VALIDATOR_IMPLEMENTATION_AUTHORITY = ARCHITECT_REQUIRED`.

The current profile's write grants are limited to the listed E1-WP-001 task paths; `adapter/` is not an authorized write root. The Candidate-3 construction authority is candidate-only and expressly excludes implementation change, issuance, lifecycle, ownership, repository, host, provider, model, and production effects. Neither grants permission to refactor `adapter/workauth_lifecycle.py` or add the validation API. The implementation change therefore needs a distinct, narrowly scoped Architect implementation decision covering the specific consumer validation seam, associated non-effecting tests, and qualification only. It must not authorize invocation or production execution.

## 4. Planner state distinctions

The planner must keep these propositions distinct:

| State proposition | What satisfaction proves | What it does not prove |
|---|---|---|
| `LIFECYCLE_TEMPLATE_SEMANTICS_QUALIFIED` | Reusable Template-2 lifecycle constraints have qualified semantics and applicable policy approval. | No invocation-specific values, current binding inputs, or consumer-ready Template-1. |
| `WORKAUTHORIZATION_BINDING_INPUT_CURRENT` | Every input source is independently authenticated, complete, current, in scope, and mapped by a defined rule. | Does not create authority or prove a Template-1 exists. |
| `WORKAUTHORIZATION_TEMPLATE1_CONSUMER_READY` | Exact Template-1 bytes/identity satisfy schema, projection and non-effecting consumer acceptance. | Does not qualify or authorize a WorkAuthorization candidate. |
| `WORKAUTHORIZATION_CANDIDATE_CONSUMER_VALIDATED` | Exact immutable candidate passes pure consumer validation and semantic/authority qualification. | Does not grant issuance authority or issue/consume the candidate. |
| `WORKAUTHORIZATION_ISSUANCE_AUTHORIZED` | Candidate-specific issuance authority applies to that exact candidate/current envelope. | Does not mean issuance occurred, lifecycle is ACTIVE, or ownership exists. |

`ISSUED`, lifecycle state, ownership state, and acceptance/production evidence must remain separate downstream propositions. A single `LIFECYCLE_TEMPLATE` SATISFIED bit cannot represent these materially distinct states. The minimum listed distinctions are therefore required; model this as `SEMANTIC_STATE_DISTINCTION_REQUIRED` and `BASELINE_DEFECT = YES`. No topology/status change is made here.

## 5. Candidate-3 preservation

`WorkAuthorizationCandidateConstructionAuthority-sha256:46a00d2c619b6e3dbbe5dc59683d3d4144f64f23b375e5fe1a959deb2b6e9c8c` remains issued and unconsumed. The Candidate-3 report records that authoritative-input validation stopped before candidate bytes or identity existed. Its scope is exactly one Candidate 3 construction/qualification, and its exclusions remain intact. Resolving upstream Template-1 inputs and implementing a pure validator does not itself consume that grant. Candidate 3 must wait until Template-1's source/mapping contract is complete and the non-effecting consumer-validation gate is qualified.

## 6. Overall disposition

The Architect-adopted architecture is non-circular in design, but `TEMPLATE1_CONSTRUCTION_READY = NO`: current source records and deterministic mappings are missing, and the full consumer acceptance boundary is not implemented/available. No new dependency was discovered; the gaps arise from already enumerated consumer-required values and the missing validation seam. The accepted architecture and its five planner states are design findings only. No implementation or production authority is inferred.

`NEW_DEPENDENCY_DISCOVERED = NO`  
`BASELINE_DEFECT = YES`  
`PRODUCTION_EFFECT = NO`
