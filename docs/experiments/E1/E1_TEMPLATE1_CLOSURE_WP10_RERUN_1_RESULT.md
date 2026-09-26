# E1 Template-1 Contract Closure — WP-10 re-run 1

## Result

```text
WORK_PACKAGE = WP-10
RESULT = BLOCKED
REPAIR_RESULT = PASS (local checkout qualification only)
SLOTS_RESOLVED = []
SLOTS_REMAINING = 41
NEWLY_ELIGIBLE = []
NEXT_WORK_PACKAGE = WP-11
NEXT_ELIGIBLE_WORK_PACKAGE = WP-11
NEW_CLOSURE_PLAN_EXCEPTION = NO
CLOSURE_PLAN_EXCEPTION = YES (accumulated)
TEMPLATE1_CONSTRUCTION_READY = NO
CANDIDATE3_RESUMPTION_READY = NO
PRODUCTION_EFFECT = NO
```

## Re-run eligibility and prerequisite repair

The user's instruction explicitly authorizes this bounded re-run of WP-10 after independent justification and qualification of the argv representation repair. It does not change the general next-package selection or authorize WP-11. See [repair justification and regression evidence](E1_TEMPLATE1_WP10_ARGV_REPAIR_1.md). That analysis established JSON arrays as the canonical field representation and tuples as the intentional runtime representation from the effective contract, existing typed producer, and host comparison. All five focused tests passed before re-evaluation. The host comparison was not modified.

The original [WP-10 result](E1_TEMPLATE1_CLOSURE_WP10_RESULT.md) remains unchanged as historical evidence. No production Template-1 or Candidate 3 was created; tests use synthetic identities only.

## Bounded re-evaluation and exact remaining root condition

The named policy source bodies independently recomputed to:

| Source | Canonical identity | Bytes |
|---|---|---|
| Released profile content | `CurrentProfileRootCandidate-sha256:83b8cbc0549c64d21eaccaffc1fa45b49be368a878ccecdf9572d476477dfcd6` | 2390 |
| ProgrammerProfile | `ProgrammerProfile-sha256:0a0718f285a942c13a9f00e4b367cbea2394937fa18c4d7e11ed2c6c2803dd67` | 2304 |
| RepositoryAuthority | `RepositoryAuthority-sha256:79b5d23d69e623306279d4966c31443a45ceea2adc03549b08cf1d2967e515fb` | 1131 |

Canonicalization was UTF-8 sorted-key compact JSON, preserving listed array order. Profile bodies exclude `identity` and derived `canonical_byte_length`; the repository body is the first JSON record in `E1_HOST_PREREQUISITE_AUTHORITY_ISSUANCE_1.md`, excluding `authority_id`. The RepositoryAuthority's ProgrammerProfile reference matches. Runtime, controller-store and lineage values agree across these three sources, as do their read/write roots. The two profile argv arrays agree exactly. This is content and cross-reference validation, not full currentness/publication qualification.

**Remaining root condition: `MISSING_DETERMINISTIC_MAPPING` for `fields_values.exec_bins`.** Neither the released profile `/least_authority`, ProgrammerProfile `/constraints/execution`, nor the RepositoryAuthority defines an independent `exec_bins` value. Closure Plan 1 §1B expressly requires each execution field to be projected independently and prohibits inferring executables from argv. The production contract's `exec_bins` row independently records that deriving bins from argv is not authorized/defined. The historical/current helper `authority_profile.programmer_authorization()` derives basenames from argv; that implementation behavior cannot override this explicit closure constraint or establish an independent policy source.

The requested JSON hydration repair does not resolve that policy-mapping gap. No bin was inferred, no executable permission added, and no replacement source or authority was invented. This is a pre-enumerated gap, not a newly discovered exception. Re-evaluation stopped here without recursively investigating or repairing it. Complete deny-root, path normalization/conflict, and directory-grant qualification was not reached; no partial source observations count as resolved slots.

## Cumulative state and mechanical recomputation

