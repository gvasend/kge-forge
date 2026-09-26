# E1 WorkAuthorization Template-1 Production Contract 1

## Result

| Output | Determination |
|---|---|
| `RESULT` | `PRODUCTION_CONTRACT_INCOMPLETE` |
| `BINDING_INPUT_SCHEMA_COMPLETE` | NO — a safe reference-manifest shape can be proposed, but exact source references and resolved values are missing. |
| `FIELDS_VALUES_MAPPING_COMPLETE` | NO — sources are named for many fields, but exact projections/types are not specified or validated by the consumer. |
| `BINDING_DIGEST_RULE_COMPLETE` | YES as an algorithm; NO as an executable current derivation because the exact authenticated input map is incomplete. |
| `CIRCULARITY` | NO in the proposed direction, provided explicit exclusions below are enforced. |
| `AUTHORITY_MODEL_COMPLETE` | NO — authority for several inputs/projections is absent or not bound to the expected consumer field semantics. |
| `CONSUMER_VALIDATION_DEFINED` | NO for the required end-to-end non-effecting path; pure constructor checks exist, but the lifecycle bridge proceeds directly to issuance. |
| `BASELINE_GRANULARITY` | `SEMANTIC_STATE_DISTINCTION_REQUIRED` (existing coarse node has a granularity defect). |
| `CANDIDATE_3_AUTHORITY_REMAINS_VALID` | YES — no Candidate 3 was constructed. |
| `PRODUCTION_EFFECT` | NO |

No binding-input object, Template-1, Candidate 3, authority, or dependency update was created.

## 1. Required value inventory

The actual T1 constructor contract is implemented in [invocation_constructor.py](../../../adapter/invocation_constructor.py). Its authenticated input map has exactly 22 keys. Template-1's `binding_digest` is `digest(authenticated_inputs)`, where `digest` is SHA-256 over UTF-8 JSON with sorted object keys and compact separators. The separate 23-key `fields_values` map creates the typed host/lifecycle WorkAuthorization. Current artifacts expose many identity references, but identity/reference presence alone does not establish the owning canonical record or the required field projection.

Status terms below: **AVAILABLE REF** means a current candidate artifact carries the reference, not that every byte/value needed by the consumer is independently resolved; **MISSING** means no applicable current source/value was found; **RULE GAP** means an authority domain is identifiable but the exact transformation into the consumer field is not defined.

### Authenticated inputs hashed for `binding_digest`

