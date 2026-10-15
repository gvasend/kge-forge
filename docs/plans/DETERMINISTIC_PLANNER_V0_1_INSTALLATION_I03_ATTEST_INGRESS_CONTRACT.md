# INSTALLATION-I03 — ATTEST / ingress definition installation contract

RESULT = PASS (contract definition only). Runtime implementation and application qualification remain future work. No authentication object, authority, attestation instance or Evidence has been admitted by this package.

## Authoritative basis

The dependency-provenance closure establishes that the extra offline trust provenance is required but its attestor/predicate subjects are absent. Removing that record exposes unknown predicate ID. I01/I02 supply the generic installation event and transaction boundary; T04 supplies authority → attestor → source predicate semantics; E02 supplies transient Evidence-bound derivation. The canonical P03/P04 phase boundary remains unchanged.

Inputs: [dependency provenance closure](DETERMINISTIC_PLANNER_V0_1_E2_P04_DEPENDENCY_PROVENANCE_CLOSURE_1.md), [I01](DETERMINISTIC_PLANNER_V0_1_INSTALLATION_I01_CONTRACT.md), [I02](DETERMINISTIC_PLANNER_V0_1_INSTALLATION_I02_RESULT.md), [continuation closure](DETERMINISTIC_PLANNER_V0_1_E2_P04_CONTINUATION_INPUT_CLOSURE_1.md). Exact source hashes, sealed bodies and native projections are recorded in the machine companion.

## Object inventory and identity domains

The four native declarations are prospective definitions. Their existing deterministic native IDs identify declarations, not accepted authority issuance or installation. Member descriptor identity, canonical body ContentID, native entity/predicate ID and qualification wrapper identity remain distinct. The new canonical bodies are sealed offline under qualification/INSTALLATION_I03_1; prior files are unchanged. Members cannot be installed individually.

| Member | Native object ID | Definition ID | Body ContentID |
|---|---|---|---|
| authority | `E2-ATTEST-AUTHORITY:7af52928fbc6b7960e26eb799f97f1e610478a08bec8fed41a3f8af356d4b8ca` | `dc0986e0358c7ebf087714cb8c489328c4f2a7750e7bdf9534c97ac19f4efec0` | `94fff2c47ddaa656b3279a42dea31db39ea0cc4829035360e3d7fe84d7b3c4c7` |
| authority_predicate | `ATTEST-AUTHORITY:7af52928fbc6b7960e26eb799f97f1e610478a08bec8fed41a3f8af356d4b8ca` | `fa0f47cc95ffc93654d2eab28dca5e88987d7dc7e9e6b69bf895780e03ea54db` | `41c7e65b0d30ae7ff458fd0d8551209acb76bac15a25775c6bc053bc22bdd9d1` |
| attestor | `E2-SYNTHETIC-ATTESTOR:80f82bc3c61ea0dd5cb77f715d2af356b5249d01fc37e6a8c1701102713c7539` | `de754a27fe4e5d5af166641ae0b674814da4e346ac0283ea203855a93b798f20` | `2c351047c6d1d70db5bba80db5b0fc895ce7a708ac09d7d2364d7e68a1249cbc` |
| source_predicate | `E2-ATTESTOR-MAY-ATTEST:80f82bc3c61ea0dd5cb77f715d2af356b5249d01fc37e6a8c1701102713c7539` | `a8ca10f789e9c2ba32f1666bbb947a5857685fbe752aca6552406c12f7c3e9a3` | `8facd8df588c644748d110f5ac5993b7021a873e5020018d4c2c55e15e9501d9` |

Every member binds scope E2-QUALIFICATION-ONLY, lineage E2-P03-PROSPECTIVE-QUALIFICATION-1, generation E2-P03-PROSPECTIVE-GENERATION-1, source AUTHORITY_IDENTITY/TEST-rule-owner/bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb, consumer A09, E2-GATE and E2-EXTERNAL-REQUIREMENT. Validity is tick 0 through 100, subject to native boundary semantics. Native Predicate has no standalone provenance/generation field: installed membership and subject currentness supply those checks.

EvidenceBoundAttestation has no I03 object ID, bytes or ContentID because no instance is created. E02 derives it transiently/atomically against the exact native Evidence during A09 preparation/admission. It must never be installed as a definition.

The prepared definitions originate in P04 preparation, not a prior accepted ATTEST issuance. T04 generic construction can be reused; adopting a historical or newly materialized T04 Snapshot would bypass installation and is prohibited.

## Typed adapter and allowed state effects

