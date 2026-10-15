"""Independent trusted source/consumer oracle, sealed before materialization.

Expected Action/model values come directly from retained JSON bytes, declared
PC01 semantics and the recovered consumer contract. This program does not call
materialized(), action_row(), preflight() or any native model operation.
"""
from copy import deepcopy
import json
from binding import (ROOT, OUT, DOCS, P, CLOSURE, BASE_ID, ACCEPTANCE_ID, INPUT_ID, c, m,
    read, ref, save, qid, source_specs, process_definition, consumer, inputs, equal, check_pins)


def normalize(value):
    if isinstance(value,list):return [normalize(x) for x in value]
    if isinstance(value,dict):
        result={k:normalize(v) for k,v in value.items()}
        cls=c.TYPES.get(value.get('$type'))
        for name in c.SET_FIELDS.get(cls,set()):
            if name in result:result[name]=sorted(result[name],key=c.canonical_bytes)
        return result
    return value


def select(value,expression):
    for token in expression.split('/')[1:]:
        token=token.replace('~1','/').replace('~0','~')
        value=value[int(token)] if isinstance(value,list) else value[token]
    return value


def main():
    verify=read(CLOSURE/'verification.json')
    for item in verify['reports']+verify['harnesses']:check_pins(item)
    minimum=read(CLOSURE/'minimum-PC01-closure-contract.json');check_pins(minimum)
    declaration=read(ROOT/minimum['source']['definition']['path'])
    qualification=read(DOCS/(P+'E2_PC01_EXIT_RECONCILIATION_1.json'))
    equal('original qualified PC01 exit',qualification['e2_pc01_result'],'PASS')
    action_ids=sorted(d['id'] for d in declaration['declarations']);equal('exact declared Action count',len(action_ids),6)
    expected_models=[]
    for spec in source_specs():
        state=select(read(ROOT/spec['source']['path']),spec['source']['pointer'])
        equal('independent source context',state['context'],spec['context'])
        equal('independent six-Action source membership',sorted(a['id']['value'] for a in state['actions']),action_ids)
        rows=[]
        for raw in sorted(state['actions'],key=lambda a:a['id']['value']):
            action=normalize(raw);name=action['id']['value'];d=next(x for x in declaration['declarations'] if x['id']==name)
            equal('independent PC01 operation contract',action['operation']['value'],d['operation'])
            equal('independent PC01 effect contract',action['effect']['value'],d['effect'])
            status=next(s for s in state['statuses'] if s['id']==action['id'])
            rows.append({'ACTION_ID':name,'TYPE':action['operation']['value'],'EFFECT':action['effect']['value'],
                'STATE':status['state']['value'],'PREREQUISITES':action['prerequisites'],
                'ACCEPTED_INVENTORY':action['accepted_inventory'],
                'RESULT_OUTPUT_DECLARATIONS':{'accepted_result':action.get('accepted_result',{'value':'PASS'})['value'],
                    'prepared_dossier':action.get('prepared_dossier'),'accepted_inventory_is_prospective':True,
                    'pass_model_complete':action.get('pass_model_complete',False)},
                'scope':spec['context']['scope'],'lineage':spec['context']['lineage'],'generation':spec['context']['generation'],
                'provenance':action['source'],'native_definition':action,
                'definition_comparison_identity':qid('qualification-native-action-view-v1',action),
                'source_snapshot':spec['snapshot_id'],'no_actual_result_created_from_declaration':True})
        expected_models.append(dict(spec,actions=rows,source_identity={'file_content':'raw-file-sha256:'+spec['source']['raw_sha256'],
            'native_Snapshot':spec['snapshot_id']},accepted_inventory_not_actual_Knowledge=True))
    process=process_definition()
    body={'schema':'PC01-END-QUALIFICATION-PROJECTION-1','kind':'QUALIFICATION_EVIDENCE_NOT_NATIVE_STATE',
        'PC01_definition':ref(DOCS/(P+'E2_PC01_SOURCES.json')),
        'PC01_qualification':ref(DOCS/(P+'E2_PC01_EXIT_RECONCILIATION_1.json')),
        'PC01_RESULT':'PASS','action_ids':action_ids,'models':expected_models,'consumer':consumer(),
        'process_identity':process['identity'],'process_definition':process['process'],
        'scope':'E2-QUALIFICATION-ONLY','lineage_policy':'Each native context retained separately; no native lineage synthesized',
        'currentness_boundary':'Current documentary END consumption of exact qualified historical/current model roles; not Action execution permission',
        'new_native_Snapshot_Action_event_INSTALL_authority':False}
    save('expected-oracle.json',{'schema':'PC01-END-INDEPENDENT-BINDING-ORACLE-1',
        'authorship':'Retained source JSON plus PC01 declaration and consumer/process contracts, before evaluating materialized output',
        'expected_projection':body,'expected_action_ids':action_ids,
        'expected_native_model_admission':'PASS','comparator_only':True,
        'expected_input_ids':['PC01_DEFINITION_SOURCE','PC01_QUALIFICATION','ORIGINAL_NATIVE_MODEL','CURRENT_NATIVE_MODEL',
            'END_CONSUMER','PROCESS_CONTRACT','SCOPE_CAPTURE','COMPOSITE_GRAPH','QUALIFIED_ACCEPTANCE_MAPPING',
            'GOVERNED_DEFINITION_HISTORY','SUPPORTED_POLICY','INDEPENDENT_BINDING_ORACLE']})
    projid=qid('qualification-PC01-END-projection-v1',body)
    rows=[]
    for input_id,expected_type,source in inputs():
        rows.append({'INPUT_ID':input_id,'EXPECTED_TYPE':expected_type,'SOURCE_ARTIFACT':source,
            'SOURCE_IDENTITY':'raw-file-sha256:'+source['raw_sha256'],'SOURCE_VALUE_SEMANTICS':expected_type,
            'PROJECTION_IDENTITY':projid,'CONSUMER':consumer(),'PROCESS':process['identity'],'SCOPE':'E2-QUALIFICATION-ONLY',
            'LINEAGE':'Exact source native context if present; otherwise declared source/contract scope, not an invented native lineage',
            'PROVENANCE':source,'CURRENTNESS':'Exact source pin and required declared consumer-boundary role; comparator distinguished from operative input',
            'input_role':'COMPARISON_ONLY' if input_id=='INDEPENDENT_BINDING_ORACLE' else 'PINNED_QUALIFICATION_INPUT'})
    manifest={'schema':'PC01-END-INVOCATION-INPUT-MANIFEST-1','projection_identity':projid,
        'interface':INPUT_ID,'consumer':consumer(),'process':process,'inputs':rows,
        'environment':{'PYTHONDONTWRITEBYTECODE':'1','PYTHONPATH':'.'},
        'invocation':process['process']['invocations'],'permitted_parameters':{'seeds':[0,1,7,101],'reader_indices':[1,2,3],'presentations':['original','reversed','rotated']},
        'writer':'Metadata materialization only, from pinned retained native sources; no producer PC01 rerun',
        'reader_allowlist':[r['SOURCE_ARTIFACT'] for r in rows],
        'process_edges':['PC01 sources -> exact historical/current definition model projection','projection -> invocation/input manifest',
            'manifest -> E2-END#/dependencies/0 qualified consumer'],'P05_EXECUTED':False,'native_mutating_operations':[]}
    save('expected-manifest-oracle.json',{'expected_manifest':manifest,'comparator_only':True,
        'no_writer_output_used_to_choose_expected_source_or_value':True})
    names=['wrong_PC01_Snapshot','wrong_PC01_qualification','five_Actions','seven_Actions','wrong_Action_identity','foreign_Action',
        'wrong_consumer','wrong_process','missing_manifest_input','extra_manifest_input','wrong_source_identity','wrong_projection_identity',
        'wrong_scope','wrong_lineage','wrong_provenance','stale_source','unordered_presentation_semantic_difference','report_only_source']
    save('negative-plan.json',{'cases':[{'id':'PC01-END-N%02d'%(i+1),'name':name,'expected':'REJECT_BEFORE_INTERFACE_PASS'} for i,name in enumerate(names)],
        'count':18,'sealed_before_positive_preflight':True,'native_sources_or_state_not_mutated':True,
        'unordered_semantics':'Valid Action set permutations are equivalent. A fabricated order-sensitive projection identity is rejected.'})
    save('source-pins.json',{'PC01_RESULT':'PASS','selected_sources':source_specs(),
        'minimum_contract':ref(CLOSURE/'minimum-PC01-closure-contract.json'),'consumer_contract':ref(CLOSURE/'END-PC01-consumer-contract.json'),
        'PC01_definition':ref(DOCS/(P+'E2_PC01_SOURCES.json')),'PC01_qualification':ref(DOCS/(P+'E2_PC01_EXIT_RECONCILIATION_1.json')),
        'policy':ref(ROOT/'docs/experiments/E1/E1_GRAPH_RESOLUTION_SELECTION_POLICY_1.md'),
        'process_definition':process,'closed_bridges_revisited':False,'no_new_native_sources':True})
    print(json.dumps({'INDEPENDENT_ORACLE':'SEALED','Actions':action_ids,'projection_identity_expected':projid,
                      'manifest_identity_expected':qid('qualification-PC01-END-manifest-v1',manifest),'negative_cases':18}))


if __name__=='__main__':main()
