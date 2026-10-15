"""Read-only PC02 END projection and preflight over retained native contracts."""
import argparse
from copy import deepcopy
from dataclasses import fields, is_dataclass, replace
from enum import Enum
import hashlib
import json
import os
from contract import (ROOT, OUT, DOCS, PREFIX, CLOSURE, PRIOR, COMPOSITE, INPUT,
    GRAPH_ID, ACCEPTANCE_ID, SNAPSHOT_ID, CONTEXT, FIELDS, ROLE_FIELDS, TERMS,
    HISTORICAL, NEGATIVES, c, read, sha, aid, qid, ref, at, save, equal,
    Reject, check_pins, recovered, source_specs, consumer, process, fixed_inputs,
    currentness_contract)
from adapter.planner import (model as m, core, gates as g, installation as i,
    proof_installation as pi, typed_proofs as tp, authentication_installation as auth,
    validation_installation as vi, action_installation as ai)
from adapter.planner.selector import validate_policy

CALLS = []


def deny(name):
    def no(*args, **kwargs):
        CALLS.append(name)
        raise AssertionError('Qualification binding cannot perform ' + name)
    return no


for module, names in (
    (core, ('apply_event', 'apply_result', 'apply_receipt', 'recompute', 'resume_eligibility', '_inventory')),
    (c, ('apply_event', '_replay', 'record_result', 'append_event', 'commit_event', 'commit_result',
         'save_bundle', 'restore', 'admit_external_evidence', '_publish_head', '_prefix_bundle', 'bundle_id', 'bundle_bytes')),
    (i, ('apply', 'commit')), (pi, ('apply', 'admit_semantic_authority')),
    (tp, ('apply', 'reevaluate')), (auth, ('apply',)), (vi, ('apply',)), (ai, ('apply',))):
    for name in names:
        setattr(module, name, deny(module.__name__ + '.' + name))


def presented(value, form):
    """Permute only native-declared sets; never event ancestry or positional pairs."""
    if is_dataclass(value) and type(value).__name__ in c.TYPES:
        changes = {}
        for field in fields(value):
            item = presented(getattr(value, field.name), form)
            if field.name in c.SET_FIELDS.get(type(value), set()) and len(item) > 1:
                if form == 'reversed':
                    item = tuple(reversed(item))
                elif form == 'rotated':
                    item = item[1:] + item[:1]
            changes[field.name] = item
        return replace(value, **changes)
    if isinstance(value, tuple):
        return tuple(presented(x, form) for x in value)
    return value


def object_key(value):
    if isinstance(value, dict):
        for key in ('id', 'predicate', 'gate', 'action', 'artifact'):
            if key in value:
                return {'field': key, 'native_value': value[key]}
    return {'field': 'snapshot_member', 'native_value': None}


def views(encoded, source):
    result = []
    for name in FIELDS:
        values = encoded.get(name, [])
        body = {'field': name, 'source': dict(source, pointer='/bundle/current/' + name),
            'native_snapshot_identity': SNAPSHOT_ID, 'native_context': encoded['context'],
            'members': [{'source_pointer': '/bundle/current/' + name + '/' + str(index),
                'native_type': value['$type'], 'native_key': object_key(value),
                'native_value': value} for index, value in enumerate(values)]}
        result.append({'identity': qid('qualification-PC02-native-view-v1', body), 'view': body})
    return result


def installation_views(bundle, source):
    result = []
    for event in bundle.events:
        if type(event.result) is not m.InstallDefinition:
            continue
        request = event.result
        record = next(x for x in bundle.current.installed_definitions if x.request == request)
        descriptor, native = i.descriptor(request.definition)
        result.append({'event_source': dict(source, pointer='/bundle/events/' + str(event.sequence - 1)),
            'event_id': aid(event.identity), 'event_sequence': event.sequence,
            'parent_event': None if event.parent_event is None else aid(event.parent_event),
            'pre_state': aid(event.parent_snapshot), 'post_state': aid(event.after_snapshot),
            'installed_record_id': aid(record.id), 'definition_id': aid(request.definition.id),
            'definition_type': descriptor['definition_type'], 'content_id': descriptor['content_id'],
            'descriptor': descriptor, 'operation': request.operation.value,
            'INSTALL_authority_id': aid(request.authority.id),
            'operating_semantic_authority_ids': [aid(x.operating_authorization_id) for x in request.authority_bindings],
            'scope': descriptor['scope'], 'lineage': descriptor['lineage'], 'generation': descriptor['generation'],
            'provenance': c._wire(request.definition.provenance),
            'consumer': descriptor['subject']['consumer'],
            'role': 'CURRENT_SUPPORTED_HISTORY_NOT_NEW_INSTALL_OR_EXECUTION_PERMISSION'})
    return result


