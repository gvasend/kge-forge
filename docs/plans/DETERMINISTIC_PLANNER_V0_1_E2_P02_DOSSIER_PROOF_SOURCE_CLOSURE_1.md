# E2-P02 Decision-Dossier Proof-Source Closure

## Result

The current `0/11` state is **COMBINED**: the two required-fact proof
propositions and sources are defined by the canonical knowledge contracts, but
the nine dossier checks have no authoritative proposition/proof-source rule
beyond fixture labels. Runtime dossier binding and proof construction are also
not available. No proof was materialized.

## Obligation matrix

### Required facts

`E2-KP-CHECK` means that the accepted, current `E2-K-CHECK` knowledge record
was produced by `E2-CHECK` under the E2 scope/lineage. Its producer, source
identity, construction (`PredicateKind.KNOWLEDGE_ACCEPTED`) and consumer
(`DecisionDossier.required_facts`) are defined. The same is true for
`E2-KP-COLLECT` and `E2-K-COLLECT`. These are **READY_FOR_MATERIALIZATION**
once predicate instances are placed in the runtime state; they are not yet
admitted in the current snapshot.

### Dossier checks

The nine IDs are present in the authoritative dossier and PC02 fixture, and
their requirement origin is the native `DossierCheck`/`DecisionDossier`
contract as exercised by PC02. The records do not define the proposition each
check proves, its authoritative source content, or a typed proof/admission
rule. The PC02 oracle validates that the labels and count are present; it does
not create native predicates or prove them. Each check is therefore
`PROPOSITION_UNDEFINED` and `CONSTRUCTION_RULE_MISSING`, not an inferred
PASS.

| Obligation | Proposition | Source / producer | Current status |
|---|---|---|---|
| E2-KP-CHECK | accepted E2-K-CHECK | E2-CHECK result; knowledge predicate | READY_FOR_MATERIALIZATION |
| E2-KP-COLLECT | accepted E2-K-COLLECT | E2-COLLECT result; knowledge predicate | READY_FOR_MATERIALIZATION |
| QUESTION_SCOPE | undefined beyond check label | dossier/PC02 fixture; validator undefined | PROPOSITION_UNDEFINED |
| SOURCE_PROVENANCE | undefined beyond check label | dossier/PC02 fixture; validator undefined | PROPOSITION_UNDEFINED |
| CONCRETE_ALTERNATIVES | undefined beyond check label | dossier/PC02 fixture; validator undefined | PROPOSITION_UNDEFINED |
| ASSUMPTIONS_CONSEQUENCES | undefined beyond check label | dossier/PC02 fixture; validator undefined | PROPOSITION_UNDEFINED |
| AUTHORITY_BOUNDARY | undefined beyond check label | dossier/PC02 fixture; validator undefined | PROPOSITION_UNDEFINED |
| DOWNSTREAM_QUALIFICATION | undefined beyond check label | dossier/PC02 fixture; validator undefined | PROPOSITION_UNDEFINED |
| NO_INVENTED_FACTS | undefined beyond check label | dossier/PC02 fixture; validator undefined | PROPOSITION_UNDEFINED |
| DECISION_FACTS_COMPLETE | undefined beyond check label | dossier/PC02 fixture; validator undefined | PROPOSITION_UNDEFINED |
| INDEPENDENT_VALIDATION | undefined beyond check label | dossier/PC02 fixture; validator undefined | PROPOSITION_UNDEFINED |

The checks are deterministic validations over dossier/source content in
concept, but no canonical validator output type or independent oracle binds
those validations to native proof instances. The current Planner has typed
predicate evaluation, but no generic “validated dossier check → admitted
proof” transaction for these undefined propositions.

## Lifecycle and routes

The fact route is already available after CHECK/COLLECT; it is not an
external acquisition route. The dossier-check route is undefined because the
authoritative propositions and sources are undefined. No `MISSING_CONTROL_ROUTE`
is asserted here; the missing item is the proof-source contract first.

The E2-PREPARE → dossier binding also remains absent from the materialized
Action/result path. Its producer is E2-PREPARE, but native admission requires a
bound dossier plus all independently admitted required facts/checks.

## Closure packages (not executed)

1. **DPC01 — dossier-check semantic contract**: define the nine propositions,
   authoritative source content, deterministic validator rules and independent
   oracles. Unlocks a complete proof-source matrix for all checks.
2. **DPC02 — static fact/binding materialization**: add the two typed fact
   predicate instances and bind the authoritative dossier candidate to the
   E2-PREPARE result contract without prepopulating actual runtime facts.
3. **DPC03 — runtime proof constructor/admission**: provide the native path
   from actual PREPARE result and qualified inputs to the 11-proof set and
   existing dossier admission. Require negative cases and deterministic
   replay.

`DOSSIER_PROOF_MATERIALIZATION_RETRY_ALLOWED = NO` until all three packages
provide propositions, sources, producers, construction rules, admission rules,
routes and independent oracles.

```text
PROOF_OBLIGATIONS = 11
PROPOSITIONS_DEFINED = 2/11
SOURCES_DEFINED = 2/11
PRODUCERS_DEFINED = 2/11
CONSTRUCTION_RULES_DEFINED = 2/11
CONTROL_ROUTES_DEFINED = 2/11
READY_FOR_MATERIALIZATION = 2/11
CLASSIFICATION = COMBINED
E2_P02_RETRY_ALLOWED = NO
E2_P03_READY = NO
N_REAL_SATISFIED = NO
CANONICAL_E2_QUALIFIED = NO
IMPLEMENTATION_MODIFIED = NO
EXPERIMENT_ACTIONS_EXECUTED = 0
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
```
