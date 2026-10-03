# O08 validator-authority gate admission contract 1

GATE = `gate:validator_authority`  
O08_EXECUTABLE = YES  
C06A_3_RETRY_ALLOWED = YES at the contract gate only.

This additive specification closes the executable admission-profile gap identified by [C06A-3 retry 1](DETERMINISTIC_PLANNER_V0_1_C06A_3_RETRY_1_RESULT.md). It changes neither the operational registry nor implementation. No E1 authority is issued, used, expanded or consumed.

## Exact recorded chain

| Member | Artifact and selector | Identity domain and exact identity |
|---|---|---|
| Accepted PREP-VALIDATOR result and original inline dossier | [Preparation result](../experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_PREP_VALIDATOR_1_RESULT.md), Proposed DEC-VALIDATOR dossier, Required future qualification, Accepted knowledge and provenance | CONTENT_IDENTITY/raw SHA-256 `bf0662e3aeba6128ab4c1b268a626e872c89cdc0eb77edc7c98d262cc4742337` |
| Review dossier | [Batch review](../experiments/E1/E1_TEMPLATE1_ARCHITECT_DECISION_BATCH_1.md), `## DEC-VALIDATOR` | CONTENT_IDENTITY/raw SHA-256 `985f3d69c89b220940db9c4d19d27223802127900a2157d2adcd33d05ae4d32b` |
| Architect decision and issued grant | [DEC-VALIDATOR record](../experiments/E1/E1_TEMPLATE1_ARCHITECT_DEC_VALIDATOR_AUTHORITY_1.json), entire object | CONTENT_IDENTITY/raw SHA-256 `df2828f5350de92a10f588c08c86f15dabcf6207c8357ec29aefde38ef97cd87`; AUTHORITY_IDENTITY `E1-ArchitectDecisionAuthority-sha256:ddd8e36587e2780f640b7babb0e44951b4f5510955822af1db8a00aa74fdd629` |
| Accepted relationship to root gate | [Issuance result](../experiments/E1/E1_TEMPLATE1_ARCHITECT_DECISION_BATCH_1_ISSUANCE_RESULT.md), Mechanical propagation paragraph | CONTENT_IDENTITY/raw SHA-256 `6ee91360c12e6c255135fcba009f0ff30b578d038860c16cbe53bdd6915069a5` |

The decision and authority are **one recorded object with two roles**, not two newly invented records. Its type is `E1-ARCHITECT-DECISION-AUTHORITY-1 / DEC-VALIDATOR`, status ISSUED, selected decision APPROVED_OPTION_1, issuer the Architect under the recorded explicit instruction. The authority's semantic identity is independently recomputed over sorted-key compact UTF-8 JSON excluding only `authority_id`.

Its `source_artifacts` array binds the exact review and preparation raw identities above. The original preparation report contains an inline unissued dossier; it has no separate semantic authority identity. The review's DEC-VALIDATOR section preserves that bounded proposal. Section selectors remain distinct even where one whole-document raw identity authenticates several claims.

The grant's exact scope is:

> adapter/workauth_lifecycle.py::consume_and_issue pre-effect stage; adapter/workauth_issuance.py::validate; adapter/invocation_constructor.py canonical checks; directly associated isolated adapter/tests qualification and only helpers necessary for this seam.

Its lineage is the recorded source/dossier chain, bound to the frozen graph/plan/selection-policy snapshot. The grant does not define a separate runtime-lineage, expiration or consumption field. This contract does not fabricate one, infer a new R4/G4 applicability rule, or turn absence of such a field into unlimited authority. The review limits it to bounded implementation/qualification, not reusable operational authority; no publication or automatic runtime migration is permitted.

The issuance result explicitly states that accepted preparation plus the issued authenticated record satisfies this gate, resolves no slot, performs no implementation and leaves CONTRACT-T1 blocking IMPL-VALIDATOR. It claims neither an external signer nor live-store publication. The oracle preserves that authentication boundary.

## Gate semantics and exclusions

SATISFIED means: the independently admitted, current-at-snapshot evidence chain proves that the exact bounded validator implementation/test grant was issued for the accepted dossier, with its conditions and exclusions intact.

It does not mean that:

- validator implementation exists or its tests pass;
- CONTRACT-T1 is complete;
- `gate:validator` or any slot is satisfied;
- IMPL-VALIDATOR is now eligible without its other prerequisites;
- WorkAuthorization acceptance, issuance, consumption, activation, ownership, transmission or execution is authorized;
- a validator PASS authorizes any effect.

