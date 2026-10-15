"""Governed native Action definition replacement; never executes an Action."""
from dataclasses import fields, replace
from pathlib import Path
from . import model as m

TYPE = 'ACTION_DEFINITION'

def same_action(left,right):
    c,_=env()
    return c.canonical_bytes(c._wire(left))==c.canonical_bytes(c._wire(right))

def env():
    from . import codec as c, installation as i
    return c, i

def descriptor(definition):
    c,i=env();q=i.require;p=definition.provenance
    d=c.parse_json(definition.descriptor_json.encode())
    q(set(d)==set('schema definition_type canonical_body_schema content_id subject scope lineage generation canonical_source_reference source_pin provenance currentness_rule'.split()),'ACTION_DEFINITION_SCHEMA')
    q(c.canonical_bytes(d).decode()==definition.descriptor_json and d['schema']=='PLANNER-INSTALLABLE-DEFINITION-1' and d['definition_type']==TYPE and d['canonical_body_schema']=='PLANNER-ACTION-DEFINITION-1' and definition.id==i.digest(d,'planner-installable-definition-v1'),'ACTION_DEFINITION_ID')
    q(p.path and not Path(p.path).is_absolute() and '..' not in Path(p.path).parts and Path(p.path).as_posix()==p.path,'ACTION_SOURCE_PATH')
    q(i.identity(d['content_id'])==p.identity==c._identity(p.excerpt.encode(),'raw-file-sha256'),'ACTION_CONTENT')
    q(d['source_pin']=={'path':p.path,'profile':'raw-file-sha256','pointer':'','identity':i.simple(p.identity)} and d['canonical_source_reference']=={'kind':'IMMUTABLE_FILE','path':p.path,'content_id':i.simple(p.identity)} and d['provenance']=={'path':p.path,'content_id':i.simple(p.identity),'section':p.section,'method':p.method,'scope':p.scope} and p.section=='/' and p.scope==d['scope'],'ACTION_SOURCE_PIN')
    subject=d['subject'];q(set(subject)=={'kind','action','consumer'} and subject['kind']=='ACTION_ROLE' and all(type(x) is str and x for x in subject.values()),'ACTION_ROLE')
    q(d['currentness_rule']=={'schema':'PLANNER-DEFINITION-CURRENTNESS-1','rule_id':'ACTION_DEFINITION_CURRENT_V1','consumer':subject['consumer'],'activation_witness':'OWN_INSTALL_EVENT_AND_EXACT_ACTION','authority_current_required':True,'exact_scope_lineage_generation_required':True,'installation_required':True,'source_current_required':True},'ACTION_CURRENTNESS_RULE')
    b=c.parse_json(p.excerpt.encode())
    q(set(b)=={'schema','contract'} and b['schema']=='PLANNER-ACTION-DEFINITION-1' and c.canonical_bytes(b).decode()==p.excerpt,'ACTION_NATIVE_BODY')
    b=b['contract'];q(set(b)=={'old_action','action','allowed_changes'},'ACTION_CONTRACT_SCHEMA')
    names={'$type'}|{f.name for f in fields(m.Action)}
    q(all(type(b[k]) is dict and names-c.P03_FIELDS.get(m.Action,set()) <= set(b[k]) <= names and b[k]['$type']=='Action' for k in ('old_action','action')),'ACTION_REQUIRED_FIELDS')
    old,new=(c._unwire(b[k]) for k in ('old_action','action'))
    for a in (old,new):
        m.validate_types(a,m.Action);m.validate_provenance(a.source)
        for k in a.accepted_inventory:m.validate_knowledge(k)
    q(old.id==new.id==m.ActionId(subject['action']),'ACTION_IDENTITY')
    q(new.source.scope==d['scope'],'ACTION_SCOPE')
    changes=b['allowed_changes'];q(type(changes) is list and len(changes)==len(set(changes)) and all(x in names-{'$type','id'} for x in changes),'ACTION_FRAME_SCHEMA')
    actual={f.name for f in fields(old) if getattr(old,f.name)!=getattr(new,f.name)}
    q(actual==set(changes) and bool(actual),'ACTION_FRAME')
    return d,(old,new)

def extra_provenances(request):
    c,i=env();d,(old,new)=descriptor(request.definition)
    return tuple(dict.fromkeys((old.source,new.source)+tuple(k.provenance for a in (old,new) for k in a.accepted_inventory)))

def support_current(snapshot,record):
    c,i=env()
    try:
        d,(old,new)=descriptor(record.request.definition);ctx=snapshot.context
        i.require(record.validation is m.ValidationState.ACCEPTED and i.old_reference(snapshot,d)==record.id,'ACTION_DEFINITION_INACTIVE')
        i.validate_authority(record.request,ctx)
        i.require((ctx.scope,ctx.lineage,ctx.generation)==(d['scope'],d['lineage'],d['generation']),'ACTION_CONTEXT')
        i.require(same_action(next(a for a in snapshot.actions if a.id==new.id),new),'ACTION_NOT_CANONICAL')
        return True
    except (m.PlannerError,StopIteration,AttributeError,KeyError):return False

def action_current(snapshot,action):
    c,i=env()
    # Unrelated definition classes cannot govern this Action. Fully validate the
    # selected Action record below; do not repeatedly parse their typed bodies.
    records=[]
    for r in snapshot.installed_definitions:
        d=c.parse_json(r.request.definition.descriptor_json.encode())
        if d.get('definition_type')==TYPE and d.get('subject',{}).get('action')==action.id.value:
            records.append(r)
    return not records or support_current(snapshot,max(records,key=lambda r:r.request.sequence))

def apply(snapshot,request,d,parsed):
    c,i=env();from .core import TransitionReport,recompute
    old,new=parsed
    i.require(request.operation is m.InstallationOperation.REPLACE and not request.authority_bindings and not request.definition_sources,'ACTION_REPLACE_ONLY')
    i.require(same_action(next((a for a in snapshot.actions if a.id==old.id),None),old),'ACTION_OLD_CONTENT')
    i.require(not any(s.id==old.id and s.state is m.ActionState.COMPLETED for s in snapshot.statuses),'ACTION_ALREADY_EXECUTED')
    record=m.InstalledDefinition(i.installed_id(request),request,request.expected_old_reference)
    after=replace(snapshot,actions=tuple(new if a.id==new.id else a for a in snapshot.actions),installed_definitions=snapshot.installed_definitions+(record,))
    m.validate_model(after);i.require(support_current(after,record),'ACTION_NOT_APPLICABLE')
    return TransitionReport(after,(),recompute(after))
