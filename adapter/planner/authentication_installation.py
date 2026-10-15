"""Closed prospective authentication/ingress adapters for INSTALL_DEFINITION.

Operating ATTEST is admitted independently; installation only projects its
accepted declaration. No Evidence or attestation instance is created here.
"""
from dataclasses import replace
from pathlib import Path
from . import model as m


def env():
    from . import codec as c, installation as i
    return c,i


def descriptor(definition):
    c,i=env();q=i.require
    d=c.parse_json(definition.descriptor_json.encode());p=definition.provenance
    q(c.canonical_bytes(d).decode()==definition.descriptor_json,'DEFINITION_NONCANONICAL')
    q(set(d)=={'schema','definition_type','canonical_body_schema','content_id','subject','scope','lineage','generation','canonical_source_reference','source_pin','provenance','currentness_rule'},'DEFINITION_SCHEMA')
    types={'AUTHENTICATION_DEFINITION_SET':('PLANNER-AUTHENTICATION-DEFINITION-SET-1','INGRESS_AUTHENTICATION_ROLE','AUTHENTICATION_SET_CURRENT_V1'),
           'EVIDENCE_INGRESS_CONTRACT':('PLANNER-EVIDENCE-INGRESS-1','EVIDENCE_INGRESS_ROLE','EVIDENCE_INGRESS_CURRENT_V1')}
    q(d['definition_type'] in types,'DEFINITION_TYPE_NOT_ENABLED')
    schema,role,rule=types[d['definition_type']]
    q(d['schema']=='PLANNER-INSTALLABLE-DEFINITION-1' and definition.id==i.digest(d,'planner-installable-definition-v1'),'DEFINITION_ID')
    q(d['canonical_body_schema']==schema,'NATIVE_BODY_REQUIRED')
    q(p.path and not Path(p.path).is_absolute() and '..' not in Path(p.path).parts and Path(p.path).as_posix()==p.path,'DEFINITION_SOURCE_PATH')
    q(i.identity(d['content_id'])==p.identity==c._identity(p.excerpt.encode(),'raw-file-sha256'),'CANONICAL_CONTENT_ID')
    q(d['source_pin']=={'path':p.path,'profile':'raw-file-sha256','pointer':'','identity':i.simple(p.identity)} and
      d['canonical_source_reference']=={'kind':'IMMUTABLE_FILE','path':p.path,'content_id':i.simple(p.identity)} and
      d['provenance']=={'path':p.path,'content_id':i.simple(p.identity),'section':p.section,'method':p.method,'scope':p.scope} and p.scope==d['scope'] and p.section=='/','DEFINITION_SOURCE_PIN')
    s=d['subject'];keys={'kind','gate','requirement','consumer','source','receipt_action'}
    if role=='EVIDENCE_INGRESS_ROLE':keys.add('authentication')
    q(set(s)==keys and s['kind']==role and all(type(s[k]) is str and s[k] for k in keys-{'source'}),'DEFINITION_SUBJECT')
    m.validate_types(c._unwire(s['source']),m.ArtifactIdentity)
    r=d['currentness_rule'];q(set(r)=={'schema','rule_id','consumer','native_consumer','qualified_precedent_source_hashes','installation_required','authority_current_required','source_current_required','exact_scope_lineage_generation_required'} and
      r['schema']=='PLANNER-DEFINITION-CURRENTNESS-1' and r['rule_id']==rule and r['consumer']==s['consumer'] and r['native_consumer']=='evidence.apply' and
      all(r[k] is True for k in ('installation_required','authority_current_required','source_current_required','exact_scope_lineage_generation_required')),'CURRENTNESS_RULE')
    hashes=r['qualified_precedent_source_hashes'];q(set(hashes)=={'attestor.py','evidence.py','evidence_attestation.py','gates.py','installation.py'} and all(type(v) is str and len(v)==64 and all(ch in '0123456789abcdef' for ch in v) for v in hashes.values()),'PRECEDENT_PIN')
    b=c.parse_json(p.excerpt.encode());q(c.canonical_bytes(b).decode()==p.excerpt and b.get('schema')==schema,'NATIVE_BODY_REQUIRED')
    if role=='EVIDENCE_INGRESS_ROLE':
        q(set(b)=={'schema','contract'} and b['contract'].get('$type')=='EvidenceIngressContract' and 'provenance' not in b['contract'],'NATIVE_BODY_REQUIRED')
        native=c._unwire(dict(b['contract'],provenance=c._wire(p)));m.validate_types(native,m.EvidenceIngressContract)
        q(native.gate.value==s['gate'] and native.receipt_action==s['receipt_action'] and native.requirements==(m.EvidenceId(s['requirement']),) and native.authentication.value==s['authentication'] and
          (native.scope,native.lineage,native.generation)==(d['scope'],d['lineage'],d['generation']),'INGRESS_BINDING')
        return d,native
    q(set(b)=={'schema','authority_reference','binding','scope','lineage','generation','members','operating_authority_requirement','projection'},'AUTHENTICATION_SET_SCHEMA')
    q(b['binding']=={k:s[k] for k in ('gate','requirement','consumer','source','receipt_action')} and
      (b['scope'],b['lineage'],b['generation'])==(d['scope'],d['lineage'],d['generation']),'AUTHENTICATION_BINDING')
    q(b['projection']=={'entity_provenance':'COMMON_SET_PROVENANCE','predicate_provenance':'MEMBERSHIP_WITNESS_TO_COMMON_SET_PROVENANCE','standalone_member_activation':False},'AUTHENTICATION_PROJECTION')
    members=b['members'];q(set(members)=={'authority','authority_predicate','attestor','source_predicate'},'AUTHENTICATION_ATOMIC_MEMBERS')
    native={}
    schemas={'authority':'PLANNER-ATTEST-AUTHORITY-REFERENCE-1','authority_predicate':'PLANNER-ATTEST-AUTHORITY-PREDICATE-1','attestor':'PLANNER-ATTESTOR-DEFINITION-1','source_predicate':'PLANNER-SOURCE-ATTESTOR-PREDICATE-1'}
    for key,x in members.items():
        q(set(x)=={'body','content_id','definition_id','source'},'AUTHENTICATION_MEMBER_SCHEMA')
        v=x['body'];q(set(v)=={'schema','authority_reference','binding','scope','lineage','generation','native_definition','native_type'} and v['schema']==schemas[key] and
          all(v[k]==b[k] for k in ('authority_reference','binding','scope','lineage','generation')),'AUTHENTICATION_MEMBER_BINDING')
        q(c._unwire(x['content_id'])==c._identity(c.canonical_bytes(v),'raw-file-sha256'),'AUTHENTICATION_MEMBER_CONTENT')
        did=c._unwire(x['definition_id']);q(did.namespace=='planner-installable-definition-v1' and did.kind is m.IdentityKind.CONTENT_IDENTITY,'AUTHENTICATION_MEMBER_ID')
        w=v['native_definition'];q('provenance' not in w,'NATIVE_BODY_REQUIRED')
        typ=m.GraphEntity if key in ('authority','attestor') else m.Predicate
        q(v['native_type']==typ.__name__ and w.get('$type')==typ.__name__,'AUTHENTICATION_MEMBER_TYPE')
        native[key]=c._unwire(dict(w,provenance=c._wire(p)) if typ is m.GraphEntity else w);m.validate_types(native[key],typ)
        member_type={'authority':'ATTEST_AUTHORITY_REFERENCE','authority_predicate':'ATTEST_AUTHORITY_PREDICATE','attestor':'ATTESTOR_DEFINITION','source_predicate':'SOURCE_ATTESTOR_PREDICATE'}[key]
        md=dict(d,definition_type=member_type,canonical_body_schema=v['schema'],content_id=i.simple(c._unwire(x['content_id'])),
          subject=dict(s,kind='AUTHENTICATION_MEMBER_ROLE',object_id=native[key].id.value),
          canonical_source_reference={'kind':'IMMUTABLE_FILE','path':x['source'],'content_id':i.simple(c._unwire(x['content_id']))},
          source_pin={'path':x['source'],'profile':'raw-file-sha256','pointer':'','identity':i.simple(c._unwire(x['content_id']))},
          provenance={'path':x['source'],'content_id':i.simple(c._unwire(x['content_id'])),'section':'/','method':p.method,'scope':d['scope']},
          currentness_rule=dict(d['currentness_rule'],rule_id='AUTHENTICATION_MEMBER_CURRENT_V1'))
        q(did==i.digest(md,'planner-installable-definition-v1'),'AUTHENTICATION_MEMBER_ID')

    a,t,ap,sp=(native[k] for k in ('authority','attestor','authority_predicate','source_predicate'))
    source=c._unwire(s['source']);q(a.identity==c._unwire(b['authority_reference']) and a.id!=t.id and a.identity!=t.identity and ap.id!=sp.id,'AUTHENTICATION_IDENTITY')
    for e in (a,t):
        q(e.kind is m.EntityKind.AUTHORITY and e.identity.kind is m.IdentityKind.AUTHORITY_IDENTITY and e.permissions==(m.AuthorityClass.ATTEST,) and e.target==source and e.produced and e.validated and e.validation is m.ValidationState.ACCEPTED and not e.consumed and
          (e.scope,e.lineage,e.generation)==(d['scope'],d['lineage'],d['generation']) and e.validator is None and e.decision is None and e.choice is None,'AUTHENTICATION_ENTITY')
    for pred,entity in ((ap,a),(sp,t)):
        q(pred.kind is m.PredicateKind.AUTHORITY and pred.entity==entity.id and pred.expected==source and pred.permission is m.AuthorityClass.ATTEST and
          not pred.operands and pred.knowledge is None and pred.action is None and pred.condition is None and pred.other is None and pred.obligation is None and pred.unavailable is None,'AUTHENTICATION_PREDICATE')
    req=b['operating_authority_requirement']
    q(set(req)=={'admission_schema','authority_identity','automatic_issuance_by_install','class','delegation','exact_members','issuer_role','source','valid_from','valid_until'} and req['admission_schema']=='PLANNER-ATTEST-DEFINITION-ADMISSION-1' and
      req['authority_identity']==b['authority_reference'] and req['automatic_issuance_by_install'] is False and req['class']=='ATTEST' and req['delegation'] is False and req['issuer_role']=='QUALIFICATION_AUTHORITY' and req['source']==s['source'] and
      req['exact_members']=={k:x['definition_id'] for k,x in members.items()} and type(req['valid_from']) is int and type(req['valid_until']) is int and req['valid_from']<=req['valid_until']==a.valid_until==t.valid_until,'OPERATING_AUTHORITY_REQUIREMENT')
    return d,native


