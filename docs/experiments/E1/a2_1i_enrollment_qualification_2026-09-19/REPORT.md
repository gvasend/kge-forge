# A2.1i — Prospective enrollment component

**ENROLLMENT_COMPONENT_QUALIFICATION_PASS** — 22 component probes passed (21-test suite plus the explicit predecessor-lock probe). **R2 readiness remains unestablished.**

The Architect's prospective material delegation supplies the authority basis that was absent in the earlier assessment. It authorizes implementation and qualification, **not actual C2 enrollment or adoption**. The staged component separates candidate creation, independent qualification attestation, exact enrollment authorization and later adoption.

## Scope and authority model

`candidate/continuation_enrollment.py` is new staged code. No accepted runtime, bootstrap, private production catalog or authority journal was modified. The component has no adoption operation, no runtime-head writer and no invocation/model/effect interface.

```text
Unchanged accepted bootstrap → unchanged runtime-head authority → C1 → current R1

Prospective Architect material delegation (separate authority basis)
  → qualified enrollment mechanism [staged, not production-selected]
  → independently qualified exact candidate
  + separately authenticated exact enrollment decision
  → append-only eligibility event
  + separately authenticated exact adoption authorization [not present for C2]
  → ordinary adoption integration [not yet qualified]
```

The copied `ARCHITECT_DELEGATION_SOURCE.md` records the user decision. Its presence in the repository is documentary provenance, not automatic operational authority. Production use requires an externally authenticated private-store selection for this delegation, qualified mechanism and authority intake. The component cannot provision its own trusted decision entries.

## Implementation

The component consumes a pinned controller-private catalog. Candidate content alone does not qualify. A qualification attestation must be selected under a distinct `qualification-attestation:<digest>` authority reference and bind exact candidate digest, policy, evidence and qualification/production scope. An enrollment decision must independently be selected under `enrollment-decision:<digest>` and bind exact delegation, candidate, qualification and predecessor head event. An actor string, PASS field, candidate-created file or ordinary content-addressed object does not substitute for these trusted selections.

The delegation is separately selected, content sealed, implementation bound, lineage/context bound and limited to `ENROLL_EXACT_QUALIFIED_CONTINUATION_ONLY`. No implicit future authority is attributed to bootstrap or R1. Synthetic decision catalogs used by tests are explicitly `QUALIFICATION_BINDING`; the production API mode rejects them.

Enrollment rechecks runtime ancestry through the established runtime consumer. It holds a shared runtime-head lock followed by an exclusive enrollment-journal lock through the append and fsync. This prevents a predecessor transition during enrollment commit, uses consistent lock ordering and does not mutate the head. Journal rows bind sequence, previous event digest, delegation, candidate, qualification, exact enrollment decision, predecessor and head event. Changed, duplicated, reordered, torn or unattributable records fail closed. Exact repetition cannot append another enrollment.

Eligibility consumption rechecks the exact record, dependencies, live successor inventory and fresh runtime head. Its return value grants no runtime-transition authority and must not be cached as permanent eligibility. A future adoption integration must serialize its separate authorized transition, recheck eligibility under that transaction, and avoid nested reacquisition of the runtime-head lock. That integration has not been implemented or qualified in this package.

## Qualification and limits

The fixtures use the real existing C2 implementation inventory and read-only reconstruction of actual current R1. Enrollment journals, decisions, qualification attestations and catalogs are isolated under private temporary directories. Synthetic qualification attestations certify only the enrollment contract exercised by these tests; they do not pretend to be complete production C2 runtime qualification.

Positive qualification establishes that the exact candidate can receive an eligibility event from an independently selected fixture decision and that eligibility reconstructs after reopening the store. R1 remains current. The frozen ordinary adoption validator continues to reject presenting enrollment as adoption authority.

Negative probes cover qualified-but-unenrolled content, missing delegation, unrelated delegation, absent selected enrollment decision, unauthorized actor, missing qualification attestation, qualification mismatch/substitution, candidate substitution, wrong candidate at consumption, stale head decision, enrollment replay, changed/torn journal, qualification-to-production crossover and simultaneous duplicate enrollment. Fault injection tests predecessor/head change and interruption after append before fsync acknowledgment; these are explicitly synthetic fault probes, not production head transitions or power-loss durability claims. A lock probe verifies that an exclusive runtime-head lock cannot be obtained while the enrollment append holds its predecessor stable.

Ordinary C2 adoption success, adoption replay, R2 self-selection and complete production runtime integration are **not qualified by this component-only suite**. There is no production C2 qualification identity, enrollment identity or adoption authorization. The isolated sample includes exact synthetic identities and must never be promoted into production decisions.

## Applicability

Enrollment capability and its future runtime-selection integration are MATERIAL authority functionality under the new prospective delegation. No non-material continuation classification is used to hide that authority extension. The accepted bootstrap, C1, R1, release/context identities, budgets, status and invocation semantics remain untouched.

Final results, candidate implementation hash, exact isolated sample identities and preservation evidence are in `head_locked/PUBLICATION.json`, `head_locked/ISOLATED_SAMPLE.json` and `head_locked/TESTS.log`. Earlier top-level test/publication artifacts describe the initial component revision and are superseded for qualification by the head-locked revision; they are retained as evidence, not silently overwritten.

The required next boundary is qualified ordinary-consumer integration plus explicit exact production enrollment and adoption decisions. This package does not claim C2/R2 readiness. Zero r13 invocations, real model requests or E1 effects were created.
