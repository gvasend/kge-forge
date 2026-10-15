"""Read-only contract negatives and independent fresh-process reconstruction."""
import copy,json,os,subprocess,sys
from pathlib import Path
E=Path(__file__).resolve().parent;sys.path.insert(0,str(E))
from recover import load,emit,canonical,sha,R,Q,CAP,pin
from adapter.planner import codec,model
inventory=load(E/'recovered-inventory.json');state=inventory['STATE_ID'];ctx=inventory['STATE_CONTEXT']
for c in inventory['DESCRIPTOR_CANDIDATES']:
 body=codec._unwire(c['RETAINED_BODY']);model.validate_types(body,model.SourceInvalidation);assert codec._wire(body.expected_snapshot)!=state
for c in inventory['OCCURRENCE_CANDIDATES']:
 event=next(load(R/r['source']['path']) for r in c['REFERENCES'] if r['pointer']=='') if any(r['pointer']=='' for r in c['REFERENCES']) else None
 if event is not None:
  native=codec._unwire(event);model.validate_types(native,model.ExecutionEvent);assert codec._wire(codec._event_identity(native.sequence,native.parent_snapshot,native.parent_event,native.result,native.after_snapshot,native.resume_binding))==c['EVENT_ID']
# This is a contract envelope, not an event body or an occurrence assertion.
contract={'NATIVE_INPUT_TYPE':'SourceInvalidation','EVENT_ROLE':'INPUT_INVALIDATION_DESCRIPTOR','PRODUCER':'qualification fixture preparation; native application core.apply_event','SUBJECT':'exact sealed A15 pre-state','EXPECTED_SNAPSHOT':state,'SCOPE':ctx['scope'],'LINEAGE':ctx['lineage'],'GENERATION':ctx['generation'],'PROVENANCE':pin(CAP),'NATIVE_INPUT_EVENT_ID':None,'PARENT_EVENT_INPUT':None,'LEDGER_INPUT':None,'POSITION_INPUT':None,'EXISTS_AS_QUALIFYING_RETAINED_INPUT':False,'FUTURE_EVENT_ASSERTED_EXISTING':False}
def validate_schema(candidate):
 if candidate!=contract:raise ValueError('A15_INPUT_ROLE_DOMAIN_OR_BOUNDARY_MISMATCH')
 return True
assert validate_schema(contract)
negatives=[]
def reject(name,candidate):
 try:validate_schema(candidate)
 except ValueError as error:negatives.append({'NAME':name,'RESULT':'PASS','REJECTION':str(error),'NATIVE_OPERATION_EXECUTED':False});return
 raise AssertionError('FAIL_OPEN '+name)
for name,field in [('wrong event type','NATIVE_INPUT_TYPE'),('wrong producer','PRODUCER'),('wrong subject','SUBJECT'),('wrong parent','EXPECTED_SNAPSHOT'),('wrong ledger','LEDGER_INPUT'),('wrong position','POSITION_INPUT'),('wrong Snapshot/state','EXPECTED_SNAPSHOT'),('wrong scope','SCOPE'),('wrong lineage','LINEAGE'),('wrong provenance','PROVENANCE')]:
 bad=copy.deepcopy(contract);bad[field]='wrong';reject(name,bad)
for name,typ in [('report substituted for event','QualificationReport'),('Snapshot substituted for event','Snapshot'),('A14 persistence evidence substituted for event','PersistedHandoff'),('event from another case','ExternalEvent'),('semantically equivalent occurrence with different event identity','ExecutionEvent')]:
 bad=copy.deepcopy(contract);bad['NATIVE_INPUT_TYPE']=typ;bad['NATIVE_INPUT_EVENT_ID']='foreign-event-identity';reject(name,bad)
