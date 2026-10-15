# INSTALLATION-I04 — native ATTEST / ingress installation

Generic installation qualification passed before the exact authorized P04 application. Two ordinary INSTALL_DEFINITION events install the atomic authority-reference/attestor/predicate set and its ingress definition. Operating ATTEST was issued/admitted separately; installation did not issue ATTEST rights or create an attestation instance.

The I03 sealed identities and source bytes remain unchanged. The original route checkpoint and every historical report are preserved. Both boundary oracles were recorded before the respective transition; the second grant binds the actual first-event descendant.

## Results

```text
WORK_PACKAGE = INSTALLATION-I04
RESULT = PASS
SELECTED_OPTION = AUTHORIZE_P04_ATTEST_INGRESS_INSTALLATION
AUTHORIZATION_AUTHENTICATION = PASS
ATTEST_INGRESS_INSTALLATION_CAPABILITY = PASS
INSTALL_AUTHORITY_ADMISSION = PASS
INSTALL_AUTHORITY_APPLICABILITY = PASS
DEPENDENCY_PROVENANCE_CARDINALITY = 4
DEPENDENCY_PROVENANCE = PASS
POST_INSTALL_BUNDLE_PATH = docs/plans/DETERMINISTIC_PLANNER_V0_1_E2_P04_POST_ATTEST_INSTALL_BUNDLE_1.json
CURRENTNESS = PASS
PERSISTENCE = PASS
COLD_RESTORE = PASS
REPLAY = PASS
DETERMINISM = PASS
HISTORICAL_IMMUTABILITY = PASS
ATOMICITY = PASS
IDEMPOTENCE = PASS
SECURITY_NEGATIVES = PASS
OLD_A09_CANDIDATE = STALE
old_candidate_failure = PARENT_MISMATCH
A09_CANDIDATE_REMATERIALIZED = YES
A09_PREFLIGHT = PASS
NEXT_PACKAGE = P04-A09-E02-ATOMIC-INGRESS-CONTINUATION-CONTRACT
P04_EXECUTION_READY = NO
E2_P04_READY = NO
A09_A13_EXECUTED = NO
E2_FINISH_EXECUTED = NO
P03_RESULT = PASS
P03_HISTORICAL_CORRESPONDENCE = UNPROVEN
N_REAL_SATISFIED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
git_diff_check = PASS
legacy_regression_counterexamples = docs/plans/qualification/INSTALLATION_I04_1/legacy-baseline-counterexamples.json
legacy_regression_log = docs/plans/qualification/INSTALLATION_I04_1/legacy-baseline-tests.log
```

## Canonical installation trace

