# Installation I01 — Authority and contract-installation event contract

WORK_PACKAGE = INSTALLATION-I01  
RESULT = PASS — **semantics only**  
INSTALLATION_IMPLEMENTATION_READY = YES for the generic protocol and first route adapter  
ROUTE_INSTALLED = NO  
P04_EXECUTION_READY = NO

Installation means: **definition D is authorized to become canonical beginning at event E in lineage L**. It neither makes D exist in earlier states nor executes the lifecycle governed by D. This document defines a future generic native extension; it does not add an enum, event type, installer or authority to the current runtime.

## Installable definition and identities

The closed `PLANNER-INSTALLABLE-DEFINITION-1` descriptor requires definition_id, definition_type, canonical body schema/bytes or immutable source reference, content_id, subject, scope, lineage, generation, exact physical source pin, provenance and currentness rule. The registered type adapter must prove complete native canonical-body equality and subject/context correspondence. Metadata wrapper bytes cannot stand in for a body. The first enabled type is EXTERNAL_RESOLUTION_CONTRACT; the representation is generic, but the adapter registry is closed and reviewed.

Use existing `codec.canonical_bytes` for descriptor dictionaries. Each type's body follows its native codec, including declared unordered collections; event histories and policy clauses remain ordered. Reject duplicate keys, unknown fields, wrong projection/schema or noncanonical source bytes. No dynamic evaluator or unreviewed definition type is accepted. Definition content excludes self-referential provenance where its native schema requires that; the enclosing descriptor independently binds exact path, section, method and raw content pin.

| Identity | Meaning / construction |
| --- | --- |
| Qualification artifact | Report/evidence identity only. |
| Metadata wrapper | Raw hash authenticates metadata bytes only. |
| Definition content | CONTENT_IDENTITY/raw-file-sha256 over exact native body bytes. |
| DEFINITION_ID | CONTENT_IDENTITY/planner-installable-definition-v1; SHA-256 of closed descriptor excluding its own ID and transport bytes. Content/type/subject/context/source/provenance/currentness rule all included. |
| AUTHORITY_ID | AUTHORITY_IDENTITY/planner-install-authority-v1; deterministic issued-grant body, excluding own ID and authentication receipt; issuance/provenance references included. |
| REQUEST_KEY | CONTENT_IDENTITY/planner-install-command-v1; exact request minus its own key, including expected head/state/bundle/policy and authority/operation/old-reference. |
| INSTALLED_DEFINITION_ID | INSTANCE_IDENTITY/planner-installed-definition-v1; exact request_key, definition_id, authority_id, role, operation, parent event, activation sequence and context. |
| INSTALL event ID | Existing planner-event-v1 algebra, computed after post-Snapshot identity exists. |
| Baseline definition reference | planner-baseline-definition-reference-v1 binds the exact trusted pre-existing native record/source/role/pre-state. It is not an invented old installation. |

No arbitrary UUID or clock nonce supplies identity. The logical role key is `(definition_type, subject, scope, lineage, generation)`.

**Hash-cycle rule:** the installed record stores request_key, parent_event and activation_sequence, not its own activation event hash inside the hashed Snapshot. Replay joins that record to exactly one ledger event at that sequence with matching request/definition. The post-state is hashed first, then its ExecutionEvent identity. This proves activation at E without circular event-ID/post-state hashing.

## Installation authority and issuer

INSTALL is the minimum **new proposed authority class**. Existing CONSTRUCT, ISSUE, USE, RELEASE, EXPAND, IMPLEMENT_TEST, DECIDE, ATTEST and GENESIS have no reviewed generic prospective-installation semantics; none is reused by inference. INSTALL is distinct from qualification-fixture permission and Action execution. A qualification role may issue INSTALL, but a fixture DECIDE/ATTEST/GENESIS grant is not an INSTALL grant.

An issued grant requires authority_id/class, issuer_id/role, issuance decision and verified authentication receipt, permitted definition type/operation, exact definition or explicitly enumerated finite set, subject, exact predecessor reference, expected pre-bundle/state/parent, exact policy pin/version, scope/lineage/generation, tick validity, use limit, provenance and currentness rule. Default is exact definition; class-wide wildcards are not supported in I01. Replacement permission is explicit.

