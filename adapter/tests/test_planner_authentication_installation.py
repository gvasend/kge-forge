"""I04 generic, non-E2 adapter qualification with independent native fixtures."""
import copy,json,hashlib,os,subprocess,sys
from pathlib import Path
from dataclasses import replace,fields
from unittest.mock import patch
import unittest
from adapter.planner import codec as c,model as m,installation as i,authentication_installation as a,core,evidence as ev,evidence_attestation as ea
from adapter.tests.test_planner_installation import request as make_request
from adapter.tests import test_planner_external_unknown as unknown
ROOT=Path(__file__).resolve().parents[2]
CONTRACT=ROOT/'docs/plans/DETERMINISTIC_PLANNER_V0_1_INSTALLATION_I03_ATTEST_INGRESS_CONTRACT.json'
ZERO=c._identity(b'','placeholder')


def definition(d,body,path):
    d=copy.deepcopy(d);raw=c.canonical_bytes(body);cid=c._identity(raw,'raw-file-sha256');scope=d['scope']
    d.update(content_id=i.simple(cid),canonical_source_reference={'kind':'IMMUTABLE_FILE','path':path,'content_id':i.simple(cid)},source_pin={'path':path,'profile':'raw-file-sha256','pointer':'','identity':i.simple(cid)},provenance={'path':path,'content_id':i.simple(cid),'section':'/','method':'I03-PROSPECTIVE-DEFINITION-1','scope':scope})
    p=m.Provenance(path,cid,'/',raw.decode(),'I03-PROSPECTIVE-DEFINITION-1',scope)
    return m.InstallableDefinition(i.digest(d,'planner-installable-definition-v1'),c.canonical_bytes(d).decode(),p)


def operating(defn,decision,contract,path):
    d,n=i.descriptor(defn);b=c.parse_json(defn.provenance.excerpt.encode());s=d['subject']
    g={'schema':'PLANNER-ATTEST-DEFINITION-AUTHORIZATION-1','authority_class':'ATTEST','issuer':'AUTHENTICATED_HUMAN_USER','issuer_role':'QUALIFICATION_AUTHORITY','authenticated_decision_reference':i.simple(decision),'I03_contract_content_reference':i.simple(contract),'declared_authority_identity':b['authority_reference'],'member_definition_and_content_ids':{k:{'definition_id':v['definition_id'],'content_id':v['content_id']} for k,v in b['members'].items()},'source':s['source'],'consumer':s['consumer'],'gate':s['gate'],'requirement':s['requirement'],'scope':d['scope'],'lineage':d['lineage'],'generation':d['generation'],'valid_from':0,'valid_until':100,'delegation':False,'provenance':i.simple(decision)}
    gid=i.digest(g,'planner-attest-definition-authorization-v1',m.IdentityKind.AUTHORITY_IDENTITY)
    return a.admit_operating_authority(g,expected_grant=gid,expected_decision=decision,trusted_issuer='QUALIFICATION_AUTHORITY',receipt_path=path)


def request(bundle,defn,decision,contract,path,binding=None):
    r,_=make_request(bundle,defn,op=m.InstallationOperation.INSTALL,decision=decision,contract=contract,receipt_path=path)
    r=replace(r,authority_bindings=(binding,) if binding else ())
    ps=i.request_provenances(r);r=replace(r,source_additions=tuple(m.ArtifactPin(p.path,p.identity) for p in ps if m.ArtifactPin(p.path,p.identity) not in bundle.sources))
    return replace(r,command_key=i.command_key(r))


