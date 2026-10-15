"""Generic I02 qualification, independent TEST lineage, no E2 execution."""
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest
from dataclasses import replace,fields
from unittest.mock import patch
from adapter.planner import codec as c, model as m, installation as i, core
from adapter.tests import test_planner_external_unknown as unknown
source=unknown.source

ZERO=c._identity(b'', 'placeholder')
ROOT=Path(__file__).resolve().parents[2]
I01=ROOT/'docs/plans/DETERMINISTIC_PLANNER_V0_1_INSTALLATION_I01_CONTRACT.json'


def definition(route,ctx):
    d=copy.deepcopy(json.loads(I01.read_text())['P04_route_application']['definition_descriptor'])
    p=route.provenance
    d.update(scope=ctx.scope,lineage=ctx.lineage,generation=ctx.generation,content_id=i.simple(p.identity))
    d['subject']={'kind':'EXTERNAL_ROUTE_ROLE','gate':route.gate.value,'requirement':route.requirement.value,'consumer':route.reentry[0].value}
    d['canonical_source_reference']={'kind':'IMMUTABLE_FILE','path':p.path,'content_id':i.simple(p.identity)}
    d['source_pin']={'path':p.path,'profile':'raw-file-sha256','pointer':'','identity':i.simple(p.identity)}
    d['provenance']={'path':p.path,'content_id':i.simple(p.identity),'section':p.section,'method':p.method,'scope':p.scope}
    d['currentness_rule']['consumer']=route.reentry[0].value
    return m.InstallableDefinition(i.digest(d,'planner-installable-definition-v1'),c.canonical_bytes(d).decode(),p)


def request(bundle,defn,op=m.InstallationOperation.REPLACE,receipt_path='install-authority.json',decision=None,contract=None):
    decision=decision or i.digest({'decision':'generic authorized configuration'},'generic-human-decision-v1')
    contract=contract or c._identity(I01.read_bytes(),'raw-file-sha256')
    d,_=i.descriptor(defn)
    authority=m.InstallAuthority(ZERO,m.AuthorityClass.INSTALL,'{}',defn.provenance)
    r=m.InstallDefinition('INSTALL_DEFINITION',1,ZERO,c.bundle_id(bundle),c.snapshot_id(bundle.current),bundle.events[-1].identity,
        len(bundle.events)+1,defn,authority,op,i.old_reference(bundle.current,d),bundle.policy,bundle.policy_version,())
    grant=dict(i.grant_fields(r),schema='PLANNER-INSTALL-GRANT-1',issuer='QUALIFICATION_AUTHORITY',authority_class='INSTALL',
        decision_id=i.simple(decision),contract_id=i.simple(contract),valid_from=0,valid_until=100,use_limit=1,
        delegation=False,provenance=i.simple(decision))
    gid=i.digest(grant,'planner-install-authority-v1',m.IdentityKind.AUTHORITY_IDENTITY)
    authority=i.admit_authority(grant,expected_grant=gid,expected_decision=decision,trusted_issuer='QUALIFICATION_AUTHORITY',receipt_path=receipt_path)
    additions=tuple(m.ArtifactPin(p.path,p.identity) for p in (defn.provenance,authority.admission_provenance)
        if m.ArtifactPin(p.path,p.identity) not in bundle.sources)
    r=replace(r,authority=authority,source_additions=additions)
    return replace(r,command_key=i.command_key(r)),decision


