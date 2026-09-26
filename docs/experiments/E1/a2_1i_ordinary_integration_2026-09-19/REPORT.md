# C2 enrollment and ordinary-adoption integration

**BLOCKED_EXACT_R2_SELF_HOSTING**. This is not `R2_READY_FOR_ARCHITECT_ADOPTION`.

Enrollment/adoption composition works in the isolated integration candidate. The exact existing R2 implementation cannot consume the resulting runtime selection. Its own ordinary validator rejects the binding with `invocation runtime is not current adopted head`. An external helper selecting R2 is not R2 self-hosting.

## Scope and preservation

The accepted enrollment module was consumed unchanged at SHA-256 `7adf73eb300d7dd2fc1fae8fc36595de2c8b0b35cc534f8c795448414422c549`. New code is staged in this package only. Synthetic qualification, enrollment, integration and adoption decisions are explicitly marked `QUALIFICATION_BINDING` and held in isolated private stores. No real C2 enrollment or adoption decision was manufactured or applied.

The existing bootstrap, C1, R1, runtime-head authority, original production journals and historical invocation evidence remain unchanged. All 227 historical preservation checks pass. Fresh host observation verifies S3 exact, exclusive and READY. No r13, real invocation, real ownership acquisition, model request or E1 effect occurred.

Production R1 remains `sha256:1b31ac92d38952444076e3997083cf035e0862f1bc0182261826d6690ec31c15`.

Unchanged runtime-head authority is `RUNTIME-HEAD-AUTHORITY-sha256:75e6b7f2b5867c6d04bf0eeefc66f0c148d3f3e15e776c0d9e2b20b6352a1a5d`.

## Exact candidate and synthetic evidence

The existing content candidate remains `C2-CONTENT-CANDIDATE-sha256:0084c85d313ee3fc6e55f4ab012e7fd693337a384d1804e8967dafbb0253b2a2`, file SHA-256 `5b91c00d1e07e1520d3db1f9015ba618698964b5c8db5ed77e0b6789a7af8bdb`.

Its typed enrollment wrapper is `FUTURE-CONTINUATION-CANDIDATE-sha256:1ddd9833bbceca02d402bd4f594d992462299ea8f9dad42f29bea32087c238f0` and points to the same exact three-file implementation delta and R1 predecessor.

Exact existing R2 implementation: `sha256:a37de248a046263db9269e88d4714bfd1d9468719dbff3365d77bde2c501bc3c`.

The following are **synthetic qualification identities only**, not production authority:

- Qualification attestation: `CONTINUATION-QUALIFICATION-ATTESTATION-sha256:41dc059501af1d6319d1e8474d1df2d7737134cb10f89cdeef49719e3f874f23`.
- Enrollment: `CONTINUATION-ENROLLMENT-sha256:5b7187f7a5cf3edd354b51aafc1d2f2e6a77545fbb75f572db618ef1d47713ee`.
- Exact synthetic adoption decision: `ENROLLED-RUNTIME-ADOPTION-DECISION-sha256:d15667e065f09eb4756af3354509bc9f0c733c5e1abebd74649e8f896f659a09`.
- Isolated integration authority: `ORDINARY-ADOPTION-INTEGRATION-sha256:9b32369fdf13a4b7d21b28a1de730c7cc1a48efee819d158bfa257a7fac83d71`.
- Synthetic terminal head: `ENROLLED-RUNTIME-EVENT-sha256:e917ffb4197b83fc04c230338e8e5577b20cdf74722f36ad175869e0c94310d8`.

`SYNTHETIC_RECORDS.json` contains the complete exact bodies, references, isolated store pins and qualification scope. The attestation covers synthetic enrollment-contract qualification, not an independently completed production C2 runtime qualification. `FINGERPRINTS.json` provides individual canonical-body fingerprints.

## Integration mechanics and test results

The candidate external consumer reconstructs the unchanged authenticated R1 anchor, then an isolated append-only runtime extension. An independently selected synthetic material integration decision is distinct from the prospective enrollment delegation. Enrollment provides eligibility only. Adoption additionally requires an independently selected exact Architect adoption decision binding C2, R1, R2, qualification, enrollment, lineage and predecessor head.

One writer serializes extension transitions. An intent precedes commit, followed by a terminal record. Reconstruction validates every event, predecessor, grant and enrollment, rather than selecting the latest arbitrary row. Pre-commit interrupted intents abort without promoting the successor; post-commit recovery records the committed selection. Torn or reordered histories fail closed. The extension is qualification-only and is not selected by ordinary production.

Seventeen integration probes passed, including the expected negative self-hosting probe:

