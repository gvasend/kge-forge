"""Append-only, controller-owned authorization lifecycle (no model/tool entrypoint).

An activation commits under the common ownership-ledger and audit locks. Its
intent pins the complete preceding audit bytes. Recovery validates the original
authorization, dispatch authority, ordered events and exact effective binding.
"""
from dataclasses import replace
from pathlib import Path
import fcntl, json, os, signal
from .context_projection import canonical, digest, sha, read_exact


from .controller_authority_store import read_authority_ref


class LifecycleDenied(RuntimeError): pass


VALIDATION_KEYS = ('PD06_RELEASED', 'E1_B01_PASS', 'release_basis', 'release_decision',
    'operational_context', 'continuation_chain', 'full_context', 'model_projection',
    'released_profile', 'work_package', 'launch', 'clearance', 'no_material_continuation',
    'no_conflicting_scope', 'no_conflicting_reservation', 'supervisor_host_authority',
    'audit_isolation', 'provisioning')
TERMINAL = ('COMPLETED', 'REVOKED', 'CANCELLED')


def serialized(auth):
    value = dict(auth.__dict__)
    if auth.context_binding is not None:
        b = auth.context_binding
        value['context_binding'] = {'context_sha256': b.digest, 'capture_commit': b.capture_commit,
            'baseline_id': b.manifest.get('baseline_id'), 'work_id': b.manifest.get('work_id')}
    return json.loads(canonical(value))


def original(value):
    value = json.loads(canonical(value)); value['state'] = 'INACTIVE'
    op = json.loads(value['operational_binding']); op.pop('dispatch_authorization', None)
    value['operational_binding'] = canonical(op)
    return value


def historical_original(auth):
    value=original(serialized(auth));op=json.loads(value['operational_binding'])
    if op['governance'].get('schema') in (2,3):
        auth.context_binding.governance.verify()
        value['operational_binding']=canonical(auth.context_binding.governance.anchor_op)
    return value


def requires_lifecycle(auth):
    if not auth.operational_binding: return False
    op = json.loads(auth.operational_binding)
    ref = op['released_launch']
    launch = json.loads(read_authority_ref(ref))
    return launch['authorization']['state'] == 'INACTIVE'


def dispatch_binding(auth, audit, ref):
    decision = json.loads(read_authority_ref(ref))
    if 'invocation_attempt' in decision:
        from .controller_authority_store import current
        from .invocation_attempt import child_dispatch, require_claim
        require_claim(current(),decision['invocation_attempt'])
        if decision!=child_dispatch(current(),decision['invocation_attempt']):
            raise LifecycleDenied('unauthenticated invocation attempt dispatch')
    op = json.loads(auth.operational_binding)
    identities = op['governance']['identities']
    profile = json.loads(read_authority_ref(op['governance']['released_profile']))
    historical=None
    run2_mode=None
    if op['governance'].get('schema') == 5:
        from .attempt_context import verify_dispatch
        run2_mode=verify_dispatch(auth,decision)
    if op['governance'].get('schema') == 4:
        from .run2_context import verify_dispatch
        run2_mode=verify_dispatch(auth,decision)
    if op['governance'].get('schema') in (2,3):
        from .continuation_envelope import dispatch_ancestor
        historical=dispatch_ancestor(auth,decision)
    dispatch_context=historical or op
    expected = {'authorization_id': auth.authorization_id, 'revision': auth.revision,
        'session_id': auth.session_id, 'turn_id': auth.turn_id}
    if (decision.get('decision') != ('PROPOSED_DISPATCH' if run2_mode=='PROSPECTIVE' else 'DISPATCH_AUTHORIZED') or decision.get('authority') != 'Architect'
            or decision.get('invocation_identity') != expected
            or decision.get('work_package_id') != auth.work_package_id
            or decision.get('released_profile_sha256') != digest(profile)
            or any(decision.get(k) != v for k, v in dispatch_context['governance']['identities'].items())
            or any(decision.get(k) != dispatch_context['context_identities'][k]
                   for k in ('FullContextDigest', 'ModelProjectionDigest'))):
        raise LifecycleDenied('dispatch identity/context/profile mismatch')
    source = decision['authority_source']; read_authority_ref(source)
    bound = decision['all_authorized_bindings']
    task_path = json.loads(auth.context_projection)['task_path']
    if (bound['audit'] != str(Path(audit).resolve()) or bound['ownership_ledger'] != auth.ownership_ledger
            or bound['work_id'] != auth.work_package_id
            or bound['operational_binding_sha256'] != digest(historical or json.loads(original(serialized(auth))['operational_binding']))
            or bound['production_task_sha256'] != sha(Path(task_path).read_bytes())):
        raise LifecycleDenied('dispatch audit/ledger/task/original binding mismatch')
    return {**expected, **identities,
        'FullContextDigest': op['context_identities']['FullContextDigest'],
        'ModelProjectionDigest': op['context_identities']['ModelProjectionDigest'],
        'released_profile_sha256': digest(profile), 'work_package_id': auth.work_package_id,
        'production_task_sha256': bound['production_task_sha256'],
        'audit': str(Path(audit).resolve()), 'ownership_ledger': auth.ownership_ledger,
        **({k:op['context_identities'][k] for k in ('ModelPayloadDigest','ModelProjectionBindingDigest')} if historical or run2_mode else {}),
        'dispatch_record': ref, 'dispatch_record_id': 'E1-ARCHITECT-DISPATCH-sha256:' + ref['sha256']}


