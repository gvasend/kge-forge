"""Exclusive append-only material publication after independent verification."""
import os,json
from pathlib import Path
from adapter.controller_authority_store import ControllerAuthorityStore,_directory,_put,outside,encoded,sha
OUT=Path(__file__).resolve().parent
load=lambda n:json.loads((OUT/n).read_bytes())
proof=load('INDEPENDENT_RECONSTRUCTION.json');assert proof['result']=='PASS'
selection=load('PREPARED_STORE.json');assert proof['private_store']==selection
release=load('PD06_AMENDMENT_DECISION.json');dispatch=load('ARCHITECT_DISPATCH_AMENDMENT.json')
for p,h in load('PRESERVED_STATE.json').items():assert sha(Path(p).read_bytes())==h
q=load('CONSUMPTION_QUALIFICATION.json')
for p,h in q['implementation']['current'].items():assert sha(Path(p).read_bytes())==h
# Preserve all historical evidence fingerprints; no 716-path migration.
inv=json.loads((OUT.parent/'controller_authority_store_2026-09-17/qualified/REFERENCE_CLASSIFICATION.json').read_bytes())
assert inv['total']==716
for r in inv['references']:assert sha(Path(r['evidence']['path']).read_bytes())==r['evidence']['sha256']
store=ControllerAuthorityStore(**selection)
try:
 private=store.root.parent/'material-amendment-publication-2026-09-17'
 outside(private,store.catalog['programmer_roots'])
 for identity in store.catalog['objects']:store.resolve(identity)
 record={'event':'material_supervisor_authority_amendment_published','schema':'PD06-MATERIAL-PUBLICATION-1',
  'architect_authority':load('ARCHITECT_AUTHORIZATION.json'),
  'predecessor_private_adoption':json.loads((OUT.parent/'controller_authority_store_adoption_2026-09-17/PRIVATE_BOOTSTRAP_PIN.json').read_bytes()),
  'amendment_identity':release['amendment_identity'],'release_amendment_decision':release['id'],
  'resulting_release_authority':release['resulting_release_authority'],'dispatch_amendment':dispatch['id'],
  'dispatch_amendment_file_sha256':sha((OUT/'ARCHITECT_DISPATCH_AMENDMENT.json').read_bytes()),
  'material_application':load('MATERIAL_RELEASE_APPLICATION.json'),'selected_store':selection,
  'prepublication_independent_reconstruction_sha256':sha((OUT/'INDEPENDENT_RECONSTRUCTION.json').read_bytes()),
  'accepted_succession_implementation':q['accepted_succession_implementation'],'consumption_implementation':q['implementation_identity'],
  'historical_reference_fingerprints_verified':716,'original_PD06_rewritten':False,'state':'INACTIVE','ownership':'NONE',
  'S2_launched':False,'succession_event':None,'E1_activation_events_created':0,'E1_model_requests':0,'E1_implementation_effects':0,
  'selection_semantics':'Append-only material release and explicit dispatch amendment; original authorities immutable. This external private pin selects the authenticated application and qualified implementation, not a successor or launch.'}
 data=encoded(record);private.mkdir(mode=0o700);fd=_directory(private)
 try:_put(fd,'PUBLICATION_RECORD.json',data);os.fsync(fd)
 finally:os.close(fd)
 fd=_directory(private.parent)
 try:os.fsync(fd)
 finally:os.close(fd)
 with (OUT/'PUBLICATION_RECORD.json').open('xb') as f:f.write(data)
 pin={'path':str(private/'PUBLICATION_RECORD.json'),'sha256':sha(data),'role':'Documentary receipt of externally selected private publication pin'}
 with (OUT/'PRIVATE_PUBLICATION_PIN.json').open('xb') as f:f.write(encoded(pin))
 print(json.dumps(pin),flush=True)
finally:store.close()
