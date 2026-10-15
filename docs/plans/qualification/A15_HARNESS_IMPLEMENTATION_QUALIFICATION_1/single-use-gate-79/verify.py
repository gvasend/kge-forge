"""Independent static reconstruction; no launch gate imports or operations."""
import hashlib,json,pathlib,sys
E=pathlib.Path(__file__).parent;R=E.parent
def cb(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def read(p):return json.loads(pathlib.Path(p).read_text())
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def require(x,m):
    if not x:raise ValueError(m)
def verify(overrides=None):
    overrides=overrides or {}
    def get(n):return overrides[n] if n in overrides else read(E/n)
    for pkg in ['execution-contract-77','probe-grant-issuance-78']:
        for p,h in read(R/pkg/'evidence-index.json')['FILES'].items():require(sha(p)==h,'PRIOR_EVIDENCE_CHANGED')
    s=read(R/'execution-contract-77/host-capability-test-authorization-subject.json')
    require(s['IDENTITY']['sha256']=='762b88071476cea67c08c8e57d5b893f61c2d8843cc7f0f04a07f05b52fe3a80' and hashlib.sha256(cb(s['CONTENT'])).hexdigest()==s['IDENTITY']['sha256'],'SUBJECT')
    inventory=get('existing-primitive-inventory.json')
    require(not inventory['EXISTING_QUALIFIED_GATE'],'APPEND_ONLY_NOT_GATE')
    for c in inventory['COMPONENTS']:require(sha(c['SOURCE_PIN']['PATH'])==c['SOURCE_PIN']['RAW_SHA256'],'SOURCE')
    native=pathlib.Path('adapter/planner/codec.py').read_text();require('os.fsync(stream.fileno())' in native and 'os.link(temporary, str(target))' in native,'PRIMITIVE_EVIDENCE')
    state=get('single-use-state-machine.json')
    require(state['GRANT_CURRENT_STATE']=='OWNER_APPROVED_NOT_ISSUED' and state['ATTEMPT_CURRENT_STATE']=='NONE','APPROVAL_NOT_CONSUMPTION')
    require(state['CONSUMPTION_IRREVERSIBLE'] and state['NO_RETRY'] and state['TERMINAL_OUTCOMES_DO_NOT_REOPEN'],'IRREVERSIBILITY')
    edges=[['APPROVED','ISSUED'],['ISSUED','EFFECTIVE'],['EFFECTIVE','CONSUMED'],['CONSUMED','LAUNCHED'],['CONSUMED','LAUNCH_FAILED'],['CONSUMED','OUTCOME_UNKNOWN'],['LAUNCHED','COMPLETED'],['LAUNCHED','FAILED'],['LAUNCHED','OUTCOME_UNKNOWN']]
    require(state['ALLOWED_TRANSITIONS']==edges,'STATE_EDGES')
    key=get('consumption-key-specification.json')
    require(key['FIELDS']==['issued_grant_identity','approved_subject_identity','probe_identity','command_identity','execution_context','authorized_attempt_number'],'STABLE_KEY')
    require(key['AUTHORIZED_ATTEMPT_NUMBER']==1 and key['ACTUAL_CONSUMPTION_IDENTITY'] is None and not key['ACTUAL_BINDINGS_READY'],'FUTURE_KEY_NOT_ISSUED')
    require(key['APPROVED_SUBJECT_IDENTITY']==s['IDENTITY'] and key['PROBE_IDENTITY']==s['CONTENT']['PROCEDURE']['PROGRAM']['CONTENT_IDENTITY'],'KEY_DOMAIN')
    require(key['COMMAND_IDENTITY']['sha256']==hashlib.sha256(cb(s['CONTENT']['PROCEDURE']['COMMAND_OR_TEST'])).hexdigest(),'EXACT_COMMAND')
    contract=get('atomicity-durability-contract.json')
    require(not contract['IMPLEMENTED'] and not contract['QUALIFIED'] and not contract['DIRECT_HOST_ENTRY_VERIFIED'],'SPEC_NOT_QUALIFIED')
    steps=contract['STEPS'];require('O_EXCL|O_NOFOLLOW' in steps[4] and 'No exists-then-create' in steps[4],'NO_CHECK_CREATE_RACE')
    require('stale lock' in steps[5] and 'no repair/reset/removal' in steps[5],'STALE_LOCK')
    require('fsync(file)' in steps[6] and 'fsync(store directory)' in steps[6] and 'independent' in steps[7].lower(),'DURABILITY_BARRIER')
    require('Only this first claimant' in steps[8] and 'Recovery readers never mint capabilities' in steps[8] and 'before spawn' in steps[9],'LAUNCH_BEFORE_CLAIM')
    require('copied store' in key['STORE_RULE'] and 'unqualified remote' in steps[3],'SINGLE_STORE')
    crash=get('crash-concurrency-matrix.json')
    require(crash['CONCURRENT_WINNERS_MAX']==1 and crash['RESTART_WINNERS_AFTER_RESERVATION']==0,'CONCURRENT_CLAIMS')
    require(len(crash['CASES'])==6 and all(x['LAUNCH_PERMITTED']=='NO' and not x['RETRY_PERMITTED'] for x in crash['CASES']),'CRASH_REOPEN')
    design=get('minimal-gate-design.json');auth=get('implementation-authority-assessment.json')
    files=['adapter/qualification_h77_02_gate/__init__.py','adapter/qualification_h77_02_gate/gate.py','adapter/tests/test_h77_02_launch_gate.py']
    require(design['SOURCE_PATHS']==files and design['NO_CODE_CONSTRUCTED'] and not design['ADAPTER_MODIFICATION'],'GATE_SCOPE')
    require(not auth['IMPLEMENTATION_AUTHORITY_AVAILABLE'] and not auth['PATHS_AUTHORIZED_BY_PACKAGE71'],'AUTHORITY_SCOPE')
    require(not set(files)&set(auth['EXACT_EXISTING_ALLOWLIST']),'OLD_GRANT_SUBSTITUTION')
    require(sha(auth['EXISTING_GRANT_PIN']['PATH'])==auth['EXISTING_GRANT_PIN']['RAW_SHA256'],'GRANT_PIN')
    old=read(auth['EXISTING_GRANT_PIN']['PATH']);require(hashlib.sha256(cb(old['RECORD'])).hexdigest()==old['GRANT_IDENTITY']['sha256'],'ISSUED_GRANT_ID')
    subject=get('proposed-implementation-authority-subject.json');content=subject['CONTENT']
    require(not subject['ISSUED'] and subject['APPROVAL'] is None,'PREMATURE_ISSUANCE')
    require(content['IMPLEMENTATION_PATHS']==files and content['H77_SUBJECT']==s['IDENTITY'],'UNAUTHORIZED_PATH')
    require(content['SYNTHETIC_INPUTS']['LAUNCH_BACKEND']=='Inert in-process callback only; child claim tests may invoke pinned Python and authorized test file only','ACTUAL_PROBE_EXECUTION')
    require('A15 adapter/fake/native/real execution or capture' in content['EXCLUSIONS'] and 'H77-02 execution or grant issuance' in content['EXCLUSIONS'],'REAL_EXECUTION')
    require('unknown denies all active tests' in content['PHASE_GATES']['ACTIVE_SYNTHETIC'][3] and 'No real H77 argv' in content['PHASE_GATES']['ACTIVE_SYNTHETIC'][5],'ENVIRONMENT_GATE')
    require(content['RESOURCE_LIMITS']=={'MAX_ACTUAL_PROCESS_SLOTS':4,'MAX_PAYLOAD_LAUNCHES':128,'CHILD_WALL':60,'CHILD_CPU':30,'CHILD_AS':1073741824,'CHILD_FSIZE':16777216,'CHILD_FDS':64,'TOTAL_WRITES':67108864,'TOTAL_WALL':600,'RETRIES':0},'RESOURCES')
    require(not content['APPROVAL_EVIDENCE_INCLUDED_IN_DIGEST'],'NONCIRCULAR')
    for p in content['CONTRACT_PINS']+content['EVIDENCE_PINS']:require(sha(p['PATH'])==p['RAW_SHA256'],'BOUND_CONTENT_CHANGED')
    require(hashlib.sha256(cb(content)).hexdigest()==subject['IDENTITY']['sha256'],'AUTHORITY_CONTENT_ID')
    charter=read(content['EVIDENCE_PINS'][3]['PATH']);require(charter['CHARTER_EFFECTIVE'] and charter['CHARTER_CONTENT_IDENTITY']==content['GOVERNING_CHARTER'],'CHARTER')
    require(charter['EFFECTIVE_LIFECYCLE_IDENTITY']==content['EFFECTIVE_CHARTER_LIFECYCLE'],'LIFECYCLE')
    for p in files:require(not pathlib.Path(p).exists(),'UNAUTHORIZED_GATE_CONSTRUCTED')
    # Independent deterministic example calculation, not an actual consumption record.
    fixture={'schema':'H77-02-CONSUMPTION-KEY-1','issued_grant_identity':{'kind':'CONTENT_IDENTITY','namespace':'qualification-h77-02-gate-synthetic-grant-v1','sha256':'1'*64},'approved_subject_identity':key['APPROVED_SUBJECT_IDENTITY'],'probe_identity':key['PROBE_IDENTITY'],'command_identity':key['COMMAND_IDENTITY'],'execution_context':{'host_profile_identity':{'kind':'CONTENT_IDENTITY','namespace':'qualification-h77-02-gate-synthetic-host-v1','sha256':'2'*64}},'authorized_attempt_number':1}
    reverse=dict(reversed(list(fixture.items())));require(cb(fixture)==cb(reverse),'UNSTABLE_SERIALIZATION')
    return {'RESULT':'PASS_STATIC_DESIGN','H77_02_SUBJECT_AUTHENTICATED':'YES','EXISTING_QUALIFIED_GATE':'NO','NEW_IMPLEMENTATION_REQUIRED':'YES','CONSUMPTION_IDENTITY_COMPLETE':'YES_SPECIFICATION','ATOMIC_CLAIM_CONTRACT_COMPLETE':'YES_DESIGN','DURABILITY_CONTRACT_COMPLETE':'YES_REQUIREMENTS_NOT_HOST_ASSURANCE','CRASH_CONCURRENCY_CONTRACT_COMPLETE':'YES_CONTRACT','IMPLEMENTATION_AUTHORITY_AVAILABLE':'NO','IMPLEMENTATION_DECISION_READY':'YES_CONDITIONAL_SYNTHETIC_ENTRY','IMPLEMENTATION_SUBJECT_IDENTITY':subject['IDENTITY'],'SYNTHETIC_KEY_EXAMPLE_SHA256':hashlib.sha256(cb(fixture)).hexdigest(),'NO_GATE_PROBE_OR_TEST_EXECUTION':True}
if __name__=='__main__':print(json.dumps(verify(json.load(sys.stdin) if '--candidate' in sys.argv else None),sort_keys=True))
