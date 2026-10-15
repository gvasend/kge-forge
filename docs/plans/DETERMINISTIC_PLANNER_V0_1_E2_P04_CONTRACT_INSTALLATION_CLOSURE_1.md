# E2-P04 prospective contract installation / route currentness closure 1

WORK_PACKAGE = E2-P04-CONTRACT-INSTALLATION-CLOSURE  
RESULT = BLOCKED  
INITIAL_PARENT_PREFLIGHT = PASS  
INITIAL_FAILURE = ROUTE_NOT_CURRENT  
ROUTE_CURRENTNESS_CLOSED = NO  
P04_EXECUTION_READY = NO

The fresh A09 candidate reproduces the exact parent-bound native failure. The prepared route source already has the correct identity domain and exact canonical fields. However, there is **no existing native definition/source installation event or complete installation-authority contract** for admitting it into the preserved checkpoint lineage. Phase I's prerequisite is therefore not met: no route is installed, P03 is not rewritten, and no A09–A13 operation is accepted.

## Exact route trace

Native `evidence.apply` checks the fresh command's schema/key, Snapshot parent, active gate, ingress context and exact route bindings, then requires `gates.governed_external_unknown`. That predicate returns false and produces ROUTE_NOT_CURRENT. The parent bundle/State/event/context checks all pass.

| Field | Exact value / finding |
| --- | --- |
| ROUTE_ID | Logical lookup `(GateId E2-GATE, EvidenceId E2-EXTERNAL-REQUIREMENT)`; native model has no RouteId field. |
| ROUTE_TYPE | ExternalResolutionContract. |
| ROUTE_SOURCE | `docs/plans/qualification/P03_PROSPECTIVE_CHECKPOINT_1/sources/mainline-source-08.json`, provenance section `/`. |
| ROUTE_PIN | CONTENT_IDENTITY/raw-file-sha256 `76a1358ea02e5657fb4819905c86b577d5f9d37c86c76a6f312b310fa26a653b`. |
| EXPECTED_SOURCE | Canonical UTF-8 JSON `EXTERNAL-RESOLUTION-CONTRACT-1`, with `contract` equal to the complete native route projection excluding `$type` and provenance. |
| ACTUAL_SOURCE | Qualification metadata wrapper with authored_initial_premise, generation, historical_reconstruction, lineage, qualification_type, scope, scope_decision and nested template_provenance. |
| SCOPE / LINEAGE | E2-QUALIFICATION-ONLY / E2-P03-PROSPECTIVE-QUALIFICATION-1; generation E2-P03-PROSPECTIVE-GENERATION-1. |
| CONSUMER | E2-REENTER; its evidence-obligation predicate is independently required. |

The expected `/schema` and every `/contract/<field>` are missing at those paths in the actual source. Outer metadata includes context strings but not the native contract envelope. Its nested `template_provenance.excerpt` contains historical TEST-GATE/TEST-RULE/TEST-ACTION/TEST context and source bindings; it is neither the current contract source nor a permitted alternate projection. Native currentness does not recursively interpret template metadata.

All current typed route-to-gate fields—scope/lineage/generation, gate/requirement, proposition/target/producer, gate and requirement source identities, receipt/reentry/held-action references—match the current Snapshot. The failed checks are exact source bytes and the expected source-content digest. The actual pin correctly hashes its metadata file; authenticating those bytes does not make them canonical route-contract bytes. The [machine trace](qualification/E2_P04_CONTRACT_INSTALLATION_CLOSURE_1/native-trace.json) enumerates every field and both full sources.

The [prepared source](qualification/E2_P04_CONTINUATION_INPUT_CLOSURE_1/resolution-contract.json) is byte-for-byte the required canonical route projection. Its distinct raw-file identity is independently derived in the trace. No wrong identity domain was found in this prepared file. It is a valid offline definition source, **not an installed CURRENT route**.

## Identity and currentness domains

The logical route lookup key, raw route-source content identity, ArtifactPin's physical path/profile/pointer binding, producer AUTHORITY_IDENTITY, target CANONICAL_OBJECT_IDENTITY, and native Snapshot/bundle/event identities have different roles. None is substituted for another. The prepared raw source hash does not grant permission to replace the canonical route or extend its source index.

