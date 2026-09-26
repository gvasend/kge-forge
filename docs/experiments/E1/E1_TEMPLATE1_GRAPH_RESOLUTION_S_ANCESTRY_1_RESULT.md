# E1 Template-1 graph resolution — S-ANCESTRY result 1

## Result and boundary

**BLOCKED**. Acquisition outcome: **NOT_FOUND within the defined inspected source set**. No exact current allocation, predecessor and session/turn owning record was acquired. This is not a claim that such evidence cannot exist elsewhere. No authority or mapping was inferred.

The action explicitly permits a NOT_FOUND acquisition outcome without completing root resolution. The plan states that absent sources block dependent mapping. Consequently this is a recorded unsuccessful acquisition, not a completed prerequisite or PASS. `root:ancestry` and its predecessor slot remain unresolved. This is the existing source gap, not an unexpected issue: `RESOLUTION_PLAN_EXCEPTION = NO`.

## Selection and actionability

The graph SHA-256 still matches the validated policy snapshot; all four authoritative plan-input hashes match. Recomputing from zero completed actions and existing external gates yields the original 15 eligible actions. Criteria 1 and 2 remain non-decisive, Criterion 3 retains five source-acquisition actions, effect/cost does not distinguish them, and Criterion 5 selects S-ANCESTRY.

S-ANCESTRY has no prerequisite actions or external prerequisites. Its referenced closure plan and WP-01 report exist and match their recorded identities. The user authorizes this read-only acquisition; contract-definition scope suffices. No grant for construction, issuance, activation or mapping is inferred. Missing sought source values are the bounded acquisition outcome, not an unmet prerequisite to beginning the inspection.

## Exact findings

- Current candidate `InvocationAttempt-sha256:e89c032eb0b0a006b041e3b0ddf0093d8d8b7a7f30882ac21f9ab05b0eb8bbfa`: `/allocation = R13_NAMESPACE`, `/predecessor = R12_HISTORY`, `/ownership = NONE_NOT_YET_RESERVED`, `/runtime_state = NOT_ACTIVATED`; no top-level session_id or turn_id. Canonical identity and 2300-byte length recomputed successfully. These labels do not identify an authenticated current allocation or session/turn owning source.
- Current dispatch identity and 2167-byte canonical length recomputed successfully. It likewise records ownership NONE_NOT_YET_RESERVED; it supplies no missing attempt-chain projection.
- The cited CURRENT_CANONICAL_R13_BINDING.json has concrete historical `/invocation_identity/session_id = session-e1-run2-r13-current`, `/invocation_identity/turn_id = turn-e1-run2-r13-current`, `/invocation_identity/authorization_id = auth-e1-wp-001-r13-current`, revision 13. Its InvocationAttemptId is `InvocationAttempt-sha256:5f2c6a1582f88a23a8e92caa04e82404469dc15a525a791727f95b5e94bf063c`, different from the current candidate. Its predecessor authorization is `auth-e1-wp-001-r12-86af4f6e7bb64eb384108dec11692c86`. These fields cannot be rebound to the current candidate.
- The R12_PREDECESSOR.json historical record states `/safe_predecessor = ACTIVE_CANCELLED_PRE_MODEL_NO_EFFECTS`, `/lifecycle/state = CANCELLED`, `/ownership = null`, `/new_attempt_created = false`. It corroborates R12 history; it does not establish a current owning allocation or the current typed predecessor value.
- Joint-construction evidence establishes independently hashed candidate identities and post-construction correspondence, retaining NOT_ACTIVATED / NONE_NOT_YET_RESERVED. It supplies no missing session/turn owning record.

Inspection followed only WP-01/Closure Plan references for current invocation/dispatch, historical R12/R13 allocation and joint construction. No runtime stores, authority publication, alternate-source search, sibling action or recursive repair was performed.

## Provenance

Raw-file SHA-256 values below identify the exact inspected bytes; they are distinct from declared canonical object identities. Source changes stale this result’s derived observations and require revalidation. Historical observations are not live runtime qualification.

