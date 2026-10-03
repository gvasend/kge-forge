# O09 baseline slot-proof admission contract 1

O09_EXECUTABLE = YES. C06A_3_RETRY_ALLOWED = YES at the contract gate; no implementation package is executed by this record. Restored-and-qualified coverage remains **2/17**.

This additive specification fills the specific baseline-proof admission gap recorded in [C06A-3](DETERMINISTIC_PLANNER_V0_1_C06A_3_RESULT.md). It does not modify the baseline registry or reinterpret either slot as full consumer acceptance. It does not change the prior blocked result.

## Governing evidence and exact subjects

The [remaining-contract matrix](DETERMINISTIC_PLANNER_V0_1_C06A_REMAINING_CONTRACT_1.json) assigns O09 and its two baseline proof tests to C06A-3. The [completion registry](DETERMINISTIC_PLANNER_V0_1_C06A_2_ORACLE_COMPLETION_1.json), `/family_rules/root_slot/target_registry`, names the targets below. Their identities are independently corroborated by the frozen graph and original closure results, not inferred from the generic `slot:qualified` fixture.

| Contract member | Invocation baseline | Profile baseline |
|---|---|---|
| SLOT_ID | `slot:authenticated_inputs.InvocationAttemptId` | `slot:authenticated_inputs.profile_sha256` |
| SLOT_TYPE | TEMPLATE1_SLOT / authenticated input | TEMPLATE1_SLOT / authenticated input |
| VALUE_TYPE | JSON string; INSTANCE_IDENTITY | JSON string; CONTENT_IDENTITY |
| Value | `InvocationAttempt-sha256:e89c032eb0b0a006b041e3b0ddf0093d8d8b7a7f30882ac21f9ab05b0eb8bbfa` | `83b8cbc0549c64d21eaccaffc1fa45b49be368a878ccecdf9572d476477dfcd6` |
| Producer/source | Existing current InvocationCandidate, `/identity` | Released profile candidate content, selected by release record |
| Accepted mapping | Verified candidate identity string, unchanged | Verified released candidate content SHA-256 component, without identity prefix |
| PROOF_TYPE | `ACCEPTED_BASELINE_SLOT_COMPLETION_1` | `ACCEPTED_BASELINE_SLOT_COMPLETION_1` |
| Resolution scope | `Candidate identity only, no issuance/use` | `Released profile content digest, not authority ID` |
| Root dependencies | Empty, as recorded in graph | Empty, as recorded in graph |
| Source dependencies | Candidate bytes and WP-01 accepted slot result | Candidate bytes, profile release record, WP-08 accepted mapping/slot result |
| Consumer | `consumer:constructor`, `authenticated_inputs.InvocationAttemptId` | `consumer:constructor`, `authenticated_inputs.profile_sha256` |

Exact original acceptance evidence:

- [WP-01](../experiments/E1/E1_TEMPLATE1_CLOSURE_WP01_RESULT.md), “Current invocation candidate” and acceptance table “Exact InvocationAttemptId”: hash and 2,300-byte canonical body agree; **WP-01 overall remains BLOCKED**. This directly resolves only candidate identity. Missing canonical binding, attempt-chain projection and dispatch mapping remain missing.
- [InvocationCandidate](../experiments/E1/E1_INVOCATION_CANDIDATE_1.json): body excluding `identity` and `canonical_byte_length`, compact sorted-key UTF-8 JSON, produces the prefixed identity. Scope/runtime/controller-store are body fields. `predecessor = R12_HISTORY` and `allocation = R13_NAMESPACE` are declared labels, not proof of canonical ancestry.
- [WP-08](../experiments/E1/E1_TEMPLATE1_CLOSURE_WP08_RESULT.md), “Accepted mapping”: released profile content is the consumer's intended domain. It explicitly excludes root authority, release authority and ProgrammerProfile identities. The 2,390-byte candidate body independently hashes to the accepted value.
- [Profile candidate](../experiments/E1/E1_CURRENT_PROFILE_ROOT_CANDIDATE_1.json) and [candidate identity rule](../experiments/E1/E1_CURRENT_PROFILE_ROOT_CANDIDATE_1.md): canonical body excludes the derived identity and length fields.
- [Profile release](../experiments/E1/E1_CURRENT_PROFILE_RELEASE_1.md), sole JSON block in “Issued authority”: `candidate_profile_identity` binds that exact content; `authority_id` authenticates the release identity body excluding `authority_id`. The release digest is not the slot value.
- [Frozen graph](../experiments/E1/E1_TEMPLATE1_TYPED_KNOWLEDGE_GRAPH_1.json), entities selected by the two exact slot IDs: current-state cache, resolved values, limited scopes, identity types and partial pipeline statuses. Graph pointers are stored in each profile's provenance. The graph label alone is not the proof.

