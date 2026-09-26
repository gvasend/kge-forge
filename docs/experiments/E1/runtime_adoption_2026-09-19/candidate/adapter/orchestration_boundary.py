"""One session owner per phase; restart uses durable identity, never a PASS flag."""
import json
from .controller_authority_store import current,AuthorityDenied
from .authority_bootstrap import reconstruct_authorization
from .authorization_lifecycle import reconstruct
from .activation_transaction import ActivationTransaction
from .invocation_issuance import start_control
from .validation_spans import recording
from .controlled_dispatch import dispatch

def recover_boundary(store,authorization_id):
    if current() is not None:
        raise AuthorityDenied('orchestration boundary requires no ambient authority session')
    tx=None
    with store.session():
        auth=reconstruct_authorization(store,authorization_id)
        audit=store.state_path(authorization_id+':audit')
        state=reconstruct(audit.read_bytes(),auth,audit)
        ref=state['dispatch_record']['authority_id']
        control=start_control(auth,audit,json.loads(auth.model_transmission)['run_control'])
        try:
            # The process owning the audit transaction also owns its timing sink.
            with recording(control),control.span('activation_recovery'):
                tx=ActivationTransaction.recover(auth,audit,ref)
            result=dict(tx.recovery)
            if result['handoff_eligible']:
                control.emit('governance_observation',{'authorization':'ACTIVE',
                    'ownership':'OWNERSHIP_HELD','supervisor':'READY'})
            return result
        finally:
            if tx:tx.close()

def recover_then_dispatch(store,authorization_id):
    recovered=recover_boundary(store,authorization_id)
    if not recovered['handoff_eligible']:
        raise AuthorityDenied('recovered activation not eligible for dispatcher entry')
    if current() is not None:
        raise AuthorityDenied('authority session leaked across dispatcher boundary')
    # Dispatcher reconstructs and validates the current bindings/owner again.
    # No caller assertion or recovered object is supplied as effect authority.
    return dispatch(store,authorization_id)
