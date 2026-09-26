from pathlib import Path
import json,hashlib,os,urllib.request,subprocess,datetime
from adapter.context_binding import CommittedContext
from adapter.authority_profile import programmer_authorization
from adapter.responses_orchestrator import tool_definitions
root=Path('/home/gvasend/app/kge-forge'); out=root/'docs/experiments/E1/pre_dispatch/pd05_closure_evidence'
b=CommittedContext(root/'docs/experiments/E1/pre_dispatch/CONTEXT_MANIFEST.json','5871bdce4f5b6539c84f69f4f2b2f94ee31be5cd')
sha=lambda data:hashlib.sha256(data).hexdigest()
a=programmer_authorization(b,'auth-pd05-r2-inactive-evidence',2,'session-pd05-r2-inactive-evidence','turn-pd05-r2-inactive-evidence')
assert a.state=='INACTIVE' and not a.exec_bins
argv=['/usr/bin/python3','-B','-m','unittest','discover','-s','tests/context','-p','test_*.py','-v']
runtime=[{'path':p,'resolved':str(Path(p).resolve()),'sha256':sha(Path(p).read_bytes())} for p in ['/usr/bin/python3','/usr/bin/git','/usr/bin/bwrap']]
# Record configuration facts without reading any environment variable value or credential.
observations={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'proxy_variable_names_present':sorted(k for k in os.environ if k.lower() in ('http_proxy','https_proxy','all_proxy','no_proxy')),
 'urllib_global_opener_is_unset':urllib.request._opener is None,
 'runtime_identities':runtime,
 'root_preconditions':{str(root/p):{'exists':(root/p).exists(),'is_directory':(root/p).is_dir()} for p in ['src/kge_forge','src/kge_forge/context','tests/context','docs/implementation']},
 'context_sha256':b.digest,'capture_commit':b.capture_commit,'sources_verified':len(b.sources),'mandatory_closure_count':len(b.closure)}
(out/'configuration_observations.json').write_text(json.dumps(observations,indent=2)+'\n')
base_ref={'baseline':'411cb5a9fabc71e482a414ed58387de0ff557e93','preparation':b.capture_commit,
 'service':'c9458a8698c90bd43137025fa7e1dc3c34c4e37a','adapter_base':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
 'architect_supplement':'../PD05_CLOSURE_AUTHORITY_2026-09-16.md',
 'work_package':'../E1-WP-001.md','manifest':'../CONTEXT_MANIFEST.json'}
communication={'endpoint':'https://api.openai.com/v1/responses','model':'gpt-5','store':False,
 'parallel_tool_calls':False,'continuation':'caller-owned; no previous_response_id; include reasoning.encrypted_content',
 'credential_reference':'controller environment variable OPENAI_API_KEY; value never in profile, audit or payload environment',
 'transport':{'implementation':'unchanged urllib.request.Request/urlopen with default HTTPS certificate verification',
   'proxy_policy':'DIRECT_ONLY; controller launch must reject presence of http_proxy, https_proxy, all_proxy or no_proxy (case-insensitive); no proxy secrets or values recorded',
   'custom_opener':'prohibited; require urllib.request._opener is None at launch',
   'redirect_policy':'No alternate information destination is authorized. Current urllib default redirect handling is not a destination-confinement proof; controller configuration is trusted, and runtime redirect confinement is unresolved.',
   'endpoint_selection':'controller only; exact endpoint above; no model override or alternate endpoint grant'},
 'authorized_information_categories':[
   'E1-WP-001 task text and committed mandatory governing sources/context metadata, including repository identities and declared unresolved blockers',
   'Ordinary files, directory names and bounded literal search results under the two designated repository roots after .git/.codex/.agents exclusions; scope of G1/C, not arbitrary host directories',
   'In-scope implementation source, test fixtures and implementation evidence produced through governed writes/patches',
   'Bounded governed action results, execution stdout/stderr, status, hashes, provenance, denied-request explanations, expansion requests and finish summaries',
   'Prior model outputs and encrypted reasoning continuation items needed for the qualified stateless loop'],
 'excluded_information_categories':['credentials and secret values','all excluded hidden-directory contents','controller/supervisor private audit and ownership contents','unrelated host files or connector data'],
 'unresolved_content_condition':'Read policy is path-based, not a secret detector. Controller must obtain scoped content-suitability assurance for allowed ordinary files/results; no new redaction mechanism or whole-repository secret scan is claimed.',
 'authority':'Architect G3 authorizes approved Responses destination, controller model selection, store=false and reference-only credential; ordinary repository categories derive from C/W as narrowed by G1.',
 'enforcement_status':'PROPOSED_CONTROLLER_CONFIGURATION; no API call, transport change, launcher integration or active E1 run performed'}
