"""Independent readonly source/evidence reconstruction; no namespace/socket tests."""
import ast,copy,hashlib,json,os,pathlib,sys
D=pathlib.Path(__file__).resolve().parent;E=D.parent;R=D.parents[4];Q=R/'docs/plans/qualification'
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canon(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def verify(overrides=None):
 overrides=overrides or {}
 def read(n):return copy.deepcopy(overrides[n]) if n in overrides else load(D/n)
 prior=load(E/'evidence-index.json');assert all(sha(R/p)==h for p,h in prior['FILES'].items())
 failure=load(E/'resource-enforcement-assessment.json');assert failure['OBSERVATIONS'][0]['exit_status']==1 and failure['NO_RETRY_OR_FALLBACK']
 assert failure['OBSERVATIONS'][0]['stderr']=='bwrap: loopback: Failed to create NETLINK_ROUTE socket: Operation not permitted\n'
 assert not failure['REQUIRED_CONTROLS_ENFORCEABLE'] and failure['FAKE_PROTOCOL_TESTS_EXECUTED']==failure['NATIVE_CALLS']==0
 auth=read('failure-evidence-authentication.json');assert auth['EXIT_STATUS']==1 and auth['STDERR']==failure['OBSERVATIONS'][0]['stderr'] and auth['PROCESS_OBSERVATION']==failure['OBSERVATIONS'][0]
 assert auth['RETRIES']==auth['FALLBACKS']==auth['RECOVERY_ATTEMPTS']==0
 assert auth['SOURCE_FILES_UNCHANGED'] and auth['ARGV_EVIDENCE_STATUS'].startswith('Source-derived reconstruction, not originally recorded argv.')
 assert canon(auth['INVOKED_ARGV_RECONSTRUCTION'])==auth['ARGV_RECONSTRUCTION_SHA256']
 argv=auth['INVOKED_ARGV_RECONSTRUCTION'];assert argv[0]=='/usr/bin/bwrap' and all(x in argv for x in ['--unshare-user','--unshare-net','--unshare-pid','--unshare-ipc','--unshare-uts','--cap-drop','--ro-bind'])
 assert argv[-3:-1]==['/usr/bin/python3','-c']
 tree=ast.parse((R/'adapter/qualification_a15/supervisor.py').read_text());probe=ast.literal_eval(next(x.value for x in tree.body if isinstance(x,ast.Assign) and any(isinstance(a,ast.Name) and a.id=='PROBE' for a in x.targets)))
 assert argv[-1]==probe.replace("os.environ['A15_PROBE_FIXTURES']",repr(failure['SCRATCH_BOUNDARY']+'/fixtures'))
 for p,h in failure['SOURCE_SEAL'].items():assert sha(R/p)==h
 ledger=[json.loads(x) for x in (E/'campaign-budget.jsonl').read_text().splitlines()];assert [x['kind'] for x in ledger]==['campaign_start','reserve','bytes','release','stop']
 assert sum(x.get('amount',0) for x in ledger if x['kind']=='reserve')==2
 binary=read('installed-binary-localization.json');assert binary['BINARY_RAW_SHA256']==sha(pathlib.Path('/usr/bin/bwrap'))
 assert binary['SOCKET_ARGUMENTS_X86_64_ABI']=={'edi_address_family':16,'esi_type_and_flags':524291,'edx_protocol':0}
 assert binary['BWRAP_EXECUTED'] is False and '0.4.0-1ubuntu4.1' in binary['PACKAGE']
 obs=read('read-only-environment-inventory.json');assert obs['SYSTEM_SETTINGS_CHANGED'] is False and obs['BWRAP_RETRIED'] is False and obs['ELEVATED_PERMISSION_REQUESTED'] is False
 assert obs['BWRAP']['SUID'] is False and obs['BWRAP']['RAW_SHA256']==binary['BINARY_RAW_SHA256']
 assert obs['SECCOMP_EFFECTIVE_FILTER_RULES']['STATUS']=='NOT_OBSERVABLE' and obs['HISTORICAL_CHILD_SECURITY_CONTEXT']['STATUS']=='UNDETERMINED'
 fields=dict(line.split(':',1) for line in obs['READS']['/proc/self/status']['VALUE'].splitlines())
 assert fields['Seccomp'].strip()=='2' and fields['CapBnd'].strip()=='0000000000000000'
 assert obs['READS']['/proc/sys/kernel/unprivileged_userns_clone']['VALUE'].strip()=='1'
 assert obs['READS']['/proc/self/attr/current']['VALUE'].strip()=='unconfined'
 assert obs['INTERPRETER']['RAW_SHA256']==sha(pathlib.Path(sys.executable).resolve())
 cause=read('confinement-root-cause-assessment.json');assert cause['FAILURE_POINT_ESTABLISHED'] is True and cause['FAILURE_CAUSE_ESTABLISHED'] is False
 expected={'H73-NETNS-CREATE-DENIED':'CONTRADICTED','H73-LOOPBACK-STAGE':'SUPPORTED','H73-NETLINK-SOCKET-DENIED':'SUPPORTED','H73-USERNS-GLOBALLY-DISABLED':'CONTRADICTED','H73-MISSING-CAPABILITY-ROOT-CAUSE':'UNDETERMINED','H73-SPECIFIC-SECCOMP-RULE':'UNDETERMINED','H73-APPARMOR-OR-LSM':'UNDETERMINED','H73-OUTER-CONTAINER-OR-LAUNCHER-POLICY':'UNDETERMINED','H73-INVOCATION-CONFIGURATION-CAUSE':'UNDETERMINED'}
 assert {x['HYPOTHESIS_ID']:x['CLASSIFICATION'] for x in cause['HYPOTHESES']}==expected
 assert cause['NO_GLOBAL_HOST_INCAPABILITY_INFERENCE'] is True
 approved=load(Q/'E2_P05_D01_A15_IMPLEMENTATION_TEST_AUTHORITY_70/environment-resource-permission-contract.json')
 controls=read('approved-control-matrix.json');assert controls['RESOURCE_LIMITS']==approved['RESOURCE_LIMITS'] and controls['P70_PHASE_GUARDS']==approved['PHASE_GUARDS']
 assert len(controls['CONTROL_MATRIX'])==8
 net=next(x for x in controls['CONTROL_MATRIX'] if x['CONTROL_ID']=='NETWORK_BOUNDARY');assert net['ENFORCER'].startswith('OS ') and 'Never remove --unshare-net' in net['NON_SUBSTITUTION_RULE']
 fs=next(x for x in controls['CONTROL_MATRIX'] if x['CONTROL_ID']=='FILESYSTEM_BOUNDARY');assert 'OS mount/access confinement' in fs['ENFORCER'] and 'checks alone do not enforce' in fs['NON_SUBSTITUTION_RULE']
 host=read('existing-host-recovery-assessment.json');assert host['EXISTING_HOST_COMPATIBLE']=='UNDETERMINED' and host['CONFIGURATION_CHANGED'] is False
 alt=read('alternative-host-profile.json');assert alt['ACTUAL_HOST_IDENTITY'] is None and alt['ACTUAL_HOST_QUALIFIED'] is False and alt['MIGRATION_PERFORMED'] is False and alt['ACTUAL_A15_EXECUTION_ALLOWED'] is False
 assert alt['ACTUAL_SECURITY_PROFILE_IDENTITY'] is None and alt['RESOURCE_LIMITS']==approved['RESOURCE_LIMITS'] and alt['PROFILE_COMPLETE_FOR_IMPLEMENTABLE_DECISION'] is False
 equivalent=read('alternative-confinement-equivalence-assessment.json');assert equivalent['ALTERNATIVE_CONFINEMENT_EQUIVALENT']=='UNDETERMINED' and equivalent['SUBSTITUTION_SELECTED'] is False and equivalent['UNRESTRICTED_SUBPROCESS_EQUIVALENT'] is False
 assert all(x['EQUIVALENCE']=='UNDETERMINED' and x['QUALIFIED'] is False for x in equivalent['OPTIONS'])
 auth=read('campaign-authority-assessment.json');state=load(E/'grant-state-observation.json');assert state['CURRENT_GRANT_ACTIVE_FOR_FURTHER_CAMPAIGN_OPERATIONS'] is False
 assert auth['ORIGINAL_CAMPAIGN_TERMINATED'] is True and auth['AUTOMATIC_RETRIES']==0 and auth['FRESH_CAMPAIGN_AUTHORITY_REQUIRED'] is True
 assert auth['OLD_GRANT_REFERENCE_ALONE_MAY_AUTHORIZE_NEW_CAMPAIGN'] is False and auth['NEW_GRANT_ISSUED'] is False and auth['NEW_CAMPAIGN_SUBJECT_READY'] is False and auth['DECISION_OPTIONS']==[]
 assert auth['EXTRA_CAMPAIGNS']=='FRESH_EXPLICIT_BOUNDED_APPROVAL'
 comparison=read('recovery-comparison.json');assert comparison['SUPERIOR_OPTION_PROVEN'] is False and comparison['SELECTED_RECOVERY_ENVIRONMENT'] is None and len(comparison['OPTIONS'])==3
 gates=read('readiness-gates.json');assert gates=={'FAILURE_CAUSE_ESTABLISHED':'NO','FAILURE_POINT_ESTABLISHED':'YES','EXISTING_HOST_COMPATIBLE':'UNDETERMINED','ALTERNATIVE_HOST_PROFILE_COMPLETE':'NO (requirements specified; actual host/profile/permission bindings absent)','ALTERNATIVE_CONFINEMENT_EQUIVALENT':'UNDETERMINED','RESOURCE_ENFORCEMENT_READY':'NO','FRESH_CAMPAIGN_AUTHORITY_REQUIRED':'YES','FAKE_PROTOCOL_TEST_READY':'NO','NATIVE_SYNTHETIC_TEST_READY':'NO','CURRENT_CAMPAIGN_ACTIVE':'NO','CAMPAIGN_AUTHORITY_DOSSIER_READY':'NO'}
 for p in [D/'inspect.py',D/'verify.py']:
  for n in ast.walk(ast.parse(p.read_text())):
   if isinstance(n,ast.Import):assert all(not a.name.startswith('adapter') for a in n.names)
   if isinstance(n,ast.ImportFrom):assert not (n.module or '').startswith('adapter')
 return {'RESULT':'PASS_STATIC_PARTIAL_RECOVERY','PACKAGE72_FAILURE_AUTHENTICATED':'YES','FAILURE_POINT_ESTABLISHED':'YES','UNDERLYING_CAUSE_ESTABLISHED':'NO','SOURCE_HASHES':failure['SOURCE_SEAL'],'INVOCATION_RECONSTRUCTION_HASH':canon(argv),'INSTALLED_BINARY_LOCALIZATION_HASH':canon(binary),'ENVIRONMENT_SNAPSHOT_HASH':canon(obs),'HYPOTHESES':expected,'APPROVED_CONTROLS_HASH':canon(controls),'RECOVERY_COMPARISON_HASH':canon(comparison),'AUTHORITY_ASSESSMENT_HASH':canon(auth),'READINESS':gates,'RECOVERY_EXECUTIONS':0}
if __name__=='__main__':print(json.dumps(verify(json.load(sys.stdin) if '--candidate' in sys.argv else None),sort_keys=True))
