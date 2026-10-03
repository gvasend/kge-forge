"""Pure graph projection, finite propagation and bounded action-result application."""
from typing import Tuple, Optional
from dataclasses import dataclass, replace
from . import model as m
# Public core entry points admit the snapshot via validate_model/project before
# evaluating predicates. Keep public gate admission without repeating it per node.
from .gates import blockers, validate_result, evaluate_predicate, _evaluate_predicate as _evaluate_admitted, usable, decision_readiness, recorded_decision_valid, check_receipt, external_complete, _check_receipt as _check_receipt_admitted, _external_complete as _external_complete_admitted
from .gates import unavailable_support, current_completion, governed_external_unknown
from .selector import SelectionTrace, select


@dataclass(frozen=True)
class Projection:
    edges: tuple  # (prerequisite, dependent), typed IDs
    order: tuple
    defects: Tuple[str, ...]


def _key(ref):
    return (type(ref).__name__, ref.value)


def project(snapshot):
    m.validate_model(snapshot)
    nodes = {item.id for seq in (snapshot.actions, snapshot.roots, snapshot.slots, snapshot.entities) for item in seq}
    metadata = {(gate.target, action.id) for action in snapshot.actions for gate in action.prerequisites}
    declared, defects = set(), []
    has_ordering = False
    for assertion in snapshot.assertions:
        if assertion.relation is None:
            continue
        if assertion.relation is m.Relation.REQUIRES:
            has_ordering = True
            if not assertion.ordering_justification:
                defects.append('ORDERING_JUSTIFICATION_MISSING:' + assertion.id.value)
            else:
                declared.add((assertion.object, assertion.subject))
        elif assertion.ordering_justification:
            defects.append('NON_ORDERING_RELATION:' + assertion.id.value)
    if has_ordering:
        action_ids = {a.id for a in snapshot.actions}
        represented = {edge for edge in declared if edge[1] in action_ids}
        for edge in metadata.symmetric_difference(represented):
            defects.append('PREREQUISITE_METADATA_MISMATCH:' + edge[0].value + '->' + edge[1].value)
    edges = metadata | declared | {(ref, d.action) for d in snapshot.decisions for ref in d.depends_on}
    remaining = set(nodes)
    order = []
    while remaining:
        ready = sorted((node for node in remaining if not any(
            before in remaining and after == node for before, after in edges)), key=_key)
        if not ready:
            defects.append('PREREQUISITE_CYCLE')
            break
        order.extend(ready)
        remaining.difference_update(ready)
    return Projection(tuple(sorted(edges, key=lambda e: (_key(e[0]), _key(e[1])))),
                      tuple(order), tuple(sorted(set(defects))))


def _predicate_refs(snapshot, ref, seen=()):
    if ref is None or ref in seen:
        return set(), set(), set()
    p = next(p for p in snapshot.predicates if p.id == ref)
    kinds, knowledge, roots = {p.kind}, set(), set()
    if p.knowledge is not None:
        knowledge.add(p.knowledge)
    if p.condition is not None:
        roots.add(p.condition)
    for child in p.operands:
        k, known, r = _predicate_refs(snapshot, child, seen + (ref,))
        kinds.update(k); knowledge.update(known); roots.update(r)
    return kinds, knowledge, roots


