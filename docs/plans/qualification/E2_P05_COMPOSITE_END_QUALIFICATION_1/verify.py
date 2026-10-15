"""Final source, scope, graph, oracle and preservation integrity audit."""
import ast
import hashlib
import json
import re
import subprocess
from qualify import ROOT, OUT, SEALED, DOCS, PREFIX, BASE_ID, SUBJECT_ID, OPTION, read, ref, save, sealed, c


def main():
    auth=read(OUT/'scope-authentication.json')
    original={k:v for k,v in auth.items() if k!='identity'}
    assert auth['identity']==sealed.qid('qualification-END-scope-authentication-v1',original)
    assert auth['SELECTED_OPTION']==OPTION and auth['qualification_scope_subject']==SUBJECT_ID
    assert read(SEALED/'aggregate-END-decision-dossier.json')['selected_option']=='NONE'
    mapping=read(OUT/'qualified-composite-mapping.json')
    identity=mapping['qualification_identity']
    assert identity==sealed.qid('qualification-composite-END-acceptance-v1',{k:v for k,v in mapping.items() if k!='qualification_identity'})
    graph=read(SEALED/'qualified-evidence-graph.json')['graph']
    assert mapping['base_graph_identity']==BASE_ID==sealed.qid('qualification-END-evidence-graph-v1',graph)
    assert mapping['overlay']['stage_bindings']==[n['original_stage_binding_retained_exact'] for n in graph['stage_nodes']]
    assert len(mapping['bridge_checks'])==len(mapping['overlay']['bridges'])==4
    assert [b['BRIDGE_ID'] for b in mapping['bridge_checks']]==auth['bridge_ids']
    assert all(not b['native_handoff_proven'] for b in mapping['bridge_checks'])
    assert all(b['RESULT']=='PASS' for b in mapping['bridge_checks'])
    assert mapping['aggregate_N12']['RESULT']==mapping['aggregate_N13']['RESULT']=='PASS'
    assert len(mapping['aggregate_N12']['terms'])==len(mapping['aggregate_N13']['terms'])==6
    assert mapping['overlay']['pass_claim']==auth['pass_claim']
    assert mapping['overlay']['excluded_claims']==auth['excluded_claims']
    assert not mapping['overlay']['native_history_changed'] and not mapping['overlay']['native_permissions_changed']
    assert not mapping['overlay']['continuous_original_lineage_proven'] and not mapping['overlay']['continuous_new_mainline_proven']
    assert read(OUT/'negative-results.json')['count']==16
    assert all(c['RESULT']=='PASS' for c in read(OUT/'negative-results.json')['cases'])
    readers=[read(p) for p in (OUT/'readers').glob('*.json')]
    assert len(readers)==12 and {r['seed'] for r in readers}=={'0','1','7','101'}
    assert all(r['RESULT']=='PASS' and r['qualification_identity']==identity and not r['native_lifecycle_calls'] for r in readers)
    oracle=read(OUT/'END-oracle-results.json')
    assert oracle['COMPOSITE_P05_END_QUALIFICATION']=='FAIL'
    failures=[e for e in oracle['edge_terms'] if e['RESULT']=='FAIL_NOT_BOUND']
    assert len(failures)==6
    assert oracle['FIRST_REMAINING_BLOCKER']['edge_id']==failures[0]['edge_id']
    old_dossier=read(ROOT/auth['dossier']['path'])
    pinned_oracle=old_dossier['subject']['acceptance_oracle']
    assert oracle['FIRST_REMAINING_BLOCKER']['source']['path']==pinned_oracle['path']
    assert oracle['FIRST_REMAINING_BLOCKER']['source']['raw_sha256']==pinned_oracle['raw_sha256']
    assert oracle['FIRST_REMAINING_BLOCKER']['not_new_criterion']
    assert read(OUT/'P05-readiness-result.json')['FULL_P05_READINESS_RERUN_PERFORMED'] is False
    assert read(OUT/'P05-readiness-result.json')['P05_EXECUTION_READY']=='NO'
    baseline=read(OUT/'baseline.json')['files']
    changed=[p for p,h in baseline.items() if not (ROOT/p).is_file() or hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h]
    assert not changed,changed
    report_path=DOCS/(PREFIX+'E2_P05_COMPOSITE_END_QUALIFICATION_1.json')
    report=read(report_path)
    assert report['RESULT']=='PARTIAL' and report['SCOPE_AUTHENTICATION']=='PASS'
    assert report['P05_BOUND_STAGE_INPUTS']==13 and report['COMPOSITE_P05_END_QUALIFICATION']=='FAIL'
    assert report['P05_EXECUTED']==report['P06_EXECUTED']=='NO'
    checked=set()
    for path in list(OUT.rglob('*.json'))+[report_path]:
        if path.name in ('baseline.json','verification.json'):continue
        for pin in sealed.pins(read(path)):
            target=ROOT/pin['path']
            assert hashlib.sha256(target.read_bytes()).hexdigest()==pin['raw_sha256'],pin['path']
            if pin.get('pointer') and target.suffix=='.json':sealed.pointers(read(target),pin['pointer'])
            checked.add((pin['path'],pin['raw_sha256'],pin.get('pointer','')))
    for path in OUT.glob('*.py'):ast.parse(path.read_text(),str(path))
    md=report_path.with_suffix('.md')
    for target in re.findall(r'\]\(([^)]+)\)',md.read_text()):
        path=md.parent/re.sub(r':\d+$','',target)
        assert path.is_file() or path==OUT/'verification.json',target
    assert not sealed.CALLS
    check=subprocess.run(['git','diff','--check'],cwd=str(ROOT),capture_output=True,text=True)
    assert check.returncode==0
    save(OUT/'verification.json',{'RESULT':'PASS','scope_authentication':'PASS','baseline_files_unchanged':len(baseline),
        'original_stage_bindings_and_native_histories_unchanged':True,'source_pointer_identity_checks':len(checked),
        'bridge_count':4,'negative_controls_passed':16,'fresh_readers':12,'base_graph_identity':BASE_ID,
        'accepted_mapping_identity':identity,'scope_subject':SUBJECT_ID,'complete_END_oracle':'FAIL_UNBOUND_INTERFACE_INPUTS',
        'known_sealed_gap_not_new_criterion':True,'P05_EXECUTION_READY':'NO','P05_EXECUTED':'NO','P06_EXECUTED':'NO',
        'native_lifecycle_calls':sealed.CALLS,'RUNTIME_MODIFIED':'NO','E1_ARTIFACTS_MODIFIED':0,'PRODUCTION_EFFECT':'NO',
        'git_diff_check':'PASS','reports':[ref(report_path),ref(md)],'harnesses':[ref(p) for p in sorted(OUT.glob('*.py'))]})
    print(json.dumps({'VERIFICATION':'PASS','RESULT':'PARTIAL','scope':'PASS','bridges':4,'stage_bindings':'13/13',
                      'complete_END':'FAIL_UNBOUND_INTERFACES','P05_EXECUTION_READY':'NO','preserved_files':len(baseline)}))


if __name__=='__main__':main()