| Exact key | Meaning and authoritative source | Current source/value and derivation status | Freshness/scope requirement |
|---|---|---|---|
| `InvocationAttemptId` | Invocation authority; current invocation attempt identity | `InvocationAttempt-sha256:e89c032e…bbfa` appears in current invocation/binding evidence. **AVAILABLE REF**, but must resolve to canonical current invocation source. | Exact first E1-WP-001 attempt, current R4/G4 lineage, not consumed. |
| `binding_sha256` | Digest of `canonical_binding` | No current canonical binding bytes are present in the current invocation/binding artifacts. **MISSING; DERIVATION_DEFINED_INPUT_MISSING.** | Must be recomputed over exact canonical binding bytes for the same attempt. |
| `canonical_binding` | Invocation binding used for cross-domain consistency | Current artifacts provide references and sibling correspondence, not the actual canonical binding object. **MISSING.** Historical WorkAuthorization binding is stale and cannot substitute. | Must bind current dispatch, context, runtime, profile and exact attempt; no sibling-ID recursion. |
| `DispatchAuthorizationId` | Current dispatch authority | Current dispatch identity `CurrentDispatch-sha256:ee06120a…775aa3` is available. Mapping its identity to the consumer's `DispatchAuthorizationId` field is a **RULE GAP**; prior R4 dispatch ID is stale. | Re-resolve current live G4 selection immediately before construction. |
| `specific_approval_id` | Specific Architect approval consumed by the WorkAuthorization | Current release record carries a decision description, but no exact current `specific_approval_id` mapping is established. Old proposed R4 adoption ID is historical. **MISSING.** | Must be the applicable current Architect decision, exact R4/E1 scope. |
| `predecessor` | Attempt-chain predecessor | Current invocation candidate says `R12_HISTORY`; this is a reference, not itself the canonical current predecessor/attempt-allocation proof. **AVAILABLE REF; authority resolution required.** | Validate against current attempt chain and single-use allocation. |
| `eligibility` | Independent evidence that the current invocation is eligible | Historical WorkAuthorization carries old eligibility flags. No exact current eligibility record/value is bound into current invocation inputs. **MISSING.** | Current R4/G4 applicability and freshness at construction. |
| `release_authority` | Current release authority | `ReleaseAuthority-sha256:18184991…29ff1e`. **AVAILABLE REF** in current R4 qualification artifacts; verify canonical authority source and currentness. | Exact current R4/G4 and profile/policy scope. |
| `OperationalContextId` | Current operational context | `OperationalContext-sha256:ff57a210…bc10c`. **AVAILABLE REF**; current source/applicability must be revalidated. | Must agree with release, dispatch, invocation, binding. |
| `runtime` | Exact current runtime | `sha256:b6bcbb43…625761`. **AVAILABLE** in current R4 source/lineage evidence. | Runtime-head/currentness must be fresh at construction. |
| `runtime_head` | Authority selecting runtime head | Old concrete WorkAuthorization references `RUNTIME-HEAD-AUTHORITY-sha256:75e6…`; current release root and invocation artifacts do not establish that as the current independently authenticated head. **MISSING current source.** | Current runtime-head authority and G4 generation. |
| `supervisor` | Current supervisor authority/instance | Old WorkAuthorization contains a supervisor identity; no current R4/G4 owning source is established in this input set. **MISSING current source.** | Current supervisor scope and readiness. |
| `succession_head` | Current supervisor succession authority | Old WorkAuthorization contains an identity; no current applicable canonical source is bound by the present current artifacts. **MISSING current source.** | Current succession chain/head. |
| `profile_sha256` | Exact profile value consumed by legacy constructor | Current ReleasedProfileAuthority is `ec39636d…a407`; profile-root candidate `83b8…fcd6` and ProgrammerProfile `0a0718…dd67` are distinct identities. Which bytes/identity this field requires is not defined. **RULE GAP.** | Must bind released current profile and task scope; cannot substitute authority ID for content digest without schema rule. |
| `ModelPayloadDigest` | Exact current model payload digest | Approved payload SHA-256 `768fd880…d88` and payload authority `cc20ba70…9ada` exist. The consumer field expects the payload digest; use the exact approved payload identity, after independent authority resolution. **DERIVATION AVAILABLE subject to source check.** | First E1-WP-001 request only; immutable payload. |
| `transmission_retention` | Transmission/retention binding | Separate current authorities exist (`CurrentTransmissionAuthority…a611f79c`; `CurrentRetentionAuthority…9d60462`). No qualified rule combines them into this singular field. **RULE GAP.** | Exact provider/model/payload and single request; preserve unresolved retention as authorized. |
| `budget_policy` | Budget-policy value | `StatusBudgetAuthority-sha256:02cc22de…edc99` exists. Mapping authority ID to the constructor's expected policy value is not specified. **RULE GAP.** | Exact first-request/R4 budget, no reset/enlargement. |
| `implementation_identity` | Implementation/runtime identity | Current R4 runtime identity `sha256:b6bcbb43…625761`. **DERIVATION AVAILABLE** if the constructor contract defines this field as that identity; no separate mapping validation exists. | Exact current frozen runtime bytes. |
| `audit` | Audit binding/state consumed by constructor and passed to ownership ledger | Current operational binding says `CANONICAL_AUDIT_NAMESPACE_UNBOUND_UNUSED`; no actual current audit namespace/store identity or audit-state source is established. **MISSING.** | Must be independently selected/authorized before issuance; no post-issuance state may be assumed. |
| `initial_state` | Initial lifecycle boundary | Architect-approved value `INACTIVE`. **AUTHORIZED POLICY INPUT.** | Exact current R4 lifecycle semantics. |
| `ownership` | Initial ownership boundary | Architect-approved value `NONE`. **AUTHORIZED POLICY INPUT.** | No ownership grant; fresh ledger remains ownership authority. |
| `lifecycle_envelope` | Consumer lifecycle envelope | Template-2 carries `INACTIVE_ACTIVE_TERMINAL_ONLY`; T1 summary labels `WORK-AUTHORIZATION-1`; mapping between these is not defined. **RULE GAP.** | Must be only previously qualified R4 lifecycle transitions. |

