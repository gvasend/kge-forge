"""Canonical pinned replay persistence; full P06 import never resumes live E1."""
from dataclasses import fields, is_dataclass, replace
from enum import Enum
import hashlib
import json
import os
from pathlib import Path
import tempfile

from . import model as m
from .core import apply_event

E1_CANONICALIZATION = ('UTF-8 JSON, sort_keys=True, separators=(comma,colon), '
                       'ensure_ascii=False; hash exact extracted JSON value, not raw whitespace.')
# Closed registry, never import/execute a type named by input bytes.
TYPES = {name: cls for name, cls in vars(m).items()
         if isinstance(cls, type) and cls.__module__ == m.__name__ and
         (is_dataclass(cls) or issubclass(cls, Enum))}
SET_FIELDS = {
    m.EvidenceSourceAdmission: {"requirements", "source_additions", "field_provenance"},
    m.EvidenceIngressContract: {"requirements"},
    m.SourceInvalidation: {'changed'},
    m.BudgetProofMatrix: {'evidence'},
    m.Snapshot: {'budget_matrices', 'actions', 'statuses', 'roots', 'slots', 'knowledge', 'assertions', 'entities', 'predicates', 'information', 'decisions', 'evidence_requirements', 'external_gates', 'receipt_admissions', 'boundaries', 'goals', 'validation_instances'},
    m.Action: {'prerequisites', 'accepted_inventory', 'evidence', 'requirements'},
    m.RootCondition: {'evidence'}, m.ValueSlot: {'evidence', 'requirements', 'root_requirements'},
    m.KnowledgeRecord: {'evidence'}, m.GraphAssertion: {'depends_on'},
    m.EvidenceRequirement: {'producers'}, m.ExternalGate: {'requirements', 'reentry', 'held_actions', 'resolution_contracts'},
    m.ExternalResolutionContract: {'producers', 'reentry', 'held_actions'},
    m.ControlBoundary: {'actions'}, m.Goal: {'entry_actions', 'recovery'},
    m.ReceiptAdmission: {'claims', 'dependencies'}, m.ReceiptObservation: {'claims', 'reasons'},
    m.Predicate: {'operands'}, m.GraphEntity: {'permissions'},
    m.EvaluationContext: {'allowed_effects'}, m.InformationModel: {'alternatives', 'partitions'},
    m.Decision: {'depends_on', 'interferes_with', 'downstream'},
    m.DecisionDossier: {'alternatives', 'checks', 'required_facts', 'deferred_downstream_facts'},
    m.SuppliedResult: {'knowledge'}, m.PersistenceBundle: {'sources'},
}


# Additive P03 fields omit their defaults so existing P02 canonical bytes/IDs
# remain valid. C01 adds the explicit unavailable binding used by fixture v2.
# C02 adds Action.qualification: current proof validity, separate from history.
# Accepted default preserves old encoding; stale source/edge proof is still gated.
# ExternalGate.resolution_contracts is an additive control-only acquisition binding.
# Its absent default preserves existing bytes and never qualifies an old unknown gate.
# Only these explicitly versioned additions may be absent.
P03_FIELDS = {
    m.ReceiptAdmission: {"dependencies"},
    m.ExternalGate: {"resolution_contracts"},
    m.ExecutionEvent: {"resume_binding"},
    m.Predicate: {'obligation', 'unavailable', 'required_outcome'},
    m.KnowledgeRecord: {'producer', 'outcome'},
    m.Snapshot: {'budget_matrices', 'entities', 'predicates', 'context', 'information', 'decisions', 'evidence_requirements', 'external_gates', 'receipt_admissions', 'receipt_observations', 'boundaries', 'goals', 'validation_instances'},
    m.Action: {'requirements', 'authority', 'stage', 'cost', 'cost_unit', 'pass_model_complete', 'accepted_result', 'prepared_dossier', 'qualification'},
    m.RootCondition: {'predicate'},
    m.SuppliedResult: {'expected_snapshot', 'dossier'},
    m.ValueSlot: {'value', 'requirements', 'root_requirements'},
    m.GraphAssertion: {'relation', 'subject', 'object', 'ordering_justification'},
    m.GraphEntity: {'decision', 'choice'},
}


def parse_json(data, allow_floats=False):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise m.PlannerError('duplicate JSON key')
            result[key] = value
        return result

    def no_number(value):
        raise m.PlannerError('unsupported JSON number: ' + value)
    try:
        return json.loads(data, object_pairs_hook=pairs, parse_constant=no_number,
                          parse_float=float if allow_floats else no_number)
    except (ValueError, TypeError, UnicodeError) as exc:
        raise m.PlannerError('invalid JSON: ' + str(exc)) from exc


def canonical_bytes(value):
    def check(obj):
        if obj is None or type(obj) in (str, bool, int):
            return
        if type(obj) is list:
            for child in obj:
                check(child)
            return
        if type(obj) is dict and all(type(k) is str for k in obj):
            for child in obj.values():
                check(child)
            return
        raise m.PlannerError('not a canonical planner JSON value')
    check(value)
    try:
        return json.dumps(value, sort_keys=True, separators=(',', ':'),
                          ensure_ascii=False, allow_nan=False).encode('utf-8')
    except (ValueError, UnicodeError) as exc:
        raise m.PlannerError('invalid canonical text') from exc


