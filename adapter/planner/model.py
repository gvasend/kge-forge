"""Immutable planner slice and provenance/persistence types; no authority issuance."""
from typing import Tuple
from dataclasses import dataclass, fields, is_dataclass
from enum import Enum
import re
from typing import get_args, get_origin, get_type_hints, Union, Optional


class PlannerError(ValueError):
    pass


class IdentityKind(Enum):
    CONTENT_IDENTITY = 'CONTENT_IDENTITY'
    AUTHORITY_IDENTITY = 'AUTHORITY_IDENTITY'
    INSTANCE_IDENTITY = 'INSTANCE_IDENTITY'
    RELEASE_IDENTITY = 'RELEASE_IDENTITY'
    CANONICAL_OBJECT_IDENTITY = 'CANONICAL_OBJECT_IDENTITY'
    WORKAUTHORIZATION_ID = 'WORKAUTHORIZATION_ID'
    BINDING_DIGEST = 'BINDING_DIGEST'


@dataclass(frozen=True, order=True)
class Identifier:
    value: str

    def __post_init__(self):
        if type(self.value) is not str or not self.value or self.value.strip() != self.value:
            raise PlannerError('invalid canonical identifier')


@dataclass(frozen=True, order=True)
class ActionId(Identifier):
    pass


@dataclass(frozen=True, order=True)
class ConditionId(Identifier):
    pass


@dataclass(frozen=True, order=True)
class SlotId(Identifier):
    pass


@dataclass(frozen=True, order=True)
class KnowledgeId(Identifier):
    pass


@dataclass(frozen=True, order=True)
class AssertionId(Identifier):
    pass


@dataclass(frozen=True, order=True)
class EntityId(Identifier):
    pass


@dataclass(frozen=True, order=True)
class PredicateId(Identifier):
    pass


@dataclass(frozen=True)
class ArtifactIdentity:
    kind: IdentityKind
    namespace: str
    sha256: str

    def __post_init__(self):
        if type(self.kind) is not IdentityKind or type(self.namespace) is not str or not self.namespace:
            raise PlannerError('identity kind/domain required')
        if type(self.sha256) is not str or not re.fullmatch('[0-9a-f]{64}', self.sha256):
            raise PlannerError('invalid SHA-256')


@dataclass(frozen=True)
class Provenance:
    path: str
    identity: ArtifactIdentity
    section: str
    excerpt: str
    method: str
    scope: str


class ActionState(Enum):
    ACTION_ELIGIBLE = 'ACTION_ELIGIBLE'
    ACTIONABLE = 'ACTIONABLE'
    SELECTED = 'SELECTED'
    COMPLETED = 'COMPLETED'
    BLOCKED = 'BLOCKED'
    WAITING = 'WAITING'


class ActionResult(Enum):
    PASS = 'PASS'
    FAIL = 'FAIL'
    BLOCKED = 'BLOCKED'
    AUTHORITY_REQUIRED = 'AUTHORITY_REQUIRED'
    EXTERNAL_GATE_REQUIRED = 'EXTERNAL_GATE_REQUIRED'


class OperationClass(Enum):
    SOURCE_ACQUISITION = 'SOURCE_ACQUISITION'
    DETERMINISTIC_VALIDATION = 'DETERMINISTIC_VALIDATION'
    DETERMINISTIC_CONSTRUCTION = 'DETERMINISTIC_CONSTRUCTION'
    DETERMINISTIC_MAPPING = 'DETERMINISTIC_MAPPING'
    IMPLEMENTATION_PREPARATION = 'IMPLEMENTATION_PREPARATION'
    SEMANTIC_EVALUATION = 'SEMANTIC_EVALUATION'
    SEMANTIC_RESOLUTION = 'SEMANTIC_RESOLUTION'
    ARCHITECT_PREPARATION = 'ARCHITECT_PREPARATION'
    RUNTIME_EXPERIMENT = 'RUNTIME_EXPERIMENT'
    GOVERNED_OPERATION = 'GOVERNED_OPERATION'
    ARCHITECT_AUTHORITY = 'ARCHITECT_AUTHORITY'
    ARCHITECT_CONTRACT_DECISION = 'ARCHITECT_CONTRACT_DECISION'
    IMPLEMENTATION_REPAIR = 'IMPLEMENTATION_REPAIR'
    VALIDATOR_IMPLEMENTATION = 'VALIDATOR_IMPLEMENTATION'
    FACT_ACQUISITION = 'FACT_ACQUISITION'
    DECISION_INPUT_ACQUISITION = 'DECISION_INPUT_ACQUISITION'
    OTHER = 'OTHER'


class ActionStage(Enum):
    DEFAULT = 'DEFAULT'
    DECISION_PREPARATION = 'DECISION_PREPARATION'


class Relation(Enum):
    REQUIRES = 'REQUIRES'
    PRODUCED_BY = 'PRODUCED_BY'
    DERIVED_FROM = 'DERIVED_FROM'
    AUTHORIZED_BY = 'AUTHORIZED_BY'
    VALIDATED_BY = 'VALIDATED_BY'
    CONSUMED_BY = 'CONSUMED_BY'
    EVIDENCED_BY = 'EVIDENCED_BY'
    BINDS = 'BINDS'
    APPLIES_TO = 'APPLIES_TO'
    HAS_SLOT = 'HAS_SLOT'
    HAS_IDENTITY_TYPE = 'HAS_IDENTITY_TYPE'
    PROVEN_BY = 'PROVEN_BY'
    SATISFIED_BY = 'SATISFIED_BY'
    CORRESPONDS_TO = 'CORRESPONDS_TO'


class EntityKind(Enum):
    SOURCE = 'SOURCE'
    PRODUCER = 'PRODUCER'
    MAPPING = 'MAPPING'
    VALIDATOR = 'VALIDATOR'
    AUTHORITY = 'AUTHORITY'
    VALUE = 'VALUE'
    EVIDENCE = 'EVIDENCE'
    TARGET = 'TARGET'


class AuthorityClass(Enum):
    CONSTRUCT = 'CONSTRUCT'
    ISSUE = 'ISSUE'
    USE = 'USE'
    RELEASE = 'RELEASE'
    EXPAND = 'EXPAND'
    IMPLEMENT_TEST = 'IMPLEMENT_TEST'
    DECIDE = 'DECIDE'
    ATTEST = 'ATTEST'


