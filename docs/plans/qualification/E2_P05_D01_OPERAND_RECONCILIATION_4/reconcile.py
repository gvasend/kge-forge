"""Contract and native-input reconciliation only. No case operation or mutation runs."""
import ast,hashlib,json
from collections import Counter
from pathlib import Path
from adapter.planner import codec
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;D=R/'docs/plans';Q=D/'qualification';P='DETERMINISTIC_PLANNER_V0_1_'
C3=Q/'E2_P05_D01_OPERAND_CLOSURE_3';C2=Q/'E2_P05_D01_FIXTURE_ORACLE_CLOSURE_2';REC=Q/'E2_P05_D01_RUNNER_INPUT_MATRIX_RECOVERY_1';PLAN=Q/'E2_P05_D01_PROSPECTIVE_MATRIX_CONTRACT_1'
def read(p):return json.loads(Path(p).read_bytes())
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def digest(b):return hashlib.sha256(b).hexdigest()
def ident(x):return 'qualification-D01-reconciliation-v1:'+digest(canon(x))
def pin(p,ptr=''):
 p=Path(p);return dict(path=str(p.relative_to(R)),pointer=ptr,raw_sha256=digest(p.read_bytes()))
def save(n,x):(O/n).write_bytes(canon(x)+b'\n')
def at(x,ptr):
 for k in ptr.split('/')[1:]:x=x[int(k)] if isinstance(x,list) else x[k.replace('~1','/').replace('~0','~')]
 return x
def native_sid(s):return {'$type':'ArtifactIdentity','kind':{'$enum':'IdentityKind','value':'CONTENT_IDENTITY'},'namespace':'planner-snapshot-v1','sha256':digest(codec.canonical_bytes({'schema':'PLANNER-SNAPSHOT-1','snapshot':codec._wire(codec._unwire(s))}))}
def native_bid(p):return {'$type':'ArtifactIdentity','kind':{'$enum':'IdentityKind','value':'CONTENT_IDENTITY'},'namespace':'planner-bundle-v1','sha256':digest(Path(p).read_bytes())}
def source_check(p):
 path=R/p['path'];okay=path.is_file() and not path.is_symlink()
 if not okay:return {'status':'MISSING_OR_SYMLINK','pin':p}
 raw=path.read_bytes();profile=p['profile']['value'];expected=p['identity']
 if expected['namespace']!=profile:return {'status':'IDENTITY_DOMAIN_MISMATCH','pin':p}
 if profile=='raw-file-sha256':actual=digest(raw)
 elif profile=='canonical-json-sha256':actual=digest(codec.canonical_bytes(codec.parse_json(raw)))
 else:return {'status':'UNSUPPORTED_PROFILE','pin':p}
 return {'status':'PASS' if actual==expected['sha256'] and expected['kind']['value']=='CONTENT_IDENTITY' else 'FAIL','pin':p,'actual_sha256':actual}
def check_bundle(p,body):
 codec._unwire(body) # structural decoding only
 checks=[source_check(x) for x in body['sources']+[body['policy']]]
 assert all(x['status']=='PASS' for x in checks),checks
 assert codec.canonical_bytes({'schema':'PLANNER-BUNDLE-1','bundle':codec._wire(codec._unwire(body))})==Path(p).read_bytes()
 return checks
source_inventory=read(C3/'operand-source-and-derivation-inventory.json');frozen39=source_inventory['ROWS'];assert len(frozen39)==39
runtime=read(C3/'entrypoint-contracts.json')
for op,contract in runtime.items():
 p=contract['SOURCE'];assert digest((R/p['path']).read_bytes())==p['raw_sha256']
seal=read(C2/'runner-v2-source-seal.json')
for key in ['source','helpers','dispatch']:
 p=seal[key];assert digest((R/p['path']).read_bytes())==p['raw_sha256']