def evaluate_satisfaction(snapshot):
    """Derive independent conditions from proofs, never from a PASS label."""
    m.validate_model(snapshot)
    projection = project(snapshot)
    if projection.defects:
        raise m.PlannerError('invalid prerequisite projection')
    unavailable = unavailable_support(snapshot)
    def prerequisites_met(node, current):
        if node in unavailable:
            return False
        roots = {r.id: r.state for r in current.roots}
        actions = {a.id: a.state for a in current.statuses}
        slots = {v.id: v.state for v in current.slots}
        entities = {e.id: e for e in current.entities}
        for before, after in projection.edges:
            if after != node:
                continue
            met = (roots.get(before) is m.ConditionState.SATISFIED or
                   (before in actions and current_completion(current, before)) or
                   slots.get(before) is m.SlotState.RESOLVED or
                   (before in entities and usable(entities[before], current).state is m.ProofState.PROVED))
            if not met:
                return False
        return True
    snapshot = replace(snapshot,
        roots=tuple(replace(r, state=m.ConditionState.STALE) if r.id in unavailable else r for r in snapshot.roots),
        slots=tuple(replace(v, state=m.SlotState.STALE) if v.id in unavailable else v for v in snapshot.slots))
    state = replace(snapshot, roots=tuple(replace(r, state=m.ConditionState.UNRESOLVED)
        if r.predicate is not None and r.state is not m.ConditionState.STALE else r for r in snapshot.roots))
    for _ in range(len(state.roots) + 1):
        roots = []
        for root in state.roots:
            if root.predicate is None or root.state is m.ConditionState.STALE:
                roots.append(root)
                continue
            proof = _evaluate_admitted(state, root.predicate)
            if not prerequisites_met(root.id, state):
                roots.append(replace(root, state=m.ConditionState.UNRESOLVED))
                continue
            status = {m.ProofState.PROVED: m.ConditionState.SATISFIED,
                      m.ProofState.DISPROVED: m.ConditionState.DISPROVED,
                      m.ProofState.UNKNOWN: m.ConditionState.UNRESOLVED}[proof.state]
            roots.append(replace(root, state=status))
        roots = tuple(roots)
        if roots == state.roots:
            break
        state = replace(state, roots=roots)
    required = {m.PredicateKind.SOURCE_IDENTITY, m.PredicateKind.PRODUCER_AVAILABLE,
                m.PredicateKind.MAPPING_AVAILABLE, m.PredicateKind.AUTHORITY, m.PredicateKind.CONSUMER_CHECK}
    entities = {e.id: e for e in state.entities}
    root_states = {r.id: r.state for r in state.roots}
    slots = []
    for slot in state.slots:
        if slot.state is m.SlotState.STALE or (slot.value is None and not slot.requirements):
            slots.append(slot)
            continue
        kinds = set()
        for ref in slot.requirements:
            kinds.update(_predicate_refs(state, ref)[0])
        value = entities.get(slot.value)
        # Mandatory contract links must prove this exact value independently,
        # not merely occur in an ANY branch whose other operand passed.
        reachable = set(slot.requirements)
        while True:
            expanded = reachable | {ref for p in state.predicates if p.id in reachable for ref in p.operands}
            if expanded == reachable:
                break
            reachable = expanded
        contracts = [p for p in state.predicates if p.id in reachable and p.kind in required]
        def bound(p):
            if value is None:
                return False
            if p.kind is m.PredicateKind.SOURCE_IDENTITY:
                return p.entity == slot.value and p.expected == value.identity
            if p.kind is m.PredicateKind.PRODUCER_AVAILABLE:
                return p.entity == slot.value
            if p.kind is m.PredicateKind.CONSUMER_CHECK:
                return p.other == slot.value and p.expected == value.identity
            if p.kind is m.PredicateKind.AUTHORITY:
                return p.expected == value.identity
            mapping = entities.get(p.entity)
            return mapping is not None and mapping.target == value.identity
        mandatory = all(any(p.kind is kind and bound(p) and
            _evaluate_admitted(state, p.id).state is m.ProofState.PROVED for p in contracts) for kind in required)
        proved = prerequisites_met(slot.id, state) and value is not None and value.identity.kind is slot.required_type and \
            usable(value, state).state is m.ProofState.PROVED and mandatory and required.issubset(kinds) and \
            all(_evaluate_admitted(state, ref).state is m.ProofState.PROVED for ref in slot.requirements) and \
            all(root_states[ref] is m.ConditionState.SATISFIED for ref in slot.root_requirements)
        slots.append(replace(slot, state=m.SlotState.RESOLVED if proved else m.SlotState.UNRESOLVED))
    return replace(state, slots=tuple(slots))


@dataclass(frozen=True)
class Computation:
    actionable: Tuple[m.ActionId, ...]
    statuses: Tuple[m.ActionStatus, ...]
    blocked: Tuple[Tuple[m.ActionId, Tuple[str, ...]], ...]
    selection: Optional[SelectionTrace]
    defects: Tuple[str, ...] = ()
    human_batches: tuple = ()
    human_routing: m.HumanRouting = m.HumanRouting.NO_INTERNAL_ACTION
    control: Optional[m.ControlState] = None
    frontier: tuple = ()
    branches: tuple = ()
    unresolved_roots: int = 0
    unresolved_slots: int = 0


@dataclass(frozen=True)
class TransitionReport:
    snapshot: m.Snapshot
    action_transitions: Tuple[m.ActionStatus, ...]
    computation: Computation


def _actionability(snapshot):
    previous = {s.id: s.state for s in snapshot.statuses}
    statuses, blocked, actionable = [], [], []
    for action in sorted(snapshot.actions, key=lambda a: a.id.value):
        state = previous[action.id]
        if state in (m.ActionState.COMPLETED, m.ActionState.BLOCKED, m.ActionState.WAITING):
            if state is not m.ActionState.COMPLETED:
                blocked.append((action.id, ('PRIOR_ATTEMPT_HOLD:' + state.value,)))
        else:
            reasons = blockers(action, snapshot)
            if reasons:
                state = m.ActionState.BLOCKED
                blocked.append((action.id, reasons))
            else:
                state = m.ActionState.ACTIONABLE
                actionable.append(action)
        statuses.append(m.ActionStatus(action.id, state))
    return tuple(statuses), tuple(blocked), tuple(actionable)


def _inventory(snapshot, action, supplied):
    if action.operation in (m.OperationClass.ARCHITECT_AUTHORITY, m.OperationClass.ARCHITECT_CONTRACT_DECISION,
                            m.OperationClass.GOVERNED_OPERATION, m.OperationClass.IMPLEMENTATION_REPAIR,
                            m.OperationClass.VALIDATOR_IMPLEMENTATION):
        raise m.PlannerError('governed execution/decision outside P03')
    validate_result(action, supplied)
    existing = {k.id: k for k in snapshot.knowledge}
    for record in supplied.knowledge:
        if record.id in existing and existing[record.id] != record:
            raise m.PlannerError('conflicting accepted knowledge')
        existing[record.id] = record
    outcome_state = m.ActionState.COMPLETED if supplied.result is m.ActionResult.PASS else m.ActionState.BLOCKED
    statuses = tuple(sorted((m.ActionStatus(s.id, outcome_state)
                             if s.id == action.id else s for s in snapshot.statuses), key=lambda s: s.id.value))
    updated = replace(snapshot, statuses=statuses,
        knowledge=tuple(sorted(existing.values(), key=lambda k: k.id.value)))
    updated = _decision_result(updated, action, supplied)
    # Decision preparation changes knowledge/readiness only. It cannot promote domain proofs.
    return updated if any(action.id in (d.semantic_action, d.input_action) for d in snapshot.decisions) else evaluate_satisfaction(updated)


