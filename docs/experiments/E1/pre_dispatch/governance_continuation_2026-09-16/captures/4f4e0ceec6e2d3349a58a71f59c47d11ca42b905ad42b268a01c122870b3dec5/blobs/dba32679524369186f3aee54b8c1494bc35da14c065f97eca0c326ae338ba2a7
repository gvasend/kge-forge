"""Bounded A2.1c payload: report a result, then leave a detached descendant held."""
import json, os, sys, time

def run(hold_fd):
    if sys.stdin.buffer.read(1) != b'1': return 2
    start = time.monotonic_ns()
    r, w = os.pipe()
    child = os.fork()
    if child == 0:
        os.close(r)
        os.setsid()
        session_pid = os.getpid()
        grandchild = os.fork()
        if grandchild == 0:
            os.close(w)
            os.close(0); os.close(1); os.close(2)
            # The supervisor releases this hold; a bounded alarm avoids leaks.
            import signal
            signal.alarm(45)
            os.read(hold_fd, 1)
            os._exit(0)
        os.write(w, json.dumps({'session_pid':session_pid,
                                'descendant_pid':grandchild,
                                'descendant_created_ns':time.monotonic_ns()}).encode()+b'\n')
        os.close(w)
        os._exit(0)
    os.close(w)
    details = json.loads(os.read(r, 4096))
    os.close(r)
    os.waitpid(child, 0)
    print(json.dumps({'result':'ok','payload_start_ns':start,
                      'result_ns':time.monotonic_ns(), **details}), flush=True)
    return 0

if __name__ == '__main__': raise SystemExit(run(int(sys.argv[1])))
