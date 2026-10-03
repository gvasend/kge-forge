"""Finite synthetic budget contract normalization, never live E1 evidence.

Trust is an independently pinned qualification parameter contract. Submission
hashes/claims do not establish competence or adopt real applicability rules.
"""
import hashlib
import json
from dataclasses import replace
from pathlib import Path

from . import model as m

PARAMETER_PIN = '1b0533a7c24306c2452a68df1b5777d1b6d699420aa1947b1b3ac5ef5d5079f7'
SUFFIXES = ('AVAILABILITY_PUBLICATION','SCOPE','LINEAGE','RUNTIME','CONTROLLER_STORE_G4',
            'PROGRAMMER_PROFILE','TEMPORAL_CURRENTNESS','EXECUTION_REQUEST_PHASE')
ROLES = ('PUBLISHER','SCOPE_OWNER','LINEAGE_OWNER','RUNTIME_OWNER','STORE_OWNER',
         'PROFILE_OWNER','VALIDITY_OWNER','PHASE_OWNER')
IDS = tuple('BUDGET-PROOF-'+s for s in SUFFIXES)
ENVELOPE = ('authority','invocation','dispatch','context','release','runtime','controller_store',
            'profile','lineage','source_scope','target_scope','operation')


def require(value, reason):
    if not value:
        raise m.PlannerError('budget: '+reason)


def fields(obj, names):
    require(type(obj) is dict and set(obj)==set(names.split()), 'unknown/missing fields')


def canonical(obj):
    # The profile's ASCII identity algorithm is explicit, independent of planner JSON.
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False)


def digest(obj):
    return hashlib.sha256(canonical(obj).encode()).hexdigest()


def identity(value):
    fields(value,'kind namespace sha256')
    require(all(type(v) is str and v for v in value.values()),'identity types')
    try:
        result=m.ArtifactIdentity(m.IdentityKind(value['kind']),value['namespace'],value['sha256'])
        m.validate_types(result,m.ArtifactIdentity)
    except (ValueError,TypeError) as exc:
        raise m.PlannerError('budget: invalid identity') from exc
    return result


def structural(value):
    require(value is not None,'null unsupported')
    if type(value) is dict:
        for key,item in value.items():
            require(type(key) is str and bool(key),'key type')
            structural(item)
    elif type(value) is list:
        for item in value: structural(item)
    else:
        require(type(value) in (str,int,bool),'scalar type')
        if type(value) is str: require(bool(value),'empty string')


