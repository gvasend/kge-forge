# E1 Run-2 remediation — Architect review package

This package proposes controller remediation. It does not authorize, activate,
dispatch, or restart E1. Run 1 remains CANCELLED / INTERRUPTED_NO_EFFECTS.
E1-WP-001 and E1-ARCH-1 have not been edited. The exact Run-1 initial cleared
task/context is used to construct the proposed payload; its old tool definitions
recompute the historical ModelPayloadDigest before the new digest is calculated.

The final evidence is in `qualification_final_seal/`. Earlier qualification
directories retain development failures and intermediate measurements; they are
not substitutes for its source-inventory-bound closure. `PROPOSAL_SUMMARY.json`
and `PROPOSED_OPERATIONAL_BINDING.json` identify the exact review candidate.

**Implementation and scope.** `adapter.run_control` supplies a versioned,
hash-linked timing stream, budget admission, deadline interruption, and read-only
operator projection. Timing records bind the entire preceding audit prefix,
invocation/work identity, cycle, boot identity, monotonic time, wall time, ordering,
and policy fingerprint. No model reasoning or arbitrary response message is
retained. Usage is selected from numeric provider fields; reasoning/cached token
details are supplementary, not double-counted into totals.

`adapter.controlled_dispatch.dispatch` is an opt-in entry for an already selected
private store and already active invocation. It does not activate or issue
dispatch authority. It reads the budget policy from the private authorization,
starts durable invocation control before authorization reconstruction, and wraps
bootstrap, activation recovery, host construction and reasoning construction.
It refuses to restart a prior model attempt automatically. Store selection itself
is trusted controller initialization preceding invocation admission.

The reasoning loop records preparation, request intent, transport, response
receipt, validation, tool extraction, continuation, progress and disposition.
The transport event means a local transport attempt, not invented provider
acceptance. A provider request-header ID is recorded only when supplied. A local
timeout with no response explicitly retains REQUEST_OUTCOME_UNKNOWN and does
not claim provider cancellation. No API retry was added.

**Status.** `adapter.run_control.status(audit_path)` is read-only and intended for
the controller/operator boundary, not a new Programmer tool. It exposes identity,
cycle, subphase/outstanding operation, timestamps and ages, counts, governance
observations, budget transitions, reported usage, terminal state and uncertainty.
It validates timing order and preceding audit fingerprints. Event freshness and
governance-observation freshness are evaluated separately. After 60 seconds,
stale mutable facts become UNKNOWN. A recent activity event cannot freshen an old
supervisor observation. Fifteen-second activity receipts are not substantive
progress. Equivalent governed result identities are deduplicated; denied actions,
verification, heartbeats, and redacted reads do not reset progress.

The recorded examples are `OPERATOR_STATUS_EXAMPLE.json` (three synthetic model
cycles, one denial, one corrected read, zero implementation effects) and
`OPERATOR_LIFECYCLE_STATUS.json` (typed CANCELLED lifecycle, released ownership).
Synthetic supervisor readiness in the latter comes from mocked kernel observation;
it is not a statement about current live S2 readiness.

**Budgets.** These are E1/v0.1 policy values, not universal defaults:

| Budget | Soft | Hard |
|---|---:|---:|
| Model cycle | 120 s | 300 s |
| No substantive progress | 180 s | 300 s |
| Work-package invocation | 1200 s | 1800 s |
| Validation/preparation phase | 30 s | 120 s |
| Model request count | 8 | 12 |
| Reliable reported cumulative tokens | 100,000 | 150,000 |

Soft limits produce durable warnings with the operation and last progress.
Hard limits durably close admission and invoke governed interruption/recovery.
Blocking phases are interrupted by a controller-owned POSIX timer; an existing
signal owner or non-main-thread deadline runner is rejected rather than silently
losing enforcement. Existing execution limits and quiescence semantics remain.
The twelfth request may finish; a thirteenth is denied. State/counters and original
deadlines reconstruct from the audit. Boot ambiguity, backwards monotonic evidence,
an unresolved prior request, and durable closure fail closed. Restart is not retry
authorization. Fresh production validation consults durable budget closure.

Reported token thresholds stop further admission once reliably observed. No
provider-side reservation is implemented; status always says
`token_ceiling_enforced:false` and `token_budget_state:USAGE_UNKNOWN` because no
reservation bound is available, even when reported usage is retained accurately.
Missing/inconsistent usage accounting is also USAGE_UNKNOWN; the
proposed explicit fallback enforces time and request-count budgets only. This is
not a claim that the provider cannot exceed a token threshold during a request.

**Practical validation.** Only pure validation of externally pinned, immutable
catalog bytes is reused. The parsed catalog is recursively immutable. Each lookup
still reads/hashes the catalog, checks its directory identity and current placement,
and reads/hashes the selected object. Each grant is resolved once per fresh path
comparison rather than repeatedly within one predicate. Mutable ownership,
execution, supervisor, lifecycle, ancestry selection, repository inputs and
implementation bytes are not cached away. Substitution and changed-context probes
remain negative.

`TIMING_RESULTS.json` records cold bootstrap, cold activation and three warm
handoff validations with a 477-entry synthetic private store. All production
validation code runs, with synthetic release/context/dispatch and mocked kernel
supervisor observations. This is representative non-live qualification, not a
measurement of the full amended real E1 ancestry. `VALIDATION_PROFILE.txt` records
the remaining dominant functions. Separate actual Run-1-store lookup measurements
are read-only and must not be presented as full production validation timings.

**All nine tool contracts.** Names and capabilities are unchanged:

| Tool | Contract reviewed and retained | Evidence |
|---|---|---|
| governed_read | Designated root + relative path; integer limit 1..65536; separate result clearance | New correction/boundary tests; existing path/transmission negatives |
| governed_list | Permitted directory; integer entry limit 1..1000 | Schema range; existing list/search grant tests |
| governed_search | Permitted directory; nonempty literal query; limit 1..100; existing file/scan bounds described | Schema/runtime review; existing grant/hidden-source tests |
| governed_write | Whole replacement; 1,000,000 UTF-8 byte bound; exact grants and qualified parent creation | Existing write/patch authority regressions |
| governed_patch | Exactly one whole-file `write`; same byte bound; existing parent | Schema min/max/enum; existing patch authority regressions |
| governed_exec | Exact released executable, argv, cwd and bounded inputs; no shell or scope injection | Production execution, snapshot and no-bypass regressions |
| governed_status | No arguments; read-only; separate disclosure policy still applies | Registry/status and transmission regressions |
| authority_expansion_request | Non-effecting PENDING request, not self-authorization | Existing expansion/registry regressions |
| finish_task | Programmer assessment, not Experiment acceptance; terminal ownership/quiescence checks | Existing finish/lifecycle regressions |

Integer coercion at the orchestration boundary was removed so strings, floats and
booleans cannot masquerade as schema-declared integer limits. Runtime checks remain
authoritative; the schema does not grant access. UTF-8 byte constraints and
release-specific executable/argv constraints remain described and runtime enforced,
not inaccurately expressed as character limits or broad static executable enums.

**Denial correction and audit.** Only READ_LIMIT_OUT_OF_RANGE is newly proposed for
disclosure, together with the fixed 1..65536 range. The boundary independently
checks that the call contains an invalid integer limit. It never echoes a path,
error string, resource-existence predicate, hash, credentials or private evidence.
Other denials remain redacted. The synthetic Programmer receives that diagnostic,
corrects the limit, and reads an independently authorized and cleared file.

Private ActionRequest evidence includes operation, scalar limit, request digest,
authorization identity, released-profile fingerprint and operational-binding
fingerprint. A canonical resource path is retained only under the proposed
GRANTED_RESOURCE_AND_SCALARS_V1 policy and only after path authorization succeeds;
otherwise only a digest representation is kept. This permits explaining the tested
limit denial without retaining file content. Timing/status projections exclude
those private argument details.

**INCOMPLETE.** Under the proposed policy, INCOMPLETE and loop exhaustion require
terminal cancellation after reconciliation. They never mean success or permission
to continue automatically. `ActivationTransaction.cancel` requires the live
controller fence, matching invocation ownership, governed interruption, no pending
actions or uncertain results, and no unresolved execution ownership/scope. Safe
cancellation appends the lifecycle event and reservation release. Uncertainty
instead yields INDETERMINATE / HELD_FOR_RECONCILIATION. Remote provider uncertainty
is reported separately from controller-observed effect uncertainty. Fresh terminal
recovery and hard-stop execution reconciliation are qualified synthetically.

**Qualification coverage.** The sealed regression log identifies every test. It
covers correlated timing/order/tamper checks; multi-cycle live status and staleness;
provider versus validation phases; soft/hard thresholds; blocking deadline
interruption; execution reconciliation without retry; restart budget persistence;
meaningless-activity/equivalent-progress rejection; cold/warm validation; schema
and denial correction; protected-result filtering; reconstructable read arguments;
typed INCOMPLETE cancellation/ownership release; namespace isolation; execution,
QUIESCENT, authority, transmission, recovery and no-bypass regressions. No real
model request or E1 invocation is used. Provider API schema acceptance and remote
cancellation are not live-tested or claimed.

One pre-existing synthetic regression selected real historical preparation files
and failed on legitimately appended `preparation_decisions`. Its fixture now uses
synthetic acceptance data. Production stale-context validation was not relaxed.
The original test bytes and failed qualification are retained. Qualification
attempts lacking an unchanged-source closure are intermediate evidence only.

**Separate applicability decisions.**

| Component | Proposed classification | Required action before adoption |
|---|---|---|
| Content-free telemetry/status storage | Non-material implementation candidate, subject to retention review | Approve exact evidence fields and implementation binding |
| Budget/stopping semantics | Material release change | Approve time/count/token-fallback policy and interruption semantics |
| Catalog validation performance | Non-material implementation candidate | Review equivalence argument and freshness/substitution regressions |
| Tool schemas / ModelPayloadDigest | Material release change | Approve new exact payload; preserve old digest historically |
| Safe denial transmission | Material release change | Explicit clearance for the sole fixed diagnostic |
| Argument evidence retention | Material policy change | Approve private resource/scalar retention; no model disclosure inferred |
| INCOMPLETE lifecycle | Material release change | Approve cancellation or explicit held-uncertainty disposition |

No classification of the entire package as a non-material continuation is made.
The proposed profile preserves the original execution, filesystem, snapshot,
network/destination, supervision and quiescence constraints and adds the explicit
policies. Original task/context content remains exact; changed tool definitions
necessarily change ModelPayloadDigest. Proposed new invocation identifiers are
unissued and cannot reuse the cancelled Run-1 activation/reservation.

**Unresolved release gates.** Architect approval of this material scope and exact
candidate is required. The current material-release decision consumer is scoped
to supervisor succession; it cannot lawfully consume this broader policy amendment.
A qualified binding/decision-consumption step covering the approved Run-2 scope is
therefore required before private materialization/adoption. Full amended real
ancestry performance and fresh supervisor readiness must then be established.
New invocation dispatch/activation authorization is separate. The proposal contains
no Architect decision, dispatch approval, activation or ownership reservation.
It is not an operationally usable release and does not claim current Run-2
OperationalContextId or FullContextDigest before that binding exists.
