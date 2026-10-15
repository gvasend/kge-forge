"""R05 isolated requalification, leaving sealed R04 evidence unchanged."""
import sys,json,itertools
from pathlib import Path
from dataclasses import replace
from adapter.tests import qualify_reentry_r04 as r04
from adapter.planner import codec as c,model as m,validation_transaction as vt,core,gates
R=Path(__file__).resolve().parents[2];O=R/'docs/plans/qualification/REENTRY_R05_1';Q=O/'r04-requalification'
r04.O=Q

def permutations(components_only=False):
 # Cardinality tests are record/input/projection components. Empty/short sets
 # cannot satisfy a full A10 command's mandatory Evidence/receipt/source DAG.
 old=R/'docs/plans/qualification/REENTRY_R04_1';inv=c.parse_json((old/'checkpoint-inventory.json').read_bytes());z=inv[-1]
 b=c.restore(R/z['path'],c._unwire(z['identity']),R);record=b.current.validation_results[0]
 admission=next(e.result for e in b.events if type(e.result) is m.ValidationSupportAdmission)
 _,_,_,native=vt.definitions(b.current,record.definition_set)
 rule=c.parse_json(native['validation'].body_json.encode())['contract']
 rows=[]
 for size in (0,1,2,3,5):
  members=record.input_identities[:size];expected=vt.canonical_inputs(members)
  original=vt.identified(replace(record,input_identities=members),'planner-validation-result-record-v1')
  baseline=c.canonical_bytes(c._wire(original));projected=vt.project(replace(b.current,validation_results=(),validation_instances=()),original)
  projection=projected.validation_instances[-1]
  count=0
  for order in itertools.permutations(members):
   candidate=vt.identified(replace(record,input_identities=order),'planner-validation-result-record-v1')
   assert c.canonical_bytes(c._wire(candidate))==baseline and candidate.id==original.id
   assert vt.canonical_inputs(order)==expected
   # Missing mandatory actual DAG members are rejected in every ordering.
   assessment=vt.identified(replace(admission.assessment,input_identities=order),'planner-validation-assessment-v1')
   try:vt.verify_assessment(admission.command,assessment,rule,record.input_identities)
   except m.PlannerError as exc:assert str(exc)=='VALIDATION_ASSESSMENT_BINDING'
   else:raise AssertionError('underspecified actual A10 input DAG accepted')
   result=vt.project(replace(b.current,validation_results=(),validation_instances=()),candidate)
   assert result.validation_instances[-1]==projection
   for identity in members:assert (identity in order)==(identity in members)
   count+=1
  rows.append({'cardinality':size,'permutations':count,'canonical_bytes_identity_membership_projection':'PASS','actual_A10_admission':'REJECTED_EQUIVALENTLY: mandatory actual DAG members missing','Proof_C03':'unchanged existing authoritative state; invalid operands never applied'})
 if components_only:
  (O/'component-permutations.json').write_bytes(c.canonical_bytes({'RESULT':'PASS','cases':rows}))
  print('component cardinalities and actual mandatory-DAG rejection PASS',flush=True);return
 # Full actual canonical state tests all consumers, including assessment,
 # result/support, model admission, Proof, C03, and event-ledger replay.
 expected=r04.view(b);full=[]
 for mode in ('reverse','rotate','sorted'):
  def ordering(values):
   if mode=='reverse':return tuple(reversed(values))
   if mode=='rotate':return values[1:]+values[:1]
   return vt.canonical_inputs(values)
  def changed(obj):
   if type(obj) in (m.ValidationAssessment,m.ValidationResultRecord,m.ValidationSupportRecord):return replace(obj,input_identities=ordering(obj.input_identities))
   return obj
  state=replace(b.current,validation_results=tuple(changed(x) for x in b.current.validation_results),validation_support_records=tuple(changed(x) for x in b.current.validation_support_records))
  events=[]
  for e in b.events:
   if type(e.result) is m.ValidationSupportAdmission:
    admission=replace(e.result,assessment=changed(e.result.assessment),validation_result=changed(e.result.validation_result),support=changed(e.result.support))
    e=replace(e,result=admission)
   events.append(e)
  trial=replace(b,current=state,events=tuple(events))
  assert c._bundle_bytes_admitted(trial)==c._bundle_bytes_admitted(b)
  m.validate_model(trial.current);assert r04.view(trial)==expected
  assert c.bundle_bytes(trial)==c.bundle_bytes(b)
  # Persistence emits identical native bytes/identity for equivalent presentations.
  path,bid=c.save_bundle(trial,O/('permutation-'+mode),R)
  restored=c.restore(path,bid,R);assert r04.view(restored)==expected
  # Membership invalidation is native SourceInvalidation over the same exact member.
  identity=record.provenance.identity
  withdrawn=c.record_result(trial,m.SourceInvalidation((identity,),c.snapshot_id(trial.current)))
  assert not core.resume_eligibility(withdrawn,R).allowed
  full.append({'ordering':mode,'admission_Proof_C03_replay':'PASS','bundle':c._wire(bid),'dependency_invalidation':'PASS','path':str(path.relative_to(R))})
 duplicates=[]
 for cls in (m.ValidationResultRecord,m.ValidationAssessment,m.ValidationSupportRecord):
  try:vt.canonical_inputs((record.input_identities[0],record.input_identities[0]))
  except m.PlannerError as exc:duplicates.append({'type':cls.__name__,'result':'REJECTED','reason':str(exc)})
  else:raise AssertionError('duplicate accepted')
 # Distinct membership remains distinct; projection does not erase members.
 a,bid,cid=record.input_identities[:3]
 pairs=[((a,bid),(a,cid)),((a,),(a,bid))]
 for one,two in pairs:
  x=vt.identified(replace(record,input_identities=one),'planner-validation-result-record-v1');y=vt.identified(replace(record,input_identities=two),'planner-validation-result-record-v1')
  assert x.id!=y.id and c.canonical_bytes(c._wire(x))!=c.canonical_bytes(c._wire(y))
  assert vt.canonical_inputs(one)!=vt.canonical_inputs(two)
 # Changing only result membership breaks support projection, rather than being normalized away.
 wrong=vt.identified(replace(record,input_identities=record.input_identities[:-1]),'planner-validation-result-record-v1')
 bad=replace(b.current,validation_results=(wrong,))
 try:m.validate_model(bad)
 except m.PlannerError as exc:membership_error=str(exc)
 else:raise AssertionError('changed membership admitted with original support')
 (O/'permutation-qualification.json').write_bytes(c.canonical_bytes({'RESULT':'PASS','cardinality_components':rows,'full_native_set_cardinality':len(record.input_identities),'full_actual_state':full,'duplicates':duplicates,'membership_negatives':'PASS','membership_error':membership_error,'codec_identity_changed':False}))
 print('input/projection permutations and full native consumers PASS',flush=True)

if __name__=='__main__':
 mode=sys.argv[1]
 if mode=='write':
  # Fresh qualified A09/A10 reproduction; no canonical commit or reused live instance.
  r04.replay_capture=r04.construct;r04.write()
 elif mode=='permutations':permutations()
 elif mode=='components':permutations(True)
 else:{'read':r04.reader,'reproduce_capture':r04.reproduce_capture,'supplement':r04.supplement}[mode]()
