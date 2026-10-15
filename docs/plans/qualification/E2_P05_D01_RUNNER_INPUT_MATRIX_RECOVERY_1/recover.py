"""Static contract/source recovery only. Never import or execute a runner."""
import ast
import hashlib
import json
from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parents[4];OUT=Path(__file__).resolve().parent
D=ROOT/'docs/plans';Q=D/'qualification';P='DETERMINISTIC_PLANNER_V0_1_'
def read(p):return json.loads(Path(p).read_bytes())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def ref(p,pointer=''):
 p=Path(p);return dict(path=str(p.relative_to(ROOT)),pointer=pointer,raw_sha256=sha(p))
def save(n,x):(OUT/n).write_text(json.dumps(x,sort_keys=True,indent=2)+'\n')
def require(v,m):
 if not v:raise ValueError(m)
def pointer(x,p):
 for t in p.split('/')[1:]:x=x[int(t)] if isinstance(x,list) else x[t.replace('~1','/').replace('~0','~')]
 return x
plan=read(D/(P+'CANONICAL_QUALIFICATION_EXPERIMENT_1.json'));spec=read(D/(P+'E2_PC04_D01.json'))
caseindex=next(i for i,c in enumerate(plan['cases']) if c['CASE_ID']=='E2-D01');case=plan['cases'][caseindex]
interface=read(Q/'E2_P05_END_INTERFACE_CLOSURE_1/six-interface-inventory.json')['interfaces'][4]
fx=read(D/(P+'E2_PC03_FIXTURES.json'));pc03=read(Q/'E2_P05_PC03_END_BINDING_1/selected-source-collection.json')
blocked=read(D/(P+'E2_P05_D01_END_BINDING_1.json'))
require(blocked['RESULT']=='BLOCKED' and blocked['END_INTERFACES_BOUND']==4,'BLOCKED_BASELINE')
# Namespace inspection only; do not treat these as runner source candidates.
durable=read(D/(P+'DURABLE_ADMISSION_D01_RESULT.json'))
namespace=dict(E2_D01=dict(identity=ref(D/(P+'E2_PC04_D01.json')),case_id='E2-D01',purpose=case['PURPOSE'],owning_package='Canonical E2; E2-P05 aggregate determinism, E2-PC04 preflight interface',inputs=spec['dependencies'],outputs=spec['oracle']['compare'],consumer='E2-END and later E2-REVIEW',qualification_result=spec['status'],native_operation='Aggregate seed/presentation/fresh-process comparison over supported native states; not a new native event'),DURABLE_ADMISSION_D01=dict(identity=ref(D/(P+'DURABLE_ADMISSION_D01_RESULT.json')),work_package=durable['WORK_PACKAGE'],purpose='Generic durable dossier-result transaction and historical replay',owning_package=durable['WORK_PACKAGE'],inputs=durable['EXECUTION_INPUTS'],outputs=['post-Snapshot','occurrence event','DossierMaterializationBinding','PersistenceBundle','atomic HEAD'],consumer='Qualified bounded dossier-result acquisitions; prospective A04 actual consumer',qualification_result=durable['DURABLE_ADMISSION_CAPABILITY'],native_operation='dossier_transaction.prepare/commit/execute'),E2_D01_IS_DURABLE_ADMISSION_D01='NO')
save('namespace-disambiguation.json',namespace)
original=dict(D01_ID='E2-D01',D01_PURPOSE=case['PURPOSE'],earliest_authoritative_definition_located=ref(D/(P+'CANONICAL_QUALIFICATION_EXPERIMENT_1.json'),'/cases/'+str(caseindex)),original_acceptance=ref(D/(P+'CANONICAL_QUALIFICATION_ACCEPTANCE_MATRIX_1.md')),absolute_creation_chronology='Not inferred from filesystem timestamps; canonical original declaration governs',D01_RUNNER='Aggregate determinism protocol; exact executable/hash not specified',D01_INPUTS=dict(semantic_states=case['INITIAL_STATE'],dependencies=spec['dependencies'],dimensions=spec['dimensions']),D01_PRECONDITIONS='Qualified PC01-PC03 canonical model/proof/authority/lifecycle/phase/persistence/oracle contracts and T01 capability; later execution dependencies explicit',D01_EXECUTION_MODEL=case['OPERATION'],D01_EXPECTED_OUTPUTS=spec['oracle'],D01_ACCEPTANCE=case,D01_POSTCONDITION='Full equal-semantic comparisons pass, ordered chronology preserved; no qualification authority or future execution permission issued',pc04_definition=ref(D/(P+'E2_PC04_D01.json')),pc04_explanatory_source=ref(D/(P+'E2_PC04_RESULT.md')))
save('original-contract.json',original)
# Exact code candidates are enumerated via AST only; none is named by sealed END.
code_paths=[D/(P+'E2_PC01_ORACLE.py'),D/(P+'E2_PC02_ORACLE.py'),D/(P+'E2_PC03_ORACLE.py'),ROOT/'adapter/tests/qualify_finish_f03.py',ROOT/'adapter/tests/qualify_finish_f03_checks.py',ROOT/'adapter/tests/qualify_reentry_r05.py',Q/'E2_P04_CANONICAL_EXECUTION_RETRY_1/verify.py',Q/'E2_P05_A03_PROSPECTIVE_OCCURRENCE_EXECUTION_1/execution_driver.py',Q/'E2_P05_A04_PROSPECTIVE_ANCESTRY_EXECUTION_1/execution_driver.py',Q/'E2_P05_A05_ALTERNATE_NATIVE_EVIDENCE_1/execution_driver.py',Q/'E2_P05_A06_PROSPECTIVE_REQUEST_WAIT_EXECUTION_1/execution_driver.py',Q/'E2_P05_PC03_END_BINDING_1/binding_v2.py',Q/'E2_P05_T01_END_BINDING_1/binding.py']
runner=[]
for path in code_paths:
 if not path.is_file():continue
 tree=ast.parse(path.read_text());funcs=[dict(name=n.name,line=n.lineno,parameters=[a.arg for a in n.args.args]) for n in ast.walk(tree) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))]
 runner.append(dict(source=ref(path),version_hash=sha(path),entrypoints=funcs,declared_by_sealed_contract=False,classification='OTHER' if 'adapter/tests' in str(path) or path.suffix=='.py' else 'QUALIFICATION_PROJECTION',eligible_role='Candidate component only; no complete E2-D01 runner provenance binding',input_schema='Local source function parameters and retained manifests; no common complete E2-D01 invocation schema',output_schema='Local fixture checks/typed-state comparisons/reader result JSON; no complete E2-D01 output envelope',does_not_cover_all_32_state_cases=True))
