"""E2-T01 qualification only: no E2 Action execution or E1 writes."""
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest
from dataclasses import replace, fields, is_dataclass
from unittest.mock import patch
from adapter.planner import codec as c, model as m, core, gates, evidence
from adapter.tests import test_planner_external_unknown as unknown
from adapter.tests.test_planner_external_unknown import source


def setup_fixture(test, outcome=m.ProofState.PROVED, known=True, suffix=""):
    helper=unknown.ExternalUnknownTests();helper.setUp();test.addCleanup(helper.doCleanups)
    root=Path(helper.temp.name); state=helper.state
    if suffix:
        def rename(x):
            if isinstance(x,m.Identifier):return type(x)(x.value+suffix)
            if type(x) is tuple:return tuple(rename(v) for v in x)
            if is_dataclass(x):return replace(x,**{f.name:rename(getattr(x,f.name)) for f in fields(x)})
            return x
        state=rename(state)
        gate=state.external_gates[0]; route=gate.resolution_contracts[0]
        body=c._wire(route);del body['$type'];del body['provenance']
        route=replace(route,provenance=source(root/('resolution'+suffix+'.json'),{'schema':'EXTERNAL-RESOLUTION-CONTRACT-1','contract':body}))
        state=replace(state,external_gates=(replace(gate,resolution_contracts=(route,)),))
    ctx=state.context
    req=replace(state.evidence_requirements[0],rule_known=known)
    state=replace(state,evidence_requirements=(req,))
    raw=c.canonical_bytes({'producer':c._wire(req.producers[0]),'target':c._wire(req.target),
        'claims':[c._wire(m.EvidenceClaim(req.id,outcome))]})
    identity=c._identity(raw,'raw-file-sha256')
    trust_source=source(root/('trust'+suffix+'.json'),{'qualification_only':True,'producer':c._wire(req.producers[0]),'target':c._wire(identity)})
    trust=m.GraphEntity(m.EntityId('T01-ATTESTOR'+suffix),m.EntityKind.AUTHORITY,req.producers[0],trust_source,
        ctx.scope,ctx.lineage,ctx.generation,20,permissions=(m.AuthorityClass.ATTEST,),target=identity)
    auth=m.Predicate(m.PredicateId('T01-AUTH'+suffix),m.PredicateKind.AUTHORITY,entity=trust.id,expected=identity,permission=m.AuthorityClass.ATTEST)
    state=replace(state,entities=(trust,),predicates=state.predicates+(auth,))
    contract=m.EvidenceIngressContract('PLANNER-EVIDENCE-INGRESS-1',state.external_gates[0].id,
        state.external_gates[0].receipt_action,(req.id,),auth.id,state.external_gates[0].resolution_contracts[0].source_class,ctx.scope,ctx.lineage,ctx.generation,20,trust_source)
    body=c._wire(contract);del body['provenance']
    contract=replace(contract,provenance=source(root/('ingress'+suffix+'.json'),{'schema':'PLANNER-EVIDENCE-INGRESS-1','contract':body}))
    bundle=helper.bundle(state)
    bundle=replace(bundle,sources=bundle.sources+(m.ArtifactPin(trust_source.path,trust_source.identity),m.ArtifactPin(contract.provenance.path,contract.provenance.identity)))
    provenance=m.Provenance('incoming/'+identity.sha256+'.json',identity,'/',raw.decode(),'PLANNER-EVIDENCE-ADMISSION-1',ctx.scope)
    entity=m.GraphEntity(evidence.evidence_id(contract.gate,identity,ctx),m.EntityKind.EVIDENCE,identity,provenance,ctx.scope,ctx.lineage,ctx.generation,20)
    dependencies={contract.provenance,trust_source,req.provenance,state.external_gates[0].provenance}
    dependencies.update(x.provenance for x in state.external_gates[0].resolution_contracts)
    admission=m.ReceiptAdmission(entity.id,req.producers[0],req.target,(m.EvidenceClaim(req.id,outcome),),auth.id,provenance,
        tuple(sorted(dependencies,key=lambda x:x.path)))
    request=m.EvidenceSourceAdmission('PLANNER-EVIDENCE-ADMISSION-1',c.bundle_id(bundle),c.snapshot_id(state),None,
        c._identity(b'', 'planner-evidence-command-v1'),contract.gate,contract.receipt_action,(req.id,),contract.provenance.identity,
        (m.ArtifactPin(provenance.path,identity),),entity,admission,evidence.field_bindings(entity,admission,contract))
    request=replace(request,command_key=evidence.command_key(request))
    return root,bundle,request,raw


