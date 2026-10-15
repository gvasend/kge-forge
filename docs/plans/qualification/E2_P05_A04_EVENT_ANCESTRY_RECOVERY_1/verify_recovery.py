"""Verify recovery artifacts and preservation without evaluating Planner state."""
import ast
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
REPORT = ROOT/'docs/plans/DETERMINISTIC_PLANNER_V0_1_E2_P05_A04_EVENT_ANCESTRY_RECOVERY_1.json'
MARKDOWN = REPORT.with_suffix('.md')


def read(path):
    return json.loads(path.read_bytes())


def lookup(document, pointer):
    for part in pointer.split('/')[1:] if pointer else ():
        part=part.replace('~1','/').replace('~0','~')
        document=document[int(part)] if isinstance(document,list) else document[part]
    return document


def pointer_document(raw, pointer):
    if pointer.startswith('@line:'):
        line, _, pointer=pointer[len('@line:'):].partition('/')
        document=json.loads(raw.splitlines()[int(line)-1])
        pointer='/'+pointer if pointer else ''
    elif pointer.startswith('@fenced-line:'):
        # Text witness pointers are absent in this recovery; do not assume JSON.
        raise AssertionError('Unexpected native text witness; inspect its source')
    else:
        document=json.loads(raw)
    parts=pointer.split('@decoded-json')
    document=lookup(document,parts[0])
    for part in parts[1:]:
        document=lookup(json.loads(document),part)
    return document


