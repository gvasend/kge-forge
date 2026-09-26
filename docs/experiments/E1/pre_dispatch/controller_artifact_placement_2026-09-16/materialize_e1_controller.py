from pathlib import Path
import json,os,sys,importlib
from adapter.context_projection import canonical,digest,sha,read_exact
from adapter.governance_continuation import reference,GovernanceContinuation
R=Path('/home/gvasend/app/kge-forge');B=R/'docs/experiments/E1/pre_dispatch';A=B/'complete_continuation_adoption_2026-09-16';O=B/'controller_artifact_placement_2026-09-16';S=Path('/tmp/kge-forge-e1-controller/auth-e1-wp-001-r7-94f511dfcdcc43ac837191f8732ced39')
O.mkdir(exist_ok=False)
def load(p):return json.loads(Path(p).read_bytes())
def write(name,v):
 p=O/name;p.write_text(canonical(v));return reference(p)
op=load(A/'OPERATIONAL_BINDING.json');spec=op['governance'];profile_ref=spec['released_profile'];profile_bytes=read_exact(profile_ref['path'],profile_ref['sha256']);profile= json.loads(profile_bytes)
launch=load(op['released_launch']['path']);auth=launch['authorization'];roots=tuple(Path(x) for x in set(auth['read_roots']+auth['write_roots']+auth['write_directory_roots']+[profile['runtime']['cwd']]))
def outside(p):return all(p!=r and r not in p.parents for r in roots)
assert outside(S) and S.is_absolute()
# Explicit controller-owned ancestors; never follow an existing symlink.
for p in reversed([S,*S.parents]):
 if p in (Path('/'),Path('/tmp')):continue
 if p.exists():assert not p.is_symlink() and p.is_dir() and p.stat().st_uid==os.getuid() and p.stat().st_mode&0o077==0
 else:p.mkdir(mode=0o700)
def put(data):
 h=sha(data);p=S/h
 if p.exists():assert read_exact(str(p),h)==data
 else:
  fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
  with os.fdopen(fd,'wb') as f:f.write(data);f.flush();os.fsync(f.fileno())
 return {'path':str(p),'sha256':h}
# Observe only exact reads made by read-only production ancestry reconstruction.
# The wrapper returns the original function's bytes and preserves every denial.
for name in ['adapter.context_binding','adapter.authorization_lifecycle','adapter.activation_transaction','adapter.continuation_envelope']:importlib.import_module(name)
observed={}
def trace(path,h):
 data=read_exact(path,h);observed[(str(path),h)]=data;return data
patched=[]
for module in list(sys.modules.values()):
 if module and getattr(module,'__name__','').startswith('adapter.') and getattr(module,'read_exact',None) is read_exact:
  patched.append(module);module.read_exact=trace
try:
 env={};source=Path('/tmp/adopt_complete_e1.py').read_text().split("if len(sys.argv)>1 and sys.argv[1]=='reconstruct':")[0];exec(compile(source,'inventory-reconstruction','exec'),env)
 real_auth,audit,dispatch,verification=env['reconstruct']()
finally:
 for module in patched:module.read_exact=read_exact
# Direct bootstrap inputs read before the exact-read verifier begins.
for name in ['ADOPTION_RECORD.json','OPERATIONAL_BINDING.json','ADOPTED_SPECIFICATION.json','ISSUED_APPROVAL.json','ARCHITECT_ADOPTION_AUTHORITY.json']:
 p=A/name;observed[(str(p),sha(p.read_bytes()))]=p.read_bytes()
observed[(profile_ref['path'],profile_ref['sha256'])]=profile_bytes
inventory=[]
for (path,h),data in sorted(observed.items()):
 p=Path(path)
 # Live source/code reads remain current-context checks, not relocatable history.
 if '/blobs/' not in path and (p.suffix=='.py' or str(p) in real_auth.context_binding.protected_paths):continue
 if not path.startswith(str(B)+'/'):continue
 dest=put(data);assert outside(Path(dest['path']))
 inventory.append({'historical_reference':{'path':path,'sha256':h},'controller_copy':dest,'location_defect':not outside(p),'authoritative_selection':'NOT_BOUND: materialized candidate only'})
copy=put(profile_bytes);assert copy['sha256']==profile_ref['sha256'] and digest(json.loads(read_exact(copy['path'],copy['sha256'])))==launch['profile_sha256']
fd=os.open(S,os.O_RDONLY|os.O_DIRECTORY);os.fsync(fd);os.close(fd)
record={'result':'MATERIALIZED_NOT_OPERATIONALLY_BOUND','ReleasedProfileContentId':{'bytes_sha256':profile_ref['sha256'],'canonical_profile_fingerprint':digest(profile)},'OperationalProfileLocation':copy['path'],'profile_bytes_identical':True,'private_root':str(S),'root_mode':'0700','object_mode':'0600','outside_read_list_search_write_patch_and_cwd_roots':True,'inventory':inventory,'original_profile_unchanged':reference(Path(profile_ref['path'])),'implementation_changed':False}
write('MATERIALIZATION.json',record)
(S/'MATERIALIZATION_RECEIPT.json').write_text(canonical(record));(S/'MATERIALIZATION_RECEIPT.json').chmod(0o600)
# Exact production acceptance of a location-only operational reference change.
# This is a candidate in memory; the adopted specification remains untouched.
candidate=json.loads(canonical(spec));candidate['released_profile']=copy
try:GovernanceContinuation(candidate)
except Exception as exc:
 result={'result':'BLOCKED','operation':'production OPERATIONAL-CONTINUATION-1 verification of byte-identical profile location substitution','exception':type(exc).__name__,'reason':str(exc),'candidate_not_applied':True,'profile_copy':copy,'profile_content_unchanged':True,'production_implementation_changed':False,'activation_attempted':False,'activation_event':None,'ownership_reservation':None,'model_handoff_eligible':False,'E1_model_requests':0,'E1_implementation_effects':0,'current_operational_identities':spec['identities'],'current_context_identities':op['context_identities'],'dispatch_inheritance_for_unchanged_adopted_context':'PASS (read-only reconstruction)','relocated_binding_dispatch_inheritance':'NOT REACHED','qualification':'INCOMPLETE: production location binding rejected; no claim of integrated relocation qualification','required_mechanism':'Content-preserving operational location indirection is not represented by the current canonical verifier, which compares the full released_profile reference (path and hash) to the historical anchor. A production change and qualified continuation are needed; none was applied in this failed attempt.'}
 write('PLACEMENT_VALIDATION_BLOCKED.json',result)
 print(canonical({'profile':copy,'materialized_artifacts':len(inventory),'result':result}));sys.exit(2)
raise AssertionError('Unexpected acceptance: no further effect authorized by this evidence script')
