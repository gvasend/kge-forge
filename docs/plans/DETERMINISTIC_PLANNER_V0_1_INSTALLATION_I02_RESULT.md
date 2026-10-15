# Deterministic Planner v0.1 — INSTALLATION-I02 result

**RESULT = PASS** for the bounded generic INSTALL/REPLACE capability and the explicitly authorized P04 route replacement. **P04 execution readiness remains NO.** No A09–A13 operation or E2-FINISH execution occurred.

The new [native post-route-install bundle](DETERMINISTIC_PLANNER_V0_1_E2_P04_POST_ROUTE_INSTALL_BUNDLE_1.json) extends the exact published P03 prospective lineage by one ordinary `INSTALL_DEFINITION` event at sequence 3. The original P03 bundle and both of its events remain byte-identical. No historical definition, qualification record or frozen-E1 artifact was rewritten. Detailed evidence is in the [machine companion](DETERMINISTIC_PLANNER_V0_1_INSTALLATION_I02_RESULT.json) and [qualification directory](qualification/INSTALLATION_I02_1/).

## Authorization and identities

The authenticated human selection is `AUTHORIZE_P04_ROUTE_REPLACEMENT`. I01 named its authorize option `AUTHORIZE_P04_ROUTE_INSTALLATION`, but its exact decision subject and effect expressly define REPLACE. The [capture](qualification/INSTALLATION_I02_1/human-replacement-authorization.json) records this equivalence without changing any authorized term. I01 bytes, descriptor/content identity, old baseline reference, policy, context and ordinary parent were independently verified before application. The trusted authority-admission interface takes expected grant/decision/issuer anchors outside the untrusted command. It emits an immutable pinned receipt; no cryptographic human signature or unrelated authority is claimed.

The separately admitted INSTALL grant permits only this exact REPLACE, tick 0–100, one use, no delegation or lifecycle execution. Its accepted receipt embeds the exact issued grant and trust bindings. One installed record provides the canonical use witness; retries consume no additional use.

| Identity domain | SHA-256 |
|---|---|
| INSTALL authority (`AUTHORITY_IDENTITY / planner-install-authority-v1`) | `66570262d49eb55ac4e49638b33ad901e7b6c2f4723c083827ad4f24e0b1e75b` |
| Authorized definition (`CONTENT_IDENTITY / planner-installable-definition-v1`) | `1de38b5278463e9c55b656af1c765fe8952cdadc7bf53d4322eb32f7deb5a970` |
| Canonical native body (`CONTENT_IDENTITY / raw-file-sha256`) | `bb528a253ed466ff2fce89cadfdd6a1b0cdab41458651230d733f7455aba2567` |
| Installed instance (`INSTANCE_IDENTITY / planner-installed-definition-v1`) | `24df303e02168de2441d77bea08787566bb9b2419e80804c0029e2e5b71679da` |
| INSTALL event (`CONTENT_IDENTITY / planner-event-v1`) | `a19b52ab601c6d3c7668b78c6e20cc87e54cfc317595e4da641fcbb7d107fb1e` |
| Post-install Snapshot (`CONTENT_IDENTITY / planner-snapshot-v1`) | `99e47ad1e462c30cd33e2258e4c74ff670164fa7378e5a998e0f23b9256e4454` |
| Post-install native bundle (`CONTENT_IDENTITY / planner-bundle-v1`) | `885b23b6f64503153d2d6c4419b160cc278112b26238eecbab14c8b9ecb92ee4` |

The parent remains the original head `9f00d563a015969d02179c7a991d2efec97b763448fbc27c34e7bd634d36a728`. The append head is the INSTALL event above. The native ledger root is its first-event anchor, `a0413d075c0ec54dfa6f2fe6a16a540a6cb185a104efe143e02cc0985fb44ee0`, and remains unchanged; this codec does not expose a separate LedgerId or append-changing Merkle root.

## Generic native capability

The [installer](../../adapter/planner/installation.py), typed native model, ordinary event dispatcher and codec implement the I01 contract. Optional installation fields omit defaults so historical Snapshot/bundle identities retain their original encoding. The first enabled adapter is `EXTERNAL_RESOLUTION_CONTRACT`; unsupported definitions and lifecycle instances fail closed.

INSTALL requires an absent logical role. REPLACE requires the exact baseline/active predecessor by compare-and-swap and retains an explicit supersession relation. Standalone SUPERSEDE, CONFLICT and silent overwrites are rejected according to I01. The installed identity binds the request, definition, authority, role, ordinary parent, sequence and context without hashing its own activation EventId.

Currentness is derived from active installation, actual event witness, canonical body/source pin, authority validity, generation/scope/lineage and the ordinary governed-route predicate. Revoked/expired support withdraws use without deleting history or restoring the predecessor. Native Evidence consumers check installed authority support as well as the existing route predicate. The existing gates implementation and its I01-pinned source hash remain unchanged.

All checks precede semantic publication. A local writer lock and current-head compare-and-swap protect immutable source/state/event staging and one fsynced atomic HEAD publication. Real subprocess crashes immediately before and after publication respectively preserve the prior head or recover one committed installation. Exact historical retries return the original installation identity and current canonical bundle without duplication or revival. A separately authorized, current-head request for the same active descriptor is a checked semantic no-op.

