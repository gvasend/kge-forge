"""Static recovery checks, not confinement/fake/native tests."""
import copy,importlib.util,json,os,pathlib,subprocess,sys
D=pathlib.Path(__file__).resolve().parent;R=D.parents[4]
def read(n):return json.loads((D/n).read_text())
def put(n,x):
 with (D/n).open('x') as f:json.dump(x,f,sort_keys=True,indent=2);f.write('\n')
spec=importlib.util.spec_from_file_location('readonly_recovery_reader',D/'verify.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
seeds=[]
for seed in [0,1,7,101]:
 x=json.loads(subprocess.check_output([sys.executable,str(D/'verify.py')],env=dict(os.environ,PYTHONHASHSEED=str(seed),PYTHONDONTWRITEBYTECODE='1'),cwd=str(R)))
 if seed==0:reference=x
 else:assert x==reference
 seeds.append({'PYTHONHASHSEED':seed,'RESULT':'PASS','SEMANTIC_SHA256':v.canon(x)})
put('independent-reconstruction.json',reference)
put('four-seed-determinism.json',{'RESULT':'PASS_STATIC_READONLY','FRESH_METADATA_READERS':4,'SEEDS':seeds,'BWRAP_RETRIES':0,'FAKE_OR_NATIVE_TESTS_EXECUTED':0})
neg=[]
def reject(name,file,mutate):
 x=read(file);mutate(x)
 try:v.verify({file:x})
 except (AssertionError,KeyError,ValueError):neg.append({'CONTROL':name,'RESULT':'REJECTED','NO_RECOVERY_EXECUTION':True});return
 raise RuntimeError('Accepted invalid recovery evidence: '+name)
reject('failed bwrap invocation treated as success','failure-evidence-authentication.json',lambda x:x.update(EXIT_STATUS=0))
reject('unknown namespace capability treated as available','readiness-gates.json',lambda x:x.update(EXISTING_HOST_COMPATIBLE='YES'))
reject('network confinement silently disabled','approved-control-matrix.json',lambda x:next(y for y in x['CONTROL_MATRIX'] if y['CONTROL_ID']=='NETWORK_BOUNDARY').update(NON_SUBSTITUTION_RULE='Disable --unshare-net'))
reject('application checks substituted for OS isolation','approved-control-matrix.json',lambda x:next(y for y in x['CONTROL_MATRIX'] if y['CONTROL_ID']=='FILESYSTEM_BOUNDARY').update(ENFORCER='Application path checks only'))
reject('unsupported resource limits ignored','approved-control-matrix.json',lambda x:x['RESOURCE_LIMITS'].update(CHILD_CPU_SECONDS=None))
reject('unauthorized host configuration change','existing-host-recovery-assessment.json',lambda x:x.update(CONFIGURATION_CHANGED=True))
reject('alternative confinement assumed equivalent','alternative-confinement-equivalence-assessment.json',lambda x:x.update(ALTERNATIVE_CONFINEMENT_EQUIVALENT='YES'))
reject('terminated campaign reused','campaign-authority-assessment.json',lambda x:x.update(OLD_GRANT_REFERENCE_ALONE_MAY_AUTHORIZE_NEW_CAMPAIGN=True))
reject('automatic retry permitted','campaign-authority-assessment.json',lambda x:x.update(AUTOMATIC_RETRIES=1))
reject('unsealed host treated as qualified','alternative-host-profile.json',lambda x:x.update(ACTUAL_HOST_QUALIFIED=True))
reject('actual A15 readiness inferred','readiness-gates.json',lambda x:x.update(NATIVE_SYNTHETIC_TEST_READY='YES'))
reject('underlying root cause claimed without evidence','confinement-root-cause-assessment.json',lambda x:x.update(FAILURE_CAUSE_ESTABLISHED=True))
reject('seccomp mode treated as exact rejecting rule','confinement-root-cause-assessment.json',lambda x:next(y for y in x['HYPOTHESES'] if y['HYPOTHESIS_ID']=='H73-SPECIFIC-SECCOMP-RULE').update(CLASSIFICATION='SUPPORTED'))
reject('historical argv presented as observed capture','failure-evidence-authentication.json',lambda x:x.update(ARGV_EVIDENCE_STATUS='EXACT_CAPTURED_ARGV'))
reject('unrestricted subprocess accepted as equivalent','alternative-confinement-equivalence-assessment.json',lambda x:x.update(UNRESTRICTED_SUBPROCESS_EQUIVALENT=True))
put('negative-controls.json',{'RESULT':'PASS','TOTAL':len(neg),'PASSED':len(neg),'CONTROLS':neg,'QUALIFICATION_DOMAIN':'Static recovery/authority interpretation only, not runtime fault injection'})
print(json.dumps({'RESULT':'PASS_STATIC_READONLY','FOUR_SEED_DETERMINISM':'PASS','NEGATIVE_SUITE':str(len(neg))+'/'+str(len(neg))+' PASS','RECOVERY_TESTS_EXECUTED':0}))
