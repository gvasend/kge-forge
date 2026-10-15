"""Static Package69 evidence construction; imports no Planner runtime modules.
This is an inventory tool, not the proposed supervisor, worker, reader or tests.
"""
import ast, hashlib, json, os, pathlib, platform, stat, sys, datetime
D=pathlib.Path(__file__).resolve().parent;R=D.parents[3];Q=R/'docs/plans/qualification'
P61=Q/'E2_P05_D01_A15_CAPTURE_PERSISTENCE_RESUME_CLOSURE_61'
WP='E2-P05-D01-A15-EXECUTOR-ENVIRONMENT-QUALIFICATION-69'
def load(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def canon(x): return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def pin(p): return {'PATH':str(p.relative_to(R)),'RAW_SHA256':sha(p)}
def write(name,data):
 with (D/name).open('x') as f: json.dump(data,f,indent=2,sort_keys=True);f.write('\n')
def sym(path,name):
 t=ast.parse(path.read_text());parts=name.split('.');nodes=t.body
 for part in parts:
  n=next(x for x in nodes if isinstance(x,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)) and x.name==part)
  nodes=n.body
 args=n.args if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) else None
 if args:
  aa=list(args.posonlyargs)+list(args.args);default_at=len(aa)-len(args.defaults);words=[]
  for i,a in enumerate(aa):
   val=ast.get_source_segment(path.read_text(),args.defaults[i-default_at]) if i>=default_at else None
   words.append(a.arg+('='+val if val is not None else ''))
  if args.vararg:words.append('*'+args.vararg.arg)
  elif args.kwonlyargs:words.append('*')
  for a,z in zip(args.kwonlyargs,args.kw_defaults):words.append(a.arg+('='+ast.get_source_segment(path.read_text(),z) if z is not None else ''))
  if args.kwarg:words.append('**'+args.kwarg.arg)
  signature='('+', '.join(words)+')'
 else: signature='class'
 return signature,n.lineno

# Authenticate all sealed inputs; no effecting scripts are invoked.
auth=[]
for name in ['E2_P05_D01_A15_NORMATIVE_ADOPTION_ISSUANCE_68','E2_P05_D01_A15_BOUNDED_AUTHORITY_DECISION_PREPARATION_67','E2_P05_D01_A15_BOUNDED_AUTHORITY_QUALIFICATION_62','E2_P05_D01_A15_CAPTURE_PERSISTENCE_RESUME_CLOSURE_61','E2_P05_D01_A15_PROSPECTIVE_SCENARIO_DESIGN_59','KGE_FORGE_QUALIFICATION_GOVERNANCE_CHARTER_ADOPTION_66','KGE_FORGE_QUALIFICATION_GOVERNANCE_CHARTER_65','E2_P05_D01_A14_RUNTIME_PERSISTENCE_QUALIFICATION_31']:
 p=Q/name/'evidence-index.json';a=load(p)
 for file,h in a['FILES'].items():assert sha(R/file)==h,file
 auth.append({'EVIDENCE_INDEX':pin(p),'FILES_VERIFIED':len(a['FILES'])})
# Preserve current workspace evidence/runtime bytes, without overwriting earlier inventories.
baseline={}
for base in ['adapter','docs','rust']:
 if not (R/base).exists():continue
 for p in (R/base).rglob('*'):
  if p.is_file() and D not in p.parents and '__pycache__' not in p.parts:baseline[str(p.relative_to(R))]=sha(p)
for name in ['E2-DECIDE.json','E2-CHECK.json','E2-COLLECT.json','E2-FINISH.json','E2-PREPARE.json','source.json','resolution.json']:
 if (R/name).exists():baseline[name]=sha(R/name)
