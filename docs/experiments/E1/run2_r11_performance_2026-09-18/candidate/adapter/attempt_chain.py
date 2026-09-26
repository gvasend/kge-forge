"""Prepared authenticated attempt ancestry. No implicit successor or retry grant.

Historical evaluation is reused only through a content-bound qualified capture.
All underlying immutable witnesses and mutable source hashes are revalidated.
Ownership is observed separately and never stored in the eligibility cache.
"""
import json
from pathlib import Path
from .context_projection import canonical,digest,sha,read_exact
from .controller_authority_store import current,ControllerAuthorityStore,outside,read_authority_ref
from .attempt_context import require,read,ident,unseal,identities,peer
from .continuation_envelope import seal,BODY_KEYS
from .terminal_attempt import classify
from .invocation_attempt import predecessor_no_effects
from .attempt_ownership import observe,attribute

from .history_catalogs import historical_store
from .validation_spans import measured

RULES=('authenticated_exact_ancestry','closed_predecessor_audits','terminal_pre_model_no_effects',
 'attributable_non_effecting_final_disposition_after_terminal',
 'attempt_scoped_ownership','no_unknown_or_conflicting_owner','exact_current_reservation_and_lifecycle',
 'no_surviving_predecessor_scope','specific_successor_Architect_authorization',
 'no_inherited_state_ownership_counters_namespace','no_automatic_retry')

def state_of(governance):
 return governance['run7'] if 'run7' in governance else governance['run6']

def selected(store=None):
 store=store or current();require(store is not None,'private store required')
 s=json.loads(store.resolve(store.applicability['authorization_id']+':attempt-chain'))
 require(set(s)=={'mode','amendment','continuation','specific_invocation_authorization','qualification'},'selection shape')
 require(s['mode'] in ('PREPARED','ISSUED'),'unknown selection');return s

@measured('attempt_history_historical_capture')
def historical_capture(a):
 proof=read(a['predecessor_capture'])
 require(proof['publication']==a['predecessor_publication'],'capture publication substitution')
 pending=[(proof,a['predecessor_publication'])];seen=set()
 while pending:
  node,pin=pending.pop();key=digest(pin)
  require(key not in seen,'recursive or repeated history');seen.add(key)
  publication=json.loads(read_exact(pin['path'],pin['sha256']))
  with historical_store(publication['selected_store']) as old:
   old.verify_immutable_witness(node['immutable_witness'])
   require(json.loads(old.resolve(node['authorization']['authorization_id']))==node['authorization'],'captured authorization substituted')
   dispatch_id=publication['dispatch']['authority_id'] if 'dispatch' in publication else publication['dispatch_ref']
   require(json.loads(old.resolve(dispatch_id))==node['dispatch'],'captured dispatch substituted')
   require(node['governance']['identities']=={k:old.applicability[k] for k in node['governance']['identities']},'captured context ancestry substituted')
   for path,h in node['mutable'].items():read_exact(path,h)
   # Original runtimes remain immutable engineering/release dependencies.
   if 'controller_runtime' in publication:
    runtime=json.loads(old.resolve(publication['controller_runtime']['authority_id']))
    require(runtime['identity']==publication['controller_runtime_identity'],'historical runtime identity')
    require({p.name:sha(p.read_bytes()) for p in (Path(runtime['root'])/'adapter').glob('*.py')}==runtime['files'],'historical implementation changed')
   else:
    runtime=json.loads(old.resolve(node['governance']['run2']['candidate']['implementation']['authority_id']))
    require(runtime['identity']=='sha256:'+digest(runtime['inventory']),'historical implementation inventory')
    for path,h in runtime['inventory'].items():read_exact(path,node['mutable'].get(path,h))
  g=node['governance']
  state=state_of(g) if 'run7' in g or 'run6' in g else g.get('run5')
  if state:
   conf=state['amendment'].get('predecessor_verifier')
   if conf:
    read_exact(conf['path'],conf['sha256']);read_exact(conf['python'],conf['python_sha256'])
   pending.append((state['predecessor'],state['amendment']['predecessor_publication']))
 return proof

