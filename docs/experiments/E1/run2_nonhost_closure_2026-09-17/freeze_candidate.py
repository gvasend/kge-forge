"""Export documentary candidate bytes and host instructions; never install/apply."""
import json,hashlib
from pathlib import Path
from adapter.context_projection import canonical,digest,sha
from adapter.run_control import E1_POLICY
O=Path(__file__).resolve().parent;R=O.parent/'run2_remediation_2026-09-17';D=O.parent/'run2_release_construction_2026-09-17'
def read(p):return json.loads(p.read_bytes())
def write(n,v):
 p=O/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(canonical(v))
 return sha(p.read_bytes())
r=read(O/'PROBE_RESULT.json');assert r['result']=='PASS_EXCEPT_CURRENT_SUPERVISOR'
root=Path(r['selected_store']['root']);catalog=read(root/'catalog.json')
def data(ref):return (root/ref['sha256']).read_bytes()
c=read(O/'CANDIDATE.json');op=read(O/'OPERATIONAL_BINDING.json')
assert c['id']==r['candidate_identity']
q=read(O/'IMPLEMENTATION_QUALIFICATION.json');assert sha((O/'IMPLEMENTATION_QUALIFICATION.json').read_bytes())==c['qualification']['sha256']
assert q['implementation_identity']==r['implementation_identity']
for key,name in [('profile','FINAL_PROFILE.json'),('payload','FINAL_MODEL_PAYLOAD.json'),('policy','FINAL_TRANSMISSION_RETENTION_POLICY.json'),('implementation','FINAL_IMPLEMENTATION.json'),('construction_approval','CONSTRUCTION_APPROVAL.json'),('authorization_template','PROPOSED_AUTHORIZATION_TEMPLATE.json'),('launch','PROPOSED_CONTROLLER_LAUNCH.json')]:
 b=data(c[key]);assert sha(b)==c[key]['sha256'];(O/name).write_bytes(b)
(O/'FINAL_AMENDMENT_CANDIDATE.json').write_bytes(data(op['governance']['candidate']))
profile=read(O/'FINAL_PROFILE.json');template=read(O/'PROPOSED_AUTHORIZATION_TEMPLATE.json')
inv=read(O/'FINAL_IMPLEMENTATION.json')['inventory']
assert all(sha(Path(p).read_bytes())==h for p,h in inv.items())
budgethash=write('FINAL_BUDGET_POLICY.json',E1_POLICY)
clearance=op['governance']['clearance']
identities={**r['operational_identities'],**r['context_identities'],'implementation_identity':r['implementation_identity'],
 'profile_sha256':r['profile_sha256'],'Run2AmendmentId':r['candidate_identity'],'proposed_release_authority':r['release_authority'],
 'amendment_file_sha256':sha((O/'FINAL_AMENDMENT_CANDIDATE.json').read_bytes()),
 'historical_content_clearance':clearance,'transmission_retention_content_identity':c['policy']['authority_id'],
 'budget_policy_identity':'sha256:'+budgethash,'qualification_identity':c['qualification']['authority_id'],
 'candidate_store':r['selected_store'],'status':'FROZEN_PROPOSED_NOT_ISSUED'}
write('FINAL_IDENTITIES.json',identities)
plan=read(D/'host_package/PROPOSED_LAUNCH_SPEC.json')
for k in ('applicability_note','missing_before_executable_plan'):plan.pop(k,None)
plan['status']='QUALIFIED_HOST_LAUNCH_SPEC';plan['implementation']=inv
plan['host_lifetime']=c['supervisor_durability']
plan['host_launcher']={'path':str(O/'host_package/host_launch.py'),'sha256':c['host_package']['launcher']['sha256']}
plan['runtime_binding']={'authorization_id':template['authorization_id'],**r['operational_identities'],
 'released_profile_content_sha256':r['profile_sha256'],'execution_profile_sha256':sha(template['execution_profile'].encode()),
 'authority_store_epoch_sha256':digest({'authorization_id':template['authorization_id'],**r['operational_identities']})}
plan['prelaunch_supervisor_audit_sha256']='0e61d05208459051bda9772783ebded01067caa131e7253371805c42c3d040b7'
planhash=write('host_package/LAUNCH_SPEC.json',plan)
files=[]
for n,dest,mode in [('host_launch.py','/var/lib/kge-forge-supervisor-run2/host_launch.py','0600'),('LAUNCH_SPEC.json','/var/lib/kge-forge-supervisor-run2/LAUNCH_SPEC.json','0600'),('kge-forge-supervisor-run2.service','/etc/systemd/system/kge-forge-supervisor-run2.service','0644')]:
 p=O/'host_package'/n;files.append({'source':str(p),'destination':dest,'sha256':sha(p.read_bytes()),'owner':'root:root','mode':mode})