write('preservation-before.json',baseline)
write('input-authentication.json',{'RESULT':'PASS','INDICES':auth,'NATIVE_FUNCTIONS_CALLED':False})
sub=load(Q/'E2_P05_D01_A15_BOUNDED_AUTHORITY_QUALIFICATION_62'/'authority-subject-manifest.json')
assert canon(sub['TECHNICAL_BODY'])==sub['TECHNICAL_PREPARATION_IDENTITY']['sha256']=='befe07aacc6b4c4e203488bce731f265a0520cf145174dca33dbfb4e68b43e9b'
checkpoint=load(P61/'initial-checkpoint-restore-contract.json')
for p,h in checkpoint['RETAINED_LEDGER_FILES'].items():assert sha(R/p)==h
assert len(checkpoint['RETAINED_LEDGER_FILES'])==20
# Explicitly verify live source and policy pins, not only a historical PASS label.
bundle=load(R/checkpoint['SOURCE_PATH'])['bundle'];pins=bundle['sources']+[bundle['policy']]
for p in pins: assert p['profile']['value']=='raw-file-sha256' and sha(R/p['path'])==p['identity']['sha256']
assert len(pins)==55
harness=load(P61/'static-harness-contract.json');assert harness['STATIC_HARNESS_READY'] and len(harness['EXACT_OPERATION_BINDINGS'])==2
for x in harness['EXACT_OPERATION_BINDINGS']:assert load(P61/x['ORACLE_FILE'])['FULL_ORACLE_READY']
write('checkpoint-and-variant-bindings.json',{'TECHNICAL_SUBJECT':sub['TECHNICAL_PREPARATION_IDENTITY'],'CHECKPOINT_CONTRACT_PIN':pin(P61/'initial-checkpoint-restore-contract.json'),'CHECKPOINT_PATH':checkpoint['SOURCE_PATH'],'INITIAL_SNAPSHOT_IDENTITY':checkpoint['INITIAL_SNAPSHOT_IDENTITY'],'BUNDLE_IDENTITY':checkpoint['NATIVE_BUNDLE_IDENTITY'],'LEDGER_FILES_VERIFIED':19,'LIVE_PINS_VERIFIED':55,'STARTING_PRECONDITION_PIN':pin(P61/'starting-state-precondition-oracle.json'),'STARTING_STATE_EVIDENCE_KIND':'Retained Package61 oracle and exact unchanged checkpoint; no native restore/query run','VARIANTS':[{'BINDING':load(P61/x['CAPTURE_BINDING']),'ORACLE_PIN':pin(P61/x['ORACLE_FILE']),'ORACLE_CANONICAL_SHA256':canon(load(P61/x['ORACLE_FILE']))} for x in harness['EXACT_OPERATION_BINDINGS']],'STATIC_HARNESS_PIN':pin(P61/'static-harness-contract.json'),'NO_NATIVE_RESTORE':True})

A14='docs/plans/qualification/E2_P05_D01_A14_RUNTIME_PERSISTENCE_QUALIFICATION_31/execute.py'
V3='docs/plans/qualification/E2_P05_D01_SOURCE_BYTES_DISPATCH_CORRECTION_33/runner_v3.py'
WR='docs/plans/qualification/E2_P05_D01_A14_WRITER_HANDOFF_CLOSURE_28/writer_entrypoint.py'
RD='docs/plans/qualification/E2_P05_D01_A14_COLD_READER_BINDING_CLOSURE_29/reader_entrypoint.py'
# Each status is bounded to the stated evidence domain, never universal qualification.
rows=[
('N69-RESTORE','adapter/planner/codec.py','restore','IMPLEMENTED_AND_QUALIFIED','A14 save/reader retained evidence, zero-event frame only','19-event A15 exact start and post-invalidation cold restore must be integrated and qualified'),
('N69-INVALIDATION','adapter/planner/core.py','apply_event','IMPLEMENTED_NOT_QUALIFIED','Package61 source contract and typed-proof test source','No observed qualification of these two sealed A15 variants'),
('N69-RECORD','adapter/planner/codec.py','record_result','IMPLEMENTED_NOT_QUALIFIED','Package61 native interface and capture bindings','No A15 implementation binding updated PersistenceBundle to complete DTO'),
('N69-SERIALIZE','adapter/planner/codec.py','bundle_bytes','IMPLEMENTED_AND_QUALIFIED','A14 native bundle bytes/persistence evidence only','Full Package61 updated bundle/events comparison integration'),
('N69-PUBLISH','adapter/planner/codec.py','save_bundle','IMPLEMENTED_AND_QUALIFIED','A14 retained native immutable publication only','Integrate two A15 targets, 20-event manifests and publication guards'),
('N69-IMMUTABLE','adapter/planner/codec.py','_write_immutable','IMPLEMENTED_AND_QUALIFIED','A14 retained publication; file fsync then hard-link only','No multi-file atomicity/directory-fsync/general crash guarantee'),
('N69-RESUME','adapter/planner/core.py','resume_eligibility','IMPLEMENTED_NOT_QUALIFIED','Package61 complete independent reason oracle and existing test source','Compare all four fields including ordered reasons under new A15 harness'),
('N69-USABILITY','adapter/planner/typed_proofs.py','usable','IMPLEMENTED_NOT_QUALIFIED','Existing typed proof test source plus Package61 expected queries','Full native usability/ALL-ANY comparison for both A15 outputs'),
('N69-REPLAY','adapter/planner/codec.py','_replay','IMPLEMENTED_AND_QUALIFIED','A14 restore replay validation within retained A14 frame','New 20-event full-output comparison and preserved 19-event prefix'),
('R69-A14-SUPERVISOR',A14,'launch','PARTIALLY_IMPLEMENTED','Package31 two writers/24 cold-reader retained results','Fixed A14 authority, frame, source modules, 12 readers per row; lacks Package61 A15 scope/results'),
('R69-A14-WRITER',WR,'run_writer','PARTIALLY_IMPLEMENTED','Package31 retained save/handoff evidence','Rejects any events; cannot restore/apply/record exact A15 inputs'),
('R69-A14-READER',RD,'run_reader','PARTIALLY_IMPLEMENTED','Package31 retained fresh-reader evidence','Requires zero events and different policy/frame; no complete A15 DTO/query oracle comparison'),
('R69-V3-CAPTURE',V3,'capture','PARTIALLY_IMPLEMENTED','Selected V3 source and Package61 exact normalized DTO shape','Selected A15 dispatch still carries prior bundle after apply_event; no dispatch repair authorized'),
('R69-V3-PROCESSES',V3,'cold_readers','PARTIALLY_IMPLEMENTED','Static source presence only; no new run','Synchronous process calls exist; no A15 exact handoff/publication/oracle/authority gates'),
('R69-CGROUP','adapter/host_supervisor.py','HostScopeSupervisor.__init__','IMPLEMENTED_NOT_QUALIFIED','Generic supervisor source/tests, unrelated cgroup-v2 domain','No A15 adapter or proof of delegated subtree availability/permission'),
('R69-BARRIER','adapter/exec_barrier.py','run','IMPLEMENTED_NOT_QUALIFIED','Generic launch barrier source only','Bubblewrap/cgroup/security launcher not qualified for exact A15 profile'),
('R69-PAYLOAD','adapter/qual_launcher.py','run','IMPLEMENTED_NOT_QUALIFIED','Unrelated A2.1c payload source','Detached-descendant payload is not an A15 qualification worker; must not invoke')]
inv=[]
for cid,path,entry,status,evidence,missing in rows:
 signature,line=sym(R/path,entry)
 inv.append({'COMPONENT_ID':cid,'SOURCE_PATH':path,'SOURCE_IDENTITY':pin(R/path),'ENTRYPOINT':entry,'FUNCTION_SIGNATURE':signature,'LINE':line,'EXISTING_TEST_EVIDENCE':evidence,'QUALIFICATION_STATUS':status,'QUALIFICATION_DOMAIN':'Retained A14 primitive domain only' if status=='IMPLEMENTED_AND_QUALIFIED' else 'No Package61 A15 orchestration qualification asserted','MISSING_BEHAVIOR':missing,'INVOKED':False})
