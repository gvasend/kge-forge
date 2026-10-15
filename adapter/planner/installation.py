"""I01 bounded definition installation; no governed lifecycle operation executes.

Live admission takes trust anchors outside the untrusted command. Replay checks
an already accepted, pinned admission receipt and the historical prefix instead
of issuing authority again. Only the external-route adapter is enabled.
"""
from dataclasses import replace
from pathlib import Path
import hashlib
from . import model as m


def _codec():
    from . import codec
    return codec


def require(ok, reason):
    if not ok:
        raise m.PlannerError(reason)


def simple(identity):
    return {'kind': identity.kind.value, 'namespace': identity.namespace, 'sha256': identity.sha256}


def identity(value):
    require(type(value) is dict and set(value) == {'kind','namespace','sha256'}, 'INSTALL_IDENTITY_DOMAIN')
    return m.ArtifactIdentity(m.IdentityKind(value['kind']), value['namespace'], value['sha256'])


def digest(value, namespace, kind=m.IdentityKind.CONTENT_IDENTITY):
    c = _codec()
    return m.ArtifactIdentity(kind, namespace, hashlib.sha256(c.canonical_bytes(value)).hexdigest())


def route_descriptor(definition):
    c = _codec()
    d = c.parse_json(definition.descriptor_json.encode())
    require(c.canonical_bytes(d).decode() == definition.descriptor_json, 'DEFINITION_NONCANONICAL')
    require(set(d) == {'schema','definition_type','canonical_body_schema','content_id','subject',
        'scope','lineage','generation','canonical_source_reference','source_pin','provenance','currentness_rule'}, 'DEFINITION_SCHEMA')
    require(d['schema'] == 'PLANNER-INSTALLABLE-DEFINITION-1', 'DEFINITION_SCHEMA')
    require(definition.id == digest(d,'planner-installable-definition-v1'), 'DEFINITION_ID')
    require(d['definition_type'] == 'EXTERNAL_RESOLUTION_CONTRACT' and
        d['canonical_body_schema'] == 'EXTERNAL-RESOLUTION-CONTRACT-1', 'DEFINITION_TYPE_NOT_ENABLED')
    subject = d['subject']
    require(set(subject) == {'kind','gate','requirement','consumer'} and
        subject['kind'] == 'EXTERNAL_ROUTE_ROLE' and all(type(v) is str and v for v in subject.values()), 'DEFINITION_SUBJECT')
    p = definition.provenance
    require(type(p.path) is str and bool(p.path) and not Path(p.path).is_absolute() and
        '..' not in Path(p.path).parts and Path(p.path).as_posix() == p.path, 'DEFINITION_SOURCE_PATH')
    content = identity(d['content_id'])
    require(content == c._identity(p.excerpt.encode(),'raw-file-sha256') and content == p.identity, 'CANONICAL_CONTENT_ID')
    require(d['source_pin'] == {'path':p.path,'profile':'raw-file-sha256','pointer':'','identity':simple(content)} and
        d['canonical_source_reference'] == {'kind':'IMMUTABLE_FILE','path':p.path,'content_id':simple(content)} and
        d['provenance'] == {'path':p.path,'content_id':simple(content),'section':p.section,'method':p.method,'scope':p.scope}, 'DEFINITION_SOURCE_PIN')
    require(p.scope == d['scope'] and p.section == '/', 'DEFINITION_PROVENANCE')
    rule = d['currentness_rule']
    expected_rule = {'schema':'PLANNER-DEFINITION-CURRENTNESS-1','rule_id':'EXTERNAL_RESOLUTION_CONTRACT_CURRENT_V1',
        'consumer':subject['consumer'],'native_predicate':'gates.governed_external_unknown',
        'native_predicate_source_sha256':hashlib.sha256((Path(__file__).parent/'gates.py').read_bytes()).hexdigest(),
        'installation_required':True,'authority_current_required':True,'source_current_required':True,
        'exact_scope_lineage_generation_required':True}
    require(rule == expected_rule, 'CURRENTNESS_RULE')
    body = c.parse_json(p.excerpt.encode())
    require(c.canonical_bytes(body).decode() == p.excerpt and set(body) == {'schema','contract'} and
        body['schema'] == d['canonical_body_schema'] and type(body['contract']) is dict, 'NATIVE_BODY_REQUIRED')
    require('$type' not in body['contract'] and 'provenance' not in body['contract'], 'NATIVE_BODY_REQUIRED')
    route = c._unwire(dict(body['contract'], **{'$type':'ExternalResolutionContract','provenance':c._wire(p)}))
    m.validate_types(route,m.ExternalResolutionContract)
    require((route.scope,route.lineage,route.generation) == (d['scope'],d['lineage'],d['generation']) and
        route.gate.value == subject['gate'] and route.requirement.value == subject['requirement'] and
        m.ActionId(subject['consumer']) in route.reentry, 'DEFINITION_TARGET')
    return d, route