save('runtime-currentness.json',{'STATUS':'PASS_EXACT_CLOSURE3_NATIVE_PINS_AND_V2_SEAL','ENTRYPOINT_CONTRACT_SOURCE':pin(C3/'entrypoint-contracts.json'),'CONTRACTS':runtime,'V2_SEAL':pin(C2/'runner-v2-source-seal.json'),'SEMANTIC_EXECUTION_OR_REPLAY_VALIDATION':'NOT_RUN'})
# Exact raw prior inventory is retained by pin; record bodies are copied without editing.
save('frozen-39-bindings.json',{'SOURCE':pin(C3/'operand-source-and-derivation-inventory.json'),'ROWS':frozen39,'SEMANTIC_IDENTITY':ident(frozen39),'MUTATIONS_APPLIED':0,'INVALIDATIONS_APPLIED':0})
for row in frozen39:
 p=row['SOURCE_ARTIFACT'];assert digest((R/p['path']).read_bytes())==p['raw_sha256']
 for p in row.get('PROVENANCE',[]):
  if isinstance(p,dict) and 'raw_sha256' in p:assert digest((R/p['path']).read_bytes())==p['raw_sha256']
all111=read(C3/'initial-111-operand-inventory.json')['ROWS'];pending=[r for r in all111 if r['STATUS']!='RESOLVED'];assert len(all111)==111 and len(pending)==72
obligations=read(PLAN/'sealed-128-obligations.json')['obligations'];obs={r['OBLIGATION_ID']:r for r in obligations};catalog=read(C2/'fixture-catalog.json');dispatch=read(C2/'dispatch-table-v2.json')
canonical_path=D/(P+'CANONICAL_QUALIFICATION_EXPERIMENT_1.json');cases=read(canonical_path)['cases'];case_byid={c['CASE_ID']:c for c in cases};case_ptr={c['CASE_ID']:'/cases/'+str(i) for i,c in enumerate(cases)}
initial_classes=['A03_BOUNDARY','A14_BOUNDARY','A03_A14_CROSS_BOUNDARY','MUTATION_SOURCE','MUTATION_DESCRIPTOR','SOURCE_BINDING','SOURCE_CURRENTNESS','IDENTITY_DOMAIN','PARENT_HEAD','CONTEXT_PHASE','OTHER']
classified=[]
for old in pending:
 row=dict(old);case=row['CASE_ID'];name=row['OPERAND_NAME'];oid=row['OBLIGATION_ID']
 if case=='E2-A03':cause='A03_BOUNDARY';boundary='D01_A03_PRE_ACQUISITION'
 elif case in ['E2-A14','E2-A16','E2-N02']:cause='A14_BOUNDARY';boundary='D01_A14_GOVERNED_UNKNOWN_BEFORE_AND_AFTER_COLD_RESTORE'
 elif name=='expected_bundle_identity':cause='SOURCE_BINDING';boundary='TRUSTED_PRETAMPER_BUNDLE'
 elif oid in ['D01-OBL:MUTATION_SOURCE','D01-OBL:CONTROL_01']:cause='MUTATION_SOURCE';boundary='SOURCE_BYTES_PRE_MUTATION'
 elif name=='pin':cause='OTHER';boundary='ALL_CURRENT_AND_PREFIX_AVAILABLE_SOURCES'
 elif name in ['request','predicate_id','bundle_path']:cause='MUTATION_DESCRIPTOR';boundary='ROW_NATIVE_PRESTATE_BEFORE_DEFERRED_MUTATION'
 else:cause='SOURCE_BINDING';boundary='ROW_NATIVE_PRESTATE_BEFORE_SOURCE_INVALIDATION'
 row.update(PRIMARY_CAUSE=cause,DEPENDENT_BOUNDARY=boundary,EXACT_ROOT_CAUSE='')
 if cause=='A14_BOUNDARY' and case=='E2-N02':row['EXACT_ROOT_CAUSE']='Canonical N02 starts from A14 unknown-rule copy; capsule instead has rule_known=true and different lineage/generation. Its request operand is not uniquely specified by malformed-route semantics.'
 elif oid=='D01-OBL:SOURCE_BYTES':row['EXACT_ROOT_CAUSE']='Frozen source role requires each current/prefix source; singular LOAD_PIN(pin) does not select one complete collection. No authoritative singular-source selection.'
 elif name=='expected_bundle_identity':row['EXACT_ROOT_CAUSE']='Trusted pre-tamper identity is absent from arguments but deterministically recoverable from exact retained capsule bundle source.'
 else:row['EXACT_ROOT_CAUSE']=row['CURRENT_GAP']
 classified.append(row)
