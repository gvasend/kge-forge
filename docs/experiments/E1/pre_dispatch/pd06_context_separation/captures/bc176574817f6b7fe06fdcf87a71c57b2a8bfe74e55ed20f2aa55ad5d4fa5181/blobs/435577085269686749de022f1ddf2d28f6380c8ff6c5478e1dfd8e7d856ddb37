# E1-CONTEXT-1 — prepared input protocol

This is an Architect-defined input contract for E1-WP-001, not its implementation.
CONTEXT_MANIFEST.json is a real prepared instance. It intentionally has unresolved
dispatch gates and must not yield dispatch READY.

- `schema_version`, `baseline_id`, `work_id`, `intended_role` and `status` identify
  what is being assessed. Unsupported versions or malformed fields are invalid.
- `repositories` maps explicit aliases to designated root paths and expected
  committed source states. Caller mappings must match the authorized identities;
  arbitrary root substitution is not permission to inspect unrelated information.
- `sources` identifies repository-relative files, exact SHA-256 content, source
  revision, knowledge status, governing dependencies and usage. A source carries
  either `revision` or `revision_binding`, never both.
- The sole supported binding in this preparation is `package_capture_commit`:
  supplied externally as a full commit identity after preparation is committed.
  It refers to that capture, not HEAD or an arbitrary later branch tip. Missing
  binding is an explicit blocker. The final dispatch record supplies it; this
  avoids a commit having to contain its own hash.
- `mandatory_roots` are required source identities. `dependencies` are governing
  relationships explicitly specified in the manifest, not every Markdown link.
  Validate the reachable closure and detect missing IDs, duplicates and cycles.
- `derived_from`, when present, records source ID and source content identity.
  Verify those identities and revisions against the governing closure; an old
  summary is not made fresh merely by matching its own hash.
- Source `knowledge_status` distinguishes DECIDED, ASSUMED, UNRESOLVED and
  SUPERSEDED. An assumption or unresolved item is not a decided requirement.
  Historical evidence may be present without being relied on as governing authority;
  usage and declared blockers must remain explicit.
- `scope` describes permitted source writes, designated read roots, scratch binding,
  protected areas and external-tool restrictions. It does not itself enforce them.
- `prerequisites` reports status and evidence references for this exact work.
  Only PASS with matching, applicable, retrievable reviewed evidence can satisfy
  a required gate. UNKNOWN, BLOCKED or missing evidence must not be coerced to PASS.
- `unresolved_issues` and `context_sufficiency` preserve the Architect's assessment
  and limitations. Adequacy to prepare a package is not proof of invocation fit,
  adapter confinement, or authority to dispatch it.

The source-content checks and the required dispatch-gate checks are separate.
Context may be valid while dispatch remains blocked. The receipt must identify
which facts were actually verified and which gate conclusions rely on supplied
Architect-reviewed evidence. It is not an independent runtime adapter attestation.

Current prerequisite facts are deliberately a preparation snapshot. Closing a
gate requires a new versioned context/release assessment, not editing a manifest
silently after dispatch. Human/authority changes need an impact decision; benign
later intervention entries do not automatically replace frozen governing sources.

Working-state comparison must account for the intended implementation stage:
pre-dispatch expects the captured preparation; post-implementation verification
reports in-scope changes separately and must not bless unrelated authority edits.
This utility's first increment assesses pre-dispatch only. It may not claim that
ordinary implementation output is an authorized update to baseline knowledge.
