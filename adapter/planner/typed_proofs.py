"""Typed, contract-bound admission and bounded prerequisite-hold reevaluation.

Replay calls the same pure transition on its historical pre-state. Proof records
are immutable history; current usability is derived from live dependencies.
"""
from dataclasses import replace
from . import model as m


def identity(record):
    from . import codec as c
    body = c._wire(record)
    body.pop('id', None)
    body.pop('validation', None)
    return c._identity(c.canonical_bytes(body), 'planner-' + type(record).__name__ + '-v1')


def support_identity(snapshot, ref):
    from . import codec as c
    if type(ref) is m.KnowledgeId:
        record = next((k for k in snapshot.knowledge if k.id == ref), None)
        return None if record is None else c._identity(c.canonical_bytes(c._wire(record)), 'planner-proof-support-v1')
    proofs = tuple(sorted((p.id for p in snapshot.typed_proofs if p.target == ref and usable(snapshot, p)), key=lambda x: x.sha256))
    return c._identity(c.canonical_bytes(c._wire(proofs)), 'planner-proof-support-v1')


def validate_records(snapshot):
    m.unique(snapshot.proof_contracts, lambda p: p.id)
    m.unique(snapshot.proof_contracts, lambda p: p.target)
    m.unique(snapshot.typed_proofs, lambda p: p.id)
    contracts = {p.id: p for p in snapshot.proof_contracts}
    for p in snapshot.proof_contracts + snapshot.typed_proofs:
        m.validate_provenance(p.provenance)
        if p.id != identity(p) or not p.proposition or not p.supports or len(p.supports) != len(p.support_identities):
            raise m.PlannerError('invalid typed proof identity/contract')
        m.unique(p.supports, lambda x: x)
        if p.provenance.scope != p.scope or p.authority not in {e.id for e in snapshot.entities}:
            raise m.PlannerError('invalid proof provenance/authority reference')
        if p.proof_type is m.TypedProofKind.SLOT_PROOF:
            if type(p.target) is not m.SlotId or p.target not in {v.id for v in snapshot.slots} or any(type(r) is not m.KnowledgeId for r in p.supports):
                raise m.PlannerError('invalid SLOT_PROOF target/support')
        elif type(p.target) is not m.ConditionId or p.target not in {r.id for r in snapshot.roots} or any(type(r) is not m.SlotId for r in p.supports):
            raise m.PlannerError('invalid ROOT_PROOF target/support')
        if type(p) is m.TypedProof:
            contract = contracts.get(p.contract)
            if contract is None or any(getattr(p, f) != getattr(contract, f) for f in ('proof_type', 'proposition', 'target', 'supports', 'support_identities', 'scope', 'lineage', 'generation', 'valid_until', 'authority', 'authority_identity', 'provenance')):
                raise m.PlannerError('proof does not match independent contract')
    # Typed contracts own their targets; avoid alternate predicate bypasses.
    for contract in snapshot.proof_contracts:
        if type(contract.target) is m.SlotId:
            slot = next(v for v in snapshot.slots if v.id == contract.target)
            if slot.value is not None or slot.requirements or slot.root_requirements:
                raise m.PlannerError('typed slot has alternate value proof')
        if type(contract.target) is m.ConditionId and next(r for r in snapshot.roots if r.id == contract.target).predicate is not None:
            raise m.PlannerError('typed root has alternate predicate')
        if any(ref not in {k.id for k in snapshot.knowledge} | {s.id for s in snapshot.slots} for ref in contract.supports):
            raise m.PlannerError('dangling proof support')


