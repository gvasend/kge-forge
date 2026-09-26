# PD-05 revised evidence and proposed E1 profile

**Applicability finding: GAP. Not every proposed runnable E1 authority is covered.** G1, G2 and G4 now have positive, bounded synthetic qualification evidence. G3 and G6 have concrete proposed records with remaining operational conditions. G5 identifies execution requirements the current mechanism does not yet implement or qualify. These are evidence verdicts, not the Architect's final PD-05 or PD-06 decision.

E1 remains **INACTIVE**; PD-05 **pending**; PD-06 **unauthorized**; A2 **PARTIAL**; E1-B01 **BLOCKED**; E1-WP-001 **INELIGIBLE and UNDISPATCHED**. No E1 product code, real hidden-directory contents, credentials or API traffic were involved in the scratch qualification. No supervisor implementation, process or execution environment was changed.

## Exact artifacts and source attribution

- [PROPOSED_E1_PROFILE.json](pd05_closure_evidence/PROPOSED_E1_PROFILE.json) is the authoritative **proposal**, `E1-WP-001-PROPOSED-R2`, not an executable release record. It includes the complete nine-tool registry, all scope fields, concrete controller policies, execution constraints, per-field provenance, unresolved selections and `all_proposed_runnable_authorities_covered=false`.
- [MODEL_COMMUNICATION.json](pd05_closure_evidence/MODEL_COMMUNICATION.json) contains the same communication object separately for review.
- [PD05_CLOSURE_AUTHORITY_2026-09-16.md](PD05_CLOSURE_AUTHORITY_2026-09-16.md) attributes this increment to the Architect's current G1–G6 instruction. Earlier baseline/preparation sources remain unchanged.
- [REPORT.json](pd05_closure_evidence/REPORT.json) preserves five synthetic committed fixtures, exact capture commits, 42 registered-dispatcher calls, full before/after synthetic worktree inventories, pre/post file bytes in hexadecimal, outcomes and provenance. Git internals are intentionally excluded from those inventories and were not targeted for mutation. Synthetic `.codex/.agents` marker bytes are fixture-owned test data, not real hidden content.
- The five adjacent `normal.jsonl`, `missing_directory_root.jsonl`, `directory_root_is_file.jsonl`, `leaf_is_directory.jsonl`, and `parent_is_file.jsonl` are independent controller audits. Fixture roots and commits remain identified under `/tmp/pd05-qualified-scratch-*`. These tests called the real file dispatcher/host without mocking file enforcement; no model or governed payload was invoked.
- [INACTIVE_VERIFICATION.json](pd05_closure_evidence/INACTIVE_VERIFICATION.json) and [inactive_r2_audit.jsonl](pd05_closure_evidence/inactive_r2_audit.jsonl) show revised supported profile fields, including the proposed nonempty command tuple, remain non-effecting under INACTIVE. Unsupported proposed execution constraints are explicitly identified, not falsely represented as implemented.
- [configuration_observations.json](pd05_closure_evidence/configuration_observations.json) records non-secret controller/runtime observations, missing directory preconditions and committed-source verification. [tests.txt](pd05_closure_evidence/tests.txt) records **43 adapter tests passing**. The new persistent scratch qualification separately passed **42 dispatcher actions**.
- `source.patch` and `sha256.json` in the evidence directory identify this uncommitted working-tree implementation and evidence. The adapter base is `5a3895d76212615b86a9e0764bf7dd702ed9451b`; no new release commit is claimed. Historical evidence bundles are preserved unchanged and their old source hashes remain historical identities.

The frozen E1 baseline remains `411cb5a9fabc71e482a414ed58387de0ff557e93`, preparation capture `5871bdce4f5b6539c84f69f4f2b2f94ee31be5cd`, and service publication `c9458a8698c90bd43137025fa7e1dc3c34c4e37a`. All 24 designated source blobs/current files and the 22-source mandatory closure were revalidated. Context digest remains `4407eb45c55375d6fdd39634ace78420d21f773f39f8cfdade380ca0949f6a21`.

## Individual closure verdicts

### G1 — Evidence complete for the directed exclusion

