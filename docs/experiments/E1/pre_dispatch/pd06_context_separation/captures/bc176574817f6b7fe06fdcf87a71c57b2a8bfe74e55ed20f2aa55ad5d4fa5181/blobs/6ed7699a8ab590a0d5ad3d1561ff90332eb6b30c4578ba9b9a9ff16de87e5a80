# PD-06 controller/model context separation — 2026-09-16

**Scoped qualification PASS. Final PD-06 technical verification is recorded in PD06_VERIFICATION.json.** Actual PD-06 remains UNRELEASED, E1 INACTIVE, E1-WP-001 INELIGIBLE and UNDISPATCHED. No Architect release decision is made.

## Separate authority and projection

The controller retains the full committed context binding, historical immutable 186-input capture, accepted clearance and explicitly attributed current implementation/authority supplement. FullContextDigest hashes the canonical full binding representation: capture identity, clearance identity, committed manifest/capture identity, full controller context and current material-input fingerprints. AuthoritativeContextId names that digest. ModelProjectionDigest independently hashes the deterministic selected payload and per-item provenance, attributed to the authoritative context and accepted clearance.

The immutable source capture is historical authority, not a claim that its old controller implementation and append-only audit bytes are current. IMPLEMENTATION_SUPPLEMENT.json attributes current adapter changes and qualified audit additions to this instruction; full committed E1 sources and all six TRANSMIT source bytes remain unchanged. Current implementation bytes are independently pinned and checked. Mutable lifecycle/audit state is still governed by the existing action, recovery and common-ownership mechanisms; it is not silently sent as reasoning context.

Projection provenance stays controller-local: each item records authoritative source identity, captured source hash, exact cleared byte ranges, accepted clearance entry/index/digest and projection-content digest. The model receives only the exact task and cleared text selections, with their approved source/selection labels. It does not receive full-context/projection provenance hashes, gate state, recovery evidence or the controller context object. Already-qualified tool schemas and constant protocol/redaction scaffolding are retained.

Before every model request, after each model response and before each action, the controller verifies committed governance, current implementation inputs, immutable capture and clearance bytes, deterministic projection, session/turn/authorization identity and consistency between transmission policy and accepted clearance. Action authorization remains with the registered dispatcher. Every continuation rebuilds/re-filters all previous local tool results under the currently verified policy. A model-supplied summary, projection, authority change or substituted context is not accepted.

Reconstruction uses the exact persisted authorization containing the immutable context/projection specification. The qualified audit-recovery check rejects changed bindings; a fresh CommittedContext and projection are reconstructed and verified locally. This is recovery of governance/projection identity, not a claim to durable replay of model reasoning transcripts. Historical private audit contents never enter the model payload.

## Identities

- AuthoritativeContextId: `E1-AUTHORITATIVE-CONTEXT-sha256:cb8782e9337fc2891653e285799f34824accf869e501fdfdec93911eeb53fddd`
- FullContextDigest: `cb8782e9337fc2891653e285799f34824accf869e501fdfdec93911eeb53fddd`
- ModelProjectionDigest: `0a3d0d0e37decdf571b143924181d344ccf7cbe761341ceebc13901582fe1f47`

## Exact six-source projection inventory

- `/home/gvasend/app/kge-forge/docs/EXPERIMENT_1_ARCHITECTURE.md` — BOUNDED_CONTENT; D-01 [bytes 3002,3232), D-02 [bytes 3232,3443), D-03 [bytes 3443,3634), Sections 3-5 [bytes 6594,14340). Source SHA-256 `951fb5736a7a16093ed5d995293496f8a2e18b1cca45f52e9f3c5be38f699ca8`.
- `/home/gvasend/app/kge-forge/docs/EXPERIMENT_1_REQUIREMENTS_SYNTHESIS.md` — BOUNDED_CONTENT; F-01 [bytes 820,989), F-02 [bytes 989,1190), F-03 [bytes 1190,1419), F-04 [bytes 1419,1637), F-05 [bytes 1637,1865), F-06 [bytes 1865,2096), F-07 [bytes 2096,2297), F-08 [bytes 2297,2496), F-09 [bytes 2496,2683), F-10 [bytes 2683,2891), F-11 [bytes 2891,3088), A-13 [bytes 9927,10128), A-14 [bytes 10128,10337), A-15 [bytes 10337,10553). Source SHA-256 `6fe78c3a27507dfe0d36012d5a878ed107780e6bc1fcef53b70c62f60084a8b2`.
- `/home/gvasend/app/kge-forge/docs/experiments/E1/pre_dispatch/CONTEXT_PROTOCOL.md` — COMPLETE_FILE; complete captured file [bytes 0,3665). Source SHA-256 `435577085269686749de022f1ddf2d28f6380c8ff6c5478e1dfd8e7d856ddb37`.
- `/home/gvasend/app/kge-forge/docs/experiments/E1/pre_dispatch/DECISIONS.md` — BOUNDED_CONTENT; PD-04 tooling only [bytes 2077,2537). Source SHA-256 `026c689de2012f914ea2d572a31f17a703cef37d3ae096256606a183a58a6e3e`.
- `/home/gvasend/app/kge-forge/docs/experiments/E1/pre_dispatch/E1-WP-001.md` — COMPLETE_FILE; complete captured file [bytes 0,9278). Source SHA-256 `1d0c276f2e0e818b89c128bfd6185cfa21968374d9868db833500e1e283c774c`.
- `/home/gvasend/app/kge-forge/docs/experiments/E1/pre_dispatch/pd06_release_evidence/PROPOSED_PRODUCTION_PROFILE.json` — BOUNDED_CONTENT; runtime argv/cwd/inputs/environment/network/shell [bytes 288,819), exact committed acceptance input identity [bytes 1370,1663). Source SHA-256 `158fc81437ef2e36d9f5a03fe7f322e4fb8905d6bd7acf29e837172e0729a5b1`.

