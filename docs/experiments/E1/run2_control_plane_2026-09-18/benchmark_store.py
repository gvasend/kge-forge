"""Real pinned authority bytes, isolated store primitive benchmark, not activation."""
import hashlib,json,sys,time
from pathlib import Path
O=Path(__file__).resolve().parent
pin=json.loads((O.parent/'run2_r12_dispatch_2026-09-18/CURRENT_PIN.json').read_bytes())
b=Path(pin['path']).read_bytes();assert hashlib.sha256(b).hexdigest()==pin['sha256'];p=json.loads(b)
kind=sys.argv[1];sys.path.insert(0,p['runtime_root'] if kind=='applied' else str(O/'candidate'))
from adapter.controller_authority_store import ControllerAuthorityStore
rows=[]
for i in range(4):
 t=time.monotonic();s=ControllerAuthorityStore(**p['selected_store']);bootstrap=time.monotonic()-t
 try:
  t=time.monotonic()
  for _ in range(100):s._verify_catalog()
  elapsed=time.monotonic()-t
  rows.append({'sample':i,'bootstrap_seconds':bootstrap,'fresh_catalog_checks':100,'seconds':elapsed})
 finally:s.close()
(O/('STORE_BENCHMARK_'+kind.upper()+'.json')).write_text(json.dumps({'scope':'ACTUAL_PINNED_STORE_PRIMITIVE_NOT_FULL_PRODUCTION','publication':pin,'samples':rows},indent=2))
print(json.dumps(rows))