def predecessor_nodes(proof):
 nodes=[];node=proof
 while 'terminal' in node:
  nodes.append(node)
  g=node['governance']
  if 'run7' not in g and 'run6' not in g:break
  node=state_of(g)['predecessor']
 require('run5' in node['governance'],'missing pre-issuance history anchor')
 failed=node['governance']['run5']['proposal']
 predecessor_no_effects(failed)
 return list(reversed(nodes)),failed['predecessor']

def classify_terminal(rows,terminal,identity):
 """Proposed narrow material extension, not a change to historical recovery.

 Only a final-disposition telemetry suffix naming the exact authoritative
 terminal event may follow it. No heartbeats, actions, new lifecycle facts,
 provider events or unbound/uncertain final assertions are admitted.
 """
 suffix=[];prefix=list(rows)
 while prefix and prefix[-1].get('schema')=='E1-RUN-CONTROL-1' and prefix[-1].get('event')=='final_disposition':
  suffix.append(prefix.pop())
 require(len(suffix)<=1,'repeated terminal telemetry')
 if suffix:
  require(bool(prefix) and prefix[-1].get('event')=='authorization_lifecycle_terminal','terminal telemetry lacks lifecycle predecessor')
  final=prefix[-1];row=suffix[0];details=row['details']
  require(row['cycle']==0 and row['identity']['authorization_id']==identity,'unattributed terminal telemetry')
  require(details=={'disposition':'CANCELLED','ownership':'RELEASED','provider_uncertainty':None,
   'terminal_event_id':final['event_id'],'uncertainty':None},'nonmatching terminal telemetry')
 return classify(prefix,terminal['lifecycle'],terminal['actions'],None,None,identity)

@measured('attempt_history_ancestry')
def ancestry(proof,p):
 nodes,failed=predecessor_nodes(proof)
 expected=[{k:failed[k] for k in ('authorization_id','audit','audit_sha256')}]
 for node in nodes:
  t=node['terminal'];identity=node['authorization']['authorization_id']
  raw=read_exact(t['audit'],t['audit_sha256'])
  from .run_control import events
  rows=events(Path(t['audit'])) # validates telemetry correlation/hash ordering
  require(classify_terminal(rows,t,identity)=='ACTIVE_CANCELLED_PRE_MODEL_NO_EFFECTS','predecessor outside selected safe class')
  expected.append({'authorization_id':identity,'audit':t['audit'],'audit_sha256':t['audit_sha256']})
 require(p['predecessors']==expected,'missing/reordered/substituted attempt ancestry')
 require(len({n['authorization_id'] for n in expected})==len(expected),'duplicate attempt identity')
 owner,scope,_=observe(proof['authorization']['ownership_ledger'])
 return attribute(owner,scope,[n['authorization_id'] for n in expected],p['invocation_identity'],p['audit'])

