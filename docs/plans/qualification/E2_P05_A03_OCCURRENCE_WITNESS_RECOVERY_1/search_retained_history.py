"""Inspect existing bytes only. Never construct, admit, apply or replay an event."""
import collections
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
TARGET_ACTIONS = {'E2-CHECK', 'E2-COLLECT'}
TARGET_KNOWLEDGE = {'E2-K-CHECK', 'E2-K-COLLECT'}
STATES = {
    '545ad19184d8dd7dfb5b2737e081b043d13982f05d05326939ac2cbb89bf54e2',
    'e381424d14336d918fd3bafff16698361395c77ef03fef628d7d74d36af8a9da',
    '6c7efb221870974d76d12d7ceb372369ef68104bb1f522a16d47f7dc37236677',
    '39114028d38b9571c46e211248644b09a3ac63ad9f47cd21a75fc922a2d152e3',
    '8985701af4db7bf08327dc5e455fcd9182ca71e7cfde7b2868c253b0e8bd2d5e',
    '9b3d8e6a074687a7aef9dca0279262cf2888492de73b7207768dc48bb0f5edfa',
    '8d77f7f1997ca884e07490c4c93f5fbe3a31b09278fd57c6c6ea1f9fa26b3aaf',
    # Earlier rejected/replaced P02 prefixes are searched, but not substituted.
    '71fe19caaeb0f7c10da8db2bbb5d849156c59cc521e3e11e4fffb8d578080db9',
    '973f3beb794f1161609604675e70a066d08d1365d3f25b9069feebb0cab6959c',
    'f2841f609a1f4636484132cbfa755cd8af071465d2af17866a3156aa1dfcd889',
    '33c0bb5c4ed55496cde6ec0ce3eb5ee74307872697d8202a06db65c2c731e9b5',
    'd220d3685ba2af01267be8fc158babd214c663169c0d298b989116ed155e5b35',
    '43a238851a34b2e58f4a49ec870fa258fdcb8d3a88fda50a305df2b570281e79',
}
EVENT_FIELDS = {'sequence', 'parent_snapshot', 'parent_event', 'result',
                'after_snapshot', 'identity'}
BUNDLE_FIELDS = {'initial', 'current', 'events', 'sources', 'policy'}
IDENTITY_BODY_FIELDS = {'sequence', 'parent', 'parent_event', 'result', 'after'}


def value(x):
    x = x.get('value') if isinstance(x, dict) else x
    return x if isinstance(x, str) else None


def sid(x):
    return x.get('sha256') if isinstance(x, dict) else x


def escape(x):
    return str(x).replace('~', '~0').replace('/', '~1')


def save(name, data):
    (OUT/name).write_text(json.dumps(data, sort_keys=True, indent=2)+'\n')


