"""Read-only PREPARE definition/context inventory and version comparisons."""
import hashlib,json
from pathlib import Path
from adapter.planner import codec
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;D=R/'docs/plans'
def read(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p,ptr=''):return {'path':str(p.relative_to(R)),'pointer':ptr,'raw_sha256':sha(p.read_bytes())}
def save(n,v):(O/n).write_text(json.dumps(v,sort_keys=True,indent=2)+'\n')
sp=O.parent/'E2_P05_D01_A14_PROVENANCE_FIXTURE_CORRECTION_7/corrected-prospective-snapshot.json';snap=read(sp)['snapshot'];old=next(a for a in snap['actions'] if a['id']['value']=='E2-PREPARE');oldbytes=old['source']['excerpt'].encode();oldbody=codec.canonical_bytes(codec._wire(codec._unwire(old)))
def summary(a,context,source):
 n=codec._unwire(a)
 return {'ACTION_SOURCE':source,'NATIVE_ACTION_ID':a['id'],'ACTION_COMPARISON_CONTENT_IDENTITY':{'DOMAIN':'qualification-PREPARE-action-comparison-v1','SHA256':sha(codec.canonical_bytes(codec._wire(n)))},'NATIVE_ACTION_FIELDS':a,'SOURCE_CONTENT_IDENTITY':a['source']['identity'],'INPUTS':{'prerequisites':a['prerequisites'],'requirements':codec._wire(n.requirements),'prepared_dossier_required_facts':codec._wire(n.prepared_dossier.required_facts) if n.prepared_dossier else [],'source':a['source']},'OUTPUTS':{'accepted_inventory':a['accepted_inventory'],'prepared_dossier':a.get('prepared_dossier')},'RESULT_CONTRACT':{'accepted_result':codec._wire(n.accepted_result),'pass_model_complete':n.pass_model_complete,'stage':codec._wire(n.stage)},'DEPENDENCIES':a['prerequisites'],'ACCEPTED_INVENTORY':a['accepted_inventory'],'SCOPE':context['scope'] if context else a['source']['scope'],'LINEAGE':context.get('lineage') if context else None,'GENERATION':context.get('generation') if context else None,'CONTEXT_SOURCE':'containing Snapshot context' if context else 'not present in Action artifact; scope from native provenance only','PHYSICAL_SOURCE_PATH':a['source']['path'],'SOURCE_RAW_BYTE_LENGTH':len(a['source']['excerpt'].encode()),'SOURCE_RAW_SHA256':a['source']['identity']['sha256']}
left=summary(old,snap['context'],pin(sp,'/snapshot/actions/'+str(snap['actions'].index(old))))
target=D/'DETERMINISTIC_PLANNER_V0_1_E2_P04_CANONICAL_TARGET_BUNDLE_1.json';resultpath=D/'DETERMINISTIC_PLANNER_V0_1_E2_P04_CANONICAL_EXECUTION_RETRY_1_RESULT.json';result=read(resultpath);assert sha(target.read_bytes())==result['execution_evidence']['target_bundle']['sha256'];current=read(target)['bundle']['current'];new=next(a for a in current['actions'] if a['id']['value']=='E2-PREPARE');right=summary(new,current['context'],pin(target,'/bundle/current/actions/'+str(current['actions'].index(new))))
np=codec._path(R,new['source']['path']);nbytes=np.read_bytes();assert sha(nbytes)==new['source']['identity']['sha256'] and nbytes==new['source']['excerpt'].encode() and nbytes!=oldbytes
inventory=read(O/'retained-prepare-definition-inventory.json');groups={};invalid=[]
for row in inventory['ROWS']:
 a=row['native_action'];context=row['containing_snapshot_context']
 try:body=codec.canonical_bytes(codec._wire(codec._unwire(a)))
 except (ValueError,TypeError,KeyError) as exc:
  invalid.append({'SOURCE':row['source'],'CLASSIFICATION':'UNRELATED','REASON':'non-decodable native Action candidate: '+str(exc)});continue
 key=sha(codec.canonical_bytes({'native_action_body_hash':sha(body),'context':context}))
 if key not in groups:
  samebytes=a['source']['excerpt'].encode()==oldbytes and a['source']['identity']==old['source']['identity']
  samecontext=context is None or all(context.get(k)==snap['context'].get(k) for k in ['scope','lineage','generation'])
  if body==oldbody and samecontext:classification='EXACT_SAME_SOURCE'
  elif samebytes and body==oldbody:classification='BYTE_IDENTICAL_DIFFERENT_CONTEXT'
  else:classification='DIFFERENT_VERSION'
  groups[key]={'VARIANT_ID':'qualification-PREPARE-retained-variant-v1:'+key,'CLASSIFICATION':classification,'DEFINITION':summary(a,context,row['source']),'EXACT_A14_SOURCE_BYTES_IN_EXCERPT':samebytes,'NATIVE_ACTION_BODY_EQUAL':body==oldbody,'PHYSICAL_BYTES_SUBSTITUTABLE':'Only separately authenticated exact A14 raw bytes; never the Action object or wrapper','OCCURRENCES':[]}
 groups[key]['OCCURRENCES'].append(row['source'])