source_resolution=dict(RUNNER_SOURCE=None,RUNNER_SOURCE_IDENTITY=None,RUNNER_VERSION_HASH=None,ENTRYPOINT=None,INPUT_SCHEMA='No complete executable invocation schema pinned; protocol input obligations recoverable',OUTPUT_SCHEMA='Comparisons specified; complete runner result serialization not fixed',candidates=runner,resolution='CONTRACT_AMBIGUITY: protocol is uniquely identified; exact complete executable is not declared. Local components are not interchangeable by name.',no_runner_selected=True)
save('runner-source-candidates.json',source_resolution)
# Candidate pool: exact per-case declarations, native roles and all named local contracts/process records.
catalog={};serial=0
allowed=['CANONICAL_NATIVE','QUALIFIED_NATIVE','AUTHORIZED_PROSPECTIVE_REPLACEMENT','AUTHORIZED_ALTERNATE_NATIVE_EVIDENCE','QUALIFICATION_PROJECTION','REPORT_ONLY','SNAPSHOT_ONLY','STALE','OTHER']
def add(source,classification,role,semantics=None,context=None):
 global serial
 require(classification in allowed,'CLASS')
 path=ROOT/source['path'];actual=ref(path,source.get('pointer',''));pin_match=actual['raw_sha256']==source.get('raw_sha256',actual['raw_sha256'])
 key=(actual['path'],actual['pointer'],role)
 for cid,c in catalog.items():
  if (c['source']['path'],c['source']['pointer'],c['role'])==key:return cid
 serial+=1;cid='C'+str(serial).zfill(4)
 catalog[cid]=dict(source=actual,classification=classification if pin_match else 'STALE',role=role,source_identity=semantics or actual['raw_sha256'],context=context or 'Source-specific contract; no inherited composite lineage',pin_currentness='EXACT_RETAINED_BYTES_MATCH' if pin_match else 'PIN_MISMATCH',END_runner_eligibility='Role/scope/currentness/coverage must independently match selected runner contract; not automatically authorized by PC03/END projection',selection=False)
 return cid
spec_cids=[]
for i,c in enumerate(plan['cases']):
 if c['CASE_ID'].startswith(('E2-A','E2-N')):spec_cids.append(add(ref(D/(P+'CANONICAL_QUALIFICATION_EXPERIMENT_1.json'),'/cases/'+str(i)),'OTHER',c['CASE_ID']+'_SPECIFICATION',c))
modelids={}
for m in pc03['native_models']:
 cl=m['binding_classification'];typ=m['type']
 classification='SNAPSHOT_ONLY' if typ=='Snapshot' else ('AUTHORIZED_PROSPECTIVE_REPLACEMENT' if 'REPLACEMENT' in cl else 'CANONICAL_NATIVE')
 modelids[m['model_id']]=add(m['source'],classification,m['model_id'],m['native_snapshot'],m['context'])
 if m.get('semantic_oracle'):add(m['semantic_oracle'],'OTHER',m['model_id']+'_SEALED_ORACLE')
for i,pair in enumerate(pc03['independent_boundary_pairs']):add(pair['independent_expected'],'OTHER',pair['native_model_id']+'_INDEPENDENT_ORACLE')
for fam in pc03['mutation_families']:
 add(fam['contract'],'OTHER',fam['family']+'_MUTATION_CONTRACT')
 for code in fam.get('producer_code',[]):add(code,'OTHER',fam['family']+'_LOCAL_CHECKER_CODE')
# Inspect original per-case fixture contract positions without pretending a fixture specification is a native state.
for name in ['E2_PC01_FIXTURES','E2_PC02_FIXTURES','E2_PC03_FIXTURES','E2_PC01_VALIDATION','E2_PC02_VALIDATION','E2_PC03_VALIDATION','E2_PC04_PREFLIGHT']:
 p=D/(P+name+'.json');add(ref(p),'REPORT_ONLY' if 'VALIDATION' in name or 'PREFLIGHT' in name else 'OTHER',name)
