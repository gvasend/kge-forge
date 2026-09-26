# r11 ownership, status and authenticated attempt ancestry qualification

**RUN2_R11_READY_FOR_ARCHITECT_ISSUANCE — qualified and prepared, not adopted or issued.** The Architect must accept/apply the exact proposed material amendment and implementation continuation and authorize this specific invocation before any issuance. This result is not permission to retry r10. No real r11 authorization, activation, ownership, model request, ActionRequest, execution or implementation effect occurred.

## Ownership defect and correction

The frozen schema-6 validator correctly selected fresh predecessor-specific ownership but then required the old captured **global** ledger owner to be None. A cold capture after r10 activation therefore rejected r10's legitimate reservation; a long-lived observer retaining that capture remained UNKNOWN even after cancellation. The original failed recovery stderr was retained only as a hash. Diagnosis rests on frozen source, durable ordering and isolated reproduction, not an invented original error transcript.

The candidate separates immutable predecessor eligibility evidence from fresh mutable ownership. The unchanged ledger parser rejects duplicate reservations, fingerprint substitution, contradictory release/order and malformed history. `attempt_ownership.attribute` checks the exact authorization/session/audit tuple. A predecessor owner, unknown owner, mismatched tuple or unowned execution scope blocks. It permits only attribution of the specifically selected current owner; it never grants ACTIVE or handoff. Existing lifecycle recovery and handoff still require the exact reservation committed in the current attempt's ACTIVE event. INACTIVE/terminal ownership conflicts block; an intent/reservation crash stays held for reconciliation and ineligible.

Captured owners are historical observations and are not reused as current ownership. No global-empty-ledger requirement replaces predecessor-specific verification. Current mutable ownership and execution state remain freshly observed. Existing cancellation releases only the reservation matching that invocation's authoritative activation event.

## Replacement-policy applicability and newly exposed gap

r10 independently reconstructs CANCELLED / INTERRUPTED_NO_EFFECTS, unowned and QUIESCENT, with no model/provider request, ActionRequest, ExecutionScope or implementation effect. It follows the safe pre-model ACTIVE→cancelled class. Its unchanged audit SHA-256 is `595487a35a5095c774dd193e15f0ceac839c5e2fe698ff784c5b6417bf44260c`.

However, the existing policy does **not** fully cover r10's physical record layout: r10's final physical row is hash-correlated `final_disposition` telemetry naming the immediately preceding authoritative cancellation event. The old predicate requires cancellation itself to be the last physical row. The initial construction correctly blocked on this requirement; its failure is retained in BUILD.log and CONSTRUCTION_RESULT.json. Neither the original predicate nor the r10 audit was rewritten.

The proposed material amendment adds only the missing suffix semantics: one attributable cycle-zero final-disposition record may follow cancellation, with exactly CANCELLED, RELEASED, the same terminal-event identity and no uncertainty. Unknown events, a second suffix, conflicting disposition, provider uncertainty, action/model activity or a changed terminal reference remain rejected. The complete telemetry hash/order chain is checked. Telemetry does not create or override lifecycle authority.

The amendment also replaces exact-r9→r10 selection with authenticated ordered attempt ancestry under that safe-predecessor policy. There are no hard-coded r11 identities in the validator and no latest-attempt rule. Each selected successor still requires its exact proposal and a separate attributable Architect adoption/issuance decision. Completed, effecting, uncertain, owned and non-QUIESCENT predecessors remain ineligible. No automatic retry is introduced.

## Qualification and its limits

- **24 synthetic tests PASS:** ownership attribution, predecessor/unknown/competing owner rejection, duplicate reservations, wrong lifecycle, exact reservation matching, restart, cancellation, session boundaries, status transitions, stale activity and protected model handoff.
- The combined cold-process fixture uses the genuine immutable r8/r9/r10 predecessor evidence and an isolated **non-E1 synthetic current invocation/ledger**. It issues INACTIVE, activates, independently recovers current ownership in a new process, enters the dispatcher-owned session, reaches an in-memory stub transport, and cancels/releases. The genuine shared ledger is never modified. No E1 task or real provider is invoked.
- **8 actual-identity/policy tests PASS:** captured-owner poisoning correction; exact candidate attribution and all predecessor negatives; missing/reordered ancestry; suffix-policy negatives; r10 original-policy rejection retained; unused namespace and historical preservation.
- **6 synthetic specific-grant tests PASS:** missing, PREPARED, wrong candidate/release/context/ancestry, wrong qualification and unattributed source are rejected. Synthetic approvals exist only in test memory and are not real Architect grants.
- **19 actual-context negative probes PASS:** alternate authorization/task/read/execution/transmission, missing private amendment/proposal/dispatch/continuation/capture, substituted payload/profile/budget/release/supervisor/task, reordered selection and absent specific issuance authority.
- **32 regression tests PASS:** ownership, budgets, immutable witnesses, controller store, governed execution/QUIESCENT and transmission isolation. One test initially hit the sandbox's blocked NETLINK_ROUTE operation; the exact isolated payload-namespace test passed outside the sandbox. Both results remain recorded.
- Actual prepared production bootstrap, full non-effecting pre-issuance validation including genuine S3, warm validation, context/projection verification and independent sealed-store reconstruction **PASS**.

