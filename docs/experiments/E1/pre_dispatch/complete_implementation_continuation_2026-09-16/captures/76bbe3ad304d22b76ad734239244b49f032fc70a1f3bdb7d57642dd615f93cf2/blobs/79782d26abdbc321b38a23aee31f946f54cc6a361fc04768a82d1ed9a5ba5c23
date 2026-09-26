"""Live synthetic production-transaction qualification. Never loads E1 authority."""
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch
import json, os, sys, threading, time, subprocess
from adapter.tests.test_governance_continuation import continued,write
from adapter.governance_continuation import reference
from adapter.context_projection import digest,sha,canonical
from adapter.governed_host import GovernedHost,Denied
from adapter.orchestrator import ReasoningOrchestrator
from adapter.responses_orchestrator import ResponsesReasoning
from adapter.authorization_lifecycle import reconstruct,LifecycleDenied
from adapter.activation_transaction import ActivationTransaction,invocation
from adapter import activation_transaction as production
from adapter.recovery_ledger import CGROUP_BASE,SUPERVISOR_AUDIT,_observe
from adapter.runnable_profile import ARGV,INPUTS


def fixture(out, supervisor_identity=None):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    def metadata(root,auth):
        if supervisor_identity is None:
            pid=57950;proc=Path('/proc')/str(pid)
            supervisor={'pid':pid,'ppid':int((proc/'stat').read_text().split(') ',1)[1].split()[1]),
                'exe':str((proc/'exe').resolve()),'exe_sha256':sha((proc/'exe').read_bytes()),
                'cwd':str((proc/'cwd').resolve()),'argv':(proc/'cmdline').read_bytes().rstrip(b'\0').replace(b'\0',b' ').decode(),
                'uid':proc.stat().st_uid,'cgroup':(proc/'cgroup').read_text().strip()}
        else: supervisor=supervisor_identity
        dirs=sorted(set(auth.write_directory_roots)|{str(Path(p).parent) for p in auth.write_roots}|{str(root/'docs')},key=lambda p:(len(Path(p).parts),p))
        rows=[];created=[]
        for path in dirs:
            missing=not Path(path).exists()
            if missing:Path(path).mkdir();created.append(path)
            rows.append({'path':path,'authorized_parent':str(Path(path).parent),
                'controller_provisioning_required':missing,'authority_source':'synthetic fixture authorization'})
        plan={'root':str(root),'directories':rows,'state_required':'INACTIVE'}
        receipt=write(out/'PROVISIONING.json',{'result':'PASS','plan_sha256':sha(json.dumps(plan,sort_keys=True).encode()),
            'created':created,'state':'INACTIVE','profile_activated':False})
        return {'runtime':json.loads(auth.execution_profile),'provisioning_plan':plan,
            'provisioning_receipt_sha256':receipt['sha256'],'supervisor_binding':[supervisor],
            'ownership':{'ledger':auth.ownership_ledger,'override_permitted':False},
            'model_transport':json.loads(auth.model_transport)},[Path(receipt['path'])]
    root,binding,auth,spec,projection,clearance=continued(out,inactive=True,production_metadata=metadata)
    audit=out/'controller.jsonl';host=GovernedHost(auth,audit);host.ownership.active()
    op=json.loads(auth.operational_binding)
    profile=json.loads(Path(op['governance']['released_profile']['path']).read_bytes())
    source=out/'SYNTHETIC_DISPATCH_AUTHORITY.md'
    source.write_text('Synthetic Architect dispatch for non-E1 fixture only; exact activation requirements and invocation below.\n')
    decision={'decision':'DISPATCH_AUTHORIZED','authority':'Architect','work_package_id':auth.work_package_id,
        **binding.governance.identities,**op['context_identities'],'released_profile_sha256':digest(profile),
        'invocation_identity':{k:getattr(auth,k) for k in ('authorization_id','revision','session_id','turn_id')},
        'authority_source':reference(source),
        'all_authorized_bindings':{'audit':str(audit),'ownership_ledger':auth.ownership_ledger,
            'work_id':auth.work_package_id,'operational_binding_sha256':digest(op),
            'production_task_sha256':sha((root/'task.txt').read_bytes())}}
    ref=write(out/'SYNTHETIC_DISPATCH.json',decision)
    return root,auth,audit,ref,projection


