"""Independent static Package82 reconstruction; never imports gate/tests."""
import ast,hashlib,json,pathlib,sys
E=pathlib.Path(__file__).parent;P81=E.parent/'single-use-gate-implementation-qualification-1'
def cb(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def read(p):return json.loads(pathlib.Path(p).read_text())
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def need(x,m):
    if not x:raise ValueError(m)
def verify(overrides=None):
    overrides=overrides or {}
    def get(n):return overrides[n] if n in overrides else read(E/n)
    idx=read(P81/'evidence-index.json')
    for p,h in idx['FILES'].items():need(sha(p)==h,'PACKAGE81_CHANGED')
    sources=idx['SOURCE_FILES'];need(len(sources)==3,'SOURCE_ALLOWLIST')
    tree=ast.parse(pathlib.Path('adapter/tests/test_h77_02_launch_gate.py').read_text())
    funcs={n.name:n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef)}
    methods=[n for n in funcs if n.startswith('test_')];need(len(methods)==18,'TEST_COUNT')
    inventory=get('eighteen-test-inventory.json')
    need(inventory['COUNT']==18 and {r['METHOD'] for r in inventory['TESTS']}==set(methods),'TEST_INVENTORY')
    need(inventory['ACTUAL_PURE_INVOCATIONS']==0,'PURE_TEST_SCOPE')
    for row in inventory['TESTS']:
        n=funcs[row['METHOD']];need(row['SOURCE_LOCATION']['LINE']==n.lineno,'SOURCE_POINTER')
        need('FILESYSTEM_SYNTHETIC' in row['PHASES'] and row['CURRENT_READINESS']=='NOT_READY','PHASE_EFFECTS')
    src=pathlib.Path('adapter/tests/test_h77_02_launch_gate.py').read_text()
    setup=ast.get_source_segment(src,funcs['setUp'])
    need("pathlib.Path('/tmp')" in setup and 'uuid.uuid4().hex' in setup and 'make_fixture(self.root)' in setup,'ROOT_CONFLICT_EVIDENCE')
    fixture=ast.get_source_segment(src,funcs['make_fixture'])
    need('store.stat()' in fixture and 'store_inode' in fixture and 'INERT_CALLBACK' in fixture,'FIXTURE_INPUT_RULES')
    need('fixture_manifest_pin' not in fixture,'UNBOUND_GENERATED_FIXTURE')
    oracle=get('independent-synthetic-oracle-specification.json')
    need(oracle['COUNT']==18 and not oracle['INDEPENDENT_ORACLES_COMPLETE'] and oracle['NO_GATE_OUTPUT_USED'] is True,'ORACLE_COMPLETENESS')
    positive={'test_first_and_duplicate_claim','test_concurrent_claimants_at_most_one','test_process_restart_preserves_claim','test_post_consumption_failure_unknown_and_no_retry','test_no_real_launcher_reachable_in_synthetic_mode'}
    for row in oracle['ORACLES']:
        method=next(i['METHOD'] for i in inventory['TESTS'] if i['TEST_ID']==row['TEST_ID'])
        count=row['EXPECTED_LAUNCH_COUNT']['VALUE']
        if method=='test_controlled_crash_points_remain_blocked':
            need(count=={'DURING_CLAIM':0,'AFTER_FILE_FSYNC':0,'AFTER_DIRECTORY_FSYNC':0,'AFTER_CLAIM_BEFORE_LAUNCH':0,'DURING_LAUNCH':0,'AFTER_LAUNCH_BEFORE_OBSERVATION':1,'AFTER_COMPLETION_BEFORE_AUDIT':1},'CRASH_ORACLE')
        else:need(count==(1 if method in positive else 0),'CALLBACK_ORACLE')
        need(row['EXPECTED_RETRY_COUNT']==0 and row['COMPLETENESS']=='PARTIAL_BOUND_INPUT_AND_OBSERVATION','ORACLE_UNKNOWN_PRESERVED')
        body=dict(row);ident=body.pop('SPECIFICATION_IDENTITY')
        need(ident['sha256']==hashlib.sha256(cb(body)).hexdigest(),'ORACLE_SPEC_IDENTITY')
    invocation=get('test-invocation-specification.json')
    expected=['adapter.tests.test_h77_02_launch_gate.GateSyntheticTests.'+n for n in methods]
    need(set(invocation['TEST_DISCOVERY_SCOPE'])==set(expected) and len(invocation['CANDIDATE_ARGV'])==22,'TEST_DISCOVERY_SCOPE')
    need(invocation['CANDIDATE_ARGV'][:4]==['/usr/bin/python3','-m','unittest','-v'] and set(invocation['CANDIDATE_ARGV'][4:])==set(expected),'UNRESTRICTED_DISCOVERY')
    need(invocation['SOURCE_PINS']==sources and not invocation['TEST_INVOCATION_SEALED'],'EXECUTABLE_PINS')
    actual=invocation['OBSERVED_CURRENT_INTERPRETER'];need(sha(actual['RESOLVED_PATH'])==actual['RAW_SHA256'],'INTERPRETER_OBSERVATION')
    template=get('synthetic-fixture-template.json')
    need(template['CONTENT']['NO_REAL_GRANT_INPUT'] and template['CONTENT']['ACTUAL_FIXTURE_IDENTITIES'] is None and not template['EXECUTABLE_FIXTURE'],'REAL_FIXTURE_OR_UNBOUND_IDENTITY')
    controller=get('test-controller-assessment.json');need(not controller['TEST_CONTROLLER_QUALIFIED'] and not controller['EXISTING_CONTROLLER_QUALIFIED'],'CONTROLLER_NOT_QUALIFIED')
    resource=get('resource-enforcement-matrix.json')
    grant=read(resource['LIMIT_SOURCE_PIN']['PATH']);need(sha(resource['LIMIT_SOURCE_PIN']['PATH'])==resource['LIMIT_SOURCE_PIN']['RAW_SHA256'],'GRANT_PIN')
    need(hashlib.sha256(cb(grant['RECORD'])).hexdigest()==grant['GRANT_IDENTITY']['sha256'],'ISSUED_GRANT_ID')
    limits=grant['RECORD']['RESOURCE_LIMITS'];need(resource['ACTUAL_APPROVED_LIMITS']==limits,'WRONG_LIMITS')
    need({r['CONTROL_ID']:r['LIMIT'] for r in resource['CONTROLS']}==limits,'MISSING_LIMIT')
    need(all(r['STATUS']=='PROPOSED_LIMIT_NOT_QUALIFIED_ENFORCEMENT' for r in resource['CONTROLS']) and not resource['RESOURCE_ENFORCEMENT_VERIFIED'],'UNSUPPORTED_ENFORCEMENT')
    controls={r['CONTROL_ID']:r for r in resource['CONTROLS']}
    need('deadline' in controls['CHILD_WALL']['ENFORCEMENT_MECHANISM'] and 'deadline600' in controls['TOTAL_WALL']['ENFORCEMENT_MECHANISM'],'MISSING_TIMEOUT')
    fs=get('filesystem-isolation-specification.json');need(not fs['FILESYSTEM_ISOLATION_VERIFIED'] and fs['ROOTS_CREATED_IN_PACKAGE82']==0 and 'one' in fs['REQUIRED'].lower(),'MISSING_FS_BOUNDARY')
    profile=get('direct-host-profile.json');need(not profile['ENVIRONMENT_PROFILE_SEALED'] and not profile['OBSERVATIONS_INDEPENDENTLY_REPRODUCED'],'UNSEALED_HOST')
    campaign=get('fresh-campaign-specification.json');c=campaign['CONTENT']
    need(c['EFFECTIVE_PACKAGE80_GRANT']==grant['GRANT_IDENTITY'] and c['SOURCE_PINS']==sources and c['RESOURCE_LIMITS']==limits,'CAMPAIGN_BINDINGS')
    need(c['HISTORICAL_EXCLUSIONS']==grant['RECORD']['HISTORICAL_EXCLUSIONS'],'HISTORICAL_OR_A15_SCOPE_EXPANSION')
    need(c['ISSUED_CAMPAIGN_IDENTITY'] is None and c['AUTHORIZATION_SELECTION'] is None and not c['STOPPED_CAMPAIGN_REUSED'] and c['NO_RETRY_POLICY']==0,'CAMPAIGN_AUTHORITY_EXPANSION')
    need(not c['DECISION_READY'] and not c['CAMPAIGN_AUTHORITY_APPLICABLE'] and not campaign['EXECUTION_READY'],'INCOMPLETE_CAMPAIGN_READY')
    need(campaign['SPECIFICATION_IDENTITY']['sha256']==hashlib.sha256(cb(c)).hexdigest(),'CAMPAIGN_SPEC_ID')
    for p in [c['FIXTURE_TEMPLATE_PIN'],c['ORACLE_SPEC_PIN']]:need(sha(p['PATH'])==p['RAW_SHA256'],'CAMPAIGN_INPUT_PIN')
    authority=get('proposed-controller-authority-scope.json');need(authority['OPTIONAL_SCOPE_CANDIDATE'] and authority['NOT_PROVEN_REQUIRED'] is True and not authority['DECISION_READY'],'AUTHORITY_MINIMALITY')
    gate=ast.parse(pathlib.Path('adapter/qualification_h77_02_gate/gate.py').read_text())
    constant=next(n.value for n in gate.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='QUALIFIED_REAL_AUTHORITY_BINDING' for t in n.targets))
    need(isinstance(constant,ast.Constant) and constant.value is None,'REAL_AUTHORITY_ACTIVATION')
    need(not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='Popen' for n in ast.walk(tree)),'REAL_COMMAND_IN_TESTS')
    need('adapter.planner' not in src,'A15_EXECUTION')
    gates=get('readiness-gates.json')
    need(gates['TEST_INVENTORY_COMPLETE']=='YES' and all(gates[x]=='NO' for x in ['INDEPENDENT_ORACLES_COMPLETE','TEST_INVOCATION_SEALED','TEST_CONTROLLER_QUALIFIED','ENVIRONMENT_PROFILE_SEALED','RESOURCE_ENFORCEMENT_VERIFIED','FILESYSTEM_ISOLATION_VERIFIED','CAMPAIGN_AUTHORITY_APPLICABLE','SYNTHETIC_TEST_DECISION_READY','SYNTHETIC_TEST_EXECUTION_READY']),'READINESS_FALSE_PROMOTION')
    return {'RESULT':'PASS_STATIC_PARTIAL_READINESS_RECONSTRUCTION','TEST_COUNT':18,'SOURCE_IDENTITIES':sources,'PROPOSED_TEST_SET_IDENTITY':hashlib.sha256(cb(sorted(expected))).hexdigest(),'ORACLE_SPEC_IDENTITIES':sorted(r['SPECIFICATION_IDENTITY']['sha256'] for r in oracle['ORACLES']),'RESOURCE_LIMITS':limits,'CAMPAIGN_SPEC_IDENTITY':campaign['SPECIFICATION_IDENTITY'],'SOURCE_ROOT_CONFLICT_CONFIRMED':True,'GENERATION_TO_MANIFEST_UNBOUND':True,'REAL_AUTHORITY_BINDING':'DISABLED','SYNTHETIC_TEST_DECISION_READY':False,'SYNTHETIC_TEST_EXECUTION_READY':False,'GATE_OR_TEST_EXECUTION':0}
if __name__=='__main__':print(json.dumps(verify(json.load(sys.stdin) if '--candidate' in sys.argv else None),sort_keys=True))
