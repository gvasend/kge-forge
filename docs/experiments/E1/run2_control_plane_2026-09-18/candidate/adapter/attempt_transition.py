"""Authenticated, exact r9-to-r10 material transition. PREPARED is non-effecting."""
import json,os
from pathlib import Path
from .context_projection import canonical,digest,sha,read_exact
from .controller_authority_store import current,read_authority_ref,outside
from .attempt_context import require,read,ident,unseal,peer,predecessor,identities
from .continuation_envelope import seal,BODY_KEYS
from .terminal_attempt import classify
PROPOSAL_SHA='35fde13e12ee9318fca076c5a28aa898718e83074e65c3ada7f14e54830363e4'
REASON='PRE_MODEL_DISPATCHER_SESSION_COMPOSITION_FAILURE_NO_EFFECTS'
PREVIOUS='E1-RELEASE-AUTHORITY-sha256:a8e228850a699e201cd2202b76c6de7de976e7aa34890f3247afda4a599f0708'
RULES=('exact_dispatch_and_attempt_ancestry','terminal_CANCELLED','ownership_released','no_execution_scope',
 'no_model_or_provider_request','no_ActionRequest_or_effect','no_uncertainty','specific_successor_authorization',
 'new_unused_audit','no_inherited_lifecycle_ownership_counters','no_automatic_retry')
def selected(store=None):
 store=store or current();require(store is not None,'private store required')
 s=json.loads(store.resolve(store.applicability['authorization_id']+':terminal-attempt-context'))
 require(set(s)=={'mode','amendment','continuation','specific_invocation_authorization','qualification'},'selection shape')
 require(s['mode'] in ('PREPARED','ISSUED'),'unknown selection mode');return s

def terminal(store,a,p,proof):
 from .activation_transaction import invocation,_read
 from .invocation_ownership import InvocationOwnership
 from .run_control import events
 t=proof['terminal'];require(t['audit']==p['predecessor']['audit'] and t['audit_sha256']==p['predecessor']['audit_sha256'],'predecessor audit substituted')
 read_exact(t['audit'],t['audit_sha256'])
 # Captured shared-ledger ownership is historical observation, never current
 # predecessor authority. Re-read the strict ledger and attribute every owner.
 from .attempt_ownership import observe,attribute
 predecessor_id=p['predecessor']['authorization_id']
 owner,scope,_=observe(proof['authorization']['ownership_ledger'])
 attribute(owner,scope,[predecessor_id],p['invocation_identity'],p['audit'])
 require(classify(events(Path(t['audit'])),t['lifecycle'],t['actions'],None,None,predecessor_id)=='ACTIVE_CANCELLED_PRE_MODEL_NO_EFFECTS','unqualified predecessor class for this transition')
 # This function never grants ACTIVE/handoff: lifecycle reconstruction and the
 # transaction still require the current owner's exact committed reservation.
 return t

