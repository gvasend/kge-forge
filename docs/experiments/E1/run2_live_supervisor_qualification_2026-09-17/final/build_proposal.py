"""Documentary candidate and exact pending proposal. Never append/select authority."""
import base64,json,time,os
from pathlib import Path
from adapter.context_projection import canonical,digest,sha
from adapter.controller_authority_store import ControllerAuthorityStore
from adapter.authority_bootstrap import reconstruct_authorization
from adapter.run2_context import supervisor_prefix
from adapter.supervisor_succession import instance,equivalent,sealed,check_id,validate_instance,reconstruct,legacy_tuple
from adapter.supervisor_observation import observe
from adapter.activation_transaction import _host
O=Path(__file__).resolve().parent;P=O.parent;E=P.parent;F=E/'run2_nonhost_closure_2026-09-17';A=E/'run2_host_qualification_authorization_2026-09-17';J=E/'run2_host_consent_2026-09-17'
def read(p):return json.loads(p.read_bytes())
def put(n,v):
 b=canonical(v).encode();p=O/n
 with p.open('xb') as f:f.write(b)
 return 'sha256:'+sha(b)
raw=Path('/tmp/kge-forge-s3-host-verification/HOST_EXPORT.json').read_bytes();assert sha(raw)=='1cbf36e93771828484dcb570a66b2f061608e813d65bd4efe0456db619e15361'
w=json.loads(raw);assert digest(w['body'])==w['body_sha256']
files={Path(x['path']).name:base64.b64decode(x['base64']) for x in w['body']['files'] if not x.get('absent')}
c=instance(json.loads(files['CANDIDATE_S3.json']));h=json.loads(files['HOST_LAUNCH.json']);pre=json.loads(files['PRELAUNCH.json'])
assert c['id']=='SupervisorInstance-sha256:83f22718a56ab733257208c6e1dfe9767a95e0d10b82f8583f222f88ee9669a2'
vr=read(P/'RECEIPT_VERIFICATION.json');assert vr['all_checks_pass'] and vr['fresh_instance']==c
live=read(O/'LIVE_RECHECK.json');assert not live['errors'] and live['process']==c['process']
assert live['checks']['supervisor_process_inventory']=={'pids':[1465900],'unreadable_pids':[]}
assert live['checks']['S1_absent'] and live['checks']['S2_absent'] and live['checks']['stable_process_birth'] and live['checks']['stable_socket']
assert live['checks']['live_status']['pass'] and live['checks']['socket']==c['socket']
assert live['checks']['supervisor_audit_before']==live['checks']['supervisor_audit_after']==json.loads(files['LAUNCH_SPEC.json'])['prelaunch_supervisor_audit_sha256']
assert not read(P/'TIMING_SUMMARY.json')['events']
# Reconstruct the private candidate and historical prefix with a fresh handle.
r=read(F/'PROBE_RESULT.json');begin=time.monotonic();s=ControllerAuthorityStore(**r['selected_store'])
with s.session():
 auth=reconstruct_authorization(s,s.applicability['authorization_id']);prefix=supervisor_prefix(s)
 old=reconstruct(s,prefix['policy'],prefix['data'],historical_applicability=prefix['applicability'])
 assert old['instance']['id']==prefix['instance'] and old['head']==prefix['head']
 baseline=equivalent(old['instance']);req=equivalent(c)
 assert all(req[k]==baseline[k] for k in ('uid','gid','groups','executable','workspace','socket'))
 assert all(req['cgroup'][k]==baseline['cgroup'][k] for k in ('path','unified','device','inode'))
 config=json.loads(canonical(baseline['protocol_configuration']));config['environment']['PYTHONPYCACHEPREFIX']='/var/cache/kge-forge-supervisor-run2/S3';assert req['protocol_configuration']==config
 assert c['implementation']==read(F/'FINAL_IMPLEMENTATION.json')['inventory']
 assert c['runtime_binding']==read(F/'host_package/LAUNCH_SPEC.json')['runtime_binding']
 # Complete fresh kernel identity and unchanged original idle-scope checks.
 assert observe(c)==c;kernel=_host(legacy_tuple(c),check_scopes=True);assert observe(c)==c
