"""Independent expected values from pinned raw sources, sealed before preflight.

Never imports binding.py or calls its native decoder, projection, inventory or
model checks. Native-declared set semantics are read from the unchanged codec.
Shared contract metadata supplies exact consumer/process identities, not values
chosen from materializer output.
"""
from copy import deepcopy
import json
from contract import (ROOT, OUT, DOCS, PREFIX, CLOSURE, PRIOR, COMPOSITE, INPUT,
    SNAPSHOT_ID, CONTEXT, FIELDS, ROLE_FIELDS, HISTORICAL, NEGATIVES, c, read, ref,
    save, qid, equal, check_pins, recovered, source_specs, consumer, process,
    fixed_inputs, currentness_contract)


def normalize(value):
    if isinstance(value, list):
        return [normalize(x) for x in value]
    if isinstance(value, dict):
        answer = {k: normalize(v) for k, v in value.items()}
        cls = c.TYPES.get(value.get('$type'))
        for field in c.SET_FIELDS.get(cls, set()):
            if field in answer:
                answer[field] = sorted(answer[field], key=c.canonical_bytes)
        return answer
    return value


def simple_identity(value):
    return None if value is None else value['namespace'] + ':' + value['sha256']


def main():
    baseline = read(OUT / 'baseline.json')['file_sha256']
    for directory in (CLOSURE, PRIOR):
        verification = read(directory / 'verification.json')
        for pin in verification['reports'] + verification['harnesses']:
            check_pins(pin)
    old = recovered()
    equal('PC01 remains qualified', read(DOCS / (PREFIX + 'E2_P05_PC01_END_BINDING_1.json'))['PC01_END_INTERFACE'], 'PASS')
    specs = source_specs()
    for item in specs:
        equal('pre-work source byte pin', item['source']['raw_sha256'], baseline[item['source']['path']])
    fixture = read(ROOT / specs[0]['source']['path'])
    qualification = read(ROOT / specs[1]['source']['path'])
    raw_bundle = read(ROOT / specs[2]['source']['path'])['bundle']
    s = normalize(raw_bundle['current'])
    equal('original PC02 preparation PASS', qualification['fixture_oracle_result'], 'PASS')
    equal('six distinct declared PC02 roles', sorted(x['role'] for x in fixture['source_roles']), sorted(ROLE_FIELDS))
    equal('retained original scope', fixture['scope'], 'E2-QUALIFICATION-ONLY')
    equal('retained baseline lineage', fixture['lineage'], 'E2-CANONICAL-BASELINE-1')
    equal('PC02 does not claim execution', fixture['actions_executed'], 0)
    equal('independent original oracle assigned cases', (len(fixture['cases']), qualification['pc02_cases']), (23, 23))
    equal('nine distinct original dossier checks', len(set(fixture['dossier']['checks'])), 9)
    equal('current native context', s['context'], CONTEXT)
    equal('native current root-slot contract cardinality', len(s['proof_contracts']), 2)
    equal('independent typed contract kinds', sorted(p['proof_type']['value'] for p in s['proof_contracts']), ['ROOT_PROOF', 'SLOT_PROOF'])
    root = next(p for p in s['proof_contracts'] if p['proof_type']['value'] == 'ROOT_PROOF')
    slot = next(p for p in s['proof_contracts'] if p['proof_type']['value'] == 'SLOT_PROOF')
    equal('slot consumes actual reenter output', slot['supports'], [{'$type': 'KnowledgeId', 'value': 'E2-K-REENTER'}])
    equal('root consumes satisfied distinct slot', root['supports'], [{'$type': 'SlotId', 'value': 'E2-SLOT'}])
    equal('independent proof propositions', (slot['proposition'], root['proposition']), ('E2-SLOT-PROPOSITION', 'E2-ROOT-PROPOSITION'))
    equal('distinct source content', root['provenance']['identity'] == slot['provenance']['identity'], False)
    equal('distinct native semantic authority', root['authority'] == slot['authority'], False)
    for p in (slot, root):
        equal('current proof definition consumer context', (p['scope'], p['lineage'], p['generation']),
            (CONTEXT['scope'], CONTEXT['lineage'], CONTEXT['generation']))
    equal('both historical route variants retain expected absence',
        [fixture['external_routes'][name]['positive_evidence'] for name in ('known_rule', 'governed_unknown')], [False, False])
    equal('governed unknown rule absent', fixture['external_routes']['governed_unknown']['rule_known'], False)
    equal('authority identity domain', fixture['authority']['identity_domain'], 'AUTHORITY_IDENTITY')
    equal('exact semantic separation invariants', fixture['invariants'], [
        'authority requirement != possession', 'possession != applicability',
        'evidence requirement != receipt', 'receipt != validation', 'validation != proof',
        'proof != resume', 'Action PASS != root/slot satisfaction',
        'expected absence != positive evidence', 'selection != execution'])
    proc = process()
    expected_views = []
    for field in FIELDS:
        members = []
        for index, value in enumerate(s.get(field, [])):
            key = next((k for k in ('id', 'predicate', 'gate', 'action', 'artifact') if k in value), None)
            members.append({'source_pointer': '/bundle/current/' + field + '/' + str(index),
                'native_type': value['$type'],
                'native_key': {'field': key, 'native_value': value[key]} if key else {'field': 'snapshot_member', 'native_value': None},
                'native_value': value})
        view = {'field': field, 'source': dict(specs[2]['source'], pointer='/bundle/current/' + field),
            'native_snapshot_identity': SNAPSHOT_ID, 'native_context': s['context'], 'members': members}
        expected_views.append({'identity': qid('qualification-PC02-native-view-v1', view), 'view': view})
    versions = []
    for event in raw_bundle['events']:
        if event['result']['$type'] != 'InstallDefinition':
            continue
        req = event['result']
        desc = json.loads(req['definition']['descriptor_json'])
        # Direct retained native membership, not event inferred from final state.
        record = next(r for r in s['installed_definitions'] if normalize(r['request']) == normalize(req))
        versions.append({'event_source': dict(specs[2]['source'], pointer='/bundle/events/' + str(event['sequence'] - 1)),
            'event_id': simple_identity(event['identity']), 'event_sequence': event['sequence'],
            'parent_event': simple_identity(event['parent_event']),
            'pre_state': simple_identity(event['parent_snapshot']), 'post_state': simple_identity(event['after_snapshot']),
            'installed_record_id': simple_identity(record['id']), 'definition_id': simple_identity(req['definition']['id']),
            'definition_type': desc['definition_type'], 'content_id': desc['content_id'], 'descriptor': desc,
            'operation': req['operation']['value'], 'INSTALL_authority_id': simple_identity(req['authority']['id']),
            'operating_semantic_authority_ids': [simple_identity(x['operating_authorization_id']) for x in req.get('authority_bindings', [])],
            'scope': desc['scope'], 'lineage': desc['lineage'], 'generation': desc['generation'],
            'provenance': normalize(req['definition']['provenance']), 'consumer': desc['subject']['consumer'],
            'role': 'CURRENT_SUPPORTED_HISTORY_NOT_NEW_INSTALL_OR_EXECUTION_PERMISSION'})
    equal('expected governed installed versions', len(versions), 9)
    equal('exact deferred concrete contract boundaries',
        [(x['definition_type'], x['event_sequence']) for x in versions if x['definition_type'].endswith('PROOF_CONTRACT_DEFINITION')],
        [('SLOT_PROOF_CONTRACT_DEFINITION', 16), ('ROOT_PROOF_CONTRACT_DEFINITION', 18)])
    expected = {'schema': 'PC02-END-QUALIFICATION-PROJECTION-1', 'kind': 'QUALIFICATION_EVIDENCE_NOT_NATIVE_STATE',
        'recovered_contract': old, 'primary_sources': specs, 'PC02_SOURCE_QUALIFICATION': 'PASS_PREPARATION_SCOPE_ONLY',
        'original_fixture': fixture, 'original_qualification': qualification,
        'native_snapshot_identity': SNAPSHOT_ID, 'current_native_context': s['context'],
        'native_views': expected_views, 'governed_versions': versions,
        'role_bindings': [{'original_role': role,
            'original_declaration': next(x for x in fixture['source_roles'] if x['role'] == role),
            'native_view_identities': [v['identity'] for v in expected_views if v['view']['field'] in ROLE_FIELDS[role]],
            'role': 'Exact native consumer contracts, not reissued historical source IDs or authority'} for role in sorted(ROLE_FIELDS)],
        'consumer': consumer(), 'process': proc, 'scope': 'E2-QUALIFICATION-ONLY',
        'lineage_policy': 'Historical PC02 baseline and current P04 native context kept separate; no retagging or synthetic ancestry',
        'currentness_contract': currentness_contract(), 'historical_exclusions': HISTORICAL,
        'PC01_BINDING_PATTERN_REUSABLE': 'YES', 'new_native_state_event_Snapshot_INSTALL_authority_ActionResult': False}
    save('expected-oracle.json', {'schema': 'PC02-END-INDEPENDENT-ORACLE-1', 'expected_projection': expected,
        'authorship': 'Raw pinned PC02/source/consumer contracts and native source bytes; no materializer or native transition called',
        'expected_terms': {term: 'PASS' for term in ('SOURCE', 'CONSUMER', 'PROJECTION', 'PROCESS', 'INPUT_MANIFEST', 'CURRENTNESS', 'SCOPE', 'LINEAGE', 'PROVENANCE')},
        'comparator_only': True, 'sealed_before_materialization_preflight': True})
    projection_id = qid('qualification-PC02-END-projection-v1', expected)
    rows = []
    for spec in specs:
        rows.append({'INPUT_ID': spec['role'], 'EXPECTED_TYPE': spec['source_type'],
            'SOURCE_ARTIFACT': spec['source'], 'SOURCE_IDENTITY': 'raw-file-sha256:' + spec['source']['raw_sha256'],
            'EXPECTED_SEMANTICS': spec['use'], 'PROJECTION_IDENTITY': projection_id,
            'CONSUMER': INPUT, 'PROCESS': proc['identity'], 'SCOPE': 'E2-QUALIFICATION-ONLY',
            'LINEAGE': CONTEXT['lineage'] if spec['role'] == 'CURRENT_P04_NATIVE_CONTRACTS' else fixture['lineage'],
            'PROVENANCE': spec['source'], 'CURRENTNESS': currentness_contract(), 'role': 'PINNED_QUALIFICATION_INPUT'})
    for v in expected_views:
        view = v['view']
        rows.append({'INPUT_ID': 'NATIVE_' + view['field'].upper(),
            'EXPECTED_TYPE': [x['native_type'] for x in view['members']],
            'SOURCE_ARTIFACT': view['source'], 'SOURCE_IDENTITY': SNAPSHOT_ID,
            'EXPECTED_SEMANTICS': {'view_identity': v['identity'], 'member_count': len(view['members']),
                'native_keys': [x['native_key'] for x in view['members']],
                'exact_values': 'Immutable values in the pinned source selector and projected native view'},
            'PROJECTION_IDENTITY': projection_id, 'CONSUMER': INPUT, 'PROCESS': proc['identity'],
            'SCOPE': CONTEXT['scope'], 'LINEAGE': CONTEXT['lineage'], 'GENERATION': CONTEXT['generation'],
            'PROVENANCE': view['source'], 'CURRENTNESS': currentness_contract(), 'role': 'PINNED_NATIVE_SOURCE_VIEW'})
    for input_id, typ, source in fixed_inputs():
        rows.append({'INPUT_ID': input_id, 'EXPECTED_TYPE': typ, 'SOURCE_ARTIFACT': source,
            'SOURCE_IDENTITY': 'raw-file-sha256:' + source['raw_sha256'], 'EXPECTED_SEMANTICS': typ,
            'PROJECTION_IDENTITY': projection_id, 'CONSUMER': INPUT, 'PROCESS': proc['identity'],
            'SCOPE': 'E2-QUALIFICATION-ONLY', 'LINEAGE': 'Exact declared qualification/context role; no new native lineage',
            'PROVENANCE': source, 'CURRENTNESS': 'Exact retained pin/selector at this declared consumer boundary',
            'role': 'COMPARISON_ONLY' if input_id == 'INDEPENDENT_ORACLE' else 'PINNED_QUALIFICATION_INPUT'})
    manifest = {'schema': 'PC02-END-INVOCATION-INPUT-MANIFEST-1', 'interface': INPUT,
        'projection_identity': projection_id, 'consumer': consumer(), 'process': proc,
        'inputs': rows, 'invocations': proc['process']['invocations'], 'environment': proc['process']['environment'],
        'native_mutating_operations': [],
        'process_edges': ['PC02 retained contracts/native sources -> END-specific qualification projection',
            'PC02 projection -> invocation/input manifest', 'Manifest -> E2-END#/dependencies/1'],
        'P05_EXECUTED': False, 'writer': 'Metadata only; never reruns PC02 or a native lifecycle',
        'oracle_excluded_from_Planner_execution_inputs': True}
    save('expected-manifest-oracle.json', {'expected_manifest': manifest, 'comparator_only': True,
        'sealed_before_materialization_preflight': True})
    save('negative-plan.json', {'count': len(NEGATIVES), 'cases': [
        {'id': 'PC02-END-N%02d' % (index + 1), 'name': name, 'expected': 'REJECT_BEFORE_INTERFACE_PASS'}
        for index, name in enumerate(NEGATIVES)],
        'sealed_before_preflight': True, 'native_sources_not_modified': True,
        'unordered_rule': 'Equivalent native set presentations pass; a fabricated order-sensitive identity rejects'})
    save('source-pins.json', {'sources': specs, 'recovered_PC02_contract': ref(CLOSURE / 'six-interface-inventory.json', '/interfaces/1'),
        'PC02_result': ref(DOCS / (PREFIX + 'E2_PC02_RESULT.md')),
        'original_qualification_result': 'PASS_PREPARATION_SCOPE_ONLY',
        'native_snapshot': SNAPSHOT_ID, 'native_context': CONTEXT,
        'process': proc, 'authority_requirement': 'Existing bounded documentary acceptance scope; no new native/INSTALL authority',
        'PC01_pattern_reusable': True, 'PC01_semantics_copied_to_PC02': False})
    save('oracle-seal.json', {'RESULT': 'SEALED_BEFORE_MATERIALIZATION',
        'oracle': ref(OUT / 'expected-oracle.json'), 'manifest_oracle': ref(OUT / 'expected-manifest-oracle.json'),
        'negative_plan': ref(OUT / 'negative-plan.json'), 'process_identity': proc['identity'],
        'expected_projection_identity': projection_id,
        'expected_manifest_identity': qid('qualification-PC02-END-manifest-v1', manifest),
        'sequence': ['Pin recovered contract/sources', 'Raw independent expectations/negative plan seal',
            'Future typed source projection materialization', 'Future independent preflight'],
        'no_future_materializer_output_used': True})
    print(json.dumps({'ORACLE': 'SEALED', 'negative_count': len(NEGATIVES), 'manifest_input_count': len(rows),
        'projection_identity_expected': projection_id}, sort_keys=True))


if __name__ == '__main__':
    main()
