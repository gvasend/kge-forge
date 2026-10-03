# CE-01 contract refinement reconciliation 1

**CE-01 classification: A — O02/O06/O10 local predicates are under-constrained.** Required supporting-source payload admission was omitted. O16's stronger composition checks are valid and remain unchanged. This additive refinement corrects only the local omissions; it does not require all component predicates to enforce every composition constraint.

## Authority, artifacts and reproduction

Governing requirements are the [remaining-contract O02/O06/O10/O16 rows](DETERMINISTIC_PLANNER_V0_1_C06A_REMAINING_CONTRACT_1.md) and the [closure specification](DETERMINISTIC_PLANNER_V0_1_C06A_3_PREFLIGHT_CLOSURE_1.md), particularly “Shared input and trust contract,” PF-02, PF-03, PF-04 and persistence sections. These require accepted source-bound current proof, independently admitted hold overrides, source pins before operational projection, and stricter composed-instance correspondence. The source/proof distinction also preserves the accepted refined C06 contract.

The [RETRY_3 report](DETERMINISTIC_PLANNER_V0_1_C06A_3_RETRY_3_RESULT.md) and its baseline evidence remain unchanged. New artifacts:

- [Predicate refinement and dependency metadata](DETERMINISTIC_PLANNER_V0_1_CE01_CONTRACT_RECONCILIATION_1.json).
- [Executable fixture generator and independent expected formulas](DETERMINISTIC_PLANNER_V0_1_CE01_CONTRACT_RECONCILIATION_1_FIXTURES.json).
- [Validation, all 12 before/after records and complete combinatorial results](DETERMINISTIC_PLANNER_V0_1_CE01_CONTRACT_RECONCILIATION_1_VALIDATION.json).
- [Complete eight-element preflight](DETERMINISTIC_PLANNER_V0_1_CE01_CONTRACT_RECONCILIATION_1_PREFLIGHT.json).

The predicate companion pins the historical inputs and carries a new reference-program digest. It reuses the exact old profiles, source identities, fixture bases, O08/O09 predicates and submissions. No historical artifact is overwritten. The fixture program takes `REFINED_PROGRAM` from the new companion and runs from the repository root. Its `OUTPUT` records deterministic results. No planner implementation is imported or executed.

All 12 CE-01 variants reproduce against the old program and reject at the affected local entry point under this refinement. They are the following six rows repeated independently for BASE and RENAMED. Every individual record in validation includes all four results, not just the originally affected predicate.

| Source mutation | Old O02 | Old O06 | Old O10 | Old O16 | Refined affected local clause |
|---|---|---|---|---|---|
| evidence substituted, HISTORY probe | ACCEPT | ACCEPT | ACCEPT | REJECT SOURCE_PIN | SOURCE_PIN |
| evidence absent, HISTORY probe | ACCEPT | ACCEPT | ACCEPT | REJECT INSTANCE_MEMBERS | SOURCE_MISSING |
| override substituted | ACCEPT | ACCEPT | ACCEPT | REJECT SOURCE_PIN | SOURCE_PIN for O02/O06 |
| override absent | ACCEPT | ACCEPT | ACCEPT | REJECT INSTANCE_MEMBERS | SOURCE_MISSING for O02/O06 |
| evidence substituted, GRAPH probe | ACCEPT | ACCEPT | ACCEPT | REJECT SOURCE_PIN | SOURCE_PIN |
| evidence absent, GRAPH probe | ACCEPT | ACCEPT | ACCEPT | REJECT INSTANCE_MEMBERS | SOURCE_MISSING |

The HISTORY and GRAPH evidence probes deliberately share a mutation but test different output claims. Old history retained current knowledge/eligibility or released H1; old graph retained EDGE1 as an operative prerequisite. The trusted profiles and validity views were not changed. Substitution changes evidence's knowledge type or override's action to an unrelated value. Canonical source digests then differ from their expected pins. O10 continues to accept override-only mutations, because override is not its local supporting source; O16 rejects them.

## Admission layers and intended predicate ownership

| Layer | Meaning | Governing entry points |
|---|---|---|
| LOCAL_OBJECT_VALIDITY | Schema, types, internal references and structural consistency; insufficient for proof use | Checks inside each predicate; not an independent operational permission |
| LOCAL_OBJECT_ADMISSION | Object plus mandatory supporting bytes/identities/provenance and role-specific validity; historical admission can preserve stale facts explicitly | O02/O06 HISTORY; O10 GRAPH; existing O01/O08/O09 |
| COMPOSITION_ADMISSION | Required admitted components, complete coverage, common envelope, graph, ledger and policy correspondences | O16 `compose` |
| OPERATIONAL_USE_ADMISSION | Current supported proof and all applicable planner prerequisites for the named operation; not implied by historical completion or an admission boolean | Existing planner gates downstream of admitted state; not implemented here |