class InstallationTests(unittest.TestCase):
    def setUp(self):
        h=unknown.ExternalUnknownTests();h.setUp();self.addCleanup(h.doCleanups)
        self.root=Path(h.temp.name);s=h.state;g=s.external_gates[0];good=g.resolution_contracts[0]
        w=c._wire(good);w.pop('$type');w.pop('provenance')
        good=replace(good,provenance=source(self.root/'replacement-route.json',{'schema':'EXTERNAL-RESOLUTION-CONTRACT-1','contract':w}))
        bad=replace(g.resolution_contracts[0],provenance=source(self.root/'old-wrapper.json',{'metadata_wrapper':True}))
        s=replace(s,external_gates=(replace(g,resolution_contracts=(bad,)),))
        b=h.bundle(s)
        witness=m.ActionReevaluation((s.actions[0].id,),c.snapshot_id(s),s.actions[0].source)
        self.bundle=c.record_result(b,witness)
        self.defn=definition(good,s.context)
        self.request,self.decision=request(self.bundle,self.defn)
        self.store=self.root/'install-store'

    def commit(self,r=None,b=None,store=None):
        r=r or self.request
        return i.commit(b or self.bundle,r,store or self.store,self.root,expected_authority=r.authority.id,expected_decision=self.decision)

    def test_replace_frame_identity_history_persistence_and_retry(self):
        before=c.bundle_bytes(self.bundle)
        after,bid,noop=self.commit();self.assertFalse(noop)
        self.assertTrue(i.current(after,after.current.installed_definitions[0]))
        self.assertEqual(len(after.events),len(self.bundle.events)+1)
        for f in fields(m.Snapshot):
            if f.name not in ('external_gates','installed_definitions'):
                self.assertEqual(getattr(after.current,f.name),getattr(self.bundle.current,f.name),f.name)
        g=after.current.external_gates[0];old=self.bundle.current.external_gates[0]
        self.assertEqual(replace(g,resolution_contracts=old.resolution_contracts),old)
        self.assertEqual(c.bundle_bytes(c._prefix_bundle(after,len(self.bundle.events))),before)
        self.assertNotIn(m.ArtifactPin(self.defn.provenance.path,self.defn.provenance.identity),c._prefix_bundle(after,1).sources)
        path=self.store/('bundle-'+bid.sha256+'.json')
        restored=c.restore(path,bid,self.root)
        self.assertEqual(c.bundle_id(restored),bid);self.assertEqual(c.snapshot_id(c._replay(restored)),c.snapshot_id(after.current))
        retry,original,noop=self.commit();self.assertTrue(noop);self.assertEqual(original,bid);self.assertEqual(c.bundle_id(retry),bid)
        repeat,repeatid,_=self.commit(store=self.root/'independent-store')
        self.assertEqual(c.bundle_bytes(repeat),c.bundle_bytes(after));self.assertEqual(repeatid,bid)
        # New request key for the same active binding is also a checked no-op.
        duplicate,decision=request(after,self.defn,receipt_path='another-authority.json')
        retry,_,noop=self.commit(duplicate,b=after)
        self.assertTrue(noop);self.assertEqual(c.bundle_id(retry),bid)

    def test_install_absent_role_and_replacement_supersession(self):
        s=replace(self.bundle.initial,external_gates=tuple(replace(g,resolution_contracts=()) for g in self.bundle.initial.external_gates))
        b=replace(self.bundle,initial=s,current=s,events=(),sources=tuple(p for p in self.bundle.sources if p.path!='old-wrapper.json'))
        b=c.record_result(b,m.ActionReevaluation((s.actions[0].id,),c.snapshot_id(s),s.actions[0].source))
        r,_=request(b,self.defn,m.InstallationOperation.INSTALL)
        after,_,_=self.commit(r,b)
        self.assertIsNone(after.current.installed_definitions[0].supersedes)
        route=i.descriptor(self.defn)[1]
        newer=replace(route,provenance=replace(route.provenance,path='third-route.json',method='SECOND_PROSPECTIVE_DEFINITION'))
        r2,_=request(after,definition(newer,s.context),receipt_path='authority-2.json')
        final,_,_=self.commit(r2,after)
        self.assertEqual(final.current.installed_definitions[1].supersedes,after.current.installed_definitions[0].id)
        self.assertFalse(i.current(final,final.current.installed_definitions[0]));self.assertTrue(i.current(final,final.current.installed_definitions[1]))
        self.assertEqual(c.bundle_id(c._prefix_bundle(final,2)),c.bundle_id(after))
        retried,original,noop=self.commit(r,b)
        self.assertTrue(noop);self.assertEqual(original,c.bundle_id(after))
        prior=next(x for x in retried.current.installed_definitions if x.id==after.current.installed_definitions[0].id)
        self.assertFalse(i.current(retried,prior))
        self.assertEqual(c.bundle_id(retried),c.bundle_id(final))

    def test_atomic_validation_and_publish_failure(self):
        r=replace(self.request,expected_old_reference=ZERO);r=replace(r,command_key=i.command_key(r))
        with self.assertRaises(m.PlannerError):self.commit(r)
        self.assertFalse((self.store/'HEAD.json').exists())
        real=os.replace
        def fail_head(src,dst):
            if str(dst).endswith('/HEAD.json'):raise OSError('injected atomic publication failure')
            return real(src,dst)
        with patch('adapter.planner.codec.os.replace',side_effect=fail_head):
            with self.assertRaises(OSError):self.commit()
        self.assertFalse((self.store/'HEAD.json').exists())
        self.assertEqual(c.bundle_id(c._read_head(self.store,self.bundle,self.root)),c.bundle_id(self.bundle))
        after,bid,_=self.commit()
        self.assertTrue(i.current(after,after.current.installed_definitions[0]));self.assertEqual(len(after.events),2)

    def test_security_negatives_and_stale_parent(self):
        cases={
            'no_authority':replace(self.request,authority=replace(self.request.authority,id=ZERO)),
            'wrong_authority_class':replace(self.request,authority=replace(self.request.authority,authority_class=m.AuthorityClass.ATTEST)),
            'wrong_definition':replace(self.request,definition=replace(self.defn,id=ZERO)),
            'wrong_identity_domain':replace(self.request,definition=replace(self.defn,id=replace(self.defn.id,kind=m.IdentityKind.INSTANCE_IDENTITY))),
            'wrong_bytes':replace(self.request,definition=replace(self.defn,provenance=replace(self.defn.provenance,excerpt='{}'))),
            'metadata_wrapper':replace(self.request,definition=replace(self.defn,provenance=self.bundle.current.external_gates[0].resolution_contracts[0].provenance)),
            'conflict_operation':replace(self.request,operation=m.InstallationOperation.CONFLICT),
            'standalone_supersede':replace(self.request,operation=m.InstallationOperation.SUPERSEDE),
            'unauthorized_overwrite':replace(self.request,operation=m.InstallationOperation.INSTALL),
            'foreign_parent':replace(self.request,expected_parent_event=ZERO),
            'wrong_policy':replace(self.request,policy=replace(self.request.policy,identity=ZERO)),
            'wrong_sequence':replace(self.request,sequence=7),
            'wrong_old_reference':replace(self.request,expected_old_reference=ZERO),
            'missing_sources':replace(self.request,source_additions=()),
        }
        for field in ('scope','lineage','generation','definition_type'):
            d=json.loads(self.defn.descriptor_json);d[field]='WRONG'
            bad=replace(self.defn,descriptor_json=c.canonical_bytes(d).decode(),id=i.digest(d,'planner-installable-definition-v1'))
            cases['wrong_'+field]=replace(self.request,definition=bad)
        for name,r in cases.items():
            with self.subTest(name=name):
                with self.assertRaises((m.PlannerError,ValueError)):self.commit(r,store=self.root/('negative-'+name))
                self.assertFalse((self.root/('negative-'+name)/'HEAD.json').exists())
        with self.assertRaises(m.PlannerError):i.commit(self.bundle,self.request,self.store,self.root,expected_authority=ZERO,expected_decision=self.decision)
        with self.assertRaises(m.PlannerError):c.record_result(self.bundle,self.request)
        with self.assertRaises(m.PlannerError):core.apply_event(self.bundle.current,replace(self.request,expected_parent_event=None))
        for typ in ('SLOT_PROOF','ROOT_PROOF','ACTION_RESULT'):
            d=json.loads(self.defn.descriptor_json);d['definition_type']=typ
            bad=replace(self.defn,descriptor_json=c.canonical_bytes(d).decode(),id=i.digest(d,'planner-installable-definition-v1'))
            with self.assertRaises(m.PlannerError):i.descriptor(bad)
        after,_,_=self.commit()
        conflicting=replace(self.request,operation=m.InstallationOperation.INSTALL)
        with self.assertRaises(m.PlannerError):self.commit(conflicting)
        changed=replace(self.request,command_key=i.command_key(conflicting),operation=m.InstallationOperation.INSTALL)
        with self.assertRaises(m.PlannerError):self.commit(changed)
        # Expected old state/parent are no longer valid, for every candidate type.
        self.assertNotEqual(self.request.expected_snapshot,c.snapshot_id(after.current))
        self.assertNotEqual(self.request.expected_parent_event,after.events[-1].identity)
        with self.assertRaises(m.PlannerError):i.validate_prefix(after,self.request)

    def test_authority_admission_is_not_self_authorization(self):
        grant=json.loads(self.request.authority.grant_json)
        gid=self.request.authority.id
        for expected,decision,issuer in [(ZERO,self.decision,'QUALIFICATION_AUTHORITY'),
                (gid,ZERO,'QUALIFICATION_AUTHORITY'),(gid,self.decision,'SYSTEM_OPERATOR')]:
            with self.assertRaises(m.PlannerError):i.admit_authority(grant,expected_grant=expected,
                expected_decision=decision,trusted_issuer=issuer,receipt_path='untrusted.json')
        for field,value in [('authority_class','ATTEST'),('issuer','SYSTEM_OPERATOR'),('delegation',True),
                ('use_limit',2),('valid_until',-1)]:
            wrong=dict(grant);wrong[field]=value
            with self.assertRaises(m.PlannerError):i.admit_authority(wrong,
                expected_grant=i.digest(wrong,'planner-install-authority-v1',m.IdentityKind.AUTHORITY_IDENTITY),
                expected_decision=self.decision,trusted_issuer='QUALIFICATION_AUTHORITY',receipt_path='untrusted.json')
        route=i.descriptor(self.defn)[1]
        wrapper=replace(route,provenance=self.bundle.current.external_gates[0].resolution_contracts[0].provenance)
        well_hashed_wrapper=definition(wrapper,self.bundle.current.context)
        with self.assertRaisesRegex(m.PlannerError,'NATIVE_BODY_REQUIRED'):i.descriptor(well_hashed_wrapper)
        for swapped in (self.bundle.current.actions[0].accepted_inventory,
                self.bundle.current.actions[0],m.ActionResult.PASS):
            with self.assertRaises(m.PlannerError):core.apply_event(self.bundle.current,replace(self.request,definition=swapped))
        from adapter.tests.test_planner_typed_proofs import fixture,candidate
        proof=candidate(fixture().proof_contracts[0])
        with self.assertRaises(m.PlannerError):core.apply_event(self.bundle.current,replace(self.request,definition=proof))

    def test_source_history_missing_records_and_concurrent_head(self):
        route=i.descriptor(self.defn)[1]
        overwriting=replace(route,provenance=replace(route.provenance,path='old-wrapper.json'))
        bad,_=request(self.bundle,definition(overwriting,self.bundle.current.context))
        with self.assertRaisesRegex(m.PlannerError,'INSTALL_SOURCE_OVERWRITE'):self.commit(bad)
        for path in ('../escape.json','/tmp/escape.json','./relative.json'):
            unsafe=definition(replace(route,provenance=replace(route.provenance,path=path)),self.bundle.current.context)
            with self.assertRaisesRegex(m.PlannerError,'DEFINITION_SOURCE_PATH'):i.descriptor(unsafe)
        (self.root/'linked').symlink_to(self.root,target_is_directory=True)
        unsafe=definition(replace(route,provenance=replace(route.provenance,path='linked/body.json')),self.bundle.current.context)
        r,_=request(self.bundle,unsafe)
        with self.assertRaisesRegex(m.PlannerError,'symlinked source path'):self.commit(r)
        self.assertFalse((self.store/'HEAD.json').exists())
        after,bid,_=self.commit()
        with patch('adapter.planner.installation.admit_authority',side_effect=AssertionError('reissued authority')), \
                patch('adapter.planner.core.apply_result',side_effect=AssertionError('executed action')), \
                patch('adapter.planner.core.apply_receipt',side_effect=AssertionError('executed receipt')):
            self.assertEqual(c.snapshot_id(c._replay(after)),c.snapshot_id(after.current))
        for broken in (replace(after,current=replace(after.current,installed_definitions=())),
                replace(after,sources=tuple(p for p in after.sources if p.identity!=self.request.authority.admission_provenance.identity))):
            with self.assertRaises(m.PlannerError):c.bundle_bytes(broken)
        receipt=self.root/self.request.authority.admission_provenance.path
        moved=receipt.with_suffix('.missing');receipt.rename(moved)
        try:
            with self.assertRaises(m.PlannerError):c.restore(self.store/('bundle-'+bid.sha256+'.json'),bid,self.root)
        finally:moved.rename(receipt)
        changed=replace(route,provenance=replace(route.provenance,path='competing-route.json'))
        competing,_=request(self.bundle,definition(changed,self.bundle.current.context),receipt_path='competing-grant.json')
        with self.assertRaisesRegex(m.PlannerError,'INSTALL_STALE_HEAD'):self.commit(competing)
        self.assertEqual(c.bundle_id(c._read_head(self.store,self.bundle,self.root)),bid)

    def test_process_crash_before_and_after_head(self):
        prepath,preid=c.save_bundle(self.bundle,self.root/'pre',self.root)
        reqpath=self.root/'request.json';reqpath.write_bytes(c.canonical_bytes(c._wire(self.request)))
        program='''import json,os,sys
from adapter.planner import codec as c,installation as i
b=c.restore(sys.argv[1],c._unwire(json.loads(sys.argv[2])),sys.argv[3])
r=c._unwire(c.parse_json(open(sys.argv[4],'rb').read()))
stage=sys.argv[8]
if stage=='before':
 real=os.replace
 def crash(src,dst):
  if str(dst).endswith('/HEAD.json'):os._exit(77)
  return real(src,dst)
 c.os.replace=crash
else:
 real=c._publish_head
 def crash(*args):
  real(*args)
  os._exit(78)
 c._publish_head=crash
i.commit(b,r,sys.argv[5],sys.argv[3],expected_authority=c._unwire(json.loads(sys.argv[6])),expected_decision=c._unwire(json.loads(sys.argv[7])))
'''
        env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(ROOT))
        for stage,code in [('before',77),('after',78)]:
            store=self.root/('crash-'+stage)
            run=subprocess.run([sys.executable,'-c',program,str(prepath),json.dumps(c._wire(preid)),str(self.root),str(reqpath),str(store),
                json.dumps(c._wire(self.request.authority.id)),json.dumps(c._wire(self.decision)),stage],env=env,cwd=str(ROOT),capture_output=True,text=True)
            self.assertEqual(run.returncode,code,run.stderr)
            head=c._read_head(store,self.bundle,self.root)
            self.assertEqual(len(head.events),1 if stage=='before' else 2)
            recovered,bid,noop=self.commit(store=store)
            self.assertEqual(noop,stage=='after');self.assertEqual(len(recovered.events),2)
            self.assertTrue(i.current(recovered,recovered.current.installed_definitions[0]))

    def test_currentness_invalidation_expiry_context_and_no_fallback(self):
        after,_,_=self.commit();record=after.current.installed_definitions[0]
        for pin in i.support_ids(self.request):
            withdrawn=c.record_result(after,m.SourceInvalidation((pin,),c.snapshot_id(after.current)))
            self.assertFalse(i.current(withdrawn,withdrawn.current.installed_definitions[0]))
            self.assertFalse(i.route_support_current(withdrawn.current,withdrawn.current.external_gates[0].resolution_contracts[0]))
            self.assertEqual(len(withdrawn.current.installed_definitions),1)
            self.assertEqual(withdrawn.current.external_gates[0].resolution_contracts,after.current.external_gates[0].resolution_contracts)
        for f,v in [('tick',101),('scope','WRONG'),('lineage','WRONG'),('generation','WRONG')]:
            bad=replace(after,current=replace(after.current,context=replace(after.current.context,**{f:v})))
            self.assertFalse(i.current(bad,record))
            self.assertFalse(i.route_support_current(bad.current,bad.current.external_gates[0].resolution_contracts[0]))
        no_event=replace(after,events=after.events[:-1])
        self.assertFalse(i.current(no_event,record))

    def test_fresh_process_reader_and_determinism(self):
        prepath,preid=c.save_bundle(self.bundle,self.root/'pre',self.root)
        request_path=self.root/'request.json';request_path.write_bytes(c.canonical_bytes(c._wire(self.request)))
        writer='''import json,sys
from adapter.planner import codec as c,installation as i
b=c.restore(sys.argv[1],c._unwire(json.loads(sys.argv[2])),sys.argv[3])
r=c._unwire(c.parse_json(open(sys.argv[4],'rb').read()))
after,bid,_=i.commit(b,r,sys.argv[5],sys.argv[3],expected_authority=c._unwire(json.loads(sys.argv[6])),expected_decision=c._unwire(json.loads(sys.argv[7])))
print(bid.sha256)
'''
        env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(ROOT))
        run=subprocess.run([sys.executable,'-c',writer,str(prepath),json.dumps(c._wire(preid)),str(self.root),str(request_path),str(self.store),
            json.dumps(c._wire(self.request.authority.id)),json.dumps(c._wire(self.decision))],env=env,cwd=str(ROOT),capture_output=True,text=True)
        self.assertEqual(run.returncode,0,run.stderr)
        bid=m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY,'planner-bundle-v1',run.stdout.strip())
        path=self.store/('bundle-'+bid.sha256+'.json')
        after=c.restore(path,bid,self.root)
        program='''import json,sys
from adapter.planner import codec as c,installation as i
b=c.restore(sys.argv[1],c._unwire(json.loads(sys.argv[2])),sys.argv[3])
assert bool(b.current.installed_definitions)==(sys.argv[4]=='installed')
if b.current.installed_definitions:assert i.current(b,b.current.installed_definitions[0])
print(c.bundle_id(b).sha256+" "+c.snapshot_id(c._replay(b)).sha256)
'''
        # The writer exited; three new readers per checkpoint and hash seed.
        for checkpoint,ident,state,stage in [(prepath,preid,self.bundle.current,'before'),(path,bid,after.current,'installed')]:
            expected=ident.sha256+' '+c.snapshot_id(state).sha256
            for seed in ('0','1','7','101'):
                for reader in range(3):
                    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED=seed,PYTHONPATH=str(ROOT))
                    run=subprocess.run([sys.executable,'-c',program,str(checkpoint),json.dumps(c._wire(ident)),str(self.root),stage],env=env,cwd=str(ROOT),capture_output=True,text=True)
                    self.assertEqual(run.returncode,0,run.stderr);self.assertEqual(run.stdout.strip(),expected)
        permuted=replace(after,sources=tuple(reversed(after.sources)),current=replace(after.current,installed_definitions=tuple(reversed(after.current.installed_definitions))))
        self.assertEqual(c.bundle_id(permuted),bid)

if __name__=='__main__':unittest.main()
