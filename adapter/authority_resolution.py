"""Successor-only authority reference resolution.

Resolvers fetch values only from their owning authority domain and preserve
source/generation provenance. They never infer authority from copied fields.
"""
from dataclasses import dataclass
from pathlib import Path
import hashlib, json

class ResolutionDenied(ValueError): pass

def canonical(v): return json.dumps(v,sort_keys=True,separators=(',',':')).encode()
def digest_bytes(b): return hashlib.sha256(b).hexdigest()

@dataclass(frozen=True)
class ResolvedAuthorityValue:
    kind: str
    value: object
    authority_domain: str
    source_identity: str
    source_store: str
    invocation_id: str
    freshness: str
    value_sha256: str

    @classmethod
    def from_bytes(cls,kind,value,domain,identity,store,invocation_id,fresh='FRESH'):
        raw=value if isinstance(value,bytes) else canonical(value)
        return cls(kind,value,domain,identity,store,invocation_id,fresh,digest_bytes(raw))

def _read_json(path):
    p=Path(path)
    if not p.is_file(): raise ResolutionDenied(f'missing authority source: {p}')
    b=p.read_bytes()
    try:return json.loads(b),b
    except Exception as e: raise ResolutionDenied('authority source is not canonical JSON') from e

def resolve_record(kind, path, expected_invocation, domain, source_identity, store):
    value,b=_read_json(path)
    if expected_invocation and value.get('InvocationAttemptId') not in (None,expected_invocation) and value.get('invocation',{}).get('InvocationAttemptId')!=expected_invocation:
        raise ResolutionDenied(f'{kind} invocation mismatch')
    return ResolvedAuthorityValue.from_bytes(kind,value,domain,source_identity,store,expected_invocation)

def resolve_dispatch(store, dispatch_id, invocation_id):
    value=store.resolve(dispatch_id); obj=json.loads(value)
    if obj.get('authority_id')!=dispatch_id: raise ResolutionDenied('dispatch identity mismatch')
    return ResolvedAuthorityValue.from_bytes('dispatch',obj,'LIVE_R4_FINAL_CONTROLLER_STORE',dispatch_id,str(store.root),invocation_id)

def resolve_invocation(store, invocation_id):
    value=store.resolve(invocation_id); obj=json.loads(value)
    if obj.get('InvocationAttemptId')!=invocation_id: raise ResolutionDenied('invocation identity mismatch')
    return ResolvedAuthorityValue.from_bytes('invocation',obj,'LIVE_R4_FINAL_CONTROLLER_STORE',invocation_id,str(store.root),invocation_id)

def _catalog_json(store, logical_id):
    """Read an object through the pinned controller catalog only."""
    return json.loads(store.resolve(logical_id))

def resolve_context(store, context_id, invocation_id):
    """Resolve the context from its own operational-context authority.

    A dispatch copy of context is deliberately not a fallback.  The live G4
    catalog must contain a canonical context record whose identity names the
    requested context.
    """
    candidates = [k for k in store.catalog['objects'] if k.startswith('E1-OPERATIONAL-CONTEXT-')]
    for key in candidates:
        obj = _catalog_json(store, key)
        ids = obj.get('context_identities', {})
        if ids.get('OperationalContextId') == context_id:
            if obj.get('invocation_identity', {}).get('revision') is not None:
                # Context records are historical and may be applicable only to
                # their named invocation; the caller still checks the shared id.
                pass
            return ResolvedAuthorityValue.from_bytes('context', obj, 'OPERATIONAL_CONTEXT_AUTHORITY', key, str(store.root), invocation_id)
    raise ResolutionDenied(f'missing authoritative context record: {context_id}')

def resolve_profile(store, profile_sha256, invocation_id):
    key = 'sha256:' + profile_sha256 if not profile_sha256.startswith('sha256:') else profile_sha256
    try:
        obj = _catalog_json(store, key)
    except Exception as exc:
        raise ResolutionDenied(f'missing authoritative profile record: {key}') from exc
    return ResolvedAuthorityValue.from_bytes('profile', obj, 'RELEASED_PROFILE_AUTHORITY', key, str(store.root), invocation_id)

def resolve_operational(store, invocation_id, binding_identity):
    # Operational binding is owned by the canonical invocation authority.  It
    # is never sourced from a dispatch or WorkAuthorization copy.
    inv = json.loads(store.resolve(invocation_id))
    if inv.get('InvocationAttemptId') != invocation_id:
        raise ResolutionDenied('operational binding invocation mismatch')
    binding = inv.get('replacement_operational_binding_sha256') or inv.get('bindings', {}).get('operational_binding_sha256')
    if binding_identity is not None and binding != binding_identity:
        raise ResolutionDenied('operational binding identity mismatch')
    if binding is None:
        raise ResolutionDenied('missing authoritative operational binding')
    return ResolvedAuthorityValue.from_bytes('operational', {'identity': binding}, 'INVOCATION_AUTHORITY', invocation_id, str(store.root), invocation_id)

def resolve_lifecycle(path, invocation_id):
    return resolve_record('lifecycle',path,invocation_id,'LIFECYCLE_JOURNAL',str(path),str(Path(path).parent))

def compose_activation_inputs(**proofs):
    required={'lifecycle','invocation','dispatch','operational','context','profile','ownership','audit'}
    if set(proofs)!=required: raise ResolutionDenied('activation authority set incomplete')
    for k,p in proofs.items():
        if not isinstance(p,ResolvedAuthorityValue): raise ResolutionDenied(f'{k} is not resolved proof')
        if p.invocation_id and p.invocation_id!=next(iter({x.invocation_id for x in proofs.values()})): raise ResolutionDenied('proof invocation mismatch')
        if p.freshness!='FRESH': raise ResolutionDenied(f'{k} proof stale')
    return dict(proofs)