write('existing-implementation-inventory.json',inv)
write('native-entrypoint-mapping.json',{'MAPPING':[x for x in inv if x['COMPONENT_ID'].startswith('N69-')],'SEQUENCE':'restore original checkpoint -> record_result(original bundle, exact supplied SourceInvalidation) -> save_bundle(updated bundle) -> successful writer exit observed by supervisor -> fresh reader restore -> complete comparison','SEPARATE_APPLY_EVENT':'Forbidden before record_result; record_result owns application','DO_NOT_USE':'codec.commit_event/HEAD mutation; unrelated A2.1c payload; A14 grant; old selected V3 dispatch as a complete A15 invocation'})
# Source inventory search is auditable and excludes immutable E1 experiment copies from implementation candidates.
scan=[]
for base in [R/'adapter',Q]:
 for p in sorted(base.rglob('*.py')):
  if D in p.parents or '__pycache__' in p.parts:continue
  text=p.read_text()
  matches=[x for x in ['SourceInvalidation','record_result','save_bundle','Popen','cold_readers','writer_exit_observed','A15'] if x in text]
  if matches:scan.append({'SOURCE_PIN':pin(p),'MATCHED_TERMS':matches})
write('implementation-search-evidence.json',{'SEARCH_BOUNDARY':['adapter/**/*.py','docs/plans/qualification/**/*.py excluding current Package69'],'E1_COPIES':'Read-only retained evidence; not executable candidates','MATCHES':scan,'CONCLUSION':'Required exact A15 executable is not established by any matched candidate; full implementation absence is bounded to inspected repository sources'})
capabilities=[
('C69-CHECKPOINT','PARTIALLY_IMPLEMENTED',['N69-RESTORE'],'Native restore exists; A15 start gate integration missing'),
('C69-INVALIDATION-CAPTURE','PARTIALLY_IMPLEMENTED',['N69-INVALIDATION','N69-RECORD','R69-V3-CAPTURE'],'Exactly one record_result call; compare updated DTO/events before save'),
('C69-PUBLICATION-HANDOFF','PARTIALLY_IMPLEMENTED',['N69-PUBLISH','N69-IMMUTABLE','R69-A14-WRITER'],'A15 exact immutable manifest and handoff adapter missing'),
('C69-WRITER-EXIT','PARTIALLY_IMPLEMENTED',['R69-A14-SUPERVISOR','R69-V3-PROCESSES'],'Own-child exit observation before readers exists generically, not A15 qualified'),
('C69-COLD-READERS','PARTIALLY_IMPLEMENTED',['R69-A14-READER','R69-V3-PROCESSES'],'Eight fresh readers, four per variant, full 20-event/DTO/query comparisons missing'),
('C69-ISOLATION','PARTIALLY_IMPLEMENTED',['R69-A14-SUPERVISOR','R69-CGROUP','R69-BARRIER'],'Exact A15 process/row isolation and enforced filesystem/network boundary unqualified'),
('C69-FAILURE-RETRY','PARTIALLY_IMPLEMENTED',['R69-A14-SUPERVISOR','N69-PUBLISH'],'Package61 fail-closed failure map not wired to exact supervisor; no automatic retries'),
('C69-EXACT-SUPERVISOR-WORKER','NOT_IMPLEMENTED',[],'No established Package61 A15 supervisor/writer/reader executable binding'),
('C69-ENVIRONMENT-SEAL','NOT_IMPLEMENTED',[],'No actual A15 executable/launcher permission profile sealed')]
write('supervisor-worker-capability-matrix.json',[{'CAPABILITY_ID':cid,'STATUS':s,'COMPONENTS':cs,'MISSING_BEHAVIOR':m,'REQUIRED_PROCESS_CONTRACT_PIN':pin(P61/'writer-handoff-cold-reader-contracts.json')} for cid,s,cs,m in capabilities])

