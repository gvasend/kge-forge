# PD-06 final content-clearance and capture verification — 2026-09-16

Classification is complete: **6 TRANSMIT, 120 LOCAL_ONLY, 60 NEVER_TRANSMIT** out of the existing 186 inputs. No source is cleared merely because it is readable. Four TRANSMIT inputs are bounded; their unselected bytes retain an explicit exclusion. Only the exact task and context protocol are complete-file clearances.

## Exact TRANSMIT inventory

### /home/gvasend/app/kge-forge/docs/EXPERIMENT_1_ARCHITECTURE.md

Captured source SHA-256: `951fb5736a7a16093ed5d995293496f8a2e18b1cca45f52e9f3c5be38f699ca8`.

BOUNDED_CONTENT: D-01 (bytes 3002–3232, end exclusive), D-02 (bytes 3232–3443, end exclusive), D-03 (bytes 3443–3634, end exclusive), Sections 3-5 (bytes 6594–14340, end exclusive).

E1-WP-001 explicitly governed by D-01 through D-03 and architecture sections 3-5; section 4 contains the AR-04/AR-05 corrections, so separate review evidence is unnecessary.

### /home/gvasend/app/kge-forge/docs/EXPERIMENT_1_REQUIREMENTS_SYNTHESIS.md

Captured source SHA-256: `6fe78c3a27507dfe0d36012d5a878ed107780e6bc1fcef53b70c62f60084a8b2`.

BOUNDED_CONTENT: F-01 (bytes 820–989, end exclusive), F-02 (bytes 989–1190, end exclusive), F-03 (bytes 1190–1419, end exclusive), F-04 (bytes 1419–1637, end exclusive), F-05 (bytes 1637–1865, end exclusive), F-06 (bytes 1865–2096, end exclusive), F-07 (bytes 2096–2297, end exclusive), F-08 (bytes 2297–2496, end exclusive), F-09 (bytes 2496–2683, end exclusive), F-10 (bytes 2683–2891, end exclusive), F-11 (bytes 2891–3088, end exclusive), A-13 (bytes 9927–10128, end exclusive), A-14 (bytes 10128–10337, end exclusive), A-15 (bytes 10337–10553, end exclusive).

E1-WP-001 names F-01 through F-11 and bounded A-13 through A-15 obligations; service-only requirements and unrelated review findings excluded.

### /home/gvasend/app/kge-forge/docs/experiments/E1/pre_dispatch/CONTEXT_PROTOCOL.md

Captured source SHA-256: `435577085269686749de022f1ddf2d28f6380c8ff6c5478e1dfd8e7d856ddb37`.

COMPLETE_FILE: complete captured file (bytes 0–3665, end exclusive).

E1-WP-001 explicitly names this input contract; all fields, provenance, error and gate semantics are needed to implement the validator.

### /home/gvasend/app/kge-forge/docs/experiments/E1/pre_dispatch/DECISIONS.md

Captured source SHA-256: `026c689de2012f914ea2d572a31f17a703cef37d3ae096256606a183a58a6e3e`.

BOUNDED_CONTENT: PD-04 tooling only (bytes 2077–2537, end exclusive).

PD-04 supplies the selected Python 3.8.10/stdlib compatibility obligation; other preparation/gate/publication decisions are not needed as model content.

### /home/gvasend/app/kge-forge/docs/experiments/E1/pre_dispatch/E1-WP-001.md

Captured source SHA-256: `1d0c276f2e0e818b89c128bfd6185cfa21968374d9868db833500e1e283c774c`.

COMPLETE_FILE: complete captured file (bytes 0–9278, end exclusive).

Exact production task expressly selected; includes all implementation, acceptance, stop and result obligations.

### /home/gvasend/app/kge-forge/docs/experiments/E1/pre_dispatch/pd06_release_evidence/PROPOSED_PRODUCTION_PROFILE.json

Captured source SHA-256: `158fc81437ef2e36d9f5a03fe7f322e4fb8905d6bd7acf29e837172e0729a5b1`.

BOUNDED_CONTENT: runtime argv/cwd/inputs/environment/network/shell (bytes 288–819, end exclusive), exact committed acceptance input identity (bytes 1370–1663, end exclusive).