def admit_operating_authority(grant, *, expected_grant, expected_decision, trusted_issuer, receipt_path):
    c,i=env();gid=i.digest(grant,'planner-attest-definition-authorization-v1',m.IdentityKind.AUTHORITY_IDENTITY)
    i.require(gid==expected_grant and grant.get('authenticated_decision_reference')==i.simple(expected_decision) and trusted_issuer=='QUALIFICATION_AUTHORITY' and grant.get('issuer_role')==trusted_issuer,'ATTEST_AUTHORITY_TRUST_ANCHOR')
    receipt={'schema':'PLANNER-ATTEST-DEFINITION-ADMISSION-1','grant_id':i.simple(gid),'exact_grant_json':c.canonical_bytes(grant).decode(),
      'trusted_issuer_reference':trusted_issuer,'authenticated_decision_reference':i.simple(expected_decision),'admission_policy_reference':grant['I03_contract_content_reference'],'result':'ACCEPTED','provenance':grant['provenance']}
    raw=c.canonical_bytes(receipt);p=m.Provenance(receipt_path,c._identity(raw,'raw-file-sha256'),'/',raw.decode(),'ATTEST_DEFINITION_ADMISSION',grant['scope'])
    return m.DefinitionAuthorityBinding(m.AuthorityClass.ATTEST,c._unwire(grant['declared_authority_identity']),gid,c.canonical_bytes(grant).decode(),p)


