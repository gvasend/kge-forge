# Canonical qualification acceptance matrix 1

All cases are **PLANNED, NOT EXECUTED**. No PASS is claimed. Companion: [machine-readable experiment/matrix](DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_EXPERIMENT_1.json). Expected states must be independently authored and pinned in E2-P01 before implementation output exists.

## E2-A01 — Complete canonical universe and independent O01 profile

**Initial State:** Reviewed six-Action definition contract and frozen source pins

**Operation:** Construct through existing canonical types; native/O01 validation

**Expected State:** Six exact13-field definitions; no extra/missing actions/statuses/references; no occurred result from declaration

**Negative Invariants:** No E1 mutation, authority leakage, fabricated proof or bypass.

**Persistence Requirement:** Canonical before/after identities and event trace required.

**Determinism Requirement:** Repeat equal semantic inputs; canonical identities and full computation equal.

## E2-A02 — Deterministic selection without execution

**Initial State:** Two independently eligible read-only acquisition actions

**Operation:** recompute and select twice without applying event

**Expected State:** Same selected ActionId and witnesses; ledger,knowledge,roots,slots unchanged

**Negative Invariants:** No E1 mutation, authority leakage, fabricated proof or bypass.

**Persistence Requirement:** Canonical before/after identities and event trace required.

**Determinism Requirement:** Repeat equal semantic inputs; canonical identities and full computation equal.

## E2-A03 — Bounded execution and accepted knowledge

**Initial State:** Selected acquisition action with independently specified output contract

**Operation:** record_result/append_event with supplied bounded result

**Expected State:** Only declared knowledge accepted; stale/missing outputs cannot complete current prerequisites; PASS alone does not resolve root/slot

**Negative Invariants:** No E1 mutation, authority leakage, fabricated proof or bypass.

**Persistence Requirement:** Canonical before/after identities and event trace required.

**Determinism Requirement:** Repeat equal semantic inputs; canonical identities and full computation equal.

## E2-A04 — Decision readiness and authority separation

**Initial State:** Preparation action dependencies met; no recorded decision

**Operation:** Apply preparation result then recompute

**Expected State:** Human decision becomes ready only with complete dossier/checks; authority requirement alone did not make it ready

**Negative Invariants:** No E1 mutation, authority leakage, fabricated proof or bypass.

**Persistence Requirement:** Canonical before/after identities and event trace required.

**Determinism Requirement:** Repeat equal semantic inputs; canonical identities and full computation equal.

## E2-A05 — Synthetic bounded decision/grant

**Initial State:** Ready human decision with predefined qualification-only choices and independently pinned record

**Operation:** apply_recorded_decision through append_event; exact permitted record

**Expected State:** Decision history recorded; bounded authority evaluated by native predicate; no root/slot automatically satisfied

**Negative Invariants:** No E1 mutation, authority leakage, fabricated proof or bypass.

**Persistence Requirement:** Canonical before/after identities and event trace required.

**Determinism Requirement:** Repeat equal semantic inputs; canonical identities and full computation equal.

## E2-A06 — External request and absence

**Initial State:** Reentry action held; known validation rule; evidence unavailable; exact route/producers/context bound

**Operation:** Native request-ready then waiting events

**Expected State:** EXTERNAL_WAIT; actionable=[]; human_ready=[]; receipt empty; evidence proof not PROVED; resume false

**Negative Invariants:** No E1 mutation, authority leakage, fabricated proof or bypass.

**Persistence Requirement:** Canonical before/after identities and event trace required.

**Determinism Requirement:** Repeat equal semantic inputs; canonical identities and full computation equal.

## E2-A07 — Persist external checkpoint

**Initial State:** E2-A06 checkpoint

**Operation:** save_bundle; terminate writer process after immutable manifest committed

**Expected State:** Source/policy/event identities pinned; no saved control label treated as authority

**Negative Invariants:** No E1 mutation, authority leakage, fabricated proof or bypass.

**Persistence Requirement:** Canonical before/after identities and event trace required.

**Determinism Requirement:** Repeat equal semantic inputs; canonical identities and full computation equal.

## E2-A08 — Cold restoration