Applicability is a conjunction: authenticated admitted issuer/receipt/provenance; INSTALL class; exact allowed type/operation/definition/role/predecessor/policy/context; authoritative head/state/bundle match; current tick within validity; no revocation/source invalidation; remaining use; and no effect outside the installation frame. Constructing authority metadata or hashing a GraphEntity cannot pass this predicate.

For P04 the issuing role is **QUALIFICATION_AUTHORITY**, exercised through an authenticated explicit human decision. An architect may specify semantics, but does not automatically issue installation authority. A system operator/configuration authority requires separately admitted role/delegation policy; no production issuer role is established here. P04 human authorization is required to issue the exact route REPLACE grant. This request to define I01 is not that selection.

**Trust/admission protocol:** capture the explicit decision through trusted user-role session transport. A dedicated authority-admission interface verifies issuer role, exact decision/grant/I01/definition/old-reference/head/policy/context and restrictions against trusted expected identities supplied outside the untrusted installation request. Emit a pinned immutable admission receipt. No cryptographic human signature is fabricated. Untrusted self-asserted receipt or grant bytes cannot bootstrap authority. The installer may atomically persist the **already-issued** grant and accepted receipt as referenced sources; INSTALL does not issue the grant.

Cold restore uses the externally trusted expected bundle identity, accepted historical receipt and pinned trust-policy binding. Replay verifies the historical admission/applicability at its original pre-state without requesting a new decision, refreshing validity or issuing another grant. Later revocation withdraws current use but does not erase past acceptance.

## Event and exact post-state

Proposed command/event: **INSTALL_DEFINITION**. Require event/schema version, request key, expected bundle ID, pre-state ID, ordinary parent event, next sequence, exact policy pin/version, operation, predecessor reference, definition ID/content ID/descriptor, authorized physical source additions, INSTALL authority ID/issued record/admission receipt, scope/lineage/generation and event provenance.

It requires a real ordinary parent equal to the committed append head, exact current Snapshot/bundle and next sequence. Parentless installation is rejected; this is not GENESIS. The payload is a definition, never a proof instance, ValidationResult, Evidence, ActionResult or completion/satisfaction status.

The future transaction atomically changes only:

1. Definition registry/active logical-role binding and installed-record witness.
2. The registered adapter's definition fields; for the route, the exact matching gate.resolution_contracts record/provenance.
3. Explicitly authorized immutable source-index additions and dedicated authority-use/audit records.
4. One ordinary ledger event/new canonical append head.

It preserves operational gate stage/history/pending/observations, knowledge, actual proof instances, Action statuses and root/slot satisfaction. New root/slot definition adapters may create only unresolved obligations, never satisfied values. No authority is issued; no receipt, validation result, proof, Action output or GENESIS is generated. Installation of a proof contract is not proof admission; installation of a result contract is not Action execution.

Derived readiness/control caches are invalidated only for bounded affected references. Pure recomputation may observe changed configuration; installing it cannot persist shortcut statuses/satisfaction. No policy upgrade or scope/lineage/generation switch occurs in I01.

New immutable source paths/pins are distinct from old versions; never overwrite an old path/content pin. Preserve old files and each historical prefix's source set. A configuration source addition is not an EvidenceSourceAdmission payload insertion.

## Currentness, replacement and history

Currentness is derived, not manually stored as TRUE:

`installed ∧ active role binding ∧ valid historical event witness ∧ current INSTALL authority ∧ exact current canonical body/source ∧ exact scope/lineage/generation ∧ applicable type/consumer predicate`.

For the route this additionally consumes native `gates.governed_external_unknown`, exact consumer/source references and physical source/policy bindings. Offline definition validity alone is insufficient. No transfer across scope, lineage or generation is permitted. I01 does not perform a generation change.

| Operation | Normative behavior |
| --- | --- |
| INSTALL | Role absent. Admit new version; occupied different role version fails CONFLICT. Exact already-active semantics may be an authenticated no-op. |
| REPLACE | Role exists. Require explicit REPLACE grant and exact compare-and-swap predecessor. Admit new immutable version and change active binding only at this event. |
| SUPERSEDE | Retirement relation resulting from REPLACE. No separate scheduled/cross-generation operation in I01. |
| CONFLICT | Wrong predecessor/content/identity/type/head/permission; reject atomically, never overwrite. |

