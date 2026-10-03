# E2-PC03 — phase, persistence and cold-restore fixture closure

`E2-PC03 = PASS` for its package-owned exit predicate. PC01 and PC02 baselines are consumed unchanged. The 32 A/N cases have exact phase inputs, independent state/rejection oracles, source invalidation relations and lifecycle separation. The persistence/cold-restore runner contract is fully specified without running a process or experiment Action. D01 and END remain PC04-owned integration dependencies.

## Package and ownership

PC03 addresses `E2-G06` and `E2-G07`, requires PC02, has operation class MIXED and unlocks PC04. Its 34 listed cases comprise A01–A16, N01–N16, D01 and END. The 32 A/N cases are executable specifications; D01 and END are explicitly deferred to PC04’s integrated dependency audit. PC03 does not execute Actions, receipt events, cold restores or P01.

## Completed contracts

The phase oracle fixes INITIAL, PRE_EXTERNAL, external checkpoint, cold-restored, received, validated, reentry-eligible and post-reentry states. It preserves receipt/validation/proof/reentry separation and does not store control labels as trusted inputs. The checkpoint persists the complete canonical bundle, ordered ledger, source and policy pins and trusted identity; a fresh reader receives only the allowlisted files and reviewed contracts. Hidden process memory is prohibited.

Six source-dependent invalidation relations specify stale propagation for knowledge, root proof, slot proof, authority, route and receipt support. Negative mutations change only one designated dimension: lineage, source, currentness, authority, proof, gate, persistence bytes, snapshot lineage, duplicate/conflicting evidence or hidden state. Expected clauses are independent of Planner output.

The native E2-T01 admission pair is the only post-restore evidence ingress: cold restore → `EvidenceSourceAdmission`/durable receipt → separate validation → proof → C03 reentry evaluation. No direct snapshot mutation or event shortcut is included.

## Validation

The independent oracle checks the shared E2 scope/lineage, all eight phase states, external wait and resume transitions, 16 positive and 16 negative case inventories, six invalidation dependencies, trusted bundle allowlist and no-action constraint. It passes under hash seeds 0, 1, 7 and 101 with the declared ordering dimensions. No implementation capability gap or runtime defect was reproduced.

After PC03, the global preflight is 57 executable, 0 fixture-incomplete and 3 dependency-incomplete: D01, END and REVIEW. PC04 is ready and remains unexecuted. P01 retry remains NO because PC04 and the full qualification predicate remain outstanding.

```text
WORK_PACKAGE = E2-PC03
RESULT = PASS
PC03_OWNED_CASES = [E2-A01..E2-A16, E2-N01..E2-N16, E2-D01, E2-END]
BLOCKERS_ADDRESSED = [E2-G06, E2-G07]
FIXTURES_COMPLETED = 32 A/N phase and mutation fixtures; persistence/cold-restore contract; six invalidation relations
ORACLES_COMPLETED = phase/state, negative-clause, invalidation and cold-restore input oracle
POSITIVE_CASES = 16
NEGATIVE_CASES = 16
PC03_CASE_RESULTS = {A01-A16: EXECUTABLE, N01-N16: EXECUTABLE, D01: DEPENDENCY_INCOMPLETE, END: DEPENDENCY_INCOMPLETE}
PC03_OWNED_INCOMPLETE_CASES = []
UPDATED_PREFLIGHT = {EXECUTABLE: 57, FIXTURE_INCOMPLETE: 0, DEPENDENCY_INCOMPLETE: 3, ORACLE_INCOMPLETE: 0, IMPLEMENTATION_CAPABILITY_MISSING: 0, CONTRACT_CONFLICT: 0}
REMAINING_CASE_OWNERSHIP = {E2-PC04: [E2-D01, E2-END, E2-REVIEW]}
NEW_RUNTIME_DEFECTS_ESTABLISHED = []
E2_PC03_RESULT = PASS
E2_PC04_READY = YES
NEXT_PACKAGE = E2-PC04
E2_P01_RETRY_ALLOWED = NO
E2_P02_READY = NO
N_REAL_SATISFIED = NO
CANONICAL_E2_QUALIFIED = NO
PLANNER_V0_1_REQUALIFICATION_READY = NO
IMPLEMENTATION_MODIFIED = NO
EXPERIMENT_ACTIONS_EXECUTED = 0
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
git diff --check = PASS
```
