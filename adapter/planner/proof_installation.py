"""Governed prospective source/slot configuration and deferred typed contracts.

Definitions are configuration, never Proof instances. Operating fixture DECIDE
is authenticated independently from INSTALL. Live support gates activation of
already sealed concrete contracts; consumers recheck installed currentness.
"""
from dataclasses import replace
from pathlib import Path
from . import model as m

TYPES = {'ROOT_SLOT_CONFIGURATION_SET', 'SLOT_PROOF_CONTRACT_DEFINITION',
         'ROOT_PROOF_CONTRACT_DEFINITION'}


def env():
    from . import codec as c, installation as i
    return c, i


def nested_pins(value):
    found = {}
    def visit(x):
        if type(x) is dict:
            if 'path' in x and 'content_id' in x:
                key = (x['path'], tuple(sorted(x['content_id'].items())))
                found[key] = x
            for v in x.values(): visit(v)
        elif type(x) is list:
            for v in x: visit(v)
    visit(value)
    return tuple(found.values())


def descriptor(definition):
    c, i = env(); q = i.require; p = definition.provenance
    d = c.parse_json(definition.descriptor_json.encode())
    q(set(d) == set('schema definition_type canonical_body_schema content_id subject scope lineage generation canonical_source_reference source_pin provenance currentness_rule'.split()), 'PROOF_DEFINITION_SCHEMA')
    q(d['definition_type'] in TYPES and d['schema'] == 'PLANNER-INSTALLABLE-DEFINITION-1' and definition.id == i.digest(d, 'planner-installable-definition-v1') and c.canonical_bytes(d).decode() == definition.descriptor_json, 'PROOF_DEFINITION_ID')
    q(p.path and not Path(p.path).is_absolute() and '..' not in Path(p.path).parts and Path(p.path).as_posix() == p.path, 'PROOF_DEFINITION_PATH')
    q(i.identity(d['content_id']) == p.identity == c._identity(p.excerpt.encode(), 'raw-file-sha256'), 'PROOF_CONTENT')
    q(d['source_pin'] == {'path':p.path,'profile':'raw-file-sha256','pointer':'','identity':i.simple(p.identity)} and d['canonical_source_reference'] == {'kind':'IMMUTABLE_FILE','path':p.path,'content_id':i.simple(p.identity)} and d['provenance'] == {'path':p.path,'content_id':i.simple(p.identity),'section':p.section,'method':p.method,'scope':p.scope} and p.section == '/' and p.scope == d['scope'], 'PROOF_SOURCE_PIN')
    b = c.parse_json(p.excerpt.encode())
    q(c.canonical_bytes(b).decode() == p.excerpt and b.get('schema') == d['canonical_body_schema'], 'PROOF_NATIVE_BODY')
    for k in ('scope','lineage','generation'):
        q(b.get(k) == d[k], 'PROOF_CONTEXT')
    q(b.get('consumer') == d['subject']['consumer'] and b.get('qualification_only') is True and type(b.get('valid_until')) is int, 'PROOF_CONSUMER')
    common = {'schema':'PLANNER-DEFINITION-CURRENTNESS-1','installation_required':True,'authority_current_required':True,'source_current_required':True,'exact_scope_lineage_generation_required':True,'consumer':b['consumer']}
    if d['definition_type'] == 'ROOT_SLOT_CONFIGURATION_SET':
        q(set(d['subject']) == {'kind','root','slot','consumer'} and d['subject']['kind'] == 'ROOT_SLOT_CONFIGURATION_ROLE', 'PROOF_CONFIGURATION_SUBJECT')
        q(b['schema'] == 'PLANNER-ROOT-SLOT-CONFIGURATION-SET-1' and d['currentness_rule'] == dict(common, rule_id='ROOT_SLOT_CONFIGURATION_CURRENT_V1'), 'PROOF_CONFIGURATION_TYPE')
        q(b.get('no_concrete_contract_installed_yet') is True and b.get('no_proof_instances') is True, 'PROOF_INSTANCE_NOT_DEFINITION')
        q(len(b['sources']) == len(b['source_entity_definitions']) == len(b['semantic_policies']) == len(b['semantic_authority_specs']) == len(b['concrete_proof_declarations']) == 2, 'PROOF_CONFIGURATION_CARDINALITY')
    else:
        root = d['definition_type'] == 'ROOT_PROOF_CONTRACT_DEFINITION'
        expected_rule = dict(common, rule_id='TYPED_PROOF_CONTRACT_CURRENT_V1')
        if root: expected_rule['independent_root_source_required'] = True
        q(b['schema'] == 'PLANNER-TYPED-PROOF-CONTRACT-DEFINITION-1' and d['currentness_rule'] == expected_rule and b.get('contract', {}).get('$type') == 'TypedProofContract', 'PROOF_INSTANCE_NOT_DEFINITION')
        contract = c._unwire(b['contract']); m.validate_types(contract, m.TypedProofContract)
        from . import typed_proofs as t
        q(contract.id == t.identity(contract) and contract.proof_type is (m.TypedProofKind.ROOT_PROOF if root else m.TypedProofKind.SLOT_PROOF), 'PROOF_CONTRACT_ID_TYPE')
        q(d['subject'] == {'kind':'TYPED_PROOF_CONTRACT_ROLE','proof_type':contract.proof_type.value,'target':contract.target.value,'consumer':b['consumer']}, 'PROOF_TARGET')
        q((contract.scope,contract.lineage,contract.generation,contract.valid_until) == (d['scope'],d['lineage'],d['generation'],b['valid_until']), 'PROOF_CONTRACT_CONTEXT')
        q(contract.validation is m.ValidationState.ACCEPTED, 'PROOF_CONTRACT_STALE')
    return d, b


