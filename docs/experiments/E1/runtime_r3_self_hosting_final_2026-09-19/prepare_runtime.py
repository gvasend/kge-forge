"""Freeze exact private R3/R4 copies and isolated ordinary authority fixtures."""
import json,sys,shutil,tempfile,importlib.util,signal,faulthandler
faulthandler.enable()
signal.signal(signal.SIGALRM,lambda *_: (_ for _ in ()).throw(TimeoutError("bounded runtime qualification exceeded 120 seconds")))
signal.alarm(120)
from pathlib import Path
O=Path(__file__).resolve().parent;E=O.parent
pin=json.loads((E/'runtime_bootstrap_application_2026-09-19/AUTHORIZED_SELECTION.json').read_bytes())
# Original verifier is loaded at its original immutable path, never substituted.
sp=importlib.util.spec_from_file_location('frozen_original',Path(pin['consumer_root'])/'adapter/__init__.py',submodule_search_locations=[str(Path(pin['consumer_root'])/'adapter')]);pkg=importlib.util.module_from_spec(sp);sys.modules[sp.name]=pkg;sp.loader.exec_module(pkg)
from frozen_original import runtime_adoption as old
from frozen_original.controller_authority_store import ControllerAuthorityStore as OldStore
root=Path(tempfile.mkdtemp(prefix='forge-r3-ordinary-'));root.chmod(0o700)
R3=root/'r3';shutil.copytree(O/'candidate/adapter',R3/'adapter',ignore=shutil.ignore_patterns('__pycache__'))
R4=root/'r4';shutil.copytree(R3,R4);(R4/'adapter/qualification_successor_marker.py').write_text('"""Synthetic future-runtime inventory marker; no operational authority."""\n')
sys.path.insert(0,str(R3))
from adapter import ordinary_runtime as a,runtime_adoption as r,continuation_enrollment as en
from adapter.controller_authority_store import ControllerAuthorityStore,encoded,sha
base=OldStore(**pin['selected_store']);p=old.policy(base);state=old.reconstruct(base)
R1=old.descriptor(base,state['current_descriptor'],live=True)
legacy_context=dict(p['release_context']);legacy_release=legacy_context.pop('release_authority')
current_release,current_context=old.production_identities(base,legacy_release,legacy_context,{'runtime_head_authority':p['id'],'runtime':state['current_runtime'],'head_event':state['head_event']})
current_context=dict(current_context,release_authority=current_release)
assert R1['identity']=='sha256:1b31ac92d38952444076e3997083cf035e0862f1bc0182261826d6690ec31c15'
records={};aliases={}
def add(value):
 data=value if isinstance(value,bytes) else encoded(value);h=sha(data);records['sha256:'+h]={'bytes':data,'evidence':[]};return {'authority_id':'sha256:'+h,'sha256':h}
def inventory(path):
 files={f.name:sha(f.read_bytes()) for f in (path/'adapter').glob('*.py')}
 return {'schema':'RUNTIME-INVENTORY-1','identity':'sha256:'+sha(encoded(files)),'root':str(path),'files':files}
d3=inventory(R3);d4=inventory(R4)
for d in (R1,d3,d4):
 for n,h in d['files'].items():assert add((Path(d['root'])/'adapter'/n).read_bytes())['sha256']==h
ref1=add(R1);ref3=add(d3);ref4=add(d4)
assert ref1==state['current_descriptor']
deps={str(base.root/'catalog.json')}
deps.update(str(base.root/x['sha256']) for x in base.catalog['objects'].values())
deps.update(str(base.state_path(p[k])) for k in ('journal','bootstrap_journal'))
descriptors=[old.descriptor(base,p['genesis'])]
for pair in p['adoptions']:
 c=old.read(base,pair['continuation']);descriptors += [old.descriptor(base,c['predecessor']),old.descriptor(base,c['successor'])]
