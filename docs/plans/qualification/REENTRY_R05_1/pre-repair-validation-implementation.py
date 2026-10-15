"""Atomic, parent-bound validation/support; replay consumes historical decisions.

Live assessment is distinct from deterministic record projection. A prepared
commit is private until the existing single-writer HEAD publication succeeds.
"""
from dataclasses import replace,fields
from . import model as m
from .validation_installation import TYPE

ZERO=m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY,'placeholder','0'*64)

def env():
 from . import codec as c,installation as i
 return c,i

def identified(value,namespace):
 c,i=env();w=c._wire(value);w.pop('id');return replace(value,id=i.digest(w,namespace))

def key(command):
 c,i=env();w=c._wire(command);w.pop('command_key');return i.digest(w,'planner-validation-support-command-v1')

def registered(snapshot,gate):
 c,i=env()
 return any(i.descriptor(x.request.definition)[0]['definition_type']==TYPE and i.descriptor(x.request.definition)[0]['subject']['gate']==gate.value for x in snapshot.installed_definitions)

def definitions(snapshot,set_id):
 c,i=env();from . import validation_installation as vi
 record=next((x for x in snapshot.installed_definitions if x.id==set_id),None)
 i.require(record is not None and i.descriptor(record.request.definition)[0]['definition_type']==TYPE and vi.support_current(snapshot,record),'VALIDATION_CONTRACT_NOT_CURRENT')
 d,(body,native)=vi.descriptor(record.request.definition)
 return record,d,body,native

def receipt(bundle,evidence):
 c,i=env();s=bundle.current
 records=[a for a in s.receipt_admissions if a.artifact==evidence]
 ingress=[e for e in bundle.events if type(e.result) is m.EvidenceSourceAdmission and e.result.entity.id==evidence]
 i.require(len(records)==len(ingress)==1,'VALIDATION_REQUIRES_RECEIPT')
 event=ingress[0];index=event.sequence
 i.require(index<len(bundle.events),'VALIDATION_RECEIVED_EVENT_MISSING')
 received=bundle.events[index]
 i.require(type(received.result) is m.ExternalEvent and received.result.stage is m.ExternalStage.EVIDENCE_RECEIVED and received.result.artifact==evidence and received.parent_event==event.identity,'VALIDATION_RECEIPT_ANCESTRY')
 a=records[0];x=event.result
 i.require(x.attestation_operand is not None and a.attestation==x.attestation_operand.attestation.attestation_id,'VALIDATION_AUTHENTICATION_WITNESS')
 from . import evidence_transaction as tx
 contract=next(z for z in s.ingress_contracts if z.gate==x.gate)
 tx.validate(s,x,contract)
 identity=i.digest({'admission':c._wire(a),'ingress_event':c._wire(event.identity),'received_event':c._wire(received.identity)},'planner-receipt-admission-reference-v1')
 return a,x,identity,(event.identity,received.identity)

def command(bundle,evidence,set_id):
 c,i=env();r,d,b,n=definitions(bundle.current,set_id);a,x,ref,_=receipt(bundle,evidence);ctx=bundle.current.context
 z=m.ValidationSupportCommand('VALIDATE_EVIDENCE_SUPPORT',1,ZERO,c.bundle_id(bundle),c.snapshot_id(bundle.current),bundle.events[-1].identity,len(bundle.events)+1,bundle.policy,bundle.policy_version,set_id,n['validation'].id,n['support'].id,n['transaction'].id,evidence,ref,x.attestation_operand.binding,ctx.scope,ctx.lineage,ctx.generation,n['validation'].provenance)
 return replace(z,command_key=key(z))