assert len(classified)==72
save('72-reference-classification.json',{'COUNT':72,'PRIMARY_CAUSE_COUNTS':{k:sum(r['PRIMARY_CAUSE']==k for r in classified) for k in initial_classes},'ROWS':classified,'CROSS_BOUNDARY_NOTE':'A03 and A14 have no shared producer/consumer edge; zero cross-boundary primary assignments. A16/N02 explicitly depend on A14 in canonical cases.'})
# Recover semantic boundaries directly from original cases, not P05 package names.
def capsule(cid):
 e=next(e for e in catalog.values() if e['state_variant_id']==f'D01-VARIANT:{cid}:CANONICAL_REQUIRED_BEHAVIOR');p=R/e['artifact']['path'];return e,read(p)
a3e,a3p=capsule('E2-A03');a14e,a14p=capsule('E2-A14');a16e,a16p=capsule('E2-A16')
a3source=D/(P+'E2_P05_A03_PROSPECTIVE_OCCURRENCE_BUNDLE_1.json');a3bundle=read(a3source)['bundle']
collect=[(i,e) for i,e in enumerate(a3bundle['events']) if e['result'].get('action',{}).get('value')=='E2-COLLECT'];assert len(collect)==1
ci,ce=collect[0]
publication=Q/'E2_P05_A03_PROSPECTIVE_OCCURRENCE_EXECUTION_1/writer-main/writer-result.json'
headpub=[x for x in read(publication)['HEAD_publications'] if x['after']=='E2-CHECK'];assert len(headpub)==1
prefixhash=headpub[0]['head']['bundle']['sha256'];prefixpath=publication.parent/'checkpoints/post-check'/('bundle-'+prefixhash+'.json');prefix=read(prefixpath)['bundle']
assert native_bid(prefixpath)==headpub[0]['head']['bundle'];assert prefix['events']==a3bundle['events'][:ci]
assert native_sid(prefix['current'])==ce['parent_snapshot']==ce['result']['expected_snapshot']
assert prefix['events'][-1]['identity']==ce['parent_event']
actions=[a for a in prefix['current']['actions'] if a['id']==ce['result']['action']];assert len(actions)==1 and actions[0]['operation']['value']=='SOURCE_ACQUISITION'
assert ce['result']['knowledge']==actions[0]['accepted_inventory']
checks=check_bundle(prefixpath,prefix)
for e in prefix['events']:
 ep=prefixpath.parent/('event-'+e['identity']['sha256']+'.json');assert ep.read_bytes()==codec.canonical_bytes(e)
