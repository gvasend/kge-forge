"""Closed atomic validation/support definition adapter. Installation is configuration."""
from dataclasses import replace
from pathlib import Path
from . import model as m

TYPE='VALIDATION_SUPPORT_DEFINITION_SET'
MEMBERS={
 'validation':(m.EvidenceValidationContract,'EVIDENCE_VALIDATION_CONTRACT','PLANNER-EVIDENCE-VALIDATION-CONTRACT-1'),
 'support':(m.EvidenceValidationSupportContract,'EVIDENCE_VALIDATION_SUPPORT_CONTRACT','PLANNER-EVIDENCE-VALIDATION-SUPPORT-CONTRACT-1'),
 'transaction':(m.EvidenceValidationTransactionContract,'EVIDENCE_VALIDATION_TRANSACTION_CONTRACT','PLANNER-EVIDENCE-VALIDATION-TRANSACTION-CONTRACT-1')}
FIELDS={
 'validation':set('accepted_outcomes consumer currentness_rule fail_is_not_support generation lineage proposition provenance_rule receipt_requirement scope semantic_expectations source_requirements target_identity_domain target_selector target_type validator_protocol_pin validator_rule'.split()),
 'support':set('acceptance_rule claims_rule consumer currentness_rule generation inputs lineage predicate predicate_id proof_boundary provenance_rule scope source_requirements subject support_instance_currentness_rule support_type target validation_contract'.split()),
 'transaction':set('atomic_result_support_publication consumer event_type lifecycle_results_created_by_installation native_lifecycle_transition operand_type ordinary_parent_required positive_control_oracle postcondition_profile protocol_pin provenance_rule scope_lineage_generation support_contract valid_from valid_until validation_contract'.split())}

def env():
 from . import codec as c,installation as i
 return c,i

def base_descriptor(definition,typ,schema):
 c,i=env();q=i.require;d=c.parse_json(definition.descriptor_json.encode());p=definition.provenance
 q(set(d)==set('schema definition_type canonical_body_schema content_id subject scope lineage generation canonical_source_reference source_pin provenance currentness_rule'.split()),'VALIDATION_DEFINITION_SCHEMA')
 q(c.canonical_bytes(d).decode()==definition.descriptor_json and d['schema']=='PLANNER-INSTALLABLE-DEFINITION-1' and d['definition_type']==typ and d['canonical_body_schema']==schema and definition.id==i.digest(d,'planner-installable-definition-v1'),'VALIDATION_DEFINITION_ID')
 q(p.path and not Path(p.path).is_absolute() and '..' not in Path(p.path).parts and Path(p.path).as_posix()==p.path,'VALIDATION_SOURCE_PATH')
 q(i.identity(d['content_id'])==p.identity==c._identity(p.excerpt.encode(),'raw-file-sha256'),'VALIDATION_CONTENT')
 q(d['source_pin']=={'path':p.path,'profile':'raw-file-sha256','pointer':'','identity':i.simple(p.identity)} and d['canonical_source_reference']=={'kind':'IMMUTABLE_FILE','path':p.path,'content_id':i.simple(p.identity)} and d['provenance']=={'path':p.path,'content_id':i.simple(p.identity),'section':p.section,'method':p.method,'scope':p.scope} and p.scope==d['scope'] and p.section=='/','VALIDATION_SOURCE_PIN')
 r=d['currentness_rule'];q(set(r)==set('activation_witness authority_current_required consumer exact_scope_lineage_generation_required installation_required rule_id schema source_current_required'.split()) and r['schema']=='PLANNER-DEFINITION-CURRENTNESS-1' and r['rule_id']=='VALIDATION_SUPPORT_SET_CURRENT_V1' and r['consumer']==d['subject']['consumer'] and all(r[k] is True for k in ('authority_current_required','exact_scope_lineage_generation_required','installation_required','source_current_required')),'VALIDATION_CURRENTNESS_RULE')
 b=c.parse_json(p.excerpt.encode());q(set(b)=={'schema','contract'} and b['schema']==schema and c.canonical_bytes(b).decode()==p.excerpt and type(b['contract']) is dict,'VALIDATION_NATIVE_BODY')
 return d,b['contract']

