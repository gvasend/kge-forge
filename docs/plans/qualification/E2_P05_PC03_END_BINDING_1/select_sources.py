"""Select existing PC03 oracle/operand/process records; never run producers."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
DOCS = ROOT / 'docs/plans'
Q = DOCS / 'qualification'
PREFIX = 'DETERMINISTIC_PLANNER_V0_1_'


def read(path):
    return json.loads(Path(path).read_bytes())


def ref(path, pointer=''):
    path = Path(path)
    return {'path': str(path.relative_to(ROOT)), 'pointer': pointer,
        'raw_sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def save(name, value):
    raw = (json.dumps(value, sort_keys=True, indent=2) + '\n').encode()
    path = OUT / name
    if path.exists():
        assert path.read_bytes() == raw, name
    else:
        path.write_bytes(raw)


def identity(value):
    return value['namespace'] + ':' + value['sha256']


def main():
    baseline = read(OUT / 'baseline.json')['file_sha256']
    contract = read(Q / 'E2_P05_END_INTERFACE_CLOSURE_1/six-interface-inventory.json')['interfaces'][2]
    graph_path = Q / 'E2_P05_END_ANCESTRY_RECONCILIATION_1/qualified-evidence-graph.json'
    graph = read(graph_path)['graph']
    graph_ref = ref(graph_path)
    assert contract['INTERFACE_ID'] == 'E2-END#/dependencies/2'
    for pin in contract['PROVENANCE']:
        assert pin['raw_sha256'] == baseline[pin['path']] == ref(ROOT / pin['path'])['raw_sha256']
    models = []
    native = read(Q / 'E2_P05_END_INTERFACE_CLOSURE_1/minimum-PC01-closure-contract.json')['source']['included_native_original_model']
    assert native['raw_sha256'] == baseline[native['path']]
    models.append({'model_id': 'ORIGINAL_INITIAL_MODEL', 'source': native, 'type': 'Snapshot',
        'native_snapshot': 'planner-snapshot-v1:545ad19184d8dd7dfb5b2737e081b043d13982f05d05326939ac2cbb89bf54e2',
        'context': {'$type': 'EvaluationContext', 'scope': 'E2-QUALIFICATION-ONLY', 'lineage': 'E2-CANONICAL-BASELINE-1',
            'generation': 'E2-GENERATION-1', 'tick': 0, 'allowed_effects': []},
        'binding_classification': 'CANONICAL_CONFIGURATION', 'state_role': 'Historical qualified definition/selection model for A01/A02',
        'semantic_oracle': dict(graph_ref, pointer='/graph/stage_nodes/0/canonical_oracle'),
        'oracle_role': 'Existing canonical A01 input/independent definition comparison; not producer output',
        'physical_source_currentness': 'HISTORICAL_EMBEDDED_PROVENANCE_ONLY',
        'native_occurrence_not_asserted': True})
    for name in ('A03', 'A04', 'A06', 'P03'):
        segment = graph['native_ledger_segments'][name]
        contract_path = DOCS / (PREFIX + {
            'A03': 'E2_P05_A03_PROSPECTIVE_OCCURRENCE_CONTRACT_1',
            'A04': 'E2_P05_A04_PROSPECTIVE_ANCESTRY_CONTRACT_1',
            'A06': 'E2_P05_A06_PROSPECTIVE_REQUEST_WAIT_CONTRACT_1',
            'P03': 'P03_PROSPECTIVE_CHECKPOINT_QUALIFICATION_1'}[name] + '.json')
        if name == 'A03':
            oracle = read(contract_path)['EXPECTED_RESULT_ORACLE']
        elif name == 'A04':
            # The prior representation/durable overlays supply the typed outcomes;
            # the sealed expected result/state remains the same source contract.
            oracle = ref(Q / 'E2_P05_A04_PROSPECTIVE_ANCESTRY_CONTRACT_1/oracles/expected-result-and-state.json')
        elif name == 'A06':
            oracle = read(contract_path)['POST_TRACE_ORACLE']
        else:
            oracle = ref(Q / 'P03_PROSPECTIVE_CHECKPOINT_1/mainline-oracle.json')
        models.append({'model_id': name + '_QUALIFIED_POST_STATE', 'source': segment['source'], 'type': 'PersistenceBundle',
            'native_bundle': segment['bundle_id'], 'native_snapshot': segment['current_snapshot'],
            'context': segment['context'], 'event_root': segment['root'], 'event_head': segment['head'],
            'binding_classification': 'AUTHORIZED_REPLACEMENT_QUALIFICATION' if name == 'P03' else 'AUTHORIZED_PROSPECTIVE_REPLACEMENT',
            'state_role': 'Already qualified native ' + name + ' phase/checkpoint; distinct historical scope preserved',
            'semantic_oracle': oracle, 'oracle_role': 'Already independently sealed local contract; no oracle chosen from current materializer output',
            'scope_contract': ref(contract_path), 'source_selection_authority': dict(graph_ref, pointer='/graph/native_ledger_segments/' + name),
            'physical_source_currentness': 'EXACT_QUALIFIED_SCOPE_NATIVE_PINS', 'historical_reconstruction': False})
    p04 = Q / 'E2_P04_CANONICAL_EXECUTION_RETRY_1'
    manifest_path = p04 / 'checkpoint-manifests.json'
    manifests = read(manifest_path)
    order = ['final-preexecution', 'installed-source-configuration', 'post-a09', 'post-a10', 'post-a11',
        'post-a12', 'slot-contract', 'post-slot-proof', 'root-contract', 'post-root-proof', 'isolated-p04-target']
    for name in order:
        fidelity_path = Q / ('FINISH_F03_1/reader-manifests/' + name + '.json')
        fidelity = read(fidelity_path)
        if name == 'final-preexecution':
            path = DOCS / (PREFIX + 'E2_P04_FINAL_PREEXECUTION_CONFIGURATION_BUNDLE_1.json')
        elif name == 'installed-source-configuration':
            path = p04 / 'checkpoints/installed-source-configuration/prefix.json'
        elif name == 'isolated-p04-target':
            path = DOCS / (PREFIX + 'E2_P04_CANONICAL_TARGET_BUNDLE_1.json')
        else:
            path = p04 / ('checkpoints/' + name + '/' + name + '.json')
        source = ref(path)
        assert source['raw_sha256'] == baseline[source['path']] == fidelity['bundle_id']['sha256'], name
        models.append({'model_id': 'P04_' + name.upper().replace('-', '_'), 'source': source, 'type': 'PersistenceBundle',
            'native_bundle': identity(fidelity['bundle_id']), 'native_snapshot': identity(fidelity['state_id']),
            'context': fidelity['semantic_oracle']['context'],
            'event_root': identity(fidelity['semantic_oracle']['ledger_root']), 'event_head': identity(fidelity['head']),
            'event_count': fidelity['event_count'], 'binding_classification': 'CANONICAL_EXECUTION' if name.startswith('post-') or name == 'isolated-p04-target' else 'CANONICAL_CONFIGURATION',
            'state_role': 'Actual retained canonical P04 ' + name + ' boundary; no replacement of native tail',
            'semantic_oracle': ref(fidelity_path, '/semantic_oracle'),
            'oracle_role': 'Previously sealed writer/reader fidelity comparator, not an independent lifecycle result oracle',
            'independent_lifecycle_oracles': ref(Q / 'FINISH_F02_1/boundary-oracles.json', '/oracles'),
            'canonical_checkpoint_manifest': ref(manifest_path, '/' + name) if name in manifests else ref(p04 / 'configuration-manifest.json'),
            'physical_source_currentness': 'EXACT_NATIVE_CHECKPOINT_PINS_AND_CONSUMER_ROLES',
            'later_installs_not_visible_to_earlier_checkpoint': True})
    comparisons = [
        {'oracle_name': name, 'native_model_id': 'P04_' + point.upper().replace('-', '_'),
         'independent_expected': ref(Q / 'FINISH_F02_1/boundary-oracles.json', '/oracles/' + name),
         'retained_qualification_comparison': ref(DOCS / (PREFIX + 'FINISH_F03_RESULT.json'), '/boundary_oracles/' + name)}
        for name, point in [('POST_A12_PRE_SUPPORT', 'post-a12'), ('POST_SUPPORT', 'slot-contract'),
            ('POST_SLOT_PROOF', 'post-slot-proof'), ('POST_ROOT_PROOF', 'post-root-proof'),
            ('POST_ROOT_SATISFACTION', 'post-root-proof'), ('PRE_FINISH', 'post-root-proof'),
            ('POST_FINISH', 'isolated-p04-target'), ('P04_TARGET', 'isolated-p04-target')]]
    family_specs = {
        'A03': {'contract': Q / 'E2_P05_A03_PROSPECTIVE_OCCURRENCE_CONTRACT_1/negative-contract.json',
            'result': Q / 'E2_P05_A03_PROSPECTIVE_OCCURRENCE_EXECUTION_1/negative-results.json',
            'driver': Q / 'E2_P05_A03_PROSPECTIVE_OCCURRENCE_EXECUTION_1/qualify.py'},
        'A04': {'contract': Q / 'E2_P05_A04_PROSPECTIVE_ANCESTRY_CONTRACT_1/negative-contract.json',
            'result': Q / 'E2_P05_A04_PROSPECTIVE_ANCESTRY_EXECUTION_1/A04-negative-results.json',
            'driver': Q / 'E2_P05_A04_PROSPECTIVE_ANCESTRY_EXECUTION_1/qualify.py'},
        'A06': {'contract': Q / 'E2_P05_A06_PROSPECTIVE_REQUEST_WAIT_CONTRACT_1/sealed-negative-oracles.json',
            'result': Q / 'E2_P05_A06_PROSPECTIVE_REQUEST_WAIT_EXECUTION_1/negative-results.json',
            'driver': Q / 'E2_P05_A06_PROSPECTIVE_REQUEST_WAIT_EXECUTION_1/qualify.py'},
        'P04_A13': {'contract': Q / 'FINISH_F02_1/negative-contract.json',
            'result': p04 / 'f02-negative-results.json', 'driver': ROOT / 'adapter/tests/qualify_finish_f03_checks.py'}}
    # Producer commands are retained provenance, never executable by this binding.
    # Resolve exact already-used driver filename from its result directory.
    for name, spec in family_specs.items():
        if not spec['driver'].is_file():
            possibilities = sorted(spec['result'].parent.glob('*.py'))
            # Record the complete retained driver set; no convenient replacement.
            spec['drivers'] = [ref(x) for x in possibilities]
        else:
            spec['drivers'] = [ref(spec['driver'])]
    mutations = [{'family': family, 'contract': ref(spec['contract']), 'retained_results': ref(spec['result']),
        'producer_code': spec['drivers'], 'native_operands':
            ['P04_ROOT_CONTRACT', 'P04_POST_A12', 'P04_POST_ROOT_PROOF', 'P04_ISOLATED_P04_TARGET'] if family == 'P04_A13' else [family + '_QUALIFIED_POST_STATE'],
        'scope': 'E2-QUALIFICATION-ONLY',
        'use': 'Exact retained mutation/rejection contract + qualified native preconditions + historical results; comparison-only, not a new mutation run'}
        for family, spec in family_specs.items()]
    process_evidence = []
    paths = [p04 / 'reader-plan.json', p04 / 'cold-reader-results.json', p04 / 'execution-trace.json',
        p04 / 'invalidation-results.json', p04 / 'unordered-permutations.json',
        Q / 'FINISH_F03_1/reader-plan.json', ROOT / 'adapter/tests/qualify_finish_f03_checks.py',
        Q / 'E2_P05_A03_PROSPECTIVE_OCCURRENCE_EXECUTION_1/cold-restore-and-replay.json',
        Q / 'E2_P05_A04_PROSPECTIVE_ANCESTRY_EXECUTION_1/process-qualification.json',
        Q / 'E2_P05_A06_PROSPECTIVE_REQUEST_WAIT_EXECUTION_1/restore-replay-determinism-results.json',
        DOCS / (PREFIX + 'P03_PROSPECTIVE_CHECKPOINT_QUALIFICATION_1.json')]
    for path in paths:
        process_evidence.append(ref(path))
    save('selected-source-collection.json', {'schema': 'PC03-END-SELECTED-SOURCE-COLLECTION-1',
        'contract': ref(Q / 'E2_P05_END_INTERFACE_CLOSURE_1/six-interface-inventory.json', '/interfaces/2'),
        'primary_sources': contract['PROVENANCE'], 'native_models': models,
        'independent_boundary_pairs': comparisons, 'mutation_families': mutations,
        'process_evidence': process_evidence, 'unchanged_stage_graph': graph_ref,
        'interpretation': 'Exact retained independent contracts and native checkpoint/phase operands are selected; producer runs and stage mappings remain unchanged',
        'current_POST_REENTRY_rule': 'Use the already-sealed F02/F03 PLAN_DEFECT post-A12 boundary, not the older PC03 RUNNABLE/FINISH scaffold',
        'original_PC03_template_still_retained': True,
        'expected_oracles_are_comparison_only': True, 'historical_reader_manifests_not_new_writer_invocations': True,
        'SOURCE_INSTANCE_ambiguity_resolution': 'Sixteen exact retained model roles, fixed native IDs/contexts and independently sourced comparison pairs; no unselected future candidate'})
    print(json.dumps({'SOURCE_SELECTION': 'SEALED', 'native_models': len(models),
        'boundary_pairs': len(comparisons), 'mutation_families': len(mutations)}))


if __name__ == '__main__':
    main()