oldstate=a3p['canonical_content']['subject'];assert native_sid(oldstate)!=native_sid(prefix['current'])
a03={
 'CASE_ID':'E2-A03','CONTRACT_SOURCE':pin(canonical_path,case_ptr['E2-A03']),'ORIGINAL_CASE':case_byid['E2-A03'],
 'INPUT_BOUNDARY':'Selected SOURCE_ACQUISITION action, bounded externally supplied result; not the start of the separately named P05 A03 two-action package',
 'PRE_STATE_SOURCE':pin(prefixpath,'/bundle/current'),'PRE_STATE_IDENTITY':native_sid(prefix['current']),
 'BUNDLE_SOURCE':pin(prefixpath),'BUNDLE_IDENTITY':native_bid(prefixpath),'EXPECTED_PARENT':ce['parent_snapshot'],'EXPECTED_HEAD':ce['parent_event'],
 'NATIVE_OPERATION':'adapter.planner.codec.commit_event (preserved V2); native result application and append remain owned by native code',
 'SUPPLIED_INPUT_SOURCE':pin(a3source,f'/bundle/events/{ci}/result'),'SUPPLIED_NATIVE_TYPE':'SuppliedResult','SUPPLIED_ACTION_DOMAIN':'ActionId/E2-COLLECT',
 'RESULT_BOUNDARY':'SuppliedResult is an existing invocation input; TransitionReport/committed bundle are future native returns, not pre-supplied',
 'EVENT_BOUNDARY':'Existing prefix head retained; future append belongs to the acquisition operation; no append in this package',
 'POST_STATE':'Future native result application; excluded from pre-state bindings; no expected full output constructed',
 'PHASE':'PRE_ACQUISITION -> NATIVE_APPLICATION_AND_APPEND -> POST_ACQUISITION',
 'MUTATION_INVALIDATION_TIMING':'No mutation during positive invocation; later invalidation only at a separately declared dependency boundary',
 'CONFLICT':'WRONG_BOUNDARY_ASSIGNMENT','CAPSULE_OVERRIDE_REQUIRED':True,'OLD_CAPSULE_SOURCE':a3e['artifact'],
 'LOCATOR_RULE':'Use qualified publication after CHECK, then verify native ordered prefix, acquisition operation class, accepted inventory, result expected_snapshot and parent/head. Locator report is not native evidence.',
 'SOURCE_CURRENTNESS_CHECKS':checks,'AFFECTED_ROWS':['D01-OBL:E2-A03_OPERANDS','D01-OBL:E2-A03_ORACLE'],'STATUS':'PASS_BOUNDARY_AND_RETAINED_INPUT_RECONCILIATION_NOT_CASE_QUALIFICATION'}
save('a03-boundary-oracle.json',a03)
gov=a14p['canonical_content']['subject'];govsid=native_sid(gov);assert all(not r['rule_known'] for r in gov['evidence_requirements']);assert any(g['resolution_contracts'] for g in gov['external_gates']);assert gov==a16p['canonical_content']['subject']
def findprovs(x):
 if isinstance(x,dict):
  if x.get('$type')=='Provenance':yield x
  for v in x.values():yield from findprovs(v)
 elif isinstance(x,list):
  for v in x:yield from findprovs(v)
