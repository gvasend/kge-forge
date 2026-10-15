"""Authorized path-only prospective fixture correction. No transitions/save/restore."""
import hashlib,json
from copy import deepcopy
from pathlib import Path
from adapter.planner import codec,model,replay
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;Q=R/'docs/plans/qualification';C6=Q/'E2_P05_D01_A14_SOURCE_PROVENANCE_RECONCILIATION_6';C5=Q/'E2_P05_D01_A14_HANDOFF_CLOSURE_5'
OPTION='AUTHORIZE_BOUNDED_PROSPECTIVE_A14_PROVENANCE_FIXTURE_CORRECTION'
def read(p):return json.loads(Path(p).read_bytes())
def canon(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def qid(v):return 'qualification-A14-provenance-correction-v1:'+sha(canon(v))
def pin(p,ptr=''):
 p=Path(p);return {'path':str(p.relative_to(R)),'pointer':ptr,'raw_sha256':sha(p.read_bytes())}
def save(n,v):(O/n).write_bytes(canon(v)+b'\n')
def at(v,ptr):
 for key in ptr.split('/')[1:]:v=v[int(key)] if isinstance(v,list) else v[key]
 return v
def put(v,ptr,value):
 tokens=ptr.split('/')[1:];node=v
 for key in tokens[:-1]:node=node[int(key)] if isinstance(node,list) else node[key]
 node[tokens[-1]]=value
contract=read(C6/'minimum-correction-contract.json');subject=contract['CORRECTION_CONTRACT_IDENTITY'];body=dict(contract);body.pop('CORRECTION_CONTRACT_IDENTITY');assert qid(body)==subject
dossier=read(C6/'bounded-correction-decision-dossier.json');did=dossier['DOSSIER_IDENTITY'];body=dict(dossier);body.pop('DOSSIER_IDENTITY');assert qid(body)==did
assert dossier['OPTION']==OPTION and dossier['DECISION_SUBJECT']==subject and dossier['DECISION_READY']
assert sha((R/dossier['EXACT_SUBJECT']['path']).read_bytes())==dossier['EXACT_SUBJECT']['raw_sha256']
src=contract['BASE_SNAPSHOT_SOURCE'];path=R/src['path'];assert sha(path.read_bytes())==src['raw_sha256'];packet=read(path);original=packet['canonical_content']['subject'];original_native=codec._unwire(original)
assert codec._wire(codec.snapshot_id(original_native))==contract['BASE_SNAPSHOT_IDENTITY']
save('scope-authentication.json',{'SELECTED_OPTION':OPTION,'SCOPE_AUTHENTICATION':'PASS','AUTHENTICATION_METHOD':'Explicit current user selection matched against exact sealed option, correction subject, dossier identity and raw subject/source hashes; no native authority issuance','SEALED_SUBJECT':subject,'DOSSIER_IDENTITY':did,'DOSSIER_SOURCE':pin(C6/'bounded-correction-decision-dossier.json'),'CORRECTION_SUBJECT_SOURCE':pin(C6/'minimum-correction-contract.json'),'PERMITTED':'Exactly two byte-preserving source files and three path assignments in a new prospective fixture','EXCLUDED':dossier['EXCLUDED'],'OLD_DOSSIER_MODIFIED':False,'NATIVE_AUTHORITIES_ISSUED':0})
sourcepins=[]
for label,commitment in contract['SOURCE_FILE_BYTE_COMMITMENTS'].items():
 raw=commitment['RAW_BYTES_UTF8'].encode('utf-8');assert sha(raw)==commitment['SHA256'];target=R/contract['SOURCE_ROLE_PATHS'][label]
 assert target.relative_to(R).as_posix()==contract['SOURCE_ROLE_PATHS'][label] and not target.is_symlink()
 target.parent.mkdir(parents=True,exist_ok=True)
 if target.exists():assert target.read_bytes()==raw,'EXISTING_SOURCE_CONFLICT'
 else:target.write_bytes(raw) # authorized fixture bytes, not runtime save_bundle or transaction
 assert target.read_bytes()==raw
 identity=model.ArtifactIdentity(model.IdentityKind.CONTENT_IDENTITY,'raw-file-sha256',sha(raw));native_pin=model.ArtifactPin(contract['SOURCE_ROLE_PATHS'][label],identity,model.HashProfile.RAW)
 codec.validate_pin(native_pin);assert codec.load_pinned(R,native_pin)==raw
 sourcepins.append({'SOURCE_LABEL':label,'SOURCE_ARTIFACT':pin(target),'NATIVE_PIN':codec._wire(native_pin),'RAW_BYTE_COUNT':len(raw),'BYTES_BEFORE_SHA256':commitment['SHA256'],'BYTES_AFTER_SHA256':sha(target.read_bytes()),'BYTES_PRESERVED':True,'NATIVE_RAW_PIN_VALIDATION':'PASS','NATIVE_PIN_LOOKUP':'PASS'})
save('physical-source-validation.json',{'ROWS':sourcepins,'PATHS_DISTINCT':sourcepins[0]['SOURCE_ARTIFACT']['path']!=sourcepins[1]['SOURCE_ARTIFACT']['path'],'SAVES_PERFORMED':0,'FIXTURE_SOURCE_FILES_MATERIALIZED':2})
corrected_packet=deepcopy(packet)
for assignment in contract['PROVENANCE_PATH_ASSIGNMENTS']:
 assert at(corrected_packet,assignment['POINTER'])==assignment['EXPECTED_ORIGINAL_VALUE']
 parent=at(corrected_packet,assignment['POINTER'].rsplit('/',1)[0]);assert parent['identity']==assignment['EXPECTED_PROVENANCE_IDENTITY_UNCHANGED']
 put(corrected_packet,assignment['POINTER'],assignment['PROPOSED_VALUE'])
corrected=corrected_packet['canonical_content']['subject']
def diff(a,b,ptr=''):
 if type(a)!=type(b):return [ptr]
 if isinstance(a,dict):
  result=[]
  for key in sorted(set(a)|set(b)):
   result += [ptr+'/'+key] if key not in a or key not in b else diff(a[key],b[key],ptr+'/'+key)
  return result
 if isinstance(a,list):
  if len(a)!=len(b):return [ptr]
  return [d for i,(x,y) in enumerate(zip(a,b)) for d in diff(x,y,ptr+'/'+str(i))]
 return [] if a==b else [ptr]
changed=diff(original,corrected,'/canonical_content/subject');authorized=sorted(a['POINTER'] for a in contract['PROVENANCE_PATH_ASSIGNMENTS']);assert sorted(changed)==authorized and len(changed)==3
reverted=deepcopy(corrected_packet)
for assignment in contract['PROVENANCE_PATH_ASSIGNMENTS']:put(reverted,assignment['POINTER'],assignment['EXPECTED_ORIGINAL_VALUE'])
assert reverted==packet # every field outside the three paths is identical
native=codec._unwire(corrected);model.validate_model(native);raw_snapshot=codec.snapshot_bytes(native);newid=codec._wire(codec.snapshot_id(native));assert newid!=contract['BASE_SNAPSHOT_IDENTITY']
(O/'corrected-prospective-snapshot.json').write_bytes(raw_snapshot+b'\n')
# Store the corrected input subject, not a stale capsule identity/arguments wrapper.
fixture={'SCHEMA':'PROSPECTIVE_A14_AUTHORIZED_PROVENANCE_FIXTURE-1','QUALIFICATION_TYPE':'BOUNDED_PROSPECTIVE_A14_PROVENANCE_FIXTURE_CORRECTION','HISTORICAL_RECONSTRUCTION':False,'ORIGINAL_SNAPSHOT_SOURCE':src,'ORIGINAL_SNAPSHOT_ID':contract['BASE_SNAPSHOT_IDENTITY'],'CORRECTED_SNAPSHOT_ID':newid,'SNAPSHOT_SOURCE':pin(O/'corrected-prospective-snapshot.json','/snapshot'),'SCOPE_AUTHENTICATION':pin(O/'scope-authentication.json'),'CORRECTION_SUBJECT':subject,'PROVENANCE_PATH_CHANGES':changed,'SOURCE_PINS':[r['NATIVE_PIN'] for r in sourcepins],'CONTENT_AUTHORITY_SEMANTIC_FACTS_PRESERVED':True,'FULL_BUNDLE_CLOSURE_READY':False,'A14_HANDOFF_EXECUTABLE':False,'ORIGINAL_117_CAPSULES_EDITED':False}
save('corrected-prospective-fixture.json',fixture)
# Native replay provenance enumeration and the unchanged native pin/type/key/path validators.
provs=replay.provenance_records(native)+[p.provenance for p in native.proof_contracts+native.typed_proofs+native.reevaluations]
bykey={};constraints=[]
for prov in provs:
 model.validate_provenance(prov);p=model.ArtifactPin(prov.path,prov.identity,model.HashProfile.RAW);codec.validate_pin(p);codec._path(R,p.path)
 key=(p.path,p.pointer,p.profile);assert key not in bykey or bykey[key]==p,'RAW_PIN_COLLISION'
 bykey[key]=p
pins=tuple(bykey.values());model.unique(pins,lambda p:(p.path,p.pointer,p.profile))
for p in pins:
 try:actual=codec.load_pinned(R,p);status='PASS';error=None
 except model.PlannerError as exc:status='BLOCKED_OUTSIDE_CORRECTION_SCOPE';error=str(exc)
 constraints.append({'PIN':codec._wire(p),'NATIVE_RAW_KEY_AND_PATH_VALIDATION':'PASS','NATIVE_LOOKUP':status,'ERROR':error})
blocked=[c for c in constraints if c['NATIVE_LOOKUP']!='PASS'];assert blocked
first=next(c for c in blocked if c['PIN']['path']=='E2-DECIDE.json')
save('native-validation-and-replay-preflight.json',{'NATIVE_STRUCTURAL_VALIDATION':'PASS','VALIDATORS':['model.validate_model','model.validate_provenance','model.unique','codec.validate_pin','codec._path','codec.load_pinned','replay.provenance_records (enumeration only)'],'CORRECTION_DUPLICATE_RAW_KEY_PREFLIGHT':'PASS','CORRECTION_NONCANONICAL_PATH_PREFLIGHT':'PASS','REQUIRED_PROVENANCE_PIN_INVENTORY':'PRESENT_DEDUPLICATED_FROM_NATIVE_ENUMERATOR','ALL_PROVENANCE_PHYSICAL_SOURCE_LOOKUP':'BLOCKED_OTHER_SOURCES_MISSING','PIN_ROWS':constraints,'FIRST_REMAINING_NATIVE_LOOKUP_BLOCKER':first,'FULL_NATIVE_BUNDLE_REPLAY':'NOT_RUN_NO_AUTHORIZED_COMPLETE_BUNDLE_OR_POLICY_HISTORY_SELECTION','NO_REPLAY_TRANSITIONS_EXECUTED':True,'NEXT_A14_BLOCKER':'OTHER_DECLARED_RAW_SOURCE_FILES_UNAVAILABLE_AT_EXISTING_SOURCE_ROOT: E2-DECIDE.json (first native provenance traversal lookup); exact root/bytes/currentness outside this grant','PREVIOUS_REPRESENTATION_ERRORS_REMOVED':True})
save('preservation-of-semantics.json',{'ORIGINAL_SUBJECT_SHA256':sha(canon(original)),'CORRECTED_SUBJECT_SHA256':sha(canon(corrected)),'EXACT_CHANGE_POINTERS':changed,'REVERSE_AUTHORIZED_PATH_ASSIGNMENTS_EQUALS_ORIGINAL':True,'CONTENT_IDENTITIES_PRESERVED':True,'AUTHORITY_IDENTITIES_PRESERVED':True,'SEMANTIC_FACTS_PRESERVED':True,'ORIGINAL_SNAPSHOT_ID':contract['BASE_SNAPSHOT_IDENTITY'],'CORRECTED_SNAPSHOT_ID':newid,'SNAPSHOT_IDENTITY_CHANGED':True,'NATIVE_STRUCTURAL_VALIDATION':'PASS','MUTATIONS_APPLIED':0,'AUTHORIZED_PATH_ONLY_FIXTURE_SUBSTITUTIONS':3})
front=read(C5/'updated-operand-inventory.json');assert front['TOTAL_RESOLVED']==52 and front['TOTAL_UNRESOLVED']==59
save('updated-a14-frontier.json',{'PREVIOUSLY_RESOLVED':52,'RESOLVED_BY_CORRECTION':0,'TOTAL_RESOLVED':52,'TOTAL_UNRESOLVED':59,'A14_DEPENDENT_REFERENCES':16,'A14_DEPENDENT_ROWS':read(C5/'a14-dependency-inventory.json')['ROWS'],'REASON_NO_OPERAND_PROMOTED':'Bundle/source, save identity, cold-reader baseline and N02 mutation requirements need separate remaining source/policy/history closure; new Snapshot identity alone is not a bundle/reader binding','CORRECTED_INPUT_ASSOCIATION':pin(O/'corrected-prospective-fixture.json'),'NEXT_A14_BLOCKER':first,'STATIC_HANDOFF_STATUS':'BLOCKED_OTHER_RAW_SOURCE_CLOSURE; prior duplicate/path contradiction removed for corrected input','INVOCATION_STATIC_PREFLIGHT':'NOT_RUN','NEXT_DECISION_DOSSIER':'NOT_READY; no unique scoped correction for other source/root/policy/history gaps specified','A14_EXECUTED':False,'D01_QUALIFICATION_CASES_EXECUTED':0,'SAVES_PERFORMED':0,'COLD_READERS_EXECUTED':0})
print(json.dumps({'SCOPE_AUTHENTICATION':'PASS','PROVENANCE_PATH_CHANGES':3,'CORRECTED_SNAPSHOT_ID':newid,'MODEL_VALIDATION':'PASS','NEXT_BLOCKER':first['PIN']['path'],'COUNTS':'52/59_UNCHANGED'}))
