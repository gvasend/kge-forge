"""Durable native dossier-result admission, with detached historical Snapshots.

Only trusted application code registers producers. No wire value can register a
callable or manufacture an executed candidate. Replay uses recorded outcomes,
never a live producer or validator. Event and Snapshot schemas are unchanged.
"""
from dataclasses import dataclass
from weakref import WeakKeyDictionary

from . import codec as c, core, model as m

_producers = WeakKeyDictionary()
_prepared = WeakKeyDictionary()


def require(value, reason):
    if not value:
        raise m.PlannerError(reason)


def _same(a, b):
    return c.canonical_bytes(c._wire(a)) == c.canonical_bytes(c._wire(b))


@dataclass(frozen=True, eq=False)
class Producer:
    action: m.ActionId
    operation: object


def register_producer(action, operation):
    """Trusted application hook, not an artifact/data admission interface."""
    m.validate_types(action, m.ActionId)
    require(callable(operation), 'DOSSIER_QUALIFIED_PRODUCER_REQUIRED')
    producer = Producer(action, operation)
    _producers[producer] = operation
    return producer


def _producer(producer):
    require(type(producer) is Producer and _producers.get(producer) is producer.operation,
            'DOSSIER_QUALIFIED_PRODUCER_REQUIRED')


def sources(artifacts):
    require(type(artifacts) is tuple, 'DOSSIER_SOURCE_ARTIFACTS_TYPE')
    for item in artifacts:
        require(type(item) is tuple and len(item) == 2, 'DOSSIER_SOURCE_ARTIFACT_TYPE')
        pin, raw = item
        m.validate_types(pin, m.ArtifactPin)
        c.validate_pin(pin)
        require(pin.profile is m.HashProfile.RAW and pin.pointer == '' and type(raw) is bytes
                and c._identity(raw, 'raw-file-sha256') == pin.identity, 'DOSSIER_SOURCE_CONTENT_PIN')
    m.unique(artifacts, lambda x: (x[0].path, x[0].pointer, x[0].profile))
    return tuple(sorted(artifacts, key=lambda x: c.canonical_bytes(c._wire(x[0]))))


def archive_objects(bundle, snapshot_resolver):
    """Resolve the complete archive closure. Never use bundle.current as fallback."""
    events = {e.identity: e for e in bundle.events}
    result = {}
    for binding in bundle.dossier_materializations:
        require(binding.event_identity in events, 'DOSSIER_ORPHAN_BINDING')
        event = events[binding.event_identity]
        require(callable(snapshot_resolver), 'DOSSIER_SNAPSHOT_RESOLVER_REQUIRED')
        snapshot = snapshot_resolver(event.after_snapshot)
        require(type(snapshot) is m.Snapshot and c.snapshot_id(snapshot) == event.after_snapshot,
                'DOSSIER_ARCHIVE_IDENTITY')
        result[event.after_snapshot] = snapshot
    return tuple(result[k] for k in sorted(result, key=lambda x: (x.namespace, x.sha256)))


def memory_resolver(snapshots):
    """Private precommit resolver; callers must pass historical objects explicitly."""
    values = {c.snapshot_id(s): s for s in snapshots}
    def resolve(identity):
        require(identity in values, 'DOSSIER_ARCHIVE_MISSING')
        return values[identity]
    return resolve


def _selected_input(snapshot, action_id):
    """Gate the bounded operation before any producer can be invoked."""
    m.validate_model(snapshot)
    action = next((a for a in snapshot.actions if a.id == action_id), None)
    require(action is not None and action.operation is m.OperationClass.DECISION_INPUT_ACQUISITION
            and action.effect is m.EffectClass.NON_EFFECTING, 'DOSSIER_INPUT_ACTION')
    computation = core.recompute(snapshot)
    require(computation.selection is not None and computation.selection.selected == action_id,
            'DOSSIER_ACTION_NOT_SELECTED')