def coverage_scores(snapshot, actions, blocked):
    """Compute only explicitly complete deterministic PASS models, one at a time."""
    projection = project(snapshot)
    if projection.defects:
        return {}
    scores = {}
    before_roots = {r.id: r.state for r in snapshot.roots}
    before_blocked = {a for a, _ in blocked}
    for action in actions:
        if not action.pass_model_complete or not action.accepted_inventory:
            continue
        try:
            after = _inventory(snapshot, action, m.SuppliedResult(action.id, m.ActionResult.PASS,
                                                                 action.accepted_inventory))
        except m.PlannerError:
            continue
        changed = {r.id for r in after.roots if r.state is m.ConditionState.SATISFIED and
                   before_roots[r.id] is not m.ConditionState.SATISFIED}
        output_ids = {k.id for k in action.accepted_inventory}
        direct = set()
        for root in after.roots:
            _, knowledge, dependent_roots = _predicate_refs(after, root.predicate)
            if root.id in changed and knowledge.intersection(output_ids) and not dependent_roots.intersection(changed):
                direct.add(root.id)
        affected_slots = set()
        for slot in snapshot.slots:
            dependencies = set(slot.root_requirements)
            for ref in slot.requirements:
                dependencies.update(_predicate_refs(snapshot, ref)[2])
            # Follow explicit root predicate dependencies transitively.
            while True:
                expanded = dependencies | {before for before, after in projection.edges
                    if after in dependencies or after == slot.id} | {r for root in snapshot.roots if root.id in dependencies
                    for r in _predicate_refs(snapshot, root.predicate)[2]}
                if expanded == dependencies:
                    break
                dependencies = expanded
            if slot.state is not m.SlotState.RESOLVED and dependencies.intersection(direct):
                affected_slots.add(slot.id)
        unlocked = {a.id for a in _actionability(after)[2]}.intersection(before_blocked)
        scores[action.id] = (len(direct), len(affected_slots), len(unlocked))
    return scores


def recompute(snapshot):
    projection = project(snapshot)
    if projection.defects:
        return Computation((), tuple(sorted(snapshot.statuses, key=lambda s: s.id.value)), (), None, projection.defects,
                           control=m.ControlState.PLAN_DEFECT if snapshot.goals else None)
    state = evaluate_satisfaction(snapshot)
    statuses, blocked, actions = _actionability(state)
    machines = tuple(a for a in actions if not _human(a))
    humans = tuple(a for a in actions if _human(a))
    selection = select(machines, coverage_scores(state, machines, blocked),
                       {info.action: info for info in state.information}) if machines else None
    if machines and humans:
        ranked = select(actions, coverage_scores(state, actions, blocked),
                        {info.action: info for info in state.information})
        if ranked.selected in {a.id for a in machines}:
            selection = ranked
    batches = _human_batches(state, humans) if not machines else ()
    routing = m.HumanRouting.RUNNABLE if machines else m.HumanRouting.HUMAN_HANDOFF if humans else m.HumanRouting.NO_INTERNAL_ACTION
    computation=Computation(tuple(a.id for a in actions), statuses, blocked, selection, (), batches, routing)
    return _global_control(state,computation) if state.goals else computation


def apply_result(snapshot, supplied):
    m.validate_types(supplied, m.SuppliedResult)
    extended = bool(snapshot.external_gates or snapshot.decisions or snapshot.entities or snapshot.predicates or any(a.relation is not None for a in snapshot.assertions))
    if supplied.expected_snapshot is not None or extended:
        from .codec import snapshot_id
        if supplied.expected_snapshot != snapshot_id(snapshot):
            raise m.PlannerError('supplied result pre-state mismatch')
    computation = recompute(snapshot)
    if computation.selection is None or supplied.action != computation.selection.selected:
        raise m.PlannerError('result is not for the currently selected action')
    action = next(a for a in snapshot.actions if a.id == supplied.action)
    updated = _inventory(snapshot, action, supplied)
    transitions = tuple(m.ActionStatus(action.id, state) for state in
                        (m.ActionState.ACTIONABLE, m.ActionState.SELECTED,
                         next(s.state for s in updated.statuses if s.id == action.id)))
    return TransitionReport(updated, transitions, recompute(updated))