The backlog's artifact provenance/invalidation, identity-domain separation and independent root/slot satisfaction rules govern both predicates. Source and governing-input raw SHA-256 pins are in the companion contract; the existing registry is untouched.

## Admission boundary and currentness

These predicates admit **restoration of the accepted, limited result at the pinned frozen snapshot**. They do not authenticate new live authority, reacquire evidence, revalidate a production request, or resume E1.

A value existing is insufficient. A hash transform existing is insufficient. Accepted source knowledge alone is insufficient. Acceptance requires the named slot-completion proof, the accepted WP source/mapping record, exact documentary source bindings, independently admitted snapshot validity, and all clauses below. Only then is `SLOT_RESOLVED` supported **within the recorded resolution scope**.

Currentness is `CURRENT_AT_PINNED_SNAPSHOT`, relative to the graph content identity in the profile, not wall-clock time or identity stability. `HISTORICAL_ONLY_UNBOUND` and `LIVE_CURRENT` claims both fail. Frozen historical bytes can support the bounded snapshot result; historical bytes cannot silently prove a different or present-day envelope. No arbitrary timestamp expiry is added because the baseline records provide no such rule.

The harness/governed admission boundary independently pins the profile and currentness/invalidation view. Neither is an untrusted proof's permission flag. The evaluator cannot discover revocations or authenticate a caller-selected profile; an integration that lets the submitted proof replace either trusted input violates this contract. Both inputs, their pins and invalidations must be persisted and restored, not reconstructed from prior acceptance or conversation.

## Typed executable predicates

[Machine-readable contract](DETERMINISTIC_PLANNER_V0_1_O09_BASELINE_SLOT_PROOF_ADMISSION_1.json) contains two complete profiles and an executable, standard-library-only reference specification. It imports no planner code, reads no files, calls no services and performs no state transition. No imported runtime artifact may cause this embedded program to be executed.

Named entry points are the fixed profiles of:

```text
ADMIT_SLOT_PROOF_InvocationAttemptId_1(profile, state, currentness)
ADMIT_SLOT_PROOF_profile_sha256_1(profile, state, currentness)
    -> ACCEPT / REJECT(failed_clause)
```

They dispatch through `admit(profile,state,currentness)`; there are no supplied callbacks or implementation-derived acceptance decisions. The independently pinned profiles fix the two slot bindings and mapping rules.

| Input | Type, identity domain and purpose |
|---|---|
| `state` | Exact `O09-SLOT-PROOF-INPUT-1` keys; `SYNTHETIC_QUALIFICATION_ONLY` mode and independent profile digest |
| `proof` | Exact `O09-SLOT-PROOF-1` object; missing is rejection |
| `proof.identity` | CONTENT_IDENTITY, `O09SlotProof-sha256`, SHA-256 of canonical proof body excluding identity; not authority |
| `predicate`, `slot` | Exact registered predicate name and SlotId string; no cross-slot substitution |
| `value`, `value_domain` | Exact string and distinct INSTANCE_IDENTITY or CONTENT_IDENTITY tag, as above |
| `proof_type` | `ACCEPTED_BASELINE_SLOT_COMPLETION_1`; not ACTION_PASS or ACCEPTED_KNOWLEDGE |
| `scope` | Exact limited resolution scope, separate from operational envelope scope |
| `lineage` | Invocation: exact predecessor/allocation declarations only. Profile: exact `R4-final CURRENT UNIQUE` lineage from candidate/release. No inferred equivalence between these forms |
| `envelope` | Exact scope `LIVE_R4/G4/E1-WP-001/FIRST_PROGRAMMER_REQUEST`, runtime and controller-store references from sources |
| `provenance` | Mapping/extraction version, exact role/path/raw CONTENT_IDENTITY/selector bindings, graph content identity and slot pointer |
| `prerequisites` | Fixed source identity-verification requirement, accepted mapping source, limited scope and empty graph root-dependency list. Verified by source checks, not by a supplied producer-COMPLETED flag |
| `mapping` | Exact versioned source/selector/transform/accepted-result/target tuple |
| `supports` | Exact required role-to-source pin bindings; no extra/missing/dangling role |
| `documents` | UTF-8 documentary texts for exactly those roles; raw hashes must match independently admitted pins |
| `currentness` | Exact snapshot/evaluation/source-status map with identity per role; every required source current at that snapshot, none stale/invalid/missing |

