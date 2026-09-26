"""Launch only this authorized driver and its read-only status observer."""
import os,sys,subprocess,json,time
from pathlib import Path
O=Path(__file__).parent
fd=os.open(O/'EXECUTION_SESSION_STARTED.json',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
os.write(fd,json.dumps({'pid':os.getpid(),'wall_time':time.time(),'one_attempt':True,'automatic_retry':False}).encode());os.fsync(fd);os.close(fd)
with (O/'OPERATOR_MONITOR.log').open('x') as log:
 monitor=subprocess.Popen([sys.executable,'-B',str(O/'monitor.py')],stdout=log,stderr=subprocess.STDOUT)
 try:
  run=subprocess.run([sys.executable,'-B',str(O/'run.py')])
 finally:
  try:monitor.wait(timeout=60)
  except subprocess.TimeoutExpired:
   monitor.terminate();monitor.wait(timeout=10)
   (O/'MONITOR_STOPPED.json').write_text(json.dumps({'reason':'DRIVER_ENDED_WITHOUT_MONITOR_TERMINAL_CONVERGENCE','read_only_monitor_only':True}))
sys.exit(run.returncode)
