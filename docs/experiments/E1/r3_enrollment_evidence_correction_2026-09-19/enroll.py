"""Exact Architect-authorized enrollment intake; no adoption capability selected."""
import json,sys,os,importlib.util,time
from pathlib import Path
from types import SimpleNamespace
O=Path(__file__).resolve().parent;Q=O.parent/'runtime_r3_self_hosting_qualified_2026-09-19'
def write(path,data):
 if not isinstance(data,bytes):data=encoded(data)
 with Path(path).open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
 fd=os.open(str(Path(path).parent),os.O_RDONLY|os.O_DIRECTORY);os.fsync(fd);os.close(fd)
q=json.loads((Q/'RUNTIME_QUALIFICATION_FINAL.json').read_bytes());pin=json.loads((O.parent/'runtime_bootstrap_application_2026-09-19/AUTHORIZED_SELECTION.json').read_bytes())
# Execute only the already-qualified enrollment component and frozen legacy
# verifier. Do not select R3 or use its prospective ordinary consumer.
sys.path.insert(0,q['integration']['anchor_verifier']['root'])
from adapter import runtime_adoption as r,runtime_bootstrap as b
from adapter.controller_authority_store import ControllerAuthorityStore,encoded,sha,roots_for,outside
mechanism=Q/'candidate/adapter/continuation_enrollment.py'
assert sha(mechanism.read_bytes())=='7adf73eb300d7dd2fc1fae8fc36595de2c8b0b35cc534f8c795448414422c549'
root=Path('/tmp/kge-forge-prospective-enrollment')/'r1-r3-e57b9e8f1fb07c594e1bf666876575abf43863d608fe864d77dbda619db0bba6'
oldroot=root
assert oldroot.exists() and (oldroot/'enrollment.jsonl').read_bytes()==b''
assert not (oldroot/'ENROLLMENT_INTENT.json').exists()
root=oldroot/'evidence-correction-1'
from structured_evidence import validate as validate_representation
for label in ('qualification_report','architect_instruction'):
 validate_representation(label,(O/(label+'.json')).read_bytes())
assert not root.exists(),'existing enrollment namespace; reconstruct, never retry implicitly'
# Verify the frozen evidence manifest before provisioning any authority records.
for line in (Q/'SHA256SUMS').read_text().splitlines():
 h,name=line.split('  ',1);assert sha((Q/name).read_bytes())==h, name
candidate_bytes=(Q/'PROPOSED_R1_R3_CONTINUATION.json').read_bytes()
assert sha(candidate_bytes)=='94bb69262b6af4020fbd829d582f439c60bcfbc42c4df2fba2e266d444554172'
c=json.loads(candidate_bytes);r.unseal('FUTURE-CONTINUATION-CANDIDATE',c)
assert c['id']=='FUTURE-CONTINUATION-CANDIDATE-sha256:e57b9e8f1fb07c594e1bf666876575abf43863d608fe864d77dbda619db0bba6'
base=ControllerAuthorityStore(**pin['selected_store']);p=r.policy(base);state=r.reconstruct(base);boot=b.reconstruct(base)
assert boot['state']=='SUCCESSOR_CURRENT' and boot['runtime_head_established']
assert state['current_runtime']==q['R1']['identity'] and state['pending'] is None
R1=r.descriptor(base,state['current_descriptor'],live=True)
legacy=dict(p['release_context']);release=legacy.pop('release_authority')
current_release,context=r.production_identities(base,release,legacy,{'runtime_head_authority':p['id'],'runtime':state['current_runtime'],'head_event':state['head_event']})
assert c['context']==dict(context,release_authority=current_release) and c['lineage']==p['id']
for descriptor in (q['R1'],q['R3']):
 assert descriptor['identity']=='sha256:'+sha(encoded(descriptor['files']))
 for n,h in descriptor['files'].items():assert sha((Path(descriptor['root'])/'adapter'/n).read_bytes())==h
