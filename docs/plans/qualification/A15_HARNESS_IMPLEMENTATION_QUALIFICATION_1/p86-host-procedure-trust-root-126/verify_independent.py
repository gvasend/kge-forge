"""Read-only static qualification evidence. Does not import/run target or native control programs."""
import pathlib,json,hashlib,collections,sys,subprocess,os,copy
O=pathlib.Path(__file__).resolve().parent;B=pathlib.Path('docs/plans/qualification/A15_HARNESS_IMPLEMENTATION_QUALIFICATION_1');P=B/'p86-trust-root-risk-decision-125';Q=B/'p86-isolation-capability-124'
def load(p):return json.loads(p.read_text())
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def sha(x):return hashlib.sha256(x).hexdigest()
def need(x,r):
 if not x:raise ValueError(r)
def value(p,pointer):
 x=load(p)
 for k in pointer.split('/')[1:]:x=x[int(k)] if isinstance(x,list) else x[k]
 return x
def graph_ok(edges):
 a={};on=set();done=set()
 for x,y in edges:a.setdefault(x,[]).append(y)
 def visit(x):
  need(x not in on,'cycle')
  if x in done:return
  on.add(x)
  for y in a.get(x,[]):visit(y)
  on.remove(x);done.add(x)
 for x in a:visit(x)
 return True
manifest=load(O/'source-authentication-index.json')
for p,h in manifest['PINS'].items():need(sha(pathlib.Path(p).read_bytes())==h,'input pin '+p)
for p,h in load(O/'preservation-before.json')['FILES'].items():need(sha(pathlib.Path(p).read_bytes())==h,'prior history '+p)
profile=load(Q/'exact-candidate-profile.json');need(profile['IDENTITY']==manifest['P124_PROFILE_IDENTITY'] and sha(canon(profile['CONTENT']))==profile['IDENTITY']['sha256']=='2f36be1b7123770d889be302a090cfef16149b270140a9ea901ba992095f46ca','P124unchanged')
wrapper=load(O/'selected-procedure-contract-or-gap.json');proc=wrapper['CONTENT'];need(sha(canon(proc))==wrapper['IDENTITY']['sha256'],'assessment identity')
primary=pathlib.Path(proc['PRIMARY_SOURCE']['PATH']);legacy=load(primary);need(sha(primary.read_bytes())==proc['PRIMARY_SOURCE']['RAW_SHA256'],'actual76 source')
need(proc['EXACT_EXISTING_COMMAND_TEXT']==legacy['COMMAND'] and proc['COMMAND_TEXT_UTF8_SHA256']==sha(legacy['COMMAND'].encode()),'existingcommandnotreplaced')
need(proc['HISTORICAL_HOST_OBSERVATION']=={k:legacy[k] for k in ['HOST_NAME','OPERATING_SYSTEM','KERNEL_VERSION','BUBBLEWRAP_VERSION','USER_CONTEXT','DECLARED_PARENT_SECURITY','OBSERVED_OUTPUT','PROBE_STATUS']} and not legacy['HOST_QUALIFIED'] and not legacy['INDEPENDENT_REPRODUCTION_PERFORMED'],'owner evidence notqualification')
need(proc['DESIRED_UNCHANGED_P124_PROFILE_REFERENCE']['EXACT_BWRAP_ARGV']==profile['CONTENT']['ARGV'] and proc['DESIRED_UNCHANGED_PASSIVE_WITNESS']==load(Q/'passive-witness-specification.json')['EXACT_ARGV'],'newdesiredvectorpreserved')
need(not proc['PROCEDURE_IDENTITY_COMPLETE'] and not proc['QUALIFIED_EXECUTION_PROCEDURE'] and proc['INVOCATIONS_PERFORMED_HERE']==0,'gapnotexistingqualifiedcomposite')
comparison=load(O/'candidate-comparison.json');selected=[r for r in comparison['CANDIDATES'] if r['SELECTED_FOR_DETAILED_ASSESSMENT']];need(len(selected)==1 and selected[0]['ID']==proc['REFERENCE_ID'] and not comparison['QUALIFIED_EXECUTION_PROCEDURE_SELECTED'],'oneanalysisselectionnotgrant')
need(all(not r['QUALIFIED_FOR_P124'] for r in comparison['CANDIDATES']),'no phantomqualification')
observed=load(O/'read-only-existing-facilities.json');need(len(observed['BINARIES'])==6 and observed['CANDIDATE_CONTROL_PROGRAMS_INVOKED']==0,'availablefacilities')
for r in observed['BINARIES']:need(sha(pathlib.Path(r['PATH']).read_bytes())==r['RAW_SHA256'] and str(pathlib.Path(r['PATH']).resolve())==r['RESOLVED'],'currentbinarypin')
trace=load(O/'governing-requirement-trace.json');need(len(trace['ROWS'])==14,'exacttrace')
for r in trace['ROWS']:
 s=r['EXACT_AUTHORITY_SOURCE'];need(sha(pathlib.Path(s['SOURCE_PATH']).read_bytes())==s['RAW_SHA256'] and value(pathlib.Path(s['SOURCE_PATH']),s['JSON_POINTER'])==r['CLAUSE']==s['EXACT_CLAUSE'],'governingclause')
