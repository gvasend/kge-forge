"""Generic TEST fixtures for governed source and deferred proof configuration."""
import json, tempfile, unittest, os
from pathlib import Path
from dataclasses import replace
from unittest.mock import patch
from adapter.planner import model as m, codec as c, core, gates
from adapter.planner import installation as i, proof_installation as pi, typed_proofs as t
from adapter.tests.test_planner_installation import request as install_request
from adapter.tests.test_planner_typed_proofs import candidate

Z=c._identity(b'', 'unused-identity')
def simple(x):return i.simple(x)
def source(root,path,value,scope):
 raw=c.canonical_bytes(value);(root/path).parent.mkdir(parents=True,exist_ok=True);(root/path).write_bytes(raw)
 return m.Provenance(path,c._identity(raw,'raw-file-sha256'),'/',raw.decode(),'TEST_AUTHORED_DEFINITION',scope)
def pin(p):return {'path':p.path,'content_id':simple(p.identity)}
def load_definition(root,item):
 d=c.parse_json((root/item['path']).read_bytes());p=d['provenance'];raw=(root/p['path']).read_text()
 prov=m.Provenance(p['path'],i.identity(p['content_id']),'/',raw,p['method'],p['scope'])
 return m.InstallableDefinition(i.digest(d,'planner-installable-definition-v1'),c.canonical_bytes(d).decode(),prov)
def with_sources(root,bundle,defn,request,bindings=()):
 _,body=i.descriptor(defn)
 sources=[]
 for x in pi.nested_pins(body):
  raw=(root/x['path']).read_text();sources.append(m.Provenance(x['path'],i.identity(x['content_id']),'/',raw,'SEALED_NESTED_DEFINITION',bundle.current.context.scope))
 r=replace(request,definition_sources=tuple(sources),authority_bindings=bindings)
 ps=i.request_provenances(r);additions=tuple(dict.fromkeys(m.ArtifactPin(p.path,p.identity) for p in ps if m.ArtifactPin(p.path,p.identity) not in bundle.sources))
 r=replace(r,source_additions=additions);return replace(r,command_key=i.command_key(r))
def bounded_request(root,b,defn,bindings=(),receipt='install.json'):
 # request() supplies qualified existing generic INSTALL admission semantics.
 r,decision=install_request(b,defn,m.InstallationOperation.INSTALL,receipt_path=receipt)
 return with_sources(root,b,defn,r,bindings),decision

def descriptor(root,typ,subject,body,ctx):
 p=source(root,typ.lower()+'-body.json',body,ctx.scope)
 d={'schema':'PLANNER-INSTALLABLE-DEFINITION-1','definition_type':typ,'canonical_body_schema':body['schema'],'content_id':simple(p.identity),'subject':subject,'scope':ctx.scope,'lineage':ctx.lineage,'generation':ctx.generation,'canonical_source_reference':{'kind':'IMMUTABLE_FILE','path':p.path,'content_id':simple(p.identity)},'source_pin':{'path':p.path,'profile':'raw-file-sha256','pointer':'','identity':simple(p.identity)},'provenance':{'path':p.path,'content_id':simple(p.identity),'section':'/','method':p.method,'scope':p.scope},'currentness_rule':{'schema':'PLANNER-DEFINITION-CURRENTNESS-1','rule_id':'ROOT_SLOT_CONFIGURATION_CURRENT_V1' if typ=='ROOT_SLOT_CONFIGURATION_SET' else 'TYPED_PROOF_CONTRACT_CURRENT_V1','consumer':body['consumer'],'installation_required':True,'authority_current_required':True,'source_current_required':True,'exact_scope_lineage_generation_required':True}}
 if typ=='ROOT_PROOF_CONTRACT_DEFINITION':d['currentness_rule']['independent_root_source_required']=True
 return m.InstallableDefinition(i.digest(d,'planner-installable-definition-v1'),c.canonical_bytes(d).decode(),p)

