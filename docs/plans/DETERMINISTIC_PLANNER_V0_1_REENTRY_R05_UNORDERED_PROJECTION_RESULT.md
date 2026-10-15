# REENTRY-R05 — unordered validation input projection consistency

RESULT = PASS. A11_NATIVE_PATH_QUALIFIED = PASS. A11_DEFINITION_READINESS = YES. A11_READY = YES. P04_EXECUTION_READY = NO.

The generic validation repair aligns semantic admission with the codec's existing unordered input-identity contract. No E2-specific normalization, codec/hashing change, definition installation or authority issuance occurred. Canonical A09–A12 remain unexecuted.

## Counterexample and field contract

The actual R04 post-event state reproduced VALIDATION_PROJECTION_REQUIRED before repair when only the ValidationResult input tuple was reversed, despite identical canonical snapshot/bundle bytes and identities. A two-input native model component also reproduced PASS for [A,B] and rejection for [B,A] through model.validate_model → validation_transaction.validate_records → positional projection comparison. Its before implementation is hash-verified against the captured pre-repair file; the component is not represented as an admitted event-bearing state. After repair both orderings pass. Exact data is in the companion.

Native assessment/result/support input_identities are tuple fields declared unordered by codec.SET_FIELDS (codec.py:80–82). Native input construction already produces a sorted unique set. Codec serialization sorts without discarding duplicates; it is not a multiset authorization. Duplicate identities are now rejected explicitly, not silently collapsed. Identity domains retain kind, namespace and hash. Different membership retains different bytes/identity. Legacy ValidationInstance.inputs remains intentionally ordered and its canonical identity contract is unchanged.

## Consumers and repair

Three consumers conflicted with the unordered contract: assessment binding compared raw tuples; project copied presentation order into the ordered legacy projection; validate_records compared that projection to raw result inputs. The shared canonical_inputs helper enforces uniqueness and the existing deterministic identity order across all three. Public result/support admission also requires exact matching input membership. All original source, outcome, command, receipt, scope/lineage/generation, provenance and currentness checks remain.

Root cause = combined admission/projection order sensitivity, not a codec or identity defect. Record/event canonical comparisons were already order-independent. Invalidation already uses membership intersections. Proof and C03 inherited the faulty model guard; their own epistemic, event, authority and Action prerequisites remain unchanged. The [hash-verified generic diff](qualification/REENTRY_R05_1/generic-repair.diff) and complete consumer inventory are recorded in the evidence.

## Permutations and membership

130 component permutations covered cardinalities 0,1,2,3,5 with equal bytes/identity and deterministic projection. The actual A10 DAG requires 15 inputs; small subsets are rejected in every order rather than treated as valid validation/proof. Complete actual states were reversed, rotated and canonically sorted across assessment, ValidationResult and support inputs: model admission, typed Proof, C03, canonical bundle/state/event identities, persistence and replay all matched. Native source invalidation withdrew eligibility in each equivalent presentation.

Five additional generic unit tests cover permutation equivalence, duplicate rejection, distinct identity namespaces/membership, untyped Boolean operands and preservation of ordered legacy projection semantics. [A,B] versus [A,C], and [A] versus [A,B], remain distinct; changed result membership cannot reuse the old support projection. No membership or cardinality information is erased.

## Complete R04 requalification

The positive A09/A10 isolated reproduction, obligation Proof, external DEPENDENT_ACTION_REENTRY and separately required E2-DECIDE DecisionReentry all passed. C03 makes only E2-REENTER eligible/actionable/selected and passes the A12 initial oracle. No ActionResult, REENTER execution/completion, root/slot proof or FINISH result was produced.

All 28 R04 negatives, exact-envelope/stale-result retries and applicable source/validation/support/DECIDE/ATTEST invalidation passed. Unrelated USE withdrawal still preserves eligibility. Four fresh independent reproductions from the same canonical start, across seeds 0,1,7,101 and native-declared unordered permutations, matched the original R04 bundle identity `6b1e2cec5c5163552d496e5b682fe72652c297cfa22b75ee9c538931ade767e0`. After the isolated writer exited, 12 fresh cold readers (three per seed) matched complete native identities, Proof/C03/Computation and history; post-event reversal now passes. Derived eligibility appears only in comparison reports, not canonical state or permission records.

73 targeted tests passed: 68 affected regressions and five new generic input-set tests. The regressions cover validation/support and V02, E03/E04/E07 receipt boundaries, I01–I04 installation, root/slot proof, native reentry/Action reevaluation, event ancestry, persistence/replay and cold restore. R01–R03 semantics and all R04 qualification dimensions are separately covered by the new isolated chain. No broad-suite PASS is claimed; unrelated historical frozen-E1 collection failures remain separate.

## Readiness and preservation

No missing A11 prospective definition was found. Existing native requirement/gate/named reentry/C03 and current A09/A10 definitions suffice. A11_READY = YES is prospective readiness; no canonical A11 event exists yet. P04_EXECUTION_READY remains NO.

A12 first blocker: canonical E2-REENTER accepted_inventory is empty; bounded prospective PASS + E2-K-REENTER accepted-result materialization/installation remains unclosed. No A12 redesign or execution occurred. The next package is bounded accepted Action-result/knowledge contract and legitimate installation/materialization closure.

Only adapter/planner/validation_transaction.py changed among 12833 protected input/runtime/E1 files. All prior qualification records, canonical P04 bundle and frozen E1 hashes remain unchanged. A09/A10/A11/A12 canonical execution = NO; RESUME_ELIGIBILITY_PERSISTED = NO; P03_RESULT = PASS; historical correspondence = UNPROVEN; N_REAL_SATISFIED = NO; E1_ARTIFACTS_MODIFIED = 0; PRODUCTION_EFFECT = NO; git diff --check = PASS.

The [machine-readable companion](DETERMINISTIC_PLANNER_V0_1_REENTRY_R05_UNORDERED_PROJECTION_RESULT.json) includes the field/consumer inventory, counterexamples, repair, per-case qualification, regression results, A11 readiness and A12 frontier. Reproduce component checks with `python3 adapter/tests/qualify_reentry_r05.py components`, full-state permutations with `... permutations`, and independent readers with `... read reverse`, using PYTHONDONTWRITEBYTECODE=1 and PYTHONPATH=.
