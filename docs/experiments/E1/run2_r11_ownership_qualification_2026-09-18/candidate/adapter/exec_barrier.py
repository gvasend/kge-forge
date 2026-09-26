"""Supervisor-owned start barrier; exec Bubblewrap only after cgroup admission."""
import os, sys, hashlib, json
from pathlib import Path

BWRAP='/usr/bin/bwrap'

def run(root, argv):
    if not argv or sys.stdin.buffer.read(1)!=b'1': return 2
    expected=None
    if argv[0].startswith('--gei-policy-sha256='):
        expected=argv[0].split('=',1)[1]; argv=argv[1:]
    flags=['--die-with-parent','--unshare-pid','--new-session','--proc','/proc',
           '--dev','/dev','--bind',root,'/scope','--chdir','/scope',
           '--ro-bind','/usr','/usr','--ro-bind','/bin','/bin',
           '--ro-bind','/lib','/lib','--ro-bind','/lib64','/lib64','--unshare-net']
    environment={'PATH':'/usr/bin:/bin','LANG':'C.UTF-8'}
    if expected is not None or (Path(root)/'.gei-runtime.json').exists():
        from .runnable_profile import launcher_policy, CONTEXT, POLICY
        if expected is None or hashlib.sha256((Path(root)/POLICY).read_bytes()).hexdigest()!=expected:
            raise ValueError('controller runtime policy seal mismatch')
        policy=launcher_policy(root,argv)
        environment=policy['specification']['environment']
        flags+=['--ro-bind',str(Path(root)/CONTEXT),'/scope/'+CONTEXT,
                '--ro-bind',str(Path(root)/POLICY),'/scope/'+POLICY]
        for mount in policy['acceptance']['repository_mounts']:
            flags+=['--ro-bind',mount['source'],mount['destination']]
        # The supervisor's first-line protocol must not depend on tests printing
        # stdout (unittest normally writes to stderr). This is a start receipt,
        # never terminal success; exit and authoritative quiescence still gate it.
        print(json.dumps({'kind':'governed_launch_receipt',
            'runtime_policy_sha256':hashlib.sha256((Path(root)/POLICY).read_bytes()).hexdigest()}),flush=True)
    # The payload must not inherit supervisor or engineering-agent environment.
    os.execve(BWRAP,[BWRAP,*flags,*argv],environment)

if __name__=='__main__': raise SystemExit(run(sys.argv[1],sys.argv[2:]))
