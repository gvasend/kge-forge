"""PROPOSED HOST-OPERATOR PROCEDURE. Never run from the governed environment.

Install root-owned with exact pinned plan and separate genuine Architect/host
launch authorization. This starts a process but cannot authorize succession,
select a controller catalog, activate E1, or acquire E1 ownership.
"""
import fcntl,hashlib,json,os,stat,sys,time,subprocess
from pathlib import Path

BASE=Path('/var/lib/kge-forge-supervisor-run2')
CG=Path('/sys/fs/cgroup/unified/kge-forge/executor')
SOCKET=Path('/tmp/a21m.sock')

def canonical(v):return json.dumps(v,sort_keys=True,separators=(',',':'))
def sha(b):return hashlib.sha256(b).hexdigest()
def require(v,m):
    if not v:raise RuntimeError(m)
def seal(kind,v):return {**v,'id':kind+'-sha256:'+sha(canonical(v).encode())}
def root_file(p):
    p=Path(p);require(p.resolve()==p,'symlink path')
    for parent in (p.parent,*p.parents):
        st=parent.stat();require(st.st_uid==0 and not st.st_mode&0o022,'non-root/writable authority directory')
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        st=os.fstat(fd);require(stat.S_ISREG(st.st_mode) and st.st_uid==0 and not st.st_mode&0o077 and st.st_nlink==1,'unsafe host authority file')
        with os.fdopen(os.dup(fd),'rb') as f:return f.read()
    finally:os.close(fd)
def write(p,v):
    fd=os.open(p,os.O_CREAT|os.O_EXCL|os.O_WRONLY|os.O_NOFOLLOW,0o600)
    with os.fdopen(fd,'w') as f:f.write(canonical(v));f.flush();os.fsync(f.fileno())
    fd=os.open(Path(p).parent,os.O_RDONLY|os.O_DIRECTORY)
    try:os.fsync(fd)
    finally:os.close(fd)
def start(pid):
    p=Path('/proc')/str(pid);s=(p/'stat').read_text().rsplit(') ',1)[1].split()
    return {'ppid':int(s[1]),'start_ticks':int(s[19])}
def proc(pid):
    p=Path('/proc')/str(pid);first=start(pid)
    fields={x.split(':',1)[0]:x.split(':',1)[1].split() for x in (p/'status').read_text().splitlines() if ':' in x}
    uid=list(map(int,fields['Uid']));gid=list(map(int,fields['Gid']))
    require(len(set(uid))==len(set(gid))==1,'mixed credentials')
    result={'pid':pid,**first,'boot_id':Path('/proc/sys/kernel/random/boot_id').read_text().strip(),
        'pid_namespace_inode':(p/'ns/pid').stat().st_ino,'parent_start_ticks':start(first['ppid'])['start_ticks'],
        'uid':uid[0],'gid':gid[0],'groups':sorted(map(int,fields['Groups']))}
    require(start(pid)==first,'process observation raced');return result

def path_identity(p):
    p=Path(p);require(p.resolve()==p and not p.is_symlink(),'noncanonical host location')
    st=p.stat();return {'path':str(p),'device':st.st_dev,'inode':st.st_ino}
def listeners():
    result=[]
    for l in Path('/proc/net/unix').read_text().splitlines()[1:]:
        x=l.split()
        if len(x)==8 and x[7]==str(SOCKET) and x[3]=='00010000':result.append(x[6])
    return result

