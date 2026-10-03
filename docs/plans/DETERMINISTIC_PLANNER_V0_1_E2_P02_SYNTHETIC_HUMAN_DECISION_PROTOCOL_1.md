# E2-P02 Synthetic Human-Decision Protocol

## Protocol status

This document defines a qualification-only protocol. It does not select an
option, issue authority, create choice evidence, or modify Planner state.

`E2_HUMAN_DECISION_PROTOCOL_COMPLETE = YES` as a contract. Runtime
materialization is still required, so `HUMAN_DECISION_READY = NO` and
`E2_P02_RETRY_ALLOWED = NO`.

## Purpose and branch policy

The synthetic decision exists solely to exercise the bounded lifecycle from
an admitted DecisionDossier through an authenticated choice and the native
Planner control path toward `EXTERNAL_WAIT`. It is not production authority,
E1 authority, or a real-world Architect decision.

P02 uses **ALLOW as the positive qualification path**. DECLINE is a required
negative/control branch and must be independently checked, but it does not
count as the positive P02 exit because it does not lead to `EXTERNAL_WAIT`.

## Option semantics

`ALLOW_QUALIFICATION_MAPPING` means that the qualification decision permits
materialization and application of the narrowly scoped synthetic `E2-GRANT`
needed to evaluate the `E2-REENTER` route. It authorizes only the
qualification-only `USE` relation for `E2-REENTER` in the E2 scope and lineage.
It does not authorize production effects, real E1 work, general Planner
authority, proof satisfaction, root/slot satisfaction, external evidence, or
automatic execution.

`DECLINE` means that the qualification authority refuses the bounded mapping
permission. No `E2-GRANT` is issued, no reentry authority becomes applicable,
and the decision path terminates in the deterministic qualification state
`QUALIFICATION_DECLINED`; the external-evidence route is not entered. This is
a qualification result, not an error and not a production denial.

## Issuer and trust

Issuer role: `E2_QUALIFICATION_DECISION_AUTHORITY`.

- Identity domain: qualification-authority identity, distinct from
  `AUTHORITY_IDENTITY` grants and from E1 identities.
- Scope: `E2-QUALIFICATION-ONLY`.
- Decision class: `ARCHITECT_CONTRACT_DECISION` for `E2-DECIDE` only.
- Options: the two dossier options exactly.
- Trust root: the independently pinned E2 qualification protocol artifact and
  its source/content identity, admitted as a qualification-only trust anchor.
- Provenance: source path, content identity, scope, lineage, sequence and
  currentness are mandatory.

No real person or external identity is named. A native trust/issuer
materializer is required to turn this contract into an admissible runtime
entity; the protocol does not self-authenticate its issuer.

## E2-GRANT

The ALLOW branch may produce exactly one qualification grant:

- authority ID: `E2-GRANT`;
- identity domain: `AUTHORITY_IDENTITY`;
- subject/consumer: `E2-REENTER`;
- permitted use: `USE`;
- scope: `E2-QUALIFICATION-ONLY`;
- lineage: `E2-CANONICAL-BASELINE-1`;
- issuer: an admitted `E2_QUALIFICATION_DECISION_AUTHORITY` instance;
- validity: current only for the pinned decision snapshot and sequence;
- provenance: grant source, issuer, dossier, choice evidence, scope and
  lineage;
- applicability predicate: exact selected option, target, permission, scope,
  lineage and current independent predicate.

The grant is not generic Planner authority and cannot satisfy proof, root, or
slot conditions by itself.

## Ordering and evidence

The required order is:

```text
human explicitly selects OPTION_ID
  -> pinned choice-evidence record
  -> RecordedDecision admission
  -> E2-GRANT materialization for ALLOW only
  -> authority applicability evaluation
  -> normal Planner recomputation
  -> external request/absence
  -> EXTERNAL_WAIT
```