def descriptor(definition):
 c,i=env();q=i.require;d,b=base_descriptor(definition,TYPE,'PLANNER-VALIDATION-SUPPORT-DEFINITION-SET-1')
 q(set(b)==set('consumer generation lineage members membership operation projection protocol_pin role scope valid_from valid_until'.split()),'VALIDATION_SET_SCHEMA')
 q(b['role']==d['subject'] and d['subject']['kind']=='EVIDENCE_VALIDATION_SUPPORT_ROLE' and set(d['subject'])==set('kind gate requirements consumer dependent_action'.split()),'VALIDATION_ROLE')
 q(b['operation']=='INSTALL' and b['membership']=='All three members one atomic definition set; individual member INSTALL prohibited' and b['projection']=='Definitions and membership only; no ValidationResult, native ValidationInstance or ReceiptObservation','VALIDATION_INSTALL_FRAME')
 q(d['currentness_rule']['activation_witness']=='OWN_INSTALL_EVENT_AND_EXACT_ATOMIC_MEMBERSHIP','VALIDATION_ACTIVATION')
 ctx=(d['scope'],d['lineage'],d['generation']);q(ctx==(b['scope'],b['lineage'],b['generation']) and b['consumer']==d['subject']['consumer'],'VALIDATION_CONTEXT')
 q(type(b['valid_from']) is int and type(b['valid_until']) is int and b['valid_from']<=b['valid_until'],'VALIDATION_VALIDITY')
 q(set(b['members'])==set(MEMBERS),'VALIDATION_ATOMIC_MEMBERS');native={}
 for key,(cls,typ,schema) in MEMBERS.items():
  x=b['members'][key];q(set(x)=={'body','body_pin','definition_id','descriptor'},'VALIDATION_MEMBER_SCHEMA')
  md=x['descriptor'];pin=x['body_pin'];raw=c.canonical_bytes({'schema':schema,'contract':x['body']}).decode()
  p=m.Provenance(pin['path'],i.identity(pin['identity']),md['provenance']['section'],raw,md['provenance']['method'],md['scope'])
  member=m.InstallableDefinition(i.identity(x['definition_id']),c.canonical_bytes(md).decode(),p)
  dd,bb=base_descriptor(member,typ,schema)
  q(set(bb)==FIELDS[key] and (dd['scope'],dd['lineage'],dd['generation'])==ctx and dd['subject']==dict(d['subject'],kind=typ.replace('_CONTRACT','_MEMBER_ROLE')),'VALIDATION_MEMBER_BINDING')
  q(pin==md['source_pin'] and dd['currentness_rule']['activation_witness']=='MEMBER_OF_ONE_ATOMIC_INSTALLED_SET; NOT_INDIVIDUALLY_INSTALLABLE','VALIDATION_MEMBER_ACTIVATION')
  native[key]=cls(member.id,raw,p)
 v,s,t=(c.parse_json(native[k].body_json.encode())['contract'] for k in ('validation','support','transaction'))
 q(v['validator_rule']=='CANONICAL_AUTHENTICATED_EVIDENCE_VALIDATION_V1' and v['target_type']=='GraphEntity:EVIDENCE' and v['accepted_outcomes']==['PASS','FAIL'] and v['fail_is_not_support'] is True,'VALIDATION_RULE')
 q(s['validation_contract']==i.simple(native['validation'].id) and t['validation_contract']==s['validation_contract'] and t['support_contract']==i.simple(native['support'].id),'VALIDATION_MEMBER_DAG')
 q(v['validator_protocol_pin']==b['protocol_pin']==t['protocol_pin'] and v['source_requirements']==s['source_requirements'],'VALIDATION_PROTOCOL_BINDING')
 q(t['event_type']=='VALIDATE_EVIDENCE_SUPPORT' and t['operand_type']=='ValidationSupportAdmission' and t['atomic_result_support_publication'] is True and t['ordinary_parent_required'] is True and t['lifecycle_results_created_by_installation'] is False and t['postcondition_profile']=='V01_RECEIVED_TO_VALIDATED_WITHOUT_REENTRY_V1','VALIDATION_EVENT_CONTRACT')
 return d,(b,native)

def extra_provenances(request):
 c,i=env();d,(b,native)=descriptor(request.definition)
 v=c.parse_json(native['validation'].body_json.encode())['contract'];pins=[b['protocol_pin'],v['source_requirements']['expectation_source'],v['source_requirements']['binding_template_source']]
 expected={(p['path'],i.identity(p['identity'])) for p in pins}
 i.require(len(request.definition_sources)==len(expected) and {(p.path,p.identity) for p in request.definition_sources}==expected,'VALIDATION_DEFINITION_SOURCE_SET')
 for p in request.definition_sources:
  i.require(p.identity==c._identity(p.excerpt.encode(),'raw-file-sha256') and p.scope==d['scope'] and p.section=='/' and c.canonical_bytes(c.parse_json(p.excerpt.encode())).decode()==p.excerpt,'VALIDATION_DEFINITION_SOURCE_BYTES')
 sources={p.path:c.parse_json(p.excerpt.encode()) for p in request.definition_sources}
 i.require(sources[v['source_requirements']['expectation_source']['path']]==v['semantic_expectations'],'VALIDATION_EXPECTATION_SOURCE')
 protocol=sources[b['protocol_pin']['path']]
 i.require(protocol.get('schema')=='PLANNER-VALIDATION-SUPPORT-PROTOCOL-1' and protocol.get('version')==1,'VALIDATION_PROTOCOL_SOURCE')
 template=sources[v['source_requirements']['binding_template_source']['path']]
 i.require(set(template)=={'schema','template_only','binding','instance_boundary'} and template['schema']=='PLANNER-SEMANTIC-NATIVE-BINDING-TEMPLATE-1' and template['template_only'] is True,'VALIDATION_BINDING_TEMPLATE')
 m.validate_types(m.SemanticNativeBinding(**{k:c._unwire(x) for k,x in template['binding'].items()}),m.SemanticNativeBinding)
 i.require(template['binding']==v['target_selector']['native_binding_template'],'VALIDATION_TEMPLATE_DEFINITION_BINDING')
 return tuple(x.provenance for x in native.values())+request.definition_sources