def preflight(plan):
    require(not Path('/proc/57950').exists(),'historical PID exists: reconcile, never reinterpret')
    require(not Path('/proc/1098552').exists(),'prior S2 PID exists: independently reconcile')
    for p in Path('/proc').iterdir():
        if not p.name.isdigit():continue
        try:cmd=(p/'cmdline').read_bytes().split(b'\0')
        except FileNotFoundError:continue
        require(b'adapter.supervisor_server' not in cmd,'existing supervisor process: stop')
    require(not listeners(),'existing supervisor listener: stop')
    require(CG.resolve()==CG and CG.is_dir(),'delegated subtree missing')
    require((CG/'cgroup.procs').read_text().strip()=='','unaccounted executor-parent process')
    observed={}
    for scope in sorted(CG.glob('scope-*')):
        dirs=[scope];members=[]
        for d in dirs:
            require(not d.is_symlink(),'scope symlink')
            dirs.extend(x for x in d.iterdir() if x.is_dir() and not x.is_symlink())
            members.extend((d/'cgroup.procs').read_text().split())
            require(len(dirs)<=1024,'scope tree unbounded')
        events=dict(l.split() for l in (scope/'cgroup.events').read_text().splitlines())
        require(not members and events.get('populated')=='0','active/uncertain old scope: stop')
        observed[scope.name]={'members':[],'populated':0,'directories':len(dirs)}
    audit=Path('/tmp/a21m.sock.supervisor-audit.jsonl')
    require(audit.is_file() and not audit.is_symlink(),'supervisor recovery history missing')
    for l in audit.read_bytes().splitlines():json.loads(l)
    require(sha(audit.read_bytes())==plan['prelaunch_supervisor_audit_sha256'],'recovery history changed; reauthorize observation')
    cache=Path(plan['environment']['PYTHONPYCACHEPREFIX'])
    require(cache==Path('/var/cache/kge-forge-supervisor-run2/S3') and cache.resolve()==cache,'unapproved bytecode cache')
    st=cache.stat();require(st.st_uid==0 and not st.st_mode&0o022 and not any(cache.iterdir()),'bytecode cache must be root-owned and empty')
    for p,h in plan['implementation'].items():require(sha(Path(p).read_bytes())==h,'implementation mismatch: '+p)
    require(sha(Path(plan['interpreter']).read_bytes())==plan['interpreter_sha256'],'interpreter mismatch')
    return {'scope_observations':observed,'supervisor_audit_sha256':sha(audit.read_bytes()),'process_absent':True,'listener_absent':True}

def lifetime(plan):
    require(os.getppid()==1,'system-manager parent required')
    require(os.getsid(0)==os.getpid(),'independent service session required')
    require(all(not os.isatty(fd) for fd in (0,1,2)),'terminal descriptor forbidden')
    require(int(Path('/proc/self/stat').read_text().rsplit(') ',1)[1].split()[4])==0,'controlling terminal forbidden')
    unit=Path('/etc/systemd/system/kge-forge-supervisor-run2.service')
    # Unit is public configuration; authority spec and authorizations stay 0600.
    require(unit.resolve()==unit and unit.stat().st_uid==0 and not unit.stat().st_mode&0o022,'unsafe service unit')
    require(sha(unit.read_bytes())==plan['host_lifetime']['unit_sha256'],'unapproved service unit')
    fields=('MainPID','User','Group','Restart','StandardInput','StandardOutput','StandardError','FragmentPath','DropInPaths','InvocationID')
    out=subprocess.check_output(['/bin/systemctl','show','kge-forge-supervisor-run2.service',
        '--property='+','.join(fields)],env={'PATH':'/usr/bin:/bin','LANG':'C'},timeout=5).decode()
    props=dict(line.split('=',1) for line in out.splitlines() if '=' in line)
    require(props['MainPID']==str(os.getpid()) and props['User']=='root' and props['Group']=='root', 'wrong service identity')
    require(props['DropInPaths']=='' and len(props['InvocationID'])==32 and props['InvocationID']==os.environ.get('INVOCATION_ID'),'unbound service invocation/drop-in')
    require(props['Restart']=='no' and props['StandardInput']=='null' and
        props['StandardOutput']==props['StandardError']=='journal' and props['FragmentPath']==str(unit), 'unapproved service lifecycle')
    return {'schema':'SUPERVISOR-HOST-LIFETIME-1','properties':props,
        'unit_sha256':sha(unit.read_bytes()),'service_invocation_id':os.environ.get('INVOCATION_ID'),
        'session_id':os.getsid(0),'parent':{'pid':1,**start(1)},'terminal_independent':True}

