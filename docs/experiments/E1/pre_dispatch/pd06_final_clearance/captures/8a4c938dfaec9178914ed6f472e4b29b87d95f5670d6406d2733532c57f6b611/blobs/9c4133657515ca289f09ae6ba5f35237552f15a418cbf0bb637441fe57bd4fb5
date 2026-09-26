# Final PD-05 runnable-profile qualification evidence

**G5 execution-authority qualification: PASS for the exact scoped mechanism and non-implementation fixture described below.** The final live run exercised the proposed Python command, executable-content identities, cwd/input restrictions, environment, network denial, committed acceptance projections, source provenance, audit, quiescence and sequential gating through the real governed supervisor path.

This is not an Architect PD-05/PD-06 decision and not an E1-WP-001 implementation or acceptance run. **PD-05 PENDING; PD-06 NOT AUTHORIZED; E1 INACTIVE; E1-WP-001 INELIGIBLE and UNDISPATCHED.** Provisioning authority, ordinary-content transmission suitability where required, and the final release/capture reference remain explicit Architect-selection items. No claim of release readiness is made.

The Architect's current instruction is the authority supplement for G5 implementation/qualification and G3/G6 operational preparation. Its accepted dispositions remain: **G1 CLOSED/PASS; G2 write semantics CLOSED; G4 CLOSED/PASS**. Their regression tests passed; none is reopened. G3/G6 remain conditional on production binding and release obligations. The original committed context and work package remain unchanged.

## Exact evidence package

- [PROPOSED_PRODUCTION_PROFILE.json](pd05_final_evidence/PROPOSED_PRODUCTION_PROFILE.json): exact proposed revision 3, complete effective scope/registry, runtime and transport, identities, ledger/audit/scratch, provisioning state, per-field authority attribution and remaining selections. [PROFILE_SHA256.txt](pd05_final_evidence/PROFILE_SHA256.txt) identifies its canonical JSON digest; no production invocation identity was allocated.
- [LIVE_REPORT.json](pd05_final_evidence/LIVE_REPORT.json): final **PASS**, fixture `/tmp/g5-nonimplementation-*` and its exact commit, negative request results, two successful executions, observed populated cgroup during the first result, sequential denial, governed synthetic source update and second-snapshot provenance. Exact fixture root/capture and all request results are in the record, not inferred from this report.
- [controller.jsonl](pd05_final_evidence/controller.jsonl), [ownership.jsonl](pd05_final_evidence/ownership.jsonl), and the two files in [snapshots](pd05_final_evidence/snapshots): fsynced controller requests/results, immutable authorization, exact snapshot/source/derived-input digests and ownership history.
- [HOST_RECEIPT.json](pd05_final_evidence/HOST_RECEIPT.json): existing supervisor **PID 57950**, socket `/tmp/a21m.sock` mode 0600, actual executable/cwd/cgroup identity, owner-bound supervisor create/close records, and fresh member-zero/populated-zero observations for both final scopes. The supervisor was not restarted or replaced. Its normal per-execution child imported the updated launcher.
- [ACCEPTANCE_INPUTS.json](pd05_final_evidence/ACCEPTANCE_INPUTS.json): every committed acceptance source, revision, digest and snapshot inclusion path, plus original-root projection mapping.
- [INACTIVE_VERIFICATION.json](pd05_final_evidence/INACTIVE_VERIFICATION.json) and [inactive_controller.jsonl](pd05_final_evidence/inactive_controller.jsonl): full revised E1 authorization remained INACTIVE; all eight non-status tool calls denied, model loop refused before any request, zero governed host invocations/scopes, and unchanged watched baseline/product targets/E1 ledger.
- [tests.txt](pd05_final_evidence/tests.txt): **47 adapter tests passed**. This covers existing G1/G2/G4 regressions, executable/environment mismatch, process-free object retrieval, transport denial, tampered derived inputs/runtime seal, and absent/unauthorized provisioning. The final live run separately covers the subsequently added fixture-only governed-source update between executions.
- `SOURCE_SHA256.json` and `SHA256.json` in the evidence directory bind current adapter/test source and the evidence package. Qualified source is an **uncommitted candidate**, based on `5a3895d76212615b86a9e0764bf7dd702ed9451b` plus the authorized G1–G6 changes; no release commit is claimed. Previous evidence packages and capture fingerprints remain historical records.