execution={'status':'PROPOSED_INACTIVE_NOT_RUNNABLE_UNTIL_REMAINING_GAPS_RESOLVED',
 'exact_top_level_argv_allowlist':[argv],
 'executable_identities':runtime,
 'top_level_executables':['/usr/bin/python3'],
 'runtime_support_executables':{'/usr/bin/git':'read-only committed fixture inspection via argument arrays inside payload; no direct model Git function or real-repository mount',
 '/usr/bin/bwrap':'trusted supervisor-only launcher, not a model executable'},
 'source_cwd':str(root),'payload_cwd':'/scope',
 'authorized_source_inputs':['src/kge_forge/__init__.py','src/kge_forge/context','tests/context'],
 'input_rules':'Only exact listed file/directory selections; every copied file must pass read policy and match designated captured blob or successful governed write/patch digest. No whole-root selection, links, hidden dirs, controller audit, credentials or unrelated files.',
 'payload_environment':{'PATH':'/usr/bin:/bin','LANG':'C.UTF-8','PYTHONPATH':'/scope/src'},
 'inherited_environment':'none; no controller credentials/proxy/HOME/SUDO variables; PWD may be set by runtime to /scope',
 'network':False,'shell':False,
 'scratch_rule':'Test-created temporary fixtures only inside private /scope workspace; no source promotion except a separate authorized write/patch. No real-repository Git mutation, installs or network.',
 'command_derivation':'W standard-library tests and Python 3.8 compatibility; unittest discovery is a proposed minimum single test command; literal test_*.py is data, not shell expansion. PYTHONPATH implements W src layout. Tests must exercise module entry point and acceptance criteria; no product test is written here.',
 'current_effective_execution_grant':{'exec_bins':[],'exec_argv_allowlist':[]},
 'qualification_mapping':[
   {'authority':'Python argv via admitted snapshot, shell=false/network=false','evidence':'prior bound.jsonl + recovery/production qualifications','result':'MECHANISM_COVERED; this exact test command not executed'},
   {'authority':'Exact source cwd and exact input selection constraint','evidence':'current issue_exec_permit accepts any read-root cwd and model-selected inputs','result':'GAP: proposed narrowing not represented/enforced by current WorkAuthorization'},
   {'authority':'PYTHONPATH=/scope/src fixed environment','evidence':'exec_barrier supplies only PATH/LANG','result':'GAP: requires separately authorized launcher environment change and qualification; not implemented'},
   {'authority':'Read-only synthetic committed Git fixtures for AC01-07','evidence':'scratch capture uses controller Git; Python payload can spawn runtime tools but no payload Git inspection fixture qualified here','result':'GAP: controller-provisioned committed fixture input/provenance contract absent; no real .git access granted'},
   {'authority':'Real-context AC08 source/revision inspection','evidence':'snapshot handles a single source root; hides .git; real context contains two roots and committed blob identities','result':'GAP: exact real-context presentation/mapping and committed-object retrieval route unresolved; no cross-root or hidden read exception granted'},
   {'authority':'Runtime executable content identity','evidence':'configuration_observations.json hashes current binaries; existing allowlist checks argv, not binary digest','result':'OBSERVED_ONLY; pre-release runtime identity binding remains required'}],
 'no_direct_cli_command':'No additional top-level kge_forge.context argv granted: final option spelling is not yet implemented. Acceptance can be tested by the exact test runner; any later standalone command needs a separately specified revision.'}
