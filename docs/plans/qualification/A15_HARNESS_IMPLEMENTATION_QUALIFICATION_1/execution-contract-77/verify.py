"""Independent static source-contract verifier, no adapter/probe imports or calls."""
import ast,copy,hashlib,json,pathlib,sys
D=pathlib.Path(__file__).resolve().parent;E=D.parent;R=D.parents[4];Q=R/'docs/plans/qualification'
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def cb(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def verify(overrides=None):
 overrides=overrides or {}
 def read(n):return copy.deepcopy(overrides[n]) if n in overrides else load(D/n)
 for a in read('input-authentication.json')['INDICES']:
  p=R/a['PIN']['PATH'];assert sha(p)==a['PIN']['RAW_SHA256'];idx=load(p);assert all(sha(R/f)==h for f,h in idx['FILES'].items())
 positive=read('positive-oracle-authentication.json');assert positive['VERIFIED']=='2/2' and positive['READER_COMPARISONS']==8 and not positive['ADAPTER_USED_TO_REGENERATE'] and not positive['ORACLES_ARE_ACTUAL_RESULTS']
 real_scope=load(Q/'E2_P05_D01_A15_IMPLEMENTATION_TEST_AUTHORITY_70/implementation-test-authority-subject.json')
 for row in positive['ORACLES']:
  for k in ['FIXTURE_PIN','EXPECTED_PIN']:assert sha(R/row[k]['PATH'])==row[k]['RAW_SHA256'] and 'direct-host-76/' in row[k]['PATH']
  oracle=load(R/row['EXPECTED_PIN']['PATH']);assert oracle['EXPECTED_OUTPUT']['PUBLISHED_OUTPUT']['identity']==row['PUBLISHED_OUTPUT_ID']
 faults=read('fault-lifecycle-oracle.json');expected=['F77-LAUNCH-FAILURE','F77-WORKER-TIMEOUT','F77-WORKER-NONZERO-EXIT','F77-INVALID-HANDOFF','F77-PUBLICATION-CONFLICT','F77-READER-MISMATCH','F77-RESOURCE-EXHAUSTION','F77-INVALID-INPUT','F77-PROTECTED-PATH','F77-UNAUTHORIZED-RETRY']
 assert [x['FAULT_ID'] for x in faults['FAULTS']]==expected and faults['FAULT_ORACLE_COMPLETE'] is False and faults['ADAPTER_OUTPUT_USED_AS_ORACLE'] is False and faults['FAILED_NATIVE_RESULT_FIELDS_INVENTED'] is False
 required={'FAULT_ID','SYNTHETIC_INPUT_IDENTITY','FAULT_INJECTION_POINT','EXPECTED_SUPERVISOR_RESULT','EXPECTED_WORKER_RESULT_IF_ANY','EXPECTED_EXIT_OBSERVATION','EXPECTED_PUBLICATION_STATE','EXPECTED_HANDOFF_STATE','EXPECTED_READER_STATE','EXPECTED_AUDIT_EVIDENCE','EXPECTED_RETRY_COUNT','EXPECTED_FIRST_COUNTEREXAMPLE','DERIVATION_RULE','INDEPENDENT_EVIDENCE','COMPLETENESS','OBSERVED_RESULT'}
 for x in faults['FAULTS']:
  assert set(x)==required and x['OBSERVED_RESULT'] is False
  assert x['SYNTHETIC_INPUT_IDENTITY']==positive['ORACLES'][0]['FIXTURE_ID']
  assert x['EXPECTED_SUPERVISOR_RESULT']['PROTOCOL_RECORD'] is None
  assert x['EXPECTED_RETRY_COUNT']=={'CLASSIFICATION':'EXACT','VALUE':0}
  assert x['EXPECTED_AUDIT_EVIDENCE']['CLASSIFICATION']=='UNDETERMINED' and x['EXPECTED_FIRST_COUNTEREXAMPLE']['CLASSIFICATION']=='UNDETERMINED'
 sources=read('executable-source-manifest.json');assert len(sources['FILES'])==6 and not sources['EXECUTABLE_QUALIFIED']
 for x in sources['FILES']:
  assert sha(R/x['SOURCE_PATH'])==x['SOURCE_SHA256'] and not x['EXECUTED']
  t=ast.parse((R/x['SOURCE_PATH']).read_text());assert [n.name for n in ast.walk(t) if isinstance(n,ast.FunctionDef)]==[a['CALLABLE'] for a in x['CALLABLES']]
 invocation=read('proposed-invocation-contract.json');assert not invocation['FULL_EXECUTABLE_INVOCATION_COMPLETE'] and invocation['INTERPRETER_IDENTITY'] is None and invocation['OUTPUT_PATHS'] is None and invocation['FRESH_AUTHORITY_IDENTITY'] is None
 assert invocation['ROLES']['SUPERVISOR']['MAIN_ARGUMENT_COUNT']==2 and invocation['ROLES']['WORKER']['MAIN_ARGUMENT_COUNT']==invocation['ROLES']['READER']['MAIN_ARGUMENT_COUNT']==3
 conf=read('direct-host-confinement-specification.json');assert conf['OBSERVATION_KIND']=='USER_SUPPLIED_NOT_REPRODUCED' and not conf['RECIPE_EXECUTED'] and not conf['ACTUAL_HOST_CONTROLS_VERIFIED']
 allowed=['--unshare-user','--unshare-pid','--unshare-net','--unshare-ipc','--unshare-uts','--die-with-parent','--new-session','--cap-drop','--ro-bind','--bind','--proc','--dev','--dir','--tmpfs','--chdir']
 assert conf['OPTION_ALLOWLIST']==allowed and '--unshare-net' in conf['BWRAP_RECIPE'] and conf['NO_HOST_NETWORK'] and conf['NO_REAL_A15_OR_HISTORY_MOUNTS'] and conf['ONE_OWNED_OUTPUT_ROW_WRITABLE']
 assert all(not arg.startswith('--') or arg in allowed for arg in conf['BWRAP_RECIPE'])
 resources=read('resource-enforcement-procedure.json');approved=real_scope['CONTENT']['CONTRACTS']['environment-resource-permission-contract.json']['RESOURCE_LIMITS'];assert resources['RESOURCE_LIMITS']==approved and len(resources['CONTROLS'])==10 and not resources['HOST_RESOURCE_ENFORCEMENT_READY'] and not resources['CGROUP_WRITES_ALLOWED']
 assert all(x['CURRENT_STATUS']=='NOT_READY' and x['REQUIRED_LIMIT']==approved[x['CONTROL_ID']] for x in resources['CONTROLS'])
 procedure=read('host-enforcement-verification-procedure.json');assert len(procedure['STEPS'])==14 and not procedure['EXECUTED'] and not procedure['HOST_TEST_IS_ADAPTER_FAKE_CAMPAIGN'] and not procedure['FULL_FOURTEEN_STEP_EXECUTABLE_BINDINGS_COMPLETE']
 host=read('host-capability-test-authorization-subject.json');b=host['CONTENT'];assert host['IDENTITY']['sha256']==hashlib.sha256(cb(b)).hexdigest() and not host['ISSUED'] and host['APPROVAL'] is None
 assert b['STATUS']=='PROPOSED_UNISSUED' and b['HOST_SELECTOR']['NAME']=='ubuntu01' and b['HOST_SELECTOR']['ACTOR_UID']==1000
 assert b['RESOURCE_LIMITS']==approved and b['CURRENT_APPROVAL_EVIDENCE'] is None and b['ISSUED_GRANT_IDENTITY'] is None
 spec=b['PROCEDURE'];assert spec['SELECTED_STEP']=='H77-02_NAMESPACE_METADATA_ONLY'
 assert spec['PROGRAM']==procedure['PROGRAMS']['namespace'] and spec['RESOURCE_BUDGET']=={'MAX_ACTUAL_PROCESS_SLOTS':4,'MAX_PAYLOAD_LAUNCHES':1,'CHILD_WALL':60,'CHILD_CPU':30,'CHILD_AS':1073741824,'CHILD_FSIZE':16777216,'CHILD_FDS':64,'TOTAL_WRITES':1048576,'TOTAL_WALL':600,'RETRIES':0}
 argv=spec['COMMAND_OR_TEST']['ARGV'];assert argv[:3]==['/usr/bin/timeout','--signal=KILL','60s'] and '/usr/bin/prlimit' in argv and '--unshare-net' in argv and argv[-1]==spec['PROGRAM']['SOURCE']
 assert 'adapter' not in spec['PROGRAM']['SOURCE']
 for p in spec['TOOL_BINARY_PINS']:assert sha(pathlib.Path(p['PATH']))==p['RAW_SHA256']
 assert 'adapter/fake-protocol execution' in b['EXCLUSIONS'] and 'native synthetic integration' in b['EXCLUSIONS'] and 'real A15 checkpoint/oracles/invalidation/capture/save/restore/replay' in b['EXCLUSIONS'] and 'host security settings/cgroup modifications/elevated privileges' in b['EXCLUSIONS']
 closure=read('campaign-input-closure.json');assert not closure['FAULT_ORACLE_COMPLETE'] and not closure['EXECUTABLE_INVOCATION_COMPLETE'] and not closure['HOST_ENFORCEMENT_PROCEDURE_COMPLETE'] and not closure['HOST_CONTROLS_VERIFIED'] and not closure['CAMPAIGN_INPUTS_COMPLETE']
 assert closure['NEW_ISSUED_CAMPAIGN_IDENTITY'] is None and closure['NO_RETRY'] and closure['NO_ACTUAL_A15_EXECUTION'] and closure['HOST_TEST_SCOPE_DOES_NOT_RENEW_OLD_CAMPAIGN']
 assert closure['ISSUED_GRANT_IDENTITY']['sha256']=='25395fb3c06be58a8c538c618b9e50b9d118aa415d0843968254d3f8e83dd8fa'
 assert sha(R/closure['STOPPED_JOURNAL_PIN']['PATH'])==closure['STOPPED_JOURNAL_PIN']['RAW_SHA256']
 gates=read('readiness-gates.json');assert gates['POSITIVE_ORACLES_VERIFIED']=='2/2' and gates['FAULT_ORACLE_COMPLETE']==gates['EXECUTABLE_INVOCATION_COMPLETE']==gates['HOST_CONTROLS_VERIFIED']==gates['CAMPAIGN_INPUTS_COMPLETE']==gates['FAKE_CAMPAIGN_DECISION_READY']=='NO'
 assert gates['HOST_CAPABILITY_TEST_DECISION_READY']=='YES for one exact namespace-metadata subset only; not full suite'
 return {'RESULT':'PASS_STATIC_PARTIAL_CONTRACT','POSITIVE_ORACLES_VERIFIED':'2/2','FAULT_ORACLE_COMPLETE':False,'FAULT_ORACLE_HASH':hashlib.sha256(cb(faults)).hexdigest(),'SOURCE_HASHES':sources['SOURCE_HASHES'],'INVOCATION_HASH':hashlib.sha256(cb(invocation)).hexdigest(),'HOST_PROCEDURE_HASH':hashlib.sha256(cb(procedure)).hexdigest(),'HOST_SUBSET_SUBJECT_IDENTITY':host['IDENTITY'],'HOST_CAPABILITY_SUBSET_DECISION_READY':True,'FAKE_CAMPAIGN_DECISION_READY':False,'READINESS':gates,'ACTIVE_HOST_OR_ADAPTER_TESTS':0}
if __name__=='__main__':print(json.dumps(verify(json.load(sys.stdin) if '--candidate' in sys.argv else None),sort_keys=True))
