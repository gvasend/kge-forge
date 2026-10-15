"""G02 generic one-root genesis ledger semantics."""
from dataclasses import dataclass
import hashlib
from . import model as m, codec
from .genesis_event import validate_genesis_event, genesis_event_identity, GenesisEventError

class GenesisLedgerError(m.PlannerError): pass

@dataclass(frozen=True)
class GenesisLedger:
    ledger_id: m.ArtifactIdentity
    root: m.ArtifactIdentity
    events: tuple
    append_head: m.ArtifactIdentity
    pre_genesis_history: str = 'NOT_REPRESENTED'

def _ledger_id(genesis):
    return m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY,'planner-genesis-ledger-v1',hashlib.sha256(codec.canonical_bytes(codec._wire(genesis))).hexdigest())

def create_genesis_ledger(genesis):
    validate_genesis_event(genesis); gid=genesis_event_identity(genesis); lid=_ledger_id(genesis)
    root=m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY,'planner-genesis-root-v1',hashlib.sha256(codec.canonical_bytes({'ledger':codec._wire(lid),'genesis':codec._wire(gid),'history':'NOT_REPRESENTED'})).hexdigest())
    return GenesisLedger(lid,root,(genesis,),gid)

def append_child(ledger,event):
    if not isinstance(event,m.ExecutionEvent): raise GenesisLedgerError('ORDINARY_EVENT_REQUIRED')
    if event.parent_event != ledger.append_head: raise GenesisLedgerError('PARENT_MISMATCH')
    if event.sequence != len(ledger.events): raise GenesisLedgerError('SEQUENCE_MISMATCH')
    if any(getattr(x,'event_type',None)=='GENESIS' for x in ledger.events[1:]): raise GenesisLedgerError('MULTIPLE_GENESIS')
    events=ledger.events+(event,)
    root=m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY,'planner-genesis-root-v1',hashlib.sha256(codec.canonical_bytes({'prior':codec._wire(ledger.root),'event':codec._wire(event.identity)})).hexdigest())
    return GenesisLedger(ledger.ledger_id,root,events,event.identity)

def validate_ledger(ledger):
    if not ledger.events or not isinstance(ledger.events[0],m.GenesisEvent): raise GenesisLedgerError('GENESIS_FIRST_REQUIRED')
    validate_genesis_event(ledger.events[0]); gid=genesis_event_identity(ledger.events[0])
    if ledger.append_head != getattr(ledger.events[-1],'identity',gid): raise GenesisLedgerError('HEAD_MISMATCH')
    if ledger.pre_genesis_history!='NOT_REPRESENTED': raise GenesisLedgerError('HISTORY_BOUNDARY')
    for i,e in enumerate(ledger.events[1:],1):
        previous = genesis_event_identity(ledger.events[0]) if i == 1 else ledger.events[i-1].identity
        if not isinstance(e,m.ExecutionEvent) or e.parent_event != previous or e.sequence != i: raise GenesisLedgerError('BROKEN_ANCESTRY')
    return True
