"""Synthetic-only authority and succession qualification; no host launch."""
import copy,json,os,subprocess,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from adapter.context_projection import canonical,digest,sha
from adapter.controller_authority_store import ControllerAuthorityStore,roots_for
from adapter.supervisor_succession import (sealed,equivalent,reconstruct,append_authorized,
    runtime_binding,SuccessionDenied,validate_instance,legacy_tuple)


def fixture_records(binding):
    records={}
    def put(v,identity=None):
        b=canonical(v).encode();key=identity or 'sha256:'+sha(b)
        records[key]={'bytes':b,'evidence':[]};return key
    def make(pid,ticks):
        proc={'pid':pid,'ppid':40,'boot_id':'00000000-0000-0000-0000-000000000001',
              'start_ticks':ticks,'parent_start_ticks':10,'pid_namespace_inode':99,'uid':1000,'gid':1000,'groups':[]}
        v={'schema':'SUPERVISOR-INSTANCE-1','process':proc,
          'executable':{'path':'/synthetic/python','sha256':'a'*64,'argv':'python -m supervisor'},
          'implementation':{'/synthetic/supervisor.py':'b'*64},
          'workspace':{'path':'/synthetic/workspace','device':1,'inode':2},
          'cgroup':{'path':'/synthetic/cgroup','unified':'0::/executor','memberships':'0::/executor','device':1,'inode':3},
          'socket':{'path':'/synthetic/socket','device':1,'inode':pid+100,'uid':1000,'gid':1000,'mode':0o600,
                    'listener_pid':pid,'listener_start_ticks':ticks,'listener_inode':pid+200},
          'protocol_configuration':{'protocol_version':1,'socket_path':'/synthetic/socket','cgroup_path':'/synthetic/cgroup','environment':{}},
          'runtime_binding':binding}
        host={'schema':'SUPERVISOR-HOST-LAUNCH-1','authority':'HOST_OPERATOR','authorized_launch':True,
              'runtime_binding':binding,'process':proc,'configuration':equivalent(v),
              'parent_start_identity':{'pid':40,'boot_id':proc['boot_id'],'start_ticks':10},
              'command_sha256':'c'*64,'operator_authorization_id':'SYNTHETIC-HOST-LAUNCH',
              'delegated_before_credentials_dropped':True,'runtime_uid':1000,'runtime_gid':1000}
        v['host_launch']=put(host);v=sealed('SupervisorInstance',v);put(v,v['id']);return v
    s1=make(51,100);s2=make(52,200)
    evidence={'schema':'SUPERVISOR-PREDECESSOR-EVIDENCE-1','instance_id':s1['id'],'runtime_binding':binding,
              'status':'UNAVAILABLE','authority':'HOST_OPERATOR','observation_id':'SYNTHETIC-ABSENCE',
              'observed_at':'2026-09-17T00:00:00Z','process_absent':True,'listener_absent':True,'outstanding_scopes_accounted':True}
    q={'schema':'SUPERVISOR-QUALIFICATION-1','instance_id':s2['id'],'runtime_binding':binding,
       'result':'PASS','configuration':equivalent(s2),'capture_sha256':'d'*64}
    body={'schema':'SUPERVISOR-SUCCESSION-1','sequence':1,'predecessor_event':None,
          'predecessor_instance':s1['id'],'predecessor_status':'UNAVAILABLE','predecessor_evidence':put(evidence),
          'successor_instance':s2['id'],'reason':'synthetic predecessor unavailable',
          'host_launch':s2['host_launch'],'qualification':put(q),'runtime_binding':binding}
    approval={'schema':'SUPERVISOR-SUCCESSION-AUTHORIZATION-1','authority':'Architect',
              'decision':'AUTHORIZE_SUPERVISOR_SUCCESSION','event_body_sha256':digest(body),'reason':body['reason']}
    aid=put(approval);row=sealed('SupervisorSuccession',{**body,'architect_authorization':aid})
    policy={'schema':'SUPERVISOR-SUCCESSION-POLICY-1','anchor_id':s1['id'],'runtime_binding':binding,
            'requirements':equivalent(s1),'authorized_succession_ids':[aid],
            'pinned_head':row['id'],'ledger_id':binding['authorization_id']+':supervisor-succession-events',
            'released_supervisor':legacy_tuple(s1)}
    return records,policy,row,s1,s2


