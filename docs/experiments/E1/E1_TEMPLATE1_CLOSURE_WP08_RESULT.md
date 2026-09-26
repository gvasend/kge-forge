# E1 Template-1 Contract Closure — WP-08 Result

## Result

| Required field | Result |
|---|---|
| `WORK_PACKAGE` | `WP-08 — Profile identity mapping` |
| `RESULT` | `PASS` |
| `SLOTS_RESOLVED` | [`authenticated_inputs.profile_sha256`] |
| `SLOTS_REMAINING` | `41` |
| `NEWLY_ELIGIBLE` | `[]` |
| `NEXT_WORK_PACKAGE` | `WP-09 — Task/runtime/context projections` |
| `BLOCKED_BRANCHES` | `WP-01` canonical invocation binding; `WP-02` eligibility producer; `WP-05` succession head; `WP-07` approval/predecessor projection |
| `AUTHORITY_REQUIRED_BRANCHES` | `WP-03` current RuntimeHeadAuthority; `WP-04` current supervisor authority; `WP-06` audit namespace/ledger authority |
| `CLOSURE_PLAN_EXCEPTION` | `NO` |
| `TEMPLATE1_CONSTRUCTION_READY` | `NO` |
| `CANDIDATE3_RESUMPTION_READY` | `NO` |
| `PRODUCTION_EFFECT` | `NO` |

## Eligibility

WP-08 was eligible: the current profile-root candidate, its Architect-issued root and release authorities, the released-profile binding, the ProgrammerProfile projection, and the qualified consumer/host implementation evidence were available. No WP-01, WP-03, WP-04, or WP-06 branch was followed.

## Accepted mapping

For `authenticated_inputs.profile_sha256`, the consumer's profile reference denotes the exact released profile content, not an authority-record identity or a host projection identity. The current [profile release record](E1_CURRENT_PROFILE_RELEASE_1.md) binds the released profile to `CurrentProfileRootCandidate-sha256:83b8cbc0549c64d21eaccaffc1fa45b49be368a878ccecdf9572d476477dfcd6`. The candidate's canonical identity body is 2,390 bytes and independently hashes to `83b8...` under its recorded identity rule. Therefore the field maps to that exact current released-profile content identity.

The identity domains remain distinct:

- `CurrentProfileRootAuthority-sha256:bffbdf78...` authorizes the candidate root; it is not profile content.
- `ReleasedProfileAuthority-sha256:ec39636d...` authorizes release of that exact candidate; it is not profile content.
- `ProgrammerProfile-sha256:0a0718f2...` identifies the host-consumable least-authority projection; it is not the released profile content identity.
- `CurrentProfileRootCandidate-sha256:83b8...` identifies the canonical released profile content body selected by the release authority.

This agrees with the consumer path: `resolve_profile()` resolves the supplied profile digest as a content-addressed profile object, and the continuation check compares the launch profile digest with the digest of the released profile bytes. No authority identity or ProgrammerProfile identity is substituted.

The relevant implementation evidence is [`resolve_profile()`](../../../adapter/authority_resolution.py#L77), the released-profile byte-digest comparison in [`governance_continuation.py`](../../../adapter/governance_continuation.py#L235), and the profile candidate's recorded canonical identity-body rule in [the candidate report](E1_CURRENT_PROFILE_ROOT_CANDIDATE_1.md).

For `fields_values.execution_profile`, code inspection establishes that the field is not a profile identity. `WorkAuthorization.execution_profile` is parsed as a runtime specification by `GovernedHost`; its producer is `runnable_profile.authorization()`, which canonically serializes `specification(binding, acceptance)`. The current profile authority and ProgrammerProfile constrain that runtime policy. WP-08 establishes this producer/projection semantics, but does not construct its invocation-specific value; the concrete binding/acceptance inputs and resulting value remain for the later authorized construction path. Accordingly, this slot remains among the 41 unresolved slots.

This distinction is explicit in [`runnable_profile.specification()` and `authorization()`](../../../adapter/runnable_profile.py#L20), and [`GovernedHost`](../../../adapter/governed_host.py#L349) parses the field as JSON and validates the runtime specification. The value therefore cannot be populated by copying any profile identity.

## Closure state

Only `authenticated_inputs.profile_sha256` is directly resolved. `fields_values.execution_profile` has a defined source/projection rule but remains unmaterialized. No work package became newly eligible as a consequence of WP-08; WP-09 is the next eligible package under the plan's sequence and existing dependencies. The accumulated blocked and authority-required branches are listed in the result table above. No exception was discovered, and neither readiness gate changed.

The result is appended to [Closure Plan 1](E1_TEMPLATE1_PRODUCTION_CONTRACT_CLOSURE_PLAN_1.md). No Template-1 or Candidate-3 artifact was constructed.
