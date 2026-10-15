"""V02 native qualification using independent TEST inputs, no canonical P04 receipt."""
import copy,json,hashlib,unittest
from pathlib import Path
from dataclasses import replace,fields
from unittest.mock import patch
from adapter.planner import codec as c,model as m,installation as i,validation_installation as vi,validation_transaction as vt,evidence_transaction as tx,evidence_attestation as ea,core,gates
from adapter.tests import test_planner_authentication_installation as auth
from adapter.tests.test_planner_evidence_transaction import binding
from adapter.tests.test_planner_installation import request as install_request
ROOT=Path(__file__).resolve().parents[2];Q=ROOT/'docs/plans/qualification/VALIDATION_V01_1'

def pin(p):return {'path':p.path,'profile':'raw-file-sha256','pointer':'','identity':i.simple(p.identity)}
def provenance(path,body,scope):
 raw=c.canonical_bytes(body).decode();return m.Provenance(path,c._identity(raw.encode(),'raw-file-sha256'),'/',raw,'V02-SEALED-QUALIFICATION-INPUT',scope)
def descriptor(d,body,path,scope):
 p=provenance(path,body,scope);d=copy.deepcopy(d)
 d.update(content_id=i.simple(p.identity),canonical_source_reference={'kind':'IMMUTABLE_FILE','path':path,'content_id':i.simple(p.identity)},source_pin=pin(p),provenance={'path':path,'content_id':i.simple(p.identity),'section':'/','method':p.method,'scope':scope})
 return m.InstallableDefinition(i.digest(d,'planner-installable-definition-v1'),c.canonical_bytes(d).decode(),p)

def generic_set(snapshot,t,expected,actual):
 ctx=snapshot.context;g=snapshot.external_gates[0];req=snapshot.evidence_requirements[0]
 db=c.parse_json((Q/'p04-definition-set-descriptor.json').read_bytes());body=c.parse_json((Q/'p04-definition-set.json').read_bytes())
 role={'kind':'EVIDENCE_VALIDATION_SUPPORT_ROLE','gate':g.id.value,'requirements':[req.id.value],'consumer':'A10','dependent_action':g.reentry[0].value}
 db.update(scope=ctx.scope,lineage=ctx.lineage,generation=ctx.generation,subject=role)
 b=body['contract'];b.update(scope=ctx.scope,lineage=ctx.lineage,generation=ctx.generation,role=role)
 exp=provenance('expected-semantics.json',expected,ctx.scope)
 bp=provenance('binding-template.json',{'schema':'PLANNER-SEMANTIC-NATIVE-BINDING-TEMPLATE-1','template_only':True,'instance_boundary':'no lifecycle instance','binding':{k:c._wire(v) for k,v in vars(binding(t)).items()}},ctx.scope)
 protocol=provenance('validation-protocol.json',c.parse_json((Q/'generic-validation-support-protocol.json').read_bytes()),ctx.scope)
 b['protocol_pin']=pin(protocol)
 old={key:copy.deepcopy(x) for key,x in b['members'].items()};new={}
 for key in ('validation','support','transaction'):
  x=old[key];md=x['descriptor'];md.update(scope=ctx.scope,lineage=ctx.lineage,generation=ctx.generation,subject=dict(role,kind=vi.MEMBERS[key][1].replace('_CONTRACT','_MEMBER_ROLE')))
  v=x['body']
  if key in ('validation','support'):
   v.update(scope=ctx.scope,lineage=ctx.lineage,generation=ctx.generation)
   sr=v['source_requirements'];sr.update(expectation_source=pin(exp),binding_template_source=pin(bp),gate_definition_source=c._wire(g.provenance),requirement_definition_source=c._wire(req.provenance),producer_identities=[c._wire(z) for z in req.producers],target=c._wire(req.target),scope_lineage_generation={'scope':ctx.scope,'lineage':ctx.lineage,'generation':ctx.generation})
  if key=='validation':v.update(proposition=req.proposition,semantic_expectations=expected,validator_protocol_pin=pin(protocol),target_selector={'gate':g.id.value,'requirement':req.id.value,'require_unique_actual_admitted_entity':True,'native_binding_template':{k:c._wire(z) for k,z in vars(binding(t)).items()}})
  if key=='support':v.update(validation_contract=i.simple(new['validation'].id),predicate_id=next(p.id.value for p in snapshot.predicates if p.obligation==req.id),predicate='existing EVIDENCE_OBLIGATION '+req.id.value,target={'gate':g.id.value,'native_projection':'ReceiptObservation','requirements':[req.id.value]})
  if key=='transaction':v.update(validation_contract=i.simple(new['validation'].id),support_contract=i.simple(new['support'].id),protocol_pin=pin(protocol),scope_lineage_generation={'scope':ctx.scope,'lineage':ctx.lineage,'generation':ctx.generation})
  member=descriptor(md,{'schema':vi.MEMBERS[key][2],'contract':v},key+'-definition.json',ctx.scope);new[key]=member
  b['members'][key]={'body':v,'body_pin':pin(member.provenance),'definition_id':i.simple(member.id),'descriptor':c.parse_json(member.descriptor_json.encode())}
 definition=descriptor(db,body,'validation-set.json',ctx.scope)
 return definition,(protocol,exp,bp)