**Initial State:** Empty fresh process, only immutable bundle/identity/source pins/contracts

**Operation:** restore and recompute; compare semantic inventory

**Expected State:** Exact action/knowledge/root/slot/authority/evidence/route/policy/validity/branch/control/resume equality; EXTERNAL_WAIT

**Negative Invariants:** No fixture rebuild, conversation, globals, cached objects or hidden files.

**Persistence Requirement:** Actual separate terminated writer/reader PIDs; no same-process roundtrip substitute.

**Determinism Requirement:** Repeat equal semantic inputs; canonical identities and full computation equal.

## E2-A09 — Evidence ingestion before receipt

**Initial State:** Cold restored checkpoint; separately created qualification-only bundle

**Operation:** Independently authenticate bytes/producer/claims through P01-pinned native admission boundary; then EVIDENCE_RECEIVED event

**Expected State:** Admitted source exists; gate pending artifact recorded; no receipt observation acceptance or resume yet

**Negative Invariants:** Cannot mutate pending/stage/status/accepted observations or call dataclass replacement as receipt; stop if required native ingestion transaction unavailable.

**Persistence Requirement:** Canonical before/after identities and event trace required.

**Determinism Requirement:** Repeat equal semantic inputs; canonical identities and full computation equal.

## E2-A10 — Validation distinct from resume

**Initial State:** Evidence received, current scoped source and authentic independent claims

**Operation:** EVIDENCE_VALIDATED event through append_event

**Expected State:** ReceiptObservation accepted and external_complete true; resume false until accepted reentry event and named eligibility

**Negative Invariants:** No E1 mutation, authority leakage, fabricated proof or bypass.

**Persistence Requirement:** Canonical before/after identities and event trace required.

**Determinism Requirement:** Repeat equal semantic inputs; canonical identities and full computation equal.

## E2-A11 — C03 reentry conjunction

**Initial State:** Validated evidence; other prerequisites current; exact policy/context lineage

**Operation:** DEPENDENT_ACTION_REENTRY event and resume_eligibility with source root

**Expected State:** Only named reentry eligible; C03 pins/lineage/currentness/other gates independently pass; no general resume permission

**Negative Invariants:** No E1 mutation, authority leakage, fabricated proof or bypass.

**Persistence Requirement:** Canonical before/after identities and event trace required.

**Determinism Requirement:** Repeat equal semantic inputs; canonical identities and full computation equal.

## E2-A12 — Actual post-reentry planning continuation

**Initial State:** Reentry action eligible under E2-A11

**Operation:** recompute -> deterministic select -> supplied permitted result -> append_event

**Expected State:** New event/state identity and accepted declared knowledge; downstream finishing action evaluated; not just resume Boolean

**Negative Invariants:** No E1 mutation, authority leakage, fabricated proof or bypass.

**Persistence Requirement:** Canonical before/after identities and event trace required.

**Determinism Requirement:** Repeat equal semantic inputs; canonical identities and full computation equal.

## E2-A13 — Root/slot proof independently admitted

**Initial State:** Required post-reentry claim available; independently defined proof predicates

**Operation:** Native proof/root/slot recomputation and selected finishing result

**Expected State:** Root/slot changes only from their complete source-bound proof; terminal success only if all declared goals proven

**Negative Invariants:** No E1 mutation, authority leakage, fabricated proof or bypass.

**Persistence Requirement:** Canonical before/after identities and event trace required.

**Determinism Requirement:** Repeat equal semantic inputs; canonical identities and full computation equal.

## E2-A14 — Governed unknown checkpoint variant

**Initial State:** Independent canonical copy of external checkpoint with rule_known=false and valid ExternalResolutionContract

**Operation:** Native recompute, save, terminate, restore

**Expected State:** EXTERNAL_WAIT; rule remains unknown; no positive proof/evidence/resume; no automatic rule-known transition

**Negative Invariants:** Not used as positive receipt continuation unless a separate native rule-admission contract exists; no flag patch.

**Persistence Requirement:** Canonical before/after identities and event trace required.

**Determinism Requirement:** Repeat equal semantic inputs; canonical identities and full computation equal.

## E2-A15 — Post-reload source invalidation

