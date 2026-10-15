"""Bounded F03 configuration application and isolated A09-A13 qualification."""
import sys,json,hashlib,os,unittest,shutil,tempfile
from dataclasses import replace,fields,is_dataclass
from enum import Enum
from pathlib import Path
from adapter.planner import codec as c,model as m,core,gates,installation as i
from adapter.planner import proof_installation as pi,typed_proofs as tp
from adapter.planner import evidence_transaction as tx,evidence_attestation as ea,validation_transaction as vt
from adapter.tests.test_planner_installation import request as base_request
from adapter.tests.test_planner_proof_installation import load_definition,with_sources,ProofInstallationTests
from adapter.tests.test_planner_typed_proofs import candidate
from adapter.tests.qualify_p04_a09_control import inputs,view
R=Path(__file__).resolve().parents[2];D=R/'docs/plans';Q=D/'qualification/FINISH_F02_1';O=D/'qualification/FINISH_F03_1';P='DETERMINISTIC_PLANNER_V0_1_'
F= c.parse_json((Q/'sealed-manifest.json').read_bytes())
def emit(name,value):
 O.mkdir(parents=True,exist_ok=True);path=O/name;raw=c.canonical_bytes(value)
 if path.exists() and path.read_bytes()==raw:return
 fd,temporary=tempfile.mkstemp(prefix='.qualification-',dir=str(O))
 try:
  with os.fdopen(fd,'wb') as stream:stream.write(raw);stream.flush();os.fsync(stream.fileno())
  os.replace(temporary,path)
 finally:
  if os.path.exists(temporary):os.unlink(temporary)
def computation_wire(value):
 if type(value).__name__ in c.TYPES:return c._wire(value)
 if is_dataclass(value):return {'native_type':type(value).__name__,**{f.name:computation_wire(getattr(value,f.name)) for f in fields(value)}}
 if isinstance(value,Enum):return {'native_enum':type(value).__name__,'value':value.value}
 if isinstance(value,(tuple,list)):return [computation_wire(v) for v in value]
 if isinstance(value,dict):return {k:computation_wire(v) for k,v in value.items()}
 if value is None or type(value) in (str,bool,int):return value
 raise TypeError(type(value))
def semantic_view(b,root=R):
 s=b.current
 return {'computation':computation_wire(core.recompute(s)),
 'obligation_proof':computation_wire(gates.obligation_proof(s,s.evidence_requirements[0].id)) if s.evidence_requirements else None,
 'resume':c._wire(core.resume_eligibility(b,root)),
 'sources':sorted(c._wire(b.sources),key=c.canonical_bytes),'policy':c._wire(b.policy),'policy_version':b.policy_version,
 'context':c._wire(s.context),'ledger_root':c._wire(b.events[0].identity),
 'typed_proof_usability':[{'id':c._wire(p.id),'usable':tp.usable(s,p)} for p in sorted(s.typed_proofs,key=lambda p:p.id.sha256)]}
def save(b,path,root=R):
 stored,bid=c.save_bundle(b,path.parent,root);path.write_bytes(stored.read_bytes());return {'path':str(path),'root':str(root),'writer_pid':os.getpid(),'writer_pid_namespace':os.readlink('/proc/self/ns/pid'),'writer_command':sys.argv,'bundle_id':c._wire(bid),'state_id':c._wire(c.snapshot_id(b.current)),'head':c._wire(b.events[-1].identity),'event_count':len(b.events),'boundary':path.stem}
def record_trace(before,after,label):
 comp=core.recompute(after.current)
 return {'stage':label,'pre_state':c._wire(c.snapshot_id(before.current)),'post_state':c._wire(c.snapshot_id(after.current)),'parent':c._wire(before.events[-1].identity),'head':c._wire(after.events[-1].identity),'event_count':len(after.events),'control':comp.control.value,'actionable':[a.value for a in comp.actionable]}