class ValidatorRule(Enum):
    PURE_IDENTITY_MATCH = 'PURE_IDENTITY_MATCH'
    EFFECTING_ONLY = 'EFFECTING_ONLY'


class PredicateKind(Enum):
    ALL = 'ALL'
    ANY = 'ANY'
    SOURCE_IDENTITY = 'SOURCE_IDENTITY'
    TYPED_EQUAL = 'TYPED_EQUAL'
    AUTHORITY = 'AUTHORITY'
    ACTION_COMPLETED = 'ACTION_COMPLETED'
    CONDITION_SATISFIED = 'CONDITION_SATISFIED'
    KNOWLEDGE_ACCEPTED = 'KNOWLEDGE_ACCEPTED'
    PRODUCER_AVAILABLE = 'PRODUCER_AVAILABLE'
    MAPPING_AVAILABLE = 'MAPPING_AVAILABLE'
    CONSUMER_CHECK = 'CONSUMER_CHECK'
    EVIDENCE = 'EVIDENCE'
    DOSSIER_COMPLETE = 'DOSSIER_COMPLETE'
    RECEIPT_COMPLETE = 'RECEIPT_COMPLETE'
    UNSUPPORTED = 'UNSUPPORTED'
    EVIDENCE_OBLIGATION = 'EVIDENCE_OBLIGATION'


class ProofState(Enum):
    PROVED = 'PROVED'
    DISPROVED = 'DISPROVED'
    UNKNOWN = 'UNKNOWN'


@dataclass(frozen=True)
class EvaluationContext:
    scope: str
    lineage: str
    generation: str
    tick: int
    allowed_effects: Tuple['EffectClass', ...] = ()


@dataclass(frozen=True)
class Predicate:
    id: PredicateId
    kind: PredicateKind
    operands: Tuple[PredicateId, ...] = ()
    entity: Optional[EntityId] = None
    other: Optional[EntityId] = None
    expected: Optional[ArtifactIdentity] = None
    permission: Optional[AuthorityClass] = None
    action: Optional[ActionId] = None
    condition: Optional[ConditionId] = None
    knowledge: Optional[KnowledgeId] = None
    obligation: Optional['EvidenceId'] = None
    # Explicit missing fact, never an unresolved identifier or accepted proof.
    unavailable: Optional[str] = None
    required_outcome: Optional[ActionResult] = None




class EffectClass(Enum):
    NON_EFFECTING = 'NON_EFFECTING'
    QUALIFICATION_EFFECT_ONLY = 'QUALIFICATION_EFFECT_ONLY'
    PRODUCTION_EFFECT = 'PRODUCTION_EFFECT'


class ConditionState(Enum):
    STALE = 'STALE'
    UNRESOLVED = 'UNRESOLVED'
    SATISFIED = 'SATISFIED'
    DISPROVED = 'DISPROVED'


class SlotState(Enum):
    STALE = 'STALE'
    UNRESOLVED = 'UNRESOLVED'
    RESOLVED = 'RESOLVED'


class KnowledgeState(Enum):
    UNKNOWN = 'UNKNOWN'
    KNOWN_INCOMPLETE = 'KNOWN_INCOMPLETE'
    KNOWN_COMPLETE = 'KNOWN_COMPLETE'


class GateKind(Enum):
    ACTION_COMPLETED = 'ACTION_COMPLETED'
    CONDITION_SATISFIED = 'CONDITION_SATISFIED'


@dataclass(frozen=True)
class Gate:
    kind: GateKind
    target: Union[ActionId, ConditionId]


class ValidationState(Enum):
    ACCEPTED = 'ACCEPTED'
    STALE = 'STALE'


class ValidationOutcome(Enum):
    PASS = 'PASS'
    FAIL = 'FAIL'
    STALE = 'STALE'
    UNEVALUATED = 'UNEVALUATED'


@dataclass(frozen=True)
class InformationModel:
    action: ActionId
    alternatives: Tuple[str, ...]
    partitions: Tuple[Tuple[str, ...], ...]
    provenance: Provenance
    validation: ValidationState = ValidationState.ACCEPTED


@dataclass(frozen=True)
class GraphEntity:
    id: EntityId
    kind: EntityKind
    identity: ArtifactIdentity
    provenance: Provenance
    scope: str
    lineage: str
    generation: str
    valid_until: int
    produced: bool = True
    validated: bool = True
    validation: ValidationState = ValidationState.ACCEPTED
    permissions: Tuple[AuthorityClass, ...] = ()
    target: Optional[ArtifactIdentity] = None
    consumed: bool = False
    validator: Optional[ValidatorRule] = None
    decision: Optional[ActionId] = None
    choice: Optional[str] = None


@dataclass(frozen=True)
class GraphAssertion:
    id: AssertionId
    provenance: Provenance
    depends_on: Tuple[AssertionId, ...] = ()
    validation: ValidationState = ValidationState.ACCEPTED
    relation: Optional[Relation] = None
    subject: Optional[Union[ActionId, ConditionId, SlotId, EntityId]] = None
    object: Optional[Union[ActionId, ConditionId, SlotId, EntityId]] = None
    ordering_justification: str = ''


@dataclass(frozen=True)
class RootCondition:
    id: ConditionId
    state: ConditionState
    evidence: Tuple[AssertionId, ...] = ()
    predicate: Optional[PredicateId] = None


class ValueType(Enum):
    NON_IDENTITY_VALUE = 'NON_IDENTITY_VALUE'
    UNDEFINED_IDENTITY_OR_VALUE_TYPE = 'UNDEFINED_IDENTITY_OR_VALUE_TYPE'


@dataclass(frozen=True)
class ValueSlot:
    id: SlotId
    state: SlotState
    required_type: Union[IdentityKind, ValueType]
    evidence: Tuple[AssertionId, ...] = ()
    value: Optional[EntityId] = None
    requirements: Tuple[PredicateId, ...] = ()
    root_requirements: Tuple[ConditionId, ...] = ()


@dataclass(frozen=True)
class KnowledgeRecord:
    id: KnowledgeId
    state: KnowledgeState
    statement: str
    provenance: Provenance
    evidence: Tuple[AssertionId, ...] = ()
    validation: ValidationState = ValidationState.ACCEPTED
    producer: Optional[ActionId] = None
    outcome: Optional[ActionResult] = None


