# E2 Decision-Dossier Validation Contract Reconciliation

## Result

The native admission contract does **not** require nine separately persisted
proof objects merely because the PC02 fixture lists nine check labels. It
requires:

1. a non-stale dossier;
2. each required fact predicate to evaluate `PROVED`; and
3. one `DecisionCheck` for every `DossierCheck` enum member, whose referenced
   predicate evaluates `PROVED`.

The two required facts are independent knowledge predicates. The nine labels
are deterministic validation categories, evaluated through native predicates.
Their actual propositions and predicate sources are not defined by the
current fixtures, so validation cannot yet be materialized safely.

## Native admission conditions

`gates.decision_readiness` evaluates:

| Native condition | Inputs | Failure |
|---|---|---|
| decision support is current | `unavailable_support`, dossier action | `STALE` |
| dossier exists | `Decision.dossier` | `DOSSIER_MISSING` |
| dossier is current | `dossier.validation` | `STALE_DOSSIER` |
| required facts prove | `dossier.required_facts`, snapshot predicates/knowledge | `FACT_BLOCKED` |
| all nine check kinds are present exactly once | `dossier.checks`, `DossierCheck` enum | semantic incompleteness |
| every check predicate proves | predicate registry/entities/content | semantic incompleteness |
| dossier structure is non-empty | question, scope, alternatives, authority bounds | `DOSSIER_STRUCTURE_INCOMPLETE` |

The generic native implementation matches this contract. It neither asserts
the labels nor creates proof records. It evaluates the referenced predicates.

## Nine-label origin matrix

All nine labels originate in the PC02 qualification fixture and are consumed
as `DecisionCheck.kind` values. Their enum categories are native, but their
E2-specific propositions are not supplied by the current fixture or plan.

```text
QUESTION_SCOPE
SOURCE_PROVENANCE
CONCRETE_ALTERNATIVES
ASSUMPTIONS_CONSEQUENCES
AUTHORITY_BOUNDARY
DOWNSTREAM_QUALIFICATION
NO_INVENTED_FACTS
DECISION_FACTS_COMPLETE
INDEPENDENT_VALIDATION
```

Classification for every label: `CONTRACT_UNDERSPECIFIED`. The corresponding
predicate IDs are present as names in the source dossier, but the proposition,
source content and proof rule behind each ID are not authoritative.

## Reconciled requirements

| Requirement | Type | Proof object required? | Current state |
|---|---|---:|---|
| `E2-KP-CHECK` | independent `KNOWLEDGE_ACCEPTED` fact | yes | source/producer defined; predicate instance absent |
| `E2-KP-COLLECT` | independent `KNOWLEDGE_ACCEPTED` fact | yes | source/producer defined; predicate instance absent |
| nine `DossierCheck` predicates | deterministic/source-bound validation | no separate proof record mandated | proposition/source/rule undefined |
| dossier structure and currentness | structural validation | no | native rule defined |

Thus:

```text
INDEPENDENT_FACT_PROOFS = 2
INDEPENDENT_OTHER_PROOFS = 0
DETERMINISTIC_VALIDATIONS = 9
SOURCE_BOUND_VALIDATIONS = 9 (once their propositions are defined)
RECONCILED_PROOF_COUNT = 2
RECONCILED_VALIDATION_COUNT = 11
```

The nine validations still block admission, but they should not be placed in
the proof-materialization queue until their predicate contracts exist.

## Fixture classification and impact

`PC02 = FIXTURE_UNDERSPECIFICATION`: it promoted nine check labels into
required records without defining the propositions those predicate IDs must
evaluate. No Planner implementation defect is shown. The bounded affected
qualification set is E2-A04 (dossier readiness), E2-A05 (decision plus grant),
and the E2-P02 PREPARE-to-decision transition. Other source, route and
external-lifecycle cases remain preserved.

The independent admission oracle must evaluate the two fact predicates,
eleven native check/structure conditions, and reject any undefined predicate.
Negative cases should target missing/unknown predicate, wrong source or
scope, stale support, incomplete structure, and missing dossier.

## Next control step

`FIXTURE_CORRECTION_REQUIRED`. Define the nine E2-specific propositions,
authoritative source bindings, and native predicate rules before any proof or
dossier materialization retry. No new semantic authority is issued here.

```text
DOSSIER_PROOF_MATERIALIZATION_RETRY_ALLOWED = NO
E2_P02_RETRY_ALLOWED = NO
E2_P03_READY = NO
N_REAL_SATISFIED = NO
CANONICAL_E2_QUALIFIED = NO
IMPLEMENTATION_MODIFIED = NO
EXPERIMENT_ACTIONS_EXECUTED = 0
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
```
