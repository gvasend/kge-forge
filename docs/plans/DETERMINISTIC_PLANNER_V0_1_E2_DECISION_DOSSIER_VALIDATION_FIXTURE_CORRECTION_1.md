# E2 Decision-Dossier Validation Fixture Correction

## Result

`FIXTURE_CORRECTION = PARTIAL`.

Six categories can be grounded in the native schema/admission contract. Three
labels remain contract-source-missing and are not assigned invented meaning.
The corrected registry therefore does not yet unlock proof materialization.

## Supported categories

| ID | Normalized proposition | Native basis | Mechanism |
|---|---|---|---|
| QUESTION_SCOPE | question and scope are present and non-empty | `decision_readiness` dossier-structure check | structural |
| SOURCE_PROVENANCE | dossier provenance passes native provenance validation | `validate_p04` / `validate_provenance` | source-bound |
| CONCRETE_ALTERNATIVES | alternatives are non-empty, unique, and each option is non-empty | `decision_readiness` structure check | structural |
| AUTHORITY_BOUNDARY | both authority-granted and authority-excluded declarations are present | native dossier structure check | structural |
| DECISION_FACTS_COMPLETE | required-fact predicates are present and evaluate proved | `decision_readiness` required-facts evaluation | source-bound |
| INDEPENDENT_VALIDATION | dossier validation state is `ACCEPTED` and support is current | native validation/currentness checks | currentness-bound |

Each supported category has a positive canonical fixture and a single-field
negative mutation. The mutation is evaluated independently from Planner output.
The corresponding generic hooks are sufficient; no native implementation
change is indicated.

## Unsupported categories

These labels remain undefined by the E2 plan, acceptance matrix, dossier
schema, PC02 contract, and native admission code:

- `ASSUMPTIONS_CONSEQUENCES`
- `DOWNSTREAM_QUALIFICATION`
- `NO_INVENTED_FACTS`

Their names do not establish propositions. No authoritative source identifies
the content to inspect, the proof rule, or an independent negative mutation.
They are recorded as `CONTRACT_SOURCE_MISSING` and are excluded from the
materialization retry gate.

## Fact proofs and oracle

The two fact predicates remain separate independent proof inputs:
`E2-KP-CHECK` and `E2-KP-COLLECT`. They are ready for materialization from the
actual accepted CHECK/COLLECT knowledge records, but are not materialized in
this fixture correction.

The corrected independent oracle accepts only when both facts are proved and
all six supported validations pass. It returns `UNDEFINED_CONTRACT` when any
of the three unsupported categories is requested, rather than treating an
undefined label as true.

## Impact and gate

Affected qualification is limited to E2-A04, E2-A05, and the P02
PREPARE-to-decision transition. Earlier CHECK/COLLECT, route, source-role and
external-gate evidence remains preserved. No Action was executed and no
snapshot was changed.

```text
VALIDATION_CATEGORIES = 9
PROPOSITIONS_DEFINED = 6/9
PREDICATES_DEFINED = 6/9
POSITIVE_FIXTURES = 6/9
NEGATIVE_FIXTURES = 6/9
AMBIGUOUS_CATEGORIES = []
CONTRACT_SOURCE_MISSING = [ASSUMPTIONS_CONSEQUENCES, DOWNSTREAM_QUALIFICATION, NO_INVENTED_FACTS]
FACT_PROOFS_READY = 2/2
DETERMINISTIC_VALIDATIONS_READY = 6/9
NATIVE_HOOKS_SUFFICIENT = 6/9
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
