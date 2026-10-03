# Budget proof-matrix acceptance oracle 1

**Contract only.** This defines a finite implementation-independent qualification oracle and an explicit synthetic positive instance. It does not execute planner code, authenticate actual E1 evidence, adopt an E1 applicability rule, or qualify C06A. The [JSON companion](DETERMINISTIC_PLANNER_V0_1_BUDGET_PROOF_MATRIX_ORACLE_1.json) is normative input data, not planner output or an execution ledger.

## Authority and limits

The primary source is the frozen [external evidence request](../experiments/E1/E1_BUDGET_APPLICABILITY_EXTERNAL_EVIDENCE_REQUEST_1.md): “Exact subject,” common contract, eight named propositions, minimum evidence set, receipt and deterministic reentry. Its raw hash is pinned in the companion. The frozen [resolution plan](../experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_PLAN_1.json), FACT-BUDGET-APPLICABILITY acceptance criteria, requires complete proof before PASS; partial acquisition does not suffice. [Backlog](../backlog/DETERMINISTIC_REASONING_PLANNING_RUNTIME.md) knowledge, fact acquisition, authority-reference applicability and proof-obligation requirements prohibit treating references or missing rules as evidence. [Traceability](../backlog/DETERMINISTIC_REASONING_PLANNING_RUNTIME_E1_TRACEABILITY.md) preserves observed evidence versus architectural inference.

The [reconciliation](DETERMINISTIC_PLANNER_V0_1_C06_C07_RECONCILIATION_1.md) and [blocked C06A result](DETERMINISTIC_PLANNER_V0_1_C06A_RESULT.md) require an independent positive contract. This artifact supplies one as a **qualification profile**, not a claim that the unknown real producer, source format, trust chain or governing rule has been discovered. The original [correction plan](DETERMINISTIC_PLANNER_V0_1_CORRECTION_PLAN_1.md) and [matrix](DETERMINISTIC_PLANNER_V0_1_CORRECTION_MATRIX_1.md) remain unchanged.

Observed E1 requirement: current subject facts AND independently governing rules AND authenticated competence/currentness. New qualification specification: exact pinned record admission and exact checkpoint equality are one sufficient finite realization of that requirement. They are not inferred universal E1 freshness/publication rules. Other formats/rules require separately admitted mappings; unsupported inputs return false with an explicit reason. No arbitrary TTL, live wall clock, online signatures, network, prose evaluator or LLM is needed.

## Recovered obligations

For **every row**, identity means full typed identity equality, distinct from the raw content identity of its evidence; scope binds authority, invocation, dispatch, context, release, operation and source/target phases; lineage requires a current authenticated selection; currentness requires coherent governing rule/evidence and a trusted evaluation anchor. These are mandatory common columns, not optional omissions. The exact real subject values remain in the frozen request; synthetic values must never replace them in E1.

| ID suffix (prefix `BUDGET-PROOF-`) | Proposition / current subject fact | Governing rule and evidence requirement | Competent source / identity-specific requirement | Accept / reject |
|---|---|---|---|---|
| AVAILABILITY_PUBLICATION | Authority available in owning domain; membership/publication status | Publication requirement or explicit exemption; authenticated catalog/resolution/publication record | Publisher/store owner; exact budget identity, store, returned authority body identity and record hash | Available and required publication proved, or adopted exemption; reject local-file existence, stale catalog or missing membership |
| SCOPE | Recorded EXECUTION source and REQUEST target scopes/operation | Adopted scope-binding rule and exact application | Scope/contract authority plus target source; exact scope pair/envelope | Exact permitted pair; reject prefix similarity, copied reference or DEC-BUDGET representation approval as applicability |
| LINEAGE | Source and target lineage and selected release | Current selection/adoption rule; authenticated direct selection or qualified chain | Release/lineage owner; selection/head identities | Both match applicable selected lineage and release, no supersession; reject missing selection, wrong lineage or stale chain |
| RUNTIME | Source/target runtime content and current selection | Authenticated owning content/selection binding and applicability rule | Runtime/content and selection owners; CONTENT_IDENTITY, not any equal SHA domain | Verified exact runtime and current selection; reject copied references or unverifiable/obsolete content linkage |
| CONTROLLER_STORE_G4 | Source/target store generation and authority membership | Current generation selection and authority resolution rule | Store/catalog owner; exact generation and authority IDs | Same selected G4 and membership; reject other generation, guessed location or untrusted catalog |
| PROGRAMMER_PROFILE | Owning profile identity and target binding | Required profile rule or explicit non-applicability rule | Profile owner and target-binding authority; ProgrammerProfile identity, not released-profile or authority substitute | Verified current target profile, or explicit exemption; reject omission without rule, wrong domain or supersession |
| TEMPORAL_CURRENTNESS | Revocation/supersession/single-use availability at evaluation | Owning validity/usage rule and independently trusted current anchor | Competent validity/usage owner (real concrete owner unknown); exact authority/invocation, event/snapshot and rule identities | Required validity facts pass current rule; reject unknown usage, old snapshot, consumed grant or FRESH default |
| EXECUTION_REQUEST_PHASE | Actual source/target phases and preconstruction operation | Existing adopted phase rule plus application and exclusions | Governing phase authority; exact rule and source/target identity | Reference-only preconstruction permitted with no effects; reject missing/unadopted rule or inferred EXECUTION⇒REQUEST |