@measured('attempt_history_decision')
def decision(spec):
 store=current();s=selected();require(s['amendment']==spec['amendment'] and s['continuation']==spec['continuation'],'unselected amendment')
 amendment=read(spec['amendment']);a=unseal(amendment,'E1-RUN2-ATTEMPT-CHAIN-AMENDMENT')
 require(a['schema']=='E1-RUN2-ATTEMPT-CHAIN-1' and a['rules']==list(RULES),'attempt policy changed')
 p=read(a['proposal'])
 require(read(a['authority_source'])=={'authority':'Architect','channel':'user',
  'decision':'QUALIFY_ATTEMPT_SCOPED_OWNERSHIP_AND_PREPARE_SUCCESSOR',
  'predecessor_release_authority':a['predecessor_release_authority'],
  'predecessor_publication':a['predecessor_publication'],'rules':list(RULES),'issuance_authorized':False},'unattributed preparation')
 require(p['invocation_identity']['authorization_id']==store.applicability['authorization_id'],'unselected invocation')
 require(p['schema']=='PROPOSED-AUTHENTICATED-ATTEMPT-CHAIN-1' and not p['automatic_retry'] and
  p['proposed_initial_state']=='INACTIVE' and p['ownership']=='NONE' and not any(p['inheritance'].values()),'inherited attempt authority')
 require(p['dispatch']==a['parent_dispatch'],'dispatch substituted')
 parent=read(a['parent_dispatch']);require(parent['decision']=='DISPATCH_AUTHORIZED' and parent['authority']=='Architect','original dispatch absent')
 c=read(spec['continuation']);body={k:c[k] for k in BODY_KEYS}
 require(c==seal(body,c['approval']) and c['approval'] is None,'unapproved continuation changed')
 require(c['classification']=='NON_MATERIAL_IMPLEMENTATION_CONTINUATION' and body['authority_invariants']==p['bindings'],'correction changes invariant')
 require(read(body['evidence'])['status']=='PASS_SYNTHETIC_CORRECTIONS_NON_ADOPTED','missing correction qualification')
 runtime=read(a['controller_runtime']);root=Path(runtime['root']);outside(root,store.catalog['programmer_roots'])
 require(runtime['identity']=='sha256:'+digest(runtime['files']),'runtime identity')
 require(Path(__file__).resolve().parent==root/'adapter' and {f.name:sha(f.read_bytes()) for f in (root/'adapter').glob('*.py')}==runtime['files'],'unaccounted runtime')
 for row in body['artifacts']:
  require(sha(read_authority_ref(row['new_content']))==row['new_sha256']==runtime['files'][Path(row['path']).name],'unqualified correction content')
 return s,amendment,a,c,p,runtime

def verify(owner):
 spec=owner.spec;store=current()
 require(spec['schema']==7 and digest(spec)==owner._issued_digest,'context changed')
 s,amendment,a,c,p,runtime=decision(spec)
 proof=historical_capture(a);old=proof['governance'];oldop=json.loads(proof['authorization']['operational_binding'])
 require(proof['dispatch']['release_authority']==a['predecessor_release_authority'],'wrong release predecessor')
 expected=dict(state_of(old)['proposal']['bindings']);expected.update(old['identities'])
 expected.update({k:proof['context'][k] for k in ('FullContextDigest','ModelPayloadDigest','ModelProjectionBindingDigest')})
 expected.update(release_authority=a['predecessor_release_authority'],controller_runtime_identity=old['supplement']['controller_runtime']['identity'])
 require(p['bindings']==expected,'task/profile/payload/budget/transmission/supervisor changed')
 require(p['dispatch']==state_of(old)['proposal']['dispatch'],'original dispatch ancestry changed')
 for k in ('release_basis','release_decision','released_profile','clearance'):require(spec[k]==oldop['governance'][k],'released content replaced')
 ancestry(proof,p)
 require(c['predecessor_OperationalContextId']==old['identities']['OperationalContextId'] and c['predecessor_chain_digest']==old['identities']['continuation_chain_digest'],'continuation ancestry changed')
 release,ids=identities(amendment,c,dict(old['identities'],release_authority=a['predecessor_release_authority']))
 require(ids==spec['identities'] and store.applicability==dict(ids,authorization_id=p['invocation_identity']['authorization_id']),'context selection mismatch')
 for name in ('changes','authority_invariants','anchor_projection','anchor_op','ancestor_ops'):setattr(owner,name,old[name])
 owner.identities=ids;owner.supplement=json.loads(canonical(old['supplement']))
 owner.supplement['controller_runtime']={'identity':runtime['identity'],'authority':spec['amendment'],'corrections':spec['continuation']}
 owner.ancestry=old['ancestry']+[{'attempt_chain_amendment':amendment['id'],'release_authority':release,'implementation_continuation':c['continuation_id'],**ids}]
 owner.run7={'release_authority':release,'proposal':p,'amendment':a,'selection':s,'predecessor':proof,'continuation':c}
 return ids