missing_gov=sorted({p['path'] for p in findprovs(gov) if p.get('path') and not (R/p['path']).is_file()})
a14={
 'CASE_ID':'E2-A14','CONTRACT_SOURCE':pin(canonical_path,case_ptr['E2-A14']),'ORIGINAL_CASE':case_byid['E2-A14'],
 'INPUT_BOUNDARY':'Independent external checkpoint copy with unknown rule and valid ExternalResolutionContract',
 'PRE_STATE_SOURCE':a14e['artifact'],'PRE_STATE_IDENTITY':govsid,'SCOPE':gov['context']['scope'],'LINEAGE':gov['context']['lineage'],'GENERATION':gov['context']['generation'],
 'NATIVE_OPERATION_SEQUENCE':['recompute','native persistence','writer termination','cold restore'],
 'RESULT_BOUNDARY':'Computed qualification observation separate from native checkpoint; not a SuppliedResult or positive receipt',
 'EVENT_STATE_BOUNDARY':'No Evidence/rule admission; rule_known remains false; no new occurrence is required by recompute alone',
 'PHASES':['GOVERNED_UNKNOWN_PRE_RECOMPUTE','COMPUTED_OBSERVATION','PERSISTED_CHECKPOINT','WRITER_TERMINATED','COLD_RESTORED_CHECKPOINT'],
 'MUTATION_INVALIDATION_TIMING':'A14 does not mutate/admit rule; A16 invalidation occurs only after successful cold restore of A14 variant',
 'PERSISTENCE_CONFLICT':'V2 SAVE_BUNDLE requires absent PersistenceBundle; subsequent RESTORE fixture fields do not reference preceding native save return',
 'BUNDLE_BINDING':'UNRESOLVED: no retained exact governed-unknown PersistenceBundle is selected, and policy/source-root/archive construction is not uniquely pinned',
 'CONTRACT_PERSISTENCE_AMBIGUITY':'Historical backend is not recovered from original save/terminate/restore wording. Prospective backend stays the sealed V2 codec.save_bundle/codec.restore; Snapshot decode from the retained E06 analogue cannot replace that bundle contract.',
 'REQUIRED_SAVE_RETURN_BINDINGS':{'bundle_path':{'producer':'codec.save_bundle','selector':[0],'native_type':'Path'},'expected_bundle_identity':{'producer':'codec.save_bundle','selector':[1],'native_type':'ArtifactIdentity CONTENT_IDENTITY/planner-bundle-v1'}},
 'COLD_PROCESS_TRANSFER_GAP':'Writer must terminate after native save before a fresh reader parses a durable handoff of path/trusted identity. Same-process prior_result alone does not establish cold-reader isolation. No handoff values or backend substitution are fabricated.',
 'MISSING_REPO_ROOT_SOURCE_PATHS':missing_gov,
 'AFFECTED_ROWS':sorted({r['OBLIGATION_ID'] for r in classified if r['PRIMARY_CAUSE']=='A14_BOUNDARY'}),
 'STATUS':'PASS_SEMANTIC_STATE_BOUNDARY; CONCRETE_PERSISTENCE_BINDING_UNRESOLVED'}
save('a14-boundary-oracle.json',a14)
conflicts=[]
for r in classified:
 if r['PRIMARY_CAUSE'] not in ['A03_BOUNDARY','A14_BOUNDARY']:continue
 case=r['CASE_ID'];reason='WRONG_BOUNDARY_ASSIGNMENT' if case in ['E2-A03','E2-N02'] else ('MISSING_SOURCE' if r['OPERAND_NAME']=='bundle' else 'MISSING_PROJECTION')
 conflicts.append({'OBLIGATION_ID':r['OBLIGATION_ID'],'OPERAND_NAME':r['OPERAND_NAME'],'EXPECTED_PRODUCER':'Qualified pre-acquisition prefix' if case=='E2-A03' else 'Governed-unknown A14 checkpoint / native save return','EXPECTED_CONSUMER':r['REQUIRED_BY_ENTRYPOINT'],'OWNER_BOUNDARY':r['DEPENDENT_BOUNDARY'],'PRE_OR_POST':'PRE_OPERATION' if r['OPERAND_NAME'] not in ['bundle_path','expected_bundle_identity'] else 'POST_SAVE_NATIVE_RETURN consumed before RESTORE','DURABLE_OR_COMPUTED':'NATIVE_INPUT_OR_DURABLE_SAVE_RETURN; never Computation as bundle','CROSSING_RULE':'Only explicit predecessor-native-return selectors after save; A03 and A14 cannot consume one another','CONFLICT_CLASS':reason,'UNIQUE_CONCRETE_RESOLUTION':case=='E2-A03'})