def inputs(bundle,cmd):
 c,i=env();m.validate_types(cmd,m.ValidationSupportCommand);s=bundle.current
 i.require(cmd.event_type=='VALIDATE_EVIDENCE_SUPPORT' and cmd.schema_version==1 and cmd.command_key==key(cmd),'VALIDATION_COMMAND')
 i.require((cmd.expected_bundle,cmd.expected_snapshot,cmd.expected_parent_event,cmd.sequence)==(c._identity(c._bundle_bytes_admitted(bundle),'planner-bundle-v1'),c.snapshot_id(s),bundle.events[-1].identity,len(bundle.events)+1),'VALIDATION_PREFIX_MISMATCH')
 i.require((cmd.policy,cmd.policy_version)==(bundle.policy,bundle.policy_version),'VALIDATION_POLICY')
 record,d,b,n=definitions(s,cmd.definition_set);ctx=s.context
 i.require((cmd.scope,cmd.lineage,cmd.generation)==(ctx.scope,ctx.lineage,ctx.generation),'VALIDATION_CONTEXT')
 i.require((cmd.validation_contract,cmd.support_contract,cmd.transaction_contract)==tuple(n[k].id for k in ('validation','support','transaction')) and cmd.provenance==n['validation'].provenance,'VALIDATION_MEMBER_REFERENCE')
 a,x,ref,history=receipt(bundle,cmd.evidence)
 i.require(ref==cmd.receipt_reference and cmd.semantic_binding==x.attestation_operand.binding,'VALIDATION_RECEIPT_BINDING')
 entity=next((e for e in s.entities if e.id==cmd.evidence),None);gate=next((g for g in s.external_gates if g.id==x.gate),None)
 i.require(entity is not None and entity.kind is m.EntityKind.EVIDENCE and entity.produced and entity.validation is m.ValidationState.NOT_EVALUATED and not entity.validated and gate.stage is m.ExternalStage.EVIDENCE_RECEIVED and gate.pending==entity.id,'VALIDATION_STAGE')
 i.require((entity.scope,entity.lineage,entity.generation)==(ctx.scope,ctx.lineage,ctx.generation) and ctx.tick<=entity.valid_until,'VALIDATION_EVIDENCE_NOT_CURRENT')
 v=c.parse_json(n['validation'].body_json.encode())['contract'];sources={p.path:p for p in record.request.definition_sources}
 template=c.parse_json(sources[v['source_requirements']['binding_template_source']['path']].excerpt.encode())
 binding=m.SemanticNativeBinding(**{k:c._unwire(z) for k,z in template['binding'].items()})
 i.require(binding==cmd.semantic_binding,'VALIDATION_TEMPLATE_BINDING')
 for pin in i.request_provenances(record.request):i.require(m.ArtifactPin(pin.path,pin.identity) in bundle.sources,'VALIDATION_SOURCE_NOT_PINNED')
 invalidated={p for e in bundle.events if type(e.result) is m.SourceInvalidation for p in e.result.changed}
 ids=tuple(sorted({cmd.expected_snapshot,cmd.expected_parent_event,cmd.receipt_reference,entity.identity,a.provenance.identity,cmd.semantic_binding.content_id,cmd.semantic_binding.semantic_evidence_id,*(p.identity for p in i.request_provenances(record.request)),*history},key=lambda z:(z.kind.value,z.namespace,z.sha256)))
 i.require(not invalidated.intersection(ids),'VALIDATION_SOURCE_INVALIDATED')
 return record,d,b,n,a,x,entity,gate,v,ids

def semantic_shape(payload,expected):
 c,i=env()
 i.require(type(payload) is dict and set(payload)==set(expected)==set('schema qualification_only scope lineage generation currentness gate_id proposition_id proposition source_id subject value'.split()),'VALIDATION_SEMANTIC_SCHEMA')
 i.require(type(payload['qualification_only']) is bool and all(type(payload[k]) is str for k in ('schema','scope','lineage','generation','gate_id','proposition_id','proposition','value')) and set(payload['currentness'])=={'valid_from','valid_until'} and all(type(z) is int for z in payload['currentness'].values()),'VALIDATION_SEMANTIC_TYPES')
 for k in ('source_id','subject'):i.identity(payload[k])
 i.require(payload['schema']==expected['schema'] and payload['currentness']['valid_from']<=payload['currentness']['valid_until'],'VALIDATION_SEMANTIC_SCHEMA')