def main():
    baseline=read(OUT/'baseline.json')
    cache={}
    def digest(path):
        name=str(path.relative_to(ROOT))
        if name not in cache:
            cache[name]=hashlib.sha256(path.read_bytes()).hexdigest()
        return cache[name]
    changed=[]
    for name,expected in baseline['files'].items():
        path=ROOT/name
        if not path.is_file() or digest(path)!=expected:
            changed.append(name)
    assert not changed,changed
    current=set(subprocess.run(['rg','--files','docs/plans','adapter/planner','docs/experiments/E1'],
        cwd=str(ROOT),check=True,capture_output=True,text=True).stdout.splitlines())
    added=sorted(current-set(baseline['files']))
    allowed={str(REPORT.relative_to(ROOT)),str(MARKDOWN.relative_to(ROOT))}
    assert all(n in allowed or n.startswith(str(OUT.relative_to(ROOT))+'/') for n in added),added
    assert {n for n in current if n.startswith('docs/experiments/E1/')}=={
        n for n in baseline['files'] if n.startswith('docs/experiments/E1/')}
    syntax=[]
    for path in sorted(OUT.glob('*.py')):
        ast.parse(path.read_text(),filename=str(path))
        syntax.append(str(path.relative_to(ROOT)))
    report=read(REPORT)
    assert report['RESULT']=='BLOCKED'
    assert report['LOSSLESS_RECOVERY']=='NO' and report['ANCESTRY_CLASSIFICATION']=='NO_NATIVE_ANCESTRY'
    assert report['A04_EVENT'] is None and report['A04_PARENT'] is None and report['LEDGER_MEMBERSHIP'] is None
    assert report['E2_A04_PREPARE_RESULT_EVENT_ANCESTRY']=='FAIL'
    assert report['P05_BOUND_STAGE_INPUTS']==10 and report['P05_EXECUTION_READY']=='NO'
    assert report['P05_NEXT_MISSING_INPUT']=='E2-A04.prepare_result_event_ancestry'
    assert all(report[k]=='NO' for k in ('A04_REPRODUCED','P05_EXECUTED','P06_EXECUTED',
        'RUNTIME_MODIFIED','PRODUCTION_EFFECT','NEW_AUTHORITY_ISSUED'))
    assert report['NATIVE_EXECUTION_ADMISSION_REPLAY_CALLS']==0
    assert report['ORIGINAL_A03_HISTORICAL_OCCURRENCE']=='UNPROVEN'
    assert report['P03_HISTORICAL_CORRESPONDENCE']=='UNPROVEN' and report['N_REAL_SATISFIED']=='NO'
    frontier=read(OUT/'P05-binding-frontier.json')
    assert sum(s['binding_status']=='BOUND' for s in frontier['current_bindings'])==10
    assert next(s for s in frontier['current_bindings'] if s['stage']=='E2-A04')['binding_status']!='BOUND'
    assert frontier['A04_new_binding_created'] is False
    decision=read(OUT/'scope-decision-dossier.json')
    assert decision['selected_option'] is None
    body=json.dumps(decision['subject'],sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
    subject='qualification-scope-subject-v1:'+hashlib.sha256(body).hexdigest()
    assert subject==decision['subject_identity']==report['SCOPE_SUBJECT_ID']
    assert subject in MARKDOWN.read_text()
    search=read(OUT/'search-summary.json')
    assert search['parse_errors']==0 and search['A04_event_occurrences']==0
    assert search['original_state_event_occurrences']==0
    corpus=read(OUT/'search-corpus.json')
    assert all((ROOT/x['path']).read_bytes()==b'' for x in corpus['non_event_records'])
    assert report['CANONICAL_EVENT_SEARCH']==search
    assert 'verification.json' in MARKDOWN.read_text()
    pins,pointers=0,0
    # Verify all search and conclusion pins, including embedded-JSON coordinates.
    for path in sorted(OUT.glob('*.json'))+[REPORT]:
        if path.name in ('baseline.json','verification.json'):
            continue
        queue=[read(path)]
        while queue:
            value=queue.pop()
            if isinstance(value,dict):
                if 'path' in value and 'raw_sha256' in value:
                    pinned=ROOT/value['path']
                    assert pinned.is_file(),value
                    assert digest(pinned)==value['raw_sha256'],value
                    pins+=1
                    pointer=value.get('pointer','')
                    if pointer:
                        pointer_document(pinned.read_bytes(),pointer)
                        pointers+=1
                queue.extend(value.values())
            elif isinstance(value,list):
                queue.extend(value)
    diff=subprocess.run(['git','diff','--check'],cwd=str(ROOT),capture_output=True,text=True)
    assert diff.returncode==0,diff.stdout+diff.stderr
    report['GIT_DIFF_CHECK']='PASS'
    report['verification_artifact']={'path':str((OUT/'verification.json').relative_to(ROOT))}
    REPORT.write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')
    verification={'result':'PASS','preexisting_files_checked':len(baseline['files']),
        'changed_preexisting_files':changed,'frozen_E1_root_files_preserved':baseline['frozen_E1_file_count'],
        'copied_E1_policy_fixtures_preserved':sum('/E1/' in n and not n.startswith('docs/experiments/E1/') for n in baseline['files']),
        'runtime_files_preserved':baseline['runtime_file_count'],'new_files_confined_to_requested_recovery_outputs':True,
        'new_files_at_check':added,'artifact_pin_checks':pins,'source_pointer_checks':pointers,
        'native_identity_and_parent_inspection':'PASS; pure decoding/serialization only, no semantic admission/replay',
        'P05_frontier_checks':'PASS; 10/13, A04 remains first missing input, no new binding',
        'scope_subject_hash_check':'PASS','scope_option_selected':None,
        'native_transition_admission_replay_calls':0,'recovery_script_syntax':'PASS','scripts':syntax,
        'historical_label_and_release_separation_checks':'PASS','git_diff_check':'PASS',
        'RUNTIME_MODIFIED':'NO','E1_ARTIFACTS_MODIFIED':0,'PRODUCTION_EFFECT':'NO'}
    (OUT/'verification.json').write_text(json.dumps(verification,sort_keys=True,indent=2)+'\n')
    print(json.dumps({k:v for k,v in verification.items() if k not in ('new_files_at_check','scripts')}))


if __name__=='__main__':
    main()
