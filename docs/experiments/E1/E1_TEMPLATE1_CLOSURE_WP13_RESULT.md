# E1 Template-1 Contract Closure — WP-13 Result

## Result

```text
WORK_PACKAGE = WP-13
RESULT = BLOCKED
SLOTS_RESOLVED = []
SLOTS_REMAINING = 41
NEWLY_ELIGIBLE = []
NEWLY_ELIGIBLE_WORK_PACKAGES = []
NEXT_WORK_PACKAGE = NONE
NEXT_ELIGIBLE_WORK_PACKAGE = NONE
CLOSURE_PLAN_EXCEPTION = YES
TEMPLATE1_CONSTRUCTION_READY = NO
CANDIDATE3_RESUMPTION_READY = NO
PRODUCTION_EFFECT = NO
```

## Eligibility and scope

The latest cumulative state in Closure Plan 1, after WP-12, marks WP-13 eligible and next. Section 2 permits independent specification of its consumer field/type contract under adopted contract-definition authority. Eligibility to inspect/specify does not imply that complete schema and identity acceptance criteria have passed.

WP-13 requires a versioned exact schema, field types, a T1 identity body and canonicalization distinct from T2 and WorkAuthorization identities, and strict source/mapping validation with complete field coverage. This execution inspected the current constructor, dataclass, lifecycle bridge and separate issuance-authority validator. No earlier blocker or exception was investigated or repaired.

## CLOSURE_PLAN_EXCEPTION — WP13-EX01

Classification: **consumer-contract/identity-verification gap at the T1-to-issuance-authority boundary**.

Exact root condition: the current constructor does not authenticate a T1 identity covering `fields_values`, while the separate issuance-authority validator trusts the supplied template identity for its template binding comparison.

The source-level trace is:

1. `invocation_constructor.construct_work_authorization()` checks T1 schema/state/ownership literals and `binding_digest == digest(authenticated_inputs)`. It checks the exact 23-key `fields_values` set, decodes the argv representation, applies four overrides and constructs the typed object. It does not read or verify `WorkAuthorizationTemplateId`, recompute a T1 identity body, or enforce an exact top-level T1 key set.
2. `artifact()` derives `WorkAuthorizationId` from the authenticated inputs plus the WorkAuthorization schema. `fields_values` is not in that body. The template `binding_digest` also hashes only authenticated inputs. Neither of these hashes authenticates the template field-value map.
3. `workauth_issuance.validate()` verifies the issuance record's own digest, then compares its `body['template_id']` directly with `template['WorkAuthorizationTemplateId']`. It does not recompute the supplied template's identity from its fields before that comparison. Authenticating an issuance record that names an identity is distinct from authenticating the supplied content carrying that identity.
4. The inspected `workauth_lifecycle.consume_and_issue()` verifies/reconstructs the WorkAuthorization artifact and checks the typed initial state before delegation. In this visible function there is no additional T1 identity recomputation. Its downstream effect boundary was not followed or invoked.

Consequently a claimed template ID and the two existing input/artifact hashes do not establish the content identity of `fields_values` at the inspected checks. This is a bounded source-level identity-binding finding, not an executed substitution, proof of an end-to-end issuance bypass, or a claim about uninspected downstream checks. No modified template, candidate, authority, or test fixture was constructed to demonstrate it.

The original plan already requires a T1 identity contract. The newly exposed concrete issue is the consumer linkage: the issuance-authority comparison consumes the supplied T1 identity without authenticating the template body, and the existing constructor hashes do not fill that gap. It is recorded as WP13-EX01 rather than silently accepting that comparison as identity validation.

Inspection stopped at this finding. No alternate consumer search, downstream issuance investigation, identity-rule invention, implementation change, authority issuance, or prior-blocker resolution was performed. No complete versioned schema or identity contract is accepted; the shared schema/identity readiness gate remains unsatisfied. This is BLOCKED pending disposition of the consumer-contract gap, not an authority grant or an implementation authorization.

## Bounded field-contract observations

Static parsing confirms that the dataclass has 23 fields, exactly matching the closure inventory. The constructor's exact field-key test is therefore an established shape check. Python annotations alone do not implement complete runtime field-type, source, provenance or mapping validation; the inspected function has specific checks rather than a complete strict schema validator. The existing argv decoding is observed only, not re-evaluated or expanded.

These observations do not select any missing field semantics, resolve any of the 41 slots, or discharge a prior authority requirement. In particular, WP-12's ignored-key decision and all earlier representation/mapping findings remain untouched. WorkAuthorization identity, template identity and issuance-authority identity remain distinct domains; none is substituted for another.

## Exact provenance and validation limits

Raw-file SHA-256 at inspection:

