"""Bounded documentary oracle/operand/process projection over retained sources."""
import argparse
from copy import deepcopy
from dataclasses import fields, is_dataclass, replace
from enum import Enum
import json
import os
from common_v2 import (ROOT, OUT, DOCS, Q, PREFIX, PRIOR, INPUT, HISTORICAL, TERMS,
    NEGATIVES, c, read, ref, at, aid, qid, save, equal, Reject, check_pins,
    recovered, selection, consumer, process, metadata_body, input_plan)
from adapter.planner import (model as m, core, gates as g, typed_proofs as tp,
    installation as i, proof_installation as pi)
from adapter.planner.selector import validate_policy

CALLS = []


def deny(name):
    def no(*args, **kwargs):
        CALLS.append(name)
        raise AssertionError('PC03 mapping cannot execute ' + name)
    return no


# core.recompute and its immutable speculative coverage calculations remain
# ordinary read-only calculations. No actual result/event/commit path is open.
for module, names in (
    (core, ('apply_event', 'apply_result', 'apply_receipt', 'apply_recorded_decision',
        'apply_decision_reentry', 'admit_dossier_materialization', 'resume_eligibility')),
    (c, ('apply_event', '_replay', 'restore', 'record_result', 'append_event', 'commit_event', 'commit_result',
        'save_bundle', 'admit_external_evidence', '_publish_head', '_prefix_bundle', 'bundle_id', 'bundle_bytes')),
    (i, ('apply', 'commit')), (pi, ('apply', 'admit_semantic_authority')), (tp, ('apply',))):
    for name in names:
        setattr(module, name, deny(module.__name__ + '.' + name))


def present(value, form):
    if is_dataclass(value) and type(value).__name__ in c.TYPES:
        changes = {}
        for field in fields(value):
            item = present(getattr(value, field.name), form)
            if field.name in c.SET_FIELDS.get(type(value), set()) and len(item) > 1:
                item = tuple(reversed(item)) if form == 'reversed' else item[1:] + item[:1] if form == 'rotated' else item
            changes[field.name] = item
        return replace(value, **changes)
    if type(value) is tuple:
        return tuple(present(x, form) for x in value)
    return value


def load_model(spec, form='original'):
    value = at(read(ROOT / spec['source']['path']), spec['source']['pointer'])
    if spec['type'] == 'PersistenceBundle':
        bundle = present(c._unwire(value['bundle']), form)
        return bundle.current, bundle
    return present(c._unwire(value), form), None


def semantic_summary(encoded):
    return {'context': encoded['context'],
        'Action_status': {x['id']['value']: x['state']['value'] for x in encoded['statuses']},
        'Knowledge': [{'id': x['id']['value'], 'state': x['state']['value'], 'validation': x['validation']['value'],
            'producer': x.get('producer'), 'outcome': x.get('outcome'), 'source': x['provenance']['identity']} for x in encoded['knowledge']],
        'roots': {x['id']['value']: x['state']['value'] for x in encoded['roots']},
        'slots': {x['id']['value']: x['state']['value'] for x in encoded['slots']},
        'gates': [{'id': x['id'], 'stage': x['stage'], 'history': x['history'], 'pending': x['pending']} for x in encoded.get('external_gates', [])],
        'decisions': [{'action': x['action'], 'stage': x['stage'], 'record': x['record'], 'recorded_choice': x['recorded_choice']} for x in encoded.get('decisions', [])],
        'proof_contracts': [x['id'] for x in encoded.get('proof_contracts', [])],
        'typed_proofs': [x['id'] for x in encoded.get('typed_proofs', [])],
        'receipts': [{'artifact': x['artifact'], 'claims': x['claims']} for x in encoded.get('receipt_admissions', [])],
        'observations': encoded.get('receipt_observations', []),
        'validation_instances': [{'predicate': x['predicate'], 'dossier': x['dossier'], 'result': x['result'],
            'currentness': x['currentness']} for x in encoded.get('validation_instances', [])],
        'ValidationResults': [x['id'] for x in encoded.get('validation_results', [])],
        'support_records': [x['id'] for x in encoded.get('validation_support_records', [])]}