def event(body):
    result = dict(body); result['event_sha256'] = digest(body)
    result['event_id'] = 'E1-AUTHORIZATION-LIFECYCLE-sha256:' + result['event_sha256']
    return result


def decode(data):
    if data and not data.endswith(b'\n'): raise LifecycleDenied('truncated lifecycle audit')
    rows = []; prefix = b''
    for line in data.splitlines(keepends=True):
        try: row = json.loads(line)
        except (ValueError, UnicodeError) as exc: raise LifecycleDenied('invalid lifecycle audit') from exc
        rows.append((row, sha(prefix))); prefix += line
    return rows


def reconstruct(data, auth, audit):
    rows = decode(data); expected = serialized(auth); current_initial=original(expected);initial=dict(current_initial)
    op=json.loads(current_initial['operational_binding'])
    if op['governance'].get('schema') in (2,3):
        auth.context_binding.governance.verify()
        initial['operational_binding']=canonical(auth.context_binding.governance.anchor_op)
    state = None; phase = 'INACTIVE'; intent = None; commit = None; last = None
    seen = set(); effective = current_initial; dispatch_ref = None
    for row, prefix_hash in rows:
        name = row.get('event')
        if name == 'authorization_issued':
            issued = dict(row['authorization']); issued.setdefault('operational_binding', '')
            if state is None:
                if issued != initial: raise LifecycleDenied('original INACTIVE authorization changed or missing')
                state = 'INACTIVE'
            elif issued != effective and not (state=='INACTIVE' and issued==initial):
                raise LifecycleDenied('authorization record contradicts lifecycle state')
            continue
        if not str(name).startswith('authorization_lifecycle_'): continue
        if state is None: raise LifecycleDenied('lifecycle precedes original authorization')
        body = dict(row); eid = body.pop('event_id', None); fingerprint = body.pop('event_sha256', None)
        if body.get('version') != 1 or fingerprint != digest(body) or eid != 'E1-AUTHORIZATION-LIFECYCLE-sha256:' + fingerprint:
            raise LifecycleDenied('lifecycle event fingerprint mismatch')
        # Byte-identical repeated evidence never causes another transition.
        if eid in seen: continue
        if (body['predecessor_event'] != last or body['authorization_sha256'] != digest(initial)
                or body['audit_prefix_sha256'] != prefix_hash):
            raise LifecycleDenied('lifecycle order/original audit mismatch')
        ref = body['binding']['dispatch_record']
        if body['binding'] != dispatch_binding(auth, audit, ref):
            raise LifecycleDenied('activation binding mismatch')
        if dispatch_ref is not None and ref != dispatch_ref:
            raise LifecycleDenied('competing dispatch reference')
        dispatch_ref = ref
        if name == 'authorization_lifecycle_dispatch_authorized':
            if state != 'INACTIVE' or phase != 'INACTIVE': raise LifecycleDenied('duplicate dispatch lifecycle')
            if body['predecessor_state'] != 'INACTIVE' or body['resulting_state'] != 'INACTIVE':
                raise LifecycleDenied('dispatch alone cannot activate')
            phase = 'DISPATCH_AUTHORIZED'
        elif name == 'authorization_lifecycle_activation_intent':
            if state != 'INACTIVE' or phase != 'DISPATCH_AUTHORIZED':
                raise LifecycleDenied('activation predecessor is not inactive dispatch-authorized')
            if body['predecessor_state'] != 'INACTIVE' or body['resulting_state'] != 'INACTIVE':
                raise LifecycleDenied('intent alone cannot activate')
            if not valid_validation(body['validation'], body['binding']):
                raise LifecycleDenied('atomic activation validation incomplete')
            intent = row; phase = 'ACTIVATION_INDETERMINATE'
        elif name == 'authorization_lifecycle_activated':
            if state != 'INACTIVE' or phase != 'ACTIVATION_INDETERMINATE' or intent is None:
                raise LifecycleDenied('competing or invalid activation transition')
            if (body['predecessor_state'] != 'INACTIVE' or body['resulting_state'] != 'ACTIVE'
                    or body['intent_event_id'] != intent['event_id']
                    or body['validation'] != intent['validation']):
                raise LifecycleDenied('activation commit contradicts intent')
            effective = dict(current_initial); effective['state'] = 'ACTIVE'
            op = json.loads(effective['operational_binding']); op['dispatch_authorization'] = ref
            effective['operational_binding'] = canonical(op)
            if body['effective_authorization_sha256'] != digest(effective):
                raise LifecycleDenied('effective ACTIVE authorization changed')
            state = phase = 'ACTIVE'; commit = row
        elif name == 'authorization_lifecycle_terminal':
            target = body['resulting_state']
            if state not in ('INACTIVE', 'ACTIVE') or target not in TERMINAL or body['predecessor_state'] != state:
                raise LifecycleDenied('contradictory terminal lifecycle')
            state = phase = target
            effective = dict(effective); effective['state'] = target
        else: raise LifecycleDenied('unknown lifecycle event')
        seen.add(eid); last = eid
    if state is None: raise LifecycleDenied('original INACTIVE authorization missing')
    if expected['state'] == 'ACTIVE' and (state != 'ACTIVE' or expected != effective):
        raise LifecycleDenied('ACTIVE lacks exact durable activation event')
    if expected['state'] == 'INACTIVE' and expected != current_initial:
        raise LifecycleDenied('inactive authorization altered')
    return {'state': state, 'phase': phase, 'effective_authorization': effective,
        'activation_event': commit, 'last_event_id': last, 'dispatch_record': dispatch_ref,
        'non_active': state != 'ACTIVE', 'uncertain': phase == 'ACTIVATION_INDETERMINATE'}


