"""Final qualified binding/source/process identity and preservation verification."""
import ast
import hashlib
import json
import re
import subprocess
from binding import ROOT, OUT, DOCS, P, CLOSURE, BASE_ID, ACCEPTANCE_ID, read, ref, save, pins, pointer, qid, CALLS


def main():
    p=read(OUT/'END-projection.json');manifest=read(OUT/'invocation-input-manifest.json')
    expected=read(OUT/'expected-oracle.json');expected_manifest=read(OUT/'expected-manifest-oracle.json')
    assert p['identity']==qid('qualification-PC01-END-projection-v1',p['projection'])
    assert manifest['identity']==qid('qualification-PC01-END-manifest-v1',manifest['manifest'])
    assert p['projection']==expected['expected_projection'] and manifest['manifest']==expected_manifest['expected_manifest']
    assert p['projection']['consumer']['composite_graph_identity']==BASE_ID
    assert p['projection']['consumer']['acceptance_mapping_identity']==ACCEPTANCE_ID
    assert len(p['projection']['action_ids'])==6
    assert len({a for a in p['projection']['action_ids']})==6
    assert len(p['projection']['models'])==2
    for model in p['projection']['models']:
        assert len(model['actions'])==6
        assert [a['ACTION_ID'] for a in model['actions']]==p['projection']['action_ids']
    assert len(manifest['manifest']['inputs'])==12
    assert len(manifest['manifest']['process']['process']['invocations']['readers'])==36
    assert manifest['manifest']['process']['identity']==qid('qualification-PC01-END-process-v1',manifest['manifest']['process']['process'])
    negatives=read(OUT/'negative-results.json')
    assert negatives['count']==len(negatives['cases'])==18 and all(case['RESULT']=='PASS' for case in negatives['cases'])
    assert read(OUT/'preflight.json')['PC01_END_INTERFACE']=='PASS'
    assert read(OUT/'currentness-provenance-policy.json')['RESULT']=='PASS'
    readers=[read(path) for path in (OUT/'readers').glob('*.json')]
    assert len(readers)==36 and {r['seed'] for r in readers}=={'0','1','7','101'}
    assert {r['presentation'] for r in readers}=={'original','reversed','rotated'}
    assert all(r['PC01_END_INTERFACE']=='PASS' and r['projection_identity']==p['identity'] and r['manifest_identity']==manifest['identity'] and not r['native_mutating_calls'] for r in readers)
    for seed in ('0','1','7','101'):
        for form in ('original','reversed','rotated'):assert len([r for r in readers if r['seed']==seed and r['presentation']==form])==3
    frontier=read(OUT/'six-interface-frontier.json')
    old=read(CLOSURE/'six-interface-inventory.json')
    assert frontier['interfaces'][1:]==old['interfaces'][1:]
    assert frontier['END_INTERFACES_BOUND']==1 and frontier['END_INTERFACE_COUNT']==6
    assert frontier['NEXT_UNRESOLVED_INTERFACE']==old['interfaces'][1]['SOURCE']+' -> E2-END'
    assert frontier['P05_STAGE_BINDINGS']=='13/13' and frontier['P05_EXECUTION_READY']=='NO'
    baseline=read(OUT/'baseline.json')['files']
    changed=[name for name,expected_sha in baseline.items() if not (ROOT/name).is_file() or hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=expected_sha]
    assert not changed,changed
    report_path=DOCS/(P+'E2_P05_PC01_END_BINDING_1.json')
    report=read(report_path)
    assert report['RESULT']=='PASS' and report['PC01_END_INTERFACE']=='PASS'
    assert report['NATIVE_STATE_CHANGED']=='NO' and report['INSTALL_EVENTS']==report['NEW_AUTHORITIES']==0
    assert report['P05_EXECUTED']==report['P06_EXECUTED']=='NO'
    assert report['P05_EXECUTION_READY']=='NO'
    checked=set()
    for path in list(OUT.rglob('*.json'))+[report_path]:
        if path.name in ('baseline.json','verification.json'):continue
        for pin in pins(read(path)):
            source=ROOT/pin['path']
            assert hashlib.sha256(source.read_bytes()).hexdigest()==pin['raw_sha256'],pin['path']
            if pin.get('pointer') and source.suffix=='.json':pointer(read(source),pin['pointer'])
            checked.add((pin['path'],pin['raw_sha256'],pin.get('pointer','')))
    for path in OUT.glob('*.py'):ast.parse(path.read_text(),str(path))
    md=report_path.with_suffix('.md')
    for link in re.findall(r'\]\(([^)]+)\)',md.read_text()):
        source=md.parent/re.sub(r':\d+$','',link)
        assert source.is_file() or source==OUT/'verification.json',link
    check=subprocess.run(['git','diff','--check'],cwd=str(ROOT),capture_output=True,text=True)
    assert check.returncode==0 and not CALLS
    save('verification.json',{'RESULT':'PASS','PC01_END_INTERFACE':'PASS','projection_identity':p['identity'],
        'manifest_identity':manifest['identity'],'process_identity':p['projection']['process_identity'],
        'source_pointer_identity_checks':len(checked),'native_models_admitted':2,'Actions_per_model':6,
        'independent_expected_projection_and_manifest_match':True,'negative_cases_passed':18,'fresh_readers':36,
        'END_INTERFACES_BOUND':1,'END_INTERFACE_COUNT':6,'NEXT_UNRESOLVED_INTERFACE':'E2-PC02 -> E2-END',
        'remaining_five_records_unchanged':True,'baseline_files_unchanged':len(baseline),
        'NATIVE_STATE_CHANGED':'NO','INSTALL_EVENTS':0,'NEW_AUTHORITIES':0,'P05_EXECUTED':'NO','P06_EXECUTED':'NO',
        'P05_EXECUTION_READY':'NO','RUNTIME_MODIFIED':'NO','E1_ARTIFACTS_MODIFIED':0,'PRODUCTION_EFFECT':'NO',
        'native_mutating_calls':CALLS,'git_diff_check':'PASS','reports':[ref(report_path),ref(md)],
        'harnesses':[ref(path) for path in sorted(OUT.glob('*.py'))]})
    print(json.dumps({'VERIFICATION':'PASS','PC01_END_INTERFACE':'PASS','interfaces':'1/6','next':'E2-PC02 -> E2-END',
        'baseline_unchanged':len(baseline),'native_state_changed':'NO','P05_EXECUTION_READY':'NO','git_diff_check':'PASS'}))


if __name__=='__main__':main()