```json
{
  "allowed_runtime_edits_future": [
    "closed adapter registry/body parsing/role-CAS/post-state projection",
    "optional authority-binding operands and ingress projection/membership witnesses",
    "configuration source prefix chronology/authority invalidation support",
    "bounded consumer currentness guard"
  ],
  "authentication_state_effect": [
    "exact authorized GraphEntity authority/attestor representations in Snapshot.entities",
    "both exact Predicate definitions in Snapshot.predicates",
    "installed set/member/authority-reference witness and source-index additions",
    "one ordinary event"
  ],
  "authority_binding_operand": {
    "fields": [
      "authority_class=ATTEST",
      "declared_authority_reference",
      "operating_authorization_id",
      "issued_authorization_json",
      "accepted_admission_Provenance",
      "binding/subject IDs",
      "issuer/admission_policy refs"
    ],
    "optional_versioned_field": "InstallDefinition.authority_bindings = immutable tuple default empty, omitted for old events",
    "source_set": "Exact aggregate/member body pins, admitted operating receipt pin, INSTALL receipt pin; receipt/grant data inline historical operands for pure replay, no filesystem-dependent decision in apply_event.",
    "type": "DefinitionAuthorityBinding",
    "validation": "Existing INSTALL authority remains distinct; typed adapter independently verifies operating grant/receipt against external trusted anchors and exact sealed members/source/context before any state projection."
  },
  "classification": "INSTALLABLE_WITH_TYPED_ADAPTER; existing generic event representation/protocol reused; adapters and authority-binding operands not implemented",
  "closed_types": [
    "AUTHENTICATION_DEFINITION_SET",
    "EVIDENCE_INGRESS_CONTRACT"
  ],
  "consumer_guard": "For installed classes only, resolve canonical ingress and its installed authentication set; prove authority/attestor/predicate/consumer closure before ordinary evidence.apply. Bind E02 authority, attestor and source_predicate to canonical chain, not values supplied by the transient instance itself; recompute its identity with the qualified E02 formula. Then invoke ordinary native predicate/attestation/admission checks.",
  "event_type": "INSTALL_DEFINITION",
  "frame": "Preserve existing route, native Actions/statuses/knowledge, gate lifecycle/pending/history/observations, actual proofs and root/slot state, decisions, context/policy. No authority issuance, Evidence, receipt, ValidationResult, ActionResult, GENESIS.",
  "ingress_state_effect": [
    "additive optional Snapshot.ingress_contracts tuple, default omitted for old encodings",
    "exact typed EvidenceIngressContract decoded with ingress descriptor provenance",
    "installed role witness, source-index additions and one event"
  ],
  "member_projection": "Decode each sealed native body; remove no native semantic field except provenance supplied by the aggregate descriptor. Entities use common full aggregate body Provenance. Predicates retain exact IDs/subject/expected/ATTEST permission; their provenance is the installed-member witness.",
  "member_types": {
    "attestor": "GraphEntity",
    "authority": "GraphEntity",
    "authority_predicate": "Predicate",
    "source_predicate": "Predicate"
  },
  "new_event_semantics_required": false,
  "role_resolution": "Dispatch by definition_type and closed typed role. Authentication role=(gate,requirement,consumer,source,scope,lineage,generation); ingress role=(gate,receipt_action,requirements,authentication,context). All four member/native IDs absent for INSTALL; any occupied member/role conflicts. No route-only role lookup or generation fallback.",
  "schema_version": 1
}
```

## Independent operating and installation authority