proof=json.loads((Q/'R12_AUTHENTICATED_CAPTURE.json').read_bytes());roots=roots_for(SimpleNamespace(**proof['authorization']))
outside(root,roots);outside(q['R3']['root'],roots)
_,record,_=b.verify_records(base);b.fresh_supervisor(base,record)
baseline={str(base.state_path(p[k])):sha(base.state_path(p[k]).read_bytes()) for k in ('journal','bootstrap_journal')}
baseline[str(base.root/'catalog.json')]=sha((base.root/'catalog.json').read_bytes())
baseline[proof['terminal']['audit']]=proof['terminal']['audit_sha256'];baseline['/tmp/kge-forge-e1-invocations.jsonl']=proof['terminal']['ledger_sha256']
for name,h in baseline.items():assert sha(Path(name).read_bytes())==h
root.mkdir(mode=0o700);write(root/'continuation_enrollment.py',mechanism.read_bytes())
spec=importlib.util.spec_from_file_location('qualified_prospective_enrollment',root/'continuation_enrollment.py');en=importlib.util.module_from_spec(spec);spec.loader.exec_module(en)
records={};aliases={}
def add(value):
 data=value if isinstance(value,bytes) else encoded(value);h=sha(data);records['sha256:'+h]={'bytes':data,'evidence':[]};return {'authority_id':'sha256:'+h,'sha256':h}
source=(O.parent/'r3_enrollment_2026-09-19/ARCHITECT_ENROLLMENT_SOURCE.md').read_bytes();source_ref=add(source)
old_source=(O.parent/'a2_1i_enrollment_qualification_2026-09-19/ARCHITECT_DELEGATION_SOURCE.md').read_bytes();old_source_ref=add(old_source)
cr=add(candidate_bytes);assert cr==q['continuation_ref']
for desc in (q['R1'],q['R3']):
 for n in desc['files']:add((Path(desc['root'])/'adapter'/n).read_bytes())
 add(desc)