def selections():
 x=c.parse_json((O/'authenticated-decisions.json').read_bytes())
 for item in x['sealed_subjects'].values():assert hashlib.sha256(Path(item['path']).read_bytes()).hexdigest()==item['sha256']
 resolution={'status':'RESOLVED_BY_EXPLICIT_HUMAN_CLARIFICATION','clarification':'retain that sealed oracle and qualify the remaining path','oracle':'Retain F02 PLAN_DEFECT before root proof; no control/goal rewrite'}
 if 'scope_conflict' in x:assert x['scope_conflict']==resolution
 else:x['scope_conflict']=resolution;emit('authenticated-decisions.json',x)
 return x,c._identity(c.canonical_bytes(x),'raw-file-sha256')
def generic():
 with (O/'generic-tests.log').open('w') as f:r=unittest.TextTestRunner(stream=f,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(ProofInstallationTests))
 assert r.wasSuccessful(),(O/'generic-tests.log').read_text()
 emit('generic-qualification.json',{'result':'PASS','tests':r.testsRun,'hashes':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in (R/'adapter/planner').glob('*.py')}})
 print('GENERIC_PASS',r.testsRun,flush=True)
def generic_checkpoint():
 h=ProofInstallationTests();h.setUp()
 try:
  *_,target=h.lifecycle();folder=O/'generic-root'
  shutil.copytree(h.root,folder,dirs_exist_ok=True)
  man=save(target,folder/'generic-qualified.json',folder)
  man['semantic_oracle']=semantic_view(target,folder);man['writer_terminated']=True
  emit('generic-reader-manifest.json',man)
 finally:h.doCleanups()
 print('GENERIC_CHECKPOINT_PASS',flush=True)
def repersist():
 for name in ('configuration-manifest.json','generic-reader-manifest.json'):
  man=c.parse_json((O/name).read_bytes());root=Path(man.get('root',str(R)));b=c.restore(Path(man['path']),c._unwire(man['bundle_id']),root)
  # Exact immutable state republication records a terminated writer process;
  # it neither reissues authority nor reexecutes an installation or lifecycle.
  saved=save(b,Path(man['path']),root);man.update(saved);emit(name,man)
 print('EXACT_PERSISTENCE_WRITER_PASS',os.getpid(),flush=True)
def semantic_binding(defn,decision):
 d,body=i.descriptor(defn)
 grant={'schema':'PLANNER-FIXTURE-SEMANTIC-GRANT-1','issuer':'QUALIFICATION_AUTHORITY','authority_class':'DECIDE','decision_id':i.simple(decision),'semantic_request_id':F['semantic_authority_request']['content_id'],'configuration_definition_id':i.simple(defn.id),'scope':d['scope'],'lineage':d['lineage'],'generation':d['generation'],'consumer':body['consumer'],'valid_from':0,'valid_until':body['valid_until'],'delegation':False,'automatic_issuance_by_install':False,'sources':body['sources'],'policies':body['semantic_policies'],'authority_specs':body['semantic_authority_specs']}
 gid=i.digest(grant,'planner-fixture-semantic-authorization-v1',m.IdentityKind.AUTHORITY_IDENTITY)
 x=pi.admit_semantic_authority(grant,expected_grant=gid,expected_decision=decision,trusted_issuer='QUALIFICATION_AUTHORITY',receipt_path=str((O/'semantic-admission.json').relative_to(R)))
 emit('semantic-binding.json',c._wire(x));return x