Canonical JSON: sorted object keys, compact separators, UTF-8, retained array order, no floats/non-JSON values; duplicate object keys are rejected when parsing source JSON. Raw documentary identities and canonical semantic identities are different domains. Release authority identity is checked as a release binding, never returned as content identity.

## Predicate clauses and positive proof

The reference returns the first failed clause in this stable order:

| Clause | Required truth |
|---|---|
| C00_SCHEMA | Exact input/proof schemas, qualification mode and admitted profile binding; malformed input fails closed |
| C01_PROOF_REQUIRED | Named completion proof present |
| C02_TARGET | Exact slot and predicate match |
| C03_COMPLETION_PROOF_TYPE | Completion proof type, not generic knowledge or action result |
| C04_VALUE_DOMAIN | Exact JSON string value and identity domain |
| C05_SCOPE | Limited baseline resolution scope unchanged |
| C06_LINEAGE | Exact applicable source lineage/declaration tuple |
| C07_ENVELOPE | Same scope/runtime/G4-controller-store envelope as profile |
| C08_PREREQUISITES | Required source verification/mapping/scope/dependency contract retained |
| C09_PROVENANCE | Exact source selectors, raw pins, graph binding and extraction version retained |
| C10_MAPPING | Registered identity projection, target and acceptance source retained |
| C11_SUPPORT_BINDINGS | Every named source role bound to its exact typed pin |
| C12_CURRENTNESS | All support valid in the independently admitted snapshot view |
| C13_SOURCE_BYTES | Actual supplied documentary bytes agree with every pin |
| C14_SOURCE_IDENTITY | Candidate identity and canonical byte length recompute; correct candidate schema/type and slot projection |
| C15_SOURCE_CORRESPONDENCE | Candidate envelope/declared lineage agree; for profile, release identity recomputes and binds exact candidate, lineage, runtime and controller-store |
| C16_ACCEPTANCE_RECORD | Required exact WP acceptance statements present in the pinned result, not a caller's PASS claim |
| C17_PROOF_IDENTITY | Proof content identity recomputes with all bindings |

Minimum positive proof requires precisely the two source roles for invocation and three for profile. Dispatch, canonical binding, status budget, audit and invocation issuance are not additional completion prerequisites for these limited baseline slots. Requiring WP-01 COMPLETED would contradict its accepted result and refined C06 semantics.

For profile, checking the recorded release establishes which candidate's content was selected at the snapshot. It grants no permission to consume a single-use authority now. Profile-root authority and other nested references remain pinned source content; this predicate does not recursively requalify them or claim they are usable for effects.

The two positive fixtures use the actual baseline SlotIds and values, with newly synthesized qualification-only proof objects. Documentary bytes are copied from the pinned records above. They are not new authority records or evidence for E1. Every proof member serves a clause in the table; no opaque callback can declare completion.

## Negative fixtures and source invalidation

[Fixture companion](DETERMINISTIC_PLANNER_V0_1_O09_BASELINE_SLOT_PROOF_ADMISSION_1_FIXTURES.json) contains **2 positives and 52 negatives**, each with exact expected failed clause. Cases cover both slots:

- missing proof (C01); wrong/other-baseline slot (C02);
- action PASS or accepted knowledge in place of completion proof (C03);
- integer value, placeholder or AUTHORITY_IDENTITY substitution (C04);
- enlarged scope, wrong lineage and incompatible runtime envelope (C05–C07);
- unresolved/missing prerequisite, missing provenance or wrong mapping (C08–C10);
- missing or dangling/wrong source binding (C11), substituted source bytes (C13);
- historical-only, inferred live currentness, wrong snapshot, and every required source individually STALE or INVALID (C12);
- altered proof identity (C17).

Except the proof-identity case, mutated proofs are rehashed before evaluation, so rejection is not merely a corrupt enclosing hash. Raw source substitution is intentionally rejected at C13 before semantic parsing; pins are not relaxed to force a later clause. Identity and release correspondence checks execute on both applicable positive sources.

For each of the **five source roles across the two profiles**, validation also runs this sequence:

```text
accepted proof -> JSON persist/reload -> required source becomes STALE
-> JSON persist/reload -> REJECT(C12_CURRENTNESS)
```

The proof object itself remains unchanged. The persisted source validity view withdraws support. An importer must propagate that loss through its existing proof/dependency mechanism and recompute dependent conclusions; it must not restore a cached resolved boolean over the rejection. The specification tests the rejection after reload, not a planner recomputation implementation. That integration remains C06A-3 work.

