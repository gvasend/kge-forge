# Controller placement recheck — BLOCKED, remediation incomplete

E1 remains **INACTIVE**. E1-WP-001 remains **INELIGIBLE AND UNDISPATCHED**.
This diagnostic report is not a controller authority record or an operational selector.
The requested ACTIVE + OWNERSHIP_HELD + CURRENT_RELEASE_BINDINGS_VALID stop point was not reached.

The unchanged production validator rejected the current operational binding with
`LifecycleDenied: controller evidence within Programmer grant`. A byte-identical
profile-reference substitution in memory was separately rejected with
`ValueError: immutable release selection changed`. No candidate was installed.
The content-versus-location mechanism remains unimplemented; these checks do not
complete the requested remediation or its qualification.

A separate invocation of the unchanged production host prerequisite found an
additional blocker: the released profile pins supervisor PID **57950**, but
`/proc/57950/stat` does not exist. This was a separate prerequisite check; the
complete production validator stopped earlier at placement. Starting another
supervisor would not satisfy the pinned PID, parent, executable, cwd, argv and
cgroup identity. No supervisor was started and no profile field was changed.

## Profile bytes and Programmer boundary

The existing controller-side candidate copy was reverified at:

```
/tmp/kge-forge-e1-controller/auth-e1-wp-001-r7-94f511dfcdcc43ac837191f8732ced39/a0547c7c33b95628d9419a62972f15062bd6fa8ab9236496ceb7d6ab21fbab75
```

- ReleasedProfileContentId, exact bytes SHA-256:
  `a0547c7c33b95628d9419a62972f15062bd6fa8ab9236496ceb7d6ab21fbab75`.
- Released canonical JSON fingerprint:
  `b9e7f72d97525f39fbddfe92f276ab6aedd057ef6c5b7284dc163f1db9c9c328`.
- Exact equality against the historical released file: **PASS**.
- Independent child-process read and SHA-256 verification: **PASS**.
- Outside released Programmer read/list/search, write/patch, runtime cwd and
  snapshot input roots: **PASS**.
- Actual governed read/list/search/write/patch calls with a separate synthetic
  identity using the released path grants: all **DENIED: outside grant**.
- Absolute-path escape and direct snapshot inclusion using either the repository
  or private source root: **DENIED** by existing path/snapshot validation.
- Synthetic altered bytes under the released expected hash: **DENIED**.

These tests exercise the governed Programmer interface. They do not assert that
host UID permissions alone separate controller and Programmer. The independent
child loaded candidate bytes; it did not reconstruct a relocated operational
binding. Payload execution and live QUIESCENT qualification were not performed.

## Other required artifacts

All 715 previously inventoried historical references and their private copies
were reverified byte-for-byte. The production validator also directly loads:

```
docs/experiments/E1/pre_dispatch/pd06_release_evidence/provisioning/RECEIPT.json
SHA-256: 2583ed2b52165591050256f4e51c0f99af94289f0f8c1aff0c43b2aa67f0d3e9
```

That direct reference was absent from the earlier 715-reference inventory. Its
exact bytes already exist at `<controller candidate root>/<SHA-256>` and were
verified. The expanded inventory contains **716 references** inside Programmer
authority, with exact private candidates outside it. Copies remain unbound.
They include release, approval, dispatch, launch, profile, context, qualification
and provisioning evidence. No filesystem cleanup or repository restructuring
was performed.

The real authorization audit, shared ownership ledger and controller fence remain
outside released Programmer roots. Their operational locations were inspected.
The audit and ledger were not modified; the ledger remains empty.

## Preserved operational ancestry

| Item | Result |
| --- | --- |
| PD-06 / E1-B01 | RELEASED / PASS, unchanged |
| Authorization | `auth-e1-wp-001-r7-94f511dfcdcc43ac837191f8732ced39` |
| ReleaseBasisId | `E1-RELEASE-BASIS-sha256:bc176574817f6b7fe06fdcf87a71c57b2a8bfe74e55ed20f2aa55ad5d4fa5181` |
| ReleaseDecisionId | `E1-RELEASE-DECISION-sha256:43ab22254604a29f3cf2164152803ee5f689f7540e2006c43d27ded87d83d8c0` |
| OperationalContextId | `E1-OPERATIONAL-CONTEXT-sha256:9392a7af0670749265950e0a7bcbcc8be9f393452a8d85656a44514f86bfac47` |
| Chain digest | `a46764481045e12aaedbf4551000a038918a6f57d7239c1b5dce5ce29a80364f` |
| ModelPayloadDigest | `8e9b1fa28d57a4c4e21e28dbe9be7d70e028438ce425862b43b3728d9c22b577` |
| Adopted implementation continuation | Preserved; every production Python file unchanged |
| Dispatch inheritance | PASS for the unchanged adopted context |
| New operational continuation | None constructed or adopted |
| Activation validation | BLOCKED, controller evidence inside Programmer grant |
| Activation event | None |
| Ownership reservation | None |
| Independent lifecycle reconstruction | INACTIVE, certain, no ownership |
| Model-handoff eligibility | False |

The historical release, dispatch, adoption and profile files remain unchanged.
The live audit contains only authorization issuance, projection verification and
controller reconstruction events. **Zero E1 model requests and zero E1
implementation effects**, including during this recheck.

The remaining work is a qualified operational location-binding mechanism for
all required controller evidence, followed by an authorized continuation and
full production revalidation. The missing released supervisor is an additional
external prerequisite; this report does not authorize replacing its binding.

Reproducible command from the repository root:

```
PYTHONPATH=. python3 docs/experiments/E1/pre_dispatch/controller_placement_recheck_2026-09-17/recheck.py
```

`RECHECK.json` contains the complete inventory, denial results, current identities
and preservation fingerprints. No production validator was weakened or bypassed.