The accepted manifest is unchanged: 6 TRANSMIT, 120 LOCAL_ONLY, 60 NEVER_TRANSMIT. Bounded entries do not clear their remaining bytes. Only task/protocol complete-file read results remain eligible for transmission; bounded governing/test excerpts enter through the initial deterministic projection. All other result bodies and outcomes remain redacted. Future implementation files/test diagnostics acquire no automatic clearance.

## Twelve qualification properties

| Property | Result / evidence |
|---|---|
| Full governance retained locally | PASS — committed synthetic gate/state remains in controller binding |
| Only cleared model projection | PASS — recorded requests contain task/public selections only |
| Iterative reasoning completes | PASS — read, redaction, governed denial and finish through registered dispatcher |
| LOCAL_ONLY absent | PASS — local content and gate markers absent from every recorded model request |
| NEVER_TRANSMIT absent | PASS — private marker absent from every recorded model request |
| Local governance denies action privately | PASS — attempted protected governing write denied without disclosing its content/state |
| Transmitted-source change | PASS — changed public source blocks before another request/action |
| Local-only governing-source change | PASS — unchanged selected content does not rescue stale full governance |
| Clearance change | PASS — exact manifest-byte change fails closed |
| Tool-result filtering | PASS — local/private reads, status/errors/hashes/alternate results redacted; contradictory policy rejected |
| QUIESCENT/sequential gating | PASS — live synthetic execution emits no terminal result or next model request while populated; overlapping execution denied |
| Recovery/restart identity | PASS — reconstruction from durable authorization restores exact full/projection IDs; altered binding rejected |

`synthetic/REPORT.json` contains model payloads, private controller evidence, denial results and stale probes. `live/LIVE_REPORT.json` records two synthetic governed executions through the new loop and the unchanged production supervisor/runtime path, kernel population, closed admission, QUIESCENT ordering and cleared ownership. Both use synthetic committed context/acceptance inputs; there is no actual E1 implementation or actual model/API call. COMMITTED_FIXTURE.json files preserve verified synthetic commit/tree/blob objects for later retrieval.

Focused regression: 22 tests passed, covering only context binding/projection, continuations, transmission, stale sources, recovery and affected execution invariants. Earlier PD-05/A2 evidence remains accepted and is not rerun wholesale. Exact final source fingerprints are in SOURCE_SHA256.json. No read/write grant, execution argv/cwd/input/environment, network prohibition, ownership rule or transport destination was broadened.

## PD-06 reconstruction and verification

The R6 profile/launch records bind the exact E1 task, accepted clearance, current qualified controller implementation, deterministic projection and existing production transport/execution settings. Independent verification reconstructs every projected byte range without calling the implementation's derive routine; checks identities, profile/launch fields, all 186 classified input representations, provisioning receipt/directories, current binaries/transport, scope closure, ownership, outside-grant audits, and actual E1 inactivity. All eight non-status registered E1 requests remain denied and non-effecting. E1 has no recorded supervisor scope/admission and no product files have been created. These facts rely on the previously accepted host/controller/audit integrity assumptions.

The new content-addressed capture includes historical authority bytes, accepted clearance, current implementation and instruction supplement, qualification/recovery/live evidence, exact profile/launch/projection, provisioning, PD-05 PASS, independent verification and relevant prior anomaly/limitation records. SHA-256 verification re-reads authoritative current inputs and stored blobs. It is read-only content-addressed storage, not a privileged write-once guarantee. HEAD plus exact working-source fingerprints identify uncommitted qualified changes; they are not falsely described as a Git commit.

Remaining inherited limits: no actual production model/API/E1 task was run; model transcript persistence and general timing-channel noninterference are not claimed; the existing bounded execution-output/timeout and loose-Git-object limits remain. None of those previously recorded limits is silently weakened. No new material authority/enforcement gap is identified by this scoped qualification.

**Proposal for the Architect: E1-B01 PASS; E1-WP-001 eligible only upon the reserved Architect PD-06 release. Actual PD-06 UNRELEASED, E1 INACTIVE, E1-WP-001 INELIGIBLE and UNDISPATCHED.**