The current invocation/dispatch/context/binding JSONs are constructed summaries with identities and cross-references. In particular, the current operational binding does not contain the canonical invocation-binding object or its digest. They cannot be used as substitutes for those missing input values merely because their references agree.

### `fields_values` mapping

The constructor requires exactly the following `WorkAuthorization` dataclass keys. The source classes below are those in the qualified historical field authority analysis; a named domain is not treated as proof that a deterministic T1 value mapping exists.

| `fields_values` key | Proposed owner/source | Deterministic mapping available? | Current result |
|---|---|---|---|
| `authorization_id` | Current `InvocationAttemptId` | Yes: consumer overwrites with invocation ID | Source invocation ref available; exact canonical binding inputs still unresolved. |
| `revision` | Issuance protocol | Yes: consumer overwrites with `1` | Rule exists; constructor still requires this key in `fields_values` but defines no sentinel for its ignored input value. |
| `work_package_id` | Current dispatch / E1 task | No explicit field projection function | Dispatch/task identities exist; projection/type rule missing. |
| `session_id` | Invocation identity | No current source field or projection rule | MISSING. |
| `turn_id` | Invocation identity | No current source field or projection rule | MISSING. |
| `read_roots` | Current released profile / RepositoryAuthority | Authority IDs and profile summary exist; no qualified T1 projector/cross-check | RULE GAP; source values must be resolved from owning authorities. |
| `write_roots` | Current released profile / RepositoryAuthority | Same | RULE GAP. |
| `deny_roots` | Released profile policy | Same | RULE GAP. |
| `exec_bins` | Released profile execution policy | `exec_argv_allowlist` exists, but deriving executable bins from argv is not authorized/defined | RULE GAP. |
| `shell` | Released profile policy | Candidate says false; no T1 authority resolver validation | RULE GAP; matching copy alone is insufficient. |
| `network` | Current transmission/task network policy | Separate authority references exist; T1 mapping absent | RULE GAP. |
| `state` | Lifecycle policy | Yes: consumer overwrites to `INACTIVE` | Rule/policy exists; ignored source value sentinel still unspecified. |
| `context_binding` | Current release/context authority | No T1 derivation/validation rule | RULE GAP. |
| `exec_argv_allowlist` | Released profile | Profile includes an allowlist | Source value potentially resolvable; exact provenance-bound projection and freshness validation absent. |
| `read_deny_roots` | Released profile policy | No T1 projector | RULE GAP. |
| `write_deny_roots` | Released profile policy | No T1 projector | RULE GAP. |
| `ownership_ledger` | Audit/ownership authority; consumer overwrites with `audit` input | The T1 field is overwritten, but `audit` source/ledger namespace is missing; ignored field input sentinel also unspecified | MISSING source and contract detail. |
| `write_directory_roots` | Released profile / RepositoryAuthority | No T1 projector | RULE GAP. |
| `execution_profile` | Released profile identity/constraints | Profile is available by identity; exact typed projection is not defined | RULE GAP. |
| `model_transport` | Provider/transmission authority | Authority exists; exact object/value schema and mapping absent | RULE GAP. |
| `model_transmission` | Transmission/retention authorities | Two authorities exist; no composition rule or schema for this field | RULE GAP. |
| `context_projection` | Current context/payload projection | Current payload exists; no exact typed value/derivation for this host field is established | RULE GAP. |
| `operational_binding` | Current OperationalBinding | Identity `0fc7fdb6…40cb7` exists; current artifact has correspondence metadata, not a typed value projection | RULE GAP. |

