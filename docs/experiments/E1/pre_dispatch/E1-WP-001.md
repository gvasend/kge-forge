# E1-WP-001 — Offline governing-context and dispatch-preflight validator

Status: **PREPARED_NOT_DISPATCHABLE**. No implementation agent has received this
package. Adapter qualification remains a dispatch gate; see PRE_DISPATCH_REVIEW.md.

Baseline: E1-ARCH-1 at Forge commit
`411cb5a9fabc71e482a414ed58387de0ff557e93`.
Owner: Architect. Intended executor: one separately invoked Implementation Agent.
Governing context: CONTEXT_MANIFEST.json; decisions: DECISIONS.md.

## Objective and boundary

Implement an offline utility that checks a supplied governing-context manifest
against explicit local repository roots and reports context validity separately
from dispatch readiness. A missing, stale, contradictory, uncommitted, or
unqualified governing input must be visible; it must not become an implicit READY.

This is the first bounded component of Forge, not the whole engineering loop.
It must not invoke an AI model, launch tools on behalf of a model, implement the
task service, write authoritative state, create a repository, or select service
storage/execution mechanisms. No application source currently exists in Forge.

## Requirements and invariants

Direct: F-06, F-07, F-08; bounded contributions to F-02, F-03, F-09 and A-13–15.
Authority/trust constraints: F-01, F-04, F-05, F-10, F-11. Architecture §§3–5,
D-01–03 and AR-04/05 govern this increment. Other service requirements are context
for ownership, not permission to implement their runtime.

- Input metadata is data, never executable instructions or permission expansion.
- No source/summary gains authority solely by being newest or matching keywords.
- Hashes verify identified content; source material must also be retrievable.
- Context validity and permission to dispatch are distinct results.
- Missing or unknown required evidence blocks; no optimistic defaults.
- A referenced historical revision may remain valid despite later append-only
  process records; material current-state changes must be assessed explicitly.
- Receipt generation must not mutate either repository or call network services.
- The utility cannot attest that an adapter is safe merely because a flag says so.
  It validates references to Architect-reviewed qualification evidence for the
  specific scope, and reports that basis; enforcement remains the actual adapter's job.

## Allowed repository scope after dispatch

Forge root: `/home/gvasend/app/kge-forge`.

Writable product paths only:

- `src/kge_forge/__init__.py`
- `src/kge_forge/context/` (utility and its local protocol documentation)
- `tests/context/` (isolated fixtures and meaningful tests)
- `docs/implementation/E1-WP-001.md` (usage and implementation evidence references)

The implementation invocation must enforce that scope through its qualified
execution boundary. Governing docs, this package, `.git`, `.codex`, `.agents`,
`AGENTS.md`, other existing files, and the service repository are read-only.
Temporary fixtures may be created only in the invocation's explicitly designated
scratch directory and must not modify real governing artifacts. No installs,
remote services, commits, policy changes, approval bypass, or other agents.

Repository roots and authoritative paths are provided by the Architect context;
the implementation must not discover arbitrary private directories. Read host
runtime/library material only as required for ordinary Python execution.

## Implementation contract

Use the existing Python 3 standard library; no external dependency or packaging
tool is needed. Provide the entry point `python3 -m kge_forge.context` with
`PYTHONPATH=src`, accepting an explicit manifest file and repository-root mapping.
Accept an explicit package-capture commit binding where the manifest refers to
the commit containing this preparation. Never infer that binding from a mutable
branch name. CONTEXT_PROTOCOL.md defines the prepared manifest's interpretation.
Expose the validation as importable functions for testing. No daemon is required.

The manifest protocol must make these concepts explicit:

1. Schema/version, baseline/work identity, intended role and allowed scope.
2. Repository aliases bound to the explicitly supplied roots, expected revisions,
   source paths, content identities, and retrievable committed source versions.
3. Mandatory roots and dependency references, knowledge status, provenance and
   source relationships for summaries/derived records.
4. Known unresolved blockers, any explicit non-impacting-change assessment, and
   claim-scoped prerequisite evidence for this intended invocation.

