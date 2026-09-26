# Runtime-consumption implementation and remaining production gate

`BLOCKED_NOT_PRODUCTION_ADOPTED`

The previous overstatement is preserved in ../run2_r13_preparation_2026-09-19/REPORT.md. This package does not repeat it: journal qualification is not ordinary production pre-model qualification, and no real runtime head has been advanced.

## Implemented candidate

The staged runtime adds `runtime_adoption.py` and an explicit ordinary schema-7 validator branch in `attempt_chain.py`. Existing released files and all r8–r12 records are unchanged. Schema 8 remains byte-identical and qualification-only.

The mechanism separates:

* QUALIFIED: exact delta and implementation inventory have selected, content-bound evidence.
* ADOPTED: attributable Architect authority and a durable HEAD_COMMITTED event establish an adopted transition.
* CURRENT: independent ordered-journal reconstruction selects a unique adopted head.
* EXECUTING: a production invocation must bind that exact current head and actual runtime bytes, in addition to all existing invocation activation/ownership/dispatch gates. Adoption does not execute an invocation.

A bootstrap-pinned private catalog selects the material policy and exact decisions. Merely writing files or supplying a PASS label does not change that selection. Every continuation binds predecessor/successor inventories, delta, schema, applicability, qualification, release/context and independently selected adoption authority. The original OPERATIONAL-CONTINUATION-1 is preserved as a byte-exact referenced object.

One private append-only journal is both the ordered adoption evidence and the current-head authority. An exclusive flock serializes writers; read reconstruction takes a shared lock. The typed operation appends and fsyncs ADOPTION_INTENT, HEAD_COMMITTED, then ADOPTION_RECORDED. HEAD_COMMITTED is the linearization point. Partial/invalid records fail closed. Recovery never turns a pending intent into an adoption: before commitment it aborts the intent and retains PREDECESSOR_CURRENT; after commitment it completes terminal audit and retains SUCCESSOR_CURRENT. Invalid/ambiguous journal evidence raises a fail-closed error, without rewriting the journal.

The new validator branch requires an authenticated current runtime head; its absence retains the original `unaccounted runtime` check. Historical inventories and semantic qualification remain independently verified. A runtime-head overlay derives new release/context identities rather than changing historical invocation identities.

## Qualification actually performed

Twenty behavioral tests passed (`TESTS_FINAL.log`): genesis; qualified-but-unadopted rejection; exact adoption; independent-process reconstruction; two-hop order; concurrent processes (one winner); replay; skipped predecessor; implementation substitution; changed continuation reference; unpinned PASS; stale grant; qualification/production boundary; interruption before intent/after intent/after commit/after terminal audit; torn, missing, reordered and altered journal evidence; historical invocation binding preservation; release/context mismatch; and wrong executing root. A separate byte-preservation test confirms schema 8 is unchanged. The intermediate 22-test log also includes a structural test subsequently removed as redundant; it is not a substitute for actual-context validation.

The exact accepted control-plane continuation was verified against its original private objects, runtime bytes, fingerprint and predecessor, then adopted through the new journal in an isolated qualification store. Independent process reconstruction selected its exact successor. This was 1.068s, not production pre-model timing. Synthetic authority records are explicitly scoped to qualification; they do not authorize production adoption. See EXACT_C1_QUALIFICATION.json.

Fresh genuine host verification established S3's exact birth identity, parent, implementation, socket/listener, credentials, workspace, cgroup, readiness and unchanged succession head. The check took 0.159s. The sandbox initially hid host PIDs; escalated read-only observation resolved that discrepancy. No launch, restart, signal, ownership or model operation occurred.

## Materiality and unresolved integration

The consumption mechanism is MATERIAL: it changes which authenticated evidence selects the permitted runtime. The original control-plane delta remains NON_MATERIAL_IMPLEMENTATION_CONTINUATION. These classifications are separate.

The consumer is itself new code. Its staged inventory differs from the exact previously qualified successor inventory. The original continuation cannot silently authorize those additional consumer bytes. The material mechanism proposal therefore records the new consumer implementation independently and leaves its material decision unset. A complete installation/bootstrap treatment must establish the consumer's own trust before using it to select a runtime; this must not become circular self-authorization.

The journal and validator components are qualified as stated above, but the ordinary production-context integration and complete production pre-model path have NOT yet been demonstrated with this new consumer. That is an engineering qualification blocker, not merely a missing signature. The earlier 104–105s measurements belong to the previous qualified binding and are not reported as measurements of this new path.

No production material decision was manufactured. PROPOSED_MATERIAL_AMENDMENT.json and PROPOSED_RUNTIME_HEAD_AUTHORITY.json are reviewable proposals, not valid current selectors; null decision fields deliberately prevent treating them as production adoption authority. PUBLICATION.json records exact proposal fingerprints, candidate inventory, existing continuation, unchanged current release/context, and absence of adoption.

Required next closure: qualify the consumer installation/bootstrap trust and ordinary context integration, including its own material implementation identity, then perform the complete bounded production pre-model qualification without a real model request. Only authenticated material authority for that exact mechanism can select its production runtime-head store. Only thereafter can exact C1 production adoption and independent reconstruction establish the requested ready state.

No r13 was created. No invocation was issued or activated, no real ownership acquired, no real model request sent, and no E1 implementation/repository/knowledge effect occurred. Budget and substantive-progress semantics are unchanged. The current real runtime, release and context remain historical current authority; there is no adopted new continuation or new production current head to report.