Route currentness is a **derived Snapshot predicate**, bound to scope/lineage/generation, allowed gate stage/accepted validation, exact requirement/consumer references, and canonical provenance bytes/hash. It has no stored CURRENT flag or native DEFINED→ADMITTED→CURRENT enum. Those terms mean:

- DEFINED: typed route object/draft exists.
- ADMITTED: whole model validation is available; no independent route-installation event exists.
- BOUND: exact gate/requirement/context/source/consumer correspondences.
- CURRENT/APPLICABLE: computed native route predicate for this consumer, followed by wider ingress/current support/authentication requirements for admission.
- INVALIDATED/STALE: native support/gate validation is withdrawn or context/source correspondence fails; historical route obligations remain.

The route itself has no `valid_until` or parent-event field. Wider support and authority checks handle expiry/currentness. Codec source/policy verification enforces physical files; event/admission replay authenticates expected bundle/State/parent and prefix source index. Thus a true isolated route predicate alone does not prove bundle admission, physical source-prefix membership, authority or legitimate ancestry.

An isolated, unsaved definition oracle with the exact prepared source computes a true route predicate. The canonical checkpoint still computes false. This diagnostic never replaces the bundle's initial/current state, marks a definition current, or emits a new event/bundle.

## Native installation contract and authority

Inspected native model/dispatch/codec admit only SuppliedResult, RecordedDecision, DecisionReentry, ExternalEvent, SourceInvalidation, EvidenceSourceAdmission, TypedProofAdmission, ProofDependencyChange and ActionReevaluation. None installs external routes, source-contract pins, authority/predicate definitions, Action accepted-result models or proof/root/slot contracts. EvidenceSourceAdmission permits the payload source addition; its ingress and field-provenance sources must already be in the preceding source index. SourceInvalidation only withdraws support.

T04 and E05 construct offline definitions/new fixture Snapshots. E06 admits proof **instances against existing contracts**, not proof contracts themselves. G04 establishes a new event-lineage start and cannot preserve this prefix by resetting history. Native restore/replay detects a replaced current state that lacks supporting events. No supported configuration event or authority-governed bundle transformation was found.

INSTALLATION_MECHANISM = **NEW_RUNTIME_CAPABILITY_REQUIRED after CONTRACT_COMPLETION**. The current task authorizes this investigation and any minimum supported installation; it does not supply the missing typed transaction/applicability/replay semantics. No generic INSTALL authority class, permission target or installer behavior is invented here.

| Definition class | Required authority domain | Existing installed support | Installation applicability |
| --- | --- | --- | --- |
| External route | Admission/replacement for exact named gate/requirement and preserved context | Qualification preparation capture; no configuration grant | Unestablished |
| Source pin | Admission of immutable provenance bytes into preserved source prefix | Existing pins authenticate existing bytes only | Unestablished |
| ATTEST | Scoped authority/attestor/predicate admission, distinct from later evidence authentication | Offline candidates; native USE/DECIDE do not authorize this domain | Unestablished |
| Action result contract | Exact authored definition/output contract admission without Action completion | PC01 semantics/offline E05 inventories | Unestablished |
| Validation contract | Validator/input/persistence contract admission | Qualified E04 helper, no installation event | Unestablished |
| Typed proof contracts | Contract target/support/currentness admission, distinct from proof instance | Offline E06 contract candidates | Unestablished |
| Root/slot fixture | Exact prospective targets/relationships and fixture applicability | Offline prepared authority/fixture sources | Unestablished |

The required native authority class/reference rules are **contract-incomplete**, not silently mapped to ATTEST, DECIDE, USE or GENESIS. Whether a new authority record is required versus an existing qualified issuer can authorize installation must be specified by that contract. No repeated human consent is requested; requested work is already authorized. The missing item is native domain/applicability semantics and admission support.

## Ownership, DAG and state effects

The canonical plan requires P01 complete definition/interface preflight, forbids post-restore Snapshot replacement/reset/repin bypass, and allocates A09–A13 to P04. It does not define post-checkpoint configuration installation. If a native contract is established, this prospective installation belongs to **P04 configuration/preparation**, not fabricated P03 history. At present that is a proposed ownership classification, not an admitted operation or an acceptance amendment.

