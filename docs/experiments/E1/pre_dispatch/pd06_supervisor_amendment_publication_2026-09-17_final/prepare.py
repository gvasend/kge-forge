"""Prepare exact private material authority; publication is a separate final pin.
No activation, ownership lock, host intervention or model transport is called.
"""
import json, os
from pathlib import Path
from adapter.context_projection import canonical,digest,sha
from adapter.supervisor_amendment import seal,material_identities
from adapter.controller_authority_store import ControllerAuthorityStore,encoded
from adapter.continuation_envelope import historical_operation
ROOT=Path.cwd();OUT=Path(__file__).resolve().parent;PRE=OUT.parent
OLD=PRE/'pd06_supervisor_authority_amendment_2026-09-17';FROZEN=PRE/'supervisor_succession_2026-09-17'
def load(p):return json.loads(Path(p).read_bytes())
def write(name,obj):
 p=OUT/name;data=encoded(obj)
 if p.exists():assert p.read_bytes()==data,str(p)
 else:
  with p.open('xb') as f:f.write(data)
 return {'authority_id':'sha256:'+sha(data),'sha256':sha(data)}
def file_ref(p):return {'authority_id':'sha256:'+sha(Path(p).read_bytes()),'sha256':sha(Path(p).read_bytes())}
def evidence(p):return {'path':str(p),'sha256':sha(p.read_bytes())}
candidate=load(OLD/'PD06_AMENDMENT_CANDIDATE.json');cid=candidate['amendment_candidate_identity'];rid=candidate['proposed_release_authority_identity']
assert sha((OLD/'PD06_AMENDMENT_CANDIDATE.json').read_bytes())=='5a73a14859ddf63a733fcc1941a0a744f9c399863ef7eaf8f6889c4e769d0eae'
assert cid=='PD06-SUPERVISOR-AUTHORITY-AMENDMENT-sha256:979201e9e2d4269a483ce904ae4e7f9329ab0378836e7ada59070b3e4636d3b6'
assert rid=='E1-RELEASE-AUTHORITY-sha256:c0d6aed0894c9d07945b017423b3bb2fedb7207780b5e3d4e6c928aacb82bae3'
pin=load(PRE/'controller_authority_store_adoption_2026-09-17/PRIVATE_BOOTSTRAP_PIN.json');assert sha(Path(pin['path']).read_bytes())==pin['sha256']
adoption=load(pin['path']);old=ControllerAuthorityStore(**adoption['selected_store']);authid=old.applicability['authorization_id']
raw=json.loads(old.resolve(authid));op=json.loads(raw['operational_binding']);parent=op['governance'];inv=parent['authority_invariants']
# Before-state immutable evidence of actual audits, ownership and prior selection.
state={str(Path(pin['path'])):pin['sha256']}
for v in old.catalog['private_state'].values():state[v['path']]=sha(Path(v['path']).read_bytes())
write('PRESERVED_STATE.json',state)
source=write('ARCHITECT_AUTHORIZATION.json',{'authority':'Architect','channel':'user','date':'2026-09-17',
 'decision':'AUTHORIZE_MATERIAL_RELEASE_AND_DISPATCH_AMENDMENT',
 'accepted':{'amendment_identity':cid,'candidate_file_sha256':file_ref(OLD/'PD06_AMENDMENT_CANDIDATE.json')['sha256'],
             'resulting_release_authority':rid,'succession_implementation':candidate['body']['required_implementation_identity']},
 'authorize_dispatch_amendment_for':authid,
 'authorization_quote':'The Architect accepts and authorizes the narrowly scoped PD-06 Supervisor Authority Amendment. Publish this as an append-only material release amendment. Create a narrowly scoped Architect amendment to the existing dispatch authorization. The amendment changes only the supervisor readiness binding. All other original dispatch conditions remain exactly unchanged. Implement and qualify production verification of original PD-06 release -> material Supervisor Authority Amendment and original Architect dispatch authorization -> Architect dispatch amendment.',
 'source_title':'ARCHITECT MATERIAL RELEASE AMENDMENT AUTHORIZATION, current user instruction',
 'human_host_authorization':None,'specific_successor_authorization':None,
 'prohibited':['install host package','execute host launch','authorize unidentified S2','activate E1','acquire E1 ownership','make E1 model request','dispatch E1-WP-001']})
release=seal('PD06-SUPERVISOR-AMENDMENT-DECISION',{'schema':'PD06-SUPERVISOR-AMENDMENT-DECISION-1',
 'authority':'Architect','decision':'AUTHORIZE_MATERIAL_SUPERVISOR_AMENDMENT','candidate':file_ref(OLD/'PD06_AMENDMENT_CANDIDATE.json'),
 'amendment_identity':cid,'resulting_release_authority':rid,
 'original_release':{k:parent['identities'][k] for k in ('ReleaseBasisId','ReleaseDecisionId')},
 'authority_source':source,'successor_instance_id':None,'succession_authorization':None,'host_authorization':None})
