"""Inspect retained bytes for request/wait history. No native execution/replay."""
import collections
import hashlib
import json
from pathlib import Path
import re
import subprocess

from adapter.planner import codec as c

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
EVENT_FIELDS = {'sequence', 'parent_snapshot', 'parent_event', 'result', 'after_snapshot', 'identity'}
BUNDLE_FIELDS = {'initial', 'current', 'events', 'sources', 'policy'}
STAGES = ('EVIDENCE_REQUEST_READY', 'WAITING_FOR_EXTERNAL_EVIDENCE')
MARKERS = ('ExternalEvent', 'ExecutionEvent', 'PersistenceBundle', 'PLANNER-BUNDLE-1',
           'PLANNER-HEAD-1', 'ExternalResolutionContract', 'E2-A06', 'E2-GATE',
           'TEST-REQUEST', 'EXTERNAL_WAIT', *STAGES)


def barred(*args, **kwargs):
    raise RuntimeError('No native execution, append, save/restore or replay permitted')


for name in ('_replay', '_prefix_bundle', 'bundle_id', 'bundle_bytes', 'append_event',
             'record_result', 'save_bundle', 'restore', 'commit_event', 'apply_event',
             'admit_external_evidence', '_publish_head', '_extend_private'):
    setattr(c, name, barred)


def save(name, value):
    (OUT / name).write_text(json.dumps(value, sort_keys=True, indent=2) + '\n')


def val(value):
    return value.get('value') if isinstance(value, dict) else value


def aid(value):
    if isinstance(value, dict) and value.get('namespace') and value.get('sha256'):
        return value['namespace'] + ':' + value['sha256']
    return None


def pointer(at, key):
    return at + '/' + str(key).replace('~', '~0').replace('/', '~1')