def validate_binding(request,d,native,ctx):
    c,i=env();q=i.require
    q(len(request.authority_bindings)==1,'OPERATING_ATTEST_REQUIRED');x=request.authority_bindings[0];g=c.parse_json(x.issued_authorization_json.encode())
    q(set(g)=={'schema','authority_class','issuer','issuer_role','authenticated_decision_reference','I03_contract_content_reference','declared_authority_identity','member_definition_and_content_ids','source','consumer','gate','requirement','scope','lineage','generation','valid_from','valid_until','delegation','provenance'},'ATTEST_GRANT_SCHEMA')
    b=c.parse_json(request.definition.provenance.excerpt.encode());s=d['subject']
    q(g['schema']=='PLANNER-ATTEST-DEFINITION-AUTHORIZATION-1' and g['authority_class']=='ATTEST' and g['issuer_role']=='QUALIFICATION_AUTHORITY' and g['issuer']=='AUTHENTICATED_HUMAN_USER' and g['delegation'] is False and x.authority_class is m.AuthorityClass.ATTEST,'OPERATING_ATTEST_CLASS')
    q(g['declared_authority_identity']==b['authority_reference'] and x.declared_authority_reference==native['authority'].identity and
      g['member_definition_and_content_ids']=={k:{'definition_id':v['definition_id'],'content_id':v['content_id']} for k,v in b['members'].items()},'OPERATING_ATTEST_SUBJECT')
    q(all(g[k]==d[k] for k in ('scope','lineage','generation')) and all(g[k]==s[k] for k in ('source','consumer','gate','requirement')) and
      type(g['valid_from']) is int and type(g['valid_until']) is int and g['valid_from']<=ctx.tick<=g['valid_until'] and g['valid_until']==native['authority'].valid_until and g['valid_from']==b['operating_authority_requirement']['valid_from'],'OPERATING_ATTEST_CURRENTNESS')
    q(c.canonical_bytes(g).decode()==x.issued_authorization_json and x.operating_authorization_id==i.digest(g,'planner-attest-definition-authorization-v1',m.IdentityKind.AUTHORITY_IDENTITY),'OPERATING_ATTEST_ID')
    for k in ('authenticated_decision_reference','I03_contract_content_reference','provenance'):i.identity(g[k])
    ig=c.parse_json(request.authority.grant_json.encode());q(g['authenticated_decision_reference']==ig['decision_id'] and g['I03_contract_content_reference']==ig['contract_id'],'OPERATING_ATTEST_DECISION')
    p=x.accepted_admission_provenance;r=c.parse_json(p.excerpt.encode())
    expected={'schema':'PLANNER-ATTEST-DEFINITION-ADMISSION-1','grant_id':i.simple(x.operating_authorization_id),'exact_grant_json':x.issued_authorization_json,'trusted_issuer_reference':g['issuer_role'],'authenticated_decision_reference':g['authenticated_decision_reference'],'admission_policy_reference':g['I03_contract_content_reference'],'result':'ACCEPTED','provenance':g['provenance']}
    q(r==expected and p.excerpt==c.canonical_bytes(expected).decode() and p.identity==c._identity(p.excerpt.encode(),'raw-file-sha256') and p.scope==ctx.scope and p.section=='/' and p.method=='ATTEST_DEFINITION_ADMISSION','OPERATING_ATTEST_ADMISSION')


