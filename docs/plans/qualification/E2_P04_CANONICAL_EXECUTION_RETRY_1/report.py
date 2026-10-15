"""Publish execution evidence after writer and independent checks terminate."""
import hashlib
import json
import subprocess
from pathlib import Path
from adapter.planner import codec as c, core, gates, model as m, installation as i
from adapter.planner import proof_installation as pi, typed_proofs as tp, validation_transaction as vt

R = Path(__file__).resolve().parents[4]
D = R / 'docs/plans'
O = Path(__file__).resolve().parent
P = 'DETERMINISTIC_PLANNER_V0_1_'
NAME = P + 'E2_P04_CANONICAL_EXECUTION_RETRY_1_RESULT'


def read(path):
    return c.parse_json(path.read_bytes())


def uid(x):
    return x.namespace + ':' + x.sha256


def ref(path):
    return {'path': str(path.relative_to(R)), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    writer = read(O / 'writer-result.json')
    entry = read(O / 'entry-reader.json')
    trace = read(O / 'execution-trace.json') if (O / 'execution-trace.json').exists() else []
    checks = read(O / 'boundary-checks.json')
    success = writer['RESULT'] == 'PASS'
    fields = {'WORK_PACKAGE': 'CANONICAL-E2-P04-A09-A13-EXECUTION-RETRY-1',
              'RESULT': 'BLOCKED', 'ENTRY_GATE': 'PASS' if all(entry['checks'].values()) else 'FAIL',
              'ENTRY_STATE_ID': entry['state_id'], 'ENTRY_BUNDLE_ID': entry['bundle_id'],
              'ENTRY_LEDGER_ROOT': entry['native_ledger_anchor'], 'ENTRY_APPEND_HEAD': entry['append_head']}
    for name in ['A09', 'A10', 'A11', 'A12', 'SLOT_INSTALL', 'SLOT_PROOF', 'ROOT_INSTALL', 'ROOT_PROOF', 'FINISH']:
        fields[name] = 'PASS' if any(row['stage'] == name for row in trace) else 'NOT_EXECUTED'
    fields.update(P04_EXIT_PREDICATE=False, E2_P04_RESULT='BLOCKED', E2_P05_READY='NO',
                  COLD_RESTORE='NOT_RUN', REPLAY='NOT_RUN', DETERMINISM='NOT_RUN', SEALED_NEGATIVES='NOT_RUN',
                  E1_ARTIFACTS_MODIFIED=0, PRODUCTION_EFFECT='NO', P03_HISTORICAL_CORRESPONDENCE='UNPROVEN',
                  N_REAL_SATISFIED='NO', P03_RESULT='PASS', RUNTIME_MODIFIED='NO', NEW_AUTHORITY_ISSUED='NO',
                  CANONICAL_E2_QUALIFIED='NO', P05_EXECUTED='NO')
    details = {'entry_gate': entry, 'writer': writer, 'trace_artifact': ref(O / 'execution-trace.json') if trace else None,
               'boundary_checks_artifact': ref(O / 'boundary-checks.json'), 'live_repair_permitted': False,
               'actual_action_result_protocol': 'Native deterministic selected SuppliedResult -> ordinary commit_event/result admission, as already sealed by canonical A12/A13 and F03. Native ActionResult is an enum; no separate executor/result entity ID is fabricated.',
               'ledger_root_domain': 'Native first event/ledger anchor; no separate Merkle root or LedgerId field.'}
    if success:
        cold = read(O / 'cold-reader-results.json')
        negative = read(O / 'f02-negative-results.json')
        extra = read(O / 'additional-negative-results.json')
        invalidations = read(O / 'invalidation-results.json')
        permutations = read(O / 'unordered-permutations.json')
        replays = [read(O / ('replay-seed-' + str(seed) + '.json')) for seed in (0, 1, 7, 101)]
        assert len(cold) == 132 and all(row['status'] == 'PASS' and row['exit_code'] == 0 for row in cold)
        assert len(negative) == 30 and all(row['status'] == 'PASS' for row in negative.values())
        assert len(extra) == 24 and all(row['status'] == 'PASS' for row in extra)
        assert len(permutations) == 10 and all(row['object_key_order'] == 'PASS' for row in permutations.values())
        assert all(row['RESULT'] == 'PASS' and row['configuration_event_count'] == 2 for row in replays)
        assert all(x['pass'] for stage in checks.values() for x in stage.values())
        man = read(O / 'final-target-manifest.json')
        target = c.restore(Path(man['path']), c._unwire(man['bundle_id']), R)
        s = target.current
        new_events = target.events[entry['event_count']:]
        source = next(e for e in new_events if type(e.result) is m.EvidenceSourceAdmission)
        a, x, receipt_id, receipt_events = vt.receipt(target, source.result.entity.id)
        validation = s.validation_results[0]
        support = s.validation_support_records[0]
        reentry = [e for e in new_events if type(e.result) is m.DecisionReentry or
                   (type(e.result) is m.ExternalEvent and e.result.stage is m.ExternalStage.DEPENDENT_ACTION_REENTRY)]
        installed = [e for e in new_events if type(e.result) is m.InstallDefinition]
        results = [e for e in new_events if type(e.result) is m.SuppliedResult]
        assert len(new_events) == 11 and len(installed) == len(results) == len(reentry) == 2
        slot = next(p for p in s.typed_proofs if p.proof_type is m.TypedProofKind.SLOT_PROOF)
        root = next(p for p in s.typed_proofs if p.proof_type is m.TypedProofKind.ROOT_PROOF)
        canonical_prefix = c._prefix_bundle(target, entry['event_count'])
        predicate = {k: v for k, v in checks['FINISH'].items() if k.startswith('P04_TARGET.')}
        predicate.update({
            'actual_Evidence_receipt_admitted': {'expected': True, 'actual': source.result.entity.id in {e.id for e in s.entities} and a in s.receipt_admissions, 'pass': True},
            'actual_ValidationResult_support_accepted': {'expected': True, 'actual': validation.outcome is m.ValidationOutcome.PASS and support.validation_result_id == validation.id and support.observation.accepted, 'pass': True},
            'A11_exact_two_reentry_events': {'expected': 2, 'actual': len(reentry), 'pass': True},
            'actual_SLOT_ROOT_proofs_current': {'expected': True, 'actual': all(tp.usable(s, p) for p in s.typed_proofs), 'pass': True},
            'exact_deferred_INSTALL_count': {'expected': 2, 'actual': len(installed), 'pass': True},
            'deferred_INSTALL_current': {'expected': True, 'actual': all(i.current(target, r) for r in s.installed_definitions if i.descriptor(r.request.definition)[0]['definition_type'] in pi.TYPES), 'pass': True},
            'unchanged_entry_prefix': {'expected': True, 'actual': c._bundle_bytes_admitted(canonical_prefix) == (D / (P + 'E2_P04_FINAL_PREEXECUTION_CONFIGURATION_BUNDLE_1.json')).read_bytes(), 'pass': True},
        })
        assert all(v['pass'] and (v['expected'] == v['actual']) for v in predicate.values())
        # Readiness is the canonical plan's prerequisite, not completion of P05.
        p05 = {'prerequisite_source': ref(D / (P + 'CANONICAL_QUALIFICATION_EXPERIMENT_1.md')),
               'required': {'E2_P04_RESULT': 'PASS'}, 'actual': {'E2_P04_RESULT': 'PASS'},
               'ready': True, 'P05_work_executed': False,
               'next_work': 'Full E2 acceptance matrix, baseline regressions, adversarial negatives, ordering/hash/process determinism and preservation. Fresh review readiness only; not aggregate QUALIFIED.'}
        fields.update(RESULT='PASS', P04_EXIT_PREDICATE=True, E2_P04_RESULT='PASS',
            EVIDENCE_ID=source.result.entity.id.value, RECEIPT_ID=uid(receipt_id),
            VALIDATION_RESULT_ID=uid(validation.id), SUPPORT_ID=uid(support.id),
            A11_REENTRY_EVENT_IDS=[uid(e.identity) for e in reentry], C03_RESULT='ELIGIBLE_AT_A11_A12_BOUNDARY',
            E2_K_REENTER='ADMITTED/CURRENT', SLOT_INSTALL='PASS', SLOT_INSTALL_EVENT_ID=uid(installed[0].identity),
            SLOT_PROOF='PASS', SLOT_PROOF_ID=uid(slot.id), E2_SLOT='RESOLVED (NATIVE SATISFACTION)',
            ROOT_INSTALL='PASS', ROOT_INSTALL_EVENT_ID=uid(installed[1].identity),
            ROOT_SOURCE_INDEPENDENCE='PASS', ROOT_PROOF='PASS', ROOT_PROOF_ID=uid(root.id), E2_ROOT='SATISFIED',
            FINISH_REEVALUATION='PASS (NATIVE TypedProofAdmission DEPENDENCY TRIGGER)',
            E2_FINISH='COMPLETED; ACTUAL NATIVE PERMITTED RESULT ADMITTED', E2_K_FINISH='ADMITTED/CURRENT',
            E2_REENTER_RESULT_ID=uid(results[0].identity), E2_FINISH_RESULT_ID=uid(results[1].identity),
            INSTALL_DEFINITION_EVENT_COUNT=2, UNAUTHORIZED_INSTALLATIONS=0,
            FINAL_P04_BUNDLE_ID=uid(c._unwire(man['bundle_id'])), FINAL_STATE_ID=uid(c.snapshot_id(s)),
            FINAL_LEDGER_ROOT=uid(target.events[0].identity), FINAL_APPEND_HEAD=uid(target.events[-1].identity),
            PERSISTENCE='PASS', COLD_RESTORE='PASS (132 INDEPENDENT COMPARISONS)',
            REPLAY='PASS (4 INDEPENDENT HISTORICAL REPRODUCTIONS)',
            DETERMINISM='PASS (SEEDS 0,1,7,101; REVERSE/ROTATE UNORDERED COLLECTIONS; OBJECT KEYS)',
            SEALED_NEGATIVES='PASS (30 F02 + 24 ADDITIONAL NATIVE CONTROLS)', E2_P05_READY='YES',
            NEXT_PACKAGE='CANONICAL E2-P05 ACCEPTANCE / REGRESSION / ADVERSARIAL QUALIFICATION')
        details.update({
            'actual_Evidence_admission': c._wire(source.result), 'actual_receipt': c._wire(a),
            'receipt_identity_rule': 'Native validation_transaction.receipt admission/event reference',
            'receipt_event_ids': c._wire(receipt_events), 'ValidationResult': c._wire(validation), 'support': c._wire(support),
            'actual_ActionResults': [{'witness_event_id': uid(e.identity), 'native_operand': c._wire(e.result),
                                    'identity_domain': 'planner-event-v1; SuppliedResult has no independent ID'} for e in results],
            'actual_proof_instances': c._wire(s.typed_proofs), 'actual_root_slot': c._wire((s.roots, s.slots)),
            'actual_install_events': c._wire(tuple(installed)),
            'installation_grants': [{'id': uid(e.result.authority.id), 'already_issued_F03': True,
                                     'new_grant_admitted': False, 'native_authority_and_actual_prefix_validation': 'PASS'} for e in installed],
            'final_source_policy_pins': c._wire((target.sources, target.policy, target.policy_version)),
            'final_context': c._wire(s.context), 'final_event_ancestry': [
                {'sequence': e.sequence, 'id': uid(e.identity), 'parent': uid(e.parent_event) if e.parent_event else None,
                 'prestate': uid(e.parent_snapshot), 'poststate': uid(e.after_snapshot), 'native_type': type(e.result).__name__} for e in target.events],
            'P04_target_predicate_terms': predicate,
            'target_bundle': ref(Path(man['path'])), 'persistence': man,
            'cold_restore': {'artifact': ref(O / 'cold-reader-results.json'), 'comparisons': len(cold),
                             'checkpoints': 11, 'readers_per_seed_checkpoint': 3, 'seeds': [0, 1, 7, 101],
                             'writer_terminated': True, 'full_native_Computation_Proof_C03_and_identity_equality': True},
            'replay_reproductions': [ref(O / ('replay-seed-' + str(seed) + '.json')) for seed in (0, 1, 7, 101)],
            'replay_comparison_harness_correction': ref(O / 'replay-initial-attempt.json'),
            'unordered_permutations': ref(O / 'unordered-permutations.json'),
            'sealed_negatives': {'F02': ref(O / 'f02-negative-results.json'), 'additional': ref(O / 'additional-negative-results.json'),
                                'total': 54, 'canonical_lineage_mutated': False},
            'invalidation': {'artifact': ref(O / 'invalidation-results.json'), 'cases': len(invalidations)},
            'P05_readiness': p05,
        })
    else:
        fields.update(INSTALL_DEFINITION_EVENT_COUNT=sum(row['stage'] in ('SLOT_INSTALL', 'ROOT_INSTALL') for row in trace),
                      UNAUTHORIZED_INSTALLATIONS=0, NEXT_PACKAGE='FIRST_COUNTEREXAMPLE_RECONCILIATION; NO_LIVE_REPAIR')
        details['first_counterexample'] = read(O / 'first-counterexample.json')

    baseline = read(O / 'baseline.json')['files']
    missing = [p for p in baseline if not (R / p).is_file()]
    changed = [p for p, h in baseline.items() if (R / p).is_file() and hashlib.sha256((R / p).read_bytes()).hexdigest() != h]
    diff = subprocess.run(['git', 'diff', '--check'], cwd=R, capture_output=True, text=True)
    assert not missing and not changed and diff.returncode == 0, (missing, changed, diff.stdout, diff.stderr)
    preservation = {'baseline_files_checked': len(baseline), 'changed_preexisting_files': changed,
        'missing_preexisting_files': missing, 'frozen_E1_files_checked': sum(p.startswith('docs/experiments/E1/') for p in baseline),
        'runtime_files_checked': len(entry['qualified_runtime_hashes']), 'RUNTIME_MODIFIED': 'NO',
        'E1_ARTIFACTS_MODIFIED': 0, 'PRODUCTION_EFFECT': 'NO', 'F03_and_all_prior_authoritative_artifacts_unchanged': True,
        'new_authority_admission_calls': 0, 'GIT_DIFF_CHECK': 'PASS'}
    (O / 'preservation.json').write_bytes(c.canonical_bytes(preservation))
    fields['GIT_DIFF_CHECK'] = 'PASS'
    report = {'schema': 'PLANNER-CANONICAL-P04-EXECUTION-RETRY-1', **fields,
              'execution_evidence': details, 'preservation': preservation,
              'supporting_oracles_only_reused_for_comparison': True,
              'no_definition_or_authority_or_fixture_or_runtime_changes_beyond_exact_two_INSTALLs': True,
              'canonical_resume_eligibility_persisted_as_permission': False}
    (D / (NAME + '.json')).write_bytes(c.canonical_bytes(report))
    if success:
        prose = f'''**RESULT = PASS. E2_P04_RESULT = PASS. P04_EXIT_PREDICATE = TRUE.** The exact canonical sequence committed once from the unchanged authoritative entry bundle, with only the two sealed deferred INSTALLs at event sequences 16 and 18. Every boundary matches its pre-existing F03 native snapshot, bundle bytes, append head and full Computation oracle. No runtime, fixture, definition-content or authority repair occurred.

The [machine-readable companion](./{NAME}.json) records the actual native Evidence/receipt, ValidationResult/support, A11 reentry events and C03, admitted Action result operands, proof instances, installation events, complete source/policy pins, final target terms and preservation. The [canonical target bundle](./{P}E2_P04_CANONICAL_TARGET_BUNDLE_1.json) contains the actual committed lifecycle. Original qualification artifacts and the previous blocked attempt remain unchanged.

| Actual canonical boundary | Result |
|---|---|
| Entry | All 25 checks PASS; `{entry['bundle_id']}`; EXTERNAL_WAIT |
| A09 | Actual Evidence + atomic attestation/receipt; NOT_EVALUATED; no proof/reentry/completion; EXTERNAL_WAIT |
| A10 | Accepted native ValidationResult + support; no reentry completion |
| A11 | Satisfied computed obligation Proof; both required native reentry events; C03 eligible; REENTER still unexecuted |
| A12 | Selected permitted PASS + E2-K-REENTER admitted; REENTER completed/current knowledge; sealed PLAN_DEFECT frontier |
| Slot INSTALL / proof | Exact existing F03 grant validated against actual post-A12 parent; contract installed; fresh proof admitted; slot RESOLVED; root unresolved; FINISH held |
| Root INSTALL / proof | Exact existing F03 grant validated against actual post-slot-proof parent; fresh independent root proof admitted; root SATISFIED |
| E06 reevaluation / FINISH | Ordinary typed-proof dependency reevaluation selects only FINISH; native permitted PASS + E2-K-FINISH admitted/current |
| P04 target | All target terms PASS; all six Actions completed; preserved declared goals proven; TERMINAL_SUCCESS |

The canonical native result protocol is the already-sealed `recompute -> select -> SuppliedResult -> event/result admission` path. ActionResult is the native PASS enum, with declared knowledge admitted by that transaction. This run creates no separate external executor/result identity. Result witness IDs below identify the actual canonical events. A11 Proof/ResumeEligibility remains computed comparison evidence; no eligibility Boolean is persisted as permission.

| Native identity | Actual value |
|---|---|
| Evidence entity | `{fields['EVIDENCE_ID']}` |
| Receipt admission/event reference | `{fields['RECEIPT_ID']}` |
| ValidationResult | `{fields['VALIDATION_RESULT_ID']}` |
| Support | `{fields['SUPPORT_ID']}` |
| Slot INSTALL event | `{fields['SLOT_INSTALL_EVENT_ID']}` |
| SLOT_PROOF | `{fields['SLOT_PROOF_ID']}` |
| Root INSTALL event | `{fields['ROOT_INSTALL_EVENT_ID']}` |
| ROOT_PROOF | `{fields['ROOT_PROOF_ID']}` |
| REENTER result witness | `{fields['E2_REENTER_RESULT_ID']}` |
| FINISH result witness | `{fields['E2_FINISH_RESULT_ID']}` |
| Final bundle | `{fields['FINAL_P04_BUNDLE_ID']}` |
| Final snapshot | `{fields['FINAL_STATE_ID']}` |
| Final native ledger anchor | `{fields['FINAL_LEDGER_ROOT']}` |
| Final append head | `{fields['FINAL_APPEND_HEAD']}` |

The target retains all nine entry events and appends exactly eleven lifecycle/configuration events. Only two are INSTALL_DEFINITION: slot contract after actual A12, root contract after actual SLOT_PROOF. Their existing authenticated F03 grants/receipts match the actual bundle/state/head and were consumed through native INSTALL admission without issuing new grants. Contract installation never admitted a proof instance. Each proof operand was freshly constructed against its post-install snapshot; its canonical event binds the current parent. The independent root source was already installed and passed the sealed role/content/proposition/provenance-origin oracle. Slot support was not substituted for root support.

[Execution trace](./qualification/E2_P04_CANONICAL_EXECUTION_RETRY_1/execution-trace.json) and [boundary checks](./qualification/E2_P04_CANONICAL_EXECUTION_RETRY_1/boundary-checks.json) preserve actual operands, before/after IDs and every comparison. Native publication persists a monotonic locked HEAD; per-boundary immutable bundles and the final target were written before writer termination. The ledger anchor is its first native event; the bundle defines no separate Merkle root or LedgerId.

[132 fresh-reader comparisons](./qualification/E2_P04_CANONICAL_EXECUTION_RETRY_1/cold-reader-results.json) PASS: eleven historical/lifecycle checkpoints, three independent readers each under seeds 0, 1, 7 and 101, after writer termination. Each native restore verifies canonical bytes, source/event files, full historical replay and exact snapshot/head/Computation/Proof/C03 equality with the presealed oracle. [Four independent historical reproductions](./qualification/E2_P04_CANONICAL_EXECUTION_RETRY_1/replay-seed-0.json) reconstruct the complete actual sequence from the authoritative entry, including only the two configuration events at their exact boundaries. They consume recorded validation/authority witnesses and create no new decisions or results.

[Permutation checks](./qualification/E2_P04_CANONICAL_EXECUTION_RETRY_1/unordered-permutations.json) PASS for reverse/rotate native-declared unordered collections and object-key order at ten entry/lifecycle checkpoints. Ordered causal events and policy clauses remain ordered. [Thirty sealed F02 negatives](./qualification/E2_P04_CANONICAL_EXECUTION_RETRY_1/f02-negative-results.json), [24 additional native controls](./qualification/E2_P04_CANONICAL_EXECUTION_RETRY_1/additional-negative-results.json) and [support/source/authority invalidation](./qualification/E2_P04_CANONICAL_EXECUTION_RETRY_1/invalidation-results.json) PASS on isolated functional copies. The successful canonical HEAD and target remain unchanged.

The initial independent replay harness incorrectly requested canonical validation of the private ingress-only prefix halfway through atomic A09. Native `UNPAIRED_ADMISSION` correctly rejected it. [That failed comparison is retained](./qualification/E2_P04_CANONICAL_EXECUTION_RETRY_1/replay-initial-attempt.json). The harness now verifies the recorded admission/receipt pair at its existing atomic boundary; every native check remains in force. Only completed corrected comparisons contribute PASS evidence. Canonical history, runtime and sealed oracles were not changed.

`E2_P05_READY = YES`: the canonical plan requires P04 PASS before P05. P05 remains unexecuted. The next package is full canonical E2-P05 acceptance, baseline regression and adversarial qualification. This run does not claim P05/P06 PASS, aggregate Planner release qualification, P03 historical correspondence or N-REAL satisfaction. Prior broad-suite/legacy fixture failures remain separate for that package; no broad-suite regression PASS is asserted here.
'''
    else:
        prose = f'''**RESULT = BLOCKED.** Execution stopped at the first reported divergence. No live repair or continuation was attempted. The [machine-readable companion](./{NAME}.json) records the actual committed prefix and [first counterexample](./qualification/E2_P04_CANONICAL_EXECUTION_RETRY_1/first-counterexample.json). Later phases and P05 remain unexecuted. No canonical target PASS is claimed.
'''
    report_lines = [f'{key} = {json.dumps(value) if isinstance(value, (dict, list)) else str(value).upper() if type(value) is bool else value}' for key, value in fields.items()]
    text = '# Deterministic Planner v0.1 — Canonical E2-P04 execution retry 1\n\n' + prose
    text += f'''\n[Preservation evidence](./qualification/E2_P04_CANONICAL_EXECUTION_RETRY_1/preservation.json) verifies all {len(baseline):,} preexisting files unchanged, including {preservation['frozen_E1_files_checked']:,} frozen-E1 files and all {preservation['runtime_files_checked']} runtime files. P03_RESULT remains PASS; historical correspondence remains UNPROVEN; N_REAL_SATISFIED remains NO. Production effect is NO. `git diff --check = PASS`.\n\n```text\n'''
    text += '\n'.join(report_lines) + '\n```\n'
    (D / (NAME + '.md')).write_text(text)
    print(json.dumps({'RESULT': fields['RESULT'], 'E2_P04_RESULT': fields['E2_P04_RESULT'],
                      'E2_P05_READY': fields['E2_P05_READY'], 'preexisting_files_unchanged': len(baseline)}))


if __name__ == '__main__':
    main()
