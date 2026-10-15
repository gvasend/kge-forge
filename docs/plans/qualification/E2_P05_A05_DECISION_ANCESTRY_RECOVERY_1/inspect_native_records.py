"""Read retained records and compare identities without replaying a decision."""
import hashlib
import json
from pathlib import Path

from adapter.planner import codec as c, core, human_decision as hd, model as m

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
PLANS=ROOT/'docs/plans'
PREFIX='DETERMINISTIC_PLANNER_V0_1_'
BARRED=[]


def deny(name):
    def rejected(*args,**kwargs):
        BARRED.append(name)
        raise RuntimeError('Recovery cannot invoke '+name)
    return rejected


for owner,names in (
    (hd,('capture_choice','materialize_choice','apply_explicit_choice')),
    (core,('apply_result','admit_dossier_materialization','apply_recorded_decision',
           'apply_decision_reentry','apply_event','apply_receipt')),
    (c,('_replay','append_event','record_result','bundle_bytes','bundle_id',
        'save_bundle','restore','commit_event','_publish_head','_read_head')),
):
    for name in names:setattr(owner,name,deny(owner.__name__+'.'+name))


def ident(x):return None if x is None else x.namespace+':'+x.sha256
def wire(x):return c._wire(x)
def pin(path,pointer=''):
    p=Path(path)
    return {'path':str(p.relative_to(ROOT)),'pointer':pointer,
            'raw_sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def write(name,obj):
    (OUT/name).write_text(json.dumps(obj,sort_keys=True,indent=2)+'\n')
def native(path,field):
    raw=path.read_bytes();obj=c._unwire(json.loads(raw)[field]);return obj
def dossier_identity(d):
    return ident(c._identity(c.canonical_bytes(wire(d)),'planner-dossier-sha256'))
def state_view(path):
    s=native(path,'snapshot');m.validate_model(s)
    d=next(x for x in s.decisions if x.action.value=='E2-DECIDE')
    record=next((x for x in s.entities if x.id==d.record),None)
    grant=next((x for x in s.entities if x.id.value=='E2-GRANT'),None)
    choice=next((x for x in s.knowledge if x.id.value=='decision-choice:E2-DECIDE'),None)
    result={'source':pin(path,'/snapshot'),'snapshot_id':ident(c.snapshot_id(s)),
        'model_admission':'PASS','context':wire(s.context),'decision':wire(d),
        'action_definition':wire(next(a for a in s.actions if a.id==d.action)),
        'action_status':wire(next(a for a in s.statuses if a.id==d.action)),
        'dossier_identity':dossier_identity(d.dossier),'record':wire(record),
        'grant':wire(grant),'choice_knowledge':wire(choice),
        'authority_predicates':[wire(p) for p in s.predicates if p.entity is not None and
                                p.entity in tuple(x.id for x in (record,grant) if x is not None)],
        'enclosing_ExecutionEvent':'NOT_PRESENT_IN_SNAPSHOT_SCHEMA',
        'ledger_membership':'NOT_PRESENT_IN_SNAPSHOT_SCHEMA'}
    if record:
        payload=json.loads(record.provenance.excerpt)
        digest=hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
        result.update({'choice_payload':payload,'choice_payload_digest':digest,
            'choice_content_identity_matches':digest==record.provenance.identity.sha256,
            'choice_knowledge_provenance_matches':choice.provenance==record.provenance,
            'choice_subject_matches':payload['subject']==d.action.value,
            'choice_dossier_matches':payload['dossier']==dossier_identity(d.dossier).split(':')[1]})
        gp=json.loads(grant.provenance.excerpt)
        gd=hashlib.sha256(json.dumps(gp,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
        result.update({'grant_payload':gp,'grant_content_identity_matches':gd==grant.provenance.identity.sha256==grant.identity.sha256,
            'grant_choice_binding_matches':gp['choice']==digest,
            'grant_dossier_binding_matches':gp['dossier']==payload['dossier'],
            'grant_USE_permission_matches':grant.permissions==(m.AuthorityClass.USE,)})
        for k,v in result.items():
            if k.endswith('_matches'):assert v,k
    return result


def bundle_view(path):
    b=native(path,'bundle');m.validate_types(b,m.PersistenceBundle)
    m.validate_model(b.initial);m.validate_model(b.current)
    c._verify_sources(b,ROOT)
    rows=[]
    for i,e in enumerate(b.events):
        current=ident(e.identity)
        expected=ident(c._event_identity(e.sequence,e.parent_snapshot,e.parent_event,
                                        e.result,e.after_snapshot,e.resume_binding))
        assertions={'event_comparison_identity_exact':current==expected,
            'sequence_matches_position':e.sequence==i+1,
            'parent_event_exact':e.parent_event==(b.events[i-1].identity if i else None),
            'pre_state_exact':e.parent_snapshot==(b.events[i-1].after_snapshot if i else c.snapshot_id(b.initial)),
            'RecordedDecision_pre_state_exact':type(e.result) is not m.RecordedDecision or e.result.expected_snapshot==e.parent_snapshot}
        assert all(assertions.values()),(path,i,assertions)
        rows.append({'index':i,'sequence':e.sequence,'identity':current,'result_type':type(e.result).__name__,
            'parent':ident(e.parent_event),'pre_state':ident(e.parent_snapshot),
            'post_state':ident(e.after_snapshot),'checks':assertions})
    assert b.events[-1].after_snapshot==c.snapshot_id(b.current)
    bid=ident(c._identity(c._bundle_bytes_admitted(b),'planner-bundle-v1'))
    result={'source':pin(path,'/bundle'),'bundle_comparison_identity':bid,
        'fresh_replay_or_trust_claim':'NOT_PERFORMED_RECOVERY_READ_ONLY',
        'source_pins_verified':'PASS','source_pin_count':len(b.sources),'policy_pin':wire(b.policy),
        'ledger_id':'NOT_EXPOSED_BY_NATIVE_PERSISTENCEBUNDLE',
        'ledger_membership_domain':bid+'#/bundle/events','event_count':len(b.events),
        'root':ident(b.events[0].identity),'head':ident(b.events[-1].identity),
        'initial_state':ident(c.snapshot_id(b.initial)),'current_state':ident(c.snapshot_id(b.current)),
        'context':wire(b.current.context),'events':rows,
        'initial_decision':[wire(d) for d in b.initial.decisions if d.action.value=='E2-DECIDE'],
        'current_decision':[wire(d) for d in b.current.decisions if d.action.value=='E2-DECIDE']}
    matching=[(i,e) for i,e in enumerate(b.events) if type(e.result) is m.RecordedDecision and e.result.decision.value=='E2-DECIDE']
    result['decision_events']=[]
    for i,e in matching:
        record=next(x for x in b.initial.entities if x.id==e.result.record)
        choice=next(x for x in b.initial.knowledge if x.id.value=='decision-choice:E2-DECIDE')
        authority=next(x for x in b.initial.predicates if x.id==e.result.authority)
        grant=next(x for x in b.initial.entities if x.id.value=='E2-GRANT')
        physical_choice=next(x for x in b.sources if x.path==record.provenance.path)
        c.load_pinned(ROOT,physical_choice)
        choice_value=json.loads((ROOT/physical_choice.path).read_bytes())
        grant_pin=next(x for x in b.sources if x.path==grant.provenance.path)
        c.load_pinned(ROOT,grant_pin)
        grant_value=json.loads((ROOT/grant_pin.path).read_bytes())
        relations={'record_to_exact_subject':record.decision==e.result.decision,
            'record_to_exact_choice':record.choice==e.result.choice==choice.statement==choice_value['option'],
            'native_DECIDE_authority_binding':authority.entity==record.id and authority.permission is m.AuthorityClass.DECIDE,
            'choice_evidence_provenance_binding':record.provenance==choice.provenance,
            'native_choice_source_identity':record.provenance.identity==physical_choice.identity,
            'native_grant_source_identity':grant.provenance.identity==grant_pin.identity,
            'grant_choice_binding':grant_value['choice']['sha256']==physical_choice.identity.sha256,
            'grant_dossier_binding':grant_value['dossier']['sha256']==choice_value['dossier']['sha256'],
            'grant_already_present_in_pre_state':True}
        assert all(relations.values()),relations
        result['decision_events'].append({'source':pin(path,'/bundle/events/'+str(i)),'event':wire(e),
            'record':wire(record),'choice':wire(choice),'authority_predicate':wire(authority),
            'choice_source_pin':wire(physical_choice),'choice_source_payload':choice_value,
            'grant':wire(grant),'grant_source_pin':wire(grant_pin),'grant_source_payload':grant_value,
            'checks':relations,'pre_state_authored_grant_is_not_event_grant_issuance':True,
            'successor':rows[i+1] if i+1<len(rows) else None,
            'post_state_for_this_event':ident(e.after_snapshot)})
    return result


def main():
    handoff=state_view(PLANS/(PREFIX+'E2_AUTHORITATIVE_HANDOFF_SNAPSHOT_1.json'))
    post=state_view(PLANS/(PREFIX+'E2_HUMAN_DECISION_ALLOW_POST_SNAPSHOT_1.json'))
    checkpoint=bundle_view(PLANS/(PREFIX+'P03_PROSPECTIVE_CHECKPOINT_BUNDLE_1.json'))
    target=bundle_view(PLANS/(PREFIX+'E2_P04_CANONICAL_TARGET_BUNDLE_1.json'))
    prospective=bundle_view(PLANS/(PREFIX+'E2_P05_A04_PROSPECTIVE_ANCESTRY_BUNDLE_1.json'))
    assert target['events'][:2]==checkpoint['events']
    assert len(checkpoint['decision_events'])==len(target['decision_events'])==1
    assert not prospective['decision_events']
    assert handoff['decision']['stage']['value']=='DECISION_READY'
    assert post['decision']['stage']['value']=='DECISION_RECORDED'
    retained=native(PLANS/(PREFIX+'P03_PROSPECTIVE_CHECKPOINT_BUNDLE_1.json'),'bundle')
    unchanged={field:getattr(retained.initial,field)==getattr(retained.current,field)
               for field in ('roots','slots','entities','knowledge','predicates','actions')}
    assert all(unchanged.values())
    original_event_candidates=json.loads((OUT/'event-search.json').read_text())['matching_A05_events']
    assert all(x['event']['result']['record']['value']!=post['record']['id']['value'] for x in original_event_candidates)
    comparison={'semantic_subject_same':True,
        'original_record_id':post['record']['id']['value'],
        'prospective_record_id':checkpoint['decision_events'][0]['event']['result']['record']['value'],
        'original_choice_content_identity':'raw-file-sha256:'+post['choice_payload_digest'],
        'prospective_choice_content_identity':ident(c._unwire(checkpoint['decision_events'][0]['choice_source_pin']['identity'])),
        'original_dossier':post['dossier_identity'],
        'P03_dossier':dossier_identity(native(PLANS/(PREFIX+'P03_PROSPECTIVE_CHECKPOINT_BUNDLE_1.json'),'bundle').initial.decisions[0].dossier),
        'A04_prospective_dossier':dossier_identity(native(PLANS/(PREFIX+'E2_P05_A04_PROSPECTIVE_ANCESTRY_BUNDLE_1.json'),'bundle').current.decisions[0].dossier),
        'original_choice_context':post['context'],'P03_choice_context':checkpoint['context'],
        'A04_context':prospective['context'],
        'original_handoff_state':handoff['snapshot_id'],
        'original_post_decision_state':post['snapshot_id'],
        'P03_event_pre_state':checkpoint['decision_events'][0]['event']['parent_snapshot'],
        'P03_event_post_state':checkpoint['decision_events'][0]['post_state_for_this_event'],
        'A04_current_state':prospective['current_state'],
        'original_event_identity_recovered':None,
        'P03_event_can_be_original_A05_event':False,
        'old_choice_reusable_as_fresh_choice_against_A04':False,
        'reason':'Native subject/dossier/snapshot and provenance context must be exact; same semantic option cannot rebind immutable choice evidence.'}
    write('native-state-and-ledger-inspection.json',{'original_handoff':handoff,'original_post_decision':post,
        'P03_prospective_checkpoint':checkpoint,'P04_canonical_descendant':target,'A04_prospective_frontier':prospective,
        'P03_recorded_decision_unchanged_state_domains':unchanged,
        'identity_domain_comparison':comparison,'inspection':'PURE_DECODE_TYPE_MODEL_IDENTITY_PIN_AND_ENROLLED_HISTORY_COMPARISON',
        'barred_calls':BARRED,'decision_capture_calls':0,'decision_application_calls':0,'replay_calls':0,'events_created':0})
    print(json.dumps({'result':'PASS_READ_ONLY_INSPECTION','original_snapshot':post['snapshot_id'],
        'qualified_decision_event':target['decision_events'][0]['event']['identity'],
        'event_identity_verified':True,'parent_ledger_verified':True,'new_A05_calls':len(BARRED)}))


if __name__=='__main__':main()