def _identity(data, namespace):
    return m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY, namespace,
                              hashlib.sha256(data).hexdigest())


def _wire(value):
    if isinstance(value, Enum):
        return {'$enum': type(value).__name__, 'value': value.value}
    if is_dataclass(value) and type(value).__name__ in TYPES:
        encoded = {'$type': type(value).__name__}
        for field in fields(value):
            if field.name in P03_FIELDS.get(type(value), set()) and getattr(value, field.name) == field.default:
                continue
            item = _wire(getattr(value, field.name))
            if type(value) is m.InformationModel and field.name == 'partitions':
                item = [sorted(part) for part in item]
            if field.name in SET_FIELDS.get(type(value), set()):
                item = sorted(item, key=canonical_bytes)
            encoded[field.name] = item
        return encoded
    if type(value) is tuple:
        return [_wire(item) for item in value]
    if value is None or type(value) in (str, bool, int):
        return value
    raise m.PlannerError('unsupported typed value')


def _unwire(value):
    if type(value) is list:
        return tuple(_unwire(item) for item in value)
    if type(value) is dict:
        tag = value.get('$type', value.get('$enum'))
        cls = TYPES.get(tag) if type(tag) is str else None
        if cls is None:
            raise m.PlannerError('unknown typed tag')
        try:
            if issubclass(cls, Enum):
                if set(value) != {'$enum', 'value'}:
                    raise m.PlannerError('unknown enum fields')
                return cls(value['value'])
            allowed = {'$type'} | {field.name for field in fields(cls)}
            required = allowed - P03_FIELDS.get(cls, set())
            if not required.issubset(value) or not set(value).issubset(allowed):
                raise m.PlannerError('unknown or missing typed fields')
            obj = cls(**{key: _unwire(v) for key, v in value.items() if key != '$type'})
            m.validate_types(obj, cls)
            return obj
        except (ValueError, TypeError) as exc:
            raise m.PlannerError('invalid typed record: ' + str(exc)) from exc
    if value is None or type(value) in (str, bool, int):
        return value
    raise m.PlannerError('unsupported typed scalar')


def snapshot_bytes(snapshot):
    m.validate_model(snapshot)
    return canonical_bytes({'schema': 'PLANNER-SNAPSHOT-1', 'snapshot': _wire(snapshot)})


def snapshot_id(snapshot):
    return _identity(snapshot_bytes(snapshot), 'planner-snapshot-v1')


def decode_snapshot(data):
    value = parse_json(data)
    if type(value) is not dict or set(value) != {'schema', 'snapshot'} or \
            value['schema'] != 'PLANNER-SNAPSHOT-1':
        raise m.PlannerError('unknown snapshot schema')
    snapshot = _unwire(value['snapshot'])
    m.validate_model(snapshot)
    return snapshot


def _path(root, relative):
    if type(relative) is not str or not relative or Path(relative).is_absolute() or \
            '..' in Path(relative).parts or Path(relative).as_posix() != relative:
        raise m.PlannerError('noncanonical relative source path')
    root = Path(root).resolve()
    path = root / relative
    if path.resolve() != path:
        raise m.PlannerError('symlinked source path')
    return path


def json_pointer(value, pointer):
    if type(pointer) is not str or (pointer and not pointer.startswith('/')):
        raise m.PlannerError('invalid JSON pointer')
    for token in pointer.split('/')[1:] if pointer else ():
        if '~' in token.replace('~0', '').replace('~1', ''):
            raise m.PlannerError('invalid pointer escape')
        token = token.replace('~1', '/').replace('~0', '~')
        try:
            if type(value) is list:
                if not token.isascii() or not token.isdigit() or str(int(token)) != token:
                    raise m.PlannerError('noncanonical array index')
                value = value[int(token)]
            elif type(value) is dict:
                value = value[token]
            else:
                raise m.PlannerError('pointer crosses scalar')
        except (KeyError, IndexError) as exc:
            raise m.PlannerError('missing JSON pointer') from exc
    return value


def validate_pin(pin):
    m.validate_types(pin, m.ArtifactPin)
    if pin.identity.kind is not m.IdentityKind.CONTENT_IDENTITY or \
            pin.identity.namespace != pin.profile.value:
        raise m.PlannerError('pin identity type/hash domain mismatch')
    if pin.profile is m.HashProfile.RAW and pin.pointer:
        raise m.PlannerError('raw pin cannot project a JSON value')


def load_pinned(root, pin):
    validate_pin(pin)
    try:
        raw = _path(root, pin.path).read_bytes()
    except OSError as exc:
        raise m.PlannerError('pinned source unavailable') from exc
    if pin.profile is m.HashProfile.RAW:
        hashed, value = raw, raw
    else:
        value = json_pointer(parse_json(raw, allow_floats=pin.profile is m.HashProfile.E1_EMBEDDED_JSON),
                             pin.pointer)
        if pin.profile is m.HashProfile.PLANNER_JSON:
            hashed = canonical_bytes(value)
        else:
            hashed = json.dumps(value, sort_keys=True, separators=(',', ':'),
                                ensure_ascii=False, allow_nan=False).encode('utf-8')
    if _identity(hashed, pin.profile.value) != pin.identity:
        raise m.PlannerError('pinned source changed: ' + pin.path + pin.pointer)
    return value


