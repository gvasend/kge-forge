"""Read only the enumerated S3 receipts/package. JSON to stdout; no mutations."""
import base64,hashlib,json,os,stat,time
from pathlib import Path
assert os.geteuid()==0,'Host root is needed only to read original authority evidence'
base=Path('/var/lib/kge-forge-supervisor-run2')
paths=[base/'S3'/n for n in ('CANDIDATE_S3.json','HOST_LAUNCH.json','PLACEMENT_BEFORE_DROP.json','PRELAUNCH.json','STALE_SOCKET_REMOVAL.json')]
paths += [base/n for n in ('host_launch.py','LAUNCH_SPEC.json','HOST_LAUNCH_AUTHORIZATION.json')]
paths += [Path('/etc/systemd/system/kge-forge-supervisor-run2.service')]
rows=[]
for p in paths:
 try:
  fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
  try:
   before=os.fstat(fd)
   assert stat.S_ISREG(before.st_mode) and before.st_uid==0 and before.st_nlink==1,str(p)
   with os.fdopen(os.dup(fd),'rb') as f:data=f.read(4*1024*1024+1)
   assert len(data)<=4*1024*1024,'bounded export exceeded'
   after=os.fstat(fd)
   assert (before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns)==(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns),'receipt changed'
  finally:os.close(fd)
  rows.append({'path':str(p),'sha256':hashlib.sha256(data).hexdigest(),'base64':base64.b64encode(data).decode(),
   'uid':before.st_uid,'gid':before.st_gid,'mode':stat.S_IMODE(before.st_mode),'device':before.st_dev,'inode':before.st_ino,'size':before.st_size})
 except FileNotFoundError:
  assert p.name=='STALE_SOCKET_REMOVAL.json','required receipt absent: '+str(p)
  rows.append({'path':str(p),'absent':True})
p=Path('/proc/1465890');fields=(p/'stat').read_text().rsplit(') ',1)[1].split()
parent={'pid':1465890,'ppid':int(fields[1]),'session_id':int(fields[3]),'tty_nr':int(fields[4]),'start_ticks':int(fields[19]),'status':{}}
for line in (p/'status').read_text().splitlines():
 if line.split(':',1)[0] in ('Uid','Gid','Groups'):parent['status'][line.split(':',1)[0]]=line.split(':',1)[1].split()
env=dict(x.split(b'=',1) for x in (p/'environ').read_bytes().split(b'\0') if x)
parent['INVOCATION_ID']=env.get(b'INVOCATION_ID',b'').decode()
body={'schema':'S3-ROOT-READONLY-EXPORT-1','observed_at_unix_ns':time.time_ns(),'export_euid':os.geteuid(),'files':rows,'parent':parent,
 'process_exit_receipt_exists':(base/'S3/PROCESS_EXIT.json').exists(),'originals_modified':False}
encoded=json.dumps(body,sort_keys=True,separators=(',',':')).encode()
print(json.dumps({'body':body,'body_sha256':hashlib.sha256(encoded).hexdigest()},sort_keys=True))