Final live evidence originated at `/tmp/pd05-g5-live-final-v4-20260916`; review copies above preserve it. The two final scopes were `scope-98bc40bd98114c3e9d29324879bfc0ab` and `scope-b4bcb8c7cddb459ebe400eb49a07b71f`. Both reached authoritative QUIESCENT before successful terminal ActionResult. No active reservation remained in the fixture ledger.

## Exact runnable envelope and enforcement

The only proposed top-level argv is the exact tuple:

```text
/usr/bin/python3 -B -m unittest discover -s tests/context -p test_*.py -v
```

No shell is involved and `test_*.py` is a literal argument. Python, Git and Bubblewrap path, resolved path and SHA-256 are recorded in `runtime.executables`; Python resolves to `/usr/bin/python3.8`. Only Python is a model-requestable top-level executable. Git is support for read-only projected committed data inside the already-governed payload; Bubblewrap is supervisor-only. There is no model Git function or generic controller Git execution service.

The production source cwd is **exactly** `/home/gvasend/app/kge-forge`; the fixture substitutes its synthetic Forge root. The payload cwd is exactly `/scope`. Model-requested inputs must equal this ordered list, with no additional, missing or reordered entry:

```text
src/kge_forge/__init__.py
src/kge_forge/context
tests/context
```

Directory selections expand only into files admitted by read policy and size/link limits; each file must match a designated committed blob or an exact successful governed write/patch digest. The action/snapshot record fixes the expanded file set. No entire-repository, arbitrary extra-path, hidden-directory or controller-evidence selection is accepted.

The controller checks argv, executable identities, cwd, inputs and fixed profile environment **before snapshot/scope reservation**. The fixed payload environment is:

```text
PATH=/usr/bin:/bin
LANG=C.UTF-8
PYTHONPATH=/scope/src
TMPDIR=/scope/.scratch
```

No host environment is inherited by the payload. Runtime-generated PWD is allowed only as `/scope`; the live fixture checked the entire observed environment. TMPDIR is an explicit refinement of the previously proposed scratch policy, needed to keep Python temporary fixtures in the private execution workspace. It adds no host temporary-directory mount. The `-B` flag suppresses bytecode writes. The profile does not pretend an interpreter cannot alter its own environment after start; containment, readonly mounts and network namespace remain the authority boundary for all descendants.

`adapter/runnable_profile.py` constructs the controller-owned policy and acceptance bundle. The host passes the **sealed policy digest** to the admitted launcher through a controller-only argument, not a model argument. `exec_barrier` verifies the seal, exact executable identities and every derived-input digest before starting the payload; readonly binds protect policy and acceptance projections. The host also verifies the launch receipt against its expected seal. Wrong seal/tampered derived-input tests deny before `execve`.

The launcher emits a bounded **start receipt**, not a success claim. This removes dependence on unittest printing stdout. The synthetic test emits **no stdout**, writes its detailed qualification result into `/scope/.scratch/qualification.json`, and remains alive for two seconds. The supervisor still requires launcher exit zero and authoritative scope emptiness before the host returns terminal success. The result carries the bound receipt, source/snapshot identity and observed workspace effects; it is not a general stdout/stderr transcript. Full transcript capture is not claimed by this profile. Excessive output or timeout remains an indeterminate/fail-closed outcome.

## Committed Git-derived inputs: no controller Git execution

`adapter/committed_objects.py` reads **loose Git objects directly in Python**, verifies zlib structure, size, SHA-1 object identity, commit/tree traversal and regular-file mode, and returns the requested blob. Final source bytes must also match the manifest's SHA-256. It never invokes Git or any subprocess and never consults repository config, hooks, attributes, filters, diff drivers, refs, alternates, replacement refs or remotes. `CommittedContext` now uses this reader rather than controller `git cat-file` subprocesses.

The independent bounded test supplies hostile hooks, fsmonitor/filter commands and a promisor/remote configuration, makes any attempted controller subprocess creation fail, and verifies exact retrieval plus failure on unavailable objects and traversal. No marker process runs. There is no fallback to a repository-controlled command. Packed, alternate, linked-worktree or missing loose-object storage is unsupported and **fails closed**; the exact baseline/preparation/service captures used here were successfully retrieved from their loose objects. A future repository packing change must not silently select another reader.

