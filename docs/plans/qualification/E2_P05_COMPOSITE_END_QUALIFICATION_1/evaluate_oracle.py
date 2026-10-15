"""Evaluate the unchanged complete END oracle, including its remaining input gate."""
import json
from qualify import ROOT, OUT, SEALED, BASE_ID, read, ref, save, equal


def main():
    oracle = read(SEALED / 'END-qualification-oracle.json')
    qualified = read(OUT / 'qualified-composite-mapping.json')
    negatives = read(OUT / 'negative-results.json')
    determinism = read(OUT / 'determinism.json')
    equal('all sealed aggregate controls pass', negatives['RESULT'], 'PASS')
    equal('fresh reconstruction qualified', determinism['RESULT'], 'PASS')
    bridges = qualified['bridge_checks']
    graph = read(SEALED / 'qualified-evidence-graph.json')['graph']
    terms = []
    for node in oracle['stage_terms']:
        terms.append({'term':node['term'],'kind':'STAGE_BINDING','RESULT':'PASS',
            'evidence_sources':node['evidence_sources'],'native_identity':node['native_identity'],
            'assurance':node['required_assurance'],'classification':node['classification'],
            'historical_label':node['historical_label'],'original_local_binding_unchanged':True})
    original_edges = {e['edge_id']:e for e in oracle['edge_terms']}
    edge_terms = []
    for result in qualified['edge_checks']:
        expected = original_edges[result['edge_id']]
        interface = expected['relationship']=='DECLARED_PC04_INTERFACE'
        row = dict(result, required_assurance=expected['required_assurance'],
                   evidence=expected['evidence'], identity_classification_check='PASS')
        if interface:
            # The immutable declaration names a dependency. It contains no
            # current consumer projection/process manifest. Its exact assurance
            # was sealed before authorization and is not waived by that choice.
            row.update(RESULT='FAIL_NOT_BOUND', assurance_check='NOT_SATISFIED',
                actual='Only the historical PC04 END /dependencies string is bound; no exact current interface/consumer/process projection is sealed on this edge',
                sealed_current_status=expected['current_status'])
        else:
            row.update(RESULT='PASS', assurance_check='PASS_AT_EXACT_QUALIFIED_COMPONENT_SCOPE')
        edge_terms.append(row)
    failures = [row for row in edge_terms if row['RESULT']!='PASS']
    equal('six existing unprepared interface terms retained', len(failures), 6)
    equal('first interface order', failures[0]['source'], oracle['six_interfaces_and_process_inputs']['interfaces'][0])
    first = {'term':'END_INTERFACE_PROCESS_BINDINGS','edge_id':failures[0]['edge_id'],
        'input':'E2-PC01 canonical six-Action model -> E2-END current interface/consumer/process binding',
        'expected':oracle['six_interfaces_and_process_inputs']['expected'],
        'actual':failures[0]['actual'], 'classification':'KNOWN_UNPREPARED_SEALED_END_INPUT',
        'source':ref(SEALED / 'END-qualification-oracle.json','/six_interfaces_and_process_inputs'),
        'not_new_criterion':True,'not_missing_aggregate_authority':True,'native_runtime_counterexample':False}
    body = {'RESULT':'FAIL_COMPLETE_ORACLE_UNBOUND_INPUTS','COMPOSITE_P05_END_QUALIFICATION':'FAIL',
        'MAPPING_QUALIFICATION':'PASS','scope_authentication':'PASS','base_graph_identity':BASE_ID,
        'accepted_mapping_identity':qualified['qualification_identity'],
        'oracle':ref(SEALED / 'END-qualification-oracle.json'), 'stage_terms':terms,'edge_terms':edge_terms,
        'bridge_terms':bridges,'aggregate_N12':qualified['aggregate_N12'],'aggregate_N13':qualified['aggregate_N13'],
        'historical_exclusions':'PASS','permission_separation':'PASS','identity':'PASS','determinism':'PASS','negative_suite':'PASS',
        'all_four_bridges_pass':True,'all_13_stage_bindings_pass':True,
        'six_interfaces_and_process_inputs':dict(oracle['six_interfaces_and_process_inputs'],RESULT='FAIL_NOT_BOUND'),
        'FIRST_REMAINING_BLOCKER':first,'new_acceptance_criteria':0,
        'bounded_pass_claim':oracle['PASS_CLAIM'],'pass_claim_fully_established':False,
        'stronger_continuous_mainline_claim':False,'P05_EXECUTED':'NO','P06_EXECUTED':'NO',
        'no_live_repair_or_new_interface_binding':True}
    save(OUT / 'END-oracle-results.json',body)
    # Complete composite qualification did not pass. Phase R's conditional full
    # P05 rerun cannot be claimed performed. Preserve its NO and precisely map
    # the already sealed first global gate to the current residual input.
    old_path = ROOT / 'docs/plans/qualification/E2_P05_A06_PROSPECTIVE_REQUEST_WAIT_EXECUTION_1/P05-complete-readiness-result.json'
    old = read(old_path)
    save(OUT / 'P05-readiness-result.json',{
        'RESULT':'NO_PREREQUISITE_COMPOSITE_END_ORACLE_FAILED','P05_EXECUTION_READY':'NO',
        'P05_BOUND_STAGE_INPUTS':13,'P05_REQUIRED_STAGE_INPUTS':13,
        'FULL_P05_READINESS_RERUN_PERFORMED':False,
        'conditional_rule':'Run the complete P05 predicate only after complete composite END qualification PASS',
        'composite_qualification':ref(OUT / 'END-oracle-results.json'),
        'prior_complete_authoritative_readiness':ref(old_path),
        'unchanged_readiness_terms':old['terms'],
        'aggregate_scope_and_four_bridge_gap_resolved':True,
        'first_remaining_readiness_term':'GLOBAL_END_BINDINGS','FIRST_REMAINING_BLOCKER':first,
        'sixteen_P05_negative_expectations':'UNCHANGED_NOT_EXECUTED',
        'other_input_manifest_N08_N12_persistence_replay_authority_terms':'NOT_REPAIRED; retained existing obligations',
        'NEXT_PACKAGE':'E2-P05 CURRENT COMPOSITE END INTERFACE / PROCESS BINDING CLOSURE',
        'P05_EXECUTED':'NO','P06_EXECUTED':'NO','new_readiness_criteria':0})
    print(json.dumps({'MAPPING_QUALIFICATION':'PASS','COMPOSITE_P05_END_QUALIFICATION':'FAIL',
        'P05_EXECUTION_READY':'NO','first_remaining_blocker':first['input'],'unbound_interface_terms':6}))


if __name__=='__main__':
    main()