def projection_body(form='original'):
    specs = source_specs()
    fixture = read(ROOT / specs[0]['source']['path'])
    qualification = read(ROOT / specs[1]['source']['path'])
    bundle = presented(c._unwire(read(ROOT / specs[2]['source']['path'])['bundle']), form)
    state = bundle.current
    equal('exact current retained Snapshot', aid(c.snapshot_id(state)), SNAPSHOT_ID)
    equal('exact current native context', c._wire(state.context), CONTEXT)
    encoded = c._wire(state)
    native_views = views(encoded, specs[2]['source'])
    proc = process()
    return {'schema': 'PC02-END-QUALIFICATION-PROJECTION-1', 'kind': 'QUALIFICATION_EVIDENCE_NOT_NATIVE_STATE',
        'recovered_contract': recovered(), 'primary_sources': specs,
        'PC02_SOURCE_QUALIFICATION': 'PASS_PREPARATION_SCOPE_ONLY',
        'original_fixture': fixture, 'original_qualification': qualification,
        'native_snapshot_identity': SNAPSHOT_ID, 'current_native_context': encoded['context'],
        'native_views': native_views, 'governed_versions': installation_views(bundle, specs[2]['source']),
        'role_bindings': [{'original_role': role, 'original_declaration': next(x for x in fixture['source_roles'] if x['role'] == role),
            'native_view_identities': [v['identity'] for v in native_views if v['view']['field'] in ROLE_FIELDS[role]],
            'role': 'Exact native consumer contracts, not reissued historical source IDs or authority'}
            for role in sorted(ROLE_FIELDS)],
        'consumer': consumer(), 'process': proc,
        'scope': 'E2-QUALIFICATION-ONLY',
        'lineage_policy': 'Historical PC02 baseline and current P04 native context kept separate; no retagging or synthetic ancestry',
        'currentness_contract': currentness_contract(), 'historical_exclusions': HISTORICAL,
        'PC01_BINDING_PATTERN_REUSABLE': 'YES',
        'new_native_state_event_Snapshot_INSTALL_authority_ActionResult': False}


def manifest_body(projection):
    body = projection['projection']
    proc = body['process']
    rows = []
    for spec in body['primary_sources']:
        rows.append({'INPUT_ID': spec['role'], 'EXPECTED_TYPE': spec['source_type'],
            'SOURCE_ARTIFACT': spec['source'], 'SOURCE_IDENTITY': 'raw-file-sha256:' + spec['source']['raw_sha256'],
            'EXPECTED_SEMANTICS': spec['use'], 'PROJECTION_IDENTITY': projection['identity'],
            'CONSUMER': INPUT, 'PROCESS': proc['identity'], 'SCOPE': 'E2-QUALIFICATION-ONLY',
            'LINEAGE': body['original_fixture']['lineage'] if spec['role'] != 'CURRENT_P04_NATIVE_CONTRACTS' else CONTEXT['lineage'],
            'PROVENANCE': spec['source'], 'CURRENTNESS': currentness_contract(), 'role': 'PINNED_QUALIFICATION_INPUT'})
    for view in body['native_views']:
        item = view['view']
        rows.append({'INPUT_ID': 'NATIVE_' + item['field'].upper(), 'EXPECTED_TYPE': [x['native_type'] for x in item['members']],
            'SOURCE_ARTIFACT': item['source'], 'SOURCE_IDENTITY': SNAPSHOT_ID,
            'EXPECTED_SEMANTICS': {'view_identity': view['identity'], 'member_count': len(item['members']),
                'native_keys': [x['native_key'] for x in item['members']],
                'exact_values': 'Immutable values in the pinned source selector and projected native view'},
            'PROJECTION_IDENTITY': projection['identity'], 'CONSUMER': INPUT, 'PROCESS': proc['identity'],
            'SCOPE': CONTEXT['scope'], 'LINEAGE': CONTEXT['lineage'], 'GENERATION': CONTEXT['generation'],
            'PROVENANCE': item['source'], 'CURRENTNESS': currentness_contract(), 'role': 'PINNED_NATIVE_SOURCE_VIEW'})
    for input_id, typ, source in fixed_inputs():
        rows.append({'INPUT_ID': input_id, 'EXPECTED_TYPE': typ, 'SOURCE_ARTIFACT': source,
            'SOURCE_IDENTITY': 'raw-file-sha256:' + source['raw_sha256'], 'EXPECTED_SEMANTICS': typ,
            'PROJECTION_IDENTITY': projection['identity'], 'CONSUMER': INPUT, 'PROCESS': proc['identity'],
            'SCOPE': 'E2-QUALIFICATION-ONLY', 'LINEAGE': 'Exact declared qualification/context role; no new native lineage',
            'PROVENANCE': source, 'CURRENTNESS': 'Exact retained pin/selector at this declared consumer boundary',
            'role': 'COMPARISON_ONLY' if input_id == 'INDEPENDENT_ORACLE' else 'PINNED_QUALIFICATION_INPUT'})
    return {'schema': 'PC02-END-INVOCATION-INPUT-MANIFEST-1', 'interface': INPUT,
        'projection_identity': projection['identity'], 'consumer': consumer(), 'process': proc,
        'inputs': rows, 'invocations': proc['process']['invocations'],
        'environment': proc['process']['environment'], 'native_mutating_operations': [],
        'process_edges': ['PC02 retained contracts/native sources -> END-specific qualification projection',
            'PC02 projection -> invocation/input manifest', 'Manifest -> E2-END#/dependencies/1'],
        'P05_EXECUTED': False, 'writer': 'Metadata only; never reruns PC02 or a native lifecycle',
        'oracle_excluded_from_Planner_execution_inputs': True}


