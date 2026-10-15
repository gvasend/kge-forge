"""Finish issuance checks and separate effectiveness publication; no repair/test."""
import hashlib,json,os,stat,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];OUT=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text())
def pin(p):return {'path':str(p.relative_to(ROOT)),'raw_sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def publish(name,value):
 target=OUT/name;assert not target.exists() and not target.is_symlink()
 raw=(json.dumps(value,indent=2,sort_keys=True,ensure_ascii=False)+'\n').encode();fd,tmp=tempfile.mkstemp(prefix='.effect-publication-',dir=str(OUT))
 try:
  with os.fdopen(fd,'wb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
  os.link(tmp,str(target));os.unlink(tmp)
  directory=os.open(str(OUT),os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
  try:os.fsync(directory)
  finally:os.close(directory)
  fd=os.open(str(target),os.O_RDONLY|os.O_NOFOLLOW)
  try:
   parts=[]
   while True:
    chunk=os.read(fd,4096)
    if not chunk:break
    parts.append(chunk)
   assert b''.join(parts)==raw and os.fstat(fd).st_nlink==1
  finally:os.close(fd)
 finally:
  if os.path.exists(tmp):os.unlink(tmp)
 return target
runs=[]
for seed in (0,1,7,101):
 p=subprocess.run(['/usr/bin/python3.8',str((OUT/'verify_record.py').relative_to(ROOT))],cwd=str(ROOT),env=dict(os.environ,PYTHONHASHSEED=str(seed),PYTHONDONTWRITEBYTECODE='1'),capture_output=True,text=True,check=True)
 runs.append({'PYTHONHASHSEED':seed,**json.loads(p.stdout)})
assert len({json.dumps(r['SEMANTIC_IDENTITY'],sort_keys=True) for r in runs})==1
publish('four-seed-persisted-reconstruction.json',{'RESULT':'PASS','FRESH_RECORD_READERS':4,'NO_BOOTSTRAP_IMPORT_OR_EXECUTION':True,'RUNS':runs})
neg=runs[0]['RECONSTRUCTION']['NEGATIVES'];assert len(neg)==24 and all(n['RESULT']=='REJECTED' for n in neg)
publish('negative-control-results.json',{'RESULT':'PASS','PASSED':len(neg),'TOTAL':len(neg),'CONTROLS':neg,'METHOD':'in-memory record mutations, canonical re-identification, independent exact-scope validation; no target/test/probe invocation'})
prior=read(OUT/'preservation-before.json');changed=[p for p,h in prior.items() if not (ROOT/p).is_file() or pin(ROOT/p)['raw_sha256']!=h];assert not changed,changed
publish('preservation-audit.json',{'RESULT':'PASS','RETAINED_FILES_CHECKED':len(prior),'CHANGED_PREVIOUS_FILES':changed,'BOOTSTRAP_SOURCE_FILES_MODIFIED':0,'GATE_SOURCE_FILES_MODIFIED':0,'ADAPTER_SOURCE_FILES_MODIFIED':0,'STOPPED_CAMPAIGN_MODIFIED':False,'LL_11_PRESERVED':True,'LESSONS_REGISTER_CHANGED':False,'BOOTSTRAP_INERT_TESTS_EXECUTED':0,'SYSTEM_LEVEL_PROBES_EXECUTED':0,'H77_02_PROBE_EXECUTED':False,'A15_EXECUTED':False,'A15_EXECUTION_AUTHORITY_ISSUED':False,'A15_CAPTURE_AUTHORITY_ISSUED':False,'BASELINE_AMENDED':False,'E1_ARTIFACTS_MODIFIED':0,'PRODUCTION_EFFECT':False})
check=subprocess.run(['git','diff','--check'],cwd=str(ROOT),capture_output=True,text=True);assert check.returncode==0,check.stdout+check.stderr
publish('git-diff-check.json',{'RESULT':'PASS','COMMAND':['git','diff','--check']})
binding=read(OUT/'grant-record-binding.json');record=ROOT/binding['FUTURE_RECORD_PATH'];envelope=read(record);decision=read(OUT/'project-owner-decision-provenance.json');body=envelope['CONTENT']
prereqs=['exact-subject-authentication.json','effective-governance-verification.json','pre-issuance-conflict-audit.json','prepublication-independent-validation.json','independent-persisted-record-verification.json','append-only-publication-evidence.json','four-seed-persisted-reconstruction.json','negative-control-results.json','preservation-audit.json','git-diff-check.json']
ref={'SCHEMA':'BOOTSTRAP-REPAIR-EFFECTIVE-GRANT-REFERENCE-94-1','GRANT_IDENTITY':envelope['IDENTITY'],'GRANT_RECORD_PIN':pin(record),'APPROVED_SUBJECT_IDENTITY':body['APPROVED_SUBJECT_IDENTITY'],'OWNER_DECISION_IDENTITY':decision['IDENTITY'],'GOVERNING_CHARTER_IDENTITY':body['GOVERNING_CHARTER_IDENTITY'],'EFFECTIVE_CHARTER_LIFECYCLE':body['EFFECTIVE_CHARTER_LIFECYCLE'],'REPAIR_GRANT_EFFECTIVE':True,'EFFECTIVE_BOUNDARY':'This separate no-overwrite publication after all ordered issuance, persisted read, four-seed, 24-negative and preservation checks; no backdating. Current source unchanged. Source repair requires a fresh construction guard; active tests remain independently gated.','ROOT_ENTRY_MAX_BYTES':207444,'ORDINARY_RECORD_MAX_BYTES':65536,'RESOURCE_LIMITS_UNCHANGED':True,'EXACT_SOURCE_ALLOWLIST':body['EXACT_SOURCE_ALLOWLIST'],'PRIOR_SOURCE_IDENTITIES':body['PRIOR_SOURCE_IDENTITIES'],'REPAIR_PHASE_PERMITTED':True,'REPAIR_CONSTRUCTION_ENTRY_READY_SNAPSHOT':True,'FRESH_ENTRY_GUARDS':body['CONSTRUCTION_ENTRY_PREDICATES'],'ACTIVE_INERT_TEST_READY':False,'TEST_ENTRY_PREDICATES':body['TEST_ENTRY_PREDICATES'],'SOURCE_REPAIR_PERFORMED':False,'BOOTSTRAP_INERT_TESTS_EXECUTED':0,'SYSTEM_LEVEL_PROBES_EXECUTED':0,'H77_02_PROBE_EXECUTED':False,'A15_EXECUTED':False,'A15_EXECUTION_AUTHORITY_ISSUED':False,'A15_CAPTURE_AUTHORITY_ISSUED':False,'NO_EXTRA_CAMPAIGN_OR_RETRY':True,'VERIFICATION_PINS':[pin(OUT/n) for n in prereqs],'INDEPENDENT_READER_PIN':pin(OUT/'verify_record.py'),'POWER_LOSS_DURABILITY_CLAIMED':False}
path=publish('effective-bootstrap-repair-grant-reference.json',ref)
post=subprocess.run(['/usr/bin/python3.8',str((OUT/'verify_record.py').relative_to(ROOT)),'--effective'],cwd=str(ROOT),capture_output=True,text=True,check=True);v=json.loads(post.stdout)
assert v['RECONSTRUCTION']['GRANT_EFFECTIVE'] and v['RECONSTRUCTION']['CONSTRUCTION_ENTRY_READY'] and not v['RECONSTRUCTION']['ACTIVE_INERT_TEST_READY']
publish('independent-effective-reference-verification.json',v)
print('GRANT_EFFECTIVE',envelope['IDENTITY']);print('CONSTRUCTION_SNAPSHOT_READY; ACTIVE_TESTS_BLOCKED; NO_SOURCE_MODIFICATION')