def main():
    paths = subprocess.run(['rg', '--files', 'docs/plans', '-g', '*.json',
        '-g', '*.jsonl', '-g', '*.ndjson', '-g', '!qualification/E2_P05_A03_OCCURRENCE_WITNESS_RECOVERY_1/**'],
        cwd=str(ROOT), check=True, capture_output=True, text=True).stdout.splitlines()
    # Content-based expansion outside plans. Frozen E1 is not an E2 history source.
    terms = sorted(TARGET_ACTIONS | TARGET_KNOWLEDGE | STATES)
    command = ['rg', '-l', '-F']
    for term in terms:
        command += ['-e', term]
    command += ['docs/experiments', 'adapter', '-g', '*.json', '-g', '*.jsonl',
                '-g', '*.ndjson', '-g', '!E1/**']
    extra = subprocess.run(command, cwd=str(ROOT), capture_output=True, text=True)
    if extra.returncode not in (0, 1):
        raise RuntimeError(extra.stderr)
    paths = sorted({p for p in paths+extra.stdout.splitlines()
                    if OUT not in (ROOT/p).parents and '/E1/' not in p})
    files, errors, bundles, heads, genesis_ledgers, identity_bodies = [], [], [], [], [], []
    events = {}
    supplied, reports, embedded_records = [], [], []
    markers = collections.Counter()
    recognized_schemas = collections.Counter()
    target_event_occurrences = []

    for name in paths:
        p = ROOT/name
        raw = p.read_bytes()
        file_pin = {'path':name, 'raw_sha256':hashlib.sha256(raw).hexdigest()}
        files.append(file_pin)
        if name.endswith(('.jsonl', '.ndjson')):
            documents = []
            for i, line in enumerate(raw.splitlines()):
                if not line.strip():
                    continue
                try:
                    documents.append((json.loads(line), '@line:'+str(i+1)))
                except (ValueError, UnicodeDecodeError) as exc:
                    errors.append(dict(file_pin, line=i+1, error=str(exc)))
        else:
            try:
                documents = [(json.loads(raw), '')]
            except (ValueError, UnicodeDecodeError) as exc:
                errors.append(dict(file_pin, error=str(exc)))
                continue
        queue = list(documents)
        while queue:
            doc, pointer = queue.pop()
            if isinstance(doc, dict):
                tag = doc.get('$type', doc.get('type'))
                if isinstance(tag, str):
                    markers[tag] += 1
                if isinstance(doc.get('schema'), str):
                    recognized_schemas[doc['schema']] += 1
                result = doc.get('result')
                if IDENTITY_BODY_FIELDS <= set(doc):
                    identity_bodies.append({'file':file_pin,'pointer':pointer,'body':doc,
                        'A03_Action':isinstance(result,dict) and value(result.get('action')) in TARGET_ACTIONS,
                        'classification':'EXPLICIT_NATIVE_IDENTITY_BODY; MEMBERSHIP_MUST_BE_PROVED_SEPARATELY'})
                if tag == 'ExecutionEvent' or EVENT_FIELDS <= set(doc):
                    action = value(result.get('action')) if isinstance(result, dict) else None
                    identity = doc.get('identity')
                    key = json.dumps(identity, sort_keys=True) if identity else hashlib.sha256(
                        json.dumps(doc, sort_keys=True).encode()).hexdigest()
                    if key not in events:
                        events[key] = {'identity':identity, 'sequence':doc.get('sequence'),
                            'event_type':result.get('$type', result.get('type')) if isinstance(result, dict) else type(result).__name__,
                            'action':action, 'parent_event':doc.get('parent_event'),
                            'pre_state':doc.get('parent_snapshot'), 'post_state':doc.get('after_snapshot'),
                            'occurrences':[]}
                    events[key]['occurrences'].append(dict(file_pin, pointer=pointer))
                    if action in TARGET_ACTIONS or sid(doc.get('parent_snapshot')) in STATES or sid(doc.get('after_snapshot')) in STATES:
                        target_event_occurrences.append({'file':file_pin,'pointer':pointer,'event':doc,
                            'target_Action':action in TARGET_ACTIONS,'original_or_earlier_prefix_state_match':
                            sid(doc.get('parent_snapshot')) in STATES or sid(doc.get('after_snapshot')) in STATES})
                if tag == 'PersistenceBundle' or BUNDLE_FIELDS <= set(doc):
                    current = doc.get('current', {})
                    initial = doc.get('initial', {})
                    history = doc.get('events', [])
                    ctx = current.get('context', {}) if isinstance(current, dict) else {}
                    ctx = ctx or {}
                    native_actions = [value(a.get('id')) for a in current.get('actions', [])]
                    result_actions = [value(e['result'].get('action')) for e in history
                        if isinstance(e, dict) and isinstance(e.get('result'), dict)]
                    chain_fields = all(isinstance(e, dict) and EVENT_FIELDS <= set(e) for e in history)
                    chain_links = chain_fields and all(e['parent_event'] == history[i-1]['identity'] and
                        e['parent_snapshot'] == history[i-1]['after_snapshot'] for i,e in enumerate(history) if i)
                    bundles.append({'file':file_pin,'pointer':pointer,'event_count':len(history),
                        'context':ctx,'declared_Actions':native_actions,'result_Actions':result_actions,
                        'A03_event_indices':[i for i,e in enumerate(history) if isinstance(e,dict) and
                            isinstance(e.get('result'),dict) and value(e['result'].get('action')) in TARGET_ACTIONS],
                        'original_prefix_state_event_indices':[i for i,e in enumerate(history) if isinstance(e,dict) and
                            (sid(e.get('parent_snapshot')) in STATES or sid(e.get('after_snapshot')) in STATES)],
                        'event_identity_chain_fields_complete':chain_fields,'parent_links_continuous':chain_links,
                        'append_head':history[-1].get('identity') if history else None,
                        'initial_completed_prefix':[value(s.get('id')) for s in initial.get('statuses',[]) if
                            value(s.get('state'))=='COMPLETED' and value(s.get('id')) in TARGET_ACTIONS]})
                if doc.get('schema') == 'PLANNER-HEAD-1':
                    heads.append(dict(file_pin, pointer=pointer, bundle=doc.get('bundle'),
                                      previous=doc.get('previous'), command=doc.get('command')))
                if tag=='GenesisLedger' or {'ledger_id','root','events','append_head'} <= set(doc):
                    history=doc.get('events',[])
                    genesis_ledgers.append({'file':file_pin,'pointer':pointer,
                        'ledger_id':doc.get('ledger_id'),'root':doc.get('root'),
                        'append_head':doc.get('append_head'),'pre_genesis_history':doc.get('pre_genesis_history'),
                        'event_count':len(history),'A03_event_indices':[i for i,e in enumerate(history)
                            if isinstance(e,dict) and isinstance(e.get('result'),dict) and
                            value(e['result'].get('action')) in TARGET_ACTIONS]})
                if tag == 'SuppliedResult' and value(doc.get('action')) in TARGET_ACTIONS:
                    supplied.append({'file':file_pin,'pointer':pointer,'value':doc,
                                     'class':'TYPED_RESULT_PAYLOAD; LEDGER_OCCURRENCE_NOT_IMPLIED'})
                report_action = value(doc.get('action', doc.get('action_executed', doc.get('selected'))))
                if report_action in TARGET_ACTIONS and tag not in ('Action', 'ActionStatus', 'SuppliedResult', 'KnowledgeRecord', 'GraphEntity'):
                    classification = ('REPORT_METADATA; NOT_NATIVE_EVENT' if
                        any(k in doc for k in ('pre_state','pre_state_id','post_state','post_state_id','result_identity','knowledge_produced','action_executed'))
                        else 'OTHER_REFERENCE_OR_DEFINITION; NOT_NATIVE_EVENT')
                    reports.append({'file':file_pin,'pointer':pointer,'value':doc,
                                    'classification':classification})
                for k,v in doc.items():
                    queue.append((v, pointer+'/'+escape(k)))
            elif isinstance(doc, list):
                for i,v in enumerate(doc):
                    queue.append((v,pointer+'/'+str(i)))
            elif isinstance(doc, str) and doc.startswith(('{','[')) and any(x in doc for x in
                    ('ExecutionEvent','PersistenceBundle','SuppliedResult','PLANNER-EVENT-1','PLANNER-HEAD-1')):
                try:
                    inner=json.loads(doc)
                except ValueError:
                    continue
                embedded_records.append(dict(file_pin,pointer=pointer))
                queue.append((inner,pointer+'@decoded-json'))

    save('search-corpus.json',{'scope':'Every retained JSON/JSONL/NDJSON artifact in docs/plans plus content-matched non-E1 experiment/adapter artifacts; recovery outputs excluded.',
        'files':files,'file_count':len(files),'outside_plans_content_matches':extra.stdout.splitlines(),
        'parse_errors':errors,'embedded_native_JSON_strings_inspected':embedded_records,
        'search_ActionIds':sorted(TARGET_ACTIONS),'search_KnowledgeIds':sorted(TARGET_KNOWLEDGE),
        'search_state_sha256s':sorted(STATES),'recognized_native_tags':dict(markers),
        'recognized_schemas':dict(recognized_schemas),'result_payload_and_event_identity_fields_inspected':True,
        'HEAD_command_and_parent_bundle_fields_inspected':True,'no_event_constructed':True})
    save('native-events.json',{'unique_native_event_count':len(events),'events':list(events.values()),
        'A03_or_original_prefix_candidate_occurrences':target_event_occurrences,
        'A03_Action_event_occurrences':sum(x['target_Action'] for x in target_event_occurrences),
        'native_event_types':dict(collections.Counter(x['event_type'] for x in events.values()))})
    save('persistence-bundles.json',{'bundle_occurrences':bundles,'bundle_occurrence_count':len(bundles),
        'bundles_containing_A03_events':sum(bool(x['A03_event_indices']) for x in bundles),
        'bundles_containing_original_prefix_event_states':sum(bool(x['original_prefix_state_event_indices']) for x in bundles),
        'heads':heads,'head_count':len(heads),'genesis_ledgers':genesis_ledgers,
        'genesis_ledger_count':len(genesis_ledgers),
        'genesis_ledgers_containing_A03':sum(bool(x['A03_event_indices']) for x in genesis_ledgers)})
    save('result-and-report-candidates.json',{'native_SuppliedResult_candidates':supplied,
        'native_result_payload_candidate_count':len(supplied),'report_candidates':reports,
        'report_candidate_count':len(reports),'standalone_ActionResult_record_ID':
        'NOT_A_NATIVE_TYPE; ActionResult is outcome enum, not occurrence identity.',
        'explicit_event_identity_bodies':identity_bodies,
        'A03_event_identity_body_count':sum(x['A03_Action'] for x in identity_bodies)})
    print(json.dumps({'corpus_files':len(files),'parse_errors':len(errors),'native_events_unique':len(events),
        'A03_event_occurrences':sum(x['target_Action'] for x in target_event_occurrences),
        'original_prefix_event_occurrences':sum(x['original_or_earlier_prefix_state_match'] for x in target_event_occurrences),
        'bundle_occurrences':len(bundles),'native_A03_SuppliedResult_payloads':len(supplied),
        'report_candidates':len(reports),'HEAD_records':len(heads)}))


if __name__ == '__main__':
    main()