def admit_dossier_materialization(snapshot, supplied, validation_instances):
    """Atomically bind a prepared dossier and its evaluated validations.

    Predicate evaluation remains external to this transaction.  This boundary
    only verifies canonical bindings, records the typed instances, and then
    invokes the normal native decision-readiness predicate.
    """
    from .codec import canonical_bytes, snapshot_id, _wire
    m.validate_types(supplied, m.SuppliedResult)
    if type(validation_instances) is not tuple or any(type(v) is not m.ValidationInstance for v in validation_instances):
        raise m.PlannerError('typed validation instance tuple required')
    if supplied.expected_snapshot != snapshot_id(snapshot):
        raise m.PlannerError('dossier materialization pre-state mismatch')
    # Re-submission against the already-admitted canonical state is an
    # idempotent no-op.  It is recognized before selection because the next
    # Planner selection is intentionally different after admission.
    prior_action = next((a for a in snapshot.actions if a.id == supplied.action), None)
    prior_status = next((s for s in snapshot.statuses if s.id == supplied.action), None)
    prior_decision = next((d for d in snapshot.decisions if d.input_action == supplied.action), None)
    if (prior_action is not None and prior_status is not None and
            prior_status.state is m.ActionState.COMPLETED and
            prior_decision is not None and prior_decision.dossier is not None):
        from .codec import canonical_bytes, _wire
        if (supplied.dossier is not None and
                canonical_bytes(_wire(prior_decision.dossier)) == canonical_bytes(_wire(supplied.dossier)) and
                tuple(snapshot.validation_instances) == tuple(sorted(validation_instances,
                    key=lambda v: (v.predicate.value, v.proposition, v.dossier.sha256)))):
            return TransitionReport(snapshot, (), recompute(snapshot))
    computation = recompute(snapshot)
    if computation.selection is None or supplied.action != computation.selection.selected:
        raise m.PlannerError('dossier materialization requires selected input action')
    action = next(a for a in snapshot.actions if a.id == supplied.action)
    if action.operation is not m.OperationClass.DECISION_INPUT_ACQUISITION:
        raise m.PlannerError('dossier materialization requires decision-input action')
    if supplied.result is not m.ActionResult.PASS or supplied.dossier is None:
        raise m.PlannerError('successful dossier materialization requires PASS and dossier')
    # Validate the bounded result/inventory while intentionally deferring the
    # dossier comparison to this producer binding boundary.
    validate_result(action, replace(supplied, dossier=None))
    decision = next((d for d in snapshot.decisions if d.input_action == action.id), None)
    if decision is None or supplied.dossier.decision != decision.action:
        raise m.PlannerError('dossier decision/input binding mismatch')
    dossier_bytes = canonical_bytes(_wire(supplied.dossier))
    dossier_identity = m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY,
                                           'planner-dossier-sha256',
                                           __import__('hashlib').sha256(dossier_bytes).hexdigest())
    expected = set(c.predicate for c in supplied.dossier.checks
                   if c.kind in m.SUPPORTED_DOSSIER_CHECKS)
    # Canonicalize the admission payload so validation ordering cannot alter
    # snapshot identity or replay semantics.
    validation_instances = tuple(sorted(validation_instances,
                                         key=lambda v: (v.predicate.value,
                                                        v.proposition,
                                                        v.dossier.sha256)))
    actual = {v.predicate for v in validation_instances}
    if actual != expected:
        raise m.PlannerError('validation instance set does not match dossier')
    for v in validation_instances:
        if v.dossier != dossier_identity or v.scope != snapshot.context.scope or v.lineage != snapshot.context.lineage:
            raise m.PlannerError('validation instance dossier/scope/lineage mismatch')
        if v.result is not m.ValidationOutcome.PASS or v.currentness is not m.ValidationState.ACCEPTED:
            raise m.PlannerError('validation instance is not admitted PASS')
    existing = {k.id: k for k in snapshot.knowledge}
    for record in supplied.knowledge:
        if record.id in existing and existing[record.id] != record:
            raise m.PlannerError('conflicting accepted knowledge')
        existing[record.id] = record
    statuses = tuple(m.ActionStatus(s.id, m.ActionState.COMPLETED if s.id == action.id else s.state)
                     for s in snapshot.statuses)
    actions = tuple(replace(a, prepared_dossier=supplied.dossier) if a.id == action.id else a
                    for a in snapshot.actions)
    decisions = tuple(replace(d, dossier=supplied.dossier,
                              stage=m.DecisionStage.DECISION_INPUT_ACQUISITION,
                              history=d.history + (m.DecisionStage.DECISION_INPUT_ACQUISITION,))
                      if d.action == decision.action else d for d in snapshot.decisions)
    updated = replace(snapshot, actions=actions, statuses=statuses,
                      knowledge=tuple(sorted(existing.values(), key=lambda k: k.id.value)),
                      decisions=decisions, validation_instances=tuple(validation_instances))
    m.validate_model(updated)
    ready = decision_readiness(updated, next(d for d in updated.decisions if d.action == decision.action))
    if ready.state is not m.DecisionReadiness.DECISION_READY:
        raise m.PlannerError('dossier admission not ready: ' + ','.join(ready.missing))
    decisions = tuple(_advance(d, m.DecisionStage.DECISION_DOSSIER_READY,
                               m.DecisionStage.DECISION_READY)
                      if d.action == decision.action else d for d in updated.decisions)
    updated = replace(updated, decisions=decisions,
                      statuses=tuple(m.ActionStatus(s.id, m.ActionState.ACTIONABLE)
                                     if s.id == decision.action and s.state is not m.ActionState.COMPLETED else s
                                     for s in updated.statuses))
    m.validate_model(updated)
    return TransitionReport(updated, (), recompute(updated))


def _human(action):
    return action.operation in (m.OperationClass.ARCHITECT_AUTHORITY, m.OperationClass.ARCHITECT_CONTRACT_DECISION)


def _advance(decision, *stages):
    history = decision.history or (decision.stage,)
    return replace(decision, stage=stages[-1], history=history + stages)