class AdmissionFixture(unittest.TestCase):
    def setUp(self):
        self.root,self.bundle,self.request,self.raw=setup_fixture(self)
        self.store=self.root/'store'

    def admit(self,request=None,bundle=None):
        return c.admit_external_evidence(bundle or self.bundle,request or self.request,
            {self.request.entity.provenance.path:self.raw},self.store,self.root)

    def event(self,bundle,stage):
        return m.ExternalEvent(self.request.gate,stage,c.snapshot_id(bundle.current))


class AdmissionTests(AdmissionFixture):
    def test_cold_live_receipt_cli_and_replay_once(self):
        path,identity=c.save_bundle(self.bundle,self.store,self.root)
        for name,body in [('identity',c._wire(identity)),('request',c._wire(self.request))]:
            (self.root/name).write_bytes(c.canonical_bytes(body))
        (self.root/'payload').write_bytes(self.raw)
        argv=[sys.executable,'-m','adapter.planner','admit-evidence',str(path),'--request',str(self.root/'request'),
            '--payload',str(self.root/'payload'),'--expected-identity',str(self.root/'identity'),
            '--source-root',str(self.root),'--out',str(self.store)]
        run=subprocess.run(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
        self.assertEqual(run.returncode,0,run.stderr)
        response=json.loads(run.stdout);newid=c._unwire(response['current'])
        after=c.restore(self.store/('bundle-'+newid.sha256+'.json'),newid,self.root)
        self.assertEqual(len(after.events),2);self.assertEqual(len(after.current.receipt_admissions),1)
        self.assertEqual(after.current.receipt_observations,())
        self.assertEqual(after.current.external_gates[0].stage,m.ExternalStage.EVIDENCE_RECEIVED)
        self.assertFalse(core.resume_eligibility(after,self.root).allowed)
        self.assertEqual(gates.obligation_proof(after.current,self.request.requirements[0]).state,m.ProofState.UNKNOWN)
        retry=subprocess.run(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
        self.assertEqual(retry.returncode,0,retry.stderr);self.assertTrue(json.loads(retry.stdout)['idempotent_noop'])

    def test_validation_and_reentry_separate(self):
        after,_,_=self.admit()
        validated,_=c.commit_event(after,self.event(after,m.ExternalStage.EVIDENCE_VALIDATED),self.store,self.root)
        self.assertEqual(validated.current.external_gates[0].stage,m.ExternalStage.EVIDENCE_VALIDATED)
        self.assertFalse(core.resume_eligibility(validated,self.root).allowed)
        entered,_=c.commit_event(validated,self.event(validated,m.ExternalStage.DEPENDENT_ACTION_REENTRY),self.store,self.root)
        self.assertTrue(core.resume_eligibility(entered,self.root).allowed)
        self.assertEqual(entered.current.knowledge,())
        self.assertEqual(entered.current.roots,self.bundle.current.roots)

    def test_negative_fields_never_commit(self):
        r=self.request
        changes=[dict(gate=m.GateId('WRONG')),dict(receipt_action='WRONG'),dict(requirements=()),
            dict(expected_snapshot=c._identity(b'wrong','planner-snapshot-v1')),dict(expected_bundle=c._identity(b'wrong','planner-bundle-v1')),
            dict(entity=replace(r.entity,lineage='WRONG')),dict(entity=replace(r.entity,valid_until=-1)),
            dict(entity=replace(r.entity,kind=m.EntityKind.AUTHORITY)),dict(field_provenance=()),
            dict(admission=replace(r.admission,producer=replace(r.admission.producer,kind=m.IdentityKind.CONTENT_IDENTITY))),
            dict(admission=replace(r.admission,target=replace(r.admission.target,sha256='f'*64))),
            dict(schema='UNKNOWN'),dict(entity=replace(r.entity,provenance=replace(r.entity.provenance,method='FAKE')))]
        for change in changes:
            bad=replace(r,**change);bad=replace(bad,command_key=evidence.command_key(bad))
            with self.subTest(change=change),self.assertRaises(m.PlannerError):self.admit(bad)
            self.assertFalse((self.store/'HEAD.json').exists())
            self.assertFalse((self.root/r.entity.provenance.path).exists())

    def test_idempotence_conflict_and_parent(self):
        after,identity,noop=self.admit();self.assertFalse(noop)
        repeated,original,noop=self.admit();self.assertTrue(noop);self.assertEqual(original,identity)
        with self.assertRaisesRegex(m.PlannerError,'IDEMPOTENCY_CONFLICT'):
            self.admit(replace(self.request,receipt_action='WRONG'))
        other=replace(self.request,receipt_action='WRONG');other=replace(other,command_key=evidence.command_key(other))
        with self.assertRaisesRegex(m.PlannerError,'PARENT_MISMATCH'):self.admit(other)
        self.assertEqual(len(repeated.events),2)

    def test_no_standalone_or_backdated_admission(self):
        with self.assertRaises(m.PlannerError):c.record_result(self.bundle,self.request)
        after,_,_=self.admit()
        with self.assertRaises(m.PlannerError):c.bundle_bytes(replace(after,events=after.events[:1]))
        with self.assertRaises(m.PlannerError):c.bundle_bytes(replace(after,initial=after.current))
        with self.assertRaises(m.PlannerError):c.bundle_bytes(replace(after,sources=self.bundle.sources))

    def test_invalidation_preserves_history_withdraws_support(self):
        for source in [self.request.contract_pin,self.bundle.current.external_gates[0].resolution_contracts[0].provenance.identity,
                       self.request.entity.identity,self.bundle.current.entities[0].provenance.identity]:
            # Separate stores; source files are immutable and may already exist.
            self.store=self.root/('store-'+source.sha256)
            after,_,_=self.admit()
            changed,_=c.commit_event(after,m.SourceInvalidation((source,),c.snapshot_id(after.current)),self.store,self.root)
            self.assertEqual(len(changed.events),3)
            self.assertFalse(core.resume_eligibility(changed,self.root).allowed)
            self.assertNotEqual(gates.check_receipt(changed.current,changed.current.external_gates[0],self.request.entity.id).state,m.ProofState.PROVED)
            # Historical receipt still replays, source validity is now stale.
            path,identity=c.save_bundle(changed,self.store,self.root)
            self.assertEqual(c.bundle_id(c.restore(path,identity,self.root)),identity)
            validate=self.event(changed,m.ExternalStage.EVIDENCE_VALIDATED)
            if changed.current.external_gates[0].validation is m.ValidationState.STALE:
                with self.assertRaises(m.PlannerError):c.commit_event(changed,validate,self.store,self.root)
            else:
                rejected,_=c.commit_event(changed,validate,self.store,self.root)
                self.assertEqual(rejected.current.external_gates[0].stage,m.ExternalStage.WAITING_FOR_EXTERNAL_EVIDENCE)
                self.assertFalse(rejected.current.receipt_observations[-1].accepted)
                self.assertFalse(core.resume_eligibility(rejected,self.root).allowed)

    def test_route_stale_before_admission(self):
        source=self.bundle.current.external_gates[0].resolution_contracts[0].provenance.identity
        stale=c.record_result(self.bundle,m.SourceInvalidation((source,),c.snapshot_id(self.bundle.current)))
        request=replace(self.request,expected_bundle=c.bundle_id(stale),expected_snapshot=c.snapshot_id(stale.current),expected_parent_event=stale.events[-1].identity)
        request=replace(request,command_key=evidence.command_key(request))
        with self.assertRaises(m.PlannerError):self.admit(request,stale)

    def test_unknown_and_negative_claim_never_positive(self):
        for known,outcome in [(False,m.ProofState.PROVED),(True,m.ProofState.DISPROVED)]:
            root,bundle,request,raw=setup_fixture(self,outcome,known)
            received,_,_=c.admit_external_evidence(bundle,request,{request.entity.provenance.path:raw},root/'store',root)
            event=m.ExternalEvent(request.gate,m.ExternalStage.EVIDENCE_VALIDATED,c.snapshot_id(received.current))
            validated,_=c.commit_event(received,event,root/'store',root)
            self.assertEqual(validated.current.external_gates[0].stage,m.ExternalStage.WAITING_FOR_EXTERNAL_EVIDENCE)
            self.assertFalse(core.resume_eligibility(validated,root).allowed)

    def test_payload_pin_and_deleted_source(self):
        with self.assertRaises(m.PlannerError):c.admit_external_evidence(self.bundle,self.request,{self.request.entity.provenance.path:b'wrong'},self.store,self.root)
        after,identity,_=self.admit()
        (self.root/self.request.entity.provenance.path).write_bytes(b'substitution')
        with self.assertRaises(m.PlannerError):c.restore(self.store/('bundle-'+identity.sha256+'.json'),identity,self.root)

    def test_crash_before_head_leaves_parent(self):
        oldpath,oldid=c.save_bundle(self.bundle,self.store,self.root)
        with patch('adapter.planner.codec.os.replace',side_effect=OSError('crash')):
            with self.assertRaises(OSError):self.admit()
        self.assertFalse((self.store/'HEAD.json').exists())
        self.assertEqual(c.bundle_id(c.restore(oldpath,oldid,self.root)),oldid)
        after,identity,noop=self.admit();self.assertFalse(noop)
        self.assertEqual(len(after.events),2)


class AdditionalAdmissionTests(AdmissionFixture):
    """Additional adversarial transaction tests."""
    def test_ingress_invalidated_before_receipt(self):
        stale=c.record_result(self.bundle,m.SourceInvalidation((self.request.contract_pin,),c.snapshot_id(self.bundle.current)))
        request=replace(self.request,expected_bundle=c.bundle_id(stale),expected_snapshot=c.snapshot_id(stale.current),expected_parent_event=stale.events[-1].identity)
        request=replace(request,command_key=evidence.command_key(request))
        with self.assertRaisesRegex(m.PlannerError,'ALREADY_INVALIDATED'):self.admit(request,stale)

    def test_conflicting_claims_are_not_overwritten(self):
        root,bundle,request,raw=setup_fixture(self,m.ProofState.DISPROVED)
        received,_,_=c.admit_external_evidence(bundle,request,{request.entity.provenance.path:raw},root/'store',root)
        validated=c.record_result(received,m.ExternalEvent(request.gate,m.ExternalStage.EVIDENCE_VALIDATED,c.snapshot_id(received.current)))
        self.assertEqual(validated.current.receipt_observations[0].claims[0].outcome,m.ProofState.DISPROVED)
        # Same evidence entity cannot be rewritten even after gate returns waiting.
        changed=replace(request,expected_bundle=c.bundle_id(validated),expected_snapshot=c.snapshot_id(validated.current),expected_parent_event=validated.events[-1].identity)
        changed=replace(changed,command_key=evidence.command_key(changed))
        with self.assertRaisesRegex(m.PlannerError,'IDENTITY_CONFLICT'):core.apply_event(validated.current,changed)

    def test_replay_receipt_not_live_event_and_stale_attestor(self):
        after,_,_=self.admit()
        with self.assertRaises(m.PlannerError):c.record_result(after,after.events[-1].result)
        # An old trusted source is withdrawn without changing the source bytes.
        stale=c.record_result(self.bundle,m.SourceInvalidation((self.bundle.current.entities[0].provenance.identity,),c.snapshot_id(self.bundle.current)))
        request=replace(self.request,expected_bundle=c.bundle_id(stale),expected_snapshot=c.snapshot_id(stale.current),expected_parent_event=stale.events[-1].identity)
        request=replace(request,command_key=evidence.command_key(request))
        with self.assertRaises(m.PlannerError):self.admit(request,stale)

    def test_hash_order_process_determinism(self):
        path,pin=c.save_bundle(self.bundle,self.root/'checkpoint',self.root)
        (self.root/'request').write_bytes(c.canonical_bytes(c._wire(self.request)))
        (self.root/'payload').write_bytes(self.raw)
        program='''import json,sys
from pathlib import Path
from adapter.planner import codec as c
p,root,pin,store=sys.argv[1:]
b=c.restore(p,c._unwire(json.loads(pin)),root)
r=c._unwire(c.parse_json((Path(root)/'request').read_bytes()))
a,i,n=c.admit_external_evidence(b,r,{r.entity.provenance.path:(Path(root)/'payload').read_bytes()},store,root)
for _ in range(3):
 a=c.restore(Path(store)/('bundle-'+i.sha256+'.json'),i,root)
print(i.sha256)
'''
        identities=[]
        for seed in ('0','1','7','101'):
            r=subprocess.run([sys.executable,'-c',program,str(path),str(self.root),json.dumps(c._wire(pin)),str(self.root/('seed-'+seed))],
                env=dict(os.environ,PYTHONHASHSEED=seed,PYTHONDONTWRITEBYTECODE='1'),stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
            self.assertEqual(r.returncode,0,r.stderr);identities.append(r.stdout.strip())
            reader="""import sys,json
from pathlib import Path
from adapter.planner import codec as c,model as m,core
store,root,digest=sys.argv[1:]
i=m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY,'planner-bundle-v1',digest)
b=c.restore(Path(store)/('bundle-'+digest+'.json'),i,root)
assert len(b.events)==2 and not b.current.receipt_observations
assert not core.resume_eligibility(b,root).allowed
print(c.bundle_id(b).sha256)
"""
            for _ in range(3):
                cold=subprocess.run([sys.executable,'-c',reader,str(self.root/('seed-'+seed)),str(self.root),identities[-1]],
                    env=dict(os.environ,PYTHONHASHSEED=seed,PYTHONDONTWRITEBYTECODE='1'),stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
                self.assertEqual(cold.returncode,0,cold.stderr);self.assertEqual(cold.stdout.strip(),identities[-1])
        self.assertEqual(len(set(identities)),1)
        reordered=replace(self.bundle,sources=tuple(reversed(self.bundle.sources)),current=replace(self.bundle.current,predicates=tuple(reversed(self.bundle.current.predicates))),initial=replace(self.bundle.initial,predicates=tuple(reversed(self.bundle.initial.predicates))))
        request=replace(self.request,field_provenance=tuple(reversed(self.request.field_provenance)),admission=replace(self.request.admission,dependencies=tuple(reversed(self.request.admission.dependencies))))
        self.assertEqual(evidence.command_key(request),self.request.command_key)
        a,i,n=c.admit_external_evidence(reordered,request,{request.entity.provenance.path:self.raw},self.root/'ordered',self.root)
        self.assertEqual(i.sha256,identities[0])

    def test_two_process_writers_one_semantic_receipt(self):
        path,pin=c.save_bundle(self.bundle,self.store,self.root)
        (self.root/'request').write_bytes(c.canonical_bytes(c._wire(self.request)))
        (self.root/'payload').write_bytes(self.raw)
        (self.root/'identity').write_bytes(c.canonical_bytes(c._wire(pin)))
        command=[sys.executable,'-m','adapter.planner','admit-evidence',str(path),'--request',str(self.root/'request'),'--payload',str(self.root/'payload'),
            '--expected-identity',str(self.root/'identity'),'--source-root',str(self.root),'--out',str(self.store)]
        children=[subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True) for _ in range(2)]
        outputs=[]
        for child in children:
            out,err=child.communicate();self.assertEqual(child.returncode,0,err);outputs.append(json.loads(out))
        self.assertEqual(sorted(x['idempotent_noop'] for x in outputs),[False,True])
        self.assertEqual(outputs[0]['transaction'],outputs[1]['transaction'])

    def test_process_crash_each_persistence_boundary(self):
        path,pin=c.save_bundle(self.bundle,self.root/'checkpoint',self.root)
        (self.root/'request').write_bytes(c.canonical_bytes(c._wire(self.request)))
        (self.root/'payload').write_bytes(self.raw)
        program='''import json,sys,os
from pathlib import Path
from adapter.planner import codec as c
p,root,pin,store,limit=sys.argv[1:]; limit=int(limit); count=[0]
b=c.restore(p,c._unwire(json.loads(pin)),root)
r=c._unwire(c.parse_json((Path(root)/'request').read_bytes()))
def wrap(fn):
 def hooked(*a,**k):
  v=fn(*a,**k); count[0]+=1
  if count[0]==limit: os._exit(91)
  return v
 return hooked
for name in ('fsync','link','replace'): setattr(c.os,name,wrap(getattr(c.os,name)))
c.admit_external_evidence(b,r,{r.entity.provenance.path:(Path(root)/'payload').read_bytes()},store,root)
print(count[0])
'''
        # First measure actual persistence boundaries, then terminate at each one.
        base=[sys.executable,'-c',program,str(path),str(self.root),json.dumps(c._wire(pin))]
        dry=subprocess.run(base+[str(self.root/'dry'),'0'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
        self.assertEqual(dry.returncode,0,dry.stderr)
        total=int(dry.stdout.strip());self.assertGreater(total,5)
        for index in range(1,total+1):
            fresh_root,fresh_bundle,fresh_request,fresh_raw=setup_fixture(self)
            fresh_path,fresh_pin=c.save_bundle(fresh_bundle,fresh_root/'checkpoint',fresh_root)
            (fresh_root/'request').write_bytes(c.canonical_bytes(c._wire(fresh_request)))
            (fresh_root/'payload').write_bytes(fresh_raw)
            store=fresh_root/'store'
            fresh_base=[sys.executable,'-c',program,str(fresh_path),str(fresh_root),json.dumps(c._wire(fresh_pin))]
            run=subprocess.run(fresh_base+[str(store),str(index)],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            self.assertIn(run.returncode,(0,91))
            current=c._read_head(store,fresh_bundle,fresh_root)
            self.assertIn(len(current.events),(0,2))
            self.assertEqual(current.current.receipt_observations,())
            self.assertFalse(core.resume_eligibility(current,fresh_root).allowed)

    def test_two_distinct_gates_serialize_against_new_parent(self):
        root2,bundle2,request2,raw2=setup_fixture(self,suffix='-SECOND')
        from shutil import copyfile
        for pin in bundle2.sources:
            target=self.root/pin.path;target.parent.mkdir(parents=True,exist_ok=True)
            if target.exists():self.assertEqual(target.read_bytes(),(root2/pin.path).read_bytes())
            else:copyfile(root2/pin.path,target)
        collections=('actions','statuses','roots','predicates','entities','evidence_requirements','external_gates','goals','boundaries')
        state=replace(self.bundle.current,**{name:getattr(self.bundle.current,name)+getattr(bundle2.current,name) for name in collections})
        bundle=replace(self.bundle,initial=state,current=state,sources=tuple(set(self.bundle.sources+bundle2.sources)))
        first=replace(self.request,expected_bundle=c.bundle_id(bundle),expected_snapshot=c.snapshot_id(state))
        first=replace(first,command_key=evidence.command_key(first))
        received,_,_=c.admit_external_evidence(bundle,first,{first.entity.provenance.path:self.raw},self.store,self.root)
        stale=replace(request2,expected_bundle=c.bundle_id(bundle),expected_snapshot=c.snapshot_id(state))
        stale=replace(stale,command_key=evidence.command_key(stale))
        with self.assertRaisesRegex(m.PlannerError,'PARENT_MISMATCH'):
            c.admit_external_evidence(bundle,stale,{stale.entity.provenance.path:raw2},self.store,self.root)
        second=replace(request2,expected_bundle=c.bundle_id(received),expected_snapshot=c.snapshot_id(received.current),expected_parent_event=received.events[-1].identity)
        second=replace(second,command_key=evidence.command_key(second))
        complete,identity,_=c.admit_external_evidence(received,second,{second.entity.provenance.path:raw2},self.store,self.root)
        self.assertEqual(len(complete.events),4)
        self.assertEqual(len(complete.current.receipt_admissions),2)
        self.assertEqual(complete.current.receipt_observations,())
        restored=c.restore(self.store/('bundle-'+identity.sha256+'.json'),identity,self.root)
        self.assertEqual(c.bundle_id(restored),identity)

    def test_head_audit_and_claim_conflict(self):
        received,_,_=self.admit()
        head=self.store/'HEAD.json';original=head.read_bytes();body=json.loads(original)
        body['previous']['sha256']='f'*64;head.write_bytes(c.canonical_bytes(body))
        with self.assertRaisesRegex(m.PlannerError,'HEAD_AUDIT_MISMATCH'):self.admit()
        head.write_bytes(original)
        # A historical accepted opposite claim is not overwritten even when its
        # old supporting proof is no longer current. This is a synthetic initial
        # history fixture, never an executed Action or a live state mutation.
        prior_entity=replace(self.request.entity,id=m.EntityId('HISTORICAL-EVIDENCE'),validation=m.ValidationState.STALE)
        prior_admission=replace(self.request.admission,artifact=prior_entity.id,
            claims=(m.EvidenceClaim(self.request.requirements[0],m.ProofState.DISPROVED),))
        observation=m.ReceiptObservation(self.request.gate,prior_entity.id,True,(),prior_admission.claims)
        history=replace(self.bundle.current,entities=self.bundle.current.entities+(prior_entity,),
            receipt_admissions=(prior_admission,),receipt_observations=(observation,))
        m.validate_model(history)
        request=replace(self.request,expected_snapshot=c.snapshot_id(history))
        request=replace(request,command_key=evidence.command_key(request))
        with self.assertRaisesRegex(m.PlannerError,'CLAIM_CONFLICT'):core.apply_event(history,request)

    def test_pinned_source_shaped_fixture(self):
        import tempfile
        fixture_path=Path(__file__).resolve().parents[2]/'docs/plans/DETERMINISTIC_PLANNER_V0_1_E2_T01_FIXTURE.json'
        fixture=json.loads(fixture_path.read_text())
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            for path,raw in fixture['pinned_source_bytes_utf8'].items():
                target=root/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(raw)
            bundle=c._unwire(fixture['initial_bundle']);request=c._unwire(fixture['request'])
            expected=fixture['independent_expectations']
            self.assertEqual(core.recompute(bundle.current).control.value,expected['initial_control'])
            path,identity=c.save_bundle(bundle,root/'store',root)
            cold=c.restore(path,identity,root)
            after,identity,noop=c.admit_external_evidence(cold,request,{request.entity.provenance.path:fixture['new_evidence_utf8'].encode()},root/'store',root)
            self.assertEqual(len(after.events)-len(cold.events),expected['events_added'])
            self.assertEqual(after.current.external_gates[0].stage.value,expected['received_stage'])
            self.assertEqual(len(after.current.receipt_observations),expected['accepted_observations_after_receipt'])
            self.assertEqual(gates.obligation_proof(after.current,request.requirements[0]).state.value,expected['obligation_after_receipt'])
            self.assertEqual(core.resume_eligibility(after,root).allowed,expected['resume_after_receipt'])

    def test_source_changed_during_commit_has_no_head(self):
        original=c._write_immutable
        def write(directory,name,raw):
            result=original(directory,name,raw)
            if name.startswith('event-'):
                (self.root/self.request.entity.provenance.path).write_bytes(b'changed during persistence')
            return result
        with patch('adapter.planner.codec._write_immutable',side_effect=write):
            with self.assertRaises(m.PlannerError):self.admit()
        self.assertFalse((self.store/'HEAD.json').exists())


if __name__=='__main__':unittest.main()
