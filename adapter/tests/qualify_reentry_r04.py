"""Isolated native A09/A10/A11 qualification; never publishes canonical P04."""
import json,sys,hashlib,os,subprocess
from pathlib import Path
from dataclasses import replace,fields,is_dataclass
from concurrent.futures import ThreadPoolExecutor
from adapter.planner import codec as c,core,gates,model as m,validation_transaction as vt,installation as i
from adapter.tests.qualify_p04_a09_control import inputs
from adapter.tests.qualify_validation_v02 import computation_wire
R=Path(__file__).resolve().parents[2];D=R/'docs/plans';O=D/'qualification/REENTRY_R04_1'
BID=m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY,'planner-bundle-v1','1b69d962865c23fa43b3ec362af096e39d72bbfc4dee2252d1e0d4914d487054')
REQ=m.EvidenceId('E2-EXTERNAL-REQUIREMENT'); ACTION=m.ActionId('E2-REENTER'); GATE=m.GateId('E2-GATE')
def emit(name,value):
 O.mkdir(parents=True,exist_ok=True);(O/name).write_bytes(c.canonical_bytes(value))
def permute(x):
 if is_dataclass(x):
  updates={f.name:permute(getattr(x,f.name)) for f in fields(x)}
  for f in c.SET_FIELDS.get(type(x),set()):
   if type(updates.get(f)) is tuple:updates[f]=tuple(reversed(updates[f]))
  return replace(x,**updates)
 if type(x) is tuple:return tuple(permute(v) for v in x)
 return x

def view(b):
 proof=gates.obligation_proof(b.current,REQ);elig=core.resume_eligibility(b,R)
 return {'bundle':c._wire(c.bundle_id(b)),'state':c._wire(c.snapshot_id(b.current)),
  'head':c._wire(b.events[-1].identity),'events':c._wire(b.events),'sources':sorted(c._wire(b.sources),key=c.canonical_bytes),'policy':c._wire(b.policy),
  'proof':{'state':proof.state.value,'reasons':list(proof.reasons)},'eligibility':c._wire(elig),'computation':computation_wire(b.current)}
def construct(reverse=False):
 b=c.restore(D/'DETERMINISTIC_PLANNER_V0_1_E2_P04_POST_A10_INSTALL_BUNDLE_1.json',BID,R)
 if reverse:b=permute(b)
 _,_,expected=inputs()
 x=c._unwire(c.parse_json((D/'qualification/VALIDATION_V02_1/fresh-a09-candidate.json').read_bytes()))
 if reverse:x=permute(x)
 received=c.preflight_external_evidence(b,x,{p.path:(R/p.path).read_bytes() for p in x.source_additions},R,expected_binding=expected)
 record=next(z for z in b.current.installed_definitions if i.descriptor(z.request.definition)[0]['definition_type']=='VALIDATION_SUPPORT_DEFINITION_SET')
 a,validated=vt.prepare(received,vt.command(received,x.entity.id,record.id),R)
 assert gates.obligation_proof(validated.current,REQ)==gates.Proof(m.ProofState.PROVED,())
 pre=core.resume_eligibility(validated,R);assert not pre.allowed
 event=m.ExternalEvent(GATE,m.ExternalStage.DEPENDENT_ACTION_REENTRY,c.snapshot_id(validated.current))
 external=c.record_result(validated,event)
 extelig=core.resume_eligibility(external,R);assert not extelig.allowed and any('DECISION_REENTRY_REQUIRED' in z for z in extelig.reasons)
 decision=next(d for d in external.current.decisions if ACTION in d.downstream)
 post=c.record_result(external,m.DecisionReentry(decision.action,c.snapshot_id(external.current)))
 assert core.resume_eligibility(post,R).actions==(ACTION,)
 return b,x,received,a,validated,event,external,post

def read(path,identity,reverse=False):
 b=c.restore(path,c._unwire(identity),R)
 if reverse:
  reordered=permute(b);assert c.bundle_bytes(b)==c.bundle_bytes(reordered);b=reordered
 before=c.bundle_bytes(b);answer=view(b);assert c.bundle_bytes(b)==before
 assert answer['proof']=={'state':'PROVED','reasons':[]}
 assert core.resume_eligibility(b,R).actions==(ACTION,)
 return answer

