"""Pure fixture authoring and read-only structural decoding; no case execution."""
import ast
from copy import deepcopy
import hashlib
import json
from pathlib import Path
from adapter.planner import codec as c
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;D=R/'docs/plans';Q=D/'qualification';P='DETERMINISTIC_PLANNER_V0_1_'
OLD=Q/'E2_P05_D01_RUNNER_FIXTURE_CLOSURE_1';CONTRACT=Q/'E2_P05_D01_PROSPECTIVE_MATRIX_CONTRACT_1'
def read(p):return json.loads(Path(p).read_bytes())
def canonical(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def hashfile(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def ref(p,pointer=''):return dict(path=str(Path(p).relative_to(R)),pointer=pointer,raw_sha256=hashfile(p))
def identity(v):return 'qualification-prospective-D01-fixture-content-v1:'+hashlib.sha256(canonical(v)).hexdigest()
def save(n,v):
 p=O/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(canonical(v)+b'\n')
def check(x,m):
 if not x:raise ValueError(m)
source_index=read(OLD/'partial-construction-index.json')['rows'];oldcatalog=read(OLD/'fixture-catalog.json')
missing=[v['variant'] for v in read(OLD/'state-variant-closure.json') if v['status']!='CONCRETE_STRUCTURAL_INPUT_MATERIALIZED'];check(len(missing)==10,'TEN_MISSING')
govpath=D/(P+'EVIDENCE_E06_GOVERNED_UNKNOWN_SNAPSHOT.json');gov=read(govpath)['snapshot']
startpath=Q/'P03_PROSPECTIVE_CHECKPOINT_1/mainline-start.json';start=read(startpath)['bundle']
checkpointpath=D/(P+'P03_PROSPECTIVE_CHECKPOINT_BUNDLE_1.json');checkpoint=read(checkpointpath)['bundle']
rootpath=Q/'E2_P04_CANONICAL_EXECUTION_RETRY_1/checkpoints/post-root-proof/post-root-proof.json';root=read(rootpath)['bundle']
# Same native context for independent human branch; controlled initial-state construction,
# not a rollback of a committed ledger or simulation of a native transition.
scopedgov=deepcopy(checkpoint['current']);check(len(scopedgov['evidence_requirements'])==1,'UNIQUE_REQUIREMENT')
scopedgov['evidence_requirements'][0]['rule_known']=False
requirements=[];packets={}
for vid in missing:
 consumers=[row for row in source_index if vid in row['STATE_VARIANT_IDS']]
 cid=vid.split(':')[1];tag=vid.split(':')[-1]
 basepath=None;bundle=None;args={};changes=[];kind='RETAINED_NATIVE_SOURCE';reason=''
 if cid=='E2-A05':basepath=startpath;bundle=deepcopy(start);state=deepcopy(start['current']);reason='Qualified ready decision prestate, no recorded choice; not checkpoint after choice'
 elif cid=='E2-A14':basepath=govpath;state=deepcopy(gov);reason='Exact retained governed-unknown initial model, rule_known=false and native resolution correspondence'
 elif cid=='E2-A15':basepath=rootpath;bundle=deepcopy(root);state=deepcopy(root['current']);reason='Accepted knowledge/proof/authority input; six-source invalidation operand closure remains separately required'
 elif cid=='E2-A16':basepath=govpath;state=deepcopy(gov);reason='Exact governed-unknown pre-invalidation state; invalidation event not applied during construction'
 elif cid=='E2-N01':basepath=govpath;state=deepcopy(gov);state['external_gates'][0]['resolution_contracts']=[];changes=['external_gates[E2-GATE].resolution_contracts'];kind='CONTROLLED_MUTATION';reason='Remove only governing acquisition route; retain unknown obligation and all remaining native fields'
 elif cid=='E2-N16':
  basepath=checkpointpath;state=deepcopy(scopedgov);kind='PURE_DERIVATION'
  if tag=='HUMAN_FRONTIER':
   # Re-declare an independent initial scenario from same-scope ready decision objects.
   check(start['current']['context']==state['context'],'HUMAN_CONTEXT')
   state=deepcopy(start['current']);state['evidence_requirements'][0]['rule_known']=False
   reason='Ready human decision plus governed-unknown route in same exact native context; no committed history relabeled'
   changes=['initial scenario readiness inputs','evidence_requirements.rule_known']
  else:
   action=deepcopy(next(a for a in state['actions'] if a['id']['value']=='E2-CHECK'))
   action['id']['value']='PROSPECTIVE-D01-INDEPENDENT';action['prerequisites']=[];action['requirements']=[];action['authority']=None;action['accepted_inventory']=[]
   state['actions'].append(action);state['statuses'].append({'$type':'ActionStatus','id':action['id'],'state':{'$enum':'ActionState','value':'ACTION_ELIGIBLE'}})
   changes=['actions[PROSPECTIVE-D01-INDEPENDENT]','statuses[PROSPECTIVE-D01-INDEPENDENT]','initial requirement.rule_known']
   reason='Explicit independent eligible non-effecting branch; original governed-unknown branch remains'
   if tag=='FACTUAL_BLOCKED_FRONTIER':
    rid={'$type':'ConditionId','value':'PROSPECTIVE-D01-FACT-ROOT'}
    state['roots'].append({'$type':'RootCondition','id':rid,'state':{'$enum':'ConditionState','value':'UNRESOLVED'},'evidence':[]})
    state['boundaries'].append({'$type':'ControlBoundary','id':{'$type':'GateId','value':'PROSPECTIVE-D01-FACT'},'kind':{'$enum':'BoundaryKind','value':'EXTERNAL_FACT'},'actions':[action['id']],'provenance':action['source']})
    state['goals'].append({'$type':'Goal','target':rid,'entry_actions':[action['id']],'provenance':action['source'],'failure':None,'recovery':[]})
    changes+=['independent factual root','boundary','goal'];reason='Frozen N16 expressly permits factual frontier branch with native MIXED_WAIT precedence'
 elif cid=='PHASE_PRE_EXTERNAL':basepath=startpath;bundle=deepcopy(start);state=deepcopy(start['current']);reason='Exact post-preparation/pre-choice phase; human decision ready'
 elif cid=='PHASE_POST_REENTRY':basepath=rootpath;bundle=deepcopy(root);state=deepcopy(root['current']);reason='Post-reentry and admitted proof-support before FINISH; current source contract distinguishes this from immediate unsupported post-A12'
 else:raise ValueError('UNKNOWN_MISSING_VARIANT')
 normalized=c._wire(c._unwire(state)) # Structural codec only, not validate_model/recompute.
 args={'snapshot':normalized}
 if bundle:args['bundle']=deepcopy(bundle)
 content=dict(subject=normalized,bundle=deepcopy(bundle),arguments=args,mutation_fields=changes,source=ref(basepath),scope=normalized['context']['scope'],lineage=normalized['context']['lineage'],generation=normalized['context']['generation'])
 fid='D01-FIXTURE:'+vid.split('D01-VARIANT:',1)[1]
 packet=dict(schema='PROSPECTIVE-D01-CONSTRUCTION-FIXTURE-2',fixture_id=fid,role_ids=sorted({next(p['FIXTURE'] for p in read(CONTRACT/'planned-realization-matrix.json')['rows'] if p['OBLIGATION_ID']==row['OBLIGATION_ID']) for row in consumers}),state_variant_id=vid,native_type='Snapshot',canonical_content=content,content_identity=identity(content),source_construction_rule=reason,construction_class=kind,execution_inputs_complete=False,precondition_assurance='STRUCTURAL_AND_DECLARED_ROLE_INPUT; full semantic operation and native applicability not executed',oracle_independence='No prospective operation/output or mutable case report used; future expected records are separate',provenance=[ref(basepath)],historical_reconstruction=False)
 filename='fixtures/'+vid.replace(':','__')+'.json';save(filename,packet)
 packets[fid]=dict(fixture_id=fid,state_variant_id=vid,artifact=ref(O/filename),content_identity=packet['content_identity'],native_type='Snapshot',construction_class=kind,scope=normalized['context']['scope'],lineage=normalized['context']['lineage'],provenance=packet['provenance'],structural_validation='PASS_NATIVE_CODEC_TYPES_ONLY',operative_arguments_complete=False)
 requirements.append(dict(VARIANT_ID=vid,OBLIGATIONS_CONSUMING_IT=[row['OBLIGATION_ID'] for row in consumers],ROLE=packet['role_ids'],EXPECTED_NATIVE_TYPE='Snapshot',BASE_SOURCE=ref(basepath),TRANSFORMATION=reason,INTENDED_SEMANTIC_DIFFERENCE=changes,REQUIRED_OPERANDS=[step['args'] for row in consumers for step in read(OLD/'dispatch-table.json')[row['RUNNER_DISPATCH_ID']]['steps']],CURRENT_GAP='Initial missing structural subject closed; full invocation/process/independent output contract not yet closed',CONSTRUCTION_CLASS=kind,CAPSULE_ID=fid))
combined=dict(oldcatalog);combined.update(packets);check(len(combined)==117,'ALL_117_STRUCTURAL_SUBJECTS')
save('missing-variant-inventory-and-construction.json',requirements);save('fixture-catalog.json',combined)
save('structural-validation.json',dict(count=117,rows=[dict(CAPSULE_ID=k,NATIVE_TYPE='Snapshot',STRUCTURAL_VALIDATION='PASS_STRUCTURAL_DECODER_TYPE_ONLY',IDENTITY=v['content_identity'],SOURCE=v['artifact']) for k,v in combined.items()],qualification_operations_invoked=0,semantic_case_result='NOT_RUN'))
# Independently inspect argument references: do not trust prior complete flags.
dispatch=read(OLD/'dispatch-table.json');schemas={};operand_audit=[]
for did,path in dispatch.items():
 symbols=path['operation_ids'];fields={b['fixture_field'] for s in path['steps'] for b in s['args'] if 'fixture_field' in b}
 schemas[did]=dict(dispatch=did,required_fixture_operands=sorted(fields),native_operations=symbols,required_context=['source_root','isolated_store_root','exact scope/lineage/generation','current runtime/definition/policy/source pins'],phase_sealed_by_obligation=True,defaults='Only explicit native signature defaults may be permitted; prototype did not seal all defaults')
 row=next(r for r in source_index if r['RUNNER_DISPATCH_ID']==did)
 for vid in row['STATE_VARIANT_IDS']:
  entry=next(v for v in combined.values() if v['state_variant_id']==vid);packet=read(R/entry['artifact']['path']);available=set(packet['canonical_content']['arguments']);missingfields=fields-available
  operand_audit.append(dict(OBLIGATION_ID=row['OBLIGATION_ID'],CAPSULE_ID=entry['fixture_id'],DISPATCH_ID=did,MISSING_OPERANDS=sorted(missingfields),REFERENCE_COMPLETENESS='FAIL' if missingfields else 'PASS_REFERENCES_ONLY',native_applicability='NOT_ESTABLISHED_COMPLETE',complete_flag_trusted=False))
save('operand-schemas.json',schemas);save('operand-completeness-audit.json',dict(missing_reference_occurrences=sum(len(x['MISSING_OPERANDS']) for x in operand_audit),capsule_dispatch_checks=operand_audit))
print('STRUCTURAL_SUBJECTS=117/117; NO_CASE_EXECUTED; OPERAND_CLOSURE_AUDITED')