```json
{
  "authenticity": "Grant/receipt identities and issuer decision supplied by trusted caller independently of definition/request. Replay validates historical accepted receipt without live issuance/authentication.",
  "class": "INSTALL",
  "common": {
    "consumer": "A09",
    "current_policy": {
      "$type": "ArtifactPin",
      "identity": {
        "$type": "ArtifactIdentity",
        "kind": {
          "$enum": "IdentityKind",
          "value": "CONTENT_IDENTITY"
        },
        "namespace": "raw-file-sha256",
        "sha256": "475bef0b28d7b484ba2641c654b37e9ce3d6f6ae1b0e13dfdcadaa3f79a2a3b5"
      },
      "path": "docs/experiments/E1/E1_GRAPH_RESOLUTION_SELECTION_POLICY_1.md",
      "pointer": "",
      "profile": {
        "$enum": "HashProfile",
        "value": "raw-file-sha256"
      }
    },
    "delegation": false,
    "generation": "E2-P03-PROSPECTIVE-GENERATION-1",
    "lineage": "E2-P03-PROSPECTIVE-QUALIFICATION-1",
    "policy_version": "E1-SELECTION-1-P06",
    "scope": "E2-QUALIFICATION-ONLY",
    "validity": [
      0,
      100
    ]
  },
  "issuer_role": "QUALIFICATION_AUTHORITY",
  "operating_ATTEST_separate": {
    "admission_schema": "PLANNER-ATTEST-DEFINITION-ADMISSION-1",
    "already_issued_declaration_rule": "Human may explicitly authorize the exact sealed candidate authority declaration; T04 construction ID alone never proves issuance. Receipt references that declaration exactly; installer must not rerun T04 with changed terms or issue rights.",
    "authorized_subjects": {
      "attestor": {
        "$type": "ArtifactIdentity",
        "kind": {
          "$enum": "IdentityKind",
          "value": "CONTENT_IDENTITY"
        },
        "namespace": "planner-installable-definition-v1",
        "sha256": "de754a27fe4e5d5af166641ae0b674814da4e346ac0283ea203855a93b798f20"
      },
      "authority": {
        "$type": "ArtifactIdentity",
        "kind": {
          "$enum": "IdentityKind",
          "value": "CONTENT_IDENTITY"
        },
        "namespace": "planner-installable-definition-v1",
        "sha256": "dc0986e0358c7ebf087714cb8c489328c4f2a7750e7bdf9534c97ac19f4efec0"
      },
      "authority_predicate": {
        "$type": "ArtifactIdentity",
        "kind": {
          "$enum": "IdentityKind",
          "value": "CONTENT_IDENTITY"
        },
        "namespace": "planner-installable-definition-v1",
        "sha256": "fa0f47cc95ffc93654d2eab28dca5e88987d7dc7e9e6b69bf895780e03ea54db"
      },
      "source_predicate": {
        "$type": "ArtifactIdentity",
        "kind": {
          "$enum": "IdentityKind",
          "value": "CONTENT_IDENTITY"
        },
        "namespace": "planner-installable-definition-v1",
        "sha256": "a8ca10f789e9c2ba32f1666bbb947a5857685fbe752aca6552406c12f7c3e9a3"
      }
    },
    "binding": {
      "consumer": "A09",
      "gate": "E2-GATE",
      "receipt_action": "TEST-RECEIVE",
      "requirement": "E2-EXTERNAL-REQUIREMENT",
      "source": {
        "$type": "ArtifactIdentity",
        "kind": {
          "$enum": "IdentityKind",
          "value": "AUTHORITY_IDENTITY"
        },
        "namespace": "TEST-rule-owner",
        "sha256": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
      }
    },
    "class": "ATTEST",
    "declared_authority_identity": {
      "$type": "ArtifactIdentity",
      "kind": {
        "$enum": "IdentityKind",
        "value": "AUTHORITY_IDENTITY"
      },
      "namespace": "qualification-attest-authority",
      "sha256": "7af52928fbc6b7960e26eb799f97f1e610478a08bec8fed41a3f8af356d4b8ca"
    },
    "generation": "E2-P03-PROSPECTIVE-GENERATION-1",
    "grant_identity": "AUTHORITY_IDENTITY/planner-attest-definition-authorization-v1 = SHA256 canonical issued authorization body excluding own ID/receipt",
    "grant_schema": "PLANNER-ATTEST-DEFINITION-AUTHORIZATION-1",
    "lineage": "E2-P03-PROSPECTIVE-QUALIFICATION-1",
    "live_trust_anchors": [
      "expected operating grant id",
      "expected decision id",
      "qualified issuer role",
      "expected I03 contract/content/member subjects"
    ],
    "permission": "Source-level ATTEST for the exact A09 binding; issue/admit independently before installation. No A09 execution permission.",
    "receipt_content_identity": "raw-file-sha256 exact accepted admission bytes including grant + external trusted issuer/decision/admission-policy references",
    "scope": "E2-QUALIFICATION-ONLY",
    "source": {
      "$type": "ArtifactIdentity",
      "kind": {
        "$enum": "IdentityKind",
        "value": "AUTHORITY_IDENTITY"
      },
      "namespace": "TEST-rule-owner",
      "sha256": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
    },
    "status": "NOT_ISSUED",
    "validity": [
      0,
      100
    ]
  },
  "operating_use": "INSTALL consumes its own one-use configuration grant only. It neither exercises nor consumes operational ATTEST or emits an EvidenceBoundAttestation.",
  "ordered_install_grants": [
    {
      "content_id": {
        "$type": "ArtifactIdentity",
        "kind": {
          "$enum": "IdentityKind",
          "value": "CONTENT_IDENTITY"
        },
        "namespace": "raw-file-sha256",
        "sha256": "072686aaee68ff6f9fa704c45467f93b65cd457955a96200e4578bbe0b0d38a8"
      },
      "definition_id": {
        "$type": "ArtifactIdentity",
        "kind": {
          "$enum": "IdentityKind",
          "value": "CONTENT_IDENTITY"
        },
        "namespace": "planner-installable-definition-v1",
        "sha256": "dfc8ce46edcc16a97967bc139e1c108bb6dfb3c42591681de4bdb644a10c1436"
      },
      "operation": "INSTALL",
      "parent": {
        "$type": "ArtifactIdentity",
        "kind": {
          "$enum": "IdentityKind",
          "value": "CONTENT_IDENTITY"
        },
        "namespace": "planner-event-v1",
        "sha256": "a19b52ab601c6d3c7668b78c6e20cc87e54cfc317595e4da641fcbb7d107fb1e"
      },
      "pre_bundle": {
        "$type": "ArtifactIdentity",
        "kind": {
          "$enum": "IdentityKind",
          "value": "CONTENT_IDENTITY"
        },
        "namespace": "planner-bundle-v1",
        "sha256": "885b23b6f64503153d2d6c4419b160cc278112b26238eecbab14c8b9ecb92ee4"
      },
      "pre_state": {
        "$type": "ArtifactIdentity",
        "kind": {
          "$enum": "IdentityKind",
          "value": "CONTENT_IDENTITY"
        },
        "namespace": "planner-snapshot-v1",
        "sha256": "99e47ad1e462c30cd33e2258e4c74ff670164fa7378e5a998e0f23b9256e4454"
      },
      "sequence": 4,
      "subjects": [
        "authority",
        "authority_predicate",
        "attestor",
        "source_predicate"
      ],
      "type": "AUTHENTICATION_DEFINITION_SET",
      "use_limit": 1
    },
    {
      "content_id": {
        "$type": "ArtifactIdentity",
        "kind": {
          "$enum": "IdentityKind",
          "value": "CONTENT_IDENTITY"
        },
        "namespace": "raw-file-sha256",
        "sha256": "db89cd62739a5d92ff98d5d6db391c45a81d3cfe4a2647adb38e978bf09d1461"
      },
      "definition_id": {
        "$type": "ArtifactIdentity",
        "kind": {
          "$enum": "IdentityKind",
          "value": "CONTENT_IDENTITY"
        },
        "namespace": "planner-installable-definition-v1",
        "sha256": "a41322cc192110fda4ee51f6cd93125231d1b43a7d6238fe905a16dd702bb0a3"
      },
      "operation": "INSTALL",
      "pre_bundle_state_parent": "Issue only after exact authentication installation committed/cold-restored; bind actual resulting bundle/State/head and exact authorized seq4 predecessor. No guessed hashes, wildcard parent, unrelated intervening event or silent rebase.",
      "sequence": 5,
      "type": "EVIDENCE_INGRESS_CONTRACT",
      "use_limit": 1
    }
  ],
  "trusted_transport": "authenticated explicit human decision, outside untrusted payload; no fabricated signature"
}
```

## Operating authority admission wire contract

