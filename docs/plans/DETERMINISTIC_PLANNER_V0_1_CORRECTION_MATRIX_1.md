# Deterministic Planner v0.1 — Correction Matrix 1

Planning specification only. Companion to [Correction Plan 1](DETERMINISTIC_PLANNER_V0_1_CORRECTION_PLAN_1.md). Source findings are the unchanged [adversarial review](DETERMINISTIC_PLANNER_V0_1_ADVERSARIAL_REVIEW.md); the original [qualification](DETERMINISTIC_PLANNER_V0_1_QUALIFICATION.md) remains historical. No finding is closed by writing this matrix, and none of the tests below is claimed to have been implemented or passed by this task.

## 1. Finding normalization and package ownership

Code paths are repository-relative. Requirements and cases retain the review's meanings; additional regression obligations are labeled separately.

| Finding / severity | Exact defect and affected code/types | Requirements / replay / invariants | Concrete review counterexample and consequence | Review's minimum correction / owner |
|---|---|---|---|---|
| F01 / MAJOR | `core.project` skips STALE assertions; `evaluate_satisfaction` then enforces only surviving REQUIRES edges. `codec.invalidate_sources` does not necessarily invalidate ordering dependents. GraphAssertion, RootCondition, ValueSlot and prerequisite consumers affected. | R16/R20; C/N; X02/X10 | Child otherwise proved, unresolved parent required through an edge with independent provenance. Invalidating only that edge's source changes child UNRESOLVED to SATISFIED. A downstream action can become eligible without the old prerequisite. | Preserve stale ordering as an unavailable obligation or stale/block dependents transitively; add root/slot/downstream counterexamples. **C02**; C01 supplies validated references. |
| F02 / MAJOR | `replay.plan_output` derives resume eligibility from any gate's DEPENDENT_ACTION_REENTRY stage alone. ExternalGate's historical phase is confused with a current proof; gates/core themselves reject stale evidence. | R08/R10/R15/R20; J/N; X01/X04/X10 | After accepted complete synthetic receipt and reentry, invalidate the independent attestor. `external_complete=false`, ACTIONABLE empty, EXTERNAL_WAIT, but `resume_allowed=true`. Misleading control-transfer permission. | Derive eligibility from current proof and actual named reentry actionability, including other applicable gates; test stale/conflicting/blocked reentry. **C03**. |
| F03 / MAJOR | `replay.import_e1` loads reduced M normalization and appends original graph/ledger/manifest records as opaque assertions. `Snapshot` lacks restored Decision/GraphEntity/action contract semantics; persistence faithfully stores omissions. | R01/R04/R07/R15/R17/R18/R20/R22; M/full N; regression X01–X11, particularly X03/X04/X05/X07/X08/X10/X11 | Decoded M has 63 actions, zero decisions/entities, zero action requirement/authority predicates and all accepted_result defaults PASS. After a hold is released, original bounded source/authority/result requirements are absent; human routes lack objects. Current frozen wait reproduction does not prove future contract correctness. | Restore typed action, decision/dossier, authority/evidence and reentry contracts from a reviewed mapping; explicit unsupported-rule holds, no empty/default PASS substitutes; test a supplied result after isolated reentry. **C06**. |
| F04 / MAJOR | `model.validate_p03` checks references to predicates/operands but incompletely checks Predicate entity/other/action/condition/knowledge targets and kind-specific structure. `codec.decode_snapshot` admits them. | R16/R18/R20; P06 importer; malformed reference/identity tests; regression X05/X06/X08/X10/X11 | SOURCE_IDENTITY names absent EntityId and survives encode/decode. A self-ALL cycle survives admission and evaluates UNKNOWN. Invalid input accepted as structurally validated; these probes did not themselves grant authority. | Validate kind-specific target domains and declared future outputs before use; explicitly decide/enforce forbidden proof-cycle rules. **C01**. |
| F05 / MINOR | `core._global_control` sorts goals by bare target.value; typed IDs of different domains may have equal spellings. Branch tuple/witness ordering is not fully canonical. | R02/R12/R15/R22; D/M/N; added typed-output permutation regression alongside X11 | Equal canonical snapshot bytes with ConditionId('same') and SlotId('same'), reversed goal order, produce different branch tuples. Scalar control and selected action were not shown to change. | Consistent total typed ordering and unambiguous typed witnesses; cross-domain permutation tests. **C04 — FIX_BEFORE_REQUALIFICATION**. |
| F06 / MINOR | `replay.import_fixture` accepts an arbitrary valid policy pin while executing a hard-coded policy version; `codec._replay` allowlists versions without binding them to policy content. `selector` executes its fixed map. | R02/R15/R20; D/N and policy provenance; regression X10/X11 | Replace B's policy pin with its correctly hashed Candidate-3 authority pin. Import succeeds. This misbinds audit policy identity; the probe did not alter the fixed selector. | Bind supported policy/version to its admitted policy identity/canonical contract; reject unrelated hashes. **C05 — FIX_BEFORE_REQUALIFICATION**. |

