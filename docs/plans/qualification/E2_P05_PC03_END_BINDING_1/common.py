"""Documentary PC03 binding metadata; reuse qualified comparison primitives."""
import importlib.util
from functools import lru_cache
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
DOCS = ROOT / 'docs/plans'
Q = DOCS / 'qualification'
PREFIX = 'DETERMINISTIC_PLANNER_V0_1_'
PRIOR = Q / 'E2_P05_PC02_END_BINDING_1'
CLOSURE = Q / 'E2_P05_END_INTERFACE_CLOSURE_1'
COMPOSITE = Q / 'E2_P05_COMPOSITE_END_QUALIFICATION_1'
spec = importlib.util.spec_from_file_location('qualified_pc02_documentary_primitives', PRIOR / 'contract.py')
primitive = importlib.util.module_from_spec(spec)
spec.loader.exec_module(primitive)
read, sha, ref, at = primitive.read, primitive.sha, primitive.ref, primitive.at
aid, qid, equal, Reject = primitive.aid, primitive.qid, primitive.equal, primitive.Reject
pins, check_pins, c = primitive.pins, primitive.check_pins, primitive.c
INPUT = 'E2-END#/dependencies/2'
HISTORICAL = primitive.HISTORICAL
TERMS = primitive.TERMS
GRAPH_ID = primitive.GRAPH_ID
ACCEPTANCE_ID = primitive.ACCEPTANCE_ID


def save(name, value):
    path = OUT / name
    raw = (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + '\n').encode()
    if path.exists():
        equal('immutable PC03 qualification evidence ' + name, path.read_bytes(), raw)
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)


@lru_cache(maxsize=1)
def recovered():
    item = read(CLOSURE / 'six-interface-inventory.json')['interfaces'][2]
    equal('sealed PC03 interface ordinal', item['ORDINAL'], 3)
    equal('sealed consumer input', item['INTERFACE_ID'], INPUT)
    equal('sealed PC03 consumer edge', item['SEALED_EDGE_ID'],
        'qualification-END-edge-v1:b34d2cb6f849d1f4a5f8ef5bc52ba2fcaffb8c61c02e64c4c30befb9c1d8cb0e')
    check_pins(item)
    return item


@lru_cache(maxsize=1)
def selection():
    selected = read(OUT / 'selected-source-collection.json')
    equal('selected primary sources match recovered contract', selected['primary_sources'], recovered()['PROVENANCE'])
    check_pins(selected)
    return selected


@lru_cache(maxsize=1)
def consumer():
    contract = recovered()
    return {'input': INPUT, 'declaration': contract['CONSUMER_DECLARATION'], 'edge': contract['SEALED_EDGE_ID'],
        'semantics': contract['REQUIRED_OUTPUT'], 'scope': contract['SCOPE'],
        'graph_identity': GRAPH_ID, 'acceptance_mapping_identity': ACCEPTANCE_ID,
        'existing_scope_capture': ref(COMPOSITE / 'scope-authentication.json'),
        'native_END_Action_or_slot': False}


@lru_cache(maxsize=1)
def process():
    value = {'schema': 'PC03-END-READ-ONLY-PROCESS-1',
        'semantics': recovered()['PROCESS'], 'consumer': INPUT,
        'selection': ref(OUT / 'selected-source-collection.json'),
        'code': [ref(OUT / name) for name in ('select_sources.py', 'common.py', 'binding.py', 'oracle.py')],
        'reused_documentary_identity_and_pin_primitives': ref(PRIOR / 'contract.py'),
        'native_primitives': [ref(ROOT / ('adapter/planner/' + name + '.py')) for name in
            ('model', 'codec', 'core', 'gates', 'typed_proofs', 'installation', 'proof_installation', 'selector')],
        'interpreter': {'path': sys.executable, 'version': sys.version},
        'environment': {'PYTHONDONTWRITEBYTECODE': '1', 'PYTHONPATH': '.'},
        'invocations': {'seal': [sys.executable, str((OUT / 'oracle.py').relative_to(ROOT))],
            'materialize': [sys.executable, str((OUT / 'binding.py').relative_to(ROOT)), 'materialize'],
            'preflight': [sys.executable, str((OUT / 'binding.py').relative_to(ROOT)), 'preflight'],
            'negatives': [sys.executable, str((OUT / 'binding.py').relative_to(ROOT)), 'negatives'],
            'readers': [[sys.executable, str((OUT / 'binding.py').relative_to(ROOT)), 'reader',
                '--seed', str(seed), '--index', str(index), '--presentation', form]
                for seed in (0, 1, 7, 101) for index in (1, 2, 3)
                for form in ('original', 'reversed', 'rotated')]},
        'operative_inputs': 'Pinned existing native source bytes and declared contracts; no producer is invoked',
        'comparison_inputs': 'Independent fixed oracles and writer fidelity comparators are comparison-only, never Planner operands',
        'historical_writer_reader_records': 'Retained provenance and allowlists, not commands authorized to run now',
        'pure_computation': 'Structural/identity/currentness and read-only core.recompute over immutable retained states; no commit or actual execution',
        'no_ledger_restore_or_replay_or_result_application': True, 'native_mutating_operations': [],
        'ordered_event_and_phase_sequences': 'Never normalized as unordered sets'}
    return {'identity': qid('qualification-PC03-END-process-v1', value), 'definition': value}