def generic_definitions(snapshot):
    x=json.loads(CONTRACT.read_text());ctx=snapshot.context;g=snapshot.external_gates[0];req=snapshot.evidence_requirements[0];src=req.producers[0]
    s={'kind':'INGRESS_AUTHENTICATION_ROLE','gate':g.id.value,'requirement':req.id.value,'consumer':'TEST-INGRESS','source':c._wire(src),'receipt_action':g.receipt_action}
    d=copy.deepcopy(x['P04_mapping']['authentication_set']['descriptor']);d.update(scope=ctx.scope,lineage=ctx.lineage,generation=ctx.generation,subject=s);d['currentness_rule']['consumer']=s['consumer']
    b=copy.deepcopy(x['P04_mapping']['authentication_set']['canonical_body']);b.update(scope=ctx.scope,lineage=ctx.lineage,generation=ctx.generation,binding={k:v for k,v in s.items() if k!='kind'})
    aid=i.digest({'native_authority':'TEST-I04','source':c._wire(src)},'test-operating-attest',m.IdentityKind.AUTHORITY_IDENTITY);tid=i.digest({'native_attestor':'TEST-I04','source':c._wire(src)},'test-attestor',m.IdentityKind.AUTHORITY_IDENTITY)
    b['authority_reference']=c._wire(aid)
    for k,v in b['members'].items():
        body=v['body'];body.update(scope=ctx.scope,lineage=ctx.lineage,generation=ctx.generation,binding=b['binding'],authority_reference=c._wire(aid));w=body['native_definition']
        if k in ('authority','attestor'):
            ident=aid if k=='authority' else tid;w.update(id=c._wire(m.EntityId('TEST-I04-'+k)),identity=c._wire(ident),target=c._wire(src),scope=ctx.scope,lineage=ctx.lineage,generation=ctx.generation)
        else:w.update(id=c._wire(m.PredicateId('TEST-I04-'+k)),entity=c._wire(m.EntityId('TEST-I04-authority' if k=='authority_predicate' else 'TEST-I04-attestor')),expected=c._wire(src))
        md=copy.deepcopy(x['AUTHENTICATION_OBJECTS'][k]['descriptor']);md.update(scope=ctx.scope,lineage=ctx.lineage,generation=ctx.generation,subject=dict(s,kind='AUTHENTICATION_MEMBER_ROLE',object_id=w['id']['value']));md['currentness_rule']['consumer']=s['consumer']
        member=definition(md,body,k+'.json');v.update(content_id=c._wire(member.provenance.identity),definition_id=c._wire(member.id),source=member.provenance.path)
    o=b['operating_authority_requirement'];o.update(authority_identity=c._wire(aid),exact_members={k:v['definition_id'] for k,v in b['members'].items()},source=c._wire(src))
    auth=definition(d,b,'auth-set.json')
    idesc=copy.deepcopy(x['P04_mapping']['ingress']['descriptor']);idesc.update(scope=ctx.scope,lineage=ctx.lineage,generation=ctx.generation,subject=dict(s,kind='EVIDENCE_INGRESS_ROLE',authentication='TEST-I04-source_predicate'));idesc['currentness_rule']['consumer']=s['consumer']
    body=copy.deepcopy(x['P04_mapping']['ingress']['canonical_body']);body['contract'].update(gate=c._wire(g.id),requirements=c._wire((req.id,)),receipt_action=g.receipt_action,authentication=c._wire(m.PredicateId('TEST-I04-source_predicate')),scope=ctx.scope,lineage=ctx.lineage,generation=ctx.generation)
    ing=definition(idesc,body,'ingress.json');return auth,ing


