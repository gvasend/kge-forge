# E1 preparation decisions — 2026-09-11

Authority: Architect under E1-ARCH-1 and the user's instruction to satisfy
pre-dispatch prerequisites and prepare the first bounded implementation package.
These are contract-preserving preparation decisions, not permission to start code.
The reviewed baseline remains unchanged at Forge commit
`411cb5a9fabc71e482a414ed58387de0ff557e93`.

## PD-01 — Baseline capture reconciled

DECIDED: All nine baseline artifacts match the manifest in both the working tree
and that commit. The baseline manifest's pending-capture field is a historical
observation; do not rewrite its fingerprinted source set. Record current capture
evidence separately in baseline_verification.json.

## PD-02 — Service repository and publication

DECIDED: Use `/home/gvasend/app/kge-forge-demo` as the separate, local demonstration
repository. It is a sibling, not a directory inside Forge, so ownership and work
scope remain distinct. No remote is configured. Naming is an implementation setup
choice explicitly deferred by the architecture, not a new human-purpose decision.

Publish the service vision, service requirements/acceptance obligations, and
service architecture module there. Each cites the exact Forge baseline source
and records its extraction provenance. The Forge publication bundle is a frozen
process record; active service documents are owned by the new repository. An
activation receipt references the published commit and content identities before
dependent service work. Publication creates documents only, not source code.

## PD-03 — First increment

DECIDED: E1-WP-001 implements an offline context and dispatch-preflight validator
in Forge. It checks authoritative inputs and emits explicit reasons why dispatch
is ready or blocked; it does not launch agents or execute service tasks. This
provides a small testable foundation for architecture §§3–5, before the actual
orchestration loop or service runtime is trusted. It is not a claim that the
validator by itself implements orchestration or establishes adapter safety.

## PD-04 — First-increment tooling

DECIDED: Use the available Python 3 interpreter and standard library for this
offline utility, with compatibility to the inspected Python 3.8.10 environment.
Use standard-library tests and no downloaded packages. This choice minimizes
setup/external access for the bounded utility and does not select the task-service
language, storage engine, or Codex integration product. No implementation is
written by the Architect.

## PD-05 — Adapter evidence cannot be inferred

DECIDED: CLI help and generated local protocol schemas establish interface
availability only. They do not prove scope enforcement, disabled unrelated
connectors, attributable lifecycle tracking, or safe recovery of an agent turn.
E1-WP-001 stays PREPARED_NOT_DISPATCHABLE until its bootstrap invocation facility
has reviewed evidence for those properties. Do not claim a validator that does
not exist can qualify the invocation needed to implement itself.

The qualification must be a separate, confined, non-implementation diagnostic:
scratch files only, one attributable session, test allowed/denied paths, no
unrelated connectors or task-tool network, inspect status and interrupt to a
confirmed terminal state. A later invocation needs an approved runtime boundary;
neither an elevated shell nor `danger-full-access` is an acceptable substitute.
No model turn, implementation invocation, or delegation is started during this
preparation. The human may designate an existing qualified facility or authorize
that separate qualification session. No change to the baseline's guarantees is
requested.

## PD-06 — Context publication and dispatch

DECIDED: Persist this package, its context, evidence and blocker state in a new
Forge commit after local publication. That commit supplements rather than alters
E1-ARCH-1. A capture receipt identifies it without self-referential commit hashes.
Before dispatch, compare that commit and the service publication with current
state, revalidate adapter evidence and single-active-invocation status, and issue
a separate dispatch record. Prepared does not mean issued.