**Initial State:** Restored accepted knowledge/proof/authority state in isolated copy

**Operation:** SourceInvalidation event for each disjoint required source

**Expected State:** Dependent admission stale; ordering obligations retained; held/blocked descendants; resume false; reload preserves invalidation

**Negative Invariants:** No E1 mutation, authority leakage, fabricated proof or bypass.

**Persistence Requirement:** Canonical before/after identities and event trace required.

**Determinism Requirement:** Repeat equal semantic inputs; canonical identities and full computation equal.

## E2-A16 — Governed route invalidation

**Initial State:** Restored E2-A14 variant

**Operation:** Invalidate required acquisition-contract source

**Expected State:** PLAN_DEFECT when no other valid route; waiting label does not suppress defect

**Negative Invariants:** No E1 mutation, authority leakage, fabricated proof or bypass.

**Persistence Requirement:** Canonical before/after identities and event trace required.

**Determinism Requirement:** Repeat equal semantic inputs; canonical identities and full computation equal.

## E2-N01 — Unknown with no route

**Initial State:** E2-A14 copy

**Operation:** Remove exact external-resolution binding in negative candidate

**Expected State:** PLAN_DEFECT; no runnable/reentry

**Negative Invariants:** No E1 mutation, authority leakage, fabricated proof or bypass.

**Persistence Requirement:** Canonical before/after identities and event trace required.

**Determinism Requirement:** Repeat equal semantic inputs; canonical identities and full computation equal.

## E2-N02 — Malformed route

**Initial State:** E2-A14 copy

**Operation:** Substitute request/proposition/producer or receipt target

**Expected State:** Reject admission or PLAN_DEFECT at contract-defined boundary; never waiting eligibility

**Negative Invariants:** No E1 mutation, authority leakage, fabricated proof or bypass.

**Persistence Requirement:** Canonical before/after identities and event trace required.

**Determinism Requirement:** Repeat equal semantic inputs; canonical identities and full computation equal.

## E2-N03 — Wrong lineage

**Initial State:** Checkpoint/evidence copy

**Operation:** Use correctly hashed but wrong-lineage source/contract

**Expected State:** Reject correspondence; invalid unknown-route probe is PLAN_DEFECT; no resume

**Negative Invariants:** No E1 mutation, authority leakage, fabricated proof or bypass.

**Persistence Requirement:** Canonical before/after identities and event trace required.

**Determinism Requirement:** Repeat equal semantic inputs; canonical identities and full computation equal.

## E2-N04 — Stale evidence

**Initial State:** Received/validated copy

**Operation:** Invalidate evidence or independent attestor

**Expected State:** Not accepted/current; no eligible reentry or resume

**Negative Invariants:** No E1 mutation, authority leakage, fabricated proof or bypass.

**Persistence Requirement:** Canonical before/after identities and event trace required.

**Determinism Requirement:** Repeat equal semantic inputs; canonical identities and full computation equal.

## E2-N05 — Source substitution

**Initial State:** Pinned source set

**Operation:** Replace bytes or same-digest wrong identity domain

**Expected State:** Pin/domain rejection before planning use

**Negative Invariants:** No E1 mutation, authority leakage, fabricated proof or bypass.

**Persistence Requirement:** Canonical before/after identities and event trace required.

**Determinism Requirement:** Repeat equal semantic inputs; canonical identities and full computation equal.

## E2-N06 — Wrong authority

**Initial State:** Authority-dependent action

**Operation:** Supply unrelated/wrong-class/out-of-scope grant

**Expected State:** Authority predicate not proved; action ineligible

**Negative Invariants:** No E1 mutation, authority leakage, fabricated proof or bypass.

**Persistence Requirement:** Canonical before/after identities and event trace required.

**Determinism Requirement:** Repeat equal semantic inputs; canonical identities and full computation equal.

## E2-N07 — Invalid proof

**Initial State:** Post-reentry candidate

**Operation:** Missing/wrong-root/wrong-slot/placeholder proof

**Expected State:** Root/slot unresolved/stale; no satisfaction from PASS

**Negative Invariants:** No E1 mutation, authority leakage, fabricated proof or bypass.

**Persistence Requirement:** Canonical before/after identities and event trace required.

