"""Read retained bytes; never execute, reconstruct, admit, or replay A04."""
import collections
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
ACTION = 'E2-PREPARE'
KNOWLEDGE = 'E2-K-PREPARE'
STATES = {
    '545ad19184d8dd7dfb5b2737e081b043d13982f05d05326939ac2cbb89bf54e2',
    'e381424d14336d918fd3bafff16698361395c77ef03fef628d7d74d36af8a9da',
    '6c7efb221870974d76d12d7ceb372369ef68104bb1f522a16d47f7dc37236677',
    '39114028d38b9571c46e211248644b09a3ac63ad9f47cd21a75fc922a2d152e3',
    '8985701af4db7bf08327dc5e455fcd9182ca71e7cfde7b2868c253b0e8bd2d5e',
    '996d1fa73a7c1a880b8cd7a6c27ec48c03386feba4c5a089711482f51aff5069',
    '9b3d8e6a074687a7aef9dca0279262cf2888492de73b7207768dc48bb0f5edfa',
    '8d77f7f1997ca884e07490c4c93f5fbe3a31b09278fd57c6c6ea1f9fa26b3aaf',
    '43a238851a34b2e58f4a49ec870fa258fdcb8d3a88fda50a305df2b570281e79',
    '33c0bb5c4ed55496cde6ec0ce3eb5ee74307872697d8202a06db65c2c731e9b5',
    'd220d3685ba2af01267be8fc158babd214c663169c0d298b989116ed155e5b35',
}
DOSSIER = '6a507317bc9cc323fbaa626e97b5954cf3ad934b0bd92d9dc96bd4f63e07bddb'
EVENT_FIELDS = {'sequence', 'parent_snapshot', 'parent_event', 'result', 'after_snapshot', 'identity'}
BUNDLE_FIELDS = {'initial', 'current', 'events', 'sources', 'policy'}
IDENTITY_FIELDS = {'sequence', 'parent', 'parent_event', 'result', 'after'}
STRUCTURED_SUFFIXES = ('.json', '.jsonl', '.ndjson')
NATIVE_MARKERS = ('ExecutionEvent', 'PersistenceBundle', 'SuppliedResult',
                  'PLANNER-EVENT-1', 'PLANNER-BUNDLE-1', 'PLANNER-HEAD-1', 'GenesisLedger')
RECOVERY_REPORT = 'docs/plans/DETERMINISTIC_PLANNER_V0_1_E2_P05_A04_EVENT_ANCESTRY_RECOVERY_1'


def value(obj):
    return obj.get('value') if isinstance(obj, dict) else obj


def sid(obj):
    return obj.get('sha256') if isinstance(obj, dict) else obj


def escape(key):
    return str(key).replace('~', '~0').replace('/', '~1')


def save(name, obj):
    (OUT/name).write_text(json.dumps(obj, sort_keys=True, indent=2)+'\n')


def rg_matches(terms, extra_args):
    args = ['rg', '-l', '-F']
    for term in terms:
        args += ['-e', term]
    args += ['.', '-g', '!docs/experiments/E1/**', '-g', '!**/__pycache__/**',
             '-g', '!docs/plans/qualification/E2_P05_A04_EVENT_ANCESTRY_RECOVERY_1/**',
             '-g', '!'+RECOVERY_REPORT+'.*'] + extra_args
    result = subprocess.run(args, cwd=str(ROOT), capture_output=True, text=True)
    if result.returncode not in (0, 1):
        raise RuntimeError(result.stderr)
    return sorted(p[2:] if p.startswith('./') else p for p in result.stdout.splitlines())


