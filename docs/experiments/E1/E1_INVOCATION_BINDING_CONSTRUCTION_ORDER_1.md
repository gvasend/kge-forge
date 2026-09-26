# E1 Invocation / Operational Binding Construction Order 1

## Result

`JOINT_DETERMINISTIC_CONSTRUCTION`

The reciprocal relationship is derivation plus post-construction correspondence/applicability validation, not a circular prerequisite. The correct protocol is a joint deterministic construction from common authoritative inputs, followed by independent identity and cross-binding validation.

## Semantics

`INVOCATION_CANDIDATE` represents the exact E1-WP-001 attempt identity, task, dispatch, predecessor/lineage, scope, and invocation-specific authority bindings. Its sources are current dispatch, R12 history, R13 allocation rules, current runtime/context/profile, and applicable Architect/task authority.

`OPERATIONAL_BINDING_CURRENT` represents the canonical binding of invocation, dispatch, OperationalContext, profile, runtime/release, payload/policy, and audit context. It is derived from those independently authoritative inputs and cannot use WorkAuthorization as an input to itself.

The invocation and binding each have an identity body. Correspondence references and consistency digests are validated after construction and are excluded from the other object's identity where they would create recursion.

## Relationship classification

- Invocation → binding: `POST_CONSTRUCTION_BINDING` and `CONSISTENCY_CONSTRAINT`; the binding records the invocation identity after both are derived.
- Binding → invocation: `DERIVATION` input plus `APPLICABILITY_CONSTRAINT`; the binding must agree with the exact invocation, but the invocation's final identity is not a prerequisite for constructing the common-input body.

Neither direction is a final-identity construction prerequisite.

## Construction protocol

1. Resolve common current authorities: R4/G4, ReleaseAuthority, OperationalContext, CurrentDispatch, released profile/Programmer Profile, payload/provider/retention/transmission/content clearance, R12 history, R13 allocation, audit policy, and task scope.
2. Construct the invocation candidate body and binding body from those inputs using the qualified canonical serializers, excluding reciprocal final-identity metadata from identity bodies.
3. Derive both identities independently.
4. Insert canonical correspondence references/digests.
5. Recompute canonical full objects and verify both identities, shared InvocationAttemptId, dispatch/context/runtime/profile/policy equality, and applicability.

## Identity recursion test

No hash(A)↔hash(B) recursion is required. Each identity hashes a body made from common authoritative inputs. Reciprocal identity references are correspondence metadata validated after derivation, not identity-bearing prerequisites. WorkAuthorization remains downstream.

## Runtime state

Construction requires no ACTIVE state, ownership reservation, repository effect, or execution effect. Runtime remains `NOT_ACTIVATED`; ownership remains `NONE_NOT_YET_RESERVED`. Activation and ownership are later lifecycle transitions.

## Actionability

`NEXT_OPERATION = joint deterministic invocation/binding construction and validation`.

`OPERATION_CLASS = DETERMINISTIC_CONSTRUCTION`.

Both blocked nodes become jointly actionable under the corrected semantics because their common authoritative inputs are satisfied and no runtime state is required. This review does not construct them or change status.

`AUTHORITY_REQUIRED = NO`\n`PRODUCTION_EFFECT = NO`\n`NEW_DEPENDENCY_DISCOVERED = NO`\n`BASELINE_DEFECT = NO`
