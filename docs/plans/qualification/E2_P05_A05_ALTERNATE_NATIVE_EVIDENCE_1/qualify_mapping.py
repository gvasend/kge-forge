"""Pure retained-record acceptance queries. Native capture/apply/replay are barred."""
import copy
from dataclasses import fields
import hashlib
import json
import os
from pathlib import Path
import sys

from adapter.planner import codec as c, core, gates, human_decision as hd, model as m

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
BARRED=[]


class MappingRejected(Exception):
    pass


def check(condition,code):
    if not condition:raise MappingRejected(code)


def deny(name):
    def fail(*args,**kwargs):
        BARRED.append(name)
        raise RuntimeError('No native operation permitted: '+name)
    return fail


for module,names in (
    (hd,('capture_choice','materialize_choice','apply_explicit_choice')),
    (core,('apply_result','admit_dossier_materialization','apply_recorded_decision','apply_decision_reentry','apply_event','apply_receipt')),
    (c,('_replay','_prefix_bundle','append_event','record_result','save_bundle','restore','commit_event',
        '_publish_head','_read_head','apply_event','bundle_id','bundle_bytes','admit_external_evidence','_extend_private')),
):
    for name in names:setattr(module,name,deny(module.__name__+'.'+name))


def canonical(obj):return json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def ident(obj):return obj.namespace+':'+obj.sha256
def digest(obj):return hashlib.sha256(canonical(obj)).hexdigest()
def load_pin(pin):
    raw=(ROOT/pin['path']).read_bytes()
    check(hashlib.sha256(raw).hexdigest()==pin['raw_sha256'],'PIN_CHANGED:'+pin['path'])
    return json.loads(raw)
def wire_equal(a,b):return c.canonical_bytes(c._wire(a))==c.canonical_bytes(c._wire(b))
def artifact_pointer(path,pointer,raw_sha):return {'path':path,'pointer':pointer,'raw_sha256':raw_sha}


def presented(obj,mode):
    """Vary only codec-declared sets and JSON key presentation in memory."""
    if isinstance(obj,list):return [presented(x,mode) for x in obj]
    if not isinstance(obj,dict):return obj
    result={key:presented(obj[key],mode) for key in (reversed(list(obj)) if mode!='native' else obj)}
    cls=c.TYPES.get(obj.get('$type'))
    for name in c.SET_FIELDS.get(cls,set()):
        items=result.get(name)
        if isinstance(items,list) and len(items)>1:
            if mode=='reverse_unordered':result[name]=list(reversed(items))
            elif mode=='rotate_unordered':result[name]=items[1:]+items[:1]
    return result


def authenticate(contract):
    seal=json.loads((OUT/'seal.json').read_bytes())
    for pin in seal['pins']:load_pin(pin)
    dossier=load_pin(contract['dossier_pin'])
    check('qualification-scope-subject-v1:'+digest(dossier['subject'])==contract['subject_identity']==dossier['subject_identity'],'SCOPE_SUBJECT_CHANGED')
    auth=load_pin(contract['scope_authentication_pin'])
    check(auth['selected_option']==contract['selected_option']=='AUTHORIZE_P05_A05_ALTERNATE_NATIVE_EVIDENCE','SCOPE_OPTION_CHANGED')
    check(auth['qualification_scope_subject']==contract['subject_identity'],'SCOPE_AUTH_SUBJECT_CHANGED')
    check(auth['dossier']['raw_sha256']==contract['dossier_raw_sha256'],'SCOPE_DOSSIER_CHANGED')
    check(auth['scope_type']=='QUALIFICATION_ACCEPTANCE_ONLY','SCOPE_IS_NOT_NATIVE_AUTHORITY')
    check(all(auth[k] is False for k in ('native_Action_authority','DECIDE_authority','USE_authority',
                                        'event_authority','new_grant_issuance','P05_execution_authority','new_native_choice_evidence')),'SCOPE_EXCEEDED')
    recovery=load_pin(auth['recovery_JSON']);load_pin_bytes(auth['recovery_MD'])
    check(recovery['SCOPE_DECISION_SUBJECT_ID']==contract['subject_identity'] and recovery['SCOPE_OPTIONS']==dossier['options'],'RECOVERY_DOSSIER_CHANGED')
    check(auth['authorized_option_terms']==contract['selected_option_terms']==next(x for x in dossier['options'] if x['option']==auth['selected_option']),'OPTION_TERMS_CHANGED')
    for pin in contract['governing_source_pins']:load_pin_bytes(pin)
    for pin in contract['authoritative_sources'].values():load_pin_bytes(pin)
    return auth,dossier