def bodies(request):
    c, i = env(); d, b = descriptor(request.definition)
    required = nested_pins(b)
    ps = {p.path:p for p in request.definition_sources}
    i.require(len(ps) == len(request.definition_sources) == len(required), 'PROOF_DEFINITION_SOURCE_SET')
    out = {}
    for pin in required:
        p = ps.get(pin['path'])
        i.require(p is not None and p.identity == i.identity(pin['content_id']) == c._identity(p.excerpt.encode(),'raw-file-sha256') and p.section == '/' and p.scope == d['scope'], 'PROOF_NESTED_SOURCE_PIN')
        m.validate_provenance(p)
        v = c.parse_json(p.excerpt.encode())
        i.require(c.canonical_bytes(v).decode() == p.excerpt, 'PROOF_NESTED_CANONICAL_BODY')
        out[p.path] = v
    return d, b, out


def extra_provenances(request):
    return request.definition_sources + tuple(x.accepted_admission_provenance for x in request.authority_bindings)


def admit_semantic_authority(grant, *, expected_grant, expected_decision, trusted_issuer, receipt_path):
    c, i = env()
    gid = i.digest(grant, 'planner-fixture-semantic-authorization-v1', m.IdentityKind.AUTHORITY_IDENTITY)
    i.require(gid == expected_grant and grant.get('decision_id') == i.simple(expected_decision) and grant.get('issuer') == trusted_issuer == 'QUALIFICATION_AUTHORITY', 'FIXTURE_SEMANTIC_TRUST_ANCHOR')
    i.require(grant.get('schema') == 'PLANNER-FIXTURE-SEMANTIC-GRANT-1' and grant.get('authority_class') == 'DECIDE' and grant.get('delegation') is False and grant.get('automatic_issuance_by_install') is False, 'FIXTURE_SEMANTIC_CLASS')
    receipt = {'schema':'PLANNER-FIXTURE-SEMANTIC-ADMISSION-1','grant_id':i.simple(gid),'grant':grant,'trusted_decision':i.simple(expected_decision),'trusted_issuer':trusted_issuer,'authentication':'EXPLICIT_HUMAN_DECISION_TRANSPORT','result':'ACCEPTED'}
    raw = c.canonical_bytes(receipt)
    return m.DefinitionAuthorityBinding(m.AuthorityClass.DECIDE, i.identity(grant['semantic_request_id']), gid, c.canonical_bytes(grant).decode(), m.Provenance(receipt_path,c._identity(raw,'raw-file-sha256'),'/',raw.decode(),'FIXTURE_SEMANTIC_ADMISSION',grant['scope']))


