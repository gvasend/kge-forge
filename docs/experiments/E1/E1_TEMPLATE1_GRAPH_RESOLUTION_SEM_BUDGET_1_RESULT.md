# E1 Template-1 graph resolution — SEM-BUDGET result 1

## Result and boundary

ACTION_RESULT = AUTHORITY_REQUIRED. ROOT_CONDITION_TRANSITION = UNCHANGED. SLOT_TRANSITION = UNCHANGED. SEM-BUDGET is attempted/blocked, not completed.

Exact root condition: the governing contract has not selected the canonical semantic type/representation for authenticated_inputs.budget_policy: authority identity, policy body, or typed projection. The existing budget values and authority record do not themselves determine this choice. The action explicitly requires “Establish exact policy/reference representation without changing bounds. Unaddressed policy choices return AUTHORITY_REQUIRED.” This is that anticipated branch, not an unexpected plan/contract exception.

## Recomputed selection and actionability

All four plan-input hashes and completed-action result identities matched persisted state. Recomputed ACTIONABLE contained 11 actions. The validated selector returned SEM-BUDGET at Criterion 5. The action has no prerequisite or external-gate requirements to begin bounded semantic review; its referenced sources are available. SEMANTIC_RESOLUTION / NON_EFFECTING permits read-only analysis under contract-definition scope. It does not permit issuing a new governing choice. Required authority to settle that choice was not inferred. No other action was executed.

## Directly established observations

- **SEM-BUDGET-K1**: Existing StatusBudgetAuthority canonical body recomputes to its declared authority identity, length 1189 bytes; existing bounds remain unmodified.
- **SEM-BUDGET-K2**: The governing contract leaves authority-identity versus policy-body versus typed-projection representation undefined. Constructor key inclusion/hash behavior does not choose that semantic type.
- **SEM-BUDGET-K3**: An exact field representation and canonical source-to-field projection decision is required before SEM-BUDGET can complete; no candidate representation is approved by this result.

The exact inspected authority is `StatusBudgetAuthority-sha256:02cc22de4ad70612c8b1e39e4df6f3bf8733c777d4729fb66d59d519fc6edc99`, scope `LIVE_R4/G4/E1-WP-001/FIRST_PROGRAMMER_EXECUTION`, lineage `R4-final CURRENT UNIQUE`. Sorted-key compact UTF-8 JSON excluding authority_id reproduces its identity over 1189 bytes. This is source-byte verification, not fresh publication or applicability qualification.

Existing policy, recorded without modification:

```json
{
  "schema": "E1-RUN-CONTROL-1",
  "seconds": {
    "cycle": [
      120,
      300
    ],
    "no_progress": [
      180,
      300
    ],
    "invocation": [
      1200,
      1800
    ],
    "phase": [
      30,
      120
    ]
  },
  "requests": [
    8,
    12
  ],
  "tokens": [
    100000,
    150000
  ],
  "automatic_retry": false,
  "usage_unknown": "TIME_AND_REQUEST_LIMITS_ONLY"
}
```

The record also preserves single-use/no-expansion, hard-exhaustion cancellation, durable recovery without reset and FAIL_CLOSED escalation. No bounds, counters or runtime state were changed.

Closure Plan §1A explicitly calls for selecting policy values, authority identity or typed projection; Production Contract Decision line 43 repeats the undefined type/mapping. The production contract’s “Budget-policy value” label does not specify exact canonical bytes/type or authorize dropping the authority/source linkage. Constructor _body requires the key and preserves the supplied value; artifact() includes it in the digest. It supplies no budget-specific selector or type validation resolving that ambiguity. Accepting a JSON value into a hash does not establish its semantic authority.

A bounded governing decision must specify the exact representation and source/provenance projection, preserving current bounds and scope. This report does not choose among alternatives, issue that decision, create a new plan action, implement a validator, or perform MAP-BUDGET/CONTRACT-T1. Review stops at the explicit authority requirement. The previously recorded ignored state/revision condition and other blocked/completed actions were not reevaluated.

## Provenance

Every observation retains producing-source indices in execution_history. Raw artifact SHA-256 values below are distinct from the canonical authority identity. A source identity change stales the observations derived from it and requires revalidation.

