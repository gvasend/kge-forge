# PROOF-P01 — A11 contract recovery and unresolved boundary

RESULT = BLOCKED. No runtime, installation or lifecycle operation was performed.

The requested proof-only A11 cannot be sealed as the canonical A11 contract while the original plan and acceptance matrix remain authoritative. Matrix E2-A11 requires `DEPENDENT_ACTION_REENTRY` and C03 `resume_eligibility`; its exit makes only the named Action eligible. E2-A12 starts with that eligibility and owns actual selection/result execution. Requiring reentry eligibility to remain false after A11 contradicts both boundaries. V01 explicitly records this distinction; V02 preserves it. This is a contract conflict, not an established runtime defect.

Authoritative recovery:

- [DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_ACCEPTANCE_MATRIX_1.md:145](DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_ACCEPTANCE_MATRIX_1.md) — lines 145–157.
- [DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_ACCEPTANCE_MATRIX_1.md:159](DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_ACCEPTANCE_MATRIX_1.md) — lines 159–171.
- [DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_EXPERIMENT_1.md:30](DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_EXPERIMENT_1.md) — lines 30–49.
- [DETERMINISTIC_PLANNER_V0_1_VALIDATION_V01_A10_CONTRACT.md:9](DETERMINISTIC_PLANNER_V0_1_VALIDATION_V01_A10_CONTRACT.md) — lines 9–11.
- [DETERMINISTIC_PLANNER_V0_1_VALIDATION_V02_RESULT.md:7](DETERMINISTIC_PLANNER_V0_1_VALIDATION_V02_RESULT.md) — lines 7–7.
- [DETERMINISTIC_PLANNER_V0_1_VALIDATION_V02_RESULT.md:41](DETERMINISTIC_PLANNER_V0_1_VALIDATION_V02_RESULT.md) — lines 41–41.

Canonical A11 starts from validated Evidence with current prerequisites and exact policy/context lineage, independently checks C03 pins/currentness/other gates, and establishes named eligibility only. It does not complete REENTER. A12 owns actual REENTER execution and accepted knowledge. The original artifacts do not define a separately persisted A11 Evidence-proof proposition, its entailment rule, operating proof authority or proof-only control oracle. These cannot be inferred from a requested `PROVED` label.

V02 records accepted validation/support and allows native obligation queries to derive PROVED. That derived query is distinct from a persisted Proof instance. E04's helper ProofResult is not the complete persisted installation/event contract requested here. E06 supplies typed SLOT_PROOF and ROOT_PROOF with Knowledge/Slot supports; their targets cannot substitute for Evidence, ValidationResult and support identity domains.

The exact post-A10-install bundle was loaded using native `codec.restore`, checking canonical bundle bytes, pinned sources and immutable event sidecars. Bundle `1b69d962865c23fa43b3ec362af096e39d72bbfc4dee2252d1e0d4914d487054`, state `94adb7403d30b7843124c823e0304b4a0b1a38b49b602fa9db75d09a2729ecab`, append head `c3f48f66c77527c886fe483868deedd101bccfd69000385732a9b545fd07ea24` remain unchanged. V02's readiness evidence is retained; this read does not execute its private A09/A10 simulations.

## Proposed proof capability, pending canonical reconciliation

The companion defines a candidate schema only. It is neither an authorized P04 definition set nor a complete implementable canonical contract. A typed proposition must name subject, predicate, typed expected value, scope/lineage and currentness. The independent rule that validated Evidence entails that proposition is missing; generic TRUE is prohibited. Whether it supports the C03 conjunction or replaces a phase transition requires explicit resolution.

The proof contract separately binds semantic Evidence ID, native Evidence entity ID, content ID, receipt ID, ValidationResult ID, support instance ID and source pin ID. It also binds proof type/proposition/target, validation/support/source/operating-authority requirements, generation and provenance. No instance exists prospectively. A future deterministic instance identity must hash these complete typed bindings and admitted outcome in its own identity domain.