def usable(snapshot, proof):
    from .gates import usable as entity_usable, unavailable_support, current_completion
    contract = next((c for c in snapshot.proof_contracts if c.id == proof.contract), None)
    ctx = snapshot.context
    if contract is None or ctx is None or proof.validation is not m.ValidationState.ACCEPTED or contract.validation is not m.ValidationState.ACCEPTED:
        return False
    from . import proof_installation
    if not proof_installation.contract_current(snapshot, contract):
        return False
    if (proof.scope, proof.lineage, proof.generation) != (ctx.scope, ctx.lineage, ctx.generation) or proof.valid_until < ctx.tick:
        return False
    authority = next((e for e in snapshot.entities if e.id == proof.authority), None)
    if authority is None or authority.kind is not m.EntityKind.AUTHORITY or authority.identity != proof.authority_identity or authority.consumed or m.AuthorityClass.DECIDE not in authority.permissions or entity_usable(authority, snapshot).state is not m.ProofState.PROVED:
        return False
    if authority.target is not None and authority.target not in (contract.id, contract.provenance.identity):
        return False
    unavailable = unavailable_support(snapshot)
    if proof.target in unavailable:
        return False
    # Structural prerequisites remain authoritative for typed targets too.
    for edge in snapshot.assertions:
        if edge.relation is m.Relation.REQUIRES and edge.subject == proof.target:
            ref = edge.object
            met = (any(a.id == ref and a.state is m.ActionState.COMPLETED for a in snapshot.statuses) if type(ref) is m.ActionId else
                   any(r.id == ref and r.state is m.ConditionState.SATISFIED for r in snapshot.roots) if type(ref) is m.ConditionId else
                   any(v.id == ref and v.state is m.SlotState.RESOLVED for v in snapshot.slots) if type(ref) is m.SlotId else
                   any(e.id == ref and entity_usable(e, snapshot).state is m.ProofState.PROVED for e in snapshot.entities))
            if not met or ref in unavailable:
                return False
    for ref, expected in zip(proof.supports, proof.support_identities):
        if ref in unavailable or support_identity(snapshot, ref) != expected:
            return False
        if type(ref) is m.KnowledgeId:
            k = next((k for k in snapshot.knowledge if k.id == ref), None)
            if k is None or k.validation is not m.ValidationState.ACCEPTED or k.state is not m.KnowledgeState.KNOWN_COMPLETE or k.provenance.scope != proof.scope or k.outcome not in (None, m.ActionResult.PASS):
                return False
            if k.producer is not None and not current_completion(snapshot, k.producer):
                return False
        elif (not any(s.id == ref and s.state is m.SlotState.RESOLVED for s in snapshot.slots) or
              not any(p.proof_type is m.TypedProofKind.SLOT_PROOF and p.target == ref and usable(snapshot, p)
                      for p in snapshot.typed_proofs)):
            return False
    return True


def derive(snapshot):
    slots = {c.target for c in snapshot.proof_contracts if c.proof_type is m.TypedProofKind.SLOT_PROOF}
    state = replace(snapshot, slots=tuple(replace(s, state=m.SlotState.RESOLVED if any(p.target == s.id and usable(snapshot, p) for p in snapshot.typed_proofs) else m.SlotState.UNRESOLVED) if s.id in slots else s for s in snapshot.slots))
    roots = {c.target for c in snapshot.proof_contracts if c.proof_type is m.TypedProofKind.ROOT_PROOF}
    return replace(state, roots=tuple(replace(r, state=m.ConditionState.SATISFIED if any(p.target == r.id and usable(state, p) for p in state.typed_proofs) else m.ConditionState.UNRESOLVED) if r.id in roots else r for r in state.roots))


def affected_actions(snapshot, dependencies):
    from .core import project
    edges = set(project(snapshot).edges)
    for p in snapshot.predicates:
        edges.update((ref, p.id) for ref in p.operands + tuple(x for x in (p.knowledge, p.entity, p.other, p.condition, p.action) if x is not None))
    for a in snapshot.actions:
        edges.add((a.source.identity, a.id))
        edges.update((k.provenance.identity, a.id) for k in a.accepted_inventory)
        edges.update((ref, a.id) for ref in a.requirements + ((a.authority,) if a.authority else ()))
    for r in snapshot.roots:
        if r.predicate: edges.add((r.predicate, r.id))
    for s in snapshot.slots:
        edges.update((ref, s.id) for ref in s.requirements + s.root_requirements + ((s.value,) if s.value else ()))
    for c in snapshot.proof_contracts:
        edges.update((ref, c.target) for ref in c.supports + (c.authority, c.id, c.provenance.identity))
    for p in snapshot.typed_proofs:
        edges.update((ref, p.target) for ref in (p.id, p.provenance.identity))
    for k in snapshot.knowledge:
        edges.add((k.provenance.identity, k.id))
    for e in snapshot.entities:
        edges.update(((e.provenance.identity, e.id), (e.identity, e.id)))
    reached = set(dependencies)
    while True:
        new = reached | {after for before, after in edges if before in reached}
        if new == reached: break
        reached = new
    return reached & {a.id for a in snapshot.actions}


