"""Synthetic Run-2 remediation qualification. No E1 dispatch or network calls."""
from dataclasses import replace
from pathlib import Path
import json,tempfile,time,unittest
from types import SimpleNamespace
from unittest.mock import patch
from adapter.run_control import RunControl,E1_POLICY,BudgetExceeded,events,status
from adapter.governed_host import GovernedHost,WorkAuthorization
from adapter.model_transmission import production_policy,digest,TransmissionBoundary
from adapter.orchestrator import ReasoningOrchestrator
from adapter.responses_orchestrator import ResponsesReasoning,tool_definitions,TOOL_NAMES

IDENTITY={'authorization_id':'synthetic','session_id':'synthetic','invocation_id':'synthetic','work_package_id':'synthetic'}
class Clock:
    def __init__(self):self.now=1000.
    def __call__(self):return self.now

class BudgetTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.path=Path(self.tmp.name)/'audit';self.clock=Clock()
        self.c=RunControl(self.path,IDENTITY,E1_POLICY,self.clock,self.clock)
    def tearDown(self):self.tmp.cleanup()
    def test_no_progress_soft_hard_and_restart(self):
        self.clock.now+=181;self.c.emit('activity',{});self.c.check()
        self.assertTrue(any(r['event']=='budget_warning' for r in events(self.path)))
        restarted=RunControl(self.path,IDENTITY,E1_POLICY,self.clock,self.clock)
        self.assertEqual(restarted.progress,1000)
        self.clock.now=1300
        with self.assertRaises(BudgetExceeded):restarted.check()
        with self.assertRaises(BudgetExceeded):RunControl(self.path,IDENTITY,E1_POLICY,self.clock,self.clock)
    def test_equivalent_progress_and_usage(self):
        self.clock.now+=1;self.c.progress_event('same','GOVERNED_RESULT');first=self.c.progress
        self.clock.now+=10;self.c.progress_event('same','GOVERNED_RESULT')
        self.assertEqual(first,self.c.progress)
        self.c.response({'id':'resp_fixture','usage':{'input_tokens':1,'output_tokens':2,'total_tokens':3},'output':[{'text':'PROTECTED'}]})
        self.assertEqual(self.c.tokens,3);self.assertNotIn('PROTECTED',self.path.read_text())
        self.c.response({'usage':{'total_tokens':0}});self.assertFalse(self.c.usage_known)
    def test_cycle_phase_invocation_count_tokens(self):
        for name in ('cycle','phase','invocation','requests','tokens'):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as d:
                clock=Clock();c=RunControl(Path(d)/'audit',IDENTITY,E1_POLICY,clock,clock)
                if name in ('cycle','phase','invocation'):
                    hard=E1_POLICY['seconds'][name][1]
                    if name=='cycle':c.cycle_start=1000
                    if name=='phase':c.phase='validation';c.phase_start=1000
                    clock.now+=hard;c.progress=clock.now
                else:setattr(c,name,E1_POLICY[name][1])
                with self.assertRaises(BudgetExceeded):c.check(admit_model=True)
    def test_blocking_phase_is_interrupted(self):
        c=RunControl(Path(self.tmp.name)/'real',IDENTITY,E1_POLICY)
        c.start=time.monotonic()-1799.9
        begin=time.monotonic()
        with self.assertRaises(BudgetExceeded):
            with c.span('validation'):time.sleep(5)
        self.assertLess(time.monotonic()-begin,1)
        self.assertTrue(c.closed)
    def test_unresolved_request_never_replayed(self):
        self.c.emit('model_request_start',{'request_digest':'0'*64})
        with self.assertRaises(BudgetExceeded):RunControl(self.path,IDENTITY,E1_POLICY,self.clock,self.clock)
    def test_reordered_or_substituted_timing_rejected(self):
        self.c.emit('activity',{});rows=self.path.read_text().splitlines()
        self.path.write_text('\n'.join(reversed(rows))+'\n')
        with self.assertRaises(ValueError):status(self.path)
    def test_fresh_and_stale_status(self):
        self.c.emit('governance_observation',{'authorization':'ACTIVE','ownership':'HELD','supervisor':'READY'})
        self.assertEqual(status(self.path,1000)['supervisor_readiness'],'READY')
        self.assertEqual(status(self.path,1061)['supervisor_readiness'],'UNKNOWN')
    def test_mutable_governance_age_is_not_refreshed_by_activity(self):
        self.c.emit('governance_observation',{'authorization':'ACTIVE','ownership':'HELD','supervisor':'READY'})
        self.clock.now=1061;self.c.emit('activity',{})
        self.assertEqual(status(self.path,1061)['supervisor_readiness'],'UNKNOWN')
    def test_budget_closure_blocks_independent_production_admission(self):
        from adapter.run_control import assert_admission
        self.c.close('HARD_STOP')
        with self.assertRaises(BudgetExceeded):assert_admission(self.path,E1_POLICY,IDENTITY)

class InteractionTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.base=Path(self.tmp.name)
        self.root=self.base/'repo';self.root.mkdir();self.audit=self.base/'audit'
        (self.root/'public.txt').write_text('CLEARED CONTENT')
        policy=production_policy(SimpleNamespace(digest='synthetic'));policy['run_control']=E1_POLICY
        policy['safe_diagnostics']={'schema':'E1-SAFE-DIAGNOSTICS-1','codes':['READ_LIMIT_OUT_OF_RANGE']}
        policy['action_evidence']='GRANTED_RESOURCE_AND_SCALARS_V1'
        self.payload={'task':'SYNTHETIC','context':{}}
        policy['initial_clearances']=[{'sha256':digest(self.payload),'category':'cleared-reasoning-context','authority_source':'synthetic'}]
        import hashlib
        policy['file_clearances']=[{'path':str(self.root/'public.txt'),'sha256':hashlib.sha256(b'CLEARED CONTENT').hexdigest(),'category':'ordinary','authority_source':'synthetic'}]
        self.auth=WorkAuthorization('synthetic',1,'synthetic','session','turn',read_roots=(str(self.root),),model_transmission=json.dumps(policy))
        self.host=GovernedHost(self.auth,self.audit);self.orch=ReasoningOrchestrator(self.host)
        self.host.run_control=RunControl(self.audit,{'authorization_id':'synthetic','session_id':'session',
            'invocation_id':'turn','work_package_id':'synthetic'},E1_POLICY)
    def tearDown(self):self.tmp.cleanup()
    def test_correction_multicycle_and_incomplete(self):
        root=self.root;observations=[]
        class Model(ResponsesReasoning):
            def _call(s,payload):
                observations.append(status(s.orchestrator.host.audit))
                n=len(observations)
                if n==2:
                    output=json.loads(payload['input'][-1]['output'])
                    assert output['reason_code']=='READ_LIMIT_OUT_OF_RANGE'
                    assert output['permitted_range']=={'minimum':1,'maximum':65536}
                if n==3:assert json.loads(payload['input'][-1]['output'])['content']=='CLEARED CONTENT'
                call={'type':'function_call','name':'governed_read','call_id':'call_'+str(n),
                    'arguments':json.dumps({'repository':str(root),'path':'public.txt','limit':65537 if n==1 else 65536})}
                return {'id':'resp_'+str(n),'usage':{'input_tokens':10,'output_tokens':2,'total_tokens':12},
                    'output':[call] if n<3 else [{'type':'message','text':'DO_NOT_RETAIN'}]}
        model=Model(self.orch);r=model.run(**self.payload)
        self.assertEqual(r['status'],'INCOMPLETE');self.assertTrue(self.host._interruption_requested)
        rows=events(self.audit);s=status(self.audit)
        self.assertEqual(s['responses'],3);self.assertEqual(s['model_requests'],3)
        self.assertEqual(s['reported_cumulative_tokens'],36)
        self.assertEqual(s['usage_state'],'REPORTED_ONLY_NO_RESERVATION')
        self.assertEqual(s['token_budget_state'],'USAGE_UNKNOWN')
        self.assertEqual(s['action_requests'],{'accepted':1,'denied':1,'pending':0})
        self.assertEqual(s['terminal_disposition']['disposition'],'CANCELLED')
        self.assertEqual(s['ownership'],'NONE');self.assertNotIn('DO_NOT_RETAIN',self.audit.read_text())
        req=next(r for r in rows if r.get('event')=='action_request')
        self.assertEqual(req['argument_evidence']['limit'],65537)
        self.assertEqual(req['argument_evidence']['granted_resource'],str(root/'public.txt'))
        self.assertTrue(all(s['outstanding_operation']=='provider_transport' for s in observations))
        self.assertEqual(sum(r['event']=='substantive_progress' for r in rows),1)
        self.assertEqual(len({r['cycle'] for r in rows if r.get('schema')=='E1-RUN-CONTROL-1'}),4)
    def test_diagnostics_do_not_echo_protected_material(self):
        boundary=TransmissionBoundary(self.host)
        call={'name':'governed_read','arguments':json.dumps({'repository':'SECRET','path':'CREDENTIAL','limit':65537})}
        result={'result':'DENIED','reason_code':'READ_LIMIT_OUT_OF_RANGE','error':'SECRET CREDENTIAL'}
        safe=boundary.result(call,result)
        self.assertEqual(safe['reason_code'],'READ_LIMIT_OUT_OF_RANGE')
        self.assertNotIn('SECRET',json.dumps(safe));self.assertNotIn('CREDENTIAL',json.dumps(safe))
        call['arguments']=json.dumps({'limit':1})
        self.assertEqual(boundary.result(call,result)['transmission'],'REDACTED')
        boundary.policy.pop('safe_diagnostics')
        self.assertEqual(boundary.result(call,result)['transmission'],'REDACTED')
    def test_provider_timeout_preserves_remote_uncertainty(self):
        class Model(ResponsesReasoning):
            def _call(s,payload):
                s.control.start=time.monotonic()-1799.9;s.control._arm();time.sleep(5)
        with self.assertRaises(BudgetExceeded):Model(self.orch).run(**self.payload)
        state=status(self.audit)
        self.assertEqual(state['model_requests'],1);self.assertEqual(state['responses'],0)
        self.assertEqual(state['uncertainty'],'REQUEST_OUTCOME_UNKNOWN')
        self.assertEqual(state['terminal_disposition']['disposition'],'CANCELLED')
        self.assertEqual(state['authoritative_effects'],0)
    def test_all_nine_contracts_and_runtime_boundaries(self):
        schemas={r['name']:r for r in tool_definitions()}
        self.assertEqual(set(schemas),set(TOOL_NAMES));self.assertEqual(len(schemas),9)
        for name,maximum in [('governed_read',65536),('governed_list',1000),('governed_search',100)]:
            spec=schemas[name]['parameters']['properties']['limit']
            self.assertEqual((spec['minimum'],spec['maximum']),(1,maximum))
        self.assertEqual(schemas['governed_patch']['parameters']['properties']['changes']['maxItems'],1)
        from adapter.governed_host import Denied
        for n in (0,65537):
            with self.assertRaises(Denied):self.host.governed_read(str(self.root),'public.txt',n)
        for n in (1,65536):self.assertIn('content',self.host.governed_read(str(self.root),'public.txt',n))