Restoring validity requires independently accepted source revalidation for the same contract. Merely clearing a stale flag, rehashing a proof or changing a historical producer to COMPLETED is not authorized by this specification.

## Registry relationship and composition

The registry must eventually associate each exact baseline SlotId with:

- its `ADMIT_SLOT_PROOF_<name>_1` predicate;
- `O09-SLOT-PROOF-1` schema and `ACCEPTED_BASELINE_SLOT_COMPLETION_1` type;
- independently pinned profile identity and source-role domains/selectors;
- existing INSTANCE_IDENTITY or CONTENT_IDENTITY value requirement;
- the exact baseline resolution scope and graph/snapshot binding.

These bindings are supplied in `/registry_bindings_required` in the contract JSON. The existing registry is **not modified**. Future implementation should integrate these named predicates with existing typed proof/persistence mechanisms; it must not use the reference as a second runtime, require historical producer completion, or restore proof satisfaction from a copied graph label.

For composition, both profiles must refer to the same pinned graph snapshot and identical target scope/runtime/controller-store when used in one envelope. Each profile validates those fields against independently pinned source bytes. Profile release-to-candidate identity is checked explicitly. Invocation predecessor/allocation are not equated to profile lineage; invocation `released_profile` is a source-pinned reference, not an inferred content identity. Graph/body hash equality cannot replace a domain conversion. Invalidation and acceptance records remain role-specific.

## Executability, retry and validation

O09 now has both baseline-specific positive profiles, negative clauses/fixtures, source invalidation, reload semantics and registry binding instructions. The prior completion records no other missing C06A-3 prerequisite; the blocked C06A-3 check records only this O09 gap. The pinned mapping/completion inputs remain unchanged. Accordingly **C06A_3_RETRY_ALLOWED = YES** for a new package attempt under these additive predicates. This is contract readiness, not conformance or permission to execute in this task. C06A-3 must still reproduce its implementation gaps and satisfy every assigned test; any newly discovered mismatch must fail closed.

[Validation companion](DETERMINISTIC_PLANNER_V0_1_O09_BASELINE_SLOT_PROOF_ADMISSION_1_VALIDATION.json) records:

- 2/2 positive ACCEPT and 52/52 negative REJECT with exact expected clause;
- all 54 cases preserve results through JSON round trip;
- all five accepted-then-invalidate sequences reject after reload without changing proof;
- source raw pins verified against read-only originals;
- reversed case/object-key order and three independent processes with hash seeds 0, 17 and 113 produce identical semantic digest `5eb7024bbe72f199e9195e7cda741d53c95741365b4483e815b87702c116315e`.

The initial temporary output-digest harness used tuples, which the JSON-only canonicalizer correctly rejected. Replacing those harness rows with JSON arrays allowed all three seed runs; no predicate semantics or implementation changed.

No planner implementation/test qualification, C06A-3, C07 or E1 action was executed. This task adds only four specification/result companions. Protected pre-existing files and all 10,911 E1 files are verified unchanged; local links, JSON and `git diff --check` pass.

## Report

```text
BASELINE_SLOT_PROOFS = [slot:authenticated_inputs.InvocationAttemptId,
                       slot:authenticated_inputs.profile_sha256]
ADMISSION_PREDICATES = [ADMIT_SLOT_PROOF_InvocationAttemptId_1,
                        ADMIT_SLOT_PROOF_profile_sha256_1]
POSITIVE_FIXTURES = [POS-InvocationAttemptId, POS-profile_sha256]
NEGATIVE_FIXTURES = 52, individually identified in fixture companion
SOURCE_INVALIDATION_RULES = [each required support invalidates its slot proof;
                             persisted invalidity survives reload]
REGISTRY_BINDINGS_REQUIRED = [two entries in contract companion; not installed]
O09_EXECUTABLE = YES
O09_MISSING_ELEMENTS = []
C06A_3_RETRY_ALLOWED = YES
C06A_3_RETRY_PREREQUISITES = [prior mapping/completion contracts pinned,
  both baseline profiles executable, positives/negatives PASS,
  invalidation/reload PASS, registry bindings specified,
  no additional recorded prerequisite missing]
RESTORED_AND_QUALIFIED = 2/17
C06A_4_READY = NO
C07_RETRY_ALLOWED = NO
F03_STATUS = CLOSED
V0_1_CURRENT_STATUS = CORRECTION_REQUIRED
IMPLEMENTATION_MODIFIED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
```
