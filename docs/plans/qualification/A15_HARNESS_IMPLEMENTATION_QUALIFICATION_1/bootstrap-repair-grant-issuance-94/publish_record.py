"""Approved documentary publication only. No source modification or testing."""
import hashlib,json,os,stat,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];OUT=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text())
def pin(p):return {'path':str(p.relative_to(ROOT)),'raw_sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def reader(*args):
 p=subprocess.run(['/usr/bin/python3.8',str((OUT/'verify_record.py').relative_to(ROOT)),*args],cwd=str(ROOT),text=True,capture_output=True,check=True);return json.loads(p.stdout)
def publish(name,value):
 target=OUT/name;raw=(json.dumps(value,indent=2,sort_keys=True,ensure_ascii=False)+'\n').encode()
 info=OUT.stat();assert info.st_uid==os.geteuid() and stat.S_IMODE(info.st_mode)==0o700 and not OUT.is_symlink()
 assert not target.exists() and not target.is_symlink(),target
 fd,tmp=tempfile.mkstemp(prefix='.grant-publication-',dir=str(OUT))
 try:
  with os.fdopen(fd,'wb') as f:
   f.write(raw);f.flush();os.fsync(f.fileno())
  os.link(tmp,str(target))  # Atomic no-overwrite; existing pathname never succeeds.
  os.unlink(tmp)
  directory=os.open(str(OUT),os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
  try:os.fsync(directory)
  finally:os.close(directory)
  readonly=os.open(str(target),os.O_RDONLY|os.O_NOFOLLOW)
  try:
   post=os.fstat(readonly);assert stat.S_ISREG(post.st_mode) and post.st_nlink==1 and stat.S_IMODE(post.st_mode)==0o600
   chunks=[]
   while True:
    data=os.read(readonly,4096)
    if not data:break
    chunks.append(data)
   assert b''.join(chunks)==raw
  finally:os.close(readonly)
 finally:
  if os.path.exists(tmp):os.unlink(tmp)  # Private incomplete temp only, never published target.
 return target
# Independent reader/negative suite and conflict scan precede issued publication.
audit=reader('--conflicts');publish('pre-issuance-conflict-audit.json',audit)
pre=reader('--candidate');publish('prepublication-independent-validation.json',pre)
envelope=read(OUT/'grant-candidate.json');binding=read(OUT/'grant-record-binding.json')
record=publish(Path(binding['FUTURE_RECORD_PATH']).name,envelope)
post=reader();assert post['RECONSTRUCTION']['GRANT_IDENTITY']==envelope['IDENTITY']
publish('independent-persisted-record-verification.json',post)
publish('append-only-publication-evidence.json',{'METHOD':'qualified prior Package71/90 full temp write+file fsync+link no-overwrite+unlink temp+directory fsync+readonly exact bytes','ATOMIC_NO_OVERWRITE':True,'FILE_FSYNC':True,'DIRECTORY_FSYNC':True,'READONLY_BYTES_MATCH':True,'PUBLISHED_TARGET_NEVER_REMOVED':True,'GENERAL_POWER_LOSS_ASSURANCE':False,'GRANT_RECORD_PIN':pin(record),'CONTENT_IDENTITY':post['RECONSTRUCTION']['GRANT_IDENTITY'],'SOURCE_OR_TEST_EFFECT':False})
print('GRANT_PERSISTED_INDEPENDENTLY_VERIFIED_NOT_YET_EFFECTIVE',post['RECONSTRUCTION']['GRANT_IDENTITY'])
