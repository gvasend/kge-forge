"""Execute only the already sealed A03 supplied-result experiment.

Provider operands come from inputs, never from comparison oracles. This driver
does not change the runtime, source definitions, authority or sealed oracles.
"""
from dataclasses import fields, is_dataclass, replace
from enum import Enum
import hashlib
import json
import os
from pathlib import Path
import sys

from adapter.planner import codec as c, core, gates, model as m

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
SEALED = OUT.with_name('E2_P05_A03_PROSPECTIVE_OCCURRENCE_CONTRACT_1')
PLANS = ROOT / 'docs/plans'
REPORT_PATH = PLANS / 'DETERMINISTIC_PLANNER_V0_1_E2_P05_A03_PROSPECTIVE_OCCURRENCE_CONTRACT_1.json'
LABELS = {
    'QUALIFICATION_TYPE': 'PROSPECTIVE_REPLACEMENT',
    'ORIGINAL_HISTORICAL_OCCURRENCE': 'UNPROVEN',
    'ORIGINAL_A03_HISTORICAL_OCCURRENCE': 'UNPROVEN',
    'HISTORICAL_RECONSTRUCTION': 'NO',
    'PROSPECTIVE_EVENT_IS_ORIGINAL_EVENT': 'NO',
}
STATE = {'phase': 'ENTRY', 'state_id': None, 'event_id': None}


class Divergence(Exception):
    def __init__(self, name, expected, actual, classification='SEALED_ORACLE_DIVERGENCE'):
        self.name, self.expected, self.actual = name, expected, actual
        self.classification = classification
        super().__init__(name)


def read(path):
    return json.loads(Path(path).read_bytes())


def uid(value):
    return None if value is None else value.namespace + ':' + value.sha256


def identity(value):
    namespace, digest = value.split(':', 1)
    return m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY, namespace, digest)


def typed(value):
    """Encode Computation without inventing a native persisted type."""
    if isinstance(value, Enum):
        return {'type': type(value).__name__, 'value': value.value}
    if is_dataclass(value):
        if type(value).__name__ in c.TYPES and c.TYPES[type(value).__name__] is type(value):
            return c._wire(value)
        return {'type': type(value).__name__, **{f.name: typed(getattr(value, f.name)) for f in fields(value)}}
    if isinstance(value, (tuple, list)):
        return [typed(item) for item in value]
    if isinstance(value, dict):
        return {str(key): typed(item) for key, item in value.items()}
    if value is None or type(value) in (str, bool, int):
        return value
    raise TypeError('Unsupported comparison value ' + type(value).__name__)


def equal(name, actual, expected, classification='SEALED_ORACLE_DIVERGENCE'):
    if actual != expected:
        raise Divergence(name, expected, actual, classification)


def jbytes(value):
    return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + '\n').encode('utf-8')


def write(path, value):
    path = Path(path)
    raw = jbytes(value)
    if path.exists():
        equal('IMMUTABLE_EXECUTION_EVIDENCE', path.read_bytes(), raw, 'OUTPUT_CONFLICT')
        return path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)
    return path


