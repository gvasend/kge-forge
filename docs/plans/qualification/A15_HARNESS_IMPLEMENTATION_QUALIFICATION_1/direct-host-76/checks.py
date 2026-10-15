"""Documentary/static checks only, never a fake-protocol or host test."""
import hashlib,importlib.util,json,os,pathlib,subprocess,sys
D=pathlib.Path(__file__).resolve().parent;R=D.parents[4]
def read(n):return json.loads((D/n).read_text())
def put(n,x):
 with (D/n).open('x') as f:json.dump(x,f,sort_keys=True,indent=2);f.write('\n')
spec=importlib.util.spec_from_file_location('metadata_verifier',D/'verify.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
rows=[]
for seed in [0,1,7,101]:
 x=json.loads(subprocess.check_output([sys.executable,str(D/'verify.py')],cwd=str(R),env=dict(os.environ,PYTHONHASHSEED=str(seed),PYTHONDONTWRITEBYTECODE='1')))
 if seed==0:ref=x
 else:assert x==ref
 rows.append({'PYTHONHASHSEED':seed,'RESULT':'PASS','SEMANTIC_SHA256':hashlib.sha256(v.encode(x)).hexdigest()})
put('independent-reconstruction.json',ref)
put('four-seed-determinism.json',{'RESULT':'PASS_STATIC_DOCUMENTARY','SEEDS':rows,'ADAPTER_FAKE_PROTOCOL_TESTS':0,'HOST_PROBE_REPRODUCTIONS':0})
neg=[]
def reject(name,file,fn):
 x=read(file);fn(x)
 try:v.verify({file:x})
 except (AssertionError,KeyError,ValueError):neg.append({'CONTROL':name,'RESULT':'REJECTED','NO_ADAPTER_OR_HOST_TEST':True});return
 raise RuntimeError('Accepted invalid direct-host metadata: '+name)
reject('Codex context substituted for direct host','execution-context-comparison.json',lambda x:x.update(CONTEXTS_EQUIVALENT=True))
reject('host launch treated as complete qualification','direct-host-probe-evidence.json',lambda x:x.update(HOST_QUALIFIED=True))
reject('unverified resources marked enforceable','resource-enforcement-matrix.json',lambda x:x.update(RESOURCE_ENFORCEMENT_READY=True))
reject('proposed subject substituted for issued grant','effective-grant-reconciliation.json',lambda x:x.update(GRANT_IDENTITY=x['APPROVED_SUBJECT_IDENTITY']))
reject('stopped campaign reused','stopped-campaign-reconciliation.json',lambda x:x.update(CURRENT_CAMPAIGN_ACTIVE=True))
reject('real checkpoint claimed as fake initial Snapshot','fixtures/SYNTHETIC-ONE.json',lambda x:x['FIXTURE'].update(initial_snapshot_identity={'kind':'CONTENT_IDENTITY','namespace':'planner-snapshot-v1','sha256':'ce54ff49907abcad564ec0ddfe8c7a019fab129936172b67f4ce0ff5ed013586'}))
reject('real oracle substituted for fake expected output','synthetic-fixture-manifest.json',lambda x:x.update(REAL_A15_ORACLES_USED=True))
reject('unknown executable identity accepted','executable-identity-manifest.json',lambda x:x['SOURCE_HASHES'].update({'adapter/qualification_a15/worker.py':'0'*64}))
reject('unsealed host profile marked ready','direct-host-profile-assessment.json',lambda x:x.update(DIRECT_HOST_PROFILE_SEALED=True))
reject('automatic retry allowed','fresh-campaign-authority-prerequisites.json',lambda x:x['RETRY_POLICY'].update(AUTOMATIC_RETRIES=1))
reject('actual A15 execution included','fresh-campaign-authority-prerequisites.json',lambda x:x.update(ACTUAL_A15_INCLUDED=True))
reject('new campaign authority issued before approval','fresh-campaign-authority-prerequisites.json',lambda x:x.update(NO_NEW_CAMPAIGN_AUTHORITY_ISSUED=False))
reject('user-supplied probe relabelled reproduced','direct-host-probe-evidence.json',lambda x:x.update(INDEPENDENT_REPRODUCTION_PERFORMED=True))
reject('cgroup v2 delegation assumed','resource-enforcement-matrix.json',lambda x:x.update(CGROUP_V2_DELEGATION_ASSUMED=True))
reject('wrong full fake expected output','expected/SYNTHETIC-ONE.json',lambda x:x['EXPECTED_OUTPUT']['PUBLISHED_OUTPUT']['payload'].update(control='NATIVE_PASS'))
reject('unsealed invocation oracles labelled complete','readiness-gates.json',lambda x:x.update(INDEPENDENT_FAKE_ORACLES_COMPLETE='YES'))
put('negative-controls.json',{'RESULT':'PASS','PASSED':len(neg),'TOTAL':len(neg),'CONTROLS':neg,'DOMAIN':'Static metadata semantic contradictions only, no implementation/runtime fault injection'})
print(json.dumps({'FOUR_SEED_DETERMINISM':'PASS_STATIC','NEGATIVE_SUITE':str(len(neg))+'/'+str(len(neg))+' PASS','TESTS_EXECUTED':0}))