def validate_semantics(request, d, b):
    c, i = env(); q = i.require
    q(len(request.authority_bindings) == 1, 'FIXTURE_SEMANTIC_AUTHORITY_REQUIRED')
    x = request.authority_bindings[0]; g = c.parse_json(x.issued_authorization_json.encode())
    q(x.authority_class is m.AuthorityClass.DECIDE and x.operating_authorization_id == i.digest(g,'planner-fixture-semantic-authorization-v1',m.IdentityKind.AUTHORITY_IDENTITY), 'FIXTURE_SEMANTIC_CLASS')
    q(g == dict(schema='PLANNER-FIXTURE-SEMANTIC-GRANT-1',issuer='QUALIFICATION_AUTHORITY',authority_class='DECIDE',decision_id=g.get('decision_id'),semantic_request_id=i.simple(x.declared_authority_reference),configuration_definition_id=i.simple(request.definition.id),scope=d['scope'],lineage=d['lineage'],generation=d['generation'],consumer=b['consumer'],valid_from=0,valid_until=b['valid_until'],delegation=False,automatic_issuance_by_install=False,sources=b['sources'],policies=b['semantic_policies'],authority_specs=b['semantic_authority_specs']), 'FIXTURE_SEMANTIC_APPLICABILITY')
    expected = {'schema':'PLANNER-FIXTURE-SEMANTIC-ADMISSION-1','grant_id':i.simple(x.operating_authorization_id),'grant':g,'trusted_decision':g['decision_id'],'trusted_issuer':'QUALIFICATION_AUTHORITY','authentication':'EXPLICIT_HUMAN_DECISION_TRANSPORT','result':'ACCEPTED'}
    p = x.accepted_admission_provenance
    q(c.parse_json(p.excerpt.encode()) == expected and p.excerpt.encode() == c.canonical_bytes(expected) and p.identity == c._identity(p.excerpt.encode(),'raw-file-sha256') and p.method == 'FIXTURE_SEMANTIC_ADMISSION' and p.scope == d['scope'] and p.section == '/', 'FIXTURE_SEMANTIC_ADMISSION')


