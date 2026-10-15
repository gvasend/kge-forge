"""Bounded read-only outer policy inspection. No socket/namespace/adapter calls."""
import datetime,hashlib,json,os,pathlib,re,stat,sys
D=pathlib.Path(__file__).resolve().parent;R=D.parents[4];E=D.parent
load=lambda p:json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,x):
 with (D/n).open('x') as f:json.dump(x,f,indent=2,sort_keys=True);f.write('\n')
# Capture only launcher options, never the shell command/env/credentials.
args=[a.decode(errors='replace') for a in pathlib.Path('/proc/1/cmdline').read_bytes().split(b'\0') if a]
cut=args.index('--') if '--' in args else len(args);prefix=args[:cut]
allowed={};flags=[]
for flag in ['--sandbox-policy-cwd','--command-cwd','--permission-profile']:
 if flag in prefix:
  v=prefix[prefix.index(flag)+1];allowed[flag]=json.loads(v) if flag=='--permission-profile' else v
for flag in ['--apply-seccomp-then-exec','--managed-network','--use-legacy-landlock']:flags.append({'FLAG':flag,'PRESENT':flag in prefix})
exe=pathlib.Path(os.readlink('/proc/1/exe'));s=exe.stat()
ancestry=[];pid=os.getpid()
for _ in range(8):
 p=pathlib.Path('/proc')/str(pid)
 try:
  status=p.joinpath('status').read_text();ppid=int(next(x.split(':',1)[1] for x in status.splitlines() if x.startswith('PPid:')))
  ancestry.append({'PID':pid,'PPID':ppid,'COMM':p.joinpath('comm').read_text().strip(),'EXE':os.readlink(str(p/'exe')),'SECURITY_FIELDS':[x for x in status.splitlines() if x.startswith(('Uid:','Gid:','NSpid:','NoNewPrivs:','Seccomp:','CapEff:','CapBnd:'))]})
 except OSError as exc:ancestry.append({'PID':pid,'STATUS':'NOT_OBSERVABLE','ERROR':str(exc)});break
 if ppid==0:break
 pid=ppid
