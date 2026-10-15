"""Run sealed A04 and durable overlay controls against isolated evidence."""
from dataclasses import replace
import copy
import hashlib
from pathlib import Path
import shutil
import unittest
from unittest.mock import patch

import execution_driver as d
from adapter.planner import codec as c, core, dossier_transaction as dt, model as m

ZERO=c._identity(b'wrong','planner-snapshot-v1')


def hashes(path):
    return {str(p.relative_to(path)):hashlib.sha256(p.read_bytes()).hexdigest()
            for p in path.rglob('*') if p.is_file()}


def descriptor():
    return {**d.LABELS,'kind':'NATIVE_D01_ADMITTED_TRANSACTION',
        'native_head_directory':str(d.OUT/'primary/native-head'),
        'writer_report':str(d.OUT/'primary/writer-result.json'),
        'original_historical_event_ids':None,'original_history_splice':False,
        'scope_authorization_subject':d.read(d.DA/'versioned-overlay.json')['authorization_subject'],
        'selected_option':'AUTHORIZE_PROSPECTIVE_P05_A04_ANCESTRY_QUALIFICATION'}


def validate_witness(evidence):
    """Read-only END qualification witness guard, not a new native END API."""
    dt.require(type(evidence) is dict and evidence.get('kind')=='NATIVE_D01_ADMITTED_TRANSACTION',
               'NATIVE_ANCESTRY_TRANSACTION_REQUIRED')
    for key,value in d.LABELS.items():
        dt.require(evidence.get(key)==value,'HISTORICAL_LABEL_SEPARATION_REQUIRED:'+key)
    dt.require(evidence.get('original_historical_event_ids') is None and
        evidence.get('original_history_splice') is False,'ORIGINAL_IDENTITY_SUBSTITUTION_FORBIDDEN')
    overlay=d.read(d.DA/'versioned-overlay.json')
    dt.require(evidence.get('scope_authorization_subject')==overlay['authorization_subject'] and
        evidence.get('selected_option')==overlay['scope_decision'],'EXACT_SCOPE_AUTHORIZATION_REQUIRED')
    store=Path(evidence['native_head_directory']);writer=d.read(evidence['writer_report'])
    dt.require((store/'HEAD.json').is_file(),'PUBLISHED_NATIVE_OCCURRENCE_REQUIRED')
    dt.require(writer['producer_invocations']==1 and writer['actual_native_transaction'] is True and
        writer['oracle_files_read_by_producer']==[],'ACTUAL_OPERATION_WITNESS_REQUIRED')
    for key,value in d.LABELS.items():dt.require(writer.get(key)==value,'WRITER_HISTORY_LABELS')
    before,bid,artifacts=d.load_start()
    head=d.read(store/'HEAD.json');postid=c._unwire(head['bundle'])
    bundle=c.restore(store/('bundle-'+postid.sha256+'.json'),postid,d.ROOT)
    c._read_head(store,before,d.ROOT)
    d.check_bundle(before,bundle,c.snapshot_resolver(store))
    event=bundle.events[2]
    d.native_equal('REPORT_ACTUAL_NATIVE_EVENT',event,c._unwire(writer['EVENT_PAYLOAD']))
    d.equal('EVENT_FILE_BYTES',(store/('event-'+event.identity.sha256+'.json')).read_bytes(),c.canonical_bytes(c._wire(event)))
    d.equal('POST_CONTEXT',bundle.current.context,before.current.context)
    d.equal('NO_NEW_AUTHORITY',bundle.current.entities,before.current.entities)
    return bundle


