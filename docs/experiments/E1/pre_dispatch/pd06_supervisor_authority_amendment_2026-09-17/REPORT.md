# Proposed PD-06 Supervisor Authority Amendment — 2026-09-17

**Assessment: narrowly scoped material amendment proposal ready for Architect review. NOT DECIDED, NOT APPLIED; operational publication remains blocked.**

The only proposed authority change is who may become the current holder of the existing Execution Supervisor role. It does not grant new Programmer privileges, waive host authority, change the E1 task or authorize S2, dispatch, activation or ownership.

## Exact amendment identities

| Identity | Value |
| --- | --- |
| Amendment candidate | `PD06-SUPERVISOR-AUTHORITY-AMENDMENT-sha256:979201e9e2d4269a483ce904ae4e7f9329ab0378836e7ada59070b3e4636d3b6` |
| Exact candidate-file SHA-256 | `5a73a14859ddf63a733fcc1941a0a744f9c399863ef7eaf8f6889c4e769d0eae` |
| Proposed composite release-authority identity | `E1-RELEASE-AUTHORITY-sha256:c0d6aed0894c9d07945b017423b3bb2fedb7207780b5e3d4e6c928aacb82bae3` |
| Qualified implementation identity | `sha256:a90b06ddeaf9d2ba58cfd5ce3807f4e5a529aac8e720a63c1e1800e11e345aa0` |
| Original ReleaseBasisId | `E1-RELEASE-BASIS-sha256:bc176574817f6b7fe06fdcf87a71c57b2a8bfe74e55ed20f2aa55ad5d4fa5181` |
| Original ReleaseDecisionId | `E1-RELEASE-DECISION-sha256:43ab22254604a29f3cf2164152803ee5f689f7540e2006c43d27ded87d83d8c0` |

The candidate was written exclusively, fsynced and made read-only. Its content identity and every referenced assessment bind its exact bytes. This is a frozen engineering proposal, not a private runtime authority selection. The original release decision is unchanged. A future Architect amendment decision must be a separate append-only artifact bound to this candidate; the null decision placeholder is not overwritten. Proposed identities confer no authority. No effective new release identity or amended OperationalContextId has been issued.

## Exact proposed rule

CurrentAuthorityHolder = historically released S1, or exactly one explicitly Architect-authorized and qualified successor selected by authenticated SupervisorSuccession; no current ready holder is inferred when evidence is absent.

A successor may hold the role only when **all** of these conditions hold:

1. Complete modern SupervisorInstanceId captured from genuine host observations; PID/configuration equality is insufficient.
2. Instance created through the exact approved host-authorized launch mechanism with independent Architect and human/host consent.
3. Executable, complete implementation inventory and configuration match this amendment-bound qualified requirements and separately approved final applicability.
4. Runtime UID=1000, GID=1000, supplementary groups=[]; complete real/effective/saved credentials satisfy the qualified identity.
5. Host-authorized root placement in /sys/fs/cgroup/unified/kge-forge/executor with 0::/kge-forge/executor verified before dropping runtime credentials.
6. Workspace is /home/gvasend/app/kge-forge with genuine, pinned directory identity.
7. Socket is /tmp/a21m.sock, UID/GID=1000:1000, mode=0600, genuine filesystem and kernel listener identity bound to this process birth.
8. Protocol/configuration/environment match the qualified requirements; source identity and fresh observations verify them.
9. Complete immutable host-launch provenance binds genuine host consent, root parent/start identity, command/spec hashes and placement-before-drop observations.
10. Predecessor is unavailable with fresh authenticated host evidence and all old work accounted for; another eligibility mode requires its own explicit qualified authority, not mere configuration equivalence.
11. Exactly one current authority holder; no conflicting process authority, outstanding invocation or execution ownership, competing successor, stale head or branch.
12. Architect explicitly authorizes this specific predecessor-to-successor event, exact successor ID and qualification, reason and current operational ancestry.
13. The private append-only SupervisorSuccession event and pinned chain/head validate; replay is non-effecting, missing/reordered/substituted evidence fails closed.
14. Independent recovery from private authority and journal reconstructs the successor as the unique current holder; fresh readiness and unchanged QUIESCENT checks also pass.

S1 remains the original immutable historical authority anchor:
`SupervisorHistoricalInstance-sha256:8ffe7a419d3953ed54fb1a73a9bd1d793cbe2c540c181cee9c0ca4e30987d572`.

Its original PID 57950, PPID 57949, executable, argv, UID, cwd and complete cgroup tuple are embedded without alteration in the candidate. S1 predates the modern SupervisorInstanceId schema. Its missing boot/start observations are not reconstructed or invented. Historical authority does not prove current availability; a later matching PID or configuration cannot be S1. The current accepted state is S1 unavailable. The initial proposal uses UNAVAILABLE; the candidate code’s FENCED branch does not authorize an unqualified live-predecessor fencing procedure.