def install(b,index,decision,bind=(),store=None):
 item=F['installable_definitions'][index];df=load_definition(R,item)
 r,_=base_request(b,df,m.InstallationOperation.REPLACE if index==1 else m.InstallationOperation.INSTALL,receipt_path=str((O/('install-authority-'+str(index)+'.json')).relative_to(R)),decision=decision,contract=c._identity((Q/'bounded-installation-workflow.json').read_bytes(),'raw-file-sha256'))
 if index==1:
  ps=i.request_provenances(r);r=replace(r,source_additions=tuple(dict.fromkeys(m.ArtifactPin(p.path,p.identity) for p in ps if m.ArtifactPin(p.path,p.identity) not in b.sources)));r=replace(r,command_key=i.command_key(r))
 else:r=with_sources(R,b,df,r,bind)
 i.validate_authority(r,b.current.context)
 kw={'expected_authority':r.authority.id,'expected_decision':decision}
 if bind:kw['expected_operating_authority']=bind[0].operating_authorization_id
 after,ident,_=i.commit(b,r,store or O/('install-store-'+str(index)),R,**kw)
 assert i.current(after,after.current.installed_definitions[-1]);emit('install-request-'+str(index)+'.json',c._wire(r))
 retry,bid,no=i.commit(b,r,store or O/('install-store-'+str(index)),R,**kw);assert no and bid==ident and c.bundle_bytes(retry)==c.bundle_bytes(after)
 return after,r

def apply():
 qualified=c.parse_json((O/'generic-qualification.json').read_bytes());assert qualified['result']=='PASS'
 assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in qualified['hashes'].items())
 _,did=selections();base=D/(P+'E2_P04_POST_REENTER_DEFINITION_INSTALL_BUNDLE_1.json')
 b=c.restore(base,i.identity(F['initial_checkpoint']['bundle_id']),R)
 assert i.simple(c.snapshot_id(b.current))==F['initial_checkpoint']['state_id'] and i.simple(b.events[-1].identity)==F['initial_checkpoint']['append_head']
 df=load_definition(R,F['installable_definitions'][0]);binding=semantic_binding(df,did)
 a,req1=install(b,0,did,(binding,));z,req2=install(a,1,did)
 assert b.current.statuses==a.current.statuses==z.current.statuses
 assert not z.current.proof_contracts and not z.current.typed_proofs and not z.current.validation_results and not z.current.receipt_admissions
 assert not z.current.knowledge or z.current.knowledge==b.current.knowledge
 assert z.current.goals==b.current.goals;assert z.current.slots[0].state is m.SlotState.UNRESOLVED;assert z.current.roots[0].state is m.ConditionState.UNRESOLVED
 fin=next(a for a in z.current.actions if a.id.value=='E2-FINISH');old=next(a for a in b.current.actions if a.id==fin.id)
 assert fin.accepted_inventory==old.accepted_inventory and not fin.blocked_terminal and fin.pass_model_complete
 assert m.ActionId('E2-FINISH') not in core.recompute(z.current).actionable
 path=D/(P+'E2_P04_FINAL_PREEXECUTION_CONFIGURATION_BUNDLE_1.json');manifest=save(z,path)
 manifest.update(before_count=len(b.events),before_bundle_id=c._wire(c.bundle_id(b)),semantic_grant=c._wire(binding.operating_authorization_id))
 emit('configuration-manifest.json',manifest)
 emit('configuration-trace.json',[record_trace(b,a,'configuration/source/slot'),record_trace(a,z,'FINISH root prerequisite/nonterminal hold')])
 assert c.bundle_bytes(c._prefix_bundle(z,len(b.events)))==c.bundle_bytes(b)
 print('CANONICAL_CONFIG_PASS',flush=True)