def materialize(form='original'):
    body = projection_body(form)
    p = {'identity': qid('qualification-PC02-END-projection-v1', body), 'projection': body}
    mb = manifest_body(p)
    return p, {'identity': qid('qualification-PC02-END-manifest-v1', mb), 'manifest': mb}


def native_validation():
    spec = source_specs()[2]
    bundle = c._unwire(read(ROOT / spec['source']['path'])['bundle'])
    state = bundle.current
    before = c.canonical_bytes(c._wire(bundle))
    m.validate_model(state)
    c._verify_sources(bundle, ROOT)
    c._check_snapshot_pins(state, bundle.sources)
    validate_policy(bundle.policy, bundle.policy_version)
    equal('exact native Snapshot support identity', aid(c.snapshot_id(state)), SNAPSHOT_ID)
    events = []
    last = None
    parent_state = c.snapshot_id(bundle.initial)
    for pos, event in enumerate(bundle.events, 1):
        m.validate_types(event, m.ExecutionEvent)
        equal('native ledger position', event.sequence, pos)
        equal('native append parent', event.parent_event, last)
        equal('native immutable pre-state continuity', event.parent_snapshot, parent_state)
        equal('native event comparison identity', event.identity, c._event_identity(
            event.sequence, event.parent_snapshot, event.parent_event, event.result, event.after_snapshot, event.resume_binding))
        events.append({'id': aid(event.identity), 'position': pos, 'type': type(event.result).__name__,
            'parent': None if last is None else aid(last)})
        last, parent_state = event.identity, event.after_snapshot
    equal('current Snapshot at retained head', parent_state, c.snapshot_id(state))
    version_checks = []
    for record in state.installed_definitions:
        desc, native = i.descriptor(record.request.definition)
        expected = desc['definition_type'] != 'EXTERNAL_RESOLUTION_CONTRACT'
        equal('native definition consumer-bound currentness ' + desc['definition_type'], i.current(bundle, record), expected)
        i.validate_authority(record.request, state.context)
        if not expected:
            equal('retained route support current', i.route_support_current(state, native), True)
        version_checks.append({'definition_id': aid(record.request.definition.id),
            'type': desc['definition_type'], 'sequence': record.request.sequence,
            'support_current': True, 'consumer_applicable_now': expected,
            'use': 'Current native definition' if expected else 'Historical governed route; no current acquisition permission'})
    equal('exact governed definition inventory', len(version_checks), 9)
    contracts = []
    for contract in state.proof_contracts:
        m.validate_types(contract, m.TypedProofContract)
        equal('typed proof exact native identity', contract.id, tp.identity(contract))
        equal('typed proof definition current', pi.contract_current(state, contract), True)
        contracts.append({'id': aid(contract.id), 'kind': contract.proof_type.value, 'target': contract.target.value,
            'supports': c._wire(contract.supports), 'provenance': c._wire(contract.provenance)})
    equal('distinct root and slot proof types', sorted(x['kind'] for x in contracts), ['ROOT_PROOF', 'SLOT_PROOF'])
    for proof in state.typed_proofs:
        equal('retained proof usability', tp.usable(state, proof), True)
    for decision in state.decisions:
        equal('independent native dossier readiness', g.decision_readiness(state, decision).state.value, 'DECISION_READY')
        equal('retained recorded decision applicability', g.recorded_decision_valid(state, decision), True)
    equal('current USE independent applicability', g.evaluate_predicate(state, m.PredicateId('E2-USE-AUTHORITY')).state.value, 'PROVED')
    equal('current evidence obligation support', g.obligation_proof(state, m.EvidenceId('E2-EXTERNAL-REQUIREMENT')).state.value, 'PROVED')
    for entity in state.entities:
        m.validate_provenance(entity.provenance)
        equal('native entity provenance content identity', entity.provenance.identity,
            c._identity(entity.provenance.excerpt.encode(), 'raw-file-sha256'))
    equal('read-only native model/event/source inspection', c.canonical_bytes(c._wire(bundle)), before)
    equal('native mutation barriers', CALLS, [])
    return {'RESULT': 'PASS', 'model': 'PASS', 'native_types': 'PASS', 'source_pins': 'PASS',
        'policy': 'PASS', 'provenance': 'PASS', 'ledger_membership_and_continuity': events,
        'definition_currentness': version_checks, 'proof_contracts': contracts,
        'dossier_readiness': 'PASS', 'authority_applicability': 'PASS',
        'receipt_validation_proof_boundaries': 'PASS', 'native_mutating_calls': CALLS,
        'current_route_acquisition_permission': False, 'retained_route_support_current': True}