manifest={'schema':'RUN2-HOST-PACKAGE-1','status':'FROZEN_NOT_INSTALLED_OR_AUTHORIZED','files':files,
 'directories':{'/var/lib/kge-forge-supervisor-run2':'root:root 0700','/var/cache/kge-forge-supervisor-run2/S3':'root:root 0755 empty'},
 'separately_authorized_file':{'destination':'/var/lib/kge-forge-supervisor-run2/HOST_LAUNCH_AUTHORIZATION.json','owner':'root:root','mode':'0600','sha256':'DEFINED_ONLY_AFTER_GENUINE_ARCHITECT_AND_HOST_DECISIONS'},
 'implementation_identity':r['implementation_identity'],'candidate_identity':r['candidate_identity'],'runtime_binding':plan['runtime_binding']}
manifesthash=write('HOST_INSTALLATION_MANIFEST.json',manifest)
request={'status':'REQUEST_ONLY_NO_CONSENT','Architect_fields':{'authority':'Architect','decision':'AUTHORIZE_HOST_SUPERVISOR_LAUNCH',
 'authorization_id':'REQUIRES_NEW_ATTRIBUTABLE_ARCHITECT_DECISION','qualification_acceptance_id':'REQUIRES_ARCHITECT_ACCEPTANCE_OF_THIS_PACKAGE',
 'predecessor_id':plan['predecessor_id'],'runtime_binding':plan['runtime_binding'],'launch_spec_sha256':planhash,'launcher_sha256':files[0]['sha256']},
 'Jerry_host_fields':{'host_operator_authorization_id':'REQUIRES_NEW_JERRY_EXPLICIT_HOST_CONSENT','operator':'Jerry',
 'launch_spec_sha256':planhash,'launcher_sha256':files[0]['sha256'],'installation_manifest_sha256':manifesthash,
 'unit_sha256':files[2]['sha256'],'one_candidate_attempt':True,'remove_verified_stale_socket':'REQUIRES_EXPLICIT_CONDITIONAL_CONSENT'},
 'authorization_boundary':'Root-protected launch authorization file must represent both genuine decisions. Neither this request, the qualification label, old S2 consent nor matching configuration supplies consent.',
 'succession_authorized':False,'automatic_retry':False}
write('HOST_AUTHORIZATION_REQUEST.json',request)
commands=['set -euo pipefail','# Only after the exact new package and authorization-file digest receive separate Architect and Jerry approval.']
commands.append("sha256sum --check <<'FROZEN_SOURCES'")
commands += [x['sha256']+'  '+x['source'] for x in files];commands += ['FROZEN_SOURCES']
commands += ['# Verify the separately issued authorization file and its approved SHA-256 before ANY privileged mutation.',
 '# Abort if the service, launch lock, S3 evidence directory, or package is already installed; reconcile; never retry or overwrite an attempt.',
 'sudo install -d -o root -g root -m 0700 /var/lib/kge-forge-supervisor-run2',
 'sudo install -d -o root -g root -m 0755 /var/cache/kge-forge-supervisor-run2/S3']
commands += ['sudo install -o root -g root -m '+x['mode']+' '+x['source']+' '+x['destination'] for x in files]
commands += ['# Install the separately approved authorization file root:root 0600 at /var/lib/kge-forge-supervisor-run2/HOST_LAUNCH_AUTHORIZATION.json.',
 '# Its source path/hash cannot be fabricated before the new decisions. Verify that approved installed hash separately.',
 "sudo sha256sum --check <<'FROZEN_INSTALLED'"]
commands += [x['sha256']+'  '+x['destination'] for x in files];commands += ['FROZEN_INSTALLED',
 'sudo /bin/systemctl daemon-reload','sudo /bin/systemctl start kge-forge-supervisor-run2.service']
