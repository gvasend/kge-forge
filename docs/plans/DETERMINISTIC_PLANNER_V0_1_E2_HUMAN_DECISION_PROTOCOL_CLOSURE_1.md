# E2 Human-Handoff Decision Protocol Closure

## Result

`PROTOCOL_CONTRACT_INCOMPLETE`.

The canonical experiment identifies this as a qualification-only synthetic
human choice and the dossier supplies two allowed option identifiers. It does
not define enough semantics to let a human make an informed, later
authenticated choice. In particular, `DECLINE` has no documented control or
downstream consequence, and the issuer, concrete authority binding, selected
choice evidence source, and issuance/authentication record are absent.

## Supported contract

The decision subject is `E2-DECIDE`, an
`ARCHITECT_CONTRACT_DECISION`, with options:
`ALLOW_QUALIFICATION_MAPPING` and `DECLINE`. The dossier states that approval
would be prospective qualification-only `USE` permission for the E2 mapping
target, while excluding production authority, E1 authority, proof
satisfaction, and root/slot satisfaction. No separate option-specific
consequences are authoritative.

The canonical plan says the human choice is a predeclared qualification-only
test input and that a synthetic grant must have an exact type, scope, issuer
trust, and independent applicability predicate pinned before execution. The
current E2 artifacts do not pin those issuer-trust values.

The authority fixture provides only:

- authority identity/domain: `E2-GRANT` / `AUTHORITY_IDENTITY`;
- permission: `USE`;
- subject: `E2-REENTER`;
- scope: `E2-QUALIFICATION-ONLY`;
- lineage: `E2-CANONICAL-BASELINE-1`;
- applicability: exact choice, target, permission, scope, lineage and current
  independent predicate.

It does not define an issuer/owner or native authority entity/predicate.

## Native admission contract

`apply_recorded_decision` accepts a `RecordedDecision` containing
`decision`, `choice`, `record`, `authority`, and `expected_snapshot`. Native
admission additionally requires an applicable `AUTHORITY` predicate bound to a
current authority entity, the exact dossier, scope, selected option, and
accepted knowledge named `decision-choice:E2-DECIDE` whose statement and
provenance match the authenticated record.

This is an existing supported admission path. The missing part is the
authoritative protocol for issuing/materializing its inputs. Conversational
text cannot serve as canonical choice evidence under the current contract.

## Option lifecycle

For `ALLOW_QUALIFICATION_MAPPING`, the only supported sequence is:

```text
human choice -> authenticated choice evidence -> applicable E2-GRANT
-> RecordedDecision admission -> normal Planner recomputation
```

The post-choice control state is not asserted here because the authority and
record are not defined. For `DECLINE`, no authoritative terminal, blocked, or
external-wait transition is specified; it cannot be assigned one in this
closure.

## Readiness

`HUMAN_DECISION_READY = NO`.

Blockers:

- `DECLINE` meaning and consequences are undefined;
- issuer role, identity domain, and trust are undefined;
- concrete authority entity/predicate and applicability binding are absent;
- selected option and authenticated record are intentionally absent;
- choice-evidence source and authentication/ordering mechanism are not
  defined;
- option-specific downstream consequences are insufficient for informed
  choice.

No option was selected, no authority was issued, no decision was recorded,
and no Planner state or E1 artifact was modified.

`NEXT_CONTROL_STEP = PROTOCOL_CONTRACT_INCOMPLETE`.
