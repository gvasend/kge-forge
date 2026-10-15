"""Explicit receipt/validation/proof/reentry state machine."""
from dataclasses import dataclass
from enum import Enum
from . import model as m

class EvidenceStage(Enum):
    ABSENT='ABSENT'; RECEIVED='RECEIVED'; VALIDATED='VALIDATED'; PROVED='PROVED'; REENTRY_ELIGIBLE='REENTRY_ELIGIBLE'; REENTER_COMPLETED='REENTER_COMPLETED'; VALIDATION_REJECTED='VALIDATION_REJECTED'

@dataclass(frozen=True)
class Lifecycle:
    stage: EvidenceStage
    evidence: m.EntityId
    validation_id: object = None
    proof_id: object = None

def received(evidence):
    return Lifecycle(EvidenceStage.RECEIVED, evidence)

def validate(state, validation_id, passed):
    if state.stage is not EvidenceStage.RECEIVED: raise m.PlannerError('VALIDATION_STAGE')
    return Lifecycle(EvidenceStage.VALIDATED if passed else EvidenceStage.VALIDATION_REJECTED,
                     state.evidence, validation_id)

def prove(state, proof_id):
    if state.stage is not EvidenceStage.VALIDATED: raise m.PlannerError('PROOF_REQUIRES_VALIDATION')
    return Lifecycle(EvidenceStage.PROVED, state.evidence, state.validation_id, proof_id)

def reentry(state, eligible):
    if state.stage is not EvidenceStage.PROVED or not eligible: raise m.PlannerError('REENTRY_NOT_ELIGIBLE')
    return Lifecycle(EvidenceStage.REENTRY_ELIGIBLE, state.evidence, state.validation_id, state.proof_id)

def complete_reenter(state):
    if state.stage is not EvidenceStage.REENTRY_ELIGIBLE: raise m.PlannerError('REENTER_STAGE')
    return Lifecycle(EvidenceStage.REENTER_COMPLETED, state.evidence, state.validation_id, state.proof_id)