Preparation alone creates no authority. A grant merely existing is insufficient without identity, source-chain, scope and validity admission. A gate label alone is insufficient without the completion proof below. This is restoration of a historical accepted authority relationship within the pinned snapshot, not a new decision or live authority check.

## Accepted preparation and exact grant correspondence

The source-pinned PREP-VALIDATOR PASS is for bounded preparation only. Its named seam and requested API are `validate_for_issuance(candidate, current_state)` sharing one authoritative private pre-effect helper with `consume_and_issue()`. Its complete requirements remain in the pinned dossier:

1. Candidate bytes/parse, WORK-AUTHORIZATION-1 schema, exact authenticated-input keys and WorkAuthorizationId.
2. Binding hash and invocation/dispatch/release/context correspondence.
3. T1 schema/content identity, INACTIVE/NONE, exact binding_digest and field types.
4. Independent source authority, scope, lineage, freshness and mappings.
5. Deterministic reconstruction and representation equality.
6. Current-state and issuance-authority checks as validation output only.
7. Shared helper, no supplied-PASS bypass, and atomic current-generation/freshness recheck at the effect boundary.

Required qualification includes differential valid/invalid decisions; malformed/schema/type/digest/key/stale-reference/changed-projection failures; zero-effect PASS and FAIL; shared-helper call and mutable-generation race checks; active-consumer import and exact implementation identity. These are requirements preserved by the grant, not completed tests claimed by this admission.

The T1 body must be verified in its proper canonical/version/domain before comparing issuance identity. T1 identity, WorkAuthorizationId, binding_digest and issuance-authority identity remain distinct. Exact T1 body/schema choices are still CONTRACT-T1 outputs. The grant's `preconditions = [CONTRACT-T1]` must persist. This predicate checks that binding, **not CONTRACT-T1 satisfaction**.

The issued record must exactly preserve authorized operation, API, sharing requirement, exclusions, prohibited effects and false flags for runtime permission, Candidate-3 consumption, validator-PASS authority and implementation performed. Broadening any field rejects. No single-use operational permission, repository task permission, context/governance/transmission repair or general adapter refactor is implied.

## Typed executable admission predicate

The [machine-readable contract](DETERMINISTIC_PLANNER_V0_1_O08_VALIDATOR_AUTHORITY_GATE_ADMISSION_1.json) supplies the complete profile and independent reference entry point:

```text
ADMIT_VALIDATOR_AUTHORITY_GATE_1(profile, state, validity)
    -> ACCEPT / REJECT(failed_clause)
```

`admit(profile,state,validity)` implements that specification using only deterministic standard-library operations. It imports no planner code, performs no I/O, executes no callbacks and alters no state. The embedded program is qualification specification, never code to execute from an untrusted runtime import.

| Input | Typed requirement |
|---|---|
| Profile | Independently pinned `O08-ADMISSION-PROFILE-1`; contains exact admitted source records and contract, not selected by submitted proof |
| State | Exact `O08-INPUT-1` keys; SYNTHETIC_QUALIFICATION_ONLY mode; profile digest |
| Gate/predicate | Exact `gate:validator_authority` and `ADMIT_VALIDATOR_AUTHORITY_GATE_1` |
| Completion proof | `O08-GATE-PROOF-1`, type `ISSUED_BOUNDED_VALIDATOR_GRANT_PROOF`; content identity `O08GateProof-sha256` over body excluding identity |
| Preparation | Type `ACCEPTED_PREP_VALIDATOR_DOSSIER_1`, admitted at pinned snapshot, exact raw source and selectors |
| Dossier | Exact review source raw pin and DEC-VALIDATOR section |
| Decision | Exact decision type/id/option, binding the semantic authority identity |
| Authority | AUTHORITY_IDENTITY, namespace/digest above; full issued record, separately raw-content authenticated |
| Scope/source lineage | Exact scope and ordered `source_artifacts` identity/path bindings from grant |
| Context | CONTENT_IDENTITY pins for frozen graph, plan and selection policy; evaluation PINNED_SNAPSHOT_ONLY |
| Supports/provenance | Four role-specific raw source pins/selectors and extraction version `O08_ACCEPTED_CHAIN_1` |
| Preconditions/downstream | CONTRACT-T1 retained; conditional IMPL-VALIDATOR route; no slots resolved or validator completion |
| Documentary inputs | Exact UTF-8 source texts, matching independent raw pins; copied documentary inputs are not new authority |
| Validity | Independently admitted context and per-source identity/status; every role CURRENT_AT_PINNED_SNAPSHOT |

