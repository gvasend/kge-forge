"""External, single-use issuance authority for corrected WorkAuthorization."""
import json, hashlib
SCHEMA='WORKAUTH-ISSUANCE-AUTHORITY-1'
class IssuanceDenied(ValueError): pass

def canonical(v): return json.dumps(v,sort_keys=True,separators=(',',':')).encode()
def digest(v): return hashlib.sha256(canonical(v)).hexdigest()
def construct(body):
    required={'schema','template_id','workauthorization_id','invocation_attempt_id','dispatch_id','runtime','release_context','architect_decision','scope','replay'}
    if set(body)!=required or body['schema']!=SCHEMA: raise IssuanceDenied('issuance schema/fields invalid')
    if body['scope']!='EXACT_SINGLE_WORKAUTHORIZATION_INACTIVE': raise IssuanceDenied('issuance scope expanded')
    if body['replay']!='REJECT': raise IssuanceDenied('replay policy invalid')
    return {**body,'IssuanceAuthorityId':'WorkAuthorizationIssuance-sha256:'+digest(body)}
def validate(record,template,workauth,invocation,dispatch,runtime,release):
    if record.get('schema')!=SCHEMA: raise IssuanceDenied('wrong issuance authority')
    body={k:v for k,v in record.items() if k!='IssuanceAuthorityId'}
    if record.get('IssuanceAuthorityId')!='WorkAuthorizationIssuance-sha256:'+digest(body): raise IssuanceDenied('issuance identity mismatch')
    if body['template_id']!=template['WorkAuthorizationTemplateId'] or body['workauthorization_id']!=workauth['WorkAuthorizationId']: raise IssuanceDenied('authority binding mismatch')
    if body['invocation_attempt_id']!=invocation['InvocationAttemptId'] or body['dispatch_id']!=dispatch['authority_id']: raise IssuanceDenied('invocation/dispatch mismatch')
    if body['runtime']!=runtime or body['release_context']!=release: raise IssuanceDenied('runtime/release mismatch')
    return True