def replay_capture():
 # Replay legitimate independently reproduced event records; no fresh validator decision.
 rows=c.parse_json((O/'independent-reproduction-results.json').read_bytes());captured=rows[0]['result']['view']
 b=c.restore(D/'DETERMINISTIC_PLANNER_V0_1_E2_P04_POST_A10_INSTALL_BUNDLE_1.json',BID,R)
 events=c._unwire(captured['events']);state=b.initial
 for e in events:
  state=core.apply_event(state,e.result).snapshot
  assert c.snapshot_id(state)==e.after_snapshot
 post=replace(b,events=events,current=state,sources=c._unwire(captured['sources']))
 c._replay(post);assert view(post)==captured
 x=c._unwire(c.parse_json((D/'qualification/VALIDATION_V02_1/fresh-a09-candidate.json').read_bytes()))
 received=c._prefix_bundle(post,8);v=c._prefix_bundle(post,9);ext=c._prefix_bundle(post,10)
 a=v.events[-1].result;event=ext.events[-1].result
 return b,x,received,a,v,event,ext,post

def write():
 b,x,received,a,v,event,ext,post=replay_capture()
 baseline=c.bundle_bytes(b)
 assert not b.current.receipt_admissions and not b.current.validation_results
 assert received.current.external_gates[0].stage is m.ExternalStage.EVIDENCE_RECEIVED
 assert not received.current.validation_results and not core.resume_eligibility(received,R).allowed
 assert v.current.external_gates[0].stage is m.ExternalStage.EVIDENCE_VALIDATED
 assert a.validation_result.outcome is m.ValidationOutcome.PASS and a.support.observation.accepted
 assert not any(type(z.result) is m.ExternalEvent and z.result.stage is m.ExternalStage.DEPENDENT_ACTION_REENTRY for z in v.events)
 assert not core.resume_eligibility(v,R).allowed
 comp=core.recompute(post.current);assert comp.actionable==(ACTION,) and comp.selection.selected==ACTION
 assert {s.id for s in post.current.statuses if s.state is m.ActionState.COMPLETED}=={s.id for s in b.current.statuses if s.state is m.ActionState.COMPLETED}
 assert post.current.knowledge==b.current.knowledge and post.current.typed_proofs==()
 assert post.current.roots==b.current.roots and post.current.slots==b.current.slots
 assert not any(isinstance(e.result,m.SuppliedResult) for e in post.events[len(b.events):])
 assert set(f.name for f in fields(m.Snapshot)).isdisjoint({'resume_eligibility','eligibility','permission'})
 assert all(type(e.result) is not m.ResumeEligibility for e in post.events)
 eventrecord=ext.events[-1]
 native_checks={'actual_received_Evidence':bool(v.current.receipt_admissions),'receipt_current':gates.check_receipt(v.current,v.current.external_gates[0],x.entity.id).state is m.ProofState.PROVED,'exact_PROVED':gates.obligation_proof(v.current,REQ).state is m.ProofState.PROVED,'exact_prestate':event.expected_snapshot==c.snapshot_id(v.current),'exact_parent':eventrecord.parent_event==v.events[-1].identity,'gate':event.gate==GATE,'named_set':v.current.external_gates[0].reentry==(ACTION,),'source_pins':all(c.load_pinned(R,p) is not None for p in post.sources+(post.policy,)),'context':(post.current.context.scope,post.current.context.lineage,post.current.context.generation)==('E2-QUALIFICATION-ONLY','E2-P03-PROSPECTIVE-QUALIFICATION-1','E2-P03-PROSPECTIVE-GENERATION-1')}
 assert all(native_checks.values())
 negatives=[]
 def reject(name,fn):
  try:fn()
  except (m.PlannerError,TypeError,ValueError) as exc:negatives.append({'name':name,'result':'PASS','rejection':str(exc)})
  else:raise AssertionError('negative accepted: '+name)
 def badstate(name,state):reject(name,lambda:core.resume_eligibility(replace(post,current=state),R))
 reject('proof_unsatisfied_received_only',lambda:c.record_result(received,replace(event,expected_snapshot=c.snapshot_id(received.current))))
 reject('receipt_absent_pre_A09',lambda:c.record_result(b,replace(event,expected_snapshot=c.snapshot_id(b.current))))
 reject('wrong_gate',lambda:c.record_result(v,replace(event,gate=m.GateId('FOREIGN-GATE'))))
 reject('wrong_prestate',lambda:c.record_result(v,replace(event,expected_snapshot=c.snapshot_id(b.current))))
 reject('wrong_parent',lambda:c.append_event(v,replace(eventrecord,parent_event=b.events[-1].identity)))
 reject('foreign_lineage_envelope',lambda:c.append_event(v,replace(eventrecord,parent_snapshot=c.snapshot_id(b.current))))
 reject('conflicting_event_same_identity',lambda:c.append_event(ext,replace(eventrecord,resume_binding=BID)))
 assert c.bundle_bytes(c.append_event(ext,eventrecord))==c.bundle_bytes(ext)
 reject('successful_result_retry_is_stale',lambda:c.record_result(ext,event))
 # A previously admitted identical event is historical idempotence, not a fresh append.
 assert c.bundle_bytes(c.append_event(post,eventrecord))==c.bundle_bytes(post)
 reject('new_event_stale_parent',lambda:c.append_event(post,replace(eventrecord,identity=BID)))
 reject('caller_eligibility_operand',lambda:core.apply_event(v.current,m.ResumeEligibility(True,(ACTION,),(),())))
 wire=c._wire(event);wire['eligibility']=True
 reject('persistent_eligibility_boolean',lambda:c._unwire(wire))
 reject('A11_result_execution_payload',lambda:c._unwire(dict(c._wire(event),ActionResult='PASS')))
 badstate('wrong_receipt',replace(post.current,receipt_admissions=()))
 badstate('wrong_Evidence',replace(post.current,entities=tuple(e for e in post.current.entities if e.id!=x.entity.id)))
 badstate('wrong_ValidationResult',replace(post.current,validation_results=tuple(replace(z,evidence=m.EntityId('WRONG')) for z in post.current.validation_results)))
 badstate('wrong_support',replace(post.current,validation_support_records=()))
 badstate('wrong_named_reentry',replace(post.current,external_gates=tuple(replace(g,reentry=(m.ActionId('E2-FINISH'),)) for g in post.current.external_gates)))
 badstate('unrelated_Action_reopening',replace(post.current,statuses=tuple(replace(z,state=m.ActionState.ACTION_ELIGIBLE) if z.id.value=='E2-FINISH' else z for z in post.current.statuses)))
 for f in ['scope','lineage','generation']:
  badstate('wrong_'+f,replace(post.current,context=replace(post.current.context,**{f:'FOREIGN'})))
 badstate('wrong_provenance',replace(post.current,entities=tuple(replace(e,provenance=replace(e.provenance,excerpt='tampered')) if e.id==x.entity.id else e for e in post.current.entities)))
 assert c.bundle_bytes(c.record_result(v,event))==c.bundle_bytes(ext) # retry after noncommitting negative failure
 invalidations=[]
 identities=[('Evidence_source',x.entity.provenance.identity),('validation/support_definition',a.validation_result.provenance.identity),('gate_source',post.current.external_gates[0].provenance.identity)]
 # Operating decision authority is actual canonical authority; Action.authority=None is legitimate here.
 decision=post.current.decisions[0]
 authorities=[e for e in post.current.entities if e.kind is m.EntityKind.AUTHORITY]
 for authority in authorities:identities.append(('authority_source:'+authority.id.value,authority.provenance.identity))
 for name,identity in identities:
  try:
   withdrawn=c.record_result(post,m.SourceInvalidation((identity,),c.snapshot_id(post.current)))
   eligible=core.resume_eligibility(withdrawn,R)
   expected_allowed=name=='authority_source:E2-GRANT'
   assert eligible.allowed==expected_allowed,(name,eligible)
   assert withdrawn.events[:len(post.events)]==post.events
   invalidations.append({'name':name,'result':'PASS','event':c._wire(withdrawn.events[-1].identity),'eligibility':c._wire(eligible),'expected_allowed':expected_allowed,'classification':'UNRELATED_INVALIDATION_CONTROL' if expected_allowed else 'APPLICABLE_DEPENDENCY_WITHDRAWAL'})
  except m.PlannerError as exc:
   # Invalid canonical projections must not be promoted to usable permission.
   invalidations.append({'name':name,'result':'FAIL_CLOSED_AT_MODEL_ADMISSION','reason':str(exc)})
 assert invalidations
 checks={'accepted_event':True,'exact_named_Action':core.resume_eligibility(post,R).actions==(ACTION,),'no_reasons':not core.resume_eligibility(post,R).reasons,'source_policy_verified':native_checks['source_pins'],'external_obligations':True,'decision_reentry_present':type(post.events[-1].result) is m.DecisionReentry,'binding':all(e.resume_binding==c.resume_binding(post) for e in post.events[-2:]),'current_actionability':ACTION in comp.actionable,'no_Action_completion':True}
 assert all(checks.values())
 checkpoints=[]
 for name,bundle in [('post-A09',received),('post-A10',v),('post-external-A11',ext),('post-complete-A11',post)]:
  path,ident=c.save_bundle(bundle,O/name,R);checkpoints.append({'name':name,'path':str(path.relative_to(R)),'identity':c._wire(ident),'state':c._wire(c.snapshot_id(bundle.current)),'head':c._wire(bundle.events[-1].identity)})
 final=checkpoints[-1];answer=view(post)
 emit('expected-post-A11.json',answer)
 emit('checkpoint-inventory.json',checkpoints)
 emit('a09-candidate.json',c._wire(x));emit('a10-private-admission.json',c._wire(a));emit('a11-event-candidate.json',c._wire(event));emit('a11-event.json',c._wire(eventrecord))
 emit('writer-evidence.json',{'RESULT':'PASS','noncanonical':True,'canonical_bundle':c._wire(BID),'A09_simulation':'PASS','A10_simulation':'PASS','proof_oracle':{'expected':{'state':'PROVED','reasons':[]},'actual':answer['proof'],'proposition':v.current.evidence_requirements[0].proposition,'requirement':REQ.value,'Evidence':c._wire(x.entity.id),'ValidationResult':c._wire(a.validation_result.id),'support':c._wire(a.support.id),'receipt':c._wire(a.command.receipt_reference)},'pre_event_eligibility':c._wire(core.resume_eligibility(v,R)),'external_only_eligibility':c._wire(core.resume_eligibility(ext,R)),'event_preflight':native_checks,'C03':checks,'final':answer,'negative_suite':negatives,'invalidations':invalidations,'retry':'PASS: identical envelope no-op; conflicting/stale fresh envelopes rejected; fresh successful-result retry fails closed','authority_separation':{'Action_authority':None,'meaning':'canonical optional Action authority absent; no nonexistent operating grant fabricated','required_recorded_decision':'E2-DECIDE current and DOWNSTREAM_REEVALUATION after native DecisionReentry','authority_invalidation':invalidations},'A12_initial_oracle':'PASS','named_Action_reopening':'E2-REENTER only','no_A12_execution':True,'no_persisted_eligibility':True,'final_checkpoint':final})
 assert c.bundle_bytes(b)==baseline
 print('isolated writer PASS',flush=True)