The raw-profile pin, raw source pins and canonical semantic authority/proof identities are distinct. Canonical JSON uses UTF-8, sorted keys, compact separators and retained array order; non-JSON values/floats reject. Permission-boundary equality uses canonical typed equality, so integer zero is not boolean false.

Trust is explicit: the harness/governed acceptance boundary admits the profile and validity view independently of the proof. A submitting party cannot repin a substituted grant or invent accepted validity. The evaluator authenticates the recorded chain relative to those pins; it does not independently discover live revocation or acquire publication evidence.

## Acceptance clauses and negative fixtures

| Clause | Rejection condition |
|---|---|
| C00_SCHEMA | Malformed/extra/missing schema keys, wrong mode or profile binding |
| C01_PROOF | No completion proof |
| C02_GATE | Wrong gate or predicate/schema binding |
| C03_PROOF_TYPE | Knowledge/PASS in place of named grant completion proof |
| C04_PREPARATION | Missing, unaccepted or incorrectly bound preparation |
| C05_DOSSIER | Wrong dossier identity/selector |
| C06_DECISION | Wrong decision, option, decision type or authority binding |
| C07_AUTHORITY_REQUIRED | Authority absent, regardless of implementation/test observations |
| C08_AUTHORITY_IDENTITY | Wrong authority domain, namespace or semantic identity |
| C09_AUTHORITY_TYPE_STATUS | Wrong authority schema/type or unissued status |
| C10_SOURCE_LINEAGE | Dossier/preparation source chain differs or is absent |
| C11_SCOPE | Grant or proof scope broader/different |
| C12_PRECONDITIONS | CONTRACT-T1 prerequisite removed or changed |
| C13_PERMISSION_BOUNDARY | Issuance permission, changed helper/tests/exclusions/effect controls or other grant expansion |
| C14_CONTEXT | Incompatible graph/plan/policy snapshot or evaluation context |
| C15_BINDINGS | Missing/wrong source pins or provenance |
| C16_GATE_BOUNDARY | Incorrect downstream conclusion, slot resolution or validator completion |
| C17_VALIDITY | Missing/currentness mismatch, stale or revoked support |
| C18_SOURCE_BYTES | Missing/substituted documentary source bytes |
| C19_RECORD_CORRESPONDENCE | Supplied record differs from independently admitted exact grant/source |
| C20_AUTHORITY_HASH | Canonical semantic authority identity does not recompute |
| C21_ACCEPTED_CHAIN | Pinned documents fail required preparation/review/propagation statements |
| C22_PROOF_IDENTITY | Completion-proof identity fails recomputation |

[Fixtures](DETERMINISTIC_PLANNER_V0_1_O08_VALIDATOR_AUTHORITY_GATE_ADMISSION_1_FIXTURES.json) contain one positive for the actual gate and **41 negatives**, each with expected failed clause. Negatives include every requested applicable category, all four supports individually stale/revoked, graph/policy mismatch, generic knowledge, false-to-zero substitution and proof identity corruption. Mutated proof bodies are rehashed except the identity-corruption case, preventing unrelated enclosing-hash failures from masking semantic rejection. Cases with implementation/tests but no authority attach those observations outside predicate input; neither observation supplies the missing grant.

The positive proof is synthetic qualification data over copies of authentic frozen documentary inputs. Its profile/validity admissions are explicit qualification premises. It does not issue an E1 authority, change the frozen gate or supply any missing external evidence.

## Invalidation, cold restoration and composition

Persist the profile identity, typed completion proof and its identity, all documentary source pins/selectors or resolvable pinned bytes, graph/plan/policy context, exact authority record and semantic identity, preparation/dossier relationship, precondition/exclusion set, and separately admitted source validity/invalidation state. The gate boolean is only a cache.

On cold restoration reauthenticate source bytes, recompute semantic identities, recheck the entire source/decision/grant chain and validity, then derive gate support. A required source becoming STALE/REVOKED/absent withdraws support even if the proof bytes and previously cached SATISFIED label remain unchanged. Persist invalidations so reload cannot restore support from an old cache. Dependent planner conclusions must then be recomputed using the existing proof/dependency system; this specification does not implement that integration.

Four explicit validation sequences cover every support role: accepted -> serialize/reload -> invalidate source -> serialize/reload -> C17 rejection, preserving the original proof. Revalidation requires separately accepted source evidence; this contract authorizes no flag reset or new grant.