def independent_recovery(audit,ref,compete=False):
    command=[sys.executable,'-m','adapter.tests.qualify_activation_transaction',
        '--compete' if compete else '--recover-only',str(audit),ref['path'],ref['sha256']]
    result=subprocess.run(command,text=True,capture_output=True,timeout=30)
    if result.returncode: raise AssertionError(result.stderr)
    return json.loads(result.stdout)


def recovered_input(audit):
    from adapter.governed_host import WorkAuthorization
    from adapter.context_binding import CommittedContext
    raw=next(json.loads(line)['authorization'] for line in Path(audit).read_text().splitlines()
        if json.loads(line).get('event')=='authorization_issued')
    op=json.loads(raw['operational_binding']);runtime=json.loads(raw['execution_profile'])
    raw['context_binding']=CommittedContext(runtime['acceptance']['manifest_path'],
        raw['context_binding']['capture_commit'],op['governance'])
    for field in ('read_roots','write_roots','deny_roots','exec_bins','read_deny_roots','write_deny_roots','write_directory_roots'):
        raw[field]=tuple(raw[field])
    raw['exec_argv_allowlist']=tuple(tuple(x) for x in raw['exec_argv_allowlist'])
    return WorkAuthorization(**raw)


def denied(call):
    try:call()
    except Exception as exc:return {'denied':True,'exception':type(exc).__name__,'reason':str(exc)}
    raise AssertionError('unexpectedly permitted')


def facts(auth,audit,ref):
    value=reconstruct(audit.read_bytes(),auth,audit)
    own=production.InvocationOwnership(auth.ownership_ledger);fd=own._locked()
    try:owner=invocation(fd);scope=own._history(fd)
    finally:os.close(fd)
    recovered=None
    try:
        tx=ActivationTransaction.recover(auth,audit,ref)
        recovered=tx.recovery;tx.close()
    except Exception as exc:recovered={'handoff_eligible':False,'denial':str(exc),'reconciliation_required':True}
    independent=independent_recovery(audit,ref)
    return {'independent_process_recovery':independent,'state':value['state'],'phase':value['phase'],'ownership':owner,'scope':scope,
        'recovery':recovered,'audit_sha256':sha(audit.read_bytes()),
        'ledger_sha256':sha(Path(auth.ownership_ledger).read_bytes())}


