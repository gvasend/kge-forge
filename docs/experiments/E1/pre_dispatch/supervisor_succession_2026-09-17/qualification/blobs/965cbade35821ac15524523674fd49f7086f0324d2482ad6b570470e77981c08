"""G5 fixtures qualify adapter authority, never the E1 implementation."""
from dataclasses import replace
import hashlib, json, os, subprocess, tempfile, threading, time, unittest
from pathlib import Path
from unittest.mock import patch
from adapter.committed_objects import read_blob, ObjectDenied
from adapter.context_binding import CommittedContext
from adapter.governed_host import GovernedHost
from adapter.orchestrator import ReasoningOrchestrator
from adapter.responses_orchestrator import ResponsesReasoning
from adapter.runnable_profile import authorization, specification, validate, ARGV, INPUTS, ENV

ROOT=Path(__file__).resolve().parents[2]
CAPTURE='5871bdce4f5b6539c84f69f4f2b2f94ee31be5cd'
PAYLOAD=r'''
import hashlib,json,os,pathlib,socket,subprocess,time,unittest
from kge_forge.context.probe import SYNTHETIC_ONLY

class AuthorityFixture(unittest.TestCase):
    def test_authority_only(self):
        self.assertTrue(SYNTHETIC_ONLY)
        self.assertEqual(os.getcwd(),'/scope')
        expected={'PATH':'/usr/bin:/bin','LANG':'C.UTF-8','PYTHONPATH':'/scope/src','TMPDIR':'/scope/.scratch'}
        actual=dict(os.environ)
        if 'PWD' in actual: self.assertEqual(actual.pop('PWD'),'/scope')
        self.assertEqual(actual,expected)
        base=pathlib.Path('/scope/.gei-context')
        info=json.loads((base/'INDEX.json').read_text())
        paths={m['source'].split('/')[-1]:m['destination'] for m in info['repository_mounts']}
        verified=[]
        for item in info['sources']:
            target=pathlib.Path(paths[item['repository']])/item['path']
            data=target.read_bytes()
            self.assertEqual(hashlib.sha256(data).hexdigest(),item['sha256'])
            env={'PATH':'/usr/bin:/bin','LANG':'C.UTF-8','GIT_CONFIG_NOSYSTEM':'1',
                 'GIT_CONFIG_GLOBAL':'/dev/null','GIT_OPTIONAL_LOCKS':'0'}
            blob=subprocess.check_output(['/usr/bin/git','-C',paths[item['repository']],
                'cat-file','blob',item['revision']+':'+item['path']],env=env)
            self.assertEqual(blob,data)
            with self.assertRaises(OSError): target.write_bytes(b'MUST_NOT_WRITE')
            verified.append(item['id'])
        for alias,path in paths.items():
            self.assertEqual((pathlib.Path(path)/'.git/config').read_text(),
                             '[core]\nrepositoryformatversion = 0\nbare = false\n')
            self.assertFalse((pathlib.Path(path)/'.git/hooks').exists())
        with self.assertRaises(OSError): (base/'INDEX.json').write_text('MUST_NOT_WRITE')
        s=socket.socket(); s.settimeout(.2)
        try:
            with self.assertRaises(OSError): s.connect(('1.1.1.1',80))
        finally: s.close()
        pathlib.Path('/scope/.scratch/probe.txt').write_text('SYNTHETIC_SNAPSHOT_ONLY')
        evidence={'fixture':'G5_NON_IMPLEMENTATION','verified_sources':verified,
            'environment':actual,'cwd':os.getcwd(),'network':'DENIED','baseline_mounts':'READ_ONLY'}
        pathlib.Path('/scope/.scratch/qualification.json').write_text(json.dumps(evidence))
        time.sleep(2)
'''

def git(root,*args):
    return subprocess.check_output(['/usr/bin/git','-C',str(root),'-c','core.hooksPath=/dev/null',
        '-c','user.name=G5 Scratch','-c','user.email=scratch@example.invalid',*args],
        stderr=subprocess.DEVNULL,text=True).strip()