def assess(bundle,cmd,repo_root):
 """Only live validation runs this registered semantic rule; never replay."""
 c,i=env();record,d,b,n,a,x,e,g,v,ids=inputs(bundle,cmd)
 pin=v['source_requirements']['expectation_source']
 # Actual input comes from the historical ingress payload, not expectation bytes.
 payload_pins=[p for p in bundle.sources if p.profile is m.HashProfile.RAW and p.identity.sha256==cmd.semantic_binding.content_id.sha256]
 i.require(bool(payload_pins),'VALIDATION_SEMANTIC_SOURCE_MISSING')
 raw_inputs=[c.load_pinned(repo_root,p) for p in sorted(payload_pins,key=lambda p:p.path)]
 i.require(all(raw==raw_inputs[0] for raw in raw_inputs),'VALIDATION_SEMANTIC_SOURCE_CONFLICT')
 payload=c.parse_json(raw_inputs[0])
 expected=v['semantic_expectations']
 semantic_shape(payload,expected)
 # E01 domains are the independently installed mapping, including exact content.
 binding=cmd.semantic_binding
 i.require(c._identity(c.canonical_bytes(payload),binding.content_id.namespace)==binding.content_id,'VALIDATION_CONTENT_BINDING')
 clauses=tuple(m.ValidationClause(k,c.canonical_bytes(expected[k]).decode(),c.canonical_bytes(payload[k]).decode(),() if payload[k]==expected[k] else ('SEMANTIC_MISMATCH:'+k,)) for k in sorted(expected))
 outcome=m.ValidationOutcome.PASS if all(not x.reasons for x in clauses) else m.ValidationOutcome.FAIL
 z=m.ValidationAssessment(ZERO,cmd.command_key,ids,cmd.validation_contract,v['validator_rule'],clauses,outcome,cmd.scope,cmd.lineage,cmd.generation,cmd.provenance)
 return identified(z,'planner-validation-assessment-v1')

def verify_assessment(cmd,assessment,v,ids):
 c,i=env();m.validate_types(assessment,m.ValidationAssessment)
 i.require(assessment==identified(assessment,'planner-validation-assessment-v1') and (assessment.command_key,assessment.input_identities,assessment.validation_contract,assessment.rule_id,assessment.scope,assessment.lineage,assessment.generation,assessment.provenance)==(cmd.command_key,ids,cmd.validation_contract,v['validator_rule'],cmd.scope,cmd.lineage,cmd.generation,cmd.provenance),'VALIDATION_ASSESSMENT_BINDING')
 expected=v['semantic_expectations'];i.require(tuple(z.clause_id for z in assessment.clauses)==tuple(sorted(expected)),'VALIDATION_ASSESSMENT_CLAUSES')
 for clause in assessment.clauses:
  actual=c.parse_json(clause.actual_json.encode());exp=c.parse_json(clause.expected_json.encode())
  i.require(clause.expected_json==c.canonical_bytes(expected[clause.clause_id]).decode() and clause.actual_json==c.canonical_bytes(actual).decode() and clause.reasons==(() if exp==actual else ('SEMANTIC_MISMATCH:'+clause.clause_id,)),'VALIDATION_CLAUSE_WITNESS')
 # Check immutable witness binding, not a new decision or oracle invocation.
 actual={z.clause_id:c.parse_json(z.actual_json.encode()) for z in assessment.clauses}
 semantic_shape(actual,expected)
 i.require(c._identity(c.canonical_bytes(actual),cmd.semantic_binding.content_id.namespace)==cmd.semantic_binding.content_id,'VALIDATION_ASSESSMENT_CONTENT')
 outcome=m.ValidationOutcome.PASS if all(not x.reasons for x in assessment.clauses) else m.ValidationOutcome.FAIL
 i.require(assessment.outcome is outcome,'VALIDATION_OUTCOME')

