"""Read-only Linux instance observations. No launch, signals or socket requests."""
from pathlib import Path
import json
import os
import stat
from .context_projection import sha
from .supervisor_succession import require, sealed


def start(proc):
    fields=(proc/'stat').read_text().rsplit(') ',1)[1].split()
    return {'ppid':int(fields[1]),'start_ticks':int(fields[19])}


def process(pid):
    proc=Path('/proc')/str(pid);first=start(proc)
    fields={line.split(':',1)[0]:line.split(':',1)[1].split() for line in (proc/'status').read_text().splitlines() if ':' in line}
    uid=[int(x) for x in fields['Uid']];gid=[int(x) for x in fields['Gid']]
    require(len(set(uid))==len(set(gid))==1,'mixed real/effective/saved credentials')
    result={'pid':pid,**first,'boot_id':Path('/proc/sys/kernel/random/boot_id').read_text().strip(),
        'pid_namespace_inode':(proc/'ns/pid').stat().st_ino,
        'parent_start_ticks':start(Path('/proc')/str(first['ppid']))['start_ticks'],
        'uid':uid[0],'gid':gid[0],'groups':sorted(int(x) for x in fields['Groups'])}
    require(start(proc)==first,'process identity changed during observation')
    return result


def path_identity(path):
    p=Path(path);require(p.is_absolute() and p.resolve()==p and not p.is_symlink(),'noncanonical host path')
    s=p.stat();return {'path':str(p),'device':s.st_dev,'inode':s.st_ino}


def socket_identity(path,p):
    sock=Path(path);s=sock.lstat()
    require(stat.S_ISSOCK(s.st_mode),'socket absent/wrong type')
    proc=Path('/proc')/str(p['pid'])
    listeners=[]
    for line in (proc/'net/unix').read_text().splitlines()[1:]:
        parts=line.split()
        if len(parts)==8 and parts[7]==path and parts[3]=='00010000' and parts[4]=='0001':listeners.append(parts[6])
    require(len(listeners)==1,'missing/ambiguous listening socket')
    inode=listeners[0]
    links=[]
    for fd in (proc/'fd').iterdir():
        try: links.append(os.readlink(fd))
        except FileNotFoundError: pass
    require('socket:['+inode+']' in links,'listener not owned by instance')
    return {'path':path,'device':s.st_dev,'inode':s.st_ino,'uid':s.st_uid,'gid':s.st_gid,
        'mode':stat.S_IMODE(s.st_mode),'listener_pid':p['pid'],
        'listener_start_ticks':p['start_ticks'],'listener_inode':int(inode)}


def observe(expected):
    """Return freshly measured instance; caller compares the entire sealed value.

    Protocol is the qualified source/configuration contract, checked against exact
    source bytes, argv and the complete launch environment, not a READY response.
    """
    before=process(expected['process']['pid']);proc=Path('/proc')/str(before['pid'])
    exe={'path':str((proc/'exe').resolve()),'sha256':sha((proc/'exe').read_bytes()),
         'argv':(proc/'cmdline').read_bytes().rstrip(b'\0').replace(b'\0',b' ').decode()}
    workspace=path_identity(str((proc/'cwd').resolve()))
    cg=path_identity(expected['cgroup']['path'])
    unified=[l for l in (proc/'cgroup').read_text().splitlines() if l.startswith('0::')]
    require(len(unified)==1,'unified cgroup unavailable')
    cg['unified']=unified[0]
    cg['memberships']=(proc/'cgroup').read_text().strip()
    sock=socket_identity(expected['socket']['path'],before)
    impl={p:sha(Path(p).read_bytes()) for p in expected['implementation']}
    config=expected['protocol_configuration']
    environ={}
    for entry in (proc/'environ').read_bytes().split(b'\0'):
        if entry:
            k,v=entry.split(b'=',1);environ[k.decode()]=v.decode()
    require(environ==config['environment'],'protocol launch environment changed')
    require(config['protocol_version']==1 and config['socket_path']==sock['path'] and config['cgroup_path']==cg['path'],'protocol/configuration mismatch')
    require(process(before['pid'])==before,'PID reuse or process changed')
    body={k:v for k,v in expected.items() if k!='id'}
    body.update(process=before,executable=exe,workspace=workspace,cgroup=cg,socket=sock,implementation=impl)
    return sealed('SupervisorInstance',body)
