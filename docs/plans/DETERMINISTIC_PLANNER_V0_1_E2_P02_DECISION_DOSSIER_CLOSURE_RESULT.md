# Deterministic Planner v0.1 — E2-P02 Decision-Dossier Closure

## Result

`E2-P02-DECISION-DOSSIER-CLOSURE = BLOCKED`.

The authoritative source contains a complete `DecisionDossier` candidate for
`E2-DECIDE`, attached to the source definition of `E2-PREPARE`. Its canonical
content identity is:

`6a507317bc9cc323fbaa626e97b5954cf3ad934b0bd92d9dc96bd4f63e07bddb`.

The native snapshot used by P02 does not carry that candidate on the Action or
result path. More fundamentally, it does not contain the predicate and typed
proof entities required to independently admit the dossier. Native rejection
is therefore correct and fail-closed:

```text
input PASS requires complete independently proved dossier
```

No dossier, proof, decision readiness, authority, or evidence was fabricated.

## Counterexample pin

The replayed state immediately before preparation is
`43a238851a34b2e58f4a49ec870fa258fdcb8d3a88fda50a305df2b570281e79`.
It contains completed `E2-CHECK` and `E2-COLLECT`, their accepted knowledge,
and the qualified `DecisionRoute:E2-DECIDE:E2-PREPARE`. Native selection is
`E2-PREPARE` and control is `RUNNABLE`.

The source Action definition declares a prospective `E2-K-PREPARE` output and
contains the dossier candidate. The actual supplied PASS result contains no
dossier, and the materialized Action has no `prepared_dossier`, so admission
rejects before producing a post-state. `POST_STATE_ID = NONE`.

## Dossier contract and sources

| Field | Type / identity | Authoritative source | Status |
|---|---|---|---|
| `decision` | `ActionId` | source `prepared_dossier.decision` | available |
| `provenance` | `Provenance` | source dossier | available |
| `question` | string | source dossier | available |
| `scope` | scope string | source dossier / E2 context | available |
| `alternatives` | ordered strings | source dossier | available |
| `checks` | typed `DecisionCheck[]` | source dossier | available |
| `required_facts` | `PredicateId[]` | source dossier | available |
| `deferred_downstream_facts` | strings | source dossier | available |
| `authority_granted_if_approved` | bounded declaration | source dossier | available |
| `authority_excluded` | bounded declaration | source dossier | available |
| `validation` | `ValidationState` | source dossier | available |
| dossier identity | content identity | canonical serialization | derivable |

The candidate is not historical execution evidence. It describes the
definition-time decision question and its bounded alternatives.

## Independent proof obligations

Admission requires all source-bound required facts and dossier checks to be
proved independently:

```text
required facts:
  E2-KP-CHECK
  E2-KP-COLLECT

checks:
  E2-CHECK-QUESTION_SCOPE
  E2-CHECK-SOURCE_PROVENANCE
  E2-CHECK-CONCRETE_ALTERNATIVES
  E2-CHECK-ASSUMPTIONS_CONSEQUENCES
  E2-CHECK-AUTHORITY_BOUNDARY
  E2-CHECK-DOWNSTREAM_QUALIFICATION
  E2-CHECK-NO_INVENTED_FACTS
  E2-CHECK-DECISION_FACTS_COMPLETE
  E2-CHECK-INDEPENDENT_VALIDATION
```

The current snapshot has none of these dossier proof predicate instances;
it only has `E2-PROOF`. PC02’s fixture/oracle records the required checks but
does not create native predicate/entity admissions. Consequently:

```text
DOSSIER_CONSTRUCTION = SOURCE_CANDIDATE_COMPLETE
DOSSIER_PROOF = BLOCKED (11 proof instances absent)
DOSSIER_ADMISSION = REJECTED
```

The missing work is a bounded canonical materialization contract for the
source dossier, its producer/result binding, and the eleven independent proof
instances. It must preserve source identity, scope, lineage, currentness and
provenance. It must not turn Action PASS into decision readiness.

## Replay and control

The CHECK/COLLECT/PREPARE replay is:

```text
CHECK  -> PASS -> E2-K-CHECK
COLLECT -> PASS -> E2-K-COLLECT
PREPARE selected with route -> admission rejected (missing dossier)
```

The P02 target `EXTERNAL_WAIT` was not reached. No post-dossier control
oracle exists yet because dossier admission did not occur. No additional E2
Action was executed.

Classification: `COMBINED` — qualified-model omission of the dossier/result
binding plus missing native proof-instance materialization. This is not a
Planner runtime defect.

The static control-closure lesson is retained: preflight must verify that
every governed output required by a downstream control transition has a
producer, construction rule, proof rule, admission rule and consumer path.

```text
E2_P02_RETRY_ALLOWED = NO
OTHER_P02_BLOCKERS = [CANONICAL_DOSSIER_BINDING, DOSSIER_PROOF_INSTANCES]
E2_P03_READY = NO
N_REAL_SATISFIED = NO
CANONICAL_E2_QUALIFIED = NO
IMPLEMENTATION_MODIFIED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
```