save('prepare-definition-variant-comparison.json',{'NATIVE_ACTION_OCCURRENCE_COUNT':inventory['COUNT'],'VARIANT_COUNT':len(groups),'VARIANTS':[groups[k] for k in sorted(groups)],'INVALID_CANDIDATES':invalid,'SCOPE':inventory['SCOPE'],'CLASSIFICATION_RULE':'Full native Action canonical body, physical source identity/excerpt and containing Snapshot context; source byte equality alone does not substitute an Action definition','NO_RETAINED_CANDIDATE_SELECTED_AS_A14_FIXTURE':True})
named=[]
for name in ['DETERMINISTIC_PLANNER_V0_1_P03_PROSPECTIVE_CHECKPOINT_BUNDLE_1.json','DETERMINISTIC_PLANNER_V0_1_E2_P04_FINAL_PREEXECUTION_CONFIGURATION_BUNDLE_1.json','DETERMINISTIC_PLANNER_V0_1_E2_P04_CANONICAL_TARGET_BUNDLE_1.json']:
 p=D/name;s=read(p)['bundle']['current'];a=next(x for x in s['actions'] if x['id']['value']=='E2-PREPARE');named.append(summary(a,s['context'],pin(p,'/bundle/current/actions/'+str(s['actions'].index(a)))))
out={'A14_EXPECTED_PREPARE_SOURCE':left,'CURRENT_P04_PREPARE_DEFINITION':right,'CURRENT_PREPARE_DEFINITIONS':named,'CURRENT_P04_QUALIFICATION_RESULT':pin(resultpath),'CURRENT_P04_PHYSICAL_SOURCE':pin(np),'HISTORICAL_CURRENT_RELATIONSHIP':'DIFFERENT_VERSION','CURRENT_PREPARE_SUBSTITUTION_ALLOWED':False,'SOURCE_BYTE_EQUALITY':False,'SOURCE_HASH_EQUALITY':False,'FIELD_COMPARISON':{k:{'A14':old.get(k),'CURRENT_P04':new.get(k),'EQUAL':old.get(k)==new.get(k)} for k in sorted(set(old)|set(new))},'CONTEXT_COMPARISON':{k:{'A14':snap['context'][k],'CURRENT_P04':current['context'][k],'EQUAL':snap['context'][k]==current['context'][k]} for k in ['scope','lineage','generation']},'ALL_RETAINED_VARIANT_COMPARISON':pin(O/'prepare-definition-variant-comparison.json'),'VARIANT_COUNT':len(groups),'RATIONALE':'P03/P04 authored prospective wrapper differs from A14 raw marker. Action IDs, operation and CHECK/COLLECT gates overlap but native source/inventory/dossier provenance and lineage/generation differ. Nested template provenance is not the physical wrapper. Current definition is compared only; none substituted or executed.','NATIVE_OPERATIONS_EXECUTED':0}
save('historical-current-prepare-comparison.json',out)
print(json.dumps({'RELATIONSHIP':'DIFFERENT_VERSION','A14_BYTES':len(oldbytes),'CURRENT_SOURCE_BYTES':len(nbytes),'CURRENT_SOURCE_HASH':sha(nbytes),'VARIANTS':len(groups),'OCCURRENCES':inventory['COUNT'],'SUBSTITUTION_ALLOWED':False}))