F01/F02 are confirmed fail-open enforcement/reporting paths. F04 is an invalid-input admission defect even where evaluation later remains UNKNOWN. F03 is a semantic restoration gap, not proof that its current MIXED_WAIT scalar is wrong. These distinctions are preserved rather than inflating every finding into the same failure class.

## 2. Required adversarial red/green tests

Each test must be independently specified before repair. Record the pre-correction failure against the reviewed revision in an isolated checkout/copy if needed; do not alter frozen sources or the historical result records. A corrected diagnostic/hold satisfies a rejection oracle; crashing after use, dropping the offending relation or selecting another action by preference does not.

| Test / package | GIVEN | WHEN | THEN / AND MUST NOT | Independent oracle and red condition |
|---|---|---|---|---|
| T01 / C02 | Two unresolved roots; explicit child REQUIRES parent; child has otherwise accepted proof from another source | Call actual `invalidate_sources` on ordering provenance, then project/recompute; canonical round-trip and repeat | Child remains unproved/stale/blocked; original obligation remains represented; its downstream action, slot and decision cannot become ready; unaffected branch may run | Parent is still unproved and no accepted change removed its requirement. Reviewed code instead satisfies child. Do not mock projection or invalidation. |
| T02 / C03 | K-derived isolated state with complete independently attested evidence and accepted reentry transition | Invalidate independent attestor, recompute API/CLI resume and restore in a new process | `RESUME_ALLOWED=false`, no eligible route from that evidence; lifecycle history retained; no root/slot change | Current receipt authentication is false and ACTIONABLE lacks a valid named reentry. Reviewed output instead returns true. |
| T03 / C06 | Actual manifest source contracts plus independently enumerated required operational fields; separate supported synthetic variation | Import into typed state; isolate an accepted evidence/reentry attempt and supply a bounded result in replay | Restored requirements, output contract, authority and decision gates are actually enforced; empty/default PASS and missing proof rejected; valid bounded supplied result accepted without effects | Source contract for FACT-BUDGET-APPLICABILITY requires a complete proof matrix; default empty inventory is not its acceptance contract. Dossier/authority checks are independently compared to source fields, not importer output. Reviewed M lacks those operational objects. |
| T04 / C01 | Otherwise valid snapshot with a declared SOURCE_IDENTITY entity target absent from entities | Direct validation, structured import, snapshot decode and native restore | Reject before planner use with exact target/domain diagnostic | Named target does not exist. Reviewed decode accepts it. Do not replace the target with an invented placeholder. |
| T05 / C04 | Root and slot with equal spelling but distinct typed IDs; goals/witnesses refer to both | Enumerate goal/reference orders; encode/decode, recompute and compare outputs | Complete Computation and canonical output identical; type-preserving distinct witnesses | Canonical input identity is equal; reviewed branch tuple depends on input order. Do not assert only scalar control or ActionId. |
| T06 / C05 | Valid B-style input with valid construction-authority raw pin | Substitute that pin only into policy field and import/restore/select | Reject policy/version/contract mismatch before using selector | Artifact is an authority record, not the supported policy. Correct file hashing is insufficient. Reviewed import accepts it. |

### Expanded negative and positive controls