The constructor applies `.git`, `.codex`, and `.agents` read denies beneath **both** repository roots. Search now prunes denied directories before descending. A two-repository, committed synthetic profile exercised all three tools against all three hidden directories in each root: **18 explicit DENIED results**. Root listings omitted the directories; root searches returned no hidden marker; positive visible searches succeeded in each root. These six additional successful operations had no file effects. The roots differ from E1 only by scratch location and synthetic contents; the same constructor and registered dispatcher were used. Real hidden contents were not inspected.

Closure evidence: `REPORT.json`, normal case labels `forge.git-read` through `service.agents-search`, plus root-list/root-search/visible-search labels; `normal.jsonl`; changed `authority_profile.py` and `governed_host.py`. Remaining G3 ordinary-content suitability is separate and is not implied by hidden-directory exclusion.

### G2 — Evidence complete for the directed write semantics; setup precondition remains unmet

`WorkAuthorization.write_directory_roots` explicitly classifies recursive grants. Other `write_roots` are exact file targets. The constructor derives directory grants from the trailing slash in the committed manifest's directory entries, rather than guessing from current filesystem types. Directly constructed diagnostic test authorities now explicitly identify their directory grants too.

Before any directory creation, the host checks target type, the existing ancestor, every proposed missing ancestor, directory-grant membership and protected paths. Missing ancestors can be created **strictly below an already-existing granted directory**. Creation of a grant root itself is denied; a file grant cannot bootstrap its parent chain. Existing directory targets cannot be replaced as files; file-grant descendants deny even if the file target has been replaced by a directory. Patch retains its existing-parent requirement. Atomic file replacement uses a temporary staging file in the already-authorized target parent; it does not grant arbitrary directory creation.

The qualification demonstrates: exact existing-file replacement; nested writes and their directory additions under both directory grants; unchanged state for sibling/protected/service writes; denied absent leaf parents; denied missing grant roots; denied file-typed grant roots and parents; denied directory targets and descendants of file grants. Every action has complete before/after synthetic worktree inventories. There are three successful write actions; all negative cases have zero final worktree changes. No concurrent hostile host filesystem mutation or injected I/O failure was simulated; existing trusted/stable host filesystem assumptions remain.

**Readiness consequence:** actual `src/kge_forge`, `src/kge_forge/context`, `tests/context` and `docs/implementation` do not exist. The new policy correctly does not create them using E1 leaf authority. Their controller-owned setup/authorization is unresolved and was not performed. This is not a failed denial qualification and must not be hidden by relaxing ancestor semantics.

### G3 — Configuration prepared; operational applicability still conditional

The proposal binds the controller to `https://api.openai.com/v1/responses`, controller-selected **gpt-5**, `store=false`, `parallel_tool_calls=false`, the existing stateless continuation, and **OPENAI_API_KEY by reference only**. It retains the existing `urllib.request` HTTPS implementation and default certificate verification. No new transport implementation, proxy, API call or secret transmission was introduced.

The explicit proposed transport policy is **direct-only**: case-insensitive HTTP/HTTPS/ALL/NO proxy environment variables must be absent at authorized controller launch, with no custom urllib opener. Current non-secret observations show no such names and an unset opener in the inspection process; they do not attest a future process. This is a configuration restriction on the existing mechanism, not evidence of a new transport's qualification. Historical scratch evidence did not freeze proxy configuration, so identical historical routing is not asserted.

Authorized information categories are exact in `MODEL_COMMUNICATION.json`: committed governing context/task metadata; ordinary in-scope repository file/list/search outputs after exclusions; governed implementation/test/evidence content; bounded results/status/output/provenance/requests; and required prior model continuation items. Excluded categories include credentials, secrets, hidden directories, unrelated host files and private controller audit/ownership contents. That exclusion is a policy obligation, not a new content scanner: broad ordinary-file reads can contain secrets, and suitability assurance remains unresolved.

**Remaining enforcement limit:** the client accepts a controller-selected endpoint and uses default urllib redirect handling; no installed production launch gate binds this whole record or proves confinement of redirects to the approved destination. No alternate destination is authorized. No transport fix or new mechanism was introduced to conceal the limit. A reviewed operational binding/content assessment (and, if required, separate destination-enforcement qualification) remains necessary before claiming full G3 applicability.

### G4 — Evidence complete for supported single-file patch

