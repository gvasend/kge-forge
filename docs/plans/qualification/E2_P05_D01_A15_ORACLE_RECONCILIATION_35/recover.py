"""Independent oracle-role recovery; no native case, descriptor or oracle creation."""
import ast,json,hashlib,subprocess,sys
from pathlib import Path
R=Path('/home/gvasend/app/kge-forge');E=Path(__file__).resolve().parent;Q=R/'docs/plans/qualification'
def load(p):return json.loads(Path(p).read_bytes())
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def sha(x):return hashlib.sha256(x).hexdigest()
def pin(p):return {'path':str(p.relative_to(R)),'raw_sha256':sha(p.read_bytes())}
def emit(n,x):(E/n).write_text(json.dumps(x,sort_keys=True,indent=2)+'\n')
def walk(x,p=''):
 yield p,x
 if isinstance(x,dict):
  for k,v in x.items():yield from walk(v,p+'/'+k.replace('~','~0').replace('/','~1'))
 elif isinstance(x,list):
  for i,v in enumerate(x):yield from walk(v,p+'/'+str(i))
def recover():
 frozen=load(Q/'E2_P05_D01_PROSPECTIVE_MATRIX_CONTRACT_1/sealed-128-obligations.json');ob=[x for x in frozen['obligations'] if x['OBLIGATION_ID']=='D01-OBL:E2-A15_ORACLE'];assert len(ob)==1
 prior=load(Q/'E2_P05_D01_A15_EVENT_RECONCILIATION_34/operand-frontier.json');owners=[x['REFERENCE'] for x in prior['REFERENCES'] if x['REFERENCE']['OBLIGATION_ID']=='D01-OBL:E2-A15_ORACLE'];assert len(owners)==1
 dispatch=load(Q/'E2_P05_D01_SOURCE_BYTES_DISPATCH_CORRECTION_33/dispatch-table-v3.json');op=dispatch['D01-DISPATCH:E2-A15_OPERANDS'];oc=dispatch['D01-DISPATCH:E2-A15_ORACLE'];assert op['steps']==oc['steps']
 capsule=load(Q/'E2_P05_D01_FIXTURE_ORACLE_CLOSURE_2/fixtures/D01-VARIANT__E2-A15__CANONICAL_REQUIRED_BEHAVIOR.json');bundle=capsule['canonical_content']['arguments']['bundle'];snapshot=capsule['canonical_content']['arguments']['snapshot'];a15state=load(Q/'E2_P05_D01_A15_EVENT_RECONCILIATION_34/event-input-contract.json')['NATIVE_DESCRIPTOR_FIELDS']['expected_snapshot']
 fullschema=load(Q/'E2_P05_D01_PROSPECTIVE_MATRIX_CONTRACT_1/full-output-comparison-contract.json');tree=ast.parse((Q/'E2_P05_D01_SOURCE_BYTES_DISPATCH_CORRECTION_33/runner_v3.py').read_text());capture=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='capture');call=next(n for n in ast.walk(capture) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='dict');fields=sorted([kw.arg for kw in call.keywords]+['output_field_set'])
 groups={name:{} for name in ['DESCRIPTORS','OCCURRENCES','RESULT_EVENT_PROJECTIONS','SNAPSHOTS','REPORTS','INDEPENDENT_LOCAL_ORACLES','COMPLETE_EXPECTED_OUTPUT_CANDIDATES']};searched=[]
 result=subprocess.run(['rg','-l','"SourceInvalidation"|"TransitionReport"|"expected_full_output"|"typed_snapshot"',str(R/'docs'),str(R/'adapter'),'-g','*.json'],capture_output=True,text=True,check=True)
 files=sorted(Path(p) for p in result.stdout.splitlines() if E not in Path(p).parents and not Path(p).name.startswith('DETERMINISTIC_PLANNER_V0_1_E2_P05_D01_A15_ORACLE_RECONCILIATION_35'))
 # Explicit independent authored P03 oracles: partial local models, never runner-output replacement.
 files=sorted(set(files)|set((Q/'P03_PROSPECTIVE_CHECKPOINT_1').glob('*oracle*.json')))
 for path in files:
  raw=path.read_bytes()
  try:doc=json.loads(raw)
  except (ValueError,UnicodeError):continue
  relevant=False
  for ptr,node in walk(doc):
   if not isinstance(node,dict):continue
   group=None;classification=None;reason=None;extra={}
   if node.get('$type')=='SourceInvalidation':
    group='DESCRIPTORS';classification='WRONG_TYPE';reason='Operative input body is not independent expected full output';extra={'expected_snapshot':node.get('expected_snapshot'),'input_binding_classification':'WRONG_PRE_STATE' if node.get('expected_snapshot')!=a15state else 'OTHER','changed':node.get('changed')}
   elif node.get('$type')=='ExecutionEvent' and node.get('result',{}).get('$type')=='SourceInvalidation':
    group='OCCURRENCES';classification='WRONG_PRE_STATE' if node.get('parent_snapshot')!=a15state else 'OTHER';reason='Retained occurrence may be an event projection, not the complete oracle; exact parent/variant mismatches exclude it';extra={'event_identity':node.get('identity'),'parent_snapshot':node.get('parent_snapshot'),'after_snapshot':node.get('after_snapshot'),'position':node.get('sequence')}
   elif node.get('$type')=='Snapshot':
    group='SNAPSHOTS';classification='WRONG_TYPE';reason='Snapshot can populate a typed-state field only; cannot stand for event, descriptor or complete expected envelope';extra={'context':node.get('context'),'equal_to_sealed_prestate':canon(node)==canon(snapshot),'post_state_proven':False}
   elif node.get('$type')=='TransitionReport' or node.get('qualification_type')=='TransitionReport':
    group='RESULT_EVENT_PROJECTIONS';classification='WRONG_TYPE';reason='Recorded native result projection is partial and producer-derived, not an independent full oracle';extra={'producer_derived':True}
   elif isinstance(node.get('expected_full_output'),dict):
    group='COMPLETE_EXPECTED_OUTPUT_CANDIDATES';expected=node['expected_full_output'];classification='OTHER' if set(expected)==set(fields) else 'WRONG_TYPE';reason='Must establish exact A15 descriptor/variant/pre-state and independent authoritative provenance; no input target currently sealed';extra={'closed_field_set_matches':set(expected)==set(fields),'independent_A15_ownership_proven':False}
   elif set(fields).issubset(node):
    group='RESULT_EVENT_PROJECTIONS';classification='OTHER';reason='Complete captured shape alone is not independent oracle authority; case-produced values cannot define expectations';extra={'snapshot_identity':node.get('snapshot_identity'),'closed_field_set_matches':set(node)==set(fields),'independent_A15_ownership_proven':False}
   if group:
    identifier='qualification-retained-'+group.lower()+'-v1:'+sha(canon(node));entry=groups[group].setdefault(identifier,{'CANDIDATE_ID':identifier,'GROUP':group,'CLASSIFICATION':classification,'REASON':reason,'DETAILS':extra,'REFERENCES':[]});entry['REFERENCES'].append({'source':pin(path),'pointer':ptr});relevant=True
  if path.parent==Q/'P03_PROSPECTIVE_CHECKPOINT_1' and 'oracle' in path.name:
   identity='qualification-local-oracle-v1:'+sha(raw);groups['INDEPENDENT_LOCAL_ORACLES'][identity]={'CANDIDATE_ID':identity,'GROUP':'INDEPENDENT_LOCAL_ORACLES','CLASSIFICATION':'WRONG_PRE_STATE','REASON':'Authored local P03 checkpoint oracle; different start/checkpoint and partial schema, not a complete A15 post-root-proof invalidation oracle','DETAILS':{'schema':doc.get('schema'),'fixture':doc.get('fixture'),'context':doc.get('context'),'start':doc.get('start'),'checkpoint':doc.get('checkpoint'),'field_names':sorted(doc)},'REFERENCES':[{'source':pin(path),'pointer':''}]};relevant=True
  if relevant:searched.append(pin(path))
 # Retained reports are inventoried as evidence only, never selected as expectations.
 for base in [Q/'P03_PROSPECTIVE_CHECKPOINT_1',Q/'E2_P04_CANONICAL_EXECUTION_RETRY_1']:
  for path in sorted(base.rglob('*result*.json')):
   raw=path.read_bytes();doc=json.loads(raw);identity='qualification-retained-report-v1:'+sha(raw);groups['REPORTS'][identity]={'CANDIDATE_ID':identity,'GROUP':'REPORTS','CLASSIFICATION':'WRONG_TYPE','REASON':'Mutable/producer runtime evidence or qualification report; not independent expected native full output','DETAILS':{'field_names':sorted(doc) if isinstance(doc,dict) else None},'REFERENCES':[{'source':pin(path),'pointer':''}]}
 assert len(groups['DESCRIPTORS'])==39 and len(groups['OCCURRENCES'])==36
 return {'OWNERS':owners,'ORACLE_OBLIGATION':ob[0],'ORACLE_JOB_DISPATCH':oc,'INPUT_JOB_DISPATCH':op,'NATIVE_ARG_TYPE':'SourceInvalidation','NATIVE_ARG_CARDINALITY':1,'ORACLE_ROLE_TYPE':ob[0]['INPUT_REQUIREMENTS']['expected_type'],'ORACLE_PATH':'Future matrix row.oracle_reference -> expected_full_output; concrete A15 full-output reference/value not sealed','RELATIONSHIP':'Same logical operative-input projection on two distinct job rows; independent expected output is a separate object, not .event','PRE_STATE_ID':a15state,'PRE_STATE_CONTEXT':snapshot['context'],'POLICY_VERSION':bundle['policy_version'],'NATIVE_REPLAY_SCOPE':bundle['scope'],'FULL_CAPTURE_FIELDS':fields,'FROZEN_FULL_OUTPUT_CONTRACT':fullschema,'INVENTORIES':{k:sorted(v.values(),key=lambda x:x['CANDIDATE_ID']) for k,v in groups.items()},'SEARCHED_ARTIFACTS':searched,'SELECTED_ORACLE':None,'ORACLE_SELECTION_UNIQUE':False,'ORACLE_DERIVABLE_NOW':False,'REASON_NOT_DERIVABLE':'Exact changed-source/disjoint variant descriptor unsealed; complete native dependency effects, computation/proofs/resume and durable trace cannot be uniquely valued. No independent complete model oracle exists for this exact input.'}
if __name__=='__main__':
 data=recover()
 if '--identity' in sys.argv:print(sha(canon(data)));raise SystemExit
 emit('recovered-oracle-contract.json',data);emit('candidate-counts.json',{k:len(v) for k,v in data['INVENTORIES'].items()});print('A15 oracle role recovered; .event is input; no complete expected oracle selected/derived')