The controller builds minimal, deterministic repository projections containing only the declared source files, their necessary verified commit/tree/blob objects, a fixed detached HEAD and a controller-generated minimal config. No source repository config, hooks, refs, index, alternates or executable filter configuration is copied. These are **derived execution inputs**, not a relaxation of G1 model read/list/search exclusions on real `.git` directories.

The projections are bound read-only both under `/scope/.gei-context` and at the original Forge/service absolute paths **inside the payload namespace**. Original host repositories are not mounted. The live fixture used exact `git cat-file blob <full-commit>:<relative-path>` calls inside the already-admitted execution scope against these sterile readonly projections, with explicit Git environment. All 25 results matched their expected SHA-256 and working projection bytes. Attempts to modify projected source files or the input index failed. No generic Git tool was exposed to the Programmer.

## Exact real-context and acceptance/test input contract

Committed baseline: `411cb5a9fabc71e482a414ed58387de0ff557e93`; preparation: `5871bdce4f5b6539c84f69f4f2b2f94ee31be5cd`; service publication: `c9458a8698c90bd43137025fa7e1dc3c34c4e37a`. Context digest: `4407eb45c55375d6fdd39634ace78420d21f773f39f8cfdade380ca0949f6a21`.

The acceptance inputs are **all 24 declared sources plus the exact captured CONTEXT_MANIFEST.json**. The 22-source mandatory dependency closure is not substituted for the full declared source inventory: unresolved qualification-plan/prerequisite data remains visible as data, never authority to run E1. `ACCEPTANCE_INPUTS.json` provides the exact path/revision/hash for all 25. This avoids silently omitting non-mandatory declared sources when checking the real context.

| Work-package obligation | Required input and delivery contract | Qualified posture / scope of evidence |
|---|---|---|
| WP1-AC01 captured synthetic closure | Test source under `tests/context`, explicit manifest/root/capture metadata, and committed expected bytes from controller-built projection | Test source is commit/governed-action attributed. Private derived copies for test variations may be made only inside `/scope/.scratch`. The fixture proves delivery and committed lookup, not validator behavior. |
| AC02 missing/changed inputs, dependencies, IDs, authority | Isolated synthetic copies of manifest/source data with exact test-authored variations | Mutable scratch copies, immutable original acceptance bundle. Variation definitions belong to future governed test source; no E1 tests or validator were implemented here. |
| AC03 stale derivation | Original `derived_from`/source identities plus a synthetic changed-reference copy | Exact original metadata included and readonly; derived invalid input belongs in scratch. |
| AC04 current source/capture consistency | Captured source bytes/revisions and controller verification of current **designated source files**, with synthetic changed/uncommitted cases | Current designated files are checked before each action. Projection is not a full live Git status/diff view. No assertion about unrelated live worktree files is inferred from omitted paths. |
| AC05 traversal/command-like/symlink/alias inputs | Test-authored invalid metadata and isolated scratch objects, explicit root mappings | No additional real root authority. G5 rejects altered cwd/input selections; controller object reader denies traversal and never executes metadata. This is not an AC05 implementation PASS. |
| AC06 blocked dispatch facts | Original prerequisites/unresolved issues/work status and qualification evidence references | Original INACTIVE/prepared/blocker facts are included unchanged. The bundle does not manufacture READY. |
| AC07 reconstructible rerun | Persistent source/capture metadata and independently built, digest-bound snapshots | Two sequential live executions build distinct snapshots; original committed data is stable. Future utility restart semantics are not tested here. |
| AC08 real preparation context | Original manifest, all 24 sources, exact capture binding, readonly projected Forge/service roots at their original absolute paths | All identities, blobs, cwd relationship and mount posture verified by the synthetic payload. No actual E1 utility was run. Any broader full-live-worktree requirement is outside this minimal projection and must return unsupported/blocking rather than being inferred satisfied. |
| AC09 isolation and unchanged authoritative baseline | Writable private `/scope/.scratch`, readonly projections, no automatic source promotion | Live writes were confined to snapshot scratch; attempts to write acceptance projections denied. Actual baseline sources reverified afterward. |