def descriptor(definition):
    d = _codec().parse_json(definition.descriptor_json.encode())
    from . import proof_installation
    if d.get('definition_type') in proof_installation.TYPES:
        return proof_installation.descriptor(definition)
    if d.get('definition_type') == 'ACTION_DEFINITION':
        from . import action_installation as adapter
        return adapter.descriptor(definition)
    if d.get('definition_type') == 'EXTERNAL_RESOLUTION_CONTRACT':
        return route_descriptor(definition)
    if d.get('definition_type') == 'VALIDATION_SUPPORT_DEFINITION_SET':
        from . import validation_installation as validation
        return validation.descriptor(definition)
    from . import authentication_installation as auth
    return auth.descriptor(definition)


def old_reference(snapshot, d):
    c = _codec()
    subject = d['subject']
    installed = [x for x in snapshot.installed_definitions if descriptor(x.request.definition)[0]['subject'] == subject]
    if installed:
        # Registry order is an unordered collection; activation sequence is order.
        return max(installed,key=lambda x:x.request.sequence).id
    if d['definition_type'] == 'ACTION_DEFINITION':
        matches = [a for a in snapshot.actions if a.id.value == subject['action']]
        require(len(matches) == 1, 'ACTION_BASELINE_ROLE')
        return digest({'kind':'BASELINE_BOUND_DEFINITION_REFERENCE','role':subject,
            'pre_state_id':c._wire(c.snapshot_id(snapshot)), 'native_definition':c._wire(matches[0]),
            'source_pin_identity':c._wire(matches[0].source.identity)},'planner-baseline-definition-reference-v1')
    if d['definition_type'] != 'EXTERNAL_RESOLUTION_CONTRACT':
        return None
    matches = [r for g in snapshot.external_gates for r in g.resolution_contracts
        if r.gate.value == subject['gate'] and r.requirement.value == subject['requirement']]
    require(len(matches) <= 1,'DEFINITION_ROLE_CONFLICT')
    if not matches:
        return None
    r = matches[0]
    return digest({'kind':'BASELINE_BOUND_DEFINITION_REFERENCE','role':subject,
        'pre_state_id':c._wire(c.snapshot_id(snapshot)), 'native_definition':c._wire(r),
        'source_pin_identity':c._wire(r.provenance.identity)},'planner-baseline-definition-reference-v1')


def grant_fields(request):
    c = _codec()
    d,_ = descriptor(request.definition)
    return {'definition_id':simple(request.definition.id),'content_id':d['content_id'],
        'definition_type':d['definition_type'],'subject':d['subject'],'scope':d['scope'],
        'lineage':d['lineage'],'generation':d['generation'],'operation':request.operation.value,
        'expected_old_reference':None if request.expected_old_reference is None else simple(request.expected_old_reference),
        'pre_bundle':c._wire(request.expected_bundle),'pre_state':c._wire(request.expected_snapshot),
        'parent_event':c._wire(request.expected_parent_event),'policy':c._wire(request.policy),
        'policy_version':request.policy_version}