## Material-change boundary

| Released authority | Assessment |
| --- | --- |
| E1-WP-001 | Preserved; exact field hashes and unchanged enforcing sources recorded |
| Programmer tool registry | Preserved; exact field hashes and unchanged enforcing sources recorded |
| read authority | Preserved; exact field hashes and unchanged enforcing sources recorded |
| write/patch authority | Preserved; exact field hashes and unchanged enforcing sources recorded |
| execution-scope semantics | Preserved; exact field hashes and unchanged enforcing sources recorded |
| QUIESCENT semantics | Preserved; exact field hashes and unchanged enforcing sources recorded |
| sequential execution | Preserved; exact field hashes and unchanged enforcing sources recorded |
| ownership semantics | Preserved; exact field hashes and unchanged enforcing sources recorded |
| model-transmission authority | Preserved; exact field hashes and unchanged enforcing sources recorded |
| external destination policy | Preserved; exact field hashes and unchanged enforcing sources recorded |
| released ModelPayloadDigest | Preserved; exact field hashes and unchanged enforcing sources recorded |
| filesystem/snapshot isolation | Preserved; exact field hashes and unchanged enforcing sources recorded |
| audit/evidence isolation | Preserved; exact field hashes and unchanged enforcing sources recorded |
| authority-expansion semantics | Preserved; exact field hashes and unchanged enforcing sources recorded |
| Architect dispatch requirement | Preserved; exact field hashes and unchanged enforcing sources recorded |
| human/host authority boundary | Preserved; exact field hashes and unchanged enforcing sources recorded |

Released ModelPayloadDigest remains `8e9b1fa28d57a4c4e21e28dbe9be7d70e028438ce425862b43b3728d9c22b577`.

The entire original profile remains byte-identical. The non-supervisor fields are separately hashed. The candidate activation module equals the current module after normalizing only the supervisor-readiness selection call. ActivationTransaction, `_host`, invocation ordering and the existing ownership fence retain identical ASTs. The other 30 existing controller modules are byte-identical; two new succession/observation modules and the one selection-call change are the material controller delta. The proposed host launcher is included in the complete implementation identity. All 33 required controller hashes and the host-launcher hash match the frozen accepted qualification.

The human/host boundary remains a requirement: no Programmer root privilege, delegation expansion or generic private-store access is granted. The wrapper requires root-controlled staging and places a root child in the delegated cgroup before credential drop. The host tool has only static/source verification here, not live launch qualification or a grant of host permission.

## Dispatch impact

**Automatic inheritance across the material amendment is denied.** The original Architect authorization requires no MATERIAL governance continuation and exact release/context/profile bindings; its dispatch record explicitly prohibits replacement bindings. The previous PASS concerns the unchanged original release and adopted non-material ancestry only. Equal payload or a passing succession test cannot override those restrictions.

The smallest semantically correct treatment is a **separate explicit Architect dispatch-amendment authorization**, referencing the exact original dispatch and the issued supervisor amendment. It should authorize only that material exception, bind final release/applicability/context/chain/full-context/projection-binding identities, retain the same E1 invocation/task/payload/grants/clearance/audit/ownership/destinations, and preserve all remaining readiness and uncertainty conditions. S2 launch/succession authorization is separate. No dispatch-amendment record or new dispatch decision was created.

The current canonical non-material continuation verifier does not represent this material decision chain. The qualified succession implementation validates a pinned private policy, but does not itself consume a PD-06 amendment or explicit dispatch-amendment decision. Therefore its synthetic dispatch-inheritance PASS is not proof of material inheritance. Before deployment/selection, qualify the typed amendment and dispatch-amendment consumption path. If that narrowly scoped representation is unavailable, a new full Architect dispatch decision is required. Any additional implementation changes require exact qualification and an append-only superseding candidate; do not silently update this frozen candidate.

## Host-launch package verification

| Named installed artifact | Observation |
| --- | --- |
| `/var/lib/kge-forge-supervisor-succession/host_launch.py` | ABSENT |
| `/var/lib/kge-forge-supervisor-succession/LAUNCH_SPEC.json` | ABSENT |
| `/var/lib/kge-forge-supervisor-succession/HOST_LAUNCH_AUTHORIZATION.json` | ABSENT |

The named installed package could not be verified because all three files are absent in the inspected filesystem. Nothing was installed. The repository wrapper/source matches its qualified fingerprint and parses successfully; the proposal spec remains PROPOSED_NOT_AUTHORIZED with a null fresh prelaunch audit hash and old-context ancestry pending final material applicability. No final authorization file exists.

Qualified wrapper SHA-256: `bf98d94070c5fdcc7861fc6383529f31e8de228571f184342c4cbd414b9be7d6`.

The command is preserved verbatim as evidence and **was not executed**:

```sh
sudo /usr/bin/python3.11 /var/lib/kge-forge-supervisor-succession/host_launch.py /var/lib/kge-forge-supervisor-succession/LAUNCH_SPEC.json /var/lib/kge-forge-supervisor-succession/HOST_LAUNCH_AUTHORIZATION.json
```

## Required authorization fields

These are all authorization-file keys accessed by the qualified wrapper. Actual values must come from genuine decisions, not this assessment.

| Field | Required authority and meaning |
| --- | --- |
| `authority` | **ARCHITECT** — Architect; backed by genuine decision provenance, never sufficient as a label |
| `authorization_id` | **ARCHITECT** — Genuine Architect launch-decision identity |
| `decision` | **ARCHITECT** — AUTHORIZE_HOST_SUPERVISOR_LAUNCH; separate from amendment adoption, succession selection and dispatch |
| `host_operator_authorization_id` | **HUMAN_HOST ONLY** — Independent host decision identifying operator/host, exact spec and launcher, purpose and permitted privileged actions. Architect must not invent it |
| `launch_spec_sha256` | **ARCHITECT AND HUMAN_HOST** — Both consent to the exact final spec bytes, including source inventory, paths, runtime identity, cgroup-before-drop, environment and fresh audit hash |
| `launcher_sha256` | **ARCHITECT AND HUMAN_HOST** — bf98d94070c5fdcc7861fc6383529f31e8de228571f184342c4cbd414b9be7d6 |
| `predecessor_id` | **ARCHITECT; HOST acknowledges same target** — SupervisorHistoricalInstance-sha256:8ffe7a419d3953ed54fb1a73a9bd1d793cbe2c540c181cee9c0ca4e30987d572 |
| `qualification_acceptance_id` | **ARCHITECT** — Genuine accepted qualification/applicability decision for the final exact implementation and plan |
| `remove_verified_stale_socket` | **ARCHITECT scope AND HUMAN_HOST action consent** — Conditional true only with explicit permission from both and fresh proof the exact socket is stale; default deny. Observation alone grants no unlink authority |
| `runtime_binding` | **ARCHITECT; HOST acknowledges exact binding** — Final approved release-amendment applicability, authorization/context/chain/profile/execution/store epoch; current old-context proposal is not final applicability |

The Architect decides release/amendment applicability, exact qualified launch scope, and the separate specific succession and dispatch exceptions. The human host authority independently grants the privileged operation on the designated host, including exact launcher/spec hashes, permitted cgroup placement before credential drop, UID/GID/groups, socket/evidence handling and any conditional stale-socket removal. That host decision must have attributable operator/host identity, scope/validity and a source linked to `host_operator_authorization_id`. Both parties must agree on the shared hashes, predecessor, runtime binding and any destructive conditional action. Neither actor substitutes for the other.

**Evidence limitation:** the existing wrapper only tests that `host_operator_authorization_id` is nonempty; it does not resolve an independent host-decision object. Root-controlled file ownership proves staging control, not both decisions’ authenticity. Genuine independent host consent and authentic Architect provenance must be demonstrated before staging or launch. If automation is required to enforce those links, it is an additional implementation change requiring qualification; this assessment does not alter the accepted wrapper or fabricate an approval.

## Proposed S1→S2 binding and stop point

[PROPOSED_S1_TO_S2_BINDING.json](PROPOSED_S1_TO_S2_BINDING.json) binds the exact S1 anchor, this amendment candidate, the proposed composite authority, the current operational ancestor and the qualified implementation. S2 ID/PID/start observations, final amended context, host consent, launch evidence, qualification, Architect succession authorization and event ID are all null. This is not a valid succession event and cannot be selected as runtime authority.

All 123 qualification inputs and archived blobs, all 716 historical reference fingerprints, the unchanged current adapter inventory, original release/profile/dispatch, and unchanged E1 audit/empty ownership ledger passed verification. The accepted independent E1 reconstruction remains applicable to those unchanged inputs; no new live supervisor observation or production activation validation is claimed.

**E1 INACTIVE; NO OWNERSHIP. E1-WP-001 INELIGIBLE and UNDISPATCHED.** No PD-06 amendment, specific S2 authorization, S2 launch, succession event, activation event, new dispatch authority, model request or E1 implementation effect occurred.

## Evidence

- [Immutable candidate](PD06_AMENDMENT_CANDIDATE.json) and [identity receipt](CANDIDATE_IDENTITY.json).
- [Exact qualified implementation](QUALIFIED_IMPLEMENTATION_IDENTITY.json).
- [Material-boundary verification](MATERIAL_BOUNDARY_ASSESSMENT.json).
- [Dispatch impact](DISPATCH_IMPACT_ASSESSMENT.json).
- [Host package and authorization fields](HOST_PACKAGE_ASSESSMENT.json).
- [Verification results](VERIFICATION.json).