def verify_authorization(auth):
 g=auth.context_binding.governance;g.verify();op=json.loads(auth.operational_binding)
 require(set(op)-{'dispatch_authorization'}=={'governance','released_launch','invocation_identity','context_identities'} and op['governance']==g.spec,'authorization context')
 expected=json.loads(canonical(g.run7['predecessor']['authorization']));expected.update(g.run7['proposal']['invocation_identity']);expected.pop('operational_binding')
 actual=dict(auth.__dict__);actual.pop('operational_binding');actual['context_binding']={'path':str(auth.context_binding.path),'capture_commit':auth.context_binding.capture_commit}
 if actual['state']=='ACTIVE':require_issued(auth);expected['state']='ACTIVE'
 require(json.loads(canonical(actual))==expected,'authorization substituted')
 oldop=json.loads(g.run7['predecessor']['authorization']['operational_binding'])
 require(op['released_launch']==oldop['released_launch'] and op['invocation_identity']==g.run7['proposal']['invocation_identity'],'invocation/launch changed')
 return op

def require_issued(auth):
 g=auth.context_binding.governance;g.verify();s=selected()
 require(s['mode']=='ISSUED' and s['specific_invocation_authorization'] is not None,'specific Architect attempt-chain adoption/issuance absent')
 expected={'authority':'Architect','decision':'ADOPT_EXACT_ATTEMPT_CHAIN_AND_AUTHORIZE_SPECIFIC_INVOCATION',
  'proposal':g.run7['amendment']['proposal'],'amendment':g.spec['amendment'],'continuation':g.spec['continuation'],
  'release_authority':g.run7['release_authority'],**g.identities,'predecessors':g.run7['proposal']['predecessors'],'automatic_retry':False}
 grant=read(s['specific_invocation_authorization'])
 require(set(grant)==set(expected)|{'authority_source'} and all(grant[k]==v for k,v in expected.items()),'wrong specific attempt-chain authorization')
 require(read(grant['authority_source'])==dict(expected,channel='user'),'unattributed specific authority')
 q=read(s['qualification'])
 require(q['result']=='PASS' and q['amendment']==g.spec['amendment'] and q['controller_runtime']==g.run7['amendment']['controller_runtime'] and q['accepted_proposal']==g.run7['amendment']['proposal'],'missing complete production qualification')
 return grant

def derive_dispatch(auth):
 g=auth.context_binding.governance;p=g.run7['proposal'];op=json.loads(auth.operational_binding)
 d=dict(g.run7['predecessor']['dispatch']);d.update(g.identities);d.update(op['context_identities'])
 d.update(invocation_identity=p['invocation_identity'],decision='PROPOSED_DISPATCH' if selected()['mode']=='PREPARED' else 'DISPATCH_AUTHORIZED',parent_dispatch=p['dispatch'],attempt_authority=g.spec['amendment'],
  accepted_attempt_binding=g.run7['amendment']['proposal'],authority_source=g.run7['amendment']['authority_source'],release_authority=g.run7['release_authority'])
 original=dict(op);original.pop('dispatch_authorization',None)
 d['all_authorized_bindings']=dict(d['all_authorized_bindings'],audit=p['audit'],operational_binding_sha256=digest(original))
 return d

def verify_dispatch(auth,decision):
 auth.context_binding.governance.verify()
 if selected()['mode']=='ISSUED':require_issued(auth)
 require(decision==derive_dispatch(auth),'dispatch substituted');return 'PROSPECTIVE' if selected()['mode']=='PREPARED' else 'ISSUED'

def readiness(auth,store,historical,check_scopes,legacy_check):
 g=auth.context_binding.governance;g.verify()
 node=g.run7['predecessor']
 while 'run7' in node['governance'] or 'run6' in node['governance']:node=state_of(node['governance'])['predecessor']
 a=node['governance']['run5']['amendment']
 r=peer(a,'readiness');r.pop('immutable_witness',None)
 require(r['SupervisorInstanceId']==g.run7['proposal']['bindings']['current_supervisor'] and r['SupervisorSuccessionHead']==g.run7['proposal']['bindings']['succession_head'],'supervisor substituted')
 return r