def reader():
 inv=c.parse_json((O/'checkpoint-inventory.json').read_bytes());entry=inv[-1]
 actual=read(R/entry['path'],entry['identity'],sys.argv[2]=='reverse' if len(sys.argv)>2 else False)
 expected=c.parse_json((O/'expected-post-A11.json').read_bytes());expected['sources']=sorted(expected['sources'],key=c.canonical_bytes);assert actual==expected
 print(json.dumps({'result':'PASS','bundle':actual['bundle'],'state':actual['state'],'head':actual['head']}))

def reproduce():
 *_,post=construct(reverse=sys.argv[2]=='reverse' if len(sys.argv)>2 else False)
 expected=c.parse_json((O/'expected-post-A11.json').read_bytes());expected['sources']=sorted(expected['sources'],key=c.canonical_bytes);assert view(post)==expected
 print(json.dumps({'result':'PASS','bundle':c._wire(c.bundle_id(post))}))
def reproduce_capture():
 *_,post=construct(reverse=sys.argv[2]=='reverse' if len(sys.argv)>2 else False)
 print(json.dumps({'result':'PASS','view':view(post)}))

def supplement():
 inventory=c.parse_json((O/'checkpoint-inventory.json').read_bytes());z=inventory[-1]
 post=c.restore(R/z['path'],c._unwire(z['identity']),R)
 results=[]
 def reject(name,fn):
  try:fn()
  except (m.PlannerError,TypeError,ValueError) as exc:results.append({'name':name,'result':'PASS','rejection':str(exc)})
  else:raise AssertionError(name)
 wrong=replace(post.current,evidence_requirements=tuple(replace(r,proposition='WRONG PROPOSITION') for r in post.current.evidence_requirements))
 reject('wrong_proposition',lambda:core.resume_eligibility(replace(post,current=wrong),R))
 wrong=replace(post.current,entities=tuple(e for e in post.current.entities if e.id.value!='E2-PROSPECTIVE-CHOICE'))
 reject('required_DECIDE_authority_absent',lambda:core.resume_eligibility(replace(post,current=wrong),R))
 wrong=replace(post.current,validation_instances=tuple(replace(v,currentness=m.ValidationState.STALE) for v in post.current.validation_instances))
 reject('stale_validation_projection',lambda:core.resume_eligibility(replace(post,current=wrong),R))
 wire=c._wire(post.events[-2].result);wire['proof']=True
 reject('cached_Proof_from_another_state_operand',lambda:c._unwire(wire))
 wire=c._wire(post.events[-2].result);wire['dependent_actions']=c._wire((m.ActionId('E2-FINISH'),))
 reject('conflicting_named_Action_payload',lambda:c._unwire(wire))
 missing=core.resume_eligibility(post,R/'docs/plans/qualification/REENTRY_R04_1/missing-source-root')
 assert not missing.allowed and any('SOURCE_PIN_FAILED' in r for r in missing.reasons)
 results.append({'name':'wrong_physical_source_root','result':'PASS','eligibility':c._wire(missing)})
 ext=c._prefix_bundle(post,10);pre=c._prefix_bundle(post,9)
 delta=[after.id.value for after in ext.current.statuses if after!=next(z for z in pre.current.statuses if z.id==after.id)]
 assert delta==['E2-REENTER']
 emit('supplemental-negative-results.json',{'RESULT':'PASS','negative_suite':results,'exact_status_delta':delta,'required_authority':'recorded choice DECIDE; optional Action.authority is None and not invented'})
 print('supplemental boundary checks PASS')

