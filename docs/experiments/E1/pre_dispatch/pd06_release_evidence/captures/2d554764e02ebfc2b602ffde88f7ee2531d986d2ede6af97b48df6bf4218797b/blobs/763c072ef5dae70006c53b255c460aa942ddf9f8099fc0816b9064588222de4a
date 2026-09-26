# PD-05 — six proposed gap disposition records

Returned to the Architect, 2026-09-16. These are individual proposed classifications and evidence requirements, not adopted dispositions. No aggregate applicability conclusion is made here and no gap is closed by this document.

The Architect's supplied decision remains controlling: **PD-05 NOT YET ACCEPTED; PD-06 RELEASE NOT AUTHORIZED; A2 PARTIAL; E1-B01 BLOCKED; E1 profile INACTIVE; E1-WP-001 INELIGIBLE and UNDISPATCHED.** This records that decision without rewriting the historical captured STATE.json or issuing a release.

Basis: [PD05_AUTHORITY_APPLICABILITY_2026-09-16.md](PD05_AUTHORITY_APPLICABILITY_2026-09-16.md), especially its six numbered gaps. For this disposition task, the existing package's 37 fingerprinted files were checked against [sha256.json](pd05_applicability_evidence/sha256.json); all matched. Adapter source was inspected read-only. No probe, test suite, model call, supervisor operation, or new qualification was run. No implementation or authority configuration was changed.

Evidence shorthand below:

- **V** — [verification.json](pd05_applicability_evidence/verification.json): exact prepared profile, policy-resolution observations, source identities and inactive results.
- **I** — [inactive_audit.jsonl](pd05_applicability_evidence/inactive_audit.jsonl): prior non-effecting inactive requests.
- **B** — [bound.jsonl](pd05_applicability_evidence/bound.jsonl): historical ACTIVE `auth-bound`, revision 1, `scratch-bound-programmer`; one scratch repository, write only `calc.py`, exact `python3 test_calc.py` execution, seven successful actions (read/write/exec/finish).
- **R** — [recovery.jsonl](pd05_applicability_evidence/recovery.jsonl), [recovery_second.jsonl](pd05_applicability_evidence/recovery_second.jsonl), [ownership.jsonl](pd05_applicability_evidence/ownership.jsonl), [restart.jsonl](pd05_applicability_evidence/restart.jsonl): later ACTIVE scratch recovery and ownership evidence.
- **T** — existing adapter tests and the prior [16-test result](pd05_applicability_evidence/tests.txt). No tests were rerun for this document.
- **C/W** — captured [CONTEXT_MANIFEST.json](CONTEXT_MANIFEST.json) and [E1-WP-001.md](E1-WP-001.md), preparation capture `5871bdce4f5b6539c84f69f4f2b2f94ee31be5cd`; per-source revisions/hashes are in V.

“Can affect” below distinguishes the authority encoded for a prospective released invocation from present effects: the existing INACTIVE gate blocks all eight non-status actions. That common gate is not a reason to declare every latent read/write capability NOT_APPLICABLE. G5 is different because its executable grant is empty independently of activation state.

## G1 — Second repository hidden-path read authority

1. **Exact gap.** `programmer_authorization` constructs hidden read denies from `binding.repos['forge']` only. Service `.git/config` and corresponding hypothetical `.codex/.agents` paths resolve within its read grant; Forge equivalents deny. The qualified scratch profile excludes those directories in its sole repository.

2. **Exact authority/property.** E1-G01/G02/G03: `governed_read`, `governed_list`, `governed_search` over `/home/gvasend/app/kge-forge` and `/home/gvasend/app/kge-forge-demo`. Only `/home/gvasend/app/kge-forge/{.git,.codex,.agents}` are read-denied. Service `.git` exists; presence of service `.codex/.agents` was not asserted. Generic file access is involved, not Git execution. Captured-source write protection does not supply read confidentiality.

