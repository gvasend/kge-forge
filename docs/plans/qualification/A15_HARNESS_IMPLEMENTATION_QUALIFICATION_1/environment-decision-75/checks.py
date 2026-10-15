"""Static corruption checks only, no environment or adapter tests."""
import importlib.util,json,os,pathlib,subprocess,sys
D=pathlib.Path(__file__).resolve().parent;R=D.parents[4]
def read(n):return json.loads((D/n).read_text())
def put(n,x):
 with (D/n).open('x') as f:json.dump(x,f,indent=2,sort_keys=True);f.write('\n')
spec=importlib.util.spec_from_file_location('static_verifier',D/'verify.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
rows=[]
for seed in [0,1,7,101]:
 x=json.loads(subprocess.check_output([sys.executable,str(D/'verify.py')],cwd=str(R),env=dict(os.environ,PYTHONHASHSEED=str(seed),PYTHONDONTWRITEBYTECODE='1')))
 if seed==0:ref=x
 else:assert x==ref
 rows.append({'PYTHONHASHSEED':seed,'RESULT':'PASS','SEMANTIC_SHA256':v.canon(x)})
put('independent-reconstruction.json',ref);put('four-seed-determinism.json',{'RESULT':'PASS_STATIC','FRESH_DOCUMENTARY_READERS':4,'SEEDS':rows,'CONFINEMENT_OR_ADAPTER_TESTS':0})
neg=[]
def reject(name,file,mutate):
 x=read(file);mutate(x)
 try:v.verify({file:x})
 except (AssertionError,KeyError,ValueError):neg.append({'CONTROL':name,'RESULT':'REJECTED','RUNTIME_ACTION':False});return
 raise RuntimeError('Accepted invalid environment decision: '+name)
reject('unsupported Codex policy assumed compatible','recovery-strategy-comparison.json',lambda x:x['PATH_A'].update(COMPATIBLE='YES'))
reject('unknown permissions treated as granted','independent-qualification-host-specification.json',lambda x:x.update(PERMISSIONS_VERIFIED=True))
reject('unqualified VM treated as compatible','independent-qualification-host-specification.json',lambda x:x.update(ENVIRONMENT_QUALIFIED=True))
reject('network confinement weakened','resource-control-equivalence-matrix.json',lambda x:x.update(NETWORK_DISABLED_REQUIREMENT_WEAKENED=True))
reject('missing resource enforcement ignored','resource-control-equivalence-matrix.json',lambda x:x['ROWS'].pop())
reject('unauthorized host provisioning/change','independent-qualification-host-specification.json',lambda x:x.update(PROVISIONING_PERFORMED=True))
reject('unapproved artifact transfer','artifact-transfer-contract.json',lambda x:x.update(TRANSFER_PERFORMED=True))
reject('terminated campaign reused','campaign-authority-prerequisites.json',lambda x:x.update(EXISTING_GRANT_IS_UNLIMITED_RETRY_PERMISSION=True))
reject('automatic retries allowed','campaign-authority-prerequisites.json',lambda x:x['CURRENT_VALUES']['RETRY_POLICY'].update(AUTOMATIC_RETRIES=1))
reject('real checkpoint transfer permitted','artifact-transfer-contract.json',lambda x:x['FORBIDDEN_TRANSFER'].remove('real A15 checkpoint and original19 ledger files'))
reject('native A15 execution included','campaign-authority-prerequisites.json',lambda x:x.update(NO_ACTUAL_A15_SCOPE=False))
reject('missing host identity treated as sealed','readiness-gates.json',lambda x:x.update(PATH_B_PROFILE_COMPLETE='YES'))
reject('lack of PathA evidence treated as impossibility','recovery-strategy-comparison.json',lambda x:x['PATH_A'].update(IMPOSSIBILITY_PROVEN=True))
put('negative-controls.json',{'RESULT':'PASS','PASSED':len(neg),'TOTAL':len(neg),'CONTROLS':neg})
print(json.dumps({'FOUR_SEED_DETERMINISM':'PASS_STATIC','NEGATIVE_SUITE':str(len(neg))+'/'+str(len(neg))+' PASS','TESTS_OR_TRANSFER':False}))
