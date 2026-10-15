"""Independent raw-byte PC03 comparison oracle, sealed before materialization.

Does not import the materializer/decoder or run native operations. Selected
qualified source identities, independent lifecycle oracles and persistence
comparators are retained with their original distinct assurance roles.
"""
import json
from common_v2 import (ROOT, OUT, DOCS, PREFIX, Q, INPUT, HISTORICAL, TERMS,
    NEGATIVES, c, read, ref, at, qid, save, equal, check_pins,
    recovered, selection, consumer, process, metadata_body, input_plan)


def normalize(value):
    if isinstance(value, list):
        return [normalize(x) for x in value]
    if isinstance(value, dict):
        out = {k: normalize(v) for k, v in value.items()}
        cls = c.TYPES.get(value.get('$type'))
        for field in c.SET_FIELDS.get(cls, set()):
            if field in out:
                out[field] = sorted(out[field], key=c.canonical_bytes)
        return out
    return value


def identity(value):
    return None if value is None else value['namespace'] + ':' + value['sha256']


def main():
    selected = selection(); sources = recovered()['PROVENANCE']
    baseline = read(OUT.parent / 'baseline.json')['file_sha256']
    for path, digest in baseline.items():
        if path in [x['path'] for x in sources]:
            equal('pre-work primary pin', next(x['raw_sha256'] for x in sources if x['path'] == path), digest)
    for name in ('PC01', 'PC02'):
        previous = read(DOCS / (PREFIX + 'E2_P05_' + name + '_END_BINDING_1.json'))
        equal('previous interface qualification unchanged', previous[name + '_END_INTERFACE'], 'PASS')
    fixture = read(ROOT / sources[0]['path']); qualification = read(ROOT / sources[1]['path'])
    for key in ('phase_oracle', 'persistence_contract', 'cold_restore_contract', 'invalidation_contract'):
        equal('original PC03 qualification ' + key, qualification[key], 'PASS')
    equal('original case inventory', (len(fixture['cases']['positive']), len(fixture['cases']['negative'])), (16, 16))
    equal('phase oracle declared order', [x['phase'] for x in fixture['phase_oracle']],
        ['INITIAL', 'PRE_EXTERNAL', 'EXTERNAL_CHECKPOINT', 'COLD_RESTORED', 'EVIDENCE_RECEIVED',
         'EVIDENCE_VALIDATED', 'REENTRY_ELIGIBLE', 'POST_REENTRY'])
    equal('original invalidation dependency inventory', len(fixture['invalidation']), 6)
    equal('no original PC03 producer execution', fixture['actions_executed'], 0)
    equal('full source collection selected', len(selected['native_models']), 16)
    expected = metadata_body(); models = []
    for spec in selected['native_models']:
        raw = at(read(ROOT / spec['source']['path']), spec['source']['pointer'])
        bundle = normalize(raw['bundle']) if spec['type'] == 'PersistenceBundle' else None
        state = bundle['current'] if bundle else normalize(raw)
        equal('independent native context selection', state['context'], spec['context'])
        versions = []
        for record in state.get('installed_definitions', []):
            req = record['request']; desc = json.loads(req['definition']['descriptor_json'])
            versions.append({'record_id': identity(record['id']), 'definition_id': identity(req['definition']['id']),
                'content_id': desc['content_id'], 'type': desc['definition_type'], 'sequence': req['sequence'],
                'authority_id': identity(req['authority']['id']), 'consumer': desc['subject']['consumer'],
                'scope': desc['scope'], 'lineage': desc['lineage'], 'generation': desc['generation']})
        # Build the expected summary directly from independent raw field access;
        # no materializer extraction helper or computed output is used.
        summary = {'context': state['context'],
            'Action_status': {x['id']['value']: x['state']['value'] for x in state['statuses']},
            'Knowledge': [{'id': x['id']['value'], 'state': x['state']['value'], 'validation': x['validation']['value'],
                'producer': x.get('producer'), 'outcome': x.get('outcome'), 'source': x['provenance']['identity']} for x in state['knowledge']],
            'roots': {x['id']['value']: x['state']['value'] for x in state['roots']},
            'slots': {x['id']['value']: x['state']['value'] for x in state['slots']},
            'gates': [{'id': x['id'], 'stage': x['stage'], 'history': x['history'], 'pending': x['pending']} for x in state.get('external_gates', [])],
            'decisions': [{'action': x['action'], 'stage': x['stage'], 'record': x['record'], 'recorded_choice': x['recorded_choice']} for x in state.get('decisions', [])],
            'proof_contracts': [x['id'] for x in state.get('proof_contracts', [])],
            'typed_proofs': [x['id'] for x in state.get('typed_proofs', [])],
            'receipts': [{'artifact': x['artifact'], 'claims': x['claims']} for x in state.get('receipt_admissions', [])],
            'observations': state.get('receipt_observations', []),
            'validation_instances': [{'predicate': x['predicate'], 'dossier': x['dossier'], 'result': x['result'],
                'currentness': x['currentness']} for x in state.get('validation_instances', [])],
            'ValidationResults': [x['id'] for x in state.get('validation_results', [])],
            'support_records': [x['id'] for x in state.get('validation_support_records', [])]}
        initial_snapshot = 'planner-snapshot-v1:' + qid('raw', {'schema': 'PLANNER-SNAPSHOT-1', 'snapshot': bundle['initial']}).split(':')[1] if bundle else None
        trace = [{'sequence': e['sequence'], 'event_id': identity(e['identity']), 'parent_event': identity(e['parent_event']),
            'pre_state': identity(e['parent_snapshot']), 'post_state': identity(e['after_snapshot']),
            'native_result_type': e['result']['$type'],
            'result_comparison_identity': qid('qualification-PC03-retained-result-view-v1', e['result'])}
            for e in bundle['events']] if bundle else []
        models.append({'selected_model': spec, 'native_snapshot_identity': spec['native_snapshot'],
            'full_state_comparison_identity': qid('qualification-PC03-full-state-view-v1', state),
            'native_snapshot_source': dict(spec['source'], pointer='/bundle/current') if bundle else spec['source'],
            'semantic_summary': summary, 'definition_versions': sorted(versions, key=lambda x: x['sequence']),
            'initial_snapshot': initial_snapshot, 'ordered_event_trace': trace,
            'source_policy': {'sources': bundle['sources'], 'policy': bundle['policy'], 'version': bundle['policy_version']} if bundle else None,
            'oracle_binding': {'source': spec['semantic_oracle'], 'role': spec['oracle_role'],
                'exact_comparison_identity': qid('qualification-PC03-comparator-view-v1', at(read(ROOT / spec['semantic_oracle']['path']), spec['semantic_oracle']['pointer'])),
                'comparison_only': True}, 'lifecycle_occurrence_created': False})
    expected['models'] = models
    expected['independent_boundary_bindings'] = [dict(pair,
        expected=at(read(ROOT / pair['independent_expected']['path']), pair['independent_expected']['pointer']),
        comparison_only=True) for pair in selected['independent_boundary_pairs']]
    expected['mutation_bindings'] = [dict(family, expected_contract=at(read(ROOT / family['contract']['path']), family['contract']['pointer']),
        retained_result_identity='raw-file-sha256:' + family['retained_results']['raw_sha256'], no_mutation_run=True)
        for family in selected['mutation_families']]
    equal('current post-A12 control remains independently sealed', expected['independent_boundary_bindings'][0]['expected']['control'], 'PLAN_DEFECT')
    save('expected-oracle.json', {'schema': 'PC03-END-INDEPENDENT-BINDING-ORACLE-1',
        'expected_projection': expected, 'expected_terms': {key: 'PASS' for key in TERMS},
        'authorship': 'Pinned raw contracts/native source bytes and already independent local expectations; no materializer or native operation output used',
        'comparator_only': True, 'sealed_before_materialization': True,
        'lifecycle_expected_vs_writer_fidelity_distinguished': True})
    projection_id = qid('qualification-PC03-END-projection-v1', expected)
    proc = process(); rows = []
    for name, typ, source, role in input_plan():
        rows.append({'INPUT_ID': name, 'EXPECTED_TYPE': typ, 'SOURCE_ARTIFACT': source,
            'SOURCE_IDENTITY': 'raw-file-sha256:' + source['raw_sha256'],
            'EXPECTED_SEMANTICS': {'type': typ, 'role': role, 'selector': source['pointer'], 'immutable_content_required': True},
            'PROJECTION_IDENTITY': projection_id, 'CONSUMER': consumer(), 'PROCESS': proc['identity'],
            'SCOPE': 'E2-QUALIFICATION-ONLY',
            'LINEAGE': 'Exact selected native/source checkpoint context; no merged lineage or historical identity replacement',
            'PROVENANCE': source, 'CURRENTNESS': expected['currentness'], 'input_role': role})
    manifest = {'schema': 'PC03-END-INVOCATION-INPUT-MANIFEST-1', 'consumer': consumer(), 'process': proc,
        'projection_identity': projection_id, 'interface': INPUT, 'inputs': rows,
        'invocations': proc['definition']['invocations'], 'environment': proc['definition']['environment'],
        'process_edges': ['Retained independent PC03/local oracles and native phase/mutation/checkpoint operands -> END projection',
            'END projection -> invocation/input manifest', 'Explicit manifest/process -> E2-END#/dependencies/2'],
        'hidden_process_memory': False, 'native_mutating_operations': [],
        'comparison_files_excluded_from_Planner_operands': True, 'P05_EXECUTED': False}
    save('expected-manifest-oracle.json', {'expected_manifest': manifest, 'comparator_only': True,
        'expected_input_count': len(rows), 'sealed_before_materialization': True})
    save('negative-plan.json', {'count': len(NEGATIVES), 'cases': [{'id': 'PC03-END-N%02d' % (index + 1),
        'name': name, 'expected': 'REJECT_BEFORE_INTERFACE_PASS'} for index, name in enumerate(NEGATIVES)],
        'sealed_before_preflight': True, 'ordered_permutation_requires_native_ledger_rejection': True,
        'unordered_presentations_must_preserve_identity': True, 'PC03_or_prior_producers_not_rerun': True})
    save('oracle-seal.json', {'RESULT': 'SEALED_BEFORE_MATERIALIZATION', 'oracle': ref(OUT / 'expected-oracle.json'),
        'manifest_oracle': ref(OUT / 'expected-manifest-oracle.json'), 'negative_plan': ref(OUT / 'negative-plan.json'),
        'selection': ref(OUT.parent / 'selected-source-collection.json'), 'process_identity': proc['identity'],
        'expected_projection_identity': projection_id,
        'expected_manifest_identity': qid('qualification-PC03-END-manifest-v1', manifest),
        'no_materializer_output_or_native_operation_used': True})
    print(json.dumps({'ORACLE': 'SEALED', 'manifest_inputs': len(rows), 'native_model_count': len(models),
        'negative_cases': len(NEGATIVES), 'expected_projection_identity': projection_id}))


if __name__ == '__main__':
    main()
