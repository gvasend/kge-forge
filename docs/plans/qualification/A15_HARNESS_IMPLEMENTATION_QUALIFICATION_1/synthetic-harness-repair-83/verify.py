"""Independent read-only AST qualification; never imports test/gate modules."""
import ast,hashlib,json,pathlib,sys
E=pathlib.Path(__file__).parent
TEST='adapter/tests/test_h77_02_launch_gate.py'
def read(p):return json.loads(pathlib.Path(p).read_text())
def cb(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def need(v,m):
    if not v:raise ValueError(m)
def verify(candidate=None):
    candidate=candidate or {}
    need(set(candidate)<= {'source','binding','oracle'},'UNAUTHORIZED_CONTROLLER_FILE')
    source=candidate.get('source',pathlib.Path(TEST).read_text())
    tree=ast.parse(source);compile(tree,TEST,'exec')
    funcs={n.name:n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef)}
    names=[n.name for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name.startswith('test_')]
    need(names==read(E/'preserved-test-names.json'),'TEST_SET_CHANGED')
    setup=ast.get_source_segment(source,funcs['setUp'])
    need('self.runtime.case_root' in setup and 'uuid' not in setup and 'mkdir' not in setup,'UNCONTROLLED_TEST_ROOT')
    need('UNASSIGNED_TEST_DIRECTORY' in source and 'SIBLING_TEST_ACCESS' in source and 'SYMLINK_OR_PATH_ESCAPE' in source,'ROOT_OWNERSHIP')
    need('WRONG_CAMPAIGN_ROOT' in source and "root['identity']['sha256'][:32]" in source,'WRONG_ROOT_IDENTITY')
    prepare=ast.get_source_segment(source,funcs['prepare_campaign_instance'])
    need("root.mkdir(mode=0o700, exist_ok=False)" in prepare and "entry['binding_phase'] != 'PREPARE'" in prepare,'ROOT_CREATION_RULE')
    need('_produce_fixture(path, descriptor)' in prepare and '_expected_fixture(path, descriptor)' in prepare and 'produced != expected' in prepare,'UNSEALED_GENERATED_FIXTURE')
    need('FIXTURE_ID_COLLISION' in prepare and 'PRODUCER_BYTES_MISMATCH' in prepare,'FIXTURE_BINDING')
    expected=ast.get_source_segment(source,funcs['_expected_fixture'])
    need('gate.' not in expected and 'issued_grant_identity' in expected and 'authorized_attempt_number' in expected,'INDEPENDENT_FIXTURE_PATH')
    observe=ast.get_source_segment(source,funcs['observed_claim'])
    need('callback.invoked' in observe and 'callback.returned' in observe and 'callback.exception' in observe,'MISSING_CALLBACK_WITNESS')
    need('fault.observed' in observe and 'first.append(detail)' in observe and "'first': first[0]" in observe,'MISSING_FAULT_WITNESS')
    fault_events=[n for n in ast.walk(funcs['observe_failure']) if isinstance(n,ast.Call)
                  and isinstance(n.func,ast.Attribute) and n.func.attr=='event'
                  and len(n.args)==4 and isinstance(n.args[2],ast.Constant)
                  and n.args[2].value=='fault.observed']
    need(len(fault_events)==1,'FAULT_EVENT_SHAPE')
    payload=fault_events[0].args[3]
    first_value=next(v for k,v in zip(payload.keys,payload.values) if isinstance(k,ast.Constant) and k.value=='first')
    need(isinstance(first_value,ast.Subscript) and isinstance(first_value.value,ast.Name)
         and first_value.value.id=='first','SECONDARY_REPLACES_FIRST')
    need("'secondary': _error(secondary)" in observe and 'raise' in observe,'SECONDARY_REPLACES_FIRST')
    compare=ast.get_source_segment(source,funcs['_compare_observations'])
    for marker in ['CALLBACK_COUNT_MISMATCH','DUPLICATE_CALLBACK','FIRST_COUNTEREXAMPLE_CONTENT',
                   'AUDIT_CONTENT','RECOVERY_REOPENS_AUTHORITY','EXACT_FILE_BARRIER_ORDER',
                   'UNSEALED_RUNTIME_INPUT','CRASH_EXIT_NOT_INDEPENDENTLY_OBSERVED']:
        need(marker in compare,'MISSING_ORACLE:'+marker)
    need("'launch_permitted'] is not False" in compare and "'retry_allowed'] is not False" in compare,'CRASH_REOPENS_PERMISSION')
    budget=ast.get_source_segment(source,funcs['account'])
    need("limits['MAX_ACTUAL_PROCESS_SLOTS']" in budget and "limits['MAX_PAYLOAD_LAUNCHES']" in budget,'UNBOUNDED_CONCURRENCY')
    need("event['charged_bytes']" in budget and 'CAMPAIGN_OUTPUT_LIMIT' in budget,'OUTPUT_ACCOUNTING')
    runner=ast.get_source_segment(source,funcs['run_bound_controller'])
    need('failfast=True' in runner and "len(names) != 18" in runner and 'stop_after_unexpected_failure' in runner,'AUTOMATIC_RETRY_OR_SELECTION')
    need('Popen(' not in source and 'adapter.planner' not in source,'REAL_EXECUTION_IN_HARNESS')
    need('os.system(' not in source and 'subprocess.run(' not in source,'UNRESTRICTED_PROCESS')
    base=read(E/'preservation-before.json')
    for f in ['adapter/qualification_h77_02_gate/__init__.py','adapter/qualification_h77_02_gate/gate.py']:
        need(hashlib.sha256(pathlib.Path(f).read_bytes()).hexdigest()==base[f],'GATE_CONSUMPTION_CHANGED')
    gate=ast.parse(pathlib.Path('adapter/qualification_h77_02_gate/gate.py').read_text())
    disabled=next(n.value for n in gate.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='QUALIFIED_REAL_AUTHORITY_BINDING' for t in n.targets))
    need(isinstance(disabled,ast.Constant) and disabled.value is None,'REAL_BINDING_ENABLED')
    binding=candidate.get('binding',read(E/'fixture-manifest-binding-specification.json'))
    b=dict(binding);i=b.pop('identity');need(i['sha256']==hashlib.sha256(cb(b)).hexdigest(),'FIXTURE_MANIFEST_IDENTITY')
    need(binding['test_names']==names and binding['synthetic_namespace_prefix']=='qualification-h77-02-gate-synthetic-','REAL_OR_UNBOUND_FIXTURE')
    oracle=candidate.get('oracle',read(E/'independent-executable-oracle-specification.json'))
    need(set(oracle['tests'])==set(names) and oracle['gate_output_used'] is False,'ORACLE_COVERAGE_OR_OUTPUT_DERIVATION')
    need(oracle['status']=='PARTIAL','INCOMPLETE_ORACLE_PROMOTED')
    return {'RESULT':'PASS_STATIC_REPAIR_WITH_EXPLICIT_CLOSURE_GAPS','SOURCE_SHA256':hashlib.sha256(source.encode()).hexdigest(),
            'SOURCE_AST_IDENTITY':hashlib.sha256(ast.dump(tree,include_attributes=False).encode()).hexdigest(),
            'PRESERVED_TESTS':names,'GATE_SOURCE_UNCHANGED':True,'BINDING_SPEC_IDENTITY':binding['identity'],
            'ORACLE_SPEC_IDENTITY':oracle['identity'],'INDEPENDENT_EXECUTABLE_ORACLES_COMPLETE':False,
            'ACTIVE_SYNTHETIC_TEST_READY':False,'TESTS_EXECUTED':0}
if __name__=='__main__':print(json.dumps(verify(json.load(sys.stdin) if '--candidate' in sys.argv else None),sort_keys=True))