def validate_input(parameters, submission, trusted_parameter_pin=PARAMETER_PIN):
    """Validate closed contract; caller supplies trust separately, not in submission.

    Returns verified indexed records. No planner objects or expected outputs are
    inputs. Unsupported/missing/stale evidence rejects; no partial positive result.
    """
    structural(parameters); structural(submission)
    fields(parameters,'mode expected_envelope anchor trusted_record_grants parameters_sha256')
    body={k:v for k,v in parameters.items() if k!='parameters_sha256'}
    require(digest(body)==parameters['parameters_sha256']==trusted_parameter_pin,'parameter pin mismatch')
    fields(submission,'schema mode envelope records source_authentication_id rows invalidated_ids')
    require(submission['schema']=='BUDGET-PROOF-SUBMISSION-1','schema')
    require(submission['mode']==parameters['mode']=='SYNTHETIC_QUALIFICATION_ONLY','synthetic mode required')
    e=parameters['expected_envelope']; fields(e,' '.join(ENVELOPE))
    for key in ENVELOPE[:9]: identity(e[key])
    for key,kind in (('authority','AUTHORITY_IDENTITY'),('invocation','INSTANCE_IDENTITY'),
                     ('release','RELEASE_IDENTITY'),('runtime','CONTENT_IDENTITY')):
        require(e[key]['kind']==kind,'identity domain')
    require(type(e['source_scope']) is str and e['source_scope'].endswith('/FIRST_PROGRAMMER_EXECUTION'),'source scope phase')
    require(type(e['target_scope']) is str and e['target_scope'].endswith('/FIRST_PROGRAMMER_REQUEST'),'target scope phase')
    require(e['operation']=='BUDGET_REFERENCE_PRECONSTRUCTION','operation')
    require(submission['envelope']==e,'envelope mismatch')
    anchor=parameters['anchor']; fields(anchor,'id generation envelope')
    require(type(anchor['generation']) is int and anchor['generation']>=0 and anchor['envelope']==e,'anchor')
    require(type(anchor['id']) is str,'anchor id')
    for key in ('records','rows','invalidated_ids'): require(type(submission[key]) is list,'collection type')
    require(type(parameters['trusted_record_grants']) is list,'grants type')
    records={}; indices={}
    for i,record in enumerate(submission['records']):
        fields(record,'id body'); require(type(record['id']) is str,'record id')
        require(record['id'] not in records and digest(record['body'])==record['id'],'duplicate/hash mismatch')
        records[record['id']]=record['body']; indices[record['id']]=i
    grants={}
    for grant in parameters['trusted_record_grants']:
        fields(grant,'record_id role producer envelope anchor'); identity(grant['producer'])
        require(type(grant['record_id']) is str and type(grant['role']) is str,'grant type')
        key=(grant['record_id'],grant['role']); require(key not in grants,'duplicate grant'); grants[key]=grant
    used=set()
    def record(ref,role,kind,extra):
        require(type(ref) is str and ref in records,'missing evidence')
        r=records[ref]; fields(r,'synthetic record_type producer envelope anchor generation '+extra)
        require(r['synthetic'] is True and r['record_type']==kind,'record type')
        identity(r['producer'])
        require(r['envelope']==e and r['anchor']==anchor['id'],'cross-field envelope/anchor')
        require(type(r['generation']) is int and r['generation']==anchor['generation'],'stale generation')
        g=grants.get((ref,role)); require(g is not None,'untrusted producer')
        require(g['producer']==r['producer'] and g['envelope']==e and g['anchor']==anchor['id'],'competence binding')
        used.add(ref); return r
    auth=record(submission['source_authentication_id'],'BUDGET_OWNER','SOURCE_AUTHENTICATION',
                'source_type authority_identity identity_verified owning_policy_preserved')
    require(auth['source_type']=='StatusBudgetAuthority' and auth['authority_identity']==e['authority'] and
            auth['identity_verified'] is True and auth['owning_policy_preserved'] is True,'source authentication')
    rows={}
    for row in submission['rows']:
        fields(row,'id fact_id rule_id'); require(type(row['id']) is str and row['id'] not in rows,'duplicate row')
        rows[row['id']]=row
    require(set(rows)==set(IDS),'missing/extra obligation')
    for name,role in zip(IDS,ROLES):
        row=rows[name]
        fbody=record(row['fact_id'],role,'FACT','obligation facts')
        rbody=record(row['rule_id'],'GOVERNING_RULE_OWNER','RULE','obligation rule_profile policy')
        require(fbody['obligation']==rbody['obligation']==name,'row substitution')
        require(rbody['rule_profile']=='EXACT_CHECKPOINT_1','unresolved governing rule')
        f,p=fbody['facts'],rbody['policy']; suffix=name[len('BUDGET-PROOF-'):]
        # Schema types are checked independently of truthiness/equality: bool != int.
        def schema(obj,keys):
            fields(obj,' '.join(keys))
            for key,typ in keys.items():
                if typ=='id': identity(obj[key])
                else: require(type(obj[key]) is typ,'fact/policy value type')
        if suffix=='AVAILABILITY_PUBLICATION':
            schema(f,dict(available=bool,authority_body='id',store='id',published=bool)); schema(p,dict(publication=str))
            ok=f['available'] and f['authority_body']==e['authority'] and f['store']==e['controller_store'] and (p['publication']=='NOT_REQUIRED' or (p['publication']=='REQUIRED' and f['published']))
        elif suffix=='SCOPE':
            schema(f,dict(source_scope=str,target_scope=str,operation=str)); schema(p,dict(source_scope=str,target_scope=str,operation=str,permitted=bool))
            ok=p['permitted'] and all(f[k]==p[k]==e[k] for k in ('source_scope','target_scope','operation'))
        elif suffix=='LINEAGE':
            schema(f,dict(source_lineage='id',target_lineage='id',selected_release='id',superseded=bool)); schema(p,dict(selected_lineage='id',selected_release='id'))
            ok=f['source_lineage']==f['target_lineage']==p['selected_lineage']==e['lineage'] and f['selected_release']==p['selected_release']==e['release'] and not f['superseded']
        elif suffix=='RUNTIME':
            schema(f,dict(source_runtime='id',target_runtime='id',content_verified=bool,selection_current=bool)); schema(p,dict(selected_runtime='id'))
            ok=f['source_runtime']==f['target_runtime']==p['selected_runtime']==e['runtime'] and f['content_verified'] and f['selection_current']
        elif suffix=='CONTROLLER_STORE_G4':
            schema(f,dict(source_store='id',target_store='id',authority='id',membership=bool)); schema(p,dict(selected_store='id'))
            ok=f['source_store']==f['target_store']==p['selected_store']==e['controller_store'] and f['authority']==e['authority'] and f['membership']
        elif suffix=='PROGRAMMER_PROFILE':
            schema(f,dict(profile='id',identity_verified=bool,target_binding=bool,superseded=bool)); schema(p,dict(profile_check=str,profile='id'))
            ok=f['profile']==p['profile']==e['profile'] and (p['profile_check']=='NOT_APPLICABLE' or (p['profile_check']=='REQUIRED' and f['identity_verified'] and f['target_binding'] and not f['superseded']))
        elif suffix=='TEMPORAL_CURRENTNESS':
            schema(f,dict(authority='id',invocation='id',revoked=bool,superseded=bool,single_use_available=bool)); schema(p,dict(require_unrevoked=bool,require_unsuperseded=bool,require_single_use_available=bool))
            ok=f['authority']==e['authority'] and f['invocation']==e['invocation'] and all(p.values()) and not f['revoked'] and not f['superseded'] and f['single_use_available']
        else:
            schema(f,dict(source_phase=str,target_phase=str,operation=str)); schema(p,dict(source_phase=str,target_phase=str,operation=str,permitted=bool,effects_allowed=list))
            ok=f['source_phase']==p['source_phase']=='FIRST_PROGRAMMER_EXECUTION' and f['target_phase']==p['target_phase']=='FIRST_PROGRAMMER_REQUEST' and f['operation']==p['operation']==e['operation'] and p['permitted'] and p['effects_allowed']==[]
        require(ok,'unproved '+name)
    require(used==set(records),'unrelated/conflicting records')
    dependencies=list(used)+[parameters['parameters_sha256'],anchor['id']]+[e[k] for k in ENVELOPE[:9]]
    for invalid in submission['invalidated_ids']:
        if type(invalid) is dict: identity(invalid)
        else: require(type(invalid) is str and bool(invalid),'invalidation type')
        require(invalid not in dependencies,'required source invalidated')
    return records,rows,indices