def support_current(snapshot,record):
 c,i=env()
 try:
  d,(b,native)=descriptor(record.request.definition);ctx=snapshot.context
  i.require(record.validation is m.ValidationState.ACCEPTED and i.old_reference(snapshot,d)==record.id,'VALIDATION_SET_INACTIVE')
  i.validate_authority(record.request,ctx)
  i.require((ctx.scope,ctx.lineage,ctx.generation)==(d['scope'],d['lineage'],d['generation']) and b['valid_from']<=ctx.tick<=b['valid_until'],'VALIDATION_CONTEXT_CURRENT')
  extra_provenances(record.request)
  for key,field in [('validation','validation_contracts'),('support','validation_support_contracts'),('transaction','validation_transaction_contracts')]:
   i.require(native[key] in getattr(snapshot,field),'VALIDATION_MEMBER_NOT_CANONICAL')
  v=c.parse_json(native['validation'].body_json.encode())['contract'];subject=d['subject']
  gate=next(g for g in snapshot.external_gates if g.id.value==subject['gate'])
  reqs=[r for r in snapshot.evidence_requirements if r.id.value in subject['requirements']]
  i.require(len(reqs)==len(subject['requirements'])==1 and reqs[0].proposition==v['proposition'] and reqs[0].id in gate.requirements,'VALIDATION_GATE_BINDING')
  req=reqs[0];sr=v['source_requirements'];support=c.parse_json(native['support'].body_json.encode())['contract']
  i.require(sr['gate_definition_source']==c._wire(gate.provenance) and sr['requirement_definition_source']==c._wire(req.provenance) and set(c._unwire(z) for z in sr['producer_identities'])==set(req.producers) and c._unwire(sr['target'])==req.target and sr['scope_lineage_generation']=={'scope':ctx.scope,'lineage':ctx.lineage,'generation':ctx.generation} and sr['valid_from']<=ctx.tick<=sr['valid_until'],'VALIDATION_SOURCE_APPLICABILITY')
  i.require(any(p.id.value==support['predicate_id'] and p.obligation==req.id and p.kind is m.PredicateKind.EVIDENCE_OBLIGATION for p in snapshot.predicates),'VALIDATION_SUPPORT_PREDICATE')
  i.require(v['target_selector']['gate']==gate.id.value and v['target_selector']['requirement']==req.id.value and v['target_selector']['require_unique_actual_admitted_entity'] is True and support['target']=={'gate':gate.id.value,'native_projection':'ReceiptObservation','requirements':subject['requirements']},'VALIDATION_TARGET_BINDING')
  from . import authentication_installation as auth
  ingress=[x for x in snapshot.ingress_contracts if x.gate==gate.id]
  i.require(len(ingress)==1,'VALIDATION_AUTHENTICATION_MISSING')
  rec=next(x for x in snapshot.installed_definitions if i.descriptor(x.request.definition)[0]['definition_type']=='EVIDENCE_INGRESS_CONTRACT' and i.descriptor(x.request.definition)[1]==ingress[0])
  i.require(auth.support_current(snapshot,rec),'VALIDATION_AUTHENTICATION_NOT_CURRENT')
  return True
 except (m.PlannerError,StopIteration,AttributeError,KeyError):return False

def apply(snapshot,request,d,parsed):
 c,i=env();from .core import TransitionReport,recompute
 b,native=parsed
 i.require(request.operation is m.InstallationOperation.INSTALL and not request.authority_bindings,'VALIDATION_INSTALL_ONLY')
 extra_provenances(request)
 i.require(not any(x.id==native[k].id for k,field in [('validation','validation_contracts'),('support','validation_support_contracts'),('transaction','validation_transaction_contracts')] for x in getattr(snapshot,field)),'VALIDATION_MEMBER_CONFLICT')
 record=m.InstalledDefinition(i.installed_id(request),request,None)
 after=replace(snapshot,installed_definitions=snapshot.installed_definitions+(record,),validation_contracts=snapshot.validation_contracts+(native['validation'],),validation_support_contracts=snapshot.validation_support_contracts+(native['support'],),validation_transaction_contracts=snapshot.validation_transaction_contracts+(native['transaction'],))
 i.require(support_current(after,record),'VALIDATION_SET_NOT_APPLICABLE')
 m.validate_model(after)
 return TransitionReport(after,(),recompute(after))
