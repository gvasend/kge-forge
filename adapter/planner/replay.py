"""Pinned historical replay adapters and deterministic structured E1 import."""
from dataclasses import dataclass
from pathlib import Path

from .model import (Action, ActionId, ActionResult, ActionState, ActionStatus,
                    ArtifactIdentity, ConditionId, ConditionState, EffectClass,
                    Gate, GateKind, IdentityKind, KnowledgeId, KnowledgeRecord,
                    KnowledgeState, OperationClass, PlannerError, Provenance,
                    RootCondition, SlotId, SlotState, Snapshot, SuppliedResult,
                    ValueSlot, validate_model, ArtifactPin, HashProfile)
from .core import apply_result
from .codec import parse_json, load_pinned


def object_fields(value, names):
    if type(value) is not dict or set(value) != set(names.split()):
        raise PlannerError('unknown or missing object fields')
    return value


def array(value):
    if type(value) is not list:
        raise PlannerError('JSON array required')
    return value


def string(value):
    if type(value) is not str or not value:
        raise PlannerError('nonempty JSON string required')
    return value


def enum(cls, value):
    try:
        return cls(string(value))
    except ValueError as exc:
        raise PlannerError('unknown ' + cls.__name__) from exc


def _source(value, repo_root):
    object_fields(value, 'path sha256 section excerpt method scope')
    values = {key: string(v) for key, v in value.items()}
    relative = Path(values['path'])
    if relative.is_absolute() or '..' in relative.parts:
        raise PlannerError('source must be repository-relative')
    root = Path(repo_root).resolve()
    path = root / relative
    allowed = root / 'docs/experiments/E1'
    try:
        path.relative_to(allowed)
    except ValueError as exc:
        raise PlannerError('source outside frozen E1') from exc
    if path.resolve() != path:
        raise PlannerError('source must be an exact frozen E1 path')
    identity = ArtifactIdentity(IdentityKind.CONTENT_IDENTITY, 'raw-file-sha256', values['sha256'])
    try:
        raw = load_pinned(root, ArtifactPin(values['path'], identity))
        text = raw.decode('utf-8')
    except (OSError, UnicodeError) as exc:
        raise PlannerError('source unavailable') from exc
    marker = '## ' + values['section'] + '\n'
    if text.count(marker) != 1:
        raise PlannerError('source section not unique')
    section = text.split(marker, 1)[1].split('\n## ', 1)[0]
    if values['excerpt'] not in section:
        raise PlannerError('source excerpt absent from declared section')
    return Provenance(values['path'], identity, values['section'], values['excerpt'],
                      values['method'], values['scope'])


def decode_result(value, snapshot):
    object_fields(value, 'action result knowledge_ids')
    action_id = ActionId(string(value['action']))
    action = next((a for a in snapshot.actions if a.id == action_id), None)
    if action is None:
        raise PlannerError('unknown action')
    records = {k.id.value: k for k in action.accepted_inventory}
    ids = [string(k) for k in array(value['knowledge_ids'])]
    if any(k not in records for k in ids):
        raise PlannerError('knowledge outside bounded inventory contract')
    return SuppliedResult(action_id, enum(ActionResult, value['result']),
                          tuple(records[k] for k in ids))


@dataclass(frozen=True)
class ReplayFixture:
    snapshot: Snapshot
    supplied_result: SuppliedResult