def matrix_statement(p,s):
    return canonical({'type':'BUDGET_APPLICABILITY_PROOF_MATRIX_V1',
        'source_authentication_id':s['source_authentication_id'],
        'parameter_identity':{'kind':'CONTENT_IDENTITY','namespace':'budget-parameters-sha256','sha256':p['parameters_sha256']},
        'envelope':p['expected_envelope'],'anchor':p['anchor'],
        'rows':[dict(obligation=r['id'],fact_id=r['fact_id'],rule_id=r['rule_id'],
                     envelope=p['expected_envelope'],anchor=p['anchor']['id'],
                     generation=p['anchor']['generation'],proof_state='PROVED')
                for r in sorted(s['rows'],key=lambda r:r['id'])],
        'invalidated_ids':s['invalidated_ids']})


def validate_matrix(matrix):
    """Recheck persisted normalized contract, not a saved acceptance flag."""
    from . import codec as c
    p=c.parse_json(matrix.parameters); s=c.parse_json(matrix.submission)
    require(matrix.parameters==canonical(p) and matrix.submission==canonical(s),'noncanonical embedded contract')
    _,rows,_=validate_input(p,s)
    require(s['records']==sorted(s['records'],key=lambda r:r['id']) and s['rows']==sorted(s['rows'],key=lambda r:r['id']), 'noncanonical proof ordering')
    require(tuple(r.obligation.value for r in matrix.rows)==tuple(sorted(rows)),'typed row coverage/order')
    for r in matrix.rows:
        source=rows[r.obligation.value]
        require(r.fact.sha256==source['fact_id'] and r.rule.sha256==source['rule_id'],'typed row source mismatch')
        require(r.fact.kind is m.IdentityKind.CONTENT_IDENTITY and r.rule.kind is m.IdentityKind.CONTENT_IDENTITY and
                r.fact.namespace==r.rule.namespace=='raw-file-sha256','row identity domain')