The original inventory has 20 unresolved authenticated-input slots and 23 field-value slots. Earlier records resolved only `InvocationAttemptId` and `profile_sha256`. This re-run accepts no slots: `20 - 2 + 23 = 41` (18 authenticated inputs, all 23 field values). All ten WP-10 fields remain unresolved. A local representation repair is not a complete authoritative field-value derivation. No unrelated slot changed.

Package states remain:

| Package | Status |
|---|---|
| WP-01 | BLOCKED |
| WP-02 | BLOCKED |
| WP-03 | AUTHORITY_REQUIRED |
| WP-04 | AUTHORITY_REQUIRED |
| WP-05 | BLOCKED |
| WP-06 | AUTHORITY_REQUIRED |
| WP-07 | BLOCKED |
| WP-08 | PASS |
| WP-09 | BLOCKED |
| WP-10 | BLOCKED |
| WP-11 | ELIGIBLE |
| WP-12 | ELIGIBLE |
| WP-13 | ELIGIBLE |
| WP-14 | AUTHORITY_REQUIRED |
| WP-15 | BLOCKED |

Accumulated blockers: WP-01 canonical invocation/dispatch binding; WP-02 eligibility prerequisites; WP-05 supervisor/succession source path; WP-07 attempt-chain inputs; WP-09 context hydration and OperationalBinding governance-shape gaps; WP-10 independent `exec_bins` source/projection and unfinished repository/execution field qualification; WP-15 incomplete sources, mappings, schema, validator, and construction/release gates. Earlier blockers were not reinvestigated.

Accumulated authority requirements remain unchanged: WP-03 current runtime-head, WP-04 applicable supervisor, WP-06 audit namespace/store; separate WP-14 validator implementation authority; binding-input construction authority; Template-1 construction authority; and exact-artifact Template-1 release authority. This bounded repair does not grant any of them.

Accumulated exceptions retain WP-09's two open representation/shape gaps. WP10-EX01 is **repaired and regression-qualified in the local constructor**, with its original evidence preserved. This does not certify or publish a changed frozen R4 runtime. No new unexpected closure-plan exception was found in this re-run: the independent executable mapping gap is already explicit in the original plan §1B and production contract. Thus accumulated `CLOSURE_PLAN_EXCEPTION = YES`, while `NEW_CLOSURE_PLAN_EXCEPTION = NO`.

The eligible unexecuted set remains `{WP-11, WP-12, WP-13}`; minimum plan order yields `NEXT_ELIGIBLE_WORK_PACKAGE = WP-11`. None became newly eligible and none was executed. The complete-input and complete-field conjuncts of §6 remain false; source, schema and validator gates are also incomplete. Therefore Template-1 readiness is false, and §7's prerequisite makes Candidate-3 resumption readiness false. No construction authority was consumed or production effect performed.

## Snapshot provenance

| Evidence | SHA-256 |
|---|---|
| `adapter/invocation_constructor.py` | `5908b257fdc7325d94d7524fbacbe3a7ec26d18d98507d6232c9ba1d41e8f9f7` |
| `adapter/tests/test_invocation_constructor.py` | `413f4623650ebbd78d3dedbfa57cd6589eb8f0cc765e43194cce38c9aaf8268e` |
| `docs/experiments/E1/E1_TEMPLATE1_WP10_ARGV_REPAIR_1.md` | `f7e01055e3d07f615068f12ba3e255e287cf070c8b5730f95a0f602d173ef039` |
| `docs/experiments/E1/E1_HOST_PREREQUISITE_AUTHORITY_ISSUANCE_1.md` | `5cf24bf05643e69543a9db154af7e2a6edc1943fe32280ea7d7762b06a43132f` |
| `docs/experiments/E1/E1_TEMPLATE1_CLOSURE_WP10_RESULT.md` | `7062fe6a5c38269d271b77d2edb7f037bb5cc668fe6b7bad65a46e70894f4d26` |

Closure Plan 1 before this append: `cc41fdac526c0f0838025b19f245805139428e4f1d978dfaea5416828c736a5b`. Source/profile and host/producer files remain byte-identical to the pre-repair snapshot; only the constructor, new regression test, and new documentation/plan append were changed.