# Retained artifacts from all relevant local qualification families, excluding durable namespace and prior diagnostic packages.
roots=[Q/n for n in ['E2_P05_A03_PROSPECTIVE_OCCURRENCE_EXECUTION_1','E2_P05_A04_PROSPECTIVE_ANCESTRY_EXECUTION_1','E2_P05_A05_ALTERNATE_NATIVE_EVIDENCE_1','E2_P05_A06_PROSPECTIVE_REQUEST_WAIT_EXECUTION_1','E2_P04_CANONICAL_EXECUTION_RETRY_1','FINISH_F02_1','FINISH_F03_1','REENTRY_R05_1','P03_PROSPECTIVE_CHECKPOINT_1']]
search_records=[]
for directory in roots:
 if not directory.is_dir():continue
 for p in sorted(directory.rglob('*.json')):
  if any(t in p.relative_to(directory).parts for t in ['docs','sources','source-store','reader-logs']):continue
  # Discover every retained native source and manifest without importing code.
  try:value=read(p)
  except (ValueError,OSError):continue
  cl='REPORT_ONLY';native=None
  if isinstance(value,dict) and value.get('schema')=='PLANNER-BUNDLE-1':cl='OTHER';native='planner-bundle-v1:'+sha(p)
  elif isinstance(value,dict) and value.get('schema')=='PLANNER-SNAPSHOT-1':cl='SNAPSHOT_ONLY';native='planner-snapshot-v1:'+sha(p)
  elif isinstance(value,dict) and value.get('$type')=='ExecutionEvent':cl='OTHER';v=value.get('identity');native=v['namespace']+':'+v['sha256'] if v else None
  elif any(t in p.name.lower() for t in ['oracle','contract','manifest','plan','seal']):cl='OTHER'
  search_records.append(dict(source=ref(p),classification=cl,native_identity=native,local_family=directory.name,not_selected=True))
# Search scope and native coverage discovery are stored separately from candidate role eligibility.
save('retained-artifact-search.json',dict(search_roots=[str(p.relative_to(ROOT)) for p in roots],method='Static parse and exact raw SHA256; no restore, mutation or runner invocation',artifacts=search_records,classification_limit='Wire-type discovery alone does not establish native qualification: discovered bundles/events are OTHER until an exact local qualified source-role association is recorded; Snapshot-only archives remain SNAPSHOT_ONLY'))
for directory in roots:
 for item in search_records:
  if item['local_family']==directory.name and item['classification'] in ['OTHER','REPORT_ONLY'] and len(Path(item['source']['path']).parts)<=len(directory.relative_to(ROOT).parts)+2:
   add(item['source'],item['classification'],directory.name+'_'+Path(item['source']['path']).stem,item['native_identity'])
# Direct phase reader manifests supply exact native paths and oracle pairing candidates.
for directory in [Q/'E2_P04_CANONICAL_EXECUTION_RETRY_1/reader-manifests',Q/'FINISH_F03_1/reader-manifests']:
 if not directory.is_dir():continue
 for p in sorted(directory.glob('*.json')):
  man=read(p);candidatepath=Path(man['path']);candidatepath=candidatepath if candidatepath.is_absolute() else ROOT/candidatepath
  if candidatepath.is_file():add(ref(candidatepath),'QUALIFIED_NATIVE',directory.parent.name+'_'+man['boundary'],man['bundle_id'])
  add(ref(p),'OTHER',directory.parent.name+'_'+man['boundary']+'_READER_MANIFEST')
# Alternate A05 must retain its exact individual authorization, not acquire scope from aggregate END.
a05=D/(P+'E2_P05_A05_ALTERNATE_NATIVE_EVIDENCE_RESULT_1.json')
if a05.is_file():
 alt=read(a05);add(ref(a05),'REPORT_ONLY','A05_AUTHORIZED_ALTERNATE_REPORT')
 for key in ['event_file','event_in_checkpoint','event_in_canonical_descendant']:
  add(alt['native_ancestry'][key],'AUTHORIZED_ALTERNATE_NATIVE_EVIDENCE','A05_ALTERNATE_'+key,alt['native_ancestry']['event_id'],alt['native_ancestry']['scope_lineage_generation'])
# Record obsolete historical qualified implementation pins as STALE references, never as current runtime proof.
for path,pin in read(D/(P+'E2_PC01_VALIDATION.json')).get('input_pins',{}).items():
 if path.startswith('adapter/') and (ROOT/path).is_file():
  add(dict(path=path,pointer='',raw_sha256=pin),'OTHER','HISTORICAL_PC01_RUNTIME_PIN',pin)

for n in ['E2_P05_PC01_END_BINDING_1','E2_P05_PC02_END_BINDING_1','E2_P05_PC03_END_BINDING_1','E2_P05_T01_END_BINDING_1']:
 path=D/(P+n+'.json');add(ref(path),'QUALIFICATION_PROJECTION',n)
save('candidate-source-catalog.json',catalog)
rows=[];ambiguities=[]
def cands(*tokens):return [cid for cid,c in catalog.items() if any(t.lower() in (c['role']+' '+c['source']['path']).lower() for t in tokens)]
def row(i,role,typ,sem,classes,card,order,candidates,state='CONTRACT_AMBIGUITY',prov=None):
 x=dict(INPUT_ID=i,ROLE=role,EXPECTED_TYPE=typ,EXPECTED_SEMANTICS=sem,EXPECTED_SOURCE_CLASS=classes,CARDINALITY=card,ORDERING_SEMANTICS=order,CURRENTNESS='Exact supported native definitions, sources, policy and implementation for each chosen comparison/checkpoint; retained history is not current execution permission',SCOPE='E2-QUALIFICATION-ONLY; any scoped replacement needs its own explicit applicability to this runner position',LINEAGE='Each writer/reader native context retained; equal-semantic comparison members must use compatible exact context, not one invented common lineage',PROVENANCE=prov or [ref(D/(P+'E2_PC04_D01.json')),ref(D/(P+'CANONICAL_QUALIFICATION_EXPERIMENT_1.json'),'/cases/'+str(caseindex))],CANDIDATE_IDS=sorted(set(candidates)),RESOLUTION=state,SELECTED_SOURCE=None)
 rows.append(x)
 if state!='UNIQUE_ELIGIBLE_SOURCE':ambiguities.append(dict(INPUT_ID=i,status=state,reason=i+': '+('Complete aggregate executable/composition is not named by the sealed contract' if i=='RUNNER_EXECUTABLE' else 'Case-specific complete native variant/independent oracle and runner-scope correspondence not pinned' if i.startswith('E2-') else 'Exact '+role+' source/coverage/schema/applicability is not uniquely bound by the original protocol'),candidate_ids=x['CANDIDATE_IDS']))
 return x