def decision(spec):
 store=current();s=selected();require(s['amendment']==spec['amendment'] and s['continuation']==spec['continuation'],'unselected transition')
 amendment=read(spec['amendment']);a=unseal(amendment,'E1-RUN2-TERMINAL-ATTEMPT-AMENDMENT')
 require(a['schema']=='E1-RUN2-TERMINAL-ATTEMPT-1' and a['rules']==list(RULES) and a['reason']==REASON,'transition rules changed')
 require(a['predecessor_release_authority']==PREVIOUS and a['proposal']['sha256']==PROPOSAL_SHA,'unaccepted transition')
 source=read(a['authority_source'])
 require(source=={'authority':'Architect','channel':'user','decision':'AUTHORIZE_QUALIFICATION_AND_CONSTRUCTION_OF_EXACT_R9_TO_R10_TRANSITION',
  'accepted_candidate':a['proposal'],'predecessor_release_authority':PREVIOUS,'parent_dispatch':a['parent_dispatch'],
  'rules':list(RULES),'reason':REASON,'issuance_authorized':False},'unattributed material transition')
 p=read(a['proposal']);require(p['invocation_identity']['authorization_id']==store.applicability['authorization_id'],'alternate successor forbidden')
 require(p['schema']=='PROPOSED-INVOCATION-ATTEMPT-BINDING-1' and p['automatic_retry'] is False and
  p['ownership']=='NONE' and p['proposed_initial_state']=='INACTIVE' and not any(p['inheritance'].values()),'attempt inherits authority')
 require(p['dispatch']==a['parent_dispatch'] and p['replacement_reason']==REASON,'dispatch/reason substituted')
 original=read(a['parent_dispatch']);require(original['authority']=='Architect' and original['decision']=='DISPATCH_AUTHORIZED' and
  p['DispatchAuthorizationId']==a['parent_dispatch']['authority_id'],'original dispatch unauthenticated')
 c=read(spec['continuation']);body={k:c[k] for k in BODY_KEYS}
 require(c==seal(body,c['approval']) and c['classification']=='NON_MATERIAL_IMPLEMENTATION_CONTINUATION','invalid correction candidate')
 require(c['approval'] is None,'unissued candidate cannot fabricate continuation adoption')
 require(a['correction_continuation']==spec['continuation'] and body['authority']==a['authority_source'] and body['authority_invariants']==p['bindings'],'corrections change authority')
 q=read(body['evidence']);require(q['status']=='PASS_SYNTHETIC_NOT_PRODUCTION_ADOPTION','correction qualification absent')
 require({Path(x['path']).name for x in body['artifacts']}=={'orchestration_boundary.py','operator_projection.py','run_control.py'},'unrelated non-material delta')
 for x in body['artifacts']:require(sha(read_authority_ref(x['new_content']))==x['new_sha256'],'correction content substituted')
 runtime=read(a['controller_runtime']);require(runtime['identity']=='sha256:'+digest(runtime['files']),'runtime identity mismatch')
 root=Path(runtime['root']);outside(root,store.catalog['programmer_roots'])
 require(Path(__file__).resolve().parent==root/'adapter' and {f.name:sha(f.read_bytes()) for f in (root/'adapter').glob('*.py')}==runtime['files'],'unexplained implementation')
 for x in body['artifacts']:require(runtime['files'][Path(x['path']).name]==x['new_sha256'],'correction not integrated')
 return s,amendment,a,c,p,original,runtime

def verify(owner):
 store=current();spec=owner.spec
 require(set(spec)=={'schema','amendment','continuation','identities','release_basis','release_decision','released_profile','clearance'} and spec['schema']==6 and digest(spec)==owner._issued_digest,'transition context changed')
 s,amendment,a,c,p,original,runtime=decision(spec);proof=predecessor(store,a);old=proof['governance'];oldop=json.loads(proof['authorization']['operational_binding'])
 require(old['run5']['release_authority']==PREVIOUS and proof['dispatch']['parent_dispatch']==a['parent_dispatch'],'released attempt ancestry changed')
 require(proof['authorization']['authorization_id']==p['predecessor']['authorization_id'] and
  old['run5']['proposal']['predecessor']==p['historical_r8'],'r8/r9 attempt ancestry changed')
 for k in ('release_basis','release_decision','released_profile','clearance'):require(spec[k]==oldop['governance'][k],'profile/clearance authority replaced')
 # Accepted candidate names prior authority; this append-only amendment derives context-only changes.
 expected=dict(p['bindings']);checks={**old['identities'],**{k:proof['context'][k] for k in ('FullContextDigest','ModelPayloadDigest','ModelProjectionBindingDigest')},'release_authority':PREVIOUS}
 for k,v in checks.items():require(expected[k]==v,'candidate prior context mismatch: '+k)
 for k in ('current_supervisor','succession_head','work_package_id','released_profile_sha256','budget_policy_identity','transmission_retention_identity','implementation_identity','material_amendment'):
  require(expected[k]==old['run5']['proposal']['bindings'][k],'released binding changed: '+k)
 require(expected['controller_runtime_identity']==old['supplement']['controller_runtime']['identity'],'predecessor implementation substituted')
 terminal(store,a,p,proof)
 require(c['predecessor_OperationalContextId']==old['identities']['OperationalContextId'] and c['predecessor_chain_digest']==old['identities']['continuation_chain_digest'],'correction ancestry changed')
 release,ids=identities(amendment,c,dict(old['identities'],release_authority=PREVIOUS))
 require(ids==spec['identities'] and store.applicability==dict(ids,authorization_id=p['invocation_identity']['authorization_id']),'context ancestry substituted')
 for name in ('changes','authority_invariants','anchor_projection','anchor_op','ancestor_ops'):setattr(owner,name,old[name])
 owner.identities=ids;owner.supplement=json.loads(canonical(old['supplement']))
 owner.supplement['controller_runtime']={'identity':runtime['identity'],'authority':spec['amendment'],'corrections':spec['continuation']}
 owner.ancestry=old['ancestry']+[{'terminal_attempt_amendment':amendment['id'],'release_authority':release,'implementation_continuation':c['continuation_id'],**ids}]
 owner.run6={'release_authority':release,'proposal':p,'amendment':a,'selection':s,'predecessor':proof,'continuation':c}
 return ids

