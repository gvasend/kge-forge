# Activation lifecycle implementation applicability — 2026-09-16

**Classification: INDETERMINATE.**

No expanded Programmer tool, grant, execution command, cleared content or external destination was found. The complete newly enabled activation/dispatch sequence is not established by the available evidence. This is not a revocation of PD-06 or the accepted component lifecycle qualification. No rebind or activation is performed.

## Comparison basis and completeness

The predecessor is the exact operational implementation capture `E1-OPERATIONAL-CONTINUATION-20260916-4f4e0ceec6e2d334` (SHA-256 `4f4e0ceec6e2d3349a58a71f59c47d11ca42b905ad42b268a01c122870b3dec5`), not an inferred clean Git tree or the older R6 implementation. The complete captured/current Python inventory establishes four changed production files, one added production module, no deletions, and two test-file changes. The latter are test_governance_continuation.py and the added test_authorization_lifecycle.py. Git HEAD alone is not the implementation identity.

`DELTA_INVENTORY.json` records complete inventory and AST comparisons; `EXACT_DELTA.patch` contains the exact production diff. All lifecycle-qualified source hashes still match the accepted lifecycle package.

## Exact production changes

### adapter/governed_host.py

- Previous captured SHA-256: `5fca5ed2053806df914365dc0f9bbdd81ef470e27c9b74486863be2d29b7e352`.
- Current SHA-256: `5dba29c66ff78d434878a7bd2b1a75b22d0cb6acea6843264adcdfd3c7e03922`.
- Semantic responsibility: Constructor checks reconstructed lifecycle state; verify_lifecycle() replays durable history and rejects uncertain/mismatched state.
- Affected invariant numbers: [9, 13, 18]
- Before: Exact serialized authorization replay; historical INACTIVE versus requested ACTIVE rejected. No lifecycle recheck method.
- After: Valid append-only transition can support ACTIVE; missing/incomplete/contradictory lifecycle denies host/action/model admission. Existing grants, effect functions and scope mechanics unchanged.
- Programmer tool schema changed: False
- Result semantics: Success envelopes unchanged; additional controller-local lifecycle denials/startup failures. Model filtering continues to redact outcomes/diagnostics.
- Authority: Grant set identical; admission narrowed to valid lifecycle. Reachability of intended ACTIVE-after-INACTIVE path added, subject to dispatch integration evidence gaps.
- New effecting path: No new Programmer effect type. Newly admitted valid lifecycle can reach existing effects; unproved reservation-before-model integration noted.
- Enforcement replaced or bypassed: Original effect/path/exec functions unchanged (AST verified); host constructor now relies on lifecycle-aware recovery and adds checks.

### adapter/orchestrator.py

- Previous captured SHA-256: `6ca75fa81f76e358b4f7e54f4021ed4bbbbb521c3a97299cb33f8169839b1d55`.
- Current SHA-256: `0c877f506111e1e0aca744a8b66b6c8254751cb56868dfe93bcc893fdedfba1d`.
- Semantic responsibility: One verify_lifecycle() call added before context verification for context-bound requests.
- Affected invariant numbers: [3, 4, 5, 12, 13, 14, 15, 18]
- Before: Request identity, ACTIVE/interruption, ownership, context and scope-quiescence gates.
- After: Same gates plus lifecycle validity. A lifecycle denial produces existing DENIED ActionResult type.
- Programmer tool schema changed: False
- Result semantics: ActionResult schema unchanged; lifecycle-invalid requests can now return DENIED with a new local diagnostic. Existing allowed results and model redaction unchanged.
- Authority: Identical resources/actions; stricter admission.
- New effecting path: None; dispatch targets unchanged.
- Enforcement replaced or bypassed: None; lifecycle check inserted before existing context gate. Existing ownership check is retained, not replaced.

### adapter/recovery_ledger.py

