"""G01 native parentless GENESIS event representation and validation."""
import hashlib
from . import codec, model as m

class GenesisEventError(m.PlannerError): pass


def genesis_event_identity(event: m.GenesisEvent) -> m.ArtifactIdentity:
    validate_genesis_event(event)
    body = codec._wire(event)
    body.pop('identity', None)
    return m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY, 'planner-genesis-event-v1', hashlib.sha256(codec.canonical_bytes(body)).hexdigest())


def validate_genesis_event(event):
    if not isinstance(event, m.GenesisEvent): raise GenesisEventError('GENESIS_TYPE')
    if event.event_type != 'GENESIS': raise GenesisEventError('GENESIS_EVENT_TYPE')
    if event.parent_event_id is not None: raise GenesisEventError('GENESIS_PARENT_FORBIDDEN')
    if event.authority_class is not m.AuthorityClass.GENESIS: raise GenesisEventError('GENESIS_AUTHORITY_CLASS')
    if event.pre_genesis_history != 'NOT_REPRESENTED': raise GenesisEventError('GENESIS_HISTORY_BOUNDARY')
    for value, code in ((event.scope,'GENESIS_SCOPE'),(event.lineage,'GENESIS_LINEAGE')):
        if not value: raise GenesisEventError(code)
    m.validate_provenance(event.provenance)
    return True
