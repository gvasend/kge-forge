# E1 Template-1 Contract Closure — WP-10 Result

## Result

```text
WORK_PACKAGE = WP-10
RESULT = BLOCKED
SLOTS_RESOLVED = []
SLOTS_REMAINING = 41
NEWLY_ELIGIBLE = []
NEXT_WORK_PACKAGE = WP-11
CLOSURE_PLAN_EXCEPTION = YES
TEMPLATE1_CONSTRUCTION_READY = NO
CANDIDATE3_RESUMPTION_READY = NO
PRODUCTION_EFFECT = NO
```

## Eligibility and bounded scope

The latest Closure Plan 1 execution record, after WP-09, explicitly marks WP-10 eligible and next. Section 2 permits independent mapping work for WP-08–12 where sources are grounded. WP-13 remains a prerequisite to final projections; no final projection was accepted here. Existing repository/profile authority permits no new permissions.

The ten scoped `fields_values` slots are `read_roots`, `write_roots`, `deny_roots`, `read_deny_roots`, `write_deny_roots`, `exec_bins`, `exec_argv_allowlist`, `shell`, `network`, and `write_directory_roots`. All remain unresolved. RepositoryAuthority authentication, complete path normalization/subset/conflict checks, and the other field mappings were not completed because the exception required stopping. This is not a finding that those sources are absent.

## CLOSURE_PLAN_EXCEPTION — WP10-EX01

Classification: **canonical/runtime representation mismatch; producer/consumer contract mismatch; missing deterministic hydration mapping**.

Exact root condition: canonical JSON `fields_values.exec_argv_allowlist` contains inner arrays decoded as lists. `construct_work_authorization()` (`adapter/invocation_constructor.py:70–75`) copies `fields_values` with `dict(...)`, overwrites four unrelated fields, and passes it directly to `WorkAuthorization(**fields)`, without conversion. The dataclass's tuple annotation (`adapter/governed_host.py:24`) does not convert values. The host execution guard (`adapter/governed_host.py:346–347`) checks `tuple(argv) not in self.auth.exec_argv_allowlist`. A tuple does not equal the corresponding list, so the declared exact command fails this guard through that JSON representation. This describes the guard condition, not an execution reaching or passing the earlier host gates.

Both current profile `/least_authority/exec_argv_allowlist/0` and ProgrammerProfile `/constraints/execution/exec_argv_allowlist/0` specify:

```json
["/usr/bin/python3","-B","-m","unittest","discover","-s","tests/context","-p","test_*.py","-v"]
```

A standard-library-only expression reproduction JSON-round-tripped that array within an allowlist. Its entry type was `list`; `tuple(argv) not in decoded_allowlist` returned `True`. The comparison `tuple(argv) in (tuple(argv),)` returned `True`. This establishes the type distinction only, not an accepted projector or repair. No adapter was imported, no WorkAuthorization or Template-1 was constructed, and no host or allowlisted command was executed.

The policy requires a nonempty exact allowlist. An empty replacement would disable this guard; an invented type tag or hydration rule is not defined by this constructor. Investigation stopped at the confirmed mismatch. No repair, alternative producer search, or recursive investigation followed. Task network and model transport remain separate; neither permission was changed.

## Source and derivation provenance

Raw-file SHA-256 at inspection (checkout evidence, not a claim of runtime release qualification):

| Evidence | SHA-256 |
|---|---|
| `docs/experiments/E1/E1_TEMPLATE1_PRODUCTION_CONTRACT_CLOSURE_PLAN_1.md` (before append) | `e2de99d70a8e485dc102a2f8646b3713c66313cfe329f1ce2ef8ac83a95e03d1` |
| `docs/experiments/E1/E1_CURRENT_PROFILE_ROOT_CANDIDATE_1.json` | `8116f039c40f380470e53151d6189b1b12be98e077275b5229cff9d50a2e3342` |
| `docs/experiments/E1/E1_PROGRAMMER_PROFILE_1.json` | `27105027fee5ba4139cd78d6d974a61db3bc1f529f29bddbc30503fb6873ec60` |
| `adapter/invocation_constructor.py` | `0799ca15ab055ddd13117cd67e4e47a924f02eacc78620d5ecee567f5d694ce2` |
| `adapter/governed_host.py` | `cb1d56d5787f69848ac67a8eee11755bd524cfbce17f5c0d797245357c0cdc16` |

Profile identity bodies were independently recomputed using UTF-8 JSON, sorted keys, compact separators, listed array order, excluding `identity` and derived `canonical_byte_length`:

- Released profile content: 2,390 bytes; `CurrentProfileRootCandidate-sha256:83b8cbc0549c64d21eaccaffc1fa45b49be368a878ccecdf9572d476477dfcd6`.
- ProgrammerProfile projection: 2,304 bytes; `ProgrammerProfile-sha256:0a0718f285a942c13a9f00e4b367cbea2394937fa18c4d7e11ed2c6c2803dd67`.

