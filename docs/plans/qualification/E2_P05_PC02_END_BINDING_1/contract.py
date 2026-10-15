"""Pinned PC02 consumer contract and documentary comparison primitives.

This module declares metadata only. It cannot install, execute or restore a
Planner lineage. Qualification identities are separate from native identities.
"""
import hashlib
import json
import sys
from pathlib import Path
from adapter.planner import codec as c

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
DOCS = ROOT / 'docs/plans'
PREFIX = 'DETERMINISTIC_PLANNER_V0_1_'
CLOSURE = DOCS / 'qualification/E2_P05_END_INTERFACE_CLOSURE_1'
PRIOR = DOCS / 'qualification/E2_P05_PC01_END_BINDING_1'
COMPOSITE = DOCS / 'qualification/E2_P05_COMPOSITE_END_QUALIFICATION_1'
INPUT = 'E2-END#/dependencies/1'
GRAPH_ID = 'qualification-END-evidence-graph-v1:d3979240252a12139aac34db1bb1cb2396c6860af371084b94118740ec23af15'
ACCEPTANCE_ID = 'qualification-composite-END-acceptance-v1:6c37715a38233e9f556279e182bb3a13d5f03579257e20d787a858c5d246941c'
SNAPSHOT_ID = 'planner-snapshot-v1:046fdc270a0060503729151368a68672f76af122830b86e65d372e6bc5d7dea4'
CONTEXT = {'$type': 'EvaluationContext', 'scope': 'E2-QUALIFICATION-ONLY',
    'lineage': 'E2-P03-PROSPECTIVE-QUALIFICATION-1',
    'generation': 'E2-P03-PROSPECTIVE-GENERATION-1', 'tick': 0, 'allowed_effects': []}
FIELDS = (
    'actions', 'decisions', 'validation_instances', 'entities', 'predicates',
    'evidence_requirements', 'external_gates', 'ingress_contracts',
    'validation_contracts', 'validation_support_contracts', 'validation_transaction_contracts',
    'proof_contracts', 'roots', 'slots', 'boundaries', 'receipt_admissions',
    'receipt_observations', 'validation_results', 'validation_support_records',
    'typed_proofs', 'knowledge', 'reevaluations', 'statuses', 'goals')
ROLE_FIELDS = {
    'DOSSIER': ['decisions', 'validation_instances', 'predicates', 'knowledge', 'actions'],
    'GRANT': ['entities', 'predicates', 'decisions', 'actions'],
    'ROOT_PROOF': ['proof_contracts', 'roots', 'slots', 'entities', 'typed_proofs'],
    'SLOT_PROOF': ['proof_contracts', 'slots', 'entities', 'knowledge', 'typed_proofs'],
    'EXTERNAL_ROUTE': ['evidence_requirements', 'external_gates', 'boundaries', 'validation_contracts',
        'validation_support_contracts', 'validation_transaction_contracts', 'receipt_observations'],
    'ATTESTOR': ['entities', 'predicates', 'ingress_contracts', 'receipt_admissions']}
TERMS = ('SOURCE', 'CONSUMER', 'PROJECTION', 'PROCESS', 'INPUT_MANIFEST',
    'CURRENTNESS', 'SCOPE', 'LINEAGE', 'PROVENANCE')
HISTORICAL = {key: 'UNPROVEN' for key in (
    'ORIGINAL_A03_HISTORICAL_OCCURRENCE', 'ORIGINAL_A04_HISTORICAL_ANCESTRY',
    'ORIGINAL_A05_HISTORICAL_ANCESTRY', 'ORIGINAL_A06_HISTORICAL_REQUEST_WAIT_TRACE',
    'P03_HISTORICAL_CORRESPONDENCE')}


class Reject(Exception):
    def __init__(self, term, expected, actual):
        self.record = {'term': term, 'expected': expected, 'actual': actual}
        super().__init__(json.dumps(self.record, sort_keys=True, default=str))


def equal(term, actual, expected):
    if actual != expected:
        raise Reject(term, expected, actual)


def read(path):
    return json.loads(Path(path).read_bytes())


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def aid(value):
    return value.namespace + ':' + value.sha256


def qid(namespace, value):
    return namespace + ':' + hashlib.sha256(c.canonical_bytes(value)).hexdigest()


