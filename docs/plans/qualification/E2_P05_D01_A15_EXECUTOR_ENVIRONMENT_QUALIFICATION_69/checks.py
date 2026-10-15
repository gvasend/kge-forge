"""Package69 static corruption controls only, not implementation/runtime tests."""
import copy, importlib.util, json, os, pathlib, subprocess, sys
D=pathlib.Path(__file__).resolve().parent;R=D.parents[3]
def load(n):return json.loads((D/n).read_text())
def write(n,a):
 with (D/n).open('x') as f:json.dump(a,f,indent=2,sort_keys=True);f.write('\n')
spec=importlib.util.spec_from_file_location('static_reader',D/'verify.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
rows=[]
for seed in [0,1,7,101]:
 out=json.loads(subprocess.check_output([sys.executable,str(D/'verify.py')],cwd=str(R),env=dict(os.environ,PYTHONHASHSEED=str(seed),PYTHONDONTWRITEBYTECODE='1')))
 rows.append({'PYTHONHASHSEED':seed,'RESULT':'PASS','SEMANTIC_SHA256':v.canon(out)})
 if seed==0:ref=out
 else:assert out==ref
write('independent-reconstruction.json',ref)
write('four-seed-determinism.json',{'RESULT':'PASS','FRESH_STATIC_PROCESSES':4,'SEEDS':rows,'NO_NATIVE_WORKER_OR_COLD_READER_LAUNCHED':True,'ENVIRONMENT_OBSERVATION':'Revalidated against actual interpreter/access metadata; time record is pinned inventory observation, not future sealed profile'})
neg=[]
def reject(name,file,mutate,reidentify=False):
 value=load(file);mutate(value)
 if reidentify:value['CONTENT_IDENTITY']['sha256']=v.canon(value['CONTENT'])
 try:v.run({file:value},entry=False)
 except (AssertionError,KeyError,ValueError,StopIteration):neg.append({'CONTROL':name,'RESULT':'REJECTED','METHOD':'In-memory documentary corruption; actual implementation not invoked'});return
 raise RuntimeError('Accepted negative: '+name)
reject('wrong executable identity','candidate-executable-invocation-inventory.json',lambda x:x[0]['SOURCE_IDENTITY'].update(RAW_SHA256='0'*64))
reject('wrong interpreter','candidate-executable-invocation-inventory.json',lambda x:x[0]['INTERPRETER'].update(RAW_SHA256='0'*64))
reject('wrong checkpoint','checkpoint-and-variant-bindings.json',lambda x:x['INITIAL_SNAPSHOT_IDENTITY'].update(sha256='0'*64))
reject('wrong source identity','checkpoint-and-variant-bindings.json',lambda x:x['VARIANTS'][0]['BINDING']['RECORD_RESULT_INPUT'].update(changed=[]))
reject('missing process isolation','supervisor-worker-architecture-analysis.json',lambda x:x.update(DISTINCT_MUTABLE_STATE_AND_OUTPUTS=False))
reject('worker self-certifying termination','supervisor-worker-architecture-analysis.json',lambda x:x.update(WORKER_SELF_CERTIFIES_EXIT=True))
reject('handoff substituted for writer exit','supervisor-worker-architecture-analysis.json',lambda x:x.update(HANDOFF_IS_EXIT_EVIDENCE=True))
reject('readers before supervisor exit/publication','supervisor-worker-architecture-analysis.json',lambda x:x.update(READERS_REQUIRE_EXIT_AND_PUBLICATION=False))
reject('incomplete resource permissions marked verified','resource-permission-assessment.json',lambda x:x.update(RESOURCE_PERMISSIONS_VERIFIED=True))
reject('unsealed environment marked ready','readiness-gates.json',lambda x:x.update(ENVIRONMENT_PROFILE_SEALED='YES'))
reject('normative authority treated as implementation authority','implementation-authority-assessment.json',lambda x:x.update(NORMATIVE_AUTHORITY_INCLUDES_IMPLEMENTATION=True))
reject('static specification treated as qualified implementation','supervisor-worker-architecture-analysis.json',lambda x:x.update(A15_PROCESS_MODEL_IMPLEMENTED_AND_QUALIFIED=True))
reject('actual A15 execution during inventory accepted','input-authentication.json',lambda x:x.update(NATIVE_FUNCTIONS_CALLED=True))
reject('production scope expansion','proposed-implementation-test-authority-subject.json',lambda x:x['CONTENT'].update(PURPOSE='Production execution'),True)
reject('wrong native entrypoint signature','existing-implementation-inventory.json',lambda x:x[0].update(FUNCTION_SIGNATURE='(guessed)'))
reject('A14 qualification transferred to complete A15','existing-implementation-inventory.json',lambda x:x[0].update(QUALIFICATION_DOMAIN='All A15 scenarios'))
reject('automatic retry added','failure-retry-capability-mapping.json',lambda x:x[0].update(AUTOMATIC_RETRY_AUTHORIZED=True))
reject('wrong future output namespace','future-execution-profile-specification.json',lambda x:x.update(OUTPUT_ALLOWLIST=[]))
reject('capture readiness inferred from normative adoption','readiness-gates.json',lambda x:x.update(A15_CAPTURE_DECISION_READY='YES'))
write('negative-controls.json',{'RESULT':'PASS','PASSED':len(neg),'TOTAL':len(neg),'CONTROLS':neg,'QUALIFICATION_DOMAIN':'Static inventory and readiness evidence only; not runtime fault injection'})
print(json.dumps({'FOUR_SEED_DETERMINISM':'PASS','NEGATIVE_SUITE':str(len(neg))+'/'+str(len(neg))+' PASS'},sort_keys=True))