def load_fixture(path, repo_root):
    try:
        data = parse_json(Path(path).read_text(encoding='utf-8'))
    except OSError as exc:
        raise PlannerError('fixture unavailable') from exc
    object_fields(data, 'schema scope sources actions roots slots result')
    if data['schema'] != 'P01-E-SLICE-1' or data['scope'] != 'PARTIAL_HISTORICAL_REPLAY':
        raise PlannerError('not a P01 slice')
    if type(data['sources']) is not dict or not data['sources']:
        raise PlannerError('pinned source map required')
    sources = {string(key): _source(value, repo_root) for key, value in data['sources'].items()}

    def source(key):
        key = string(key)
        if key not in sources:
            raise PlannerError('unknown source reference')
        return sources[key]

    roots = []
    for row in array(data['roots']):
        object_fields(row, 'id state')
        roots.append(RootCondition(ConditionId(string(row['id'])), enum(ConditionState, row['state'])))
    slots = []
    for row in array(data['slots']):
        object_fields(row, 'id state required_type')
        slots.append(ValueSlot(SlotId(string(row['id'])), enum(SlotState, row['state']),
                               enum(IdentityKind, row['required_type'])))
    actions, statuses = [], []
    for row in array(data['actions']):
        object_fields(row, 'id operation effect state prerequisites source accepted_inventory')
        gates = []
        for gate in array(row['prerequisites']):
            object_fields(gate, 'kind target')
            kind = enum(GateKind, gate['kind'])
            cls = ActionId if kind is GateKind.ACTION_COMPLETED else ConditionId
            gates.append(Gate(kind, cls(string(gate['target']))))
        knowledge = []
        for record in array(row['accepted_inventory']):
            object_fields(record, 'id state statement source')
            knowledge.append(KnowledgeRecord(KnowledgeId(string(record['id'])),
                enum(KnowledgeState, record['state']), string(record['statement']),
                source(record['source'])))
        if row['operation'] != 'SOURCE_ACQUISITION':
            raise PlannerError('P01 slice operation unsupported')
        action_id = ActionId(string(row['id']))
        actions.append(Action(action_id, enum(OperationClass, row['operation']),
            enum(EffectClass, row['effect']), tuple(gates), source(row['source']), tuple(knowledge)))
        statuses.append(ActionStatus(action_id, enum(ActionState, row['state'])))
    snapshot = Snapshot(tuple(actions), tuple(statuses), tuple(roots), tuple(slots), ())
    validate_model(snapshot)
    return ReplayFixture(snapshot, decode_result(data['result'], snapshot))


def run_replay(fixture):
    """Apply one supplied bounded result. Never execute the next selected action."""
    return apply_result(fixture.snapshot, fixture.supplied_result)


def load_source_manifest(path, repo_root):
    """P02 fixture pins, verified before use; not authority/applicability evidence."""
    data = parse_json(Path(path).read_bytes())
    object_fields(data, 'schema sources')
    if data['schema'] != 'PLANNER-SOURCES-1':
        raise PlannerError('unknown source manifest')
    pins = []
    for row in array(data['sources']):
        object_fields(row, 'path kind profile sha256 pointer')
        profile = enum(HashProfile, row['profile'])
        pin = ArtifactPin(string(row['path']), ArtifactIdentity(
            enum(IdentityKind, row['kind']), profile.value, string(row['sha256'])),
            profile, row['pointer'])
        load_pinned(repo_root, pin)
        pins.append(pin)
    keys = [(p.path, p.pointer, p.profile.value) for p in pins]
    if len(keys) != len(set(keys)):
        raise PlannerError('duplicate source manifest pin')
    return tuple(sorted(pins, key=lambda p: (p.path, p.pointer, p.profile.value)))


def load_p03_fixture(path, repo_root):
    """Reviewed C/D fixture adapter only. Expected values never enter core state."""
    from .codec import decode_snapshot, canonical_bytes
    data = parse_json(Path(path).read_bytes())
    object_fields(data, 'schema case_id sources snapshot given when then must_not expected')
    if data['schema'] != 'PLANNER-P03-FIXTURE-1' or data['case_id'] not in ('C', 'D'):
        raise PlannerError('unknown P03 fixture')
    for label in ('given', 'when', 'then', 'must_not'):
        string(data[label])
    sources = tuple(_source(row, repo_root) for row in array(data['sources']))
    snapshot = decode_snapshot(canonical_bytes(data['snapshot']))
    provenances = [a.source for a in snapshot.actions] + [a.provenance for a in snapshot.assertions]
    provenances += [e.provenance for e in snapshot.entities] + [i.provenance for i in snapshot.information]
    provenances += [k.provenance for k in snapshot.knowledge]
    provenances += [k.provenance for a in snapshot.actions for k in a.accepted_inventory]
    if any(p not in sources for p in provenances):
        raise PlannerError('unverified fixture provenance')
    return snapshot, data['expected']


def load_p04_fixture(path, repo_root):
    return _load_decision_or_control_fixture(path,repo_root,False)


def load_p05_fixture(path, repo_root):
    return _load_decision_or_control_fixture(path,repo_root,True)


