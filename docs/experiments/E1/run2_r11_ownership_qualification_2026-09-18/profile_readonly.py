"""Non-authorizing bounded profiling of unchanged authority reconstruction."""
import cProfile,pstats,json,sys,time,signal
from pathlib import Path
O=Path(__file__).parent;sys.path.insert(0,'/tmp/forge-r10-transition-jxppjwou')
from adapter.controller_authority_store import ControllerAuthorityStore
from adapter.authority_bootstrap import reconstruct_authorization
from adapter.context_projection import canonical,sha,derive
from adapter.operator_projection import project
pin=json.loads((O.parent/'run2_r10_dispatch_2026-09-18/CURRENT_PIN.json').read_bytes())
b=Path(pin['path']).read_bytes();assert sha(b)==pin['sha256'];pub=json.loads(b)
store=ControllerAuthorityStore(**pub['selected_store']);measurements=[]
def measure(name,fn):
 profiler=cProfile.Profile();begin=time.monotonic();wall=time.time()
 def alarm(*_):raise TimeoutError('120 second hard qualification phase budget')
 signal.signal(signal.SIGALRM,alarm);signal.alarm(120)
 try:
  profiler.enable();result=fn();profiler.disable()
 finally:
  profiler.disable();signal.alarm(0)
  stats=pstats.Stats(profiler)
  functions=[{'file':str(k[0]),'line':k[1],'function':k[2],'primitive_calls':v[0],'calls':v[1],'self_seconds':v[2],'cumulative_seconds':v[3]} for k,v in stats.stats.items()]
  row={'schema':'NON_AUTHORIZING_TIMING_OBSERVATION-1','sequence':len(measurements)+1,'name':name,'monotonic_start':begin,'wall_start':wall,'seconds':time.monotonic()-begin,'profiled':True,'functions':sorted(functions,key=lambda x:x['cumulative_seconds'],reverse=True)[:35]}
  row.update(soft_exceeded=row['seconds']>=30,hard_exceeded=row['seconds']>=120)
  measurements.append(row);(O/'READONLY_TIMING.json').write_text(canonical(measurements))
 return result
try:
 with store.session():
  a=measure('frozen_cold_private_bootstrap',lambda:reconstruct_authorization(store,store.applicability['authorization_id']))
  measure('frozen_warm_context_verification',lambda:a.context_binding.governance.verify())
  measure('frozen_warm_model_projection',lambda:derive(json.loads(a.context_projection),a.context_binding))
 status=measure('frozen_terminal_operator_projection',lambda:project(store,a.authorization_id))
 (O/'FROZEN_TERMINAL_STATUS.json').write_text(canonical(status))
 print(canonical({r['name']:r['seconds'] for r in measurements}))
finally:store.close()
