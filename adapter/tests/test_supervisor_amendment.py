"""Synthetic decision-consumption probes; never launch a supervisor or E1."""
import json, tempfile, unittest, subprocess, sys
from pathlib import Path
from types import SimpleNamespace
from adapter.supervisor_amendment import decisions, seal, digest, readiness, verify_dispatch, host_event, authenticated_policy
from adapter.controller_authority_store import ControllerAuthorityStore, encoded, sha


def fixture():
    refs={};records={}
    def put(name,value):
        data=encoded(value);h=sha(data);records['sha256:'+h]={'bytes':data,'evidence':[]}
        refs[name]={'authority_id':'sha256:'+h,'sha256':h};return refs[name]
    parent={'ReleaseBasisId':'basis','ReleaseDecisionId':'decision','OperationalContextId':'parent','continuation_chain_digest':'chain'}
    invariants={'task':'SYNTHETIC','ModelPayloadDigest':'payload','transmission':'unchanged'}
    body={'classification':'MATERIAL_RELEASE_CHANGE','current_operational_ancestor':parent,
        'required_implementation_identity':'synthetic-implementation','historical_S1_evidence_identity':'synthetic-S1'}
    cid='PD06-SUPERVISOR-AUTHORITY-AMENDMENT-sha256:'+digest(body)
    orig={k:parent[k] for k in ('ReleaseBasisId','ReleaseDecisionId')}
    rid='E1-RELEASE-AUTHORITY-sha256:'+digest({**orig,'SupervisorAuthorityAmendmentId':cid})
    candidate=put('candidate',{'body':body,'amendment_candidate_identity':cid,'proposed_release_authority_identity':rid})
    source=put('source',{'authority':'Architect','channel':'user','decision':'AUTHORIZE_MATERIAL_RELEASE_AND_DISPATCH_AMENDMENT',
        'accepted':{'amendment_identity':cid,'candidate_file_sha256':candidate['sha256'],
                    'resulting_release_authority':rid,'succession_implementation':body['required_implementation_identity']},
        'authorize_dispatch_amendment_for':'synthetic-auth'})
    release=seal('PD06-SUPERVISOR-AMENDMENT-DECISION',{'schema':'PD06-SUPERVISOR-AMENDMENT-DECISION-1','authority':'Architect',
        'decision':'AUTHORIZE_MATERIAL_SUPERVISOR_AMENDMENT','candidate':candidate,'amendment_identity':cid,
        'resulting_release_authority':rid,'original_release':orig,'authority_source':source,
        'successor_instance_id':None,'succession_authorization':None,'host_authorization':None})
    release_ref=put('release',release)
    old=put('original',{'authority':'Architect','decision':'DISPATCH_AUTHORIZED','invocation_identity':{'authorization_id':'synthetic-auth'},'authority_source':source})
    d={'schema':'ARCHITECT-DISPATCH-AMENDMENT-1','authority':'Architect','decision':'AMEND_SUPERVISOR_READINESS_ONLY',
        'authority_source':source,'release_amendment_decision':release['id'],'original_release':orig,
        'resulting_release_authority':rid,'amendment_identity':cid,'historical_S1':'synthetic-S1',
        'succession_implementation':'synthetic-implementation','predecessor_operational_ancestry':parent,
        'authorization_id':'synthetic-auth','unchanged_authorities':invariants,'changed_condition':'supervisor_readiness_only',
        'successor_instance_id':None,'succession_authorization':None,'all_other_original_conditions_unchanged':True,
        'original_dispatch':old,'original_dispatch_identity':'E1-ARCHITECT-DISPATCH-sha256:'+old['sha256']}
    dr=put('dispatch',seal('ARCHITECT-DISPATCH-AMENDMENT',d))
    selected={'release_decision':release_ref,'dispatch_amendment':dr,'implementation_qualification':put('q',{})}
    spec={'schema':3,'predecessor':{'schema':2,'identities':parent},'authority_invariants':invariants,'material_release':selected}
    return records,refs,spec,put


class AmendmentTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='synthetic-amendment-');self.root=Path(self.tmp.name)
        self.records,self.refs,self.spec,self.put=fixture();self.counter=0
    def tearDown(self):self.tmp.cleanup()
    def store(self):
        self.counter+=1
        self.records['synthetic-auth:supervisor-authority-amendment']={'bytes':encoded(self.spec['material_release']),'evidence':[]}
        return ControllerAuthorityStore.materialize(self.root/str(self.counter),self.records,{},
            {'authority_source':self.refs['source'],'release_identities':{'ReleaseBasisId':'basis','ReleaseDecisionId':'decision'}},
            {'authorization_id':'synthetic-auth'},[],getattr(self,'private_state',{}))
    def check(self):
        s=self.store()
        try:
            with s.session():return decisions(self.spec)
        finally:s.close()
    def change(self,name,key,value,reseal=False):
        obj=json.loads(self.records[self.refs[name]['authority_id']]['bytes']);obj[key]=value
        if reseal:obj=seal('PD06-SUPERVISOR-AMENDMENT-DECISION' if name=='release' else 'ARCHITECT-DISPATCH-AMENDMENT',{k:v for k,v in obj.items() if k!='id'})
        r=self.put(name,obj)
        self.spec['material_release']['release_decision' if name=='release' else 'dispatch_amendment']=r
    def test_original_release_keeps_S1(self):
        auth=SimpleNamespace(authorization_id='synthetic-auth',operational_binding=json.dumps({'governance':{'schema':2}}),context_binding=SimpleNamespace(governance=None))
        calls=[]
        s=self.store()
        try:
            self.assertEqual(readiness(auth,s,{'pid':57950},True,lambda x,**kw:calls.append(x) or x),{'pid':57950})
            self.assertEqual(calls,[{'pid':57950}])
        finally:s.close()
    def test_valid_release_and_dispatch(self):
        r,d,c=self.check();self.assertEqual(r['amendment_identity'],c['amendment_candidate_identity'])
    def test_missing_material_amendment(self):
        del self.records[self.refs['release']['authority_id']]
        with self.assertRaises(ValueError):self.check()
    def test_invalid_material_amendment(self):
        self.change('release','decision','CALLER_ASSERTED',True)
        with self.assertRaises(ValueError):self.check()
    def test_wrong_release_authority(self):
        self.change('release','resulting_release_authority','wrong',True)
        with self.assertRaises(ValueError):self.check()
    def test_original_dispatch_cannot_cross_alone(self):
        self.spec['material_release']['dispatch_amendment']=self.refs['original']
        with self.assertRaises((ValueError,KeyError)):self.check()
    def test_missing_dispatch_amendment(self):
        del self.records[self.refs['dispatch']['authority_id']]
        with self.assertRaises(ValueError):self.check()
    def test_wrong_dispatch_scope(self):
        self.change('dispatch','unchanged_authorities',{'task':'OTHER'},True)
        with self.assertRaises(ValueError):self.check()
    def test_no_amendment_self_authorizes_S2(self):
        for name in ('release','dispatch'):
            saved=(dict(self.records),json.loads(encoded(self.spec)),dict(self.refs))
            self.change(name,'successor_instance_id','unobserved-S2',True)
            with self.assertRaises(ValueError):self.check()
            self.records.clear();self.records.update(saved[0]);self.spec=saved[1];self.refs.clear();self.refs.update(saved[2])
    def test_valid_amendment_without_specific_succession_blocks(self):
        s=self.store();g=SimpleNamespace(spec=self.spec,verify=lambda:decisions(self.spec))
        a=SimpleNamespace(authorization_id='synthetic-auth',operational_binding=json.dumps({'governance':{'schema':3}}),context_binding=SimpleNamespace(governance=g))
        try:
            with s.session(),self.assertRaises(ValueError):readiness(a,s,{},True,lambda *a,**kw:self.fail('legacy fallback'))
        finally:s.close()
    def test_host_receipt_requires_separate_host_grant(self):
        s=self.store()
        try:
            with self.assertRaises(ValueError):host_event(s,{'predecessor_status':'UNAVAILABLE','architect_authorization':'missing-specific-approval'})
        finally:s.close()
    def test_separate_attributable_host_authorization(self):
        self.spec['material_release']['implementation_qualification']=self.put('q',{'implementation':{'current':{'source':'qualified'}}})
        release,dispatch,candidate=self.check()
        runtime={'context':'synthetic'}
        hostsource=self.put('hostsource',{'operator':'Jerry','channel':'user','authorization_id':'SYNTHETIC-HOST-CONSENT'})['authority_id']
        grant={'authority':'HOST_OPERATOR','decision':'AUTHORIZE_HOST_SUPERVISOR_LAUNCH','operator':'Jerry',
            'authorization_id':'SYNTHETIC-HOST-CONSENT','authority_source':hostsource,'runtime_binding':runtime,
            'predecessor_id':'synthetic-S1','launch_spec_sha256':'plan','launcher_sha256':'launcher'}
        grantref=self.put('hostgrant',grant)['authority_id']
        approval=self.put('specific',{'host_authorization':grantref,'predecessor_instance':'synthetic-S1',
            'launch_spec_sha256':'plan','launcher_sha256':'launcher'})['authority_id']
        ledger=self.root/'journal';ledger.write_bytes(b'');ledger.chmod(0o600)
        self.private_state={'synthetic-journal':{'path':str(ledger),'mutation':'APPEND_ONLY','mechanism':'SupervisorSuccession'}}
        policy={'anchor_id':'synthetic-S1','release_authority':release['resulting_release_authority'],
            'dispatch_amendment':dispatch['id'],'requirements':{'implementation':{'source':'qualified'}},
            'authorized_succession_ids':[approval],'runtime_binding':runtime,'ledger_id':'synthetic-journal'}
        self.records['synthetic-auth:supervisor-succession']={'bytes':encoded(policy),'evidence':[]}
        g=SimpleNamespace(spec=self.spec,verify=lambda:decisions(self.spec))
        auth=SimpleNamespace(authorization_id='synthetic-auth',context_binding=SimpleNamespace(governance=g))
        store=self.store()
        try:
            with store.session():self.assertEqual(authenticated_policy(auth,store),policy)
        finally:store.close()
        for field in ('authority','operator','authorization_id'):
            saved=self.records[grantref]
            changed={**grant,field:'UNAUTHORIZED'}
            # An object substitution must fail even when syntactically complete.
            self.records[grantref]={'bytes':encoded(changed),'evidence':[]}
            with self.assertRaises(ValueError):
                store=self.store()
                try:
                    with store.session():authenticated_policy(auth,store)
                finally:store.close()
            self.records[grantref]=saved

    def test_append_only_consumption_correction_ancestry(self):
        release,dispatch,candidate=self.check()
        previous={**self.spec['predecessor']['identities'],'OperationalContextId':'previous-material-context','continuation_chain_digest':'previous-material-chain'}
        prior={'event':'material_supervisor_authority_amendment_published','amendment_identity':release['amendment_identity'],
            'resulting_release_authority':release['resulting_release_authority'],'dispatch_amendment':dispatch['id'],
            'material_application':{'predecessor':self.spec['predecessor']['identities'],'identities':previous},
            'architect_authority':json.loads(self.records[self.refs['source']['authority_id']]['bytes'])}
        self.spec['material_release']['prior_publication']=self.put('prior',prior)
        self.spec['material_release']['application_predecessor']=previous
        self.check()
        self.spec['material_release']['application_predecessor']['continuation_chain_digest']='reordered'
        with self.assertRaises(ValueError):self.check()

    def test_host_receipt_exact_spec_and_launcher(self):
        grant={'authorization_id':'SYNTHETIC-CONSENT','launch_spec_sha256':'exact-spec','launcher_sha256':'exact-launcher'}
        gr=self.put('grant',grant)['authority_id']
        approval={'host_authorization':gr,'predecessor_instance':'synthetic-S1',
            'launch_spec_sha256':'exact-spec','launcher_sha256':'exact-launcher'}
        ap=self.put('specific',approval)['authority_id']
        receipt={'operator_authorization_id':'SYNTHETIC-CONSENT','launch_spec_sha256':'exact-spec','launcher_sha256':'exact-launcher'}
        hr=self.put('receipt',receipt)['authority_id']
        row={'predecessor_status':'UNAVAILABLE','architect_authorization':ap,'host_launch':hr,'predecessor_instance':'synthetic-S1'}
        store=self.store()
        try:host_event(store,row)
        finally:store.close()
        for field in ('operator_authorization_id','launch_spec_sha256','launcher_sha256'):
            hr=self.put('receipt',dict(receipt,**{field:'wrong'}))['authority_id']
            row['host_launch']=hr;store=self.store()
            try:
                with self.assertRaises(ValueError):host_event(store,row)
            finally:store.close()

    def test_substitution_replay_and_reordering(self):
        with self.subTest('substitution'):
            s=self.store();p=s.location(self.refs['dispatch']['authority_id']);p.write_bytes(b'{}')
            try:
                with s.session(),self.assertRaises(ValueError):decisions(self.spec)
            finally:s.close()
        with self.subTest('replay'):
            self.spec['material_release']['replayed_decision']=self.refs['release']
            with self.assertRaises(ValueError):self.check()
            del self.spec['material_release']['replayed_decision']
        with self.subTest('reordering'):
            self.spec['predecessor']['identities']['OperationalContextId']='different-head'
            with self.assertRaises(ValueError):self.check()
    def test_independent_restart_reconstructs_decisions(self):
        s=self.store();p=self.root/'spec.json';p.write_bytes(encoded(self.spec))
        try:
            args=[sys.executable,'-m','adapter.tests.test_supervisor_amendment','--recover',str(s.root),s.catalog_sha256,str(p)]
            result=subprocess.run(args,capture_output=True,text=True,check=True)
            self.assertEqual(json.loads(result.stdout),[r['id'] for r in self.check()[:2]])
        finally:s.close()
    def test_wrong_original_dispatch_does_not_inherit(self):
        s=self.store()
        try:
            with s.session(),self.assertRaises(ValueError):verify_dispatch(SimpleNamespace(spec=self.spec),{'decision':'different'})
        finally:s.close()

if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='--recover':
        s=ControllerAuthorityStore(sys.argv[2],sys.argv[3],{'authorization_id':'synthetic-auth'})
        try:
            with s.session():print(json.dumps([x['id'] for x in decisions(json.loads(Path(sys.argv[4]).read_bytes()))[:2]]))
        finally:s.close()
    else:unittest.main()