def _decision_result(snapshot, action, supplied):
    decisions, reopen = [], set()
    for decision in snapshot.decisions:
        if action.id == decision.semantic_action and supplied.result is m.ActionResult.AUTHORITY_REQUIRED:
            if decision.stage is not m.DecisionStage.SEMANTIC_GAP_IDENTIFIED:
                raise m.PlannerError('semantic reentry requires a new bounded attempt')
            decision = _advance(decision, m.DecisionStage.DECISION_INPUTS_REQUIRED)
            if decision_readiness(snapshot, decision).state is m.DecisionReadiness.DECISION_READY:
                decision = _advance(decision, m.DecisionStage.DECISION_DOSSIER_READY, m.DecisionStage.DECISION_READY)
                reopen.add(decision.action)
            elif decision.input_action is not None:
                reopen.add(decision.input_action)
        if action.id == decision.input_action:
            if decision.stage is not m.DecisionStage.DECISION_INPUTS_REQUIRED:
                raise m.PlannerError('input transition out of order')
            decision = _advance(decision, m.DecisionStage.DECISION_INPUT_ACQUISITION)
            decision = replace(decision, dossier=supplied.dossier)
            readiness = decision_readiness(snapshot, decision)
            if supplied.result is m.ActionResult.PASS:
                if readiness.state is not m.DecisionReadiness.DECISION_READY:
                    raise m.PlannerError('input PASS requires complete independently proved dossier')
                decision = _advance(decision, m.DecisionStage.DECISION_DOSSIER_READY,
                                    m.DecisionStage.DECISION_READY)
                reopen.add(decision.action)
            elif readiness.state is m.DecisionReadiness.DECISION_READY:
                raise m.PlannerError('blocked input contradicts complete dossier')
        decisions.append(decision)
    updated = replace(snapshot, decisions=tuple(decisions), statuses=tuple(
        m.ActionStatus(s.id, m.ActionState.ACTION_ELIGIBLE) if s.id in reopen and
        s.state is not m.ActionState.COMPLETED else s for s in snapshot.statuses))
    m.validate_model(updated)
    return updated


def _human_batches(snapshot, humans):
    """Stable independent groups; conflicts are review ordering, never an adopted choice."""
    definitions = {d.action: d for d in snapshot.decisions}
    batches = []
    for action in sorted(humans, key=lambda a: a.id.value):
        for batch in batches:
            if all(other not in definitions[action.id].interferes_with and
                   action.id not in definitions[other].interferes_with for other in batch):
                batch.append(action.id)
                break
        else:
            batches.append([action.id])
    return tuple(tuple(batch) for batch in batches)


def apply_recorded_decision(snapshot, supplied):
    """Import an already authenticated scoped record; never create/issue authority."""
    from .codec import snapshot_id
    m.validate_types(supplied, m.RecordedDecision)
    m.validate_model(snapshot)
    if supplied.expected_snapshot != snapshot_id(snapshot):
        raise m.PlannerError('decision pre-state mismatch')
    decision = next((d for d in snapshot.decisions if d.action == supplied.decision), None)
    if decision is None or decision.stage is not m.DecisionStage.DECISION_READY or \
            supplied.decision not in recompute(snapshot).actionable or \
            decision_readiness(snapshot, decision).state is not m.DecisionReadiness.DECISION_READY:
        raise m.PlannerError('decision not ready for authenticated record')
    record = next((e for e in snapshot.entities if e.id == supplied.record), None)
    predicate = next((p for p in snapshot.predicates if p.id == supplied.authority), None)
    if snapshot.context is None or snapshot.context.scope != decision.dossier.scope or \
            supplied.choice not in decision.dossier.alternatives or record is None or predicate is None or \
            record.decision != decision.action or record.choice != supplied.choice or \
            predicate.kind is not m.PredicateKind.AUTHORITY or predicate.entity != supplied.record or \
            predicate.permission is not m.AuthorityClass.DECIDE or \
            predicate.expected != decision.dossier.provenance.identity or \
            _evaluate_admitted(snapshot, predicate.id).state is not m.ProofState.PROVED:
        raise m.PlannerError('record not authenticated/bound to exact dossier and scope')
    # The admitted record's exact choice must be independently pinned, not chosen by this call.
    if not any(k.id == m.KnowledgeId('decision-choice:' + supplied.decision.value) and
               k.statement == supplied.choice and k.provenance == record.provenance and
               k.state is m.KnowledgeState.KNOWN_COMPLETE and k.validation is m.ValidationState.ACCEPTED
               for k in snapshot.knowledge):
        raise m.PlannerError('recorded choice evidence missing')
    decision = _advance(replace(decision, recorded_choice=supplied.choice, record=supplied.record),
                        m.DecisionStage.DECISION_RECORDED)
    conflicts = {d.action for d in snapshot.decisions if d.action in decision.interferes_with or
                 decision.action in d.interferes_with}
    updated = replace(snapshot, decisions=tuple(decision if d.action == decision.action else
        replace(d, dossier=replace(d.dossier, validation=m.ValidationState.STALE))
        if d.action in conflicts and d.dossier is not None else d for d in snapshot.decisions),
        statuses=tuple(m.ActionStatus(s.id, m.ActionState.COMPLETED) if s.id == decision.action else
            m.ActionStatus(s.id, m.ActionState.WAITING) if s.id in conflicts else s for s in snapshot.statuses))
    return TransitionReport(updated, (m.ActionStatus(decision.action, m.ActionState.COMPLETED),), recompute(updated))