nativeclasses=['CANONICAL_NATIVE','QUALIFIED_NATIVE','AUTHORIZED_PROSPECTIVE_REPLACEMENT','AUTHORIZED_ALTERNATE_NATIVE_EVIDENCE']
specclasses=['OTHER'];reportclasses=['REPORT_ONLY','QUALIFICATION_PROJECTION']
row('RUNNER_EXECUTABLE','Full E2-D01 aggregate harness','ReviewedRunnerSource','Implement every declared semantic-state, permutation, process and output comparison position; local subset scripts cannot substitute alone',['OTHER'],'One complete entrypoint or explicit reviewed composition; not pinned','Execution steps and event chronology ordered',cands('LOCAL_CHECKER_CODE'), 'CONTRACT_AMBIGUITY')
row('RUNTIME_PINS','Native implementation/configuration','CodePolicyDefinitionPinSet','Pins for codec/core/model/selector/gates and all applicable native routes must match selected state contracts',['OTHER'],'All applicable modules, exact applicability closure unresolved','Pin membership unordered; binding associations exact',cands('HISTORICAL_PC01_RUNTIME_PIN'), 'CONTRACT_AMBIGUITY')
for n in ['PC01','PC02','PC03','T01']:
 row(n+'_CONTRACT','Required dependency','QualifiedDefinitionCapabilityOracleContract','Exact '+n+' definition/model/proof/authority/phase/persistence/receipt contract at its owned scope',['OTHER','QUALIFICATION_PROJECTION'],'One exact applicable dependency plus native operands per role','Contract field roles fixed; native collections use their own semantics',cands('E2_'+n,n+'_END_BINDING'))
row('TRUSTED_NATIVE_BUNDLES','Persistence operands','PersistenceBundleWithTrustedIdentity','Retained initial/current Snapshot, ordered ledger, source/policy pins, archive and exact bundle identity',nativeclasses,'Each supported checkpoint; exact checkpoint inventory not sealed','Sources unordered; event sequence ordered',list(modelids.values()))
row('POST_SNAPSHOT_ARCHIVES','Historical replay operands','NativeSnapshotArchive','Original event.after_snapshot objects and archived validation values; Snapshot-only source cannot replace a bundle',['SNAPSHOT_ONLY','QUALIFIED_NATIVE'],'One exact archive per required event reference','Native Snapshot sets unordered; validation inputs retain their declared order',list(modelids.values()))
row('SOURCE_BYTES','Native source availability','ArtifactPinAndPinnedBytes','Each current/prefix-available source; future additions excluded from earlier replay',nativeclasses+['OTHER'],'All source dependencies for every selected native checkpoint','Native source sets unordered; temporal availability ordered',list(modelids.values()))
row('POLICY','Selection policy','ExactVersionedPolicyPin','Existing supported selection policy hash/version; no E2 relabeling substitutes bytes',['OTHER'],'Exactly matching policy for each state and comparison equivalence class','Selection-policy rule order ordered',list(modelids.values()))
row('CONTEXT_AND_DEFINITIONS','Scope/generation compatibility','EvaluationContextAndActionDefinitions','Six exact E2 Action versions plus proof/authority/route contracts appropriate to each boundary',nativeclasses,'Each semantic state; no global shared generation inferred','Native Action/authority sets unordered; prerequisite/result edges fixed',list(modelids.values()))
row('ORDERED_EVENT_ANCESTRY','Causal input','ExecutionEventSequence','Exact parent/pre/post/ordinal chain and lifecycle order; reject reordering',nativeclasses,'Complete required event chain per event-bearing checkpoint','STRICTLY_ORDERED',list(modelids.values()))
row('HASH_SEEDS','Process dimension','HashSeedSet','Exactly 0,1,7,101',['OTHER'],'4','Set of test dimensions; per-process scalar fixed',[add(ref(D/(P+'E2_PC04_D01.json'),'/dimensions/hash_seeds'),'OTHER','HASH_SEEDS')],'UNIQUE_ELIGIBLE_SOURCE')
for name in ['actions','sources','goals','proofs','authorities']:
 row('PERMUTE_'+name.upper(),'Presentation dimension','NativeDeclaredUnorderedCollectionPresentations','Original/reversed/rotated presentations for '+name+' while respecting native SET_FIELDS and duplicate rejection',['OTHER'],'All 3 presentations for every applicable field; exact native field applicability must be resolved','UNORDERED_NATIVE_SEMANTICS; tests distinct presentations',cands('E2_PC03_FIXTURES'), 'CONTRACT_AMBIGUITY')
row('PERMUTE_OBJECT_KEYS','Serialization presentation dimension','RecursiveObjectKeyPermutation','Object-key presentation must not alter canonical semantic identity',['OTHER'],'Required; original and permuted object keys; exact exhaustive key permutations not specified','UNORDERED_JSON_OBJECT_KEYS',[add(ref(D/(P+'E2_PC04_D01.json'),'/dimensions/object_key_permutations'),'OTHER','OBJECT_KEY_PERMUTATIONS')],'UNIQUE_ELIGIBLE_SOURCE')
row('WRITER_PROCESS','Process inputs','IndependentWriterInvocationContract','Real writer/process provenance and supported native occurrence inputs; no manufacture from expected oracle',['OTHER','REPORT_ONLY'],'All required state-producing writer processes; count not pinned','Invocation causal actions ordered; independent jobs not declared semantic sequence',cands('writer','execution_driver','process-qualification'))
row('COLD_READER_PROCESS','Process inputs','ColdReaderInvocationAndAllowlist','Fresh independent reader after writer termination; persisted bundle, trusted identity, source/policy bytes and reviewed contracts only',['OTHER','REPORT_ONLY'],'At least 3 independent cold restores per checkpoint per seed (>=12 per checkpoint); per-presentation allocation is unspecified','Reader isolation required; job-list presentation semantics unspecified',cands('reader','process-qualification','E2_PC03_FIXTURES'))
row('ROOTS_AND_STORES','Process environment inputs','RepositoryAndImmutableArtifactStoreRoots','Exact path/source/archive resolution within each independent store, no hidden memory or latest-state fallback',['OTHER'],'One exact resolver context per invocation','Paths exact and source references coherent',cands('READER_MANIFEST'))
comparisons=spec['oracle']['compare']+['branches','rejections']
for name in comparisons:
 row('EXPECTED_'+name.upper(),'Independent expected comparison','IndependentOracle:'+name,'Independent full '+name+' oracle; scalar control/report PASS insufficient',['OTHER'],'Every applicable state/case/checkpoint and equal-semantic comparison','Native unordered collections invariant; branch/policy/causal sequences preserve declared order',cands('ORACLE','E2_PC03_FIXTURES'))