save('boundary-conflicts.json',conflicts)
boundarymap=[{'OBLIGATION_ID':r['OBLIGATION_ID'],'STATE_VARIANT_ID':r['STATE_VARIANT_ID'],'OWNER_BOUNDARY':'D01_A03_PRE_ACQUISITION' if r['CASE_ID']=='E2-A03' else 'D01_A14_GOVERNED_UNKNOWN','CASE_PHASE':'AFTER_A14_RESTORE_BEFORE_INVALIDATION' if r['CASE_ID']=='E2-A16' else 'A14_COPY_BEFORE_ROUTE_MUTATION' if r['CASE_ID']=='E2-N02' else 'PRE_ACQUISITION' if r['CASE_ID']=='E2-A03' else 'PRE_RECOMPUTE_THEN_SAVE_TERMINATE_RESTORE','LEGITIMATE_BOUNDARY_COUNT':1,'NO_PRE_POST_ALIAS':True} for r in classified if r['PRIMARY_CAUSE'] in ['A03_BOUNDARY','A14_BOUNDARY']]
boundarymap=list({(r['OBLIGATION_ID'],r['STATE_VARIANT_ID']):r for r in boundarymap}.values());save('affected-row-boundary-map.json',boundarymap)
# New resolved references: exact A03 input rebind, and external trusted pre-tamper identities.
new=[];cross=[];sourcebindings=[];overrides=[]
for row in classified:
 name=row['OPERAND_NAME'];cid=row['CASE_ID'];e=catalog[row['CAPSULE_ID']];packet=read(R/e['artifact']['path']);content=packet['canonical_content'];native_state=content['subject']
 result=None
 if cid=='E2-A03':
  v=ce['result'];src=pin(a3source,f'/bundle/events/{ci}/result');codec._unwire(v)
  override={'OBLIGATION_ID':row['OBLIGATION_ID'],'CAPSULE_ID':e['fixture_id'],'STATE_VARIANT_ID':e['state_variant_id'],'ORIGINAL_CAPSULE':e['artifact'],'OVERRIDE_REASON':'WRONG_BOUNDARY_ASSIGNMENT proved by original case and exact expected_snapshot mismatch','OPERAND_SOURCE_OVERRIDES':{'snapshot':pin(prefixpath,'/bundle/current'),'bundle':pin(prefixpath,'/bundle'),'policy':pin(prefixpath,'/bundle/policy'),'policy_version':pin(prefixpath,'/bundle/policy_version')},'EXPECTED_PARENT':ce['parent_snapshot'],'EXPECTED_HEAD':ce['parent_event'],'PHASE':'PRE_ACQUISITION','NATIVE_STATE_MUTATION':False,'OLD_CAPSULE_EDITED':False}
  overrides.append(override);native_state=prefix['current'];result={'VALUE_REFERENCE':src,'NATIVE_TYPE':'SuppliedResult','SOURCE_IDENTITY':ident(v),'NATIVE_IDENTITY_DOMAINS':{'action':v['action'],'expected_snapshot':v['expected_snapshot']},'DERIVATION_RULE':a03['LOCATOR_RULE'],'SOURCE_CURRENTNESS':'PASS_EXACT_PREFIX_SOURCE_AND_POLICY_PINS','BOUNDARY_ORACLE':pin(O/'a03-boundary-oracle.json'),'REQUIRES_INVOCATION_CAPSULE_OVERRIDE':True}
 elif name=='expected_bundle_identity' and cid!='E2-A14':
  base=content.get('bundle');original=content['source'];p=R/original['path'];doc=read(p)
  assert base is not None and doc.get('bundle')==base and digest(p.read_bytes())==original['raw_sha256']
  checks=check_bundle(p,base);v=native_bid(p)
  result={'VALUE':v,'NATIVE_TYPE':'ArtifactIdentity','SOURCE_IDENTITY':v,'DERIVATION_RULE':'Retain externally trusted raw pre-tamper bundle identity from exact capsule-owned native file; never trust attacker-rehashed or future saved bytes','SOURCE_CURRENTNESS':'PASS_RAW_IDENTITY_ALL_BASE_SOURCE_AND_POLICY_PINS','SOURCE_CHECKS':checks,'BOUNDARY_ORACLE':None,'MUTATED_BUNDLE_PATH_STILL_UNRESOLVED':True};src=pin(p)
 if result:
  ctx=native_state['context'];newrow={'OBLIGATION_ID':row['OBLIGATION_ID'],'CASE_ID':cid,'DISPATCH_ID':row['DISPATCH_ID'],'CAPSULE_ID':row['CAPSULE_ID'],'STATE_VARIANT_ID':row['STATE_VARIANT_ID'],'STEP':row['STEP'],'OPERAND_NAME':name,'SOURCE_ARTIFACT':src,'SCOPE':ctx['scope'],'LINEAGE':ctx['lineage'],'GENERATION':ctx['generation'],'PROVENANCE':[e['artifact'],src],'STATUS':'RESOLVED','OPERATION_EXECUTED':False,'MUTATIONS_APPLIED':0,'INVALIDATIONS_APPLIED':0,**result}
  new.append(newrow);sourcebindings.append(newrow)
  cross.append({'OBLIGATION_ID':row['OBLIGATION_ID'],'OPERAND_NAME':name,'CHECKS':{'BASE_SOURCE_PRECEDES_MUTATION':True,'NATIVE_IDENTITY_DOMAIN':True,'SCOPE_LINEAGE_GENERATION_FROM_INPUT':True,'NO_FUTURE_OUTPUT_AS_INPUT':True,'PARENT_HEAD_FROM_INPUT':True,'NO_A03_A14_SOURCE_LEAKAGE':True},'BOUND_OPERAND_CHECK':'PASS','COMPLETE_INVOCATION_CHECK':'NOT_RUN'})
