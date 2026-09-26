# Integrated production activation qualification — 2026-09-16

Qualification: **PASS**. Applicability assessment: **NON_MATERIAL_IMPLEMENTATION_CONTINUATION**.

The original five-file lifecycle change preserves released authority when integrated with the qualified transaction and ownership enforcement. Completing the chain required two explicit production dependencies: new `adapter/activation_transaction.py` and changes to `adapter/invocation_ownership.py`. They are part of this assessment, not an unreported change outside the five-file comparison. [DELTA_INVENTORY.json](DELTA_INVENTORY.json) records all previous/current hashes; [EXACT_PRODUCTION_DELTA.patch](EXACT_PRODUCTION_DELTA.patch) contains the complete production delta against the operational predecessor.

This is an implementation-applicability recommendation, not an Architect continuation adoption, release, rebind, activation, or dispatch decision.

## Production operation and ordering

`adapter.activation_transaction.validate_production` verifies facts from the immutable dispatch record, released profile/launch, capture, release decision, authoritative context, clearance and continuation chain, then current provisioning, supervisor process/socket/cgroups, audit and common ledger. It does not accept a caller-provided PASS checklist. Missing sources/configuration or mismatches deny. Production requirements are derived from existing released fields; no new dispatch-record field is needed.

The transaction obtains the exclusive controller fence, locks the common ledger and controller audit, performs validation, fsyncs its receipt, fsyncs activation intent, fsyncs the invocation reservation, then fsyncs ACTIVE bound to the intent/validation/reservation. Recovery must independently reconstruct ACTIVE plus that exact reservation. A process-bound live controller lock is also required; identifiers or an ACTIVE audit event alone are insufficient. Profile attachment and every model continuation revalidate the bindings. Governed tool calls and execution admission also verify owned lifecycle state. Per-scope execution reservations remain nested under invocation ownership.

The controller fence is `<common ownership ledger>.controller-lock`; it conveys no Programmer filesystem authority. It remains controller-local. No real E1 fence was created. Same trusted-controller/local-filesystem flock/fsync assumptions apply; a hostile privileged host is not newly claimed to be contained.

Validation identity: `DISPATCH-VALIDATION-sha256:5c52c50c24b53e32fa071cd973ea839f628cabf409748f2913da6704359e3d04`.

Synthetic activation event: `E1-AUTHORIZATION-LIFECYCLE-sha256:4c34837138ed6d760523fabcb663c6a56909f53dd76845622c73abfd44725c9a`.

Synthetic ownership reservation: `INVOCATION-RESERVATION-sha256:0d86c6a25ee88f13b9e6f5843c5fc10ab9752b39008cc2c74186b2d75e8ac9e1`.

Synthetic task: `G5-NON-IMPLEMENTATION`; authorization: `projection-fixture`. The fixture uses committed synthetic repositories and the same production validator, lifecycle, ownership, dispatcher, snapshot, supervisor, kernel scope and terminal-audit components. No E1 work-package inputs were executed. The Responses call was a recording stub; no API request was sent.

## Integrated evidence

[synthetic/live/LIVE_REPORT.json](synthetic/live/LIVE_REPORT.json) preserves the activation receipt/event/reservation, independent-process restart, independent competing-controller denial, all model request payloads, execution result, kernel observations, supervisor events and terminal reconstruction.

- Restart before activation: INACTIVE; handoff denied.
- Restart in a fresh Python process after durable ACTIVE: exact ACTIVE+OWNED reconstructed; handoff eligible only after acquiring the live controller fence and revalidation.
- Competing process: activation and recovery denied by the live fence. Another host with identical ACTIVE authorization but no transaction could not obtain handoff or a scope reservation. There was one effective activation event and no competing scope.
- Bounded execution: `scope-ff87e97308c64bc2af388b803384bd07`. Authoritative supervisor admission recorded the exact session/authorization/action owner.
- While scope was CLOSED but populated, only one model request existed and no terminal execution result had been emitted. A second execution was denied. Observed event indexes: `{"action_result": 30, "execution_result_available": 22, "execution_scope_closed": 23, "execution_scope_quiescent": 28}`.
- Kernel population reached zero before QUIESCENT and terminal ActionResult. The successful bounded execution used the released-shaped argv/environment/snapshot mechanisms; the fixture proved readonly committed inputs and denied payload network access.
- Finish ActionResult, final reasoning response, durable COMPLETED lifecycle, then invocation release occurred through the production terminal path. Independent process restart reconstructed COMPLETED with no owner and handoff denied.
- Recorded model requests contain no synthetic LOCAL_ONLY, NEVER_TRANSMIT or local release-decision marker. The local read result passed through production transmission filtering.

## Failure boundaries

[FAILURE_BOUNDARIES.json](FAILURE_BOUNDARIES.json) and its archived fixture audits/ledgers preserve the individual facts. Fault injection interrupts actual production writes; it does not replace the production validator.