def pin(path):
    path = Path(path)
    return {'path': str(path.relative_to(ROOT)), 'raw_sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def verify_entry():
    entry = read(OUT / 'entry-gate.json')
    equal('ENTRY_GATE', entry['result'], 'PASS')
    equal('CONTRACT_REPORT_PIN', hashlib.sha256(REPORT_PATH.read_bytes()).hexdigest(), entry['contract_report_sha256'])
    equal('CONTRACT_MARKDOWN_PIN', hashlib.sha256(REPORT_PATH.with_suffix('.md').read_bytes()).hexdigest(), entry['contract_markdown_sha256'])
    for name, digest in {**entry['checked_file_pins'], **entry['runtime_file_pins'], **entry['contract_directory_file_pins']}.items():
        equal('SEALED_FILE:' + name, hashlib.sha256((ROOT / name).read_bytes()).hexdigest(), digest)
    report = read(REPORT_PATH)
    seal = read(SEALED / 'seal.json')
    for key, value in LABELS.items():
        if key in report:
            equal('LABEL:' + key, report[key], value)
    for key, value in [('RESULT', 'PASS'), ('PROSPECTIVE_A03_EXECUTION_READY', 'YES'),
                       ('PROSPECTIVE_A03_EXECUTED', 'NO'), ('N12_MAPPING_PRESERVED', 'YES'),
                       ('N13_MAPPING_PRESERVED', 'YES'),
                       ('SELECTED_OPTION', 'AUTHORIZE_PROSPECTIVE_P05_A03_OCCURRENCE_QUALIFICATION')]:
        equal('CONTRACT:' + key, report[key], value)
    equal('ADDITIONAL_AUTHORITY_REQUIRED', seal['additional_authority_required'], False)
    capture = read(SEALED / 'authorization-capture.json')
    equal('AUTHORIZATION', capture['scope_authentication_result'], 'PASS')
    equal('AUTHORIZATION_OPTION', capture['selected_option'], report['SELECTED_OPTION'])
    equal('OPERATING_AUTHORITY_REQUIRED', capture['native_operating_authority_required'], False)
    equal('NATIVE_AUTHORITIES_ISSUED', capture['native_authorities_issued'], 0)
    return report


def load_start():
    report = verify_entry()
    start = report['PROSPECTIVE_START']
    bundle = c.restore(ROOT / start['start_bundle']['path'], identity(start['START_BUNDLE_ID']), ROOT)
    equal('START_STATE', uid(c.snapshot_id(bundle.current)), start['START_STATE_ID'])
    equal('START_EVENTS', len(bundle.events), 0)
    equal('START_CONTEXT', c._wire(bundle.current.context), start['context'])
    equal('START_LEDGER', uid(c.bundle_id(bundle)) + '#/bundle/events', start['LEDGER_ID'])
    return bundle


def computation(snapshot):
    computed = core.recompute(snapshot)
    return {
        'full_computation': typed(computed),
        'actionable': sorted(x.value for x in computed.actionable),
        'selected': computed.selection.selected.value if computed.selection else None,
        'control': computed.control.value if computed.control else None,
        'defects': list(computed.defects),
    }


def check_computation(snapshot, oracle, name):
    actual = computation(snapshot)
    for field in ('actionable', 'selected', 'control'):
        equal(name + ':' + field, actual[field], oracle[field])
    equal(name + ':defects', actual['defects'], [])
    return actual


def permute(value, presentation):
    """Presentation-only permutations of the native codec's declared sets."""
    if is_dataclass(value):
        kwargs = {}
        for field in fields(value):
            item = permute(getattr(value, field.name), presentation)
            if field.name in c.SET_FIELDS.get(type(value), set()) and isinstance(item, tuple):
                if presentation == 'Reversed':
                    item = tuple(reversed(item))
                elif presentation == 'Rotated' and item:
                    item = item[1:] + item[:1]
            kwargs[field.name] = item
        return replace(value, **kwargs)
    if isinstance(value, tuple):
        return tuple(permute(item, presentation) for item in value)
    return value


def permute_keys(value, presentation):
    if isinstance(value, dict):
        keys = list(value)
        if presentation == 'Reversed':
            keys.reverse()
        elif presentation == 'Rotated' and keys:
            keys = keys[1:] + keys[:1]
        return {key: permute_keys(value[key], presentation) for key in keys}
    if isinstance(value, list):
        return [permute_keys(item, presentation) for item in value]
    return value


def provide_result(snapshot, provider_path):
    """Fresh native operand from the allowlisted authored input provider."""
    inventory = read(SEALED / 'input-inventory.json')
    allowed = ROOT / inventory['bounded_result_producer']['source']['path']
    equal('PROVIDER_ALLOWLIST', str(Path(provider_path).resolve()), str(allowed.resolve()), 'INPUT_SEPARATION')
    equal('PROVIDER_BYTES', hashlib.sha256(allowed.read_bytes()).hexdigest(), inventory['bounded_result_producer']['source']['raw_sha256'])
    provider = read(allowed)
    selected = core.recompute(snapshot).selection.selected
    declaration = next(item for item in provider['declarations'] if item['id'] == selected.value)
    equal('PROVIDER_OPERATION_ORDER', selected.value in provider['invocation_order'], True)
    action = next(action for action in snapshot.actions if action.id == selected)
    packet_path = ROOT / action.source.path
    equal('ACTION_SOURCE_PIN', hashlib.sha256(packet_path.read_bytes()).hexdigest(), action.source.identity.sha256)
    packet = read(packet_path)
    equal('PROVIDER_SOURCE_DECLARATION', declaration in packet['action_declarations'], True)
    for field in ('scope', 'lineage', 'generation'):
        equal('PROVIDER_CONTEXT:' + field, declaration[field], getattr(snapshot.context, field))
    equal('PROVIDER_OPERATING_AUTHORITY', action.authority, None)
    output = declaration['output']
    record = m.KnowledgeRecord(
        m.KnowledgeId(output['id']), m.KnowledgeState.KNOWN_COMPLETE,
        output['statement'], action.source, (), m.ValidationState.ACCEPTED,
        m.ActionId(output['producer']), m.ActionResult(output['outcome']))
    supplied = m.SuppliedResult(action.id, m.ActionResult(declaration['accepted_result']),
                                (record,), expected_snapshot=c.snapshot_id(snapshot))
    m.validate_types(supplied, m.SuppliedResult)
    gates.validate_result(action, supplied)
    return supplied, {
        'ActionId': action.id.value, 'kind': 'Fresh bounded synthetic SuppliedResult',
        'provider_files_read': [str(allowed.relative_to(ROOT)), str(packet_path.relative_to(ROOT))],
        'oracle_files_read_by_provider': [], 'copied_saved_actual_result': False,
        'expected_pre_state': uid(supplied.expected_snapshot),
        'native_operating_authority': None, 'external_world_execution_claim': False,
    }


def boundary(bundle, name, persisted_path):
    return {
        'boundary': name, 'bundle_id': uid(c.bundle_id(bundle)),
        'state_id': uid(c.snapshot_id(bundle.current)),
        'ledger_id': uid(c.bundle_id(bundle)) + '#/bundle/events',
        'lineage_ledger_anchor': read(SEALED / 'prospective-start.json')['LEDGER_ID'],
        'ledger_root': uid(bundle.events[0].identity) if bundle.events else None,
        'append_head': uid(bundle.events[-1].identity) if bundle.events else None,
        'event_count': len(bundle.events), 'context': c._wire(bundle.current.context),
        'bundle': pin(persisted_path), 'computation': computation(bundle.current),
    }


def event_trace(event, bundle, event_path, invocation):
    return {
        **LABELS, 'EVENT_ID': uid(event.identity), 'EVENT_TYPE': type(event).__name__,
        'EVENT_PAYLOAD': c._wire(event.result), 'native_event': c._wire(event),
        'PARENT_EVENT_ID': uid(event.parent_event), 'PRE_STATE_ID': uid(event.parent_snapshot),
        'POST_STATE_ID': uid(event.after_snapshot), 'RESULT_BINDINGS': c._wire(event.result),
        'OUTPUT_BINDINGS': [c._wire(record) for record in event.result.knowledge],
        'LEDGER_ID': uid(c.bundle_id(bundle)) + '#/bundle/events',
        'lineage_ledger_anchor': read(SEALED / 'prospective-start.json')['LEDGER_ID'],
        'LEDGER_POSITION': event.sequence, 'SCOPE': bundle.current.context.scope,
        'LINEAGE': bundle.current.context.lineage, 'GENERATION': bundle.current.context.generation,
        'PROVENANCE': [c._wire(record.provenance) for record in event.result.knowledge],
        'durable_event_file': pin(event_path), 'provider_invocation': invocation,
        'admission': 'codec.commit_event', 'actual_native_transaction': True,
        'no_external_world_executor_claim': True,
    }


def writer(name, presentation):
    run = OUT / name
    equal('UNEXECUTED_WRITER_STORE', run.exists(), False, 'RETRY_REQUIRES_AUDIT')
    bundle = load_start()
    original = c.bundle_bytes(bundle)
    bundle = permute(c._unwire(permute_keys(c._wire(bundle), presentation)), presentation)
    equal('UNORDERED_START_BYTES', c.bundle_bytes(bundle), original)
    report = read(REPORT_PATH)
    start = report['PROSPECTIVE_START']
    events = read(SEALED / 'oracles/expected-events.json')['event_oracles']
    results = read(SEALED / 'oracles/expected-results.json')['result_oracles']
    check_computation(bundle.current, start['entry_oracle'], 'START')
    before_selection = c.bundle_bytes(bundle)
    twice = [computation(bundle.current), computation(bundle.current)]
    equal('N12_RECOMPUTATION', twice[0], twice[1])
    equal('N12_CANONICAL_UNCHANGED', c.bundle_bytes(bundle), before_selection)
    run.mkdir(parents=True)
    initial_path = ROOT / start['start_bundle']['path']
    boundaries = [boundary(bundle, 'SEALED_START', initial_path)]
    traces, heads = [], []
    provider_path = ROOT / read(SEALED / 'input-inventory.json')['bounded_result_producer']['source']['path']
    for index, action_name in enumerate(read(provider_path)['invocation_order']):
        STATE.update(phase=action_name, state_id=uid(c.snapshot_id(bundle.current)))
        equal('SELECTED_ACTION', computation(bundle.current)['selected'], action_name)
        supplied, invocation = provide_result(bundle.current, provider_path)
        supplied = permute(supplied, presentation)
        # Independent sealed comparison only; never feed an oracle to the provider.
        expected_event = c._unwire(events[index]['expected_native_wire'])
        equal('ACTUAL_SUPPLIED_RESULT', c._wire(supplied), c._wire(expected_event.result))
        current_id = c.bundle_id(bundle)
        updated, updated_id = c.commit_event(bundle, supplied, run / 'native-head', ROOT)
        STATE.update(state_id=uid(c.snapshot_id(updated.current)), event_id=uid(updated.events[-1].identity))
        equal('ACTUAL_EVENT', c._wire(updated.events[-1]), c._wire(expected_event))
        equal('ACTUAL_POST_STATE', c._wire(updated.current), results[index]['post_state'])
        equal('POST_STATE_ID', uid(c.snapshot_id(updated.current)), results[index]['POST_STATE_ID'])
        expected_boundary = report['PERSISTENCE_CONTRACT']['boundaries'][index]
        equal('POST_BUNDLE_ID', uid(updated_id), expected_boundary['native_bundle_id'])
        check_computation(updated.current, results[index], action_name + '_POST')
        head = read(run / 'native-head/HEAD.json')
        equal('HEAD_PREVIOUS', c._unwire(head['previous']), current_id)
        equal('HEAD_COMMAND', head['command'], None)
        equal('HEAD_BUNDLE', c._unwire(head['bundle']), updated_id)
        equal('NATIVE_HEAD_AUDIT', c.bundle_id(c._read_head(run / 'native-head', bundle, ROOT)), updated_id)
        checkpoint = 'post-check' if index == 0 else 'post-collect'
        checkpoint_path, checkpoint_id = c.save_bundle(updated, run / 'checkpoints' / checkpoint, ROOT)
        equal('CHECKPOINT_ID', checkpoint_id, updated_id)
        native_event_path = run / 'native-head' / ('event-' + updated.events[-1].identity.sha256 + '.json')
        traces.append(event_trace(updated.events[-1], updated, native_event_path, invocation))
        heads.append({'after': action_name, 'head': head})
        boundaries.append(boundary(updated, expected_boundary['boundary'], checkpoint_path))
        bundle = updated
    equal('EXACT_NATIVE_EVENT_COUNT', len(bundle.events), 2)
    equal('NO_EXTRA_ACTIONS_EXECUTED', sorted(row.id.value for row in bundle.current.statuses if row.state is m.ActionState.COMPLETED), ['E2-CHECK', 'E2-COLLECT'])
    result = {**LABELS, 'result': 'PASS', 'kind': 'Actual new native A03 result transactions',
              'writer': name, 'presentation': presentation, 'hash_seed': os.environ.get('PYTHONHASHSEED'),
              'PID': os.getpid(), 'canonical_P04_modified': False, 'native_authorities_issued': 0,
              'commit_event_calls': 2, 'provider_invocations': 2, 'N12_read_only': 'PASS',
              'N12_checks': twice, 'boundaries': boundaries, 'events': traces,
              'HEAD_publications': heads, 'overall_occurrence_verdict': 'PENDING_READER_REPLAY_NEGATIVES'}
    write(run / 'writer-result.json', result)
    print(json.dumps({'result': 'PASS', 'writer': name, 'events': len(traces), 'final_bundle': boundaries[-1]['bundle_id']}))


def reader(checkpoint, seed, number):
    verify_entry()
    primary = read(OUT / 'writer-main/writer-result.json')
    expected = next(item for item in primary['boundaries'] if item['boundary'] == checkpoint)
    path = ROOT / expected['bundle']['path']
    bundle = c.restore(path, identity(expected['bundle_id']), ROOT)
    actual = boundary(bundle, checkpoint, path)
    equal('COLD_BOUNDARY', actual, expected)
    replayed = c._replay(bundle)
    equal('REPLAY_CURRENT', c._wire(replayed), c._wire(bundle.current))
    equal('REPLAY_COMPUTATION', computation(replayed), expected['computation'])
    prefix_checks = []
    for count in range(len(bundle.events) + 1):
        prefix = c._prefix_bundle(bundle, count)
        target = primary['boundaries'][count]
        equal('REPLAY_PREFIX_STATE', uid(c.snapshot_id(prefix.current)), target['state_id'])
        equal('REPLAY_PREFIX_BUNDLE', uid(c.bundle_id(prefix)), target['bundle_id'])
        equal('REPLAY_PREFIX_COMPUTATION', computation(c._replay(prefix)), target['computation'])
        prefix_checks.append({'event_count': count, 'bundle_id': target['bundle_id'], 'result': 'PASS'})
    restored_start = load_start()
    if bundle.events:
        audited = c._read_head(OUT / 'writer-main/native-head', restored_start, ROOT)
        equal('RESTORED_MAIN_HEAD', uid(c.bundle_id(audited)), primary['boundaries'][-1]['bundle_id'])
    result = {**LABELS, 'result': 'PASS', 'checkpoint': checkpoint, 'hash_seed': seed,
              'reader_number': number, 'PID': os.getpid(), 'boundary': actual,
              'replay_prefix_checks': prefix_checks, 'replay_provider_invocations': 0,
              'actual_result_transactions_executed': 0, 'native_authorities_issued': 0,
              'writer_memory_used': False, 'writer_process_already_terminated': True,
              'historical_original_proven': False, 'END_mapping_labels': 'SEPARATE_UNPROVEN_ORIGINAL'}
    write(OUT / 'cold-readers' / ('seed-' + seed) / (checkpoint.lower() + '-' + number + '.json'), result)
    print(json.dumps({'result': 'PASS', 'checkpoint': checkpoint, 'hash_seed': seed, 'reader': number}))


def main():
    if sys.argv[1] == 'writer':
        writer(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'reader':
        reader(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        raise ValueError('Unknown mode')


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        record = {**LABELS, 'result': 'FAIL', 'FIRST_COUNTEREXAMPLE': getattr(exc, 'name', type(exc).__name__),
                  'EXPECTED': typed(exc.expected) if isinstance(exc, Divergence) and not isinstance(exc.expected, bytes) else repr(getattr(exc, 'expected', None)),
                  'ACTUAL': typed(exc.actual) if isinstance(exc, Divergence) and not isinstance(exc.actual, bytes) else repr(getattr(exc, 'actual', str(exc))),
                  'STATE_ID': STATE['state_id'], 'EVENT_ID': STATE['event_id'], 'phase': STATE['phase'],
                  'CLASSIFICATION': getattr(exc, 'classification', 'EXECUTION_DRIVER_ERROR'), 'no_live_repair': True}
        write(OUT / 'STOP.json', record)
        print(json.dumps(record, sort_keys=True))
        raise
