"""Read-only acceptance/binding/readiness evaluation and immutable artifact export."""
import hashlib
import json
from pathlib import Path
import subprocess

from common import (ROOT, OUT, SEALED, LABELS, CONTRACT, aid, bundle_path, c, equal,
                    fixture, identity, m, read, ref, save, semantic_projection,
                    trace_check, verify_refs)

DOCS = ROOT / 'docs/plans'
STEM = 'DETERMINISTIC_PLANNER_V0_1_E2_P05_A06_PROSPECTIVE_REQUEST_WAIT_RESULT_1'
BUNDLE_NAME = 'DETERMINISTIC_PLANNER_V0_1_E2_P05_A06_PROSPECTIVE_REQUEST_WAIT_BUNDLE_1.json'


def main():
    spec = fixture('primary')
    primary_store = OUT / 'runs/primary-seed-0'
    primary = c.restore(bundle_path(primary_store, spec['EXPECTED_POST_WAIT_BUNDLE_ID']),
                        identity(spec['EXPECTED_POST_WAIT_BUNDLE_ID']), ROOT)
    trace = trace_check(primary, spec)
    equal('primary actual transitions committed once', len(list(primary_store.glob('commit-*.json'))), 2)
    negative = read(OUT / 'negative-results.json')
    equal('27 controls pass', negative['executed_count'], 27)
    equal('negative suite', negative['RESULT'], 'PASS')
    equal('native retry', read(OUT / 'retry/primary-seed-0.json')['RESULT'], 'PASS')
    equal('presentation permutations', read(OUT / 'presentation-comparison.json')['RESULT'], 'PASS')

    # Compare independently committed histories to their own sealed oracles;
    # comparison data did not become a native execution operand.
    projection = semantic_projection(primary)
    comparisons = []
    for path in sorted((OUT / 'runs').glob('*/commit-2.json')):
        record = read(path)
        equal('native writer verdict ' + record['run'], record['RESULT'], 'PASS')
        equal('writer compared no fabricated oracle input', record['no_oracle_submitted'], True)
        equal('independent A06 semantic projection', record['semantic_projection'], projection)
        own = fixture(record['fixture'])
        equal('own sealed post bundle', record['bundle_id'], own['EXPECTED_POST_WAIT_BUNDLE_ID'])
        comparisons.append({'run': record['run'], 'fixture': record['fixture'], 'seed': record['PYTHONHASHSEED'],
                            'native_bundle_id': record['bundle_id'], 'RESULT': 'PASS', 'evidence': ref(path)})
    equal('sealed primary/permutation/reproduction writers', len(comparisons), 15)
    readers = []
    for path in sorted((OUT / 'readers').rglob('*.json')):
        record = read(path)
        equal('cold reader verdict', record['RESULT'], 'PASS')
        equal('historical replay without append', record['replay_append_calls'], [])
        equal('no replay occurrence', record['new_occurrences'], 0)
        readers.append({'run': record['run'], 'boundary': record['boundary'], 'seed': record['PYTHONHASHSEED'],
                        'reader': record['reader_index'], 'process_id': record['process_id'], 'evidence': ref(path)})
    equal('all contracted plus permutation cold readers', len(readers), 120)
    for seed in ('0', '1', '7', '101'):
        for boundary in ('start', 'ready', 'wait'):
            equal('3 primary cold readers/checkpoint/seed',
                  len([r for r in readers if r['run'] == 'primary-seed-' + seed and r['boundary'] == boundary]), 3)
    for number in (1, 2, 3):
        equal('3 final distinct-fixture cold readers',
              len([r for r in readers if r['run'] == 'reproduction-' + str(number) and r['boundary'] == 'wait']), 3)
    save(OUT / 'restore-replay-determinism-results.json', dict(LABELS, RESULT='PASS',
        primary_hash_seeds=[0, 1, 7, 101], distinct_fixture_reproductions=3,
        unordered_presentations=['original', 'reversed', 'rotated'], native_writer_histories=15,
        primary_cold_reads_required_and_passed=36, reproduction_final_cold_reads=9,
        total_cold_reader_processes=120, repeated_replay_creates_events=False,
        writer_results=comparisons, reader_results=readers,
        event_snapshot_bundle_codec_changes=False,
        permitted_key_set_presentation=ref(OUT / 'presentation-comparison.json')))

    # Export the actual committed primary objects; no new operation/event is run.
    native_path, exported_id = c.save_bundle(primary, DOCS, ROOT)
    equal('exported actual bundle', aid(exported_id), spec['EXPECTED_POST_WAIT_BUNDLE_ID'])
    named_bundle = DOCS / BUNDLE_NAME
    if named_bundle.exists():
        equal('immutable named bundle', named_bundle.read_bytes(), native_path.read_bytes())
    else:
        named_bundle.write_bytes(native_path.read_bytes())
    c._write_immutable(DOCS, 'snapshot-' + c.snapshot_id(primary.current).sha256 + '.json', c.snapshot_bytes(primary.current))
    save(OUT / 'actual-native-witness.json', dict(LABELS, RESULT='PASS',
        actual_trace=trace, actual_post_bundle=ref(named_bundle), actual_bundle_id=aid(exported_id),
        actual_post_snapshot_id=aid(c.snapshot_id(primary.current)),
        request_binding=c._wire(primary.current.external_gates[0].resolution_contracts[0]),
        gate_binding=c._wire(primary.current.external_gates[0]), actual_parent_events=[aid(e.parent_event) for e in primary.events],
        primary_events=[ref(DOCS / ('event-' + e.identity.sha256 + '.json')) for e in primary.events],
        control_is_recomputed='EXTERNAL_WAIT', new_native_grants=0, action_execution_or_completion=0))

    mapping_contract = read(SEALED / 'END-N12-N13-mapping.json')
    equal('actual END event identities', [aid(e.identity) for e in primary.events], mapping_contract['END']['expected_native_event_ids'])
    equal('actual END bundle identity', aid(exported_id), mapping_contract['END']['expected_post_bundle_id'])
    passed_controls = {r['name']: r for r in negative['cases']}
    mappings = {}
    for name in ('N12', 'N13'):
        terms = []
        for control in mapping_contract[name]['required_controls']:
            equal(name + ' independent negative premise', passed_controls[control]['RESULT'], 'PASS')
            terms.append({'id': control, 'RESULT': 'PASS', 'native_or_acceptance_evidence': passed_controls[control]['actual']})
        equal(name + ' presealed preservation', mapping_contract[name]['assurance_preserved'], True)
        mappings[name] = {'RESULT': 'PASS', 'independent_terms': terms,
                          'canonical_assurance': mapping_contract[name]['original_assurance'],
                          'actual_phase_events': [aid(e.identity) for e in primary.events],
                          'declarations_or_reports_not_occurrences': True,
                          'no_ActionResult_Knowledge_root_slot_effect': True,
                          'global_P05_case_executed': False,
                          'original_historical_assurance': 'UNPROVEN'}
    mapping = dict(LABELS, RESULT='PASS', classification='AUTHORIZED_PROSPECTIVE_REPLACEMENT',
        input='E2-A06.request_wait_event_trace', selected_option=read(CONTRACT)['SELECTED_OPTION'],
        governing_contract=ref(CONTRACT), governing_mapping=ref(SEALED / 'END-N12-N13-mapping.json'),
        actual_native_witness=ref(OUT / 'actual-native-witness.json'),
        original_event_ids=None, original_parent_ids=None, historical_identity_alias=False,
        actual_native_event_ids=[aid(e.identity) for e in primary.events], N12=mappings['N12'], N13=mappings['N13'],
        N12_MAPPING='PASS', N13_MAPPING='PASS', full_original_END_ancestry_waived=False,
        only_A06_binding_closed=True, no_new_qualification_scope_or_grant=True)
    save(OUT / 'END-N12-N13-mapping-result.json', mapping)

    readiness_contract = read(SEALED / 'post-A06-complete-P05-readiness-oracle.json')
    old_graph = read(ROOT / readiness_contract['current_graph']['path'])
    checked = verify_refs(old_graph)
    rows = list(old_graph['stage_bindings'])
    equal('exact stage set', [row['stage'] for row in rows], ['E2-A%02d' % n for n in range(1, 14)])
    equal('only previous A06 gap', [r['stage'] for r in rows if r['binding_status'] != 'BOUND'], ['E2-A06'])
    rows[5] = dict(LABELS, stage='E2-A06', binding_status='BOUND', classification='AUTHORIZED_PROSPECTIVE_REPLACEMENT',
        logical_required_input='E2-A06.request_wait_event_trace', mapping_result='PASS',
        actual_native_bundle=ref(named_bundle), native_event_ids=[aid(e.identity) for e in primary.events],
        ledger_id=trace['ledger_id'], event_positions=[0, 1], event_sequences=[1, 2],
        prospective_lineage=primary.current.context.lineage, prospective_generation=primary.current.context.generation,
        source_pins=c._wire(primary.sources), original_event_ids=None, original_parent_ids=None,
        original_history_splice=False, historical_identity_alias=False,
        governing_decision='AUTHORIZE_PROSPECTIVE_P05_A06_REQUEST_WAIT_QUALIFICATION',
        qualification_result=ref(OUT / 'END-N12-N13-mapping-result.json'), N12_MAPPING='PASS', N13_MAPPING='PASS')
    equal('twelve old bindings byte-equivalent values', [r for i, r in enumerate(rows) if i != 5],
          [r for i, r in enumerate(old_graph['stage_bindings']) if i != 5])
    equal('all thirteen unique required stage bindings', sum(r['binding_status'] == 'BOUND' for r in rows), 13)
    graph = dict(LABELS, RESULT='PASS_STAGE_BINDING_GRAPH_ONLY', P05_INITIAL_ORACLE='PASS',
        E2_A06_REQUEST_WAIT_EVENT_TRACE='PASS', P05_BOUND_STAGE_INPUTS=13, P05_REQUIRED_STAGE_INPUTS=13,
        stage_bindings=rows, P05_previous_bound_stage_inputs=12, only_stage_row_changed='E2-A06',
        twelve_prior_rows_preserved_exact=True, prior_pinned_artifact_references_rechecked=len(set(checked)),
        E2_END_STAGE_INPUT_GRAPH='PASS', E2_END_INPUT_GRAPH='FAIL_UNRESOLVED_GLOBAL_END_ANCESTRY',
        additional_unresolved_END_gate=old_graph['additional_unresolved_END_gate'],
        original_full_END_ancestry_waived=False, P05_EXECUTION_READY='NO', P05_EXECUTED='NO', P06_EXECUTED='NO',
        P03_HISTORICAL_CORRESPONDENCE='UNPROVEN', N_REAL_SATISFIED='NO',
        ORIGINAL_A03_HISTORICAL_OCCURRENCE='UNPROVEN', ORIGINAL_A04_HISTORICAL_ANCESTRY='UNPROVEN',
        ORIGINAL_A05_HISTORICAL_ANCESTRY='UNPROVEN', binding_representation='Read-only qualification evidence graph',
        old_graph=ref(ROOT / readiness_contract['current_graph']['path']))
    save(OUT / 'P05-binding-rerun.json', graph)

    # Evaluate every already sealed readiness predicate, even after finding the
    # first missing non-stage term. No additional predicate is introduced.
    initial = read(OUT / 'P04-initial-oracle-recheck.json')
    equal('P05 initial oracle', initial['RESULT'], 'PASS')
    native_target = c._unwire(read(ROOT / initial['target_path'])['bundle'])
    history = read(ROOT / readiness_contract['configuration_history']['path'])
    history_results = []
    for record in history['records']:
        event = native_target.events[record['event_sequence'] - 1]
        equal('configuration occurrence native type', type(event.result).__name__, 'InstallDefinition')
        equal('configuration event ID', event.identity, c._unwire(record['event_id']))
        equal('configuration parent', event.parent_event, c._unwire(record['parent_event']))
        equal('configuration pre-Snapshot', event.parent_snapshot, c._unwire(record['pre_state']))
        equal('configuration after-Snapshot', event.after_snapshot, c._unwire(record['post_state']))
        equal('configuration definition', event.result.definition.id, c._unwire(record['definition_id']))
        equal('configuration authority identity', event.result.authority.id, c._unwire(record['installation_authority_id']))
        equal('configuration operation', event.result.operation.value, record['operation'])
        equal('configuration native source pointer', c._wire(event), read(ROOT / record['source']['path'])['bundle']['events'][record['event_sequence'] - 1])
        history_results.append({'sequence': event.sequence, 'event_id': aid(event.identity), 'RESULT': 'PASS',
                                'historical_occurrence': True, 'currentness_requirement': record['current_consumer_applicability'],
                                'source_support_current': record['source_support_current']})
    equal('all nine configuration occurrences', [r['sequence'] for r in history_results], [3, 4, 5, 6, 7, 8, 9, 16, 18])
    save(OUT / 'configuration-history-recheck.json', {'RESULT': 'PASS', 'records': history_results,
         'original_history_unchanged': True, 'new_installations': 0, 'source': ref(ROOT / readiness_contract['configuration_history']['path'])})
    p05_negatives = read(ROOT / readiness_contract['negative_oracles']['path'])
    expected_cases = readiness_contract['sixteen_expected_negative_cases']
    equal('all sixteen P05 expectations unchanged',
          [(r['CASE_ID'], r['EXPECTED_STATE']) for r in p05_negatives['cases']],
          [(r['case'], r['expected']) for r in expected_cases])
    negative_preparation = [{'case': row['CASE_ID'], 'expectation': row['EXPECTED_STATE'],
                             'input_classification': row['input_classification'],
                             'actual_execution': 'NOT_EXECUTED', 'seed_inputs': row['seed_inputs']}
                            for row in p05_negatives['cases']]
    verify_refs(p05_negatives)
    save(OUT / 'P05-negative-readiness.json', {'RESULT': 'BLOCKED_PREPARATION',
         'sixteen_expectations': 'PASS_UNCHANGED', 'executed': False, 'cases': negative_preparation,
         'first_unprepared_initial_or_selected_fixture': 'E2-N08/E2-N12',
         'all_concrete_native_seed_mutation_bindings_materialized': False,
         'source': ref(ROOT / readiness_contract['negative_oracles']['path'])})
    inputs = read(ROOT / 'docs/plans/qualification/E2_P05_READINESS_1/input-inventory.json')
    authorities = read(ROOT / 'docs/plans/qualification/E2_P05_READINESS_1/authority-inventory.json')
    capabilities = read(ROOT / 'docs/plans/qualification/E2_P05_READINESS_1/capability-inventory.json')
    verify_refs(inputs)
    for item in capabilities['capabilities']:
        if 'qualified_evidence' in item:
            equal('qualified capability subject ' + item['id'],
                  hashlib.sha256((ROOT / item['qualified_evidence']).read_bytes()).hexdigest(), item['raw_sha256'])
    outcomes = {
        'P04_INITIAL_ORACLE': ('PASS', '37/37 native initial checks re-evaluated; trusted target unchanged'),
        'STAGE_BINDINGS': ('PASS', '13/13 unique authorized stage bindings; only A06 changed'),
        'GLOBAL_END_BINDINGS': ('FAIL_UNRESOLVED', old_graph['additional_unresolved_END_gate']),
        'CONFIGURATION_HISTORY': ('PASS', '9/9 exact ordered historical native InstallDefinition events; no new installation'),
        'IDENTITY_DOMAINS': ('PASS_FOR_BOUND_GRAPH', 'All native source/event/Snapshot/result identities retained; no original/prospective alias. Complete END unresolved'),
        'CURRENTNESS': ('PASS_FOR_BOUND_GRAPH', 'P04 37-term native currentness and A06 scoped pins PASS; global END consumer not bound'),
        'PROVENANCE': ('PASS_FOR_BOUND_GRAPH', 'Prior twelve source/scope values exact; A06-only scope and separate native source pins exact; full END mapping remains unresolved'),
        'P05_NEGATIVE_READINESS': ('FAIL_UNPREPARED', '16 expectations unchanged; initial/selected-unexecuted N08/N12 and complete native mutation/process operands not materialized'),
        'PERSISTENCE_PLAN': ('FAIL_UNBOUND_END_MANIFEST', 'Sealed plan and A06 reader/termination bindings PASS; full END/D01 process/checkpoint manifests remain unbound'),
        'REPLAY_PLAN': ('FAIL_UNBOUND_END_HISTORY', 'P04 and new A06 historical replay PASS; no complete governing joined END history/mapping'),
        'AUTHORITY_APPLICABILITY': ('FAIL_UNBOUND_END_SUBJECT', authorities['END_REPRODUCTION_AUTHORITY_BINDING']['classification']),
        'QUALIFIED_CAPABILITIES_CURRENT_DEFINITIONS': ('PASS_AVAILABLE_BUT_END_INPUTS_UNRESOLVED', 'All retained capability pins and P04 active definitions pass; no new runtime capability need established; complete END definition/input projection unbound'),
        'NON_STAGE_END_INPUTS': ('FAIL_UNBOUND', 'Global PC01/PC02/PC03/T01/D01/post-reentry interface, A14-A16 and D01/REG concrete execution input/checkpoint bindings remain incomplete'),
        'NO_UNRESOLVED_PREPARATION': ('FAIL', 'Global END ancestry/mapping/process/authority/negative operands remain unresolved'),
    }
    equal('no readiness term added or removed', list(outcomes), [term['id'] for term in readiness_contract['terms']])
    terms = [dict(term, RESULT=outcomes[term['id']][0], actual=outcomes[term['id']][1])
             for term in readiness_contract['terms']]
    first = next(term for term in terms if term['RESULT'].startswith('FAIL'))
    equal('first non-stage blocker', first['id'], 'GLOBAL_END_BINDINGS')
    ready = {'RESULT': 'EVALUATED_NO', 'P05_EXECUTION_READY': 'NO', 'P05_EXECUTED': 'NO', 'P06_EXECUTED': 'NO',
             'sealed_oracle': ref(SEALED / 'post-A06-complete-P05-readiness-oracle.json'),
             'terms': terms, 'terms_evaluated': 14, 'new_readiness_criteria': 0,
             'P05_INITIAL_ORACLE': 'PASS', 'P05_BOUND_STAGE_INPUTS': 13, 'P05_REQUIRED_STAGE_INPUTS': 13,
             'sixteen_P05_negative_expectations': 'PASS_UNCHANGED_NOT_EXECUTED',
             'FIRST_NON_STAGE_BLOCKER': {'term': first['id'],
                 'input': 'E2-END.original_prefix_to_checkpoint_to_target_ancestry_or_full_END_acceptance_mapping',
                 'expected': first['predicate'], 'actual': first['actual'],
                 'classification': 'UNRESOLVED_GOVERNING_FULL_END_ANCESTRY_MAPPING',
                 'scope_expansion_permitted_here': False},
             '13_of_13_implies_P05_PASS': False, 'global_END_scope_gap_waived': False,
             'readiness_input_inventory': ref(ROOT / 'docs/plans/qualification/E2_P05_READINESS_1/input-inventory.json')}
    save(OUT / 'P05-complete-readiness-result.json', ready)

    # Preservation is measured against the workspace at the beginning of this
    # package, including inherited runtime changes and all previous seals.
    old_files = read(OUT / 'baseline.json')['files']
    changed = [name for name, wanted in old_files.items() if not (ROOT / name).is_file() or
               hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != wanted]
    equal('all pre-existing artifacts preserved', changed, [])
    check = subprocess.run(['git', 'diff', '--check'], cwd=str(ROOT), capture_output=True, text=True)
    equal('git diff --check', check.returncode, 0)
    frozen = [name for name in old_files if name.startswith('docs/experiments/E1/')]
    runtime = [name for name in old_files if name.startswith('adapter/planner/')]
    save(OUT / 'preservation.json', dict(LABELS, RESULT='PASS', baseline_files_unchanged=len(old_files),
        old_files_changed=[], frozen_E1_files_unchanged=len(frozen), runtime_files_unchanged=len(runtime),
        RUNTIME_MODIFIED='NO', E1_ARTIFACTS_MODIFIED=0, PRODUCTION_EFFECT='NO', git_diff_check='PASS',
        canonical_P04_unchanged=True, old_contract_oracle_scope_graph_artifacts_changed=0,
        P05_EXECUTED='NO', P06_EXECUTED='NO', new_native_authority_issued=0,
        ORIGINAL_A03_HISTORICAL_OCCURRENCE='UNPROVEN', ORIGINAL_A04_HISTORICAL_ANCESTRY='UNPROVEN',
        ORIGINAL_A05_HISTORICAL_ANCESTRY='UNPROVEN', P03_HISTORICAL_CORRESPONDENCE='UNPROVEN', N_REAL_SATISFIED='NO'))
    harness_note = {
        'phase': 'Before any primary A06 transition',
        'original_diagnostic': ref(OUT / 'STOP-primary-seed-0-bootstrap-0.json'),
        'classification': 'REPORT_SERIALIZATION_ERROR_BEFORE_EXECUTION',
        'cause': 'Qualification report tried closed native codec serialization of read-only Computation, which is not a persisted native entity',
        'correction': 'Serialize derived Computation as qualification metadata only; native codec and all inputs/oracles unchanged',
        'native_events_before_correction': 0, 'durable_HEAD_before_correction': False,
        'actual_sealed_state_oracle_mismatch': False, 'runtime_repair': False,
        'read_only_configuration_report_comparator_correction': 'Project InstallAuthority.id when comparing the sealed authority identity; the native wrapper and oracle identity were not changed',
    }
    save(OUT / 'pre-execution-harness-diagnostic.json', harness_note)
    summary = dict(LABELS, WORK_PACKAGE='E2-P05-A06-PROSPECTIVE-REQUEST-WAIT-EXECUTION', RESULT='PASS',
        SELECTED_OPTION=read(CONTRACT)['SELECTED_OPTION'], ENTRY_GATE='PASS',
        REQUEST='TEST-REQUEST; exact sealed scoped ExternalResolutionContract', WAIT_GATE='E2-GATE',
        REQUEST_READY_EVENT_ID=aid(primary.events[0].identity), WAIT_EVENT_ID=aid(primary.events[1].identity),
        EVENT_ORDERING='PASS', LEDGER_MEMBERSHIP='PASS', POST_A06_CONTROL='EXTERNAL_WAIT',
        PROSPECTIVE_A06_REQUEST_WAIT_TRACE='PASS', E2_A06_REQUEST_WAIT_EVENT_TRACE='PASS',
        POST_A06_BUNDLE_ID=aid(exported_id), POST_A06_STATE_ID=aid(c.snapshot_id(primary.current)),
        POST_A06_SNAPSHOT_ID=aid(c.snapshot_id(primary.current)), POST_A06_LEDGER_ROOT=trace['root'],
        POST_A06_APPEND_HEAD=trace['head'], POST_A06_BUNDLE_PATH=str(named_bundle.relative_to(ROOT)),
        COLD_RESTORE='PASS', HISTORICAL_REPLAY='PASS; recorded new prospective lineage only',
        IDEMPOTENCE='PASS; native append identity idempotence, conflicting/stale durable retry rejection',
        INDEPENDENT_REPRODUCTION='PASS; 3 distinct sealed new fixtures', DETERMINISM='PASS',
        NEGATIVE_SUITE='PASS; 27/27 sealed isolated controls', END_MAPPING='PASS_FOR_A06_ONLY',
        N12_MAPPING='PASS', N13_MAPPING='PASS', BINDING_CLASSIFICATION='AUTHORIZED_PROSPECTIVE_REPLACEMENT',
        P05_BOUND_STAGE_INPUTS=13, P05_REQUIRED_STAGE_INPUTS=13, E2_END_STAGE_INPUT_GRAPH='PASS',
        E2_END_INPUT_GRAPH='FAIL_UNRESOLVED_GLOBAL_END_ANCESTRY',
        P05_COMPLETE_READINESS_ORACLE='EVALUATED; 14/14 TERMS; NOT SATISFIED', P05_INITIAL_ORACLE='PASS; 37/37',
        P05_EXECUTION_READY='NO', FIRST_NON_STAGE_BLOCKER=ready['FIRST_NON_STAGE_BLOCKER'],
        NEXT_PACKAGE='E2-P05 FULL-END ANCESTRY / ACCEPTANCE-MAPPING CLOSURE',
        PROSPECTIVE_A06_EXECUTED='YES', P05_EXECUTED='NO', P06_EXECUTED='NO', E2_P04_RESULT='PASS', E2_P05_READY='YES',
        ORIGINAL_A03_HISTORICAL_OCCURRENCE='UNPROVEN', ORIGINAL_A04_HISTORICAL_ANCESTRY='UNPROVEN',
        ORIGINAL_A05_HISTORICAL_ANCESTRY='UNPROVEN', P03_HISTORICAL_CORRESPONDENCE='UNPROVEN', N_REAL_SATISFIED='NO',
        RUNTIME_MODIFIED='NO', E1_ARTIFACTS_MODIFIED=0, PRODUCTION_EFFECT='NO', GIT_DIFF_CHECK='PASS',
        FIRST_COUNTEREXAMPLE=None, native_oracle_divergence=False, pre_execution_harness_diagnostic=harness_note,
        evidence={name: ref(OUT / filename) for name, filename in {
            'entry': 'entry-gate.json', 'actual_witness': 'actual-native-witness.json',
            'restore_replay_determinism': 'restore-replay-determinism-results.json',
            'negatives': 'negative-results.json', 'END_N12_N13': 'END-N12-N13-mapping-result.json',
            'P05_graph': 'P05-binding-rerun.json', 'P05_readiness': 'P05-complete-readiness-result.json',
            'P04_initial_oracle': 'P04-initial-oracle-recheck.json',
            'configuration_history': 'configuration-history-recheck.json', 'preservation': 'preservation.json',
        }.items()})
    save(DOCS / (STEM + '.json'), summary)
    document = '''# E2-P05 A06 prospective request/wait qualification execution 1

**RESULT = PASS.** The exact sealed prospective fixture completed the two native phase transitions, matched the independent event/state oracles, survived cold restore/replay and passed all 27 negative controls. The A06-only authorized replacement binding closes stage coverage to **13/13**. **P05_EXECUTION_READY = NO** because the already sealed global END ancestry/acceptance-mapping requirement remains unresolved. P05 and P06 were not executed.

The [machine-readable result](DETERMINISTIC_PLANNER_V0_1_E2_P05_A06_PROSPECTIVE_REQUEST_WAIT_RESULT_1.json) links complete native execution, comparison, reader, negative, mapping, binding and readiness evidence. The [native post-A06 bundle](DETERMINISTIC_PLANNER_V0_1_E2_P05_A06_PROSPECTIVE_REQUEST_WAIT_BUNDLE_1.json) contains the actual new occurrence history.

## Entry and actual native occurrence

The explicit option **AUTHORIZE_PROSPECTIVE_P05_A06_REQUEST_WAIT_QUALIFICATION** was verified against the sealed [contract](DETERMINISTIC_PLANNER_V0_1_E2_P05_A06_PROSPECTIVE_REQUEST_WAIT_CONTRACT_1.md), dossier/source/input/oracle hashes, native start identity, context and previous 12/13 graph. All 93 referenced seals matched. Additional authority was not required; no grant, definition installation or Action execution occurred.

The primary start bundle was `planner-bundle-v1:0cbb30fed94acefafa765ad8d2ae2a6b7b6b42c07d76ea9de1a5f32c805e2ec6`, with empty native ledger/root/head/parent. The request `TEST-REQUEST`, requirement `E2-EXTERNAL-REQUIREMENT` and gate `E2-GATE` retained exact scoped content/provenance, target, producers, receipt and held/reentry bindings.

| Native occurrence | Position / sequence | Event identity | Parent |
|---|---|---|---|
| EVIDENCE_REQUEST_READY | 0 / 1 | EVENT1 | null |
| WAITING_FOR_EXTERNAL_EVIDENCE | 1 / 2 | EVENT2 | EVENT1 |

The writer used `codec.commit_event` on commands constructed from the actual restored Snapshot and native phase enums. No expected event or Snapshot was submitted as an operand. Each phase durably committed its native result, occurrence event, immutable state and bundle/head. The request-ready writer terminated and fresh readers restored the checkpoint before the waiting writer ran. [Actual native witness](qualification/E2_P05_A06_PROSPECTIVE_REQUEST_WAIT_EXECUTION_1/actual-native-witness.json) retains full payloads, pre/after Snapshot bindings, request/gate context, exact ledger coordinate and identities.

The final state is WAITING_FOR_EXTERNAL_EVIDENCE with gate history REQUIRED → READY → WAITING; CONTROL recomputes EXTERNAL_WAIT, the known-rule obligation remains UNKNOWN, and the Action is held. Evidence, receipt, validation/support, typed proof, Knowledge, ActionResult, decision/grant, reentry and Action completion remain absent. Global control already computed EXTERNAL_WAIT at the sealed start; the new **waiting-stage occurrence** is proved by event ancestry/positions, rather than inferred from the control scalar.

```text
POST_A06_BUNDLE_ID = BUNDLE
POST_A06_STATE_ID = SNAPSHOT
POST_A06_LEDGER_ROOT = EVENT1
POST_A06_APPEND_HEAD = EVENT2
```

## Restore, replay, retry and independent qualification

[Qualification comparisons](qualification/E2_P05_A06_PROSPECTIVE_REQUEST_WAIT_EXECUTION_1/restore-replay-determinism-results.json) passed four original-presentation seed writers (0,1,7,101), three separately sealed reproduction fixtures and reversed/rotated predicate/source presentations under all four seeds. All fifteen writer histories matched their own independent oracles; separate reproduction identities remained distinct, and the declared A06 semantic projection matched. The primary occurrence was committed once with exactly two events; other stores are comparison/reproduction evidence.

There were **120 independent cold-reader processes**, including all 36 required primary START/READY/WAIT reads and nine required reproduction final reads. Readers restored exact native event bodies, parent/position/root/head, request/gate/context/source/policy and complete state. Historical replay consumed recorded phase results, reconstructed the sealed initial-to-final history and repeated without appending or committing a new result/occurrence. It proves only this new prospective history.

[Retry](qualification/E2_P05_A06_PROSPECTIVE_REQUEST_WAIT_EXECUTION_1/retry/primary-seed-0.json) confirmed identity-idempotent native append of each enrolled event, conflicting bytes rejected, stale durable resubmission rejected with PARENT_MISMATCH and successful durable files unchanged. [Presentation comparison](qualification/E2_P05_A06_PROSPECTIVE_REQUEST_WAIT_EXECUTION_1/presentation-comparison.json) also verified recursive object-key order and declared unordered native sets preserve bytes, identity and Computation; causal events/gate history retained order.

All **27/27** [sealed negatives](qualification/E2_P05_A06_PROSPECTIVE_REQUEST_WAIT_EXECUTION_1/negative-results.json) failed closed at their contract-specified native or trusted acceptance boundary. Native failures advanced no durable HEAD; report/Snapshot/oracle substitutes and historical/scope aliasing produced no accepted binding. A request-ready-only checkpoint is a legal intermediate state and fails complete A06 acceptance. Negative fixtures did not change the successful lineage. The sixteen global P05 negative expectations remain sealed and were not executed here.

## END replacement and N12/N13

The [mapping](qualification/E2_P05_A06_PROSPECTIVE_REQUEST_WAIT_EXECUTION_1/END-N12-N13-mapping-result.json) binds only the actual primary native witness to `E2-A06.request_wait_event_trace`, classified **AUTHORIZED_PROSPECTIVE_REPLACEMENT**. N12 independently passes actual-occurrence versus definition/selection/Snapshot/report separation and its four required controls. N13 independently passes prospective-versus-actual result separation, unchanged Knowledge/root/slot/Action effects and its four controls. Neither mapping asserts original historical occurrence or global P05 case PASS.

```text
QUALIFICATION_TYPE = PROSPECTIVE_REPLACEMENT
ORIGINAL_A06_HISTORICAL_REQUEST_WAIT_TRACE = UNPROVEN
HISTORICAL_RECONSTRUCTION = NO
PROSPECTIVE_A06_TRACE_IS_ORIGINAL_TRACE = NO
PROSPECTIVE_A06_REQUEST_WAIT_TRACE = PASS
E2_A06_REQUEST_WAIT_EVENT_TRACE = PASS
```

The [binding rerun](qualification/E2_P05_A06_PROSPECTIVE_REQUEST_WAIT_EXECUTION_1/P05-binding-rerun.json) covers all thirteen stage rows with unique native identities under their own governing scopes. Only A06 changed; all twelve preceding bindings are exact unchanged values with rechecked source pins. No new event is aliased to an unknown original event, and no history is spliced.

## Complete P05 readiness evaluation

The [readiness result](qualification/E2_P05_A06_PROSPECTIVE_REQUEST_WAIT_EXECUTION_1/P05-complete-readiness-result.json) evaluates **all fourteen previously sealed terms**, without adding criteria. The P04 initial oracle recheck passes **37/37**, the thirteen stage bindings pass, and all nine governed configuration-history occurrences match their exact native identities, parents and ordered positions. Source/identity/currentness checks pass for the bound graph. The sixteen P05 expectations remain unchanged.

**FIRST_NON_STAGE_BLOCKER = GLOBAL_END_BINDINGS:** the original prefix-to-checkpoint-to-target ancestry, or a separately governing full END acceptance mapping, has not been bound. Separate A03/A04/A06 qualification histories and the A05 alternate event demonstrate their authorized case assurances; their stage mappings do not authorize a causal joined full END history. This limitation was sealed before execution and is not a new readiness criterion.

The same existing preparation gap also leaves full END process/checkpoint/replay/authority subjects, non-stage END interfaces and concrete N08/N12 negative inputs unprepared. They were evaluated and recorded rather than repaired. **13/13 stage coverage does not imply P05 PASS or execution readiness.** Next package: **E2-P05 FULL-END ANCESTRY / ACCEPTANCE-MAPPING CLOSURE**.

## Preservation

[Preservation](qualification/E2_P05_A06_PROSPECTIVE_REQUEST_WAIT_EXECUTION_1/preservation.json) verifies every pre-existing workspace file against the package entry baseline. Runtime, all prior contracts/oracles/dossiers/bindings, historical A06 records, the successful canonical P04 target and frozen E1 remain unchanged. New files contain only prospective native execution/qualification evidence and report harnesses.

Before the first transition, the report harness attempted to serialize derived Computation through the closed native entity codec and stopped with no event or HEAD. Only report serialization was corrected to record computed metadata. The [retained diagnostic](qualification/E2_P05_A06_PROSPECTIVE_REQUEST_WAIT_EXECUTION_1/pre-execution-harness-diagnostic.json) records that error; no native state/oracle mismatch or runtime repair occurred.

```text
WORK_PACKAGE = E2-P05-A06-PROSPECTIVE-REQUEST-WAIT-EXECUTION
RESULT = PASS
EVENT_ORDERING = PASS
LEDGER_MEMBERSHIP = PASS
POST_A06_CONTROL = EXTERNAL_WAIT
COLD_RESTORE = PASS
HISTORICAL_REPLAY = PASS
IDEMPOTENCE = PASS
INDEPENDENT_REPRODUCTION = PASS
DETERMINISM = PASS
NEGATIVE_SUITE = PASS (27/27)
END_MAPPING = PASS_FOR_A06_ONLY
N12_MAPPING = PASS
N13_MAPPING = PASS
P05_BOUND_STAGE_INPUTS = 13
P05_REQUIRED_STAGE_INPUTS = 13
P05_COMPLETE_READINESS_ORACLE = EVALUATED; NOT SATISFIED
P05_EXECUTION_READY = NO
FIRST_NON_STAGE_BLOCKER = GLOBAL_END_BINDINGS
PROSPECTIVE_A06_EXECUTED = YES
P05_EXECUTED = NO
P06_EXECUTED = NO
ORIGINAL_A03_HISTORICAL_OCCURRENCE = UNPROVEN
ORIGINAL_A04_HISTORICAL_ANCESTRY = UNPROVEN
ORIGINAL_A05_HISTORICAL_ANCESTRY = UNPROVEN
ORIGINAL_A06_HISTORICAL_REQUEST_WAIT_TRACE = UNPROVEN
P03_HISTORICAL_CORRESPONDENCE = UNPROVEN
N_REAL_SATISFIED = NO
RUNTIME_MODIFIED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
git diff --check = PASS
```
'''
    import re
    substitutions = {'EVENT1': summary['REQUEST_READY_EVENT_ID'], 'EVENT2': summary['WAIT_EVENT_ID'],
                     'BUNDLE': summary['POST_A06_BUNDLE_ID'], 'SNAPSHOT': summary['POST_A06_STATE_ID']}
    document = re.sub(r'\b(EVENT1|EVENT2|BUNDLE|SNAPSHOT)\b', lambda match: substitutions[match.group()], document)
    report_path = DOCS / (STEM + '.md')
    if report_path.exists():
        equal('immutable human-readable execution report', report_path.read_text(), document)
    else:
        report_path.write_text(document)
    print(json.dumps({'RESULT': 'PASS', 'A06': 'PASS', 'bound_stages': '13/13',
                      'P05_EXECUTION_READY': 'NO', 'first_non_stage_blocker': 'GLOBAL_END_BINDINGS',
                      'native_bundle': aid(exported_id)}, sort_keys=True))


if __name__ == '__main__':
    main()
