"""Read-only candidate checks; exactly one status request, no scope operations."""
import hashlib,json,os,socket,struct,time
from pathlib import Path
from adapter.supervisor_observation import process,socket_identity,path_identity
sha=lambda b:hashlib.sha256(b).hexdigest()
root=Path('/home/gvasend/app/kge-forge')
out=root/'docs/experiments/E1/run2_live_supervisor_qualification_2026-09-17/POST_CLOSURE_OBSERVATIONS.json'
planpath=root/'docs/experiments/E1/run2_nonhost_closure_2026-09-17/host_package/LAUNCH_SPEC.json'
plan=json.loads(planpath.read_bytes())
r={'observed_at_unix_ns':time.time_ns(),'checks':{},'errors':{}}
def check(name,fn):
 try:r['checks'][name]=fn()
 except Exception as e:r['errors'][name]=type(e).__name__+': '+str(e)
p=process(1465900);r['process']=p
check('credentials',lambda:{'pass':(p['uid'],p['gid'],p['groups'])==(plan['uid'],plan['gid'],plan['supplementary_groups'])})
proc=Path('/proc/1465900')
check('executable',lambda:{'path':os.readlink(proc/'exe'),'sha256':sha((proc/'exe').read_bytes()),'pass':os.readlink(proc/'exe')==plan['interpreter'] and sha((proc/'exe').read_bytes())==plan['interpreter_sha256']})
check('argv',lambda:{'observed':(proc/'cmdline').read_bytes().rstrip(b'\0').decode().split('\0'),'pass':(proc/'cmdline').read_bytes().rstrip(b'\0').decode().split('\0')==plan['argv']})
check('workspace',lambda:{'observed':path_identity(os.readlink(proc/'cwd')),'pass':os.readlink(proc/'cwd')==plan['workspace']})
check('cgroup',lambda:{'identity':path_identity(plan['cgroup']),'memberships':(proc/'cgroup').read_text(),'pass':'0::/kge-forge/executor' in (proc/'cgroup').read_text().splitlines()})
check('environment',lambda:{'pass':dict(x.decode().split('=',1) for x in (proc/'environ').read_bytes().split(b'\0') if x)==plan['environment']})
check('implementation',lambda:{'files':len(plan['implementation']),'mismatches':[k for k,v in plan['implementation'].items() if sha(Path(k).read_bytes())!=v]})
check('launch_spec',lambda:{'sha256':sha(planpath.read_bytes()),'pass':sha(planpath.read_bytes())=='f9b79b3ac85eb5cbb73d0209cf034c041236dd6519275b6529f139e5b322d309'})
check('frozen_launcher',lambda:{'sha256':sha(Path(plan['host_launcher']['path']).read_bytes()),'pass':sha(Path(plan['host_launcher']['path']).read_bytes())==plan['host_launcher']['sha256']})
check('socket',lambda:socket_identity(plan['socket'],p))
check('parent_cmdline',lambda:(Path('/proc')/str(p['ppid'])/'cmdline').read_bytes().rstrip(b'\0').decode().split('\0'))
check('S2_absent',lambda:not Path('/proc/1098552').exists())
check('S1_absent',lambda:not Path('/proc/57950').exists())
def supervisors():
 found=[];denied=[]
 for d in Path('/proc').iterdir():
  if not d.name.isdigit():continue
  try:argv=(d/'cmdline').read_bytes().split(b'\0')
  except FileNotFoundError:continue
  except PermissionError:denied.append(int(d.name));continue
  if b'adapter.supervisor_server' in argv:found.append(int(d.name))
 return {'pids':sorted(found),'unreadable_pids':denied}
check('supervisor_process_inventory',supervisors)
audit=Path('/tmp/a21m.sock.supervisor-audit.jsonl')
check('supervisor_audit_before',lambda:sha(audit.read_bytes()))
def status():
 with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as s:
  s.settimeout(3);s.connect(plan['socket'])
  peer=struct.unpack('3i',s.getsockopt(socket.SOL_SOCKET,socket.SO_PEERCRED,12))
  if peer!=(1465900,1000,1000):raise ValueError('unexpected peer '+repr(peer))
  def recv(n):
   b=b''
   while len(b)<n:
    x=s.recv(n-len(b))
    if not x:raise ValueError('truncated frame')
    b+=x
   return b
  payload=b'{"op":"status"}';s.sendall(struct.pack('!I',len(payload))+payload)
  size=struct.unpack('!I',recv(4))[0]
  if size>65536:raise ValueError('oversized response')
  result=json.loads(recv(size))
  return {'peer_pid_uid_gid':list(peer),'response':result,'pass':result=={'status':'READY'},'requests':1,'operation':'status'}
check('live_status',status)
check('supervisor_audit_after',lambda:sha(audit.read_bytes()))
import subprocess
check('service',lambda:subprocess.run(['/bin/systemctl','show','kge-forge-supervisor-run2.service','--property=MainPID,ActiveState,SubState,User,Group,Restart,StandardInput,StandardOutput,StandardError,FragmentPath,DropInPaths,InvocationID,ExecMainStartTimestampMonotonic'],capture_output=True,text=True,timeout=5).stdout)
check('stable_process_birth',lambda:process(1465900)==p)
check('stable_socket',lambda:socket_identity(plan['socket'],p)==r['checks'].get('socket'))
r['qualification_limit']='Root-owned candidate and launch receipts unavailable: no SupervisorInstanceId recomputation or launch-time provenance validation.'
with out.open('x') as f:json.dump(r,f,sort_keys=True,indent=2);f.write('\n')
print(json.dumps(r,indent=2))