The normal committed fixture sends `positive-patch` through `ResponsesReasoning._dispatch`, `ReasoningOrchestrator`, and `GovernedHost.governed_patch`, using `op=write` on `src/kge_forge/context/a/b/module.py`. It succeeds with exactly that file changed, with preserved before/after bytes and SHA-256. The source-effect record binds the same path/digest to action `positive-patch`; controller request audit precedes the operation/result. `protected-patch` denies the protected neighbor with no changes; `missing-parent-patch` denies without creating directories. No model call was required and no E1 patch occurred.

This proves successful mutation, its audit and provenance record. It does not claim that a new execution/snapshot was launched from this patch; that is outside G4's requested proof.

### G5 — Exact minimum test proposal prepared; runnable applicability GAP

The proposed sole top-level executable tuple is:

```text
/usr/bin/python3 -B -m unittest discover -s tests/context -p test_*.py -v
```

There is no shell expansion: `test_*.py` is one literal argument. Source cwd is exactly `/home/gvasend/app/kge-forge`; payload cwd is `/scope`. Inputs are exactly the selections `src/kge_forge/__init__.py`, `src/kge_forge/context`, `tests/context`, with per-file committed/governed-action attribution and normal size/link/deny rules. Proposed payload environment is exactly `PATH=/usr/bin:/bin`, `LANG=C.UTF-8`, `PYTHONPATH=/scope/src`, plus runtime-generated PWD; no inherited controller credentials/proxies/environment. Network and shell remain denied. Tests would use private `/scope` scratch and must exercise the specified module entry point and acceptance obligations.

This choice is derived from W's Python standard-library tests, `src` layout and `PYTHONPATH=src` requirement. The exact unittest discovery spelling is a concrete proposed controller selection, not claimed literal text from the baseline. It does not implement or run tests for E1. No separate CLI argument syntax was invented for the not-yet-implemented validator. A later standalone command needs an explicit revision.

The proposal records `/usr/bin/python3` resolving to `/usr/bin/python3.8` and current hashes of Python, Git and Bubblewrap. Git is runtime support for committed fixture inspection, not a top-level model Git tool; Bubblewrap is supervisor-only. An interpreter can spawn subprocesses inside the same containment boundary—the top-level argv allowlist is not a child-program filter. No real-repository commit, hidden-file exception or authoritative Git mount is granted.

Remaining differences:

1. The current launcher supplies only PATH/LANG. **PYTHONPATH requires a launcher/environment change and qualification**. Neither was performed.
2. Current WorkAuthorization does not encode/enforce the proposal's exact source cwd and fixed input set; it accepts a read-root cwd and model-selected bounded inputs. **This proposed narrowing is not yet an implemented enforcement property.**
3. Synthetic committed Git fixture provisioning/identity/provenance and payload Git inspection evidence are not supplied by the calc.py scratch task. A controller-provided captured test corpus requires a concrete input contract; this is not permission for E1 to mutate real Git repositories.
4. **WP1-AC08 cannot presently be claimed runnable.** The real preparation uses two repositories, absolute root identities and committed blob retrieval; the current snapshot exposes one root and excludes `.git`. The proposal makes no hidden-access exception. The exact real-context presentation and committed-object retrieval route remain unresolved; the three code/test selections alone are not sufficient evidence for AC08.
5. Binary hashes are observations, not current digest-enforced executable grants. Release must bind/revalidate the runtime identity. No proposed command was executed.

Thus this is the minimum specified test-command proposal, **not a complete runnable authority for every acceptance criterion**. The original empty command grant remains the effective unreleased baseline restriction. Even when the proposed tuple was constructed for the inactive denial probe, no execution was released.

### G6 — Proposed production record complete as a review artifact; selections/operational gates remain

The profile fixes the common ledger to `/tmp/kge-forge-e1-invocations.jsonl`, retaining the existing E1 constructor choice. **Every E1 controller, session, turn and revision must share that same canonical ledger**; no per-session ledger, empty ledger, truncation, deletion or reset is authorized. The existing locked reservation/durable terminal-result/closed owner/zero-member release rule remains. This preserves the design of the qualified single-active invariant; fresh production path identity and ownership readiness are not inferred from a document.