A single competent record may prove several rows. Eight rows are required; eight physical evidence artifacts are not. The companion uses separate records for audit clarity, not as an E1 minimum-file requirement. Authenticity/identity of the owning StatusBudgetAuthority is a shared premise, not a ninth applicability obligation. It preserves owning policy; it neither copies policy into budget_policy nor changes the approved authority-reference representation.

## Typed input and trust boundary

Oracle signature: `evaluate(parameters, submission_or_absent) -> {accepted: bool, receipt_state, row_results, dependencies, reasons}`. No planner state or expected answer is an input.

The companion contains exact keys and a complete example. Types and parsing rules:

- JSON objects reject duplicate/unknown keys; arrays have unique IDs; no coercion of strings/numbers/bools; integers exclude booleans; all strings nonempty. No floats, null in required fields, placeholders, implicit defaults or unresolved references.
- Identity = `{kind, namespace, sha256}`. Kind is one of CONTENT_IDENTITY, AUTHORITY_IDENTITY, INSTANCE_IDENTITY, RELEASE_IDENTITY, CANONICAL_OBJECT_IDENTITY, WORKAUTHORIZATION_ID, BINDING_DIGEST; digest is exactly 64 lowercase hex. Namespace is part of identity. Authority, runtime, invocation and release use their exact designated kinds. Other envelope identities retain their qualified namespaces, including ProgrammerProfile. Equal digest does not permit substitution.
- Envelope has exactly the companion's 12 keys. Compare the entire typed object, not a subset. Expected envelope is an independently admitted parameter, never read from a submission as its own oracle.
- Parameters = mode, expected_envelope, anchor, trusted_record_grants, parameters_sha256. Anchor = id, nonnegative integer generation, envelope. Grant = exact record_id, producer typed identity, role, envelope, anchor. Role is BUDGET_OWNER, GOVERNING_RULE_OWNER, or the row's named role. Grants are unique by record_id/role. Canonical hash of parameters excluding parameters_sha256 must match an **out-of-band pinned parameter identity** in the test contract. A self-consistent replacement parameter set is not automatically trusted.
- Submission = schema, mode, envelope, records, source_authentication_id, rows, invalidated_ids. Schema/mode must equal the literal companion values. Row = id, fact_id, rule_id; exactly one per eight obligation IDs, no extras. Records = unique `{id, body}`; id = SHA256 of canonical body bytes. Canonical encoding is ASCII JSON with lexically sorted object keys, compact separators, integers in decimal, no NaN; no trailing newline. Original source bytes/pointers are retained alongside normalized records on import. Qualification records use this declared format; real source identity algorithms are not replaced by it.
- Common record body = synthetic=true, record_type, producer, envelope, anchor, generation. RULE additionally contains obligation, rule_profile=`EXACT_CHECKPOINT_1`, policy. FACT additionally contains obligation, facts. SOURCE_AUTHENTICATION additionally contains source_type=`StatusBudgetAuthority`, authority_identity, identity_verified and owning_policy_preserved. The two booleans must be true and backed by exact independent BUDGET_OWNER admission, not accepted on their own.
- Fact/policy schemas are exactly those in the positive companion, with one bounded exception: publication policy enum REQUIRED/NOT_REQUIRED; profile_check enum REQUIRED/NOT_APPLICABLE. Required identities remain typed in both alternatives. A profile exemption still needs the authenticated rule; it does not turn absent rule into exemption.
- Invalidated IDs are a persisted set of record content IDs, parameter identity, anchor ID, or envelope typed identities. Any required member being invalidated makes acceptance false. Unknown invalidation entries do not grant anything or invalidate unrelated sources. They must still be well-typed strings or identity objects.

