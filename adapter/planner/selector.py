"""Validated E1 ordering: unavailable metrics fall through, never get estimated."""
from typing import Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib
import json
from . import model as m


@dataclass(frozen=True)
class SelectionTrace:
    selected: m.ActionId
    criterion: int
    steps: Tuple[str, ...]


PRIORITY = (m.OperationClass.DETERMINISTIC_VALIDATION, m.OperationClass.DETERMINISTIC_CONSTRUCTION,
    m.OperationClass.SOURCE_ACQUISITION, m.OperationClass.DETERMINISTIC_MAPPING,
    m.OperationClass.IMPLEMENTATION_PREPARATION, m.OperationClass.SEMANTIC_EVALUATION,
    m.OperationClass.ARCHITECT_PREPARATION, m.OperationClass.RUNTIME_EXPERIMENT,
    m.OperationClass.GOVERNED_OPERATION)


# Closed, code-reviewed policy registry. These are historical replay schema
# versions of the same admitted E1 selector, not permission to adopt new policy.
POLICY_PIN = m.ArtifactPin(
    'docs/experiments/E1/E1_GRAPH_RESOLUTION_SELECTION_POLICY_1.md',
    m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY, 'raw-file-sha256',
        '475bef0b28d7b484ba2641c654b37e9ce3d6f6ae1b0e13dfdcadaa3f79a2a3b5'))
CLASS_MAP = (
    (m.OperationClass.FACT_ACQUISITION, m.OperationClass.SOURCE_ACQUISITION),
    (m.OperationClass.DECISION_INPUT_ACQUISITION, m.OperationClass.ARCHITECT_PREPARATION),
    (m.OperationClass.ARCHITECT_AUTHORITY, m.OperationClass.GOVERNED_OPERATION),
    (m.OperationClass.ARCHITECT_CONTRACT_DECISION, m.OperationClass.GOVERNED_OPERATION),
    (m.OperationClass.IMPLEMENTATION_REPAIR, m.OperationClass.GOVERNED_OPERATION),
    (m.OperationClass.VALIDATOR_IMPLEMENTATION, m.OperationClass.GOVERNED_OPERATION))
EFFECT_PRIORITY = (m.EffectClass.NON_EFFECTING,
    m.EffectClass.QUALIFICATION_EFFECT_ONLY, m.EffectClass.PRODUCTION_EFFECT)


@dataclass(frozen=True)
class PolicyBinding:
    policy_id: str
    version: str
    artifact: m.ArtifactPin
    implementation_rule_version: str
    class_priority: tuple
    class_map: tuple
    effect_priority: tuple
    rules: tuple


# Full rules, including absence/fallthrough and the stage-sensitive mapping,
# are part of the supported binding. No input-supplied rule is executed.
RULES = ('singleton:0', 'coverage:complete-nonnegative-triple-lex-max-else-skip',
    'information:accepted-common-universe-partitions-max-else-skip',
    'class:all-mapped-min-else-skip',
    'semantic-resolution:decision-preparation=architect-preparation;else=semantic-evaluation',
    'effect:min', 'cost:complete-nonnegative-common-unit-min-else-skip',
    'tie:canonical-action-id-unicode-lex-min')
SUPPORTED_POLICIES = tuple(PolicyBinding('E1-SELECTION-1', version, POLICY_PIN,
    'E1-SELECTOR-RULES-1', PRIORITY, CLASS_MAP, EFFECT_PRIORITY, RULES)
    for version in ('E1-SELECTION-1-P01-SUBSET', 'E1-SELECTION-1-P03',
                    'E1-SELECTION-1-P04', 'E1-SELECTION-1-P05', 'E1-SELECTION-1-P06'))


def policy_contract_bytes(binding):
    """Canonical implementation contract; never deserialize executable rules."""
    def encode_enum(value):
        if isinstance(value, Enum):
            return value.value
        raise m.PlannerError('unsupported policy contract value')
    return json.dumps(asdict(binding), sort_keys=True, separators=(',', ':'),
        ensure_ascii=True, default=encode_enum).encode('utf-8')


# Reviewed contract commitments: changing a rule/map requires explicit admission.
CONTRACT_DIGESTS = {
    'E1-SELECTION-1-P01-SUBSET':
        'e75cc9b49b7c13e4a811b25cb57f102d0efac188c0f9f4ebb3703102306e6616',
    'E1-SELECTION-1-P03':
        '5cb4f48528b47210dcac6f4681470aa464960a3a9d2f54c90fe4c28d8393d2b0',
    'E1-SELECTION-1-P04':
        'b7f675443b6728d6f09339267bc0f813e75294f7f7425931a2fc51ea9cd40f52',
    'E1-SELECTION-1-P05':
        '1a9cdaaa6a28456a417be7c64733762f9686df86124a49c4b9933395b099dc6c',
    'E1-SELECTION-1-P06':
        'cced16ced0b421bd75bea86dabb95dd63d9392152c344b8bfdd88c602831d0cd',
}


