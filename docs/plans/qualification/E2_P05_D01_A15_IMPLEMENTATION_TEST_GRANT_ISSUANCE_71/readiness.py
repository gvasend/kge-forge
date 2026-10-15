"""Read-only current construction guard assessment, not activation or implementation.
Native/fake tests are never enabled by these documentary observations.
"""
import hashlib,json,os,pathlib,platform,stat,subprocess,sys
D=pathlib.Path(__file__).resolve().parent;R=D.parents[3];P=R/'docs/plans/qualification/E2_P05_D01_A15_IMPLEMENTATION_TEST_AUTHORITY_70'
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def assess():
 effective=json.loads(subprocess.check_output([sys.executable,str((D/'verify_effective.py').relative_to(R))],cwd=str(R)))
 subject=load(P/'implementation-test-authority-subject.json');c=subject['CONTENT']['CONTRACTS'];profile=c['environment-resource-permission-contract.json'];obs=load(P/'observed-environment.json')
 facts={'EP70-GRANT':effective['IMPLEMENTATION_TEST_GRANT_EFFECTIVE']=='YES'};actor_fail=[]
 actual={'OS':platform.system(),'MACHINE':platform.machine(),'KERNEL':platform.release(),'NODE_NAME':platform.node(),'BOOT_ID_SHA256':hashlib.sha256(pathlib.Path('/proc/sys/kernel/random/boot_id').read_bytes()).hexdigest()}
 if actual!=obs['HOST_FACTS']:actor_fail.append('approved host fingerprint mismatch')
 if os.geteuid()!=obs['UID'] or os.getegid()!=obs['GID']:actor_fail.append('approved acting UID/GID mismatch')
 if platform.python_version()!=obs['INTERPRETER_VERSION'] or sha(pathlib.Path(sys.executable).resolve())!=obs['INTERPRETER_BINARY_SHA256']:actor_fail.append('interpreter mismatch')
 if sha(pathlib.Path(obs['BWRAP_PATH']))!=obs['BWRAP_BINARY_SHA256']:actor_fail.append('approved bwrap bytes mismatch')
 facts['EP70-ACTOR']=not actor_fail
 observations=[];path_fail=[]
 for rel in c['source-file-scope.json']['PERMITTED_SOURCE_FILES']:
  p=R/rel
  if p.exists() or p.is_symlink():path_fail.append('new target is preexisting or symlink: '+rel)
  # Fixed approved workspace anchor: observe all prefix components for symlink
  # substitution; owner-control applies only to project-managed descendants,
  # never a claim of ownership/permission to change system filesystem ancestors.
  for ancestor in [p]+list(p.parents):
   if ancestor.is_symlink():path_fail.append('symlink ancestor: '+str(ancestor))
  parent=p.parent
  while not parent.exists():parent=parent.parent
  if R!=parent and R not in parent.parents:path_fail.append('creation parent outside approved workspace')
  st=parent.stat();row={'SOURCE_PATH':rel,'CURRENT_EXISTING_CREATION_PARENT':str(parent),'UID':st.st_uid,'GID':st.st_gid,'MODE':oct(stat.S_IMODE(st.st_mode)),'WRITE':os.access(str(parent),os.W_OK),'SEARCH':os.access(str(parent),os.X_OK),'NEW_TARGET_ABSENT':not p.exists() and not p.is_symlink()};observations.append(row)
  if not row['WRITE'] or not row['SEARCH']:path_fail.append('current source-parent write/search denied: '+rel)
  if st.st_uid!=os.geteuid():path_fail.append('foreign project source-parent ownership: '+rel)
  if st.st_uid!=os.geteuid():actor_fail.append('unverified source resource control: '+rel)
 facts['EP70-ACTOR']=not actor_fail
 facts['EP70-PATHS']=not path_fail
 audit={'METHOD':'External documentary reader, outside the six modules under test; authenticated explicit owner grant and source/resource evidence, not a worker self-assertion','CONTROLLER_SOURCE_IDENTITY':{'kind':'CONTENT_IDENTITY','namespace':'raw-file-sha256','sha256':sha(pathlib.Path(__file__))},'EVIDENCE_LOCATION':str(D.relative_to(R)),'ENTRYPOINT':'readiness.assess (read-only)','FUTURE_AUDIT_REQUIREMENT':'Before/during actual construction, recheck the grant/current guards and preserve exact source-path operation and before/after bytes. Code/test/fixture/profile hashes are generated phase artifacts, not claimed present now. No campaign/runtime process evidence is fabricated.'}

 audit['CURRENT_BINDINGS']={'APPROVED_SUBJECT_IDENTITY':subject['IDENTITY'],'GRANT_IDENTITY':effective['GRANT_IDENTITY'],'EFFECTIVE_REFERENCE_PIN':effective['EFFECTIVE_REFERENCE_PIN'],'APPROVED_PROFILE_POLICY_RAW_SHA256':sha(P/'environment-resource-permission-contract.json'),'OWNER_DECISION_RAW_SHA256':sha(D/'project-owner-decision.json'),'CURRENT_SCOPE_SOURCE_FILES':c['source-file-scope.json']['PERMITTED_SOURCE_FILES']}
 audit['INITIAL_ENTRY_ONLY']='All six paths absent at initial entry. Once legitimate construction begins, future controller must distinguish authorized campaign-created files/edits using immutable creation audit from preexisting foreign targets; this initial checker is not an ongoing editor or blanket rejection of authorized edits.'
 facts['EP70-AUDIT']=True
 required=profile['PHASE_GUARDS']['CONSTRUCTION'];ready=all(facts.get(x) is True for x in required)
 return {'RESULT':'PASS_READ_ONLY_GUARD_ASSESSMENT','GRANT_IDENTITY':effective['GRANT_IDENTITY'],'IMPLEMENTATION_TEST_GRANT_EFFECTIVE':'YES','CONSTRUCTION_GUARD':{'REQUIRED':required,'CURRENT_FACTS':facts,'ACTOR_FAILURES':actor_fail,'PATH_FAILURES':path_fail,'RESOURCE_OBSERVATIONS':observations,'AUDIT_EVIDENCE':audit,'ASSESSMENT_BOUNDARY':'Point-in-time approved host/actor/project-managed creation parents and documentary audit. Revalidate independently immediately before construction; no future OS rights or test confinement inferred.'},'CONSTRUCTION_ACTIVATION_READY':'YES' if ready else 'NO','CONSTRUCTION_ACTIVATED':False,'ADAPTER_CONSTRUCTION_PERFORMED':False,'FAKE_PROTOCOL_TEST_READY':'NO','NATIVE_SYNTHETIC_TEST_READY':'NO','TEST_BLOCKERS':['All six implementation source files currently absent','Exact code/invocation/dependency/profile evaluator seals not produced','Actual resource enforcement/network/filesystem/process confinement not independently established','Fake protocol qualification not performed','Synthetic fixture/oracle identities and runtime comparison evidence not produced'],'TEST_PROFILE_SEALED':'NO','SYNTHETIC_TESTS_EXECUTED':False,'A15_EXECUTION_AUTHORITY_ISSUED':'NO','A15_CAPTURE_AUTHORITY_ISSUED':'NO','A15_EXECUTED':False}
if __name__=='__main__':print(json.dumps(assess(),sort_keys=True))
