"""Read-only operand recovery. No runner imports or Planner operations under test.
Only codec._unwire/_wire (native structural decoding) are invoked.
Unresolved semantic operands fail closed; no expected output is constructed.
"""
import ast
import hashlib
import json
from collections import Counter
from pathlib import Path
from adapter.planner import codec
ROOT=Path(__file__).resolve().parents[4]
OUT=Path(__file__).resolve().parent
Q=ROOT/'docs/plans/qualification';D=ROOT/'docs/plans';P='DETERMINISTIC_PLANNER_V0_1_'
C2=Q/'E2_P05_D01_FIXTURE_ORACLE_CLOSURE_2';OLD=Q/'E2_P05_D01_RUNNER_FIXTURE_CLOSURE_1';CONTRACT=Q/'E2_P05_D01_PROSPECTIVE_MATRIX_CONTRACT_1'
def canon(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def sha(v):return hashlib.sha256(v).hexdigest()
def read(p):return json.loads(Path(p).read_bytes())
def save(n,v):(OUT/n).write_bytes(canon(v)+b'\n')
def pin(p,ptr=''):
 p=Path(p);return {'path':str(p.relative_to(ROOT)),'pointer':ptr,'raw_sha256':sha(p.read_bytes())}
def at(v,p):
 for k in p.split('/')[1:]:v=v[int(k)] if isinstance(v,list) else v[k.replace('~1','/').replace('~0','~')]
 return v
def sid(s):return {'$type':'ArtifactIdentity','kind':{'$enum':'IdentityKind','value':'CONTENT_IDENTITY'},'namespace':'planner-snapshot-v1','sha256':sha(codec.canonical_bytes({'schema':'PLANNER-SNAPSHOT-1','snapshot':codec._wire(codec._unwire(s))}))}
def native_type(v):
 if isinstance(v,dict) and '$type' in v:
  if v['$type']=='SelectionTrace':return 'QUALIFICATION_DTO_NOT_NATIVE'
  return type(codec._unwire(v)).__name__
 if isinstance(v,list):
  for x in v:native_type(x)
  return 'Tuple'
 return type(v).__name__
def qid(v):return 'qualification-D01-operands-v1:'+sha(canon(v))
frozen=read(CONTRACT/'sealed-128-obligations.json')['obligations'];obs={o['OBLIGATION_ID']:o for o in frozen}
refs=read(C2/'revised-operand-audit.json')['references'];dispatch=read(C2/'dispatch-table-v2.json');catalog=read(C2/'fixture-catalog.json');ops=read(OLD/'supported-operation-set.json');index={r['OBLIGATION_ID']:r for r in read(OLD/'partial-construction-index.json')['rows']}
assert len(frozen)==128 and sum(len(r['missing']) for r in refs)==111
seal=read(C2/'runner-v2-source-seal.json')
for name in ['source','helpers','dispatch']:
 p=seal[name];assert sha((ROOT/p['path']).read_bytes())==p['raw_sha256']
# Exact retained transaction inputs; event ancestry is never inferred from reports.
paths={name:D/(P+name+'.json') for name in ['E2_P05_A03_PROSPECTIVE_OCCURRENCE_BUNDLE_1','E2_P05_A04_PROSPECTIVE_ANCESTRY_BUNDLE_1','E2_P05_A06_PROSPECTIVE_REQUEST_WAIT_BUNDLE_1']}
chainpath=Q/'E2_P04_CANONICAL_EXECUTION_RETRY_1/checkpoints/isolated-p04-target/isolated-p04-target.json'
chain=read(chainpath)['bundle'];candidate={}
def offer(case,name,p,ptr,rule):candidate[(case,name)]=(at(read(p),ptr),pin(p,ptr),rule)
for case,inds in {'E2-A05':[1],'E2-A11':[12,13],'E2-A12':[14],'E2-A13':[18,19]}.items():
 for j,i in enumerate(inds):offer(case,'event_'+str(j),chainpath,f'/bundle/events/{i}/result','EXPLICIT_NATIVE_LEDGER_SEQUENCE; consume result operand, not OccurrenceEvent envelope')
# A03 requires acquisition at COLLECT. Existing capsule is before CHECK: candidate is tested and rejected below.
offer('E2-A03','event_0',paths['E2_P05_A03_PROSPECTIVE_OCCURRENCE_BUNDLE_1'],'/bundle/events/1/result','Acquisition SuppliedResult; exact expected_snapshot must match capsule')
offer('E2-A04','supplied',paths['E2_P05_A04_PROSPECTIVE_ANCESTRY_BUNDLE_1'],'/bundle/events/2/result','Native operation consumes externally supplied result; no result generation or replay')
offer('E2-A04','validation_instances',paths['E2_P05_A04_PROSPECTIVE_ANCESTRY_BUNDLE_1'],'/bundle/current/validation_instances','Existing typed validation records are explicit inputs to admit_dossier_materialization; never supply post-Snapshot')
for i in range(2):offer('E2-A06','event_'+str(i),paths['E2_P05_A06_PROSPECTIVE_REQUEST_WAIT_BUNDLE_1'],f'/bundle/events/{i}/result','Explicit ordered READY then WAIT event inputs')
requestpath=Q/'E2_P04_CANONICAL_EXECUTION_RETRY_1/a09-command.json'
offer('E2-A09','request',requestpath,'','Retained EvidenceSourceAdmission command before transaction')
offer('E2-A10','validation_admission',chainpath,'/bundle/events/11/result','Retained ValidationSupportAdmission before validation commit')
classification={'snapshot':'SNAPSHOT','bundle':'PERSISTENCE_BUNDLE','bundle_path':'READER_CONFIG','expected_bundle_identity':'PERSISTENCE_BUNDLE','source_bytes':'SOURCE','pin':'SOURCE','supplied':'RESULT','validation_instances':'OTHER','request':'EVENT','event':'INVALIDATION','event_0':'EVENT','event_1':'EVENT','predicate_id':'AUTHORITY'}
contracts={}
for op,m in ops.items():
 if not m['module']:continue
 p=ROOT/(m['module'].replace('.','/')+'.py');tree=ast.parse(p.read_text());fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==m['entrypoint'])
 args=fn.args;names=[a.arg for a in args.posonlyargs+args.args];defaults={n:ast.dump(v) for n,v in zip(names[-len(args.defaults):] if args.defaults else [],args.defaults)}
 defaults.update({a.arg:ast.dump(v) for a,v in zip(args.kwonlyargs,args.kw_defaults) if v is not None})
 contracts[op]={'NATIVE_ENTRYPOINT':m['module']+'.'+m['entrypoint'],'SOURCE':pin(p),'POSITIONAL_OPERANDS':names,'KEYWORD_ONLY':[a.arg for a in args.kwonlyargs],'NATIVE_DEFAULTS':defaults,'INPUT_TYPE':m['input_type'],'OUTPUT_TYPE':m['output_type'],'DOCSTRING':ast.get_docstring(fn),'OPERATION_EXECUTED':False}