def ref(path, pointer=''):
    return {'path': str(Path(path).relative_to(ROOT)), 'pointer': pointer, 'raw_sha256': sha(path)}


def at(value, pointer):
    for token in pointer.split('/')[1:]:
        token = token.replace('~1', '/').replace('~0', '~')
        value = value[int(token)] if isinstance(value, list) else value[token]
    return value


def save(name, value):
    path = OUT / name
    data = (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + '\n').encode()
    if path.exists():
        equal('immutable qualification artifact ' + name, path.read_bytes(), data)
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)


def pins(value):
    if isinstance(value, dict):
        if isinstance(value.get('path'), str) and isinstance(value.get('raw_sha256'), str):
            yield value
        for child in value.values():
            yield from pins(child)
    elif isinstance(value, list):
        for child in value:
            yield from pins(child)


def check_pins(value):
    for pin in pins(value):
        path = ROOT / pin['path']
        equal('source bytes ' + pin['path'], sha(path), pin['raw_sha256'])
        if pin.get('pointer') and path.suffix == '.json':
            at(read(path), pin['pointer'])


def recovered():
    item = read(CLOSURE / 'six-interface-inventory.json')['interfaces'][1]
    equal('sealed PC02 ordinal', item['ORDINAL'], 2)
    equal('sealed consumer slot', item['INTERFACE_ID'], INPUT)
    equal('sealed PC02 edge', item['SEALED_EDGE_ID'],
        'qualification-END-edge-v1:e45ec4bf691372c7726d213cd9de9fa07e5c82688effb94880150e0826df3d10')
    check_pins(item)
    return item


def source_specs():
    declared = recovered()['PROVENANCE']
    equal('three already recovered source artifacts', len(declared), 3)
    roles = ['ORIGINAL_PC02_FIXTURE_CONTRACTS', 'ORIGINAL_PC02_QUALIFICATION', 'CURRENT_P04_NATIVE_CONTRACTS']
    return [dict(role=role, source=pin, source_type=typ, use=use)
        for role, pin, typ, use in zip(roles, declared,
            ['E2-PC02-FIXTURES-1', 'E2-PC02-VALIDATION-1', 'PersistenceBundle/current Snapshot'],
            ['Historical preparation-scope declarations; not lifecycle instances or P04 authority',
             'Retained preparation-scope PASS; not a future END execution PASS',
             'Current typed native definitions and their retained canonical support/history'])]


def consumer():
    old = recovered()
    return {'input_id': INPUT, 'declaration': old['CONSUMER_DECLARATION'],
        'edge_id': old['SEALED_EDGE_ID'], 'required_assurance': old['SEALED_REQUIRED_ASSURANCE'],
        'composite_graph_identity': GRAPH_ID, 'acceptance_mapping_identity': ACCEPTANCE_ID,
        'scope_capture': ref(COMPOSITE / 'scope-authentication.json'),
        'native_END_Action_or_slot': False}


def process():
    body = {'schema': 'PC02-END-READ-ONLY-PROCESS-1',
        'kind': 'READ_ONLY_QUALIFICATION_PROJECTION_AND_INPUT_BINDING',
        'contract': ref(CLOSURE / 'six-interface-inventory.json', '/interfaces/1'),
        'declared_semantics': recovered()['PROCESS'], 'consumer': INPUT,
        'code': [ref(OUT / name) for name in ('contract.py', 'binding.py', 'oracle.py')],
        'native_primitives': [ref(ROOT / ('adapter/planner/' + name + '.py')) for name in
            ('codec', 'model', 'gates', 'installation', 'action_installation', 'proof_installation',
             'typed_proofs', 'authentication_installation', 'validation_installation', 'selector')],
        'precedent': ref(DOCS / (PREFIX + 'E2_P05_PC01_END_BINDING_1.json')),
        'invocations': {'seal': [sys.executable, str((OUT / 'oracle.py').relative_to(ROOT))],
            'materialize': [sys.executable, str((OUT / 'binding.py').relative_to(ROOT)), 'materialize'],
            'preflight': [sys.executable, str((OUT / 'binding.py').relative_to(ROOT)), 'preflight'],
            'negatives': [sys.executable, str((OUT / 'binding.py').relative_to(ROOT)), 'negatives'],
            'readers': [[sys.executable, str((OUT / 'binding.py').relative_to(ROOT)), 'reader',
                '--seed', str(seed), '--index', str(index), '--presentation', form]
                for seed in (0, 1, 7, 101) for index in (1, 2, 3)
                for form in ('original', 'reversed', 'rotated')]},
        'interpreter': {'path': sys.executable, 'version': sys.version},
        'environment': {'PYTHONDONTWRITEBYTECODE': '1', 'PYTHONPATH': '.'},
        'declared_unordered_presentations': ['original', 'reversed', 'rotated'],
        'native_mutating_operations': [], 'new_native_process_definition': False,
        'authority_use': 'Existing bounded qualification consumption only; not INSTALL/USE/execution',
        'ordered_event_ledger_preserved': True}
    return {'identity': qid('qualification-PC02-END-process-v1', body), 'process': body}


