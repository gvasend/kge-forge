"""Generic Action replacement tests in a TEST lineage."""
import json, unittest
from dataclasses import replace,fields
from pathlib import Path
from unittest.mock import patch
from adapter.planner import codec as c,model as m,installation as i,action_installation as ai
from adapter.tests.test_planner_installation import InstallationTests,request,ZERO

def definition(root,old,new,ctx,name='action-definition.json'):
    raw=c.canonical_bytes({'schema':'PLANNER-ACTION-DEFINITION-1','contract':{'old_action':c._wire(old),'action':c._wire(new),'allowed_changes':[f.name for f in fields(old) if getattr(old,f.name)!=getattr(new,f.name)]}})
    path=root/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw)
    p=m.Provenance(name,c._identity(raw,'raw-file-sha256'),'/',raw.decode(),'ACTION_DEFINITION_SOURCE',ctx.scope)
    subject={'kind':'ACTION_ROLE','action':old.id.value,'consumer':'O01/model.Action/gates.validate_result/core.apply_result'}
    d={'schema':'PLANNER-INSTALLABLE-DEFINITION-1','definition_type':ai.TYPE,'canonical_body_schema':'PLANNER-ACTION-DEFINITION-1','content_id':i.simple(p.identity),'subject':subject,'scope':ctx.scope,'lineage':ctx.lineage,'generation':ctx.generation,'canonical_source_reference':{'kind':'IMMUTABLE_FILE','path':name,'content_id':i.simple(p.identity)},'source_pin':{'path':name,'profile':'raw-file-sha256','pointer':'','identity':i.simple(p.identity)},'provenance':{'path':name,'content_id':i.simple(p.identity),'section':'/','method':p.method,'scope':p.scope},'currentness_rule':{'schema':'PLANNER-DEFINITION-CURRENTNESS-1','rule_id':'ACTION_DEFINITION_CURRENT_V1','consumer':subject['consumer'],'activation_witness':'OWN_INSTALL_EVENT_AND_EXACT_ACTION','authority_current_required':True,'exact_scope_lineage_generation_required':True,'installation_required':True,'source_current_required':True}}
    return m.InstallableDefinition(i.digest(d,'planner-installable-definition-v1'),c.canonical_bytes(d).decode(),p)