def admit_authority(grant, *, expected_grant, expected_decision, trusted_issuer, receipt_path):
    """Trusted caller supplies decision/grant/issuer anchors independently.

    This is authenticated transport, not a cryptographic signature or a general
    ISSUE permission. The immutable receipt is added only by a successful install.
    """
    c = _codec()
    gid = digest(grant,'planner-install-authority-v1',m.IdentityKind.AUTHORITY_IDENTITY)
    require(gid == expected_grant and grant.get('decision_id') == simple(expected_decision), 'AUTHORITY_TRUST_ANCHOR')
    require(trusted_issuer == 'QUALIFICATION_AUTHORITY' and grant.get('issuer') == trusted_issuer and
        grant.get('authority_class') == 'INSTALL' and grant.get('schema') == 'PLANNER-INSTALL-GRANT-1', 'INSTALL_ISSUER_CLASS')
    require(grant.get('use_limit') == 1 and grant.get('delegation') is False and
        type(grant.get('valid_from')) is int and type(grant.get('valid_until')) is int and
        grant['valid_from'] <= grant['valid_until'], 'INSTALL_AUTHORITY_BOUND')
    receipt = {'schema':'PLANNER-INSTALL-AUTHORITY-ADMISSION-1','authority_id':simple(gid),
        'grant':grant,'trusted_decision':simple(expected_decision),'trusted_issuer':trusted_issuer,
        'authentication':'EXPLICIT_HUMAN_DECISION_TRANSPORT','result':'ACCEPTED'}
    raw = c.canonical_bytes(receipt)
    p = m.Provenance(receipt_path,c._identity(raw,'raw-file-sha256'),'/',raw.decode(),
        'INSTALL_AUTHORITY_ADMISSION',grant['scope'])
    return m.InstallAuthority(gid,m.AuthorityClass.INSTALL,c.canonical_bytes(grant).decode(),p)


def validate_authority(request, ctx):
    c = _codec()
    a = request.authority
    require(a.authority_class is m.AuthorityClass.INSTALL,'INSTALL_AUTHORITY_CLASS')
    g = c.parse_json(a.grant_json.encode())
    require(c.canonical_bytes(g).decode() == a.grant_json and
        a.id == digest(g,'planner-install-authority-v1',m.IdentityKind.AUTHORITY_IDENTITY), 'INSTALL_AUTHORITY_ID')
    require(set(g) == set(grant_fields(request)) | {'schema','issuer','authority_class','decision_id',
        'contract_id','valid_from','valid_until','use_limit','delegation','provenance'}, 'INSTALL_GRANT_SCHEMA')
    require(all(g.get(k) == v for k,v in grant_fields(request).items()), 'INSTALL_AUTHORITY_APPLICABILITY')
    require(g['schema'] == 'PLANNER-INSTALL-GRANT-1' and g['authority_class'] == 'INSTALL' and
        g['issuer'] == 'QUALIFICATION_AUTHORITY' and g['use_limit'] == 1 and g['delegation'] is False and
        type(g['valid_from']) is int and type(g['valid_until']) is int and
        g['valid_from'] <= ctx.tick <= g['valid_until'], 'INSTALL_AUTHORITY_CURRENTNESS')
    for name in ('decision_id','contract_id','provenance'):
        identity(g[name])
    receipt = c.parse_json(a.admission_provenance.excerpt.encode())
    expected = {'schema':'PLANNER-INSTALL-AUTHORITY-ADMISSION-1','authority_id':simple(a.id),
        'grant':g,'trusted_decision':g['decision_id'],'trusted_issuer':g['issuer'],
        'authentication':'EXPLICIT_HUMAN_DECISION_TRANSPORT','result':'ACCEPTED'}
    p = a.admission_provenance
    require(receipt == expected and p.excerpt.encode() == c.canonical_bytes(expected) and
        p.identity == c._identity(p.excerpt.encode(),'raw-file-sha256') and p.scope == ctx.scope and
        p.section == '/' and p.method == 'INSTALL_AUTHORITY_ADMISSION', 'INSTALL_AUTHORITY_ADMISSION')


def command_key(request):
    c = _codec()
    w = c._wire(request);w.pop('command_key')
    return digest(w,'planner-install-command-v1')


def installed_id(request):
    d,_ = descriptor(request.definition)
    return digest({'request_key':simple(request.command_key),'definition_id':simple(request.definition.id),
        'authority_id':simple(request.authority.id),'logical_role':d['subject'],'operation':request.operation.value,
        'parent_event_id':simple(request.expected_parent_event),'activation_sequence':request.sequence,
        'scope':d['scope'],'lineage':d['lineage'],'generation':d['generation']},
        'planner-installed-definition-v1',m.IdentityKind.INSTANCE_IDENTITY)


