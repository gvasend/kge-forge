# Current-authority dispatch amendment

## Result

`RUN2_CURRENT_DISPATCH_READY_FOR_ARCHITECT_INVOCATION_DECISION`

The historical dispatch remains immutable. The current authority is represented
by an append-only derived dispatch, bound to the adopted temporal transition
and current R3 authority.

## Identities

* Original dispatch: `E1-ARCHITECT-DISPATCH-sha256:6e676c5decd4ae745d8977c2392e559896403ce5d6507db7dafc4f7a92ddd1ab`
* Temporal amendment: `E1-RUN2-TEMPORAL-AUTHORITY-AMENDMENT-sha256:910051f9b5c39a7bcd880dbd3d7549863b9c69a11d10ac85e6569c1ef193464c`
* Dispatch amendment: `E1-RUN2-DISPATCH-TEMPORAL-AMENDMENT-sha256:4133420c330d20cdac20f1c7f345b110422eafe71f14551a24ff16b19d50ba31`
* Current dispatch: `E1-ARCHITECT-DISPATCH-CURRENT-sha256:f873c2910acc596f026f24881fd96898b5f11be192f5aacf976946748ca92b77`
* Current runtime: `sha256:eebb05f30a4a64befeca7802990129ac79dff701dd192789fbdf59be2ec118ff`
* Runtime-head authority: `RUNTIME-HEAD-AUTHORITY-sha256:75e6b7f2b5867c6d04bf0eeefc66f0c148d3f3e15e776c0d9e2b20b6352a1a5d`

The current dispatch binds release authority `...bb1808a...` and
OperationalContextId `...1ab699d...`, while retaining the exact E1-WP-001,
profile, payload, transmission, budget, supervisor, and no-retry constraints.

## Candidate and gate

The old canonical r13 remains unchanged and is superseded before issuance. The
new current-authority candidate remains attempt number r13 because the old
candidate was never allocated or issued.

* Authorization label: `auth-e1-wp-001-r13-current`
* InvocationAttemptId: `InvocationAttempt-sha256:5f2c6a1582f88a23a8e92caa04e82404469dc15a525a791727f95b5e94bf063c`
* Binding SHA-256: `19cc4d0311e62fad0b8c29acce5af9b7a2a59bf16e6364e87c17cb3804a7bfaf`
* Audit namespace: absent/unused

Production-equivalent validation passed for canonical shape, amended dispatch,
r12 historical validity, temporal ancestry, current safe-predecessor policy,
R3/runtime-head, release/context, S3 readiness, and absence of competing
ownership or invocation. Negative substitution/replay cases passed.

No invocation was issued; model requests and effects remain zero.
