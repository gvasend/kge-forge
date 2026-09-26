"""Three explicitly authorized synthetic qualification slots, no real retry."""
import json,subprocess,sys
from pathlib import Path
O=Path(__file__).resolve().parent
for name in ('warm1','warm2','warm3'):
 with (O/('PATH_'+name+'.log')).open('w') as log:
  result=subprocess.run([sys.executable,'-B',str(O/'qualify_path.py'),name],stdout=log,stderr=subprocess.STDOUT)
 if result.returncode:raise SystemExit('qualification failed: '+name)
 value=json.loads((O/('PATH_'+name+'.json')).read_text())
 if value['result']!='PASS':raise SystemExit('path blocked: '+name)
 print(json.dumps({'case':name,'result':value['result'],'cumulative_seconds':value['cumulative_model_request_ready_seconds']}),flush=True)
