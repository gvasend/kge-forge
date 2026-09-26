"""Attempt-attributable ownership observations; never an activation grant.

The ledger parser retains duplicate, ordering and reservation-fingerprint checks.
Only reconstructed lifecycle can establish whether attributed current ownership
is legitimate. Historical captured owners are observations, not mutable facts.
"""
import os
from pathlib import Path
from .activation_transaction import invocation, _read
from .invocation_ownership import InvocationOwnership


def observe(path):
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        data = _read(fd)
        held = os.fstat(fd)
        named = os.stat(path, follow_symlinks=False)
        if (held.st_dev, held.st_ino) != (named.st_dev, named.st_ino):
            raise ValueError('ownership ledger replaced')
        owner = invocation(fd)
        scope = InvocationOwnership.__new__(InvocationOwnership)._history(fd)
        if data != _read(fd):
            raise ValueError('ownership changed during observation')
        return owner, scope, data
    finally:
        os.close(fd)


def attribute(owner, scope, predecessors, current_identity, audit):
    """Separate predecessor ownership from exact current ownership.

    Success means attribution only. Callers must subsequently reconstruct the
    lifecycle and match its reservation before readiness or handoff is possible.
    """
    current_id = current_identity['authorization_id']
    if current_id in predecessors or len(set(predecessors)) != len(predecessors):
        raise ValueError('ambiguous attempt ancestry')
    expected = {'authorization_id': current_id,
                'session_id': current_identity['session_id'],
                'controller_audit': str(Path(audit).resolve())}
    for record in (owner, scope):
        if record is None:
            continue
        identity = record.get('authorization_id')
        if identity in predecessors:
            raise ValueError('unreleased predecessor ownership')
        if any(record.get(k) != v for k, v in expected.items()):
            raise ValueError('unknown or conflicting ownership attribution')
    if scope is not None and owner is None:
        raise ValueError('execution scope without current invocation ownership')
    return {'predecessor_ownership': None, 'current_ownership': owner,
            'current_scope': scope, 'handoff_eligible': False}


def lifecycle_ownership(lifecycle, owner, scope):
    """Reconcile a *reconstructed* lifecycle, not a caller's ACTIVE assertion."""
    state, phase = lifecycle['state'], lifecycle['phase']
    if state == 'ACTIVE':
        event = lifecycle.get('activation_event')
        if not event or owner is None or owner != event['ownership_reservation']:
            raise ValueError('ACTIVE ownership is not its exact committed reservation')
    elif phase == 'ACTIVATION_INDETERMINATE':
        # Intent/reservation crash is unresolved; it grants no handoff authority.
        if scope is not None:
            raise ValueError('execution before ACTIVE')
        return 'HELD_FOR_RECONCILIATION' if owner else 'NONE'
    elif owner is not None or scope is not None:
        raise ValueError('ownership in incompatible lifecycle state')
    return 'OWNERSHIP_HELD' if owner else 'NONE'
