"""G03 trusted binding of qualified state, GenesisEvent and genesis ledger."""
from dataclasses import dataclass, replace
import hashlib
from . import model as m, codec
from .genesis_event import validate_genesis_event, genesis_event_identity
from .genesis_ledger import GenesisLedger, validate_ledger

class GenesisBundleError(m.PlannerError): pass

GENESIS_BUNDLE_SCHEMA = 'PLANNER-GENESIS-BUNDLE-1'

@dataclass(frozen=True)
class GenesisBoundBundle:
    source_snapshot: m.ArtifactIdentity
    source_state: m.ArtifactIdentity
    current: m.Snapshot
    genesis_event: m.GenesisEvent
    ledger: GenesisLedger
    authority: m.ArtifactIdentity
    scope: str
    lineage: str
    provenance: m.Provenance
    trusted: bool = False
    pre_genesis_history: str = 'NOT_REPRESENTED'

def bundle_identity(bundle):
    body={'source_snapshot':codec._wire(bundle.source_snapshot),'source_state':codec._wire(bundle.source_state),'genesis':codec._wire(genesis_event_identity(bundle.genesis_event)),'ledger':codec._wire(bundle.ledger.ledger_id),'root':codec._wire(bundle.ledger.root),'head':codec._wire(bundle.ledger.append_head),'authority':codec._wire(bundle.authority),'scope':bundle.scope,'lineage':bundle.lineage,'history':bundle.pre_genesis_history}
    return m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY,'planner-genesis-bundle-v1',hashlib.sha256(codec.canonical_bytes(body)).hexdigest())

def bind(snapshot, genesis, ledger, authority, provenance):
    validate_genesis_event(genesis); validate_ledger(ledger)
    sid=codec.snapshot_id(snapshot)
    if genesis.source_snapshot_id != sid or genesis.source_state_id != sid: raise GenesisBundleError('SNAPSHOT_BINDING')
    if genesis.genesis_authority_id != authority or genesis.scope != snapshot.context.scope or genesis.lineage != snapshot.context.lineage: raise GenesisBundleError('BINDING_MISMATCH')
    if ledger.events[0] != genesis or ledger.append_head != genesis_event_identity(genesis): raise GenesisBundleError('LEDGER_BINDING')
    b=GenesisBoundBundle(sid,sid,snapshot,genesis,ledger,authority,genesis.scope,genesis.lineage,provenance,False)
    return replace(b,trusted=trust(b))

def trust(bundle):
    if bundle.pre_genesis_history!='NOT_REPRESENTED' or not bundle.scope or not bundle.lineage: return False
    try: validate_genesis_event(bundle.genesis_event); validate_ledger(bundle.ledger)
    except Exception: return False
    current_id = codec.snapshot_id(bundle.current)
    if bundle.source_snapshot != codec.snapshot_id(bundle.current) and bundle.ledger.events[-1:] and \
       isinstance(bundle.ledger.events[-1], m.ExecutionEvent):
        state_bound = bundle.ledger.events[-1].after_snapshot == current_id
    else:
        state_bound = bundle.source_snapshot == current_id and bundle.source_state == current_id
    return state_bound and bundle.genesis_event.genesis_authority_id == bundle.authority and bundle.ledger.events[0] == bundle.genesis_event

def append_child(bundle,event):
    if not bundle.trusted: raise GenesisBundleError('UNTRUSTED_BUNDLE')
    from .genesis_ledger import append_child
    ledger=append_child(bundle.ledger,event); return replace(bundle,ledger=ledger,trusted=trust(replace(bundle,ledger=ledger)))

def encode_bundle(bundle):
    """Canonical persistence envelope for the generic genesis bundle."""
    validate_genesis_bundle(bundle)
    value = {
        'schema': GENESIS_BUNDLE_SCHEMA,
        'source_snapshot': codec._wire(bundle.source_snapshot),
        'source_state': codec._wire(bundle.source_state),
        'current': codec._wire(bundle.current),
        'genesis_event': codec._wire(bundle.genesis_event),
        'ledger': {
            'ledger_id': codec._wire(bundle.ledger.ledger_id),
            'root': codec._wire(bundle.ledger.root),
            'events': [codec._wire(e) for e in bundle.ledger.events],
            'append_head': codec._wire(bundle.ledger.append_head),
            'pre_genesis_history': bundle.ledger.pre_genesis_history,
        },
        'authority': codec._wire(bundle.authority),
        'scope': bundle.scope, 'lineage': bundle.lineage,
        'provenance': codec._wire(bundle.provenance),
        'trusted': bundle.trusted,
        'pre_genesis_history': bundle.pre_genesis_history,
    }
    return codec.canonical_bytes(value)

def decode_bundle(data):
    value = codec.parse_json(data)
    if value.get('schema') != GENESIS_BUNDLE_SCHEMA:
        raise GenesisBundleError('BUNDLE_SCHEMA')
    ledger_value = value['ledger']
    ledger = GenesisLedger(
        codec._unwire(ledger_value['ledger_id']), codec._unwire(ledger_value['root']),
        tuple(codec._unwire(e) for e in ledger_value['events']),
        codec._unwire(ledger_value['append_head']), ledger_value['pre_genesis_history'])
    bundle = GenesisBoundBundle(
        codec._unwire(value['source_snapshot']), codec._unwire(value['source_state']),
        codec._unwire(value['current']), codec._unwire(value['genesis_event']), ledger,
        codec._unwire(value['authority']), value['scope'], value['lineage'],
        codec._unwire(value['provenance']), value['trusted'], value['pre_genesis_history'])
    validate_genesis_bundle(bundle)
    return bundle

def validate_genesis_bundle(bundle):
    if not isinstance(bundle, GenesisBoundBundle):
        raise GenesisBundleError('BUNDLE_TYPE')
    if not trust(bundle):
        raise GenesisBundleError('BUNDLE_UNTRUSTED')
    return True

def begin_event_lineage(snapshot, authorization_identity, contract, provenance):
    """Compose G01/G02/G03 into an atomic in-memory genesis transaction."""
    if not isinstance(authorization_identity, m.ArtifactIdentity): raise GenesisBundleError('AUTHORIZATION_REQUIRED')
    if snapshot.context is None or snapshot.context.scope != contract.scope or snapshot.context.lineage != contract.lineage: raise GenesisBundleError('CONTEXT_MISMATCH')
    if codec.snapshot_id(snapshot) != contract.source_snapshot: raise GenesisBundleError('SNAPSHOT_NOT_COVERED')
    authority=m.ArtifactIdentity(m.IdentityKind.AUTHORITY_IDENTITY,'genesis-authority-v1',hashlib.sha256(codec.canonical_bytes({'authorization':codec._wire(authorization_identity),'snapshot':codec._wire(codec.snapshot_id(snapshot)),'scope':contract.scope,'lineage':contract.lineage})).hexdigest())
    event=m.GenesisEvent('GENESIS',codec.snapshot_id(snapshot),codec.snapshot_id(snapshot),authority,m.AuthorityClass.GENESIS,contract.scope,contract.lineage,provenance)
    from .genesis_ledger import create_genesis_ledger
    ledger=create_genesis_ledger(event)
    return bind(snapshot,event,ledger,authority,provenance)