def reevaluate(before, updated, dependencies, provenance):
    from .core import evaluate_satisfaction, project, _actionability
    from .codec import snapshot_id
    # Immutable provisional state; commit only after all ordinary checks pass.
    state = evaluate_satisfaction(updated)
    affected = affected_actions(updated, dependencies)
    current = {s.id: s for s in state.statuses}
    eligible = {a.id for a in state.actions if a.id in affected and not current[a.id].terminal_failure and
                (current[a.id].state in (m.ActionState.ACTIONABLE, m.ActionState.ACTION_ELIGIBLE) or
                 (current[a.id].state is m.ActionState.BLOCKED and not a.blocked_terminal))}
    statuses = tuple(replace(s, state=m.ActionState.ACTION_ELIGIBLE) if s.id in eligible and not s.terminal_failure and s.state in (m.ActionState.BLOCKED, m.ActionState.ACTIONABLE, m.ActionState.ACTION_ELIGIBLE) else s for s in state.statuses)
    candidate = replace(state, statuses=statuses)
    if project(candidate).defects:
        raise m.PlannerError('reevaluation projection failed')
    derived = {s.id: s for s in _actionability(candidate, eligible)[0]}
    support_state = snapshot_id(state)
    records = list(state.reevaluations)
    old = {s.id: s.state for s in before.statuses}
    for ref in sorted(affected, key=lambda x: x.value):
        if old[ref] != derived[ref].state:
            records.append(m.ReevaluationRecord(dependencies, ref, old[ref], support_state, derived[ref].state, provenance))
    return replace(state, statuses=tuple(derived[s.id] if s.id in eligible else s for s in state.statuses), reevaluations=tuple(records))


def apply(snapshot, event):
    from .core import TransitionReport, recompute
    from .codec import snapshot_id
    if type(event) not in (m.TypedProofAdmission, m.ProofDependencyChange, m.ActionReevaluation):
        raise m.PlannerError('unsupported typed proof transition')
    m.validate_model(snapshot); m.validate_types(event, type(event))
    if event.expected_snapshot != snapshot_id(snapshot):
        raise m.PlannerError('typed proof transition pre-state mismatch')
    if type(event) is m.ActionReevaluation:
        m.validate_provenance(event.provenance)
        m.unique(event.dependencies, lambda ref: ref)
        known = {item.id for seq in (snapshot.actions, snapshot.knowledge, snapshot.slots, snapshot.roots, snapshot.entities, snapshot.predicates, snapshot.proof_contracts, snapshot.typed_proofs) for item in seq}
        if not event.dependencies or not set(event.dependencies) <= known or snapshot.context is None or event.provenance.scope != snapshot.context.scope:
            raise m.PlannerError('invalid reevaluation dependency/context')
        updated = reevaluate(snapshot, snapshot, event.dependencies, event.provenance)
        m.validate_model(updated)
        return TransitionReport(updated, (), recompute(updated))
    if type(event) is m.TypedProofAdmission:
        proof = event.proof
        updated = replace(snapshot, typed_proofs=snapshot.typed_proofs if proof in snapshot.typed_proofs else snapshot.typed_proofs + (proof,))
        m.validate_model(updated)
        if not usable(derive(snapshot), proof):
            raise m.PlannerError('typed proof oracle rejected current support/authority')
        if updated == snapshot:
            return TransitionReport(snapshot, (), recompute(snapshot))
        dependencies, provenance = (proof.id, proof.target), proof.provenance
    else:
        m.validate_provenance(event.provenance)
        m.unique(event.dependencies, lambda ref: ref)
        from . import proof_installation
        dependencies, provenance = proof_installation.normalize_dependencies(snapshot,event.dependencies), event.provenance
        if not dependencies or snapshot.context is None or event.provenance.scope != snapshot.context.scope:
            raise m.PlannerError('invalid dependency invalidation')
        known = {k.id for k in snapshot.knowledge} | {s.id for s in snapshot.slots} | {r.id for r in snapshot.roots} | {e.id for e in snapshot.entities} | {p.id for p in snapshot.typed_proofs + snapshot.proof_contracts}
        if not set(dependencies) <= known:
            raise m.PlannerError('unknown dependency invalidation')
        affected = set(dependencies)
        while True:
            new = affected | {c.target for c in snapshot.proof_contracts if affected.intersection(c.supports + (c.id, c.authority))} | {p.target for p in snapshot.typed_proofs if p.id in affected}
            if new == affected: break
            affected = new
        updated = replace(snapshot,
            knowledge=tuple(replace(k, validation=m.ValidationState.STALE) if k.id in affected else k for k in snapshot.knowledge),
            entities=tuple(replace(e, validation=m.ValidationState.STALE) if e.id in affected else e for e in snapshot.entities),
            proof_contracts=tuple(replace(c, validation=m.ValidationState.STALE) if c.id in affected else c for c in snapshot.proof_contracts),
            typed_proofs=tuple(replace(p, validation=m.ValidationState.STALE) if p.id in affected or p.target in affected else p for p in snapshot.typed_proofs))
    updated = reevaluate(snapshot, updated, dependencies, provenance)
    m.validate_model(updated)
    return TransitionReport(updated, (), recompute(updated))