# Every canonical positive and negative case gets separate operand and independent-oracle positions.
case_models={'A01':['ORIGINAL_INITIAL_MODEL'],'A02':['ORIGINAL_INITIAL_MODEL'],'A03':['A03_QUALIFIED_POST_STATE'],'A04':['A04_QUALIFIED_POST_STATE'],'A05':['P03_QUALIFIED_POST_STATE'],'A06':['A06_QUALIFIED_POST_STATE'],'A07':['A06_QUALIFIED_POST_STATE','P04_FINAL_PREEXECUTION'],'A08':['P03_QUALIFIED_POST_STATE','P04_FINAL_PREEXECUTION'],'A09':['P04_POST_A09'],'A10':['P04_POST_A10'],'A11':['P04_POST_A11'],'A12':['P04_POST_A12'],'A13':['P04_ISOLATED_P04_TARGET','P04_POST_ROOT_PROOF','P04_POST_SLOT_PROOF']}
for i,c in enumerate(plan['cases']):
 cid=c['CASE_ID']
 if not cid.startswith(('E2-A','E2-N')):continue
 short=cid[3:];nativeids=[modelids[m] for m in case_models.get(short,[])];related=cands(short,short.replace('A','A0') if len(short)==2 else short)
 contractref=ref(D/(P+'CANONICAL_QUALIFICATION_EXPERIMENT_1.json'),'/cases/'+str(i))
 specid=next(k for k,v in catalog.items() if v['role']==cid+'_SPECIFICATION')
 operand=row(cid+'_OPERANDS','Supported '+('positive' if cid.startswith('E2-A') else 'negative')+' semantic state','NativeStateAndTypedEventOrRejectionOperands',c['INITIAL_STATE']+'; '+c['OPERATION'],nativeclasses,'All supported variants under this case; original contract does not fix a single representative or complete concrete variant list','Native unordered inputs preserved; event/action chronology and policy rules ordered',nativeids+related,'CONTRACT_AMBIGUITY',[contractref])
 operand['CANDIDATE_NATIVE_ROLES']=case_models.get(short,[]);operand['coverage_limit']='Candidate roles supply only their declared local boundary; no coverage equivalence or scope transfer to whole case is claimed'
 oracle=row(cid+'_ORACLE','Independent case oracle','ExpectedFullStateAndNegativeInvariants',c['EXPECTED_STATE']+'; '+c['NEGATIVE_INVARIANTS']+'; '+c['DETERMINISM_REQUIREMENT'],['OTHER'],'One independent exact full oracle for every case variant','Unordered state equality; ordered chronology constraints',related+[specid],'CONTRACT_AMBIGUITY',[contractref])
for i,phase in enumerate(fx['phase_oracle']):
 ids=cands('post-a09' if phase['phase']=='EVIDENCE_RECEIVED' else 'post-a10' if phase['phase']=='EVIDENCE_VALIDATED' else 'post-a11' if phase['phase']=='REENTRY_ELIGIBLE' else 'post-a12' if phase['phase']=='POST_REENTRY' else phase['phase'])
 row('PHASE_'+phase['phase'],'Required PC03 phase operand/oracle pair','NativeBoundaryPlusIndependentOracle','Original phase specification '+json.dumps(phase)+'; old POST_REENTRY RUNNABLE/resume-true is not current deferred-install P04 post-A12 PLAN_DEFECT',nativeclasses+['OTHER'],'Every required phase; concrete current equivalents not inferred','Phase sequence STRICTLY_ORDERED; native sets unordered',ids+[add(ref(D/(P+'E2_PC03_FIXTURES.json'),'/phase_oracle/'+str(i)),'OTHER','PHASE_'+phase['phase'])])
for name,sem in fx['case_mutation_rules'].items():
 row('MUTATION_'+name.upper(),'Designated mutation family','NativeOperandAndSealedMutationContract',sem+'; exact native family and rejection oracle required',nativeclasses+['OTHER'],'Every designated supported mutation, no arbitrary extra mutation','Only declared fields vary; ordered dependencies/chronology retained',cands('MUTATION_CONTRACT','negative','invalidation'))
for i,item in enumerate(fx['invalidation']):
 row('INVALIDATE_'+item['source_role'],'Source-role negative state','NativeInvalidationOperandPlusIndependentOracle',json.dumps(item),nativeclasses+['OTHER'],'Each of six source-role invalidation relations and supported variants','Invalidation membership unordered if declared; original/new event chronology ordered',cands('invalidation')+[add(ref(D/(P+'E2_PC03_FIXTURES.json'),'/invalidation/'+str(i)),'OTHER','INVALIDATE_'+item['source_role'])])
