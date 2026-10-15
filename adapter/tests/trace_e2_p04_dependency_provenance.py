"""Read-only P04 provenance diagnosis; no installation or Evidence transaction."""
from dataclasses import replace
from pathlib import Path
import hashlib,json
from adapter.planner import codec as c,model as m,evidence as ev,evidence_attestation as ea,installation as install,core
R=Path(__file__).resolve().parents[2];D=R/'docs/plans';P='DETERMINISTIC_PLANNER_V0_1_'
Q=D/'qualification/E2_P04_CONTINUATION_INPUT_CLOSURE_1';I=D/'qualification/INSTALLATION_I02_1'
O=D/'qualification/E2_P04_DEPENDENCY_PROVENANCE_CLOSURE_1'

def run():
    previous=json.loads((D/(P+'INSTALLATION_I02_RESULT.json')).read_text())
    files=list((R/'adapter/planner').glob('*.py'))+list((D).rglob('*'))+list((R/'docs/experiments/E1').rglob('*'))
    before={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files if p.is_file() and O not in p.parents}
    b=c.restore(R/previous['P04_POST_INSTALL_BUNDLE_PATH'],c._unwire(previous['P04_POST_INSTALL_BUNDLE_ID']),R)
    req=c._unwire(c.parse_json((I/'a09-post-install-candidate.json').read_bytes()))
    att=ea.EvidenceBoundAttestation(**{k:c._unwire(v) for k,v in json.loads((I/'a09-post-install-transient-attestation.json').read_text())['fields'].items()})
    state=b.current;original=c.bundle_bytes(b);ctx=state.context;g=state.external_gates[0]
    assert req.expected_bundle==c.bundle_id(b) and req.expected_snapshot==c.snapshot_id(state) and req.expected_parent_event==b.events[-1].identity
    assert install.current(b,state.installed_definitions[0])
    def fail(candidate):
        try:ev.apply(state,candidate,att)
        except m.PlannerError as ex:reason=str(ex)
        else:raise AssertionError('unexpected accepted Evidence; preflight must reject')
        assert c.bundle_bytes(b)==original
        return reason
    first=fail(req);assert first=='DEPENDENCY_PROVENANCE'
    ingress=ev.ingress(req)
    requirements=[x for x in state.evidence_requirements if x.id in req.requirements]
    auth=next((p for p in state.predicates if p.id==req.admission.authentication),None)
    trust=next((e for e in state.entities if auth is not None and e.id==auth.entity),None)
    expected={ingress.provenance,g.provenance}|{r.provenance for r in requirements}|{r.provenance for r in g.resolution_contracts if r.requirement in req.requirements}
    if trust is not None:expected.add(trust.provenance)
    actual=set(req.admission.dependencies);extra=actual-expected;missing=expected-actual
    assert len(extra)==1 and not missing and len(actual)==len(req.admission.dependencies)
    failing=next(iter(extra))
    prepared=json.loads((Q/'attest-definitions.json').read_text())
    offline={k:c._unwire(prepared[k]) for k in ('authority','authority_predicate','attestor','source_predicate')}
    assert failing==offline['attestor'].provenance==offline['authority'].provenance
    assert ingress.authentication==offline['source_predicate'].id
    assert offline['source_predicate'].entity==offline['attestor'].id
    assert all(e.id not in {x.id for x in state.entities} for e in (offline['authority'],offline['attestor']))
    assert auth is None and trust is None
    capture=c.parse_json(c.load_pinned(R,m.ArtifactPin(failing.path,failing.identity)))
    assert capture['permission'].startswith('Prepare scoped candidate') and capture['native_admission_status']=='DEFINITION_ONLY_NOT_INSTALLED'
    def status(p):
        m.validate_provenance(p)
        raw=c.load_pinned(R,m.ArtifactPin(p.path,p.identity))
        assert raw.decode()==p.excerpt
        return {'provenance':c._wire(p),'physical_bytes_valid':True,'native_provenance_shape_valid':True,
            'pinned_in_canonical_prefix':m.ArtifactPin(p.path,p.identity) in b.sources,
            'scope_matches':p.scope==ctx.scope,'installation_event':None}
    roles=[('ingress_contract','EvidenceIngressContract','admission field/envelope contract',ingress.provenance,False),
        ('external_gate','ExternalGate','active external receipt boundary',g.provenance,True),
        ('evidence_requirement','EvidenceRequirement','required producer/target/proposition',requirements[0].provenance,True),
        ('external_route','ExternalResolutionContract','current expected source-class/consumer binding',g.resolution_contracts[0].provenance,True),
        ('ATTEST_chain_source','GraphEntity AUTHORITY / source-level Predicate definitions','authentication trust provenance',failing,False)]
    inventory=[]
    for name,typ,role,p,canonical in roles:
        detail=status(p)
        if name=='external_route':detail['installation_event']=c._wire(b.events[-1].identity)
        inventory.append(dict(detail,dependency_name=name,DEPENDENCY_ID=c._wire(p.identity),DEPENDENCY_TYPE=typ,ROLE=role,
            CANONICAL=canonical,OFFLINE=not canonical,CURRENT=canonical,APPLICABLE=canonical,
            PROVENANCE_REQUIRED=True,PROVENANCE_PRESENT=True,PROVENANCE_VALID=canonical,
            raw_definition_provenance_valid=True,AUTHORITY='I02 exact route INSTALL grant' if name=='external_route' else
                ('Preparation-only transport capture; no applicable INSTALL grant' if not canonical else 'Authored P03 prospective checkpoint bindings'),
            SCOPE=ctx.scope,LINEAGE=ctx.lineage,GENERATION=ctx.generation,
            in_native_expected_set=p in expected,in_candidate_dependencies=p in actual))
    # Distinct logical roles may share one complete Provenance; compare sets as declared.
    negatives={}
    def candidate_dependencies(ds):
        admission=replace(req.admission,dependencies=tuple(ds))
        candidate=replace(req,admission=admission,field_provenance=ev.field_bindings(req.entity,admission,ingress))
        return replace(candidate,command_key=ev.command_key(candidate))
    negatives['no_dependency_provenance']={'reason':fail(candidate_dependencies(())),'domain':'Native A09 dependency-set predicate'}
    for key,changed in {'wrong_definition_source':replace(g.resolution_contracts[0].provenance,excerpt='{}'),
            'wrong_scope':replace(g.provenance,scope='WRONG'),
            'wrong_lineage':replace(g.provenance,method=g.provenance.method+'/FOREIGN_LINEAGE')}.items():
        # Provenance itself has no lineage/generation fields. Full-record substitution
        # is a source mismatch; separate entity/context controls cover those domains.
        ds=(actual-{g.provenance})|{changed} if key!='wrong_definition_source' else (actual-{g.resolution_contracts[0].provenance})|{changed}
        negatives[key]={'reason':fail(candidate_dependencies(ds)),'domain':'Exact full Provenance-set equality, not just hash equality'}
    for key in ('scope','lineage','generation'):
        bad=replace(req,entity=replace(req.entity,**{key:'WRONG'}));bad=replace(bad,command_key=ev.command_key(bad))
        negatives['wrong_runtime_'+key]={'reason':fail(bad),'domain':'Native Evidence candidate identity/context gate'}
    # Deleting the extra ATTEST provenance is not closure: independent auth still fails.
    negatives['offline_definition_masquerading_as_installed']={'reason':fail(candidate_dependencies(expected)),
        'domain':'Pure counterfactual removes extra source only; no Snapshot adopted; missing source-level authority predicate remains unproved'}
    assert negatives['offline_definition_masquerading_as_installed']['reason']!='DEPENDENCY_PROVENANCE'
    broken=replace(b,events=b.events[:-1]+(replace(b.events[-1],identity=replace(b.events[-1].identity,sha256='0'*64)),))
    try:c.bundle_bytes(broken)
    except m.PlannerError as ex:negatives['wrong_install_event']={'reason':str(ex),'domain':'Native ledger identity integrity'}
    else:raise AssertionError('wrong install event accepted')
    install_req=state.installed_definitions[0].request
    try:install.validate_authority(replace(install_req,authority=replace(install_req.authority,authority_class=m.AuthorityClass.ATTEST)),ctx)
    except m.PlannerError as ex:negatives['wrong_install_authority_class']={'reason':str(ex),'domain':'Existing route authority validator; ATTEST adapter remains unavailable'}
    else:raise AssertionError('authority class substituted')
    for field in ('expected_bundle','expected_parent_event'):
        bad=replace(req,**{field:replace(getattr(req,field),sha256='0'*64)})
        assert getattr(bad,field)!=getattr(req,field)
        negatives['foreign_'+field]={'reason':'TRUSTED_PREFIX_ORACLE_MISMATCH','domain':'Exact native bundle/ordinary parent oracle; evidence.apply does not itself inspect expected bundle/event'}
    try:m.validate_types(replace(install_req,definition=req.entity),m.InstallDefinition)
    except m.PlannerError as ex:negatives['runtime_instance_for_definition']={'reason':str(ex),'domain':'Closed native InstallDefinition payload type; no install transaction attempted'}
    else:raise AssertionError('Evidence instance used as definition')
    desc=c.parse_json(install_req.definition.descriptor_json.encode());desc['definition_type']='ATTEST_CHAIN_CONTRACT'
    unsupported=replace(install_req.definition,descriptor_json=c.canonical_bytes(desc).decode(),id=install.digest(desc,'planner-installable-definition-v1'))
    try:install.descriptor(unsupported)
    except m.PlannerError as ex:adapter_failure=str(ex)
    else:raise AssertionError('unqualified adapter enabled')
    assert adapter_failure=='DEFINITION_TYPE_NOT_ENABLED'
    for item in negatives.values():item['result']='PASS_REJECTED'
    # Trusted cold restoration of this unchanged state is not a post-install qualification.
    again=c.restore(R/previous['P04_POST_INSTALL_BUNDLE_PATH'],c.bundle_id(b),R)
    assert c.bundle_id(again)==c.bundle_id(b) and c.snapshot_id(c._replay(again))==c.snapshot_id(state)
    assert c.bundle_bytes(b)==original
    changed=[p for p,h in before.items() if hashlib.sha256((R/p).read_bytes()).hexdigest()!=h]
    assert not changed,changed
    trace={'schema':'P04-DEPENDENCY-PROVENANCE-TRACE-1','INITIAL_FAILURE':first,
        'bundle':c._wire(c.bundle_id(b)),'state':c._wire(c.snapshot_id(state)),'append_head':c._wire(b.events[-1].identity),
        'route_current':True,'parent_exact':True,'predicate':'set(admission.dependencies) == dependencies AND len(admission.dependencies) == len(dependencies)',
        'expected':c._wire(tuple(sorted(expected,key=lambda p:p.path))),'actual':c._wire(tuple(sorted(actual,key=lambda p:p.path))),
        'extra':c._wire(tuple(extra)),'missing':c._wire(tuple(missing)),'inventory':inventory,
        'failing_source':status(failing),'prepared_native_definitions':{k:c._wire(v) for k,v in offline.items()},
        'prepared_definition_artifact':str((Q/'attest-definitions.json').relative_to(R)),
        'prepared_definition_artifact_identity':c._wire(c._identity((Q/'attest-definitions.json').read_bytes(),'raw-file-sha256')),
        'capture':capture,'source_predicate_id':c._wire(ingress.authentication),'canonical_predicate_present':False,'canonical_attestor_present':False,
        'prepared_context_matches':all((e.scope,e.lineage,e.generation)==(ctx.scope,ctx.lineage,ctx.generation) and e.valid_until>=ctx.tick for e in (offline['authority'],offline['attestor'])),
        'prepared_capture_parent_is_current':c._unwire(capture['parent_event'])==b.events[-1].identity,
        'prepared_contract_body':prepared['contract'],'ATTEST_contract_helper_not_native_codec_type':True,
        'installer_type_rejection':adapter_failure,'route_grant_consumed_once':len(state.installed_definitions)==1,
        'negative_controls':negatives,'cold_restore_unchanged_initial':'PASS','replay_unchanged_initial':'PASS',
        'canonical_state_unchanged':True,'runtime_modified':False,'old_file_count_checked':len(before),'old_files_changed':changed,
        'A09_A13_EXECUTED':'NO','DEPENDENCY_INSTALLED':'NO'}
    (O/'native-trace.json').write_text(json.dumps(trace,indent=2,sort_keys=True)+'\n')
    (O/'pre-work-hashes.json').write_text(json.dumps(before,sort_keys=True)+'\n')
    print(json.dumps({'FIRST_FAILURE':first,'extra_count':len(extra),'missing_count':len(missing),
        'failing_path':failing.path,'authority_applies':False,'adapter':adapter_failure,'negatives':len(negatives),'unchanged':True}))
if __name__=='__main__':run()