def validate_restored(snapshot):
    """Completeness and bindings are mandatory at decode, before planner use."""
    from . import codec as c
    m.unique(snapshot.budget_matrices,lambda x:x.knowledge)
    assertions={a.id:a for a in snapshot.assertions}
    all_known={k.id:k for k in snapshot.knowledge}
    covered=set()
    for matrix in snapshot.budget_matrices:
        validate_matrix(matrix)
        p=c.parse_json(matrix.parameters); s=c.parse_json(matrix.submission)
        expected=m.BudgetEnvelope(**{k:(identity(v) if k in ENVELOPE[:9] else v) for k,v in p['expected_envelope'].items()})
        require(matrix.envelope==expected,'typed envelope mismatch')
        required={'budget-source:'+r['id']:r['body'] for r in s['records']}
        required.update({'budget-parameters':p,'budget-submission':s})
        require({a.value for a in matrix.evidence}==set(required) and len(matrix.evidence)==len(required),'dependency coverage')
        for name,value in required.items():
            a=assertions.get(m.AssertionId(name))
            require(a is not None,'missing dependency')
            require(a.provenance.identity==m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY,'raw-file-sha256',digest(value)) and
                    a.provenance.excerpt==canonical(value) and a.provenance.section=='/' and a.provenance.method=='BUDGET_ORACLE_1',
                    'dependency source substitution')
        known=all_known.get(matrix.knowledge);require(known is not None,'matrix knowledge absent')
        expected_statement=matrix_statement(p,s)
        require(matrix.identity==m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY,'budget-proof-matrix-sha256',hashlib.sha256(expected_statement.encode()).hexdigest()),'matrix identity mismatch')
        require(known.statement==expected_statement and known.provenance==matrix.provenance and
                matrix.provenance==assertions[m.AssertionId('budget-submission')].provenance and
                set(known.evidence)==set(matrix.evidence),'knowledge binding mismatch')
        action=next((a for a in snapshot.actions if a.id==matrix.consumer),None)
        require(action is not None,'consumer absent')
        require(any(pred.id in action.requirements and pred.kind is m.PredicateKind.KNOWLEDGE_ACCEPTED and
                    pred.knowledge==matrix.knowledge and pred.unavailable is None for pred in snapshot.predicates),'consumer lost matrix requirement')
        output=next((k for k in action.accepted_inventory if k.id==matrix.output),None)
        require(output is not None and output.statement==expected_statement and output.provenance==matrix.provenance and
                set(output.evidence)==set(matrix.evidence) and output.producer==matrix.consumer and output.outcome is m.ActionResult.PASS,'result contract lost')
        covered.update((matrix.knowledge,matrix.output))
    require(all(k.id in covered for k in snapshot.knowledge if k.provenance.method=='BUDGET_ORACLE_1'),'matrix metadata absent')