- Previous captured SHA-256: `c9a9ad0e85ec9a0bc87a4cb16ab23e6f17cfe4e1dd38ea09389c95fa9553d609`.
- Current SHA-256: `2c87f3f25725b40b4cf68c1327b9f9fd25497333b6872c5eb543a6c9c607c957`.
- Semantic responsibility: For profiles released INACTIVE, replay lifecycle; reject ACTIVE without original/activation history; return controller-local lifecycle reconstruction.
- Affected invariant numbers: [9, 10, 11, 12, 13, 18]
- Before: Every authorization_issued record must equal requested effective authorization exactly; authorized state transition in same audit rejected.
- After: For lifecycle-required profiles, validated original plus ordered activation history explains ACTIVE. Legacy issued-equality remains for other profiles. Existing action digest, scope ownership, kernel population, interruption and QUIESCENT recovery code retained.
- Programmer tool schema changed: False
- Result semantics: Controller reconstruction gains authorization_lifecycle field and lifecycle-specific recovery failures. No model tool schema or cleared content change.
- Authority: Grant comparison still exact after narrowly removing state/dispatch-reference lifecycle delta. Historical-to-effective acceptance changes intentionally; no new work/resource grant.
- New effecting path: Recovery can now permit subsequent use of valid ACTIVE lifecycle instead of rejecting authorized transition; function itself reads evidence only.
- Enforcement replaced or bypassed: YES: unconditional issued-record equality is replaced by ordered exact lifecycle validation for profiles released INACTIVE; kernel/scope/action recovery checks not replaced.

### adapter/responses_orchestrator.py

- Previous captured SHA-256: `62fe79f4575037a1a10fb7cd2ccf545d26bbfa1531be8e417f72ee6aa37b08ad`.
- Current SHA-256: `eb6edbf4fd61f0ef6ea3608050e5cf79cd1510c4fcca53b8615b35e206296a98`.
- Semantic responsibility: Calls host.verify_lifecycle() first in _verify_context().
- Affected invariant numbers: [2, 6, 13, 15, 18]
- Before: Context/projection, effective authorization and transmission policy checked before requests/actions.
- After: Those checks plus durable lifecycle validation. Missing ACTIVE history stops before request construction/continuation. _call, run, _dispatch and tool_definitions unchanged (AST verified).
- Programmer tool schema changed: False
- Result semantics: No new model-visible result schema/content; additional local failure may terminate/prevent reasoning. Original redaction remains.
- Authority: Same model-visible tools/destination/context; lifecycle gate reduces admissible invalid starts.
- New effecting path: No new model request function/destination. Newly valid lifecycle may reach existing request path; reservation-to-request sequencing not proven.
- Enforcement replaced or bypassed: None; prior checks retained after new guard.

### adapter/authorization_lifecycle.py

- Previous captured SHA-256: `ABSENT — new module`.
- Current SHA-256: `b4259a331a4f85e80b2358a995d3cb9a4df7df19a8e10769cbb4495585956c76`.
- Semantic responsibility: New controller-only canonical lifecycle events, identity/dispatch validation, ordered reconstruction and locked/fsynced activation writer.
- Affected invariant numbers: [9, 12, 13, 15, 18]
- Before: No append-only lifecycle writer; no accepted INACTIVE-to-ACTIVE history in the exact existing audit.
- After: Dispatch-authorized, intent, committed ACTIVE and terminal phases recognized. Exact replay non-effecting; competing/invalid predecessors and incomplete history denied. activate() writes administrative lifecycle records after a caller-provided validation callback returns a complete PASS map.
- Programmer tool schema changed: False
- Result semantics: No registered tool or model-facing output. New controller event schema and recovery states only.
- Authority: No new Programmer grants or authority identity; new controller capability to append authoritative ACTIVE lifecycle is effecting and must meet existing Architect prerequisites. Applicability of complete production sequencing remains unproved.
- New effecting path: YES: os.write/fsync lifecycle events to exact existing audit. Checks existing ledger but does not reserve it; releases locks before caller ownership/profile/model stages.
- Enforcement replaced or bypassed: Provides lifecycle validator replacing historical equality in recovery. No registered payload enforcement bypass established. Real atomic validator and ownership handoff not implemented here; delegated to caller.

## Eighteen-invariant comparison