```json
{
  "application": "Authorize exact sealed declaration prospectively; existing preparation capture is insufficient. No rights are issued by installation.",
  "closed_grant_fields": [
    "schema",
    "authority_class",
    "issuer",
    "issuer_role",
    "authenticated_decision_reference",
    "I03_contract_content_reference",
    "declared_authority_identity",
    "member_definition_and_content_ids",
    "source",
    "consumer",
    "gate",
    "requirement",
    "scope",
    "lineage",
    "generation",
    "valid_from",
    "valid_until",
    "delegation=false",
    "provenance"
  ],
  "closed_receipt_fields": [
    "schema",
    "grant_id",
    "exact_grant_json",
    "trusted_issuer_reference",
    "authenticated_decision_reference",
    "admission_policy_reference",
    "result=ACCEPTED",
    "provenance"
  ],
  "grant_identity": "canonical issued body SHA256 excluding its own identity and receipt",
  "status": "NORMATIVE_NEW_CONTRACT_NOT_IMPLEMENTED",
  "trust": "Independent trusted caller expectations, never self-attested payload fields. Replay consumes previously accepted receipt without issuing authority.",
  "unknown_fields": "REJECT"
}
```

## Dependency order, state advancement and candidate rematerialization

```json
{
  "no_post_state_prediction": "Post-State/Event/bundle hashes derive only from actual accepted issued operands and deterministic transitions; none claimed today.",
  "phase0": "Authenticate human selection; admit exact already-issued ATTEST declaration separately from INSTALL. Do not adopt T04 Snapshot.",
  "phase1": "Atomic seq4 INSTALL authentication set: authority reference + authority predicate + attestor + source-level predicate, all-or-none under one set grant.",
  "phase2": "Verify/cold restore first result, issue exact second INSTALL grant and install ingress at seq5; no unrelated transition allowed.",
  "phase3": "Cold restore/replay complete configuration; derive four-record provenance set, rematerialize transient attestation during A09 ingress preparation and fresh command; only non-mutating preflight in installation package.",
  "staleness": "Current I02 A09 stale after seq4, any interim candidate stale after seq5; latest exact bundle/State/head/key/dependencies/field bindings required."
}
```

## Exact dependency provenance closure

```json
{
  "after_auth_and_ingress_install": [
    {
      "$type": "Provenance",
      "identity": {
        "$type": "ArtifactIdentity",
        "kind": {
          "$enum": "IdentityKind",
          "value": "CONTENT_IDENTITY"
        },
        "namespace": "raw-file-sha256",
        "sha256": "bb528a253ed466ff2fce89cadfdd6a1b0cdab41458651230d733f7455aba2567"
      },
      "method": "P04-PROSPECTIVE-DEFINITION-1",
      "path": "docs/plans/qualification/E2_P04_CONTINUATION_INPUT_CLOSURE_1/resolution-contract.json",
      "scope": "E2-QUALIFICATION-ONLY",
      "section": "/"
    },
    {
      "$type": "Provenance",
      "identity": {
        "$type": "ArtifactIdentity",
        "kind": {
          "$enum": "IdentityKind",
          "value": "CONTENT_IDENTITY"
        },
        "namespace": "raw-file-sha256",
        "sha256": "072686aaee68ff6f9fa704c45467f93b65cd457955a96200e4578bbe0b0d38a8"
      },
      "method": "I03-PROSPECTIVE-DEFINITION-1",
      "path": "docs/plans/qualification/INSTALLATION_I03_1/authentication-set-body.json",
      "scope": "E2-QUALIFICATION-ONLY",
      "section": "/"
    },
    {
      "$type": "Provenance",
      "identity": {
        "$type": "ArtifactIdentity",
        "kind": {
          "$enum": "IdentityKind",
          "value": "CONTENT_IDENTITY"
        },
        "namespace": "raw-file-sha256",
        "sha256": "db89cd62739a5d92ff98d5d6db391c45a81d3cfe4a2647adb38e978bf09d1461"
      },
      "method": "I03-PROSPECTIVE-DEFINITION-1",
      "path": "docs/plans/qualification/INSTALLATION_I03_1/ingress-body.json",
      "scope": "E2-QUALIFICATION-ONLY",
      "section": "/"
    },
    {
      "$type": "Provenance",
      "identity": {
        "$type": "ArtifactIdentity",
        "kind": {
          "$enum": "IdentityKind",
          "value": "CONTENT_IDENTITY"
        },
        "namespace": "raw-file-sha256",
        "sha256": "3a744d47b6c1a69de40652976068b3d438cee276c546cff46d695dd01fca0afd"
      },
      "method": "PROSPECTIVE_AUTHORED_INPUT",
      "path": "docs/plans/qualification/P03_PROSPECTIVE_CHECKPOINT_1/sources/mainline-source-01.json",
      "scope": "E2-QUALIFICATION-ONLY",
      "section": "/"
    }
  ],
  "cardinality": 4,
  "common_auth_source": {
    "$type": "Provenance",
    "identity": {
      "$type": "ArtifactIdentity",
      "kind": {
        "$enum": "IdentityKind",
        "value": "CONTENT_IDENTITY"
      },
      "namespace": "raw-file-sha256",
      "sha256": "072686aaee68ff6f9fa704c45467f93b65cd457955a96200e4578bbe0b0d38a8"
    },
    "method": "I03-PROSPECTIVE-DEFINITION-1",
    "path": "docs/plans/qualification/INSTALLATION_I03_1/authentication-set-body.json",
    "scope": "E2-QUALIFICATION-ONLY",
    "section": "/"
  },
  "common_ingress_source": {
    "$type": "Provenance",
    "identity": {
      "$type": "ArtifactIdentity",
      "kind": {
        "$enum": "IdentityKind",
        "value": "CONTENT_IDENTITY"
      },
      "namespace": "raw-file-sha256",
      "sha256": "db89cd62739a5d92ff98d5d6db391c45a81d3cfe4a2647adb38e978bf09d1461"
    },
    "method": "I03-PROSPECTIVE-DEFINITION-1",
    "path": "docs/plans/qualification/INSTALLATION_I03_1/ingress-body.json",
    "scope": "E2-QUALIFICATION-ONLY",
    "section": "/"
  },
  "gate_requirement_share_full_provenance": true,
  "logical_roles": [
    "ingress",
    "gate",
    "requirement",
    "route",
    "canonical trust/attestor"
  ],
  "no_extra_receipt_dependency": "Operating/INSTALL grant receipts and member sources must be pinned audit/support operands of installation; do not add them arbitrarily to ReceiptAdmission.dependencies, which names the native consumed closure.",
  "rule": "Unchanged full Provenance set equality and exact cardinality in evidence.apply"
}
```