def model_view(spec, form):
    state, bundle = load_model(spec, form)
    encoded = c._wire(state)
    equal('exact selected native Snapshot identity', aid(c.snapshot_id(state)), spec['native_snapshot'])
    equal('exact selected native context', encoded['context'], spec['context'])
    versions = []
    for record in state.installed_definitions:
        desc = c.parse_json(record.request.definition.descriptor_json.encode())
        versions.append({'record_id': aid(record.id), 'definition_id': aid(record.request.definition.id),
            'content_id': desc['content_id'], 'type': desc['definition_type'], 'sequence': record.request.sequence,
            'authority_id': aid(record.request.authority.id), 'consumer': desc['subject']['consumer'],
            'scope': desc['scope'], 'lineage': desc['lineage'], 'generation': desc['generation']})
    return {'selected_model': spec, 'native_snapshot_identity': aid(c.snapshot_id(state)),
        'full_state_comparison_identity': qid('qualification-PC03-full-state-view-v1', encoded),
        'native_snapshot_source': dict(spec['source'], pointer='/bundle/current') if bundle else spec['source'],
        'semantic_summary': semantic_summary(encoded),
        'definition_versions': sorted(versions, key=lambda x: x['sequence']),
        'initial_snapshot': aid(c.snapshot_id(bundle.initial)) if bundle else None,
        'ordered_event_trace': [{'sequence': e.sequence, 'event_id': aid(e.identity),
            'parent_event': None if e.parent_event is None else aid(e.parent_event),
            'pre_state': aid(e.parent_snapshot), 'post_state': aid(e.after_snapshot),
            'native_result_type': type(e.result).__name__,
            'result_comparison_identity': qid('qualification-PC03-retained-result-view-v1', c._wire(e.result))}
            for e in bundle.events] if bundle else [],
        'source_policy': {'sources': c._wire(bundle)['sources'], 'policy': c._wire(bundle.policy), 'version': bundle.policy_version} if bundle else None,
        'oracle_binding': {'source': spec['semantic_oracle'], 'role': spec['oracle_role'],
            'exact_comparison_identity': qid('qualification-PC03-comparator-view-v1', at(read(ROOT / spec['semantic_oracle']['path']), spec['semantic_oracle']['pointer'])),
            'comparison_only': True},
        'lifecycle_occurrence_created': False}


def materialize(form='original'):
    body = metadata_body()
    selected = selection()
    body['models'] = [model_view(spec, form) for spec in selected['native_models']]
    body['independent_boundary_bindings'] = [dict(pair,
        expected=at(read(ROOT / pair['independent_expected']['path']), pair['independent_expected']['pointer']),
        comparison_only=True) for pair in selected['independent_boundary_pairs']]
    body['mutation_bindings'] = [dict(item, expected_contract=at(read(ROOT / item['contract']['path']), item['contract']['pointer']),
        retained_result_identity='raw-file-sha256:' + item['retained_results']['raw_sha256'],
        no_mutation_run=True) for item in selected['mutation_families']]
    p = {'identity': qid('qualification-PC03-END-projection-v1', body), 'projection': body}
    rows = []
    for name, typ, source, role in input_plan():
        rows.append({'INPUT_ID': name, 'EXPECTED_TYPE': typ, 'SOURCE_ARTIFACT': source,
            'SOURCE_IDENTITY': 'raw-file-sha256:' + source['raw_sha256'],
            'EXPECTED_SEMANTICS': {'type': typ, 'role': role, 'selector': source['pointer'],
                'immutable_content_required': True},
            'PROJECTION_IDENTITY': p['identity'], 'CONSUMER': consumer(), 'PROCESS': process()['identity'],
            'SCOPE': 'E2-QUALIFICATION-ONLY',
            'LINEAGE': 'Exact selected native/source checkpoint context; no merged lineage or historical identity replacement',
            'PROVENANCE': source, 'CURRENTNESS': body['currentness'], 'input_role': role})
    mb = {'schema': 'PC03-END-INVOCATION-INPUT-MANIFEST-1', 'consumer': consumer(), 'process': process(),
        'projection_identity': p['identity'], 'interface': INPUT, 'inputs': rows,
        'invocations': process()['definition']['invocations'], 'environment': process()['definition']['environment'],
        'process_edges': ['Retained independent PC03/local oracles and native phase/mutation/checkpoint operands -> END projection',
            'END projection -> invocation/input manifest', 'Explicit manifest/process -> E2-END#/dependencies/2'],
        'hidden_process_memory': False, 'native_mutating_operations': [],
        'comparison_files_excluded_from_Planner_operands': True, 'P05_EXECUTED': False}
    return p, {'identity': qid('qualification-PC03-END-manifest-v1', mb), 'manifest': mb}