| # | Invariant | Assessment and evidence |
|---|---|---|
| 1 | Exact E1-WP-001 identity | PRESERVED. Task file/hash and released task selection unchanged. Lifecycle dispatch binding checks work identity and exact task hash. |
| 2 | Released Programmer tool registry | PRESERVED. Same nine tools; tool_definitions, _dispatch and registry-bearing source unchanged except lifecycle guard. |
| 3 | Read authority | PRESERVED; ADMISSION IMPLEMENTATION CHANGED. Read roots/exclusions and _path/read/list/search unchanged. Added lifecycle gate before dispatch. |
| 4 | Write/patch authority | PRESERVED; ADMISSION IMPLEMENTATION CHANGED. Exact file/directory grants, ancestor rules, protected-path denial and atomic promotion methods unchanged; targeted dispatcher tests pass. |
| 5 | Execution authority | PRESERVED; ADMISSION IMPLEMENTATION CHANGED. Executable/argv/cwd/inputs/environment and permit/snapshot/exec functions unchanged. New lifecycle gate precedes them; combined activation-to-real-scope evidence gap remains. |
| 6 | Model-transmission authority | PRESERVED; PRE-REQUEST GATE ADDED. Manifest/policy and filtering code unchanged; current direct allowed/denied/alternate probes pass. No released context bytes added. |
| 7 | Network prohibition | PRESERVED. Runtime profile, execution barrier and transport code unchanged; no new networking in lifecycle module. |
| 8 | Filesystem/snapshot isolation | PRESERVED. Path checks, snapshot/acceptance builder and promotion paths unchanged; no automatic snapshot promotion introduced. |
| 9 | Audit/evidence isolation | ISOLATION PRESERVED; WRITER/RECOVERY CHANGED. New local authoritative audit appends are an effect. Existing destination/grant exclusions retained; model receives no lifecycle metadata. Prefix/identity checks qualified. |
| 10 | ExecutionScope admission | COMPONENT PRESERVED; COMPOSED PATH UNPROVED. Permit, supervisor and bridge functions unchanged; targeted scope binding/admission tests plus prior live evidence reused. No lifecycle-aware production dispatch run established. |
| 11 | QUIESCENT-before-success | COMPONENT PRESERVED. governed_exec/action_terminal unchanged; current result-before-QUIESCENT and interruption tests pass. Earlier live synthetic cgroup proof reused within unchanged execution implementation scope. |
| 12 | Sequential ownership | EXECUTION GATE PRESERVED; INVOCATION HANDOFF UNPROVED. Common-ledger rule/implementation unchanged and overlap tests pass. Activation releases lock with no invocation reservation; no production handoff before model/effects is shown. |
| 13 | Recovery semantics | ENFORCEMENT REPLACED IN PART. Ordered lifecycle substitutes for equality only for INACTIVE-origin profiles. Original grant identity, replay, mismatch and interrupted-activation tests pass. Scope/action recovery retained. Complete integrated dispatch/restart trace absent. |
| 14 | Authority-expansion semantics | PRESERVED. Same request tool; expansion() unchanged and decision remains PENDING. No self-authorization added. |
| 15 | Context/projection binding | CHECKS PRESERVED; IMPLEMENTATION PINS REQUIRE DISPOSITION. Context/projection modules and stored release artifacts unchanged. Current runtime correctly rejects changed pinned code. No new operational/full/projection identity is proposed or installed. |
| 16 | Released production profile | PRESERVED. Canonical fingerprint remains b9e7f72d97525f39fbddfe92f276ab6aedd057ef6c5b7284dc163f1db9c9c328; no field edited. |
| 17 | External destination policy | PRESERVED. Same endpoint/model/store/credential reference/proxy/CA settings; no added external destination or model-visible lifecycle information. |
| 18 | Human/Architect authority boundaries | LOCAL CHECKS PRESERVED; END-TO-END ENFORCEMENT UNPROVED. Exact existing dispatch required; no model registry activation capability. Correct full atomic validation and ownership-before-model depend on an unprovided caller/validator path, not established by PASS-dictionary fixtures. |

## Lifecycle semantic assessment

Exact inactive identity + an exact dispatch reference + a supplied complete validation map produces an append-only intent and ACTIVE commit. Restart checks event/prefix/authorization identity; invalid predecessor, material grant substitution and missing ACTIVE event fail closed in the qualified cases. That is narrower than proving **successful real atomic validation and a mandatory ownership handoff** precede every model/effect path. The callback is controller-owned, not model-supplied; the review does not assume an attacker can forge controller state. It also does not invent a production caller or new trust guarantee to complete the proof.

## Specific unresolved applicability evidence

### LIA-01 — Production atomic validator is not established

- activate() accepts validate() returning named PASS strings. It checks audit immutability around that callback, not observations for all named release/host/provisioning predicates.
- The lifecycle tests supply lambda: self.checks. The production adapter has no caller of activate(); no pinned full production validation implementation/receipt is connected to this API.