for i,item in enumerate(fx['negative_controls']):
 row('CONTROL_'+str(i).zfill(2),'Required PC03 rejection control','NativeCandidateAndRejectionOracle',item,nativeclasses+['OTHER'],'Each listed control; may overlap canonical N-case but coverage equivalence must be explicit','Native set permutations allowed; causal/process constraints ordered',cands('negative')+[add(ref(D/(P+'E2_PC03_FIXTURES.json'),'/negative_controls/'+str(i)),'OTHER','CONTROL_'+item)])
save('runner-input-matrix.json',rows);save('matrix-ambiguities.json',ambiguities);save('candidate-source-catalog.json',catalog)
eligibility=dict(per_row={r['INPUT_ID']:dict(allowed_classes=r['EXPECTED_SOURCE_CLASS'],candidate_ids=r['CANDIDATE_IDS'],candidate_assessments={cid:('REJECT_CLASS_OR_STALE_PIN' if catalog[cid]['classification']=='STALE' or catalog[cid]['classification'] not in r['EXPECTED_SOURCE_CLASS'] else 'PROVENANCE_ONLY_NOT_NATIVE_OPERAND' if catalog[cid]['classification']=='REPORT_ONLY' else 'CONDITIONAL_EXACT_ROLE_SCOPE_CURRENTNESS_COVERAGE_NOT_YET_BOUND') for cid in r['CANDIDATE_IDS']},resolution=r['RESOLUTION'],native_vs_oracle_separate=True,none_selected=True) for r in rows},class_rules=dict(CANONICAL_NATIVE='Exact native role/version/parent/context pins; canonical tag alone insufficient',QUALIFIED_NATIVE='Local native qualification and exact source/oracle pairing retained; no automatic whole-runner coverage',AUTHORIZED_PROSPECTIVE_REPLACEMENT='Only under the original specific authorization; independent runner-role applicability not yet sealed',AUTHORIZED_ALTERNATE_NATIVE_EVIDENCE='Specific alternate source/consumer authorization only; no continuous native history claim',QUALIFICATION_PROJECTION='May supply documentary scoped mapping/provenance; cannot replace native event-bearing operands',REPORT_ONLY='Can establish retained result/provenance only; cannot replace native state or actual process input',SNAPSHOT_ONLY='Only Snapshot/model/archive roles; not event-bearing bundle or event ancestry',STALE='Rejected for current native applicability; retain as historical provenance',OTHER='Protocol/oracle/code/manifest specifications only in corresponding role'),composite_END_scope_does_not_automatically_apply_to_runner=True,historical_UNPROVEN_preserved=True)
save('source-eligibility.json',eligibility)
constraints=[dict(id='EQUIVALENCE_CONTEXT',rule='Equal-semantic comparison members must match exact scope/lineage/generation/tick and supported definition versions. Separate native contexts may coexist as separate rows; no global common generation is required or synthesized.'),dict(id='NATIVE_ORACLE_PAIR',rule='Each native candidate and expected oracle must name the same boundary/Action/result/mutation semantics; old original PC03 POST_REENTRY cannot silently replace current F03 post-A12.'),dict(id='PREFIX_PINS',rule='Source/policy pins and event parent/pre/post/ordinal must match the native prefix; sources added later are unavailable earlier.'),dict(id='CURRENT_CODE',rule='Chosen runner and native applicable implementation versions must be exactly pinned and independently supported; historical code hash changes are not requalification.'),dict(id='ARCHIVE_CLOSURE',rule='Every required after_snapshot resolves to its original archive; Snapshot-only cannot prove occurrence/ancestry.'),dict(id='PROCESS_INDEPENDENCE',rule='Writer termination before fresh readers, distinct stores/processes where specified, no unlisted hidden inputs, >=3 readers per checkpoint per seed.'),dict(id='SCOPE_MAPPING',rule='PC03 and composite END source choices retain their own authorized roles; E2-D01 reuse requires exact source eligibility, not automatic transfer.'),dict(id='ORACLE_SEPARATION',rule='Independent expectation bytes remain comparison-only and do not produce native execution output.'),dict(id='ALL_CASE_COVERAGE',rule='All supported positive/negative states, cases, phase/mutation/invalidation/rejection obligations included; overlapping local checks need explicit coverage proof.'),dict(id='ORDERING',rule='Native codec.SET_FIELDS defines unordered collections. Event/lifecycle chronology, policy rules and un-reclassified ordered inputs stay ordered.'),dict(id='INVOCATION_ORDER_UNRESOLVED',rule='No complete invocation schema declares aggregate runner argument/list order; do not infer order-insensitivity for the matrix itself.'),dict(id='PROJECTION_GENERATION',rule='No D01 projection generation yet exists or is specified; bind exact agreed source versions later, rather than inheriting another interface generation.')]
save('cross-input-constraints.json',constraints)
# Historical implementation pins are comparisons, not current qualification claims.
old=read(D/(P+'E2_PC01_VALIDATION.json'));current=[]
for path,expected in old.get('input_pins',{}).items():
 if path.startswith('adapter/') and (ROOT/path).is_file():current.append(dict(path=path,qualified_hash=expected,current_hash=sha(ROOT/path),classification='UNCHANGED' if sha(ROOT/path)==expected else 'CHANGED_CURRENT_QUALIFICATION_REQUIRED_FOR_CHOSEN_ROLE'))
