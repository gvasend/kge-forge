# Exact runtime-authority bootstrap application

`BLOCKED_R1_ORDINARY_VALIDATOR_CONSUMPTION`

The specifically authorized bootstrap is durably APPLIED. Independent reconstruction establishes R1 as the unique current runtime. The lineage is consumed and must not bootstrap again. R0 is historical only; r8–r12 retain their historical runtime bindings.

The initial private-store materialization failed before calling the bootstrap: two aliases copied from the qualification catalog collided with the production aliases. The failed staging directory is preserved. Corrected provisioning omitted only those two copied aliases and installed the exact authorized aliases using the materializer. Both journals were verified empty before proceeding. No bootstrap intent or head transition existed before the correction. The qualified bootstrap operation was invoked once and committed one transition. See PROVISIONING_FAILURE.json.

All exact artifact, private object, consumer inventory, R0/C1/R1 byte and predecessor checks passed. The pinned independent legacy verifier reconstructed current release/context, CANCELLED r12, no ownership and no ExecutionScope. Genuine S3 checks preceded and followed staging. The applied bootstrap journal contains INTENT → COMMITTED → RECORDED; the runtime journal contains adoption INTENT → HEAD_COMMITTED → RECORDED. All writes used the qualified typed operations. Replay remains rejected by the consumed-lineage gate.

## Independent result

- Applied bootstrap: `RUNTIME-AUTHORITY-BOOTSTRAP-sha256:7837030f70d5545b8ba3ac466317b5b7b15e29950bf0056a1d5eeaeda23b1239`
- Bootstrap file SHA-256: `84f838bf3c655f75e75b8f4532081c3e5d4c9e532d7b6fb6776a98c7b9b688c6`
- Applied material amendment: `RUNTIME-CONSUMPTION-AMENDMENT-sha256:dcce6338e15f0691c6487be9641129331f93d2599b09a378f7bff9f818d80e9d`
- Runtime-head authority: `RUNTIME-HEAD-AUTHORITY-sha256:75e6b7f2b5867c6d04bf0eeefc66f0c148d3f3e15e776c0d9e2b20b6352a1a5d`
- Preserved/adopted C1: `CONTINUATION-sha256:b9476d2017ea8528a6d22759c0c692481fd4234d7e360a744c160e013ca69cea`
- Runtime continuation envelope: `IMPLEMENTATION-RUNTIME-CONTINUATION-sha256:c936760b7d97e13c7fd8131c39b7aee9e5de1b006a9b64aaf9674a48c94736d6`
- Historical R0: `sha256:5c8cfcffc7a994aa17d1222184113f017b9afa237f25c32e06015491f485b97c`
- Current R1: `sha256:1b31ac92d38952444076e3997083cf035e0862f1bc0182261826d6690ec31c15`
- Runtime ancestry head: `RUNTIME-ADOPTION-EVENT-sha256:aa914837c69eb4ca9202e817a9de35f4065d3d56be8d237f828477d38227f9fd`
- Resulting release authority: `E1-RELEASE-AUTHORITY-sha256:d1d66c1f11789bbdf70b23bd49127fb8b5d04a91296ec4aa396e131ea2b4462e`
- Runtime-authority OperationalContextId: `E1-OPERATIONAL-CONTEXT-sha256:0f99f592753bcf614262ee379c8d6a19f7d0af5ae57d8eef212596df496f2b19`
- Runtime-authority chain digest: `97fb6671ba27feb502db32a00d93ccae9be1a7898fc6987a035e7daadcc75b53`

These are reconstructed runtime-authority identities. They are not represented as an issued invocation or a successfully integrated ordinary model-context projection. No r13 context/authorization was created.

Bootstrap application took **29.099s**. Independent runtime/head/S3 reconstruction took **5.400s**. Fresh runtime-head verification samples were **0.900 / 0.893 / 0.860s**. S3 verification remained PASS for `SupervisorInstance-sha256:83f22718a56ab733257208c6e1dfe9767a95e0d10b82f8583f222f88ee9669a2`. Budgets and substantive-progress semantics were unchanged.

## Production integration blocker

Actual R1 bytes match the adopted runtime head. However, its frozen `attempt_chain.py` (SHA-256 `e8a4087a769298cbc8e72e0f7b91ec9c8dbef50c841cbf029faf714751d20d31`, decision entry line 133) has no runtime-head-consumption branch. It still checks the implementation selected by the legacy attempt amendment.

The runtime-aware branch exists in the separately authorized bootstrap-consumer implementation (`attempt_chain.py` SHA-256 `c426e182ae189135506b27cd12f2abc2d79275147cab8c5b86fab266ca6c16f3`). The new head verifier correctly rejects that consumer root when offered as current R1: `unaccounted runtime`. These are different inventories. Bootstrap authority permits the bounded transition; it does not silently make that entire consumer bundle the executing R1 controller.

A read-only historical-context probe also correctly rejected reconstructing r12 through R1. That negative is explicitly evidence of historical-binding preservation, not an attempted new invocation and not a complete new-context production test.

Completing ordinary controller consumption requires an exact qualified ordinary implementation continuation from R1; replacing files under R1 would invalidate its authorized identity. No second bootstrap is required or permitted. No such continuation was manufactured or adopted in this step.

The ordinary continuation tests demonstrated two preselected synthetic successors without reusing bootstrap. They do not prove production acceptance of a future, previously-unlisted grant: the applied head policy currently pins only C1. Extension/consumption of a subsequent explicit Architect grant must be addressed and qualified in the ordinary mechanism without reusing bootstrap. This limitation is not hidden behind the earlier synthetic PASS.

Complete ordinary production context/projection, live-status integration and fresh preparation→MODEL_REQUEST_READY performance are therefore NOT ESTABLISHED. No cold/warm pre-model timing is claimed; the earlier 104–105s measurements were not reused. Readiness is withheld.

## Preservation and effects

Fresh semantic classification accepts r12 as ACTIVE_CANCELLED_PRE_MODEL_NO_EFFECTS. Its immutable audit hash matches; all 227 historical files and the real ownership ledger match prior fingerprints. No historical invocation was rebound to R1. No active invocation, real ownership reservation, r13, real model request, Programmer action or E1 repository/knowledge/implementation effect was created. The authorized runtime-authority adoption is the sole production authority transition made here.