def import_budget(path, root, data):
    """Independent synthetic contract -> existing operational snapshot.

    This profile is partial qualification scope, never a frozen-E1 replacement.
    """
    from . import codec as c, replay
    fields(data,'schema parameters submission')
    p,s=data['parameters'],data['submission']; records,rows,indices=validate_input(p,s)
    s=dict(s, records=sorted(s['records'],key=lambda r:r['id']), rows=sorted(s['rows'],key=lambda r:r['id']), invalidated_ids=sorted(s['invalidated_ids'],key=canonical))
    root=Path(root).resolve()
    try: relative=str(Path(path).resolve().relative_to(root))
    except ValueError as exc: raise m.PlannerError('budget fixture outside source root') from exc
    pins=[]; assertions=[]
    def provenance(pointer,value):
        # Raw, immutable source members are provided by the fixture author. The
        # importer never materializes evidence files or repins a changed source.
        raw=canonical(value).encode()
        ident=m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY,'raw-file-sha256',hashlib.sha256(raw).hexdigest())
        member=str(Path(relative).parent/'budget.sources'/(ident.sha256+'.json'))
        pin=m.ArtifactPin(member,ident); c.load_pinned(root,pin); pins.append(pin)
        return m.Provenance(member,ident,'/',raw.decode(),'BUDGET_ORACLE_1','SYNTHETIC_QUALIFICATION_ONLY')
    source=provenance('/parameters',p)
    # Stable semantic IDs, never array positions; source pointers retain original locations.
    for ref in sorted(records):
        prov=provenance('/submission/records/'+str(indices[ref])+'/body',records[ref])
        assertions.append(m.GraphAssertion(m.AssertionId('budget-source:'+ref),prov))
    parameter_assertion=m.GraphAssertion(m.AssertionId('budget-parameters'),source)
    assertions.append(parameter_assertion)
    # The whole submission pin also covers envelope, references, and invalidation set.
    submitted=provenance('/submission',s)
    assertions.append(m.GraphAssertion(m.AssertionId('budget-submission'),submitted))
    dependencies=tuple(sorted((a.id for a in assertions),key=lambda a:a.value))
    typed_rows=tuple(m.BudgetProofRow(m.EvidenceId(name),
        m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY,'raw-file-sha256',rows[name]['fact_id']),
        m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY,'raw-file-sha256',rows[name]['rule_id'])) for name in sorted(rows))
    kid=m.KnowledgeId('budget-proof-matrix')
    matrix=m.BudgetProofMatrix(m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY,'budget-proof-matrix-sha256',hashlib.sha256(matrix_statement(p,s).encode()).hexdigest()),m.ActionId('FACT-BUDGET-APPLICABILITY'),m.KnowledgeId('budget-proof-result'),
        m.BudgetEnvelope(**{k:(identity(v) if k in ENVELOPE[:9] else v) for k,v in p['expected_envelope'].items()}),
        kid,canonical(p),canonical(s),typed_rows,submitted,dependencies)
    known=m.KnowledgeRecord(kid,m.KnowledgeState.KNOWN_COMPLETE,matrix_statement(p,s),submitted,dependencies)
    requirement=m.Predicate(m.PredicateId('budget-matrix'),m.PredicateKind.KNOWLEDGE_ACCEPTED,knowledge=kid)
    producer=m.ActionId('REEVAL-BUDGET'); fact=m.ActionId('FACT-BUDGET-APPLICABILITY')
    next_action=m.ActionId('QUALIFICATION-REEVAL-BUDGET')
    output=replace(known,id=m.KnowledgeId('budget-proof-result'),producer=fact,outcome=m.ActionResult.PASS)
    actions=(m.Action(producer,m.OperationClass.SOURCE_ACQUISITION,m.EffectClass.NON_EFFECTING,(),source,()),
        m.Action(fact,m.OperationClass.SOURCE_ACQUISITION,m.EffectClass.NON_EFFECTING,(),source,(output,),requirements=(requirement.id,)),
        m.Action(next_action,m.OperationClass.SOURCE_ACQUISITION,m.EffectClass.NON_EFFECTING,
                 (m.Gate(m.GateKind.ACTION_COMPLETED,fact),),source,(),requirements=(requirement.id,)))
    state=m.Snapshot(actions,(m.ActionStatus(producer,m.ActionState.BLOCKED),m.ActionStatus(fact,m.ActionState.ACTION_ELIGIBLE),
        m.ActionStatus(next_action,m.ActionState.ACTION_ELIGIBLE)),
        (m.RootCondition(m.ConditionId('root:budget'),m.ConditionState.UNRESOLVED),),
        (m.ValueSlot(m.SlotId('slot:authenticated_inputs.budget_policy'),m.SlotState.UNRESOLVED,m.IdentityKind.AUTHORITY_IDENTITY),),
        (known,),tuple(assertions),predicates=(requirement,),budget_matrices=(matrix,),
        goals=(m.Goal(m.ConditionId('root:budget'),(next_action,),source),
               m.Goal(m.SlotId('slot:authenticated_inputs.budget_policy'),(next_action,),source)))
    # Retain the independently pinned historical non-PASS prerequisite through C06's real importer.
    plan_path=root/'docs/experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_PLAN_1.json'
    plan_identity=m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY,'raw-file-sha256','2662971aa42bda300dcea7bf591e95c113b4ed5cb32db1381cd25b024c06e91c')
    plan_pin=m.ArtifactPin(str(plan_path.relative_to(root)),plan_identity)
    plan=c.parse_json(c.load_pinned(root,plan_pin)); row=next(a for a in plan['resolution_actions'] if a['id']==fact.value)
    req=row['knowledge_requirements'][0]; ep=req['evidence']
    pins.append(m.ArtifactPin(ep['path'],m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY,'raw-file-sha256',ep['sha256'])))
    producer_row=next(a for a in plan['resolution_actions'] if a['id']==producer.value)
    state=replay.restore_accepted_knowledge(state,{'resolution_actions':[producer_row,{'id':fact.value,'knowledge_requirements':[req]}, {'id':next_action.value}]},pins,root)
    # Pin the plan driving the projection as well as the actual result source.
    pins.append(plan_pin)
    definition=m.GraphAssertion(m.AssertionId('budget-action-contract'),m.Provenance(plan_pin.path,plan_identity,
        '/resolution_actions',canonical(row),'BUDGET_ACTION_CONTRACT_1','SYNTHETIC_QUALIFICATION_ONLY'))
    state=replace(state,assertions=state.assertions+(definition,),actions=tuple(
        replace(a,evidence=a.evidence+(definition.id,)) if a.id in (fact,next_action) else a for a in state.actions))
    policy_path='docs/experiments/E1/E1_GRAPH_RESOLUTION_SELECTION_POLICY_1.md'
    policy=m.ArtifactPin(policy_path,m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY,'raw-file-sha256','475bef0b28d7b484ba2641c654b37e9ce3d6f6ae1b0e13dfdcadaa3f79a2a3b5'))
    bundle=m.PersistenceBundle(state,(),state,tuple(pins),policy,'E1-SELECTION-1-P05','PARTIAL_SYNTHETIC_BUDGET_QUALIFICATION')
    c.bundle_bytes(bundle)
    return bundle,(),{}