(O/'HOST_INSTALLATION_PROCEDURE.md').write_text('Host procedure for review only. Do not execute before new separate approvals. No enable, restart, fallback, manual launcher invocation, or second attempt. A pre-existing or uncertain state stops the procedure.\n\n```bash\n'+'\n'.join(commands)+'\n```\n\nThe unit invokes `/usr/bin/python3.11 /var/lib/kge-forge-supervisor-run2/host_launch.py /var/lib/kge-forge-supervisor-run2/LAUNCH_SPEC.json /var/lib/kge-forge-supervisor-run2/HOST_LAUNCH_AUTHORIZATION.json` under root system service authority. The launcher checks the independent service lifetime and exclusive state, then places the child in the delegated cgroup before credential drop. Only its qualified conditional rule may remove an explicitly authorized stale socket; a live/indeterminate socket stops launch. No host operations were executed during this qualification.\n')
write('POST_LAUNCH_EVIDENCE_REQUIREMENTS.json',{'status':'GENUINE_HOST_EVIDENCE_PENDING','receipts':['PRELAUNCH.json','PLACEMENT_BEFORE_DROP.json','HOST_LAUNCH.json','CANDIDATE_S3.json','STALE_SOCKET_REMOVAL.json if socket removed'],
 'observations':['PID, PPID, boot_id, process and parent start ticks, PID namespace inode','UID/GID/groups','interpreter path/hash/argv, implementation inventory','workspace device/inode','0:: cgroup path/device/inode, placement before setgroups/setgid/setuid','socket path/device/inode/uid/gid/mode and listener PID ownership','protocol/configuration and runtime_binding','root-owned original receipt hashes and installed package hashes','service MainPID, root launcher, InvocationID, parent/session/tty, FragmentPath/hash, empty DropInPaths, Restart=no, journal IO','same candidate birth identity before and after genuine authenticated terminal closure, from independent host observer','S1/S2 unavailable, no competing supervisor/listener/current authority, current release/dispatch/context ancestry'],
 'required_terminal_record_fields':['schema=SUPERVISOR-TERMINAL-CLOSURE-1','result=PASS','instance_id','before=complete genuine candidate process identity','after=same complete genuine process identity','operator_terminal_closed=true','independent_observer','authority=HOST_OPERATOR'],
 'capture_boundary':'Root-owned receipts are authority; attributed read-only copies may verify bytes. No missing birth observation may be manufactured.',
 'resulting_identity':'SupervisorInstance-sha256:<canonical complete genuine instance body SHA-256>; unset until observed'})
write('SUCCESSION_BINDING_TEMPLATE.json',{'status':'TEMPLATE_NOT_AN_EVENT_OR_AUTHORIZATION','sequence':2,
 'predecessor_event':'SupervisorSuccession-sha256:e547147d27f88c38fe8dbfafdd6e45330621cf2e59ae156af60b885fa6f83db5',
 'predecessor_id':plan['predecessor_id'],'successor_id':None,'historical_S1_anchor':'SupervisorHistoricalInstance-sha256:8ffe7a419d3953ed54fb1a73a9bd1d793cbe2c540c181cee9c0ca4e30987d572',
 'runtime_binding':plan['runtime_binding'],'release_authority':r['release_authority'],'launch_spec_sha256':planhash,
 'host_installation_manifest_sha256':manifesthash,'qualification_acceptance':'PENDING_ARCHITECT','specific_succession_authorization':'PENDING_OBSERVED_SUCCESSOR_ACCEPTANCE',
 'genuine_host_launch_and_terminal_closure_evidence':'PENDING_HOST','Run2_specific_dispatch_decision':'PENDING_ARCHITECT',
 'reason':'SUP-E1-003: S2 unavailable; new independent host lifetime required','do_not_apply':True})
# Inclusive nested spans: report count/min/max; do not sum nested spans as wall duration.
rows=[json.loads(x) for x in (O/'TIMING.jsonl').read_bytes().splitlines()];stack=[];timings={}
for row in rows:
 if row['event']=='span_start':stack.append(row)
 elif row['event']=='span_end':
  begin=stack.pop();name=begin['details']['name'];assert name==row['details']['name']
  timings.setdefault(name,[]).append(row['monotonic']-begin['monotonic'])
assert not stack
warnings=[x for x in rows if x['event'] in ('budget_warning','budget_exhausted','admission_closed')]
assert not warnings,warnings
assert max(max(x) for x in timings.values())<30,timings
write('FINAL_TIMING_SUMMARY.json',{'result':'PASS','cold_definition':r['cold_definition'],'cold_private_bootstrap_seconds':r['cold_private_bootstrap_seconds'],
 'authority_store_resolution_seconds':r['authority_store_resolution_seconds'],'validation_samples':r['samples'],
 'spans_inclusive_not_additive':{k:{'count':len(v),'min_seconds':min(v),'max_seconds':max(v)} for k,v in timings.items()},
 'budget_events':warnings,'model_requests':0,'token_accounting':'USAGE_UNKNOWN','timing_sha256':sha((O/'TIMING.jsonl').read_bytes())})
# Historical evidence preserved, including earlier draft package (no rewriting).
counts={}
for folder in (R,D):
 hist=read(folder/'PACKAGE_MANIFEST.json')
 for name,h in hist.items():assert sha((folder/name).read_bytes())==h,(folder,name)
 counts[folder.name]=len(hist)
for row in read(R/'RUN1_PRESERVATION.json')['historical_receipts']:assert sha(Path(row['path']).read_bytes())==row['sha256']
assert sha(Path('/tmp/kge-forge-e1-invocations.jsonl').read_bytes())=='651ced1160af0760f8b46073972a88f9d1ffc2c8ed0394e900bfa05fec586fe7'
write('FINAL_PRESERVATION.json',{'result':'PASS','historical_manifests':counts,'Run1_receipts':12,'Run1_ownership_ledger_unchanged':True,'Run2_started':False})
print(json.dumps({'identities':identities,'host_manifest_sha256':manifesthash,'launch_spec_sha256':planhash,'timing':timings},sort_keys=True))