| File | SHA-256 |
|---|---|
| `docs/experiments/E1/E1_TEMPLATE1_PRODUCTION_CONTRACT_CLOSURE_PLAN_1.md` (before append) | `f20ed7120bf57aa3e2e483e60552ff7d47e64804129d1f400e6608b2d702f477` |
| `adapter/invocation_constructor.py` | `5908b257fdc7325d94d7524fbacbe3a7ec26d18d98507d6232c9ba1d41e8f9f7` |
| `adapter/workauth_issuance.py` | `a29c3f4bcd1f76c3e214006b2db875dc715a8e0db5b4610ed53e96441e3de3ed` |
| `adapter/workauth_lifecycle.py` | `a63522a4c901b7a349c64b6ce0edd085471186ebf80a99755880afbf18a5493a` |
| `adapter/governed_host.py` | `cb1d56d5787f69848ac67a8eee11755bd524cfbce17f5c0d797245357c0cdc16` |

Validation used read-only code inspection and standard-library AST parsing only: the constructor function contains no `WorkAuthorizationTemplateId` reference, and the 23 dataclass field names equal the inventory. This is local checkout evidence, not frozen-runtime release qualification. No adapter import, constructor invocation, issuance validator invocation, lifecycle operation, host operation, audit write, ownership operation, provider/model request, or production effect occurred.

## Accumulated state after WP-13

| Package | Status |
|---|---|
| WP-01 | BLOCKED |
| WP-02 | BLOCKED |
| WP-03 | AUTHORITY_REQUIRED |
| WP-04 | AUTHORITY_REQUIRED |
| WP-05 | BLOCKED |
| WP-06 | AUTHORITY_REQUIRED |
| WP-07 | BLOCKED |
| WP-08 | PASS |
| WP-09 | BLOCKED |
| WP-10 | BLOCKED |
| WP-11 | BLOCKED |
| WP-12 | AUTHORITY_REQUIRED |
| WP-13 | BLOCKED |
| WP-14 | AUTHORITY_REQUIRED |
| WP-15 | BLOCKED |

Accumulated blockers: WP-01 canonical invocation/dispatch binding; WP-02 eligibility prerequisites; WP-05 supervisor/succession source path; WP-07 attempt-chain inputs; WP-09 context hydration and OperationalBinding governance-shape gaps; WP-10 independent `exec_bins` mapping and unfinished repository/execution qualification; WP-11 transmission-to-initial-clearance mapping; WP-13 T1 content-identity verification at the inspected consumer boundary (WP13-EX01), leaving complete schema/identity acceptance unsatisfied; WP-15 incomplete sources/mappings/schema/validator/construction/release prerequisites. Earlier conditions are carried forward without re-evaluation.

Accumulated authority requirements remain unchanged: WP-03 current runtime-head, WP-04 applicable supervisor, WP-06 audit namespace/store; WP-12 ignored-input `state`/`revision` contract decision; WP-14 validator implementation; separate binding-input construction, Template-1 construction and exact-artifact Template-1 release authorities. WP-13 neither issues authority nor infers that existing contract-definition authority permits implementation or production effects.

Accumulated exceptions: the two open WP-09 context/OperationalBinding gaps; WP10-EX01 retained as locally repaired/regression-qualified, not production-published; open WP11-EX01; and new open WP13-EX01. The WP-10 independent executable mapping and WP-12 authority requirement retain their recorded classifications.

Mechanical inventory: `20 originally unresolved authenticated inputs - 2 previously established slots + 23 field values - 0 WP-13 resolutions = 41`. The established slots are `InvocationAttemptId` and `profile_sha256`; initial-state/ownership constants were already excluded. Eighteen authenticated inputs and all 23 field values remain unresolved. The shared schema/identity/validator/authority gates are additional and are not counted as value slots.

Mechanical eligibility: before WP-13 the eligible unexecuted set was `{WP-13}`; after recording it BLOCKED the set is empty. Thus `NEWLY_ELIGIBLE_WORK_PACKAGES = []` and `NEXT_ELIGIBLE_WORK_PACKAGE = NONE`. WP-14 is not next eligible: its implementation authority remains required. WP-15 remains blocked on its source/mapping/schema/validator and construction/release gates. There is no authorized eligible next package under the recorded state; no package was executed after WP-13.

Section 6 remains false because complete-input and complete-field requirements fail with 41 unresolved slots, and schema/identity, qualified-validator, canonical-binding and current-source gates are incomplete. Therefore `TEMPLATE1_CONSTRUCTION_READY = NO`. Section 7 requires that readiness, so `CANDIDATE3_RESUMPTION_READY = NO`. No Template-1 or Candidate 3 was constructed and no Candidate-3 construction authority was consumed. `PRODUCTION_EFFECT = NO`.