class SuccessionTests(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory(prefix='supervisor-succession-synthetic-');self.root=Path(self.t.name)
        self.app={'authorization_id':'SYNTHETIC','OperationalContextId':'SYNTHETIC-CONTEXT',
            'continuation_chain_digest':'1'*64,'ReleaseBasisId':'SYNTHETIC-RELEASE','ReleaseDecisionId':'SYNTHETIC-DECISION'}
        self.records,self.policy,self.row,self.s1,self.s2=fixture_records(self.app)
        self.ledger=self.root/'succession.jsonl';self.ledger.touch(mode=0o600)
        self.ownership=self.root/'ownership.jsonl';self.ownership.touch(mode=0o600)
        self.stores=[];self.store=self.materialize();self.data=canonical(self.row).encode()+b'\n'
    def tearDown(self):
        for s in self.stores:s.close()
        self.t.cleanup()
    def materialize(self,records=None):
        s=ControllerAuthorityStore.materialize(self.root/('store-'+str(len(self.stores))),records or self.records,{},
            {'authority_source':{'path':'SYNTHETIC','sha256':'e'*64},'release_identities':self.app},self.app,[],
            {self.policy['ledger_id']:{'path':str(self.ledger),'mutation':'APPEND_ONLY','mechanism':'SupervisorSuccession.append_authorized'},
             self.app['authorization_id']+':ownership':{'path':str(self.ownership),'mutation':'TYPED_LIFECYCLE','mechanism':'InvocationOwnership'}})
        self.stores.append(s);return s
    def deny(self,row=None,policy=None,store=None,data=None):
        with self.assertRaises((SuccessionDenied,KeyError,ValueError,OSError)):
            reconstruct(store or self.store,policy or self.policy,data if data is not None else canonical(row or self.row).encode()+b'\n')
    def test_01_s1_validates_as_itself(self):
        self.assertEqual(reconstruct(self.store,{**self.policy,'pinned_head':None},b'')['instance'],self.s1)
    def test_02_missing_succession_blocks(self):self.deny(data=b'')
    def test_03_valid_succession_and_04_immutable_history(self):
        before=self.store.resolve(self.s1['id'])
        self.assertEqual(reconstruct(self.store,self.policy,self.data)['instance'],self.s2)
        self.assertEqual(before,self.store.resolve(self.s1['id']))
    def test_05_pid_reuse_distinct(self):
        v=copy.deepcopy(self.s1);v.pop('id');v['process']['start_ticks']+=1;v['socket']['listener_start_ticks']+=1
        self.assertNotEqual(sealed('SupervisorInstance',v)['id'],self.s1['id'])
        bad=dict(self.row,successor_instance=self.s1['id']);bad.pop('id');self.deny(sealed('SupervisorSuccession',bad))
    def mutate(self,change):
        records=copy.deepcopy(self.records);v=copy.deepcopy(self.s2);change(v)
        records[self.s2['id']]['bytes']=canonical(v).encode();self.deny(store=self.materialize(records))
    def test_06_wrong_implementation(self):self.mutate(lambda v:v['implementation'].update({'/synthetic/supervisor.py':'f'*64}))
    def test_07_wrong_uid_gid(self):
        for k in ('uid','gid'):
            with self.subTest(k=k):self.mutate(lambda v:v['process'].update({k:999}))
    def test_08_wrong_cgroup(self):self.mutate(lambda v:v['cgroup'].update(unified='0::/user.slice'))
    def test_09_wrong_workspace(self):self.mutate(lambda v:v['workspace'].update(inode=999))
    def test_10_wrong_socket(self):
        for k,v in [('path','/wrong'),('uid',0),('gid',0),('mode',0o666),('inode',999),('listener_inode',999),('listener_pid',999)]:
            with self.subTest(k=k):self.mutate(lambda x:x['socket'].update({k:v}))
    def test_11_missing_launch(self):
        records=copy.deepcopy(self.records);del records[self.s2['host_launch']];self.deny(store=self.materialize(records))
    def test_12_competing(self):
        v=dict(self.row);v.pop('id');v['reason']='competing';self.deny(data=self.data+canonical(sealed('SupervisorSuccession',v)).encode()+b'\n')
    def test_13_replay_non_effecting(self):
        initial={**self.policy,'pinned_head':None}
        self.assertTrue(append_authorized(self.store,initial,self.ledger,self.row));before=self.ledger.read_bytes()
        self.assertFalse(append_authorized(self.store,self.policy,self.ledger,self.row));self.assertEqual(before,self.ledger.read_bytes())
        self.assertEqual(reconstruct(self.store,self.policy,self.data+self.data)['sequence'],1)
        with self.assertRaises(SuccessionDenied):append_authorized(self.store,initial,self.ledger,self.row)
    def test_14_ancestry(self):
        for key,value in [('sequence',2),('predecessor_event','UNKNOWN'),('runtime_binding',{})]:
            bad=dict(self.row);bad.pop('id');bad[key]=value;self.deny(sealed('SupervisorSuccession',bad))
        self.deny(data=self.data[:-1]);self.deny(policy={**self.policy,'pinned_head':'UNKNOWN'})
    def test_15_fresh_process_recovery(self):
        self.ledger.write_bytes(self.data);p=self.root/'policy.json';p.write_text(canonical(self.policy))
        cmd=[sys.executable,'-B','-m','adapter.tests.test_supervisor_succession','--recover',str(self.store.root),self.store.catalog_sha256,canonical(self.app),str(p),str(self.ledger)]
        result=subprocess.run(cmd,check=True,capture_output=True,text=True)
        self.assertEqual(json.loads(result.stdout)['instance']['id'],self.s2['id'])
    def test_20_active_and_unapproved_denied(self):
        bad=dict(self.row);bad.pop('id');bad['predecessor_status']='ACTIVE';self.deny(sealed('SupervisorSuccession',bad))
        self.deny(policy={**self.policy,'authorized_succession_ids':[]})
    def test_executable_protocol_parent(self):
        self.mutate(lambda v:v['executable'].update(sha256='0'*64))
        self.mutate(lambda v:v['protocol_configuration'].update(protocol_version=2))
        self.mutate(lambda v:v['process'].update(parent_start_ticks=99))
    def test_resealed_configuration_denied(self):
        for key in ('implementation','workspace','cgroup','protocol_configuration'):
            records=copy.deepcopy(self.records);v=copy.deepcopy(self.s2);v.pop('id');v[key]['SUBSTITUTION']='bad'
            v=sealed('SupervisorInstance',v);records[v['id']]={'bytes':canonical(v).encode(),'evidence':[]}
            with self.assertRaises(SuccessionDenied):validate_instance(self.materialize(records),v['id'],self.policy)

    def test_succession_cannot_race_existing_invocation_fence(self):
        from adapter.activation_transaction import _lease
        from adapter.authorization_lifecycle import LifecycleDenied
        fence=_lease(self.ownership)
        try:
            with self.assertRaises(LifecycleDenied):
                append_authorized(self.store,{**self.policy,'pinned_head':None},self.ledger,self.row)
            self.assertEqual(self.ledger.read_bytes(),b'')
        finally:os.close(fence)

    def test_authenticated_competitor_rejected_by_append_CAS(self):
        v={k:x for k,x in self.row.items() if k not in ('id','architect_authorization')}
        v['reason']='second independently authorized proposal'
        approval={'schema':'SUPERVISOR-SUCCESSION-AUTHORIZATION-1','authority':'Architect',
            'decision':'AUTHORIZE_SUPERVISOR_SUCCESSION','event_body_sha256':digest(v),'reason':v['reason']}
        aid='sha256:'+sha(canonical(approval).encode())
        records=copy.deepcopy(self.records);records[aid]={'bytes':canonical(approval).encode(),'evidence':[]}
        store=self.materialize(records);other=sealed('SupervisorSuccession',{**v,'architect_authorization':aid})
        policy={**self.policy,'authorized_succession_ids':self.policy['authorized_succession_ids']+[aid],'pinned_head':None}
        self.assertTrue(append_authorized(store,policy,self.ledger,self.row))
        before=self.ledger.read_bytes()
        with self.assertRaises(SuccessionDenied):append_authorized(store,policy,self.ledger,other)
        self.assertEqual(before,self.ledger.read_bytes())

    def test_legacy_anchor_has_no_invented_birth_and_can_succeed(self):
        records=copy.deepcopy(self.records)
        anchor=sealed('SupervisorHistoricalInstance',{'schema':'SUPERVISOR-HISTORICAL-INSTANCE-1',
            'released_supervisor':legacy_tuple(self.s1),'released_profile_bytes_sha256':'0'*64,
            'missing_birth_evidence':['boot_id','start_ticks'],'source':'SYNTHETIC'})
        records[anchor['id']]={'bytes':canonical(anchor).encode(),'evidence':[]}
        evidence=json.loads(records[self.row['predecessor_evidence']]['bytes']);evidence['instance_id']=anchor['id']
        eid='sha256:'+sha(canonical(evidence).encode());records[eid]={'bytes':canonical(evidence).encode(),'evidence':[]}
        v={k:x for k,x in self.row.items() if k not in ('id','architect_authorization')}
        v.update(predecessor_instance=anchor['id'],predecessor_evidence=eid)
        approval={'schema':'SUPERVISOR-SUCCESSION-AUTHORIZATION-1','authority':'Architect',
            'decision':'AUTHORIZE_SUPERVISOR_SUCCESSION','event_body_sha256':digest(v),'reason':v['reason']}
        aid='sha256:'+sha(canonical(approval).encode());records[aid]={'bytes':canonical(approval).encode(),'evidence':[]}
        row=sealed('SupervisorSuccession',{**v,'architect_authorization':aid})
        policy={**self.policy,'anchor_id':anchor['id'],'pinned_head':row['id'],'authorized_succession_ids':[aid]}
        store=self.materialize(records)
        self.assertEqual(reconstruct(store,policy,canonical(row).encode()+b'\n')['instance'],self.s2)
        self.assertEqual(reconstruct(store,{**policy,'pinned_head':None},b'')['instance'],anchor)


class KernelObservationTests(unittest.TestCase):
    def test_process_birth_and_socket_observation_without_supervisor_launch(self):
        import socket
        from adapter.supervisor_observation import process,path_identity,socket_identity,observe
        with tempfile.TemporaryDirectory(prefix='observation-SYNTHETIC-') as td:
            listener=socket.socket(socket.AF_UNIX);path=Path(td)/'probe.sock'
            try:
                listener.bind(str(path));path.chmod(0o600);listener.listen(1)
                p=process(os.getpid());base=Path('/proc')/str(os.getpid())
                cg=path_identity(td);cg['memberships']=(base/'cgroup').read_text().strip()
                cg['unified']=next(x for x in cg['memberships'].splitlines() if x.startswith('0::'))
                environment={k.decode():v.decode() for k,v in (x.split(b'=',1) for x in (base/'environ').read_bytes().split(b'\0') if x)}
                v={'schema':'SUPERVISOR-INSTANCE-1','process':p,
                    'executable':{'path':str((base/'exe').resolve()),'sha256':sha((base/'exe').read_bytes()),
                        'argv':(base/'cmdline').read_bytes().rstrip(b'\0').replace(b'\0',b' ').decode()},
                    'implementation':{str(Path(__file__).resolve()):sha(Path(__file__).read_bytes())},
                    'workspace':path_identity(str(Path.cwd())), 'cgroup':cg,'socket':socket_identity(str(path),p),
                    'protocol_configuration':{'protocol_version':1,'socket_path':str(path),'cgroup_path':td,'environment':environment},
                    'host_launch':'SYNTHETIC-NOT-A-SUPERVISOR','runtime_binding':{'synthetic':True}}
                v=sealed('SupervisorInstance',v);self.assertEqual(observe(v),v)
                reused=copy.deepcopy(v);reused['process']['start_ticks']+=1
                self.assertNotEqual(observe(reused),reused)
                wrong=copy.deepcopy(v);wrong['protocol_configuration']['environment']['FORGED']='yes'
                with self.assertRaises(SuccessionDenied):observe(wrong)
                listener.close()
                with self.assertRaises(SuccessionDenied):observe(v)
            finally:listener.close()


class ProductionIntegrationTests(unittest.TestCase):
    def test_16_to_19_dispatch_activation_ownership_recovery_quiescence(self):
        from adapter.tests.qualify_activation_transaction import fixture
        from adapter.authority_bootstrap import capture_inputs,selection,reconstruct_authorization
        from adapter.activation_transaction import ActivationTransaction
        from adapter.authorization_lifecycle import dispatch_binding
        with tempfile.TemporaryDirectory(prefix='supervisor-integration-SYNTHETIC-') as td:
            out=Path(td);fake=fixture_records({'authorization_id':'SYNTHETIC'})[3]
            root,auth,audit,dispatch,projection=fixture(out/'fixture',supervisor_identity=legacy_tuple(fake))
            records=capture_inputs(auth,audit,dispatch);aliases,app,prov,private=selection(auth,audit,dispatch)
            op=json.loads(auth.operational_binding);profile=json.loads(Path(op['governance']['released_profile']['path']).read_bytes())
            added,policy,row,s1,s2=fixture_records(runtime_binding(auth,None,profile));records.update(added)
            records[auth.authorization_id+':supervisor-succession']={'bytes':canonical(policy).encode(),'evidence':[]}
            ledger=out/'succession.jsonl';ledger.write_text(canonical(row)+'\n');ledger.chmod(0o600)
            private[policy['ledger_id']]={'path':str(ledger),'mutation':'APPEND_ONLY','mechanism':'SupervisorSuccession.append_authorized'}
            store=ControllerAuthorityStore.materialize(out/'private',records,aliases,prov,app,roots_for(auth),private)
            did='E1-ARCHITECT-DISPATCH-sha256:'+dispatch['sha256']
            try:
                with store.session():
                    restored=reconstruct_authorization(store,auth.authorization_id);dispatch_binding(restored,audit,dispatch)
                    before=audit.read_bytes();ownership=Path(auth.ownership_ledger).read_bytes()
                    with patch('adapter.supervisor_observation.observe',side_effect=FileNotFoundError('synthetic unavailable')):
                        with self.assertRaises(FileNotFoundError):ActivationTransaction.activate(restored,audit,did)
                    self.assertEqual(before,audit.read_bytes());self.assertEqual(ownership,Path(auth.ownership_ledger).read_bytes())
                    for field,change in [('process',{'start_ticks':999}),('implementation',{'/synthetic/supervisor.py':'0'*64}),('socket',{'inode':999})]:
                        wrong=copy.deepcopy(s2);wrong[field].update(change)
                        with patch('adapter.supervisor_observation.observe',return_value=wrong):
                            with self.assertRaises(SuccessionDenied):ActivationTransaction.activate(restored,audit,did)
                    with patch('adapter.supervisor_observation.observe',return_value=s2),patch('adapter.activation_transaction._host',return_value={'synthetic_host':'PASS'}) as legacy:
                        tx=ActivationTransaction.activate(restored,audit,did)
                        try:self.assertTrue(tx.verify_handoff());self.assertIsNotNone(tx.reservation)
                        finally:tx.close()
                        tx=ActivationTransaction.recover(restored,audit,did)
                        try:self.assertTrue(tx.recovery['handoff_eligible'])
                        finally:tx.close()
                        self.assertTrue(legacy.called)
                    with patch('adapter.supervisor_observation.observe',return_value=s2),patch('adapter.activation_transaction._host',side_effect=RuntimeError('non-QUIESCENT scope')):
                        with self.assertRaises(RuntimeError):ActivationTransaction.recover(restored,audit,did)
            finally:store.close()

if __name__=='__main__':
    if '--recover' in sys.argv:
        _,_,root,h,app,p,ledger=sys.argv;store=ControllerAuthorityStore(root,h,json.loads(app))
        try:print(canonical(reconstruct(store,json.loads(Path(p).read_bytes()),Path(ledger).read_bytes())))
        finally:store.close()
    else:unittest.main()