def _load_decision_or_control_fixture(path, repo_root, p05):
    """Reviewed decision snapshots with exact raw pins and JSON-pointer/section evidence."""
    from . import model as m
    from .codec import decode_snapshot, canonical_bytes, json_pointer, decision_provenances, external_provenances
    data = parse_json(Path(path).read_bytes())
    object_fields(data, 'schema case_id sources snapshot given when then must_not expected')
    if data['schema'] not in (('PLANNER-P05-FIXTURE-1', 'PLANNER-P05-FIXTURE-2') if p05 else ('PLANNER-P04-FIXTURE-1', 'PLANNER-P04-FIXTURE-2')) or data['case_id'] not in (('J','K','L','M') if p05 else ('E','F','G','H','I')):
        raise PlannerError('unknown P04 fixture')
    for label in ('given', 'when', 'then', 'must_not'):
        string(data[label])
    sources = []
    for row in array(data['sources']):
        if not row['section'].startswith('/'):
            sources.append(_source(row, repo_root))
            continue
        object_fields(row, 'path sha256 section excerpt method scope')
        relative = Path(string(row['path']))
        if relative.is_absolute() or '..' in relative.parts or relative.parts[:3] != ('docs', 'experiments', 'E1'):
            raise PlannerError('decision source outside frozen E1')
        identity = ArtifactIdentity(IdentityKind.CONTENT_IDENTITY, 'raw-file-sha256', row['sha256'])
        value = parse_json(load_pinned(repo_root, ArtifactPin(row['path'], identity)))
        if canonical_bytes(json_pointer(value, row['section'])).decode('utf-8') != row['excerpt']:
            raise PlannerError('decision source projection mismatch')
        sources.append(Provenance(row['path'], identity, row['section'], row['excerpt'], row['method'], row['scope']))
    snapshot = decode_snapshot(canonical_bytes(data['snapshot']))
    provenances = [a.source for a in snapshot.actions] + [a.provenance for a in snapshot.assertions]
    provenances += [e.provenance for e in snapshot.entities] + [i.provenance for i in snapshot.information]
    provenances += [k.provenance for k in snapshot.knowledge]
    provenances += [k.provenance for a in snapshot.actions for k in a.accepted_inventory]
    provenances += decision_provenances(snapshot) + external_provenances(snapshot)
    if any(p not in sources for p in provenances):
        raise PlannerError('unverified decision fixture provenance')
    return snapshot, data['expected']


# P06 structured import. Frozen prose is never interpreted by this adapter.
def provenance_records(snapshot):
    from . import codec as c
    return ([a.source for a in snapshot.actions] + [a.provenance for a in snapshot.assertions]
        + [e.provenance for e in snapshot.entities] + [i.provenance for i in snapshot.information]
        + [k.provenance for k in snapshot.knowledge]
        + [k.provenance for a in snapshot.actions for k in a.accepted_inventory]
        + c.decision_provenances(snapshot) + c.external_provenances(snapshot))


def import_fixture(path, repo_root):
    """Closed PLANNER-REPLAY-1 format; expected/prohibited are never core inputs."""
    from . import codec as c, model as m
    data = c.parse_json(Path(path).read_bytes())
    if type(data) is dict and data.get('schema') == 'PLANNER-BUDGET-QUALIFICATION-1':
        from .budget import import_budget
        return import_budget(path, repo_root, data)
    object_fields(data, 'schema case_id mode source_manifest initial policy events expected prohibited')
    if data['schema'] not in ('PLANNER-REPLAY-1', 'PLANNER-REPLAY-2') or data['case_id'] not in tuple('ABCDEFGHIJKLMN'):
        raise PlannerError('unknown replay schema/case')
    if data['mode'] not in ('HISTORICAL', 'COUNTERFACTUAL_SYNTHETIC'):
        raise PlannerError('unknown replay mode')
    pins = tuple(c._unwire(p) for p in array(data['source_manifest']))
    for pin in pins:
        c.validate_pin(pin)
        c.load_pinned(repo_root, pin)
    policy = c._unwire(data['policy'])
    c.validate_pin(policy)
    from .selector import validate_policy
    validate_policy(policy, 'E1-SELECTION-1-P05')
    c.load_pinned(repo_root, policy)
    state = c.decode_snapshot(c.canonical_bytes(data['initial']))
    bundle = m.PersistenceBundle(state, (), state, pins, policy, 'E1-SELECTION-1-P05')
    c.bundle_bytes(bundle)  # References, provenance coverage, enums, types and ledger.
    for p in provenance_records(state):
        raw = c.load_pinned(repo_root, m.ArtifactPin(p.path, p.identity))
        if p.section.startswith('/'):
            if c.canonical_bytes(c.json_pointer(c.parse_json(raw), p.section)).decode() != p.excerpt:
                raise PlannerError('source projection mismatch')
        elif p.section == 'whole artifact':
            if p.excerpt != raw.decode('utf-8'):
                raise PlannerError('whole artifact mismatch')
        else:
            _source(dict(path=p.path, sha256=p.identity.sha256, section=p.section,
                         excerpt=p.excerpt, method=p.method, scope=p.scope), repo_root)
    if data['case_id'] == 'A':
        from dataclasses import replace
        candidate = next((p for p in pins if p.path.endswith('E1_CURRENT_WORKAUTHORIZATION_CANDIDATE_2.json')), None)
        consumer = next((p for p in pins if p.path == 'adapter/invocation_constructor.py'), None)
        if candidate is None or consumer is None or any(k.id.value == 'consumer-contract' for k in state.knowledge):
            raise PlannerError('missing consumer pins or supplied consumer success claim')
        passed, detail = consumer_identity_precheck(repo_root, candidate, consumer)
        provenance = next((a.source for a in state.actions if a.source.path == candidate.path), None)
        if provenance is None:
            raise PlannerError('consumer action has no candidate provenance')
        knowledge = m.KnowledgeRecord(m.KnowledgeId('consumer-contract' if passed else 'consumer-rejection'),
            m.KnowledgeState.KNOWN_COMPLETE, detail, provenance)
        state = replace(state, knowledge=state.knowledge + (knowledge,),
            predicates=tuple(replace(p, knowledge=knowledge.id, unavailable=None)
                if passed and p.kind is m.PredicateKind.KNOWLEDGE_ACCEPTED and
                p.id == m.PredicateId('consumer-contract') and p.unavailable is not None
                else p for p in state.predicates))
        bundle = replace(bundle, initial=state, current=state)
        c.bundle_bytes(bundle)
    events = tuple(c._unwire(e) for e in array(data['events']))
    if any(type(e) not in (m.SuppliedResult, m.RecordedDecision, m.DecisionReentry, m.ExternalEvent) for e in events):
        raise PlannerError('unknown replay event')
    if type(data['expected']) is not dict or type(data['prohibited']) is not list:
        raise PlannerError('invalid replay oracle')
    return bundle, events, data['expected']


