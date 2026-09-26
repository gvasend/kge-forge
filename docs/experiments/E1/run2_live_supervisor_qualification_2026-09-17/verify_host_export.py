"""Read-only receipt verification after Jerry supplies export hash attribution."""
import base64,json,sys,time
from pathlib import Path
from adapter.context_projection import canonical,digest,sha
from adapter.supervisor_succession import instance,equivalent,check_id
from adapter.supervisor_observation import observe
O=Path(__file__).resolve().parent;F=O.parent/'run2_nonhost_closure_2026-09-17';A=O.parent/'run2_host_qualification_authorization_2026-09-17';J=O.parent/'run2_host_consent_2026-09-17'
export=Path('/tmp/kge-forge-s3-host-verification/HOST_EXPORT.json')
assert len(sys.argv)==2,'Require Jerry-attributed exact export SHA-256'
raw=export.read_bytes();assert sha(raw)==sys.argv[1],'host export hash mismatch'
w=json.loads(raw);b=w['body'];assert digest(b)==w['body_sha256'] and b['export_euid']==0 and b['originals_modified'] is False
files={}
for row in b['files']:
 if row.get('absent'):continue
 data=base64.b64decode(row['base64'],validate=True);assert sha(data)==row['sha256'];assert row['uid']==0 and row['mode'] in (0o600,0o644)
 files[Path(row['path']).name]=data
expected={'host_launch.py':F/'host_package/host_launch.py','LAUNCH_SPEC.json':F/'host_package/LAUNCH_SPEC.json','HOST_LAUNCH_AUTHORIZATION.json':J/'HOST_LAUNCH_AUTHORIZATION.json','kge-forge-supervisor-run2.service':F/'host_package/kge-forge-supervisor-run2.service'}
for n,p in expected.items():assert files[n]==p.read_bytes(),n+' installed bytes mismatch'
c,h,placement,pre=[json.loads(files[x+'.json']) for x in ('CANDIDATE_S3','HOST_LAUNCH','PLACEMENT_BEFORE_DROP','PRELAUNCH')]
plan=json.loads(files['LAUNCH_SPEC.json']);auth=json.loads(files['HOST_LAUNCH_AUTHORIZATION.json']);a=json.loads((A/'ARCHITECT_ATTEMPT_AUTHORIZATION.json').read_bytes());j=json.loads((J/'JERRY_HOST_AUTHORIZATION.json').read_bytes());checks={}
def ck(k,v):checks[k]=bool(v)
instance(c);ck('instance_identity',check_id(c,'SupervisorInstance')==c['id'])
ck('reported_process',c['process']['pid']==1465900 and c['process']['ppid']==1465890)
ck('receipt_link',c['host_launch']=='sha256:'+digest(h))
ck('host_configuration',h['configuration']==equivalent(c) and h['process']==c['process'])
ck('runtime_binding',c['runtime_binding']==h['runtime_binding']==plan['runtime_binding']==a['runtime_binding']==auth['runtime_binding'])
ck('parent_birth',h['parent_start_identity']=={k:pre['parent'][k] for k in ('pid','boot_id','start_ticks')} and pre['parent']['pid']==c['process']['ppid'] and pre['parent']['start_ticks']==c['process']['parent_start_ticks'] and pre['parent']['uid']==pre['parent']['gid']==0)
ck('predrop',placement['pid']==1465900 and placement['uid_before_drop']==0 and '0::/kge-forge/executor' in placement['cgroup_before_drop'].splitlines() and placement['cgroup_before_drop'].strip()==c['cgroup']['memberships'] and h['delegated_before_credentials_dropped'] is True)
ck('credentials',c['process']['uid']==c['process']['gid']==h['runtime_uid']==h['runtime_gid']==1000 and c['process']['groups']==[])
ck('spec',pre['launch_spec_sha256']==h['launch_spec_sha256']==a['launch_spec_sha256']==auth['launch_spec_sha256']==sha(files['LAUNCH_SPEC.json']))
ck('launcher',h['launcher_sha256']==a['launcher_sha256']==auth['launcher_sha256']==sha(files['host_launch.py']))
ck('authorization',pre['authorization_sha256']==sha(files['HOST_LAUNCH_AUTHORIZATION.json']))
ck('architect',h['architect_launch_authorization_id']==a['id']==auth['authorization_id'])
ck('jerry',h['operator_authorization_id']==j['id']==auth['host_operator_authorization_id'] and j['authority']=='Jerry' and j['channel']=='user' and sha(j['source_text'].encode())==j['source_text_sha256'])
ck('command',h['command_sha256']==digest({'argv':plan['argv'],'environment':plan['environment'],'launcher_sha256':auth['launcher_sha256']}))
ck('implementation',c['implementation']==plan['implementation'] and all(sha(Path(k).read_bytes())==v for k,v in c['implementation'].items()))
ck('protocol',c['protocol_configuration']==plan['protocol_configuration'])
ck('exe',c['executable']=={'path':plan['interpreter'],'sha256':plan['interpreter_sha256'],'argv':' '.join(plan['argv'])})
ck('workspace',c['workspace']['path']==plan['workspace'])
ck('prelaunch',pre['evidence']['process_absent'] is True and pre['evidence']['listener_absent'] is True and all(not x['members'] and x['populated']==0 for x in pre['evidence']['scope_observations'].values()))
ck('prelaunch_audit',pre['evidence']['supervisor_audit_sha256']==plan['prelaunch_supervisor_audit_sha256'])
if 'STALE_SOCKET_REMOVAL.json' in files:
 st=json.loads(files['STALE_SOCKET_REMOVAL.json']);ck('stale_socket',auth['remove_verified_stale_socket'] is True and j['remove_verified_stale_socket'] is True and st['path']==plan['socket'] and st['uid']==1000 and st['mode']==0o600 and pre['evidence']['listener_absent'] is True)
