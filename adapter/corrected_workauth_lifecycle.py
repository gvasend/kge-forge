"""Corrected lifecycle boundary: template constraints, concrete WorkAuthorization,
and external single-use issuance authority are independently authenticated."""
from .workauth_template_v2 import validate as validate_template, TemplateDenied
from .workauth_issuance import validate as validate_issuance, IssuanceDenied
class CorrectedLifecycleDenied(ValueError): pass

def validate_and_issue(template, issuance, workauth, invocation, dispatch, runtime, release, audit_unused=True):
    try:
        validate_template(template)
        if workauth.get('schema')!='WORK-AUTHORIZATION-1' or workauth.get('WorkAuthorizationId') is None: raise CorrectedLifecycleDenied('invalid concrete WorkAuthorization')
        if workauth.get('InvocationAttemptId')!=invocation.get('InvocationAttemptId') or workauth.get('DispatchAuthorizationId')!=dispatch.get('authority_id'): raise CorrectedLifecycleDenied('concrete binding mismatch')
        validate_issuance(issuance,template,workauth,invocation,dispatch,runtime,release)
        if not audit_unused: raise CorrectedLifecycleDenied('audit namespace used')
        return {'state':'INACTIVE','ownership':'NONE','authorization_id':invocation['InvocationAttemptId']}
    except (TemplateDenied,IssuanceDenied,KeyError,TypeError) as e:
        raise CorrectedLifecycleDenied(str(e)) from e