| Family | Required variants | Acceptance boundary |
|---|---|---|
| T-REFERENCE / C01 | Missing entity, other, action, condition, obligation and knowledge targets; unknown kind and unknown predicate ID; wrong typed ID/domain; duplicate ID with identical or conflicting definitions; conflicting source/identity binding; irrelevant/forbidden fields; malformed cycle | Malformed declarations rejected. Explicit unavailable bindings remain valid blocked data. Future outputs require declared bounded producer/output contracts and confer no evidence until accepted. |
| T-STALE / C02 | Stale ordering after initial root/slot/action qualification; chains and diamonds; accepted action's output subsequently stale; stale dossier dependency; stale authority/proof source; no alternate valid support; legitimate independent alternative; mixed independent branch | No stale support used for current conclusions. Historical result remains immutable. Legitimate explicit alternatives evaluated under contract, mandatory edges never silently dropped. Requalified new evidence must have its own accepted binding. |
| T-RESUME / C03 | Phase only; waiting gate only; bytes only; reentry action only; saved true flag; stale/conflicting/partial/negative/unrelated proof; missing currentness; missing original prerequisite; multiple gates; completed/held reentry action; changed target/policy | False unless full shared predicate passes. Positive accepted evidence permits only its eligible named route in an isolated state. Snapshot reload and CLI agree with core. |
| T-ORDER / C04 | Equal-spelling typed IDs; all set-valued collection orders; dictionary-key reversal; imported-reference ordering; filesystem enumeration variation; predicate operand order where semantically set-valued; different process seeds | Complete output/identity equality for identical semantics. Ordered event/history arrays stay causal; invalid reorder rejected. No new filesystem/time/random source of identity. |
| T-POLICY / C05 | Correct supported policy; exact supported extension; unrelated valid bytes; policy/version mismatch; changed priority map/tie-break/effect rule; unsupported extension; stale policy | Supported selection rules retain D; mismatches fail closed and never silently relabel or repin policy. |
| T-IMPORT / C06 | Per-field contract coverage and identity checks; unknown required fields; missing dossier or accepted decision binding; non-PASS accepted knowledge prerequisite; stale authority; divergent history/current overlay; missing producer; unsupported necessary rule; alpha-renamed supported synthetic contracts | Every planner-relevant rule is operative or explicitly blocked. Opaque retention alone insufficient. No historical report status used as a permission or final satisfaction oracle. |
| N-REAL / C06–C07 | Actual frozen manifest/checkpoint/handoff and pinned sources in fresh process, no M snapshot or prior objects | Typed contract import and independent computation match source-derived frozen oracle; no E1 action is run; new isolated bundle cold-restores identical semantic state. Synthetic continuation tests are separate. |

## 3. State and persistence requirements exercised by correction

| Dimension | Must persist or reconstruct with provenance | Must not infer |
|---|---|---|
| Action definition | Operation/stage/effect/scope; structural, knowledge, authority and external requirements; per-outcome bounded acceptance; declared outputs and reentry routes | Empty requirement list or PASS as universal defaults |
| Historical attempt | Exact result/evidence identity, accepted knowledge, original blockers, transition lineage | Current output validity merely from COMPLETED |
| Root/slot | Independent satisfaction criteria, value/identity types, mandatory producer/source/mapping/authority/consumer links, current proof validity, baseline resolution scope | Resolution from scheduling, authority grant, PASS, edge disappearance or placeholder |
| Decision | Required facts, complete dossier/identity, all checklist proofs, readiness versus stage, recorded scoped choice and authority, explicit downstream route | AUTHORITY_REQUIRED as DECISION_READY or absence of facts as an Architect alternative |
| External receipt | Contract/target/producer identity, admitted bytes, independent authentication and competence, exact obligations/currentness, accepted observation/transition | Evidence presence/identity as applicability or publication |
| Resume | All inputs to section 5's proof, current original-action gates, qualified policy, scope/lineage and accepted reentry lineage | True from previous phase, saved flag, old process memory or unrelated runnable work |
| Global control | Full-run required goal inventory, current branch routes, typed witnesses and explicit partial/full scope | Whole-run success from a partial goal projection |
| Policy | Supported canonical identity, rule version, static map and extensions bound together | Any correctly hashed record as a policy |

Historical stale objects remain admissible **as history**; attempts to use them as accepted current proof must fail before scheduling or propagation. C01's referential integrity is not an excuse for C02 to delete unavailable ordering obligations.

## 4. Package dependencies, regressions and release evidence

