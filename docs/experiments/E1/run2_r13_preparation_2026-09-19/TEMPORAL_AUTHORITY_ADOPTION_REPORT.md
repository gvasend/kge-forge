# Temporal-authority adoption and current-attempt gate

## Material amendment

The adopted implementation is `adapter/temporal_authority.py`, SHA-256
`28a3af975677a485e53a784f65b5ca6269b2ec2e1659f9cdf2a753d1b26dd225`.

The append-only amendment artifact is
`TEMPORAL_AUTHORITY_AMENDMENT.json`:

`E1-RUN2-TEMPORAL-AUTHORITY-AMENDMENT-sha256:910051f9b5c39a7bcd880dbd3d7549863b9c69a11d10ac85e6569c1ef193464c`

It changes predecessor validation only. It does not rewrite r12 or alter the
bootstrap, runtime head, supervisor, or historical invocation journals.

## Independent reconstruction

* r12 historical validity: **PASS** under runtime `sha256:5c8cfcffc7a994aa17d1222184113f017b9afa237f25c32e06015491f485b97c` and OperationalContextId `...a59e215...`.
* Transition ancestry: **PASS** through bootstrap, R1, and the adopted R1→R3 decision.
* Current R3: **PASS**, `sha256:eebb05f30a4a64befeca7802990129ac79dff701dd192789fbdf59be2ec118ff`.
* Current safe-predecessor eligibility: **PASS** for r12.
* Negative tamper cases: **PASS**; altered historical bytes, missing transition links, stale/unadopted runtime, and substituted predecessor all fail closed.

## Existing candidate

The original canonical r13 object remains unchanged, unissued, and excluded
from the attempt chain. Its pre-R3 binding is superseded before issuance by
the adopted authority transition; its digest is not modified.

The post-R3 candidate is recorded separately as
`CURRENT_R13_CANDIDATE.json`, using current context `...1ab699d...`, current
R3 release authority `...bb1808a...`, current projection digests, and the
same unused r13 audit namespace. Its structured InvocationAttemptId remains
derived from the unchanged dispatch/predecessor/audit identity.

## Fresh-gate result

`BLOCKED_CURRENT_DISPATCH_BINDING_STALE`

The production `INVOCATION-ATTEMPT-BINDING-1` validator requires the
candidate `bindings` map to equal the immutable Run-2 dispatch bindings. That
dispatch still authenticates the pre-R3 values:

* release authority `E1-RELEASE-AUTHORITY-sha256:84b7294...`;
* OperationalContextId `E1-OPERATIONAL-CONTEXT-sha256:a59e215...`.

The current R3 production authority is:

* release authority `E1-RELEASE-AUTHORITY-sha256:bb1808a...`;
* OperationalContextId `E1-OPERATIONAL-CONTEXT-sha256:1ab699d...`.

The validator therefore correctly rejects the current candidate as a binding
substitution against the still-frozen dispatch. This is a separate authority
gap from temporal predecessor reconciliation. A new Architect dispatch or
dispatch amendment binding current R3 authority is required before any
current canonical candidate can pass.

No invocation was issued, no ownership was acquired, and no model/provider or
engineering effect occurred.