def apply_decision_reentry(snapshot, supplied):
    from .codec import snapshot_id
    m.validate_types(supplied, m.DecisionReentry)
    m.validate_model(snapshot)
    if supplied.expected_snapshot != snapshot_id(snapshot):
        raise m.PlannerError('decision reentry pre-state mismatch')
    decision = next((d for d in snapshot.decisions if d.action == supplied.decision), None)
    if decision is None or decision.stage is not m.DecisionStage.DECISION_RECORDED or \
            not recorded_decision_valid(snapshot, decision):
        raise m.PlannerError('decision reentry lacks valid recorded decision')
    decision = _advance(decision, m.DecisionStage.DOWNSTREAM_REEVALUATION)
    # Reenable only declared routes; all original gates are independently recalculated.
    updated = replace(snapshot, decisions=tuple(decision if d.action == decision.action else d for d in snapshot.decisions),
        statuses=tuple(m.ActionStatus(s.id, m.ActionState.ACTION_ELIGIBLE) if s.id in decision.downstream and
            s.state is not m.ActionState.COMPLETED else s for s in snapshot.statuses))
    return TransitionReport(updated, (), recompute(updated))


def apply_event(snapshot, supplied):
    if type(supplied) is m.EvidenceSourceAdmission:
        from .evidence import apply
        return apply(snapshot, supplied)
    if type(supplied) is m.SuppliedResult:
        return apply_result(snapshot, supplied)
    if type(supplied) is m.RecordedDecision:
        return apply_recorded_decision(snapshot, supplied)
    if type(supplied) is m.DecisionReentry:
        return apply_decision_reentry(snapshot, supplied)
    if type(supplied) is m.ExternalEvent:
        return apply_receipt(snapshot,supplied)
    if type(supplied) is m.SourceInvalidation:
        from .codec import snapshot_id, invalidate_sources
        m.validate_types(supplied,m.SourceInvalidation)
        if supplied.expected_snapshot != snapshot_id(snapshot):
            raise m.PlannerError('source invalidation pre-state mismatch')
        updated = invalidate_sources(snapshot,supplied.changed)
        return TransitionReport(updated,(),recompute(updated))
    raise m.PlannerError('unsupported event')


def apply_receipt(snapshot, event):
    """One explicit external lifecycle event; no acquisition, sending or execution."""
    from .codec import snapshot_id
    m.validate_types(event,m.ExternalEvent);m.validate_model(snapshot)
    if event.expected_snapshot!=snapshot_id(snapshot):
        raise m.PlannerError('external event pre-state mismatch')
    gate=next((g for g in snapshot.external_gates if g.id==event.gate),None)
    if gate is None:
        raise m.PlannerError('unknown external gate')
    old=gate.stage; new=event.stage; E=m.ExternalStage
    legal={E.EXTERNAL_EVIDENCE_REQUIRED:E.EVIDENCE_REQUEST_READY,
           E.EVIDENCE_REQUEST_READY:E.WAITING_FOR_EXTERNAL_EVIDENCE,
           E.WAITING_FOR_EXTERNAL_EVIDENCE:E.EVIDENCE_RECEIVED,
           E.EVIDENCE_RECEIVED:E.EVIDENCE_VALIDATED,
           E.EVIDENCE_VALIDATED:E.DEPENDENT_ACTION_REENTRY}
    if legal.get(old) is not new or gate.validation is not m.ValidationState.ACCEPTED:
        raise m.PlannerError('illegal external lifecycle transition')
    if new is E.EVIDENCE_REQUEST_READY and not gate.contract_complete:
        raise m.PlannerError('request/receipt contract incomplete')
    observations=snapshot.receipt_observations;statuses=snapshot.statuses
    if new is E.EVIDENCE_RECEIVED:
        if event.artifact is None or not any(e.id==event.artifact and e.produced for e in snapshot.entities):
            raise m.PlannerError('receipt requires admitted concrete bytes')
        gate=replace(gate,pending=event.artifact)
    elif event.artifact is not None:
        raise m.PlannerError('receipt identity supplied out of phase')
    history=(gate.history or (old,))+(new,)
    if new is E.EVIDENCE_VALIDATED:
        proof=_check_receipt_admitted(snapshot,gate,gate.pending)
        admission=next((a for a in snapshot.receipt_admissions if a.artifact==gate.pending),None)
        accepted=proof.state is m.ProofState.PROVED
        observation=m.ReceiptObservation(gate.id,gate.pending,accepted,proof.reasons,
            admission.claims if accepted else ())
        observations=observations+(observation,)
        trial=replace(snapshot,receipt_observations=observations)
        if not external_complete(trial,gate):
            new=E.WAITING_FOR_EXTERNAL_EVIDENCE
            history=(gate.history or (old,))+(new,)
    if new is E.DEPENDENT_ACTION_REENTRY:
        if not _external_complete_admitted(snapshot,gate):
            raise m.PlannerError('reentry requires every independent proof')
        statuses=tuple(replace(s,state=m.ActionState.ACTION_ELIGIBLE) if s.id in gate.reentry and
                       s.state is not m.ActionState.COMPLETED else s for s in statuses)
    gate=replace(gate,stage=new,history=history)
    updated=replace(snapshot,external_gates=tuple(gate if g.id==gate.id else g for g in snapshot.external_gates),
                    receipt_observations=observations,statuses=statuses)
    return TransitionReport(updated,(),recompute(updated))