def apply(snapshot, request):
    from .core import TransitionReport,recompute
    from . import gates
    c = _codec()
    m.validate_types(request,m.InstallDefinition)
    m.validate_model(snapshot)
    require(request.event_type == 'INSTALL_DEFINITION' and request.schema_version == 1,'INSTALL_EVENT_TYPE')
    require(request.command_key == command_key(request),'INSTALL_COMMAND_KEY')
    require(request.expected_snapshot == c.snapshot_id(snapshot),'INSTALL_PRE_STATE')
    require(request.expected_parent_event.namespace == 'planner-event-v1' and
        request.expected_parent_event.kind is m.IdentityKind.CONTENT_IDENTITY and request.sequence > 1,'INSTALL_ORDINARY_PARENT')
    d,route = descriptor(request.definition)
    ctx = snapshot.context
    require(ctx is not None and (ctx.scope,ctx.lineage,ctx.generation) == (d['scope'],d['lineage'],d['generation']), 'INSTALL_CONTEXT')
    validate_authority(request,ctx)
    require(not any(x.request.authority.id == request.authority.id for x in snapshot.installed_definitions),'INSTALL_AUTHORITY_CONSUMED')
    old = old_reference(snapshot,d)
    require(request.operation in (m.InstallationOperation.INSTALL,m.InstallationOperation.REPLACE), 'INSTALL_OPERATION_NOT_ENABLED')
    require((request.operation is m.InstallationOperation.INSTALL and old is None and request.expected_old_reference is None) or
        (request.operation is m.InstallationOperation.REPLACE and old is not None and old == request.expected_old_reference), 'INSTALL_COMPARE_AND_SWAP')
    require(not any(x.request.definition.id == request.definition.id for x in snapshot.installed_definitions), 'DEFINITION_ALREADY_INSTALLED')
    from . import proof_installation
    if d['definition_type'] in proof_installation.TYPES:
        return proof_installation.apply(snapshot,request,d,route)
    if d['definition_type'] == 'ACTION_DEFINITION':
        from . import action_installation as adapter
        return adapter.apply(snapshot,request,d,route)
    if d['definition_type'] == 'VALIDATION_SUPPORT_DEFINITION_SET':
        from . import validation_installation as validation
        return validation.apply(snapshot,request,d,route)
    require(not request.definition_sources,'INSTALL_UNEXPECTED_DEFINITION_SOURCES')
    if d['definition_type'] != 'EXTERNAL_RESOLUTION_CONTRACT':
        from . import authentication_installation as auth
        return auth.apply(snapshot,request,d,route)
    require(not request.authority_bindings,'INSTALL_UNEXPECTED_BINDING')
    gs = [g for g in snapshot.external_gates if g.id == route.gate]
    require(len(gs) == 1,'INSTALL_TARGET_GATE')
    gate = gs[0]
    new_gate = replace(gate,resolution_contracts=tuple(r for r in gate.resolution_contracts
        if r.requirement != route.requirement) + (route,))
    rec = m.InstalledDefinition(installed_id(request),request,old)
    updated = replace(snapshot,external_gates=tuple(new_gate if g.id == gate.id else g for g in snapshot.external_gates),
        installed_definitions=snapshot.installed_definitions + (rec,))
    req = next((r for r in updated.evidence_requirements if r.id == route.requirement),None)
    require(req is not None and gates.governed_external_unknown(updated,new_gate,req,m.ActionId(d['subject']['consumer'])), 'INSTALL_ADAPTER_NOT_APPLICABLE')
    m.validate_model(updated)
    return TransitionReport(updated,(),recompute(updated))


def validate_prefix(bundle, request):
    c = _codec()
    # Codec replay has already admitted the preceding event prefix by induction;
    # commit admits the full bundle before calling this checker. Hash those exact
    # bytes without recursively replaying the same prefix a second time.
    prefix_identity = c._identity(c._bundle_bytes_admitted(bundle), 'planner-bundle-v1')
    require(request.expected_bundle == prefix_identity and request.expected_snapshot == c.snapshot_id(bundle.current) and
        request.expected_parent_event == (bundle.events[-1].identity if bundle.events else None) and
        request.sequence == len(bundle.events)+1,'INSTALL_PREFIX_MISMATCH')
    require(request.policy == bundle.policy and request.policy_version == bundle.policy_version,'INSTALL_POLICY')
    invalidated = {i for e in bundle.events if type(e.result) is m.SourceInvalidation for i in e.result.changed}
    require(not invalidated.intersection(support_ids(request)), 'INSTALL_SUPPORT_ALREADY_INVALIDATED')
    c._check_snapshot_pins(bundle.current,bundle.sources)
    expected = tuple(m.ArtifactPin(p.path,p.identity) for p in request_provenances(request))
    require(set(request.source_additions) == set(p for p in expected if p not in bundle.sources),'INSTALL_SOURCE_SET')
    c._unwire(c._wire(request))
    require(not any(p.path == old.path and p != old for p in request.source_additions for old in bundle.sources), 'INSTALL_SOURCE_OVERWRITE')
    for p in request.source_additions:
        c.validate_pin(p)


