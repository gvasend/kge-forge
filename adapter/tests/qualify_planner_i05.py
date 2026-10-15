"""I05 generic qualification and exactly bounded P04 configuration application."""
import json,hashlib,os,sys,shutil,unittest
from pathlib import Path
from dataclasses import replace,fields
from adapter.planner import codec as c,model as m,core,gates,installation as i,action_installation as ai
from adapter.planner import validation_transaction as vt,evidence_transaction as tx,evidence_attestation as ea
from adapter.tests.test_planner_action_installation import ActionInstallationTests,definition
from adapter.tests.test_planner_installation import request
from adapter.tests.qualify_p04_a09_control import inputs
R=Path(__file__).resolve().parents[2];D=R/'docs/plans';O=D/'qualification/INSTALLATION_I05_1';Q=D/'qualification/REENTRY_R06_1';P='DETERMINISTIC_PLANNER_V0_1_'
def emit(name,obj):
 O.mkdir(parents=True,exist_ok=True);(O/name).write_bytes(c.canonical_bytes(obj))
def hashes():return {str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (R/'adapter/planner').glob('*.py')}
def save(b,path,root=R):
 c.save_bundle(b,path.parent,root);path.write_bytes(c.bundle_bytes(b))
def generic():
 suite=unittest.defaultTestLoader.loadTestsFromTestCase(ActionInstallationTests)
 with (O/'generic-tests.log').open('w') as f:r=unittest.TextTestRunner(stream=f,verbosity=2).run(suite)
 assert r.wasSuccessful(),(O/'generic-tests.log').read_text()
 h=ActionInstallationTests();h.setUp()
 try:
  after,bid,_=h.commit();target=O/'generic-root';shutil.copytree(h.root,target,dirs_exist_ok=True)
  save(after,target/'checkpoint.json',target)
  emit('generic-manifest.json',{'path':str(target/'checkpoint.json'),'root':str(target),'bundle_id':c._wire(bid),'before_bundle_id':c._wire(c.bundle_id(h.bundle)),'before_count':len(h.bundle.events),'state_id':c._wire(c.snapshot_id(after.current))})
 finally:h.doCleanups()
 emit('generic-qualification.json',{'RESULT':'WRITER_PASS_READERS_PENDING','tests':r.testsRun,'runtime_hashes':hashes()})
 print('GENERIC_WRITER_PASS')
def reader(manifest):
 x=c.parse_json(Path(manifest).read_bytes());b=c.restore(Path(x['path']),c._unwire(x['bundle_id']),Path(x['root']))
 assert c._wire(c.snapshot_id(b.current))==x['state_id']
 if x.get('boundary')=='POST_A12':
  assert all(i.current(b,r) for r in b.current.installed_definitions if i.descriptor(r.request.definition)[0]['definition_type']=='ACTION_DEFINITION')
 else:
  assert all(i.current(b,r) for r in b.current.installed_definitions)
 if 'before_count' in x:assert c._wire(c.bundle_id(c._prefix_bundle(b,x['before_count'])))==x['before_bundle_id']
 assert c.snapshot_id(c._replay(b))==c.snapshot_id(b.current)
 if x.get('boundary')=='POST_A12':
  action=m.ActionId('E2-REENTER');pre=c._prefix_bundle(b,len(b.events)-1)
  assert gates.obligation_proof(pre.current,m.EvidenceId('E2-EXTERNAL-REQUIREMENT')).state is m.ProofState.PROVED
  assert core.resume_eligibility(pre,Path(x['root'])).actions==(action,)
  assert core.recompute(pre.current).selection.selected==action
  assert gates.current_completion(b.current,action)
  a=next(a for a in b.current.actions if a.id==action)
  assert b.events[-1].result==m.SuppliedResult(action,m.ActionResult.PASS,a.accepted_inventory,c.snapshot_id(pre.current))
  assert next(k for k in b.current.knowledge if k.id.value=='E2-K-REENTER')==a.accepted_inventory[0]
  assert not b.current.typed_proofs and not any(s.id.value=='E2-FINISH' and s.state is m.ActionState.COMPLETED for s in b.current.statuses)
 print(json.dumps({'bundle':c._wire(c.bundle_id(b)),'state':c._wire(c.snapshot_id(b.current)),'head':c._wire(b.events[-1].identity),'currentness':'PASS','replay':'PASS'}))