Controller identities use fresh UUID-based authorization/session/turn IDs with an immutable revision 2/profile digest/context binding; restart reuses exact IDs and audit, never a replacement identity to escape a reservation. No production IDs have been allocated. Audit path rule: `/tmp/kge-forge-e1-evidence/<authorization_id>/<session_id>/<turn_id>/controller.jsonl`, private controller directories mode 0700, file mode 0600, outside agent grants. Snapshot placement remains the qualified `/tmp/a2-exec-*` private workspace with controller-only manifest under the audit parent and payload `/scope` bind. No production audit directory or ledger reset was created.

The record includes G3, G5, environment/external policies, and provenance classifications. “Newly Architect-selected” records the current G1–G6 policy/delegated preparation authority; concrete naming/default choices are explicitly **proposed**, not a fabricated final acceptance. Baseline fields point to C/W; retained mechanism fields point to A2 qualifications; unknowns are marked unresolved. Each attribution applies to the named value and its nested fields unless an explicit nested qualification/unknown overrides it.

**Schema consequence:** adding `write_directory_roots` changes the serialized effective authorization. Existing recovery code compares complete authorization records, so old-schema audits cannot silently reconstruct under the new profile. New-schema recovery tests pass; historical active R qualification is not a live migration test. No old scope or ledger was migrated. Any old active/unaccounted invocation must be reconciled under its original qualified record before a separately authorized revised launch.

Unresolved selections/conditions remain: absent directory provisioning; synthetic Git corpus and real two-repository AC08 input/access mapping; exact production release commit/runtime binding and launch IDs; operational transport/profile binding and ordinary-content suitability. These are listed in the proposal rather than supplied through inferred authority.

## Revised PD-05 authority-coverage matrix

“Covered” below is a mechanism/evidence claim, never release eligibility. New evidence **N** is `REPORT.json` plus its five audits; **I2** is revised inactive evidence; **B/R/T** refer to the original preserved bound/recovery/test evidence and current regression log. All nine model functions were derived from the actual unchanged registry; controller-only capabilities are also included.