def main():
    names = subprocess.run(['rg', '--files', 'docs/plans'], cwd=str(ROOT), check=True,
                           capture_output=True, text=True).stdout.splitlines()
    broad = rg_matches(sorted({ACTION, KNOWLEDGE, DOSSIER} | STATES) + list(NATIVE_MARKERS), [])
    # Extensionless native HEAD/ledger files are included, not just *.json.
    paths = sorted({p for p in names+broad if
                    not p.startswith(str(OUT.relative_to(ROOT))+'/') and not p.startswith(RECOVERY_REPORT+'.') and '/__pycache__/' not in p and
                    '/E1/' not in p and (p.endswith(STRUCTURED_SUFFIXES) or
                    Path(p).suffix not in ('.py', '.md', '.txt', '.log', '.rs', '.js', '.ts', '.sh', '.diff'))})
    texts = sorted(p for p in broad if p not in paths)
    files, errors, bundles, heads, genesis, identity_bodies = [], [], [], [], [], []
    non_records = []
    events, markers, schemas = {}, collections.Counter(), collections.Counter()
    supplied, reports, snapshots, embedded = [], [], [], []
    target_events, original_state_events, text_audit = [], [], []
    decoded_text_documents = []

    def inspect(document, pointer, file_pin):
        queue = [(document, pointer)]
        while queue:
            obj, at = queue.pop()
            if isinstance(obj, dict):
                tag = obj.get('$type', obj.get('type'))
                if isinstance(tag, str):
                    markers[tag] += 1
                if isinstance(obj.get('schema'), str):
                    schemas[obj['schema']] += 1
                result = obj.get('result')
                action = value(result.get('action')) if isinstance(result, dict) else None
                if IDENTITY_FIELDS <= set(obj):
                    identity_bodies.append(dict(file_pin, pointer=at, target_Action=action == ACTION,
                                                classification='IDENTITY_BODY; LEDGER_MEMBERSHIP_SEPARATE'))
                if tag == 'ExecutionEvent' or EVENT_FIELDS <= set(obj):
                    key = json.dumps(obj.get('identity'), sort_keys=True)
                    if key not in events:
                        events[key] = {'identity':obj.get('identity'), 'sequence':obj.get('sequence'),
                            'result_type':result.get('$type', result.get('type')) if isinstance(result,dict) else type(result).__name__,
                            'action':action,'parent_event':obj.get('parent_event'),
                            'pre_state':obj.get('parent_snapshot'),'post_state':obj.get('after_snapshot'),
                            'occurrences':[]}
                    events[key]['occurrences'].append(dict(file_pin,pointer=at))
                    match = {'file':file_pin,'pointer':at,'event':obj}
                    if action == ACTION:
                        target_events.append(match)
                    if sid(obj.get('parent_snapshot')) in STATES or sid(obj.get('after_snapshot')) in STATES:
                        original_state_events.append(match)
                if tag == 'PersistenceBundle' or BUNDLE_FIELDS <= set(obj):
                    history = obj.get('events', [])
                    current, initial = obj.get('current', {}), obj.get('initial', {})
                    complete = all(isinstance(e,dict) and EVENT_FIELDS <= set(e) for e in history)
                    links = complete and all(e['parent_event']==history[i-1]['identity'] and
                        e['parent_snapshot']==history[i-1]['after_snapshot'] and
                        e['sequence']==history[i-1]['sequence']+1 for i,e in enumerate(history) if i)
                    context = current.get('context') or {}
                    initial_completed = [value(s.get('id')) for s in initial.get('statuses',[]) if
                        value(s.get('state'))=='COMPLETED']
                    target_indices = [i for i,e in enumerate(history) if isinstance(e,dict) and
                        isinstance(e.get('result'),dict) and value(e['result'].get('action'))==ACTION]
                    bundles.append(dict(file_pin,pointer=at,event_count=len(history),context=context,
                        result_Actions=[value(e['result'].get('action')) for e in history if
                            isinstance(e,dict) and isinstance(e.get('result'),dict) and 'action' in e['result']],
                        A04_event_indices=target_indices, original_state_event_indices=[i for i,e in enumerate(history)
                            if isinstance(e,dict) and (sid(e.get('parent_snapshot')) in STATES or
                                                     sid(e.get('after_snapshot')) in STATES)],
                        complete_native_event_fields=complete,parent_links_continuous=links,
                        root=history[0].get('identity') if history else None,
                        append_head=history[-1].get('identity') if history else None,
                        initial_completed_prefix=[s for s in initial_completed if s in ('E2-CHECK','E2-COLLECT',ACTION)],
                        A04_completed_in_initial=ACTION in initial_completed,
                        occurrence_inference_from_initial='PROHIBITED'))
                if obj.get('schema') == 'PLANNER-HEAD-1':
                    heads.append(dict(file_pin,pointer=at,bundle=obj.get('bundle'),
                                      previous=obj.get('previous'),command=obj.get('command')))
                if tag == 'GenesisLedger' or {'ledger_id','root','events','append_head'} <= set(obj):
                    history = obj.get('events', [])
                    genesis.append(dict(file_pin,pointer=at,ledger_id=obj.get('ledger_id'),root=obj.get('root'),
                        append_head=obj.get('append_head'),pre_genesis_history=obj.get('pre_genesis_history'),
                        event_count=len(history),A04_event_indices=[i for i,e in enumerate(history) if
                            isinstance(e,dict) and isinstance(e.get('result'),dict) and value(e['result'].get('action'))==ACTION]))
                if tag == 'SuppliedResult' and value(obj.get('action')) == ACTION:
                    supplied.append(dict(file_pin,pointer=at,payload=obj,
                        classification='TYPED_PAYLOAD; ACTUAL_EXECUTION_AND_LEDGER_MEMBERSHIP_NOT_IMPLIED'))
                report_action = value(obj.get('action',obj.get('action_executed',obj.get('selected'))))
                if report_action == ACTION and tag not in ('Action','ActionStatus','SuppliedResult','KnowledgeRecord','GraphEntity'):
                    keys = ('action','action_executed','selected','sequence','result','pre_state','post_state',
                            'pre_state_id','post_state_id','dossier','knowledge','validation_instances','result_identity')
                    reports.append(dict(file_pin,pointer=at,fields={k:obj[k] for k in keys if k in obj},
                        native_type=tag,classification='REPORT_METADATA_OR_DEFINITION; NOT_NATIVE_EVENT'))
                if tag == 'Snapshot':
                    status = next((s for s in obj.get('statuses',[]) if value(s.get('id'))==ACTION),None)
                    records = [k for k in obj.get('knowledge',[]) if value(k.get('id'))==KNOWLEDGE]
                    if status or records:
                        snapshots.append(dict(file_pin,pointer=at,context=obj.get('context'),prepare_status=status,
                            prepare_knowledge=records,validation_instance_count=len(obj.get('validation_instances',[])),
                            classification='SNAPSHOT_ONLY; NO_EVENT_PARENT_OR_LEDGER_HISTORY'))
                queue.extend((v,at+'/'+escape(k)) for k,v in obj.items())
            elif isinstance(obj,list):
                queue.extend((v,at+'/'+str(i)) for i,v in enumerate(obj))
            elif isinstance(obj,str) and obj.startswith(('{','[')) and any(x in obj for x in NATIVE_MARKERS):
                try:
                    decoded = json.loads(obj)
                except ValueError:
                    continue
                embedded.append(dict(file_pin,pointer=at))
                queue.append((decoded,at+'@decoded-json'))

    for name in paths:
        raw = (ROOT/name).read_bytes()
        pin = {'path':name,'raw_sha256':hashlib.sha256(raw).hexdigest()}
        if Path(name).name == 'LOCK' and not raw:
            non_records.append(dict(pin,classification='EMPTY_NATIVE_STORE_LOCK; NO_EVENT_BYTES'))
            continue
        files.append(pin)
        if name.endswith(('.jsonl','.ndjson')):
            docs = []
            for i,line in enumerate(raw.splitlines()):
                if line.strip():
                    try:
                        docs.append((json.loads(line),'@line:'+str(i+1)))
                    except (ValueError,UnicodeDecodeError) as exc:
                        errors.append(dict(pin,line=i+1,error=str(exc)))
        else:
            try:
                docs = [(json.loads(raw),'')]
            except (ValueError,UnicodeDecodeError) as exc:
                errors.append(dict(pin,error=str(exc)))
                continue
        for doc,pointer in docs:
            inspect(doc,pointer,pin)

    terms = {ACTION,KNOWLEDGE,DOSSIER} | STATES
    for name in texts:
        raw = (ROOT/name).read_bytes()
        pin = {'path':name,'raw_sha256':hashlib.sha256(raw).hexdigest()}
        body = raw.decode('utf-8',errors='replace')
        matches = []
        for i,line in enumerate(body.splitlines()):
            hits = sorted(t for t in terms if t in line)
            if hits:
                matches.append({'line':i+1,'terms':hits,'excerpt':line[:1400],
                                'excerpt_truncated':len(line)>1400})
            # Standalone native JSON lines and multiline fenced blocks are searched.
            if line.strip().startswith(('{','[')) and any(t in line for t in NATIVE_MARKERS):
                try:
                    document = json.loads(line.strip())
                except ValueError:
                    continue
                inspect(document,'@line:'+str(i+1),pin)
                decoded_text_documents.append(dict(pin,line=i+1))
        fenced = False
        block = []
        start = None
        for i,line in enumerate(body.splitlines()):
            if line.startswith('```'):
                if fenced:
                    joined='\n'.join(block)
                    if any(t in joined for t in NATIVE_MARKERS):
                        try:
                            document=json.loads(joined)
                        except ValueError:
                            pass
                        else:
                            inspect(document,'@fenced-line:'+str(start),pin)
                            decoded_text_documents.append(dict(pin,line=start))
                fenced,block,start = not fenced,[],i+2
            elif fenced:
                block.append(line)
        text_audit.append(dict(pin,matches=matches))

    save('search-corpus.json',{'scope':'All retained structured docs/plans files, plus repository content matches including extensionless native records and native JSON embedded in text; current recovery outputs and frozen E1 excluded.',
        'files':files,'file_count':len(files),'text_file_count':len(texts),'outside_plans_matches':[p for p in broad if not p.startswith('docs/plans/')],
        'parse_errors':errors,'non_event_records':non_records,
        'embedded_native_JSON_strings':embedded,'decoded_native_text_documents':decoded_text_documents,
        'search_ActionId':ACTION,'search_KnowledgeId':KNOWLEDGE,'search_state_sha256s':sorted(STATES),
        'search_dossier_sha256':DOSSIER,'recognized_native_tags':dict(markers),'recognized_schemas':dict(schemas),
        'event_result_parent_state_command_payload_fields_inspected':True,'event_or_result_constructed':False})
    save('native-events.json',{'unique_native_event_count':len(events),'events':list(events.values()),
        'A04_candidate_occurrences':target_events,'A04_Action_event_occurrences':len(target_events),
        'original_prefix_or_handoff_state_events':original_state_events,
        'original_prefix_or_handoff_event_count':len(original_state_events),
        'event_result_types':dict(collections.Counter(e['result_type'] for e in events.values()))})
    save('persistence-bundles.json',{'bundle_occurrences':bundles,'bundle_occurrence_count':len(bundles),
        'bundles_containing_A04_events':sum(bool(b['A04_event_indices']) for b in bundles),
        'bundles_containing_original_state_events':sum(bool(b['original_state_event_indices']) for b in bundles),
        'bundles_with_PREPARE_completed_in_initial':sum(b['A04_completed_in_initial'] for b in bundles),
        'heads':heads,'head_count':len(heads),'genesis_ledgers':genesis,'genesis_ledger_count':len(genesis),
        'genesis_ledgers_containing_A04':sum(bool(b['A04_event_indices']) for b in genesis)})
    save('result-and-report-candidates.json',{'native_SuppliedResult_candidates':supplied,'native_payload_count':len(supplied),
        'report_candidates':reports,'report_candidate_count':len(reports),'snapshot_occurrences':snapshots,
        'snapshot_occurrence_count':len(snapshots),'explicit_event_identity_bodies':identity_bodies,
        'A04_event_identity_body_count':sum(b['target_Action'] for b in identity_bodies),
        'SuppliedResult_and_KnowledgeRecord_are_not_event_occurrence_or_ancestry':True})
    save('text-search.json',{'files':text_audit,'file_count':len(text_audit),
        'matching_line_count':sum(len(x['matches']) for x in text_audit),'native_documents_decoded':decoded_text_documents})
    summary={'corpus_files':len(files),'parse_errors':len(errors),'text_files':len(texts),
        'native_events_unique':len(events),'A04_event_occurrences':len(target_events),
        'original_state_event_occurrences':len(original_state_events),'bundle_occurrences':len(bundles),
        'native_A04_payloads':len(supplied),'report_candidates':len(reports),'HEAD_records':len(heads),
        'GenesisLedgers':len(genesis),'snapshot_occurrences':len(snapshots)}
    save('search-summary.json',summary)
    print(json.dumps(summary))


if __name__ == '__main__':
    main()