A future transaction would consume actual admitted receipt/Evidence, accepted ValidationResult, current support, installed definitions, independently checked entailment witness and exact command/pre-state/parent. It would atomically publish Proof, ordinary-parent proof event and native post-state bundle. It must reject caller-supplied proved flags. Receipt/validation/support remain distinct records. Proof-only admission would leave reentry, Action completion, root/slot proof instances and FINISH completion unchanged; this proposed boundary is precisely the unresolved canonical conflict. Rejection must produce no successful proof admission or head advancement; any durable rejection-record policy must be separately specified.

Currentness must verify installed proposition/contract and all live input/source/authority/context bindings. Dependency invalidation withdraws usability, preserves immutable historical records and triggers only bounded native recomputation. Atomic commit leaves no reachable partial Proof/event/head; identical command retries preserve semantic identity and conflicting retries fail closed. Cold restore must preserve exact typed links and ancestry. Replay reproduces historical admission without making a new proof decision.

Prospective proposition, proof contract and transaction/event definitions require a typed adapter to native proof consumers. The adapter installs definitions only. A coherent definition set must publish without dangling references, ordered proposition → proof contract → transaction definition. INSTALL/REPLACE/SUPERSEDE is not assigned until exact existing logical roles are compared. Proof instances are not installable definitions. Prior route, ATTEST and A10 grants do not cover this set.

Security negatives are fully enumerated in the companion, including absent/rejected/invalidated validation, absent/wrong support, all Evidence/content/receipt/proposition/source/context substitutions, generic TRUE, stale definitions, wrong parent, conflicting retries, premature reentry/Action completion, prospective instances and metadata-wrapper substitution. They are a proposed qualification plan, not executed PASS evidence.

## Decisions and missing terms

Two boundary resolutions are recorded without selection: retain original named-reentry A11 and qualify C03; or explicitly authorize an A11/A12 acceptance-boundary revision with complete proposition, authority and new oracles. The latter needs qualification-scope authority distinct from ordinary INSTALL permission. No acceptance change is applied here.

The requested installation options remain `AUTHORIZE_P04_A11_PROOF_INSTALLATION` and `DECLINE_P04_A11_PROOF_INSTALLATION`. Authorization is not decision-ready: exact definition/content IDs, entailment/source/operating-authority rules, phase boundary and control oracle must first be sealed. A later bounded INSTALL grant must bind exact set/content/operation, current bundle/state/parent, scope/lineage/generation/consumer, issuer, validity and provenance. It cannot authorize proof execution or change qualification scope. Declining leaves canonical state and readiness unchanged.

P04_A11_PROPOSITION_ID = UNASSIGNED_PENDING_CANONICAL_BOUNDARY_AND_PROPOSITION_DECISION

P04_A11_PROOF_CONTRACT_ID = UNASSIGNED_PENDING_CANONICAL_BOUNDARY_AND_PROPOSITION_DECISION

P04_A11_TRANSACTION_DEFINITION_ID = UNASSIGNED_PENDING_CANONICAL_BOUNDARY_AND_PROPOSITION_DECISION

Scope/lineage/generation remain E2-QUALIFICATION-ONLY / E2-P03-PROSPECTIVE-QUALIFICATION-1 / E2-P03-PROSPECTIVE-GENERATION-1. No hash is presented as an authoritative definition identity for an incomplete contract.

A11_IMPLEMENTATION_READY = NO. P04_A11_INSTALLATION_DECISION_REQUIRED = YES. P04_A11_INSTALLATION_DECISION_READY = NO. A09_READY = YES; A10_READY = YES; A11_READY = NO; P04_EXECUTION_READY = NO.

A09/A10/A11_EXECUTED = NO; PROOF_INSTANCE_CREATED = NO; RUNTIME_MODIFIED = NO; P03_RESULT = PASS; historical correspondence = UNPROVEN; N_REAL_SATISFIED = NO; E1_ARTIFACTS_MODIFIED = 0; PRODUCTION_EFFECT = NO. No option was selected. Prior V02's 52 tests and 84 fresh-reader checks are cited as existing evidence, not new P01 runs. Broad-suite status remains separate.

Preservation hashes and `git diff --check` are recorded in the [machine-readable companion](DETERMINISTIC_PLANNER_V0_1_PROOF_P01_A11_CONTRACT.json).
