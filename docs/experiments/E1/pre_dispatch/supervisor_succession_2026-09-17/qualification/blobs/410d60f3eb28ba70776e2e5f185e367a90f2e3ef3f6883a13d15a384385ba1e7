"""Focused synthetic committed qualification of controller/model separation."""
from dataclasses import replace
from pathlib import Path
import json,tempfile,unittest
from adapter.tests.test_runnable_profile import fixture,git
from adapter.context_binding import CommittedContext
from adapter.context_projection import specification,derive,sha,digest,canonical
from adapter.runnable_profile import authorization
from adapter.model_transmission import production_policy
from adapter.governed_host import GovernedHost,Denied,WorkAuthorization
from adapter.orchestrator import ReasoningOrchestrator
from adapter.responses_orchestrator import ResponsesReasoning


def prepared(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    root,old,acceptance=fixture(synthetic_acceptance=True)
    contents={'task.txt':'SYNTHETIC_TASK_ONLY\n','public.txt':'CLEARED_PUBLIC_ONLY\n',
              'local.txt':'LOCAL_ONLY_MARKER_5eb43; deny writes to protected governing files\n',
              'private.txt':'NEVER_TRANSMIT_MARKER_b8c22\n'}
    manifest=json.loads(old.path.read_text())
    for rel,value in contents.items():
        (root/rel).write_text(value)
        manifest['sources'].append({'id':rel,'repository':'forge','path':rel,
            'sha256':sha(value.encode()),'revision_binding':'package_capture_commit',
            'knowledge_status':'DECIDED','dependencies':[]})
        manifest['mandatory_roots'].append(rel)
    manifest['scope']['protected_paths'].append('local.txt')
    manifest['prerequisites']=[{'id':'LOCAL_ONLY_GATE_NAME_90c5','status':'LOCAL_ONLY_GATE_STATUS_c40f'}]
    old.path.write_text(json.dumps(manifest));git(root,'add','.');git(root,'commit','-qm','Synthetic separated context')
    binding=CommittedContext(old.path,git(root,'rev-parse','HEAD'))
    capdir=out/'authority';capdir.mkdir();(capdir/'blobs').mkdir()
    inputs={};entries=[]
    capture_contents={**contents,'package.txt':(root/'package.txt').read_text(),
                      'CONTEXT_MANIFEST.json':binding.path.read_text()}
    for rel,value in capture_contents.items():
        data=(root/rel).read_bytes();key=sha(data);(capdir/'blobs'/key).write_bytes(data)
        inputs[str(root/rel)]={'sha256':key,'bytes':len(data)}
        cls='TRANSMIT' if rel in ('task.txt','public.txt') else 'NEVER_TRANSMIT' if rel in ('private.txt','CONTEXT_MANIFEST.json') else 'LOCAL_ONLY'
        row={'source_identity':rel,'canonical_path':str(root/rel),'captured_sha256':key,
             'classification':cls,'designation':'COMPLETE_FILE'}
        if cls=='TRANSMIT':row['spans']=[{'start_byte':0,'end_byte_exclusive':len(data),'sha256':key,'label':rel}]
        entries.append(row)
    cap=capdir/'MANIFEST.json';cap.write_text(canonical({'inputs':inputs,'commit':binding.capture_commit}))
    clearance=out/'CLEARANCE.json';clearance.write_text(canonical({'candidate':{'capture_sha256':sha(cap.read_bytes())},'inputs':entries}))
    spec=specification(binding,cap,clearance,root/'task.txt',{})
    projection=derive(spec,binding);payload=projection['projection']['payload']
    policy=production_policy(binding)
    policy['initial_clearances']=[{'sha256':digest(payload),'category':'cleared-reasoning-context','authority_source':'Synthetic committed qualification'}]
    policy['file_clearances']=[{'path':str(root/'public.txt'),'sha256':inputs[str(root/'public.txt')]['sha256'],
                              'category':'explicitly-cleared-governing','authority_source':'Synthetic committed qualification'}]
    auth=authorization(binding,binding,'projection-fixture',6,'projection-session','projection-turn',True)
    auth=replace(auth,model_transmission=canonical(policy),context_projection=canonical(spec))
    return root,binding,auth,spec,projection,clearance


def qualify(out):
    out=Path(out);root,binding,auth,spec,projection,clearance=prepared(out)
    host=GovernedHost(auth,out/'controller.jsonl');orch=ReasoningOrchestrator(host)
    local=binding.model_context();assert local['prerequisites'][0]['status']=='LOCAL_ONLY_GATE_STATUS_c40f'
    class Model(ResponsesReasoning):
        def __init__(self,orchestrator,mutate=None):super().__init__(orchestrator);self.payloads=[];self.mutate=mutate
        def _call(self,payload):
            self.payloads.append(json.loads(json.dumps(payload)))
            if self.mutate:self.mutate();return {'output':[{'type':'function_call','name':'governed_status','call_id':'stale','arguments':'{}'}]}
            n=len(self.payloads)
            if n<=4:
                names=['governed_read','governed_read','governed_read','governed_write']
                paths=['public.txt','local.txt','private.txt','local.txt']
                args={'repository':str(root),'path':paths[n-1]}
                args.update({'content':'MUST NOT CHANGE'} if n==4 else {'limit':65536})
                return {'output':[{'type':'function_call','name':names[n-1],'call_id':'loop-'+str(n),'arguments':json.dumps(args)}]}
            if n==5:return {'output':[{'type':'function_call','name':'finish_task','call_id':'done','arguments':'{"summary":"synthetic complete"}'}]}
            return {'output':[]}
    runner=Model(orch);payload=projection['projection']['payload']
    result=runner.run(payload['task'],payload['context'],6);assert result['status']=='COMPLETE'
    assert runner.payloads[0]['input'][0]['content'][0]['text']==payload['task']+'\nContext:\n'+canonical(payload['context'])
    serialized=json.dumps(runner.payloads)
    forbidden=['LOCAL_ONLY_MARKER_5eb43','NEVER_TRANSMIT_MARKER_b8c22','LOCAL_ONLY_GATE_NAME_90c5','LOCAL_ONLY_GATE_STATUS_c40f']
    assert not any(x in serialized for x in forbidden)
    assert 'CLEARED_PUBLIC_ONLY' in serialized and 'SYNTHETIC_TASK_ONLY' in serialized
    assert orch.results['loop-4']['result']=='DENIED' and (root/'local.txt').read_text().startswith(forbidden[0])
    assert runner.projection.verify()['controller_context']['controller_context']==local
    # Fresh restart rebuilds full and projected identities from the same immutable
    # authorization and existing local audit, with no model evidence replay.
    issued=next(json.loads(line)['authorization'] for line in (out/'controller.jsonl').read_text().splitlines()
                if json.loads(line).get('event')=='authorization_issued')
    issued['context_binding']=CommittedContext(binding.path,issued['context_binding']['capture_commit'])
    for field in ('read_roots','write_roots','deny_roots','exec_bins','read_deny_roots','write_deny_roots','write_directory_roots'):
        issued[field]=tuple(issued[field])
    issued['exec_argv_allowlist']=tuple(tuple(row) for row in issued['exec_argv_allowlist'])
    recovered_auth=WorkAuthorization(**issued)
    resumed_host=GovernedHost(recovered_auth,out/'controller.jsonl')
    resumed=ResponsesReasoning(ReasoningOrchestrator(resumed_host))
    rebuilt=resumed.projection.verify()
    assert all(rebuilt[k]==projection[k] for k in ('AuthoritativeContextId','FullContextDigest','ModelProjectionDigest'))
    altered=replace(recovered_auth,context_projection=canonical(dict(spec,ModelProjectionDigest='0'*64)))
    try:GovernedHost(altered,out/'controller.jsonl')
    except Denied:pass
    else:raise AssertionError('changed projection adopted on restart')
    stale=[]
    for rel in ('public.txt','local.txt','private.txt'):
        path=root/rel;before=path.read_bytes();path.write_bytes(before+b'changed')
        try:resumed.projection.verify()
        except ValueError:stale.append(rel)
        else:raise AssertionError('stale source accepted')
        finally:path.write_bytes(before)
    before=clearance.read_bytes();clearance.write_bytes(before+b' ')
    try:resumed.projection.verify()
    except ValueError:stale.append('clearance')
    else:raise AssertionError('changed clearance accepted')
    finally:clearance.write_bytes(before)
    saved=resumed.projection.spec['ModelProjectionDigest'];resumed.projection.spec['ModelProjectionDigest']='0'*64
    try:resumed.projection.verify()
    except ValueError:stale.append('projection')
    else:raise AssertionError('changed projection accepted')
    finally:resumed.projection.spec['ModelProjectionDigest']=saved
    resumed_host.auth=replace(recovered_auth,turn_id='substituted')
    try:resumed.projection.verify()
    except ValueError:stale.append('turn-binding')
    else:raise AssertionError('substituted identity accepted')
    finally:resumed_host.auth=recovered_auth
    # Changes between response and action prevent the action and next API request.
    for field in ('local.txt','public.txt'):
        before=(root/field).read_bytes()
        fresh=GovernedHost(auth,out/('between-'+field+'.jsonl'))
        model=Model(ReasoningOrchestrator(fresh),lambda:(root/field).write_bytes(before+b'changed'))
        try:model.run(payload['task'],payload['context'],6)
        except ValueError:pass
        else:raise AssertionError('stale continuation accepted')
        finally:(root/field).write_bytes(before)
        assert len(model.payloads)==1 and not fresh.invocations
        stale.append('between-response-action-'+field)
    contradictory=json.loads(auth.model_transmission)
    contradictory['file_clearances'].append({'path':str(root/'local.txt'),
        'sha256':sha((root/'local.txt').read_bytes()),'category':'explicitly-cleared-governing',
        'authority_source':'not authorized by accepted clearance'})
    bad_host=GovernedHost(replace(auth,model_transmission=canonical(contradictory)),out/'contradictory-policy.jsonl')
    try:ResponsesReasoning(ReasoningOrchestrator(bad_host))
    except ValueError:stale.append('policy-clearance-contradiction')
    else:raise AssertionError('contradictory transmission policy accepted')
    # A caller cannot supply an independently authored projection.
    changed=json.loads(json.dumps(payload['context']));changed['summary']='invented'
    try:resumed.run(payload['task'],changed,1)
    except ValueError:stale.append('caller-projection')
    else:raise AssertionError('caller projection accepted')
    report={'result':'PASS','synthetic_commit':binding.capture_commit,
       'identities':{k:projection[k] for k in ('AuthoritativeContextId','FullContextDigest','ModelProjectionDigest')},
       'controller_retained_local_state':True,'model_payloads':runner.payloads,
       'forbidden_markers_absent':forbidden,'iterative_result':result,'local_governance_denial':orch.results['loop-4'],
       'stale_denials':stale,'recovery':'PASS exact identities; changed authorization rejected',
       'projection':projection,'api_calls':0,'E1_activated':False,'E1_executed':False}
    (out/'REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


def live_qualify(out):
    import threading,time
    from adapter.runnable_profile import ARGV,INPUTS
    from adapter.recovery_ledger import _observe,CGROUP_BASE,SUPERVISOR_AUDIT
    out=Path(out);root,binding,auth,spec,projection,clearance=prepared(out)
    auth=replace(auth,ownership_ledger=str(out/'ownership.jsonl'))
    host=GovernedHost(auth,out/'controller.jsonl');orch=ReasoningOrchestrator(host)
    class Model(ResponsesReasoning):
        def __init__(self,orchestrator):super().__init__(orchestrator);self.payloads=[]
        def _call(self,payload):
            self.payloads.append(json.loads(json.dumps(payload)));n=len(self.payloads)
            if n<=2:return {'output':[{'type':'function_call','name':'governed_exec',
                'call_id':'execution-'+str(n),'arguments':json.dumps({'executable':ARGV[0],
                'argv':list(ARGV[1:]),'cwd':str(root),'inputs':list(INPUTS)})}]}
            if n==3:return {'output':[{'type':'function_call','name':'finish_task',
                'call_id':'finish','arguments':'{"summary":"synthetic execution complete"}'}]}
            return {'output':[]}
    runner=Model(orch);payload=projection['projection']['payload'];results=[];errors=[]
    def work():
        try:results.append(runner.run(payload['task'],payload['context'],4))
        except Exception as exc:errors.append(repr(exc))
    thread=threading.Thread(target=work);thread.start();deadline=time.monotonic()+25
    while time.monotonic()<deadline and thread.is_alive():
        if host.scope and host.scope.state=='CLOSED':break
        time.sleep(.01)
    population=None;gated=None;before_terminal=None
    if thread.is_alive() and host.scope and host.scope.state=='CLOSED':
        population=_observe(CGROUP_BASE/host.scope.id)
        before_terminal={'model_requests':len(runner.payloads),'terminal_result_present':'execution-1' in orch.results}
        gated=runner._dispatch({'name':'governed_exec','call_id':'while-active',
            'arguments':json.dumps({'executable':ARGV[0],'argv':list(ARGV[1:]),'cwd':str(root),'inputs':list(INPUTS)})})
    thread.join(40)
    report={'errors':errors,'results':results,'population_while_active':population,
        'before_terminal':before_terminal,'sequential_gating':gated,'model_payloads':runner.payloads,
        'synthetic_commit':binding.capture_commit,'api_calls':0,'real_E1_inputs_used':False}
    (out/'LIVE_REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
    assert not errors and not thread.is_alive() and results[0]['status']=='COMPLETE',report
    assert population['populated']==1 and population['members']
    assert before_terminal=={'model_requests':1,'terminal_result_present':False}
    assert gated['result']=='DENIED'
    serialized=json.dumps(runner.payloads)
    for marker in ('LOCAL_ONLY_MARKER_5eb43','NEVER_TRANSMIT_MARKER_b8c22','LOCAL_ONLY_GATE_NAME_90c5','LOCAL_ONLY_GATE_STATUS_c40f'):
        assert marker not in serialized
    events=[json.loads(line) for line in host.audit.read_text().splitlines()]
    scopes=[]
    for rid in ('execution-1','execution-2'):
        assert orch.results[rid]['result']=='SUCCEEDED'
        sid=orch.results[rid]['data']['scope_id'];scopes.append(sid)
        order=[next(i for i,e in enumerate(events) if e.get('event')==name and e.get('action_request_id')==rid)
            for name in ('execution_result_available','execution_scope_closed','execution_scope_quiescent','action_result')]
        assert order==sorted(order)
    assert scopes[0]!=scopes[1] and host.ownership.active() is None
    report.update({'result':'PASS','scope_ids':scopes,'kernel_after':{sid:_observe(CGROUP_BASE/sid) for sid in scopes},
       'supervisor_events':[json.loads(line) for line in SUPERVISOR_AUDIT.read_text().splitlines() if any(sid in line for sid in scopes)],
       'active_ownership':None,'exact_runnable_profile':json.loads(auth.execution_profile),
       'context_identities':{k:projection[k] for k in ('AuthoritativeContextId','FullContextDigest','ModelProjectionDigest')}})
    assert all(not v['members'] and v['populated']==0 for v in report['kernel_after'].values())
    (out/'LIVE_REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


class ContextProjectionTests(unittest.TestCase):
    def test_synthetic_committed_projection(self):
        with tempfile.TemporaryDirectory(prefix='pd06-separated-') as out:self.assertEqual(qualify(out)['result'],'PASS')

if __name__=='__main__':unittest.main()