Synthetic trust is an explicit premise: the qualification author pins the parameter artifact, which independently admits precise fact and rule records for the indicated roles, envelope and checkpoint. No submission may add grants. A governing rule is adopted **in this test world only** through that independent admission. This is the defined qualification trust boundary, not a signature/authentication implementation or an E1 grant. Real-mode submissions are unsupported by this synthetic profile and fail closed until separately admitted actual source rules and trust exist.

## Deterministic positive oracle

The following is normative pseudocode; implementers may translate it without consulting planner output. Each named check has a finite definition above or below; none calls the planner, its receipt helper or its oracle fields.

```text
REQUIRED := the eight exact row IDs in this document
if submission absent: return false, EVIDENCE_NOT_YET_AVAILABLE
strictly parse and type-check parameters and submission; any failure returns false
verify parameters against independent pinned identity
verify parameter anchor.envelope == expected_envelope
require submission.envelope == expected_envelope
require exact supported schema/mode and complete unique REQUIRED rows
index unique records by content ID; verify canonical body digest for every record
reject unrelated extra records not referenced by a row or source_authentication_id
for every required source/rule/authentication record:
    require exact role/producer/envelope/anchor grant in independent parameters
    require body.envelope == expected_envelope
    require body.anchor == parameters.anchor.id
    require body.generation == parameters.anchor.generation
    require no required identity, record, anchor or parameter is invalidated
verify source_authentication record type/fields, exact authority_identity,
    identity_verified == true and owning_policy_preserved == true
for each row in sorted REQUIRED:
    require referenced FACT and RULE have matching row ID and proper record_type
    require RULE rule_profile == EXACT_CHECKPOINT_1
    evaluate the row expression below using strictly typed facts, policy and envelope
accepted := every common check and all eight row expressions true
return accepted with sorted row results and dependency identities
```

Row expressions (F=facts, P=authenticated policy, E=expected envelope; `==` always type-sensitive):

1. **Availability:** F.available AND F.authority_body==E.authority AND F.store==E.controller_store AND ((P.publication==REQUIRED AND F.published) OR P.publication==NOT_REQUIRED). Even exemption does not waive availability/owning-domain proof.
2. **Scope:** F.source_scope==P.source_scope==E.source_scope; F.target_scope==P.target_scope==E.target_scope; F.operation==P.operation==E.operation; P.permitted==true.
3. **Lineage:** F.source_lineage==F.target_lineage==P.selected_lineage==E.lineage; F.selected_release==P.selected_release==E.release; F.superseded==false.
4. **Runtime:** F.source_runtime==F.target_runtime==P.selected_runtime==E.runtime; F.content_verified==true; F.selection_current==true. The admitted competent owning attestation is the qualified content proof; an unauthenticated boolean is insufficient.
5. **Store:** F.source_store==F.target_store==P.selected_store==E.controller_store; F.authority==E.authority; F.membership==true.
6. **Profile:** P.profile==E.profile AND (P.profile_check==NOT_APPLICABLE OR (P.profile_check==REQUIRED AND F.profile==E.profile AND F.identity_verified AND F.target_binding AND NOT F.superseded)). An individually supplied fact with a contradictory profile identity cannot coexist with the envelope even under exemption: enforce F.profile==E.profile as a cross-field check always.
7. **Temporal:** F.authority==E.authority; F.invocation==E.invocation; P.require_unrevoked==true, P.require_unsuperseded==true, P.require_single_use_available==true; NOT F.revoked; NOT F.superseded; F.single_use_available==true. This supported profile represents the explicit unconsumed single-use case; unknown or different governing policies are unsupported, never guessed.
8. **Phase:** F.source_phase==P.source_phase==FIRST_PROGRAMMER_EXECUTION; F.target_phase==P.target_phase==FIRST_PROGRAMMER_REQUEST; F.operation==P.operation==E.operation==BUDGET_REFERENCE_PRECONSTRUCTION; P.permitted; P.effects_allowed==[]. Scope suffixes must correspond exactly to their phase names. Scope permission does not substitute for this independent rule.

No greater-than timestamp heuristic exists. Exact checkpoint matching is an explicit synthetic governing freshness profile with an independently pinned anchor. Other valid real freshness models are not declared invalid E1 policy; they are unimplemented profile inputs and produce false/UNSUPPORTED_RULE rather than accidental permission. No data beyond the frozen common requirements is demanded of real E1 by this profile.

## Negative oracle and cross-field consistency