def read_e1_manifest(root, manifest_pin):
    """Verify raw and embedded references only; no operational state is restored."""
    if manifest_pin.profile is not m.HashProfile.RAW:
        raise m.PlannerError('manifest requires raw pin')
    manifest = parse_json(load_pinned(root, manifest_pin))
    if type(manifest) is not dict or manifest.get('schema') != 'E1-RESUME-MANIFEST-1':
        raise m.PlannerError('unknown E1 resume manifest')
    pins = {}

    def visit(value):
        if type(value) is dict:
            pin = None
            if 'raw_sha256' in value:
                pin = m.ArtifactPin(value.get('path'), m.ArtifactIdentity(
                    m.IdentityKind.CONTENT_IDENTITY, m.HashProfile.RAW.value, value['raw_sha256']))
            elif 'json_pointer' in value:
                if value.get('canonicalization') != E1_CANONICALIZATION:
                    raise m.PlannerError('unsupported E1 embedded hash rule')
                profile = m.HashProfile.E1_EMBEDDED_JSON
                pin = m.ArtifactPin(value.get('container'), m.ArtifactIdentity(
                    m.IdentityKind.CONTENT_IDENTITY, profile.value, value.get('sha256')),
                    profile, value['json_pointer'])
            if pin:
                validate_pin(pin)
                key = (pin.path, pin.pointer, pin.profile.value)
                if key in pins and pins[key] != pin:
                    raise m.PlannerError('conflicting manifest source pins')
                pins[key] = pin
            for child in value.values():
                visit(child)
        elif type(value) is list:
            for child in value:
                visit(child)
    visit(manifest)
    required = {'/execution_history', '/execution_state', '/selection_policy'}
    if not required.issubset({p.pointer for p in pins.values()}):
        raise m.PlannerError('incomplete E1 embedded manifest references')
    result = tuple(pins[key] for key in sorted(pins))
    for pin in result:
        load_pinned(root, pin)
    return result