**P04 uses REPLACE**, because the route role already exists in the trusted baseline Snapshot. Its metadata-wrapper source binding is the exact predecessor; no fictitious prior INSTALL event/identity is introduced. Old definitions/pins remain visible in historical states. Before the new event, replay sees the old route only; at/after it, the new binding is visible. An invalidated replacement never automatically reactivates its predecessor.

## Candidate staleness, atomicity and retries

Installing any canonical definition invalidates commands bound to the old head/state/bundle. An old A09 candidate **must fail** after INSTALL, even if its Evidence payload is unchanged. Rematerialize expected bundle/State/parent, command key, route dependency provenance and source-prefix/field bindings. The new parent is the actual INSTALL event/append head. Reuse of a semantic/native Evidence ID is allowed only if its exact identity inputs still match; it never permits reuse of an obsolete command parent.

Under the local single-writer lock, validate authoritative prefix/head, authority, bytes/domains/type/references/currentness/old version and sources before publication. Stage complete canonical descriptor/body/grant receipt/installed registry/post-state/event; fsync immutable artifacts; atomically publish one HEAD pointing at the complete bundle; fsync its directory. No distributed commit semantics are claimed.

No reachable durable state may have event without definition, current definition without event, changed pin without matching definition, or consumed grant without consistent installation. Rejection before HEAD leaves the original canonical state/use count intact. Unreferenced orphan staging files are not installed/current. Crash after committed HEAD restores exactly once; missing/corrupt referenced objects fail closed.

P04's grant is single-use. Use consumption, installed record, source admission and event publish together. Identical committed request_key/full-payload retry returns its original receipt and **present** current/active status without new event/use/source; it cannot resurrect a later invalidated/superseded definition. Same key with different payload fails. A new-key request for the exactly same active binding is a semantic no-op only after current-parent/authority checks; it consumes no grant. Claimed same identity with different bytes always fails digest checks—even REPLACE authority never authorizes an identity collision.

## Invalidation, persistence and replay

Authority revocation/expiry, source or definition invalidation, scope/lineage mismatch and generation supersession withdraw derived applicability/currentness. Installation history/obligations remain auditable; no receipt/result/proof is invented. Dependencies withdraw through bounded graph propagation and readiness-cache invalidation. Recovery requires an explicit authorized replacement/reactivation contract; no predecessor fallback or manual CURRENT flag.

Future native persistence must retain definition/body/content ID, installed witness, actual event/prior ledger, issued grant/accepted authentication receipt/use count, physical old/new source pins, context/consumer and policy/trust-policy bindings. Fresh readers authenticate trusted bundle identity and exact file bytes, replay predecessor/activation/source chronology, and derive currentness. They do not trust a saved label or discover trust from arbitrary metadata.

Replay installs configuration once at its historical sequence. Before E, new definition/source is unavailable; after E, installed/current according to that historical state; after later withdrawal it is historical/unusable. Replay never asks for new authority, re-admits proof or executes an Action. The implementation qualification suite must cover actual writer termination, fresh readers, seeds 0/1/7/101, three readers per checkpoint/seed, unordered native permutations, full typed semantic/identity/pin/authority-use equality and ordered ledger preservation.

## Fail-closed qualification suite

The machine companion defines 31 negative cases, all **specified, not executed**. They include metadata wrapper substitution, wrong bytes/definition/content/domain, wrong authority/issuer/self-authentication/type, scope/lineage/generation/expiry, foreign or absent parent, old A09 parent after installation, proof instance/result substitution, unsupported overwrite/wrong predecessor, policy upgrade, old source-path mutation, half-committed event/source/grant, conflicting retries/identities, historical visibility, replay side effects, invalidation/fallback, concurrent head change and crashes around commit.

Every rejection must preserve durable head/state/source/use count; crash/replay controls require exact atomic recovery and historical visibility. Positive qualification must additionally prove install/replace/no-op/history/currentness/withdrawal, scope narrowing, physical pins and pure installation frame. Defining this suite is implementation readiness, not a claim that its runtime tests passed.

## P04 mapping and unselected decision