def validate_policy(pin, version):
    """Semantic admission, in addition to the codec's byte authentication.

    A matching arbitrary content hash is not sufficient. Only an exact reviewed
    artifact/domain/profile/projection and supported implementation binding pass.
    Historical versions are retained, never upgraded by this function.
    """
    m.validate_types(pin, m.ArtifactPin)
    binding = next((p for p in SUPPORTED_POLICIES if p.version == version), None)
    if binding is None or binding.artifact != pin or hashlib.sha256(
            policy_contract_bytes(binding)).hexdigest() != CONTRACT_DIGESTS.get(version):
        raise m.PlannerError('unsupported selection policy identity/version binding')
    if (binding.class_priority, binding.class_map, binding.effect_priority, binding.rules) != (
            PRIORITY, CLASS_MAP, EFFECT_PRIORITY, RULES):
        raise m.PlannerError('selection policy implementation contract drift')
    return binding


def priority_class(action):
    if action.operation is m.OperationClass.SEMANTIC_RESOLUTION:
        return (m.OperationClass.ARCHITECT_PREPARATION if action.stage is m.ActionStage.DECISION_PREPARATION
                else m.OperationClass.SEMANTIC_EVALUATION)
    return dict(CLASS_MAP).get(action.operation, action.operation)


def select(actions, coverage=None, information=None, *, policy=POLICY_PIN,
           policy_version="E1-SELECTION-1-P05"):
    validate_policy(policy, policy_version)
    actions = tuple(actions)
    if not actions:
        raise m.PlannerError('selector requires a nonempty actionable set')
    for action in actions:
        m.validate_types(action, m.Action)
    m.unique(actions, lambda a: a.id)
    byid = {a.id: a for a in actions}
    ids = sorted(byid)
    steps = []
    if len(ids) == 1:
        return SelectionTrace(ids[0], 0, ('SINGLETON',))

    def narrow(scores, greatest=False):
        nonlocal ids
        best = (max if greatest else min)(scores[i] for i in ids)
        ids = [i for i in ids if scores[i] == best]
        return len(ids) == 1

    complete = coverage is not None and all(i in coverage and type(coverage[i]) is tuple and
        len(coverage[i]) == 3 and all(type(v) is int and v >= 0 for v in coverage[i]) for i in ids)
    if complete:
        if narrow(coverage, True):
            return SelectionTrace(ids[0], 1, ('CRITERION_1_COVERAGE',))
        steps.append('CRITERION_1_TIED')
    else:
        steps.append('CRITERION_1_NOT_DECISIVE')
    scores, universes = {}, set()
    for i in ids:
        info = (information or {}).get(i)
        if info is None:
            continue
        m.validate_types(info, m.InformationModel)
        universe = frozenset(info.alternatives)
        flat = tuple(v for part in info.partitions for v in part)
        if info.validation is not m.ValidationState.ACCEPTED or info.action != i or not universe or any(not label for label in universe) or len(universe) != len(info.alternatives) or \
                any(not part for part in info.partitions) or len(flat) != len(set(flat)) or set(flat) != universe:
            continue
        scores[i] = len(info.partitions) - 1
        universes.add(universe)
    if len(universes) == 1 and all(i in scores for i in ids):
        if narrow(scores, True):
            return SelectionTrace(ids[0], 2, tuple(steps + ['CRITERION_2_INFORMATION']))
        steps.append('CRITERION_2_TIED')
    else:
        steps.append('CRITERION_2_NOT_DECISIVE')
    classes = {i: priority_class(byid[i]) for i in ids}
    if all(value in PRIORITY for value in classes.values()):
        if narrow({i: PRIORITY.index(classes[i]) for i in ids}):
            return SelectionTrace(ids[0], 3, tuple(steps + ['CRITERION_3_CLASS']))
        steps.append('CRITERION_3_TIED')
    else:
        steps.append('CRITERION_3_NOT_DECISIVE')
    effects = {effect: rank for rank, effect in enumerate(EFFECT_PRIORITY)}
    if narrow({i: effects[byid[i].effect] for i in ids}):
        return SelectionTrace(ids[0], 4, tuple(steps + ['CRITERION_4_EFFECT']))
    units = {byid[i].cost_unit for i in ids}
    if len(units) == 1 and '' not in units and all(type(byid[i].cost) is int and byid[i].cost >= 0 for i in ids):
        if narrow({i: byid[i].cost for i in ids}):
            return SelectionTrace(ids[0], 4, tuple(steps + ['CRITERION_4_COST']))
        steps.append('CRITERION_4_TIED')
    else:
        steps.append('CRITERION_4_TIED_NO_COST')
    return SelectionTrace(ids[0], 5, tuple(steps + ['CRITERION_5_ACTION_ID']))