def fixture(root):
 ctx=m.EvaluationContext('TEST_ONLY','independent-test-lineage','test-generation',0,())
 binding=dict(scope=ctx.scope,lineage=ctx.lineage,generation=ctx.generation,consumer='test-proof-consumer',valid_until=100,qualification_only=True)
 p=source(root,'result.json',{'independent':'result declaration'},ctx.scope)
 k=m.KnowledgeRecord(m.KnowledgeId('test-knowledge'),m.KnowledgeState.KNOWN_COMPLETE,'Actual generic permitted output',p,producer=m.ActionId('test-producer'),outcome=m.ActionResult.PASS)
 rp=source(root,'dependent.json',{'definition':'dependent'},ctx.scope)
 output=m.KnowledgeRecord(m.KnowledgeId('test-final'),m.KnowledgeState.KNOWN_COMPLETE,'Final generic permitted output',rp,producer=m.ActionId('test-dependent'),outcome=m.ActionResult.PASS)
 a=m.Action(k.producer,m.OperationClass.DETERMINISTIC_MAPPING,m.EffectClass.NON_EFFECTING,(),p,(k,),pass_model_complete=True)
 rootcondition=m.RootCondition(m.ConditionId('test-root'),m.ConditionState.UNRESOLVED)
 slot=m.ValueSlot(m.SlotId('test-slot'),m.SlotState.UNRESOLVED,m.ValueType.NON_IDENTITY_VALUE)
 finish=m.Action(output.producer,m.OperationClass.DETERMINISTIC_VALIDATION,m.EffectClass.NON_EFFECTING,(m.Gate(m.GateKind.CONDITION_SATISFIED,rootcondition.id),),rp,(output,),pass_model_complete=True,blocked_terminal=False)
 other=replace(a,id=m.ActionId('unrelated'),accepted_inventory=(),pass_model_complete=False)
 s=m.Snapshot((a,finish,other),(m.ActionStatus(a.id,m.ActionState.ACTION_ELIGIBLE),m.ActionStatus(finish.id,m.ActionState.BLOCKED),m.ActionStatus(other.id,m.ActionState.BLOCKED)),(rootcondition,),(),(),context=ctx)
 policy_path='docs/experiments/E1/E1_GRAPH_RESOLUTION_SELECTION_POLICY_1.md'
 policy_raw=Path(policy_path).read_bytes();(root/policy_path).parent.mkdir(parents=True,exist_ok=True);(root/policy_path).write_bytes(policy_raw)
 pp=m.Provenance(policy_path,c._identity(policy_raw,'raw-file-sha256'),'/',policy_raw.decode(),'READ_ONLY_POLICY',ctx.scope)
 b=m.PersistenceBundle(s,(),s,tuple(m.ArtifactPin(x.path,x.identity) for x in (p,rp)),m.ArtifactPin(pp.path,pp.identity),'E1-SELECTION-1-P06')
 b=c.record_result(b,m.ActionReevaluation((a.id,),c.snapshot_id(s),p))
 sources=[];entities=[];policies=[];specs=[]
 for label,target,proposition in [('SLOT_PROOF',slot.id,'knowledge establishes slot'),('ROOT_PROOF',rootcondition.id,'independently established root')]:
  ss={'schema':'PLANNER-QUALIFICATION-PROPOSITION-SOURCE-1',**binding,'id':'source-'+label,'role':label,'target':target.value,'proposition':{'id':proposition},'provenance_origin':{'origin':label},'asserts_execution':False,'asserts_satisfaction':False,'support_selector':{'knowledge':k.id.value,'producer':a.id.value,'expected_output_contract':c._wire(k)} if label=='SLOT_PROOF' else {'slot':slot.id.value,'native_state':'RESOLVED','proof_kind':'SLOT_PROOF','proposition':'knowledge establishes slot'}}
  sp=source(root,label+'-source.json',ss,ctx.scope);sources.append(pin(sp))
  native=c._wire(m.GraphEntity(m.EntityId(ss['id']),m.EntityKind.SOURCE,sp.identity,sp,ctx.scope,ctx.lineage,ctx.generation,100))
  for field in ('permissions','target','consumed','validator'):native.pop(field)
  entities.append(native)
  pol={'schema':'PLANNER-BOUNDED-QUALIFICATION-FIXTURE-POLICY-1',**binding,'native_permission':'DECIDE','subject':target.value,'source_content_id':simple(sp.identity),'native_authority_target':simple(sp.identity),'no_delegation':True}
  polp=source(root,label+'-semantic-policy.json',pol,ctx.scope);policies.append(pin(polp))
  specs.append({'entity_id':c._wire(m.EntityId('semantic-'+label)),'identity':c._wire(polp.identity),'permissions':['DECIDE'],'target':simple(sp.identity),'provenance':c._wire(polp),'binding':binding})
 sc=m.TypedProofContract(Z,m.TypedProofKind.SLOT_PROOF,'knowledge establishes slot',slot.id,(k.id,),(c._identity(c.canonical_bytes(c._wire(k)),'planner-proof-support-v1'),),ctx.scope,ctx.lineage,ctx.generation,100,c._unwire(specs[0]['entity_id']),c._unwire(specs[0]['identity']),c._unwire(entities[0]['provenance']));sc=replace(sc,id=t.identity(sc))
 wire=c._wire(sc);wire.pop('id');wire.pop('validation',None);wire['$type']='TypedProof';wire['contract']=c._wire(sc.id)
 pid=c._identity(c.canonical_bytes(wire),'planner-TypedProof-v1')
 rc=replace(sc,id=Z,proof_type=m.TypedProofKind.ROOT_PROOF,proposition='independently established root',target=rootcondition.id,supports=(slot.id,),support_identities=(c._identity(c.canonical_bytes(c._wire((pid,))),'planner-proof-support-v1'),),authority=c._unwire(specs[1]['entity_id']),authority_identity=c._unwire(specs[1]['identity']),provenance=c._unwire(entities[1]['provenance']));rc=replace(rc,id=t.identity(rc))
 slotp=source(root,'slot.json',{'contract':c._wire(slot),'proposition':sc.proposition},ctx.scope)
 rootp=source(root,'root.json',{'contract':c._wire(rootcondition),'proposition':rc.proposition,'independent_source_required':True,'required_slot':slot.id.value},ctx.scope)
 declarations=[];definitions=[]
 for contract,pin_source,pol in zip((sc,rc),sources,policies):
  body={'schema':'PLANNER-TYPED-PROOF-CONTRACT-DEFINITION-1',**binding,'contract':c._wire(contract),'source':pin_source,'semantic_policy':pol}
  df=descriptor(root,contract.proof_type.value+'_CONTRACT_DEFINITION',{'kind':'TYPED_PROOF_CONTRACT_ROLE','proof_type':contract.proof_type.value,'target':contract.target.value,'consumer':binding['consumer']},body,ctx);definitions.append(df);declarations.append(pin(df.provenance))
 config={'schema':'PLANNER-ROOT-SLOT-CONFIGURATION-SET-1',**binding,'sources':sources,'source_entity_definitions':entities,'slot':pin(slotp),'existing_root_to_bind':pin(rootp),'semantic_policies':policies,'semantic_authority_specs':specs,'concrete_proof_declarations':declarations,'no_concrete_contract_installed_yet':True,'no_proof_instances':True}
 df=descriptor(root,'ROOT_SLOT_CONFIGURATION_SET',{'kind':'ROOT_SLOT_CONFIGURATION_ROLE','root':rootcondition.id.value,'slot':slot.id.value,'consumer':binding['consumer']},config,ctx)
 decision=i.digest({'trusted':'TEST explicit semantic decision'},'test-decision-v1');semid=i.digest({'exact':'TEST semantic subject'},'test-subject-v1')
 grant={'schema':'PLANNER-FIXTURE-SEMANTIC-GRANT-1','issuer':'QUALIFICATION_AUTHORITY','authority_class':'DECIDE','decision_id':simple(decision),'semantic_request_id':simple(semid),'configuration_definition_id':simple(df.id),'scope':ctx.scope,'lineage':ctx.lineage,'generation':ctx.generation,'consumer':binding['consumer'],'valid_from':0,'valid_until':100,'delegation':False,'automatic_issuance_by_install':False,'sources':sources,'policies':policies,'authority_specs':specs}
 gid=i.digest(grant,'planner-fixture-semantic-authorization-v1',m.IdentityKind.AUTHORITY_IDENTITY)
 auth=pi.admit_semantic_authority(grant,expected_grant=gid,expected_decision=decision,trusted_issuer='QUALIFICATION_AUTHORITY',receipt_path='semantic-admission.json')
 r,install_dec=bounded_request(root,b,df,(auth,))
 return b,r,install_dec,definitions,sc,rc