HISTORY returns historical states **and** current knowledge/eligibility qualifications. Admission of the former does not establish the latter. GRAPH here projects operative assertions, so stale required support rejects its operational projection. O16 acceptance establishes a coherent qualification instance, not permission to issue authority, execute an action, satisfy a root/slot, or resume E1.

## Supporting-source ownership

These classifications are relative to the indicated component; a source may be local to one and composition-only to another.

| Relationship | Owner | Classification and currentness rule | Governing basis |
|---|---|---|---|
| history → accepted result bytes | O02/O06 | REQUIRED_FOR_LOCAL_ADMISSION; exact result pin | PF-02 accepted source records; O06 historical overlays |
| accepted knowledge/result → evidence bytes | O02/O06 | REQUIRED_FOR_LOCAL_ADMISSION; stale authenticated bytes may support history, never current knowledge/use | PF-02 current source validity and historical/current distinction; remaining O02 |
| hold release → override bytes | O02/O06 | REQUIRED_FOR_LOCAL_ADMISSION; current source required for the admitted override | PF-02 “separately admitted H1 release” and “source” binding; remaining O06 |
| operative graph assertion → evidence bytes | O10 | REQUIRED_FOR_LOCAL_ADMISSION; current transitive support required | PF-03 “accepted provenance, source pins” and required assertion currentness; remaining O10 |
| graph payload → HISTORY component | O16 | REQUIRED_ONLY_FOR_COMPOSITION relative to HISTORY | PF-04 five-source complete instance; not a HISTORY dependency |
| override payload → GRAPH component | O16 | REQUIRED_ONLY_FOR_COMPOSITION relative to GRAPH | PF-04 complete instance; no override dependency for EDGE1 |
| complete coverage/all source roles/admission submissions | O16 | REQUIRED_ONLY_FOR_COMPOSITION relative to individual source predicates | PF-04 composed source accounting and O08/O09 joins |

The shared `source()` primitive verifies payload presence and canonical digest. Existing `current()` checks the accepted validity identity/state and transitive dependencies; it cannot authenticate bytes it never reads. No new external source, producer or freshness rule is introduced. No CE-01 evidence/override relationship is optional or unsupported.

The old local predicates were not declared “already source-authenticated” helpers. They were exposed as independent admission predicates, and their outputs claim current knowledge/operative edges. Consequently neither B (composition-only constraint) nor C (both already correct but staged admission omitted) describes the demonstrated local-source cases. Genuine composition-only cases remain valid and are tested separately.

## Rule reconciliation

| Predicate | Current executable rule | Governing rule | Reconciliation | Reconciled rule |
|---|---|---|---|---|
| O02 | Checks plan/results bytes; evidence/override identity and currentness only through validity view | Mandatory source-bound proof and accepted holds | YES | Before ACCEPT also authenticate evidence and override payloads with existing `source()` |
| O06 | Same HISTORY path; permits supported-history output without authenticating override/evidence bytes | Accepted historical records and explicit independently admitted override | YES | Same two local checks; preserve record order, hold logic and currentness calculations |
| O10 | Checks graph bytes; supporting evidence consulted only via validity | Source-pinned, accepted operative graph projection | YES | Before ACCEPT also authenticate evidence payload with existing `source()` |
| O16 | Checks every role before composing required predicates | Stricter coherent operational instance | NO executable change | Preserve all checks; invoke refined local predicates; record refinement relationship explicitly |

The new program makes exactly three additional `source()` calls. Existing schema, type, provenance, scope/lineage, source-dependency, history, graph-ordering, O08/O09, and rejection rules remain intact. The new reference is a specification artifact, not a runtime patch. Registry installation is not performed.

Missing payload rejects SOURCE_MISSING locally; substituted payload rejects SOURCE_PIN. An equal-looking authority-domain identity in place of a content-source identity is not accepted: the trusted content-pin/role contract remains unchanged and the validity identity comparison rejects it. The profile is trusted independently of candidate state; a candidate cannot repin itself.

Every source binds exact contents, including its provenance, scope, lineage, currentness context and operational envelope where represented. Changing any such member fails the fixed pin even when it looks structurally compatible. An independently governed new source/profile could define another instance, but none of the CE-01 substitutions establishes that admission. STALE/REVOKED are separately represented, not treated as byte substitutions.

## Refinement and executable meta-invariants

The required property is one-way:

```text
O16_ACCEPT => ACTION_ACCEPT AND HISTORY_ACCEPT AND GRAPH_ACCEPT
              AND O08_ACCEPT AND both_O09_ACCEPT
component_ACCEPT does not imply O16_ACCEPT
```

The five meta-invariants are encoded and exercised:

1. O16 ACCEPT cannot coexist with a required component rejection. `compose` evaluates fixed O08/O09 predicates, and the generated cases independently compare local ACTION/HISTORY/GRAPH outcomes.
2. Missing/substituted required composition sources prevent O16 acceptance.
3. HISTORY remains locally admitted with a missing graph source when its own sources are valid; GRAPH remains admitted with a missing override. Both composed instances reject. Incomplete composition coverage also rejects without forcing local failure.
4. Missing/substituted locally mandatory support rejects the corresponding local predicate.
5. Invalidation after canonical persistence/reload produces the same outcomes as an equivalent freshly constructed invalid state. Historical bytes remain preserved; current support is not resurrected.

