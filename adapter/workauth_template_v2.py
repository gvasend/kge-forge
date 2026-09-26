"""Constraint-only WorkAuthorization lifecycle template.

Template records never carry concrete invocation values. They define bounded
lifecycle constraints and are independently identity-bound.
"""
import json, hashlib

SCHEMA = 'WORK-AUTHORIZATION-TEMPLATE-2'
class TemplateDenied(ValueError): pass

def canonical(v): return json.dumps(v, sort_keys=True, separators=(',',':')).encode()
def digest(v): return hashlib.sha256(canonical(v)).hexdigest()

def construct(body):
    required={'schema','lifecycle_schema','initial_state','initial_ownership','required_binding_classes','policy_constraints','runtime_scope','release_scope','replay_policy','lifecycle_envelope'}
    if set(body)!=required or body['schema']!=SCHEMA: raise TemplateDenied('template schema/fields invalid')
    if body['initial_state']!='INACTIVE' or body['initial_ownership']!='NONE': raise TemplateDenied('invalid initial constraints')
    ident='WorkAuthorizationTemplate-sha256:'+digest(body)
    return {**body,'WorkAuthorizationTemplateId':ident}

def validate(record):
    if record.get('schema')!=SCHEMA: raise TemplateDenied('wrong template')
    body={k:v for k,v in record.items() if k!='WorkAuthorizationTemplateId'}
    expected='WorkAuthorizationTemplate-sha256:'+digest(body)
    if record.get('WorkAuthorizationTemplateId')!=expected: raise TemplateDenied('template identity mismatch')
    if body['initial_state']!='INACTIVE' or body['initial_ownership']!='NONE': raise TemplateDenied('initial constraint mismatch')
    return expected