records={o['OBLIGATION_ID']:{'OBLIGATION_ID':o['OBLIGATION_ID'],'CASE_ID':o['CASE_ID'],'DISPATCH_ID':index[o['OBLIGATION_ID']]['RUNNER_DISPATCH_ID'],'VARIANTS':[],'COMPLETE':False} for o in frozen}
gaps=[];resolutions=[];cross=[];alloperands=[]
for ref in refs:
 ob=obs[ref['OBLIGATION_ID']];cid=ob['CASE_ID'];entry=catalog[ref['CAPSULE_ID']];src=ROOT/entry['artifact']['path'];assert sha(src.read_bytes())==entry['artifact']['raw_sha256']
 packet=read(src);content=packet['canonical_content'];s=content['subject'];normalized=codec._wire(codec._unwire(s));stateid=sid(s);available=content['arguments'];steps=dispatch[ref['DISPATCH_ID']].get('variant_paths',{}).get(ref['STATE_VARIANT_ID'],dispatch[ref['DISPATCH_ID']]['steps'])
 context=normalized['context']; checks=[];bound={};recovered={}; local=[]
 for gap in ref['missing']:
  name=gap['operand'];step=steps[gap['step']];op=step['operation_id'];types=ops[op]['input_type'].split(',');positions=[i for i,b in enumerate(step['args']) if b.get('fixture_field')==name];typ=types[positions[0]] if positions and positions[0]<len(types) else 'Native signature operand'
  g={'OBLIGATION_ID':ob['OBLIGATION_ID'],'CASE_ID':cid,'DISPATCH_ID':ref['DISPATCH_ID'],'CAPSULE_ID':ref['CAPSULE_ID'],'STATE_VARIANT_ID':ref['STATE_VARIANT_ID'],'STEP':gap['step'],'OPERAND_NAME':name,'EXPECTED_TYPE':typ,'EXPECTED_IDENTITY_DOMAIN':{'snapshot':'CONTENT_IDENTITY/planner-snapshot-v1','expected_bundle_identity':'CONTENT_IDENTITY/planner-bundle-v1','predicate_id':'PredicateId (semantic reference; not ArtifactIdentity)'}.get(name,typ+' native model domain'),'SEMANTIC_ROLE':classification.get(name,'OTHER'),'REQUIRED_BY_ENTRYPOINT':contracts.get(op,{}).get('NATIVE_ENTRYPOINT'),'REQUIREMENT':'REQUIRED_EXPLICIT','INITIAL_GAP':'fixture_field absent from sealed capsule arguments','STATUS':'UNRESOLVED','CURRENT_GAP':'No exact applicable source bound','SOURCE_ARTIFACT':None,'SOURCE_IDENTITY':None,'SOURCE_TYPE':None,'SCOPE':context['scope'],'LINEAGE':context['lineage'],'PROVENANCE':packet['provenance'],'CURRENTNESS':'NOT_ESTABLISHED'}
  cand=candidate.get((cid,name))
  if cand:
   v,p,rule=cand;g['CANDIDATE_SOURCE']=p
   # Only step zero precondition is compared with pre-state. Later parents are explicit retained event chain links.
   parent=v.get('expected_snapshot') if isinstance(v,dict) else None
   okay=(not parent or gap['step']!=0 or parent==stateid)
   if okay:
    nt=native_type(v);recovered[name]=(v,p,rule);g.update(STATUS='RESOLVED',CURRENT_GAP=None,SOURCE_ARTIFACT=p,SOURCE_IDENTITY=qid(v),SOURCE_TYPE=nt,CURRENTNESS='PIN_MATCH; exact retained operand and capsule pre-state, native runtime pinned',DERIVATION_RULE=rule)
   else:g['CURRENT_GAP']='RETAINED_OPERAND_PRESTATE_MISMATCH';g['PRE_STATE_IDENTITY']=stateid;g['CANDIDATE_EXPECTED_SNAPSHOT']=parent
  if cid=='E2-A09' and name=='source_bytes':
   payload=Q/'E2_P04_CONTINUATION_INPUT_CLOSURE_1/native-payload.json';rq=read(requestpath);pins=rq.get('source',rq.get('pin'))
   # Source bytes stay raw; no JSON round-trip or admission operation.
   def findpins(x):
    if isinstance(x,dict):
     if x.get('$type')=='ArtifactPin':yield x
     for v in x.values():yield from findpins(v)
    elif isinstance(x,list):
     for v in x:yield from findpins(v)
   ps=list(findpins(rq));matches=[p for p in ps if p['identity']['sha256']==sha(payload.read_bytes())]
   if len(matches)==1:
    v={'representation':'RAW_BYTES_FILE_MAP','entries':[{'key':matches[0]['path'],'source':pin(payload),'sha256':sha(payload.read_bytes())}]};recovered[name]=(v,pin(payload),'Read exact raw bytes; map by request ArtifactPin.path')
    g.update(STATUS='RESOLVED',CURRENT_GAP=None,SOURCE_ARTIFACT=pin(payload),SOURCE_IDENTITY=qid(v),SOURCE_TYPE='SourceBytes descriptor',CURRENTNESS='RAW_SHA256_MATCHES_REQUEST_PIN',DERIVATION_RULE='Read raw file bytes under exact pin.path; do not parse/reserialize')
  if name in ('bundle_path','expected_bundle_identity') and not (cid=='E2-N11' or 'MUTATION_' in ob['ORIGINAL_INPUT_ID'] or 'CONTROL_' in ob['ORIGINAL_INPUT_ID']):
   base=content.get('bundle');sp=content['source'];p=ROOT/sp['path'];doc=read(p)
   if base and doc.get('bundle')==base:
    events=base.get('events',[]);archive=[p.parent/('event-'+e['identity']['sha256']+'.json') for e in events]
    exact=all(a.is_file() and a.read_bytes()==codec.canonical_bytes(e) for a,e in zip(archive,events))
    if exact:
     ident={'$type':'ArtifactIdentity','kind':{'$enum':'IdentityKind','value':'CONTENT_IDENTITY'},'namespace':'planner-bundle-v1','sha256':sha(p.read_bytes())};v=str(p.relative_to(ROOT)) if name=='bundle_path' else ident;recovered[name]=(v,pin(p),'Exact sealed capsule source; raw hash binds trusted identity; ledger artifacts compared without replay')
     g.update(STATUS='RESOLVED',CURRENT_GAP=None,SOURCE_ARTIFACT=pin(p),SOURCE_IDENTITY=ident,SOURCE_TYPE='Path' if name=='bundle_path' else 'ArtifactIdentity',CURRENTNESS='PIN_AND_LEDGER_ARTIFACT_BYTES_MATCH; restore not executed',DERIVATION_RULE='Pinned source raw bytes -> planner-bundle-v1 identity; no bundle_id/replay invocation')
    else:g['CURRENT_GAP']='SEALED_BUNDLE_SOURCE_HAS_NO_COMPLETE_SIBLING_LEDGER_ARCHIVE';g['MISSING_EVENT_FILES']=[str(a.relative_to(ROOT)) for a in archive if not a.is_file()]
   elif cid=='E2-A14':g['CURRENT_GAP']='SNAPSHOT_ONLY_CAPSULE; SAVE_RESULT_PATH_AND_IDENTITY_NOT_REFERENCED_BY_V2_DISPATCH'
  if name=='bundle' and cid=='E2-A14':g['CURRENT_GAP']='SNAPSHOT_ONLY_CAPSULE; NO_PERSISTENCE_BUNDLE_OR_SEALED_PURE_CONSTRUCTION_RULE'
  if name in ('bundle_path','expected_bundle_identity') and (cid=='E2-N11' or ob['ORIGINAL_INPUT_ID'] in ['MUTATION_PERSISTENCE','CONTROL_06','CONTROL_07']):g['CURRENT_GAP']='EXACT_DEFERRED_BUNDLE_TAMPER_DESCRIPTOR_AND_TRUSTED_PRETAMPER_IDENTITY_NOT_SEALED'
  if name=='pin' and g['STATUS']=='UNRESOLVED':g['CURRENT_GAP']='EXACT_SOURCE_ROLE_PIN_OR_DEFERRED_SOURCE_MUTATION_NOT_SEALED; one arbitrary pin cannot cover complete source role'
  if name=='request' and g['STATUS']=='UNRESOLVED' and cid!='E2-A09':g['CURRENT_GAP']='CONTROLLED_MUTATION_DESCRIPTOR_NOT_BOUND; unchanged A09 request would erase negative dimension'
  if name=='predicate_id' and g['STATUS']=='UNRESOLVED':g['CURRENT_GAP']='EXACT_AUTHORITY_MUTATION_TARGET_AND_APPLICABILITY_NOT_SEALED; semantic variants share baseline'
  if name=='event' and g['STATUS']=='UNRESOLVED':
   target=None;selector=None
   if cid=='E2-N04' and len(normalized.get('receipt_admissions',[]))==1:
    receipt=normalized['receipt_admissions'][0];entityid=receipt['artifact'];selector='unique receipt_admissions[0].artifact -> entities.id -> provenance.identity'
    if ref['STATE_VARIANT_ID'].endswith(':ATTESTOR_INVALIDATED'):
     predicates=[p for p in normalized['predicates'] if p['id']==receipt['authentication']]
     if len(predicates)==1:entityid=predicates[0]['entity'];selector='unique receipt authentication -> predicates.id -> predicate.entity -> entities.id -> provenance.identity'
    entities=[e for e in normalized['entities'] if e['id']==entityid]
    if len(entities)==1:target=entities[0]['provenance']['identity']
   elif ob['ORIGINAL_INPUT_ID']=='INVALIDATE_GRANT':
    actions=[a for a in normalized['actions'] if a['id']['value']=='E2-REENTER']
    predicates=[p for p in normalized['predicates'] if actions and p['id']==actions[0].get('authority')]
    entities=[e for e in normalized['entities'] if predicates and e['id']==predicates[0]['entity']]
    if len(actions)==len(predicates)==len(entities)==1:target=entities[0]['provenance']['identity'];selector='E2-REENTER.authority -> unique predicate.entity -> entity.provenance.identity'
   elif ob['ORIGINAL_INPUT_ID']=='INVALIDATE_EXTERNAL_ROUTE':
    routes=[r for gate in normalized['external_gates'] for r in gate['resolution_contracts']]
    if len(routes)==1:target=routes[0]['provenance']['identity'];selector='unique native ExternalResolutionContract.provenance.identity'
   if target:
    v={'$type':'SourceInvalidation','changed':[target],'expected_snapshot':stateid};native_type(v)
    dest=OUT/('descriptor-'+sha(canon([ref['STATE_VARIANT_ID'],name]))+'.json');dest.write_bytes(canon(v)+b'\n');p=pin(dest)
    rule='Pure descriptor only: '+selector+'; expected_snapshot from sealed pre-state canonical bytes; no invalidation applied'
    recovered[name]=(v,p,rule);g.update(STATUS='RESOLVED',CURRENT_GAP=None,SOURCE_ARTIFACT=p,SOURCE_IDENTITY=qid(v),SOURCE_TYPE='SourceInvalidation descriptor',CURRENTNESS='Input source identity derived from exact sealed capsule boundary; not applied',DERIVATION_RULE=rule,DERIVATION_SOURCE=entry['artifact'],TARGET_IDENTITY=target)
   else:g['CURRENT_GAP']='EXACT_INVALIDATION_TARGET_SOURCE_IDENTITY_NOT_SEALED; baseline alone does not establish role'

  gaps.append(g)
  if g['STATUS']=='RESOLVED':resolutions.append(g)
  local.append(g)
 invocation=[]
 for si,step in enumerate(steps):
  op=step['operation_id']; operands=[];contract=contracts.get(op);names=contract['POSITIONAL_OPERANDS'] if contract else []
  for ai,binding in enumerate(step['args']):
   rec={'POSITION':ai,'PARAMETER':names[ai] if ai<len(names) else 'qualification_metadata','BINDING':binding,'STATUS':'UNRESOLVED'}
   if 'fixture_field' in binding:
    field=binding['fixture_field']
    if field in available:
     v=available[field];nt=native_type(v);rec.update(STATUS='STRUCTURALLY_LOADED',VALUE=v,NATIVE_TYPE=nt,SOURCE=pin(src,'/canonical_content/arguments/'+field),IDENTITY=qid(v),DERIVATION_RULE='Exact sealed capsule argument; no native operation')
    elif field in recovered:
     v,p,rule=recovered[field];rec.update(STATUS='RESOLVED_RETAINED_INPUT',VALUE=v,NATIVE_TYPE=native_type(v) if not (isinstance(v,dict) and v.get('representation')) else 'SourceBytes descriptor',SOURCE=p,IDENTITY=qid(v),DERIVATION_RULE=rule)
   elif 'prior_result' in binding:
    valid=binding['prior_result'] in bound;rec.update(STATUS='SEALED_FUTURE_DATAFLOW' if valid else 'INVALID_DATAFLOW',DERIVATION_RULE='At execution only, consume preceding native return via exact selector; no pre-supplied future result',SOURCE=pin(C2/'dispatch-table-v2.json'),IDENTITY=qid(binding));checks.append({'check':'PRIOR_RESULT_PRECEDES_CONSUMER','status':'PASS' if valid else 'FAIL','step':si})
   elif 'literal' in binding:rec.update(STATUS='NATIVE_LITERAL',VALUE=binding['literal'],NATIVE_TYPE=native_type(binding['literal']),SOURCE=pin(C2/'dispatch-table-v2.json'),IDENTITY=qid(binding))
   elif 'context_field' in binding:
    field=binding['context_field'];rec.update(STATUS='PATH_DESCRIPTOR_BOUND',VALUE=str(ROOT) if field=='source_root' else '/tmp/prospective-d01/'+sha(canon([ob['OBLIGATION_ID'],ref['STATE_VARIANT_ID']]))+'/store',SOURCE=pin(C2/'dispatch-table-v2.json'),DERIVATION_RULE='Repository root / per-row isolated future store, no store created',IDENTITY=qid([field,ob['OBLIGATION_ID'],ref['STATE_VARIANT_ID']]))
   if 'VALUE' in rec and len(canon(rec['VALUE']))>2048:
    rec['VALUE_REFERENCE']=rec['SOURCE'];rec['VALUE_REPRESENTATION']='Exact pinned JSON pointer; value structurally loaded by this audit';del rec['VALUE']
   operands.append(rec);alloperands.append(rec)
  bound[step['bind_result_as']]=op
  invocation.append({'STEP':si,'OPERATION_ID':op,'NATIVE_ENTRYPOINT':contract['NATIVE_ENTRYPOINT'] if contract else None,'ENTRYPOINT_CONTRACT':contract,'POSITIONAL_OPERANDS':operands,'KWARGS':step['kwargs'],'SEALED_NATIVE_DEFAULTS':step.get('sealed_native_defaults',{}),'BIND_RESULT_AS':step['bind_result_as']})
 # All operands resolving by field name is insufficient for compatible mutations, archive closure and native defaults.
 pending=[g for g in local if g['STATUS']!='RESOLVED'];checks.append({'check':'INITIAL_GAP_REFERENCES_RESOLVED','status':'PASS' if not pending else 'FAIL','count':len(pending)})
 checks.append({'check':'NATIVE_STRUCTURAL_SNAPSHOT','status':'PASS','identity':stateid})
 checks.append({'check':'EXPECTED_PARENT_FROM_INPUT_ONLY','status':'PASS','head':(content.get('bundle') or {}).get('events',[])[-1]['identity'] if (content.get('bundle') or {}).get('events') else None})
 # Relative short source paths need a proven root, never guessed from file name.
 def provs(x):
  if isinstance(x,dict):
   if x.get('$type')=='Provenance':yield x
   for v in x.values():yield from provs(v)
  elif isinstance(x,list):
   for v in x:yield from provs(v)
 missingpaths=sorted({p['path'] for p in provs(s) if p.get('path') and not (ROOT/p['path']).is_file()})
 checks.append({'check':'SOURCE_ROOT_FILE_APPLICABILITY','status':'FAIL' if missingpaths else 'PASS_PATHS_ONLY','missing':missingpaths})
 variant={'CAPSULE_ID':ref['CAPSULE_ID'],'CAPSULE_SOURCE':entry['artifact'],'STATE_VARIANT_ID':ref['STATE_VARIANT_ID'],'SCOPE':context['scope'],'LINEAGE':context['lineage'],'GENERATION':context['generation'],'PROVENANCE':packet['provenance'],'CURRENTNESS':{'runtime_contracts_pinned':True,'case_applicability':'NOT_COMPLETE'},'INVOCATION_STEPS':invocation,'COMPLETE':False,'MISSING_REFERENCES':len(pending),'READER_MODE':index[ob['OBLIGATION_ID']]['READER_MODE'],'PERMUTATION_MODE':index[ob['OBLIGATION_ID']]['PERMUTATION_MODE'],'MUTATION_DESCRIPTOR_STATUS':'NOT_APPLIED; sealed exact target required where applicable','VALIDATION_STATUS':'PARTIAL_STATIC_NO_CASE_OPERATION'}
 records[ob['OBLIGATION_ID']]['VARIANTS'].append(variant);cross.append({'OBLIGATION_ID':ob['OBLIGATION_ID'],'STATE_VARIANT_ID':ref['STATE_VARIANT_ID'],'CHECKS':checks,'COMPLETE_CROSS_OPERAND_VALIDATION':'NOT_PASS'})
