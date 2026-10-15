"""Separate read-only effectiveness verifier. No construction or synthetic tests."""
import hashlib,json,pathlib,subprocess,sys
D=pathlib.Path(__file__).resolve().parent;R=D.parents[3]
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canon(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def verify():
 result=json.loads(subprocess.check_output([sys.executable,str((D/'verify.py').relative_to(R))],cwd=str(R)))
 e=load(D/'effective-implementation-test-grant-reference.json')
 assert e['IMPLEMENTATION_TEST_GRANT_EFFECTIVE'] is True and e['GRANT_IDENTITY']==result['GRANT_IDENTITY']
 assert e['APPROVED_SUBJECT_IDENTITY']==result['APPROVED_SUBJECT_IDENTITY'] and e['PROJECT_OWNER_DECISION_IDENTITY']==result['PROJECT_OWNER_DECISION_IDENTITY']
 pin=e['GRANT_RECORD_PIN'];assert sha(R/pin['PATH'])==pin['RAW_SHA256']
 assert e['GOVERNING_CHARTER_IDENTITY']['sha256']=='d26962c58f17281173e965433dae63a941e078115f3dcc30e2a3512fa21812b8'
 assert e['EFFECTIVE_CHARTER_LIFECYCLE_IDENTITY']['sha256']=='a27516baa0ab7f34a36a1130490b6cfa38c508975ca337e0824c8eac33715cbb'
 for p in e['PREREQUISITE_PINS']:assert sha(R/p['PATH'])==p['RAW_SHA256']
 seeds=load(D/'four-seed-determinism.json');assert seeds['RESULT']=='PASS' and [x['PYTHONHASHSEED'] for x in seeds['SEEDS']]==[0,1,7,101]
 assert all(x['SEMANTIC_SHA256']==canon(result) for x in seeds['SEEDS'])
 neg=load(D/'negative-controls.json');assert neg['PASSED']==neg['TOTAL']==22 and all(x['RESULT']=='REJECTED' for x in neg['CONTROLS'])
 preservation=load(D/'preservation-audit.json');assert preservation['RESULT']=='PASS' and not preservation['CHANGED_PREEXISTING_FILES']
 for flag in ['A15_EXECUTION_AUTHORITY_ISSUED','A15_CAPTURE_AUTHORITY_ISSUED','A15_EXECUTED','ADAPTER_CONSTRUCTION_PERFORMED','SYNTHETIC_TESTS_EXECUTED','TEST_CAMPAIGN_STARTED']:assert e[flag] is False
 return {'RESULT':'PASS_EFFECTIVE_IMPLEMENTATION_TEST_GRANT','GRANT_IDENTITY':result['GRANT_IDENTITY'],'APPROVED_SUBJECT_IDENTITY':result['APPROVED_SUBJECT_IDENTITY'],'EFFECTIVE_REFERENCE_PIN':{'PATH':str((D/'effective-implementation-test-grant-reference.json').relative_to(R)),'RAW_SHA256':sha(D/'effective-implementation-test-grant-reference.json')},'IMPLEMENTATION_TEST_GRANT_EFFECTIVE':'YES','A15_EXECUTION_AUTHORITY_ISSUED':'NO','A15_CAPTURE_AUTHORITY_ISSUED':'NO','CONSTRUCTION_OR_TESTS_STARTED_BY_ISSUANCE':'NO'}
if __name__=='__main__':print(json.dumps(verify(),sort_keys=True))