def _global_control(snapshot, computation):
    """Traverse unsatisfied prerequisite paths to exposed control-transfer records."""
    actions={a.id:a for a in snapshot.actions};statuses={s.id:s.state for s in snapshot.statuses}
    roots={r.id:r.state for r in snapshot.roots};slots={s.id:s.state for s in snapshot.slots}
    goals={g.target:g for g in snapshot.goals};bounds={b.id:b for b in snapshot.boundaries}
    frontier={};defects=set(computation.defects);branches=[]
    def satisfied(target):
        return roots.get(target) is m.ConditionState.SATISFIED or slots.get(target) is m.SlotState.RESOLVED
    def walk(action_id,goal,path=()):
        if action_id in path:
            defects.add('CONTROL_ROUTE_CYCLE:'+action_id.value);return set()
        path=path+(action_id,)
        if current_completion(snapshot, action_id) or action_id in computation.actionable:
            return set()
        action=actions[action_id];children=[]
        if any('UNSUPPORTED_RULE' in _evaluate_admitted(snapshot,ref).reasons for ref in action.requirements):
            defects.add('UNSUPPORTED_REQUIRED_RULE:'+action_id.value)
        for prerequisite in action.prerequisites:
            if prerequisite.kind is m.GateKind.ACTION_COMPLETED and not current_completion(snapshot, prerequisite.target):
                children.append(prerequisite.target)
            elif prerequisite.kind is m.GateKind.CONDITION_SATISFIED and not satisfied(prerequisite.target):
                target_goal=goals.get(prerequisite.target)
                if target_goal is None:
                    defects.add('MISSING_GOAL_ROUTE:'+prerequisite.target.value)
                else: children.extend(target_goal.entry_actions)
        # Later external stages are not the currently exposed frontier while an
        # earlier prerequisite blocks this operation.
        if children:
            found=set()
            for child in sorted(set(children),key=lambda x:x.value):found.update(walk(child,goal,path))
            return found
        found=set()
        for boundary in snapshot.boundaries:
            if action_id not in boundary.actions:continue
            if boundary.kind is m.BoundaryKind.EXTERNAL_EVIDENCE:
                gate=next(g for g in snapshot.external_gates if g.id==boundary.id)
                if not gate.contract_complete or gate.validation is not m.ValidationState.ACCEPTED or any(
                        not r.rule_known and not governed_external_unknown(snapshot,gate,r,action_id)
                        for r in snapshot.evidence_requirements if r.id in gate.requirements):
                    defects.add('UNQUALIFIED_EXTERNAL_CONTRACT:'+gate.id.value)
                if gate.stage is m.ExternalStage.DEPENDENT_ACTION_REENTRY and _external_complete_admitted(snapshot,gate):continue
            frontier.setdefault(boundary.id,set()).add((_key(goal),tuple(_key(a) for a in path)))
            found.add(boundary.id)
            if boundary.kind is m.BoundaryKind.PLAN_DEFECT:defects.add('LOCAL_PLAN_DEFECT:'+boundary.id.value)
        if not found:defects.add('MISSING_CONTROL_ROUTE:'+action_id.value)
        return found
    terminal_failures=[]
    for goal in sorted(snapshot.goals,key=lambda x:_key(x.target)):
        if satisfied(goal.target):
            branches.append((goal.target,m.BranchState.TERMINAL_SUCCESS));continue
        if goal.failure is not None and not goal.recovery and _evaluate_admitted(snapshot,goal.failure).state is m.ProofState.PROVED:
            terminal_failures.append(goal.target);branches.append((goal.target,m.BranchState.TERMINAL_FAILURE));continue
        if not goal.entry_actions:
            defects.add('MISSING_GOAL_ROUTE:'+goal.target.value)
        found=set()
        for action in goal.entry_actions:found.update(walk(action,goal.target))
        reachable=set(goal.entry_actions)
        while True:
            expanded=reachable|{g.target for a in snapshot.actions if a.id in reachable for g in a.prerequisites
                                if g.kind is m.GateKind.ACTION_COMPLETED}
            if expanded==reachable:break
            reachable=expanded
        live=reachable.intersection(computation.actionable)
        if any(not _human(actions[a]) for a in live):branch=m.BranchState.RUNNABLE_INTERNAL
        elif live:branch=m.BranchState.HUMAN_DECISION_REQUIRED
        elif any(bounds[b].kind is m.BoundaryKind.PLAN_DEFECT for b in found):branch=m.BranchState.BLOCKED_BY_PLAN_DEFECT
        elif len(found)==1:
            kind=bounds[next(iter(found))].kind
            branch={m.BoundaryKind.EXTERNAL_EVIDENCE:m.BranchState.WAITING_FOR_EXTERNAL_EVIDENCE,
                    m.BoundaryKind.EXTERNAL_FACT:m.BranchState.FACT_ACQUISITION_REQUIRED,
                    m.BoundaryKind.IMPLEMENTATION_AUTHORITY:m.BranchState.IMPLEMENTATION_AUTHORITY_REQUIRED}.get(kind,m.BranchState.BLOCKED_BY_PLAN_DEFECT)
        else:branch=m.BranchState.DEPENDENCY_BLOCKED
        branches.append((goal.target,branch))
    declined = any(d.action.value == 'E2-DECIDE' and d.recorded_choice == 'DECLINE'
                   for d in snapshot.decisions)
    if declined:
        control=m.ControlState.QUALIFICATION_DECLINED
    elif computation.selection is not None:control=m.ControlState.RUNNABLE
    elif computation.human_batches:control=m.ControlState.HUMAN_HANDOFF
    elif defects:control=m.ControlState.PLAN_DEFECT
    elif all(satisfied(g.target) for g in snapshot.goals):control=m.ControlState.TERMINAL_SUCCESS
    elif terminal_failures:control=m.ControlState.TERMINAL_FAILURE
    elif frontier:
        control=m.ControlState.EXTERNAL_WAIT if all(bounds[b].kind is m.BoundaryKind.EXTERNAL_EVIDENCE for b in frontier) else m.ControlState.MIXED_WAIT
    else:
        control=m.ControlState.PLAN_DEFECT;defects.add('UNRESOLVED_GOAL_WITHOUT_CONTROL_PATH')
    return replace(computation,control=control,frontier=tuple((key,tuple(sorted(values))) for key,values in sorted(frontier.items(),key=lambda x:x[0].value)),
                   branches=tuple(branches),defects=tuple(sorted(defects)),
                   unresolved_roots=sum(r.state is not m.ConditionState.SATISFIED for r in snapshot.roots),
                   unresolved_slots=sum(s.state is not m.SlotState.RESOLVED for s in snapshot.slots))



