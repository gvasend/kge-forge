"""Exact authorized ordinary adoption. No invocation creation."""
import json,sys,os,time
from pathlib import Path
O=Path(__file__).resolve().parent;E=O.parent;P=E/'r3_enrollment_evidence_correction_2026-09-19';Q=E/'runtime_r3_self_hosting_qualified_2026-09-19'
load=lambda p:json.loads(p.read_bytes())
q=load(Q/'RUNTIME_QUALIFICATION_FINAL.json');ep=load(P/'AUTHORIZED_ENROLLMENT_SELECTION.json');proposal=load(P/'PROPOSED_ADOPTION.json');material=load(P/'PROPOSED_PRODUCTION_INTEGRATION.json');row=load(P/'ENROLLMENT_RESULT.json')
sys.path.insert(0,q['R3']['root'])
from adapter import ordinary_runtime as a,runtime_adoption as r,continuation_enrollment as en
from adapter.controller_authority_store import ControllerAuthorityStore,encoded,sha
assert sha((P/'PROPOSED_ADOPTION.json').read_bytes())=='925d195c9933b38047e4c7c03dd1fd637a140ae3484d8ef6dbd621e0b6c5567c'
assert sha(encoded(row))=='735ceb55bd763e505fd7d967b816e46272247ccd1d7d64028a4f4a6bf5613028'
r.unseal('PROPOSED-R3-ADOPTION',proposal);r.unseal('PROPOSED-R3-PRODUCTION-INTEGRATION',material)
assert proposal['material_integration_proposal']==material['id']
for directory in (P,Q):
 for line in (directory/'SHA256SUMS').read_text().splitlines():
  h,n=line.split('  ',1);assert sha((directory/n).read_bytes())==h,n
old=ControllerAuthorityStore(**ep['selected_store']);d=en.delegation(old)
# Exact immutable historical verifier; a.anchor freshly authenticates its bytes
# and entire consumed-bootstrap dependency closure before using it.
p=material['integration'];anchor=a.anchor(old,p)
assert anchor['current_runtime']==proposal['decision_fields']['predecessor'] and anchor['head_event']==row['head_event'] and anchor['pending'] is None
assert d['context']==anchor['runtime_authority_context']==proposal['release_context']
assert en.validate(old,d,ep['candidate'],ep['qualification'],ep['decision'])[2]['identity']==q['R3']['identity']
with en.lock(old,d,False) as fd:assert en.history(old,d,fd)==[row]
assert old.state_path(d['journal']).stat().st_mode&0o777==0o600
# Frozen historical package, loaded independently by anchor; fresh S3 from it.
legacy=next(v for k,v in sys.modules.items() if k.startswith('_forge_frozen_runtime_') and k.endswith('.runtime_adoption'))
boot=sys.modules[legacy.__package__+'.runtime_bootstrap'];Store=sys.modules[legacy.__package__+'.controller_authority_store'].ControllerAuthorityStore
base=Store(**ep['base_store']);_,record,_=boot.verify_records(base);boot.fresh_supervisor(base,record)
for path,h in ep['baseline'].items():assert sha(Path(path).read_bytes())==h
root=Path('/tmp/kge-forge-prospective-enrollment/r3-adoption-3fdc36c8e4934c619eb48e13488c1e9bd26d3eaf45bca524ed55747258ad84fd');assert not root.exists();root.mkdir(mode=0o700)
def write(path,obj):
 data=obj if isinstance(obj,bytes) else encoded(obj);fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
 try:
  with os.fdopen(fd,'wb') as f:f.write(data);f.flush();os.fsync(f.fileno())
 finally:pass
 fd=os.open(Path(path).parent,os.O_RDONLY|os.O_DIRECTORY);os.fsync(fd);os.close(fd)
records={key:{'bytes':old.resolve(key),'evidence':[]} for key in old.catalog['objects']};aliases={}
def add(obj):
 data=obj if isinstance(obj,bytes) else encoded(obj);h=sha(data);records['sha256:'+h]={'bytes':data,'evidence':[]};return {'authority_id':'sha256:'+h,'sha256':h}