Choice evidence is a `PINNED_QUALIFICATION_RECORD` bound to the dossier
identity, `E2-DECIDE`, selected option, issuer identity, scope, lineage,
monotonic sequence/order, canonical content identity and provenance. A future
human interface must accept an explicit option identifier and construct this
record; free-form text and model-generated assertions are not evidence.

The native `RecordedDecision` shape remains:
`decision`, `choice`, `record`, `authority`, and `expected_snapshot`. Native
admission must additionally verify the exact dossier, current applicable
authority predicate, record choice binding, and accepted
`decision-choice:E2-DECIDE` knowledge. The choice record is not created here.

## Independent lifecycle oracles

ALLOW oracle:

```text
HUMAN_HANDOFF
 -> authenticated choice evidence
 -> RecordedDecision admitted
 -> E2-GRANT current and applicable
 -> E2-DECIDE recorded/completed
 -> normal recomputation
 -> E2-REENTER remains governed by external evidence
 -> EXTERNAL_WAIT
```

At the positive P02 exit, expected external evidence is absent, the gate,
receipt route and reentry route are valid, `E2-FINISH` remains blocked,
`ACTIONABLE=[]`, `SELECTED=None`, and `CONTROL=EXTERNAL_WAIT`.

DECLINE oracle:

```text
HUMAN_HANDOFF
 -> authenticated DECLINE choice
 -> RecordedDecision admitted without E2-GRANT
 -> QUALIFICATION_DECLINED terminal qualification state
```

No external wait or reentry is expected on DECLINE.

## Native capability matrix

| Capability | Status |
|---|---|
| issuer identity and trust root | `MATERIALIZER_REQUIRED` |
| pinned choice-evidence record | `MATERIALIZER_REQUIRED` |
| `RecordedDecision` type and native admission | `SUPPORTED` |
| authority entity/predicate | `MATERIALIZER_REQUIRED` |
| authority applicability | `SUPPORTED` once bound inputs exist |
| persistence/replay of new decision objects | `MATERIALIZER_REQUIRED` |
| DECLINE terminal state representation | `MISSING_RUNTIME_CAPABILITY` unless an existing terminal qualification record is adopted |

The protocol is complete as a qualification contract, but runtime readiness is
not. A bounded future implementation/materializer package must add only the
missing qualification objects and preserve native admission semantics.

## Negative controls

The protocol rejects unauthorized or missing issuer, wrong or model-generated
choice evidence, wrong dossier/subject/option/scope/lineage, stale decision,
invalid or non-applicable authority, wrong authority use, duplicate or
conflicting decisions, DECLINE with a grant, and an ALLOW grant escaping E2
scope.

`SELECTED_OPTION=NONE`, `AUTHORITY_ISSUED=NO`, `DECISION_RECORDED=NO`,
`HUMAN_DECISION_READY=NO`, `E2_P02_RETRY_ALLOWED=NO`, and `E2_P03_READY=NO`.

## Qualification result

`ALLOW_SEMANTICS` and `DECLINE_SEMANTICS` are complete qualification-only
contracts. `QUALIFICATION_BRANCH_POLICY` is ALLOW as the positive P02 path
with DECLINE as a required negative/control case. The issuer role, trust
anchor, E2-GRANT scope, choice-evidence binding, RecordedDecision schema, and
both branch oracles are defined above.

`E2_HUMAN_DECISION_PROTOCOL_COMPLETE = YES` means the protocol contract is
closed. It does not mean that runtime objects have been issued or that a
human choice has occurred. `HUMAN_DECISION_READY = NO` because the native
issuer/evidence/grant materializers and the DECLINE terminal representation
are not yet available, and no option has been selected. Consequently
`E2_P02_RETRY_ALLOWED = NO`, `E2_P03_READY = NO`,
`N_REAL_SATISFIED = NO`, and `CANONICAL_E2_QUALIFIED = NO`.

`IMPLEMENTATION_MODIFIED = NO`, `EXPERIMENT_ACTIONS_EXECUTED = 0`,
`E1_ARTIFACTS_MODIFIED = 0`, and `PRODUCTION_EFFECT = NO`.