The exact production r11 invocation remains **unissued**, not ACTIVE or model-handoff eligible. Effecting lifecycle/model-boundary tests are synthetic; actual-context preflight is read-only. This does not claim a real r11 ACTIVE recovery or live Programmer turn has happened.

## Operator projection

The principal r10 UNKNOWN cause was the contaminated predecessor capture, not a payload/profile mismatch. The observer's initial 0755 directory rejection was a separate historical orchestration problem already corrected during r10; it was not a cause of the continued cached-owner rejection.

The candidate projects lifecycle/ownership from freshly checked authoritative evidence and presents activity freshness separately. A freshly established INACTIVE or ACTIVE state is retained when old/absent telemetry cannot establish the current subphase; that subphase is UNKNOWN. Source absence, substitution, inconsistent snapshots or incompatible ownership makes the authoritative projection UNKNOWN. A terminal lifecycle dominates stale provisional activity. The inherited `state=UNKNOWN` field is explicitly reconciled so it cannot contradict the lifecycle field.

Synthetic live projections cover INACTIVE, ACTIVATING, ACTIVE/OWNERSHIP_HELD, DISPATCHING and CANCELLED/RELEASED/QUIESCENT, including the actual predecessor-chain predicate and cold recovery. Intent without a reservation projects ownership NONE; an incomplete owned activation stays HELD_FOR_RECONCILIATION. Status always has `handoff_eligible=false`: it is a view, never execution authority. Representative complete snapshots are retained in SYNTHETIC_FINAL.log.

## Timing and attempt-history cost

Historical r10 activation validation: **38.7317s**. Three recorded nested model-projection spans total **14.8503s** (4.9443s, 4.9647s, 4.9413s). The remaining **23.8814s** lacks finer historical spans; it is not retroactively assigned to an invented cause.

Current read-only profiling of the unchanged frozen runtime measured cold bootstrap 30.2206s, including 26.543s in the predecessor subprocess; warm governance verification 0.4117s; model projection 6.4504s; terminal status 11.4535s. Projection included 348 catalog checks and 3,133 boundary/path checks. These measurements are explicitly profiled and are not substituted for the historical r10 durations.

Final prepared production measurements (unprofiled):

| Phase | Seconds | Released phase policy |
|---|---:|---|
| Cold private bootstrap | 4.0249 | below soft |
| Cold production pre-issuance validation | 35.1389 | soft warning, below hard |
| Warm unchanged validation | 35.1048 | soft warning, below hard |
| Operational-context reconstruction | 0.9744 | below soft |
| Model-projection validation | 5.8886 | below soft |
| Independent sealed authority/projection/S3 reconstruction | 25.7648 | below soft |

Two initial qualification soft warnings plus 1 final sealed-store recheck soft warning are durable, explicitly outside any authorization lifecycle. The exact sealed-store full production validation passed in 34.6092s (bootstrap 4.0411s); see SEALED_PRODUCTION_PREFLIGHT.json. **30s soft / 120s hard remain unchanged.** No hard threshold was exceeded. Warm validation still misses the practical sub-30s target; this is reported, not hidden or converted into a hard-budget failure. All other released cycle/no-progress/invocation/request/token policies are byte-identical. No reliable token accounting is claimed; there were zero real requests.

The proposed private historical capture removes recursive cold verifier-process execution. It preserves exact publication pins, all underlying private-store witnesses, runtime/verifier/interpreter identities, immutable audit hashes and current mutable context inputs; current ownership/scope/S3 are checked separately and freshly. Prefix microbenchmarks measured about 0.485s through r9 and 0.679s through r10. Verification still grows with distinct history; no constant-time or unlimited-attempt performance guarantee is made. HISTORY_REUSE_PROPOSAL.md separates the proposed proof representation from a possible later deduplicated cumulative-witness optimization. No mutable authority fact is cached away.

## Separate applicability classifications

1. **Attempt-scoped ownership correction: NON_MATERIAL_IMPLEMENTATION_CONTINUATION candidate.** Restores required attribution; preserves lifecycle, reservation, cancellation, recovery and handoff gates.
2. **Live-status correction: NON_MATERIAL_IMPLEMENTATION_CONTINUATION candidate.** Read-only projection reconciliation; no authority or model-transmission expansion.
3. **Generic selected-attempt ancestry plus the final-disposition suffix rule: MATERIAL_RELEASE_CHANGE candidate.** Explicitly bound in the append-only proposed amendment. Historical r10's precise record layout was not previously eligible under the exact terminal-row rule.
4. **Persistent historical proof representation/reuse: explicitly included in the proposed material amendment's runtime and capture binding, not concealed inside the non-material continuation.** It changes which qualified private representation is consumed on cold restart. Current factual checks remain fresh. Further cumulative-witness deduplication is proposed separately and not implemented/adopted.

