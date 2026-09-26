"""Build documentary qualification/proposal only; no runtime store or ledger writes."""
import json
from pathlib import Path
from adapter.context_projection import canonical,digest,sha
from adapter.supervisor_succession import instance,equivalent,sealed,check_id,validate_instance,reconstruct
P=Path(__file__).resolve().parent
B=P.parents[1]
V=Path('/tmp/kge-forge-s2-verification')
def read(p):return json.loads(p.read_bytes())
def put(name,obj):
 data=canonical(obj).encode();p=P/name
 with p.open('xb') as f:f.write(data)
 return 'sha256:'+sha(data)
receipt_hashes={'CANDIDATE_S2.json':'9dbf2910561c90ba325cc2769ad8181aad71ffcf5b1b31b734bfe0ae395e5c64','HOST_LAUNCH.json':'600bb02c166f364ddd5ac5c71cad841bef7e0a1fbad18e5af4dbc069eef8d33d','PLACEMENT_BEFORE_DROP.json':'70c5f69966b6b20fa3a583572383e76f97f6029177faaee8559b1fecee4e3791','PRELAUNCH.json':'030987fc8d099f1a1ceac3d57ed72673988f0306dba6b01862bb92dcf0bc409c','STALE_SOCKET_REMOVAL.json':'55014aeb3b64f785c02364bf1584fef05ba80700ebdf63a32babd086eee6ac0e'}
package={'host_launch.py':'bf98d94070c5fdcc7861fc6383529f31e8de228571f184342c4cbd414b9be7d6','LAUNCH_SPEC.json':'b71bb732ae2206c00911fe50abe4806618ca5709185743c7f9af3a6e2ddc7a43','HOST_LAUNCH_AUTHORIZATION.json':'fadb9bfd204efb8fc0f16152dbaed9ff9ac73d6b8064f7224b17ae596fa0caef'}
source={'operator':'Jerry','channel':'user','role':'Attributable read-only host hash evidence','root_receipt_directory':'/var/lib/kge-forge-supervisor-succession/S2','original_receipt_sha256':receipt_hashes,'verification_copy_directory':str(V),'installed_package_directory':'/var/lib/kge-forge-supervisor-succession','installed_package_sha256':package,'attribution_quote':'Treat this as attributable read-only host evidence from the authorized host operator.','scope':'Hash evidence only; no specific succession decision.'}
source_ref=put('HOST_HASH_ATTESTATION.json',source)
for k,h in receipt_hashes.items():assert sha((V/k).read_bytes())==h
frozen={'host_launch.py':B/'supervisor_succession_2026-09-17/host_launch.py','LAUNCH_SPEC.json':B/'supervisor_succession_attempt_2026-09-17/LAUNCH_SPEC.json','HOST_LAUNCH_AUTHORIZATION.json':B/'supervisor_s2_host_attempt_2026-09-17/HOST_LAUNCH_AUTHORIZATION.json'}
for k,h in package.items():assert sha(frozen[k].read_bytes())==h
c=instance(read(V/'CANDIDATE_S2.json'));host=read(V/'HOST_LAUNCH.json');pre=read(V/'PRELAUNCH.json')
a=read(P/'ANCESTRY_RECHECK.json');live=read(P/'LIVE_RECHECK.json');checks=read(P/'RECEIPT_CONTENT_CHECKS.json')
assert a['result']=='PASS' and a['state']=='INACTIVE' and a['ownership']=='NONE'
assert live['result']=='PASS' and live['fresh_instance']==c and live['supervisor_pids']==[1098552] and live['S1_absent']
assert checks['all_content_checks_pass']
assert c['runtime_binding']['OperationalContextId']==a['identities']['OperationalContextId']
assert c['runtime_binding']['continuation_chain_digest']==a['identities']['continuation_chain_digest']
historical=read(B/'supervisor_succession_2026-09-17/HISTORICAL_S1.json');check_id(historical,'SupervisorHistoricalInstance')
assert historical['id']=='SupervisorHistoricalInstance-sha256:8ffe7a419d3953ed54fb1a73a9bd1d793cbe2c540c181cee9c0ca4e30987d572'
att=read(B/'supervisor_succession_attempt_2026-09-17/ARCHITECT_ATTEMPT_AUTHORIZATION.json')
grant=read(B/'supervisor_s2_host_attempt_2026-09-17/HOST_OPERATOR_AUTHORIZATION.json')
evidence={'root_receipts':{k:{'original_path':'/var/lib/kge-forge-supervisor-succession/S2/'+k,'sha256':h} for k,h in receipt_hashes.items()},'host_hash_attestation':source_ref,'installed_frozen_package_sha256':package,'PD06_amendment':att['material_amendment'],'release_authority':att['release_authority'],'dispatch_amendment':att['dispatch_amendment'],'architect_attempt_authorization':att['authorization_id'],'architect_attempt_file_sha256':sha((B/'supervisor_succession_attempt_2026-09-17/ARCHITECT_ATTEMPT_AUTHORIZATION.json').read_bytes()),'host_authorization':grant['authorization_id'],'host_authorization_file_sha256':sha((B/'supervisor_s2_host_attempt_2026-09-17/HOST_OPERATOR_AUTHORIZATION.json').read_bytes()),'stale_socket_disposition':{'result':'CONDITIONALLY_REMOVED_BEFORE_CANDIDATE_LAUNCH','prelaunch_listener_absent':True,'scope_count':92,'receipt_sha256':receipt_hashes['STALE_SOCKET_REMOVAL.json'],'note':'Filesystem inode reuse is not process/listener identity; current listener is separately bound to process birth and kernel socket inode.'},'fresh_identity_exclusivity_evidence_sha256':sha((P/'LIVE_RECHECK.json').read_bytes()),'authority_reconstruction_sha256':sha((P/'ANCESTRY_RECHECK.json').read_bytes()),'receipt_content_checks_sha256':sha((P/'RECEIPT_CONTENT_CHECKS.json').read_bytes()),'prior_non_E1_status_evidence_sha256':sha((P.parent/'RUNTIME_OBSERVATIONS.json').read_bytes()),'operational_ancestry':a['ancestry'],'runtime_binding':c['runtime_binding']}
evidence_ref=put('COMPLETE_EVIDENCE_BINDING.json',evidence)
q={'schema':'SUPERVISOR-QUALIFICATION-1','instance_id':c['id'],'runtime_binding':c['runtime_binding'],'result':'PASS','configuration':equivalent(c),'capture_sha256':evidence_ref.split(':',1)[1],'evidence_binding':evidence_ref,'verdict':'S2_CANDIDATE_QUALIFIED'}
qref=put('QUALIFICATION.json',q)
pred={'schema':'SUPERVISOR-PREDECESSOR-EVIDENCE-1','instance_id':historical['id'],'runtime_binding':c['runtime_binding'],'status':'UNAVAILABLE','authority':'HOST_OPERATOR','observation_id':'sha256:'+receipt_hashes['PRELAUNCH.json'],'observed_at':pre['observed_at'],'process_absent':True,'listener_absent':True,'outstanding_scopes_accounted':True,'source_original_receipt_sha256':receipt_hashes['PRELAUNCH.json'],'host_hash_attestation':source_ref,'fresh_absence_evidence_sha256':sha((P/'LIVE_RECHECK.json').read_bytes())}
pref=put('PREDECESSOR_EVIDENCE.json',pred)
body={'schema':'SUPERVISOR-SUCCESSION-1','sequence':1,'predecessor_event':None,'predecessor_instance':historical['id'],'predecessor_status':'UNAVAILABLE','predecessor_evidence':pref,'successor_instance':c['id'],'reason':'Historical released S1 is unavailable. Select the genuinely observed and qualified S2 through the amended PD-06 supervisor authority, subject to the specific Architect succession decision.','host_launch':c['host_launch'],'qualification':qref,'runtime_binding':c['runtime_binding']}
body_digest=digest(body)
# Reserve an auth-scoped logical reference, not an authorization object or grant.
reserved=c['runtime_binding']['authorization_id']+':supervisor-succession-authorization:'+body_digest
event=sealed('SupervisorSuccession',{**body,'architect_authorization':reserved})
eref=put('PROPOSED_SUPERVISOR_SUCCESSION.json',event)
request={'status':'PROPOSED_AWAITING_SPECIFIC_ARCHITECT_DECISION','event_identity':event['id'],'event_file_sha256':eref.split(':',1)[1],'event_body_sha256':body_digest,'reserved_authorization_reference':reserved,'authorization_object_exists':False,'required_specific_decision':'AUTHORIZE_SUPERVISOR_SUCCESSION','predecessor_instance':historical['id'],'successor_instance':c['id'],'reason':body['reason'],'host_authorization':grant['authorization_id'],'launch_spec_sha256':package['LAUNCH_SPEC.json'],'launcher_sha256':package['host_launch.py'],'note':'This is a decision request, not an Architect authorization. No approval object, private catalog selection or succession ledger is created. The event hash is exact for this proposal; issuing a different authorization reference requires a new event fingerprint.'}
put('ARCHITECT_DECISION_REQUEST.json',request)
# In-memory verification adapter only; never a production authority resolver.
objects={c['id']:c,c['host_launch']:host,historical['id']:historical,pref:pred,qref:q}
class VerificationOnly:
 applicability={k:c['runtime_binding'][k] for k in ('authorization_id','ReleaseBasisId','ReleaseDecisionId','OperationalContextId','continuation_chain_digest')}
 def resolve(self,key):
  if key not in objects:raise ValueError('unissued specific authorization: '+key)
  return canonical(objects[key]).encode()