class DecisionStage(Enum):
    SEMANTIC_GAP_IDENTIFIED = 'SEMANTIC_GAP_IDENTIFIED'
    DECISION_INPUTS_REQUIRED = 'DECISION_INPUTS_REQUIRED'
    DECISION_INPUT_ACQUISITION = 'DECISION_INPUT_ACQUISITION'
    DECISION_DOSSIER_READY = 'DECISION_DOSSIER_READY'
    DECISION_READY = 'DECISION_READY'
    DECISION_RECORDED = 'DECISION_RECORDED'
    DOWNSTREAM_REEVALUATION = 'DOWNSTREAM_REEVALUATION'


class DecisionReadiness(Enum):
    DECISION_READY = 'DECISION_READY'
    FACT_BLOCKED = 'FACT_BLOCKED'
    SEMANTICALLY_INCOMPLETE = 'SEMANTICALLY_INCOMPLETE'
    STALE = 'STALE'


class DossierCheck(Enum):
    QUESTION_SCOPE = 'QUESTION_SCOPE'
    SOURCE_PROVENANCE = 'SOURCE_PROVENANCE'
    CONCRETE_ALTERNATIVES = 'CONCRETE_ALTERNATIVES'
    ASSUMPTIONS_CONSEQUENCES = 'ASSUMPTIONS_CONSEQUENCES'
    AUTHORITY_BOUNDARY = 'AUTHORITY_BOUNDARY'
    DOWNSTREAM_QUALIFICATION = 'DOWNSTREAM_QUALIFICATION'
    NO_INVENTED_FACTS = 'NO_INVENTED_FACTS'
    DECISION_FACTS_COMPLETE = 'DECISION_FACTS_COMPLETE'
    INDEPENDENT_VALIDATION = 'INDEPENDENT_VALIDATION'

# The E2 reconciliation identifies these as the only dossier-level checks
# with an authoritative native proposition.  The remaining enum members are
# retained for historical fixture compatibility and are enforced at their
# rehomed qualification/governance layers.
SUPPORTED_DOSSIER_CHECKS = frozenset({
    DossierCheck.QUESTION_SCOPE,
    DossierCheck.SOURCE_PROVENANCE,
    DossierCheck.CONCRETE_ALTERNATIVES,
    DossierCheck.AUTHORITY_BOUNDARY,
    DossierCheck.DECISION_FACTS_COMPLETE,
    DossierCheck.INDEPENDENT_VALIDATION,
})


class HumanRouting(Enum):
    RUNNABLE = 'RUNNABLE'
    HUMAN_HANDOFF = 'HUMAN_HANDOFF'
    NO_INTERNAL_ACTION = 'NO_INTERNAL_ACTION'  # P05 classifies global exhaustion.


@dataclass(frozen=True)
class DecisionCheck:
    kind: DossierCheck
    predicate: PredicateId
    provenance: Provenance


@dataclass(frozen=True)
class DecisionDossier:
    decision: ActionId
    provenance: Provenance
    question: str
    scope: str
    alternatives: Tuple[str, ...]
    checks: Tuple[DecisionCheck, ...]
    required_facts: Tuple[PredicateId, ...]
    deferred_downstream_facts: Tuple[str, ...]
    authority_granted_if_approved: str
    authority_excluded: str
    validation: ValidationState = ValidationState.ACCEPTED


@dataclass(frozen=True)
class ValidationInstance:
    """Typed result of an independently evaluated dossier validation."""
    predicate: PredicateId
    proposition: str
    dossier: ArtifactIdentity
    inputs: Tuple[ArtifactIdentity, ...]
    result: ValidationOutcome
    scope: str
    lineage: str
    currentness: ValidationState
    provenance: Provenance


@dataclass(frozen=True)
class Decision:
    action: ActionId
    semantic_action: Optional[ActionId]
    input_action: Optional[ActionId]
    external_input: str
    stage: DecisionStage
    provenance: Provenance
    dossier: Optional[DecisionDossier] = None
    history: Tuple[DecisionStage, ...] = ()
    depends_on: Tuple[ActionId, ...] = ()
    interferes_with: Tuple[ActionId, ...] = ()
    downstream: Tuple[ActionId, ...] = ()
    recorded_choice: Optional[str] = None
    record: Optional[EntityId] = None


@dataclass(frozen=True)
class Action:
    id: ActionId
    operation: OperationClass
    effect: EffectClass
    prerequisites: Tuple[Gate, ...]
    source: Provenance
    # Reviewed bounded result contract, not domain satisfaction criteria.
    accepted_inventory: Tuple[KnowledgeRecord, ...]
    evidence: Tuple[AssertionId, ...] = ()
    requirements: Tuple[PredicateId, ...] = ()
    authority: Optional[PredicateId] = None
    stage: ActionStage = ActionStage.DEFAULT
    cost: Optional[int] = None
    cost_unit: str = ''
    pass_model_complete: bool = False
    accepted_result: ActionResult = ActionResult.PASS
    prepared_dossier: Optional[DecisionDossier] = None
    qualification: ValidationState = ValidationState.ACCEPTED


@dataclass(frozen=True)
class ActionStatus:
    id: ActionId
    state: ActionState


@dataclass(frozen=True)
class Snapshot:
    actions: Tuple[Action, ...]
    statuses: Tuple[ActionStatus, ...]
    roots: Tuple[RootCondition, ...]
    slots: Tuple[ValueSlot, ...]
    knowledge: Tuple[KnowledgeRecord, ...]
    assertions: Tuple[GraphAssertion, ...] = ()
    entities: Tuple[GraphEntity, ...] = ()
    predicates: Tuple[Predicate, ...] = ()
    context: Optional[EvaluationContext] = None
    information: Tuple[InformationModel, ...] = ()
    decisions: Tuple[Decision, ...] = ()
    evidence_requirements: Tuple['EvidenceRequirement', ...] = ()
    external_gates: Tuple['ExternalGate', ...] = ()
    receipt_admissions: Tuple['ReceiptAdmission', ...] = ()
    receipt_observations: Tuple['ReceiptObservation', ...] = ()
    boundaries: Tuple['ControlBoundary', ...] = ()
    goals: Tuple['Goal', ...] = ()
    budget_matrices: Tuple['BudgetProofMatrix', ...] = ()
    validation_instances: Tuple[ValidationInstance, ...] = ()


@dataclass(frozen=True)
class SuppliedResult:
    action: ActionId
    result: ActionResult
    knowledge: Tuple[KnowledgeRecord, ...]
    expected_snapshot: Optional[ArtifactIdentity] = None
    dossier: Optional[DecisionDossier] = None


