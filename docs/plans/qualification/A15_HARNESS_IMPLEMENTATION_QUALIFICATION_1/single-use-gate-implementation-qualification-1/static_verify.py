"""Independent Package81 AST/source reconstruction; never imports gate/test code."""
import ast,hashlib,json,pathlib,sys
E=pathlib.Path(__file__).parent
FILES=['adapter/qualification_h77_02_gate/__init__.py','adapter/qualification_h77_02_gate/gate.py','adapter/tests/test_h77_02_launch_gate.py']
def read(p):return json.loads(pathlib.Path(p).read_text())
def cb(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def require(ok,why):
    if not ok:raise ValueError(why)
def calls(node):
    return [n for n in ast.walk(node) if isinstance(n,ast.Call)]
def named(node,name):
    return [n for n in calls(node) if isinstance(n.func,ast.Name) and n.func.id==name]
def attr(node,name):
    return [n for n in calls(node) if isinstance(n.func,ast.Attribute) and n.func.attr==name]
def verify(overrides=None):
    overrides=overrides or {}
    sources={p:overrides.get(p,pathlib.Path(p).read_text()) for p in FILES}
    require(set(overrides)<=set(FILES),'UNAUTHORIZED_SOURCE_PATH')
    trees={p:ast.parse(s,filename=p) for p,s in sources.items()}
    for p,t in trees.items():compile(t,p,'exec') # Compilation only, never exec/import.
    gate=trees[FILES[1]];test=trees[FILES[2]];funcs={n.name:n for n in gate.body if isinstance(n,ast.FunctionDef)}
    constants={}
    for n in gate.body:
        if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name):
            try:constants[n.targets[0].id]=ast.literal_eval(n.value)
            except (ValueError,TypeError):pass
    spec=read(E.parent/'single-use-gate-79/consumption-key-specification.json')
    require(constants['SUBJECT_SHA']==spec['APPROVED_SUBJECT_IDENTITY']['sha256'],'WRONG_SUBJECT')
    require(constants['EXACT_COMMAND_SHA']==spec['COMMAND_IDENTITY']['sha256'],'WRONG_COMMAND')
    require(constants['QUALIFIED_REAL_AUTHORITY_BINDING'] is None,'REAL_BINDING_NOT_QUALIFIED')
    require(constants['REAL_LIMITS']=={'MAX_ACTUAL_PROCESS_SLOTS':4,'MAX_PAYLOAD_LAUNCHES':1,'CHILD_WALL':60,'CHILD_CPU':30,'CHILD_AS':1073741824,'CHILD_FSIZE':16777216,'CHILD_FDS':64,'TOTAL_WRITES':1048576,'TOTAL_WALL':600,'RETRIES':0},'RESOURCE_LIMITS')
    key=funcs['consumption_key'];fields=next(n.value for n in ast.walk(key) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='fields' for t in n.targets))
    require({ast.literal_eval(k) for k in fields.keys}=={'schema','issued_grant_identity','approved_subject_identity','probe_identity','command_identity','execution_context','authorized_attempt_number'},'UNSTABLE_KEY')
    require(not attr(key,'getpid') and not attr(key,'time') and not attr(key,'uuid4'),'UNSTABLE_KEY_INPUT')
    reserve=funcs['_exclusive_record'];code=ast.get_source_segment(sources[FILES[1]],reserve)
    require('os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW' in code,'NON_ATOMIC_OR_DUPLICATE_CLAIM')
    require('FileExistsError' not in code and not named(reserve,'recover'),'DUPLICATE_ACCEPTED')
    require('os.fsync(fd)' in code,'MISSING_FILE_FSYNC')
    require('os.fsync(directory)' in code,'MISSING_DIRECTORY_FSYNC')
    require(not attr(gate,'unlink') and not attr(gate,'remove') and not attr(gate,'rmdir'),'CONSUMPTION_RESET')
    for node in ast.walk(gate):
        if isinstance(node,ast.Dict):
            for k,v in zip(node.keys,node.values):
                if isinstance(k,ast.Constant) and k.value in ('retry_allowed','launch_permitted'):
                    require(isinstance(v,ast.Constant) and v.value is False,'RETRY_PERMISSION_REOPENED')
    claim=funcs['claim_and_launch'];confirm=funcs['verify_consumption_record'];recover=funcs['recover']
    writer=named(claim,'_exclusive_record')[0].lineno
    barrier=named(claim,'verify_consumption_record')[0].lineno
    launch=named(claim,'_fixed_real_launch')[0].lineno
    callback=named(claim,'synthetic_callback')[0].lineno
    require(writer<barrier<min(launch,callback),'LAUNCH_BEFORE_DURABLE_CONFIRMATION')
    require('fsync' not in ast.get_source_segment(sources[FILES[1]],confirm) and named(confirm,'read_at'),'INDEPENDENT_REREAD')
    claimcode=ast.get_source_segment(sources[FILES[1]],claim)
    require('fcntl.LOCK_EX | fcntl.LOCK_NB' in claimcode and 'claimed = True' in claimcode,'CONCURRENCY_LOCK')
    require('fresh == raw' in claimcode and 'info.st_ino == os.fstat(epochfd).st_ino' in claimcode,'EPOCH_REPLACEMENT')
    require('entry = decode(canonical(entry))' in claimcode,'MUTABLE_CALLER_BINDING')
    recovercode=ast.get_source_segment(sources[FILES[1]],recover)
    require("'launch_permitted': False" in recovercode and "'retry_allowed': False" in recovercode and not named(recover,'claim_and_launch') and not attr(recover,'Popen'),'CRASH_REOPENS_AUTHORITY')
    authority=ast.get_source_segment(sources[FILES[1]],funcs['validate_authority'])
    require("identity(grant['content'], grant['identity']['namespace']) == grant['identity']" in authority,'WRONG_GRANT_ACCEPTED')
    require("epoch['status'] == 'EFFECTIVE'" in authority and "effective['effective'] is True" in authority,'REVOKED_OR_INEFFECTIVE')
    require("'REAL_INPUT_IN_SYNTHETIC_MODE'" in authority and "{'operation': 'INERT_CALLBACK', 'argv': []}" in authority,'REAL_SYNTHETIC_INVOCATION')
    popens=attr(gate,'Popen');require(len(popens)==1,'UNRESTRICTED_SUBPROCESS_INTERFACE')
    fixed=funcs['_fixed_real_launch'];require(popens[0] in list(ast.walk(fixed)),'UNRESTRICTED_LAUNCH_SITE')
    fixedcode=ast.get_source_segment(sources[FILES[1]],fixed)
    require('QUALIFIED_REAL_AUTHORITY_BINDING is not None' in fixedcode and '== EXACT_COMMAND_SHA' in fixedcode and "command['ARGV']" in fixedcode and not attr(fixed,'run'),'FIXED_COMMAND_GUARD')
    require(not any(isinstance(n,ast.keyword) and n.arg=='shell' and isinstance(n.value,ast.Constant) and n.value.value is True for n in ast.walk(gate)),'SHELL_EXPANSION')
    require(not any(isinstance(n,ast.Name) and n.id in ['eval','exec'] for n in ast.walk(gate)),'DYNAMIC_EXECUTION')
    testfunctions={n.name:n for n in ast.walk(test) if isinstance(n,ast.FunctionDef)}
    expected=['test_first_and_duplicate_claim','test_key_is_independently_reconstructed_and_stable','test_concurrent_claimants_at_most_one','test_process_restart_preserves_claim','test_controlled_crash_points_remain_blocked','test_before_claim_failure_does_not_launch','test_invalid_grant_pin','test_wrong_command','test_revoked_epoch','test_resource_mismatch','test_partial_and_conflicting_records','test_file_fsync_failure_blocks_launch','test_directory_fsync_failure_blocks_launch','test_independent_reread_failure_blocks_launch','test_post_consumption_failure_unknown_and_no_retry','test_missing_permissions_and_wrong_subject','test_symlink_store_rejected','test_no_real_launcher_reachable_in_synthetic_mode']
    require(set(expected)<set(testfunctions),'SYNTHETIC_COVERAGE')
    require('require_test_entry()' in ast.get_source_segment(sources[FILES[2]],testfunctions['setUpClass']),'ACTIVE_TEST_GUARD')
    require(not attr(test,'Popen') and not attr(test,'system') and not attr(test,'run'),'REAL_PROBE_IN_TESTS')
    require('adapter.planner' not in sources[FILES[1]]+sources[FILES[2]],'A15_IMPORT')
    require("'SYNTHETIC_DISPOSABLE_HOST'" in sources[FILES[2]] and "'INERT_CALLBACK'" in sources[FILES[2]],'SYNTHETIC_FIXTURES')
    for n in [n for n in ast.walk(gate) if isinstance(n,ast.For)]:
        require(not named(n,'_fixed_real_launch'),'AUTOMATIC_RETRY')
    hashes={p:hashlib.sha256(s.encode()).hexdigest() for p,s in sources.items()}
    return {'RESULT':'PASS_STATIC_CORE_WITH_EXPLICIT_REAL_BINDING_GAP','SOURCE_SHA256':hashes,'AUTHORIZED_SOURCE_FILES':3,'SOURCE_AST_IDENTITIES':{p:hashlib.sha256(ast.dump(t,include_attributes=False).encode()).hexdigest() for p,t in trees.items()},'ATOMIC_RESERVATION_PRESENT':True,'FILE_AND_DIRECTORY_BARRIERS_PRESENT':True,'READONLY_CONFIRMATION_PRESENT':True,'RECOVERY_NEVER_ADMITS_LAUNCH':True,'NO_ACTUAL_PROBE_POSSIBLE_WITH_CURRENT_REAL_BINDING':True,'REAL_AUTHORITY_READER_PROFILE_BOUND':False,'SYNTHETIC_CASES_IMPLEMENTED':len(expected),'SYNTHETIC_TESTS_EXECUTED':0,'ACTIVE_HOST_VERIFIED':False,'STATIC_QUALIFICATION':'PARTIAL (static core passes; real issued-authority mapping/profile remains unavailable)','GATE_FULLY_QUALIFIED':False}
if __name__=='__main__':print(json.dumps(verify(json.load(sys.stdin) if '--candidate' in sys.argv else None),sort_keys=True))
