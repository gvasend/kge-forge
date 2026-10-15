"""Static governance/file/JSON reconstruction; no target, host control, or source import."""
import pathlib,json,hashlib,sys,subprocess,os,copy
O=pathlib.Path(__file__).resolve().parent;B=pathlib.Path('docs/plans/qualification/A15_HARNESS_IMPLEMENTATION_QUALIFICATION_1');P=B/'p86-isolation-capability-124'
def load(p):return json.loads(p.read_text())
def canon(x,ascii=False):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=ascii).encode()
def sha(x):return hashlib.sha256(x).hexdigest()
def need(x,r):
 if not x:raise ValueError(r)
def pointer(p,k):
 x=load(p)
 for part in k.split('/')[1:]:x=x[int(part)] if isinstance(x,list) else x[part]
 return x
def graph_ok(edges):
 on=set();done=set();a={}
 for x,y in edges:a.setdefault(x,[]).append(y)
 def v(x):
  need(x not in on,'cycle')
  if x in done:return
  on.add(x)
  for y in a.get(x,[]):v(y)
  on.remove(x);done.add(x)
 for x in a:v(x)
 return True
manifest=load(O/'authenticated-input-index.json')
for p,h in manifest['PINS'].items():need(sha(pathlib.Path(p).read_bytes())==h,'input pin '+p)
for p,h in load(O/'preservation-before.json')['FILES'].items():need(sha(pathlib.Path(p).read_bytes())==h,'history '+p)
profile=load(P/'exact-candidate-profile.json');need(profile['IDENTITY']==manifest['P124_PROFILE_IDENTITY'] and sha(canon(profile['CONTENT']))==profile['IDENTITY']['sha256']=='2f36be1b7123770d889be302a090cfef16149b270140a9ea901ba992095f46ca','unchanged124profile')
reference=load(O/'preserved-candidate-reference.json');need(reference['EXACT_ARGV']==profile['CONTENT']['ARGV'] and reference['ENVIRONMENT']==profile['CONTENT']['OUTER_EXEC_ENVIRONMENT'],'command/envpreserved')
need(sha(canon(reference['EXACT_ARGV']))==profile['CONTENT']['ARGV_SHA256'],'argvdigest');need(reference['FINDMNT_WITNESS']==load(P/'passive-witness-specification.json'),'witnessnotsubstituted')
roots=load(O/'trust-root-alternatives.json');need([r['ID'] for r in roots['ALTERNATIVES']]==['A_CODEX','B_DIRECT_NONPRIV_SHELL','C_ADMIN_SYSTEMD_CGROUP_V1','D_EXISTING_DISPOSABLE_VM_CONTAINER'] and roots['SELECTED']=='NONE','fouralternatives')
for r in roots['ALTERNATIVES']:
 need(not r['QUALIFIED_SUPPORTED'] and not r['DIRECT_HOST_PERMISSION_INFERRED'],'noqualifiedrootinferred')
 for p in r['EXACT_EVIDENCE_PINS']:need(sha(pathlib.Path(p['PATH']).read_bytes())==p['RAW_SHA256'],'alternativereference')
classification=load(O/'authority-classification-matrix.json');need(classification['COUNT']==len(classification['ROWS'])==34,'authorityrows')
allowed=set(classification['CATEGORY_LEGEND'].values())
for r in classification['ROWS']:
 need(r['AUTHORITY_CATEGORY'] in allowed,'authoritylevel')
 s=r['SOURCE'];need(sha(pathlib.Path(s['SOURCE_PATH']).read_bytes())==s['RAW_SHA256'] and pointer(pathlib.Path(s['SOURCE_PATH']),s['JSON_POINTER'])==s['EXACT_CLAUSE'],'exactclause/pin')
ids={r['CONTROL_ID']:r for r in classification['ROWS']}
need(ids['QUALIFIED_INVOCATION_CONTEXT']['AUTHORITY_CATEGORY']=='A_BINDING_CHARTER_OR_ISSUED_MANDATE','qualifiedcontextbinding')
for x in ['CPU_MEMORY_FD_TASK_WALL','SCRATCH_OCCUPANCY_METHOD','OUTSIDE_OBSERVER_METHOD','MAX_ONE_CAP_ATTEMPT','CRITICAL_RESERVE']:need(ids[x]['AUTHORITY_CATEGORY']=='C_PROSPECTIVE_SUBJECT_POLICY','prospectivechoice notuniversallaw')
need(ids['OLD_GRANT_90']['AUTHORITY_CATEGORY']==ids['OLD_GRANT_94']['AUTHORITY_CATEGORY']=='B_EFFECTIVE_SCOPED_GRANT' and all(ids[x]['CURRENT_STATUS']=='NOT_APPLICABLE_ORIGINAL_SCOPE' for x in ['OLD_GRANT_90','OLD_GRANT_94']),'oldscopeonly')
mandatory=load(O/'mandatory-pre-entry-matrix.json');need(len(mandatory['ROWS'])==mandatory['COUNT']==14 and not mandatory['ALL_CONTROLS_COMPLETE'],'entrymatrix')
for r in mandatory['ROWS']:
 s=r['EXACT_SOURCE'];need(pointer(pathlib.Path(s['SOURCE_PATH']),s['JSON_POINTER'])==s['EXACT_CLAUSE'],'mandatorysource')
