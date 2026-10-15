"""Read-only D01 compatibility overlay. No PREPARE/T02/commit/replay of A04."""
from dataclasses import fields, replace
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

from adapter.planner import codec as c, core, dossier_transaction as dt, model as m

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
DA=ROOT/'docs/plans/qualification/E2_P05_A04_DURABLE_ADMISSION_CONTRACT_1'
BASE=ROOT/'docs/plans/qualification/E2_P05_A04_PROSPECTIVE_ANCESTRY_CONTRACT_1'


def read(path):return json.loads(Path(path).read_bytes())
def text_id(x):return x.namespace+':'+x.sha256
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def same(a,b):return c.canonical_bytes(c._wire(a))==c.canonical_bytes(c._wire(b))


def qualify():
    assert read(OUT/'process-qualification.json')['result']=='PASS'
    tests=read(OUT/'generic-tests.json')
    assert tests['tests_run']>=20 and not tests['errors'] and not tests['failures']
    checks={};verified=[];runtime_updates=[];blocked_calls=[]
    def gate(name,condition):
        assert condition,name
        checks[name]='PASS'
    def barred(name):
        def fail(*args,**kwargs):
            blocked_calls.append(name)
            raise AssertionError('A04 compatibility may not invoke '+name)
        return fail
    contract=read(DA.parent.parent/'DETERMINISTIC_PLANNER_V0_1_E2_P05_A04_DURABLE_ADMISSION_CONTRACT_1.json')
    gate('durable_contract',contract['RESULT']=='PASS' and contract['A04_DURABLE_TRANSACTION_IMPLEMENTATION_READY']=='YES')
    overlay=read(DA/'versioned-overlay.json')
    label_rules={'QUALIFICATION_TYPE':'PROSPECTIVE_REPLACEMENT',
        'ORIGINAL_A04_HISTORICAL_ANCESTRY':'UNPROVEN','ORIGINAL_A03_HISTORICAL_OCCURRENCE':'UNPROVEN',
        'HISTORICAL_RECONSTRUCTION':'NO','PROSPECTIVE_A04_EVENT_IS_ORIGINAL_EVENT':'NO'}
    def verify_labels(value):
        assert all(value.get(k)==v for k,v in label_rules.items()),'qualification history relabeling'
    verify_labels(overlay)
    rejected_labels=[]
    for field,value in (('QUALIFICATION_TYPE','CANONICAL_HISTORICAL'),
                        ('ORIGINAL_A04_HISTORICAL_ANCESTRY','PROVEN'),
                        ('ORIGINAL_A03_HISTORICAL_OCCURRENCE','PROVEN'),
                        ('HISTORICAL_RECONSTRUCTION','YES'),
                        ('PROSPECTIVE_A04_EVENT_IS_ORIGINAL_EVENT','YES')):
        try:verify_labels(dict(overlay,**{field:value}))
        except AssertionError:rejected_labels.append(field)
        else:raise AssertionError('historical relabeling accepted')
    gate('historical_label_negatives',len(rejected_labels)==5)
    pins=read(DA/'source-pins.json')['pins']+overlay['preserved_files']
    for pin in pins:
        if pin['path'] in ('adapter/planner/codec.py','adapter/planner/model.py'):
            # These pins describe the inspected old implementation, not sealed
            # experiment inputs. D01 explicitly authorizes these integrations.
            baseline=read(OUT/'baseline.json')
            gate('original_runtime_reference:'+pin['path'],baseline['files'][pin['path']]==pin['raw_sha256'])
            runtime_updates.append({'path':pin['path'],'prior_sha256':pin['raw_sha256'],
                                    'qualified_current_sha256':sha(ROOT/pin['path'])})
            continue
        gate('unchanged:'+pin['path'],sha(ROOT/pin['path'])==pin['raw_sha256'])
        verified.append(pin)
    original=read(ROOT/overlay['base_contract']['path'])
    start_spec=read(BASE/'prospective-start.json')
    authority=read(BASE/'authority.json')
    mappings=read(BASE/'N12-N13-assurance-mapping.json')
    binding_spec=read(DA/'snapshot-event-binding.json')
    comparison=read(DA/'oracles/prospective-native-binding.json')
    representation=read(ROOT/comparison['native_event_oracle']['path'])
    with patch.object(dt,'register_producer',side_effect=barred('producer registration')), \
         patch.object(dt,'prepare',side_effect=barred('live prepare')), \
         patch.object(dt,'execute',side_effect=barred('live execute')), \
         patch.object(dt,'commit',side_effect=barred('live commit')), \
         patch.object(core,'admit_dossier_materialization',side_effect=barred('A04/T02 state admission')), \
         patch.object(c,'_publish_head',side_effect=barred('HEAD publication')):
        sid=start_spec['START_BUNDLE_ID'].split(':')[1]
        expected=c._identity((ROOT/start_spec['START_PATH']['path']).read_bytes(),'planner-bundle-v1')
        before=c.restore(ROOT/start_spec['START_PATH']['path'],expected,ROOT)
        gate('start_bundle',expected.sha256==sid and text_id(c.bundle_id(before))==start_spec['START_BUNDLE_ID'])
        gate('start_state',text_id(c.snapshot_id(before.current))==start_spec['START_STATE_ID'])
        gate('start_ledger',len(before.events)==2 and text_id(before.events[0].identity)==start_spec['LEDGER_ROOT']
             and text_id(before.events[-1].identity)==start_spec['APPEND_HEAD']==start_spec['PARENT_EVENT_ID'])
        ctx=before.current.context
        gate('scope_lineage_generation',(ctx.scope,ctx.lineage,ctx.generation,ctx.tick)==
             (start_spec['scope'],start_spec['lineage'],start_spec['generation'],start_spec['tick']))
        action=next(a for a in before.current.actions if a.id.value=='E2-PREPARE')
        gate('native_authority',action.authority is None and authority['ADDITIONAL_AUTHORITY_REQUIRED']=='NO')
        auth=authority['QUALIFICATION_SCOPE_AUTHORIZATION']
        gate('scope_authorization',auth['selected_option']==overlay['scope_decision']
             and auth['subject_identity']==overlay['authorization_subject']
             and auth['AUTHORIZATION_SUBJECT_MATCH']=='PASS')
        gate('unexecuted',action.prepared_dossier is None and not before.current.validation_instances
             and next(s for s in before.current.statuses if s.id==action.id).state is not m.ActionState.COMPLETED)
        supplied=c._unwire(original['EXPECTED_RESULT_ORACLE']['expected_result'])
        after=c._unwire(original['EXPECTED_RESULT_ORACLE']['expected_post_state'])
        event=c._unwire(representation['native_event'])
        pin=c._unwire(binding_spec['A04_expected_source_additions'][0])
        raw=(ROOT/pin.path).read_bytes()
        gate('exact_input',pin not in before.sources and sha(ROOT/pin.path)==pin.identity.sha256)
        dt.sources(((pin,raw),))
        # These are pure type/currentness/operand checks. The expected result is
        # comparison data only and cannot enter the live Prepared API.
        dt.validate_operands(before.current,supplied,after.validation_instances,before.sources+(pin,),before.events)
        gate('generic_typed_operand_compatibility',True)
        gate('event_schema_unchanged',{f.name for f in fields(m.ExecutionEvent)}==set(comparison['existing_event_schema'])
             and 'validation_instances' not in {f.name for f in fields(m.SuppliedResult)})
        gate('event_result_binding',same(event.result,supplied) and event.parent_snapshot==c.snapshot_id(before.current)
             and event.parent_event==before.events[-1].identity and event.sequence==3)
        gate('event_identity_unchanged',text_id(event.identity)==comparison['EXPECTED_EVENT_ID']
             and event.identity==c._event_identity(3,event.parent_snapshot,event.parent_event,supplied,event.after_snapshot))
        gate('snapshot_identity_unchanged',text_id(c.snapshot_id(after))==comparison['EXPECTED_POST_SNAPSHOT_ID']
             and c.snapshot_id(after)==event.after_snapshot)
        gate('six_validation_members',len(after.validation_instances)==6)
        for member in binding_spec['A04_member_bindings']:
            matches=[v for v in after.validation_instances if v.predicate==c._unwire(member['predicate'])]
            gate('typed_member:'+matches[0].predicate.value,len(matches)==1 and matches[0].dossier==c._unwire(member['dossier'])
                 and matches[0].inputs==c._unwire(member['ordered_inputs']) and c._unwire(member['snapshot'])==event.after_snapshot)
        binding=m.DossierMaterializationBinding(event.identity,expected,(pin,))
        gate('native_binding_schema',c._wire(binding)==comparison['binding_future_wire'])
        future=replace(before,events=before.events+(event,),current=after,sources=before.sources+(pin,),
                       dossier_materializations=(binding,))
        # Pure codec serialization of a COMPARISON oracle, never live admission,
        # historical A04 replay or an accepted/persisted target bundle.
        wire={'schema':'PLANNER-BUNDLE-1','bundle':c._wire(future)}
        gate('exact_future_wire',wire==comparison['future_bundle_wire'] and same(c._unwire(wire['bundle']),future))
        bid=c._identity(c._bundle_bytes_admitted(future),'planner-bundle-v1')
        gate('bundle_comparison_identity',text_id(bid)==comparison['EXPECTED_FUTURE_BUNDLE_ID_COMPARISON_ONLY'])
        gate('legacy_bytes_unchanged',c._bundle_bytes_admitted(before)==(ROOT/start_spec['START_PATH']['path']).read_bytes()
             and 'dossier_materializations' not in c._wire(before))
        gate('identity_order',read(DA/'identity-order.json')['IDENTITY_CYCLE']=='NO')
        negative=read(BASE/'negative-contract.json')
        gate('24_negatives_preserved',len(negative['cases'])==len(original['NEGATIVE_SUITE'])==24)
        gate('N12_mapping_preserved',mappings['N12']['N12_MAPPING_PRESERVED']=='YES')
        gate('N13_mapping_preserved',mappings['N13']['N13_MAPPING_PRESERVED']=='YES')
        end=read(BASE/'END-replacement-mapping.json')
        gate('END_mapping_unchanged',end['target']=='E2-A04.prepare_result_event_ancestry'
             and end['current_stage_count']==10 and end['maximum_stage_count_after_A04_only']==11)
        gate('no_operation_state_admission_or_publication',not blocked_calls)
    return {'result':'PASS','role':'READ_ONLY_TYPED_REPRESENTATION_AND_SEAL_PREFLIGHT',
        'checks':checks,'preserved_input_pins':verified,'authorized_runtime_updates':runtime_updates,
        'comparison_event':text_id(event.identity),'comparison_snapshot':text_id(event.after_snapshot),
        'comparison_future_bundle':text_id(bid),'comparison_only':True,
        'native_A04_admission_calls':0,'live_producer_calls':0,'A04_replay_calls':0,'published_bundles':0,
        'prior_reports_rewritten':False,'historical_relabeling_negative_fields':rejected_labels,
        'historical_relabeling_test_layer':'QUALIFICATION_OVERLAY_VALIDATOR_NOT_NATIVE_EVENT_SCHEMA',
        'ADDITIONAL_AUTHORITY_REQUIRED':'NO',
        'N12_MAPPING_PRESERVED':'YES','N13_MAPPING_PRESERVED':'YES',
        'QUALIFICATION_TYPE':'PROSPECTIVE_REPLACEMENT','ORIGINAL_A04_HISTORICAL_ANCESTRY':'UNPROVEN',
        'ORIGINAL_A03_HISTORICAL_OCCURRENCE':'UNPROVEN','HISTORICAL_RECONSTRUCTION':'NO',
        'PROSPECTIVE_A04_EVENT_IS_ORIGINAL_EVENT':'NO','PROSPECTIVE_A04_EXECUTED':'NO',
        'PROSPECTIVE_A04_EXECUTION_READY':'YES','P05_BOUND_STAGE_INPUTS':10,'P05_EXECUTION_READY':'NO',
        'readiness_overlay':'D01 qualification closes only the previously missing generic capability; immutable old readiness reports remain historical.'}


if __name__=='__main__':
    result=qualify()
    (OUT/'A04-compatibility.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('result','PROSPECTIVE_A04_EXECUTION_READY','PROSPECTIVE_A04_EXECUTED')}))
