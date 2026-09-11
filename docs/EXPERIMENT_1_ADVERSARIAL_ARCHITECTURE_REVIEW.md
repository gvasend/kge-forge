# Experiment 1 — Adversarial Architecture Review

Review: E1-AAR-1. Scope: proposed E1-ARCH-1, Forge control loop and demonstration
service, against the Vision, elicitation, requirements synthesis, and gap analysis.

Method: same Architect adopts a failure-seeking review perspective, traces
interleavings/crash boundaries and authority transitions, amends the architecture,
then rechecks the resulting contracts. No additional agent or independent external
reviewer participated. This is design review, not runtime verification or a formal
proof of all possible failures.

The pre-reconciliation candidate had SHA-256
`96beaf254224116343b6317aa73ba7f08fc32b4b14ed81ba954e3c3465cce714`.
The [reviewed candidate](EXPERIMENT_1_ARCHITECTURE_CANDIDATE.md) is retained as
archival review evidence with that exact content identity; it is not the governing
architecture. Its reconstruction from the recorded amendments was checked against
the original pre-review digest. The findings below preserve each earlier weakness,
correction, and verification obligation. The baseline manifest fingerprints both
the candidate evidence and the final reconciled document.

## 1. Material findings and reconciliation

Severity describes the consequence if uncorrected. CLOSED means reconciled in
the architecture and rechecked at the contract level, not proved by implementation.

| ID | Severity | Attack or failure trace and candidate weakness | Reconciliation in E1-ARCH-1 | Recheck and status |
|---|---|---|---|---|
| AR-01 | Critical | Retry is human-approved, the service acts, the response is lost, and the same approval is repeated. Candidate binds approval to state but does not define single consumption or command replay. | D-15 and §13: stable command identity, content/state checks, atomic approval consumption plus attempt reservation and grant. | Same command yields one grant; conflicting/revised command must be evaluated anew. Lost-approval-response scenario added to §14. CLOSED. |
| AR-02 | High | A task has partial effects, enters the retry queue, then is cancelled. Candidate's generic queued-cancellation wording could report that the task never executed. | §12 separates cancellation before any execution from cancellation of a queued retry and preserves prior attempt/effect history. | Cancelling retry removes future permission without changing earlier facts. §14 includes this case. CLOSED. |
| AR-03 | Critical | Input is modified during consumption and restored before a post-check. Candidate mentions integrity checks but does not establish the identity of consumed bytes. | D-16 and §9 require verified private material or verified consumed segments; live paths are not used as accepted inputs. | Result evidence identifies actual verified input; pre/post equality alone is explicitly insufficient. §14 includes change-and-restore. CLOSED. |
| AR-04 | High | Repository or tool text instructs an agent to expand scope; a prompt-only boundary could accept it as authority. | §4 distinguishes evidence text from governing decisions and requires action/capability validation at invocation/tool boundaries. Unsupported adapters block dependent dispatch. | Data cannot grant itself authority; unresolved adapter capability is an operational gate, not permission. CLOSED. |
| AR-05 | High | Files are fingerprinted but untracked, then unavailable after context loss or cleanup. Candidate has source provenance but does not explicitly gate dispatch on version-control capture. | §4 requires retrievable version-controlled governing context before dispatch; untracked digests are not falsely represented as committed history. | Readiness separately reports architectural readiness and pending operational capture. CLOSED. |
| AR-06 | High | Repeated crashes during continuation consume no budget and repeatedly reset work bounds. Candidate finite-attempt policy does not define grant accounting. | §10 counts initial, retry and recovered-continuation grants; retains uncertain reservations; requires progress and unchanged accepted bounds. | Duplicate commands allocate no new grant; continuation cannot reset limits. CLOSED. |
| AR-07 | High | Second-pass review: a recovery grant is accepted, then new evidence undermines its safety before the next effect. One-time validation is insufficient. | D-17 and §10 recheck authority/evidence applicability at each effect boundary, serialize invalidation against permission, and retain the truth about in-flight effects. | No later step proceeds under invalidated authority; an already-started effect is accounted for rather than pretended reversed. CLOSED. |

All seven identified material architecture gaps have explicit corrections.
None required changing human intent, widening trust, or requiring a human to choose
an implementation technology.

## 2. Challenges satisfied by the architecture

These are review challenges whose existing design was sufficient, not additional
claims that implementation evidence already exists.

