"""Search retained bytes only. No decision capture, application, or replay."""
import collections
import hashlib
import json
import re
from pathlib import Path
import subprocess

from adapter.planner import codec as c

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
SUBJECT='E2-DECIDE'
CHOICE='6bebc233783b5faa0898ecccb20cf51ce529086c74ca672a113450f6e270a411'
GRANT='cddac13f5e0b0f460e5d58a68d4ce753ce43cb5d17481be408d9b5f43d616574'
DOSSIER='6a507317bc9cc323fbaa626e97b5954cf3ad934b0bd92d9dc96bd4f63e07bddb'
STATES={'9b3d8e6a074687a7aef9dca0279262cf2888492de73b7207768dc48bb0f5edfa',
        '8d77f7f1997ca884e07490c4c93f5fbe3a31b09278fd57c6c6ea1f9fa26b3aaf'}
EVENT_FIELDS={'sequence','parent_snapshot','parent_event','result','after_snapshot','identity'}
BUNDLE_FIELDS={'initial','current','events','sources','policy'}
DECISION_FIELDS={'decision','choice','record','authority','expected_snapshot'}
MARKERS=('ExecutionEvent','PersistenceBundle','RecordedDecision','ChoiceEvidence','HumanChoiceInput',
         'PLANNER-BUNDLE-1','PLANNER-HEAD-1',SUBJECT,CHOICE,GRANT,DOSSIER,*sorted(STATES))


def save(name,value):
    (OUT/name).write_text(json.dumps(value,sort_keys=True,indent=2)+'\n')
def value(x):return x.get('value') if isinstance(x,dict) else x
def digest(x):return x.get('sha256') if isinstance(x,dict) else x
def pointer(at,key):return at+'/'+str(key).replace('~','~0').replace('/','~1')