def invalidate_sources(snapshot, changed):
    """Pure invalidation on exact old content identities; no facts or authority inferred."""
    m.validate_model(snapshot)
    changed = frozenset(changed)
    for identity in changed:
        m.validate_types(identity, m.ArtifactIdentity)
        if identity.kind is not m.IdentityKind.CONTENT_IDENTITY:
            raise m.PlannerError('source invalidation requires content identity')
    stale = {a.id for a in snapshot.assertions if a.validation is m.ValidationState.STALE or
             a.provenance.identity in changed}
    while True:
        expanded = stale | {a.id for a in snapshot.assertions if stale.intersection(a.depends_on)}
        if expanded == stale:
            break
        stale = expanded
    def affected(record):
        return bool(stale.intersection(record.evidence))
    def knowledge(record):
        return replace(record, validation=m.ValidationState.STALE) if (
            affected(record) or record.provenance.identity in changed) else record
    stale_entities = {e.id for e in snapshot.entities if e.validation is m.ValidationState.STALE or
                      e.provenance.identity in changed}
    stale_knowledge = {k.id for k in snapshot.knowledge if knowledge(k).validation is m.ValidationState.STALE}
    stale_roots = {r.id for r in snapshot.roots if affected(r) or r.state is m.ConditionState.STALE}
    stale_obligations={r.id for r in snapshot.evidence_requirements if r.provenance.identity in changed}
    for admission in snapshot.receipt_admissions:
        auth=next(p for p in snapshot.predicates if p.id==admission.authentication)
        if admission.artifact in stale_entities or auth.entity in stale_entities or admission.provenance.identity in changed or any(p.identity in changed for p in admission.dependencies):
            if any(p.identity in changed for p in admission.dependencies):
                stale_entities.add(admission.artifact)
            stale_obligations.update(c.requirement for c in admission.claims)
    stale_predicates = {p.id for p in snapshot.predicates if p.obligation in stale_obligations}
    while True:
        new_predicates = stale_predicates | {p.id for p in snapshot.predicates if
            p.entity in stale_entities or p.other in stale_entities or p.knowledge in stale_knowledge or
            p.condition in stale_roots or (bool(p.operands) and
                (all(ref in stale_predicates for ref in p.operands) if p.kind is m.PredicateKind.ANY
                 else bool(stale_predicates.intersection(p.operands))))}
        new_roots = stale_roots | {r.id for r in snapshot.roots if r.predicate in new_predicates}
        if new_predicates == stale_predicates and new_roots == stale_roots:
            break
        stale_predicates, stale_roots = new_predicates, new_roots
    held = {a.id for a in snapshot.actions if affected(a) or a.source.identity in changed or
            any(affected(k) or k.provenance.identity in changed for k in a.accepted_inventory)}
    held.update(a.id for a in snapshot.actions if stale_predicates.intersection(a.requirements) or
                a.authority in stale_predicates)
    def stale_dossier(dossier):
        if dossier is None:
            return None
        stale_proof = stale_predicates.intersection(dossier.required_facts) or any(
            c.predicate in stale_predicates or c.provenance.identity in changed for c in dossier.checks)
        return replace(dossier, validation=m.ValidationState.STALE) if (
            dossier.provenance.identity in changed or stale_proof) else dossier
    decision_states = []
    for d in snapshot.decisions:
        dossier = stale_dossier(d.dossier)
        if d.provenance.identity in changed and dossier is not None:
            dossier = replace(dossier, validation=m.ValidationState.STALE)
        if d.provenance.identity in changed or (dossier is not None and dossier.validation is m.ValidationState.STALE):
            held.update((d.action,) + d.downstream)
            if d.input_action is not None:
                held.add(d.input_action)
        decision_states.append(replace(d, dossier=dossier))
    for action in snapshot.actions:
        prepared = stale_dossier(action.prepared_dossier)
        if prepared is not None and prepared.validation is m.ValidationState.STALE:
            held.add(action.id)
    stale_external={g.id for g in snapshot.external_gates if g.provenance.identity in changed or
        any(c.provenance.identity in changed for c in g.resolution_contracts) or any(
        r.provenance.identity in changed for r in snapshot.evidence_requirements if r.id in g.requirements)}
    for gate in snapshot.external_gates:
        if gate.id in stale_external or any(o.gate==gate.id and o.artifact in stale_entities for o in snapshot.receipt_observations):
            held.update(gate.reentry+gate.held_actions)
    invalidated = replace(snapshot,
        external_gates=tuple(replace(g,validation=m.ValidationState.STALE) if g.id in stale_external else g for g in snapshot.external_gates),
        decisions=tuple(decision_states),
        entities=tuple(replace(e, validation=m.ValidationState.STALE) if e.id in stale_entities else e
                       for e in snapshot.entities),
        information=tuple(replace(i, validation=m.ValidationState.STALE) if i.provenance.identity in changed else i
                          for i in snapshot.information),
        assertions=tuple(replace(a, validation=m.ValidationState.STALE) if a.id in stale else a
                         for a in snapshot.assertions),
        roots=tuple(replace(r, state=m.ConditionState.STALE) if r.id in stale_roots else r for r in snapshot.roots),
        slots=tuple(replace(s, state=m.SlotState.STALE) if (affected(s) or s.value in stale_entities or
            stale_predicates.intersection(s.requirements) or stale_roots.intersection(s.root_requirements)) else s for s in snapshot.slots),
        knowledge=tuple(knowledge(k) for k in snapshot.knowledge),
        actions=tuple(replace(a, qualification=m.ValidationState.STALE if a.id in held else a.qualification, prepared_dossier=stale_dossier(a.prepared_dossier), accepted_inventory=tuple(knowledge(k) for k in a.accepted_inventory))
                      for a in snapshot.actions),
        statuses=tuple(replace(s, state=m.ActionState.WAITING) if s.id in held and s.state is not m.ActionState.COMPLETED else s
                       for s in snapshot.statuses),
        validation_instances=tuple(
            replace(v, result=m.ValidationOutcome.STALE, currentness=m.ValidationState.STALE)
            if (v.predicate in stale_predicates or v.provenance.identity in changed or
                any(i in changed for i in v.inputs)) else v
            for v in snapshot.validation_instances))

    # Propagate current qualification loss through the retained ordering graph.
    from .gates import unavailable_support
    unavailable = unavailable_support(invalidated)
    return replace(invalidated,
        entities=tuple(replace(e, validation=m.ValidationState.STALE) if e.id in unavailable else e for e in invalidated.entities),
        actions=tuple(replace(a, qualification=m.ValidationState.STALE) if a.id in unavailable else a for a in invalidated.actions),
        roots=tuple(replace(r, state=m.ConditionState.STALE) if r.id in unavailable else r for r in invalidated.roots),
        slots=tuple(replace(v, state=m.SlotState.STALE) if v.id in unavailable else v for v in invalidated.slots),
        knowledge=tuple(replace(k, validation=m.ValidationState.STALE) if k.id in unavailable else k for k in invalidated.knowledge),
        statuses=tuple(replace(s, state=m.ActionState.WAITING) if s.id in unavailable and
            s.state is not m.ActionState.COMPLETED else s for s in invalidated.statuses))


def resume_binding(bundle):
    """C03 exact policy/suspension-context binding, not C05 policy qualification."""
    return _identity(canonical_bytes({'schema': 'RESUME-EVENT-BINDING-1',
        'policy': _wire(bundle.policy), 'policy_version': bundle.policy_version,
        'scope': bundle.scope}), 'planner-resume-binding-v1')


def _event_identity(sequence, parent, parent_event, result, after, resume_binding=None):
    body = {'sequence': sequence, 'parent': _wire(parent),
        'parent_event': _wire(parent_event), 'result': _wire(result), 'after': _wire(after)}
    if resume_binding is not None:
        body['resume_binding'] = _wire(resume_binding)
    return _identity(canonical_bytes(body), 'planner-event-v1')