need({r['STATUS'] for r in mandatory['ROWS']} <= {'VERIFIED','SPECIFIED_ONLY','FUTURE_ENTRY_PREDICATE','NOT_APPLICABLE_WITH_CLAUSE','BLOCKED'},'statusclasses')
risks=load(O/'risk-register-and-acceptance-classification.json');need(len(risks['RISKS'])==12 and not risks['NUMERIC_EXPECTED_VALUES_INVENTED'] and risks['NO_BLANKET_RISK_WAIVER'],'riskclasses')
need({r['RESIDUAL_RISK_CLASS'] for r in risks['RISKS']}=={'CANNOT_ACCEPT_MISSING_MANDATORY_CONTROL','SCOPED_OWNER_DECISION_REQUIRED','ACCEPTABLE_UNDER_CURRENT_RULES_ONLY_AFTER_EXACT_GRANT_AND_ENTRY','SCOPED_OWNER_DECISION_REQUIRED_FOR_OUTCOME_NOT_WAIVER','SCOPED_OWNER_DECISION_REQUIRED_AFTER_SUPPORTED_TRUST_ROOT','SEPARATE_NORMATIVE_AMENDMENT_REQUIRED','CANNOT_ACCEPT_MISSING_ACTUAL_PERMISSION'},'riskacceptancecategories')
envelope=load(O/'bounded-envelope-recovery.json');need(envelope['EXACT_PROPOSED_LIMITS']==load(P/'resource-observer-contract.json')['RETAINED_PROPOSED_NUMERIC_LIMITS'],'numericlimitsunchanged')
need(envelope['EVIDENCE_MODEL']=={'FIXED_NORMAL':5542,'COMBINED_RAW_CAPTURE':8658872,'NORMAL_TOTAL':8664414,'P124_CRITICAL_MAX':581,'CRITICAL_RESERVED':2336,'PROTECTED_ALLOCATION':8666750},'evidencevalues')
entry=load(O/'entry-execution-mapping.json');need(entry['ORIGINAL36MATRIX']==load(P/'36-requirement-phase-matrix.json') and entry['EARLIEST_PHASE_CHANGES']==[] and len(entry['PHASES'])==5,'36phases/fivedecisionentryoutputphases')
slots=load(O/'publication-slot-preservation.json');need(slots==load(P/'publication-slot-preservation.json') and slots['SELECTED'] is None and not slots['ANY_OPTION_EFFECTIVE'],'slotsunselected')
reg=load(pathlib.Path('docs/plans/PLANNER_REASONING_LESSONS_REGISTER_1.json'));prev='0'*64
for e in reg['EVENTS']:
 need(e['PREVIOUS_EVENT_HASH']==prev and sha(canon({k:v for k,v in e.items() if k!='EVENT_HASH'},True))==e['EVENT_HASH'],'lessonchain');prev=e['EVENT_HASH']
need(len(reg['EVENTS'])==122 and prev==manifest['REGISTER_CHAIN_HEAD']=='885fd0eaceb15847201dfd058217682741fb43c255298713ccbc1e7251eec791','LL11prefix')
need(sum(e.get('LESSON',{}).get('LESSON_ID')=='LL-11' for e in reg['EVENTS'])==1 and not load(O/'lessons-register-review.json')['APPENDED'],'LL11preserved')
cp=subprocess.run([sys.executable,str(B/'p86-publication-amendment-issuance-115/verify_independent.py'),'EFFECTIVE'],capture_output=True,text=True);need(cp.returncode==0,'currentcharter/104/115/A15');json.loads(cp.stdout)
ready=load(O/'owner-decision-readiness-assessment.json');need(ready['DECISION_OPTIONS']==[] and not ready['RISK_ACCEPTANCE_DECISION_READY'] and not ready['CAPABILITY_CHECK_DECISION_READY'] and not ready['CAPABILITY_CHECK_ENTRY_READY'] and not ready['CONSTRUCTION_DECISION_READY'],'no incompleteoption')
graph=load(O/'dependency-graph-and-root-audit.json');graph_ok(graph['EDGES']);need(graph['ACTUAL_SMALLEST_STRONGLY_CONNECTED_COMPONENT']==[],'actualnoSCC')
contracts=['authority-classification-matrix.json','minimum-acceptable-trust-root.json','trust-root-alternatives.json','mandatory-pre-entry-matrix.json','risk-register-and-acceptance-classification.json','bounded-envelope-recovery.json','observer-publication-gap-assessment.json','entry-execution-mapping.json','owner-decision-readiness-assessment.json','exact-gap-dossier.json']
model={'profile_id':profile['IDENTITY'],'argv':reference['EXACT_ARGV'],'root_supported':False,'sudo_verified_from_attestation':False,'scratch_covering_proof':False,'unbounded_scratch_accepted':False,'inherited_fd_exposure':False,'protected_writable':False,'observer_qualified':False,'stderr_unbounded':False,'resource_verified':False,'future_witness_at_entry':False,'auto_retry':0,'mandatory_waived':False,'slotchoice':None,'grant_issued':False,'probe_authority':False,'architecture_effective':False,'root_needs_new_supervisor_forever':False,'cgroup_universal_charter_law':False,'exact_permission_clause_optional':False,'risk_acceptance_equals_verification':False,'own_output_qualifies_guard':False,'construction_enabled':False,'history_preserved':True,'budget_predicts_completion':False,'edges':graph['EDGES']}
def check(m):
 need(m['profile_id']==profile['IDENTITY'] and m['argv']==reference['EXACT_ARGV'],'forgedprofile/command')
 need(not m['root_supported'] and not m['sudo_verified_from_attestation'],'unsupportedrootorpermission')
 need(not m['scratch_covering_proof'] and not m['unbounded_scratch_accepted'] and not m['inherited_fd_exposure'] and not m['protected_writable'],'unknownprotection/resourceproof')
 need(not m['observer_qualified'] and not m['stderr_unbounded'] and not m['resource_verified'],'missingobserver/output/control')
 need(not m['future_witness_at_entry'] and m['auto_retry']==0 and not m['mandatory_waived'],'preentryvsfuture/rules')
 need(m['slotchoice'] is None and not m['grant_issued'] and not m['probe_authority'] and not m['architecture_effective'],'no selection/authorityinference')
 need(not m['root_needs_new_supervisor_forever'] and not m['cgroup_universal_charter_law'] and not m['exact_permission_clause_optional'],'sourceboundtrustroot/ruleclassification')
 need(not m['risk_acceptance_equals_verification'] and not m['own_output_qualifies_guard'] and not m['construction_enabled'] and m['history_preserved'] and not m['budget_predicts_completion'],'riskvsqualifiedfacts')
 graph_ok(m['edges'])