def result(cmd,assessment,v,ids,b):
 until=min(b['valid_until'],v['semantic_expectations']['currentness']['valid_until'])
 z=m.ValidationResultRecord(ZERO,cmd.command_key,cmd.expected_snapshot,cmd.expected_parent_event,cmd.sequence,cmd.validation_contract,cmd.definition_set,cmd.evidence,cmd.receipt_reference,cmd.semantic_binding.semantic_evidence_id,cmd.semantic_binding.content_id,v['proposition'],v['validator_rule'],assessment.id,assessment.outcome,ids,cmd.scope,cmd.lineage,cmd.generation,until,cmd.provenance)
 return identified(z,'planner-validation-result-record-v1')

def predicate_id(r):
 c,i=env();return m.PredicateId('VALIDATION:'+i.digest({'contract':c._wire(r.validation_contract),'evidence':c._wire(r.evidence),'scope':r.scope,'lineage':r.lineage,'generation':r.generation},'planner-validation-projection-v1').sha256)

def project(snapshot,r):
 state=m.ValidationState.ACCEPTED if r.outcome is m.ValidationOutcome.PASS else m.ValidationState.REJECTED
 inst=m.ValidationInstance(predicate_id(r),r.proposition,r.provenance.identity,r.input_identities,r.outcome,r.scope,r.lineage,state,r.provenance)
 return replace(snapshot,entities=tuple(replace(e,validated=r.outcome is m.ValidationOutcome.PASS,validation=state) if e.id==r.evidence else e for e in snapshot.entities),validation_results=snapshot.validation_results+(r,),validation_instances=snapshot.validation_instances+(inst,))

def build(bundle,cmd,assessment):
 c,i=env();from . import core,gates
 record,d,b,n,a,x,e,g,v,ids=inputs(bundle,cmd);verify_assessment(cmd,assessment,v,ids)
 actual_currentness=c.parse_json(next(z.actual_json for z in assessment.clauses if z.clause_id=='currentness').encode())
 i.require(actual_currentness['valid_from']<=bundle.current.context.tick<=actual_currentness['valid_until'],'VALIDATION_SOURCE_NOT_CURRENT')
 r=result(cmd,assessment,v,ids,b)
 r=identified(replace(r,valid_until=min(r.valid_until,e.valid_until,v['source_requirements']['valid_until'],actual_currentness['valid_until'])),'planner-validation-result-record-v1')
 private=project(bundle.current,r)
 # Raw admitted receipt precheck has no dependence on support being constructed.
 proof=gates._check_receipt(private,g,e.id);accepted=proof.state is m.ProofState.PROVED
 i.require(accepted==(r.outcome is m.ValidationOutcome.PASS),'SUPPORT_POSTCONDITION_MISMATCH')
 observation=m.ReceiptObservation(g.id,e.id,accepted,proof.reasons,a.claims if accepted else ())
 sr=m.ValidationSupportRecord(ZERO,cmd.command_key,cmd.expected_parent_event,cmd.sequence,cmd.support_contract,r.id,e.id,cmd.receipt_reference,g.id,g.requirements,observation,m.ValidationSupportOutcome.ACCEPTED_RECEIPT_SUPPORT if accepted else m.ValidationSupportOutcome.REJECTED_RECEIPT_OBSERVATION,ids,cmd.scope,cmd.lineage,cmd.generation,n['support'].provenance)
 sr=identified(sr,'planner-validation-support-record-v1');private=replace(private,validation_support_records=private.validation_support_records+(sr,))
 post=core.apply_receipt(private,m.ExternalEvent(g.id,m.ExternalStage.EVIDENCE_VALIDATED,c.snapshot_id(private))).snapshot
 actual=post.receipt_observations[-1];i.require(actual==observation,'SUPPORT_OBSERVATION_MISMATCH')
 gate=next(z for z in post.external_gates if z.id==g.id)
 i.require(gates.external_complete(post,gate)==accepted and gate.stage is (m.ExternalStage.EVIDENCE_VALIDATED if accepted else m.ExternalStage.WAITING_FOR_EXTERNAL_EVIDENCE),'VALIDATION_POSTCONDITION')
 frame={'entities','validation_instances','validation_results','validation_support_records','receipt_observations','external_gates'}
 for f in fields(m.Snapshot):
  if f.name not in frame:i.require(getattr(post,f.name)==getattr(bundle.current,f.name),'VALIDATION_FRAME:'+f.name)
 z=m.ValidationSupportAdmission(cmd,assessment,r,sr,c.snapshot_id(post),ZERO)
 return replace(z,precommit_seal=seal(z)),post