permission=load(O/'permissions-protection-matrix.json');need(not permission['HOST_PERMISSIONS_SUPPORTED_FOR_EXACT_P124'] and not permission['PROTECTED_PATH_CLOSURE_COMPLETE'] and not permission['DESCRIPTOR_ENVIRONMENT_CLOSURE_COMPLETE'],'unverifiedclosure')
resource=load(O/'resource-observer-evidence-contract.json');need(resource['EXACT_P124_RESOURCE_PROPOSALS']==load(Q/'resource-observer-contract.json')['RETAINED_PROPOSED_NUMERIC_LIMITS'] and resource['P124_EVIDENCE_MODEL']==load(Q/'evidence-allocation.json'),'allocationsnotsubstituted')
need(not resource['FINITE_PROPOSED_LIMITS_ENFORCED'] and not resource['RESOURCE_TERMINATION_COMPLETE'] and not resource['INDEPENDENT_OBSERVER_COMPLETE'] and not resource['EVIDENCE_PUBLICATION_COMPLETE'],'no controlclaim')
orig=load(B/'p86-construction-isolation-promotion-122/36-requirement-trace-matrix.json')['ROWS'];phase=load(O/'36-requirement-phase-matrix.json')['ROWS'];need(len(orig)==len(phase)==36,'36requirements')
allowed={'STATICALLY_SPECIFIED','VERIFIED_PRE_ENTRY','ENTRY_PREDICATE_PENDING','EXECUTION_OBSERVATION_REQUIRED','POST_EXECUTION_QUALIFICATION_REQUIRED','UNDETERMINED'}
for o,n in zip(orig,phase):
 need(o['REQUIREMENT_ID']==n['REQUIREMENT_ID'] and o['PHASE']==n['ORIGINAL_PHASE'] and o['ORIGINAL_CLASS']==n['ORIGINAL_CLASS'] and o['EXACT_AUTHORITY_CLAUSE']==n['EXACT_CLAUSE'] and o['AUTHORITY_PIN']==n['EXACT_AUTHORITY_SOURCE'] and n['CLASS'] in allowed,'phaseauthoritypreserved')
 if o['PHASE']=='AUTHORIZED_EXECUTION':need(n['CLASS']=='EXECUTION_OBSERVATION_REQUIRED','no outputatentry')
 elif o['PHASE'].endswith('_ENTRY'):need(n['CLASS']=='ENTRY_PREDICATE_PENDING','nopreentrysafetydeferral')
slots=load(O/'publication-slot-preservation.json');need(slots==load(P/'publication-slot-preservation.json') and slots['SELECTED'] is None,'slotchoicenotselected')
frontpath=pathlib.Path('docs/plans/qualification/E2_P05_D01_A15_EVENT_RECONCILIATION_34/operand-frontier.json');front=load(frontpath);counter=collections.Counter(r['STATUS'] for r in front['REFERENCES']);counts={'TOTAL_REFERENCES':len(front['REFERENCES']),'TOTAL_RESOLVED':counter['RESOLVED'],'TOTAL_UNRESOLVED':counter['UNRESOLVED']}
need(counts==manifest['BASELINE_SOURCE_RECOUNTED']=={'TOTAL_REFERENCES':161,'TOTAL_RESOLVED':109,'TOTAL_UNRESOLVED':52},'retainedbaselinecounts')
need(all(front[k]==v for k,v in counts.items()) and load(O/'baseline-frontier-audit.json')['DISCREPANCIES']==[],'nodiscrepancynormalization');need(sha(frontpath.read_bytes())==load(frontpath.parent/'evidence-index.json')['FILES'][str(frontpath)],'frontierindexpin')
cp=subprocess.run([sys.executable,str(B/'p86-publication-amendment-issuance-115/verify_independent.py'),'EFFECTIVE'],capture_output=True,text=True);need(cp.returncode==0,'freshcharter/104/115/A15');json.loads(cp.stdout)
ready=load(O/'decision-readiness-assessment.json');need(ready['EXISTING_PROCEDURE_SELECTED_FOR_ASSESSMENT'] and not ready['EXISTING_PROCEDURE_QUALIFIED_OR_AUTHORIZED'] and not ready['HOST_PROCEDURE_DECISION_READY'] and not ready['HOST_PROCEDURE_ENTRY_READY'] and ready['DECISION_OPTIONS']==[],'no incompleteoption')
edges=load(O/'dependency-graph.json')['EDGES'];graph_ok(edges)
model={'reference_id':wrapper['IDENTITY'],'old_command':legacy['COMMAND'],'desired_argv':profile['CONTENT']['ARGV'],'permissions_verified':False,'protected_writable':False,'inherited_writable_fd':False,'isolation_supported':False,'unbounded_scratch_accepted':False,'aggregate_verified':False,'parent_only_is_complete_kill':False,'observer_qualified':False,'publication_cap':8666750,'critical_reserve':2336,'duplicate_attempt':False,'own_output_at_entry':False,'slotchoice':None,'authority_issued':False,'h77_enabled':False,'a15_enabled':False,'basic_old_equals_new':False,'installedtools_make_existing_composite':False,'env_umask_verified':False,'attestation_is_sudo':False,'probe_grant_reused':False,'history_preserved':True,'budget_guarantees_completion':False,'edges':edges}
def valid(m):
 need(m['reference_id']==wrapper['IDENTITY'] and m['old_command']==legacy['COMMAND'] and m['desired_argv']==profile['CONTENT']['ARGV'],'exactoldreference/targetidentity')
 need(not any(m[k] for k in ['permissions_verified','protected_writable','inherited_writable_fd','isolation_supported','unbounded_scratch_accepted','aggregate_verified','parent_only_is_complete_kill','observer_qualified']),'unknowncontrol/closure notverified')
 need(m['publication_cap']==8666750 and m['critical_reserve']==2336,'finiteevidence/reserve')
 need(not m['duplicate_attempt'] and not m['own_output_at_entry'] and m['slotchoice'] is None and not m['authority_issued'],'entry/output/attempt/authority')
 need(not any(m[k] for k in ['h77_enabled','a15_enabled','basic_old_equals_new','installedtools_make_existing_composite','env_umask_verified','attestation_is_sudo','probe_grant_reused','budget_guarantees_completion']) and m['history_preserved'],'scope/qualification/riskdistinct')
 graph_ok(m['edges'])