class ProofInstallationTests(unittest.TestCase):
 def setUp(self):
  tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup);self.root=Path(tmp.name)
  self.b,self.r,self.dec,self.defs,self.sc,self.rc=fixture(self.root);self.store=self.root/'store'
 def commit(self,b=None,r=None,store=None):
  b=b or self.b;r=r or self.r
  return i.commit(b,r,store or self.store,self.root,expected_authority=r.authority.id,expected_decision=self.dec,expected_operating_authority=self.r.authority_bindings[0].operating_authorization_id)
 def configured(self):return self.commit()[0]
 def lifecycle(self):
  b=self.configured();a=next(a for a in b.current.actions if a.id.value=='test-producer')
  before=c.record_result(b,m.SuppliedResult(a.id,m.ActionResult.PASS,a.accepted_inventory,c.snapshot_id(b.current)))
  sr,_=bounded_request(self.root,before,self.defs[0],receipt='slot-install.json');slot_contract=self.commit(before,sr,store=self.root/'slot-store')[0]
  slot=c.record_result(slot_contract,m.TypedProofAdmission(candidate(self.sc),c.snapshot_id(slot_contract.current)))
  rr,_=bounded_request(self.root,slot,self.defs[1],receipt='root-install.json');root_contract=self.commit(slot,rr,store=self.root/'root-store')[0]
  target=c.record_result(root_contract,m.TypedProofAdmission(candidate(self.rc),c.snapshot_id(root_contract.current)))
  return before,slot_contract,slot,root_contract,target
 def test_positive_deferred_support_and_independence(self):
  before,sc,slot,rc,target=self.lifecycle()
  self.assertFalse(before.current.typed_proofs);self.assertFalse(before.current.proof_contracts)
  self.assertTrue(i.current(target,target.current.installed_definitions[0]))
  self.assertEqual(slot.current.slots[0].state,m.SlotState.RESOLVED);self.assertEqual(slot.current.roots[0].state,m.ConditionState.UNRESOLVED)
  self.assertNotIn(m.ActionId('test-dependent'),core.recompute(slot.current).actionable)
  self.assertIn(m.ActionId('test-dependent'),core.recompute(target.current).actionable)
  self.assertEqual(next(s for s in target.current.statuses if s.id.value=='unrelated').state,m.ActionState.BLOCKED)
 def test_premature_contracts_and_no_lifecycle_installation(self):
  b=self.configured();self.assertFalse(b.current.typed_proofs);self.assertFalse(b.current.proof_contracts);self.assertFalse(b.current.knowledge)
  for index in (0,1):
   r,_=bounded_request(self.root,b,self.defs[index],receipt='premature-'+str(index)+'.json')
   with self.assertRaises(m.PlannerError):self.commit(b,r,store=self.root/('bad'+str(index)))
  self.assertEqual(b.current.statuses,self.b.current.statuses)
 def test_identity_authority_context_negatives(self):
  cases={'wrong authority':replace(self.r,authority=replace(self.r.authority,authority_class=m.AuthorityClass.ATTEST)), 'missing semantic':replace(self.r,authority_bindings=()), 'wrong semantic class':replace(self.r,authority_bindings=(replace(self.r.authority_bindings[0],authority_class=m.AuthorityClass.INSTALL),)), 'wrapper':replace(self.r,definition=replace(self.r.definition,provenance=replace(self.r.definition.provenance,excerpt='{}'))),'wrong source':replace(self.r,definition_sources=self.r.definition_sources[1:]), 'wrong parent':replace(self.r,expected_parent_event=Z),'wrong prestate':replace(self.r,expected_snapshot=Z),'wrong generation':replace(self.r,definition=replace(self.r.definition,descriptor_json=self.r.definition.descriptor_json.replace('test-generation','foreign-generation')))}
  for name,r in cases.items():
   with self.subTest(name=name):
    with self.assertRaises(m.PlannerError):self.commit(r=r,store=self.root/name)
    self.assertFalse((self.root/name/'HEAD.json').exists())
  auth=self.r.authority_bindings[0];grant=json.loads(auth.issued_authorization_json)
  for issuer in ('SYSTEM_OPERATOR','ATTEST'):
   with self.assertRaises(m.PlannerError):pi.admit_semantic_authority(grant,expected_grant=auth.operating_authorization_id,expected_decision=i.identity(grant['decision_id']),trusted_issuer=issuer,receipt_path='bad.json')
 def test_atomic_failure_retry_and_restore(self):
  real=os.replace
  def fail(src,dst):
   if str(dst).endswith('/HEAD.json'):raise OSError('injected')
   return real(src,dst)
  with patch('adapter.planner.codec.os.replace',side_effect=fail):
   with self.assertRaises(OSError):self.commit()
  self.assertFalse((self.store/'HEAD.json').exists())
  after,bid,_=self.commit();retry,ident,noop=self.commit();self.assertTrue(noop);self.assertEqual(ident,bid);self.assertEqual(c.bundle_bytes(after),c.bundle_bytes(retry))
  restored=c.restore(self.store/('bundle-'+bid.sha256+'.json'),bid,self.root);self.assertEqual(c.bundle_bytes(restored),c.bundle_bytes(after))
  self.assertEqual(c.snapshot_id(c._replay(restored)),c.snapshot_id(after.current));self.assertFalse(restored.current.typed_proofs)
 def test_source_entity_and_policy_invalidation(self):
  *_,target=self.lifecycle()
  for dep in (m.EntityId('source-ROOT_PROOF'),self.rc.authority,self.sc.supports[0]):
   changed=c.record_result(target,m.ProofDependencyChange((dep,),c.snapshot_id(target.current),self.rc.provenance))
   self.assertEqual(changed.current.roots[0].state,m.ConditionState.UNRESOLVED);self.assertNotIn(m.ActionId('test-dependent'),core.recompute(changed.current).actionable)
   self.assertEqual(len(changed.current.typed_proofs),2)
  changed=c.record_result(target,m.SourceInvalidation((self.rc.provenance.identity,),c.snapshot_id(target.current)))
  self.assertNotIn(m.ActionId('test-dependent'),core.recompute(changed.current).actionable)
 def test_owned_contract_cannot_fall_back_to_legacy(self):
  _,_,_,before,_=self.lifecycle()
  for changes in ({'proposition':'generic TRUE'},{'provenance':self.sc.provenance},{'generation':'old-generation'},{'authority':self.sc.authority}):
   wrong=replace(self.rc,**changes);wrong=replace(wrong,id=t.identity(wrong))
   state=replace(before.current,proof_contracts=tuple(wrong if x.target==wrong.target else x for x in before.current.proof_contracts))
   self.assertFalse(pi.contract_current(state,wrong))
   with self.assertRaises(m.PlannerError):core.apply_event(state,m.TypedProofAdmission(candidate(wrong),c.snapshot_id(state)))
  # Source records with another origin/body cannot retain live usability.
  for change in ({'identity':self.sc.provenance.identity},{'provenance':self.sc.provenance},{'scope':'foreign'},{'generation':'foreign'}):
   state=replace(before.current,entities=tuple(replace(x,**change) if x.id.value=='source-ROOT_PROOF' else x for x in before.current.entities))
   self.assertFalse(pi.contract_current(state,self.rc))
if __name__=='__main__':unittest.main()