def seal(admission):
 c,i=env();w=c._wire(admission);w.pop('precommit_seal');return i.digest(w,'planner-validation-support-precommit-v1')

def prepare(bundle,cmd,repo_root):
 c,i=env();c._replay(bundle);c._verify_sources(bundle,repo_root)
 assessment=assess(bundle,cmd,repo_root);a,post=build(bundle,cmd,assessment)
 trial=c._extend_private(bundle,a);c._replay(trial)
 return a,trial

def validate_prefix(bundle,admission):
 c,i=env();m.validate_types(admission,m.ValidationSupportAdmission)
 expected,post=build(bundle,admission.command,admission.assessment)
 i.require(c.canonical_bytes(c._wire(expected))==c.canonical_bytes(c._wire(admission)),'VALIDATION_PRECOMMIT_SUBSTITUTION')
 return post

def apply(snapshot,admission):
 """Historical projection verifies the full witness in the codec prefix first."""
 c,i=env();from . import core
 m.validate_types(admission,m.ValidationSupportAdmission);cmd=admission.command
 i.require(c.snapshot_id(snapshot)==cmd.expected_snapshot and key(cmd)==cmd.command_key and seal(admission)==admission.precommit_seal,'VALIDATION_PRE_STATE')
 # Event prefix admission checks receipt/event join. Snapshot projection rechecks
 # identities and the native receipt oracle; it never executes the validator.
 r=admission.validation_result;sr=admission.support
 i.require(r==identified(r,'planner-validation-result-record-v1') and sr==identified(sr,'planner-validation-support-record-v1') and sr.validation_result_id==r.id and r.command_key==cmd.command_key,'VALIDATION_RECORD_ID')
 private=replace(project(snapshot,r),validation_support_records=snapshot.validation_support_records+(sr,))
 post=core.apply_receipt(private,m.ExternalEvent(sr.gate,m.ExternalStage.EVIDENCE_VALIDATED,c.snapshot_id(private))).snapshot
 i.require(post.receipt_observations[-1]==sr.observation and c.snapshot_id(post)==admission.post_state,'VALIDATION_HISTORICAL_POSTCONDITION')
 return core.TransitionReport(post,(),core.recompute(post))

