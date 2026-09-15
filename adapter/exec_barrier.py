"""Supervisor-owned start barrier; exec Bubblewrap only after cgroup admission."""
import os, sys

BWRAP='/usr/bin/bwrap'

def run(root, argv):
    if not argv or sys.stdin.buffer.read(1)!=b'1': return 2
    flags=['--die-with-parent','--unshare-pid','--new-session','--proc','/proc',
           '--dev','/dev','--bind',root,'/scope','--chdir','/scope',
           '--ro-bind','/usr','/usr','--ro-bind','/bin','/bin',
           '--ro-bind','/lib','/lib','--ro-bind','/lib64','/lib64','--unshare-net']
    # The payload must not inherit supervisor or engineering-agent environment.
    os.execve(BWRAP,[BWRAP,*flags,*argv],{'PATH':'/usr/bin:/bin','LANG':'C.UTF-8'})

if __name__=='__main__': raise SystemExit(run(sys.argv[1],sys.argv[2:]))