closure=add((Q/'QUALIFICATION_CLOSURE.json').read_bytes());report=add((O/'qualification_report.json').read_bytes());publication=add((Q/'PUBLICATION.json').read_bytes())
# Exact accepted qualification evidence, not the earlier synthetic attestation.
qualification=r.seal('CONTINUATION-QUALIFICATION-ATTESTATION',{'schema':'CONTINUATION-QUALIFICATION-ATTESTATION-1','candidate':cr,'result':'PASS','qualification_policy':'EXACT_R3_SELF_HOSTING_ARCHITECT_ACCEPTED_1','binding_kind':'PRODUCTION_ENROLLMENT','evidence':[closure,report,publication,add((O/'architect_instruction.json').read_bytes())]});qr=add(qualification);aliases['qualification-attestation:'+qr['sha256']]=qr['authority_id']
dsource=add({'authority':'Architect','decision':'DELEGATE_FUTURE_ENROLLMENT','lineage':p['id'],'binding_kind':'PRODUCTION_ENROLLMENT','capability':'ENROLL_EXACT_QUALIFIED_CONTINUATION_ONLY'})
d=r.seal('CONTINUATION-ENROLLMENT-DELEGATION',{'schema':'CONTINUATION-ENROLLMENT-DELEGATION-1','lineage':p['id'],'context':c['context'],'binding_kind':'PRODUCTION_ENROLLMENT','capability':'ENROLL_EXACT_QUALIFIED_CONTINUATION_ONLY','authority_source':dsource,'mechanism_sha256':sha(mechanism.read_bytes()),'qualification_policy':qualification['qualification_policy'],'journal':'production:enrollment'})
aliases[en.DELEGATION]=add(d)['authority_id']
g=r.seal('CONTINUATION-ENROLLMENT-DECISION',{'schema':'CONTINUATION-ENROLLMENT-DECISION-1','authority':'Architect','decision':'ENROLL_ONLY','delegation':d['id'],'candidate':cr,'qualification':qr,'binding_kind':'PRODUCTION_ENROLLMENT','head_event':state['head_event']});gr=add(g);aliases['enrollment-decision:'+gr['sha256']]=gr['authority_id']
intake=r.seal('ARCHITECT-ENROLLMENT-INTAKE',{'schema':'ATTRIBUTABLE-AUTHORITY-INTAKE-1','source':source_ref,'prospective_delegation_source':old_source_ref,'decision':gr,'delegation':d['id'],'qualification':qr,'candidate':cr,'successor':q['R3']['identity'],'authority_scope':'ENROLL_ONLY_NO_ADOPTION','accepted_materiality':'MATERIAL_RUNTIME_CONSUMPTION_INTEGRATION'})
write(root/'AUTHORITY_INTAKE.json',intake)
assert (oldroot/'enrollment.jsonl').read_bytes()==b''
s=ControllerAuthorityStore.materialize(root/'store',records,aliases,{'authority_source':add(intake),'release_identities':c['context']},{'enrollment_delegation':d['id']},roots,{'production:enrollment':{'path':str(oldroot/'enrollment.jsonl'),'mutation':'APPEND_ONLY','mechanism':'CONTINUATION-ENROLLMENT-1'}})
selected={'root':str(s.root),'catalog_sha256':s.catalog_sha256,'applicability':s.applicability}
selection={'schema':'ARCHITECT-AUTHORIZED-ENROLLMENT-SELECTION-1','selected_store':selected,'base_store':pin['selected_store'],'consumer_root':q['integration']['anchor_verifier']['root'],'enrollment_module':str(root/'continuation_enrollment.py'),'enrollment_module_sha256':sha(mechanism.read_bytes()),'intake':intake,'candidate':cr,'qualification':qr,'decision':gr,'runtime':q['R3'],'R1':q['R1']['identity'],'base_binding':{'runtime_head_authority':p['id'],'runtime':state['current_runtime'],'head_event':state['head_event']},'baseline':baseline}
write(root/'AUTHORIZED_ENROLLMENT_SELECTION.json',selection);write(O/'AUTHORIZED_ENROLLMENT_SELECTION.json',selection)
# Final fresh gates, then attributable intent before the qualified append.
b.fresh_supervisor(base,record)
for label in ('qualification_report','architect_instruction'):
 validate_representation(label,(O/(label+'.json')).read_bytes())
en.validate(s,en.delegation(s),cr,qr,gr)
with en.current_head(base,d) as head,en.lock(s,d,False) as fd:
 assert en.history(s,d,fd)==[] and head['current_runtime']==q['R1']['identity']
intent=r.seal('CONTINUATION-ENROLLMENT-INTENT',{'schema':'ENROLLMENT-INTENT-1','candidate':cr,'qualification':qr,'decision':gr,'delegation':d['id'],'runtime_head':state['head_event'],'current_runtime':q['R1']['identity'],'selected_catalog_sha256':s.catalog_sha256,'wall_time':time.time(),'authority_scope':'ENROLL_ONLY'})
write(root/'ENROLLMENT_INTENT.json',intent)
row=en.enroll(s,base,cr,qr,gr,binding_kind='PRODUCTION_ENROLLMENT')
assert en.require_eligible(s,base,cr,row['id'],binding_kind='PRODUCTION_ENROLLMENT')==row
assert r.reconstruct(base)==state
for name,h in baseline.items():assert sha(Path(name).read_bytes())==h
write(root/'ENROLLMENT_RESULT.json',row);write(O/'ENROLLMENT_RESULT.json',row);write(O/'ENROLLMENT_INTENT.json',intent)
write(O/'PRODUCTION_DELEGATION.json',d);write(O/'PRODUCTION_QUALIFICATION.json',qualification)
write(O/'PRODUCTION_ENROLLMENT_DECISION.json',g)
s.close();base.close();print(json.dumps({'enrollment':row['id'],'R1':'CURRENT','R3':'ENROLLED_ELIGIBLE_UNADOPTED','store':selected,'real_model_requests':0}))