def metadata_body():
    selected = selection()
    source = recovered()['PROVENANCE']
    return {'schema': 'PC03-END-PROJECTION-1', 'kind': 'QUALIFICATION_EVIDENCE_NOT_NATIVE_STATE',
        'recovered_contract': recovered(), 'source_selection': selected,
        'original_PC03_fixture': read(ROOT / source[0]['path']),
        'original_PC03_qualification': read(ROOT / source[1]['path']),
        'F03_qualification_result': {'source': source[2], 'RESULT': read(ROOT / source[2]['path'])['RESULT'],
            'scope': 'Isolated F03 native qualification; actual canonical P04 operands selected separately'},
        'consumer': consumer(), 'process': process(), 'historical_exclusions': HISTORICAL,
        'currentness': {'boundary': 'Current documentary P05 END consumption of exact retained role/checkpoint versions',
            'historical_template_role': 'Original baseline PC03 phase assertions remain original preparation specifications',
            'current_POST_REENTRY': 'Already sealed F02/F03 PLAN_DEFECT at post-A12; not old scaffold RUNNABLE/FINISH/true-resume',
            'native_versions': 'Supported installed versions at each exact checkpoint; later definitions absent before their installation',
            'route_applicability': 'Supported retained acquisition contract may be inapplicable after completion',
            'resume': 'Already-qualified local comparison values remain computed evidence; no persisted eligibility permission',
            'source_policy_code': 'Physical pins/current native support and exact process code/oracle inputs',
            'no_new_runtime_permission': True},
        'EXISTING_BINDING_PATTERN_REUSABLE': 'YES_WITH_PC03_ORACLE_OPERAND_PROCESS_VARIANT',
        'new_native_state_event_INSTALL_authority': False}


def fixed_inputs():
    return [('END_CONSUMER', 'Experiment interface declaration', recovered()['CONSUMER_DECLARATION'], 'CONTRACT'),
        ('RECOVERED_CONTRACT', 'PC03 independent comparison interface', ref(CLOSURE / 'six-interface-inventory.json', '/interfaces/2'), 'CONTRACT'),
        ('SELECTED_SOURCES', 'Exact current comparison/operand selection', ref(OUT / 'selected-source-collection.json'), 'CONTRACT'),
        ('SCOPE_CAPTURE', 'Existing authenticated qualification scope', consumer()['existing_scope_capture'], 'QUALIFICATION_SCOPE_ONLY'),
        ('COMPOSITE_GRAPH', 'Unchanged qualified evidence graph', selection()['unchanged_stage_graph'], 'QUALIFIED_SOURCE'),
        ('COMPOSITE_ACCEPTANCE_MAPPING', 'Existing qualified acceptance overlay', ref(COMPOSITE / 'qualified-composite-mapping.json'), 'QUALIFIED_SOURCE'),
        ('PC01_PATTERN', 'Closed PC01 documentary binding', ref(DOCS / (PREFIX + 'E2_P05_PC01_END_BINDING_1.json')), 'QUALIFIED_SOURCE'),
        ('PC02_PATTERN', 'Closed PC02 documentary binding', ref(DOCS / (PREFIX + 'E2_P05_PC02_END_BINDING_1.json')), 'QUALIFIED_SOURCE'),
        ('INDEPENDENT_BINDING_ORACLE', 'Fixed independent metadata comparator', ref(OUT / 'expected-oracle.json'), 'COMPARISON_ONLY')]


def input_plan():
    selected = selection()
    rows = []
    for index, source in enumerate(selected['primary_sources']):
        rows.append(('PRIMARY_SOURCE_%d' % index, ['PC03 fixture declarations', 'PC03 preparation-scope validation', 'F03 qualified boundary collection'][index], source, 'QUALIFIED_SOURCE'))
    for model in selected['native_models']:
        rows.append(('NATIVE_' + model['model_id'], model['type'], model['source'], 'PINNED_NATIVE_OPERAND'))
        rows.append(('ORACLE_' + model['model_id'], model['oracle_role'], model['semantic_oracle'], 'COMPARISON_ONLY'))
    for pair in selected['independent_boundary_pairs']:
        rows.append(('BOUNDARY_' + pair['oracle_name'], 'Independent F02 boundary contract', pair['independent_expected'], 'COMPARISON_ONLY'))
    for index, family in enumerate(selected['mutation_families']):
        rows.append(('MUTATION_CONTRACT_' + family['family'], 'Sealed isolated mutation/rejection expectations', family['contract'], 'COMPARISON_ONLY'))
        rows.append(('MUTATION_HISTORY_' + family['family'], 'Retained qualification results; no new run', family['retained_results'], 'QUALIFIED_SOURCE'))
        for number, code in enumerate(family['producer_code']):
            rows.append(('MUTATION_CODE_' + family['family'] + '_' + str(number), 'Pinned historical mutation driver', code, 'PROCESS_HISTORY_PROVENANCE'))
    for index, source in enumerate(selected['process_evidence']):
        rows.append(('PROCESS_HISTORY_' + str(index), 'Exact retained writer/reader/input/oracle record', source, 'PROCESS_HISTORY_PROVENANCE'))
    return rows + fixed_inputs()


NEGATIVES = ('wrong_source', 'wrong_qualification', 'missing_source', 'extra_source',
    'wrong_native_identity', 'wrong_semantic_value', 'wrong_consumer', 'wrong_process',
    'missing_manifest_input', 'extra_manifest_input', 'wrong_projection', 'wrong_current_version',
    'wrong_scope', 'wrong_lineage', 'wrong_provenance', 'stale_source',
    'report_substituted_for_native_source', 'unordered_order_sensitive_identity',
    'ordered_ancestry_permutation', 'old_POST_REENTRY_oracle_substitution',
    'comparison_oracle_used_as_Planner_operand', 'hidden_writer_memory',
    'cross_lineage_history_splice', 'missing_independent_boundary_pair')