class AuthenticationInstallationTests(unittest.TestCase):
    def setUp(self):
        h=unknown.ExternalUnknownTests();h.setUp();self.addCleanup(h.doCleanups);self.root=Path(h.temp.name);self.state=h.state
        b=h.bundle(h.state);self.bundle=c.record_result(b,m.ActionReevaluation((h.state.actions[0].id,),c.snapshot_id(h.state),h.state.actions[0].source))
        self.auth,self.ing=generic_definitions(self.state)
        self.decision=i.digest({'selection':'authorize generic authentication installation'},'test-human-decision');self.contract=c._identity(CONTRACT.read_bytes(),'raw-file-sha256')
        self.binding=operating(self.auth,self.decision,self.contract,'operating-receipt.json')
        self.r=request(self.bundle,self.auth,self.decision,self.contract,'install-auth-receipt.json',self.binding);self.store=self.root/'head'

    def commit(self,b=None,r=None,store=None):
        b=b or self.bundle;r=r or self.r
        return i.commit(b,r,store or self.store,self.root,expected_authority=r.authority.id,expected_decision=self.decision,expected_operating_authority=self.binding.operating_authorization_id)

    def installed(self):
        post,_,_=self.commit();r=request(post,self.ing,self.decision,self.contract,'install-ingress-receipt.json');end,bid,_=self.commit(post,r);return post,end,bid,r

    def candidate(self,b):
        s=b.current;gate=s.external_gates[0];req=s.evidence_requirements[0];contract=s.ingress_contracts[0];auth=i.descriptor(s.installed_definitions[0].request.definition)[1]
        claim=m.EvidenceClaim(req.id,m.ProofState.PROVED)
        producer=req.producers[0];target=req.target
        raw=c.canonical_bytes({'producer':c._wire(producer),'target':c._wire(target),'claims':[c._wire(claim)]});cid=c._identity(raw,'raw-file-sha256');prov=m.Provenance('incoming.json',cid,'/',raw.decode(),'PLANNER-EVIDENCE-ADMISSION-1',s.context.scope)
        entity=m.GraphEntity(ev.evidence_id(gate.id,cid,s.context),m.EntityKind.EVIDENCE,cid,prov,scope=s.context.scope,lineage=s.context.lineage,generation=s.context.generation,valid_until=100,produced=True)
        deps={contract.provenance,gate.provenance,req.provenance,gate.resolution_contracts[0].provenance,auth['attestor'].provenance}
        admission=m.ReceiptAdmission(entity.id,producer,target,(claim,),contract.authentication,prov,tuple(deps))
        # Match native command schema from prepared P04 precedent, replacing every binding.
        x=c._unwire(c.parse_json((ROOT/'docs/plans/qualification/INSTALLATION_I02_1/a09-post-install-candidate.json').read_bytes()))
        contract_json=c.canonical_bytes({'schema':'PLANNER-EVIDENCE-INGRESS-1','contract':{k:v for k,v in c._wire(contract).items() if k!='provenance'}}).decode()
        x=replace(x,expected_bundle=c.bundle_id(b),expected_snapshot=c.snapshot_id(s),expected_parent_event=b.events[-1].identity,contract_pin=contract.provenance.identity,gate=gate.id,receipt_action=gate.receipt_action,requirements=(req.id,),entity=entity,admission=admission,field_provenance=ev.field_bindings(entity,admission,contract),source_additions=(m.ArtifactPin(prov.path,prov.identity),))
        x=replace(x,command_key=ev.command_key(x))
        attest=ea.materialize(attestor_authority=auth['authority'].identity,attestor=auth['attestor'].identity,source_predicate=contract.authentication,source_pin=producer,native_entity=entity.id,semantic_evidence=i.digest({'fixture':'test-semantic'},'test-semantic-evidence'),content=i.digest({'content':'test'},'test-content'),proposition=req.proposition,gate=gate.id,scope=s.context.scope,lineage=s.context.lineage,provenance=cid)
        return x,attest

    def test_positive_atomic_frame_four_record_provenance(self):
        first,end,bid,r=self.installed();self.assertEqual(len(end.events),3)
        for f in fields(m.Snapshot):
            if f.name not in ('entities','predicates','installed_definitions','ingress_contracts'):self.assertEqual(getattr(end.current,f.name),getattr(self.bundle.current,f.name),f.name)
        self.assertEqual(len(first.current.entities)-len(self.state.entities),2);self.assertEqual(len(first.current.predicates)-len(self.state.predicates),2)
        self.assertFalse(first.current.ingress_contracts);self.assertEqual(len(end.current.ingress_contracts),1)
        x,t=self.candidate(end);self.assertEqual(len(x.admission.dependencies),4)
        before=c.snapshot_bytes(end.current);ev.apply(end.current,x,t);self.assertEqual(c.snapshot_bytes(end.current),before)
        self.assertFalse(end.current.receipt_admissions)

    def test_persistence_replay_temporal_identity_and_independent_reproduction(self):
        first,end,bid,r=self.installed();path=self.store/('bundle-'+bid.sha256+'.json')
        cold=c.restore(path,bid,self.root);self.assertEqual(c.bundle_bytes(cold),c.bundle_bytes(end));self.assertEqual(c.snapshot_id(c._replay(cold)),c.snapshot_id(end.current))
        self.assertEqual(c.bundle_bytes(c._prefix_bundle(end,1)),c.bundle_bytes(self.bundle));self.assertFalse(c._prefix_bundle(end,1).current.installed_definitions)
        self.assertFalse(c._prefix_bundle(end,2).current.ingress_contracts)
        for record in cold.current.installed_definitions:self.assertTrue(i.current(cold,record))
        again,_,_=self.commit(store=self.root/'second');other,otherid,_=self.commit(again,r,self.root/'second');self.assertEqual(otherid,bid)
        program='from pathlib import Path;from adapter.planner import codec as c,installation as i,model as m;import sys;b=c.restore(Path(sys.argv[1]),m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY,"planner-bundle-v1",sys.argv[2]),Path(sys.argv[3]));assert all(i.current(b,r) for r in b.current.installed_definitions);print(c.snapshot_id(c._replay(b)).sha256)'
        for seed in ('0','1','7','101'):
            out=subprocess.check_output([sys.executable,'-c',program,str(path),bid.sha256,str(self.root)],env=dict(os.environ,PYTHONHASHSEED=seed,PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(ROOT)),text=True);self.assertEqual(out.strip(),c.snapshot_id(end.current).sha256)

    def test_idempotence_conflict_and_stale_parent(self):
        first,end,bid,r=self.installed();retry,orig,noop=self.commit();self.assertTrue(noop);self.assertEqual(orig,c.bundle_id(first));self.assertEqual(c.bundle_id(retry),bid)
        x,t=self.candidate(end);old=replace(x,expected_snapshot=c.snapshot_id(first.current),expected_parent_event=first.events[-1].identity);old=replace(old,command_key=ev.command_key(old))
        with self.assertRaisesRegex(m.PlannerError,'PARENT_MISMATCH'):ev.apply(end.current,old,t)
        bad=replace(self.r,definition=replace(self.auth,provenance=replace(self.auth.provenance,excerpt='{}')));bad=replace(bad,command_key=i.command_key(bad))
        with self.assertRaises(m.PlannerError):self.commit(r=bad)

    def test_failure_injection_never_commits_partial_set(self):
        for suffix in ('HEAD.json','auth-set.json','attestor.json','operating-receipt.json'):
            store=self.root/('failure-'+suffix);real=os.replace
            for p in i.request_provenances(self.r):
                target=self.root/p.path
                if target.exists():target.unlink()
            def fail(src,dst):
                if str(dst).endswith('/'+suffix):raise OSError('injected publish failure')
                return real(src,dst)
            realwrite=c._write_immutable
            def failwrite(directory,name,raw):
                if name==suffix:raise OSError('injected immutable write failure')
                return realwrite(directory,name,raw)
            with patch('adapter.planner.codec.os.replace',side_effect=fail), patch('adapter.planner.codec._write_immutable',side_effect=failwrite):
                with self.assertRaises(OSError):self.commit(store=store)
            self.assertFalse((store/'HEAD.json').exists());self.assertEqual(c.bundle_id(c._read_head(store,self.bundle,self.root)),c.bundle_id(self.bundle))

    def test_closed_negative_definition_suite(self):
        mutations={
          'missing_attestor':lambda b:b['members'].pop('attestor'),
          'missing_predicate':lambda b:b['members'].pop('source_predicate'),
          'wrong_attestor':lambda b:b['members']['attestor']['body']['native_definition'].update(kind={'$enum':'EntityKind','value':'EVIDENCE'}),
          'wrong_predicate':lambda b:b['members']['source_predicate']['body']['native_definition'].update(entity=c._wire(m.EntityId('OTHER'))),
          'wrong_source':lambda b:b['binding'].update(source=c._wire(ZERO)),
          'wrong_consumer':lambda b:b['binding'].update(consumer='OTHER'),
          'wrong_authority':lambda b:b.update(authority_reference=c._wire(ZERO)),
          'wrong_scope':lambda b:b.update(scope='FOREIGN'),
          'wrong_lineage':lambda b:b.update(lineage='FOREIGN'),
          'wrong_generation':lambda b:b.update(generation='FOREIGN'),
          'metadata_wrapper':lambda b:b.update(metadata='qualification envelope'),
          'instance':lambda b:b.update(schema='EvidenceBoundAttestation')}
        for name,mutate in mutations.items():
            with self.subTest(name=name):
                d=c.parse_json(self.auth.descriptor_json.encode());body=c.parse_json(self.auth.provenance.excerpt.encode());mutate(body);bad=definition(d,body,'bad-'+name+'.json')
                with self.assertRaises(m.PlannerError):i.descriptor(bad)

    def test_wrong_authorities_and_foreign_prefix(self):
        bads=[replace(self.r,authority_bindings=()),replace(self.r,authority=replace(self.r.authority,authority_class=m.AuthorityClass.ATTEST)),replace(self.r,expected_parent_event=ZERO),replace(self.r,sequence=5),replace(self.r,operation=m.InstallationOperation.REPLACE),replace(self.r,authority_bindings=(replace(self.binding,declared_authority_reference=ZERO),))]
        for bad in bads:
            with self.subTest(bad=bad):
                bad=replace(bad,command_key=i.command_key(bad))
                with self.assertRaises(m.PlannerError):self.commit(r=bad)
        with self.assertRaisesRegex(m.PlannerError,'LIVE_TRUST_ANCHOR'):i.commit(self.bundle,self.r,self.store,self.root,expected_authority=self.r.authority.id,expected_decision=self.decision)

    def test_ingress_without_prerequisite_wrong_reference_and_instance(self):
        r=request(self.bundle,self.ing,self.decision,self.contract,'ingress-first.json')
        with self.assertRaisesRegex(m.PlannerError,'INGRESS_AUTHENTICATION_SET'):self.commit(r=r)
        first,end,_,_=self.installed()
        x,t=self.candidate(end)
        x=replace(x,expected_snapshot=c.snapshot_id(first.current),expected_parent_event=first.events[-1].identity,expected_bundle=c.bundle_id(first));x=replace(x,command_key=ev.command_key(x))
        with self.assertRaisesRegex(m.PlannerError,'INGRESS_NOT_INSTALLED'):ev.apply(first.current,x,t)
        for field,value in [('authentication',c._wire(m.PredicateId('OTHER'))),('scope','FOREIGN'),('generation','FOREIGN')]:
            d=c.parse_json(self.ing.descriptor_json.encode());body=c.parse_json(self.ing.provenance.excerpt.encode());body['contract'][field]=value
            with self.assertRaises(m.PlannerError):i.descriptor(definition(d,body,'bad-ingress.json'))
        d=c.parse_json(self.ing.descriptor_json.encode());d['definition_type']='EVIDENCE_BOUND_ATTESTATION'
        with self.assertRaises(m.PlannerError):i.descriptor(definition(d,{'schema':'EVIDENCE_BOUND_ATTESTATION'},'instance.json'))

    def test_exact_provenance_and_attestation_chain_negatives(self):
        _,end,_,_=self.installed();x,t=self.candidate(end)
        for deps in [x.admission.dependencies[:-1],x.admission.dependencies+(x.entity.provenance,),x.admission.dependencies+(x.admission.dependencies[0],)]:
            admission=replace(x.admission,dependencies=deps);bad=replace(x,admission=admission,field_provenance=ev.field_bindings(x.entity,admission,end.current.ingress_contracts[0]));bad=replace(bad,command_key=ev.command_key(bad))
            with self.assertRaisesRegex(m.PlannerError,'DEPENDENCY_PROVENANCE'):ev.apply(end.current,bad,t)
        for k,v in [('attestor',ZERO),('source_predicate',m.PredicateId('OTHER')),('attestor_authority',ZERO),('attestation_id',ZERO)]:
            with self.assertRaisesRegex(m.PlannerError,'EVIDENCE_ATTESTATION'):ev.apply(end.current,x,replace(t,**{k:v}))

    def test_invalidation_and_expiry_withdraw_currentness(self):
        _,end,_,_=self.installed()
        ids=i.support_ids(end.current.installed_definitions[0].request)
        for identity in (x for x in ids if x.kind is m.IdentityKind.CONTENT_IDENTITY):
            bad=c.record_result(end,m.SourceInvalidation((identity,),c.snapshot_id(end.current)))
            self.assertFalse(i.current(bad,bad.current.installed_definitions[0]));self.assertFalse(i.current(bad,bad.current.installed_definitions[1]))
        expired=replace(end,current=replace(end.current,context=replace(end.current.context,tick=101)))
        self.assertFalse(i.current(expired,expired.current.installed_definitions[0]))

    def test_correctly_hashed_members_still_require_native_semantics(self):
        def reseal_member(d,b,key):
            x=b['members'][key];v=x['body'];cid=c._identity(c.canonical_bytes(v),'raw-file-sha256')
            types={'authority':'ATTEST_AUTHORITY_REFERENCE','attestor':'ATTESTOR_DEFINITION','authority_predicate':'ATTEST_AUTHORITY_PREDICATE','source_predicate':'SOURCE_ATTESTOR_PREDICATE'}
            md=dict(d,definition_type=types[key],canonical_body_schema=v['schema'],content_id=i.simple(cid),subject=dict(d['subject'],kind='AUTHENTICATION_MEMBER_ROLE',object_id=v['native_definition']['id']['value']),canonical_source_reference={'kind':'IMMUTABLE_FILE','path':x['source'],'content_id':i.simple(cid)},source_pin={'path':x['source'],'profile':'raw-file-sha256','pointer':'','identity':i.simple(cid)},provenance={'path':x['source'],'content_id':i.simple(cid),'section':'/','method':'I03-PROSPECTIVE-DEFINITION-1','scope':d['scope']},currentness_rule=dict(d['currentness_rule'],rule_id='AUTHENTICATION_MEMBER_CURRENT_V1'))
            x['content_id']=c._wire(cid);x['definition_id']=c._wire(i.digest(md,'planner-installable-definition-v1'))
            b['operating_authority_requirement']['exact_members']={k:x['definition_id'] for k,x in b['members'].items()}
        cases=[('source_predicate','entity',c._wire(m.EntityId('FOREIGN_ATTESTOR')),'AUTHENTICATION_PREDICATE'),('source_predicate','expected',c._wire(ZERO),'AUTHENTICATION_PREDICATE'),('source_predicate','permission',c._wire(m.AuthorityClass.USE),'AUTHENTICATION_PREDICATE'),('authority_predicate','entity',c._wire(m.EntityId('FOREIGN_AUTHORITY')),'AUTHENTICATION_PREDICATE'),('attestor','target',c._wire(ZERO),'AUTHENTICATION_ENTITY'),('attestor','permissions',c._wire((m.AuthorityClass.USE,)),'AUTHENTICATION_ENTITY'),('attestor','kind',c._wire(m.EntityKind.EVIDENCE),'AUTHENTICATION_ENTITY')]
        for key,field,value,reason in cases:
            with self.subTest(member=key,field=field):
                d=c.parse_json(self.auth.descriptor_json.encode());b=c.parse_json(self.auth.provenance.excerpt.encode());b['members'][key]['body']['native_definition'][field]=value;reseal_member(d,b,key)
                bad=definition(d,b,'correctly-hashed-wrong-'+field+'.json')
                with self.assertRaisesRegex(m.PlannerError,reason):i.descriptor(bad)