elapsed=time.monotonic()-begin;assert elapsed<30,elapsed
pin=Path('/tmp/kge-forge-controller-authority/auth-e1-wp-001-r7-94f511dfcdcc43ac837191f8732ced39/supervisor-succession-adoption-2026-09-17/SUCCESSION_PUBLICATION.json')
assert sha(pin.read_bytes())=='95a2454b094f2b6e4af044cbfa8a8efd98a225866e2b19fc286a2d63abdacd4e'
assert sha(Path('/tmp/kge-forge-e1-invocations.jsonl').read_bytes())=='651ced1160af0760f8b46073972a88f9d1ffc2c8ed0394e900bfa05fec586fe7'
att=put('HOST_EXPORT_ATTRIBUTION.json',{'operator':'Jerry','channel':'user','supplied_sha256':sha(raw),'supplied_path':'/tmp/kge-forge-s3-host-verification/HOST_EXPORT.json','role':'Attributable verification export of root-owned originals; no new authority or grant'})
closure=put('TERMINAL_CLOSURE_QUALIFICATION.json',{'schema':'SUPERVISOR-TERMINAL-CLOSURE-1','result':'PASS','authority':'HOST_OPERATOR',
 'instance_id':c['id'],'before':c['process'],'after':vr['fresh_instance']['process'],'operator_terminal_closed':True,
 'independent_observer':'Controller host observations in new tool sessions after Jerry reports closing original SSH session; root exporter from new host session',
 'host_statement_sha256':sha((P/'HOST_TERMINAL_CLOSURE_ATTESTATION.json').read_bytes()),'original_candidate_receipt_sha256':sha(files['CANDIDATE_S3.json']),
 'postclosure_observation_sha256':sha((O/'LIVE_RECHECK.json').read_bytes()),'root_export_attribution':att,
 'before_observation_source':'Genuine original launch receipt; not a manufactured pre-closure probe',
 'SSH_session_identifiers_and_exact_closure_time':'NOT_SUPPLIED; closure attributed to Jerry, same birth independently compared'})
ancestry=put('INDEPENDENT_RECONSTRUCTION.json',{'result':'PASS','mode':'NON_EFFECTING_CANDIDATE_INSPECTION','fresh_private_bootstrap_and_host_checks_seconds':elapsed,
 'candidate_operational_identities':r['operational_identities'],'candidate_context_identities':r['context_identities'],
 'historical_supervisor':prefix['instance'],'historical_succession_head':prefix['head'],'original_production_pin_sha256':sha(pin.read_bytes()),
 'candidate_instance_observation':'PASS','kernel_idle_scope_checks':kernel,'current_supervisor_authority_promoted':False,'Run2_ownership':'NONE'})
a=read(A/'ARCHITECT_ATTEMPT_AUTHORIZATION.json');j=read(J/'JERRY_HOST_AUTHORIZATION.json')
ev=put('COMPLETE_EVIDENCE_BINDING.json',{'schema':'S3-CANDIDATE-EVIDENCE-1','instance_id':c['id'],'host_export_sha256':sha(raw),'host_export_attribution':att,
 'original_root_hashes':vr['original_receipt_hashes'],'receipt_verification_sha256':sha((P/'RECEIPT_VERIFICATION.json').read_bytes()),
 'architect_attempt_authorization':a['id'],'jerry_authorization':j['id'],'authorization_file_sha256':sha(files['HOST_LAUNCH_AUTHORIZATION.json']),
 'frozen_installation_manifest_sha256':a['installation_manifest_sha256'],'frozen_candidate_amendment':r['candidate_identity'],'proposed_release_authority':r['release_authority'],
 'prior_supervisor_amendment':'PD06-SUPERVISOR-AUTHORITY-AMENDMENT-sha256:979201e9e2d4269a483ce904ae4e7f9329ab0378836e7ada59070b3e4636d3b6',
 'historical_dispatch_amendment':'ARCHITECT-DISPATCH-AMENDMENT-sha256:3f29a0c359e626b5fe532af6c9fd06218d33bb9644a4906a2214dbf655d67a31',
 'Run2_dispatch_authority':'NOT_ISSUED; historical dispatch does not inherit',
 'terminal_closure_qualification':closure,'independent_reconstruction':ancestry,'live_exclusivity_ready_sha256':sha((O/'LIVE_RECHECK.json').read_bytes()),
 'production_timing_sha256':sha((P/'PRODUCTION_TIMING_RESULT.json').read_bytes()),'durable_timing_sha256':sha((P/'PRODUCTION_TIMING.jsonl').read_bytes()),
 'stale_socket':'Qualified conditional removal evidenced before launch; inode reuse alone is not identity',
 'stale_socket_receipt_sha256':sha(files['STALE_SOCKET_REMOVAL.json']),'runtime_binding':c['runtime_binding']})