Implement strict validation: unsupported/malformed metadata, duplicate identities,
unknown dependencies, dependency cycles, missing mandatory roots, unresolved
material blockers, absent source, content mismatch, unrecorded working-tree change,
stale summary basis, invalid revision or uncommitted required source must yield
specific blocking reasons. Reject absolute source paths, traversal, symlink escapes
and repository aliases not explicitly designated. Do not resolve dependencies by
searching arbitrary filesystem locations.

Read exact committed source with Git using argument arrays, no shell evaluation.
Treat untrusted path/revision strings as data; constrain revision identifiers and
repository-relative paths before passing them to Git. Unsupported repository
state must return a structured blocker rather than silently using current files.

Required dispatch gates include reviewed architecture, captured work/context,
current-state consistency, qualified scoped adapter, explicit work authority,
and no active or unaccounted implementation invocation. A gate must identify its
evidence and scope. Unavailable adapter/session facts remain UNKNOWN/BLOCKED; the
offline tool must not query external agents or fabricate those facts.

Output one machine-readable receipt on stdout with schema, baseline/work IDs,
context result, dispatch result, checked source identities/revisions, unmet gates,
reason codes with affected references, assumptions and evidence limitations.
Send diagnostics to stderr; use distinct documented exit outcomes for READY,
BLOCKED and invalid input/tool failure. Exact numeric codes may be chosen and
documented by the Implementation Agent; no arbitrary output is accepted as success.

## Acceptance criteria

| ID | Required evidence |
|---|---|
| WP1-AC01 | A complete synthetic, captured source closure validates; a receipt identifies the exact content and required scope. Test qualification records are visibly synthetic, not evidence that the real adapter is qualified. |
| WP1-AC02 | Missing/changed content, unknown dependency, cycle, duplicate ID and missing mandatory authority produce specific blockers naming affected inputs. |
| WP1-AC03 | A summary referring to an obsolete governing revision blocks even when its own bytes match its declared hash. |
| WP1-AC04 | Changed required working-tree state and uncommitted required context block; explicitly evidenced irrelevant changes are distinguishable from undetected drift. |
| WP1-AC05 | Traversal, absolute/unapproved paths, symlink escapes and command-like revision/path strings cannot escape designated roots or execute commands. |
| WP1-AC06 | Otherwise valid context with missing qualification evidence or unknown invocation status remains dispatch-BLOCKED, with context status reported independently. |
| WP1-AC07 | Rerun after process interruption reconstructs the result from supplied persisted inputs without hidden conversation/process state. No writes or network are necessary. |
| WP1-AC08 | Running against the real preparation context honestly reports its unqualified-adapter blocker; no fabricated READY result. |
| WP1-AC09 | Tests isolate changes in temporary fixtures. Real baseline hashes and protected paths remain unchanged; changed-file inventory is inside the allowlist. |

Use meaningful standard-library tests covering these behaviors, with a documented
single command to run them. Verify no network access or model invocation is needed.
Do not claim A-13–15 are fully satisfied by unit fixtures: actual multi-increment
agent/context recovery remains a later experiment obligation.

## Stop conditions

Do not start until a separate dispatch record releases this exact package/context
through the qualified adapter. Once dispatched, stop affected work on baseline
mismatch, an out-of-scope modification need, conflicting authority, an input
protocol ambiguity that changes authority semantics, or inability to verify the
allowed execution boundary. Return BLOCKED with evidence; do not broaden access,
install dependencies, relax checks, implement the adapter, or start service code.

## Required result

Return PASS, PARTIAL, BLOCKED, or INCOMPLETE with work ID, governing context
identity, base/result repository state, changed-file inventory, per-criterion
evidence, exact test commands/results, limitations, discoveries and missing-context
disclosures. Explicitly distinguish synthetic adapter fixtures from live evidence.
The Architect independently inspects the result and decides increment acceptance.

The final result must include no claim that the entire Forge loop, task service,
or experiment is complete. This package does not itself authorize its execution.
