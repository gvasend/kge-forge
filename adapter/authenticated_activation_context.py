"""Typed composition of independently authenticated activation proofs.

This layer owns no authority. It rejects missing, stale, conflicting, or
caller-asserted proofs before an activation transaction can run.
"""
from dataclasses import dataclass

class ActivationContextDenied(ValueError): pass

@dataclass(frozen=True)
class Proof:
    kind: str
    invocation_id: str
    source: str
    identity: str
    fresh: bool = True
    authenticated: bool = True
    values: tuple = ()

@dataclass(frozen=True)
class AuthenticatedActivationContext:
    invocation_id: str
    lifecycle: Proof
    invocation: Proof
    dispatch: Proof
    operational: Proof
    context: Proof
    profile: Proof
    ownership: Proof
    audit: Proof

_REQUIRED=('lifecycle','invocation','dispatch','operational','context','profile','ownership','audit')

def compose(**proofs):
    if set(proofs)!=set(_REQUIRED): raise ActivationContextDenied('activation proofs incomplete')
    for name,p in proofs.items():
        if not isinstance(p,Proof) or not p.authenticated: raise ActivationContextDenied(f'{name} proof unauthenticated')
        if not p.fresh: raise ActivationContextDenied(f'{name} proof stale')
    ids={p.invocation_id for p in proofs.values()}
    if len(ids)!=1: raise ActivationContextDenied('activation proof invocation mismatch')
    if proofs['lifecycle'].kind!='INACTIVE': raise ActivationContextDenied('INACTIVE lifecycle proof required')
    if proofs['ownership'].kind!='OWNERSHIP_NONE': raise ActivationContextDenied('ownership is not NONE')
    if proofs['audit'].kind!='AUDIT_UNUSED': raise ActivationContextDenied('audit namespace is not unused')
    return AuthenticatedActivationContext(next(iter(ids)),**proofs)