def boundaries(out):
    reports={}
    for name,stop in [('before_intent','authorization_lifecycle_dispatch_authorized'),
        ('after_intent','invocation_reserved'),('owned_before_ACTIVE','authorization_lifecycle_activated')]:
        root,auth,audit,ref,_=fixture(out/name)
        append=production._append
        def interrupted(fd,row):
            if row['event']==stop:raise OSError('synthetic boundary interruption '+name)
            append(fd,row)
        with patch.object(production,'_append',interrupted):
            result=denied(lambda:ActivationTransaction.activate(auth,audit,ref))
        assert 'synthetic boundary interruption' in result['reason'],result
        result['durable']=facts(auth,audit,ref)
        assert not result['durable']['recovery']['handoff_eligible']
        result['retry']=denied(lambda:ActivationTransaction.activate(auth,audit,ref)) if name!='before_intent' else 'new explicit activation permissible; no intent or effects'
        reports[name]=result
    root,auth,audit,ref,_=fixture(out/'validation_failure')
    (root/'task.txt').write_text('UNAUTHORIZED TASK')
    before=audit.read_bytes();reports['validation_failure']=denied(lambda:ActivationTransaction.activate(auth,audit,ref))
    assert audit.read_bytes()==before
    reports['validation_failure']['audit_unchanged']=True
    root,auth,audit,ref,_=fixture(out/'ledger_unavailable')
    Path(auth.ownership_ledger).rename(auth.ownership_ledger+'.unavailable')
    reports['ledger_unavailable']=denied(lambda:ActivationTransaction.activate(auth,audit,ref))
    assert reconstruct(audit.read_bytes(),auth,audit)['state']=='INACTIVE'
    root,auth,audit,ref,_=fixture(out/'ownership_denied')
    lock=production._lease(auth.ownership_ledger)
    try:reports['ownership_denied']=denied(lambda:ActivationTransaction.activate(auth,audit,ref))
    finally:os.close(lock)
    reports['ownership_denied']['durable']=facts(auth,audit,ref)
    root,auth,audit,ref,_=fixture(out/'active_before_handoff')
    tx=ActivationTransaction.activate(auth,audit,ref);tx.close()
    reports['active_before_handoff']=facts(auth,audit,ref)
    assert reports['active_before_handoff']['recovery']['handoff_eligible']
    # A stale binding after durable ACTIVE cannot be used on restart or handoff.
    (root/'local.txt').write_bytes((root/'local.txt').read_bytes()+b'UNAUTHORIZED')
    reports['stale_ACTIVE_context']=denied(lambda:ActivationTransaction.recover(auth,audit,ref))
    root,auth,audit,ref,_=fixture(out/'missing_ownership')
    tx=ActivationTransaction.activate(auth,audit,ref);tx.close()
    Path(auth.ownership_ledger).write_bytes(b'')
    reports['ACTIVE_missing_ownership']=denied(lambda:ActivationTransaction.recover(auth,audit,ref))
    root,auth,audit,ref,_=fixture(out/'truncated_ownership')
    tx=ActivationTransaction.activate(auth,audit,ref);tx.close()
    p=Path(auth.ownership_ledger);p.write_bytes(p.read_bytes()[:-1])
    reports['truncated_ownership']=denied(lambda:ActivationTransaction.recover(auth,audit,ref))
    write(out/'FAILURE_BOUNDARIES.json',reports);return reports