## Currentness

```json
{
  "conjunction": [
    "active complete installed set/ingress role",
    "exact historical event/member witness",
    "physical body/member/policy/receipt pins current",
    "INSTALL authority not invalidated/expired",
    "prior operating ATTEST grant/admission current",
    "exact source/consumer/gate/requirement",
    "exact scope/lineage/generation",
    "native entities usable and exact native AUTHORITY predicate evaluates PROVED"
  ],
  "generation": "T04 authority IDs omit generation internally; never accept on ID equality alone. Native entities, descriptor, grant and current context independently require exact generation.",
  "ingress": "typed canonical ingress matches request-parsed contract exactly, is active and pinned at prefix, and references the current canonical source predicate/attestor/set and installed route",
  "predicate_provenance": "Native Predicate has no Provenance/generation/expiry fields. Derive membership/source/authority/context validity from installed set witness plus exact subject entity; never add an independent TRUE flag.",
  "transient": "Attestation native_entity/content/semantic/proposition/source/gate/scope/lineage/provenance and attestor/authority/predicate chain match canonical inputs; generation enforced via native Evidence ID/context and installed set. No new generation field invented in E02 instance."
}
```

## Atomicity, replacement and idempotence

```json
{
  "idempotence": "Exact request/full payload retry returns original receipt and present active/current status without event/use. Authorized current-head identical active set/ingress is semantic no-op after all independent authority checks. Same identity/different bytes or overlapping IDs/role without exact replacement fails closed. No silent reactivation.",
  "ingress": "Separate complete atomic event; failure may leave the valid auth set installed but ingress absent, A09 unready. Retry from exact accepted historical receipt or exact current head; no invalid partially installed set.",
  "replacement": "P04 INSTALL only. General future REPLACE requires exact whole-set predecessor and explicit replacement authority; never replace one member independently. SUPERSEDE is explicit whole-set retirement relation, not new generation/role fallback.",
  "set": "One authentication set grant/request/installed record/event atomically projects all four members. No public member-by-member commits or dangling predicate. Keep old canonical head until full validated body/authority/projection/pins/event durable; reuse I02 lock/CAS/fsync/HEAD protocol."
}
```

## Invalidation

```json
{
  "effect": "Withdraw set/ingress currentness and authentication predicate support at bounded dependent A09 consumer; reject stale commands/transient attestations. Preserve historical event/members, no predecessor fallback.",
  "native_projection": "Consumer guard must consult set/member/admission validity, not just GraphEntity.validation. Ordinary invalidation marks affected typed support stale via native transition; no manual CURRENT/status mutation.",
  "post_receipt": "Any accepted Evidence support depending on this authentication must become unusable through ordinary bounded dependency invalidation; historical receipt preserved. This contract installs no receipt/result/proof.",
  "triggers": [
    "INSTALL authority invalidation/expiry",
    "operating ATTEST invalidation/expiry",
    "attestor or member/predicate invalidation",
    "definition/member/receipt/source invalidation",
    "generation supersession",
    "scope/lineage/context mismatch"
  ]
}
```

## Persistence and historical replay

```json
{
  "pure_replay": "Replay historical already-accepted authority and installation at exact pre-state/parent/sequence. No human prompt, new operating/INSTALL issuance, T04 re-materialization with new inputs, attestation generation, Evidence admission or Action execution.",
  "qualification": "Future tests: generic non-E2 fixtures, cold restore after each boundary, actual writer termination, three fresh readers/checkpoint/seed 0/1/7/101, unordered native permutations and ordered event equality, invalidation, crash-before/after commit, exact retries and all defined negatives. Not executed by I03.",
  "required": [
    "all aggregate/member/ingress bytes and content/definition IDs",
    "canonical native entity/predicate/ingress projections",
    "authority references, issued operating/INSTALL grant+accepted receipt operands",
    "member/set witnesses",
    "exact dependency Provenance",
    "source/policy pins/context",
    "ordinary events/root/head/use history"
  ],
  "temporal": "Before seq4 no members; after seq4 all four; before seq5 ingress absent; after seq5 ingress present. Filter later config sources from old prefixes, preserve absence and exact I02 prefix bytes."
}
```

## Replay requirements

```json
{
  "pure_replay": "Replay historical already-accepted authority and installation at exact pre-state/parent/sequence. No human prompt, new operating/INSTALL issuance, T04 re-materialization with new inputs, attestation generation, Evidence admission or Action execution.",
  "qualification": "Future tests: generic non-E2 fixtures, cold restore after each boundary, actual writer termination, three fresh readers/checkpoint/seed 0/1/7/101, unordered native permutations and ordered event equality, invalidation, crash-before/after commit, exact retries and all defined negatives. Not executed by I03.",
  "required": [
    "all aggregate/member/ingress bytes and content/definition IDs",
    "canonical native entity/predicate/ingress projections",
    "authority references, issued operating/INSTALL grant+accepted receipt operands",
    "member/set witnesses",
    "exact dependency Provenance",
    "source/policy pins/context",
    "ordinary events/root/head/use history"
  ],
  "temporal": "Before seq4 no members; after seq4 all four; before seq5 ingress absent; after seq5 ingress present. Filter later config sources from old prefixes, preserve absence and exact I02 prefix bytes."
}
```

## Bounded human decision