def extra_provenances(request):
    c,i=env();d=c.parse_json(request.definition.descriptor_json.encode())
    ps=tuple(x.accepted_admission_provenance for x in request.authority_bindings)
    if d.get('definition_type')=='AUTHENTICATION_DEFINITION_SET':
        b=c.parse_json(request.definition.provenance.excerpt.encode())
        ps+=tuple(m.Provenance(v['source'],c._unwire(v['content_id']),'/',c.canonical_bytes(v['body']).decode(),request.definition.provenance.method,d['scope']) for v in b['members'].values())
    return ps


def role_record(snapshot,d):
    c,i=env()
    rs=[r for r in snapshot.installed_definitions if i.descriptor(r.request.definition)[0]['subject']==d['subject']]
    return max(rs,key=lambda r:r.request.sequence) if rs else None


def support_current(snapshot,record):
    c,i=env()
    try:
        d,n=descriptor(record.request.definition);ctx=snapshot.context
        i.require(record.validation is m.ValidationState.ACCEPTED and (ctx.scope,ctx.lineage,ctx.generation)==(d['scope'],d['lineage'],d['generation']) and role_record(snapshot,d)==record,'AUTHENTICATION_INACTIVE')
        i.validate_authority(record.request,ctx)
        if d['definition_type']=='AUTHENTICATION_DEFINITION_SET':
            validate_binding(record.request,d,n,ctx)
            i.require(all(x in snapshot.entities for x in (n['authority'],n['attestor'])) and all(x in snapshot.predicates for x in (n['authority_predicate'],n['source_predicate'])),'AUTHENTICATION_MEMBERS_ABSENT')
            from . import gates
            i.require(all(gates.evaluate_predicate(snapshot,n[k].id).state is m.ProofState.PROVED for k in ('authority_predicate','source_predicate')),'AUTHENTICATION_UNPROVED')
        else:
            i.require(n in snapshot.ingress_contracts,'INGRESS_NOT_INSTALLED');authentication_record(snapshot,d,n)
        return True
    except (m.PlannerError,AttributeError,KeyError):return False


