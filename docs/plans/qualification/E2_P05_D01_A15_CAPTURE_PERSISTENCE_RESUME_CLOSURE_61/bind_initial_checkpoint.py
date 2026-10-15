"""Bind the authoritative existing native checkpoint; static byte reads only."""
import pathlib,json,hashlib
E=pathlib.Path(__file__).parent;Q=E.parent
read=lambda p:json.loads(pathlib.Path(p).read_text())
sha=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
fixture=Q/'E2_P05_D01_FIXTURE_ORACLE_CLOSURE_2/fixtures/D01-VARIANT__E2-A15__CANONICAL_REQUIRED_BEHAVIOR.json';f=read(fixture)
# The exact retained capsule provenance governs selection among native aliases.
assert len(f['provenance'])==1;pin=f['provenance'][0];path=pathlib.Path(pin['path']);assert path.resolve()==path.absolute() and sha(path)==pin['raw_sha256']
b=read(path);assert b=={'schema':'PLANNER-BUNDLE-1','bundle':f['canonical_content']['bundle']}
identity={'$type':'ArtifactIdentity','kind':{'$enum':'IdentityKind','value':'CONTENT_IDENTITY'},'namespace':'planner-bundle-v1','sha256':pin['raw_sha256']}
files={str(path):sha(path)}
for event in b['bundle']['events']:
 p=path.parent/('event-'+event['identity']['sha256']+'.json');raw=json.dumps(event,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
 assert p.resolve()==p.absolute() and p.read_bytes()==raw;files[str(p)]=sha(p)
assert len(files)==20
record={'SOURCE_PRECEDENCE':'Exact original capsule /provenance/0, not newest alias or semantic similarity','SOURCE_PATH':str(path),'SOURCE_HASH':sha(path),'NATIVE_BUNDLE_IDENTITY':identity,'INITIAL_SNAPSHOT_IDENTITY':read(E/'before-route-query-evidence.json')['BEFORE_SNAPSHOT'],'EXPECTED_NATIVE_RESTORE_TYPE':'PersistenceBundle','EXPECTED_BUNDLE':f['canonical_content']['bundle'],'RETAINED_LEDGER_FILES':files,'PLANNED_INITIAL_RESTORES':2,'ACTUAL_RESTORES_EXECUTED':0,'INITIAL_RESTORE_ENTRYPOINT':'adapter.planner.codec.restore(path,expected_identity,repo_root)','AFTER_RESTORE_PRECONDITION':'Exact original current Snapshot, all initial bundle fields, source/policy pins and ledger prefix; compare before record_result','AUTHORITY_REQUIRED':'Separate prospective execution grant must cover initial native restores in both isolated writers','BASELINE_ADDED_OR_AMENDED':False}
(E/'initial-checkpoint-restore-contract.json').write_text(json.dumps(record,sort_keys=True,indent=2)+'\n')
auth=read(E/'authentication.json');auth['FILES'].update(files);(E/'authentication.json').write_text(json.dumps(auth,sort_keys=True,indent=2)+'\n')
for p in E.glob('PROPOSED-*-capture-binding.json'):
 x=read(p);assert x['INITIAL_BUNDLE_IDENTITY']==identity;x['INITIAL_NATIVE_RESTORE_BINDING']={'PATH':str(path),'EXPECTED_IDENTITY':identity,'REPO_ROOT':str(pathlib.Path('.').resolve()),'NATIVE_RETURN':'Original immutable PersistenceBundle; exact comparison before record_result','RESTORE_EXECUTED':False};p.write_text(json.dumps(x,sort_keys=True,indent=2)+'\n')
p=E/'writer-handoff-cold-reader-contracts.json';x=read(p);x['PROCESS_SEQUENCE'][1]='Fresh writer native restore of exact retained checkpoint using initial-checkpoint-restore-contract.json; verify complete initial bundle, Snapshot identity, source/policy pins and 19-event prefix before record_result';x['PLANNED_INITIAL_RESTORES']=2;x['TOTAL_PLANNED_RESTORE_CALLS']=10;p.write_text(json.dumps(x,sort_keys=True,indent=2)+'\n')
p=E/'static-harness-contract.json';x=read(p);x['INITIAL_RESTORE_CONTRACT']='initial-checkpoint-restore-contract.json';p.write_text(json.dumps(x,sort_keys=True,indent=2)+'\n')
p=E/'authority-preparation-eligibility.json';x=read(p);x['INITIAL_RESTORE_SCOPE']='Two writer-owned native restores of the exact original retained checkpoint before record_result; eight later cold restore readers. No new baseline save/amendment.';p.write_text(json.dumps(x,sort_keys=True,indent=2)+'\n')
print(json.dumps({'CHECKPOINT':str(path),'INITIAL_NATIVE_BUNDLE':identity,'VERIFIED_RETAINED_FILES':20,'ACTUAL_RESTORES':0}))