source=add((O/'ARCHITECT_ADOPTION_SOURCE.md').read_bytes())
authority=r.seal('ARCHITECT-R3-ADOPTION-AUTHORITY',{'schema':'ATTRIBUTABLE-EXACT-ADOPTION-AUTHORITY-1','authority':'Architect','source':source,'proposal':proposal['id'],'proposal_sha256':sha(encoded(proposal)),'enrollment':row['id'],'enrollment_sha256':sha(encoded(row)),'predecessor':ep['R1'],'successor':q['R3']['identity'],'material_integration_proposal':material['id'],'scope':'EXACT_R1_TO_R3_ONLY_NO_INVOCATION'})
authority_ref=add(authority)
filled=dict(proposal,architect_adoption_authority=authority_ref)
# The executable decision uses the exact qualified shape, with only the reserved
# actor filled by this decision. Its attributable source is catalog provenance.
body=dict(proposal['decision_fields'],authority='Architect');grant=r.seal('ENROLLED-RUNTIME-ADOPTION-DECISION',body);gr=add(grant);aliases['runtime-adoption-decision:'+gr['sha256']]=gr['authority_id']
mr=add(material['required_decision_payload']);assert mr==p['authority'];aliases['integration-decision:'+mr['sha256']]=mr['authority_id'];aliases[a.SELECTOR]=add(p)['authority_id']
write(root/'ordinary-runtime.jsonl',b'');private=dict(old.catalog['private_state']);private[p['journal']]={'path':str(root/'ordinary-runtime.jsonl'),'mutation':'APPEND_ONLY','mechanism':'ENROLLED-RUNTIME-EVENT-1'}
s=ControllerAuthorityStore.materialize(root/'store',records,aliases,{'authority_source':authority_ref,'release_identities':d['context']},dict(old.applicability,ordinary_integration=p['id']),old.catalog['programmer_roots'],private)
selected={'root':str(s.root),'catalog_sha256':s.catalog_sha256,'applicability':s.applicability}
selection={'schema':'ARCHITECT-AUTHORIZED-R3-ADOPTION-SELECTION-1','selected_store':selected,'runtime_root':q['R3']['root'],'authority':authority,'grant':gr,'candidate':ep['candidate'],'enrollment':row['id'],'predecessor':ep['R1'],'successor':q['R3']['identity'],'enrollment_selection':ep,'integration':p,'base_store':ep['base_store'],'baseline':ep['baseline']}
write(root/'AUTHORIZED_SELECTION.json',selection);write(O/'AUTHORIZED_SELECTION.json',selection)
assert a.reconstruct(s)['runtime']==ep['R1'];a.transition(s,d,ep['candidate'],row['id'],gr)
boot.fresh_supervisor(base,record)
start=time.monotonic();state=a.adopt(s,None,ep['candidate'],row['id'],gr);duration=time.monotonic()-start
assert state['runtime']==q['R3']['identity'] and state['pending'] is None
binding=a.binding(s);verified=a.validate_executing_runtime(s,binding)
release,ids=a.production_identities(s,p['legacy_release_context']['release_authority'],{k:v for k,v in p['legacy_release_context'].items() if k!='release_authority'},binding)
for path,h in ep['baseline'].items():assert sha(Path(path).read_bytes())==h
out={'state':state,'binding':binding,'self_hosting':verified,'release_authority':release,'context':ids,'adoption_seconds':duration,'authority':authority['id'],'grant':grant,'filled_proposal':filled,'real_model_requests':0,'E1_effects':0}
write(root/'ADOPTION_RESULT.json',out);write(O/'ADOPTION_RESULT.json',out);write(O/'ARCHITECT_ADOPTION_AUTHORITY.json',authority);write(O/'APPLIED_ADOPTION_DECISION.json',grant)
s.close();old.close();base.close();print(json.dumps({'runtime':state['runtime'],'head':state['head'],'authority':authority['id'],'seconds':duration,'release':release,'context':ids}))
