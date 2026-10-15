"""Reconstruct retained P05 bindings and apply the A04-only scope mapping."""
import copy
import json
import os
from pathlib import Path

import execution_driver as d
from qualification_checks import descriptor, validate_witness
from adapter.planner import codec as c

OLD=d.OUT.with_name('E2_P05_END_INPUT_BINDING_1')
A03=d.OUT.with_name('E2_P05_A03_PROSPECTIVE_OCCURRENCE_EXECUTION_1')


def pin(path,pointer=''):
    return {'path':str(path.relative_to(d.ROOT)),'raw_sha256':d.sha(path),'pointer':pointer}


def verify_pins(value,seen):
    if isinstance(value,dict):
        if 'path' in value and 'raw_sha256' in value:
            path=d.ROOT/value['path']
            d.equal('RETAINED_BINDING_SOURCE:'+value['path'],d.sha(path),value['raw_sha256'])
            seen.add((value['path'],value['raw_sha256']))
            if value.get('pointer'):
                item=d.read(path)
                for word in value['pointer'].lstrip('/').split('/'):
                    word=word.replace('~1','/').replace('~0','~')
                    item=item[int(word)] if isinstance(item,list) else item[word]
        for item in value.values():verify_pins(item,seen)
    elif isinstance(value,list):
        for item in value:verify_pins(item,seen)