def consumer_identity_precheck(repo_root, candidate_pin, constructor_pin):
    """Call only the pinned pure identity function; never a construction/effect path."""
    from . import codec as c
    c.load_pinned(repo_root, constructor_pin)
    if constructor_pin.path != 'adapter/invocation_constructor.py':
        raise PlannerError('unsupported consumer')
    # Ensure the code actually executing is the code whose bytes were pinned.
    from .. import invocation_constructor as consumer
    if Path(consumer.__file__).resolve() != (Path(repo_root) / constructor_pin.path).resolve():
        raise PlannerError('consumer execution source mismatch')
    candidate = c.parse_json(c.load_pinned(repo_root, candidate_pin))
    if type(candidate) is not dict:
        raise PlannerError('candidate object required')
    try:
        return True, consumer.identity(candidate)
    except consumer.ConstructionDenied as exc:
        return False, str(exc)


def restore_accepted_knowledge(state, plan, pins, root):
    """E1_ACCEPTED_OUTCOME_1: finite structured requirement/report projection.

    Restores knowledge of an accepted historical outcome, never completion of
    its producer. Raw source pins and exact report fields authenticate the
    observation; current validity remains subject to normal stale propagation.
    """
    import re
    from dataclasses import replace
    from . import codec as c, model as m
    rows = {row['id']: row for row in plan['resolution_actions']}
    actions = {action.id.value: action for action in state.actions}
    knowledge, predicates = list(state.knowledge), list(state.predicates)
    for consumer in sorted(rows):
        for requirement in rows[consumer].get('knowledge_requirements', []):
            object_fields(requirement, 'action required_recorded_outcome evidence requirement')
            evidence = object_fields(requirement['evidence'], 'path sha256 location')
            producer = string(requirement['action'])
            outcome = enum(m.ActionResult, requirement['required_recorded_outcome'])
            if producer not in rows or producer not in actions or consumer not in actions:
                raise PlannerError('accepted knowledge producer/consumer absent')
            identity = m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY,
                'raw-file-sha256', string(evidence['sha256']))
            pin = m.ArtifactPin(string(evidence['path']), identity)
            if pin not in pins:
                raise PlannerError('accepted knowledge source is not independently pinned')
            text = c.load_pinned(root, pin).decode('utf-8')
            reports = re.findall(r'^```text\n(.*?)^```', text, re.M | re.S)
            def field(name):
                values = [value for report in reports for value in
                    re.findall(r'^' + name + r' = ([^\n]+)$', report, re.M)]
                if len(values) != 1:
                    raise PlannerError('accepted knowledge report field absent/ambiguous: ' + name)
                return values[0]
            recorded = rows[producer].get('execution_result', {})
            if (field('ACTION') != producer or field('ACTION_RESULT') != outcome.value or
                    recorded.get('result') != outcome.value or recorded.get('result_artifact') != pin.path):
                raise PlannerError('accepted knowledge producer/outcome/source conflict')
            kid = m.KnowledgeId('accepted-outcome:' + consumer + ':' + producer + ':' + identity.sha256)
            pid = m.PredicateId(kid.value)
            source = m.Provenance(pin.path, identity, string(evidence['location']),
                'ACTION = ' + producer + '\nACTION_RESULT = ' + outcome.value,
                'E1_ACCEPTED_OUTCOME_1', actions[consumer].source.scope)
            knowledge.append(m.KnowledgeRecord(kid, m.KnowledgeState.KNOWN_COMPLETE,
                c.canonical_bytes({'producer': producer, 'recorded_outcome': outcome.value}).decode(),
                source, producer=m.ActionId(producer), outcome=outcome))
            predicates.append(m.Predicate(pid, m.PredicateKind.KNOWLEDGE_ACCEPTED,
                knowledge=kid, expected=identity, action=m.ActionId(producer), required_outcome=outcome))
            actions[consumer] = replace(actions[consumer],
                requirements=actions[consumer].requirements + (pid,))
    result = replace(state, actions=tuple(actions[k] for k in sorted(actions)),
        knowledge=tuple(sorted(knowledge, key=lambda k:k.id.value)),
        predicates=tuple(sorted(predicates, key=lambda p:p.id.value)))
    m.validate_model(result)
    return result