def main():
    listed=subprocess.run(['rg','--files','docs/plans','adapter','docs'],cwd=str(ROOT),
                          capture_output=True,text=True,check=True).stdout.splitlines()
    args=['rg','-l','-F']
    for token in MARKERS:args.extend(['-e',token])
    args.extend(['.','-g','!docs/experiments/E1/**','-g','!**/__pycache__/**',
                 '-g','!'+str(OUT.relative_to(ROOT))+'/**'])
    broad=subprocess.run(args,cwd=str(ROOT),capture_output=True,text=True)
    if broad.returncode not in (0,1):raise RuntimeError(broad.stderr)
    hits=sorted({p[2:] if p.startswith('./') else p for p in broad.stdout.splitlines()})
    names=sorted({p for p in listed+hits if '/E1/' not in p and '/__pycache__/' not in p
                  and not p.startswith(str(OUT.relative_to(ROOT))+'/') and
                  (Path(p).suffix in ('.json','.jsonl','.ndjson','.bundle','.snapshot','.ledger')
                   or (p in hits and Path(p).suffix not in
                       ('.py','.md','.txt','.log','.rs','.js','.ts','.sh','.diff','.svg')))})
    manifests=[];errors=[];empty=[];documents=0;bundles=[];heads=[];genesis=[]
    events={};target_events=[];state_events=[];commands=[];records=[];evidence=[];grants=[];snapshots=[]
    identity_bodies=[];embedded=[];seen_strings=set();schemas=collections.Counter();tags=collections.Counter()
    text_audit=[]
    def inspect(document,at,pin,encoding=None):
        queue=[(document,at)]
        while queue:
            obj,path=queue.pop()
            ref={**pin,'pointer':path}
            if encoding:ref['encoding']=encoding
            if isinstance(obj,dict):
                tag=obj.get('$type',obj.get('type'))
                if isinstance(tag,str):tags[tag]+=1
                if isinstance(obj.get('schema'),str):schemas[obj['schema']]+=1
                result=obj.get('result');kind=result.get('$type',result.get('type')) if isinstance(result,dict) else None
                decision=value(result.get('decision')) if isinstance(result,dict) else None
                if tag=='ExecutionEvent' or EVENT_FIELDS<=set(obj):
                    key=json.dumps(obj.get('identity'),sort_keys=True)
                    if key not in events:
                        events[key]={'identity':obj.get('identity'),'sequence':obj.get('sequence'),
                            'result_type':kind,'decision':decision,'parent':obj.get('parent_event'),
                            'pre_state':obj.get('parent_snapshot'),'post_state':obj.get('after_snapshot'),'occurrences':[]}
                    events[key]['occurrences'].append(ref)
                    if (kind=='RecordedDecision' or (isinstance(result,dict) and DECISION_FIELDS<=set(result))) and decision==SUBJECT:
                        target_events.append({'source':ref,'event':obj,'classification_pending':True})
                    if digest(obj.get('parent_snapshot')) in STATES or digest(obj.get('after_snapshot')) in STATES:
                        state_events.append({'source':ref,'event':obj})
                if tag=='RecordedDecision' or DECISION_FIELDS<=set(obj):
                    commands.append({'source':ref,'subject':value(obj.get('decision')),'payload':obj,
                        'typed_codec_representation':tag=='RecordedDecision',
                        'classification':'NATIVE_RECORDED_DECISION_WITHOUT_EVENT' if tag=='RecordedDecision' else 'REPORT_METADATA'})
                if tag=='GraphEntity' and value(obj.get('decision'))==SUBJECT:
                    row={'source':ref,'EntityId':value(obj.get('id')),'authority_identity':obj.get('identity'),
                         'choice':obj.get('choice'),'scope':obj.get('scope'),'lineage':obj.get('lineage'),
                         'generation':obj.get('generation'),'target':obj.get('target'),'provenance':obj.get('provenance')}
                    if value(obj.get('id'))=='E2-GRANT' or digest(obj.get('identity'))==GRANT:
                        grants.append(row)
                    else:records.append(row)
                if tag in ('HumanChoiceInput','ChoiceEvidence') or (
                    (value(obj.get('subject'))==SUBJECT or value(obj.get('decision'))==SUBJECT)
                    and 'option' in obj and ('issuer' in obj or 'trust_root' in obj)):
                    evidence.append({'source':ref,'payload':obj,'classification':'CHOICE_EVIDENCE_ONLY'})
                if tag=='Snapshot' and any(value(d.get('action'))==SUBJECT and d.get('record') is not None
                                          for d in obj.get('decisions',[]) if isinstance(d,dict)):
                    snapshots.append({'source':ref,'context':obj.get('context'),
                        'decision':[d for d in obj['decisions'] if value(d.get('action'))==SUBJECT],
                        'classification':'SNAPSHOT_ONLY; NATIVE_RECORDED_STATE_WITHOUT_OCCURRENCE'})
                if tag=='PersistenceBundle' or BUNDLE_FIELDS<=set(obj):
                    history=obj.get('events',[]);initial=obj.get('initial',{});current=obj.get('current',{})
                    target=[i for i,e in enumerate(history) if isinstance(e,dict) and isinstance(e.get('result'),dict)
                            and value(e['result'].get('decision'))==SUBJECT and
                            (e['result'].get('$type')=='RecordedDecision' or DECISION_FIELDS<=set(e['result']))]
                    initial_decisions=[d for d in initial.get('decisions',[]) if isinstance(d,dict) and value(d.get('action'))==SUBJECT]
                    native_id=None;identity_error=None
                    try:
                        decoded=c._unwire(obj)
                        native_id=c._identity(c._bundle_bytes_admitted(decoded),'planner-bundle-v1')
                        native_id=native_id.namespace+':'+native_id.sha256
                    except Exception as exc:identity_error=str(exc)
                    links=all(isinstance(e,dict) and EVENT_FIELDS<=set(e) for e in history)
                    if links:links=all(e['parent_event']==history[i-1]['identity'] and
                        e['parent_snapshot']==history[i-1]['after_snapshot'] and
                        e['sequence']==history[i-1]['sequence']+1 for i,e in enumerate(history) if i)
                    bundles.append({'source':ref,'native_bundle_comparison_identity':native_id,
                        'identity_comparison_is_not_trust_or_occurrence':True,'identity_decode_error':identity_error,
                        'event_count':len(history),'recorded_decision_event_indices':target,
                        'result_types':[e.get('result',{}).get('$type') for e in history if isinstance(e,dict) and isinstance(e.get('result'),dict)],
                        'initial_recorded_decision':initial_decisions,'context':current.get('context'),
                        'parent_links_continuous':links,'root':history[0].get('identity') if history else None,
                        'append_head':history[-1].get('identity') if history else None,
                        'initial_record_is_not_event_occurrence':True})
                if obj.get('schema')=='PLANNER-HEAD-1':
                    heads.append({**ref,'bundle':obj.get('bundle'),'previous':obj.get('previous'),'command':obj.get('command')})
                if tag=='GenesisLedger' or {'ledger_id','root','events','append_head'}<=set(obj):
                    genesis.append({**ref,'ledger_id':obj.get('ledger_id'),'root':obj.get('root'),
                        'head':obj.get('append_head'),'event_count':len(obj.get('events',[])),
                        'matching_events':[e for e in obj.get('events',[]) if isinstance(e,dict) and
                                           value((e.get('result') or {}).get('decision'))==SUBJECT]})
                if {'sequence','parent','result','after'}<=set(obj):
                    identity_bodies.append({'source':ref,'body':obj,'target':isinstance(obj['result'],dict)
                        and value(obj['result'].get('decision'))==SUBJECT})
                queue.extend((item,pointer(path,key)) for key,item in obj.items())
            elif isinstance(obj,list):queue.extend((item,pointer(path,i)) for i,item in enumerate(obj))
            elif isinstance(obj,str) and obj.lstrip().startswith(('{','[')) and any(t in obj for t in MARKERS):
                hashed=hashlib.sha256(obj.encode()).hexdigest()
                if hashed in seen_strings:continue
                seen_strings.add(hashed)
                try:decoded=json.loads(obj)
                except (TypeError,ValueError):continue
                embedded.append({'source':ref,'decoded_text_sha256':hashed})
                inspect(decoded,'',pin,encoding={'container_pointer':path,'kind':'JSON_STRING','json_text_sha256':hashed})
    for name in names:
        p=ROOT/name
        if p.is_symlink() or not p.is_file():continue
        raw=p.read_bytes();pin={'path':name,'raw_sha256':hashlib.sha256(raw).hexdigest()}
        manifests.append(pin)
        if not raw.strip():empty.append(name);continue
        try:items=[(json.loads(line),'/line/'+str(i+1)) for i,line in enumerate(raw.decode().splitlines()) if line.strip()] \
                  if p.suffix in ('.jsonl','.ndjson') else [(json.loads(raw),'')]
        except (UnicodeDecodeError,TypeError,ValueError) as exc:errors.append({**pin,'error':str(exc)});continue
        for document,at in items:documents+=1;inspect(document,at,pin)
    decoder=json.JSONDecoder()
    for name in hits:
        p=ROOT/name
        if p.suffix not in ('.md','.log','.txt','.py') or not p.is_file():continue
        raw=p.read_bytes();body=raw.decode();pin={'path':name,'raw_sha256':hashlib.sha256(raw).hexdigest()}
        row={**pin,'source_classification':'SOURCE_CODE_NOT_OCCURRENCE' if p.suffix=='.py' else 'TEXT_OR_REPORT_METADATA',
             'matching_tokens':[token for token in MARKERS if token in body],
             'JSON_fragments_parsed':0,'native_event_occurrences':0}
        # Source code establishes capability, not a retained occurrence. Logs and
        # fenced/document JSON can retain actual typed records and are decoded.
        if p.suffix!='.py':
            cursor=0
            for match in re.finditer(r'[\{\[]',body):
                if match.start()<cursor:continue
                try:doc,finish=decoder.raw_decode(body,match.start())
                except ValueError:continue
                cursor=finish;row['JSON_fragments_parsed']+=1
                before=len(target_events)
                inspect(doc,'',pin,encoding={'kind':'JSON_TEXT_FRAGMENT','character_start':match.start(),
                                             'character_end':finish,'json_text_sha256':hashlib.sha256(body[match.start():finish].encode()).hexdigest()})
                row['native_event_occurrences']+=len(target_events)-before
        text_audit.append(row)
    summary={'result':'PASS_SEARCH_COMPLETE','scope':'Retained non-E1 repository structured/native/embedded representations and text hit inventory',
        'files_scanned':len(manifests),'documents_parsed':documents,'json_parse_errors':len(errors),
        'empty_files':len(empty),'native_events_unique':len(events),'bundle_representations':len(bundles),
        'native_A05_decision_events':len(target_events),'original_state_neighbor_events':len(state_events),
        'RecordedDecision_representations':len(commands),'record_entities':len(records),'choice_evidence_representations':len(evidence),
        'grant_entities':len(grants),'recorded_decision_snapshots':len(snapshots),'HEAD_representations':len(heads),
        'genesis_representations':len(genesis),'embedded_JSON_decoded':len(embedded),
        'text_artifacts_inspected':len(text_audit),
        'text_JSON_fragments_parsed':sum(x['JSON_fragments_parsed'] for x in text_audit),
        'text_A05_event_occurrences':sum(x['native_event_occurrences'] for x in text_audit),
        'distinct_A05_event_identities':len({json.dumps(x['event']['identity'],sort_keys=True) for x in target_events}),
        'identity_bodies_target':sum(x['target'] for x in identity_bodies),
        'A05_native_capture_calls':0,'A05_result_application_calls':0,'A05_replay_calls':0,
        'events_constructed':0,'events_appended':0,'authorities_issued':0}
    save('file-search-manifest.json',{'files':manifests,'text_hits':hits,'empty_files':empty,'parse_errors':errors})
    save('event-search.json',{'unique_events':list(events.values()),'matching_A05_events':target_events,
        'original_state_neighbor_events':state_events,'identity_bodies':identity_bodies})
    save('persistence-search.json',{'bundles':bundles,'heads':heads,'genesis_ledgers':genesis})
    save('native-record-search.json',{'RecordedDecision_values':commands,'record_entities':records,
        'choice_evidence':evidence,'grant_entities':grants,'recorded_snapshots':snapshots,'embedded_JSON':embedded})
    save('search-summary.json',summary)
    save('text-audit.json',{'artifacts':text_audit})
    print(json.dumps(summary))


if __name__=='__main__':main()
