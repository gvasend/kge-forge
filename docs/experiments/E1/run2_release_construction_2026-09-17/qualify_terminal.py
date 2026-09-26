"""Bounded synthetic terminal/session probe; no supervisor, cgroup or host mutation."""
import json,os,pty,signal,subprocess,sys,tempfile,time
from pathlib import Path

def birth(pid):
    fields=Path('/proc/{}/stat'.format(pid)).read_text().rsplit(') ',1)[1].split()
    return {'pid':pid,'start_ticks':int(fields[19]),'session':int(fields[3]),'tty_nr':int(fields[4]),'state':fields[0]}

with tempfile.TemporaryDirectory(prefix='terminal-lifetime-fixture-') as d:
    receipt=Path(d)/'candidate.json'
    child="import os,time; from pathlib import Path; Path(%r).write_text(str(os.getpid())); time.sleep(20)" % str(receipt)
    operator,master=pty.fork()
    if operator==0:
        try:
            subprocess.Popen([sys.executable,'-c',child],start_new_session=True,
                stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,close_fds=True)
            time.sleep(20)
        finally: os._exit(0)
    candidate=None
    try:
        deadline=time.monotonic()+5
        while not receipt.exists() and time.monotonic()<deadline:time.sleep(.01)
        assert receipt.exists(),'synthetic candidate failed to start'
        candidate=int(receipt.read_text());before=birth(candidate)
        assert before['tty_nr']==0 and before['session']==candidate
        # Closing the operator PTY produces a genuine controlling-terminal HUP.
        os.close(master);master=None
        time.sleep(.2)
        after=birth(candidate)
        assert after['start_ticks']==before['start_ticks'] and after['state'] not in ('Z','X')
        print(json.dumps({'result':'PASS','scope':'SYNTHETIC_SESSION_DETACHMENT_ONLY',
            'before_terminal_close':before,'after_terminal_close':after,
            'real_service_launch_qualified':False,'real_supervisor_created':False},sort_keys=True))
    finally:
        if master is not None:os.close(master)
        for pid in (candidate,operator):
            if pid:
                try:os.kill(pid,signal.SIGTERM)
                except ProcessLookupError:pass
        try:os.waitpid(operator,0)
        except ChildProcessError:pass