def load_pin_bytes(pin):
    raw=(ROOT/pin['path']).read_bytes()
    check(hashlib.sha256(raw).hexdigest()==pin['raw_sha256'],'PIN_CHANGED:'+pin['path'])
    return raw


def validate_proposal(proposal,contract):
    expected=contract['expected_proposal']
    checks=[
        ('witness_kind','NATIVE_EVENT_REQUIRED'),('event_id','EVENT_ID_EXACT'),
        ('event_source','EVENT_SOURCE_EXACT'),('choice_identity','CHOICE_IDENTITY_EXACT'),
        ('context','DECISION_CONTEXT_EXACT'),('parent_event_id','PARENT_EVENT_EXACT'),
        ('ledger_bundle_id','LEDGER_MEMBERSHIP_EXACT'),('ledger_position','LEDGER_POSITION_EXACT'),
        ('choice_source_pin','CHOICE_PROVENANCE_EXACT'),('scope_subject','SCOPE_SUBJECT_EXACT'),
        ('dossier_raw_sha256','DOSSIER_HASH_EXACT'),('scope_type','QUALIFICATION_SCOPE_ONLY'),
        ('P03_EVENT_IS_ORIGINAL_A05_EVENT','NO_HISTORICAL_ALIAS'),
        ('original_A05_event_id','NO_HISTORICAL_ALIAS'),('original_A05_parent_id','NO_HISTORICAL_ALIAS'),
        ('new_A05_event_id','NO_NEW_A05_IDENTITY'),('new_A05_choice_id','NO_NEW_A05_IDENTITY'),
        ('grant_preexisting','PREEXISTING_GRANT_LIMITATION'),('grant_issuance_proven','PREEXISTING_GRANT_LIMITATION'),
        ('original_prefix_gap_closed','ORIGINAL_PREFIX_STILL_OPEN'),
        ('full_END_original_ancestry_waived','ORIGINAL_PREFIX_STILL_OPEN'),('A06_gap_closed','A06_STILL_OPEN'),
        ('N12_mode','N12_INDEPENDENT_MAPPING_REQUIRED'),('N12_required_terms','N12_INDEPENDENT_MAPPING_REQUIRED'),
        ('N13_mode','N13_INDEPENDENT_MAPPING_REQUIRED'),('N13_required_terms','N13_INDEPENDENT_MAPPING_REQUIRED')]
    for key,code in checks:check(proposal.get(key)==expected[key],code)
    check(set(proposal)==set(expected),'MAPPING_SCHEMA_EXACT')
    check(proposal==expected,'MAPPING_TERM_EXACT')


def bundle_facts(pin,expected_identity,mode):
    raw=load_pin(pin);b=c._unwire(presented(raw['bundle'],mode))
    m.validate_types(b,m.PersistenceBundle);m.validate_model(b.initial);m.validate_model(b.current)
    check(ident(c._identity(c._bundle_bytes_admitted(b),'planner-bundle-v1'))==expected_identity,'BUNDLE_IDENTITY_EXACT')
    c._verify_sources(b,ROOT)
    rows=[]
    for i,event in enumerate(b.events):
        parent=b.events[i-1].identity if i else None
        pre=b.events[i-1].after_snapshot if i else c.snapshot_id(b.initial)
        body={'sequence':event.sequence,'parent':c._wire(event.parent_snapshot),
              'parent_event':c._wire(event.parent_event),'result':c._wire(event.result),'after':c._wire(event.after_snapshot)}
        if event.resume_binding is not None:body['resume_binding']=c._wire(event.resume_binding)
        independent=m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY,'planner-event-v1',hashlib.sha256(c.canonical_bytes(body)).hexdigest())
        check(event.identity==independent==c._event_identity(event.sequence,event.parent_snapshot,event.parent_event,event.result,event.after_snapshot,event.resume_binding),'NATIVE_EVENT_IDENTITY')
        check(event.sequence==i+1 and event.parent_event==parent and event.parent_snapshot==pre,'NATIVE_PARENT_POSITION')
        rows.append({'index':i,'sequence':event.sequence,'id':ident(event.identity),
            'parent':ident(parent) if parent else None,'pre':ident(pre),'post':ident(event.after_snapshot),
            'result_type':type(event.result).__name__})
    check(b.events[-1].after_snapshot==c.snapshot_id(b.current),'NATIVE_FINAL_SNAPSHOT')
    return b,raw,rows