3. **Why scratch does not cover it.** B exercises a single scratch root whose hidden directories are excluded. Its outcomes cannot establish that permitting the second real repository's hidden paths is an acceptable E1 information scope. V already demonstrates the effective policy difference without reading hidden contents; another ordinary scratch read would not answer the policy question.

4. **Effect on outcome/boundary.** **Yes, potentially material.** A released read/list/search could expose additional names, metadata or contents and change the information available to reasoning and model transport. No actual secret is alleged and no present E1 disclosure occurred. Treating all repository roots as equivalently protected would be incorrect.

5. **Proposed class.** **`ARCHITECT_DECISION_REQUIRED`.** The relevant scope difference is evidenced. Whether the committed broad service read scope intentionally includes these paths, and whether that is acceptable for E1, is an architectural authority judgment. This proposal does not call the difference non-material or approve it.

6. **Existing support.** V `profile.read_roots`, `profile.read_deny_roots`, and `path_policy_resolution_without_read`; B's `authorization_issued` record; `adapter/authority_profile.py:20–29`; `adapter/governed_host.py:156–161`; C.scope and W's repository boundary. I establishes that unreleased reads remain denied.

7. **Smallest additional evidence.** No further behavioral evidence is needed to establish the asymmetry. The missing item is an Architect-authored disposition referencing the exact service hidden-path scope and governing permission: accept that scope on an explicit basis, or require a different boundary. If acceptance depends on what those paths contain, a narrowly authorized, non-secret-bearing content-category/access-suitability assessment is needed first; a current empty/benign snapshot alone cannot establish safety of future contents. A boundary change, if requested, would require separate authorization and assessment; this record neither implements nor prescribes one.

8. **Obtainable with E1 INACTIVE and without E1-WP-001?** **Yes.** Documentary judgment and any separately authorized read-only assessment can occur outside the Programmer invocation. No active E1 tool or implementation run is necessary. No such assessment was performed here.

## G2 — Write-scope shape and effects

1. **Exact gap.** E1 has four real targets, including recursive directory grants and missing-parent creation, whereas B demonstrates replacement of one existing file. Intended file targets use prefix semantics and could admit descendants if their filesystem type were a directory. Ancestor creation can affect paths outside a narrow leaf grant; existing broad-root tests do not establish the exact scope's applicability.

2. **Exact authority/property.** E1-G04, and E1-G05 for shared path-grant semantics: writes to `/home/gvasend/app/kge-forge/src/kge_forge/__init__.py`, `/home/gvasend/app/kge-forge/src/kge_forge/context`, `/home/gvasend/app/kge-forge/tests/context`, `/home/gvasend/app/kge-forge/docs/implementation/E1-WP-001.md`, subject to protected/captured-source denies. `_path` accepts equal paths and descendants. `governed_write` may create missing ancestors before replacement; `governed_patch` requires an existing parent and does not create it.

3. **Why scratch does not cover it.** B's existing `calc.py` requires neither directory-subtree enforcement nor missing-ancestor handling. T's other grant shapes do not demonstrate the four-target mapping, file-versus-directory distinction, and complete mutation footprint under a correspondingly narrow bound profile.

4. **Effect on outcome/boundary.** **Yes.** Unexpected directory/descendant authority or ancestor mutation can enlarge the actual write footprint. Missing-parent or wrong-type behavior can also change whether an otherwise intended edit succeeds or leaves partial directory effects. Real-product consequences cannot be dismissed merely because the replacement primitive is shared.

5. **Proposed class.** **`QUALIFICATION_REQUIRED`.** Material write behavior under the E1 scope shape remains unproved. Whether necessary ancestor creation is intended authority is also an Architect policy question; qualification must report actual effects rather than silently assume that permission.

6. **Existing support.** B's successful `calc.py` write; V's four write roots; C/W's allowed and protected paths; `adapter/governed_host.py:160–161,208–253`; T read/write denial tests. I proves non-effecting inactive write/patch, not allowed write behavior.