P04_ROUTE_DEFINITION_ID = `planner-installable-definition-v1:1de38b5278463e9c55b656af1c765fe8952cdadc7bf53d4322eb32f7deb5a970`  
P04_ROUTE_CONTENT_ID = `raw-file-sha256:bb528a253ed466ff2fce89cadfdd6a1b0cdab41458651230d733f7455aba2567`  
P04_ROUTE_TYPE = EXTERNAL_RESOLUTION_CONTRACT  
P04_ROUTE_SCOPE = E2-QUALIFICATION-ONLY  
P04_ROUTE_LINEAGE = E2-P03-PROSPECTIVE-QUALIFICATION-1  
P04_ROUTE_GENERATION = E2-P03-PROSPECTIVE-GENERATION-1  
P04_ROUTE_CONSUMER = E2-REENTER  
P04_INSTALL_AUTHORITY_REQUIRED = YES

Canonical bytes are the already prepared [route body](qualification/E2_P04_CONTINUATION_INPUT_CLOSURE_1/resolution-contract.json); its complete closed descriptor, baseline reference/identity and exact predecessor/head/policy binding are in the [machine companion](DETERMINISTIC_PLANNER_V0_1_INSTALLATION_I01_CONTRACT.json). Expected pre-bundle `d1944fe1…`, Snapshot `576fe3a9…`, parent `9f00d563…` remain those of the unmodified P03 prospective checkpoint. No post-state, installed-definition or event identity is fabricated before an installation exists.

The human decision has exactly two options:

- **AUTHORIZE_P04_ROUTE_INSTALLATION:** authenticate and issue the bounded INSTALL grant for this exact definition/content/type/subject and REPLACE predecessor/context/pre-head/policy; valid ticks 0–100, one use, no delegation. Installation is gated on implementation qualification and grant applicability. This grants no A09–A13 execution, other definition installation, P03 edits, history reconstruction, GENESIS, N-REAL/release change or production effect.
- **DECLINE_P04_ROUTE_INSTALLATION:** issue no grant; preserve route/source/head/checkpoint; ROUTE_NOT_CURRENT and P04 execution readiness NO remain; prepared evidence remains available.

P04_ROUTE_INSTALLATION_DECISION_REQUIRED = YES  
P04_ROUTE_INSTALLATION_DECISION_READY = YES  
SELECTED_OPTION = NONE  
AUTHORITY_ISSUED = NO

No decision is selected by I01. The later authenticated capture must bind exact I01/definition/content/old-reference/head/policy/context identities, issuer/role/receipt, provenance/sequence/date, restrictions and option. Implementation-ready does not authorize implementation/installation or bypass that decision gate.

## Future types and preservation

The generic protocol may support ATTEST, Action accepted-result, validation, typed-proof and root/slot definitions through separately specified/qualified closed adapters. Each still requires its own INSTALL grant and domain authority/applicability. ATTEST definition installation does not perform an attestation; proof contract installation does not create proof; future-support declarations cannot seed accepted knowledge; root/slot definitions create unresolved obligations only. These adapters and grants are **not enabled or authorized by the P04 route option**.

INSTALLATION_IMPLEMENTATION_READY = YES: model, identity/acyclic hashing, bounded authority/trust protocol, ordinary-parent event, post-state frame, currentness, replacement, staleness, atomicity/idempotence, invalidation, persistence/replay and negative suite are defined. This verdict covers the generic protocol and first route adapter; future adapters need their own semantic/qualification work. No current runtime capability is claimed.

ROUTE_INSTALLED = NO  
P04_EXECUTION_READY = NO  
A09_EXECUTED = NO  
A09_A13_EXECUTED = NO  
P04_LIFECYCLE_ADVANCEMENT = NO  
E2_FINISH_EXECUTED = NO  
P03_RESULT = PASS  
P03_HISTORICAL_CORRESPONDENCE = UNPROVEN  
N_REAL_SATISFIED = NO  
RUNTIME_MODIFIED = NO  
E1_ARTIFACTS_MODIFIED = 0  
PRODUCTION_EFFECT = NO  
git diff --check = PASS

Only this contract Markdown/JSON pair is created. All prior artifacts, prepared objects, runtime Python files and frozen-E1 files are preserved. No runtime tests, authority issuance, definition installation or lifecycle operation was performed.