resolved_keys={(r['OBLIGATION_ID'],r['STATE_VARIANT_ID'],r['STEP'],r['OPERAND_NAME']) for r in new}
remaining=[r for r in classified if (r['OBLIGATION_ID'],r['STATE_VARIANT_ID'],r['STEP'],r['OPERAND_NAME']) not in resolved_keys]
assert len(new)==13 and len(remaining)==59 and 39+len(new)+len(remaining)==111
save('new-source-bindings.json',{'ROWS':sourcebindings,'COUNT':len(new),'NATIVE_OPERATIONS_EXECUTED':0})
save('a03-invocation-source-overrides.json',overrides)
save('cross-operand-checks.json',{'ROWS':cross,'COMPLETE_INVOCATION_STATIC_PREFLIGHT':'NOT_RUN_UNRESOLVED_REFERENCES'})
# Candidate inventory from retained recovery, plus capsule-native source classes/identities.
cat=read(REC/'candidate-source-catalog.json');originalrows={r['INPUT_ID']:r for r in read(REC/'runner-input-matrix.json')};candidates=[];mutations=[]
for row in remaining:
 e=catalog[row['CAPSULE_ID']];packet=read(R/e['artifact']['path']);content=packet['canonical_content'];s=content['subject'];ob=obs[row['OBLIGATION_ID']];oldrole=originalrows[ob['ORIGINAL_INPUT_ID']]
 owned=[]
 for i,k in enumerate(s.get('knowledge',[])):owned.append({'ROLE':'KNOWLEDGE','SOURCE':{**e['artifact'],'pointer':'/canonical_content/subject/knowledge/'+str(i)},'NATIVE_ID':k['id'],'SOURCE_IDENTITY':k['provenance']['identity'],'STATUS':'CANDIDATE_NOT_SELECTED'})
 for i,p in enumerate((content.get('bundle') or {}).get('sources',[])):owned.append({'ROLE':'SOURCE','SOURCE':{**e['artifact'],'pointer':'/canonical_content/bundle/sources/'+str(i)},'NATIVE_PIN':p,'CURRENTNESS':source_check(p),'STATUS':'CANDIDATE_NOT_SELECTED'})
 candidates.append({'OBLIGATION_ID':row['OBLIGATION_ID'],'STATE_VARIANT_ID':row['STATE_VARIANT_ID'],'OPERAND_NAME':row['OPERAND_NAME'],'REQUIRED_SOURCE_CLASS':ob['INPUT_REQUIREMENTS']['expected_source_class'],'EXPECTED_NATIVE_TYPE':row['EXPECTED_TYPE'],'CONSUMER':row['REQUIRED_BY_ENTRYPOINT'],'SCOPE':s['context']['scope'],'LINEAGE':s['context']['lineage'],'PROVENANCE':packet['provenance'],'IDENTITY_DOMAIN':row['EXPECTED_IDENTITY_DOMAIN'],'RECOVERED_CANDIDATES':[{'CANDIDATE_ID':cid,**cat[cid]} for cid in oldrole['CANDIDATE_IDS']],'CAPSULE_OWNED_CANDIDATES':owned,'ELIGIBILITY':'NOT_SELECTED; role, boundary and currentness must all match; report-only evidence cannot replace native operand','UNRESOLVED_REASON':row['EXACT_ROOT_CAUSE']})
 if row['PRIMARY_CAUSE'] in ['MUTATION_SOURCE','MUTATION_DESCRIPTOR','A14_BOUNDARY'] and (row['OPERAND_NAME'] in ['request','predicate_id','bundle_path','pin']):
  mutations.append({'OBLIGATION_ID':row['OBLIGATION_ID'],'STATE_VARIANT_ID':row['STATE_VARIANT_ID'],'OPERAND_NAME':row['OPERAND_NAME'],'BASE_SOURCE':e['artifact'],'BASE_IDENTITY':e['content_identity'],'BASE_STATE_IDENTITY':native_sid(s),'EXPECTED_AFFECTED_DIMENSION':ob['EXPECTED_BEHAVIOR'],'FROZEN_MUTATION_EXPECTATION':ob['MUTATION_EXPECTATION'],'TARGET':'NOT_UNIQUELY_SELECTED','OPERATOR':'NOT_UNIQUELY_SELECTED','PARAMETERS':'NOT_SEALED','EXPECTED_UNCHANGED_DIMENSIONS':['state generation except where lineage/generation explicitly tested','unrelated Action definitions','unrelated source/policy pins','ordered ancestry except declared tampering','scope except explicit scope negative'],'STATUS':'UNSEALED_CONTRACT_INVENTORY_NOT_EXECUTABLE_DESCRIPTOR','APPLIED':False,'IS_INVALIDATION_DESCRIPTOR':False})