def validate_operands(snapshot, supplied, validations, pins, history=()):
    """Check typed subject/input/source bindings before unchanged T02 admission."""
    m.validate_types(supplied, m.SuppliedResult)
    require(type(validations) is tuple and all(type(v) is m.ValidationInstance for v in validations),
            'DOSSIER_TYPED_VALIDATIONS_REQUIRED')
    require(supplied.expected_snapshot == c.snapshot_id(snapshot), 'DOSSIER_PRE_STATE')
    require(supplied.dossier is not None and supplied.result is m.ActionResult.PASS,
            'DOSSIER_ACTUAL_RESULT_REQUIRED')
    _selected_input(snapshot, supplied.action)
    dossier = supplied.dossier
    dossier_id = c._identity(c.canonical_bytes(c._wire(dossier)), 'planner-dossier-sha256')
    checks = {x.predicate: x for x in dossier.checks if x.kind in m.SUPPORTED_DOSSIER_CHECKS}
    require(len(checks) == len(m.SUPPORTED_DOSSIER_CHECKS), 'DOSSIER_CHECK_SET')
    m.unique(validations, lambda v: v.predicate)
    require({v.predicate for v in validations} == set(checks), 'DOSSIER_VALIDATION_SET')
    allowed = {(p.path, p.identity) for p in pins if p.profile is m.HashProfile.RAW}
    provenances = [dossier.provenance] + [x.provenance for x in dossier.checks] + [v.provenance for v in validations]
    require(all((p.path, p.identity) in allowed for p in provenances), 'DOSSIER_SOURCE_NOT_PINNED')
    invalidated = {p for e in history if type(e.result) is m.SourceInvalidation for p in e.result.changed}
    require(not invalidated.intersection({dossier_id, dossier.provenance.identity}
                | {p.identity for p in provenances}), 'DOSSIER_SOURCE_INVALIDATED')
    ctx = snapshot.context
    require(ctx is not None and dossier.scope == ctx.scope, 'DOSSIER_CONTEXT')
    for v in validations:
        m.validate_types(v, m.ValidationInstance)
        check = checks[v.predicate]
        require(v.dossier == dossier_id and v.proposition == check.kind.value
                and v.inputs == (supplied.expected_snapshot, dossier.provenance.identity)
                and v.provenance == check.provenance, 'DOSSIER_VALIDATION_BINDING')
        require((v.scope, v.lineage) == (ctx.scope, ctx.lineage)
                and v.result is m.ValidationOutcome.PASS and v.currentness is m.ValidationState.ACCEPTED,
                'DOSSIER_VALIDATION_NOT_CURRENT')


def historical_projection(prefix, binding, event, snapshot_resolver):
    """Verify the historical T02 effect; no operation or independent rule runs."""
    m.validate_types(binding, m.DossierMaterializationBinding)
    require(binding.event_identity == event.identity and binding.expected_bundle ==
            c._identity(c._bundle_bytes_admitted(prefix), 'planner-bundle-v1'), 'DOSSIER_PREFIX_BINDING')
    require(type(event.result) is m.SuppliedResult and event.resume_binding is None,
            'DOSSIER_EVENT_BRANCH')
    require(callable(snapshot_resolver), 'DOSSIER_SNAPSHOT_RESOLVER_REQUIRED')
    archived = snapshot_resolver(event.after_snapshot)
    require(type(archived) is m.Snapshot and c.snapshot_id(archived) == event.after_snapshot,
            'DOSSIER_ARCHIVE_IDENTITY')
    m.unique(binding.source_additions, lambda p: (p.path, p.pointer, p.profile))
    for pin in binding.source_additions:
        c.validate_pin(pin)
        require(pin.profile is m.HashProfile.RAW and pin.pointer == '' and pin not in prefix.sources,
                'DOSSIER_SOURCE_INTRODUCTION')
    validations = archived.validation_instances
    validate_operands(prefix.current, event.result, validations,
                      prefix.sources + binding.source_additions, prefix.events)
    used = {(p.path, p.identity) for p in c.decision_provenances(archived)}
    used.update((v.provenance.path, v.provenance.identity) for v in validations)
    require(all((p.path, p.identity) in used for p in binding.source_additions),
            'DOSSIER_UNRELATED_SOURCE_ADDITION')
    after = core.admit_dossier_materialization(prefix.current, event.result, validations).snapshot
    require(c.snapshot_bytes(after) == c.snapshot_bytes(archived), 'DOSSIER_POST_STATE_MISMATCH')
    return after