def _replay(bundle):
    m.validate_types(bundle, m.PersistenceBundle)
    from .selector import validate_policy
    validate_policy(bundle.policy, bundle.policy_version)
    if bundle.policy_version not in ('E1-SELECTION-1-P01-SUBSET', 'E1-SELECTION-1-P03', 'E1-SELECTION-1-P04', 'E1-SELECTION-1-P05', 'E1-SELECTION-1-P06') or bundle.scope not in ('PARTIAL_HISTORICAL_REPLAY', 'FULL_FROZEN_E1_REPLAY', 'PARTIAL_SYNTHETIC_BUDGET_QUALIFICATION'):
        raise m.PlannerError('unsupported replay bundle policy/scope')
    if any(s.budget_matrices for s in (bundle.initial,bundle.current)) and bundle.scope != 'PARTIAL_SYNTHETIC_BUDGET_QUALIFICATION':
        raise m.PlannerError('synthetic budget contract cannot become real E1 evidence')
    if bundle.scope == 'FULL_FROZEN_E1_REPLAY' and bundle.policy_version != 'E1-SELECTION-1-P06':
        raise m.PlannerError('full import requires P06 policy')
    m.validate_model(bundle.initial)
    m.validate_model(bundle.current)
    if bundle.policy_version == 'E1-SELECTION-1-P01-SUBSET':
        for state in (bundle.initial, bundle.current):
            if state.entities or state.predicates or state.context or state.information or any(
                a.operation is not m.OperationClass.SOURCE_ACQUISITION or a.requirements or
                a.authority is not None or a.stage is not m.ActionStage.DEFAULT or a.cost is not None or
                a.pass_model_complete for a in state.actions) or any(a.relation is not None for a in state.assertions) or any(
                r.predicate is not None for r in state.roots) or any(s.value is not None or s.requirements or
                s.root_requirements for s in state.slots):
                raise m.PlannerError('extended state requires P03 policy version')
    if bundle.policy_version not in ('E1-SELECTION-1-P04','E1-SELECTION-1-P05','E1-SELECTION-1-P06') and any(state.decisions or any(
            a.prepared_dossier is not None or a.accepted_result is not m.ActionResult.PASS
            for a in state.actions) or any(e.decision is not None or e.choice is not None for e in state.entities) for state in (bundle.initial, bundle.current)):
        raise m.PlannerError('decision state requires P04 policy version')
    if bundle.policy_version not in ('E1-SELECTION-1-P05','E1-SELECTION-1-P06') and any(state.external_gates or state.goals or state.boundaries or
            state.evidence_requirements or state.receipt_admissions or state.receipt_observations or
            any(p.obligation is not None for p in state.predicates) or any(type(v.required_type) is m.ValueType for v in state.slots)
            for state in (bundle.initial,bundle.current)):
        raise m.PlannerError('external state requires P05 policy')
    for pin in bundle.sources + (bundle.policy,):
        validate_pin(pin)
    m.unique(bundle.sources, lambda p: (p.path, p.pointer, p.profile))
    # Every provenance source must be pinned in the bundle, not just named in state.
    raw_sources = {(p.path, p.identity) for p in bundle.sources if p.profile is m.HashProfile.RAW}
    for snapshot in (bundle.initial, bundle.current):
        provenances = [a.source for a in snapshot.actions] + [a.provenance for a in snapshot.assertions]
        provenances += [k.provenance for k in snapshot.knowledge]
        provenances += [e.provenance for e in snapshot.entities] + [i.provenance for i in snapshot.information]
        provenances += [k.provenance for a in snapshot.actions for k in a.accepted_inventory]
        provenances += decision_provenances(snapshot) + external_provenances(snapshot)
        if any((p.path, p.identity) not in raw_sources for p in provenances):
            raise m.PlannerError('missing provenance source pin')
    admissions = [e.result for e in bundle.events if type(e.result) is m.EvidenceSourceAdmission]
    additions = tuple(p for a in admissions for p in a.source_additions)
    m.unique(additions, lambda p: (p.path,p.pointer,p.profile))
    if any(p not in bundle.sources for p in additions):
        raise m.PlannerError('SOURCE_ADDITIONS_MISSING')
    prefix_sources = tuple(p for p in bundle.sources if p not in additions)
    if admissions:
        _check_snapshot_pins(bundle.initial, prefix_sources)
    state, parent_event = bundle.initial, None
    for sequence, event in enumerate(bundle.events, 1):
        if event.sequence != sequence or event.parent_snapshot != snapshot_id(state) or \
                event.parent_event != parent_event:
            raise m.PlannerError('ledger sequence/parent mismatch')
        if event.identity != _event_identity(sequence, event.parent_snapshot,
                                             parent_event, event.result, event.after_snapshot, event.resume_binding):
            raise m.PlannerError('event identity mismatch')
        if type(event.result) is m.EvidenceSourceAdmission:
            a = event.result
            prefix = replace(bundle, events=bundle.events[:sequence-1], current=state, sources=prefix_sources)
            expected = _identity(_bundle_bytes_admitted(prefix), 'planner-bundle-v1')
            if a.expected_bundle != expected or a.expected_parent_event != parent_event:
                raise m.PlannerError('ADMISSION_PREFIX_MISMATCH')
            invalidated = {identity for previous in bundle.events[:sequence-1]
                           if type(previous.result) is m.SourceInvalidation for identity in previous.result.changed}
            support = {p.identity for p in a.admission.dependencies} | {a.contract_pin, a.entity.identity}
            if support.intersection(invalidated):
                raise m.PlannerError('ADMISSION_SOURCE_ALREADY_INVALIDATED')
            if a.contract_pin not in {p.identity for p in prefix_sources}:
                raise m.PlannerError('INGRESS_PIN_MISSING')
            for binding in a.field_provenance:
                if binding.provenance.identity != a.entity.identity and not any(
                        p.path==binding.provenance.path and p.identity==binding.provenance.identity for p in prefix_sources):
                    raise m.PlannerError('FIELD_SOURCE_NOT_IN_PREFIX')
            if sequence >= len(bundle.events):
                raise m.PlannerError('UNPAIRED_ADMISSION')
            follow = bundle.events[sequence].result
            if type(follow) is not m.ExternalEvent or follow.stage is not m.ExternalStage.EVIDENCE_RECEIVED or follow.gate != a.gate or follow.artifact != a.entity.id:
                raise m.PlannerError('ADMISSION_RECEIPT_PAIR')
            prefix_sources += a.source_additions
        state = apply_event(state, event.result).snapshot
        if admissions:
            _check_snapshot_pins(state, prefix_sources)
        if event.after_snapshot != snapshot_id(state):
            raise m.PlannerError('event outcome mismatch')
        parent_event = event.identity
    if snapshot_id(state) != snapshot_id(bundle.current):
        raise m.PlannerError('ledger/current state mismatch')
    return state