def lifecycle(store_suffix='',reproduction=False):
 _,did=selections();man=c.parse_json((O/'configuration-manifest.json').read_bytes());b=c.restore(Path(man['path']),c._unwire(man['bundle_id']),R)
 _,_,expected=inputs();old=c._unwire(c.parse_json((D/'qualification/INSTALLATION_I05_1/fresh-a09-candidate.json').read_bytes()))
 raw={p.path:(R/p.path).read_bytes() for p in old.source_additions}
 try:c.preflight_external_evidence(b,old,raw,R,expected_binding=expected)
 except m.PlannerError as e:stale=str(e)
 else:raise AssertionError('old candidate current')
 fresh=replace(old,expected_bundle=c.bundle_id(b),expected_snapshot=c.snapshot_id(b.current),expected_parent_event=b.events[-1].identity)
 kw=dict(vars(old.attestation_operand.attestation));kw.pop('attestation_id');fresh=tx.bind(fresh,ea.materialize(**kw),expected);emit('fresh-a09-candidate.json',c._wire(fresh))
 received=c.preflight_external_evidence(b,fresh,raw,R,expected_binding=expected)
 expected_receipt=tx.receipt_oracle(b.current,fresh)
 tx.check_receipt_postcondition(expected_receipt,received.current)
 actual=view(received);entity=next(e for e in received.current.entities if e.id==fresh.entity.id)
 a09_checks={'control':actual['control']=='EXTERNAL_WAIT','actionable':actual['actionable']==[],
 'selected':actual['selected'] is None,'decision_ready':actual['decision_ready']==[],
 'received':actual['gate'][0]['stage']=='EVIDENCE_RECEIVED' and actual['gate'][0]['pending']==fresh.entity.id.value,
 'unvalidated':not entity.validated and entity.validation is m.ValidationState.NOT_EVALUATED,
 'no_validation':received.current.validation_instances==b.current.validation_instances,
 'no_proof':received.current.typed_proofs==b.current.typed_proofs,
 'no_proof_contract_admission':received.current.proof_contracts==b.current.proof_contracts,
 'no_observation_acceptance':received.current.receipt_observations==b.current.receipt_observations,
 'no_resume':not actual['resume_allowed'],'no_external_complete':not actual['gate'][0]['external_complete'],
 'no_knowledge':received.current.knowledge==b.current.knowledge,
 'root_slot_unchanged':received.current.roots==b.current.roots and received.current.slots==b.current.slots,
 'no_action_completion':{s.id for s in received.current.statuses if s.state is m.ActionState.COMPLETED}=={s.id for s in b.current.statuses if s.state is m.ActionState.COMPLETED},
 'two_private_events':len(received.events)==len(b.events)+2,
 'canonical_unchanged':c.bundle_bytes(b)==Path(man['path']).read_bytes(),
 'no_canonical_commit':True}
 assert len(a09_checks)==18 and all(a09_checks.values()),a09_checks
 emit('a09-precommit-oracle.json',a09_checks)
 validation=next(r for r in b.current.installed_definitions if i.descriptor(r.request.definition)[0]['definition_type']=='VALIDATION_SUPPORT_DEFINITION_SET')
 operand,validated=vt.prepare(received,vt.command(received,fresh.entity.id,validation.id),R)
 assert operand.validation_result.outcome is m.ValidationOutcome.PASS and operand.support.observation.accepted and not core.resume_eligibility(validated,R).allowed
 proof=gates.obligation_proof(validated.current,m.EvidenceId('E2-EXTERNAL-REQUIREMENT'));assert proof.state is m.ProofState.PROVED
 external=c.record_result(validated,m.ExternalEvent(m.GateId('E2-GATE'),m.ExternalStage.DEPENDENT_ACTION_REENTRY,c.snapshot_id(validated.current)))
 d=next(d for d in external.current.decisions if m.ActionId('E2-REENTER') in d.downstream)
 eligible=c.record_result(external,m.DecisionReentry(d.action,c.snapshot_id(external.current)))
 assert core.resume_eligibility(eligible,R).actions==(m.ActionId('E2-REENTER'),)
 comp=core.recompute(eligible.current);assert comp.selection.selected==m.ActionId('E2-REENTER') and m.ActionId('E2-FINISH') not in comp.actionable
 action=next(a for a in eligible.current.actions if a.id==comp.selection.selected)
 post=c.record_result(eligible,m.SuppliedResult(action.id,action.accepted_result,action.accepted_inventory,c.snapshot_id(eligible.current)))
 assert gates.current_completion(post.current,action.id) and next(k for k in post.current.knowledge if k.id==m.KnowledgeId('E2-K-REENTER'))==action.accepted_inventory[0]
 assert core.recompute(post.current).control is m.ControlState.PLAN_DEFECT  # Explicit human clarification preserves F02 oracle.
 assert not post.current.typed_proofs and m.ActionId('E2-FINISH') not in core.recompute(post.current).actionable
 print('A09_A12_ISOLATED_PASS',flush=True)
 slot_contract,sr=install(post,2,did,store=O/('isolated-slot-store'+store_suffix))
 sc=c._unwire(c.parse_json(Path(F['proof_definitions'][0]['path']).read_bytes())['contract'])
 slot=c.record_result(slot_contract,m.TypedProofAdmission(candidate(sc),c.snapshot_id(slot_contract.current)))
 assert slot.current.slots[0].state is m.SlotState.RESOLVED and slot.current.roots[0].state is m.ConditionState.UNRESOLVED and m.ActionId('E2-FINISH') not in core.recompute(slot.current).actionable
 root_contract,rr=install(slot,3,did,store=O/('isolated-root-store'+store_suffix))
 rc=c._unwire(c.parse_json(Path(F['proof_definitions'][1]['path']).read_bytes())['contract'])
 root=c.record_result(root_contract,m.TypedProofAdmission(candidate(rc),c.snapshot_id(root_contract.current)))
 recomputed=core.recompute(root.current);assert root.current.roots[0].state is m.ConditionState.SATISFIED and recomputed.selection.selected==m.ActionId('E2-FINISH') and recomputed.control is m.ControlState.RUNNABLE
 assert all(s.state is m.ActionState.COMPLETED for s in root.current.statuses if s.id.value!='E2-FINISH')
 fin=next(a for a in root.current.actions if a.id==recomputed.selection.selected)
 supplied=m.SuppliedResult(fin.id,fin.accepted_result,fin.accepted_inventory,c.snapshot_id(root.current));target=c.record_result(root,supplied)
 assert gates.current_completion(target.current,fin.id) and next(k for k in target.current.knowledge if k.id.value=='E2-K-FINISH')==fin.accepted_inventory[0]
 assert core.recompute(target.current).control is m.ControlState.TERMINAL_SUCCESS and all(s.state is m.ActionState.COMPLETED for s in target.current.statuses)
 stages={'post-a09':received,'post-a10':validated,'post-a11':eligible,'post-a12':post,'slot-contract':slot_contract,'post-slot-proof':slot,'root-contract':root_contract,'post-root-proof':root,'isolated-p04-target':target}
 if reproduction:
  target_path=O/'reproductions'/store_suffix/'target.json';target_path.parent.mkdir(parents=True,exist_ok=True)
  manifest=save(target,target_path)
  # Compare admitted bytes and complete recomputed outputs; event causal order
  # stays ordered while the codec's declared unordered collections canonicalize.
  references=c.parse_json((O/'isolated-checkpoints.json').read_bytes());comparisons={}
  for name,bundle in stages.items():
   reference=c._unwire(c.parse_json(Path(references[name]['path']).read_bytes())['bundle'])
   checks={'bundle_bytes':c._bundle_bytes_admitted(bundle)==Path(references[name]['path']).read_bytes(),
           'snapshot':c.snapshot_id(bundle.current)==c._unwire(references[name]['state_id']),
           'append_head':bundle.events[-1].identity==c._unwire(references[name]['head']),
           'full_computation':semantic_view(bundle)==semantic_view(reference)}
   assert all(checks.values()),(name,checks);comparisons[name]=checks
  emit('reproduction-'+store_suffix+'.json',{'pid':os.getpid(),'seed':os.environ.get('PYTHONHASHSEED'),'positive_path':'PASS','boundaries':comparisons,'target':manifest})
  print('INDEPENDENT_REPRODUCTION_PASS',store_suffix,flush=True);return
 manifests={name:save(bundle,O/(name+'.json')) for name,bundle in stages.items()};emit('isolated-checkpoints.json',manifests)
 trace=[];previous=b
 for name,bundle in stages.items():trace.append(record_trace(previous,bundle,name));previous=bundle
 emit('isolated-execution-trace.json',trace)
 negatives=[]
 def reject(label,fn):
  try:fn()
  except (m.PlannerError,ValueError) as e:negatives.append({'case':label,'status':'PASS','reason':str(e)})
  else:raise AssertionError(label)
 for changes in [{'proof_type':m.TypedProofKind.ROOT_PROOF},{'proposition':'wrong'},{'target':m.SlotId('wrong')},{'authority':m.EntityId('old-PC02')},{'scope':'foreign'},{'lineage':'foreign'},{'generation':'foreign'},{'support_identities':(c._identity(b'bad','wrong'),)},{'validation':m.ValidationState.STALE}]:
  bad=replace(candidate(sc),**changes);bad=replace(bad,id=tp.identity(bad));reject('wrong slot proof '+str(changes),lambda bad=bad:c.record_result(slot_contract,m.TypedProofAdmission(bad,c.snapshot_id(slot_contract.current))))
 reject('slot proof without actual knowledge',lambda:core.apply_event(b.current,m.TypedProofAdmission(candidate(sc),c.snapshot_id(b.current))))
 reject('root proof without installed contract/satisfied slot',lambda:c.record_result(slot_contract,m.TypedProofAdmission(candidate(rc),c.snapshot_id(slot_contract.current))))
 reject('SLOT_PROOF substituted as ROOT_PROOF',lambda:c.record_result(root_contract,m.TypedProofAdmission(replace(candidate(sc),contract=rc.id),c.snapshot_id(root_contract.current))))
 for ref in (m.EntityId('P04-A13-INDEPENDENT-ROOT-SOURCE-1'),rc.authority):
  invalid=c.record_result(root_contract,m.ProofDependencyChange((ref,),c.snapshot_id(root_contract.current),rc.provenance))
  reject('root proof invalid source/semantic authority '+ref.value,lambda invalid=invalid:c.record_result(invalid,m.TypedProofAdmission(candidate(rc),c.snapshot_id(invalid.current))))
 for field,value in [('proposition','wrong'),('target',m.ConditionId('wrong')),('authority',m.EntityId('old-PC02'))]:
  bad=replace(candidate(rc),**{field:value});bad=replace(bad,id=tp.identity(bad));reject('wrong root '+field,lambda bad=bad:c.record_result(root_contract,m.TypedProofAdmission(bad,c.snapshot_id(root_contract.current))))
 reject('FINISH early',lambda:c.record_result(post,replace(supplied,expected_snapshot=c.snapshot_id(post.current))))
 for label,change in [('wrong outcome',{'result':m.ActionResult.FAIL}),('missing output',{'knowledge':()}),('extra output',{'knowledge':supplied.knowledge+(replace(supplied.knowledge[0],id=m.KnowledgeId('extra')),)}),('wrong Action',{'action':m.ActionId('E2-REENTER')})]:
  reject('FINISH '+label,lambda change=change:c.record_result(root,replace(supplied,**change)))
 invalidations=[]
 for ref in (m.KnowledgeId('E2-K-REENTER'),m.EntityId('P04-A13-INDEPENDENT-ROOT-SOURCE-1'),rc.authority):
  invalid=c.record_result(root,m.ProofDependencyChange((ref,),c.snapshot_id(root.current),rc.provenance));assert invalid.current.roots[0].state is m.ConditionState.UNRESOLVED and m.ActionId('E2-FINISH') not in core.recompute(invalid.current).actionable
  after=c.record_result(target,m.ProofDependencyChange((ref,),c.snapshot_id(target.current),rc.provenance));assert len(after.current.typed_proofs)==2 and any(e.result==supplied for e in after.events)
  assert not core.recompute(after.current).actionable;invalidations.append({'dependency':c._wire(ref),'pre_finish':'READINESS_WITHDRAWN','post_finish':'HISTORICAL_RESULT_RETAINED_NO_REEXECUTION'})
 # Already-qualified generic proofs cannot bypass terminal failure/status contracts.
 for state in (replace(root.current,statuses=tuple(replace(s,terminal_failure=True,state=m.ActionState.BLOCKED) if s.id==fin.id else s for s in root.current.statuses)),replace(root.current,actions=tuple(replace(a,blocked_terminal=True) if a.id==fin.id else a for a in root.current.actions),statuses=tuple(replace(s,state=m.ActionState.BLOCKED) if s.id==fin.id else s for s in root.current.statuses))):
  derived=tp.reevaluate(state,state,(rc.target,),rc.provenance);assert fin.id not in core.recompute(derived).actionable
  negatives.append({'case':'terminal FINISH not force reopened','status':'PASS'})
 emit('lifecycle-qualification.json',{'A09':'PASS_18_TERMS','A10':'PASS','A11':'PASS','A12':'PASS','A13':'PASS','old_candidate':stale,'Proof':proof.state.value,'C03':c._wire(core.resume_eligibility(eligible,R)),'F03_no_PLAN_DEFECT_clause':'OVERRIDDEN_BY_EXPLICIT_HUMAN_CLARIFICATION_RETAIN_SEALED_F02_ORACLE','pre_A13_control':'PLAN_DEFECT','slot_proof':c._wire(candidate(sc).id),'root_proof':c._wire(candidate(rc).id),'finish_execution':c._wire(supplied),'target':manifests['isolated-p04-target'],'negative_cases':negatives,'invalidations':invalidations,'canonical_lifecycle_executed':False,'p04_exit':True})
 print('A13_TARGET_PASS',len(negatives),flush=True)