```json
{
  "SELECTED_OPTION": "NONE",
  "admission_receipts_today": null,
  "authorize": "After adapter implementation qualification, authenticate exact I03 sealed set/member/ingress IDs/content/source/context/pre-head/policy. Separately issue/admit scoped operational ATTEST authorization naming exact sealed declaration; issue bounded INSTALL set grant; after its verified exact result issue bounded ingress grant against actual descendant head. No installation may issue operating authority; no wildcard or silent term change.",
  "bounded_subjects": {
    "authentication_set": {
      "$type": "ArtifactIdentity",
      "kind": {
        "$enum": "IdentityKind",
        "value": "CONTENT_IDENTITY"
      },
      "namespace": "planner-installable-definition-v1",
      "sha256": "dfc8ce46edcc16a97967bc139e1c108bb6dfb3c42591681de4bdb644a10c1436"
    },
    "ingress": {
      "$type": "ArtifactIdentity",
      "kind": {
        "$enum": "IdentityKind",
        "value": "CONTENT_IDENTITY"
      },
      "namespace": "planner-installable-definition-v1",
      "sha256": "a41322cc192110fda4ee51f6cd93125231d1b43a7d6238fe905a16dd702bb0a3"
    },
    "members": {
      "attestor": {
        "$type": "ArtifactIdentity",
        "kind": {
          "$enum": "IdentityKind",
          "value": "CONTENT_IDENTITY"
        },
        "namespace": "planner-installable-definition-v1",
        "sha256": "de754a27fe4e5d5af166641ae0b674814da4e346ac0283ea203855a93b798f20"
      },
      "authority": {
        "$type": "ArtifactIdentity",
        "kind": {
          "$enum": "IdentityKind",
          "value": "CONTENT_IDENTITY"
        },
        "namespace": "planner-installable-definition-v1",
        "sha256": "dc0986e0358c7ebf087714cb8c489328c4f2a7750e7bdf9534c97ac19f4efec0"
      },
      "authority_predicate": {
        "$type": "ArtifactIdentity",
        "kind": {
          "$enum": "IdentityKind",
          "value": "CONTENT_IDENTITY"
        },
        "namespace": "planner-installable-definition-v1",
        "sha256": "fa0f47cc95ffc93654d2eab28dca5e88987d7dc7e9e6b69bf895780e03ea54db"
      },
      "source_predicate": {
        "$type": "ArtifactIdentity",
        "kind": {
          "$enum": "IdentityKind",
          "value": "CONTENT_IDENTITY"
        },
        "namespace": "planner-installable-definition-v1",
        "sha256": "a8ca10f789e9c2ba32f1666bbb947a5857685fbe752aca6552406c12f7c3e9a3"
      }
    }
  },
  "decline": "Issue no new operating/INSTALL authority and append no config event; prepared definitions remain offline, DEPENDENCY_PROVENANCE remains unresolved and P04 readiness NO.",
  "exclusions": [
    "A09-A13",
    "Evidence-bound attestation creation/ingress execution",
    "unrelated Action/result/validation/proof/root-slot installation",
    "P03/historical/N-REAL/release changes",
    "GENESIS",
    "production effects"
  ],
  "grant_ids_today": null,
  "material_change": "If any sealed member/body/identity/subject/context or prospective source pin changes after decision, STOP. Do not silently reinterpret old T04 IDs. Issue a revised reviewable scope decision.",
  "options": [
    "AUTHORIZE_P04_ATTEST_INGRESS_INSTALLATION",
    "DECLINE_P04_ATTEST_INGRESS_INSTALLATION"
  ],
  "preconditions": [
    "human explicitly selects authorize option",
    "I03 contracts and sealed candidate identities unchanged",
    "native adapters/operating authority admission and consumer guards qualified before applying P04",
    "exact I02 pre-head unchanged",
    "both authority classes independently admitted/current"
  ],
  "ready": true,
  "required": true,
  "subject": "Authorize exact scoped P04 authentication definitions and ingress configuration; two ordered installations, no A09 execution"
}
```

## P04 provenance set

The expected set is prospective, not currently canonical. Compare full Provenance objects, including physical path, section, excerpt, identity, scope and method. Five logical consumed roles reduce to four records because gate and requirement share exactly the same provenance. Installation grant/receipt sources belong to the installation audit closure, not arbitrary extra A09 dependencies.

- `docs/plans/qualification/E2_P04_CONTINUATION_INPUT_CLOSURE_1/resolution-contract.json` — `bb528a253ed466ff2fce89cadfdd6a1b0cdab41458651230d733f7455aba2567`.
- `docs/plans/qualification/INSTALLATION_I03_1/authentication-set-body.json` — `072686aaee68ff6f9fa704c45467f93b65cd457955a96200e4578bbe0b0d38a8`.
- `docs/plans/qualification/INSTALLATION_I03_1/ingress-body.json` — `db89cd62739a5d92ff98d5d6db391c45a81d3cfe4a2647adb38e978bf09d1461`.
- `docs/plans/qualification/P03_PROSPECTIVE_CHECKPOINT_1/sources/mainline-source-01.json` — `3a744d47b6c1a69de40652976068b3d438cee276c546cff46d695dd01fca0afd`.

## Security qualification suite

All following cases are specified fail-closed oracles for future implementation qualification. They have not been executed as runtime installation tests in I03.