def configuration(request):
    c, i = env(); q = i.require
    d, b, files = bodies(request); validate_semantics(request,d,b)
    sources = [files[x['path']] for x in b['sources']]
    q({x['role'] for x in sources} == {'SLOT_PROOF','ROOT_PROOF'}, 'ROOT_SOURCE_INDEPENDENCE')
    slot_source = next(x for x in sources if x['role'] == 'SLOT_PROOF')
    root_source = next(x for x in sources if x['role'] == 'ROOT_PROOF')
    for x in sources:
        q(x.get('schema') == 'PLANNER-QUALIFICATION-PROPOSITION-SOURCE-1' and x.get('asserts_execution') is False and x.get('asserts_satisfaction') is False, 'QUALIFICATION_SOURCE_BODY')
        q(all(x[k] == b[k] for k in ('scope','lineage','generation','consumer','valid_until','qualification_only')), 'PROOF_SOURCE_CONTEXT')
    q(slot_source['id'] != root_source['id'] and b['sources'][0]['content_id'] != b['sources'][1]['content_id'] and slot_source['provenance_origin'] != root_source['provenance_origin'] and slot_source['proposition']['id'] != root_source['proposition']['id'], 'ROOT_SOURCE_INDEPENDENCE')
    slot_body, root_body = files[b['slot']['path']], files[b['existing_root_to_bind']['path']]
    slot, root = c._unwire(slot_body['contract']), c._unwire(root_body['contract'])
    m.validate_types(slot,m.ValueSlot); m.validate_types(root,m.RootCondition)
    q(slot.id.value == d['subject']['slot'] == slot_source['target'] and root.id.value == d['subject']['root'] == root_source['target'] and slot.state is m.SlotState.UNRESOLVED and root.state is m.ConditionState.UNRESOLVED and slot.value is None and not slot.requirements and not slot.root_requirements and root.predicate is None, 'PROOF_TARGET_DEFINITIONS')
    q(slot_body['proposition'] == slot_source['proposition']['id'] and root_body['proposition'] == root_source['proposition']['id'] and root_body['independent_source_required'] is True and root_body['required_slot'] == slot.id.value, 'PROOF_SOURCE_PROPOSITION')
    # Prospective SOURCE bodies may omit these native inert defaults. Expand at
    # the typed adapter boundary; never change codec identity/required fields or
    # the sealed authored bytes, and never synthesize permissions or execution.
    source_defaults = {'permissions':[], 'target':None, 'consumed':False, 'validator':None}
    entities = tuple(c._unwire(dict(source_defaults, **x)) for x in b['source_entity_definitions'])
    authorities = []
    for source, pin, entity, policy_pin, spec in zip(sources,b['sources'],entities,b['semantic_policies'],b['semantic_authority_specs']):
        m.validate_types(entity,m.GraphEntity)
        q((entity.scope,entity.lineage,entity.generation,entity.valid_until) == (d['scope'],d['lineage'],d['generation'],b['valid_until']), 'PROOF_SOURCE_CONTEXT')
        q(entity.kind is m.EntityKind.SOURCE and entity.id.value == source['id'] and entity.identity == i.identity(pin['content_id']) and entity.provenance.path == pin['path'] and entity.provenance.excerpt.encode() == c.canonical_bytes(source) and entity.provenance.identity == entity.identity and entity.produced and entity.validated and not entity.permissions and entity.target is None and not entity.consumed and entity.validator is None and entity.decision is None and entity.choice is None and entity.validation is m.ValidationState.ACCEPTED, 'PROOF_SOURCE_ENTITY')
        policy = files[policy_pin['path']]
        q(all(policy[k] == b[k] for k in ('scope','lineage','generation','consumer','valid_until','qualification_only')), 'PROOF_POLICY_CONTEXT')
        q(policy['schema'] == 'PLANNER-BOUNDED-QUALIFICATION-FIXTURE-POLICY-1' and policy['native_permission'] == 'DECIDE' and policy['source_content_id'] == pin['content_id'] and policy['subject'] == source['target'] and policy['native_authority_target'] == pin['content_id'] and policy['no_delegation'] is True, 'PROOF_SEMANTIC_POLICY')
        q(spec['permissions'] == ['DECIDE'] and spec['target'] == pin['content_id'] and c._unwire(spec['identity']) == i.identity(policy_pin['content_id']) and spec['binding']['scope'] == d['scope'] and spec['binding']['lineage'] == d['lineage'] and spec['binding']['generation'] == d['generation'], 'PROOF_AUTHORITY_BOUND')
        p = c._unwire(spec['provenance'])
        q(p.path == policy_pin['path'] and p.identity == i.identity(policy_pin['content_id']) and p.excerpt.encode() == c.canonical_bytes(policy), 'PROOF_POLICY_PROVENANCE')
        authorities.append(m.GraphEntity(c._unwire(spec['entity_id']),m.EntityKind.AUTHORITY,c._unwire(spec['identity']),p,d['scope'],d['lineage'],d['generation'],b['valid_until'],permissions=(m.AuthorityClass.DECIDE,),target=i.identity(pin['content_id'])))
    contracts = tuple(c._unwire(files[x['path']]['contract']) for x in b['concrete_proof_declarations'])
    from . import typed_proofs as t
    for contract, source, pin, authority in zip(contracts,sources,b['sources'],authorities):
        m.validate_types(contract,m.TypedProofContract)
        q(contract.id == t.identity(contract) and contract.proof_type.value == source['role'] and contract.proposition == source['proposition']['id'] and contract.target.value == source['target'] and contract.authority == authority.id and contract.authority_identity == authority.identity and contract.provenance.identity == i.identity(pin['content_id']) and contract.provenance.path == pin['path'] and contract.provenance.excerpt.encode() == c.canonical_bytes(source), 'PROOF_DECLARATION_BINDING')
        q((contract.scope,contract.lineage,contract.generation,contract.valid_until) == (d['scope'],d['lineage'],d['generation'],b['valid_until']), 'PROOF_DECLARATION_CONTEXT')
    q(contracts[0].supports == (m.KnowledgeId(slot_source['support_selector']['knowledge']),) and contracts[1].supports == (slot.id,), 'PROOF_SUPPORT_DECLARATION')
    q(root_source['support_selector']['slot'] == slot.id.value and root_source['support_selector']['proposition'] == contracts[0].proposition and root_source['support_selector']['proof_kind'] == 'SLOT_PROOF' and root_source['support_selector']['native_state'] == 'RESOLVED', 'ROOT_SUPPORT_DECLARATION')
    return d, b, files, slot, root, entities + tuple(authorities), contracts