def preflight(p, mf, full_native=True):
    expected = read(OUT / 'expected-oracle.json')
    for name in ('primary_sources', 'original_fixture', 'original_qualification', 'native_views',
                 'governed_versions', 'consumer', 'process', 'current_native_context', 'currentness_contract'):
        equal('independent expected ' + name, p['projection'][name], expected['expected_projection'][name])
    equal('exact independent projection', p['projection'], expected['expected_projection'])
    equal('projection comparison identity', p['identity'], qid('qualification-PC02-END-projection-v1', p['projection']))
    equal('independent manifest', mf['manifest'], read(OUT / 'expected-manifest-oracle.json')['expected_manifest'])
    equal('manifest comparison identity', mf['identity'], qid('qualification-PC02-END-manifest-v1', mf['manifest']))
    equal('manifest projection reference', mf['manifest']['projection_identity'], p['identity'])
    check_pins(p)
    check_pins(mf)
    checks = native_validation() if full_native else {'RESULT': 'PINNED_COMPARATOR_ONLY'}
    equal('no native mutation', CALLS, [])
    return {'PC02_END_INTERFACE': 'PASS', 'terms': {key: 'PASS' for key in TERMS},
        'projection_identity': p['identity'], 'manifest_identity': mf['identity'],
        'native_validation': checks, 'native_mutating_calls': CALLS}