def resume_eligibility(bundle, source_root=None):
    """Current, non-effecting resume proof from replayed persisted inputs.

    Legacy phase/history text is not an accepted reentry event. Native events
    bind their entire pre-state plus the exact policy/context. No imported
    historical checkpoint is promoted to a native event here (C06 owns import).
    Source bytes must be independently available to return permission.
    """
    from . import codec as c
    from .gates import _obligation_proof
    state = c._replay(bundle)
    computation = recompute(state)
    reasons, eligible, support, forbidden = set(), set(), set(), set()
    binding = c.resume_binding(bundle)
    routes = []
    for gate in sorted(state.external_gates, key=lambda g:g.id.value):
        why = []
        if gate.stage is not m.ExternalStage.DEPENDENT_ACTION_REENTRY:
            why.append('REENTRY_STAGE_REQUIRED')
        if not gate.contract_complete or gate.validation is not m.ValidationState.ACCEPTED:
            why.append('RECEIPT_CONTRACT_UNQUALIFIED')
        for ref in sorted(gate.requirements,key=lambda x:x.value):
            proof = _obligation_proof(state,ref)
            if proof.state is not m.ProofState.PROVED:
                why.append('OBLIGATION:' + ref.value + ':' + proof.state.value + ':' + ','.join(proof.reasons))
                for observation in state.receipt_observations:
                    if observation.gate == gate.id and any(cl.requirement == ref for cl in observation.claims):
                        check = _check_receipt_admitted(state,gate,observation.artifact)
                        why.extend('RECEIPT:' + observation.artifact.value + ':' + reason for reason in check.reasons)
        events = [e for e in bundle.events if type(e.result) is m.ExternalEvent and
            e.result.gate == gate.id and e.result.stage is m.ExternalStage.DEPENDENT_ACTION_REENTRY]
        routes.append(('EXTERNAL:' + gate.id.value, gate.reentry, events, why, gate.held_actions + gate.reentry))
    for decision in sorted(state.decisions,key=lambda d:d.action.value):
        if decision.stage is not m.DecisionStage.DOWNSTREAM_REEVALUATION:
            continue
        why = [] if recorded_decision_valid(state,decision) else ['RECORDED_DECISION_UNPROVED']
        events = [e for e in bundle.events if type(e.result) is m.DecisionReentry and e.result.decision == decision.action]
        routes.append(('DECISION:' + decision.action.value, decision.downstream, events, why, decision.downstream))
    for route, actions, events, why, affected in routes:
        if not events:
            why.append('ACCEPTED_REENTRY_EVENT_MISSING')
        elif events[-1].resume_binding != binding:
            why.append('REENTRY_POLICY_BINDING_MISSING_OR_CHANGED')
        if state.context is None:
            why.append('EVALUATION_CONTEXT_MISSING')
        live = set(actions).intersection(computation.actionable)
        if not live:
            why.append('NAMED_REENTRY_NOT_ACTIONABLE')
            blocked = dict(computation.blocked)
            for action in sorted(actions,key=lambda a:a.value):
                why.extend(action.value + ':' + r for r in blocked.get(action,('COMPLETED_OR_UNAVAILABLE',)))
        if why:
            reasons.update(route + ':' + reason for reason in why)
            forbidden.update(affected)
        else:
            eligible.update(live)
            support.update((events[-1].identity,events[-1].parent_snapshot,binding))
    eligible.difference_update(forbidden)
    if eligible:
        if source_root is None:
            reasons.add('SOURCE_VERIFICATION_REQUIRED'); eligible.clear()
        else:
            for pin in sorted(bundle.sources + (bundle.policy,),key=lambda p:(p.path,p.pointer or '',p.profile.value)):
                try:
                    c.load_pinned(source_root,pin)
                except (m.PlannerError,OSError,ValueError):
                    reasons.add('SOURCE_PIN_FAILED:' + pin.path); eligible.clear()
            if eligible:
                support.update(pin.identity for pin in bundle.sources + (bundle.policy,))
    if not routes:
        reasons.add('NO_DEFINED_REENTRY_ROUTE')
    return m.ResumeEligibility(bool(eligible),tuple(sorted(eligible,key=lambda a:a.value)),
        tuple(sorted(reasons)),tuple(sorted(support,key=lambda i:(i.kind.value,i.namespace,i.sha256))))