| Package | Prerequisites | Primary regression cases | Invariants / additional counterexamples | Unlocks |
|---|---|---|---|---|
| C01 | Existing code/review; status 1 recorded at implementation start | B/C/F/H/J/N, structural codec tests | X02/X05/X06/X08/X10/X11; T04/T-REFERENCE | C02 |
| C02 | C01 | C/E/F/I/L/M/N | X02/X07/X10; retain authority/decision controls; T01/T-STALE | C03 |
| C03 | C01/C02 | J/K/L/M/N | X01/X03/X04/X07/X08/X10/X11; T02/T-RESUME | C06 when other prerequisites accepted |
| C04 | None beyond baseline review/preservation | D/I/L/M/N | X02/X11 retained; T05/T-ORDER | C06 |
| C05 | None beyond baseline review/preservation | D/I/L/M/N | X10/X11, X03 retained; T06/T-POLICY | C06 |
| C06 | C01–C05 | A–N, full actual-manifest N | X01–X11; T03/T-IMPORT/N-REAL | C07 |
| C07 | C01–C06 | A–N and affected repository regressions | All X01–X11 and every new counterexample, fresh review | Conditional new qualification/status; never E1 execution |

No unrelated corrections are implied by a package's regression set. A failure assigned to another package is recorded and held rather than opportunistically repaired. Earliest executable package under the plan's stable scheduling rule is **C01**.

## 5. Minor findings and observations

| Item | Disposition | Reason / required evidence |
|---|---|---|
| F05 | FIX_BEFORE_REQUALIFICATION | Can affect deterministic control output and persistence comparison; deferral prohibited by the requested gate |
| F06 | FIX_BEFORE_REQUALIFICATION | Can affect policy provenance/trust and restore binding; deferral prohibited |
| O01 | DOCUMENT_ONLY | Reviewed initial normalization and synthetic trust remain explicit admission assumptions; no online authority service added. Keep existing trust-boundary negative tests. |
| O02 | TEST_HARDENING | Partial goal success is legitimate under the original plan. Add explicit partial/full scope controls and verify required-goal coverage for full E1 import; do not reinterpret the observation as F01-style fail-open behavior. |
| O03 | TEST_HARDENING | Preserve typed identities, pure validation, knowledge separation and absence of deferred/effecting dependencies through regressions/audit |

No required minor deferral, new E1 blocker resolution, speculative architectural feature or new authority is part of this correction plan.

## 6. Requalification evidence checklist

The C07 record must provide each item separately, with exact command/test/source identities and outcomes:

- F01–F04 closed; F05/F06 closed; O01–O03 dispositions satisfied.
- Each T01–T06 fails against the relevant reviewed behavior and passes after its correction with independent oracles; expanded negative and positive controls pass.
- A, B, C, D, E, F, G, H, I, J, K, L, M, N all PASS.
- X01, X02, X03, X04, X05, X06, X07, X08, X09, X10, X11 all PASS; no skipped or not-yet-applicable entries.
- Importer, CLI, complete contract coverage, policy binding, actual frozen-E1 import/validation, process-independent cold resume and canonical persistence PASS.
- All seven scalar global controls, localized/global defect precedence, machine/human/wait combinations, full/partial goal coverage and typed branch/frontier reports PASS.
- Repeated complete replay under controlled collection/reference/filesystem/key order and process-seed variations, with repeated serialize/reload and selector execution, produces identical semantic outputs and canonical state identities. Compare more than selected IDs.
- Fail-open paths = 0 and hidden nondeterminism = 0 **within the tested v0.1 scope**; no claim of universal proof.
- Frozen 10,911-file path/hash inventory unchanged; no E1 resume, authority consumption or production effects; deferred-scope violations = 0; unrelated changes absent; existing qualification artifacts preserved.
- Fresh independent adversarial review accepts corrected enforcing paths and test independence. Original-suite PASS alone is insufficient.

The result of the real frozen test must be derived from the source contracts and then compared to the manifest/checkpoint/handoff oracle. Present frozen semantics are suspension/MIXED_WAIT, no received external evidence, empty actionable/decision-ready sets, no next action, 27 unresolved roots, 41 unresolved slots and VALID_UNCONSUMED Candidate-3 authority. A test that writes these values into the computed state is not a passing readiness test.

Current-status metadata is specified for C01 implementation and a later accepted C07 result, not created now. Historical qualification and the adverse review remain unchanged. Until all required gates and the new review succeed, the superseding implementation status must remain CORRECTION_REQUIRED.