else:ck('stale_socket',False) # Known prelaunch socket existed; require its qualified disposition.
l=h['host_lifetime'];lp=l['properties'];bp=b['parent']
ck('lifetime',l==pre['evidence']['host_lifetime'] and l['terminal_independent'] is True and l['unit_sha256']==sha(files['kge-forge-supervisor-run2.service']) and l['session_id']==1465890 and l['parent']['pid']==1 and lp['MainPID']=='1465890' and lp['User']==lp['Group']=='root' and lp['Restart']=='no' and lp['DropInPaths']=='' and lp['StandardInput']=='null' and lp['StandardOutput']==lp['StandardError']=='journal' and lp['FragmentPath']=='/etc/systemd/system/kge-forge-supervisor-run2.service' and lp['InvocationID']==l['service_invocation_id']==bp['INVOCATION_ID'])
ck('postclosure_parent',bp['ppid']==1 and bp['session_id']==1465890 and bp['tty_nr']==0 and bp['start_ticks']==c['process']['parent_start_ticks'] and bp['status']['Uid']==['0']*4 and bp['status']['Gid']==['0']*4)
ck('not_exited',b['process_exit_receipt_exists'] is False)
ck('temporal',pre['observed_at']<h['observed_at_unix_ns']<b['observed_at_unix_ns'])
begin=time.monotonic();fresh=observe(c);elapsed=time.monotonic()-begin;ck('fresh_complete_instance',fresh==c)
r={'checks':checks,'all_checks_pass':all(checks.values()),'instance_id':c['id'],'fresh_instance':fresh,'fresh_observation_seconds':elapsed,'host_export_sha256':sha(raw),'original_receipt_hashes':{x['path']:x.get('sha256') for x in b['files']},'copies_are_authority':False}
(O/'RECEIPT_VERIFICATION.json').write_text(json.dumps(r,sort_keys=True,indent=2)+'\n');print(json.dumps(r,sort_keys=True));assert all(checks.values()),checks
