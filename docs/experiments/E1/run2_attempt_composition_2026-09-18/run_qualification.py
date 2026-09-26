import json,subprocess,sys,time,unittest
from pathlib import Path
import qualify
out=Path(sys.argv[1]);names=unittest.defaultTestLoader.getTestCaseNames(qualify.Composition);results=[]
for name in names:
 begin=time.monotonic()
 try:
  p=subprocess.run([sys.executable,'-m','unittest','-v','qualify.Composition.'+name],capture_output=True,text=True,timeout=40)
  result={'test':name,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'deadlock_timeout':False}
 except subprocess.TimeoutExpired as e:
  result={'test':name,'returncode':None,'stdout':(e.stdout or b'').decode(),'stderr':(e.stderr or b'').decode(),'deadlock_timeout':True}
 result['seconds']=time.monotonic()-begin;results.append(result);print(name,result['returncode'],flush=True)
 (out/'INTEGRATED_TESTS.json').write_text(json.dumps(results,sort_keys=True))
