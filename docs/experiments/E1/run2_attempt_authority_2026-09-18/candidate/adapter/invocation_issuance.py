"""Candidate orchestration barrier; no real issuance until Architect review.

Pre-issuance validation has no authorization-bound telemetry sink. Existing audit
paths (even empty ones) are never reset, repaired, renamed, or silently reused.
"""
import json
import os
from pathlib import Path
from adapter.activation_transaction import _lease, invocation
from adapter.authorization_lifecycle import dispatch_binding, reconstruct, LifecycleDenied
from adapter.governed_host import GovernedHost
from adapter.invocation_ownership import InvocationOwnership
from adapter.run_control import RunControl
from adapter.validation_spans import recording


def issue_inactive(auth, audit, dispatch_ref):
    audit = Path(audit)
    if json.loads(auth.operational_binding)['governance'].get('schema')==5:
        from .attempt_context import require_issued as require_specific_authorization
        require_specific_authorization(auth)
        from .invocation_attempt import require_claim
        from .controller_authority_store import current
        require_claim(current(),auth.context_binding.governance.run5['amendment']['proposal'])
    if auth.state != 'INACTIVE':
        raise LifecycleDenied('new issuance requires INACTIVE template')
    fence = _lease(Path(auth.ownership_ledger))
    try:
        if os.path.lexists(str(audit)):
            raise LifecycleDenied('new issuance requires unused audit; existing evidence preserved')
        owner = InvocationOwnership(auth.ownership_ledger)
        fd = owner._locked()
        try:
            if invocation(fd) is not None or owner._history(fd) is not None:
                raise LifecycleDenied('competing ownership requires reconciliation')
        finally:
            os.close(fd)
        # Validate exact Architect dispatch before the first durable lifecycle fact.
        # Suppress only the optional timing sink, never an authority check.
        with recording(None):
            dispatch_binding(auth, audit, dispatch_ref)
            host = GovernedHost(auth, audit)
        require_issued(auth, audit)
        return host
    finally:
        os.close(fence)


def require_issued(auth, audit):
    data = Path(audit).read_bytes()
    rows = [json.loads(line) for line in data.splitlines()]
    if not rows or rows[0].get('event') != 'authorization_issued':
        raise LifecycleDenied('original INACTIVE authorization must precede telemetry')
    if rows[0]['authorization'].get('state') != 'INACTIVE':
        raise LifecycleDenied('initial authorization is not INACTIVE')
    return reconstruct(data, auth, Path(audit))


def start_control(auth, audit, policy):
    require_issued(auth, audit)
    return RunControl(audit, {'authorization_id': auth.authorization_id,
        'session_id': auth.session_id, 'invocation_id': auth.turn_id,
        'work_package_id': auth.work_package_id}, policy)
