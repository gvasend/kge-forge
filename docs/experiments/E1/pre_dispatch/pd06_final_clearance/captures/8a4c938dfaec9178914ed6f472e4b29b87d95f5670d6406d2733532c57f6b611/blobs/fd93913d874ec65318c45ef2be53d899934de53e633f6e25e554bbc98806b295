from pathlib import Path
import json,subprocess,hashlib,sys
sys.path.insert(0,'/home/gvasend/app/kge-forge')
from adapter.tests.test_runnable_profile import live
from adapter.recovery_ledger import _observe,CGROUP_BASE
out=Path('/tmp/pd05-g5-live-final-v4-20260916')
r=live(out)
scopes=[r['first'][0]['data']['scope_id'],r['second']['data']['scope_id']]
found=[]
for line in subprocess.check_output(['ps','-eo','pid=,ppid=,uid=,args='],text=True).splitlines():
 parts=line.strip().split(None,3)
 if len(parts)==4 and parts[3].endswith('-m adapter.supervisor_server /tmp/a21m.sock'):
  pid=parts[0];exe=Path('/proc')/pid/'exe'
  found.append({'pid':int(pid),'ppid':int(parts[1]),'uid':int(parts[2]),'argv':parts[3],
   'exe':str(exe.resolve()),'exe_sha256':hashlib.sha256(exe.read_bytes()).hexdigest(),
   'cwd':str((Path('/proc')/pid/'cwd').resolve()),'cgroup':(Path('/proc')/pid/'cgroup').read_text().strip()})
s=Path('/tmp/a21m.sock').stat()
events=[json.loads(line) for line in Path('/tmp/a21m.sock.supervisor-audit.jsonl').read_text().splitlines() if any(sid in line for sid in scopes)]
receipt={'supervisor':found,'socket':{'path':'/tmp/a21m.sock','mode':oct(s.st_mode&0o777),'uid':s.st_uid,'gid':s.st_gid},
 'kernel_after':{sid:_observe(CGROUP_BASE/sid) for sid in scopes},'supervisor_events':events}
assert len(found)==1 and all(v['members']==[] and v['populated']==0 for v in receipt['kernel_after'].values())
(out/'HOST_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'result':r['result'],'evidence':str(out),'scopes':scopes,'supervisor_pid':found[0]['pid']}))
