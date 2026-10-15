# Evidence E07 — atomic E02 ingress transaction integration

WORK_PACKAGE = EVIDENCE-E07  
RESULT = PARTIAL

Generic E02 ingress integration passes. The ordinary atomic Evidence transaction now consumes the same typed attestation that preflight validates. The exact post-I04 P04 execution-level precommit check proceeds through authentication and stops at **RECEIPT_CHANGED_CONTROL**. A09 remains uncommitted; A09 readiness and full P04 execution readiness are NO.

## Authority and scope

This package uses the unchanged [E02 contract](DETERMINISTIC_PLANNER_V0_1_EVIDENCE_E02_ATTESTATION_RESULT.md), [T01-D precedent](DETERMINISTIC_PLANNER_V0_1_E2_P03_T01_D_LIVE_ADMISSION_RESULT.md), [I03](DETERMINISTIC_PLANNER_V0_1_INSTALLATION_I03_ATTEST_INGRESS_CONTRACT.md), [I04](DETERMINISTIC_PLANNER_V0_1_INSTALLATION_I04_RESULT.md), and the canonical [plan](DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_EXPERIMENT_1.md) / [acceptance matrix](DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_ACCEPTANCE_MATRIX_1.md). Generic committed fixtures use TEST/scope and TEST/lineage. Canonical P04 receives only non-mutating precommit evaluation. No additional INSTALL, ATTEST issuance or lifecycle authority was applied to P04.

## Interface gap and operand contract

Previously `evidence.apply(snapshot, request, evidence_attestation=instance)` accepted the typed E02 instance, while `codec.admit_external_evidence(bundle, request, source_bytes, output_dir, repo_root)` called `_extend_private -> core.apply_event -> evidence.apply` without that instance.

`EvidenceSourceAdmission.attestation_operand` now optionally carries an `EvidenceAttestationOperand`: the unchanged typed E02 attestation, its typed E01 `SemanticNativeBinding`, and the exact expected bundle, snapshot and parent event. The classes reside in the native model's closed codec registry; their existing E02/E01 identities and binding semantics remain unchanged. Absent operands omit their default from canonical encoding, preserving earlier bundle/command identities.

The live transaction additionally requires `expected_binding`, an independent trusted E01 expectation selected and sealed by the boundary owner. It must not be inferred from the submitted operand. P04's expectation is independently checked against the previously qualified semantic payload/content formulas and sealed before preflight. A boolean authentication flag is never accepted. Installed ATTEST authority, attestor, source predicate, ingress contract and exact provenance remain independently validated.

The command key seals the full operand and its source, semantic/native Evidence, content, proposition, provenance, scope/lineage and pre-state bindings. Substituting an instance, including one with a correctly recomputed malicious E02 identity, fails. Changing both the submitted instance and embedded binding still fails against the independent expectation. A candidate cannot cross a canonical parent-state change unnoticed.

## Atomic transaction and replay

`codec.preflight_external_evidence` is the same private projection used by execution after its locked trusted-HEAD check:

1. Replay/verify the trusted bundle, current parent and raw source pins; compare the sealed E01 expectation.
2. Validate the typed E02 operand, installed authentication definitions/currentness, and complete native admission.
3. Privately derive admitted Evidence and its authentication association, ingress event, EVIDENCE_RECEIVED receipt and receipt event.
4. Replay that complete proposed bundle and enforce the existing full-Computation guard.
5. Publish immutable source/bundle/event files and atomically replace HEAD only after all checks pass.

The full historical attestation witness is persisted inside the committed ingress event; `ReceiptAdmission.attestation` associates its exact identity with the admitted Evidence. Before semantic commit, no canonical Evidence/attestation/receipt is published. Interrupted immutable-file publication can leave orphan files, which do not constitute a trusted published canonical head. Every reachable committed bundle contains the complete transaction, never a partial admission.

Replay verifies the historical typed witness, hashes, bindings and original authority/pre-state. It never calls `ea.materialize` to create another attestation decision. Tests and fresh readers patch that function to raise if invoked. The pre-ingress prefix remains free of Evidence/attestation/receipt. Exact retries produce no additional semantic objects/events; altered attestation content under the same command fails closed.

## Generic qualification

All six new E07 tests pass. They cover execution/preflight equivalence, the [negative suite](qualification/EVIDENCE_E07_1/generic-tests.log), three independent envelope-state negatives, stale complete commands, exact retry/conflict, four failure-injection boundaries, cold restore, historical replay and independent deterministic execution.

The archived [generic qualification](qualification/EVIDENCE_E07_1/generic-qualification.json) identifies its native committed bundle and isolated source root. Four independent readers after writer exit pass **72 comparisons**, across hash seeds 0, 1, 7 and 101. Another four fresh readers run within the unit persistence test. Do not treat these isolated TEST-lineage transactions as canonical A09 execution.

## Exact P04 precommit and remaining blocker

The unchanged I04 bundle is pinned to:

- Bundle: `fa86ce94d76651ce5eccfa76c2d862243548d6d8dcaae91e74dca4e9c571c7d1`
- State: `c5c85434ddfb69be7f327e9e8fd72d2c7270505cf4908ea4fd9b4918075c1591`
- Parent/append head: `549e41859f55cd3414d91b5ce97f023ab9e150f55ed01ae81a9a9dc5ef2f362c`