deps.update(str(Path(d['root'])/'adapter'/n) for d in descriptors for n in d['files'])
anchor={'root':pin['consumer_root'],'files':{f.name:sha(f.read_bytes()) for f in (Path(pin['consumer_root'])/'adapter').glob('*.py')},'store':pin['selected_store'],'dependencies':{x:sha(Path(x).read_bytes()) for x in sorted(deps)}}
source={'authority':'Architect','decision':'DELEGATE_FUTURE_ENROLLMENT','lineage':p['id'],'binding_kind':'QUALIFICATION_BINDING','capability':'ENROLL_EXACT_QUALIFIED_CONTINUATION_ONLY'}
d=r.seal('CONTINUATION-ENROLLMENT-DELEGATION',{'schema':'CONTINUATION-ENROLLMENT-DELEGATION-1','lineage':p['id'],'context':current_context,'binding_kind':'QUALIFICATION_BINDING','capability':source['capability'],'authority_source':add(source),'mechanism_sha256':sha(Path(en.__file__).read_bytes()),'qualification_policy':'SYNTHETIC_RUNTIME_SELF_HOSTING_QUALIFICATION','journal':'qualification:enrollment'})
assert d['mechanism_sha256']=='7adf73eb300d7dd2fc1fae8fc36595de2c8b0b35cc534f8c795448414422c549'
aliases[en.DELEGATION]=add(d)['authority_id']
material=add({'authority':'Architect','decision':'QUALIFY_ORDINARY_ENROLLED_ADOPTION','lineage':p['id'],'delegation':d['id'],'implementation_sha256':sha(Path(a.__file__).read_bytes()),'binding_kind':'QUALIFICATION_BINDING'})
aliases['integration-decision:'+material['sha256']]=material['authority_id']
integration=r.seal('ORDINARY-ADOPTION-INTEGRATION',{'schema':'ORDINARY-ADOPTION-INTEGRATION-1','binding_kind':'QUALIFICATION_BINDING','lineage':p['id'],'delegation':d['id'],'implementation_sha256':sha(Path(a.__file__).read_bytes()),'authority':material,'anchor_runtime':R1['identity'],'anchor_head':state['head_event'],'anchor_verifier':anchor,'legacy_release_context':p['release_context'],'journal':'qualification:runtime'})
aliases[a.SELECTOR]=add(integration)['authority_id']
ledger=root/'ordinary.jsonl';ledger.touch(mode=0o600);ej=root/'enrollment.jsonl';ej.touch(mode=0o600)
private={'qualification:runtime':{'path':str(ledger),'mutation':'APPEND_ONLY','mechanism':'ENROLLED-RUNTIME-EVENT-1'},'qualification:enrollment':{'path':str(ej),'mutation':'APPEND_ONLY','mechanism':'CONTINUATION-ENROLLMENT-1'}}
app={'ordinary_integration':integration['id'],'enrollment_delegation':d['id']}
def candidate(before,after,bref,aref):
 delta=[{'path':n,'old_sha256':before['files'].get(n),'new_sha256':after['files'].get(n)} for n in sorted(set(before['files'])|set(after['files'])) if before['files'].get(n)!=after['files'].get(n)]
 c=r.seal('FUTURE-CONTINUATION-CANDIDATE',{'schema':'FUTURE-CONTINUATION-CANDIDATE-1','predecessor':bref,'successor':aref,'delta':delta,'lineage':p['id'],'context':current_context,'classification':'MATERIAL_RUNTIME_CONSUMPTION_INTEGRATION'});cr=add(c)
 q=r.seal('CONTINUATION-QUALIFICATION-ATTESTATION',{'schema':'CONTINUATION-QUALIFICATION-ATTESTATION-1','candidate':cr,'result':'PASS','qualification_policy':d['qualification_policy'],'binding_kind':'QUALIFICATION_BINDING','evidence':[add({'scope':'SYNTHETIC_CONTRACT_ATTESTATION_NOT_PRODUCTION_ENROLLMENT','candidate':cr,'implementation_inventory':after['files']})]});qr=add(q);aliases['qualification-attestation:'+qr['sha256']]=qr['authority_id']
 return c,cr,q,qr