class ActionInstallationTests(unittest.TestCase):
    def setUp(self):
        h=InstallationTests();h.setUp();self.addCleanup(h.doCleanups)
        self.root=h.root;self.bundle=h.bundle;self.old=self.bundle.current.actions[0]
        k=m.KnowledgeRecord(m.KnowledgeId('TEST-OUTPUT'),m.KnowledgeState.KNOWN_COMPLETE,'test output',self.old.source,(),m.ValidationState.ACCEPTED,self.old.id,m.ActionResult.PASS)
        self.new=replace(self.old,accepted_inventory=(k,),pass_model_complete=True)
        self.defn=definition(self.root,self.old,self.new,self.bundle.current.context)
        self.request,self.decision=request(self.bundle,self.defn)

    def commit(self,r=None,store='action-store'):
        r=r or self.request
        return i.commit(self.bundle,r,self.root/store,self.root,expected_authority=self.request.authority.id,expected_decision=self.decision)

    def test_positive_frame_history_restore_retry_and_determinism(self):
        after,bid,_=self.commit();record=after.current.installed_definitions[-1]
        self.assertTrue(i.current(after,record));self.assertTrue(ai.action_current(after.current,self.new))
        for f in fields(m.Snapshot):
            if f.name not in ('actions','installed_definitions'):self.assertEqual(getattr(after.current,f.name),getattr(self.bundle.current,f.name),f.name)
        self.assertEqual(c.bundle_bytes(c._prefix_bundle(after,len(self.bundle.events))),c.bundle_bytes(self.bundle))
        cold=c.restore(self.root/'action-store'/('bundle-'+bid.sha256+'.json'),bid,self.root)
        self.assertEqual(c.bundle_bytes(cold),c.bundle_bytes(after))
        _,rid,no=self.commit();self.assertTrue(no);self.assertEqual(rid,bid)
        again,aid,_=self.commit(store='independent');self.assertEqual(aid,bid);self.assertEqual(c.bundle_bytes(again),c.bundle_bytes(after))

    def test_independent_field_changes(self):
        for n,new in enumerate((replace(self.old,accepted_inventory=self.new.accepted_inventory),replace(self.old,pass_model_complete=not self.old.pass_model_complete))):
            d=definition(self.root,self.old,new,self.bundle.current.context,'one-%d.json'%n)
            r,decision=request(self.bundle,d,receipt_path='authority-%d.json'%n)
            b,_,_=i.commit(self.bundle,r,self.root/('one-store-%d'%n),self.root,expected_authority=r.authority.id,expected_decision=decision)
            self.assertEqual(next(a for a in b.current.actions if a.id==new.id),new)

    def test_codec_unordered_action_collections(self):
        k=self.new.accepted_inventory[0]
        new=replace(self.new,accepted_inventory=(k,replace(k,id=m.KnowledgeId('TEST-SECOND-OUTPUT'))))
        d=definition(self.root,self.old,new,self.bundle.current.context,'two-outputs.json')
        r,decision=request(self.bundle,d,receipt_path='two-authority.json')
        after,_,_=i.commit(self.bundle,r,self.root/'two-store',self.root,expected_authority=r.authority.id,expected_decision=decision)
        from adapter.tests.qualify_reentry_r04 import permute
        reordered=permute(after)
        self.assertEqual(c.bundle_bytes(reordered),c.bundle_bytes(after))
        self.assertTrue(i.current(reordered,reordered.current.installed_definitions[-1]))
        self.assertEqual(c.snapshot_id(c._replay(reordered)),c.snapshot_id(after.current))

    def test_bounded_substitution_negatives(self):
        changes=[replace(self.new,id=m.ActionId('FOREIGN')),replace(self.new,accepted_inventory=()),replace(self.new,pass_model_complete=False),replace(self.new,prerequisites=()),replace(self.new,source=replace(self.new.source,scope='foreign'))]
        # Every different definition remains outside the existing exact grant, even if well typed.
        for n,new in enumerate(changes):
            with self.subTest(n=n):
                try:d=definition(self.root,self.old,new,self.bundle.current.context,'bad-%d.json'%n);r=replace(self.request,definition=d);r=replace(r,command_key=i.command_key(r));self.commit(r,store='bad-%d'%n)
                except m.PlannerError:pass
                else:self.fail('unauthorized substitution')
        for r in (replace(self.request,expected_parent_event=ZERO),replace(self.request,expected_snapshot=ZERO),replace(self.request,operation=m.InstallationOperation.INSTALL),replace(self.request,authority=replace(self.request.authority,authority_class=m.AuthorityClass.ATTEST))):
            with self.assertRaises(m.PlannerError):self.commit(replace(r,command_key=i.command_key(r)))
        for field in ('scope','lineage','generation'):
            dd=json.loads(self.defn.descriptor_json);dd[field]='FOREIGN'
            bad=replace(self.defn,id=i.digest(dd,'planner-installable-definition-v1'),descriptor_json=c.canonical_bytes(dd).decode())
            rr=replace(self.request,definition=bad)
            with self.assertRaises(m.PlannerError):self.commit(replace(rr,command_key=i.command_key(rr)))

    def test_closed_body_no_results_or_completion(self):
        body=json.loads(self.defn.provenance.excerpt)
        for mutate in ('state','result','missing-field','wrong-type'):
            b=json.loads(json.dumps(body))
            if mutate=='missing-field':del b['contract']['action']['effect']
            elif mutate=='wrong-type':b['contract']['action']['$type']='SuppliedResult'
            else:b['contract']['action'][mutate]='COMPLETED'
            raw=c.canonical_bytes(b);p=replace(self.defn.provenance,excerpt=raw.decode(),identity=c._identity(raw,'raw-file-sha256'))
            d=json.loads(self.defn.descriptor_json);d['content_id']=i.simple(p.identity);d['source_pin']['identity']=i.simple(p.identity);d['canonical_source_reference']['content_id']=i.simple(p.identity);d['provenance']['content_id']=i.simple(p.identity)
            bad=m.InstallableDefinition(i.digest(d,'planner-installable-definition-v1'),c.canonical_bytes(d).decode(),p)
            with self.assertRaises(m.PlannerError):ai.descriptor(bad)

    def test_failure_before_publish_no_partial_head(self):
        before=c.bundle_bytes(self.bundle)
        with patch.object(c,'_extend_private',side_effect=m.PlannerError('injected before publication')):
            with self.assertRaises(m.PlannerError):self.commit()
        self.assertFalse((self.root/'action-store'/'HEAD').exists());self.assertEqual(c.bundle_bytes(self.bundle),before)

    def test_invalidation_and_context_fail_closed(self):
        after,_,_=self.commit();rec=after.current.installed_definitions[-1]
        for snapshot in (replace(after.current,installed_definitions=after.current.installed_definitions[:-1]+(replace(rec,validation=m.ValidationState.STALE),)),replace(after.current,context=replace(after.current.context,lineage='foreign'))):
            self.assertFalse(ai.action_current(snapshot,self.new))
        event=m.SourceInvalidation((self.defn.provenance.identity,),c.snapshot_id(after.current))
        stale=c.record_result(after,event)
        self.assertFalse(i.current(stale,stale.current.installed_definitions[-1]))

if __name__=='__main__':unittest.main()
