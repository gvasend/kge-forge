"""Controller bootstrap from an externally pinned store; no authority issuance."""
from pathlib import Path
from .validation_spans import measured
import json
from .controller_authority_store import authority_bytes, read_authority_ref, capture_evidence
from .context_projection import canonical, sha, derive


def capture_inputs(auth, audit, dispatch):
    """Offline engineering inventory of the verifier's immutable dependencies.

    No import happens here. The caller selects and pins a resulting store only
    after qualifying the exact continuation and controller bootstrap.
    """
    from .context_binding import CommittedContext
    from .governance_continuation import verify_authorization
    from .authorization_lifecycle import dispatch_binding
    with capture_evidence() as records:
        op = json.loads(auth.operational_binding)
        context = CommittedContext(auth.context_binding.path, auth.context_binding.capture_commit,
                                   op['governance'])
        from dataclasses import replace
        verified = replace(auth, context_binding=context)
        verify_authorization(verified)
        dispatch_binding(verified, audit, dispatch)
        derive(json.loads(auth.context_projection), context)
        # Snapshot provenance reads committed objects for the exact execution
        # inputs, beyond the mandatory governing-source closure. Capture those
        # immutable Git witnesses too; missing/new files still require governed
        # action provenance at execution time.
        runtime = json.loads(auth.execution_profile)
        for rel in runtime['inputs']:
            entry = Path(runtime['cwd']) / rel
            if entry.is_symlink(): raise ValueError('snapshot input symlink')
            candidates = sorted(entry.rglob('*')) if entry.is_dir() else [entry]
            for path in candidates:
                if path.is_file() and not path.is_symlink():
                    context.captured_file(path)
        profile = json.loads(read_authority_ref(op['governance']['released_profile']))
        basis = json.loads(read_authority_ref(op['governance']['release_basis']))
        for p, row in basis.get('current_inputs', basis.get('inputs')).items():
            if row['sha256'] == profile['provisioning_receipt_sha256']:
                authority_bytes('sha256:'+row['sha256'], evidence_path=p)
        # Bootstrap representations preserve effective authorization and existing
        # context identity. They grant nothing beyond the verified ancestry.
        raw = dict(auth.__dict__)
        raw['context_binding'] = {'path': str(context.path), 'capture_commit': context.capture_commit}
        records[auth.authorization_id] = {'bytes': canonical(raw).encode(), 'evidence': []}
        records[op['governance']['identities']['OperationalContextId']] = {
            'bytes': auth.operational_binding.encode(), 'evidence': []}
    return records


def selection(auth, audit, dispatch):
    op = json.loads(auth.operational_binding)
    g = op['governance']
    aliases = {
        g['identities']['ReleaseBasisId']: 'sha256:'+g['release_basis']['sha256'],
        g['identities']['ReleaseDecisionId']: 'sha256:'+g['release_decision']['sha256'],
        'E1-ARCHITECT-DISPATCH-sha256:'+dispatch['sha256']: 'sha256:'+dispatch['sha256'],
    }
    applicability = {'authorization_id': auth.authorization_id, **g['identities']}
    decision = json.loads(read_authority_ref(dispatch))
    provenance = {'authority_source': decision['authority_source'],
                  'release_identities': g['identities']}
    private = {
        auth.authorization_id+':audit': {'path': str(audit), 'mutation': 'APPEND_ONLY',
                                         'mechanism': 'authorization_lifecycle / GovernedHost._write'},
        auth.authorization_id+':ownership': {'path': auth.ownership_ledger, 'mutation': 'TYPED_LIFECYCLE',
                                             'mechanism': 'InvocationOwnership / ActivationTransaction'},
    }
    return aliases, applicability, provenance, private


@measured('private_bootstrap')
def reconstruct_authorization(store, authorization_id):
    """Call in store.session(). No repository evidence file is a bootstrap input."""
    from .controller_authority_store import current, AuthorityDenied
    from .context_binding import CommittedContext
    from .governed_host import WorkAuthorization
    if current() is not store:
        raise AuthorityDenied('private bootstrap session required')
    raw = json.loads(store.resolve(authorization_id))
    if raw['authorization_id'] != authorization_id:
        raise AuthorityDenied('bootstrap authorization identity mismatch')
    # Run 2 cannot inherit the cancelled Run-1 dispatch or consume a proposal
    # as authority. This is additional to all existing reconstruction checks.
    if raw.get('work_package_id') == 'E1-WP-001' and raw.get('revision') == 8:
        if json.loads(raw['operational_binding'])['governance'].get('schema') != 4:
            from .run2_amendment import verify
            verify(authorization_id)
    op_id = store.applicability['OperationalContextId']
    op_bytes = store.resolve(op_id)
    if raw['operational_binding'].encode() != op_bytes:
        raise AuthorityDenied('bootstrap operational binding mismatch')
    saved = raw['context_binding']
    raw['context_binding'] = CommittedContext(saved['path'], saved['capture_commit'],
                                             json.loads(op_bytes)['governance'])
    for key in ('read_roots', 'write_roots', 'deny_roots', 'exec_bins',
                'read_deny_roots', 'write_deny_roots', 'write_directory_roots'):
        raw[key] = tuple(raw[key])
    raw['exec_argv_allowlist'] = tuple(tuple(x) for x in raw['exec_argv_allowlist'])
    auth = WorkAuthorization(**raw)
    store.require(auth)
    return auth