Cannot prove successful actual atomic dispatch validation is a non-bypass predecessor to lifecycle commit. This is a missing integration proof, not evidence the Programmer can call a forged validator.

Smallest additional evidence: Identify the exact trusted production validator/caller and its bound observations; exercise each relevant false/stale predicate and interleaving, proving no commit or request on failure. Do not infer sufficiency from a supplied PASS map.

### LIA-02 — Invocation ownership handoff is not established

- activate() returns durable ACTIVE and closes ledger/audit locks without an ownership reservation.
- The archived accepted positive fixture has an empty ownership ledger; read-only replay shows verify_lifecycle() accepts that ACTIVE history.
- ResponsesReasoning.run/_verify_context do not require a matching invocation reservation before the first _call. Existing request ownership gate rejects any outstanding per-execution reservation; no distinct invocation-lease/handoff protocol is provided.

Existing per-ExecutionScope sequential gating is preserved, but it does not establish the Architect-required invocation reservation before profile/model use. No model request or bypass attempt was executed.

Smallest additional evidence: Specify and qualify the normal activation→matching invocation reservation→profile→pre-model handoff, including races/crash/restart and compatibility with existing per-execution ownership. Prove the first request/effect cannot pass without that reservation.

### LIA-03 — No combined lifecycle and production execution qualification

- Prior live governance-continuation fixture uses a profile released ACTIVE and therefore skips the new lifecycle-required branch.
- Current targeted execution regressions use a mock supervisor and legacy synthetic authorization. Current lifecycle proof stops before invocation ownership and execution.

These valid component results cannot alone establish unchanged behavior of the full INACTIVE-origin lifecycle-required execution/recovery path.

Smallest additional evidence: After resolving the normal handoff, one bounded synthetic trace combining durable activation, restart, ownership, governed effect/exec, result-before-QUIESCENT and terminal audit suffices; broad PD-05/A2 reopening is unnecessary.

## Targeted regression and evidence reuse

Nine new targeted tests passed (`TARGETED_REGRESSIONS.txt`): committed context binding and stale-source denial; governed read/write/patch exclusions, ancestor behavior and promotion; governed exec identity/replay; result-before-QUIESCENT gating; scope substitution denial; supervisor-loss uncertainty; and interruption ordering. The execution bridge is simulated, so these are current controller regressions, not new live-kernel qualification. No model request or activation event was generated.

`TRANSMISSION_AND_PREMODEL_PROBES.json` verifies current cleared-read forwarding, local/private redaction, list/search/status/error/hash and alternate-result redaction, unchanged context/projection validation, and INACTIVE denial before _call. _call was replaced with a must-not-call sentinel and was never called.

`ARCHIVED_LIFECYCLE_PROBES.json` replays the already-captured synthetic audit in memory, with exact captured source bytes supplied to its content-reference reader. No event was created or appended. ACTIVE reconstruction, missing-event denial, exact replay and identity mismatch pass. The same guard accepts the archived empty ownership ledger, showing its limited scope rather than proving an actual model request bypass.

The 30-test accepted lifecycle qualification remains applicable to the exact unchanged lifecycle source bytes. Its lifecycle/replay/mismatch/terminal/interruption checks are reused rather than rerun to create new events. The previous live governance-continuation execution evidence is reused only for unchanged execution components; it is not mislabeled as lifecycle-required activation integration.

## Disposition returned to the Architect

NON_MATERIAL_IMPLEMENTATION_CONTINUATION is not established. MATERIAL_RELEASE_CHANGE is also not asserted merely from code-hash changes or missing integration evidence: no new Programmer grants/destinations or actual external bypass has been demonstrated. The supported classification is INDETERMINATE, limited to activation orchestration, atomic validation, invocation ownership handoff and their composed recovery path. Broader PD-05/A2 reopening is not supported by this review.

No proposed OperationalContextId, FullContextDigest or ModelProjectionDigest is calculated, and no proposed implementation-continuation record is issued. Those are conditional on a supported NON_MATERIAL classification. Existing release, dispatch, authorization, profile, clearance and historical INACTIVE records remain unchanged. E1 stays INACTIVE; E1-WP-001 stays INELIGIBLE and UNDISPATCHED.
