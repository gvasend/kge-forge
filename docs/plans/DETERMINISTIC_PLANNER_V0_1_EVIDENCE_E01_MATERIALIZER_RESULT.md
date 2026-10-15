# Evidence E01 — Semantic-to-Native Materializer

`EVIDENCE_MATERIALIZER = PASS` and `SEMANTIC_NATIVE_BINDING = PASS`.

The generic materializer derives canonical provenance identity `bce5320d831bd228af30dab403add01e0fa1b9e82896ff5ea2449b495e43bf36` and native Evidence entity `EVIDENCE:ca7dc4db2428cf62724b26abee3669af02742e6f50ac64bdf3ec40395b1f825d` using the unchanged native identity rule. Semantic ID `70087bfc…` and content ID `78654fdd…` remain separate and are preserved by binding `ea9ea350b5199c765931a01cf24c4b1dee1f89bcb7a982e58cffa352657d7776`. The corrected candidate is [here](./DETERMINISTIC_PLANNER_V0_1_E2_P03_SEMANTIC_NATIVE_EVIDENCE_BINDING_1_CANDIDATE.json).

`SOURCE_PROVENANCE = PASS`. Full T01 preflight remains **BLOCKED** at `PRODUCER_AUTHENTICATION_UNPROVED`: the existing attestor predicate is qualified with the expected source identity, while native admission requires its authentication predicate to expect the native Evidence entity identity. A scoped native admission predicate/materializer mapping is required; no existing authority was broadened.

No evidence, receipt, proof, Action, or E1 artifact was created. `T01_ADMISSION_BUNDLE_RETRY_ALLOWED = NO`.
