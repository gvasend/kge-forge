"""Read-only final effective-reference verification, independent of issuance."""
import hashlib, json, pathlib, subprocess, sys
D=pathlib.Path(__file__).resolve().parent
ROOT=D.parents[3]
def read(p): return json.loads(p.read_text())
def h(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def canon(x): return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()).hexdigest()
r=json.loads(subprocess.check_output([sys.executable,str(D/'verify.py')],cwd=str(ROOT)))
e=read(D/'effective-normative-mandate-reference.json')
assert e['NORMATIVE_MANDATE_EFFECTIVE'] is True and e['MANDATE']=='NORMATIVE_SCOPE_ONLY'
assert e['ADOPTION_RECORD_IDENTITY']==r['ADOPTION_RECORD_IDENTITY']
p=e['ADOPTION_RECORD_PIN'];assert h(ROOT/p['PATH'])==p['RAW_SHA256']
assert e['OWNER_DECISION']==r['OWNER_DECISION_IDENTITY'] and e['NORMATIVE_SUBJECT']==r['NORMATIVE_SUBJECT']
assert e['GOVERNING_CHARTER']['sha256']=='d26962c58f17281173e965433dae63a941e078115f3dcc30e2a3512fa21812b8'
assert e['EFFECTIVE_LIFECYCLE']['sha256']=='a27516baa0ab7f34a36a1130490b6cfa38c508975ca337e0824c8eac33715cbb'
for flag in ['A15_EXECUTION_AUTHORITY_ISSUED','A15_CAPTURE_AUTHORITY_ISSUED','A15_EXECUTED']: assert e[flag] is False
for p in e['VERIFICATION_PINS']: assert h(ROOT/p['PATH'])==p['RAW_SHA256']
s=read(D/'four-seed-determinism.json');assert s['RESULT']=='PASS' and [a['PYTHONHASHSEED'] for a in s['SEEDS']]==[0,1,7,101]
assert all(a['RECONSTRUCTION']==r and a['SEMANTIC_SHA256']==canon(r) for a in s['SEEDS'])
n=read(D/'negative-controls.json');assert n['TOTAL']==n['PASSED']==19 and all(a['RESULT']=='REJECTED' for a in n['CONTROLS'])
p=read(D/'preservation-audit.json');assert p['RESULT']=='PASS' and not p['CHANGED_PREEXISTING_FILES']
a=read(D/'updated-authority-readiness.json');assert a['NORMATIVE_MANDATE_EFFECTIVE'] is True
assert not a['EXECUTION_DECISION_READY'] and not a['CAPTURE_DECISION_READY']
print(json.dumps({'RESULT':'PASS','EFFECTIVE_REFERENCE_RAW_SHA256':h(D/'effective-normative-mandate-reference.json'),'ADOPTION_RECORD_IDENTITY':r['ADOPTION_RECORD_IDENTITY'],'NORMATIVE_MANDATE_EFFECTIVE':True,'EXECUTION_AUTHORITY':False,'CAPTURE_AUTHORITY':False},sort_keys=True))