def commit(bundle,admission,output_dir,repo_root,*,failure_hook=None):
 c,i=env();c._replay(bundle);c._verify_sources(bundle,repo_root);directory=c._transaction_directory(output_dir,repo_root)
 with c._transaction_lock(directory):
  head=c._read_head(directory,bundle,repo_root)
  i.require(c.canonical_bytes(c._wire(head.initial))==c.canonical_bytes(c._wire(bundle.initial)) and c.canonical_bytes(c._wire(head.events[:len(bundle.events)]))==c.canonical_bytes(c._wire(bundle.events)),'VALIDATION_UNTRUSTED_LINEAGE')
  for index,event in enumerate(head.events):
   if type(event.result) is m.ValidationSupportAdmission and event.result.command.command_key==admission.command.command_key:
    i.require(c.canonical_bytes(c._wire(event.result))==c.canonical_bytes(c._wire(admission)),'VALIDATION_IDEMPOTENCY_CONFLICT')
    return head,c.bundle_id(c._prefix_bundle(head,index+1)),True
  i.require(c.bundle_id(head)==c.bundle_id(bundle),'VALIDATION_STALE_HEAD')
  validate_prefix(head,admission)
  if failure_hook:failure_hook('validated')
  updated=c._extend_private(head,admission);c._replay(updated)
  if failure_hook:failure_hook('staged')
  ident=c._publish_head(directory,updated,c.bundle_id(head),admission.command.command_key,repo_root)
  return updated,ident,False

def validate_records(snapshot):
 """Admission guard for public native queries; no proposition-only substitution."""
 c,i=env()
 for field in ('validation_contracts','validation_support_contracts','validation_transaction_contracts','validation_results','validation_support_records'):
  values=getattr(snapshot,field);m.unique(values,lambda x:x.id)
 m.unique(snapshot.validation_results,lambda r:(r.evidence,r.validation_contract,r.generation))
 for support in snapshot.validation_support_records:
  i.require(any(r.id==support.validation_result_id for r in snapshot.validation_results),'VALIDATION_SUPPORT_WITHOUT_RESULT')
 for r in snapshot.validation_results:
  i.require(r==identified(r,'planner-validation-result-record-v1'),'VALIDATION_RESULT_ID')
  sr=[x for x in snapshot.validation_support_records if x.validation_result_id==r.id]
  i.require(len(sr)==1,'VALIDATION_SUPPORT_REQUIRED')
  s=sr[0];i.require(s==identified(s,'planner-validation-support-record-v1') and s.evidence==r.evidence and s.receipt_reference==r.receipt_reference and s.command_key==r.command_key and s.observation.artifact==r.evidence and s.observation.accepted==(r.outcome is m.ValidationOutcome.PASS) and s.outcome is (m.ValidationSupportOutcome.ACCEPTED_RECEIPT_SUPPORT if s.observation.accepted else m.ValidationSupportOutcome.REJECTED_RECEIPT_OBSERVATION),'VALIDATION_SUPPORT_RECORD')
 for entity in snapshot.entities:
  if entity.kind is not m.EntityKind.EVIDENCE or not entity.validated or entity.validation is not m.ValidationState.ACCEPTED:continue
  claims={claim.requirement for a in snapshot.receipt_admissions if a.artifact==entity.id for claim in a.claims}
  gates=[g for g in snapshot.external_gates if (g.pending==entity.id or claims.intersection(g.requirements)) and registered(snapshot,g.id)]
  if not gates:continue
  rs=[r for r in snapshot.validation_results if r.evidence==entity.id and r.outcome is m.ValidationOutcome.PASS]
  i.require(len(rs)==1,'VALIDATION_REGISTERED_RESULT_REQUIRED')
  r=rs[0];i.require(snapshot.context.tick<=r.valid_until and (r.scope,r.lineage,r.generation)==(snapshot.context.scope,snapshot.context.lineage,snapshot.context.generation),'VALIDATION_RESULT_NOT_CURRENT')
  record=next(x for x in snapshot.installed_definitions if x.id==r.definition_set)
  i.require(record.validation is m.ValidationState.ACCEPTED,'VALIDATION_SET_INVALIDATED')
  i.validate_authority(record.request,snapshot.context)
  inst=next((v for v in snapshot.validation_instances if v.predicate==predicate_id(r)),None)
  i.require(inst is not None and inst.result is m.ValidationOutcome.PASS and inst.currentness is m.ValidationState.ACCEPTED and inst.inputs==r.input_identities and inst.dossier==r.provenance.identity,'VALIDATION_PROJECTION_REQUIRED')