def append_event(bundle, event):
    _replay(bundle)
    m.validate_types(event, m.ExecutionEvent)
    for existing in bundle.events:
        if existing.identity == event.identity:
            if canonical_bytes(_wire(existing)) != canonical_bytes(_wire(event)):
                raise m.PlannerError('conflicting event replay')
            return bundle
    after = apply_event(bundle.current, event.result).snapshot
    updated = replace(bundle, events=bundle.events + (event,), current=after)
    _replay(updated)
    return updated


def record_result(bundle, supplied):
    _replay(bundle)
    after = apply_event(bundle.current, supplied).snapshot
    sequence = len(bundle.events) + 1
    parent = snapshot_id(bundle.current)
    parent_event = bundle.events[-1].identity if bundle.events else None
    after_id = snapshot_id(after)
    binding = resume_binding(bundle) if (type(supplied) is m.DecisionReentry or
        (type(supplied) is m.ExternalEvent and supplied.stage is m.ExternalStage.DEPENDENT_ACTION_REENTRY)) else None
    event = m.ExecutionEvent(sequence, parent, parent_event, supplied, after_id,
        _event_identity(sequence, parent, parent_event, supplied, after_id, binding), binding)
    return append_event(bundle, event)


def _bundle_bytes_admitted(bundle):
    return canonical_bytes({'schema': 'PLANNER-BUNDLE-1', 'bundle': _wire(bundle)})


def bundle_bytes(bundle):
    _replay(bundle)
    return _bundle_bytes_admitted(bundle)


def bundle_id(bundle):
    return _identity(bundle_bytes(bundle), 'planner-bundle-v1')


def _verify_sources(bundle, root):
    for pin in bundle.sources + (bundle.policy,):
        load_pinned(root, pin)


def _write_immutable(directory, name, raw):
    target = directory / name
    if target.exists():
        if target.is_symlink() or target.read_bytes() != raw:
            raise m.PlannerError('immutable output conflict')
        return target
    fd, temporary = tempfile.mkstemp(prefix='.planner-', dir=str(directory))
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        # Atomic create-without-overwrite: earlier ledger records cannot be replaced.
        try:
            os.link(temporary, str(target))
        except FileExistsError:
            if target.is_symlink() or target.read_bytes() != raw:
                raise m.PlannerError('immutable output conflict')
    finally:
        os.unlink(temporary)
    return target


def save_bundle(bundle, output_dir, repo_root):
    raw = bundle_bytes(bundle)
    _verify_sources(bundle, repo_root)
    directory = Path(output_dir).absolute()
    if directory.resolve() != directory:
        raise m.PlannerError('symlinked output directory')
    frozen_roots = (Path(repo_root).resolve() / 'docs/experiments/E1',
                    Path(__file__).resolve().parents[2] / 'docs/experiments/E1')
    if any(directory == frozen or frozen in directory.parents for frozen in frozen_roots):
        raise m.PlannerError('E1 is read-only')
    directory.mkdir(parents=True, exist_ok=True)
    for event in bundle.events:
        _write_immutable(directory, 'event-' + event.identity.sha256 + '.json', canonical_bytes(_wire(event)))
    identity = _identity(raw, 'planner-bundle-v1')
    return _write_immutable(directory, 'bundle-' + identity.sha256 + '.json', raw), identity