- Qualification, filesystem presence and enrollment leave R1 selected.
- Missing enrollment or adoption decision blocks.
- Candidate/R2 self-authorization and wrong actor, candidate, successor, predecessor or head block.
- Enrollment replay and adoption replay have no second effect.
- Concurrent duplicate and distinct competing candidates produce exactly one committed transition.
- Interruption before intent, after intent, after commit and after terminal append reconstructs the appropriate predecessor/successor with no automatic adoption retry.
- Independent reconstruction agrees on the exact synthetic current R2 and retains C1/R1 ancestry.
- Arbitrary filesystem roots, torn records and reordered history fail closed.

The accepted enrollment component's existing 22 probes remain applicable by exact implementation hash. Additional successful external selection is explicitly not counted as an R2 self-hosting PASS.

## Self-hosting blocker

The exact R2 inventory contains the frozen `runtime_adoption.py` at SHA-256 `e019dac4053a9e30c75304b94961096b8b9525272ed96c9564587da17154976c`. That consumer still requires adoption to be preselected in the original immutable policy and reconstructs only the original journal. It has no enrollment-consumption or authenticated-extension-selection path.

A fresh process loaded those exact R2 bytes and rejected the synthetic adopted binding. A further check supplies a combined isolated catalog containing both historical authority and all extension/enrollment/adoption evidence; the same exact consumer still rejects it. Thus this is not merely absent private evidence or a missing caller field. `EXACT_R2_SELF_HOSTING.json` and `EXACT_R2_COMBINED_CATALOG.json` capture the failures.

R2 cannot presently validate later ordinary continuation eligibility through the new extension either. No bootstrap authority was replayed; historical bootstrap reconstruction only reads its consumed evidence. Full production-path qualification stops before model-request readiness instead of substituting the external helper for the selected runtime.

## Production applicability and required implementation delta

| Area | Assessment |
|---|---|
| Enrollment consumption | Accepted component stays byte-identical; production requires independently authenticated selection of its delegation, policy and exact decisions. No real enrollment is authorized by these fixtures. |
| Ordinary adoption | The new composition extends eligible adoption evidence and current-head selection; this is MATERIAL integration. Its synthetic policy is not a production amendment or authority selection. |
| Runtime-head consumption | Must be present in the successor's own qualified inventory and called by the ordinary validator. Adding the staged integration to existing R2 changes its implementation identity and therefore requires a newly content-bound C2 candidate and qualification. |
| Context and invocation binding | Must authenticate the selected integration and adopted head throughout ordinary reconstruction and projection binding. Historical invocation contexts must retain their original consumers. This remains unqualified. |

The minimum remaining implementation is to integrate the governed enrollment/adoption consumer into the successor inventory, route ordinary runtime selection through authenticated extension ancestry, and qualify that exact updated successor and its context bindings. Historical bootstrap/C1 verification must remain read-only and exact. Copying new helper bytes under the existing R2 identity would correctly be `UNACCOUNTED_RUNTIME`; this package does not do that.

No new root/bootstrap is proposed. No missing authorization is inferred from qualification. The present existing C2 is not silently relabeled to point at different bytes.

## Timing

Seconds, first process sample followed by two warm samples. These are isolated component timings against actual immutable R1/C2 inputs; the machine's filesystem caches were not flushed. The samples ran while the negative suite was also active.

| Operation | First | Warm 1 | Warm 2 |
|---|---:|---:|---:|
| Enrollment validation | 0.048 | 0.051 | 0.050 |
| Enrollment append/fsync I/O | 0.028 | 0.037 | 0.049 |
| Complete enrollment transaction | 0.857 | 0.858 | 0.872 |
| Adoption validation | 0.121 | 0.113 | 0.111 |
| Runtime-head commit I/O | 0.037 | 0.052 | 0.032 |
| Complete adoption transaction | 4.628 | 4.663 | 4.637 |
| Independent reconstruction | 1.246 | 1.255 | 1.256 |
| External runtime-head/bytes verification | 2.006 | 2.013 | 2.009 |

All measured component phases are below 30 seconds. Existing thresholds are unchanged. These measurements do not establish complete post-adoption production performance. `MODEL_REQUEST_READY` was not reached, so cumulative pre-model timing is **unavailable/blocked**, not zero and not the sum of component timings.

## Result

Synthetic enrollment/adoption separation and serialized recovery have evidence. Production integration, exact R2 self-hosting, subsequent continuation consumption and full pre-model qualification remain unestablished. The required readiness conjunction therefore fails. Production remains R1 current, C2 unenrolled/unadopted, and R2 not current.