save('source-candidate-inventory.json',candidates)
save('mutation-contract-inventory.json',mutations)
save('mutation-descriptors.json',{'SEALED_DESCRIPTORS':[],'COUNT':0,'UNSEALED_CONTRACT_INVENTORY':pin(O/'mutation-contract-inventory.json'),'REASON':'No remaining mutation reference has a uniquely pinned target/operator/parameter combination from the frozen obligation and capsule. No arbitrary wrong value or unrelated positive base is selected.','APPLIED':0,'INVALIDATIONS_APPLIED':0})
save('resolved-bindings.json',{'PRESERVED_39':frozen39,'NEW_BINDINGS':new,'TOTAL_RESOLVED':52,'TOTAL_UNRESOLVED':59,'SEMANTIC_IDENTITY':ident({'PRESERVED_39':frozen39,'NEW_BINDINGS':new})})
save('remaining-frontier.json',{'TOTAL_UNRESOLVED':59,'PRIMARY_CAUSE_COUNTS':dict(Counter(r['PRIMARY_CAUSE'] for r in remaining)),'NEXT_UNRESOLVED_CLASS':'A14_BOUNDARY','ROWS':remaining,'COMPLETE_PREFLIGHT':'NOT_RUN','ORACLE_HANDOFF':'NOT_CREATED','REQUIRED_RECONCILIATION':'Pin A14 persistence/source root/policy/archive and explicit save-return-to-restore dataflow; repair N02 unknown-rule boundary before binding request mutations. Then pin remaining target/operator/parameters and source variants.'})
print(json.dumps({'INITIAL':72,'RESOLVED_THIS_PACKAGE':13,'TOTAL_RESOLVED':52,'TOTAL_UNRESOLVED':59,'A03':'RECONCILED','A14':'SEMANTIC_BOUNDARY_RECOVERED_PERSISTENCE_UNRESOLVED'}))