bad=copy.deepcopy(contract);bad['FUTURE_EVENT_ASSERTED_EXISTING']=True;reject('future event asserted as already existing',bad)
# Do not equate body projection with a ledger witness, or claim A15 -> A16 ancestry.
bad=copy.deepcopy(contract);bad['EVENT_ROLE']='HISTORICAL_OCCURRENCE_WITNESS';reject('descriptor confused with occurrence witness',bad)
bad=copy.deepcopy(contract);bad['EXPECTED_SNAPSHOT']={'sha256':'7ec95347f9662731ad5254221c03196fe789eb3435d02947eb09a70077ab66b9'};reject('A14 corrected Snapshot used as A15 pre-state',bad)
seeds=[]
for seed in [0,1,7,101]:
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED=str(seed));p=subprocess.run([sys.executable,str(E/'recover.py'),'--identity'],cwd=str(R),env=env,capture_output=True,text=True,check=True);seeds.append({'seed':seed,'inventory_semantic_hash':p.stdout.strip(),'selected_event':None,'candidate_exact_matches':0})
assert len({x['inventory_semantic_hash'] for x in seeds})==1
emit('event-input-contract.json',{'CONTRACT_ENVELOPE':contract,'NATIVE_DESCRIPTOR_FIELDS':{'changed':'Tuple[ArtifactIdentity,...]; exact disjoint required source targets remain unsealed; native unordered field, no source selected','expected_snapshot':state},'INPUT_NATIVE_IDENTITY':'No SourceInvalidation.identity field; consumes exact source identities and expected Snapshot identity, not an ExecutionEvent ID','PRODUCER_BOUNDARIES':{'descriptor':'Pure native-model fixture preparation or exact retained ExecutionEvent.result projection, only after input/target ownership is sealed','state_transition':'adapter.planner.core.apply_event(snapshot,supplied) -> TransitionReport; does not append a ledger occurrence','ledger_occurrence':'adapter.planner.codec.record_result(bundle,supplied) -> updated native bundle with new ExecutionEvent; executes transition and replay; future execution authority required','durable_commit':'codec.commit_event additionally publishes transactional state/HEAD; not authorized here'},'STATE_CONTEXT':ctx,'CURRENT_LEDGER':{'event_count':inventory['EXISTING_LEDGER_EVENT_COUNT'],'head':inventory['EXISTING_LEDGER_HEAD'],'future_record_result_sequence_rule':'len(exact input bundle.events)+1; 20 only if this exact 19-event bundle is selected unchanged','future_parent_event_rule':'last exact input event identity; no native ledger root/append-head operand consumed by core.apply_event'},'OCCURRENCE_IDENTITY_RULE':'planner-event-v1 hash over canonical sequence,parent_snapshot,parent_event,typed result,after_snapshot and optional resume_binding. Future after_snapshot is unknown; no future occurrence ID computed','HISTORICAL_EVENT_REQUIRED':False,'PROSPECTIVE_EVENT_PERMITTED':True,'NATIVE_EVENT_MANUFACTURED':False,'A14_PERSISTENCE_EVENT_APPLICABLE':False,'A16_DEPENDENCY':'No direct dependency: canonical A16 starts from restored A14 unknown-rule variant, not A15 invalidated accepted-support state','ADDITIONAL_GATE':'Full A15 event-trace/reload assurance requires its separately sealed persistence/ledger sequence; current APPLY_EVENT dispatch alone does not generate an occurrence or persist invalidation'})
emit('negative-suite.json',{'RESULT':'PASS','PASS':len(negatives),'TOTAL':len(negatives),'CASES':negatives,'CONTROL_KIND':'Metadata schema/domain/boundary controls only; no SourceInvalidation descriptor or native occurrence constructed/applied','RETAINED_BODY_TYPE_CHECKS':len(inventory['DESCRIPTOR_CANDIDATES'])})
emit('determinism.json',{'RESULT':'PASS','SEEDS':seeds,'SELECTION_UNIQUE':False,'SELECTED_EVENT':None,'NATIVE_CASES_EXECUTED':0})
print('A15 checks PASS:',len(negatives),'negatives; 4-seed inventory identical; no event manufactured')
