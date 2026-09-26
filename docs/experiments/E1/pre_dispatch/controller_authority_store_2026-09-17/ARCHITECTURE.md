# Controller authority store

The controller selects a private catalog by its exact SHA-256 and applicability.
Catalog existence, a matching repository file, or an authority label alone does
not issue release, dispatch, continuation, transmission, or execution authority.
The existing ancestry/content verifiers still verify those decisions.

`adapter/controller_authority_store.py` provides immutable materialization,
logical resolution, provenance, private-state registration and controller-scoped
resolution sessions. It is not registered as a Programmer tool.
`adapter/authority_bootstrap.py` reconstructs authorization and operational context
from an explicitly pinned private catalog.

## Selection and historical evidence

Logical selection uses existing identities:

| Authority | Selection |
| --- | --- |
| Exact profile, clearance, capture, provisioning receipt, historical witnesses | Existing `sha256:<content fingerprint>` |
| Release basis / decision | Existing `E1-RELEASE-BASIS-sha256:…` / `E1-RELEASE-DECISION-sha256:…` aliases |
| Dispatch | Existing `E1-ARCHITECT-DISPATCH-sha256:…` |
| Current operational binding | Existing `OperationalContextId` |
| Effective authorization / runtime configuration | Existing authorization identity |
| Continuation envelopes and approvals | Their existing exact SHA-256 references; envelope identities and ancestry are independently verified |
| Committed source witnesses | Existing Git object IDs; the manifest uses the existing capture commit with a context-manifest role |
| Authorization lifecycle, controller audit and recovery history | Existing authorization identity with audit role |
| Ownership state | Existing authorization identity with ownership role, resolving to the existing shared ledger |

Release and dispatch records retain their exact bytes, including historical
repository paths. In a private controller session, those paths are inert
provenance: the controller resolves the pinned content identity. It never opens
the repository evidence path as fallback. Changing an immutable historical
reference in an envelope still fails the existing ancestry checks.

The production activation/recovery API takes the logical dispatch identity.
Production validation requires a normalized private logical reference. Supplying
a repository path or the former path/hash API reference is rejected. Store
resolution rejects paths, unknown IDs, missing objects, changed bytes, malformed
provenance, stale applicability and store placement overlapping Programmer roots.

Read-only engineering verification can still reproduce repository evidence
outside a private session. It cannot activate an invocation: production validation,
activation/recovery and active handoff require a pinned private store. There is
no fallback from a private session to the engineering reader.

## Provenance and temporal applicability

Each immutable catalog entry contains its exact private SHA-256, original
evidence path/hash references where applicable, an exact authority-source
reference, release/decision/context identities and a mutation class.
Applicability is the exact authorization identity plus ReleaseBasisId,
ReleaseDecisionId, OperationalContextId and continuation-chain digest. This is
an authority epoch, not a filesystem timestamp or a newly allocated release.
Reopening a catalog with a different epoch fails. Production validation also
compares its applicability and Programmer roots with the effective authorization.

The bootstrap catalog hash is a controller trust input. Repository copies of
catalog descriptors in this package are review/reproduction evidence and must
not be used as a mutable production selector. The prepared catalog and
continuation require adoption before operational selection. No adoption is
performed by materialization.

## Mutation rules

| Kind | Rule |
| --- | --- |
| Profiles, decisions, dispatch, contexts, continuations, captures, provisioning receipts, bootstrap configuration | Immutable exact-byte objects. Exclusive creation; no replace/update API. A changed selection requires a new qualified catalog/continuation. |
| Lifecycle/action/terminal audit | Append-only through the existing typed lifecycle and governed-host operations, with existing durable event validation. |
| Ownership | Existing typed reservation/release transitions under the shared ledger and live controller fence. No generic store mutation operation. |
| Recovery | Derived from the private audit/ownership records and independently observed kernel/supervisor state. It is not a caller-supplied PASS record. |

Existing audit/ownership locations remain in their already-qualified private
mechanisms. The store registers them by logical role, checks canonical paths,
ownership/mode/type, and verifies that they remain outside Programmer grants.
Their records are not rewritten or moved. Activation receipts bind the selected
catalog; recovery/handoff reject a different catalog from the activation receipt.

## Production read paths

| Path stage | Controller-authoritative input |
| --- | --- |
| Dispatch validation | Private dispatch, released profile, release basis/decision, operational ancestry, approval/source records and witnesses |
| Activation | The same private inputs plus private provisioning receipt; existing directory, transport and supervisor checks |
| Ownership | Registered existing private ledger and live controller lock |
| Model handoff | Private effective authorization, context/clearance/projection inputs and runtime configuration; unchanged exact transmission clearance |
| Governed action | Private authority and committed provenance witnesses; generated sealed acceptance projection; live worktree integrity observations |
| Recovery | Private bootstrap and ancestry; existing private durable audit/ownership; live supervisor/kernel facts |
| Terminal audit | Existing typed ActionResult, QUIESCENT, completion and reservation-release operations |

Current worktree files are still observed for task/source/implementation integrity.
They are not substituted for private authority. In particular, current Python
implementation hashes are checked against the qualified continuation; a stored
old implementation blob cannot hide changed running source. TLS roots,
executables, supervisor socket and cgroup facts retain their existing qualified
host checks. None is replaced with a caller-provided PASS assertion.

The committed execution-input witness closure is captured separately from the
mandatory governing-source closure. This lets snapshot provenance resolve
privately without treating new/unattributed workspace files as committed inputs.

## Programmer separation

Store roots are checked against released read/list/search and write/patch roots,
runtime cwd and input roots, and file/root transmission selections. An ancestor
overlap is rejected too. Store directories use 0700, immutable files 0600,
controller ownership, no symlink traversal and no hard-linked objects. Every
object read checks its exact hash. The catalog itself is pinned and checked.

Permissions alone are not claimed as a same-UID Programmer boundary. The boundary
is the released governed-tool grants plus the execution namespace and exact
transmission policy. Synthetic governed read/list/search/write/patch probes,
snapshot probes, forged-transmission probes and an actual Bubblewrap payload
probe qualify that separation. Only already-authorized acceptance/context
projections are derived for execution; the private store is never mounted into
the payload or added to a model-visible tool.

## Qualification limits and handoff

The full non-live controller path is tested using synthetic authorities, ledgers,
audits and supervisor observations. The Bubblewrap payload isolation test uses
the actual namespace barrier. Synthetic observations do not qualify a live
supervisor or imply that real E1 activation validation has passed.

Current released E1 authority is materialized unchanged. A separate prepared
catalog contains the qualified implementation descendant; the already-adopted
continuation remains its authenticated ancestor. Neither prepared catalog
existence nor a successful read-only reconstruction makes E1 eligible.

Host-authorized read-only observation confirms PID 57950 is absent. Host
reconciliation/restart planning is required before live validation, and a new
PID would also require authorized handling of the released supervisor binding.
No restart, E1 activation, ownership reservation, model request or dispatch was
performed by this work.