def reader(manifest_path):
 man=c.parse_json(Path(manifest_path).read_bytes());root=Path(man.get('root',str(R)));b=c.restore(Path(man['path']),c._unwire(man['bundle_id']),root)
 assert c._wire(c.snapshot_id(b.current))==man['state_id'] and c._wire(b.events[-1].identity)==man['head']
 # restore() already performs full native replay and exact canonical-byte
 # comparison before it returns. Avoid a redundant second replay per reader.
 if man.get('before_count'):assert c._wire(c.bundle_id(c._prefix_bundle(b,man['before_count'])))==man['before_bundle_id']
 typ=lambda r:i.descriptor(r.request.definition)[0]['definition_type']
 assert all(i.current(b,r) for r in b.current.installed_definitions if typ(r) in pi.TYPES or typ(r)=='ACTION_DEFINITION')
 if man['boundary']=='isolated-p04-target':assert core.recompute(b.current).control is m.ControlState.TERMINAL_SUCCESS and len(b.current.typed_proofs)==2
 if man['boundary']=='generic-qualified':assert b.current.roots[0].state is m.ConditionState.SATISFIED and len(b.current.typed_proofs)==2
 semantic=semantic_view(b,root)
 if 'semantic_oracle' in man:assert semantic==man['semantic_oracle']
 control=core.recompute(b.current).control
 print(json.dumps({'pid':os.getpid(),'pid_namespace':os.readlink('/proc/self/ns/pid'),'seed':os.environ.get('PYTHONHASHSEED'),'bundle':man['bundle_id'],'state':man['state_id'],'head':man['head'],'currentness':'PASS','replay':'PASS','control':control.value if control is not None else None,'semantic':semantic}),flush=True)
if __name__=='__main__':
 if sys.argv[1]=='lifecycle':lifecycle(sys.argv[2] if len(sys.argv)>2 else '')
 elif sys.argv[1]=='reproduce':lifecycle('seed-'+sys.argv[2],True)
 else:{'generic':generic,'generic-checkpoint':generic_checkpoint,'repersist':repersist,'apply':apply}.get(sys.argv[1],lambda:reader(sys.argv[2]))()