def validate_types(value, expected):
    """Reject loose strings/lists at the typed API boundary, including nested data."""
    origin, args = get_origin(expected), get_args(expected)
    if origin is Union:
        if not any(type(value) is t for t in args):
            raise PlannerError('wrong typed reference')
        validate_types(value, type(value))
    elif origin is tuple:
        if type(value) is not tuple:
            raise PlannerError('immutable tuple required')
        for member in value:
            validate_types(member, args[0])
    elif type(value) is not expected:
        raise PlannerError('wrong type: expected ' + expected.__name__)
    elif is_dataclass(value):
        hints = get_type_hints(expected)
        for field in fields(value):
            validate_types(getattr(value, field.name), hints[field.name])


def unique(items, key):
    keys = [key(item) for item in items]
    if len(keys) != len(set(keys)):
        raise PlannerError('duplicate identifier')


def validate_model(snapshot):
    validate_types(snapshot, Snapshot)
    for collection in (snapshot.actions, snapshot.statuses, snapshot.roots,
                       snapshot.slots, snapshot.knowledge, snapshot.assertions, snapshot.entities, snapshot.predicates):
        unique(collection, lambda item: item.id)
    actions = {a.id for a in snapshot.actions}
    roots = {r.id for r in snapshot.roots}
    if {s.id for s in snapshot.statuses} != actions:
        raise PlannerError('action/status sets differ')
    assertions = {a.id for a in snapshot.assertions}
    owners = (snapshot.actions + snapshot.roots + snapshot.slots + snapshot.knowledge +
              tuple(k for a in snapshot.actions for k in a.accepted_inventory))
    for item in owners:
        unique(item.evidence, lambda ref: ref)
        if any(ref not in assertions for ref in item.evidence):
            raise PlannerError('unknown evidence assertion')
    for assertion in snapshot.assertions:
        validate_provenance(assertion.provenance)
        unique(assertion.depends_on, lambda ref: ref)
        if any(ref not in assertions for ref in assertion.depends_on):
            raise PlannerError('unknown assertion dependency')
    stale = {a.id for a in snapshot.assertions if a.validation is ValidationState.STALE}
    for assertion in snapshot.assertions:
        if stale.intersection(assertion.depends_on) and assertion.validation is not ValidationState.STALE:
            raise PlannerError('dependent assertion left silently current')
    for root in snapshot.roots:
        if stale.intersection(root.evidence) and root.state is not ConditionState.STALE:
            raise PlannerError('root proof is stale')
    for slot in snapshot.slots:
        if stale.intersection(slot.evidence) and slot.state is not SlotState.STALE:
            raise PlannerError('slot proof is stale')
    for record in snapshot.knowledge:
        if stale.intersection(record.evidence) and record.validation is not ValidationState.STALE:
            raise PlannerError('knowledge proof is stale')
    states = {s.id: s.state for s in snapshot.statuses}
    for action in snapshot.actions:
        if (stale.intersection(action.evidence) or
            any(k.validation is ValidationState.STALE or stale.intersection(k.evidence)
                for k in action.accepted_inventory)) and states[action.id] not in (
                    ActionState.BLOCKED, ActionState.WAITING, ActionState.COMPLETED):
            raise PlannerError('action with stale evidence requires a hold')
        validate_provenance(action.source)
        unique(action.accepted_inventory, lambda k: k.id)
        for knowledge in action.accepted_inventory:
            validate_knowledge(knowledge)
            if knowledge.producer is not None and knowledge.producer not in actions:
                raise PlannerError('accepted knowledge has dangling producer')
        for gate in action.prerequisites:
            if gate.kind is GateKind.ACTION_COMPLETED:
                valid = type(gate.target) is ActionId and gate.target in actions
            else:
                valid = type(gate.target) is ConditionId and gate.target in roots
            if not valid:
                raise PlannerError('invalid prerequisite reference')
    for knowledge in snapshot.knowledge:
        validate_knowledge(knowledge)
        if knowledge.producer is not None and knowledge.producer not in actions:
            raise PlannerError('accepted knowledge has dangling producer')
    unique(snapshot.validation_instances, lambda x: x.predicate)
    for instance in snapshot.validation_instances:
        validate_provenance(instance.provenance)
        if not instance.proposition or not instance.scope or not instance.lineage:
            raise PlannerError('incomplete validation instance')
        if instance.dossier.kind is not IdentityKind.CONTENT_IDENTITY:
            raise PlannerError('validation dossier identity must be content identity')
        if instance.result is ValidationOutcome.PASS and instance.currentness is not ValidationState.ACCEPTED:
            raise PlannerError('passing validation must be current')
    validate_p03(snapshot)
    validate_p04(snapshot)
    validate_p05(snapshot)
    if snapshot.budget_matrices or any(k.provenance.method == 'BUDGET_ORACLE_1' for k in snapshot.knowledge):
        from .budget import validate_restored
        validate_restored(snapshot)


def validate_provenance(source):
    validate_types(source, Provenance)
    if source.identity.kind is not IdentityKind.CONTENT_IDENTITY or \
            source.identity.namespace != 'raw-file-sha256':
        raise PlannerError('P01 provenance requires raw content identity')
    if not all((source.path, source.section, source.excerpt, source.method, source.scope)):
        raise PlannerError('incomplete provenance')


def validate_knowledge(record):
    validate_types(record, KnowledgeRecord)
    validate_provenance(record.provenance)
    if (record.producer is None) != (record.outcome is None):
        raise PlannerError('incomplete accepted-outcome knowledge binding')
    if not record.statement or record.state is KnowledgeState.UNKNOWN:
        raise PlannerError('accepted knowledge requires a bounded finding')


class HashProfile(Enum):
    RAW = 'raw-file-sha256'
    PLANNER_JSON = 'planner-json-v1'
    E1_EMBEDDED_JSON = 'e1-embedded-json-v1'


@dataclass(frozen=True)
class ArtifactPin:
    path: str
    identity: ArtifactIdentity
    profile: HashProfile = HashProfile.RAW
    pointer: str = ''


@dataclass(frozen=True)
class ExecutionEvent:
    sequence: int
    parent_snapshot: ArtifactIdentity
    parent_event: Optional[ArtifactIdentity]
    result: Union[SuppliedResult, 'RecordedDecision', 'DecisionReentry', 'ExternalEvent', 'SourceInvalidation', 'EvidenceSourceAdmission']
    after_snapshot: ArtifactIdentity
    identity: ArtifactIdentity
    resume_binding: Optional[ArtifactIdentity] = None