s=VerificationOnly();policy={'schema':'SUPERVISOR-SUCCESSION-POLICY-1','runtime_binding':c['runtime_binding'],'anchor_id':historical['id'],'requirements':equivalent(c),'authorized_succession_ids':[],'pinned_head':None}
assert validate_instance(s,c['id'],policy)==c
try:reconstruct(s,policy,canonical(event).encode()+b'\n')
except ValueError as e: rejection=str(e)
else:raise AssertionError('proposal incorrectly accepted without specific authority')
assert 'not independently authorized' in rejection
put('PROPOSAL_VALIDATION.json',{'candidate_instance_validation':'PASS','event_identity_check':check_id(event,'SupervisorSuccession'),'without_specific_architect_decision':'REJECTED_AS_REQUIRED','rejection':rejection,'scope':'Read-only in-memory schema/instance validation; no policy or authority issued.'})
put('RESULT.json',{'verdict':'S2_CANDIDATE_QUALIFIED','instance_id':c['id'],'original_copy_hash_comparison':'PASS_FROM_JERRY_ATTRIBUTABLE_HOST_EVIDENCE','installed_frozen_package_comparison':'PASS_FROM_JERRY_ATTRIBUTABLE_HOST_EVIDENCE','live_identity_exclusivity':'PASS','ancestry':'PASS','event_identity':event['id'],'event_file_sha256':eref.split(':',1)[1],'event_body_sha256':body_digest,'succession_applied':False,'specific_succession_authorization':'NOT_ISSUED','E1_state':'INACTIVE','ownership':'NONE','E1_activation_events':0,'E1_model_requests':0,'E1_implementation_effects':0,'E1_WP_001':'INELIGIBLE_AND_UNDISPATCHED','copies_role':'Verification representations only; no runtime authority selection.'})
print(canonical(read(P/'RESULT.json')))