These implications constrain future implementation without introducing a second operational-use/resume model. No historical producer is required to become COMPLETED merely to use independently accepted current knowledge.

## Bounded combinatorial qualification

The fixture generator uses two fixed bases and the complete product:

```text
2 bases
× 5 evidence states
× 5 override states
× 5 graph states
× 2 historical-summary consistency states
× 2 composition-coverage completeness states
= 1,000 cases
```

Each source dimension is PRESENT, ABSENT, SUBSTITUTED, STALE, or WRONG_DOMAIN. Each case records O02, O06, O10 and O16 acceptance/rejection clauses and repeats after canonical reload. Expected truth is derived from the ownership table, separately from predicate outputs:

- HISTORY accepts iff evidence is PRESENT or STALE, override is PRESENT, and history is consistent.
- GRAPH accepts iff evidence and graph are PRESENT.
- O16 accepts iff all three are PRESENT, history is consistent, and composition coverage is complete.

These formulas apply to the fixed bases with all other prerequisites valid; they are not a universal simplification of the governing predicates. REVOKED is tested separately with STALE in 12 ordered invalidation sequences across three roles and both bases. Twenty-four further substitutions alter scope, lineage, runtime, ledger, identity or provenance in evidence/override payloads. All reject as required. The original twelve failures are also retained explicitly.

Results: **1,000 combinatorial cases PASS; 24 targeted substitutions PASS; 12 CE-01 reproductions reconciled; 12 additional invalidation sequences PASS.** Existing **313 specification cases and 11 sequences PASS** unchanged, including O03, O08 and O09. The old 62-case output digest remains `4066636d7965eb02642ca73a8cb1463ddcc9e2e83d1e89727ddac96a43d72001` under the refinement. New rejection behavior is confined to previously untested supporting-source omissions/substitutions.

## Minimum dependency metadata

Metadata is required to make the relationships machine-checkable. The companion specifies predicate identities, phase and exact source roles for REQUIRES_SOURCE; required component identities for COMPOSES/REQUIRES_ADMISSION; the one-way acceptance implication for REFINES; and the limited downstream meaning for OPERATIONALIZES. A consumer must reject unknown relation kinds, dangling predicate references or conflicting source requirements. Entries bind to the pinned predicate/profile version rather than a display name alone.

No new metadata runtime or registry is implemented. The metadata explicitly denies permission inference: OPERATIONALIZES means the coherent admitted instance may be supplied to existing planner gates, not that those gates pass. Currentness/provenance/source identity remains conjunctive with the original predicates.

## Complete preflight and status

All eight assignments are rechecked: O01 source ACTION; O02/O06 refined HISTORY; O03 original bounded-result predicates; O08 original exact grant chain; O09 both baseline slot predicates; O10 refined GRAPH; O16 unchanged composition over refined components. The mapping inventory, O08/O09 submissions and cross-envelope bindings are unchanged. The full original specification suite plus the new meta-invariants and product yield no remaining mismatch, conflict or exception in this bounded contract set.

C06A-3 retry is permitted only by this conjunction: CE-01 local-source ownership resolved; refined predicate identities fixed; original suites pass; new five meta-invariants pass; all 1,000 product cases pass; complete eight-element preflight is clean. This permits a future implementation retry, not implementation conformance or qualification.

```text
CE_01_REPRODUCED = YES
CE_01_CLASSIFICATION = A_LOCAL_PREDICATES_UNDER_CONSTRAINED
ADMISSION_LAYERS = [LOCAL_OBJECT_VALIDITY, LOCAL_OBJECT_ADMISSION, COMPOSITION_ADMISSION, OPERATIONAL_USE_ADMISSION]
O02_RECONCILIATION = mandatory evidence/override payload admission added
O06_RECONCILIATION = mandatory evidence/override payload admission added
O10_RECONCILIATION = mandatory evidence payload admission added
O16_RECONCILIATION = executable constraints preserved; refinement metadata explicit
CROSS_ORACLE_META_INVARIANTS = PASS
COMBINATORIAL_CASES = 1000
COMBINATORIAL_RESULT = PASS
ORACLE_DEPENDENCY_METADATA_REQUIRED = YES
C06A_3_CONTRACT_MISMATCH_SET = []
C06A_3_CONTRACT_CONFLICT_SET = []
C06A_3_CONTRACT_EXCEPTION_SET = []
C06A_3_RETRY_ALLOWED = YES
RESTORED_AND_QUALIFIED = 2/17
C06A_4_READY = NO
C07_RETRY_ALLOWED = NO
F03_STATUS = CLOSED
V0_1_CURRENT_STATUS = CORRECTION_REQUIRED
IMPLEMENTATION_MODIFIED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
```