| Source | Raw SHA-256 | Location |
|---|---|---|
| `docs/experiments/E1/E1_TEMPLATE1_PRODUCTION_CONTRACT_CLOSURE_PLAN_1.md` | `sha256:bf88220168766599236a22d34f88686fb943bd55682ef4458046d84c36e6eaaf` | §1 predecessor and session/turn rows; §2 WP-01/WP-07; §6–7 readiness |
| `docs/experiments/E1/E1_TEMPLATE1_CLOSURE_WP01_RESULT.md` | `sha256:bda7ec419589f732bcd362a4e6ab822bcfb4bbe057844f7b95e0856d100ebe8d` | §2 Current invocation candidate / Existing binding record / Attempt ancestry; §3 |
| `docs/experiments/E1/E1_INVOCATION_CANDIDATE_1.json` | `sha256:c0fdde77ba3dddd1fcaecc798b5a7252e5b333238063aec750bbaa522ede7c6a` | /identity; /allocation; /predecessor; /ownership; /runtime_state; absent /session_id and /turn_id |
| `docs/experiments/E1/E1_CURRENT_DISPATCH_1.json` | `sha256:475861a32de000a8527074748bfbaaf8b0b0efa6e405e9a3f9a0a1f27dfc7b35` | /identity; /ownership; /runtime_state |
| `docs/experiments/E1/run2_r13_preparation_2026-09-19/CURRENT_CANONICAL_R13_BINDING.json` | `sha256:19cc4d0311e62fad0b8c29acce5af9b7a2a59bf16e6364e87c17cb3804a7bfaf` | /InvocationAttemptId; /invocation_identity; /predecessor |
| `docs/experiments/E1/run2_control_plane_2026-09-18/R12_PREDECESSOR.json` | `sha256:d5d0d3387488ea0d21f3fb746e4a832b919d953c1c9d53c06f9cc185e82de0e1` | /safe_predecessor; /lifecycle/state; /lifecycle/effective_authorization/authorization_id; /ownership; /new_attempt_created |
| `docs/experiments/E1/E1_INVOCATION_BINDING_JOINT_CONSTRUCTION_1.md` | `sha256:63af55bd888dfb4ea2dac81b5e9c36b5c472415889777e928268e287462f68f4` | Result; final runtime/ownership paragraph |

Extraction: read-only exact fields and cited report sections; canonical hashing applied only to the two current candidate objects.

## Recomputed state

No accepted complete proof: 28 cut conditions unresolved; 2 previously established slots and 41 unresolved slots; zero completed actions, one attempted/blocked action. S-ANCESTRY is blocked pending new qualifying source evidence. MAP-ANCESTRY and BUILD-BINDING remain blocked on accepted S-ANCESTRY output and their other prerequisites. Fourteen actions remain actionable, 42 blocked, none newly actionable.

The typed graph is byte-for-byte preserved because the result confirms its existing missing-source state and establishes no new relationship. The plan records the result and provenance without altering topology or unrelated action definitions. Readiness remains false under incomplete sources/mappings/contracts/validator gates. The previous selection attempt and policy dry run remain historical records; the latest execution_state is current.

Applying the policy to the remaining set yields S-APPROVAL at Criterion 5. It was not executed. Candidate-3 construction authority remains valid and unconsumed as recorded.

```text
ACTION = S-ANCESTRY
RESULT = BLOCKED
ROOT_CONDITIONS_RESOLVED = []
ROOT_CONDITIONS_REMAINING = 28
SLOTS_RESOLVED = []
SLOTS_REMAINING = 41
ACTIONABLE = ["PREP-AUDIT", "PREP-BINDING-GRANT", "PREP-RUNTIME_HEAD", "PREP-SUPERVISOR", "PREP-VALIDATOR", "S-APPROVAL", "S-BINDING", "S-CONTEXT", "S-EXEC", "SEM-BUDGET", "SEM-ELIGIBILITY", "SEM-IGNORED", "SEM-IMPLEMENTATION", "SEM-INTERFACES"]
NEXT_ACTION = S-APPROVAL
DECIDING_CRITERION = 5
RESOLUTION_PLAN_EXCEPTION = NO
TEMPLATE1_CONSTRUCTION_READY = NO
CANDIDATE3_RESUMPTION_READY = NO
PRODUCTION_EFFECT = NO
```
