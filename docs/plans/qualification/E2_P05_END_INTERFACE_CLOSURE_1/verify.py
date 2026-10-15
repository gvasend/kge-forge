"""Verify recovered document identities, scope limits and zero binding mutation."""
import ast
import hashlib
import json
import re
import subprocess
from recover import ROOT, OUT, DOCS, P, REC, QUAL, read, ref, save


def pins(value):
    if isinstance(value,dict):
        if isinstance(value.get('path'),str) and isinstance(value.get('raw_sha256'),str):yield value
        for child in value.values():yield from pins(child)
    elif isinstance(value,list):
        for child in value:yield from pins(child)


def pointer(value,expression):
    for token in expression.split('/')[1:]:
        token=token.replace('~1','/').replace('~0','~')
        value=value[int(token)] if isinstance(value,list) else value[token]
    return value


def main():
    baseline=read(OUT/'baseline.json')['files']
    changed=[name for name,expected in baseline.items() if not (ROOT/name).is_file() or hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=expected]
    assert not changed,changed
    inventory=read(OUT/'six-interface-inventory.json')
    declared=read(DOCS/(P+'E2_PC04_END.json'))['dependencies']
    assert inventory['authoritative_order']==declared and inventory['count']==6
    assert [r['SOURCE'] for r in inventory['interfaces']]==declared
    allowed=set(inventory['allowed_dimension_statuses'])
    dims={'SOURCE_DEFINITION','SOURCE_INSTANCE','CONSUMER_DEFINITION','CONSUMER_BINDING','PROCESS_DEFINITION','PROCESS_BINDING','CURRENTNESS','SCOPE','LINEAGE','PROVENANCE'}
    for row in inventory['interfaces']:
        assert set(row['STATUS'])==dims
        assert set(row['STATUS'].values()).issubset(allowed)
        assert row['STATUS']['CONSUMER_BINDING']==row['STATUS']['PROCESS_BINDING']=='MISSING'
        assert row['TARGET']=='E2-END' and row['DECLARED_NATIVE_INTERFACE_ID'] is None
    pc01=inventory['interfaces'][0]
    assert pc01['STATUS']['SOURCE_DEFINITION']==pc01['STATUS']['SOURCE_INSTANCE']=='PASS'
    findings=read(OUT/'root-cause-and-readiness.json')
    assert findings['ROOT_CAUSE']=='MISSING_FIXTURE_BINDING'
    assert findings['FIRST_UNRESOLVED_INTERFACE']=='E2-PC01 -> E2-END'
    assert findings['DECISION_REQUIRED']==findings['IMPLEMENTATION_REQUIRED']=='NO'
    minimum=read(OUT/'minimum-PC01-closure-contract.json')
    assert minimum['STATUS']=='CONTRACT_ONLY_NOT_MATERIALIZED_OR_APPLIED'
    assert minimum['no_code_or_binding_created_here']
    assert minimum['identity']['consumer_edge_id']==pc01['SEALED_EDGE_ID']
    assert not minimum['authority']['new_authority_required']
    assert minimum['authority']['INSTALL_configuration']['status']=='NOT_REQUIRED'
    assert minimum['authority']['runtime_USE_or_execution']['status']=='NOT_REQUIRED'
    usage=read(OUT/'PC01-reference-consumer-inventory.json')
    assert usage['matching_artifacts']==len(usage['artifacts'])==954
    assert all(r['source']['path'] in baseline for r in usage['artifacts'])
    assert all(r['operative_consumption_not_inferred_from_text'] for r in usage['artifacts'])
    assert not usage['closed_bridge_qualifications_reexecuted']
    report_path=DOCS/(P+'E2_P05_END_INTERFACE_CLOSURE_1.json')
    report=read(report_path)
    assert report['RESULT']=='PASS' and report['END_INTERFACE_COUNT']==6
    assert report['DECISION_READY']==report['IMPLEMENTATION_READY']=='NO'
    assert report['P05_STAGE_BINDINGS']=='13/13'
    assert report['FOUR_SEMANTIC_BRIDGES']==report['AGGREGATE_N12']==report['AGGREGATE_N13']=='PASS'
    assert report['COMPOSITE_P05_END_QUALIFICATION']=='FAIL' and report['P05_EXECUTION_READY']=='NO'
    assert report['P05_EXECUTED']==report['P06_EXECUTED']==report['RUNTIME_MODIFIED']=='NO'
    checked=set()
    for path in list(OUT.glob('*.json'))+[report_path]:
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
    # Fixed before-work hash inventory protects qualified bridge results,
    # scope/authentication, all native input states, runtime and frozen E1.
    check=subprocess.run(['git','diff','--check'],cwd=str(ROOT),capture_output=True,text=True)
    assert check.returncode==0
    save('verification.json',{'RESULT':'PASS','baseline_files_unchanged':len(baseline),
        'source_pointer_identity_checks':len(checked),'interfaces_in_authoritative_order':6,
        'all_ten_dimensions_per_interface_explicit':True,'PC01_source_instance_presence_not_consumer_binding':True,
        'consumer_and_process_gap':'MISSING_FIXTURE_BINDING','native_adapter_INSTALL_or_authority_gap_established':False,
        'PC01_retained_reference_artifacts':954,'closed_qualifications_reexecuted':False,'bindings_modified':0,
        'native_runtime_operations_called':0,'P05_EXECUTED':'NO','P06_EXECUTED':'NO','P05_EXECUTION_READY':'NO',
        'RUNTIME_MODIFIED':'NO','E1_ARTIFACTS_MODIFIED':0,'PRODUCTION_EFFECT':'NO','git_diff_check':'PASS',
        'reports':[ref(report_path),ref(md)],'harnesses':[ref(p) for p in sorted(OUT.glob('*.py'))]})
    print(json.dumps({'VERIFICATION':'PASS','baseline_unchanged':len(baseline),'interfaces':6,
        'bindings_modified':0,'native_runtime_operations':0,'P05_EXECUTION_READY':'NO','git_diff_check':'PASS'}))


if __name__=='__main__':main()
