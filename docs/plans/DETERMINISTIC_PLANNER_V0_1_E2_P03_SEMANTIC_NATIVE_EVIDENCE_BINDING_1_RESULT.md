# E2-P03 Semantic-to-Native Evidence Binding Closure

`T01_C_RESULT = BLOCKED`.

The binding is defined explicitly: semantic evidence `70087bfc0162f2a3fc44df7d8e2ff3121258b1ea0f97276883c59a2333da154b` and content `78654fdd7f475d76caa4e8c4b022103a2b9e34686cc0f759e4fd86a49959a605` are retained as qualification identities, while native Evidence uses its own provenance-bound identity. The unchanged native rule requires the native content identity to equal the SHA-256 of the canonical admission provenance bytes (`bce5320d831bd228af30dab403add01e0fa1b9e82896ff5ea2449b495e43bf36`), producing native entity `EVIDENCE:ca7dc4db2428cf62724b26abee3669af02742e6f50ac64bdf3ec40395b1f825d`.

This is different from the earlier provisional candidate `EVIDENCE:690302397fb12980f9ccd02f3a28447ce6e43d39af1465a9f0ae8774d462a057`, which was computed by feeding the semantic identity directly into `evidence_id` and therefore did not satisfy native `SOURCE_PROVENANCE`. The native rule is preserved; no identity was rewritten and no evidence was admitted.

The semantic validation oracle remains unchanged and consumes proposition/content/source/gate/context semantics. Proof and reentry consume typed proof, native entity reference at admission, and current source lineage; they do not require semantic/native ID equality. The explicit binding is recorded in [the machine-readable binding](./DETERMINISTIC_PLANNER_V0_1_E2_P03_SEMANTIC_NATIVE_EVIDENCE_BINDING_1_BINDING.json).

A generic materializer/mapping accepted by native admission is still required before T01-C can pass. No receipt, proof, Action, or E1 artifact was created.