def reconstruct():
    d.verify_entry()
    for name in ('process-qualification.json','A04-negative-results.json',
                 'D01-overlay-negative-results.json','idempotence.json','bundle-export.json'):
        d.equal('A04_FINAL_QUALIFICATION:'+name,d.read(d.OUT/name)['result'],'PASS')
    negatives=d.read(d.OUT/'A04-negative-results.json')
    d.equal('N12_GATE',negatives['N12_MAPPING'],'PASS');d.equal('N13_GATE',negatives['N13_MAPPING'],'PASS')
    bundle=validate_witness(descriptor());start,sid,artifacts=d.load_start()
    mapping=d.read(d.BASE/'END-replacement-mapping.json')
    prior=d.read(A03/'P05-binding-rerun.json');original=d.read(OLD/'canonical-bindings.json')
    seen=set()
    for name in ('canonical-bindings.json','input-oracle.json','input-oracle-comparison.json',
                 'dependency-DAG.json','configuration-history.json','P03-replacement-treatment.json'):
        verify_pins(d.read(OLD/name),seen)
    verify_pins(prior,seen)
    d.equal('PREVIOUS_STAGE_COUNT',prior['P05_BOUND_STAGE_INPUTS'],10)
    d.equal('PREVIOUS_FRONTIER',prior['P05_NEXT_MISSING_INPUT'],mapping['target'])
    d.equal('ORIGINAL_HISTORICAL_A03',prior['ORIGINAL_A03_HISTORICAL_OCCURRENCE'],'UNPROVEN')
    target_path=d.ROOT/original['actual_target']['path']
    target_id=c._identity(target_path.read_bytes(),'planner-bundle-v1')
    target=c.restore(target_path,target_id,d.ROOT)
    p04=d.read(d.PLANS/'DETERMINISTIC_PLANNER_V0_1_E2_P04_CANONICAL_EXECUTION_RETRY_1_RESULT.json')
    d.equal('CANONICAL_P04_PASS',p04['E2_P04_RESULT'],'PASS')
    d.equal('CANONICAL_P04_ID',d.uid(target_id),p04['FINAL_P04_BUNDLE_ID'])
    d.equal('CANONICAL_P04_STATE',d.uid(c.snapshot_id(target.current)),p04['FINAL_STATE_ID'])
    for row in original['stage_bindings']:
        if row['binding_status']=='BOUND':
            for event in row['EVENTS']:
                d.equal('PRIOR_CANONICAL_EVENT:'+row['STEP_ID'],event,c._wire(target.events[event['sequence']-1]))
    a03=next(row for row in prior['stage_bindings'] if row['stage']=='E2-A03')
    d.equal('A03_REPLACEMENT_PREFIX_EVENTS',a03['replacement_native_event_ids'],[d.uid(e.identity) for e in start.events])
    d.equal('A03_REPLACEMENT_PREFIX_BUNDLE',a03['replacement_post_bundle_id'],d.uid(c.bundle_id(start)))
    stages=copy.deepcopy(prior['stage_bindings']);event=bundle.events[2]
    index=next(i for i,row in enumerate(stages) if row['stage']=='E2-A04')
    d.equal('A04_PREVIOUSLY_UNBOUND',stages[index]['binding_status']=='BOUND',False)
    export=d.read(d.OUT/'bundle-export.json');post_path=d.ROOT/export['path']
    stages[index]={'stage':'E2-A04','logical_required_input':mapping['target'],'binding_status':'BOUND',
        'classification':'AUTHORIZED_PROSPECTIVE_REPLACEMENT','mapping_result':'PASS',
        'governing_decision':'AUTHORIZE_PROSPECTIVE_P05_A04_ANCESTRY_QUALIFICATION',
        'authorization_subject':d.read(d.DA/'versioned-overlay.json')['authorization_subject'],
        'original_historical_ancestry':'UNPROVEN','original_event_id':None,'original_parent_id':None,
        'original_ledger_position':None,'original_history_splice':False,'historical_identity_alias':False,
        'replacement_event_id':d.uid(event.identity),'replacement_parent_id':d.uid(event.parent_event),
        'replacement_pre_snapshot':d.uid(event.parent_snapshot),'replacement_post_snapshot':d.uid(event.after_snapshot),
        'replacement_bundle_id':export['bundle_id'],'replacement_ledger_anchor':d.read(d.BASE/'prospective-start.json')['LEDGER_ID'],
        'replacement_sequence':3,'replacement_index':2,'replacement_scope':bundle.current.context.scope,
        'replacement_lineage':bundle.current.context.lineage,'replacement_generation':bundle.current.context.generation,
        'native_event':pin(post_path,'/bundle/events/2'),
        'native_result':pin(post_path,'/bundle/events/2/result'),
        'native_output':pin(post_path,'/bundle/events/2/result/knowledge/0'),
        'native_transaction_binding':pin(post_path,'/bundle/dossier_materializations/0'),
        'native_original_post_snapshot':pin(d.ROOT/export['detached_archive'],'/snapshot'),
        'immutable_member_selector':'(event.after_snapshot, PredicateId, dossier identity); six complete typed members',
        'sealed_mapping':pin(d.BASE/'END-replacement-mapping.json'),
        'N12_MAPPING':'PASS','N13_MAPPING':'PASS','cold_restore':'PASS','historical_replay':'PASS',
        'qualification_negatives':'PASS','determinism':'PASS','original_record_changed':False,
        'currentness':'Actual native result/typed members current at sealed prospective A04 boundary; qualification occurrence is not downstream permission.'}
    for i,row in enumerate(stages):
        if i!=index:d.equal('UNAFFECTED_STAGE_BINDING:'+row['stage'],row,prior['stage_bindings'][i])
    count=sum(row['binding_status']=='BOUND' for row in stages)
    d.equal('A04_ONLY_BINDING_EFFECT',count,mapping['maximum_stage_count_after_A04_only'])
    gaps=[x for x in prior['remaining_stage_gaps'] if x!=mapping['target']]
    missing=[row['stage'] for row in stages if row['binding_status']!='BOUND']
    d.equal('BOUND_STAGE_UNIVERSE',[row['stage'] for row in stages],['E2-A%02d'%i for i in range(1,14)])
    d.equal('GAP_STAGE_UNIVERSE',[x.split('.')[0] for x in gaps],missing)
    # Stop at the existing first unresolved dependency. No new recovery or execution.
    first=gaps[0] if gaps else None
    return {**d.LABELS,'result':'PASS_FOR_A04_MAPPING; FULL_GRAPH_INCOMPLETE',
        'schema':'E2-P05-A04-AUTHORIZED-PROSPECTIVE-BINDING-RESULT-1',
        'E2_A04_PREPARE_RESULT_EVENT_ANCESTRY':'PASS','END_MAPPING':'PASS','N12_MAPPING':'PASS','N13_MAPPING':'PASS',
        'stage_bindings':stages,'P05_PREVIOUS_BOUND_STAGE_INPUTS':10,'P05_BOUND_STAGE_INPUTS':count,
        'P05_TOTAL_STAGE_INPUTS':13,'P05_NEXT_MISSING_INPUT':first,'remaining_stage_gaps':gaps,
        'additional_unresolved_END_gate':prior['additional_unresolved_END_gate'],
        'original_full_END_ancestry_waived':False,'original_ancestry_edges_changed':False,
        'prior_source_hash_pins_rechecked':len(seen),'P04_target_replay_restore':'PASS',
        'P04_target_bundle_id':d.uid(target_id),'P04_target_event_count':len(target.events),'canonical_P04_unchanged':True,
        'P05_INITIAL_ORACLE':'PASS; retained P04 target exact and prior sealed entry/oracle pins unchanged',
        'E2_END_INPUT_GRAPH':'FAIL_COMPLETENESS','P05_EXECUTION_READY':'NO','E2_P05_READY':'YES',
        'P05_EXECUTED':'NO','P06_EXECUTED':'NO','next_missing_input_resolved':False,
        'P03_scope_decision_reopened':False,'P03_HISTORICAL_CORRESPONDENCE':'UNPROVEN','N_REAL_SATISFIED':'NO',
        'binding_representation':mapping['representation'],'new_native_objects_or_authority_from_binding':0,
        'NEXT_PACKAGE':'E2-P05-A05-RECORDED-DECISION-EVENT-ANCESTRY-RECOVERY'}


if __name__=='__main__':
    try:
        graph=reconstruct();path=d.OUT/'graph-readers'/('seed-'+os.environ['PYTHONHASHSEED']+'.json')
        d.write(path,graph)
        print(json.dumps({'A04_mapping':'PASS','bound':graph['P05_BOUND_STAGE_INPUTS'],'next':graph['P05_NEXT_MISSING_INPUT']}))
    except Exception as exc:
        d.write(d.OUT/'binding-divergence.json',{**d.LABELS,'result':'FAIL',
            'FIRST_COUNTEREXAMPLE':getattr(exc,'name',type(exc).__name__),
            'EXPECTED':repr(getattr(exc,'expected',None)),'ACTUAL':repr(getattr(exc,'actual',str(exc))),
            'CLASSIFICATION':'BINDING_ORACLE_DIVERGENCE','no_live_repair':True})
        raise