Cross-oracle rules:

- Decision/authority: preserve the same record, option, dossier, scope and identity rules. DECISION_RECORDED alone does not satisfy a root; this named chain proof is the independent completion criterion for this particular authority gate.
- O09: preserve content-vs-authority identity domains and separate proof admission from source knowledge or producer completion. Neither O08 acceptance nor this grant changes either baseline slot.
- Overlay/control: require the exact graph/plan context before composition; admit this gate as derived proof support, not a trusted cached control label. All other goals/holds remain independently evaluated.
- Selection policy: profile pins the qualified frozen policy source. Substitution rejects. O08 does not select an action or change policy ordering.
- Envelope: grant scope/source lineage and snapshot pins must match. The grant has no separate runtime/G4/profile applicability fields; do not infer them or demand manufactured evidence. It cannot be transplanted into a different graph/plan/policy envelope.
- CONTRACT-T1 remains a downstream conjunct. Gate admission is insufficient for IMPL-VALIDATOR actionability, PURE_VALIDATION_READY or WorkAuthorization issuance/use.

## Registry binding and retry gate

The unchanged operational registry must eventually bind the exact gate to predicate version 1, `O08-GATE-PROOF-1`, `ISSUED_BOUNDED_VALIDATOR_GRANT_PROOF`, accepted preparation type, decision/authority types, source CONTENT_IDENTITY domains, authority AUTHORITY_IDENTITY domain and independently pinned profile. Exact values are under `/registry_binding_required`. Installation and typed planner integration remain implementation work; no registry edit occurs here.

O08_EXECUTABLE = YES: specific predicate, positive/negative fixtures, invalidation/restoration rules, registry binding and composition rules are present. O09 remains executable. The prior mapping/completion inputs are unchanged, and this was the sole additional prerequisite recorded by retry 1. Thus C06A_3_RETRY_ALLOWED = YES at the contract gate. This permits a later retry to revalidate the entire package and implement; it is not an implementation PASS or a claim that no future issue can be discovered.

## Validation and preservation

The [validation companion](DETERMINISTIC_PLANNER_V0_1_O08_VALIDATOR_AUTHORITY_GATE_ADMISSION_1_VALIDATION.json) records 1 positive and 41 negatives PASS with exact outcomes, all 42 JSON round trips, four source-invalidation/reload sequences, and source-pin verification. Independent processes under hash seeds 0/17/113 and reversed fixture/object-key ordering yield identical semantic digest `5fd4c543a02b00b3810c8a5c0f08debdc406db31c175f4f7829f61ef60c94fcd`.

These are specification tests, not planner regressions or implementation qualification. All 10,911 E1 files, implementation/tests, prior registries/oracles, backlog and historical results remain byte-for-byte unchanged. Only four new contract/fixture/validation/report files are added. JSON/local links and `git diff --check` pass.

```text
GATE = gate:validator_authority
PREPARATION_EVIDENCE = PREP-VALIDATOR result, raw bf0662e3aeba6128ab4c1b268a626e872c89cdc0eb77edc7c98d262cc4742337
DECISION = DEC-VALIDATOR / APPROVED_OPTION_1
AUTHORITY = E1-ArchitectDecisionAuthority-sha256:ddd8e36587e2780f640b7babb0e44951b4f5510955822af1db8a00aa74fdd629
ADMISSION_PREDICATE = ADMIT_VALIDATOR_AUTHORITY_GATE_1
POSITIVE_FIXTURES = [POS-VALIDATOR-AUTHORITY-GATE]
NEGATIVE_FIXTURES = 41, individually enumerated in fixture companion
SOURCE_INVALIDATION_RULE = required support invalid -> gate proof unsupported after reload
PERSISTENCE_RULE = restore and validate chain and validity, never trust gate boolean
REGISTRY_BINDING_REQUIRED = specified, not installed
O08_EXECUTABLE = YES
O08_MISSING_ELEMENTS = []
C06A_3_RETRY_ALLOWED = YES
C06A_3_RETRY_PREREQUISITES = [prior mappings/oracles pinned, O09 executable,
 O08 specific positive/negatives PASS, invalidation/restoration PASS,
 registry binding specified, no additional recorded prerequisite missing]
RESTORED_AND_QUALIFIED = 2/17
C06A_4_READY = NO
C07_RETRY_ALLOWED = NO
F03_STATUS = CLOSED
V0_1_CURRENT_STATUS = CORRECTION_REQUIRED
IMPLEMENTATION_MODIFIED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
```