def restore(path, expected_identity, repo_root):
    m.validate_types(expected_identity, m.ArtifactIdentity)
    try:
        path = Path(path).absolute()
        if path.resolve() != path:
            raise m.PlannerError('symlinked bundle')
        raw = path.read_bytes()
    except OSError as exc:
        raise m.PlannerError('bundle unavailable') from exc
    if _identity(raw, 'planner-bundle-v1') != expected_identity:
        raise m.PlannerError('bundle identity mismatch')
    value = parse_json(raw)
    if type(value) is not dict or set(value) != {'schema', 'bundle'} or value['schema'] != 'PLANNER-BUNDLE-1':
        raise m.PlannerError('unknown bundle schema')
    bundle = _unwire(value['bundle'])
    if bundle_bytes(bundle) != raw:
        raise m.PlannerError('noncanonical bundle')
    _verify_sources(bundle, repo_root)
    # Verify immutable ledger artifacts too, not only the embedded copy.
    for event in bundle.events:
        event_path = path.parent / ('event-' + event.identity.sha256 + '.json')
        if event_path.is_symlink() or not event_path.is_file() or \
                event_path.read_bytes() != canonical_bytes(_wire(event)):
            raise m.PlannerError('ledger artifact missing or changed')
    return bundle


def decision_provenances(snapshot):
    sources = [d.provenance for d in snapshot.decisions]
    for dossier in tuple(d.dossier for d in snapshot.decisions) + tuple(a.prepared_dossier for a in snapshot.actions):
        if dossier is not None:
            sources.append(dossier.provenance)
            sources.extend(c.provenance for c in dossier.checks)
    return sources


def external_provenances(snapshot):
    return [p for a in snapshot.receipt_admissions for p in a.dependencies] + [c.provenance for g in snapshot.external_gates for c in g.resolution_contracts] + [item.provenance for seq in (snapshot.evidence_requirements,snapshot.external_gates,
            snapshot.receipt_admissions,snapshot.boundaries,snapshot.goals) for item in seq]


def _check_snapshot_pins(snapshot, pins):
    from .replay import provenance_records
    allowed = {(p.path,p.identity) for p in pins if p.profile is m.HashProfile.RAW}
    sources = provenance_records(snapshot) + external_provenances(snapshot)
    if any((p.path,p.identity) not in allowed for p in sources):
        raise m.PlannerError('SOURCE_NOT_AVAILABLE_AT_PREFIX')