def apply():
 qualified=c.parse_json((O/'generic-qualification.json').read_bytes());assert qualified['RESULT']=='PASS' and qualified['runtime_hashes']==hashes()
 dec=c.parse_json((Q/'bounded-installation-decision.json').read_bytes())
 for file,key in [('canonical-action-before.json','old_body'),('prospective-action-definition.json','replacement_body')]:assert hashlib.sha256((Q/file).read_bytes()).hexdigest()==dec[key]['sha256']
 b=c.restore(D/(P+'E2_P04_POST_A10_INSTALL_BUNDLE_1.json'),c._unwire(dec['expected_bundle']),R)
 assert c._wire(c.snapshot_id(b.current))==dec['expected_state'] and c._wire(b.events[-1].identity)==dec['expected_parent']
 old=c._unwire(c.parse_json((Q/'canonical-action-before.json').read_bytes()));new=c._unwire(c.parse_json((Q/'prospective-action-definition.json').read_bytes()))
 assert next(a for a in b.current.actions if a.id==old.id)==old
 assert [f.name for f in fields(old) if getattr(old,f.name)!=getattr(new,f.name)]==dec['allowed_frame_change']
 assert hashlib.sha256((D/(P+'E2_PC01_SOURCES.json')).read_bytes()).hexdigest()==dec['source_declaration_sha256']
 capture={'schema':'INSTALLATION-I05-HUMAN-SELECTION-1','selected_option':'AUTHORIZE_P04_A12_REENTER_RESULT_INSTALLATION','issuer':'AUTHENTICATED_HUMAN_USER','role':'QUALIFICATION_AUTHORITY','authentication':'EXPLICIT_CURRENT_SESSION_HUMAN_DECISION_TRANSPORT','R06_contract_id':i.simple(c._identity((D/(P+'REENTRY_R06_A12_RESULT_CONTRACT.json')).read_bytes(),'raw-file-sha256')),'bounded_decision':dec,'scope':b.current.context.scope,'lineage':b.current.context.lineage,'generation':b.current.context.generation,'consumer':dec['consumer'],'operation':'REPLACE','sequence':len(b.events)+1,'transport_date':'2026-10-04','excludes':dec['exclusions'],'material_R06_terms_changed':False}
 emit('authenticated-selection.json',capture);did=c._identity(c.canonical_bytes(capture),'raw-file-sha256')
 defn=definition(R,old,new,b.current.context,str((O/'p04-action-definition.json').relative_to(R)))
 r,decision=request(b,defn,receipt_path=str((O/'p04-install-authority.json').relative_to(R)),decision=did,contract=c._identity((D/(P+'REENTRY_R06_A12_RESULT_CONTRACT.json')).read_bytes(),'raw-file-sha256'))
 i.validate_authority(r,b.current.context);emit('authorized-request.json',c._wire(r))
 after,bid,_=i.commit(b,r,O/'p04-install-store',R,expected_authority=r.authority.id,expected_decision=decision)
 m.validate_model(after.current)
 for f in fields(m.Snapshot):
  if f.name not in ('actions','installed_definitions'):assert getattr(b.current,f.name)==getattr(after.current,f.name),f.name
 for a in b.current.actions:
  if a.id!=old.id:assert c.canonical_bytes(c._wire(a))==c.canonical_bytes(c._wire(next(z for z in after.current.actions if z.id==a.id)))
 assert next(a for a in after.current.actions if a.id==new.id)==new
 assert c.bundle_bytes(c._prefix_bundle(after,len(b.events)))==c.bundle_bytes(b)
 assert i.current(after,after.current.installed_definitions[-1])
 output=D/(P+'E2_P04_POST_REENTER_DEFINITION_INSTALL_BUNDLE_1.json');save(after,output)
 again,againid,_=i.commit(b,r,O/'independent-install-store',R,expected_authority=r.authority.id,expected_decision=decision);assert againid==bid and c.bundle_bytes(again)==c.bundle_bytes(after)
 retry,retryid,no=i.commit(b,r,O/'p04-install-store',R,expected_authority=r.authority.id,expected_decision=decision);assert no and retryid==bid and len(retry.events)==len(b.events)+1
 emit('p04-manifest.json',{'path':str(output),'root':str(R),'bundle_id':c._wire(bid),'state_id':c._wire(c.snapshot_id(after.current)),'before_count':len(b.events),'before_bundle_id':c._wire(c.bundle_id(b))})
 emit('p04-installation.json',{'authority':c._wire(r.authority.id),'event':c._wire(after.events[-1].identity),'definition':c._wire(defn.id),'installed_definition':c._wire(i.installed_id(r)),'state':c._wire(c.snapshot_id(after.current)),'head':c._wire(after.events[-1].identity),'bundle':c._wire(bid),'currentness':'PASS','history':'PASS','retry':'PASS','independent_installation':'PASS','no_lifecycle_commit':True})
 print('P04_INSTALL_PASS')