The “ignored key” issue for `authorization_id`, `revision`, `state`, and `ownership_ledger` is not a reason to invent placeholder values. A production contract must either define a canonical sentinel/type for those mandatory keys or revise the consumer contract so it does not require unused values.

## 2. Binding-input schema assessment

A safe **conceptual** `WORK-AUTHORIZATION-BINDING-INPUT-1` should be a provenance manifest, not an authority object. The least-authority representation is immutable references to source records, with no copied source value treated as authoritative:

```text
schema = WORK-AUTHORIZATION-BINDING-INPUT-1
scope = exact InvocationAttemptId + E1-WP-001 + current R4/G4 generation
sources = map from every authenticated-input key and every fields_values key
          to {authority_domain, source_record_identity, source_content_digest,
              store/generation/head, invocation/context/runtime scope,
              version/freshness, resolver/projection rule identity}
canonicalization = UTF-8 JSON, lexicographically sorted object keys,
                   compact separators; arrays have schema-defined order
identity = hash of this manifest body excluding its derived identity
```

Completeness would require one and only one owning source or explicitly authorized deterministic derivation for every output field; source bytes/identity recomputation; current generation and applicability checks; invocation/runtime/context consistency; no missing, duplicate, substituted, stale, or caller-supplied values; and immediate revalidation before Template-1 construction. This is not yet a complete schema: several source identities/rules in the tables are missing, and no resolver/projection-rule identity exists for T1.

The wrapper manifest must not be hashed as `binding_digest`: the existing consumer computes `digest(authenticated_inputs)`. The producer must resolve references, construct the exact canonical 22-key `authenticated_inputs` object, and then compute `binding_digest` over that object. Keep the wrapper's own provenance identity separate. Adding wrapper metadata to the 22-key input object would fail the consumer's exact-key check and change the digest contract.

## 3–5. Derivation and circularity review

### Digest rule

The algorithm is defined: canonical bytes are sorted-key compact JSON UTF-8 of exactly the `authenticated_inputs` map, hashed with SHA-256. The input keys and canonicalization come from the existing consumer. No key may be added or omitted. Exclude the binding-input manifest's own identity/provenance wrapper, Template-1 identity, Template-2 identity unless explicitly one of the existing 22 values (it is not), WorkAuthorizationId, Candidate-3 identity, and any derived sibling identity not in the fixed input set. Current input sources are incomplete, so the derivation result is not currently computable without guessing.

### Dependency/cycle tests

| Threat | Result under proposed architecture | Required invariant |
|---|---|---|
| Template-1 authorizes its own inputs | No cycle if each input reference terminates in an independently authoritative source; source provenance must be checked before T1 construction. |
| WorkAuthorization authorizes its own template | No cycle if Template-1 is built from binding-input references and T2 policy, never from Candidate 3/WorkAuthorization bytes. |
| `binding_digest` depends on Template-1 identity | No: digest is over the exact 22-key inputs before T1 identity exists. Do not put Template-1 ID in that map. |
| `fields_values` depends on Candidate 3 | No: fields must derive from authority references and deterministic field rules; Candidate 3 is a downstream consumer. |
| Invocation/binding identity recursion | Avoidable: use the qualified joint construction's common authoritative inputs and exclude post-construction sibling correspondence from canonical IDs. The actual `canonical_binding` bytes are nevertheless missing today. |
| Authority derived from compatibility/presence | Prohibited. A binding-input manifest proves provenance and consistency only; it cannot elevate its references. |
| Template-2 becomes invocation authority | Prohibited. T2 contributes lifecycle constraints only. Its historical `runtime_scope`/`release_scope` do not select current invocation, dispatch, profile, or other operational values. |

`CIRCULARITY = NO` for the Architect's proposed dependency direction as constrained above. This is a design result, not evidence that a complete producer exists. If the audit input is actually a future ledger state rather than a pre-existing ledger namespace/reference, or if binding construction includes Template-1/WorkAuthorization identities, the implementation would violate this acyclic design and fail qualification.