def records(snapshot, typ):
    c, _ = env()
    return [r for r in snapshot.installed_definitions if c.parse_json(r.request.definition.descriptor_json.encode()).get('definition_type') == typ]


def support_current(snapshot, record):
    c, i = env()
    try:
        d, b = descriptor(record.request.definition);ctx=snapshot.context
        i.require(record.validation is m.ValidationState.ACCEPTED and i.old_reference(snapshot,d) == record.id and (ctx.scope,ctx.lineage,ctx.generation) == (d['scope'],d['lineage'],d['generation']), 'PROOF_INSTALL_CURRENT')
        i.validate_authority(record.request,ctx)
        if d['definition_type'] == 'ROOT_SLOT_CONFIGURATION_SET':
            _,_,_,slot,root,entities,_=configuration(record.request)
            i.require(any(s.id == slot.id and s.required_type == slot.required_type and s.value is None and not s.requirements and not s.root_requirements for s in snapshot.slots) and any(r.id == root.id and r.predicate is None for r in snapshot.roots), 'PROOF_CONFIGURATION_FRAME')
            from .gates import usable
            for e in entities:
                actual=next(x for x in snapshot.entities if x.id == e.id)
                i.require(actual == e and usable(actual,snapshot).state is m.ProofState.PROVED,'PROOF_SOURCE_POLICY_CURRENT')
        else:
            configurations = [r for r in records(snapshot,'ROOT_SLOT_CONFIGURATION_SET') if any(p.id == c._unwire(b['contract']).id for p in configuration(r.request)[-1])]
            i.require(len(configurations)==1 and support_current(snapshot,configurations[0]),'PROOF_CONFIGURATION_NOT_CURRENT')
            contract=c._unwire(b['contract'])
            i.require(contract in snapshot.proof_contracts,'PROOF_CONTRACT_NOT_CURRENT')
        return True
    except (m.PlannerError,ValueError,KeyError,StopIteration,AttributeError,TypeError):
        return False