- {"case": "attestor_without_predicate", "id": "I03-N01", "oracle": "Reject/withdraw use fail closed; preserve prior canonical head/state/uses/history. Reject admission before any Evidence/receipt; no partial authentication set or dangling predicate.", "status": "DEFINED_NOT_EXECUTED"}
- {"case": "predicate_without_attestor", "id": "I03-N02", "oracle": "Reject/withdraw use fail closed; preserve prior canonical head/state/uses/history. Reject admission before any Evidence/receipt; no partial authentication set or dangling predicate.", "status": "DEFINED_NOT_EXECUTED"}
- {"case": "wrong_predicate_subject", "id": "I03-N03", "oracle": "Reject/withdraw use fail closed; preserve prior canonical head/state/uses/history. Reject admission before any Evidence/receipt; no partial authentication set or dangling predicate.", "status": "DEFINED_NOT_EXECUTED"}
- {"case": "wrong_attestor", "id": "I03-N04", "oracle": "Reject/withdraw use fail closed; preserve prior canonical head/state/uses/history. Reject admission before any Evidence/receipt; no partial authentication set or dangling predicate.", "status": "DEFINED_NOT_EXECUTED"}
- {"case": "wrong_ATTEST_authority", "id": "I03-N05", "oracle": "Reject/withdraw use fail closed; preserve prior canonical head/state/uses/history. Reject admission before any Evidence/receipt; no partial authentication set or dangling predicate.", "status": "DEFINED_NOT_EXECUTED"}
- {"case": "wrong_source", "id": "I03-N06", "oracle": "Reject/withdraw use fail closed; preserve prior canonical head/state/uses/history. Reject admission before any Evidence/receipt; no partial authentication set or dangling predicate.", "status": "DEFINED_NOT_EXECUTED"}
- {"case": "wrong_consumer", "id": "I03-N07", "oracle": "Reject/withdraw use fail closed; preserve prior canonical head/state/uses/history. Reject admission before any Evidence/receipt; no partial authentication set or dangling predicate.", "status": "DEFINED_NOT_EXECUTED"}
- {"case": "wrong_scope", "id": "I03-N08", "oracle": "Reject/withdraw use fail closed; preserve prior canonical head/state/uses/history. Reject admission before any Evidence/receipt; no partial authentication set or dangling predicate.", "status": "DEFINED_NOT_EXECUTED"}
- {"case": "wrong_lineage", "id": "I03-N09", "oracle": "Reject/withdraw use fail closed; preserve prior canonical head/state/uses/history. Reject admission before any Evidence/receipt; no partial authentication set or dangling predicate.", "status": "DEFINED_NOT_EXECUTED"}
- {"case": "wrong_generation", "id": "I03-N10", "oracle": "Reject/withdraw use fail closed; preserve prior canonical head/state/uses/history. Reject admission before any Evidence/receipt; no partial authentication set or dangling predicate.", "status": "DEFINED_NOT_EXECUTED"}
- {"case": "offline_definition_as_installed", "id": "I03-N11", "oracle": "Reject/withdraw use fail closed; preserve prior canonical head/state/uses/history. Reject admission before any Evidence/receipt; no partial authentication set or dangling predicate.", "status": "DEFINED_NOT_EXECUTED"}
- {"case": "Evidence_bound_attestation_as_definition", "id": "I03-N12", "oracle": "Reject/withdraw use fail closed; preserve prior canonical head/state/uses/history. Reject admission before any Evidence/receipt; no partial authentication set or dangling predicate.", "status": "DEFINED_NOT_EXECUTED"}
- {"case": "route_REPLACE_grant_for_authentication", "id": "I03-N13", "oracle": "Reject/withdraw use fail closed; preserve prior canonical head/state/uses/history. Reject admission before any Evidence/receipt; no partial authentication set or dangling predicate.", "status": "DEFINED_NOT_EXECUTED"}
- {"case": "metadata_wrapper_as_body", "id": "I03-N14", "oracle": "Reject/withdraw use fail closed; preserve prior canonical head/state/uses/history. Reject admission before any Evidence/receipt; no partial authentication set or dangling predicate.", "status": "DEFINED_NOT_EXECUTED"}
- {"case": "unissued_operating_authority", "id": "I03-N15", "oracle": "Reject/withdraw use fail closed; preserve prior canonical head/state/uses/history. Reject admission before any Evidence/receipt; no partial authentication set or dangling predicate.", "status": "DEFINED_NOT_EXECUTED"}
- {"case": "self_authenticated_issuer", "id": "I03-N16", "oracle": "Reject/withdraw use fail closed; preserve prior canonical head/state/uses/history. Reject admission before any Evidence/receipt; no partial authentication set or dangling predicate.", "status": "DEFINED_NOT_EXECUTED"}
- {"case": "INSTALL_issues_ATTEST", "id": "I03-N17", "oracle": "Reject/withdraw use fail closed; preserve prior canonical head/state/uses/history. Reject admission before any Evidence/receipt; no partial authentication set or dangling predicate.", "status": "DEFINED_NOT_EXECUTED"}
- {"case": "partial_set_publication", "id": "I03-N18", "oracle": "Reject/withdraw use fail closed; preserve prior canonical head/state/uses/history. Reject admission before any Evidence/receipt; no partial authentication set or dangling predicate.", "status": "DEFINED_NOT_EXECUTED"}
- {"case": "ingress_before_current_auth_set", "id": "I03-N19", "oracle": "Reject/withdraw use fail closed; preserve prior canonical head/state/uses/history. Reject admission before any Evidence/receipt; no partial authentication set or dangling predicate.", "status": "DEFINED_NOT_EXECUTED"}
- {"case": "stale_foreign_or_parentless_install", "id": "I03-N20", "oracle": "Reject/withdraw use fail closed; preserve prior canonical head/state/uses/history. Reject admission before any Evidence/receipt; no partial authentication set or dangling predicate.", "status": "DEFINED_NOT_EXECUTED"}
- {"case": "stale_A09_after_install", "id": "I03-N21", "oracle": "Reject/withdraw use fail closed; preserve prior canonical head/state/uses/history. Reject admission before any Evidence/receipt; no partial authentication set or dangling predicate.", "status": "DEFINED_NOT_EXECUTED"}
- {"case": "extra_missing_duplicate_dependency_provenance", "id": "I03-N22", "oracle": "Reject/withdraw use fail closed; preserve prior canonical head/state/uses/history. Reject admission before any Evidence/receipt; no partial authentication set or dangling predicate.", "status": "DEFINED_NOT_EXECUTED"}
- {"case": "conflicting_retry_or_content_identity", "id": "I03-N23", "oracle": "Reject/withdraw use fail closed; preserve prior canonical head/state/uses/history. Reject admission before any Evidence/receipt; no partial authentication set or dangling predicate.", "status": "DEFINED_NOT_EXECUTED"}
- {"case": "source_path_overwrite_or_symlink", "id": "I03-N24", "oracle": "Reject/withdraw use fail closed; preserve prior canonical head/state/uses/history. Reject admission before any Evidence/receipt; no partial authentication set or dangling predicate.", "status": "DEFINED_NOT_EXECUTED"}
- {"case": "expired_revoked_or_superseded_support", "id": "I03-N25", "oracle": "Reject/withdraw use fail closed; preserve prior canonical head/state/uses/history. Reject admission before any Evidence/receipt; no partial authentication set or dangling predicate.", "status": "DEFINED_NOT_EXECUTED"}
- {"case": "replay_reissues_authority_or_attestation", "id": "I03-N26", "oracle": "Reject/withdraw use fail closed; preserve prior canonical head/state/uses/history. Reject admission before any Evidence/receipt; no partial authentication set or dangling predicate.", "status": "DEFINED_NOT_EXECUTED"}
- {"case": "pre_install_replay_sees_new_members", "id": "I03-N27", "oracle": "Reject/withdraw use fail closed; preserve prior canonical head/state/uses/history. Reject admission before any Evidence/receipt; no partial authentication set or dangling predicate.", "status": "DEFINED_NOT_EXECUTED"}
- {"case": "operating_grant_consumed_by_install", "id": "I03-N28", "oracle": "Reject/withdraw use fail closed; preserve prior canonical head/state/uses/history. Reject admission before any Evidence/receipt; no partial authentication set or dangling predicate.", "status": "DEFINED_NOT_EXECUTED"}
- {"case": "unrelated_definition_or_lifecycle_changed", "id": "I03-N29", "oracle": "Reject/withdraw use fail closed; preserve prior canonical head/state/uses/history. Reject admission before any Evidence/receipt; no partial authentication set or dangling predicate.", "status": "DEFINED_NOT_EXECUTED"}
- {"case": "authority_receipt_or_body_missing_after_commit", "id": "I03-N30", "oracle": "Reject/withdraw use fail closed; preserve prior canonical head/state/uses/history. Reject admission before any Evidence/receipt; no partial authentication set or dangling predicate.", "status": "DEFINED_NOT_EXECUTED"}
- {"case": "wrong_transient_authority_predicate_attestor_chain", "id": "I03-N31", "oracle": "Reject/withdraw use fail closed; preserve prior canonical head/state/uses/history. Reject admission before any Evidence/receipt; no partial authentication set or dangling predicate.", "status": "DEFINED_NOT_EXECUTED"}
- {"case": "forged_transient_attestation_id", "id": "I03-N32", "oracle": "Reject/withdraw use fail closed; preserve prior canonical head/state/uses/history. Reject admission before any Evidence/receipt; no partial authentication set or dangling predicate.", "status": "DEFINED_NOT_EXECUTED"}

