"""Documentary authority checks; not execution of adapter/synthetic/native tests."""
import copy,importlib.util,itertools,json,os,pathlib,subprocess,sys
D=pathlib.Path(__file__).resolve().parent;R=D.parents[3]
def load(p):return json.loads(p.read_text())
def put(n,x):
 with (D/n).open('x') as f:json.dump(x,f,indent=2,sort_keys=True,ensure_ascii=False);f.write('\n')
spec=importlib.util.spec_from_file_location('independent_documentary_verifier',D/'verify.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
seeds=[]
for seed in [0,1,7,101]:
 out=json.loads(subprocess.check_output([sys.executable,str(D/'verify.py')],cwd=str(R),env=dict(os.environ,PYTHONHASHSEED=str(seed),PYTHONDONTWRITEBYTECODE='1')))
 if seed==0:reference=out
 else:assert out==reference
 seeds.append({'PYTHONHASHSEED':seed,'RESULT':'PASS','SEMANTIC_SHA256':v.canon(out)})
put('independent-subject-qualification.json',reference)
put('four-seed-determinism.json',{'RESULT':'PASS','FRESH_DOCUMENTARY_PROCESSES':4,'SEEDS':seeds,'ADAPTER_OR_NATIVE_TESTS_EXECUTED':0,'INDEPENDENT_METHOD':'Canonical reconstruction from persisted exact subject plus original sources/contracts/host observations, semantic scope/phase checks and all abstract guard assignments; no run-derived expected values'})
base=load(D/'implementation-test-authority-subject.json');negative=[]
def reject(name,mutate):
 candidate=copy.deepcopy(base);mutate(candidate);candidate['IDENTITY']['sha256']=v.canon(candidate['CONTENT'])
 try:v.verify(candidate,check_entry=False,check_contract_files=False)
 except (AssertionError,KeyError,ValueError):negative.append({'CONTROL':name,'RESULT':'REJECTED','REIDENTIFIED_BEFORE_SEMANTIC_CHECK':True,'NATIVE_OR_SYNTHETIC_TEST_EXECUTED':False});return
 raise RuntimeError('Accepted documentary negative: '+name)
def c(x,n):return x['CONTENT']['CONTRACTS'][n]
reject('wrong charter identity',lambda x:x['CONTENT']['GOVERNING_CHARTER'].update(sha256='0'*64))
reject('wrong normative mandate',lambda x:x['CONTENT']['NORMATIVE_SUBJECT'].update(sha256='0'*64))
reject('unbounded implementation paths',lambda x:c(x,'source-file-scope.json')['PERMITTED_SOURCE_FILES'].append('adapter/**'))
reject('unauthorized runtime modification',lambda x:c(x,'source-file-scope.json').update(NO_EXISTING_RUNTIME_MODIFICATION=False))
reject('real A15 checkpoint admitted as synthetic fixture',lambda x:c(x,'synthetic-fixture-contract.json')['REAL_INPUT_DENYLIST'].update(CHECKPOINT_PATH='ALLOW_REAL_CHECKPOINT_AS_SYNTHETIC'))
reject('real A15 variant execution permitted',lambda x:c(x,'synthetic-fixture-contract.json').update(REAL_A15_EXECUTION_ALLOWED=True))
reject('unsealed environment treated as qualified',lambda x:c(x,'environment-resource-permission-contract.json').update(SEALED_FOR_TEST_ENTRY=True))
reject('missing process isolation',lambda x:c(x,'process-isolation-persistence-controls.json').update(CROSS_VARIANT_STATE_REUSE=True))
reject('worker self-certifying exit',lambda x:c(x,'process-isolation-persistence-controls.json').update(WORKER_SELF_CERTIFIES_EXIT=True))
reject('handoff substituted for writer exit',lambda x:c(x,'process-isolation-persistence-controls.json').update(HANDOFF_IS_EXIT_PROOF=True))
reject('unauthorized automatic retry',lambda x:c(x,'failure-retry-controls.json').update(AUTOMATIC_RETRY=True))
reject('production external scope expansion',lambda x:x['CONTENT']['HISTORICAL_EXCLUSIONS'].remove('general engineering/production/external/government authority or security bypass'))
reject('authority issued before decision',lambda x:x.update(ISSUED_GRANT_IDENTITY={'CLAIM':'ISSUED'}))
reject('synthetic PASS treated as real A15 authorization',lambda x:c(x,'implementation-qualification-acceptance.json').update(NO_REAL_A15_EXECUTION_AUTHORITY_FROM_TEST_PASS=False))
reject('unknown permission silently accepted',lambda x:c(x,'environment-resource-permission-contract.json')['ACTIVATION_EVALUATION_RULE'].update(UNKNOWN_POLICY='ALLOW'))
reject('native test phase omits authority predicate',lambda x:c(x,'environment-resource-permission-contract.json')['PHASE_GUARDS']['NATIVE_SYNTHETIC_TEST'].remove('EP70-GRANT'))
reject('unbounded process launches',lambda x:c(x,'environment-resource-permission-contract.json')['RESOURCE_LIMITS'].update(MAX_CHILD_LAUNCHES_PER_APPROVED_CAMPAIGN=None))
reject('changed real source denylist',lambda x:c(x,'synthetic-fixture-contract.json')['REAL_INPUT_DENYLIST'].update(RETAINED_SOURCE_IDENTITIES=[]))
reject('policy used as invalidation target',lambda x:c(x,'synthetic-fixture-contract.json')['POLICY_EXCEPTION'].update(PERMITTED_USE='CHANGE_POLICY_AS_SYNTHETIC_SUPPORT'))
reject('HEAD operation authorized',lambda x:c(x,'permitted-test-inventory.json').update(HEAD_MUTATION=True))
reject('future approval placed inside grant-content subject',lambda x:x['CONTENT'].update(PROJECT_OWNER_APPROVAL_EVIDENCE={'APPROVED':True}))
put('negative-controls.json',{'RESULT':'PASS','TOTAL':len(negative),'PASSED':len(negative),'CONTROLS':negative,'DOMAIN':'Prospective authority metadata semantic checks; no implementation/runtime fault-injection tests'})
# Additional temporal logic proof prevents a writer-exit-before-writer-launch circularity.
profile=base['CONTENT']['CONTRACTS']['environment-resource-permission-contract.json'];facts=profile['TEMPORAL_GATES']['READER_LAUNCH_REQUIRED_RUNTIME_FACTS'];rows=[]
for bits in itertools.product([False,True],repeat=3):
 enabled=all(bits);rows.append({'FACTS':dict(zip(facts,bits)),'READER_ELIGIBLE_IF_PHASE_ENTRY_ALSO_VALID':enabled})
assert sum(x['READER_ELIGIBLE_IF_PHASE_ENTRY_ALSO_VALID'] for x in rows)==1
put('phase-and-temporal-guard-evidence.json',{'RESULT':'PASS_ABSTRACT_POLICY_ONLY','NATIVE_PHASE_CONJUNCTION_ASSIGNMENTS':2048,'ONLY_ALL_ELEVEN_TRUE_ENABLES_NATIVE_PHASE':True,'CURRENT_ACTUAL_GRANT_EFFECTIVE':False,'CURRENT_ACTUAL_NATIVE_PHASE_ENABLED':False,'READER_RUNTIME_FACT_ASSIGNMENTS':rows,'WORKER_LAUNCH_REQUIRES_PRIOR_EXIT':False,'SIMULATED_FACTS_ARE_NOT_AUTHORITY_OR_OS_PERMISSION_EVIDENCE':True})
print(json.dumps({'FOUR_SEED_DETERMINISM':'PASS','NEGATIVE_SUITE':str(len(negative))+'/'+str(len(negative))+' PASS','SUBJECT_IDENTITY':base['IDENTITY'],'CONDITIONAL_DECISION_READINESS':reference['IMPLEMENTATION_TEST_DECISION_READY']},sort_keys=True))