def import_e1(manifest_path, repo_root, descriptor_path=None):
    """Versioned, pinned pointer normalization into an isolated replay bundle.

    Non-operational graph records are retained verbatim as provenance assertions.
    They cannot create prerequisite edges or satisfy predicates. The reviewed
    normalization defines the executable projection, never a report's oracles.
    """
    from dataclasses import replace
    from . import codec as c, model as m
    root = Path(repo_root).resolve()
    descriptor_path = descriptor_path or root / 'adapter/tests/fixtures/planner_v0_1/N_P06.json'
    descriptor = c.parse_json(Path(descriptor_path).read_bytes())
    object_fields(descriptor, 'schema manifest normalization checkpoint policy given when then must_not')
    if descriptor['schema'] != 'PLANNER-E1-IMPORT-1':
        raise PlannerError('unknown E1 importer mapping')
    manifest_pin = c._unwire(descriptor['manifest'])
    if Path(manifest_path).resolve() != (root / manifest_pin.path).resolve():
        raise PlannerError('unmapped E1 manifest')
    policy = c._unwire(descriptor['policy'])
    from .selector import validate_policy
    validate_policy(policy, 'E1-SELECTION-1-P06')
    c.load_pinned(root, policy)
    pins = list(c.read_e1_manifest(root, manifest_pin)) + [manifest_pin, policy]
    checkpoint_pin = c._unwire(descriptor['checkpoint'])
    checkpoint = c.parse_json(c.load_pinned(root, checkpoint_pin))
    import hashlib
    checkpoint_body = {k:v for k,v in checkpoint.items() if k != 'checkpoint_identity'}
    if checkpoint.get('schema') != 'E1-SUSPENSION-CHECKPOINT-1' or checkpoint.get('checkpoint_identity') != \
            'E1-SuspensionCheckpoint-sha256:' + hashlib.sha256(c.canonical_bytes(checkpoint_body)).hexdigest():
        raise PlannerError('checkpoint identity mismatch')
    if checkpoint['bindings']['resume_manifest']['raw_sha256'] != manifest_pin.identity.sha256:
        raise PlannerError('checkpoint/manifest mismatch')
    pins.append(checkpoint_pin)
    normalization = c._unwire(descriptor['normalization'])
    c.load_pinned(root, normalization)
    state, _ = load_p05_fixture(root / normalization.path, root)
    pins.append(normalization)
    pins += [m.ArtifactPin(p.path, p.identity) for p in provenance_records(state)]
    manifest = c.parse_json(c.load_pinned(root, manifest_pin))
    graph_ref = manifest['current_graph']
    graph = c.parse_json(c.load_pinned(root, next(p for p in pins if p.path == graph_ref['path'] and not p.pointer)))
    plan_ref = manifest['current_plan']
    plan = c.parse_json(c.load_pinned(root, next(p for p in pins if p.path == plan_ref['path'] and not p.pointer)))
    if graph.get('schema') != 'E1-TEMPLATE1-TYPED-KNOWLEDGE-GRAPH-1' or plan.get('schema') != 'E1-TEMPLATE1-GRAPH-RESOLUTION-PLAN-1':
        raise PlannerError('unknown E1 graph/plan schema')
    # Exact coverage required, not counts copied from expected report fields.
    def ids(rows):
        result = [string(row['id']) for row in rows]
        if len(result) != len(set(result)):
            raise PlannerError('duplicate imported identity')
        return set(result)
    graph_ids = ids(graph['entities'])
    ids(graph['assertions'])
    if any(a['subject'] not in graph_ids or a['object'] not in graph_ids for a in graph['assertions']):
        raise PlannerError('dangling frozen graph reference')
    if {a.id.value for a in state.actions} != ids(plan['resolution_actions']) or \
       {r.id.value for r in state.roots} != ids(plan['normalized_root_conditions']) or \
       {s.id.value for s in state.slots} != ids([e for e in graph['entities'] if e['entity_type'] == 'TEMPLATE1_SLOT']):
        raise PlannerError('incomplete E1 projection')
    state = restore_accepted_knowledge(state, plan, pins, root)
    opaque = []
    # Preserve full source records, including identity semantics, original assertions,
    # execution history, authority refs and waiting routes. Not operational truth.
    def retain(path, identity, pointer, value):
        p = m.Provenance(path, identity, pointer, c.canonical_bytes(value).decode(),
                         'P06_PINNED_OPAQUE_RECORD', 'FROZEN_HISTORICAL_REPLAY')
        opaque.append(m.GraphAssertion(m.AssertionId('import:' + path + '#' + pointer), p))
    for ref, document, sections in ((graph_ref, graph, ('entities','assertions')),
                                    (plan_ref, plan, ('execution_history','execution_state','selection_policy'))):
        pin = next(p for p in pins if p.path == ref['path'] and not p.pointer)
        for section in sections:
            rows = document[section]
            if type(rows) is list:
                for index, row in enumerate(rows):
                    retain(pin.path, pin.identity, '/' + section + '/' + str(index), row)
            else:
                retain(pin.path, pin.identity, '/' + section, rows)
    for key, value in checkpoint.items():
        retain(checkpoint_pin.path, checkpoint_pin.identity, '/' + key, value)
    for key, value in manifest.items():
        retain(manifest_pin.path, manifest_pin.identity, '/' + key, value)
    state = replace(state, assertions=state.assertions + tuple(opaque))
    unique_pins = {(p.path,p.pointer,p.profile): p for p in pins}
    policy = next(p for p in pins if p.path.endswith('E1_GRAPH_RESOLUTION_SELECTION_POLICY_1.md'))
    bundle = m.PersistenceBundle(state, (), state, tuple(unique_pins.values()), policy, 'E1-SELECTION-1-P06', 'FULL_FROZEN_E1_REPLAY')
    c.bundle_bytes(bundle)
    return bundle


