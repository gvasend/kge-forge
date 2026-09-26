# r13 cross-runtime predecessor reconciliation

## Qualification update

The temporal-authority qualification now passes using the immutable r12
capture and the authenticated R3 adoption records. Machine-readable evidence
is in `TEMPORAL_AUTHORITY_QUALIFICATION.json`; the implementation is in
`adapter/temporal_authority.py` with negative-case tests in
`adapter/tests/test_temporal_authority.py`.

## Result

`RUN2_TEMPORAL_AUTHORITY_READY_FOR_ARCHITECT_DECISION`

The fresh gate's `bootstrap operational binding mismatch` was a real field
mismatch in the current validator. It is not evidence that r12 was invalid.
The validator compares the predecessor's historical operational binding with
the current R3 store applicability as though they were the same invocation
field.

No invocation, ownership, audit append, model request, or implementation
effect was created. The canonical r13 object and its unused audit namespace
are unchanged.

## Old and current bindings

| Field | r12 historical binding | Current R3 binding | Interpretation |
|---|---|---|---|
| OperationalContextId | `E1-OPERATIONAL-CONTEXT-sha256:a59e21566098fee1756bbe991f74e0d2c8c5b756a76d90877911c35d57044a8a` | Current production store applicability: `E1-OPERATIONAL-CONTEXT-sha256:1ab699d479fb2086981b30074384cb2e2144241c7f009fd5edec146d53606d39` | Different authenticated context epochs |
| Full/authoritative context | `0aacb34bde5b10ae7d45ec84ac68395066848dc7136f764d8c6853300fc5ab6c` | Current R3 production projection | Current validator must use the current projection for r13, while retaining r12's value historically |
| Model projection binding | `da2e1a7f37d61ced3a31fbaa3a82e99b3d381ca7dda69c4f03395a0b71be0568` | Current R3 projection | Must be checked for r13; must not rewrite r12 |
| Continuation-chain digest | `ddf509e2283fe93aa9bb9b857a45dc449ff5ca309c66f9bdfd18c45dcf2dedfd` | `2933203c93cc4cf19170cfe51400b20a1e302ba92735767861f0251cad5a38d6` | Historical versus post-R3 ancestry |
| Release authority | `E1-RELEASE-AUTHORITY-sha256:84b7294bef3e2ccdbae8364b66f202135fcc9def9dd0081b473f847b4636628d` | `E1-RELEASE-AUTHORITY-sha256:bb1808a5ffbd720cd8447db29dc7946dbc7e50f336d4ca6c809ea82b321b3e30` | Current r13 must use the current authority; r12 keeps its historical authority |
| Runtime | r12 executed under the pre-R3 production runtime (old runtime root); reconstruction passes with that runtime | `R3 = sha256:eebb05f30a4a64befeca7802990129ac79dff701dd192789fbdf59be2ec118ff` | Runtime transition is authenticated and must not rebind r12 |

The r12 raw operational binding contains governance identities `a59e...`,
`bc176...`, `43ab...`, and `ddf509...`. The canonical r13 binding correctly
uses r12 only as predecessor and separately binds current R3/runtime-head
authority.

The existing canonical r13 artifact still carries the pre-R3 `a59e...` /
`84b729...` operational/release binding. It remains intact and unissued, but
it is not the current R3 production binding (`1ab699...` / `bb1808...`). If
the reconciled current binding is adopted, a new canonical candidate identity
will be required; the existing digest must not be changed in place.

## Reconstruction evidence

* r12 reconstruction with its original prepared authority store and original
  runtime passes. Its terminal evidence remains `CANCELLED /
  INTERRUPTED_NO_EFFECTS`, with ownership released, QUIESCENT, and no model or
  provider request.
* The same r12 bytes are unchanged in the R3-era store. Running the R3
  bootstrap verifier against that store reaches the operational-binding check
  (and, in the complete-byte store, subsequently lacks historical logical
  references); it cannot be used as proof of r12 invalidity because it applies
  the current store selector to a historical authorization.
* R3 independently reconstructs as the unique current runtime under
  `RUNTIME-HEAD-AUTHORITY-sha256:75e6b7f2b5867c6d04bf0eeefc66f0c148d3f3e15e776c0d9e2b20b6352a1a5d`.

## Authenticated transition ancestry

`R0 (historical)` → one-time bootstrap
`RUNTIME-AUTHORITY-BOOTSTRAP-sha256:7837030f70d5545b8ba3ac466317b5b7b15e29950bf0056a1d5eeaeda23b1239`
→ `R1 = sha256:1b31ac92d38952444076e3997083cf035e0862f1bc0182261826d6690ec31c15`
→ enrolled/adopted R1→R3 continuation
(`CONTINUATION-ENROLLMENT-sha256:9864f482d436c2d4727d9f030d2560fccabd45308014c3fe5202f986c68f440d`, adoption
`ENROLLED-RUNTIME-ADOPTION-DECISION-sha256:bd90f1a6ef588c62502e1b0e315e6f49aae7e71ad5b947df6a560f5a6c49b01d`)
→ `R3` current.

This ancestry answers historical validity and current succession eligibility
as separate questions. It does not authorize a caller assertion or rewrite
r12.

## Negative checks

The qualified runtime/adoption evidence establishes fail-closed behavior for
changed runtime bytes, missing bootstrap ancestry, missing R1→R3 adoption,
unadopted runtime, stale head, competing/substituted successor, and altered
historical content. A changed r12 digest or disposition also invalidates its
historical record. These checks remain required; only the comparison between a
historical predecessor context and the current context is missing.

## Applicability and disposition

This is a **material predecessor-runtime reconciliation semantic gap** unless
the released policy is amended to state the two-phase rule explicitly:

1. validate r12 against its original release/context/runtime; then
2. evaluate r12's authenticated terminal safe-predecessor disposition under
   the current R3 authority, requiring authenticated runtime-transition
   ancestry and exact current R3 for r13.

The correction belongs in current validation/reconciliation. No historical
rebinding is permitted. The temporal rule is qualified, but its production
runtime adoption remains an Architect decision. The existing canonical r13
identity remains preserved as an unissued artifact; it must be re-bound to
current fields only through a separately authorized canonical candidate if the
current R3 release/context is adopted.

## State

`R3 = CURRENT`; S3 remains the exact qualified READY supervisor. r12 remains
immutable and safe. No r13 lifecycle fact, ownership, model request, or effect
was created.