```json
[
  {
    "operation": "INSTALL",
    "type": "AUTHENTICATION_DEFINITION_SET",
    "authority": {
      "$type": "ArtifactIdentity",
      "kind": {
        "$enum": "IdentityKind",
        "value": "AUTHORITY_IDENTITY"
      },
      "namespace": "planner-install-authority-v1",
      "sha256": "443808e8ca1150f8ff8abc807b8cd1365500c17695caf86278e4efad2e66a7c1"
    },
    "event": {
      "$type": "ArtifactIdentity",
      "kind": {
        "$enum": "IdentityKind",
        "value": "CONTENT_IDENTITY"
      },
      "namespace": "planner-event-v1",
      "sha256": "a537ba9f5be1ef3d099ff178028847036e83406bd338e662f5b7680d4b90a3a0"
    },
    "pre_state": {
      "$type": "ArtifactIdentity",
      "kind": {
        "$enum": "IdentityKind",
        "value": "CONTENT_IDENTITY"
      },
      "namespace": "planner-snapshot-v1",
      "sha256": "99e47ad1e462c30cd33e2258e4c74ff670164fa7378e5a998e0f23b9256e4454"
    },
    "post_state": {
      "$type": "ArtifactIdentity",
      "kind": {
        "$enum": "IdentityKind",
        "value": "CONTENT_IDENTITY"
      },
      "namespace": "planner-snapshot-v1",
      "sha256": "92e51d3a60bb02d807fdc7b340546b1fcd08a94a121a3effb6a4cc4e911484a6"
    },
    "parent": {
      "$type": "ArtifactIdentity",
      "kind": {
        "$enum": "IdentityKind",
        "value": "CONTENT_IDENTITY"
      },
      "namespace": "planner-event-v1",
      "sha256": "a19b52ab601c6d3c7668b78c6e20cc87e54cfc317595e4da641fcbb7d107fb1e"
    },
    "sequence": 4
  },
  {
    "operation": "INSTALL",
    "type": "EVIDENCE_INGRESS_CONTRACT",
    "authority": {
      "$type": "ArtifactIdentity",
      "kind": {
        "$enum": "IdentityKind",
        "value": "AUTHORITY_IDENTITY"
      },
      "namespace": "planner-install-authority-v1",
      "sha256": "8519cc44bdef58aeac7fb7c366db08cfde44b2f7b015a6f9889d8dd07665f172"
    },
    "event": {
      "$type": "ArtifactIdentity",
      "kind": {
        "$enum": "IdentityKind",
        "value": "CONTENT_IDENTITY"
      },
      "namespace": "planner-event-v1",
      "sha256": "549e41859f55cd3414d91b5ce97f023ab9e150f55ed01ae81a9a9dc5ef2f362c"
    },
    "pre_state": {
      "$type": "ArtifactIdentity",
      "kind": {
        "$enum": "IdentityKind",
        "value": "CONTENT_IDENTITY"
      },
      "namespace": "planner-snapshot-v1",
      "sha256": "92e51d3a60bb02d807fdc7b340546b1fcd08a94a121a3effb6a4cc4e911484a6"
    },
    "post_state": {
      "$type": "ArtifactIdentity",
      "kind": {
        "$enum": "IdentityKind",
        "value": "CONTENT_IDENTITY"
      },
      "namespace": "planner-snapshot-v1",
      "sha256": "c5c85434ddfb69be7f327e9e8fd72d2c7270505cf4908ea4fd9b4918075c1591"
    },
    "parent": {
      "$type": "ArtifactIdentity",
      "kind": {
        "$enum": "IdentityKind",
        "value": "CONTENT_IDENTITY"
      },
      "namespace": "planner-event-v1",
      "sha256": "a537ba9f5be1ef3d099ff178028847036e83406bd338e662f5b7680d4b90a3a0"
    },
    "sequence": 5
  }
]
```

## Qualification

39 targeted tests passed. They cover generic non-E2 positive projection, closed definitions, wrong references/context/authority, exact provenance cardinality, transient attestation chain guards, atomic publication failures, retry/conflict semantics, independent reproduction, source invalidation and four fresh-process hash-seed readers. P04 adds 24 fresh readers across both new installation boundaries (three per boundary per hash seed 0/1/7/101), plus cold restore at both installation boundaries, exact prefix replay and independent two-event reproduction.

A09 preflight evaluates an isolated immutable candidate through ordinary native admission checks; its proposed Snapshot is discarded and no Evidence/receipt event is committed. The transient E02 attestation body is held only in memory. The old candidate remains unmodified and fails PARENT_MISMATCH.

The expected dependency set has four complete Provenance records: installed ingress body, shared gate/requirement source, installed route body and common installed authentication-set body. Member bodies and authority admission receipts are pinned installation support, not extra A09 dependencies. Extra, missing and duplicate records fail closed.

## Continuation boundary

A09 preflight: **PASS**. P04 execution readiness remains **NO**: A10-A13 prospective definitions remain offline and their authority/adapters are not installed. No later lifecycle instance is expected yet. I04 authority does not cover them.