def fixed_inputs():
    return [
        ('END_CONSUMER', 'EXPERIMENT_ACCEPTANCE_CASE interface declaration', recovered()['CONSUMER_DECLARATION']),
        ('RECOVERED_INTERFACE_CONTRACT', 'Recovered PC02 consumer/process terms', ref(CLOSURE / 'six-interface-inventory.json', '/interfaces/1')),
        ('SCOPE_CAPTURE', 'Existing authenticated bounded qualification-scope selection', ref(COMPOSITE / 'scope-authentication.json')),
        ('COMPOSITE_GRAPH', 'Unchanged qualification evidence graph', ref(DOCS / 'qualification/E2_P05_END_ANCESTRY_RECONCILIATION_1/qualified-evidence-graph.json')),
        ('ACCEPTANCE_MAPPING', 'Qualified composite acceptance overlay', ref(COMPOSITE / 'qualified-composite-mapping.json')),
        ('PC01_PATTERN_PRECEDENT', 'Qualified read-only binding mechanism only', ref(DOCS / (PREFIX + 'E2_P05_PC01_END_BINDING_1.json'))),
        ('GOVERNED_CONFIGURATION_HISTORY', 'Retained actual installation history', ref(DOCS / 'qualification/E2_P05_END_INPUT_BINDING_1/configuration-history.json')),
        ('SUPPORTED_POLICY', 'Supported selector/codec policy', ref(ROOT / 'docs/experiments/E1/E1_GRAPH_RESOLUTION_SELECTION_POLICY_1.md')),
        ('INDEPENDENT_ORACLE', 'Fixed comparator only; excluded from Planner operands', ref(OUT / 'expected-oracle.json'))]


def currentness_contract():
    return {'boundary': 'Current P05 documentary consumption at the exact canonical P04 target',
        'original_fixture': 'Historical qualified E2-CANONICAL-BASELINE-1 declarations; no P04 retagging or authority reuse',
        'current_native_snapshot': SNAPSHOT_ID, 'current_native_context': CONTEXT,
        'definitions': 'Exact active installed versions with native authority/source support and retained install ancestry',
        'source_policy': 'Physical P04 source pins and supported current policy verified read-only',
        'route': {'support_current': True, 'current_acquisition_applicability': False,
            'reason': 'Completed gate lifecycle; retained governed route is supported history, not live acquisition permission'},
        'root_slot': 'Distinct current source-bound contract and authority identities; no new instance admission',
        'qualified_variants': 'Both original known-rule absence and governed-unknown variants remain qualification contracts; no second P04 gate invented',
        'dossier_checks': 'Nine original named checks retained; current native supported typed evaluations remain exact and separately bound',
        'permission_inference_from_END_mapping': False}


NEGATIVES = (
    'wrong_PC02_native_source', 'wrong_PC02_qualification', 'missing_required_source',
    'extra_primary_source', 'wrong_source_identity', 'wrong_semantic_proposition',
    'wrong_consumer', 'wrong_process', 'missing_manifest_input', 'extra_manifest_input',
    'wrong_projection_identity', 'wrong_current_proof_contract_version', 'wrong_scope',
    'wrong_lineage', 'wrong_provenance', 'stale_source', 'report_substituted_for_native_artifact',
    'order_sensitive_projection_identity', 'slot_proof_substituted_for_root_contract',
    'old_fixture_authority_reused_in_P04', 'receipt_collapsed_into_validation',
    'historical_READINESS_upgraded_to_execution_permission')