profile={
 'schema':'E1-PROPOSED-PROFILE-2','proposal_id':'E1-WP-001-PROPOSED-R2','state':'INACTIVE',
 'architect_status':{'PD-05':'PENDING','PD-06':'RELEASE_NOT_AUTHORIZED','A2':'PARTIAL','E1-B01':'BLOCKED','E1-WP-001':'INELIGIBLE_UNDISPATCHED'},
 'source_refs':base_ref,'work_id':'E1-WP-001','baseline_id':'E1-ARCH-1','context_sha256':b.digest,
 'identity':{'authorization_revision':2,'authorization_id_rule':'controller allocates auth-e1-wp-001-r2-<uuid4>; immutable binding to this exact profile digest and context capture',
  'session_id_rule':'controller allocates session-e1-<uuid4> only at separately authorized launch; reuse exact identity solely for audited restart',
  'turn_id_rule':'controller allocates turn-e1-<uuid4>; every ActionRequest bound to session/turn/authorization/revision; model cannot supply replacement identity',
  'action_id_rule':'unique model call id checked against durable request digest; changed replay denied',
  'scope_id_rule':'controller allocates scope-<uuid4> per exec; caller scope ids denied',
  'allocated_production_ids':None},
 'read_roots':list(a.read_roots),'read_deny_roots':list(a.read_deny_roots),
 'write_file_roots':[p for p in a.write_roots if p not in a.write_directory_roots],
 'write_directory_roots':list(a.write_directory_roots),'write_deny_roots':list(a.write_deny_roots),
 'captured_source_write_denies':sorted(str(p) for p in b.protected_paths),
 'write_semantics':'exact file targets; directory descendants only; preflight all missing parents; creation strictly below an existing explicit directory grant; grant-root or leaf-ancestor provisioning not delegated',
 'host_setup_preconditions':observations['root_preconditions'],
 'ownership':{'ledger':'/tmp/kge-forge-e1-invocations.jsonl',
  'rule':'Every E1 controller/turn/revision uses this same canonical ledger and qualified locking/reservation/release mechanism. No per-session alternate, empty ledger, deletion, truncation or reset on restart. Active or uncertain reservation blocks replacement. Release only after durable terminal ActionResult and supervisor-owner/closed/zero-member evidence.',
  'restart_rule':'same immutable authorization/schema and audit; old-schema audits deny reconstruction; no migration or optimistic adoption',
  'remaining_check':'fresh release-time common-ledger identity, ownership and no-active/unaccounted checks; no E1 execution performed here'},
 'audit':{'path_rule':'/tmp/kge-forge-e1-evidence/<authorization_id>/<session_id>/<turn_id>/controller.jsonl',
  'directory_mode':'0700 controller-owned','file_mode':'0600','outside_all_agent_grants':True,
  'restart':'reuse exact audit for identity; append/fsync; no truncate',
  'status':'proposed placement; no production audit created'},
 'snapshot':{'workspace_rule':'controller tempfile.mkdtemp(prefix=a2-exec-,dir=/tmp), private 0700; payload bind /scope',
  'manifest_rule':'<controller audit parent>/snapshots/<scope_id>.json; controller-only 0600',
  'source_promotion':'none; observe changed/new/deleted workspace files; only explicit governed write/patch changes authoritative source',
  'scratch':'payload fixtures confined to /scope; no extra host temp mount'},
 'model_communication':communication,'execution':execution,
 'environment_policy':{'payload':'execution.payload_environment (PYTHONPATH is proposed, not implemented)',
  'controller':'trusted controller; credential by reference only; direct transport preconditions; fixed context Git env PATH/GIT_CONFIG_NOSYSTEM/GIT_CONFIG_GLOBAL/GIT_OPTIONAL_LOCKS as implemented',
  'source':'W src entry-point; G3/G5/G6; existing context_binding.py/exec_barrier.py'},
 'external_destination_policy':{'allowed':'exact model_communication.endpoint for controller reasoning only','task_network':False,'MCP_plugins_connectors':False,'additional_agents':False,'alternate_endpoints':False},
 'tool_definitions':tool_definitions(),
 'unresolved_selections':[
  'Controller-owned creation of absent E1 parent/grant directories is not assigned/authorized as E1 source-write authority; readiness precondition unmet.',
  'Exact two-repository real-context presentation/committed-source access for AC08; no hidden-file or authoritative Git mount exception selected.',
  'Controller-provided synthetic committed Git fixture identities and provenance/input selection for acceptance tests.',
  'Production runtime IDs and artifact release commit allocated only after separate authorization; profile digest is bound when allocated.',
  'Content-suitability assurance for allowed ordinary files and operational binding of destination/proxy policy; current client does not police redirects to other destinations.'
 ],
 'all_proposed_runnable_authorities_covered':False}