```json
{
  "A10_VALIDATION": {
    "status": "RUNTIME_BLOCKED",
    "authority": "AUTHORITY_REQUIRED",
    "reason": "Prepared offline definitions are not installed; no authority from I04 applies; generic closed adapter for this type not enabled"
  },
  "A11_TYPED_EVIDENCE_PROOF": {
    "status": "RUNTIME_BLOCKED",
    "authority": "AUTHORITY_REQUIRED",
    "reason": "Prepared offline definitions are not installed; no authority from I04 applies; generic closed adapter for this type not enabled"
  },
  "A12_REENTER_ACTION_RESULTS": {
    "status": "RUNTIME_BLOCKED",
    "authority": "AUTHORITY_REQUIRED",
    "reason": "Prepared offline definitions are not installed; no authority from I04 applies; generic closed adapter for this type not enabled"
  },
  "ROOT_SLOT": {
    "status": "RUNTIME_BLOCKED",
    "authority": "AUTHORITY_REQUIRED",
    "reason": "Prepared offline definitions are not installed; no authority from I04 applies; generic closed adapter for this type not enabled"
  },
  "A13_FINISH_RESULT": {
    "status": "RUNTIME_BLOCKED",
    "authority": "AUTHORITY_REQUIRED",
    "reason": "Prepared offline definitions are not installed; no authority from I04 applies; generic closed adapter for this type not enabled"
  },
  "INSTANCES": {
    "status": "LIFECYCLE_INSTANCE_NOT_YET_EXPECTED",
    "objects": [
      "ValidationResult",
      "Evidence proof",
      "REENTER ActionResult",
      "SLOT_PROOF",
      "ROOT_PROOF",
      "FINISH ActionResult"
    ]
  }
}
```

## Preservation

P03 PASS and historical correspondence UNPROVEN remain unchanged. N-REAL remains NO; no release conclusion follows. A09-A13 and E2-FINISH were not executed. E1 hash comparison reports zero changes. git diff --check passed. The expanded legacy Evidence-admission suite has 4 passes, 4 failures and 12 errors. The same 16 failures reproduce using the exact pre-I04 Evidence module (hash verified), so they remain separately recorded rather than reported as passing. Representative native failures are RECEIPT_CHANGED_CONTROL and FIELD_PROVENANCE. The pre-existing frozen-E1 broad collection blocker is also preserved; neither failure class was repaired by this bounded package.

[Machine evidence](DETERMINISTIC_PLANNER_V0_1_INSTALLATION_I04_RESULT.json) and [native bundle](DETERMINISTIC_PLANNER_V0_1_E2_P04_POST_ATTEST_INSTALL_BUNDLE_1.json).

The nine adapter tests also passed a final verification after the consumer guard was completed. Intermediate fresh readers run after termination of the qualification writer and verify absence of ingress before its installation. The old A09 candidate hash matches its pre-I03 hash. Runtime source hashes and the additional read-only comparison evidence are recorded in the machine companion; the original execution evidence and native bundles remain immutable.

Seven additional negative cases reseal valid member/content/descriptor hashes before presenting wrong native authority, attestor and predicate semantics; all reject at the semantic clauses rather than checksum validation. This adds one test (40 unique targeted tests total). Both installation boundaries now have twelve fresh readers after writer termination, with the earlier twelve writer-in-process reads retained separately.

A09 live execution remains a separate qualification boundary: I04 passes native semantic preflight with an explicit transient E02 instance. The existing codec Evidence transaction does not accept that transient operand. Its atomic receipt/replay binding must be recovered/qualified before A09 execution; I04 does not bypass the installed consumer guard, serialize an instance, or claim live receipt qualification. This is the first continuation contract to close, ahead of the still-offline A10–A13 contracts.

The machine companion verifies each of the four provenance records separately, including its native role, physical source pin, canonical definition/event/authority binding and applicable context. Provenance itself has no lineage/generation fields. Canonical control remains EXTERNAL_WAIT at PRE_RECEIPT; no P04 lifecycle advancement occurred. All 10,967 pre-existing frozen-E1 files retain their hashes.