@dataclass(frozen=True, eq=False)
class Prepared:
    before: m.PersistenceBundle
    expected_bundle: m.ArtifactIdentity
    producer: Producer
    supplied: m.SuppliedResult
    validations: tuple
    source_artifacts: tuple
    snapshots: tuple
    updated: m.PersistenceBundle

    def resolve(self, identity):
        return memory_resolver(self.snapshots)(identity)


def _seal(candidate):
    return c.canonical_bytes({'before': c._wire(candidate.expected_bundle),
        'result': c._wire(candidate.supplied), 'validations': sorted(c._wire(candidate.validations), key=c.canonical_bytes),
        'sources': [[c._wire(p), c._wire(c._identity(raw, 'raw-file-sha256'))] for p, raw in candidate.source_artifacts],
        'archives': [c._wire(c.snapshot_id(s)) for s in candidate.snapshots], 'updated': c._wire(candidate.updated)})


def _hook(hook, stage):
    if hook is not None:
        hook(stage)


def prepare(bundle, expected_bundle, producer, source_artifacts, repo_root, *,
            snapshot_resolver=None, postcondition=None, failure_hook=None):
    """Execute the qualified NON_EFFECTING producer once into private native state."""
    _producer(producer)
    m.validate_types(expected_bundle, m.ArtifactIdentity)
    require(expected_bundle == c.bundle_id(bundle, snapshot_resolver=snapshot_resolver), 'DOSSIER_PRE_BUNDLE')
    c._verify_sources(bundle, repo_root)
    artifacts = sources(source_artifacts)
    for pin, raw in artifacts:
        c._path(repo_root, pin.path)
    additions = tuple(p for p, raw in artifacts if p not in bundle.sources)
    before_state = c.snapshot_id(bundle.current)
    _selected_input(bundle.current, producer.action)
    result = producer.operation(bundle.current, artifacts)
    _hook(failure_hook, 'after_producer')
    require(type(result) is tuple and len(result) == 2, 'DOSSIER_PRODUCER_RESULT_TYPE')
    supplied, validations = result
    require(c.snapshot_id(bundle.current) == before_state, 'DOSSIER_PRODUCER_MUTATED_PRE_STATE')
    m.validate_types(supplied, m.SuppliedResult)
    require(supplied.action == producer.action, 'DOSSIER_PRODUCER_ACTION')
    validate_operands(bundle.current, supplied, validations, bundle.sources + additions, bundle.events)
    _hook(failure_hook, 'after_validations')
    after = core.admit_dossier_materialization(bundle.current, supplied, validations).snapshot
    _hook(failure_hook, 'after_result_application')
    after_id = c.snapshot_id(after)
    _hook(failure_hook, 'after_snapshot')
    ordinal = len(bundle.events) + 1
    parent = bundle.events[-1].identity if bundle.events else None
    event = m.ExecutionEvent(ordinal, before_state, parent, supplied, after_id,
        c._event_identity(ordinal, before_state, parent, supplied, after_id))
    binding = m.DossierMaterializationBinding(event.identity, expected_bundle, additions)
    from dataclasses import replace
    updated = replace(bundle, events=bundle.events + (event,), current=after,
                      sources=bundle.sources + additions,
                      dossier_materializations=bundle.dossier_materializations + (binding,))
    _hook(failure_hook, 'after_event_binding')
    snapshots = archive_objects(bundle, snapshot_resolver) + (after,)
    resolver = memory_resolver(snapshots)
    c._replay(updated, snapshot_resolver=resolver)
    if postcondition is not None:
        require(postcondition(bundle.current, after, event) is not False, 'DOSSIER_POSTCONDITION')
    candidate = Prepared(bundle, expected_bundle, producer, supplied, validations, artifacts, snapshots, updated)
    _prepared[candidate] = _seal(candidate)
    return candidate


def _trusted_head(directory, before, expected_bundle, repo_root, snapshot_resolver):
    current = c._read_head(directory, before, repo_root)
    resolver = c.snapshot_resolver(directory) if (directory / 'HEAD.json').exists() else snapshot_resolver
    prefix = c._prefix_bundle(current, len(before.events), snapshot_resolver=resolver)
    require(c.bundle_id(prefix, snapshot_resolver=resolver) == expected_bundle, 'DOSSIER_UNTRUSTED_HEAD_LINEAGE')
    return current, resolver