def _read(fd):
    os.lseek(fd, 0, os.SEEK_SET)
    size = os.fstat(fd).st_size
    if size > 16 * 1024 * 1024: raise LifecycleDenied('audit exceeds lifecycle bound')
    data = b''
    while len(data) < size:
        part = os.read(fd, size - len(data))
        if not part: raise LifecycleDenied('audit truncated while reading')
        data += part
    return data


def _append(fd, row):
    # A signal-driven timing event must not interleave a partial authority record.
    mask=signal.pthread_sigmask(signal.SIG_BLOCK,{signal.SIGALRM})
    try:
        data = (canonical(row) + '\n').encode(); os.lseek(fd, 0, os.SEEK_END)
        while data:
            n = os.write(fd, data)
            if n <= 0: raise LifecycleDenied('activation write incomplete')
            data = data[n:]
        os.fsync(fd)
    finally:
        signal.pthread_sigmask(signal.SIG_SETMASK,mask)


def valid_validation(value, binding):
    # Retain readability of historical evidence; only the production transaction
    # can create new usable activation, and it requires a versioned receipt.
    if value == {k: 'PASS' for k in VALIDATION_KEYS}: return True
    body = dict(value); identity = body.pop('validation_id', None)
    return (body.get('schema') == 'PRODUCTION-DISPATCH-VALIDATION-1'
            and body.get('binding') == binding
            and identity == 'DISPATCH-VALIDATION-sha256:' + digest(body))


def activate(inactive, audit, dispatch_ref):
    """Only supported activation entrypoint; caller-supplied checklists forbidden."""
    from .activation_transaction import ActivationTransaction
    return ActivationTransaction.activate(inactive, audit, dispatch_ref)
