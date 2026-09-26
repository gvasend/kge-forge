"""Freeze a content-addressed, unreleased PD06 evidence candidate; never activate."""
import hashlib,json,os,subprocess,sys
from pathlib import Path
ROOT=Path('/home/gvasend/app/kge-forge');sys.path.insert(0,str(ROOT))
from adapter.context_binding import CommittedContext
from adapter.runnable_profile import canonical,validate,ARGV,INPUTS
from adapter.model_transport import validate as validate_transport
from adapter.committed_objects import object_bytes
from adapter.recovery_ledger import _observe,CGROUP_BASE,SUPERVISOR_AUDIT
from adapter.invocation_ownership import InvocationOwnership
from adapter.launch_profile import LEDGER
PRE=ROOT/'docs/experiments/E1/pre_dispatch';OUT=PRE/'pd06_release_evidence'
sha=lambda data:hashlib.sha256(data).hexdigest()
def write(path,value):path.write_text(json.dumps(value,indent=2)+'\n')
b=CommittedContext(PRE/'CONTEXT_MANIFEST.json','5871bdce4f5b6539c84f69f4f2b2f94ee31be5cd');assert b.verify()
p=json.loads((OUT/'PROPOSED_PRODUCTION_PROFILE.json').read_text())
launch=json.loads((OUT/'PRODUCTION_LAUNCH_RECORD.json').read_text())
assert sha(canonical(p).encode())==(OUT/'PROFILE_SHA256.txt').read_text().strip()==launch['profile_sha256']
validate(p['runtime'],ARGV,str(ROOT),list(INPUTS))
validate_transport(p['model_transport'],p['model_transport']['endpoint'],p['model_transport']['model'])
assert p['state']=='INACTIVE' and not any(launch[k] for k in ('RELEASED','ELIGIBLE','DISPATCHED'))
assert InvocationOwnership(LEDGER).active() is None
for sub in ('execution','failed_attempt'):
 assert InvocationOwnership(OUT/sub/'ownership.jsonl').active() is None
states={d.name:_observe(d) for d in CGROUP_BASE.iterdir() if d.is_dir() and d.name.startswith('scope-')}
assert all(not row['members'] and row['populated']==0 for row in states.values())
events=[json.loads(x) for x in SUPERVISOR_AUDIT.read_text().splitlines()]
created={e.get('scope_id') for e in events if e.get('event')=='scope_created'}
closed={e.get('scope_id') for e in events if e.get('event')=='scope_closed'}
assert created<=closed
write(OUT/'FINAL_SCOPE_VERIFICATION.json',{'scope_states':states,'unclosed_scopes':sorted(created-closed),
 'common_E1_ownership':None,'scratch_ownership':None,'E1_INACTIVE':True})
# Verify the committed docs tree lacks the implementation directory too.
derivation=json.loads((OUT/'provisioning/BASELINE_DERIVATION.json').read_text())
kind,tree,_=object_bytes(ROOT,derivation['entries']['docs']['oid']);assert kind=='tree'
docs={}
while tree:
 head,_,tail=tree.partition(b'\0');mode,name=head.split(b' ',1)
 docs[name.decode()]={'mode':mode.decode(),'oid':tail[:20].hex()};tree=tail[20:]
assert 'implementation' not in docs
write(OUT/'PROVISIONING_DOCS_BASELINE.json',{'revision':derivation['revision'],
 'docs_tree':derivation['entries']['docs']['oid'],'entries':docs,'implementation_absent':True})
# The runtime fixture used the same final execution spec and transmission policy schema.
live=json.loads((OUT/'execution/LIVE_REPORT.json').read_text())
assert live['result']=='PASS' and json.loads((OUT/'boundary/BOUNDARY_REPORT.json').read_text())['result']=='PASS'
assert 'Ran 48 tests' in (OUT/'regression.txt').read_text() and (OUT/'regression.txt').read_text().rstrip().endswith('OK')
assert all(sha((ROOT/rel).read_bytes())==value for rel,value in json.loads((OUT/'SOURCE_SHA256.json').read_text()).items())
# Add the current literal source revision; worktree fingerprint is separately bound.
revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=str(ROOT),text=True).strip()
paths=set((ROOT/'adapter').rglob('*.py'))
paths.update(b.protected_paths)
paths.update(q for q in PRE.rglob('*') if q.is_file() and '__pycache__' not in q.parts
 and 'captures' not in q.parts and q.name not in ('CAPTURE_REFERENCE.json','FINAL_FINGERPRINT_VERIFICATION.json'))
