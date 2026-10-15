"""Independent, read-only Package78 evidence verifier. Never launches the probe."""
import hashlib, json, pathlib, sys

R = pathlib.Path('.')
P = R / 'docs/plans/qualification/A15_HARNESS_IMPLEMENTATION_QUALIFICATION_1'
E = P / 'probe-grant-issuance-78'
S = P / 'execution-contract-77'
SUBJECT = '762b88071476cea67c08c8e57d5b893f61c2d8843cc7f0f04a07f05b52fe3a80'
RAW = '8c6a1e64c932b03a8c24fee823d0b84ae7178fca708db2986308e4610a35bf8f'
QUAL = '11b3be42101a65df4e5050ada594a39e76b2ad1986f1695883c68097221265bd'

def read(p):
    return json.loads(pathlib.Path(p).read_text())

def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()

def cb(v):
    return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()

def need(condition, reason):
    if not condition:
        raise ValueError(reason)

def reconstruct():
    subject = read(S/'host-capability-test-authorization-subject.json')
    need(sha(S/'host-capability-test-authorization-subject.json') == RAW, 'SUBJECT_BYTES')
    b = subject['CONTENT']
    need(hashlib.sha256(cb(b)).hexdigest() == SUBJECT == subject['IDENTITY']['sha256'], 'SUBJECT_CONTENT_ID')
    need(sha(S/'independent-reconstruction.json') == QUAL, 'QUALIFICATION_PIN')
    qualified = read(S/'independent-reconstruction.json')
    need(qualified['HOST_CAPABILITY_SUBSET_DECISION_READY'] and qualified['HOST_SUBSET_SUBJECT_IDENTITY']==subject['IDENTITY'], 'QUALIFICATION_SCOPE')
    for path,h in read(S/'evidence-index.json')['FILES'].items():
        need(sha(path)==h,'PACKAGE77_CHANGED:'+path)
    dossier = read(S/'unselected-host-capability-decision-dossier.json')
    decision = read(E/'owner-decision-provenance.json')
    need(dossier['SELECTION'] is None and not dossier['AUTHORITY_ISSUED'], 'EARLIER_DOSSIER_CHANGED')
    need(decision['SELECTED_OPTION']==dossier['OPTIONS'][0]['OPTION_ID']=='AUTHORIZE_ONE_DIRECT_HOST_NAMESPACE_METADATA_PROBE', 'OWNER_OPTION')
    need(decision['APPROVED_SUBJECT_IDENTITY']==dossier['EXACT_SUBJECT_IDENTITY']==subject['IDENTITY'], 'OWNER_SUBJECT')
    need(decision['ISSUER_ROLE']==b['ISSUER_ROLE'], 'ISSUER_ROLE')
    need(sha(E/'owner-decision-source.txt')==decision['SOURCE_PIN']['RAW_SHA256'], 'OWNER_PROVENANCE')
    source=(E/'owner-decision-source.txt').read_text()
    need(SUBJECT in source and decision['SELECTED_OPTION'] in source and 'one H77-02' in source,'OWNER_SOURCE')
    proc=b['PROCEDURE']; argv=proc['COMMAND_OR_TEST']['ARGV']
    need(argv[:4]==['/usr/bin/timeout','--signal=KILL','60s','/usr/bin/prlimit'], 'COMMAND_PREFIX')
    need(argv[4:8]==['--cpu=30:30','--as=1073741824:1073741824','--fsize=16777216:16777216','--nofile=64:64'], 'RESOURCE_ARGV')
    need(argv[8]=='/usr/bin/bwrap' and argv[-3:-1]==['/usr/bin/python3','-c'], 'EXECUTABLE_ARGV')
    need(argv[-1]==proc['PROGRAM']['SOURCE'],'PROGRAM_SUBSTITUTED')
    need(hashlib.sha256(cb(argv[-1])).hexdigest()==proc['PROGRAM']['CONTENT_IDENTITY']['sha256'],'PROGRAM_ID')
    need(all(x in argv for x in ['--unshare-user','--unshare-pid','--unshare-net']), 'NAMESPACE')
    for pin in proc['TOOL_BINARY_PINS']:
        need(sha(pin['PATH'])==pin['RAW_SHA256'],'BINARY_PIN:'+pin['PATH'])
    need(pathlib.Path('/usr/bin/python3').resolve()==pathlib.Path('/usr/bin/python3.8'), 'PYTHON_RESOLUTION')
    budget={'CHILD_AS':1073741824,'CHILD_CPU':30,'CHILD_FDS':64,'CHILD_FSIZE':16777216,'CHILD_WALL':60,'MAX_ACTUAL_PROCESS_SLOTS':4,'MAX_PAYLOAD_LAUNCHES':1,'RETRIES':0,'TOTAL_WALL':600,'TOTAL_WRITES':1048576}
    need(proc['RESOURCE_BUDGET']==budget,'RESOURCE_BUDGET')
    charterpath=pathlib.Path('docs/plans/qualification/KGE_FORGE_QUALIFICATION_GOVERNANCE_CHARTER_ADOPTION_66/effective-charter-reference.json')
    charter=read(charterpath)
    need(charter['CHARTER_EFFECTIVE'] and charter['CHARTER_VERSION']=='1.0' and charter['CHARTER_CONTENT_IDENTITY']==b['GOVERNING_CHARTER_IDENTITY'], 'CHARTER')
    prev=None
    for n,t in enumerate(charter['TRANSITIONS'],1):
        record=read(t['PATH']); body=record['RECORD']
        need(hashlib.sha256(cb(body)).hexdigest()==record['IDENTITY']['sha256']==t['IDENTITY']['sha256'],'LIFECYCLE_ID')
        need(body['transition_ordinal']==n and body['from_state']==['DRAFT','REVIEWED','APPROVED'][n-1] and body['to_state']==['REVIEWED','APPROVED','EFFECTIVE'][n-1],'LIFECYCLE_ORDER')
        if prev:need(body['predecessor_lifecycle_record_identity']==prev,'LIFECYCLE_PREDECESSOR')
        prev=record['IDENTITY']
    need(prev==b['CHARTER_LIFECYCLE_IDENTITY'],'EFFECTIVE_LIFECYCLE')
    for pin in [b['NORMATIVE_MANDATE_REFERENCE_PIN'], b['CONFINEMENT_SPEC_PIN'], b['PROCEDURE_PIN']]:
        need(sha(pin['PATH'])==pin['RAW_SHA256'],'REFERENCE_PIN')
    norm=read(b['NORMATIVE_MANDATE_REFERENCE_PIN']['PATH'])
    need(norm['NORMATIVE_MANDATE_EFFECTIVE'] and norm['MANDATE']=='NORMATIVE_SCOPE_ONLY','NORMATIVE_STATUS')
    need(sha(norm['ADOPTION_RECORD_PIN']['PATH'])==norm['ADOPTION_RECORD_PIN']['RAW_SHA256'],'NORMATIVE_RECORD')
    grant=read('docs/plans/qualification/E2_P05_D01_A15_IMPLEMENTATION_TEST_GRANT_ISSUANCE_71/effective-implementation-test-grant-reference.json')
    closure=read(S/'campaign-input-closure.json')
    pin=closure['STOPPED_JOURNAL_PIN'];need(sha(pin['PATH'])==pin['RAW_SHA256'],'STOPPED_JOURNAL')
    checks=read(E/'one-use-consumption-contract.json')
    need(checks['STATUS']=='PROPOSED_NOT_QUALIFIED' and not checks['IMPLEMENTED_LAUNCH_GATE'] and not checks['ACTUAL_HOST_DURABILITY_VERIFIED'],'ONE_USE_FALSE_QUALIFICATION')
    return {'SUBJECT_VERIFIED':'YES','COMMAND_AND_BINARY_PINS_VERIFIED':'YES','RESOURCE_LIMITS_VERIFIED':'YES (approved values, not host enforceability)','CHARTER_EFFECTIVE':'YES','ISSUER_ROLE_VERIFIED':'YES','OWNER_OPTION_VERIFIED':'YES','GRANT_PERSISTED':'NO','GRANT_INDEPENDENTLY_VERIFIED':'NO','GRANT_EFFECTIVE':'NO','ONE_USE_CONSUMPTION_CONTRACT':'FAIL','DIRECT_HOST_ENTRY_READY':'NO','RESULT':'PARTIAL','APPROVED_SUBJECT':subject['IDENTITY'],'COMMAND_SHA256':hashlib.sha256(cb(argv)).hexdigest(),'RESOURCE_BUDGET':budget,'PROBE_EXECUTED':False,'REASON':'No independently qualified, durable one-use launch/consumption gate bound to this host-probe authority'}

def validate_claim(v):
    expected=reconstruct()
    need(v==expected,'UNSUPPORTED_ISSUANCE_OR_SCOPE_CLAIM')
    return expected

if __name__=='__main__':
    result=validate_claim(json.load(sys.stdin)) if '--candidate' in sys.argv else reconstruct()
    print(json.dumps(result,sort_keys=True))
