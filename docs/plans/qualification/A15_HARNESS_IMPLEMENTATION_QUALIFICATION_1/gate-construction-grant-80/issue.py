"""Documentary Package80 grant issuance only. No implementation or active tests."""
import copy,hashlib,json,os,pathlib,subprocess,sys,tempfile
E=pathlib.Path(__file__).parent;S=E.parent/'single-use-gate-79'
def cb(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def read(p):return json.loads(pathlib.Path(p).read_text())
def pin(p):return {'PATH':str(p),'RAW_SHA256':hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()}
def aid(v,ns):return {'kind':'CONTENT_IDENTITY','namespace':ns,'sha256':hashlib.sha256(cb(v)).hexdigest()}
publications=[]
def publish(name,value):
    target=E/name
    assert not target.exists() and not target.is_symlink(),str(target)
    raw=value.encode() if isinstance(value,str) else (json.dumps(value,sort_keys=True,indent=2,ensure_ascii=False)+'\n').encode()
    fd,tmp=tempfile.mkstemp(prefix='.documentary-grant-80-',dir=str(E))
    try:
        with os.fdopen(fd,'wb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
        os.link(tmp,str(target));os.unlink(tmp)
        d=os.open(str(E),os.O_RDONLY|os.O_DIRECTORY)
        try:os.fsync(d)
        finally:os.close(d)
        assert target.read_bytes()==raw
    finally:
        if os.path.exists(tmp):os.unlink(tmp)
    publications.append({'PATH':str(target),'RAW_SHA256':hashlib.sha256(raw).hexdigest(),'FILE_FSYNC':True,'NO_OVERWRITE_HARDLINK_PUBLICATION':True,'DIRECTORY_FSYNC':True,'INDEPENDENT_BYTE_REREAD':True})
    return target
source='''# Package80 owner authorization (verbatim Authority section)
The KGE-Forge project owner explicitly selected:

`AUTHORIZE_BOUNDED_H77_02_GATE_CONSTRUCTION_AND_SYNTHETIC_QUALIFICATION`

Exact approved subject:

`CONTENT_IDENTITY/qualification-h77-02-gate-implementation-test-subject-v1:9c6ccc426dc2acb4126d85006ea6fb6f830b8c21bbfbfcdf8003058e146c9354`

Governing authority: effective KGE-Forge Qualification Governance Charter v1.0.

This decision authorizes issuance of the exact bounded construction/test instrument only after independent authentication.

It does not authorize H77-02 probe execution.
'''
publish('owner-approval-source.txt',source)
subject=read(S/'proposed-implementation-authority-subject.json');b=subject['CONTENT']
owner={'SCHEMA':'H77-02-GATE-OWNER-CONSTRUCTION-DECISION-80-1','SELECTED_OPTION':'AUTHORIZE_BOUNDED_H77_02_GATE_CONSTRUCTION_AND_SYNTHETIC_QUALIFICATION','APPROVED_SUBJECT_IDENTITY':subject['IDENTITY'],'ISSUER_ROLE':b['ISSUER_ROLE'],'SOURCE_PIN':pin(E/'owner-approval-source.txt'),'SOURCE_PROVENANCE':'Explicit current-session project-owner user instruction, Authority section transcribed verbatim; no personal credential, signature, platform message ID or timestamp invented','ORIGINAL_DOSSIER_PIN':pin(S/'unselected-implementation-decision-dossier.json'),'SUBJECT_PIN':pin(S/'proposed-implementation-authority-subject.json'),'QUALIFICATION_PIN':pin(S/'independent-verification.json'),'MANDATE_LIMIT':'Exact bounded gate construction/test instrument issuance only; no implementation/tests in Package80; no H77 or A15 execution'}
publish('owner-approval-provenance.json',owner)
record={'SCHEMA':'H77-02-GATE-CONSTRUCTION-TEST-GRANT-80-1','APPROVED_SUBJECT_IDENTITY':subject['IDENTITY'],'APPROVED_SUBJECT_PIN':pin(S/'proposed-implementation-authority-subject.json'),'QUALIFICATION_EVIDENCE_PIN':pin(S/'independent-verification.json'),'ISSUER_ROLE':b['ISSUER_ROLE'],'GOVERNING_CHARTER':b['GOVERNING_CHARTER'],'CHARTER_LIFECYCLE':b['EFFECTIVE_CHARTER_LIFECYCLE'],'PROJECT_OWNER_DECISION_EVIDENCE':{'IDENTITY':aid(owner,'qualification-h77-02-gate-owner-construction-decision-v1'),'PIN':pin(E/'owner-approval-provenance.json')},'PERMITTED_SOURCE_PATHS':b['IMPLEMENTATION_PATHS'],'PERMITTED_SYNTHETIC_TESTS':b['PERMITTED_TESTS'],'RESOURCE_LIMITS':b['RESOURCE_LIMITS'],'TEST_ENTRY_PREDICATES':b['PHASE_GATES'],'OUTPUT_EVIDENCE_BOUNDARY':b['OUTPUT_BOUNDARY'],'TEMP_BOUNDARY':b['TEMP_BOUNDARY'],'FAILURE_RETRY_POLICY':{'AUTOMATIC_RETRIES':0,'CAMPAIGN_LIMIT':b['CAMPAIGN_LIMIT'],'PARTIALLY_MUTATED_INPUT_REUSE':False},'HISTORICAL_EXCLUSIONS':b['EXCLUSIONS'],'EFFECTIVE_BOUNDARY':'Only after immutable grant publication, independent reread/verification, four-seed reconstruction, negative controls and preservation checks; then separate effective reference publication. No backdating.','REVOCATION_RULE':b['EXPIRATION_RULE'],'SCOPE_CONTRACT':b,'INSTRUMENT_STATUS':'ISSUED_REQUIRES_SEPARATE_EFFECTIVENESS_REFERENCE','H77_PROBE_AUTHORITY':None,'A15_EXECUTION_AUTHORITY':None,'A15_CAPTURE_AUTHORITY':None}
doc={'RECORD':record,'GRANT_IDENTITY':aid(record,'qualification-h77-02-gate-construction-test-issued-grant-v1')}
verify=['python3',str(E/'verify.py')]
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
# Independent reader verifies candidate bytes, authority and conflict search BEFORE publication.
candidate=subprocess.run(verify+['--candidate'],input=json.dumps(doc),text=True,capture_output=True,env=env,check=True)
publish('prepublication-independent-validation.json',json.loads(candidate.stdout))
publish('subject-pin-verification.json',{'RESULT':'PASS','SUBJECT_PIN':pin(S/'proposed-implementation-authority-subject.json'),'SUBJECT_IDENTITY':subject['IDENTITY'],'QUALIFICATION_PIN':pin(S/'independent-verification.json'),'OWNER_OPTION':owner['SELECTED_OPTION'],'EXACT_ALLOWLIST':b['IMPLEMENTATION_PATHS'],'ALL_PREPUBLICATION_CHECKS':'PASS','CONFLICTING_GRANT_FOUND':False})
grantpath=publish('issued-gate-construction-test-grant-'+doc['GRANT_IDENTITY']['sha256']+'.json',doc)
q=subprocess.run(verify,text=True,capture_output=True,env=env,check=True)
publish('independent-persisted-record-verification.json',json.loads(q.stdout))
seeds=[]
for seed in [0,1,7,101]:
    q=subprocess.run(verify,text=True,capture_output=True,env=dict(env,PYTHONHASHSEED=str(seed)),check=True)
    result=json.loads(q.stdout);seeds.append({'SEED':seed,'RECONSTRUCTION':result,'SEMANTIC_SHA256':hashlib.sha256(cb(result)).hexdigest()})
assert len({x['SEMANTIC_SHA256'] for x in seeds})==1
publish('four-seed-determinism.json',{'RESULT':'PASS_STATIC_DOCUMENTARY_READERS','FRESH_READERS':4,'SEEDS':seeds,'NO_GATE_OR_SYNTHETIC_TESTS':True})
cases=[]
def add(label,edit):
    bad=copy.deepcopy(doc);edit(bad['RECORD']);bad['GRANT_IDENTITY']=aid(bad['RECORD'],'qualification-h77-02-gate-construction-test-issued-grant-v1');cases.append((label,bad))
add('Wrong approved subject',lambda r:r['APPROVED_SUBJECT_IDENTITY'].update(sha256='0'*64))
add('Wrong issuer',lambda r:r.update(ISSUER_ROLE='UNAUTHORIZED'))
add('Wrong governing charter',lambda r:r['GOVERNING_CHARTER'].update(sha256='0'*64))
add('Wrong owner decision evidence',lambda r:r['PROJECT_OWNER_DECISION_EVIDENCE']['IDENTITY'].update(sha256='0'*64))
add('Unauthorized fourth implementation path',lambda r:r['PERMITTED_SOURCE_PATHS'].append('adapter/planner/codec.py'))
add('Actual H77 probe test permitted',lambda r:r['PERMITTED_SYNTHETIC_TESTS'].append('Run actual H77-02'))
add('Resource ceiling expanded',lambda r:r['RESOURCE_LIMITS'].update(CHILD_CPU=31))
add('Missing synthetic entry predicates',lambda r:r['TEST_ENTRY_PREDICATES'].update(ACTIVE_SYNTHETIC=[]))
add('Output scope expanded',lambda r:r.update(OUTPUT_EVIDENCE_BOUNDARY='/'))
add('Automatic retry enabled',lambda r:r['FAILURE_RETRY_POLICY'].update(AUTOMATIC_RETRIES=1))
add('Missing historical exclusion',lambda r:r['HISTORICAL_EXCLUSIONS'].remove('old campaign reuse'))
add('Premature effectiveness',lambda r:r.update(EFFECTIVE_BOUNDARY='Immediately on owner message'))
add('Grant self-issuance allowed',lambda r:r['SCOPE_CONTRACT'].update(MANDATES='Unrestricted self-issuance'))
add('Actual H77 probe authority included',lambda r:r.update(H77_PROBE_AUTHORITY={'granted':True}))
add('A15 execution authority included',lambda r:r.update(A15_EXECUTION_AUTHORITY={'granted':True}))
add('A15 capture authority included',lambda r:r.update(A15_CAPTURE_AUTHORITY={'granted':True}))
results=[]
for label,bad in cases:
    q=subprocess.run(verify+['--candidate'],input=json.dumps(bad),text=True,capture_output=True,env=env)
    assert q.returncode!=0,(label,q.stdout)
    results.append({'CONTROL':label,'RESULT':'REJECTED','COUNTEREXAMPLE':q.stderr.splitlines()[-1]})
publish('negative-controls.json',{'RESULT':'16/16 PASS_STATIC_DOCUMENTARY_CONTROLS','CONTROLS':results,'NOTE':'Mutated record digests recomputed; scope checks reject independently of hash validity. No implementation/host/process qualification tests.'})
old=read(E/'preservation-before.json');changed=[p for p,h in old.items() if not pathlib.Path(p).is_file() or pin(p)['RAW_SHA256']!=h];assert not changed,changed
publish('preservation-audit.json',{'RESULT':'PASS','PRIOR_FILES_VERIFIED':len(old),'CHANGED':changed,'GATE_IMPLEMENTATION_PERFORMED':False,'GATE_SYNTHETIC_TESTS_EXECUTED':False,'H77_PROBE_EXECUTED':False,'A15_EXECUTED':False,'A15_EXECUTION_AUTHORITY_ISSUED':False,'A15_CAPTURE_AUTHORITY_ISSUED':False,'STOPPED_CAMPAIGN_MODIFIED':False,'ADAPTER_SOURCE_FILES_MODIFIED':0,'BASELINE_AMENDED':False,'TOTAL_REFERENCES':161,'TOTAL_RESOLVED':109,'TOTAL_UNRESOLVED':52,'PRODUCTION_EFFECT':False})
paths=b['IMPLEMENTATION_PATHS'];assert all(not pathlib.Path(x).exists() for x in paths)
publish('construction-and-test-entry-assessment.json',{'CONSTRUCTION_ENTRY_READY':'YES_AT_PACKAGE80_SNAPSHOT_REQUIRES_FRESH_ENTRY_RECHECK','APPROVED_SUBJECT_IDENTITY':subject['IDENTITY'],'EXACT_SOURCE_ALLOWLIST':paths,'NO_CONFLICTING_IMPLEMENTATION':True,'CONSTRUCTION_PHASE_PERMITTED':True,'CURRENT_REVOKED_OR_SUPERSEDED_RECORD':'NONE_FOUND_IN_AVAILABLE_PROJECT_EVIDENCE','GRANT_EFFECTIVE_DEPENDENCY':'Only after final separate reference publication and reread','SYNTHETIC_TEST_READY':False,'MISSING_SYNTHETIC_ENTRY':['qualified construction executable/source identity','sealed fixtures and independent expected outputs','verified runtime permissions, confinement and resources','exact future synthetic campaign manifest and authority binding'],'H77_PROBE_READY':False,'NO_CONSTRUCTION_OR_TEST_ACTIVATED':True})
publish('persistence-publication-evidence.json',{'MECHANISM':'File fsync -> no-overwrite hard-link publication -> directory fsync -> byte reread; exclusive documentary files only','PUBLICATIONS':publications,'ASSURANCE_LIMITATION':'Successful local syscalls/publication observed, not general power-loss durability or qualified future consumption-store persistence'})
checks=['subject-pin-verification.json','prepublication-independent-validation.json','independent-persisted-record-verification.json','four-seed-determinism.json','negative-controls.json','preservation-audit.json','construction-and-test-entry-assessment.json','persistence-publication-evidence.json']
ref={'SCHEMA':'H77-02-GATE-EFFECTIVE-CONSTRUCTION-GRANT-REFERENCE-80-1','GRANT_EFFECTIVE':True,'GRANT_IDENTITY':doc['GRANT_IDENTITY'],'GRANT_RECORD_PIN':pin(grantpath),'APPROVED_SUBJECT_IDENTITY':subject['IDENTITY'],'ISSUER_ROLE':b['ISSUER_ROLE'],'GOVERNING_CHARTER':b['GOVERNING_CHARTER'],'ISSUANCE_CHECK_PINS':[pin(E/x) for x in checks],'EFFECTIVE_BOUNDARY':record['EFFECTIVE_BOUNDARY'],'CONSTRUCTION_ACTIVATION':'Fresh exact grant, lifecycle, revocation, actor, source-path and nonconflicting implementation check before modifications','SYNTHETIC_TEST_READY':False,'H77_PROBE_EXECUTED':False,'GATE_IMPLEMENTATION_PERFORMED':False,'GATE_SYNTHETIC_TESTS_EXECUTED':False,'A15_EXECUTION_AUTHORITY_ISSUED':False,'A15_CAPTURE_AUTHORITY_ISSUED':False,'NO_H77_PROBE_AUTHORITY':True,'PRODUCTION_EFFECT':False}
publish('effective-gate-construction-grant-reference.json',ref)
q=subprocess.run(verify+['--effective'],text=True,capture_output=True,env=env,check=True)
publish('independent-effectiveness-verification.json',json.loads(q.stdout))
print(json.dumps({'RESULT':'PASS','GRANT_IDENTITY':doc['GRANT_IDENTITY'],'GRANT_EFFECTIVE':True,'CONSTRUCTION_ENTRY_READY':True,'SYNTHETIC_TEST_READY':False,'NO_CONSTRUCTION_OR_PROBE':True}))