7. **Smallest additional evidence.** One separately authorized, committed synthetic scratch fixture reproducing the four grant shapes and protection rules, exercised through the supplied dispatcher under a scratch authorization. Capture an exact before/after inventory for: existing-file replacement; nested writes within each directory grant; denied sibling/protected paths; absent-parent creation including ancestor paths; and a directory occupying an intended file-grant path. Record request/result/provenance and all directory effects, including on failure. Expected permitted ancestor effects must be stated by the Architect or reported as unresolved. No model generation, payload execution, product code, or real-repository mutation is needed to establish these file-operation behaviors. This is an evidence specification, not authorization to run it.

8. **Obtainable with E1 INACTIVE and without E1-WP-001?** **Yes.** It needs a separate ACTIVE diagnostic scratch authority, if subsequently authorized; E1 and its repositories remain untouched. No new scratch fixture or qualification was created here.

## G3 — Information destination and content assumptions

1. **Exact gap.** The same default AI endpoint is available but is not bound in the effective WorkAuthorization; C permits only the existing approved service. Two broadly readable real repositories introduce different information consequences. An exact E1 transport configuration and content-scope assessment are absent.

2. **Exact authority/property.** Controller-owned model communication and transmission of context and tool results, especially E1-G01/G03 read/search and G02 names. `ResponsesReasoning` defaults to `https://api.openai.com/v1/responses`, model `gpt-5`, `store=false`; endpoint/model are controller constructor inputs. The controller reads `OPENAI_API_KEY`; transport can depend on inherited host/proxy configuration. The Programmer cannot select these settings. Task-tool `network=false` is a separate restriction, not an assertion that model transport has no external destination.

3. **Why scratch does not cover it.** The scratch continuation evidence establishes a transport mechanism and synthetic data flow. It does not establish that E1's exact controller-selected destination/environment is the approved configuration, or that the two real repositories' entire readable contents are approved for that destination. Source code defaults do not identify a deployed configuration. No changed endpoint, proxy, or credential exposure has been demonstrated.

4. **Effect on outcome/boundary.** **Yes.** A different endpoint/transport route or unsuitable readable content could change the external information boundary; the selected model can affect reasoning outcomes. `store=false` does not mean no transmission. The inactive client run guard prevents a present E1 model request.

5. **Proposed class.** **`ARCHITECT_DECISION_REQUIRED`.** Existing evidence identifies the qualified transport mechanism, its controller trust boundary and the content-scope difference. Applicability depends first on an explicit approved destination/data-scope judgment and a concrete configuration, not an automatic repetition of an API call. This proposal does not assert that an unspecified configuration is qualified.

6. **Existing support.** C.scope.model_communication/task_tool_network; V exact read scope and profile fields; `adapter/responses_orchestrator.py:55–64,93–121`; the committed `A2_1P_FORGE_OWNED_PROGRAMMER_SUBSTRATE_2026-09-15.md` and `A2_REMAINING_GATES_2026-09-15.md` accounts of the real scratch model loop. I/V document the pre-call inactive rejection. G1 identifies a concrete content-scope difference; this record retains a separate transport/content question.

7. **Smallest additional evidence.** A non-effecting, source-attributed E1 launch-configuration record identifying endpoint, model, transport/proxy policy, controller credential source by reference only, and the read-result/context categories permitted to leave for that destination; compare these fields with the recorded scratch configuration and identify unknowns. The Architect must then approve or reject the applicability of that mapping under C's approved-service restriction. No secret values or real repository contents need be sent to establish the mapping. If the mapping reveals a new execution/transport mechanism or unproved enforcement property, that specific difference requires separately authorized qualification; documentary approval alone cannot prove new behavior.

8. **Obtainable with E1 INACTIVE and without E1-WP-001?** **Yes.** Configuration capture and content-scope judgment can be read-only and offline. Any later necessary transport diagnostic could use synthetic content and separate scratch authority; no E1 model call is required or authorized here.

## G4 — Successful patch evidence