paths.update(Path(row['path']) for row in p['runtime']['executables'])
paths.add(Path(p['model_transport']['ca_file']))
paths.add(Path(launch['audit_destination']));paths.add(Path(LEDGER));paths.add(SUPERVISOR_AUDIT)
for row in p['supervisor_binding']: paths.add(Path(row['exe']))
inputs={};content={}
for path in sorted(paths):
 assert path.is_file(),str(path)
 data=path.read_bytes();value=sha(data)
 inputs[str(path)]={'sha256':value,'bytes':len(data)};content[value]=data
# Exact post-provision directory identities and entries are part of the state capture.
directories={}
for row in p['provisioning_plan']['directories']:
 path=Path(row['path']);assert path.is_dir() and not path.is_symlink()
 st=path.stat();directories[str(path)]={'device':st.st_dev,'inode':st.st_ino,
 'mode':st.st_mode,'entries':sorted(child.name for child in path.iterdir())}
manifest={'schema':'E1-RELEASE-CAPTURE-CANDIDATE-1','baseline':'E1-ARCH-1','work':'E1-WP-001',
 'implementation_HEAD':revision,'implementation_worktree_sha256':sha(canonical(json.loads((OUT/'SOURCE_SHA256.json').read_text())).encode()),
 'profile_sha256':launch['profile_sha256'],'committed_context':{'capture':b.capture_commit,'sha256':b.digest},
 'authority_supplement':str(OUT/'ARCHITECT_AUTHORITY.md'),
 'QUALIFIED':True,'RELEASED':False,'ELIGIBLE':False,'DISPATCHED':False,'E1':'INACTIVE',
 'PD05':'Architect PASS','PD06':'UNRELEASED / content-clearance selection pending',
 'inputs':inputs,'post_provision_directories':directories,
 'limitation':'Content-addressed read-only snapshot, not privileged write-once storage. Future changes require recapture.'}
encoded=canonical(manifest).encode();fingerprint=sha(encoded)
capture=OUT/'captures'/fingerprint;capture.mkdir(parents=True,exist_ok=False)
blobs=capture/'blobs';blobs.mkdir()
for key,data in content.items():
 dest=blobs/key;dest.write_bytes(data);dest.chmod(0o444)
(capture/'MANIFEST.json').write_bytes(encoded);(capture/'MANIFEST.json').chmod(0o444)
# Independently re-read authoritative inputs and stored blobs after construction.
for raw,row in inputs.items():
 assert sha(Path(raw).read_bytes())==row['sha256'],raw
 assert sha((blobs/row['sha256']).read_bytes())==row['sha256'],raw
for raw,row in directories.items():
 path=Path(raw);st=path.stat()
 assert not path.is_symlink() and (st.st_dev,st.st_ino,st.st_mode)==(row['device'],row['inode'],row['mode'])
 assert sorted(child.name for child in path.iterdir())==row['entries']
assert sha((capture/'MANIFEST.json').read_bytes())==fingerprint
identifier='E1-PD06-CANDIDATE-20260916-'+fingerprint[:16]
write(OUT/'CAPTURE_REFERENCE.json',{'identifier':identifier,'manifest':str(capture/'MANIFEST.json'),
 'capture_sha256':fingerprint,'profile_sha256':launch['profile_sha256'],
 'hash_definition':'SHA256(canonical compact sorted-key JSON); manifest input hashes bind exact file bytes',
 'RELEASED':False,'ELIGIBLE':False,'DISPATCHED':False})
write(OUT/'FINAL_FINGERPRINT_VERIFICATION.json',{'result':'PASS','capture_sha256':fingerprint,
 'profile_sha256':launch['profile_sha256'],'input_count':len(inputs),'unique_blobs':len(content),
 'authoritative_inputs_match':True,'stored_blobs_match':True,'directory_state_matches':True,
 'PD06_readiness':'BLOCKED: production reasoning-context/content clearance pending',
 'E1':'INACTIVE','E1_WP_001':'INELIGIBLE AND UNDISPATCHED'})
print(json.dumps({'identifier':identifier,'capture_sha256':fingerprint,'profile_sha256':launch['profile_sha256'],'inputs':len(inputs)}))