assert len(gaps)==111 and len(records)==128
ordered=[records[o['OBLIGATION_ID']] for o in frozen]
classification_counts=dict(Counter(g['SEMANTIC_ROLE'] for g in gaps));final=sum(g['STATUS']!='RESOLVED' for g in gaps)
save('initial-111-operand-inventory.json',{'INITIAL_COUNT':111,'ROWS':gaps})
save('entrypoint-contracts.json',contracts)
save('operand-source-and-derivation-inventory.json',{'RESOLVED_REFERENCE_OCCURRENCES':len(resolutions),'ROWS':resolutions,'UNRESOLVED':final,'CLASSIFICATION':classification_counts,'case_operations_executed':0})
save('invocation-records.partial.json',{'ROWS':ordered,'ROW_COUNT':128,'COMPLETE_ROWS':0,'MISSING_INITIAL_REFERENCE_OCCURRENCES':final,'NOTE':'Draft records, not complete invocations; unresolved scopes/mutations/archives are not promoted'})
save('cross-operand-validation.json',{'ROWS':cross,'STATUS':'PARTIAL_NOT_PASS'})
# Independent coverage reconstruction does not claim independent semantic binding reconstruction.
expected={(o['OBLIGATION_ID'],e['state_variant_id']) for o in frozen for e in catalog.values() if e['state_variant_id'] in index[o['OBLIGATION_ID']]['STATE_VARIANT_IDS']}
actual={(r['OBLIGATION_ID'],v['STATE_VARIANT_ID']) for r in ordered for v in r['VARIANTS']};assert expected==actual
save('independent-reconstruction.json',{'COVERAGE_COMPARISON':'PASS','VARIANT_INVOCATION_COUNT':len(actual),'FULL_SEMANTIC_RECONSTRUCTION':'NOT_PASS_UNRESOLVED_OPERANDS','ROW_COUNT':128})
# Fail-closed static source/coverage/identity guards; no semantic execution.
class Reject(ValueError):pass
def validate(rows):
 if len(rows)!=128 or {r['OBLIGATION_ID'] for r in rows}!={o['OBLIGATION_ID'] for o in frozen}:raise Reject('COVERAGE')
 for row in rows:
  if row['DISPATCH_ID']!=index[row['OBLIGATION_ID']]['RUNNER_DISPATCH_ID']:raise Reject('DISPATCH')
  for v in row['VARIANTS']:
   e=catalog.get(v['CAPSULE_ID'])
   if not e or v['STATE_VARIANT_ID']!=e['state_variant_id'] or v['CAPSULE_SOURCE']!=e['artifact']:raise Reject('CAPSULE_DOMAIN_OR_PIN')
   if v['COMPLETE']:raise Reject('INCOMPLETE_ROW_PROMOTED')
 return True
