# External unknown-rule control repair 1

RESULT = PASS

This bounded repair separates an independently source-bound external-resolution contract from positive proof. It changes control interpretation only: the required rule remains unknown, evidence remains absent, actionability remains empty and resume remains false. Existing unbound unknown-rule gates still produce PLAN_DEFECT.

## Pinned authority and pre-repair evidence

The repair uses the unchanged [reconciliation](DETERMINISTIC_PLANNER_V0_1_EXTERNAL_UNKNOWN_RULE_RECONCILIATION_1.md) and [reproducible validation companion](DETERMINISTIC_PLANNER_V0_1_EXTERNAL_UNKNOWN_RULE_RECONCILIATION_1_VALIDATION.json). Their raw SHA-256 identities are:

- `DETERMINISTIC_PLANNER_V0_1_EXTERNAL_UNKNOWN_RULE_RECONCILIATION_1.md`: `ddce8953120bb1111d832b6d80148497d502c5e14338c38d53dcafb55d8e11f0`.
- `DETERMINISTIC_PLANNER_V0_1_EXTERNAL_UNKNOWN_RULE_RECONCILIATION_1_VALIDATION.json`: `48a1e7e69e958e07ff1fbcf58790161cd8cc2cf0a7e966feb3eeb6015d2c63f0`.

The counterexample was promoted into [test_planner_external_unknown.py](../../adapter/tests/test_planner_external_unknown.py) before repair. Running `python3 -m unittest adapter.tests.test_planner_external_unknown` failed at the unchanged expected assertion: actual PLAN_DEFECT versus expected EXTERNAL_WAIT. The run recorded one failure, not a parser/import failure. PRE_REPAIR_COUNTEREXAMPLE=REPRODUCED; PRE_REPAIR_REGRESSION=FAIL_EXPECTED.

The original fixture expressed independent acquisition correspondence in its synthetic source contract. The old gate type carried only a generic completeness Boolean and prose provenance. The permanent regression now gives that same governed-acquisition premise an explicit persisted typed binding. This is necessary to avoid accepting arbitrary unbound waiting labels. The original *unbound encoding* is retained as a negative control; merely replaying those old bytes without the new binding still produces PLAN_DEFECT. No oracle expectation was changed and no source-shaped prose is automatically interpreted as authority.

## Implementation

- [model.py](../../adapter/planner/model.py): additive immutable `ExternalResolutionContract` and default-empty `ExternalGate.resolution_contracts`. The record binds request, gate, missing proposition/EvidenceId, typed target, expected producers/source class, requirement/gate source identities, receipt/reentry/held-action routes and scope/lineage/generation. It carries its own pinned provenance. Duplicate bindings are rejected.
- [gates.py](../../adapter/planner/gates.py): `governed_external_unknown` validates the exact typed correspondence, current evaluation envelope, pending lifecycle, gate qualification, actual consumer's evidence-obligation predicate and canonical source-content binding. It does not evaluate a missing positive rule or accept evidence.
- [core.py](../../adapter/planner/core.py): the unknown-rule control defect is suppressed only for the exact requirement/consumer that passes that check. Incomplete/stale gates, unknowns without bindings and unsupported required predicates retain their defects. Global precedence is unchanged.
- [codec.py](../../adapter/planner/codec.py): canonical set ordering and additive default omission preserve old snapshot encodings; all new contract provenance must be in bundle source pins. Invalidation of the contract source stales the gate and holds dependents through the existing source-invalidation path. No second persistence or planner model was added.

The contract's source body is canonical Planner JSON with schema `EXTERNAL-RESOLUTION-CONTRACT-1` and `contract` equal to all typed record fields except provenance and the outer `$type`. Set-valued producer/action lists use existing canonical ordering. Its raw content identity must equal the hash of those exact bytes, and provenance.excerpt must match them. Provenance section is `/`; its scope must agree with the gate, requirement and current context. The record cannot authenticate a positive producer merely by naming one. An unresolved concrete producer remains unavailable to receipt proof; its governed source class can describe the pending acquisition.

This binding is an admitted input premise with verified source pins, not a signature or new authority issuer. Native snapshot computations remain pure: they validate the in-memory content binding; bundle save/restore independently verifies source files. A raw checksum is not a positive trust grant. Importers must supply independently accepted acquisition contracts; this task does not implement migration or general source ingestion.

## Preserved boundaries

`EvidenceRequirement.rule_known` is never set true by this repair. `_obligation_proof`, receipt authentication/claim validation, `external_complete`, decision readiness and resume eligibility are unchanged. No evidence, accepted proof, applicability, root/slot transition or action permission is created. The currentness of a historical BLOCKED producer's independently accepted knowledge remains governed by C06.

WAITING is not RECEIVED; RECEIVED is not VALIDATED; VALIDATED is not RESUME_ALLOWED. C03 still requires current evidence, accepted native reentry lineage bound to policy/context, verified pins and named-action eligibility. Both snapshot cold reload and full source-verified bundle persistence retain false resume eligibility for the governed unknown.

Invalidating the acquisition-contract source is distinct from receiving insufficient positive evidence. The former makes the route itself stale and restores PLAN_DEFECT; the latter cannot prove the obligation and remains governed waiting while the route remains valid.

## Focused qualification

Nine permanent test methods cover:

