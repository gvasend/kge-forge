"""Static contract checks, not host capability or fake-protocol tests."""
import hashlib,importlib.util,json,os,pathlib,subprocess,sys
D=pathlib.Path(__file__).resolve().parent;R=D.parents[4]
def load(n):return json.loads((D/n).read_text())
def put(n,x):
 with (D/n).open('x') as f:json.dump(x,f,indent=2,sort_keys=True);f.write('\n')
spec=importlib.util.spec_from_file_location('static_contract',D/'verify.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
rows=[]
for seed in [0,1,7,101]:
 x=json.loads(subprocess.check_output([sys.executable,str(D/'verify.py')],cwd=str(R),env=dict(os.environ,PYTHONHASHSEED=str(seed),PYTHONDONTWRITEBYTECODE='1')))
 if seed==0:ref=x
 else:assert x==ref
 rows.append({'PYTHONHASHSEED':seed,'RESULT':'PASS','SEMANTIC_SHA256':hashlib.sha256(v.cb(x)).hexdigest()})
put('independent-reconstruction.json',ref);put('four-seed-determinism.json',{'RESULT':'PASS_STATIC','FRESH_METADATA_READERS':4,'SEEDS':rows,'HOST_TESTS_OR_ADAPTER_RUNS':0})
neg=[]
def reject(name,file,fn):
 x=load(file);fn(x)
 if file=='host-capability-test-authorization-subject.json':x['IDENTITY']['sha256']=hashlib.sha256(v.cb(x['CONTENT'])).hexdigest()
 try:v.verify({file:x})
 except (AssertionError,KeyError,ValueError):neg.append({'CONTROL':name,'RESULT':'REJECTED','NO_ACTIVE_TEST':True});return
 raise RuntimeError('Accepted invalid contract: '+name)
reject('real fixture substituted for fake input','positive-oracle-authentication.json',lambda x:x['ORACLES'][0]['FIXTURE_PIN'].update(PATH='docs/plans/qualification/E2_P04_CANONICAL_EXECUTION_RETRY_1/checkpoints/post-root-proof/post-root-proof.json'))
reject('adapter output used as oracle','fault-lifecycle-oracle.json',lambda x:x.update(ADAPTER_OUTPUT_USED_AS_ORACLE=True))
reject('missing fault expectation','fault-lifecycle-oracle.json',lambda x:x['FAULTS'].pop())
reject('wrong executable hash','executable-source-manifest.json',lambda x:x['FILES'][0].update(SOURCE_SHA256='0'*64))
reject('unsupported Bubblewrap option','direct-host-confinement-specification.json',lambda x:x['BWRAP_RECIPE'].append('--unsupported-control'))
reject('unverified control marked enforceable','resource-enforcement-procedure.json',lambda x:x.update(HOST_RESOURCE_ENFORCEMENT_READY=True))
reject('missing output confinement','direct-host-confinement-specification.json',lambda x:x.update(ONE_OWNED_OUTPUT_ROW_WRITABLE=False))
reject('stopped campaign reused','campaign-input-closure.json',lambda x:x.update(HOST_TEST_SCOPE_DOES_NOT_RENEW_OLD_CAMPAIGN=False))
reject('automatic retry enabled','host-capability-test-authorization-subject.json',lambda x:x['CONTENT']['PROCEDURE']['RESOURCE_BUDGET'].update(RETRIES=1))
reject('host probe treated as fake campaign approval','readiness-gates.json',lambda x:x.update(FAKE_CAMPAIGN_DECISION_READY='YES'))
reject('native synthetic scope included','host-capability-test-authorization-subject.json',lambda x:x['CONTENT']['EXCLUSIONS'].remove('native synthetic integration'))
reject('actual A15 execution included','campaign-input-closure.json',lambda x:x.update(NO_ACTUAL_A15_EXECUTION=False))
reject('unknown first counterexample silently sealed','fault-lifecycle-oracle.json',lambda x:x['FAULTS'][0]['EXPECTED_FIRST_COUNTEREXAMPLE'].update(CLASSIFICATION='EXACT'))
reject('host subset authority issued before approval','host-capability-test-authorization-subject.json',lambda x:x.update(ISSUED=True))
put('negative-controls.json',{'RESULT':'PASS','PASSED':len(neg),'TOTAL':len(neg),'CONTROLS':neg,'DOMAIN':'Static metadata contradiction checks only'})
print(json.dumps({'FOUR_SEED_DETERMINISM':'PASS_STATIC','NEGATIVE_SUITE':str(len(neg))+'/'+str(len(neg))+' PASS','HOST_TESTS':0}))