def calculation_wire(value):
    if type(value).__name__ in c.TYPES:
        return c._wire(value)
    if is_dataclass(value):
        return {'native_type': type(value).__name__, **{f.name: calculation_wire(getattr(value, f.name)) for f in fields(value)}}
    if isinstance(value, Enum):
        return {'native_enum': type(value).__name__, 'value': value.value}
    if isinstance(value, (tuple, list)):
        return [calculation_wire(x) for x in value]
    if isinstance(value, dict):
        return {k: calculation_wire(v) for k, v in value.items()}
    if value is None or type(value) in (str, bool, int):
        return value
    raise TypeError(type(value))


def validate_ledger(bundle):
    last = None
    previous_snapshot = c.snapshot_id(bundle.initial)
    for index, event in enumerate(bundle.events, 1):
        equal('native ordered ledger sequence', event.sequence, index)
        equal('native parent event continuity', event.parent_event, last)
        equal('native pre-state continuity', event.parent_snapshot, previous_snapshot)
        equal('unchanged native event identity', event.identity, c._event_identity(event.sequence, event.parent_snapshot,
            event.parent_event, event.result, event.after_snapshot, event.resume_binding))
        last, previous_snapshot = event.identity, event.after_snapshot
    equal('retained last event binds exact current state', previous_snapshot, c.snapshot_id(bundle.current))