def ordering_counterexample():
 inventory=c.parse_json((O/'checkpoint-inventory.json').read_bytes());z=inventory[-1]
 post=c.restore(R/z['path'],c._unwire(z['identity']),R)
 record=post.current.validation_results[0];assert len(record.input_identities)>1
 assert 'input_identities' in c.SET_FIELDS[type(record)]
 changed=replace(record,input_identities=tuple(reversed(record.input_identities)))
 state=replace(post.current,validation_results=tuple(changed if r.id==record.id else r for r in post.current.validation_results))
 cased=replace(post,current=state)
 assert c.canonical_bytes(c._wire(state))==c.canonical_bytes(c._wire(post.current))
 assert c._bundle_bytes_admitted(cased)==c._bundle_bytes_admitted(post)
 m.validate_model(post.current)
 try:m.validate_model(state)
 except m.PlannerError as exc:reason=str(exc)
 else:raise AssertionError('expected recorded ordering defect not reproduced')
 assert reason=='VALIDATION_PROJECTION_REQUIRED'
 emit('ordering-counterexample.json',{'RESULT':'FAIL_REQUIRED_ORDERING_DIMENSION','classification':'CODEC_MODEL_ORDERING_INCONSISTENCY','minimal_mutation':'reverse only validation_results[0].input_identities, declared unordered','record':c._wire(record.id),'original_inputs':c._wire(record.input_identities),'permuted_inputs':c._wire(changed.input_identities),'native_declared_set':True,'canonical_snapshot_bytes_equal':True,'canonical_bundle_bytes_equal':True,'expected':'model admission passes for equal canonical presentation','actual':reason,'source':'validation_transaction.validate_records: inst.inputs == r.input_identities','Proof_C03':'public model admission fails before computation','runtime_modified':False,'canonical_P04_modified':False})
 print('minimal unordered-set counterexample reproduced')

if __name__=='__main__':
 {'write':write,'read':reader,'reproduce':reproduce,'reproduce_capture':reproduce_capture,'supplement':supplement,'ordering_counterexample':ordering_counterexample}[sys.argv[1]]()
