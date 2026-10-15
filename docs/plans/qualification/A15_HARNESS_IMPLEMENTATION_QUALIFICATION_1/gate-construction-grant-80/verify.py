"""Independent documentary grant verification. No gate construction/test/launch."""
import hashlib,json,pathlib,sys
E=pathlib.Path(__file__).parent;S=E.parent/'single-use-gate-79'
DIGEST='9c6ccc426dc2acb4126d85006ea6fb6f830b8c21bbfbfcdf8003058e146c9354'
NS='qualification-h77-02-gate-construction-test-issued-grant-v1'
def cb(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def read(p):return json.loads(pathlib.Path(p).read_text())
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def aid(v,ns):return {'kind':'CONTENT_IDENTITY','namespace':ns,'sha256':hashlib.sha256(cb(v)).hexdigest()}
def need(v,msg):
    if not v:raise ValueError(msg)
def inputs():
    need(sha(S/'proposed-implementation-authority-subject.json')=='e72a217eabceeaaecb339d6479b6329b2f41dd06b8aa1829eb283374fc50aa74','SUBJECT_RAW_PIN')
    need(sha(S/'independent-verification.json')=='ddc6b12d7af5b5b8a3d9184cece93c7bd63424a284f0237e6d66f50e1bf3d6f7','QUALIFICATION_RAW_PIN')
    for p,h in read(S/'evidence-index.json')['FILES'].items():need(sha(p)==h,'PACKAGE79_CHANGED')
    s=read(S/'proposed-implementation-authority-subject.json');b=s['CONTENT']
    need(aid(b,'qualification-h77-02-gate-implementation-test-subject-v1')==s['IDENTITY'] and s['IDENTITY']['sha256']==DIGEST,'SUBJECT_ID')
    need(s['APPROVAL'] is None and not s['ISSUED'],'SUBJECT_IMMUTABILITY')
    d=read(S/'unselected-implementation-decision-dossier.json');q=read(S/'independent-verification.json')
    need(d['SELECTION'] is None and d['DECISION_READY'] and q['IMPLEMENTATION_DECISION_READY']=='YES_CONDITIONAL_SYNTHETIC_ENTRY','ORIGINAL_READINESS')
    owner=read(E/'owner-approval-provenance.json')
    need(owner['SELECTED_OPTION']==d['OPTIONS'][0]['OPTION_ID']=='AUTHORIZE_BOUNDED_H77_02_GATE_CONSTRUCTION_AND_SYNTHETIC_QUALIFICATION','OWNER_OPTION')
    need(owner['APPROVED_SUBJECT_IDENTITY']==s['IDENTITY'] and owner['ISSUER_ROLE']==b['ISSUER_ROLE'],'OWNER_SUBJECT_ROLE')
    need(sha(owner['SOURCE_PIN']['PATH'])==owner['SOURCE_PIN']['RAW_SHA256'],'OWNER_SOURCE_PIN')
    text=pathlib.Path(owner['SOURCE_PIN']['PATH']).read_text()
    need(DIGEST in text and owner['SELECTED_OPTION'] in text and 'does not authorize H77-02 probe execution' in text,'OWNER_PROVENANCE')
    for pin in b['EVIDENCE_PINS']+b['CONTRACT_PINS']:need(sha(pin['PATH'])==pin['RAW_SHA256'],'SUBJECT_BINDING_PIN')
    charter=read(b['EVIDENCE_PINS'][3]['PATH'])
    need(charter['CHARTER_EFFECTIVE'] and charter['CHARTER_VERSION']=='1.0' and charter['CHARTER_CONTENT_IDENTITY']==b['GOVERNING_CHARTER'],'CHARTER_EFFECTIVE')
    prior=None
    for n,t in enumerate(charter['TRANSITIONS'],1):
        doc=read(t['PATH']);r=doc['RECORD']
        need(hashlib.sha256(cb(r)).hexdigest()==doc['IDENTITY']['sha256']==t['IDENTITY']['sha256'],'CHARTER_TRANSITION_ID')
        need(r['transition_ordinal']==n and (r['from_state'],r['to_state'])==[('DRAFT','REVIEWED'),('REVIEWED','APPROVED'),('APPROVED','EFFECTIVE')][n-1],'CHARTER_ORDER')
        if prior:need(r['predecessor_lifecycle_record_identity']==prior,'CHARTER_PREDECESSOR')
        prior=doc['IDENTITY']
    need(prior==b['EFFECTIVE_CHARTER_LIFECYCLE'],'EFFECTIVE_CHARTER_ID')
    return s,b,owner
def conflicts(expected=None):
    found=[]
    for p in pathlib.Path('docs/plans').rglob('*.json'):
        if p==E/'conflict-search.json':continue
        raw=p.read_text()
        if DIGEST not in raw:continue
        doc=json.loads(raw)
        if isinstance(doc,dict) and isinstance(doc.get('RECORD'),dict) and doc['RECORD'].get('APPROVED_SUBJECT_IDENTITY',{}).get('sha256')==DIGEST:
            if p.parent==E and expected and doc.get('GRANT_IDENTITY')==expected:continue
            found.append(str(p))
        if isinstance(doc,dict) and doc.get('TARGET_SUBJECT_IDENTITY',{}).get('sha256')==DIGEST and doc.get('AUTHORITY_ACTION') in ['REVOKE','SUPERSEDE']:
            found.append(str(p))
    need(not found,'CONFLICTING_AUTHORITY:'+repr(found))
def validate(doc):
    s,b,owner=inputs();r=doc['RECORD']
    need(set(doc)=={'RECORD','GRANT_IDENTITY'} and doc['GRANT_IDENTITY']==aid(r,NS),'GRANT_CONTENT_ID')
    fields={'SCHEMA','APPROVED_SUBJECT_IDENTITY','APPROVED_SUBJECT_PIN','QUALIFICATION_EVIDENCE_PIN','ISSUER_ROLE','GOVERNING_CHARTER','CHARTER_LIFECYCLE','PROJECT_OWNER_DECISION_EVIDENCE','PERMITTED_SOURCE_PATHS','PERMITTED_SYNTHETIC_TESTS','RESOURCE_LIMITS','TEST_ENTRY_PREDICATES','OUTPUT_EVIDENCE_BOUNDARY','TEMP_BOUNDARY','FAILURE_RETRY_POLICY','HISTORICAL_EXCLUSIONS','EFFECTIVE_BOUNDARY','REVOCATION_RULE','SCOPE_CONTRACT','INSTRUMENT_STATUS','H77_PROBE_AUTHORITY','A15_EXECUTION_AUTHORITY','A15_CAPTURE_AUTHORITY'}
    need(set(r)==fields,'GRANT_FIELD_SET')
    need(r['SCHEMA']=='H77-02-GATE-CONSTRUCTION-TEST-GRANT-80-1' and r['INSTRUMENT_STATUS']=='ISSUED_REQUIRES_SEPARATE_EFFECTIVENESS_REFERENCE','GRANT_SCHEMA_STATUS')
    need(r['APPROVED_SUBJECT_IDENTITY']==s['IDENTITY'] and r['SCOPE_CONTRACT']==b,'GRANT_SCOPE')
    for k in ['APPROVED_SUBJECT_PIN','QUALIFICATION_EVIDENCE_PIN']:need(sha(r[k]['PATH'])==r[k]['RAW_SHA256'],'GRANT_EVIDENCE_PIN')
    need(r['ISSUER_ROLE']==b['ISSUER_ROLE'] and r['GOVERNING_CHARTER']==b['GOVERNING_CHARTER'] and r['CHARTER_LIFECYCLE']==b['EFFECTIVE_CHARTER_LIFECYCLE'],'ISSUER_CHARTER')
    de=r['PROJECT_OWNER_DECISION_EVIDENCE'];need(de['IDENTITY']==aid(owner,'qualification-h77-02-gate-owner-construction-decision-v1') and sha(de['PIN']['PATH'])==de['PIN']['RAW_SHA256'],'APPROVAL_EVIDENCE')
    need(r['PERMITTED_SOURCE_PATHS']==b['IMPLEMENTATION_PATHS']==['adapter/qualification_h77_02_gate/__init__.py','adapter/qualification_h77_02_gate/gate.py','adapter/tests/test_h77_02_launch_gate.py'],'SOURCE_PATHS')
    for field,source in [('PERMITTED_SYNTHETIC_TESTS','PERMITTED_TESTS'),('RESOURCE_LIMITS','RESOURCE_LIMITS'),('TEST_ENTRY_PREDICATES','PHASE_GATES'),('OUTPUT_EVIDENCE_BOUNDARY','OUTPUT_BOUNDARY'),('TEMP_BOUNDARY','TEMP_BOUNDARY'),('HISTORICAL_EXCLUSIONS','EXCLUSIONS'),('REVOCATION_RULE','EXPIRATION_RULE')]:need(r[field]==b[source],'MANDATE_FIELD:'+field)
    need(r['FAILURE_RETRY_POLICY']=={'AUTOMATIC_RETRIES':0,'CAMPAIGN_LIMIT':b['CAMPAIGN_LIMIT'],'PARTIALLY_MUTATED_INPUT_REUSE':False},'RETRY_POLICY')
    need(r['EFFECTIVE_BOUNDARY']=='Only after immutable grant publication, independent reread/verification, four-seed reconstruction, negative controls and preservation checks; then separate effective reference publication. No backdating.','EFFECTIVE_BOUNDARY')
    need(r['H77_PROBE_AUTHORITY'] is None and r['A15_EXECUTION_AUTHORITY'] is None and r['A15_CAPTURE_AUTHORITY'] is None,'FORBIDDEN_AUTHORITY')
    conflicts(doc['GRANT_IDENTITY'])
    return {'RESULT':'PASS_DOCUMENTARY_GRANT_CONTENT','GRANT_IDENTITY':doc['GRANT_IDENTITY'],'SUBJECT_VERIFIED':'YES','CHARTER_EFFECTIVE':'YES','ISSUER_AUTHORITY_VERIFIED':'YES','PERMITTED_SOURCE_PATHS':r['PERMITTED_SOURCE_PATHS'],'SYNTHETIC_TEST_READY':'NO','H77_PROBE_AUTHORITY':None,'A15_EXECUTION_AUTHORITY':None,'A15_CAPTURE_AUTHORITY':None}
def persisted():
    files=list(E.glob('issued-gate-construction-test-grant-*.json'));need(len(files)==1,'GRANT_RECORD_COUNT')
    doc=read(files[0]);result=validate(doc)
    need(files[0].name=='issued-gate-construction-test-grant-'+doc['GRANT_IDENTITY']['sha256']+'.json','GRANT_FILENAME')
    result['PERSISTED_RECORD_PIN']={'PATH':str(files[0]),'RAW_SHA256':sha(files[0])}
    return result
def effective():
    r=persisted();ref=read(E/'effective-gate-construction-grant-reference.json')
    need(ref['GRANT_IDENTITY']==r['GRANT_IDENTITY'] and ref['GRANT_EFFECTIVE'] is True,'EFFECTIVE_REFERENCE')
    need(ref['GRANT_RECORD_PIN']==r['PERSISTED_RECORD_PIN'],'EFFECTIVE_GRANT_PIN')
    for p in ref['ISSUANCE_CHECK_PINS']:need(sha(p['PATH'])==p['RAW_SHA256'],'EFFECTIVE_CHECK_PIN')
    need(not ref['H77_PROBE_EXECUTED'] and not ref['GATE_IMPLEMENTATION_PERFORMED'] and not ref['GATE_SYNTHETIC_TESTS_EXECUTED'],'EFFECT_NOT_EXECUTION')
    r['GRANT_EFFECTIVE']='YES';return r
if __name__=='__main__':
    r=validate(json.load(sys.stdin)) if '--candidate' in sys.argv else effective() if '--effective' in sys.argv else persisted()
    print(json.dumps(r,sort_keys=True))