@dataclass(frozen=True)
class PersistenceBundle:
    initial: Snapshot
    events: Tuple[ExecutionEvent, ...]
    current: Snapshot
    sources: Tuple[ArtifactPin, ...]
    policy: ArtifactPin
    policy_version: str = 'E1-SELECTION-1-P01-SUBSET'
    scope: str = 'PARTIAL_HISTORICAL_REPLAY'


def validate_predicate_contracts(snapshot):
    """C01 closed reference contracts. Future outputs are declarations, not facts.

    Unavailable predicates retain their intended kind and a nonempty reason, but
    no operative fields. Replacing them requires a new, valid bound predicate.
    A stale entity remains addressable history; usable() cannot prove it current.
    """
    K = PredicateKind
    contracts = {
        K.ALL: ({'operands'}, set()), K.ANY: ({'operands'}, set()),
        K.DOSSIER_COMPLETE: ({'operands'}, set()), K.RECEIPT_COMPLETE: ({'operands'}, set()),
        K.SOURCE_IDENTITY: ({'entity', 'expected'}, set()),
        K.TYPED_EQUAL: ({'entity', 'expected'}, set()),
        K.AUTHORITY: ({'entity', 'expected', 'permission'}, set()),
        K.ACTION_COMPLETED: ({'action'}, set()),
        K.CONDITION_SATISFIED: ({'condition'}, set()),
        K.KNOWLEDGE_ACCEPTED: ({'knowledge'}, {'expected', 'action', 'required_outcome'}),
        K.PRODUCER_AVAILABLE: ({'entity'}, {'other'}),
        K.MAPPING_AVAILABLE: ({'entity'}, set()),
        K.CONSUMER_CHECK: ({'entity', 'other', 'expected'}, set()),
        K.EVIDENCE: ({'entity'}, set()), K.EVIDENCE_OBLIGATION: ({'obligation'}, set()),
        K.UNSUPPORTED: (set(), set()),
    }
    entities = {e.id: e for e in snapshot.entities}
    predicates = {p.id: p for p in snapshot.predicates}
    known = {k.id: k for k in snapshot.knowledge}
    outputs = {}
    for action in sorted(snapshot.actions, key=lambda item: item.id.value):
        for output in sorted(action.accepted_inventory, key=lambda item: item.id.value):
            if output.id in outputs:
                raise PlannerError('REFERENCE_CONTRACT: duplicate output producer: ' + output.id.value)
            outputs[output.id] = output
            if output.id in known and any(getattr(known[output.id], field) != getattr(output, field)
                                          for field in ('statement', 'provenance', 'producer', 'outcome')):
                raise PlannerError('REFERENCE_CONTRACT: conflicting output binding: ' + output.id.value)
    collections = {'entity': entities, 'other': entities,
                   'action': {a.id for a in snapshot.actions},
                   'condition': {r.id for r in snapshot.roots},
                   'knowledge': set(known) | set(outputs),
                   'obligation': {r.id for r in snapshot.evidence_requirements}}
    operative = ('operands', 'entity', 'other', 'expected', 'permission',
                 'action', 'condition', 'knowledge', 'obligation', 'required_outcome')
    for p in sorted(snapshot.predicates, key=lambda item: item.id.value):
        validate_types(p, Predicate)
        present = {name for name in operative if getattr(p, name) not in (None, ())}
        if p.unavailable is not None:
            if not p.unavailable.strip() or present:
                raise PlannerError('REFERENCE_CONTRACT: unavailable must have reason and no bindings: ' + p.id.value)
            continue
        required, optional = contracts[p.kind]
        if not required <= present or present - required - optional:
            raise PlannerError('REFERENCE_CONTRACT: invalid fields: ' + p.id.value)
        if p.kind is K.KNOWLEDGE_ACCEPTED:
            binding = present & {'expected', 'action', 'required_outcome'}
            if binding and (binding != {'expected', 'action', 'required_outcome'} or
                    p.expected.kind is not IdentityKind.CONTENT_IDENTITY or
                    p.expected.namespace != 'raw-file-sha256'):
                raise PlannerError('REFERENCE_CONTRACT: incomplete/wrong-domain knowledge binding')
        unique(p.operands, lambda ref: ref)
        if any(ref not in predicates for ref in p.operands):
            raise PlannerError('REFERENCE_CONTRACT: missing predicate operand: ' + p.id.value)
        for name, targets in collections.items():
            ref = getattr(p, name)
            if ref is not None and ref not in targets:
                raise PlannerError('REFERENCE_CONTRACT: dangling ' + name + ': ' + p.id.value)
        required_domain = {K.AUTHORITY: EntityKind.AUTHORITY,
                           K.MAPPING_AVAILABLE: EntityKind.MAPPING,
                           K.CONSUMER_CHECK: EntityKind.VALIDATOR,
                           K.EVIDENCE: EntityKind.EVIDENCE}.get(p.kind)
        if required_domain is not None and entities[p.entity].kind is not required_domain:
            raise PlannerError('REFERENCE_CONTRACT: wrong entity domain: ' + p.id.value)
        if p.kind is K.AUTHORITY and entities[p.entity].identity.kind is not IdentityKind.AUTHORITY_IDENTITY:
            raise PlannerError('REFERENCE_CONTRACT: wrong authority identity domain: ' + p.id.value)
        if p.kind is K.PRODUCER_AVAILABLE and p.other is not None and entities[p.other].kind is not EntityKind.PRODUCER:
            raise PlannerError('REFERENCE_CONTRACT: wrong producer domain: ' + p.id.value)
    # Reject finite cyclic definitions at admission, including root proof and
    # receipt-authentication recursion. Iterative traversal avoids recursion limits.
    edges = {p.id: set(p.operands) for p in snapshot.predicates}
    roots = {r.id: r for r in snapshot.roots}
    for p in sorted(snapshot.predicates, key=lambda item: item.id.value):
        if p.condition is not None and roots[p.condition].predicate is not None:
            edges[p.id].add(roots[p.condition].predicate)
        if p.obligation is not None:
            edges[p.id].update(a.authentication for a in snapshot.receipt_admissions
                              if any(c.requirement == p.obligation for c in a.claims))
    pending = set(edges)
    while pending:
        leaves = {ref for ref in pending if not (edges[ref] & pending)}
        if not leaves:
            raise PlannerError('REFERENCE_CONTRACT: cyclic predicate definitions')
        pending -= leaves


