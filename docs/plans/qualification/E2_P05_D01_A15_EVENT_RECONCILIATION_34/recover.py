"""Retained event/descriptor inventory only: never apply, record, replay or save."""
import json,hashlib,subprocess,sys
from pathlib import Path
R=Path('/home/gvasend/app/kge-forge');E=Path(__file__).resolve().parent;Q=R/'docs/plans/qualification'
sys.path.insert(0,str(R))
from adapter.planner import codec,model
CAP=Q/'E2_P05_D01_FIXTURE_ORACLE_CLOSURE_2/fixtures/D01-VARIANT__E2-A15__CANONICAL_REQUIRED_BEHAVIOR.json'
def load(p):return json.loads(Path(p).read_bytes())
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def sha(x):return hashlib.sha256(x).hexdigest()
def pin(p):return {'path':str(p.relative_to(R)),'raw_sha256':sha(p.read_bytes())}
def emit(n,x):(E/n).write_text(json.dumps(x,sort_keys=True,indent=2)+'\n')
def walk(x,pointer=''):
 yield pointer,x
 if isinstance(x,dict):
  for k,v in x.items():yield from walk(v,pointer+'/'+k.replace('~','~0').replace('/','~1'))
 elif isinstance(x,list):
  for i,v in enumerate(x):yield from walk(v,pointer+'/'+str(i))