For each mutation start from the companion, change only the named semantic field, recompute that record's hash and update row references. For authenticated-negative cases, the test author separately admits the changed record at a different pinned synthetic parameter identity; this is not something a submitted record may do. Thus failures can exercise semantic comparisons rather than merely a broken checksum. Also run checksum-only mutations without repinning to test authentication. Expected accepted=false in every row below.

| Mutation | Expected reason / affected row |
|---|---|
| Remove each fact or rule reference in turn | MISSING_EVIDENCE / that row; not DISPROVED |
| Change any record generation from 7 to 6 | STALE_OR_INCOHERENT_CHECKPOINT / dependent rows |
| Change scope to another target while rule unchanged | SCOPE_MISMATCH |
| Change source or target lineage only | LINEAGE_MISMATCH |
| Change runtime identity only | RUNTIME_MISMATCH |
| Change source/target store generation only | STORE_MISMATCH |
| Substitute ReleasedProfileAuthority or content identity for ProgrammerProfile | IDENTITY_DOMAIN_OR_PROFILE_MISMATCH |
| Remove phase rule, deny permission, or add EXECUTE to effects_allowed | RULE_MISSING or PHASE_NOT_PERMITTED |
| Replace authority with another domain sharing digest, or change body bytes without matching pin | IDENTITY_SUBSTITUTION / CONTENT_IDENTITY_MISMATCH |
| Unknown rule profile, publication enum, or missing policy key | UNSUPPORTED_RULE / INVALID_SCHEMA |
| available=false or required published=false | AVAILABILITY_PUBLICATION_NOT_PROVED |
| revoked=true, superseded=true or single_use_available=false | TEMPORAL_INCOMPATIBILITY |
| Remove source authentication or set owning_policy_preserved=false | SOURCE_AUTHENTICATION_UNPROVED |
| Change one row's full envelope to another individually valid subject | ENVELOPE_MISMATCH |
| Keep valid records but remove competent producer grant | UNAUTHENTICATED_PRODUCER |
| Replace current anchor with another checkpoint without independent admission | ANCHOR_OR_PARAMETER_MISMATCH |
| Duplicate row/record/key; unresolved reference; boolean represented as string | INVALID_SCHEMA |

All records bind the **same** authority, runtime, controller-store generation, profile, lineage, release, invocation/dispatch/context, source/target scope and operation. Rule versions and fact generations must refer to the same admitted checkpoint in this profile. No union of independently valid but incompatible envelopes is accepted. Extra conflicting records are rejected rather than silently selecting the convenient one. Authentication of contradictory facts preserves evidence but never acceptance.

## Availability, invalidation and persistence

Return EVIDENCE_NOT_YET_AVAILABLE for no submission. With a submission, per-row outcomes distinguish missing proof (EVIDENCE_NOT_FOUND), unsupported or missing governing permission (AUTHORITY_DECISION_REQUIRED/UNSUPPORTED_RULE), stale/untrusted input (REJECTED), and authenticated contrary fact (DISPROVED). A received partial matrix has accepted=false, receipt_state=ACCEPTED_PARTIAL if any valid positive observations remain, otherwise EVIDENCE_RECEIVED_BUT_INVALID. Complete valid matrix alone has receipt_state=EVIDENCE_ACCEPTED. Diagnostic precedence is schema/authentication before semantic interpretation; sort all reasons lexicographically by row then reason. Never interpret a missing row as negative proof.

Persist exact parameters/pin, records/raw provenance, normalized rows, envelope, anchor, rule profile version and invalidation set. Recompute acceptance after reload; a saved accepted=true is not proof. Required dependencies include every used fact, rule, source-authentication record, trust parameter, current anchor and envelope identity. Invalidation of any required dependency makes accepted=false, even if bytes remain. Canonical reserialization cannot remove invalidation. A newly admitted replacement and independent fresh anchor may support a new attempt only through the defined receipt/reentry route; clearing a stale flag is insufficient.

The separate refined C06 prerequisite remains required for FACT actionability: typed accepted REEVAL-BUDGET BLOCKED knowledge with its exact current source binding. Matrix acceptance does not recreate or supersede that knowledge, and the producer need not become COMPLETED. Invalidating that source can block actionability even while this matrix remains mathematically accepted; the two predicates must not be conflated.

## Positive qualification instance and C06A counterexample

The companion provides every required field: independent parameter/trust/anchor inputs; full synthetic envelope and typed identities; source-authentication record; eight facts; eight rules; eight references; empty invalidation set. Each fact supplies one row's observable premises. Each separately admitted rule supplies normative permission/selection/validity, not inferred compatibility. Artifact count is convenient, not asserted minimal. All identity namespaces and records are marked synthetic. Parameter pinning is performed by the qualification harness, not by reading a digest from untrusted submission as authority.