def verify_authorization(auth):
 g=auth.context_binding.governance;g.verify();op=json.loads(auth.operational_binding)
 require(set(op)-{'dispatch_authorization'}=={'governance','released_launch','invocation_identity','context_identities'} and op['governance']==g.spec,'authorization context substituted')
 expected=json.loads(canonical(g.run6['predecessor']['authorization']));expected.update(g.run6['proposal']['invocation_identity']);expected.pop('operational_binding')
 actual=dict(auth.__dict__);actual.pop('operational_binding');actual['context_binding']={'path':str(auth.context_binding.path),'capture_commit':auth.context_binding.capture_commit}
 if actual['state']=='ACTIVE':require_issued(auth);expected['state']='ACTIVE'
 require(json.loads(canonical(actual))==expected,'successor authority expanded or substituted')
 oldop=json.loads(g.run6['predecessor']['authorization']['operational_binding'])
 require(op['released_launch']==oldop['released_launch'] and op['invocation_identity']==g.run6['proposal']['invocation_identity'],'launch or invocation substitution')
 return op

def issuance_expectation(auth):
 g=auth.context_binding.governance
 return {'authority':'Architect','decision':'AUTHORIZE_EXACT_TERMINAL_ATTEMPT_ISSUANCE',
  'proposal':g.run6['amendment']['proposal'],'amendment':g.spec['amendment'],
  'continuation':g.spec['continuation'],'release_authority':g.run6['release_authority'],
  'OperationalContextId':g.identities['OperationalContextId'],
  'continuation_chain_digest':g.identities['continuation_chain_digest'],
  'predecessor':g.run6['proposal']['predecessor'],'automatic_retry':False}

def verify_specific_grant(selection,expected):
 require(selection['mode']=='ISSUED' and selection['specific_invocation_authorization'] is not None,'specific Architect r10 issuance absent')
 grant=read(selection['specific_invocation_authorization'])
 require(set(grant)==set(expected)|{'authority_source'} and all(grant[k]==v for k,v in expected.items()),'wrong specific issuance decision')
 require(read(grant['authority_source'])==dict(expected,channel='user'),'unattributed specific issuance')
 return grant

def require_issued(auth):
 g=auth.context_binding.governance;g.verify();s=selected()
 grant=verify_specific_grant(s,issuance_expectation(auth))
 q=read(s['qualification'])
 require(q['result']=='PASS' and q['amendment']==g.spec['amendment'] and
  q['controller_runtime']==g.run6['amendment']['controller_runtime'] and
  q['accepted_proposal']==g.run6['amendment']['proposal'],'transition production qualification absent')
 return grant

def derive_dispatch(auth):
 g=auth.context_binding.governance;p=g.run6['proposal'];op=json.loads(auth.operational_binding)
 mode=selected()['mode']
 d=dict(g.run6['predecessor']['dispatch']);d.update(g.identities);d.update(op['context_identities'])
 d.update(invocation_identity=p['invocation_identity'],decision='PROPOSED_DISPATCH' if mode=='PREPARED' else 'DISPATCH_AUTHORIZED',parent_dispatch=p['dispatch'],
  attempt_authority=g.spec['amendment'],accepted_attempt_binding=g.run6['amendment']['proposal'],
  authority_source=g.run6['amendment']['authority_source'],release_authority=g.run6['release_authority'])
 original=dict(op);original.pop('dispatch_authorization',None)
 d['all_authorized_bindings']=dict(d['all_authorized_bindings'],audit=p['audit'],operational_binding_sha256=digest(original))
 return d

def verify_dispatch(auth,decision):
 auth.context_binding.governance.verify()
 if selected()['mode']=='ISSUED':require_issued(auth)
 require(decision==derive_dispatch(auth),'dispatch derivation substituted')
 return 'PROSPECTIVE' if selected()['mode']=='PREPARED' else 'ISSUED'

def readiness(auth,store,historical,check_scopes,legacy_check):
 g=auth.context_binding.governance;g.verify();r=peer(g.run6['predecessor']['governance']['run5']['amendment'],'readiness');r.pop('immutable_witness',None)
 require(r['SupervisorInstanceId']==g.run6['proposal']['bindings']['current_supervisor'] and r['SupervisorSuccessionHead']==g.run6['proposal']['bindings']['succession_head'],'supervisor substitution');return r