def fixture(outcome='PASS'):
 h=auth.AuthenticationInstallationTests();h.setUp()
 ctx=h.state.context;g=h.state.external_gates[0];req=h.state.evidence_requirements[0]
 actual={'schema':'TEST-SEMANTIC-PAYLOAD-1','qualification_only':True,'scope':ctx.scope,'lineage':ctx.lineage,'generation':ctx.generation,'currentness':{'valid_from':0,'valid_until':100},'gate_id':g.id.value,'proposition_id':req.id.value,'proposition':req.proposition,'source_id':i.simple(req.producers[0]),'subject':i.simple(req.target),'value':'RULE_PRESENT' if outcome=='PASS' else 'RULE_MISSING'}
 expected=dict(actual,value='RULE_PRESENT')
 ap=provenance('actual-semantics.json',actual,ctx.scope);(h.root/ap.path).write_text(ap.excerpt)
 h.bundle=replace(h.bundle,sources=h.bundle.sources+(m.ArtifactPin(ap.path,ap.identity),))
 h.r=auth.request(h.bundle,h.auth,h.decision,h.contract,'install-auth-receipt.json',h.binding)
 _,b,_,_=h.installed();x,t=h.candidate(b)
 args=dict(vars(t));args.pop('attestation_id');args.update(content=c._identity(c.canonical_bytes(actual),'test-semantic-content-v1'),semantic_evidence=c._identity(c.canonical_bytes({'payload':actual,'proposition':req.proposition,'consumer':g.reentry[0].value,'gate':g.id.value}),'test-semantic-evidence-v1'))
 t=ea.materialize(**args)
 defn,extras=generic_set(b.current,t,expected,actual)
 r,decision=install_request(b,defn,m.InstallationOperation.INSTALL,receipt_path='validation-install-authority.json')
 r=replace(r,definition_sources=extras)
 r=replace(r,source_additions=tuple(m.ArtifactPin(p.path,p.identity) for p in i.request_provenances(r) if m.ArtifactPin(p.path,p.identity) not in b.sources))
 r=replace(r,command_key=i.command_key(r))
 installed,bid,_=i.commit(b,r,h.root/'validation-install',h.root,expected_authority=r.authority.id,expected_decision=decision)
 x=replace(x,expected_bundle=c.bundle_id(installed),expected_snapshot=c.snapshot_id(installed.current),expected_parent_event=installed.events[-1].identity)
 x=tx.bind(x,t,binding(t));raw={x.entity.provenance.path:x.entity.provenance.excerpt.encode()}
 received,_,_=c.admit_external_evidence(installed,x,raw,h.root/'receipt-store',h.root,expected_binding=binding(t))
 cmd=vt.command(received,x.entity.id,installed.current.installed_definitions[-1].id)
 return h,b,r,installed,x,received,cmd

class ValidationSupportTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.positive=fixture();cls.negative=fixture('FAIL')
 @classmethod
 def tearDownClass(cls):
  cls.positive[0].doCleanups();cls.negative[0].doCleanups()
 def test_positive_rejected_and_frame(self):
  for data,outcome in ((self.positive,m.ValidationOutcome.PASS),(self.negative,m.ValidationOutcome.FAIL)):
   h,b,r,installed,x,received,cmd=data;a,trial=vt.prepare(received,cmd,h.root)
   self.assertIs(a.validation_result.outcome,outcome)
   self.assertEqual(trial.current.typed_proofs,received.current.typed_proofs)
   self.assertEqual(trial.current.statuses,received.current.statuses)
   self.assertEqual(trial.current.knowledge,received.current.knowledge)
   self.assertEqual(trial.current.roots,received.current.roots)
   self.assertEqual(trial.current.slots,received.current.slots)
   self.assertEqual(trial.current.external_gates[0].stage,m.ExternalStage.EVIDENCE_VALIDATED if outcome is m.ValidationOutcome.PASS else m.ExternalStage.WAITING_FOR_EXTERNAL_EVIDENCE)
   self.assertEqual(gates.external_complete(trial.current,trial.current.external_gates[0]),outcome is m.ValidationOutcome.PASS)
 def test_atomic_commit_replay_idempotence(self):
  h,b,r,installed,x,received,cmd=self.positive;a,trial=vt.prepare(received,cmd,h.root)
  end,bid,no=vt.commit(received,a,h.root/'validation-store',h.root);self.assertFalse(no);self.assertEqual(c.bundle_bytes(end),c.bundle_bytes(trial))
  with patch.object(vt,'assess',side_effect=AssertionError('new validation decision forbidden')):
   cold=c.restore(h.root/'validation-store'/('bundle-'+bid.sha256+'.json'),bid,h.root)
   self.assertEqual(c.bundle_bytes(cold),c.bundle_bytes(end))
   retry,rid,no=vt.commit(received,a,h.root/'validation-store',h.root);self.assertTrue(no);self.assertEqual(rid,bid)
  other,oid,_=vt.commit(received,a,h.root/'independent-validation',h.root);self.assertEqual(oid,bid)
  for stage in ('validated','staged'):
   def fail(s):
    if s==stage:raise OSError('injected')
   with self.assertRaises(OSError):vt.commit(received,a,h.root/('fail-'+stage),h.root,failure_hook=fail)
   self.assertFalse((h.root/('fail-'+stage)/'HEAD.json').exists())
 def test_command_security(self):
  h,b,r,installed,x,received,cmd=self.positive
  changes={'evidence':m.EntityId('OTHER'),'receipt_reference':vt.ZERO,'validation_contract':vt.ZERO,'support_contract':vt.ZERO,'transaction_contract':vt.ZERO,'definition_set':vt.ZERO,'scope':'OTHER','lineage':'OTHER','generation':'OTHER','expected_parent_event':vt.ZERO,'expected_snapshot':vt.ZERO,'expected_bundle':vt.ZERO,'provenance':replace(cmd.provenance,excerpt='tampered')}
  for field,value in changes.items():
   with self.subTest(field=field):
    bad=replace(cmd,**{field:value});bad=replace(bad,command_key=vt.key(bad))
    with self.assertRaises(m.PlannerError):vt.prepare(received,bad,h.root)
  with self.assertRaises(m.PlannerError):vt.prepare(installed,cmd,h.root)
  with self.assertRaises(m.PlannerError):vt.prepare(received,True,h.root)
 def test_no_prospective_instances_or_bypass(self):
  h,b,r,installed,x,received,cmd=self.positive
  self.assertFalse(installed.current.validation_results);self.assertFalse(installed.current.validation_support_records)
  with self.assertRaisesRegex(m.PlannerError,'VALIDATION_TRANSACTION_REQUIRED'):c.record_result(received,m.ExternalEvent(x.gate,m.ExternalStage.EVIDENCE_VALIDATED,c.snapshot_id(received.current)))
  a,trial=vt.prepare(received,cmd,h.root)
  for field,value in [('assessment',replace(a.assessment,outcome=m.ValidationOutcome.FAIL)),('validation_result',replace(a.validation_result,outcome=m.ValidationOutcome.FAIL)),('support',replace(a.support,outcome='ACCEPTED')),('post_state',vt.ZERO)]:
   bad=replace(a,**{field:value});bad=replace(bad,precommit_seal=vt.seal(bad))
   with self.assertRaises(m.PlannerError):vt.validate_prefix(received,bad)
  with self.assertRaises(m.PlannerError):c.record_result(received,a)
  e=replace(received.current.entities[-1],validated=True,validation=m.ValidationState.ACCEPTED)
  with self.assertRaises(m.PlannerError):core.recompute(replace(received.current,entities=received.current.entities[:-1]+(e,)))
 def test_install_frame_and_stale_candidate(self):
  h,b,r,installed,x,received,cmd=self.positive
  for f in fields(m.Snapshot):
   if f.name not in ('installed_definitions','validation_contracts','validation_support_contracts','validation_transaction_contracts'):self.assertEqual(getattr(b.current,f.name),getattr(installed.current,f.name),f.name)
  self.assertTrue(i.current(installed,installed.current.installed_definitions[-1]))
  self.assertEqual(c.bundle_bytes(c._prefix_bundle(installed,len(b.events))),c.bundle_bytes(b))
 def test_invalidation_retains_history(self):
  h,b,r,installed,x,received,cmd=self.positive;a,end=vt.prepare(received,cmd,h.root)
  for identity in (r.definition.provenance.identity,cmd.semantic_binding.provenance,cmd.semantic_binding.content_id):
   if identity.kind is not m.IdentityKind.CONTENT_IDENTITY:continue
   stale=c.record_result(end,m.SourceInvalidation((identity,),c.snapshot_id(end.current)))
   self.assertEqual(stale.current.validation_results,end.current.validation_results)
   self.assertFalse(gates.external_complete(stale.current,stale.current.external_gates[0]))
 def test_installation_negatives_are_atomic(self):
  h,b,r,installed,x,received,cmd=self.positive
  cases=[replace(r,authority=replace(r.authority,authority_class=m.AuthorityClass.ATTEST)),replace(r,operation=m.InstallationOperation.REPLACE),replace(r,definition_sources=r.definition_sources[:-1]),replace(r,definition_sources=r.definition_sources+(r.definition_sources[0],)),replace(r,expected_parent_event=vt.ZERO),replace(r,expected_snapshot=vt.ZERO)]
  for bad in cases:
   bad=replace(bad,command_key=i.command_key(bad))
   with self.assertRaises(m.PlannerError):i.commit(b,bad,h.root/'install-negative',h.root,expected_authority=r.authority.id,expected_decision=i.identity(c.parse_json(r.authority.grant_json.encode())['decision_id']))
   self.assertFalse((h.root/'install-negative/HEAD.json').exists())
  d=c.parse_json(r.definition.descriptor_json.encode());body=c.parse_json(r.definition.provenance.excerpt.encode())
  for name in ('validation','support','transaction'):
   wrong=copy.deepcopy(body);wrong['contract']['members'][name]['body']['ValidationResult']=True
   with self.assertRaises(m.PlannerError):vi.descriptor(descriptor(d,wrong,'wrong-'+name+'.json',d['scope']))
 def test_assessment_and_support_substitution(self):
  h,b,r,installed,x,received,cmd=self.positive;a,_=vt.prepare(received,cmd,h.root)
  for field,value in [('validation_contract',vt.ZERO),('outcome',m.ValidationOutcome.FAIL),('scope','OTHER'),('provenance',replace(a.assessment.provenance,excerpt='wrong'))]:
   wrong=vt.identified(replace(a.assessment,**{field:value}),'planner-validation-assessment-v1')
   with self.assertRaises(m.PlannerError):vt.build(received,cmd,wrong)
  with self.assertRaises(m.PlannerError):vt.build(received,cmd,True)
  forged=replace(a.support,validation_result_id=vt.ZERO);forged=vt.identified(forged,'planner-validation-support-record-v1')
  with self.assertRaises(m.PlannerError):core.recompute(replace(received.current,validation_support_records=(forged,)))
 def test_binding_substitutions_and_closed_operands(self):
  h,b,r,installed,x,received,cmd=self.positive
  for field in vars(cmd.semantic_binding):
   value=getattr(cmd.semantic_binding,field)
   wrong=vt.ZERO if type(value) is m.ArtifactIdentity else type(value)('OTHER') if type(value) in (m.EntityId,m.PredicateId,m.GateId) else 'OTHER'
   bad=replace(cmd,semantic_binding=replace(cmd.semantic_binding,**{field:wrong}));bad=replace(bad,command_key=vt.key(bad))
   with self.subTest(field=field):
    with self.assertRaises(m.PlannerError):vt.prepare(received,bad,h.root)
  a,_=vt.prepare(received,cmd,h.root)
  wire=c._wire(a)
  for field in ('ValidationResult','support_instance','validated','proof'):
   wrong=copy.deepcopy(wire);wrong[field]=True
   with self.assertRaises(m.PlannerError):c._unwire(wrong)
 def test_definition_set_publish_failure_has_no_head(self):
  h,b,r,installed,x,received,cmd=self.positive
  real=c.os.replace
  def fail(src,dst):
   if str(dst).endswith('/HEAD.json'):raise OSError('injected set publication failure')
   return real(src,dst)
  with patch.object(c.os,'replace',side_effect=fail):
   with self.assertRaises(OSError):i.commit(b,r,h.root/'set-publish-failure',h.root,expected_authority=r.authority.id,expected_decision=i.identity(c.parse_json(r.authority.grant_json.encode())['decision_id']))
  self.assertEqual(c.bundle_id(c._read_head(h.root/'set-publish-failure',b,h.root)),c.bundle_id(b))
 def test_conflicting_command_and_expired_contract(self):
  h,b,r,installed,x,received,cmd=self.positive;a,_=vt.prepare(received,cmd,h.root)
  end,bid,_=vt.commit(received,a,h.root/'conflict-store',h.root)
  wrong=replace(a,assessment=vt.identified(replace(a.assessment,outcome=m.ValidationOutcome.FAIL),'planner-validation-assessment-v1'))
  wrong=replace(wrong,precommit_seal=vt.seal(wrong))
  with self.assertRaisesRegex(m.PlannerError,'IDEMPOTENCY_CONFLICT'):vt.commit(received,wrong,h.root/'conflict-store',h.root)
  self.assertEqual(c.bundle_id(c._read_head(h.root/'conflict-store',received,h.root)),bid)
  expired=replace(installed.current,context=replace(installed.current.context,tick=101))
  self.assertFalse(i.current(replace(installed,current=expired),installed.current.installed_definitions[-1]))