def validate_p03(snapshot):
    """Structural checks only. Unknown facts remain UNKNOWN at evaluation."""
    nodes = {item.id for items in (snapshot.actions, snapshot.roots, snapshot.slots, snapshot.entities)
             for item in items}
    predicates = {p.id for p in snapshot.predicates} | {v.predicate for v in snapshot.validation_instances}
    for assertion in snapshot.assertions:
        if assertion.relation is not None:
            if assertion.subject not in nodes or assertion.object not in nodes:
                raise PlannerError('dangling graph relation')
        elif assertion.subject is not None or assertion.object is not None or assertion.ordering_justification:
            raise PlannerError('untyped graph relationship')
    validate_predicate_contracts(snapshot)
    for root in snapshot.roots:
        if root.predicate is not None and root.predicate not in predicates:
            raise PlannerError('missing root predicate')
    for item in snapshot.actions + snapshot.slots:
        unique(item.requirements, lambda x: x)
        if any(ref not in predicates for ref in item.requirements):
            raise PlannerError('missing requirement predicate')
    for action in snapshot.actions:
        if action.authority is not None and action.authority not in predicates:
            raise PlannerError('missing authority predicate')
        if action.cost is not None and (action.cost < 0 or not action.cost_unit):
            raise PlannerError('cost requires nonnegative value and unit')
    roots = {r.id for r in snapshot.roots}
    for slot in snapshot.slots:
        if slot.value is not None and slot.value not in {e.id for e in snapshot.entities}:
            raise PlannerError('REFERENCE_CONTRACT: dangling slot value')
        unique(slot.root_requirements, lambda x: x)
        if any(ref not in roots for ref in slot.root_requirements):
            raise PlannerError('missing slot root dependency')
    for entity in snapshot.entities:
        validate_provenance(entity.provenance)
        unique(entity.permissions, lambda x: x)
    unique(snapshot.information, lambda x: x.action)
    for info in snapshot.information:
        validate_provenance(info.provenance)
        if info.action not in {a.id for a in snapshot.actions}:
            raise PlannerError('information model action missing')
    if snapshot.context is not None:
        if not all((snapshot.context.scope, snapshot.context.lineage, snapshot.context.generation)):
            raise PlannerError('incomplete evaluation context')
        if snapshot.context.tick < 0:
            raise PlannerError('invalid evaluation tick')


def validate_p04(snapshot):
    unique(snapshot.decisions, lambda d: d.action)
    actions = {a.id: a for a in snapshot.actions}
    decisions = {d.action for d in snapshot.decisions}
    predicates = {p.id for p in snapshot.predicates} | {v.predicate for v in snapshot.validation_instances}
    input_owners = [d.input_action for d in snapshot.decisions if d.input_action is not None]
    unique(input_owners, lambda x: x)
    human = (OperationClass.ARCHITECT_AUTHORITY, OperationClass.ARCHITECT_CONTRACT_DECISION)
    for d in snapshot.decisions:
        validate_provenance(d.provenance)
        if d.action not in actions or actions[d.action].operation not in human:
            raise PlannerError('decision must name a human action')
        for ref in (d.semantic_action, d.input_action):
            if ref is not None and ref not in actions:
                raise PlannerError('missing decision route action')
        if d.input_action is not None and actions[d.input_action].operation not in (
            OperationClass.DECISION_INPUT_ACQUISITION, OperationClass.ARCHITECT_PREPARATION,
            OperationClass.IMPLEMENTATION_PREPARATION):
            raise PlannerError('invalid decision input operation')
        if d.input_action is not None and actions[d.input_action].effect is not EffectClass.NON_EFFECTING:
            raise PlannerError('decision input acquisition must be non-effecting')
        if d.stage is DecisionStage.DECISION_INPUTS_REQUIRED and not (d.input_action or d.external_input):
            raise PlannerError('missing decision input reentry route')
        for refs in (d.depends_on, d.interferes_with, d.downstream):
            unique(refs, lambda x: x)
            if any(ref not in actions or ref == d.action for ref in refs):
                raise PlannerError('invalid decision route reference')
        if any(ref not in decisions for ref in d.depends_on + d.interferes_with):
            raise PlannerError('missing decision dependency')
        if d.history and d.history[-1] is not d.stage:
            raise PlannerError('decision history/stage mismatch')
        stages = tuple(DecisionStage)
        if any(stages.index(after) != stages.index(before) + 1 and (before, after) != (
                DecisionStage.DECISION_INPUTS_REQUIRED, DecisionStage.DECISION_DOSSIER_READY)
                for before, after in zip(d.history, d.history[1:])):
            raise PlannerError('illegal decision lifecycle shortcut')
        if d.stage in (DecisionStage.DECISION_DOSSIER_READY, DecisionStage.DECISION_READY,
                       DecisionStage.DECISION_RECORDED, DecisionStage.DOWNSTREAM_REEVALUATION) and d.dossier is None:
            raise PlannerError('decision stage requires dossier')
        if d.dossier is not None and d.dossier.decision != d.action:
            raise PlannerError('dossier belongs to another decision')
        recorded = d.stage in (DecisionStage.DECISION_RECORDED, DecisionStage.DOWNSTREAM_REEVALUATION)
        if recorded != (d.record is not None and d.recorded_choice is not None):
            raise PlannerError('recorded decision requires independent record')
        if recorded and (d.record not in {e.id for e in snapshot.entities} or d.recorded_choice not in d.dossier.alternatives):
            raise PlannerError('unknown recorded decision evidence/choice')
    for dossier in tuple(d.dossier for d in snapshot.decisions if d.dossier is not None) + tuple(
            a.prepared_dossier for a in snapshot.actions if a.prepared_dossier is not None):
        validate_provenance(dossier.provenance)
        if dossier.decision not in decisions:
            raise PlannerError('unbound dossier')
        unique(dossier.checks, lambda c: c.kind)
        unique(dossier.alternatives, lambda x: x)
        unique(dossier.required_facts, lambda x: x)
        for check in dossier.checks:
            validate_provenance(check.provenance)
        if any(c.kind in SUPPORTED_DOSSIER_CHECKS and c.predicate not in predicates for c in dossier.checks) or any(
                ref not in predicates for ref in dossier.required_facts):
            raise PlannerError('missing dossier proof predicate')
    for a in snapshot.actions:
        if a.prepared_dossier is not None and not any(
            d.input_action == a.id and d.action == a.prepared_dossier.decision for d in snapshot.decisions):
            raise PlannerError('dossier outside input route')
        if a.accepted_result is not ActionResult.PASS and a.operation is not OperationClass.FACT_ACQUISITION and not any(
            a.id in (d.input_action, d.semantic_action) for d in snapshot.decisions):
            raise PlannerError('non-PASS contract outside bounded decision route')


