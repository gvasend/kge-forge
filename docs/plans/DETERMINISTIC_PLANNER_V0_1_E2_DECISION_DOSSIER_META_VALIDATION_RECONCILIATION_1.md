# E2 Decision-Dossier Meta-Validation Boundary Reconciliation

## Result

The original nine-label fixture was **BOTH OVER_SCOPED AND UNDER_SPECIFIED**.
Six categories have native dossier-level rules. The other three do not form a
valid additional dossier predicate set:

| Category | Disposition | Layer | Dossier admission? |
|---|---|---|---|
| `ASSUMPTIONS_CONSEQUENCES` | unsupported label; no E2 proposition or dossier field | `UNRESOLVED` | `NO` |
| `DOWNSTREAM_QUALIFICATION` | later qualification concern | `L6_EXPERIMENT_QUALIFICATION` | `NO` |
| `NO_INVENTED_FACTS` | global source/provenance governance invariant | `L7_GLOBAL_GOVERNANCE` | `NO` |

`ASSUMPTIONS_CONSEQUENCES` has no authoritative E2 field, proposition, or
native admission condition. The dossier has bounded authority declarations
and deferred downstream facts, but neither establishes an assumptions-truth
predicate. No dossier-level Boolean is authorized.

`DOWNSTREAM_QUALIFICATION` concerns later decision/action qualification. A
dossier may describe downstream consequences, but native dossier admission
does not prove a future qualification outcome. It is enforced by later E2
phase gates (A05/A12 and aggregate D01/END ownership).

`NO_INVENTED_FACTS` is a governance invariant enforced through source-bound
provenance, admitted knowledge and the two independent fact predicates. A
dossier asserting the phrase cannot prove it, so it is not a separate
dossier predicate.

## Reconciled dossier boundary

The actual dossier-level set is:

```text
2 independent fact proofs:
  E2-KP-CHECK
  E2-KP-COLLECT

6 deterministic validations:
  QUESTION_SCOPE
  SOURCE_PROVENANCE
  CONCRETE_ALTERNATIVES
  AUTHORITY_BOUNDARY
  DECISION_FACTS_COMPLETE
  INDEPENDENT_VALIDATION
```

The native implementation matches this boundary. It evaluates dossier
structure/currentness, required facts and referenced predicates; it does not
evaluate the three rehomed labels. No implementation change is indicated.

## Rehomed requirements

- Downstream qualification remains required at E2-A05 (recorded decision and
  bounded authority), E2-A12 (post-reentry continuation), and aggregate D01 /
  END gates. No new matrix case is required.
- No-fabrication remains a global invariant at source binding, knowledge
  admission and negative source-substitution cases (A01/A03/N05). No new
  dossier predicate is required.
- Assumptions/consequences remains an unsupported fixture label. It is not
  discarded as a governance principle; it simply has no current Boolean
  contract and therefore cannot gate dossier admission.

## Readiness

Both fact proofs are ready and all six actual dossier validations are defined
with native hooks and independent fixture mutations. Therefore dossier proof
materialization is now permitted; P02 execution is not yet permitted until
materialization and native admission succeed.

```text
FACT_PROOFS_READY = 2/2
DOSSIER_VALIDATIONS_DEFINED = 6/6
NON_DOSSIER_REQUIREMENTS_ASSIGNED = 2/2
FIXTURE_CLASSIFICATION = BOTH
ACCEPTANCE_MATRIX_CHANGES_REQUIRED = NO
P01_CASES_AFFECTED = [E2-A04, E2-A05, E2-P02-PREPARE-DECISION]
IMPLEMENTATION_COMPARISON = IMPLEMENTATION_MATCH
DOSSIER_PROOF_MATERIALIZATION_RETRY_ALLOWED = YES
NEXT_CONTROL_STEP = DOSSIER_MATERIALIZATION_READY
E2_P02_RETRY_ALLOWED = NO
E2_P03_READY = NO
N_REAL_SATISFIED = NO
CANONICAL_E2_QUALIFIED = NO
IMPLEMENTATION_MODIFIED = NO
EXPERIMENT_ACTIONS_EXECUTED = 0
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
```