def authentication_record(snapshot,d,ingress):
    c,i=env();matches=[]
    for r in snapshot.installed_definitions:
        x,n=i.descriptor(r.request.definition)
        if x['definition_type']=='AUTHENTICATION_DEFINITION_SET' and x['subject']['gate']==d['subject']['gate'] and n['source_predicate'].id==ingress.authentication:
            matches.append((r,x,n))
    i.require(len(matches)==1,'INGRESS_AUTHENTICATION_SET')
    r,x,n=matches[0]
    i.require(support_current(snapshot,r) and all(x[k]==d[k] for k in ('scope','lineage','generation')) and all(x['subject'][k]==d['subject'][k] for k in ('gate','requirement','consumer','source','receipt_action')),'INGRESS_AUTHENTICATION_CURRENTNESS')
    return r,n


def apply(snapshot,request,d,n):
    c,i=env();q=i.require
    from .core import TransitionReport,recompute
    s=d['subject'];gate=next((g for g in snapshot.external_gates if g.id.value==s['gate']),None)
    req=next((r for r in snapshot.evidence_requirements if r.id.value==s['requirement']),None)
    q(gate is not None and req is not None and req.id in gate.requirements and gate.receipt_action==s['receipt_action'] and c._unwire(s['source']) in req.producers,'AUTHENTICATION_CONSUMER_SOURCE')
    rec=m.InstalledDefinition(i.installed_id(request),request,request.expected_old_reference)
    q(request.operation is m.InstallationOperation.INSTALL,'AUTHENTICATION_OPERATION')
    if d['definition_type']=='AUTHENTICATION_DEFINITION_SET':
        validate_binding(request,d,n,snapshot.context)
        q(not ({n['authority'].id,n['attestor'].id}&{x.id for x in snapshot.entities}) and not ({n['authority_predicate'].id,n['source_predicate'].id}&{x.id for x in snapshot.predicates}),'AUTHENTICATION_MEMBER_CONFLICT')
        updated=replace(snapshot,entities=snapshot.entities+(n['authority'],n['attestor']),predicates=snapshot.predicates+(n['authority_predicate'],n['source_predicate']),installed_definitions=snapshot.installed_definitions+(rec,))
    else:
        q(not request.authority_bindings,'INGRESS_UNEXPECTED_AUTHORITY_BINDING')
        authentication_record(snapshot,d,n)
        q(not any(x.gate==n.gate and x.receipt_action==n.receipt_action for x in snapshot.ingress_contracts),'INGRESS_ROLE_CONFLICT')
        q(n.valid_until>=snapshot.context.tick,'INGRESS_EXPIRED')
        q(any(x.source_class==n.source_class and x.requirement==req.id for x in gate.resolution_contracts),'INGRESS_ROUTE_SOURCE')
        updated=replace(snapshot,ingress_contracts=snapshot.ingress_contracts+(n,),installed_definitions=snapshot.installed_definitions+(rec,))
    m.validate_model(updated);q(support_current(updated,rec),'AUTHENTICATION_NOT_CURRENT')
    return TransitionReport(updated,(),recompute(updated))


def consumer_guard(snapshot,contract,attestation):
    c,i=env()
    rs=[r for r in snapshot.installed_definitions if i.descriptor(r.request.definition)[0]['definition_type']=='EVIDENCE_INGRESS_CONTRACT' and i.descriptor(r.request.definition)[1].gate==contract.gate]
    if not rs:
        auth_sets=[r for r in snapshot.installed_definitions if i.descriptor(r.request.definition)[0]['definition_type']=='AUTHENTICATION_DEFINITION_SET' and i.descriptor(r.request.definition)[0]['subject']['gate']==contract.gate.value]
        i.require(not auth_sets,'INGRESS_NOT_INSTALLED')
        return
    i.require(len(rs)==1,'INGRESS_ROLE_CONFLICT');r=rs[0];d,n=descriptor(r.request.definition)
    i.require(n==contract and support_current(snapshot,r),'INGRESS_NOT_CURRENT')
    _,members=authentication_record(snapshot,d,n)
    i.require(attestation is not None and attestation.source_predicate==n.authentication and attestation.attestor==members['attestor'].identity and attestation.attestor_authority==members['authority'].identity,'EVIDENCE_ATTESTATION_CHAIN')
    from . import evidence_attestation as ea
    fields=dict(vars(attestation));fields.pop('attestation_id')
    i.require(ea.identity(**fields)==attestation.attestation_id,'EVIDENCE_ATTESTATION_ID')