The non-material continuation lists only attempt_ownership.py, attempt_transition.py and operator_projection.py. Schema-7 routing and proof/selection consumption changes are bound by the material amendment's complete implementation identity. The exact delta is in IMPLEMENTATION_DELTA.json. Original release/amendment/continuation bytes and the original nested-session guard are preserved.

## Exact proposed identities

- Invocation: `auth-e1-wp-001-r11-4dae6644072f42c0b4ffd00be7e80a5d`
- Binding SHA-256: `50cd9be1a0f068ae05506380e3b8847820438098e48d345e5c70e56225694887`
- Amendment: `E1-RUN2-ATTEMPT-CHAIN-AMENDMENT-sha256:6cb2acacc01df9933f3935c1d7acdf26d433616dc2b542bcd0360435f6da6a20`
- Amendment file SHA-256: `0437e7d70f03f18331d9d01e3e53d23fd1c8752e1123393dc49a64d6bac5d40f`
- Non-material continuation: `CONTINUATION-sha256:56ae933e54076524dc57b39f6439ec3fa3b55918f155ce27c65b1b91ea5b2249`
- Continuation file SHA-256: `06f1e7986240bcf37b9f2ea61901bcfa4f957d64aa5e6b3943e03b3c9a2099f2`
- Candidate controller runtime: `sha256:6aee3657aeab07f8bb309c387658bec1e51fd5fb1b392b76a6cd4ebb6de7d95e`
- Proposed resulting release authority: `E1-RELEASE-AUTHORITY-sha256:c700953e36c6f3e24a2da31aa4a8249bba4d886b5dc563055b897c536784800e`
- Proposed OperationalContextId: `E1-OPERATIONAL-CONTEXT-sha256:cec20b572e28e6de7c9d3f4c928b1bef631a4ad4c2a01ecafb845edbefd26227`
- Proposed ancestry digest: `8cf1090f08f89342ef236e6cbb3f4fdcd60df8c31382369e43a8aad63de25275`
- Proposed FullContextDigest: `91ed21d3006bf116885cda5dbdc69aa04f5dd2f1e20184554a2d743fe9b38e32`
- Proposed ModelProjectionBindingDigest: `831dfc4dafaf102e5a5d3f7304b6c6158cdbd18664dbfdeddf114abfd53cb5ac`
- Unchanged ModelPayloadDigest: `d675d581c80f43e691a31da73ccf17fd4bcc6b00d3a5331f26b9294e294e1538`
- Unchanged profile SHA-256: `fb842649d30e5876fb3f299e890e2c555a88be759c29b2c6577552d4885b0226`

PROPOSED_R11_BINDING.json preserves the current predecessor authority/content bindings. The proposed append-only amendment derives the new effective operational/release identities above without rewriting that proposal. The original Run-2 dispatch remains `E1-ARCHITECT-DISPATCH-sha256:e20ee636c728511681bf45513147e0087ef86598b0454e90c28f5b7184468758`. The exact ordered r8/r9/r10 audit pins are in the proposal; the fresh namespace is `/tmp/kge-forge-e1-evidence/auth-e1-wp-001-r11-4dae6644072f42c0b4ffd00be7e80a5d/session-e1-run2-r11-4dae6644072f42c0/turn-e1-run2-r11-b4ffd00be7e80a5d/controller.jsonl`. Neither that file nor its invocation directory exists.

The **currently applied** release remains `E1-RELEASE-AUTHORITY-sha256:c9b00cdf029e657936ba3e51fa8a3c9361e315483eeda58e428aff5f1c3b6d3c` with OperationalContextId `E1-OPERATIONAL-CONTEXT-sha256:109c1fb95fee2e95f58cce8ca7723384092706fa33a4ef7ec051abfdcacea125`. No candidate amendment or continuation has been applied. CURRENT_PIN.json selects only a QUALIFIED_PREPARED store; the existing applied production pin is unchanged.

## S3, history and stop point

The genuine host check and independent final reconstruction retain exact S3 `SupervisorInstance-sha256:83f22718a56ab733257208c6e1dfe9767a95e0d10b82f8583f222f88ee9669a2` through succession `SupervisorSuccession-sha256:b86bbb15d9d9d468b2de87926ad6b1cb4063218fd71eb5426089f689c0aecce8`. PID 1465900, parent 1465890 and socket inode 4203637 remain matched by the qualified readiness verifier, including process birth, implementation, cgroup, workspace, socket and exclusivity. No replacement supervisor or host launch occurred.

r8 stays unissued with its closed namespace; r9 and r10 stay CANCELLED / INTERRUPTED_NO_EFFECTS. 106 historical files, including the shared ownership ledger, remain byte-identical to the opening baseline. r10 remains ownership RELEASED, ExecutionScope NONE and QUIESCENT. Run-1 evidence is unchanged.

**Zero real r11 model requests, ActionRequests, executions, repository/knowledge changes or implementation effects. No r11 issuance, activation, ownership acquisition or dispatch.** The only effecting invocations in qualification are isolated synthetic non-E1 fixtures. Stop for the Architect's exact material/adoption/issuance decision. No Experiment 1 PASS or v0.1 completion is asserted.