# Observations require no native calls, socket requests, signals, file probes or privilege escalation.
exe=pathlib.Path(sys.executable);binary=exe.resolve()
def permission(p):
 st=p.stat();return {'PATH':str(p),'RESOLVED':str(p.resolve()),'MODE':oct(stat.S_IMODE(st.st_mode)),'OWNER_UID':st.st_uid,'OWNER_GID':st.st_gid,'SYMLINK':p.is_symlink(),'EUID_R_ACCESS':os.access(str(p),os.R_OK),'EUID_W_ACCESS':os.access(str(p),os.W_OK),'EUID_X_ACCESS':os.access(str(p),os.X_OK)}
obs={'OBSERVATION_TIME_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'HOST_IDENTITY':None,'HOST_IDENTITY_REASON':'Observed uname is not a sealed trusted host identity','OPERATING_SYSTEM':platform.system(),'KERNEL_RELEASE':platform.release(),'MACHINE':platform.machine(),'PYTHON_RUNTIME':{'EXECUTABLE_PATH':str(exe),'RESOLVED_PATH':str(binary),'VERSION':platform.python_version(),'RAW_SHA256':sha(binary)},'EUID':os.geteuid(),'EGID':os.getegid(),'WORKSPACE_BOUNDARY':str(R),'FILESYSTEM_BOUNDARY':['/home/gvasend/app/kge-forge','/tmp'],'PERMISSIONS':[permission(p) for p in [R,Q,P61,R/checkpoint['SOURCE_PATH'],pathlib.Path('/tmp'),binary]],'PROCESS_CREATION_CAPABILITY':'Ordinary read-only inventory processes observed; no native worker, sandbox launcher or cold reader launched','PROCESS_ISOLATION':'Separate metadata processes only; future A15 isolation not established','NETWORK_ACCESS':'Not probed; tool environment network restricted, exact future deny enforcement UNDETERMINED','AUDIT_BOUNDARY':'Only Package69 documentary artifacts; no runtime evidence','ENVIRONMENT_FRESHNESS':'Point-in-time observation only; reverify every binding at future entry','RESOURCE_PERMISSION_SOURCE':'stat/os.access/current actor observations, not charter-granted OS rights','OBSERVED_CGROUP_BASE_EXISTS':pathlib.Path('/sys/fs/cgroup/unified/kge-forge/executor').exists(),'BWRAP_PRESENT':pathlib.Path('/usr/bin/bwrap').exists(),'REQUIRED_PERMISSIONS_NOT_PROBED':['hard-link publication in future output directories','future launcher cgroup/namespace rights','enforced no-network policy','future actor access','resource-limit enforcement']}
write('execution-environment-observations.json',obs)
resource={'CURRENT_FILESYSTEM_READS':'VERIFIED_CURRENT_ACTOR: checkpoint, 19 ledgers and 55 raw source/policy bytes authenticated','CURRENT_PARENT_DAC_WRITES':'OBSERVED via stat/os.access only; no A15 runtime target created','ISOLATED_FILESYSTEM_WRITES':'UNDETERMINED_FUTURE_PROFILE','IMMUTABLE_HARDLINK_PUBLICATION':'A14 capability evidence, not verified permission at future A15 row targets','PROCESS_CREATION':'Observed metadata subprocess capability; actual A15 launcher binding unsealed','PROCESS_TERMINATION_OBSERVATION':'Python supervisor mechanism exists in retained A14 code, no new runtime exercise','FRESH_READER_LAUNCH':'Ordinary process mechanism exists, future launcher/policy unsealed','LOCAL_TEMPORARY_STORAGE':'Current /tmp stat/access only; exact private scratch mount unsealed','AUDIT_PUBLICATION':'Package69 documentary publication works; future runtime audit targets/profile unsealed','NETWORK_DENIAL':'UNDETERMINED enforcement for future native worker','RESOURCE_PERMISSIONS_VERIFIED':False,'ELEVATION_REQUESTED':False,'CHARTER_CREATES_OS_PERMISSIONS':False}
write('resource-permission-assessment.json',resource)

# Candidate source identities are pins, not qualified A15 invocation identities.
invocations=[]
for path,entry in [(V3,'run_preapproved'),(A14,'execute'),(WR,'run_writer'),(RD,'run_reader'),('adapter/exec_barrier.py','run')]:
 invocations.append({'EXECUTABLE_PATH':path,'SOURCE_IDENTITY':pin(R/path),'INTERPRETER':obs['PYTHON_RUNTIME'],'DEPENDENCIES':'Python standard library and source-local adapter dependencies; complete transitive future closure unsealed','INVOCATION_ARGUMENTS':None,'EXISTING_ENTRYPOINT':entry,'WORKING_DIRECTORY':str(R),'ENVIRONMENT_VARIABLES':None,'INPUT_BOUNDARY':'Existing candidate-specific subject; not transferable to A15','OUTPUT_BOUNDARY':'Existing candidate-specific scope; no output granted by inventory','NETWORK_POLICY':'Future exact enforcement unsealed','AUTHORITY_REQUIREMENT':'Explicit bounded implementation/test or A15 execution/evidence grant matching candidate purpose','QUALIFICATION_EVIDENCE':'Existing domain only; no candidate is designated qualified A15 executable'})
write('candidate-executable-invocation-inventory.json',invocations)

# Proposed minimal new qualification adapter files, not native runtime changes.
source_files=['adapter/qualification_a15/__init__.py','adapter/qualification_a15/contracts.py','adapter/qualification_a15/supervisor.py','adapter/qualification_a15/worker.py','adapter/qualification_a15/reader.py','adapter/tests/test_qualification_a15_harness.py']
assert all(not (R/p).exists() for p in source_files),'proposed source path occupied'
missing=[
{'REQUIREMENT_ID':'M69-SUPERVISOR','SOURCE_FILES':[source_files[2]],'EXPECTED_BEHAVIOR':'Authenticate scoped grants/profile/input pins; launch two fresh workers from same checkpoint, independently wait for success, reverify handoff/publication, launch eight fresh readers; stop on first failure; record authoritative exit evidence','DEPENDENCIES':['M69-CONTRACTS','M69-WORKER','M69-READER','M69-ENVIRONMENT'],'TEST_REQUIREMENTS':['fake own-child lifecycle','reader forbidden before supervisor wait','nonzero/timeout/missing handoff fail closed','variant namespace separation']},
{'REQUIREMENT_ID':'M69-WORKER','SOURCE_FILES':[source_files[3]],'EXPECTED_BEHAVIOR':'Restore exact checkpoint; verify full initial state; record_result once with sealed SourceInvalidation; compare complete DTO/query/protection/event/byte outputs; save updated bundle immutably; verify manifests; publish handoff without claiming exit','DEPENDENCIES':['M69-CONTRACTS','M69-COMPARISON'],'TEST_REQUIREMENTS':['synthetic backend trace order','wrong parent/source rejects before backend call','zero real A15 checkpoint access in implementation tests']},
{'REQUIREMENT_ID':'M69-READER','SOURCE_FILES':[source_files[4]],'EXPECTED_BEHAVIOR':'Fresh process, verified supervisor exit evidence; restore exact row bundle, compare complete outputs and bytes including resume reason order; independent reader evidence; no save/application','DEPENDENCIES':['M69-CONTRACTS','M69-COMPARISON'],'TEST_REQUIREMENTS':['fresh interpreter cache separation with fake backend','wrong event/policy/protected field fail closed','cannot launch from handoff alone']},
{'REQUIREMENT_ID':'M69-CONTRACTS','SOURCE_FILES':[source_files[1]],'EXPECTED_BEHAVIOR':'Typed exact subject/variant/profile/invocation/handoff manifests, authority gates, input/source identities, allowlists, retries default none; no wildcard paths or mode','DEPENDENCIES':['M69-IMPLEMENTATION-AUTHORITY'],'TEST_REQUIREMENTS':['wrong identities and grants','symlink/output conflicts','no automatic retry','approval-content identity noncircular']},
{'REQUIREMENT_ID':'M69-COMPARISON','SOURCE_FILES':[source_files[1],source_files[3],source_files[4]],'EXPECTED_BEHAVIOR':'Complete Package61 DTO + native query + canonical byte comparisons; exact event order, proof validation/usability/ANY, FINISH and all resume fields; missing fields fail','DEPENDENCIES':['M69-CONTRACTS'],'TEST_REQUIREMENTS':['independent synthetic expected values','drop each comparison domain fails','false resume with wrong/order-changed reasons fails']},
{'REQUIREMENT_ID':'M69-ENVIRONMENT','SOURCE_FILES':[],'EXPECTED_BEHAVIOR':'Bind qualified executable/dependency hashes and actual actor/host/security launcher permissions, deny network, exact RO inputs/RW isolated outputs, bounded process/resource/audit policy; execution-entry recheck','DEPENDENCIES':['M69-IMPLEMENTATION-QUALIFICATION'],'TEST_REQUIREMENTS':['static profile missing field denial','later authorized synthetic sandbox verification; no real variants']},
{'REQUIREMENT_ID':'M69-IMPLEMENTATION-AUTHORITY','SOURCE_FILES':source_files,'EXPECTED_BEHAVIOR':'Explicit isolated qualification-adapter construction/test approval plus actual repo and synthetic-test resource permissions; no normative-authority substitution','DEPENDENCIES':[],'TEST_REQUIREMENTS':['grant exact file/fixture/operation exclusions']}
]
for row in missing:row['AUTHORITY_REQUIRED']='Separate bounded implementation/test approval; none issued or inferred here'
write('missing-implementation-requirements.json',missing)
plan={'IMPLEMENTATION_PHASES':['Explicit exact implementation/test grant and resource confirmation','Create only six allowlisted new adapter/test source files with unchanged native runtime','Synthetic unit/protocol tests with fake backend; no real checkpoint/variant loaded','Isolated subprocess tests with fake backend; independent exit/reader order/failure audit','Static transitive dependency and source identity seal; read-only Package61 comparison-shape review','Seal executable/argv/environment/permission profile under applicable authority','Only then prepare separate A15 execution/capture decision'],'PERMITTED_FUTURE_TEST_COMMANDS':['python3 -m unittest adapter.tests.test_qualification_a15_harness'],'SYNTHETIC_TEST_FIXTURE_BOUNDARY':'TemporaryDirectory under /tmp/kge-a15-harness-test-* only; dedicated invented SYNTHETIC-HARNESS-TEST identity namespace; no retained checkpoint, raw variant source, native runtime call or real oracle data in effecting tests','NATIVE_BACKEND_DURING_IMPLEMENTATION_TESTS':'Injected fake only; deny imports/calls to adapter.planner execution/persistence entrypoints; assert denylist access and zero native effects','ENTRYPOINT_INTEGRATION_EVIDENCE':'Static source/signature compatibility plus future separately authorized native A15 run; synthetic tests do not establish A15 acceptance','TESTS_RUN_THIS_PACKAGE':0,'RETRY_LIMIT':'No automatic retry. Package61 transient retries require a separately explicit bounded grant and fresh immutable start; no invented limit','INDEPENDENT_EXPECTATIONS':'Manually authored synthetic protocol traces and full synthetic fields, not actual test outputs','QUALIFICATION_ACCEPTANCE':['supervisor owns wait evidence and worker cannot self-certify exit','strict same-start/distinct-output isolation','all failure controls fail closed','complete output comparison on every exposed field','reader runs only after successful own-child exit and publication verification','exact resource and authority entry gates','no real A15 effects or previous-artifact writes'],'DEPENDENCY_ORDER':['M69-IMPLEMENTATION-AUTHORITY','M69-CONTRACTS','M69-COMPARISON','M69-WORKER','M69-READER','M69-SUPERVISOR','M69-IMPLEMENTATION-QUALIFICATION','M69-ENVIRONMENT','separate A15 execution/capture authorization']}
write('implementation-qualification-test-plan.json',plan)
subject={'SCHEMA_ID':'A15-BOUNDED-IMPLEMENTATION-TEST-SUBJECT-1','PURPOSE':'New isolated qualification-only supervisor/worker/reader adapter; preserve native/V3 code and frozen artifacts','STATUS':'PROPOSED_UNISSUED','PERMITTED_SOURCE_FILES':source_files,'SOURCE_FILE_STATUS':'All six NEW; exact content identities unavailable until construction/qualification','PERMITTED_TESTS':plan['PERMITTED_FUTURE_TEST_COMMANDS'],'TEST_FIXTURE_BOUNDARY':plan['SYNTHETIC_TEST_FIXTURE_BOUNDARY'],'TEST_BACKEND':plan['NATIVE_BACKEND_DURING_IMPLEMENTATION_TESTS'],'TEST_EVIDENCE_OUTPUT':'docs/plans/qualification/A15_HARNESS_IMPLEMENTATION_QUALIFICATION_1/ only; absent, not created','RESOURCE_BOUNDARY':{'INPUTS':'Allowlisted new sources, immutable static contract pins, stdlib and interpreter','WRITES':'Only six new source files, future test evidence namespace and private synthetic scratch','NETWORK':'DENY; no sockets or external systems','PROCESSES':'Synthetic isolated test workers/readers only; bounded lifecycle/fault injection in test namespace','RESOURCE_LIMITS':'Must be bounded by actual future test permission/profile before issuance; no unlimited process creation'},'PRESERVED_SUBJECT':sub['TECHNICAL_PREPARATION_IDENTITY'],'CONTRACT_PINS':[pin(P61/x) for x in ['static-harness-contract.json','writer-handoff-cold-reader-contracts.json','failure-retry-matrix.json','resume-comparison-schema.json']],'REQUIRED_APPROVAL':'Explicit project-owner bounded construction/testing approval within actual source/test resource control. Charter qualification governance and Package68 normative grant alone do not establish this implementation permission; do not expand to general engineering governance. Confirm actor/resource rights and concrete process limits before issuance.','EXCLUDED':['actual A15 variants or their native restore/apply/record/save/replay','native runtime or selected V3 modification','new baseline or fixture pins','frozen or historical evidence rewrite','E1','A14 rerun','production/external/government permissions','execution/capture grants','unbounded retries'],'ISSUED_GRANT':None}
write('proposed-implementation-test-authority-subject.json',{'CONTENT':subject,'CONTENT_IDENTITY':{'kind':'CONTENT_IDENTITY','namespace':'qualification-A15-implementation-test-subject-v1','sha256':canon(subject)},'APPROVAL_EVIDENCE':None,'ISSUANCE_READY':False,'UNBOUND_PREREQUISITES':['explicit applicable implementation/test owner approval','actual future actor/test launcher permission and fixed resource limits']})
write('implementation-authority-assessment.json',{'APPLICABLE_IMPLEMENTATION_TEST_GRANTS_FOUND':0,'AUTHORITY_RECORDS_REVIEWED_PIN':pin(Q/'E2_P05_D01_A15_AUTHORITY_ROOT_RECONCILIATION_63'/'authority-root-inventory.json') if (Q/'E2_P05_D01_A15_AUTHORITY_ROOT_RECONCILIATION_63'/'authority-root-inventory.json').exists() else pin(Q/'E2_P05_D01_A15_AUTHORITY_ROOT_RECONCILIATION_63'/'evidence-index.json'),'CURRENT_AUTHORITY_EVIDENCE':pin(Q/'E2_P05_D01_A15_NORMATIVE_ADOPTION_ISSUANCE_68'/'effective-normative-mandate-reference.json'),'NORMATIVE_AUTHORITY_INCLUDES_IMPLEMENTATION':False,'A14_AUTHORITY_REUSED':False,'CHARTER_SCOPE':'Qualification governance; excludes general engineering and does not grant OS rights or automatic code/test execution','PROPOSED_SUBJECT_PIN':pin(D/'proposed-implementation-test-authority-subject.json'),'IMPLEMENTATION_TEST_AUTHORITY_READY':False,'DECISION_OPTIONS':[],'REASON':'No actual construction/test approval or sealed test-launcher/resource limit profile. Content preparation is not a grant; no selectable incomplete approval instrument.'})
future={'PROFILE_STATUS':'UNSEALED_SPECIFICATION','ENVIRONMENT_ID':None,'EXECUTABLE_IDENTITY':None,'HOST_IDENTITY':None,'INTERPRETER_CANDIDATE':obs['PYTHON_RUNTIME'],'DEPENDENCY_LOCK_IDENTITY':None,'WORKING_DIRECTORY':str(R),'PROPOSED_INVOCATIONS':{'SUPERVISOR':['/usr/bin/python3','-m','adapter.qualification_a15.supervisor','--sealed-manifest','UNBOUND'],'WORKER':['/usr/bin/python3','-m','adapter.qualification_a15.worker','--variant-manifest','EXACT_VARIANT_ONLY'],'READER':['/usr/bin/python3','-m','adapter.qualification_a15.reader','--variant-manifest','EXACT_VARIANT_ONLY','--exit-evidence','EXACT_SUPERVISOR_RECORD']},'INVOCATIONS_SEALED':False,'ENVIRONMENT_ALLOWLIST':{'PATH':'/usr/bin:/bin','PYTHONPATH':str(R),'PYTHONDONTWRITEBYTECODE':'1','LC_ALL':'C.UTF-8','PYTHONHASHSEED':'writer 0; reader 0,1,7,101'},'ENVIRONMENT_INHERITANCE':'Deny all unlisted variables, inherited objects/fds/caches; exact launcher environment seal required','INPUT_ALLOWLIST_SOURCE':pin(Q/'E2_P05_D01_A15_BOUNDED_AUTHORITY_DECISION_PREPARATION_67'/'qualification-environment-permission-inventory.json'),'INPUTS':'Exact checkpoint/19 ledgers/55 pins, Package61 oracles/contracts, effective charter and normative/exec/capture grants, sealed executable/dependencies only','OUTPUT_ALLOWLIST':load(P61/'save-target-contracts.json'),'OUTPUTS_CREATED':False,'READ_ONLY_INPUT_ENFORCEMENT':None,'NETWORK_POLICY':'DENY; actual enforcing launcher/namespace/policy identity UNBOUND','PROCESS_ISOLATION':'One supervisor, two fresh writers, eight fresh readers, four per variant; exact process contract; no shared mutated state','RESOURCE_LIMITS':{'max_native_workers':1,'total_native_workers':2,'total_cold_readers':8,'reader_seeds':[0,1,7,101],'wall_time_seconds':None,'memory_bytes':None,'max_child_processes':None,'max_output_bytes':None,'NO_AUTOMATIC_RETRY':True},'AUDIT_REQUIREMENTS':'Exact source/profile/subject/checkpoint/variant IDs; authority checks; supervisor-observed PID/wait/exit/time; publication/handoff hashes; eight independent complete comparisons; failures retained','FRESHNESS_VERIFICATION':'Rehash executable/interpreter/dependency tree, check grants not revoked, current actor/access/security confinement, exact immutable inputs and empty nonsymlink output rows at every launch','ACTUAL_SECURITY_LAUNCHER':None,'RESOURCE_PERMISSION_EVIDENCE':None,'ASSURANCE':'Native file fsync and immutable publication only; no directory/general crash durability claim'}
write('future-execution-profile-specification.json',future)
failures=load(P61/'failure-retry-matrix.json')
write('failure-retry-capability-mapping.json',[dict(x,IMPLEMENTATION_STATUS='PARTIALLY_IMPLEMENTED',EXISTING_BEHAVIOR='Native identity/save guards and generic A14 nonzero wait rejection exist; exact A15 supervisor/comparison/stop routing unqualified',REQUIRED_COMPONENTS=['M69-CONTRACTS','M69-SUPERVISOR','M69-WORKER','M69-READER'],NO_RETRY_EXPANSION=True) for x in failures])
# Read lessons rather than changing an append-only register for redundant observations.
register=load(R/'docs/plans/PLANNER_REASONING_LESSONS_REGISTER_1.json');lessons=[e['LESSON'] for e in register['EVENTS'] if 'LESSON' in e]
assert {x['LESSON_ID'] for x in lessons}=={'LL-'+str(i).zfill(2) for i in range(1,11)}
reviews=[]
for x in lessons:
 lid=x['LESSON_ID'];classification='SUPPORTING_EVIDENCE' if lid in ['LL-03','LL-05','LL-06','LL-10'] else 'NO_NEW_EVIDENCE'
 reviews.append({'LESSON_ID':lid,'CLASSIFICATION':classification,'EVIDENCE':'Package61 static process/oracle specification differs from available A14/selectedV3 implementation and future environment/grants' if classification=='SUPPORTING_EVIDENCE' else 'No distinct Package69 observation tests this causal hypothesis','COUNTEREVIDENCE':'The earlier package explicitly states STATIC_HARNESS_READY is specification readiness; this is an acknowledged engineering scope boundary, not demonstrated model failure','CAUSAL_HYPOTHESIS_PROVEN':False,'NEW_CAPABILITY_REQUIRED':'No new runtime feature established; existing completeness and epistemic-state lessons cover this distinction'})
write('reasoning-lessons-evidence-update.json',{'REGISTER_PIN':pin(R/'docs/plans/PLANNER_REASONING_LESSONS_REGISTER_1.json'),'MD_PIN':pin(R/'docs/plans/PLANNER_REASONING_LESSONS_REGISTER_1.md'),'LESSONS_REVIEWED':10,'REVIEWS':reviews,'NEW_LESSONS':0,'REGISTER_MODIFIED':False})
gates={'CHARTER_EFFECTIVE':'YES','A15_NORMATIVE_MANDATE_EFFECTIVE':'YES','IMPLEMENTATION_INVENTORY_COMPLETE':'YES','SUPERVISOR_WORKER_QUALIFIED':'NO','EXECUTABLE_IDENTITY_SEALED':'NO','ENVIRONMENT_PROFILE_SEALED':'NO','RESOURCE_PERMISSIONS_VERIFIED':'NO (current read/DAC observations only; future profile unsealed)','IMPLEMENTATION_TEST_AUTHORITY_READY':'NO','A15_EXECUTION_DECISION_READY':'NO','A15_CAPTURE_DECISION_READY':'NO'}
write('readiness-gates.json',gates)
print(json.dumps({'RESULT':'STATIC_INVENTORY_CREATED','COMPONENTS':len(inv),'CAPABILITIES':len(capabilities),'SEARCH_MATCHES':len(scan),'GATES':gates},sort_keys=True))