@dataclass(frozen=True)
class RecordedDecision:
    decision: ActionId
    choice: str
    record: EntityId
    authority: PredicateId
    expected_snapshot: ArtifactIdentity


@dataclass(frozen=True)
class DecisionReentry:
    decision: ActionId
    expected_snapshot: ArtifactIdentity


@dataclass(frozen=True, order=True)
class GateId(Identifier):
    pass


@dataclass(frozen=True, order=True)
class EvidenceId(Identifier):
    pass


class ExternalStage(Enum):
    EXTERNAL_EVIDENCE_REQUIRED = 'EXTERNAL_EVIDENCE_REQUIRED'
    EVIDENCE_REQUEST_READY = 'EVIDENCE_REQUEST_READY'
    WAITING_FOR_EXTERNAL_EVIDENCE = 'WAITING_FOR_EXTERNAL_EVIDENCE'
    EVIDENCE_RECEIVED = 'EVIDENCE_RECEIVED'
    EVIDENCE_VALIDATED = 'EVIDENCE_VALIDATED'
    DEPENDENT_ACTION_REENTRY = 'DEPENDENT_ACTION_REENTRY'


class ControlState(Enum):
    RUNNABLE = 'RUNNABLE'
    HUMAN_HANDOFF = 'HUMAN_HANDOFF'
    EXTERNAL_WAIT = 'EXTERNAL_WAIT'
    MIXED_WAIT = 'MIXED_WAIT'
    PLAN_DEFECT = 'PLAN_DEFECT'
    TERMINAL_SUCCESS = 'TERMINAL_SUCCESS'
    TERMINAL_FAILURE = 'TERMINAL_FAILURE'
    QUALIFICATION_DECLINED = 'QUALIFICATION_DECLINED'


class BoundaryKind(Enum):
    EXTERNAL_EVIDENCE = 'EXTERNAL_EVIDENCE'
    EXTERNAL_FACT = 'EXTERNAL_FACT'
    IMPLEMENTATION_AUTHORITY = 'IMPLEMENTATION_AUTHORITY'
    PLAN_DEFECT = 'PLAN_DEFECT'


class BranchState(Enum):
    RUNNABLE_INTERNAL = 'RUNNABLE_INTERNAL'
    HUMAN_DECISION_REQUIRED = 'HUMAN_DECISION_REQUIRED'
    WAITING_FOR_EXTERNAL_EVIDENCE = 'WAITING_FOR_EXTERNAL_EVIDENCE'
    FACT_ACQUISITION_REQUIRED = 'FACT_ACQUISITION_REQUIRED'
    IMPLEMENTATION_AUTHORITY_REQUIRED = 'IMPLEMENTATION_AUTHORITY_REQUIRED'
    BLOCKED_BY_PLAN_DEFECT = 'BLOCKED_BY_PLAN_DEFECT'
    DEPENDENCY_BLOCKED = 'DEPENDENCY_BLOCKED'
    TERMINAL_SUCCESS = 'TERMINAL_SUCCESS'
    TERMINAL_FAILURE = 'TERMINAL_FAILURE'


@dataclass(frozen=True)
class EvidenceRequirement:
    id: EvidenceId
    proposition: str
    target: ArtifactIdentity
    producers: Tuple[ArtifactIdentity, ...]
    provenance: Provenance
    rule_known: bool = True


@dataclass(frozen=True)
class EvidenceClaim:
    requirement: EvidenceId
    outcome: ProofState


@dataclass(frozen=True)
class ReceiptAdmission:
    """An independently admitted trust attestation, never supplied by a receipt event.

    authentication proves producer competence for these exact bytes/claims. Raw
    identity alone is insufficient. Historical or explicitly synthetic trust only.
    """
    artifact: EntityId
    producer: ArtifactIdentity
    target: ArtifactIdentity
    claims: Tuple[EvidenceClaim, ...]
    authentication: PredicateId
    provenance: Provenance
    dependencies: Tuple[Provenance, ...] = ()


@dataclass(frozen=True)
class ReceiptObservation:
    gate: GateId
    artifact: EntityId
    accepted: bool
    reasons: Tuple[str, ...]
    claims: Tuple[EvidenceClaim, ...] = ()


@dataclass(frozen=True)
class ExternalResolutionContract:
    """Pinned acquisition contract, never positive evidence or a known proof rule."""
    request: str
    gate: GateId
    requirement: EvidenceId
    proposition: str
    target: ArtifactIdentity
    producers: Tuple[ArtifactIdentity, ...]
    source_class: str
    requirement_source: ArtifactIdentity
    gate_source: ArtifactIdentity
    receipt_action: str
    reentry: Tuple[ActionId, ...]
    held_actions: Tuple[ActionId, ...]
    scope: str
    lineage: str
    generation: str
    provenance: Provenance


@dataclass(frozen=True)
class ExternalGate:
    id: GateId
    requirements: Tuple[EvidenceId, ...]
    receipt_action: str
    reentry: Tuple[ActionId, ...]
    held_actions: Tuple[ActionId, ...]
    stage: ExternalStage
    provenance: Provenance
    history: Tuple[ExternalStage, ...] = ()
    pending: Optional[EntityId] = None
    contract_complete: bool = True
    validation: ValidationState = ValidationState.ACCEPTED
    resolution_contracts: Tuple[ExternalResolutionContract, ...] = ()


@dataclass(frozen=True)
class ControlBoundary:
    id: GateId
    kind: BoundaryKind
    actions: Tuple[ActionId, ...]
    provenance: Provenance


@dataclass(frozen=True)
class Goal:
    target: Union[ConditionId, SlotId]
    entry_actions: Tuple[ActionId, ...]
    provenance: Provenance
    failure: Optional[PredicateId] = None
    recovery: Tuple[ActionId, ...] = ()