Future implementation files/test files do not yet have content identities. The exact authority is for the three named selections with **per-action expanded file hashes and committed/governed-action provenance**, not a fabricated present hash for nonexistent E1 code. The synthetic fixture substitutes only those program/test bytes and its source root/work/session identities. Its first scope used committed inputs; a registered governed write updated a synthetic marker module between scopes; the second snapshot attributed that module to `fixture-source-update` and its exact digest. No source snapshot modification was automatically promoted.

## G3/G6 operational binding and remaining authority selections

The proposed production record explicitly binds:

| Field | Concrete proposed selection / authority basis |
|---|---|
| Model endpoint/model/storage | `https://api.openai.com/v1/responses`, controller-selected `gpt-5`, `store=false`; current G3 instruction and prior qualified service/model. Constructor rejects mismatched endpoint/model. |
| Credential | Controller environment reference `OPENAI_API_KEY` only; no value read for this qualification, no payload credential and no secret in artifacts. |
| Proxy/transport | New explicit `urllib` opener with `ProxyHandler({})`, pinned CA bundle path/hash, TLS client hostname/certificate verification, minimum TLSv1.2, 60-second timeout, and **all redirects denied**. Ambient proxy/CA/opener settings are not used. The exact controller Python/OpenSSL and selected platform TLS policy are recorded. |
| Transport evidence limit | Offline checks qualify configuration, wrong endpoint/model/store rejection, inherited-proxy exclusion and redirect denial. No API call was needed or made. Earlier live service evidence does not become a live test of this explicit opener; service/network availability remains a runtime fact, not authority to select another destination. |
| Information categories | Exact governing/context/task material, ordinary granted tool outputs after exclusions, in-scope source/test/evidence, bounded status/results/provenance and required model continuation. Credentials, unrelated host files, excluded real hidden paths and private audits are not authorized transmission categories. Ordinary-file content suitability is not established merely by path access; any required clearance remains an Architect-selection item. |
| Ownership ledger | `/tmp/kge-forge-e1-invocations.jsonl` for **all** E1 controllers/sessions/turns/revisions, without overrides/reset/truncation. Existing locked reservation and terminal-audit/owner/zero-member release mechanism retained. Qualification uses a separate scratch ledger; no E1 reservation is acquired. |
| Audit | `/tmp/kge-forge-e1-evidence/{authorization_id}/{session_id}/{turn_id}/controller.jsonl`, controller-owned 0700 parents/0600 file, outside both read roots, append/fsync, exact audit reused on restart. No production audit hierarchy created. |
| Snapshot/scratch | Controller-private `/tmp/a2-exec-*`, payload `/scope`, writable `.scratch`, readonly policy/acceptance projections; manifest under audit parent. No other host temp root grant. |
| Identities | Controller UUID-based authorization/session/turn/scope identities, revision 3, immutable serialized runtime/transport/context grants; model cannot supply a new scope or authorization. A changed record is a new revision, not an automatic runtime refresh. Production IDs are unallocated until separately authorized launch. |
| Runnable profile/environment | Exact tuple, source cwd, inputs, binaries, policy seal, PATH/LANG/PYTHONPATH/TMPDIR described above; no generic shell or inherited payload environment. |
| External policy | Only the approved controller Responses destination; task network, alternate endpoints, redirects, connectors/MCP/plugins and additional agents denied. |
| Provisioning | `src/kge_forge`, `src/kge_forge/context`, `tests/context`, `docs/implementation` must already be valid non-symlink directories under an exact recognized Architect provisioning receipt. No such authority/receipt exists here; all are absent. `launch_profile.provisioning` fails closed for absent paths **and** for a nonempty but unrecognized authority reference. No directories were created. |
| Release/capture | Exact source and canonical profile hashes are supplied for review. Final committed release/capture selection and PD-06 authorization are absent; neither is inferred from qualification. |

The explicit transport opener is a change from the earlier default-urlopen transport. It was independently checked offline rather than described as identical. Required operational choices are recorded; where authority is missing, the record says **ARCHITECT-SELECTION-PENDING**, not an inherited default or implied approval.

## Final PD-05 authority-coverage matrix