c3,cr3,q3,qr3=candidate(R1,d3,ref1,ref3)
def enroll_grant(cr,qr,head):
 g=r.seal('CONTINUATION-ENROLLMENT-DECISION',{'schema':'CONTINUATION-ENROLLMENT-DECISION-1','authority':'Architect','decision':'ENROLL_ONLY','delegation':d['id'],'candidate':cr,'qualification':qr,'binding_kind':'QUALIFICATION_BINDING','head_event':head});gr=add(g);aliases['enrollment-decision:'+gr['sha256']]=gr['authority_id'];return gr

def materialize(name):
 s=ControllerAuthorityStore.materialize(root/name,records,aliases,{'authority_source':material,'release_identities':p['release_context']},app,[],private)
 return s,{'root':str(s.root),'catalog_sha256':s.catalog_sha256,'applicability':s.applicability}
gr3=enroll_grant(cr3,qr3,state['head_event'])
s,sp=materialize('enrollment-r3');row=a.enroll(s,cr3,qr3,gr3);assert a.reconstruct(s)['runtime']==R1['identity'];s.close()
ag=r.seal('ENROLLED-RUNTIME-ADOPTION-DECISION',{'schema':'ENROLLED-RUNTIME-ADOPTION-DECISION-1','authority':'Architect','decision':'ADOPT_EXACT_ENROLLED_CONTINUATION','binding_kind':'QUALIFICATION_BINDING','lineage':d['lineage'],'delegation':d['id'],'candidate':cr3,'enrollment':row['id'],'qualification':qr3,'predecessor':R1['identity'],'successor':d3['identity'],'head_event':state['head_event']});ar=add(ag);aliases['runtime-adoption-decision:'+ar['sha256']]=ar['authority_id']
s,sp=materialize('adoption-r3');adopted=a.adopt(s,None,cr3,row['id'],ar);binding=a.binding(s);verified=a.validate_executing_runtime(s,binding);s.close()
# Later continuation is genuinely created *after* R3 adoption, not preselected.
c4,cr4,q4,qr4=candidate(d3,d4,ref3,ref4);gr4=enroll_grant(cr4,qr4,adopted['head'])
s,finalpin=materialize('future-r4');row4=a.enroll(s,cr4,qr4,gr4);assert a.eligible(s,cr4,row4['id'])==row4
assert a.reconstruct(s)['runtime']==d3['identity'];assert a.validate_executing_runtime(s,binding)==verified
try:a.adopt(s,None,cr4,row4['id'],ar);raise AssertionError('R4 adopted with R3 grant')
except ValueError:pass
s.close();base.close()
output={'schema':'R3-SELF-HOSTING-QUALIFICATION-1','qualification_only':True,'selected_lineage':'R1 -> new continuation -> R3','root':str(root),'R1':R1,'R3':d3,'R4':d4,'selected_store':finalpin,'R3_binding':binding,'continuation':c3,'continuation_ref':cr3,'qualification':q3,'enrollment':row,'adoption':ag,'adoption_ref':ar,'synthetic_current':adopted,'executing_verification':verified,'R4_candidate':c4,'R4_ref':cr4,'R4_qualification':q4,'R4_enrollment':row4,'R4_disposition':'ENROLLED_ELIGIBLE_UNADOPTED_NOT_CURRENT','integration':integration,'delegation':d,'real_enrollment':False,'real_adoption':False,'model_requests':0,'E1_effects':0}
with (O/'RUNTIME_QUALIFICATION_FINAL.json').open('xb') as f:f.write(encoded(output))
print(json.dumps({'R3':d3['identity'],'continuation':c3['id'],'self_hosting':'PASS','R4':'ELIGIBLE_UNADOPTED','runtime_root':str(R3)}))