- Governed external unknown → EXTERNAL_WAIT with no defects/actionable actions and UNKNOWN proof; roots/slots/knowledge/receipt inventories unchanged; resume=false.
- Original unbound snapshot, missing route and incomplete route → PLAN_DEFECT.
- Exact field substitutions, missing source class/request, wrong identity/domain/source pins, receipt/reentry/held-action mismatch, incompatible scope/lineage/generation and detached consumer predicate reject. A correctly hashed wrong-lineage contract also returns PLAN_DEFECT, independently of checksum validation.
- Contract/gate/requirement source invalidation after canonical reload → PLAN_DEFECT and resume=false, surviving another reload.
- Governed unknown plus factual frontier → MIXED_WAIT; independent machine work → RUNNABLE; ready independent human work → HUMAN_HANDOFF; both → RUNNABLE. Bounded internal acquisition can be runnable while its consumer remains blocked.
- A 24-combination cross-product of known/missing, governed unknown, no-route unknown, malformed route, received-invalid and validated-before-reentry states with all four independent machine/human combinations preserves global precedence.
- Illegal lifecycle shortcut rejects; unknown governing rule still fails receipt proof; invalid receipt does not create reentry; independently valid receipt uses the existing normal reentry path.
- Two external gates, branches and source contracts preserve canonical identity and complete computation under collection reversals. Hash seeds 1, 7, 101, reversed JSON object keys, independent process reloads and repeated computation preserve the result. Ungoverned unknown cold reload remains PLAN_DEFECT.

Existing seven-state tests retain their ungoverned unknown negative. Synthetic fixture sources/policy copies and persistence outputs are isolated in temporary directories. No synthetic evidence is written into E1.

## Full regression and limitations

`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s adapter/tests -p 'test_planner*.py'` completed with **158 tests PASS in 1103.175 seconds**. This covers A–N replay, X01–X11 invariants, C01–C06 corrections, refined C06, C06A budget qualification, global controls, external gates, receipt/reentry, C03 resume proof, importer, CLI, canonical persistence/replay, cold resume, determinism and constructors.

The final focused command `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest adapter.tests.test_planner_external_unknown` completed with **9 tests PASS in 7.684 seconds**. Two focused methods were added after full-suite discovery; all final methods passed in that focused run. There are **160 distinct passing tests** across the two runs, not 167 independent tests. A separate C06 run also passed all 8 tests in 336.089 seconds; those overlap the full suite. F01–F06 retain their prior closed status; F03 source invalidation remains fail-closed after reload.

The relevant minimum-state probe is the synthetic governed unknown plus an independent factual frontier; it derives MIXED_WAIT without a positive proof. This is not the real frozen-E1 migration/readiness test. CUT01–CUT05 remain independently tracked; the Planner portion of CUT04 is addressed, but actual source-to-contract mapping, other minimum-state interfaces and complete migration qualification are not established.

After accepted repair qualification, M01 contract closure may resume to consume this typed distinction; that is not M01 completion, M02 authorization or E1 resume. No M01 work is executed here. Historical reconciliation, CC01, M01 and blocked package artifacts remain unchanged.

```text
REPAIR = EXTERNAL_UNKNOWN_RULE_CONTROL_1
RESULT = PASS
PRE_REPAIR_COUNTEREXAMPLE = REPRODUCED
PRE_REPAIR_REGRESSION = FAIL_EXPECTED
POST_REPAIR_COUNTEREXAMPLE = PASS for explicitly source-bound governed premise
NEGATIVE_CONTROL = PASS
MALFORMED_ROUTE_CONTROL = PASS
WRONG_LINEAGE_CONTROL = PASS
CONTROL_STATE_MATRIX = PASS
RECEIPT_SEMANTICS = PASS
RESUME_SEMANTICS = PASS
PERSISTENCE_RELOAD = PASS
INVALIDATION = PASS
DETERMINISM = PASS (hash seeds 1/7/101, ordering, cold reload, repeated computation, full suite)
TESTS_PASSED = 158 full suite + 9 final focused (160 distinct); separate C06 8 PASS (overlapping)
E1_REPLAY_CASES = {A:PASS,B:PASS,C:PASS,D:PASS,E:PASS,F:PASS,G:PASS,H:PASS,I:PASS,J:PASS,K:PASS,L:PASS,M:PASS,N:PASS}
NEGATIVE_INVARIANTS = {X01:PASS,X02:PASS,X03:PASS,X04:PASS,X05:PASS,X06:PASS,X07:PASS,X08:PASS,X09:PASS,X10:PASS,X11:PASS}
PRIOR_CORRECTION_REGRESSIONS = {C01:PASS,C02:PASS,C03:PASS,C04:PASS,C05:PASS,C06:PASS,C06_REFINED:PASS,C06A_BUDGET:PASS}
F03_STATUS = CLOSED
PLANNER_CONTROL_DEFECT = CLOSED
FROZEN_MINIMUM_STATE_IMPACT = relevant synthetic control probe corrected; full E1 not restored
M01_CLOSURE_REENTRY_ALLOWED = YES
M02_READY = NO
V0_1_CURRENT_STATUS = CORRECTION_REQUIRED
REAL_E1_EVIDENCE_CREATED = NO
E1_ARTIFACTS_MODIFIED = 0
DEFERRED_SCOPE_VIOLATIONS = 0
PRODUCTION_EFFECT = NO
```

Post-regression SHA-256 comparison against the pre-repair inventory verified all **10,911 E1 files byte-for-byte unchanged**, all 150 pre-existing planning artifacts unchanged, and both protected backlog artifacts unchanged. The two pinned reconciliation identities also match. `git diff --check` and explicit changed-source/new-artifact whitespace checks pass. Existing untracked repository work is preserved; only the four runtime files, one new regression file and this new result artifact belong to this repair.
