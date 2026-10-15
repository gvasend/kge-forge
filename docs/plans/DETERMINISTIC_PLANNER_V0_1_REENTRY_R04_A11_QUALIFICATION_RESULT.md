# REENTRY-R04 — native A11 positive qualification

RESULT = PARTIAL. Required post-event unordered presentation equality fails. A11_READY = NO. P04_EXECUTION_READY = NO.

The exact post-A10-definition-install P04 bundle was restored with native trust/source/event-sidecar checks. E07 A09 precommit and V02 A10 preparation created an isolated event-bearing qualification lineage without committing canonical P04. Actual authenticated Evidence/receipt and accepted ValidationResult/support produced the expected typed obligation Proof(PROVED, reasons=()). No Proof instance or permission was persisted.

Proof alone left C03 ineligible before accepted reentry. The native DEPENDENT_ACTION_REENTRY event reopened exactly E2-REENTER, but C03 still reported DECISION_REENTRY_REQUIRED: the current E2-DECIDE route also needed its separate native DecisionReentry. That event was admitted only in isolation. With both native routes current, C03 returned allowed=true for E2-REENTER alone, no reasons, exact event/pre-state/policy/source support. Native recomputation selected E2-REENTER. Neither transition executed it.

External reentry event = `57c8db886a64e0636d96e808f5afffc90fee04d8550bb0989cd7535dc8849af8`.

Complete isolated bundle = `6b1e2cec5c5163552d496e5b682fe72652c297cfa22b75ee9c538931ade767e0`; state = `d35dc4fe85c0a343aefda8d177742d3379d7fb1d7b05573ec14c506b81401d64`; append head = `7f8969c9aa4bf1af92cfd1f0d5c1f0f2f9dc9cf86696d36305adba85d4c1ec1f`.

## Oracles and authority separation

Independent assertions require accepted/current receipt and validation/support, exact E2-EXTERNAL-REQUIREMENT/proposition/native Evidence bindings, Proof PROVED, pre-event C03 false, exact current parent/pre-state/gate/named set and all source/context pins. After the two required native reentry events, only E2-REENTER is actionable/selected; completed Action set, knowledge and stored root/slot state remain unchanged; no typed root/slot proofs, supplied ActionResult or FINISH result appears. This passes the A12 initial oracle without executing A12.

The canonical Action.authority field is None. No nonexistent standalone Action grant was invented. Current authenticated receipt and recorded-choice DECIDE governance remain independent prerequisites. The initial development sweep incorrectly expected withdrawing unrelated E2-GRANT USE source to remove eligibility. The corrected oracle requires that unrelated withdrawal preserve eligibility, while applicable Evidence/validation/support/gate/DECIDE/ATTEST source withdrawals remove eligibility or fail closed at model admission. Runtime was not changed. Full case outcomes and any qualification limitation are recorded in the companion.

## Negatives, retries and invalidation

28 negative controls passed. They cover absent or substituted receipt/Evidence/validation/support, wrong gate/proposition/named route/context/provenance, malformed or stale event envelopes, wrong required authority, unsupported execution/result payload, caller eligibility/Proof operands and persisted Boolean substitution. These tests use isolated malformed candidates/projections; they do not fabricate accepted history or weaken admission. Context changes have no new native event invented here.

Identical accepted ExecutionEvent resubmission is a semantic no-op with unchanged history/bundle. Conflicting bytes under that identity and fresh stale-parent/pre-state retries fail closed. Retry against the unchanged isolated parent after a noncommitting negative reproduces the original event. A newly submitted ExternalEvent after success is stale; it cannot duplicate the transition. This qualifies the exact native retry behavior, not a nonexistent ExternalEvent command-key transaction.

Native SourceInvalidation tests retain the accepted reentry event prefix for audit while recomputing current C03. Historical event presence does not become durable permission. Invalidation acceptance = PASS; the companion distinguishes successful ineligibility recomputation, unrelated controls and any model-admission failure rather than collapsing them.

## Persistence, replay and determinism

Four native isolated checkpoints were emitted: post-A09, post-A10, post-external-reentry and post-complete-A11. Their role is ISOLATED_QUALIFICATION, not canonical P04 lifecycle output or historical reconstruction. Immutable event sidecars accompany each bundle. The writer exited before 12 independent cold readers (three each for seeds 0,1,7,101). Native restore/replay preserved exact event history, ledger/head, state/bundle identities and source/policy pins; freshly computed Proof, ResumeEligibility and full Computation matched.

Four independent complete reproductions from the same sealed canonical start matched exactly, including reversed pre-execution unordered collections. However reversing the post-event ValidationResult input_identities set fails model admission even though canonical snapshot and bundle bytes are identical. Native validation_transaction.validate_records compares the unordered result inputs positionally against ordered ValidationInstance.inputs. The exact minimal counterexample is preserved in ordering-counterexample.json; this mandatory determinism dimension is FAIL. Ordered causal history was not permuted. No runtime repair was applied in this existing-path qualification. No validator was rerun as a new decision during historical replay. Derived eligibility is serialized only in comparison evidence, never as a canonical field, event or authority.

## Canonical readiness and preservation

No missing A11 prospective definition set was found. Existing requirement/gate/named reentry/C03 plus current installed A09/A10 definitions support the native path. No installation or new authority occurred. A11 definition readiness = YES; native-path qualification = PARTIAL.

A11_READY remains NO because the required post-event ordering dimension failed. The next package is a bounded correction/qualification of validation projection set consistency; it must preserve all source/context/identity checks. A12 also remains unready: canonical E2-REENTER accepted_inventory is empty, and its prospectively declared PASS + E2-K-REENTER result needs its own legitimate typed Action replacement/materialization and bounded authority. A13 root/slot and FINISH contracts remain separate. A11 eligibility does not supply a result inventory or execute the Action.

Canonical A09_EXECUTED = NO; A10_EXECUTED = NO; A11_EVENT_ADMITTED = NO; A12_EXECUTED = NO. Canonical P04 bundle and all prior input/runtime/E1 hashes remain unchanged. A09_READY = YES; A10_READY = YES; A11_READY = NO; P04_EXECUTION_READY = NO. P03_RESULT = PASS; historical correspondence = UNPROVEN; N_REAL_SATISFIED = NO; E1_ARTIFACTS_MODIFIED = 0; PRODUCTION_EFFECT = NO; git diff --check = PASS.

The [machine-readable result](DETERMINISTIC_PLANNER_V0_1_REENTRY_R04_A11_QUALIFICATION_RESULT.json) and [qualification inventory](qualification/REENTRY_R04_1/checkpoint-inventory.json) include exact traces, inputs, per-case oracles, comparison results and preservation evidence. Reproduce the ordering defect with `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 adapter/tests/qualify_reentry_r04.py ordering_counterexample`; reproduce the normal positive path with `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 adapter/tests/qualify_reentry_r04.py reproduce normal`; native reader mode recomputes from the emitted isolated bundle. No broad-suite PASS claim is made by this focused qualification.