FIRST_INSTALLATION_PACKAGE = **P04-INSTALL-CONTRACT**, followed by minimum **P04-ROUTE-INSTALL-CAPABILITY**. Route currentness is the first native failure, but legitimate installation requires the authority/event contract first. Then ordered work is ingress/ATTEST installation and attestation commit/replay integration; Action/fixture/proof-definition installation; A10/A11 validation/proof persistence qualification; and final input/oracle resealing. Independent branches can be separately qualified; no unsupported all-definition atomic transaction is presumed.

The future contract must define expected bundle/State/parent/policy/context; exact old/new definition and physical source identities; class-separated authority applicability; permitted replacements/references; atomic source/definition publication; event hashing; idempotence/conflict rules; invalidation; and fail-closed type/provenance/scope/lineage checks. Replay must reproduce **historical configuration**, without fresh authority issuance, Evidence receipt, ValidationResult creation, proof admission, Action completion or root/slot satisfaction. No runtime implementation can be qualified from an unspecified authority contract.

PRE_INSTALL_STATE_ID = `planner-snapshot-v1:576fe3a99286bcbceee1587dedf7db8e3073517e251d6a064821f286b77b5324`  
POST_INSTALL_STATE_ID = NONE  
INSTALL_EVENT_ID = NONE  
POST_INSTALL_APPEND_HEAD = NONE

No installation occurred; the canonical current state and actual append head remain unchanged. A future configuration event must preserve the initial checkpoint and prior event identities while changing its current definition/source state and appending a real event. Even a source-index-only change alters bundle identity; route/authority/Action changes alter Snapshot bytes. The fresh A09 candidate must then be rematerialized for the **actual new bundle, Snapshot and append head**. An obsolete parent cannot be retained to reuse a candidate. No new event identity is guessed here.

## Closure, persistence and negatives

Phase I installation is conditional on a complete contract and existing native support. Neither is established. ROUTE_INSTALLATION = NOT EXECUTED; ROUTE_CURRENTNESS_CLOSED = NO. Existing checkpoint trust/physical pins/cold restore/replay pass, but no installed-route serialization/cold/replay is claimed.

A09_CANDIDATE_REMATERIALIZED = NO: the prior candidate still binds the unchanged checkpoint exactly. A09_PREFLIGHT_AFTER_ROUTE = NOT RUN because no route was installed. NEXT_FAILURE = NOT OBSERVED; ROUTE_NOT_CURRENT remains the actual first failure. Unreached ingress/authority clauses are dependency findings, not a claimed next native preflight result.

The read-only [trace harness](../../adapter/tests/trace_e2_p04_installation.py) qualifies eight route/policy/parent diagnostic negatives: wrong source bytes, route hash, source identity domain, scope, lineage, stale gate validation, policy pin and parent identity. These are native predicate/policy or explicit exact-parent checks on isolated fixtures; they do **not** qualify an installer. Wrong installation authority, unauthorized definition installation, proof INSTANCE substituted for CONTRACT and ActionResult substituted for accepted-result CONTRACT remain explicit **NOT QUALIFIED** requirements because no installation interface exists. They must fail atomically in the future installer; they are not labeled PASS here.

DEFINITION_STATUS: ATTEST and VALIDATION are contract-blocked; Action/proof/root/slot/source installation is runtime-blocked under incomplete authority/event contracts. Prepared definitions are not ALREADY_CURRENT. The minimum ordered packages and exact dependency DAG are in the [machine-readable result](DETERMINISTIC_PLANNER_V0_1_E2_P04_CONTRACT_INSTALLATION_CLOSURE_1.json).

## Preservation

P04_EXECUTION_READY = NO  
E2_P04_READY = NO  
P03_RESULT = PASS  
P03_HISTORICAL_CORRESPONDENCE = UNPROVEN  
N_REAL_SATISFIED = NO  
A09_EXECUTED = NO  
A10_EXECUTED = NO  
A11_EXECUTED = NO  
A12_EXECUTED = NO  
A13_EXECUTED = NO  
E2_FINISH_EXECUTED = NO  
RUNTIME_MODIFIED = NO  
E1_ARTIFACTS_MODIFIED = 0  
PRODUCTION_EFFECT = NO  
git diff --check = PASS

Only new read-only diagnostic evidence/harness and this result pair are written. Every prior artifact, prepared input, native runtime Python file and frozen-E1 file in the preservation inventory remains unchanged. No installation is represented as lifecycle execution, and no unsuccessful counterexample is promoted into a runtime repair or qualified route.