## 6. Authority boundaries

1. **Authorize/adopt the production contract:** Architect/lifecycle authority-owner decision required. The current Architect direction authorizes formal validation only; it is not adoption of the contract.
2. **Construct a binding-input candidate:** Composition adds no authority, but the current Candidate-3 grant names Candidate 3 only. It does not clearly authorize publication of a separate canonical binding-input artifact. Internal reference resolution strictly necessary for the one Candidate-3 construction may be part of that authorized task only after the inputs exist; any separately issued/published B-input record needs explicit scope approval. No source authority is expanded by this step.
3. **Construct Template-1:** A separate construction scope/contract is needed after sources and mappings are complete. Prior lifecycle approval covers INACTIVE/NONE and transition semantics, not the unresolved projection contract.
4. **Issue/release Template-1 for current R4:** Distinct Architect issuance/release authority is required. Candidate construction authority, Template-2 qualification, and the previous summary are not release authority for a new consumer-ready T1.

No authority is issued by this assessment.

## 7. Mandatory validation pipeline

The ordered pipeline is sound, with one precision: reference validation must resolve and independently authenticate all source objects before constructing the 22-key input map; the `binding_digest` is over that resolved consumer map, not the reference manifest.

`authoritative sources → binding-input reference manifest → source resolution/currentness/completeness validation → exact canonical authenticated_inputs → binding_digest → explicit fields_values projection → Template-1 construction → schema/key validation → template identity validation under the selected template contract → WorkAuthorization identity validation → actual non-effecting consumer reconstruction/equality acceptance → semantic and authority qualification → immutable Template-1 identity → Architect release decision`.

The current T1 implementation has no template identity constructor/validator; issuance later assumes `WorkAuthorizationTemplateId`. The selected contract must define that identity and how it binds the T1 body before consumer acceptance. T2's identity function applies only to T2 schema and cannot silently be reused for T1.

There is also no non-effecting entrypoint for the complete lifecycle bridge. `workauth_lifecycle.consume_and_issue()` checks bytes, canonical WorkAuthorization identity, reconstructs the artifact and typed object, and then calls `issue_inactive()`. It has no validation-only mode. The pure `identity()` and `construct_work_authorization()` helpers can be called directly without effects, but that does not exercise the complete bridge acceptance path. The required actual-consumer, non-effecting acceptance gate is therefore not yet executable as specified.

## 8. Dependency-model consequence

The planning graph should distinguish:

- `LIFECYCLE_TEMPLATE_SEMANTICS_QUALIFIED` — reusable, technically qualified T2 constraints;
- `WORKAUTHORIZATION_BINDING_INPUT_CURRENT` — all source refs/values are independently authenticated, current, complete, and projectable;
- `WORKAUTHORIZATION_TEMPLATE1_CONSUMER_READY` — exact T1 bytes validate and are accepted by the non-effecting consumer.

These propositions can differ independently; the currently satisfied coarse `LIFECYCLE_TEMPLATE` node hides the known state where semantic qualification exists but current input/template readiness does not. Classification: `SEMANTIC_STATE_DISTINCTION_REQUIRED` and the present model has a `BASELINE_GRANULARITY_DEFECT`. No graph changes were made.

## 9. Actionability

`NEXT_OPERATION = PRODUCTION_CONTRACT_INCOMPLETE`.

The architecture proposed is non-circular in principle, but there is no complete B-input schema/source map, exact current authenticated input object, or deterministic `fields_values` projector. The minimum next work is to ground the missing current authorities and formally define/qualify the per-field projections and T1 identity contract. A design approval alone cannot fill those values. Candidate 3 remains authorized for one construction but must not be attempted until those inputs and rules pass validation.

`NEW_DEPENDENCY_DISCOVERED = NO` — these requirements derive from the already known T1 consumer fields and source gaps; the B-input is a composition/provenance mechanism, not a new authority root.

No model, dependency, authority, template, WorkAuthorization, lifecycle, ownership, repository, host, or production state changed. `PRODUCTION_EFFECT = NO`.