def fixture(synthetic_acceptance=False):
    base=Path(tempfile.mkdtemp(prefix='g5-nonimplementation-'))
    root=base/'forge'; service=base/'service'; root.mkdir(); service.mkdir()
    for repo in (root,service): git(repo,'init','-q')
    (service/'service.txt').write_text('synthetic service')
    git(service,'add','.'); git(service,'commit','-qm','synthetic service')
    for rel,data in [('src/kge_forge/__init__.py','# synthetic only\n'),
        ('src/kge_forge/context/probe.py','SYNTHETIC_ONLY = True\n'),
        ('tests/context/test_fixture.py',PAYLOAD),('package.txt','DECIDED G5 qualification only\n')]:
        p=root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(data)
    manifest={'schema_version':'E1-CONTEXT-1','baseline_id':'G5-SYNTHETIC',
        'work_id':'G5-NON-IMPLEMENTATION','status':'DIAGNOSTIC_AUTHORIZED',
        'repositories':{'forge':{'root':str(root)},'service':{'root':str(service),
            'working_revision':git(service,'rev-parse','HEAD')}},
        'sources':[{'id':'package','repository':'forge','path':'package.txt',
            'sha256':hashlib.sha256((root/'package.txt').read_bytes()).hexdigest(),
            'revision_binding':'package_capture_commit','knowledge_status':'DECIDED','dependencies':[]}],
        'mandatory_roots':['package'],'scope':{'read_roots':[str(root),str(service)],
            'writable_paths':['src/kge_forge/__init__.py','src/kge_forge/context/',
                              'tests/context/','docs/implementation/E1-WP-001.md'],
            'protected_paths':['package.txt'],'task_tool_network':'DENIED','unrelated_connectors':'DENIED'},
        'prerequisites':[]}
    (root/'CONTEXT_MANIFEST.json').write_text(json.dumps(manifest))
    git(root,'add','.');git(root,'commit','-qm','G5 non-implementation capture')
    binding=CommittedContext(root/'CONTEXT_MANIFEST.json',git(root,'rev-parse','HEAD'))
    acceptance=binding if synthetic_acceptance else CommittedContext(ROOT/'docs/experiments/E1/pre_dispatch/CONTEXT_MANIFEST.json',CAPTURE)
    return root,binding,acceptance

def dispatch(runner,rid,root,**overrides):
    fields={'executable':ARGV[0],'argv':list(ARGV[1:]),'cwd':str(root),'inputs':list(INPUTS)}
    fields.update(overrides)
    return runner._dispatch({'name':'governed_exec','call_id':rid,'arguments':json.dumps(fields)})

