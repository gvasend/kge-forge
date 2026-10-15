# E2-P03 Evidence Identity-Layer Reconciliation

`70087bfc…` is a **semantic evidence identity** from the qualified synthetic evidence contract. It is a pinned fixture identity used by the payload, validation oracle, proof contract, and ingress documentation; it was not produced by the native Evidence entity identity function.

The native identity candidate is `EVIDENCE:690302397fb12980f9ccd02f3a28447ce6e43d39af1465a9f0ae8774d462a057`. Native admission correctly derives this `EntityId` from the gate, content identity, scope, lineage, and generation, then requires the canonical Evidence provenance bytes to hash to that native identity. This protects source binding and immutable provenance and remains unchanged.

No authoritative contract requires semantic ID `70087bfc…` to equal the native entity ID. The correct relationship is a semantic-to-native binding: the native entity retains the semantic/content IDs through its qualified payload/provenance binding while using its own admission identity. The current model does not expose a dedicated semantic-ID field, so the materializer must carry that binding explicitly without weakening native provenance validation.

Classification: **E2 fixture identity misclassification plus missing semantic-to-native mapping**. The smallest correction is to reclassify `70087…` as `SEMANTIC_EVIDENCE_ID`, retain native ID `EVIDENCE:690302397fb12980f9ccd02f3a28447ce6e43d39af1465a9f0ae8774d462a057`, and add the explicit mapping at materialization. No evidence, receipt, proof, or Action was created.

`T01_C_RETRY_ALLOWED = NO` until that mapping is represented and independently validated.