def live(out):
    root,auth,audit,ref,projection=fixture(out)
    initial=audit.read_bytes();pre=facts(auth,audit,ref)
    assert pre['state']=='INACTIVE' and not pre['recovery']['handoff_eligible']
    tx=ActivationTransaction.activate(auth,audit,ref)
    activated=reconstruct(audit.read_bytes(),tx.auth,audit)['activation_event']
    assert audit.read_bytes().startswith(initial)
    competition={'independent_controller':independent_recovery(audit,ref,compete=True)}
    assert competition['independent_controller']['denied']
    competition['activation']=denied(lambda:ActivationTransaction.activate(auth,audit,ref))
    competition['recovery']=denied(lambda:ActivationTransaction.recover(auth,audit,ref))
    other=GovernedHost(tx.auth,audit)
    competition['handoff']=denied(other.verify_lifecycle)
    before_scopes=set(CGROUP_BASE.glob('scope-*'))
    competition['scope_reservation']=denied(lambda:other.ownership.reserve('scope-'+'b'*32,'competing',auth.session_id,auth.authorization_id,audit))
    assert set(CGROUP_BASE.glob('scope-*'))==before_scopes
    tx.close()
    process_restart=independent_recovery(audit,ref)
    assert process_restart['recovery']['handoff_eligible']
    tx=ActivationTransaction.recover(auth,audit,ref);restart=tx.recovery
    assert restart['handoff_eligible']
    host=GovernedHost(tx.auth,audit);tx.attach(host);host.verify_lifecycle()
    orch=ReasoningOrchestrator(host)
    class Model(ResponsesReasoning):
        def __init__(self):super().__init__(orch);self.payloads=[]
        def _call(self,payload):
            self.payloads.append(payload);n=len(self.payloads)
            if n==1:
                return {'output':[{'type':'function_call','name':'governed_exec','call_id':'bounded-exec',
                    'arguments':json.dumps({'executable':ARGV[0],'argv':list(ARGV[1:]),'cwd':str(root),'inputs':list(INPUTS)})}]}
            if n==2:return {'output':[{'type':'function_call','name':'governed_read','call_id':'local-read',
                'arguments':json.dumps({'repository':str(root),'path':'local.txt','limit':65536})}]}
            if n==3:return {'output':[{'type':'function_call','name':'finish_task','call_id':'finish','arguments':'{"summary":"synthetic bounded task completed"}'}]}
            return {'output':[]}
    runner=Model();payload=projection['projection']['payload'];result=[];errors=[]
    def work():
        try:result.append(runner.run(payload['task'],payload['context'],5))
        except Exception as exc:errors.append(repr(exc))
    thread=threading.Thread(target=work);thread.start();deadline=time.monotonic()+40
    while time.monotonic()<deadline and thread.is_alive():
        if host.scope and host.scope.state=='CLOSED':break
        time.sleep(.01)
    assert thread.is_alive() and host.scope and host.scope.state=='CLOSED',(errors,result)
    population=_observe(CGROUP_BASE/host.scope.id)
    pending={'model_requests':len(runner.payloads),'terminal_result':'bounded-exec' in orch.results}
    gated=runner._dispatch({'name':'governed_exec','call_id':'too-early','arguments':json.dumps({
        'executable':ARGV[0],'argv':list(ARGV[1:]),'cwd':str(root),'inputs':list(INPUTS)})})
    thread.join(45)
    assert not thread.is_alive() and not errors,(errors,result)
    assert result[0]['status']=='COMPLETE' and orch.results['bounded-exec']['result']=='SUCCEEDED',orch.results
    assert population['populated']==1 and population['members'] and pending=={'model_requests':1,'terminal_result':False}
    assert gated['result']=='DENIED'
    rows=[json.loads(x) for x in audit.read_text().splitlines()]
    order={name:next(i for i,x in enumerate(rows) if x.get('event')==name and x.get('action_request_id')=='bounded-exec')
        for name in ('execution_result_available','execution_scope_closed','execution_scope_quiescent','action_result')}
    assert list(order.values())==sorted(order.values())
    assert all(marker not in canonical(runner.payloads) for marker in (
        'LOCAL_ONLY_MARKER_5eb43','NEVER_TRANSMIT_MARKER_b8c22','LOCAL_ONLY_RELEASE_DECISION_7fa2'))
    terminal=ActivationTransaction.recover(auth,audit,ref);final=terminal.recovery;terminal.close()
    final['independent_process']=independent_recovery(audit,ref)
    assert final['lifecycle_state']=='COMPLETED' and final['ownership'] is None and not final['handoff_eligible']
    sid=host.scope.id
    report={'result':'PASS','activation_event':activated,'ownership_reservation':tx.reservation,
        'independent_process_ACTIVE_recovery':process_restart,'restart_before':pre,'restart_ACTIVE_owned':restart,'competition':competition,
        'while_scope_closed':population,'before_terminal':pending,'sequential_denial':gated,
        'execution_result':orch.results['bounded-exec'],'event_order':order,'programmer_result':result,
        'terminal_recovery':final,'kernel_after':_observe(CGROUP_BASE/sid),
        'supervisor_events':[json.loads(x) for x in SUPERVISOR_AUDIT.read_text().splitlines() if sid in x],
        'model_payloads':runner.payloads,'actual_API_calls':0,'real_E1_effects':0,
        'synthetic_commit':auth.context_binding.capture_commit}
    write(out/'LIVE_REPORT.json',report);return report


if __name__=='__main__':
    if sys.argv[1] in ('--recover-only','--compete'):
        try:
            audit=Path(sys.argv[2]);ref={'path':sys.argv[3],'sha256':sys.argv[4]}
            auth=recovered_input(audit)
            tx=(ActivationTransaction.activate(auth,audit,ref) if sys.argv[1]=='--compete' else ActivationTransaction.recover(auth,audit,ref))
            value={'denied':False,'recovery':getattr(tx,'recovery',{})};tx.close()
        except Exception as exc:value={'denied':True,'reason':str(exc),'handoff_eligible':False}
        print(canonical(value));sys.exit(0)
    out=Path(sys.argv[1]).resolve();out.mkdir(parents=True,exist_ok=True)
    failures=boundaries(out/'boundaries')
    report=live(out/'live')
    print(canonical({'result':report['result'],'failure_cases':len(failures),
        'activation_event':report['activation_event']['event_id'],
        'reservation':report['ownership_reservation']['reservation_id']}))