**Determinism Requirement:** Repeat equal semantic inputs; canonical identities and full computation equal.

## E2-N08 — Dangling prerequisite

**Initial State:** Initial candidate

**Operation:** Reference undeclared ActionId or wrong domain

**Expected State:** Native admission rejects before recompute

**Negative Invariants:** No E1 mutation, authority leakage, fabricated proof or bypass.

**Persistence Requirement:** Canonical before/after identities and event trace required.

**Determinism Requirement:** Repeat equal semantic inputs; canonical identities and full computation equal.

## E2-N09 — Stale accepted knowledge

**Initial State:** Held descendant

**Operation:** Invalidate knowledge source after producer historical completion

**Expected State:** Current prerequisite fails; no producer-completion shortcut

**Negative Invariants:** No E1 mutation, authority leakage, fabricated proof or bypass.

**Persistence Requirement:** Canonical before/after identities and event trace required.

**Determinism Requirement:** Repeat equal semantic inputs; canonical identities and full computation equal.

## E2-N10 — Wrong selection policy

**Initial State:** Valid bundle

**Operation:** Substitute valid unrelated pin or unsupported version

**Expected State:** Import/restore/selection rejects policy binding

**Negative Invariants:** No E1 mutation, authority leakage, fabricated proof or bypass.

**Persistence Requirement:** Canonical before/after identities and event trace required.

**Determinism Requirement:** Repeat equal semantic inputs; canonical identities and full computation equal.

## E2-N11 — Persistence tampering

**Initial State:** Checkpoint bytes

**Operation:** Alter event parent/current snapshot/source index; retain trusted expected bundle identity

**Expected State:** Restore rejects; rehashing attacker bytes cannot replace trusted expected identity

**Negative Invariants:** No E1 mutation, authority leakage, fabricated proof or bypass.

**Persistence Requirement:** Canonical before/after identities and event trace required.

**Determinism Requirement:** Repeat equal semantic inputs; canonical identities and full computation equal.

## E2-N12 — Selection/history conflation

**Initial State:** Selected action with no supplied result

**Operation:** Attempt to use selection record as execution/completion

**Expected State:** No native result accepted; ledger/knowledge not fabricated

**Negative Invariants:** No E1 mutation, authority leakage, fabricated proof or bypass.

**Persistence Requirement:** Canonical before/after identities and event trace required.

**Determinism Requirement:** Repeat equal semantic inputs; canonical identities and full computation equal.

## E2-N13 — Prospective/actual conflation

**Initial State:** Admitted Action definition

**Operation:** Present its output declaration as actual supplied result

**Expected State:** Reject wrong event/result; knowledge/root/slot unchanged

**Negative Invariants:** No E1 mutation, authority leakage, fabricated proof or bypass.

**Persistence Requirement:** Canonical before/after identities and event trace required.

**Determinism Requirement:** Repeat equal semantic inputs; canonical identities and full computation equal.

## E2-N14 — Receipt/reentry bypass

**Initial State:** Waiting or merely received evidence

**Operation:** Attempt validation/reentry out of order or unrelated artifact

**Expected State:** Illegal transition/failed proof; no resume

**Negative Invariants:** No E1 mutation, authority leakage, fabricated proof or bypass.

**Persistence Requirement:** Canonical before/after identities and event trace required.

**Determinism Requirement:** Repeat equal semantic inputs; canonical identities and full computation equal.

## E2-N15 — Accepted evidence with blocked named action

**Initial State:** Valid receipt/reentry copy

**Operation:** Leave independent required condition unsatisfied

**Expected State:** Named-action eligibility false and C03 resume false

**Negative Invariants:** No E1 mutation, authority leakage, fabricated proof or bypass.

**Persistence Requirement:** Canonical before/after identities and event trace required.

**Determinism Requirement:** Repeat equal semantic inputs; canonical identities and full computation equal.

## E2-N16 — Independent branch precedence

**Initial State:** Governed unknown checkpoint variants

**Operation:** Add independently eligible machine/human or factual blocked frontier

**Expected State:** RUNNABLE for machine; HUMAN_HANDOFF for only ready human; MIXED_WAIT with factual frontier; unknown still unknown