[Tests](../../adapter/tests/test_planner_installation.py) qualify a non-E2 `TEST/lineage`: INSTALL, REPLACE, explicit supersession, frame preservation, authority admission, rejection/atomicity, idempotence, history, invalidation/expiry, candidate staleness, concurrent head changes, missing reachable artifacts, traversal/symlink rejection and actual process crash recovery. All 31 I01 negative obligations are mapped to executed controls in the JSON. A terminated writer is followed by three fresh readers for each of two checkpoints and each hash seed 0/1/7/101: **24 generic comparisons PASS**. Independent reproduction yields identical native state/bundle/event identities; declared unordered collections compare canonically.

## P04 replacement, persistence and preflight

Only the matching gate route/provenance, installation bookkeeping, two configuration source pins and one ledger event changed. The old wrapper source remains physically pinned and visible before INSTALL. The exact prepared native body becomes the active source afterward. Action models/statuses/results, gate lifecycle stage/history/pending/observations, Evidence, knowledge, proofs, roots/slots, policy and context remain unchanged. The independent [pre-install oracle](qualification/INSTALLATION_I02_1/pre-install-oracle.json) was persisted before the transition and matches the reached Snapshot exactly.

The post-install state is persisted through the native transaction HEAD and published native bundle. Cold restore and replay reproduce its exact state and one installation. Replay at the prior boundary returns the original P03 bundle byte-for-byte, excluding the new configuration sources. After the writer exited, three independent readers per seed/checkpoint performed **24 additional P04 comparisons PASS**, covering native identity/state, physical source/policy pins, authority/use, scope/lineage/generation, provenance, ordered events and control. See [fresh-reader evidence](qualification/INSTALLATION_I02_1/fresh-readers.json).

The old A09 candidate remains unmodified and fails the pure native model preflight with `PARENT_MISMATCH`. Its original bundle/State/parent precede INSTALL. The [fresh candidate](qualification/INSTALLATION_I02_1/a09-post-install-candidate.json) binds the new bundle, Snapshot, append head and current route source and has a newly computed command key. Exact unchanged native Evidence identity inputs were independently checked; no admitted Evidence instance was reused. A transient Evidence-bound attestation was rematerialized from the still-offline input definitions.

The fresh candidate passes bundle/State/parent/context/policy/route checks. Native model preflight then rejects **DEPENDENCY_PROVENANCE**: its offline ATTEST dependency has no corresponding canonical current predicate/attestor. The prepared ingress pin is also absent from the canonical prefix. No dependency was dropped to bypass this check, and no admission transaction was attempted.

## Remaining installation dependencies

| Definition class | Status | Required next work |
|---|---|---|
| Route | ALREADY_CURRENT | Completed exact bounded REPLACE |
| Ingress | AUTHORITY_REQUIRED | Qualify an ingress-definition adapter and issue its own bounded installation grant |
| ATTEST | AUTHORITY_REQUIRED | Specify/qualify atomic authority–attestor–predicate installation and applicable authority |
| Action result contracts | AUTHORITY_REQUIRED | Qualify accepted-result-definition installation; REENTER inventory remains empty |
| Validation | CONTRACT_BLOCKED | Define the native A10 validation event/persistence composition |
| Typed proofs | AUTHORITY_REQUIRED | Applicable definition adapter/authority after ingress and validation |
| Root/slot | AUTHORITY_REQUIRED | Separate adapter/installation grant; the route grant does not permit PC02/E06 installation |

**NEXT_PACKAGE = P04 ingress/ATTEST installation adapter contract + bounded authority.** The generic envelope does not authorize these definitions or qualify their adapters. Complete A09–A13 execution readiness remains NO.

## Regression and preservation

The final [targeted log](qualification/INSTALLATION_I02_1/qualified-tests.log) records **30 PASS**: nine installation tests, twelve typed-proof/E01–E06/T01/G01–G04 tests and nine route/control tests. Expanded legacy T01 receipt compatibility tests retain four failures and twelve errors. An isolated pre-work runtime with all four original changed-file hashes verified reproduces the exact same failing test identities; the [comparison](qualification/INSTALLATION_I02_1/current-pre-existing-regression-comparison.json) records this separately. Existing frozen-E1 duplicate-import collection failures and earlier broad-runtime failures remain unresolved; no full-suite or release PASS is inferred.

All 12,173 pre-existing tracked-by-manifest files were checked. Only the four intended existing runtime files changed; the installer and qualification harness/tests are new. Every previous plan/prepared fixture/P03/I01 artifact and frozen-E1 file remains unchanged. `git diff --check = PASS`. P03 remains PASS, historical correspondence UNPROVEN, N-REAL unsatisfied and aggregate release gates unchanged.

```text
WORK_PACKAGE = INSTALLATION-I02
RESULT = PASS
SELECTED_OPTION = AUTHORIZE_P04_ROUTE_REPLACEMENT
AUTHORIZATION_AUTHENTICATION = PASS
INSTALLATION_CAPABILITY = PASS
INSTALL_AUTHORITY_ADMISSION = PASS
INSTALL_AUTHORITY_APPLICABILITY = PASS
ROUTE_CURRENTNESS = PASS
ROUTE_APPLICABILITY = PASS
PERSISTENCE = PASS
COLD_RESTORE = PASS
REPLAY = PASS
HISTORICAL_IMMUTABILITY = PASS
OLD_A09_CANDIDATE = STALE
A09_CANDIDATE_REMATERIALIZED = YES
A09_PREFLIGHT = FAIL_CLOSED
NEXT_FAILURE = DEPENDENCY_PROVENANCE
P04_EXECUTION_READY = NO
E2_P04_READY = NO
A09_A13_EXECUTED = NO
P03_RESULT = PASS
P03_HISTORICAL_CORRESPONDENCE = UNPROVEN
N_REAL_SATISFIED = NO
E2_FINISH_EXECUTED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
```