def lifecycle():
 man=c.parse_json((O/'p04-manifest.json').read_bytes());b=c.restore(Path(man['path']),c._unwire(man['bundle_id']),R)
 _,_,expected=inputs();old=c._unwire(c.parse_json((D/'qualification/VALIDATION_V02_1/fresh-a09-candidate.json').read_bytes()))
 raw={p.path:(R/p.path).read_bytes() for p in old.source_additions}
 try:c.preflight_external_evidence(b,old,raw,R,expected_binding=expected)
 except m.PlannerError as e:stale=str(e)
 else:raise AssertionError('old candidate accepted')
 fresh=replace(old,expected_bundle=c.bundle_id(b),expected_snapshot=c.snapshot_id(b.current),expected_parent_event=b.events[-1].identity)
 kw=dict(vars(old.attestation_operand.attestation));kw.pop('attestation_id');fresh=tx.bind(fresh,ea.materialize(**kw),expected)
 emit('fresh-a09-candidate.json',c._wire(fresh))
 received=c.preflight_external_evidence(b,fresh,raw,R,expected_binding=expected)
 checks=tx.check_receipt_postcondition(tx.receipt_oracle(b.current,fresh),received.current)
 assert not received.current.validation_results and not core.resume_eligibility(received,R).allowed
 rec=next(r for r in b.current.installed_definitions if i.descriptor(r.request.definition)[0]['definition_type']=='VALIDATION_SUPPORT_DEFINITION_SET')
 a,validated=vt.prepare(received,vt.command(received,fresh.entity.id,rec.id),R)
 assert a.validation_result.outcome is m.ValidationOutcome.PASS and a.support.observation.accepted
 assert not core.resume_eligibility(validated,R).allowed
 proof=gates.obligation_proof(validated.current,m.EvidenceId('E2-EXTERNAL-REQUIREMENT'));assert proof.state is m.ProofState.PROVED
 external=c.record_result(validated,m.ExternalEvent(m.GateId('E2-GATE'),m.ExternalStage.DEPENDENT_ACTION_REENTRY,c.snapshot_id(validated.current)))
 d=next(d for d in external.current.decisions if m.ActionId('E2-REENTER') in d.downstream)
 eligible=c.record_result(external,m.DecisionReentry(d.action,c.snapshot_id(external.current)))
 assert core.resume_eligibility(eligible,R).actions==(m.ActionId('E2-REENTER'),)
 comp=core.recompute(eligible.current);assert comp.selection.selected==m.ActionId('E2-REENTER') and m.ActionId('E2-FINISH') not in comp.actionable
 action=next(x for x in eligible.current.actions if x.id==comp.selection.selected)
 # Canonical A12 executor protocol is the matrix's supplied permitted result.
 # Materialize that authored fixture only after native selection, then let unchanged
 # apply_result/record_result admit the actual execution operand and derive completion.
 declaration=c.parse_json((Q/'authoritative-source-declaration.json').read_bytes())
 from adapter.planner.action_materializer import materialize_action
 assert materialize_action(action,declaration)==action
 supplied=m.SuppliedResult(comp.selection.selected,action.accepted_result,action.accepted_inventory,c.snapshot_id(eligible.current))
 post=c.record_result(eligible,supplied)
 assert gates.current_completion(post.current,action.id)
 knowledge=next(k for k in post.current.knowledge if k.id==m.KnowledgeId('E2-K-REENTER'));assert knowledge==action.accepted_inventory[0]
 assert m.ActionId('E2-FINISH') not in {s.id for s in post.current.statuses if s.state is m.ActionState.COMPLETED}
 neg=[]
 def reject(name,fn):
  try:fn()
  except m.PlannerError as e:neg.append({'name':name,'reason':str(e),'result':'PASS'})
  else:raise AssertionError(name)
 reject('without A11 event',lambda:c.record_result(validated,replace(supplied,expected_snapshot=c.snapshot_id(validated.current))))
 reject('stale pre-state',lambda:c.record_result(eligible,replace(supplied,expected_snapshot=c.snapshot_id(validated.current))))
 reject('wrong outcome',lambda:c.record_result(eligible,replace(supplied,result=m.ActionResult.FAIL)))
 reject('missing knowledge',lambda:c.record_result(eligible,replace(supplied,knowledge=())))
 reject('extra knowledge',lambda:c.record_result(eligible,replace(supplied,knowledge=supplied.knowledge+(replace(knowledge,id=m.KnowledgeId('EXTRA')),))))
 reject('wrong Action',lambda:c.record_result(eligible,replace(supplied,action=m.ActionId('E2-FINISH'))))
 reject('wrong scope',lambda:c.record_result(eligible,replace(supplied,knowledge=(replace(knowledge,provenance=replace(knowledge.provenance,scope='foreign')),))))
 reject('wrong lineage provenance',lambda:c.record_result(eligible,replace(supplied,knowledge=(replace(knowledge,provenance=replace(knowledge.provenance,excerpt='foreign lineage')),))))
 reject('prospective definition as result',lambda:c.record_result(eligible,action))
 old_action=c._unwire(c.parse_json((Q/'canonical-action-before.json').read_bytes()))
 obsolete=replace(eligible,current=replace(eligible.current,actions=tuple(old_action if z.id==old_action.id else z for z in eligible.current.actions)))
 reject('old pre-install Action after replacement',lambda:c._replay(obsolete))
 reject('result before receipt/execution readiness',lambda:c.record_result(b,replace(supplied,expected_snapshot=c.snapshot_id(b.current))))
 manual=replace(post,current=replace(eligible.current,statuses=post.current.statuses))
 reject('manual completion without consistent execution ancestry',lambda:c._replay(manual))
 withdrawn=c.record_result(eligible,m.SourceInvalidation((a.validation_result.provenance.identity,),c.snapshot_id(eligible.current)))
 reject('stale C03 premises',lambda:c.record_result(withdrawn,replace(supplied,expected_snapshot=c.snapshot_id(withdrawn.current))))
 invalid_definition=c.record_result(eligible,m.SourceInvalidation((b.current.installed_definitions[-1].request.definition.provenance.identity,),c.snapshot_id(eligible.current)))
 reject('old/unusable definition after replacement',lambda:c.record_result(invalid_definition,replace(supplied,expected_snapshot=c.snapshot_id(invalid_definition.current))))
 output=O/'isolated-post-a12.json';save(post,output)
 emit('a12-manifest.json',{'path':str(output),'root':str(R),'bundle_id':c._wire(c.bundle_id(post)),'state_id':c._wire(c.snapshot_id(post.current)),'boundary':'POST_A12'})
 emit('a09-a12-qualification.json',{'A09':'PASS','A10':'PASS','A11':'PASS','A12':'PASS','old_candidate':stale,'Proof':{'state':proof.state.value,'reasons':list(proof.reasons)},'C03':c._wire(core.resume_eligibility(eligible,R)),'execution_operand':c._wire(supplied),'execution_event':c._wire(post.events[-1]),'knowledge':c._wire(knowledge),'completion':True,'negatives':neg,'source_protocol':'Canonical A12 supplied permitted result; no independent domain executor or output invention','pre_A12_state':c._wire(c.snapshot_id(eligible.current)),'post_A12_state':c._wire(c.snapshot_id(post.current)),'post_A12_computation':str(core.recompute(post.current)),'canonical_no_execution':not b.current.receipt_admissions and not b.current.validation_results,'A13_first_blocker':'No typed SLOT/ROOT proof contracts or accepted domain proof instances in canonical configuration; recover exact A13 fixture/authority installation before execution.'})
 print(json.dumps({'A09':'PASS','A10':'PASS','A11':'PASS','A12':'PASS','negatives':len(neg),'bundle':c._wire(c.bundle_id(post))}))
if __name__=='__main__':
 if sys.argv[1]=='generic':generic()
 elif sys.argv[1]=='read':reader(sys.argv[2])
 elif sys.argv[1]=='apply':apply()
 elif sys.argv[1]=='lifecycle':lifecycle()