def native_validation(form='original'):
    selected = selection(); rows = []; states = {}; computations = {}
    for spec in selected['native_models']:
        state, bundle = load_model(spec, form)
        before = c.snapshot_bytes(state)
        m.validate_model(state)
        computation = core.recompute(state)
        states[spec['model_id']], computations[spec['model_id']] = state, computation
        versions = []
        if bundle:
            equal('immutable trusted bundle bytes', c._identity((ROOT / spec['source']['path']).read_bytes(), 'planner-bundle-v1'), c._unwire({'$type': 'ArtifactIdentity',
                'kind': {'$enum': 'IdentityKind', 'value': 'CONTENT_IDENTITY'}, 'namespace': spec['native_bundle'].split(':')[0], 'sha256': spec['native_bundle'].split(':')[1]}))
            c._verify_sources(bundle, ROOT); c._check_snapshot_pins(state, bundle.sources)
            validate_policy(bundle.policy, bundle.policy_version)
            validate_ledger(bundle)
            for record in state.installed_definitions:
                desc, native = i.descriptor(record.request.definition)
                i.validate_authority(record.request, state.context)
                active = i.current(bundle, record)
                if desc['definition_type'] == 'EXTERNAL_RESOLUTION_CONTRACT':
                    equal('retained route source support current', i.route_support_current(state, native), True)
                else:
                    equal('exact checkpoint active definition', active, True)
                versions.append({'type': desc['definition_type'], 'definition': aid(record.request.definition.id),
                    'sequence': record.request.sequence, 'source_support_current': True, 'consumer_applicable_now': active})
        expected = at(read(ROOT / spec['semantic_oracle']['path']), spec['semantic_oracle']['pointer'])
        if spec['model_id'].startswith('P04_'):
            # Independent F02 lifecycle assertions are checked separately below.
            # The frozen full Computation is only a writer/reader fidelity term.
            equal('full retained computation fidelity', calculation_wire(computation), expected['computation'])
            if state.evidence_requirements:
                equal('retained obligation Proof fidelity', calculation_wire(g.obligation_proof(state, state.evidence_requirements[0].id)), expected['obligation_proof'])
            m.validate_types(c._unwire(expected['resume']), m.ResumeEligibility)
            for field, value in {'context': c._wire(state.context), 'sources': c._wire(bundle)['sources'],
                'policy': c._wire(bundle.policy), 'policy_version': bundle.policy_version,
                'ledger_root': c._wire(bundle.events[0].identity),
                'typed_proof_usability': [{'id': c._wire(p.id), 'usable': tp.usable(state, p)} for p in sorted(state.typed_proofs, key=lambda p: p.id.sha256)]}.items():
                equal('full checkpoint fidelity ' + field, value, expected[field])
        elif spec['model_id'] == 'A03_QUALIFIED_POST_STATE':
            last = expected['result_oracles'][-1]
            equal('A03 independently expected state', aid(c.snapshot_id(state)), last['POST_STATE_ID'])
            equal('A03 independent control', computation.control.value, last['control'])
            equal('A03 independent accumulated Knowledge', c._wire(state)['knowledge'],
                sorted([record for result in expected['result_oracles'] for record in result['knowledge']], key=c.canonical_bytes))
        elif spec['model_id'] == 'A04_QUALIFIED_POST_STATE':
            equal('A04 independent complete Snapshot', c.snapshot_id(state), c.snapshot_id(c._unwire(expected['expected_post_state'])))
            equal('A04 independent control', computation.control.value, expected['expected_control'])
            equal('A04 exact independently expected validations', c._wire(state)['validation_instances'],
                sorted(expected['expected_validation_instances'], key=c.canonical_bytes))
        elif spec['model_id'] == 'A06_QUALIFIED_POST_STATE':
            equal('A06 independent Snapshot', aid(c.snapshot_id(state)), expected['snapshot_identity'])
            equal('A06 independent control', computation.control.value, expected['CONTROL'])
            equal('A06 governed event ordering', [e.result.stage.value for e in bundle.events], ['EVIDENCE_REQUEST_READY', 'WAITING_FOR_EXTERNAL_EVIDENCE'])
            equal('A06 unresolved gate history', [x.value for x in state.external_gates[0].history], expected['gate_history'])
        elif spec['model_id'] == 'P03_QUALIFIED_POST_STATE':
            equal('P03 independent complete Snapshot', c.snapshot_id(state), c.snapshot_id(c._unwire(expected['checkpoint'])))
            equal('P03 independently scoped control', computation.control.value, expected['checkpoint_control'])
        equal('native source Snapshot remains byte exact', c.snapshot_bytes(state), before)
        rows.append({'model_id': spec['model_id'], 'native_snapshot': aid(c.snapshot_id(state)),
            'native_model': 'PASS', 'native_types': 'PASS', 'physical_source_pins': 'PASS' if bundle else 'HISTORICAL_EMBEDDED_SCOPE',
            'control': None if computation.control is None else computation.control.value,
            'ordered_event_count': len(bundle.events) if bundle else 0, 'definition_versions': versions,
            'no_native_mutation': True})
    independent = []
    for pair in selected['independent_boundary_pairs']:
        state = states[pair['native_model_id']]; comp = computations[pair['native_model_id']]
        expected = at(read(ROOT / pair['independent_expected']['path']), pair['independent_expected']['pointer'])
        equal('independent current boundary control', comp.control.value, expected['control'])
        equal('independent current boundary root', state.roots[0].state.value, expected['root'])
        equal('independent current boundary slot', state.slots[0].state.value, expected['slot'])
        equal('independently bound typed proof instances', sorted(p.id.sha256 for p in state.typed_proofs), sorted(x['sha256'] for x in expected['typed_proofs']))
        equal('unchanged independent goal inventory', c._wire(state)['goals'], sorted(expected['goal_inventory'], key=c.canonical_bytes))
        equal('retained typed proof support remains usable', all(tp.usable(state, p) for p in state.typed_proofs), True)
        independent.append({'name': pair['oracle_name'], 'model': pair['native_model_id'], 'RESULT': 'PASS',
            'independent_oracle_source': pair['independent_expected']})
    equal('no actual result/event/replay/commit', CALLS, [])
    return {'RESULT': 'PASS', 'model_count': len(rows), 'model_checks': rows,
        'independent_boundary_checks': independent, 'native_mutating_calls': CALLS,
        'ResumeEligibility_not_replayed_or_persisted_as_permission': True,
        'writer_derived_fidelity_comparators_not_lifecycle_oracles': True}


