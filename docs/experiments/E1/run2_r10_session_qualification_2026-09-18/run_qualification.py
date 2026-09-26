import subprocess,json,time,os
from pathlib import Path
out=Path('/home/gvasend/app/kge-forge/docs/experiments/E1/run2_r10_session_qualification_2026-09-18')
results=[]
for name,modules in [('session',['qualify_session']),('prior_attempt',['qualify_base']),('regressions',['adapter.tests.test_run_control','adapter.tests.test_authorization_lifecycle','adapter.tests.test_controller_authority_store'])]:
 t=time.monotonic()
 try:
  p=subprocess.run(['/usr/bin/python3.8','-m','unittest','-v']+modules,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=180,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
  text=p.stdout.decode();code=p.returncode
 except subprocess.TimeoutExpired as e:text=(e.stdout or b'').decode();code='BOUNDED_DEADLOCK_DETECTOR_TIMEOUT'
 (out/(name+'.log')).write_text(text);results.append({'suite':name,'returncode':code,'seconds':time.monotonic()-t,'timeout_seconds':180})
 (out/'TEST_RESULTS.json').write_text(json.dumps(results,indent=2))
 print(results[-1],flush=True)