currentness=dict(runner_source='NOT_PINNED_BY_CONTRACT; no complete executable can be called CURRENT',local_code=[dict(source=r['source'],status='CURRENT_BYTES_IDENTIFIED_ONLY; scope-specific qualification retained, no global E2-D01 PASS') for r in runner],historical_PC01_runtime_comparison=current,native_source_currentness='Exact retained source-role hashes inspected. Actual applicability and source bytes/definition/archive closure must be evaluated after unambiguous matrix recovery; no restore or qualification rerun here',source_scope='Historical initial model retained in historical role; scoped replacements and current P04 role-specific native sources remain distinct')
save('currentness.json',currentness)
ordering=dict(R05=ref(D/(P+'REENTRY_R05_UNORDERED_PROJECTION_RESULT.json')),R05_semantics=read(D/(P+'REENTRY_R05_UNORDERED_PROJECTION_RESULT.json'))['FIELD_SEMANTICS'],native_authority=ref(ROOT/'adapter/planner/codec.py'),unordered='Only native codec.SET_FIELDS and independently declared unique identity/membership sets',ordered=['event ancestry','lifecycle phases','selection-policy rules','original ordered validation/source input tuples not explicitly reclassified'],runner_input_order='CONTRACT_AMBIGUITY: no complete invocation schema or declaration that aggregate argument/row order is a native unordered collection',matrix_presentation='Recovery row order documentary; that fact does not establish runner invocation argument semantics')
save('ordering-contract.json',ordering)
# Existing full E2-D01 execution search excludes the unrelated durable namespace.
searched=[];hits=[]
for p in sorted(D.glob('*.json')):
 if 'DURABLE_ADMISSION' in p.name:continue
 try:v=read(p)
 except ValueError:continue
 text=p.read_text()
 if 'E2-D01' not in text:continue
 searched.append(ref(p))
 if isinstance(v,dict) and (v.get('case_id')=='E2-D01' or str(v.get('WORK_PACKAGE','')).startswith('E2-D01')):hits.append(dict(source=ref(p),case_id=v.get('case_id'),work_package=v.get('WORK_PACKAGE'),result=v.get('RESULT',v.get('status')),operation_executed=v.get('operation_executed')))
existing=dict(D01_previously_executed='NO',domain='No retained authoritative full E2-D01 execution result found in searched original/planning/result records. Local determinism qualification exists and is not full E2-D01.',result='READY_FOR_LATER_PHASE',input_matrix_used='Protocol dependencies declared; no complete full-runner matrix/result identified',runner_source='No exact complete source named',output='No full E2-D01 output; local PC01/PC02/PC03, R05, prospective readers and P04 seed/permutation checks retained',persistence_replay='Scoped local reader/replay evidence only; not aggregate all-state E2-D01 assurance',current_END_match='NOT_ESTABLISHED',matched_case_records=hits,searched_records=searched,local_results=[ref(D/(P+n+'.json')) for n in ['E2_PC01_VALIDATION','E2_PC02_VALIDATION','E2_PC03_VALIDATION','REENTRY_R05_UNORDERED_PROJECTION_RESULT']],local_P04_reader_contract=ref(Q/'E2_P04_CANONICAL_EXECUTION_RETRY_1/reader-plan.json'))
save('existing-qualification-search.json',existing)
# Exact partial candidate matrices are factored as row -> candidate-ID sets, never selected.
original_family={r['INPUT_ID']:[cid for cid in r['CANDIDATE_IDS'] if any(k in catalog[cid]['role'] for k in ['E2_PC0','SPECIFICATION','ORIGINAL_INITIAL','PHASE_'])] for r in rows}
scoped_family={r['INPUT_ID']:r['CANDIDATE_IDS'] for r in rows}
dossier=dict(schema='E2-D01-INPUT-MATRIX-BOUNDED-DOSSIER-1',DECISION_REQUIRED='YES',DECISION_READY='NO',selection=None,authority_issued=False,decision_subject='Complete runner composition, supported-state coverage and qualification scope of any reuse of retained local sources',candidate_matrices=[dict(id='ORIGINAL_CANONICAL_FAMILY',row_candidate_sets=original_family,complete=False,assurance_consequences='Original canonical fixture/phase definitions retained; old runtime pins and later boundary versions cannot be claimed current; no complete event-bearing negative/state matrix proven'),dict(id='SCOPED_RETAINED_NATIVE_FAMILY',row_candidate_sets=scoped_family,complete=False,assurance_consequences='Includes exact existing prospective/alternate/P03/P04 native sources and local oracles; no global continuous history, no automatic composite END authorization transfer to E2-D01')],DECISION_OPTIONS=['Complete original canonical-role runner matrix while retaining exact version/currentness boundaries','Specify a runner matrix over explicitly authorized scoped native source/oracle pairs without claiming original continuous history','Defer selection until missing executable/coverage/oracle roles are contractually resolved'],options_are_not_ready_for_selection=True,missing_before_decision_ready=['Complete executable composition and input/output schemas','All-case/state/checkpoint variant coverage and oracle associations','Exact row scope applicability and compatibility graph','Current native code/source/archive applicability closure','Complete invocation matrix/order semantics'],authority_class='No native authority issuance established; qualification-scope/contract selection may be required, not automatic execution permission',source_contract=interface)
save('decision-dossier.json',dossier)
preparation=dict(sequence=['recover or explicitly specify complete runner source/coverage/schema','resolve only role-compatible exact native/oracle candidate rows under required qualification scope','construct exact runner invocation manifest with seeds, presentations, independent process and archive/source/policy pins','independently validate complete input coverage and cross-row compatibility','qualify runner projection/output under sealed comparisons in later authorized package','bind E2-D01 -> E2-END and rerun six-interface preflight'],not_executed_here=True,mechanical_rule='Exact role/type/boundary/native identity/policy/code/source/context and scope match; retain all candidates when more than one satisfies these constraints; never choose by file order, recency, name or convenience',INPUT_MATRIX_SELECTION_REQUIRED='YES',SELECTION_CLASSIFICATION='CONTRACT_COMPLETION_AND_FIXTURE_RESOLUTION; QUALIFICATION_SCOPE_DECISION_IF_SCOPED_SOURCES_ARE_SUBSTITUTED',reason='No complete unique matrix is recoverable mechanically; retained candidate families are partial and some eligibility conditions/runner source definitions remain ambiguous, not proven multiple complete legitimate matrices')
save('preparation-contract.json',preparation)
# Preservation and unchanged six-interface frontier.
for name,key in [('PC01','PC01_END_INTERFACE'),('PC02','PC02_END_INTERFACE'),('PC03','PC03_END_INTERFACE'),('T01','T01_END_INTERFACE')]:require(read(D/(P+'E2_P05_'+name+'_END_BINDING_1.json'))[key]=='PASS','PRIOR_PASS')
base=read(OUT/'preservation-baseline.json');changed=[p for p,h in base.items() if not (ROOT/p).is_file() or sha(ROOT/p)!=h];require(not changed,'PRESERVATION')
diff=subprocess.run(['git','diff','--check'],cwd=ROOT,text=True,capture_output=True);require(diff.returncode==0,'DIFF_CHECK')
composite=read(D/(P+'E2_P05_COMPOSITE_END_QUALIFICATION_1.json'));require(composite['STAGE_BINDINGS']=='13/13','STAGE_COUNT')
preservation=dict(P05_STAGE_BINDINGS='13/13',END_INTERFACES_BOUND='4/6',PC01_END='PASS',PC02_END='PASS',PC03_END='PASS',T01_END='PASS',E2_D01_END='BLOCKED',continuation_interface='UNRESOLVED_UNCHANGED',DURABLE_ADMISSION_D01='PASS',E2_D01_IS_DURABLE_ADMISSION_D01='NO',P05_EXECUTED='NO',P06_EXECUTED='NO',N_REAL_SATISFIED='NO',RUNTIME_MODIFIED='NO',NATIVE_STATE_CHANGED='NO',E1_ARTIFACTS_MODIFIED=0,PRODUCTION_EFFECT='NO',RUNNER_EXECUTED='NO',QUALIFICATION_RERUN='NO',INPUT_SELECTION_PERFORMED='NO',END_PROJECTION_CREATED='NO',INSTALL_EVENTS=0,NEW_AUTHORITIES=0,GIT_DIFF_CHECK='PASS',preexisting_files_checked=len(base),E1_files_checked=sum(p.startswith('docs/experiments/E1/') for p in base),changed_preexisting_files=changed)
for k,v in composite.items():
 if v=='UNPROVEN':preservation[k]=v