| Boundary | Durable outcome and recovery | Handoff |
|---|---|---|
| Validation failure / changed task | Original INACTIVE audit unchanged; no reservation or activation event | DENIED |
| After validation, before intent | Durable validation receipt only; `VALIDATED_NOT_ACTIVATED`, INACTIVE | DENIED |
| After intent, before ownership / ownership-write failure | INACTIVE intent; `ACTIVATION_PENDING`; no owner; explicit reconciliation, no automatic retry | DENIED |
| Ownership acquisition denied by controller fence | Original INACTIVE state; no competing reservation/event | DENIED |
| Ownership acquired, before ACTIVE | INACTIVE plus owned intent; `OWNERSHIP_HELD_ACTIVATION_INCOMPLETE`; retain uncertainty and reconcile | DENIED |
| ACTIVE committed, before handoff | ACTIVE plus exact reservation survives restart; no model call occurred before recovery | ELIGIBLE after owned recovery and validation |
| Ledger unavailable | Cannot reconstruct authoritative ownership; no activation | DENIED |
| Governing context stale after ACTIVE | Durable historical event remains; current release/context revalidation fails | DENIED |
| ACTIVE with missing ownership | Contradictory combined state; recovery fails closed | DENIED |
| Truncated ownership history | Incomplete durable evidence; no permission inferred | DENIED |
| Competing controller | Cannot acquire live fence, duplicate transition, model eligibility, or competing execution scope | DENIED |

Failure fixtures are isolated under synthetic `/tmp` ledgers. Pending/contradictory records were retained as evidence, not silently reset or retried. No real E1 ownership record was touched.

## Focused regressions and authority comparison

34 targeted tests passed in [TARGETED_REGRESSIONS.txt](TARGETED_REGRESSIONS.txt). After ledger identity hardening, 18 lifecycle/ownership tests passed in [FINAL_RESOURCE_IDENTITY_REGRESSIONS.txt](FINAL_RESOURCE_IDENTITY_REGRESSIONS.txt), and the final live transaction passed on those exact source bytes. [TRANSMISSION_REGRESSION.txt](TRANSMISSION_REGRESSION.txt) records the synthetic transmission/provisioning regression. An initial legacy test attempted to load superseded E1 decision bytes and failed stale-context detection; substituting synthetic acceptance inputs (not changing enforcement) passed. The real governing decision was not changed.

[UNCHANGED_ENFORCEMENT_AST.json](UNCHANGED_ENFORCEMENT_AST.json) verifies 13 unchanged enforcement/schema bodies. [APPLICABILITY_ASSESSMENT.json](APPLICABILITY_ASSESSMENT.json) compares all 18 released invariants individually. The registered tools, result schemas, filesystem grants, write/patch promotion, executable/argv/cwd/input authority, environment, network prohibition, model transmission and destinations remain unchanged. The changed admission/recovery/terminal implementation now denies unowned ACTIVE usage and records invocation completion durably. It introduces controller-local audit/ownership effects only, not a new Programmer capability or external effect destination.

## Proposed continuation — not applied

[PROPOSED_IMPLEMENTATION_CONTINUATION.json](PROPOSED_IMPLEMENTATION_CONTINUATION.json) and [PROPOSED_CONTINUATION_EVENT.json](PROPOSED_CONTINUATION_EVENT.json) bind the immutable release/dispatch ancestry, existing authorization, complete implementation hashes and qualification evidence.

- Proposed OperationalContextId: `E1-OPERATIONAL-CONTEXT-sha256:118489f2d87c7eb207e38927706f4eaab1b31f42347474a7d0cee59e005c7f2c`
- Proposed chain digest: `dd5b16f6acc76c5f4aefd4863b8c15cd47943bb6f47aa34dbbffa862f1c03e05`
- Proposed FullContextDigest: `bce720131300f61c713836c9a794e682e526393ea946dc937f558307a6620e48`
- Proposed ModelProjectionDigest: `8d0d91a29131626b7cd91de41b69e825c0621c9eff501f6c3a51a48f9cccbdf9`
- Historical released profile fingerprint, unchanged: `b9e7f72d97525f39fbddfe92f276ab6aedd057ef6c5b7284dc163f1db9c9c328`
- Model payload hash, unchanged: `5847a9c8ffe36c9e8fa69d53006eebf2a8b39f667a05ade222d045822e7dfc95`

These are deterministic **proposal identities**, not current effective E1 bindings. The six released sources and cleared ranges remain byte-identical ([RELEASED_PAYLOAD_PRESERVATION.json](RELEASED_PAYLOAD_PRESERVATION.json)); projection metadata would change to identify the implementation continuation, while transmitted content would not.

The current governance verifier accepts source-append continuations only and intentionally will not accept this proposed implementation-replacement member. Any later authorized adoption must validate that member and its relationship to the immutable dispatch ancestor. That rebinding was neither implemented nor applied by this qualification. The existing dispatch record still pins its historical operational identity; it was not regenerated or silently made to accept new fingerprints.

## Preserved real E1 state

[PRESERVATION_VERIFICATION.json](PRESERVATION_VERIFICATION.json) verifies immutable release/profile/launch/clearance/dispatch/continuation references and the unchanged historical audit SHA-256. The real common ownership ledger is empty and no E1 controller fence exists.

**PD-06 RELEASED; E1-B01 PASS; E1 INACTIVE; E1-WP-001 INELIGIBLE and UNDISPATCHED.** No E1 activation event, ownership acquisition, model request, implementation effect, or new Architect dispatch authorization occurred.