def recover():
 capsule=load(CAP);content=capsule['canonical_content'];snapshot=content['arguments']['snapshot'];bundle=content['arguments']['bundle'];stateid=codec._wire(codec.snapshot_id(codec._unwire(snapshot)))
 prior=load(Q/'E2_P05_D01_SOURCE_BYTES_DISPATCH_CORRECTION_33/operand-accounting-v3.json');owners=[x['REFERENCE'] for x in prior['REFERENCES'] if x['REFERENCE']['CASE_ID']=='E2-A15'];assert len(owners)==2
 frozen=load(Q/'E2_P05_D01_PROSPECTIVE_MATRIX_CONTRACT_1/sealed-128-obligations.json');obligations=[x for x in frozen['obligations'] if x['CASE_ID']=='E2-A15'];case=load(R/'docs/plans/DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_EXPERIMENT_1.json')['cases'][14]
 # Search all retained qualification JSON, including embedded native bundles/results.
 found=subprocess.run(['rg','-l','"SourceInvalidation"',str(R/'docs'),str(R/'adapter'),'-g','*.json'],capture_output=True,text=True,check=True)
 files=sorted(Path(p) for p in found.stdout.splitlines() if E not in Path(p).parents and not Path(p).name.startswith('DETERMINISTIC_PLANNER_V0_1_E2_P05_D01_A15_EVENT_RECONCILIATION_34'))
 descriptors={};events={};searched=[]
 for file in files:
  raw=file.read_bytes()
  try:doc=json.loads(raw)
  except (ValueError,UnicodeError):continue
  occurrences=[]
  for pointer,node in walk(doc):
   if not isinstance(node,dict):continue
   if node.get('$type')=='SourceInvalidation':
    identity='qualification-retained-source-invalidation-body-v1:'+sha(canonical(node));entry=descriptors.setdefault(identity,{'CANDIDATE_ID':identity,'TYPE':'SourceInvalidation','RETAINED_BODY':node,'REFERENCES':[],'CLASSIFICATION':'WRONG_STATE_BOUNDARY' if node.get('expected_snapshot')!=stateid else 'OTHER','REASON':'Expected Snapshot does not equal exact sealed A15 pre-state' if node.get('expected_snapshot')!=stateid else 'Exact parent alone is insufficient: target role and scope need independent proof','INPUT_IDENTITY_DOMAIN':'changed[] are source identities; expected_snapshot is planner-snapshot-v1; no native descriptor identity field','PRODUCER':'SourceInvalidation input preparation; native consumption is core.apply_event','SUBJECT':'Referenced expected Snapshot; changed sources describe support withdrawal'})
    entry['REFERENCES'].append({'source':pin(file),'pointer':pointer});occurrences.append(pointer)
   if node.get('$type')=='ExecutionEvent' and node.get('result',{}).get('$type')=='SourceInvalidation':
    identity=node['identity']['sha256'];entry=events.setdefault(identity,{'EVENT_ID':node['identity'],'TYPE':'ExecutionEvent','PRODUCER':'codec.record_result / append_event (native result ledger); exact retained writer provenance separately recorded','SUBJECT':node['result']['changed'],'PARENT':node['parent_event'],'PARENT_SNAPSHOT':node['parent_snapshot'],'POSITION':node['sequence'],'AFTER_SNAPSHOT':node['after_snapshot'],'DESCRIPTOR_BODY_ID':'qualification-retained-source-invalidation-body-v1:'+sha(canonical(node['result'])),'STATE_BOUNDARY':{'before':node['parent_snapshot'],'after':node['after_snapshot']},'SCOPE_LINEAGE_PROVENANCE':'Provided by exact parent state/source bundle and retained artifact references, not fields invented in ExecutionEvent','QUALIFICATION_STATUS':'Retained native evidence; not blanket A15 applicability','CLASSIFICATION':'WRONG_EVENT_TYPE','RESULT_PROJECTION_CLASSIFICATION':'WRONG_STATE_BOUNDARY' if node['parent_snapshot']!=stateid else 'OTHER','REASON':'V3 applies SourceInvalidation, not ExecutionEvent. Its result body also has a different pre-state.','LEDGER_CONTAINERS':[],'REFERENCES':[]})
    entry['REFERENCES'].append({'source':pin(file),'pointer':pointer})
  if occurrences:searched.append({'source':pin(file),'descriptor_pointers':occurrences})
 # Context and ordered ledger ownership come from actual containing native bundles.
 contexts=[]
 for file in files:
  try:doc=load(file)
  except (ValueError,UnicodeError):continue
  for pointer,node in walk(doc):
   if not isinstance(node,dict) or node.get('$type')!='PersistenceBundle':continue
   relevant=[event for event in node.get('events',[]) if event.get('identity',{}).get('sha256') in events]
   if not relevant:continue
   ctx=node.get('current',{}).get('context',{});ledger={'source':pin(file),'pointer':pointer,'event_count':len(node['events']),'ordered_event_ids':[x['identity'] for x in node['events']],'head':node['events'][-1]['identity'] if node['events'] else None,'root':node['events'][0]['identity'] if node['events'] else None,'scope':ctx.get('scope'),'lineage':ctx.get('lineage'),'generation':ctx.get('generation'),'policy':node.get('policy'),'policy_version':node.get('policy_version')}
   contexts.append(ledger)
   for event in relevant:events[event['identity']['sha256']]['LEDGER_CONTAINERS'].append({'source':pin(file),'pointer':pointer,'position':event['sequence'],'event_count':len(node['events']),'root':ledger['root'],'head':ledger['head'],'scope':ledger['scope'],'lineage':ledger['lineage'],'generation':ledger['generation']})
 assert not [x for x in descriptors.values() if x['RETAINED_BODY']['expected_snapshot']==stateid]
 # Native source support inventory is informational; no changed tuple chosen/constructed.
 provenances=[{'pointer':ptr,'path':node.get('path'),'identity':node.get('identity'),'scope':node.get('scope'),'method':node.get('method')} for ptr,node in walk(snapshot) if isinstance(node,dict) and node.get('$type')=='Provenance']
 support=[]
 for source in bundle['sources']:
  roles=[x for x in provenances if x['path']==source['path'] and x['identity']==source['identity']]
  support.append({'pin':source,'native_provenance_occurrences':roles,'DIRECT_CURRENT_PROVENANCE':bool(roles),'TARGET_SELECTED':False,'eligibility':'Informational current source; disjoint accepted-support role and exact target partition not sealed for A15'})
 return {'OWNERS':owners,'CASE':case,'OBLIGATIONS':obligations,'CAPSULE_SOURCE':pin(CAP),'STATE_ID':stateid,'STATE_CONTEXT':snapshot['context'],'EXISTING_LEDGER_EVENT_COUNT':len(bundle['events']),'EXISTING_LEDGER_HEAD':bundle['events'][-1]['identity'],'DESCRIPTOR_CANDIDATES':sorted(descriptors.values(),key=lambda x:x['CANDIDATE_ID']),'OCCURRENCE_CANDIDATES':sorted(events.values(),key=lambda x:x['EVENT_ID']['sha256']),'SEARCHED':searched,'CONTAINING_LEDGERS':contexts,'SOURCE_SUPPORT_INVENTORY':support,'SELECTION_UNIQUE':False,'SELECTED_EVENT':None}
if __name__=='__main__':
 data=recover()
 if '--identity' in sys.argv:print(sha(canonical(data)));raise SystemExit
 emit('recovered-inventory.json',data);emit('candidate-search.json',{'SEARCHED_ARTIFACT_COUNT':len(data['SEARCHED']),'DESCRIPTOR_BODY_COUNT':len(data['DESCRIPTOR_CANDIDATES']),'EXECUTION_EVENT_COUNT':len(data['OCCURRENCE_CANDIDATES']),'EXACT_INPUT_PRESTATE_MATCHES':0,'NATIVE_QUALIFICATION_OPERATION_EXECUTED':False,'SEMANTIC_IDENTITY':'qualification-A15-event-inventory-v1:'+sha(canonical(data))})
 print('A15 inventory:',len(data['DESCRIPTOR_CANDIDATES']),'retained descriptor bodies;',len(data['OCCURRENCE_CANDIDATES']),'native invalidation events; zero exact pre-state matches')