**Negative Invariants:** No E1 mutation, authority leakage, fabricated proof or bypass.

**Persistence Requirement:** Canonical before/after identities and event trace required.

**Determinism Requirement:** Repeat equal semantic inputs; canonical identities and full computation equal.

## E2-D01 — Ordering/hash/process determinism

**Initial State:** All positive and negative supported semantic states

**Operation:** Seeds0,1,7,101; reversed/rotated action,source,goal,proof,authority orders; object-key permutations; fresh processes

**Expected State:** Full Computation,selected action,canonical snapshot/bundle identity equal for equal semantics; ordered event chronology preserved

**Negative Invariants:** Do not permute causal ledger history or ordered selection-policy rules as if sets.

**Persistence Requirement:** At least3 independent cold restores per checkpoint per seed.

**Determinism Requirement:** Compare branches,witnesses,rejections,all typed identities,not only scalar control.

## E2-END — End-to-end canonical lifecycle

**Initial State:** Only independently authored canonical E2 contracts and source bytes

**Operation:** A01-A13 across real writer termination and fresh reader then repeat under D01

**Expected State:** All stage-specific independent oracles pass; real post-reentry event and updated state; no legacy importer or E1 execution

**Negative Invariants:** Expected oracle files excluded from execution inputs; no planner output becomes its own oracle.

**Persistence Requirement:** Canonical before/after identities and event trace required.

**Determinism Requirement:** Repeat equal semantic inputs; canonical identities and full computation equal.

## E2-REG — Existing baseline remains required

**Initial State:** Pinned current code/contracts and read-only E1 corpus

**Operation:** Full affected native/CLI/importer/constructor suites including A-N,X01-X11,C01-C06,budget and external unknown

**Expected State:** All prior closed findings remain closed; no skipped requirements or blanket historical count reused

**Negative Invariants:** No E1 mutation, authority leakage, fabricated proof or bypass.

**Persistence Requirement:** Canonical before/after identities and event trace required.

**Determinism Requirement:** Repeat equal semantic inputs; canonical identities and full computation equal.

## E2-REVIEW — Fresh independent adversarial review

**Initial State:** E2-END/D01/REG all pass with complete evidence

**Operation:** New reviewer probes all enforcing paths and mutations after qualification

**Expected State:** No open correctness/determinism/persistence/authority/resume defect for final acceptance; new finding returns to correction package

**Negative Invariants:** No E1 mutation, authority leakage, fabricated proof or bypass.

**Persistence Requirement:** Canonical before/after identities and event trace required.

**Determinism Requirement:** Repeat equal semantic inputs; canonical identities and full computation equal.

## Thirty-requirement coverage

| # | Required semantic | Case |
|---|---|---|
| 1 | complete typed Action definitions | E2-A01 |
| 2 | multiple operation classes | E2-A01 |
| 3 | prerequisites | E2-A03 |
| 4 | accepted knowledge | E2-A03 |
| 5 | source validity | E2-A15 |
| 6 | stale invalidation | E2-A15 |
| 7 | authority requirement versus possession | E2-A05 |
| 8 | decision readiness | E2-A04 |
| 9 | roots | E2-A13 |
| 10 | slots | E2-A13 |
| 11 | typed proof admission | E2-A13 |
| 12 | typed authority admission | E2-A05 |
| 13 | deterministic selection | E2-A02 |
| 14 | policy binding | E2-N10 |
| 15 | external request | E2-A06 |
| 16 | expected absence | E2-A06 |
| 17 | governed unknown | E2-A14 |
| 18 | receipt | E2-A09 |
| 19 | evidence validation | E2-A10 |
| 20 | reentry lineage | E2-A11 |
| 21 | resume eligibility | E2-A11 |
| 22 | branch/global controls | E2-N16 |
| 23 | persistence | E2-A07 |
| 24 | cold restoration | E2-A08 |
| 25 | canonical serialization | E2-D01 |
| 26 | provenance | E2-A01 |
| 27 | invalidation after reload | E2-A15 |
| 28 | selection versus execution | E2-N12 |
| 29 | prospective versus actual result | E2-N13 |
| 30 | fail-closed unexplained state | E2-N01 |
