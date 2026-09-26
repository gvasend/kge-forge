"""Read-only profiling of the applied context. No lifecycle writes or model calls."""
import cProfile, hashlib, json, pstats, sys, time
from pathlib import Path
O=Path(__file__).resolve().parent
R=O.parent/'run2_r12_dispatch_2026-09-18'
pin=json.loads((R/'CURRENT_PIN.json').read_bytes())
raw=Path(pin['path']).read_bytes()
assert hashlib.sha256(raw).hexdigest()==pin['sha256']
p=json.loads(raw)
sys.path.insert(0,p['runtime_root'])
from adapter.controller_authority_store import ControllerAuthorityStore
from adapter.authority_bootstrap import reconstruct_authorization
from adapter.context_projection import derive
from adapter.attempt_chain import readiness
s=ControllerAuthorityStore(**p['selected_store'])
prof=cProfile.Profile();results=[]
try:
 with s.session():
  for name,fn in [('bootstrap',lambda:reconstruct_authorization(s,p['r12_authorization_id']))]:
   t=time.monotonic();prof.enable();a=fn();prof.disable();results.append({'name':name,'seconds':time.monotonic()-t})
  for i in range(3):
   t=time.monotonic();prof.enable();a.context_binding.governance.verify();prof.disable();results.append({'name':'history_verify','sample':i,'seconds':time.monotonic()-t})
  t=time.monotonic();prof.enable();ids=derive(json.loads(a.context_projection),a.context_binding);prof.disable();results.append({'name':'projection','seconds':time.monotonic()-t})
  assert all(ids[k]==v for k,v in p['context_identities'].items())
  if '--readiness' in sys.argv:
   t=time.monotonic();ready=readiness(a,s,None,True,None);results.append({'name':'fresh_supervisor','seconds':time.monotonic()-t,'result':ready})
finally:s.close()
prof.dump_stats(str(O/'CURRENT_PROFILE.pstats'))
with (O/'CURRENT_PROFILE.txt').open('w') as f:pstats.Stats(prof,stream=f).strip_dirs().sort_stats('cumulative').print_stats(60)
(O/'CURRENT_PROFILE.json').write_text(json.dumps({'publication':pin,'measurements':results,'profiling_overhead':True,'lifecycle_mutations':0,'model_requests':0},indent=2))
print(json.dumps(results,default=str))
