"""Parent-bound E01/E02 operands; no authority issuance or attestation decision."""
from dataclasses import replace
from . import model as m, evidence_attestation as ea, evidence_materializer as em


def bind(request, attestation, binding):
    from .evidence import command_key
    operand = m.EvidenceAttestationOperand(attestation, binding,
        request.expected_bundle, request.expected_snapshot, request.expected_parent_event)
    m.validate_types(operand, m.EvidenceAttestationOperand)
    request = replace(request, attestation_operand=operand)
    return replace(request, command_key=command_key(request))


def validate(snapshot, request, contract, supplied=None):
    """Verify the recorded operand. Replay verifies history, never materializes E02."""
    operand = request.attestation_operand
    if operand is None:
        return supplied  # legacy preflight/API remains available
    m.validate_types(operand, m.EvidenceAttestationOperand)
    if (operand.expected_bundle, operand.expected_snapshot, operand.expected_parent_event) != (
        request.expected_bundle, request.expected_snapshot, request.expected_parent_event):
        raise m.PlannerError('ATTESTATION_PRE_STATE')
    t, b = operand.attestation, operand.binding
    if supplied is not None and supplied != t:
        raise m.PlannerError('ATTESTATION_SUBSTITUTION')
    args = dict(vars(t)); args.pop('attestation_id')
    if ea.identity(**args) != t.attestation_id:
        raise m.PlannerError('EVIDENCE_ATTESTATION_ID')
    reqs = tuple(r for r in snapshot.evidence_requirements if r.id in contract.requirements)
    if not reqs or any(r.proposition != b.proposition for r in reqs):
        raise m.PlannerError('ATTESTATION_PROPOSITION')
    em.validate_binding(b, request.entity, t.content, t.proposition,
        request.admission.producer, t.attestor, request.admission.authentication,
        request.gate, snapshot.context)
    if (b.semantic_evidence_id, b.content_id, b.attestor, b.attestor_predicate) != (
        t.semantic_evidence, t.content, t.attestor, t.source_predicate):
        raise m.PlannerError('ATTESTATION_BINDING')
    ea.validate(t, entity=request.entity, contract=contract, gate=request.gate,
        context=snapshot.context, source_pin=b.source_pin,
        semantic_evidence=b.semantic_evidence_id, content=b.content_id,
        proposition=b.proposition, attestor=b.attestor)
    return t


def trusted_binding(request, expected):
    """The boundary owner supplies its presealed E01 expectation, not a bool.

    expected is a trusted input, analogous to the trusted parent bundle: do not
    derive it from an untrusted request. The command embeds it for historical
    verification; the live boundary must independently pin the same value.
    """
    if request.attestation_operand is None:
        if expected is not None:
            raise m.PlannerError('MISSING_ATTESTATION_OPERAND')
        return
    if type(expected) is not m.SemanticNativeBinding:
        raise m.PlannerError('TRUSTED_EVIDENCE_BINDING_REQUIRED')
    m.validate_types(expected, m.SemanticNativeBinding)
    if expected != request.attestation_operand.binding:
        raise m.PlannerError('TRUSTED_EVIDENCE_BINDING_MISMATCH')


def receipt_oracle(snapshot, request):
    """Expected RECEIVED-only delta, sealed before native private execution.

    This is a postcondition oracle, never an execution or publication path.
    E03 permits the derived ActionStatus projection, but no validation, proof,
    reentry, result, knowledge, configuration or root/slot advancement. Control
    is derived from this expected post-state; it need not equal pre-control.
    """
    from . import core
    m.validate_model(snapshot)
    m.validate_types(request, m.EvidenceSourceAdmission)
    gate = next((g for g in snapshot.external_gates if g.id == request.gate), None)
    if gate is None or gate.stage is not m.ExternalStage.WAITING_FOR_EXTERNAL_EVIDENCE:
        raise m.PlannerError('NO_ACTIVE_GATE')
    received = replace(request.entity, validated=False,
                       validation=m.ValidationState.NOT_EVALUATED)
    admission = request.admission
    if request.attestation_operand is not None:
        admission = replace(admission,
            attestation=request.attestation_operand.attestation.attestation_id)
    receipt_gate = replace(gate, pending=received.id,
        stage=m.ExternalStage.EVIDENCE_RECEIVED,
        history=(gate.history or (gate.stage,)) + (m.ExternalStage.EVIDENCE_RECEIVED,))
    return replace(snapshot,
        entities=snapshot.entities + (received,),
        receipt_admissions=snapshot.receipt_admissions + (admission,),
        statuses=core.recompute(snapshot).statuses,
        external_gates=tuple(receipt_gate if g.id == gate.id else g
                             for g in snapshot.external_gates))


def check_receipt_postcondition(expected, actual):
    """Compare exact canonical delta and its native computed control/readiness.

    Canonical identity handles native-declared unordered collections; no
    presentation-order equality is imposed. All unchanged domain fields are
    protected, so this cannot authorize receipt-to-validation/proof/reentry.
    """
    from . import codec, core
    m.validate_model(actual)
    if codec.snapshot_id(actual) != codec.snapshot_id(expected):
        raise m.PlannerError('RECEIPT_POSTCONDITION')
    if core.recompute(actual) != core.recompute(expected):
        raise m.PlannerError('RECEIPT_COMPUTATION_POSTCONDITION')