def request_provenances(request):
    d,_ = descriptor(request.definition)
    from . import proof_installation
    if d['definition_type'] in proof_installation.TYPES:
        adapter = proof_installation
    elif d['definition_type'] == 'ACTION_DEFINITION':
        require(not request.definition_sources,'INSTALL_UNEXPECTED_DEFINITION_SOURCES')
        from . import action_installation as adapter
    elif d['definition_type'] == 'VALIDATION_SUPPORT_DEFINITION_SET':
        from . import validation_installation as adapter
    else:
        require(not request.definition_sources,'INSTALL_UNEXPECTED_DEFINITION_SOURCES')
        from . import authentication_installation as adapter
    return (request.definition.provenance,request.authority.admission_provenance) + adapter.extra_provenances(request)


def provenances(snapshot):
    return [p for x in snapshot.installed_definitions for p in request_provenances(x.request)] + [x.provenance for x in snapshot.ingress_contracts]


def support_ids(request):
    grant = _codec().parse_json(request.authority.grant_json.encode())
    return {p.identity for p in request_provenances(request)} | {v for x in request.authority_bindings for v in (x.operating_authorization_id,x.declared_authority_reference)} | {
        identity(grant[k]) for k in ('decision_id','contract_id','provenance')}


def route_support_current(snapshot, route):
    """Consumer guard for an installed role; baseline definitions are unchanged.

    Snapshot integrity/event witness is checked by native bundle replay. Runtime
    consumption also checks authority/support currentness in the live context.
    """
    records = [x for x in snapshot.installed_definitions if
        descriptor(x.request.definition)[0]['definition_type'] == 'EXTERNAL_RESOLUTION_CONTRACT' and
        descriptor(x.request.definition)[0]['subject']['gate'] == route.gate.value and
        descriptor(x.request.definition)[0]['subject']['requirement'] == route.requirement.value]
    if not records:
        return True
    active = max(records,key=lambda x:x.request.sequence)
    try:
        d,r = descriptor(active.request.definition)
        require(active.validation is m.ValidationState.ACCEPTED and r == route,'INSTALL_ROUTE_SUPPORT')
        require((snapshot.context.scope,snapshot.context.lineage,snapshot.context.generation) ==
            (d['scope'],d['lineage'],d['generation']),'INSTALL_CONTEXT')
        validate_authority(active.request,snapshot.context)
        return True
    except m.PlannerError:
        return False


def current(bundle, record):
    """Derived currentness, never a persisted CURRENT flag or fallback binding."""
    from . import gates
    c = _codec()
    try:
        d,r = descriptor(record.request.definition)
        ctx = bundle.current.context
        require(record.validation is m.ValidationState.ACCEPTED,'INSTALL_INVALIDATED')
        require((ctx.scope,ctx.lineage,ctx.generation) == (d['scope'],d['lineage'],d['generation']), 'INSTALL_CONTEXT')
        validate_authority(record.request,ctx)
        require(old_reference(bundle.current,d) == record.id,'INSTALL_SUPERSEDED')
        event = bundle.events[record.request.sequence-1]
        require(event.result == record.request and event.parent_event == record.request.expected_parent_event and
            record.id == installed_id(record.request),'INSTALL_EVENT_WITNESS')
        invalidated = {i for e in bundle.events if type(e.result) is m.SourceInvalidation for i in e.result.changed}
        require(not invalidated.intersection(support_ids(record.request)), 'INSTALL_SOURCE_INVALIDATED')
        for p in request_provenances(record.request):
            require(m.ArtifactPin(p.path,p.identity) in bundle.sources,'INSTALL_SOURCE_MISSING')
        if d['definition_type'] != 'EXTERNAL_RESOLUTION_CONTRACT':
            from . import proof_installation
            if d['definition_type'] in proof_installation.TYPES:
                adapter = proof_installation
            elif d['definition_type'] == 'ACTION_DEFINITION':
                from . import action_installation as adapter
            elif d['definition_type'] == 'VALIDATION_SUPPORT_DEFINITION_SET':
                from . import validation_installation as adapter
            else:
                from . import authentication_installation as adapter
            require(adapter.support_current(bundle.current,record),'DEFINITION_NOT_CURRENT')
            return True
        g = next(g for g in bundle.current.external_gates if g.id == r.gate)
        req = next(q for q in bundle.current.evidence_requirements if q.id == r.requirement)
        require(r in g.resolution_contracts and gates.governed_external_unknown(bundle.current,g,req,m.ActionId(d['subject']['consumer'])), 'INSTALL_ROUTE_NOT_CURRENT')
        return True
    except (m.PlannerError,IndexError,StopIteration,AttributeError):
        return False


