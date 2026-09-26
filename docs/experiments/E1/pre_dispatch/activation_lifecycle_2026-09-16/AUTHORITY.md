# Authorization lifecycle qualification authority — 2026-09-16

Authority: the Architect's current instruction accepting the blocked dispatch
and requiring a qualified append-only INACTIVE → ACTIVE lifecycle transition.
This is implementation/qualification authority, not a new dispatch authorization.

The existing invocation identity is preserved:
`auth-e1-wp-001-r7-94f511dfcdcc43ac837191f8732ced39`.
The existing immutable Architect dispatch record is
`../dispatch_authorization_2026-09-16/DISPATCH_RECORD.json`, SHA-256
`08f721ab75f001d5b2a4a91c259cf52174b78d4060e0d0ecacdcc2b7ae1abaf7`.

The Architect required preservation of the historical INACTIVE authorization,
an identity-bound durable activation event, ordered recovery, a complete atomic
dispatch validation before activation, twelve specified synthetic negative and
positive qualification cases, and independent ACTIVE reconstruction before any
model request. Ownership reservation and profile activation must also succeed
before reporting ACTIVATED_AND_READY_TO_DISPATCH.

The Architect explicitly instructed:

> If any previously authorized binding has changed materially, stop and return to the Architect.
>
> Do not create a new Architect dispatch authorization.
>
> Do not dispatch E1-WP-001 during this qualification.

No current instruction permits silently replacing the existing operational
implementation pins, FullContextDigest, ModelProjectionDigest, audit path, or
authorization identity. Qualification does not itself revise these bindings.