1. **Exact gap.** Available live evidence shows unsupported patch denial and recovery; B contains no patch action, and the identified T patch test proves rejection. Successful single-file `op=write` patch coverage under the final bound authority is missing. Similarity to atomic write is not successful patch qualification evidence.

2. **Exact authority/property.** E1-G05 `governed_patch`: one change object with `op=write`, a path within the four E1 write grants, content no larger than 1,000,000 UTF-8 bytes, existing parent, protected/captured-source exclusions, atomic replacement and governed-action digest provenance. This is replacement, not arbitrary diff application.

3. **Why scratch does not cover it.** Denial of unsupported `replace` or multiple changes does not exercise accepted patch dispatch, replacement, provenance or successful result audit. B's successful `governed_write` follows a different branch and has different parent handling.

4. **Effect on outcome/boundary.** **Yes.** An unproved allowed patch path can affect source contents, subsequent attributed execution inputs and evidence. Shared `_path` and replacement primitives are useful supporting evidence but do not establish the whole accepted action path.

5. **Proposed class.** **`QUALIFICATION_REQUIRED`.** An available material file-mutation action lacks positive qualification evidence. It is not NOT_APPLICABLE merely because E1 currently remains inactive.

6. **Existing support.** B's action inventory in V; `adapter/tests/test_governed_host.py::A2Tests.test_whole_patch`; the A2.1p qualification account's unsupported-patch denial; `adapter/governed_host.py:232–253`; `adapter/orchestrator.py:94`; registered patch schema in V. I establishes unreleased patch denial only.

7. **Smallest additional evidence.** One separately authorized synthetic bound scratch case sending a supported single-file `op=write` through the registered function dispatcher. Preserve the ACTIVE scratch profile, exact request, pre/post file bytes and full change inventory, pre-effect request audit, successful result, and matching governed-action provenance digest. Include a neighboring protected-target denial to bind the positive case to enforcement; existing rejection evidence can remain referenced. Establish provenance acceptance by a controller-only snapshot check if that claim is included, without launching a payload. No model/API call, full programming task, implementation work, or real E1 execution is necessary.

8. **Obtainable with E1 INACTIVE and without E1-WP-001?** **Yes.** A separately authorized scratch diagnostic suffices. None was performed for this disposition report.

## G5 — Empty execution grant / future-work fit

1. **Exact gap.** No E1 executable is authorized. The current restriction is covered, but a future test command, input set, PYTHONPATH treatment, scratch Git-fixture behavior or real-context acceptance run cannot be certified until specified. W's implementation instructions do not automatically grant execution.

2. **Exact authority/property.** E1-G06 `governed_exec`: both `exec_bins=()` and `exec_argv_allowlist=()`, shell=false, network=false. W's proposed Python entry point/PYTHONPATH and acceptance tests are work requirements, not effective grants. The empty executable set is decisive: an empty argv allowlist alone would not be sufficient evidence of no execution, because that allowlist check is conditional.

3. **Why scratch does not cover it.** B's concrete `python3 test_calc.py` cannot prove an unspecified future E1 command or inputs. But that future behavior is absent from the exact prepared authority, so there is no currently granted E1 execution to qualify beyond denial. R's recovery mechanism evidence does not create a command grant.

4. **Effect on outcome/boundary.** **No executable effect is possible through this exact prepared grant.** It also cannot perform the work package's required test executions; that is a readiness limitation, not authority leakage. Adding an executable/command/environment/input configuration later can change outcomes and boundaries and would require a new applicability assessment.

5. **Proposed class.** **`NOT_APPLICABLE`**, strictly for positive execution/future-command fit in the **exact empty prepared execution grant**. This does not classify the work package's eventual execution requirements as unnecessary, close G6's configuration attribution question, or establish release readiness. The Architect retains the disposition.

6. **Existing support.** V `profile.exec_bins`, `profile.exec_argv_allowlist`, and inactive exec result; I `pd05-exec`; `adapter/authority_profile.py:30–43`; `adapter/governed_host.py:262–270`, which denies every executable against the empty set before scope creation. This structural fact is independent of the additional INACTIVE denial.

