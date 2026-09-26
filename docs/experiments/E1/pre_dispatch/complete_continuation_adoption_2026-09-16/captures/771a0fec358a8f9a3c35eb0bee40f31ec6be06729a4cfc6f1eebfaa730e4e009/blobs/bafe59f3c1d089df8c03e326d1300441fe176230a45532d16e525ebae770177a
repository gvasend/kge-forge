from pathlib import Path
import json,os,sys
from adapter.context_projection import canonical,digest,sha,read_exact,derive
from adapter.continuation_envelope import archive,seal,BODY_KEYS,historical_operation
from adapter.governance_continuation import reference,GovernanceContinuation
from adapter.context_binding import CommittedContext
from adapter.governed_host import WorkAuthorization
from adapter.authorization_lifecycle import dispatch_binding,historical_original
R=Path('/home/gvasend/app/kge-forge');B=R/'docs/experiments/E1/pre_dispatch';C=B/'complete_implementation_continuation_2026-09-16';O=B/'complete_continuation_adoption_2026-09-16'
def load(p):return json.loads(Path(p).read_bytes())
def durable(n,v):
 p=O/n;data=canonical(v).encode();tmp=p.with_name(p.name+'.pending')
 fd=os.open(tmp,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
 try:os.write(fd,data);os.fsync(fd)
 finally:os.close(fd)
 os.link(tmp,p);tmp.unlink();fd=os.open(O,os.O_RDONLY|os.O_DIRECTORY)
 try:os.fsync(fd)
 finally:os.close(fd)
 return reference(p)
def reconstruct():
 record=load(O/'ADOPTION_RECORD.json')
 for ref in record['durable_inputs']:read_exact(ref['path'],ref['sha256'])
 spec=load(O/'ADOPTED_SPECIFICATION.json');g=GovernanceContinuation(spec);op=load(O/'OPERATIONAL_BINDING.json');old=g.anchor_op
 launch=load(op['released_launch']['path']);ctx=CommittedContext(B/'CONTEXT_MANIFEST.json',launch['authorization']['context_binding']['capture_commit'],spec)
 result=derive(json.loads(launch['authorization']['context_projection']),ctx)
 assert all(result[k]==v for k,v in op['context_identities'].items())
 assert result['projection']['payload']==g.anchor_projection['payload']
 dispatch_ref=reference(B/'dispatch_authorization_2026-09-16/DISPATCH_RECORD.json');decision=load(dispatch_ref['path']);audit=Path(decision['all_authorized_bindings']['audit'])
 issued=next(json.loads(s)['authorization'] for s in audit.read_text().splitlines() if json.loads(s).get('event')=='authorization_issued')
 raw=dict(issued);raw['context_binding']=ctx;raw['operational_binding']=canonical(op)
 for key in ('read_roots','write_roots','deny_roots','exec_bins','read_deny_roots','write_deny_roots','write_directory_roots'):raw[key]=tuple(raw[key])
 raw['exec_argv_allowlist']=tuple(tuple(x) for x in raw['exec_argv_allowlist'])
 auth=WorkAuthorization(**raw);assert historical_original(auth)==issued
 binding=dispatch_binding(auth,audit,dispatch_ref)
 return auth,audit,dispatch_ref,{'result':'PASS','ancestry':g.ancestry,'context_identities':op['context_identities'],'dispatch_inheritance':binding,'adoption':reference(O/'ADOPTION_RECORD.json')}
if len(sys.argv)>1 and sys.argv[1]=='reconstruct':
 auth,audit,ref,result=reconstruct();print(canonical(result));sys.exit(0)
O.mkdir(exist_ok=False)
review=load(C/'FINAL_CAPTURE.json');inputs=archive(review)
for p,r in inputs.items():read_exact(p,r['sha256'])
ends=load(C/'IMPLEMENTATION_ENDPOINTS.json');current={str(p):sha(p.read_bytes()) for p in (R/'adapter').rglob('*.py') if 'tests' not in p.parts}
assert current==ends['candidate_files'];assert len(ends['complete_delta'])==10
original=load(C/'CANONICAL_COMPLETE_CONTINUATION.json');oldspec=load(C/'PROPOSED_SPECIFICATION.json');anchor=load(oldspec['anchor']['operational_binding']['path'])
assert original['predecessor_OperationalContextId']==anchor['governance']['identities']['OperationalContextId']
assert original['predecessor_chain_digest']==anchor['governance']['identities']['continuation_chain_digest']
assert original['classification']=='NON_MATERIAL_IMPLEMENTATION_CONTINUATION'
authority=durable('ARCHITECT_ADOPTION_AUTHORITY.json',{'authority':'Architect','decision':'ADOPT_CANONICAL_COMPLETE_CONTINUATION','source':'Current user message: ARCHITECT ADOPTION AUTHORIZATION','authorized_proposal':reference(C/'CANONICAL_COMPLETE_CONTINUATION.json'),'accepted':['complete implementation-delta NON_MATERIAL_IMPLEMENTATION_CONTINUATION','integrated regression PASS','versioned operational-binding qualification PASS','bootstrap/prospective production-verifier validation PASS'],'instruction':'Adopt the single canonical complete implementation continuation. Do not substitute the earlier unissued draft approval for this Architect authority. Preserve release, dispatch, existing authorization, historical INACTIVE, profile, task, payload and clearance. Revalidate inherited dispatch; use qualified real activation transaction, independently recover ACTIVE+OWNED, stop before first model request. Any failure must stop fail-closed.','authorization_id':'auth-e1-wp-001-r7-94f511dfcdcc43ac837191f8732ced39','no_intermediate_adoptions':True,'E1_model_requests_authorized':False})
body={k:original[k] for k in BODY_KEYS};body['authority']=authority
body['reason']='Architect adoption of the exact complete ten-file candidate; issued approval replaces only the unissued proposal approval binding. Historical proposal remains immutable evidence; no intermediate implementation adopted.'
approval=durable('ISSUED_APPROVAL.json',{'authority':'Architect','decision':'AUTHORIZE_NON_MATERIAL_CONTINUATION','body_sha256':digest(body),'evidence':body['evidence'],'authority_source':authority,'status':'ISSUED','adoption_authorized':True,'authorized_proposal':reference(C/'CANONICAL_COMPLETE_CONTINUATION.json')})
row=seal(body,approval);rowref=durable('CONTINUATION_0001.json',row)
spec={**oldspec,'records':[rowref],'approvals':[approval],'identities':{**oldspec['identities'],**{k:row[k] for k in ('OperationalContextId','continuation_chain_digest')}}}
spec_ref=durable('ADOPTED_SPECIFICATION.json',spec)
verified=GovernanceContinuation(spec)
assert row['artifacts']==original['artifacts'] and row['authority_invariants']==original['authority_invariants'] and row['evidence']==original['evidence']
full=load(spec['anchor']['full_context']['path']);projection=load(spec['anchor']['projection']['path'])
op=historical_operation(anchor,full,projection,spec,verified.supplement)
launch=load(op['released_launch']['path']);ctx=CommittedContext(B/'CONTEXT_MANIFEST.json',launch['authorization']['context_binding']['capture_commit'],spec)
derived=derive(json.loads(launch['authorization']['context_projection']),ctx)
assert derived['projection']['payload']==projection['payload'] and all(derived[k]==v for k,v in op['context_identities'].items())
op_ref=durable('OPERATIONAL_BINDING.json',op)
validation=durable('ADOPTION_VALIDATION.json',{'result':'PASS','production_verifier':'OPERATIONAL-CONTINUATION-1','complete_delta_count':10,'all_29_production_files_match':True,'proposal':reference(C/'CANONICAL_COMPLETE_CONTINUATION.json'),'review_capture':review,'issued_authority':authority,'unissued_draft_not_used_as_authority':True,'preserved_invariants':row['authority_invariants'],'historical_anchor_unchanged':spec['anchor'],'candidate_identity_changes':'Only current issued approval, authority attribution and reason differ from proposed envelope; artifacts/evidence/classification/predecessor and released authorities identical.'})
# Exclusive creation + fsync is the atomic append/commit point. No historical selector is overwritten.
durable('ADOPTION_RECORD.json',{'event':'operational_continuation_adopted','authority':authority,'canonical_mechanism':'OPERATIONAL-CONTINUATION-1','predecessor':anchor['governance']['identities'],'continuation':rowref,'continuation_id':row['continuation_id'],'identities':{**spec['identities'],**op['context_identities']},'operational_binding':op_ref,'durable_inputs':[authority,approval,rowref,spec_ref,op_ref,validation],'intermediate_implementation_continuations_adopted':0,'activation_performed':False})
print(canonical({'adoption':'APPLIED','record':reference(O/'ADOPTION_RECORD.json'),'identities':{**spec['identities'],**op['context_identities']}}))