These checks authenticate the cited content and support the representation finding only; they do not establish full WP-10 source applicability or resolve a slot.

## Mechanical inventory accounting

The original tables contain 20 unresolved authenticated-input slots and 23 field-value slots. Earlier records established `InvocationAttemptId` and `profile_sha256`. WP-10 resolves zero: `20 - 2 + 23 - 0 = 41`. Policy-fixed `initial_state` and `ownership` were excluded from the original unresolved inventory. Schema, validator, and authority gates remain separate.

Remaining authenticated-input slots (18):

`binding_sha256`, `canonical_binding`, `DispatchAuthorizationId`, `specific_approval_id`, `predecessor`, `eligibility`, `release_authority`, `OperationalContextId`, `runtime`, `runtime_head`, `supervisor`, `succession_head`, `ModelPayloadDigest`, `transmission_retention`, `budget_policy`, `implementation_identity`, `audit`, `lifecycle_envelope`.

Remaining `fields_values` slots (23):

`authorization_id`, `revision`, `work_package_id`, `session_id`, `turn_id`, `read_roots`, `write_roots`, `deny_roots`, `read_deny_roots`, `write_deny_roots`, `exec_bins`, `exec_argv_allowlist`, `shell`, `network`, `state`, `context_binding`, `context_projection`, `ownership_ledger`, `write_directory_roots`, `execution_profile`, `model_transport`, `model_transmission`, `operational_binding`.

## Accumulated closure state after WP-10

| Package | Status | Root condition / gate |
|---|---|---|
| WP-01 | BLOCKED | Canonical current invocation/dispatch binding absent; carried forward. |
| WP-02 | BLOCKED | WP-01 and eligibility evidence prerequisites unresolved. |
| WP-03 | AUTHORITY_REQUIRED | Current R4/G4 runtime-head authority absent; carried forward. |
| WP-04 | AUTHORITY_REQUIRED | Current applicable supervisor authority absent; carried forward. |
| WP-05 | BLOCKED | Supervisor/succession source path unresolved. |
| WP-06 | AUTHORITY_REQUIRED | Current audit namespace/store authority absent; carried forward. |
| WP-07 | BLOCKED | Authoritative attempt-chain inputs unresolved. |
| WP-08 | PASS | Profile content mapping previously accepted; concrete execution-profile value still open. |
| WP-09 | BLOCKED | JSON context hydration and current OperationalBinding governance-shape gaps; carried forward. |
| WP-10 | BLOCKED | WP10-EX01: JSON argv inner lists do not match the host tuple membership guard. |
| WP-11 | ELIGIBLE | Independent provider/content/retention/transport mapping; not executed. |
| WP-12 | ELIGIBLE | Independent budget/lifecycle mapping; not executed. |
| WP-13 | ELIGIBLE | Independent contract specification under adopted definition authority; not executed. |
| WP-14 | AUTHORITY_REQUIRED | Separate validator implementation authority required; not executed. |
| WP-15 | BLOCKED | Source/mapping/schema/validator prerequisites and separate construction/release authorities unsatisfied. |

Accumulated authority requirements: current runtime-head, applicable supervisor, and audit namespace/store selections (WP-03/04/06); `AUTHORITY_TO_IMPLEMENT_VALIDATOR`; `AUTHORITY_TO_CONSTRUCT_BINDING_INPUT`; `AUTHORITY_TO_CONSTRUCT_TEMPLATE1`; and artifact-specific `AUTHORITY_TO_RELEASE_TEMPLATE1`. No new authority was issued or inferred. Conditional future decisions retain their original plan conditions.

Accumulated closure-plan exceptions: WP-09's JSON context-binding hydration gap and OperationalBinding missing-governance consumer-shape gap; plus WP10-EX01's argv representation mismatch. Earlier blockers and exceptions are carried forward without reinvestigation or repair.

Mechanical selection: eligible unexecuted packages are `{WP-11, WP-12, WP-13}`; the minimum in plan order is `WP-11`. WP-10 unlocks nothing: `NEWLY_ELIGIBLE = []`. These independent packages were already eligible; selection is not execution.

The 41 unresolved slots falsify the complete-input and complete-field conjuncts of §6. Canonical binding, current source authorities, schema/identity, and qualified-validator gates also remain incomplete. Thus Template-1 construction readiness is false. Section 7 requires that readiness first, so Candidate-3 resumption readiness is false. No next package was executed.

```text
NEXT_ELIGIBLE_WORK_PACKAGE = WP-11
TEMPLATE1_CONSTRUCTION_READY = NO
CANDIDATE3_RESUMPTION_READY = NO
PRODUCTION_EFFECT = NO
```

Only this result and Closure Plan 1 were changed. No previous artifact was modified, authority issued, Template-1 or Candidate 3 constructed, Candidate-3 construction authority consumed, or production effect performed.