save('preservation.json',preservation)
result=dict(WORK_PACKAGE='E2-P05-D01-RUNNER-INPUT-MATRIX-RECOVERY',RESULT='PARTIAL',result_domain='Protocol and candidate-obligation recovery complete; exact executable/concrete full input matrix and source eligibility remain contractually ambiguous',E2_D01_IDENTITY=namespace['E2_D01'],DURABLE_ADMISSION_D01_IDENTITY=namespace['DURABLE_ADMISSION_D01'],D01_PURPOSE=case['PURPOSE'],D01_RUNNER=original,D01_RUNNER_SOURCE_RESOLUTION=source_resolution,RUNNER_SOURCE=None,RUNNER_SOURCE_IDENTITY=None,END_CONSUMER_CONTRACT=dict(END_INTERFACE_ID=interface['INTERFACE_ID'],END_CONSUMER=interface['CONSUMER'],END_INPUTS=interface['REQUIRED_INPUT'],EXPECTED_RUNNER='E2-PC04 determinism protocol plus exact current deterministic harness/input matrix, not DURABLE-ADMISSION-D01',EXPECTED_RESULTS=spec['oracle'],EXPECTED_PROCESS=interface['PROCESS'],CURRENTNESS=interface['CURRENTNESS'],SCOPE=interface['SCOPE'],LINEAGE=interface['LINEAGE'],PROVENANCE=interface['PROVENANCE'],recovered_declaration=interface),RUNNER_INPUT_MATRIX=rows,CANDIDATE_SOURCES=catalog,SOURCE_ELIGIBILITY=eligibility,MATRIX_AMBIGUITIES=ambiguities,CROSS_INPUT_CONSTRAINTS=constraints,EXPECTED_RUNNER_OUTPUT=dict(independent_specification=case['EXPECTED_STATE'],comparison_requirements=spec['oracle'],determinism=case['DETERMINISM_REQUIREMENT'],output_serialization='Not fixed by original protocol',END_consumption='Pinned supported comparison/input/process assurance and later full execution evidence remain separate; no future PASS inferred now',independent_values='Original fixture phase expectations and local independently sealed oracles retained; complete concrete per-variant oracle unselected'),EXISTING_D01_QUALIFICATION=existing,CURRENTNESS=currentness,INPUT_MATRIX_SELECTION_REQUIRED='YES',SELECTION_CLASSIFICATION=preparation['SELECTION_CLASSIFICATION'],DECISION_REQUIRED='YES',DECISION_READY='NO',DECISION_OPTIONS=dossier['DECISION_OPTIONS'],DECISION_DOSSIER=ref(OUT/'decision-dossier.json'),NEXT_PACKAGE='E2-P05 E2-D01 runner source/coverage/schema contract completion and bounded matrix-scope resolution; binding materialization only after exact compatible matrix is resolved',P05_EXECUTION_READY='NO',**preservation,evidence={p.name:ref(p) for p in sorted(OUT.glob('*.json'))},recovery_code=ref(OUT/'recover.py'),no_complete_candidate_matrix_claimed=True)
(D/(P+'E2_P05_D01_RUNNER_INPUT_MATRIX_RECOVERY_1.json')).write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
print(json.dumps(dict(result='PARTIAL',matrix_rows=len(rows),ambiguous_rows=len(ambiguities),candidate_roles=len(catalog),retained_artifacts=len(search_records),runner_code_candidates=len(runner),frontier='4/6')))