This contract is sufficient to build a test without copying planner output. The harness independently evaluates the equations, requires true, and supplies the same normalized record/pin set to the importer. The old receipt helper is not the positive oracle. The expected output is the independent canonical set of eight `(obligation, fact_id, rule_id, envelope, anchor, generation, PROVED)` tuples, their source-authentication/trust dependencies and exact provenance. The supplied FACT result is PASS with knowledge type BUDGET_APPLICABILITY_PROOF_MATRIX_V1 and fields {source_authentication_id, parameter_identity, envelope, anchor, rows, invalidated_ids}; rows are exactly the eight tuples above sorted by obligation. Its knowledge identity is CONTENT_IDENTITY of the canonical encoding of these fields, with the type tag included. It is KNOWN_COMPLETE only for this bounded matrix at this anchor, retaining its independent prerequisite. Root and slot transitions remain UNCHANGED. Missing or substituted member must reject the result; reordered set members must preserve identity.

**GIVEN** this explicitly synthetic, independently accepted full matrix and independently valid original action prerequisites, including current accepted BLOCKED knowledge;

**WHEN** the source contracts and matrix are imported through the current full-import boundary, persisted, restored in a cold process, and a bounded FACT result is supplied;

**THEN** every operational tuple/dependency is restored, the complete bounded result is accepted, and only its defined reevaluation route may become eligible;

**AND MUST NOT** execute selected work, resolve budget merely from PASS, silently synthesize missing proofs, equate producer BLOCKED with missing knowledge, or use expected actionability as input.

Expected pre-repair failure is loss/unavailability of the supported proof-matrix output contract: current imported empty accepted inventory rejects the independently valid result. If input schema instead rejects the independently specified source-contract profile before restoration, record that exact missing-contract boundary; do not patch post-load state to manufacture a red test. The future C06A regression must exercise the existing real importer/result path and require preservation plus valid result acceptance; it must fail before repair and pass after. The negative mutations above and refined C06 test remain required. **No counterexample was executed here.**

C06A may now retry the budget-oracle prerequisite and develop its red test against this complete finite contract. The distinct decision-route restoration, full inventory, other C06A positive tests and source-preservation gates remain mandatory; this artifact does not establish C06A PASS. If another required source contract is insufficient, that gap must still be reported. C07 remains blocked until its complete independent gate is met.

## Real E1 boundary and report

The actual E1 expected envelope is the frozen one, not the TEST envelope. It has no received applicability bundle or adopted synthetic trust. Evaluating the frozen no-submission state returns false/EVIDENCE_NOT_YET_AVAILABLE; the budget branch remains WAITING_FOR_EXTERNAL_EVIDENCE. No external request, authority issuance, source creation, receipt, FACT revalidation, REEVAL or MAP operation is performed by defining this contract.

```text
BUDGET_PROOF_OBLIGATIONS = [AVAILABILITY_PUBLICATION, SCOPE, LINEAGE, RUNTIME, CONTROLLER_STORE_G4, PROGRAMMER_PROFILE, TEMPORAL_CURRENTNESS, EXECUTION_REQUEST_PHASE]
POSITIVE_ORACLE = COMPLETE (finite synthetic qualification profile)
NEGATIVE_ORACLE = COMPLETE (same profile; unknown rules fail closed)
CROSS_FIELD_CONSISTENCY = [authority, invocation, dispatch, context, release, lineage, runtime, controller_store, profile, scopes, phases, operation, checkpoint]
SOURCE_INVALIDATION_RULE = any required dependency invalidated => accepted=false after reload
QUALIFICATION_FIXTURE_DEFINED = YES
REAL_E1_EVIDENCE_CREATED = NO
C06A_COUNTEREXAMPLE_DEFINED = YES (not executed)
C06A_RETRY_ALLOWED = YES
C06A_RETRY_PREREQUISITES = [independently pin oracle parameters, verify positive equations, reproduce red regression through real import path, preserve other C06A contract gates]
F03_STATUS = CLOSED
C07_RETRY_ALLOWED = NO
V0_1_CURRENT_STATUS = CORRECTION_REQUIRED
IMPLEMENTATION_MODIFIED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
```

Only these new contract artifacts were created. Existing tests, implementation, historical plans/results and all 10,911 frozen E1 files are preserved. JSON structure/content hashes, fixture references, Markdown links, whitespace and `git diff --check` were checked. No planner qualification tests or action executions occurred.