profile=allowed.get('--permission-profile');assert profile is not None and profile.get('network')=='restricted'
put('outer-launch-context.json',{'OBSERVATION_TIME_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'PROCESS_ANCESTRY':ancestry,'VISIBLE_OUTER_EXECUTABLE':str(exe),'EXECUTABLE_RAW_SHA256':sha(exe),'RELEASE_PATH_VERSION':'0.162.0-x86_64-unknown-linux-musl','EXECUTABLE_UID':s.st_uid,'EXECUTABLE_GID':s.st_gid,'EXECUTABLE_MODE':oct(stat.S_IMODE(s.st_mode)),'ARGV0':prefix[0],'SELECTED_LAUNCH_OPTIONS':allowed,'BOOLEAN_FLAGS':flags,'COMMAND_BODY_OR_ENVIRONMENT_COPIED':False,'CURRENT_ENFORCER_IDENTIFICATION':'Local Codex linux-sandbox entrypoint in packaged app-server executable; managed permission profile applied before command exec','HISTORICAL_PACKAGE72_ATTRIBUTION':'Current inspected execution context; original Package72 outer argv/filter/owner assignment was not recorded. Same host/runtime indicators support a hypothesis, not an exact historical filter reconstruction.'})
configs=[]
for name in ['/home/gvasend/.codex/config.toml','/etc/codex/requirements.toml','/etc/codex/managed_config.toml','/home/gvasend/.codex/requirements.toml']:
 p=pathlib.Path(name);row={'PATH':name,'EXISTS':p.exists(),'READABLE':os.access(str(p),os.R_OK)}
 if row['EXISTS']:
  try:
   text=p.read_text();selected=[];section=''
   for line in text.splitlines():
    if re.match(r'^\s*\[',line):section=line.strip()
    elif re.match(r'^\s*(sandbox_mode|approval_policy|network_access|network_policy|sandbox_policy|experimental_use_linux_sandbox|use_linux_sandbox_bwrap)\s*=',line):selected.append({'SECTION':section,'POLICY_LINE':line.strip()})
   row.update(STATUS='READ_ONLY_POLICY_PROJECTION',RAW_SHA256=sha(p),SELECTED_POLICY_FIELDS=selected,UID=p.stat().st_uid,GID=p.stat().st_gid)
  except OSError as exc:row.update(STATUS='NOT_OBSERVABLE',ERROR=str(exc))
 else:row['STATUS']='ABSENT_IN_CURRENT_VIEW; no inference about cloud/managed overrides'
 configs.append(row)
put('launch-configuration-observations.json',{'FILES':configs,'EFFECTIVE_NETWORK_VALUE':'restricted from actual launcher argv, not inferred config default','CONFIG_CONTENT_DISCLOSURE':'Only allowlisted policy keys; no authentication/credential/proxy/model data captured','CONFIG_FILE_OWNER_IS_POLICY_OWNER_PROOF':False,'ADMIN_POLICY_ASSIGNMENT_AVAILABLE':False})
logs=[]
for name in ['/home/gvasend/.codex/log','/home/gvasend/.codex/logs','/var/log/audit/audit.log','/var/log/kern.log','/sys/kernel/security/apparmor/profiles']:
 p=pathlib.Path(name);row={'PATH':name,'EXISTS':p.exists(),'READABLE_ACCESS_CHECK':os.access(str(p),os.R_OK)}
 if p.is_file():
  try:
   data=p.read_text();matches=[x for x in data.splitlines() if any(q in x.lower() for q in ['bwrap','netlink','seccomp'])]
   row.update(STATUS='OBSERVED',READ_BYTES=len(data),RELEVANT_LINE_COUNT=len(matches))
   # Do not expose arbitrary logged command/credentials. Only classify relevance.
   row['MATCHING_PACKAGE72_DENIAL_ESTABLISHED']=False
  except OSError as exc:row.update(STATUS='NOT_OBSERVABLE',ERROR=str(exc))
 elif p.is_dir():row['STATUS']='DIRECTORY_PRESENT; no credential/history crawl'
 else:row['STATUS']='ABSENT_IN_CURRENT_VIEW'
 logs.append(row)
put('existing-denial-log-assessment.json',{'LOCATIONS':logs,'MATCHING_SYSCALL_DENIAL_FOUND':False,'NO_LOG_IS_COMPATIBILITY_PROOF':False,'BPF_FILTER_DUMP_AVAILABLE':False,'AUDIT_OR_PRIVILEGED_TRACE_ATTEMPTED':False})
put('policy-owner-assessment.json',{'IMPLEMENTATION_PROVIDER':'Codex packaged application/Linux sandbox','VISIBLE_OS_ACTOR_UID':os.geteuid(),'EVIDENCED_PERSON_OR_ORGANIZATION_POLICY_OWNER':None,'RESPONSIBLE_CONTROL_PLANE_ROLE':'Administrator/operator supplying this Codex app-server managed permission profile and linux-sandbox security policy','ROLE_IS_CONTACT_LOCUS_NOT_VERIFIED_DESIGNATION':True,'WHY_NOT_PROJECT_OWNER_BY_DEFAULT':'Project qualification charter and source-file ownership do not establish power over session/control-plane/OS security policy','OWNER_MAPPING_EVIDENCE_REQUIRED':'Authenticated session/installation policy assignment naming the actual operator empowered to attest this profile and permitted qualification launch contexts','RESPONSIBILITY_HANDOFF':'If that operator identifies an OS/LSM/container policy as the rejecting layer, obtain its actual security owner designation as part of the same evidence bundle.'})
missing=[{'ID':'M74-EFFECTIVE-FILTER','MISSING':'Effective filter/rule bundle for installed launcher/profile, identifying the action on socket(AF_NETLINK=16,type=0x80003,protocol=0)','ACCESS_STATUS':'Not exposed through proc status or inspected config; no privileged retrieval attempted','RESPONSIBLE_OWNER_ROLE':'Codex managed-profile/linux-sandbox operator'}, {'ID':'M74-POLICY-ORIGIN','MISSING':'Authoritative source and owner assignment for the managed permission profile used for Package72, linked to installed version/hash and original launch context','ACCESS_STATUS':'Current argv is observable; original per-command assignment absent','RESPONSIBLE_OWNER_ROLE':'Codex app-server/session permission-profile administrator'}, {'ID':'M74-DENIAL-CORRELATION','MISSING':'Existing syscall-denial audit or policy explanation correlated to Package72 operation, namespace/PID mapping and EPERM','ACCESS_STATUS':'Kernel log has no usable record; audit log absent; loaded AppArmor profile listing denied','RESPONSIBLE_OWNER_ROLE':'Launcher operator, with host/LSM security administrator if another layer owns the denial'}, {'ID':'M74-PERMITTED-CONTEXT','MISSING':'Exact approved same-host context allowing necessary private namespace route control while preserving every filesystem/network/process/resource limit','ACCESS_STATUS':'No authoritative permitted context supplied or discovered','RESPONSIBLE_OWNER_ROLE':'Actual outer-policy security administrator; project-owner qualification approval remains separately required'}]
put('missing-policy-evidence.json',{'ITEMS':missing,'DO_NOT_BYPASS':True,'PERMISSION_OR_SECURITY_CHANGES_REQUESTED':False})
put('assessment.json',{'PACKAGE_RESULT':'PARTIAL','BOUNDED_REVIEW_COMPLETE':True,'SAME_HOST_COMPATIBILITY':'UNDETERMINED','CURRENT_CONTEXT_COMPATIBILITY':'NOT_SUPPORTED_BY_EVIDENCE: recorded preflight failed and current restricted launch layer identified','FAILURE_POINT_ESTABLISHED':True,'EXACT_REJECTING_POLICY_RULE_ESTABLISHED':False,'OBSERVED_FACTS':['Codex linux-sandbox argv0 and installed local executable identified','managed permission profile sets network=restricted','--apply-seccomp-then-exec is present','current inherited seccomp mode2/no-new-privileges/capability restriction is visible','no usable matching denial evidence in inspected locations'],'HYPOTHESES':['Outer Codex restricted-network filtering may explain route-netlink EPERM; no exact BPF/argument rule or historical proof available','Other inherited/LSM/outer controls remain possible'],'ABSENCE_OF_DENIAL_LOG_IMPLIES_COMPATIBILITY':False,'DEDICATED_HOST_VM_CANDIDATE':{'STATUS':'UNQUALIFIED_NOT_PROVISIONED','REQUIREMENTS_REFERENCE':'../recovery-73/alternative-host-profile.json','PERMISSION_PROFILE_AND_OWNER':None,'TESTED':False},'SINGLE_RECOMMENDED_NEXT_ACTION':'Ask the administrator/operator of the Codex app-server managed launch profile for one authoritative, credential-free policy/denial evidence bundle identifying the actual policy owner, the decision for the Package72 route-netlink socket call, and any approved same-host qualification context. No probe or configuration change.','FUTURE_CAMPAIGN':'Separate explicit approval and exact current grant/journal binding required; stopped original journal cannot be reset/reused','PACKAGE75_INITIATED':False,'NETWORK_SOCKET_RETRIES':0,'CONFINEMENT_TESTS_RUN':0,'SOURCE_EDITS':0,'SECURITY_SETTINGS_CHANGED':False,'CAMPAIGN_RESUMED':False})
put('official-documentation-context.json',{'SKILL':'/home/gvasend/.codex/skills/.system/openai-docs/SKILL.md','PAGES':[{'URL':'https://learn.chatgpt.com/docs/config-file/config-reference','SUPPORT':'Managed/admin requirements may constrain settings; existence of configuration mechanism does not identify current policy assignment or owner'},{'URL':'https://learn.chatgpt.com/docs/security','SUPPORT':'General security-policy context; not proof of installed binary filter decisions'}],'LIMITATION':'Current official documentation is general context, not an attestation of deployment 0.162.0 or the failed historical socket. No policy rule inferred from it.'})
print(json.dumps({'PACKAGE_RESULT':'PARTIAL','SAME_HOST_COMPATIBILITY':'UNDETERMINED','OUTER_LAUNCHER':str(exe),'NETWORK_POLICY':profile['network'],'POLICY_OWNER_IDENTITY_VERIFIED':False,'RETRIES':0}))
