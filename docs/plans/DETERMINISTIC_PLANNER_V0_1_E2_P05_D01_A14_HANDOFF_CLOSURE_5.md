# E2-P05 D01 A14 bundle/source and cold-reader handoff closure 5

`WORK_PACKAGE = E2-P05-D01-A14-HANDOFF-CLOSURE-5`

**RESULT = BLOCKED.** The exact frozen A14 Snapshot cannot satisfy the current native PersistenceBundle source-index contract. This is a source-contract contradiction, not a missing save result to discover by executing A14. All 52 resolved bindings remain unchanged. **52 resolved + 59 unresolved = 111.** Sixteen remaining references depend on A14; none is promoted.

## Decisive source-closure proof

The Snapshot identified as planner-snapshot-v1:91017c3947096a0470ba44aff95901872768fa205205d39c7bf60f840f848c9c contains both a human choice and grant provenance at `qualification://E2-P02-human-decision`, with two distinct required CONTENT_IDENTITY/raw-file-sha256 values:

- Choice: `6bebc233783b5faa0898ecccb20cf51ce529086c74ca672a113450f6e270a411`.
- Grant: `cddac13f5e0b0f460e5d58a68d4ce753ce43cb5d17481be408d9b5f43d616574`.

The native codec imposes three simultaneous constraints: every initial/current provenance `(path, identity)` must be present as a RAW source pin; RAW pins cannot project a JSON section; and bundle source pins must be unique by `(path, pointer, profile)`. The two obligations therefore require duplicate raw-pin keys with different identities. Including both violates uniqueness; omitting either violates provenance membership. A new source root cannot fix that contradiction. The URI additionally fails `_path` canonicalization: `Path(path).as_posix()` changes the repeated slash.

This proof uses the frozen Snapshot fields and current source code, without invoking bundle validation, replay, recompute, save, or restore. The prior checkpoint qualification independently records this exact GOVERNED_UNKNOWN state as Snapshot-only with no PersistenceBundle. Its GenesisBoundBundle alternative has a different Snapshot and identity domain. Neither reports nor alternate bundle types are selected as native reader inputs.

## Recovered boundary and save contract

The earliest canonical E2-A14 case and acceptance matrix require an independent external-checkpoint copy with rule_known=false and a valid ExternalResolutionContract; native recompute, save, writer termination, and cold restore. This preserves unknown-rule semantics and excludes positive receipt continuation or a rule-known flag patch.

V2 remains the prospective native backend: save_bundle/restore. A14 recompute produces a Computation observation; it does not apply an external event or produce a SuppliedResult. That observation is not an independent persisted native result or PersistenceBundle member. Prior event history cannot be inferred empty from a Snapshot merely because recompute adds no event.

The bundle requires initial/current Snapshots, ordered events, source/policy pins, policy version, replay scope and applicable dossier-materialization bindings. Snapshot context scope/lineage/generation differs from bundle replay scope. Extended external state requires a supported P05/P06 policy version; no exact policy or scope is chosen from an absent bundle. Ledger root/head must come from authoritative ordered event history, not report order or the Snapshot hash.

Native save_bundle validates/replays the already-built bundle, verifies sources, publishes event/archive dependencies and canonical PLANNER-BUNDLE-1 bytes, and returns `(Path, ArtifactIdentity)`. It does not apply a result transaction or publish HEAD. Newly written files are fsynced by `_write_immutable`; save_bundle itself does not fsync the containing directory. Successful normal writer-exit visibility is not a blanket crash-durability claim.

The per-row isolated save directories already declared by Reconciliation 4 are preserved in save-contract.json. Their directories are not created. The final filename is `bundle-<native bundle SHA256>.json`; no native SHA256 value is supplied because no valid complete input bundle exists. A Snapshot identity, ledger identity, or qualification handoff identity cannot authenticate that bundle.

## Writer termination and reader contract

The writer must finish native publication and exit successfully before launching an independent reader. Snapshot/Bundle/Computation objects, in-memory save return tuples, resolver callables, and interpreter context must not cross that process boundary. A durable metadata handoff can carry the actual native path/trusted identity; it cannot replace the native saved artifact.

`adapter.planner.codec.restore(path, expected_identity, repo_root)` has three explicit operands and no native defaults. It checks the trusted raw bundle identity, schema, canonical native replay, source/policy pins, and immutable sibling event artifacts. No parameter may be obtained by trusting an unverified report or by deriving the expected identity from the artifact under test.

The current native entrypoint and source pins match Reconciliation 4. The V2 cold_readers helper waits for writer termination before starting reader subprocesses, but the same-process RESTORE step alone is insufficient. Actual saved path, expected bundle identity, source root, archive closure and complete commands remain unavailable. No writer or qualification reader is launched.

## Static handoff manifest

`handoff-manifest.json` binds recovered source/boundary/bundle/save/termination/reader contracts and the preserved target-directory rules. Its required native value slots are explicitly unresolved. **It is a blocked, non-executable contract manifest, not a sealed usable invocation handoff.** Its deterministic qualification identity is:

`qualification-D01-A14-handoff-contract-v1:32f647ae44eab262b800ce1abe828a2c2b2a0a2649ca219ebee2184def689d92`