def main():
    require(os.getuid()==os.geteuid()==0,'host root operator required')
    require(len(sys.argv)==3,'usage: host_launch.py LAUNCH_SPEC.json HOST_LAUNCH_AUTHORIZATION.json')
    spec_bytes=root_file(sys.argv[1]);plan=json.loads(spec_bytes)
    auth_bytes=root_file(sys.argv[2]);auth=json.loads(auth_bytes)
    require(auth['decision']=='AUTHORIZE_HOST_SUPERVISOR_LAUNCH' and auth['authority']=='Architect','actual Architect launch authority required')
    require(auth['authorization_id'] and auth['host_operator_authorization_id'],'authorization identities missing')
    require(auth['launch_spec_sha256']==sha(spec_bytes) and auth['launcher_sha256']==sha(root_file(Path(__file__).resolve())),'unapproved launch bytes')
    require(auth['predecessor_id']==plan['predecessor_id'] and auth['runtime_binding']==plan['runtime_binding'],'launch ancestry mismatch')
    require(plan['status']=='AUTHORIZED_FOR_HOST_LAUNCH','proposal is not launch authority')
    require(plan['runtime_binding']['OperationalContextId'] and auth['qualification_acceptance_id'],'qualified operational applicability required')
    require(plan['uid']==plan['gid']==1000 and plan['workspace']=='/home/gvasend/app/kge-forge','wrong runtime authority')
    require(plan['cgroup']==str(CG) and plan['socket']==str(SOCKET),'wrong delegated/socket boundary')
    lifetime_evidence=lifetime(plan)
    lock=os.open(BASE/'host-launch.lock',os.O_CREAT|os.O_RDWR|os.O_NOFOLLOW,0o600)
    st=os.fstat(lock);require(st.st_uid==0 and stat.S_ISREG(st.st_mode) and not st.st_mode&0o077 and st.st_nlink==1,'unsafe launch lock')
    fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    evidence=preflight(plan)
    evidence['host_lifetime']=lifetime_evidence
    run=BASE/'S3';run.mkdir(mode=0o700) # exclusive one-shot; replay never starts another child
    write(run/'PRELAUNCH.json',{'authority':'HOST_OPERATOR','authorization_sha256':sha(auth_bytes),
        'launch_spec_sha256':sha(spec_bytes),'observed_at':time.time_ns(),'evidence':evidence,'parent':proc(os.getpid())})
    if SOCKET.exists():
        st=SOCKET.lstat();require(stat.S_ISSOCK(st.st_mode) and st.st_uid==1000 and not listeners(),'stale socket not safely attributable')
        require(auth.get('remove_verified_stale_socket') is True,'stale socket unlink not authorized')
        write(run/'STALE_SOCKET_REMOVAL.json',{'path':str(SOCKET),'device':st.st_dev,'inode':st.st_ino,'uid':st.st_uid,'mode':stat.S_IMODE(st.st_mode)})
        SOCKET.unlink()
    require(not SOCKET.exists() and not listeners(),'socket race before launch')
    read_fd,write_fd=os.pipe();pid=os.fork()
    if pid==0:
        try:
            os.close(read_fd)
            # Root child enters delegation BEFORE any credential reduction.
            fd=os.open(CG/'cgroup.procs',os.O_WRONLY|os.O_NOFOLLOW)
            try:os.write(fd,str(os.getpid()).encode())
            finally:os.close(fd)
            membership=Path('/proc/self/cgroup').read_text()
            require('0::/kge-forge/executor' in membership.splitlines(),'root placement failed')
            os.write(write_fd,canonical({'pid':os.getpid(),'uid_before_drop':os.getuid(),'cgroup_before_drop':membership}).encode())
            os.close(write_fd);os.setgroups([]);os.setgid(1000);os.setuid(1000)
            require(os.getuid()==os.geteuid()==1000 and os.getgid()==os.getegid()==1000,'credential reduction failed')
            os.chdir(plan['workspace']);os.umask(0o077)
            os.execve(plan['interpreter'],plan['argv'],plan['environment'])
        except BaseException:os._exit(111)
    os.close(write_fd);placement=os.read(read_fd,65536);os.close(read_fd)
    require(placement,'child placement receipt missing; stop and reconcile')
    write(run/'PLACEMENT_BEFORE_DROP.json',json.loads(placement))
    for _ in range(100):
        dead,status=os.waitpid(pid,os.WNOHANG)
        require(dead==0,'candidate exited; no succession')
        if SOCKET.exists() and len(listeners())==1:break
        time.sleep(.1)
    require(SOCKET.exists() and len(listeners())==1,'candidate not ready; no succession, host reconciliation required')
    p=proc(pid);base=Path('/proc')/str(pid);st=SOCKET.lstat();inode=listeners()[0]
    require('socket:['+inode+']' in [os.readlink(fd) for fd in (base/'fd').iterdir()],'listener is not candidate')
    cg=path_identity(CG);cg['memberships']=(base/'cgroup').read_text().strip();cg['unified']=next(x for x in cg['memberships'].splitlines() if x.startswith('0::'))
    executable={'path':str((base/'exe').resolve()),'sha256':sha((base/'exe').read_bytes()),'argv':(base/'cmdline').read_bytes().rstrip(b'\0').replace(b'\0',b' ').decode()}
    implementation={path:sha(Path(path).read_bytes()) for path in plan['implementation']}
    environ={k.decode():v.decode() for k,v in (x.split(b'=',1) for x in (base/'environ').read_bytes().split(b'\0') if x)}
    require(implementation==plan['implementation'] and environ==plan['environment'],'startup source/configuration changed')
    require(p['uid']==p['gid']==1000 and p['groups']==[] and cg['unified']=='0::/kge-forge/executor','wrong runtime placement/credentials')
    require(st.st_uid==st.st_gid==1000 and stat.S_IMODE(st.st_mode)==0o600,'wrong socket credentials')
    require(executable['path']==plan['interpreter'] and executable['sha256']==plan['interpreter_sha256'] and executable['argv']==' '.join(plan['argv']),'wrong executable/argv')
    sock={'path':str(SOCKET),'device':st.st_dev,'inode':st.st_ino,'uid':st.st_uid,'gid':st.st_gid,'mode':stat.S_IMODE(st.st_mode),
        'listener_pid':pid,'listener_start_ticks':p['start_ticks'],'listener_inode':int(inode)}
    body={'schema':'SUPERVISOR-INSTANCE-1','process':p,'executable':executable,'implementation':implementation,
        'workspace':path_identity(plan['workspace']),'cgroup':cg,'socket':sock,
        'protocol_configuration':plan['protocol_configuration'],'runtime_binding':plan['runtime_binding']}
    config={k:body[k] for k in ('executable','implementation','workspace','cgroup','protocol_configuration')}
    config.update(uid=p['uid'],gid=p['gid'],groups=p['groups'],socket={k:sock[k] for k in ('path','uid','gid','mode')})
    host={'schema':'SUPERVISOR-HOST-LAUNCH-1','host_lifetime':lifetime_evidence,'authority':'HOST_OPERATOR','authorized_launch':True,
        'runtime_binding':plan['runtime_binding'],'process':p,'configuration':config,
        'parent_start_identity':{'pid':p['ppid'],'boot_id':p['boot_id'],'start_ticks':p['parent_start_ticks']},
        'command_sha256':sha(canonical({'argv':plan['argv'],'environment':plan['environment'],'launcher_sha256':auth['launcher_sha256']}).encode()),
        'operator_authorization_id':auth['host_operator_authorization_id'],'architect_launch_authorization_id':auth['authorization_id'],
        'delegated_before_credentials_dropped':True,'runtime_uid':1000,'runtime_gid':1000,
        'launch_spec_sha256':sha(spec_bytes),'launcher_sha256':auth['launcher_sha256'],'observed_at_unix_ns':time.time_ns(),
        'clock_ticks_per_second':os.sysconf('SC_CLK_TCK'),'boot_time_seconds':next(int(x.split()[1]) for x in Path('/proc/stat').read_text().splitlines() if x.startswith('btime '))}
    require(proc(pid)==p,'birth identity changed before evidence commit')
    write(run/'HOST_LAUNCH.json',host)
    # Content ID uses canonical object bytes, not pretty-print or trailing newline.
    body['host_launch']='sha256:'+sha(canonical(host).encode())
    candidate=seal('SupervisorInstance',body);write(run/'CANDIDATE_S3.json',candidate)
    print(canonical({'candidate':candidate['id'],'evidence_directory':str(run),'succession_authorized':False,'E1_activation':False}),flush=True)
    # Keep parent identity and exclusive host-launch lock alive. No controller work.
    _,status=os.waitpid(pid,0);write(run/'PROCESS_EXIT.json',{'pid':pid,'wait_status':status,'observed_at_unix_ns':time.time_ns()})

if __name__=='__main__':main()