| Authority / exact proposed scope | Governing source | Enforcement and active qualification correspondence | Differences / disposition |
|---|---|---|---|
| Read: F and S except both roots' `.git/.codex/.agents`; 1–65,536 bytes | C/W + G1 | Same typed read/path mechanism; N normal `auth-pd05-normal`, two synthetic roots, all hidden read denials; B positive reads; I2 inactive denial | **COVERED for path enforcement**; real ordinary-content suitability/transport remains G3. No hidden narrower grant exists. |
| List: same roots/denies; 1–1,000 entries | C/W + G1 | N registered dispatcher: hidden list denies and root omissions on both roots | **COVERED**; explicit two-root denial replaces former direct-host-only evidence limitation. |
| Search: same roots/denies; literal query, 1–100 matches, ≤2,000 eligible files, ≤1MB/file, bounded line output | C/W + G1 | N hidden search denies, root hidden-marker absence, positive visible matches; denied directories pruned | **COVERED for path enforcement**; real content transmission remains G3. |
| Write exact files: F/src/kge_forge/__init__.py and F/docs/implementation/E1-WP-001.md; directory descendants: F/src/kge_forge/context and F/tests/context; protected/context denies; ≤1MB content | C/W + G2 | New explicit directory-grant field and parent preflight; N existing leaf/nested grants, sibling/protected/type/parent denials and complete effects | **COVERED for directed semantics**; actual missing directory setup unresolved. Synthetic vs real consequences do not grant setup authority. |
| Patch: one `op=write` in same scope, existing parent, ≤1MB | C/W + G4 | N successful positive-patch with audited digest/provenance and exactly one changed file; protected-neighbor and missing-parent denies | **COVERED** for accepted single-file patch and denial boundaries. |
| Exec: exact `/usr/bin/python3` unittest tuple, F cwd, three listed code/test inputs, proposed PATH/LANG/PYTHONPATH, /scope cwd, network/shell false | W + G5 | B/R qualify snapshot/admission/quiescence/interpreter mechanism; I2 denies even supplied proposed tuple while inactive | **GAP**: PYTHONPATH not supported, exact cwd/input restriction not implemented, committed test corpus and AC08 mapping unresolved; no exact command run. |
| Status: this host's IDs/state/counts; no arbitrary audit read | A1, C/D | Same implementation; current T regression and I2 successful status | **COVERED**, but status is not global release proof and architectural AUTHORIZED is not ACTIVE permission. |
| Authority expansion: request/PENDING only, no self-grant | A1 + C/W | Unchanged registry/host expansion; current T and prior Q; I2 denies unreleased request | **COVERED**; no approval or escalated-exec capability added. |
| Finish: request/latch only, requires no unresolved execution/effects | A1/W/D | B successful finish; current T continuation; I2 denies inactive finish | **COVERED**; not Architect acceptance or dispatch authority. |
| Additional capabilities: no shell/raw exec, Git function, MCP/plugin/connector, spawn, installs, link/delete/rename/mode or environment-setting function | C/W + A1 | Exact unchanged nine-function registry and rejection tests | **COVERED for registry exclusion**. Contained interpreter subprocesses are not filtered by the registry; proposed Git test needs are separately identified above. |
| Controller context Git: fixed read-only cat-file/full commits/fixed environment over C sources | C protocol + A2 context qualification | Same `CommittedContext`; 24 sources/22 closure revalidated; B mechanism | **COVERED for controller source verification**; does not supply payload access to committed real repositories. |
| Model communication/external destination: exact Responses endpoint, gpt-5/store=false, credential reference, direct-only policy | C + G3 | Same qualified urllib/Responses mechanism; no network call/change here | **GAP/CONDITIONAL** operational endpoint/proxy/redirect binding and ordinary-content suitability; exact current proxy-name observation is not a future launch attestation. |
| Environment: isolated payload proposed PATH/LANG/PYTHONPATH; no inherited credentials/proxies; controller credential only | W + G3/G5/G6 | Qualified launcher currently only PATH/LANG; environment test passes unchanged | **GAP** for proposed PYTHONPATH environment revision. No new environment was installed. |
| Filesystem/runtime: private writable snapshot, read-only /usr,/bin,/lib,/lib64, namespace /proc,/dev, no source promotion | Qualified A2 snapshot/supervisor + G6 | Same execution workspace/runtime mounts; prior B/R and current production mocks | **COVERED existing mechanism**, not the unresolved real-context/committed-fixture input delivery. Runtime hashes recorded, no live supervisor requalification. |
| Recovery and ownership: common E1 ledger, immutable IDs, terminal audit before release, owner-bound zero-member reconciliation | A2 recovery + G6 | R active scratch mechanism; current 43 tests include ownership/recovery; no ledger reset or alternate selected | **COVERED mechanism with conditions**: new schema requires fresh compatible authorization; old audit migration not qualified; fresh global readiness still required. |
| Audit/evidence: private per-identity audit outside both roots, fsynced request/result, snapshot manifests, controlled copies for Architect | A1/A2 + G6 | N/I2 prove current file-action audit and separation; B/R cover execution/recovery audit | **COVERED mechanism**; exact production launch path/profile binding not deployed. Published synthetic evidence is intentionally readable review material, not live audit authority. |

F = `/home/gvasend/app/kge-forge`; S = `/home/gvasend/app/kge-forge-demo`. All grant paths, protected context source paths and tool schemas are enumerated in the JSON proposal, not inferred from this abbreviated table.

## Remaining material differences and stopping state

There is no new model tool type, MCP/plugin, host administration grant, secret-read grant, alternate external destination or shell authority. Material proposed differences still needing evidence/implementation or selection are exactly recorded above: fixed execution environment/cwd/inputs, committed fixture and real-context access, pre-existing directory setup, transport/content binding and new-schema release/recovery compatibility. Qualification of file operations does not prove these other properties.

**Answer to runnable authority coverage: NO.** The complete runnable authority needed for E1-WP-001 cannot yet be represented and shown covered by the currently qualified mechanism. The proposal intentionally denies release rather than treating a test command alone as sufficient for all acceptance obligations.

Fresh I2 checks constructed the supported revised fields with state INACTIVE and the proposed exact command tuple. All eight non-status functions returned `authorization not released`; zero host file invocations, permits or scopes were created; the reasoning loop refused before any API call. Watched product targets, governing sources and E1 ledger were unchanged. The unsupported environment/cwd/input constraints were not silently materialized or exercised. No E1 implementation invocation was issued.

The changed adapter/test source and this evidence are returned to the Architect. No PD-05 acceptance, PD-06 release, E1 eligibility or dispatch is inferred. Stop with E1 **INACTIVE** and E1-WP-001 **INELIGIBLE / UNDISPATCHED**.
