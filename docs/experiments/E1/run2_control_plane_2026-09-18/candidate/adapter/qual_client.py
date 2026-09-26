"""Read-only kernel observations and bounded socket calls for A2.1c."""
import json, os, socket, struct, sys, threading, time
from pathlib import Path

SOCKET='/tmp/a21m.sock'
BASE=Path('/sys/fs/cgroup/unified/kge-forge/executor')

def call(op, sid, **fields):
    request={'op':op,'scope_id':sid,**fields}
    data=json.dumps(request).encode()
    with socket.socket(socket.AF_UNIX) as sock:
        sock.connect(SOCKET)
        sock.sendall(struct.pack('!I',len(data))+data)
        header=sock.recv(4)
        size=struct.unpack('!I',header)[0]
        chunks=[]
        while sum(map(len,chunks))<size:
            chunks.append(sock.recv(size-sum(map(len,chunks))))
    return json.loads(b''.join(chunks))

def observe(sid, launcher, descendant, label):
    path=BASE/sid
    data={'label':label,'observed_ns':time.monotonic_ns(),
          'events':(path/'cgroup.events').read_text(),
          'procs':(path/'cgroup.procs').read_text().split(),
          'launcher_exists':Path(f'/proc/{launcher}').exists(),
          'descendant_exists':Path(f'/proc/{descendant}').exists()}
    for name,pid in (('launcher',launcher),('descendant',descendant)):
        proc=Path(f'/proc/{pid}')
        if proc.exists():
            data[name+'_cgroup']=(proc/'cgroup').read_text().splitlines()[-1]
            data[name+'_status']={line.split(':',1)[0]:line.split(':',1)[1].strip()
                                  for line in (proc/'status').read_text().splitlines()
                                  if line.startswith(('State:','PPid:','Uid:','Gid:'))}
    return data

def run(sid):
    log=[]; released=False; live=[]; stop=threading.Event()
    def monitor():
        path=BASE/sid/'cgroup.procs'
        while not stop.is_set():
            stamp=time.monotonic_ns()
            try:
                for raw in path.read_text().split():
                    pid=int(raw); proc=Path(f'/proc/{pid}/cgroup')
                    if proc.exists():
                        live.append({'observed_ns':stamp,'pid':pid,
                                     'cgroup':proc.read_text().splitlines()[-1]})
            except (OSError, ValueError): pass
            time.sleep(.0005)
    watcher=threading.Thread(target=monitor,daemon=True); watcher.start()
    spawn=call('qual_spawn',sid); stop.set(); watcher.join(timeout=1)
    log.append({'op':'qual_spawn','response':spawn})
    if not spawn.get('error'):
        before=[sample for sample in live if sample['pid']==spawn['launcher_pid']
                and sample['observed_ns']<spawn['payload_start_ns']]
        log.append({'live_launcher_samples_before_payload':before[:8],
                    'live_launcher_sample_count':len(before)})
    if spawn.get('error') or not spawn.get('admitted'):
        print(json.dumps(log,indent=2)); return 2
    launcher=spawn['launcher_pid']; descendant=spawn['descendant_pid']
    try:
        log.append(observe(sid,launcher,descendant,'after_result_launcher_exit'))
        log.append({'op':'quiescent_before_close','response':call('quiescent',sid)})
        log.append({'op':'close','response':call('close',sid)})
        log.append(observe(sid,launcher,descendant,'closed_with_survivor'))
        log.append({'op':'quiescent_while_populated','response':call('quiescent',sid)})
        late={'pid':descendant}
        log.append({'op':'late_admit','response':call('admit',sid,**late)})
        log.append({'op':'replayed_late_admit','response':call('admit',sid,**late)})
        log.append({'op':'reopen_create','response':call('create',sid)})
        log.append({'op':'release','response':call('qual_release',sid)}); released=True
        for _ in range(50):
            sample=observe(sid,launcher,descendant,'drain')
            if 'populated 0' in sample['events']:
                log.append(sample); break
            time.sleep(.1)
        else: log.append(sample)
        log.append({'op':'final_quiescent','response':call('quiescent',sid)})
        log.append(observe(sid,launcher,descendant,'after_final_decision'))
    finally:
        if not released:
            try: log.append({'op':'emergency_release','response':call('qual_release',sid)})
            except Exception as exc: log.append({'emergency_release_error':str(exc)})
        print(json.dumps(log,indent=2))
    return 0

if __name__=='__main__': raise SystemExit(run(sys.argv[1]))
