"""Exact authorized one-time bootstrap; no invocation, model or governed effects."""
import json,sys,os,time,shutil,signal
from pathlib import Path
O=Path(__file__).resolve().parent;Q=O.parent/'runtime_bootstrap_2026-09-19'
sys.path.insert(0,str(Q/'candidate'))
from adapter import runtime_bootstrap as b, runtime_adoption as r
from adapter.controller_authority_store import ControllerAuthorityStore,encoded,sha,outside,_directory,_put
start=time.monotonic();signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('bootstrap 120s hard phase limit')));signal.alarm(120)
pub=json.loads((Q/'PUBLICATION.json').read_bytes());package=json.loads((Q/'PROPOSED_AUTHORIZATION_PACKAGE.json').read_bytes());record=json.loads((Q/'PROPOSED_BOOTSTRAP_RECORD.json').read_bytes());policy=json.loads((Q/'PROPOSED_RUNTIME_HEAD_AUTHORITY.json').read_bytes())
assert record['id']=='RUNTIME-AUTHORITY-BOOTSTRAP-sha256:7837030f70d5545b8ba3ac466317b5b7b15e29950bf0056a1d5eeaeda23b1239'
assert sha((Q/'PROPOSED_BOOTSTRAP_RECORD.json').read_bytes())=='84f838bf3c655f75e75b8f4532081c3e5d4c9e532d7b6fb6776a98c7b9b688c6'
for filename,key in [('PROPOSED_MATERIAL_AMENDMENT.json','material_amendment_file_sha256'),('PROPOSED_RUNTIME_HEAD_AUTHORITY.json','head_authority_file_sha256')]:assert sha((Q/filename).read_bytes())==pub[key]
r.unseal('RUNTIME-AUTHORITY-BOOTSTRAP',record);r.unseal('RUNTIME-HEAD-AUTHORITY',policy)
assert record['consumer_files']=={f.name:sha(f.read_bytes()) for f in (Q/'candidate/adapter').glob('*.py')}
# Historical closure tests are evidence, never a substitute for fresh preflight.
assert 'Ran 20 tests' in (Q/'TESTS.log').read_text() and (Q/'TESTS.log').read_text().rstrip().endswith('OK')
for name in ('ORDINARY_SUCCESSORS.log','DISTINCT_COMPETITORS.log'):assert (Q/name).read_text().rstrip().endswith('OK')
for filename in ('ACTUAL_IDENTITY_QUALIFICATION.json','QUALIFIED_BOOTSTRAP_RECORD.json','QUALIFIED_HEAD_POLICY.json'):
 index=json.loads((Q/'EVIDENCE_HASHES.json').read_bytes());assert sha((Q/filename).read_bytes())==index[filename]
base=ControllerAuthorityStore(**package['base_objects']);records={}
with base.session():
 for key in base.catalog['objects']:
  if key not in (r.POLICY,b.SELECTOR):records[key]={'bytes':base.resolve(key),'evidence':[]}
base.close()
for key,v in package['objects'].items():
 data=encoded(v);assert key=='sha256:'+sha(data);records[key]={'bytes':data,'evidence':[]}
selector_data=encoded(package['proposed_selector']);selector_key='sha256:'+sha(selector_data);records[selector_key]={'bytes':selector_data,'evidence':[]}
source={'schema':'ARCHITECT-RUNTIME-BOOTSTRAP-ADOPTION-1','authority':'Architect','channel':'user','decision':'ONE-TIME RUNTIME-AUTHORITY BOOTSTRAP ADOPTION AUTHORIZED',
 'bootstrap':record['id'],'bootstrap_file_sha256':sha(encoded(record)),'amendment':record['material_amendment'],'runtime_head_authority':record['runtime_head_authority'],
 'predecessor':record['legacy_runtime'],'successor':record['successor_runtime'],'consumer_files':record['consumer_files'],'release_context':record['release_context'],
 'scope':'Exact selected one-time bootstrap only; no r13 or real invocation/model/effects',
 'recorded_wall_time':time.time()}
sdata=encoded(source);sr={'authority_id':'sha256:'+sha(sdata),'sha256':sha(sdata)};records[sr['authority_id']]={'bytes':sdata,'evidence':[]}
# Use all actual Programmer roots, not merely the narrower qualification roots.
req=json.loads(records[record['legacy_verifier']['input']['authority_id']]['bytes']);oldpub=json.loads(Path(req['publication']['path']).read_bytes());assert sha(Path(req['publication']['path']).read_bytes())==req['publication']['sha256']
old=ControllerAuthorityStore(**oldpub['selected_store']);roots=list(old.catalog['programmer_roots']);old.close()
root=Path(package['intended_private_lineage_directory']);outside(root,roots)
assert root.is_dir() and not (root/'AUTHORIZED_SELECTION.json').exists()
assert (root/'authority').is_dir() and not (root/'authority/catalog.json').exists()
for filename in ('bootstrap.jsonl','runtime.jsonl'):
 assert (root/filename).read_bytes()==b'', 'nonempty lineage: stop'
assert not (root/'authority-complete').exists(), 'corrected provisioning already attempted'
store=ControllerAuthorityStore.materialize(root/'authority-complete',records,{r.POLICY:package['head_policy']['authority_id'],b.SELECTOR:selector_key},
 {'authority_source':sr,'release_identities':record['release_context']},{'runtime_head_authority':policy['id']},roots,
 {policy['journal']:{'path':str(root/'runtime.jsonl'),'mutation':'APPEND_ONLY','mechanism':'RUNTIME-ADOPTION-JOURNAL-1'},policy['bootstrap_journal']:{'path':str(root/'bootstrap.jsonl'),'mutation':'APPEND_ONLY','mechanism':'ONE-TIME-RUNTIME-BOOTSTRAP-1'}})
pin={'root':str(store.root),'catalog_sha256':store.catalog_sha256,'applicability':store.applicability}
plan={'schema':'AUTHORIZED-RUNTIME-BOOTSTRAP-SELECTION-1','selected_store':pin,'consumer_root':str(Q/'candidate'),'bootstrap_id':record['id'],'bootstrap_sha256':sha(encoded(record)),'source':sr,'lineage_root':str(root)}
fd=_directory(root)
try:_put(fd,'AUTHORIZED_SELECTION.json',encoded(plan));os.fsync(fd)
finally:os.close(fd)
(O/'AUTHORIZED_SELECTION.json').write_bytes(encoded(plan))
try:
 result=b.establish(store)
 assert result['runtime']==pub['candidate_R1'] and result['state']=='SUCCESSOR_CURRENT'
 (O/'APPLICATION_RESULT.json').write_bytes(encoded({'result':'APPLIED','reconstruction':result,'seconds':time.monotonic()-start,'bootstrap':record['id'],'amendment':record['material_amendment'],'source':sr}))
 print(encoded({'result':'APPLIED','state':result,'seconds':time.monotonic()-start}).decode())
except BaseException as e:
 (O/'APPLICATION_FAILURE.json').write_bytes(encoded({'error':type(e).__name__+': '+str(e),'seconds':time.monotonic()-start,'selection':plan,'no_automatic_retry':True}));raise
finally:store.close();signal.alarm(0)