def negatives():
    plan = read(OUT / 'negative-plan.json')
    answers = []
    for item in plan['cases']:
        p = deepcopy(read(OUT / 'END-projection.json'))
        mf = deepcopy(read(OUT / 'invocation-input-manifest.json'))
        b = p['projection']; name = item['name']
        group = lambda field: next(v['view'] for v in b['native_views'] if v['view']['field'] == field)
        if name == 'wrong_PC02_native_source': b['primary_sources'][2]['source'] = b['primary_sources'][0]['source']
        elif name == 'wrong_PC02_qualification': b['original_qualification']['fixture_oracle_result'] = 'FAIL'
        elif name == 'missing_required_source': b['primary_sources'].pop()
        elif name == 'extra_primary_source': b['primary_sources'].append(deepcopy(b['primary_sources'][0]))
        elif name == 'wrong_source_identity': b['primary_sources'][2]['source']['raw_sha256'] = 'a' * 64
        elif name == 'wrong_semantic_proposition': group('proof_contracts')['members'][0]['native_value']['proposition'] = 'FOREIGN'
        elif name == 'wrong_consumer': b['consumer']['input_id'] = 'E2-END#/dependencies/0'
        elif name == 'wrong_process': b['process']['identity'] = 'qualification-other-process-v1:' + 'a' * 64
        elif name == 'missing_manifest_input': mf['manifest']['inputs'].pop()
        elif name == 'extra_manifest_input': mf['manifest']['inputs'].append(deepcopy(mf['manifest']['inputs'][0]))
        elif name == 'wrong_projection_identity': p['identity'] = 'planner-snapshot-v1:' + 'a' * 64
        elif name == 'wrong_current_proof_contract_version': group('proof_contracts')['members'][0]['native_value']['id']['sha256'] = 'a' * 64
        elif name == 'wrong_scope': b['current_native_context']['scope'] = 'PRODUCTION'
        elif name == 'wrong_lineage': b['current_native_context']['lineage'] = 'E2-CANONICAL-BASELINE-1'
        elif name == 'wrong_provenance': group('proof_contracts')['members'][0]['native_value']['provenance']['method'] = 'FOREIGN'
        elif name == 'stale_source': b['currentness_contract']['route']['support_current'] = False
        elif name == 'report_substituted_for_native_artifact': b['primary_sources'][2]['source'] = ref(DOCS / (PREFIX + 'E2_PC02_VALIDATION.json'))
        elif name == 'order_sensitive_projection_identity': p['identity'] = qid('qualification-PC02-END-projection-v1', {'presentation': 'reversed', 'projection': b})
        elif name == 'slot_proof_substituted_for_root_contract':
            v = group('proof_contracts'); v['members'][0] = deepcopy(v['members'][1])
        elif name == 'old_fixture_authority_reused_in_P04': group('proof_contracts')['members'][0]['native_value']['lineage'] = 'E2-CANONICAL-BASELINE-1'
        elif name == 'receipt_collapsed_into_validation': group('validation_results')['members'] = deepcopy(group('receipt_admissions')['members'])
        elif name == 'historical_READINESS_upgraded_to_execution_permission': b['currentness_contract']['permission_inference_from_END_mapping'] = True
        else: raise AssertionError('unsealed negative ' + name)
        if name not in ('wrong_projection_identity', 'order_sensitive_projection_identity'):
            p['identity'] = qid('qualification-PC02-END-projection-v1', p['projection'])
            mf['manifest']['projection_identity'] = p['identity']
        mf['identity'] = qid('qualification-PC02-END-manifest-v1', mf['manifest'])
        try:
            preflight(p, mf, full_native=False)
        except Reject as rejection:
            answers.append(dict(item, RESULT='PASS', rejection_term=rejection.record['term'],
                independently_trusted_oracle_unchanged=True, candidate_rehashed=True))
        else:
            raise AssertionError('negative accepted ' + name)
    save('negative-results.json', {'RESULT': 'PASS', 'count': len(answers), 'cases': answers,
        'native_sources_modified': False, 'native_mutating_calls': CALLS,
        'valid_unordered_presentations': 'All equivalent; only an order-sensitive false comparison identity rejects'})
    return {'NEGATIVE_SUITE': 'PASS', 'count': len(answers)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=('materialize', 'preflight', 'reader', 'negatives'))
    parser.add_argument('--seed'); parser.add_argument('--index')
    parser.add_argument('--presentation', choices=('original', 'reversed', 'rotated'), default='original')
    args = parser.parse_args()
    if args.mode == 'materialize':
        p, mf = materialize()
        save('END-projection.json', p); save('invocation-input-manifest.json', mf)
        save('source-semantics-inventory.json', {'original_fixture': p['projection']['original_fixture'],
            'native_views': p['projection']['native_views'], 'role_bindings': p['projection']['role_bindings'],
            'governed_versions': p['projection']['governed_versions'], 'source_roles_not_retagged': True})
        save('process-binding.json', {'RESULT': 'MATERIALIZED_NOT_YET_QUALIFIED', 'process': p['projection']['process'],
            'projection': ref(OUT / 'END-projection.json'), 'manifest': ref(OUT / 'invocation-input-manifest.json'),
            'edges': mf['manifest']['process_edges'], 'consumer': consumer()})
        answer = {'MATERIALIZED': True, 'projection_identity': p['identity'], 'manifest_inputs': len(mf['manifest']['inputs'])}
    elif args.mode == 'preflight':
        answer = preflight(read(OUT / 'END-projection.json'), read(OUT / 'invocation-input-manifest.json'))
        save('preflight.json', answer)
    elif args.mode == 'negatives': answer = negatives()
    else:
        equal('explicit seed environment', os.environ.get('PYTHONHASHSEED'), args.seed)
        p, mf = materialize(args.presentation)
        answer = preflight(p, mf)
        answer = {key: value for key, value in answer.items() if key != 'native_validation'}
        answer.update(seed=args.seed, index=args.index, presentation=args.presentation,
            independent_process=True, writer_memory_available=False,
            unordered_collections=[cls.__name__ + '.' + field for cls, names in c.SET_FIELDS.items() for field in sorted(names)],
            ordered_event_ledger_permuted=False)
        save('readers/seed-' + args.seed + '-reader-' + args.index + '-' + args.presentation + '.json', answer)
    print(json.dumps(answer if args.mode != 'preflight' else {k: v for k, v in answer.items() if k != 'native_validation'}, sort_keys=True))


if __name__ == '__main__':
    main()