@dataclass(frozen=True)
class ExternalEvent:
    gate: GateId
    stage: ExternalStage
    expected_snapshot: ArtifactIdentity
    artifact: Optional[EntityId] = None


def validate_p05(snapshot):
    for items, key in ((snapshot.evidence_requirements, lambda x:x.id),
                       (snapshot.external_gates, lambda x:x.id),
                       (snapshot.receipt_admissions, lambda x:x.artifact),
                       (snapshot.boundaries, lambda x:x.id), (snapshot.goals, lambda x:x.target)):
        unique(items,key)
    actions={a.id for a in snapshot.actions}; entities={e.id for e in snapshot.entities}
    requirements={r.id for r in snapshot.evidence_requirements}; gates={g.id for g in snapshot.external_gates}
    predicates={p.id for p in snapshot.predicates}
    targets={r.id for r in snapshot.roots}|{s.id for s in snapshot.slots}
    for r in snapshot.evidence_requirements:
        validate_provenance(r.provenance)
        unique(r.producers,lambda x:x)
        if not r.proposition:
            raise PlannerError('empty proof obligation')
    for g in snapshot.external_gates:
        unique(g.resolution_contracts, lambda c: c.requirement)
        for contract in g.resolution_contracts:
            validate_provenance(contract.provenance)
            unique(contract.producers, lambda x: x)
            unique(contract.reentry, lambda x: x)
            unique(contract.held_actions, lambda x: x)
        validate_provenance(g.provenance)
        unique(g.requirements,lambda x:x)
        if not g.requirements or not set(g.requirements)<=requirements or not g.receipt_action or not g.reentry:
            raise PlannerError('incomplete external gate')
        if not set(g.reentry+g.held_actions)<=actions:
            raise PlannerError('unknown gate action')
        if g.pending is not None and g.pending not in entities:
            raise PlannerError('unknown pending receipt')
        if g.history and g.history[-1] is not g.stage:
            raise PlannerError('external stage/history mismatch')
        sequence=tuple(ExternalStage)
        if any(sequence.index(after)!=sequence.index(before)+1 and (before,after)!=(
                ExternalStage.EVIDENCE_RECEIVED,ExternalStage.WAITING_FOR_EXTERNAL_EVIDENCE)
                for before,after in zip(g.history,g.history[1:])):
            raise PlannerError('external lifecycle history shortcut')
        if g.stage is ExternalStage.EVIDENCE_RECEIVED and g.pending is None:
            raise PlannerError('received state without receipt')
    for admission in snapshot.receipt_admissions:
        validate_provenance(admission.provenance)
        unique(admission.claims,lambda x:x.requirement)
        if admission.artifact not in entities or admission.authentication not in predicates or any(
                c.requirement not in requirements or c.outcome is ProofState.UNKNOWN for c in admission.claims):
            raise PlannerError('invalid receipt admission')
    for observation in snapshot.receipt_observations:
        if observation.gate not in gates or observation.artifact not in entities:
            raise PlannerError('unknown receipt observation')
        admission=next((a for a in snapshot.receipt_admissions if a.artifact==observation.artifact),None)
        if observation.accepted and (admission is None or set(observation.claims)!=set(admission.claims)) or (
                not observation.accepted and observation.claims):
            raise PlannerError('receipt observation differs from admitted claims')
    for boundary in snapshot.boundaries:
        validate_provenance(boundary.provenance)
        if not boundary.actions or not set(boundary.actions)<=actions:
            raise PlannerError('invalid control boundary')
        if boundary.kind is BoundaryKind.EXTERNAL_EVIDENCE and boundary.id not in gates:
            raise PlannerError('external boundary lacks receipt contract')
    for goal in snapshot.goals:
        validate_provenance(goal.provenance)
        if goal.target not in targets or not set(goal.entry_actions+goal.recovery)<=actions or (
                goal.failure is not None and goal.failure not in predicates):
            raise PlannerError('invalid goal route')


@dataclass(frozen=True)
class ResumeEligibility:
    """Derived proof, never a persisted permission Boolean."""
    allowed: bool
    actions: Tuple[ActionId, ...]
    reasons: Tuple[str, ...]
    supporting_identities: Tuple[ArtifactIdentity, ...]


@dataclass(frozen=True)
class SourceInvalidation:
    """Persist loss of proof qualification; cannot create evidence or permission."""
    changed: Tuple[ArtifactIdentity, ...]
    expected_snapshot: ArtifactIdentity


@dataclass(frozen=True)
class BudgetProofRow:
    obligation: EvidenceId
    fact: ArtifactIdentity
    rule: ArtifactIdentity


@dataclass(frozen=True)
class BudgetProofMatrix:
    identity: ArtifactIdentity
    consumer: ActionId
    output: KnowledgeId
    envelope: 'BudgetEnvelope'
    knowledge: KnowledgeId
    parameters: str
    submission: str
    rows: Tuple[BudgetProofRow, ...]
    provenance: Provenance
    evidence: Tuple[AssertionId, ...]


@dataclass(frozen=True)
class BudgetEnvelope:
    authority: ArtifactIdentity
    invocation: ArtifactIdentity
    dispatch: ArtifactIdentity
    context: ArtifactIdentity
    release: ArtifactIdentity
    runtime: ArtifactIdentity
    controller_store: ArtifactIdentity
    profile: ArtifactIdentity
    lineage: ArtifactIdentity
    source_scope: str
    target_scope: str
    operation: str


@dataclass(frozen=True)
class EvidenceIngressContract:
    schema: str
    gate: GateId
    receipt_action: str
    requirements: Tuple[EvidenceId, ...]
    authentication: PredicateId
    source_class: str
    scope: str
    lineage: str
    generation: str
    valid_until: int
    provenance: Provenance


@dataclass(frozen=True)
class EvidenceFieldProvenance:
    target: str
    selector: str
    provenance: Provenance


@dataclass(frozen=True)
class EvidenceSourceAdmission:
    schema: str
    expected_bundle: ArtifactIdentity
    expected_snapshot: ArtifactIdentity
    expected_parent_event: Optional[ArtifactIdentity]
    command_key: ArtifactIdentity
    gate: GateId
    receipt_action: str
    requirements: Tuple[EvidenceId, ...]
    contract_pin: ArtifactIdentity
    source_additions: Tuple[ArtifactPin, ...]
    entity: GraphEntity
    admission: ReceiptAdmission
    field_provenance: Tuple[EvidenceFieldProvenance, ...]