def commit(bundle, request, output_dir, repo_root, *, expected_authority, expected_decision, expected_operating_authority=None):
    """Validate/stage privately, publish one locked/fsynced canonical HEAD."""
    c = _codec()
    require(request.authority.id == expected_authority,'INSTALL_LIVE_TRUST_ANCHOR')
    g = c.parse_json(request.authority.grant_json.encode())
    require(g.get('decision_id') == simple(expected_decision),'INSTALL_LIVE_TRUST_ANCHOR')
    if request.authority_bindings:
        require(len(request.authority_bindings)==1 and request.authority_bindings[0].operating_authorization_id==expected_operating_authority,'OPERATING_ATTEST_LIVE_TRUST_ANCHOR')
    c._replay(bundle);c._verify_sources(bundle,repo_root)
    directory = c._transaction_directory(output_dir,repo_root)
    with c._transaction_lock(directory):
        head = c._read_head(directory,bundle,repo_root)
        require(c.canonical_bytes(c._wire(head.initial)) == c.canonical_bytes(c._wire(bundle.initial)) and
            c.canonical_bytes(c._wire(head.events[:len(bundle.events)])) == c.canonical_bytes(c._wire(bundle.events)) and
            all(p in head.sources for p in bundle.sources),'UNTRUSTED_HEAD_LINEAGE')
        for index,event in enumerate(head.events):
            if type(event.result) is m.InstallDefinition and event.result.command_key == request.command_key:
                require(c.canonical_bytes(c._wire(event.result)) == c.canonical_bytes(c._wire(request)), 'INSTALL_IDEMPOTENCY_CONFLICT')
                return head,c.bundle_id(c._prefix_bundle(head,index+1)),True
        require(c.bundle_id(head) == c.bundle_id(bundle),'INSTALL_STALE_HEAD')
        validate_prefix(head,request)
        for pin in request.source_additions:
            c._path(repo_root,pin.path)  # Reject traversal/symlink paths before staging any bytes.
        validate_authority(request,head.current.context)
        require(request.command_key == command_key(request),'INSTALL_COMMAND_KEY')
        d,_ = descriptor(request.definition)
        active = [x for x in head.current.installed_definitions if x.id == old_reference(head.current,d)]
        if active and active[0].request.definition == request.definition:
            require(request.operation is m.InstallationOperation.REPLACE and
                request.expected_old_reference == active[0].id and current(head,active[0]), 'INSTALL_DUPLICATE_NOT_CURRENT')
            return head,c.bundle_id(head),True
        updated = c._extend_private(head,request)
        updated = replace(updated,sources=head.sources+request.source_additions)
        c._replay(updated)
        require(current(updated,updated.current.installed_definitions[-1]),'INSTALL_NOT_CURRENT')
        # All semantic checks pass before any durable artifact is written.
        for p in request_provenances(request):
            target = Path(repo_root).resolve()/p.path
            parent = c._transaction_directory(target.parent,repo_root)
            c._write_immutable(parent,target.name,p.excerpt.encode());c._fsync_directory(parent)
        ident = c._publish_head(directory,updated,c.bundle_id(head),request.command_key,repo_root)
        return updated,ident,False