valid(model);neg=[]
def reject(name,mutation):
 m=copy.deepcopy(model);mutation(m)
 try:valid(m)
 except ValueError as e:neg.append({'DESIGN':name,'RESULT':'REJECTED','CAUSE':str(e),'MUTATION_SHA256':sha(canon(m))});return
 raise AssertionError('negativeadmitted:'+name)
def change(k,v):return lambda m:m.__setitem__(k,v)
reject('forged selected-reference pin',lambda m:m['reference_id'].__setitem__('sha256','0'*64))
reject('wrong unchanged124argv',lambda m:m['desired_argv'].append('extra'))
reject('historical command silentlyreplaced',change('old_command','findmnt --json'))
for name,k in [('inventedpermission','permissions_verified'),('writableprotectedpath','protected_writable'),('inheritedwritablefd','inherited_writable_fd'),('unsupportedisolation','isolation_supported'),('unboundedscratch','unbounded_scratch_accepted'),('unqualifiedaggregatecontrol','aggregate_verified'),('parentonlykillcomplete','parent_only_is_complete_kill'),('missingobserverqualified','observer_qualified'),('duplicatelaunch','duplicate_attempt'),('ownfutureoutputasentryproof','own_output_at_entry'),('prematureauthorization','authority_issued'),('H77permission','h77_enabled'),('A15permission','a15_enabled'),('oldsuccessqualifies124','basic_old_equals_new'),('installedtoolsinventexistingcomposite','installedtools_make_existing_composite'),('unknownenvumaskverified','env_umask_verified'),('attestationassudo','attestation_is_sudo'),('realprobegrantreused','probe_grant_reused'),('budgetguaranteescompletion','budget_guarantees_completion')]:reject(name,change(k,True))
reject('unboundedpublication',change('publication_cap',None));reject('missingcriticalreserve',change('critical_reserve',0));reject('unselectedslotchoiceadopted',change('slotchoice','RESERVE_EXISTING_THREE'));reject('historymodified',change('history_preserved',False));reject('owncontextqualificationcycle',lambda m:m['edges'].append(['CHECK_PRODUCED_METADATA','QUALIFIED_NEW_CONTEXT']))
contracts=['candidate-comparison.json','selected-procedure-contract-or-gap.json','existing-to-p124-difference-assessment.json','governing-requirement-trace.json','permissions-protection-matrix.json','resource-observer-evidence-contract.json','risk-reward-assessment.json','remaining-gap-dossier.json','baseline-frontier-audit.json']
semantic={'VERIFIER_RAW_SHA256':sha(pathlib.Path(__file__).read_bytes()),'INPUT_PINS_SHA256':sha(canon(manifest['PINS'])),'EXISTING_ASSESSMENT_PROCEDURE':proc['REFERENCE_ID'],'REFERENCE_IDENTITY':wrapper['IDENTITY'],'OLD_OWNER_COMMAND_SHA256':proc['COMMAND_TEXT_UTF8_SHA256'],'P124_PROFILE_IDENTITY':profile['IDENTITY'],'P124_ARGV_SHA256':profile['CONTENT']['ARGV_SHA256'],'P124_WITNESS_UNCHANGED':True,'PROCEDURE_QUALIFIED':False,'PHASE_ROWS':36,'RETAINED_COUNTS':counts,'CONTRACT_IDENTITIES':{n:sha(canon(load(O/n))) for n in contracts},'READINESS':ready,'GRAPH_ACYCLIC':True,'PRIOR_PRESERVATION':'PASS','NEGATIVES':neg}
print(json.dumps({'HASH_SEED':os.environ.get('PYTHONHASHSEED'),'RECONSTRUCTION':semantic,'SEMANTIC_SHA256':sha(canon(semantic))},sort_keys=True))
