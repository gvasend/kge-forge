# R3 production-observation qualification

Verdict: `RUN2_R3_PRODUCTION_READY_FOR_NEXT_ATTEMPT`.

The harness now has an explicit `OBSERVE_AND_QUALIFY_EXISTING_PRODUCTION_RUNTIME` mode. It verifies the authenticated production enrollment and adopted R3 runtime as evidence, while granting no runtime-selection, invocation, provider, or E1-effect authority. The correction is `NON_MATERIAL_IMPLEMENTATION_CONTINUATION`; R3 production bytes and authority journals are unchanged. The exact file identities and results are in [PUBLICATION.json](./PUBLICATION.json).

R3 is `sha256:eebb05f30a4a64befeca7802990129ac79dff701dd192789fbdf59be2ec118ff`, adopted by `ENROLLED-RUNTIME-ADOPTION-sha256:bd90f1a6ef588c62502e1b0e315e6f49aae7e71ad5b947df6a560f5a6c49b01d`, with runtime-head authority `RUNTIME-HEAD-AUTHORITY-sha256:75e6b7f2b5867c6d04bf0eeefc66f0c148d3f3e15e776c0d9e2b20b6352a1a5d`. Scope negatives reject qualification binding presented as production, production enrollment presented as the old qualification scope, and missing, arbitrary, stale, or substituted scope.

Cold preparation through `MODEL_REQUEST_READY` took 158.235s. Warm samples took 158.284s and 152.812s. The maximum normal phase was 24.833s, below the 30s soft threshold and well below the 300s no-progress hard limit. Thirty monitored status samples were all `FRESH`; the terminal projection converged to `CANCELLED`, released ownership, and `QUIESCENT`.

The qualification used isolated synthetic invocation identities and stopped before provider/model handoff. It recorded zero real model/provider requests, real invocations, ownership left behind, or effects. r12 remains an eligible `ACTIVE_CANCELLED_PRE_MODEL_NO_EFFECTS` predecessor. S3 remains the exact qualified READY supervisor. Historical runtime, adoption, enrollment, and invocation evidence remains preserved.