def preflight(p, mf, full_native=True, form='original'):
    expected = read(OUT / 'expected-oracle.json')
    for field in ('source_selection', 'original_PC03_qualification', 'models', 'independent_boundary_bindings',
                  'mutation_bindings', 'consumer', 'process', 'currentness'):
        equal('independent PC03 interface ' + field, p['projection'][field], expected['expected_projection'][field])
    equal('whole independent projection', p['projection'], expected['expected_projection'])
    equal('projection identity', p['identity'], qid('qualification-PC03-END-projection-v1', p['projection']))
    equal('whole independent manifest', mf['manifest'], read(OUT / 'expected-manifest-oracle.json')['expected_manifest'])
    equal('manifest identity', mf['identity'], qid('qualification-PC03-END-manifest-v1', mf['manifest']))
    check_pins(p); check_pins(mf)
    native = native_validation(form) if full_native else {'RESULT': 'FIXED_COMPARATOR_ONLY'}
    return {'PC03_END_INTERFACE': 'PASS', 'terms': {name: 'PASS' for name in TERMS},
        'projection_identity': p['identity'], 'manifest_identity': mf['identity'],
        'native_validation': native, 'native_mutating_calls': CALLS}


def negatives():
    results = []
    for case in read(OUT / 'negative-plan.json')['cases']:
        p = deepcopy(read(OUT / 'END-projection.json')); mf = deepcopy(read(OUT / 'invocation-input-manifest.json'))
        body = p['projection']; model = body['models'][3]; name = case['name']
        native_rejection = None
        if name == 'wrong_source': model['selected_model']['source'] = body['source_selection']['primary_sources'][0]
        elif name == 'wrong_qualification': body['original_PC03_qualification']['phase_oracle'] = 'FAIL'
        elif name == 'missing_source': body['models'].pop()
        elif name == 'extra_source': body['models'].append(deepcopy(body['models'][0]))
        elif name == 'wrong_native_identity': model['native_snapshot_identity'] = 'planner-event-v1:' + 'a' * 64
        elif name == 'wrong_semantic_value': body['independent_boundary_bindings'][0]['expected']['control'] = 'RUNNABLE'
        elif name == 'wrong_consumer': body['consumer']['input'] = 'E2-END#/dependencies/1'
        elif name == 'wrong_process': body['process']['identity'] = 'qualification-other-process-v1:' + 'a' * 64
        elif name == 'missing_manifest_input': mf['manifest']['inputs'].pop()
        elif name == 'extra_manifest_input': mf['manifest']['inputs'].append(deepcopy(mf['manifest']['inputs'][0]))
        elif name == 'wrong_projection': p['identity'] = 'planner-snapshot-v1:' + 'a' * 64
        elif name == 'wrong_current_version': body['models'][-1]['definition_versions'][-1]['definition_id'] = 'planner-installable-definition-v1:' + 'a' * 64
        elif name == 'wrong_scope': model['selected_model']['context']['scope'] = 'PRODUCTION'
        elif name == 'wrong_lineage': model['selected_model']['context']['lineage'] = 'ORIGINAL'
        elif name == 'wrong_provenance': model['selected_model']['source']['pointer'] = '/bundle/initial'
        elif name == 'stale_source': model['selected_model']['source']['raw_sha256'] = '0' * 64
        elif name == 'report_substituted_for_native_source': model['selected_model']['source'] = body['source_selection']['primary_sources'][1]
        elif name == 'unordered_order_sensitive_identity': p['identity'] = qid('qualification-PC03-END-projection-v1', {'presentation': 'reversed', 'body': body})
        elif name == 'ordered_ancestry_permutation':
            spec = next(x for x in selection()['native_models'] if x['model_id'] == 'A06_QUALIFIED_POST_STATE')
            _, bundle = load_model(spec)
            try: validate_ledger(replace(bundle, events=tuple(reversed(bundle.events))))
            except Reject as error: native_rejection = error.record['term']
            else: raise AssertionError('native ordered ancestry permutation accepted')
            row = next(x for x in body['models'] if x['selected_model']['model_id'] == 'A06_QUALIFIED_POST_STATE')
            row['ordered_event_trace'].reverse()
        elif name == 'old_POST_REENTRY_oracle_substitution': body['independent_boundary_bindings'][0]['expected']['control'] = body['original_PC03_fixture']['phase_oracle'][-1]['control']
        elif name == 'comparison_oracle_used_as_Planner_operand':
            next(x for x in mf['manifest']['inputs'] if x['input_role'] == 'COMPARISON_ONLY')['input_role'] = 'PINNED_NATIVE_OPERAND'
        elif name == 'hidden_writer_memory': mf['manifest']['hidden_process_memory'] = True
        elif name == 'cross_lineage_history_splice': body['models'][2]['initial_snapshot'] = body['models'][-1]['initial_snapshot']
        elif name == 'missing_independent_boundary_pair': body['independent_boundary_bindings'].pop()
        else: raise AssertionError('unsealed negative ' + name)
        if name not in ('wrong_projection', 'unordered_order_sensitive_identity'):
            p['identity'] = qid('qualification-PC03-END-projection-v1', body)
            mf['manifest']['projection_identity'] = p['identity']
        mf['identity'] = qid('qualification-PC03-END-manifest-v1', mf['manifest'])
        try: preflight(p, mf, full_native=False)
        except Reject as error:
            results.append(dict(case, RESULT='PASS', rejection=error.record['term'],
                native_ordered_ledger_rejection=native_rejection, successful_native_sources_unchanged=True))
        else: raise AssertionError('negative accepted ' + name)
    save('negative-results.json', {'RESULT': 'PASS', 'count': len(results), 'cases': results,
        'unordered_positive_presentations_equivalent': True, 'ordered_ancestry_permutation_rejected_natively': True,
        'retained_PC03_or_lifecycle_negatives_not_rerun': True, 'native_mutating_calls': CALLS})
    return {'NEGATIVE_SUITE': 'PASS', 'count': len(results)}


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('mode', choices=('materialize', 'preflight', 'negatives', 'reader'))
    parser.add_argument('--seed'); parser.add_argument('--index')
    parser.add_argument('--presentation', default='original', choices=('original', 'reversed', 'rotated'))
    args = parser.parse_args()
    if args.mode == 'materialize':
        p, mf = materialize()
        save('END-projection.json', p); save('invocation-input-manifest.json', mf)
        save('source-semantics-inventory.json', {'native_models': p['projection']['models'],
            'independent_boundary_pairs': p['projection']['independent_boundary_bindings'],
            'mutations': p['projection']['mutation_bindings'], 'original_fixture': p['projection']['original_PC03_fixture']})
        save('process-binding.json', {'process': p['projection']['process'], 'projection': ref(OUT / 'END-projection.json'),
            'manifest': ref(OUT / 'invocation-input-manifest.json'), 'consumer': consumer(), 'edges': mf['manifest']['process_edges'],
            'RESULT': 'MATERIALIZED_BEFORE_PREFLIGHT'})
        result = {'MATERIALIZED': True, 'projection_identity': p['identity'], 'manifest_input_count': len(mf['manifest']['inputs'])}
    elif args.mode == 'preflight':
        result = preflight(read(OUT / 'END-projection.json'), read(OUT / 'invocation-input-manifest.json'))
        save('preflight.json', result)
    elif args.mode == 'negatives': result = negatives()
    else:
        equal('seed environment', os.environ.get('PYTHONHASHSEED'), args.seed)
        p, mf = materialize(args.presentation)
        result = preflight(p, mf, form=args.presentation)
        result = {key: value for key, value in result.items() if key != 'native_validation'}
        result.update(seed=args.seed, reader=args.index, presentation=args.presentation,
            writer_memory_available=False, native_model_count=16, ordered_events_permuted=False)
        save('readers/seed-' + args.seed + '-reader-' + args.index + '-' + args.presentation + '.json', result)
    print(json.dumps({k: v for k, v in result.items() if k != 'native_validation'}, sort_keys=True))


if __name__ == '__main__':
    main()