| Index | Source | Raw SHA-256 | Location |
|---|---|---|---|
| 0 | `docs/experiments/E1/E1_TEMPLATE1_PRODUCTION_CONTRACT_CLOSURE_PLAN_1.md` | `sha256:bf88220168766599236a22d34f88686fb943bd55682ef4458046d84c36e6eaaf` | §1A budget_policy row; §2 WP-12; §3 contract-definition scope; §6/7 |
| 1 | `docs/experiments/E1/E1_TEMPLATE1_CLOSURE_WP12_RESULT.md` | `sha256:f5f2dfc5ddddb510cb469e19720667a3cb36e95beb6c3f2fd283696d3cea9d7f` | Bounded evidence and limits: budget representation not selected |
| 2 | `docs/experiments/E1/E1_WORKAUTHORIZATION_TEMPLATE1_PRODUCTION_CONTRACT_1.md` | `sha256:1af1f3aac2acc34aefb8c0b2a9a6fb775de152f2f8db6eaf6dd0673458ea6b6a` | line 46 budget_policy rule gap |
| 3 | `docs/experiments/E1/E1_WORKAUTHORIZATION_PRODUCTION_CONTRACT_DECISION_1.md` | `sha256:b916edc33d1534b516a187118146364c88aa360f0c8ff4f2dcc91a205aca1ad6` | line 43 budget_policy expected type and canonical mapping; line 49 provenance requirements |
| 4 | `docs/experiments/E1/E1_HOST_PREREQUISITE_AUTHORITY_ISSUANCE_1.md` | `sha256:5cf24bf05643e69543a9db154af7e2a6edc1943fe32280ea7d7762b06a43132f` | second JSON block: StatusBudgetAuthority /policy, /scope, /lineage, /authority_id |
| 5 | `adapter/invocation_constructor.py` | `sha256:5908b257fdc7325d94d7524fbacbe3a7ec26d18d98507d6232c9ba1d41e8f9f7` | _body required keys and return; artifact digest construction; construct_work_authorization |

## Persisted state and readiness

Only SEM-BUDGET becomes blocked with AUTHORITY_REQUIRED. Its observed source verification and unresolved decision need are retained as bounded knowledge, not a successful representation proof. Root:budget and authenticated_inputs.budget_policy remain unresolved under their existing independent satisfaction rules. The typed graph remains byte-for-byte unchanged; its existing mapping gap is not replaced by an inferred relationship.

Partition: 10 actionable, 43 blocked, 3 completed (S-BINDING, S-CONTEXT, S-EXEC). No newly actionable action. DEC-EXEC remains prerequisite-ready for the Architect, not issued or executed. All 28 root conditions and 41 slots remain unresolved; 2 slots were previously established. Source/mapping/consumer/validator completeness remains false, so Template-1 construction and Candidate-3 resumption readiness remain NO. Candidate-3 authority remains valid and unconsumed as recorded.

Next selection is SEM-ELIGIBILITY at Criterion 5. It was not executed.

```text
ACTION = SEM-BUDGET
ACTION_RESULT = AUTHORITY_REQUIRED
ACTION_KNOWLEDGE_PRODUCED = ["SEM-BUDGET-K1", "SEM-BUDGET-K2", "SEM-BUDGET-K3"]
ROOT_CONDITION_TRANSITION = UNCHANGED
SLOT_TRANSITION = UNCHANGED
ROOT_CONDITIONS_RESOLVED = []
ROOT_CONDITIONS_REMAINING = 28
SLOTS_RESOLVED = []
SLOTS_REMAINING = 41
ACTIONABLE = ["DEC-EXEC", "PREP-AUDIT", "PREP-BINDING-GRANT", "PREP-RUNTIME_HEAD", "PREP-SUPERVISOR", "PREP-VALIDATOR", "SEM-ELIGIBILITY", "SEM-IGNORED", "SEM-IMPLEMENTATION", "SEM-INTERFACES"]
NEXT_ACTION = SEM-ELIGIBILITY
DECIDING_CRITERION = 5
RESOLUTION_PLAN_EXCEPTION = NO
TEMPLATE1_CONSTRUCTION_READY = NO
CANDIDATE3_RESUMPTION_READY = NO
PRODUCTION_EFFECT = NO
```