def main():
    listed = subprocess.run(['rg', '--files', 'docs', 'adapter'], cwd=str(ROOT),
                            capture_output=True, text=True, check=True).stdout.splitlines()
    args = ['rg', '-l', '-F']
    for token in MARKERS:
        args.extend(['-e', token])
    args.extend(['.', '-g', '!docs/experiments/E1/**', '-g', '!**/__pycache__/**',
                 '-g', '!' + str(OUT.relative_to(ROOT)) + '/**'])
    broad = subprocess.run(args, cwd=str(ROOT), capture_output=True, text=True)
    assert broad.returncode in (0, 1), broad.stderr
    hits = sorted({p[2:] if p.startswith('./') else p for p in broad.stdout.splitlines()})
    names = sorted({p for p in listed + hits if '/E1/' not in p and '/__pycache__/' not in p
                    and not p.startswith(str(OUT.relative_to(ROOT)) + '/') and
                    (Path(p).suffix in ('.json', '.jsonl', '.ndjson', '.bundle', '.snapshot', '.ledger')
                     or (p in hits and Path(p).suffix not in
                         ('.py', '.md', '.txt', '.log', '.rs', '.js', '.ts', '.sh', '.diff', '.svg')))})
    manifests, errors, empty, bundles, heads, genesis = [], [], [], [], [], []
    events, commands, gate_records, requests, identity_bodies, embedded = {}, [], {}, {}, [], []
    seen_strings, text_audit = set(), []
    documents = 0
    def inspect(document, at, pin, encoding=None):
        queue = [(document, at)]
        while queue:
            obj, path = queue.pop()
            ref = dict(pin, pointer=path)
            if encoding:
                ref['encoding'] = encoding
            if isinstance(obj, dict):
                tag = obj.get('$type', obj.get('type'))
                result = obj.get('result')
                kind = result.get('$type', result.get('type')) if isinstance(result, dict) else None
                if tag == 'ExecutionEvent' or EVENT_FIELDS <= set(obj):
                    key = aid(obj.get('identity')) or json.dumps(obj.get('identity'), sort_keys=True)
                    body_key = hashlib.sha256(c.canonical_bytes(obj)).hexdigest()
                    if key not in events:
                        events[key] = {'identity': obj.get('identity'), 'event': obj,
                                       'result_type': kind, 'occurrences': [], 'body_representations': {}}
                    events[key]['occurrences'].append(ref)
                    events[key]['body_representations'].setdefault(body_key, ref)
                if tag == 'ExternalEvent' or {'gate', 'stage', 'expected_snapshot'} <= set(obj):
                    commands.append({'source': ref, 'payload': obj, 'gate': val(obj.get('gate')),
                                     'stage': val(obj.get('stage')), 'typed': tag == 'ExternalEvent',
                                     'classification': 'NATIVE_COMMAND_WITHOUT_ENCLOSING_EVENT' if tag == 'ExternalEvent' else 'REPORT_METADATA'})
                if tag == 'ExternalGate' or {'requirements', 'receipt_action', 'reentry', 'held_actions', 'stage', 'history', 'id'} <= set(obj):
                    key = hashlib.sha256(c.canonical_bytes(obj)).hexdigest()
                    gate_records.setdefault(key, {'gate': obj, 'occurrences': []})['occurrences'].append(ref)
                if tag == 'ExternalResolutionContract' or {'request', 'gate', 'requirement', 'proposition', 'receipt_action', 'scope', 'lineage'} <= set(obj):
                    key = hashlib.sha256(c.canonical_bytes(obj)).hexdigest()
                    requests.setdefault(key, {'contract': obj, 'occurrences': []})['occurrences'].append(ref)
                if tag == 'PersistenceBundle' or BUNDLE_FIELDS <= set(obj):
                    history = obj.get('events', [])
                    indexes = [i for i, e in enumerate(history) if isinstance(e, dict) and
                               isinstance(e.get('result'), dict) and
                               val(e['result'].get('stage')) in STAGES]
                    native_id, error = None, None
                    try:
                        decoded = c._unwire(obj)
                        identity = c._identity(c._bundle_bytes_admitted(decoded), 'planner-bundle-v1')
                        native_id = identity.namespace + ':' + identity.sha256
                    except Exception as exc:
                        error = str(exc)
                    links = all(isinstance(e, dict) and EVENT_FIELDS <= set(e) for e in history)
                    if links:
                        links = all(e['parent_event'] == history[i - 1]['identity'] and
                                    e['parent_snapshot'] == history[i - 1]['after_snapshot'] and
                                    e['sequence'] == history[i - 1]['sequence'] + 1
                                    for i, e in enumerate(history) if i)
                    def gates(snapshot):
                        return [{'id': val(g.get('id')), 'stage': val(g.get('stage')),
                                 'history': [val(x) for x in g.get('history', [])],
                                 'request': [x.get('request') for x in g.get('resolution_contracts', [])]}
                                for g in snapshot.get('external_gates', [])]
                    bundles.append({'source': ref, 'native_bundle_comparison_identity': native_id,
                        'comparison_is_not_restore_or_event_occurrence': True, 'identity_decode_error': error,
                        'event_count': len(history), 'request_wait_event_indices': indexes,
                        'request_wait_events': [history[i] for i in indexes],
                        'events': [{'id': aid(e.get('identity')), 'sequence': e.get('sequence'),
                                    'parent': aid(e.get('parent_event')), 'pre': aid(e.get('parent_snapshot')),
                                    'post': aid(e.get('after_snapshot')), 'result_type': e.get('result', {}).get('$type', e.get('result', {}).get('type')),
                                    'gate': val(e.get('result', {}).get('gate')), 'stage': val(e.get('result', {}).get('stage'))}
                                   for e in history if isinstance(e, dict) and isinstance(e.get('result'), dict)],
                        'initial_gates': gates(obj.get('initial', {})), 'current_gates': gates(obj.get('current', {})),
                        'initial_context': obj.get('initial', {}).get('context'),
                        'current_context': obj.get('current', {}).get('context'),
                        'parent_links_continuous': links,
                        'root': aid(history[0].get('identity')) if history else None,
                        'head': aid(history[-1].get('identity')) if history else None})
                if obj.get('schema') == 'PLANNER-HEAD-1':
                    heads.append(dict(ref, bundle=obj.get('bundle'), previous=obj.get('previous'), command=obj.get('command')))
                if tag == 'GenesisLedger' or {'ledger_id', 'root', 'events', 'append_head'} <= set(obj):
                    genesis.append(dict(ref, ledger_id=obj.get('ledger_id'), root=obj.get('root'),
                        head=obj.get('append_head'), event_count=len(obj.get('events', [])),
                        request_wait_events=[e for e in obj.get('events', []) if isinstance(e, dict) and
                            isinstance(e.get('result'), dict) and val(e['result'].get('stage')) in STAGES]))
                if {'sequence', 'parent', 'result', 'after'} <= set(obj):
                    identity_bodies.append({'source': ref, 'body': obj,
                        'request_wait': isinstance(obj['result'], dict) and val(obj['result'].get('stage')) in STAGES})
                queue.extend((item, pointer(path, key)) for key, item in obj.items())
            elif isinstance(obj, list):
                queue.extend((item, pointer(path, i)) for i, item in enumerate(obj))
            elif isinstance(obj, str) and obj.lstrip().startswith(('{', '[')) and any(t in obj for t in MARKERS):
                hashed = hashlib.sha256(obj.encode()).hexdigest()
                if hashed in seen_strings:
                    continue
                seen_strings.add(hashed)
                try:
                    decoded = json.loads(obj)
                except (TypeError, ValueError):
                    continue
                embedded.append({'source': ref, 'decoded_text_sha256': hashed})
                inspect(decoded, '', pin, encoding={'container_pointer': path, 'kind': 'JSON_STRING', 'json_text_sha256': hashed})
    for name in names:
        path = ROOT / name
        if path.is_symlink() or not path.is_file():
            continue
        raw = path.read_bytes()
        pin = {'path': name, 'raw_sha256': hashlib.sha256(raw).hexdigest()}
        manifests.append(pin)
        if not raw.strip():
            empty.append(name)
            continue
        try:
            items = [(json.loads(line), '/line/' + str(i + 1)) for i, line in enumerate(raw.decode().splitlines()) if line.strip()] \
                if path.suffix in ('.jsonl', '.ndjson') else [(json.loads(raw), '')]
        except (UnicodeDecodeError, TypeError, ValueError) as exc:
            errors.append(dict(pin, error=str(exc)))
            continue
        for document, at in items:
            documents += 1
            inspect(document, at, pin)
    decoder = json.JSONDecoder()
    for name in hits:
        path = ROOT / name
        if path.suffix not in ('.md', '.log', '.txt', '.py') or not path.is_file():
            continue
        raw = path.read_bytes()
        body = raw.decode()
        pin = {'path': name, 'raw_sha256': hashlib.sha256(raw).hexdigest()}
        row = dict(pin, classification='SOURCE_CODE_NOT_OCCURRENCE' if path.suffix == '.py' else 'TEXT_OR_REPORT_METADATA',
                   tokens=[t for t in MARKERS if t in body], JSON_fragments_parsed=0)
        if path.suffix != '.py':
            cursor = 0
            for match in re.finditer(r'[\{\[]', body):
                if match.start() < cursor:
                    continue
                try:
                    document, finish = decoder.raw_decode(body, match.start())
                except ValueError:
                    continue
                cursor = finish
                row['JSON_fragments_parsed'] += 1
                inspect(document, '', pin, encoding={'kind': 'JSON_TEXT_FRAGMENT', 'character_start': match.start(),
                    'character_end': finish, 'json_text_sha256': hashlib.sha256(body[match.start():finish].encode()).hexdigest()})
        text_audit.append(row)
    event_list = list(events.values())
    matching = [e for e in event_list if isinstance(e['event'].get('result'), dict) and val(e['event']['result'].get('stage')) in STAGES]
    external = [e for e in event_list if e['result_type'] == 'ExternalEvent']
    summary = {'result': 'PASS_SEARCH_COMPLETE', 'scope': 'Retained non-E1 native structured, embedded JSON and matching text artifacts',
        'structured_files_scanned': len(manifests), 'documents_parsed': documents, 'parse_errors': len(errors),
        'empty_files': len(empty), 'native_event_identities': len(events), 'native_ExternalEvent_identities': len(external),
        'request_wait_native_event_identities': len(matching),
        'request_wait_native_command_representations': sum(x['typed'] and x['stage'] in STAGES for x in commands),
        'request_wait_identity_bodies': sum(x['request_wait'] for x in identity_bodies),
        'bundle_representations': len(bundles), 'HEAD_representations': len(heads), 'genesis_representations': len(genesis),
        'text_artifacts_inspected': len(text_audit), 'text_JSON_fragments_parsed': sum(x['JSON_fragments_parsed'] for x in text_audit),
        'embedded_JSON_decoded': len(embedded), 'gate_representations_distinct': len(gate_records),
        'request_contract_representations_distinct': len(requests),
        'native_operations_or_replay': 0, 'events_constructed': 0, 'events_appended': 0, 'authorities_issued': 0}
    save('file-search-manifest.json', {'files': manifests, 'text_hits': hits, 'parse_errors': errors, 'empty_files': empty})
    save('event-search.json', {'unique_events': event_list, 'external_events': external,
                             'request_wait_events': matching, 'identity_bodies': identity_bodies})
    save('persistence-search.json', {'bundles': bundles, 'heads': heads, 'genesis_ledgers': genesis})
    save('native-record-search.json', {'external_commands': commands, 'gate_records': list(gate_records.values()),
                                      'request_contracts': list(requests.values()), 'embedded_JSON': embedded})
    save('text-audit.json', {'artifacts': text_audit})
    save('search-summary.json', summary)
    print(json.dumps(summary))


if __name__ == '__main__':
    main()