rr=write('PD06_AMENDMENT_DECISION.json',release)
original_dispatch=PRE/'dispatch_authorization_2026-09-16/DISPATCH_RECORD.json'
dispatch=seal('ARCHITECT-DISPATCH-AMENDMENT',{'schema':'ARCHITECT-DISPATCH-AMENDMENT-1','authority':'Architect',
 'decision':'AMEND_SUPERVISOR_READINESS_ONLY','authority_source':source,'release_amendment_decision':release['id'],
 'original_release':release['original_release'],'resulting_release_authority':rid,'amendment_identity':cid,
 'historical_S1':candidate['body']['historical_S1_evidence_identity'],
 'succession_implementation':candidate['body']['required_implementation_identity'],
 'predecessor_operational_ancestry':parent['identities'],'authorization_id':authid,'unchanged_authorities':inv,
 'changed_condition':'supervisor_readiness_only','successor_instance_id':None,'succession_authorization':None,
 'all_other_original_conditions_unchanged':True,'original_dispatch':file_ref(original_dispatch),
 'original_dispatch_identity':'E1-ARCHITECT-DISPATCH-sha256:'+file_ref(original_dispatch)['sha256']})
dr=write('ARCHITECT_DISPATCH_AMENDMENT.json',dispatch)
# Validate frozen qualified closure. No original evidence file is rewritten.
records={}
for identity,item in old.catalog['objects'].items():records[identity]={'bytes':old.resolve(identity),'evidence':item['evidence']}
seen=set()
def import_ref(ref):
 if 'path' not in ref:return
 if 'sha256:'+ref['sha256'] in records:return
 p=Path(ref['path']);data=p.read_bytes();assert sha(data)==ref['sha256'],str(p)
 records['sha256:'+sha(data)]={'bytes':data,'evidence':[{'path':str(p),'sha256':sha(data)}]}
 if sha(data) in seen:return
 seen.add(sha(data))
 if p.parent.name=='blobs':return
 try:value=json.loads(data)
 except (ValueError,UnicodeError):return
 visit(value)
 if isinstance(value,dict) and ('inputs' in value or 'current_inputs' in value) and (p.parent/'blobs').is_dir():
  for row in value.get('current_inputs',value.get('inputs')).values():
   if isinstance(row,dict) and 'sha256' in row:
    blob=p.parent/'blobs'/row['sha256']
    if blob.exists():import_ref({'path':str(blob),'sha256':row['sha256']})
def visit(obj):
 if isinstance(obj,dict):
  if set(obj)=={'path','sha256'}:import_ref(obj)
  else:
   for v in obj.values():visit(v)
 elif isinstance(obj,list):
  for v in obj:visit(v)
# Restrict traversal to accepted amendment and qualification closure.
import_ref(evidence(OLD/'PD06_AMENDMENT_CANDIDATE.json'))
inventory=load(OLD/'QUALIFIED_IMPLEMENTATION_IDENTITY.json')
assert 'sha256:'+digest(inventory['inventory'])==candidate['body']['required_implementation_identity']
for p,h in inventory['inventory']['controller'].items():
 frozen=FROZEN/'candidate/adapter'/Path(p).name
 assert sha(frozen.read_bytes())==h
assert sha((FROZEN/'host_launch.py').read_bytes())==inventory['inventory']['host_launcher']
# Full accepted implementation and exact consumption overlay are separately bound.
before={str(ROOT/p):h for p,h in load(FROZEN/'IMPLEMENTATION_BEFORE.json').items() if Path(p).parent==Path('adapter')}
final={str(p):sha(p.read_bytes()) for p in (ROOT/'adapter').glob('*.py')}
cap=OUT/'qualification';cap.mkdir();(cap/'blobs').mkdir();inputs={}
for p,h in final.items():
 data=Path(p).read_bytes();(cap/'blobs'/h).write_bytes(data);inputs[p]={'sha256':h}
for p in (ROOT/'adapter/tests/test_supervisor_amendment.py',OUT/'AMENDMENT_PROBES.log',OUT/'REGRESSION_TESTS.log',OUT/'ISOLATION_RETRY.log',OUT/'CURRENT_REGRESSION.log'):
 data=p.read_bytes();h=sha(data);(cap/'blobs'/h).write_bytes(data);inputs[str(p)]={'sha256':h}
for name in ('AMENDMENT_PROBES.log','ISOLATION_RETRY.log','CURRENT_REGRESSION.log'):
 assert (OUT/name).read_text().rstrip().endswith('OK'),name