class LifecycleTests(unittest.TestCase):
    def test_cancel_releases_and_independent_reconstruction(self):
        from adapter.tests.qualify_activation_transaction import fixture
        from adapter.tests.test_controller_authority_store import private_fixture
        from adapter.activation_transaction import ActivationTransaction
        with tempfile.TemporaryDirectory() as d:
            out=Path(d);root,auth,audit,ref,projection=fixture(out/'fixture',supervisor_identity={'synthetic':'NON_LIVE'})
            store=private_fixture(auth,audit,ref,out/'private')
            try:
                with store.session(),patch('adapter.activation_transaction._host',return_value={'synthetic':'NON_LIVE'}):
                    logical='E1-ARCHITECT-DISPATCH-sha256:'+ref['sha256']
                    tx=ActivationTransaction.activate(auth,audit,logical)
                    host=GovernedHost(tx.auth,audit);tx.attach(host)
                    host.run_control=RunControl(audit,{'authorization_id':auth.authorization_id,
                        'session_id':auth.session_id,'invocation_id':auth.turn_id,'work_package_id':auth.work_package_id},E1_POLICY)
                    class Model(ResponsesReasoning):
                        def _call(self,payload):return {'id':'resp_fixture','output':[{'type':'message','content':'NOT_RETAINED'}]}
                    result=Model(ReasoningOrchestrator(host)).run(**projection['projection']['payload'])
                    self.assertEqual(result['status'],'INCOMPLETE')
                    self.terminal_status=status(audit)
                    self.assertEqual(status(audit)['ownership'],'RELEASED');tx.close()
                    recovered=ActivationTransaction.recover(auth,audit,logical)
                    self.assertEqual(recovered.recovery['lifecycle_state'],'CANCELLED')
                    self.assertFalse(recovered.recovery['handoff_eligible']);self.assertIsNone(recovered.recovery['ownership']);recovered.close()
            finally:store.close()

    def test_budget_interrupts_execution_and_reconciles_without_retry(self):
        from adapter.tests.test_production_exec import ProductionExecTests
        case=ProductionExecTests('test_model_facing_schema_and_mapping');case.setUp()
        try:
            c=RunControl(case.audit,IDENTITY,E1_POLICY);case.host.run_control=c
            case.bridge.status_release.clear()
            def bridge(*args):
                instance=case.bridge(*args);exchange=instance.exchange
                triggered=False
                def observed(op,**kwargs):
                    nonlocal triggered
                    if op=='quiescent' and not triggered:
                        triggered=True;c.start=time.monotonic()-1799.9;c._arm()
                    return exchange(op,**kwargs)
                instance.exchange=observed;return instance
            with patch('adapter.governed_host.ForwardBridge',bridge),self.assertRaises(BudgetExceeded):
                with c.span('action_dispatch'):result=case.request()
            case.host.revoke()
            self.assertEqual(case.host.scope.state,'QUIESCENT')
            self.assertEqual(sum(op[2]=='production_spawn' for op in case.bridge.calls),1)
            self.assertEqual(sum(op[2]=='terminate_reconcile' for op in case.bridge.calls),1)
            self.assertEqual(case.orchestrator.results['req-1']['result'],'INDETERMINATE')
            with self.assertRaises(BudgetExceeded):case.request('must-not-retry')
        finally:case.tearDown()

if __name__=='__main__':unittest.main()