def _retry(current, resolver, before, expected_bundle, action, additions, candidate=None):
    index = len(before.events)
    if len(current.events) == index:
        return None
    event = current.events[index]
    binding = next((b for b in current.dossier_materializations if b.event_identity == event.identity), None)
    require(binding is not None and binding.expected_bundle == expected_bundle
            and type(event.result) is m.SuppliedResult and event.result.action == action,
            'DOSSIER_STALE_PARENT')
    require(_same(tuple(sorted(binding.source_additions, key=lambda p: c.canonical_bytes(c._wire(p)))), additions),
            'DOSSIER_IDEMPOTENCY_CONFLICT')
    if candidate is not None:
        require(_same(event, candidate.updated.events[-1])
                and c.snapshot_bytes(resolver(event.after_snapshot)) == c.snapshot_bytes(candidate.updated.current),
                'DOSSIER_IDEMPOTENCY_CONFLICT')
    committed = c._prefix_bundle(current, index + 1, snapshot_resolver=resolver)
    return current, c.bundle_id(committed, snapshot_resolver=resolver), True


def _commit_locked(candidate, directory, repo_root, failure_hook):
    require(type(candidate) is Prepared and _prepared.get(candidate) == _seal(candidate),
            'DOSSIER_LIVE_EXECUTION_CONTEXT_REQUIRED')
    _producer(candidate.producer)
    current, resolver = _trusted_head(directory, candidate.before, candidate.expected_bundle, repo_root, candidate.resolve)
    artifacts = sources(candidate.source_artifacts)
    additions = tuple(p for p, raw in artifacts if p not in candidate.before.sources)
    retry = _retry(current, resolver, candidate.before, candidate.expected_bundle, candidate.supplied.action,
                   additions, candidate)
    if retry is not None:
        c._verify_sources(current, repo_root)
        return retry
    require(c.bundle_id(current, snapshot_resolver=resolver) == candidate.expected_bundle, 'DOSSIER_STALE_PARENT')
    c._replay(candidate.updated, snapshot_resolver=candidate.resolve)
    c._verify_sources(candidate.before, repo_root)
    for pin, raw in artifacts:
        if pin not in additions:
            continue
        target = c._path(repo_root, pin.path)
        parent = c._transaction_directory(target.parent, repo_root)
        c._write_immutable(parent, target.name, raw)
        c._fsync_directory(parent)
    _hook(failure_hook, 'after_source_stage')
    identity = c._publish_head(directory, candidate.updated, candidate.expected_bundle, None, repo_root,
                               snapshot_resolver=candidate.resolve, failure_hook=failure_hook)
    return candidate.updated, identity, False


def commit(candidate, output_dir, repo_root, *, failure_hook=None):
    """Publish an authentic prepared context or return its historical exact retry."""
    require(type(candidate) is Prepared and candidate in _prepared, 'DOSSIER_LIVE_EXECUTION_CONTEXT_REQUIRED')
    directory = c._transaction_directory(output_dir, repo_root)
    with c._transaction_lock(directory):
        return _commit_locked(candidate, directory, repo_root, failure_hook)


def execute(bundle, expected_bundle, producer, source_artifacts, output_dir, repo_root, *,
            snapshot_resolver=None, postcondition=None, failure_hook=None):
    """Retry-check, execute, admit and publish under one existing local lock."""
    _producer(producer)
    require(c.bundle_id(bundle, snapshot_resolver=snapshot_resolver) == expected_bundle, 'DOSSIER_PRE_BUNDLE')
    c._verify_sources(bundle, repo_root)
    artifacts = sources(source_artifacts)
    additions = tuple(p for p, raw in artifacts if p not in bundle.sources)
    directory = c._transaction_directory(output_dir, repo_root)
    with c._transaction_lock(directory):
        current, resolver = _trusted_head(directory, bundle, expected_bundle, repo_root, snapshot_resolver)
        retry = _retry(current, resolver, bundle, expected_bundle, producer.action, additions)
        if retry is not None:
            c._verify_sources(current, repo_root)
            return retry
        candidate = prepare(bundle, expected_bundle, producer, artifacts, repo_root,
            snapshot_resolver=snapshot_resolver, postcondition=postcondition, failure_hook=failure_hook)
        return _commit_locked(candidate, directory, repo_root, failure_hook)