def contract_current(snapshot, contract):
    c,_=env()
    owners=[r for r in records(snapshot,'ROOT_SLOT_CONFIGURATION_SET') if contract.target in {x.target for x in configuration(r.request)[-1]}]
    if not owners: return True  # Legacy independently admitted E06 contracts unchanged.
    if len(owners) != 1 or contract not in configuration(owners[0].request)[-1]: return False
    typ=contract.proof_type.value+'_CONTRACT_DEFINITION'
    installed=[r for r in records(snapshot,typ) if c._unwire(descriptor(r.request.definition)[1]['contract']).id == contract.id]
    return len(owners)==len(installed)==1 and support_current(snapshot,installed[0])


def normalize_dependencies(snapshot, dependencies):
    """Native source EntityId changes also reach the concrete contract role."""
    c,_=env();out=set(dependencies)
    for r in records(snapshot,'ROOT_SLOT_CONFIGURATION_SET'):
        _,_,_,_,_,entities,contracts=configuration(r.request)
        for entity in entities:
            if entity.id in out or entity.identity in out:
                out.update(p.id for p in snapshot.proof_contracts if p.id in {x.id for x in contracts} and (p.provenance.identity == entity.identity or p.authority == entity.id))
    return tuple(sorted(out,key=lambda x:(type(x).__name__,str(x))))


def apply(snapshot, request, d, b):
    c,i=env();from .core import TransitionReport,recompute
    i.require(request.operation is m.InstallationOperation.INSTALL,'PROOF_INSTALL_ONLY')
    if d['definition_type'] == 'ROOT_SLOT_CONFIGURATION_SET':
        _,_,_,slot,root,entities,_=configuration(request)
        i.require(root in snapshot.roots and not any(s.id==slot.id for s in snapshot.slots) and not set(e.id for e in entities).intersection(e.id for e in snapshot.entities),'PROOF_CONFIGURATION_CONFLICT')
        updated=replace(snapshot,slots=snapshot.slots+(slot,),entities=snapshot.entities+entities)
    else:
        i.require(not request.authority_bindings,'PROOF_CONTRACT_UNEXPECTED_AUTHORITY')
        _,_,_=bodies(request);contract=c._unwire(b['contract'])
        owners=[r for r in records(snapshot,'ROOT_SLOT_CONFIGURATION_SET') if contract in configuration(r.request)[-1]]
        i.require(len(owners)==1 and support_current(snapshot,owners[0]),'PROOF_CONFIGURATION_NOT_CURRENT')
        from . import typed_proofs as t
        if contract.proof_type is m.TypedProofKind.SLOT_PROOF:
            knowledge=next((k for k in snapshot.knowledge if k.id==contract.supports[0]),None)
            source=c.parse_json(contract.provenance.excerpt.encode())
            expected=c._unwire(source['support_selector']['expected_output_contract'])
            from .gates import current_completion
            i.require(knowledge==expected and knowledge is not None and knowledge.producer is not None and current_completion(snapshot,knowledge.producer),'PROOF_ACTUAL_KNOWLEDGE_REQUIRED')
        else:
            matching=[p for p in snapshot.typed_proofs if p.target==contract.supports[0] and t.usable(snapshot,p)]
            i.require(len(matching)==1 and any(s.id==contract.supports[0] and s.state is m.SlotState.RESOLVED for s in snapshot.slots),'PROOF_ACTUAL_SLOT_REQUIRED')
        i.require(tuple(t.support_identity(snapshot,x) for x in contract.supports)==contract.support_identities,'PROOF_SUPPORT_FINGERPRINT')
        i.require(not any(p.target==contract.target for p in snapshot.proof_contracts),'PROOF_CONTRACT_ROLE_CONFLICT')
        updated=replace(snapshot,proof_contracts=snapshot.proof_contracts+(contract,))
    record=m.InstalledDefinition(i.installed_id(request),request,request.expected_old_reference)
    updated=replace(updated,installed_definitions=updated.installed_definitions+(record,))
    m.validate_model(updated);i.require(support_current(updated,record),'PROOF_INSTALL_NOT_APPLICABLE')
    return TransitionReport(updated,(),recompute(updated))