Statuses below are exactly **QUALIFIED**, **NOT APPLICABLE**, **ARCHITECT-SELECTION-PENDING**, or **GAP**. A QUALIFIED mechanism does not authorize release.

| Authority/property | Status | Governing/evidence basis and limits |
|---|---|---|
| Read on both exact repositories with `.git/.codex/.agents` exclusions | **QUALIFIED** | Architect G1 CLOSED/PASS; prior two-root dispatcher evidence and passing regression. Real hidden paths remain excluded from model tools. |
| List on both roots, bounded and exclusions applied | **QUALIFIED** | Accepted G1 evidence; registry/path implementation unchanged. |
| Search on both roots, bounded, denied directories pruned | **QUALIFIED** | Accepted G1 evidence and regressions. |
| Exact leaf writes, recursive directory grants, restricted ancestor creation | **QUALIFIED** | Architect G2 write semantics CLOSED; regressions pass. Does not grant initial directory provisioning. |
| Supported single-file patch and provenance | **QUALIFIED** | Architect G4 CLOSED/PASS; regression retained. |
| Exact top-level executable identities | **QUALIFIED** | Recorded absolute/resolved paths and SHA-256 checked by controller and admitted launcher; identity-mismatch test fails closed; exact live Python executed. |
| Exact argv | **QUALIFIED** | Only specified unittest tuple; bare Python/wrong argv rejected through registered dispatcher before scope creation. |
| Exact source cwd / payload cwd | **QUALIFIED** | Wrong source subdirectory denied; live payload verified `/scope`; production substitutes exact F root only. |
| Exact authorized code/test input selections and expanded-file provenance | **QUALIFIED** | Missing/additional/wrong selections denied; commit-attributed first scope and governed-update second scope; immutable per-file snapshot manifests. |
| PYTHONPATH and environment allowlist | **QUALIFIED** | Fixed `/scope/src`, PATH/LANG/TMPDIR only, no arbitrary model environment argument; full live environment equality and confined import verified; altered profile env denied. |
| Network prohibition | **QUALIFIED** | `--unshare-net` retained; live socket connect denied; no controller credential/proxy inherited. |
| Controller-built snapshot seal/provenance | **QUALIFIED** | Digests bound host→admitted launcher→receipt; derived tampering/wrong seal denied before payload start; readonly policy and projections. |
| Controller-owned committed Git acquisition | **QUALIFIED** | Process-free bounded SHA-verified object reader; hostile config/hooks/filter/promisor test plus subprocess trap; all designated actual blobs verified. Unsupported stores fail closed. |
| Readonly projected committed Git lookup inside scope | **QUALIFIED** | Actual 25 `cat-file` results verified within admitted payload against sterile controller-built objects/config; no generic model Git tool. |
| Real-context input identity/inclusion/read-write/cwd/environment relation | **QUALIFIED** | `ACCEPTANCE_INPUTS.json`, live 25-source equality, read-only write failures, original absolute root mapping and `/scope/src` import. Covers declared-source projection, not unrelated live Git status. |
| Result/audit attribution | **QUALIFIED** | Request/authorization/context/snapshot/action/scope identities and receipt seal match; payload evidence is hash-observed scratch data. Result is not a full stdout/stderr transcript. |
| Authoritative QUIESCENT before terminal success | **QUALIFIED** | Both final scopes: supervisor CLOSED then kernel members=[]/populated=0; controller quiescent audit precedes terminal success and ownership release. |
| Sequential execution gating | **QUALIFIED** | Result observed with populated cgroup; intervening exec denied; later fresh scope succeeds only after first terminal result/release. |
| Common ownership and recovery mechanism | **QUALIFIED** | Prior active recovery/cross-controller evidence, current tests, live common scratch ledger. All E1 controllers must use fixed production ledger. Fresh global readiness still mandatory. Old-schema recovery remains fail-closed, not migrated. |
| Status/evidence function | **QUALIFIED** | Existing qualified status plus final inactive status success. Does not assert release or global idle. |
| Authority expansion/escalation request only | **QUALIFIED** | Existing PENDING/no-self-grant mechanism and regression. No approval or alternate execution function added. |
| Finish request/latch | **QUALIFIED** | Prior qualified finish/continuation and regression. Does not confer Architect acceptance. |
| Generic Git/shell/MCP/plugin/connector/spawn/host-administration tools | **NOT APPLICABLE** | Not present in the complete nine-function registry or proposed grants. Contained interpreter descendants remain under the same boundary. |
| Explicit model endpoint/model/store/credential-reference/proxy/redirect/CA binding | **QUALIFIED** | Serialized immutable transport config, constructor/request checks and offline adversarial tests. No live API availability or authentication success claimed. |
| Real ordinary-content transmission suitability beyond the explicitly non-secret categories | **ARCHITECT-SELECTION-PENDING** | No secret clearance is inferred from broad read grants; no secret scan/disclosure performed. Resolve before an affected model transmission. |
| E1 initial directory provisioning | **ARCHITECT-SELECTION-PENDING** | Exact paths absent; no recognized provisioning approval/receipt. Checker denies missing or unauthorized setup. G2 semantics remain CLOSED. |
| Exact final release/capture and production launch authorization | **ARCHITECT-SELECTION-PENDING** | Candidate source/profile hashes exist; release commit/decision, production IDs and fresh global readiness are not issued. |
| Actual E1-WP-001 semantic acceptance/implementation results | **NOT APPLICABLE** | Explicitly not executed. Fixture proves authority/input delivery, not validator correctness or implementation completion. |