q={'schema':'SUPERVISOR-QUALIFICATION-1','instance_id':c['id'],'runtime_binding':c['runtime_binding'],'result':'PASS','configuration':equivalent(c),'capture_sha256':ev.split(':',1)[1],'evidence_binding':ev,'verdict':'S3_CANDIDATE_QUALIFIED','SUP_E1_003':'PASS'}
qr=put('QUALIFICATION.json',q)
pred={'schema':'SUPERVISOR-PREDECESSOR-EVIDENCE-1','instance_id':prefix['instance'],'runtime_binding':c['runtime_binding'],'status':'UNAVAILABLE','authority':'HOST_OPERATOR',
 'observation_id':'sha256:'+sha(files['PRELAUNCH.json']),'observed_at':pre['observed_at'],'process_absent':True,'listener_absent':True,'outstanding_scopes_accounted':True,
 'fresh_controller_absence_observation_sha256':sha((O/'LIVE_RECHECK.json').read_bytes()),'host_export_attribution':att}
pr=put('PREDECESSOR_EVIDENCE.json',pred)
body={'schema':'SUPERVISOR-SUCCESSION-1','sequence':2,'predecessor_event':prefix['head'],'predecessor_instance':prefix['instance'],'predecessor_status':'UNAVAILABLE',
 'predecessor_evidence':pr,'successor_instance':c['id'],'reason':'SUP-E1-003: historical S2 is unavailable; select the genuinely observed terminal-independent S3 only after specific Architect succession acceptance under the proposed Run-2 material authority.',
 'host_launch':c['host_launch'],'qualification':qr,'runtime_binding':c['runtime_binding']}
bodyhash=digest(body);reserved=auth.authorization_id+':supervisor-succession-authorization:'+bodyhash
event=sealed('SupervisorSuccession',dict(body,architect_authorization=reserved));er=put('PROPOSED_SUPERVISOR_SUCCESSION.json',event)
# Schema and provenance checks through existing consumer; reject absent authority.
objects={c['id']:c,c['host_launch']:h,pr:pred,qr:q}
class VerificationOnly:
 applicability=s.applicability
 def resolve(self,key):return canonical(objects[key]).encode() if key in objects else s.resolve(key)
p={'schema':'SUPERVISOR-SUCCESSION-POLICY-2','runtime_binding':c['runtime_binding'],'historical_prefix':prefix['reference'],'anchor_id':prefix['instance'],
 'requirements':equivalent(c),'authorized_succession_ids':[],'pinned_head':prefix['head']}
with s.session():
 assert validate_instance(VerificationOnly(),c['id'],p)==c
 try:reconstruct(VerificationOnly(),p,canonical(event).encode()+b'\n')
 except ValueError as exc:rejection=str(exc)
 else:raise AssertionError('unissued proposal accepted')
 assert 'not independently authorized' in rejection,rejection
s.close()
put('ARCHITECT_DECISION_REQUEST.json',{'status':'PROPOSED_NOT_APPLIED','event_identity':event['id'],'event_file_sha256':er.split(':',1)[1],
 'authorization_body_sha256':bodyhash,'reserved_authorization_reference':reserved,'specific_succession_authorization_issued':False,
 'prerequisites':['Architect exact Run-2 material release decision','Specific Architect S2-to-observed-S3 succession acceptance','Run-2-specific dispatch decision before activation/dispatch'],
 'without_specific_authority':rejection,'no_runtime_catalog_or_ledger_mutation':True})
result={'verdict':'S3_CANDIDATE_QUALIFIED','SUP_E1_003':'PASS','SupervisorInstanceId':c['id'],'pid':1465900,'ppid':1465890,'start_ticks':c['process']['start_ticks'],
 'root_receipts_and_installed_package':'PASS_FROM_JERRY_ATTRIBUTED_HASH_EXPORT','postclosure_birth_socket_READY_exclusivity':'PASS','independent_candidate_reconstruction':'PASS',
 'production_validation_scope':'Non-effecting prospective context plus live candidate kernel/idle-scope predicates; no current-authority promotion',
 'timing':read(P/'PRODUCTION_TIMING_RESULT.json')['samples'],'fresh_private_bootstrap_and_host_checks_seconds':elapsed,
 'proposed_event_identity':event['id'],'proposed_event_file_sha256':er.split(':',1)[1],'authorization_body_sha256':bodyhash,
 'release_applied':False,'succession_applied':False,'Run2_activation':False,'Run2_ownership':False,'Run2_model_requests':0,'Run2_implementation_effects':0,'Run2_dispatch':False}
put('RESULT.json',result);print(canonical(result))