profile['limits']={'read_bytes': [1, 65536], 'list_entries': [1, 1000], 'search_matches': [1, 100], 'search_eligible_files': 2000, 'search_file_bytes': 1000000, 'search_line_output_chars': 500, 'write_or_patch_content_bytes': 1000000, 'patch_change_count': 1, 'exec_argv_count': 64, 'exec_argv_total_bytes': 8192, 'snapshot_requested_inputs': 100, 'snapshot_files': 2000, 'snapshot_total_bytes': 67108864, 'snapshot_single_file_bytes': 8388608}
profile['deny_roots']=[]
# All substantive top-level fields have explicit provenance classification; nested
# execution comparisons explain the narrower new/unsupported selections.
attrs={}
for k in profile:
 if k in ('limits','deny_roots'):
  cls='previously human/Architect-approved'; src='Existing qualified governed_host.py/execution_snapshot.py limits and empty generic denies; typed denies and captured-source protections apply'
 elif k in ('schema','proposal_id','source_refs','tool_definitions'):
  cls='newly Architect-selected'; src='G6 permits preparation of this proposed record; schema/id are documentary; registry is existing adapter source'
 elif k in ('work_id','baseline_id','context_sha256','read_roots','write_file_roots','write_directory_roots','write_deny_roots','captured_source_write_denies'):
  cls='baseline-derived'; src='captured C.scope/C.sources and W allowed paths; directory/file distinction clarified by current Architect G2'
 elif k in ('state','architect_status','read_deny_roots','write_semantics','model_communication','external_destination_policy'):
  cls='newly Architect-selected'; src='current Architect G1/G2/G3 and explicit no-release instruction; concrete model choice retains qualified gpt-5 under delegated controller selection'
 elif k in ('snapshot',):
  cls='previously human/Architect-approved'; src='A2_CONTROLLER_EXECUTION_WORKSPACE and A2_LIVE_RECOVERY qualification; existing mechanism retained'
 elif k in ('identity','ownership','audit','environment_policy','execution'):
  cls='newly Architect-selected'; src='current G5/G6 mandate to prepare a proposed launch profile preserving qualified identity/ownership mechanism; concrete naming/paths are proposed controller selections, not final release decisions'
 else:
  cls='unresolved'; src='observed preconditions or missing evidence/selection; no implied grant'
 attrs[k]={'classification':cls,'authority_source':src,'adoption_status':'PROPOSED_NOT_RELEASED'}
profile['field_attribution']=attrs
(out/'PROPOSED_E1_PROFILE.json').write_text(json.dumps(profile,indent=2)+'\n')
(out/'MODEL_COMMUNICATION.json').write_text(json.dumps(communication,indent=2)+'\n')
print('Prepared inactive proposed profile; model transport unchanged; exact execution gaps recorded.')