| Challenge | Reason the reconciled architecture withstands it | Remaining verification |
|---|---|---|
| Crash before/after acceptance and lost reply. | §8–9: one durable acceptance boundary, stable reference, input-before-reference durability, existing-task lookup, uncertain ledger never treated as empty. | A-01–03, including repeated restart. |
| Torn final write is called excluded storage corruption. | §8 explicitly includes interrupted/torn writes in supported recovery; permanent media loss is the separate exclusion. | Crash/write-failure tests must establish old-or-new complete state. |
| Artifact exists but publication or task completion is missing. | §10–11: owned intent, material inspection and separate effect/task claims; bytes do not alone prove semantic completion. | A-04 and evidence of partial states. |
| Supervisor disappears while work continues and a new worker starts. | §6/11: admitted tasks cannot spawn detached processes; one process-lifetime ownership domain; unknown ownership blocks new execution. | A-09 plus sole-owner/executor-lifetime tests. |
| Abandoned task still has unknown outcome. | §7/12: administrative closure is separate; running abandonment waits for established cessation; no history deletion or implicit rollback. | A-07 with partial/uncertain effects. |
| Human says “success” despite conflicting records. | §13: retain both sources; distinguish administrative choice from factual claim; material uncertainty survives preference. | A-08 with conflicting timing, task identity, and content. |
| Same submission identity carries new inputs or retry policy. | §9: canonical specification conflict; no in-place replacement in E1; explicit new identity for new work. | A-03 including definition/policy changes. |
| Generic timeout triggers retry of an effectful task. | §12: safety proof and authority are separate; all unresolved attempts and effects are considered. | A-05 with missing/contradictory evidence. |
| Retry scheduling violates apparent FIFO. | §10: oldest eligible execution request, retry re-enters at tail, recorded lifecycle causes; no acceptance-FIFO promise. | A-11 including cancellation and blocked tasks. |
| Co-hosted service writes Forge files or uses the agents' AI connection. | §1/6: typed admitted operations, scoped object mediation, no arbitrary host paths/programs/network, separate role permissions. | A-12 including alias/traversal and forbidden destination attempts. |
| Half-published requirements across two repositories become active. | §4: active pair references exact retrievable source sets; activation follows validation; incomplete publication leaves prior activation authoritative. | A-13–14 and interrupted activation. |
| Human edits arrive while an implementation command runs. | §4/5: operation-boundary validation and post-operation impact review; results lose presumed validity and human edits are preserved. | A-14, including unrelated versus material edits. |
| Summary is stale, relevant sources do not fit context, or a needed dependency is missing. | §4: mandatory roots, explicit dependency closure, source validation, recorded staged retrieval or narrower work; no silent truncation. | A-13–14, including recorded insufficiency. |
| Lost dispatch acknowledgement causes two Implementation Agents. | §5: persist action intent, inspect invocation status, never blindly retry ambiguous dispatch, suspend if termination cannot be established. | A-15; adapter capabilities and intervention evidence. |
| No budgets are interpreted as endless work or permission to delete evidence. | §5/8/12: non-progress justification, finite task allowance, no automatic expiry, admission/suspension on unavailable capacity. | A-15 and storage-pressure scenarios. |
| Human manually coordinates the demonstration and the result is still called autonomous. | §1/5/14: orchestration is an evaluated capability, manual relay is recorded, service success does not imply process success. | A-16 and actual multi-increment process evidence. |

## 3. Combined failure traces checked

1. **Accepted task, lost acknowledgement, restarted service, repeated submission.**
   Recover ledger, resolve reference, show known/uncertain execution; no new task
   and no implicit retry grant.
2. **Partial effect, interrupted cancellation, repeated cancel, abandonment.**
   Repeated command returns one request. Reconstruct cessation and effects;
   preserve uncertainty, obtain explicit abandonment authority, close only after
   active execution is known ended. No rollback or invented failure.
3. **Human retry approval, concurrent evidence change, interrupted command.**
   Command expected-state check rejects stale authorization; if already committed,
   replay returns its one grant. New facts must be reconciled before dependent
   execution; prior permission does not authorize an altered risk basis.
4. **Changed input restored before result review.**
   Consumed input is verified private material. Unverified live-path consumption
   violates the architecture even if pre/post hashes match. Result cannot be
   accepted on those hashes alone.
5. **Forge restart while implementation invocation outcome is unknown.**
   Persisted work identity and context are reconstructed; adapter status is
   inspected. Until execution is accounted for, the system cannot issue another
   implementation package and call it sequential.
6. **Service conformance passes but human repeatedly restores context.**
   Technical completion evidence remains valid for its supported claims. The
   comparative autonomy assessment records process defects and belongs to the
   human; no automatic experimental-success conclusion follows.

## 4. Review coverage and limitations

- Authority, lifecycle, durable state, interruption, retry, cancellation,
  abandonment, security boundaries, context, change, provenance, evidence,
  observability, and completion were examined above.
- Performance/scaling: bounded admitted work and finite task allowance; no
  large-scale, fairness, priority, or distributed guarantees. Unknown numeric
  capacity is an implementation measurement, not an invented SLA.
- Interoperability/deployment: local single-operator boundary and logical agent
  adapters; no public/remote deployment or new external service required.
- Retention: no automatic identity/evidence expiry; later disposal remains a
  scoped human retention decision before any weakening of auditability.
- Context completeness, operating-system/storage primitives, and adapter control
  cannot be empirically established from documents. Their acceptance obligations
  and blocking behavior are explicit; they remain unverified implementation claims.

No open material architecture finding remains after reconciliation. There is no
claim of independent review, formal verification, implemented recovery, service
conformance, or successful autonomy. The next document must make the readiness
decision separately from those later claims.