## Contract readiness and preservation

Sealed body hashes/native decoding/reference projections and source-set cardinality were checked offline against the cold-restored I02 checkpoint. No post-install state/event/bundle IDs are claimed. Actual issued authority operands and deterministic transition results will determine those identities. Broad runtime regressions and new-adapter negative execution belong to the implementation package; no runtime change was made here.

```text
WORK_PACKAGE = INSTALLATION-I03-ATTEST-INGRESS-CONTRACT
RESULT = PASS
ATTESTOR_INSTALLABILITY = INSTALLABLE_WITH_TYPED_ADAPTER_AS_ATOMIC_SET_MEMBER
PREDICATE_INSTALLABILITY = INSTALLABLE_WITH_TYPED_ADAPTER_AS_ATOMIC_SET_MEMBER
INSTALL_AUTHORITY_CLASS = INSTALL
EVIDENCE_BOUND_ATTESTATION = A09_LIFECYCLE_INSTANCE_NOT_PROSPECTIVE_DEFINITION
P04_ATTEST_INSTALLATION_DECISION_REQUIRED = YES
P04_ATTEST_INSTALLATION_DECISION_READY = YES
ATTEST_INSTALLATION_IMPLEMENTATION_READY = YES
SELECTED_OPTION = NONE
AUTHORITY_ISSUED = NO
ATTESTOR_INSTALLED = NO
PREDICATE_INSTALLED = NO
INGRESS_INSTALLED = NO
P04_EXECUTION_READY = NO
E2_P04_READY = NO
A09_EXECUTED = NO
P04_LIFECYCLE_ADVANCEMENT = NO
P03_RESULT = PASS
P03_HISTORICAL_CORRESPONDENCE = UNPROVEN
N_REAL_SATISFIED = NO
RUNTIME_MODIFIED = NO
E2_FINISH_EXECUTED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
git diff --check = PASS
```

The existing dirty workspace was preserved. Hash comparisons cover prior Planner and qualification artifacts and frozen E1. The human options remain unselected. Neither option implies A09 execution, P04 readiness, changes to P03 scope, historical reconstruction or release qualification.

[Machine-readable contract](DETERMINISTIC_PLANNER_V0_1_INSTALLATION_I03_ATTEST_INGRESS_CONTRACT.json) contains the complete bytes/pins, adapter rules, sealed mapping, authority matrix, expected provenance objects and preservation evidence.