def qualify(proposal,contract,mode='native'):
    validate_proposal(proposal,contract)
    auth,dossier=authenticate(contract)
    w=dossier['subject']['alternate_native_witness'];sources=contract['authoritative_sources']
    cp,raw_cp,cp_rows=bundle_facts(sources['checkpoint'],w['checkpoint_bundle'],mode)
    target,raw_target,target_rows=bundle_facts(sources['canonical_descendant'],w['canonical_descendant_bundle'],mode)
    check(len(cp.events)==2 and len(target.events)==20,'EXACT_RETAINED_HISTORY_SIZE')
    check(all(wire_equal(x,y) for x,y in zip(cp.events,target.events[:2])),'CANONICAL_DESCENDANT_PREFIX')
    event=cp.events[1];command=event.result
    check(type(command) is m.RecordedDecision,'TYPED_RECORDED_DECISION_REQUIRED')
    check(c.canonical_bytes(c._wire(event))==c.canonical_bytes(contract['expected_event']),'SEALED_NATIVE_PAYLOAD')
    standalone=load_pin(sources['immutable_event'])
    check(c.canonical_bytes(standalone)==c.canonical_bytes(c._wire(event)),'IMMUTABLE_LEDGER_EVENT_BYTES')
    check(ident(event.identity)==proposal['event_id'],'EXACT_NAMED_NATIVE_EVENT')
    check(ident(event.parent_snapshot)==ident(c.snapshot_id(cp.initial))==proposal['pre_state_id'],'EXACT_NATIVE_PRE_STATE')
    check(ident(event.after_snapshot)==ident(c.snapshot_id(cp.current))==proposal['post_state_id'],'EXACT_NATIVE_POST_STATE')
    check(command.expected_snapshot==event.parent_snapshot,'RESULT_PRE_STATE_BINDING')
    check(type(cp.events[0].result) is m.ActionReevaluation and cp.events[0].after_snapshot==cp.events[0].parent_snapshot,'RETAINED_NOOP_PREDECESSOR')
    check(c.canonical_bytes(c._wire(cp.initial.context))==c.canonical_bytes(contract['expected_context'])==c.canonical_bytes(c._wire(cp.current.context)),'NATIVE_SCOPE_LINEAGE_GENERATION')
    before=next(d for d in cp.initial.decisions if d.action==command.decision)
    after=next(d for d in cp.current.decisions if d.action==command.decision)
    record=next(e for e in cp.initial.entities if e.id==command.record)
    grant=next(e for e in cp.initial.entities if e.id.value=='E2-GRANT')
    choice=next(k for k in cp.initial.knowledge if k.id.value=='decision-choice:E2-DECIDE')
    authority=next(p for p in cp.initial.predicates if p.id==command.authority)
    use=next(p for p in cp.initial.predicates if p.id.value=='E2-USE-AUTHORITY')
    action=next(a for a in cp.initial.actions if a.id==command.decision)
    check(action.operation is m.OperationClass.ARCHITECT_CONTRACT_DECISION and action.effect is m.EffectClass.NON_EFFECTING,'CANONICAL_ACTION_TYPE_SCOPE')
    expected_dossier=c._identity(c.canonical_bytes(c._wire(before.dossier)),'planner-dossier-sha256')
    choice_pin=c._unwire(w['choice_source']);grant_pin=c._unwire(w['grant_source'])
    check(choice_pin in cp.sources and grant_pin in cp.sources,'PINNED_CHOICE_AND_GRANT')
    choice_bytes=c.load_pinned(ROOT,choice_pin);grant_bytes=c.load_pinned(ROOT,grant_pin)
    choice_source=json.loads(choice_bytes);grant_source=json.loads(grant_bytes)
    scope_source=load_pin(w['scope_authority'])
    check(choice_source['scope_authority']['sha256']==w['scope_authority']['raw_sha256'],'CHOICE_SCOPE_TRUST_ROOT')
    check(scope_source['selected_option']=='AUTHORIZE_PROSPECTIVE_P03_CHECKPOINT_QUALIFICATION' and
          'Bounded synthetic ALLOW_QUALIFICATION_MAPPING capture' in scope_source['permissions'],'P03_AUTHENTICATED_CHOICE_SCOPE')
    check(choice_source['issuer']==scope_source['issuer']=='authenticated human user of this session','NATIVE_CHOICE_ISSUER')
    check(record.provenance.identity==choice_pin.identity==choice.provenance.identity and
          record.provenance==choice.provenance and record.provenance.excerpt.encode()==choice_bytes,'CHOICE_NATIVE_PROVENANCE')
    check(choice_source['dossier']==c._wire(expected_dossier) and
          choice_source['decision']==command.decision.value=='E2-DECIDE' and
          choice_source['option']==command.choice==record.choice==choice.statement=='ALLOW_QUALIFICATION_MAPPING','EXACT_NATIVE_CHOICE_DOSSIER_RESULT')
    check(choice.state is m.KnowledgeState.KNOWN_COMPLETE and choice.validation is m.ValidationState.ACCEPTED,'ACTUAL_ACCEPTED_CHOICE_KNOWLEDGE')
    check(record.decision==command.decision and record.kind is m.EntityKind.AUTHORITY and
          authority.kind is m.PredicateKind.AUTHORITY and authority.entity==record.id and
          authority.permission is m.AuthorityClass.DECIDE and authority.expected==record.target==before.dossier.provenance.identity,'EXACT_DECIDE_RELATION')
    check(grant.provenance.identity==grant_pin.identity and grant.provenance.excerpt.encode()==grant_bytes and
          grant_source['choice']==c._wire(choice_pin.identity) and grant_source['dossier']==c._wire(expected_dossier) and
          grant_source['subject']=='E2-REENTER' and grant_source['permission']=='USE' and grant_source['qualification_only'] is True,'EXACT_PREEXISTING_GRANT_SOURCE')
    check(grant.permissions==(m.AuthorityClass.USE,) and use.entity==grant.id and
          use.permission is m.AuthorityClass.USE and use.expected==grant.target==expected_dossier,'EXACT_USE_RELATION')
    for entity in (record,grant):
        check((entity.scope,entity.lineage,entity.generation)==(cp.initial.context.scope,cp.initial.context.lineage,cp.initial.context.generation) and
              entity.valid_until>=cp.initial.context.tick and entity.provenance.scope==cp.initial.context.scope,'CURRENT_BOUND_ENTITY_CONTEXT')
    check(choice_source['scope']==grant_source['scope']==cp.initial.context.scope and
          choice_source['lineage']==grant_source['lineage']==scope_source['lineage']==cp.initial.context.lineage,'CURRENT_BOUND_CHOICE_SOURCE_CONTEXT')
    readiness=gates.decision_readiness(cp.initial,before)
    check(readiness.state is m.DecisionReadiness.DECISION_READY and not readiness.missing,'INDEPENDENT_DECISION_READINESS')
    check(not gates.blockers(action,cp.initial),'INDEPENDENT_DECISION_ACTIONABILITY')
    decide_before=gates.evaluate_predicate(cp.initial,command.authority)
    decide_after=gates.evaluate_predicate(cp.current,command.authority)
    use_before=gates.evaluate_predicate(cp.initial,use.id)
    use_after=gates.evaluate_predicate(cp.current,use.id)
    check(all(p.state is m.ProofState.PROVED for p in (decide_before,decide_after,use_before,use_after)),'INDEPENDENT_NATIVE_AUTHORITY_PROOFS')

    changed_fields=sorted(f.name for f in fields(m.Snapshot) if not wire_equal(getattr(cp.initial,f.name),getattr(cp.current,f.name)))
    check(changed_fields==['decisions','statuses'],'ONLY_NATIVE_DECISION_STATE_EFFECT')
    db=c._wire(before);da=c._wire(after)
    decision_changes=sorted(k for k in db if c.canonical_bytes(db[k])!=c.canonical_bytes(da[k]))
    expected=contract['independent_state_oracle']
    check(decision_changes==expected['decision_field_changes'],'EXACT_NATIVE_DECISION_FIELD_EFFECTS')
    check(before.stage.value==expected['before_decision_stage'] and after.stage.value==expected['after_decision_stage'] and
          before.record is None and before.recorded_choice is None and after.record==record.id and after.recorded_choice==command.choice,'ACTUAL_RECORDED_DECISION_STATE')
    check(after.history==before.history+(m.DecisionStage.DECISION_RECORDED,),'EXACT_NATIVE_DECISION_HISTORY')
    states_before={s.id:s for s in cp.initial.statuses};states_after={s.id:s for s in cp.current.statuses}
    changes=sorted(i.value for i in states_before if states_before[i]!=states_after[i])
    check(changes==['E2-DECIDE'] and states_before[command.decision].state.value==expected['before_action_status'] and
          states_after[command.decision].state.value==expected['after_action_status'],'EXACT_NATIVE_DECISION_COMPLETION_ONLY')
    unchanged={name:wire_equal(getattr(cp.initial,name),getattr(cp.current,name)) for name in
               ('knowledge','roots','slots','entities','predicates','actions','typed_proofs')}
    check(all(unchanged.values()),'NO_FABRICATED_KNOWLEDGE_AUTHORITY_OR_PROOF_EFFECT')
    check(all(r.state.value==expected['root_state'] for r in cp.current.roots) and
          all(s.state.value==expected['slot_state'] for s in cp.current.slots),'NO_AUTOMATIC_ROOT_SLOT_SATISFACTION')
    check(gates.recorded_decision_valid(cp.current,after),'ACTUAL_RECORDED_DECISION_VALID')
    check(wire_equal(grant,next(e for e in cp.current.entities if e.id==grant.id)),'PREEXISTING_GRANT_UNCHANGED')
    # Separate evidence paths: N13 is not a copy of N12's aggregate outcome.
    n12=[
        {'term':contract['N12_terms'][0],'pass':type(event) is m.ExecutionEvent and type(command) is m.RecordedDecision,'evidence':'Enclosing typed event in immutable native file and checkpoint /bundle/events/1'},
        {'term':contract['N12_terms'][1],'pass':event.sequence==2 and event.parent_event==cp.events[0].identity and event.after_snapshot==c.snapshot_id(cp.current),'evidence':'Native identity/body and retained state/ledger continuity'},
        {'term':contract['N12_terms'][2],'pass':after.record==command.record and after.recorded_choice==command.choice and states_after[command.decision].state is m.ActionState.COMPLETED,'evidence':'Actual retained post-decision fields/status'},
        {'term':contract['N12_terms'][3],'pass':not BARRED and proposal['NEW_A05_OCCURRENCE_CREATED']=='NO','evidence':'No native apply/capture/append/replay permitted; source immutability audit'}]
    n13=[
        {'term':contract['N13_terms'][0],'pass':type(command) is m.RecordedDecision and command.record==record.id and choice.validation is m.ValidationState.ACCEPTED,'evidence':'Exact existing record/knowledge referenced by actual typed command'},
        {'term':contract['N13_terms'][1],'pass':choice.provenance==record.provenance and choice_source['dossier']==c._wire(expected_dossier) and choice_source['issuer']==scope_source['issuer'],'evidence':'Independent native choice/dossier/issuer/scope-root source correspondence'},
        {'term':contract['N13_terms'][2],'pass':decide_after.state is m.ProofState.PROVED and use_after.state is m.ProofState.PROVED,'evidence':'Independent pure native authority queries'},
        {'term':contract['N13_terms'][3],'pass':all(unchanged.values()) and proposal['grant_preexisting'] and not proposal['grant_issuance_proven'],'evidence':'Before/after immutable native field equality; pre-existing grant limitation'},
        {'term':contract['N13_terms'][4],'pass':proposal['original_A05_event_id'] is None and not proposal['original_prefix_gap_closed'],'evidence':'Exact authorized labels/limits; no historical identity assignment'}]
    check(all(x['pass'] for x in n12),'N12_ASSURANCE_NOT_PRESERVED')
    check(all(x['pass'] for x in n13),'N13_ASSURANCE_NOT_PRESERVED')
    ancestry={'status':'PASS','event_id':ident(event.identity),'event_type':'ExecutionEvent<RecordedDecision>',
        'event_payload':c._wire(command),'event_file':sources['immutable_event'],
        'event_in_checkpoint':{**sources['checkpoint'],'pointer':'/bundle/events/1'},
        'event_in_canonical_descendant':{**sources['canonical_descendant'],'pointer':'/bundle/events/1'},
        'parent':ident(event.parent_event),'pre_snapshot':ident(event.parent_snapshot),'post_snapshot':ident(event.after_snapshot),
        'ledger_id':'NOT_EXPOSED_BY_NATIVE_PERSISTENCEBUNDLE','ledger_membership':w['checkpoint_bundle']+'#/bundle/events',
        'ledger_position':2,'zero_based_index':1,'checkpoint_root':cp_rows[0]['id'],'checkpoint_head':cp_rows[-1]['id'],
        'canonical_descendant_root':target_rows[0]['id'],'canonical_descendant_head':target_rows[-1]['id'],
        'canonical_descendant_successor':target_rows[2],
        'event_identity':'PASS','payload_comparison_identity':'qualification-recorded-decision-payload-v1:'+hashlib.sha256(c.canonical_bytes(c._wire(command))).hexdigest(),
        'payload_identity_is_not_native_result_id':True,'scope_lineage_generation':c._wire(cp.current.context),
        'source_pin_count':len(cp.sources),'source_and_policy_pin_validation':'PASS',
        'complete_checkpoint_and_descendant_parent_sequence_hash_checks':'PASS'}
    binding={'status':'PASS','native_RecordDecision_id':'NOT_EXPOSED; use actual enclosing event /result selector',
        'native_result_reference':proposal['recorded_decision_reference'],'record_EntityId':record.id.value,
        'record_AuthorityIdentity':c._wire(record.identity),'native_record_predicate':command.authority.value,
        'choice_evidence_identity':ident(choice_pin.identity),'choice_source':c._wire(choice_pin),
        'choice_source_payload':choice_source,'issuer':choice_source['issuer'],
        'choice_scope_trust_root':w['scope_authority'],'original_T03_issuer_trust_root_envelope_preserved':False,
        'native_dossier_identity':ident(expected_dossier),'native_dossier_provenance_identity':ident(before.dossier.provenance.identity),
        'native_grant_EntityId':grant.id.value,'native_grant_AuthorityIdentity':c._wire(grant.identity),
        'grant_source':c._wire(grant_pin),'grant_source_payload':grant_source,
        'grant_was_already_present':True,'grant_issuance_occurrence_proven':False,
        'DECIDE_proof_before':decide_before.state.value,'DECIDE_proof_after':decide_after.state.value,
        'USE_proof_before':use_before.state.value,'USE_proof_after':use_after.state.value,
        'currentness_domain':'Exact retained qualification boundary; no new execution permission generated'}
    semantic=[]
    rules={
        'decision_event_id':('SEMANTICALLY_EQUIVALENT_UNDER_AUTHORIZED_SCOPE','Exact named P03 event stands for the scoped A05 qualification term; original event remains unknown.'),
        'event_type':('EXACT_NATIVE_MATCH','Actual enclosing ExecutionEvent contains native RecordedDecision.'),
        'payload':('EXACT_NATIVE_MATCH','Five required native fields and exact E2-DECIDE/ALLOW positive semantics; candidate context IDs stay native P03.'),
        'RecordedDecision_binding':('EXACT_NATIVE_MATCH','Actual typed result references the existing native choice record/predicate and exact pre-state.'),
        'choice_evidence_binding':('SEMANTICALLY_EQUIVALENT_UNDER_AUTHORIZED_SCOPE','Existing pinned P03 synthetic choice/issuer/scope root preserved; original T03 identity/envelope not asserted.'),
        'parent_event':('SEMANTICALLY_EQUIVALENT_UNDER_AUTHORIZED_SCOPE','Exact real P03 predecessor, not an invented historical A05/A04 parent.'),
        'pre_state':('SEMANTICALLY_EQUIVALENT_UNDER_AUTHORIZED_SCOPE','Exact native P03 ready state, current immutable command binding.'),
        'post_state':('SEMANTICALLY_EQUIVALENT_UNDER_AUTHORIZED_SCOPE','Exact immutable P03 accepted-decision Snapshot with independent required effects.'),
        'ledger_identity':('SEMANTICALLY_EQUIVALENT_UNDER_AUTHORIZED_SCOPE','Exact retained native checkpoint ledger enrollment, also present in P04 descendant.'),
        'ledger_position':('EXACT_NATIVE_MATCH','Native sequence/index/predecessor and descendant successor directly retained.'),
        'result_authority':('EXACT_NATIVE_MATCH','Native DECIDE and USE relationships/proof queries match; no grant issuance occurrence is required or claimed.'),
        'scope_lineage_generation':('SEMANTICALLY_EQUIVALENT_UNDER_AUTHORIZED_SCOPE','Only exact dossier-authorized P03 context replaces the missing old-lineage qualification occurrence.'),
        'provenance':('SEMANTICALLY_EQUIVALENT_UNDER_AUTHORIZED_SCOPE','Exact existing physical P03 pins/context retained; no old-source or human-choice relabeling.'),
        'ordering':('SEMANTICALLY_EQUIVALENT_UNDER_AUTHORIZED_SCOPE','Local native predecessor -> decision -> checkpoint ordering proven; original prepare/A05/A06 prefix remains separately open.')}
    old_contract=json.loads((ROOT/'docs/plans/qualification/E2_P05_A05_DECISION_ANCESTRY_RECOVERY_1/ancestry-contract-and-assurance.json').read_bytes())
    for term in old_contract['requirements']:
        classification,support=rules[term['term']]
        semantic.append({'term':term['term'],'required_native_witness':term['required_native_witness'],
            'required_in_local_mapping':True,'classification':classification,'pass':True,'support':support,
            'authorization_support':'Exact selected alternate option and named witness/exclusions in sealed dossier'})
    semantic.extend([
        {'term':'original_A04_to_A05_and_full_END_prefix_recovery','required_in_local_mapping':False,'classification':'NOT_REQUIRED',
         'remains_required_elsewhere':True,'status':'UNPROVEN_UNRESOLVED; not waived by local A05 mapping'},
        {'term':'grant_issuance_occurrence','required_in_local_mapping':False,'classification':'NOT_REQUIRED',
         'status':'Not native RecordedDecision responsibility; pre-existing-grant limitation preserved'}])
    mapping={'schema':'E2-P05-A05-AUTHORIZED-ALTERNATE-END-MAPPING-1','classification':proposal['classification'],
        'logical_required_input':proposal['required_input'],'replacement_acceptance_term':'E2-A05.authorized_alternate_native_recorded_decision_event_ancestry',
        'scope_subject':proposal['scope_subject'],'selected_option':proposal['selected_scope_option'],
        'native_event_id':proposal['event_id'],'native_result_reference':proposal['recorded_decision_reference'],
        'native_event':ancestry['event_in_checkpoint'],'native_ancestry':ancestry,
        'RecordedDecision_binding':binding,'semantic_correspondence':semantic,
        'native_effects':{'changed_snapshot_fields':changed_fields,'changed_decision_fields':decision_changes,
            'changed_statuses':changes,'before_status':expected['before_action_status'],'after_status':expected['after_action_status'],
            'unchanged_domains':unchanged,'native_history_before':[x.value for x in before.history],
            'native_history_after':[x.value for x in after.history],'root_slot_unsatisfied':True},
        'END_MAPPING':'PASS_FOR_A05_ALTERNATE_TERM_ONLY','N12_MAPPING':{'result':'PASS','terms':n12},
        'N13_MAPPING':{'result':'PASS','terms':n13},'historical_and_scope_labels':proposal,
        'new_native_operation_or_replay_calls':0,'new_native_events':0,'new_native_grants':0}
    comparison='qualification-a05-alternate-mapping-v1:'+digest(mapping)
    return {'result':'PASS','mapping':mapping,'mapping_comparison_identity':comparison,'barred_calls':BARRED,
        'N12_MAPPING':'PASS','N13_MAPPING':'PASS','END_MAPPING':'PASS','original_full_END_mapping':'UNRESOLVED'}


def main():
    contract=json.loads((OUT/'mapping-contract.json').read_bytes())
    mode=sys.argv[1] if len(sys.argv)>1 else 'native'
    result=qualify(copy.deepcopy(contract['expected_proposal']),contract,mode)
    result['reader']={'pid':os.getpid(),'hash_seed':os.environ.get('PYTHONHASHSEED'),
                      'mode':mode,'native_events_written':0,'native_operation_or_replay_calls':0}
    print(json.dumps(result,sort_keys=True,separators=(',',':')))


if __name__=='__main__':main()