No additional model-visible capability was found: registry still consists of read, list, search, write, patch, exec, status, authority-expansion request and finish. Controller object reading, input projection, model transport, audit, identity/ownership and provisioning are separately inventoried above.

## Differences between active fixture and proposed E1 runtime

1. **Program/work identity and source content:** scratch task `G5-NON-IMPLEMENTATION`, scratch source repositories/commits and diagnostic ACTIVE state versus E1-WP-001, real source roots and INACTIVE state. Exact authority shapes and enforcement code match. Fixture code asserts authority properties; it is not the validator. Future product code is admitted only by per-file committed/governed-action identity.
2. **Ledger/audit destinations and identities:** scratch ledger and audit are outside scratch grants; production uses the fixed common E1 ledger and named audit rule. Same mechanism, different controller-selected resources; production is not launched.
3. **Acceptance data:** the fixture uses the **actual** captured E1 context and its exact declared-source projections, not fabricated E1 baseline values. Both proposed production and fixture use the same projection builder, object reader, readonly binds and absolute root mapping. These projections deliberately do not expose a full live repository or arbitrary hidden metadata.
4. **Environment:** proposed R2's PATH/LANG/PYTHONPATH has been concretely implemented and qualified, with explicit TMPDIR under `/scope/.scratch`. No inherited payload setting is relied on.
5. **Transport:** the active execution fixture makes no model request. Explicit production transport guards are tested offline; previous live Responses evidence establishes earlier service use, not a live run of the new opener.
6. **Provisioning:** scratch directories were created under the authorized synthetic fixture setup. Actual E1 paths remain absent/unapproved and are blocked as required; this difference is a pre-activation obligation, not authority to create them.
7. **Input representation support:** exact captures are loose-object stores; packed/alternate/worktree storage is unsupported, not silently serviced by Git. Source/runtime drift causes denial and requires renewed assessment.
8. **Result semantics:** start receipt plus terminal exit/quiescence proves execution outcome attribution. No semantic claim about future test assertions, full transcript collection, real validator READY/BLOCKED output or implementation acceptance follows.

**Coverage answer:** all twelve requested G5 enforcement properties have evidence through the implemented profile, including a live exact-command fixture. Remaining entries are explicit selection/release obligations, not silently granted runnable authority. No E1 work has run, and this package does not decide PD-05 or PD-06.

Final inactive check constructed the full revision-3 supported authorization with its nonempty exact command grant and bound model transport. Eight non-status requests were denied as unreleased; status alone succeeded; zero governed invocations/scopes existed; model execution refused before credential/API access. All 24 designated sources/22-source closure reverified and watched product targets/E1 ledger remained unchanged. Return to the Architect with **PD-05 PENDING, PD-06 NOT AUTHORIZED, E1 INACTIVE, E1-WP-001 INELIGIBLE and UNDISPATCHED**.