check(model);neg=[]
def reject(name,mut):
 m=copy.deepcopy(model);mut(m)
 try:check(m)
 except ValueError as e:neg.append({'DESIGN':name,'RESULT':'REJECTED','CAUSE':str(e),'MUTATION_SHA256':sha(canon(m))});return
 raise AssertionError('negativeadmitted:'+name)
def changed(k,v):return lambda m:m.__setitem__(k,v)
reject('forged profile pin',lambda m:m['profile_id'].__setitem__('sha256','0'*64))
reject('changed exact candidate argv',lambda m:m['argv'].append('extra-command'))
for name,key in [('unsupportedtrustroot','root_supported'),('ownerattestationassudopermission','sudo_verified_from_attestation'),('scratchcoveringproofinvented','scratch_covering_proof'),('unboundedscratchaccepted','unbounded_scratch_accepted'),('inheriteddescriptor exposure','inherited_fd_exposure'),('writableprotectedpath','protected_writable'),('unqualifiedobserver accepted','observer_qualified'),('unboundedstderr','stderr_unbounded'),('unverifiedresourcecontrol','resource_verified'),('futurewitnessrequiredatentry','future_witness_at_entry'),('mandatorycontrolswaived','mandatory_waived'),('prematuregrant','grant_issued'),('realprobeauthorityinferred','probe_authority'),('architecturedirectioneffective','architecture_effective'),('infinitesupervisorchainrequired','root_needs_new_supervisor_forever'),('cgroupsclaimeduniversalcharterlaw','cgroup_universal_charter_law'),('qualifiedcontextclauseoptional','exact_permission_clause_optional'),('riskacceptanceasverification','risk_acceptance_equals_verification'),('ownoutputqualifiesouterguard','own_output_qualifies_guard'),('prematureconstruction','construction_enabled'),('budgetguaranteestaskcompletion','budget_predicts_completion')]:reject(name,changed(key,True))
reject('implicitretry',changed('auto_retry',1));reject('publicationslotschanged',changed('slotchoice','EXPLICIT_REVISED_FOUR'));reject('historymodified',changed('history_preserved',False))
reject('selflaunchqualificationcycle',lambda m:m['edges'].append(['MOUNT_WITNESS','NARROW_QUALIFIED_LAUNCH_CONTEXT']))
semantic={'VERIFIER_RAW_SHA256':sha(pathlib.Path(__file__).read_bytes()),'INPUT_PINS_SHA256':sha(canon(manifest['PINS'])),'P124_PROFILE_IDENTITY':profile['IDENTITY'],'AUTHORITY_ROWS':34,'PREENTRY_ROWS':14,'RISK_ROWS':12,'TRUST_ROOTS':['A','B','C','D'],'QUALIFIED_ROOT_IDENTIFIED':False,'PHASE_REQUIREMENTS':36,'REGISTER_HEAD':prev,'CONTRACT_IDENTITIES':{n:sha(canon(load(O/n))) for n in contracts},'READINESS':ready,'GRAPH_ACYCLIC':True,'ACTUAL_SCC':[],'PRIOR_PRESERVATION':'PASS','NEGATIVES':neg}
print(json.dumps({'HASH_SEED':os.environ.get('PYTHONHASHSEED'),'RECONSTRUCTION':semantic,'SEMANTIC_SHA256':sha(canon(semantic))},sort_keys=True))
