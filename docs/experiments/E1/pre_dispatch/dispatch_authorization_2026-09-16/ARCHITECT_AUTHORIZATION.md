**ARCHITECT DISPATCH AUTHORIZATION**

The Architect accepts the final pre-dispatch assessment as PASS and authorizes dispatch of E1-WP-001.

Authorized invocation:

`auth-e1-wp-001-r7-94f511dfcdcc43ac837191f8732ced39`

This authorization is bound to the exact session, turn, context, audit, ownership, work-package, profile, release, and governance-continuation identities recorded in:

`docs/experiments/E1/pre_dispatch/governance_continuation_2026-09-16/PRE_DISPATCH_ASSESSMENT_FINAL.json`

Authoritative release identities:

ReleaseBasisId:

`E1-RELEASE-BASIS-sha256:bc176574817f6b7fe06fdcf87a71c57b2a8bfe74e55ed20f2aa55ad5d4fa5181`

ReleaseDecisionId:

`E1-RELEASE-DECISION-sha256:43ab22254604a29f3cf2164152803ee5f689f7540e2006c43d27ded87d83d8c0`

OperationalContextId:

`E1-OPERATIONAL-CONTEXT-sha256:0cd0d5c59caee38ab381e22a3d9824ee5b79bb942ee4c4dfede3f2e554043c0c`

Continuation-chain digest:

`ae3a8a1b5996ebeb2cd1f7f7098e0e40eb5bab809b1d759ab68470e48df155e8`

FullContextDigest:

`37d75fd7b3837dedb41513436878b620609b4958a3e9dce7276a248e53288656`

ModelProjectionDigest:

`ea2ced0e8e128d3afbe2bfb0591f6be2311a8512576159d20d40baf6f0bec610`

Released profile fingerprint:

`b9e7f72d97525f39fbddfe92f276ab6aedd057ef6c5b7284dc163f1db9c9c328`

## Required dispatch procedure

Create an immutable Architect dispatch record containing this authorization and all referenced bindings.

Immediately before dispatch, atomically revalidate:

* PD-06 remains RELEASED;
* E1-B01 remains PASS;
* ReleaseBasisId matches;
* ReleaseDecisionId matches;
* OperationalContextId matches;
* continuation-chain digest matches;
* FullContextDigest matches;
* ModelProjectionDigest matches;
* released profile fingerprint matches;
* E1-WP-001 identity and bytes match;
* production profile and launch configuration match;
* transmission-clearance manifest remains unchanged;
* no MATERIAL governance continuation has occurred;
* no active or INDETERMINATE conflicting ExecutionScope exists;
* no conflicting ownership reservation exists;
* required supervisor/host authority is available;
* audit/evidence isolation remains valid;
* required provisioning remains valid.

Any mismatch invalidates this dispatch authorization for execution and must fail closed.

Do not repair, regenerate, or silently substitute a changed binding during dispatch.

## Activation

If and only if the atomic dispatch validation passes:

1. Activate the exact released E1 Programmer profile for this authorized invocation.
2. Acquire the authoritative E1 invocation ownership reservation.
3. Bind the Programmer to the exact released Model Context Projection.
4. Establish the authorized audit chain.
5. Dispatch E1-WP-001 to the released KGE Forge Programmer.

The Programmer receives only the released TRANSMIT context.

LOCAL_ONLY and NEVER_TRANSMIT information remains controller-side.

## Execution

All Programmer effects remain governed.

Execution must continue to use:

`governed_exec`
→ authoritative ExecutionScope
→ result
→ CLOSED
→ authoritative QUIESCENT
→ terminal ActionResult

Result availability alone does not authorize subsequent execution or completion.

All authoritative repository mutations must occur through the released governed write/patch promotion paths.

Execution-snapshot changes do not automatically become authoritative repository changes.

Authority-expansion requests remain non-self-authorizing.

## Interruption and uncertainty

Preserve the qualified interruption/recovery semantics.

If execution, controller state, context identity, authority, or effect outcome becomes uncertain:

* fail closed;
* preserve explicit uncertainty;
* reconstruct from durable evidence;
* do not automatically retry uncertain persistent effects;
* require the established recovery authority where applicable.

## Work-package boundary

This authorization applies only to E1-WP-001.

It does not authorize:

* another work package;
* materially changed E1-WP-001 content;
* a regenerated production profile;
* a changed Model Context Projection;
* additional external destinations;
* expanded filesystem or execution authority;
* a new authorization identity.

Any such change requires a new Architect assessment and authorization.

## Completion

After E1-WP-001 terminates, do not infer Experiment 1 acceptance from Programmer completion.

Return the implementation, authoritative knowledge changes, verification evidence, traceability, anomalies, authority-expansion requests, unresolved uncertainty, and Programmer completion status to the Architect for the required final Architect assessment and subsequent human acceptance.

**Architect decision: DISPATCH AUTHORIZED.**