def live(evidence):
    evidence=Path(evidence);evidence.mkdir(parents=True,exist_ok=True)
    root,binding,acceptance=fixture()
    auth=authorization(binding,acceptance,'auth-g5-live',3,'session-g5-live','turn-g5-live',True)
    auth=replace(auth,ownership_ledger=str(evidence/'ownership.jsonl'))
    host=GovernedHost(auth,evidence/'controller.jsonl')
    runner=ResponsesReasoning(ReasoningOrchestrator(host))
    negatives={}
    for rid,kw in [('wrong-executable',{'executable':'python3'}),
        ('wrong-argv',{'argv':['-c','print(1)']}),
        ('wrong-cwd',{'cwd':str(root/'tests')}),
        ('wrong-inputs',{'inputs':['package.txt']}),
        ('extra-input',{'inputs':list(INPUTS)+['package.txt']})]:
        negatives[rid]=dispatch(runner,rid,root,**kw)
        assert negatives[rid]['result']=='DENIED' and host.scope is None
    results=[]
    thread=threading.Thread(target=lambda:results.append(dispatch(runner,'first',root)))
    thread.start(); deadline=time.monotonic()+25
    while time.monotonic()<deadline and thread.is_alive():
        if host.scope and host.scope.state=='CLOSED': break
        time.sleep(.01)
    population=None; sequential=None
    if thread.is_alive() and host.scope and host.scope.state=='CLOSED':
        from adapter.recovery_ledger import _observe, CGROUP_BASE
        population=_observe(CGROUP_BASE/host.scope.id)
        sequential=dispatch(runner,'while-active',root)
    thread.join(30)
    report={'fixture_root':str(root),'fixture_capture':binding.capture_commit,
        'specification':json.loads(auth.execution_profile),'negative_results':negatives,
        'first':results,'population_during_result':population,'sequential_blocked':sequential,
        'thread_alive':thread.is_alive(),'status':host.status()}
    (evidence/'LIVE_REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
    assert not thread.is_alive() and results and results[0]['result']=='SUCCEEDED',report
    report['first_payload_evidence']=json.loads((host.scope.root/'.scratch/qualification.json').read_text())
    receipt=json.loads(results[0]['data']['result'])
    assert receipt['kind']=='governed_launch_receipt'
    assert receipt['runtime_policy_sha256']==host.scope.snapshot['runtime_policy_sha256']
    assert population['populated']==1 and population['members']
    assert sequential['result']=='DENIED'
    report['governed_fixture_update']=runner._dispatch({'name':'governed_write',
        'call_id':'fixture-source-update','arguments':json.dumps({'repository':str(root),
            'path':'src/kge_forge/context/probe.py',
            'content':'SYNTHETIC_ONLY = True\n# governed fixture update, not E1 implementation\n'})})
    assert report['governed_fixture_update']['result']=='SUCCEEDED'
    report['second']=dispatch(runner,'second',root)
    assert report['second']['result']=='SUCCEEDED'
    report['second_payload_evidence']=json.loads((host.scope.root/'.scratch/qualification.json').read_text())
    report['second_source_provenance']=host.scope.snapshot['files']['src/kge_forge/context/probe.py']['authority_provenance']
    assert report['second_source_provenance']['kind']=='governed_action'
    assert report['second_source_provenance']['action_request_id']=='fixture-source-update'
    assert report['second']['data']['scope_id']!=results[0]['data']['scope_id']
    assert host.ownership.active() is None
    events=[json.loads(line) for line in host.audit.read_text().splitlines()]
    for rid in ('first','second'):
        ordered=[next(i for i,e in enumerate(events) if e.get('event')==name and
            e.get('action_request_id')==rid) for name in ('action_request',
            'execution_snapshot_created','execution_scope_created','execution_result_available',
            'execution_scope_closed','execution_scope_quiescent','action_result')]
        assert ordered==sorted(ordered)
    report['result']='PASS';report['ownership_after']=None
    report['acceptance_binding_valid_after']=acceptance.verify()
    (evidence/'LIVE_REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
    return report

class RunnableProfileTests(unittest.TestCase):
    def test_exact_profile_and_changed_identity(self):
        root,binding,acceptance=fixture(synthetic_acceptance=True);spec=specification(binding,acceptance)
        validate(spec,ARGV,str(root),list(INPUTS))
        for change in ({'cwd':str(root/'tests')},{'environment':dict(ENV,PYTHONPATH='/tmp')},
                       {'inputs':['.']},{'argv':['/bin/sh']}):
            with self.assertRaises(ValueError): validate({**spec,**change},ARGV,str(root),list(INPUTS))
        altered=json.loads(json.dumps(spec));altered['executables'][0]['sha256']='0'*64
        with self.assertRaises(ValueError): validate(altered,ARGV,str(root),list(INPUTS))

    def test_object_reader_has_no_repository_process_path(self):
        root,binding,_=fixture(synthetic_acceptance=True);marker=root.parent/'MUST_NOT_EXECUTE'
        (root/'.git/hooks/post-checkout').write_text('#!/bin/sh\ntouch '+str(marker)+'\n')
        (root/'.git/config').write_text('[core]\nfsmonitor = touch '+str(marker)+'\n[filter "evil"]\nsmudge = touch '+str(marker)+'\n[remote "origin"]\npromisor = true\nurl = ext::touch '+str(marker)+'\n')
        with patch('subprocess.Popen',side_effect=AssertionError('controller subprocess forbidden')):
            self.assertEqual(read_blob(root,binding.capture_commit,'package.txt'),(root/'package.txt').read_bytes())
            with self.assertRaises(ObjectDenied): read_blob(root,'0'*40,'package.txt')
        self.assertFalse(marker.exists())
        with self.assertRaises(ObjectDenied): read_blob(root,binding.capture_commit,'../package.txt')

    def test_transport_rejects_redirect_endpoint_storage_and_ambient_proxy(self):
        from adapter.model_transport import configuration,opener,request,NoRedirect
        import urllib.request,urllib.error
        cfg=configuration()
        with patch.dict(os.environ,{'HTTPS_PROXY':'http://untrusted.invalid:1'}):
            client=opener(cfg)
        self.assertFalse(any(isinstance(h,urllib.request.ProxyHandler) and h.proxies for h in client.handlers))
        with self.assertRaises(ValueError): request(cfg,'https://untrusted.invalid',{'model':'gpt-5','store':False},'SYNTHETIC')
        with self.assertRaises(ValueError): request(cfg,cfg['endpoint'],{'model':'gpt-5','store':True},'SYNTHETIC')
        with self.assertRaises(urllib.error.HTTPError):
            NoRedirect().redirect_request(urllib.request.Request(cfg['endpoint']),None,302,'redirect',{},'https://untrusted.invalid')

    def test_derived_snapshot_tampering_and_provisioning_fail_closed(self):
        from adapter.runnable_profile import seal,launcher_policy
        from adapter.execution_snapshot import construct
        from adapter.launch_profile import provisioning
        root,binding,acceptance=fixture(synthetic_acceptance=True);spec=specification(binding,acceptance)
        with tempfile.TemporaryDirectory(prefix='g5-seal-check-') as out:
            workspace,manifest,path=construct(root,list(INPUTS),lambda rel:root/rel,out,'scope-seal')
            seal(spec,workspace,manifest,path)
            launcher_policy(workspace,ARGV)
            import io
            from adapter import exec_barrier
            class Stdin: buffer=io.BytesIO(b'1')
            with patch.object(exec_barrier.sys,'stdin',Stdin), patch.object(exec_barrier.os,'execve') as launch:
                with self.assertRaises(ValueError):
                    exec_barrier.run(str(workspace),['--gei-policy-sha256='+'0'*64,*ARGV])
                launch.assert_not_called()
            (workspace/'.gei-context/INDEX.json').write_text('tampered')
            with self.assertRaises(ValueError): launcher_policy(workspace,ARGV)
        self.assertFalse(provisioning(binding)['ready'])
        # Even present directories alone do not supply provisioning authority.
        (root/'docs/implementation').mkdir(parents=True)
        self.assertFalse(provisioning(binding)['ready'])
        from adapter.directory_provisioning import plan
        proposed=plan(root,binding.digest)
        receipt={'architect_authority_reference':'SYNTHETIC TEST ONLY',
            'plan_sha256':hashlib.sha256(json.dumps(proposed,sort_keys=True).encode()).hexdigest(),
            'created':[r['path'] for r in proposed['directories'] if r['controller_provisioning_required']],
            'result':'PASS','state':'INACTIVE','profile_activated':False}
        self.assertFalse(provisioning(binding,receipt)['ready'])
        self.assertTrue(provisioning(binding,receipt,('SYNTHETIC TEST ONLY',))['ready'])

if __name__=='__main__': unittest.main()