That identity authenticates documentary contract content; it is not planner-bundle-v1, Snapshot, ledger or authority identity.

## Dependency inventory and report

Each of the 16 dependent occurrences receives one primary dependency class and one phase owner. Other requested classes have zero missing-reference occurrences; recovered save/termination/context requirements are documented separately and are not added to the 111-reference count.

| Dependency class | Count |
| --- | ---: |
| A14_APPEND_HEAD | 0 |
| A14_BUNDLE | 2 |
| A14_LEDGER_ROOT | 0 |
| A14_OPERATION | 0 |
| A14_POST_STATE | 2 |
| A14_PRE_STATE | 8 |
| A14_RESULT | 0 |
| A14_SAVE_IDENTITY | 2 |
| A14_SAVE_TARGET | 0 |
| A14_SNAPSHOT | 0 |
| A14_SOURCE | 0 |
| COLD_READER_BUNDLE | 0 |
| COLD_READER_CONTEXT | 0 |
| COLD_READER_OPERAND | 0 |
| COLD_READER_SOURCE | 2 |
| OTHER | 0 |
| WRITER_TERMINATION | 0 |

| Report field | Result |
| --- | --- |
| PREVIOUSLY_RESOLVED | 52 |
| INITIAL_UNRESOLVED | 59 |
| A14_CONTRACT | Recovered; exact-source persistence blocked |
| A14_REFERENCES_RESOLVED | 0 |
| TOTAL_RESOLVED | 52 |
| TOTAL_UNRESOLVED | 59 |
| INDEPENDENT_RECONSTRUCTION | PASS: all 52 bindings and static contract, seeds 0/1/7/101 |
| NEGATIVE_SUITE | 23 fail-closed metadata guards |
| INVOCATION_STATIC_PREFLIGHT | NOT_RUN |
| NEXT_UNRESOLVED_CLASS | A14_SOURCE_CONTRACT_CONFLICT |
| D01_INVOCATION_OPERANDS_COMPLETE | NO |
| FULL_OUTPUT_ORACLES | 0/128 |
| PROSPECTIVE_D01_MATRIX_CONSTRUCTION_READY | NO |
| PROSPECTIVE_D01_SCOPE_DECISION_READY | NO |
| PROSPECTIVE_D01_EXECUTION_READY | NO |
| END_INTERFACES_BOUND | 4/6 |
| P05_EXECUTION_READY | NO |
| E1_ARTIFACTS_MODIFIED | 0 |
| PRODUCTION_EFFECT | NO |

Fresh metadata processes independently derive the pin contradiction, verify the original 39 plus 13 additions, and reproduce the handoff identity. Twenty-three static guards reject source/pre-state/operation/type/identity/save/reader/ledger/scope/lineage/provenance substitutions, warm-reader or ordering violations, pre/post swaps, and promotion of the blocked contract. They do not claim accepted executable-handoff validation or native qualification negatives.

## Next unresolved work

A corrected prospective source/provenance fixture contract is required before this exact durable boundary can be constructed. The contradiction cannot be resolved by executing A14, trying a different source directory, using JSON sections with RAW pins, removing a mandatory pin, supplying a Snapshot hash as a bundle hash, treating a manifest as the bundle, or silently switching to GenesisBoundBundle/Snapshot restore. This package leaves the frozen source and all prior binding identities intact. It issues no scope authority.

## Machine-readable artifacts

All supporting files reside in `qualification/E2_P05_D01_A14_HANDOFF_CLOSURE_5/`:

- `frozen-52-bindings.json`, `a14-dependency-inventory.json`, `updated-operand-inventory.json`.
- `a14-boundary-oracle.json`, `bundle-source-inventory.json`, `bundle-contract.json`.
- `save-contract.json`, `cold-reader-contract.json`, `reader-currentness.json`, `handoff-manifest.json`.
- `fresh-process-verification.json`, `negative-suite.json`, `preservation.json` and baseline.
- `construct.py`, `verify.py`, `negatives.py`, `report.py`: metadata-only recovery and verification.

## Preservation

All pre-existing adapter/docs file hashes remain unchanged, including all 52 bindings, 117 capsules, V2 contracts and frozen E1. Historical UNPROVEN labels and ORIGINAL_D01_COMPLETE_INPUT_MATRIX=UNRECOVERED remain. P05 stage bindings stay 13/13; PC01/PC02/PC03/T01 stay PASS; E2-D01 stays BLOCKED; the continuation interface is unchanged.

`QUALIFICATION_CASES_EXECUTED = 0`; `A14_EXECUTED = NO`; `SAVES_PERFORMED = 0`; `COLD_READERS_EXECUTED = 0`; `MUTATIONS_APPLIED = 0`; `INVALIDATIONS_APPLIED = 0`; `P05_EXECUTED = NO`; `P06_EXECUTED = NO`; `NATIVE_STATE_CHANGED = NO`; `NEW_AUTHORITIES = 0`; `INSTALL_EVENTS = 0`; `N_REAL_SATISFIED = NO`; `E1_ARTIFACTS_MODIFIED = 0`; `PRODUCTION_EFFECT = NO`; `git diff --check = PASS`.