def plan_output(bundle, source_root=None):
    from . import codec as c, core
    resume = core.resume_eligibility(bundle, source_root)
    state = core.evaluate_satisfaction(bundle.current)
    computation = core.recompute(state)
    return dict(schema='PLANNER-OUTPUT-1', snapshot_identity=c._wire(c.snapshot_id(state)),
        bundle_identity=c._wire(c._identity(c._bundle_bytes_admitted(bundle), "planner-bundle-v1")),
        actionable=[a.value for a in computation.actionable],
        next_action=computation.selection.selected.value if computation.selection else None,
        control=computation.control.value if computation.control else computation.human_routing.value,
        roots={r.id.value:r.state.value for r in state.roots},
        slots={s.id.value:s.state.value for s in state.slots},
        statuses={s.id.value:s.state.value for s in computation.statuses},
        blocked={action.value:list(reasons) for action,reasons in computation.blocked},
        unresolved_roots=sum(r.state.value != 'SATISFIED' for r in state.roots),
        unresolved_slots=sum(s.state.value != 'RESOLVED' for s in state.slots),
        frontier=[g.value for g, _ in computation.frontier], defects=list(computation.defects),
        resume_allowed=resume.allowed, resume_actions=[a.value for a in resume.actions],
        resume_reasons=list(resume.reasons), resume_support=[c._wire(i) for i in resume.supporting_identities],
        selection_trace=dict(criterion=computation.selection.criterion, steps=list(computation.selection.steps)) if computation.selection else None)