from copy import deepcopy
validate(ordered);neg=[]
for name,mutate in [('missing row',lambda r:r.pop()),('duplicate row',lambda r:r.__setitem__(0,deepcopy(r[1]))),('wrong dispatch',lambda r:r[0].update(DISPATCH_ID='WRONG')),('wrong variant',lambda r:r[0]['VARIANTS'][0].update(STATE_VARIANT_ID='WRONG')),('wrong capsule',lambda r:r[0]['VARIANTS'][0].update(CAPSULE_ID='WRONG')),('wrong source pin',lambda r:r[0]['VARIANTS'][0]['CAPSULE_SOURCE'].update(raw_sha256='0'*64)),('incomplete promoted',lambda r:r[0]['VARIANTS'][0].update(COMPLETE=True))]:
 r=deepcopy(ordered);mutate(r)
 try:validate(r)
 except Reject as exc:neg.append({'case':name,'status':'REJECTED','reason':str(exc)})
 else:raise AssertionError(name)
save('operand-negatives.json',{'STATIC_GUARDS':'PASS','CASES':neg,'REQUESTED_SEMANTIC_NEGATIVE_SUITE':'NOT_COMPLETE; no completed invocation validator','NATIVE_OPERATIONS_EXECUTED':0})
save('oracle-handoff.preparation.json',{'STATUS':'NOT_READY_NOT_A_COMPLETE_HANDOFF','EXPECTED_VALUES_POPULATED':False,'ROWS':[{'OBLIGATION_ID':o['OBLIGATION_ID'],'INVOCATION_RECORD':{'path':str((OUT/'invocation-records.partial.json').relative_to(ROOT)),'pointer':'/ROWS/'+str(i)},'OUTPUT_SCHEMA':pin(OLD/'normalization-and-output-schema.json'),'INDEPENDENT_ORACLE_SOURCE_CLASSIFICATION':['AUTHORITATIVE_CONTRACT','CANONICAL_IDENTITY_RULE','NEGATIVE_REJECTION_CONTRACT'] if o['CASE_ID'].startswith('E2-N') else ['AUTHORITATIVE_CONTRACT','CANONICAL_IDENTITY_RULE','SNAPSHOT_RULE','LEDGER_RULE','PERSISTENCE_RULE','REPLAY_RULE'],'FIELDS_REQUIRING_EXPECTED_VALUES':read(OLD/'normalization-and-output-schema.json')['fields'],'EXPECTED_VALUES':'NOT_POPULATED','READY':False} for i,o in enumerate(frozen)]})
summary={'WORK_PACKAGE':'E2-P05-D01-OPERAND-CLOSURE-3','RESULT':'PARTIAL','INITIAL_MISSING_OPERANDS':111,'FINAL_MISSING_OPERANDS':final,'RESOLVED_OPERAND_REFERENCES':len(resolutions),'INVOCATION_RECORDS':'0/128 complete; 128 draft obligation records','OPERAND_CLASSIFICATION':classification_counts,'SOURCE_RESOLUTION':'PARTIAL; exact retained source pins for resolved references','DERIVED_OPERANDS':'Pinned raw-byte and canonical structural identities only; no native case calls','CROSS_OPERAND_CONSISTENCY':'NOT_PASS','INVOCATION_STATIC_PREFLIGHT':'NOT_PASS_UNRESOLVED_OPERANDS_AND_APPLICABILITY','INDEPENDENT_OPERAND_RECONSTRUCTION':'COVERAGE_PASS; FULL_SEMANTIC_RECONSTRUCTION_NOT_PASS','OPERAND_NEGATIVE_SUITE':'7 static guards PASS; requested semantic suite NOT_COMPLETE','D01_INVOCATION_OPERANDS_COMPLETE':'NO','ORACLE_HANDOFF_MANIFEST':'NOT_READY; preparation only','FULL_OUTPUT_ORACLES':'0/128','PROSPECTIVE_D01_MATRIX_CONSTRUCTION_READY':'NO','PROSPECTIVE_D01_SCOPE_DECISION_READY':'NO','PROSPECTIVE_D01_EXECUTION_READY':'NO','END_INTERFACES_BOUND':'4/6','E2_D01_END':'BLOCKED','P05_EXECUTION_READY':'NO','QUALIFICATION_CASES_EXECUTED':0,'P05_EXECUTED':'NO','P06_EXECUTED':'NO','NATIVE_STATE_CHANGED':'NO','E1_ARTIFACTS_MODIFIED':0,'PRODUCTION_EFFECT':'NO','ORIGINAL_D01_COMPLETE_INPUT_MATRIX':'UNRECOVERED','AUTHORITY_ISSUED':0,'HISTORICAL_UNPROVEN_LABELS_PRESERVED':True,'ARTIFACTS':{n:pin(OUT/n) for n in ['initial-111-operand-inventory.json','entrypoint-contracts.json','operand-source-and-derivation-inventory.json','invocation-records.partial.json','cross-operand-validation.json','independent-reconstruction.json','operand-negatives.json','oracle-handoff.preparation.json']}}
save('summary.json',summary)
print(json.dumps({k:summary[k] for k in ['RESULT','INITIAL_MISSING_OPERANDS','FINAL_MISSING_OPERANDS','RESOLVED_OPERAND_REFERENCES','INVOCATION_RECORDS']}))