capref=write('qualification/MANIFEST.json',{'schema':'EXACT-MATERIAL-IMPLEMENTATION-CAPTURE-1','current_inputs':inputs})
q={'schema':'SUPERVISOR-AMENDMENT-CONSUMPTION-QUALIFICATION-1','result':'PASS',
 'classification':'MATERIAL_RELEASE_IMPLEMENTATION','authority_source':source,
 'accepted_succession_implementation':inventory['identity'],'accepted_inventory':file_ref(OLD/'QUALIFIED_IMPLEMENTATION_IDENTITY.json'),
 'authority_invariants':inv,'implementation':{'predecessor':before,'current':final},
 'implementation_identity':'sha256:'+digest(final),'capture':evidence(cap/'MANIFEST.json'),
 'probes':[file_ref(OUT/'AMENDMENT_PROBES.log'),file_ref(OUT/'REGRESSION_TESTS.log'),file_ref(OUT/'ISOLATION_RETRY.log'),file_ref(OUT/'CURRENT_REGRESSION.log')],
 'scope':'Exact frozen succession base plus authenticated material-release/dispatch consumption; not a non-material continuation.'}
qr=write('CONSUMPTION_QUALIFICATION.json',q)
prior_path=OUT.parent/'pd06_supervisor_amendment_publication_2026-09-17/PUBLICATION_RECORD.json'
prior=load(prior_path)
import_ref(evidence(prior_path))
selected={'release_decision':rr,'dispatch_amendment':dr,'implementation_qualification':qr,
 'prior_publication':file_ref(prior_path),'application_predecessor':prior['material_application']['identities']}
spec={'schema':3,'predecessor':parent,**{k:parent[k] for k in ('release_basis','release_decision','released_profile','clearance','authority_invariants')},
      'material_release':selected,'identities':material_identities(parent['identities'],selected)}
# Pure deterministic context reconstruction, followed by independent production verification before publication.
anchor_full=json.loads(old.resolve('sha256:'+parent['anchor']['full_context']['sha256']))
anchor_op=json.loads(old.resolve('sha256:'+parent['anchor']['operational_binding']['sha256']))
projection=json.loads(old.resolve('sha256:'+parent['anchor']['projection']['sha256']))
basis=json.loads(old.resolve('sha256:'+parent['release_basis']['sha256']));sources=basis.get('current_inputs',basis.get('inputs'))
supplement=json.loads(old.resolve('sha256:'+anchor_op['governance']['implementation_supplement']['sha256']))
for p,h in final.items():supplement['inputs'][p]={'previous_sha256':sources.get(p,{}).get('sha256'),'sha256':h}
newop=historical_operation(anchor_op,anchor_full,projection,spec,supplement)
assert newop['invocation_identity']==op['invocation_identity'] and newop['released_launch']==op['released_launch']
raw['operational_binding']=canonical(newop)
write('OPERATIONAL_BINDING.json',newop);write('AUTHORIZATION_PRIVATE_REPRESENTATION.json',raw)
write('MATERIAL_RELEASE_APPLICATION.json',{'schema':'MATERIAL-RELEASE-APPLICATION-1','predecessor':parent['identities'],'application_predecessor':selected['application_predecessor'],
 'selected':selected,'identities':spec['identities'],'context_identities':newop['context_identities'],
 'succession_event':None,'successor_instance_id':None,'state':'INACTIVE','ownership':'NONE'})
for p in OUT.rglob('*'):
 if p.is_file() and p.suffix!='.py':import_ref(evidence(p))
records[authid]={'bytes':encoded(raw),'evidence':[]}
records[spec['identities']['OperationalContextId']]={'bytes':encoded(newop),'evidence':[]}
records[authid+':supervisor-authority-amendment']={'bytes':encoded(selected),'evidence':[]}
app={'authorization_id':authid,**spec['identities']}
root=old.root.parent/'material-supervisor-amendment-qualified-final'
store=ControllerAuthorityStore.materialize(root,records,{}, {'authority_source':source,'release_identities':spec['identities']},app,old.catalog['programmer_roots'],old.catalog['private_state'])
write('PREPARED_STORE.json',{'root':str(store.root),'catalog_sha256':store.catalog_sha256,'applicability':app})
write('IMPLEMENTATION_DELTA.json',{'accepted_base':inventory['identity'],'consumption_implementation':q['implementation_identity'],
 'delta':[{'path':p,'frozen_sha256':inventory['inventory']['controller'].get(p),'current_sha256':h} for p,h in final.items() if h!=inventory['inventory']['controller'].get(p)]})
print(canonical({'prepared':str(root),'catalog_sha256':store.catalog_sha256,'identities':spec['identities']}),flush=True)
store.close();old.close()