The fresh typed operand is constructed in memory against this exact head. Bundle, parent, route, source/policy, scope/lineage, four-record dependency provenance, reference contract, typed E01/E02 binding and authentication pass. No new transient attestation body or candidate operand is persisted for canonical P04. The [precommit result](qualification/EVIDENCE_E07_1/p04-execution-preflight.json) records identities/check outcomes only; its private projection is discarded.

The unchanged strict transaction guard rejects complete Computation inequality. The [counterexample](qualification/EVIDENCE_E07_1/p04-control-counterexample.json) shows only the `blocked` diagnostic tuple differs:

| Action | Before | Private post-receipt computation |
|---|---|---|
| E2-FINISH | ACTION_COMPLETED:E2-REENTER | PRIOR_ATTEMPT_HOLD:BLOCKED |
| E2-REENTER | DECISION_REENTRY_REQUIRED; EXTERNAL_GATE:E2-GATE; PREDICATE:E2-PROOF:UNKNOWN | PRIOR_ATTEMPT_HOLD:BLOCKED |

Control remains EXTERNAL_WAIT and the actionable set remains empty. `evidence.apply` publishes derived blocked statuses; native recomputation then takes `core.recompute`'s cached prior-attempt hold branch. This diagnostic discrepancy also reproduces with the exact pre-E07 runtime. E07 does not relax the guard or alter cached Action/control semantics to claim readiness.

NEXT_PACKAGE = P04-A09-RECEIPT-CONTROL-INVARIANT-CLOSURE.

A10 validation, A11 evidence proof/exact reentry, A12 REENTER result inventory and A13 root/slot/finishing-result definitions remain offline, with typed installation support and bounded authority required. Canonical A11 owns named reentry; A13 owns root/slot proof and selected finishing-result work. No later stage was reassigned or installed here. Prospective configuration may occur only under its applicable installation contract before use; it never retroactively changes P03. Any further canonical installation stales an uncommitted A09 candidate. Full P04 readiness also requires the continuation package's complete prospective contract/inventory/oracle checks.

## Regressions and preservation

- **46 affected tests PASS:** six E07 and 40 installation/authentication, T01, E01-E06, G01-G04, external-unknown and root/slot regressions.
- Expanded replay/resume: **72 PASS, 1 pre-existing failure**. `P04ReplayTests.test_x05_all_nine_checks_required_not_majority_vote` reproduces under the exact pre-E07 hashes of all six changed runtime files. See the [baseline reproduction](qualification/EVIDENCE_E07_1/baseline-dossier-test.log).
- Legacy Evidence admission: **4 PASS, 4 FAIL, 12 ERROR**, the exact failing test set previously recorded before I04. See the [comparison](qualification/EVIDENCE_E07_1/legacy-comparison.json).
- The known frozen-E1 duplicate-import broad-suite collection blocker is preserved separately. A fresh pytest collection attempt could not run because the system Python lacks pytest. No full-suite PASS is claimed.

The [preservation check](qualification/EVIDENCE_E07_1/preservation.json) compares 10,967 frozen E1 files and prior qualification records: zero modifications. Core/gates remain byte-identical to the pre-E07 workspace. `git diff --check` passes. P03 PASS, historical correspondence UNPROVEN and N-REAL NO remain unchanged. A09-A13 and E2-FINISH were not executed. Production effect is NO.

## Report

```text
WORK_PACKAGE = EVIDENCE-E07
RESULT = PARTIAL
TRANSACTION_INTERFACE_GAP = CLOSED
E02_OPERAND_CONTRACT = PASS
PREFLIGHT_EXECUTION_EQUIVALENCE = PASS
EVIDENCE_BINDING = PASS
PRE_STATE_BINDING = PASS
ATOMICITY = PASS
IDEMPOTENCE = PASS
TRANSIENT_BOUNDARY = PASS
SECURITY_NEGATIVES = PASS
PERSISTENCE = PASS
COLD_RESTORE = PASS
REPLAY = PASS
DETERMINISM = PASS
REGRESSIONS = AFFECTED_46_PASS; PREEXISTING_FAILURES_SEPARATE
E02_INGRESS_INTEGRATION = PASS
P04_A09_EXECUTION_PREFLIGHT = FAIL: RECEIPT_CHANGED_CONTROL
A09_READY = NO
P04_EXECUTION_READY = NO
E2_P04_READY = NO
NEXT_PACKAGE = P04-A09-RECEIPT-CONTROL-INVARIANT-CLOSURE
A09_A13_EXECUTED = NO
P03_RESULT = PASS
P03_HISTORICAL_CORRESPONDENCE = UNPROVEN
N_REAL_SATISFIED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
```

The [machine-readable companion](DETERMINISTIC_PLANNER_V0_1_EVIDENCE_E07_INGRESS_INTEGRATION_RESULT.json) contains the operand schema, ordering, qualification/negatives, archived native identities, fresh-reader results, exact live counterexample and dependency-ordered readiness result.
