"""Exercise the sealed negatives and read-only prospective END mapping."""
from dataclasses import replace
import hashlib
import json
from pathlib import Path
import shutil
import sys

import execution_driver as d
from adapter.planner import codec as c, core, model as m


def store_hashes(directory):
    return {str(path.relative_to(directory)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in directory.rglob('*') if path.is_file()}


def primary_evidence():
    return {**d.LABELS, 'kind': 'NATIVE_ADMITTED_TRANSACTION',
            'writer_report': str((d.OUT / 'writer-main/writer-result.json').relative_to(d.ROOT)),
            'native_head_directory': str((d.OUT / 'writer-main/native-head').relative_to(d.ROOT)),
            'original_historical_event_ids': None, 'original_history_splice': False,
            'lineage': d.read(d.SEALED / 'prospective-start.json')['lineage'],
            'scope': d.read(d.SEALED / 'prospective-start.json')['scope'],
            'generation': d.read(d.SEALED / 'prospective-start.json')['generation']}


def validate_occurrence_evidence(evidence):
    """Contract evidence guard, not an invented native END consumer API."""
    if not isinstance(evidence, dict) or evidence.get('kind') != 'NATIVE_ADMITTED_TRANSACTION':
        raise m.PlannerError('NATIVE_OCCURRED_TRANSACTION_REQUIRED')
    for key, value in d.LABELS.items():
        if evidence.get(key) != value:
            raise m.PlannerError('HISTORICAL_LABEL_SEPARATION_REQUIRED:' + key)
    if evidence.get('original_historical_event_ids') is not None or evidence.get('original_history_splice') is not False:
        raise m.PlannerError('ORIGINAL_EVENT_IDENTITY_SUBSTITUTION_FORBIDDEN')
    start = d.read(d.SEALED / 'prospective-start.json')
    for key in ('lineage', 'scope', 'generation'):
        if evidence.get(key) != start[key]:
            raise m.PlannerError('PROSPECTIVE_CONTEXT_REQUIRED:' + key)
    report_path = d.ROOT / evidence.get('writer_report', 'MISSING_NATIVE_WRITER')
    head_dir = d.ROOT / evidence.get('native_head_directory', 'MISSING_NATIVE_HEAD')
    if not report_path.is_file() or not (head_dir / 'HEAD.json').is_file():
        raise m.PlannerError('ACTUAL_WRITER_AND_PUBLISHED_HEAD_REQUIRED')
    writer = d.read(report_path)
    if writer.get('commit_event_calls') != 2 or writer.get('provider_invocations') != 2:
        raise m.PlannerError('ACTUAL_NATIVE_RESULT_ADMISSION_REQUIRED')
    for key, value in d.LABELS.items():
        if writer.get(key) != value:
            raise m.PlannerError('WRITER_LABEL_MISMATCH')
    if any(item['provider_invocation']['oracle_files_read_by_provider'] for item in writer['events']):
        raise m.PlannerError('ORACLE_IS_NOT_A_RESULT_OPERAND')
    if any(not item['actual_native_transaction'] for item in writer['events']):
        raise m.PlannerError('ACTUAL_NATIVE_RESULT_ADMISSION_REQUIRED')
    head = d.read(head_dir / 'HEAD.json')
    bundle_identity = c._unwire(head['bundle'])
    bundle_path = head_dir / ('bundle-' + bundle_identity.sha256 + '.json')
    bundle = c.restore(bundle_path, bundle_identity, d.ROOT)
    sealed_start = d.load_start()
    c._read_head(head_dir, sealed_start, d.ROOT)
    if c._wire(bundle.initial) != c._wire(sealed_start.initial):
        raise m.PlannerError('EXACT_PROSPECTIVE_LEDGER_REQUIRED')
    expected = d.read(d.SEALED / 'oracles/expected-events.json')['event_oracles']
    if len(bundle.events) != len(expected) or len(writer['events']) != len(expected):
        raise m.PlannerError('EXACT_TWO_EVENT_LEDGER_REQUIRED')
    for index, event in enumerate(bundle.events):
        if c._wire(event) != expected[index]['expected_native_wire']:
            raise m.PlannerError('SEALED_EVENT_ORACLE_REQUIRED')
        trace = writer['events'][index]
        if trace['native_event'] != c._wire(event):
            raise m.PlannerError('WRITER_LEDGER_PAYLOAD_MISMATCH')
        event_path = d.ROOT / trace['durable_event_file']['path']
        if event_path.read_bytes() != c.canonical_bytes(c._wire(event)):
            raise m.PlannerError('NATIVE_EVENT_ARTIFACT_REQUIRED')
        if trace['LEDGER_POSITION'] != index + 1 or trace['lineage_ledger_anchor'] != start['LEDGER_ID']:
            raise m.PlannerError('EXACT_LEDGER_POSITION_REQUIRED')
    return bundle


def scope_guard(bundle, capture):
    expected = d.read(d.SEALED / 'authorization-capture.json')
    if capture != expected:
        raise m.PlannerError('EXACT_SCOPE_DECISION_REQUIRED')
    for action in bundle.current.actions:
        if action.id.value in ('E2-CHECK', 'E2-COLLECT') and action.authority is not None:
            raise m.PlannerError('UNAUTHORIZED_OPERATING_AUTHORITY_SUBSTITUTION')
    if c._wire(bundle.current.context) != d.read(d.SEALED / 'prospective-start.json')['context']:
        raise m.PlannerError('EXACT_PROSPECTIVE_CONTEXT_REQUIRED')


def context_guard(bundle):
    scope_guard(bundle, d.read(d.SEALED / 'authorization-capture.json'))
    if d.uid(c.bundle_id(bundle)) != d.read(d.SEALED / 'prospective-start.json')['START_BUNDLE_ID']:
        raise m.PlannerError('EXACT_SEALED_START_REQUIRED')


def negatives():
    d.verify_entry()
    contract = d.read(d.SEALED / 'negative-contract.json')
    positive_before = store_hashes(d.OUT / 'writer-main')
    start = d.load_start()
    primary = d.read(d.OUT / 'writer-main/writer-result.json')
    final_row = primary['boundaries'][-1]
    final = c.restore(d.ROOT / final_row['bundle']['path'], d.identity(final_row['bundle_id']), d.ROOT)
    provider = d.ROOT / d.read(d.SEALED / 'input-inventory.json')['bounded_result_producer']['source']['path']
    good, _ = d.provide_result(start.current, provider)
    capture = d.read(d.SEALED / 'authorization-capture.json')
    cases = []
    for spec in contract['cases']:
        name = spec['name']
        d.STATE.update(phase=spec['id'], state_id=d.uid(c.snapshot_id(start.current)), event_id=None)
        case_dir = d.OUT / 'negatives' / spec['id']
        case_dir.mkdir(parents=True, exist_ok=False)
        original = c.bundle_bytes(start)
        before_files = store_hashes(case_dir)
        attempts = []

        def rejects(label, operation):
            try:
                operation()
            except m.PlannerError as exc:
                attempts.append({'variant': label, 'rejected': True, 'reason': str(exc)})
                return
            except d.Divergence as exc:
                attempts.append({'variant': label, 'rejected': True,
                                 'reason': exc.name, 'layer': exc.classification})
                return
            raise d.Divergence(spec['id'] + ':' + label, 'REJECT', 'ACCEPTED', 'SEALED_NEGATIVE_COUNTEREXAMPLE')

        def commit_bad(supplied):
            return c.commit_event(start, supplied, case_dir / 'native-head', d.ROOT)

        if name == 'wrong_A03_input':
            rejects('wrong selected Action', lambda: commit_bad(replace(good, action=m.ActionId('E2-COLLECT'))))
            rejects('oracle instead of allowlisted input', lambda: d.provide_result(start.current, d.SEALED / 'oracles/expected-results.json'))
        elif name == 'wrong_result':
            rejects('FAIL instead of PASS', lambda: commit_bad(replace(good, result=m.ActionResult.FAIL)))
        elif name == 'wrong_output':
            record = good.knowledge[0]
            for label, knowledge in [('missing', ()), ('wrong ID', (replace(record, id=m.KnowledgeId('FOREIGN-KNOWLEDGE')),)),
                                     ('wrong producer', (replace(record, producer=m.ActionId('E2-COLLECT')),)),
                                     ('extra', good.knowledge + (replace(record, id=m.KnowledgeId('EXTRA-OUTPUT')),))]:
                rejects(label, lambda knowledge=knowledge: commit_bad(replace(good, knowledge=knowledge)))
        elif name == 'wrong_parent':
            for index in (0, 1):
                events = list(final.events)
                events[index] = replace(events[index], parent_event=events[index].identity)
                rejects('parent at sequence ' + str(index + 1), lambda events=events: c.bundle_bytes(replace(final, events=tuple(events))))
        elif name == 'wrong_pre_state':
            wrong = m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY, 'planner-snapshot-v1', '0' * 64)
            rejects('foreign expected_snapshot', lambda: commit_bad(replace(good, expected_snapshot=wrong)))
        elif name == 'wrong_event_payload':
            event = final.events[0]
            tampered = replace(event, result=replace(event.result, result=m.ActionResult.FAIL))
            rejects('retain trusted event ID with altered payload', lambda: c.bundle_bytes(replace(final, events=(tampered,) + final.events[1:])))
        elif name == 'wrong_ledger':
            other_initial = replace(final.initial, context=replace(final.initial.context, lineage='FOREIGN-LINEAGE'))
            rejects('move events to foreign initial ledger', lambda: c.bundle_bytes(replace(final, initial=other_initial)))
            rejects('foreign sealed start coordinate', lambda: context_guard(replace(start, sources=start.sources[:-1])))
        elif name == 'wrong_append_position':
            rejects('skip sequence', lambda: c.bundle_bytes(replace(final, events=(replace(final.events[0], sequence=2), final.events[1]))))
            rejects('reverse chronology', lambda: c.bundle_bytes(replace(final, events=tuple(reversed(final.events)))))
            rejects('duplicate semantic event', lambda: c.bundle_bytes(replace(final, events=final.events + (final.events[-1],))))
        elif name == 'wrong_authority':
            rejects('GENESIS replaces selected scope', lambda: scope_guard(start, dict(capture, selected_option='AUTHORIZE_GENESIS')))
            actions = tuple(replace(a, authority=m.PredicateId('FOREIGN-AUTHORITY')) if a.id == good.action else a for a in start.current.actions)
            rejects('add operating grant to CHECK', lambda: scope_guard(replace(start, current=replace(start.current, actions=actions)), capture))
        elif name in ('wrong_scope', 'wrong_lineage', 'wrong_generation'):
            field = name.split('_', 1)[1]
            context = replace(start.current.context, **{field: 'FOREIGN-' + field.upper()})
            rejects('change ' + field, lambda: context_guard(replace(start, initial=replace(start.initial, context=context), current=replace(start.current, context=context))))
        elif name == 'wrong_provenance':
            changed = replace(good.knowledge[0], provenance=replace(good.knowledge[0].provenance, method='FOREIGN-PROVENANCE'))
            rejects('KnowledgeRecord provenance changed', lambda: commit_bad(replace(good, knowledge=(changed,))))
        elif name == 'foreign_event':
            event = final.events[0]
            foreign = replace(event, parent_snapshot=m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY, 'planner-snapshot-v1', '1' * 64))
            rejects('same named Action foreign event', lambda: c.bundle_bytes(replace(final, events=(foreign, final.events[1]))))
            rejects('foreign mapping lineage', lambda: validate_occurrence_evidence(dict(primary_evidence(), lineage='FOREIGN-LINEAGE')))
        elif name == 'event_without_actual_A03_admission':
            rejects('oracle descriptor without writer/head', lambda: validate_occurrence_evidence({**d.LABELS, 'kind': 'EXPECTED_ORACLE_ONLY_NOT_OCCURRED'}))
        elif name == 'snapshot_as_occurrence':
            rejects('Snapshot only', lambda: validate_occurrence_evidence(final.current))
        elif name == 'report_as_occurrence':
            rejects('PASS report only', lambda: validate_occurrence_evidence({'result': 'PASS', 'kind': 'REPORT_METADATA'}))
        elif name == 'prospective_labeled_historical':
            rejects('historical PROVEN claim', lambda: validate_occurrence_evidence(dict(primary_evidence(), ORIGINAL_HISTORICAL_OCCURRENCE='PROVEN')))
            rejects('historical reconstruction claim', lambda: validate_occurrence_evidence(dict(primary_evidence(), HISTORICAL_RECONSTRUCTION='YES')))
        elif name == 'prospective_bound_as_original_identity':
            rejects('put replacement IDs in original slot', lambda: validate_occurrence_evidence(dict(primary_evidence(), original_historical_event_ids=[d.uid(e.identity) for e in final.events])))
            rejects('splice history', lambda: validate_occurrence_evidence(dict(primary_evidence(), original_history_splice=True)))
        elif name == 'selection_as_execution_N12':
            first, second = core.recompute(start.current), core.recompute(start.current)
            d.equal('N12_READ_ONLY_IDENTICAL', d.typed(first), d.typed(second))
            d.equal('N12_EMPTY_LEDGER_UNCHANGED', c.bundle_bytes(start), original)
            rejects('SelectionTrace as result', lambda: commit_bad(first.selection))
            rejects('selection as occurrence', lambda: validate_occurrence_evidence({'kind': 'SelectionTrace', 'selected': first.selection.selected.value}))
        elif name == 'output_declaration_as_result_N13':
            action = next(a for a in start.current.actions if a.id == good.action)
            rejects('Action declaration as result', lambda: commit_bad(action))
            rejects('KnowledgeRecord as result', lambda: commit_bad(action.accepted_inventory[0]))
            rejects('source output declaration as result', lambda: commit_bad(d.read(provider)['declarations'][0]['output']))
        elif name == 'oracle_loaded_as_operand':
            rejects('oracle provider path', lambda: d.provide_result(start.current, d.SEALED / 'oracles/expected-events.json'))
            rejects('expected event as result', lambda: commit_bad(c._unwire(d.read(d.SEALED / 'oracles/expected-events.json')['event_oracles'][0]['expected_native_wire'])))
        elif name == 'duplicate_KnowledgeId':
            rejects('duplicate identical KnowledgeId', lambda: commit_bad(replace(good, knowledge=good.knowledge + good.knowledge)))
        elif name == 'repeat_committed_command':
            shutil.copytree(d.OUT / 'writer-main/native-head', case_dir / 'native-head')
            before_files = store_hashes(case_dir)
            rejects('resubmit start operand against committed head', lambda: commit_bad(good))
        else:
            raise ValueError('Unknown sealed negative ' + name)
        after_files = store_hashes(case_dir)
        # Native locking may create a zero-length LOCK file; no semantic output.
        new_semantic_files = sorted(key for key in after_files if key not in before_files and not key.endswith('/LOCK'))
        changed_files = sorted(key for key in before_files if after_files.get(key) != before_files[key])
        d.equal(spec['id'] + ':NO_DURABLE_SUCCESSOR', new_semantic_files, [])
        d.equal(spec['id'] + ':EXISTING_FILES_UNCHANGED', changed_files, [])
        d.equal(spec['id'] + ':START_STATE_UNCHANGED', c.bundle_bytes(start), original)
        d.equal(spec['id'] + ':POSITIVE_LINEAGE_UNCHANGED', store_hashes(d.OUT / 'writer-main'), positive_before)
        cases.append({**d.LABELS, 'id': spec['id'], 'name': name, 'sealed_layer': spec['layer'],
                      'expected': spec['expected'], 'result': 'PASS', 'attempts': attempts,
                      'durable_partial_state': False, 'native_result_events_added': 0,
                      'positive_lineage_modified': False, 'original_state_unchanged': True})
        d.write(case_dir / 'result.json', cases[-1])
    result = {**d.LABELS, 'result': 'PASS', 'count': len(cases),
              'variants_rejected': sum(len(row['attempts']) for row in cases), 'cases': cases,
              'N12_MAPPING': 'PASS', 'N13_MAPPING': 'PASS', 'P05_cases_executed': False,
              'sealed_P05_16_negatives_changed': False, 'native_authorities_issued': 0,
              'native_result_events_added': 0, 'positive_lineage_unchanged': True}
    d.write(d.OUT / 'negative-results.json', result)
    print(json.dumps({'result': 'PASS', 'negative_controls': len(cases), 'variants_rejected': result['variants_rejected'], 'N12': 'PASS', 'N13': 'PASS'}))


def main():
    if sys.argv[1] == 'negatives':
        negatives()
    else:
        raise ValueError('Unknown mode')


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        record = {**d.LABELS, 'result': 'FAIL', 'FIRST_COUNTEREXAMPLE': getattr(exc, 'name', type(exc).__name__),
                  'EXPECTED': repr(getattr(exc, 'expected', None)),
                  'ACTUAL': repr(getattr(exc, 'actual', str(exc))),
                  'STATE_ID': d.STATE['state_id'], 'EVENT_ID': d.STATE['event_id'],
                  'phase': d.STATE['phase'], 'CLASSIFICATION': getattr(exc, 'classification', 'QUALIFICATION_DRIVER_ERROR'),
                  'no_live_repair': True}
        d.write(d.OUT / 'STOP.json', record)
        print(json.dumps(record, sort_keys=True))
        raise