def main():
    primary=d.OUT/'primary/native-head';original_hashes=hashes(primary)
    bundle=validate_witness(descriptor());before,bid,artifacts=d.load_start()
    result=bundle.events[-1].result;vs=bundle.current.validation_instances
    resolver=c.snapshot_resolver(primary)
    negative_root=d.OUT/'negatives';negative_root.mkdir(exist_ok=True)
    output=[]
    def reject(case,operation,layer):
        prebytes=c.bundle_bytes(before);captured=None
        try:operation()
        except (m.PlannerError,d.Divergence) as exc:captured=str(exc)
        if captured is None:raise d.Divergence('NEGATIVE_ACCEPTED:'+case,True,False)
        d.equal('NEGATIVE_PRE_STATE_UNCHANGED',c.bundle_bytes(before),prebytes)
        d.equal('PRIMARY_NOT_MUTATED',hashes(primary),original_hashes)
        sealed=next(x for x in d.read(d.BASE/'negative-contract.json')['cases'] if x['case']==case)
        output.append({**sealed,'result':'PASS','status':'EXECUTED_FAIL_CLOSED','observed_rejection':captured,
            'test_layer':layer,'primary_lineage_unchanged':True,'durable_new_occurrences':0})
    def operands(supplied=result,validations=vs,state=before.current):
        dt.validate_operands(state,supplied,validations,bundle.sources,before.events)
        return core.admit_dossier_materialization(state,supplied,validations)
    def changed(supplied=None,after=None,**fields):
        post=after or bundle.current;old=bundle.events[-1]
        event=replace(old,result=supplied or old.result,after_snapshot=c.snapshot_id(post),**fields)
        event=replace(event,identity=c._event_identity(event.sequence,event.parent_snapshot,event.parent_event,
                                                     event.result,event.after_snapshot,event.resume_binding))
        binding=replace(bundle.dossier_materializations[0],event_identity=event.identity)
        wrong=replace(bundle,current=post,events=bundle.events[:-1]+(event,),dossier_materializations=(binding,))
        return c._replay(wrong,snapshot_resolver=dt.memory_resolver((post,)))
    altered=replace(before.current,knowledge=(replace(before.current.knowledge[0],statement='wrong'),)+before.current.knowledge[1:])
    reject('WRONG_A04_INPUT',lambda:operands(state=altered),'NATIVE_PRE_STATE_BINDING')
    reject('WRONG_PREPARE_RESULT',lambda:operands(replace(result,result=m.ActionResult.FAIL)),'NATIVE_TYPED_RESULT_ADMISSION')
    reject('WRONG_OUTPUT',lambda:operands(replace(result,knowledge=())),'NATIVE_RESULT_INVENTORY')
    reject('WRONG_PARENT',lambda:changed(parent_event=ZERO),'NATIVE_LEDGER_REPLAY')
    reject('WRONG_PRE_STATE',lambda:operands(replace(result,expected_snapshot=ZERO)),'NATIVE_PRE_STATE_BINDING')
    reject('WRONG_EVENT_PAYLOAD',lambda:changed(supplied=replace(result,dossier=replace(result.dossier,question='wrong'))),'NATIVE_RESULT_SNAPSHOT_PROJECTION')
    foreign=replace(bundle,initial=replace(bundle.initial,context=replace(bundle.initial.context,lineage='foreign')))
    reject('WRONG_LEDGER',lambda:c._replay(foreign,snapshot_resolver=resolver),'NATIVE_LEDGER_MEMBERSHIP')
    reject('WRONG_APPEND_POSITION',lambda:changed(sequence=4),'NATIVE_LEDGER_REPLAY')
    reject('WRONG_PREDECESSOR',lambda:c._replay(replace(bundle,events=(bundle.events[1],bundle.events[0],bundle.events[2])),snapshot_resolver=resolver),'NATIVE_ORDERED_LEDGER')
    successor=replace(bundle.events[-1],sequence=4,parent_event=ZERO,parent_snapshot=c.snapshot_id(bundle.current))
    successor=replace(successor,identity=c._event_identity(4,successor.parent_snapshot,ZERO,successor.result,successor.after_snapshot))
    reject('WRONG_SUCCESSOR_IF_PRESENTED',lambda:c._replay(replace(bundle,events=bundle.events+(successor,)),snapshot_resolver=resolver),'NATIVE_CONDITIONAL_DESCENDANT_LINK')
    reject('WRONG_AUTHORITY',lambda:validate_witness(dict(descriptor(),scope_authorization_subject='foreign')),'QUALIFICATION_SCOPE_AUTHORIZATION')
    reject('WRONG_SCOPE',lambda:operands(validations=(replace(vs[0],scope='PRODUCTION'),)+vs[1:]),'NATIVE_TYPED_VALIDATION')
    reject('WRONG_LINEAGE',lambda:operands(validations=(replace(vs[0],lineage='ORIGINAL'),)+vs[1:]),'NATIVE_TYPED_VALIDATION')
    reject('WRONG_PROVENANCE',lambda:operands(validations=(replace(vs[0],provenance=replace(vs[0].provenance,path='foreign.json')),)+vs[1:]),'NATIVE_TYPED_SOURCE_BINDING')
    reject('FOREIGN_EVENT',lambda:changed(supplied=replace(result,action=m.ActionId('E2-FINISH'))),'NATIVE_EVENT_RESULT_ACTION_BINDING')
    reject('SNAPSHOT_AS_ANCESTRY',lambda:validate_witness(bundle.current),'QUALIFICATION_NATIVE_OCCURRENCE_GUARD')
    reject('REPORT_AS_ANCESTRY',lambda:validate_witness({'result':'PASS','parent':'summary'}),'QUALIFICATION_NATIVE_OCCURRENCE_GUARD')
    reject('OCCURRENCE_WITHOUT_PARENT_PROOF',lambda:c._replay(replace(bundle,events=(bundle.events[-1],)),snapshot_resolver=resolver),'NATIVE_LEDGER_PARENT_ENROLLMENT')
    reject('PROSPECTIVE_LABELED_HISTORICAL',lambda:validate_witness(dict(descriptor(),ORIGINAL_A04_HISTORICAL_ANCESTRY='PROVEN')),'QUALIFICATION_HISTORICAL_LABEL_GUARD')
    reject('PROSPECTIVE_AS_ORIGINAL_IDENTITY',lambda:validate_witness(dict(descriptor(),original_historical_event_ids=[d.uid(bundle.events[-1].identity)])),'QUALIFICATION_IDENTITY_SEPARATION')
    reject('SELECTION_AS_COMPLETION_N12',lambda:dt.commit(core.recompute(before.current),negative_root/'N12-store',d.ROOT),'NATIVE_ACTUAL_EXECUTION_CONTEXT')
    action=next(a for a in before.current.actions if a.id.value=='E2-PREPARE')
    reject('DECLARATION_AS_RESULT_N13',lambda:dt.commit(action.accepted_inventory[0],negative_root/'N13-store',d.ROOT),'NATIVE_ACTUAL_EXECUTION_CONTEXT')
    reject('MISSING_OR_INVALID_INDEPENDENT_VALIDATION',lambda:operands(validations=vs[:-1]),'NATIVE_COMPLETE_TYPED_MEMBER_SET')
    reject('EVENT_WITHOUT_ATOMIC_NATIVE_ADMISSION',lambda:dt.commit(bundle.events[-1],negative_root/'N24-store',d.ROOT),'NATIVE_D01_ORIGIN_CHECKED_ATOMIC_COMMIT')
    d.equal('SEALED_A04_NEGATIVE_COUNT',len(output),24)
    # Additional native post-Snapshot controls required by the representation overlay.
    overlay=[]
    for name,operation in [
        ('FOREIGN_POST_SNAPSHOT',lambda:c._replay(bundle,snapshot_resolver=lambda identity:before.current)),
        ('TAMPERED_POST_STATE_REHASHED',lambda:changed(after=replace(bundle.current,context=replace(bundle.current.context,generation='foreign')))),
        ('VALIDATION_FOREIGN_SNAPSHOT',lambda:changed(after=replace(bundle.current,validation_instances=(replace(vs[0],inputs=(ZERO,vs[0].inputs[1])),)+vs[1:]))),
        ('VALIDATION_DUPLICATE',lambda:operands(validations=vs+vs[:1])),
        ('VALIDATION_REJECTED',lambda:operands(validations=(replace(vs[0],result=m.ValidationOutcome.FAIL),)+vs[1:])),
        ('BOOLEAN_AS_TYPED_VALIDATION',lambda:operands(validations=True)),
        ('ORDERED_INPUT_REVERSAL',lambda:operands(validations=(replace(vs[0],inputs=vs[0].inputs[::-1]),)+vs[1:]))]:
        try:operation()
        except m.PlannerError as exc:overlay.append({'case':name,'result':'PASS','rejection':str(exc)})
        else:raise d.Divergence('OVERLAY_NEGATIVE_ACCEPTED:'+name,True,False)
    d.equal('PRIMARY_AFTER_ALL_NEGATIVES',hashes(primary),original_hashes)
    d.write(d.OUT/'A04-negative-results.json',{**d.LABELS,'result':'PASS','cases':output,
        'sealed_A04_negative_count':24,'snapshot_validation_overlay_cases':overlay,
        'N12_MAPPING':'PASS','N13_MAPPING':'PASS','successful_lineage_mutated':False})


if __name__=='__main__':
    main()