def _fsync_directory(path):
    descriptor = os.open(str(path), os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _transaction_directory(output_dir, repo_root):
    directory = Path(output_dir).absolute()
    if directory.resolve() != directory:
        raise m.PlannerError('symlinked transaction directory')
    for frozen in (Path(repo_root).resolve()/'docs/experiments/E1',
                   Path(__file__).resolve().parents[2]/'docs/experiments/E1'):
        if directory == frozen or frozen in directory.parents:
            raise m.PlannerError('E1 is read-only')
    missing = []
    ancestor = directory
    while not ancestor.exists():
        missing.append(ancestor); ancestor = ancestor.parent
    directory.mkdir(parents=True, exist_ok=True)
    for created in reversed(missing):
        _fsync_directory(created); _fsync_directory(created.parent)
    return directory


def _publish_head(directory, bundle, previous, command, repo_root):
    path, identity = save_bundle(bundle, directory, repo_root)
    _fsync_directory(directory)
    raw = canonical_bytes({'schema':'PLANNER-HEAD-1', 'bundle':_wire(identity),
                           'previous':_wire(previous), 'command':_wire(command)})
    fd, temporary = tempfile.mkstemp(prefix='.head-',dir=str(directory))
    try:
        with os.fdopen(fd,'wb') as stream:
            stream.write(raw); stream.flush(); os.fsync(stream.fileno())
        _verify_sources(bundle, repo_root)
        os.replace(temporary, str(directory/'HEAD.json'))
        _fsync_directory(directory)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    return identity


def _read_head(directory, fallback, repo_root):
    head = directory/'HEAD.json'
    if not head.exists():
        return fallback
    if head.is_symlink():
        raise m.PlannerError('symlinked head')
    value = parse_json(head.read_bytes())
    if type(value) is not dict or set(value) != {'schema','bundle','previous','command'} or value['schema'] != 'PLANNER-HEAD-1':
        raise m.PlannerError('head schema')
    if canonical_bytes(value) != head.read_bytes():
        raise m.PlannerError('noncanonical head')
    identity = _unwire(value['bundle'])
    bundle = restore(directory/('bundle-'+identity.sha256+'.json'),identity,repo_root)
    count = len(bundle.events)
    if not count:
        raise m.PlannerError('head without committed event')
    command = None
    prior_count = count-1
    if count >= 2 and type(bundle.events[-2].result) is m.EvidenceSourceAdmission:
        prior_count = count-2
        command = bundle.events[-2].result.command_key
    prefix = _prefix_bundle(bundle,prior_count)
    if _unwire(value['previous']) != bundle_id(prefix) or _unwire(value['command']) != command:
        raise m.PlannerError('HEAD_AUDIT_MISMATCH')
    return bundle


def _transaction_lock(directory):
    # Single local writer, no distributed or parallel command semantics.
    import fcntl
    from contextlib import contextmanager
    @contextmanager
    def locked():
        descriptor = os.open(str(directory/'LOCK'),os.O_RDWR|os.O_CREAT|os.O_NOFOLLOW,0o600)
        try:
            fcntl.flock(descriptor,fcntl.LOCK_EX)
            yield
        finally:
            fcntl.flock(descriptor,fcntl.LOCK_UN); os.close(descriptor)
    return locked()


def _extend_private(bundle, supplied):
    after = apply_event(bundle.current,supplied).snapshot
    sequence = len(bundle.events)+1
    parent, previous = snapshot_id(bundle.current), bundle.events[-1].identity if bundle.events else None
    after_id = snapshot_id(after)
    event = m.ExecutionEvent(sequence,parent,previous,supplied,after_id,
        _event_identity(sequence,parent,previous,supplied,after_id))
    return replace(bundle,events=bundle.events+(event,),current=after)


def admit_external_evidence(bundle, request, source_bytes, output_dir, repo_root):
    """Commit a new source admission + receipt, or return an exact committed retry.

    bundle is the caller's trusted parent, not an arbitrary discovered head. The
    returned tuple is (current bundle, original transaction bundle identity, noop).
    No validation or reentry event is synthesized here.
    """
    m.validate_types(request,m.EvidenceSourceAdmission)
    _replay(bundle); _verify_sources(bundle,repo_root)
    directory = _transaction_directory(output_dir,repo_root)
    with _transaction_lock(directory):
        current = _read_head(directory,bundle,repo_root)
        _replay(current); _verify_sources(current,repo_root)
        if canonical_bytes(_wire(current.initial)) != canonical_bytes(_wire(bundle.initial)) or canonical_bytes(_wire(current.events[:len(bundle.events)])) != canonical_bytes(_wire(bundle.events)) or any(p not in current.sources for p in bundle.sources):
            raise m.PlannerError('UNTRUSTED_HEAD_LINEAGE')
        for index, event in enumerate(current.events):
            old = event.result
            if type(old) is m.EvidenceSourceAdmission and old.command_key == request.command_key:
                if canonical_bytes(_wire(old)) != canonical_bytes(_wire(request)):
                    raise m.PlannerError('IDEMPOTENCY_CONFLICT')
                if request.expected_bundle != bundle_id(bundle):
                    raise m.PlannerError('RETRY_PARENT_MISMATCH')
                original_events = current.events[:index+2]
                later = {p for e in current.events[index+2:] if type(e.result) is m.EvidenceSourceAdmission for p in e.result.source_additions}
                state = current.initial
                for old_event in original_events:
                    state = apply_event(state,old_event.result).snapshot
                original = replace(current,events=original_events,current=state,sources=tuple(p for p in current.sources if p not in later))
                return current,bundle_id(original),True
        if bundle_id(current) != bundle_id(bundle) or request.expected_bundle != bundle_id(current):
            raise m.PlannerError('PARENT_MISMATCH')
        if request.expected_parent_event != (current.events[-1].identity if current.events else None):
            raise m.PlannerError('PARENT_MISMATCH')
        if type(source_bytes) is not dict or set(source_bytes) != {p.path for p in request.source_additions}:
            raise m.PlannerError('SOURCE_BYTES_SET')
        for pin in request.source_additions:
            validate_pin(pin)
            raw = source_bytes[pin.path]
            if type(raw) is not bytes or pin.profile is not m.HashProfile.RAW or _identity(raw,'raw-file-sha256') != pin.identity:
                raise m.PlannerError('SOURCE_CONTENT_PIN')
            if raw.decode('utf-8') != request.entity.provenance.excerpt:
                raise m.PlannerError('SOURCE_BYTES_PROVENANCE')
        admitted = _extend_private(current,request)
        receipt = m.ExternalEvent(request.gate,m.ExternalStage.EVIDENCE_RECEIVED,snapshot_id(admitted.current),request.entity.id)
        updated = _extend_private(admitted,receipt)
        updated = replace(updated,sources=current.sources+request.source_additions)
        _replay(updated)
        from .core import recompute
        if recompute(current.current) != recompute(updated.current):
            raise m.PlannerError('RECEIPT_CHANGED_CONTROL')
        # Validate everything before creating source files. Orphan immutable files
        # after a crash are not visible to a committed canonical head.
        for pin in request.source_additions:
            target = Path(repo_root).resolve()/pin.path
            parent = _transaction_directory(target.parent,repo_root)
            _write_immutable(parent,target.name,source_bytes[pin.path])
            _fsync_directory(parent)
        _verify_sources(current,repo_root)
        identity = _publish_head(directory,updated,bundle_id(current),request.command_key,repo_root)
        return updated,identity,False


def commit_event(bundle, supplied, output_dir, repo_root):
    """Durable later validation/reentry/invalidation under the same head lock."""
    directory = _transaction_directory(output_dir,repo_root)
    with _transaction_lock(directory):
        current = _read_head(directory,bundle,repo_root)
        if bundle_id(current) != bundle_id(bundle):
            raise m.PlannerError('PARENT_MISMATCH')
        _verify_sources(current,repo_root)
        updated = record_result(current,supplied)
        identity = _publish_head(directory,updated,bundle_id(current),None,repo_root)
        return updated,identity


def _prefix_bundle(bundle, count):
    state = bundle.initial
    for event in bundle.events[:count]:
        state = apply_event(state,event.result).snapshot
    later = {p for e in bundle.events[count:] if type(e.result) is m.EvidenceSourceAdmission for p in e.result.source_additions}
    return replace(bundle,events=bundle.events[:count],current=state,sources=tuple(p for p in bundle.sources if p not in later))