7. **Smallest additional evidence.** **None for the narrow proposed NOT_APPLICABLE classification.** Existing profile bytes, denial evidence and executable-membership check suffice. If a future runnable profile is proposed, the minimum starting input is a separately authorized exact command/cwd/input/environment specification and its mapping to qualification evidence. Missing behaviors can then be identified; neither a future grant nor its qualification is inferred here.

8. **Obtainable with E1 INACTIVE and without E1-WP-001?** **Yes; the evidence for the current restriction already exists.** Any future specification and assessment can be prepared offline, with separately authorized synthetic qualification if needed. No E1 activation is required to assess a proposed command; none is performed here.

## G6 — Complete E1 input authorization attribution

1. **Exact gap.** Committed source provenance is verified, but exact authority for subsequent E1-specific ledger selection and a full production controller launch configuration is not established by the captured baseline and inspected records. Evidence-local probe identifiers do not supply production authorization.

2. **Exact authority/property.** Hard-coded ownership ledger `/tmp/kge-forge-e1-invocations.jsonl`; production authorization ID/revision/session/turn binding; controller audit destination; snapshot/scratch binding; endpoint/model/transport inputs; and any future command specification. Existing empty executable authority is already attributed as a restriction under G5. These are configuration/authorization provenance issues, distinct from whether the mechanisms function.

3. **Why scratch does not cover it.** R proves ownership/recovery behavior for its own ledger and scratch identities. B proves context-bound scratch operation. Neither authorizes E1's ledger destination or supplies E1's missing production launch record. A commit establishes what source was captured, not who approved each E1-specific input. Existing preparation source verification cannot fill unspecified inputs.

4. **Effect on outcome/boundary.** **Yes.** Ledger selection determines which controllers share single-active ownership; separate ledger choices can partition that protection. Audit placement affects evidence isolation and recovery; incorrect identity/context bindings affect attribution. An absence of approval is independently material even if a mechanism is unchanged. No current faulty E1 ledger operation or new configuration was demonstrated.

5. **Proposed class.** **`ARCHITECT_DECISION_REQUIRED`.** Existing source and scratch mechanism evidence supports review, but accepting the E1-specific mapping requires an explicit authority record. This is not a request for implementation, automatic approval, or PD-06 release.

6. **Existing support.** V's 24 committed-source checks and prepared profile; R's exact ownership ledgers and identities; `adapter/authority_profile.py:45`; `adapter/invocation_ownership.py` path-bound locking/reservation; `adapter/governed_host.py` audit placement and authorization checks. `A2_LIVE_RECOVERY_AND_READINESS_2026-09-15.md` and the source history identify recovery/profile changes at `b7c603308623c689e0330da1de2c092faceef95c`, terminal-audit ordering at `ba077bf6b61596f17c72d5de4ec053633afa2842`, and source hygiene at `5a3895d76212615b86a9e0764bf7dd702ed9451b`; these are not E1 release records.

7. **Smallest additional evidence.** A field-by-field, source-attributed proposed E1 launch/profile record: mark each value as baseline-derived, explicitly subsequently approved (with the actual authority reference), or unresolved. Include the common-ledger selection rule for all controllers intended to participate in E1, audit/scratch placement outside model grants, and the production identity allocation/binding rule; future session IDs may be allocated later under an approved rule rather than invented now. Retrieve any existing explicit approval or obtain an Architect decision on the unapproved selections. Keep INACTIVE and release/dispatch flags separate and unchanged. A novel recovery/ownership topology would require further qualification, but a new run cannot substitute for the missing authorization record.

8. **Obtainable with E1 INACTIVE and without E1-WP-001?** **Yes.** Source tracing, documentary configuration and an explicit Architect decision are sufficient to address attribution without effects. The record can remain proposed/inactive; approving an input mapping need not authorize activation, PD-06 release, eligibility or dispatch. No missing authority was supplied on the Architect's behalf here.
