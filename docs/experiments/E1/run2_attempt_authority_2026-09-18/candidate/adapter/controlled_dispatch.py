"""Explicit opt-in dispatch entry, never activates, retries, or grants authority.

An approved caller supplies an already selected private authority store. The
policy is read from its authorization, not supplied by the model or CLI flags.
"""
import json
from .run_control import RunControl
from .validation_spans import recording
from .authority_bootstrap import reconstruct_authorization
from .activation_transaction import ActivationTransaction
from .governed_host import GovernedHost
from .orchestrator import ReasoningOrchestrator
from .responses_orchestrator import ResponsesReasoning

def dispatch(store,authorization_id):
    tx=None;host=None;runner=None;control=None
    with store.session():
        raw=json.loads(store.resolve(authorization_id))
        if json.loads(raw['operational_binding'])['governance'].get('schema')==5:
            from .attempt_context import selected
            if selected()['mode']!='ISSUED':raise ValueError('specific Architect invocation issuance authorization absent')
        if json.loads(raw['operational_binding'])['governance'].get('schema')==4:
            from .run2_context import selection
            selection(authorization_id,issued=True)
        policy=json.loads(raw['model_transmission'])['run_control']
        audit=store.state_path(authorization_id+':audit')
        # This entry does not infer authority to resume a previous model cycle.
        rows=[json.loads(x) for x in audit.read_bytes().splitlines()]
        if any(r.get('event')=='model_request_content_bound' for r in rows):
            raise ValueError('prior model invocation requires explicit reconciliation; no automatic continuation')
        # An ISSUED authority selection is not proof that durable issuance exists.
        # Check lifecycle history before any authorization-bound telemetry.
        from .invocation_issuance import start_control
        with recording(None):
            admission_auth=reconstruct_authorization(store,authorization_id)
            control=start_control(admission_auth,audit,policy)
        with recording(control):
            try:
                with control.span('private_bootstrap'):auth=reconstruct_authorization(store,authorization_id)
                op=json.loads(auth.operational_binding)
                # Resolve the already issued dispatch; this helper never creates one.
                if 'material_release' in op['governance']:
                    d=json.loads(store.resolve('sha256:'+op['governance']['material_release']['dispatch_amendment']['sha256']))
                    ref='E1-ARCHITECT-DISPATCH-sha256:'+d['original_dispatch']['sha256']
                else:
                    from .authorization_lifecycle import reconstruct
                    ref=reconstruct(audit.read_bytes(),auth,audit)['dispatch_record']['authority_id']
                with control.span('activation_recovery'):tx=ActivationTransaction.recover(auth,audit,ref)
                if not tx.recovery['handoff_eligible']:raise ValueError('current activation not eligible')
                with control.span('host_construction'):
                    host=GovernedHost(tx.auth,audit);host.run_control=control;tx.attach(host)
                with control.span('reasoning_construction'):
                    runner=ResponsesReasoning(ReasoningOrchestrator(host))
                    payload=runner.projection.verify()['projection']['payload']
                return runner.run(payload['task'],payload['context'])
            except BaseException:
                if runner is None:
                    control.close('PREPARATION_INTERRUPTED')
                    if host and tx:
                        host.revoke();result=tx.cancel(host,'PREPARATION_INTERRUPTED')
                    else:
                        # Never manufacture a host/lease or release unresolved ownership.
                        result={'disposition':'INDETERMINATE','ownership':'UNKNOWN',
                            'uncertainty':'PREPARATION_INTERRUPTED_RECONCILIATION_REQUIRED'}
                    control.emit('final_disposition',result)
                raise
            finally:
                if tx:tx.close()