Explicitly released test context: exact argv, cwd, input list, environment, shell/network posture and committed acceptance identity needed to invoke the authorized test and real-context acceptance case. All binary/host-control/ledger/audit/identity/gate/transport fields excluded.

## Exclusions and enforcement

LOCAL_ONLY comprises unrelated service/vision/governing material, adapter implementation and test evidence, architectural and qualification reviews, gate/release/provisioning records, and other nonessential evidence. NEVER_TRANSMIT comprises outside-read-grant runtime/host inputs and private controller, raw audit, snapshot, authorization, identity and execution state. Credentials were not accessed or included. Hidden paths remain prohibited; none were added to the capture universe. The manifest attributes every input individually.

Exact complete-file read results are permitted only for the task and protocol. The four bounded sources are supplied only as captured excerpts in the proposed initial context; their complete read results are redacted. All read results for the 180 excluded sources and all list/search/status/exec/write/patch/finish/expansion result bodies are redacted. Hash/error/echo representations are withheld. A changed task or changed approved file content fails the exact digest check. Raw model continuation never receives a local result directly. These checks evaluate the selected policy controller-side while E1 stays INACTIVE; they do not call a model or execute E1 tools.

The policy replaces the old coarse pre_dispatch evidence-directory exclusion with exact source exclusions so the specifically cleared task/protocol can pass without declaring the entire directory transmittable. No sibling receives clearance. Initial payload clearance is exact-content-bound. The clearances are instructions for a proposed launch, not activation authority.

## Failed prerequisite: qualified context compatibility

The unchanged `ResponsesReasoning.run` requires `context == binding.model_context()` before the first request. The binding emits mandatory evidence identities, knowledge/gate assessments, prerequisites and unresolved controller dispatch state. Those fields are not cleared under the Architect selection. The selected minimum context is different, and the current implementation has no configurable projection.

Independent checks establish both sides: the minimum payload is permitted by the new transmission policy but fails the loop's equality requirement; the loop's mandatory full controller context fails the new transmission policy. E1 was never activated to demonstrate this: the source guard, exact context values and their hashes suffice. `CONTEXT_COMPATIBILITY_FAILURE.json` records the evidence.

This is no longer an unresolved content-selection question. Making the selection usable requires a separately scoped controller context-projection change, preserving the full committed binding for local governance while supplying only approved excerpts to the model, with focused regression evidence. No adapter implementation was changed to force release. The captured task remains byte-identical, including its historical prepared/not-dispatchable wording.

## Verification and disposition

`VERIFICATION.json` records each final prerequisite. Fingerprints, provisioning, exact task identity, classification completeness, necessity/read-authority checks, final-policy exclusion checks, unchanged execution/transport grants, scope/ownership, audit isolation and inactivity are independently checked. Private audit-directory modes are explicitly set to the already-selected 0700 policy; no host environment default supplies this configuration. The real product directories remain empty, there is no initializer, the E1 ledger has no reservation, and no E1 supervisor scope/admission is recorded. These claims rely on the previously accepted controller/audit integrity assumptions.

The final evidence capture includes all 186 original inputs plus the new Architect selections, clearance manifest, exact proposed task/context/profile/launch, offline policy probes, independent verification, current HEAD and unchanged qualified adapter source inventory. It also binds the prior candidate and its provisioning, PD-05 PASS, anomaly and limitation evidence. New release-machinery artifacts are local; derived task/context files inherit only their selected captured source bytes, not independent authority. All original files and adapter sources remain unchanged.

The capture is a new **unreleased final evidence snapshot**, not a final release record. Fingerprints and identifiers are in `CAPTURE_REFERENCE.json`; stored bytes are content-addressed and read-only, not claimed to be privileged write-once storage. Actual material changes require recapture.

**PD-06 prerequisite verification FAILS on context compatibility. No final release record is prepared. Proposed E1-B01: BLOCKED. Proposed E1-WP-001 eligibility: INELIGIBLE. Actual E1: INACTIVE; RELEASED=false; ELIGIBLE=false; DISPATCHED=false. The final Architect release decision remains reserved.**
