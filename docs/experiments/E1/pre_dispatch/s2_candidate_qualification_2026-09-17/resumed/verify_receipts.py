import json,hashlib
from pathlib import Path
from adapter.supervisor_succession import instance,equivalent,check_id
from adapter.context_projection import digest
base=Path('/home/gvasend/app/kge-forge/docs/experiments/E1/pre_dispatch')
p=Path('/tmp/kge-forge-s2-verification');out=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
files={x.name:x.read_bytes() for x in p.iterdir() if x.suffix=='.json'}
c,h,placement,pre,stale=[json.loads(files[x+'.json']) for x in ['CANDIDATE_S2','HOST_LAUNCH','PLACEMENT_BEFORE_DROP','PRELAUNCH','STALE_SOCKET_REMOVAL']]
plan=json.loads((base/'supervisor_succession_attempt_2026-09-17/LAUNCH_SPEC.json').read_bytes())
a=json.loads((base/'supervisor_succession_attempt_2026-09-17/ARCHITECT_ATTEMPT_AUTHORIZATION.json').read_bytes())
j=json.loads((base/'supervisor_s2_host_attempt_2026-09-17/HOST_OPERATOR_AUTHORIZATION.json').read_bytes())
authbytes=(base/'supervisor_s2_host_attempt_2026-09-17/HOST_LAUNCH_AUTHORIZATION.json').read_bytes();auth=json.loads(authbytes)
checks={}
def ck(k,v):checks[k]=bool(v)
instance(c)
ck('candidate_id',check_id(c,'SupervisorInstance')=='SupervisorInstance-sha256:1aaa0c96caadb97c3e0678e8c0039f32cb2ac7f7ff3c607cf84998190b8e0a41')
ck('host_receipt_content_link',c['host_launch']=='sha256:'+digest(h))
ck('host_configuration',h['configuration']==equivalent(c))
ck('host_process',h['process']==c['process'])
ck('runtime_bindings',c['runtime_binding']==h['runtime_binding']==plan['runtime_binding']==a['runtime_binding']==j['runtime_binding']==auth['runtime_binding'])
ck('parent_birth',h['parent_start_identity']=={k:pre['parent'][k] for k in ('pid','boot_id','start_ticks')} and pre['parent']['pid']==c['process']['ppid'] and pre['parent']['start_ticks']==c['process']['parent_start_ticks'] and pre['parent']['uid']==pre['parent']['gid']==0)
ck('pre_drop_placement',placement['pid']==c['process']['pid'] and placement['uid_before_drop']==0 and '0::/kge-forge/executor' in placement['cgroup_before_drop'].splitlines() and placement['cgroup_before_drop'].strip()==c['cgroup']['memberships'] and h['delegated_before_credentials_dropped'] is True)
ck('runtime_credentials',c['process']['uid']==c['process']['gid']==h['runtime_uid']==h['runtime_gid']==1000 and c['process']['groups']==[])
ck('spec_hash',pre['launch_spec_sha256']==h['launch_spec_sha256']==a['finalized_launch_spec_sha256']==j['launch_spec_sha256']==sha((base/'supervisor_succession_attempt_2026-09-17/LAUNCH_SPEC.json').read_bytes())=='b71bb732ae2206c00911fe50abe4806618ca5709185743c7f9af3a6e2ddc7a43')
ck('launcher_hash',h['launcher_sha256']==a['launcher_sha256']==j['launcher_sha256']==sha(Path(plan['host_launcher']['path']).read_bytes()))
ck('authorization_bytes',pre['authorization_sha256']==sha(authbytes)=='fadb9bfd204efb8fc0f16152dbaed9ff9ac73d6b8064f7224b17ae596fa0caef')
ck('architect_link',h['architect_launch_authorization_id']==a['authorization_id']==auth['authorization_id'])
ck('jerry_link',h['operator_authorization_id']==j['authorization_id']==auth['host_operator_authorization_id'] and j['authority_source']=='sha256:'+sha((base/'supervisor_s2_host_attempt_2026-09-17/HOST_AUTHORIZATION_SOURCE.json').read_bytes()))
ck('command_hash',h['command_sha256']==digest({'argv':plan['argv'],'environment':plan['environment'],'launcher_sha256':auth['launcher_sha256']}))
ck('implementation',c['implementation']==plan['implementation'] and all(sha(Path(k).read_bytes())==v for k,v in c['implementation'].items()))
ck('protocol',c['protocol_configuration']==plan['protocol_configuration'])
ck('executable',c['executable']=={'path':plan['interpreter'],'sha256':plan['interpreter_sha256'],'argv':' '.join(plan['argv'])})
ck('workspace',c['workspace']['path']==plan['workspace'])
ck('prelaunch_eligibility',pre['evidence']['process_absent'] is True and pre['evidence']['listener_absent'] is True and all(not v['members'] and v['populated']==0 for v in pre['evidence']['scope_observations'].values()))
ck('audit_binding',pre['evidence']['supervisor_audit_sha256']==plan['prelaunch_supervisor_audit_sha256'])
ck('conditional_stale_removal',auth['remove_verified_stale_socket'] is True and j['remove_verified_stale_socket'] is True and stale['path']==plan['socket'] and stale['uid']==1000 and stale['mode']==0o600 and pre['evidence']['listener_absent'] is True)
ck('temporal_order',pre['observed_at']<h['observed_at_unix_ns'] and h['clock_ticks_per_second']==100 and h['boot_time_seconds']+c['process']['start_ticks']/h['clock_ticks_per_second']<=h['observed_at_unix_ns']/1e9)
r={'checks':checks,'all_content_checks_pass':all(checks.values()),'recomputed_instance_id':c['id'],'verification_copy_hashes':{k:sha(v) for k,v in files.items()},'root_original_copy_hash_comparison':'PENDING_HOST_CAPTURE','installed_package_hash_comparison':'PENDING_HOST_CAPTURE','scope_count':len(pre['evidence']['scope_observations']),'copy_status':'Verification representations only; no operational authority materialized.'}
(out/'RECEIPT_CONTENT_CHECKS.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
